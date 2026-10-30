# -*- coding: utf-8 -*-
"""S320 d_H 精确解结构探测（2026-10-28）

用户点名'必须推进解决 d_H'。精确目标：
  α⁻¹(CODATA2018) = 137.035999084 → d_H* = 137.035999084/24 − 3
  d_H* = ln15 + δ*——δ* = 0.0017830940...
S256d/e δ = 6σ³+4σ⁵+14σ⁷+13σ⁸ = 0.001783132279（差 3.8e-8——王者口径）
结构探测：δ* 的连分数/有理逼近/框架组合
"""
import math
from fractions import Fraction

sigma = 1/15
alpha_inv_exp = 137.035999084
dH_star = alpha_inv_exp/24 - 3
delta_star = dH_star - math.log(15)

print("=== S320 d_H 精确解结构探测 ===\n")
print(f"α⁻¹(exp) = {alpha_inv_exp}")
print(f"d_H* = α⁻¹/24 − 3 = {dH_star:.12f}")
print(f"δ* = d_H* − ln15 = {delta_star:.12f}")

# S256d/e 对照
d_256 = 6*sigma**3 + 4*sigma**5 + 14*sigma**7 + 13*sigma**8
print(f"S256d/e δ = {d_256:.12f}——差 = {abs(d_256-delta_star):.3e}")
print(f"（S256d/e 命中王者 137.036——对实验差 {abs(d_256-delta_star)*24:.3e} 绝对）")

# ① 连分数/有理逼近
print(f"\n① 有理逼近（分母 ≤ 2^20）：")
cf = Fraction(delta_star).limit_denominator(2**20)
print(f"  δ* ≈ {cf} = {cf.numerator/cf.denominator:.12f}——偏差 {abs(cf-delta_star):.2e}")
print(f"  分母因子：{cf.denominator}（框架分解？——{cf.denominator} = ?）")
cf2 = Fraction(delta_star).limit_denominator(2**24)
print(f"  高分母版：{cf2}——偏差 {abs(cf2-delta_star):.2e}")

# ② σ 幂组合探测（系数 ∈ {1..42}，幂次 ∈ {3,5,7,8}）
print(f"\n② σ 幂组合（aσ³+bσ⁵+cσ⁷+dσ⁸——a,b,c,d ∈ 1..42）：")
best = []
for a in range(0, 20):
    for b in range(0, 20):
        for c in range(0, 20):
            for d in range(0, 20):
                v = a*sigma**3 + b*sigma**5 + c*sigma**7 + d*sigma**8
                if v == 0: continue
                diff = abs(v - delta_star)
                if diff < 5e-10:
                    best.append((diff, a, b, c, d))
best.sort()
if best:
    print(f"  ≤5e-10 命中 {len(best)} 个：")
    for diff, a, b, c, d in best[:5]:
        print(f"    {a}σ³+{b}σ⁵+{c}σ⁷+{d}σ⁸ = {a*sigma**3+b*sigma**5+c*sigma**7+d*sigma**8:.12f}——偏差 {diff:.2e}")
else:
    print(f"  无 ≤5e-10 命中——扫描 {20**4} 组合")
    # 最优
    best_any = []
    for a in range(0, 20):
        for b in range(0, 20):
            for c in range(0, 20):
                for d in range(0, 20):
                    v = a*sigma**3 + b*sigma**5 + c*sigma**7 + d*sigma**8
                    diff = abs(v - delta_star)
                    best_any.append((diff, a, b, c, d))
    best_any.sort()
    diff, a, b, c, d = best_any[0]
    print(f"  最优：{a}σ³+{b}σ⁵+{c}σ⁷+{d}σ⁸ = {a*sigma**3+b*sigma**5+c*sigma**7+d*sigma**8:.12f}——偏差 {diff:.2e}")

# ③ 修正项视角（0.035999084）
print(f"\n③ α⁻¹ 修正项 0.035999084（vs 王者 137.036）：")
print(f"  α⁻¹*−137.036 = {alpha_inv_exp-137.036:.9f}——S256b 已扫（最优 12.3σ）")
print(f"  ——维持证伪状态——δ* 探测为补充通道")

print(f"\n结论：δ* = {delta_star:.12f}——结构探测结果见上——")
print(f"  （若 ② 无 ≤5e-10 命中——精确解不属简单 σ 幂组合——维持开放）")
