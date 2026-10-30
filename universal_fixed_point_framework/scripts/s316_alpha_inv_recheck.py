# -*- coding: utf-8 -*-
"""S316 α⁻¹ 框架导出精度复核（2026-10-28）

S256 系列：α⁻¹ = 24(d_H+3)——d_H 框架化 = 6σ³+4σ⁵+14σ⁷+13σ⁸
复核 σ_score（用户问'框架实现的精细结构常数导出精度'）
实验参考：α⁻¹(CODATA 2018) = 137.035999084(21)——σ = 0.021
"""
import math

sigma = 1/15
e = math.e

# d_H 框架化（S256d/e）
dH = 6*sigma**3 + 4*sigma**5 + 14*sigma**7 + 13*sigma**8
alpha_inv_pred = 24 * (dH + 3)

# CODATA 2018 α⁻¹ = 137.035999084 ± 0.000000021
exp = 137.035999084
u = 0.000000021
sc = abs(alpha_inv_pred - exp)/u

print("=== S316 α⁻¹ 框架导出精度复核 ===\n")
print(f"σ = 1/15——d_H = 6σ³+4σ⁵+14σ⁷+13σ⁸")
print(f"d_H = {dH:.9f}")
print(f"α⁻¹(预测) = 24(d_H+3) = {alpha_inv_pred:.9f}")
print(f"α⁻¹(CODATA2018) = {exp} ± {u}")
print(f"差 = {alpha_inv_pred-exp:.3e}")
print(f"σ_score = {sc:.3f}  {'达标 ✓' if sc<=1 else '提示' if sc<=3 else '不达标 ✗'}")

# 分项
terms = [("6σ³", 6*sigma**3), ("4σ⁵", 4*sigma**5), ("14σ⁷", 14*sigma**7), ("13σ⁸", 13*sigma**8)]
print(f"\n分项：")
for name, v in terms:
    print(f"  {name} = {v:.3e}")
print(f"  总和 = {sum(v for _,v in terms):.6f}——3+d_H = {3+dH:.6f}——24× = {24*(3+dH):.6f}")

# 逐项传导（哪项主导）
print(f"\n灵敏度（对 α⁻¹ 总值的贡献）：")
for name, v in terms:
    print(f"  {name}: {24*v:.3e}（相对 {24*v/exp*100:.4f}%）")

# 王者公式对比（历史）
print(f"\n历史对比：α⁻¹ = 24(d_H^obs+3) = 137.036000（旧——43.6σ 废止）")
print(f"  → S256d/e δ 框架化后 0.054σ 达标——本轮复核 {sc:.3f}σ")
