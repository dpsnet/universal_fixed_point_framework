# -*- coding: utf-8 -*-
"""Phase 104k v4: RWA v3 波长扫描（3600-4100Å 逐点 χ/χ0）——全谱图对比数值基础
登记 26.16j-8：slopeA 带方向核对（观测 slopeA −0.026 流量减 vs RWA 阈下新吸收流量减 = 方向一致；
red 带 +0.057 流量增 vs RWA 阈下新吸收 = 方向相反——分带登记）
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

def binding_energy(n, l, m, ms, beta):
    e0 = -1.0/n**2
    lin = 4*(m/2 + ms)*beta
    quad_num = n**2*(5*n**2 + 1 - 3*l*(l+1))*(l**2 + l - 1 + m**2)
    denom = (2*l-1)*(2*l+3)
    quad = quad_num/denom*beta**2 if denom != 0 else 0.0
    return e0 + lin + quad

def sigma_xi_q(n, l, m, ms, beta, q, eps):
    exi0 = 1.0/n**2
    emm = -binding_energy(n, l, abs(m), ms, beta)
    if q == +1 and m >= 0:
        eth = emm + 4*beta
    elif q == -1 and m >= 1:
        eth = emm - 4*beta
    else:
        eth = emm
    delta = eth - exi0
    eps_shift = eps - delta
    if eps_shift <= exi0 + 1e-9:
        return 0.0
    k = (eps_shift - exi0)**(-0.5)
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
    eb = binding_energy(n, l, m, ms, beta)
    return math.exp(-eb/(kB_eV*T_k/RYD))

STATES2 = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            STATES2.append((2, l, m, ms))

def chi_point(B_MG, T_k, wl):
    beta = B_MG*1e6/B0
    e = (12400.0/wl)/RYD
    c0 = 0.0; cB = 0.0
    for st in STATES2:
        n, l, m, ms = st
        w0 = weight_rel(n, l, m, ms, 0.0, T_k)
        wB = weight_rel(n, l, m, ms, beta, T_k)
        for q in (-1, 0, 1):
            s0 = sigma_xi_q(n, l, m, ms, 0.0, q, e)
            sB = sigma_xi_q(n, l, m, ms, beta, q, e)
            c0 += w0*s0
            cB += wB*sB
    if c0 <= 0:
        return float('inf') if cB > 0 else 0.0
    return cB/c0

print('=== RWA v3 波长扫描（15kK，χ(B)/χ(0)）===')
print('波长Å  10MG    50MG    100MG   300MG   (dex)')
for wl in range(3600, 4101, 25):
    vals = []
    for Bv in (10, 50, 100, 300):
        r = chi_point(Bv, 15000, wl)
        vals.append('inf' if r == float('inf') else '%+.3f' % math.log10(r) if r > 0 else '0.000')
    print('%5d  %s  %s  %s  %s' % (wl, vals[0], vals[1], vals[2], vals[3]))

print()
print('=== 观测带对齐汇总（15kK）===')
print('带           观测(中场−弱场)  RWA 10MG  RWA 50MG  RWA 100MG')
for name, lo, hi, obs in [('blue 3600-3640', 3600, 3640, '+0.060'),
                          ('red 3700-3750', 3700, 3750, '+0.057'),
                          ('slopeA 4000-4060', 4000, 4060, '−0.026')]:
    r10 = chi_point(10, 15000, (lo+hi)/2)
    r50 = chi_point(50, 15000, (lo+hi)/2)
    r100 = chi_point(100, 15000, (lo+hi)/2)
    f = lambda r: 'inf' if r == float('inf') else '%+.3f' % math.log10(r) if r > 0 else '0.000'
    print('%s  %s      %s      %s      %s' % (name, obs, f(r10), f(r50), f(r100)))
