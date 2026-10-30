# -*- coding: utf-8 -*-
"""
Phase 104az-98: 隙倒数一循环端点结构
环 3 核心：为何 F_np 用 1/Δλ₃ 而非其他谱量?
1. ★★ 1/Δλ₃ = (N_gen/2)(√6+√2) = (N_gen/2)·√2·(√N_gen+1) —— 隙倒数全框架闭式
2. ★★ F_np 无理数来源定位: √6+√2 全部来自隙倒数（织³×(1−δ) 有理数）
3. ★ 端点发散结构: Δλ→0 → 1/Δλ→∞（临界穿越强度发散端点）
4. ★ 为何 Δλ₃ 而非 Δλ_min: 双谱隙桥参与（对偶穿越）
"""
from decimal import Decimal, getcontext
from fractions import Fraction
getcontext().prec = 50

Ngen = 3
kmax = 8
sqrt2 = Decimal(2).sqrt()
sqrt3 = Decimal(3).sqrt()

print("=" * 70)
print("[1] 1/Δλ₃ 全框架闭式")
dlmin = (sqrt3 - 1)/6
dl3 = sqrt2 * dlmin
inv_dl3 = 1/dl3
print(f"  Δλ_min = (√3−1)/6 = {dlmin}")
print(f"  Δλ₃ = √2·Δλ_min = {dl3}")
print(f"  1/Δλ₃ = {inv_dl3}")
c1 = Decimal(Ngen)/2 * sqrt2 * (sqrt3 + 1)
print(f"  (N_gen/2)·√2·(√3+1) = {c1}")
c2 = Decimal(Ngen)/2 * (Decimal(6).sqrt() + sqrt2)
print(f"  (N_gen/2)(√6+√2) = {c2}")
print(f"  恒等? {abs(inv_dl3-c1) < Decimal('1e-40')} / {abs(inv_dl3-c2) < Decimal('1e-40')}")
print(f"  → 1/Δλ₃ = (N_gen·√2/2)(√3+1) = (N_gen/2)·√2·(√N_gen+1)（全框架闭式）")
print(f"  √6 = √2·√3 = 桥×√N_gen; √2 = 双谱隙桥; N_gen/2 = 生成半")

print("\n[2] F_np 无理数来源定位")
w3 = Fraction(9, 10)**3
corr = Fraction(674, 675)
rat = w3 * corr
print(f"  织³×(1−δ) = {rat} = {float(rat):.10f}（有理数——无 √6+√2）")
print(f"  F_np = 织³×(1−δ)×1/Δλ₃ = 有理数 × 隙倒数")
print(f"  → F_np 的 √6+√2 唯一来源 = 隙倒数 1/Δλ₃")
# 等价形式核对
F1 = Decimal(rat.numerator)/Decimal(rat.denominator) * inv_dl3
F2 = Decimal(27297)/Decimal(25000) * (Decimal(6).sqrt() + sqrt2)
print(f"  F_np = {F1}")
print(f"  (27297/25000)(√6+√2) = {F2}")
print(f"  一致? {abs(F1-F2) < Decimal('1e-40')}")

print("\n[3] 端点发散结构")
print(f"  Δλ→0 时 1/Δλ→∞——临界穿越强度发散端点（禁闭穿越点谱隙趋于零）")
print(f"  F_np 语义: 临界穿越强度 = β临界指数³ × 静默修正 × 穿越前谱隙倒数（发散量）")
print(f"  → '隙倒数一循环端点结构': 谱隙倒数在端点处发散, F_np 含唯一发散量")

print("\n[4] 为何 Δλ₃ 而非 Δλ_min")
inv_min = 1/dlmin
print(f"  1/Δλ_min = {inv_min} = 3(√3+1)（无桥最强发散）")
print(f"  1/Δλ₃ = {inv_dl3}（桥×基——双谱隙对偶参与的穿越）")
print(f"  比值 = {inv_min/inv_dl3} = √2 ✓（自然）")
print(f"  判别: F_np 用 Δλ₃ = 桥×基（对偶穿越——#455 双谱隙对偶的谱量形式）")
print(f"        而非 Δλ_min（纯基谱隙——无桥）——穿越是双谱隙对偶参与的")

print("\n[5] F_np 三形式等价")
print(f"  A: F_np = (27297/25000)(√6+√2)")
print(f"  B: F_np = (27297/37500)·1/Δλ₃")
print(f"  C: F_np = (729/1000)(674/675)·1/Δλ₃（β函数×静默修正×隙倒数——104az-96/97 完整形式）")
print(f"  27297/37500 = 织³×(1−δ) = (729/1000)(674/675) 化简")

print("\n[6] 诚实边界")
print(f"  端点发散语义仍在诠释层（F_np 含唯一发散量 1/Δλ₃——机制候选）")
print(f"  '为何对偶穿越用桥×基' 待 #455 双谱隙对偶严格形式化")
print(f"  1/Δλ₃ 闭式由 Δλ_min 定义直接推出（代数必然, 非独立发现）——登记为闭式化")
