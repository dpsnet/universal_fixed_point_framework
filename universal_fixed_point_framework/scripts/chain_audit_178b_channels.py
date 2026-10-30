# -*- coding: utf-8 -*-
"""chain_audit_178b_channels.py — 家族 N(k)=49+4^k 完整通道扫描（Miller-Rabin + Pollard Rho）"""
import io, sys, random, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# --- Miller-Rabin ---
def isprime(n):
    if n < 2: return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small:
        if n % p == 0: return n == p
    d, s = n-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0: continue
        x = pow(a, d, n)
        if x == 1 or x == n-1: continue
        for _ in range(s-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True

def pollard_rho(n):
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    while True:
        c = random.randrange(1, n)
        f = lambda x: (x*x + c) % n
        x = y = random.randrange(2, n)
        d = 1
        while d == 1:
            x = f(x); y = f(f(y))
            d = math.gcd(abs(x-y), n)
        if d != n: return d

def factor(n, out):
    if n == 1: return
    if isprime(n): out.append(n); return
    d = pollard_rho(n)
    factor(d, out); factor(n//d, out)

def ord_mod(a, p):
    phi = p-1
    facs = []
    m = phi
    d = 2
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

random.seed(42)
print("=== N(k) = 49+4^k：k=0..60 完整扫描 ===")
primes, comp = [], []
for k in range(0, 61):
    v = 49 + 4**k
    if isprime(v):
        primes.append(k)
        print(f"k={k:>2}: 素数 ★")
    else:
        facs = []
        factor(v, facs)
        facs.sort()
        f = facs[0]
        ordv = ord_mod(4, f)
        comp.append((k, f, facs))
        print(f"k={k:>2}: 合数 因子 {'×'.join(map(str,facs))} 最小 {f}（ord={ordv}）→ 通道 k≡{k%ordv} mod {ordv}")

print(f"\n素数 k：{primes}")
print(f"奇合数 k：{[k for k,_,_ in comp if k%2==1]}")
print(f"偶合数 k：{[k for k,_,_ in comp if k%2==0]}")

print("\n=== 通道结构（奇 k）===")
for k, f, facs in comp:
    if k % 2 == 1:
        ordv = ord_mod(4, f)
        print(f"奇 k={k:>2}: 最小因子 {f:<7} ord={ordv:<6} 通道 k ≡ {k%ordv} (mod {ordv})  全因子 {facs}")

print("\n=== 素数成员自通道核验 ===")
for k0 in primes:
    v0 = 49 + 4**k0
    if isprime(v0):
        ordv = ord_mod(4, v0)
        # 找第一个 k>k0 且 k≡k0 mod ordv 的成员
        k2 = k0 + ordv
        if k2 <= 60:
            ok = (49 + 4**k2) % v0 == 0
            print(f"N({k0}) = {v0}（素数）ord_4 = {ordv} → 通道 k ≡ {k0} mod {ordv}：k={k2} 被 {v0} 整除 = {ok}")
        else:
            print(f"N({k0}) = {v0}（素数）ord_4 = {ordv} → 首个覆盖点 k={k0+ordv} > 60（未验证）")
