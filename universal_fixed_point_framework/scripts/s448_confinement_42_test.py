# -*- coding: utf-8 -*-
"""
S448 强子链假设：42 域候选检验（2026-10-29）

S446 已确认强子质量比不落已登记框架量族。本脚本
检验"禁闭域 42 直出"假设族（42 的组合构造）——
若全不达标则强子链假设立项为开放理论项。

42 = 对合×(静默+1) = 7×6（S209）= 2×3×7（S210 链积）
42 的已登记语义构造族（防试凑）：
  42×σ、42×σ^k、42/机制代数、42/(窗口算术)、
  42e^{-窗口算术}（I_μ 先例 42e⁻⁶）、ln 组合
"""
import math

LN15 = 2.7080502011
I_mu = 2.8223920536
sig = 1/15

# PDG 2024（MeV）
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

print("=" * 100)
print("S448 强子链假设：42 域直出候选族检验")
print("=" * 100)

# 候选构造族（42 的组合——已登记语义模式）
cands = {
    "42×σ=2.8": 42*sig,
    "42×σ/10": 42*sig/10,
    "42/15": 42/15,
    "42/16": 42/16,
    "42/6": 42/6,
    "42/7": 42/7,
    "42σ/15": 42*sig/15,
    "42e^-6": 42*math.exp(-6),
    "ln(42/6)": math.log(42/6),
    "ln(42/7)": math.log(42/7),
    "ln(42σ×2)": math.log(84*sig),
    "e^(I_mu)-42e^-6": math.exp(I_mu) - 42*math.exp(-6),
    "e^-6×42×σ": 42*math.exp(-6)*sig,
    "42/(15×5×2)": 42/150,
}

RATIOS = [
    ("m_pi±/m_mu",  MASS["m_pi±"], MASS["m_mu"]),
    ("m_rho/m_mu",  MASS["m_rho"],  MASS["m_mu"]),
    ("m_rho/m_pi±", MASS["m_rho"],  MASS["m_pi±"]),
    ("m_N/m_mu",    MASS["m_N"],    MASS["m_mu"]),
    ("m_K±/m_mu",   MASS["m_K±"],   MASS["m_mu"]),
]

for rname, m1, m2 in RATIOS:
    r_obs = m1[0]/m2[0]
    u = u_ratio(m1, m2)
    lnr = math.log(r_obs)
    best = None
    for cname, cval in cands.items():
        # 同时检验比值直配与对数配
        for mode, diff in [("比值", abs(r_obs - cval)/(r_obs*u)),
                           ("对数", abs(lnr - math.log(cval))/(u) if cval > 0 else float('inf'))]:
            if best is None or diff < best[0]:
                best = (diff, cname, mode, cval)
    status = "达标" if best[0] <= 1 else ("提示" if best[0] <= 3 else "不达标")
    print(f"  {rname:<14} R={r_obs:.6f}  最近42族: {best[1]:<18} "
          f"[{best[2]}]  σ_score={best[0]:.2f} [{status}]")

print("-" * 100)
print("结论：若全部 >3σ → 42 域直出假设被排除——强子链需全新结构")
