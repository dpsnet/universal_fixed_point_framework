# -*- coding: utf-8 -*-
"""v0.4 搜索对象 4（104az-208）：g_n/2 候选 44/23 的模板族判别 + 身份核验

① 身份核验：枚举 44、23 在框架量集 M 内全部 (a*b ± c) 分解 → 判定 104az-157 身份表述
② T5 线性商族（预注册）：V = (a*b + c)/(d*e + f)，a..f ∈ M（12 框架量，12⁶≈300 万组合）
   目标：g_n/2（主判别）、g_p/2（选择性对照）、21/100（精确多解对照）
   判据：P1 σ_dev 分档（≤0.5/1/3/5σ）
"""
from fractions import Fraction
import time

def _fmt(n, d):
    f = Fraction(n, d)
    return "%d/%d" % (f.numerator, f.denominator)

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
MS = set(M)

TARGETS = [
    ("|g_n/2|", 1.91304273, 4.5e-7, "CODATA 2018 μ_n/μ_N 绝对值（观测 −1.91304273，候选 44/23 正对绝对值）"),
    ("g_p/2", 2.79284734463, 8.2e-8, "CODATA 2018 μ_p/μ_N（T4 已锁，对照；注意 T5 分子上限 11130 < 40217，预期值域不覆盖）"),
    ("21/100", 0.21, 0.0, "框架精确恒等（精确多解对照）"),
]

# ---- ① 身份核验：44、23 的全部 (a*b ± c) 分解（a,b,c ∈ M）----
print("===== ① 44 / 23 框架量分解核验（a*b ± c，a,b,c ∈ M）=====", flush=True)
for N in (44, 23):
    decomps = []
    for a in M:
        for b in M:
            p = a * b
            for c in M:
                for sign, name in ((1, "+"), (-1, "-")):
                    if p + sign * c == N:
                        decomps.append((a, b, name, c))
    print("N=%d：共 %d 个分解" % (N, len(decomps)), flush=True)
    for d in decomps:
        print("  %d = %d×%d %s %d" % (N, d[0], d[1], d[2], d[3]), flush=True)
    print("  104az-157 表述核验：", flush=True)
    if N == 44:
        ok1 = any(d[0] == 7 and d[1] == 8 and d[2] == "+" and d[3] == 4 for d in decomps)
        print("    '44 = 静默×k_max + 不动点'（7×8+4=60）：%s" % ("成立" if ok1 else "✗ 不成立（7×8+4=60）"), flush=True)
    if N == 23:
        ok1 = any(d[0] == 7 and d[1] == 4 and d[2] == "+" and d[3] == 3 for d in decomps)
        print("    '23 = 静默×不动点 + N_gen'（7×4+3=31）：%s" % ("成立" if ok1 else "✗ 不成立（7×4+3=31）"), flush=True)

# ---- ② T5 线性商族全扫 ----
print("\n===== ② T5 线性商族 (a*b+c)/(d*e+f)，a..f ∈ M（%d 组合）=====" % (len(M)**6), flush=True)
Rf = [(m, float(m)) for m in M]
for name, T, S, src in TARGETS:
    t0 = time.time()
    hits = []
    for a in M:
        for b in M:
            n1 = a * b
            nf = float(n1)
            for c in M:
                num = n1 + c
                if num <= 0:
                    continue
                for d in M:
                    for e in M:
                        m1 = d * e
                        mf = float(m1)
                        for f in M:
                            den = m1 + f
                            if den == 0:
                                continue
                            vf = (nf + c) / (mf + f)
                            if S == 0.0:
                                exact = (num * 100 == 21 * den)  # 精确有理比较
                                sd = 0.0 if exact else float("inf")
                            else:
                                sd = abs(vf - T) / S
                            if sd <= 5.0:
                                hits.append((a, b, c, d, e, f, vf, sd))
    print("\n----- %s = %s（σ_obs=%.1e）-----" % (name, T, S), flush=True)
    print("≤0.5σ: %d  ≤1σ: %d  ≤3σ: %d  ≤5σ: %d（%.1fs）" % (
        sum(1 for h in hits if h[7] <= 0.5),
        sum(1 for h in hits if h[7] <= 1.0),
        sum(1 for h in hits if h[7] <= 3.0),
        len(hits), time.time() - t0), flush=True)
    for a, b, c, d, e, f, v, sd in sorted(hits, key=lambda t: t[7])[:20]:
        print("  (%d×%d+%d)/(%d×%d+%d) = %s → %.12f  σ=%.3f" % (
            a, b, c, d, e, f, _fmt(a*b+c, d*e+f), v, sd), flush=True)
    if len(hits) > 20:
        print("  …共 %d 条" % len(hits), flush=True)
    if not hits:
        print("  （σ≤5 无命中）", flush=True)
