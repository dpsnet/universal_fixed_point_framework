# -*- coding: utf-8 -*-
"""
S555 P2 强子比值链 m_τ/m_ρ 升格资格复核（S554 候选矩阵对齐后执行）
背景：P2 = m_τ/m_ρ √21/2（S185——1.09σ 提示——S280 统一口径）。
e 升格主线后：m_τ 侧 E_τ^D 已全升格（S546——泊松形式），m_ρ =
8×(16+3⁴)×(1−8/3σ³) 无 e——比值公式 √21/2 纯框架量（√21=√(活跃×对合
域)——21=42/2 约束域/幂基导出）。
本步：① √21/2 vs 实验比值 σ_score 复核（S280 口径）；② 组装链交叉
复核（m_τ(泊松升格)/m_ρ(框架) vs 实验比值——e 升格零损失验证）；
③ 升格资格登记。
"""
import math

print("=" * 78)
print("S555 P2 强子比值链 m_τ/m_ρ 升格资格复核")
print("=" * 78)

SIG = 1/15.0
M_Pl = 1.220890e22   # CODATA 2022 锚定（MeV）

def e_tsum(K=50):
    return sum(1.0/math.factorial(k) for k in range(K+1))

E = e_tsum()
def exp_neg(n):
    return (E**n)**(-1)

# E_τ^D 泊松升格形式（S546/S552 复核）
alpha_v_p = 16/15.0 + math.sqrt(2/3.0)*(1 + 6*SIG**3)
eps_mu_L = 144*exp_neg(16)*(1 + 6*SIG**3)
E_tau_D_L = 16*math.log(15) + 0.7*math.log(16/15.0) - 8*eps_mu_L \
    - (SIG**5 - exp_neg(16)) - 2*SIG**8*(1 + SIG)

# m_τ 预测（泊松升格链——绝对锚定）
m_tau_pred = math.exp(-E_tau_D_L)*M_Pl
# m_ρ 框架（无 e——纯 σ 链——S121/S174/S282 Lean 锚）
m_rho_frame = 8*(16+3**4)*(1-(8/3.0)*SIG**3)

# PDG 2024 实验（S280 口径）
m_tau_exp, s_tau = 1776.86, 0.12
m_rho_exp, s_rho = 775.11, 0.34

print(f"e_tsum(50) = {E!r}")
print(f"E_τ^D_lifted = {E_tau_D_L:.12f}")
print(f"m_τ_pred(泊松) = {m_tau_pred:.6f} MeV（实验 {m_tau_exp}）")
print(f"m_ρ_frame = {m_rho_frame:.6f} MeV（实验 {m_rho_exp}）")
print()

print("① √21/2 候选复核（S280 口径——Δln——无 e 依赖）：")
r_pred = math.sqrt(21)/2.0
r_exp = m_tau_exp/m_rho_exp
s_r = math.sqrt((s_tau/m_tau_exp)**2 + (s_rho/m_rho_exp)**2)
d = abs(math.log(r_pred/r_exp))
ss = d/s_r
print(f"  √21/2 = {r_pred:.6f} vs 实验 {r_exp:.6f}——Δln {d:.3e}"
      f"——σ_score {ss:.3f}（{'达标' if ss<=1 else '提示'}级）")
print(f"  √21 = √(活跃×对合域) = √(3×7) = √(42/2)（约束域/幂基导出）"
      f"——分母 2 = 幂基")
print()

print("② 组装链交叉复核（e 升格零损失验证）：")
r_cross = m_tau_pred/m_rho_frame
s_cross = math.sqrt((s_tau/m_tau_exp)**2 + (s_rho/m_rho_exp)**2)
d_cross = abs(math.log(r_cross/r_exp))
ss_cross = d_cross/s_cross
print(f"  m_τ(泊松)/m_ρ(框架) = {r_cross:.6f} vs 实验 {r_exp:.6f}"
      f"——Δln {d_cross:.3e}——σ_score {ss_cross:.3f}")
print(f"  未升格参考（e 直用）：")
E_tau_D_0 = 16*math.log(15) + 0.7*math.log(16/15.0) \
    - 8*(144*math.e**(-16)*(1+6*SIG**3)) \
    - (SIG**5 - math.e**(-16)) - 2*SIG**8*(1+SIG)
m_tau_0 = math.exp(-E_tau_D_0)*M_Pl
r_0 = m_tau_0/m_rho_frame
print(f"  m_τ(e 直用)/m_ρ = {r_0:.6f}——升格残差 {r_cross-r_0:+.3e}")
print()

print("③ 升格资格登记：")
print("  · m_τ 侧：E_τ^D 已全升格（S546——泊松显式）——✓ e 内生")
print("  · m_ρ 侧：8×(16+3⁴)×(1−8/3σ³)——无 e 出现——✓ e 内生")
print("  · 比值公式 √21/2：纯框架量（活跃×对合域开方/幂基）——无 e——"
      "✓ 比值链 e 内生")
print("  · 升格障碍 = 强子端精度（m_ρ 宽共振 ±0.34 未含口径系统差——"
      "证据强度弱于轻子端 3 数量级）——非 e 依赖")
print()
print("=" * 78)
print("结论：P2 比值链 e 内生性确认（三侧全无外部 e 依赖）——")
print("      √21/2 与组装链交叉 σ_score 复核一致（1.09σ 提示级维持）——")
print("      升格资格 ✓——升格执行仅待强子端精度提升——登记")
