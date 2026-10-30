# -*- coding: utf-8 -*-
# Phase 104az-95: σ 交汇封闭定理 Lean 形式化前置证伪检验
# 定理: ∀ k N : ℕ, 1 ≤ N → N < 2k → N(2k−N) = 2^k−1 → k ∈ {1,2,4}
# 证伪策略: 全枚举 k=1..12, N=1..2k−1 (比随机样本更严格)
#   ① 收集所有解, 验证解集 k ∈ {1,2,4}
#   ② 验证 bound 引理: N(2k−N) ≤ k² 对所有 1≤N<2k
#   ③ 验证 k≥5 → k² < 2^k−1 (归纳引理的真值)
#   ④ 验证判别式条件: k²−2^k+1 ≥ 0 且为平方 ⟺ k ∈ {1,2,4}
import math

print("=== ① 全枚举解集 (k=1..12, N=1..2k−1) ===")
sols = []
for k in range(1, 13):
    for N in range(1, 2*k):
        lhs = N*(2*k - N)
        rhs = 2**k - 1
        if lhs == rhs:
            sols.append((k, N))
print(f"解集: {sols}")
sol_k = sorted(set(k for k, _ in sols))
print(f"解的 k 值: {sol_k}")
print(f"k ∈ {{1,2,4}}? {sol_k == [1, 2, 4]}")
assert sol_k == [1, 2, 4], "定理证伪!"
print("✓ ① 通过: 解集 k ∈ {1,2,4}")

print("\n=== ② bound 引理: N(2k−N) ≤ k² (k=1..12 全 N) ===")
ok = True
for k in range(1, 13):
    for N in range(1, 2*k):
        if N*(2*k-N) > k*k:
            ok = False
            print(f"  反例 k={k}, N={N}")
print(f"bound 成立? {ok}")
assert ok, "bound 证伪!"
print("✓ ② 通过: N(2k−N) ≤ k² 恒成立 (等号 N=k)")

print("\n=== ③ k≥5 → k² < 2^k−1 (k=5..20) ===")
ok = True
for k in range(5, 21):
    if k*k >= 2**k - 1:
        ok = False
        print(f"  反例 k={k}")
print(f"指数引理成立? {ok}")
assert ok, "指数引理证伪!"
print("✓ ③ 通过: k≥5 时 k² < 2^k−1")

print("\n=== ④ 判别式条件: k²−2^k+1 ≥ 0 且为完全平方 ===")
res = []
for k in range(1, 11):
    v = k*k - 2**k + 1
    sq = math.isqrt(v) if v >= 0 else None
    is_sq = sq is not None and sq*sq == v
    res.append((k, v, is_sq))
    print(f"  k={k}: k²−2^k+1 = {v}, 完全平方={is_sq}")
good = [k for k, v, s in res if s]
print(f"完全平方的 k: {good} ⟺ {{1,2,4}}? {good == [1,2,4]}")
assert good == [1, 2, 4], "判别式条件证伪!"
print("✓ ④ 通过: 判别式完全平方 ⟺ k ∈ {1,2,4}")

print("\n=== ⑤ 解表与对偶结构 ===")
for k, N in sols:
    sil = 2*k - N
    print(f"  (k_max={2*k}, N_gen={N}, 静默={sil}): {N}×{sil} = {2**k}-1 = M_{k}")
print("\n全部证伪检验通过 — 定理可投入 Lean 形式化")
