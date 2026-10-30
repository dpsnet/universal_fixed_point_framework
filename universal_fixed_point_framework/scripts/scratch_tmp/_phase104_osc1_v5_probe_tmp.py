# -*- coding: utf-8 -*-
"""v5 数值探针：验证 GSIG/GC/radial_int 关键量"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import genlaguerre, factorial, sph_harm_y

def R_nl(n, l, r):
    rho = 2.0*r/n
    norm = np.sqrt((2.0/n)**3 * factorial(n-l-1) / (2.0*n*factorial(n+l)))
    L = genlaguerre(n-l-1, 2*l+1)(rho)
    return norm * np.exp(-r/n) * (2.0*r/n)**l * L

def radial_int(n, l, np_, lp, power, r_max=120.0, N=8000):
    r = np.linspace(1e-8, r_max, N)
    f = R_nl(n, l, r) * R_nl(np_, lp, r) * r**power * r*r
    return np.trapezoid(f, r)

def gaunt_sigma(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = sph_harm_y(l1, 0, th, 0.0)
    y2 = sph_harm_y(l2, 1, th, 0.0)
    integrand = np.conj(y1) * np.sin(th) * y2 * np.sin(th)
    return float(np.real(np.sum(w * integrand) * (2.0*np.pi) / np.sqrt(2.0)))

def gaunt_cos(l1, l2):
    th, w = leggauss(96); th = np.arccos(th)
    y1 = sph_harm_y(l1, 0, th, 0.0); y2 = sph_harm_y(l2, 0, th, 0.0)
    return float(np.real(np.sum(w * np.conj(y1) * np.cos(th) * y2 * np.sin(th))))

print("=== 数值探针 ===")
# 1. 归一化自检：∫|Y_00|² sinθ dθ 应 = 1/2π（φ 已积掉）
th, w = leggauss(96); th = np.arccos(th)
y00 = sph_harm_y(0, 0, th, 0.0)
print("∫|Y00|² sinθ dθ =", np.sum(w*np.conj(y00)*y00*np.sin(th)), "（应≈1/2π=%.4f）" % (1/(2*np.pi)))

# 2. 径向矩阵元
print("<2s|r|3p> =", radial_int(2, 0, 3, 1, 1), "（解析≈0.4849）")
print("<2s|r|4p> =", radial_int(2, 0, 4, 1, 1))
print("<2s|r²|2s> =", radial_int(2, 0, 2, 0, 2), "（解析=6）")
print("<2p|r²|2p> =", radial_int(2, 1, 2, 1, 2), "（解析=30）")
print("<3s|r²|3s> =", radial_int(3, 0, 3, 0, 2), "（解析=63）")
print("<3p|r²|3p> =", radial_int(3, 1, 3, 1, 2), "（解析=147）")

# 3. Gaunt
print("GC(0,1)=<Y00|cosθ|Y10> =", gaunt_cos(0, 1), "（解析 1/√3=%.4f）" % (1/np.sqrt(3)))
print("GC(1,2)=<Y10|cosθ|Y20> =", gaunt_cos(1, 2), "（解析 √(4/15)=%.4f）" % np.sqrt(4.0/15))
print("GSIG(0,1)=<Y00|σ+|Y11> =", gaunt_sigma(0, 1), "（解析 1/√3=%.4f）" % (1/np.sqrt(3)))
print("GSIG(1,2)=<Y10|σ+|Y21> =", gaunt_sigma(1, 2))

# 4. 单分量强度 f(2s→3p) = (2/3)·ΔE·|d|²——d = radial·Gaunt
d_pi = radial_int(2, 0, 3, 1, 1) * gaunt_cos(0, 1)
d_sig = radial_int(2, 0, 3, 1, 1) * gaunt_sigma(0, 1)
dE = 1.0/8 - 1.0/18
print("d_pi(2s→3p) =", d_pi, " f_pi =", 2.0/3*dE*d_pi**2)
print("d_sig(2s→3p+) =", d_sig, " f_sig =", 2.0/3*dE*d_sig**2)
