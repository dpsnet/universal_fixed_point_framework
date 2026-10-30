# -*- coding: utf-8 -*-
"""S174 m_ρ 链先验化探索（先证伪——M_ud_eff 框架分解）
核心问题：
- M_ud_eff(独立) = m_ud + κΛ(1−2σ/3) = 387.229（P7-6b）
- M_ud_eff(判别口径) = 387.94（后验反解——从 m_ρ 实验）
- 差 Δ = 0.711——独立先验值能否框架化命中判别口径？
- 若否：m_ρ 链 0.25σ"达标"是口径循环（后验反解）——真缺口 = M_ud_eff 独立框架导出
"""
import math

print("=== S174: m_ρ 链先验化探索 ===\n")

sigma = 1/15
m_ud = 3.45
kappa_Lambda = 401.629  # κΛ（Λ=210.2923 谱定）
M_eff_ind = m_ud + kappa_Lambda*(1 - 2*sigma/3)
M_eff_disc = 387.94  # P7-6 判别口径（后验反解）
delta = M_eff_disc - M_eff_ind
print(f"M_ud_eff(独立) = 3.45 + 401.629×(1−2σ/3) = {M_eff_ind:.4f}")
print(f"M_ud_eff(判别口径) = {M_eff_disc}（后验反解）")
print(f"差 Δ = {delta:.4f} MeV")
print(f"Δ/σ  = {delta/sigma:.2f}")
print(f"Δ 相对 m_ud = {delta/m_ud:.3f}")

# m_ρ 链检验（用两个口径分别组装）
corr = 1 - 8/10125  # 静默族修正 (k_max/N_gen)·σ³ = 8/10125
m_rho_exp = 775.26
m_rho_ind = 2*M_eff_ind*corr
m_rho_disc = 2*M_eff_disc*corr
print(f"\n=== m_ρ 链两种口径 ===")
print(f"m_ρ(独立) = 2×{M_eff_ind:.3f}×0.999210 = {m_rho_ind:.3f} vs 实验 {m_rho_exp}——差 {m_rho_exp-m_rho_ind:.3f} MeV")
print(f"m_ρ(判别) = 2×{M_eff_disc:.3f}×0.999210 = {m_rho_disc:.3f} vs 实验 {m_rho_exp}——差 {m_rho_exp-m_rho_disc:.3f} MeV")
sigma_rho = m_rho_exp*2.97e-4  # 绝对不确定度
print(f"σ_ρ,abs = {sigma_rho:.4f} MeV")
print(f"σ_score(独立) = {abs(m_rho_exp-m_rho_ind)/sigma_rho:.2f}σ ✗（不达标）")
print(f"σ_score(判别) = {abs(m_rho_exp-m_rho_disc)/sigma_rho:.2f}σ ✓（达标——口径循环）")
print(f"\n>>> 关键结论：m_ρ 链'0.25σ 达标'依赖后验反解 M_ud_eff——")
print(f">>> 独立先验 M_ud_eff = 387.229 不达标（~6σ）——")
print(f">>> 真缺口 = M_ud_eff 的独立框架导出（Δ=0.711 待解释）")

print(f"\n=== Δ=0.711 框架分解扫描 ===")
print(f"Δ = {delta:.4f}")
print(f"Δ/0.7  = {delta/0.7:.4f}（0.7 = 对合/10——S120 候选）")
print(f"Δ−0.7  = {delta-0.7:.4f}")
print(f"Δ/σ³   = {delta/sigma**3:.2f}（σ³ = 1/3375 = 2.963e-4）")
print(f"Δ×15   = {delta*15:.3f}（×SigmaInv）")
print(f"Δ×15×3 = {delta*15*3:.3f}（×SigmaInv×Ngen）")
print(f"Δ/42   = {delta/42:.4f}（/约束域）")

# m_ud 候选分解
print(f"\n=== m_ud = 3.45 框架分解 ===")
print(f"3.45/σ = {3.45/sigma:.1f}")
print(f"3.45×15 = {3.45*15:.2f}")
print(f"3.45×15×3 = {3.45*15*3:.2f}（51.75——53 接近？53 = k_max+静默²？）")
print(f"3.45 ≈ 7/2 = 3.5？——{3.5}")
print(f"3.45 ≈ e+0.73？——{math.e:.4f} + 0.73")
print(f"3.45 ≈ 2π×0.549？")
print(f"3.45 ≈ 16/4.638？")

# M_ud_eff 整体候选（框架公式扫描）
print(f"\n=== M_ud_eff = 387.229（独立）或 387.94（判别）框架候选 ===")
cands = {}
cands["4×97"] = 4*(4**2+3**4)  # 4×97 = 不动点×(不动点²+活跃⁴)
cands["16×24.2"] = 16*24.2
cands["8×48.404"] = 8*48.404
cands["42×9.224"] = 42*9.224
cands["15×25.815"] = 15*25.815
cands["7×55.42"] = 7*55.42
cands["3×129.08"] = 3*129.08
cands["388−6/100"] = 388 - 6/100
for name, v in cands.items():
    d1 = v - M_eff_ind
    d2 = v - M_eff_disc
    print(f"  {name:14s} = {v:.3f}  vs 独立差 {d1:+.3f}（{abs(d1)/M_eff_ind*100:.3f}%） vs 判别差 {d2:+.3f}")

# 判别口径 = 独立 + 0.7 + ε？
print(f"\n=== 判别口径 = 独立 + 0.7 + 修正？ ===")
print(f"M_eff_disc − (M_eff_ind + 0.7) = {M_eff_disc - M_eff_ind - 0.7:.4f}")
print(f"0.011 ≈ σ×静默/3×1.5？ σ×5/3 = {sigma*5/3:.5f}")
print(f"0.011 ≈ 1/90 = {1/90:.6f}（1/(活跃²×幂基×静默)？）")
print(f"0.011 ≈ 静默⁻³×活跃²×σ？ 5³×9/15 = {125*9/15:.2f}（75——不）")
print(f"0.011 ≈ ε_μ？ ε_μ = e^{{-16}} = {math.e**(-16):.3e}（不）")
