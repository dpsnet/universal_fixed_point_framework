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

"""测试 Kerr 情况的连分数"""
import sys
sys.path.insert(0, 'src')
from leaver_final_solver import LeaverFinalSolver
import numpy as np
import cmath

print("=" * 60)
print("测试 Kerr 径向连分数")
print("=" * 60)

# 测试 a=0.5, l=2, m=0
# 参考值: omega = 0.355051 - 0.095299i
ref_omega = complex(0.355051, -0.095299)

solver = LeaverFinalSolver(M=1.0, a=0.5, s=-2, max_iter=500)

# 计算角向本征值
A_lm = complex(2 * 3 - (-2) * (-2 + 1), 0.0)  # l(l+1) - s(s+1) = 6 - 2 = 4
print(f"初始 A_lm = {A_lm}")

# 先求角向本征值
for i in range(20):
    f_ang = solver._angular_cf(A_lm, ref_omega, 0, 2)
    print(f"  角向迭代 {i}: A = {A_lm.real:.6f}, 残差 = {abs(f_ang):.2e}")
    if abs(f_ang) < 1e-10:
        break
    f_ang_re = solver._angular_cf(A_lm + 1e-6, ref_omega, 0, 2)
    df_ang = (f_ang_re - f_ang) / 1e-6
    if abs(df_ang) > 1e-15:
        A_lm -= f_ang / df_ang

print(f"角向本征值: A_lm = {A_lm.real:.6f} {A_lm.imag:.6f}i")
print()

# 计算径向残差
radial_res = solver._kerr_radial_cf(ref_omega, A_lm, 0)
print(f"参考频率处的径向残差 (乘积形式): {abs(radial_res):.2e}")

# 用 Newton 法找根
print()
print("用 Newton 法找根...")
omega = complex(ref_omega)
for i in range(30):
    # 先更新角向本征值
    A_curr = complex(4.0, 0.0)
    for j in range(10):
        f_ang = solver._angular_cf(A_curr, omega, 0, 2)
        if abs(f_ang) < 1e-10:
            break
        f_ang_re = solver._angular_cf(A_curr + 1e-6, omega, 0, 2)
        df_ang = (f_ang_re - f_ang) / 1e-6
        if abs(df_ang) > 1e-15:
            A_curr -= f_ang / df_ang
    
    f = solver._kerr_radial_cf(omega, A_curr, 0)
    res = abs(f)
    print(f"  迭代 {i}: omega = {omega.real:.8f} {omega.imag:.8f}i, 残差 = {res:.2e}")
    
    if res < 1e-10:
        break
    
    eps = 1e-8
    # 计算 f(omega+eps) 和 f(omega+i*eps)
    A_re = complex(4.0, 0.0)
    for j in range(10):
        f_ang = solver._angular_cf(A_re, omega + eps, 0, 2)
        if abs(f_ang) < 1e-10:
            break
        f_ang_re = solver._angular_cf(A_re + 1e-6, omega + eps, 0, 2)
        df_ang = (f_ang_re - f_ang) / 1e-6
        if abs(df_ang) > 1e-15:
            A_re -= f_ang / df_ang
    f_re = solver._kerr_radial_cf(omega + eps, A_re, 0)
    
    A_im = complex(4.0, 0.0)
    for j in range(10):
        f_ang = solver._angular_cf(A_im, omega + 1j * eps, 0, 2)
        if abs(f_ang) < 1e-10:
            break
        f_ang_re = solver._angular_cf(A_im + 1e-6, omega + 1j * eps, 0, 2)
        df_ang = (f_ang_re - f_ang) / 1e-6
        if abs(df_ang) > 1e-15:
            A_im -= f_ang / df_ang
    f_im = solver._kerr_radial_cf(omega + 1j * eps, A_im, 0)
    
    df_dre = (f_re - f) / eps
    df_dim = (f_im - f) / eps
    
    jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
    rhs = -np.array([f.real, f.imag])
    
    try:
        delta = np.linalg.solve(jacobian, rhs)
        omega += complex(delta[0], delta[1])
    except np.linalg.LinAlgError:
        omega -= 0.01 * f

print()
print(f"最终: omega = {omega.real:.8f} {omega.imag:.8f}i")
print(f"参考: omega = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
print(f"偏差: DeltaRe = {abs(omega.real - ref_omega.real):.2e}, DeltaIm = {abs(omega.imag - ref_omega.imag):.2e}")
