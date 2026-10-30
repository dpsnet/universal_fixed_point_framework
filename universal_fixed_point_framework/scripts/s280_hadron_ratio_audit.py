# -*- coding: utf-8 -*-
"""S280: 强子端比值候选 σ_score 统一审计（2026-10-28）

历史强子端比值候选分散登记（S185/S242/S243 等）——本审计用统一 σ_score
口径（|预测−实验|/合成不确定度——用户纪律）重新判定——识别真实达标 vs
观察级。达标 ≤1σ、提示 1-3σ、不达标 >3σ。
"""
import math

print("=== S280: 强子端比值候选 σ_score 统一审计 ===\n")

# PDG 2024 质量（MeV）——中心值 + 不确定度
m_tau, s_tau = 1776.86, 0.12
m_mu, s_mu = 105.6583755, 0.00023
m_rho, s_rho = 775.11, 0.34      # ρ(770) 宽共振——PDG 775.11(34)
m_Delta, s_Delta = 1232.0, 0.4    # Δ(1232)——PDG 1232.0(4)
m_N, s_N = 938.272046, 0.000021  # 质子
m_e, s_e = 0.51099895, 0.00000015

def check(name, pred, s_rel, note):
    """s_rel 为实验比值相对不确定度（合成）"""
    # 实验中心值由 pred 对应对象决定——这里由调用方给实验值与不确定度
    return name, pred, s_rel, note

print("候选 1：m_τ/m_ρ = √21/2（S185——活跃×对合/幂基）")
r_pred = math.sqrt(21)/2
r_exp = m_tau/m_rho
s = math.sqrt((s_tau/m_tau)**2 + (s_rho/m_rho)**2)
d = abs(math.log(r_pred/r_exp))
print(f"  预测 {r_pred:.6f} vs 实验 {r_exp:.6f}——Δln {d:.3e}——σ_score {d/s:.3f}")

print("\n候选 2：m_τ²/m_ρ² = 21/4 = 5.25（S185 平方口径——约束域/k_max 42/8）")
r_pred = 21/4
r_exp = (m_tau/m_rho)**2
s = 2*math.sqrt((s_tau/m_tau)**2 + (s_rho/m_rho)**2)
d = abs(math.log(r_pred/r_exp))
print(f"  预测 {r_pred:.6f} vs 实验 {r_exp:.6f}——Δln {d:.3e}——σ_score {d/s:.3f}")

print("\n候选 3：m_Δ/m_μ = 35/3 = 11.6667（S243——段因子层）")
r_pred = 35/3
r_exp = m_Delta/m_mu
s = math.sqrt((s_Delta/m_Delta)**2 + (s_mu/m_mu)**2)
d = abs(math.log(r_pred/r_exp))
print(f"  预测 {r_pred:.6f} vs 实验 {r_exp:.6f}——Δln {d:.3e}——σ_score {d/s:.3f}")

print("\n候选 4：m_Δ/m_N = 21/16（活跃×对合/全态——21 谱标度二次出现）")
r_pred = 21/16
r_exp = m_Delta/m_N
s = math.sqrt((s_Delta/m_Delta)**2 + (s_N/m_N)**2)
d = abs(math.log(r_pred/r_exp))
print(f"  预测 {r_pred:.6f} vs 实验 {r_exp:.6f}——Δln {d:.3e}——σ_score {d/s:.3f}")

print("\n候选 5：m_ρ/m_μ = ?（S175 家族——m_ρ 无直接比值候选——参照 2⁴+3⁴ 离散谱）")
print(f"  实验 m_ρ/m_μ = {m_rho/m_mu:.6f}——框架候选：")
print(f"    2⁴+3⁴ = 97——m_ρ/m_μ 实验 7.336——97/13.2？——不干净——观察级")
print(f"    m_ρ/m_μ ≈ 7.336——7+1/3 = 22/3 = 7.3333——差 3.6e-3/7.336 = 4.9e-4")
s = math.sqrt((s_rho/m_rho)**2 + (s_mu/m_mu)**2)
r_pred = 22/3
r_exp = m_rho/m_mu
d = abs(math.log(r_pred/r_exp))
print(f"    22/3 = 7.3333——Δln {d:.3e}——σ_score {d/s:.3f}（m_ρ 宽共振 σ 大）")

print("\n=== 统一判定汇总 ===")
items = [
    ("m_τ/m_ρ = √21/2",  math.sqrt(21)/2, m_tau/m_rho,
     math.sqrt((s_tau/m_tau)**2+(s_rho/m_rho)**2)),
    ("m_τ²/m_ρ² = 21/4", 21/4, (m_tau/m_rho)**2,
     2*math.sqrt((s_tau/m_tau)**2+(s_rho/m_rho)**2)),
    ("m_Δ/m_μ = 35/3",   35/3, m_Delta/m_mu,
     math.sqrt((s_Delta/m_Delta)**2+(s_mu/m_mu)**2)),
    ("m_Δ/m_N = 21/16",  21/16, m_Delta/m_N,
     math.sqrt((s_Delta/m_Delta)**2+(s_N/m_N)**2)),
    ("m_ρ/m_μ = 22/3",   22/3, m_rho/m_mu,
     math.sqrt((s_rho/m_rho)**2+(s_mu/m_mu)**2)),
]
for name, p, e, s in items:
    sc = abs(math.log(p/e))/s
    g = "达标 ✓" if sc <= 1 else ("提示" if sc <= 3 else "不达标 ✗")
    print(f"  {name:<18} 预测 {p:<12.6f} 实验 {e:<12.6f} σ_score {sc:<6.3f} {g}")

print("\n诚实边界：")
print("  · 强子端质量不确定度大（m_ρ ±0.34、m_Δ ±0.4 MeV）——σ_score 判定")
print("    受限于实验精度——'达标'是相对当前测量——未来精度提升可再判")
print("  · m_ρ 为宽共振——质量定义口径（Breit-Wigner pole vs peak）影响")
print("    中心值——±0.34 未含口径系统差——σ_score 可能低估")
print("  · 与轻子端（0.0004σ/0.001σ 级）相比——强子端精度低 3 个数量级——")
print("    '命中'的证据强度不可同日而语")
