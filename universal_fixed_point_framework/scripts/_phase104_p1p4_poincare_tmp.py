# -*- coding: utf-8 -*-
"""
Phase 104az-22 (26.16j-70): 相位切片 = Poincare 球 8 等分单元 -- 缺口位置编码偏振通道
几何: 8 等分 = 立方体顶点 8 方向 (s1,s2,s3) = (+-1,+-1,+-1)/sqrt(3) -- 每单元立体角 4pi/8
物理: 8 单元等权混合 = 非偏振 (I=1, Q=U=V=0); 缺口 = 1 单元被转移 -> 残余 7 单元 -> 净 Stokes 失衡
关键: 缺口位置(球面方向) 决定失衡通道:
  - 极点方向 (s3=+-1/sqrt3 主导? 或纯极点 (0,0,+-1)) -> 圆偏振 V 失衡 (P4)
  - 赤道方向 (s3=0) -> 线偏振 Q/U 失衡 (P1)
  - 一般方向 -> 椭圆(混合)失衡
"""
import math
import itertools

# 立方体顶点 8 方向 (8 等分 Poincare 球)
dirs = []
for s1, s2, s3 in itertools.product([-1, 1], repeat=3):
    n = math.sqrt(3)
    dirs.append((s1/n, s2/n, s3/n))

# 纯极点/赤道特殊方向 (对照)
pol_n  = (0, 0, 1)   # sigma+ 纯圆偏振
pol_s  = (0, 0, -1)  # sigma-
eq_0   = (1, 0, 0)   # 线偏振 0 度
eq_45  = (0, 1, 0)   # 线偏振 45 度

print("=" * 78)
print("Poincare 球 8 等分(立方体顶点) -- 缺口单元 -> 残余 7 单元净失衡")
print("=" * 78)
for d in dirs:
    s1, s2, s3 = d
    # 每单元 Stokes 权重 = 方向向量 (球面均匀 8 等分时 I 权重相等, 归一化 1/8)
    # 缺 1 单元 -> 净失衡 = -(方向)/8 (相对完整 8 单元)
    Q, U, V = -s1/8, -s2/8, -s3/8
    # 归一化到残余强度 7/8
    Qn, Un, Vn = Q/(7/8), U/(7/8), V/(7/8)
    # 通道分类
    pol = math.sqrt(Qn**2 + Un**2 + Vn**2)
    chan = "V(圆偏振/P4)" if abs(Vn) > 0.8*pol and pol > 1e-9 else \
           "Q/U(线偏振/P1)" if abs(Vn) < 0.2*pol and pol > 1e-9 else "混合(椭圆)"
    print("  缺 {}: Q/I={:+.1f}% U/I={:+.1f}% V/I={:+.1f}% | 通道={}".format(
        tuple(round(x, 3) for x in d), Qn*100, Un*100, Vn*100, chan))

print()
print("对照: 纯极点/赤道缺口 (特殊几何)")
for name, d in [("sigma+(上极点)", pol_n), ("sigma-(下极点)", pol_s), ("线偏振 0 度", eq_0), ("线偏振 45 度", eq_45)]:
    s1, s2, s3 = d
    Q, U, V = -s1/8, -s2/8, -s3/8
    Qn, Un, Vn = Q/(7/8), U/(7/8), V/(7/8)
    pol = math.sqrt(Qn**2 + Un**2 + Vn**2)
    chan = "V(圆偏振/P4)" if abs(Vn) > 0.8*pol and pol > 1e-9 else \
           "Q/U(线偏振/P1)" if abs(Vn) < 0.2*pol and pol > 1e-9 else "混合(椭圆)"
    print("  缺 {}: Q/I={:+.1f}% U/I={:+.1f}% V/I={:+.1f}% | 通道={}".format(name, Qn*100, Un*100, Vn*100, chan))

print()
print("=" * 78)
print("核心结论")
print("=" * 78)
print("1. 缺口位置(球面方向) 编码偏振通道: 极点->纯 V(P4), 赤道->纯 Q/U(P1), 一般->椭圆(混合)")
print("2. 立方体 8 等分缺口: 全为混合(椭圆)通道 (|V|~|Q/U|~sqrt(3) 分量) -- 非纯 P1/P4 单通道")
print("   -> 立方体 8 等分非纯线/圆偏振切分 -- 104t'圆周极化 8 等分'应为赤道偏振角等分(线偏振)")
print("3. 特殊几何(极点/赤道)缺口: 纯 V 或纯 Q/U -- 104u 情形1/情形2 对应")
print("4. ★ 统一判别: 缺口位置 = P1(线)/P4(圆) 通道开关 -- 观测 Q/U 与 V 的比值确定缺口在球面的位置")
print("   -> 同星 Q/U vs V 比值 = 缺口几何指纹 (新判别预言 P7)")
print("5. 观测: J2346 V=-1.51% (P4 信号) + J135141/J100356 Lp 0.6% (P1 信号) -- 缺口含极向分量+赤道分量")

out = {
    "cube_8fold_missing": [{"dir": list(d), "Q_pct": round(-d[0]/(7/8)*100, 1), "U_pct": round(-d[1]/(7/8)*100, 1), "V_pct": round(-d[2]/(7/8)*100, 1)} for d in dirs],
    "special": {"sigma_plus": {"Q": 0, "U": 0, "V": round(-1/(7/8)*100, 1)}, "eq_0": {"Q": round(-1/(7/8)*100, 1), "U": 0, "V": 0}},
    "conclusions": [
        "缺口位置(Poincare 球方向) 编码偏振通道: 极点->V(P4), 赤道->Q/U(P1)",
        "立方体 8 等分缺口全为椭圆混合 -- 非纯线/圆切分; 纯通道需极点/赤道特殊几何",
        "统一判别 P7: 同星 Q/U vs V 比值 = 缺口几何指纹",
        "观测暗示缺口含极向+赤道分量 (V 与 Lp 均非零)",
    ],
}
import json
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase104_p1p4_poincare_tmp.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print()
print("已存盘: _phase104_p1p4_poincare_tmp.json")
