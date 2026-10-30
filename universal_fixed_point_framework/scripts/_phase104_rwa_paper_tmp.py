# -*- coding: utf-8 -*-
"""Phase 104k: RWA 论文式修正实现 v2 —— 含自旋向上/正m 占据移除（VR&R 2020 关键机制）
weight_rel 修正：E_κ = E_rest + 4β·δ(ms=+1/2) + 4mβ·δ(m>0)（Ry 单位）
驱动"占据数骤降"= 自旋向上态（+4β）与正m态（+4mβ）能量上移 → Boltzmann 因子骤降
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
for (l, m), vals in {
    (1, 0): {-1: 9/10, 0: 6/5, 1: 9/10},
    (1, 1): {-1: 3/10, 0: 9/10, 1: 9/5},
}.items():
    A[(l, m)] = vals
    B[(l, m)] = {-1: 0.0, 0: 3.0, 1: 0.0} if m == 0 else {-1: 3.0, 0: 0.0, 1: 0.0}
A[(1, -1)] = {q: A[(1, 1)][-q] for q in (-1, 0, 1)}
B[(1, -1)] = {q: B[(1, 1)][-q] for q in (-1, 0, 1)}

def binding_energy(n, l, m, ms, beta):
    """E_rest：Zeeman 一阶 + 二阶（Ry）——中场 10-100MG 二阶小，一阶主导"""
    e0 = -1.0/n**2
    lin = 4*(m/2 + ms)*beta
    quad_num = n**2*(5*n**2 + 1 - 3*l*(l+1))*(l**2 + l - 1 + m**2)
    denom = (2*l-1)*(2*l+3)
    quad = quad_num/denom*beta**2 if denom != 0 else 0.0
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

def sigma_xi_q(n, l, m, ms, beta, q, eps):
    exi0 = 1.0/n**2
    exis = threshold_emax(n, l, m, ms, beta, q)
    delta = exis - exi0
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

def weight_rel_v2(n, l, m, ms, beta, T_k):
    """VR&R 关键机制：E_κ = E_rest + 4β·δ(ms=+1/2) + 4mβ·δ(m>0)
    —— 自旋向上/正m 态能量上移 → 占据骤降（Boltzmann 因子）"""
    eb = binding_energy(n, l, m, ms, beta)
    # 4β 自旋上移（对 ms=+1/2）与 4mβ 正m上移已含于 binding_energy 的 lin 项（4(m/2+ms)β）
    # lin = 4(m/2+ms)β：ms=+1/2 → +2β；m=+1 → +2β——合计正m且自旋上 +4β ✓
    return math.exp(-eb/(kB_eV*T_k/RYD))

STATES2 = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            STATES2.append((2, l, m, ms))

def chi_ratio(B_MG, T_k, wl_lo, wl_hi, npts=201):
    beta = B_MG*1e6/B0
    wl = np.linspace(wl_lo, wl_hi, npts)
    eps = (12400.0/wl)/RYD
    c0 = 0.0; cB = 0.0
    for e in eps:
        s0 = sigma_nk_total(2, (e-0.25)**(-0.5)) if e > 0.25 else 0.0
        w0tot = 0.0
        for st in STATES2:
            n, l, m, ms = st
            w0tot += weight_rel_v2(n, l, m, ms, 0.0, T_k)
        c0 += w0tot*s0
        for st in STATES2:
            n, l, m, ms = st
            wB = weight_rel_v2(n, l, m, ms, beta, T_k)
            sB = 0.0
            for q in (-1, 0, 1):
                sB += sigma_xi_q(n, l, m, ms, beta, q, e)
            cB += wB*sB
    return cB/c0

thr = 3646.0
print('=== RWA 修正实现 v2（VR&R 占据移除机制，n=2）===')
print('B(MG)  T(kK) | 阈上 3600-3646Å | 阈下 3646-3750Å | 全带 3600-3750Å')
for Bv in (10, 50, 100, 300):
    for T in (12000, 15000, 20000):
        r_up = chi_ratio(Bv, T, 3600.0, thr)
        r_dn = chi_ratio(Bv, T, thr, 3750.0)
        r_all = chi_ratio(Bv, T, 3600.0, 3750.0)
        print('%5d  %5d | %+.4f | %s | %+.4f (dex)'
              % (Bv, T, math.log10(r_up), 'inf' if r_dn == float('inf') else '%+.4f' % math.log10(r_dn),
                 math.log10(r_all)))

print()
print('=== 占据权重诊断（15kK，β=B/4.701e9）===')
for Bv in (10, 50, 100):
    beta = Bv*1e6/B0
    print('B=%d MG (β=%.4f):' % (Bv, beta))
    for st in STATES2:
        n, l, m, ms = st
        wB = weight_rel_v2(n, l, m, ms, beta, 15000)
        w0 = weight_rel_v2(n, l, m, ms, 0.0, 15000)
        print('  l=%d m=%+d ms=%+.1f: w0=%.3f wB=%.3f 比值=%.3f' % (l, m, ms, w0, wB, wB/w0))
