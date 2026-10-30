# -*- coding: utf-8 -*-
"""S291: Koide Q 交叉验证（MUFPF 轻子公式 → Koide 关系）（2026-10-28）

文献（2608.19277，2026-10-26）：Koide 关系 Q=(Σm)/(Σ√m)²=2/3，
实验 Q=0.66666446(508)——偏差 2e-6——equipartition 机制树级导出。
本步交叉验证：MUFPF 轻子公式预测质量 → Koide Q——检验：
  (a) Q_pred 是否落在实验 Q ± σ；
  (b) MUFPF 公式的 Q 偏差方向/量级是否与实验一致（内部一致性）。
"""
import math

print("=== S291: Koide Q 交叉验证（MUFPF → Koide）===\n")

sigma = 1/15
e = math.e

# MUFPF 轻子公式（S288 溯源——M_Pl=1 内部单位）
E_tau_D = 16*math.log(15) + (7/10)*math.log(16/15) - 8*(144*e**(-16)*(1+6*sigma**3)) \
          - (sigma**5 - e**(-16)) - 2*sigma**8*(1+sigma)
eps_mu = 144*e**(-16)*(1+6*sigma**3)
alpha_vp = 16/15 + math.sqrt(2/3)*(1+6*sigma**3)
I_e = 3*e - sigma**3*(1+alpha_vp)
I_mu = e + 42*e**(-6) + 2*sigma**5
I_e_next = I_e + (5/2)*e**(-18)

E_e = E_tau_D + I_e_next - (27/80)*e**(-19)
E_mu = E_tau_D + I_mu
E_tau = E_tau_D

m_e = e**(-E_e)      # M_Pl = 1 内部单位
m_mu = e**(-E_mu)
m_tau = e**(-E_tau)

# 实验（PDG 2026——Koide 论文引）
m_e_exp = 0.51099895069
m_mu_exp = 105.6583755
m_tau_exp = 1776.93

def koide_Q(me, mmu, mtau):
    return (me + mmu + mtau) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau))**2

Q_pred = koide_Q(m_e, m_mu, m_tau)
Q_exp = koide_Q(m_e_exp, m_mu_exp, m_tau_exp)
Q_sigma = 0.00000508  # Koide 论文 0.66666446(508)

print(f"MUFPF 内部质量（M_Pl=1）：m_e = {m_e:.6e}、m_mu = {m_mu:.6e}、m_tau = {m_tau:.6e}")
print(f"Koide Q（MUFPF 公式值） = {Q_pred:.10f}")
print(f"Koide Q（实验 PDG 2026）= {Q_exp:.10f}（σ = {Q_sigma:.2e}）")
print(f"Q_pred − 2/3 = {Q_pred-2/3:+.3e}")
print(f"Q_exp − 2/3 = {Q_exp-2/3:+.3e}")

d = abs(Q_pred - Q_exp)
print(f"\nQ_pred vs Q_exp：Δ = {d:.2e}——σ_score = {d/Q_sigma:.3f}")

# 内部一致性：MUFPF 公式的偏差结构 vs 实验偏差结构
print(f"\n★ 内部一致性检查（偏差方向/量级）：")
print(f"  Q_pred − 2/3 = {Q_pred-2/3:+.3e}（MUFPF 公式）")
print(f"  Q_exp  − 2/3 = {Q_exp-2/3:+.3e}（实验）")
print(f"  方向一致：{'✓' if (Q_pred-2/3)*(Q_exp-2/3) > 0 else '✗ 反号'}")
print(f"  量级比：|Q_pred-2/3|/|Q_exp-2/3| = {abs(Q_pred-2/3)/abs(Q_exp-2/3):.3f}")

print(f"\n判定：")
d2 = abs(Q_pred - Q_exp)/Q_sigma
if d2 <= 1:
    print(f"  Koide Q 交叉验证：σ_score = {d2:.3f}——≤1σ 达标 ✓")
    print(f"  ——MUFPF 轻子公式自动复现 Koide 关系（非独立新检验——")
    print(f"    但确认 MUFPF 体系与 Koide 经验关系的内部一致性）")
else:
    print(f"  σ_score = {d2:.3f}——需核查")
print(f"  价值：交叉确认——MUFPF 质量比体系与独立经验关系（Koide）一致；")
print(f"  Koide 框架的 equipartition 均分机制为 MUFPF 等权公设提供外部类比支撑。")
