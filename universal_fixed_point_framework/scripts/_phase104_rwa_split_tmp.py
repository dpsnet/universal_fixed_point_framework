# -*- coding: utf-8 -*-
"""Phase 104d: RWA 子态×极化分解（纯 math 版，无 numpy）
复用 _phase86_r4b_rwa.py 公式（Eq.44/56/60/64/68）
"""
import math

alpha = 7.2973525693e-3
a0 = 5.29177210903e-9
B0 = 4.70103e9
RYD = 13.605693
PI = math.pi

def sigma_nk(n, k):
    n3 = n**3
    k8 = k**8
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

# Balmer 带网格（纯 math 循环）——修正单位：Å→nm（12400/wl）
wl = [3600 + i*(3750-3600)/29 for i in range(30)]
eps = [13.605693/(12400.0/w)/RYD for w in wl]
eps = [e for e in eps if e > 0.25 + 1e-4]

beta = 10*1e6/B0
s0_band = [sigma2_zero(e) for e in eps]
TOT0 = sum(s0_band)

states = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            states.append((2, l, m, ms))

print('=== RWA 子态×极化分解（10MG，Balmer 带 3600-3750Å）===')
print('%-20s | %-5s | %-8s | %-6s | %-8s | %-7s | %-7s | %s' %
      ('子态(l,m,ms)', 'q', '阈(eV)', '可及', 'σ保留比', 'w12k', 'w20k', '机制'))
for st in states:
    n, l, m, ms = st
    for q in (-1, 0, 1):
        sB = [sigma_xi(n, l, m, ms, beta, q, e) for e in eps]
        eth = threshold_emax(n, l, m, ms, beta, q)*RYD
        keep = sum(sB)/TOT0
        w12 = weight(n, l, m, ms, beta, 12000)/(1.0/n**2)
        w20 = weight(n, l, m, ms, beta, 20000)/(1.0/n**2)
        mech = 'q+抬升被禁' if (q == 1 and m >= 0) else ('q-下移保留' if (q == -1 and m >= 1) else '微变保留')
        print('2p(l=%d)m=%+d,ms=%+d | q=%+d | %+.3f | %s | %.4f | %.4f | %.4f | %s'
              % (l, m, ms, q, eth-3.4, '可及' if eth < 3.44 else '被禁', keep, w12, w20, mech))

print()
print('=== 汇总（占据加权保留占比 = A 的 RWA 机制）===')
for T in (12000, 15000, 20000):
    num = 0.0; den = 0.0
    for st in states:
        n, l, m, ms = st
        wT = weight(n, l, m, ms, beta, T)/(1.0/n**2)
        for q in (-1, 0, 1):
            sB = [sigma_xi(n, l, m, ms, beta, q, e) for e in eps]
            keep = sum(sB)/TOT0
            num += wT*keep
            den += wT
    A_rwa = num/den
    Af = 0.10*(8.617e-5*T/1.03)**3
    print('T=%dkK: A_rwa(占权保留) = %.4f | A_fit = %.4f' % (T/1000, A_rwa, Af))

print()
print('=== 判定 ===')
print('A 的机制 = RWA 极化通道残余（q=+1 m≥0 子态阈抬 4β 被禁；q=-1/π 保留）')
print('温度依赖 = 占据数 Eq.68（子态能移 4(m/2+ms)β → 玻尔兹曼权重随 T 均化）')
