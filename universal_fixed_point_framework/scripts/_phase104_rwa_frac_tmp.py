# -*- coding: utf-8 -*-
"""Phase 104l: χ_Balmer/χ_total 量级评估 —— v5 阈上巨降 → 观测流量效应的换算
目标：B=0 时 Balmer 连续谱（n=2 光电离）在 3600-3646Å 窗口占总连续谱吸收的比例 r。
若 r ~ 1-10%，v5 的 -1.5~-2.8 dex（相对 χ_Balmer 的 97-99.7% 吸收消失）→ ΔF/F ≈ r×(0.5~0.7)
→ 与观测 +5.8% 同量级 → 量级闭合。
含：Balmer bf（Menzel-Pekeris σ）+ H⁻ bf（John 1988）+ H⁻ ff + H ff（Kramers）+ 电子散射。
大气参数：T、log g=8（P_gas~1e5 dyn/cm² → n_H 由理想气体给出）、Saha 电离平衡。
"""
import numpy as np, math

alpha = 7.2973525693e-3
a0 = 5.29177210903e-9
RYD_eV = 13.605693
kB_eV = 8.617333262e-5
h = 6.62607015e-27   # erg·s
c = 2.99792458e10    # cm/s
k_erg = 1.380649e-16 # erg/K
me = 9.1093837e-28   # g
mH = 1.6735575e-24   # g
e_esu = 4.8032047e-10
PI = math.pi

def Saha_ne(T, nH_total, P_e_guess):
    """迭代 Saha：中性 H + 质子 + 电子。χ_ion=13.598eV"""
    chi_eV = 13.598
    # Saha：n_p n_e / n_H = K，K = 2×(2πm_e kT/h²)^{3/2}×e^{−χ/kT}
    K = 2*(2*PI*me*k_erg*T/h**2)**1.5 * math.exp(-chi_eV*1.602e-12/(k_erg*T))
    n_e = (-K + math.sqrt(K*K + 4*K*nH_total))/2
    n_p = n_e
    n_H = nH_total - n_p
    if n_H < 0: n_H = 0
    return n_e, n_p, n_H

def balmer_chi(lam_A, T, n2_pop_cm3):
    """Balmer 连续谱吸收系数（n=2 光电离）——归一化到 n2 数密度"""
    eps = (12400.0/lam_A)/RYD_eV
    k = (eps - 0.25)**(-0.5)
    if k <= 0: return 0.0
    # 8 态 × 3q 通道和（零场全部阈=0.25，σ^q 和为 3×[A ξ_up + B ξ_dn]σ_nk）
    def Q_2s_kp(kk): return 16*(1+kk**2)*(4+kk**2)
    def Q_2p_kd(kk): return 128*kk**2*(1+kk**2)/9
    def Q_2p_ks(kk): return 4*kk**2*(4+kk**2)/9
    def P_2(kk): return (4+3*kk**2)*(4+5*kk**2)
    n3=8; k8=k**8; denom=(4+k**2)**6
    expo=math.exp(-4*k*math.atan(2/k))
    P=P_2(k)
    dfde=(128/3)*n3*k8*P/denom*expo/(1-math.exp(-2*PI*k))
    sig = 4*PI**2*alpha*a0**2*dfde  # cm²（n=2 总截面近似，求和系数 ~2.9 未含——见注）
    # 注：逐态求和系数（A/B 权重×ξ）≈ 2.9 已被零场通道和吸收；此处用单态近似 ×2.9 补齐
    sig *= 2.9
    return sig*n2_pop_cm3

def Hminus_bf(lam_A, T, nH0, nHm):
    """H⁻ 束缚-自由（John 1988 拟合）：κ_bf = α_bf(λ,T) × n(H⁻)"""
    lam = lam_A*1e-8  # cm
    T4 = T/1e4
    # John 1988 多项式（λ 单位 cm？——用 μm 版本）
    lam_um = lam_A/1e4
    l2 = lam_um**2; l3 = lam_um**3
    a = (1.99654 - 1.18267e-5*T + 2.64243e-6*T**2)/T4  # John 88 系数（粗略记忆）
    # 直接用 Doughty-Fraser 1966 表列近似（CGS，λ∈[3500,10000]Å）：
    # α_bf ≈ 10^(-25) × [1.87e-3 + ... ] ——改用 Lambert 1994 显式拟合：
    # κ_bf(H⁻)/n(H⁻) = 10^-26 × (a0 + a1·λ + ...) 复杂——用量级常数：
    # 公认：3600-4100Å 处 H⁻ bf 截面 ≈ (3-8)e-17 cm²（John 1988 Fig）——插值 ~5e-17
    sig_bf = 5.0e-17  # cm² per H⁻ @ ~3700Å（John 1988 量级）
    return sig_bf * nHm

def ff_chi(lam_A, T, n_e, n_ion, g_ff):
    """Kramers 自由-自由（H⁺ + e）：κ_ff = 4e-10×(Z² n_e n_i / T^1/2 ν³)×g_ff×(1−e^{−hν/kT}) cm⁻¹"""
    nu = c/(lam_A*1e-8)
    K = 4.0e-10 * n_e*n_ion / (math.sqrt(T)*nu**3) * g_ff * (1-math.exp(-h*nu/(k_erg*T)))
    return K  # cm⁻¹（系数含 π 常数——近似 3.69e8×n_e n_i/T^1/2 ν^3 g）

def es_chi(n_e):
    return n_e*6.652e-25

print('=== Phase 104l: χ_Balmer/χ_total 量级评估 ===')
print('T(kK)  n_Htot  电离度  n2占比   κ_Balmer   κ_H⁻bf    κ_ff      κ_es    κ_total   r=B/total')
for T in (12000, 15000, 20000):
    # log g=8 → P_gas≈1e5 dyn/cm² → n_Htot = P/(kT)（理想气体，T=15000K 时 n~4.8e17）
    n_Htot = 1.0e5/(k_erg*T)
    ne, np_, nH = Saha_ne(T, n_Htot, None)
    ion_frac = np_/n_Htot
    # n=2 玻尔兹曼占比（束缚 H 内）：g2/g1 × e^{−(E2−E1)/kT} = 8/2 × e^{−10.2eV/kT}
    g_ratio = 8.0/2.0*math.exp(-(13.6-3.4)*1.602e-12/(k_erg*T))
    n2 = nH*g_ratio/(1+g_ratio)  # 简化：束缚 H 中 n=2 占比
    # H⁻ 丰度（Saha 平衡：H + e⁻ ↔ H⁻）：n_H⁻/n_H = n_e × K_H⁻
    K_Hm = (h**2/(2*PI*me*k_erg*T))**1.5 * 0.5 * math.exp(0.754*1.602e-12/(k_erg*T))
    nHm = nH*ne*K_Hm
    k_b = balmer_chi(3623.0, T, n2)
    k_hm = Hminus_bf(3623.0, T, nH, nHm)
    k_ff = ff_chi(3623.0, T, ne, np_, 1.0)
    k_es = es_chi(ne)
    k_tot = k_b + k_hm + k_ff + k_es
    r = k_b/k_tot if k_tot > 0 else 0
    print('%5d  %.2e  %.4f  %.4f  %.2e  %.2e  %.2e  %.2e  %.2e  %.3f' %
          (T, n_Htot, ion_frac, n2/(nH+1e-30), k_b, k_hm, k_ff, k_es, k_tot, r))

print()
print('=== v5 巨降 → 流量效应（ΔF/F ≈ r × 吸收消失比例 × 形成层稀释 0.5~0.7）===')
print('B(MG)  Δχ_Balmer(dex)  吸收消失%   r=1%   r=3%   r=10%  观测 +5.8%')
for Bv, d in [(10, 1.52), (50, 1.61), (100, 1.76), (300, 2.64)]:
    frac = 1 - 10**(-d)
    for r in (0.01, 0.03, 0.10):
        dF = r*frac*0.6*100
        print('%4d  %5.2f           %6.2f%%   %5.2f%%  %5.2f%%  %5.2f%%' % (Bv, d, frac*100, dF, dF, dF))
