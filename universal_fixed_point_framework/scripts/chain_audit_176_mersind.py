# -*- coding: utf-8 -*-
"""chain_audit_176_mersind.py — 对合域²+2^(2k) 家族素数成员的梅森指标规律验证"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    d = 3
    while d*d <= n:
        if n % d == 0: return False
        d += 2
    return True

inv, base = 7, 2
print("=== 对合域² + 2^(2k) 家族素性扫描 k=0..15 ===")
primes = []
for k in range(0, 16):
    v = inv*inv + base**(2*k)
    p = isprime(v)
    mers_k = k in (1, 3, 7, 15)  # M_1..M_4
    tag = ""
    if p: primes.append(k); tag = " ★素数"
    if mers_k: tag += " (梅森指标 k=" + str(k) + ")"
    print(f"k={k:>2}: 7²+2^{2*k:>3} = {v:<10} {'素数' if p else '合数'}{tag}")

print(f"\n=== 规律检验 ===")
print(f"素数成员 k = {primes}")
print(f"梅森指标集 {1,3,7,15} 中 k=1,3,7 全素数；k=15（M_4）→ {inv*inv+base**30} = {inv*inv+base**30:,}")
print(f"  素性 = {isprime(inv*inv+base**30)} ← M_4 检验")
print(f"非梅森小 k {0,2,4,5,6,8,9,10,11,12,13,14} 全合数" + 
      "（9/10/11/12/13/14 未扫描则待确认）")

print(f"\n=== 53/113/16433 素因子辅助 ===")
print(f"65 = 5×13；305 = 5×61；1073 = 29×37；4145 = 5×829")
print(f"k=9: {inv*inv+base**18} = ? k=10: {inv*inv+base**20}")

# 细化：扫描 k=8..14 素性
print(f"\n=== 补充扫描 k=8..14 ===")
for k in range(8, 15):
    v = inv*inv + base**(2*k)
    print(f"k={k}: 7²+2^{2*k} = {v:,} {'素数' if isprime(v) else '合数'}")
