# -*- coding: utf-8 -*-
# Phase 104az-93b: σ 交汇方程解的精确证明 — Bott 塔封闭
# 交汇方程: N_gen·(k_max−N_gen) = 2^{k_max/2}−1
# 定理: 解集 k_max ∈ {2, 4, 8} = Bott 塔前三层, 8 为最大解 (封闭层)
import math

def M(n): return 2**n - 1

print("=== 定理: 交汇方程 N·(2k−N) = 2^k−1 的整数解 ===")
print("令 k_max = 2k (Mersenne 侧需整数指数), 则 N_gen²−2k·N_gen+(2^k−1) = 0")
print("判别式 D = 4k²−4(2^k−1) = 4(k²−2^k+1)")
print("有整数解 ⟺ k²−2^k+1 ≥ 0 且为完全平方")
print()

print("=== k 扫描 (k=1..10) ===")
sols = []
for k in range(1, 11):
    val = k*k - 2**k + 1
    sq = int(math.isqrt(val)) if val >= 0 else None
    is_sq = sq is not None and sq*sq == val
    k_max = 2*k
    ng_sols = []
    if is_sq:
        # N = [2k ± 2·sqrt(val)]/2 = k ± sqrt(val)
        for ng in {k - sq, k + sq}:
            if 1 <= ng <= k_max-1 and ng*(k_max-ng) == 2**k-1:
                ng_sols.append(ng)
        sols.append((k, k_max, ng_sols))
    tag = ''
    if is_sq:
        tag = '平方! N_gen解=' + str(ng_sols)
    elif val < 0:
        tag = '<0'
    else:
        tag = '非平方'
    print(f"  k={k}: k_max={k_max}, k²−2^k+1 = {val} [{tag}]")

print()
print("=== 结论 ===")
print("解 k ∈ {1,2,4} (k²−2^k+1 = 0,1,1 全为平方)")
print("k≥5: k²−2^k+1 < 0 (指数增长超越平方) → 无解")
print("→ k_max = 2k ∈ {2, 4, 8} — 全部是 2 的幂 = Bott 塔前三层!")
print("→ k_max=8 是最大解 — 交汇方程在 8 处封闭!")
print()

print("=== 解表 ===")
for k, km, ngs in sols:
    for ng in ngs:
        sil = km - ng
        print(f"  k_max={km}, N_gen={ng}, 静默单元={sil}: {ng}×{sil} = {2**k-1} = M_{k} ✓")

print()
print("=== 对偶结构 ===")
print("解 (N_gen, 静默) 成对出现: (4,1)↔(4,3), (8,3)↔(8,5), (2,1) 自对偶")
print("(8,3) 的对偶 (8,5) = 104az-84 的 (3,5) 互补对 Rec/Sp 分岔!")
print("活跃侧指数 3→M_3=7 (Sp 缺失对偶), 静默侧指数 5→M_5=31 (Rec d_eff 分子)")
print()

print("=== 实际参数选择的约束 ===")
print("N_gen=3 的解: (4,3) 与 (8,3)")
print("约束 N_gen < k_max/2 (代数自由度小于半维): (4,3) 中 3>2 排除, (8,3) 中 3<4 保留 ✓")
print("约束 N_gen ≥ 2 (至少双色): 排除 (2,1),(4,1)")
print("→ (8,3) 是唯一满足 N_gen≥2 ∧ N_gen<k_max/2 的解")
print()

print("=== 第四个独立论证: k_max=8 必然性 ===")
print("① 104az-263: 代数映射门坎 (k_max=8 代数必然)")
print("② 104az-264: k_max=8 = Clifford(3,1) 三类空结构")
print("③ 104az-265: k_max=2 幂 = paper20 定理 5.3")
print("④ 本段: σ 交汇方程解 = Bott 塔 {2,4,8}, 8 为封闭层, (3,5) 对偶 = Rec/Sp 分岔")

print()
print("=== 诚实边界 ===")
print("定理证明依赖: 交汇恒等 (104az-91 代数) + 判别式完全平方条件 (标准二次方程)")
print("解集 {2,4,8} 是精确数学结论 (可复核)")
print("约束 N_gen<k_max/2 与 N_gen≥2 是框架诠释 (选择 (8,3) 的附加条件)")
print("(4,3) 解的存在说明交汇方程本身不唯一 — 需框架约束排除")
