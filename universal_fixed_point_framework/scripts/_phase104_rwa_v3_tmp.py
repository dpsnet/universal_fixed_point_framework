# -*- coding: utf-8 -*-
"""Phase 104k v3: RWA 归一化 bug 修复 —— 零场 c0 也做 q 通道展开（Σ_q[A ξ_up + B ξ_dn]σ_nk）
v2 的错误：c0 用单通道基准 σ_nk，cB 用 Σ_q 展开 ≈3(ξ_up+ξ_dn)σ_nk ≈ 2.9σ_nk → 系统虚增 ~0.46 dex
v3 修正：零场与有场同构（同 A/B 权重、同 k 计算，仅阈值位移 β=0）
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
    """单态单 q 通道截面：σ^q = [A ξ_up + B ξ_dn]σ_nk
    β=0 时即零场通道展开（同构）"""
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

def chi_ratio(B_MG, T_k, wl_lo, wl_hi, npts=201):
    beta = B_MG*1e6/B0
    wl = np.linspace(wl_lo, wl_hi, npts)
    eps = (12400.0/wl)/RYD
    c0 = 0.0; cB = 0.0
    for e in eps:
        # 零场：8 态 × 3q 通道展开（与有场同构，β=0）
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

thr = 3646.0
print('=== RWA v3（零场/有场 q 通道同构，归一化修复）n=2 ===')
print('B(MG)  T(kK) | 阈上 3600-3646Å | 阈下 3646-3750Å | 全带 3600-3750Å')
for Bv in (0, 10, 50, 100, 300):
    for T in (12000, 15000, 20000):
        r_up = chi_ratio(Bv, T, 3600.0, thr)
        r_dn = chi_ratio(Bv, T, thr, 3750.0)
        r_all = chi_ratio(Bv, T, 3600.0, 3750.0)
        fmt = lambda v: 'inf' if v == float('inf') else '%+.4f' % math.log10(v) if v > 0 else '0.0'
        print('%5d  %5d | %s | %s | %s (dex)'
              % (Bv, T, fmt(r_up), fmt(r_dn), fmt(r_all)))

print()
print('=== 观测窗口对齐：blue 3600-3640 / red 3700-3750（论文 §4.8 带定义）===')
print('B(MG)  T(kK) | blue 3600-3640 | red 3700-3750 | slopeA 4000-4060')
for Bv in (10, 50, 100):
    for T in (12000, 15000, 20000):
        r_b = chi_ratio(Bv, T, 3600.0, 3640.0)
        r_r = chi_ratio(Bv, T, 3700.0, 3750.0)
        r_s = chi_ratio(Bv, T, 4000.0, 4060.0)
        fmt = lambda v: 'inf' if v == float('inf') else '%+.4f' % math.log10(v) if v > 0 else '0.0'
        print('%5d  %5d | %s | %s | %s (dex)'
              % (Bv, T, fmt(r_b), fmt(r_r), fmt(r_s)))
