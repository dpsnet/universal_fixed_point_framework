# -*- coding: utf-8 -*-
"""Phase 104c: 混合机制检验——A = (高n光电离 + H⁻ + ff)/(n2 + 高n + H⁻ + ff)
正确 Kramers 权重：σ_n(ν) ∝ (1/n⁵)(ν_n/ν)³ = 64/n¹¹ @ Balmer 带（ν=3.4 eV）
诊断：通道占比总量级能否解释 A_fit 0.10-0.47
"""
import math

RY = 13.6
KB_EV = 8.617e-5
ALPHA = 1.0/137.02876
A0 = 0.529e-8
H_P = 6.626e-27
ME_G = 9.109e-28
KB_ERG = 1.381e-16
NH = 1e15
NU_B = 3.4   # Balmer 带光子能量 eV

SIG2_TH = (64*math.pi/(3*math.sqrt(3)))*ALPHA*A0**2   # σ 基准（1/n⁵ 前的系数）

def sig_n(n, nu=NU_B):
    """σ_n(ν) ∝ (1/n⁵)(ν_n/ν)³——ν_n = R/n²"""
    vn = RY/n**2
    return SIG2_TH * (1.0/n**5) * (vn/nu)**3

def N_n(n, T):
    kT = KB_EV*T
    return n**2 * math.exp(-RY*(1-1/n**2)/kT)

def saha_ion_frac(T, nH=NH):
    kT = KB_EV*T
    C = 2.41e21*(T/300.0)**1.5*1e-6
    ne = math.sqrt(nH*C*2.0*math.exp(-RY/kT))
    return ne/nH, ne

def kap_Hm(T, ne):
    kT_erg = KB_ERG*T
    Keq = (H_P**2/(2*math.pi*ME_G*kT_erg))**1.5 * math.exp(0.755/(KB_EV*T))
    return NH*ne*Keq*1e-17   # σ_H⁻~1e-17

def kap_ff(T, ne, x):
    return ne*(x*NH)*6.692e-39

print('=== 混合机制：全通道占比（正确 1/n¹¹ 权重）===')
print('%-6s | %-9s | %-9s | %-9s | %-9s | %-9s | %-8s | %-8s' %
      ('T', 'κ_n2', 'Σκ_高n', 'κ_H⁻', 'κ_ff', '背景总', 'A混合', 'A_fit'))
for T in (12000, 15000, 20000):
    x, ne = saha_ion_frac(T)
    kn2 = N_n(2, T)*NH*sig_n(2)
    khn = sum(N_n(n, T)*NH*sig_n(n) for n in range(3, 7))
    kHm = kap_Hm(T, ne)
    kff = kap_ff(T, ne, x)
    kb = kHm + kff
    Amix = (khn + kb) / (kn2 + khn + kb)
    Af = 0.10*(KB_EV*T/1.03)**3
    print('%-6d | %.2e | %.2e | %.2e | %.2e | %.2e | %.4f | %.4f'
          % (T/1000, kn2, khn, kHm, kff, kb, Amix, Af))

print()
print('=== 分解（12kK）===')
T = 12000
x, ne = saha_ion_frac(T)
kn2 = N_n(2, T)*NH*sig_n(2)
print('σ2(Balmer带) = %.2e cm²' % sig_n(2))
for n in (3, 4, 5, 6):
    print('n=%d: σ=%.2e, N/nH=%.2e, κ=%.2e' % (n, sig_n(n), N_n(n, T), N_n(n, T)*NH*sig_n(n)))
print('κ_H⁻=%.2e, κ_ff=%.2e, κ_n2=%.2e' % (kap_Hm(T, ne), kap_ff(T, ne, x), kn2))

print()
print('=== 判定 ===')
print('正确权重下：n2 主导 %.0f×（vs 高n+背景）→ A混合 ~ %.4f（12kK）'
      % (kn2/(sum(N_n(n,T)*NH*sig_n(n) for n in range(3,7))+kap_Hm(T,ne)+kap_ff(T,ne,x)),
         (sum(N_n(n,T)*NH*sig_n(n) for n in range(3,7))+kap_Hm(T,ne)+kap_ff(T,ne,x))/(kn2+sum(N_n(n,T)*NH*sig_n(n) for n in range(3,7))+kap_Hm(T,ne)+kap_ff(T,ne,x))))
print('混合机制（高n+背景）总量级不足——A_fit 0.10-0.47 需非通道解释（RWA 模型残余结构）')
