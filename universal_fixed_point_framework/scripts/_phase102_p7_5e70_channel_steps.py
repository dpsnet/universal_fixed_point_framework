# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-70：通道数台阶结构补测——找 8→7→4 边界
================================================================
P7-5e-69：非零 m 通道范围随场强收缩
  94 MG：m = −8..+2（11 通道，负 m 范围 8 = k_max）
  164.5 MG：m = −8..+1（10 通道，负 m 范围 8）
  587.5 MG：m = −7..0（8 通道，负 m 范围 7 = k_max−1）
  940 MG：m = −4..0（5 通道，负 m 范围 4 = N_Weyl）
台阶候选：负 m 范围 {8, 8, 7, 4}——8→7→4 边界场强未知
补测：0.08/0.1/0.15/0.2/0.25/0.3/0.35/0.4 au 通道数 + m_min/m_max
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
print("P7-5e-70：通道数台阶结构补测——找 8→7→4 边界")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
tests = [0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]

results = {}
for B in tests:
    t0_all = time.time()
    Ns = {}
    for m in range(-m_max, m_max + 1):
        t0 = time.time()
        n = n_bound_m(N_r, r_max, m, B)
        Ns[m] = n
    nonzero = {m: n for m, n in Ns.items() if n > 0}
    tot = sum(Ns.values())
    m_min = min(nonzero.keys())
    m_max_ok = max(nonzero.keys())
    neg_range = sum(1 for m in nonzero if m < 0)
    pos_range = sum(1 for m in nonzero if m > 0)
    n_chan = len(nonzero)
    results[B] = {"n_total": tot, "n_chan": n_chan, "m_min": m_min, "m_max": m_max_ok,
                  "neg_range": neg_range, "pos_range": pos_range, "N_m": nonzero}
    print("  B=%.2f au（%.1f MG）→ n_total=%d 通道=%d（m=%d..%d，负%d 正%d 零%d）[%.0fs]"
          % (B, B*2350, tot, n_chan, m_min, m_max_ok, neg_range, pos_range,
             1 if 0 in nonzero else 0, time.time()-t0_all), flush=True)

print()
print("【台阶结构】")
print("-"*104)
print("  B_au    通道  负m范围  正m范围  n_total")
for B in tests:
    r = results[B]
    print("  %5.2f    %3d    %3d      %3d      %3d" % (B, r["n_chan"], r["neg_range"], r["pos_range"], r["n_total"]))

print()
print("【裁决】负 m 范围台阶：8→7→4 的精确边界场强 = ?")
json.dump({str(k): v for k, v in results.items()},
          open(os.path.join(BASE, "_phase102_p7_5e70_channel_steps.json"), "w", encoding="utf-8"),
          indent=1, default=str)
print("JSON 落盘 ✓  exit 0")
