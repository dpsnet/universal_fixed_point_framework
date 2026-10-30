# -*- coding: utf-8 -*-
"""Phase 103r: v6 拓扑阈值位移模型——RWA 内生推导尝试
机制：Landau 化把连续态底抬升（零点能 ħω_c/2）→ 电离阈上移 → Balmer 跳变带
      （hν ∈ [3.4, 3.4+Δ]）部分不能电离 → 吸收系数下降
对照 RWA 表（论文 §4.8）：
  10MG: 15kK −0.628 / 20kK −0.343；50MG: −0.606/−0.330；100MG: −0.535/−0.286
  12kK 档 −0.78~−0.91
"""
import math

RY = 13.6          # eV
HBARC = 1.0        # 自然单位示意（ħc）
ME = 0.511e6       # eV/c²（用内生可替代量）

def E_n(n): return RY / (n * n)

def landau_energy(B_mg):
    """Landau 零点能 ħω_c/2（eV）——B 单位 MG（1 MG = 100 T）"""
    # ω_c = eB/m_e；ħω_c = ħeB/m_e。用常数：ħω_c(B) = 1.16 eV × (B/10 MG)
    # （10MG=10^4 T：ħω_c = 1.16 eV，零点能 0.58 eV）
    return 1.16 * (B_mg / 10.0) / 2.0

def photo_ion_cross_section(hv, thresh):
    """束缚-连续光电离截面（阈值附近）：σ ∝ (ν_th/ν)^3 × 阶跃（hν>阈值）"""
    if hv <= thresh: return 0.0
    return (thresh / hv) ** 3

def occupancy(n, T, B_mg):
    """玻尔兹曼占据（相对 n=1）：Landau 化轻微改变束缚能（暂忽略 B 依赖）"""
    kT = 8.617e-5 * T
    return math.exp(-(E_n(1) - E_n(n)) / kT)

def chi_band(B_mg, T, lam_lo, lam_hi):
    """Balmer 连续区吸收（n=2 光电离为主）：积分 hν 对应波长带"""
    # hν(eV) = 12398 / λ(Å)
    hv_lo = 12398.0 / lam_hi      # 长波端 = 低能
    hv_hi = 12398.0 / lam_lo      # 短波端 = 高能
    thresh = E_n(2)               # n=2 电离阈 3.4 eV
    thresh_B = thresh + landau_energy(B_mg)   # 磁场抬升
    N = 200
    chi = 0.0
    for i in range(N):
        hv = hv_lo + (hv_hi - hv_lo) * (i + 0.5) / N
        chi += photo_ion_cross_section(hv, thresh_B) * (thresh_B ** 2) * (1.0 / hv ** 2)
    return chi / N

def dex(B_mg, T, lam_lo, lam_hi):
    c0 = chi_band(0.0, T, lam_lo, lam_hi)
    cB = chi_band(B_mg, T, lam_lo, lam_hi)
    return math.log10(cB / c0) if c0 > 0 else -999

BLUE = (3600.0, 3640.0)
RED  = (3700.0, 3750.0)
SLOPEA = (4000.0, 4060.0)
SLOPEB = (5000.0, 5800.0)

print('=== v6 拓扑阈值位移：χ_cont(B)/χ_cont(0)（dex，负=吸收下降）===')
print('Landau 零点能：10MG=%.2f eV、50MG=%.2f eV、100MG=%.2f eV'
      % (landau_energy(10), landau_energy(50), landau_energy(100)))
print()
print('--- blue 带 (3600-3640Å) ---')
print('%-7s | %s' % ('B(MG)', 'T=12kK    T=15kK    T=20kK'))
for B in (10, 50, 100):
    row = []
    for T in (12000, 15000, 20000):
        row.append('%+.3f' % dex(B, T, *BLUE))
    print('%-7d | %s' % (B, '  '.join(row)))

print()
print('--- 带间分布（T=15kK, B=50MG）---')
for name, band in (('blue', BLUE), ('red', RED), ('slopeA', SLOPEA), ('slopeB', SLOPEB)):
    print('%-7s: %+.3f dex' % (name, dex(50, 15000, *band)))

print()
print('--- RWA 表对照（15kK / 20kK blue 带）---')
print('B=10:  RWA −0.628/−0.343    v6 %+.3f/%+.3f' % (dex(10, 15000, *BLUE), dex(10, 20000, *BLUE)))
print('B=50:  RWA −0.606/−0.330    v6 %+.3f/%+.3f' % (dex(50, 15000, *BLUE), dex(50, 20000, *BLUE)))
print('B=100: RWA −0.535/−0.286    v6 %+.3f/%+.3f' % (dex(100, 15000, *BLUE), dex(100, 20000, *BLUE)))
