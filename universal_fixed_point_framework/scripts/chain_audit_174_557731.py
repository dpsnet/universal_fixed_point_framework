# -*- coding: utf-8 -*-
"""chain_audit_174_557731.py — 557731 素分解 + 梅森数家族拆解检查"""
import io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def factorize(n):
    facs = []
    d = 2
    while d*d <= n:
        while n % d == 0:
            facs.append(d); n //= d
        d += 1
    if n > 1: facs.append(n)
    return facs

N = 557731
facs = factorize(N)
print(f"=== 1. 557731 素分解 ===")
print(f"557731 = {' × '.join(map(str,facs))}")
prod = 1
for f in facs: prod *= f
print(f"核验：{'✓' if prod == N else '✗'}  (prod={prod})")
print(f"分解为 {len(facs)} 个素因子，{'纯素数' if len(facs)==1 else '合数'}")

print(f"\n=== 2. 梅森数家族对照（框架 Mersenne 谱系 104az-204/205）===")
mers = [(m, 2**m-1) for m in range(1, 25)]
for m, v in mers:
    if v <= N*2:
        mark = "  ←★" if v in facs else ""
        print(f"M_{m} = 2^{m}−1 = {v}{mark}")

print(f"\n=== 3. 557731 vs 相邻梅森数 ===")
M19 = 2**19-1; M20 = 2**20-1
print(f"M_19 = {M19}；N−M_19 = {N-M19}（差 33444）")
print(f"M_20 = {M20}；M_20−N = {M20-N}")
print(f"N 是否本身梅森：2^m−1 = 557731 → m = log2(557732) = {math.log2(557732):.4f} 非整数 → 否")

print(f"\n=== 4. 梅森家族乘积组合检查 ===")
# N 的因子中含梅森素数：3,7,31,127,8191,131071,524287...
Mlist = [v for _, v in mers if v <= N and v in facs]
print(f"N 的素因子中含梅森素数：{Mlist if Mlist else '无'}")
# 用梅森数做除法检查
for m, v in mers:
    if v > 1 and N % v == 0:
        print(f"N 可被 M_{m} = {v} 整除：N = {v} × {N//v} ← ★★★")
print("（若上面无输出则 N 不被任何小梅森数整除）")

print(f"\n=== 5. 557731 = 梅森数 ± 框架量 搜索 ===")
fw = [2,3,4,5,7,8,9,10,16,24,40,42,45,49,56,61,63,64,65,71,125,127,210,231,343,371,405,500,13500]
for m, v in mers:
    for w in fw:
        for op in [1,-1]:
            cand = v + op*w
            if cand == N:
                print(f"★★★ 557731 = M_{m}({v}) {'+' if op==1 else '−'} {w}（{w} 框架量）")
print("（若上面无输出则无梅森数±框架量直接命中）")

print(f"\n=== 6. 相邻框架量差审计 ===")
print(f"N−524287 = {N-524287}（524287 = M_19 梅森素数）")
print(f"N−131071 = {N-131071}（131071 = M_17 梅森素数）")
print(f"N−65535 = {N-65535}（65535 = M_16）")
print(f"N−262143 = {N-262143}（262143 = M_18）")
