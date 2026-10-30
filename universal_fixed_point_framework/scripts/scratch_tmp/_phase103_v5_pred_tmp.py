# -*- coding: utf-8 -*-
"""Phase 103o: v5 预言对照——①线序（出发 n）②B 依赖 vs 观测
① 线序预言：Hα(n=3)/Hβ(n=4)/Hγ(n=5) 出发 → 转移份额 1/n → 高阶线缺失更多
② B 依赖：转移份额随 B 上升 vs 观测 blue/|缺失| 分档（26.14）
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

def simulate(B_mg, T, K, n0, n_trials=200000, seed=7):
    kT = 8.617e-5 * T
    random.seed(seed)
    trans = missing = 0
    for _ in range(n_trials):
        n = n0
        fail_run = 0
        for t in range(1, 501):
            e = eta_comp(B_mg, n)
            if random.random() < e:
                if random.random() < 1.0 / n:
                    trans += 1
                else:
                    missing += 1
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
                if n > n0 - 1 and n > 2:   # 向下滞留不低于出发线低一档（Balmer 禁 n=2）
                    n -= 1
        else:
            missing += 1
    return (trans/n_trials, missing/n_trials)

print('=== ① 线序预言：出发 n 依赖（T=12000K, K=10, B=45MG）===')
print('预言：转移份额 ∝ 1/n₀ → 高阶线（n₀ 大）缺失更多')
print('%-6s | %-8s | %-8s | %s' % ('出发', '转移', '缺失', '比'))
for n0, line in ((3, 'Hα'), (4, 'Hβ'), (5, 'Hγ')):
    tr, mi = simulate(45.0, 12000, 10, n0)
    r = tr/mi if mi else 999
    print('%-4s(%s) | %.3f   | %.3f   | %.3f' % (n0, line, tr, mi, r))

print()
print('=== ② B 依赖预言 vs 观测（T=12000K, K=10, 出发 n=4）===')
print('v5 预言：转移份额随 B 上升')
print('%-8s | %-22s | %s' % ('B(MG)', 'v5 转移份额', '观测 blue/|缺失|（26.14）'))
for B in (5.0, 10.0, 20.0, 45.0, 100.0):
    tr, mi = simulate(B, 12000, 10, 4)
    r = tr/mi if mi else 999
    print('%-8.0f | 转移=%.3f 缺失=%.3f 比=%.3f | <10MG: 0.055 / 10-48: 0.074'
          % (B, tr, mi, r))
