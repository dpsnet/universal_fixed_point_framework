# -*- coding: utf-8 -*-
"""S224 指数集来源攻坚：指数资格准则证伪扫描
候选准则：n ∈ 指数集 ⟺ 2^n±1 至少单侧落框架命名集
扫描 n=1..30——确认 [1,8] 闭合、[9,30] 无命中（k_max 封顶）
"""
print("=== S224: 指数集来源——指数资格准则 ===\n")

# 框架命名集（核心常数 + 链上身份）
FC_named = {3, 5, 7, 8, 9, 15, 16, 17, 42, 127, 257}
# 链身份（非壳——正交结构）：31（梅森链）、137（幂基递归）
chain_id = {31, 137}
print(f"框架命名集: {sorted(FC_named)}")
print(f"链身份（非壳）: {sorted(chain_id)}")

print("\n=== 1. n=1..30 的 2^n±1 闭合扫描 ===")
print(f"{'n':<4}{'2^n-1':<12}{'2^n+1':<12}{'2^n':<10}闭合判定")
exponents = []
for n in range(1, 31):
    lo, mid, hi = 2**n-1, 2**n, 2**n+1
    hits = []
    if lo in FC_named: hits.append(f"{lo}=2^{n}-1")
    if mid in FC_named: hits.append(f"{mid}=2^{n}")
    if hi in FC_named: hits.append(f"{hi}=2^{n}+1")
    # 链身份单独标记（不计数为壳闭合）
    chain = []
    if lo in chain_id: chain.append(f"{lo}(链)")
    if hi in chain_id: chain.append(f"{hi}(链)")
    status = "闭合" if hits else ("链身份" if chain else "-")
    if hits: exponents.append(n)
    print(f"{n:<4}{lo:<12}{hi:<12}{mid:<10}{status}{(' ['+', '.join(hits)+']') if hits else ((' ('+', '.join(chain)+')') if chain else '')}")

print(f"\n壳闭合指数（n<=8 内）: {sorted(e for e in exponents if e<=8)}")
print(f"超界闭合指数（n>8）: {sorted(e for e in exponents if e>8)}——空？")

print("\n=== 2. 准则检验 ===")
print("候选：n ∈ 指数集 ⟺ 2^n±1（或 2^n）落框架命名集")
print(f"指数集 [1,8] 内闭合: {sorted(e for e in exponents if e<=8)}")
print(f"指数集 [1,8] 内未闭合: {sorted(set(range(1,9)) - set(e for e in exponents if e<=8))}")
print(f"超界（n>8）命中: {sorted(e for e in exponents if e>8)}")

print("\n=== 3. 5、6 的排除原因 ===")
print("n=5: 31/33——31 链身份（梅森 M(5)）、33=3x11（11 显态但非命名）")
print("  → 结果侧无框架命名——不闭合——'开放窗口不闭壳'（静默语义）")
print("n=6: 63/65——63=3²x7（框架分解！）但 63 无命名身份")
print("  → 框架分解 ≠ 框架命名——资格看命名（命名集）")
print("  → 6=活跃x幂基——指数侧身份 ≠ 指数资格——资格由结果侧决定")

print("\n=== 4. 链身份 vs 壳身份（正交） ===")
print("31：梅森链身份（链端点 M(5)）——但非壳闭合——正交结构")
print("137：幂基递归身份（2⁷+2³+2⁰）——非 2^n±1 形式——独立身份")
print("→ '链身份≠壳身份'——两种结构分离——正交性确立")

print("\n=== 5. 结论 ===")
print("指数资格准则（数值支持）：")
print("  n ∈ {1..k_max}：2^n±1/2^n 落框架命名集 ⟺ n ∈ {1,2,3,4,7,8}")
print("  5、6 排除：结果侧无框架命名（31 链身份≠壳身份）")
print("  n>8 无命中：k_max 自指封顶（最大指数=幂基³）")
print("→ 准则先证伪通过（n=1..30 无超界意外闭合）")
print("→ '为何静默 5 不作指数' = 静默语义（不产生壳）+ 结果侧无命名")
