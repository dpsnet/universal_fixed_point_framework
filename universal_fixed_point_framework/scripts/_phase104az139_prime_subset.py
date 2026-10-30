# -*- coding: utf-8 -*-
"""104az-139：闭包质数子列判别（137/138 深化）。
检验：闭包 n（n≤512）的质数成员密度 vs 随机期望；全部质数成员的框架身份。"""
import math

FRAME = [2, 3, 5, 7]

def is_smooth(x):
    if x <= 0:
        return False
    for p in FRAME:
        while x % p == 0:
            x //= p
    return x == 1

def factors(x):
    facs = []
    d = 2
    t = x
    while d * d <= t:
        while t % d == 0:
            facs.append(d)
            t //= d
        d += 1
    if t > 1:
        facs.append(t)
    return facs

def is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True

closure = [2,3,4,5,6,7,8,9,11,13,15,17,19,26,29,31,41,49,55,71,97,99,127,161,244,251,449]
primes = [n for n in closure if is_prime(n)]
composites = [n for n in closure if not is_prime(n)]

print("=" * 78)
print("闭包质数子列判别（104az-139，n<=512）")
print("=" * 78)
print(f"\n① 闭包成员 {len(closure)} 个，质数 {len(primes)} 个，合数 {len(composites)} 个")
print(f"   质数密度 = {len(primes)}/{len(closure)} = {len(primes)/len(closure)*100:.1f}%")
# 随机期望：n<=512 质数约 95 个（π(512)=97），在 27 个随机样本中期望
n_expect = sum(is_prime(i) for i in range(2, 513))
expect_in_27 = n_expect / 511 * len(closure)
print(f"   随机对照：n<=512 质数 {n_expect} 个（密度 {n_expect/511*100:.1f}%），27 个随机样本期望质数 {expect_in_27:.1f} 个")
print(f"   ★ 实测 {len(primes)} vs 期望 {expect_in_27:.1f} —— 比值 {len(primes)/expect_in_27:.1f}x")

print(f"\n② 质数闭包成员及其框架身份：")
for n in primes:
    # 尝试 Mersenne / 框架积±1 / 框架幂±1
    ident = []
    # Mersenne 2^p-1
    p = 0
    while 2 ** p - 1 <= n:
        if 2 ** p - 1 == n:
            ident.append(f"Mersenne 2^{p}-1")
        p += 1
    # 框架积 ±1：n-1 或 n+1 为 7-平滑
    if is_smooth(n - 1):
        ident.append(f"(n-1)={n-1} 7-平滑 ({factors(n-1)})")
    if is_smooth(n + 1):
        ident.append(f"(n+1)={n+1} 7-平滑 ({factors(n+1)})")
    print(f"   n={n:3d}: {n}²−1={n*n-1} ({factors(n*n-1)})  {'; '.join(ident)}")

print(f"\n③ 合数闭包成员（对照）：")
for n in composites:
    print(f"   n={n:3d}: {n}²−1={n*n-1} ({factors(n*n-1)})")

print(f"\n④ 判别结论：")
print(f"   质数密度 {len(primes)}/{len(closure)}={len(primes)/len(closure)*100:.0f}% vs 随机期望 {expect_in_27:.0f} 个（~{expect_in_27/len(closure)*100:.0f}%）")
print(f"   —— 比值 {len(primes)/expect_in_27:.1f}x：闭包结构强偏好质数（'闭包即质数筛选'）")
all_ident = True
for n in primes:
    ok = (n in (3,7,31,127)) or is_smooth(n-1) or is_smooth(n+1)
    if not ok:
        all_ident = False
print(f"   全部 {len(primes)} 个质数闭包成员均满足 Mersenne 或 (n±1) 7-平滑 —— {all_ident}")
print("=" * 78)
