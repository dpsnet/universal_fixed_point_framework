# -*- coding: utf-8 -*-
"""chain_audit_183_quartic.py — 深度分界的互反律解析判别
四次互反律（Ireland–Rosen）：p ≡ 1 mod 8 且 2 是四次剩余 ⟺ p = a²+64b²（a 奇）。
八次剩余：2 是八次剩余 ⟺ p ≡ 1 mod 16 且 p = a²+128b²。
十六次/更深：p = a²+256b²（试探）。
对照观测：2^((p−1)/4)、2^((p−1)/8)、2^((p−1)/16) mod p。
"""
import io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def find_rep(p, coef):
    """找 p = a² + coef·b²，返回 (a, b) 或 None；a 取正根"""
    bmax = int(math.isqrt(p // coef))
    for b in range(0, bmax + 1):
        r = p - coef * b * b
        a = math.isqrt(r)
        if a * a == r:
            return (a, b)
    return None

Ks = [1, 3, 7, 9, 11, 13]
print("=== 互反律解析判别（深度 2/3/4 分界）===")
print(f"{'k':>3} {'p':>10} {'d2':>3} {'2^((p−1)/4)':>12} {'2^((p−1)/8)':>12} {'2^((p−1)/16)':>13} | {'a²+64b²':>16} {'a²+128b²':>18} {'a²+256b²':>18}")
d2_map = {1: 0, 3: 2, 7: 3, 9: 4, 11: 3, 13: 4}
for k in Ks:
    p = 49 + 4**k
    r4 = pow(2, (p - 1) // 4, p)
    r8 = pow(2, (p - 1) // 8, p) if (p - 1) % 8 == 0 else None
    r16 = pow(2, (p - 1) // 16, p) if (p - 1) % 16 == 0 else None
    r64 = find_rep(p, 64)
    r128 = find_rep(p, 128)
    r256 = find_rep(p, 256)
    s64 = "无" if r64 is None else f"{r64[0]}²+64×{r64[1]}²"
    s128 = "无" if r128 is None else f"{r128[0]}²+128×{r128[1]}²"
    s256 = "无" if r256 is None else f"{r256[0]}²+256×{r256[1]}²"
    s8 = "—" if r8 is None else str(r8)
    s16 = "—" if r16 is None else str(r16)
    print(f"{k:>3} {p:>10} {d2_map[k]:>3} {r4:>12} {s8:>12} {s16:>13} | {s64:>16} {s128:>18} {s256:>18}")

print("\n=== 判别对照 ===")
print("四次剩余（d2≥2）：p = a²+64b² 存在（k=3,7,9,11,13 应全有；k=1 无）")
print("八次剩余（d2≥3）：p = a²+128b² 存在（k≥7 应有；k=3 应无）")
print("十六次/更深（d2=4）：p = a²+256b² 存在（k=9,13 应有；k=7,11 应无）")
