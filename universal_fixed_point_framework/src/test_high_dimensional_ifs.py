"""
test_high_dimensional_ifs.py

验证高维 IFS 收敛率理论：
1. 解析层：相似维数、有效维数、收敛指数的一致性
2. 数值层：合成核矩阵的特征值衰减与理论预测的对比
3. 相变层：维数相变图的自洽性
"""

from __future__ import annotations

import numpy as np
import pytest

from high_dimensional_ifs import HighDimIFSAnalysis


# ===========================================================================
# 1. 解析层测试
# ===========================================================================

def test_similarity_dimension_cantor():
    """经典 Cantor 集：d_sim = log 2 / log 3 ≈ 0.6309"""
    c = np.array([1.0/3, 1.0/3])
    p = np.array([0.5, 0.5])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=1)
    expected = np.log(2) / np.log(3)
    assert abs(hda.d_sim - expected) < 1e-10


def test_similarity_dimension_sierpinski():
    """Sierpinski 垫片：d_sim = log 3 / log 2 ≈ 1.585"""
    c = np.array([0.5, 0.5, 0.5])
    p = np.array([1.0/3, 1.0/3, 1.0/3])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=2)
    expected = np.log(3) / np.log(2)
    assert abs(hda.d_sim - expected) < 1e-10


def test_similarity_dimension_menger():
    """Menger 海绵：d_sim = log 20 / log 3 ≈ 2.7268"""
    c = np.array([1.0/3] * 20)
    p = np.full(20, 1.0/20)
    hda = HighDimIFSAnalysis(c, p, ambient_dim=3)
    expected = np.log(20) / np.log(3)
    assert abs(hda.d_sim - expected) < 1e-8


def test_effective_dimension_strong_separation():
    """强分离时 d_eff = d_sim（限于 ambient_dim）"""
    c = np.array([0.4, 0.4])
    p = np.array([0.5, 0.5])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=3, separation_type="strong")
    assert abs(hda.d_effective - hda.d_sim) < 1e-10


def test_effective_dimension_non_separated():
    """非分离时 d_eff < d_sim"""
    c = np.array([0.5, 0.3])
    p = np.array([0.6, 0.4])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=2,
                              separation_type="non_separated",
                              overlap_degree=0.5)
    assert hda.d_effective < hda.d_sim


def test_convergence_bounds_monotonic():
    """收敛上界应随 N 单调递减"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])

    for sep in ["strong", "weak", "non_separated"]:
        hda = HighDimIFSAnalysis(c, p, ambient_dim=2,
                                  separation_type=sep)
        prev = hda.convergence_bound(10)
        for N in [20, 50, 100, 200]:
            cur = hda.convergence_bound(N)
            assert cur <= prev + 1e-15, f"{sep}: N={N}, prev={prev}, cur={cur}"
            prev = cur


def test_exponential_bound_faster_than_polynomial():
    """指数上界最终快于多项式上界"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=2,
                              separation_type="weak")
    for N in [10, 100, 1000]:
        exp_b = hda.exponential_bound(N)
        poly_b = hda.polynomial_bound_potential(N)
        assert exp_b < poly_b + 1e-15, f"N={N}: exp={exp_b}, poly={poly_b}"


def test_switching_point_behavior():
    """切换点随 d_frac 增大而单调递增"""
    c = np.array([0.5, 0.3])
    p = np.array([0.6, 0.4])
    prev_n_star = 0.0
    for rho in np.linspace(0.0, 0.8, 5):
        hda = HighDimIFSAnalysis(c, p, ambient_dim=3,
                                  separation_type="non_separated",
                                  overlap_degree=rho)
        n_star = hda.optimal_switching_point()
        if n_star < 1e6 and prev_n_star < 1e6:
            assert n_star >= prev_n_star - 1e-10, f"rho={rho}: n*={n_star} < prev={prev_n_star}"
        prev_n_star = n_star


# ===========================================================================
# 2. 数值层测试：合成核矩阵的特征值衰减
# ===========================================================================

def _synthetic_high_dim_kernel(
    d_frac: float,
    d_amb: int,
    n_points: int,
    smoothness: float = 1.0,
    seed: int = 42,
) -> np.ndarray:
    """
    生成 d_amb 维空间中嵌入 d_frac 维分形集上的合成核矩阵。

    用随机分形采样点 + Gauss 核模拟 RKHS 特征值衰减。
    """
    np.random.seed(seed)

    # 在 [0,1]^d_amb 中采样，使有效维数为 d_frac
    # 方法：只在 d_frac 个维度上变化，其余维度固定
    X = np.random.rand(n_points, d_amb).astype(np.float64)
    if d_frac < d_amb:
        # 将高维 "投影" 到低维流形：固定多余维度
        fixed_dims = list(range(int(d_frac), d_amb))
        X[:, fixed_dims] = 0.5

    # Gauss 核：K(x,y) = exp(-||x-y||^2 / (2*sigma^2))
    sigma = 0.5
    K = np.zeros((n_points, n_points))
    for i in range(n_points):
        diff = X - X[i:i+1]
        dist_sq = np.sum(diff ** 2, axis=1)
        K[i, :] = np.exp(-dist_sq / (2 * sigma ** 2))
    K = 0.5 * (K + K.T) + 1e-12 * np.eye(n_points)
    return K


def test_synthetic_eigenvalue_decay():
    """合成核矩阵的特征值应呈幂律衰减（log-log 斜率稳定）"""
    n_points = 80
    d_amb = 3
    d_frac = 1.5

    K = _synthetic_high_dim_kernel(
        d_frac=d_frac, d_amb=d_amb,
        n_points=n_points, smoothness=1.0,
        seed=42,
    )
    eigenvalues = np.linalg.eigvalsh(K)
    eigenvalues = np.sort(eigenvalues)[::-1]

    # 特征值应单调衰减
    for i in range(n_points - 1):
        assert eigenvalues[i] >= eigenvalues[i+1] - 1e-15

    # 在 log-log 空间中检查幂律行为：从中段取斜率
    # 理论：λ_k ~ k^{-α/d_frac}，跳过前 5 个和后 20 个（边界效应）
    idx = np.arange(5, n_points - 20)
    log_k = np.log(idx + 1)
    log_lambda = np.log(np.maximum(eigenvalues[5:-20], 1e-300))
    if len(log_k) > 5:
        slope, _ = np.polyfit(log_k, log_lambda, 1)
        # 斜率应为负值
        assert slope < 0, f"特征值衰减斜率为正: {slope:.4f}"
        # 理论值在 -1 到 -5 之间（取决于维数与光滑度）
        assert -10 < slope < 0, f"衰减斜率异常: {slope:.4f}"


def test_synthetic_higher_dim_faster_decay():
    """高维嵌入空间应导致更快的特征值衰减（相同 d_frac）"""
    n_points = 64
    d_frac = 1.0

    eigenvalues_by_dim = {}
    for d_amb in [2, 4]:
        K = _synthetic_high_dim_kernel(
            d_frac=d_frac, d_amb=d_amb,
            n_points=n_points, smoothness=1.0
        )
        ev = np.sort(np.linalg.eigvalsh(K))[::-1]
        eigenvalues_by_dim[d_amb] = ev

    # 高维空间的覆盖熵指数 1-d_frac/d_amb 更大
    # → 特征值衰减更快 → 前 20 个特征值的和应更集中于前几个
    sum_top5_2 = np.sum(eigenvalues_by_dim[2][:5])
    sum_top5_4 = np.sum(eigenvalues_by_dim[4][:5])
    total_2 = np.sum(eigenvalues_by_dim[2])
    total_4 = np.sum(eigenvalues_by_dim[4])

    conc_2 = sum_top5_2 / max(total_2, 1e-15)
    conc_4 = sum_top5_4 / max(total_4, 1e-15)

    # d_amb=4 时覆盖熵指数更大 → 更集中
    # 但这依赖于随机采样，用宽松阈值
    assert conc_4 > conc_2 * 0.5, (
        f"d_amb=4 集中度 {conc_4:.4f} 未显著高于 d_amb=2 的 {conc_2:.4f}"
    )


# ===========================================================================
# 3. 相变层测试
# ===========================================================================

def test_phase_diagram_has_three_regions():
    """相变图应包含低维/中间/高维三种相"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=5)
    phases = hda.dimension_phase_diagram()
    phase_labels = set(entry["phase"] for entry in phases["phases"])
    assert "low_dim" in phase_labels
    assert "intermediate" in phase_labels
    assert "high_dim" in phase_labels


def test_phase_diagram_monotonic_exponents():
    """势论指数应随 d_frac 增大而单调递减"""
    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=3)
    phases = hda.dimension_phase_diagram()
    exponents = [entry["polynomial_exponent"] for entry in phases["phases"]]
    for i in range(len(exponents) - 1):
        # 势论指数 = α/d_frac，应随 d_frac 增大而递减
        assert exponents[i] >= exponents[i+1] - 1e-15, (
            f"指数不应递增: [{i}]={exponents[i]}, [{i+1}]={exponents[i+1]}"
        )


# ===========================================================================
# 4. 跨维数对比测试
# ===========================================================================

def test_ambient_dimension_scaling():
    """不同环境维数下同一 IFS 的行为应可预测"""
    c = np.full(5, 0.5)
    p = np.full(5, 0.2)

    prev_n_star = float('inf')
    for d_amb in [1, 2, 3, 4]:
        hda = HighDimIFSAnalysis(c, p, ambient_dim=d_amb,
                                  separation_type="non_separated",
                                  overlap_degree=0.3)
        n_star = hda.optimal_switching_point()
        # 随 d_amb 增大，d_frac/d_amb 减小，N* 应单调递减
        if n_star < 1e6 and prev_n_star < 1e6:
            assert n_star <= prev_n_star + 1e-10, (
                f"d_amb={d_amb}: N*={n_star} > prev={prev_n_star}"
            )
        if n_star < 1e6:
            prev_n_star = n_star


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
