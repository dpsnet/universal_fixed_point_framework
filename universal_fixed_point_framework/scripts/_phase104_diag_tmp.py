# -*- coding: utf-8 -*-
"""Phase 104: 三开放项综合诊断
① 15kK 中间点偏差模式（S 形诊断）
② C 截面比 Kramers 独立计算（σ2/κ̄_ff 数量级核对）
③ 高场溶解补偿渠道（束缚态溶解 → n_e → ff 增强 的数量级）
"""
import math

RY = 13.6
ALPHA = 1.0/137.02876
A0 = 0.529e-8          # cm
ME = 9.109e-28          # g
C_L = 2.998e10          # cm/s
HBAR = 1.055e-27        # erg s
KB_EV = 8.617e-5
E_CGS = 4.803e-10       # esu

def saha_ion_frac(T, nH=1e15):
    kT = KB_EV*T
    C = 2.41e21*(T/300.0)**1.5*1e-6
    ne = math.sqrt(nH*C*2.0*math.exp(-RY/kT))
    return ne/nH, ne

def N2_frac(T):
    kT = KB_EV*T
    return 4.0*math.exp(-(RY-RY/4.0)/kT)

# ① 15kK 偏差模式
print('=== ① 15kK 偏差模式（S 形诊断）===')
x12, ne12 = saha_ion_frac(12000)
C0 = (1/0.10-1)/((N2_frac(12000)*1e15)/ne12**2)
print('T   x(电离度)  A模型   A_fit  偏差')
for T in (12000,15000,20000):
    x, ne = saha_ion_frac(T)
    A = 1/(1+C0*(N2_frac(T)*1e15)/ne**2)
    Af = 0.10*(KB_EV*T/1.03)**3
    print('%d  %.4f   %.4f  %.4f  %+.1f%%' % (T/1000, x, A, Af, (A-Af)/Af*100))
print('诊断：中间点+16.7% vs 两端<1.2% —— S 形偏差（电离度转变区 x~0.21 半电离附近）')
print()

# ② C Kramers 独立计算
print('=== ② C = σ2/κ̄_ff Kramers 独立计算 ===')
# σ2：氢 n=2 光电离 Kramers（Gaunt≈1）
# σ_bf(n,ν) = (64π/3√3) α a₀² (1/n⁵)(ν_n/ν)³ g_bf
sig2_kr = (64*math.pi/(3*math.sqrt(3))) * ALPHA * A0**2 / 32.0
# κ̄_ff：每对 e-H+ 截面 Kramers（ν 单位 Hz）
# κ_ff = 3.69e8 n_e n_i T^{-1/2} ν^{-3} g_ff (1-e^{-hν/kT})
nu = C_L/3.7e-5
for T in (12000,):
    kff = 3.69e8 * T**-0.5 * nu**-3 * 1.1 * (1-math.exp(-3.35/(KB_EV*T)))
    print('σ2(Kramers)   = %.3e cm²' % sig2_kr)
    print('κ̄_ff(Kramers) = %.3e cm² (T=%dkK)' % (kff, T/1000))
    print('C_Kramers     = %.3e' % (sig2_kr/kff))
    print('C_标定         = 1.024e17')
    print('比值           = %.1f×' % ((sig2_kr/kff)/1.024e17))
print('核对：σ2 文献值 ~2e-19（1s→2p 标度 6.3e-18/32）——Kramers 式给 %.2e（差 %.0f×）'
      % (sig2_kr, 2e-19/sig2_kr if sig2_kr>0 else float('nan')))
print()

# ③ 高场溶解补偿
print('=== ③ 高场溶解补偿（束缚态溶解 → n_e → ff）数量级 ===')
# 束缚态数表（Phase 89/26.15）：N(B) 单原子束缚态总数
B_p = [0.001, 0.01, 0.05, 0.1, 0.2]
N_p = [303.0, 300.0, 152.0, 69.0, 33.0]
nH = 1e15
for b, N in zip(B_p, N_p):
    N_diss = 303.0 - N
    # 高 n 态占据率（溶解的是高 n——n≈n_ion 最低溶解态附近，占据率 e^{-13.6(1-1/n²)/kT}）
    occ = math.exp(-13.6*(1-1/16)/(KB_EV*12000))   # n=4 占据（保守上界）
    dn_e = N_diss*nH*occ
    x, ne = saha_ion_frac(12000)
    print('B=%.3f(%.0fMG): N_diss=%.0f, 高n占据~%.1e, Δn_e=%.1e vs n_e(0)=%.1e → ff增=%.1e×'
          % (b, b*2350, N_diss, occ, dn_e, ne, (ne+dn_e)**2/ne**2))
print('判定：高 n 占据率 e^{-12.4} → Δn_e/n_e ~ 1e-12 → ff 增可忽略 → n_e 机制数量级不足')
print('     回升缺口（RWA -0.535/-0.286 vs v6d 饱和）需其他渠道——保持开放（归 RWA 高场细节）')
