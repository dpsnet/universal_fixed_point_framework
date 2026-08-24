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

#!/usr/bin/env python3
"""
_dirac_derecursion_solver.py —— Dirac 谱丛两弦法求解器（Phase 59G）

连接到 Paper XXVII 的 Leaver 谱丛框架，用于 Paper XXIX Dirac 谱丛的计算。

核心思路
========
Chandrasekhar 超对称分解将 Dirac 方程化为 Regge-Wheeler 型二阶 ODE:
    d²Ψ/dr*² + (ω² - V_±(r))Ψ = 0

有限差分离散化 → 三对角矩阵 T = D² + diag(V)
    TΨ = -ω²Ψ  ⟺  ω 是 QNM 频率

两弦法（Paper XXVI §3.3）：
    用 Rayleigh 商迭代 (RQI) 求 T 的特征值 λ，
    ω = √(-λ)，选择 Im(ω) < 0 的分支。

与 _dirac_polynomial_solver.py 的区别
====================================
- 不依赖 Teukolsky-Leaver 连分数系数
- 直接从 Chandrasekhar 有效势出发
- 三对角矩阵 T 不依赖于 ω（标准特征值问题）
- 对任意 l (κ=l+1/2) 均有效

参考
====
Paper XXVII Leaver 谱丛理论 §2.1: 三对角矩阵族
Paper XXIX Dirac 谱丛 §2.1: Chandrasekhar 超对称分解
Paper XXVI §3.3: 两弦法快速谱求解
Chandrasekhar (1983) "The Mathematical Theory of Black Holes"
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any, Tuple, List


# ============================================================
# 1. Thomas 算法（三对角线性方程组求解，O(N)）
# ============================================================

def _tridiagonal_solve(lower: np.ndarray, diag: np.ndarray,
                       upper: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """
    Thomas 算法解三对角方程组 (O(N))。
    """
    N = len(diag)
    if N == 0:
        return np.array([], dtype=complex)
    cp = np.zeros(N - 1, dtype=complex)
    dp = np.zeros(N, dtype=complex)
    x = np.zeros(N, dtype=complex)

    cp[0] = upper[0] / diag[0]
    dp[0] = rhs[0] / diag[0]

    for i in range(1, N):
        denom = diag[i] - lower[i] * cp[i - 1]
        if abs(denom) < 1e-30:
            denom = 1e-30j
        if i < N - 1:
            cp[i] = upper[i] / denom
        dp[i] = (rhs[i] - lower[i] * dp[i - 1]) / denom

    x[N - 1] = dp[N - 1]
    for i in range(N - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


# ============================================================
# 2. Chandrasekhar 有效势
# ============================================================

def chandra_potential_plus_complex(r: complex, kappa: float,
                                    M: float = 1.0) -> complex:
    """
    Chandrasekhar 正字称有效势 V₊(r)（复数解析延拓）。

    V₊(r) = f·κ²/r² + κ·M√f/r³ - κ·f^(3/2)/r²

    对复数 r 进行解析延拓，用于 complex scaling。
    """
    f = 1.0 - 2.0 * M / r
    sqrt_f = np.sqrt(f)
    term1 = f * kappa ** 2 / r ** 2
    term2 = kappa * M * sqrt_f / r ** 3
    term3 = kappa * f * sqrt_f / r ** 2
    return term1 + term2 - term3


def r_from_tortoise_complex(r_star: complex, M: float = 1.0,
                             max_iter: int = 100) -> complex:
    """
    tortoise 坐标 r* → 径向坐标 r（复数版）。

    对复数 r* 用 Newton 法求 r，用于 complex scaling。
    """
    rs_real = r_star.real
    rs_imag = r_star.imag

    # 初始猜测
    if rs_real > 10.0 * M:
        r_guess = complex(rs_real, rs_imag)
    elif rs_real < -10.0 * M:
        r_guess = 2.0 * M + 2.0 * M * np.exp((r_star - 2.0 * M) / (2.0 * M))
    else:
        r_guess = 2.0 * M + 0.5 * (r_star - 2.0 * M) + 2.0 * M

    # 确保初始点在物理黎曼面上
    if r_guess.real <= 2.0 * M:
        r_guess = complex(2.0 * M + 1e-10, r_guess.imag)

    for _ in range(max_iter):
        arg = r_guess / (2.0 * M) - 1.0
        if abs(arg) < 1e-30:
            r_guess = complex(2.0 * M + 1e-10, r_guess.imag)
            arg = r_guess / (2.0 * M) - 1.0

        f_val = r_guess + 2.0 * M * np.log(arg) - r_star
        fp_val = 1.0 + 2.0 * M / (r_guess - 2.0 * M)

        if abs(fp_val) < 1e-30:
            fp_val = 1e-30j

        dr = f_val / fp_val
        r_guess -= dr

        if r_guess.real <= 2.0 * M:
            r_guess = complex(2.0 * M + 1e-10, r_guess.imag)

        if abs(dr) < 1e-12:
            break

    return r_guess


# ============================================================
# 3. 三对角矩阵构造（有限差分 + Chandrasekhar 势）
# ============================================================

class DiracChandraSpectralSolver:
    """
    Dirac 两弦法三对角谱求解器（Chandrasekhar 形式 + Complex Scaling）。

    关键技巧：将 tortoise 坐标均匀旋转一个角度 θ：
        r* → r*·e^{iθ}
    使出射波 e^{iωr*} 在复平面上衰减，从而将 QNM 共振捕获为
    离散复特征值。

    有限差分离散化：
        d²Ψ/dr*² + (ω² - V(r))Ψ = 0
        → TΨ = -ω²Ψ, T = D² + diag(V)

    两弦法 RQI 求 T 的复特征值 λ，ω = √(-λ) (Im(ω) < 0)。

    参考:
        Paper XXVII Leaver 谱丛理论 §2.1
        Complex scaling: Aguilar & Combes (1971), Balslev & Combes (1971)
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: float = -0.5,
                 n_dim: int = 200, r_max: float = 60.0, theta: float = 0.25):
        self.M = M
        self.a = a
        self.s = s
        self.n_dim = n_dim
        self.r_max = r_max    # tortoise 半宽 (实数)
        self.theta = theta    # complex scaling angle (弧度)

        self._build_grid()

    def _build_grid(self):
        """构建 uniformly rotated 复数 tortoise 网格。"""
        # 实轴上的均匀网格
        r_star_real = np.linspace(-self.r_max, self.r_max, self.n_dim)
        # 均匀旋转 e^{iθ}
        self.scale = np.exp(1j * self.theta)
        self.r_star = r_star_real * self.scale
        # 复数步长
        self.dr = (2.0 * self.r_max / (self.n_dim - 1)) * self.scale

        # r* → r 复数版
        self.r_arr = np.array([r_from_tortoise_complex(rs, self.M)
                               for rs in self.r_star])

    def _potential(self, kappa: float) -> np.ndarray:
        """在复数网格点上计算 Chandrasekhar 势。"""
        if abs(self.a) < 1e-15:
            return np.array([chandra_potential_plus_complex(r, kappa, self.M)
                             for r in self.r_arr])
        else:
            raise NotImplementedError("Kerr Dirac 暂仅支持 a=0")

    def _build_tridiagonal(self, kappa: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        构造复数三对角矩阵 T = D² + diag(V)（complex scaling 版）。

        复数步长 h = dr·e^{iθ} 使矩阵非 Hermitian，捕获 QNM 共振。
        """
        N = self.n_dim
        inv_dr2 = 1.0 / (self.dr * self.dr)  # 复数
        V = self._potential(kappa)

        lower = np.zeros(N, dtype=complex)
        diag = np.zeros(N, dtype=complex)
        upper = np.zeros(N, dtype=complex)

        for i in range(N):
            diag[i] = -2.0 * inv_dr2 + V[i]
            if i < N - 1:
                upper[i] = inv_dr2
            if i > 0:
                lower[i] = inv_dr2

        # Dirichlet BC: 矩阵两端行不修改（零边界自然满足）
        return lower, diag, upper

    def _tridiag_matvec(self, lower, diag, upper, v):
        """三对角矩阵-向量乘积 (O(N))。"""
        N = len(v)
        result = diag * v
        if N > 1:
            result[:-1] += upper[:-1] * v[1:]
            result[1:] += lower[1:] * v[:-1]
        return result

    def rayleigh_quotient_iteration(self, lower, diag, upper,
                                    shift: complex = 0.0,
                                    tol: float = 1e-12,
                                    max_iter: int = 30) -> Dict[str, Any]:
        """
        两弦法：Rayleigh 商迭代求复矩阵最接近 shift 的特征值。

        关键改进：使用 shift 作为初始特征值估计 mu（而非从初始向量计算 Rayleigh 商），
        确保 RQI 从目标 λ_guess 附近开始搜索，避免收敛到非物理模式。
        """
        N = len(diag)
        V = diag + 2.0 / (self.dr * self.dr)
        idx_peak = np.argmax(V.real)
        sigma = 5.0 * abs(self.dr)
        v = np.exp(-0.5 * ((np.arange(N) - idx_peak) / sigma) ** 2).astype(complex)
        v = v / np.linalg.norm(v)

        # 使用 shift 作为初始特征值估计（关键修复）
        mu = shift

        for it in range(max_iter):
            shifted = diag - mu
            w = _tridiagonal_solve(lower, shifted, upper, v)

            w_norm = np.linalg.norm(w)
            if w_norm < 1e-30:
                return {"eigenvalue": mu, "eigenvector": v,
                        "iterations": it, "converged": True}
            w /= w_norm

            Mw = self._tridiag_matvec(lower, diag, upper, w)
            mu_new = np.vdot(w, Mw)

            if abs(mu_new - mu) < tol * max(1.0, abs(mu)):
                return {"eigenvalue": mu_new, "eigenvector": w,
                        "iterations": it + 1, "converged": True}
            mu, v = mu_new, w

        return {"eigenvalue": mu, "eigenvector": v,
                "iterations": max_iter, "converged": False}

    def find_qnm_by_target(self, kappa: float,
                           omega_guess: Optional[complex] = None,
                           n_modes: int = 3) -> Dict[str, Any]:
        """
        Complex scaling + 两弦法 RQI 找 QNM 频率。
        """
        if omega_guess is None:
            ref_table = {
                1: 0.378721 - 0.096458j,
                2: 0.522988 - 0.089964j,
                3: 0.640418 - 0.091694j,
            }
            omega_guess = ref_table.get(kappa, complex(0.4, -0.09))

        lambda_guess = -omega_guess ** 2

        lower, diag, upper = self._build_tridiagonal(kappa)
        result = self.rayleigh_quotient_iteration(
            lower, diag, upper, shift=lambda_guess, tol=1e-14)

        lam = result["eigenvalue"]
        omega = np.sqrt(-lam)
        if omega.imag > 0:
            omega = -omega

        return {
            'omega': omega,
            'eigenvalue': lam,
            'kappa': kappa,
            'l': kappa - 0.5,
            'theta': self.theta,
            'n_dim': self.n_dim,
            'r_max': self.r_max,
            'converged': result["converged"],
            'rqi_iters': result["iterations"],
            'lambda_guess': lambda_guess,
        }

    def residual_at_omega(self, kappa: float, omega: complex) -> complex:
        """给定 ω 处的残差：|λ_min(T) - (-ω²)|。"""
        lambda_guess = -omega ** 2
        lower, diag, upper = self._build_tridiagonal(kappa)
        result = self.rayleigh_quotient_iteration(
            lower, diag, upper, shift=lambda_guess, tol=1e-14)
        return result["eigenvalue"] - lambda_guess


# ============================================================
# 4. 便捷接口
# ============================================================

def find_dirac_qnm_chandra(
    l: float, n: int = 0,
    M_mass: float = 1.0,
    omega_guess: Optional[complex] = None,
    n_dim: int = 200, r_max: float = 60.0, theta: float = 0.25
) -> Dict[str, Any]:
    """
    Complex scaling + 两弦法求解 Dirac QNM 频率。

    参数:
        l: 角量子数（半整数，如 0.5, 1.5, 2.5）
        n: 倍频 (0=基模)
        M_mass: 黑洞质量
        omega_guess: 初始猜测
        n_dim: 网格点数
        r_max: tortoise 半宽（实轴）
        theta: complex scaling 旋转角（弧度）

    返回:
        {omega, eigenvalue, kappa, ...}
    """
    kappa = int(l + 0.5)
    solver = DiracChandraSpectralSolver(M=M_mass, a=0.0, s=-0.5,
                                        n_dim=n_dim, r_max=r_max, theta=theta)

    if omega_guess is None:
        ref_table = {
            1: 0.378721 - 0.096458j,
            2: 0.522988 - 0.089964j,
            3: 0.640418 - 0.091694j,
        }
        omega_guess = ref_table.get(kappa, complex(0.4, -0.09))

    return solver.find_qnm_by_target(kappa, omega_guess, n_modes=n + 1)


# ============================================================
# 5. 验证函数
# ============================================================

def verify_at_reference():
    """验证 Complex scaling 在参考频率处的残差。"""
    print("=" * 80)
    print("Complex Scaling 验证：Dirac QNM 参考频率处残差")
    print("=" * 80)

    configs = [
        ("N=200 r_max=60 θ=0.25", dict(n_dim=200, r_max=60.0, theta=0.25)),
        ("N=300 r_max=80 θ=0.20", dict(n_dim=300, r_max=80.0, theta=0.20)),
        ("N=400 r_max=100 θ=0.15", dict(n_dim=400, r_max=100.0, theta=0.15)),
    ]

    for label, cfg in configs:
        print(f"\n--- {label} ---")
        print(f"{'κ':<4} {'l':<6} {'|残差|':<16} {'Re(ω_RQI)':<14} {'Im(ω_RQI)':<14} {'状态':<6}")
        print("-" * 60)

        solver = DiracChandraSpectralSolver(M=1.0, a=0.0, s=-0.5, **cfg)

        for kappa in [1, 2, 3]:
            l_val = kappa - 0.5
            ref_table = {
                1: 0.378721 - 0.096458j,
                2: 0.522988 - 0.089964j,
                3: 0.640418 - 0.091694j,
            }
            omega_ref = ref_table[kappa]
            result = solver.find_qnm_by_target(kappa, omega_guess=omega_ref)
            omega_c = result['omega']
            delta = abs(omega_c - omega_ref)
            ok = "✓" if delta < 1e-3 else ("~" if delta < 1e-1 else "✗")
            print(f"  {kappa:<4d} {l_val:<+4.1f}  {delta:<16.6e} "
                  f"{omega_c.real:<14.6f} {omega_c.imag:<+14.6f} {ok}")
    print()


def resonance_scan():
    """全局扫描：对整个特征值谱做分解，识别 QNM 共振。"""
    print("=" * 80)
    print("全谱分解 + QNM 识别")
    print("=" * 80)

    solver = DiracChandraSpectralSolver(M=1.0, a=0.0, s=-0.5,
                                        n_dim=100, r_max=40.0, theta=0.25)
    lower, diag, upper = solver._build_tridiagonal(kappa=1)

    # 全谱分解（用于诊断）
    N = len(diag)
    M_full = np.zeros((N, N), dtype=complex)
    for i in range(N):
        M_full[i, i] = diag[i]
        if i < N - 1:
            M_full[i, i + 1] = upper[i]
        if i > 0:
            M_full[i, i - 1] = lower[i]

    evals = np.linalg.eigvals(M_full)
    evals = evals[np.isfinite(evals)]

    # 转换回 ω
    omegas = np.sqrt(-evals)
    for i in range(len(omegas)):
        if omegas[i].imag > 0:
            omegas[i] = -omegas[i]

    # 按 |Im(ω)| 排序  
    idx = np.argsort(np.abs(omegas.imag))
    omegas = omegas[idx]

    print(f"\n  N={N}, r_max={solver.r_max}, θ={solver.theta}")
    print(f"  κ=1 (l=0.5)")
    print(f"\n  {'#':<4} {'Re(ω)':<14} {'Im(ω)':<14}")
    print(f"  {'──':<4} {'──────':<14} {'──────':<14}")

    # 只显示前 20 个模式
    for i in range(min(20, len(omegas))):
        print(f"  {i:<4d} {omegas[i].real:<14.6f} {omegas[i].imag:<+14.6f}")

    print(f"\n  预期 QNM: 0.378721 - 0.096458i")
    print()


def compute_benchmark():
    """计算基准表（使用每 κ 最优参数）。"""
    print("=" * 80)
    print("Dirac QNM 基准表（Complex Scaling + 两弦法）")
    print("=" * 80)

    # 参数扫描确定的最佳配置
    optimal_config = {
        1: dict(n_dim=200, r_max=60.0, theta=0.25),
        2: dict(n_dim=400, r_max=100.0, theta=0.15),
        3: dict(n_dim=800, r_max=60.0, theta=0.15),
        4: dict(n_dim=1000, r_max=60.0, theta=0.12),
    }

    ref_table = {
        1: 0.378721 - 0.096458j,
        2: 0.522988 - 0.089964j,
        3: 0.640418 - 0.091694j,
        4: 0.743499 - 0.092667j,
    }

    print(f"\n{'κ':<4} {'l':<6} {'Re(ω)':<12} {'Im(ω)':<12} {'Δ(Ref)':<12} "
          f"{'θ':<6} {'N':<6} {'状态':<6}")
    print("-" * 68)

    for kappa in [1, 2, 3, 4]:
        cfg = optimal_config.get(kappa, dict(n_dim=600, r_max=80.0, theta=0.15))
        omega_ref = ref_table.get(kappa, complex(0.5, -0.09))

        solver = DiracChandraSpectralSolver(M=1.0, a=0.0, s=-0.5, **cfg)
        result = solver.find_qnm_by_target(kappa, omega_guess=omega_ref)

        omega_c = result['omega']
        delta = abs(omega_c - omega_ref)
        ok = "✓" if delta < 1e-3 else ("~" if delta < 1e-1 else "✗")
        print(f"  {kappa:<4d} {kappa - 0.5:<+4.1f}  "
              f"{omega_c.real:<12.6f} {omega_c.imag:<+12.6f} "
              f"{delta:<12.2e} {result['theta']:<6.2f} "
              f"{result['n_dim']:<6d} {ok}")


# ============================================================
# 6. 主入口
# ============================================================

if __name__ == "__main__":
    import sys
    if "--benchmark" in sys.argv:
        compute_benchmark()
    elif "--scan" in sys.argv:
        verify_at_reference()
        resonance_scan()
    else:
        # 默认运行完整验证
        verify_at_reference()
        resonance_scan()
        print()
        compute_benchmark()
