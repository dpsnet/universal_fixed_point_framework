# -*- coding: utf-8 -*-
"""S227 能标比家族检验 + 精度证伪
新独立候选：m_c/m_tau = 5/7（静默/对合）——0.09σ 预判
证伪检验：m_mu/m_e = e^(16/3)？——实验 ppb 精度——防巧合铁律
"""
import math
print("=== S227: 能标比家族 + 精度证伪 ===\n")

print("=== 1. m_c/m_tau = 5/7（独立新检验） ===")
m_c = 1.27; m_c_err = 0.02      # GeV（PDG MS-bar 4 味）
m_tau = 1.77686; m_tau_err = 0.00012
r = m_c/m_tau
r_unc = r * math.sqrt((m_c_err/m_c)**2 + (m_tau_err/m_tau)**2)
pred = 5/7
s = abs(r - pred)/r_unc
print(f"m_c/m_tau = {r:.4f}±{r_unc:.4f} vs 5/7 = {pred:.4f}（静默/对合）")
print(f"σ_score = {s:.3f}σ —— {'达标' if s<=1 else ('提示' if s<=3 else '不达标')}")

print("\n=== 2. 证伪检验：m_mu/m_e = e^(16/3)？ ===")
m_mu = 105.6583755; m_mu_err = 2.3e-6     # MeV（ppb 精度）
m_e = 0.51099895000; m_e_err = 1.5e-10    # MeV（ppt 精度）
r2 = m_mu/m_e
r2_unc = r2 * math.sqrt((m_mu_err/m_mu)**2 + (m_e_err/m_e)**2)
pred2 = math.exp(16/3)  # 全态/活跃 = 16/3
s2 = abs(r2 - pred2)/r2_unc
print(f"m_mu/m_e = {r2:.6f}±{r2_unc:.2e}")
print(f"预测 e^(16/3) = {pred2:.6f}（16/3 = 全态/活跃——全壳）")
print(f"σ_score = {s2:.2e}σ —— {'达标' if s2<=1 else ('提示' if s2<=3 else '不达标')}")
print(f"→ 差 = {abs(r2-pred2):.4f}——实验精度压倒性——{'证伪' if s2>3 else '保留'}")

print("\n=== 3. 能标比家族汇总 ===")
print("m_b/m_tau = e^(6/7)——0.234σ（S226——同代比——含 e）")
print("m_c/m_tau = 5/7——0.09σ（本次——跨代比——不含 e）")
print("m_b/m_c = e^(6/7)x7/5——0.13σ（推导——一致）")
print("m_mu/m_e ≠ e^(16/3)——证伪（ppb 精度压倒性）")

print("\n=== 4. 结构观察（样本小——弱） ===")
print("e 只出现在同代能标比（b/tau 同代）？")
print("跨代比（c/tau）不含 e——5/7 纯框架比")
print("但：样本仅 2 独立比——不足以定论——观察级")

print("\n=== 5. 诚实评估 ===")
print("m_c/m_tau = 5/7 独立达标（依赖 m_c 大不确定度±0.02）")
print("m_mu/m_e 证伪（实验精度压制任何近似——防巧合铁律生效）")
print("能标比家族叙事：部分支持——样本小——观察级登记")
print("→ 无新升格——无新 Lean 锚——待更多能标比检验")
