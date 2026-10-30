# -*- coding: utf-8 -*-
"""family_sq_search_156.py — 平方±1 家族系统搜索：n 取框架乘积，n²±1 = m×(框架量)
目标：找 (n²+1)/m 或 (n²−1)/m 精确命中框架已知量 → 第 4 成员判别"""
import io, sys, math
from itertools import combinations_with_replacement
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 框架基础常数（种子集合）
seeds = [2, 3, 5, 7, 4, 8, 16]
# 框架已知量（精确整数，作为目标命中集合）
known = set([37, 41, 43, 49, 53, 56, 57, 65, 91, 131, 205, 210, 231, 240,
             293, 307, 320, 353, 371, 675, 727, 1763, 1765, 2048, 2430,
             40217, 1836, 1764, 882, 42, 45, 1024, 1025, 901, 3137, 577,
             44101, 44099, 899, 783, 575, 255, 11026, 4901, 78401, 12545,
             28225, 39, 2000, 56, 44, 61, 63, 71, 73, 127, 128, 129, 307,
             720, 640, 5*353, 5*307, 5*371, 45*7, 45*8, 7*53, 45*16,
             320*7, 675*2, 210*2, 42*42])
known.add(40217)  # g_p/2 分子
# n 的候选：种子乘积（含重复、去重），≤ 500
def gen_n(limit=500):
    vals = set(seeds)
    # 两两/三三乘积（允许重复因子）
    prod2 = set(a*b for a in seeds for b in seeds if a*b <= limit)
    prod3 = set(a*b*c for a in seeds for b in seeds for c in seeds if a*b*c <= limit)
    vals |= prod2 | prod3
    # 含 45、42、210、320 等复合
    for x in [45, 42, 210, 320, 675, 240, 231, 1836]:
        if x <= limit: vals.add(x)
    return sorted(vals)

ns = gen_n()
print(f"n 候选数: {len(ns)}")

def factors(x):
    f = []
    d = 2
    while d*d <= x:
        while x % d == 0:
            f.append(d); x //= d
        d += 1 if d == 2 else 2
    if x > 1: f.append(x)
    return f

hits_int = []
hits_near = []
for n in ns:
    for sgn, v in [(1, n*n+1), (-1, n*n-1)]:
        # 精确：v / m = known 量，m 为框架常数（≤100，含静默类）
        for m in [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 21, 24, 25, 28, 30, 35, 40, 42, 45, 48, 49, 56, 60, 64, 70, 80, 84, 90, 96, 100, 105, 112, 120, 128, 140, 150, 160, 168, 175, 180, 192, 200, 210, 224, 225, 240, 256, 280, 300, 320, 336, 350, 360, 384, 400, 420, 448, 450, 480, 504, 512, 560, 600, 640, 672, 700, 720, 768, 800, 840, 896, 900, 960, 1000]:
            if v % m == 0:
                q = v // m
                if q in known and q != n:
                    hits_int.append((n, sgn, v, m, q, factors(n), factors(q)))
        # 近似：v/m ≈ known（0.01%）
        for k in sorted(known):
            for m in [1, 2, 3, 4, 5, 7, 8, 16, 21, 24, 25, 42, 45, 48, 56, 64, 96, 100, 128, 210, 240, 320, 675]:
                if m == 0: continue
                r = v / m / k - 1
                if abs(r) < 1e-4:
                    hits_near.append((n, sgn, v, m, k, r))

print(f"\n=== 精确命中（v/m = 框架已知量）===")
seen = set()
for h in hits_int:
    n, sgn, v, m, q, fn, fq = h
    key = (n, sgn, m, q)
    if key in seen: continue
    seen.add(key)
    tag = "+" if sgn > 0 else "−"
    print(f"  n={n:4d}  n²{tag}1 = {v:8d} = {m}×{q:6d}   n因子={fn}  q因子={fq}")

print(f"\n=== 近似命中（0.01% 内）===")
seen2 = set()
for h in hits_near[:40]:
    n, sgn, v, m, k, r = h
    key = (n, sgn, m, k)
    if key in seen2: continue
    seen2.add(key)
    tag = "+" if sgn > 0 else "−"
    print(f"  n={n:4d}  n²{tag}1/{m:4d} = {v/m:12.4f} vs {k:8d}  dev {r*100:+.4f}%")

# 重点复核：42²+1 = 1765 = 5×353（已知）；210²±1；56²±1；32²±1；24²±1；30²±1
print("\n=== 重点家族成员复核 ===")
for n in [6, 8, 24, 28, 30, 32, 42, 56, 105, 210, 280]:
    print(f"  n={n:4d}: n²+1 = {n*n+1:8d}（因子 {factors(n*n+1)}）、n²−1 = {n*n-1:8d} = {factors(n*n-1)}")
