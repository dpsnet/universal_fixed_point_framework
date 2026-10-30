# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99b：m=−1 过零形状高精度网格（dr=0.01）——c1/c2 框架身份定案
================================================================
dr=0.02 结果：c1 = 0.30586、c2 = 0.044921（RMS 4.2e-08）
候选：c2 ~ 9/200 = 0.045（差 0.17%）或 2σ/3 = 0.044444（差 1.07%）
dr=0.01 重跑确认收敛值
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
print("P7-5e-99b：m=−1 过零形状高精度（dr=0.01）——c1/c2 定案")
print("="*104)

N_r, r_max = 12000, 120  # dr=0.01
Bs = np.linspace(1.30, 1.44, 29)
Es = np.array([e0_m(N_r, r_max, -1, float(B)) for B in Bs])
print("  采样完成（dr=0.01，29 点）")

idx0 = int(np.argmin(np.abs(Es)))
B0 = Bs[idx0]
X = Bs - B0
A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
c0, c1, c2, c3 = coef
print("\n  拟合：c1 = %+.8f、c2 = %+.8f、c3 = %+.8f、RMS = %.3e" % (c1, c2, c3, np.sqrt(np.mean((A@coef-Es)**2))))

# 精确过零（三阶反解）
i_arr = np.where(np.diff(np.sign(Es)) != 0)[0]
B_cross = None
if len(i_arr) > 0:
    i0 = int(i_arr[0])
    # 三阶反解 E(B)=0（Newton 从插值点出发）
    Bn = Bs[i0] - Es[i0]*(Bs[i0+1]-Bs[i0])/(Es[i0+1]-Es[i0])
    for _ in range(5):
        x = Bn - B0
        e = c0 + c1*x + c2*x**2 + c3*x**3
        de = c1 + 2*c2*x + 3*c3*x**2
        Bn = Bn - e/de
    B_cross = Bn
    print("\n  三阶精确过零 B* = %.7f——vs 闭式 1.370492——差 %+.6f%%"
          % (B_cross, (B_cross-1.0/(5.0/7.0+1.0/65.0))/(1.0/(5.0/7.0+1.0/65.0))*100))

# 候选定案
print("\n★ c2 候选判别（dr=0.01）：")
cands2 = {"9/200 (N_gen²/k_max·N'²)": 9.0/200.0, "2σ/3": 2.0/15.0/3.0,
          "10σ²": 10.0/225.0, "σ/3.33": 1.0/15.0/3.333}
for name, v in cands2.items():
    print("  %s = %.8f——c2 差 %+.4f%%" % (name, v, (c2-v)/v*100))
print("\n★ c1 候选判别：")
cands1 = {"1/(13/4)": 4.0/13.0, "α₀·(N_gen/N_Weyl)·0.8": 0.5*0.75*0.8,
          "0.3": 0.3, "1/3.27": 1.0/3.27, "2/α_EM+0.29": 2.0/137.028+0.29,
          "(N_gen+N_Weyl)/23": 7.0/23.0}
for name, v in cands1.items():
    print("  %s = %.8f——c1 差 %+.4f%%" % (name, v, (c1-v)/v*100))
# 组合
print("\n★ 组合身份：")
print("  1/c1 = %.6f、1/c2 = %.6f、c1·c2 = %.6f、c2·65 = %.6f、c1·65 = %.6f"
      % (1.0/c1, 1.0/c2, c1*c2, c2*65, c1*65))
print("  c2·200 = %.6f（若 = 9 则 9/200 精确）——c2·45 = %.6f（若 = 2 则 2σ/3 精确）"
      % (c2*200, c2*45))

json.dump({"Bstar_cross": B_cross, "c1": float(c1), "c2": float(c2), "c3": float(c3)},
          open(os.path.join(BASE, "_phase102_p7_5e99b_m1_shape_hr.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
