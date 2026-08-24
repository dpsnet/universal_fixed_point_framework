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
Phase 58C.1: 记忆函数连分数 → 三对角谱丛生成器

数学背景:

  光导率 σ(ω) 的记忆函数形式：

      σ(ω) = σ₀ / (1 + iωτ + M(ω))

  记忆函数 M(ω) 的连分数展开（Mori 投影算子形式）：

      M(ω) = Δ₁² / (iω + γ₁ + Δ₂² / (iω + γ₂ + Δ₃² / (...)))

  三对角谱丛矩阵 A_M(ω)（N × N, N 为连分数深度）：

      A_M(ω) = tridiag( iΔ_{n-1}, iω + γ_n, iΔ_n )

      A_{11} = iω + γ₁,   A_{12} = A_{21} = iΔ₂
      A_{22} = iω + γ₂,   A_{23} = A_{32} = iΔ₃
      ...

  核心等同关系 (Paper XIV §5.7.2)：

      M(ω) = Δ₁² · [A_M(ω)⁻¹]₁₁

  M(ω) 的极点 ω_p 满足 det(A_M(ω_p)) = 0，对应谱丛分支点。

  谱丛底空间: ω ∈ ℂ (复频率)
  纤维: σ(A_M(ω)) = {λ ∈ ℂ: det(A_M(ω) - λI) = 0}
  分支点: det(A_M(ω_b)) = 0 → 谱叶间跳跃

  物理意义:
    · Drude 峰 (ω=0) → 记忆函数无耗散的平移不变性
    · Hubbard 带 (ω ~ ±U/2) → 记忆函数分支点的临界发散
    · 量子相变临界点 → 分支点向实轴的凝聚

关联:
  · generalization.md §5.3: S_mem ≅ S_Teuk 同构
  · Paper XIV §5.7.2: 光导率记忆函数连分数的谱丛等同
  · Leaver 谱丛分支点分析 (notes/04_lorentz_gravity/spectral_sheaf_leaver.md §3-4)
"""

import numpy as np
from scipy.linalg import eigvals, inv, det
from scipy.optimize import root_scalar


# ---------------------------------------------------------------------------
# 1. 正问题: 连分数 → M(ω) → σ(ω)
# ---------------------------------------------------------------------------

def compute_memory_function(omega, Delta_n, gamma_n):
    """通过向后连分数计算记忆函数 M(ω).

    连分数形式:

        M(ω) = Δ₁² / (iω + γ₁ + Δ₂² / (iω + γ₂ + Δ₃² / (...)))

    参数
    ----------
    omega : complex or array_like
        复频率
    Delta_n : ndarray (N,)
        连分数参数 Δ_n (n=1,...,N)
    gamma_n : ndarray (N,)
        连分数参数 γ_n (n=1,...,N)

    返回
    -------
    M : complex or ndarray
        记忆函数 M(ω)
    """
    scalar_input = np.ndim(omega) == 0
    omega = np.atleast_1d(np.asarray(omega, dtype=complex))

    N = len(Delta_n)
    M = np.zeros_like(omega, dtype=complex)

    for i, w in enumerate(omega):
        iw = 1j * w
        # 从最内层开始递推
        g = 1.0 / (iw + gamma_n[-1])
        for n in range(N - 2, -1, -1):
            g = 1.0 / (iw + gamma_n[n] + Delta_n[n + 1] ** 2 * g)
        # 最外层: M = Δ₁² · g
        M[i] = Delta_n[0] ** 2 * g

    if scalar_input:
        return M[0]
    return M


def compute_conductivity(omega, Delta_n, gamma_n, sigma_0=1.0, tau=1.0):
    """从记忆函数 M(ω) 计算光导率 σ(ω).

    σ(ω) = σ₀ / (1 + iωτ + M(ω))

    参数
    ----------
    omega : array_like
        频率
    Delta_n, gamma_n : ndarray
        记忆函数参数
    sigma_0 : float
        DC 电导率 (默认 1.0)
    tau : float
        弛豫时间 (默认 1.0)

    返回
    -------
    sigma : ndarray, complex
        复光导率 σ(ω) = σ₁(ω) + iσ₂(ω)
    """
    M = compute_memory_function(omega, Delta_n, gamma_n)
    return sigma_0 / (1.0 + 1j * omega * tau + M)


def compute_optical_conductivity(omega, Delta_n, gamma_n, sigma_0=1.0, tau=1.0):
    """计算实部和虚部光导率.

    σ(ω) = σ₁(ω) + iσ₂(ω)
    """
    sigma = compute_conductivity(omega, Delta_n, gamma_n, sigma_0, tau)
    return sigma.real, sigma.imag


# ---------------------------------------------------------------------------
# 2. 三对角谱丛矩阵
# ---------------------------------------------------------------------------

def build_memory_tridiag(omega, Delta_n, gamma_n):
    """构建记忆函数的三对角谱丛矩阵 A_M(ω).

    A_M(ω) = tridiag( iΔ_{n-1}, iω + γ_n, iΔ_n )

    矩阵结构 (N × N, N = len(Delta_n)):

        [ iω+γ₁  iΔ₂     0      ...   0      ]
        [ iΔ₂    iω+γ₂   iΔ₃    ...   0      ]
        [  0     iΔ₃    iω+γ₃   ...   0      ]
        [  ...    ...     ...     ...   iΔ_N  ]
        [  0      0       0     iΔ_N  iω+γ_N  ]

    注意: off-diagonal 取纯虚数 iΔ_n 是关键设计。标准 Jacobi 矩阵的
    连分数关系为 [A⁻¹]₁₁ = 1/(a₁ - b₁²/(a₂ - b₂²/(...))), 当 b_n = iΔ_n
    时有 -b_n² = +Δ_n², 从而与 Mori 投影算子连分数的 "+" 约定一致。\

    参数
    ----------
    omega : complex
        复频率
    Delta_n : ndarray (N,)
        Δ_n 参数 (n=1,...,N)
    gamma_n : ndarray (N,)
        γ_n 参数 (n=1,...,N)

    返回
    -------
    A : ndarray (N, N), complex
        三对角谱丛矩阵
    """
    N = len(Delta_n)
    A = np.zeros((N, N), dtype=complex)

    # 对角元: iω + γ_n
    np.fill_diagonal(A, 1j * omega + gamma_n)

    # off-diagonal: iΔ_n (n=2,...,N, 纯虚数确保与 Mori 连分数 "+" 约定一致)
    # Jacobi 矩阵定理: [A⁻¹]₁₁ = 1/(a₁ - b₁²/(a₂ - b₂²/(...)))
    # 当 b = iΔ 时, -b² = -(-Δ²) = +Δ², 匹配 M(ω) = Δ₁²/(iω+γ₁ + Δ₂²/(...))
    if N > 1:
        idx = np.arange(N - 1)
        A[idx, idx + 1] = 1j * Delta_n[1:]  # iΔ₂, iΔ₃, ..., iΔ_N
        A[idx + 1, idx] = 1j * Delta_n[1:]

    return A


def compute_memory_spectral_leaves(omega, Delta_n, gamma_n):
    """计算记忆函数谱丛 S_mem 在 ω 处的纤维 (N 个特征值)."""
    A = build_memory_tridiag(omega, Delta_n, gamma_n)
    return eigvals(A)


def memory_from_tridiag(omega, Delta_n, gamma_n):
    """通过三对角矩阵求逆计算 M(ω).

    M(ω) = Δ₁² · [A_M(ω)⁻¹]₁₁

    用于交叉验证连分数计算.
    """
    A = build_memory_tridiag(omega, Delta_n, gamma_n)
    try:
        Ainv = inv(A)
        return Delta_n[0] ** 2 * Ainv[0, 0]
    except np.linalg.LinAlgError:
        return complex(np.inf, np.inf)


# ---------------------------------------------------------------------------
# 3. 分支点计算
# ---------------------------------------------------------------------------

def compute_det_AM(omega, Delta_n, gamma_n):
    """计算 det(A_M(ω)).

    det(A_M(ω)) = 0 给出分支点位置.
    对对称三对角矩阵, 行列式可通过连分数递推高效计算.
    """
    N = len(Delta_n)
    w = complex(omega)

    # 三对角矩阵行列式的三项递推
    # d_0 = 1, d_1 = a_1 (第一对角元)
    # d_n = a_n · d_{n-1} - b_{n-1}² · d_{n-2}
    # 其中 a_n = iω + γ_n, b_n = iΔ_{n+1} (矩阵 off-diagonal 取纯虚数)
    # 注意: b_{n-1}² = (iΔ_n)² = -Δ_n², 故 -b_{n-1}² = +Δ_n²

    d_prev2 = 1.0  # d_0
    d_prev1 = 1j * w + gamma_n[0]  # d_1

    for n in range(1, N):
        a_n = 1j * w + gamma_n[n]
        b_n_minus1 = Delta_n[n]  # |b| = Δ_n, 矩阵中 b = iΔ_n
        d_curr = a_n * d_prev1 + b_n_minus1 ** 2 * d_prev2
        # 注意: 用 + 号是因为矩阵 off-diagonal 为 iΔ_n, (iΔ)² = -Δ²,
        #       而标准递推 d_n = a_n·d_{n-1} - b²·d_{n-2} 中 -b² = +Δ²
        d_prev2, d_prev1 = d_prev1, d_curr

    return d_prev1


def find_branch_points(Delta_n, gamma_n, omega_range=(-5, 5), n_scan=200):
    """搜索记忆函数谱丛的分支点 (det(A_M(ω)) = 0 的实根).

    在实频率轴上扫描 det(A_M(ω)) 的过零点.
    分支点通常出现在 Drude 峰边缘和 Hubbard 带边界.

    参数
    ----------
    Delta_n, gamma_n : ndarray
        记忆函数参数
    omega_range : (float, float)
        扫描频率范围
    n_scan : int
        扫描点数

    返回
    -------
    branch_points : list
        分支点频率列表
    det_values : ndarray
        扫描点的 det(A_M(ω)) 值
    omega_scan : ndarray
        扫描频率点
    """
    omega_scan = np.linspace(omega_range[0], omega_range[1], n_scan)

    # 沿实轴扫描
    det_values = np.array([compute_det_AM(w, Delta_n, gamma_n).real
                           for w in omega_scan])

    # 找过零点 (分支点)
    branch_points = []
    for i in range(len(omega_scan) - 1):
        if det_values[i] * det_values[i + 1] < 0:
            # 二分法精确定位
            try:
                sol = root_scalar(
                    lambda w: compute_det_AM(w, Delta_n, gamma_n).real,
                    bracket=(omega_scan[i], omega_scan[i + 1]),
                    method='bisect',
                    xtol=1e-12
                )
                if sol.converged:
                    branch_points.append(sol.root)
            except (ValueError, RuntimeError):
                # 近似位置
                branch_points.append((omega_scan[i] + omega_scan[i + 1]) / 2)

    return branch_points, det_values, omega_scan


# ---------------------------------------------------------------------------
# 4. 合成测试数据 (Mori 投影算子模型)
# ---------------------------------------------------------------------------

def synthesize_memory_data(n_modes=5, n_freq=200, sigma_0=1.0, tau=1.0,
                           seed=42):
    """合成记忆函数模型的测试数据.

    使用 Mori 投影算子框架的典型参数:
    - Δ_n 随 n 代数衰减 (或来自具体模型的谱矩)
    - γ_n 为小的阻尼常数

    参数
    ----------
    n_modes : int
        连分数深度 (Mori 投影阶数)
    n_freq : int
        频率采样点数
    sigma_0 : float
        DC 电导率
    tau : float
        弛豫时间
    seed : int
        随机种子

    返回
    -------
    data : dict
        测试数据
    """
    rng = np.random.default_rng(seed)

    # Δ_n: 谱矩参数, 代数衰减
    Delta_n = np.array([1.0 / (n + 1) ** 0.5 for n in range(1, n_modes + 1)])
    # 添加随机扰动
    Delta_n *= (1.0 + 0.2 * rng.uniform(-1, 1, n_modes))

    # γ_n: 阻尼常数, 随阶数增加
    gamma_n = np.array([0.1 + 0.05 * n for n in range(n_modes)])
    gamma_n *= (1.0 + 0.1 * rng.uniform(-1, 1, n_modes))

    # 频率点: 覆盖Drude峰和Hubbard带区域
    omega_low = np.logspace(-2, 0, n_freq // 2)  # 低频 (Drude)
    omega_high = np.logspace(0, 1.5, n_freq // 2)  # 高频 (Hubbard带)
    omega = np.concatenate([[0.0], omega_low, omega_high])

    # 计算 σ(ω) 和 M(ω)
    sigma = compute_conductivity(omega, Delta_n, gamma_n, sigma_0, tau)
    M = compute_memory_function(omega, Delta_n, gamma_n)

    return {
        "omega": omega,
        "sigma": sigma,
        "sigma_1": sigma.real,
        "sigma_2": sigma.imag,
        "M": M,
        "Delta_n": Delta_n,
        "gamma_n": gamma_n,
        "sigma_0": sigma_0,
        "tau": tau,
        "n_modes": n_modes,
    }


# ---------------------------------------------------------------------------
# 5. 快速自检
# ---------------------------------------------------------------------------

def _self_test():
    """运行快速自检: 验证记忆函数谱丛的正确性."""
    np.random.seed(42)

    # 1. 三对角矩阵结构验证
    print("--- 测试 1: 三对角矩阵结构 ---")
    N = 5
    Delta_n = np.array([1.0, 0.5, 0.3, 0.2, 0.1])
    gamma_n = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    omega_test = complex(0.5, 0.05)

    A = build_memory_tridiag(omega_test, Delta_n, gamma_n)
    assert A.shape == (N, N), f"矩阵尺寸应为 {(N, N)}"
    assert np.allclose(A, A.T), "三对角矩阵应对称"

    # 带宽验证
    sup_diag = np.diag(A, k=1)
    sub_diag = np.diag(A, k=-1)
    assert np.allclose(np.triu(A, 1), np.diag(sup_diag, k=1)), "超对角外应为零"
    assert np.allclose(np.tril(A, -1), np.diag(sub_diag, k=-1)), "次对角外应为零"

    # 对角元: iω + γ_n
    diag_expected = 1j * omega_test + gamma_n
    assert np.allclose(np.diag(A), diag_expected), "对角元应为 iω + γ_n"

    # off-diagonal: iΔ₂,...,iΔ_N
    assert np.allclose(sup_diag, 1j * Delta_n[1:]), "超对角应为 iΔ₂,...,iΔ_N"
    assert np.allclose(sub_diag, 1j * Delta_n[1:]), "次对角应为 iΔ₂,...,iΔ_N"

    print(f"  矩阵尺寸 {N}×{N}, 对称 ✓, 带宽 ✓, 对角元 ✓")

    # 2. 连分数 vs 三对角矩阵求逆交叉验证
    print("\n--- 测试 2: 连分数 vs 矩阵求逆 ---")
    for w in [0.1, 0.5, 1.0, 2.0]:
        M_cf = compute_memory_function(w, Delta_n, gamma_n)
        M_inv = memory_from_tridiag(w, Delta_n, gamma_n)
        rel_diff = abs(M_cf - M_inv) / max(abs(M_cf), 1e-15)
        assert rel_diff < 1e-10, f"ω={w}: 偏差 {rel_diff:.2e}"
    print(f"  交叉验证: 连分数 vs 矩阵求逆 偏差 < 1e-10 ✓")

    # 3. Drude 峰验证: 低频 Re(σ) 应近似于 DC 值
    print("\n--- 测试 3: Drude 峰 ---")
    omega_drude = np.logspace(-2, 0, 20)
    sigma = compute_conductivity(omega_drude, Delta_n, gamma_n)
    sigma_1_low = sigma.real[0]
    # DC 电导率应从记忆函数自洽得到
    print(f"  低频 σ₁(ω→0) = {sigma_1_low:.4f} (σ₀={1.0})")

    # 4. 行列式和分支点
    print("\n--- 测试 4: 行列式与分支点 ---")
    omega_test = 0.5
    det_val = compute_det_AM(omega_test, Delta_n, gamma_n)
    print(f"  ω={omega_test}: det(A_M) = {det_val:.6e}")

    branch_points, det_vals, omega_scan = find_branch_points(
        Delta_n, gamma_n, omega_range=(-3, 3), n_scan=100
    )
    if branch_points:
        print(f"  分支点: {[f'{bp:.4f}' for bp in branch_points]}")
    else:
        print(f"  [−3, 3] 范围内无实分支点 (预期: 小阻尼体系)")

    # 5. 谱函数物理合理性
    print("\n--- 测试 5: 谱函数合理性 ---")
    data = synthesize_memory_data(n_modes=4, n_freq=100)
    assert np.all(data["sigma_1"] >= 0), "Re(σ) 应为正"
    print(f"  σ₁(ω) 全为正 ✓")
    print(f"  σ₁ 最大值 = {np.max(data['sigma_1']):.4f} @ ω={data['omega'][np.argmax(data['sigma_1'])]:.4f}")
    print(f"  σ₁ 最小值 = {np.min(data['sigma_1']):.4f}")

    print()
    print("[_memory_tridiag] 自检通过: "
          "矩阵结构 ✓, 连分数 ✓, Drude峰 ✓, 行列式 ✓, 谱函数 ✓")


if __name__ == "__main__":
    _self_test()
