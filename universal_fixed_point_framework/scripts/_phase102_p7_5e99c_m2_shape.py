# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99c：m=−2 过零形状——曲率 65 修正唯一性检验
================================================================
m=−1 曲率 c2 = (9−1/65)/200 = 0.0449231（65 修正——外推级 0.0005%）
若 m=−2 曲率 = 9/200 = 0.045（无 65 修正）——"65 修正仅 m=−1"在曲率层面确认
m=−2 过零 B* ≈ 0.8485（P7-5e-91）——采样 0.80..0.90 拟合过零形状
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
print("P7-5e-99c：m=−2 过零形状——曲率 65 修正唯一性检验")
print("="*104)

for N_r, r_max, label in [(6000, 120, "dr=0.02"), (12000, 120, "dr=0.01")]:
    Bs = np.linspace(0.80, 0.90, 21)
    Es = np.array([e0_m(N_r, r_max, -2, float(B)) for B in Bs])
    idx0 = int(np.argmin(np.abs(Es)))
    B0 = Bs[idx0]
    X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    # 三阶精确过零
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
        c1_02, c2_02 = c1, c2
    else:
        c1_01, c2_01 = c1, c2

# 外推 + 判别
print("\n★ m=−2 曲率判别（vs m=−1 的 (9−1/65)/200 = 0.0449231）：")
c2_extrap = c2_01 + (c2_01 - c2_02)/3.0
c1_extrap = c1_01 + (c1_01 - c1_02)/3.0
print("  c2 外推 = %.8f——vs 9/200 = 0.0450000：差 %+.5f%%（若 ≈0——无 65 修正）" % (c2_extrap, (c2_extrap-0.045)/0.045*100))
print("  c2 外推 = %.8f——vs (9−1/65)/200 = 0.0449231：差 %+.5f%%（若 ≈0——有 65 修正）" % (c2_extrap, (c2_extrap-0.044923077)/0.044923077*100))
print("  c1 外推 = %.8f——1/c1 = %.6f" % (c1_extrap, 1.0/c1_extrap))
print("\n★ 65 修正可检测量级：1/(65·200) = %.8f——c2 外推漂移若 < 此量级的一半则可判别" % (1.0/(65*200)))

json.dump({"m2_c2_extrap": float(c2_extrap), "m2_c1_extrap": float(c1_extrap),
           "nine_over_200": 0.045, "m1_form": (9-1.0/65)/200},
          open(os.path.join(BASE, "_phase102_p7_5e99c_m2_shape.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
