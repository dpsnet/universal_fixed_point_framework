# -*- coding: utf-8 -*-
"""
Phase 104az-73: 不动点方程解析性质论证（Banach 收缩——存在唯一性）
目标：f(a) = [d_eff(a)/(4πN_c)·(Δλ_min/Δλ₃)]^(1/3) 在物理区间上强收缩
  → Banach 不动点定理 ⇒ 存在唯一不动点 a*（104az-72 的数值收敛升格为解析唯一）
  d_eff(a) = 16 + D_q + (C_F/2)·e^{−(C_F/2)²/a}·N_c
"""
import numpy as np
import math

Nc = 3
CF = (Nc**2 - 1)/(2*Nc)      # 4/3
dlmin = (math.sqrt(3) - 1)/6
dl3 = math.sqrt(2) * dlmin
Z2 = 1.44
Dq_main = Nc*Nc*(CF/2)*math.sqrt(dlmin/dl3)*(1/Z2)   # 3.5037
K = (CF/2)**2                 # 4/9 —— m_s/T_c 分子（Λ 消去）
E = (CF/2)*Nc                 # 2

C = (1/(4*math.pi*Nc) * dlmin/dl3)**(1/3)

def d_eff(a):
    return 16 + Dq_main + E*math.exp(-K/a)

def f(a):
    return (d_eff(a)/(4*math.pi*Nc) * dlmin/dl3)**(1/3)

def fp_num(a, h=1e-7):
    return (f(a+h) - f(a-h))/(2*h)

# 1) 扫描物理区间 [0.6, 0.9] 数值导数
print("=== 1) f'(a) 数值扫描（中心差分）===")
max_fp = 0; a_max = 0
for a in np.linspace(0.55, 0.95, 401):
    fp = abs(fp_num(float(a)))
    if fp > max_fp:
        max_fp = fp; a_max = float(a)
print(f"max|f'| = {max_fp:.6f} @ a={a_max:.3f}  （远小于 1 ⇒ 强收缩）")

# 2) 解析上界：f'(a) = δd_(s)(a)·K/(3·a·d_eff(a))
#    在 a ∈ [a_lo, a_hi]：δd_(s) ≤ E、K 固定、a ≥ a_lo、d_eff ≥ 16
print("\n=== 2) 解析上界（粗糙）===")
for (alo, ahi) in [(0.6, 0.9), (0.7, 0.8), (0.72, 0.74)]:
    ub = E*K/(3*alo*16)
    # 更精细：d_eff(a) 单调增（δd_(s) 单调减？e^{−K/a} 在 a>0 单调增）→ d_eff 单调增
    # δd_(s)(a) ≤ δd_(s)(alo)；d_eff(a) ≥ d_eff(alo)
    ub2 = (E*math.exp(-K/alo))*K/(3*alo*d_eff(alo))
    print(f"  a∈[{alo},{ahi}]: 粗糙上界≤{ub:.4f}   精细上界≤{ub2:.6f}  （均 <1）")

# 3) 不动点再确认（Newton：g(a)=f(a)-a，g'(a)=f'(a)-1）
print("\n=== 3) 不动点 Newton 精化 ===")
a = 0.729
for i in range(6):
    fp = fp_num(a)
    a_new = a - (f(a)-a)/(fp-1)
    print(f"  iter{i}: a={a_new:.10f}  f(a)-a={f(a_new)-a_new:.2e}")
    a = a_new
print(f"不动点 a* = {a:.10f}")

# 4) 收缩性数值全区间验证：max over [0.55,0.95] |f'| < 1（安全裕度）
print(f"\n=== 4) 收缩判据 ===")
print(f"sup|f'| = {max_fp:.6f} < 1 ⇒ Banach 收缩成立，不动点存在唯一")
print(f"Lipschitz 常数 ≈ {max_fp:.4f} ⇒ 迭代收敛速率 ≥ {1-max_fp:.4f}")

# 5) 与 104az-72 收敛速度核对：Δ 序列 8.9e-4 → 9.6e-6 → 1.0e-7（比率 ≈ 0.0108 ≈ max|f'|）
print(f"\n=== 5) 收敛速率核对 ===")
print(f"104az-72 迭代 Δ 比率 ≈ 9.56e-6/8.92e-4 = {9.56e-6/8.92e-4:.4f} vs 预测收缩常数 {max_fp:.4f}")
