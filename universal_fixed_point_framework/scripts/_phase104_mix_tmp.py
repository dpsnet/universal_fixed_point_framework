# -*- coding: utf-8 -*-
"""Phase 104b: 混合背景模型（H⁻ + ff）——C 独立计算 + 15kK 偏差联合检验
A(T) = 1/(1 + N₂σ2 / [n_H⁻σ_H⁻ + n_e·n_H+·κ̄_ff])
- σ2 = 2.47e-19（Kramers n=2 光电离，已核对文献 2e-19 ✓）
- κ̄_ff = 6.7e-39（Kramers 每对 ff，12kK）
- n_H⁻ = nH·n_e·K_eq(T)——K_eq = (h²/2πm_e kT)^{3/2}·e^{0.755/kT}
- σ_H⁻ ~ 5e-18 至 1e-17（3700Å 估算——参数扫描）
"""
import math

RY = 13.6
KB_EV = 8.617e-5
H_P = 6.626e-27
ME_G = 9.109e-28
KB_ERG = 1.381e-16

SIG2 = 2.469e-19
KFF = 6.692e-39
NH = 1e15

def saha_ion_frac(T, nH=NH):
    kT = KB_EV*T
    C = 2.41e21*(T/300.0)**1.5*1e-6
    ne = math.sqrt(nH*C*2.0*math.exp(-RY/kT))
    return ne/nH, ne

def N2_frac(T):
    kT = KB_EV*T
    return 4.0*math.exp(-(RY-RY/4.0)/kT)

def n_Hm(T, ne):
    """H⁻ 密度：n_H⁻ = nH·n_e·K_eq（Saha 平衡，结合能 0.755 eV）"""
    kT_erg = KB_ERG*T
    Keq = (H_P**2/(2*math.pi*ME_G*kT_erg))**1.5 * math.exp(0.755/(KB_EV*T))
    return NH*ne*Keq, Keq

def A_mix(T, sig_Hm):
    x, ne = saha_ion_frac(T)
    N2 = N2_frac(T)*NH
    nHm, Keq = n_Hm(T, ne)
    kap_Hm = nHm*sig_Hm
    kap_ff = ne*(x*NH)*KFF
    kap_bg = kap_Hm + kap_ff
    kap_n2 = N2*SIG2
    return kap_bg/(kap_n2+kap_bg), kap_n2, kap_Hm, kap_ff

print('=== 混合背景（H⁻+ff）A(T) ===')
print('%-6s | %-8s | %-10s | %-9s | %-9s | %-9s | %-8s | %-8s' %
      ('T', 'x', 'K_eq', 'κ_n2', 'κ_H⁻', 'κ_ff', 'A', 'A_fit'))
for sig_Hm in (1e-17, 5e-18):
    print('--- σ_H⁻ = %.0e ---' % sig_Hm)
    for T in (12000, 15000, 20000):
        x, ne = saha_ion_frac(T)
        A, kn2, kHm, kff = A_mix(T, sig_Hm)
        nHm, Keq = n_Hm(T, ne)
        Af = 0.10*(KB_EV*T/1.03)**3
        print('%-6d | %.4f | %.2e | %.2e | %.2e | %.2e | %.4f | %.4f (%+.0f%%)'
              % (T/1000, x, Keq, kn2, kHm, kff, A, Af, (A-Af)/Af*100))

print()
print('=== C 独立计算（含 H⁻）===')
# C = σ2 / κ̄_bg——κ̄_bg 折算到每 e·nH+ 对
for sig_Hm in (1e-17, 5e-18):
    T = 12000
    x, ne = saha_ion_frac(T)
    nHm, _ = n_Hm(T, ne)
    kap_Hm = nHm*sig_Hm
    kap_ff = ne*(x*NH)*KFF
    kbar_bg = (kap_Hm+kap_ff)/(ne*x*NH)
    print('σ_H⁻=%.0e: κ̄_bg(每对)=%.2e → C=%.2e vs 标定 1.024e17（差 %.0f×）'
          % (sig_Hm, kbar_bg, SIG2/kbar_bg, (SIG2/kbar_bg)/1.024e17))
