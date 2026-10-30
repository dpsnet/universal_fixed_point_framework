# -*- coding: utf-8 -*-
"""S412 δ* 选择机制闭合尝试（d_H 缺口）
S322：d_H 生成链 7/8 溯源——唯一缺口 = δ* 系数 {6,4,8,5}
  选择机制——本步用 S409-S411 配对结构闭合：
  约束集能否唯一确定 {6,4,8,5} × {3,5,7,8}？
"""
import itertools

print("=== S412 δ* 选择机制约束唯一性检验 ===")
print()

# δ* 候选系数域：空间 {4,6} ∪ 窗口 {5,8}（S410）
COEFF_POOL = [4, 5, 6, 8]
# 幂次域：原生带 − {单位,幂基,向量,双向量} = {3,5,7,8}（S410 幂次集）
POWER_POOL = [3, 5, 7, 8]

# 空间项系数（Clifford 层）、窗口项系数（S410）
SPACE_COEFFS = {4, 6}
WINDOW_COEFFS = {5, 8}
# 低幂/高幂（S411 先几何后冻结）
LOW_POWERS = {3, 5}
HIGH_POWERS = {7, 8}

print(f"[1] 约束候选集：")
print(f"  C1 系数域 = 空间{{4,6}} ∪ 窗口{{5,8}} = {COEFF_POOL}")
print(f"  C2 幂次域 = 原生带−{{1,2,4,6}} = {POWER_POOL}")
print(f"  C3 空间配低幂、窗口配高幂：")
print(f"    {SPACE_COEFFS}×σ^{LOW_POWERS}、{WINDOW_COEFFS}×σ^{HIGH_POWERS}")
print(f"  C4 交叉和守恒：两配对（系数和=幂次和）∈ 减量带")
print(f"  C5 8 公共节点（一次幂次一次系数）")
print(f"  C6 窗口对 5+8 = 13")
print()

# C3+C4 组合检验：空间系数配低幂、窗口系数配高幂，
# 每配对 = 1 空间 + 1 窗口（S411），交叉和守恒
solutions = []
# 配对结构：每个配对取 1 空间系数 + 1 窗口系数 + 1 低幂 + 1 高幂
space_cs = list(SPACE_COEFFS)      # {4,6}
window_cs = list(WINDOW_COEFFS)    # {5,8}
low_ps = list(LOW_POWERS)          # {3,5}
high_ps = list(HIGH_POWERS)        # {7,8}

# 配对1 + 配对2 覆盖全部 4 系数 4 幂次
for s1, s2 in itertools.permutations(space_cs, 2):
    for w1, w2 in itertools.permutations(window_cs, 2):
        for l1, l2 in itertools.permutations(low_ps, 2):
            for h1, h2 in itertools.permutations(high_ps, 2):
                # 配对1：(s1, l1) + (w1, h1)
                # 配对2：(s2, l2) + (w2, h2)
                if (s1 + w1 == l1 + h1) and (s2 + w2 == l2 + h2):
                    sol = ((s1, l1), (w1, h1), (s2, l2), (w2, h2))
                    if sol not in solutions:
                        solutions.append(sol)

print(f"[2] C3+C4 组合检验结果：")
print(f"  满足（空间×低幂 + 窗口×高幂）且交叉和守恒的解：")
for sol in solutions:
    (s1, l1), (w1, h1), (s2, l2), (w2, h2) = sol
    print(f"    配对1: {s1}σ^{l1} + {w1}σ^{h1}（和 {s1+w1}={l1+h1}）"
          f"    配对2: {s2}σ^{l2} + {w2}σ^{h2}（和 {s2+w2}={l2+h2}）")
print(f"  解数 = {len(solutions)}")
print()

# 检查 δ* 是否在解中
target = ((6, 3), (5, 8), (4, 5), (8, 7))  # 按项排序
found = False
for sol in solutions:
    items = [(c, p) for c, p in sol]
    if sorted(items) == sorted(target):
        found = True
print(f"[3] δ* = 6σ³+4σ⁵+8σ⁷+5σ⁸ 是否在解中：{'✓ 是' if found else '✗ 否'}")
print()

# 附加约束 C5（8 公共节点）：8 既作系数又作幂次
c5_sols = []
for sol in solutions:
    coeffs = [c for c, p in sol]
    powers = [p for c, p in sol]
    if 8 in coeffs and 8 in powers:
        c5_sols.append(sol)
print(f"[4] C5（8 公共节点——8 既作系数又作幂次）过滤：")
print(f"  通过数 = {len(c5_sols)} / {len(solutions)}")
print()

# C6（窗口对 5+8=13——自动满足：5,8 都在窗口项）
print(f"[5] C6（窗口对 5+8=13）——窗口项包含 {5,8}——自动满足")
print()

print(f"[6] 结论：")
if len(solutions) == 1:
    print(f"  ★★ C3+C4 唯一确定解——δ* 组合在约束下唯一！")
elif len(solutions) <= 4:
    print(f"  ★★ 解数 {len(solutions)}——极窄——再加 C5 过滤：")
    print(f"    {len(c5_sols)} 个解——若唯一则选择机制闭合")
else:
    print(f"  解数 {len(solutions)}——约束不够紧——需新约束")
print()
print("  机制陈述（S412 候选）：")
print("    δ* 系数-幂次选择 = 约束组合：")
print("    · 系数 = 空间{4,6}+窗口{5,8}（Clifford 层 + 窗口机制）")
print("    · 幂次 = 演化/窗口常数{3,5,7,8}（原生带去空间层）")
print("    · 配对 = 空间+窗口跨层（先几何后冻结——S411）")
print("    · 交叉和守恒 → 11/12（显态/非向量态——S409）")
print("    · 8 公共节点 + 窗口对 5+8=13（S409/S410）")
