# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99d：m=−3 过零形状——c1/c2/c3 的 m 依赖趋势
================================================================
c1(−1)=0.30599、c1(−2)=0.28053（≈7/25=0.28 差0.19%）
c2(−1)=0.044923、c2(−2)=0.072877（非9/200家族）
c3(−1)=−0.01591（≈−1/63=k_max²−1？差0.23%）
m=−3 过零 B* ≈ 0.5773（闭式 1/B* = 3/2+1/7+1/56 = 1.73214）——采样 0.54..0.62
"""
import json, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

def e0_m(N_r, r_max, m, B, k=12):
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

print("="*104)
print("P7-5e-99d：m=−3 过零形状——c1/c2/c3 m 依赖趋势")
print("="*104)

for N_r, r_max, label in [(6000, 120, "dr=0.02"), (12000, 120, "dr=0.01")]:
    Bs = np.linspace(0.54, 0.62, 21)
    Es = np.array([e0_m(N_r, r_max, -3, float(B)) for B in Bs])
    idx0 = int(np.argmin(np.abs(Es)))
    B0 = Bs[idx0]
    X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    i_arr = np.where(np.diff(np.sign(Es)) != 0)[0]
    B_cross = None
    if len(i_arr) > 0:
        i0 = int(i_arr[0])
        Bn = Bs[i0] - Es[i0]*(Bs[i0+1]-Bs[i0])/(Es[i0+1]-Es[i0])
        for _ in range(5):
            x = Bn - B0
            e = c0 + c1*x + c2*x**2 + c3*x**3
            de = c1 + 2*c2*x + 3*c3*x**2
            Bn = Bn - e/de
        B_cross = Bn
    print("  %s：c1 = %+.8f、c2 = %+.8f、c3 = %+.8f、RMS = %.3e、B* = %.7f"
          % (label, c1, c2, c3, np.sqrt(np.mean((A@coef-Es)**2)), B_cross), flush=True)
    if N_r == 6000:
        c1_02, c2_02, c3_02 = c1, c2, c3
    else:
        c1_01, c2_01, c3_01 = c1, c2, c3

c1e = c1_01 + (c1_01-c1_02)/3.0
c2e = c2_01 + (c2_01-c2_02)/3.0
c3e = c3_01 + (c3_01-c3_02)/3.0
print("\n★ m=−3 外推：c1 = %.7f、c2 = %.7f、c3 = %.7f" % (c1e, c2e, c3e))

print("\n★ m 依赖趋势（c1/c2/c3 vs |m|）：")
print("  |m|=1：c1 = 0.30599、c2 = 0.044923、c3 = −0.01591")
print("  |m|=2：c1 = 0.28053、c2 = 0.072877、c3 = −0.04240")
print("  |m|=3：c1 = %.7f、c2 = %.7f、c3 = %.7f" % (c1e, c2e, c3e))
print("\n★ 候选判别：")
print("  c1(−3) vs 7/25=0.28：差 %+.4f%%（m=−2 候选 0.19%）" % ((c1e-0.28)/0.28*100))
print("  c1(−3) vs c1(−2)−Δ：c1(−2)−c1(−3) = %.6f、c1(−1)−c1(−2) = %.6f（差值趋势）"
      % (0.28053-c1e, 0.30599-0.28053))
print("  c2(−3) vs c2(−2)×?：c2(−3)/c2(−2) = %.4f、c2(−2)/c2(−1) = %.4f"
      % (c2e/0.072877, 0.072877/0.044923))
print("  c3(−3) vs −1/63：差 %+.4f%%（m=−1 候选 0.23%）" % ((c3e+1.0/63.0)/(1.0/63.0)*100))
print("  c3(−2) vs −1/63：差 %+.4f%%" % ((-0.04240+1.0/63.0)/(1.0/63.0)*100))

json.dump({"m3": {"c1": float(c1e), "c2": float(c2e), "c3": float(c3e)}},
          open(os.path.join(BASE, "_phase102_p7_5e99d_m3_shape.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
