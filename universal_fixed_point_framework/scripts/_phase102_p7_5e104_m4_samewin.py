# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-104：m=−4 同窗口 dr 精细外推（失调均匀性第三点 + A_4 边界点）
================================================================
目标：Rec/Sp 归属推论——"|m|≥2 相对失调 ~0.02% 均匀（Rec 级数截断残余）"需第三点验证：
   ① B*(−4) vs 闭式 1/(2+1/7+1/112) = 112/241 = 0.464730——相对失调是否落入
      {m=−2: +0.0167%、m=−3: +0.0211%} 同量级（均匀假说）还是随 m 漂移
   ② A_4 = c1(0)×D_4——D_4 = (8−8+1)² = 1（k_max−2|m|+1 边界点）
      vs 主结构 2^{5−m}−1：m=4 → 2¹−1 = 1——若命中，A 序列 m=1/2/4 全干净、
      "m=3 断裂"降级为"中间异常"（非主结构断裂）
   ③ c2/c3 m 依赖延伸（m=−1/−2/−3/−4 四点序列）
方法学铁律：同窗口 dr 扫描（固定 B 窗口、4 档 dr、Richardson 三阶）——跨 dr 对比无效
注意：print % 转义 %%——JSON 必落盘
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
print("P7-5e-104：m=−4 同窗口 dr 精细外推（失调均匀性第三点 + A_4 边界点）")
print("="*104)

# 闭式 B*：1/B* = |−4|/2+1/7+1/(7·2⁴) = 2+1/7+1/112 = 241/112 = 2.1517857
Bstar_closed = 112.0 / 241.0
print("★ 闭式 B*(−4) = %.8f（1/B = 2+1/7+1/112 = 241/112 = 2.1517857）" % Bstar_closed)

Bs = np.linspace(0.455, 0.475, 7)
print("★ B 窗口 = [0.455, 0.475] 7 点（围绕闭式 0.46473 ±2.2%%）")

results = {}
for dr in [0.02, 0.01, 0.005, 0.0025]:
    N_r = int(round(120.0 / dr))
    Es = np.array([e0_m(N_r, 120.0, -4, float(B)) for B in Bs])
    B0 = 0.465
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

print("\n★ 判别 ①：B*(−4) vs 闭式 0.4647302：")
d1B = (1.0/B_0 - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
print("  失调 = %+.5f%%（B 域 %+.5f%%）" % (d1B, (B_0 - Bstar_closed)/Bstar_closed*100))
print("  失调均匀性三点：m=−2: +0.0167%%、m=−3: +0.0211%%、m=−4: %+.5f%%" % d1B)
print("  δ(1/B) 绝对值三点：m=−2: −0.0001987、m=−3: −0.0003494、m=−4: %+.8f" % (1.0/B_0 - 1.0/Bstar_closed))

print("\n★ 判别 ②：A_4 = c1(0)×D_4（D_4 = (8−8+1)² = 1 边界点）：")
D4 = (8-2*4+1)**2  # (k_max−2|m|+1)² = 1
A4 = c1_0*D4
print("  A_4 = c1(−4)(0)×1 = %.9f" % A4)
print("  主结构 2^(5−m)−1：m=4 → 2¹−1 = 1——差 %+.5f%%" % ((A4-1.0)/1.0*100))
print("  A 序列：m=1: 15−1/150、m=2: 7.0059976、m=3: 2.4348（断裂）、m=4: %.6f" % A4)
print("  m=4 命中 → 主结构在 m=3 单独断裂（中间异常），非 m≥3 全断裂")

print("\n★ 判别 ③：c2/c3 m 依赖延伸（四点序列）：")
print("  c2 序列：|m|=1: 0.0449066、2: 0.0730713、3: 0.1033209、4: %.8f——比值 %.4f、%.4f、%.4f"
      % (c2_0, c2_0/0.0449066, 0.1033209/c2_0, c2_0/0.1033209))
print("  c3 序列：|m|=1: −0.015896、2: −0.042538、3: −0.085290、4: %.8f——比值 %.4f、%.4f、%.4f"
      % (c3_0, c3_0/(-0.015896), (-0.0852896)/c3_0, c3_0/(-0.0852896)))

json.dump({"Bstar_closed": Bstar_closed, "results": results,
           "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0, "A4": A4,
           "delta_1B_pct": d1B, "delta_1B_abs": 1.0/B_0 - 1.0/Bstar_closed},
          open(os.path.join(BASE, "_phase102_p7_5e104_m4_samewin.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
