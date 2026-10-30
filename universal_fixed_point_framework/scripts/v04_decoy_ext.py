# -*- coding: utf-8 -*-
"""104az-216：decoy 扩集复验 —— T1 质量余量稳定性 + T4 深命中普遍性
闭合 104az-215 诚实边界（decoy 集有限：T1 10/T4 8，需更大样本）。
① T1：50 decoy（同域 ±10%）最优命中 dev 分布，真实 (400,231) 3.60e-6 的秩；
② T4：20 decoy（同域 ±10%，σ_obs 同 8.2e-8）σ≤5/σ≤3 命中数与最优 σ 深度，真实 σ=1.493 的秩。
判定：真实质量在 decoy 最优中的秩 → "命中质量唯一"是否获统计支撑。
"""
import numpy as np
from fractions import Fraction
import random, time

K = [2, 3, 4, 5, 7, 8, 16, 25, 49, 64]
D = [45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100]
R = sorted({Fraction(k, d) for k in K for d in D})
M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
F16 = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105, 231, 320, 675, 400]

T_KAPPA = 401.73304855
T_G = 2.79284734463
SIG_G = 8.2e-8

print("========== ① T1（κΛ 家族）50 decoy 质量余量复验 ==========", flush=True)

def t1_best(target, A_arr, n_arr):
    """T1 族 A*(1+1/n) 最优命中 dev。"""
    best = 1e9
    for Ai in A_arr:
        v = Ai * (1 + 1.0 / n_arr)
        dev = np.abs(v - target) / target
        m = float(dev.min())
        if m < best:
            best = m
    return best

A_arr = np.array(F16, dtype=np.float64)
n_arr = np.arange(1, 5001, dtype=np.float64)
real_t1 = t1_best(T_KAPPA, A_arr, n_arr)
print("真实 κΛ 最优命中 dev = %.3e（(400,231)，v0.3 登记 3.6e-6）" % real_t1, flush=True)

rng = random.Random(216)
dec_t1 = [T_KAPPA * (0.9 + 0.2 * rng.random()) for _ in range(50)]
bests = []
t0 = time.time()
for dT in dec_t1:
    bests.append(t1_best(dT, A_arr, n_arr))
bests.sort()
rank = sum(1 for b in bests if b < real_t1) + 1
print("50 decoy 最优 dev：min=%.3e  max=%.3e  median=%.3e" % (bests[0], bests[-1], bests[24]), flush=True)
print("真实 dev %.3e 在 51 个（1 真实 + 50 decoy）最优中排名 %d（rank=1 表示族内质量最优获 50 样本支撑）" % (real_t1, rank), flush=True)
print("比值：decoy 最优 / 真实 = %.2f×（>10× 为数量级分离）" % (bests[0] / real_t1), flush=True)
print("[%.1fs]" % (time.time() - t0), flush=True)

print("", flush=True)
print("========== ② T4（g_p/2 家族）20 decoy 深命中复验（numpy 向量化） ==========", flush=True)

Rf = np.array([float(p) for p in R], dtype=np.float64)
Mf = np.array(M, dtype=np.float64)
# 预计算 p 网格（1×101）与 q 网格（101×1）
P = Rf[None, :]
Q = Rf[:, None]

def t4_stats(target, sig):
    n5 = 0
    n3 = 0
    best_sd = 1e9
    for a in Mf:
        for b in Mf:
            for c in Mf:
                denom = c + Q          # 101x101（c≥2、Q>0，无除零）
                d2 = b / denom
                vf = (a - P) / d2      # 101x101
                sd = np.abs(vf - target) / sig
                m5 = sd <= 5.0
                n5 += int(m5.sum())
                n3 += int((sd <= 3.0).sum())
                bm = float(sd.min())
                if bm < best_sd:
                    best_sd = bm
    return n5, n3, best_sd

t0 = time.time()
r5, r3, rb = t4_stats(T_G, SIG_G)
print("真实 g_p/2：σ≤5 命中 %d（≤3σ %d），最优 σ=%.3f [%.1fs]" % (r5, r3, rb, time.time() - t0), flush=True)

rng2 = random.Random(2161)
dec_t4 = [round(T_G * (0.9 + 0.2 * rng2.random()), 8) for _ in range(20)]
d5 = []
d3 = []
dbest = []
t0 = time.time()
for dT in dec_t4:
    n5, n3, bm = t4_stats(dT, SIG_G)
    d5.append(n5)
    d3.append(n3)
    dbest.append(bm)
    print("  decoy %.8f：σ≤5 %d，≤3σ %d，最优 σ=%.3f [%.1fs]" % (dT, n5, n3, bm, time.time() - t0), flush=True)

d5a = np.array(d5)
d3a = np.array(d3)
dbesta = np.array(dbest)
print("", flush=True)
print("decoy σ≤5 命中分布：0 个的有 %d/20，最大 %d，合计 %d；≤3σ 合计 %d" % (
    int((d5a == 0).sum()), int(d5a.max()), int(d5a.sum()), int(d3a.sum())), flush=True)
print("decoy 最优 σ 深度：min=%.3f  median=%.3f  max=%.3f（真实 = 1.493）" % (
    float(dbesta.min()), float(np.median(dbesta)), float(dbesta.max())), flush=True)
better = int((dbesta < rb).sum())
print("最优 σ 深于真实（<1.493）的 decoy 数 = %d/20" % better, flush=True)
print("Fisher（σ≤5）：[[%d, %d],[%d, %d]]" % (r5, 17627328 - r5, int(d5a.sum()), 20 * 17627328 - int(d5a.sum())), flush=True)
