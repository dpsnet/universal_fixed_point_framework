# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-73：找 n=1（仅 m=0）精确场强——1.1/1.2/1.3 au
================================================================
P7-5e-72 实测：负 m 2（0.7-0.8 平台）→ 1（0.9-1.0 平台）——n=1 未在 1.0 au 出现
间隔序列 {0.05, 0.05, 0.05, 0.1, 0.2, 0.2}——几何扩张倾向（×2）
两候选：
  (a) 间隔继续 ×2：负 0 在 0.9+0.4 = 1.3 au（n=1）
  (b) 间隔保持 0.2：负 0 在 0.9+0.2 = 1.1 au（n=1）
补测 1.1/1.2/1.3 au——判别！
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
print("P7-5e-73：找 n=1 精确场强——1.1/1.2/1.3 au")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
tests = [1.1, 1.2, 1.3]

results = {}
for B in tests:
    t0_all = time.time()
    Ns = {}
    for m in range(-m_max, m_max + 1):
        n = n_bound_m(N_r, r_max, m, B)
        Ns[m] = n
    nonzero = {m: n for m, n in Ns.items() if n > 0}
    tot = sum(Ns.values())
    m_min = min(nonzero.keys())
    m_max_ok = max(nonzero.keys())
    neg_range = sum(1 for m in nonzero if m < 0)
    results[B] = {"n_total": tot, "n_chan": len(nonzero), "m_min": m_min, "m_max": m_max_ok,
                  "neg_range": neg_range, "N_m": {str(k): v for k, v in nonzero.items()}}
    print("  B_au=%.2f（%.1f MG）→ n_total=%d 通道=%d（m=%d..%d，负%d）N_m=%s [%.0fs]"
          % (B, B*2350, tot, len(nonzero), m_min, m_max_ok, neg_range,
             {str(k): v for k, v in nonzero.items()}, time.time()-t0_all), flush=True)

print()
print("【裁决】")
print("-"*104)
for B, r in results.items():
    print("  B=%.2f：n=%d 负m=%d" % (B, r["n_total"], r["neg_range"]))
n1 = [B for B, r in results.items() if r["n_total"] == 1]
if n1:
    print("  ★★ n=1 出现于 B_au = %s（%.0f MG）" % (n1, n1[0]*2350))
else:
    print("  ★ n=1 未在 1.1-1.3 au 出现——需继续延伸")
print("  间隔序列：0.05,0.05,0.05,0.1,0.2,0.2,(%s→%s)" % (
    results[tests[0]]["neg_range"], results[tests[-1]]["neg_range"]))

json.dump({str(k): v for k, v in results.items()},
          open(os.path.join(BASE, "_phase102_p7_5e73_n1_search.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
