# -*- coding: utf-8 -*-
"""S156 I_μ 新基底扫描（e 幂×框架有理——S145 同族基底）
I_μ = E_μ − E_τ = 2.8223920247（μ-τ 荷间隔——观测嵌入 S144 证伪旧基底）
σ_score 口径：I_μ 误差 τ 主导——σ_rel(τ) = 6.75e-5（PDG 2024 m_τ=1776.86(12)）
达标：|pred − I_μ| ≤ 6.75e-5（1σ）
"""
import math

I_mu = 2.8223920247
sigma_rel = 6.75e-5
e = math.e
ln15 = math.log(15)
ln1615 = math.log(16/15)

print("=== S156: I_μ 新基底扫描（e 幂×框架有理） ===\n")
print(f"I_μ = {I_mu:.10f}（E_μ−E_τ——μ-τ 荷间隔）")
print(f"σ_score 口径：σ_rel(τ) = {sigma_rel:.2e}——1σ 达标窗口 ±{sigma_rel:.2e}\n")

# 候选主项 + 修正（e^{−n} × 框架有理）
print("=== 1. 主项 e + 修正 c·e^{−n}（框架有理 c ∈ {27/80, 2/75, 42, 15, 8, 5, 3, 7, 16}） ===")
delta1 = I_mu - e
print(f"δ₁ = I_μ − e = {delta1:.10f}")
for n in range(2, 15):
    for c in [42, 15, 16, 8, 5, 3, 7, 2, 27/80, 2/75, 144, 2*3*7, 3*5, 3*14]:
        cand = e + c * math.exp(-n)
        diff = abs(cand - I_mu)
        if diff < 1e-4:
            score = diff / sigma_rel
            print(f"  e + {c:.4f}·e^{{-{n}}} = {cand:.10f}  差 {diff:.2e}  σ_score {score:.3f}")

print("\n=== 2. 主项 ln15 + 修正 ===")
delta2 = I_mu - ln15
print(f"δ₂ = I_μ − ln15 = {delta2:.10f}")
for n in range(2, 15):
    for c in [42, 15, 16, 8, 5, 3, 7, 2, 27/80, 2/75, 144]:
        cand = ln15 + c * math.exp(-n)
        diff = abs(cand - I_mu)
        if diff < 1e-4:
            score = diff / sigma_rel
            print(f"  ln15 + {c:.4f}·e^{{-{n}}} = {cand:.10f}  差 {diff:.2e}  σ_score {score:.3f}")

print("\n=== 3. 主项 2√2 + 修正 ===")
delta3 = I_mu - 2*math.sqrt(2)
print(f"δ₃ = I_μ − 2√2 = {delta3:.10f}")
for n in range(2, 15):
    for c in [42, 15, 16, 8, 5, 3, 7, 2, 27/80, 2/75, 144]:
        cand = 2*math.sqrt(2) + c * math.exp(-n)
        diff = abs(cand - I_mu)
        if diff < 1e-4:
            score = diff / sigma_rel
            print(f"  2√2 + {c:.4f}·e^{{-{n}}} = {cand:.10f}  差 {diff:.2e}  σ_score {score:.3f}")

print("\n=== 4. δ₁ 的精确分解（e 幂 × 框架有理——S145 同族基底） ===")
for n in range(3, 16):
    ratio = delta1 / math.exp(-n)
    # 检查 ratio 是否接近框架有理（<0.1% 级）
    for target in [42, 40, 44, 43, 41, 45, 15*3, 14*3, 7*6, 2*21, 3*14, 27*3/2, 16*3-6]:
        if abs(ratio - target) / target < 1e-3:
            print(f"  δ₁/e^{{-{n}}} = {ratio:.6f} ≈ {target}（差 {abs(ratio-target)/target:.2e}）——候选 {target}·e^{{-{n}}}")

print("\n=== 5. 候选判定 ===")
cand = e + 42 * math.exp(-6)
diff = abs(cand - I_mu)
score = diff / sigma_rel
print(f"候选：I_μ = e + 42·e^{{-6}} = {cand:.10f}")
print(f"  I_μ(obs) = {I_mu:.10f}")
print(f"  差 = {diff:.3e}  相对差 = {diff/I_mu:.2e}  σ_score = {score:.3f}")
print(f"  42 = 约束域（S152——幂基×活跃代×对合 = 2×3×7）")
print(f"  6 = 幂基×活跃代（2×3）——e^{{-6}} = e^{{−(2×3)}}——约束域 6 步衰减")
print(f"  {'达标（≤1σ）' if score <= 1 else '不达标'}——登记候选（后验——非预测——待验证）")
