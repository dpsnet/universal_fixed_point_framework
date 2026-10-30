# -*- coding: utf-8 -*-
"""chain_audit_177_mod5.py — 家族 7²+4^k 模 5 解析规律验证 + k 偶 5 整除证明检查"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

print("=== 模 5 解析论证 ===")
print("4 ≡ −1 mod 5 → 4^k ≡ (−1)^k mod 5")
print("7² ≡ 2² ≡ 4 mod 5")
print("k 偶：4^k ≡ 1 mod 5 → 7²+4^k ≡ 4+1 = 0 mod 5 → 必被 5 整除（合数）")
print("k 奇：4^k ≡ 4 mod 5 → 7²+4^k ≡ 4+4 = 8 ≡ 3 mod 5 → 不被 5 整除（素性开放）\n")

print("=== 数值验证 k=0..14（家族 = 7² + 2^(2k) = 49 + 4^k）===")
bad = 0
for k in range(0, 15):
    v = 49 + 4**k
    is5 = (v % 5 == 0)
    expected5 = (k % 2 == 0)
    ok = (is5 == expected5)
    if not ok: bad += 1
    print(f"k={k:>2}: 49+4^{k:<2} = {v:<11} /5 {'整除' if is5 else '余 '+str(v%5):<4} 预期{'5整除' if expected5 else '非5'} {'✓' if ok else '✗'}")
print(f"\n全部一致：{bad == 0}（{bad} 个不一致）")

print("\n=== 推论 ===")
print("① 家族素性只可能出现在 k 奇（k 偶全部被 5 排除——解析证明）")
print("② 已知素数成员 {1,3,7,9,11,13} 全部为奇 k ✓；合数奇 k {5,15} 由更大素因子造成")
print("③ 53/113/16433 = 前三个梅森指标（k=1,3,7）上的素数——'梅森指标前 3 全命中' 在解析规律下：")
print("   前 3 个梅森指标都是奇数 → 未被 5 排除 → 素性开放——命中概率升为（素性开放区命中率）")
print("   开放区 k={1,3,5,7,9,11,13,15} 中素数 {1,3,7,9,11,13} = 6/8；前三个梅森指标恰好全中的条件概率 = 6/8×5/7×4/6 ≈ 0.357")
print("   → 梅森指标巧合的'显著性'修正：从 1/35（无结构）升为 ~36%（有奇 k 结构后非显著）——假说降级为观察")
