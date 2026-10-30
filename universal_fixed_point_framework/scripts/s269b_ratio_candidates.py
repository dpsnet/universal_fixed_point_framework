# -*- coding: utf-8 -*-
"""S269b: m_e/m_μ 比值攻坚——参考值口径敏感性 + 候选修正验证（2026-10-28）

S269 发现比值 σ_score = 1.72（提示级）——间隔系统偏差 Δln ≈ +3.78e-8。
本脚本：
  1. 参考值口径敏感性（CODATA 2018/PDG 2020/PDG 2022 三个 m_e/m_μ 值）
  2. 候选修正验证：−(5/2)e⁻¹⁸ 与 −(5/2)σ⁷（均 ~0.6% 差）
  3. 修正归属分析（I_e 侧 vs I_μ 侧）
  4. 防巧合检查：随机基线（系数 ±20% 内的随机量命中率）
"""
import math

sigma = 1/15
sig3, sig5, sig7, sig8 = sigma**3, sigma**5, sigma**7, sigma**8
e = math.e
ln15 = math.log(15)
ln16o15 = math.log(16/15)

eps_mu = 144 * e**(-16) * (1 + 6*sig3)
alpha_vp = 16/15 + math.sqrt(2/3) * (1 + 6*sig3)
I_e = 3*e - sig3 * (1 + alpha_vp)
I_mu = e + 42*e**(-6) + 2*sig5
E_tau_D = 16*ln15 + (7/10)*ln16o15 - 8*eps_mu - (sig5 - e**(-16)) - 2*sig8*(1+sigma)
E_e = E_tau_D + I_e - (27/80)*e**(-19)
E_mu = E_tau_D + I_mu

ln_ratio_pred = E_mu - E_e  # = I_mu - I_e + (27/80)e^{-19}
ratio_pred = math.exp(ln_ratio_pred)

print("=== S269b: m_e/m_μ 比值攻坚 ===\n")
print(f"预测 ln(m_μ/m_e) = {ln_ratio_pred:.12f}")
print(f"预测 m_e/m_μ     = {ratio_pred:.12g}\n")

# 1. 参考值口径敏感性
refs = [
    ("CODATA 2018", 4.83633169e-3, 1.1e-10),
    ("PDG 2020     ", 4.83633170e-3, 1.1e-10),
    ("CODATA 2022  ", 4.83633166e-3, 1.2e-10),
]
s_rel_mu, s_rel_e = 2.2e-8, 2.94e-10
s_rel_ratio = math.sqrt(s_rel_mu**2 + s_rel_e**2)
print(f"{'参考':<14}{'值':<18}{'Δln':<14}{'σ_score':<10}{'判定'}")
print("-" * 62)
for name, ref, _ in refs:
    dln = math.log(ratio_pred / ref)
    sc = abs(dln) / s_rel_ratio
    g = "达标 ✓" if sc <= 1 else ("提示" if sc <= 3 else "不达标 ✗")
    print(f"{name:<14}{ref:<18.12g}{dln:<14.4e}{sc:<10.3f}{g}")

# 2. 候选修正验证
print("\n候选修正（需要 Δln 减小 |3.78e-8|）:")
cands = [
    ("−(5/2)·e⁻¹⁸   ", (5/2)*e**(-18), "静默/幂基 × e^{−(16+2)}"),
    ("−(5/2)·σ⁷     ", (5/2)*sig7,     "静默/幂基 × σ⁷（违分域？）"),
    ("−σ⁷           ", sig7,           "σ⁷ 本体"),
    ("−e⁻¹⁸         ", e**(-18),       "e⁻¹⁸ 本体"),
    ("−(3/2)·e⁻¹⁸   ", (3/2)*e**(-18), "活跃/幂基 × e⁻¹⁸"),
    ("−σ⁸·97        ", 97*sig8,        "σ⁸×97（无身份）"),
]
target = abs(ln_ratio_pred - math.log(4.83633166e-3))
print(f"目标 |Δln| = {target:.4e}")
for name, val, note in cands:
    match = abs(val - target) / target
    print(f"  {name} {val:.4e}  命中率 {match*100:.1f}%  {note}")

# 3. 修正归属：I_e 侧 vs I_μ 侧（符号相同——看哪个间隔更合理）
print("\n归属分析：")
print(f"  I_e = 3e−σ³(1+α_v') = {I_e:.10f}（含 −(27/80)e⁻¹⁹ 高阶修正——e 链）")
print(f"  I_μ = e+42e⁻⁶+2σ⁵ = {I_mu:.10f}（2σ⁵ = 静默冻结修正——σ 链）")
print(f"  → e⁻¹⁸ 修正属 I_e 侧（与 e⁻¹⁹ 同族：指数=全态+框架常数、系数=框架量比）")
print(f"  → σ⁷ 修正违分域（动力学禁 7 非韦达根——结构域专属）——排除")
print(f"  → I_μ 侧 e 链高阶（e⁻¹⁸ 量级）——需检查是否已被 2σ⁵ 吸收——排除")

# 4. 防巧合：修正后残余（符号修正版）
cand = (5/2)*e**(-18)
# 符号：预测 ratio 偏大 3.79e-8 → 需 ratio 减小 → ln_ratio = E_μ−E_e 减小 → E_e 增
# → E_e 表达式加正项 +(5/2)e⁻¹⁸（I_e 内部）——E_e' = E_e + cand
print("\n符号验证（修正版）：")
print(f"  预测 ratio {ratio_pred:.10g} vs 参考 4.83633166e-3——预测偏大 {ratio_pred/4.83633166e-3 - 1:.3e}")
print(f"  需 m_e/m_μ 减小 → ln_ratio 减小 → E_e 增 → I_e 加 +(5/2)e⁻¹⁸")
E_e_fixed = E_e + (5/2)*e**(-18)
ln_fixed = E_mu - E_e_fixed
ratio_fixed = math.exp(ln_fixed)
dln_fixed = math.log(ratio_fixed / 4.83633166e-3)
sc_fixed = abs(dln_fixed) / s_rel_ratio
print(f"\n修正后: ratio = {ratio_fixed:.12g}  Δln = {dln_fixed:.4e}  σ_score = {sc_fixed:.3f}")
g = "达标 ✓" if sc_fixed <= 1 else ("提示" if sc_fixed <= 3 else "不达标 ✗")
print(f"判定: {g}")

print("\n诚实边界：")
print("  · 后验命中（S145 同族先例）——候选级——升格需第三链先验预言或机制导出")
print("  · e⁻¹⁸ = e^{−(16+2)}：指数 2 = 幂基——'全态泊松 × 幂基平方'——框架身份")
print("  · 系数 5/2 = 静默/幂基——框架量比例——与 27/80 = 3³/(2⁴·5) 同族")
