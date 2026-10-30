# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-95c：m=-1 收敛确认 + 2/α_EM 修正判别
================================================================
固定 dr=0.04 已给 B*=1.37197（三 r_max 一致）——dr=0.02 确认收敛饱和
缺口 Δ = 1/B*(−1) − 5/7 = 0.728881 − 0.714286 = 0.014595
候选修正：2/α_EM = 2/(24(d_H+3)) = 1/(12(d_H+3)) = 0.0145959（框架量纯组合——N_gen·N_Weyl·(d_H+3)）
判别：dr=0.02 的 B* vs 修正闭式 1/B* = 5/7 + 2/α_EM → B* = 1.371965
"""
import json, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
DH = 15.0 * np.log(np.e)  # placeholder
import math
dH = math.log(15.0)
alpha_EM_inv = 24.0 * (dH + 3.0)

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
print("P7-5e-95c：m=-1 收敛确认（dr=0.02）+ 2/α_EM 修正判别")
print("="*104)
print("框架量：d_H = ln15 = %.7f——1/α_EM = 24(d_H+3) = %.7f——2/α_EM = %.7f"
      % (dH, alpha_EM_inv, 2.0/alpha_EM_inv))
print("统一闭式 5/7 = %.9f——修正后 1/B* = %.9f——修正闭式 B* = %.6f"
      % (5.0/7.0, 5.0/7.0 + 2.0/alpha_EM_inv, 1.0/(5.0/7.0 + 2.0/alpha_EM_inv)))

results = {}
for N_r, r_max, dr in [(6000, 120, 0.02), (3000, 120, 0.04)]:
    b = bisect_Bstar(-1, N_r, r_max, 1.30, 1.45)
    results["%d/%d" % (N_r, r_max)] = b
    inv = 1.0/b
    print()
    print("  N_r=%4d r_max=%3d (dr=%.3f): B* = %.6f——1/B* = %.7f" % (N_r, r_max, dr, b, inv))
    print("    缺口 Δ = 1/B* − 5/7 = %.7f——vs 2/α_EM = %.7f——差 %+.4f%%"
          % (inv - 5.0/7.0, 2.0/alpha_EM_inv, (inv-5.0/7.0 - 2.0/alpha_EM_inv)/(2.0/alpha_EM_inv)*100))
    print("    B* vs 修正闭式 %.6f：差 %+.5f%%——vs 原闭式 1.4：差 %+.4f%%"
          % (1.0/(5.0/7.0+2.0/alpha_EM_inv), (b - 1.0/(5.0/7.0+2.0/alpha_EM_inv))/(1.0/(5.0/7.0+2.0/alpha_EM_inv))*100, (b-1.4)/1.4*100))

json.dump({"dH": dH, "alpha_EM_inv": alpha_EM_inv, "correction": 2.0/alpha_EM_inv, **results},
          open(os.path.join(BASE, "_phase102_p7_5e95c_m1_alphaEM.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 ✓  exit 0")
