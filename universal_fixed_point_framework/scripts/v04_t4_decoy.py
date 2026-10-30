# -*- coding: utf-8 -*-
"""104az-214：T4（g_p/2 双有理式商族）decoy 负控对照
补全 P3 v0.4 四件套到第 4 个旗舰（104az-212 遗留：T4 选择性覆盖 4 样本不足做 Fisher）。
设计：同域随机 decoy 8 个（[0.9T, 1.1T]，8 位小数，seed 固定），σ_obs 与 g_p/2 同口径（8.2e-8），
T4 全族（17627328 组合）扫每个 decoy → σ≤5 命中数；Fisher 精确检验（真实 1 命中 vs decoy 合并）。
"""
import random, time
from fractions import Fraction
from scipy.stats import fisher_exact

K = [2, 3, 4, 5, 7, 8, 16, 25, 49, 64]
D = [45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100]
R = sorted({Fraction(k, d) for k in K for d in D})
M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]

T = 2.79284734463          # g_p/2 真实目标
SIG = 8.2e-8               # σ_obs（CODATA 2018 μ_p/μ_N）
FAMILY = len(M)**3 * len(R)**2   # 17627328

Rf = [(p, float(p)) for p in R]

def scan(target, sig, cap):
    """T4 全族扫，返回 σ≤cap 命中数与 ≤3σ 命中数。"""
    n_le5 = 0
    n_le3 = 0
    for a in M:
        af = float(a)
        for b in M:
            bf = float(b)
            for c in M:
                cf = float(c)
                for p, pf in Rf:
                    for q, qf in Rf:
                        denom = cf + qf
                        if abs(denom) < 1e-15:
                            continue
                        d2 = bf / denom
                        if abs(d2) < 1e-15:
                            continue
                        vf = (af - pf) / d2
                        sd = abs(vf - target) / sig
                        if sd <= cap:
                            n_le5 += 1
                            if sd <= 3.0:
                                n_le3 += 1
    return n_le5, n_le3

print("T4 族大小 = %d；真实目标 g_p/2 = %.11f（σ_obs=%.2e）" % (FAMILY, T, SIG), flush=True)

t0 = time.time()
r5, r3 = scan(T, SIG, 5.0)
print("真实 g_p/2：σ≤5 命中 %d（其中 ≤3σ %d）[%.1fs]" % (r5, r3, time.time() - t0), flush=True)

rng = random.Random(214)
decoys = [round(T * (0.9 + 0.2 * rng.random()), 8) for _ in range(8)]
print("decoy 集（同域 [%.4f, %.4f]，8 位小数）：%s" % (T*0.9, T*1.1, decoys), flush=True)

d5_total = 0
d3_total = 0
per = []
t0 = time.time()
for i, dT in enumerate(decoys):
    t1 = time.time()
    n5, n3 = scan(dT, SIG, 5.0)
    d5_total += n5
    d3_total += n3
    per.append((dT, n5, n3))
    print("decoy %d = %.8f：σ≤5 命中 %d（≤3σ %d）[%.1fs]" % (i, dT, n5, n3, time.time() - t1), flush=True)
print("decoy 合并：σ≤5 命中 %d / %d 族（%.1fs）" % (d5_total, 8 * FAMILY, time.time() - t0), flush=True)

# Fisher：真实 1 命中 vs decoy 合并命中（家族各为一次试验域）
if r5 > 0 or d5_total > 0:
    table = [[r5, FAMILY - r5], [d5_total, 8 * FAMILY - d5_total]]
    _, p = fisher_exact(table, alternative="greater")
    print("Fisher 精确检验（σ≤5 口径）：[[%d, %d],[%d, %d]] → p = %.4g" % (
        r5, FAMILY - r5, d5_total, 8 * FAMILY - d5_total, p), flush=True)
    verdict = "唯一性获负控支撑（decoy 零命中）" if d5_total == 0 else "decoy 亦有命中，唯一性受挑战"
    print("判定：%s" % verdict, flush=True)
else:
    print("真实与 decoy 均零命中——Fisher 不可用（基线 0 vs 0）", flush=True)
