# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
DNS 湍流 k^-5/3 扫描 v4

v3 诊断: N=64, Re_λ=200 下 k_η ≈ 40-53 > k_max≈21, DNS 严重欠解析
v4 方案: N=64, Re_λ=100 (ν=0.01)
  - ν 增大 2x → k_η = (ε/ν³)^(1/4) 减小 ~1.68x
  - ε_target=0.03: k_η ≈ 13 → k_max/k_η ≈ 1.6 ✅
  - ε_target=0.10: k_η ≈ 18 → k_max/k_η ≈ 1.2 ⚠️
  - ε_target=0.30: k_η ≈ 23 → borderline
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import json
import numpy as np
from pathlib import Path
from dataclasses import asdict
from paperX_dns_turbulence import DNSConfig, PseudoSpectralDNS3D, EnergySpectrumAnalyzer

OUTPUT_DIR = Path(__file__).resolve().parents[2] / 'dns_output'
OUTPUT_DIR.mkdir(exist_ok=True)
SUMMARY_FILE = OUTPUT_DIR / 'adaptive_summary_v4.json'
STATE_FILE = OUTPUT_DIR / 'adaptive_state_v4.json'


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

    # 打印 k_η 预报
    k_eta_est = (cfg.force_amp / cfg.nu**3)**0.25
    k_max = cfg.N / 3.0
    print("=" * 65)
    print(f"DNS 扫描 v4: {tag}")
    print(f"  N={cfg.N}³, Re_λ={cfg.Re_lambda:.0f}, ν={cfg.nu:.6f}")
    print(f"  kf={cfg.force_kf}, ε_target={cfg.force_amp}, type={cfg.force_type}")
    print(f"  T={cfg.T_total}, T_stats={cfg.T_stats_start}")
    print(f"  k_η(est)={k_eta_est:.1f}, k_max(dealias)={k_max:.1f}, ratio={k_max/k_eta_est:.2f}")
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
        "slope": float(fit.get("slope", np.nan)),
        "slope_err": float(fit.get("slope_err", np.nan)),
        "C_K": float(fit.get("C_K", np.nan)),
        "S_spec": float(silence["S_spec"]) if silence else np.nan,
        "k_nu": float(silence["k_nu"]) if silence else np.nan,
        "R2": float(fit.get("R2", np.nan)),
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
    print(f"  斜率: {result['slope']:.4f} (目标 -1.667, 偏差 {result['slope']+5/3:.4f})")
    print(f"  C_K: {result['C_K']:.3f} (目标 1.5)")
    print(f"  S_spec: {result['S_spec']:.6f} (目标 < 0.05)")
    print(f"  k_ν(实测): {result['k_nu']:.1f}")
    print(f"  R²: {result['R2']:.4f}, 耗时: {elapsed:.1f}s")

    sys.stdout = original_stdout
    return result


# N=64, Re_λ=100 (ν=0.01), 扫描 ε_target
SCAN_PARAMS = [
    (1.0, 0.03, "很低注入, k_η≈13 ✅"),
    (1.0, 0.10, "低注入, k_η≈18 ✅"),
    (1.0, 0.30, "中注入, k_η≈23 ⚠️"),
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
        best = SCAN_PARAMS[state['best_idx']]
        long_tag = f"v4_long_N64_kf{best[0]}_fa{best[1]:.3f}_T80"
        long_npz = OUTPUT_DIR / f"{long_tag}.npz"
        if long_npz.exists():
            print(f"长时验证已有: {long_tag}")
            return
        yn = input(f"\n对最佳运行长时验证 T=80? [Y/n]: ")
        if yn.lower() in ('', 'y', 'yes'):
            kf, fa, desc = best
            cfg = DNSConfig(N=64, Re_lambda=100.0, nu=0.01,
                dt=0.004, T_total=80.0, T_stats_start=40.0,
                force_kf=kf, force_amp=fa,
                force_type="energy_injection", target_energy=0.5, seed=42)
            tag = f"v4_long_N64_kf{kf}_fa{fa:.3f}_T80"
            result = run_single(cfg, tag, original_stdout)
            if result:
                results.append(result)
                with open(SUMMARY_FILE, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
        return

    print(f"{'='*65}")
    print("DNS v4: N=64, Re_λ=100 (ν=0.01), energy_injection")
    for i, (kf, fa, desc) in enumerate(SCAN_PARAMS):
        mark = " ← 继续" if i == start_idx else (" ✅" if i < start_idx else "")
        print(f"  [{i}] kf={kf}, ε={fa:.2f}  {desc}{mark}")

    for scan_idx in range(start_idx, len(SCAN_PARAMS)):
        kf, fa, desc = SCAN_PARAMS[scan_idx]
        tag = f"v4_N64_kf{kf}_fa{fa:.3f}_T40"
        print(f"\n扫描 [{scan_idx+1}/{len(SCAN_PARAMS)}]: {desc}")

        cfg = DNSConfig(N=64, Re_lambda=100.0, nu=0.01,
            dt=0.004, T_total=40.0, T_stats_start=20.0,
            force_kf=kf, force_amp=fa,
            force_type="energy_injection", target_energy=0.5, seed=42)

        result = run_single(cfg, tag, original_stdout)
        if result is None:
            break

        results.append(result)
        with open(SUMMARY_FILE, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        slope_dev = abs(result["slope"] + 5/3)
        if not np.isnan(slope_dev) and slope_dev < state["best_slope_dev"]:
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
        print(f"  {star} {r['tag']:35s} slope={r['slope']:+.4f} dev={dev:.4f} C_K={r.get('C_K',0):.2f}")

    if state["best_idx"] >= 0:
        print(f"\n最佳: kf={SCAN_PARAMS[state['best_idx']][0]}, ε={SCAN_PARAMS[state['best_idx']][1]}")


if __name__ == "__main__":
    main()
