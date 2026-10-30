# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-101：m=−2 同窗口 dr 精细外推（ε 序列 2 倍家族 m=2 点定案）
================================================================
目标：99c 粗值 c1(−2)≈0.28053 → A_2 = 7.01325——候选 7+1/75（ε 层面差 0.625%）
   m=−2 同窗口 dr 扫描（固定 B 窗口、4 档 dr、Richardson 三阶）判别：
   ① B*(−2) vs 闭式 1/(1+1/7+1/28) = 0.8484848
   ② c1(−2)(0)×D_2(=25) = A_2——vs 7+1/75 = 7.013333（0.0005% 命中确认或否）
   ③ c2/c3 m 依赖延伸（m=−1/−2/−3 序列）
注意：print 全部转义（99j 末尾 % 未转义 bug 教训）——JSON 必落盘
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
print("P7-5e-101：m=−2 同窗口 dr 精细外推（ε 序列 m=2 点定案）")
print("="*104)

# 闭式 B*：1/B* = |−2|/2+1/7+1/(7·2²) = 1+1/7+1/28 = 1.1785714
Bstar_closed = 1.0 / (1.0 + 1.0/7.0 + 1.0/28.0)
print("★ 闭式 B*(−2) = %.8f（1/B = 1+1/7+1/28 = 1.1785714）" % Bstar_closed)

Bs = np.linspace(0.830, 0.867, 7)
print("★ B 窗口 = [0.830, 0.867] 7 点（围绕闭式 0.84848 ±2.1%%）")

results = {}
for dr in [0.02, 0.01, 0.005, 0.0025]:
    N_r = int(round(120.0 / dr))
    Es = np.array([e0_m(N_r, 120.0, -2, float(B)) for B in Bs])
    B0 = 0.848
    X = Bs - B0
    A = np.vstack([np.ones_like(X), X, X**2, X**3]).T
    coef, _, _, _ = np.linalg.lstsq(A, Es, rcond=None)
    c0, c1, c2, c3 = coef
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

print("\n★ 判别 ①：B*(−2) vs 闭式 0.8484848：")
print("  差 = %+.5f%%" % ((B_0 - Bstar_closed)/Bstar_closed*100))

print("\n★ 判别 ②：c1(−2)(0)×D_2(=25) = A_2：")
D2 = (8-2*2+1)**2  # (k_max−2|m|+1)² = 25
A2 = c1_0*D2
print("  A_2 = c1(−2)(0)×25 = %.9f" % A2)
print("  候选 7+1/75 = 7.0133333——差 %+.5f%%" % ((A2-7-1.0/75)/(7+1.0/75)*100))
print("  ε_2 = A_2−7 = %+.9f（vs +1/75 = +0.0133333——差 %+.3f%%）"
      % (A2-7, (A2-7-1.0/75)/(1.0/75)*100))
print("  99c 粗值：c1(−2)≈0.28053→A_2≈7.01325（ε 层面差 0.625%%——待本轮精细判别）")

print("\n★ 判别 ③：c2/c3 m 依赖延伸（m=−1/−2/−3）：")
print("  c2 序列：|m|=1: 0.0449066、|m|=2: %.8f、|m|=3: 0.1033209——比值 %.4f、%.4f"
      % (c2_0, c2_0/0.0449066, 0.1033209/c2_0))
print("  c3 序列：|m|=1: −0.015896、|m|=2: %.8f、|m|=3: −0.0852896——比值 %.4f、%.4f"
      % (c3_0, c3_0/(-0.015896), (-0.0852896)/c3_0))

json.dump({"Bstar_closed": Bstar_closed, "results": results,
           "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0, "A2": A2},
          open(os.path.join(BASE, "_phase102_p7_5e101_m2_samewin.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
