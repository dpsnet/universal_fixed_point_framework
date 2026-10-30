# -*- coding: utf-8 -*-
"""
S488 k_pred 偏差来源分解：轻子链 gap/I_e 残差结构——链精确化方向
背景：S487 k_pred（链值）= 0.6666605145 vs 2/3 = 1.558σ 提示（实验
k_exp 0.053σ 达标）——链值偏离 2/3 比实验多——偏差 −6.15e-6。
本步：① 分解 k_pred 偏差的来源（r_mue、r_tau_e 各自贡献）；
② 链残差结构：r_mue_pred（0.377σ✓）vs r_tau_e_pred（0.777σ✓）
——哪个主导 k 偏差？③ 若 r_tau_e 主导——指向 I_e_next 修正方向
（S308-S309 二阶修正）——轻子链精确化路径；④ 对称量检验：
k 的偏差是否可归因于单一链参数（gap or I_e_next）？
纪律：σ_score；先证伪再证明；pyenv。
"""
import math

# --- 轻子链（S274——与 S485/S487 一致）---
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
r_tau_mu_pred = math.exp(I_mu)
r_tau_e_pred = math.exp(I_e_next - (27/80.0)*e**(-19))

# 实验
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.93
r_mue_exp = m_mu/m_e
r_tau_e_exp = m_tau/m_e

def koide_k(masses):
    s_sqrt = sum(math.sqrt(m) for m in masses)
    return sum(masses)/(s_sqrt*s_sqrt)

k_pred = koide_k([1.0, r_mue_pred, r_tau_e_pred])
k_exp = koide_k([m_e, m_mu, m_tau])

print("=" * 78)
print("S488 k_pred 偏差来源分解——轻子链精确化方向")
print("=" * 78)

# ① 各比值对 k 的贡献
# k(1, r1, r2)——∂k/∂r1、∂k/∂r2（数值）
eps = 1e-8
def k_of(r1, r2):
    return koide_k([1.0, r1, r2])
dk_dr1 = (k_of(r_mue_pred*(1+eps), r_tau_e_pred) - k_pred)/(eps*r_mue_pred)
dk_dr2 = (k_of(r_mue_pred, r_tau_e_pred*(1+eps)) - k_pred)/(eps*r_tau_e_pred)
d_r1 = r_mue_pred - r_mue_exp
d_r2 = r_tau_e_pred - r_tau_e_exp
contrib1 = dk_dr1*d_r1
contrib2 = dk_dr2*d_r2
print("① 偏差分解：Δk = k_pred − k_exp = %+.3e" % (k_pred - k_exp))
print("   ∂k/∂r_mue × Δr_mue = %+.3e" % contrib1)
print("   ∂k/∂r_tau_e × Δr_tau_e = %+.3e" % contrib2)
print("   和 = %+.3e（对照 Δk = %+.3e）" % (contrib1+contrib2, k_pred-k_exp))
print("   → r_tau_e 贡献占比 = %.1f%%" % (100*abs(contrib2)/max(abs(contrib1),1e-30)))

# ② 链残差结构（每个比值的 σ_score）
def ss_ratio(pred, exp, rel_u):
    return abs(pred - exp)/exp/rel_u
rel_u_mue = math.sqrt((2.3e-6/m_mu)**2 + (1.6e-10/m_e)**2)
rel_u_tau_e = math.sqrt((0.09/m_tau)**2 + (1.6e-10/m_e)**2)
ss_mue = ss_ratio(r_mue_pred, r_mue_exp, rel_u_mue)
ss_tau_e = ss_ratio(r_tau_e_pred, r_tau_e_exp, rel_u_tau_e)
print()
print("② 链残差结构：")
print("   r_mue_pred：σ_score = %.3f（S474: 0.377——m_μ/m_e 路径）" % ss_mue)
print("   r_tau_e_pred：σ_score = %.3f（S474: 0.777——m_τ/m_e 路径）" % ss_tau_e)
print("   r_mue 相对残差 = %+.3e" % ((r_mue_pred-r_mue_exp)/r_mue_exp))
print("   r_tau_e 相对残差 = %+.3e" % ((r_tau_e_pred-r_tau_e_exp)/r_tau_e_exp))

# ③ 主导来源定位
print()
print("=" * 78)
print("③ 主导来源定位")
print("=" * 78)
print("   Δk 主导来自：%s"
      % ("r_tau_e（m_τ 侧）" if abs(contrib2) > abs(contrib1) else "r_mue（m_μ/m_e 侧）"))
print("   → 若 r_tau_e 主导——指向 I_e_next = I_e + (5/2)e⁻¹⁸ 修正")
print("     （m_τ/m_e 间隔——S308-S309 二阶修正方向）")
print("   → 若 r_mue 主导——指向 gap = I_μ − I_e_next + (27/80)e⁻¹⁹")

# ④ 对称量检验：k 偏差能否归因于单一链参数修正
print()
print("=" * 78)
print("④ 反向检验：修正单一链参数使 k_pred → 2/3")
print("=" * 78)
# 目标：找 d_gap 使 k(exp(−gap−d), r_tau_e_pred) = 2/3
import scipy.optimize as opt
def f_gap(d):
    r1 = math.exp(-(gap + d))
    return koide_k([1.0, r1, r_tau_e_pred]) - 2/3.0
try:
    d_gap = opt.brentq(f_gap, -0.1, 0.1)
    print("   仅调 gap：d_gap = %+.3e（相对 %.3e）——gap 需修正量" % (d_gap, d_gap/gap))
except Exception as ex:
    print("   gap 通道无解：%s" % ex)
def f_ie(d):
    r2 = math.exp(I_e_next + d - (27/80.0)*e**(-19))
    return koide_k([1.0, r_mue_pred, r2]) - 2/3.0
try:
    d_ie = opt.brentq(f_ie, -0.1, 0.1)
    print("   仅调 I_e_next：d_Ie = %+.3e（相对 %.3e）——I_e_next 需修正量" % (d_ie, d_ie/I_e_next))
except Exception as ex:
    print("   I_e_next 通道无解：%s" % ex)
print("   → 修正方向（若 d 小 ~1e-5 级——链精确化可行候选）")

print()
print("=" * 78)
print("结论")
print("=" * 78)
print("  ① Δk 主导来源（r_mue or r_tau_e）见上")
print("  ② 链残差结构（0.377σ/0.777σ）——精度主导源 m_τ")
print("  ③ 单一链参数修正量（d_gap/d_Ie）见上——若 ~1e-5 级")
print("     ——链精确化候选（S308-S309 二阶修正方向检验）")
print("  [诚实边界]：分解为诊断性——不构成自动修正依据——")
print("    修正量需机制论证（S308-S309 已核算二阶修正口径）")
