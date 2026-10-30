# -*- coding: utf-8 -*-
"""
S450 强子链候选 a：束缚态能级模型检验 + 三方向收官（2026-10-29）

候选 a 公设：42 域 = 束缚态系统——能级由框架机制
代数生成（非现成量直出）。

检验 1：ln(介子质量比) vs 机制代数整数/组合
  （能级差 = 机制代数×常数——谐振子/壳层模型形式）
检验 2：质量比 vs 能级函数 f(n)（n ∈ 机制代数）
"""
import math

MASS = {
    "m_pi±":  (139.57039, 0.00018),
    "m_K±":   (493.677,   0.016),
    "m_eta":  (547.862,   0.017),
    "m_rho":  (775.11,    0.17),
    "m_omega":(782.65,    0.12),
    "m_phi":  (1019.461,  0.016),
    "m_N":    (939.565346,0.000023),
    "m_eta'": (957.78,    0.06),
    "m_D±":   (1870.29,   0.05),
    "m_B±":   (5279.34,   0.11),
}

sig = 1/15
LN15 = 2.7080502011

def u_ratio(m1, m2):
    v1, u1 = m1; v2, u2 = m2
    return math.hypot(u1/v1, u2/v2)

print("=" * 100)
print("S450 候选 a：能级模型检验 1——ln(质量比) vs 机制代数")
print("=" * 100)

# 机制代数/组合候选（能级差单位——已登记语义）
LEVEL_UNITS = {
    "1（单位）": 1, "2（幂基）": 2, "3（活跃）": 3,
    "5（静默）": 5, "7（对合）": 7, "8（k_max）": 8,
    "15（全态-1）": 15, "16（全态）": 16,
    "ln15": LN15, "I_μ": 2.8223920536,
    "42σ": 42*sig,
}

RATIOS = [
    ("m_eta/m_pi", MASS["m_eta"],  MASS["m_pi±"]),
    ("m_K±/m_pi",  MASS["m_K±"],   MASS["m_pi±"]),
    ("m_rho/m_pi", MASS["m_rho"],  MASS["m_pi±"]),
    ("m_omega/m_pi", MASS["m_omega"], MASS["m_pi±"]),
    ("m_phi/m_pi", MASS["m_phi"],  MASS["m_pi±"]),
    ("m_N/m_pi",   MASS["m_N"],    MASS["m_pi±"]),
    ("m_eta'/m_pi", MASS["m_eta'"], MASS["m_pi±"]),
    ("m_D±/m_pi",  MASS["m_D±"],   MASS["m_pi±"]),
    ("m_B±/m_pi",  MASS["m_B±"],   MASS["m_pi±"]),
]

for rname, m1, m2 in RATIOS:
    r_obs = m1[0]/m2[0]
    u = u_ratio(m1, m2)
    lnr = math.log(r_obs)
    u_ln = u
    best = None
    for lname, lval in LEVEL_UNITS.items():
        # 能级差 = 机制代数整数（ln 尺度）
        score = abs(lnr - lval) / u_ln
        if best is None or score < best[0]:
            best = (score, lname, lval)
    status = "达标" if best[0] <= 1 else ("提示" if best[0] <= 3 else "不达标")
    print(f"  {rname:<14} lnR={lnr:+.6f}±{u:.2e}  最近能级单位: {best[1]:<8} "
          f"= {best[2]:+.4f}  σ_score={best[0]:.2f} [{status}]")

print("-" * 100)
print("检验 2：质量比 vs 能级函数 f(n)——三角数/平方/线性（n=机制代数）")
n_vals = {"幂基2": 2, "活跃3": 3, "静默5": 5, "对合7": 7, "k_max8": 8, "15": 15}
f_fams = {
    "f(n)=n": lambda n: n,
    "f(n)=n²": lambda n: n*n,
    "f(n)=n(n+1)/2": lambda n: n*(n+1)/2,
    "f(n)=2^n−1": lambda n: 2**n - 1,
    "f(n)=2^n": lambda n: 2**n,
}
for rname, m1, m2 in [("m_rho/m_pi", MASS["m_rho"], MASS["m_pi±"]),
                      ("m_phi/m_pi", MASS["m_phi"], MASS["m_pi±"]),
                      ("m_B±/m_pi", MASS["m_B±"], MASS["m_pi±"])]:
    r_obs = m1[0]/m2[0]
    u_abs = u_ratio(m1, m2) * r_obs
    print(f"\n  {rname}: R={r_obs:.4f}±{u_abs:.2e}")
    for fname, f in f_fams.items():
        for nname, n in n_vals.items():
            cand = f(n)
            score = abs(r_obs - cand) / u_abs
            mark = "✓" if score <= 1 else ("~" if score <= 3 else "×")
            if score <= 3:
                print(f"    {mark} f={fname:<14} n={nname:<6} → {cand:.4f}  σ_score={score:.2f}")

print("=" * 100)
print("三方向收官：a 能级直出（本轮负）、b Goldstone（m_π 非近零——待）、")
print("c 42 通道（S449 弱信号）——强子链挂起为开放理论项")
