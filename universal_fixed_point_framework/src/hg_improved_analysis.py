"""
Hg 谱框架预测改进分析 v1.0
==========================
目的：
  系统性地分析 Hg (λ=1.0, μ*=0.11, ω_D=95K, Tc_exp=4.2K, a_exp=0.438)
  的两步方案偏差 5.32%，通过多种策略寻求改进。

策略：
  1. 实验 Tc 直接代入两步方案（绕过 McMillan 公式）
  2. ω_D 扫描：求使 McMillan Tc 匹配实验 Tc 的 ω_D 值
  3. μ* 扫描：求使 McMillan Tc 匹配实验 Tc 的 μ* 值
  4. 双峰 Einstein 谱模型：ω_E1 + ω_E2 双峰
  5. 参数空间网格扫描：(λ, ω_D) 联合优化

参考: notes/02_superconductivity/spectral_BCS_weave.md §7.5.5
"""

import numpy as np

# ============================================================
# 谱框架常数
# ============================================================
D0 = 0.122           # Δλ_min
A_BCS_WEAK = 0.567   # BCS 弱耦合值
R_WEAK = 0.874       # 弱耦合谱间隙比
D_PREFACTOR = np.sqrt(3)  # √3

def a_spectral(r, Z=1.0):
    """谱框架比例因子 a = ((1 + √3·√r/Z)/(4π) · r)^(1/3)"""
    d = D_PREFACTOR * np.sqrt(r)
    return ((1.0 + d / Z) / (4.0 * np.pi) * r) ** (1.0/3.0)

def r_from_a(a_target, Z=1.0):
    """从 a 逆解 r（二分法）"""
    lo, hi = 0.01, 2.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        a_mid = a_spectral(mid, Z)
        if a_mid < a_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def Tc_McMillan(lam, mu_star, wD):
    """McMillan T_c 公式"""
    if lam <= mu_star * (1 + 0.62 * lam):
        return 0.0
    exponent = -(1.0 + lam) / (lam - mu_star * (1.0 + 0.62 * lam))
    return (wD / 1.2) * np.exp(exponent)

def a_two_step_Tc(Tc, lam, wD):
    """
    两步方案: 给定 Tc，计算谱框架 a
    (不通过 McMillan，直接使用实验 Tc)
    """
    if Tc <= 0:
        return A_BCS_WEAK
    w_log = wD / 1.2
    if w_log <= 2 * Tc:
        return A_BCS_WEAK
    ratio = Tc / w_log
    gk_correction = ratio**2 * np.log(w_log / (2.0 * Tc))
    beta = 15.24
    r = R_WEAK * np.exp(-beta * gk_correction)
    Z = 1.0 + lam
    d = np.sqrt(3) * np.sqrt(r) / Z
    return ((1.0 + d) / (4.0 * np.pi) * r) ** (1.0/3.0)

def a_two_step(lam, mu_star, wD):
    """完整两步方案（McMillan Tc + GK r 修正 + 谱框架）"""
    Tc = Tc_McMillan(lam, mu_star, wD)
    return a_two_step_Tc(Tc, lam, wD)

def a_two_step_double_peak(lam1, lam2, wE1, wE2, mu_star, Tc_exp_guess=None):
    """
    双峰 Einstein 谱模型:
    α²F(ω) = (λ₁/2)·ω_E1·δ(ω-ω_E1) + (λ₂/2)·ω_E2·δ(ω-ω_E2)
    
    有效参数:
    λ_eff = λ₁ + λ₂
    ω_D_eff ≈ (λ₁·ω_E1 + λ₂·ω_E2) / λ_eff  (加权平均)
    ω_log_eff = exp((λ₁·ln(ω_E1) + λ₂·ln(ω_E2)) / λ_eff)
    
    先用双峰参数计算有效 McMillan Tc，再走两步方案
    """
    lam_eff = lam1 + lam2
    wD_eff = (lam1 * wE1 + lam2 * wE2) / lam_eff if lam_eff > 0 else 95.0
    w_log_eff = np.exp((lam1 * np.log(wE1) + lam2 * np.log(wE2)) / lam_eff) if lam_eff > 0 else 95.0/1.2
    
    # 用有效参数计算 Tc
    if lam_eff <= mu_star * (1 + 0.62 * lam_eff):
        return A_BCS_WEAK, {'lam_eff': lam_eff, 'wD_eff': wD_eff, 'w_log_eff': w_log_eff, 'Tc_mcm': 0}
    
    Tc_mcm = (wD_eff / 1.2) * np.exp(-(1 + lam_eff) / (lam_eff - mu_star * (1 + 0.62 * lam_eff)))
    
    if Tc_mcm <= 0:
        return A_BCS_WEAK, {'lam_eff': lam_eff, 'wD_eff': wD_eff, 'w_log_eff': w_log_eff, 'Tc_mcm': 0}
    
    # 使用双峰 ω_log 计算 GK 修正
    ratio = Tc_mcm / w_log_eff
    gk_correction = ratio**2 * np.log(w_log_eff / (2.0 * Tc_mcm))
    beta = 15.24
    r = R_WEAK * np.exp(-beta * gk_correction)
    Z = 1.0 + lam_eff
    d = np.sqrt(3) * np.sqrt(r) / Z
    a = ((1.0 + d) / (4.0 * np.pi) * r) ** (1.0/3.0)
    
    return a, {'lam_eff': lam_eff, 'wD_eff': wD_eff, 'w_log_eff': w_log_eff, 'Tc_mcm': Tc_mcm}

# ============================================================
# Hg 参数
# ============================================================
LAM_HG = 1.00
MU_HG = 0.11
WD_HG = 95.0
TC_HG_EXP = 4.2
A_HG_EXP = 0.438
A_PB_EXP = 0.415

print("=" * 76)
print("Hg 谱框架预测改进分析 v1.0")
print("=" * 76)
print(f"\nHg 标称参数: λ={LAM_HG}, μ*={MU_HG}, ω_D={WD_HG} K, Tc_exp={TC_HG_EXP} K")
print(f"  a_exp = {A_HG_EXP}")
print(f"  a_two_step (McMillan Tc = {Tc_McMillan(LAM_HG, MU_HG, WD_HG):.2f} K) = "
      f"{a_two_step(LAM_HG, MU_HG, WD_HG):.4f}")
print()

# ============================================================
# 策略 1: 实验 Tc 直接代入两步方案
# ============================================================
print("━" * 76)
print("策略 1: 实验 Tc 直接代入两步方案")
print("━" * 76)

a_Hg_expTc = a_two_step_Tc(TC_HG_EXP, LAM_HG, WD_HG)
dev_Hg_expTc = abs(a_Hg_expTc - A_HG_EXP) / A_HG_EXP * 100
print(f"  a_two_step(λ={LAM_HG}, Tc_exp={TC_HG_EXP}, ω_D={WD_HG})")
print(f"    a = {a_Hg_expTc:.4f}, a_exp = {A_HG_EXP}, 偏差 = {dev_Hg_expTc:.2f}%")
print()

# 解释: 使用实验 Tc 时，GK 修正需要的 Tc/ω_log 比不同
# 但 ω_D 可能也需要调整，因为 Tc 本身来自 McMillan 近似
# 继续尝试 ω_D 扫描

# ============================================================
# 策略 2: ω_D 扫描 — 求使 McMillan Tc 匹配实验 Tc
# ============================================================
print("━" * 76)
print("策略 2: ω_D 扫描 — 求使 McMillan Tc = 4.2 K 的 ω_D")
print("━" * 76)

best_wD = WD_HG
best_a_wD = a_two_step(LAM_HG, MU_HG, WD_HG)
best_dev_wD = abs(best_a_wD - A_HG_EXP) / A_HG_EXP * 100

for wD_test in np.arange(30, 150, 1):
    Tc_test = Tc_McMillan(LAM_HG, MU_HG, wD_test)
    if abs(Tc_test - TC_HG_EXP) < abs(Tc_McMillan(LAM_HG, MU_HG, best_wD) - TC_HG_EXP):
        best_wD = wD_test

print(f"  McMillan Tc(λ={LAM_HG}, μ*={MU_HG}, ω_D) 扫描:")
print(f"    标称 ω_D={WD_HG} K → Tc={Tc_McMillan(LAM_HG, MU_HG, WD_HG):.2f} K (偏差 {(Tc_McMillan(LAM_HG, MU_HG, WD_HG)-TC_HG_EXP)/TC_HG_EXP*100:.1f}%)")
print(f"    最优 ω_D={best_wD} K → Tc={Tc_McMillan(LAM_HG, MU_HG, best_wD):.2f} K")
Tc_opt_wD = Tc_McMillan(LAM_HG, MU_HG, best_wD)
print(f"    调整比 = {best_wD/WD_HG:.3f}")

# 用最优 ω_D 计算 a
a_opt_wD = a_two_step(LAM_HG, MU_HG, best_wD)
dev_opt_wD = abs(a_opt_wD - A_HG_EXP) / A_HG_EXP * 100
print(f"    a(ω_D={best_wD}) = {a_opt_wD:.4f}, 偏差 = {dev_opt_wD:.2f}%")

# 在最优 ω_D 附近精细扫描 a
print(f"\n  ω_D 精细扫描 (围绕 {best_wD} K):")
print(f"  {'ω_D':>6s} {'T_c':>7s} {'a':>8s} {'偏差%':>8s}")
for dw in range(-10, 11, 2):
    wd = best_wD + dw
    if wd < 20: continue
    a_wd = a_two_step(LAM_HG, MU_HG, wd)
    dev_wd = abs(a_wd - A_HG_EXP)/A_HG_EXP*100
    Tc_wd = Tc_McMillan(LAM_HG, MU_HG, wd)
    print(f"  {wd:6.0f} {Tc_wd:7.2f} {a_wd:8.4f} {dev_wd:7.2f}%")
print()

# ============================================================
# 策略 3: μ* 扫描
# ============================================================
print("━" * 76)
print("策略 3: μ* 扫描 — 求使 McMillan Tc = 4.2 K 的 μ*")
print("━" * 76)

best_mu = MU_HG
for mu_test in np.arange(0.01, 0.30, 0.001):
    Tc_test = Tc_McMillan(LAM_HG, mu_test, WD_HG)
    if abs(Tc_test - TC_HG_EXP) < abs(Tc_McMillan(LAM_HG, MU_HG, best_mu) - TC_HG_EXP):
        best_mu = mu_test

print(f"  标称 μ*={MU_HG} → Tc={Tc_McMillan(LAM_HG, MU_HG, WD_HG):.2f} K")
print(f"  最优 μ*={best_mu:.3f} → Tc={Tc_McMillan(LAM_HG, best_mu, WD_HG):.2f} K")

a_opt_mu = a_two_step(LAM_HG, best_mu, WD_HG)
dev_opt_mu = abs(a_opt_mu - A_HG_EXP)/A_HG_EXP*100
print(f"  a(μ*={best_mu:.3f}) = {a_opt_mu:.4f}, 偏差 = {dev_opt_mu:.2f}%")

print(f"\n  μ* 精细扫描:")
print(f"  {'μ*':>6s} {'T_c':>7s} {'a':>8s} {'偏差%':>8s}")
for mu in [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24]:
    a_mu = a_two_step(LAM_HG, mu, WD_HG)
    dev_mu = abs(a_mu - A_HG_EXP)/A_HG_EXP*100
    Tc_mu = Tc_McMillan(LAM_HG, mu, WD_HG)
    print(f"  {mu:6.2f} {Tc_mu:7.2f} {a_mu:8.4f} {dev_mu:7.2f}%")
print()

# ============================================================
# 策略 4: 双峰 Einstein 谱模型
# ============================================================
print("━" * 76)
print("策略 4: 双峰 Einstein 谱模型")
print("━" * 76)

# Hg 的多峰 α²F(ω) 谱有两个主要特征：
# 低能峰 (~10-15 meV, 116-174 K) — 声学声子
# 高能峰 (~30-40 meV, 348-464 K) — 光学声子
# 文献中 Hg 的 λ ≈ 1.0-1.6, 峰值分布在 10-40 meV

# 尝试几种双峰配置
configs = [
    # (λ₁, wE1_K, λ₂, wE2_K, μ*, 描述)
    (0.4, 120, 0.6, 360, 0.11, "声学 0.4+光学 0.6 (总 λ=1.0)"),
    (0.5, 120, 0.6, 360, 0.11, "声学 0.5+光学 0.6 (总 λ=1.1)"),
    (0.3, 100, 0.7, 350, 0.11, "声学 0.3+光学 0.7 (总 λ=1.0)"),
    (0.4, 140, 0.7, 400, 0.12, "声学 0.4+光学 0.7 (总 λ=1.1)"),
    (0.5, 120, 0.8, 380, 0.12, "声学 0.5+光学 0.8 (总 λ=1.3)"),
    (0.6, 130, 0.6, 370, 0.11, "声学 0.6+光学 0.6 (总 λ=1.2)"),
]

print(f"{'配置':>4s} {'λ₁':>5s} {'ω_E1(K)':>8s} {'λ₂':>5s} {'ω_E2(K)':>8s} {'μ*':>5s} "
      f"{'λ_eff':>6s} {'T_c':>7s} {'a':>8s} {'a_exp':>8s} {'偏差%':>8s}")
print("-" * 76)

best_double = (None, 999, None)
for i, (lam1, we1, lam2, we2, mu, desc) in enumerate(configs):
    a_double, params = a_two_step_double_peak(lam1, lam2, we1, we2, mu)
    dev = abs(a_double - A_HG_EXP)/A_HG_EXP*100
    Tc = params['Tc_mcm']
    print(f"  {i+1:4d} {lam1:5.2f} {we1:8.0f} {lam2:5.2f} {we2:8.0f} {mu:5.2f} "
          f"{params['lam_eff']:6.2f} {Tc:7.2f} {a_double:8.4f} {A_HG_EXP:8.4f} {dev:7.2f}%")
    if dev < best_double[1]:
        best_double = (i, dev, a_double)

if best_double[0] is not None:
    print(f"\n  最优双峰配置: #{best_double[0]+1}, a={best_double[2]:.4f}, 偏差={best_double[1]:.2f}%")
    print(f"  描述: {configs[best_double[0]][5]}")
print()

# ============================================================
# 策略 5: (λ, ω_D) 联合优化 — 求使 a 最佳匹配实验值的参数
# ============================================================
print("━" * 76)
print("策略 5: (λ, ω_D) 联合参数扫描")
print("━" * 76)
print(f"  固定 μ*={MU_HG}，扫描 λ∈[0.8,1.6], ω_D∈[50,150]")
print()

best_a = 999
best_params = (LAM_HG, WD_HG)
scan_results = []

for lam in np.arange(0.8, 1.61, 0.02):
    for wD in np.arange(50, 151, 2):
        a_test = a_two_step(lam, MU_HG, wD)
        dev = abs(a_test - A_HG_EXP)
        if dev < best_a:
            best_a = dev
            best_params = (lam, wD)

lam_opt, wD_opt = best_params
Tc_opt = Tc_McMillan(lam_opt, MU_HG, wD_opt)
a_opt_scan = a_two_step(lam_opt, MU_HG, wD_opt)
dev_opt_scan = abs(a_opt_scan - A_HG_EXP) / A_HG_EXP * 100

print(f"  全局最优:")
print(f"    λ_opt = {lam_opt:.2f}, ω_D_opt = {wD_opt:.0f} K")
print(f"    McMillan Tc = {Tc_opt:.2f} K (实验 {TC_HG_EXP} K)")
print(f"    a_opt = {a_opt_scan:.4f}, a_exp = {A_HG_EXP}")
print(f"    偏差 = {dev_opt_scan:.2f}%")
print()

# 显示最优参数附近的参数空间
print(f"  最优参数附近扫描 (λ={lam_opt:.2f}±0.10, ω_D={wD_opt:.0f}±10):")
print(f"  {'λ':>5s} {'ω_D':>6s} {'T_c':>7s} {'a':>8s} {'偏差%':>8s}")
print("-" * 38)
for lam in [lam_opt - 0.08, lam_opt - 0.04, lam_opt, lam_opt + 0.04, lam_opt + 0.08]:
    lam = round(lam, 2)
    for wD in [wD_opt - 8, wD_opt - 4, wD_opt, wD_opt + 4, wD_opt + 8]:
        if wD < 30: continue
        a_s = a_two_step(lam, MU_HG, wD)
        dev_s = abs(a_s - A_HG_EXP)/A_HG_EXP*100
        Tc_s = Tc_McMillan(lam, MU_HG, wD)
        print(f"  {lam:5.2f} {wD:6.0f} {Tc_s:7.2f} {a_s:8.4f} {dev_s:7.2f}%")
print()

# ============================================================
# 综合对比
# ============================================================
print("━" * 76)
print("综合对比: 各策略最优结果")
print("━" * 76)
print()

# Pb 参考值
print(f"{'策略':>30s} {'a_Hg':>8s} {'a_exp':>8s} {'偏差%':>8s}")
print("-" * 56)

# 原始
a_orig = a_two_step(LAM_HG, MU_HG, WD_HG)
dev_orig = abs(a_orig - A_HG_EXP)/A_HG_EXP*100
print(f"{'0. 原始 McMillan + GK + 谱框架':>30s} {a_orig:8.4f} {A_HG_EXP:8.4f} {dev_orig:7.2f}%")

# 策略1: 实验 Tc
print(f"{'1. 实验 Tc 直接代入':>30s} {a_Hg_expTc:8.4f} {A_HG_EXP:8.4f} {dev_Hg_expTc:7.2f}%")

# 策略2: 最优 ω_D
print(f"{'2. ω_D 扫描 (ω_D='+str(best_wD)+'K)':>30s} {a_opt_wD:8.4f} {A_HG_EXP:8.4f} {dev_opt_wD:7.2f}%")

# 策略3: 最优 μ*
print(f"{'3. μ* 扫描 (μ*='+f'{best_mu:.3f}'+')':>30s} {a_opt_mu:8.4f} {A_HG_EXP:8.4f} {dev_opt_mu:7.2f}%")

# 策略4: 最优双峰
if best_double[0] is not None:
    print(f"{'4. 双峰 Einstein 最优':>30s} {best_double[2]:8.4f} {A_HG_EXP:8.4f} {best_double[1]:7.2f}%")

# 策略5: 全局扫描
print(f"{'5. (λ, ω_D) 联合扫描最优':>30s} {a_opt_scan:8.4f} {A_HG_EXP:8.4f} {dev_opt_scan:7.2f}%")
print()

# Pb 参考对比
print(f"\n{'Pb 参考 (两步方案)':>30s} {a_two_step(1.55, 0.12, 105):8.4f} {A_PB_EXP:8.4f} "
      f"{abs(a_two_step(1.55, 0.12, 105)-A_PB_EXP)/A_PB_EXP*100:7.2f}%")

# ============================================================
# 参数灵敏度分析
# ============================================================
print("\n" + "━" * 76)
print("Hg 参数灵敏度分析")
print("━" * 76)

dlam = 0.05
dmu = 0.01
dwD = 5.0

a_base = a_two_step(LAM_HG, MU_HG, WD_HG)

# λ 灵敏度
a_lam_up = a_two_step(LAM_HG + dlam, MU_HG, WD_HG)
a_lam_down = a_two_step(LAM_HG - dlam, MU_HG, WD_HG)
sens_lam = (a_lam_up - a_lam_down) / (2 * dlam)

# μ* 灵敏度
a_mu_up = a_two_step(LAM_HG, MU_HG + dmu, WD_HG)
a_mu_down = a_two_step(LAM_HG, MU_HG - dmu, WD_HG)
sens_mu = (a_mu_up - a_mu_down) / (2 * dmu)

# ω_D 灵敏度
a_wD_up = a_two_step(LAM_HG, MU_HG, WD_HG + dwD)
a_wD_down = a_two_step(LAM_HG, MU_HG, WD_HG - dwD)
sens_wD = (a_wD_up - a_wD_down) / (2 * dwD)

print(f"  ∂a/∂λ (Δλ={dlam}) = {sens_lam:.4f} K⁻¹")
print(f"  ∂a/∂μ* (Δμ*={dmu}) = {sens_mu:.4f} K⁻¹")
print(f"  ∂a/∂ω_D (Δω_D={dwD}) = {sens_wD:.4f} K⁻¹")
print()
print(f"  半定量不确定度估计:")
print(f"    σ_a(λ={LAM_HG}±0.1) = {abs(sens_lam * 0.1):.4f} ({abs(sens_lam * 0.1)/a_base*100:.1f}%)")
print(f"    σ_a(μ*={MU_HG}±0.03) = {abs(sens_mu * 0.03):.4f} ({abs(sens_mu * 0.03)/a_base*100:.1f}%)")
print(f"    σ_a(ω_D={WD_HG}±10) = {abs(sens_wD * 10):.4f} ({abs(sens_wD * 10)/a_base*100:.1f}%)")
print()

# ============================================================
# 结论
# ============================================================
print("━" * 76)
print("结论: Hg 改进分析")
print("━" * 76)
print()
print(f"  Best achievable deviation with current approach: {min([dev_orig, dev_Hg_expTc, dev_opt_wD, dev_opt_mu, dev_opt_scan]):.2f}%")

best_all = min([
    ('原始', dev_orig),
    ('实验 Tc', dev_Hg_expTc),
    ('ω_D 扫描', dev_opt_wD),
    ('μ* 扫描', dev_opt_mu),
    ('双峰', best_double[1] if best_double[0] is not None else 999),
    ('联合扫描', dev_opt_scan),
], key=lambda x: x[1])

print(f"  Best strategy: {best_all[0]} ({best_all[1]:.2f}%)")
print()
print("  根本限制:")
print("    1. McMillan T_c 公式对 Hg 的 ω_D/μ* 输入敏感，且仅用两参数")
print("      无法完全描述 Hg 的多峰 α²F(ω) 谱")
print("    2. Einstein 单峰/双峰模型是严重简化——文献中 Hg 的 α²F(ω)")
print("      有至少 3-4 个特征峰分布在 5-45 meV 范围")
print("    3. 谱框架 β = 15.24 从 Pb 标定，对 Hg 不一定最优")
print()
print("  建议改进路径 (按优先级):")
print("    A. 从文献获取 Hg 的实测 α²F(ω) 谱，进行全数值")
print("       Matsubara 求和求解（优于 McMillan 近似）")
print("    B. 使用全数值 Eliashberg 求解器 (eliashberg_numerical_solver.py)")
print("       结合 Hg 实际谱函数计算 Tc 和 Δ₀")
print("    C. 将 β 作为材料依赖参数拟合，或从谱流方程第一性原理推导")
print()
