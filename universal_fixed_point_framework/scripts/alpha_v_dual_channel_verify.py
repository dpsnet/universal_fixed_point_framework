# -*- coding: utf-8 -*-
"""α_v 双通道互证验证（2026-10-26）

通道 A（P7-5a 登记候选，2026-10-09）：α_v = ln7 − Δλ_min/2 = 1.8849（+0.10%）
通道 B（假设 D 反推，2026-10-26）：α_v' = 16/15 + √(2/3)(1+6σ³) = 1.8846
两通道差 0.016%——验证 α_v^A 是否闭合轻子失配（I_e + 双链体系）。
"""
import math

sigma = 1/15; s3 = sigma**3
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
rel_e, rel_mu = 2.935e-8, 2.177e-8
rel_cross = math.sqrt(rel_e**2+rel_mu**2)
I_e_exp = math.log(m_tau_c/m_e_c)
I_mu_exp = math.log(m_tau_c/m_mu_c)
I_em_exp = math.log(m_mu_c/m_e_c)

def I_e(av):
    return 3*math.e - s3*(1+av)

def grade(s):
    return "✓ 达标" if s <= 1 else ("～ 提示" if s <= 3 else "✗ 不达标")

print("=== α_v 候选对比 ===")
alphas = {
    "α_v0（旧）": 1.8831,
    "α_v'（假设D 16/15+√(2/3)(1+6σ³)）": 16/15+math.sqrt(2/3)*(1+6*s3),
    "α_v^A（ln7−Δλ_min/2）": 1.8849,
}
for n, a in alphas.items():
    ie = I_e(a)
    sig = abs(ie-I_e_exp)/(I_e_exp*rel_e)
    print(f"  {n:30s} = {a:.6f} → I_e = {ie:.10f} → σ_score = {sig:.3f} {grade(sig)}")

print()
print("=== α_v^A + ε_μ 双链体系（m_e/m_μ 窗口） ===")
avA = 1.8849
eps_mu = 144*math.e**(-16)
I_eA = I_e(avA)
I_muA = math.log(16) + math.e**(-3) + eps_mu
I_emA = I_eA - I_muA
s_em = abs(I_emA-I_em_exp)/rel_cross
print(f"α_v^A：I_e−I_μ = {I_emA:.10f} vs 实验 {I_em_exp:.10f} → σ_score = {s_em:.2f} {grade(s_em)}")
print(f"I_μ' σ（vs m_τ）= {abs(I_muA-I_mu_exp)/(I_mu_exp*rel_mu):.3f}")
print()

print("=== α_v 精确值扫描（I_e 失配最小化） ===")
best = None
for i in range(1883000, 1887000):
    a = i/1e6
    ie = I_e(a)
    s = abs(ie-I_e_exp)/(I_e_exp*rel_e)
    if best is None or s < best[0]:
        best = (s, a)
print(f"最优 α_v* = {best[1]:.6f}（σ_score = {best[0]:.3f}）")
av_star = best[1]
print(f"α_v* − 1.8831 = {av_star-1.8831:+.4f}（+{ (av_star-1.8831)/1.8831*100:.3f}%）")
print(f"α_v* vs ln7−Δλ_min/2（1.8849）：{(av_star-1.8849)/1.8849*100:+.3f}%")
print(f"α_v* vs 假设D（{16/15+math.sqrt(2/3)*(1+6*s3):.6f}）：{(av_star-(16/15+math.sqrt(2/3)*(1+6*s3)))/(16/15+math.sqrt(2/3)*(1+6*s3))*100:+.3f}%")
print()

print("=== α_v* 的框架身份扫描（±0.1% 窗口内的组合） ===")
# η* = (α_v* − 16/15)/√(2/3) − 1
eta_star = (av_star - 16/15)/math.sqrt(2/3) - 1
print(f"η*（√(2/3) 相对修正）= {eta_star:.6f}")
print(f"η* vs 6σ³（{6*s3:.6f}）：{(eta_star-6*s3)/(6*s3)*100:+.2f}%")
print(f"η* vs σ²(1+σ²)×2/5（{sigma**2*(1+sigma**2)*2/5:.6f}）：{(eta_star-sigma**2*(1+sigma**2)*2/5)/(sigma**2*(1+sigma**2)*2/5)*100:+.2f}%")
print(f"η* vs ln(16/15)/36（{math.log(16/15)/36:.6f}）：{(eta_star-math.log(16/15)/36)/(math.log(16/15)/36)*100:+.2f}%")
