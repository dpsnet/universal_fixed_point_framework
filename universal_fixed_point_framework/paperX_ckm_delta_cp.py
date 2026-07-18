"""
paperX_ckm_delta_cp.py — CKM δ_CP 谱计算
从 IFS 谱结构与 CKM 矩阵的几何相位推导 δ_CP。
"""
import numpy as np

# ============================================================
# 谱输入
# ============================================================
N_gen, d_H = 3, 2.7095
S3, S4 = np.exp(-N_gen), np.exp(-d_H)
k = np.sum((np.array([S3*S4, S4, 1.0])) ** d_H) ** (-1/d_H)
c = k * np.array([S3*S4, S4, 1.0])
cn = c / c[2]

# 各扇区 α
alpha_u, alpha_d = 1.945, 1.229

# Yukawa 本征值（质量比）
yu_ratio = cn ** alpha_u  # (m_u/m_t, m_c/m_t, 1)
yd_ratio = cn ** alpha_d  # (m_d/m_b, m_s/m_b, 1)

# ============================================================
# CKM 矩阵（实验值，用于验证）
# ============================================================
# PDG 2024: sinθ12=0.2265, sinθ23=0.0422, sinθ13=0.0037, δ=1.20
s12, s23, s13 = 0.2265, 0.0422, 0.0037
c12, c23, c13 = np.sqrt(1-s12**2), np.sqrt(1-s23**2), np.sqrt(1-s13**2)
delta_exp = 1.20  # rad

# 标准 CKM 参数化
V_ckm_exp = np.array([
    [c12*c13, s12*c13, s13*np.exp(-1j*delta_exp)],
    [-s12*c23 - c12*s23*s13*np.exp(1j*delta_exp), 
     c12*c23 - s12*s23*s13*np.exp(1j*delta_exp), s23*c13],
    [s12*s23 - c12*c23*s13*np.exp(1j*delta_exp), 
     -c12*s23 - s12*c23*s13*np.exp(1j*delta_exp), c23*c13]
])

# Jarlskog 不变量
J_exp = (V_ckm_exp[0,0]*V_ckm_exp[1,1]*V_ckm_exp[0,1].conj()*V_ckm_exp[1,0].conj()).imag

print("="*65)
print("CKM δ_CP 谱计算")
print("="*65)
print(f"\n实验值: δ_CP = {delta_exp:.4f} rad")
print(f"Jarlskog J = {J_exp:.6e}")

# ============================================================
# 谱框架推导
# ============================================================
# 在谱框架中，Y_u 和 Y_d 的 Yukawa 矩阵不同体现在:
# 1. 特征值: yu_ratio 和 yd_ratio (已从 c_i 预测)
# 2. 特征向量: U_u 和 U_d 之间的旋转角
#
# CKM = U_u^† U_d
# 
# CP 破坏来自特征向量矩阵的复相位。
# 在谱框架中，复相位来自 IFS 收缩因子在复平面上的规范相位。
#
# 方法: 用谱间隙比构造 CKM 的实部矩阵，然后从幺正性约束
# 反推 δ_CP 的允许值范围。

# 谱间隙比给出的 CKM 实部矩阵
# 使用 Paper XI §8.5 的谱间隙比公式:
# sinθ_ij = Δλ_d^(ij) - Δλ_u^(ij) / Λ_scale

# 从上/下型 Yukawa 本征值计算谱间隙
lam_u = yu_ratio
lam_d = yd_ratio

# 相邻代的质量谱间隙
du12 = np.abs(lam_u[1] - lam_u[0])
du23 = np.abs(lam_u[2] - lam_u[1])
du13 = np.abs(lam_u[2] - lam_u[0])

dd12 = np.abs(lam_d[1] - lam_d[0])
dd23 = np.abs(lam_d[2] - lam_d[1])
dd13 = np.abs(lam_d[2] - lam_d[0])

# 归一化标度
scale = (du12 + dd12 + du23 + dd23) / 4

# 预测 CKM 角
sin12_pred = (dd12 - du12) / scale
sin23_pred = (dd23 - du23) / scale
sin13_pred = (dd13 - du13) / scale

# 限制在 (0,1) 范围内
sin12_pred = max(0, min(1, sin12_pred))
sin23_pred = max(0, min(1, sin23_pred))
sin13_pred = max(0, min(1, sin13_pred))

print(f"\n谱间隙比预测:")
print(f"  sinθ₁₂ = {sin12_pred:.4f} (exp={s12:.4f})")
print(f"  sinθ₂₃ = {sin23_pred:.4f} (exp={s23:.4f})")
print(f"  sinθ₁₃ = {sin13_pred:.4f} (exp={s13:.4f})")

# ============================================================
# CP 相位的谱起源
# ============================================================
# CP 相位来自:
# 1. 上型和下型特征向量失配的几何 Berry 相位
# 2. 在谱框架中，这由 IFS 三重态在 SU(3) 权重空间中的
#    并行输运的相位差给出
#
# 几何相位公式:
# δ_CP = arg[1 + Σ (c_u_i/c_d_i) exp(i·Δφ_i)]
# 其中 Δφ_i 是第 i 代上/下型谱算符的规范相位差
#
# 设规范相位差正比于谱间隙:
# Δφ_i ∝ |c_u_i - c_d_i| / (c_u_i + c_d_i)

# 代间谱间隙差
gap_diff = np.abs(yu_ratio - yd_ratio)
norm_sum = yu_ratio + yd_ratio

# 规范相位差
phi = np.pi * gap_diff / (norm_sum + 1e-15)

print(f"\n谱规范相位差:")
for i in range(3):
    print(f"  Δφ_{i+1} = {phi[i]:.4f} rad")

# 从相位构造 CKM 的不可约相位
# CKM 的 Jarlskog 不变量由下式给出:
# J = sinθ₁₂ sinθ₂₃ sinθ₁₃ cosθ₁₂ cosθ₂₃ cosθ₁₃ sinδ

# 从上/下型特征值的复相位差估计 δ_CP
# δ_CP ≈ asin(sin(φ_u - φ_d)) 在幺正三角形中

# 简化模型: δ_CP 由谱间隙失配的加权和决定
w = yu_ratio * yd_ratio / np.sum(yu_ratio * yd_ratio)
delta_pred = np.sum(w * phi)

print(f"\n预测 δ_CP = {delta_pred:.4f} rad")
print(f"实验 δ_CP = {delta_exp:.4f} rad")
print(f"偏差: ×{max(delta_pred, delta_exp)/min(delta_pred, delta_exp):.2f}")

# ============================================================
# Jarlskog 不变量
# ============================================================
# 从预测的角构造 CKM
t12 = np.arcsin(sin12_pred)
t23 = np.arcsin(sin23_pred) 
t13 = np.arcsin(sin13_pred)

# 使用预测的 δ_CP
c12_p, s12_p = np.cos(t12), np.sin(t12)
c23_p, s23_p = np.cos(t23), np.sin(t23)
c13_p, s13_p = np.cos(t13), np.sin(t13)

V_pred = np.array([
    [c12_p*c13_p, s12_p*c13_p, s13_p*np.exp(-1j*delta_pred)],
    [-s12_p*c23_p - c12_p*s23_p*s13_p*np.exp(1j*delta_pred),
     c12_p*c23_p - s12_p*s23_p*s13_p*np.exp(1j*delta_pred), s23_p*c13_p],
    [s12_p*s23_p - c12_p*c23_p*s13_p*np.exp(1j*delta_pred),
     -c12_p*s23_p - s12_p*c23_p*s13_p*np.exp(1j*delta_pred), c23_p*c13_p]
])

J_pred = (V_pred[0,0]*V_pred[1,1]*V_pred[0,1].conj()*V_pred[1,0].conj()).imag
J_exp_val = (V_ckm_exp[0,0]*V_ckm_exp[1,1]*V_ckm_exp[0,1].conj()*V_ckm_exp[1,0].conj()).imag

print(f"\nJarlskog 不变量:")
print(f"  J_pred = {J_pred:.6e}")
print(f"  J_exp  = {J_exp_val:.6e}")
print(f"  |J|   = {abs(J_exp_val):.2e} (SM: ~3e-5)")

# ============================================================
# PMNS δ_CP 扫描
# ============================================================
print(f"\n{'='*65}")
print("PMNS δ_CP 谱估计")
print(f"="*65)

# PMNS δ_CP 来自 M_R 的非自伴结构
# 用 c_i 估计 M_R 的复相位
# M_R ∝ diag(c₁, c₂, c₃) × exp(i·φ_R_i)
# φ_R_i ∝ 谱间隙比

phi_R = 2 * np.pi * gap_diff  # M_R 的相位扫描范围
delta_pmns_est = np.mean(phi_R)
print(f"估计 PMNS δ_CP = {delta_pmns_est:.4f} rad = {delta_pmns_est/np.pi:.4f}π")
print(f"实验 PMNS δ_CP = 1.36π rad")

# ============================================================
# 检查
# ============================================================
print(f"\n{'检查':^65}")
checks = [
    (f"CKM δ_CP 在 [0.5, 2.0] rad 内", 0.5 < delta_pred < 2.0),
    (f"sinθ₁₂ ≈ {sin12_pred:.4f} 在 30% 内", abs(sin12_pred/s12 - 1) < 0.3),
    (f"sinθ₂₃ ≈ {sin23_pred:.4f} 在 30% 内", abs(sin23_pred/s23 - 1) < 0.3),
]
for desc, ok in checks:
    print(f"  {'✅' if ok else '❌'} {desc}")
