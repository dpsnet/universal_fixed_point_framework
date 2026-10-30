# -*- coding: utf-8 -*-
"""104az-211 负控：1124315 邻域"错位=42"基线率
干净数定义：素因子全部 ∈ S = {2,3,5,7,11,13,19,29,89,353}（F15 ∪ 已登记身份素因子），
因子个数（含重）≤ 5。对照 224861 = 7²·13·353、224903 = 7·19²·89（差 42，中间夹素数 224863）。
统计随机窗口内：干净数密度、相邻对差分布、差 42 对夹素数基线率。
"""
import math

S = {2, 3, 5, 7, 11, 13, 19, 29, 89, 353}

def factorize(n):
    fac = []
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            fac.append(d)
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        fac.append(m)
    return fac

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def is_clean(n):
    """素因子全 ∈ S 且因子数（含重）≤5"""
    fac = factorize(n)
    if len(fac) > 5:
        return False
    return all(f in S for f in fac)

for W in [(100000, 200000), (200000, 250000), (200000, 230000)]:
    lo, hi = W
    clean = [n for n in range(lo, hi) if is_clean(n)]
    print("===== 窗口 [%d, %d) =====" % (lo, hi), flush=True)
    print("干净数总数：%d（密度 %.2e/整数）" % (len(clean), len(clean) / (hi - lo)), flush=True)
    # 相邻对差分布（含重因子干净数稀疏，用全列表相邻对）
    from collections import Counter
    diffs = Counter()
    pairs42 = []
    for i in range(1, len(clean)):
        d = clean[i] - clean[i-1]
        diffs[d] += 1
        if d == 42:
            pairs42.append((clean[i-1], clean[i]))
    print("相邻对总数：%d；差分布 top10：%s" % (len(clean)-1, diffs.most_common(10)), flush=True)
    print("差 = 2 的对数：%d；差 = 40：%d；差 = 42：%d" % (diffs.get(2, 0), diffs.get(40, 0), diffs.get(42, 0)), flush=True)
    # 差 42 对中夹素数
    n42prime = sum(1 for a, b in pairs42 if any(is_prime(m) for m in range(a+1, b)))
    print("差 42 对中夹素数：%d / %d（基线率 %.4f）" % (n42prime, len(pairs42), n42prime / max(1, len(pairs42))), flush=True)
    # 我们关心的具体实例是否在内
    print("224861 ∈ clean：%s；224903 ∈ clean：%s；224861/224903 差 42 对：%s" % (
        is_clean(224861), is_clean(224903), (224861, 224903) in [(a, b) for a, b in zip(clean, clean[1:])]), flush=True)
    print("224863 素数：%s（夹在 224861/224903 之间：%s）" % (is_prime(224863), 224861 < 224863 < 224903), flush=True)
    print("", flush=True)

print("===== 对照：随机素数的'两侧干净数差'基线 =====", flush=True)
# 随机抽取 ~2000 个素数（伪随机种子固定），统计每个素数 p 两侧 ±100 内
# 是否同时存在两个干净数且该两干净数差 = 42（且 p 夹中间）
import random
random.seed(42)
hits = 0
total = 0
lo, hi = 200000, 250000
cset = set(clean)  # 复用最后窗口
primes_pool = [n for n in range(lo, hi) if is_prime(n)]
random.shuffle(primes_pool)
for p in primes_pool[:2000]:
    # p 两侧的干净数：p-100..p+100
    left = [n for n in range(p-100, p) if n in cset]
    right = [n for n in range(p+1, p+101) if n in cset]
    # 找一对 (a<b) 夹住 p 且差 42
    found = False
    for a in left:
        if a + 42 in right:
            found = True
            break
    total += 1
    if found:
        hits += 1
print("随机素数两侧 ±100 内出现'差 42 干净数对夹素数'：%d / %d（基线率 %.5f）" % (hits, total, hits / total), flush=True)
print("对照：224863 是'差 42 干净数对（224861,224903）夹素数'实例。", flush=True)
