"""测试乘积形式系数 + 正确连分数迭代"""
import cmath
import numpy as np

M = 1.0
a = 0.0
s = -2
l = 2
omega = complex(0.373672, -0.088962)

b = cmath.sqrt(M**2 - a**2)
r_plus = M + b
r_minus = M - b

# 乘积形式系数
sigma_plus = (omega * r_plus - 0) / (r_plus - r_minus)
A_lm = l * (l + 1) - s * (s + 1)

print(f"sigma_plus = {sigma_plus.real:.6f} {sigma_plus.imag:.6f}i")
print(f"A_lm = {A_lm}")
print()

def alpha_prod(n):
    return -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)

def beta_prod(n):
    return n * (n + 1.0) + 4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - A_lm

def gamma_prod(n):
    return 2.0j * omega * (n - 4.0j * sigma_plus - 1.0)

# 迭代方式1: 旧的 1/(β - αγ*cf) 形式
print("--- 迭代方式1: 旧的 1/(β - αγ*cf) 形式")
max_iter = 300
cf1 = 0.0j
for n in range(max_iter, 0, -1):
    denom = beta_prod(n) - alpha_prod(n) * gamma_prod(n + 1) * cf1
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf1 = 1.0 / denom
res1 = beta_prod(0) - alpha_prod(0) * gamma_prod(1) * cf1
print(f"残差: {abs(res1):.2e}")

# 迭代方式2: 正确的连分数形式 β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...)))
print()
print("--- 迭代方式2: 正确的连分数形式 β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...)))")
cf2 = 0.0j
for n in range(max_iter, -1, -1):
    numer = alpha_prod(n) * gamma_prod(n + 1)
    denom = beta_prod(n + 1) - cf2
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf2 = numer / denom
res2 = beta_prod(0) - cf2
print(f"残差: {abs(res2):.2e}")

# 迭代方式3: 另一种形式 - 从 n=max_iter 向下到 n=1, 然后计算 β₀ - α₀γ₁/(β₁ - cf)
print()
print("--- 迭代方式3: 另一种形式")
cf3 = 0.0j
for n in range(max_iter, 1, -1):
    numer = alpha_prod(n) * gamma_prod(n + 1)
    denom = beta_prod(n) - cf3
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf3 = numer / denom

# cf3 现在是 α₁γ₂/(β₁ - α₂γ₃/(β₂ - ...)))
# 完整连分数 = α₀γ₁/(β₁ - α₁γ₂/(...)) = α₀γ₁/(β₁ - cf3) ? 不对
# 让我们重新思考:
# 完整的连分数是: α₀γ₁ / (β₁ - α₁γ₂ / (β₂ - α₂γ₃ / (...)))
# 上面的循环从 n=max_iter 到 n=1, 计算的是:
# 当 n=max_iter 时: cf = α_max γ_{max+1} / β_max
# 当 n=max_iter-1 时: cf = α_{max-1} γ_max / (β_{max-1} - α_max γ_{max+1}/β_max)
# 所以当 n=1 时, cf = α₁γ₂ / (β₁ - α₂γ₃ / (β₂ - ...)))
# 那么完整的连分数 = α₀γ₁ / (β₁ - α₁γ₂ / (β₂ - ...))) 
# 注意: 第一层的分母是 β₁, 分子是 α₁γ₂/(β₂ - ...)
# 不对, 让我搞混了索引...

# 让我们从定义重新来:
# 连分数: C = α₀γ₁ / (β₁ - α₁γ₂ / (β₂ - α₂γ₃ / (β₃ - ...)))
# 定义 C_n = α_n γ_{n+1} / (β_{n+1} - C_{n+1})
# 则 C = C_0
# C_0 = α₀γ₁ / (β₁ - C₁)
# C₁ = α₁γ₂ / (β₂ - C₂)
# ...

# 所以我们应该从 n=N 开始, C_N ≈ α_N γ_{N+1} / β_{N+1} (近似)
# 然后向下迭代直到 n=0

# 让我们用正确的方式:
cf4 = 0.0j
for n in range(max_iter, -1, -1):
    numer = alpha_prod(n) * gamma_prod(n + 1)
    denom = beta_prod(n + 1) - cf4
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf4 = numer / denom

# 特征方程: β₀ - C_0 = 0 ? 不对
# Leaver 1991 的特征方程是: β₀/α₀ + F = 0, 其中 F = -γ₁/(β₁ - α₁γ₂/(β₂ - ...))
# 即 β₀ + α₀ * F = 0
# 即 β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...)) = 0

# 所以残差 = β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...))
# = β₀ - C_0, 其中 C_0 = α₀γ₁/(β₁ - C₁), C₁ = α₁γ₂/(β₂ - C₂), ...

# 但我们上面的 cf4 是从 n=N 到 n=0 的迭代:
# cf4 (n=0) = α₀γ₁/(β₁ - cf4 (n=1))
# 不对, 让我们打印一些中间值看看

# 让我们用另一种方式: 直接计算连分数
# F = -γ₁/(β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))
# 特征方程: β₀/α₀ + F = 0

# 定义 G_n = α_n γ_{n+1} / (β_{n+1} - G_{n+1})
# 则 -γ₁/(β₁ - α₁γ₂/(...)) = -γ₁/β₁ * 1/(1 - α₁γ₂/(β₁β₂) / (...)) 不对

# 不管了, 直接用 Leaver 1991 的方式来测试乘积形式
# 在 Leaver 1991 中, 特征方程是 β₀/α₀ + F(ρ) = 0
# 其中 F(ρ) = -γ₁/(β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...)))

# 让我们计算 F:
# F = -γ₁ / (β₁ - α₁γ₂/(β₂ - α₂γ₃/(...)))
# 定义 H_n = α_n γ_{n+1} / (β_n - H_{n+1})  不对...

# 直接计算连分数:
# β₁ - α₁γ₂/(β₂ - α₂γ₃/(β₃ - ...))
# = β₁ - H₁
# 其中 H_n = α_n γ_{n+1} / (β_{n+1} - H_{n+1})
# 不对, H₁ = α₁γ₂ / (β₂ - H₂)

# 让我们从后向前算:
H = 0.0j
for n in range(max_iter, 0, -1):
    numer = alpha_prod(n) * gamma_prod(n + 1)
    denom = beta_prod(n + 1) - H
    if abs(denom) < 1e-30:
        denom = 1e-30
    H = numer / denom

# H (n=1) = α₁γ₂ / (β₂ - α₂γ₃/(...))
# 那么 β₁ - H = β₁ - α₁γ₂/(β₂ - ...)
# F = -γ₁ / (β₁ - H)
F = -gamma_prod(1) / (beta_prod(1) - H)

# 特征方程: β₀/α₀ + F = 0
res5 = beta_prod(0) / alpha_prod(0) + F
print(f"方式3 (β₀/α₀ + F): 残差 = {abs(res5):.2e}")

# 方式4: β₀ + α₀*F = 0
res6 = beta_prod(0) + alpha_prod(0) * F
print(f"方式4 (β₀ + α₀*F): 残差 = {abs(res6):.2e}")

# 现在, 让我们也用 Leaver 1991 的方式来验证二次形式
print()
print("--- 验证: 用 Leaver 1991 方式验证二次形式 ---")
omega_leaver = 2.0 * M * omega
rho = -1j * omega_leaver
epsilon_grav = 3.0

def alpha_1991(n):
    return n**2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0

def beta_1991(n):
    return -(2.0 * n**2 + (8.0 * rho + 2.0) * n + 8.0 * rho**2 + 4.0 * rho + l * (l + 1.0) - epsilon_grav)

def gamma_1991(n):
    return n**2 + 4.0 * rho * n + 4.0 * rho**2 - epsilon_grav - 1.0

H2 = 0.0j
for n in range(max_iter, 0, -1):
    numer = alpha_1991(n) * gamma_1991(n + 1)
    denom = beta_1991(n + 1) - H2
    if abs(denom) < 1e-30:
        denom = 1e-30
    H2 = numer / denom

F2 = -gamma_1991(1) / (beta_1991(1) - H2)
res7 = beta_1991(0) / alpha_1991(0) + F2
print(f"二次形式 (β₀/α₀ + F): 残差 = {abs(res7):.2e}")
