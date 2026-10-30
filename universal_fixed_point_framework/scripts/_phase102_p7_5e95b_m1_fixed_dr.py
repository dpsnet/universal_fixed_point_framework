# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-95b：m=-1 高阶修正判别——固定 dr 收敛（网格精度判别）
================================================================
P7-5e-95 显示 r_max 外推单调增大未饱和——但 N_r=1500 固定时 dr 随 r_max 变粗（r_max=200: dr=0.133）
  粗网格可能高估 B*——需要固定 dr（增大 N_r）判别真实收敛
判别：dr = 0.04 固定——r_max=120/160/200（N_r=3000/4000/5000）——B* 收敛 vs 1.37593（1/80）vs 1.4（原闭式）
"""
import json, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=20):
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
        return float(np.real(vals[0]))
    except Exception:
        return None

def bisect_Bstar(m, N_r, r_max, lo=1.3, hi=1.5, iters=14):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        e = e0_m(N_r, r_max, m, mid)
        if e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

print("="*104)
print("P7-5e-95b：m=-1 固定 dr 收敛判别（dr = 0.04 恒定）")
print("="*104)

PRED_NEW = 1.375930   # +1/80 修正
PRED_OLD = 1.400000   # 原闭式
results = {}
for r_max, N_r in [(120, 3000), (160, 4000), (200, 5000)]:
    b = bisect_Bstar(-1, N_r, r_max)
    results["%d/%d" % (N_r, r_max)] = b
    print("  N_r=%4d r_max=%3d (dr=%.4f): B* = %.5f——1/B* = %.6f——vs 1.37593 %+.4f%%——vs 1.4 %+.4f%%"
          % (N_r, r_max, r_max/N_r, b, 1.0/b, (b-PRED_NEW)/PRED_NEW*100, (b-PRED_OLD)/PRED_OLD*100), flush=True)

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e95b_m1_fixed_dr.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
