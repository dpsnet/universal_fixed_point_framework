"""
DNS 湍流数值验证 v3 — 修复能谱归一化 + 平衡 forcing
  48³, nu=0.005, force_amp=0.5, T=30
"""
import sys; sys.path.insert(0, '.')
import time
import numpy as np
from paperX_dns_turbulence import DNSConfig, PseudoSpectralDNS3D, EnergySpectrumAnalyzer

cfg = DNSConfig(
    N=48,
    Re_lambda=100.0,
    nu=0.005,           # 较高粘度，维持稳态
    dt=0.004,           # 时间步长
    T_total=30.0,       # 延长积分以达稳态
    T_stats_start=10.0, # 晚一些开始统计
    force_kf=2.0,       # 窄 forcing 范围
    force_amp=0.5,      # 平衡振幅 (原1.0过强)
)

print("=" * 65)
print(f"DNS 湍流 k^-5/3 验证 v3")
print(f"  分辨率: {cfg.N}³ = {cfg.N**3:,}")
print(f"  nu = {cfg.nu}, dt = {cfg.dt}")
print(f"  T_total = {cfg.T_total}, 统计起始: t={cfg.T_stats_start}")
print(f"  force_amp = {cfg.force_amp}, force_kf = {cfg.force_kf}")
print(f"  能谱归一化: 已修正")
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

# 打印能谱数据（前几个模式）
print(f"\n能谱 E(k):")
for ki in range(1, min(15, len(k))):
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

    # 补偿谱
    print(f"\n  补偿谱 k^(5/3) E(k) (期望平坦):")
    comp = analyzer.compensated_spectrum()
    for ki in range(1, min(12, len(k))):
        print(f"    k={ki}: {comp[ki]:.6e}")

if fit.get("C_K") is not None:
    print(f"\n[2/3] Kolmogorov 常数")
    print(f"  C_K = {fit['C_K']:.3f} (文献 1.5)")

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
