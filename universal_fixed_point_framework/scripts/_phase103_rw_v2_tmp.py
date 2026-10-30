# -*- coding: utf-8 -*-
"""Phase 103i: 随机游走谱扩散 v2（能量学版）
v1 证伪：纯对称游走 → 低频(n=2)转移主导 + 缺失需人为超时——不能导出 21%/79%
v2 修正（MUFPF 物理）：
- 向下禁戒：Balmer 系整体禁戒（η_comp 禁 n→2 发射）→ n=2 方向为反射边界（不能成为转移）
- 向上热驱动：+Δn 需热库注入，概率 p_up = e^{−ΔE/kT}（白矮星大气 T，kT≈1 eV）
- 达 n_ion（电离阈/连续谱区）→ 连续谱转移（观测 blue/red 增强）
- 连续 K 次向上失败（热库不足）→ 能量囚禁 → 缺失
扫描 p_up、K、n_ion：找 P(连续谱)/P(缺失) ≈ 0.21/0.79
"""
import random
from collections import Counter

# 氢能级 E_n = -13.6/n^2 eV；从 n=4 出发（Hβ 上态）
RY = 13.6

def E(n): return -RY / (n * n)

def delta_up(n): return E(n+1) - E(n)   # 正值：向上需注入

def simulate(p_up, n_ion, K, T_max=500, n_trials=200000, seed=7):
    random.seed(seed)
    trans = missing = stalled = 0
    t_dist = Counter()
    for _ in range(n_trials):
        n = 4
        fail_run = 0
        for t in range(1, T_max + 1):
            # 向下（n→n-1）：Balmer 禁戒——禁止 n=2 到达；但 n≥3 的向下（Paschen）自由？
            # v2 简化：禁戒区为 n=2 反射；n≥3 向下到 3 算滞留（Paschen 未观测，不转移）
            # 向上尝试：热驱动
            if n >= n_ion:
                trans += 1
                t_dist[t] += 1
                break
            # 向上
            if random.random() < p_up:
                n += 1
                fail_run = 0
            else:
                fail_run += 1
                if fail_run >= K:
                    missing += 1
                    break
                # 向下滞留（n→n-1，但不低于 3）
                if n > 3:
                    n -= 1
        else:
            stalled += 1
    tot = n_trials
    return (trans/tot, missing/tot, stalled/tot,
            int(sorted(t_dist.elements())[len(t_dist)//2]) if t_dist else None)

print('=== v2 能量学版：向下 Balmer 禁戒（n=2 反射）+ 向上热驱动 + K 次失败囚禁 ===')
print('目标：P(连续谱)/P(缺失) = 0.21/0.79 = 0.266')
print('kT(12000K)=1.03 eV；ΔE(n=4→5)=%.3f eV → p_up(n=4)=%.3f' % (delta_up(4), __import__('math').exp(-delta_up(4)/1.03)))
print()
import math
p_up4 = math.exp(-delta_up(4)/1.03)
for T in (6000, 12000, 20000):
    kT = 8.617e-5 * T
    # p_up 随 n 变化：p_up(n) = exp(-ΔE(n)/kT)；用首步近似或常数
    p0 = math.exp(-delta_up(4)/kT)
    print('--- T=%d K (kT=%.3f eV) p_up(n=4)=%.3f ---' % (T, kT, p0))
    for p_scale in (1.0, 0.5, 0.25):
        p = p0 * p_scale
        for K in (1, 3, 10):
            for n_ion in (6, 8, 12):
                tr, mi, st, tmed = simulate(p, n_ion, K)
                if 0.05 < tr < 0.5 and 0.05 < mi < 0.95:
                    print('  p_up=%.3f K=%2d n_ion=%2d | 转移=%.3f 缺失=%.3f 滞留=%.3f | 比=%.3f | 中位步=%s'
                          % (p, K, n_ion, tr, mi, st, tr/mi if mi else float('inf'), tmed))
