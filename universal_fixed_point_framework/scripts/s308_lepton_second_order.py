# -*- coding: utf-8 -*-
"""S308 轻子端二阶修正项机制导出——前置数值核算（2026-10-28）

目标：m_e/m_μ 闭合链中 +(5/2)e⁻¹⁸ 二阶修正（I_e_next = I_e+5/2·e⁻¹⁸）的
机制导出前置核算：
  ① 当前闭合 σ_score（含修正）复核
  ② 无修正时 σ_score（修正必要性）
  ③ (5/2)e⁻¹⁸ 的框架分解候选（指数 18、系数 5/2）
"""
import numpy as np

# ===== 框架常数 =====
Ngen, Kmax, Powers = 3, 8, 2
SilenceUnit, Involution, FixedPoint = 5, 7, 4
Sigma = 1/15
e = np.e
pi = np.pi

# ===== 轻子端现行公式（S288）=====
alpha_vp = 16/15 + np.sqrt(2/3)*(1 + 6*Sigma**3)
I_e = 3*e - Sigma**3*(1 + alpha_vp)
I_mu = e + 42*e**(-6) + 2*Sigma**5
I_e_next = I_e + (5/2)*e**(-18)          # S269b 修正候选
corr_19 = 27/80 * e**(-19)                # S274：E_e_final = E_tau^D+I_e_next-27/80·e⁻¹⁹

print("=== S308 轻子端二阶修正核算 ===\n")
print(f"α_v'   = {alpha_vp:.12f}")
print(f"I_e    = {I_e:.12f}")
print(f"I_μ    = {I_mu:.12f}")
print(f"I_e_next = {I_e_next:.12f}")
print(f"修正项 (5/2)e⁻¹⁸ = {(5/2)*e**(-18):.12e}")

# ===== ① 含修正闭合（E_e-E_μ = I_e_next-I_μ-27/80·e⁻¹⁹）=====
dE_w = I_e_next - I_mu - corr_19      # E_e - E_μ（加权）
ratio_w = np.exp(-dE_w)
# 实验（PDG 2024）：m_e=0.51099895000(15) MeV、m_μ=105.6583755(23) MeV
m_e_exp, m_mu_exp = 0.51099895000, 105.6583755
u_me, u_mmu = 0.00000000015, 0.00000023
ratio_exp = m_e_exp/m_mu_exp
u_ratio = ratio_exp * np.sqrt((u_me/m_e_exp)**2 + (u_mmu/m_mu_exp)**2)
print(f"\n① 含修正：dE = {dE_w:.12f}  预测 m_e/m_μ = {ratio_w:.12f}")
print(f"   实验     = {ratio_exp:.12f} ± {u_ratio:.3e}")
sigma_w = abs(ratio_w - ratio_exp)/u_ratio
print(f"   σ_score = {sigma_w:.4f}  {'达标(≤1σ)' if sigma_w <= 1 else '提示(1-3σ)' if sigma_w <= 3 else '不达标(>3σ)'}")

# ===== ② 无修正（I_e 直接）=====
dE_wo = I_e - I_mu - corr_19
ratio_wo = np.exp(-dE_wo)
sigma_wo = abs(ratio_wo - ratio_exp)/u_ratio
print(f"\n② 无修正：dE = {dE_wo:.12f}  预测 = {ratio_wo:.12f}")
print(f"   σ_score = {sigma_wo:.4f}")
print(f"   修正必要性：{(5/2)*e**(-18):.3e} 相对比值效应 {abs(ratio_w-ratio_wo):.3e}")

# ===== ③ (5/2)e⁻¹⁸ 框架分解候选 =====
print("\n③ (5/2)e⁻¹⁸ 框架分解候选（先证伪角度）：")
cand = {
    "静默/幂基 × e^-(全态+幂基)": SilenceUnit/Powers * np.exp(-(16+2)),
    "SigmaInv/6 × e^-18": 15/6 * np.exp(-18),
    "全态-活跃=13? no 5=静默": (16-11)*np.exp(-18),
    "k_max·(2/8)?" : Kmax*np.exp(-18)/4,
}
for k, v in cand.items():
    print(f"  {k}: {v:.6e}  差 {(5/2)*e**(-18)-v:.2e}")

print("\n★ 指数 18 的框架分解：")
print(f"  18 = 16+2 = 全态(2⁴)+幂基(2) = 2·9 = 2·3²")
print(f"  18 = 24-6 = 4!-活跃 = 42-24? 18 = 42-24")
print(f"  18 = 2·k_max+2 = 2·8+2——幂基×k_max+幂基")
print(f"  18 = 静默+活跃+幂基+8 = 5+3+2+8? = 18 ✓")
print(f"  系数 5/2 = 静默(5)/幂基(2) = 2.5")
