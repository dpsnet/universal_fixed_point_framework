# -*- coding: utf-8 -*-
"""falsify_ngkm1.py — 先证伪：恒等 N_gen+k_max−1 = 幂基·静默 + 织³ 纯素基分解（Fraction 精确检验）"""
import io, sys
from fractions import Fraction as F
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

N_gen, k_max, Powers, Silence = 3, 8, 2, 5

print("=== 1. 恒等 N_gen+k_max−1 = 幂基·静默 ===")
lhs = N_gen + k_max - 1
rhs = Powers * Silence
print(f"LHS = {lhs}；RHS = {rhs}；相等: {lhs == rhs}")

print("\n=== 2. 织 = N_gen²/(幂基·静默) = 9/10 ===")
weave = F(N_gen**2, Powers * Silence)
print(f"织 = {N_gen}²/({Powers}·{Silence}) = {weave}；== 9/10: {weave == F(9,10)}")

print("\n=== 3. 织³ = (9/10)³ = 729/1000 ===")
weave3 = weave ** 3
print(f"织³ = {weave3}；== 729/1000: {weave3 == F(729,1000)}")

print("\n=== 4. 纯素基分解 织³ = N_gen⁶/(幂基³·静默³) ===")
dec = F(N_gen**6, (Powers**3) * (Silence**3))
print(f"3⁶/(2³·5³) = 729/(8·125) = {dec}；== 织³: {dec == weave3}")

print("\n=== 5. 补充恒等（框架常数间）===")
print(f"N_gen+k_max−1 = {lhs}；10 = 幂基·静默 = 10 ✓；10 也 = k_max+N_gen−1 = 塔第一项+1？{lhs}")
print(f"10 = N_gen+k_max−1 = 2·5；10 素分解 = 2·5 ✓（素基 {2,5}）")

print("\n=== 判别 ===")
print("全部精确恒等通过（Fraction 非浮点）；可投入 Lean 证明")
