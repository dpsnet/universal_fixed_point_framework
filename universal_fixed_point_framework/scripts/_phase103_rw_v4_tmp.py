# -*- coding: utf-8 -*-
"""Phase 103m: 随机游走 v4——部分保留 = Landau 化扭曲的逐步泄漏
修正：v2/v3 用 n_ion 一次性阈值（η_comp>0.9 才转移）——真实物理是每步泄漏
p_leak(n) = η_comp(n, B)（简并加权：tail 在 C*l_B 外的比例 = Landau 化破坏率）
- 每步先检泄漏：随机 < p_leak(n) → 转移（连续谱）
- 否则向上热驱动：p_up = e^{−ΔE/kT} × (1/n)（m=0 轴向态比例）
- K 次向上失败 → 囚禁缺失；向下滞留 n→n-1（n≥3，Balmer 禁 n=2）
检验：逐步泄漏 + 1/n 效率能否复现 21/79（比 0.266）——n_ion 参数消失
"""
import math, random

RY = 13.6
C = 3.03
B_CRIT1_MG = 2350.0

def E(n): return -RY / (n * n)
def delta_up(n): return E(n+1) - E(n)

def laguerre(n, k, x):
    if n == 0: return 1.0
    if n == 1: return 1.0 + k - x
    l0, l1 = 1.0, 1.0 + k - x
    for i in range(2, n + 1):
        l2 = ((2 * i - 1 + k - x) * l1 - (i - 1 + k) * l0) / i
        l0, l1 = l1, l2
    return l1

def radial_tail(n, l, R_L):
    norm2 = (2.0 / n) ** 3 * math.factorial(n - l - 1) / (2.0 * n * math.factorial(n + l))
    def prob_density(r):
        z = 2.0 * r / n
        L = laguerre(n - l - 1, 2 * l + 1, z)
        log_R2 = math.log(norm2) + (-2.0 * r / n) + 2.0 * l * math.log(z) + 2.0 * math.log(abs(L)) if L != 0 else -1e6
        return math.exp(log_R2) * r * r
    N = 2000
    total = 0.0
    for i in range(N):
        t = (i + 0.5) / N
        r = R_L + t / (1.0 - t)
        total += prob_density(r) / ((1.0 - t) ** 2)
    return total / N

_cache = {}
def eta_comp(B_mg, n):
    key = (round(B_mg, 2), n)
    if key in _cache: return _cache[key]
    lB = math.sqrt(B_CRIT1_MG / B_mg)
    R_L = C * lB
    tot = 0.0
    for l in range(0, n):
        w = (2.0 * l + 1) / (n * n)
        tot += w * radial_tail(n, l, R_L)
    _cache[key] = tot
    return tot

def simulate(B_mg, T, K, n_trials=200000, seed=7):
    kT = 8.617e-5 * T
    random.seed(seed)
    trans = missing = stalled = 0
    for _ in range(n_trials):
        n = 4
        fail_run = 0
        for t in range(1, 501):
            # 每步 Landau 化泄漏（强磁场扭曲）
            if random.random() < eta_comp(B_mg, n):
                trans += 1
                break
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

print('=== v4：逐步 Landau 化泄漏 + 1/n 轴向效率（无 n_ion 参数）===')
print('目标 转移/缺失 = 0.266（21%/79%）')
print()
for B in (20.0, 45.0, 100.0):
    print('--- B=%.0f MG（η_comp(n=4)=%.3f）---' % (B, eta_comp(B, 4)))
    for T in (12000, 20000):
        for K in (3, 8, 10, 20):
            tr, mi, st = simulate(B, T, K)
            r = tr/mi if mi else 999
            mark = ' <<<' if 0.15 < r < 0.45 else ''
            print('  T=%d K=%2d | 转移=%.3f 缺失=%.3f 滞留=%.3f | 比=%.3f%s' % (T, K, tr, mi, st, r, mark))
    print()
