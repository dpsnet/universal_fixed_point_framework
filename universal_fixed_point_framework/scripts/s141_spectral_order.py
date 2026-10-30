# S141 谱序-谱流参数单调 数值先证伪（模式8：全称命题→Python 采样）
# 定理候选：
#   agEigenvalue_mono : k1 ≤ k2 → λ_k1 ≤ λ_k2（k1,k2 ∈ [1,8]——谱序单调）
#   agEigenvalue_gap_positive : λ_1 < λ_2（谱隙正）
#   spectralGap_positive : 0 < Δλ_min（谱隙家族 S80）
import math, random

def ag(k, kmax=8):
    if 1 <= k <= kmax:
        return math.sqrt(k * (k + 1)) / math.sqrt(kmax * (kmax + 1))
    return 0.0

# 1) 单调性：k1 ≤ k2 → λ_k1 ≤ λ_k2
for _ in range(5000):
    k1, k2 = random.randint(1, 8), random.randint(1, 8)
    if k1 <= k2:
        assert ag(k1) <= ag(k2), f"mono fail: k1={k1} k2={k2} {ag(k1)} {ag(k2)}"
print("mono OK")

# 2) 谱隙正：λ_1 < λ_2
assert ag(1) < ag(2), "gap_positive fail"
print(f"gap_positive OK: λ1={ag(1):.12f} λ2={ag(2):.12f}")

# 3) Δλ_min > 0
d = ag(2) - ag(1)
assert d > 0, "spectralGap_positive fail"
print(f"spectralGap_positive OK: Δλ={d:.12f}")

# 4) 端点 = 1（S140 复核）
assert abs(ag(8) - 1.0) < 1e-15, "endpoint fail"
print("endpoint=1 OK")

# 5) 边界情况：k2 ≤ 8 保证（h: k1 ≤ k2 ∧ k2 ≤ 8）
for k1 in range(1, 9):
    for k2 in range(k1, 9):
        assert ag(k1) <= ag(k2), f"exhaustive fail {k1} {k2}"
print("exhaustive [1,8]² OK")

print("ALL OK")
