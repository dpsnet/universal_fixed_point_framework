#!/usr/bin/env python3
"""
debug_spectral_fast.py

诊断两弦法不收敛的原因。
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.linalg import eigvals
from leaver_unified_solver import (
    TridiagonalSpectralSolver, LeaverUnifiedSolver,
    _tridiagonal_solve, LeaverResidual
)

# 测试参数：Schwarzschild a=0, l=2, m=0
M, a, s = 1.0, 0.0, -2

# Berti 参考值
omega_ref = complex(0.373672, -0.088962)

# 对不同的 ω 检查三对角矩阵的最小特征值
print("=" * 80)
print("诊断 1：不同 ω 处三对角矩阵的谱结构")
print("=" * 80)

spectral = TridiagonalSpectralSolver(M=M, a=a, s=s, n_dim=80)
leaver = LeaverResidual(M=M, a=a, s=s)

for rel_factor in [1.0, 0.999, 0.99, 0.98, 0.95, 1.05, 1.1]:
    omega = complex(omega_ref.real * rel_factor, omega_ref.imag * rel_factor)
    lam = complex(leaver.spheroidal_eigenvalue_approx(2, 0, omega), 0.0)

    # 全特征值分解
    lower, diag, upper = spectral._get_tridiagonal_diags(omega, lam, m=0)
    M_mat = np.zeros((len(diag), len(diag)), dtype=complex)
    for i in range(len(diag)):
        M_mat[i,i] = diag[i]
        if i < len(diag)-1:
            M_mat[i,i+1] = upper[i]
            M_mat[i+1,i] = lower[i+1]
    all_eig = eigvals(M_mat)
    min_idx = np.argmin(np.abs(all_eig))
    min_eig = all_eig[min_idx]

    # 两弦法残差
    fast_res = spectral.spectral_residual_fast(omega, lam, m=0)

    # 连分数残差
    cf_res = leaver.full_residual(omega, 2, 0)

    print(f"\n  ω/ω_ref = {rel_factor:.3f}")
    print(f"    ω = {omega.real:.8f} {omega.imag:+.8f}i")
    print(f"    谱最小|λ| = {abs(min_eig):.2e}")
    print(f"    最小 λ = {min_eig.real:.8f} {min_eig.imag:+.8f}i")
    print(f"    两弦法残差 = {abs(fast_res):.2e}")
    print(f"    CF 残差 = {abs(cf_res):.2e}")

print("\n" + "=" * 80)
print("诊断 2：Rayleigh 商迭代收敛轨迹")
print("=" * 80)

# 用 Berti 参考值附近的 ω 测试 Rayleigh 商迭代
omega = complex(omega_ref)
lam = complex(leaver.spheroidal_eigenvalue_approx(2, 0, omega), 0.0)
lower, diag, upper = spectral._get_tridiagonal_diags(omega, lam, m=0)
v0 = spectral._physical_initial_vector(lower, diag, upper)
Mv0 = spectral._tridiag_matvec(lower, diag, upper, v0)
mu0 = np.vdot(v0, Mv0)
print(f"\n  物理初始向量 Rayleigh 商 = {mu0.real:.6f} {mu0.imag:+.6f}i")

# Rayleigh 商迭代
v = v0.copy()
mu = mu0
for it in range(10):
    shifted = diag - mu
    w = _tridiagonal_solve(lower, shifted, upper, v)
    w_norm = np.linalg.norm(w)
    if w_norm < 1e-30:
        print(f"  迭代 {it}: ||w|| 过小，停止")
        break
    w /= w_norm
    Mw = spectral._tridiag_matvec(lower, diag, upper, w)
    mu_new = np.vdot(w, Mw)
    print(f"  迭代 {it}: μ = {mu_new.real:.8f} {mu_new.imag:+.8f}i, "
          f"δ = {abs(mu_new-mu):.2e}")
    if abs(mu_new - mu) < 1e-14:
        break
    mu, v = mu_new, w

# 与全特征值分解比较
print("\n  全特征值分解结果 (前5个最小|λ|):")
idx_sorted = np.argsort(np.abs(all_eig))
for i in range(min(5, len(idx_sorted))):
    idx = idx_sorted[i]
    print(f"    λ[{idx}] = {all_eig[idx].real:.8f} {all_eig[idx].imag:+.8f}i, "
          f"|λ| = {abs(all_eig[idx]):.2e}")

print("\n" + "=" * 80)
print("诊断 3：解耦测试 — 直接在 ω_ref 处求 Newton 步")
print("=" * 80)

# 在 ω_ref 处计算 Jacobian
for variation in [0.0, 1e-6]:
    delta = 1e-6
    residual = lambda w: spectral.full_residual(w, 2, 0)

    f0 = residual(omega)
    f_re = residual(omega + delta)
    f_im = residual(omega + 1j*delta)
    df_dre = (f_re - f0) / delta
    df_dim = (f_im - f0) / delta

    J = np.array([[df_dre.real, df_dim.real],
                  [df_dre.imag, df_dim.imag]])
    print(f"\n  ω = {omega.real:.8f} {omega.imag:+.8f}i")
    print(f"  f(ω) = {f0.real:.8f} {f0.imag:+.8f}i, |f| = {abs(f0):.2e}")
    print(f"  Jacobian = {J}")
    if abs(np.linalg.det(J)) > 1e-30:
        delta_omega = np.linalg.solve(J, -np.array([f0.real, f0.imag]))
        step = complex(delta_omega[0], delta_omega[1])
        print(f"  Newton step = {step.real:.2e} {step.imag:+.2e}i")
        print(f"  |step| = {abs(step):.2e}")
    else:
        print("  Jacobian 奇异！")
