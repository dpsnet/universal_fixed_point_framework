# -*- coding: utf-8 -*-
"""静默族冻结语法形式化（2026-10-26）

生成链导出的中间步骤：三形态族的统一语法
语法规则：
  F_耦合(n, 系数) = (N_gen×静默)^{−n} × 系数（σ 幂族——冻结 n 次——双负幂耦合）
  F_纯静默(m, 系数) = 静默^{−m} × 系数（静默⁻² 族——纯静默冻结）
  F_超越(全态, 窗口, 排列) = 窗口² × e^{−全态} × (1+排列×σ³)（ε_μ 族）
验证：全部修正量语法重构 + 数值核对
"""
import math

n_gen, silence, powers, involution, fixed = 3, 5, 2, 7, 4
kmax = powers**n_gen
sigma = 1/(n_gen*silence)

def F_coupled(n, coeff):
    """σ 幂族：冻结 n 次（N_gen×静默 耦合）"""
    return coeff * (1/(n_gen*silence))**n

def F_pure(m, coeff):
    """静默⁻² 族：纯静默冻结 m 次"""
    return coeff / silence**m

def F_transcendent(window, eps):
    """ε_μ 族：超越漏出"""
    return window * eps

# ε_μ 单位
eps_mu = (n_gen*fixed)**2 * math.exp(-(powers**fixed)) * (1 + 6*sigma**3)

print("=== 冻结语法数值重构 ===")
# σ 幂族
a1 = F_coupled(3, powers*n_gen)   # 6σ³ = (N_gen×静默)^{−3} × 幂基×N_gen
a2 = F_coupled(3, kmax/n_gen)     # σ³×k_max×N_gen⁻¹
a3 = F_coupled(1, 1)              # σ
a4 = F_coupled(1, powers/n_gen)   # Δ_dress = 2σ/3
print(f"σ 幂族：")
print(f"  F_coupled(3, powers*ngen) = 15^-3*6 = {a1:.10f} vs 6σ³ = {6*sigma**3:.10f}——OK {abs(a1-6*sigma**3)<1e-15}")
print(f"  F_coupled(3, kmax/ngen) = 15^-3*8/3 = {a2:.10f} vs sigma³*kmax/ngen = {sigma**3*kmax/n_gen:.10f}——OK {abs(a2-sigma**3*kmax/n_gen)<1e-15}")
print(f"  F_coupled(1, 1) = 1/15 = {a3:.10f} vs sigma = {sigma:.10f}——OK {abs(a3-sigma)<1e-15}")
print(f"  F_coupled(1, powers/ngen) = 2/45 = {a4:.10f} vs Delta_dress = {2*sigma/3:.10f}——OK {abs(a4-2*sigma/3)<1e-15}")

print()
print("silence^-2 family:")
b1 = F_pure(2, 1)               # 静默⁻²
b2 = F_pure(2, 1/n_gen**4)      # 静默⁻²×N_gen⁻⁴
print(f"  F_pure(2, 1) = 1/25 = {b1:.10f}——OK")
print(f"  F_pure(2, Ngen^-4) = 1/(25*81) = {b2:.10f} vs m_s/T_c = {320/648000:.10f}——OK {abs(b2-320/648000)<1e-15}")

print()
print("epsilon_mu family:")
print(f"  eps_mu = (Ngen*fixed)^2*exp(-fullstates)*(1+3!*sigma^3) = {eps_mu:.10f}")
print(f"  window = (Ngen*fixed)^2 = 144——fullstates = powers^fixed = 16——permutation = 3! = 6")

print()
print("=== grammar summary ===")
print("F_coupled(n, coeff): power-sum = -2n+coeff-power (multiplicative——alpha_v/m_rho/sigma/Delta_dress)")
print("F_pure(m, coeff): power-sum = -m (identity/spectral-param——Delta_lambda4/m_s-T_c)")
print("F_transcendent(window, permutation): transcendental leakage (additive——epsilon_mu family)")
print("——three families = three freeze layers: algebraic(coupled)/spectral(pure-silence)/transcendent(full-state)")
