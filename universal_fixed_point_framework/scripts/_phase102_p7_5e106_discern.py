# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-106 判别：合并 4 档 Richardson 三阶外推 + 五点判别
================================================================
数据源：
  dr=0.0200/0.0100/0.0050 —— 主脚本 p106_out.txt 已成功输出（106 崩溃前）
  dr=0.0025 —— 续跑 106b JSON
输出：B*(0)、c1/c2/c3(0)、失调第四点、c1/c2/c3 五点序列、A_5、判别结论
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

# 前 3 档（来自 p106_out.txt 输出）
data = {
    0.02:  {"c1": 0.262484991, "c2": 0.164981843, "c3": -0.217778207, "B*": 0.37794172},
    0.01:  {"c1": 0.262493237, "c2": 0.164992432, "c3": -0.217784721, "B*": 0.37793567},
    0.005: {"c1": 0.262495301, "c2": 0.164995303, "c3": -0.217801278, "B*": 0.37793416},
}
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e106_m5_dr0025.json"), encoding="utf-8"))
data[0.0025] = {"c1": j["c1"], "c2": j["c2"], "c3": j["c3"], "B*": j["B*"]}

drs = [0.02, 0.01, 0.005, 0.0025]
def rich(vals):
    v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(3)]
    v2 = [(16*v1[i+1]-v1[i])/15.0 for i in range(2)]
    v3 = (64*v2[1]-v2[0])/63.0
    return v1, v2, v3

c1r = [data[d]["c1"] for d in drs]
c2r = [data[d]["c2"] for d in drs]
c3r = [data[d]["c3"] for d in drs]
Br  = [data[d]["B*"] for d in drs]

_, _, c1_0 = rich(c1r)
_, _, c2_0 = rich(c2r)
_, _, c3_0 = rich(c3r)
_, _, B_0 = rich(Br)

print("="*104)
print("P7-5e-106 判别（合并 4 档 Richardson 三阶）")
print("="*104)
print("逐档：")
for d in drs:
    print("  dr=%.4f：c1=%+.9f c2=%+.9f c3=%+.9f B*=%+.8f" % (d, data[d]["c1"], data[d]["c2"], data[d]["c3"], data[d]["B*"]))
print("\n★ Richardson 三阶外推 dr→0：")
print("  c1(0) = %.9f、c2(0) = %.9f、c3(0) = %.9f、B*(0) = %.8f" % (c1_0, c2_0, c3_0, B_0))

Bstar_closed = 224.0/593.0
print("\n★ 判别 ①：B*(−5) 失调第四点")
d1B = (1.0/B_0 - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
print("  B*(0) = %.8f vs 闭式 %.8f——失调（1/B 域）%+.5f%%（B 域 %+.5f%%）"
      % (B_0, Bstar_closed, d1B, (B_0-Bstar_closed)/Bstar_closed*100))
print("  失调四点：m=−2: −0.0169%%，m=−3: −0.0210%%，m=−4: −0.0204%%，m=−5: %+.5f%%" % d1B)
print("  δ(1/B) 绝对值四点：−0.0001987、−0.0003494、−0.0004382、%+.8f" % (1.0/B_0-1.0/Bstar_closed))

print("\n★ 判别 ②：c1 五点（几何衰减趋极限）")
c1s = [0.305988839, 0.280239903, 0.270538229, 0.265594666, c1_0]
d1c1 = [c1s[i+1]-c1s[i] for i in range(4)]
print("  c1：%s" % ["%.8f" % v for v in c1s])
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c1])
print("  增量比（前/后）：%s（105 预测第 4 增量 ~0.0025——减半？）"
      % ["%.3f" % (abs(d1c1[i])/abs(d1c1[i+1])) for i in range(3)])
# 几何极限更新
r = abs(d1c1[3]/d1c1[2])
lim = c1s[-1] - d1c1[3]*(r/(1-r)) if r < 1 else None
print("  新公比 r = %.4f、更新极限 c1(∞) ≈ %.6f" % (r, lim) if lim else "  公比 ≥1——极限未收敛")

print("\n★ 判别 ③：c2 五点（线性 κ/63）")
c2s = [0.044906645, 0.073071272, 0.103320868, 0.133962811, c2_0]
d1c2 = [c2s[i+1]-c2s[i] for i in range(4)]
print("  c2：%s" % ["%.8f" % v for v in c2s])
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c2])
print("  增量 vs κ/63 = 0.0303152：%s" % ["%+.3f%%" % (v/0.0303152*100-100) for v in d1c2])

print("\n★ 判别 ④：c3 五点（二阶差分 1/65 位点 3）")
c3s = [-0.015896, -0.042538365, -0.085289609, -0.142764543, c3_0]
d1c3 = [c3s[i+1]-c3s[i] for i in range(4)]
d2c3 = [d1c3[i+1]-d1c3[i] for i in range(3)]
print("  c3：%s" % ["%.8f" % v for v in c3s])
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c3])
print("  二阶差分：%s" % ["%+.8f" % v for v in d2c3])
print("  二阶差分 vs 1/65 = 0.0153846：%s" % ["%+.3f%%" % (abs(v)/0.0153846*100-100) for v in d2c3])

print("\n★ 判别 ⑤：A_5（D_5 = 1，主结构 2⁰−1 = 0）")
A5 = c1_0 * (8-2*5+1)**2
print("  A_5 = %.9f——主结构 2^(5−5)−1 = 0——A_5 ≠ 0（断裂终态）" % A5)
print("  A 全序列：m=1: 14.9933、2: 7.0060、3: 2.4348、4: 0.2656、5: %.6f" % A5)

json.dump({"Bstar_closed": Bstar_closed, "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0,
           "A5": A5, "delta_1B_pct": d1B, "delta_1B_abs": 1.0/B_0-1.0/Bstar_closed,
           "data": data},
          open(os.path.join(BASE, "_phase102_p7_5e106_m5_merged.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
