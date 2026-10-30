# -*- coding: utf-8 -*-
"""
S473 轻子端双路线数值探索（先证伪）
路线 A：α_v' 的 √(2/3) 开方形态机制来源候选扫描
        （纯内生纲领缺口：√(2/3) 的生成链）
路线 B：E_μ 自身口径残余复算（I_μ 2.58e-6 是否已被 S269 修正消化）
纪律：数值计算一律 pyenv 3.11.8；σ_score = |预测−实验|/合成不确定度；
      ≤1σ 达标 / 1-3σ 提示 / >3σ 不达标。
"""
import math

# ---- 框架常数（verbatim）----
SIG = 1/15.0          # σ 框架常数（专用记号——勿与 σ_score 混用）
N_GEN = 3
K_MAX = 8
POW = 2               # 幂基
SIL = 5               # 静默
INV = 7               # 对合
FP = 4                # 不动点
CONF = 42             # 约束域
SIG_INV = 15
FULL = 16             # 全态
E = math.e
LN15 = math.log(15)

def ss(exp, meas, unc):
    """σ_score = |预测−实验|/不确定度"""
    return abs(exp - meas) / unc

print("=" * 78)
print("路线 B：轻子端当前绝对链复算（S269 公式 + PDG 2026）")
print("=" * 78)

# ---- S269/S269b 公式（verbatim）----
ALPHA_VP = 16/15.0 + math.sqrt(2/3.0) * (1 + 6*SIG**3)   # α_v'
EPS_MU = 144 * math.exp(-16) * (1 + 6*SIG**3)            # ε_μ
E_TAU_D = 16*LN15 + 0.7*math.log(16/15.0) - 8*EPS_MU \
          - (SIG**5 - math.exp(-16)) - 2*SIG**8*(1+SIG)  # E_τ^D
I_E = 3*E - SIG**3 * (1 + ALPHA_VP)                      # I_e
I_MU = E + CONF*math.exp(-6) + 2*SIG**5                  # I_μ
E_E = E_TAU_D + I_E + (5/2.0)*math.exp(-18) - (27/80.0)*math.exp(-19)  # S269b 修正后
E_MU = E_TAU_D + I_MU

# PDG 2026（verbatim）
m_e = 0.51099895069;  u_e = 0.16e-9
m_mu = 105.6583755;   u_mu = 0.23e-3
m_tau = 1776.93;      u_tau = 0.09

# m_τ 锚定 M_Pl（链内单位：M_Pl 外部经质量锚定——裁决）
M_PL = m_tau * math.exp(E_TAU_D)
print(f"M_Pl（由 m_τ 锚定）= {M_PL:.6f} MeV")
print(f"E_τ^D = {E_TAU_D:.10f}（框架——m_τ 0.0000σ 锚）")

pred_e = M_PL * math.exp(-E_E)
pred_mu = M_PL * math.exp(-E_MU)
s_e = ss(pred_e, m_e, u_e)
s_mu = ss(pred_mu, m_mu, u_mu)
print(f"m_e 预测 = {pred_e:.11f} MeV（实验 {m_e}）σ_score = {s_e:.4g}")
print(f"m_μ 预测 = {pred_mu:.7f} MeV（实验 {m_mu}）σ_score = {s_mu:.4g}")

# 比值 m_e/m_μ（S470 公式）
R_MU_E = math.exp(I_E - I_MU - (27/80.0)*math.exp(-19) + (5/2.0)*math.exp(-18))
r_exp = m_mu / m_e
u_ratio = (m_mu/m_e) * math.sqrt((u_mu/m_mu)**2 + (u_e/m_e)**2)
s_ratio = ss(R_MU_E, r_exp, u_ratio)
print(f"m_μ/m_e 比值预测 = {R_MU_E:.6f}（实验 {r_exp:.6f}）σ_score = {s_ratio:.4g}")
print(f"  → 比值公式含 5/2 修正（S470 口径：e^{{I_e−I_μ−27/80·e⁻¹⁹}} 原式 +5/2·e⁻¹⁸）")

# E_μ 自身口径：残余（S156b 记录的 2.58e-6 是否仍在）
I_MU_RESID = LN_E_MU_EXP  = -math.log(m_mu / M_PL) - E_MU if False else None
# 用实验反解的 E_μ_exp 与框架 E_μ 对比
E_MU_EXP = -math.log(m_mu / M_PL)
d_E_mu = E_MU_EXP - E_MU
print(f"\nE_μ 框架 = {E_MU:.10f} vs 实验反解 = {E_MU_EXP:.10f}")
print(f"E_μ 残差 = {d_E_mu:+.3e}（S156b 记录 2.58e-6——当前残余）")
print(f"  → E_μ 自身口径（σ_score，以 m_μ 不确定度换算）="
      f"{abs(d_E_mu)/(u_mu/m_mu):.3f}σ")

# I_μ 残余候选扫描（B 路线：残余 ≈ ?）
print(f"\nI_μ 残余（d_E_mu = I_μ_exp − I_μ 方向）≈ {d_E_mu:+.3e}")
cands = {
    "σ⁷": SIG**7,
    "σ⁶": SIG**6,
    "e⁻¹³": math.exp(-13),
    "e⁻¹²": math.exp(-12),
    "5σ⁶": 5*SIG**6,
    "2σ⁵/100": 2*SIG**5/100,
    "e⁻¹⁴": math.exp(-14),
    "42e⁻¹⁰": 42*math.exp(-10),
    "8e⁻¹²": 8*math.exp(-12),
    "σ⁸×97": SIG**8*97,
    "e⁻¹³·2/3": math.exp(-13)*2/3,
}
print("候选（|残差−候选|/候选 < 20% 者标出）：")
for name, v in cands.items():
    rel = abs(abs(d_E_mu) - v) / v if v != 0 else float('inf')
    mark = "◀" if rel < 0.20 else ""
    print(f"  {name:12s} = {v:.4e}  相对差 {rel*100:5.1f}% {mark}")

print()
print("=" * 78)
print("路线 A：√(2/3) 开方形态机制来源候选扫描")
print("（纯内生缺口：√(2/3)=√(幂基/活跃) 的'开方'运算需生成链）")
print("=" * 78)
R23 = math.sqrt(2/3.0)
print(f"√(2/3) = {R23:.10f}；(√(2/3))² = 2/3 = 幂基/活跃 ✓（S192 已知）")
print(f"α_v' = 16/15 + √(2/3)(1+6σ³) = {ALPHA_VP:.10f}")

# A1：√(2/3) 与框架量的简单组合命中扫描
def near(x, y, tol=1e-3):
    if y == 0:
        return False
    return abs(x - y) / abs(y) < tol

print("\nA1：√(2/3)·框架量 vs 框架量族（命中 < 0.1%）")
fconsts = {"2": 2, "3": 3, "5": 5, "7": 7, "8": 8, "15": 15, "16": 16,
           "24": 24, "42": 42, "72": 72, "137": 137, "144": 144,
           "1/15": SIG, "ln15": LN15, "e": E, "σ⁻¹": 15}
hits = []
for n1, v1 in fconsts.items():
    for op in ("*", "/"):
        for n2, v2 in fconsts.items():
            if op == "*":
                tgt = R23 * v1
                cand = v2
            else:
                tgt = R23 * v1
                cand = v2 * v1  # 这个逻辑：√(2/3)·v1 = v2 → v1 = v2/√(2/3)？直接比对 tgt vs v2
            if near(tgt, cand, 1e-3):
                hits.append(f"√(2/3)×{n1} ≈ {n2}（{tgt:.6f} vs {cand}）")
print("命中列表：")
if hits:
    for h in hits:
        print("  " + h)
else:
    print("  无直接命中（√(2/3)×框架常数 不落框架常数族）")

# A2：√(2/3) 与 σ/d_H/e 的组合
print("\nA2：√(2/3) 的 σ/对数/指数组合候选")
candsA = {
    "1−√(2/3)": 1 - R23,
    "√(2/3)−16/15": R23 - 16/15.0,
    "ln15×(1−√(2/3))": LN15 * (1 - R23),
    "15×(1−√(2/3))": 15 * (1 - R23),
    "√(2/3)×15(=√150)": R23 * 15,
    "√150−12": R23*15 - 12,
    "1−2/3−1/15": 1 - 2/3.0 - 1/15.0,
    "√(2/3)−2/3": R23 - 2/3.0,
    "(1−√(2/3))⁻¹": 1/(1-R23),
    "√(2/3)·ln15": R23*LN15,
    "√(2/3)·σ⁶": R23*SIG**6,
    "√(2/3)·σ⁷": R23*SIG**7,
    "√(2/3)·σ⁵": R23*SIG**5,
    "√(2/3)·(1+6σ³)": R23*(1+6*SIG**3),
    "√(2/3)·e⁻¹⁸": R23*math.exp(-18),
    "√(2/3)·e⁻¹⁶": R23*math.exp(-16),
}
# 与 α_v' 相邻量比较
alpha_vp_refs = {
    "α_v'": ALPHA_VP,
    "1+σ": 1+SIG,
    "16/15": 16/15.0,
    "α_v'−16/15": ALPHA_VP - 16/15.0,
    "α_v'−(1+σ)": ALPHA_VP - (1+SIG),
    "I_e/σ³": I_E / SIG**3,
    "I_e": I_E,
    "E_e−E_τ^D": E_E - E_TAU_D,
    "3e−I_e": 3*E - I_E,
}
for name, v in candsA.items():
    for rn, rv in alpha_vp_refs.items():
        if near(v, rv, 5e-3):
            print(f"  {name} = {v:.8f} ≈ {rn} = {rv:.8f}（差 {abs(v-rv)/abs(rv)*100:.3f}%）")

# A3：关键结构观察——(1+6σ³) 共享因子
print("\nA3：(1+6σ³) 共享因子结构（ε_μ 与 α_v' 共享——S467 跨链复用延续）")
print(f"  1+6σ³ = {1+6*SIG**3:.8f}（6 = 活跃! = 3!——S469 幂基指数谱 6 的 v₂=+1 合法）")
print(f"  ε_μ = 144·e⁻¹⁶·(1+6σ³) = {EPS_MU:.8e}")
print(f"  α_v' = (1+σ) + √(幂基/活跃)·(1+6σ³) = {ALPHA_VP:.8f}")
print("  观察：α_v' = (1+σ) + √(2/3)·(1+活跃!·σ³)——")
print("        第一项 1+σ = 全态/静默（结构商）；")
print("        第二项 = √(幂基/活跃) × (1+活跃!·σ³)（根比 × 活跃冻结修正）")

# A4：平方根形态机制候选定性评估（无数值——结构论证）
print("\nA4：'为何开方'机制候选（结构层面——待 Lean/范畴论证）")
print("  候选 a：Clifford 谱投影——质量投影对 P±=(I±γ)/2 的投影比")
print("          (P₊:P₋) 特征值比 = 2/3——'振幅' = √(比值)——")
print("          质量=振幅²（概率→振幅 平方根映射——Born 规则类比）")
print("  候选 b：伴随单位 η 的范数——η: X→GFX 的'推进强度'——")
print("          若 |η|² = 2/3（单位范数平方=幂基/活跃）→ |η| = √(2/3)")
print("  候选 c：sin²θ_W 类弱混合——sin²θ_W = 3/8（GUT 1 级）——")
print("          √(2/3) 非直接；但 sinθ 结构含根——轻子投影=旋转角")
print("  候选 d：均方根结构——轻子谱连续投影（Sp 侧）——RMS 平均")
print("          ——√(均值²)=√(幂基/活跃)——'质量标度=RMS 读数'")

# A5：判别性检查——√(2/3) 在框架中的其他出现（唯一性）
print("\nA5：√(2/3) 出现点（框架内唯一性）")
print("  α_v（MassChainConstants）= 1+σ+√(2/3)（结构量——S180 对照）")
print("  α_v'（轻子投影）= 16/15+√(2/3)(1+6σ³)（动力学）")
print("  → √(2/3) 跨'结构量 α_v / 动力学 α_v'' 双角色——")
print("    与 S468 分界（系数跨链⟺动力学）相悖？——α_v 结构量也含根——")
print("    需查证 α_v 与 α_v' 的语义分工（S192 同一框架身份登记）")
