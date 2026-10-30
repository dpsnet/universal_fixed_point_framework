# -*- coding: utf-8 -*-
"""104az-135：平方差 7-平滑闭包完整谱判别（134 A1 勘误扩展）。
134 只测 n=2..8（7/7）；复核发现 n=9: 9²−1=80=2⁴·5 亦落框架素基。
本步：n=2..64 全扫描——闭包 n 序列、最长连续段、断裂结构、奇 n 亚序列。"""
import sympy as sp  # 若可用；否则用自实现试除

FRAME_PRIMES = [2, 3, 5, 7]

def is_frame_smooth(x):
    """x 的质因子 ⊆ {2,3,5,7}？"""
    rem = x
    for p in FRAME_PRIMES:
        while rem % p == 0:
            rem //= p
    return rem == 1

def prime_factors(x):
    facs = []
    d = 2
    while d * d <= x:
        while x % d == 0:
            facs.append(d)
            x //= d
        d += 1
    if x > 1:
        facs.append(x)
    return facs

N_MAX = 64
results = []
for n in range(2, N_MAX + 1):
    v = n * n - 1
    ok = is_frame_smooth(v)
    facs = prime_factors(v)
    results.append((n, v, ok, facs))

print("=" * 78)
print("平方差 7-平滑闭包谱：n=2..64（质因子 ⊆ {2,3,5,7} = 框架素基闭包）")
print("=" * 78)
print(f"{'n':>3} | {'n²−1':>6} | 闭包 | 质因子")
print("-" * 40)
for n, v, ok, facs in results:
    tag = "✓" if ok else "✗"
    print(f"{n:>3} | {v:>6} | {tag:^4} | {facs}")

# 最长连续段
segments = []
start = None
for n, v, ok, facs in results:
    if ok and start is None:
        start = n
    elif not ok and start is not None:
        segments.append((start, n - 1))
        start = None
if start is not None:
    segments.append((start, N_MAX))
print("\n>>> 连续闭包段：", segments)
longest = max(segments, key=lambda s: s[1] - s[0])
print(f">>> 最长连续段 = [{longest[0]}, {longest[1]}]（长度 {longest[1] - longest[0] + 1}）")

# 首个断裂
first_break = next((n for n, v, ok, facs in results if not ok), None)
print(f">>> 首个断裂 n = {first_break}（n={first_break}: {first_break}²−1={first_break*first_break-1} = {prime_factors(first_break*first_break-1)}）")

# 闭包 n 的奇偶分析
odd_ok = [(n, v) for n, v, ok, _ in results if ok and n % 2 == 1]
even_ok = [(n, v) for n, v, ok, _ in results if ok and n % 2 == 0]
print(f">>> 闭包奇数 n：{[n for n, _ in odd_ok]}")
print(f">>> 闭包偶数 n：{[n for n, _ in even_ok]}")

# 关键身份
print("\n>>> 关键身份判别：")
print(f"  n=9: 9²−1 = 80 = 2⁴·5 = 不动点²×静默（16×5）✓ —— 134 漏测，本步补入")
print(f"  n=9 = k_max+1 = 8+1；n=10 断裂 = k_max+2")
print(f"  n=10: 99 = 9·11（11 质因子，非框架素基）—— 首个断裂")
print(f"  n=29: 29²−1 = 840 = 2³·3·5·7 全框架（29 = 2⁵−3？29 = 对合域×4+1 = 29 +1 家族）")
print(f"  n=31: 31²−1 = 960 = 2⁶·3·5 全框架（31 = 2⁵−1 Mersenne，静默指数）")
print(f"  n=63: 63²−1 = 3968 = 2⁷·31（31 质因子离开纯框架素基——134 A3 迭代边界）")
print(f"  31 是 n=31（闭包）的 n 值、也是 n=63 断裂的质因子——31 双重角色")
