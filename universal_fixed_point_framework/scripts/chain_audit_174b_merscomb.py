# -*- coding: utf-8 -*-
"""chain_audit_174b.py — 557731 梅森组合身份广搜：M×q±r、2^m×q±r、同余类"""
import io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

N = 557731
# 框架量池（含小框架量）
fw_small = [2,3,4,5,7,8,9,10,16,24,30,31,40,42,45,49,56,61,63,64,65,71,80,125,127,210,231,343,371,405,450,500,13500]
mers = [(m, 2**m-1) for m in range(2, 21)]

print(f"=== 1. 557731 = M_m × q + r（q,r 框架量）===")
found = []
for m, Mv in mers:
    for q in fw_small:
        rem = N % Mv
        qq = N // Mv
        if rem in fw_small and qq <= 200:
            found.append((m, Mv, qq, rem))
for m, Mv, qq, rem in found:
    print(f"557731 = M_{m}({Mv}) × {qq} + {rem} ★")
print(f"共 {len(found)} 个")

print(f"\n=== 2. 557731 = 2^m × q + r（q,r 框架量）===")
found2 = []
for m in range(4, 21):
    p = 2**m
    qq, rem = divmod(N, p)
    if rem in fw_small and qq <= 200:
        found2.append((m, p, qq, rem))
for m, p, qq, rem in found2:
    print(f"557731 = 2^{m}({p}) × {qq} + {rem} ★")
print(f"共 {len(found2)} 个")

print(f"\n=== 3. 557731 ± 框架量 = M_m（梅森数邻接）===")
for m, Mv in mers:
    for w in fw_small:
        if N - w == Mv: print(f"557731 − {w} = M_{m} ★★★")
        if N + w == Mv: print(f"557731 + {w} = M_{m} ★★★")
print("（若上面无输出则无梅森数邻接）")

print(f"\n=== 4. 同余类检查（mod 框架量）===")
for w in fw_small[:18]:
    print(f"557731 mod {w:>4} = {N % w}")

print(f"\n=== 5. 557731 类型检查 ===")
print(f"557731 mod 4 = {N%4}（≡3 → 非两平方和；素数 p≡3 mod 4）")
# 索菲热尔曼：2p+1 素数？
sophie = (N-1)//2
print(f"(N−1)/2 = {sophie}，合数? {sophie%5==0}")
# 安全素数：p = 2q+1 且 q 素数
q = (N-1)//2
def isprime(x):
    if x < 2: return False
    d = 2
    while d*d <= x:
        if x % d == 0: return False
        d += 1
    return True
print(f"N 为安全素数？q=(N−1)/2={q} 素数={isprime(q)} → {isprime(q) and isprime(N)}")
print(f"N 为索菲热尔曼素数？2N+1={2*N+1} 素数={isprime(2*N+1)}")
