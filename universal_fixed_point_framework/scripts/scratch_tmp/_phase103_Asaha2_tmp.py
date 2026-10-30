# -*- coding: utf-8 -*-
"""Phase 103y: A(T) √T 修正检验——C = C0×√(T/T0)（κff∝T^{-1/2}，截面比微变）"""
import math

RY = 13.6

def saha_ion_frac(T, nH=1e15):
    kT = 8.617e-5 * T
    C = 2.41e21 * (T / 300.0) ** 1.5 * 1e-6
    ne = math.sqrt(nH * C * 2.0 * math.exp(-RY / kT))
    return ne / nH, ne

def N2_frac(T):
    kT = 8.617e-5 * T
    return 4.0 * math.exp(-(RY - RY/4.0) / kT)

T12, T15, T20 = 12000, 15000, 20000
x12, ne12 = saha_ion_frac(T12)
N2_12 = N2_frac(T12) * 1e15
C0 = (1/0.10 - 1) / (N2_12 / ne12**2)

print('=== A(T) √T 修正（C = C0·√(T/T₀)，κff∝T^{-1/2}）===')
print('C0 = %.3e' % C0)
print()
print('%-7s | %-8s | %-8s | %-8s | %-8s | %s' %
      ('T(kK)', 'A模型', 'A模型√T', 'A_fit', '偏差(原)', '偏差(√T)'))
for T in (T12, T15, T20):
    x, ne = saha_ion_frac(T)
    N2 = N2_frac(T) * 1e15
    r = N2 / ne**2
    A0 = 1.0 / (1.0 + C0 * r)
    C1 = C0 * math.sqrt(T / T12)
    A1 = 1.0 / (1.0 + C1 * r)
    kT = 8.617e-5 * T
    Afit = 0.10 * (kT/1.03)**3
    print('%-7d | %.4f | %.4f | %.4f | %+.1f%% | %+.1f%%'
          % (T/1000, A0, A1, Afit, (A0-Afit)/Afit*100, (A1-Afit)/Afit*100))

print()
print('--- 判定 ---')
print('√T 修正方向：C 随 T 增 → A 降 → 15kK 0.231 下压')
