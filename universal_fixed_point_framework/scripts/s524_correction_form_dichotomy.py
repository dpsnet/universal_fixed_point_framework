# -*- coding: utf-8 -*-
"""
S524 修正形态二分判别：乘法因子型 vs 加法内嵌型（2026-10-29）
模式 8 先证伪：α 公式组装（求和）却裸精确——检验 δ* 加法内嵌修正

背景：S522 机制候选"跨层组合→修正"——但 α⁻¹ = 72+24ln15+24δ*
  = 24(3+ln15+δ*) 是求和组装（跨层组合——活跃/d_H/δ* 不同量）
  却裸精确（Cs 通道 0.02σ）——反例？

假设：α 的修正以 δ* 形式**加法内嵌**（非外乘 (1±Nσᵏ) 因子）——
  δ* 项 = 修正谱——修正形态二分：乘法因子型（8 例）/加法内嵌型（α）

检验：
  1. 无 δ* 时的 α⁻¹ = 24(3+ln15) 与实验值偏差 → δ* 项补偿
  2. δ* 项 24δ* 恰好补偿该偏差 → δ* = 加法内嵌修正
  3. δ* 幂次谱 {3,5,7,8} 与 8 例修正因子幂次对比
"""
import math
from fractions import Fraction

sigma = 1 / 15
ln15 = math.log(15)
dstar = 6*sigma**3 + 4*sigma**5 + 8*sigma**7 + 5*sigma**8

alpha_inv_V3 = 24 * (3 + ln15 + dstar)
alpha_inv_no_dstar = 24 * (3 + ln15)
alpha_exp_cs = 137.035999046  # Cs 反冲（S498——最近第三方）
dstar_contribution = 24 * dstar
deficit = alpha_exp_cs - alpha_inv_no_dstar

print("S524 修正形态二分判别：乘法因子 vs 加法内嵌（模式 8 先证伪）")
print("=" * 68)
print("① α⁻¹ 分解：")
print("   α⁻¹ = 24×(3 + ln15 + δ*) = %.12f" % alpha_inv_V3)
print("   无 δ* 项：24×(3+ln15) = %.12f" % alpha_inv_no_dstar)
print("   δ* 项贡献：24δ* = %.12f" % dstar_contribution)
print("   实验（Cs 反冲）：%.12f" % alpha_exp_cs)
print("   无 δ* 时偏差：%.12f（%.6f%%）" % (alpha_exp_cs - alpha_inv_no_dstar,
      100*(alpha_exp_cs - alpha_inv_no_dstar)/alpha_exp_cs))
print()
print("② δ* 项补偿检验：")
print("   偏差 - δ* 贡献 = %.3e" % ((alpha_exp_cs - alpha_inv_no_dstar) - dstar_contribution))
print("   → δ* 项恰好补偿无 δ* 偏差：%s" %
      ("PASS（同一量级）" if abs((alpha_exp_cs - alpha_inv_no_dstar) - dstar_contribution) < 1e-3 else "CHECK"))
print()
print("③ 修正形态二分：")
print("   乘法因子型（8 例）：(1±Nσᵏ) 外乘——单层幂次——")
print("     σ³ 族（ε_μ/公共残差/α_s/m_ρ）、σ 族（κ/观测边界/δ_hf）、σ² 族（fnp）")
print("   加法内嵌型（α）：δ* = 6σ³+4σ⁵+8σ⁷+5σ⁸ 内嵌求和——")
print("     幂次谱 {3,5,7,8}——全层谱（活跃³/静默⁵/对合⁷/k_max⁸ 层）")
print()
print("④ 判别：")
print("   α 非反例——其修正以 δ* 加法内嵌形态在场——")
print("   S522 机制扩展：跨层组合→修正（乘法因子型 或 加法内嵌型）")
print()
print("结论：修正形态二分确认——α 的 δ* 为加法内嵌修正（观察级）")
print("诚实：δ* 幂次 {3,5,7,8} 无 σ²/σ⁴/σ⁶——与 S492 σ⁴ 禁制、σ² 未用一致")
print("      '为何 α 用加法内嵌而 8 例用乘法因子'——全域 vs 域内的机制开放")
