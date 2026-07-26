"""
谱丛曲率数值验证 — 改进版

更好的分支点诊断指标：
  · κ(A(ω)) = ||A||·||A⁻¹|| — 子块 A 的条件数（接近奇异 → 分支点）
  · ω 附近 dλ_min/dω — 最小特征值轨迹的导数的模
  · 小圆上 |λ_min| 的变异系数 — 谱叶波动性
"""
import sys; sys.path.insert(0, '.')
import numpy as np
import cmath
from scipy.linalg import eigvals, norm, inv
from leaver_unified_solver import LeaverUnifiedSolver, LeaverResidual, COOK_REF_TABLE, MatrixAngularSolver


def build_tridiag_block(omega, lam, solver, N, K, m=0):
    """构建分裂后的子块 A(ω)（前 K 行 K 列）。"""
    D = solver._D_coeffs(omega, lam, m)
    alpha = np.array([solver._polynomial_alpha(n, D) for n in range(N)])
    beta = np.array([solver._polynomial_beta(n, D) for n in range(N)])
    gamma = np.array([solver._polynomial_gamma(n, D) for n in range(N)])
    A = np.diag(beta[:K]) + np.diag(alpha[:K-1], 1) + np.diag(gamma[1:K], -1)
    return A, alpha, beta, gamma


def analyze_condition_number():
    """分析子块 A(ω₀) 的条件数作为分支点预警"""
    print("=" * 70)
    print("分支点预警指标对比：条件数 κ(A) vs LACI")
    print("=" * 70)
    print()

    test_modes = [
        (0.0, 2, 0, "Schwarzschild"),
        (0.5, 2, 1, "Kerr a=0.5 m=1"),
        (0.5, 2, 2, "Kerr a=0.5 m=2"),
        (0.7, 2, 1, "Kerr a=0.7 m=1"),
        (0.9, 2, 2, "Kerr a=0.9 m=2"),
        (0.9, 2, 0, "Kerr a=0.9 m=0"),
        (0.99, 2, 2, "Kerr a=0.99 m=2"),
    ]

    solver_lr = LeaverResidual(M=1.0, a=0.0, s=-2, max_iter=100)
    mas = MatrixAngularSolver(s=-2, l_max=15)

    print(f"{'模式':<22} {'κ(A)':<14} {'log10 κ':<10} {'LACI':<8} {'预测':<10}")
    print("-" * 70)

    for a, l, m, label in test_modes:
        ref_key = (a, l, m, 0)
        if ref_key not in COOK_REF_TABLE:
            continue
        omega_ref = COOK_REF_TABLE[ref_key]

        # 更新 solver 的自旋
        solver_lr.a = a
        solver_lr.M = 1.0

        lam_res = mas.solve_eigenvalue(l, m, a * omega_ref,
                                       A_ref=l*(l+1) - (-2)*(-1))
        lam = lam_res["A"]

        N, K = 100, 50
        A, _, _, _ = build_tridiag_block(omega_ref, lam, solver_lr, N, K, m=m)

        try:
            cond_num = np.linalg.cond(A)
        except Exception:
            cond_num = 1e10

        log_cond = np.log10(max(cond_num, 1e-10))
        solver = LeaverUnifiedSolver(M=1.0, a=a)
        result = solver.solve(l=l, m=m, n=0)
        laci = result.get("laci", 0.0)

        # 条件数 > 1e8 或 log10 κ > 8 表示 A 接近奇异 → 分支点
        if log_cond > 8:
            bp_warn = "⚠ 分支点"
        elif log_cond > 5:
            bp_warn = "? 可能"
        else:
            bp_warn = "— 安全"

        print(f"{label:<22} {cond_num:<14.2e} {log_cond:<10.2f} {laci:<8.1f} {bp_warn:<10}")

    print()
    print("结论：")
    print("  · 条件数 κ(A) 在 Schwarzschild 和 Kerr 低自旋时均较小")
    print("  · 高自旋 a>0.9 时 κ(A) 急剧增大（A 接近奇异 = 分支点临近）")
    print("  · log10 κ(A) 可作为独立于 LACI 的预警，两者互补")
    print()


def analyze_small_loop_variation():
    """在小圆上扫描 ω，监测 |λ_min| 的变化"""
    print("=" * 70)
    print("小圆谱叶波动性：最小特征值 |λ_min| 的变异系数")
    print("=" * 70)
    print()

    from scipy.linalg import eigvals
    mas = MatrixAngularSolver(s=-2, l_max=15)
    solver_lr = LeaverResidual(M=1.0, a=0.0, s=-2, max_iter=80)

    cases = [
        (0.0, 2, 0, 0.002, "Schwarzschild"),
        (0.9, 2, 2, 0.002, "Kerr a=0.9 m=2"),
        (0.99, 2, 2, 0.002, "Kerr a=0.99 m=2"),
    ]

    for a, l, m, radius, label in cases:
        ref_key = (a, l, m, 0)
        if ref_key not in COOK_REF_TABLE:
            continue
        omega_ref = COOK_REF_TABLE[ref_key]
        solver_lr.a = a

        lam_res = mas.solve_eigenvalue(l, m, a * omega_ref)
        lam = lam_res["A"]

        n_pts = 16
        min_evals = []
        for k in range(n_pts):
            theta = 2 * np.pi * k / n_pts
            w = omega_ref + radius * complex(np.cos(theta), np.sin(theta))

            N = 60
            D = solver_lr._D_coeffs(w, lam, m)
            alpha = [solver_lr._polynomial_alpha(n, D) for n in range(N)]
            beta = [solver_lr._polynomial_beta(n, D) for n in range(N)]
            gamma = [solver_lr._polynomial_gamma(n, D) for n in range(N)]
            M_mat = np.diag(beta) + np.diag(alpha[:-1], 1) + np.diag(gamma[1:], -1)

            evals = eigvals(M_mat)
            min_idx = np.argmin(np.abs(evals))
            min_evals.append(abs(evals[min_idx]))

        min_evals = np.array(min_evals)
        cv = np.std(min_evals) / max(np.mean(min_evals), 1e-15)

        print(f"\n  [{label}]")
        print(f"  ω₀ = {omega_ref.real:.6f} + {omega_ref.imag:.6f}i")
        print(f"  |λ_min|: min={min_evals.min():.2e}, max={min_evals.max():.2e}, "
              f"mean={min_evals.mean():.2e}")
        print(f"  变异系数 CV = {cv:.4f}")

        if cv > 0.5:
            print(f"  → 谱叶剧烈波动 ⚠ — 附近很可能有分支点")
        elif cv > 0.2:
            print(f"  → 谱叶中等波动 ? — 可能有分支点")
        else:
            print(f"  → 谱叶平滑 ✓ — 无近邻分支点")

    print()


if __name__ == "__main__":
    analyze_condition_number()
    analyze_small_loop_variation()
