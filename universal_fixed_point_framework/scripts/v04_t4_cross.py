# -*- coding: utf-8 -*-
"""v0.4 搜索对象 3：T4 双有理式商模板跨参数复用检验（104az-207）

模板：(A−p)/(B/(C+q))，A,B,C ∈ M（12 框架量）、p,q ∈ R（101 个 k/d，全框架身份）
目标集：g_p/2（已确立，验证）、g_n/2、1/α、21/100（精确恒等对照）
判据：P1 σ_dev 分档（≤0.5σ / ≤1σ / ≤3σ / ≤5σ）
判定：σ 判据下唯一命中 + 参数全框架身份 → 模板跨参数系统性证据
"""
from fractions import Fraction
import time

K = [2, 3, 4, 5, 7, 8, 16, 25, 49, 64]
D = [45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100]
R = sorted({Fraction(k, d) for k in K for d in D})
M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]

# 目标：(名称, 值, σ_obs, 来源)
TARGETS = [
    ("g_p/2", 2.79284734463, 8.2e-8, "CODATA 2018 μ_p/μ_N"),
    ("g_n/2", -1.91304273, 4.5e-7, "CODATA 2018 μ_n/μ_N"),
    ("1/α", 137.035999084, 2.1e-8, "CODATA 2018 α⁻¹"),
    ("21/100", 0.21, 0.0, "框架精确恒等（对照）"),
]

def val(a, b, c, p, q):
    denom = c + q
    if denom == 0:
        return None
    d2 = Fraction(b) / denom
    if d2 == 0:
        return None
    return (Fraction(a) - p) / d2

print("|R|=%d, |M|=%d, 组合数=%d" % (len(R), len(M), len(M)**3 * len(R)**2), flush=True)

# 预扫描网格（一次遍历全部组合，各目标共享）——值域检查
Rf = [(p, float(p)) for p in R]
for name, T, S, src in TARGETS:
    t0 = time.time()
    hits = []  # (a,b,c,p,q,val,sigma)
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
                        if S == 0.0:
                            sd = 0.0 if vf == T else float("inf")
                        else:
                            sd = abs(vf - T) / S
                        if sd <= 5.0:
                            hits.append((a, b, c, p, q, vf, sd))
    print("\n===== %s = %s（σ_obs=%.2e）=====" % (name, T, S), flush=True)
    print("≤0.5σ: %d  ≤1σ: %d  ≤3σ: %d  ≤5σ: %d（%.1fs）" % (
        sum(1 for h in hits if h[6] <= 0.5),
        sum(1 for h in hits if h[6] <= 1.0),
        sum(1 for h in hits if h[6] <= 3.0),
        len(hits), time.time()-t0), flush=True)
    for a, b, c, p, q, v, sd in sorted(hits, key=lambda t: t[6])[:25]:
        print("  A=%d B=%d C=%d p=%s q=%s → %.12f  σ_dev=%.3f%s" % (
            a, b, c, p, q, v, sd, " ★全框架身份" if True else ""), flush=True)
    if len(hits) > 25:
        print("  …共 %d 条" % len(hits), flush=True)
    if not hits:
        print("  （σ≤5 无命中）", flush=True)
