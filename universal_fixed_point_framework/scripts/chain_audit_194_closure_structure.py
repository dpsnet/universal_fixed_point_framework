# -*- coding: utf-8 -*-
"""chain_audit_194_closure_structure.py — 104az-194：为何 1+11 的结构刻画

假设（待验证）：
A. 无单位 3 元闭包 (a,b,c) ⟺
   A1 元素素因子 ⊆ {2,3,5,7}（纯框架素基）
   A2 全和 a+b+c ≤ 15（→ 全部子集和 ≤ 15 ≤ 16 ∈ FW_SUM 自动）
   A3 全积 abc ∈ FW 且两两积 ab/ac/bc ∈ FW
B. "为何 11"：FW 表 49 值中可互异 ≥2 因子三元分解且满足 A2/A3 的分解数 = 11
C. 4 元闭包 = {1} ∪ 无单位 3 元闭包（全提升自动：无单位 3 元闭包的积谱已含两两积、和谱已含两两和；a≤15 → 1+a ∈ FW_SUM 自动）
"""
import io, sys, itertools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FW = {
    1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 6, 10, 11, 12, 13, 14,
    20, 21, 28, 29, 30, 31, 32, 35, 40, 42, 44, 45, 46, 48, 49,
    56, 58, 60, 61, 63, 64, 65, 84, 98, 100, 105, 125, 210, 253,
    320, 675, 729, 1000,
}
FW_SUM = {v for v in FW if v <= 64} | {105, 125, 210, 253, 320, 675, 729}
PRIMES = {2, 3, 5, 7}

def prime_factors(n):
    fs = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d)
            n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs

def is_closed3(s):  # 3 元子集闭包（无单位判定用）
    ss, pp = [], []
    for r in range(1, 4):
        for c in itertools.combinations(s, r):
            ss.append(sum(c)); pr = 1
            for x in c: pr *= x
            pp.append(pr)
    return all(v in FW_SUM for v in ss) and all(v in FW for v in pp)

print("=== A. [2,16] 三约束逐步淘汰（455 候选）===")
pool = list(itertools.combinations(range(2, 17), 3))
n1 = sum(1 for s in pool if all(prime_factors(x) <= PRIMES for x in s))
n2 = sum(1 for s in pool if all(prime_factors(x) <= PRIMES for x in s) and sum(s) <= 15)
n3 = sum(1 for s in pool if all(prime_factors(x) <= PRIMES for x in s) and sum(s) <= 15
         and (s[0]*s[1]*s[2] in FW) and all(a*b in FW for a, b in itertools.combinations(s, 2)))
n4 = sum(1 for s in pool if is_closed3(s))
print(f"候选 455 → 素基 {n1} → +和≤15 {n2} → +积∈FW {n3}；真闭包 = {n4}")
print(f"假设 A 一致性：n3 == n4 → {n3 == n4}")
if n3 != n4:
    hyp = {s for s in pool if all(prime_factors(x) <= PRIMES for x in s) and sum(s) <= 15
           and (s[0]*s[1]*s[2] in FW) and all(a*b in FW for a, b in itertools.combinations(s, 2))}
    true = {s for s in pool if is_closed3(s)}
    print(f"误报（假设∈但非闭包）：{sorted(hyp - true)}")
    print(f"漏报（闭包但假设∉）：{sorted(true - hyp)}")

print("\n=== B. 互异三元分解计数（FW 值 → 分解 → 约束）===")
decomp = {}
for v in sorted(FW):
    if v < 6: continue
    ds = []
    for a in range(2, 17):
        for b in range(a + 1, 17):
            for c in range(b + 1, 17):
                if a * b * c == v:
                    ds.append((a, b, c))
    if ds:
        good = [d for d in ds if sum(d) <= 15 and all(x*y in FW for x, y in itertools.combinations(d, 2))]
        bad = [d for d in ds if d not in good]
        tag = "✓全部" if len(good) == len(ds) else (f"仅 {good}" if good else "✗全淘汰")
        print(f"  {v}: 分解 {ds} → {tag}")
        if bad: print(f"      淘汰原因: {[ (d, sum(d), [x*y for x,y in itertools.combinations(d,2)]) for d in bad ]}")
print(f"\nFW 中可分解值总数（无约束） vs 全命中分解数：")
total_good = 0
for v in sorted(FW):
    if v < 6: continue
    ds = [(a,b,c) for a in range(2,17) for b in range(a+1,17) for c in range(b+1,17) if a*b*c == v]
    good = [d for d in ds if sum(d) <= 15 and all(x*y in FW for x,y in itertools.combinations(d,2))]
    total_good += len(good)
print(f"总合格分解数 = {total_good}（应 = 11）")

print("\n=== C. [2,24] 无单位 3 元闭包（值域完备性验证）===")
pool24 = list(itertools.combinations(range(2, 25), 3))
c24 = [s for s in pool24 if is_closed3(s)]
print(f"[2,24] 候选 {len(pool24)} → 闭包 {len(c24)} 个：{c24}")
print(f"与 [2,16] 相同？ {sorted(c24) == sorted([s for s in pool if is_closed3(s)])}")

print("\n=== D. 4 元闭包 = 1 ∪ 无单位 3 元闭包（提升自动性验证）===")
uni = [s for s in pool if is_closed3(s)]
four = []
for s in itertools.combinations(range(1, 17), 4):
    ss, pp = [], []
    for r in range(1, 5):
        for c in itertools.combinations(s, r):
            ss.append(sum(c)); pr = 1
            for x in c: pr *= x
            pp.append(pr)
    if all(v in FW_SUM for v in ss) and all(v in FW for v in pp):
        four.append(s)
lift = sorted((1,) + s for s in uni)
print(f"无单位 3 元闭包 {len(uni)} 个；全提升 {len(lift)} 个；真 4 元闭包 {len(four)} 个")
print(f"提升 = 真闭包？ {lift == sorted(four)}")
if lift != sorted(four):
    print(f"  提升但非闭包：{sorted(set(lift) - set(four))}")
    print(f"  闭包但非提升：{sorted(set(four) - set(lift))}")
