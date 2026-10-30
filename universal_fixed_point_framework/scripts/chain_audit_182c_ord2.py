# -*- coding: utf-8 -*-
"""chain_audit_182c_ord2.py — ord(2) 奇偶判定修正 + v2 收缩通道完整分类（不硬编码 ord(2)）
用 2^ord(4) ≡ ±1 判定 ord(2) = ord(4)（+1，奇）或 2×ord(4)（−1）。
修正 182b 硬编码错误：k=9,13 的 ord(2) 实际为奇（= ord(4)）。
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ord(4) 已知（104az-178/181）：{k: ord_4}
ord4 = {1: 26, 3: 14, 7: 1027, 9: 16387, 11: 262147, 13: 322639}
Ks = [1, 3, 7, 9, 11, 13]
print("=== ord(2) 奇偶判定（2^ord(4) mod p）+ v2 收缩完整分类 ===\n")
print(f"{'k':>3} {'p':>10} {'v2(p−1)':>8} {'2^ord4':>8} {'ord(2)':>9} {'v2(ord2)':>8} {'ord(4)收缩':>9} {'2进深度':>7}")
for k in Ks:
    p = 49 + 4**k
    v2p = 0
    t = p - 1
    while t % 2 == 0:
        v2p += 1
        t //= 2
    o4 = ord4[k]
    sgn = pow(2, o4, p)  # +1 → ord(2)=ord(4) 奇；−1 → ord(2)=2×ord(4)
    ord2 = o4 if sgn == 1 else 2 * o4
    v2o = 0
    t = ord2
    while t % 2 == 0:
        v2o += 1
        t //= 2
    # ord(4) 的 2 进收缩因子（相对 p−1）：S = 2^(v2(p−1) − v2(ord(4)))；v2(ord4) = max(v2o−1, 0)
    v2o4 = max(v2o - 1, 0)
    S = 2 ** (v2p - v2o4)
    d = v2p - v2o  # 2 进深度（对 ord(2)）
    tag = "奇(=ord4)" if sgn == 1 else "偶(=2×ord4)"
    print(f"{k:>3} {p:>10} {v2p:>8} {sgn:>8} {ord2:>9} {v2o:>8} {S:>9} {d:>7}  [{tag}]")

print("\n=== 结论 ===")
print("ord(4) 2 进收缩 S：k=1→2（幂基）、k=3→8（k_max）、k≥7→16（不动点²）——全框架量 ✓（与 182 结论一致）")
print("ord(2) 奇偶：k=1,3,7,11 → 偶（2^ord(4) ≡ −1）；k=9,13 → 奇（2^ord(4) ≡ +1，ord(2)=ord(4)）")
print("★ 修正 182b 硬编码错误：k=9,13 的 v2(ord(2)) = 0（非 1）——2 进深度 {0,2,3,4,3,4}")
print("★ 深度 0（k=1）解析闭合：p≡5 mod 8 → Legendre(2/p)=−1 → ord(2)=p−1")
print("★ 奇删除通道：仅 k=13（g=13，ord(2) 奇且删奇因子 13）；k=7,9,11 奇部分完整保留")
