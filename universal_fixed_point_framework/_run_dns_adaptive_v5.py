"""
DNS 湍流 k^-5/3 扫描 v5

v4 诊断: energy_injection 模式实际注入率远低于 ε_target(1-5% 效率)
v5 方案: energy_controlled 模式
  - 直接维持目标能量 E_target
  - 强迫幅度正比于 (E_target - E_current) → 稳定快
  - 无需等待注入-耗散平衡 → 收敛时间 ~2-3 τ_L

参数选取:
  N=64, ν=0.01 (Re_λ≈100), kf=1.0
  target_energy=0.05 (量纲估计: 合理的大尺度能量水平)
  force_amp=0.5 (能量控制响应速率)
  T=80, T_stats=40
"""
import sys; sys.path.insert(0, '.')
import time
import json
import numpy as np
from pathlib import Path
from dataclasses import asdict
from paperX_dns_turbulence import DNSConfig, PseudoSpectralDNS3D, EnergySpectrumAnalyzer

OUTPUT_DIR = Path('dns_output')
OUTPUT_DIR.mkdir(exist_ok=True)
SUMMARY_FILE = OUTPUT_DIR / 'adaptive_summary_v5.json'
STATE_FILE = OUTPUT_DIR / 'adaptive_state_v5.json'


class TeeLogger:
    def __init__(self, filepath, stdout):
        self.file = open(filepath, 'w', encoding='utf-8')
        self.stdout = stdout
    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)
        self.file.flush()
    def flush(self):
        self.stdout.flush()
        self.file.flush()


def run_single(cfg: DNSConfig, tag: str, original_stdout):
    log_file = OUTPUT_DIR / f"{tag}.log"
    npz_file = OUTPUT_DIR / f"{tag}.npz"
    sys.stdout = TeeLogger(log_file, original_stdout)

    print("=" * 65)
    print(f"DNS v5: {tag}")
    print(f"  N={cfg.N}³, Re_λ={cfg.Re_lambda:.0f}, ν={cfg.nu:.6f}")
    print(f"  kf={cfg.force_kf}, amp={cfg.force_amp}, type={cfg.force_type}")
    print(f"  E_target={cfg.target_energy}, T={cfg.T_total}, T_stats={cfg.T_stats_start}")
    print("=" * 65)

    t0 = time.time()
    dns = PseudoSpectralDNS3D(cfg)
    dns.run(verbose=True)
    t1 = time.time()
    elapsed = t1 - t0

    k, Ek_avg = dns.get_time_averaged_spectrum()
    if Ek_avg is None:
        sys.stdout = original_stdout
        return None

    epsilon_avg = 0.0
    n_eps = 0
    for t_e, e_val in dns.dissipation_history:
        if t_e >= cfg.T_stats_start:
            epsilon_avg += e_val
            n_eps += 1
    epsilon_avg = epsilon_avg / n_eps if n_eps > 0 else 0

    analyzer = EnergySpectrumAnalyzer(k, Ek_avg, epsilon=epsilon_avg, nu=cfg.nu)
    analysis = analyzer.to_dict(force_kf=cfg.force_kf)
    fit = analysis["fit"]
    silence = analysis.get("silence")

    if len(dns.energy_history) > 0:
        energy = np.array(dns.energy_history)
        t_mid = cfg.T_total * 0.75
        E_first = np.mean(energy[(energy[:,0] >= cfg.T_total*0.5) & (energy[:,0] < t_mid), 1])
        E_last = np.mean(energy[energy[:,0] >= t_mid, 1])
        energy_growth_rate = (E_last - E_first) / (E_first + 1e-20) if E_first > 0 else 0
        final_energy = float(energy[-1, 1])
    else:
        E_first = E_last = energy_growth_rate = final_energy = 0

    result = {
        "tag": tag,
        "elapsed": elapsed,
        "final_energy": final_energy,
        "energy_first_half": float(E_first),
        "energy_last_half": float(E_last),
        "energy_growth_rate": float(energy_growth_rate),
        "slope": float(fit.get("slope", np.nan)) if "slope" in fit else np.nan,
        "slope_err": float(fit.get("slope_err", np.nan)) if "slope_err" in fit else np.nan,
        "C_K": float(fit.get("C_K", np.nan)) if "C_K" in fit else np.nan,
        "S_spec": float(silence["S_spec"]) if silence else np.nan,
        "k_nu": float(silence["k_nu"]) if silence else np.nan,
        "R2": float(fit.get("R2", np.nan)) if "R2" in fit else np.nan,
        "k_min_fit": float(fit.get("k_min", np.nan)) if "k_min" in fit else np.nan,
        "k_max_fit": float(fit.get("k_max", np.nan)) if "k_max" in fit else np.nan,
        "n_points_fit": int(fit.get("n_points", 0)) if "n_points" in fit else 0,
        "cfg": asdict(cfg),
    }

    np.savez(npz_file, k=k, Ek_avg=Ek_avg,
        energy_history=np.array(dns.energy_history) if len(dns.energy_history) > 0 else np.array([]),
        dissipation_history=np.array(dns.dissipation_history) if len(dns.dissipation_history) > 0 else np.array([]),
        **{f"cfg_{k}": v for k, v in asdict(cfg).items()},
        slope=result["slope"], C_K=result["C_K"], S_spec=result["S_spec"])

    print(f"\n结果摘要:")
    print(f"  最终能量: {result['final_energy']:.4e}")
    print(f"  能量增长率: {result['energy_growth_rate']:.3f}")
    print(f"  斜率: {result['slope']:.4f}" + (f" (偏差 {result['slope']+5/3:.4f})" if not np.isnan(result['slope']) else " (NaN)"))
    print(f"  拟合范围: k∈[{result['k_min_fit']:.1f},{result['k_max_fit']:.1f}], {result['n_points_fit']}点")
    print(f"  C_K: {result['C_K']:.3f}, S_spec: {result['S_spec']:.6f}")
    print(f"  R²: {result['R2']:.4f}, 耗时: {elapsed:.1f}s")

    sys.stdout = original_stdout
    return result


# energy_controlled 模式扫描 (v2: amp 提高 10x 以平衡耗散)
SCAN_PARAMS = [
    (1.0, 0.05, 5.0, "E_target=0.05, amp=5.0"),
    (1.0, 0.10, 10.0, "E_target=0.10, amp=10.0"),
    (1.0, 0.03, 3.0, "E_target=0.03, amp=3.0"),
]


def load_or_create_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"next_scan_idx": 0, "best_slope_dev": 999.0, "best_idx": -1, "completed_scan": False}


def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def main():
    original_stdout = sys.stdout
    state = load_or_create_state()
    results = []
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, 'r') as f:
            results = json.load(f)

    start_idx = state["next_scan_idx"]

    if state.get("completed_scan"):
        print(f"扫描已完成. 最佳参数: #{state['best_idx']}, 偏差 {state['best_slope_dev']:.4f}")
        best_params = SCAN_PARAMS[state['best_idx']]
        long_tag = f"v5_long_N64_Etarget{best_params[1]:.3f}_amp{best_params[2]:.3f}_T80"
        long_npz = OUTPUT_DIR / f"{long_tag}.npz"
        if long_npz.exists():
            print(f"长时验证已有: {long_tag}")
            return
        yn = input(f"\n对最佳运行长时验证 T=80? [Y/n]: ")
        if yn.lower() in ('', 'y', 'yes'):
            kf, et, amp, desc = best_params
            cfg = DNSConfig(N=64, Re_lambda=100.0, nu=0.01,
                dt=0.004, T_total=80.0, T_stats_start=40.0,
                force_kf=kf, force_amp=amp,
                force_type="energy_controlled", target_energy=et, seed=42)
            tag = f"v5_long_N64_Etarget{et:.3f}_amp{amp:.3f}_T80"
            result = run_single(cfg, tag, original_stdout)
            if result:
                results.append(result)
                with open(SUMMARY_FILE, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
        return

    print(f"{'='*65}")
    print("DNS v5: energy_controlled 模式")
    print(f"  N=64, Re_λ=100 (ν=0.01), kf=1.0")
    for i, (kf, et, amp, desc) in enumerate(SCAN_PARAMS):
        mark = " ← 继续" if i == start_idx else (" ✅" if i < start_idx else "")
        print(f"  [{i}] {desc}{mark}")

    for scan_idx in range(start_idx, len(SCAN_PARAMS)):
        kf, et, amp, desc = SCAN_PARAMS[scan_idx]
        tag = f"v5_N64_Etarget{et:.3f}_amp{amp:.3f}_T60"
        print(f"\n扫描 [{scan_idx+1}/{len(SCAN_PARAMS)}]: {desc}")

        cfg = DNSConfig(N=64, Re_lambda=100.0, nu=0.01,
            dt=0.004, T_total=60.0, T_stats_start=30.0,
            force_kf=kf, force_amp=amp,
            force_type="energy_controlled", target_energy=et, seed=42)

        result = run_single(cfg, tag, original_stdout)
        if result is None:
            break

        results.append(result)
        with open(SUMMARY_FILE, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        slope_dev = abs(result["slope"] + 5/3) if not np.isnan(result["slope"]) else 999.0
        if slope_dev < state["best_slope_dev"]:
            state["best_slope_dev"] = slope_dev
            state["best_idx"] = scan_idx
            print(f"  ★ 新最佳: 偏差 {slope_dev:.4f}")

        state["next_scan_idx"] = scan_idx + 1
        save_state(state)

    state["completed_scan"] = True
    save_state(state)

    print(f"\n结果汇总:")
    valid = [r for r in results if not np.isnan(r.get("slope", np.nan))]
    for r in valid:
        dev = abs(r["slope"] + 5/3)
        star = "★" if dev == min(abs(v["slope"] + 5/3) for v in valid) else " "
        print(f"  {star} {r['tag']:35s} slope={r['slope']:+.4f} dev={dev:.4f} C_K={r.get('C_K',0):.2f} n_fit={r.get('n_points_fit',0)}")

    if state["best_idx"] >= 0:
        print(f"\n最佳: #{state['best_idx']}")


if __name__ == "__main__":
    main()
