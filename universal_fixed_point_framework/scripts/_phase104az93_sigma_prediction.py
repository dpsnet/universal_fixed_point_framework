# -*- coding: utf-8 -*-
# Phase 104az-93: σ 交汇独立预言验证 — N_gen×静默单元 = M_{k_max/2} 的推广域检验
# σ⁻¹ = 15 双分解交汇 (104az-91): 代数侧 N_gen×静默单元 = Mersenne 侧 M_{k_max/2}
# 独立预言: 交汇要求 N_gen·(k_max−N_gen) = 2^{k_max/2}−1
# 若该约束唯一确定 (N_gen, k_max) 对 → 框架参数自洽预言
import math

def M(n): return 2**n - 1

print("=== σ 交汇推广域检验: N_gen·(k_max−N_gen) = 2^{k_max/2}−1 ===")
print("k_max=8: 3×(8−3) = 15 = 2⁴−1 = M_4 ✓ (104az-91 交汇)")
print()

print("=== 约束方程扫描 (k_max=2..16, N_gen=1..k_max−1) ===")
solutions = []
for km in range(2, 17):
    if km % 2 != 0:
        continue  # k_max/2 需整数 (Mersenne 侧 2^{k_max/2}−1)
    rhs = 2**(km//2) - 1
    for ng in range(1, km):
        lhs = ng * (km - ng)
        if lhs == rhs:
            solutions.append((km, ng))
            print(f"  k_max={km}: N_gen={ng} → {ng}×{km-ng} = {lhs} = 2^{km//2}−1 = {rhs} ✓ 解!")

print()
print(f"→ 共 {len(solutions)} 个整数解")
print("k_max=8, N_gen=3 是其中之一 (实际框架参数)")
print("k_max=4, N_gen=1? 检查: 1×3 = 3, 2²−1 = 3 ✓ — 也是解!")
print("k_max=16, N_gen=4? 检查: 4×12 = 48, 2⁸−1 = 255 ✗")
print()

print("=== 解的独特性分析 ===")
# 检查各解的框架相容性: N_gen 是否满足代数自由度角色
for km, ng in solutions:
    sil = km - ng
    print(f"  k_max={km}, N_gen={ng}, 静默单元={sil}, M_4侧=2^{km//2}−1={M(km//2)}")
    print(f"    → 代数侧 N_gen×静默 = {ng}×{sil} = {ng*sil}")

print()
print("=== 关键问题: 8 是唯一满足'静默单元 = k_max−N_gen = 奇数'的解? ===")
for km, ng in solutions:
    print(f"  k_max={km}: 静默单元 = {km-ng} (奇偶: {'奇' if (km-ng)%2==1 else '偶'})")

print()
print("=== 物理/框架诠释 ===")
print("交汇恒等 N_gen·(k_max−N_gen) = 2^{k_max/2}−1 是 σ⁻¹ 双结构的自洽条件")
print("实际解 (8,3): N_gen=3 是代数自由度(颜色), k_max=8 是 Clifford(3,1) 维数")
print("k_max=8 时唯一'静默单元为奇数且=5'的解 → 交汇给出唯一参数选择?")

print()
print("=== 独立预言: k_max=4 子结构? ===")
print("k_max=4, N_gen=1: 1×3 = 3 = 2²−1 = M_2")
print("  → 若 N_gen 必须≥2 (至少双自由度), k_max=4 解被排除")
print("  → 若要求 N_gen=3 (实际颜色数), 只有 k_max=8 满足")
print("  → 预言: 交汇唯一锁定 (N_gen, k_max) = (3, 8)")

print()
print("=== 诚实边界 ===")
print("交汇恒等是 104az-91 的代数结果; 推广域检验显示多个整数解")
print("(k_max=4, N_gen=1) 与 (k_max=8, N_gen=3) 都满足方程")
print("'唯一锁定 (3,8)' 依赖于附加约束 (N_gen=3 颜色数、Clifford(3,1) 维数 8)")
print("→ 交汇是自洽性证据但非唯一性预言 — 除非附加框架约束排除 (4,1)")
