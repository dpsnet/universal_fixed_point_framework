# -*- coding: utf-8 -*-
"""chain_audit_178_channels.py — 家族 N(k)=49+4^k 合数覆盖通道扫描"""
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

def minfactor(n, limit=2_000_000):
    """试除找最小素因子（到 limit 或 sqrt）"""
    if n % 2 == 0: return 2
    d = 3
    while d*d <= n and d <= limit:
        if n % d == 0: return d
        d += 2
    return None  # 无小因子（或素数）

def ord_mod(a, p):
    """a mod p 的乘法阶"""
    phi = p-1
    # 扫描 phi 的因子
    facs = []
    d = 2; m = phi
    while d*d <= m:
        if m % d == 0:
            facs.append(d)
            while m % d == 0: m //= d
        d += 1
    if m > 1: facs.append(m)
    o = phi
    for f in facs:
        while o % f == 0 and pow(a, o//f, p) == 1:
            o //= f
    return o

print("=== N(k) = 49+4^k：k=0..40 素性 + 最小素因子 + 通道 ===")
primes, composites = [], []
for k in range(0, 41):
    v = 49 + 4**k
    if isprime(v):
        primes.append(k)
        print(f"k={k:>2}: {v:<18} 素数 ★")
    else:
        f = minfactor(v)
        composites.append((k, f))
        # ord
        ordv = ord_mod(4, f) if f else None
        print(f"k={k:>2}: {v:<18} 合数 最小因子 {f}  4^ord≡1 mod {f} (ord={ordv})")

print(f"\n素数 k（奇区）: {[k for k in primes]}")
print(f"合数 k（奇区）: {[k for k,f in composites if k%2==1]}")

print("\n=== 覆盖通道分析（奇 k 合数由哪些小因子通道覆盖）===")
# 对每个奇合数 k，记录因子与 k mod ord
for k, f in composites:
    if k % 2 == 1:
        ordv = ord_mod(4, f)
        r = k % ordv
        print(f"奇 k={k}: 因子 {f}（ord_4 = {ordv}）→ 通道 k ≡ {r} (mod {ordv})")

print("\n=== 通道延伸验证 ===")
# 29 通道：ord_29(4) = 14，k ≡ 5 mod 14 → 29 整除
print("29 通道（k=5 起点）：k ≡ 5 mod 14 → k=5,19,33 → 验证 N(19) 被 29 整除:",
      49 + 4**19, "mod 29 =", (49 + 4**19) % 29)
print("验证 N(33) 被 29 整除（若可算）:", (49 + pow(4, 33, 29)) % 29 == 0)
