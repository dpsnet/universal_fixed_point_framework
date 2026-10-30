# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-97b：m=+1 缺口 Richardson 外推（dr→0 极限）
================================================================
dr=0.02 → 1/B*=4.218834（差 +0.023%）、dr=0.01 → 4.219051（+0.028%）
漂移方向：1/B* 增大——可能存在微缺口——外推确认收敛值
候选缺口：1/840 = N_gen·(k_max−1)·k_max·(k_max−N_gen) 倒数
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

closed = 4.0 + 1.0/7.0 + 3.0/40.0
print("="*104)
print("P7-5e-97b：m=+1 缺口 Richardson 外推")
print("="*104)
print("闭式 1/B*(+1) = 4.2178571——候选缺口 1/840 = 0.0011905（N_gen·(k_max−1)·k_max·(k_max−N_gen)）")

gaps = {}
for N_r, r_max in [(24000, 120), (48000, 120)]:
    dr = r_max / N_r
    b = bisect_Bstar(1, N_r, r_max, 0.20, 0.30)
    inv = 1.0/b
    gap = inv - closed
    gaps[dr] = gap
    print("  dr=%.5f: B* = %.7f——1/B* = %.7f——缺口 Δ = %.7f ≈ 1/%.1f"
          % (dr, b, inv, gap, 1.0/gap), flush=True)

dr1, dr2 = 0.005, 0.0025
d1, d2 = gaps[dr1], gaps[dr2]
extrap = d2 + (d2 - d1) / 3.0
print()
print("  二阶 Richardson 外推：Δ_∞ = %.7f ≈ 1/%.2f" % (extrap, 1.0/extrap))
print("  vs 1/840 = %.7f——差 %+.5f%%" % (1.0/840.0, (extrap-1.0/840.0)/(1.0/840.0)*100))
print("  vs 1/65 修正（应排除）：差 %+.2f%%" % ((extrap-1.0/65.0)/(1.0/65.0)*100))
inv_extrap = closed + extrap
print("  收敛 1/B*(+1) = %.7f——B* = %.6f" % (inv_extrap, 1.0/inv_extrap))

json.dump({"gaps": {str(k): v for k, v in gaps.items()}, "extrap": extrap,
           "inv840": 1.0/840.0, "inv65": 1.0/65.0,
           "extrap_vs_inv840_pct": (extrap-1.0/840.0)/(1.0/840.0)*100,
           "inv_extrap": inv_extrap},
          open(os.path.join(BASE, "_phase102_p7_5e97b_m1plus_richardson.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
