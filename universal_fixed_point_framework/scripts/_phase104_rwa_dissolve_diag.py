# -*- coding: utf-8 -*-
"""Phase 104k: 高场离位态诊断（n=2 子态溶解场强 + 高端样本流形完整性）
登记 26.16j-9：v10_int 109-778MG 高端样本的 n=2 流形不完整阈值
"""
import math

B0 = 4.70103e9
RYD = 13.605693
kB_eV = 8.617333262e-5

def binding_energy(n, l, m, ms, beta):
    e0 = -1.0/n**2
    lin = 4*(m/2 + ms)*beta
    quad_num = n**2*(5*n**2 + 1 - 3*l*(l+1))*(l**2 + l - 1 + m**2)
    denom = (2*l-1)*(2*l+3)
    quad = quad_num/denom*beta**2 if denom != 0 else 0.0
    return e0 + lin + quad

STATES2 = []
for l, mslist in [(0, [-0.5, 0.5]), (1, [-0.5, 0.5])]:
    for m in range(-l, l+1):
        for ms in mslist:
            STATES2.append((2, l, m, ms))

def label(st):
    n, l, m, ms = st
    return '2s m=0 ms=%+.1f' % ms if l == 0 else '2p m=%+d ms=%+.1f' % (m, ms)

print('=== n=2 子态束缚能随 β（Ry；0 为溶解阈值）===')
print('态                 β=0.023(109MG)  0.064(300MG)  0.1(470MG)  0.165(778MG)')
for st in STATES2:
    ebs = [binding_energy(*st, b) for b in (0.023, 0.064, 0.1, 0.165)]
    print('%-20s  %+.4f      %+.4f      %+.4f      %+.4f' % (label(st), ebs[0], ebs[1], ebs[2], ebs[3]))

print()
print('=== 溶解场强（束缚能→0，β_dissolve）===')
for st in STATES2:
    n, l, m, ms = st
    # 线性近似主导：e0 + 4(m/2+ms)β = 0 → β = -e0/(4(m/2+ms))（仅 m/2+ms>0 的态可溶解）
    coef = 4*(m/2 + ms)
    if coef > 0:
        b_diss = (1.0/n**2)/coef
        print('%-20s  β_diss=%.4f  B_diss=%.0f MG' % (label(st), b_diss, b_diss*B0/1e6))
    else:
        print('%-20s  永束缚（m/2+ms≤0）' % label(st))

print()
print('=== v10_int 高端样本（109-778MG）流形完整性 ===')
for B in (109, 300, 470, 778):
    beta = B*1e6/B0
    diss = [st for st in STATES2 if binding_energy(*st, beta) >= 0]
    print('B=%3d MG (β=%.4f): 溶解 %d/8 态 → 剩余束缚 %d/8' % (B, beta, len(diss), 8-len(diss)))
