"""
paperX_cp_phase_cluster.py — CP 相位集群：CKM/PMNS/Majorana
"""
import numpy as np

N_gen, d_H = 3, 2.7095
S3, S4 = np.exp(-N_gen), np.exp(-d_H)
k = np.sum((np.array([S3*S4, S4, 1.0]))**d_H)**(-1/d_H)
cn = k * np.array([S3*S4, S4, 1.0]) / k

print("="*65)
print("CP 相位集群 — 谱几何相位计算")
print("="*65)

# ============================================================
# CKM δ_CP: 来自IFS三重态在SU(3)权重空间的几何相位
# ============================================================
# 三个收缩因子构成一个三元组 (c₁, c₂, c₃)
# 归一化到球面上的点 ĉ = c/||c||
# 三个点确定一个球面三角形 → 立体角 → Berry相位

c_norm = cn / np.linalg.norm(cn)
print(f"\n归一化收缩因子: ({c_norm[0]:.6f}, {c_norm[1]:.6f}, {c_norm[2]:.6f})")

# 球坐标
theta = np.arccos(c_norm[2])
phi = np.arctan2(c_norm[1], c_norm[0])
print(f"球坐标: θ={theta:.4f}, φ={phi:.4f}")

# IFS三重态在SU(3)权重空间中的三个点
# 将(c₁,c₂,c₃)映射到SU(3)的根格点
# SU(3)的简单根: α₁=(1,-1,0), α₂=(0,1,-1)
# 三个基本权重: ω₁=(2/3,1/3), ω₂=(1/3,2/3), ω₃=(0,0)
# 代位置 ∝ c_i × ω_i

# 三个生成元的位置向量 (3D嵌入: 在SU(3)的加权格点上)
# 用三个收缩因子构造三维向量，然后归一化到球面上
v = np.array([[cn[0], cn[1]*np.cos(np.pi/3), cn[1]*np.sin(np.pi/3)],
              [cn[1], cn[2]*np.cos(np.pi/3), cn[2]*np.sin(np.pi/3)],
              [cn[2], cn[0]*np.cos(np.pi/3), cn[0]*np.sin(np.pi/3)]])

# 球面三角形的立体角 (3D)
def solid_angle(p1, p2, p3):
    r1, r2, r3 = p1/np.linalg.norm(p1), p2/np.linalg.norm(p2), p3/np.linalg.norm(p3)
    num = abs(np.dot(r1, np.cross(r2, r3)))
    den = 1 + np.dot(r1, r2) + np.dot(r2, r3) + np.dot(r3, r1)
    return 2 * np.arctan2(num, den)

Omega = float(solid_angle(v[0], v[1], v[2]))

# CKM δ_CP = Ω/2 (Berry phase)
delta_ckm_pred = Omega / 2
delta_ckm_exp = 1.20  # rad
J_pred = np.sin(delta_ckm_pred) * 0.2265 * 0.0422 * 0.0037 * np.cos(0.2265) * np.cos(0.0422) * np.cos(0.0037) * 8

print(f"\n--- CKM δ_CP ---")
print(f"球面三角形立体角 Ω = {Omega:.4f} sr")
print(f"Berry相位 δ_CP = Ω/2 = {delta_ckm_pred:.4f} rad")
print(f"实验值 δ_CP = {delta_ckm_exp:.4f} rad")
print(f"偏差: ×{max(delta_ckm_pred,delta_ckm_exp)/min(delta_ckm_pred,delta_ckm_exp):.2f}")
if 0.5 < delta_ckm_pred < 2.0:
    print(f"  ✅ 在 [0.5, 2.0] 范围内")
print(f"Jarlskog J ≈ {J_pred:.2e} (SM≈3.2e-5)")

# ============================================================
# PMNS δ_CP: 来自M_R的非自伴性
# ============================================================
# M_R的非自伴部分来自Dirac-Yukawa耦合的复相位
# 复相位正比于c_i之差
# PMNS δ_CP = Σ w_i · Im(Y_ν_i) / Re(Y_ν_i)

print(f"\n--- PMNS δ_CP ---")
# 中微子Yukawa的复相位来自See-saw中的M_R非对角性
# δ_PMNS ≈ arg(det(M_R)) 在轻子基中
# M_R ∝ diag(c₁, c₂, c₃) × exp(i·φ_i)
# 其中φ_i是谱间隙比

# 从谱间隙比估计M_R的复相位
gaps = np.abs(np.diff(cn))
delta_pmns_pred = 2 * np.sum(gaps)  # 简化: 相位正比于总谱间隙
delta_pmns_exp = 1.36 * np.pi  # ≈ 4.27 rad

print(f"预测 PMNS δ_CP = {delta_pmns_pred:.4f} rad = {delta_pmns_pred/np.pi:.4f}π")
print(f"实验 PMNS δ_CP = {delta_pmns_exp:.4f} rad = 1.36π")
print(f"偏差: ×{max(delta_pmns_pred,delta_pmns_exp)/min(delta_pmns_pred,delta_pmns_exp):.2f}")

# ============================================================
# Majorana 相位
# ============================================================
print(f"\n--- Majorana 相位 α₁, α₂ ---")
# Majorana相位由A_νR的自伴性决定
# 若A_νR自伴 → α₁=α₂=0
# 若A_νR非自伴 → α₁,α₂ ≠ 0
# 来源: M_R的复部分 = M_R × exp(i·φ_R)

# 从谱间隙比估计M_R的不可约相位
# α₁ = arg(m_ν₁/m_ν₃), α₂ = arg(m_ν₁/m_ν₂)
# 其中m_ν_i = c_i^{2α_ν-β_R} × exp(i·φ_i)

# 质量比
alpha_nu, beta_R = 1.358/2, 1.0
m_nu_ratio = cn ** (2*alpha_nu - beta_R)

# 相位估计: 正比于ln(c_i)
phi_i = np.log(cn + 1e-15)
alpha1_pred = abs(phi_i[0] - phi_i[2])
alpha2_pred = abs(phi_i[0] - phi_i[1])

print(f"预测 α₁ = {alpha1_pred:.4f} rad")
print(f"预测 α₂ = {alpha2_pred:.4f} rad")
print(f"0νββ 影响: |m_ee| 将受 cos(α₁) 和 cos(α₂) 调制")

# ============================================================
# 检查
# ============================================================
print(f"\n{'检查':^65}")
checks = [
    (f"CKM δ_CP 在 [0.5, 2] rad", 0.5 < delta_ckm_pred < 2.0),
    (f"几何相位非零", delta_ckm_pred > 0.01),
    (f"PMNS δ_CP > π/2", delta_pmns_pred > np.pi/2),
]
for desc, ok in checks:
    print(f"  {'✅' if ok else '❌'} {desc}")
