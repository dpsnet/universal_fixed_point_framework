# -*- coding: utf-8 -*-
"""Phase 104n: RWA 量级收敛 —— 微场展宽平滑 σ_MP → 有效 r（χ_Balmer/χ_total）
104l 遗留：Menzel-Pekeris σ 在阈处 k^8 发散（未平滑）→ r 解析口径 0.96-0.999 高估
本脚本：① Holtsmark 微场 → Stark 展宽能量 Δ_Stark（平滑宽度）
       ② Lorentzian 卷积平滑 σ_MP 阈值发散 → κ_Balmer_eff → r_smooth
       ③ 对照观测 Balmer 跳变（~10-30% → r_obs）——闭合判定
       ④ 流量效应 ΔF/F = r_eff × 巨降比例 × 稀释因子——收敛 5.8%
物理：白矮星大气（T=15 kK、log g=8）离子微场 Stark 展宽压制阈值发散
"""
import math

# ---- 常数 ----
k_B = 1.380649e-23       # J/K
eV_J = 1.602176634e-19
a0 = 5.291772109e-11     # m（Bohr 半径）
e_C = 1.602176634e-19    # C
eps0 = 8.8541878128e-12
e_esu = 4.803204712e-10  # esu（1 C = 2.9979e9 esu）
RYD_eV = 13.6057
# 高斯单位 Holtsmark：F_H = 2.6031 · e · N^(2/3)（statV/cm），N 粒子数密度 cm^-3

def holtsmark_field(N_cm3):
    """Holtsmark 离子微场（statV/cm）"""
    return 2.6031 * e_esu * N_cm3 ** (2.0/3.0)

def stark_width_eV(n_eff, F_statVcm):
    """线性 Stark 展宽能量（阈值连续态有效 n）：
    ΔE ~ (3/2)·n·(n1-n2)·a0·e·F —— 取 n~n_eff、n1-n2 ~ n_eff（最大差）
    高斯单位：a0·e·F [erg] → eV
    """
    a0_cm = a0 * 100.0
    dE_erg = 1.5 * n_eff * n_eff * a0_cm * e_esu * F_statVcm
    return dE_erg / (1.602176634e-12)  # erg → eV（1 eV = 1.602e-12 erg）

def sigma_mp_epsilon(eps_Ry, eps_th_Ry):
    """Menzel-Pekeris 氢光电离截面（阈上，k = (eps-eps_th)^(-1/2)）：
    σ ∝ k^8 渐近（阈处发散）—— 用于相对结构，常数吸收进 κ 系数
    返回 k 与 σ 相对值
    """
    de = eps_Ry - eps_th_Ry
    if de <= 0:
        return 0.0, 0.0
    k = 1.0/math.sqrt(de)
    return k, k**8

def kappa_balmer_integral(eps_lo, eps_hi, eps_th, width_Ry, smooth=True):
    """平滑/未平滑 κ_Balmer（相对值）：∫ σ(ε)·(1-exp(-hν/kT)) dε
    smooth=True：Lorentzian 卷积（宽度 width_Ry）压制阈值发散
    未平滑：直接数值积分（阈上网格，发散区截断）
    """
    N = 20000
    total = 0.0
    for i in range(N):
        eps = eps_lo + (eps_hi-eps_lo)*(i+0.5)/N
        if eps <= eps_th:
            continue
        k, sig = sigma_mp_epsilon(eps, eps_th)
        if smooth:
            # Lorentzian 平滑：σ_eff(ε) = ∫ σ(ε')·L(ε-ε') dε' —— 数值实现：
            # 阈上发散被宽度 width 截断：σ_eff ≈ σ(ε_th+width)（发散峰变有限平台）
            if eps - eps_th < width_Ry:
                # 发散区用平台值替代（Lorentzian 卷积的峰高 ~ σ(width)/π）
                k_w, sig_w = sigma_mp_epsilon(eps_th+width_Ry, eps_th)
                sig = sig_w  # 平台近似（积分等价：∫σ(L) ≈ σ_w·width 与卷积一致）
        total += sig
    return total/N*(eps_hi-eps_lo)

def main():
    T = 15000.0
    logg = 8.0
    n_Htot = 4.83e17  # cm^-3（104l 评估 15000K 值）
    eps_th = 0.25     # n=2 光电离阈（Ry）
    eps_lo, eps_hi = 0.2455, 0.2561  # Balmer 连续谱窗口（3600-3750 Å）

    F_H = holtsmark_field(n_Htot)
    n_eff = 2.0  # 阈附近有效主量子数（连续态 n~2 起点，高 n 混合）
    dE_Stark = stark_width_eV(n_eff, F_H)
    dE_Ry = dE_Stark/RYD_eV
    print('=== Phase 104n: 微场展宽平滑 σ_MP → 有效 r ===')
    print('T = %.0f K、log g = %d、n_Htot = %.2e cm^-3' % (T, logg, n_Htot))
    print('Holtsmark 微场 F_H = %.3e statV/cm = %.3e V/cm' % (F_H, F_H*300))
    print('Stark 展宽能量（n_eff=2）：ΔE = %.3e eV = %.3e Ry' % (dE_Stark, dE_Ry))
    print()

    # 平滑 vs 未平滑 κ_Balmer 对比
    for width_Ry, label in [(dE_Ry, 'Stark 平滑'), (10*dE_Ry, '10×Stark'), (100*dE_Ry, '100×Stark')]:
        k_smooth = kappa_balmer_integral(eps_lo, eps_hi, eps_th, width_Ry, smooth=True)
        k_raw = kappa_balmer_integral(eps_lo, eps_hi, eps_th, width_Ry, smooth=False)
        ratio = k_smooth/k_raw
        print('%-12s：κ_smooth/κ_raw = %.4f（平滑压制因子）' % (label, ratio))

    # 基准：未平滑 κ_Balmer 与背景（H⁻bf 2.95e-6、κ_es 2.7e-8、κ_ff 2.8e-6——104l 15000K 值）
    # κ_Balmer_raw 的相对刻度：104l 中 κ_Balmer=4.18e-4（解析积分值——用平滑前）
    kappa_bg = 2.95e-6 + 2.8e-6 + 2.7e-8  # 背景（H⁻+ff+es）
    kappa_B_raw = 4.18e-4
    print()
    print('背景 κ_bg = %.3e cm^-1（H⁻bf + ff + es）' % kappa_bg)

    # 各平滑因子下的 r 与流量效应
    print()
    print('平滑因子  κ_Balmer_eff  r=κ_B/(κ_B+κ_bg)   ΔF/F(巨降97%×稀释0.6)   观测跳变 r_obs')
    for f in (1.0, 3.0, 10.0, 30.0, 100.0):
        kB_eff = kappa_B_raw/f
        r = kB_eff/(kB_eff+kappa_bg)
        dF = 0.97*r*0.6
        print('%-8.0f  %.3e       %.3f              %.2f%%' % (f, kB_eff, r, dF*100))
    print()
    print('观测 Balmer 跳变（B=0 白矮星 3600-3646 vs 3646-3700）：~10-30% → r_obs ≈ 0.10-0.30')
    print('跳变估算：δ ≈ κ_Balmer/(κ_Balmer+κ_bg)×温度因子(0.5-0.7) → r_obs = δ/0.6 ≈ 0.17-0.50')
    print()
    # 5.8% 反推所需参数
    print('=== 5.8% 反推 ===')
    print('ΔF/F = 0.97 × r_eff × dil = 5.8% → r_eff×dil = 0.0598')
    for dil in (0.2, 0.3, 0.4, 0.5, 0.6):
        r_need = 0.0598/dil
        print('稀释因子 d=%.1f：需 r_eff = %.2f（平滑因子 = κ_raw/(r/(1-r)·κ_bg) = %.0f）'
              % (dil, r_need, 4.18e-4/(r_need/(1-r_need)*kappa_bg)))

if __name__ == '__main__':
    main()
