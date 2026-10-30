# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-95：m=-1 高阶修正判别——r_max 外推收敛
================================================================
统一闭式 1/B*(−1) = 1/2 + 1/7 + 1/14 = 5/7 = 0.714286 → B*=1.4（先验偏差 2%）
候选修正：缺口 ≈ 1/(k_max·(k_max+N_gen−1)) = 1/80 = 0.0125
  修正后 1/B* = 5/7 + 1/80 = 0.726786 → B* = 1.37593
判别：m=−1 过零 r_max 外推（120/140/160/180/200）——收敛值 vs 1.37593 vs 1.4
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

def bisect_Bstar(m, r_max, lo=1.3, hi=1.5, iters=16):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        e = e0_m(1500, r_max, m, mid)
        if e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

print("="*104)
print("P7-5e-95：m=-1 高阶修正判别——r_max 外推收敛")
print("="*104)

PRED_OLD = 1.400000   # 统一闭式（无修正）
PRED_NEW = 1.375930   # +1/80 修正
results = {}
for r_max in [120, 140, 160, 180, 200]:
    b = bisect_Bstar(-1, r_max)
    results[r_max] = b
    print("  r_max=%3d: B* = %.5f——1/B* = %.6f——vs 1.4 差 %+.2f%%——vs 1.37593 差 %+.3f%%"
          % (r_max, b, 1.0/b, (b-PRED_OLD)/PRED_OLD*100, (b-PRED_NEW)/PRED_NEW*100), flush=True)

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e95_m1_extrap.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
