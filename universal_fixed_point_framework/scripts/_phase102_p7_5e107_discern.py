# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-107 判别：合并 4 档 Richardson 三阶 + 六点判别 + 失调段 2 分析
================================================================
数据源：
  dr=0.02/0.01/0.005 —— p107_out.txt（107 脚本输出，硬编码）
  dr=0.0025 —— 107b JSON
输出：B*(0)、c1/c2/c3(0)、失调第五点、六点序列判别、失调段 2 增长律
"""
import json, os
import numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

data = {
    0.02:  {"c1": 0.260294276, "c2": 0.196363243, "c3": -0.308363541, "B*": 0.31823357},
    0.01:  {"c1": 0.260301026, "c2": 0.196373657, "c3": -0.308373623, "B*": 0.31822938},
    0.005: {"c1": 0.260302712, "c2": 0.196376471, "c3": -0.308402207, "B*": 0.31822833},
}
j = json.load(open(os.path.join(BASE, "_phase102_p7_5e107_m6_dr0025.json"), encoding="utf-8"))
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
print("P7-5e-107 判别（合并 4 档 Richardson 三阶）")
print("="*104)
print("逐档：")
for d in drs:
    print("  dr=%.4f：c1=%+.9f c2=%+.9f c3=%+.9f B*=%+.8f" % (d, data[d]["c1"], data[d]["c2"], data[d]["c3"], data[d]["B*"]))
print("\n★ Richardson 三阶外推 dr→0：")
print("  c1(0) = %.9f、c2(0) = %.9f、c3(0) = %.9f、B*(0) = %.8f" % (c1_0, c2_0, c3_0, B_0))

Bstar_closed = 1.0 / (3.0 + 1.0/7.0 + 1.0/448.0)
d1B = (1.0/B_0 - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
print("\n★ 判别 ①：B*(−6) 失调第五点（三阶外推）")
print("  B*(0) = %.8f vs 闭式 %.8f——失调（1/B 域）%+.5f%%" % (B_0, Bstar_closed, d1B))
print("  失调五点：m=-2 +0.0167pct、m=-3 +0.0210pct、m=-4 +0.0204pct、m=-5 -0.0512pct、m=-6 %+.5fpct" % d1B)
print("  失调绝对值：0.0204、0.0512、%.5f——段 2 比值 m=−6/m=−5 = %.3f" % (abs(d1B), abs(d1B)/0.0512))

print("\n★ 判别 ②：c1 六点（亚几何衰减确认）")
c1s = [0.305988839, 0.280239903, 0.270538229, 0.265594666, 0.262495944, c1_0]
d1c1 = [c1s[i+1]-c1s[i] for i in range(5)]
print("  c1：%s" % ["%.8f" % v for v in c1s])
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c1])
print("  增量比（前/后）：%s" % ["%.3f" % (abs(d1c1[i])/abs(d1c1[i+1])) for i in range(4)])
print("  ★ 判别：增量比 {2.65, 1.96, 1.60, ?}——若 <1.6 则亚几何衰减确认")

print("\n★ 判别 ③：c2 六点（超线性确认）")
c2s = [0.044906645, 0.073071272, 0.103320868, 0.133962811, 0.164995332, c2_0]
d1c2 = [c2s[i+1]-c2s[i] for i in range(5)]
print("  c2：%s" % ["%.8f" % v for v in c2s])
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c2])
print("  增量 vs κ/63 = 0.0303152：%s" % ["%+.3f%%" % (v/0.0303152*100-100) for v in d1c2])
print("  增量二次差：%s" % ["%+.6f" % (d1c2[i+1]-d1c2[i]) for i in range(4)])

print("\n★ 判别 ④：c3 六点（1/65 位点 3 存疑维持）")
c3s = [-0.015896, -0.042538365, -0.085289609, -0.142764543, -0.217422024, c3_0]
d1c3 = [c3s[i+1]-c3s[i] for i in range(5)]
d2c3 = [d1c3[i+1]-d1c3[i] for i in range(4)]
print("  c3：%s" % ["%.8f" % v for v in c3s])
print("  一阶差分：%s" % ["%+.8f" % v for v in d1c3])
print("  二阶差分：%s" % ["%+.8f" % v for v in d2c3])
print("  二阶差分 vs 1/65 = 0.0153846：%s" % ["%+.3f%%" % (abs(v)/0.0153846*100-100) for v in d2c3])

print("\n★ 判别 ⑤：A_6（D_6 = (9−12)² = 9——回升！）")
D6 = (8-2*6+1)**2
A6 = c1_0 * D6
print("  D_6 = %d、A_6 = %.6f——A 序列：m=1: 14.993、2: 7.006、3: 2.435、4: 0.266、5: 0.262、6: %.4f" % (D6, A6, A6))
print("  ★ D_m 序列 {49,25,9,1,1,9}——m=6 处 D 回升（(9−2m)² 的 U 形底部在 m=4.5）——A_6 回升判别")

json.dump({"Bstar_closed": Bstar_closed, "c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0,
           "A6": A6, "D6": D6, "delta_1B_pct": d1B, "data": data},
          open(os.path.join(BASE, "_phase102_p7_5e107_m6_merged.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 ✓  exit 0")
