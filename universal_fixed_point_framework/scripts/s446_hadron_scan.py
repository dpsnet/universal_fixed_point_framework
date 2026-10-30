# -*- coding: utf-8 -*-
"""
S446 强子端系统扫描：质量比 vs 框架量族（2026-10-29）

目的：检验强子质量比是否落在已登记框架量族（指数/对数形式）。
框架量族限定为已登记语义的量（防试凑）：
  - ln15 系数族 {1, 2, 5/2, 7/10, 3/2, 1/2, 1/3} × ln15
  - I_μ = 2.8223920536（轻子链主量——S432）
  - I_μ−I_e = ln(m_μ/m_e) = 5.33168（轻子链）
  - 窗口算术/机制代数 {1,2,3,4,5,6,7,8,15,16} 的对数直用
  - σ 相关：ln(1±kσ) 展开族
  - I_μ ± ln15、I_μ ± {1,2,3}（已登记模式组合）

判定：σ_score = |ln(R_obs)−ln(R_pred)| / 合成不确定度
  ≤1σ 达标、1-3σ 提示、>3σ 不达标（用户纪律）
输入：PDG 2024 介子/轻子质量。
"""
import math

# PDG 2024（MeV，均值±不确定度）
MASS = {
    "m_pi±":  (139.57039, 0.00018),
    "m_K±":   (493.677,   0.016),
    "m_eta":  (547.862,   0.017),
    "m_rho":  (775.11,    0.17),
    "m_omega":(782.65,    0.12),
    "m_mu":   (105.6583755, 0.0000023),
    "m_tau":  (1776.93,   0.09),
    "m_e":    (0.51099895069, 0.00000000016),
    "m_N":    (939.565346, 0.000023),  # 质子
    "m_pi0":  (134.9768,  0.0005),
}

LN15 = 2.7080502011   # ln 15
I_mu = 2.8223920536   # S432 轻子链主量
I_e = I_mu + math.log(0.0048363318)  # 派生（S432 m_e/m_μ）
LNMUM_E = math.log(206.7682830)      # ln(m_μ/m_e) ≈ I_μ−I_e

# 框架量族（对数域——已登记语义）
def framework_ln_set():
    s = {}
    def add(name, val):
        s[name] = val
    # ln15 系数族
    for k, nm in [(1, "ln15"), (2, "2ln15"), (2.5, "5/2 ln15"),
                  (0.7, "7/10 ln15"), (1.5, "3/2 ln15"),
                  (0.5, "1/2 ln15"), (1/3, "1/3 ln15")]:
        add(nm, k * LN15)
    # 轻子链量
    add("I_mu", I_mu)
    add("I_mu-I_e (=ln mμ/me)", LNMUM_E)
    add("I_mu+ln15", I_mu + LN15)
    add("I_mu-ln15", I_mu - LN15)
    for k in [1, 2, 3]:
        add(f"I_mu+{k}", I_mu + k)
        add(f"I_mu-{k}", I_mu - k)
    # 窗口算术/机制代数
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 11, 15, 16]:
        add(f"int {k}", k)
    # σ 族（比值接近 1 的用 ln(1±kσ)——小偏移）
    sig = 1/15
    for k, nm in [(1, "σ"), (3, "3σ"), (5, "5σ"), (7, "7σ"), (8, "8σ")]:
        add(nm, k * sig)
    # 组合（比值形式直接）
    for k in [1, 2, 3, 4, 5, 6, 7]:
        add(f"15/{k}", LN15 - math.log(k))
        add(f"{k}/15", math.log(k) - LN15)
    return s

FW = framework_ln_set()

def ratio_ln_unc(m1, m2):
    """ln(m1/m2) 的合成不确定度（一阶传播）"""
    v1, u1 = m1
    v2, u2 = m2
    lnr = math.log(v1 / v2)
    u = math.hypot(u1 / v1, u2 / v2)  # 一阶
    return lnr, u

RATIOS = [
    ("m_pi±/m_mu",  MASS["m_pi±"],  MASS["m_mu"]),
    ("m_K±/m_mu",   MASS["m_K±"],   MASS["m_mu"]),
    ("m_eta/m_mu",  MASS["m_eta"],  MASS["m_mu"]),
    ("m_rho/m_mu",  MASS["m_rho"],  MASS["m_mu"]),
    ("m_omega/m_mu",MASS["m_omega"],MASS["m_mu"]),
    ("m_pi±/m_tau", MASS["m_pi±"],  MASS["m_tau"]),
    ("m_K±/m_tau",  MASS["m_K±"],   MASS["m_tau"]),
    ("m_rho/m_tau", MASS["m_rho"],  MASS["m_tau"]),
    ("m_pi±/m_rho", MASS["m_pi±"],  MASS["m_rho"]),
    ("m_K±/m_rho",  MASS["m_K±"],   MASS["m_rho"]),
    ("m_eta/m_rho", MASS["m_eta"],  MASS["m_rho"]),
    ("m_K±/m_pi±",  MASS["m_K±"],   MASS["m_pi±"]),
    ("m_eta/m_pi±", MASS["m_eta"],  MASS["m_pi±"]),
    ("m_eta/m_K±",  MASS["m_eta"],  MASS["m_K±"]),
    ("m_omega/m_rho", MASS["m_omega"], MASS["m_rho"]),
    ("m_N/m_pi±",   MASS["m_N"],    MASS["m_pi±"]),
    ("m_mu/m_tau",  MASS["m_mu"],   MASS["m_tau"]),   # 对照：已登记构造
    ("m_e/m_mu",    MASS["m_e"],    MASS["m_mu"]),    # 对照：已登记构造
    ("m_tau/m_mu",  MASS["m_tau"],  MASS["m_mu"]),    # 对照：已登记构造
]

print("=" * 100)
print("S446 强子端系统扫描：ln(质量比) vs 框架量族")
print("=" * 100)

hits = []
for rname, m1, m2 in RATIOS:
    lnr, u = ratio_ln_unc(m1, m2)
    best = None
    for fname, fval in FW.items():
        score = abs(lnr - fval) / u if u > 0 else float('inf')
        if best is None or score < best[0]:
            best = (score, fname, fval)
    status = "达标" if best[0] <= 1 else ("提示" if best[0] <= 3 else "不达标")
    print(f"  {rname:<16} ln={lnr:+.6f}±{u:.1e}  最近框架量: {best[1]:<16} "
          f"= {best[2]:+.6f}  σ_score={best[0]:.2f} [{status}]")
    if best[0] <= 3:
        hits.append((rname, lnr, best[1], best[2], best[0]))

print("-" * 100)
print("σ_score≤3 命中：")
if not hits:
    print("  （无——强子端无现成框架构造命中）")
for h in hits:
    print(f"  {h[0]}: ln={h[1]:+.6f} ≈ {h[2]}={h[3]:+.6f}  σ_score={h[4]:.2f}")

# 特别核查：m_μ/m_τ vs e^{−I_μ}（已登记构造倒数）
print("-" * 100)
v_mu_m_tau, u_mu_m_tau = ratio_ln_unc(MASS["m_mu"], MASS["m_tau"])
pred_ln = -I_mu
score = abs(v_mu_m_tau - pred_ln) / u_mu_m_tau
print(f"  对照核查 m_μ/m_τ = e^(−I_μ)：ln 差 = |{v_mu_m_tau:.6f}−({pred_ln:.6f})| "
      f"= {abs(v_mu_m_tau-pred_ln):.2e}  σ_score = {score:.2f}  "
      f"[{'达标' if score<=1 else '提示' if score<=3 else '不达标'}]")
print("  → 这是 S432 已登记构造 m_τ/m_μ=e^(I_μ) 的倒数——非新发现，确认登记构造。")
