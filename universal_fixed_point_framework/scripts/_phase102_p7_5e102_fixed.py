# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-102 修复版：7 点全齐（e6 已算）+ 5 档 4 阶 Richardson 定案
================================================================
修复：① Es 取 dict key（E0）而非 value（B）——前版取错值导致拟合发散
      ② 101 JSON key 为 str(dr)（"0.02" 等）——非 "%.4f" 格式
B[6] 已算：0.8670 → E0 = +0.0051750175（不再重算）
"""
import json, os
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import warnings
warnings.filterwarnings('ignore')

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

print("="*104)
print("P7-5e-102 修复版：7 点全齐 + 5 档 4 阶 Richardson 定案")
print("="*104)

Bstar_closed = 1.0 / (1.0 + 1.0/7.0 + 1.0/28.0)
print("★ 闭式 B*(−2) = %.8f" % Bstar_closed)

# 7 点全数据（dr=0.00125、N_r=96000、m=−2）——B 升序对齐
Bs = np.array([0.8300, 0.8362, 0.8423, 0.8485, 0.8547, 0.8608, 0.8670])
Es = np.array([-0.0051960176, -0.0034814936, -0.0017612961, -0.0000354865,
               +0.0016958760, +0.0034327297, +0.0051750175])

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
print("\n★ dr=0.00125 单档：c1 = %+.9f、c2 = %+.9f、c3 = %+.9f、B* = %.8f、RMS = %.2e"
      % (c1, c2, c3, Bcross, rms))

# 合并 101 四档做 5 档 4 阶 Richardson（key = str(dr)）
j101 = json.load(open(os.path.join(BASE, "_phase102_p7_5e101_m2_samewin.json"), "r", encoding="utf-8"))
drs = [0.02, 0.01, 0.005, 0.0025, 0.00125]
keys = [str(d) for d in drs]
print("★ 101 JSON keys:", list(j101["results"].keys()))
c1s = [j101["results"][k]["c1"] for k in keys[:4]] + [float(c1)]
c2s = [j101["results"][k]["c2"] for k in keys[:4]] + [float(c2)]
c3s = [j101["results"][k]["c3"] for k in keys[:4]] + [float(c3)]
Brs = [j101["results"][k]["B*"] for k in keys[:4]] + [float(Bcross)]

def rich4(vals):
    v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(4)]
    v2 = [(16*v1[i+1]-v1[i])/15.0 for i in range(3)]
    v3 = [(64*v2[i+1]-v2[i])/63.0 for i in range(2)]
    v4 = (256*v3[1]-v3[0])/255.0
    return v1, v2, v3, v4

_, _, _, c1_0 = rich4(c1s)
_, _, _, c2_0 = rich4(c2s)
_, _, _, c3_0 = rich4(c3s)
_, _, _, B_0 = rich4(Brs)

print("\n★ 5 档 4 阶 Richardson 外推 dr→0：")
print("  c1(0) = %.9f、c2(0) = %.9f、c3(0) = %.9f、B*(0) = %.8f" % (c1_0, c2_0, c3_0, B_0))

A2 = c1_0 * 25
eps2 = A2 - 7
print("\n★ 判别 ①：A_2 = c1(0)×25 = %.9f——ε_2 = %+.9f" % (A2, eps2))
print("  候选 3/500 = 0.006——差 %+.4f%%" % ((eps2-0.006)/0.006*100))
print("  候选 1/167 = 0.0059880——差 %+.4f%%" % ((eps2-1.0/167.0)/(1.0/167.0)*100))
print("  比例 ε_1/ε_2（ε_1=−1/150）：%.6f（10/9=1.11111——差 %+.4f%%）"
      % ((1.0/150.0)/eps2, ((1.0/150.0)/eps2-10.0/9.0)/(10.0/9.0)*100))

print("\n★ 判别 ②：B*(−2) 失调——vs 闭式 0.8484848：")
print("  差 %+.5f%%" % ((B_0-Bstar_closed)/Bstar_closed*100))
d_inv2 = 1.0/B_0 - 1.0/Bstar_closed
print("  1/B 层面修正 = %+.8f（m=−3 为 −0.0003494）" % d_inv2)
print("  比值 δ(1/B)(m=3)/δ(1/B)(m=2) = %.4f" % (0.0003494/abs(d_inv2)))

json.dump({"dr00125": {"Bs": Bs.tolist(), "Es": Es.tolist(),
                       "c1": float(c1), "c2": float(c2), "c3": float(c3),
                       "B*": float(Bcross), "rms": rms},
           "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0, "A2": A2, "eps2": eps2},
          open(os.path.join(BASE, "_phase102_p7_5e102_m2_dr00125.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
