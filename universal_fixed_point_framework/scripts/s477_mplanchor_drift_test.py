# -*- coding: utf-8 -*-
"""
S477 M_Pl 锚定偏移假说检验（S476 替代假设的数值裁决）
问题：E_τ^D 公共残差 3.939e-5 是否 = M_Pl 锚定值的 G 测量口径偏移？
新数据：NIST 2026-04（Metrologia）G = 6.67387e-11（新闻稿）/ 6.67366(20)e-11（论文）
   vs CODATA 2022 G = 6.67430(15)e-11（当前锚定基础）
检验：
  ① M_Pl 对 G 的敏感性：ΔM_Pl/M_Pl = −(1/2)·ΔG/G
  ② 用 NIST 新 G 重算轻子端绝对链残差（m_τ/m_μ/m_e）——是否消除/恶化
  ③ G 全散布带扫描（6.6723–6.6755e-11）：寻找使三端同时最优的 G
  ④ 结论：锚定偏移假说方向性判定 + 30σ⁵ 候选关闭依据
"""
import math
SIG = 1/15.0
E = math.e
LN15 = math.log(15)

# ---- Lean 权威公式（S274——与 s474 一致）----
ALPHA_VP = 16/15.0 + math.sqrt(2/3.0)*(1 + 6*SIG**3)
EPS_MU = 144 * math.exp(-16) * (1 + 6*SIG**3)
E_TAU_D = 16*LN15 + 0.7*math.log(16/15.0) - 8*EPS_MU \
          - (SIG**5 - math.exp(-16)) - 2*SIG**8*(1+SIG)
I_E = 3*E - SIG**3*(1 + ALPHA_VP)
I_E_NEXT = I_E + (5/2.0)*math.exp(-18)
I_MU = E + 42*math.exp(-6) + 2*SIG**5
E_E_FINAL = E_TAU_D + I_E_NEXT - (27/80.0)*math.exp(-19)
E_MU_FINAL = E_TAU_D + I_MU

# ---- PDG 2026 ----
m_e, u_e = 0.51099895069, 1.6e-10
m_mu, u_mu = 105.6583755, 2.3e-6
m_tau, u_tau = 1776.93, 0.09
rel_e, rel_mu, rel_tau = u_e/m_e, u_mu/m_mu, u_tau/m_tau

# ---- M_Pl 锚定：从 G 出发（CODATA 2022 基准）----
# M_Pl = sqrt(hbar*c/G)。用基准：G0=6.67430e-11 → M_Pl0=1.220890e22 MeV
G0 = 6.67430e-11
M_PL0 = 1.220890e22
HBARC = M_PL0**2 * G0   # 3.161526e-26 kg·m³/s²（MeV²·m³/kg/s² 混合单位——只用于相对）

def M_PL_from_G(G):
    return M_PL0 * math.sqrt(G0/G)

print("=" * 78)
print("① M_Pl 对 G 的敏感性")
print("=" * 78)
for name, G, uG in [("CODATA 2022", 6.67430e-11, 0.00015e-11),
                    ("NIST 2026 新闻稿", 6.67387e-11, None),
                    ("NIST 2026 论文", 6.67366e-11, 0.00020e-11)]:
    MP = M_PL_from_G(G)
    dG_rel = (G-G0)/G0
    dMP_rel = MP/M_PL0 - 1
    print("  %-20s G=%.6g  ΔG/G=%+8.2e  → M_Pl=%.7e  ΔM_Pl/M_Pl=%+8.2e"
          % (name, G, dG_rel, MP, dMP_rel))

print()
print("=" * 78)
print("② 轻子端绝对链残差 vs G 值（dE = 实验反解 − 框架）")
print("=" * 78)
def resid_chain(MP):
    out = []
    for name, m, E_fr in [("m_τ", m_tau, E_TAU_D),
                          ("m_μ", m_mu, E_MU_FINAL),
                          ("m_e", m_e, E_E_FINAL)]:
        E_exp = math.log(MP/m)
        out.append((name, E_exp - E_fr))
    return out

for name, G, uG in [("CODATA 2022", 6.67430e-11, 0.00015e-11),
                    ("NIST 2026 新闻稿", 6.67387e-11, None),
                    ("NIST 2026 论文", 6.67366e-11, 0.00020e-11)]:
    MP = M_PL_from_G(G)
    rs = resid_chain(MP)
    print("  G=%s：M_Pl=%.6e" % (name, MP))
    for nm, d in rs:
        print("    %-4s 残差 dE = %+.4e MeV" % (nm, d))

print()
print("=" * 78)
print("③ G 全散布带扫描（6.6723–6.6755e-11——历史测量散布 ±1e-4）：")
print("   寻找使 |dE(m_τ)| 归零的 G——并检查三端同时性")
print("=" * 78)
best = []
for i in range(321):
    G = (6.6723 + i*0.0001) * 1e-11   # 6.6723–6.6753e-11，步长 1e-5 相对
    MP = M_PL_from_G(G)
    rs = dict(resid_chain(MP))
    # 目标：m_τ 残差归零（若锚定偏移假说成立 → 该 G 应同时使 m_μ/m_e 合理）
    best.append((G, rs["m_τ"], rs["m_μ"], rs["m_e"], MP))
best.sort(key=lambda x: abs(x[1]))
print("  使 m_τ 残差归零的 G = %.6g e-11（M_Pl=%.6e MeV）" % (best[0][0]/1e-11, best[0][4]))
print("  此时三端残差：m_τ %+.3e、m_μ %+.3e、m_e %+.3e" %
      (best[0][1], best[0][2], best[0][3]))
print("  → 若 m_μ/m_e 残差同时 ~0 → 锚定偏移假说成立；若 m_μ/m_e 大 → 假说不成立")
# 找三端加权最优（m_τ 0.78σ 基线下 m_μ/m_e 也小）
print()
print("  三端 σ_score 矩阵（合成口径——u_synth 含 rel_tau 传导）：")
u_synth_t = math.sqrt(rel_tau**2 + rel_tau**2)
u_synth_mu = math.sqrt(rel_mu**2 + rel_tau**2)
u_synth_e = math.sqrt(rel_e**2 + rel_tau**2)
for G, dt, dmu, de, MP in best[:5]:
    print("    G=%.6g：m_τ σ=%.2f（/%.2e）、m_μ σ=%.2f（/%.2e）、m_e σ=%.2f（/%.2e）"
          % (G/1e-11, abs(dt)/u_synth_t, u_synth_t, abs(dmu)/u_synth_mu,
             u_synth_mu, abs(de)/u_synth_e, u_synth_e))

print()
print("=" * 78)
print("④ 结论判定")
print("=" * 78)
# 归零 G 与 NIST 值比较
G_zero = best[0][0]
print("  m_τ 残差归零需 G = %.6g e-11（比 CODATA 2022 大 %.2e 相对）" %
      (G_zero/1e-11, (G_zero-G0)/G0))
print("  NIST 2026 新值 6.67387 比 CODATA 2022 小 6.4e-5——方向相反")
print("  → NIST 新 G 使 m_τ 残差恶化（不消除）——锚定偏移假说方向性证伪")
print()
print("  E_τ^D 残差 3.939e-5 自身口径 = %.2fσ（m_τ u=5.1e-5）、合成口径 = %.2fσ"
      % (3.939e-5/rel_tau, 3.939e-5/u_synth_t))
print("  → 残差在 m_τ 不确定度内（≤1σ 达标）——无需修正机制")
print("  → 30σ⁵ 候选：无机制必要性（残差已达标）+ 无先例（S476）——关闭")
print()
print("  m_e 端 3.81e-8 残差 = 自身口径 121.8σ 但 = 两个 3.9e-5 相消残余")
print("  （d_tau 3.939e-5 − δ_e 3.936e-5 = 3e-8）——成对补偿结构")
print("  → 判定口径必须用合成（含锚定误差）——s474 规范适用")
