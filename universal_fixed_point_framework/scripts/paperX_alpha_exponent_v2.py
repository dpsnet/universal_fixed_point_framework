# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
paperX_alpha_exponent_v2.py — α 指数 RG 推导 v2
α 来自 ∫ γ_m d ln μ 从 M_Pl 到 M_Z，使用正确 γ_m 归一化。
"""
import numpy as np

# ============================================================
# SM 跑动输入
# ============================================================
alpha_s_MZ, alpha_s_MPl = 0.118, 0.05
alpha_2_MZ, alpha_2_MPl = 1/29.6, 1/38.2  # SU(2)
alpha_1_MZ, alpha_1_MPl = 1/59.0, 1/210.0  # U(1)

def alpha_at_mu(alpha_z, b, mu):
    """α 在 mu 处的值 (one-loop running from M_Z)"""
    ln_mu = np.log(mu / 91.19)
    return alpha_z / (1 + b * alpha_z * ln_mu / (2*np.pi))

# 耦合在 [M_Z, M_Pl] 上的积分
mus = np.logspace(np.log10(91.19), np.log10(1.22e19), 10000)
dlnmu = np.log(mus[1]/mus[0])

# ============================================================
# 正确 γ_m 公式 (标准文献, 单圈)
# ============================================================
# 夸克质量反常维数 (QCD):  γ_m = -8g₃²/(16π²) * 1 (不是 C_F!)
# 完整 SM: γ_m = -[8g₃²·C₂(R₃) + 3g₂²·C₂(R₂) + 3g₁²·(Y/2)²] / (16π²)
#
# 其中:
#   C_F = (N²-1)/(2N) = 4/3 for SU(3)
#   C₂ = 3/4 for SU(2) fundamental
#   Y = 超荷
#
# 标准文献 (Peskin & Schroeder, 相对论量子场论 §18):
#   夸克质量 γ_m = -6C_F α_s/(4π) - 6·(T₃²/4)·α₂/(4π) - 6·(Y²/16)·α₁/(4π)
#   简化: γ_m = -2α_s/π - (3/8)α₂/π - (3/8)(Y²/2)α₁/π

def gamma_m_up(alpha_s, alpha_2, alpha_1):
    """上型夸克 (Q=+2/3) 质量反常维数"""
    QCD  = -2 * alpha_s / np.pi
    SU2  = -0.375 * alpha_2 / np.pi  # 3/8 因子
    U1_up = -0.375 * (1/9) * alpha_1 / np.pi  # Y=1/3 → Y²/2=1/18
    return QCD + SU2 + U1_up

def gamma_m_down(alpha_s, alpha_2, alpha_1):
    """下型夸克 (Q=-1/3) 质量反常维数"""
    QCD  = -2 * alpha_s / np.pi
    SU2  = -0.375 * alpha_2 / np.pi
    U1_down = -0.375 * (1/36) * alpha_1 / np.pi  # Y=-2/3 → Y²/2=2/9... 
    return QCD + SU2 + U1_down

# 耶,让我用标准公式。对于Standard Model，质量反常维数是:
# γ_m = -3/2 · C_F · α_s/π for QCD
# 加上 SU(2): -3/2 · (3/4) · α₂/π = -9/8 · α₂/π 对于 SU(2) 二重态
# 加上 U(1): -3/2 · (Y/2)² · α₁/π
# 
# 简化: γ_m = -(6C_F + 3/2·C₂ + 3/2·(Y/2)²) · gauge²/(16π²)
# 用 α = g²/(4π):
# γ_m = -6C_F·α_s/(4π) - 6C₂·α₂/(4π) - 6(Y/2)²·α₁/(4π)
# = -(3/2)C_F·α_s/π - (3/2)C₂·α₂/π - (3/2)(Y/2)²·α₁/π

def gamma_m_up_v2(alpha_s, alpha_2, alpha_1):
    """上型夸克 (Q_L双态 + u_R单态)"""
    # 左手上型: (3,2)_{1/3}, 右手上型: (3,1)_{4/3}
    # 取左右手平均
    C_F, C_2, Y_L = 4/3, 3/4, 1/3
    Y_Ru = 4/3
    gamma_L = (3/2) * (C_F*alpha_s + C_2*alpha_2 + (Y_L/2)**2*alpha_1) / np.pi
    gamma_R = (3/2) * (C_F*alpha_s + 0*alpha_2 + (Y_Ru/2)**2*alpha_1) / np.pi
    return -(gamma_L + gamma_R) / 2

def gamma_m_down_v2(alpha_s, alpha_2, alpha_1):
    """下型夸克 (Q_L双态 + d_R单态)"""
    C_F, C_2 = 4/3, 3/4
    Y_L, Y_Rd = 1/3, -2/3
    gamma_L = (3/2) * (C_F*alpha_s + C_2*alpha_2 + (Y_L/2)**2*alpha_1) / np.pi
    gamma_R = (3/2) * (C_F*alpha_s + 0*alpha_2 + (Y_Rd/2)**2*alpha_1) / np.pi
    return -(gamma_L + gamma_R) / 2

def gamma_m_lepton_v2(alpha_s, alpha_2, alpha_1):
    """带电轻子 (L_L双态 + e_R单态)"""
    C_2 = 3/4
    Y_L, Y_Re = -1, -2
    gamma_L = (3/2) * (0*alpha_s + C_2*alpha_2 + (Y_L/2)**2*alpha_1) / np.pi
    gamma_R = (3/2) * (0*alpha_s + 0*alpha_2 + (Y_Re/2)**2*alpha_1) / np.pi
    return -(gamma_L + gamma_R) / 2

# 积分 γ_m d ln μ
print("="*65)
print("α 指数 RG 推导 v2")
print("="*65)

# 对每个扇区积分
results = {}
for name, gamma_fn in [('up-type', gamma_m_up_v2), 
                       ('down-type', gamma_m_down_v2),
                       ('lepton', gamma_m_lepton_v2)]:
    integral = 0.0
    for i in range(len(mus)-1):
        mu = np.sqrt(mus[i] * mus[i+1])
        # 在mu处的耦合 (简化: 单圈对数跑动)
        as_ = alpha_at_mu(alpha_s_MZ, 7, mu) if mu < 1e15 else 0.05
        a2 = alpha_at_mu(alpha_2_MZ, 19/6, mu) if mu < 1e15 else alpha_2_MPl
        a1 = alpha_at_mu(alpha_1_MZ, -41/10, mu) if mu < 1e15 else alpha_1_MPl
        integral += gamma_fn(as_, a2, a1) * dlnmu
    results[name] = integral
    print(f"\n{name}:")
    print(f"  ∫γ_m d ln μ = {integral:.4f}")
    print(f"  m(M_Z)/m(M_Pl) = exp({integral:.4f}) = {np.exp(integral):.4f}")

# ============================================================
# α 指数公式
# ============================================================
# m(M_Z) = m(M_Pl) · η_RG
# m_i(M_Pl) ∝ c_i^{α_base} (universal)
# 所以: ln(m_i/m_j) = α_sector · ln(c_i/c_j)
# 其中 α_sector = α_base + correction from RG

# 从拟合值反推 α_base
alpha_l_fit = 1.358  # 轻子 (无 QCD)
alpha_u_fit = 1.945  # 上型夸克
alpha_d_fit = 1.229  # 下型夸克

print(f"\n{'='*65}")
print("α_base 确定 (从轻子扇区，无 QCD)")
print(f"{'='*65}")

# 假设 α_lepton = α_base (轻子无 QCD 修正)
alpha_base = alpha_l_fit
print(f"α_base = α_l = {alpha_base:.3f}")

# α 修正应是 RG 因子的函数:
# 由于 m(M_Z) = m(M_Pl) × η_RG
# 且 m ∝ c^{α}
# 则 c^{α_l} × η_l = c^{α_u} × η_u = c^{α_d} × η_d (同一粒子不同扇区)
# 但这里 η 是扇区依赖的，不同代共享同一 η
# 实际上 η 不依赖于代，所以它不影响 α

# 修正的理解：
# 不同扇区的 α 差异来自 c_i 在谱流方程中的有效耦合不同
# 不是来自 RG 跑动
# 而是来自 IFS 收缩因子在 gauge 耦合下的重整化

print(f"\n{'='*65}")
print("直接比较: α 差异 = Δγ_m (谱流耦合)")
print(f"{'='*65}")

# α 差异
print(f"α_u - α_l = {alpha_u_fit - alpha_base:.3f}")
print(f"α_d - α_l = {alpha_d_fit - alpha_base:.3f}")

# 这个差异应与γ_m的积分相关
# 但从RG分析: 同一扇区内不同代的η相同，α不受影响
# 
# 正确理解:
# α_sector 描述 IFS 收缩因子 c_i 如何映射到质量
# 不同扇区有不同的质量-收缩因子关系
# 这来自不同扇区在谱流方程中与不同规范场的耦合差异
# 
# α_sector - α_base = ∫(γ_m_sector - γ_m_base) · w(μ) d ln μ
# 其中 w(μ) 是谱流耦合权重

print(f"\nγ_m 积分差异 (理论预测与拟合对比):")
int_l = results['lepton']
int_u = results['up-type']
int_d = results['down-type']

diff_u_l_fit = alpha_u_fit - alpha_l_fit
diff_d_l_fit = alpha_d_fit - alpha_l_fit
diff_u_l_theory = int_u - int_l
diff_d_l_theory = int_d - int_l

print(f"  (α_u-α_l) 拟合={diff_u_l_fit:.3f}, 理论={diff_u_l_theory:.3f}")
print(f"  (α_d-α_l) 拟合={diff_d_l_fit:.3f}, 理论={diff_d_l_theory:.3f}")

# 修正: 如果α差异 ∝ (int_u - int_l) 的线性函数
# α_u = α_l + k · (int_u - int_l)
# 求k使得匹配
k_u = diff_u_l_fit / diff_u_l_theory if diff_u_l_theory != 0 else 0
k_d = diff_d_l_fit / diff_d_l_theory if diff_d_l_theory != 0 else 0

print(f"\n比例因子 k_u = {k_u:.3f}, k_d = {k_d:.3f}")
print(f"(接近1表示γ_m积分直接解释α差异)")

# 如果 k≈1，则γ_m积分直接给出α差异
# 如果 k≠1，则需要谱流耦合权重修正

print(f"\n{'='*65}")
print("修正后的α预测")
print(f"{'='*65}")

# 使用 k = 0.5 (或最优拟合) 作为谱流耦合权重
k_opt = 0.5
alpha_u_pred = alpha_base + k_opt * (int_u - int_l)
alpha_d_pred = alpha_base + k_opt * (int_d - int_l)
alpha_l_pred = alpha_base

print(f"k = {k_opt:.3f} (谱流耦合权重)")
print(f"α_u_pred = {alpha_u_pred:.3f} (fit={alpha_u_fit:.3f})")
print(f"α_d_pred = {alpha_d_pred:.3f} (fit={alpha_d_fit:.3f})")
print(f"α_l_pred = {alpha_l_pred:.3f} (fit={alpha_l_fit:.3f})")

# 搜索最优 k
best_k = None
best_err = float('inf')
for k_try in np.linspace(-2, 2, 4001):
    a_u = alpha_base + k_try * diff_u_l_theory
    a_d = alpha_base + k_try * diff_d_l_theory
    err = (a_u - alpha_u_fit)**2 + (a_d - alpha_d_fit)**2
    if err < best_err:
        best_err = err
        best_k = k_try

print(f"\n最优 k = {best_k:.4f}, RMSE = {np.sqrt(best_err/2):.4f}")
alpha_u_opt = alpha_base + best_k * diff_u_l_theory
alpha_d_opt = alpha_base + best_k * diff_d_l_theory
print(f"α_u(opt) = {alpha_u_opt:.3f} (fit={alpha_u_fit:.3f}, ×{max(alpha_u_opt,alpha_u_fit)/min(alpha_u_opt,alpha_u_fit):.2f})")
print(f"α_d(opt) = {alpha_d_opt:.3f} (fit={alpha_d_fit:.3f}, ×{max(alpha_d_opt,alpha_d_fit)/min(alpha_d_opt,alpha_d_fit):.2f})")

# ============================================================
# 验证
# ============================================================
print(f"\n{'='*65}")
print("验证: 用最优 α 预测质量比")
print(f"{'='*65}")

c_norm = np.array([0.003314, 0.066554, 1.0])

# 实验值
exp = {'m_u/m_t': 1.27e-5, 'm_c/m_t': 0.00735,
       'm_d/m_b': 0.00112, 'm_s/m_b': 0.0222,
       'm_e/m_tau': 2.88e-4, 'm_mu/m_tau': 0.0595}

for name, a_pred, a_fit in [('上型', alpha_u_opt, alpha_u_fit),
                              ('下型', alpha_d_opt, alpha_d_fit),
                              ('轻子', alpha_l_pred, alpha_l_fit)]:
    pred = c_norm ** a_pred
    fit_pred = c_norm ** a_fit
    if name == '上型':
        e1, e2 = exp['m_u/m_t'], exp['m_c/m_t']
    elif name == '下型':
        e1, e2 = exp['m_d/m_b'], exp['m_s/m_b']
    else:
        e1, e2 = exp['m_e/m_tau'], exp['m_mu/m_tau']
    
    f1 = max(pred[0],e1)/min(pred[0],e1)
    f2 = max(pred[1],e2)/min(pred[1],e2)
    ff1 = max(fit_pred[0],e1)/min(fit_pred[0],e1)
    ff2 = max(fit_pred[1],e2)/min(fit_pred[1],e2)
    print(f"\n{name}: α_pred={a_pred:.3f} (fit={a_fit:.3f})")
    print(f"  轻: pred×{f1:.2f}, fit×{ff1:.2f}")
    print(f"  中: pred×{f2:.2f}, fit×{ff2:.2f}")
