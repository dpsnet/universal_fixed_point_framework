# -*- coding: utf-8 -*-
"""S256h 框架常数幂次谱检验 + V1/V2 双口径（CODATA 2018/2022）
B/C 方向：
  B = σ 幂次取框架常数值（幂次谱 = 框架常数或其乘积）
  C = 谱按量分域（d_H 维数域用框架常数谱、修正域用 Fib 谱）
检验：① V1/V2 对 CODATA 2018/2022 双值的 σ_score
      ② 已知 σ 幂次样本全映射（框架常数谱 vs Fib 谱覆盖）
      ③ V1 幂次 {3,5,7} = 奇数域三重奏（活跃/静默/对合）
"""
from decimal import Decimal, getcontext
getcontext().prec = 40
import math

ln15 = Decimal(15).ln()
sigma = Decimal(1)/Decimal(15)
s3 = sigma**3; s5 = sigma**5; s7 = sigma**7; s8 = sigma**8

# α⁻¹ = 72 + 24ln15 + 24δ（72 = 42+30、24 = 4!）
base = 72 + 24*ln15
V1_d = 6*s3 + 4*s5 + 15*s7
V2_d = 6*s3 + 4*s5 + 14*s7 + 13*s8
alpha_V1 = base + 24*V1_d
alpha_V2 = base + 24*V2_d

print("=== S256h: 框架常数幂次谱 + 双口径 ===")
print(f"base = 72+24ln15 = {float(base):.10f}")
print(f"V1 δ = 6σ³+4σ⁵+15σ⁷ = {float(V1_d):.12f}")
print(f"V2 δ = 6σ³+4σ⁵+14σ⁷+13σ⁸ = {float(V2_d):.12f}")
print(f"α⁻¹_V1 = {float(alpha_V1):.10f}")
print(f"α⁻¹_V2 = {float(alpha_V2):.10f}")

# CODATA 2018 / 2022
data = {
    "CODATA 2018": (Decimal("137.035999084"), Decimal("0.000000021")),
    "CODATA 2022": (Decimal("137.035999177"), Decimal("0.000000021")),
}
print("\n--- V1/V2 双口径 σ_score ---")
for name, (val, unc) in data.items():
    s1 = abs(alpha_V1 - val)/unc
    s2 = abs(alpha_V2 - val)/unc
    print(f"{name} α⁻¹ = {val}±{unc}:")
    print(f"  V1（6σ³+4σ⁵+15σ⁷）: σ = {float(s1):.3f}（{'达标' if s1<=1 else '提示' if s1<=3 else '不达标'}）")
    print(f"  V2（6σ³+4σ⁵+14σ⁷+13σ⁸）: σ = {float(s2):.3f}（{'达标' if s2<=1 else '提示' if s2<=3 else '不达标'}）")

print("\n--- ① 已知 σ 幂次样本全映射 ---")
# 已知使用：σ³（S121 强子端）、σ⁵（I_μ 2σ⁵ S173）、σ⁸（S116 2σ⁸(1+σ)）
# V1 候选：σ⁷（d_H δ）
samples = {3: "S121 强子端 σ³", 5: "S173 I_μ 2σ⁵", 8: "S116 2σ⁸(1+σ)", 7: "V1 d_H δ σ⁷"}
fib = {1, 2, 3, 5, 8, 13}
# 框架常数谱：幂次数值 = 框架常数值或其乘积
fc_vals = {2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 20, 21, 24, 25, 30, 32, 42}
print(f"{'幂次':<5}{'样本':<22}{'Fib 谱':<8}{'框架常数谱':<12}{'框架常数身份'}")
for p, desc in sorted(samples.items()):
    in_fib = p in fib
    in_fc = p in fc_vals
    ident = {2:"幂基", 3:"活跃", 4:"不动点", 5:"静默", 6:"幂基×活跃", 7:"对合",
             8:"幂基×不动点/幂基³", 10:"幂基×静默", 12:"活跃×不动点", 14:"幂基×对合",
             15:"态域", 16:"全态", 20:"不动点×静默", 24:"不动点!", 42:"约束域"}.get(p, "?")
    print(f"{p:<5}{desc:<22}{'✓' if in_fib else '✗':<8}{'✓' if in_fc else '✗':<12}{ident}")

print("\n--- ② 覆盖统计 ---")
print(f"Fib 谱覆盖：{sum(1 for p in samples if p in fib)}/4（σ⁷ 违规）")
print(f"框架常数谱覆盖：{sum(1 for p in samples if p in fc_vals)}/4（全覆盖）")

print("\n--- ③ V1 幂次 {3,5,7} = 奇数域三重奏 ---")
print("3 = 活跃（梅森 2²−1）、5 = 静默（费马 2²+1）、7 = 对合（梅森 2³−1）")
print("→ 三个奇数域框架常数——在收缩谱上的'域常数响应'")
print("→ 15σ⁷ 的 15 = 态域——'态域在对合层响应'")

print("\n--- ④ 分域假说（C）---")
print("d_H 维数域：σ 幂次 = 框架常数值（{3,5,7}——奇数域三重奏）")
print("其他修正域：Fib 谱（{3,5,8}——历史 9 样本）")
print("判别样本：σ⁷——Fib 谱无、框架常数谱有（对合）")
print("→ 若 V1 成立——σ⁷ 成为'分域'证据——Fib 谱限定修正域")
