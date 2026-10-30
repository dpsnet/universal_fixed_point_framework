import math, cmath
def eTrunc(K):
    return sum(1.0 / math.factorial(k) for k in range(0, K + 1))
def eTrunc_exp(K, x):
    return sum(x ** k / math.factorial(k) for k in range(0, K + 1))
e8 = eTrunc(8)
e8_sq_trunc16 = eTrunc_exp(16, 2.0)   # e^2 的截断：Sigma 2^k/k!（正确口径）
e2 = math.e ** 2
conv_bias_correct = abs(e8 * e8 - e8_sq_trunc16)
bound = 10.0 / (9 * math.factorial(9))
print("eTrunc(8)      =", format(e8, ".12f"))
print("e8^2           =", format(e8 * e8, ".12f"))
print("e^2 截断(K=16) =", format(e8_sq_trunc16, ".12f"))
print("e^2 (精确)     =", format(e2, ".12f"))
print("conv_bias(corr)= ", format(conv_bias_correct, ".12e"))
print("bound(Thm2)    =", format(bound, ".12e"))
print("ratio vs bound =", format(conv_bias_correct / bound, ".6f"))
print("conv-exact bias=", format(abs(e8 * e8 - e2), ".12e"))
z = cmath.exp(complex(0, 2 * math.pi))
print("exp(2pi i)     =", format(z.real, ".15f"), "+", format(z.imag, ".15f"), "i")
z2 = cmath.exp(complex(0, math.pi))
print("exp(pi i)      =", format(z2.real, ".15f"), "+", format(z2.imag, ".15f"), "i")
a = 0.5
tc = eTrunc_exp(8, a) * eTrunc_exp(8, a)
td = eTrunc_exp(16, 1.0)
ex = math.exp(1.0)
print("trunc_conv     =", format(tc, ".12f"))
print("trunc_direct   =", format(td, ".12f"))
print("exact e        =", format(ex, ".12f"))
print("conv-direct    =", format(abs(tc - td), ".12e"))
print("conv-exact     =", format(abs(tc - ex), ".12e"))
