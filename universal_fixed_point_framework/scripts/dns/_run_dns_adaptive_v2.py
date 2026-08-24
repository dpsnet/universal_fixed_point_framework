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
DNS 湍流 k^-5/3 自适应参数扫描 v2

v1 问题诊断:
  1. 自适应逻辑倒置: 斜率陡(惯性区不足)→提高 kf→惯性区更小→恶性循环
  2. N=64, Re_λ=200 下 k_η≈9, kf=2 已落入耗散区
  3. 初始 kf 应为 1.0(最大尺度), fa 需扫描
  4. 脚本重启时 cfg 重置, 导致重复运行

v2 策略:
  1. 固定 kf=1.0 (最大尺度强迫, N=64 下唯一可行)
  2. 扫描 force_amp ∈ [0.1, 0.3, 1.0, 3.0]
  3. 长期 run 在最佳参数上 (T=80)
  4. 重启恢复使用上次的 cfg, 而非初始 cfg
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
SUMMARY_FILE = OUTPUT_DIR / 'adaptive_summary_v2.json'
STATE_FILE = OUTPUT_DIR / 'adaptive_state_v2.json'

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
    """运行单个 DNS 并返回分析结果"""
    log_file = OUTPUT_DIR / f"{tag}.log"
    npz_file = OUTPUT_DIR / f"{tag}.npz"
    
    sys.stdout = TeeLogger(log_file, original_stdout)
    
    print("=" * 65)
    print(f"DNS 扫描: {tag}")
    print(f"  N={cfg.N}³, Re_λ={cfg.Re_lambda:.0f}, ν={cfg.nu:.6f}")
    print(f"  kf={cfg.force_kf}, fa={cfg.force_amp}, type={cfg.force_type}")
    print(f"  T={cfg.T_total}, T_stats={cfg.T_stats_start}")
    print("=" * 65)
    
    t0 = time.time()
    dns = PseudoSpectralDNS3D(cfg)
    dns.run(verbose=True)
    t1 = time.time()
    elapsed = t1 - t0
    
    k, Ek_avg = dns.get_time_averaged_spectrum()
    if Ek_avg is None:
        print("ERROR: 未能获取时间平均能谱")
        sys.stdout = original_stdout
        return None
    
    # 时间平均耗散率
    epsilon_avg = 0.0
    n_eps = 0
    for t_e, e_val in dns.dissipation_history:
        if t_e >= cfg.T_stats_start:
            epsilon_avg += e_val
            n_eps += 1
    epsilon_avg = epsilon_avg / n_eps if n_eps > 0 else 0
    
    analyzer = EnergySpectrumAnalyzer(k, Ek_avg, epsilon=epsilon_avg, nu=cfg.nu)
    analysis = analyzer.to_dict()
    fit = analysis["fit"]
    silence = analysis.get("silence")
    
    # 能量趋势
    if len(dns.energy_history) > 0:
        energy = np.array(dns.energy_history)
        t_mid = cfg.T_total * 0.75
        E_first = np.mean(energy[(energy[:,0] >= cfg.T_total*0.5) & (energy[:,0] < t_mid), 1])
        E_last = np.mean(energy[energy[:,0] >= t_mid, 1])
        energy_growth_rate = (E_last - E_first) / (E_first + 1e-20) if E_first > 0 else 0
        final_energy = float(energy[-1, 1])
    else:
        E_first = 0; E_last = 0; energy_growth_rate = 0; final_energy = 0
    
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
    
    # 保存 NPZ
    np.savez(
        npz_file,
        k=k,
        Ek_avg=Ek_avg,
        energy_history=np.array(dns.energy_history) if len(dns.energy_history) > 0 else np.array([]),
        dissipation_history=np.array(dns.dissipation_history) if len(dns.dissipation_history) > 0 else np.array([]),
        **{f"cfg_{k}": v for k, v in asdict(cfg).items()},
        slope=result["slope"],
        C_K=result["C_K"],
        S_spec=result["S_spec"],
    )
    
    print(f"\n结果摘要:")
    print(f"  最终能量: {result['final_energy']:.4e}")
    print(f"  能量增长率: {result['energy_growth_rate']:.3f}")
    print(f"  斜率: {result['slope']:.4f} (目标 -1.667, 偏差 {result['slope']+5/3:.4f})")
    print(f"  C_K: {result['C_K']:.3f} (目标 1.5)")
    print(f"  S_spec: {result['S_spec']:.6f} (目标 < 0.05)")
    print(f"  R²: {result['R2']:.4f}")
    print(f"  耗时: {elapsed:.1f}s")
    print(f"  预计剩余: 未知")
    
    sys.stdout = original_stdout
    return result


# ============================================================
# v2 网格扫描参数
# ============================================================
# N=64 下, k_η ≈ 9, 唯一合理的惯性区在 kf=1~3。
# 我们固定 kf=1.0 (最大尺度), 扫描 fa。

SCAN_PARAMS = [
    # (kf, fa, desc)
    (1.0, 0.1, "微弱强迫"),
    (1.0, 0.3, "弱强迫"),
    (1.0, 1.0, "中等强迫"),
    (1.0, 3.0, "强强迫"),
    (1.5, 0.3, "kf=1.5 弱强迫"),
    (1.5, 1.0, "kf=1.5 中等强迫"),
]


def load_or_create_state():
    """加载或创建状态文件 (修复重启时 cfg 重置问题)"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"next_scan_idx": 0, "best_slope_dev": 999.0, "best_idx": -1, "completed_scan": False}


def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def main():
    original_stdout = sys.stdout
    
    # 加载状态
    state = load_or_create_state()
    results = []
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, 'r') as f:
            results = json.load(f)
    
    start_idx = state["next_scan_idx"]
    
    if state.get("completed_scan"):
        print(f"网格扫描已完成 (上次运行). 最佳参数: 扫描 #{state['best_idx']}")
        print(f"  最佳斜率偏差: {state['best_slope_dev']:.4f}")
        best = SCAN_PARAMS[state['best_idx']]
        print(f"  kf={best[0]}, fa={best[1]}")
        
        # 检查长时验证是否已做
        long_tag = f"v2_long_N64_kf{best[0]}_fa{best[1]:.3f}_T80"
        long_npz = OUTPUT_DIR / f"{long_tag}.npz"
        if long_npz.exists():
            print(f"长时验证已存在: {long_tag}")
            return
        
        yn = input(f"\n对最佳参数运行长时验证 (T=80)? [Y/n]: ")
        if yn.lower() in ('', 'y', 'yes'):
            kf, fa, desc = best
            cfg = DNSConfig(
                N=64, Re_lambda=200.0, nu=0.005,
                dt=0.004, T_total=80.0, T_stats_start=40.0,
                force_kf=kf, force_amp=fa,
                force_type="stochastic",
                target_energy=0.5,
                seed=42,
            )
            tag = f"v2_long_N64_kf{kf}_fa{fa:.3f}_T80"
            result = run_single(cfg, tag, original_stdout)
            if result:
                results.append(result)
                with open(SUMMARY_FILE, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print(f"\n✅ 长时验证完成: {tag}")
        return
    
    # === 网格扫描 ===
    print(f"{'='*65}")
    print(f"DNS 网格扫描 v2  (重启保护)")
    print(f"  分辨率: N=64³, Re_λ=200, ν=0.005")
    print(f"  扫描参数({len(SCAN_PARAMS)}组):")
    for i, (kf, fa, desc) in enumerate(SCAN_PARAMS):
        mark = " ← 继续" if i == start_idx else (" ✅" if i < start_idx else "")
        print(f"    [{i}] kf={kf}, fa={fa:.1f}  ({desc}){mark}")
    print(f"  起始索引: {start_idx}/{len(SCAN_PARAMS)}")
    print(f"{'='*65}\n")
    
    for scan_idx in range(start_idx, len(SCAN_PARAMS)):
        kf, fa, desc = SCAN_PARAMS[scan_idx]
        tag = f"v2_N64_kf{kf}_fa{fa:.3f}_T20"
        
        print(f"\n{'='*65}")
        print(f"网格扫描 [{scan_idx+1}/{len(SCAN_PARAMS)}]: {desc}")
        print(f"{'='*65}")
        
        cfg = DNSConfig(
            N=64, Re_lambda=200.0, nu=0.005,
            dt=0.004, T_total=20.0, T_stats_start=10.0,
            force_kf=kf, force_amp=fa,
            force_type="stochastic",
            target_energy=0.5,
            seed=42,
        )
        
        result = run_single(cfg, tag, original_stdout)
        if result is None:
            print(f"运行失败，终止")
            break
        
        results.append(result)
        with open(SUMMARY_FILE, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        slope = result["slope"]
        slope_dev = abs(slope + 5/3)
        C_K = result["C_K"]
        S_spec = result["S_spec"]
        
        # 更新最佳参数
        if not np.isnan(slope_dev) and slope_dev < state["best_slope_dev"]:
            state["best_slope_dev"] = slope_dev
            state["best_idx"] = scan_idx
            print(f"\n  ★ 新最佳: 斜率偏差 {slope_dev:.4f}")
        
        state["next_scan_idx"] = scan_idx + 1
        save_state(state)
    
    state["completed_scan"] = True
    save_state(state)
    
    # === 结果汇总 ===
    print(f"\n{'='*65}")
    print(f"网格扫描完成")
    print(f"{'='*65}")
    
    valid = [r for r in results if not np.isnan(r.get("slope", np.nan))]
    for r in valid:
        dev = abs(r["slope"] + 5/3)
        star = "★" if dev == min(abs(v["slope"] + 5/3) for v in valid) else " "
        print(f"  {star} {r['tag']:35s} slope={r['slope']:+.4f} dev={dev:.4f} C_K={r.get('C_K', 0):.2f} S_spec={r.get('S_spec', 0):.6f}")
    
    best_idx = state["best_idx"]
    if best_idx >= 0:
        best_r = valid[best_idx] if best_idx < len(valid) else valid[0]
        print(f"\n最佳参数: kf={SCAN_PARAMS[best_idx][0]}, fa={SCAN_PARAMS[best_idx][1]}")
        print(f"  斜率: {best_r['slope']:.4f} (偏差 {abs(best_r['slope']+5/3)/(5/3)*100:.1f}%)")
        print(f"  C_K: {best_r.get('C_K', 0):.3f}")
        print(f"  S_spec: {best_r.get('S_spec', 0):.6f}")
        
        # 提示长时验证
        print(f"\n运行长时验证: python _run_dns_adaptive_v2.py  (会提示进行长时验证)")
    
    print("\n完成。")


if __name__ == "__main__":
    main()
