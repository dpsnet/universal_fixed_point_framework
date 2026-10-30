# -*- coding: utf-8 -*-
"""S256e 验证：δ = 90σ⁴+4σ⁵+14σ⁷+13σ⁸？
结构假说：δ = Σ C_p·σ^p——幂次 p ∈ {4=不动点, 5=静默, 7=对合, 8=?}
系数：90 = 活跃²×幂基×静默、4 = 不动点、14 = 态域−1、13 = 静默×幂基+活跃
"""
from decimal import Decimal, getcontext
getcontext().prec = 60

ln15 = Decimal(15).ln()
dH_target = Decimal(16259)/Decimal(6000)
delta_target = dH_target - ln15
print("=== S256e: δ = 90σ⁴+4σ⁵+14σ⁷+13σ⁸ 精确验证 ===")
print(f"δ_α 目标 = {delta_target}")

s4 = Decimal(1)/Decimal(15)**4
s5 = Decimal(1)/Decimal(15)**5
s7 = Decimal(1)/Decimal(15)**7
s8 = Decimal(1)/Decimal(15)**8

cands = {
    "90σ⁴+4σ⁵+14σ⁷": 90*s4+4*s5+14*s7,
    "90σ⁴+4σ⁵+14σ⁷+13σ⁸": 90*s4+4*s5+14*s7+13*s8,
    "90σ⁴+4σ⁵+14σ⁷+12σ⁸": 90*s4+4*s5+14*s7+12*s8,
    "90σ⁴+4σ⁵+14σ⁷+13.05σ⁸": 90*s4+4*s5+14*s7+Decimal("13.05")*s8,
    "90σ⁴+4σ⁵+14σ⁷+13σ⁸−1σ⁹": 90*s4+4*s5+14*s7+13*s8 - Decimal(1)/Decimal(15)**9,
    "90σ⁴+4σ⁵+14σ⁷+13σ⁸+1σ⁹": 90*s4+4*s5+14*s7+13*s8 + Decimal(1)/Decimal(15)**9,
}
for name, v in cands.items():
    diff = v - delta_target
    d = abs(diff)
    alpha_sig = float(d)*24/2.1e-8
    print(f"\n{name} = {v}")
    print(f"  偏差 = {diff}")
    print(f"  α⁻¹σ_score = {alpha_sig:.3f}（{'达标' if alpha_sig<=1 else '提示' if alpha_sig<=3 else '不达标'}）")

print("\n=== 精确分数 ===")
num4 = 90*15**4 + 4*15**3 + 14*15 + 13  # 90σ⁴+4σ⁵+14σ⁷+13σ⁸ 通分 15⁸
den = 15**8
print(f"90σ⁴+4σ⁵+14σ⁷+13σ⁸ = {num4}/{den}")
print(f"分子分解：90×15⁴ = {90*15**4}、4×15³ = {4*15**3}、14×15 = {14*15}、+13")
print(f"15⁴ = 50625、15³ = 3375、15 = 15")
