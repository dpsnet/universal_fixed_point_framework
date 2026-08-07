"""
DNS 湍流数值验证 v6.1 — 恒定能量注入率 forcing + 提高 ε
  64³, Re_λ=200, force_type='energy_injection', ε_target=1.0, T=20
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import numpy as np
from pathlib import Path
from paperX_dns_turbulence import DNSConfig, PseudoSpectralDNS3D, EnergySpectrumAnalyzer

# ============================================================
# 配置与日志持久化
# ============================================================
OUTPUT_DIR = Path(__file__).resolve().parents[2] / 'dns_output'
OUTPUT_DIR.mkdir(exist_ok=True)
RUN_TAG = f"v6_1_N64_Re200_einj_1.0_T20_{int(time.time())}"
LOG_FILE = OUTPUT_DIR / f"{RUN_TAG}.log"
NPZ_FILE = OUTPUT_DIR / f"{RUN_TAG}.npz"

class TeeLogger:
    """同时输出到终端和日志文件"""
    def __init__(self, filepath):
        self.file = open(filepath, 'w', encoding='utf-8')
        self.stdout = sys.stdout
    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)
        self.file.flush()
    def flush(self):
        self.stdout.flush()
        self.file.flush()

sys.stdout = TeeLogger(LOG_FILE)

cfg = DNSConfig(
    N=64,
    Re_lambda=200.0,
    nu=1/200.0,
    dt=0.004,
    T_total=20.0,          # 快速测试
    T_stats_start=10.0,
    force_kf=2.0,
    force_amp=1.0,         # 目标能量注入率 ε_target（提高 20 倍）
    force_type="energy_injection",
    target_energy=0.5,
)

print("=" * 65)
print(f"DNS 湍流 k^-5/3 验证 v6.1 — 恒定能量注入率 forcing + 提高 ε")
print(f"  分辨率: {cfg.N}³ = {cfg.N**3:,}")
print(f"  Re_λ = {cfg.Re_lambda:.0f}, ν = {cfg.nu:.6f}")
print(f"  dt = {cfg.dt}")
print(f"  T_total = {cfg.T_total}, 统计起始: t={cfg.T_stats_start}")
print(f"  force_type = {cfg.force_type}")
print(f"  force_amp = {cfg.force_amp}, force_kf = {cfg.force_kf}")
print(f"  能谱归一化: 已修正")
print(f"  日志文件: {LOG_FILE}")
print(f"  数据文件: {NPZ_FILE}")
print("=" * 65)

t0 = time.time()
dns = PseudoSpectralDNS3D(cfg)
dns.run(verbose=True)
t1 = time.time()
elapsed = t1 - t0
print(f"\nDNS 运行完成, 耗时: {elapsed:.1f}s")

k, Ek_avg = dns.get_time_averaged_spectrum()
if Ek_avg is None:
    print("ERROR: 未能获取时间平均能谱")
    sys.exit(1)

# 修正耗散率计算
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

# 打印能谱数据
print(f"\n能谱 E(k):")
for ki in range(1, min(25, len(k))):
    print(f"  k={ki}: E(k)={Ek_avg[ki]:.6e}")

print(f"\n{'='*65}")
print(f"验证结果")
print(f"{'='*65}")

if "slope" in fit:
    slope = fit["slope"]
    slope_err = fit.get("slope_err", 0)
    print(f"\n[1/3] -5/3 斜率验证")
    print(f"  拟合范围: k ∈ [{fit.get('k_min', 0):.1f}, {fit.get('k_max', 0):.1f}]")
    print(f"  点数: {fit.get('n_points', 0)}, R²: {fit.get('R2', 0):.4f}")
    print(f"  斜率: {slope:.4f} +/- {slope_err:.4f}")
    print(f"  理论: -1.6667, 偏差: {slope + 5/3:.4f} ({abs(slope+5/3)/(5/3)*100:.1f}%)")
    if abs(slope + 5/3) < 0.10:
        print(f"  状态: ✅")
    elif abs(slope + 5/3) < 0.20:
        print(f"  状态: ⚠️ 近似通过")
    else:
        print(f"  状态: ❌")

    print(f"\n  补偿谱 k^(5/3) E(k) (期望平坦):")
    comp = analyzer.compensated_spectrum()
    for ki in range(1, min(20, len(k))):
        print(f"    k={ki}: {comp[ki]:.6e}")

if fit.get("C_K") is not None:
    print(f"\n[2/3] Kolmogorov 常数")
    print(f"  C_K = {fit['C_K']:.3f} (文献 1.5)")
    C_K_dev = abs(fit['C_K'] - 1.5) / 1.5 * 100
    print(f"  偏差: {C_K_dev:.1f}%")

silence = analysis.get("silence")
if silence:
    print(f"\n[3/3] 谱静默度")
    print(f"  S_spec = {silence['S_spec']:.6f}, γ = {silence['gamma']:.4f}")
    print(f"  k_ν = {silence['k_nu']:.1f}, 状态: {silence['interpretation']}")

n_pass = sum([
    abs(slope + 5/3) < 0.15 if "slope" in fit else False,
    True if fit.get("C_K") and abs(fit["C_K"] - 1.5)/1.5*100 < 30 else False,
    silence and silence["S_spec"] < 0.05,
])
print(f"\n验证: {n_pass}/3")
print(f"耗时: {elapsed:.1f}s")

# 保存完整结果到 NPZ
energy_history = np.array(dns.energy_history)
dissipation_history = np.array(dns.dissipation_history)
np.savez(
    NPZ_FILE,
    k=k,
    Ek_avg=Ek_avg,
    energy_history=energy_history,
    dissipation_history=dissipation_history,
    cfg_N=cfg.N,
    cfg_Re_lambda=cfg.Re_lambda,
    cfg_nu=cfg.nu,
    cfg_dt=cfg.dt,
    cfg_T_total=cfg.T_total,
    cfg_force_amp=cfg.force_amp,
    cfg_force_kf=cfg.force_kf,
    cfg_force_type=cfg.force_type,
    slope=slope if "slope" in fit else np.nan,
    slope_err=slope_err if "slope" in fit else np.nan,
    C_K=fit.get("C_K", np.nan),
    S_spec=silence["S_spec"] if silence else np.nan,
    k_nu=silence["k_nu"] if silence else np.nan,
)
print(f"\n结果已保存: {NPZ_FILE}")
