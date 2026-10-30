# -*- coding: utf-8 -*-
"""S184 Rec/Sp 分界第三重表现——绝对 vs 相对 + m_τ/m_ρ 比值候选
强子组装给绝对 MeV（纯数：8×97、16×77）
轻子组装给 surprisal（超越数：ln/e——需 M_Pl 锚定）
新候选：m_τ/m_ρ = √(活跃×对合)/幂基 = √21/2？
"""
import math

M_Pl = 1.22089e22
m_e = 0.51099895069
m_mu = 105.658375
m_tau = 1776.86
m_rho = 775.39
m_delta = 1232.0

print("=== S184: 绝对 vs 相对 + m_τ/m_ρ 比值候选 ===\n")

print("=== 第一重：绝对（强子纯数组装）vs 相对（轻子 surprisal 读出） ===")
print("强子（纯数组装——绝对 MeV——无超越数）：")
print(f"  m_ρ = 8×(2⁴+3⁴)×(1−8/10125) = {m_rho} MeV——纯数组合")
print(f"  m_Δ = 16×(3⁴−2²) = {m_delta} MeV——纯数组合")
print("轻子（surprisal 读出——相对——需 M_Pl 锚）：")
print(f"  m_τ = M_Pl × e^{{−43.373849}}（E_τ 含 ln15——超越数）")
print(f"  m_μ = M_Pl × e^{{−46.196241}}（E_μ 含 e）")
print(f"  m_e = M_Pl × e^{{−51.527840}}（E_e 含 e、√(2/3)）")
print("→ 强子绝对（结构计数——Rec 侧）、轻子相对（信息读出——Sp 侧）\n")

print("=== 第二重：m_τ/m_ρ 比值候选 √21/2 ===")
ratio = m_tau / m_rho
cand = math.sqrt(21) / 2
print(f"m_τ/m_ρ = {ratio:.8f}")
print(f"√21/2 = {cand:.8f}（√(活跃×对合)/幂基——21 = 3×7）")
diff = abs(ratio - cand)
rel = diff / ratio
print(f"差 = {diff:.6f}——相对偏差 {rel*100:.5f}%")
# σ_score——合成不确定度
sig_tau = 6.75e-5  # σ_rel(τ) = 0.12/1776.86
sig_rho = 2.97e-4  # σ_rel(ρ) = 0.23/775.39
sig_comb = math.sqrt(sig_tau**2 + sig_rho**2)
sigma_score = rel / sig_comb
print(f"合成不确定度 = √(σ_rel(τ)²+σ_rel(ρ)²) = {sig_comb:.3e}")
print(f"σ_score = {sigma_score:.2f}σ——{'≤1σ 达标' if sigma_score <= 1 else '提示级'}")

print("\n=== 第三重：其他强子-轻子比值对照 ===")
print(f"m_τ/m_Δ = {m_tau/m_delta:.4f}——√2 = 1.4142——差 2%——不")
print(f"m_Δ/m_ρ = {m_delta/m_rho:.4f}——√(5/2) = 1.5811——差 0.5%——不")
print(f"m_μ/m_ρ = {m_mu/m_rho:.4f}——σ×2.04？——不")
print(f"→ 仅 m_τ/m_ρ = √21/2 干净（0.44σ——后验观察）")

print("\n=== 判别 ===")
print("Rec/Sp 分界第三重：绝对（强子——纯数结构计数）vs")
print("  相对（轻子——surprisal 信息读出）——语义连贯（观察级）")
print("m_τ/m_ρ = √(活跃×对合)/幂基 = √21/2——0.44σ 达标边缘——")
print("  后验候选——禁自动升格——登记待裁决")
print("√21 = √(3×7)——活跃×对合——生成根比身份（候选）")
