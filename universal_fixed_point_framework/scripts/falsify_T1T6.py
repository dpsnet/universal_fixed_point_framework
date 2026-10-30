# -*- coding: utf-8 -*-
# falsify_T1T6.py — L14 公理化定理 T1–T6 数值真值检验（模式 8：先证伪再证明）
from fractions import Fraction
import math

print("=== T1: S(8) = 231 ===")
S = lambda k: (Fraction(k,2)-1)*(Fraction(k)-1)*(Fraction(3*k,2)-1)
print("S(8) =", S(8), "== 231:", S(8) == 231)

print("\n=== T2: gcd(231, 232) = 1 ===")
print("gcd =", math.gcd(231, 232))

print("\n=== T3: 400·(232/231) = (2·k_max·静默²)·(1+1/231) ===")
kmax, silence = 8, 5
LHS = Fraction(400) * Fraction(232, 231)
RHS = Fraction(2*kmax*silence**2) * Fraction(1) + Fraction(2*kmax*silence**2)/231
print("LHS =", LHS, "RHS =", RHS, "equal:", LHS == RHS)
# 核心恒等：2·k_max·静默² = 400
print("2·k_max·静默² =", 2*kmax*silence**2, "== 400:", 2*kmax*silence**2 == 400)

print("\n=== T4: S(k) k∈{4..12} 无 230/232 命中 ===")
vals = {k: S(k) for k in range(4, 13)}
print("S(4..12) =", {k: str(v) for k, v in vals.items()})
hits = [k for k, v in vals.items() if v in (230, 232)]
print("230/232 命中:", hits, "→ T4 成立:", not hits)

print("\n=== T5: 231 = 3·7·11 唯一分解 ===")
print("231 =", 3*7*11, "| 素因子:", end=" ")
def fac(n):
    r = []
    d = 2
    while d*d <= n:
        while n % d == 0: r.append(d); n //= d
        d += 1
    if n > 1: r.append(n)
    return r
print(fac(231))

print("\n=== T6: {230,231,232} 中唯一 S(k) 命中 = 231 ===")
# 在窗口内：symprodS(k) ∈ {230,231,232} ⟺ = 231
ok = all((v in (230, 231, 232)) == (v == 231) for v in vals.values())
print("窗口内唯一性成立:", ok)
# 显示每个 k 的值是否在窗口
for k, v in vals.items():
    in_win = v in (230, 231, 232)
    print(f"  k={k}: S={v}  in{{230,231,232}}={in_win}")
