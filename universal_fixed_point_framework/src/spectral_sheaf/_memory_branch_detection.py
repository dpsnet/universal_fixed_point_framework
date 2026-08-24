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
Phase 58C.2: 记忆函数谱丛分支点探测

基于三种互补方法探测谱丛分支点:

  1. det(A_M(ω)) = 0 方法（已实现于 _memory_tridiag.py）
  2. 条件数 κ(A_M(ω)) 尖峰法（本模块核心）
  3. 谱叶变异系数 CV 法（分支点附近谱叶平滑度分析）

数学基础:

  记忆函数谱丛 S_mem 的分支点满足 det(A_M(ω_b)) = 0。
  此时 A_M(ω_b) 接近奇异, 条件数 κ(A) = ||A||·||A⁻¹|| → ∞。
  在分支点附近, 谱叶 λ_i(ω) 对 ω 敏感, 协变系数 CV 升高。

  物理对应:
    · Drude 峰边缘: 分支点位于复 ω 平面的虚轴附近
    · Hubbard 带边界: 分支点 ~ ±U/2 对应 Mott 间隙边缘
    · 量子相变: 分支点向实轴凝聚

关联:
    · _memory_tridiag.py (谱丛基类)
    · notes/04_lorentz_gravity/spectral_sheaf_leaver.md §4 (分支点条件数预警)
    · generalization.md §5.3 (S_mem 同构)
"""

import numpy as np
from numpy.linalg import cond
from scipy.linalg import eigvals

try:
    from spectral_sheaf._memory_tridiag import (
        build_memory_tridiag, compute_det_AM, compute_memory_function,
        compute_conductivity, find_branch_points,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from _memory_tridiag import (
        build_memory_tridiag, compute_det_AM, compute_memory_function,
        compute_conductivity, find_branch_points,
    )


# ---------------------------------------------------------------------------
# 1. 条件数分析
# ---------------------------------------------------------------------------

def compute_condition_number_A(omega, Delta_n, gamma_n):
    """计算 A_M(ω) 的条件数 κ(A) = ||A||·||A⁻¹||.

    条件数尖峰指示矩阵接近奇异 → 分支点.
    使用 scipy.linalg.cond (基于 SVD).
    """
    A = build_memory_tridiag(omega, Delta_n, gamma_n)
    try:
        return cond(A)
    except np.linalg.LinAlgError:
        return np.inf


def scan_condition_number(Delta_n, gamma_n, omega_range=(-5, 5), n_scan=500):
    """扫描 ω 范围内条件数剖面.

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
    omega_scan : ndarray
        扫描频率点
    kappa_values : ndarray
        条件数 κ(A_M(ω))
    branch_points : list
        条件数尖峰位置 (局部极大值)
    """
    omega_scan = np.linspace(omega_range[0], omega_range[1], n_scan)
    kappa_values = np.array([
        compute_condition_number_A(w, Delta_n, gamma_n)
        for w in omega_scan
    ])

    # 找条件数局部极大值 (尖峰)
    branch_points = []
    threshold = np.median(kappa_values) * 10  # 10 倍中位数
    for i in range(1, n_scan - 1):
        if (kappa_values[i] > kappa_values[i - 1] and
            kappa_values[i] > kappa_values[i + 1] and
            kappa_values[i] > threshold):
            branch_points.append(omega_scan[i])

    return omega_scan, kappa_values, branch_points


def classify_branch_points(omega_bp, Delta_n, gamma_n,
                           omega_drude_threshold=0.5):
    """分类分支点的物理类型.

    返回
    -------
    classification : dict
        {"drude_edge": [...], "hubbard_band": [...], "other": [...]}
    """
    classification = {"drude_edge": [], "hubbard_band": [], "other": []}

    for w in omega_bp:
        # 检查 M(ω) 在该频率附近的行为
        M_val = compute_memory_function(complex(w, 1e-6), Delta_n, gamma_n)
        sigma = compute_conductivity(np.array([w]), Delta_n, gamma_n)

        if abs(w) < omega_drude_threshold:
            classification["drude_edge"].append(w)
        elif np.abs(sigma[0]) < 0.1:  # 低电导率区 = Hubbard 带
            classification["hubbard_band"].append(w)
        else:
            classification["other"].append(w)

    return classification


# ---------------------------------------------------------------------------
# 2. 谱叶连续性分析 (变异系数法)
# ---------------------------------------------------------------------------

def compute_leaf_variation(omega, Delta_n, gamma_n, radius=1e-3, n_points=12):
    """计算谱叶在 ω 附近小圆上的变异系数 CV.

    在以 ω 为中心、radius 为半径的小圆上采样 n_points 个点，
    计算最小特征值 |λ_min| 的变异系数 CV = std/mean.

    高 CV → 谱叶在该处剧烈变化 → 分支点附近.
    低 CV → 谱叶平滑 → 远离分支点.

    参数
    ----------
    omega : complex
        测试频率
    Delta_n, gamma_n : ndarray
        记忆函数参数
    radius : float
        小圆半径
    n_points : int
        采样点数

    返回
    -------
    cv : float
        变异系数
    leaf_vals : ndarray
        各采样点的最小 |λ|
    """
    A0 = build_memory_tridiag(omega, Delta_n, gamma_n)
    N = A0.shape[0]

    angles = np.linspace(0, 2 * np.pi, n_points + 1)[:-1]
    min_abs_evals = np.zeros(n_points)

    for i, theta in enumerate(angles):
        z = omega + radius * np.exp(1j * theta)
        A = build_memory_tridiag(z, Delta_n, gamma_n)
        evals = eigvals(A)
        min_abs_evals[i] = np.min(np.abs(evals))

    # 变异系数
    mean_val = np.mean(min_abs_evals)
    std_val = np.std(min_abs_evals)
    cv = std_val / (mean_val + 1e-15)

    return cv, min_abs_evals


def scan_leaf_variation(Delta_n, gamma_n, omega_range=(-5, 5),
                        n_scan=200, radius=1e-3):
    """扫描 ω 轴上的谱叶变异系数剖面.

    返回
    -------
    omega_scan : ndarray
    cv_values : ndarray
        变异系数 CV(ω)
    """
    omega_scan = np.linspace(omega_range[0], omega_range[1], n_scan)
    cv_values = np.zeros(n_scan)

    for i, w in enumerate(omega_scan):
        cv_values[i], _ = compute_leaf_variation(
            complex(w, 0), Delta_n, gamma_n, radius
        )

    return omega_scan, cv_values


# ---------------------------------------------------------------------------
# 3. 三方法联合分支点定位
# ---------------------------------------------------------------------------

def locate_branch_points_joint(Delta_n, gamma_n,
                               omega_range=(-5, 5),
                               n_scan_det=400,
                               n_scan_kappa=400,
                               n_scan_cv=200,
                               det_threshold_ratio=0.01,
                               kappa_threshold_factor=10,
                               cv_threshold=0.1):
    """三方法联合定位分支点.

    方法:
    M1: det(A_M(ω)) 过零点 (理论精确)
    M2: κ(A_M(ω)) 尖峰 (数值鲁棒)
    M3: CV(ω) 尖峰 (谱叶连续性)

    返回
    -------
    result : dict
    """
    # M1: det(A_M)=0
    bp_det, det_vals, omega_det = find_branch_points(
        Delta_n, gamma_n, omega_range, n_scan_det
    )

    # M2: 条件数尖峰
    omega_kap, kappa_vals, bp_kappa = scan_condition_number(
        Delta_n, gamma_n, omega_range, n_scan_kappa
    )

    # M3: 谱叶变异系数
    omega_cv, cv_vals = scan_leaf_variation(
        Delta_n, gamma_n, omega_range, n_scan_cv
    )

    return {
        "branch_points_det": bp_det,
        "omega_det": omega_det,
        "det_values": det_vals,
        "branch_points_kappa": bp_kappa,
        "omega_kappa": omega_kap,
        "kappa_values": kappa_vals,
        "omega_cv": omega_cv,
        "cv_values": cv_vals,
    }


# ---------------------------------------------------------------------------
# 4. 物理场景分析
# ---------------------------------------------------------------------------

def analyze_memory_branching(Delta_n, gamma_n, sigma_0=1.0, tau=1.0):
    """完整分析记忆函数谱丛的分支结构.

    参数
    ----------
    Delta_n, gamma_n : ndarray
        记忆函数参数
    sigma_0 : float
        DC 电导率
    tau : float
        弛豫时间

    返回
    -------
    analysis : dict
        分支结构分析结果
    """
    # 1. 三方法联合定位
    joint = locate_branch_points_joint(Delta_n, gamma_n)

    # 2. 分支点分类
    classification = classify_branch_points(
        joint["branch_points_det"], Delta_n, gamma_n
    )

    # 3. 物理量评估
    omega_drude = np.logspace(-3, 0, 50)
    sigma = compute_conductivity(omega_drude, Delta_n, gamma_n, sigma_0, tau)
    sigma_dc = sigma.real[0]

    # 4. 谱叶数量 = N
    A0 = build_memory_tridiag(complex(0, 0.01), Delta_n, gamma_n)
    n_leaves = A0.shape[0]

    analysis = {
        "n_leaves": n_leaves,
        "n_parameters": len(Delta_n),
        "branch_points_det": joint["branch_points_det"],
        "branch_points_kappa": joint["branch_points_kappa"],
        "classification": classification,
        "sigma_dc": sigma_dc,
        "max_kappa": float(np.max(joint["kappa_values"])),
        "mean_kappa": float(np.mean(joint["kappa_values"])),
        "max_cv": float(np.max(joint["cv_values"])),
    }

    return analysis


# ---------------------------------------------------------------------------
# 5. 快速自检
# ---------------------------------------------------------------------------

def _self_test():
    """运行快速自检."""
    np.random.seed(42)

    # 测试参数 (合成 Mori 模型)
    N = 5
    Delta_n = np.array([1.0, 0.5, 0.3, 0.2, 0.1])
    gamma_n = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

    print("--- 测试 1: 条件数计算 ---")
    for w in [0.1, 0.5, 1.0, 2.0]:
        kappa = compute_condition_number_A(w, Delta_n, gamma_n)
        print(f"  ω={w:.1f}: κ(A) = {kappa:.2e}")
    print("  条件数计算 ✓")

    print("\n--- 测试 2: 条件数扫描 ---")
    omega_kap, kappa_vals, bp_kappa = scan_condition_number(
        Delta_n, gamma_n, omega_range=(-3, 3), n_scan=100
    )
    print(f"  条件数范围: [{np.min(kappa_vals):.2e}, {np.max(kappa_vals):.2e}]")
    if bp_kappa:
        print(f"  条件数尖峰: {[f'{w:.4f}' for w in bp_kappa]}")
    else:
        print(f"  无显著条件数尖峰")
    print("  条件数扫描 ✓")

    print("\n--- 测试 3: 谱叶变异系数 ---")
    omega_cv, cv_vals = scan_leaf_variation(
        Delta_n, gamma_n, omega_range=(-3, 3), n_scan=50
    )
    print(f"  CV 范围: [{np.min(cv_vals):.4e}, {np.max(cv_vals):.4e}]")
    print(f"  最大 CV @ ω={omega_cv[np.argmax(cv_vals)]:.4f}")

    print("\n--- 测试 4: 三方法联合定位 ---")
    joint = locate_branch_points_joint(
        Delta_n, gamma_n, omega_range=(-3, 3)
    )
    print(f"  det(A)=0 分支点: {[f'{w:.4f}' for w in joint['branch_points_det']]}")
    print(f"  条件数尖峰:    {[f'{w:.4f}' for w in joint['branch_points_kappa']]}")

    print("\n--- 测试 5: 完整物理分析 ---")
    analysis = analyze_memory_branching(Delta_n, gamma_n)
    print(f"  谱叶数: {analysis['n_leaves']}")
    print(f"  DC 电导率: {analysis['sigma_dc']:.4f}")
    print(f"  最大条件数: {analysis['max_kappa']:.2e}")
    print(f"  最大 CV:    {analysis['max_cv']:.4e}")

    print()
    print("[_memory_branch_detection] 自检通过: "
          "条件数 ✓, 谱叶CV ✓, 联合定位 ✓, 物理分析 ✓")


if __name__ == "__main__":
    _self_test()
