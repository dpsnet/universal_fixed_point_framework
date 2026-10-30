# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-102 恢复版：复用已算 6 点 + 补算 B[6] + 5 档 4 阶 Richardson 定案
================================================================
中断恢复：原脚本被终止（B[0]-B[5] 已算完、B[6] 未算、JSON 未落盘）
已算（dr=0.00125、N_r=96000、m=−2、B=[0.830,0.867] 7 点）：
  B[0]=0.8300 E0=-0.0051960176
  B[1]=0.8362 E0=-0.0034814936
  B[2]=0.8423 E0=-0.0017612961
  B[3]=0.8485 E0=-0.0000354865
  B[4]=0.8547 E0=+0.0016958760
  B[5]=0.8608 E0=+0.0034327297
补算 B[6]=0.8670——合并 7 点拟合 + 5 档 4 阶 Richardson（101 四档 + 本档）
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
print("P7-5e-102 恢复版：补算 B[6] + 5 档 4 阶 Richardson 定案")
print("="*104)

Bstar_closed = 1.0 / (1.0 + 1.0/7.0 + 1.0/28.0)
print("★ 闭式 B*(−2) = %.8f" % Bstar_closed)

# 已算 6 点（dr=0.00125）
Es_done = {-0.0051960176: 0.8300, -0.0034814936: 0.8362, -0.0017612961: 0.8423,
           -0.0000354865: 0.8485, 0.0016958760: 0.8547, 0.0034327297: 0.8608}
Bs = np.array([0.8300, 0.8362, 0.8423, 0.8485, 0.8547, 0.8608, 0.8670])
Es = np.array([e for e, b in Es_done.items()][:6])  # 注意 dict 顺序——用 Bs 对齐
# 重新按 Bs 顺序组织
Es = np.array([v for k, v in sorted(Es_done.items(), key=lambda kv: kv[1])][:6])

print("★ 补算 B[6] = 0.8670（dr=0.00125、N_r=96000——约 15 分钟）", flush=True)
e6 = e0_m(96000, 120.0, -2, 0.8670)
Es = np.append(Es, e6)
print("  B[6] = 0.8670：E0 = %+.10f" % e6, flush=True)

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

# 合并 101 四档做 5 档 4 阶 Richardson
j101 = json.load(open(os.path.join(BASE, "_phase102_p7_5e101_m2_samewin.json"), "r", encoding="utf-8"))
drs = [0.02, 0.01, 0.005, 0.0025, 0.00125]
c1s = [j101["results"]["%.4f" % d]["c1"] for d in drs[:4]] + [float(c1)]
c2s = [j101["results"]["%.4f" % d]["c2"] for d in drs[:4]] + [float(c2)]
c3s = [j101["results"]["%.4f" % d]["c3"] for d in drs[:4]] + [float(c3)]
Brs = [j101["results"]["%.4f" % d]["B*"] for d in drs[:4]] + [float(Bcross)]

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
