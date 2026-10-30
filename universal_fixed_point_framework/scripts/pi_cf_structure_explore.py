# -*- coding: utf-8 -*-
"""π 连分数 = 作用量层级演化？——结构探索（2026-10-26 用户直觉）

检验：
1. 收敛 p_n/q_n 的分子分母素数分解——是否落框架素因子集 {2,3,5,7,11,13}
2. 部分商序列统计 vs 高斯-库兹明分布期望（随机性检验）
3. 收敛精度层级 vs 框架量
"""
import mpmath as mp
mp.mp.dps = 200
pi = mp.pi

# 连分数展开 40 项
parts = []
x = pi
for _ in range(40):
    a = int(x)
    parts.append(a)
    x = 1 / (x - a)

# 收敛 p_n/q_n
p_nm2, q_nm2 = 1, 0   # p_{-2}, q_{-2}
p_nm1, q_nm1 = 0, 1   # p_{-1}, q_{-1}
convergents = []
for a in parts:
    p_n = a * p_nm1 + p_nm2
    q_n = a * q_nm1 + q_nm2
    convergents.append((p_n, q_n))
    p_nm2, q_nm2 = p_nm1, q_nm1
    p_nm1, q_nm1 = p_n, q_n

# 素数分解工具
def prime_factors(n):
    facs = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            facs[d] = facs.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        facs[n] = facs.get(n, 0) + 1
    return facs

FW_PRIMES = {2, 3, 5, 7, 11, 13}

print("=== ① 收敛分子分母素数分解（前 15 个）===")
print(f"{'n':>2} {'部分商':>6} {'p_n':>10} {'q_n':>10}  素因子(分子) / 素因子(分母)  落FW集?")
for i, (a, (p, q)) in enumerate(zip(parts, convergents)):
    if i >= 15:
        break
    fp = prime_factors(p)
    fq = prime_factors(q)
    p_str = "×".join(f"{k}^{v}" if v > 1 else str(k) for k, v in sorted(fp.items()))
    q_str = "×".join(f"{k}^{v}" if v > 1 else str(k) for k, v in sorted(fq.items()))
    ok = set(fp) <= FW_PRIMES and set(fq) <= FW_PRIMES
    print(f"{i:>2} {a:>6} {p:>10} {q:>10}  {p_str:>20} / {q_str:>20}  {'✓' if ok else '✗'}")

print("\n=== ② 部分商序列统计 vs 高斯-库兹明期望 ===")
from collections import Counter
cnt = Counter(parts)
n = len(parts)
print(f"总项数: {n}")
for k in [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15]:
    obs = cnt.get(k, 0) / n
    # 高斯-库兹明：P(a=k) = -log2(1 - 1/(k+1)^2)
    import math
    gk = -math.log2(1 - 1 / (k + 1) ** 2)
    print(f"a={k:>2}: 观测 {obs:.3f} vs 高斯-库兹明 {gk:.3f}  偏差 {obs-gk:+.3f}")

print("\n=== ③ 收敛精度层级 ===")
print(f"{'n':>2} {'收敛 p/q':>22} {'误差':>12}")
for i, (p, q) in enumerate(convergents):
    if i >= 8:
        break
    err = abs(float(p) / q - float(mp.pi))
    print(f"{i:>2} {p}/{q:>8}  {err:.2e}")

print("\n=== ④ 部分商序列的'层级块'观察 ===")
# 非平凡部分商（≥3）的位置
pos = [(i, a) for i, a in enumerate(parts) if a >= 3]
print("≥3 部分商位置序列:", pos)
print(f"共 {len(pos)} 个非平凡项 / {n} 总项 = {len(pos)/n*100:.0f}%")
print("随机期望（高斯-库兹明）：P(a≥3) ≈ 31.5%——与观测对比")
