# -*- coding: utf-8 -*-
"""S223 壳机制攻坚：2 的壳生成特异性证伪扫描
壳 = 2^n±1 覆盖框架常数集——指数集 {1,2,3,4,7,8}
问题：2 是否特异？对照基底 3..8 的 n^m±1 覆盖率
"""
print("=== S223: 壳机制攻坚——2 的生成特异性 ===\n")

# 框架常数集（用户裁决）
FC = {3, 5, 7, 8, 15, 16, 17, 42, 127, 257, 9}
# 注意：42 是链积（2x3x7）——非 2^n±1 候选；9=k_max+1
# 框架常数（不含链积/倒数）：
FC_core = {3, 5, 7, 8, 15, 16, 17, 127, 257, 9}
print(f"框架常数集（核心）: {sorted(FC_core)}")

print("\n=== 1. 2^n±1 覆盖表（n=1..8） ===")
print(f"{'n':<3}{'2^n-1':<10}{'2^n+1':<10}{'闭合?':<6}备注")
matched = set()
for n in range(1, 9):
    lo, hi = 2**n-1, 2**n+1
    clo = "√" if lo in FC_core else "-"
    chi = "√" if hi in FC_core else "-"
    note = ""
    if lo in FC_core:
        note += " (2^n-1=%d)" % lo
        matched.add(lo)
    if hi in FC_core:
        note += " (2^n+1=%d)" % hi
        matched.add(hi)
    print(f"{n:<3}{lo:<10}{hi:<10}{clo+chi:<6}{note.strip()}")

print(f"\n覆盖：{sorted(matched)}——共 {len(matched)}/{len(FC_core)} 个核心常数")
print(f"未覆盖：{sorted(FC_core - matched)}")

print("\n=== 2. 指数集 {1,2,3,4,7,8} 的生成结构 ===")
print("1 = 单位元/恒等（id）")
print("2 = 幂基（伴随 eta/eps 对）")
print("3 = 活跃（F0 桥）")
print("4 = 不动点（伴随 4 组件）")
print("7 = 3+4 = 活跃+不动点 = 对合")
print("8 = 2x4 = 幂基x不动点 = k_max")
print("→ 指数集 = {幂基, 活跃, 不动点} 的 +/x 闭包（含恒等 1）")
print("→ '为何指数是框架常数' → '指数 = 伴随组合' 候选")

print("\n=== 3. 特异性对照扫描（基底 3..8，n^m±1，m=1..8） ===")
print(f"{'基底':<5}{'覆盖核心常数':<10}{'命中数':<6}{'命中/总'}")
for base in range(2, 9):
    hits = set()
    for m in range(1, 9):
        if base**m-1 in FC_core:
            hits.add(base**m-1)
        if base**m+1 in FC_core:
            hits.add(base**m+1)
    frac = len(hits)/len(FC_core)
    mark = " ← 2 特异？" if base == 2 else ""
    print(f"{base:<5}{sorted(hits)}{len(hits):<6}{frac:.2f}{mark}")

print("\n=== 4. 对照：3^n±1、4^n±1 明细 ===")
for base in [3, 4, 6, 8]:
    print(f"基底 {base}:")
    for m in range(1, 8):
        lo, hi = base**m-1, base**m+1
        hits = []
        if lo in FC_core: hits.append(f"{lo}=b^{m}-1")
        if hi in FC_core: hits.append(f"{hi}=b^{m}+1")
        if hits: print(f"  m={m}: {', '.join(hits)}")

print("\n=== 5. 结论 ===")
print("2 的覆盖（8/10——8/9 核心？）vs 其他基底——看命中数")
print("→ 若 2 命中显著高于其他 → 2 特异支持（伴随→2→壳）")
print("→ 若不特异 → 壳=2^n±1 是偶然 → 证伪机制候选")
