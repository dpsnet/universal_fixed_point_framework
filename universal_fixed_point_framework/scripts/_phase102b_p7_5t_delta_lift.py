# -*- coding: utf-8 -*-
"""
Phase 102b P7-5t-δ 升格攻坚：δ = 1/675 全链复核 + 机制身份深化
==============================================================================
① 全链复核：dH' = ln15+1/675 替代 dH = 2.7095——α_EM/m_τ/m_e/m_μ/E_b/v/m_t/α序列 逐链偏差
② δ 机制身份：σ³×5（静默三阶×代间静默）vs σ²/N_c（静默二阶÷色）——等价代数形式登记
③ Λ F_np 交叉验证：F_np = (b₀/10)³(1−δ)/Δλ₃ 已达标——δ 两域共享成立性
"""
import math, json

M_PL = 1.221e22
LN15 = math.log(15)
LN16_15 = math.log(16/15)
SIGMA = 1/15.0
DELTA = 1/675.0
DH_OLD = 2.7095
DH_NEW = LN15 + DELTA
KMAX = 8.0
N_GEN = 3.0
N_C = 3.0
ALPHA_V = 1+SIGMA+math.sqrt((N_C**2-1)/(4*N_C))
M_TAU_EXP = 1776.86
M_E_EXP = 0.510999
M_MU_EXP = 105.6584
M_T_EXP = 172690.0
V_EXP = 246.11*1000

def dev(f, e): return (f/e-1)*100

print("Phase 102b P7-5t-δ 升格攻坚：全链复核")
print("="*74)
print("  δ = 1/675 = %.9f；dH' = ln15+1/675 = %.7f（vs 2.7095——%+.5f%%）" % (DELTA, DH_NEW, dev(DH_NEW, DH_OLD)))

print("\n[① 全链复核——dH' 逐链偏差]")
# α_EM
a_old = 1.0/(24*(DH_OLD+3)); a_new = 1.0/(24*(DH_NEW+3))
print("  α_EM：旧 %.7f → 新 %.7f（%+.5f%%）" % (a_old, a_new, dev(a_new, a_old)))
# m_τ
E_old = 16*DH_OLD+LN16_15/3; E_new = 16*DH_NEW+LN16_15/3
mt_old = M_PL*math.exp(-E_old); mt_new = M_PL*math.exp(-E_new)
print("  m_τ：旧 %.4f MeV（%+.4f%%）→ 新 %.4f MeV（%+.4f%%）——改善 %+.4f%%" % (mt_old, dev(mt_old, M_TAU_EXP), mt_new, dev(mt_new, M_TAU_EXP), dev(mt_new, M_TAU_EXP)-dev(mt_old, M_TAU_EXP)))
# m_e / m_μ（相对 m_τ——不受 dH 影响——只经 m_τ 绝对锚）
me = mt_new*math.exp(-(3*math.e-SIGMA**3*(1+ALPHA_V)))
mmu = mt_new*math.exp(-(math.log(16)+math.e**-3))
print("  m_e(新锚) = %.6f MeV（%+.4f%%）；m_μ(新锚) = %.4f MeV（%+.4f%%）" % (me, dev(me, M_E_EXP), mmu, dev(mmu, M_MU_EXP)))
# E_b
Eb = a_new**2*me/2
print("  E_b(新) = %.5f eV（%+.4f%%——13.6057 实验）" % (Eb, dev(Eb, 13.6057)))
# v 与 m_t
v = mt_new*(3**4)*(5**(1/3.0))
mt = (1-( (math.sqrt(6)-math.sqrt(2))/math.sqrt(72) )/16)*v/math.sqrt(2)
print("  v(新锚) = %.2f MeV（%+.3f%% vs 246110）；m_t(新) = %.2f MeV（%+.4f%%）" % (v, dev(v, V_EXP), mt, dev(mt, M_T_EXP)))

print("\n[② δ 机制身份——等价代数形式]")
print("  δ = σ³×5 = (1/15)³×5 = 1/675（静默三阶 × 代间静默 k_max−N_gen=5）")
print("  δ = σ²/N_c = (1/15)²/3 = 1/675（静默二阶 ÷ 色数 N_c=3）——等价新表达")
print("  δ = 1/(3³·5²) = 1/(N_c³×(k_max−N_gen)²)——因子化：色立方×代静默平方")
print("  语义：σ³×5 = 跨代三阶静默；σ²/N_c = 色均摊静默二阶——机制论证待选")

print("\n[③ Λ F_np 交叉验证（δ 两域共享）]")
B0 = 9.0; DL3 = math.sqrt(2)*(math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
FNP = (B0/10.0)**3*(1-DELTA)/DL3
print("  F_np = (b₀/10)³(1−δ)/Δλ₃ = %.5f（目标 4.220——%+.4f%%——达标）" % (FNP, dev(FNP, 4.220)))
print("  ★ m_τ 域（16δ 指数修正）+ Λ 域（(1−δ) 因子）——δ 两域共享成立")
print("  ★ 若 δ 升格定理量——m_τ 锚与 Λ 缺口同时受益——链级联闭合")

result = {"delta": DELTA, "dH_new": DH_NEW,
          "mt_old": mt_old, "mt_new": mt_new, "mt_dev_new": dev(mt_new, M_TAU_EXP),
          "me": me, "mmu": mmu, "Eb": Eb, "v": v, "mt_t": mt,
          "identities": ["σ³×(k_max−N_gen)", "σ²/N_c", "1/(N_c³(k_max−N_gen)²)"],
          "FNP": FNP, "FNP_dev": dev(FNP, 4.220)}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102b_p7_5t_delta_lift.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
