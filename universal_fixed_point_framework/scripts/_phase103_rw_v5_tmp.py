# -*- coding: utf-8 -*-
"""Phase 103n: 随机游走 v5——Landau 化破坏的分账（1/n 转移 vs 热化）
每步：
  1) Landau 化破坏：P = η_comp(n, B)（tail 在 C*l_B 外）
     - 破坏后：m=0 轴向份额 (1/n) → 连续谱转移（B：发射）
               圆周份额 (1−1/n) → 原子吸收热化 → 缺失（A：红外窗口外，26.14b）
  2) 未破坏 (1−η_comp)：
     - 向上热驱动 p = e^{−ΔE/kT} × (1/n) → n+1
     - 失败 K 次 → 囚禁缺失；否则向下滞留（n>3）
验证：21/79（比 0.266）是否自然涌现（η_comp、1/n、玻尔兹曼全部第一性）
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
    trans = missing = 0
    for _ in range(n_trials):
        n = 4
        fail_run = 0
        for t in range(1, 501):
            e = eta_comp(B_mg, n)
            if random.random() < e:
                # Landau 化破坏：m=0 份额转移，圆周份额热化缺失
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
                if n > 3:
                    n -= 1
        else:
            missing += 1   # 超时按缺失
    return (trans/n_trials, missing/n_trials)

print('=== v5：破坏分账（1/n 转移 vs 热化）+ 未破坏游走 ===')
print('目标 转移/缺失 = 0.266（21%/79%）')
print()
for B in (20.0, 45.0, 100.0):
    print('--- B=%.0f MG（η_comp(n=4)=%.3f）---' % (B, eta_comp(B, 4)))
    for T in (12000, 20000):
        for K in (3, 8, 10):
            tr, mi = simulate(B, T, K)
            r = tr/mi if mi else 999
            mark = ' <<< 接近 0.266' if abs(r - 0.266) < 0.1 else ''
            print('  T=%d K=%2d | 转移=%.3f 缺失=%.3f | 比=%.3f%s' % (T, K, tr, mi, r, mark))
    print()
