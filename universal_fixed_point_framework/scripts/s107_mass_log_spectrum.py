# -*- coding: utf-8 -*-
# S107 质量谱模流对数组装先证伪（2026-10-27）
# 候选：M_Pl 链内 = 1（S106——用户核心目标）⟹ 质量谱 = e^{−E_i}
#   ——ln(m_i/M_Pl) = −E_i（模流对数）——m_τ 绝对链（M_Pl·e^{−E_τ}=1776.63
#   vs 1776.86——1.9σ_score——#74）——检查对数谱是否有框架结构

from math import log, pi

# 实验质量（MeV——PDG 2024）
m_e = 0.51099895069        # ±0.00000015
m_mu = 105.6583755         # ±0.0000023
m_tau = 1776.86            # ±0.12
m_rho = 775.26             # ρ(770) 共振质量
M_Pl = 1.220890e22         # 普朗克质量（MeV）

print("=== 质量谱模流对数（M_Pl 链内 = 1 口径：E_i = −ln(m_i/M_Pl)） ===")
masses = {"m_e": m_e, "m_mu": m_mu, "m_tau": m_tau, "m_rho": m_rho}
Es = {}
for name, m in masses.items():
    E = -log(m / M_Pl)
    Es[name] = E
    print(f"{name}: m = {m:.6g} MeV  E = −ln(m/M_Pl) = {E:.6f}")

print("\n=== 对数差分（比值链——已机检的扩展） ===")
d_emu = Es["m_mu"] - Es["m_e"]   # ln(m_mu/m_e)
d_tmu = Es["m_tau"] - Es["m_mu"] # ln(m_tau/m_mu)
d_rt = Es["m_rho"] - Es["m_tau"] # ln(m_rho/m_tau)
print(f"ln(m_μ/m_e) = {d_emu:.6f}（比值链已机检——0.045σ_score）")
print(f"ln(m_τ/m_μ) = {d_tmu:.6f}")
print(f"ln(m_ρ/m_τ) = {d_rt:.6f}")

print("\n=== 与框架常数对照（先证伪——是否有精确结构） ===")
print(f"E_τ = {Es['m_tau']:.6f} vs 7·2π = {7*2*pi:.6f}（差 {abs(Es['m_tau']-7*2*pi):.4f}——{(Es['m_tau']-7*2*pi)/Es['m_tau']*100:.2f}%）")
print(f"E_τ vs 42 (ConfinementDomain)：差 {Es['m_tau']-42:.4f}")
print(f"E_e = {Es['m_e']:.6f} vs 16·2π = {16*2*pi:.6f}（差 {abs(Es['m_e']-16*2*pi):.4f}——{(Es['m_e']-16*2*pi)/Es['m_e']*100:.2f}%）")
print(f"E_μ = {Es['m_mu']:.6f} vs 11·2π = {11*2*pi:.6f}（差 {abs(Es['m_mu']-11*2*pi):.4f}）")
print(f"E_μ vs 6.5·2π = {6.5*2*pi:.6f}（差 {abs(Es['m_mu']-6.5*2*pi):.4f}）")
print(f"E_e vs 8·ln256/2π 相关 = {8*log(256)/1:.4f}？——不对——ln256 = {log(256):.4f}")

print("\n=== 对数差分 vs 框架量 ===")
print(f"ln(m_μ/m_e) = {d_emu:.6f} vs 5.33？——ln(5.33) = {log(5.33):.4f}——非——直接看：")
print(f"  5.33 = 16/3？  {16/3:.4f}——差 {d_emu-16/3:.4f}")
print(f"  ln(m_μ/m_e) vs 2π·5/6？  {2*pi*5/6:.4f}——差 {abs(d_emu-2*pi*5/6):.4f}")
print(f"  ln(m_μ/m_e) vs 2π·0.85？  {2*pi*0.85:.4f}")
print(f"  ln(m_μ/m_e) vs ln(2π·7)？  {log(2*pi*7):.4f}")
print(f"  ln(m_μ/m_e) vs 42−36？  {42-36:.4f}——6？")

print(f"\nln(m_τ/m_μ) = {d_tmu:.6f} vs 3？  {3:.4f}——差 {abs(d_tmu-3):.4f}")
print(f"ln(m_τ/m_μ) vs ln(17/15)·8？  {log(17/15)*8:.4f}")
print(f"ln(m_τ/m_μ) vs ln(256)/2？  {log(256)/2:.4f}")
print(f"ln(m_τ/m_μ) vs π？  {pi:.4f}——差 {abs(d_tmu-pi):.4f}")

print(f"\nln(m_ρ/m_τ) = {d_rt:.6f} vs −ln(2.29)？——m_ρ/m_τ = {m_rho/m_tau:.4f}")
print(f"m_ρ/m_τ = {m_rho/m_tau:.6f} vs 4/9？  {4/9:.4f}——差 {(m_rho/m_tau-4/9):.5f}")

print("\n=== 组装候选判别 ===")
print("E_i = −ln(m_i/M_Pl)——质量谱的模流对数（M_Pl 链内 = 1）")
print("m_τ 绝对链：E_τ = −ln(m_τ/M_Pl) = 43.39（#74 判别——1.9σ_score 提示）")
print("E_τ vs 7·2π = 43.98（差 1.3%——不精确——证伪整倍连接）")
print("E_e vs 16·2π = 100.53 vs E_e = 100.36？ 差 =", Es["m_e"] - 16*2*pi)
