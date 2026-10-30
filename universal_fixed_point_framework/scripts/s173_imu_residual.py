# -*- coding: utf-8 -*-
"""S173 I_μ 残余解释扫描（先证伪——σ 幂/e 幂/混合候选）
I_μ^obs = E_μ − E_τ = 2.822392（间隔——观测精度 ~1e-6）
I_μ^cand = e + 42·e^{-6} = 2.8223894199——残余 Δ = 2.580e-6
目标：找到残余的框架组合候选
"""
import math

print("=== S173: I_μ 残余解释扫描（先证伪） ===\n")

e = math.e
sigma = 1/15
I_cand = e + 42*e**(-6)
I_obs = 2.822392  # E_μ − E_τ（PDG 6 位）
resid = I_obs - I_cand
print(f"I_μ^cand = {I_cand:.10f}")
print(f"I_μ^obs  = {I_obs:.10f}")
print(f"残余 Δ   = {resid:.3e}")
print(f"间隔误差 σ_interval = √(σ_μ,abs²+σ_τ,abs²) ≈ 2.93e-3（τ 主导）")
print(f"残余相对间隔误差：{abs(resid)/2.93e-3:.4f}σ（0.0009σ——误差内）\n")

print("=== σ 幂候选（σ=1/15） ===")
for k in range(3, 11):
    v = sigma**k
    print(f"  σ^{k} = {v:.3e}   2σ^{k} = {2*v:.3e}   Δ/σ^{k} = {resid/v:+.3f}")

print("\n=== e 幂候选 ===")
for k in range(10, 15):
    v = e**(-k)
    print(f"  e^{{-{k}}} = {v:.3e}   2e^{{-{k}}} = {2*v:.3e}")

print("\n=== 最优候选筛选（|Δ − 候选| 最小） ===")
cands = []
# σ 幂家族
for k in range(3, 11):
    v = sigma**k
    cands.append((abs(resid-v), f"σ^{k}", v))
    cands.append((abs(resid-2*v), f"2σ^{k}", 2*v))
    cands.append((abs(resid-3*v), f"3σ^{k}", 3*v))
# e 幂家族
for k in range(10, 16):
    v = e**(-k)
    cands.append((abs(resid-v), f"e^{{-{k}}}", v))
    cands.append((abs(resid-2*v), f"2e^{{-{k}}}", 2*v))
# 混合
cands.append((abs(resid-sigma**5*(1+sigma)), f"σ⁵(1+σ)", sigma**5*(1+sigma)))
cands.append((abs(resid-sigma**5*(2+sigma)), f"σ⁵(2+σ)", sigma**5*(2+sigma)))
cands.append((abs(resid-42*sigma**7), f"42σ⁷", 42*sigma**7))
cands.append((abs(resid-15*sigma**5), f"15σ⁵", 15*sigma**5))
cands.append((abs(resid-7*sigma**5), f"7σ⁵", 7*sigma**5))

cands.sort(key=lambda x: x[0])
print("  排名 | 候选 | 值 | |Δ−候选|")
for i, (d, name, v) in enumerate(cands[:10]):
    print(f"  {i+1}. {name:10s} = {v:.6e}   |Δ−候选| = {d:.2e}")

print("\n=== 最佳候选判别 ===")
best = cands[0]
print(f"  最佳：{best[1]} = {best[2]:.6e}——|Δ−候选| = {best[0]:.2e}")
print(f"  2σ⁵ = {2*sigma**5:.6e}（幂基 2 × σ⁵——σ 幂次家族——")
print(f"    σ³ 强子端 S121/σ⁸ 预测 S116 先例）")
print(f"  2σ⁵ vs Δ = {abs(resid-2*sigma**5):.2e}")

# 加修正后
I_new = I_cand + 2*sigma**5
print(f"\n=== 加 2σ⁵ 修正后 ===")
print(f"I_μ' = e + 42e^{{-6}} + 2σ⁵ = {I_new:.10f}")
print(f"|I_μ' − I_μ^obs| = {abs(I_new - I_obs):.3e}")
print(f"σ_score（间隔误差 2.93e-3）= {abs(I_new-I_obs)/2.93e-3:.2e}")
print(f"残余从 2.58e-6 → {abs(I_new-I_obs):.2e}——改善 {2.58e-6/abs(I_new-I_obs):.0f} 倍")

print("\n=== 语义评估 ===")
print("  2σ⁵：2=幂基、σ⁵=静默 5 次幂——框架语义成立")
print("  σ 幂修正先例：σ³（S121 强子端）、σ⁸（S116 预测）、")
print("    σ³(1+α_v')（S142 轻子投影）——σ 幂家族完整")
print("  ⚠ 后验候选：基于残余 2.58e-6≈2σ⁵ 选择——按纪律登记")
print("    待裁决——不自动升格——但改善 50 倍实质性")
