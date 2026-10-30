# -*- coding: utf-8 -*-
# 104az-226 核磁子链候选谱系收束 + 预注册协议参数核验（pyenv 3.11.8）
# 1. 两候选（g_p/2 = 40217/14400、g_n/2 = 44/23）分子分母框架量分解交集
# 2. μ_p/μ_n 衍生比平方型族扫描（标注：衍生量，先验性弱，仅记录）
# 3. 预注册协议参数确认（族定义、值域、判定规则）
import numpy as np

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
BD = sorted(set(M + [1]))

print("=== 1. 核磁子链候选谱系：框架量分解交集 ===")
gp2_num_factors = {"131": "8×16+3 (k_max×幂基⁴+N_gen)", "307": "5×9×7−8 (静默×N_gen²×对合域−k_max)"}
gp2_den_factors = {"14400": "(8×15)² = 2⁶·3²·5² (k_max×B)², B=15=N_active×N_total"}
gn2_num_factors = {"44": "7²−5 (对合域²−静默) = 4×11 (不动点×11, 11=N_active+k_max)"}
gn2_den_factors = {"23": "5²−2 (静默²−幂基) = 7×3+2 (对合域×N_gen+幂基)"}
print("g_p/2 分子:", gp2_num_factors)
print("g_p/2 分母:", gp2_den_factors)
print("g_n/2 分子:", gn2_num_factors)
print("g_n/2 分母:", gn2_den_factors)
used_p = {2, 3, 5, 7, 8, 9, 15, 16}   # g_p/2 分解用到
used_n = {2, 3, 5, 7, 11}             # g_n/2 分解用到
inter = used_p & used_n
print(f"g_p/2 参数族 = {sorted(used_p)}")
print(f"g_n/2 参数族 = {sorted(used_n)}")
print(f"交集 = {sorted(inter)}（均框架量）")
print(f"并集 = {sorted(used_p | used_n)}")

print()
print("=== 2. μ_p/μ_n 衍生比平方型族扫描（衍生量，先验性弱，仅记录） ===")
mu_p = 2.79284734463
mu_n = 1.91304273
ratio = mu_p / mu_n
# μ_p/μ_n 相对不确定度 = μ_p(2.9e-10 相对) + μ_n(2.35e-7 相对) ≈ 2.36e-7 → 3σ ≈ 1e-6 绝对
th = 1.0e-6
hits = []
for a in M:
    for c in M:
        for b in BD:
            for d in BD:
                n2, d2 = a*a - b, c*c - d
                if n2 <= 0 or d2 <= 0:
                    continue
                val = n2/d2
                if abs(val - ratio) <= th:
                    hits.append((a, b, c, d, n2, d2, val, val-ratio))
print(f"μ_p/μ_n = {ratio:.10f}，3σ≈1e-6 → 命中 {len(hits)} 个")
for h in sorted(hits, key=lambda x: abs(x[7]))[:5]:
    a, b, c, d, n2, d2, val, diff = h
    print(f"  ({a}^2-{b})/({c}^2-{d}) = {n2}/{d2} = {val:.10f}  dev {diff:+.2e}")

print()
print("=== 3. 预注册检验协议 v1.0 参数确认 ===")
print("族定义: (a²−b)/(c²−d)，a,c∈M12，b,d∈M12∪{1}，24336 组合")
print("值域: [0.000091, 11024]，去重有理值 12219 个")
print("容差: |dev| ≤ 3σ_target（绝对口径，各量 CODATA/PDG 不确定度）")
print("判定: 命中 = 3σ 内存在族分数；唯一 = 去重后唯一分数")
print("升级条件: 未来新量/新测量值在该族 3σ 内命中（先验命中）→ 44/23 升格评估")
print("负控: 同域 decoy ≥10 × 全零命中（本轮与 222/224 已通过）")
