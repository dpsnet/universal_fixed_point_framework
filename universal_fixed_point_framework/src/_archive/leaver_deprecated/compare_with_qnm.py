# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""与 qnm 包的全面对比测试"""
import numpy as np
import cmath

print("=" * 70)
print("与 qnm 包的全面对比测试")
print("=" * 70)
print()

# 测试 1: 角向分离常数对比
print("--- 测试 1: 角向分离常数对比 ---")
try:
    from qnm.angular import C_and_sep_const_closest
    
    test_cases = [
        (0.0, 2, 0, complex(0.373672, -0.088962)),
        (0.5, 2, 2, complex(0.495007, -0.093885)),
        (0.5, 2, 0, complex(0.355051, -0.095299)),
        (0.7, 2, 1, complex(0.398010, -0.092386)),
    ]
    
    from leaver_corrected_solver import LeaverAngularSolver
    my_angular = LeaverAngularSolver(s=-2, l_max=20)
    
    for a, l, m, omega in test_cases:
        c = a * omega
        A0 = l*(l+1) - (-2)*(-2+1)
        A_ref, _ = C_and_sep_const_closest(A0, s=-2, c=c, m=m, l_max=20)
        my_result = my_angular.solve_separation_constant(l, m, omega, a)
        A_my = my_result["A"]
        
        diff = abs(A_my - A_ref)
        rel_err = diff / abs(A_ref)
        
        print(f"a={a}, l={l}, m={m}:")
        print(f"  qnm:  A = {A_ref.real:.6f} {A_ref.imag:+.6f}i")
        print(f"  我们: A = {A_my.real:.6f} {A_my.imag:+.6f}i")
        print(f"  相对误差: {rel_err:.6f}")
        print()
except Exception as e:
    print(f"角向对比失败: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试 2: 径向连分数残差对比
print("--- 测试 2: 径向连分数残差对比 ---")
try:
    from qnm.radial import leaver_cf_inv_lentz
    from leaver_corrected_solver import LeaverRadialSolver, LeaverAngularSolver
    
    my_radial = LeaverRadialSolver(M=1.0, a=0.5, s=-2, max_iter=500)
    my_angular = LeaverAngularSolver(s=-2, l_max=20)
    
    test_cases = [
        (0.5, 2, 2, complex(0.495007, -0.093885)),
        (0.5, 2, 0, complex(0.355051, -0.095299)),
    ]
    
    for a, l, m, omega in test_cases:
        A0 = l*(l+1) - (-2)*(-2+1)
        A_ref, _ = C_and_sep_const_closest(A0, s=-2, c=a*omega, m=m, l_max=20)
        
        cf_ref, err_ref, n_ref = leaver_cf_inv_lentz(omega=omega, a=a, s=-2, m=m, A=A_ref, n_inv=0)
        
        my_radial.a = a
        my_result = my_angular.solve_separation_constant(l, m, omega, a)
        A_my = my_result["A"]
        cf_my = my_radial.leaver_cf(omega, A_my, m, n_inv=0)
        
        print(f"a={a}, l={l}, m={m}:")
        print(f"  qnm:  CF = {cf_ref.real:.6f} {cf_ref.imag:+.6f}i (|CF|={abs(cf_ref):.2e})")
        print(f"  我们: CF = {cf_my.real:.6f} {cf_my.imag:+.6f}i (|CF|={abs(cf_my):.2e})")
        print(f"  CF 差值: {abs(cf_my - cf_ref):.2e}")
        print(f"  A 差值: {abs(A_my - A_ref):.2e}")
        print()
except Exception as e:
    print(f"径向对比失败: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试 3: 使用 qnm 的角向分离常数 + 我们的径向连分数
print("--- 测试 3: qnm 角向 + 我们的径向 ---")
try:
    from qnm.angular import C_and_sep_const_closest
    from qnm.radial import leaver_cf_inv_lentz
    from leaver_corrected_solver import LeaverRadialSolver
    
    my_radial = LeaverRadialSolver(M=1.0, a=0.5, s=-2, max_iter=500)
    
    test_cases = [
        (0.5, 2, 2, complex(0.495007, -0.093885)),
        (0.5, 2, 0, complex(0.355051, -0.095299)),
    ]
    
    for a, l, m, omega in test_cases:
        A_ref, _, _ = C_and_sep_const_closest(a*omega, s=-2, l=l, m=m)
        
        cf_ref, err_ref, n_ref = leaver_cf_inv_lentz(omega=omega, a=a, s=-2, m=m, A=A_ref, n_inv=0)
        
        my_radial.a = a
        cf_my = my_radial.leaver_cf(omega, A_ref, m, n_inv=0)
        
        print(f"a={a}, l={l}, m={m}:")
        print(f"  qnm:  CF = {cf_ref.real:.6f} {cf_ref.imag:+.6f}i (|CF|={abs(cf_ref):.2e})")
        print(f"  我们: CF = {cf_my.real:.6f} {cf_my.imag:+.6f}i (|CF|={abs(cf_my):.2e})")
        print(f"  差值: {abs(cf_my - cf_ref):.2e}")
        print()
except Exception as e:
    print(f"测试 3 失败: {e}")
    import traceback
    traceback.print_exc()
