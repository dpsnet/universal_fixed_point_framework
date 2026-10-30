# -*- coding: utf-8 -*-
"""σ^n 双负幂耦合验证（2026-10-26 修正版）

核心规律：σ^n = N_gen^{−n}×静默^{−n}（σ 非独立幂——每次 σ^n 同时消耗
N_gen^{−n}）——修正量幂和 = −2n + 系数幂和
验证：σ、6σ³、静默⁻²、Δ_dress 的精确幂次分解
"""
import math

powers, ngen, silence = 2, 3, 5
sigma = 1/15

def calc(a, b, c, d):
    """静默^a × N_gen^b × k_max^c × 幂基^d（负幂倒数）"""
    return (silence**a if a>=0 else silence**(-a)**-1) * \
           (ngen**b if b>=0 else ngen**(-b)**-1) * \
           (2**c if c>=0 else 2**(-c)**-1) * \
           (powers**d if d>=0 else powers**(-d)**-1)

print("=== σ^n 双负幂耦合 ===")
for n in (1, 2, 3):
    lhs = sigma**n
    rhs = 1/(ngen**n * silence**n)
    print(f"σ^{n} = {lhs:.10f} = N_gen^{{−{n}}}×静默^{{−{n}}} = 1/({ngen**n}×{silence**n}) = {rhs:.10f}——恒等: {abs(lhs-rhs)<1e-12}")
print()

print("=== 修正量精确幂次分解 ===")
items = [
    # (名称, 幂次(a_静默,b_Ngen,c_kmax,d_幂基), 期望值, 幂和)
    ("σ",                (-1, -1, 0, 0), 1/15, -2),
    ("静默⁻² = 1/25",    (-2, 0, 0, 0), 1/25, -2),
    ("Δ_dress = 2σ/3",   (-1, -2, 0, 1), 2*sigma/3, -2),
    ("6σ³ = 2/1125",     (-3, -2, 0, 1), 6*sigma**3, -4),
]
for name, (a, b, c, d), expect, psum in items:
    v = calc(a, b, c, d)
    ok = abs(v - expect) < 1e-12
    print(f"{name:<20} 幂次(a,b,c,d)=({a},{b},{c},{d}) 幂和={a+b+d} 计算={v:.10f} vs {expect:.10f}——一致: {ok}")
print()

print("=== 幂和规律 ===")
print("σ^n 幂和 = −2n（σ^n = N_gen^{−n}静默^{−n}——双负幂耦合）")
print("修正量幂和 = −2n + 系数幂和：")
print("  σ（n=1、系数 1 幂和 0）：−2+0 = −2")
print("  静默⁻²（直接静默幂——n 语义 = 静默幂 2）：−2")
print("  Δ_dress（n=1、系数 2/3 = 幂基×N_gen⁻¹ 幂和 +1−1 = 0）：−2")
print("  6σ³（n=3、系数 6 = N_gen×幂基 幂和 +2）：−6+2 = −4")
print()
print("核心机制线索：**σ 不是独立幂——σ^n 同时消耗 N_gen^{−n}×静默^{−n}**")
print("——静默冻结的'代-静默耦合'：每次冻结消耗活跃代与静默同比例")
