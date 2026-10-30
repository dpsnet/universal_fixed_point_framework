# -*- coding: utf-8 -*-
"""κ 候选 σ_score 判定（2026-10-26 修正——百分比判读违规纠正）

σ_score = |预测−锚定|/合成不确定度（≤1 达标、1-3 提示、>3 不达标）
κΛ 合成不确定度 ~0.1%（Λ_QCD 实验方案依赖——L1295 κΛ 不确定度 ~0.1%）
"""
import math

dlam_p20 = (math.sqrt(3)-1)/6
kl_49a, kl_49b = 49.0039, 49.0021
kl_a, kl_b = kl_49a/dlam_p20, kl_49b/dlam_p20
kappa_a, kappa_b = kl_a/210, kl_b/210

kappa_cand = 7*(math.sqrt(3)+1)/10
kl_cand = 147*(math.sqrt(3)+1)

# 合成不确定度（相对 ~0.1%）
rel_unc = 1e-3  # κΛ 不确定度 ~0.1%

print("=== κ 候选 σ_score 判定（合成不确定度 ~0.1%）===")
for name, kl, kappa in (("A（恒等 B 49.0039）", kl_a, kappa_a),
                        ("B（登记 49.0021）", kl_b, kappa_b)):
    dev_rel = abs(kl_cand - kl)/kl
    s = dev_rel / rel_unc
    verdict = "✓ 达标" if s <= 1 else ("提示" if s <= 3 else "✗ 不达标")
    print(f"  口径 {name}：κΛ_cand = {kl_cand:.4f} vs 锚 {kl:.4f}")
    print(f"    相对差 = {dev_rel*100:.5f}%——σ_score = {dev_rel:.4f}/{rel_unc:.4f} = {s:.2f} —— {verdict}")
print()
print("κ 候选 = 对合域×(√3+1)/(幂基×静默)——σ_score 0.04~0.08（≤1 达标）")
print("——百分比判据（0.001% 级）违规——σ_score 口径下候选达标")
print()
print("=== 判别结论 ===")
print("κΛ×Δλ_P20 = 49（对合域²）精确恒等——κ 候选在 σ_score 口径达标")
print("（0.043~0.080σ_score）——'候选非锁定'表述改为'σ_score 达标候选'")
print("诚实边界：κΛ 不确定度 ~0.1% 为口径估计（Λ 实验方案依赖）；")
print("κ 生成链（为何对合域×(√3+1)/(幂基×静默)）未导出——升格仍需生成链")
