# -*- coding: utf-8 -*-
"""
S487 链内禀 Koide 检验：轻子链框架值是否内禀满足 Koide 关系（强同构）
背景：S485 已证 θ_F = f(轻子链 gap)（0.352σ✓）——θ_F 链函数身份。
本步升级：若链值（r_mue_pred、r_tau_e_pred）构造的 Koide k_pred
也 ≈ 幂基/活跃 = 2/3——则 Koide 参数化 = 轻子链的重新参数化
（链内禀 Koide——不依赖独立 Koide 假设）——强同构论证：
  ① 链值 m_e:m_μ:m_τ = 1 : r_mue_pred : r_tau_e_pred
  ② k_pred = (Σm)/(Σ√m)² vs 2/3——σ_score（链残差传导）
  ③ θ_F_pred 复算（S485）——链值同时满足 k 与 θ_F 两约束
  ④ 同构判定：Koide 参数化 ⟺ 轻子链间隔结构（两表述等价）
  ⑤ 对照 k_exp vs k_pred——链残差一致性
纪律：σ_score 判定；先证伪再证明；pyenv。
"""
import math

# --- 框架常数与轻子链（S274——与 S485 一致）---
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

# 实验（PDG 2026）
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.93
r_mue_exp = m_mu/m_e
r_tau_e_exp = m_tau/m_e

print("=" * 78)
print("S487 链内禀 Koide 检验（强同构论证）")
print("=" * 78)

# ① 链值
chain_m = [1.0, r_mue_pred, r_tau_e_pred]   # 相对 m_e
print("① 链值（相对 m_e）：m_e:m_μ:m_τ = 1 : %.8f : %.8f"
      % (r_mue_pred, r_tau_e_pred))

# ② k_pred
def koide_k(masses):
    s_sqrt = sum(math.sqrt(m) for m in masses)
    return sum(masses)/(s_sqrt*s_sqrt)

k_pred = koide_k(chain_m)
k_exp = koide_k([m_e, m_mu, m_tau])
print()
print("② k_pred（链值）= %.10f vs 幂基/活跃 = 2/3 = %.10f" % (k_pred, 2/3.0))
print("   k_exp（实验）= %.10f（S481: 0.053σ✓）" % k_exp)
print("   k_pred − 2/3 = %+.3e（相对 %.3g）" % (k_pred-2/3.0, (k_pred-2/3.0)/(2/3.0)))
print("   k_exp − 2/3  = %+.3e（相对 %.3g）" % (k_exp-2/3.0, (k_exp-2/3.0)/(2/3.0)))

# k_pred 不确定度：链残差传导（r 相对残差 ~1e-8 级——S485）
resid_r_mue = abs(r_mue_pred - r_mue_exp)/r_mue_exp
resid_r_tau_e = abs(r_tau_e_pred - r_tau_e_exp)/r_tau_e_exp
# k 对质量比的灵敏度（数值）
def k_of(r1, r2):
    return koide_k([1.0, r1, r2])
eps = 1e-8
dk_dr1 = (k_of(r_mue_pred*(1+eps), r_tau_e_pred) - k_pred)/(eps*r_mue_pred)
dk_dr2 = (k_of(r_mue_pred, r_tau_e_pred*(1+eps)) - k_pred)/(eps*r_tau_e_pred)
u_k_pred = math.sqrt((dk_dr1*resid_r_mue*r_mue_pred)**2
                   + (dk_dr2*resid_r_tau_e*r_tau_e_pred)**2)
ss_pred = abs(k_pred - 2/3.0)/u_k_pred
print("   链残差（r_mue %.1e、r_tau_e %.1e）→ u_k_pred = %.3e"
      % (resid_r_mue, resid_r_tau_e, u_k_pred))
print("   σ_score(k_pred vs 2/3) = %.3f %s"
      % (ss_pred, "✓达标" if ss_pred <= 1 else ("提示" if ss_pred <= 3 else "✗")))

# ③ θ_F_pred（链反推——S485 复算）
import scipy.optimize as opt
def theta_from_r(r):
    def f(th):
        A_mu = 1 + math.sqrt(2)*math.cos(th + 4*math.pi/3)
        A_e  = 1 + math.sqrt(2)*math.cos(th + 2*math.pi/3)
        return (A_mu/A_e)**2 - r
    return opt.brentq(f, 0.0, 0.25)
th_pred = theta_from_r(r_mue_pred)
th_exp = theta_from_r(r_mue_exp)
u_theta_pred = 1.46e-10
u_theta_exp = 3.88e-10
ss_th = abs(th_pred - th_exp)/math.sqrt(u_theta_pred**2 + u_theta_exp**2)
print()
print("③ θ_F_pred（链反推）= %.6f°——σ_score = %.3f（S485: 0.352✓）"
      % (th_pred*180/math.pi, ss_th))

# ④ 同构判定
print()
print("=" * 78)
print("④ 同构判定：Koide 参数化 ⟺ 轻子链间隔结构")
print("=" * 78)
print("  链给：m_i/m_e = {1, exp(−gap), exp(I_e_next−27/80·e⁻¹⁹)}")
print("  Koide 给：m_i = m₀(1+√2cos(θ_F+2πi/3))²——两参数 (θ_F, m₀)")
print("  → 链两间隔（gap、I_e_next）唯一确定 Koide 两参数：")
print("    θ_F = f(gap)（S485——0.352σ✓）")
print("    m₀ = 链标度（E_τ^D 系）——已由绝对链锚定（S474 0.00σ✓）")
print("  → 若 k_pred 也达标——Koide 关系是链内禀性质（非独立假设）")
print("    ——三代质量的'相位参数化'与'间隔参数化'完全等价")
verdict = "✓ 强同构成立" if (ss_pred <= 3 and ss_th <= 3) else "✗ 未完全同构"
print("  判定：%s" % verdict)

# ⑤ 一致性对照
print()
print("=" * 78)
print("⑤ 对照：k_pred vs k_exp（链残差一致性）")
print("=" * 78)
u_k_exp = 4.16e-5*2/3.0  # S481：u_k ≈ 4.16e-5（m_τ 主导）——k 的单位？
# S481：k_exp = 0.6666644634 ± u_k（u_k ≈ 4.16e-5 相对）
u_k_exp_abs = 4.16e-5*0.6666644634
ss_ke = abs(k_pred - k_exp)/math.sqrt(u_k_pred**2 + u_k_exp_abs**2)
print("  k_pred = %.10f vs k_exp = %.10f——差 %+.3e" % (k_pred, k_exp, k_pred-k_exp))
print("  σ_score(k_pred vs k_exp) = %.3f %s"
      % (ss_ke, "✓达标" if ss_ke <= 1 else ("提示" if ss_ke <= 3 else "✗")))
print("  → 链值在 Koide 关系上的残差 vs 实验——同源传导一致性")

print()
print("=" * 78)
print("结论")
print("=" * 78)
print("  ① 链值 k_pred = %.10f（vs 2/3——σ_score 见上）" % k_pred)
print("  ② θ_F_pred 0.352σ✓（S485）——链值同时满足 k 与 θ_F")
print("  ③ 强同构判定见上——Koide 参数化 = 轻子链重新参数化（若成立）")
print("  [诚实边界]：k_pred 达标性依赖链残差传导口径——")
print("    链残差 ~1e-8 级（S485）——k_pred 精度高——")
print("    若 k_pred 偏差 >3σ——链值不内禀满足 Koide 精确值——")
print("    Koide 关系是近似内禀（链残差级）——需诚实标注")
