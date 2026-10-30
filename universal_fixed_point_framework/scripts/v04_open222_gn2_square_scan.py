# -*- coding: utf-8 -*-
# 104az-222 平方型模板族 (a^2-b)/(c^2-d) 对 g_n/2 的负控扫描（pyenv 3.11.8）
# 动机：g_n/2 44/23 = (7^2-5)/(5^2-2)，参数 (7,5,2) = T4 主结构 (对合域,静默,幂基) 同源
# 判据：绝对差口径（104az-201 登记 σ_obs=4.5e-7 为绝对不确定度）
# 目标：|g_n/2| = 1.91304273；同族对 g_p/2 (40217/14400) 跨参数对照
import numpy as np
from fractions import Fraction
from collections import Counter

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]  # M12 框架量
BD = sorted(set(M + [1]))  # 修正集：框架量 + 1

gn2 = 1.91304273
gp2 = 40217/14400  # 2.7928472222
sig_obs = 4.5e-7  # 绝对口径（104az-201）
thresh = 3 * sig_obs

def scan(target):
    hits = []
    for a in M:
        for c in M:
            num = a*a
            den = c*c
            for b in BD:
                for d in BD:
                    n2, d2 = num - b, den - d
                    if n2 <= 0 or d2 <= 0:
                        continue
                    val = n2/d2
                    if abs(val - target) <= thresh:
                        hits.append((a, b, c, d, n2, d2, val, val-target))
    return hits

print("=== 平方型族 (a^2-b)/(c^2-d)：a,c∈M12，b,d∈M12∪{1} ===")
print("族规模 =", len(M)**2 * len(BD)**2)
print()
print("--- g_n/2 目标 |g_n/2|=1.91304273，|dev|≤3σ=1.35e-6 ---")
hits_g = scan(gn2)
print("命中数 =", len(hits_g))
for h in sorted(hits_g, key=lambda x: abs(x[7]))[:20]:
    a, b, c, d, n2, d2, val, diff = h
    print(f"  ({a}^2-{b})/({c}^2-{d}) = {n2}/{d2} = {val:.10f}  dev {diff:+.2e}")
fracs = Counter(Fraction(n2, d2) for _, _, _, _, n2, d2, _, _ in hits_g)
print("最简分数种类 =", len(fracs), "| 44/23 在其中？", Fraction(44,23) in fracs)

print()
print("--- g_p/2 跨参数对照 40217/14400=2.7928472，|dev|≤3σ ---")
hits_p = scan(gp2)
print("命中数 =", len(hits_p))
for h in sorted(hits_p, key=lambda x: abs(x[7]))[:10]:
    a, b, c, d, n2, d2, val, diff = h
    print(f"  ({a}^2-{b})/({c}^2-{d}) = {n2}/{d2} = {val:.10f}  dev {diff:+.2e}")

print()
print("--- decoy 负控（10 个同域随机目标，1.5~2.5）---")
rng = np.random.default_rng(222)
decoys = rng.uniform(1.5, 2.5, 10)
for i, t in enumerate(decoys):
    h = scan(float(t))
    print(f"  decoy {i}: target {t:.6f} → 命中 {len(h)}")

print()
print("--- 44/23 在族内等价表示数 ---")
eq44 = [(a,b,c,d,n2,d2) for a,b,c,d,n2,d2,val,diff in hits_g if Fraction(n2,d2)==Fraction(44,23)]
print("44/23 的族内组合数 =", len(eq44))
for a,b,c,d,n2,d2 in eq44[:10]:
    print(f"  ({a}^2-{b})/({c}^2-{d})")
