"""
paperX_gut_unification.py -- GUT 单化分析: 谱规范耦合 RGE 跑动 + 质子寿命
"""
import numpy as np, math

# ========== 谱输入: a_i(M_Z) ==========
a1_inv_SM = 127.6
a2_inv = 29.5
a3 = 0.1179; a3_inv = 1/a3
a1_inv_GUT = (3/5) * a1_inv_SM  # SU(5) 归一化

# SM 1-loop beta 系数
b_GUT = np.array([(3/5)*41/10, -19/6, -7])

M_Z = 91.1876

print("="*65)
print("  GUT 分析: 谱规范耦合 RGE 单化")
print("="*65)
print(f"\n  谱 a_i(M_Z): a1^-1={a1_inv_SM:.1f} a2^-1={a2_inv:.1f} a3^-1={a3_inv:.2f}")
print(f"  GUT 归一化: a1^-1 = {a1_inv_GUT:.2f}")

# ========== 1-loop RGE ==========
def run(ainv, b, M):
    return ainv - b * math.log(M/M_Z) / (2*math.pi)

# 搜索最佳单化能标
best_M, best_s = None, 1e10
for logM in np.linspace(10, 19, 901):
    M = 10**logM
    a1, a2, a3 = run(a1_inv_GUT, b_GUT[0], M), run(a2_inv, b_GUT[1], M), run(a3_inv, b_GUT[2], M)
    s = abs(a1-a2) + abs(a2-a3) + abs(a1-a3)
    if s < best_s: best_s, best_M = s, M

M_G = best_M
a1g, a2g, a3g = run(a1_inv_GUT, b_GUT[0], M_G), run(a2_inv, b_GUT[1], M_G), run(a3_inv, b_GUT[2], M_G)
aG = 1 / np.mean([a1g, a2g, a3g])

print(f"\n  1-loop 单化:")
print(f"  M_GUT = {M_G:.2e} GeV")
print(f"  a1^-1={a1g:.1f} a2^-1={a2g:.1f} a3^-1={a3g:.1f}")
print(f"  a_GUT = {aG:.4f}  残差={best_s:.2f}")

# ========== 实验对比 ==========
ae1 = run(127.951/(5/3), b_GUT[0], M_G)
ae2 = run(1/0.03380, b_GUT[1], M_G)
ae3 = run(1/0.11792, b_GUT[2], M_G)
se = abs(ae1-ae2)+abs(ae2-ae3)+abs(ae1-ae3)
print(f"\n  实验 SM 在 M_GUT: {ae1:.1f} {ae2:.1f} {ae3:.1f} 残差={se:.2f}")

# ========== 质子寿命 ==========
print(f"\n{'─'*65}\n质子衰变 (p -> e+ pi0)\n{'─'*65}")

m_p, f_pi, A_L, F0 = 0.938, 0.130, 3.0, 0.012
G = aG**2 * m_p**5 / (64*math.pi**2 * f_pi**2 * M_G**4) * (A_L*F0)**2
tau = (1/G) * 6.582e-25  # s
tau_yr = tau / (365.25*24*3600)

print(f"  tau_p = 10^{math.log10(tau_yr):.1f} 年")
print(f"  Super-K 下限: 10^34 年")
print(f"  Hyper-K 灵敏度: 10^35 年")

# GUT 能标不确定性
print(f"\n  能标不确定性:")
for f in [0.3, 0.5, 1.0, 2.0, 3.0]:
    Mt = M_G * f
    a1t = run(a1_inv_GUT, b_GUT[0], Mt)
    a2t = run(a2_inv, b_GUT[1], Mt)
    a3t = run(a3_inv, b_GUT[2], Mt)
    aGt = 1/np.mean([a1t, a2t, a3t])
    Gt = aGt**2 * m_p**5 / (64*math.pi**2*f_pi**2*Mt**4) * (A_L*F0)**2
    ty = (1/Gt)*6.582e-25/(365.25*24*3600)
    print(f"  M_GUT x {f:3.1f} = {Mt:.2e}: tau = 10^{math.log10(ty):.1f} yr")

print(f"\n{'='*65}")
print(f"  M_GUT = {M_G:.2e} GeV")
print(f"  tau_p = 10^{math.log10(tau_yr):.1f} yr")
print(f"{'='*65}")
