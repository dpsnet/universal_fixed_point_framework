# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-72：高场端延伸——0.8/0.9/1.0 au 先验检验
================================================================
P7-5e-71 实测：负 m 3（0.5/0.6 平台）→ 2（0.7）——台阶间隔 0.1 au
先验预言（间隔 0.1 au 继续）：
  0.8 au → 负 1（n=2）
  0.9 au → 负 1？（或负 0）
  1.0 au → 负 0（n=1——仅 m=0 通道——恰在 B_0 = 1 au = 2350 MG）
判别：n → 1 是否恰在 B_0！
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
print("P7-5e-72：高场端延伸——0.8/0.9/1.0 au 先验检验")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
tests = [(0.8, "负 1（n=2）"), (0.9, "负 1 或 0"), (1.0, "负 0（n=1——恰在 B_0）")]

results = {}
for B, pred in tests:
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
    results[B] = {"n_total": tot, "n_chan": len(nonzero), "m_min": m_min, "m_max": m_max_ok,
                  "neg_range": neg_range, "pos_range": pos_range, "N_m": {str(k): v for k, v in nonzero.items()}}
    print()
    print("【B_au=%.2f（%.1f MG）——预言 %s】" % (B, B*2350, pred))
    print("  实测：n_total=%d 通道=%d（m=%d..%d，负%d 正%d 零%d）N_m=%s"
          % (tot, len(nonzero), m_min, m_max_ok, neg_range, pos_range,
             1 if 0 in nonzero else 0, {str(k): v for k, v in nonzero.items()}), flush=True)

print()
print("【裁决】")
print("-"*104)
for B, r in results.items():
    print("  B=%.2f：n=%d 负m=%d 通道=%s" % (B, r["n_total"], r["neg_range"], r["N_m"]))
print("  ★ 关键判别：n=1（仅 m=0）是否恰在 B_au=1.0（B_0=2350 MG）？")

json.dump({str(k): v for k, v in results.items()},
          open(os.path.join(BASE, "_phase102_p7_5e72_highB_test.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
