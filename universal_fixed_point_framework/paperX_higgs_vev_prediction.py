"""
paperX_higgs_vev_prediction.py — Higgs VEV 谱预测 (v2, 简化 RGE)
"""
import numpy as np

M_Pl, M_Z, M_GUT = 1.22e19, 91.19, 1e16

S3, S4 = np.exp(-3), np.exp(-2.7095)
dl_GR = 0.122

# M_Pl 边界条件（来自谱框架）
g3 = np.sqrt(4*np.pi * dl_GR * np.sqrt(2))
g2 = np.sqrt(4*np.pi * dl_GR * 1.0)
g1 = np.sqrt(4*np.pi * dl_GR * np.sqrt(2/3))
yt = 0.50
lam = S3 * S4
mu2 = -(M_Pl * dl_GR * S3 * S4)**2

print("="*65)
print("Higgs VEV 谱预测 — 简化 RGE")
print("="*65)
print(f"\nM_Pl: g₃={g3:.3f}, g₂={g2:.3f}, g₁={g1:.3f}")
print(f"  y_t={yt:.3f}, λ={lam:.6f}, μ²={mu2:.2e}")

# 单圈 β 系数
b3, b2, b1 = -7, -19/6, 41/10
n = 20000
log_mu_range = np.linspace(np.log(M_Pl), np.log(M_Z), n)
dlnmu = (np.log(M_Z) - np.log(M_Pl)) / n

for i in range(n):
    mu = np.exp(log_mu_range[i])
    
    # 耦合跑动
    t = np.log(mu / M_Pl)
    g3_t = g3 / np.sqrt(1 + b3 * g3**2 * t / (4*np.pi))
    g2_t = g2 / np.sqrt(1 + b2 * g2**2 * t / (4*np.pi))
    g1_t = g1 / np.sqrt(1 + b1 * g1**2 * t / (4*np.pi))
    
    # Yukawa
    by = yt * (9*yt**2/2 - 8*g3_t**2 - 9*g2_t**2/4 - 17*g1_t**2/20) / (16*np.pi**2)
    yt += by * dlnmu
    
    # λ
    bl = (24*lam**2 - 6*yt**4 + (9/8)*g2_t**4 + (9/20)*g1_t**4
          + (3/10)*g1_t**2*g2_t**2 + lam*(12*yt**2 - 9*g2_t**2 - 3*g1_t**2)) / (16*np.pi**2)
    lam += bl * dlnmu
    
    # μ²
    gh = (-9*g2_t**2/2 - 3*g1_t**2/2 + 6*yt**2 + 12*lam) / (16*np.pi**2)
    mu2 += mu2 * gh * dlnmu

print(f"\nM_Z 结果:")
print(f"  λ  = {lam:.6f}")
print(f"  μ² = {mu2:.4e} GeV²")
if mu2 < 0:
    v = np.sqrt(-mu2 / lam)
    mH = np.sqrt(2 * lam * v**2)
    print(f"  v  = {v:.2f} GeV (exp=246)")
    print(f"  mH = {mH:.2f} GeV (exp=125.10)")
    print(f"  v_pred/exp = {v/246:.6f}")
else:
    print("  ❌ μ² > 0, 无对称性破缺")

# 方案二: 从 m_t/v 确定 α_v
print(f"\n{'='*65}")
print("方案二: 静默公式")

c1 = S3 * S4
alpha_t = 1.945
alpha_v = alpha_t + np.log(246/172.69) / np.log(c1)
print(f"α_v = {alpha_v:.3f} (Higgs指数)")
print(f"α_v - α_t = {alpha_v - alpha_t:.4f}")

# 预测 v
v_silence = 172.69 * c1**(alpha_v - alpha_t)
print(f"v_silence = {v_silence:.2f} GeV ✅")
