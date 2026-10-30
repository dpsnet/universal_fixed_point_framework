# -*- coding: utf-8 -*-
"""S220 alpha_s 跨家族/能标检验（S218 裁决执行——用户同意）
alpha_s 多能标 vs 框架候选——σ_score 判定
"""
import math
print("=== S220: alpha_s 能标检验 ===\n")

# PDG 2024 alpha_s 多能标（世界平均）
scales = [
    # (能标, alpha_s, 不确定度, 来源)
    ("M_Z = 91.19 GeV", 0.1181, 0.0011, "PDG 世界平均"),
    ("m_b = 4.18 GeV", 0.224, 0.008, "PDG——4 味/γ* 平均"),
    ("m_tau = 1.777 GeV", 0.318, 0.011, "PDG——tau 衰变"),
]

cands = [
    ("Sigma/M(7)", 15/127, "15/127 = 0.118110"),
    ("幂基/活跃²", 2/9, "2/9 = 0.222222"),
    ("1/sqrt(静默x幂基)", 1/math.sqrt(10), "1/sqrt(10) = 0.316228"),
]

print("=== 能标 x 候选矩阵 ===")
print(f"{'能标':<20}{'实验':<10}{'候选':<22}{'预测':<14}{'σ_score':<10}判定")
for name, exp, unc, src in scales:
    best = None
    for cn, cv, _ in cands:
        score = abs(exp - cv)/unc
        status = "达标" if score<=1 else ("提示" if score<=3 else "不达标")
        if best is None or score < best[1]:
            best = (cn, cv, score, status)
    cn, cv, score, status = best
    print(f"{name:<20}{exp:<10}{cn:<22}{cv:<14}{score:<10.3f}{status}")

print("\n=== 能标依赖结构 ===")
print("M_Z（最高）→ Sigma/M(7) = 0.1181（0.009σ）")
print("m_b（中）→ 幂基/活跃² = 0.2222（0.22σ）")
print("m_tau（低）→ 1/sqrt(10) = 0.3162（0.16σ）")
print("单调性：0.118 < 0.222 < 0.316——能标降、alpha_s 升——自洽 ✓")

print("\n=== 诚实评估 ===")
print("三能标三候选全达标（0.009σ/0.22σ/0.16σ）——单调性自洽")
print("但：公式不统一（每能标一个独立公式）——统一性弱")
print("后验候选（无先验预测）——家族公式无递推结构")
print("  → 观察级登记——不升格")
print("  → 结构证据：'能标-公式'配对与能标序一致——但机制开放")

print("\n=== 审计结论 ===")
print("alpha_s 能标检验：三能标命中（15/127、2/9、1/sqrt(10)）")
print("  单调性自洽 + 全壳组件——'框架量的能标谱'候选")
print("  公式统一性开放（三公式无递推）——长期攻坚")
