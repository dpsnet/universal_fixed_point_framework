# -*- coding: utf-8 -*-
"""S256d 验证：δ = 90σ⁴+4σ⁵+14σ⁷？
90 = 活跃²×幂基×静默、4 = 不动点、14 = 态域−1（B−1——Moran 分支加权）
δ_α = 16259/6000 − ln15 = 0.00178313223...
高精度验证 + α⁻¹σ_score
"""
import math
from decimal import Decimal, getcontext
getcontext().prec = 50

ln15_d = Decimal(15).ln()
dH_d = Decimal(16259)/Decimal(6000)
delta_d = dH_d - ln15_d
print("=== S256d: δ 候选精确验证 ===")
print(f"δ_α 目标 = {delta_d}")
print(f"δ_α 数值 = {float(delta_d):.12f}")

sigma = 1/15
# 精确分数表达：σ⁴ = 1/15⁴、σ⁵ = 1/15⁵、σ⁷ = 1/15⁷
s4 = Decimal(1)/(Decimal(15)**4)
s5 = Decimal(1)/(Decimal(15)**5)
s7 = Decimal(1)/(Decimal(15)**7)
delta_pred = 90*s4 + 4*s5 + 14*s7
print(f"90σ⁴+4σ⁵+14σ⁷ = {delta_pred}")
print(f"偏差 δ_pred−δ_α = {delta_pred - delta_d}")
diff = abs(delta_pred - delta_d)
print(f"|偏差| = {diff}")
alpha_diff = float(diff)*24
sig_score = alpha_diff/2.1e-8
print(f"α⁻¹ 层面偏差 = {alpha_diff:.3e}")
print(f"σ_score = {sig_score:.3f}（≤1 达标 / 1-3 提示 / >3 不达标）")

print("\n=== 分数形式 ===")
# 90/50625 + 4/759375 + 14/170859375
# 通分：50625 = 15⁴、759375 = 15⁵、170859375 = 15⁷
# 最小公分母 = 15⁷
num = 90*15**3 + 4*15**2 + 14
den = 15**7
print(f"δ_pred = {num}/{den} = {num}/{den}")
print(f"  {num} = ?（候选框架分解）")
print(f"  90×3375 = 303750、4×225 = 900、+14 = {num}")

print("\n=== 框架身份 ===")
print("90 = 活跃²×幂基×静默 = 3²×2×5 ✓")
print("4 = 不动点 ✓")
print("14 = 态域−1 = B−1（Moran 分支加权——δ 响应公式分母 29=2B−1 同源）✓")
print("σ 幂 = 框架常数幂 ✓")

print("\n=== 交叉验证：d_H 预测 ===")
dH_pred = ln15_d + delta_pred
print(f"d_H 预测 = ln15+δ = {dH_pred}")
print(f"d_H 目标 = 16259/6000 = {dH_d}")
print(f"|差| = {abs(dH_pred-dH_d)}")

print("\n=== α⁻¹ 预测 ===")
alpha_pred = 24*(dH_pred + 3)
alpha_target = Decimal("137.035999084")
unc = Decimal("2.1e-8")
print(f"α⁻¹ 预测 = {alpha_pred}")
print(f"α⁻¹ 实验 = {alpha_target}")
sig = abs(alpha_pred - alpha_target)/unc
print(f"σ_score = {sig:.3f}")
