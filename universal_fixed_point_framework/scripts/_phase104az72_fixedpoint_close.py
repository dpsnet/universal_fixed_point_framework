# -*- coding: utf-8 -*-
"""
Phase 104az-72: 缺口本体机制 — δd_(s) 框架化 + a₀ 不动点闭合
目标：m_s = Λ·(C_F/2)² = Λ·4/9（note L3215 候选）→ m_s/T_c = 4/(9a₀)（Λ 消去）
  → δd_(s) = C_F/2 · e^{−m_s/T_c} · N_c 纯框架化
  → d_eff = 16 + d_q 全框架化 → a₀ = (d_eff/(4πN_c)·(Δλ_min/Δλ₃))^(1/3) 自洽不动点
  → F_np = a₀(1−δ)/Δλ₃ 全框架
"""
import math

Nc = 3; Nf = 3; Ngen = 3; kmax = 8
sigma = 1/15
CF = (Nc**2 - 1)/(2*Nc)          # 4/3
delta = sigma**2 * CF / 4        # 1/675
dlmin = (math.sqrt(3) - 1) / 6   # 0.122
dl3 = math.sqrt(2) * dlmin       # 0.1725
Z2 = 1.44                        # (6/5)² = ((kmax-Ngen+1)/5)²

# m_s = Λ·(C_F/2)²  ⇒  m_s/T_c = (Λ·(C_F/2)²)/(a₀·Λ) = (C_F/2)²/a₀ —— Λ 消去！
ms_over_Tc = (CF/2)**2           # 纯框架分子
print(f"(C_F/2)² = {ms_over_Tc:.9f} —— m_s/T_c 的框架分子（Λ 消去）")

# 不动点方程：a₀ = [d_eff(a₀)/(12π·√2)]^(1/3)
#   d_eff = d_gluon + d_q = 16 + Nf·Nc·(C_F/C2_so11)·√(dlmin/dl3)·(1/Z2) + C_F/2·e^{−ms/Tc}·Nc
#   d_q 主项全部框架量；δd_(s) = C_F/2·e^{−m_s/T_c}·Nc = (4/3)/2·e^{−(C_F/2)²/a₀}·3
def d_eff(a):
    d_gluon = 16
    dq_main = Nf*Nc*(CF/2)*math.sqrt(dlmin/dl3)*(1/Z2)
    dds = (CF/2) * math.exp(-ms_over_Tc/a) * Nc
    return d_gluon + dq_main + dds, dq_main, dds

def a0_from_d(d):
    return (d/(4*math.pi*Nc) * (dlmin/dl3))**(1/3)

# 不动点迭代（m_s 候选 m_s/T_c = (C_F/2)²/a₀ —— a₀ 出现在指数中）
a = 0.729135  # paper17 初值
print(f"\n不动点迭代（δd_(s) 用框架 m_s/T_c = (C_F/2)²/a₀）:")
for i in range(12):
    d, dq_main, dds = d_eff(a)
    a_new = a0_from_d(d)
    print(f"  iter{i:2d}: a={a:.9f}  dq_main={dq_main:.6f}  δd_(s)={dds:.6f}  d_eff={d:.6f}  a_new={a_new:.9f}  Δ={abs(a_new-a):.2e}")
    a = a_new

a_fp = a
print(f"\n不动点 a* = {a_fp:.9f}")

# 检查不动点处 m_s/T_c
msTc_fp = ms_over_Tc / a_fp
print(f"不动点处 m_s/T_c = (C_F/2)²/a* = {msTc_fp:.6f}  vs 外部 0.61: dev {(msTc_fp/0.61-1)*100:+.3f}%")

# F_np 用不动点 a*
F_np_fp = a_fp * (1-delta) / dl3
F_np_reg = (9/10)**3 * (1-delta) / dl3
F_np_a0_paper17 = 0.729135 * (1-delta) / dl3
print(f"\nF_np(不动点 a*)  = {F_np_fp:.9f}  dev vs 4.220 {(F_np_fp/4.220-1)*100:+.5f}%")
print(f"F_np(登记 (b0/10)³) = {F_np_reg:.9f}  dev {(F_np_reg/4.220-1)*100:+.5f}%")
print(f"F_np(paper17 a₀) = {F_np_a0_paper17:.9f}  dev {(F_np_a0_paper17/4.220-1)*100:+.5f}%")

# Λ 预测（exp_RGE = rge3_pred = e^{−π²·2^B₀}，B₀=(Nc/2)²=9/4）
B0 = (Nc/2)**2
rge3 = math.exp(-math.pi**2 * 2**B0)
M_Pl_MeV = 1.2209e22
for name, F in [("不动点", F_np_fp), ("登记", F_np_reg), ("paper17", F_np_a0_paper17)]:
    Lambda = rge3 * F * M_Pl_MeV
    print(f"  Λ({name}) = {Lambda:.2f} MeV  (目标 210.0/210.3)")

# 关键：检查 d_q 主项 3.5037 是否 = 框架量组合（14/3=4.667 是 paper17 近似，非精确）
print(f"\nd_q 主项 = {3.503735:.6f} ≠ 14/3={14/3:.6f} —— paper17 的 ≈14/3 是近似")
print(f"d_eff(不动点) = {16+3.503735+ (CF/2)*math.exp(-ms_over_Tc/a_fp)*Nc:.6f} vs paper17 62/3={62/3:.6f}")
