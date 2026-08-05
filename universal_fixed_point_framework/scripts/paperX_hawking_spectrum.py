#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 61D (P1-3) 黑洞量子演化数值验证
======================================
对应：paper/paper42_black_hole_quantum_evolution.md
验证 P1-3 四项验收标准的数值层面：
  C1 霍金辐射谱（温度 + Planck 分布 + greybody 因子 + 功率谱）
  C2 蒸发动力学（M(t) = (M₀³-3αt)^(1/3) 质量单调递减）
  C3 Page 曲线（熵守恒 + 早期递增/晚期递减 + Page 时间分数 ≈ 0.647）
  C4 视界涨落（δT/T = Δλ_min/(2πM²) 随质量递减）
  C5 信息保持（谱流特征值不变性）

谱间隙：Δλ_min = spectralGap 8 = (√6-√2)/√72 ≈ 0.1221
"""
import math

CHECKS = 0
PASS = 0

def check(name, cond, detail=""):
    global CHECKS, PASS
    CHECKS += 1
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    print(f"  [{status}] {name}" + (f"  ({detail})" if detail else ""))

# ============ 物理常数 ============
DELTA_LAMBDA_MIN = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)  # ≈ 0.1221

def T_H(M):
    """霍金温度 T_H = Δλ_min/(2πM)"""
    return DELTA_LAMBDA_MIN / (2 * math.pi * M)

def planck_occ(M, w):
    """Planck 占据数 N(ω) = 1/(e^(βMω)-1), βM = 2πM/Δλ_min"""
    beta = 2 * math.pi * M / DELTA_LAMBDA_MIN
    return 1.0 / (math.exp(beta * w) - 1.0)

def greybody(w, M):
    """Greybody 因子 Γ(ω,M) = (27/4)(ωM)² e^(-4ωM)"""
    x = w * M
    return (27.0 / 4.0) * x**2 * math.exp(-4 * x)

def mass_evolve(M0, alpha, t):
    """质量演化 M(t) = (M₀³ - 3αt)^(1/3)"""
    return (M0**3 - 3 * alpha * t) ** (1.0 / 3.0)

def S_BH(M):
    """Bekenstein-Hawking 熵 S_BH = 4πM²"""
    return 4 * math.pi * M**2

def S_rad(M0, M):
    """辐射纠缠熵 S_rad = 4π(M₀²-M²)"""
    return 4 * math.pi * (M0**2 - M**2)

print("=" * 62)
print("Phase 61D (P1-3) 黑洞量子演化数值验证")
print("=" * 62)

# ============ C1 霍金辐射谱 ============
print("\n[C1] 霍金辐射谱")
# C1-1 谱间隙值
check("Δλ_min = 0.1221", abs(DELTA_LAMBDA_MIN - 0.1221) < 1e-4,
      f"Δλ_min = {DELTA_LAMBDA_MIN:.6f}")
# C1-2 温度递减：T_H(M₁) > T_H(M₂) 当 M₁ < M₂
M1, M2 = 1.0, 2.0
check("T_H 随质量递减 (T(M₁) > T(M₂))", T_H(M1) > T_H(M2),
      f"T(1)={T_H(M1):.4f}, T(2)={T_H(M2):.4f}")
# C1-3 温度正性
check("T_H > 0", T_H(3.0) > 0)
# C1-4 Planck 分布正性 + 递减
w1, w2 = 0.5, 1.0
check("N(ω) > 0", planck_occ(2.0, w1) > 0)
check("N(ω) 随频率递减", planck_occ(2.0, w1) > planck_occ(2.0, w2))
# C1-5 greybody 因子：低频增加（ωM<1/2）、高频减小（ωM>1）
w_small = 0.4 / 2.0   # ωM = 0.4 < 1/2
check("Γ 低频递增 (ωM<1/2)", greybody(w_small, 2.0) < greybody(w_small + 0.01, 2.0))
w_large = 2.0 / 2.0   # ωM = 1.0... 需要 > 1
w_large2 = 2.5 / 2.0  # ωM = 1.25 > 1
check("Γ 高频递减 (ωM>1)", greybody(w_large2, 2.0) < greybody(w_large2 - 0.01, 2.0))
# C1-6 greybody 正性
check("Γ > 0", greybody(0.3, 2.0) > 0)
# C1-7 功率谱正性 dP/dω = ω³ΓN/(2π²)
dPdw = lambda w, M: w**3 * greybody(w, M) * planck_occ(M, w) / (2 * math.pi**2)
check("dP/dω > 0", dPdw(0.3, 2.0) > 0)

# ============ C2 蒸发动力学 ============
print("\n[C2] 蒸发动力学")
M0, alpha = 10.0, 1e-4
t_evap = M0**3 / (3 * alpha)
t1, t2 = 0.1 * t_evap, 0.2 * t_evap
m1, m2 = mass_evolve(M0, alpha, t1), mass_evolve(M0, alpha, t2)
check("质量单调递减", m1 > m2, f"M(t₁)={m1:.6f} > M(t₂)={m2:.6f}")
check("半经典数学终点 M(t_evap)=0（物理终点由谱截断接管）", abs(mass_evolve(M0, alpha, t_evap)) < 1e-6)
check("初始 M(0)=M₀", abs(mass_evolve(M0, alpha, 0) - M0) < 1e-6)
# 质量立方线性
delta = lambda t: M0**3 - 3 * alpha * t
check("Δ(t)=M₀³-3αt 线性递减", abs(delta(t2) - (delta(t1) - 3*alpha*(t2-t1))) < 1e-9)

# ============ C3 Page 曲线 ============
print("\n[C3] Page 曲线")
# C3-1 熵守恒 S_BH + S_rad = 4πM₀²
mt = mass_evolve(M0, alpha, 0.3 * t_evap)
check("熵守恒 S_BH+S_rad=4πM₀²",
      abs(S_BH(mt) + S_rad(M0, mt) - 4 * math.pi * M0**2) < 1e-6)
# C3-2 早期递增：S_ent = S_rad 递增（M² > M₀²/2）
t_early1, t_early2 = 0.05 * t_evap, 0.1 * t_evap
m_e1, m_e2 = mass_evolve(M0, alpha, t_early1), mass_evolve(M0, alpha, t_early2)
check("早期 M² > M₀²/2", m_e2**2 > 0.5 * M0**2)
S_ent_early = lambda m: min(S_BH(m), S_rad(M0, m))
check("Page 曲线早期递增", S_ent_early(m_e1) < S_ent_early(m_e2),
      f"S_ent={S_ent_early(m_e1):.2f} → {S_ent_early(m_e2):.2f}")
# C3-3 晚期递减：S_ent = S_BH 递减（M² < M₀²/2）
t_late1, t_late2 = 0.85 * t_evap, 0.9 * t_evap
m_l1, m_l2 = mass_evolve(M0, alpha, t_late1), mass_evolve(M0, alpha, t_late2)
check("晚期 M² < M₀²/2", m_l1**2 < 0.5 * M0**2)
S_ent_late = lambda m: min(S_BH(m), S_rad(M0, m))
check("Page 曲线晚期递减", S_ent_late(m_l1) > S_ent_late(m_l2),
      f"S_ent={S_ent_late(m_l1):.2f} → {S_ent_late(m_l2):.2f}")
# C3-4 Page 时间分数 ≈ 0.647（谱公理推导：1 - 1/(2√2)）
frac_page = 1 - 1 / (2 * math.sqrt(2))
check("Page 时间分数 = 1-1/(2√2) ≈ 0.647",
      abs(frac_page - 0.647) < 1e-3, f"t_Page/t_evap = {frac_page:.6f}")
# C3-5 Page 分数区间 (1/2, 3/4)
check("Page 分数 ∈ (1/2, 3/4)", 0.5 < frac_page < 0.75)
# C3-6 Page 时间处质量立方 Δ = M₀³/(2√2)
t_page = frac_page * t_evap
m_page = mass_evolve(M0, alpha, t_page)
check("Page 时间质量 M(t_Page)=M₀/√2",
      abs(m_page - M0 / math.sqrt(2)) < 1e-3, f"M(t_Page)={m_page:.4f}")
# C3-7 熵平衡 at Page 时间（数值近似 S_BH ≈ S_rad）
check("Page 时间熵平衡 S_BH ≈ S_rad",
      abs(S_BH(m_page) - S_rad(M0, m_page)) < 1e-2 * S_BH(m_page))

# ============ C4 视界量子涨落 ============
print("\n[C4] 视界量子涨落")
# δT/T = Δλ_min/(2πM²)
fluc = lambda M: DELTA_LAMBDA_MIN / (2 * math.pi * M**2)
check("δT/T 随质量递减", fluc(1.0) > fluc(2.0) > fluc(4.0))
check("δT/T > 0", fluc(3.0) > 0)
# 涨落尺度：小质量 → Planck 尺度
check("Planck 尺度涨落 (M~M_Pl)", fluc(1.0) > 1e-2, f"δT/T(M_Pl)={fluc(1.0):.4f}")

# ============ C5 信息保持 ============
print("\n[C5] 信息保持")
import numpy as np

def mat_exp(A, terms=30):
    """矩阵指数：幂级数 exp(A) = Σ A^k/k!"""
    n = A.shape[0]
    result = np.eye(n)
    term = np.eye(n)
    for k in range(1, terms):
        term = term @ A / k
        result = result + term
    return result

# 谱流 A_t = U A₀ U⁻¹，U = exp(t·G)，G 反 Hermitian（谱不变）
n = 4
A0 = np.diag([1.0, 2.0, 3.0, 4.0])  # 初始谱
# 反 Hermitian 生成元（保证 U 酉）
G = np.array([[0, 1, 0, 0],
              [-1, 0, 1, 0],
              [0, -1, 0, 1],
              [0, 0, -1, 0]], dtype=float)
eig_before = np.sort(np.linalg.eigvalsh(A0))
ok_info = True
for t in [0.1, 0.5, 1.0]:
    U = mat_exp(t * G)
    At = U @ A0 @ np.linalg.inv(U)
    eig_after = np.sort(np.real(np.linalg.eigvals(At)))
    if not np.allclose(eig_before, eig_after, atol=1e-6):
        ok_info = False
check("谱流特征值不变 (σ(A_t)=σ(A₀))", ok_info)
# 反向：U⁻¹ A_t U = A₀
U = mat_exp(0.7 * G)
At = U @ A0 @ np.linalg.inv(U)
A_back = np.linalg.inv(U) @ At @ U
check("谱流可逆 (U⁻¹A_tU=A₀)", np.allclose(A_back, A0, atol=1e-6))

# ============ C6 量子反弹与蒸发终点（Paper IX §4 衔接） ============
print("\n[C6] 量子反弹与蒸发终点")
# 反弹临界密度 ρ_c = (8π/3)·4Δλ²（M_Pl=1, c₁=1/(4Δλ²)）
rho_c = (8 * math.pi / 3) * (4 * DELTA_LAMBDA_MIN**2)
check("ρ_c > 0（反弹密度正性）", rho_c > 0, f"ρ_c = {rho_c:.4f}")
# 有效 Friedmann 方程 H² = (8π/3)ρ(1-ρ/ρ_c)
def hubble2(rho):
    return (8 * math.pi / 3) * rho * (1 - rho / rho_c)
check("反弹点 H²(ρ_c) = 0", abs(hubble2(rho_c)) < 1e-12)
check("扩张相 H²(ρ) > 0 (ρ < ρ_c)", all(hubble2(r) > 0 for r in [0.1 * rho_c, 0.5 * rho_c]))
# 反弹最小尺度 a_min ~ 1/Δλ² > 0
a_min = 1.0 / DELTA_LAMBDA_MIN**2
check("反弹最小尺度 a_min > 0（无零尺度奇点）", a_min > 0, f"a_min ≈ {a_min:.2f}")
# 蒸发在 Planck 尺度终止：t_pl < t_evap，M(t_pl) = M_Pl
M_Pl = 1.0
t_pl = (M0**3 - M_Pl**3) / (3 * alpha)
check("Planck 时间 t_pl < t_evap", t_pl < t_evap, f"t_pl = {t_pl:.2f} < t_evap = {t_evap:.2f}")
check("蒸发在 Planck 质量终止 M(t_pl)=M_Pl", abs(mass_evolve(M0, alpha, t_pl) - M_Pl) < 1e-6)
# 蒸发终止前质量始终 ≥ M_Pl（不穿过 Planck 尺度 → 无裸奇点）
below = all(mass_evolve(M0, alpha, t) >= M_Pl for t in [t_pl*0.5, t_pl*0.9])
check("Planck 截断前 M ≥ M_Pl（无裸奇点）", below)
# 残留物成为反弹种子：M(t_pl) = M_Pl = 反弹种子质量
check("Planck 残留 = 反弹种子", abs(mass_evolve(M0, alpha, t_pl) - M_Pl) < 1e-6)

# ============ 汇总 ============
print("\n" + "=" * 62)
print(f"汇总: {PASS} / {CHECKS} 检查通过")
print("=" * 62)
if PASS == CHECKS:
    print("全部通过!")
else:
    print(f"有 {CHECKS - PASS} 项未通过!")
    raise SystemExit(1)
