# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-97：m=+1 高精度收敛检验（65 修正唯一性判别）
================================================================
P7-5e-89 的 +1 闭式：1/B*(+1) = 4+1/7+3/40 = 4.217857（3/40 = N_gen/(k_max·(k_max−N_gen))）
若 m=−1 独享 65 修正，+1 应在 dr 细分后仍命中 4.217857（无 1/65 项）
dr=0.04 → B*=0.237078（1/B*=4.21802）——dr 细分检验漂移
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

def bisect_Bstar(m, N_r, r_max, lo, hi, iters=16):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        e = e0_m(N_r, r_max, m, mid)
        if e > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

closed = 4.0 + 1.0/7.0 + 3.0/40.0  # 4.217857
print("="*104)
print("P7-5e-97：m=+1 高精度收敛检验（65 修正唯一性判别）")
print("="*104)
print("+1 闭式：1/B*(+1) = 4+1/7+3/40 = %.7f——B* = %.7f" % (closed, 1.0/closed))

results = {}
for N_r, r_max in [(1500, 60), (3000, 120), (6000, 120), (12000, 120)]:
    dr = r_max / N_r
    b = bisect_Bstar(1, N_r, r_max, 0.20, 0.30)
    results["%d/%d" % (N_r, r_max)] = b
    inv = 1.0/b
    print("  N_r=%5d r_max=%3d (dr=%.5f): B* = %.7f——1/B* = %.7f——vs 闭式差 %+.5f%%"
          % (N_r, r_max, dr, b, inv, (inv-closed)/closed*100), flush=True)
    # 若加 1/65 会是多少
    closed65 = closed + 1.0/65.0
    print("     vs 闭式+1/65 = %.7f：差 %+.4f%%" % (closed65, (inv-closed65)/closed65*100))

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e97_m1plus_conv.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
