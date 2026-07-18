"""
paperX_alpha_fine.py — α 指数精细修正分析
"""
import numpy as np
ac = {'u': 1.945, 'd': 1.229, 'l': 1.358}

# α 差异
print("="*65)
print("α 指数精细修正")
print("="*65)
print(f"\nα_u = {ac['u']:.3f}, α_d = {ac['d']:.3f}, α_l = {ac['l']:.3f}")
print(f"α_u/α_l = {ac['u']/ac['l']:.4f}")
print(f"α_d/α_l = {ac['d']/ac['l']:.4f}")
print(f"α_u/α_d = {ac['u']/ac['d']:.4f}")

# 量子数
Q = {'u': 2/3, 'd': -1/3, 'l': -1}
T3 = {'u': 0.5, 'd': -0.5, 'l': -0.5}
Y = {'u_L': 1/3, 'u_R': 4/3, 'd_L': 1/3, 'd_R': -2/3, 'l_L': -1, 'l_R': -2}

# α ∝ f(|Q|², C₂, Y²)
# 假设 α = α₀ + a·α_s + b·α₂ + c·α_Y
# 从三个方程解 a,b,c

# α_s 只在夸克中贡献
# 标准 QCD 质量反常维数 γ_m ≈ -2α_s/π
# α 的 QCD 修正部分正比于 ∫γ_m dlnμ

# 三扇区的 α 方程组:
# α_u = α₀ + a·Q_u² + b·C₂_u + c·Y_u_avg²
# α_d = α₀ + a·Q_d² + b·C₂_d + c·Y_d_avg²
# α_l = α₀ + a·Q_l² + b·C₂_l + c·Y_l_avg²

# 简化: 令 α₀ ≈ 1 (IFS 基线), 各贡献线性叠加
# 上型: C₃=4/3, C₂=3/4, Y_avg²=(1/9+16/9)/2=17/18
# 下型: C₃=4/3, C₂=3/4, Y_avg²=(1/9+4/9)/2=5/18
# 轻子: C₃=0, C₂=3/4, Y_avg²=(1+4)/2=5/2

# 简化为: α = α_base + k_s·SU(3)_factor + k_w·SU(2)_factor + k_y·U(1)_factor
# 其中 SU(3)_factor = C₃（夸克为4/3，轻子为0）
# SU(2)_factor = C₂（全为3/4）
# U(1)_factor = Y² (不同扇区不同)

C3 = {'u': 4/3, 'd': 4/3, 'l': 0}
C2 = {'u': 3/4, 'd': 3/4, 'l': 3/4}
Y2_avg = {'u': (1/9+16/9)/2, 'd': (1/9+4/9)/2, 'l': (1+4)/2}  # left+right平均

# 设 α₀ = 1 (IFS 基线, 来自分形维数), 解 k_s, k_w, k_y
a0_fixed = 1.0
A = np.array([[C3['u'], C2['u'], Y2_avg['u']],
              [C3['d'], C2['d'], Y2_avg['d']],
              [C3['l'], C2['l'], Y2_avg['l']]])
b = np.array([ac['u'] - a0_fixed, ac['d'] - a0_fixed, ac['l'] - a0_fixed])
coeffs = np.linalg.solve(A, b)
k_s, k_w, k_y = coeffs

print(f"\n最佳拟合系数 (α₀ = {a0_fixed}):")
print(f"  k_s (SU(3))  = {k_s:.4f}")
print(f"  k_w (SU(2))  = {k_w:.4f}")
print(f"  k_y (U(1))   = {k_y:.4f}")

# 验证
for s in ['u','d','l']:
    pred = a0_fixed + k_s*C3[s] + k_w*C2[s] + k_y*Y2_avg[s]
    print(f"  α_{s} pred={pred:.3f} (fit={ac[s]:.3f})")

# 关键发现: α₀ ≈ 1 + (Q²相关项)
# 如果 α₀ = 1 (来自 IFS 维数 d_H / 3 ≈ 0.9)
# 则 QCD 贡献的正负由 k_s 决定

# 检验 α 与 1-Q² 的相关性
print(f"\nα 与量子数的经验关系:")
print(f"  α ≈ α₀ + |Q|·c_Q")
c_Q = (ac['u'] - ac['d']) / (2/3 - (-1/3))
print(f"  c_Q = {c_Q:.3f}")
print(f"  → α_d predicted = α_u - c_Q·(Q_u - Q_d)")
print(f"  → α_d = {ac['u'] - c_Q * (2/3 - (-1/3)):.3f} (fit={ac['d']:.3f})")

# α ≈ α₀ + a·|Q| 拟合
Q_abs = np.array([2/3, 1/3, 1])
alpha_arr = np.array([ac['u'], ac['d'], ac['l']])
p = np.polyfit(Q_abs, alpha_arr, 1)
print(f"\nα = {p[1]:.4f} + {p[0]:.4f}·|Q|")
for s, q in zip(['u','d','l'], Q_abs):
    pred_a = p[1] + p[0]*q
    print(f"  α_{s}={pred_a:.3f} (fit={ac[s]:.3f})")
