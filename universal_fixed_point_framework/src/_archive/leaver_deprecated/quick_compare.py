"""快速对比 qnm 包的 QNM 频率"""
import numpy as np

print("=" * 70)
print("快速对比 qnm 包的 QNM 频率")
print("=" * 70)
print()

from qnm.radial import leaver_cf_inv_lentz
from qnm.angular import C_and_sep_const_closest

def newton_raphson_qnm(omega_guess, a, s, m, l, n_inv, tol=1e-10, max_iter=50):
    """用 qnm 包的函数做 Newton-Raphson"""
    omega = omega_guess
    
    for i in range(max_iter):
        A0 = l*(l+1) - s*(s+1)
        A, _ = C_and_sep_const_closest(A0, s=s, c=a*omega, m=m, l_max=20)
        cf, err, n_frac = leaver_cf_inv_lentz(omega=omega, a=a, s=s, m=m, A=A, n_inv=n_inv)
        
        if abs(cf) < tol:
            return omega, abs(cf), True, i+1
        
        delta = 1e-6
        A2, _ = C_and_sep_const_closest(A0, s=s, c=a*(omega+delta), m=m, l_max=20)
        cf2, err2, _ = leaver_cf_inv_lentz(omega=omega+delta, a=a, s=s, m=m, A=A2, n_inv=n_inv)
        dcf = (cf2 - cf) / delta
        
        if abs(dcf) > 1e-15:
            omega -= cf / dcf
    
    A0 = l*(l+1) - s*(s+1)
    A, _ = C_and_sep_const_closest(A0, s=s, c=a*omega, m=m, l_max=20)
    cf, _, _ = leaver_cf_inv_lentz(omega=omega, a=a, s=s, m=m, A=A, n_inv=n_inv)
    return omega, abs(cf), False, max_iter

# 测试用例
test_cases = [
    (0.0, 2, 0, 0, complex(0.373672, -0.088962), "Schwarzschild l=2, m=0, n=0"),
    (0.5, 2, 0, 0, complex(0.37, -0.09), "Kerr a=0.5, l=2, m=0, n=0"),
    (0.5, 2, 2, 0, complex(0.5, -0.1), "Kerr a=0.5, l=2, m=2, n=0"),
    (0.7, 2, 1, 0, complex(0.4, -0.09), "Kerr a=0.7, l=2, m=1, n=0"),
]

for a, l, m, n, guess, desc in test_cases:
    print(f"--- {desc} ---")
    omega, res, converged, iters = newton_raphson_qnm(guess, a, -2, m, l, n)
    print(f"  qnm Newton: ω = {omega.real:.6f} {omega.imag:+.6f}i")
    print(f"  残差: {res:.2e}, 收敛: {converged}, 迭代: {iters}")
    
    if a == 0.0:
        print(f"  参考 (Berti): 0.373672 -0.088962i")
    elif a == 0.5 and m == 0:
        print(f"  参考 (Berti): 0.355051 -0.095299i")
    elif a == 0.5 and m == 2:
        print(f"  参考 (Berti): 0.495007 -0.093885i")
    elif a == 0.7 and m == 1:
        print(f"  参考 (Berti): 0.398010 -0.092386i")
    print()

# 对比我们的求解器
print("=" * 70)
print("与我们的求解器对比")
print("=" * 70)
print()

from leaver_corrected_solver import CorrectedLeaverQNMSolver

for a, l, m, n, guess, desc in test_cases:
    print(f"--- {desc} ---")
    
    solver = CorrectedLeaverQNMSolver(M=1.0, a=a, s=-2, max_iter=300)
    
    # 用相同的初始猜测
    result = solver._newton_raphson(guess, l, m, a, n_inv=n, tol=1e-10)
    
    # qnm 的结果
    omega_qnm, res_qnm, _, _ = newton_raphson_qnm(guess, a, -2, m, l, n)
    
    print(f"  我们的求解器: ω = {result['omega'].real:.6f} {result['omega'].imag:+.6f}i, |CF|={result['residual']:.2e}")
    print(f"  qnm 包:     ω = {omega_qnm.real:.6f} {omega_qnm.imag:+.6f}i, |CF|={res_qnm:.2e}")
    print(f"  差值: {abs(result['omega'] - omega_qnm):.2e}")
    print()
