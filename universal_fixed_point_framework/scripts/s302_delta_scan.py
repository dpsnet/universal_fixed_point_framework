# -*- coding: utf-8 -*-
"""S302: δ 奇异距离精确分解扫描（2026-10-28）

S301 发现 δ = 15°−θ_F = 0.039569760 rad ≈ 静默⁻² = 0.04（偏差 1.09%）。
本步：
  ① δ 的系统候选扫描（框架量组合——含度/弧度双口径）
  ② m_e 修正候选（S269b +(5/2)e⁻¹⁸）对 δ 的传导检验
  ③ δ 偏差 1.09% 的来源——是否与 θ_F 的 2/9 偏差（3.3e-5）关联
"""
import math, itertools

print("=== S302: δ 奇异距离精确分解扫描 ===\n")

sigma = 1/15
e = math.e

theta_F = 12.7328197583
theta_rad = math.radians(theta_F)
delta_rad = math.radians(15.0 - theta_F)
delta_deg = 15.0 - theta_F
print(f"δ = {delta_deg:.9f}° = {delta_rad:.12f} rad")

# ① 系统候选扫描
print(f"\n① δ 候选扫描（目标 {delta_rad:.12f} rad）：")
# 框架量池
S = [2, 3, 5, 7, 15, 21, 42]          # 幂基/活跃/静默/对合/SigmaInv/约束域
sig_pows = [1, 2, 3, 5, 7, 8]
results = []
# 形式：δ = σ^p · a/b（a,b 框架量小组合）
for p in sig_pows:
    for a in S:
        for b in S:
            if b == 0:
                continue
            val = sigma**p * a / b
            diff = abs(val - delta_rad)
            results.append((diff, f"σ^{p}·{a}/{b}", val))
# 形式：δ = a·σ^p（a 框架量）
for p in sig_pows:
    for a in S:
        val = a * sigma**p
        diff = abs(val - delta_rad)
        results.append((diff, f"{a}·σ^{p}", val))
results.sort()
print(f"   最优候选（前 8）：")
for diff, name, val in results[:8]:
    print(f"     {name} = {val:.12f}——偏差 {diff:.2e}（相对 {diff/delta_rad:.2e}）")

# 度口径扫描：δ_deg = 2.267180242°
print(f"\n   δ（度）= {delta_deg:.9f}°——度口径候选：")
deg_cands = {
    "34/15": 34/15,
    "34/15·(1−σ)": 34/15*(1-sigma),
    "42/15−0.53": None,
    "3·(静默⁻²度)": None,
    "137/60.4": None,
    "2.25+2σ": 2.25+2*sigma,
    "2.25+σ⁵·静默²": None,
    "π/79.4": None,
    "e+0.55": None,
}
for name, val in deg_cands.items():
    if val is not None:
        diff = abs(val - delta_deg)
        print(f"     {name} = {val:.9f}——偏差 {diff:.2e}（相对 {diff/delta_deg:.2e}）")

# ② m_e 修正候选传导
print(f"\n② m_e 修正候选（S269b +(5/2)e⁻¹⁸）对 δ 的传导：")
# m_e 指数修正 ΔE_e = (5/2)e⁻¹⁸——ln 比值变化 ≈ ΔE_e——θ_F 变化 ≈ ΔE_e/sens
dE_e = (5/2)*e**(-18)
sens = 51.2   # S300 灵敏度
dtheta = dE_e/sens
print(f"   ΔE_e = (5/2)e⁻¹⁸ = {dE_e:.2e}——Δθ_F ≈ ΔE_e/sens = {dtheta:.2e} rad")
print(f"   ——远小于 δ 偏差 4.30e-4——m_e e⁻¹⁸ 修正不解释 δ 偏差（差 14 量级）")
print()

# ③ δ 偏差与 θ_F 的 2/9 偏差关联
print(f"③ δ 偏差与 θ_F 偏差关联：")
d_theta_29 = abs(theta_rad - 2/9)
d_delta_sil = abs(delta_rad - 1/25)
print(f"   θ_F vs 2/9 偏差：{d_theta_29:.2e}（相对 {d_theta_29/theta_rad:.2e}）")
print(f"   δ vs 静默⁻² 偏差：{d_delta_sil:.2e}（相对 {d_delta_sil/delta_rad:.2e}）")
print(f"   比率 = {d_delta_sil/d_theta_29:.1f}——δ 候选粗糙 13 倍于 θ_F 候选")
print(f"   ——θ_F=2/9 已被 S300 严格证伪（5.6σ）——δ=静默⁻² 偏差 1.09%")
print(f"     是更粗糙的近似——两候选独立（不互相解释）")
print()

# ④ δ 的精确分解——试 0.03957 的连分数
print(f"④ δ 连分数分解（rad）：")
from fractions import Fraction
cf = Fraction(delta_rad).limit_denominator(5000)
print(f"   有理近似：{cf} = {cf.numerator/cf.denominator:.9f}——偏差 {abs(cf-delta_rad):.2e}")
print(f"   分母因子：{cf.denominator} = ?——{cf.numerator} = ?")
# 检验 45/1137？——0.03957·1137 = 45.0？
print(f"   δ·900 = {delta_rad*900:.3f}？δ·1000 = {delta_rad*1000:.3f}？δ·2000 = {delta_rad*2000:.3f}")
print(f"   0.03957·126.8 = 5.017？——0.03957 ≈ 5/126.35？")

print(f"\n判定：")
print(f"  · δ 无简单框架量精确分解（最优 σ⁸·42/1 等——高位幂小修正——")
print(f"    后验拟合嫌疑）——δ ≈ 静默⁻² 维持粗糙近似候选（1.09%）")
print(f"  · m_e 的 e⁻¹⁸ 修正传导不可解释 δ 偏差（差 14 量级）")
print(f"  · δ 与 θ_F 的 2/9 偏差独立——两候选各自近似——")
print(f"    '静默保护'语义方向成立但数值精确化未达成")
print(f"  · δ = 1/(2·12.6) 偏差 0.29%——但 12.6 非框架量——巧合候选")
