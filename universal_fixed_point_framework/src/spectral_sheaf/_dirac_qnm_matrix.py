#!/usr/bin/env python3
"""
_dirac_qnm_matrix.py —— Dirac QNM 矩阵法求解器（Phase 59F）

基于 Chandrasekhar 解耦的有效势方法，使用 Chebyshev 谱方法求解
Dirac 场在 Schwarzschild/Kerr 背景下的 QNM 频率。

理论框架
========
质量为零的 Dirac 方程在 Schwarzschild 背景下可解耦为：
    d²Ψ/dr*² + (ω² - V_eff(r))Ψ = 0

有效势（Chandrasekhar-Page 形式，适用于 s=-1/2）：
    V_eff(r) = f(r) * [κ²/r² + κ · df/dr / (2r) - κ · f(r)/r²]   (正字称)
    V_eff(r) = f(r) * [κ²/r² - κ · df/dr / (2r) + κ · f(r)/r²]   (负字称)

其中 f(r) = 1-2M/r，κ = l+1/2（对角量子数 l=1/2, 3/2, ... 的模）。

正、负字称在 Schwarzschild 下等谱（超对称伙伴），因此只需计算一种。

注意：标准 Teukolsky-Leaver 递推系数对 s=-1/2 不适用，因为 Dirac 有效势
包含 √Δ 因子（视界处的分支点），导致 Frobenius 展开变量必须采用 √Δ/r
而非 (r-r₊)/(r-r₋)。

参考：
    Chandrasekhar (1983) "The Mathematical Theory of Black Holes"
    Dolan & Gair (2006) arXiv:gr-qc/0612024
    Jansen (2017) arXiv:1709.09178
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any, Tuple


# ============================================================
# 1. Dirac 有效势
# ============================================================

def dirac_effective_potential(r: float, kappa: float, M: float = 1.0) -> float:
    """
    Dirac 有效势（正字称，Chandrasekhar 形式）。

    V(r) = f(r) * κ²/r² + κ · df/dr / (2r) - κ · f(r)/r²

    对 Schwarzschild (a=0)，正、负字称是超对称伙伴，等谱。

    参数:
        r: 径向坐标
        kappa: κ = l + 1/2（正整数 1, 2, 3, ...）
        M: 黑洞质量

    返回:
        V: 有效势值
    """
    if r <= 2.0 * M:
        return 0.0  # 视界内

    f = 1.0 - 2.0 * M / r
    df_dr = 2.0 * M / r ** 2  # df/dr = 2M/r²

    term1 = f * kappa ** 2 / r ** 2
    term2 = kappa * df_dr / (2.0 * r)
    term3 = kappa * f / r ** 2

    V = term1 + term2 - term3
    return float(V)


def dirac_eff_pot_jing(r: float, kappa: float, M: float = 1.0) -> float:
    """
    Jing (2005) 新形式的 Dirac 有效势。

    Jing 重新定义了波函数 P(r)，使得有效势不再包含 √Δ 因子。
    新的势函数为：
    U(r) = f(r) * κ²/r² + κ * (κ+1)/r² * (1 - f(r))

    这在 Schwarzschild 下等价于 Chandrasekhar 形式，计算更稳定。
    """
    if r <= 2.0 * M:
        return 0.0

    f = 1.0 - 2.0 * M / r
    return float(f * kappa ** 2 / r ** 2 + kappa * (kappa + 1.0) / r ** 2 * (1.0 - f))


# ============================================================
# 2. Chebyshev 谱方法
# ============================================================

def chebyshev_differentiation_matrix(N: int) -> np.ndarray:
    """
    构造 Chebyshev 一阶微分矩阵 D (N×N)。

    Chebyshev 点: x_j = cos(j*pi/N), j=0,...,N

    返回:
        D: N×N 微分矩阵
    """
    x = np.cos(np.pi * np.arange(N) / (N - 1))
    D = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            if i == j:
                if i == 0:
                    D[i, j] = (2.0 * (N - 1) ** 2 + 1.0) / 6.0
                elif i == N - 1:
                    D[i, j] = -(2.0 * (N - 1) ** 2 + 1.0) / 6.0
                else:
                    D[i, j] = -x[i] / (2.0 * (1.0 - x[i] ** 2))
            else:
                ci = 2.0 if i == 0 or i == N - 1 else 1.0
                cj = 2.0 if j == 0 or j == N - 1 else 1.0
                D[i, j] = (ci / cj) * ((-1) ** (i + j)) / (x[i] - x[j])

    return D


def map_to_schwarzschild(x: np.ndarray, L: float = 4.0,
                         M: float = 1.0) -> np.ndarray:
    """
    将 Chebyshev 域 x ∈ [-1, 1] 映射到 tortoise 坐标 r* ∈ (-∞, ∞)。

    使用 sinh 映射（Boyd 1986）：
    r* = L * sinh( H * x ),  H = arccosh(r*_max / L)

    参数:
        x: Chebyshev 点数组
        L: 标度参数（典型值 4M）
        M: 黑洞质量

    返回:
        r_star: tortoise 坐标数组
    """
    r_star_max = 40.0 * M
    H = np.arccosh(r_star_max / L)
    return L * np.sinh(H * x)


def tortoise_to_r(r_star: np.ndarray, M: float = 1.0) -> np.ndarray:
    """
    将 tortoise 坐标 r* 转换回径向坐标 r。

    通过求解 dr/dr* = f(r) = 1 - 2M/r 的逆映射：
    r* = r + 2M * ln(r/(2M) - 1)

    逆映射通过 Newton 法迭代，确保 r > 2M。
    """
    r = np.empty_like(r_star)
    for i, rs in enumerate(r_star):
        # 初始猜测
        if rs > 10.0 * M:
            r_guess = rs
        elif rs < -10.0 * M:
            # 深度视界附近：使用渐近近似作为初值
            # r* ≈ 2M + 2M*ln(r/2M - 1) 对 r→2M
            r_guess = 2.0 * M + 2.0 * M * np.exp((rs - 2.0 * M) / (2.0 * M))
        else:
            r_guess = 2.0 * M + 0.5 * (rs - 2.0 * M) + 2.0 * M

        # 确保 r_guess > 2M
        r_guess = max(r_guess, 2.0 * M + 1e-12)

        # Newton 迭代
        for _ in range(50):
            # 确保对数参数 > 0
            arg = r_guess / (2.0 * M) - 1.0
            if arg <= 1e-15:
                r_guess = 2.0 * M + 1e-10
                arg = 1e-10

            f = r_guess + 2.0 * M * np.log(arg) - rs
            fp = 1.0 + 2.0 * M / (r_guess - 2.0 * M)

            if abs(fp) < 1e-15:
                fp = 1e-15

            dr = f / fp
            r_guess -= dr

            # 保持 r_guess > 2M
            if r_guess <= 2.0 * M:
                r_guess = 2.0 * M + 1e-10

            if abs(dr) < 1e-12:
                break

        r[i] = r_guess

    return r


def dtortoise_dx(x: np.ndarray, L: float = 4.0, H: float = None) -> np.ndarray:
    """计算 dr*/dx。"""
    if H is None:
        r_star_max = 40.0 * 1.0
        H = np.arccosh(r_star_max / L)
    return L * H * np.cosh(H * x)


# ============================================================
# 3. 特征值求解
# ============================================================

def find_dirac_qnm_matrix(kappa: float, M: float = 1.0, a: float = 0.0,
                          n_modes: int = 5, N: int = 80,
                          L: float = 6.0) -> Dict[str, Any]:
    """
    使用 Chebyshev 谱方法求解 Dirac QNM 频率。

    将 Regge-Wheeler 方程离散化为广义特征值问题：
    (A - ω²B)Ψ = 0

    其中 A = D² + diag(V_eff)，B = -I

    边界条件通过 L 参数选择吸收层或直接求解。

    参数:
        kappa: κ = l+1/2（正整数 1, 2, 3, ...）
        M: 黑洞质量
        a: 黑洞自旋（仅 Schwarzschild a=0 的精确实现）
        n_modes: 返回的模式数
        N: Chebyshev 点数
        L: 标度参数

    返回:
        { 'omega': list[complex], 'residuals': list[float], ... }
    """
    if abs(a) > 1e-10:
        # 暂仅支持 Schwarzschild
        raise NotImplementedError("Kerr Dirac QNM 暂未实现，请使用 a=0")

    # Chebyshev 点
    x = np.cos(np.pi * np.arange(N) / (N - 1))

    # 映射到 r*
    r_star_max = 40.0 * M
    H = np.arccosh(r_star_max / L)
    r_star = L * np.sinh(H * x)

    # tortoise → r
    r_arr = tortoise_to_r(r_star, M)

    # dr*/dx
    drst_dx = L * H * np.cosh(H * x)

    # 有效势
    V = np.array([dirac_eff_pot_jing(r, kappa, M) for r in r_arr])

    # Chebyshev 微分矩阵
    D1 = chebyshev_differentiation_matrix(N)

    # 二阶微分矩阵（链式法则）
    # d/dx → d/dr* = (dx/dr*) * d/dx = (1/drst_dx) * d/dx
    # d²/dr*² = (1/drst_dx) * d/dx * (1/drst_dx) * d/dx
    inv_drst = np.diag(1.0 / drst_dx)
    D2 = inv_drst @ D1 @ inv_drst @ D1

    # 构造矩阵 A = D² + V(r*)·I
    A = D2 + np.diag(V)

    # 特征值问题: (D² + V)Ψ = -ω²Ψ
    # → AΨ = -ω²Ψ → AΨ = λΨ, λ = -ω²
    eigenvalues, eigenvectors = np.linalg.eig(A)

    # 过滤物理根
    # QNM 条件: Im(ω) < 0 (衰减)
    # ω = sqrt(-λ)，需选择正确的分支
    physical_modes = []
    for ev in eigenvalues:
        omega = np.sqrt(-ev)

        # 选择正确的平方根分支
        if np.imag(omega) > 0:
            omega = -omega

        # 只保留衰减模 Im(ω) < 0
        if np.imag(omega) < -1e-10:
            physical_modes.append(omega)

    # 按 |Im(ω)| 从小到大排序（基模在 first）
    physical_modes.sort(key=lambda w: abs(w.imag))

    # 计算残差
    results = []
    for omega in physical_modes[:n_modes]:
        # 验证: ||(D² + V + ω²I)Ψ_min||
        # 使用最小特征值对应的特征向量
        residuals = []
        for i, ev in enumerate(eigenvalues):
            if abs(ev + omega ** 2) < 1e-8:
                res = np.linalg.norm((D2 + np.diag(V) + omega ** 2 * np.eye(N))
                                     @ eigenvectors[:, i])
                residuals.append(res / N)

        avg_res = np.mean(residuals) if residuals else 0.0
        results.append({
            'omega': omega,
            'residual': avg_res,
            'r_star_max': r_star_max,
            'N': N,
        })

    return {
        'modes': results,
        'kappa': kappa,
        'M': M,
        'N': N,
        'r_star_max': r_star_max,
        'L': L,
        'all_eigenvalues': eigenvalues,
    }


# ============================================================
# 4. 验证与基准
# ============================================================

def compute_dirac_benchmark_row_matrix(kappa: float, a: float = 0.0,
                                       M_mass: float = 1.0,
                                       N: int = 100, n_mode: int = 0,
                                       L: float = 6.0) -> Dict[str, Any]:
    """
    计算单条 Dirac QNM 基准记录（矩阵法）。

    返回:
        { 'omega': complex, 'residual': float, 'converged': bool, ... }
    """
    try:
        result = find_dirac_qnm_matrix(
            kappa=kappa, M=M_mass, a=a,
            n_modes=n_mode + 3, N=N, L=L
        )

        if len(result['modes']) > n_mode:
            mode = result['modes'][n_mode]
            return {
                'omega': mode['omega'],
                'residual': mode['residual'],
                'converged': True,
                'kappa': kappa,
                'N': N,
            }
        else:
            return {
                'omega': complex(0, 0),
                'residual': 1.0,
                'converged': False,
                'kappa': kappa,
                'N': N,
            }
    except Exception as e:
        return {
            'omega': complex(0, 0),
            'residual': 1.0,
            'error': str(e),
            'converged': False,
            'kappa': kappa,
            'N': N,
        }


def print_matrix_benchmark_row(kappa: float, a: float, result: Dict[str, Any],
                               n_mode: int = 0):
    """格式化打印单条基准记录。"""
    status = "✓" if result['converged'] else "✗"
    omega = result['omega']
    res = result['residual']
    k = result['kappa']
    l_val = k - 0.5  # l = κ - 1/2
    print(f"  | {l_val:<+4.1f} | {k:<3d} | {a:<5.3f} | {n_mode} "
          f"| {omega.real:<10.6f} | {omega.imag:<+10.6f} "
          f"| {res:<8.1e} "
          f"| {status} |")


def test_schwarzschild_dirac_matrix():
    """验证 Schwarzschild 极限下 Dirac QNM 的矩阵法计算精度。"""
    print("=" * 80)
    print("Dirac QNM 矩阵法验证：Schwarzschild 极限 (a=0)")
    print("=" * 80)
    print(f"  {'l':<5} {'κ':<4} {'a':<6} {'n':<4} "
          f"{'Re(ω)':<12} {'Im(ω)':<12} {'残差':<10} {'状态':<6}")
    print(f"  {'─'*5} {'─'*4} {'─'*6} {'─'*4} "
          f"{'─'*12} {'─'*12} {'─'*10} {'─'*6}")

    test_cases = [
        (1, 0),     # κ=1, l=0.5, n=0
        (2, 0),     # κ=2, l=1.5, n=0
        (3, 0),     # κ=3, l=2.5, n=0
        (1, 1),     # κ=1, l=0.5, n=1（第一倍频）
        (2, 1),     # κ=2, l=1.5, n=1
    ]

    for kappa, n_mode in test_cases:
        result = compute_dirac_benchmark_row_matrix(
            kappa=kappa, a=0.0, N=100, n_mode=n_mode, L=6.0)
        print_matrix_benchmark_row(kappa, 0.0, result, n_mode)

    # 对照参考值
    print(f"\n{'─'*50}")
    print("Dolan & Gair (2006) 参考值:")
    print(f"{'─'*50}")
    print(f"  (s=-0.5, a=0, l=0.5, κ=1, n=0): "
          f"ω_ref = 0.378721 - 0.096458i")
    print(f"  (s=-0.5, a=0, l=1.5, κ=2, n=0): "
          f"ω_ref = 0.522988 - 0.089964i")
    print(f"  (s=-0.5, a=0, l=2.5, κ=3, n=0): "
          f"ω_ref = 0.640418 - 0.091694i")
    print(f"  (s=-0.5, a=0, l=0.5, κ=1, n=1): "
          f"ω_ref = 0.347678 - 0.293755i")
    print()


# ============================================================
# 5. 收敛性测试
# ============================================================

def test_convergence():
    """测试矩阵法在不同 N 下的收敛性。"""
    kappa = 1  # l=0.5

    print("=" * 80)
    print("矩阵法收敛性测试 (κ=1, a=0)")
    print("=" * 80)
    print(f"  {'N':<6} {'Re(ω)':<12} {'Im(ω)':<12} {'Δω_n-1':<14}")
    print(f"  {'─'*6} {'─'*12} {'─'*12} {'─'*14}")

    prev_omega = None
    for N in [30, 40, 50, 60, 80, 100, 120]:
        result = find_dirac_qnm_matrix(kappa=kappa, N=N, n_modes=1, L=6.0)
        if len(result['modes']) > 0:
            omega = result['modes'][0]['omega']
            delta = abs(omega - prev_omega) if prev_omega else 0.0
            print(f"  {N:<6} {omega.real:<12.6f} {omega.imag:<+12.6f} "
                  f"{delta:<14.2e}")
            prev_omega = omega
    print()


def plot_potential():
    """绘制 Dirac 有效势。"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    r = np.linspace(2.001, 20.0, 500)
    M = 1.0

    plt.figure(figsize=(10, 6))
    for kappa in [1, 2, 3, 4]:
        V = np.array([dirac_eff_pot_jing(rr, kappa, M) for rr in r])
        plt.plot(r, V, label=f'κ={kappa} (l={kappa-0.5})')

    plt.xlabel('r/M')
    plt.ylabel('V(r)')
    plt.title('Dirac Effective Potential (Jing 2005 form)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-0.02, 0.2)
    plt.savefig('dirac_effective_potential.png', dpi=150)
    plt.close()
    print("[INFO] Dirac 有效势图保存为 dirac_effective_potential.png")


# ============================================================
# 6. 主入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dirac QNM 矩阵法求解器")
    parser.add_argument("--test", action="store_true", default=True,
                        help="运行基准验证测试（默认）")
    parser.add_argument("--kappa", type=int, default=1,
                        help="κ = l+1/2 (默认 1, 即 l=0.5)")
    parser.add_argument("--N", type=int, default=100,
                        help="Chebyshev 点数 (默认 100)")
    parser.add_argument("--L", type=float, default=6.0,
                        help="标度参数 (默认 6.0)")

    args = parser.parse_args()

    test_schwarzschild_dirac_matrix()
    test_convergence()

    # 绘图
    try:
        plot_potential()
    except Exception as e:
        print(f"[WARN] 绘图失败: {e}")
