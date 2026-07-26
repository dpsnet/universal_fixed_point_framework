"""
Phase 58A.1: 广义 Maxwell 模型 → 三对角矩阵生成器

数学背景:

  非牛顿流变学的复数剪切模量（广义 Maxwell 模型，GMM）：

      G*(ω) = G_e + Σ_{k=1}^N G_k · iω·τ_k / (1 + iω·τ_k)

  三对角谱丛矩阵 M(ω) 作为弛豫谱 {G_k, τ_k} 的结构编码：

      M_{kk}(ω) = 1 + iωτ_k                     (主对角元 — 弛豫时间)
      M_{k,k+1} = M_{k+1,k} = sqrt(G_k)         (off-diagonal — 模式耦合强度)

  注意：GMM 是求和形式，不直接等价于形如 α₀²/(β₀ + α₁²/(β₁ + ...))
        的连分数展开。三对角矩阵在此作为弛豫谱的结构编码，而非通过
        resolvent 与连分数精确对应。

  谱丛底空间: ω ∈ ℂ (复角频率)
  纤维: σ(M(ω)) = {λ ∈ ℂ: det(M(ω) - λI) = 0}
  截面: λ = 0 时对应弛豫模式的极点条件 det(M(ω)) = 0

关联:
  · generalization.md §5.1: S_Teuk ≅ S_rheo 同构（结构层）
  · Paper VI §9.3: 谱丛流变学
"""

import numpy as np
from scipy.linalg import eigvals


# ---------------------------------------------------------------------------
# 1. 正问题: GMM → G*(ω)
# ---------------------------------------------------------------------------

def compute_G_star(omega, G_i, tau_i, G_e=0.0):
    """计算广义 Maxwell 模型的复数剪切模量 G*(ω).

    参数
    ----------
    omega : array_like, shape (n_freq,)
        测试角频率 (rad/s)
    G_i : array_like, shape (n_modes,)
        各 Maxwell 单元的弹性模量 (Pa)
    tau_i : array_like, shape (n_modes,)
        各 Maxwell 单元的弛豫时间 (s)
    G_e : float, optional
        平衡（橡胶态）模量 (Pa), 默认 0

    返回
    -------
    G_star : ndarray, shape (n_freq,), complex
        G*(ω) = G' + iG''
    """
    omega = np.asarray(omega, dtype=complex)
    G_i = np.asarray(G_i, dtype=float)
    tau_i = np.asarray(tau_i, dtype=float)
    n_modes = len(G_i)

    result = np.full_like(omega, G_e, dtype=complex)
    for k in range(n_modes):
        iwt = 1j * omega * tau_i[k]
        result += G_i[k] * iwt / (1.0 + iwt)
    return result


def compute_Gp_Gpp(omega, G_i, tau_i, G_e=0.0):
    """计算储能模量 G' 和损耗模量 G''.

    G*(ω) = G'(ω) + iG''(ω)
    """
    Gs = compute_G_star(omega, G_i, tau_i, G_e)
    return Gs.real, Gs.imag


# ---------------------------------------------------------------------------
# 2. 三对角谱丛矩阵
# ---------------------------------------------------------------------------

def build_gmm_tridiag(omega, tau_i, alpha_i):
    """构建广义 Maxwell 模型的三对角谱丛矩阵 M(ω).

    矩阵结构 (N × N, N = len(tau_i)):

        M(ω) = tridiag( α_{k-1}, β_k, α_k )

        β_k(ω) = 1 + iωτ_k           (主对角 — 弛豫时间)
        α_k    = sqrt(G_k)            (off-diagonal — 模式耦合)

    性质:
        · M(ω) 是对称三对角矩阵
        · ω = i/τ_k 时 β_k = 0 (第 k 行无对角优势)
        · M(ω) 是 ω 的线性矩阵多项式: M₀ + ωM₁

    参数
    ----------
    omega : complex
        测试角频率
    tau_i : array_like, shape (N,)
        弛豫时间
    alpha_i : array_like, shape (N,)
        耦合系数 (α_k = sqrt(G_k))

    返回
    -------
    M : ndarray, shape (N, N), complex
        三对角矩阵
    """
    N = len(tau_i)
    beta = np.array([1.0 + 1j * omega * t for t in tau_i])
    a = np.array(alpha_i)

    M = np.zeros((N, N), dtype=complex)
    np.fill_diagonal(M, beta)
    if N > 1:
        idx = np.arange(N - 1)
        M[idx, idx + 1] = a[:-1]
        M[idx + 1, idx] = a[:-1]
    return M


def compute_spectral_leaves(omega, tau_i, alpha_i):
    """计算谱丛 S_rheo 在 ω 处的纤维 (N 个特征值).

    返回谱丛的 N 个叶 λ_i(ω), 即 M(ω) 的特征值.
    """
    M = build_gmm_tridiag(omega, tau_i, alpha_i)
    return eigvals(M)


# ---------------------------------------------------------------------------
# 3. 合成测试数据
# ---------------------------------------------------------------------------

def synthesize_rheo_data(n_modes=5, n_freq=100, noise_level=0.0,
                         tau_min=None, tau_max=None, seed=42):
    """合成广义 Maxwell 模型的 G*, G', G'' 测试数据.

    弛豫时间在 [tau_min, tau_max] 上对数均匀分布,
    模量 G_i 在 [0.5, 2.0] 上随机分布.

    参数
    ----------
    n_modes : int
        Maxwell 单元数 (默认 5)
    n_freq : int
        频率采样点数 (默认 100)
    noise_level : float
        添加的 Gaussian 噪声标准差 (默认 0 = 无噪声)
    tau_min, tau_max : float
        弛豫时间范围。若为 None，根据频率范围自动设置
        (tau_min = 1/omega_max × 0.1, tau_max = 1/omega_min × 10)
    seed : int
        随机种子

    返回
    -------
    data : dict
        {
            "omega": ndarray (n_freq,)   — 测试频率
            "G_star": ndarray (n_freq,)  — 复数模量
            "G_prime": ndarray (n_freq,) — 储能模量
            "G_prime2": ndarray (n_freq,)— 损耗模量
            "G_i": ndarray (n_modes,)    — 真实模量
            "tau_i": ndarray (n_modes,)  — 真实弛豫时间
            "G_e": float                 — 平衡模量
            "alpha_i": ndarray (n_modes,)— 耦合系数
        }
    """
    omega = np.logspace(-2, 2, n_freq)
    omega_max = np.max(omega)
    omega_min = np.min(omega)

    if tau_min is None:
        tau_min = 1.0 / omega_max * 0.1
    if tau_max is None:
        tau_max = 1.0 / omega_min * 10.0

    # 确保 n_modes >= 2 时 tau_min < tau_max
    if tau_min >= tau_max:
        tau_min, tau_max = 1.0 / omega_max, 1.0 / omega_min

    rng = np.random.default_rng(seed)
    tau_i = np.logspace(np.log10(tau_min), np.log10(tau_max), n_modes)
    G_i = rng.uniform(0.5, 2.0, n_modes)
    G_e = rng.uniform(0.0, 0.5)

    # 耦合系数: α_k = sqrt(G_k)
    alpha_i = np.sqrt(G_i)

    G_star = compute_G_star(omega, G_i, tau_i, G_e)

    if noise_level > 0:
        noise = noise_level * rng.normal(0, 1, n_freq)
        G_star += noise * (1.0 + 1.0j)

    return {
        "omega": omega,
        "G_star": G_star,
        "G_prime": G_star.real,
        "G_prime2": G_star.imag,
        "G_i": G_i,
        "tau_i": tau_i,
        "G_e": G_e,
        "alpha_i": alpha_i,
    }


# ---------------------------------------------------------------------------
# 4. 快速自检
# ---------------------------------------------------------------------------

def _self_test():
    """运行快速自检: 检查正问题物理合理性和矩阵结构."""
    data = synthesize_rheo_data(n_modes=3, n_freq=50, noise_level=0.0)
    Gs = data["G_star"]
    omega = data["omega"]

    # 1. 物理合理性: G'(ω) 单调增, G''(ω) 有峰值
    Gp, Gpp = Gs.real, Gs.imag
    assert np.all(np.diff(Gp) >= -1e-8), "G' 应单调增加"
    peak_idx = np.argmax(Gpp)
    assert 0 < peak_idx < len(Gpp) - 1, "G'' 应在中间有峰值"

    # 2. G' 应在理论上下界内
    G_low = Gp[0]
    G_high = Gp[-1]
    G_min = data["G_e"]
    G_max = data["G_e"] + np.sum(data["G_i"])
    assert G_low >= G_min - 1.0, f"低频 G'({G_low:.3f}) 异常"
    assert G_high <= G_max + 1.0, f"高频 G'({G_high:.3f}) 异常"

    # 3. 三对角矩阵结构验证
    M = build_gmm_tridiag(omega[len(omega)//2], data["tau_i"], data["alpha_i"])
    N = len(data["tau_i"])
    assert M.shape == (N, N), f"矩阵尺寸应为 {(N, N)}，实际 {M.shape}"
    # 对称性
    assert np.allclose(M, M.T), "三对角矩阵应对称"
    # 带宽: 超对角外应为零
    M_upper_tri = np.triu(M, 1)
    M_superdiag_only = np.diag(np.diag(M, 1), k=1)
    assert np.allclose(M_upper_tri, M_superdiag_only), \
        "超对角外应为零"
    # 次对角外应为零
    M_lower_tri = np.tril(M, -1)
    M_subdiag_only = np.diag(np.diag(M, -1), k=-1)
    assert np.allclose(M_lower_tri, M_subdiag_only), \
        "次对角外应为零"
    # 对角线元素
    beta_expected = 1.0 + 1j * omega[len(omega)//2] * data["tau_i"]
    assert np.allclose(np.diag(M), beta_expected), \
        "对角线元素应为 1 + iωτ_k"

    # 4. compute_G_star 直接计算验证 (正问题正确性)
    Gp_expected, Gpp_expected = compute_Gp_Gpp(omega, data["G_i"],
                                                data["tau_i"], data["G_e"])
    assert np.allclose(Gp, Gp_expected), "直接计算 G' 与函数计算应一致"
    assert np.allclose(Gpp, Gpp_expected), "直接计算 G'' 与函数计算应一致"

    print("[_rheo_to_tridiag] 自检通过: "
          "物理合理性 ✓, 矩阵结构 ✓, 正问题正确性 ✓")


if __name__ == "__main__":
    _self_test()
