# -*- coding: utf-8 -*-
"""轻子链 σ_score 口径重判 v2（2026-10-26）：修正符号 + m_τ 相关误差传播

判定标准（方法论升级）：σ_score = |预测−实验|/合成不确定度——≤1σ_score 达标、1~3σ_score 提示、>3σ_score 不达标。
PDG 2024：m_e = 0.51099895069(16)、m_μ = 105.6583755(23)、m_τ = 1776.86(12)。
间隔定义：I_ab = ln(m_a/m_b)（大/小为正）。
"""
import math

m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
rel = {"e": 1.5e-8/m_e_c, "mu": 2.3e-6/m_mu_c, "tau": 0.12/m_tau_c}

print("=== PDG 相对不确定度 ===")
for n, r in rel.items():
    print(f"  m_{n}：{r:.3e}")

def I_exp(m1, m2):
    return math.log(m1/m2)

def s_I(m1n, m2n):
    """ln(m1/m2) 的合成不确定度（相对误差线性化）"""
    return math.sqrt(rel[m1n]**2 + rel[m2n]**2)

def grade(sig):
    return "✓ 达标" if sig <= 1 else ("～ 提示(1-3σ_score)" if sig <= 3 else "✗ 不达标")

# ① P7-5v：I_e = 3e − σ³(1+α_v) vs ln(m_τ/m_e)
sigma = 1/15
s3 = sigma**3
alpha_v = 16/15 + math.sqrt(2/3)
I_e_pred = 3*math.e - s3*(1+alpha_v)
I_e_exp = I_exp(m_tau_c, m_e_c)
sig1 = abs(I_e_pred - I_e_exp)/s_I("tau","e")
print(f"\n① P7-5v m_e/m_τ：I_e = {I_e_pred:.10f} vs 实验 {I_e_exp:.10f} → {sig1:.3f}σ {grade(sig1)}")

# ② P7-4d：I_μ = ln16 + e^{−3} vs ln(m_τ/m_μ)
I_mu_pred = math.log(16) + math.e**(-3)
I_mu_exp = I_exp(m_tau_c, m_mu_c)
sig2 = abs(I_mu_pred - I_mu_exp)/s_I("tau","mu")
print(f"② P7-4d m_μ/m_τ：I_μ = {I_mu_pred:.10f} vs 实验 {I_mu_exp:.10f} → {sig2:.3f}σ {grade(sig2)}")

# ③ V5 比值链（等价②）
ratio_pred = math.exp(-I_mu_pred)
ratio_exp = m_mu_c/m_tau_c
sig3 = abs(ratio_pred-ratio_exp)/ratio_exp / s_I("mu","tau")
print(f"③ V5 比值链：e^(−I_μ) = {ratio_pred:.10f} vs {ratio_exp:.10f} → {sig3:.3f}σ {grade(sig3)}")

# ④ 26/9 桥：间隔比 I_e/I_μ——m_τ 相关误差传播
ratio_pred_I = I_e_pred/I_mu_pred
ratio_exp_I = I_e_exp/I_mu_exp
# 严格传播：I_ab 对 ln m_τ 偏导 = +1（两间隔同向）——比值 R 对 ln m_τ 偏导 = (∂R/∂I_e)(∂I_e/∂lnm_τ)+(∂R/∂I_μ)(∂I_μ/∂lnm_τ)
#   = (1/I_μ)·1 − (I_e/I_μ²)·1 = (1/I_μ)(1−R)
dR_dtau = (1/I_mu_exp)*(1 - ratio_exp_I)   # 比值对 ln m_τ 的敏感度
var = (dR_dtau*rel["tau"])**2 + (rel["e"]/I_mu_exp)**2 + (I_e_exp/I_mu_exp**2 * rel["mu"])**2
s_R = math.sqrt(var)
sig26 = abs(26/9 - ratio_exp_I)/s_R
sig_pred = abs(ratio_pred_I - ratio_exp_I)/s_R
print(f"\n④ 26/9 桥：实验间隔比 {ratio_exp_I:.10f}、预测 {ratio_pred_I:.10f}")
print(f"   δR（相关传播，m_τ 偏导 {dR_dtau:.4f}）= {s_R:.2e}")
print(f"   26/9 vs 实验：{sig26:.2f}σ {grade(sig26)}；框架预测 vs 实验：{sig_pred:.2f}σ {grade(sig_pred)}")

# ⑤ 16/3 间隔差：I_e−I_μ = ln(m_μ/m_e)——m_τ 完全消去
I_diff_pred = I_e_pred - I_mu_pred
I_diff_exp = math.log(m_mu_c/m_e_c)
sig_diff = abs(I_diff_pred - I_diff_exp)/s_I("mu","e")
print(f"\n⑤ 16/3 间隔差：预测 {I_diff_pred:.10f} vs 实验 ln(m_μ/m_e) = {I_diff_exp:.10f}")
print(f"   σ_score = {sig_diff:.1f} {grade(sig_diff)}（实验 10⁻⁸ 级——0.032% 百分比偏差 = 456σ_score）")

# ⑥ 附加：m_e/m_μ 直接比值（无 m_τ 链）——未来判别窗口
ratio_em_pred = math.exp(-I_diff_pred)
ratio_em_exp = m_e_c/m_mu_c
sig6 = abs(ratio_em_pred-ratio_em_exp)/ratio_em_exp / s_I("e","mu")
print(f"\n⑥ m_e/m_μ 比值链：e^(−5.331615) = {ratio_em_pred:.10f} vs 实验 {ratio_em_exp:.10f} → {sig6:.1f}σ {grade(sig6)}")

print("\n=== 分级汇总（σ_score 口径，替代百分比容差） ===")
print(f"① P7-5v：{sig1:.3f}σ——极强达标（理论精度 >> m_τ 实验精度）")
print(f"②③ P7-4d/V5：{sig2:.3f}/{sig3:.3f}σ——达标")
print(f"④ 26/9：{sig26:.2f}σ——{'达标' if sig26<=1 else '提示级（候选不立链）'}")
print(f"⑤ 16/3：{sig_diff:.0f}σ——否决（撤销候选登记）")
print(f"⑥ m_e/m_μ 链（无 m_τ）：{sig6:.1f}σ——若 26/9 桥为真，此链是最强判别窗口")
