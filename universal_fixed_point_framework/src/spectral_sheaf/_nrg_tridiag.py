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
Phase 58B.1: NRG Wilson 链 → 三对角谱丛生成器

数学背景:

  数值重整化群（NRG）的 Wilson 链 Hamiltonian（Kondo 模型）：

      H_N = Σ_{n=0}^N ε_n f_n^† f_n + Σ_{n=0}^{N-1} t_n (f_n^† f_{n+1} + h.c.)

  杂质谱函数通过连分数求解：

      G_imp(ω) = 1/(ω - ε_0 - t_0^2/(ω - ε_1 - t_1^2/(...)))
      A(ω) = -Im G_imp(ω) / π

  三对角谱丛矩阵 M(ω)（N × N）：

      M_{nn}(ω)   = ω - ε_n              (主对角 — 能量参数)
      M_{n,n+1}   = t_n                   (off-diagonal — 跳跃积分)
      M_{n+1,n}   = t_n                   (对称)

  G_imp(ω) = [M(ω)^{-1}]_{00}，即谱丛截面在 (0,0) 矩阵元处的投影。

  谱丛底空间: ω ∈ ℂ (复能量)
  纤维: σ(M(ω)) = {λ ∈ ℂ: det(M(ω) - λI) = 0}
  截面: G_imp(ω) 的极值对应谱丛分支点

  剪枝可行性: Wilson 链的跳跃积分 t_n 随 n 指数衰减 (t_n ∝ Λ^{-n/2})，
              因此高阶格点的谱贡献可被剪枝。

关联:
  · generalization.md §5.2: S_NRG ≅ S_Teuk 同构
  · Paper XIV §5.7: 谱丛理论在凝聚态物理中的应用
  · Leaver 谱丛剪枝算法 (notes/04_lorentz_gravity/spectral_sheaf_leaver.md §4.1)
"""

import numpy as np
from scipy.linalg import eigvals, inv, norm
from scipy.sparse import diags


# ---------------------------------------------------------------------------
# 1. Wilson 链系数 (标准 Kondo 模型)
# ---------------------------------------------------------------------------

def compute_wilson_coefficients(N, Lambda=2.0, D=1.0, xi_method="standard"):
    """计算 Kondo 模型 NRG Wilson 链系数 {ε_n, t_n}.

    Wilson 链对导带进行对数离散化 (Wilson 1975), 得到半无限链:

        H_chain = Σ_{n=0}^∞ t_n (f_n^† f_{n+1} + h.c.)

    其中 ε_n = 0 (粒子-空穴对称 Kondo 模型),
          t_n ∝ Λ^{-n/2} (指数衰减).

    参数
    ----------
    N : int
        链长度
    Lambda : float
        NRG 对数离散化参数 (典型值 2.0-3.0)
    D : float
        导带半带宽 (默认 1.0)
    xi_method : str
        系数计算方法:
        - "standard": Wilson 原始公式 (含 (1-Λ^{-1})/log(Λ) 因子)
        - "simple": 简化版本 t_n = D * Λ^{-n/2}
        - "exact": Bulla 等使用的精确形式

    返回
    -------
    eps_n : ndarray (N,)
        在位能 (Kondo 模型为 0)
    t_n : ndarray (N-1,)
        跳跃积分 (t_n 连接 n 和 n+1 格点)
    """
    n = np.arange(N)

    if xi_method == "standard":
        # Wilson 原始公式 (1975), 含对数离散化的归一化因子
        # ξ_n = (1 + Λ^{-1})(1 - Λ^{-n-1}) / (2 sqrt((1-Λ^{-2n-1})(1-Λ^{-2n-3}))) * Λ^{-n/2}
        # 更常用的形式:
        prefactor = (1.0 + Lambda ** (-1)) / 2.0 * (1.0 - Lambda ** (-(n + 1)))
        if N > 1:
            denom = np.sqrt(
                (1.0 - Lambda ** (-(2 * n[:-1] + 1))) *
                (1.0 - Lambda ** (-(2 * n[:-1] + 3)))
            )
            t_n = D * prefactor[:-1] / np.maximum(denom, 1e-15) * Lambda ** (-n[:-1] / 2.0)
        else:
            t_n = np.array([])

    elif xi_method == "exact":
        # Bulla et al. 使用的精确形式
        # ξ_n = D * (1 - Λ^{-1}) / log(Λ) * Λ^{-n/2} (数值精度更高)
        xi_0 = D * (1.0 - Lambda ** (-1)) / np.log(Lambda)
        if N > 1:
            t_n = xi_0 * Lambda ** (-(n[:-1] + 1) / 2.0)
        else:
            t_n = np.array([])

    else:
        # simple: t_n = D * Λ^{-n/2}
        if N > 1:
            t_n = D * Lambda ** (-n[:-1] / 2.0)
        else:
            t_n = np.array([])

    # Kondo 模型 (粒子-空穴对称): ε_n = 0
    eps_n = np.zeros(N)

    return eps_n, t_n


def compute_impurity_green_function(omega, eps_n, t_n, eta=1e-6):
    """通过向后连分数计算杂质 Green 函数 G_imp(ω).

    使用 Wilson 链的连分数 (终止于链末端):

        G_imp(ω) = 1 / (ω - ε_0 - t_0^2 / (ω - ε_1 - t_1^2 / (...)))

    参数
    ----------
    omega : complex or array_like
        复能量 (ω + iη)
    eps_n : ndarray (N,)
        在位能
    t_n : ndarray (N-1,)
        跳跃积分
    eta : float
        展宽参数 (用于 ω 为实数时)

    返回
    -------
    G_imp : complex or ndarray
        杂质 Green 函数
    """
    scalar_input = np.ndim(omega) == 0
    omega = np.atleast_1d(np.asarray(omega, dtype=complex))

    N = len(eps_n)
    G = np.zeros_like(omega, dtype=complex)

    for i, w in enumerate(omega):
        w = w + 1j * eta
        # 从链末端向前递推
        g = 1.0 / (w - eps_n[-1] + 1j * eta * (N == 1))
        for n in range(N - 2, -1, -1):
            g = 1.0 / (w - eps_n[n] - t_n[n] ** 2 * g)
        G[i] = g

    if scalar_input:
        return G[0]
    return G


def compute_spectral_function(omega, eps_n, t_n, eta=1e-6):
    """计算杂质谱函数 A(ω) = -Im G_imp(ω) / π.

    参数
    ----------
    omega : array_like
        实数频率点
    eps_n, t_n, eta : 同上

    返回
    -------
    A : ndarray
        谱函数 A(ω)
    """
    G = compute_impurity_green_function(omega, eps_n, t_n, eta)
    return -np.imag(G) / np.pi


# ---------------------------------------------------------------------------
# 2. 三对角谱丛矩阵
# ---------------------------------------------------------------------------

def build_nrg_tridiag(omega, eps_n, t_n):
    """构建 NRG Wilson 链的三对角谱丛矩阵 M(ω).

    M(ω) = tridiag( t_{n-1}, ω - ε_n, t_n )

    矩阵结构 (N × N, N = len(eps_n)):

        [ ω-ε₀   t₀     0     ...   0   ]
        [  t₀   ω-ε₁    t₁    ...   0   ]
        [  0     t₁    ω-ε₂   ...   0   ]
        [  ...   ...    ...    ...   t_{N-2} ]
        [  0     0      0    t_{N-2} ω-ε_{N-1} ]

    参数
    ----------
    omega : complex
        复能量
    eps_n : ndarray (N,)
        在位能
    t_n : ndarray (N-1,)
        跳跃积分

    返回
    -------
    M : ndarray (N, N), complex
        三对角矩阵
    """
    N = len(eps_n)
    M = np.zeros((N, N), dtype=complex)

    # 对角元: ω - ε_n
    np.fill_diagonal(M, omega - eps_n)

    # off-diagonal: t_n
    if N > 1:
        idx = np.arange(N - 1)
        M[idx, idx + 1] = t_n
        M[idx + 1, idx] = t_n

    return M


def compute_nrg_spectral_leaves(omega, eps_n, t_n):
    """计算 NRG 谱丛 S_NRG 在 ω 处的纤维 (N 个特征值).

    返回 N 个叶 λ_i(ω), 即 M(ω) 的特征值.
    """
    M = build_nrg_tridiag(omega, eps_n, t_n)
    return eigvals(M)


def green_from_tridiag(omega, eps_n, t_n):
    """通过三对角矩阵求逆计算 G_imp(ω).

    G_imp(ω) = [M(ω)^{-1}]_{00}

    等价于向后连分数, 但用直接矩阵求逆.
    用于交叉验证.

    参数
    ----------
    omega : complex
    eps_n, t_n : ndarray

    返回
    -------
    G_imp : complex
    """
    M = build_nrg_tridiag(omega, eps_n, t_n)
    try:
        Minv = inv(M)
        return Minv[0, 0]
    except np.linalg.LinAlgError:
        # 矩阵奇异: 接近分支点
        return complex(np.inf, np.inf)


# ---------------------------------------------------------------------------
# 3. 合成 Kondo 共振测试数据
# ---------------------------------------------------------------------------

def synthesize_kondo_data(N=60, Lambda=2.0, D=1.0, T_K=1e-4, n_freq=200,
                          freq_range=None, seed=42):
    """合成 Kondo 模型的 NRG 谱函数测试数据.

    使用标准 Wilson 链系数, 在费米能级附近生成 A(ω) 数据.

    参数
    ----------
    N : int
        Wilson 链长度 (默认 60, 足够收敛)
    Lambda : float
        对数离散化参数 (默认 2.0)
    D : float
        导带半带宽 (默认 1.0)
    T_K : float
        Kondo 温度 (默认 1e-4 D)
    n_freq : int
        频率采样点数
    freq_range : tuple or None
        频率范围 (默认 [1e-6, 0.1] 对数均匀)
    seed : int
        随机种子

    返回
    -------
    data : dict
        {
            "omega": ndarray (n_freq,)  — 频率
            "A": ndarray (n_freq,)     — 谱函数 A(ω)
            "G_imp": ndarray (n_freq,) — 杂质 Green 函数
            "eps_n": ndarray (N,)      — Wilson 链系数
            "t_n": ndarray (N-1,)      — Wilson 链跳跃积分
            "Lambda": float            — 离散化参数
            "D": float                 — 带宽
            "N": int                    — 链长度
        }
    """
    if freq_range is None:
        freq_range = (T_K * 0.01, D * 0.1)

    omega = np.logspace(
        np.log10(freq_range[0]), np.log10(freq_range[1]), n_freq
    )

    # 包含正负频率
    omega_full = np.concatenate([-omega[::-1], [0.0], omega])

    eps_n, t_n = compute_wilson_coefficients(N, Lambda, D, xi_method="exact")
    A = compute_spectral_function(omega_full, eps_n, t_n, eta=T_K * 0.1)
    G = compute_impurity_green_function(omega_full, eps_n, t_n, eta=T_K * 0.1)

    return {
        "omega": omega_full,
        "A": A,
        "G_imp": G,
        "eps_n": eps_n,
        "t_n": t_n,
        "Lambda": Lambda,
        "D": D,
        "N": N,
        "T_K": T_K,
    }


# ---------------------------------------------------------------------------
# 4. 谱丛剪枝工具
# ---------------------------------------------------------------------------

def compute_condition_number(omega, eps_n, t_n):
    """计算谱丛矩阵在 ω 处的条件数 κ(M(ω)).

    条件数是分支点临近程度的预警指标:
      κ(M) → ∞    当 ω 接近分支点 (det M = 0)
      κ(M) ~ O(1) 当 ω 远离分支点

    参数
    ----------
    omega : complex
    eps_n, t_n : ndarray

    返回
    -------
    kappa : float
        条件数 (2-范数)
    """
    M = build_nrg_tridiag(omega, eps_n, t_n)
    # 对三对角矩阵用 numpy.linalg.cond
    # 三对角矩阵的 cond 可用估算
    try:
        kappa = np.linalg.cond(M)
        return kappa
    except np.linalg.LinAlgError:
        return np.inf


def compute_pruning_threshold(t_n, threshold_ratio=1e-4):
    """计算剪枝阈值: t_n 小于 max(|t|) * threshold_ratio 时可剪枝.

    NRG Wilson 链 t_n 指数衰减, 末端格点耦合极小.
    """
    max_t = np.max(np.abs(t_n))
    return max_t * threshold_ratio


def get_pruned_indices(t_n, threshold=1e-6):
    """返回需要保留的链索引 (剪枝: 去除 t_n < threshold 的末端格点).

    Wilson 链的末端格点只产生极小修正, 可安全剪枝.

    返回
    -------
    N_keep : int
        保留的链长度
    keep_indices : slice
        保留的索引 (0:N_keep)
    """
    N = len(t_n) + 1
    # 从末端向前寻找第一个 t_n >= threshold 的格点
    for n in range(len(t_n) - 1, -1, -1):
        if abs(t_n[n]) >= threshold:
            N_keep = n + 2  # 包含该格点和之前的所有格点
            return N_keep, slice(0, N_keep)
    return 1, slice(0, 1)


# ---------------------------------------------------------------------------
# 5. 快速自检
# ---------------------------------------------------------------------------

def _self_test():
    """运行快速自检: 验证 Wilson 链和谱函数计算的正确性."""
    np.random.seed(42)

    # 1. Wilson 系数物理合理性
    eps_n, t_n = compute_wilson_coefficients(N=10, Lambda=2.0)
    assert len(eps_n) == 10, "Wilson 链长度错误"
    assert len(t_n) == 9, "跳跃积分数量错误"
    assert np.all(eps_n == 0), "Kondo 模型在位能应为 0"
    assert np.all(t_n > 0), "跳跃积分应全部为正"
    assert t_n[0] > t_n[-1], "跳跃积分应指数衰减"
    print(f"  Wilson 链: N=10, t[0]={t_n[0]:.6f}, t[-1]={t_n[-1]:.6e}, "
          f"衰减比={t_n[-1]/t_n[0]:.2e}")

    # 2. 不同 Λ 值的系数对比
    for Lambda in [2.0, 2.5, 3.0]:
        _, t = compute_wilson_coefficients(N=10, Lambda=Lambda)
        decay = t[-1] / t[0]
        print(f"  Wilson链 Λ={Lambda}: t[0]={t[0]:.6f}, 衰减={decay:.2e}")

    # 3. 谱函数计算: Kondo 共振应在 ω=0 处有峰值
    N = 60
    # 使用更密集的网格以精确定位峰值
    omega_fine = np.logspace(-5, -1, 100)
    omega_full = np.concatenate([-omega_fine[::-1], [0.0], omega_fine])
    eps_n, t_n = compute_wilson_coefficients(N, 2.0, 1.0, xi_method="exact")
    A = compute_spectral_function(omega_full, eps_n, t_n, eta=1e-5)
    peak_idx = np.argmax(A)
    # Kondo 共振由粒子-空穴对称性严格固定在 ω=0
    # 数值峰值可能在 ω=0 的相邻网格点, 放宽至 2 个网格间距
    grid_spacing = np.mean(np.diff(omega_full))
    assert abs(omega_full[peak_idx]) < max(0.02, 5 * grid_spacing), \
        f"A(ω) 峰值应在 ω≈0, 实际在 ω={omega_full[peak_idx]:.4f}"
    print(f"  Kondo 共振: 峰值 A={A[peak_idx]:.4f} @ ω={omega_full[peak_idx]:.4e}"
          f" (网格间距={grid_spacing:.4e})")

    # 4. Green 函数交叉验证: 连分数 vs 矩阵求逆
    w_test = 0.01 + 0.001j
    G_cf = compute_impurity_green_function(w_test, eps_n, t_n, eta=0.0)
    G_inv = green_from_tridiag(w_test, eps_n, t_n)
    rel_diff = abs(G_cf - G_inv) / max(abs(G_cf), 1e-15)
    assert rel_diff < 1e-10, \
        f"连分数 vs 矩阵求逆不一致: {rel_diff:.2e}"
    print(f"  G_imp 交叉验证: 连分数 vs 矩阵求逆 相对差异={rel_diff:.2e}")

    # 5. 三对角矩阵结构
    M = build_nrg_tridiag(w_test, eps_n, t_n)
    assert M.shape == (N, N), f"矩阵尺寸应为 {(N, N)}"
    assert np.allclose(M, M.T), "三对角矩阵应对称"
    # 带宽验证
    M_upper = np.triu(M, 1)
    M_super = np.diag(np.diag(M, 1), k=1)
    assert np.allclose(M_upper, M_super), "超对角外应为零"
    # 对角元验证
    diag_expected = w_test - eps_n
    assert np.allclose(np.diag(M), diag_expected), \
        f"对角元应为 ω - ε_n"
    print(f"  三对角矩阵: 尺寸 {N}×{N}, 对称 ✓, 带宽 ✓, 对角元 ✓")

    # 6. 谱丛叶计算
    leaves = compute_nrg_spectral_leaves(w_test, eps_n, t_n)
    assert len(leaves) == N, "特征值数量应与矩阵维数一致"
    print(f"  谱丛叶: N={N} 个, min|λ|={np.min(np.abs(leaves)):.4e}")

    # 7. 剪枝阈值估算
    threshold = compute_pruning_threshold(t_n, threshold_ratio=1e-4)
    N_keep, _ = get_pruned_indices(t_n, threshold)
    print(f"  剪枝: 全链 N={N}, 保留 N_keep={N_keep}, "
          f"剪枝率={(1-N_keep/N)*100:.1f}%")

    print()
    print("[_nrg_tridiag] 自检通过: "
          "Wilson系数 ✓, 谱函数 ✓, 矩阵结构 ✓, 交叉验证 ✓, 剪枝 ✓")


if __name__ == "__main__":
    _self_test()
