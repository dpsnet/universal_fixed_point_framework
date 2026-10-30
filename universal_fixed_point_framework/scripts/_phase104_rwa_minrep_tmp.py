# -*- coding: utf-8 -*-
"""Phase 104g: 最小复现——原脚本逻辑在 eps=2.9 Ry 处的 χ 变化来源"""
import numpy as np
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
    return math.exp(eb/(8.617333262e-5*T_k/RYD))

beta = 10*1e6/B0

# 单点 eps=2.903（原脚本 blue 带中值）
eps = 2.903
s0 = sigma2_zero(eps)
print('零场 σ0(eps=2.903 Ry) = %.4e' % s0)
print()
print('各子态×q：σ_xi / σ0 比 + w_B（原脚本逻辑）')
states = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            states.append((2, l, m, ms))
chi0 = 0; chiB = 0
for st in states:
    n, l, m, ms = st
    chi0 += s0
    wB = weight(n, l, m, ms, beta, 15000)/(1.0/n**2)
    sB = 0.0
    for q in (-1, 0, 1):
        sB += (1/3)*sigma_xi(n, l, m, ms, beta, q, eps)
    chiB += wB*sB
    print('l=%d m=%+d ms=%+.1f | w_B=%.4f | σ_xi/σ0=%.3f | 贡献/χ0=%.4f'
          % (l, m, ms, wB, sB/s0, wB*sB/(8*s0)))
print()
print('χ/χ0 = %.4f | dex = %+.4f' % (chiB/chi0, math.log10(chiB/chi0)))

# eps=2.903 与 Balmer 阈 0.25 的位移效应
print()
print('=== 位移结构（eps=2.903）===')
for st in states[:4]:
    n, l, m, ms = st
    for q in (-1, 0, 1):
        eth = threshold_emax(n, l, m, ms, beta, q)
        delta = eth - 0.25
        print('l=%d m=%+d ms=%+.1f q=%+d: exis=%.4f Ry, delta=%.5f Ry | eps_shift=%.4f (阈 0.25)'
              % (l, m, ms, q, eth, delta, eps-delta))
