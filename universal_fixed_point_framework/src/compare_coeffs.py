"""验证 Schwarzschild 下乘积形式和二次形式的等价性"""
import cmath

M = 1.0
omega = complex(0.373672, -0.088962)
l = 2
s = -2
epsilon = 3.0

# 二次形式 (Leaver 1991)
omega_leaver = 2.0 * M * omega
rho = -1j * omega_leaver

def alpha_quad(n):
    return n**2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0

def beta_quad(n):
    return -(2.0 * n**2 + (8.0 * rho + 2.0) * n + 8.0 * rho**2 + 4.0 * rho + l * (l + 1.0) - epsilon)

def gamma_quad(n):
    return n**2 + 4.0 * rho * n + 4.0 * rho**2 - epsilon - 1.0

# 乘积形式
r_plus = M + cmath.sqrt(M**2 - 0**2)
r_minus = M - cmath.sqrt(M**2 - 0**2)
sigma_plus = (omega * r_plus - 0) / (r_plus - r_minus)
A_lm = l * (l + 1) - s * (s + 1)

def alpha_prod(n):
    return -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)

def beta_prod(n):
    return n * (n + 1.0) + 4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - A_lm

def gamma_prod(n):
    return 2.0j * omega * (n - 4.0j * sigma_plus - 1.0)

print("比较 Schwarzschild 下的系数形式")
print(f"omega = {omega.real:.6f} {omega.imag:.6f}i")
print(f"omega_leaver = {omega_leaver.real:.6f} {omega_leaver.imag:.6f}i")
print(f"rho = {rho.real:.6f} {rho.imag:.6f}i")
print(f"sigma_plus = {sigma_plus.real:.6f} {sigma_plus.imag:.6f}i")
print()

for n in [0, 1, 2, 5, 10]:
    print(f"n = {n}:")
    aq = alpha_quad(n)
    ap = alpha_prod(n)
    print(f"  alpha_quad = {aq.real:.6f} {aq.imag:.6f}i")
    print(f"  alpha_prod = {ap.real:.6f} {ap.imag:.6f}i")
    print(f"  比值: {abs(aq/ap):.6f}, 角度差: {abs(cmath.phase(aq) - cmath.phase(ap)):.6f}")
    
    bq = beta_quad(n)
    bp = beta_prod(n)
    print(f"  beta_quad = {bq.real:.6f} {bq.imag:.6f}i")
    print(f"  beta_prod = {bp.real:.6f} {bp.imag:.6f}i")
    print(f"  比值: {abs(bq/bp):.6f}, 角度差: {abs(cmath.phase(bq) - cmath.phase(bp)):.6f}")
    
    gq = gamma_quad(n)
    gp = gamma_prod(n)
    print(f"  gamma_quad = {gq.real:.6f} {gq.imag:.6f}i")
    print(f"  gamma_prod = {gp.real:.6f} {gp.imag:.6f}i")
    print(f"  比值: {abs(gq/gp):.6f}, 角度差: {abs(cmath.phase(gq) - cmath.phase(gp)):.6f}")
    print()
