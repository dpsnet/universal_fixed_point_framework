# -*- coding: utf-8 -*-
"""Phase 104i: 完整 RWA（n=2..25 全子态×q）——溶解机制 + Balmer 带正确网格 + 对称权重
溶解 = 束缚能 eb >= 0（磁场抬升 → 不再束缚）→ 光电离贡献移除（线→连续谱转移主体）
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
    if k <= 0 or not np.isfinite(k):
        return 0.0
    n3 = n**3; k8 = k**8
    denom = (n**2 + k**2)**(2*n + 2)
    expo = math.exp(-4*k*math.atan(n/k))
    dfde = (128/3)*n3*k8/denom*expo/(1-math.exp(-2*PI*k))
    return 4*PI**2*alpha*a0**2*dfde

def sigma_n_zero(n, eps):
    exi0 = 1.0/n**2
    if eps <= exi0:
        return 0.0
    return sigma_nk(n, (eps - exi0)**(-0.5))

def binding_energy(n, l, m, ms, beta):
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

def sigma_xi(n, l, m, ms, beta, q, eps):
    exi0 = 1.0/n**2
    exis = threshold_emax(n, l, m, ms, beta, q)
    delta = exis - exi0
    eps_shift = eps - delta
    if eps_shift <= exi0 + 1e-6:
        return 0.0
    s0 = sigma_nk(n, (eps_shift)**(-0.5))
    return eps/max(eps_shift, 1e-6)*s0

def weight(n, l, m, ms, beta, T_k):
    eb = binding_energy(n, l, m, ms, beta)
    return math.exp(eb/(kB_eV*T_k/RYD))

def build_states(nmax):
    st = []
    for n in range(2, nmax+1):
        for l in range(n):
            for m in range(-l, l+1):
                for ms in (-0.5, 0.5):
                    st.append((n, l, m, ms))
    return st

def run(B_MG, T_k, wl_lo, wl_hi, npts=121, nmax=25):
    beta = B_MG*1e6/B0
    states = build_states(nmax)
    wl = np.linspace(wl_lo, wl_hi, npts)
    eps = (12400.0/wl)/RYD
    # 溶解统计
    ndiss = 0; ndiss_m1 = 0; ndiss_all = 0
    for st in states:
        n, l, m, ms = st
        eb = binding_energy(n, l, m, ms, beta)
        if eb >= 0:
            ndiss_all += 1
            if m == 1 and ms == 0.5:
                ndiss_m1 += 1
    chi0_sum = 0.0; chiB_sum = 0.0
    for e in eps:
        c0 = 0.0; cB = 0.0
        for st in states:
            n, l, m, ms = st
            ebB = binding_energy(n, l, m, ms, beta)
            if ebB >= 0:
                continue  # 溶解态移除（线→连续谱转移）
            w0 = weight(n, l, m, ms, 0.0, T_k)/(1.0/n**2)
            wB = weight(n, l, m, ms, beta, T_k)/(1.0/n**2)
            c0 += w0*sigma_n_zero(n, e)
            sB = 0.0
            for q in (-1, 0, 1):
                sB += (1/3)*sigma_xi(n, l, m, ms, beta, q, e)
            cB += wB*sB
        chi0_sum += c0; chiB_sum += cB
    return chiB_sum/chi0_sum, ndiss_all, len(states)

print('=== 完整 RWA（n=2..25，Balmer 带 3600-3750 Å，溶解态移除）===')
print('B(MG)  T(kK) | χ/χ0 (dex)      | 溶解态数/总')
for B in (10, 50, 100):
    for T in (12000, 15000, 20000):
        r, nd, ns = run(B, T, 3600.0, 3750.0)
        print('%5d  %5d | %+.4f dex (%8.3f) | %d/%d' % (B, T, math.log10(r), r, nd, ns))
print()
print('=== 溶解边界（m=+1, ms=+0.5 态：eb = −1/n² + 4β）===')
for B in (10, 30, 50, 100, 300, 771):
    beta = B*1e6/B0
    n_crit = int(math.sqrt(1.0/(4*beta)) + 0.999)
    print('B=%4d MG: 4β=%.4f Ry → n≥%d 的 m=1/ms=+0.5 态溶解' % (B, 4*beta, n_crit))
