# -*- coding: utf-8 -*-
"""v0.4-1 机制闭合：R 的 n≡0 mod 30 子集 vs 框架组合 S（mod 30 效应判别）"""
import random, bisect

LIMIT = 10 ** 6

def sieve(n):
    bs = bytearray([1]) * (n + 1)
    bs[0] = bs[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if bs[i]:
            bs[i * i:n + 1:i] = bytearray(len(range(i * i, n + 1, i)))
    return [i for i in range(n + 1) if bs[i]]

primes = sieve(LIMIT + 100)

def nearest_prime_dist(x):
    i = bisect.bisect_left(primes, x)
    best = float('inf')
    if i < len(primes): best = primes[i] - x
    if i > 0: best = min(best, x - primes[i - 1])
    return best

PEXT = [2, 3, 5, 7, 11, 13, 29]
cand = []
for p in PEXT:
    v = 1
    for e in range(1, 4):
        v *= p
        cand.append((p, v))

S2 = set()
def rec2(idx, prod, cnt):
    if cnt > 5: return
    if prod > LIMIT: return
    if cnt >= 1: S2.add(prod)
    for i in range(idx, len(cand)):
        if prod * cand[i][1] > LIMIT: continue
        rec2(i, prod * cand[i][1], cnt + 1)
rec2(0, 1, 0)
S = [x for x in S2 if 10 ** 5 <= x <= 3 * 10 ** 5]

random.seed(104203)
R_all = [random.randint(10 ** 5, 3 * 10 ** 5) for _ in range(60000)]

def stats(nums, label):
    if not nums: 
        print("%s: 空" % label, flush=True)
        return
    ds = [nearest_prime_dist(x) for x in nums]
    n = len(ds)
    r1 = sum(1 for d in ds if d <= 1) / n
    r2 = sum(1 for d in ds if d <= 2) / n
    print("%s: n=%d d<=1率=%.4f d<=2率=%.4f" % (label, n, r1, r2), flush=True)

stats(S, "S 框架组合（1e5~3e5）")
stats([x for x in R_all if x % 30 == 0], "R 含2·3·5（mod30=0）")
stats([x for x in R_all if x % 6 == 0], "R 含2·3（mod6=0）")
stats([x for x in R_all if x % 2 == 0], "R 偶数")
stats(R_all, "R 全随机")

# S 中 mod30=0 占比
f30 = sum(1 for x in S if x % 30 == 0) / len(S)
print("S 中 n≡0 mod 30 占比 = %.3f" % f30, flush=True)
