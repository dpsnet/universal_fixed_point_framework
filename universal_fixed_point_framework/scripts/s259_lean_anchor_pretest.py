# -*- coding: utf-8 -*-
"""S259 Lean 锚化前数值先证伪（模式 8 血泪条款）
目标定理（将锚入 SilenceSecondOrder.lean）：
  T1: 6σ³+4σ⁵+8σ⁷+5σ⁸ = 4569875/2562890625（σ = 1/15）
  T2: α⁻¹ 结构 = 72 + 24ln15 + 24·δ_V3（定义性重写——无需验证数值）
  T3: 15⁸ = 2562890625（分母锚）
随机扰动检验：参数扰动后残差非零 → 定理非恒假
"""
from fractions import Fraction
import random

sigma = Fraction(1, 15)

def delta_v3(s=sigma):
    return 6*s**3 + 4*s**5 + 8*s**7 + 5*s**8

target = Fraction(4569875, 2562890625)

print("=== S259 数值先证伪 ===")
print(f"T1: δ_V3 = {delta_v3()} = {float(delta_v3()):.15f}")
print(f"    target = {target} = {float(target):.15f}")
print(f"    残差 = {delta_v3() - target}——{'0（通过）' if delta_v3()==target else '非零（失败）'}")

print(f"\nT3: 15⁸ = {15**8} = {2562890625}——{'✓' if 15**8==2562890625 else '✗'}")
print(f"    15⁵ = {15**5}（分母 σ⁵ 项）——15³ = {15**3}")

# 随机扰动检验（确认定理非恒假——扰动后残差非零）
print("\n扰动检验（确认 T1 非恒假）：")
random.seed(42)
nonzeros = 0
for i in range(6):
    c = [random.randint(1, 30) for _ in range(4)]
    p = [random.randint(1, 12) for _ in range(4)]
    val = sum(Fraction(c[j]) * sigma**p[j] for j in range(4))
    res = val - target
    if res != 0:
        nonzeros += 1
    print(f"  样本{i+1}: 系数{c} 幂次{p} → 残差 {float(res):.2e}——{'非零 ✓' if res!=0 else '零（异常）'}")
print(f"非零率：{nonzeros}/6——{'✓ 定理有区分度' if nonzeros==6 else '✗ 注意'}")

# 精确小数对照（记录到 out）
print(f"\nα⁻¹_V3 = 72 + 24·ln15 + 24·δ_V3（数值）:")
import decimal
from decimal import Decimal, getcontext
getcontext().prec = 30
ln15 = Decimal(15).ln()
d_v3 = Decimal(6)/Decimal(15)**3 + Decimal(4)/Decimal(15)**5 + Decimal(8)/Decimal(15)**7 + Decimal(5)/Decimal(15)**8
alpha_inv = Decimal(72) + Decimal(24)*ln15 + Decimal(24)*d_v3
print(f"  δ_V3 = {d_v3}")
print(f"  α⁻¹_V3 = {alpha_inv}")
print(f"  α⁻¹_CODATA2018 = 137.035999084（偏差 {alpha_inv - Decimal('137.035999084')}）")
