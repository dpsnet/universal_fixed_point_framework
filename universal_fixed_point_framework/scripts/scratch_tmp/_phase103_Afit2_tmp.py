# -*- coding: utf-8 -*-
"""Phase 103v: A(T) 第一性化尝试 2——真实大气密度 + 多候选机制
候选 A：Saha 通道占比（nH=1e21 m^-3 真实白矮星大气密度）
候选 B：台阶翼 Lorentz 尾（γ=碰撞/热展宽）
候选 C：阈值敏感分数（Kramers 带内分布——高能翼残余）
"""
import math

RY = 13.6

def saha_ne(T, nH):
    kT = 8.617e-5 * T
    C = 2.41e21 * (T / 300.0) ** 1.5
    return math.sqrt(nH * C * 2.0 * math.exp(-RY / kT))

def occ_n2(T, nH):
    kT = 8.617e-5 * T
    return nH * 4.0 * math.exp(-(RY - RY/4.0) / kT)

def chi_n2(T, nH):
    N2 = occ_n2(T, nH)
    return N2 * 1.0

def chi_Hminus(T, nH):
    kT = 8.617e-5 * T
    ne = saha_ne(T, nH)
    lam = 3700.0
    hv = 12398.0 / lam
    return ne * nH * (lam ** 3) * (T ** -2.5) * (1.0 - math.exp(-hv/kT))

def chi_ff(T, nH):
    ne = saha_ne(T, nH)
    lam = 3700.0
    return ne * ne * (T ** -0.5) * (lam ** 3)

def A_saha(T, nH):
    c2 = chi_n2(T, nH)
    ch = chi_Hminus(T, nH)
    cf = chi_ff(T, nH)
    tot = c2 + ch + cf
    return (ch + cf) / tot if tot > 0 else 0.0

def A_lorentz(T, B_mg=10.0):
    """台阶翼 Lorentz 尾：翼宽 γ——候选 γ = kT 或 γ = ħω_c 尺度"""
    dth = 0.58 * (B_mg / 10.0)      # 阈值位移（带中心到新阈）
    kT = 8.617e-5 * T
    # 带中心 3.42 eV，新阈 3.4+dth——带内到新阈平均距离
    dist = dth - 0.02               # 带中心 3.42 - 原阈 3.4 = 0.02
    g1 = kT                          # 热展宽
    g2 = 0.25                        # 碰撞尺度（试）
    A1 = 1.0 / (1.0 + (dist/g1)**2)
    A2 = 1.0 / (1.0 + (dist/g2)**2)
    return A1, A2

print('=== A(T) 第一性化尝试 2 ===')
print()
print('--- 候选 A：Saha 通道占比（nH=1e21 m^-3 真实大气密度）---')
print('%-7s | %-10s | %-8s | %-8s | %-8s' % ('T(kK)', '电离度', 'A_saha', 'A_fit', 'n2占比'))
for T in (12000, 15000, 20000):
    nH = 1e21
    ne = saha_ne(T, nH)
    kT = 8.617e-5 * T
    Afit = 0.10 * (kT/1.03)**3
    A = A_saha(T, nH)
    c2 = chi_n2(T, nH); ch = chi_Hminus(T, nH); cf = chi_ff(T, nH)
    tot = c2+ch+cf
    print('%-7d | %.4f     | %.3f   | %.3f   | %.3f'
          % (T/1000, ne/nH, A, Afit, c2/tot))

print()
print('--- 候选 B：台阶翼 Lorentz 尾（10MG）---')
print('%-7s | %-10s | %-10s | %s' % ('T(kK)', 'γ=kT', 'γ=0.25eV', 'A_fit'))
for T in (12000, 15000, 20000):
    A1, A2 = A_lorentz(T)
    kT = 8.617e-5 * T
    print('%-7d | %.3f    | %.3f    | %.3f' % (T/1000, A1, A2, 0.10*(kT/1.03)**3))

print()
print('--- 判定 ---')
print('候选 A：n=2 光电离占比极小（玻尔兹曼 10.2eV 激发）——A_saha→1.0 与 A_fit 反向')
print('  ——模型揭示：Balmer 带主吸收不是 n=2 光电离？或 n=2 布居被低估（非 LTE/碰撞）')
print('候选 B：Lorentz 尾 γ=kT 给 0.7（12kK）远大于 0.10；γ=0.25eV 给 0.16（12kK）接近但无身份')
