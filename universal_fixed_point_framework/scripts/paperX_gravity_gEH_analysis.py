#!/usr/bin/env python3
"""
paperX_gravity_gEH_analysis.py — g_EH 转换因子的解析确定

从 Δ 的 Frobenius 范数平方到 Einstein-Hilbert 作用量系数的完整转换链。

关键关系:
  Δ ≈ [A_GR, δβ]·α'.h - β.h·[A_GR, δα]  (当 X.A=Y.A=Z.A=A_GR)
  G_N = c·Δλ_min²
  c = r_cat × F_cl17 × g_EH
  g_EH = c_Planck / (r_cat × F_cl17)
"""
import numpy as np
from numpy import linalg as LA

# ================================================================
# §1 精确代数值
# ================================================================
k_max = 8
k = np.arange(1, k_max + 1)
lam = np.sqrt(k * (k + 1))
lam = lam / lam[-1]  # λ₈ = 1
DL = lam[1] - lam[0]
n = 8  # A_GR 谱模数 k_max=8（2026-08-07 勘误标注：原注释"旋量维数"错误——Cl(1,7) 标准旋量 16 维，此 n 为 A_GR 矩阵谱模数非旋量维数）

# 精确解析公式
# λ_k = √{k(k+1)}/√72
# λ₁ = √2/√72, λ₂ = √6/√72, ...
# Δλ_min = (√6-√2)/√72
# Δλ_min² = (8-4√3)/72 = (2-√3)/18
# (λ₁²+λ₂²)/Δλ_min² = 2(2+√3) = 4+2√3
# F_cl17 = 8(2-√3) = 16-8√3
# c_Planck = 18(2+√3) = 36+18√3

DLsq_num = (2 - np.sqrt(3)) / 18  # 精确 Δλ_min²
c_Planck_exact = 18 * (2 + np.sqrt(3))  # = 1/Δλ_min²

print("=" * 72)
print("§1 精确代数值")
print("=" * 72)
print(f"  Δλ_min = (√6-√2)/√72 = {DL:.12f}")
print(f"  Δλ_min² = (2-√3)/18 = {DLsq_num:.12f}")
print(f"  (λ₁²+λ₂²)/Δλ_min² = 4+2√3 = {4+2*np.sqrt(3):.10f}")
print(f"  F_cl17 = 8(2-√3) = {8*(2-np.sqrt(3)):.10f}")
print(f"  c_Planck = 18(2+√3) = {c_Planck_exact:.10f}")

# ================================================================
# §2 交换子范数分析
# ================================================================
print("\n" + "=" * 72)
print("§2 ‖[A_GR, δ]‖_F² 的统计性质 (‖δ‖_F=1)")
print("=" * 72)

np.random.seed(42)
N = 50000

# 计算谱差平方
spec_diff_sq = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        spec_diff_sq[i][j] = (lam[i] - lam[j])**2
avg_spec_diff = np.sum(spec_diff_sq) / n**2

print(f"  谱差平均值 E[(λᵢ-λⱼ)²] = {avg_spec_diff:.6f}")

# Monte Carlo
comm_sq_vals = []
for _ in range(N):
    delta = (np.random.randn(n, n) + 1j * np.random.randn(n, n))
    delta = (delta + delta.conj().T) / 2
    delta = delta / LA.norm(delta, "fro")
    comm = lam[:, None] * delta - delta * lam[None, :]
    comm_sq_vals.append(LA.norm(comm, "fro") ** 2)

comm_sq_mean = np.mean(comm_sq_vals)
print(f"  E[‖[A_GR, δ]‖_F²] (N={N}) = {comm_sq_mean:.6f}")
print(f"  与谱差比 = {comm_sq_mean/avg_spec_diff:.6f}")

# 解析公式: E[‖[A_GR, δ]‖_F²] = (2/n²) Σ_{i<j} (λᵢ-λⱼ)²
# 对于随机 Hermitian δ (Wigner 矩阵, ‖δ‖_F²=1)
# 期望: E[|δ_ij|²] = 1/(n+1) for i=j, 1/(2(n+1)) for i≠j (GUE)
# 但这里我们用了不同的归一化

# 对于我们的归一化 (‖δ‖_F²=1, 实对角+复非对角):
# E[|δ_ii|²] = 1/n (n 个对角项, 每个方差的期望)
# E[|δ_ij|²] = 1/(2n) (n(n-1)/2 个实部 + n(n-1)/2 个虚部 = n(n-1) 个独立实变量)
# 验证: n×1/n + n(n-1)×1/(2n) = 1 + (n-1)/2 = (n+1)/2... 不等于 1

# 用对称归一化: δ = (X+X^†)/2, Tr(δ²) = 1
# 对于 X ~ iid 复高斯 N(0,σ²), nσ² = 1 (对角项方差 σ², 非对角项方差 σ²/2)
# 期望: E[|δ_ii|²] = σ² = 1/n (实值)
#       E[|δ_ij|²] = σ² = 1/n (复值, 实部和虚部各 σ²/2)
# 所以 E[‖[A_GR, δ]‖_F²] = Σ_ij (λᵢ-λⱼ)² × E[|δ_ij|²]
#                        = (1/n) Σ_ij (λᵢ-λⱼ)² = (1/n) × 2n Σ_i λᵢ² - (2/n)(Σ_i λᵢ)²
#                        = 2 Σ_i λᵢ² - (2/n)(Σ_i λᵢ)²

sum_lam = np.sum(lam)
sum_lam_sq = np.sum(lam**2)
E_comm_sq_theory = 2 * sum_lam_sq - (2/n) * sum_lam**2
print(f"  理论值 E[‖[A_GR, δ]‖_F²] = {E_comm_sq_theory:.6f}")
print(f"  MC/理论 = {comm_sq_mean/E_comm_sq_theory:.6f}")

# ================================================================
# §3 Δ 的精确到前导阶表达式
# ================================================================
print("\n" + "=" * 72)
print("§3 Δ 的前导阶表达式和 r_cat 的解析预测")
print("=" * 72)

# 当 X.A=Y.A=Z.A=A_GR 且 β.h = f(A_GR)+δβ, α'.h = g(A_GR)+δα:
# Δ = A_GR·β.h·α'.h - 2·β.h·A_GR·α'.h + β.h·α'.h·A_GR
# 展开到一阶 O(Δλ_min):
# Δ ≈ [A_GR, δβ]·g + f·[A_GR, δα] - f·g·[A_GR, δα] - [A_GR, δβ]·g  ... 简化

# 精确: β = f + δβ, α = g + δα
# Δ = A_GR·(f+δβ)·(g+δα) - 2(f+δβ)·A_GR·(g+δα) + (f+δβ)·(g+δα)·A_GR
#   = A_GR·f·g + A_GR·f·δα + A_GR·δβ·g + A_GR·δβ·δα
#   - 2f·A_GR·g - 2f·A_GR·δα - 2δβ·A_GR·g - 2δβ·A_GR·δα
#   + f·g·A_GR + f·δα·A_GR + δβ·g·A_GR + δβ·δα·A_GR

# 零阶 (O(Δλ⁰)): f·g 项
# A_GR·f·g - 2f·A_GR·g + f·g·A_GR = 0  (因为 f,g 与 A_GR 对易)

# 一阶 O(Δλ):
# A_GR·f·δα + A_GR·δβ·g - 2f·A_GR·δα - 2δβ·A_GR·g + f·δα·A_GR + δβ·g·A_GR
# = [A_GR, f]·δα + f·[A_GR, δα] + [A_GR, δβ]·g + δβ·[A_GR, g]
# = 0 + f·[A_GR, δα] + [A_GR, δβ]·g + 0
# = [A_GR, δβ]·g + f·[A_GR, δα]

# 所以 Δ ≈ [A_GR, δβ]·g(A_GR) + f(A_GR)·[A_GR, δα]

# 对于独立 δβ, δα:
# E[‖Δ‖_F²] = E[‖[A_GR, δβ]·g‖²] + E[‖f·[A_GR, δα]‖²]
#           ≈ 2 × E[‖[A_GR, δ]·f‖_F²]  (对称性)

# 现在 f(A_GR) 与 A_GR 对易:
# [A_GR, δ]·f = (A_GR·δ - δ·A_GR)·f = A_GR·(δ·f) - δ·(A_GR·f)
# 由于 f 与 A_GR 对易: A_GR·f = f·A_GR
# = A_GR·(δ·f) - δ·(f·A_GR) = A_GR·(δ·f) - (δ·f)·A_GR
# = [A_GR, δ·f]

# 所以 ‖[A_GR, δ]·f‖_F = ‖[A_GR, δ·f]‖_F (当 [f, A_GR]=0)

# 但 δ·f 与 δ 有不同范数:
# ‖δ·f‖_F ≤ ‖δ‖_F · ‖f‖_₂ ≤ ‖δ‖_F · (f 的谱范数)

# Monte Carlo 验证
np.random.seed(42)
N2 = 5000
r_vals_exact = []  # 前导阶近似

for _ in range(N2):
    cf_b = np.random.randn(3)
    cf_a = np.random.randn(3)
    f_b = (cf_b[0] * np.eye(n) + cf_b[1] * np.diag(lam) + cf_b[2] * np.diag(lam**2))
    f_a = (cf_a[0] * np.eye(n) + cf_a[1] * np.diag(lam) + cf_a[2] * np.diag(lam**2))
    f_b = f_b / LA.norm(f_b, "fro")
    f_a = f_a / LA.norm(f_a, "fro")

    db = (np.random.randn(n, n) + 1j * np.random.randn(n, n))
    db = (db + db.conj().T) / 2
    db = db / LA.norm(db, "fro") * DL
    da = (np.random.randn(n, n) + 1j * np.random.randn(n, n))
    da = (da + da.conj().T) / 2
    da = da / LA.norm(da, "fro") * DL

    A_GR_mat = np.diag(lam)

    # 前导阶: Δ ≈ [A_GR, δβ]·g + f·[A_GR, δα]
    Delta_lead = (A_GR_mat @ db - db @ A_GR_mat) @ f_a + f_b @ (A_GR_mat @ da - da @ A_GR_mat)

    # 完整 Δ
    beta_h = (f_b + db) / LA.norm(f_b + db, "fro")
    alpha_h = (f_a + da) / LA.norm(f_a + da, "fro")
    H = beta_h @ alpha_h
    Delta_full = A_GR_mat @ H - 2 * beta_h @ A_GR_mat @ alpha_h + H @ A_GR_mat

    r_vals_exact.append(LA.norm(Delta_lead, "fro") ** 2 / DL**2)

r_mean_lead = np.mean(r_vals_exact)
print(f"  Δ ≈ [A_GR,δβ]·g + f·[A_GR,δα] 的前导阶:")
print(f"  r_lead = E[‖Δ‖_F²/Δλ²] = {r_mean_lead:.6f} ± {np.std(r_vals_exact):.6f}")

# 理论预测:
# E[‖[A_GR, δ]·f‖_F²] (固定 f, 对 δ 平均)
# = (1/n) × Σ_ij (λᵢ-λⱼ)² × f_jj² × E[|δ_ij|²] / ...
# 简化: f 与 A_GR 对易 → 与 lam 相同基 → [A_GR, δ]·f 的 ij 元 = (λᵢ-λⱼ)·δ_ij·f_jj
# E[‖[A_GR, δ]·f‖_F²] = Σ_ij (λᵢ-λⱼ)² × E[|δ_ij|²] × f_jj²
# 对于 E[|δ_ij|²] = 1/n (对角), 0 (非对角)?  

# 实际上 δ 是 Hermitian, 归一化 ‖δ‖_F²=1:
# δ_ii ~ N(0,1/n) (实), δ_ij ~ N(0,1/(2n)) + i·N(0,1/(2n)) (复)
# 所以 E[|δ_ij|²] = 1/n for all i,j

# E[‖[A_GR, δ]·f‖_F²] = (1/n) Σ_ij (λᵢ-λⱼ)² × f_jj²

# 而 ‖f‖_F² = Σ_j f_jj² = 1 (因为 f 与 A_GR 对易, 在 A_GR 基下对角)

# 所以 E[‖[A_GR, δ]·f‖_F²] = (1/n) Σ_ij (λᵢ-λⱼ)² × f_jj²
# 对 f 平均 (f 随机归一化):
# E_f[E_δ[‖[A_GR, δ]·f‖_F²]] = (1/n) × E_δ[‖[A_GR, δ]‖_F²] (因为 E[f_jj²] = 1/n)
#                              = (1/n) × comm_sq_mean

# 所以: E[r_cat] = 2 × (1/n) × E_δ[‖[A_GR, δ]‖_F²] / Δλ_min²
#              = 2 × (1/8) × comm_sq_mean / Δλ_min²

r_pred = 2 * (1/n) * comm_sq_mean / DL**2
print(f"  理论预测 r_pred = 2×(1/n)×E[‖[A,δ]‖²]/Δλ² = {r_pred:.6f}")

# 更精确: 用 E_comm_sq_theory
r_pred2 = 2 * (1/n) * E_comm_sq_theory / DL**2
print(f"  理论预测 (精确公式) r_pred = {r_pred2:.6f}")

# 现在 E_comm_sq_theory = 2Σλᵢ² - (2/n)(Σλᵢ)²
# 我们需要计算这些和

print(f"\n  Σλᵢ = {sum_lam:.10f}")
print(f"  Σλᵢ² = {sum_lam_sq:.10f}")

# Σλᵢ = (√2+√6+√12+√20+√30+√42+√56+√72)/√72
# Σλᵢ² = (2+6+12+20+30+42+56+72)/72 = 240/72 = 10/3

sum_lam_sq_exact = 10/3
print(f"  Σλᵢ² (精确) = {sum_lam_sq_exact}")

# Σλᵢ 的精确值？
# λ_k = √{k(k+1)}/√72 = (1/√72) × √{k(k+1)}
# Σλᵢ = (1/√72) × Σ √{k(k+1)}
# = (√2+√6+√12+√20+√30+√42+√56+√72)/√72

sum_sqrt_kk1 = np.sum(np.sqrt(k*(k+1)))
print(f"  Sum sqrt(k(k+1)) for k=1..8 = {sum_sqrt_kk1:.10f}")

# E_comm_sq_theory 的解析形式
# E[‖[A_GR, δ]‖_F²] = 2 × 10/3 - (2/8) × (Σλᵢ)²
# = 20/3 - (1/4)(Σλᵢ)²
E_comm_exact = 2 * sum_lam_sq_exact - (2/n) * sum_lam**2
print(f"  E[‖[A,δ]‖²] (‖δ‖_F=1) = {E_comm_exact:.10f}")

r_final = 2 * (1/n) * E_comm_exact / DLsq_num
print(f"\n  最终理论 r_pred = 2 × (1/{n}) × {E_comm_exact:.6f} / {DLsq_num:.10f}")
print(f"                = {r_final:.10f}")

# 与 MC 结果比较
print(f"  MC r_mean ≈ 0.040 → 与理论比: {0.040/r_final:.4f}")

# ================================================================
# §4 g_EH 的解析闭式
# ================================================================
print("\n" + "=" * 72)
print("§4 g_EH 的解析闭式")
print("=" * 72)

# r_pred = 2 × (1/n) × (2Σλᵢ² - (2/n)(Σλᵢ)²) / Δλ²
# = (4/n·Σλᵢ² - 4/n²·(Σλᵢ)²) / Δλ²
# 
# g_EH = c_Planck / (r_pred × F_cl17)
# c_Planck = 1/Δλ²
# F_cl17 = 8(2-√3)
# r_pred = (4/n·Σλᵢ² - 4/n²·(Σλᵢ)²) / Δλ²
# 
# g_EH = 1/Δλ² × 1/(r_pred × F_cl17)
#      = 1 / [r_pred × F_cl17 × Δλ²]

# 先计算数值
r_analytical = r_final
g_EH_analytical = c_Planck_exact / (r_analytical * 8*(2-np.sqrt(3)))
print(f"  r_analytical = {r_analytical:.10f}")
print(f"  F_cl17 = {8*(2-np.sqrt(3)):.10f}")
print(f"  g_EH = {c_Planck_exact:.4f} / ({r_analytical:.6f} × {8*(2-np.sqrt(3)):.6f})")
print(f"       = {g_EH_analytical:.4f}")

# 检查 g_EH 是否能写成闭式
# g_EH = 1 / (r_pred × F_cl17 × Δλ²)
# r_pred × Δλ² = 4/n·Σλᵢ² - 4/n²·(Σλᵢ)²
# F_cl17 = 8(2-√3)
# c_Planck = 1/Δλ²

# 合并: g_EH = 1 / [(4/n·Σλᵢ² - 4/n²·(Σλᵢ)²) × 8(2-√3)]

# 代入 n=8, Σλᵢ²=10/3:
# 4/8 × 10/3 = 40/24 = 5/3
# 4/64 × (Σλᵢ)² = (1/16)(Σλᵢ)²

# g_EH = 1 / [(5/3 - (Σλᵢ)²/16) × 8(2-√3)]

# 现在关键: Σλᵢ 的闭式?
# λ_k = √{k(k+1)}/√72 for k=1,...,8
# Σλᵢ = (1/√72) × Σ_{k=1}^{8} √{k(k+1)}
# Σ √{k(k+1)} 没有简单的闭式...

# 但我们可以保留数值形式
print(f"\n  Σ√{{k(k+1)}} = {sum_sqrt_kk1:.10f}")
print(f"  Σλᵢ = {sum_sqrt_kk1/np.sqrt(72):.10f}")

# g_EH 的数值分解
print(f"\n  g_EH 分解:")
print(f"  g_EH = {g_EH_analytical:.4f}")
print(f"  g_EH/(8π) = {g_EH_analytical/(8*np.pi):.4f}")
print(f"  g_EH/(16π) = {g_EH_analytical/(16*np.pi):.4f}")
print(f"  g_EH/(4π) = {g_EH_analytical/(4*np.pi):.4f}")
print(f"  8π = {8*np.pi:.6f}")
print(f"  16π = {16*np.pi:.6f}")

# 寻找闭式: g_EH 是否等于 16π × (Σλᵢ²/Δλ²) × something?
factor_16pi = g_EH_analytical / (16*np.pi)
print(f"\n  g_EH/(16π) = {factor_16pi:.6f}")

# 检查是否等于 Tr(A_GR²)/n × (something)
print(f"  Σλᵢ² = {sum_lam_sq_exact}")
print(f"  n→4 维度缩减因子: {n/4}")
print(f"  16π × 31 ≈ {16*np.pi*31:.4f}")
print(f"  16π × (Σλᵢ² × n/4) = {16*np.pi * sum_lam_sq_exact * n/4:.4f}")
print(f"  16π × (Σλᵢ² × n/4) / DL²²...")

# 最终答案: g_EH 的解析表达式包含
# 1. 16π 来自 Einstein-Hilbert 归一化
# 2. 谱结构因子 (从 commutator 方差)
# 3. 维数转换 8/4

eh_factor = g_EH_analytical / (16*np.pi)
print(f"\n  >>> g_EH = 16π × {eh_factor:.6f}")
print(f"  >>> {eh_factor:.6f} = f(谱结构, n=8, Δλ², Σλᵢ²)")
print(f"  >>> 即 g_EH = 16π × (n²/2(n-1)) × (Δλ²/(Σλᵢ²)) × ...???")
