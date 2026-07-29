#!/usr/bin/env python3
"""
paperX_mass_delta_directionality.py — §5.7j 命题 J1-J2 数值验证（2026-07-29）

验证两个形式命题：
  J1（标量-算符分离）: Δ(A+δλ·P₀) − Δ(A) = δλ × (P₀·H − 2β·P₀·α' + H·P₀)
     — 严格线性，无高阶项，方向与 δλ 无关
  J2（模式间定位）: [A, δb]_ij = (λ_i − λ_j)·δb_ij ⇒ Δ 对角元恒为零

关联: paperX_source_defect.py (B1① 线性), paperX_delta_block_decomp.py (B4 J3 扇区分支撑)
"""

import numpy as np
from numpy import linalg as LA

rng = np.random.default_rng(20260729)
n = 8
N_TRIALS = 2000

# ---------- Cl(1,7) 谱算子 A_GR ----------
k = np.arange(1, n + 1)
lam = np.sqrt(k * (k + 1))
lam /= lam[-1]
A = np.diag(lam.astype(np.complex128))

def randH():
    X = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return (X + X.conj().T) / 2

def delta_op(A_mtx, beta, alpha):
    """Δ(A, β, α') = A·H − 2·β·A·α' + H·A,  H = β·α'"""
    H = beta @ alpha
    return A_mtx @ H - 2 * beta @ A_mtx @ alpha + H @ A_mtx


# =====================================================================
# S1: J1 标量-算符分离 — Δ(A+δλ·P₀) 严格线性于 δλ
# =====================================================================
print("=" * 74)
print("S1  命题 J1：标量-算符分离  δΔ = δλ × 方向（与 δλ 无关）")
print("=" * 74)

max_residual = 0.0
direction_std = np.zeros((n, n), dtype=np.complex128)
n_dlambda = 7
dlambda_vals = np.logspace(-6, 0, n_dlambda)

for trial in range(N_TRIALS):
    beta = randH(); beta /= LA.norm(beta, 'fro')
    alpha = randH(); alpha /= LA.norm(alpha, 'fro')
    P0 = randH(); P0 /= LA.norm(P0, 'fro')
    H = beta @ alpha

    # 计算不同 δλ 下的 Δ
    ref_direction = None
    residuals = []
    for dl in dlambda_vals:
        A_pert = A + dl * P0
        Delta_pert = delta_op(A_pert, beta, alpha)
        Delta_ref = delta_op(A, beta, alpha)
        dDelta = Delta_pert - Delta_ref
        # 提取方向 = dDelta / dl
        direction = dDelta / dl
        if ref_direction is None:
            ref_direction = direction.copy()
        else:
            residuals.append(LA.norm(direction - ref_direction, 'fro'))

    max_residual = max(max_residual, max(residuals))
    direction_std += ref_direction

direction_std /= N_TRIALS

print(f"\n  随机抽样: {N_TRIALS} 次 × {n_dlambda} 个 δλ 值（10⁻⁶ ~ 10⁰）")
print(f"  方向相对 Frobenius 残差 (max): {max_residual:.2e}")
print(f"  → J1 判定: {'✅ 严格线性（残差 = 浮点噪声 ÷ 最小 δλ）' if max_residual < 1e-9 else '❌ 有高阶项'}")
assert max_residual < 1e-9, f"方向不一致，残差 {max_residual:.2e}"

# 验证解析形式：方向 = P₀·H − 2β·P₀·α' + H·P₀
beta, alpha = randH() / LA.norm(randH(), 'fro'), randH() / LA.norm(randH(), 'fro')
P0 = randH(); P0 /= LA.norm(P0, 'fro')
H = beta @ alpha
direction_exact = P0 @ H - 2 * beta @ P0 @ alpha + H @ P0
direction_numerical = (delta_op(A + 1e-3 * P0, beta, alpha) - delta_op(A, beta, alpha)) / 1e-3
residual_exact = LA.norm(direction_numerical - direction_exact, 'fro')
print(f"\n  解析方向 vs 数值方向 (δλ=10⁻³) 残差: {residual_exact:.2e}")
print(f"  → J1 解析形式验证: {'✅ 一致' if residual_exact < 1e-13 else '❌ 不匹配'}")
assert residual_exact < 1e-13


# =====================================================================
# S2: J2 模式间定位 — [A, δb] 对角元恒为零
# =====================================================================
print("\n" + "=" * 74)
print("S2  命题 J2：模式间定位  [A, δb]_ij = (λ_i − λ_j)·δb_ij")
print("=" * 74)

diag_fracs = []
for _ in range(N_TRIALS):
    db = randH(); db = db / LA.norm(db, 'fro')
    comm = A @ db - db @ A  # [A, δb]
    diag_norm = np.sum(np.abs(np.diag(comm))**2)
    total_norm = LA.norm(comm, 'fro')**2
    diag_fracs.append(diag_norm / total_norm)

print(f"\n  [A, δb] 对角元占比: {np.mean(diag_fracs)*100:.2e}%（max: {np.max(diag_fracs)*100:.2e}%）")
print(f"  → J2 判定: {'✅ 对角元恒为零（代数恒等）' if np.mean(diag_fracs) < 1e-15 else '❌ 有对角残留'}")
assert np.mean(diag_fracs) < 1e-15


# =====================================================================
# S3: 标准化术语对照表
# =====================================================================
print("\n" + "=" * 74)
print("S3  标准化术语总结")
print("=" * 74)
print(r"""
  ┌─────────────────────┬───────────────────────────────────────┐
  │ 非正式表述           │ 标准化术语                            │
  ├─────────────────────┼───────────────────────────────────────┤
  │ 质量 = 标量幅度     │ 谱缺陷幅度 δλ (m = δλ·M_Pl)          │
  │                     │ J1 证明: δΔ 严格线性于 δλ             │
  ├─────────────────────┼───────────────────────────────────────┤
  │ Δ 给出方向          │ 偏差算符方向性                        │
  │                     │ 方向 = P₀·H−2β·P₀·α'+H·P₀ (与 δλ 无关)│
  ├─────────────────────┼───────────────────────────────────────┤
  │ Δ 不在时空内        │ 模式间定位                            │
  │                     │ J2 证明: [A,δb] 对角元 ≡ 0            │
  │                     │ Δ 完全在"模式间"分量                   │
  └─────────────────────┴───────────────────────────────────────┘
  J3（扇区间支撑 ~87%）详见 paperX_delta_block_decomp.py
""")

# =====================================================================
print(f"\n  全部检查: 2/2 通过")
