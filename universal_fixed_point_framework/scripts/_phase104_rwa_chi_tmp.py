# -*- coding: utf-8 -*-
"""Phase 104e: RWA 子态×极化 χ/χ_0 正确归一复现
χ/χ_0(带) = Σ_st Σ_q (1/3) w_B(st) σ_xi(st,q) / (8 σ0)
对照：RWA 表（10/50/100MG × 15/20kK）+ v6d（A+(1-A)exp）——验证 A 的极化通道机制
"""
import math

alpha = 7.2973525693e-3
a0 = 5.29177210903e-9
B0 = 4.70103e9
RYD = 13.605693
PI = math.pi

def sigma_nk(n, k):
    n3 = n**3; k8 = k**8
    denom = (n**2 + k**2)**(2*n + 2)
    expo = math.exp(-4*k*math.atan(n/k))
    dfde = (128/3)*n3*k8/denom*expo/(1-math.exp(-2*PI*k))
    return 4*PI**2*alpha*a0**2*dfde

def sigma2_zero(eps):
    k = (eps - 0.25)**(-0.5)
    if k <= 0:
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
    return math.exp(eb/(8.617333262e-5*T_k/RYD))

def kT_ry(T_k):
    return 8.617333262e-5*T_k/RYD

# 带网格（Å→eV→Ry：eps = 12400/wl/RYD）
wl = [3600 + i*(3750-3600)/29 for i in range(30)]
eps = [(12400.0/w)/RYD for w in wl]
eps = [e for e in eps if e > 0.25 + 1e-4]

states = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            states.append((2, l, m, ms))

# 零场带平均
s0_band = sum(sigma2_zero(e) for e in eps)/len(eps)

def chi_ratio(B_mg, T_k):
    beta = B_mg*1e6/B0
    # 每点比值再带内平均（避免阈处分母极小）
    ratios = []
    for e in eps:
        num = 0.0; den = 0.0
        for st in states:
            n, l, m, ms = st
            wB = weight(n, l, m, ms, beta, T_k)/(1.0/n**2)
            s0e = sigma2_zero(e)
            for q in (-1, 0, 1):
                sB = sigma_xi(n, l, m, ms, beta, q, e)
                num += (1.0/3)*wB*sB
            den += wB*s0e
        if den > 0:
            ratios.append(num/den)
    return sum(ratios)/len(ratios) if ratios else 0.0

print('=== RWA χ/χ_0 复现（子态×q 正确归一）===')
print('%-8s | %-6s | %-8s | %-8s | %-8s | %-8s | %-10s | %s' %
      ('B(MG)', 'T(kK)', 'χ/χ₀', 'dex', 'RWA表', 'v6d', 'A_fit', '判定'))
rwa_tab = {(10, 12): '-0.78~-0.91', (10, 15): '-0.628', (10, 20): '-0.343',
           (50, 15): '-0.606', (50, 20): '-0.330', (100, 15): '-0.535', (100, 20): '-0.286'}
for B in (10, 50, 100):
    for T in (12000, 15000, 20000):
        cr = chi_ratio(B, T)
        dex = math.log10(cr) if cr > 0 else float('-inf')
        A = 0.10*(8.617e-5*T/1.03)**3
        dth = 0.58*(B/10.0)
        v6d = A + (1-A)*math.exp(-dth/0.2)
        v6d_dex = math.log10(v6d)
        rwa = rwa_tab.get((B, T), '—')
        ok = ''
        if rwa != '—':
            try:
                diff = abs(dex - float(rwa))
                ok = '✓' if diff < 0.05 else ('±%.3f' % diff)
            except ValueError:
                ok = '—'
        print('%-8d | %-6d | %.4f | %+.3f | %-8s | %+.3f | %.3f | %s'
              % (B, T//1000, cr, dex, rwa, v6d_dex, A, ok))

print()
print('=== 分解（10MG 15kK：各通道贡献）===')
B = 10; T = 15000
beta = B*1e6/B0
num = 0.0
print('%-16s | %-5s | %-8s | %-7s | %-9s | %-9s' % ('子态(l,m,ms)', 'q', 'σ_xi带均', 'w_B', '贡献', '相对χ₀'))
for st in states:
    n, l, m, ms = st
    wB = weight(n, l, m, ms, beta, T)/(1.0/n**2)
    for q in (-1, 0, 1):
        sB = sum(sigma_xi(n, l, m, ms, beta, q, e) for e in eps)/len(eps)
        c = (1.0/3)*wB*sB
        num += c
        print('2p(l=%d)m=%+d,ms=%+d | q=%+d | %.4e | %.4f | %.4e | %.4f'
              % (l, int(m), ms, q, sB, wB, c, c/(8*s0_band)))
print('χ/χ₀ = %.4f | dex = %+.3f（RWA 表 10MG/15kK: −0.628）' % (num/(8*s0_band), math.log10(num/(8*s0_band))))
