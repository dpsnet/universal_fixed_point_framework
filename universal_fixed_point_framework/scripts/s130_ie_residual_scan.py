# -*- coding: utf-8 -*-
# s130_ie_residual_scan.py —— I_e 公式残余 1.9e-9 的修正项候选扫描（S130，2026-10-27）
# 目标：定位 I_e = 3e − σ³(1+α_v') 残余 δ = I_e(公式) − I_e(观测) ≈ 1.9e-9
#   （σ_score 6.4——组装链 E_e 不达标瓶颈）——先证伪：扫描 σ 幂次 × 框架系数
#   找整洁候选——无则维持开放（禁强行拟合——S107/S118 教训）
# 依赖：pyenv 3.11.8
import math

sigma = 1 / 15
ln15 = math.log(15)

# ── I_e 公式（S109 后验组装）
alpha_vp = 16 / 15 + math.sqrt(2 / 3) * (1 + 6 * sigma**3)
I_e_formula = 3 * math.e - sigma**3 * (1 + alpha_vp)

# ── I_e 观测反推（E_e(PDG) − E_τ^D——严格口径）
M_Pl = 1.220890e22
m_e = 0.51099895069
E_e_obs = -math.log(m_e / M_Pl)
eps_mu = 144 * math.exp(-16) * (1 + 6 * sigma**3)
E_tau_D = (16 * ln15 + (7 / 10) * math.log(16 / 15)
           - 8 * eps_mu - (sigma**5 - math.exp(-16)) - 2 * sigma**8 * (1 + sigma))
I_e_obs = E_e_obs - E_tau_D
delta = I_e_formula - I_e_obs

print("=== I_e 残余精确定位 ===")
print(f"I_e(公式) = {I_e_formula:.12f}")
print(f"I_e(观测) = {I_e_obs:.12f}")
print(f"δ = I_e(公式) − I_e(观测) = {delta:+.3e}")
print(f"σ_score = |δ|/σ_rel(e) = {abs(delta)/2.94e-10:.3f}（>1 不达标——瓶颈确认）")

# ── 候选扫描：δ ≈ c·σ^a（a ∈ {1..9}，c ∈ 框架量系数）
print("\n=== σ 幂次 × 框架系数扫描（δ/c 的整洁度） ===")
coeffs = [1, 2, 3, 4, 6, 8, 12, 15, 16, 16/3, 8/3, 15/16, 7/10, 2/3,
          9/4, 3/2, 5/3, 7/5, 11/15, 1/3, 2/5, 3/5, 1/2, 1/4, 3/4,
          144, 72, 36, 24, 48, 32, 81, 27, 9, 5, 7, 10, 11, 13, 17, 19,
          7/3, 5/2, 11/3, 13/3, 17/3, 19/3, 23/3, 1/15, 1/5, 1/7, 1/9]
best = []
for a in range(1, 10):
    for c in coeffs:
        cand = c * sigma**a
        if cand == 0:
            continue
        ratio = delta / cand
        # 整洁度：ratio 接近整数
        for r in [ratio, 1/ratio]:
            rnd = round(r)
            if abs(rnd) >= 1 and abs(rnd) <= 60:
                rel = abs(r - rnd) / abs(rnd)
                best.append((rel, a, c, cand, rnd))
best.sort()
print("最整洁候选（δ = 系数×整数×σ^a）前 12：")
for rel, a, c, cand, rnd in best[:12]:
    print(f"  a={a} c={c:.6g} σ^{a}×c={cand:.4e}——δ/候选 = {rnd:.4f}（相对差 {rel*100:.3f}%）")

# ── 关键：修正项的相对量级（δ 相对 I_e 主项）
print(f"\nδ/I_e = {delta/I_e_formula:.3e}（2e-9 相对——微扰级）")
print(f"σ⁷/3 = {sigma**7/3:.4e}（差 {(delta/(sigma**7/3)-1)*100:+.2f}%）")
print(f"σ⁸·(16/3) = {sigma**8*16/3:.4e}（差 {(delta/(sigma**8*16/3)-1)*100:+.2f}%）")
print(f"2σ⁸(1+σ) = {2*sigma**8*(1+sigma):.4e}（差 {(delta/(2*sigma**8*(1+sigma))-1)*100:+.2f}%）")
print(f"σ⁷/3×(1−σ/5) = {sigma**7/3*(1-sigma/5):.4e}（差 {(delta/(sigma**7/3*(1-sigma/5))-1)*100:+.2f}%）")
