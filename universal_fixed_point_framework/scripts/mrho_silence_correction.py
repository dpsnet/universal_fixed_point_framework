# -*- coding: utf-8 -*-
"""m_ρ 链静默族修正候选验证（2026-10-26）

候选：m_ρ = 2M_ud_eff×(1 − σ³×k_max×N_gen⁻¹)
σ³×k_max×N_gen⁻¹ = N_gen⁻³×静默⁻³×k_max×N_gen⁻¹ = N_gen⁻⁴×静默⁻³×k_max
= 8/10125 = 7.9012e-4（0.079%）
——静默族修正第三链候选（强子扇区第一处）
"""
import math

n_gen, silence, powers = 3, 5, 2
kmax = powers**n_gen  # 8
sigma = 1/(n_gen*silence)  # 1/15

m_rho_exp = 775.26
m_ud_eff = 387.94  # P7-6 判别口径
m_rho_rel = 0.03/775.26  # 保守 4e-5

# 失配率
m_rho_pred = 2*m_ud_eff
mismatch = (m_rho_pred - m_rho_exp)/m_rho_exp
print("=== m_ρ 链原始失配 ===")
print(f"m_ρ_pred = 2×387.94 = {m_rho_pred} vs 实验 {m_rho_exp}")
print(f"失配率 = {mismatch*100:.4f}%")
print(f"σ_score = |失配|/相对精度 = {abs(mismatch)/m_rho_rel:.1f}")
print()

# 静默族修正候选
corr = sigma**3 * kmax / n_gen
print("=== 静默族修正候选 ===")
print(f"σ³×k_max×N_gen⁻¹ = (1/{n_gen**3*silence**3})×{kmax}/{n_gen} = 8/10125 = {corr:.7f}")
print(f"= {corr*100:.4f}%")
print(f"幂次分解：N_gen⁻⁴×静默⁻³×k_max（幂和 −3−4+1 = −6 = σ³ 幂和 −6 + 系数幂和 0）")
print(f"失配率 {mismatch*100:.4f}% vs 修正量 {corr*100:.4f}%——差 {abs(mismatch-corr)/corr*100:.2f}%")
print()

# 修正后
resid = mismatch - corr
print("=== 修正后 σ_score ===")
print(f"残余 = {resid:.7f}（{resid*100:.4f}%）")
print(f"σ_score = |{resid:.7f}|/{m_rho_rel:.2e} = {abs(resid)/m_rho_rel:.2f}")
print(f"达标判定: {'✓ 达标' if abs(resid)/m_rho_rel <= 1 else '✗ 不达标'}")
print()

# 也检验 M_ud_eff 修正形态（组分夸克质量）
print("=== M_ud_eff 修正形态 ===")
print(f"M_ud_eff 原始 = {m_ud_eff}")
print(f"修正后 M_ud_eff' = M_ud_eff×(1−修正) = {m_ud_eff*(1-corr):.4f}")
print(f"m_ρ' = 2×{m_ud_eff*(1-corr):.4f} = {2*m_ud_eff*(1-corr):.2f} vs 实验 {m_rho_exp}")
print(f"修正后失配 = {(2*m_ud_eff*(1-corr)-m_rho_exp)/m_rho_exp*100:.4f}%")
print()

# 幂和谱核对
print("=== 修正域幂和谱（扩展）===")
items = [
    ("σ",            (-1, -1, 0), -2,  "加性"),
    ("静默⁻²",        (-2, 0, 0), -2,  "加性"),
    ("Δ_dress",      (-1, -2, 1), -2,  "加性"),
    ("6σ³",          (-3, -2, 1), -4,  "因子"),
    ("σ³×k_max×N_gen⁻¹", (-3, -4, 1), -6, "因子（m_ρ 候选）"),
]
print(f"{'量':<20} {'(a,b,c)':<14} {'幂和':<6} 形态")
for name, (a, b, c), psum, form in items:
    print(f"{name:<20} ({a},{b},{c})".ljust(38) + f"{psum:<6} {form}")
print()
print("规律：修正量幂和 = 主体 σ^n 幂和（−2n）+ 系数幂和")
print("  m_ρ 候选：σ³ 幂和 −6 + 系数 k_max×N_gen⁻¹（幂和 0）→ −6 ✓")
