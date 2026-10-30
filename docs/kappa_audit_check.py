# -*- coding: utf-8 -*-
"""κ=1/4 系数审计（修正版）：验证 2311.13990 式 20 -> 式 21 的积分恒等式。

恒等式（分部积分，w=u(u+2ℓ)，w''=2，w(0)=w(−2ℓ)=0）：
  ∫ w·A'' du = [wA'−w'A]_{−2ℓ}^{0} + ∫ w''A du = −2ℓ[A(0)+A(−2ℓ)] + 2∫A du
完整被积函数（完整面积元 √γ dθdφ，角无关情形）：
  ∫ (dΘ̃/du)√γ dθdφ = A'' − 4π f'²/f   （f=√(A/4π)，f'²/f 项为 O(ε²)）
验证：S1 = (1/16G_Nℓ)∫w[A''−4πf'²/f]du  vs  S2 = (1/4G_N)⟨⟨A⟩⟩ − [A(0)+A(−2ℓ)]/(8G_N)
"""
import math

def intg(f, a, b, N=16000):
    h = (b - a) / N
    s = 0.0
    for i in range(N):
        x = a + (i + 0.5) * h
        s += f(x) * h
    return s

L = 1.0
GN = 1.0
eps0 = 1e-6

cases = [
    ("quadratic", lambda u: 4 * math.pi * (1 + 0.01 * u * u)),
    ("linear",    lambda u: 4 * math.pi * (1 + 0.01 * u)),
    ("cubic",     lambda u: 4 * math.pi * (1 + 0.005 * u * u * u)),
]

for tag, A in cases:
    dA  = lambda u: (A(u + eps0) - A(u - eps0)) / (2 * eps0)
    ddA = lambda u: (A(u + eps0) - 2 * A(u) + A(u - eps0)) / (eps0 * eps0)
    f   = lambda u: math.sqrt(A(u) / (4 * math.pi))
    fp  = lambda u: (f(u + eps0) - f(u - eps0)) / (2 * eps0)
    w   = lambda u: u * (u + 2 * L)
    B   = lambda u: 4 * math.pi * fp(u) ** 2 / f(u)          # 完整面积元修正项 O(ε²)
    S1  = (1 / (16 * GN * L)) * intg(lambda u: w(u) * (ddA(u) - B(u)), -2 * L, 0)
    avg = (1 / (2 * L)) * intg(A, -2 * L, 0)
    S2  = (1 / (4 * GN)) * avg - (A(0) + A(-2 * L)) / (8 * GN)
    # 恒等式本身（精确，无近似）：∫w·A''du vs 2∫Adu − 2ℓ[A(0)+A(−2ℓ)]
    Ia  = intg(lambda u: w(u) * ddA(u), -2 * L, 0)
    Ib  = 2 * intg(A, -2 * L, 0) - 2 * L * (A(0) + A(-2 * L))
    print("%-10s S1=%.10f  S2=%.10f  diff(S1,S2)=%.3e  |Ia-Ib|=%.3e"
          % (tag, S1, S2, abs(S1 - S2), abs(Ia - Ib)))
