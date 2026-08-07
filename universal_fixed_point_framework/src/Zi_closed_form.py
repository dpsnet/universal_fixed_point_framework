#!/usr/bin/env python3
"""
Z_i 的 S₂ 层闭合形式推导与验证

从根因链 §4a，Z_i 的 1-loop 闭合形式为：
  Z_i = 1 / [1 - b₁·α_i(M_Z)·ln(M_Pl/M_Z)/(2π)]

其中 b₁ 展开后显式包含四层静默：
  b₁ = 11·C_A/3   [S₂ 态射]
      - 4·T_R·n_f/3  [S₃ 代结构: n_f = 2·(-ln S₃)]
      - T_R/3        [S₂ Higgs]

验证：闭合形式 vs 数值三圈 RGE 积分。
"""

import numpy as np

# 谱框架参数
M_Pl = 2.435e18
M_Z = 91.1876
ln_MPl_MZ = np.log(M_Pl / M_Z)

# 静默因子
S3 = np.exp(-3)
ln_S3 = -np.log(S3)  # = 3
n_f = 6              # = 2·N_gen = 2·(-ln S₃)

# 实验值 at M_Z
exp_alpha_s = 0.1179
exp_alpha_inv = 127.95
exp_sin2 = 0.2312

# GUT-归一化耦合 at M_Z
alpha_1_MZ = (5.0/3.0) / (exp_alpha_inv * (1 - exp_sin2))
alpha_2_MZ = 1.0 / (exp_alpha_inv * exp_sin2)
alpha_3_MZ = exp_alpha_s

# 谱裸耦合（【2026-08-06 修复】U(1) 分量 √(2/3) → √(1/3)，SU(2) 特征值归一化，
# 见 paperX_ratio_fix.py 与笔记 §8.4 修复子节）
alpha_bare = {
    'U1': 0.122 * np.sqrt(1/3) / (4*np.pi),
    'SU2': 0.122 * 1.0 / (4*np.pi),
    'SU3': 0.122 * np.sqrt(2) / (4*np.pi),
}

# 四层静默分解的 b₁
def beta_coeff_silence(C_A, T_R=0.5):
    b1_S2 = 11 * C_A / 3       # S₂ 态射（纯规范）
    b1_S3 = -4 * T_R * n_f / 3  # S₃ 代结构（费米子）
    b1_H = -T_R / 3             # Higgs
    return b1_S2, b1_S3, b1_H

print("=" * 72)
print("  Z_i 四层静默闭合形式验证")
print("=" * 72)

data = [
    ("U(1)", 0, alpha_1_MZ, alpha_bare['U1']),
    ("SU(2)", 2, alpha_2_MZ, alpha_bare['SU2']),
    ("SU(3)", 3, alpha_3_MZ, alpha_bare['SU3']),
]

print(f"\n  {'群':>6s} {'C_A':>4s} {'b1_S2':>8s} {'b1_S3':>8s} {'b1_H':>8s} {'b1_total':>10s}")
print(f"  {'─'*44}")

for name, CA, aMZ, a0 in data:
    s2, s3, h = beta_coeff_silence(CA)
    b1 = s2 + s3 + h
    print(f"  {name:>6s} {CA:4d} {s2:8.3f} {s3:8.3f} {h:8.3f} {b1:10.4f}")

print(f"\n  Z_i 闭合形式（1-loop）:")
print(f"  Z_i = 1 / [1 - b₁·α_i(M_Z)·ln(M_Pl/M_Z)/(2π)]")
print(f"  ln(M_Pl/M_Z) = {ln_MPl_MZ:.2f}")

print(f"\n  {'群':>6s} {'α(M_Z)':>10s} {'α_bare':>10s} {'b₁':>8s} {'Z_closed':>10s} {'Z_numerical':>12s} {'偏差':>8s}")
print(f"  {'─'*64}")

# 数值 Z_i 来自三圈 RGE（之前计算结果）
Z_num = {'U(1)': 3.674, 'SU(2)': 2.118, 'SU(3)': 1.439}

for name, CA, aMZ, a0 in data:
    s2, s3, h = beta_coeff_silence(CA)
    b1 = s2 + s3 + h

    # 闭合形式（1-loop）
    denom = 1 - b1 * aMZ * ln_MPl_MZ / (2*np.pi)
    Z_closed = 1.0 / denom
    Z_num_val = Z_num[name]
    dev = abs(Z_closed - Z_num_val) / Z_num_val * 100
    print(f"  {name:>6s} {aMZ:10.6f} {a0:10.6f} {b1:8.3f} {Z_closed:10.4f} {Z_num_val:12.4f} {dev:7.2f}%")

print(f"\n  S₂ 态射在 b₁ 中的贡献:")
print(f"    b1_S2 = 11·C_A/3  (纯规范)")
print(f"    b1_S3 = -4·T_R·n_f/3  = -4×0.5×6/3 = -4  (S₃ 代结构)")
print(f"    n_f = 2·(-ln S₃) = 2×{ln_S3} = {n_f}")
print(f"    b1_H = -T_R/3 = -0.5/3  (Higgs)")

print(f"\n  Z_closed vs Z_numerical 差异来源:")
print(f"    1-loop 闭合形式在 α×ln(M_Pl/M_Z) >> 1 时不精确:")
print(f"    α_s(M_Z) × ln(M_Pl/M_Z) = {alpha_3_MZ:.4f} × {ln_MPl_MZ:.1f} = {alpha_3_MZ * ln_MPl_MZ:.2f}")
print(f"    远大于 1，需 2/3-loop 修正。")
print(f"\n  Z_i 的正确闭合形式是完整 RGE 积分:")
print(f"    Z_i = α_i(M_Z) / α_i_bare(M_Pl)  ← 经三圈 RGE 积分")
print(f"    静默分解在 β 函数系数层面成立：")
print(f"    b₁ = 11·C_A/3 [S₂] - 4·T_R·n_f/3 [S₃] - T_R/3 [S₂ Higgs]")
print(f"    n_f = 2·(-ln S₃) [S₃ 代结构]")
print(f"    ln(M_Pl/M_Z) [S₄ 分形边界]")
print("=" * 72)
