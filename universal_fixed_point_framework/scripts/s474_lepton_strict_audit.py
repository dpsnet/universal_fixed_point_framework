# -*- coding: utf-8 -*-
"""
S474 轻子端严格口径全链审计（先证伪：E_τ^D 公共残差 3.9e-5 分解与来源）
公式来源：Lean AlphaChain.lean（S274 权威——E_e_final/E_mu_final/imu_final/I_e_next）
口径纪律：σ_score=|预测−实验|/合成不确定度；≤1σ 达标/1-3σ 提示/>3σ 不达标
本脚本目标：
  1. 全链 σ_score 矩阵（比值链/绝对链×自身/合成口径）
  2. E_τ^D 公共残差的精确值与候选分解（σ⁴ 族/其他）
  3. 残差来源判定（E_τ^D vs I_e vs I_μ——间隔相消检验）
"""
import math

SIG = 1/15.0
E = math.e
LN15 = math.log(15)

# ---- Lean 权威公式（S274 最终）----
ALPHA_VP = 16/15.0 + math.sqrt(2/3.0)*(1 + 6*SIG**3)
EPS_MU = 144 * math.exp(-16) * (1 + 6*SIG**3)
E_TAU_D = 16*LN15 + 0.7*math.log(16/15.0) - 8*EPS_MU \
          - (SIG**5 - math.exp(-16)) - 2*SIG**8*(1+SIG)
I_E = 3*E - SIG**3*(1 + ALPHA_VP)
I_E_NEXT = I_E + (5/2.0)*math.exp(-18)
I_MU = E + 42*math.exp(-6) + 2*SIG**5
E_E_FINAL = E_TAU_D + I_E_NEXT - (27/80.0)*math.exp(-19)
E_MU_FINAL = E_TAU_D + I_MU

# ---- PDG 2026（verbatim：m=值、u=标准不确定度）----
m_e, u_e = 0.51099895069, 1.6e-10    # (16) → 1.6e-10 MeV（1e-11 位？见下）
m_mu, u_mu = 105.6583755, 2.3e-6     # (23) → 2.3e-6 MeV
m_tau, u_tau = 1776.93, 0.09         # (9)  → 0.09 MeV

# 注意：PDG (xx) 括号惯例 = 最后数字位标准不确定度。m_e=0.51099895069(16)：
#   数值 11 位小数 → 最后位 1e-11 → (16)=16e-11=1.6e-10 MeV ✓
# m_mu=105.6583755(23)：7 位小数 → (23)=23e-7? 不对——105.6583755 小数点后 7 位
#   → 最后位 1e-7 → (23)=23e-7=2.3e-6 MeV ✓
# m_tau=1776.93(9)：2 位小数 → 0.09 MeV ✓
print("PDG 2026 不确定度口径：u_e=%.1e、u_mu=%.1e、u_tau=%.1e MeV" % (u_e, u_mu, u_tau))

# 相对不确定度（E 空间 σ）
rel_e, rel_mu, rel_tau = u_e/m_e, u_mu/m_mu, u_tau/m_tau
print("E 空间相对不确定度：m_e %.2e、m_μ %.2e、m_τ %.2e" % (rel_e, rel_mu, rel_tau))

print()
print("=" * 78)
print("① 比值链（无锚自由——E_τ^D 相消——Lean lepton_gap_interval）")
print("=" * 78)
gap = I_MU - I_E_NEXT + (27/80.0)*math.exp(-19)   # E_μ−E_e（Lean 最终）
r_mue_pred = math.exp(-gap)                         # m_μ/m_e = e^{−(E_μ−E_e)}
r_mue_exp = m_mu/m_e
u_r = r_mue_exp*math.sqrt(rel_mu**2 + rel_e**2)
print("E_μ−E_e 间隔 = %.12f" % gap)
print("m_μ/m_e 预测 = %.8f vs 实验 %.8f → σ_score = %.4g" % (r_mue_pred, r_mue_exp,
      abs(r_mue_pred-r_mue_exp)/u_r))
print("  （E_μ−E_e 间隔：框架 %.12f vs 实验 %.12f——差 %.3e）" % (
      gap, -math.log(m_mu/m_e), gap - (-math.log(m_mu/m_e))))

r_tau_mu_pred = math.exp(I_MU)
r_tau_mu_exp = m_tau/m_mu
u_rtm = r_tau_mu_exp*math.sqrt(rel_tau**2 + rel_mu**2)
print("m_τ/m_μ 预测 = %.8f vs 实验 %.8f → σ_score = %.4g" % (r_tau_mu_pred, r_tau_mu_exp,
      abs(r_tau_mu_pred-r_tau_mu_exp)/u_rtm))

r_tau_e_pred = math.exp(I_E_NEXT - (27/80.0)*math.exp(-19))
r_tau_e_exp = m_tau/m_e
u_rte = r_tau_e_exp*math.sqrt(rel_tau**2 + rel_e**2)
print("m_τ/m_e 预测 = %.8f vs 实验 %.8f → σ_score = %.4g" % (r_tau_e_pred, r_tau_e_exp,
      abs(r_tau_e_pred-r_tau_e_exp)/u_rte))

print()
print("=" * 78)
print("② 绝对链（M_Pl 锚定口径）——残差分解")
print("=" * 78)

# 口径 A：M_Pl 由 m_τ 锚定（M_Pl ≡ m_τ·e^{E_τ^D}——m_τ 完美）
# → m_i_pred = m_τ·e^{−(E_i−E_τ^D)}
pred_mu_A = m_tau * math.exp(-I_MU)
pred_e_A = m_tau * math.exp(-(I_E_NEXT - (27/80.0)*math.exp(-19)))
print("口径 A（m_τ 锚定——绝对链 = m_τ×比值）：")
print("  m_μ 预测 %.8f vs 实验 %.8f（差 %.3e MeV）" % (pred_mu_A, m_mu, pred_mu_A-m_mu))
print("  m_e 预测 %.12f vs 实验 %.12f（差 %.3e MeV）" % (pred_e_A, m_e, pred_e_A-m_e))

# 口径 B：M_Pl 外部锚定（CODATA 2022：M_Pl = 1.220890e19 GeV = 1.220890e22 MeV）
M_PL_EXT = 1.220890e22
for name, m, u, E_fr in [("m_τ", m_tau, rel_tau, E_TAU_D),
                         ("m_μ", m_mu, rel_mu, E_MU_FINAL),
                         ("m_e", m_e, rel_e, E_E_FINAL)]:
    E_exp = -math.log(m/M_PL_EXT)
    dE = E_exp - E_fr
    ss_self = abs(dE)/u                    # 自身口径
    u_synth = math.sqrt(u*u + rel_tau**2)  # 合成（含 m_τ 锚定链误差传导）
    ss_synth = abs(dE)/u_synth
    print("口径 B（M_Pl 外部锚定）：%s：E_框架=%.10f、E_实验反解=%.10f、残差=%.3e"
          % (name, E_fr, E_exp, dE))
    print("    自身口径 σ=%.2f（u=%.1e）  合成口径 σ=%.2f（u_synth=%.1e）"
          % (ss_self, u, ss_synth, u_synth))

print()
print("=" * 78)
print("③ E_τ^D 公共残差候选分解（口径 B：M_Pl 外部锚定）")
print("=" * 78)
E_tau_exp = -math.log(m_tau/M_PL_EXT)
res_tau = E_TAU_D - E_tau_exp   # 框架 − 实验（看符号）
print("E_τ^D 框架 = %.10f" % E_TAU_D)
print("E_τ 实验反解 = %.10f（M_Pl 外部 = %.6e MeV）" % (E_tau_exp, M_PL_EXT))
print("残差（框架−实验）= %+.3e" % res_tau)
print("|残差| = %.3e" % abs(res_tau))

cands = {
    "2σ⁴(=1.975e-5×2)": 2*SIG**4,
    "σ⁴": SIG**4,
    "3σ⁴": 3*SIG**4,
    "σ⁵×30": 30*SIG**5,
    "e⁻¹⁰": math.exp(-10),
    "e⁻⁹": math.exp(-9),
    "42e⁻⁸": 42*math.exp(-8),
    "144e⁻⁹": 144*math.exp(-9),
    "ln(16/15)²": math.log(16/15.0)**2,
    "σ³×0.13": SIG**3*0.13,
    "8σ⁴/4": 2*SIG**4,
    "ε_μ×2.4": EPS_MU*2.4,
    "(7/10)ln(16/15)×8.6e-4": 0.7*math.log(16/15.0)*8.6e-4,
    "σ²×8.9e-3": SIG**2*8.9e-3,
    "3e⁻¹¹": 3*math.exp(-11),
    "2e⁻¹⁰": 2*math.exp(-10),
    "e⁻⁸/300": math.exp(-8)/300,
}
print("候选扫描（|残差−候选|/候选 < 5% 标 ◀）：")
for name, v in cands.items():
    rel = abs(abs(res_tau) - v)/v if v != 0 else float('inf')
    mark = "◀◀◀" if rel < 0.05 else ("◀" if rel < 0.20 else "")
    if mark:
        print("  %-28s = %.5e  相对差 %.2f%% %s" % (name, v, rel*100, mark))

print()
print("④ 残差来源判定：公共残差 vs 间隔残差")
d_mu = -math.log(m_mu/M_PL_EXT) - E_MU_FINAL
d_e = -math.log(m_e/M_PL_EXT) - E_E_FINAL
print("  E_μ 残差（实验−框架）= %+.3e" % d_mu)
print("  E_e 残差（实验−框架）= %+.3e" % d_e)
print("  间隔一致性：d_mu − d_e = %+.3e（若≈0 → 残差全部公共——比值链自洽）"
      % (d_mu - d_e))
print("  I_μ 间隔残差（含 27/80 修正相消后）= d_mu−d_e 的分解：")
print("    实验间隔 E_μ−E_e = %+.12f vs 框架间隔 gap = %+.12f → 差 %+.3e"
      % (-math.log(m_mu/m_e), gap, (-math.log(m_mu/m_e)) - gap))

print()
print("⑤ σ⁴ 禁制警示（S21-S23 静默偶幂禁：σ⁴ 禁——若残差≈2σ⁴ 为巧合/禁制缺席）")
print("  |残差|/σ⁴ = %.3f（若 ≈ 整数 → 候选为 σ⁴ 族——但 σ⁴ 被静默偶幂禁）"
      % (abs(res_tau)/SIG**4))
print("  |残差|/(2σ⁴) = %.3f" % (abs(res_tau)/(2*SIG**4)))
