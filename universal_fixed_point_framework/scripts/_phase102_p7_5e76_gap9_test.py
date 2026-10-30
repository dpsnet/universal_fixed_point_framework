# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-76：9 缺口判别 + 中场通道边界——0.225/0.05/0.06 au
================================================================
通道数序列 {11, 10, 8, 7, 6, 5, 4, 3, 2}——缺 9（N_gen² 从未出现）
结构：0.20 au 负8正1（10 通道）→ 0.25 au 负7正0（8 通道）——正 m 归零与负 m 收缩同步
判别：
  (a) 0.225 au = 9 通道（负8正0——不同步——9 缺口被填）
  (b) 0.225 au = 8 通道（负7正0——同步——边界在 0.20-0.225 之间）
中场：0.05/0.06 au——找 11→10 通道切换边界（0.04 au 11 通道、0.07 au 10 通道）
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
print("P7-5e-76：9 缺口判别 + 中场通道边界——0.225/0.05/0.06 au")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
tests = [0.05, 0.06, 0.225]

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
    pos_range = sum(1 for m in nonzero if m > 0)
    results[B] = {"n_total": tot, "n_chan": len(nonzero), "m_min": m_min, "m_max": m_max_ok,
                  "neg_range": neg_range, "pos_range": pos_range, "N_m": {str(k): v for k, v in nonzero.items()}}
    print("  B_au=%.3f（%.1f MG）→ n_total=%d 通道=%d（m=%d..%d，负%d 正%d 零%d）N_m=%s [%.0fs]"
          % (B, B*2350, tot, len(nonzero), m_min, m_max_ok, neg_range, pos_range,
             1 if 0 in nonzero else 0, {str(k): v for k, v in nonzero.items()}, time.time()-t0_all), flush=True)

print()
print("【裁决】")
print("-"*104)
r = results[0.225]
if r["n_chan"] == 9:
    print("  ★ 0.225 au = 9 通道（负%d 正%d）——正 m 归零与负 m 收缩不同步——9 缺口在 0.20-0.225 被填" % (r["neg_range"], r["pos_range"]))
elif r["n_chan"] == 8 and r["neg_range"] == 7:
    print("  ★★ 0.225 au = 8 通道（负7 正0）——正 m 归零与负 m 收缩同步——9 通道不存在——边界在 0.20-0.225 之间")
else:
    print("  ★ 0.225 au = %d 通道（负%d 正%d）——新结构" % (r["n_chan"], r["neg_range"], r["pos_range"]))
r1, r2 = results[0.05], results[0.06]
print("  中场：0.05 au = %d 通道、0.06 au = %d 通道（0.04 = 11、0.07 = 10——11→10 边界定位）" % (r1["n_chan"], r2["n_chan"]))

json.dump({str(k): v for k, v in results.items()},
          open(os.path.join(BASE, "_phase102_p7_5e76_gap9_test.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
