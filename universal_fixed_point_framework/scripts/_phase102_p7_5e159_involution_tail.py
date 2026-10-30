# -*- coding: utf-8 -*-
"""
P7-5e-159：2^m 尾巴机制判别——对合域 × 2^m 尾巴的代数连接
判别目标：
A) 对合域 m↦9−m 与 2^m 尾巴的精确关系（尾巴镜像比 = 2^{9−2m} = 2^{√D_m}？）
B) 9−2m 的奇数序列结构（±1,±3,±5,±7——k_max−1 内奇数）
C) δ_cl 在 m 与 9−m 处的对称性（对合是否延伸到残差层）
D) 域界 m=9 = 2³+1 与尾巴收敛点 m≥10 = k_max+2 的界结构
"""
import json, math

# 权威数据：tridiag 小 m δ_cl（155b 修正后）+ 全链（129）
dcl = {1: 2.013e-4, 2: 2.013e-4, 3: 3.544e-4, 4: 4.419e-4, 5: 1.358e-3,
       6: 2.692e-3, 7: 4.055e-3, 8: 5.428e-3, 9: 6.626e-3, 10: 7.656e-3,
       11: 8.540e-3, 12: 9.298e-3, 13: 9.950e-3, 14: 1.051e-2}
# 注：m=2 的 δ_cl 用 tridiag 收敛值（155b tri−spec 修正前 spec −5.84e-2 是窗口伪影）

print("=== P7-5e-159 对合域 × 2^m 尾巴判别 ===", flush=True)
print("\n--- A) 尾巴镜像比 ---", flush=True)
print("m\t9−m\t尾巴比 2^{9−2m}\t√D_m\t2^{√D_m}")
for m in range(1, 9):
    r = 9 - m
    ratio = 2.0**(9 - 2*m)
    sqrtD = 9 - 2*m
    print("%d\t%d\t%.0f\t%d\t%.0f" % (m, r, ratio, sqrtD, 2.0**sqrtD), flush=True)
print("尾巴镜像比 = 2^{9−2m} = 2^{√D_m}——代数恒等（对合 D_m 平方结构 = 2 进指数平方）", flush=True)

print("\n--- B) 9−2m 奇数序列 ---", flush=True)
odds = [9-2*m for m in range(1, 9)]
print("m=1..8 的 9−2m：", odds, flush=True)
print("= {±1, ±3, ±5, ±7}——k_max−1=7 内奇数集（2 步差——二进制 2 进步长）", flush=True)
print("D_m = 奇数平方：", [o*o for o in odds], flush=True)

print("\n--- C) δ_cl 对合对称性检验 ---", flush=True)
print("m\tδ_cl(m)\tδ_cl(9−m)\t比值", flush=True)
for m in range(1, 5):
    r = 9 - m
    print("%d\t%.3e\t%.3e\t%.2f" % (m, dcl[m], dcl[r], dcl[m]/dcl[r]), flush=True)
print("δ_cl 单调递增——对合对称在 D_m 层成立、δ_cl 层不成立（对合不延伸到残差层）", flush=True)

print("\n--- D) 域界与收敛点 ---", flush=True)
print("对合域 [1,8] 界 = 9 = 2³+1 = k_max+1（153 家族成员）", flush=True)
print("尾巴收敛点 m≥10 = k_max+2 = n_max（157）", flush=True)
print("域界 m=9 本身 = 对合常数——域界自指（D_9 = 81 = 9² 超对合）", flush=True)

print("\n--- E) 奇数轴 × 2^m 尾巴组合判别 ---", flush=True)
# 检查 9−2m 与 2^m 尾巴指数 m 的关系：奇数轴差 2 = 尾巴公比 1/2 的指数步
print("奇数轴步长 2 ↔ 尾巴公比 1/2（指数步 2 ↔ 幂步 2）", flush=True)
print("判别结论：对合域 = k_max−1 内奇数平方集；尾巴 = 同一 2 进结构的指数投影——", flush=True)
print("'为何 2^m'候选：m 轴由 2 进代数组织（补数对合 2³+1−m + 1/2 公比尾巴）", flush=True)
print("诚实边界：代数恒等非独立机制——对合 D_m 平方 = 2 进指数的平方是重写；", flush=True)
print("但'域界=家族成员'与'δ_cl 不对称'是限制性事实（对合深度受限于 D_m 层）", flush=True)

with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e159_involution_tail.json", "w", encoding="utf-8") as f:
    json.dump({"mirror_ratio_formula": "2^(9-2m)=2^sqrt(D_m)", "odds": odds,
               "dcl_symmetry": {str(m): [dcl[m], dcl[9-m]] for m in range(1,5)},
               "domain_bound": 9, "convergence": 10}, f, indent=1)
print("saved", flush=True)
