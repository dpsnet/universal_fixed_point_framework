# -*- coding: utf-8 -*-
"""对照检验：π 连分数部分商框架化 vs 随机无理数（2026-10-26）

关键证伪：π 前 60 项 ≥3 部分商 100% 落框架素因子集 {2,3,5,7,11,13}
——这是真信号还是事后识别？对照随机无理数。
"""
import mpmath as mp
import random, math
mp.mp.dps = 80

FW_PRIMES = {2, 3, 5, 7, 11, 13}

def cf_parts(x, n):
    parts = []
    for _ in range(n):
        a = int(x)
        parts.append(a)
        x = 1 / (x - a)
    return parts

def prime_factors(n):
    facs = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            facs.add(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        facs.add(n)
    return facs

def fw_hit_ratio(parts):
    """≥3 的部分商中素因子⊆FW集的比例"""
    nontriv = [a for a in parts if a >= 3]
    hits = [a for a in nontriv if prime_factors(a) <= FW_PRIMES]
    return len(hits), len(nontriv), (len(hits)/len(nontriv) if nontriv else 0)

print("=== 对照：π vs 已知常数 vs 随机无理数（前 60 项）===")
tests = {
    "π": mp.pi,
    "e": mp.e,
    "√2": mp.sqrt(2),
    "√3": mp.sqrt(3),
    "黄金比φ": (1+mp.sqrt(5))/2,
    "ln2": mp.log(2),
    "ζ(3)": mp.zeta(3),
    "√5": mp.sqrt(5),
    "√7": mp.sqrt(7),
    "√11": mp.sqrt(11),
    "√13": mp.sqrt(13),
    "√15": mp.sqrt(15),
    "√17": mp.sqrt(17),
    "√19": mp.sqrt(19),
}
for name, val in tests.items():
    parts = cf_parts(val, 60)
    h, t, r = fw_hit_ratio(parts)
    nontriv_list = [a for a in parts if a >= 3]
    print(f"{name:>6}: {h}/{t} = {r*100:.0f}%  非平凡部分商: {nontriv_list[:12]}")

print("\n=== 随机无理数（5 个种子，各 60 项）===")
for seed in [1, 42, 123, 777, 2026]:
    random.seed(seed)
    # 生成随机无理数：随机小数 + 无理扰动
    r = random.random() + 1.0
    val = mp.mpf(str(r)) + mp.mpf(str(random.random())) * mp.mpf("1e-30")
    parts = cf_parts(val, 60)
    h, t, ratio = fw_hit_ratio(parts)
    print(f"seed {seed}: {h}/{t} = {ratio*100:.0f}%")

print("\n=== π 的非平凡部分商 vs 框架素因子集 ===")
parts_pi = cf_parts(mp.pi, 60)
h, t, r = fw_hit_ratio(parts_pi)
nontriv = [a for a in parts_pi if a >= 3]
print(f"π: {h}/{t} = {r*100:.0f}%  非平凡部分商: {nontriv}")
