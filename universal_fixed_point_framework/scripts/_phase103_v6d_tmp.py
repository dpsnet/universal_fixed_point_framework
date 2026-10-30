# -*- coding: utf-8 -*-
"""Phase 103t: v6d 修正版——阈值上移移除主体 + 台阶翼残余 A(T)
chi(B,T) = A(T) + (1-A(T))*exp(-Δ_th/Δ_scale)
  Δ_th = ħω_c/2 = 0.58 eV×(B/10MG)（Landau 化连续态底抬升，拓扑内生）
  Δ_scale = 0.2 eV（Balmer 带能量尺度）
  A(T) = 台阶翼残余（Landau 台阶天然宽度 ~kT 展宽）——低温锐（A 小）、高温弥（A 大）
对照 RWA：12kK −0.78~−0.91；15kK −0.628/−0.606/−0.535；20kK −0.343/−0.330/−0.286
"""
import math

def delta_th(B_mg):
    return 0.58 * (B_mg / 10.0)

def residual_A(T):
    """台阶翼残余：Landau 台阶展宽 ~kT 占台阶间隔 ħω_c 的比例（用 10MG 台阶 1.16 eV）"""
    kT = 8.617e-5 * T
    return min(1.0, 0.25 + 0.5 * (kT / 1.29))   # 12kK→0.60? 不对——低温应小

# 直接参数化 A(T)（机制：台阶翼随温度弥散）
def A_fit(T):
    kT = 8.617e-5 * T
    return 0.10 * (kT / 1.03) ** 3        # 12kK:0.10, 15kK:0.30, 20kK:0.46 —— 待调

def chi_ratio(B_mg, T, scale=0.20):
    A = A_fit(T)
    return A + (1.0 - A) * math.exp(-delta_th(B_mg) / scale)

def dex(B_mg, T):
    r = chi_ratio(B_mg, T)
    return math.log10(r)

print('=== v6d：阈值移除 + 台阶翼残余 ===')
print('A(T)：12kK=%.2f、15kK=%.2f、20kK=%.2f' % (A_fit(12000), A_fit(15000), A_fit(20000)))
print()
print('B(MG) | T=12kK       T=15kK       T=20kK')
for B in (10, 50, 100):
    row = []
    for T in (12000, 15000, 20000):
        row.append('%+.3f' % dex(B, T))
    print('%-5d | %s' % (B, '  '.join(row)))
print()
print('RWA 对照：')
print('  12kK: −0.78~−0.91 | 15kK: −0.628/−0.606/−0.535 | 20kK: −0.343/−0.330/−0.286')
print()
print('--- 特征 ---')
print('B 弱依赖（10→100MG, 15kK）：v6d %.3f→%.3f（变化 %.0f%%；RWA 变化 15%%）'
      % (dex(10,15000), dex(100,15000), abs((dex(100,15000)-dex(10,15000))/dex(10,15000))*100))
print('T 强依赖（12 vs 20kK, 10MG）：v6d %.3f vs %.3f（RWA −0.85 vs −0.34）'
      % (dex(10,12000), dex(10,20000)))
print()
print('--- A_fit 扫描（标定）---')
for mult in (1.0, 1.3, 1.6):
    def A_fit2(T, m=mult):
        kT = 8.617e-5 * T
        return 0.10 * (kT / 1.03) ** 3 * m
    print('mult=%.1f: 12/15/20kK A=%.2f/%.2f/%.2f → 10MG dex=%.3f/%.3f/%.3f'
          % (mult, A_fit2(12000), A_fit2(15000), A_fit2(20000),
             math.log10(A_fit2(12000) + (1-A_fit2(12000))*math.exp(-0.58/0.2)),
             math.log10(A_fit2(15000) + (1-A_fit2(15000))*math.exp(-0.58/0.2)),
             math.log10(A_fit2(20000) + (1-A_fit2(20000))*math.exp(-0.58/0.2))))
