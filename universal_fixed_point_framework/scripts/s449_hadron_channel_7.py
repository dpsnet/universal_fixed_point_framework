# -*- coding: utf-8 -*-
"""
S449 强子链候选 c：42 通道分解 + 7/10σ 指数族检验（2026-10-29）

42 = 对合×(静默+1) = 7×6（S209）= 2×3×7（S210）
通道分解候选：轻子漏出用 6（活跃×幂基——I_μ 的
42e⁻⁶ 指数 6）、强子闭合用 7（对合）。

检验 7 通道构造族（防试凑——已登记语义组合）：
  7×e^{cσ} 族（c ∈ 已登记比值：7/10、5/2、7/15、1、2）
  7×e^{7σ/10}——指数=对合σ/(静默×幂基)（7/10 已登记
  比值——E_τ^D 先例）
仅 m_ρ/m_μ 附近（S448 候选 7 基数）。
"""
import math

sig = 1/15
LN15 = 2.7080502011
I_mu = 2.8223920536

MASS = {
    "m_pi±":  (139.57039, 0.00018),
    "m_K±":   (493.677,   0.016),
    "m_eta":  (547.862,   0.017),
    "m_rho":  (775.11,    0.17),
    "m_mu":   (105.6583755, 0.0000023),
    "m_N":    (939.565346, 0.000023),
}

def u_ratio(m1, m2):
    v1, u1 = m1; v2, u2 = m2
    return math.hypot(u1/v1, u2/v2)

# 7 通道构造族（基数 7×指数微调）
SEVEN_FAMILY = {
    "7×e^(7σ/10)":        7*math.exp(7*sig/10),
    "7×e^(7σ/15)":        7*math.exp(7*sig/15),
    "7×e^(7σ/5)":         7*math.exp(7*sig/5),
    "7×e^(7σ×2/15)":      7*math.exp(7*sig*2/15),
    "7×e^σ":              7*math.exp(sig),
    "7×e^(5σ/2/15)":      7*math.exp(5*sig/2/15),
    "7×e^(-7σ/10)":       7*math.exp(-7*sig/10),
    "7×(1+7σ/10)":        7*(1+7*sig/10),
    "42/6×(1+7σ/10)":     42/6*(1+7*sig/10),
    "42×e^(-6)×15":       42*math.exp(-6)*15,
    "42×e^(-6)×(1/7)":    42*math.exp(-6)/7,
    "7×e^(42σ/60)":       7*math.exp(42*sig/60),
}

print("=" * 100)
print("S449 强子链候选 c：42 通道分解检验——7 通道构造族 vs m_ρ/m_μ 等")
print("=" * 100)

RATIOS = [
    ("m_rho/m_mu",  MASS["m_rho"],  MASS["m_mu"]),
    ("m_eta/m_mu",  MASS["m_eta"],  MASS["m_mu"]),
    ("m_K±/m_mu",   MASS["m_K±"],   MASS["m_mu"]),
    ("m_pi±/m_mu",  MASS["m_pi±"],  MASS["m_mu"]),
    ("m_N/m_mu",    MASS["m_N"],    MASS["m_mu"]),
]

for rname, m1, m2 in RATIOS:
    r_obs = m1[0]/m2[0]
    u = u_ratio(m1, m2)
    u_abs = u * r_obs
    best = None
    for cname, cval in SEVEN_FAMILY.items():
        diff = abs(r_obs - cval)
        score = diff / u_abs
        if best is None or score < best[0]:
            best = (score, cname, cval, diff)
    status = "达标" if best[0] <= 1 else ("提示" if best[0] <= 3 else "不达标")
    print(f"  {rname:<14} R={r_obs:.6f}±{u_abs:.2e}  最近: {best[1]:<20} "
          f"= {best[2]:.6f}  σ_score={best[0]:.2f} [{status}]")

print("-" * 100)
print("42 通道分解候选：42=6×7——轻子漏出通道 6（活跃×幂基——")
print("I_μ 的 42e⁻⁶ 指数 6）、强子闭合通道 7（对合）")
print("m_ρ 精确值:", 775.11/105.6583755)
print("7×e^(7σ/10) 精确值:", 7*math.exp(7*sig/10))
print("差:", abs(775.11/105.6583755 - 7*math.exp(7*sig/10)))
