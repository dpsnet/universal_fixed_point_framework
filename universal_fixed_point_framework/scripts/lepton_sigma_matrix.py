# -*- coding: utf-8 -*-
"""轻子链 σ_score 体系化矩阵（2026-10-26）

把轻子相关所有链的 σ 数集中输出（可复用审计基准）：
- 单链 vs m_τ 窗口（被 m_τ 6.75e-5 误差主导）
- 无 m_τ 窗口（m_e/m_μ、m_e/m_τ、m_μ/m_τ 交叉）
- m_τ 中心值扫描：判别 456σ_score 失配是锚问题还是框架相对结构问题
"""
import math

# ---- 实验口径（PDG 2024）----
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
rel_e, rel_mu, rel_tau = 2.935e-8, 2.177e-8, 6.753e-5
G_N_rel = 2.2e-5; M_Pl_rel = G_N_rel/2
M_Pl_MeV = 1.220890e22

# ---- 框架公式 ----
sigma = 1/15; s3 = sigma**3
alpha_v = 16/15 + math.sqrt(2/3)
I_e_pred = 3*math.e - s3*(1+alpha_v)
I_mu_pred = math.log(16) + math.e**(-3)
I_tau_pred = 16*math.log(15) + (7/10)*math.log(16/15)   # E_τ^new（#74）

def sig_abs(pred, exp, rel_unc):
    return abs(pred-exp)/ (exp*rel_unc) if rel_unc > 0 else float('inf')

def grade(s):
    return "✓ 达标" if s <= 1 else ("～ 提示" if s <= 3 else "✗ 不达标")

print("="*72)
print("轻子链 σ_score 体系化矩阵（PDG 2024 相对不确定度：m_e 2.9e-8/m_μ 2.2e-8/m_τ 6.75e-5）")
print("="*72)

# ---- ① 单链 vs m_τ 窗口 ----
I_e_exp = math.log(m_tau_c/m_e_c)
I_mu_exp = math.log(m_tau_c/m_mu_c)
E_exp = math.log(M_Pl_MeV/m_tau_c)

rows = [
    ("P7-5v m_e/m_τ", I_e_pred, I_e_exp, rel_tau, "(3e−σ³(1+α_v))"),
    ("P7-4d m_μ/m_τ", I_mu_pred, I_mu_exp, rel_tau, "(ln16+e^{−3})"),
    ("#74 E_τ(m_τ/M_Pl)", I_tau_pred, E_exp, math.sqrt(M_Pl_rel**2+rel_tau**2), "(16ln15+0.7ln16/15)"),
    ("m_τ 绝对链", M_Pl_MeV*math.exp(-I_tau_pred), m_tau_c, math.sqrt(M_Pl_rel**2+rel_tau**2)/1.0, "M_Pl·e^{−E_τ^new}"),
]
# m_τ 绝对链 σ 特殊处理（相对误差传播）
m_tau_pred = M_Pl_MeV*math.exp(-I_tau_pred)
s_mtau = abs(m_tau_pred-m_tau_c)/m_tau_c/math.sqrt(M_Pl_rel**2+(rel_tau)**2)*1  # E 误差≈δE=6.84e-5
print(f"\n① 单链 vs m_τ 窗口（m_τ 误差主导）")
for name, p, e, ru, formula in rows:
    if name.startswith("m_τ 绝对"):
        s = s_mtau
    else:
        s = abs(p-e)/(e*ru) if not name.startswith("#74") else abs(p-e)/ (math.sqrt(M_Pl_rel**2+rel_tau**2))
    print(f"  {name:22s} pred={p:.10f} exp={e:.10f} → σ_score = {s:.3f} {grade(s)}  {formula}")

# ---- ② 无 m_τ 窗口 ----
print(f"\n② 无 m_τ 窗口（交叉相对——暴露隐藏失配）")
rel_cross = math.sqrt(rel_e**2+rel_mu**2)   # ln 值的绝对误差 = 相对误差（d(ln x)=dx/x）
I_em = I_e_pred - I_mu_pred                 # ln(m_μ/m_e) 预测
I_em_exp = math.log(m_mu_c/m_e_c)
s = abs(I_em-I_em_exp)/rel_cross            # 正确口径：σ_score = |ΔI|/rel_cross
print(f"  m_e/m_μ 比值链（I_e−I_μ）: pred={I_em:.10f} exp={I_em_exp:.10f} → σ_score = {s:.1f} {grade(s)} ★P7-4d 隐藏失配源")

# ---- ③ m_τ 中心值扫描：456σ_score 失配对 m_τ 的敏感性 ----
print(f"\n③ m_τ 中心值扫描（判别：失配是锚问题还是框架相对结构）")
print(f"   m_τ 消去 → m_e/m_μ 窗口不依赖 m_τ——框架相对结构偏差 {I_em-I_em_exp:+.2e} 为真实失配")
print(f"   m_e、m_μ 相对精度 2.9e-8/2.2e-8——实验 m_μ/m_e = 206.7682830(46)")
print(f"   框架 m_μ/m_e = e^{{{I_em:.10f}}} = {math.exp(I_em):.7f}——偏差 {(math.exp(I_em)-206.7682830)/206.7682830:+.2e} 相对")
s_ratio = abs(math.exp(I_em)-206.7682830)/(206.7682830*4.6e-8)
print(f"   比值口径 σ_score = {s_ratio:.1f} {grade(s_ratio)}——与 I 口径 {s:.1f}σ 一致（几百σ）")
print(f"   ★ 结论：m_τ 中心值无法修复（m_τ 消去）——失配在框架相对结构 I_e−I_μ")

# ---- ④ ε_μ 修正后残余 ----
eps_mu = 144*math.e**(-16)
I_mu_prime = I_mu_pred + eps_mu
I_em_prime = I_e_pred - I_mu_prime
s_prime = abs(I_em_prime-I_em_exp)/rel_cross
print(f"\n④ ε_μ = 144e^{{−16}} 修正后 m_e/m_μ 残余")
print(f"   I_μ' = {I_mu_prime:.10f} → m_e/m_μ σ_score = {s_prime:.1f} {grade(s_prime)}")
print(f"   ★ I_e 侧残余（ε_e ≈ −4.3e-7 无身份）→ 双修正问题未闭合（残余 ≈ 12σ_score）")

# ---- ⑤ δ 身份 σ 化（δ_α/d_H 族） ----
print(f"\n⑤ δ 族 σ 化（m_τ 链身份）")
dP7 = (11/30)*math.log(16/15)/16
delta_target = (E_exp - 64*math.log(2) + (47/3)*math.log(16/15))/16
sE = math.sqrt(M_Pl_rel**2+rel_tau**2)
for name, d in [("δ_α = d_H−ln15", 16259/6000-math.log(15)), ("δ_P7 = 11ln(16/15)/480", dP7)]:
    sd = abs(d-delta_target)/(sE/16)
    print(f"   {name:24s} = {d:.10f} vs δ_target = {delta_target:.10f} → σ_score = {sd:.2f} {grade(sd)}")
