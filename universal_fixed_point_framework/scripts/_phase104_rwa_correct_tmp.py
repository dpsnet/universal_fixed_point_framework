# -*- coding: utf-8 -*-
"""Phase 104h: RWA 正确实现重推——Balmer 带正确网格 + 对称占据权重归一
对比：原脚本（37eV + 权重不对称）→ −0.628；正确版 → ?
"""
import numpy as np
import math

alpha = 7.2973525693e-3
a0 = 5.29177210903e-9
B0 = 4.70103e9
RYD = 13.605693
PI = math.pi
kB_eV = 8.617333262e-5

def sigma_nk(n, k):
    n3 = n**3; k8 = k**8
    denom = (n**2 + k**2)**(2*n + 2)
    expo = math.exp(-4*k*math.atan(n/k))
    dfde = (128/3)*n3*k8/denom*expo/(1-math.exp(-2*PI*k))
    return 4*PI**2*alpha*a0**2*dfde

def sigma2_zero(eps):
    k = (eps - 0.25)**(-0.5)
    if k <= 0 or not np.isfinite(k):
        return 0.0
    return sigma_nk(2, k)

def binding_energy(n, l, m, ms, beta):
    e0 = -1.0/n**2
    lin = 4*(m/2 + ms)*beta
    quad = n**2*(5*n**2 + 1 - 3*l*(l+1))*(l**2 + l - 1 + m**2)
    if (2*l-1)*(2*l+3) != 0:
        quad = quad/((2*l-1)*(2*l+3))*beta**2
    else:
        quad = 0
    return e0 + lin + quad

def threshold_emax(n, l, m, ms, beta, q):
    emm = -binding_energy(n, l, abs(m), ms, beta)
    if q == +1 and m >= 0:
        eth = emm + 4*beta
    elif q == -1 and m >= 1:
        eth = emm - 4*beta
    else:
        eth = emm
    return max(0.0, eth)

def sigma_xi(n, l, m, ms, beta, q, eps):
    exi0 = 1.0/n**2
    exis = threshold_emax(n, l, m, ms, beta, q)
    delta = exis - exi0
    eps_shift = eps - delta
    if eps_shift <= exi0 + 1e-6:
        return 0.0
    s0 = sigma_nk(n, (eps_shift)**(-0.5)) if eps_shift > 0 else 0.0
    return eps/max(eps_shift, 1e-6)*s0

def weight(n, l, m, ms, beta, T_k):
    eb = binding_energy(n, l, m, ms, beta)
    return math.exp(eb/(kB_eV*T_k/RYD))

STATES = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            STATES.append((2, l, m, ms))

def chi_ratio_correct(B_MG, T_k, wl_lo, wl_hi, npts=201):
    """正确实现：chi0/chiB 都带占据权重（对称），带内积分"""
    beta = B_MG*1e6/B0
    wl = np.linspace(wl_lo, wl_hi, npts)
    eps = (12400.0/wl)/RYD  # 正确 Balmer 带
    chi0_sum = 0.0; chiB_sum = 0.0
    for i, e in enumerate(eps):
        s0 = sigma2_zero(e)
        w0tot = 0.0; sBtot = 0.0; wBtot = 0.0
        for st in STATES:
            n, l, m, ms = st
            w0 = weight(n, l, m, ms, 0.0, T_k)/(1.0/n**2)
            wB = weight(n, l, m, ms, beta, T_k)/(1.0/n**2)
            w0tot += w0
            sB = 0.0
            for q in (-1, 0, 1):
                sB += (1/3)*sigma_xi(n, l, m, ms, beta, q, e)
            sBtot += wB*sB
            wBtot += wB
        chi0_sum += w0tot*s0
        chiB_sum += sBtot
    return chiB_sum/chi0_sum

# 原脚本口径（权重不对称）：chi0 无权重
def chi_ratio_asym(B_MG, T_k, wl_lo, wl_hi, npts=201):
    beta = B_MG*1e6/B0
    wl = np.linspace(wl_lo, wl_hi, npts)
    eps = (12400.0/wl)/RYD
    chi0_sum = 0.0; chiB_sum = 0.0
    for e in eps:
        s0 = sigma2_zero(e)
        chi0_sum += s0  # 无权重（原脚本 bug）
        for st in STATES:
            n, l, m, ms = st
            wB = weight(n, l, m, ms, beta, T_k)/(1.0/n**2)
            sB = 0.0
            for q in (-1, 0, 1):
                sB += (1/3)*sigma_xi(n, l, m, ms, beta, q, e)
            chiB_sum += wB*sB
    return chiB_sum/chi0_sum

# 正确带（3600-3750 Å ≈ eps 0.253-0.268 Ry——Balmer 连续谱蓝端）
wl_lo, wl_hi = 3600.0, 3750.0
print('=== RWA 正确实现 vs 原口径（Balmer 带 3600-3750 Å）===')
print('B(MG)  T(kK) | 正确(对称权重)  | 原口径(不对称)  | 原脚本表')
for B in (10, 50, 100):
    for T in (12000, 15000, 20000):
        rc = chi_ratio_correct(B, T, wl_lo, wl_hi)
        ra = chi_ratio_asym(B, T, wl_lo, wl_hi)
        print('%5d  %5d | %+.4f dex (%.4f) | %+.4f dex (%.4f) | %s'
              % (B, T, math.log10(rc), rc, math.log10(ra), ra, ''))
print()
print('=== 正确版带内 eps 范围 ===')
eps = (12400.0/np.array([3600.0, 3750.0]))/RYD
print('eps = %.4f - %.4f Ry（Balmer 连续谱阈 0.25 之上）' % (eps[0], eps[1]))
