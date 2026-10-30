# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99f：m=−1 过零曲率 dr=0.005 独立确认（(9−1/65)/200 定案）
================================================================
dr=0.02→0.01 外推 c2(0) = 0.0449233 vs (9−1/65)/200 = 0.044923077（差 0.0005%）
dr=0.005（N_r=24000）直接确认——过零附近 9 点
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
print("P7-5e-99f：m=−1 过零曲率 dr=0.005 独立确认")
print("="*104)

N_r, r_max = 24000, 120  # dr=0.005
Bs = np.linspace(1.355, 1.385, 11)  # 过零 1.3705 附近
Es = []
for B in Bs:
    e = e0_m(N_r, r_max, -1, float(B))
    Es.append(e)
    print("  B=%.4f：E_0 = %+.8f" % (B, e), flush=True)
Es = np.array(Es)

idx0 = int(np.argmin(np.abs(Es)))
B0 = Bs[idx0]
X = Bs - B0
A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
c0, c1, c2, c3 = coef
print("\n  拟合：c1 = %+.8f、c2 = %+.8f、c3 = %+.8f、RMS = %.3e" %
      (c1, c2, c3, np.sqrt(np.mean((A@coef-Es)**2))))

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
    print("  精确过零 B* = %.7f——vs 闭式 1.370492——差 %+.6f%%"
          % (B_cross, (B_cross-1.0/(5.0/7.0+1.0/65.0))/(1.0/(5.0/7.0+1.0/65.0))*100))

print("\n★ 定案判别（dr=0.005 直接值）：")
print("  c2 = %.8f——vs (9−1/65)/200 = 0.044923077：差 %+.5f%%" % (c2, (c2-0.044923077)/0.044923077*100))
print("  c2 = %.8f——vs 9/200 = 0.0450000：差 %+.5f%%" % (c2, (c2-0.045)/0.045*100))
print("  c2 = %.8f——vs 2σ/3 = 0.0444444：差 %+.5f%%" % (c2, (c2-0.044444444)/0.044444444*100))
print("\n★ c1 = %.8f：1/c1 = %.6f" % (c1, 1.0/c1))
print("  c3 = %.8f：vs −1/63 = −0.0158730：差 %+.5f%%" % (c3, (c3+1.0/63.0)/(1.0/63.0)*100))

json.dump({"Bstar_cross": B_cross, "c1": float(c1), "c2": float(c2), "c3": float(c3),
           "form_c2": (9-1.0/65)/200},
          open(os.path.join(BASE, "_phase102_p7_5e99f_m1_shape_dr005.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
