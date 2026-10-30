# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-84：台阶网格规则补测——0.55/0.65/0.75/0.85 au
================================================================
P7-5e-83 推断：台阶 = 量子过零的 0.05 网格上取整
  m=-4 过零 0.46488 → 上取整 0.50（0.55 应已 4 通道=负3正0）
  m=-3 过零 0.60237 → 上取整 0.65（0.65 应已 3 通道=负2正0——若 0.65 仍 4 通道则上取整规则失败）
  m=-2 过零 0.84884 → 上取整 0.90（0.75/0.85 应仍 3 通道=负2正0——0.85 < 0.84884 应仍负2）
判别：0.65 au 通道数——3 通道（负2）→ 规则 ✓；4 通道（负3）→ 规则 ✗（修正）
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
print("P7-5e-84：台阶网格规则补测——0.55/0.65/0.75/0.85 au")
print("="*104)

for B in [0.55, 0.65, 0.75, 0.85]:
    t0 = time.time()
    Ns = {}
    for m in range(-8, 3):
        Ns[m] = n_bound_m(1500, 60.0, m, B)
    nonzero = {m: n for m, n in Ns.items() if n > 0}
    neg = [m for m in nonzero if m < 0]
    pos = [m for m in nonzero if m > 0]
    print("  B=%.2f au（%.1f MG）→ n_total=%d 通道=%d（负%d 正%d——m∈[%d, %d]）[%.0fs]"
          % (B, B*2350, sum(Ns.values()), len(nonzero), len(neg), len(pos),
             min(nonzero), max(nonzero), time.time()-t0), flush=True)

print()
print("【网格规则判别】")
print("-"*104)
print("  预测：0.55 = 4 通道（负3正0——m=-4 已过零 0.46488）；0.65 = 3 通道（负2正0——m=-3 已过零 0.60237）")
print("        0.75 = 3 通道（负2正0——m=-2 过零 0.84884 未到）；0.85 = 3 通道（负2正0）")
