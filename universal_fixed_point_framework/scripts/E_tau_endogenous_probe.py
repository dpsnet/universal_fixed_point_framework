# -*- coding: utf-8 -*-
"""E_τ 纯内生候选验证（#74：m_τ 链内生闭环候选 + δ 概念分离审计）

新候选：E_τ = 16·ln15 + (7/10)·ln(16/15)——组件全框架量
 16=2⁴（Cl(1,3) 全态）、ln15=Moran 主项 d_H、7/10=(k_max−1)/(N_gen+k_max−1)、
 ln(16/15)=静默比率 ln(全态/非标量)

验证：
 V1 E_τ 双口径精度（框架 M_Pl / PDG M_Pl）
 V2 m_e 继承链（P7-5d：E_e=E_τ+3e）用新公式的数值
 V3 两个 δ 的分离审计：δ_α=16259/6000−ln15（α 判别）vs δ_P7=dH(m_τ 反解)−ln15
 V4 16259/6000 的 m_τ 链精度审计（0.0113%——超 0.1% 标准？）
"""
import numpy as np

ln15 = np.log(15)
ln1615 = np.log(16/15)
e = np.e
m_tau = 1776.86
m_e = 0.51099895000
m_mu = 105.6583755

# M_Pl 口径
M_Pl_fw = 1.221e22
M_Pl_pdg = 1.2209e22
E_tau_fw = np.log(M_Pl_fw/m_tau)
E_tau_pdg = np.log(M_Pl_pdg/m_tau)
E_tau_exp = 43.37394  # 笔记口径

E_new = 16*ln15 + (7/10)*ln1615

print("=== V1：E_τ 新公式双口径精度 ===")
print(f"E_τ^new    = {E_new:.9f}")
print(f"E_τ(框架)  = {E_tau_fw:.9f}  差 {E_new-E_tau_fw:+.7f}（{(E_new-E_tau_fw)/E_tau_fw*1e6:+.2f} ppm）")
print(f"E_τ(PDG)   = {E_tau_pdg:.9f}  差 {E_new-E_tau_pdg:+.7f}（{(E_new-E_tau_pdg)/E_tau_pdg*1e6:+.2f} ppm）")
print()

print("=== V2：m_e 继承链（E_e = E_τ + 3e，P7-5d） ===")
E_e_new = E_new + 3*e
E_e_exp = np.log(M_Pl_fw/m_e)
E_e_pdg = np.log(M_Pl_pdg/m_e)
print(f"E_e^new    = {E_e_new:.9f}")
print(f"E_e(框架)  = {E_e_exp:.9f}  差 {E_e_new-E_e_exp:+.7f}（{(E_e_new-E_e_exp)/E_e_exp*1e6:+.2f} ppm）")
print(f"E_e(PDG)   = {E_e_pdg:.9f}  差 {E_e_new-E_e_pdg:+.7f}（{(E_e_new-E_e_pdg)/E_e_pdg*1e6:+.2f} ppm）")
print()

print("=== V3：两个 δ 概念分离审计 ===")
dH_alpha = 16259/6000
delta_alpha = dH_alpha - ln15
dH_mtau = E_tau_fw - ln1615/3  # P7-5c 反解（用 1/3 修正）
delta_P7 = dH_mtau/16 - ln15  # 注意：P7-5c 是 E=16dH+ln1615/3 ⟹ dH=(E−ln1615/3)/16
dH_mtau_full = (E_tau_fw - ln1615/3)/16
delta_P7_full = dH_mtau_full - ln15
print(f"δ_α = 16259/6000−ln15 = {delta_alpha:.9f}（α 判别口径修正）")
print(f"δ_P7 = (E_τ−ln(16/15)/3)/16−ln15 = {delta_P7_full:.9f}（m_τ 反解口径修正）")
print(f"两 δ 差 = {abs(delta_alpha-delta_P7_full)/delta_alpha*100:.1f}%——概念分离确认")
print(f"δ_P7 vs (11/30)·ln(16/15)/16 = {11/30*ln1615/16:.9f}：差 {abs(delta_P7_full-11/30*ln1615/16)/(11/30*ln1615/16)*100:.2f}%")
print()

print("=== V4：16259/6000 的 m_τ 链精度审计 ===")
E_alpha_in_mtau = 16*dH_alpha + ln1615/3
print(f"用 16259/6000：E_τ = {E_alpha_in_mtau:.9f} vs 实验 {E_tau_fw:.9f}：差 {E_alpha_in_mtau-E_tau_fw:+.6f}")
print(f"  相对指数差 {abs(E_alpha_in_mtau-E_tau_fw)/E_tau_fw*100:.4f}%——质量偏差 {np.exp(abs(E_alpha_in_mtau-E_tau_fw))-1:.4f}%")
print(f"  → 16259/6000 实际不满足 m_τ 链 0.1% 标准（P7-5c 用的是反解 dH≈2.709527 非 16259/6000）")
print(f"  → 104az-152 'α+m_τ 双观测链' 的 m_τ 部分存在口径混用——审计登记")
print()

print("=== V5：m_μ/m_τ 比值链（P7-4d：ln16+e^{−3}）与实验核对 ===")
# 正确口径（P7-4d，2026-10-09）：比值链 m_μ/m_τ = e^{−(ln16+e^{−3})}
# ln16 = 旋量对偶（16=2·k_max）、e^{−3} = 对象静默 S_3（e^{−N_gen}）
# 注：旧版误将比值链实现为 M_Pl·e^{−(E_τ−间隔)} 的绝对锚定反解（29879.8 MeV 荒谬输出），
# 比值链与 E_τ 公式无直接耦合需求——"72% 差"为错误翻译产物，勘误闭合。
ratio_pred = np.exp(-(np.log(16)+np.exp(-3)))
ratio_exp = m_mu/m_tau
print(f"m_μ/m_τ 预言 = {ratio_pred:.10f} vs 实验 {ratio_exp:.10f}：差 {abs(ratio_pred-ratio_exp)/ratio_exp*100:.4f}%")
m_mu_from_ratio = m_tau*ratio_pred
print(f"m_μ(比值链) = {m_mu_from_ratio:.4f} MeV vs 实验 {m_mu:.4f}：差 {abs(m_mu_from_ratio-m_mu)/m_mu*100:.4f}%")
print(f"  → 比值链独立命中（P7-4d：+0.002%）；E_τ 公式与 m_μ 比值链无直接耦合需求")
print()

print("=== 结论 ===")
print("V1：E_τ^new=16ln15+(7/10)ln(16/15) 命中 E_τ 至 0.9–2.8 ppm（框架/PDG 口径）——1e-6 级强候选")
print("V2：m_e 继承（E_e=E_τ+3e）同精度命中（~0.9–2.6 ppm）——双轻子端一致")
print("V3：δ_α≠δ_P7（差 17%）——'δ'概念分离：α 判别修正 vs m_τ 反解修正；此前混用为审计错误")
print("V4：16259/6000 的 m_τ 链实际差 0.49%（质量）超 0.1% 标准——104az-152 双观测链口径混用审计")
print("V5：m_μ/m_τ 比值链（ln16+e^{−3}）独立命中 +0.002%（P7-4d）——旧脚本 M_Pl 反解口径勘误闭合")
print("→ E_τ=16ln15+(7/10)ln(16/15) 为 m_τ 链纯内生闭环候选（组件全框架量、零自由参数）")
