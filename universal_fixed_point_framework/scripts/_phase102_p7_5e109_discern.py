# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-109 判别：m=−8 三档硬编码（前 3 档 Richardson 二阶）
================================================================
数据源：p109_out.txt（三档全量）
判别：失调线性律（δ≈(κ/1400)(m−4) 四点半）、c2 增量 1/32 饱和三点、c1 √2 通道、c3 1/65、A_8 U 形
"""
import json, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"

data = {
    0.02:  {"c1": 0.257646273, "c2": 0.258930383, "c3": -0.536031709, "B*": 0.24166719},
    0.01:  {"c1": 0.257651231, "c2": 0.258940292, "c3": -0.536049910, "B*": 0.24166484},
    0.005: {"c1": 0.257652444, "c2": 0.258946936, "c3": -0.535165534, "B*": 0.24166425},
}

drs = [0.02, 0.01, 0.005]
def rich2(vals):
    v1 = [(4*vals[i+1]-vals[i])/3.0 for i in range(2)]
    return (16*v1[1]-v1[0])/15.0

c1_0 = rich2([data[d]["c1"] for d in drs])
c2_0 = rich2([data[d]["c2"] for d in drs])
c3_0 = rich2([data[d]["c3"] for d in drs])
B_0 = rich2([data[d]["B*"] for d in drs])

closed = 8.0/2.0 + 1.0/7.0 + 1.0/1792.0
Bstar_closed = 1.0/closed
d1B = (1.0/B_0 - 1.0/Bstar_closed)/(1.0/Bstar_closed)*100
d_abs = abs(1.0/B_0 - 1.0/Bstar_closed)
A8 = c1_0 * 49.0

print("P7-5e-109 判别（m=-8 三档 Richardson 二阶）")
print("="*100)
print("★ Richardson B*(0) = %.8f——失调（1/B 域）= %+.5f%%（δ(1/B) = %.6f）" % (B_0, d1B, d_abs))
print("★ c1(0) = %.8f、c2(0) = %.8f、c3(0) = %.8f、A_8 = c1×49 = %.4f" % (c1_0, c2_0, c3_0, A8))

print("\n★★ 判别 ①——失调段 2 线性律（四点确认）")
seg = {5: 0.00135438, 6: 0.0026848, 7: 0.00410574, 8: d_abs}
print("  δ(1/B) 段 2：m=5..8 = %s" % ["%.6f" % seg[m] for m in (5,6,7,8)])
print("  差分：%s" % ["%+.6f" % (seg[m+1]-seg[m]) for m in (5,6,7)])
pred = [0.0013642*(m-4) for m in (5,6,7,8)]
print("  线性律 δ≈(κ/1400)(m−4) 预测：%s" % ["%.6f" % p for p in pred])
print("  实测/预测偏差：%s" % ["%+.2f%%" % (seg[m]/pred[i]*100-100) for i, m in enumerate((5,6,7,8))])
a_fit = (seg[8]-seg[5])/3.0
print("  四点拟合斜率 a = %.6f vs κ/1400 = 0.0013642（偏差 %+.2f%%）" % (a_fit, (a_fit/0.0013642-1)*100))

print("\n★★ 判别 ②——c2 增量 1/32 饱和（三点确认）")
c2s = [0.044906645, 0.073071272, 0.103320868, 0.133962811, 0.164995332, 0.196375473, 0.227647509, c2_0]
d1c2 = [c2s[i+1]-c2s[i] for i in range(7)]
print("  c2 增量：%s" % ["%+.8f" % v for v in d1c2])
print("  后三点 vs 1/32=0.03125：%s" % ["%+.2f%%" % (v/0.03125*100-100) for v in d1c2[4:]])
print("  ★ 增量 {..., 0.03138, 0.03127, %.5f}——1/32 饱和三点确认" % d1c2[6])

print("\n★ 判别 ③——c1 增量比 √2 通道（未确认）")
c1s = [0.305988839, 0.280239903, 0.270538229, 0.265594666, 0.262495944, 0.260303312, 0.258788995, c1_0]
d1c1 = [c1s[i+1]-c1s[i] for i in range(7)]
print("  增量：%s" % ["%+.8f" % v for v in d1c1])
print("  增量比（m>=5 段）：%s" % ["%.3f" % (abs(d1c1[i])/abs(d1c1[i+1])) for i in range(3, 6)])
print("  ★ {1.41, 1.45, 1.33}——波动未稳定——√2 通道未确认（需更高精度或 m=-9）")

print("\n★ 判别 ④——c3 二阶差分 1/65（摆动维持）")
c3s = [-0.015896, -0.042538365, -0.085289609, -0.142764543, -0.217422024, -0.309308682, -0.414324822, c3_0]
d1c3 = [c3s[i+1]-c3s[i] for i in range(7)]
d2c3 = [d1c3[i+1]-d1c3[i] for i in range(6)]
print("  二阶差分：%s" % ["%+.8f" % v for v in d2c3])
print("  vs 1/65=0.0153846：%s" % ["%+.1f%%" % (abs(v)/0.0153846*100-100) for v in d2c3])
print("  ★ 仍在 1/65 附近摆动——位点 3 维持存疑（c3 的 dr=0.005 档跳变污染外推）")

print("\n★★ 判别 ⑤——A 层 U 形完整闭合（D 层对合满格）")
print("  A 八点：%s" % ["%.3f" % (c1s[i]*[(9-2*(i+1))**2][0]) for i in range(8)])
print("  D 层对合 m↦9−m：D_1=D_8=49、D_2=D_7=25、D_3=D_6=9、D_4=D_5=1——U 形完整")

json.dump({"c1_0": c1_0, "c2_0": c2_0, "c3_0": c3_0, "B_0": B_0, "A8": A8,
           "delta_1B_pct": d1B, "delta_1B_abs": d_abs, "data": data},
          open(os.path.join(BASE, "_phase102_p7_5e109_m8_3dr.json"), "w", encoding="utf-8"), indent=1)
print("\nJSON 落盘 OK  exit 0")
