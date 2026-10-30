# -*- coding: utf-8 -*-
"""Phase 103l: 随机游走 v3——p_up 效率第一性化检验
假说：p_up 效率 ×0.25 = 1/n₀（n=4 出发态倒数）= m=0 轴向态比例
（Landau 化横向紧致 → 禁 m≠0 圆周态 → 只留轴向 m=0 通道；n 态 m=0 数 = n，总 n²，比例 1/n）
逐步 p_up(n) = e^{−ΔE(n→n+1)/kT} × (1/n)
对照：v2 拟合 p0×0.25 = 0.743×0.25 = 0.186（常数）——v3 第一步应完全一致
目标：转移/缺失 = 0.266（21%/79%）
"""
import math, random
from collections import Counter

RY = 13.6
def E(n): return -RY / (n * n)
def delta_up(n): return E(n+1) - E(n)

def simulate(T, n_ion, K, n_trials=200000, seed=7):
    kT = 8.617e-5 * T
    random.seed(seed)
    trans = missing = stalled = 0
    for _ in range(n_trials):
        n = 4
        fail_run = 0
        for t in range(1, 501):
            if n >= n_ion:
                trans += 1
                break
            # 第一性 p_up：热驱动 × m=0 轴向比例（Landau 化禁圆周态）
            p_up = math.exp(-delta_up(n) / kT) * (1.0 / n)
            if random.random() < p_up:
                n += 1
                fail_run = 0
            else:
                fail_run += 1
                if fail_run >= K:
                    missing += 1
                    break
                if n > 3:
                    n -= 1
        else:
            stalled += 1
    return (trans/n_trials, missing/n_trials, stalled/n_trials)

print('=== v3：p_up(n) = e^{−ΔE(n→n+1)/kT} × (1/n)（m=0 轴向态比例）===')
print('目标 转移/缺失 = 0.266')
print('n=4 出发：p_up(4) @ T=12000K = %.4f（v2 拟合 p0×0.25 = 0.186 对照）' % (math.exp(-delta_up(4)/(8.617e-5*12000)) * 0.25))
print()
for T in (6000, 12000, 20000):
    print('--- T=%d K ---' % T)
    for K in (1, 3, 10):
        for n_ion in (6, 8, 12):
            tr, mi, st = simulate(T, n_ion, K)
            r = tr/mi if mi else float('inf')
            mark = ' <<< 接近目标' if 0.15 < r < 0.45 else ''
            print('  K=%2d n_ion=%2d | 转移=%.3f 缺失=%.3f 滞留=%.3f | 比=%.3f%s' % (K, n_ion, tr, mi, st, r, mark))

print()
print('=== 最优参数区精细扫描（T=12000K）===')
best = None
for K in (3, 5, 8, 10, 15):
    for n_ion in (5, 6, 7):
        tr, mi, st = simulate(12000, n_ion, K)
        r = tr/mi if mi else 999
        dev = abs(r - 0.266)
        if best is None or dev < best[0]:
            best = (dev, K, n_ion, tr, mi, r)
        if dev < 0.05:
            print('  K=%2d n_ion=%d | 转移=%.3f 缺失=%.3f | 比=%.3f | |Δ|=%.3f' % (K, n_ion, tr, mi, r, dev))
print('最优: K=%d n_ion=%d 转移=%.3f 缺失=%.3f 比=%.3f (偏差 %.3f)' % (best[1], best[2], best[3], best[4], best[5], best[0]))
