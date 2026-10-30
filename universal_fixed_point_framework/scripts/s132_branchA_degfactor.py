# -*- coding: utf-8 -*-
# s132_branchA_degfactor.py —— 分支 A 深化：态数倒数框架下的解冻因子（S132，2026-10-27）
# 1. 冻结乘法级联：Ω_τ 的乘法因子分解（E 加法 ↔ 态数乘法——Rec/Sp 对偶表现）
# 2. "3e→e^{3e}"因子身份：Ω_e/Ω_τ = e^{I_e} = e^{3e}·e^{−σ³(1+α_v')}
# 3. e/μ 解冻因子的框架分解扫描（不限于 59²——换框架量）
import math

sigma = 1 / 15
ln15 = math.log(15)
M_Pl = 1.220890e22
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.86

# ── E_τ^D 四阶截断（S117）
eps_mu = 144 * math.exp(-16) * (1 + 6 * sigma**3)
E_tau_D = (16 * ln15 + (7 / 10) * math.log(16 / 15)
           - 8 * eps_mu - (sigma**5 - math.exp(-16)) - 2 * sigma**8 * (1 + sigma))

# ── 冻结乘法级联（态数层）
print("=== 冻结乘法级联（Ω_τ = e^{E_τ^D}——乘法因子分解） ===")
Omega_tau = math.exp(E_tau_D)
print(f"Ω_τ = e^{{E_τ^D}} = {Omega_tau:.6e}")
print(f"  主导因子 15^16（全冻结态数） = {15**16:.6e}")
print(f"  投影因子 (16/15)^(7/10) = {(16/15)**(7/10):.10f}")
print(f"  修正因子 e^(−8ε_μ) = {math.exp(-8*eps_mu):.10f}")
print(f"  修正因子 e^(−(σ⁵−e^{{−16}})) = {math.exp(-(sigma**5 - math.exp(-16))):.10f}")
print(f"  修正因子 e^(−2σ⁸(1+σ)) = {math.exp(-2*sigma**8*(1+sigma)):.12f}")
print("→ 冻结级联 = 乘法因子级联（衰减链结构——每项一个乘法因子）")

# ── 3e→e^{3e} 因子身份
print("\n=== '3e'在态数层 = e^{3e} 因子（代际复合——N_gen 次递归单位复合） ===")
I_e = 3 * math.e - sigma**3 * (1 + 16/15 + math.sqrt(2/3) * (1 + 6 * sigma**3))
I_e_obs = -math.log(m_e / M_Pl) - E_tau_D
print(f"I_e(公式) = 3e − σ³(1+α_v') = {I_e:.10f}（观测反推 {I_e_obs:.10f}）")
print(f"态数比 Ω_e/Ω_τ = e^{{I_e}} = {math.exp(I_e):.4f}")
print(f"  e^{{3e}}（3 次递归单位复合——N_gen 代） = {math.exp(3*math.e):.4f}")
print(f"  e^{{−σ³(1+α_v')}}（静默冻结修正） = {math.exp(-sigma**3*(1+16/15+math.sqrt(2/3)*(1+6*sigma**3))):.8f}")
print(f"  e^{{3e}}·e^{{−σ³(1+α_v')}} = {math.exp(3*math.e)*math.exp(-sigma**3*(1+16/15+math.sqrt(2/3)*(1+6*sigma**3))):.4f}（vs 观测 {math.exp(I_e_obs):.4f}）")
print(f"  主导因子 e^{{3e}} 相对观测态数比：差 {math.exp(3*math.e)/math.exp(I_e_obs)-1:+.4f}")

# ── e/μ 解冻因子框架分解扫描
print("\n=== e/μ 解冻因子扫描（Ω_i/Ω_τ = e^{I_i}——框架量分解） ===")
rat_e = math.exp(I_e_obs)
rat_mu = math.exp(-math.log(m_mu / m_e))
print(f"Ω_e/Ω_τ = {rat_e:.4f}；Ω_μ/Ω_τ = {rat_mu:.4f}；Ω_e/Ω_μ = {math.exp(math.log(m_mu/m_e)):.4f}")
frames = [15, 16, 12, 144, 8, 27, 9, 3, 6, 42, 7, 10, 5, 2, 4, 11, 13, 17, 19, 24, 36, 48, 64]
print("候选（比 = 整数 × 框架幂次组合——穷举 2 框架幂）:")
hits = []
for a in frames:
    for b in frames:
        for ea in range(-4, 5):
            for eb in range(-4, 5):
                cand = (a ** ea) * (b ** eb)
                if cand <= 0 or abs(math.log(cand)) > 20:
                    continue
                rel = abs(math.log(rat_e) - math.log(cand))
                if rel < 0.02:  # <2% 对数距离
                    hits.append((rel, f"{a}^{ea}·{b}^{eb} = {cand:.4f}"))
hits.sort()
print("Ω_e/Ω_τ 近框架组合（对数距离<2%）前 6：")
for rel, s in hits[:6]:
    print(f"  {s}（ln 差 {rel:.4f}）")
