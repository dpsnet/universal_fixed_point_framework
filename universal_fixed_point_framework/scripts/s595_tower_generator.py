# -*- coding: utf-8 -*-
"""
S595 奇数塔生成集机制判别（候选级——开放项③'为何 {1,3,5,7} 是生成集'）
机制候选：塔 = 8 以内正奇数（幂次域 [1,k_max] 的奇半空间）
  · k_max = 8 = 2×4 = 幂基 × Clifford 活跃基（12_σ = 16−4 同源的 4）
  · 塔大小 4 = 活跃基计数
  · 塔对和 1+7 = 3+5 = 8 = k_max（对称中心 S59-S61）
  结构一致性验证（候选级——非新数值预测）
"""
import numpy as np

sigma = 1/15  # 框架常数

def check(name, cond):
    if not cond:
        raise AssertionError(f"FAIL: {name}")
    print(f"PASS: {name}")

# 1) 8 以内正奇数 = {1,3,5,7}
odds = [k for k in range(1, 9) if k % 2 == 1]
check("odds_lt_9 = {1,3,5,7}", odds == [1, 3, 5, 7])

# 2) 塔对和 = k_max：1+7 = 3+5 = 8
pairs = [(1, 7), (3, 5)]
for a, b in pairs:
    check(f"tower_pair_sum_{a}+{b}=8", a + b == 8)

# 3) 塔大小 = 4 = Clifford 活跃基（12_σ = 16−4 同源的 4）
active_base = 4  # S576：12_σ = 16−4——Clifford 活跃基计数
check("tower_size = active_base = 4", len(odds) == active_base)

# 4) k_max = 8 = 2×4 = 幂基 × 活跃基
kmax = 8
power_base = 2  # S202 幂基 2（递归尺度）
check("kmax = power_base * active_base = 2*4", kmax == power_base * active_base)

# 5) 幂次域 [1,8] 内偶数 {2,4,6,8}：2 = 幂基非塔；4,6 偶幂禁
#    （规范形——S583）；8 = k_max 终点（S268 终止层——非禁）
evens_in_domain = [k for k in range(1, 9) if k % 2 == 0]
check("evens_in_domain = {2,4,6,8}", evens_in_domain == [2, 4, 6, 8])

# 5b) 偶幂禁/缺 = {4,6}（8 = k_max 终点豁免——S268 已锚终止层）
forbidden_evens = [k for k in evens_in_domain if k != 2 and k != 8]
check("forbidden_evens = {4,6}", forbidden_evens == [4, 6])

# 6) 偶幂禁机制一致：σ^4 = 15σ^5、σ^6 = 15σ^7（S583 规范形平移 1 步）
#    ——4,6 是"禁/缺"（规范形改写为奇幂）——8 = k_max 不改写
#    （S268 终止层已锚——终点豁免）
norm4 = sigma**4 - 15*sigma**5   # 应为 0
norm6 = sigma**6 - 15*sigma**7   # 应为 0
check("normal_form_sigma4_eq_15sig5", abs(norm4) < 1e-15)
check("normal_form_sigma6_eq_15sig7", abs(norm6) < 1e-15)

# 7) 塔对和的对称语义：塔对 (1,7)、(3,5) 关于 kmax/2 = 4 对称
#    （4−3=1、4+3=7；4−1=3、4+1=5）——成对和 = 2×4 = 8 = kmax
center = kmax / 2  # 4.0
check("tower_center = kmax/2 = 4", abs(center - 4.0) < 1e-12)
# 塔内互补配对：1↔7、3↔5——关于 4 对称、对和 = kmax
print(f"INFO: tower pair sums all equal kmax = {kmax}")
print(f"INFO: tower = {odds} (size {len(odds)} = active_base {active_base})")
print(f"INFO: kmax = {kmax} = power_base {power_base} × active_base {active_base}")
print(f"INFO: forbidden evens = {forbidden_evens} (normal-form rewritten)")
print(f"INFO: kmax exempt = 8 (terminal layer, S268 anchored)")

print("ALL PASS")
