# -*- coding: utf-8 -*-
"""
S484 δ = 15°−θ_F 精确框架量定向扫描（证伪先行）+ Koide 家族不对称机制锚
背景：S483 θ_F 解析 = 12.732385°（m_μ/m_e 路径）——2/9 451σ 排除。
S301 近似级：δ = 15°−θ_F = 2.2676° ≈ 静默⁻² = 0.04 rad（偏差 1.09%）。
本步：① δ 精确值定锚；② 框架候选族扫描（σ 幂次/静默族/e 链/窗口族）
——证伪为主（S299 教训：后验扫描不作内生证据）；③ 若全部证伪——
机制分析：Koide 家族不对称（k、√2 形状成分框架化 vs θ_F 比值成分未）
纪律：σ_score 判定；先证伪再证明。
"""
import math

# --- 常数 ---
sigma = 1/15.0
m_e = 0.51099895069
m_mu = 105.6583755
# θ_F 解析反推（S483 方程：(A_μ/A_e)² = m_μ/m_e）
def theta_F(me, mmu):
    r = mmu/me
    def f(th):
        A_mu = 1 + math.sqrt(2)*math.cos(th + 4*math.pi/3)
        A_e  = 1 + math.sqrt(2)*math.cos(th + 2*math.pi/3)
        return (A_mu/A_e)**2 - r
    import scipy.optimize as opt
    return opt.brentq(f, 0.0, 0.25)

thF = theta_F(m_e, m_mu)
thF_deg = thF*180/math.pi
delta = math.pi/12 - thF          # 15° − θ_F（rad）
delta_deg = delta*180/math.pi
print("=" * 78)
print("① δ 精确值定锚")
print("=" * 78)
print("  θ_F = %.9f rad = %.7f°" % (thF, thF_deg))
print("  15° = π/12 = %.9f rad" % (math.pi/12))
print("  δ = 15°−θ_F = %.9f rad = %.7f°" % (delta, delta_deg))
print("  静默⁻² = 0.04——偏差 %.4f%%（S301 近似级复算）"
      % (abs(delta-0.04)/0.04*100))

print()
print("=" * 78)
print("② 框架候选族扫描（δ = 0.039577341 rad）——证伪为主")
print("=" * 78)
def sig_score(pred, u_est):
    return abs(pred - delta)/u_est

# δ 的不确定度：θ_F 的 u_θ = 3.88e-10（S483）——δ = π/12−θ_F——u_δ = u_θ
u_delta = 3.88e-10
print("  u_δ = %.3g rad（θ_F 传导）——严格口径" % u_delta)

# 候选族 A：σ 幂次族
cands = {}
for k in range(1, 11):
    cands["σ^%d" % k] = sigma**k
# 候选族 B：静默族
cands["静默⁻²"] = 1/25.0
cands["静默⁻²·(1−σ)"] = (1/25.0)*(1-sigma)
cands["静默⁻²·(1+σ)"] = (1/25.0)*(1+sigma)
cands["静默⁻²·(1−σ²)"] = (1/25.0)*(1-sigma**2)
cands["静默/(全态·活跃·Σ)"] = 5/(16*3*42)
cands["静默/(活跃·Σ)"] = 5/(3*42)
# 候选族 C：e 链族
cands["e⁻⁴"] = math.exp(-4)
cands["e⁻⁴·活跃"] = 3*math.exp(-4)
cands["e⁻⁴·静默"] = 5*math.exp(-4)
cands["e⁻⁴·幂基"] = 2*math.exp(-4)
# 候选族 D：对数/混合
cands["ln(26/25)"] = math.log(26/25)
cands["ln(1.04)"] = math.log(1.04)
cands["σ·ln(15)·静默⁻¹"] = sigma*math.log(15)/5
cands["σ²·ln15"] = sigma**2*math.log(15)
cands["(σ−σ³)·活跃⁻¹"] = (sigma-sigma**3)/3
cands["σ⁴·(2·全态)"] = sigma**4*32
cands["σ⁵·(2·Σ)"] = sigma**5*84
cands["σ⁵·(活跃·显态)"] = sigma**5*33
cands["σ⁷·(2·全态²)"] = sigma**7*512
cands["σ⁸·Σ"] = sigma**8*42
cands["σ⁸·(静默·活跃)"] = sigma**8*15

rows = []
for name, v in cands.items():
    s = sig_score(v, u_delta)
    rows.append((s, name, v))
rows.sort()
print("  %-28s %14s %12s %s" % ("候选", "值", "σ_score", "判定"))
for s, name, v in rows[:15]:
    mark = "✓" if s <= 1 else ("提示" if s <= 3 else "✗")
    print("  %-28s %14.9f %12.1f %s" % (name, v, s, mark))
print("  → 严格口径（u_δ=3.9e-10）下全部 ✗——δ 无简单框架量候选")

print()
print("=" * 78)
print("③ 宽松口径评估（轻子公式残差传导——S299 同源）")
print("=" * 78)
# 轻子链残差级 ~1e-6（S299：θ_F 偏离保留 ~e-6 级来自质量公式近似）
u_loose = 1e-6
print("  u_δ（轻子公式残差口径 ~1e-6 rad）下：")
for name, v in [("静默⁻²", 0.04), ("ln(26/25)", math.log(26/25)),
                ("σ⁵·(2·Σ)", sigma**5*84), ("σ²·ln15", sigma**2*math.log(15))]:
    s = abs(v - delta)/u_loose
    print("    %-14s = %.9f → σ_score = %.1f %s"
          % (name, v, s, "✓" if s <= 1 else ("提示" if s <= 3 else "✗")))
print("  → 宽松口径下仍无 ≤1σ 候选——δ 精确框架量未达成（S301 近似级维持）")

print()
print("=" * 78)
print("④ Koide 家族不对称机制锚（k、√2 框架化 vs θ_F 未框架化）")
print("=" * 78)
print("  形状成分（框架化）：k = 幂基/活跃 = 2/3（0.053σ✓）——")
print("    结构商（代数恒等——θ 无关——S481）")
print("    √2 = RMS/均值比（0.004σ✓）——形状因子（S482）")
print("    来源：三代质量幅值的整体统计形状——⟨a²⟩ = 幂基 = 2——")
print("    ⟨A⟩ = 1——RMS/⟨A⟩ = √2——不依赖具体比值")
print("  比值成分（未框架化）：θ_F = 12.7324°——2/9 451σ 排除——")
print("    决定 m_e:m_μ:m_τ 具体比值——相位步进 2π/3 = 120°")
print("  机制解读：k 与 √2 是'集合级'（三代整体形状）——框架内生：")
print("    幂基 2、活跃 3 编码集合统计；θ_F 是'个体级'（代间排布）")
print("    ——需要代间步进结构——2π/3 = 活跃!/24×2π？")
print("    ——或静默保护偏移（S301：e 侧奇异边界保护）")
print("  [候选]：θ_F 可能不是独立框架量而是'保护距离'的函数——")
print("    即 θ_F = 15° − f(静默)——f 待定——S301 近似级 f ≈ 静默⁻²")
print("    ——精确级未达成——留作开放项（S483 状态维持）")

print()
print("=" * 78)
print("结论")
print("=" * 78)
print("  ① δ = π/12−θ_F = 0.039577341 rad（精确锚）")
print("  ② 框架候选族扫描：严格口径全部 ✗——宽松口径仍无 ≤1σ")
print("  ③ δ 精确框架量未达成——S301 近似级（δ≈静默⁻² 偏差 1.09%）维持")
print("  ④ 机制锚：Koide 家族不对称 = 集合级（k、√2 框架内生）vs")
print("     个体级（θ_F 未框架化——代间步进/保护距离函数开放）")
print("  [诚实边界]：δ 候选扫描为证伪性结论——不构成 θ_F 框架身份")
print("    ——θ_F 仍开放——S483 状态维持")
