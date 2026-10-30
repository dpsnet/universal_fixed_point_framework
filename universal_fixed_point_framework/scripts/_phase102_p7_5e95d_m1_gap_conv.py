# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-95d：m=-1 缺口收敛值确定（dr=0.01/0.005/0.0025）
================================================================
dr=0.04 → 缺口 0.014594（2/α_EM 命中 0.04%）
dr=0.02 → 缺口 0.015171（2/α_EM 差 +3.9%）
dr 未饱和——继续细分确定缺口收敛值——再搜修正身份
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

print("="*104)
print("P7-5e-95d：m=-1 缺口收敛值确定（dr 细分）")
print("="*104)

results = {}
for N_r, r_max in [(12000, 120), (24000, 120), (48000, 120)]:
    dr = r_max / N_r
    b = bisect_Bstar(-1, N_r, r_max, 1.30, 1.45)
    results["%d/%d" % (N_r, r_max)] = b
    inv = 1.0/b
    gap = inv - 5.0/7.0
    print("  N_r=%5d r_max=%3d (dr=%.5f): B* = %.6f——1/B* = %.7f——缺口 Δ = %.7f ≈ 1/%.2f"
          % (N_r, r_max, dr, b, inv, gap, 1.0/gap), flush=True)

json.dump(results, open(os.path.join(BASE, "_phase102_p7_5e95d_m1_gap_conv.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
