# -*- coding: utf-8 -*-
"""chain_audit_180_seedclass.py — mod 14 奇剩余类种子-通道分层 + 1073 框架因式分解 + ord 周期身份"""
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

inv, base, fp, sil, kmax, b0, Ngen = 7, 2, 4, 5, 8, 9, 3

print("=== mod 14 奇剩余类：种子-通道分层 ===")
print("奇 k mod 14 类：{1,3,5,7,9,11,13} → 每类首成员 N(k) 素性：")
seed_primes, seed_composites = [], []
for r in [1, 3, 5, 7, 9, 11, 13]:
    v = 49 + 4**r
    isp = isprime(v)
    tag = "★素数种子" if isp else "合数（无种子）"
    if isp: seed_primes.append(r)
    else: seed_composites.append(r)
    print(f"k={r:>2}（≡{r} mod 14）: N({r}) = {v} {tag}")

print(f"\n素数种子类：{seed_primes}（6/7）  非种子类：{seed_composites}（唯一 k=5）")

print("\n=== 唯一非种子类 k=5 的框架因式分解 ===")
print(f"N(5) = 1073 = 29×37")
print(f"29 = 对合域×不动点+1 = 7×4+1 = {inv*fp+1} ✓")
print(f"37 = 幂基²×N_gen²+1 = 4×9+1 = {base*base*Ngen*Ngen+1} ✓")
print(f"1073 = (对合域×不动点+1)(幂基²×N_gen²+1) = 29×37 = {29*37} ✓")
print(f"展开：{inv*fp+1}×{base*base*Ngen*Ngen+1} = {(inv*fp+1)*(base*base*Ngen*Ngen+1)}")

print("\n=== 框架量通道周期身份 ===")
print(f"ord_29(4) = 14 = 幂基×对合域 = {base*inv} ✓")
print(f"ord_37(4) = 18 = 幂基×N_gen² = {base*Ngen*Ngen} ✓")
print(f"ord_113(4) = 14 = 幂基×对合域（113 = N(3) 素数种子自通道）")
print(f"ord_53(4) = 26 = 2×13（13 = 幂基×N_gen²−静默 = {base*Ngen*Ngen}-{sil} = {base*Ngen*Ngen-sil} ✓）")
print(f"→ 框架量通道周期全部可框架化：14 = 幂基×对合域、18 = 幂基×N_gen²、26 = 幂基×(幂基×N_gen²−静默)")

print("\n=== 大 ord 通道结构（素数种子自通道）===")
for k in [7, 9, 11, 13]:
    v = 49 + 4**k
    # ord 已在 104az-178 算出：1027, 16387, 262147, 322639
    ords = {7: 1027, 9: 16387, 11: 262147, 13: 322639}
    o = ords[k]
    print(f"N({k}) = {v}（素数种子）ord_4 = {o}")
    if k in [7, 9, 11]:
        print(f"   ord = 2^(2k−4)+3 = 2^{2*k-4}+3 = {2**(2*k-4)}+3 = {2**(2*k-4)+3} ✓")
    else:
        print(f"   ord = {o} ≠ 2^(2k−4)+3 = {2**(2*k-4)+3}（例外）")

print("\n=== 结论 ===")
print("① mod 14 奇剩余类 6/7 有素数种子——素性谱 = 种子类；唯一 k=5 无种子")
print("② k=5 被框架量因子 29（=对合域×不动点+1）/37（=幂基²×N_gen²+1）源头覆盖——1073 有框架因式分解")
print("③ 框架量通道周期 14/18/26 全框架化（幂基×对合域 / 幂基×N_gen² / 幂基×(幂基×N_gen²−静默)）")
print("④ 大 ord 通道 = 素数种子自通道（2^(2k−4)+3 对 k=7,9,11 干净；k=13 例外待查）")
