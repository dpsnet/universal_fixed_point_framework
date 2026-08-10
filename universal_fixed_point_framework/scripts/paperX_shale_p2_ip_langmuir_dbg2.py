#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断：朗缪尔阈值 IP 的 S(P) 形状 vs 朗缪尔 F(P)=P/(P+a)。"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperX_shale_p2_ip_uf import ip_union_entry

A = 1.09
n = 96; phi = 0.40; cfg = 0

rng = np.random.default_rng(cfg)
binary = rng.random((n, n, n)) < phi
rng3 = np.random.default_rng(cfg + 1000)
T = rng3.random((n, n, n))
U = A * T / (1.0 - T)
U3d = np.where(binary, U, 2.0)
pore_idx = np.flatnonzero(binary.ravel())
Ufl = U3d.ravel()
order = pore_idx[np.argsort(Ufl[pore_idx])]
P, S, Pc, Sc = ip_union_entry(binary, Ufl, order)
print(f"P_c={Pc:.4f} S_c={Sc*100:.1f}%  n_pore={len(P)}")
print(f"  {'P':>9} {'S_ip%':>8} {'F%':>7} {'S_ip/F':>8}")
for pv in [0.1, 0.2, 0.36, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]:
    # 最后一个被注入的 P<=pv 处 S 值
    m = P <= pv
    if m.sum():
        s = S[m][-1]
        F = pv / (pv + A)
        print(f"  {pv:9.2f} {s*100:8.2f} {F*100:7.1f} {s/F:8.3f}")
