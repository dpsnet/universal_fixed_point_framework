"""诊断 Kerr QNM 求解问题"""
import numpy as np
import cmath

print("=" * 70)
print("诊断 Kerr QNM 求解问题")
print("=" * 70)
print()

from leaver_corrected_solver import CorrectedLeaverQNMSolver, LeaverRadialSolver, LeaverAngularSolver

# 测试 a=0.5, l=2, m=2
a_val = 0.5
l = 2
m = 2
n = 0

print(f"测试: a={a_val}, l={l}, m={m}, n={n}")
print()

# 参考频率
omega_ref = complex(0.495007, -0.093885)
print(f"参考频率: {omega_ref.real:.6f} {omega_ref.imag:+.6f}i")

# 计算参考频率处的残差
solver = CorrectedLeaverQNMSolver(M=1.0, a=a_val, s=-2, max_iter=300)
res_ref = solver._combined_residual(omega_ref, l, m, a_val, n_inv=n)
print(f"参考频率处残差: {abs(res_ref):.2e}")
print()

# 看看我们的求解器找到了什么
result = solver.solve(l=l, m=m, n=n, tol=1e-8)
omega_my = result["omega"]
print(f"我们找到的频率: {omega_my.real:.6f} {omega_my.imag:+.6f}i")
print(f"残差: {result['residual']:.2e}")
print(f"差值: {abs(omega_my - omega_ref):.6f}")
print()

# 让我们扫描一下复平面，看看有几个根
print("--- 扫描复平面寻找根 ---")

real_range = np.linspace(0.2, 0.7, 50)
imag_range = np.linspace(-0.3, 0.0, 50)

min_res = float('inf')
best_omega = None

for re in real_range:
    for im in imag_range:
        omega = complex(re, im)
        try:
            res = abs(solver._combined_residual(omega, l, m, a_val, n_inv=n))
            if res < min_res:
                min_res = res
                best_omega = omega
        except:
            pass

print(f"扫描找到的最佳点: {best_omega.real:.6f} {best_omega.imag:+.6f}i, 残差: {min_res:.2e}")
print()

# 让我们用 Newton-Raphson 从参考频率出发
print("--- 从参考频率出发的 Newton-Raphson ---")
result_from_ref = solver._newton_raphson(omega_ref, l, m, a_val, n_inv=n, tol=1e-10)
print(f"结果: {result_from_ref['omega'].real:.6f} {result_from_ref['omega'].imag:+.6f}i")
print(f"残差: {result_from_ref['residual']:.2e}")
print(f"收敛: {result_from_ref['converged']}")
print()

# 从我们找到的解出发
print("--- 从我们的解出发的 Newton-Raphson (n_inv=0) ---")
result_from_my = solver._newton_raphson(omega_my, l, m, a_val, n_inv=0, tol=1e-10)
print(f"结果: {result_from_my['omega'].real:.6f} {result_from_my['omega'].imag:+.6f}i")
print(f"残差: {result_from_my['residual']:.2e}")
print(f"收敛: {result_from_my['converged']}")
print()

# 试试不同的 n_inv
print("--- 不同 n_inv 值的残差 ---")
for n_inv in range(5):
    res = abs(solver._combined_residual(omega_ref, l, m, a_val, n_inv=n_inv))
    print(f"  n_inv={n_inv}: |CF| = {res:.2e}")
print()

# 看看参考频率在不同 n_inv 下的 Newton 收敛
print("--- 参考频率在不同 n_inv 下的 Newton 收敛 ---")
for n_inv in range(3):
    result = solver._newton_raphson(omega_ref, l, m, a_val, n_inv=n_inv, tol=1e-10, max_newton=100)
    print(f"  n_inv={n_inv}: ω = {result['omega'].real:.6f} {result['omega'].imag:+.6f}i, |CF|={result['residual']:.2e}, conv={result['converged']}")
