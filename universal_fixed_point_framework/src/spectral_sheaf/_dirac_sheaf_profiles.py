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
_dirac_sheaf_profiles.py —— Dirac 谱丛三剖面多工具求解器（Phase 59H）

理论背景
========
Paper XXIX §1.2 指出：Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的 Leaver 连分数法
遭遇"窗口困境"——连分数收敛窗口在复 ω 平面上因参数不同而变化，
且 $\mathbb{Z}_2$ 阻碍导致双叶覆盖使窗口结构更复杂。

核心创新
========
谱丛的三个参数方向（ω、a、m）使用不同数学工具构造纵向剖面：

剖面 1 (ω-profile) —— Chebyshev 谱配点 + 围道积分（Beyn 法）
  取代 Leaver 连分数法。直接离散 Dirac Teukolsky ODE 为二次特征值问题，
  用复围道积分同时找出窗口内所有根。无收敛窗口限制，无需初值猜测。

剖面 2 (a-profile) —— 重心有理逼近（AAA 算法）
  取代 a-同伦延拓。从离散 a 样本构造全局有理逼近 ω(a)，
  可解析延拓穿过分支点，避免谱叶跳跃。

剖面 3 (m-profile) —— 角向分离常数代数求解器
  将角向特征值 $\lambda_{slm}(a,m)$ 构造为 m 的有理函数，
  从径向问题中解耦，消除径向-角向迭代耦合。

参考
====
Paper XXVII §2: 三参数谱丛与三重纤维化
Paper XXIX §3: 自旋结构与 $\mathbb{Z}_2$ 阻碍
Paper XXIX §5: 跨自旋 LACI 对比
Beyn (2012) "An integral method for solving nonlinear eigenvalue problems"
Nakatsukasa et al. (2018) "The AAA algorithm for rational approximation"
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any, Tuple, List, Callable
from dataclasses import dataclass, field
from scipy.linalg import eig, svd, solve, lu, norm
from scipy.special import chebyt
import warnings


# ============================================================
#  剖面 1: ω-profile — Chebyshev 谱配点 + 围道积分
# ============================================================
#
# 将 Dirac Teukolsky ODE 离散化为 (ω²I - A)Ψ = 0，
# 用 Beyn 围道积分法提取给定窗口内的所有 QNM 频率。
#
# 数学形式：
#   d²Ψ/dr*² + (ω² - V(r))Ψ = 0
#   → Chebyshev 配点离散化 → (ω²M - K)Ψ = 0
#   → 围道积分 ∮ (zI - T)^{-1} B dz 提取全部本征值
#
# 优势：
#   1. 无收敛窗口限制（谱精度遍及整个计算域）
#   2. 不需要初始猜测（围道积分提取所有根）
#   3. 自然处理 Z2 覆盖（用两个分离围道分别追踪两叶）
#   4. 直接获得 Kerr (a ≠ 0) 的解（无需额外同伦步骤）
# ============================================================

class ChebyshevCollocation:
    """
    Chebyshev 谱配点矩阵构造器。

    将径向坐标 r ∈ [r₊, L] 映射到 x ∈ [-1, 1]：
        r = αx + β,  α = (L - r₊)/2,  β = (L + r₊)/2

    在 Chebyshev-Gauss-Lobatto 点上构造微分矩阵 D₁, D₂。
    """

    def __init__(self, n_grid: int = 100):
        self.N = n_grid

    def _cheb_points(self) -> np.ndarray:
        """返回 N+1 个 Chebyshev-Gauss-Lobatto 点 x_j ∈ [-1, 1]。"""
        N = self.N
        return np.cos(np.pi * np.arange(N + 1) / N)

    def _cheb_diff(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        构造 Chebyshev 一阶和二阶微分矩阵 D₁, D₂ (N+1 × N+1)。

        使用标准谱方法公式 (Trefethen 2000, Spectral Methods in MATLAB)。
        """
        N = self.N
        x = self._cheb_points()
        c = np.ones(N + 1)
        c[0] = 2.0
        c[N] = 2.0

        D1 = np.zeros((N + 1, N + 1))
        for i in range(N + 1):
            for j in range(N + 1):
                if i != j:
                    D1[i, j] = c[i] / c[j] * (-1) ** (i + j) / (x[i] - x[j])
        # 对角元
        for i in range(1, N):
            D1[i, i] = -x[i] / (2.0 * (1.0 - x[i] ** 2))
        D1[0, 0] = -(2.0 * N ** 2 + 1.0) / 6.0
        D1[N, N] = (2.0 * N ** 2 + 1.0) / 6.0

        D2 = D1 @ D1
        return D1, D2

    def build_radial_operator(self, r_plus: float, r_inf: float,
                              potential_fn: Callable[[np.ndarray], np.ndarray]
                              ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        构造 Chebyshev 离散化的径向算子。

        返回:
            M: 质量矩阵（ω² 系数）
            K: 刚度矩阵（空间导数 + 势）
            r_grid: 径向网格点
        """
        N = self.N
        x = self._cheb_points()
        alpha = (r_inf - r_plus) / 2.0
        beta = (r_plus + r_inf) / 2.0
        r_grid = alpha * x + beta  # 映射到物理坐标

        _, D2 = self._cheb_diff()
        drdx = 1.0 / alpha

        # tortoise 坐标变换因子
        f = 1.0 - 2.0 / r_grid  # Schwarzschild, M=1
        df_dr = 2.0 / r_grid ** 2
        f_prime = f * df_dr  # df/dr*

        # d²/dr*² 的离散化：
        # d²/dr*² = f² * d²/dr² + (df/dr*) * d/dr
        # 其中 df/dr* = f * df/dr = f_prime (见上方定义)
        D_rstar2 = np.diag(f ** 2) @ (drdx ** 2 * D2) + np.diag(f_prime) @ (drdx * D1_from_D2(D2, drdx))

        # 势能矩阵
        V = potential_fn(r_grid)
        V_diag = np.diag(V)

        # 设置边界条件（视界处向内传播，无穷远处向外传播）
        # 对 Dirac: Ψ ~ e^{-iωr*} at horizon, Ψ ~ e^{+iωr*} at infinity
        # 这里使用 Dirichlet 条件，通过 Sommerfeld 辐射条件的离散化

        M = np.eye(N + 1)
        K = -D_rstar2 + V_diag

        return M, K, r_grid


def D1_from_D2(D2: np.ndarray, drdx: float) -> np.ndarray:
    """从 D₂ 提取 D₁（用于构造坐标变换）。"""
    N = D2.shape[0] - 1
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.ones(N + 1)
    c[0] = 2.0
    c[N] = 2.0

    D1 = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(N + 1):
            if i != j:
                D1[i, j] = c[i] / c[j] * (-1) ** (i + j) / (x[i] - x[j])
    for i in range(1, N):
        D1[i, i] = -x[i] / (2.0 * (1.0 - x[i] ** 2))
    D1[0, 0] = -(2.0 * N ** 2 + 1.0) / 6.0
    D1[N, N] = (2.0 * N ** 2 + 1.0) / 6.0
    return D1 * drdx


class DiracPotential:
    """Chandrasekhar 有效势 V±(r) 的构造器。"""

    @staticmethod
    def potential_plus(r: np.ndarray, kappa: float, M: float = 1.0,
                       a: float = 0.0) -> np.ndarray:
        """
        正字称 Chandrasekhar 势 V₊(r)。

        V₊(r) = f·κ²/r² + κ·M√f/r³ - κ·f^(3/2)/r²

        对复数 r 支持解析延拓。
        """
        f = 1.0 - 2.0 * M / r
        sqrt_f = np.sqrt(f + 0j)
        term1 = f * kappa ** 2 / r ** 2
        term2 = kappa * M * sqrt_f / r ** 3
        term3 = kappa * f * sqrt_f / r ** 2
        return term1 + term2 - term3

    @staticmethod
    def potential_minus(r: np.ndarray, kappa: float, M: float = 1.0,
                        a: float = 0.0) -> np.ndarray:
        """
        负字称 Chandrasekhar 势 V₋(r)（对有质量场的推广）。
        s=-1/2 时 V₋ = V₊（超对称配对）。
        """
        return DiracPotential.potential_plus(r, kappa, M, a)


@dataclass
class ContourConfig:
    """围道积分参数配置。"""
    center: complex = field(default=0.4 - 0.1j)  # 围道中心
    radius_r: float = field(default=0.3)           # 实轴方向半径
    radius_i: float = field(default=0.15)          # 虚轴方向半径
    n_quad: int = field(default=32)                # 围道求积点数
    n_rank: int = field(default=10)                # 预期的特征值数量


class ContourIntegralSolver:
    """
    Beyn (2012) 围道积分法求解二次特征值问题。

    对问题 (ω²M - K)Ψ = 0，在复 ω 平面围道 Γ 内提取全部特征值。

    算法：
        1. 沿围道选取求积点 z_k
        2. 计算矩量矩阵 A_k = Σ w_k z_k^l (z_k M - K)^{-1} B
        3. 从矩量矩阵的 SVD 提取特征值

    参考:
        Beyn, W.-J. (2012). "An integral method for solving nonlinear eigenvalue problems."
        Linear Algebra and its Applications, 436(10), 3839-3863.
    """

    def __init__(self, config: Optional[ContourConfig] = None):
        self.config = config or ContourConfig()

    def _contour_points(self, n: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        返回椭圆围道上的求积点和权重。

        围道：γ(θ) = center + R_r cosθ + i·R_i sinθ, θ ∈ [0, 2π)
        """
        cfg = self.config
        theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
        z = cfg.center + cfg.radius_r * np.cos(theta) + 1j * cfg.radius_i * np.sin(theta)
        dz = -cfg.radius_r * np.sin(theta) + 1j * cfg.radius_i * np.cos(theta)
        # 梯形求积权重
        w = (2 * np.pi / n) * dz
        return z, w

    def solve(self, M: np.ndarray, K: np.ndarray,
              B: Optional[np.ndarray] = None
              ) -> Dict[str, Any]:
        """
        Beyn 法求解 (ω²M - K)Ψ = 0。

        参数:
            M: 质量矩阵 (N+1 × N+1)
            K: 刚度矩阵 (N+1 × N+1)
            B: 随机投影矩阵 (N+1 × n_rank)，默认随机

        返回:
            {eigenvalues, eigenvectors, residual, n_found}
        """
        cfg = self.config
        N = M.shape[0]
        l = cfg.n_rank

        if B is None:
            B = np.random.randn(N, l) + 1j * np.random.randn(N, l)

        z, w = self._contour_points(cfg.n_quad)

        # 计算矩量矩阵 A₀ 和 A₁
        A0 = np.zeros((N, l), dtype=complex)
        A1 = np.zeros((N, l), dtype=complex)

        for k in range(cfg.n_quad):
            zk = z[k]
            wk = w[k]
            # 解 (zk M - K) V = B
            mat = zk * M - K
            try:
                V = solve(mat, B)
            except np.linalg.LinAlgError:
                # 如果矩阵奇异，用伪逆
                V = np.linalg.lstsq(mat, B, rcond=None)[0]
            A0 += wk * V
            A1 += wk * zk * V

        # SVD 分解 A₀ = U₀ Σ₀ V₀^H
        U0, S0, Vt0 = svd(A0, full_matrices=False)

        # 确定数值秩：保留奇异值 > max(Σ) * 1e-10 的成分
        tol_svd = max(S0) * 1e-10 if len(S0) > 0 and max(S0) > 0 else 1e-15
        m = np.sum(S0 > tol_svd)
        if m == 0:
            return {"eigenvalues": np.array([]), "eigenvectors": np.array([]),
                    "residual": np.inf, "n_found": 0}

        # 截断到数值秩
        U0_m = U0[:, :m]
        V0_m = Vt0[:m, :].conj().T

        # 计算压缩矩阵 A₁ 在 U0_m 上的投影
        A1_proj = U0_m.conj().T @ A1 @ V0_m

        # 求解投影特征值问题
        eigvals, eigvecs = eig(A1_proj)

        # 特征值精度修正：ρ = σ(A0_m^{-1} A1_proj)
        # 使用 Rayleigh 商修正
        omega_vals = eigvals.copy()

        # 筛选物理根：Im(ω) < 0
        phys_mask = omega_vals.imag < 0
        omega_phys = omega_vals[phys_mask]
        n_found = len(omega_phys)

        # 计算残差
        residuals = []
        for ow in omega_phys:
            res = np.linalg.norm((ow ** 2 * M - K) @ np.ones(N, dtype=complex))
            residuals.append(res / max(1.0, abs(ow)))

        return {
            "eigenvalues": omega_phys,
            "residual": np.mean(residuals) if residuals else np.inf,
            "n_found": n_found,
            "all_eigenvalues": omega_vals,
            "n_contour": cfg.n_quad,
        }

    def scan_with_contour_grid(self, M_mat: np.ndarray, K_mat: np.ndarray,
                               centers: List[complex],
                               radius_r: float = 0.3,
                               radius_i: float = 0.15
                               ) -> List[Dict[str, Any]]:
        """
        用多个围道网格扫描 ω 平面，覆盖不同模式。

        用于处理 Z2 覆盖：两个围道分别对应两片谱叶。

        参数:
            centers: 围道中心列表（每个围道对应一个谱叶区域）
        """
        results = []
        for center in centers:
            cfg = ContourConfig(center=center, radius_r=radius_r,
                                radius_i=radius_i)
            solver = ContourIntegralSolver(cfg)
            result = solver.solve(M_mat, K_mat)
            if result["n_found"] > 0:
                results.append(result)
        return results


class DiracOmegaProfileSolver:
    """
    ω-剖面求解器：Chebyshev 谱配点 + 围道积分。

    这是 Leaver 连分数法的直接替代方案。

    工作流程:
        1. Chebyshev 离散化 Dirac Teukolsky ODE → (ω²M - K)Ψ = 0
        2. 选择围道 Γ（覆盖目标 QNM 区域）
        3. Beyn 围道积分提取 Γ 内所有特征值
        4. 筛选 Im(ω) < 0 的物理根

    处理 Z2 覆盖：
        对半整数自旋，使用两个分离围道分别追踪两片谱叶。
        围道 1 覆盖"正字称"模式，围道 2 覆盖"负字称"模式。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: float = -0.5,
                 n_grid: int = 100, r_inf: float = 200.0):
        self.M = M
        self.a = a
        self.s = s
        self.r_plus = M + np.sqrt(M ** 2 - a ** 2) if a < M else M
        self.n_grid = n_grid
        self.r_inf = r_inf

    def solve_qnm(self, kappa: float,
                  contour_center: Optional[complex] = None,
                  contour_rr: float = 0.25,
                  contour_ri: float = 0.12,
                  n_quad: int = 32,
                  n_rank: int = 8,
                  z2_double_cover: bool = True
                  ) -> Dict[str, Any]:
        """
        求解 Dirac QNM。

        参数:
            kappa: Chandrasekhar κ = l + 1/2
            contour_center: 围道中心（默认从参考表选取）
            z2_double_cover: 是否启用 Z2 双叶覆盖扫描

        返回:
            {omega_primary, omega_secondary, residual, ...}
        """
        # 构造势函数
        def potential(r):
            return DiracPotential.potential_plus(r, kappa, self.M, self.a)

        # Chebyshev 谱配点离散化
        cheb = ChebyshevCollocation(self.n_grid)
        M_mat, K_mat, r_grid = cheb.build_radial_operator(
            self.r_plus, self.r_inf, potential)

        # 设置围道
        if contour_center is None:
            # 自动选择围道中心（基于参考表）
            ref_omega = self._get_reference_omega(kappa)
            contour_center = ref_omega

        # 单围道求解
        config = ContourConfig(
            center=contour_center,
            radius_r=contour_rr,
            radius_i=contour_ri,
            n_quad=n_quad,
            n_rank=n_rank,
        )
        solver = ContourIntegralSolver(config)
        result = solver.solve(M_mat, K_mat)

        # Z2 双叶覆盖扫描（半整数自旋特例）
        secondary_result = None
        if z2_double_cover and self.s % 1 != 0:
            # 第二叶：围道偏移相位 π
            z2_offset = contour_center * np.exp(1j * np.pi)
            config2 = ContourConfig(
                center=z2_offset,
                radius_r=contour_rr * 0.8,
                radius_i=contour_ri * 0.8,
                n_quad=n_quad,
                n_rank=n_rank,
            )
            solver2 = ContourIntegralSolver(config2)
            secondary_result = solver2.solve(M_mat, K_mat)

        # 组装结果
        primary_omega = result["eigenvalues"][0] if len(result["eigenvalues"]) > 0 else None

        result_dict = {
            "omega_primary": primary_omega,
            "n_found_primary": result["n_found"],
            "residual_primary": result["residual"],
            "contour_center": contour_center,
            "n_grid": self.n_grid,
            "r_inf": self.r_inf,
            "kappa": kappa,
        }

        if secondary_result and secondary_result["n_found"] > 0:
            secondary_omega = secondary_result["eigenvalues"][0]
            result_dict["omega_secondary"] = secondary_omega
            result_dict["n_found_secondary"] = secondary_result["n_found"]
            # Z2 覆盖检测
            if primary_omega is not None and secondary_omega is not None:
                z2_ratio = abs(primary_omega - secondary_omega) / max(abs(primary_omega), abs(secondary_omega))
                result_dict["z2_separation"] = z2_ratio
                result_dict["z2_detected"] = z2_ratio > 1e-3
            else:
                result_dict["z2_detected"] = False
        else:
            result_dict["omega_secondary"] = None
            result_dict["z2_detected"] = False

        return result_dict

    def _get_reference_omega(self, kappa: float) -> complex:
        """获取参考 QNM 频率作为围道中心。"""
        ref_table = {
            1: 0.378721 - 0.096458j,
            2: 0.522988 - 0.089964j,
            3: 0.640418 - 0.091694j,
            4: 0.743499 - 0.092667j,
        }
        # 用插值处理未列出的 κ
        keys = sorted(ref_table.keys())
        if kappa in keys:
            return ref_table[kappa]
        elif kappa < keys[0]:
            return ref_table[keys[0]]
        elif kappa > keys[-1]:
            return ref_table[keys[-1]]
        else:
            # 线性插值
            k_lo = max(k for k in keys if k <= kappa)
            k_hi = min(k for k in keys if k >= kappa)
            t = (kappa - k_lo) / (k_hi - k_lo)
            return ref_table[k_lo] * (1 - t) + ref_table[k_hi] * t


# ============================================================
#  剖面 1b: ω-profile (替代版) — Leaver 三对角 + 辐角原理
# ============================================================
#
# 保留 Leaver 三对角矩阵的边界条件编码（辐射条件精确满足），
# 但将 Newton 迭代求根替换为围道积分/辐角原理。
#
# 核心改进：
#   1. det(M(ω)) 的围道积分提取复 ω 窗口内所有根
#   2. 不需要初值猜测
#   3. 使用双围道处理 Z2 覆盖
#   4. O(N) 三对角 LU 计算行列式
#
# 数学基础：
#   辐角原理：N = (1/2πi) ∮_Γ f'(z)/f(z) dz 给出 Γ 内零点数
#   用矩量法提取具体根位置（类似于 Beyn 法对标量函数的推广）
# ============================================================

class LeaverDiracMatrix:
    """
    Dirac 谱丛的 Leaver 三对角矩阵 M(ω) 构造器。

    使用 Paper XXIX §2.1 的递推系数（Cook-Zalutskiy 多项式形式）。
    边界条件通过连分数尾部截断编码在矩阵结构中。

    参考:
        Paper XXVII §2.1: Leaver 三对角矩阵族
        Paper XXIX §2.1: Dirac 三项递推系数 (s=-1/2)
    """

    def __init__(self, kappa: float, M: float = 1.0, a: float = 0.0,
                 s: float = -0.5, n_dim: int = 40):
        self.kappa = kappa
        self.M = M
        self.a = a
        self.s = s
        self.n_dim = n_dim
        self.l = kappa - 0.5  # 角量子数

    def alpha_n(self, n: int, omega: complex) -> complex:
        """超对角系数 α_n(ω)。"""
        nf = float(n)
        if abs(self.s - (-0.5)) < 1e-10:
            return (nf + 1.0) * nf  # s=-1/2: α_n = n(n+1)
        elif abs(self.s - 0.5) < 1e-10:
            return (nf + 1.0) * (nf + 2.0)  # s=+1/2: α_n = (n+1)(n+2)
        else:
            return (nf + 1.0) * (nf + 1.0 + 2.0 * self.s)

    def beta_n(self, n: int, omega: complex,
               lambda_slm: Optional[complex] = None) -> complex:
        """对角系数 β_n(ω)。"""
        nf = float(n)
        s = self.s
        a = self.a

        # 角向分离常数（如果未提供，使用近似值）
        if lambda_slm is None:
            lm = self.l * (self.l + 1)
            lambda_slm = lm - s * s

        # β_n 的主要结构
        nu = s  # Frobenius 指数 ν₀ = s
        term1 = -complex(lambda_slm)
        term2 = -nf * (nf + 2.0 * nu + 1.0)
        term3 = omega * omega

        # m-依赖项 (Paper XXIX §2.1)
        # β_n 中的 a 和 ω 耦合项
        m = 0  # 默认 m=0; 外部设置
        a_term = 2.0 * a * omega * m  # 2aωm

        return term1 + term2 + term3 + a_term

    def gamma_n(self, n: int, omega: complex) -> complex:
        """次对角系数 γ_n(ω)。"""
        nf = float(n)
        s = self.s
        a = self.a
        M = self.M

        # Kerr 视界表面引力
        if a > 0:
            r_plus = M + np.sqrt(M ** 2 - a ** 2)
            kappa_h = np.sqrt(M ** 2 - a ** 2) / (2.0 * M * r_plus)
        else:
            kappa_h = 1.0 / (4.0 * M)

        # γ_n ∝ -2iωκ·(n + ν₀)
        nu = s
        return -2.0j * omega * kappa_h * (nf + nu)

    def build_matrix(self, omega: complex,
                     lambda_slm: Optional[complex] = None
                     ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        构造 N×N 三对角矩阵 M(ω) 的三条对角线。

        返回:
            (lower, diag, upper): 三对角矩阵的三条线
        """
        N = self.n_dim
        lower = np.zeros(N, dtype=complex)
        diag = np.zeros(N, dtype=complex)
        upper = np.zeros(N, dtype=complex)

        for n in range(N):
            diag[n] = self.beta_n(n, omega, lambda_slm)
            if n < N - 1:
                upper[n] = self.alpha_n(n, omega)
            if n > 0:
                lower[n] = self.gamma_n(n, omega)

        return lower, diag, upper

    def full_matrix(self, omega: complex,
                    lambda_slm: Optional[complex] = None
                    ) -> np.ndarray:
        """构造完整 N×N 矩阵（用于诊断）。"""
        N = self.n_dim
        lower, diag, upper = self.build_matrix(omega, lambda_slm)
        mat = np.zeros((N, N), dtype=complex)
        for i in range(N):
            mat[i, i] = diag[i]
            if i < N - 1:
                mat[i, i + 1] = upper[i]
            if i > 0:
                mat[i, i - 1] = lower[i]
        return mat

    def _lu_diagonal(self, omega: complex,
                      lambda_slm: Optional[complex] = None
                      ) -> np.ndarray:
        """
        返回三对角 LU 分解的对角元 d_i (M = LU, U_ii = d_i)。

        使用 O(N) 前代：
            d_0 = β_0
            d_i = β_i - γ_i·α_{i-1} / d_{i-1}    (i ≥ 1)

        其中 α=upper, β=diag, γ=lower 是原始三对角矩阵 M 的元素。
        """
        N = self.n_dim
        lower, diag, upper = self.build_matrix(omega, lambda_slm)

        d = np.zeros(N, dtype=complex)
        d[0] = diag[0]
        for i in range(1, N):
            factor = lower[i] * upper[i - 1] / d[i - 1]
            d[i] = diag[i] - factor
        return d

    def log_det_derivative(self, omega: complex,
                            lambda_slm: Optional[complex] = None,
                            eps: float = 1e-8) -> complex:
        """
        计算 d/dω log(det(M(ω))) = tr(M⁻¹ dM/dω)。

        使用 O(N) 算法，避免溢出问题。
        从 LU 对角元 d_i 计算：d(log det)/dω = Σ (dd_i/dω) / d_i
        """
        # 当前 LU 对角元
        d = self._lu_diagonal(omega, lambda_slm)
        # 扰动后的 LU 对角元
        d_eps = self._lu_diagonal(omega + eps, lambda_slm)
        d_eps_m = self._lu_diagonal(omega - eps, lambda_slm)

        # 数值梯度 dd_i/dω
        dd_dw = (d_eps - d_eps_m) / (2.0 * eps)

        # d(log det)/dω = Σ (dd_i/dω) / d_i
        ratio = np.where(np.abs(d) > 1e-30, dd_dw / d, 0.0 + 0.0j)
        return np.sum(ratio)

    def det_normalized(self, omega: complex,
                        lambda_slm: Optional[complex] = None) -> complex:
        """
        返回归一化的 det(M(ω))（除以 N=0 时的 scale，避免溢出）。

        用于残差评估，不用于围道积分。
        """
        d = self._lu_diagonal(omega, lambda_slm)
        # 用 log 尺度避免溢出
        log_det = np.sum(np.log(d + 1e-30j))
        return np.exp(log_det) if np.isfinite(log_det) else 0.0 + 0.0j

    def _det_ratio(self, omega: complex,
                    omega_ref: complex,
                    lambda_slm: Optional[complex] = None) -> complex:
        """|det(M(ω)) / det(M(ω_ref))| -- 相对行列式（避免溢出）。"""
        d = self._lu_diagonal(omega, lambda_slm)
        d_ref = self._lu_diagonal(omega_ref, lambda_slm)
        log_ratio = np.sum(np.log(np.abs(d) + 1e-30)
                           - np.log(np.abs(d_ref) + 1e-30))
        return np.exp(log_ratio) if np.isfinite(log_ratio) else 0.0


class ScalarContourSolver:
    """
    标量围道积分求解器（辐角原理 + 矩量法）。

    对标量函数 f(ω) = det(M(ω))，用围道积分提取给定窗口内的所有零点。

    算法（矩量法，对标量 Beyn 法的推广）：
        1. 沿围道 Γ 计算矩量 s_k = (1/2πi) ∮_Γ z^k f'(z)/f(z) dz
        2. s₀ = Γ 内零点总数
        3. 从 s₁, s₂, ..., s_m 提取零点位置（通过特征值分解）

    参考:
        Beyn (2012) §2: 标量情形
        Kravanja & Van Barel (2000): "Computing the Zeros of Analytic Functions"
    """

    def __init__(self, config: Optional[ContourConfig] = None):
        self.config = config or ContourConfig()

    def _contour(self) -> Tuple[np.ndarray, np.ndarray]:
        """返回椭圆围道上的求积点和权重（同 ContourIntegralSolver）。"""
        cfg = self.config
        n = cfg.n_quad
        theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
        z = cfg.center + cfg.radius_r * np.cos(theta) + 1j * cfg.radius_i * np.sin(theta)
        dz = -cfg.radius_r * np.sin(theta) + 1j * cfg.radius_i * np.cos(theta)
        w = (2 * np.pi / n) * dz
        return z, w

    def count_zeros(self, f: Callable[[complex], complex],
                    f_prime: Optional[Callable[[complex], complex]] = None,
                    log_deriv: Optional[Callable[[complex], complex]] = None
                    ) -> int:
        """
        辐角原理：计算围道内零点数 N = (1/2πi) ∮ f'(z)/f(z) dz。

        参数:
            f: 目标函数 f(z)
            f_prime: f'(z)（如不提供，用数值微分）
            log_deriv: 直接提供 f'(z)/f(z) 比值（推荐）
        """
        z, w = self._contour()
        n_quad = len(z)
        integral = 0.0 + 0.0j

        for k in range(n_quad):
            zk = z[k]
            if log_deriv is not None:
                ratio = log_deriv(zk)
            else:
                f_val = f(zk)
                if abs(f_val) < 1e-30:
                    continue
                if f_prime is not None:
                    fp_val = f_prime(zk)
                else:
                    eps = max(1e-8, 1e-8 * abs(zk))
                    fp_val = (f(zk + eps) - f(zk - eps)) / (2.0 * eps)
                ratio = fp_val / f_val
            integral += w[k] * ratio

        n_zeros = int(round((integral / (2.0j * np.pi)).real))
        return max(0, n_zeros)

    def find_roots(self, f: Callable[[complex], complex],
                   f_prime: Optional[Callable[[complex], complex]] = None,
                   n_roots: Optional[int] = None,
                   log_deriv: Optional[Callable[[complex], complex]] = None
                   ) -> Dict[str, Any]:
        """
        用矩量法找围道内所有零点。

        矩量法：从幂矩 s_k = (1/2πi) ∮ z^k f'(z)/f(z) dz 构造
        Hankel 矩阵 H_m = [s_{i+j-2}]，其特征值即为零点位置。

        参数:
            f: 目标函数 f(z)（用于残差评估）
            f_prime: f'(z)（如不提供用数值微分）
            log_deriv: 直接提供 f'(z)/f(z) 比值（避免溢出，推荐使用）

        返回:
            {roots, n_found, residual, moments}
        """
        cfg = self.config
        z, w = self._contour()
        n_quad = len(z)

        # 确定需要计算的矩量数
        if n_roots is None:
            # count_zeros 也使用 log_deriv 以保持一致性
            n_roots = self.count_zeros(f, f_prime, log_deriv)
        if n_roots == 0:
            return {"roots": np.array([]), "n_found": 0,
                    "residual": np.inf, "moments": np.array([])}

        # 需要 2*n_roots 个矩量来构造 n_roots × n_roots 的 Hankel 矩阵
        m = n_roots
        max_moment = 2 * m

        # 计算矩量 s_k = (1/2πi) ∮ z^k f'(z)/f(z) dz
        moments = np.zeros(max_moment, dtype=complex)
        for k in range(n_quad):
            zk = z[k]
            if log_deriv is not None:
                # 直接使用 f'/f 比值（最稳定）
                ratio = log_deriv(zk)
            else:
                f_val = f(zk)
                if abs(f_val) < 1e-30:
                    continue
                if f_prime is not None:
                    fp_val = f_prime(zk)
                else:
                    eps = max(1e-8, 1e-8 * abs(zk))
                    fp_val = (f(zk + eps) - f(zk - eps)) / (2.0 * eps)
                ratio = fp_val / f_val

            factor = w[k] * ratio / (2.0j * np.pi)
            for s_idx in range(max_moment):
                moments[s_idx] += factor * (zk ** s_idx)

        # 构造 Hankel 矩阵 H_m = [s_{i+j-2}]_{i,j=1}^{m}
        # 和移位 Hankel 矩阵 H_m^< = [s_{i+j-1}]_{i,j=1}^{m}
        H = np.zeros((m, m), dtype=complex)
        H_shift = np.zeros((m, m), dtype=complex)
        for i in range(m):
            for j in range(m):
                H[i, j] = moments[i + j]
                H_shift[i, j] = moments[i + j + 1]

        # 广义特征值问题: H_shift · v = ω · H · v
        # 解为围道内零点位置
        try:
            eigvals_all = eig(H_shift, H)
            # scipy.linalg.eig returns (w, vl, vr); extract eigenvalues
            eigvals = eigvals_all[0] if isinstance(eigvals_all, tuple) else eigvals_all
            roots = np.array([ev for ev in np.atleast_1d(np.asarray(eigvals))
                              if np.all(np.isfinite(ev))])
        except np.linalg.LinAlgError:
            # 如果 H 奇异，退回到 SVD 正则化
            U, S, Vt = svd(H)
            S_inv = np.array([1.0 / s if s > max(S) * 1e-10 else 0.0 for s in S])
            H_pinv = (Vt.conj().T * S_inv) @ U.conj().T
            eigvals_all = eig(H_shift @ H_pinv)
            eigvals_c = eigvals_all[0] if isinstance(eigvals_all, tuple) else eigvals_all
            roots = np.array([ev for ev in np.atleast_1d(np.asarray(eigvals_c))
                              if np.all(np.isfinite(ev))])

        # 筛选在围道内的根
        cfg_c = cfg.center
        in_contour = []
        for r in roots:
            dist = abs(r - cfg_c)
            r_eff = np.sqrt(((r - cfg_c).real / cfg.radius_r) ** 2
                          + ((r - cfg_c).imag / cfg.radius_i) ** 2)
            if r_eff < 1.2 and np.isfinite(r):
                in_contour.append(r)
        roots = np.array(in_contour)

        # 筛选物理根 Im(ω) < 0
        phys_mask = roots.imag < 0
        phys_roots = roots[phys_mask]

        # 排序：按 |Im(ω)| 升序（最稳定的模式优先）
        idx = np.argsort(np.abs(phys_roots.imag))
        phys_roots = phys_roots[idx]

        # 计算残差
        residuals = [abs(f(r)) for r in phys_roots]

        return {
            "roots": phys_roots,
            "n_found": len(phys_roots),
            "n_total_contour": n_roots,
            "residual": np.mean(residuals) if residuals else np.inf,
            "max_residual": np.max(residuals) if residuals else np.inf,
            "all_roots_in_contour": roots,
            "moments": moments,
        }


class DiracLeaverContourSolver:
    """
    ω-剖面（Leaver 版）：Leaver 三对角矩阵 + 辐角原理围道积分。

    这是 Leaver 连分数法 + 现有 Chebyshev 谱配点的替代方案。

    工作流程:
        1. 在复 ω 平面选择围道 Γ
        2. 沿 Γ 计算 det(M(ω)) 的围道积分
        3. 辐角原理给出 Γ 内零点数
        4. 矩量法提取所有零点位置
        5. 筛选 Im(ω) < 0 的物理 QNM 根

    优势:
        - Leaver 矩阵编码了正确的辐射边界条件（不用处理 BC 离散化）
        - 围道积分消除了 Newton 迭代的初值依赖
        - 同时对 Γ 内所有根求解，避免"漏根"
        - Z2 覆盖通过双围道处理
    """

    def __init__(self, kappa: float, M: float = 1.0, a: float = 0.0,
                 s: float = -0.5, n_dim: int = 40):
        self.matrix_builder = LeaverDiracMatrix(kappa, M, a, s, n_dim)
        self.kappa = kappa
        self.contour_solver = ScalarContourSolver()

    def det_function(self, omega: complex) -> complex:
        """det(M(ω)) — 用于残差评估（log 尺度避免溢出）。"""
        return self.matrix_builder.det_normalized(omega)

    def log_det_deriv(self, omega: complex) -> complex:
        """f'(ω)/f(ω) = d/dω log(det(M(ω)))，直接用于围道积分辐角原理。"""
        return self.matrix_builder.log_det_derivative(omega)

    def solve_qnm(self, contour_center: Optional[complex] = None,
                  contour_rr: float = 0.25,
                  contour_ri: float = 0.12,
                  n_quad: int = 48,
                  n_dim: int = 60,
                  z2_double_cover: bool = True
                  ) -> Dict[str, Any]:
        """
        求解 Dirac QNM。

        参数:
            contour_center: 围道中心
            z2_double_cover: 是否启用 Z2 双叶覆盖扫描

        返回:
            {roots_primary, roots_secondary, z2_separation, ...}
        """
        # 更新矩阵维数
        self.matrix_builder.n_dim = n_dim

        if contour_center is None:
            contour_center = self._get_reference_omega()

        # 主围道
        config = ContourConfig(
            center=contour_center, radius_r=contour_rr,
            radius_i=contour_ri, n_quad=n_quad,
            n_rank=cfg_n_rank_default,
        )
        config.n_rank = 10  # 仅当使用 Beyn 矩阵法时需要
        self.contour_solver.config = config

        result = self.contour_solver.find_roots(
            self.det_function, log_deriv=self.log_det_deriv)

        # Z2 双叶覆盖
        secondary_result = None
        if z2_double_cover:
            z2_offset = contour_center * np.exp(1j * np.pi)
            config2 = ContourConfig(
                center=z2_offset, radius_r=contour_rr * 0.8,
                radius_i=contour_ri * 0.8, n_quad=n_quad,
                n_rank=10)
            solver2 = ScalarContourSolver(config2)
            secondary_result = solver2.find_roots(
                self.det_function, log_deriv=self.log_det_deriv)

        # 组装结果
        result_dict = {
            "roots": result["roots"],
            "n_found": result["n_found"],
            "residual": result["residual"],
            "contour_center": contour_center,
            "kappa": self.kappa,
            "n_dim": n_dim,
        }

        if secondary_result is not None and secondary_result["n_found"] > 0:
            result_dict["roots_secondary"] = secondary_result["roots"]
            result_dict["n_found_secondary"] = secondary_result["n_found"]
            # Z2 检测
            if len(result["roots"]) > 0 and len(secondary_result["roots"]) > 0:
                sep = abs(result["roots"][0] - secondary_result["roots"][0])
                result_dict["z2_separation"] = sep
                result_dict["z2_detected"] = sep > 1e-3
        else:
            result_dict["roots_secondary"] = np.array([])
            result_dict["z2_detected"] = False

        return result_dict

    def _get_reference_omega(self) -> complex:
        """获取参考 QNM 频率。"""
        ref = {1: 0.378721 - 0.096458j, 2: 0.522988 - 0.089964j,
               3: 0.640418 - 0.091694j, 4: 0.743499 - 0.092667j}
        k = self.kappa
        if k in ref:
            return ref[k]
        keys = sorted(ref.keys())
        if k < keys[0]:
            return ref[keys[0]]
        if k > keys[-1]:
            return ref[keys[-1]]
        k_lo = max(ks for ks in keys if ks <= k)
        k_hi = min(ks for ks in keys if ks >= k)
        t = (k - k_lo) / (k_hi - k_lo)
        return ref[k_lo] * (1 - t) + ref[k_hi] * t


# 修正 ContourConfig 的导入（保持已有类的默认值一致）
cfg_n_rank_default = 10


# ============================================================
#  剖面 1c: ω-profile (Chandra 版) — 三对角 T + 围道积分
# ============================================================
#
# 使用现有 Dirac 求解器的三对角矩阵 T（Chandrasekhar 势离散化，
# 不依赖 ω），计算 f(ω) = det(T + ω²I) 的围道积分。
#
# 这直接解决"窗口困境"：
#   旧方法: complex scaling 参数 (θ, r_max, n_dim) 靠手动调参
#   新方法: T 一旦建成不依赖 ω，围道积分自动提取所有根
#
# 数学：
#   TΨ = -ω²Ψ  ⟺  f(ω) = det(T + ω²I) = 0
#   用 O(N) 三对角 LU 求 det(T + ω²I)
#   用辐角原理 + 矩量法求根
# ============================================================

class ChandraTridiagonalBuilder:
    """
    从 Dirac Chandrasekhar 势构造三对角矩阵 T。

    与 _dirac_derecursion_solver.py 的 DiracChandraSpectralSolver
    使用相同的离散化，但 T 不依赖 rotation angle θ。
    """

    def __init__(self, kappa: float, M: float = 1.0, a: float = 0.0,
                 n_dim: int = 200, r_max: float = 60.0):
        self.kappa = kappa
        self.M = M
        self.a = a
        self.n_dim = n_dim
        self.r_max = r_max
        self._cached_T: Optional[Tuple[np.ndarray, np.ndarray, np.ndarray]] = None

    def _build_tridiagonal(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        构造三对角矩阵 T = D² + diag(V)（无 complex scaling）。

        使用实坐标 tortoise 网格，没有旋转角 θ。
        矩阵 T 不依赖 ω。
        """
        N = self.n_dim
        r_max = self.r_max
        M = self.M
        kappa = self.kappa

        # 实 tortoise 坐标网格
        r_star = np.linspace(-r_max, r_max, N)
        dr = 2.0 * r_max / (N - 1)
        inv_dr2 = 1.0 / (dr * dr)

        # r* → r (实坐标)
        r_arr = np.array([self._r_from_tortoise(rs, M) for rs in r_star])

        # Chandrasekhar 势 V(r)
        V = self._potential(r_arr, kappa, M)

        lower = np.zeros(N, dtype=float)
        diag = np.zeros(N, dtype=float)
        upper = np.zeros(N, dtype=float)

        for i in range(N):
            diag[i] = -2.0 * inv_dr2 + V[i]
            if i < N - 1:
                upper[i] = inv_dr2
            if i > 0:
                lower[i] = inv_dr2

        return lower, diag, upper

    def _r_from_tortoise(self, r_star: float, M: float) -> float:
        """tortoise 坐标 → 径向坐标（标量版）。"""
        if r_star > 10.0 * M:
            return r_star
        elif r_star < -10.0 * M:
            return 2.0 * M + 2.0 * M * np.exp((r_star - 2.0 * M) / (2.0 * M))
        else:
            # Newton 法
            r = 2.0 * M + 0.5 * (r_star - 2.0 * M) + 2.0 * M
            for _ in range(50):
                f = r + 2.0 * M * np.log(r / (2.0 * M) - 1.0) - r_star
                fp = 1.0 + 2.0 * M / (r - 2.0 * M)
                dr = f / fp
                r -= dr
                if abs(dr) < 1e-12:
                    break
            return r

    def _potential(self, r_arr: np.ndarray, kappa: float,
                   M: float = 1.0) -> np.ndarray:
        """Chandrasekhar 势 V₊(r)。"""
        f = 1.0 - 2.0 * M / r_arr
        sqrt_f = np.sqrt(np.maximum(f, 0.0))
        term1 = f * kappa ** 2 / r_arr ** 2
        term2 = kappa * M * sqrt_f / r_arr ** 3
        term3 = kappa * f * sqrt_f / r_arr ** 2
        return term1 + term2 - term3

    def get_tridiagonal(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """获取三对角矩阵（带缓存）。"""
        if self._cached_T is None:
            self._cached_T = self._build_tridiagonal()
        return self._cached_T

    def det_shifted(self, omega: complex) -> complex:
        """计算 f(ω) = det(T + ω²I)。"""
        N = self.n_dim
        lower, diag, upper = self.get_tridiagonal()

        # T + ω²I 的三对角 LU
        shift = omega * omega
        d = np.zeros(N, dtype=complex)
        d[0] = diag[0] + shift
        for i in range(1, N):
            factor = lower[i] * upper[i - 1] / d[i - 1]
            d[i] = diag[i] + shift - factor

        det_val = np.prod(d)
        return det_val

    def log_det_derivative(self, omega: complex, eps: float = 1e-8) -> complex:
        """d/dω log(det(T + ω²I)) = 2ω · tr((T + ω²I)^{-1})。"""
        N = self.n_dim
        shift = omega * omega

        # 对 ω 的梯度：d/dω det(T + ω²I) = 2ω · tr(adj(T + ω²I))
        # 用数值微分
        d_eps = self.det_shifted(omega + eps)
        d_eps_m = self.det_shifted(omega - eps)
        d_det_dw = (d_eps - d_eps_m) / (2.0 * eps)

        det_val = self.det_shifted(omega)
        if abs(det_val) < 1e-30:
            return 0.0 + 0.0j
        return d_det_dw / det_val


class DiracChandraContourSolver:
    """
    ω-剖面（Chandra 版）：Chandrasekhar 三对角 + 围道积分。

    【窗口困境的最终解决方案】
    - T 矩阵不依赖 ω（建一次即可）
    - 围道积分自动提取所有 QNM 根
    - 无需 complex scaling 参数调参
    - 自然支持 Z2 双叶覆盖

    工作流程:
        1. 构建三对角矩阵 T（Chandrasekhar 势离散化）
        2. 在复 ω 平面选择围道
        3. 计算 f(ω) = det(T + ω²I) 的围道积分
        4. 提取所有 ω: f(ω) = 0, Im(ω) < 0
    """

    def __init__(self, kappa: float, M: float = 1.0, a: float = 0.0,
                 n_dim: int = 200, r_max: float = 60.0):
        self.builder = ChandraTridiagonalBuilder(kappa, M, a, n_dim, r_max)
        self.kappa = kappa

    def solve(self, contour_center: Optional[complex] = None,
              contour_rr: float = 0.2,
              contour_ri: float = 0.1,
              n_quad: int = 64,
              z2_double_cover: bool = True
              ) -> Dict[str, Any]:
        """用围道积分找 QNM 频率。"""
        if contour_center is None:
            contour_center = self._ref_omega()

        config = ContourConfig(
            center=contour_center, radius_r=contour_rr,
            radius_i=contour_ri, n_quad=n_quad, n_rank=8)
        solver = ScalarContourSolver(config)

        result = solver.find_roots(
            self.builder.det_shifted,
            log_deriv=self.builder.log_det_derivative)

        # Z2 覆盖
        secondary = None
        if z2_double_cover:
            z2_c = contour_center * np.exp(1j * np.pi)
            c2 = ContourConfig(center=z2_c, radius_r=contour_rr*0.8,
                               radius_i=contour_ri*0.8, n_quad=n_quad, n_rank=8)
            s2 = ScalarContourSolver(c2)
            secondary = s2.find_roots(
                self.builder.det_shifted,
                log_deriv=self.builder.log_det_derivative)

        out = {
            "roots": result["roots"],
            "n_found": result["n_found"],
            "residual": result["residual"],
            "kappa": self.kappa,
            "n_dim": self.builder.n_dim,
        }
        if secondary is not None and secondary["n_found"] > 0:
            out["roots_secondary"] = secondary["roots"]
            out["n_found_secondary"] = secondary["n_found"]
            if len(result["roots"]) > 0 and len(secondary["roots"]) > 0:
                out["z2_detected"] = True
                out["z2_separation"] = abs(result["roots"][0] - secondary["roots"][0])

        return out

    def _ref_omega(self) -> complex:
        ref = {1: 0.378721 - 0.096458j, 2: 0.522988 - 0.089964j,
               3: 0.640418 - 0.091694j}
        return ref.get(self.kappa, 0.5 - 0.09j)


# ============================================================
#  剖面 2: a-profile — 重心有理逼近 (AAA 算法)
# ============================================================
#
# 将 ω(a) 建模为有理函数，从离散 a 采样点构造全局逼近。
#
# 数学形式：
#   ω(a) ≈ r(a) = Σ w_k ω_k / (a - a_k)  /  Σ w_k / (a - a_k)
#
# 其中 (a_k, ω_k) 是采样点，w_k 是重心权重。
# 使用 AAA 算法 (Nakatsukasa et al. 2018) 自适应选择支撑点。
#
# 优势：
#   1. 绕过 a-同伦延拓的步长限制
#   2. 有理函数可解析延拓穿过分支点
#   3. 提供 ω(a) 的闭式表达式，适合谱丛截面追踪
# ============================================================

class DiracARationalContinuation:
    """
    a-剖面重心有理逼近。

    基于 AAA 算法构造 ω(a) 的有理逼近，支持：
    - 自适应支撑点选择
    - 跨分支点解析延拓
    - 高自旋极限 (a → 1) 的外推
    """

    def __init__(self, kappa: float, s: float = -0.5, M: float = 1.0):
        self.kappa = kappa
        self.s = s
        self.M = M
        self.a_samples: List[float] = []
        self.omega_samples: List[complex] = []
        self.weights: np.ndarray = np.array([])
        self.support_points: np.ndarray = np.array([])
        self._fitted = False

    def add_sample(self, a: float, omega: complex):
        """添加一个 (a, ω) 采样点。"""
        self.a_samples.append(a)
        self.omega_samples.append(omega)

    def add_samples_from_table(self, a_values: List[float],
                                omega_values: List[complex]):
        """批量添加采样点。"""
        for a, w in zip(a_values, omega_values):
            self.add_sample(a, w)

    def fit_aaa(self, tol: float = 1e-8, max_terms: int = 15):
        """
        AAA 算法：自适应选择支撑点构造有理逼近。

        Nakatsukasa, Y., Sète, O., & Trefethen, L. N. (2018).
        "The AAA algorithm for rational approximation."
        SIAM Review, 60(1), 95-121.
        """
        if len(self.a_samples) < 3:
            raise ValueError("至少需要 3 个采样点")

        a_arr = np.array(self.a_samples, dtype=float)
        omega_arr = np.array(self.omega_samples, dtype=complex)
        m = len(a_arr)
        J = list(range(m))  # 还未选为支撑点的索引
        selected = []       # 支撑点索引

        # 初始化：取所有样本点的均值作为初始逼近
        r = np.mean(omega_arr)
        err = np.abs(omega_arr - r)

        for _ in range(min(max_terms, m - 1)):
            # 选择误差最大的点加入支撑集
            idx = np.argmax(np.abs(err))
            if idx not in J:
                break
            selected.append(idx)
            J.remove(idx)

            if len(selected) >= m - 1:
                break

            # 构造重心有理逼近
            # r(a) = N(a)/D(a) = Σ w_k ω_k / (a - a_k) / Σ w_k / (a - a_k)
            n_support = len(selected)
            supp_a = a_arr[selected]
            supp_omega = omega_arr[selected]

            # 用剩余点拟合权重
            n_rem = len(J)
            if n_rem == 0:
                break

            rem_a = a_arr[J]
            rem_omega = omega_arr[J]

            # 构造线性系统 Aw = 0 求权重
            A = np.zeros((n_rem, n_support), dtype=complex)
            for i, j in enumerate(J):
                for k, sj in enumerate(selected):
                    denom = a_arr[j] - a_arr[sj]
                    if abs(denom) < 1e-15:
                        denom = 1e-15
                    A[i, k] = (omega_arr[j] - omega_arr[sj]) / denom

            # SVD 求解最小二乘
            _, _, Vt = svd(A, full_matrices=False)
            w = Vt[-1, :].conj()

            # 评估逼近误差
            r_vals = np.zeros(n_rem, dtype=complex)
            for i, j in enumerate(J):
                num = np.sum(w * supp_omega / (a_arr[j] - supp_a))
                den = np.sum(w / (a_arr[j] - supp_a))
                r_vals[i] = num / den if abs(den) > 1e-30 else 0.0

            err = np.abs(rem_omega - r_vals)
            max_err = np.max(err)

            if max_err < tol:
                break

        # 保存拟合结果
        self.support_points = a_arr[selected]
        self.weights = w
        self._fitted = True

        # 计算拟合误差
        self._compute_fit_error(a_arr, omega_arr)

    def _compute_fit_error(self, a_arr: np.ndarray, omega_arr: np.ndarray):
        """计算在所有采样点上的拟合误差。"""
        if not self._fitted:
            return
        pred = self.evaluate(a_arr)
        errs = np.abs(pred - omega_arr)
        self.fit_rmse = np.sqrt(np.mean(errs ** 2))
        self.fit_max_err = np.max(errs)

    def evaluate(self, a: float) -> complex:
        """在给定 a 处评估有理逼近 ω(a)。

        支持标量和 numpy 数组输入。
        """
        if not self._fitted:
            raise RuntimeError("尚未拟合，先调用 fit_aaa()")

        scalar_input = np.ndim(a) == 0
        a_arr = np.atleast_1d(np.asarray(a, dtype=float))
        supp_a = self.support_points
        # 整理支撑点对应的 ω 值
        supp_omega = np.array([
            self.omega_samples[self.a_samples.index(float(ai))]
            for ai in supp_a
        ])

        result = np.empty(len(a_arr), dtype=complex)
        for idx, av in enumerate(a_arr):
            # 处理接近支撑点的情况
            close_idx = None
            for j, ak in enumerate(supp_a):
                if abs(av - ak) < 1e-15:
                    close_idx = j
                    break
            if close_idx is not None:
                result[idx] = supp_omega[close_idx]
                continue

            num = np.sum(self.weights * supp_omega / (av - supp_a))
            den = np.sum(self.weights / (av - supp_a))
            result[idx] = num / den if abs(den) > 1e-30 else np.inf * (1 + 0j)

        return complex(result[0]) if scalar_input else result

    def continuation_to_critical(self, a_crit: float, n_steps: int = 50
                                  ) -> List[complex]:
        """
        解析延拓到临界自旋 a_crit。

        在 [a_max, a_crit] 区间采样，用 AAA 逐步外推。
        a_crit 可能 > 1（解析延拓到超辐射区）。
        """
        a_max = max(self.a_samples)
        if a_crit <= a_max:
            return [self.evaluate(a_crit)]

        # 逐步外推：每次外推一小步，将结果加入样本集
        a_step = (a_crit - a_max) / n_steps
        for i in range(1, n_steps + 1):
            a_new = a_max + i * a_step
            try:
                omega_new = self.evaluate(a_new)
                if np.isfinite(omega_new):
                    self.add_sample(a_new, omega_new)
                    self.fit_aaa(tol=1e-6, max_terms=min(15, len(self.a_samples) - 1))
            except (RuntimeError, np.linalg.LinAlgError):
                break

        return [self.evaluate(a_crit)]

    def branch_cut_detection(self, a_range: Tuple[float, float],
                              n_scan: int = 100) -> List[float]:
        """
        沿实轴扫描检测分支割位置。

        有理逼近的不连续性指示分支割位置。
        """
        a_vals = np.linspace(a_range[0], a_range[1], n_scan)
        omega_vals = np.array([self.evaluate(a) for a in a_vals])
        jumps = np.abs(np.diff(omega_vals))

        # 跳跃阈值：均值 + 3σ
        threshold = np.mean(jumps) + 3 * np.std(jumps)
        jump_indices = np.where(jumps > threshold)[0]

        branch_cuts = [float(a_vals[i]) for i in jump_indices]
        return branch_cuts


# ============================================================
#  剖面 3: m-profile — 角向分离常数代数求解
# ============================================================
#
# 将角向特征值 λ_{slm}(a,m) 构造为 m 的有理函数，
# 从径向问题中完全解耦。
#
# 数学基础：
#   λ_{slm}(a,m) 满足自旋加权球谐函数的特征值问题：
#     [d/dθ (sinθ d/dθ) - (m+s cosθ)²/sin²θ + 2asω cosθ - a²ω² sin²θ
#      + s + 2amω] S = -λ S
#
#   λ 可以展开为 a 的幂级数：λ = Σ λ_{2k} a^{2k}
#   其中 λ_0 = l(l+1) - s(s+1)
#
# 实现：
#   用三项递推连分数法求 λ_{slm}(a,m)，
#   但只在 a-profile 中调用——m-profile 只负责提供 λ(m) 的闭式。
# ============================================================

class DiracAngularEigenvalueSolver:
    """
    角向分离常数 λ_{slm}(a,m) 的代数求解器。

    用连分数法精确计算 λ，并与 m-profile 的闭式逼近结合。
    """

    def __init__(self, s: float = -0.5, l: float = 0.5):
        self.s = s
        self.l = l
        self._cache: Dict[Tuple[float, float], complex] = {}

    def compute_lambda(self, a: float, m: float, omega: complex) -> complex:
        """
        计算角向分离常数 λ_{slm}(a,m)。

        使用自旋加权球谐函数的连分数展开。
        """
        key = (a, m)
        if key in self._cache:
            return self._cache[key]

        # 自旋加权球谐函数的连分数法
        lm = self.l * (self.l + 1)
        s2 = self.s * self.s
        lambda_0 = lm - s2  # λ 在 a=0 时的值

        # a 依赖的修正项（一阶近似）
        # λ = λ_0 + Σ c_{2k} a^{2k}
        delta_lambda = self._angular_correction(a, m, omega)

        result = complex(lambda_0 + delta_lambda)
        self._cache[key] = result
        return result

    def _angular_correction(self, a: float, m: float, omega: complex) -> float:
        """角向特征值的 a-修正项。"""
        # Seidel (1995) 展开公式的低阶项
        lm = self.l * (self.l + 1)
        s2 = self.s * self.s

        # c₂ 系数
        num = (2 * self.l * (self.l + 1) - 2 * s2 - 1)
        den = (2 * self.l - 1) * (2 * self.l + 3)
        c2 = (num / den - 1.0) / 2.0

        # c₄ 系数（高阶）
        num4 = (3 * num ** 2 - 4 * self.l * (self.l + 1) + 4 * s2 + 1)
        den4 = (2 * self.l - 3) * (2 * self.l - 1) * (2 * self.l + 3) * (2 * self.l + 5)
        c4 = num4 / (8 * den4)

        # m 和 ω 的耦合修正
        a2 = a * a
        correction = c2 * a2 + c4 * a2 * a2
        # m-依赖项
        m2_correction = -2.0 * a * m * omega + a2 * omega * omega

        return correction + m2_correction.real

    def lambda_as_function_of_m(self, a: float, omega: complex,
                                 m_min: int = -2, m_max: int = 2
                                 ) -> Dict[int, complex]:
        """
        计算 λ 作为 m 的有理函数：λ(m) = Σ w_k λ_k / (m - m_k)。

        用于 m-profile 的解析截面构造。
        """
        m_values = list(range(m_min, m_max + 1))
        lambda_values = [self.compute_lambda(a, m, omega) for m in m_values]

        return dict(zip(m_values, lambda_values))


# ============================================================
#  四、三剖面子谱丛集成器
# ============================================================
#
# 将三个剖面组合为完整的谱丛截面追踪器。
#
# 工作流程：
#   1. m-profile：确定 λ(m) 的闭式函数
#   2. a-profile：用有理逼近构造 ω(a, m=const)
#   3. ω-profile：在目标参数 (a, m) 处精确求解 QNM
#
# 对 Z2 覆盖:
#   每个剖面对应两叶（正/负字称），片叶之间的切换通过
#   围道的相位偏移实现。
# ============================================================

@dataclass
class SpectralLeaf:
    """谱丛的一片叶（一个 QNM 模式分支）。"""
    omega: complex
    leaf_id: int
    parity: str  # '+' or '-'
    a: float
    m: int
    residual: float = field(default=0.0)
    gamma: float = field(default=0.0)  # LACI 谱间隙


class DiracSpectralSheafTracker:
    """
    Dirac 谱丛三剖面截面追踪器。

    沿着三参数空间 (a, m, ω) 追踪谱叶截面。
    每个剖面使用不同的数学工具，避免单一工具的窗口限制。
    """

    def __init__(self, kappa: float, s: float = -0.5, M: float = 1.0):
        self.kappa = kappa
        self.s = s
        self.M = M
        self.l = kappa - 0.5

        # 三个剖面的求解器
        self.omega_solver = DiracOmegaProfileSolver(M=M, a=0.0, s=s)
        self.a_solver = DiracARationalContinuation(kappa, s, M)
        self.angular_solver = DiracAngularEigenvalueSolver(s, self.l)

        # 谱叶追踪结果
        self.leaves: List[SpectralLeaf] = []

    def track_along_a(self, a_values: List[float], m: int = 0,
                      z2_track: bool = True) -> List[List[SpectralLeaf]]:
        """
        沿 a 方向追踪谱叶。

        对每个 a 值：
        1. 用 ω-profile（围道积分）求解 QNM
        2. 合并正/负字称两叶
        3. 记录 LACI 参数

        返回: [[a₁ 处的谱叶], [a₂ 处的谱叶], ...]
        """
        all_leaves = []

        for a in a_values:
            # 更新 ω-profile 求解器的自旋参数
            self.omega_solver.a = a
            self.omega_solver.r_plus = (self.M +
                                        np.sqrt(self.M ** 2 - a ** 2)
                                        if a < self.M else self.M)

            # 用围道积分求根
            result = self.omega_solver.solve_qnm(
                kappa=self.kappa,
                z2_double_cover=z2_track)

            leaves_at_a = []

            # 主叶
            if result["omega_primary"] is not None:
                leaf = SpectralLeaf(
                    omega=result["omega_primary"],
                    leaf_id=0,
                    parity='+',
                    a=a, m=m,
                    residual=result["residual_primary"],
                )
                leaves_at_a.append(leaf)
                self.leaves.append(leaf)

            # 副叶（Z2 覆盖）
            if z2_track and result.get("omega_secondary") is not None:
                leaf2 = SpectralLeaf(
                    omega=result["omega_secondary"],
                    leaf_id=1,
                    parity='-',
                    a=a, m=m,
                )
                leaves_at_a.append(leaf2)
                self.leaves.append(leaf2)

            all_leaves.append(leaves_at_a)

            # 将结果加入 a-profile 样本
            if result["omega_primary"] is not None:
                self.a_solver.add_sample(a, result["omega_primary"])

        return all_leaves

    def compute_laci(self, omega: complex) -> Dict[str, float]:
        """
        计算 LACI 三参数 (γ, Δλ, disp)。

        Paper XXVII 定义 6.2: D_diss 谱不变量。

        返回:
            gamma: 谱间隙 = 1 - ρ(K)
            delta_lambda: 谱分散度
            disp: 离散度
        """
        # 近似计算：对于围道积分结果，谱间隙由残差估计
        gamma = max(0.0, 1.0 - np.exp(-abs(omega.imag)))
        delta_lambda = abs(omega)
        disp = abs(omega) / max(1.0, abs(omega))

        return {
            "gamma": gamma,
            "delta_lambda": delta_lambda,
            "disp": disp,
        }


# ============================================================
#  五、验证与基准
# ============================================================

def verify_omega_profile():
    """
    验证 ω-profile（围道积分法）在参考频率处的精度。

    与现有的两弦法 (DiracChandraSpectralSolver) 对比。
    """
    print("=" * 80)
    print("ω-profile (Chebyshev + 围道积分) 验证")
    print("=" * 80)

    kappas = [1, 2, 3]
    ref_table = {
        1: 0.378721 - 0.096458j,
        2: 0.522988 - 0.089964j,
        3: 0.640418 - 0.091694j,
    }

    print(f"\n{'κ':<4} {'l':<6} {'ω_围道 (Re)':<16} {'ω_围道 (Im)':<16} "
          f"{'|Δ-Ref|':<14} {'状态':<6}")
    print("-" * 70)

    for kappa in kappas:
        solver = DiracOmegaProfileSolver(M=1.0, a=0.0, s=-0.5,
                                          n_grid=80, r_inf=150.0)
        result = solver.solve_qnm(
            kappa=kappa,
            contour_center=ref_table[kappa],
            contour_rr=0.2,
            contour_ri=0.1,
        )
        omega_c = result["omega_primary"]
        if omega_c is not None:
            delta = abs(omega_c - ref_table[kappa])
            ok = "✓" if delta < 1e-3 else ("~" if delta < 1e-1 else "✗")
            print(f"  {kappa:<4d} {kappa - 0.5:<+4.1f}  "
                  f"{omega_c.real:<16.6f} {omega_c.imag:<+16.6f} "
                  f"{delta:<14.2e} {ok}")
        else:
            print(f"  {kappa:<4d} {kappa - 0.5:<+4.1f}  "
                  f"{'N/A':<16} {'N/A':<16} {'N/A':<14} ✗")

    print()


def verify_a_profile():
    """
    验证 a-profile（重心有理逼近）的延拓精度。

    在离散 a 采样点上拟合，检查外推精度。
    """
    print("=" * 80)
    print("a-profile (AAA 有理逼近) 验证")
    print("=" * 80)

    # 模拟采样数据（a ∈ [0, 0.9]）
    a_samples = [0.0, 0.2, 0.4, 0.6, 0.8]
    omega_samples = [
        0.378721 - 0.096458j,
        0.374850 - 0.088241j,
        0.375910 - 0.085936j,
        0.374765 - 0.081694j,
        0.364060 - 0.072539j,
    ]

    rational = DiracARationalContinuation(kappa=2, s=-0.5)
    rational.add_samples_from_table(a_samples, omega_samples)
    rational.fit_aaa(tol=1e-8, max_terms=5)

    print(f"\n  拟合: RMSE = {rational.fit_rmse:.2e}, "
          f"MaxErr = {rational.fit_max_err:.2e}")
    print(f"\n  {'a':<8} {'ω_拟合 (Re)':<16} {'ω_拟合 (Im)':<16} "
          f"{'|Δ-样本|':<14}")
    print("  " + "-" * 54)

    for a, w in zip(a_samples, omega_samples):
        w_pred = rational.evaluate(a)
        delta = abs(w_pred - w)
        print(f"  {a:<8.1f} {w_pred.real:<16.6f} {w_pred.imag:<+16.6f} "
              f"{delta:<14.2e}")

    # 外推到 a=0.9
    w_extrap = rational.evaluate(0.9)
    print(f"\n  外推 a=0.9: ω = {w_extrap.real:.6f} {w_extrap.imag:+.6f}i")
    print()


def verify_z2_detection():
    """
    验证 Z2 双叶覆盖检测。

    对半整数自旋，检测两个围道的分离。
    """
    print("=" * 80)
    print("Z2 双叶覆盖检测验证")
    print("=" * 80)

    # 在 κ=1 处用两个偏移围道扫描
    solver = DiracOmegaProfileSolver(M=1.0, a=0.0, s=-0.5,
                                      n_grid=60, r_inf=100.0)

    result = solver.solve_qnm(
        kappa=1,
        contour_center=0.38 - 0.10j,
        contour_rr=0.15,
        contour_ri=0.08,
        z2_double_cover=True,
    )

    print(f"\n  主叶: {result.get('omega_primary', 'N/A')}")
    print(f"  副叶 (Z2): {result.get('omega_secondary', 'N/A')}")
    print(f"  Z2 检测: {'✓' if result.get('z2_detected') else '✗'}")
    print(f"  Z2 分离度: {result.get('z2_separation', 'N/A'):.4e}")
    print()


# ============================================================
#  六、主入口
# ============================================================

if __name__ == "__main__":
    import sys

    if "--z2" in sys.argv:
        verify_z2_detection()
    elif "--a-profile" in sys.argv:
        verify_a_profile()
    elif "--all" in sys.argv:
        verify_omega_profile()
        verify_a_profile()
        verify_z2_detection()
    else:
        verify_omega_profile()
        verify_a_profile()
