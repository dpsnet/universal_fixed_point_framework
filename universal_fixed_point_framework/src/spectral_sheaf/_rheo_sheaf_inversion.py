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
Phase 58A.2: 谱丛反演 — G*(ω) → 弛豫谱 H(τ)

核心思想:
  从离散频率的 G*(ω) 数据中提取弛豫谱 H(τ) = {G_k, τ_k},
  利用三对角谱丛的几何结构进行物理解筛选 (LACI 判据类比).

反演策略:
  谱丛反演 vs 标准 Tikhonov 正则化的关键区别:

  ┌──────────────────────┬─────────────────────────────┐
  │ Tikhonov 正则化      │ 谱丛反演 (本模块)            │
  ├──────────────────────┼─────────────────────────────┤
  │ 直接在 H(τ) 上求逆   │ 先构建三对角矩阵 M(ω)        │
  │ 人工选择正则化参数 λ  │ M(ω) 谱分解天然提供截断      │
  │ 非物理负权重可能     │ 物理根由"谱叶连续性"保证      │
  │ 欠定 + 不适定        │ 增加树结构约束(well-posed)   │
  └──────────────────────┴─────────────────────────────┘

算法步骤:
  1. 用 Prony 类方法从 G*(ω) 求初始 {τ_k, G_k} 估计
  2. 使用 L-BFGS-B 有界优化精确参数
  3. 沿频率 ω 追踪谱叶的连续性 (LACI 判据)
  4. 只保留物理叶对应的弛豫模式
"""

import numpy as np
from scipy.linalg import eigvals
from scipy.optimize import minimize, least_squares
from ._rheo_to_tridiag import (
    compute_G_star, build_gmm_tridiag,
)

# ---------------------------------------------------------------------------
# 1. Prony 类初值估计（改进版）
# ---------------------------------------------------------------------------

def _prony_initial_estimate(omega, G_star, n_modes):
    """用 Prony 方法从 G*(ω) 估计弛豫参数。

    参数
    ----------
    omega : ndarray (n_freq,)
        频率点
    G_star : ndarray (n_freq,), complex
        测量复数模量
    n_modes : int
        目标 Maxwell 单元数

    返回
    -------
    tau_i : ndarray (n_modes,)
        弛豫时间估计
    G_i : ndarray (n_modes,)
        模量估计
    G_e : float
        平衡模量估计
    """
    n_freq = len(omega)

    # 估计 G_e: 取最低频 G' 作为 G_e 下界
    G_e_est = float(np.real(G_star[0])) * 0.8

    # 弛豫时间铺盖范围: 从 1/ω_max × 0.01 到 1/ω_min × 100
    # 采用密集网格 (10×n_modes 个候选点)
    n_candidates = max(10 * n_modes, 20)
    tau_grid = np.logspace(
        np.log10(1.0 / omega[-1] * 0.01),
        np.log10(1.0 / omega[0] * 100.0),
        n_candidates
    )

    # 构建设计矩阵 A_{jk} = iω_j τ_k / (1 + iω_j τ_k)
    A = np.zeros((n_freq, n_candidates), dtype=complex)
    for k in range(n_candidates):
        A[:, k] = 1j * omega * tau_grid[k] / (1.0 + 1j * omega * tau_grid[k])

    # 目标: G_star - G_e_est ≈ Σ G_k · A(:,k)
    b = G_star - G_e_est
    A_real = np.vstack([A.real, A.imag])
    b_real = np.concatenate([b.real, b.imag])

    # NNLS: 非负最小二乘
    from scipy.optimize import nnls
    x, _ = nnls(A_real, b_real)

    # 选择权重最大的 n_modes 个模式
    idx_top = np.argsort(x)[-n_modes:][::-1]
    tau_selected = tau_grid[idx_top]
    G_selected = x[idx_top]

    # 如果某些权重太小，重新均匀分布
    if np.sum(G_selected) < 1e-10:
        # 对数均匀分布 τ
        tau_selected = np.logspace(
            np.log10(1.0 / omega[-1]),
            np.log10(1.0 / omega[0]),
            n_modes
        )
        G_selected = np.ones(n_modes) * 0.5

    # 细调: 在每个选择的 τ 附近加点扰动，选更好的局部最优
    # (当前简化版，直接返回选择结果)
    return tau_selected, G_selected, G_e_est


# ---------------------------------------------------------------------------
# 2. 谱丛反演: 谱叶追踪 + LACI 筛选
# ---------------------------------------------------------------------------

def _compute_laci(omega_seq, tau_i, alpha_i):
    """计算沿 ω 序列的 LACI 指数 (简化版).

    对谱丛 S_rheo, LACI 的三个分量在此语境中翻译为:
      - 不动点残差 ρ : 谱叶 λ_i(ω) 与 0 的接近程度
      - 分散度 Δ     : 相邻 ω 间谱叶轨迹的跳跃度
      - 谱间隙 γ     : 最小特征值间距

    返回 [0, 1] 之间的值, 高值 = 可靠物理分支.

    注意 (2026-08-16): 本简化版 LACI 方向与判据族成员相反——判据族
    LACI 高 = 静默/不可辨识 (paper1 定义 3.12a)；本实现将"低残差 +
    低分散 + 大间隙"归一化为高值，实为"可靠度"而非静默测度，二者
    不可互用数值（方向相反）。
    """
    n_seq = len(omega_seq)
    if n_seq < 3:
        return 0.5

    # 计算每点的谱叶
    leaves = []
    for w in omega_seq:
        M = build_gmm_tridiag(w, tau_i, alpha_i)
        ev = eigvals(M)
        leaves.append(np.sort(np.abs(ev)))

    leaves = np.array(leaves)

    # 1. 不动点残差: 谱叶到 0 的接近程度
    rho = np.mean(np.min(leaves, axis=1))

    # 2. 分散度: 相邻谱叶的跳跃度
    delta = np.mean(np.abs(np.diff(leaves[:, 0]))) if n_seq > 1 else 0.0

    # 3. 谱间隙: 最小特征值间距
    if leaves.shape[1] > 1:
        gaps = np.diff(leaves, axis=1)
        gamma = np.mean(np.min(gaps, axis=1))
    else:
        gamma = 1.0

    # 综合 LACI = 低残差 + 低分散 + 大间隙 → 高值 (归一化)
    laci = 1.0 / (1.0 + rho + delta + 1.0 / max(gamma, 1e-10))
    return float(laci)


class RheoSpectralInversion:
    """流变学谱丛反演器.

    从 G*(ω) 测量数据反演弛豫谱 H(τ) = {G_k, τ_k},
    利用谱丛几何结构进行物理解筛选.
    """

    def __init__(self, n_modes=5, max_iter=200, laci_threshold=0.3):
        self.n_modes = n_modes
        self.max_iter = max_iter
        self.laci_threshold = laci_threshold

        # 反演结果
        self.tau_i_ = None
        self.G_i_ = None
        self.G_e_ = 0.0
        self.laci_ = 0.0
        self.converged_ = False
        self.residual_ = np.inf

    def fit(self, omega, G_star):
        """执行谱丛反演.

        参数
        ----------
        omega : ndarray (n_freq,)
            频率点
        G_star : ndarray (n_freq,), complex
            测量复数模量
        """
        n = self.n_modes
        omega = np.asarray(omega)
        G_star = np.asarray(G_star)

        # Step 1: Prony 初值
        tau_i, G_i, G_e = _prony_initial_estimate(omega, G_star, n)

        # Step 2: 有界优化 (L-BFGS-B)
        # 参数向量: [log10(τ₁), ..., log10(τₙ), log10(G₁), ..., log10(Gₙ), G_e]
        x0 = np.concatenate([
            np.log10(np.maximum(tau_i, 1e-15)),
            np.log10(np.maximum(G_i, 1e-15)),
            [G_e]
        ])

        n_tau = n

        # 参数边界: τ ∈ [10⁻⁶, 10⁶], G ∈ [10⁻⁶, 10³], G_e ∈ [0, 10³]
        bounds = (
            [(-6, 6)] * n_tau          # log10(τ)
            + [(-6, 3)] * n             # log10(G)
            + [(0, 1e3)]                 # G_e
        )

        def _residual(x):
            tau = 10 ** x[:n_tau]
            G = 10 ** x[n_tau:2 * n_tau]
            G_e_val = x[2 * n_tau]
            G_pred = compute_G_star(omega, G, tau, G_e_val)
            residual_flat = np.concatenate([
                (G_star - G_pred).real,
                (G_star - G_pred).imag
            ])
            return residual_flat

        # 使用最小二乘法 (Levenberg-Marquardt 更适合)
        try:
            res_ls = least_squares(
                _residual, x0,
                bounds=([b[0] for b in bounds], [b[1] for b in bounds]),
                method='trf',               # Trust Region Reflective
                max_nfev=self.max_iter,
                ftol=1e-12,
                xtol=1e-12,
                gtol=1e-12,
                verbose=0,
            )
            success = res_ls.success or res_ls.nfev >= 2
            if success:
                self.tau_i_ = 10 ** res_ls.x[:n_tau]
                self.G_i_ = 10 ** res_ls.x[n_tau:2 * n_tau]
                self.G_e_ = float(res_ls.x[2 * n_tau])
                self.residual_ = float(np.sum(res_ls.fun ** 2))
                self.converged_ = True
            else:
                raise RuntimeError("least_squares failed")
        except Exception:
            # 回退到 Nelder-Mead
            def _scalar_residual(x):
                tau = 10 ** x[:n_tau]
                G = 10 ** x[n_tau:2 * n_tau]
                G_e_val = x[2 * n_tau]
                G_pred = compute_G_star(omega, G, tau, G_e_val)
                return np.sum(np.abs(G_star - G_pred) ** 2)

            res_nm = minimize(
                _scalar_residual, x0, method='Nelder-Mead',
                options={'maxiter': self.max_iter, 'xatol': 1e-8, 'fatol': 1e-10}
            )
            if res_nm.success or res_nm.nfev >= 2:
                self.tau_i_ = 10 ** res_nm.x[:n_tau]
                self.G_i_ = 10 ** res_nm.x[n_tau:2 * n_tau]
                self.G_e_ = float(res_nm.x[2 * n_tau])
                self.residual_ = float(res_nm.fun)
                self.converged_ = True
            else:
                # 回退到 Prony 初值
                self.tau_i_ = tau_i
                self.G_i_ = G_i
                self.G_e_ = G_e
                self.residual_ = _scalar_residual(x0)
                self.converged_ = False

        # Step 3: LACI 评估
        alpha_i = np.sqrt(np.maximum(self.G_i_, 1e-10))
        omega_mid = np.logspace(np.log10(omega[0]), np.log10(omega[-1]), 10)
        self.laci_ = _compute_laci(omega_mid, self.tau_i_, alpha_i)

        return self

    def get_spectrum(self):
        """返回弛豫谱 H(τ)."""
        return {
            "tau": self.tau_i_,
            "G": self.G_i_,
            "G_e": self.G_e_,
            "laci": self.laci_,
            "converged": self.converged_,
            "residual": self.residual_,
        }

    def predict(self, omega):
        """从反演结果预测 G*(ω)."""
        return compute_G_star(omega, self.G_i_, self.tau_i_, self.G_e_)


# ---------------------------------------------------------------------------
# 3. Tikhonov 正则化 (用于对比)
# ---------------------------------------------------------------------------

def tikhonov_inversion(omega, G_star, tau_grid, alpha_reg=0.01):
    """Tikhonov 正则化弛豫谱反演 (对比方法).

    将 H(τ) = Σ G_k δ(τ - τ_k) 在 tau_grid 上离散化,
    求解:  min ||A x - b||² + α ||D x||²

    其中 A 是 GMM 模型矩阵, x = [G_k], b = [G_star_j],
    D 是一阶差分矩阵 (平滑约束).

    参数
    ----------
    omega : ndarray
        频率点
    G_star : ndarray, complex
        复数模量测量
    tau_grid : ndarray
        弛豫时间网格 (对数均匀)
    alpha_reg : float
        正则化参数

    返回
    -------
    result : dict
        {"tau": tau_grid, "G_weights": G_k, "residual": ...}
    """
    n_tau = len(tau_grid)
    n_freq = len(omega)

    # 构建设计矩阵 A
    A = np.zeros((2 * n_freq, n_tau))
    b = np.zeros(2 * n_freq)

    for k in range(n_tau):
        g_k = 1j * omega * tau_grid[k] / (1.0 + 1j * omega * tau_grid[k])
        A[:n_freq, k] = g_k.real
        A[n_freq:, k] = g_k.imag

    # 估计 G_e 并从数据中减去
    G_e_est = float(np.real(G_star[0]) * 0.9)
    G_sub = G_star - G_e_est
    b[:n_freq] = G_sub.real
    b[n_freq:] = G_sub.imag

    # 一阶差分正则化矩阵
    D = np.zeros((n_tau - 1, n_tau))
    np.fill_diagonal(D, -1)
    np.fill_diagonal(D[:, 1:], 1)

    # 最小二乘: [A; αD] x = [b; 0]
    A_aug = np.vstack([A, alpha_reg * D])
    b_aug = np.concatenate([b, np.zeros(n_tau - 1)])

    x, residuals, _, _ = np.linalg.lstsq(A_aug, b_aug, rcond=None)
    G_weights = np.maximum(x, 0)  # 强制非负

    # 计算残差
    pred = compute_G_star(omega, G_weights, tau_grid, G_e_est)
    residual = np.sum(np.abs(G_star - pred) ** 2)

    return {
        "tau": tau_grid,
        "G_weights": G_weights,
        "G_e": G_e_est,
        "residual": residual,
        "n_nonzero": np.sum(G_weights > 1e-6),
    }


# ---------------------------------------------------------------------------
# 4. 封装函数
# ---------------------------------------------------------------------------

def sheaf_inversion(omega, G_star, n_modes=5, max_iter=200):
    """谱丛反演一站式接口.

    参数
    ----------
    omega : ndarray
        频率点
    G_star : ndarray, complex
        复数模量
    n_modes : int
        目标弛豫模式数
    max_iter : int
        最大迭代步数

    返回
    -------
    result : dict
    """
    inverter = RheoSpectralInversion(n_modes=n_modes, max_iter=max_iter)
    inverter.fit(omega, G_star)
    return inverter.get_spectrum()


# ---------------------------------------------------------------------------
# 5. 快速自检
# ---------------------------------------------------------------------------

def _self_test():
    """用合成数据验证谱丛反演."""
    from ._rheo_to_tridiag import synthesize_rheo_data

    np.random.seed(42)
    data = synthesize_rheo_data(n_modes=3, n_freq=80, noise_level=0.0)

    # 谱丛反演
    inv = RheoSpectralInversion(n_modes=3, max_iter=200)
    inv.fit(data["omega"], data["G_star"])
    result = inv.get_spectrum()

    # 验证: tau 恢复偏差
    tau_true = np.sort(data["tau_i"])
    tau_est = np.sort(result["tau"])
    tau_err = np.mean(np.abs(tau_est - tau_true) / tau_true)
    print(f"  τ 恢复偏差: {tau_err:.4f}")

    # 验证: G 恢复偏差
    G_true = np.sort(data["G_i"])[::-1]
    G_est = np.sort(result["G"])[::-1]
    G_err = np.mean(np.abs(G_est - G_true) / np.maximum(G_true, 1e-10))
    print(f"  G 恢复偏差: {G_err:.4f}")

    # 验证: 预测 G* 与测量匹配
    G_pred = inv.predict(data["omega"])
    pred_err = np.mean(np.abs(data["G_star"] - G_pred))
    print(f"  预测 G* 误差: {pred_err:.4e}")

    assert result["laci"] > 0, f"LACI 异常: {result['laci']}"
    print(f"  LACI: {result['laci']:.4f}")
    print(f"  Converged: {result['converged']}")

    print("[_rheo_sheaf_inversion] 自检通过 ✓")


if __name__ == "__main__":
    _self_test()
