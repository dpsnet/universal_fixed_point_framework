# -*- coding: utf-8 -*-
"""Phase 103x: A(T) 第一性化——量子圆周分账 + Saha（形状验证）
机制（纯理论构造）：
  吸收通道按圆周闭合性分账：
    轴向通道（m=0）：n=2 光电离（束缚→连续轴向）——被 Landau 化阈值位移移除（1−A）
    圆周通道（m≠0）：ff（自由电子回旋——Landau 态本征运动）+ 背景——保留（A）
  A(T) = 1/(1 + C × N₂/n_e²)
    N₂ ∝ 4e^{−10.2/kT}（n=2 布居，玻尔兹曼）
    n_e² ∝ Saha 电离度²（ff ∝ n_e n_H+）
    C = 截面比常数（σ2/κff 的 Kramers 系数比——单参数标定）
对照 A_fit = 0.10×(kT/1.03)³（12/15/20kK: 0.10/0.20/0.47）
"""
import math

RY = 13.6

def saha_ion_frac(T, nH=1e15):
    """Saha 电离度（cm^-3 单位）"""
    kT = 8.617e-5 * T
    C = 2.41e21 * (T / 300.0) ** 1.5   # m^-3 常数 → 转 cm^-3：×1e-6
    C = C * 1e-6
    ne = math.sqrt(nH * C * 2.0 * math.exp(-RY / kT))
    return ne / nH, ne

def N2_frac(T):
    """n=2 布居分数（相对 nH，简并 4）"""
    kT = 8.617e-5 * T
    return 4.0 * math.exp(-(RY - RY/4.0) / kT)

def A_saha(T, C):
    nH = 1e15
    x, ne = saha_ion_frac(T, nH)
    N2 = N2_frac(T) * nH
    ne2 = ne * ne
    ratio = N2 / ne2
    return 1.0 / (1.0 + C * ratio)

# 标定 C：使 12kK A = 0.10
T12, T15, T20 = 12000, 15000, 20000
x12, ne12 = saha_ion_frac(T12)
N2_12 = N2_frac(T12) * 1e15
C = (1/0.10 - 1) / (N2_12 / ne12**2)

print('=== A(T) 第一性化：量子圆周分账 + Saha ===')
print('C（截面比常数标定 @12kK）= %.3e' % C)
print()
print('%-7s | %-8s | %-8s | %-10s | %-8s | %-8s | %s' %
      ('T(kK)', '电离度', 'N₂/nH', 'N₂/n_e²', 'A模型', 'A_fit', '偏差'))
for T in (T12, T15, T20):
    x, ne = saha_ion_frac(T)
    N2f = N2_frac(T)
    N2 = N2f * 1e15
    A = A_saha(T, C)
    kT = 8.617e-5 * T
    Afit = 0.10 * (kT/1.03)**3
    print('%-7d | %.4f | %.2e | %.2e | %.3f | %.3f | %+.1f%%'
          % (T/1000, x, N2f, N2/ne**2, A, Afit, (A-Afit)/Afit*100))

print()
print('--- 电离度驱动检验（ff 圆周通道的核心）---')
for T in (T12, T15, T20):
    x, ne = saha_ion_frac(T)
    kT = 8.617e-5 * T
    print('T=%dkK: 电离度=%.4f (增 %.0f×), N₂=%s, ff∝n_e² ∝ %.1e' %
          (T/1000, x, x/x12, '%.2e' % N2_frac(T), ne**2))

print()
print('--- 物理机制判定 ---')
print('A(T) 陡增来源 = Saha 电离度 0.05→0.99（ff∝n_e² 增 400 倍）')
print('            vs N₂（n=2 布居 e^{−10.2/kT} 增 54 倍）')
print('          → ff/n2 比值降 7.5 倍 → A 从 0.10 升到 0.46')
print('★ 量子圆周分账：轴向 n2 光电离被阈值位移移除（1−A）')
print('                圆周 ff（回旋）保留（A）——Landau 态本征运动')
print('★ 与 26.16 统一：束缚态 m=0 轴向（1/n 转移）vs 连续态圆周（ff）')
print('                ——同一量子圆周分布结构（Landau 化紧致圆周、保留轴向）两端')
