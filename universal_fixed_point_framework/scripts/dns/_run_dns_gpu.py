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
DNS GPU 加速扫描 (N=128, CuPy)

利用 RTX 5060 大幅加速，首次具备足够的惯性区解析能力。

参数:
  N=128, ν=0.01 (Re_λ≈100), kf=1.0
  energy_controlled: target_energy=0.05, amp=5.0
  T=60, T_stats=30

预期: k_max/k_η ≈ 7.6, 约 1.5-2 倍频程惯性区
"""
import sys, os, time, json, numpy as np
from pathlib import Path
from dataclasses import asdict

# 需要 torch/lib 中的 nvrtc DLL
torch_lib = r"C:\Users\qinxi\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib"
if os.path.exists(torch_lib):
    os.environ.setdefault("CUDA_PATH", os.path.dirname(torch_lib))
    os.environ["PATH"] = torch_lib + ";" + os.environ.get("PATH", "")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paperX_dns_turbulence_gpu import PseudoSpectralDNS3DGPU, DNSConfig
from paperX_dns_turbulence import EnergySpectrumAnalyzer

OUTPUT_DIR = Path(__file__).resolve().parents[2] / 'dns_output'
OUTPUT_DIR.mkdir(exist_ok=True)
SUMMARY_FILE = OUTPUT_DIR / 'gpu_summary.json'


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


def run_single(cfg, tag, original_stdout):
    log_file = OUTPUT_DIR / f"{tag}.log"
    npz_file = OUTPUT_DIR / f"{tag}.npz"
    sys.stdout = TeeLogger(log_file, original_stdout)

    k_eta_est = (cfg.force_amp / cfg.nu**3)**0.25
    k_max = cfg.N / 3.0
    print("=" * 65)
    print(f"DNS GPU: {tag}")
    print(f"  N={cfg.N}³, Re_λ={cfg.Re_lambda:.0f}, ν={cfg.nu:.6f}")
    print(f"  kf={cfg.force_kf}, amp={cfg.force_amp}, type={cfg.force_type}")
    print(f"  E_target={cfg.target_energy}, T={cfg.T_total}, T_stats={cfg.T_stats_start}")
    print(f"  k_η(est)={k_eta_est:.1f}, k_max={k_max:.1f}, ratio={k_max/k_eta_est:.1f}")
    print("=" * 65)

    t0 = time.time()
    dns = PseudoSpectralDNS3DGPU(cfg)
    dns.run(verbose=True)
    elapsed = time.time() - t0

    k, Ek_avg = dns.get_time_averaged_spectrum()
    if Ek_avg is None:
        sys.stdout = original_stdout
        return None

    epsilon_avg = np.mean([e for t_e, e in dns.dissipation_history if t_e >= cfg.T_stats_start])

    analyzer = EnergySpectrumAnalyzer(k, Ek_avg, epsilon=epsilon_avg, nu=cfg.nu)
    analysis = analyzer.to_dict(force_kf=cfg.force_kf)
    fit = analysis["fit"]
    silence = analysis.get("silence")

    result = {
        "tag": tag,
        "elapsed": elapsed,
        "final_energy": float(dns.energy_history[-1][1]) if dns.energy_history else 0,
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
        energy_history=np.array(dns.energy_history),
        slope=result["slope"], C_K=result["C_K"], S_spec=result["S_spec"])

    print(f"\n结果:")
    print(f"  最终能量: {result['final_energy']:.4e}")
    print(f"  斜率: {result['slope']:.4f} (目标 -1.667, 偏差 {result['slope']+5/3:.4f})")
    print(f"  拟合: k∈[{result['k_min_fit']:.1f},{result['k_max_fit']:.1f}], {result['n_points_fit']}点")
    print(f"  C_K: {result['C_K']:.3f}, S_spec: {result['S_spec']:.6f}, R²: {result['R2']:.4f}")
    print(f"  耗时: {elapsed:.0f}s ({elapsed/60:.1f}min)")

    sys.stdout = original_stdout
    return result


def main():
    original_stdout = sys.stdout
    results = []
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE, 'r') as f:
            results = json.load(f)

    # GPU N=128 扫描参数 (energy_controlled 模式)
    RUNS = [
        dict(N=128, Re_lambda=100.0, nu=0.01, dt=0.004, T_total=60.0, T_stats_start=30.0,
             force_kf=1.0, force_amp=5.0, force_type="energy_controlled",
             target_energy=0.05, seed=42, tag="gpu_N128_E005_amp5"),
        dict(N=128, Re_lambda=100.0, nu=0.01, dt=0.004, T_total=60.0, T_stats_start=30.0,
             force_kf=1.0, force_amp=10.0, force_type="energy_controlled",
             target_energy=0.10, seed=42, tag="gpu_N128_E010_amp10"),
        dict(N=128, Re_lambda=200.0, nu=0.005, dt=0.004, T_total=60.0, T_stats_start=30.0,
             force_kf=1.0, force_amp=5.0, force_type="energy_controlled",
             target_energy=0.05, seed=42, tag="gpu_N128_Re200_E005_amp5"),
    ]

    start_idx = len(results)
    for i in range(start_idx, len(RUNS)):
        params = RUNS[i]
        tag = params.pop("tag")
        cfg = DNSConfig(**params)
        
        print(f"\n{'='*65}")
        print(f"GPU 扫描 [{i+1}/{len(RUNS)}]: {tag}")
        print(f"{'='*65}")
        
        result = run_single(cfg, tag, original_stdout)
        if result is None:
            break
        results.append(result)
        with open(SUMMARY_FILE, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        params["tag"] = tag  # restore

    print(f"\n完成。")
    for r in results:
        print(f"  {r['tag']:30s} slope={r.get('slope', 'N/A')} C_K={r.get('C_K', 'N/A')}")


if __name__ == "__main__":
    main()
