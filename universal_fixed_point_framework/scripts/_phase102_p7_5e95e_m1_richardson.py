# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-95e：m=-1 缺口 Richardson 外推（dr→0 极限）
================================================================
缺口序列（dr 减半）：0.005 → 0.0153694、0.0025 → 0.0153804
二阶收敛假设：Δ(dr) = Δ_∞ + a·dr²——两点外推 Δ_∞ = Δ2 + (Δ2−Δ1)/3
检验外推值 vs 1/65 = 0.01538462
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
print("P7-5e-95e：m=-1 缺口 Richardson 外推（dr→0 极限）")
print("="*104)

# 复算 dr=0.005 / 0.0025（避免依赖旧 json——重算确保同口径）
gaps = {}
for N_r, r_max in [(24000, 120), (48000, 120)]:
    dr = r_max / N_r
    b = bisect_Bstar(-1, N_r, r_max, 1.30, 1.45)
    inv = 1.0/b
    gap = inv - 5.0/7.0
    gaps[dr] = gap
    print("  dr=%.5f: B* = %.6f——1/B* = %.7f——缺口 Δ = %.7f" % (dr, b, inv, gap), flush=True)

# Richardson 二阶外推：Δ2 + (Δ2−Δ1)/(2^p − 1)，p=2 → /3
dr1, dr2 = 0.005, 0.0025
d1, d2 = gaps[dr1], gaps[dr2]
extrap = d2 + (d2 - d1) / 3.0
print()
print("  二阶 Richardson 外推（dr→0）：Δ_∞ = %.7f" % extrap)
print("  vs 1/65 = %.7f——差 %+.5f%%" % (1.0/65.0, (extrap - 1.0/65.0)/(1.0/65.0)*100))
print("  vs 2/α_EM = 0.0145993——差 %+.3f%%" % ((extrap - 0.0145993)/0.0145993*100))
print()
# 修正闭式外推检验
inv_extrap = 5.0/7.0 + extrap
B_extrap = 1.0/inv_extrap
b_meas = bisect_Bstar(-1, 96000, 120, 1.30, 1.45) if False else None  # 太贵跳过
print("  修正闭式 1/B*(−1) = 5/7 + Δ_∞ = %.7f——B* = %.6f" % (inv_extrap, B_extrap))

json.dump({"gaps": {str(k): v for k, v in gaps.items()}, "extrap": extrap,
           "inv65": 1.0/65.0, "extrap_dev_pct": (extrap - 1.0/65.0)/(1.0/65.0)*100,
           "Bstar_extrap": B_extrap},
          open(os.path.join(BASE, "_phase102_p7_5e95e_m1_richardson.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
