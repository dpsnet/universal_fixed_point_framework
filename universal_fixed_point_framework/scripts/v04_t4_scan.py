# -*- coding: utf-8 -*-
"""v0.4 搜索对象 2：T4 双有理式商族 —— g_p/2 织法唯一性复扫 + 主结构推广（104az-205）

模板：g(a,b,c,p,q) = (a − p)/(b/(c + q))，a,b,c ∈ 主结构集 M，p,q ∈ 修正集 R
目标：g_p/2 = 2.79284734463，容差 0.1%（与 v0.3 一致）
对照：104az-148 固定主结构 (7,5,2)=(对合域,静默,幂基) 的 10201 组合唯一命中 (8/45,3/64)
"""
from fractions import Fraction
import time

TARGET = 2.79284734463
TOL = 0.001  # 0.1%

K = [2, 3, 4, 5, 7, 8, 16, 25, 49, 64]
D = [45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100]
R = sorted({Fraction(k, d) for k in K for d in D})
print("修正集 |R| = %d" % len(R), flush=True)

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
print("主结构集 |M| = %d" % len(M), flush=True)

def val(a, b, c, p, q):
    denom = c + q
    if denom == 0:
        return None
    d2 = Fraction(b) / denom
    if d2 == 0:
        return None
    return (Fraction(a) - p) / d2

def dev(v):
    return abs(v - TARGET) / TARGET

# ---- 方案 A：固定主结构 (7,5,2)，复扫 10201 组合 ----
t0 = time.time()
hitsA = []
for p in R:
    for q in R:
        v = val(7, 5, 2, p, q)
        if v is not None and dev(float(v)) <= TOL:
            hitsA.append((p, q, float(v)))
print("方案A (7,5,2) 命中数 = %d（唯一性 = %s）" % (len(hitsA), len(hitsA) == 1), flush=True)
for p, q, v in hitsA:
    print("  p=%s q=%s → %.12f (dev %.3e)" % (p, q, v, dev(v)), flush=True)
print("  104az-148 期望唯一命中 (8/45, 3/64): %s" % ("✓" if any(p == Fraction(8, 45) and q == Fraction(3, 64) for p, q, _ in hitsA) else "✗"), flush=True)
print("方案A 耗时 %.1fs" % (time.time() - t0), flush=True)

# ---- 方案 B：主结构推广 a,b,c ∈ M（12³ × 101² ≈ 1760 万组合）----
print("\n方案B 主结构推广扫描开始…", flush=True)
t0 = time.time()
hitsB = []
Rf = [(p, float(p)) for p in R]
for a in M:
    for b in M:
        for c in M:
            bf = float(b)
            for p, pf in Rf:
                for q, qf in Rf:
                    denom = float(c) + qf
                    if abs(denom) < 1e-15:
                        continue
                    d2 = bf / denom
                    if abs(d2) < 1e-15:
                        continue
                    vf = (float(a) - pf) / d2
                    if abs(vf - TARGET) / TARGET <= TOL:
                        hitsB.append((a, b, c, p, q, vf))
print("方案B 命中数 = %d（主结构数 = %d）" % (len(hitsB), len(M) ** 3), flush=True)
print("方案B 耗时 %.1fs" % (time.time() - t0), flush=True)

# 命中按 (主结构,p,q) 去重列出（前 40）
from collections import Counter
combos = Counter((a, b, c, p, q) for a, b, c, p, q, _ in hitsB)
print("\n方案B 唯一 (a,b,c,p,q) 组合数 = %d" % len(combos), flush=True)
# 框架身份：p,q 是否为 k/d 且 k∈框架量、d∈修正分母家族（定义即然）
# 命中中是否含 104az-148 的原组合（(7,5,2,8/45,3/64)）
orig = (7, 5, 2, Fraction(8, 45), Fraction(3, 64))
print("104az-148 原组合在方案B中: %s" % ("✓" if orig in combos else "✗"), flush=True)

# 列出所有命中（数量可控才列出）
print("\n--- 方案B 命中明细 ---")
for a, b, c, p, q, v in sorted(hitsB, key=lambda t: dev(t[5]))[:60]:
    print("a=%d b=%d c=%d p=%s q=%s → %.12f dev=%.3e%s" % (
        a, b, c, p, q, v, dev(v), " ★=框架原组合" if (a, b, c, p, q) == orig else ""), flush=True)
if len(hitsB) > 60:
    print("…共 %d 条" % len(hitsB), flush=True)
