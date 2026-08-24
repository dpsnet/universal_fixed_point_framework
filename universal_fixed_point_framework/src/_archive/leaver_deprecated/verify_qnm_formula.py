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

"""验证 qnm 包的径向连分数系数公式"""
import cmath
import numpy as np

# 测试参数
M = 1.0
a = 0.0
s = -2
l = 2
m = 0
omega = complex(0.373672, -0.088962)
A_lm = l * (l + 1) - s * (s + 1)  # Schwarzschild 极限

print("=" * 60)
print("验证 qnm 包的径向连分数公式")
print("=" * 60)
print(f"omega = {omega.real:.6f} {omega.imag:+.6f}i")
print(f"a = {a}, M = {M}, s = {s}, l = {l}, m = {m}")
print(f"A_lm = {A_lm}")
print()

# 方法1: qnm 包的 D_coeffs 公式
def sing_pt_char_exps(omega, a, s, m):
    """qnm 包中的奇异点特征指数"""
    root = np.sqrt(1. - a*a)
    r_p, r_m = 1. + root, 1. - root
    sigma_p = (2.*omega*r_p - m*a)/(2.*root)
    sigma_m = (2.*omega*r_m - m*a)/(2.*root)
    zeta = +1.j * omega
    xi   = - s - 1.j * sigma_p
    eta  = -1.j * sigma_m
    return zeta, xi, eta

def D_coeffs(omega, a, s, m, A):
    """qnm 包中的 D_0-D_4 系数"""
    zeta, xi, eta = sing_pt_char_exps(omega, a, s, m)
    root  = np.sqrt(1. - a*a)
    p     = root * zeta
    alpha = 1. + s + xi + eta - 2.*zeta + s
    gamma = 1. + s + 2.*eta
    delta = 1. + s + 2.*xi
    sigma = (A + a*a*omega*omega - 8.*omega*omega
             + p * (2.*alpha + gamma - delta)
             + (1. + s - 0.5*(gamma + delta))
             * (s + 0.5*(gamma + delta)))
    D = [0.j] * 5
    D[0] = delta
    D[1] = 4.*p - 2.*alpha + gamma - delta - 2.
    D[2] = 2.*alpha - gamma + 2.
    D[3] = alpha*(4.*p - delta) - sigma
    D[4] = alpha*(alpha - gamma + 1.)
    return D

D = D_coeffs(omega, a, s, m, A_lm)
print("--- D_coeffs (qnm 公式) ---")
for i in range(5):
    print(f"D[{i}] = {D[i].real:.6f} {D[i].imag:+.6f}i")
print()

# 二次多项式系数
def alpha_n_qnm(n, D):
    return n*n + (D[0] + 1.)*n + D[0]

def beta_n_qnm(n, D):
    return -2.*n*n + (D[1] + 2.)*n + D[3]

def gamma_n_qnm(n, D):
    return n*n + (D[2] - 3.)*n + D[4] - D[2] + 2.

print("--- 二次多项式系数 ---")
for n in [0, 1, 2, 5]:
    print(f"n = {n}:")
    print(f"  alpha = {alpha_n_qnm(n, D).real:.6f} {alpha_n_qnm(n, D).imag:+.6f}i")
    print(f"  beta  = {beta_n_qnm(n, D).real:.6f} {beta_n_qnm(n, D).imag:+.6f}i")
    print(f"  gamma = {gamma_n_qnm(n, D).real:.6f} {gamma_n_qnm(n, D).imag:+.6f}i")
print()

# 方法2: Leaver 1991 Schwarzschild 公式（已验证正确）
omega_leaver = 2.0 * M * omega
rho = -1j * omega_leaver
epsilon_grav = 3.0

def alpha_1991(n):
    return n**2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0

def beta_1991(n):
    return -(2.0 * n**2 + (8.0 * rho + 2.0) * n + 8.0 * rho**2 + 4.0 * rho + l * (l + 1.0) - epsilon_grav)

def gamma_1991(n):
    return n**2 + 4.0 * rho * n + 4.0 * rho**2 - epsilon_grav - 1.0

print("--- Leaver 1991 系数（已验证正确）---")
for n in [0, 1, 2, 5]:
    print(f"n = {n}:")
    print(f"  alpha = {alpha_1991(n).real:.6f} {alpha_1991(n).imag:+.6f}i")
    print(f"  beta  = {beta_1991(n).real:.6f} {beta_1991(n).imag:+.6f}i")
    print(f"  gamma = {gamma_1991(n).real:.6f} {gamma_1991(n).imag:+.6f}i")
print()

# 比较两种方法的系数比值
print("--- 系数比值 (qnm / 1991) ---")
for n in [0, 1, 2, 5]:
    print(f"n = {n}:")
    ratio_a = alpha_n_qnm(n, D) / alpha_1991(n)
    ratio_b = beta_n_qnm(n, D) / beta_1991(n)
    ratio_g = gamma_n_qnm(n, D) / gamma_1991(n)
    print(f"  alpha 比值: {abs(ratio_a):.6f}, 角度: {cmath.phase(ratio_a)*180/cmath.pi:.2f}°")
    print(f"  beta  比值: {abs(ratio_b):.6f}, 角度: {cmath.phase(ratio_b)*180/cmath.pi:.2f}°")
    print(f"  gamma 比值: {abs(ratio_g):.6f}, 角度: {cmath.phase(ratio_g)*180/cmath.pi:.2f}°")
print()

# 计算连分数残差
print("--- 连分数残差 ---")
max_iter = 500

# 方法1: qnm 的反转形式 (n_inv = 0)
def leaver_cf_trunc_inversion(omega, a, s, m, A, n_inv, N=500):
    """qnm 包中的截断反转连分数"""
    D = D_coeffs(omega, a, s, m, A)
    
    n_arr = np.arange(0, N+1)
    alpha =     n_arr*n_arr + (D[0] + 1.)*n_arr + D[0]
    beta  = -2.*n_arr*n_arr + (D[1] + 2.)*n_arr + D[3]
    gamma =     n_arr*n_arr + (D[2] - 3.)*n_arr + D[4] - D[2] + 2.
    
    conv1 = 0.j
    for i in range(0, n_inv):
        conv1 = alpha[i] / (beta[i] - gamma[i] * conv1)
    
    conv2 = 0.j
    for i in range(N, n_inv, -1):
        conv2 = gamma[i] / (beta[i] - alpha[i] * conv2)
    
    return (beta[n_inv] - gamma[n_inv] * conv1 - alpha[n_inv] * conv2)

res_qnm = leaver_cf_trunc_inversion(omega, a, s, m, A_lm, 0, N=max_iter)
print(f"qnm 反转形式 (n_inv=0) 残差: {abs(res_qnm):.2e}")

# 方法2: Leaver 1991 的连分数形式
cf_1991 = 0.0j
for n in range(max_iter, -1, -1):
    numer = alpha_1991(n) * gamma_1991(n + 1)
    denom = beta_1991(n + 1) - cf_1991
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf_1991 = numer / denom
res_1991 = beta_1991(0) - cf_1991
print(f"Leaver 1991 形式残差: {abs(res_1991):.2e}")

# 测试 Kerr 情况
print()
print("=" * 60)
print("测试 Kerr 情况 (a=0.5, m=2)")
print("=" * 60)
a_test = 0.5
m_test = 2
omega_test = complex(0.495007, -0.093885)  # Berti 参考值
A_test = 4.0 + 0.0j  # 粗略估计

D_test = D_coeffs(omega_test, a_test, s, m_test, A_test)
print(f"omega = {omega_test.real:.6f} {omega_test.imag:+.6f}i")
print(f"a = {a_test}, m = {m_test}")
print(f"A = {A_test}")
print()
print("D_coeffs:")
for i in range(5):
    print(f"D[{i}] = {D_test[i].real:.6f} {D_test[i].imag:+.6f}i")

res_kerr = leaver_cf_trunc_inversion(omega_test, a_test, s, m_test, A_test, 0, N=max_iter)
print(f"\n径向连分数残差: {abs(res_kerr):.2e}")

# 和 qnm 包的实际结果对比
print()
print("--- 与 qnm 包对比 ---")
try:
    from qnm.radial import leaver_cf_inv_lentz
    result = leaver_cf_inv_lentz(omega=omega_test, a=a_test, s=s, m=m_test, A=A_test, n_inv=0)
    print(f"qnm 包结果: {result[0].real:.6f} {result[0].imag:+.6f}i, 误差: {result[1]:.2e}, 迭代: {result[2]}")
    print(f"我们的结果: {res_kerr.real:.6f} {res_kerr.imag:+.6f}i")
    print(f"差值: {abs(result[0] - res_kerr):.2e}")
except Exception as e:
    print(f"导入 qnm 失败: {e}")
