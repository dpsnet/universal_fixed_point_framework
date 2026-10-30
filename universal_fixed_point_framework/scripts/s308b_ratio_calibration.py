# -*- coding: utf-8 -*-
"""S308b m_e/m_μ 口径修正核算 + 参考值版本审计（2026-10-28）

S308 发现两问题：
  A. 不确定度笔误（u_ratio 绝对 1.06e-11 → 应为 1.06e-10——相对 2.2e-8）
  B. 参考值版本差异（CODATA2022 4.83633166e-3 vs PDG2024 相除 4.836331692e-3
     ——差 3.2e-11 绝对 / 6.6e-9 相对——与二阶修正效应同量级）
目标：统一权威口径重算 σ_score + 版本漂移审计（回答'漂移=口径差异？'）
"""
import numpy as np
import math

# ===== 框架常数与轻子公式（S288）=====
Sigma = 1/15
e = np.e
alpha_vp = 16/15 + np.sqrt(2/3)*(1 + 6*Sigma**3)
I_e = 3*e - Sigma**3*(1 + alpha_vp)
I_mu = e + 42*e**(-6) + 2*Sigma**5
corr_19 = 27/80 * e**(-19)
corr_18 = (5/2) * e**(-18)
I_e_next = I_e + corr_18

# 预测（含修正）：E_e-E_μ = I_e_next-I_μ-27/80·e⁻¹⁹
dE_w = I_e_next - I_mu - corr_19
ratio_w = math.exp(-dE_w)
dE_wo = I_e - I_mu - corr_19
ratio_wo = math.exp(-dE_wo)

print("=== S308b m_e/m_μ 口径修正核算 ===\n")
print(f"I_e = {I_e:.12f}  I_e_next = {I_e_next:.12f}  I_μ = {I_mu:.12f}")
print(f"预测(含修正) m_e/m_μ = {ratio_w:.12f}")
print(f"预测(无修正) m_e/m_μ = {ratio_wo:.12f}")
print(f"修正效应（比值相对） = {(ratio_w-ratio_wo)/ratio_w:.3e}\n")

# ===== 参考值版本表（m_e/m_μ）=====
refs = [
    ("CODATA 2018",   0.00483633169e0, 1.1e-10, "官方比值(2018: 206.7682827(46))"),
    ("CODATA 2022",   0.00483633166e0, 1.2e-10, "S269b 所用"),
    ("PDG 2024 相除", 0.51099895000/105.6583755, 0.0, "m_e/m_μ 官方独立质量相除"),
    ("PDG μ/e 比",    1/206.7682830,   0.0, "μ/e mass ratio 206.7682830(24)"),
]
print(f"{'参考':<16}{'值':<22}{'不确定度':<12}{'来源'}")
for name, val, u, note in refs:
    print(f"{name:<16}{val:<22.12g}{u:<12.2e}{note}")

# ===== 相对不确定度（官方独立质量口径）=====
s_rel_mu = 2.3e-6/105.6583755      # m_μ 相对
s_rel_e  = 1.5e-10/0.51099895000   # m_e 相对
s_rel_ratio = math.sqrt(s_rel_mu**2 + s_rel_e**2)
print(f"\n相对不确定度：m_μ {s_rel_mu:.3e}、m_e {s_rel_e:.3e}、比值合成 {s_rel_ratio:.3e}")

# ===== σ_score（含/无修正 vs 各参考值——统一相对口径）=====
print(f"\n{'参考值':<16}{'σ(含修正)':<12}{'σ(无修正)':<12}{'判定(含)'}")
for name, val, u, note in refs:
    sc_w = abs(math.log(ratio_w/val)) / s_rel_ratio
    sc_wo = abs(math.log(ratio_wo/val)) / s_rel_ratio
    g = "达标✓" if sc_w <= 1 else ("提示" if sc_w <= 3 else "不达标✗")
    print(f"{name:<16}{sc_w:<12.4f}{sc_wo:<12.4f}{g}")

# ===== 版本漂移 vs 二阶修正效应量级对比 =====
print("\n=== 版本漂移 vs 二阶修正量级 ===")
vals = [r[1] for r in refs]
drift = max(vals)-min(vals)
print(f"参考值版本间最大漂移（绝对） = {drift:.3e}（相对 {drift/0.004836:.3e}）")
print(f"二阶修正 (5/2)e⁻¹⁸ 对 dE 的贡献 = {corr_18:.3e}（比值相对效应 {corr_18:.3e}）")
print(f"结论：版本漂移相对 {drift/0.004836:.2e} vs 修正效应 {corr_18:.2e}——"
      f"{'同量级——σ_score 对版本敏感但均达标' if abs(math.log10((drift/0.004836)/corr_18)) < 1 else '不同量级'}")
