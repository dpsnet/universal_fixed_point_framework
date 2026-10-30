# -*- coding: utf-8 -*-
"""v0.4 搜索对象 2 补判：σ_dev 判据重判（104az-206）

T4 模板 (A-p)/(B/(C+q))，目标 g_p/2 = 2.79284734463
P1 判据：σ_dev = |dev_abs| / σ_obs，σ_obs = 8.2e-8（CODATA 2018 μ_p/μ_N）
分档：≤0.5σ / ≤1σ / ≤3σ / ≤5σ（P1 四档）
对照：0.1% 容差（≈28000σ）口径的宽松命中数
"""
from fractions import Fraction
import time

TARGET = 2.79284734463
SIGMA_OBS = 8.2e-8  # CODATA 2018 μ_p/μ_N 不确定度

K = [2, 3, 4, 5, 7, 8, 16, 25, 49, 64]
D = [45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100]
R = sorted({Fraction(k, d) for k in K for d in D})
M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]

def val(a, b, c, p, q):
    denom = c + q
    if denom == 0:
        return None
    d2 = Fraction(b) / denom
    if d2 == 0:
        return None
    return (Fraction(a) - p) / d2

def sigma_dev(v):
    return abs(v - TARGET) / SIGMA_OBS

# ---- 方案 A：固定主结构 (7,5,2) ----
hitsA = []
for p in R:
    for q in R:
        v = val(7, 5, 2, p, q)
        if v is not None:
            sd = sigma_dev(float(v))
            if sd <= 5.0:
                hitsA.append((p, q, float(v), sd))
print("===== 方案 A（固定主结构 (7,5,2)）=====", flush=True)
print("≤0.5σ: %d  ≤1σ: %d  ≤3σ: %d  ≤5σ: %d" % (
    sum(1 for _,_,_,s in hitsA if s <= 0.5),
    sum(1 for _,_,_,s in hitsA if s <= 1.0),
    sum(1 for _,_,_,s in hitsA if s <= 3.0),
    len(hitsA)), flush=True)
for p, q, v, sd in sorted(hitsA, key=lambda t: t[3])[:20]:
    print("  p=%s q=%s → %.12f  σ_dev=%.3f（abs dev %.3e）" % (p, q, v, sd, abs(v-TARGET)), flush=True)

# ---- 方案 B：主结构推广 ----
print("\n===== 方案 B（主结构推广 12³×101²）=====", flush=True)
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
                    sd = abs(vf - TARGET) / SIGMA_OBS
                    if sd <= 5.0:
                        hitsB.append((a, b, c, p, q, vf, sd))
print("≤0.5σ: %d  ≤1σ: %d  ≤3σ: %d  ≤5σ: %d（扫描 %d 组合，%.1fs）" % (
    sum(1 for h in hitsB if h[6] <= 0.5),
    sum(1 for h in hitsB if h[6] <= 1.0),
    sum(1 for h in hitsB if h[6] <= 3.0),
    len(hitsB),
    len(M)**3 * len(R)**2, time.time()-t0), flush=True)
for a, b, c, p, q, v, sd in sorted(hitsB, key=lambda t: t[6])[:30]:
    print("  A=%d B=%d C=%d p=%s q=%s → %.12f  σ_dev=%.3f（rel dev %.3e）" % (
        a, b, c, p, q, v, sd, abs(v-TARGET)/TARGET), flush=True)

# 对照：0.1% 容差口径（宽容差，无 σ 意义）
print("\n===== 对照：0.1% 容差（≈" + str(round(0.001*TARGET/SIGMA_OBS)) + "σ）口径 =====", flush=True)
cntA = sum(1 for p in R for q in R if val(7,5,2,p,q) is not None and abs(float(val(7,5,2,p,q))-TARGET)/TARGET <= 0.001)
print("方案 A 0.1% 容差命中 = " + str(cntA) + "（其中 σ<=3 的 = " + str(sum(1 for _,_,_,s in hitsA if s <= 3.0)) + "）", flush=True)
