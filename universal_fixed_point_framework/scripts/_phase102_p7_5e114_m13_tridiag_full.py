# -*- coding: utf-8 -*-
"""P7-5e-114 m=-13 三档全量重算（三对角专用求解器，秒级）
替换 eigsh：同一离散矩阵下 tridiag（LAPACK dstemr 直接法）比 eigsh 快 ~20万倍且更准
（交叉验证：N=6000 两法一致 2.9e-11；N=24000 eigsh 偏差 5e-7，tridiag 为权威）。
输出：三档 B* + 与 eigsh 值对比 + 初步 Richardson（正式定案仍等用户确认）。
"""
import time, json, os
import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
closed = 13.0/2.0 + 1.0/7.0 + 1.0/57344.0
Bstar_closed = 1.0/closed
w = 0.0265
Bs = np.linspace(Bstar_closed*(1-w), Bstar_closed*(1+w), 7)
m = -13

def solve(N_r, B):
    dr = r_max / N_r
    j = np.arange(N_r)
    r = (j + 0.5) * dr
    d = np.ones(N_r) / dr**2 + (m + 0.5 * B * r**2)**2 / (2.0 * r**2) - 1.0 / r
    e = -np.ones(N_r - 1) / (2.0 * dr**2)
    t0 = time.time()
    v = eigvalsh_tridiagonal(d, e, select='i', select_range=(0, 0))
    return float(v[0]), time.time() - t0

print("P7-5e-114：m=-13 三档全量重算（tridiag 权威求解器）", flush=True)
print("闭式 1/B* = %.10f、B*_closed = %.8f、窗口 ±2.65%%（w=0.0265）7 点\n" % (closed, Bstar_closed), flush=True)

# eigsh 旧值（p114_out.txt 实测，供对比）
old = {0.02: 0.15076424, 0.01: 0.15076335}

results = {}
for dr in [0.02, 0.01, 0.005]:
    r_max = 120.0
    N_r = int(round(r_max / dr))
    Es = []
    for i, B in enumerate(Bs):
        e, dt = solve(N_r, float(B))
        Es.append(e)
        print("  dr=%.4f B=%.5f（%d/7）：E0 = %+.10f（%.3f s）" % (dr, B, i+1, e, dt), flush=True)
    Es = np.array(Es)
    B0 = float(Bs[len(Bs)//2])
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
    results[dr] = {"Bstar": float(Bcross), "c1": float(c1), "c2": float(c2), "c3": float(c3), "rms": rms}
    tag = ""
    if dr in old:
        d = (Bcross - old[dr]) / old[dr]
        tag = "  vs eigsh %.8f 差 %+.3e（%+.5f%%）" % (old[dr], Bcross-old[dr], d*100)
    print("dr=%.4f：c1=%+.9f c2=%+.9f c3=%+.9f  B*=%.8f  RMS=%.2e%s"
          % (dr, c1, c2, c3, Bcross, rms, tag), flush=True)

# 初步 Richardson（二阶：B(0) = (4*B(dr1) - B(dr2))/3）
B002, B001, B0005 = results[0.02]["Bstar"], results[0.01]["Bstar"], results[0.005]["Bstar"]
R2_01_005 = (4*B0005 - B001)/3.0
R2_02_01 = (4*B001 - B002)/3.0
delta = abs(1.0/R2_01_005 - closed)
print("", flush=True)
print("Richardson 二阶（0.01/0.005 档）：B*(0) = %.8f   1/B* = %.8f   δ(1/B) = %.6f"
      % (R2_01_005, 1.0/R2_01_005, delta), flush=True)
print("先验预言对照：预测 0.00992，实测 %.6f，偏差 %+.2f%%（判据 [0.0096,0.0103]）"
      % (delta, (delta-0.00992)/0.00992*100), flush=True)
print("（对照 eigsh 两档初步 0.00994）", flush=True)
json.dump({"Bstar_closed": Bstar_closed, "results": results,
           "R2_01_005": float(R2_01_005), "delta_13_tridiag": float(delta),
           "note": "tridiag 权威求解器，正式 Richardson 定案待用户确认"},
          open(os.path.join(BASE, "_phase102_p7_5e114_m13_3dr_tridiag.json"), "w", encoding="utf-8"), indent=1)
print("JSON 落盘 OK exit 0", flush=True)
