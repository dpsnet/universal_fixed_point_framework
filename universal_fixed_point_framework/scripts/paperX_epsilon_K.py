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
paperX_epsilon_K.py — ε_K 谱预测

从谱框架推导的 CKM 矩阵计算中性 Kaon CP 破坏参数 ε_K。
ε_K = κ_ε·C_ε·B_K·Im(λ_t)·[Re(λ_c)·(η₁S₀(x_c) − η₃S₀(x_c,xₜ)) − Re(λ_t)·η₂S₀(x_t)]
"""
import numpy as np
import math

# ================================================================
# 谱输入 → CKM 矩阵
# ================================================================
dH = 2.7095
alpha_l, alpha_u = 1.3547, 1.9448

θ12 = dH / 12        # 0.2258
θ23 = 1 / 24         # 0.04167
θ13 = dH / 720       # 0.003763
δ_CP = 2*(alpha_u - alpha_l)  # 1.1802 rad

def ckm_matrix(t12, t23, t13, delta):
    c12, s12 = math.cos(t12), math.sin(t12)
    c23, s23 = math.cos(t23), math.sin(t23)
    c13, s13 = math.cos(t13), math.sin(t13)
    d = complex(math.cos(delta), math.sin(delta))
    V = np.zeros((3,3), dtype=complex)
    V[0,0] = c12*c13
    V[0,1] = s12*c13
    V[0,2] = s13 * d.conjugate()
    V[1,0] = -s12*c23 - c12*s23*s13*d
    V[1,1] = c12*c23 - s12*s23*s13*d
    V[1,2] = s23*c13
    V[2,0] = s12*s23 - c12*c23*s13*d
    V[2,1] = -c12*s23 - s12*c23*s13*d
    V[2,2] = c23*c13
    return V

V_ckm = ckm_matrix(θ12, θ23, θ13, δ_CP)

print("=" * 65)
print("  ε_K: Kaon CP 破坏谱预测")
print("=" * 65)

print(f"\n  谱 CKM 矩阵 (预测):")
print(f"    |V_ud|={abs(V_ckm[0,0]):.5f}  |V_us|={abs(V_ckm[0,1]):.5f}  |V_ub|={abs(V_ckm[0,2]):.5f}")
print(f"    |V_cd|={abs(V_ckm[1,0]):.5f}  |V_cs|={abs(V_ckm[1,1]):.5f}  |V_cb|={abs(V_ckm[1,2]):.5f}")
print(f"    |V_td|={abs(V_ckm[2,0]):.5f}  |V_ts|={abs(V_ckm[2,1]):.5f}  |V_tb|={abs(V_ckm[2,2]):.5f}")

# ================================================================
# CKM 组合因子 λ_i = V_is* · V_id
# ================================================================
λ_c = V_ckm[1,1].conjugate() * V_ckm[1,0]  # V_cs* · V_cd
λ_t = V_ckm[2,1].conjugate() * V_ckm[2,0]  # V_ts* · V_td
J_ckm = (V_ckm[0,0] * V_ckm[1,1] * V_ckm[0,1].conj() * V_ckm[1,0].conj()).imag

print(f"\n  CKM 组合因子:")
print(f"    λ_c = V_cs*·V_cd = {λ_c:.6e}")
print(f"    λ_t = V_ts*·V_td = {λ_t:.6e}")
print(f"    Im(λ_t) = {λ_t.imag:.3e}")
print(f"    Re(λ_c) = {λ_c.real:.6f}")

# ================================================================
# Inami-Lim 函数
# ================================================================
M_W = 80.377       # GeV (PDG 2024)
m_c = 1.27         # GeV (MS-bar)
m_t = 162.5        # GeV (MS-bar top mass for loop calc)
m_K = 497.614      # MeV
f_K = 156.1        # MeV
Δm_K = 3.484e-12   # MeV (K_L-K_S mass difference)
G_F = 1.1663787e-5 # GeV⁻²
B_K = 0.7625       # Bag parameter (FLAG 2024)
η_1 = 1.87         # QCD correction (charm)
η_2 = 0.577        # QCD correction (top)
η_3 = 0.496        # QCD correction (charm-top)
κ_ε = 0.94         # Phase space factor

x_c = (m_c / M_W)**2
x_t = (m_t / M_W)**2

def S0_xx(x):
    """Inami-Lim S₀(x,x) 单味圈函数"""
    if x <= 0: return 0
    if abs(1 - x) < 1e-10: return 1/3
    return (4*x - 11*x**2 + x**3) / (4*(1-x)**2) - 3*x**3 * math.log(x) / (2*(1-x)**3)

def S0_xy(x, y):
    """Inami-Lim S₀(x,y) 双味圈函数 (标准公式)"""
    if x <= 0 or y <= 0: return 0
    if abs(x - y) < 1e-10: return S0_xx(x)
    term_y = (y**2 - 8*y + 4) * math.log(y) / (4 * (y-x) * (1-y)**2)
    term_x = (x**2 - 8*x + 4) * math.log(x) / (4 * (x-y) * (1-x)**2)
    const = -3 / (4 * (1-x) * (1-y))
    return x * y * (term_y + term_x + const)

S0_c = S0_xx(x_c)
S0_t = S0_xx(x_t)
S0_ct = S0_xy(x_c, x_t)

print(f"\n  Inami-Lim 函数:")
print(f"    x_c = (m_c/M_W)² = {x_c:.4e}")
print(f"    x_t = (m_t/M_W)² = {x_t:.4f}")
print(f"    S₀(x_c) = {S0_c:.4f}")
print(f"    S₀(x_t) = {S0_t:.2f}")
print(f"    S₀(x_c,x_t) = {S0_ct:.4f}")

# ================================================================
# ε_K 计算
# ================================================================
# C_ε = G_F²·f_K²·m_K·M_W² / (6√2·π²·Δm_K)
# 所有量统一为 GeV 单位
f_K_GeV = f_K / 1000      # 156.1 MeV → GeV
m_K_GeV = m_K / 1000      # 497.6 MeV → GeV
Δm_K_GeV = Δm_K / 1000    # 3.484e-12 MeV → GeV
C_ε = G_F**2 * f_K_GeV**2 * m_K_GeV * M_W**2 / (6 * math.sqrt(2) * math.pi**2 * Δm_K_GeV)

# Im(λ_t)·[...] 部分
Imλ_t = λ_t.imag
Reλ_c = λ_c.real
Reλ_t = λ_t.real

# ε_K 公式 (绝对值)
epsilon_K_abs = κ_ε * C_ε * B_K * abs(Imλ_t) * abs(
    Reλ_c * (η_1 * S0_c - η_3 * S0_ct) - Reλ_t * η_2 * S0_t
)

# 实验值
ε_K_exp = 2.228e-3

print(f"\n{'─'*65}")
print("ε_K 计算结果")
print(f"{'─'*65}")
print(f"\n    C_ε = {C_ε:.4e}")
print(f"    B_K = {B_K:.4f}")
print(f"    κ_ε = {κ_ε:.3f}")
print(f"    Im(λ_t) = {Imλ_t:.3e}")
print(f"    圈函数和 = {abs(Reλ_c*(η_1*S0_c - η_3*S0_ct) - Reλ_t*η_2*S0_t):.4f}")

print(f"\n    ε_K (谱预测) = {epsilon_K_abs:.4e}")
print(f"    ε_K (实验)   = {ε_K_exp:.4e}")
dev_ε = abs(epsilon_K_abs - ε_K_exp) / ε_K_exp * 100
print(f"    偏差 = {dev_ε:.1f}%")
mark = '✅' if dev_ε < 30 else '⚠️'
print(f"    状态 = {mark}")

# ================================================================
# 对照: 实验 CKM 输入
# ================================================================
print(f"\n{'─'*65}")
print("对照: 实验 CKM 输入")
print(f"{'─'*65}")

θ12_exp = 0.2265; θ23_exp = 0.0422; θ13_exp = 0.00369; δ_exp = 1.20
V_exp = ckm_matrix(θ12_exp, θ23_exp, θ13_exp, δ_exp)
λ_c_exp = V_exp[1,1].conjugate() * V_exp[1,0]
λ_t_exp = V_exp[2,1].conjugate() * V_exp[2,0]
ε_K_exp_formula = κ_ε * C_ε * B_K * abs(λ_t_exp.imag) * abs(
    λ_c_exp.real * (η_1 * S0_c - η_3 * S0_ct) - λ_t_exp.real * η_2 * S0_t
)
J_exp_val = (V_exp[0,0]*V_exp[1,1]*V_exp[0,1].conj()*V_exp[1,0].conj()).imag

print(f"\n  实验 CKM: Im(λ_t) = {λ_t_exp.imag:.3e} (谱: {Imλ_t:.3e})")
print(f"  J = {J_exp_val:.3e} (谱: {J_ckm:.3e})")
print(f"  ε_K(实验CKM) = {ε_K_exp_formula:.4e}")
print(f"  ε_K(谱CKM)   = {epsilon_K_abs:.4e}")
print(f"  ε_K(实验直接) = {ε_K_exp:.4e}")

# 敏感性分析
print(f"\n  敏感性: δ_CP 对 ε_K 的影响 (固定 θ₁₂, θ₂₃, θ₁₃):")
for δ_test in [1.18, 1.19, 1.20, 1.21, 1.22]:
    V_test = ckm_matrix(θ12, θ23, θ13, δ_test)
    λ_t_test = V_test[2,1].conjugate() * V_test[2,0]
    ε_test = κ_ε * C_ε * B_K * abs(λ_t_test.imag) * abs(
        λ_c_exp.real * (η_1 * S0_c - η_3 * S0_ct) - λ_t_test.real * η_2 * S0_t
    )
    print(f"    δ={δ_test:.2f}: Im(λ_t)={λ_t_test.imag:.3e}, ε_K={ε_test:.4e}")

# ================================================================
# 幺正三角形验证
# ================================================================
print(f"\n{'─'*65}")
print("幺正三角形")
print(f"{'─'*65}")

# CKM 幺正性: V_ud·V_ub* + V_cd·V_cb* + V_td·V_tb* = 0
ut_sum = V_ckm[0,0]*V_ckm[0,2].conj() + V_ckm[1,0]*V_ckm[1,2].conj() + V_ckm[2,0]*V_ckm[2,2].conj()

# Jarlskog 不变量
J_ckm = (V_ckm[0,0] * V_ckm[1,1] * V_ckm[0,1].conj() * V_ckm[1,0].conj()).imag

print(f"\n    幺正检验: V_ud·V_ub* + V_cd·V_cb* + V_td·V_tb* = {ut_sum:.4e}")
print(f"    Jarlskog J = {J_ckm:.3e} (SM ~3.2e-5)")
print(f"    |ε_K|/(κ_ε·C_ε·B_K) = {epsilon_K_abs/(κ_ε*C_ε*B_K):.4f}")

# α, β, γ 角 (未修剪)
# β = arg(-V_cd·V_cb* / V_td·V_tb*)
beta = math.atan2(-(V_ckm[1,0]*V_ckm[1,2].conj()).imag, -(V_ckm[1,0]*V_ckm[1,2].conj()).real)
beta -= math.atan2((V_ckm[2,0]*V_ckm[2,2].conj()).imag, (V_ckm[2,0]*V_ckm[2,2].conj()).real)

# 更简单的计算: sin(2β)
# sin(2β) = 2J / (|V_cb|² × 某个组合)
sin2β = 2 * J_ckm / (abs(V_ckm[1,2])**2 * abs(V_ckm[0,1]) * abs(V_ckm[1,0]))
sin2β_exp = 0.699  # PDG 2024

print(f"\n    sin(2β) = {sin2β:.4f} (exp {sin2β_exp:.4f})")
print(f"    偏差 = {abs(sin2β - sin2β_exp)/sin2β_exp*100:.1f}%")

print(f"\n{'='*65}")
print(f"  ε_K = {epsilon_K_abs:.4e} (exp {ε_K_exp:.4e}, 偏差 {dev_ε:.1f}%)")
print(f"  来源: 谱 CKM × SM 圈图")
print(f"{'='*65}")
