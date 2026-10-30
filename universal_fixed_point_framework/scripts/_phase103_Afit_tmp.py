# -*- coding: utf-8 -*-
"""Phase 103u: A(T) 第一性化——Saha 通道占比模型
假说：A(T) = Balmer 带吸收中"非 n=2 光电离"通道占比
  （H⁻ 自由-自由/束缚-自由 + H+ 自由-自由——不受阈值位移影响）
  n=2 光电离通道被拓扑阈值位移移除（26.16e）→ 残余 = 其他通道
Saha 电离 + 通道吸收截面（Kramers 近似）
对照：A_fit = 0.10×(kT/1.03)³ —— 12kK:0.10、15kK:0.20、20kK:0.47
"""
import math

RY = 13.6  # eV

def saha_ne(T, nH):
    """Saha：n_e² = n_H1 × C(T) × e^{−13.6/kT}；C = (2πm_e kT/h²)^{3/2}×2(g+权重)"""
    kT = 8.617e-5 * T
    # (2πm_e kT/h²)^{3/2} = 2.41e21 × (T/300)^{3/2} m^-3（标准 Saha 常数）
    C = 2.41e21 * (T / 300.0) ** 1.5
    # 简并权重 g_e×g_p/g_H = 2（电子）×2（质子）/2（H）= 2（简化）
    n_e = math.sqrt(nH * C * 2.0 * math.exp(-RY / kT))
    return n_e

def occ_n2(T, nH):
    """n=2 占据（相对 n=1 简并加权 4）"""
    kT = 8.617e-5 * T
    return nH * 4.0 * math.exp(-(RY - RY/4.0) / kT)

def chi_n2_photo(T, nH, lam_lo, lam_hi):
    """n=2 光电离吸收（Kramers σ ∝ (ν_0/ν)³，Balmer 带积分）"""
    N2 = occ_n2(T, nH)
    hv_lo = 12398.0 / lam_hi
    hv_hi = 12398.0 / lam_lo
    s = 0.0
    N = 100
    for i in range(N):
        hv = hv_lo + (hv_hi - hv_lo) * (i + 0.5) / N
        if hv > RY/4.0:
            s += (RY/4.0 / hv) ** 3
    return N2 * s / N

def chi_Hminus(T, nH):
    """H⁻ 吸收（束缚-自由 + 自由-自由，Balmer 带）——标准 H⁻ 不透明度温度依赖"""
    kT = 8.617e-5 * T
    ne = saha_ne(T, nH)
    # H⁻ 形成 ∝ n_H×n_e；吸收系数 κ_H⁻(λ~3700Å) ∝ λ³ T^{-5/2}(1-e^{-hc/λkT}) × n_H n_e（近似）
    lam = 3700.0
    hv = 12398.0 / lam
    factor = (lam ** 3) * (T ** -2.5) * (1.0 - math.exp(-hv / kT))
    return ne * nH * factor

def chi_ff(T, nH):
    """H+ 自由-自由（Kramers）：κ ∝ n_e n_H+ T^{-1/2} λ³"""
    ne = saha_ne(T, nH)
    nHp = ne
    lam = 3700.0
    return ne * nHp * (T ** -0.5) * (lam ** 3)

def A_model(T, nH):
    """A = 非 n=2 通道占比"""
    c2 = chi_n2_photo(T, nH, 3600.0, 3750.0)
    chm = chi_Hminus(T, nH)
    cf = chi_ff(T, nH)
    tot = c2 + chm + cf
    return (chm + cf) / tot if tot > 0 else 0.0

print('=== A(T) 第一性化：Saha 通道占比 ===')
print('%-7s | %-10s | %-10s | %-10s | %-10s | %-10s' % ('T(kK)', 'n_e/nH', 'A模型', 'A_fit', 'n=2占比', 'H-/ff占比'))
for T in (12000, 15000, 20000):
    nH = 1.0
    ne = saha_ne(T, nH)
    A = A_model(T, nH)
    kT = 8.617e-5 * T
    Afit = 0.10 * (kT / 1.03) ** 3
    c2 = chi_n2_photo(T, nH, 3600.0, 3750.0)
    chm = chi_Hminus(T, nH)
    cf = chi_ff(T, nH)
    tot = c2+chm+cf
    print('%-7d | %.2e   | %.3f    | %.3f    | %.3f    | %.3f'
          % (T/1000, ne, A, Afit, c2/tot, (chm+cf)/tot))

print()
print('--- 扫描 n_H（密度标度不变性检验）---')
for T in (12000, 15000, 20000):
    A1 = A_model(T, 1.0)
    A10 = A_model(T, 10.0)
    print('T=%dkK: A(nH=1)=%.3f, A(nH=10)=%.3f' % (T/1000, A1, A10))

print()
print('--- 形状对照（归一化到 15kK）---')
for T in (12000, 15000, 20000):
    kT = 8.617e-5 * T
    print('T=%dkK: A_fit(归一)=%.2f, A模型(归一)=%.2f'
          % (T/1000, (kT/1.29)**3, A_model(T, 1.0)/A_model(15000, 1.0)))
