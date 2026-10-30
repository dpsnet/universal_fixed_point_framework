# -*- coding: utf-8 -*-
"""Phase 104k v5: RWA Eq.64 正确实现 —— 阈值位移基准 = ℰ_{−|m|}（自旋下 −|m| 态束缚能）
v2/v3 错误：eth = emm ± 4β（emm 含初态 4(m/2+ms)β 修正 → 双重叠加 → 阈下假新吸收）
正确：eth(ξ,q) = max(0, −ℰ_{−|m|} + Δq)，Δq = {+4β (q=+1,m≥0); −4β (q=−1,m≥1); 0 (else)}
关键结论：n=2 的 m=+1 态 q=−1 阈 = −ℰ_{−1}−4β = (0.25+4β)−4β = 0.25（零场值——无阈降！）
"""
import numpy as np
import math

alpha = 7.2973525693e-3
a0 = 5.29177210903e-9
B0 = 4.70103e9
RYD = 13.605693
PI = math.pi
kB_eV = 8.617333262e-5

def Q_2s_kp(k):  return 16*(1+k**2)*(4+k**2)
def Q_2p_kd(k):  return 128*k**2*(1+k**2)/9
def Q_2p_ks(k):  return 4*k**2*(4+k**2)/9
def P_2(k):      return (4+3*k**2)*(4+5*k**2)

def sigma_nk_total(n, k):
    if k <= 0 or not np.isfinite(k):
        return 0.0
    n3 = n**3; k8 = k**8
    denom = (n**2 + k**2)**(2*n + 2)
    expo = math.exp(-4*k*math.atan(n/k))
    P = P_2(k) if n == 2 else None
    dfde = (128/3)*n3*k8*P/denom*expo/(1-math.exp(-2*PI*k))
    return 4*PI**2*alpha*a0**2*dfde

A = {(0,0): {q: 1.0 for q in (-1,0,1)}}
B = {(0,0): {q: 0.0 for q in (-1,0,1)}}
A[(1, 0)] = {-1: 9/10, 0: 6/5, 1: 9/10}
A[(1, 1)] = {-1: 3/10, 0: 9/10, 1: 9/5}
B[(1, 0)] = {-1: 0.0, 0: 3.0, 1: 0.0}
B[(1, 1)] = {-1: 3.0, 0: 0.0, 1: 0.0}
A[(1, -1)] = {q: A[(1, 1)][-q] for q in (-1, 0, 1)}
B[(1, -1)] = {q: B[(1, 1)][-q] for q in (-1, 0, 1)}

def E_xi(n, l, m, ms, beta):
    """Eq.60 束缚态能量（负值，Ry）"""
    e0 = -1.0/n**2
    lin = 4*(m/2 + ms)*beta
    quad_num = n**2*(5*n**2 + 1 - 3*l*(l+1))*(l**2 + l - 1 + m**2)
    denom = (2*l-1)*(2*l+3)
    quad = quad_num/denom*beta**2 if denom != 0 else 0.0
    return e0 + lin + quad

def E_mminus(n, l, absm, beta):
    """ℰ_{−|m|}：自旋下 m=−|m| 态的束缚能量（Eq.62 基准，负值）"""
    return E_xi(n, l, -absm, -0.5, beta)

def eth_q(n, l, m, ms, beta, q):
    """Eq.64+65：光电离阈值（Ry）——位移基准 = ℰ_{−|m|}
    注意：位移不依赖初态 ms！Δq 仅由 (q, m) 决定"""
    emm = E_mminus(n, l, abs(m), beta)   # ℰ_{−|m|}（负值）
    if q == +1 and m >= 0:
        shift = -emm + 4*beta
    elif q == -1 and m >= 1:
        shift = -emm - 4*beta
    else:
        shift = -emm
    return max(0.0, shift)

def sigma_xi_q(n, l, m, ms, beta, q, eps):
    """单态单 q 通道截面：σ^q = [A ξ_up + B ξ_dn]σ_nk，k 由正确阈值算"""
    eth = eth_q(n, l, m, ms, beta, q)
    if eps <= eth + 1e-9:
        return 0.0
    k = (eps - eth)**(-0.5)
    if k <= 0 or not np.isfinite(k):
        return 0.0
    if l == 0:
        xi_up = Q_2s_kp(k)/P_2(k); xi_dn = 0.0
    else:
        xi_up = Q_2p_kd(k)/P_2(k); xi_dn = Q_2p_ks(k)/P_2(k)
    if (l, abs(m)) in A:
        Aq = A[(l, abs(m))][q]; Bq = B[(l, abs(m))][q]
    else:
        Aq = A[(l, 0)][q]; Bq = B[(l, 0)][q]
    if m < 0:
        Aq = A[(l, -m)][-q]; Bq = B[(l, -m)][-q]
    s_nk = sigma_nk_total(n, k)
    return (Aq*xi_up + Bq*xi_dn) * s_nk

def weight_rel(n, l, m, ms, beta, T_k):
    eb = E_xi(n, l, m, ms, beta)
    return math.exp(-eb/(kB_eV*T_k/RYD))

STATES2 = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            STATES2.append((2, l, m, ms))

def label(st):
    n, l, m, ms = st
    return '2s m0 ms%+.1f' % ms if l == 0 else '2p m%+d ms%+.1f' % (m, ms)

print('=== v5 正确阈值（Eq.64/65）诊断 ===')
print('态                 q=-1阈    q=0阈     q=+1阈    (10MG, Ry；零场阈=0.25)')
beta10 = 10e6/B0
for st in STATES2:
    n, l, m, ms = st
    t = [eth_q(n, l, m, ms, beta10, q) for q in (-1, 0, 1)]
    print('%-14s        %.4f    %.4f    %.4f' % (label(st), t[0], t[1], t[2]))

def chi_ratio(B_MG, T_k, wl_lo, wl_hi, npts=201):
    beta = B_MG*1e6/B0
    wl = np.linspace(wl_lo, wl_hi, npts)
    eps = (12400.0/wl)/RYD
    c0 = 0.0; cB = 0.0
    for e in eps:
        c0e = 0.0; cBe = 0.0
        for st in STATES2:
            n, l, m, ms = st
            w0 = weight_rel(n, l, m, ms, 0.0, T_k)
            wB = weight_rel(n, l, m, ms, beta, T_k)
            for q in (-1, 0, 1):
                s0 = sigma_xi_q(n, l, m, ms, 0.0, q, e)
                sB = sigma_xi_q(n, l, m, ms, beta, q, e)
                c0e += w0*s0
                cBe += wB*sB
        c0 += c0e
        cB += cBe
    if c0 <= 0:
        return float('inf') if cB > 0 else 0.0
    return cB/c0

print()
print('=== v5 分带结果（B=0 自检：应全 0.000）===')
print('B(MG)  T(kK) | 阈上 3600-3646Å | 阈下 3646-3750Å | 全带 3600-3750Å')
for Bv in (0, 10, 50, 100, 300):
    for T in (12000, 15000, 20000):
        r_up = chi_ratio(Bv, T, 3600.0, 3646.0)
        r_dn = chi_ratio(Bv, T, 3646.0, 3750.0)
        r_all = chi_ratio(Bv, T, 3600.0, 3750.0)
        f = lambda v: 'inf' if v == float('inf') else '%+.4f' % math.log10(v) if v > 0 else '0.0000'
        print('%5d  %5d | %s | %s | %s (dex)' % (Bv, T, f(r_up), f(r_dn), f(r_all)))

print()
print('=== v5 观测窗口 ===')
print('B(MG)  T(kK) | blue 3600-3640 | red 3700-3750 | slopeA 4000-4060')
for Bv in (10, 50, 100):
    for T in (12000, 15000, 20000):
        r_b = chi_ratio(Bv, T, 3600.0, 3640.0)
        r_r = chi_ratio(Bv, T, 3700.0, 3750.0)
        r_s = chi_ratio(Bv, T, 4000.0, 4060.0)
        f = lambda v: 'inf' if v == float('inf') else '%+.4f' % math.log10(v) if v > 0 else '0.0000'
        print('%5d  %5d | %s | %s | %s (dex)' % (Bv, T, f(r_b), f(r_r), f(r_s)))
