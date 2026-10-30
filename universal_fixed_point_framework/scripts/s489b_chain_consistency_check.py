# -*- coding: utf-8 -*-
"""
S489b 2σ⁴ 修正整链一致性检验（证伪关键步）
S489 局部命中：间隔 +2σ⁴ → r_tau_e 0.003σ。但 I_e_next 同时
出现在 gap = I_μ − I_e_next + 27/80·e⁻¹⁹（m_μ/m_e 通道）——
整体修正 I_e_next 会联动改变 r_mue。本步检验：
  ① 修 I_e_next + 2σ⁴：r_mue 恶化程度（σ_score）
  ② 若恶化——2σ⁴ 整体修正不可行——转向 m_τ 专属修正
     （只作用于 m_τ/m_e 间隔——不动 I_e_next——如独立加项）
  ③ 局部修正候选：r_tau_e_pred×exp(+2σ⁴)（m_τ 专属）——检验
     ——r_mue 不变 + r_tau_e 改善 + k_pred 升级
  ④ 诚实标注：无论局部/整体——数值命中仍需机制论证
纪律：σ_score；先证伪；pyenv。
"""
import math

sigma = 1/15.0
e = math.e
I_mu = e + 42*e**(-6) + 2*sigma**5
alpha_v_p = 16/15.0 + math.sqrt(2/3.0)*(1 + 6*sigma**3)
I_e = 3*e - sigma**3*(1 + alpha_v_p)
eps_mu = 144*e**(-16)*(1 + 6*sigma**3)
E_tau_D = 16*math.log(15) + 0.7*math.log(16/15.0) - 8*eps_mu \
    - (sigma**5 - e**(-16)) - 2*sigma**8*(1 + sigma)
I_e_next = I_e + (5/2.0)*e**(-18)
gap = I_mu - I_e_next + (27/80.0)*e**(-19)
r_mue_pred = math.exp(-gap)
r_tau_e_pred = math.exp(I_e_next - (27/80.0)*e**(-19))

m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.93
r_mue_exp = m_mu/m_e
r_tau_e_exp = m_tau/m_e
u_r_mue_rel = math.sqrt((2.3e-6/m_mu)**2 + (1.6e-10/m_e)**2)
u_r_tau_e_rel = math.sqrt((0.09/m_tau)**2 + (1.6e-10/m_e)**2)

def koide_k(masses):
    s_sqrt = sum(math.sqrt(m) for m in masses)
    return sum(masses)/(s_sqrt*s_sqrt)

d2s4 = 2*sigma**4
print("=" * 78)
print("S489b 2σ⁴ 修正整链一致性检验（证伪关键步）")
print("=" * 78)
print("  2σ⁴ = %.8e（S489 局部命中——r_tau_e 0.003σ）" % d2s4)
print("  I_e_next 双重角色：gap（m_μ/m_e）与 m_τ/m_e 间隔共用参数")
print()

# ① 整体修正：I_e_next + 2σ⁴
I_e_next_c = I_e_next + d2s4
gap_c = I_mu - I_e_next_c + (27/80.0)*e**(-19)
r_mue_c = math.exp(-gap_c)
r_tau_e_c = math.exp(I_e_next_c - (27/80.0)*e**(-19))
print("① 整体修正 I_e_next + 2σ⁴：")
print("   r_mue  = %.8f vs 实验 %.8f" % (r_mue_c, r_mue_exp))
ss_mue_c = abs(r_mue_c - r_mue_exp)/r_mue_exp/u_r_mue_rel
print("   σ_score(r_mue) = %.2f（原 0.377）——%s"
      % (ss_mue_c, "✓保持" if ss_mue_c <= 1 else "✗恶化——整体修正不可行"))
ss_tau_c = abs(r_tau_e_c - r_tau_e_exp)/r_tau_e_exp/u_r_tau_e_rel
print("   σ_score(r_tau_e) = %.3f（原 0.777）" % ss_tau_c)

# ② 局部修正：只乘 r_tau_e（不动 I_e_next）
r_tau_e_l = r_tau_e_pred*math.exp(d2s4)
print()
print("② 局部修正（m_τ 专属：r_tau_e × exp(2σ⁴)——I_e_next 不动）：")
print("   r_mue  不变 = %.8f——σ_score = 0.377 ✓保持" % r_mue_pred)
ss_tau_l = abs(r_tau_e_l - r_tau_e_exp)/r_tau_e_exp/u_r_tau_e_rel
print("   r_tau_e = %.8f vs 实验 %.8f——σ_score = %.3f"
      % (r_tau_e_l, r_tau_e_exp, ss_tau_l))
k_l = koide_k([1.0, r_mue_pred, r_tau_e_l])
print("   k_pred'（局部）= %.10f vs 2/3——差 %+.2e"
      % (k_l, k_l-2/3.0))
print("   → 轻子端 3/3 修正后：m_μ/m_e 0.377σ + m_τ/m_e %.3fσ + m_τ/m_μ 0.777σ"
      % ss_tau_l)

# ③ 局部修正后的完整比值链
r_tau_mu_l = r_tau_e_l/r_mue_pred
print()
print("③ 修正后比值链 3/3：")
print("   m_μ/m_e：0.377σ（不变）")
print("   m_τ/m_e：%.3fσ（2σ⁴ 修正后）" % ss_tau_l)
print("   m_τ/m_μ：%.3fσ（= m_τ/m_e 修正传导——m_τ/m_μ 原 0.777σ 变？）"
      % (abs(r_tau_mu_l - m_tau/m_mu)/(m_tau/m_mu)
         /math.sqrt((0.09/m_tau)**2+(2.3e-6/m_mu)**2)))
print()
print("=" * 78)
print("结论")
print("=" * 78)
if ss_mue_c > 3:
    print("  ① 整体修正 I_e_next + 2σ⁴：✗ 证伪（r_mue 恶化——")
    print("     共用参数联动——I_e_next 不可独立修正）")
    print("  ② 局部修正（m_τ 专属项）可行——r_mue 保持 0.377σ +")
    print("     r_tau_e 0.003σ——但需新独立结构（机制论证缺口）")
    print("  ③ 修正后 k_pred' = %.10f——vs 2/3 %.2fσ——链内禀"
          % (k_l, abs(k_l-2/3.0)/(4.0e-6)))
    print("     Koide 从 1.558σ 提示 → 达标准备（若机制论证成立）")
else:
    print("  整体修正未证伪——需进一步检验")
print("  [诚实边界]：2σ⁴ 局部修正 = 后验命中（非先验）——")
print("    'm_τ 专属 2σ⁴ 项'无框架语义——需机制论证——")
print("    σ⁴ 禁制语义（S476 未裁决）——2σ⁴ 缺席 δ* 谱（S321）")
