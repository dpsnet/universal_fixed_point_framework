# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-99j：m=−3 同窗口 dr 定案（修正项 2 倍家族判别 + 99d 算术复核）
================================================================
99d 错误：闭式 1/B*(−3) = 3/2+1/7+1/56 = 1.660714（不是 1.73214）
          → 正确闭式 B* = 0.6021505——实测 0.60228 差仅 0.02%——需复核
本轮：固定 B 窗口围绕过零，4 档 dr × 7 点，Richardson 外推
判别：① B*(−3) vs 闭式 0.6021505
      ② c1(−3) 修正项家族：ε 序列 m=−1: −1/150、m=−2: +1/75（符号交替 2 倍）
         → m=−3 预测 ε = −1/37.5（若家族成立）——D_m 预测 (k_max−2|m|+1)² = 9
      ③ c2/c3 m 依赖趋势延伸
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
print("P7-5e-99j：m=−3 同窗口 dr 定案（修正项 2 倍家族判别）")
print("="*104)

# 闭式 B*：1/B* = 3/2+1/7+1/56 = 1.6607143
Bstar_closed = 1.0 / (1.5 + 1.0/7.0 + 1.0/56.0)
print("★ 闭式 B*(−3) = %.8f（99d 注释 1.73214 为算术错误——正确 1.660714）" % Bstar_closed)

Bs = np.linspace(0.589, 0.615, 7)
print("★ B 窗口 = [0.589, 0.615] 7 点（围绕闭式 0.60215 ±2.1%）")

results = {}
for dr in [0.02, 0.01, 0.005, 0.0025]:
    N_r = int(round(120.0 / dr))
    Es = np.array([e0_m(N_r, 120.0, -3, float(B)) for B in Bs])
    B0 = 0.602
    X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
    # 过零：c0+c1 x+c2 x²+c3 x³ = 0 的根（牛顿，初值 −(c0/c1)）
    x = -c0/c1
    for _ in range(6):
        e = c0 + c1*x + c2*x**2 + c3*x**3
        de = c1 + 2*c2*x + 3*c3*x**2
        x = x - e/de
    Bcross = B0 + x
    rms = float(np.sqrt(np.mean((A@coef-Es)**2)))
    results[dr] = {"c1": float(c1), "c2": float(c2), "c3": float(c3), "B*": float(Bcross), "rms": rms}
    print("  dr=%.4f：c1 = %+.9f、c2 = %+.9f、c3 = %+.9f、B* = %.8f、RMS = %.2e"
          % (dr, c1, c2, c3, Bcross, rms), flush=True)

# Richardson 二阶外推（dr 减半对）
drs = [0.02, 0.01, 0.005, 0.0025]
def rich(vals):
    v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(3)]
    v2 = [(16*v1[i+1]-v1[i])/15.0 for i in range(2)]
    v3 = (64*v2[1]-v2[0])/63.0
    return v1, v2, v3

c1r = [results[d]["c1"] for d in drs]
c2r = [results[d]["c2"] for d in drs]
c3r = [results[d]["c3"] for d in drs]
Br  = [results[d]["B*"] for d in drs]

_, _, c1_0 = rich(c1r)
_, _, c2_0 = rich(c2r)
_, _, c3_0 = rich(c3r)
_, _, B_0 = rich(Br)

print("\n★ Richardson 三阶外推 dr→0：")
print("  c1(0) = %.9f、c2(0) = %.9f、c3(0) = %.9f、B*(0) = %.8f" % (c1_0, c2_0, c3_0, B_0))

print("\n★ 判别 ①：B*(−3) vs 闭式 0.6021505：")
print("  差 = %+.5f%%" % ((B_0 - Bstar_closed)/Bstar_closed*100))

print("\n★ 判别 ②：c1(−3) 修正项家族（ε 序列 −1/150、+1/75、?——符号交替 2 倍）：")
D3 = (8-2*3+1)**2  # (k_max−2|m|+1)² = 9
print("  c1(−3)(0)×D_3(=9) = %.8f" % (c1_0*D3))
print("  若家族成立 ε_3 = −1/37.5 = −0.0266667——则 A_3 候选 = %.8f" % (c1_0*D3 + 1.0/37.5))
print("  A 序列回顾：A_1 = 15（c1×49）、A_2 = 7（c1×25）——A_3 = ?")
print("  完整 ε 序列：−1/150、+1/75、%+.8f（预测 −1/37.5 若家族成立）" % (c1_0*D3 - (c1_0*D3)))

print("\n★ 判别 ③：c2/c3 m 依赖延伸：")
print("  c2 序列：|m|=1: 0.0449066、|m|=2: 0.0728771、|m|=3: %.8f——比值 %.4f、%.4f"
      % (c2_0, c2_0/0.0728771, 0.0728771/0.0449066))
print("  c3 序列：|m|=1: −0.015896、|m|=2: −0.042403、|m|=3: %.8f——比值 %.4f、%.4f"
      % (c3_0, c3_0/(-0.042403), (-0.042403)/(-0.015896)))
print("  c3 vs −1/63：差 %+.5f%%（m=−1 候选 0.15%）" % ((c3_0+1.0/63.0)/(1.0/63.0)*100))

json.dump({"Bstar_closed": Bstar_closed, "results": results,
           "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0},
          open(os.path.join(BASE, "_phase102_p7_5e99j_m3_samewin.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
