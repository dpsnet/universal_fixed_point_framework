# -*- coding: utf-8 -*-
"""E_τ/δ 链 σ_score 口径重审计（2026-10-26）：M_Pl 误差传播 + 分级

口径：
  E_τ^new = 16·ln15 + (7/10)·ln(16/15) = 43.373980182（#74 候选）
  E_exp = ln(M_Pl/m_τ)——M_Pl = √(ħc/G_N)——δM_Pl/M_Pl = ½·δG_N/G_N
  CODATA 2024：G_N 相对不确定度 2.2e-5 → δM_Pl/M_Pl ≈ 1.1e-5
  PDG 2024：m_τ = 1776.86(12) → 相对 6.75e-5（主导）
"""
import math

m_tau_c = 1776.86
d_tau_rel = 0.12/m_tau_c          # 6.75e-5
G_N_rel = 2.2e-5                  # CODATA 2024
M_Pl_rel = G_N_rel/2              # δM_Pl/M_Pl = ½δG_N/G_N
M_Pl_MeV = 1.220890e22            # 谱定 M_Pl（MeV）

def grade(sig):
    return "✓ 达标" if sig <= 1 else ("～ 提示(1-3σ_score)" if sig <= 3 else "✗ 不达标")

# ---- ① E_τ^new（#74）σ_score 审计 ----
E_pred = 16*math.log(15) + (7/10)*math.log(16/15)
E_exp = math.log(M_Pl_MeV/m_tau_c)
sE = math.sqrt(M_Pl_rel**2 + d_tau_rel**2)
sigE = abs(E_pred - E_exp)/sE
print("=== ① E_τ^new = 16·ln15+(7/10)·ln(16/15) ===")
print(f"E_pred = {E_pred:.10f}、E_exp = ln(M_Pl/m_τ) = {E_exp:.10f}")
print(f"δE（M_Pl 1.1e-5 ⊕ m_τ 6.75e-5）= {sE:.2e} → σ_score = {sigE:.3f} {grade(sigE)}")
print(f"  相对偏差 {(E_pred-E_exp)/E_exp*100:+.4f}%（展示用，非判定）")
print()

# ---- ② δ 资格（P7-5c 展开链）σ_score 审计 ----
# δ 的"实验目标"：δ_target = (E_exp − ln(2^64) + (47/3)ln(16/15))/16
# 框架 δ_cand = d_H − ln15 = 16259/6000 − ln15
dH = 16259/6000
delta_cand = dH - math.log(15)
delta_target = (E_exp - 64*math.log(2) + (47/3)*math.log(16/15))/16
s_delta = sE/16        # δ 从 E 反解：16δ → δ 误差 = δE/16
sigD = abs(delta_cand - delta_target)/s_delta
print("=== ② δ 候选（16259/6000−ln15）σ_score 审计 ===")
print(f"δ_cand = {delta_cand:.10f}、δ_target（E_exp 反解）= {delta_target:.10f}")
print(f"δE = δE/16 = {s_delta:.2e} → σ_score = {sigD:.3f} {grade(sigD)}")
print(f"  差 {delta_cand-delta_target:+.3e}——百分比 {(delta_cand-delta_target)/delta_target*100:+.2f}%（展示）")
print()

# ---- ③ 16/15 桥 vs (7/10) 系数（#74 的结构判别） ----
# E_τ^new 的 (7/10) = 0.7 vs P7-5c 的 1/3——(7/10−1/3) = 11/30
coef = 7/10
print("=== ③ #74 vs P7-5c 系数判别（σ_score 口径） ===")
E_p75c = 16*dH + math.log(16/15)/3
print(f"P7-5c 口径 E = 16·dH + ln(16/15)/3 = {E_p75c:.10f}")
print(f"  vs E_exp = {E_exp:.10f}：σ_score = {abs(E_p75c-E_exp)/sE:.3f} {grade(abs(E_p75c-E_exp)/sE)}")
print(f"#74 口径 E = {E_pred:.10f}：σ_score = {sigE:.3f}——{ '✓ #74 优' if sigE < abs(E_p75c-E_exp)/sE else 'P7-5c 优' }")
print()

# ---- ④ 追加：m_τ 绝对链（谱定 M_Pl → m_τ = M_Pl·e^{−E_τ^new}） ----
m_tau_pred = M_Pl_MeV*math.exp(-E_pred)
sig_mtau = abs(m_tau_pred - m_tau_c)/m_tau_c / math.sqrt(M_Pl_rel**2 + sE**2)
print("=== ④ m_τ 绝对链（M_Pl·e^{−E_τ^new}） ===")
print(f"m_τ_pred = {m_tau_pred:.4f} MeV vs 实验 {m_tau_c:.4f} MeV")
print(f"σ_score = {sig_mtau:.3f} {grade(sig_mtau)}")
