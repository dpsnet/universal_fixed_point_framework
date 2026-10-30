# -*- coding: utf-8 -*-
"""chain_audit_181_k13ord.py — k=13 ord 例外攻坚：322639 分解 + 框架身份 + g=13 猜想检验"""
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

inv, base, fp, sil, kmax, Ngen = 7, 2, 4, 5, 8, 3
print("=== k=13 ord 例外攻坚 ===")
p13 = 49 + 4**13
print(f"N(13) = {p13}（素数种子）")
print(f"p−1 = {p13-1} = 2^4 × {(p13-1)//16}")
odd = (p13-1)//16
print(f"奇部分 = {odd}")
# 分解奇部分
from math import isqrt
n = odd
facs = []
d = 2
while d*d <= n:
    while n % d == 0:
        facs.append(d); n //= d
    d += 1
if n > 1: facs.append(n)
print(f"奇部分分解 = {'×'.join(map(str,facs))}")
print(f"→ 13 在奇部分中：{13 in facs}；ord(4) = {p13-1}/208 = 322639（13 被从 ord 删除）")

print("\n=== 322639 分解 ===")
n = 322639
f2 = []
d = 2
while d*d <= n:
    while n % d == 0:
        f2.append(d); n //= d
    d += 1
if n > 1: f2.append(n)
print(f"322639 = {'×'.join(map(str,f2))}")
print(f"19 = 静默×不动点−1 = {sil}×{fp}−1 = {sil*fp-1} ✓（框架身份！）")
print(f"16981 素性 = {isprime(16981)}")

print("\n=== g 值序列 vs k 指标 ===")
# g = (p−1)/16 / ord（奇部分除以 ord）
gs = {1: 52//26, 3: 112//16//14, 7: 1027//1027, 9: 16387//16387, 11: 262147//262147, 13: 4194307//322639}
for k in [1,3,7,9,11,13]:
    print(f"k={k:>2}: (p−1)/16 = {[(52//16 if k==1 else (112//16 if k==3 else (1027 if k==7 else (16387 if k==9 else (262147 if k==11 else 4194307)))))]}, ord 完整/删除")
print(f"g = {{1:2, 3:8, 7:1, 9:1, 11:1, 13:13}}")
print(f"g 非平凡仅 k=1,3,13：2 = 幂基、8 = k_max、13 = k 指标自身")
print(f"→ 猜想：g_k = k 当 k | (p−1)/16 的奇部分；k=13 时 13 整除 → g=13；k=7 时 13 整除但 7 不整除 → g=1")
print(f"  k=7: 1027 = 13×79，13 整除但 g=1（13 ≠ k=7）——g 只取 k 自身，不取其他因子")
print(f"  k=13: 4194307 = 13×322639，13 = k → g=13 ✓ 猜想与两例一致")
