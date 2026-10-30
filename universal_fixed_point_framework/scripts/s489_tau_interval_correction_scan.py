# -*- coding: utf-8 -*-
"""
S489 m_τ/m_e 间隔修正量框架候选扫描（先证伪）
背景：S488 诊断 k_pred 偏差 100% 来自 m_τ 侧（m_τ/m_e 间隔
I_e_next−27/80·e⁻¹⁹ 通道——r_tau_e_pred 相对残差 −3.94e-5）。
本步：系统扫描框架量候选修正（σ 幂次族/静默族/e 族）——
  ① 基准：r_tau_e_pred vs 实验（0.777σ——S474）
  ② 候选修正：间隔 + Δln——r_tau_e_pred×exp(Δln) vs 实验
  ③ 扫描 Δln ∈ {nσ⁴, nσ³, nσ⁵, 静默族, e 族, 混合}
  ④ 若命中 ≤1σ——k_pred'（修正后）→ 2/3 升级检验（链内禀
     Koide 从提示级到达标级？）
  ⑤ 诚实边界：数值命中 ≠ 机制证明——修正量需框架语义
纪律：σ_score（合成不确定度）；先证伪；pyenv。
"""
import math

# --- 框架常数 ---
sigma = 1/15.0
e = math.e

# --- 轻子链（S274）---
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

# 实验
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.93
r_mue_exp = m_mu/m_e
r_tau_e_exp = m_tau/m_e

def koide_k(masses):
    s_sqrt = sum(math.sqrt(m) for m in masses)
    return sum(masses)/(s_sqrt*s_sqrt)

# 不确定度
u_r_mue_rel = math.sqrt((2.3e-6/m_mu)**2 + (1.6e-10/m_e)**2)   # 2.18e-8
u_r_tau_e_rel = math.sqrt((0.09/m_tau)**2 + (1.6e-10/m_e)**2)  # 5.07e-5

print("=" * 78)
print("S489 m_τ/m_e 间隔修正量框架候选扫描（先证伪）")
print("=" * 78)

# 基准
ln_resid = math.log(r_tau_e_exp/r_tau_e_pred)
print("① 基准：r_tau_e_pred = %.8f vs 实验 %.8f" % (r_tau_e_pred, r_tau_e_exp))
print("   ln 残差 = %+.4e（相对 %+.4e）" % (ln_resid, (r_tau_e_pred-r_tau_e_exp)/r_tau_e_exp))
ss_base = abs(r_tau_e_pred - r_tau_e_exp)/r_tau_e_exp/u_r_tau_e_rel
print("   σ_score（基准）= %.3f（S474: 0.777）" % ss_base)
print("   → 间隔修正量需求 Δln ≈ %+.4e" % (-ln_resid))
print()

# ② 候选修正族
cands = {}
# σ 幂次族
for n in [1,2,3,4,5,6,7,8]:
    cands["σ^%d" % n] = sigma**n
    cands["2σ^%d" % n] = 2*sigma**n
    cands["3σ^%d" % n] = 3*sigma**n
# e 族
for n in [3,4,5,6,7,8,9,10,16,18,19]:
    cands["e^-%d" % n] = e**(-n)
    cands["2e^-%d" % n] = 2*e**(-n)
# 静默族
cands["静默⁻²"] = (1/5.0)**2
cands["活跃⁻²"] = (1/3.0)**2
cands["Σ⁻¹"] = 1/42.0
cands["全态⁻¹"] = 1/16.0
cands["SigmaInv⁻¹"] = 1/15.0
# 混合
cands["σ³σ⁴"] = sigma**3*sigma**4
cands["σ⁵+σ⁶"] = sigma**5 + sigma**6
cands["σ⁷+2σ⁸"] = sigma**7 + 2*sigma**8
cands["(5/2)e⁻¹⁸"] = 2.5*e**(-18)

target = ln_resid  # 需求修正量（+——间隔加 v 使 pred→exp）
print("② 候选扫描（目标 Δln = %+.4e）：" % target)
print("   %-16s %14s %10s %8s" % ("候选", "值", "比值(值/目标)", "偏差"))
results = []
for name, v in cands.items():
    ratio = v/target
    results.append((abs(ratio-1), name, v, ratio))
results.sort()
for dev, name, v, ratio in results[:15]:
    flag = "★命中" if dev < 0.05 else ("提示" if dev < 0.3 else "")
    print("   %-16s %14.6e %10.4f %8.1f%% %s" % (name, v, ratio, 100*dev, flag))

# ③ 命中检验：修正后 σ_score
print()
print("③ 修正后检验（候选 × exp(v)——间隔 + v）：")
for dev, name, v, ratio in results[:5]:
    r_new = r_tau_e_pred*math.exp(v)
    ss_new = abs(r_new - r_tau_e_exp)/r_tau_e_exp/u_r_tau_e_rel
    # 修正后 k_pred'
    k_new = koide_k([1.0, r_mue_pred, r_new])
    ss_k = abs(k_new - 2/3.0)/4.0e-6  # u_k_pred ≈ 4e-6（S487）
    print("   %-16s σ_score(r_tau_e) = %.3f——k_pred' = %.10f（vs 2/3——σ = %.2f）"
          % (name, ss_new, k_new, ss_k))
    if ss_new <= 1:
        print("      → ★ 达标（修正量框架化候选命中）")
