# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-71：线性律先验检验——0.5/0.6/0.7 au
================================================================
P7-5e-70 发现：高场端负 m 范围 = 12 − 20·B_au（线性律）
  0.25 au：负 7（n=8）、0.30：负 6（n=7）、0.35：负 5（n=6）、0.40：负 4（n=5）
两条竞争预言：
  (a) 线性律继续：0.5 au → 负 2（n=3）、0.6 au → 负 0（n=1）
  (b) N_Weyl 饱和：0.5/0.6 au → 负 4（n=5——5 平台延伸）
判别时刻——先算！
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
print("P7-5e-71：线性律先验检验——0.5/0.6/0.7 au")
print("="*104)

N_r, r_max, m_max = 1500, 60.0, 8
tests = [(0.5, "(a)线性 负2 n=3 / (b)饱和 负4 n=5"),
         (0.6, "(a)线性 负0 n=1 / (b)饱和 负4 n=5"),
         (0.7, "(a)线性 负<0 n=? / (b)饱和 负4 n=5")]

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
    n_chan = len(nonzero)
    lin_pred_neg = max(0, 12 - 20 * B)
    results[B] = {"n_total": tot, "n_chan": n_chan, "m_min": m_min, "m_max": m_max_ok,
                  "neg_range": neg_range, "pos_range": pos_range, "lin_pred": lin_pred_neg}
    print()
    print("【B_au=%.2f（%.1f MG）——预言 %s】" % (B, B*2350, pred))
    print("  实测：n_total=%d 通道=%d（m=%d..%d，负%d 正%d 零%d）"
          % (tot, n_chan, m_min, m_max_ok, neg_range, pos_range, 1 if 0 in nonzero else 0))
    print("  线性律预言负 m 范围 = 12−20×%.2f = %d" % (B, lin_pred_neg))
    if lin_pred_neg == neg_range:
        print("  ★★ 线性律命中（负 m 范围 = %d）" % neg_range)
    elif neg_range == 4 and lin_pred_neg < 4:
        print("  ★★ N_Weyl 饱和命中（负 m 范围保持 4）")
    else:
        print("  ★ 两预言均未命中（负 m 范围 = %d）——新结构" % neg_range)
    print("  N_m 分布：%s" % {str(k): v for k, v in nonzero.items()}, flush=True)

print()
print("【裁决】")
print("-"*104)
for B, r in results.items():
    print("  B=%.2f：n=%d 负m=%d 线性预言=%d → %s"
          % (B, r["n_total"], r["neg_range"], r["lin_pred"],
             "线性命中" if r["lin_pred"] == r["neg_range"] else ("饱和命中" if r["neg_range"] == 4 else "新结构")))

json.dump({str(k): v for k, v in results.items()},
          open(os.path.join(BASE, "_phase102_p7_5e71_linear_test.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
