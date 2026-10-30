# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-106：m=−5 同窗口 dr 精细外推（失调第四点 + c1/c2/c3 演化五点判别）
================================================================
动机（P7-5e-105 全链演化分析定案后）：四点→五点定案判别——
   ① B*(−5) 失调第四点：是否落入 {−0.0169, −0.0210, −0.0204}% 均匀带（无 m 漂移）
   ② c1 增量是否继续减半（几何衰减趋极限确认——105 预测增量 ~0.0025）
   ③ c2 增量是否仍 ≈κ/63 = 0.0303（线性延续——105 预测 c2(5) ≈ 0.1643）
   ④ c3 二阶差分是否仍 ≈1/65 = 0.015385（位点 3 确认——105 预测 c3(5) ≈ −0.2156）
   ⑤ A_5 = c1×D_5（D_5 = (8−10+1)² = 1）vs 主结构 2⁰−1 = 0（m=5 主结构归零——断裂终态）
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
    # 降级重试：tol/maxiter 递进（m=−5 大 N_r 收敛慢——106 诊断单点 416s）
    for tol, maxiter in [(1e-9, 50000), (1e-8, 100000), (1e-7, 150000)]:
        try:
            vals, _ = eigsh(H.astype(np.float64), k=min(k, N_r - 5),
                            which='SA', maxiter=maxiter, tol=tol)
            return float(np.real(vals[0]))
        except Exception:
            continue
    raise RuntimeError("eigsh 全部降级失败：N_r=%d m=%d B=%.6f" % (N_r, m, B))

print("="*104)
print("P7-5e-106：m=−5 同窗口 dr 精细外推（失调第四点 + 演化五点判别）")
print("="*104)

# 闭式 B*：1/B* = |−5|/2+1/7+1/(7·2⁵) = 5/2+1/7+1/224 = 593/224 = 2.6473214
Bstar_closed = 224.0 / 593.0
print("★ 闭式 B*(−5) = %.8f（1/B = 5/2+1/7+1/224 = 593/224 = 2.6473214）" % Bstar_closed)

Bs = np.linspace(0.368, 0.388, 7)
print("★ B 窗口 = [0.368, 0.388] 7 点（围绕闭式 0.37774 ±2.7%%）")

results = {}
for dr in [0.02, 0.01, 0.005, 0.0025]:
    N_r = int(round(120.0 / dr))
    Es = np.array([e0_m(N_r, 120.0, -5, float(B)) for B in Bs])
    B0 = 0.378
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

print("\n★ 判别 ①：B*(−5) vs 闭式 0.3777420：")
d1B = (1.0/B_0 - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
print("  失调 = %+.5f%%（B 域 %+.5f%%）" % (d1B, (B_0 - Bstar_closed)/Bstar_closed*100))
print("  失调均匀性四点：m=−2: +0.0169%%、m=−3: +0.0210%%、m=−4: +0.0204%%、m=−5: %+.5f%%" % d1B)
print("  δ(1/B) 绝对值四点：m=−2: −0.0001987、m=−3: −0.0003494、m=−4: −0.0004382、m=−5: %+.8f"
      % (1.0/B_0 - 1.0/Bstar_closed))

print("\n★ 判别 ②：c1 第五点（几何衰减趋极限）：")
c1s = [0.305988839, 0.280239903, 0.270538229, 0.265594666, c1_0]
print("  c1 五点：%s" % ["%.8f" % v for v in c1s])
d1c1 = [(c1s[i+1]-c1s[i]) for i in range(4)]
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c1])
print("  增量比（前一/后一）：%s（105 预测第 4 增量 ~0.0025——减半确认？）"
      % ["%.3f" % (abs(d1c1[i])/abs(d1c1[i+1])) for i in range(3)])

print("\n★ 判别 ③：c2 第五点（线性 κ/63 延续）：")
c2s = [0.044906645, 0.073071272, 0.103320868, 0.133962811, c2_0]
print("  c2 五点：%s" % ["%.8f" % v for v in c2s])
d1c2 = [(c2s[i+1]-c2s[i]) for i in range(4)]
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c2])
print("  增量 vs κ/63 = 0.0303152：%s" % ["%+.3f%%" % (v/0.0303152*100-100) for v in d1c2])

print("\n★ 判别 ④：c3 第五点（二阶差分 1/65 位点 3）：")
c3s = [-0.015896, -0.042538365, -0.085289609, -0.142764543, c3_0]
print("  c3 五点：%s" % ["%.8f" % v for v in c3s])
d1c3 = [(c3s[i+1]-c3s[i]) for i in range(4)]
d2c3 = [(d1c3[i+1]-d1c3[i]) for i in range(3)]
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c3])
print("  二阶差分：%s——vs 1/65 = 0.0153846：%s（位点 3 四点确认？）"
      % (["%+.8f" % v for v in d2c3], ["%+.3f%%" % (abs(v)/0.0153846*100-100) for v in d2c3]))

print("\n★ 判别 ⑤：A_5 = c1×D_5（D_5 = (8−10+1)² = 1）：")
D5 = (8-2*5+1)**2
A5 = c1_0*D5
print("  A_5 = c1(−5)(0)×1 = %.9f——主结构 2^(5−5)−1 = 0（m=5 主结构归零）——A_5 = %.4f ≠ 0——断裂终态" % (A5, A5))
print("  A 全序列：m=1: 14.9933、2: 7.0060、3: 2.4348、4: 0.2656、5: %.6f" % A5)

json.dump({"Bstar_closed": Bstar_closed, "results": results,
           "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0, "A5": A5,
           "delta_1B_pct": d1B, "delta_1B_abs": 1.0/B_0 - 1.0/Bstar_closed},
          open(os.path.join(BASE, "_phase102_p7_5e106_m5_samewin.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
