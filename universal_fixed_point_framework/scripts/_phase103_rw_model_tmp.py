# -*- coding: utf-8 -*-
"""Phase 103h: 随机游走谱扩散模型 v1（探索版）
假说（26.12）：被禁吸收的能量进入再处理循环 → 量子数 ± 均匀随机游走（26.10 对称性）
→ 达电离阈（n_ion）→ 连续谱转移；达 n=2 → 低频转移；循环超时 → 囚禁缺失
目标：P(连续谱)/P(缺失) ≈ 21%/79%（对 Hβ 能量账本）能否自然导出

模型（一维吸收边界随机游走）：
- 态空间 n = 2..n_ion（n=2 下吸收边界，n_ion 上吸收边界）
- 从 n=4（Hβ 上态）出发
- 每步 n→n±1 均匀（P=0.5/0.5）
- 达 n=2 → 低频转移（Hα 区）；达 n_ion → 连续谱转移；步数超 T_max → 囚禁缺失
"""
import math
from collections import Counter

def simulate(n_start, n_low, n_high, T_max, n_trials=200000, seed=42):
    import random
    random.seed(seed)
    low = high = timeout = 0
    # 额外记录：连续谱转移的循环次数分布（延迟叠加）
    t_dist = Counter()
    for _ in range(n_trials):
        n = n_start
        for t in range(1, T_max + 1):
            n += random.choice((-1, 1))
            if n <= n_low:
                low += 1
                break
            if n >= n_high:
                high += 1
                t_dist[t] += 1
                break
        else:
            timeout += 1
    tot = n_trials
    return {
        'n_high': n_high, 'T_max': T_max,
        'P_low(低频转移)': low / tot,
        'P_high(连续谱转移)': high / tot,
        'P_timeout(囚禁缺失)': timeout / tot,
        'ratio_high_vs_timeout': high / timeout if timeout else float('inf'),
        't_med': int(sorted(t_dist.elements())[len(t_dist)//2]) if t_dist else None,
    }

print('=== 随机游走谱扩散 v1：扫描 n_ion 与 T_max ===')
print('目标：P(连续谱)/P(缺失) ≈ 0.21/0.79 = 0.266')
print()
for n_high in (5, 6, 8, 10, 14, 20):
    for T_max in (10, 30, 100, 300):
        r = simulate(4, 2, n_high, T_max)
        print('n_ion=%3d T_max=%3d | 低频=%.3f 连续谱=%.3f 缺失=%.3f | 比=%.3f | 转移中位步=%s'
              % (n_high, T_max, r['P_low(低频转移)'], r['P_high(连续谱转移)'], r['P_timeout(囚禁缺失)'],
                 r['ratio_high_vs_timeout'], r['t_med']))
    print()
