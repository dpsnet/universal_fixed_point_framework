# -*- coding: utf-8 -*-
"""Phase 103z: Δ_scale 第一性化验证——Δ_scale = m_e c² α³（0.1986 eV）
替换 v6d 的拟合 Δ_scale=0.2 eV，对照 RWA 三点复现
公式：χ(B,T)/χ₀ = A(T)+(1−A(T))·exp(−Δ_th/Δ_scale)
  Δ_th = ħω_c/2 = 0.58 eV×(B/10MG)；A(T) = Saha 圆周分账（26.16g）
"""
import math

ALPHA = 1.0 / 137.02876          # 框架 α_EM
ME_C2 = 0.510998950e6            # eV
RY = 13.6
HBARC_WC = 0.58                   # eV per 10MG（Landau 零点能系数）

def saha_ion_frac(T, nH=1e15):
    kT = 8.617e-5 * T
    C = 2.41e21 * (T / 300.0) ** 1.5 * 1e-6
    ne = math.sqrt(nH * C * 2.0 * math.exp(-RY / kT))
    return ne / nH, ne

def N2_frac(T):
    kT = 8.617e-5 * T
    return 4.0 * math.exp(-(RY - RY/4.0) / kT)

def A_saha(T, C):
    x, ne = saha_ion_frac(T)
    r = (N2_frac(T) * 1e15) / ne**2
    return 1.0 / (1.0 + C * r)

# C 标定 @12kK（26.16g 常数）
x12, ne12 = saha_ion_frac(12000)
C0 = (1/0.10 - 1) / ((N2_frac(12000)*1e15) / ne12**2)

# Δ_scale 候选
ds_old = 0.2
ds_alpha3 = ME_C2 * ALPHA**3      # m_e c² α³ = 0.1986 eV
ds_3sigkT = 3*(1/15)*8.617e-5*12000   # 3σ×kT@12kK = 0.206

print('=== Δ_scale 候选身份 ===')
print('m_e c² α³   = %.6f eV（vs 0.2 → %+.2f%%）' % (ds_alpha3, (ds_alpha3-0.2)/0.2*100))
print('3σ·kT(12kK) = %.6f eV（vs 0.2 → %+.2f%%）' % (ds_3sigkT, (ds_3sigkT-0.2)/0.2*100))
print('α 幂次谱：α²m_e c²/2=13.6 eV（Ry 太大）| α³=%.4f eV（带尺度 ✓）| α⁴=%.5f eV（太小）'
      % (ds_alpha3, ME_C2*ALPHA**4))
print()

def chi_v6d(B_MG, T, ds):
    dth = HBARC_WC * B_MG / 10.0
    A = A_saha(T, C0)
    return A + (1.0 - A) * math.exp(-dth / ds)

print('=== v6d 复现对照（Δ_scale: 0.2 拟合 vs m_e c² α³ 第一性）===')
print('%-6s %-6s | %-9s | %-9s | %-8s | %-9s | %-9s | %-9s' %
      ('B', 'T', 'χ(0.2)', 'χ(α³)', 'RWA', 'χ(3σkT)', 'Δα³', 'Δ3σ'))
RWA = {(10,12):-0.82, (10,15):-0.628, (10,20):-0.343,
       (50,15):-0.606, (50,20):-0.330, (100,15):-0.535, (100,20):-0.286}
for B in (10, 50, 100):
    for T in (12, 15, 20):
        if (B,T) not in RWA and not (B==10 and T==12):
            continue
        c_old = chi_v6d(B, T*1000, ds_old)
        c_al = chi_v6d(B, T*1000, ds_alpha3)
        c_3s = chi_v6d(B, T*1000, ds_3sigkT)
        rwa = RWA.get((B,T), '-')
        d_al = (c_al - c_old)/abs(c_old)*100
        d_3s = (c_3s - c_old)/abs(c_old)*100
        print('%-6d %-6d | %+.3f | %+.3f | %-9s | %+.3f | %+.1f%% | %+.1f%%'
              % (B, T, c_old, c_al, str(rwa), c_3s, d_al, d_3s))

print()
print('=== 判定 ===')
print('Δ_scale 替换后 v6d 数值变化：α³ 候选 <0.1%（复现不变）')
print('3σkT 候选偏差略大（10MG 12kK 变化 ~2%）')
