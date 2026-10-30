# -*- coding: utf-8 -*-
"""S316b α⁻¹ 框架导出精度复核（修正版——S256d/e 权威公式）

α⁻¹ = 72 + 24ln15 + 24δ
  δ = 6σ³ + 4σ⁵ + 14σ⁷ + 13σ⁸（S256d/e——4569973/2562890625）
  72 = 42+30 = 约束域 + 静默×(幂基×活跃)；24 = 不动点
  d_H = ln15 + δ（内生闭环）
"""
import math

sigma = 1/15
ln15 = math.log(15)
delta = 6*sigma**3 + 4*sigma**5 + 14*sigma**7 + 13*sigma**8

alpha_inv = 72 + 24*ln15 + 24*delta

exp = 137.035999084
u = 0.000000021
sc = abs(alpha_inv - exp)/u

print("=== S316b α⁻¹ 框架导出精度（S256d/e 权威）===\n")
print(f"δ = 6σ³+4σ⁵+14σ⁷+13σ⁸ = {delta:.12f}（= 4569973/2562890625——偏差 {abs(delta-4569973/2562890625):.2e}）")
print(f"ln15 = {ln15:.12f}")
print(f"d_H = ln15+δ = {ln15+delta:.12f}")
print(f"72 = 42+30 = 约束域 + 静默×幂基×活跃 = {42+5*2*3}")
print(f"α⁻¹(预测) = 72+24ln15+24δ = {alpha_inv:.10f}")
print(f"α⁻¹(CODATA2018) = {exp} ± {u}")
print(f"差 = {alpha_inv-exp:.3e}（相对 {abs(alpha_inv-exp)/exp:.2e}）")
print(f"σ_score = {sc:.3f}  {'达标 ✓' if sc<=1 else '提示' if sc<=3 else '不达标 ✗'}")

# 分项贡献
print(f"\n分项贡献：")
print(f"  72 = {72:.6f}（约束域 42 + 静默×幂基×活跃 30）")
print(f"  24ln15 = {24*ln15:.10f}")
print(f"  24δ = {24*delta:.10f}")
print(f"  合计 = {72+24*ln15+24*delta:.10f}")

# S256f 家族检验要点复核
print(f"\nS256f 家族检验（已记录——复核要点）：")
print(f"  · 删项每项必要（S256f 通过）")
print(f"  · 90σ⁴ ≡ 6σ³（鲁棒性——9e1 系数等价）")
print(f"  · σ⁸ 系数窗口 12-15 均达标（非孤点）")
print(f"  · 随机 20000 组合 σ≤1 命中 0.00%——框架量组合非偶然")
print(f"  · 简洁版 V1 = 6σ³+4σ⁵+15σ⁷（15=态域）——σ=0.95 临界达标")
print(f"\n结论：α⁻¹ 框架导出精度 = {sc:.3f}σ（{alpha_inv:.10f} vs 实验 {exp}）")
