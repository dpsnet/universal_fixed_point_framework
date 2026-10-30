# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-82：9 通道窄窗口验证——0.235/0.24/0.245 au
================================================================
P7-5e-81 推断：m=+1 过零 0.23708、m=-8 过零 0.24168——间距 0.0046 au
→ 0.237 < B < 0.242 之间：正1 已消失、负8 仍存活——9 通道（负8正0）窄窗口
预测：0.235 au = 10 通道（负8正1——正1 刚过零前）；0.24 au = 9 通道（负8正0）；
      0.245 au = 8 通道（负7正0——负8 已过零）
窗口中心 ≈ 0.24 = 2N_gen/25（框架量）
"""
import json, os, time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def n_bound_m(N_r, r_max, m, B, k=300):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    off_diag = np.ones(N_r - 1) / (2.0 * dr ** 2)
    diag_main = np.ones(N_r) / dr ** 2
    landau_centrifugal = (m + 0.5 * B * r ** 2) ** 2 / (2.0 * r ** 2)
    coulomb = -1.0 / r
    H = diags([-off_diag, diag_main + landau_centrifugal + coulomb, -off_diag],
              offsets=[-1, 0, 1], shape=(N_r, N_r), format='csr')
    try:
        vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                        which='SA', maxiter=50000, tol=1e-9)
        return int(np.sum(np.real(vals) < 0))
    except Exception:
        return 0

print("="*104)
print("P7-5e-82：9 通道窄窗口验证——0.235/0.24/0.245 au")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
for B in [0.235, 0.24, 0.245]:
    t0 = time.time()
    Ns = {}
    for m in range(-m_max, m_max + 1):
        Ns[m] = n_bound_m(N_r, r_max, m, B)
    nonzero = {m: n for m, n in Ns.items() if n > 0}
    tot = sum(Ns.values())
    neg = [m for m in nonzero if m < 0]
    pos = [m for m in nonzero if m > 0]
    print("  B=%.3f au（%.1f MG）→ n_total=%d 通道=%d（负%d 正%d——m∈[%d, %d]）[%.0fs]"
          % (B, B*2350, tot, len(nonzero), len(neg), len(pos),
             min(nonzero), max(nonzero), time.time()-t0), flush=True)

print()
print("【判别】")
print("-"*104)
print("  若 0.24 au = 9 通道（负8正0）→ 9 缺口是窄窗口（0.237-0.242）——中心 2N_gen/25 候选")
print("  若 0.24 au 非 9 通道 → 修正推断")
