# -*- coding: utf-8 -*-
"""
S494 公共残差精确化候选：30σ⁵ − 360σ⁸ 检验
背景：S490 四通道残差 ≈ 3.9356-3.9392e-5——30σ⁵ = 3.9506e-5
统一高 0.3-0.4%（近似标度）。候选：残余偏差 1.4e-7 ≈ 360σ⁸
（360 = 静默×4!×活跃 = 5×24×3——全框架量积——σ⁸ 在 δ* 谱内
合法）——公共残差精确表达候选 = 30σ⁵ − 360σ⁸ = 3.9366e-5。
检验：
  ① 四通道残差 vs 30σ⁵−360σ⁸（偏差矩阵对比）
  ② 修正后比值链 σ_score（修正量改变）
  ③ 360σ⁸ 框架身份 + 合法性审计
纪律：σ_score；先证伪；pyenv。
"""
import math

sigma = 1/15.0
e = math.e
I_mu0 = e + 42*e**(-6) + 2*sigma**5
alpha_v_p = 16/15.0 + math.sqrt(2/3.0)*(1 + 6*sigma**3)
I_e0 = 3*e - sigma**3*(1 + alpha_v_p)
eps_mu = 144*e**(-16)*(1 + 6*sigma**3)
E_tau_D0 = 16*math.log(15) + 0.7*math.log(16/15.0) - 8*eps_mu \
    - (sigma**5 - e**(-16)) - 2*sigma**8*(1 + sigma)
I_e_next0 = I_e0 + (5/2.0)*e**(-18)
gap0 = I_mu0 - I_e_next0 + (27/80.0)*e**(-19)
r_tau_e0 = math.exp(I_e_next0 - (27/80.0)*e**(-19))

m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.93
r_tau_e_exp = m_tau/m_e

s30 = 30*sigma**5
s360_s8 = 360*sigma**8
corr_new = s30 - s360_s8   # 3.9506e-5 − 1.406e-7 = 3.9366e-5

print("=" * 78)
print("S494 公共残差精确化候选：30σ⁵ − 360σ⁸ 检验")
print("=" * 78)
print("  30σ⁵ = %.5e——360σ⁸ = %.5e（360 = 静默×4!×活跃 = 5×24×3）"
      % (s30, s360_s8))
print("  30σ⁵−360σ⁸ = %.5e（公共残差候选精确表达）" % corr_new)
print()

# 四通道残差（vs 30σ⁵ 与 vs 30σ⁵−360σ⁸）
# S490 四通道残差（ln 空间）
ln_resid_Etau = 3.93916e-5
ln_resid_Imu = 3.93640e-5
ln_resid_Ie = 3.93560e-5
ln_resid_taue = math.log(r_tau_e_exp/r_tau_e0)  # S489：3.93565e-5
channels = [
    ("E_τ^D",     ln_resid_Etau),
    ("I_μ",       ln_resid_Imu),
    ("I_e",       ln_resid_Ie),
    ("m_τ/m_e",   ln_resid_taue),
]

print("① 四通道偏差矩阵（对比 30σ⁵ vs 30σ⁵−360σ⁸）：")
print("   %-10s %14s | %12s %12s | %12s %12s"
      % ("通道", "残差", "res/s30", "偏差", "res/corr", "偏差"))
dev30 = []
devnew = []
for name, res in channels:
    d30 = abs(res/s30 - 1)
    dn = abs(res/corr_new - 1)
    dev30.append(d30)
    devnew.append(dn)
    print("   %-10s %14.5e | %12.4f %10.2f%% | %12.4f %10.2f%%"
          % (name, res, res/s30, 100*d30, res/corr_new, 100*dn))
print()
print("   平均偏差：30σ⁵ = %.3f%% → 30σ⁵−360σ⁸ = %.3f%%"
      % (100*sum(dev30)/4, 100*sum(devnew)/4))
print("   极差：30σ⁵ = %.3f%% → 30σ⁵−360σ⁸ = %.3f%%"
      % (100*(max(dev30)-min(dev30)), 100*(max(devnew)-min(devnew))))
print()

print("② 修正量变化对比值链的影响（30σ⁵ → 30σ⁵−360σ⁸）：")
# 修正量改变 δcorr = −360σ⁸——I_μ'/I_e' 都 +corr 而不是 +30σ⁵
# gap = I_μ−I_e_next——成对平移抵消——比值链不变（m_μ/m_e）
# m_τ/m_e：I_e_next + (30σ⁵−360σ⁸) 修正
corr = corr_new
I_mu_c = I_mu0 + corr
I_e_c = I_e0 + corr
I_e_next_c = I_e_c + (5/2.0)*e**(-18)
gap_c = I_mu_c - I_e_next_c + (27/80.0)*e**(-19)
r_mue_c = math.exp(-gap_c)
r_tau_e_c = math.exp(I_e_next_c - (27/80.0)*e**(-19))
r_tau_mu_c = math.exp(I_mu_c)
r_mue_exp = m_mu/m_e
r_tau_mu_exp = m_tau/m_mu
print("   m_μ/m_e = %.8f vs 实验 %.8f（差 %+.3e）"
      % (r_mue_c, r_mue_exp, r_mue_c-r_mue_exp))
print("   m_τ/m_e = %.8f vs 实验 %.8f（差 %+.3e）"
      % (r_tau_e_c, r_tau_e_exp, r_tau_e_c-r_tau_e_exp))
print("   m_τ/m_μ = %.8f vs 实验 %.8f（差 %+.3e）"
      % (r_tau_mu_c, r_tau_mu_exp, r_tau_mu_c-r_tau_mu_exp))
print()

def koide_k(ms):
    s = sum(math.sqrt(x) for x in ms)
    return sum(ms)/(s*s)
k_c = koide_k([1.0, r_mue_c, r_tau_e_c])
print("   k_pred'' = %.10f vs 实验 0.6666644634（差 %+.3e）"
      % (k_c, k_c-0.6666644634))
print()

print("③ 360σ⁸ 框架身份审计：")
print("   360 = 5×24×3 = 静默×4!×活跃——全框架量积 ✓")
print("   σ⁸ 在 δ* 幂次谱 {3,5,7,8}——合法 ✓")
print("   360σ⁸ = 1.406e-7——公共残差 30σ⁵ 的 0.35% 修正——")
print("   二阶修正结构（σ⁸ 项）——与 δ* 的 8σ⁸ 同族")
print()

print("=" * 78)
print("结论")
print("=" * 78)
print("  ① 30σ⁵−360σ⁸ = 3.9366e-5——四通道偏差全面改善：")
print("     平均 0.35% → 0.03%（~12 倍）——极差 0.09% → 0.06%")
print("  ② I_μ/I_e/m_τ/m_e 三通道命中（0.005-0.025%）——")
print("     E_τ^D 通道仍 0.07% 偏差（可能含专属结构）")
print("  ③ 360 = 静默×4!×活跃 全框架量 + σ⁸ 合法——")
print("     候选有框架语义——公共残差精确表达候选升级")
print("  [诚实边界]：360σ⁸ 为后验命中（扫描残余偏差发现）——")
print("     '为何 360'（静默×4!×活跃 积）是身份而非机制——")
print("     需更多通道/量判别——E_τ^D 通道 0.07% 残余开放")
