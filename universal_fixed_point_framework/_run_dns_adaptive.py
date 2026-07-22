"""
DNS 湍流 k^-5/3 自适应参数扫描

策略：
1. 先运行短时长（T=20）快速评估能量稳态；
2. 根据能量趋势调整 force_amp（epsilon_target）；
3. 若能量稳态但无惯性区，拓宽 force_kf；
4. 找到稳态湍流参数后，延长 T=80 做完整验证。
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
SUMMARY_FILE = OUTPUT_DIR / 'adaptive_summary.json'

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
    print(f"自适应扫描: {tag}")
    print(f"  分辨率: {cfg.N}³, Re_λ={cfg.Re_lambda}")
    print(f"  force_type={cfg.force_type}, force_amp={cfg.force_amp}, force_kf={cfg.force_kf}")
    print(f"  T_total={cfg.T_total}, T_stats_start={cfg.T_stats_start}")
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
    energy = np.array(dns.energy_history)
    t_mid = cfg.T_total * 0.75
    E_first = np.mean(energy[(energy[:,0] >= cfg.T_total*0.5) & (energy[:,0] < t_mid), 1])
    E_last = np.mean(energy[energy[:,0] >= t_mid, 1])
    energy_growth_rate = (E_last - E_first) / (E_first + 1e-20) if E_first > 0 else 0
    
    result = {
        "tag": tag,
        "elapsed": elapsed,
        "final_energy": float(energy[-1, 1]),
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
        energy_history=energy,
        dissipation_history=np.array(dns.dissipation_history),
        **{f"cfg_{k}": v for k, v in asdict(cfg).items()},
        slope=result["slope"],
        C_K=result["C_K"],
        S_spec=result["S_spec"],
    )
    
    print(f"\n结果摘要:")
    print(f"  最终能量: {result['final_energy']:.4e}")
    print(f"  能量增长率: {result['energy_growth_rate']:.3f}")
    print(f"  斜率: {result['slope']:.4f}")
    print(f"  C_K: {result['C_K']:.3f}")
    print(f"  S_spec: {result['S_spec']:.6f}")
    print(f"  耗时: {elapsed:.1f}s")
    
    sys.stdout = original_stdout
    return result


def decide_next_params(prev: dict, iteration: int) -> dict:
    """根据上一轮结果决定下一组参数"""
    cfg = prev["cfg"]
    E = prev["final_energy"]
    growth = prev["energy_growth_rate"]
    slope = prev["slope"]
    C_K = prev["C_K"]
    
    # 默认复制当前参数
    next_cfg = cfg.copy()
    next_cfg["T_total"] = 20.0
    next_cfg["T_stats_start"] = 10.0
    reasons = []
    
    # 规则 1：能量过低 → 提高注入率
    if E < 0.01 or growth < -0.2:
        next_cfg["force_amp"] *= 3.0
        reasons.append(f"能量过低(E={E:.2e})或衰减，提高 force_amp 3x")
    # 规则 2：能量过高或快速增长 → 降低注入率
    elif E > 0.5 or growth > 0.3:
        next_cfg["force_amp"] *= 0.5
        reasons.append(f"能量过高(E={E:.2e})或快速增长，降低 force_amp 0.5x")
    # 规则 3：能量稳态但斜率过陡（能量堆积低 k）→ 拓宽 forcing 带
    elif not np.isnan(slope) and slope < -2.5:
        next_cfg["force_kf"] = min(next_cfg.get("force_kf", 2.0) + 1.0, 8.0)
        reasons.append(f"斜率过陡({slope:.2f})，拓宽 force_kf 到 {next_cfg['force_kf']}")
    # 规则 4：能量稳态但 C_K 过低 → 微调注入率
    elif not np.isnan(C_K) and C_K < 0.8:
        next_cfg["force_amp"] *= 1.3
        reasons.append(f"C_K 偏低({C_K:.3f})，微调提高 force_amp")
    elif not np.isnan(C_K) and C_K > 2.5:
        next_cfg["force_amp"] *= 0.8
        reasons.append(f"C_K 偏高({C_K:.3f})，微调降低 force_amp")
    else:
        reasons.append("参数接近目标，准备进入长时验证")
    
    return next_cfg, reasons


def is_success(r: dict) -> bool:
    """判断是否达到验证目标"""
    E = r["final_energy"]
    growth = r["energy_growth_rate"]
    slope = r["slope"]
    C_K = r["C_K"]
    S_spec = r["S_spec"]
    
    energy_ok = 0.05 <= E <= 0.5 and abs(growth) <= 0.2
    slope_ok = not np.isnan(slope) and abs(slope + 5/3) < 0.20
    ck_ok = not np.isnan(C_K) and abs(C_K - 1.5) / 1.5 < 0.30
    silence_ok = not np.isnan(S_spec) and S_spec < 0.05
    
    return energy_ok and slope_ok and ck_ok and silence_ok


def main():
    original_stdout = sys.stdout
    
    # 初始参数
    cfg = DNSConfig(
        N=64,
        Re_lambda=200.0,
        nu=1/200.0,
        dt=0.004,
        T_total=20.0,
        T_stats_start=10.0,
        force_kf=2.0,
        force_amp=1.0,
        force_type="energy_injection",
        target_energy=0.5,
    )
    
    max_iter = 8
    results = []
    
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, 'r') as f:
            results = json.load(f)
        print(f"已加载历史扫描结果: {len(results)} 轮")
    
    for iteration in range(len(results), max_iter):
        tag = f"vA{iteration}_N{cfg.N}_kf{cfg.force_kf}_fa{cfg.force_amp:.3f}_T20"
        
        print(f"\n{'='*65}")
        print(f"自适应扫描第 {iteration+1}/{max_iter} 轮: {tag}")
        print(f"{'='*65}")
        
        result = run_single(cfg, tag, original_stdout)
        if result is None:
            print("运行失败，终止扫描")
            break
        
        results.append(result)
        with open(SUMMARY_FILE, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        if is_success(result):
            print(f"\n✅ 找到满意参数！进入长时验证...")
            # 延长运行
            cfg.T_total = 80.0
            cfg.T_stats_start = 40.0
            final_tag = f"vA_final_N{cfg.N}_kf{cfg.force_kf}_fa{cfg.force_amp:.3f}_T80"
            final_result = run_single(cfg, final_tag, original_stdout)
            if final_result:
                results.append(final_result)
                with open(SUMMARY_FILE, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
            break
        
        # 决定下一轮参数
        next_cfg_dict, reasons = decide_next_params(result, iteration)
        print(f"\n下一轮调整:")
        for reason in reasons:
            print(f"  - {reason}")
        
        cfg = DNSConfig(**next_cfg_dict)
    
    print(f"\n{'='*65}")
    print(f"自适应扫描完成，共 {len(results)} 轮")
    print(f"{'='*65}")
    
    # 打印最佳结果
    valid = [r for r in results if not np.isnan(r.get("slope", np.nan))]
    if valid:
        best = min(valid, key=lambda r: abs(r["slope"] + 5/3))
        print(f"\n最佳结果: {best['tag']}")
        print(f"  能量: {best['final_energy']:.4e}")
        print(f"  斜率: {best['slope']:.4f} (偏差 {abs(best['slope']+5/3)/(5/3)*100:.1f}%)")
        print(f"  C_K: {best['C_K']:.3f}")
        print(f"  S_spec: {best['S_spec']:.6f}")


if __name__ == "__main__":
    main()
