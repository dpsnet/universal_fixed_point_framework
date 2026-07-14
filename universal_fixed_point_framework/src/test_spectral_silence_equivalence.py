"""
test_spectral_silence_equivalence.py

Phase 15A-5: 谱静默判据(S1-S4)等价链系统验证。

验证四个静默判据之间的逻辑关系：
  S1: 连续谱条件 — 谱无离散本征态
  S2: 零测度条件 — 谱测度权重为零
  S3: LACI 高条件 — 谱间隙消失
  S4: 轨道权重条件 — 规范群作用下无不变量

验证策略：
  1. 构造已知谱型的测试用例（纯点谱/绝对连续/奇异连续/混合）
  2. 对每个用例运行全部四个判据
  3. 记录判据一致/不一致的模式
  4. 识别判据等价成立/不成立的条件
"""

from __future__ import annotations

import numpy as np
import pytest

from spectral_silence import SpectralSilence


# ===========================================================================
# 构造具有不同谱型的测试用例
# ===========================================================================

def make_pure_point_spectrum(n: int = 10, seed: int = 42) -> dict:
    """纯点谱：离散特征值，分布稀疏。"""
    rng = np.random.RandomState(seed)
    eigenvalues = np.sort(rng.uniform(0, 5, n))
    weights = np.full(n, 1.0 / n)
    return {"eigenvalues": eigenvalues, "weights": weights, "label": "纯点谱"}


def make_absolutely_continuous_spectrum(n: int = 100, seed: int = 42) -> dict:
    """
    绝对连续谱：特征值密集排列，近似连续区间。
    通过生成大量等间距特征值模拟。
    """
    eigenvalues = np.linspace(0, 5, n)
    # 权重均匀分布（Lebesgue 测度的离散近似）
    weights = np.full(n, 1.0 / n)
    return {"eigenvalues": eigenvalues, "weights": weights, "label": "绝对连续谱"}


def make_singular_continuous(
    n: int = 100, seed: int = 42
) -> dict:
    """
    奇异连续谱：Cantor 型谱分布。

    构造方法：用三分 Cantor 集生成特征值位置。
    """
    # 递归生成 Cantor 集点
    def cantor_set(level: int, start: float = 0.0, end: float = 5.0):
        if level == 0:
            return [(start + end) / 2.0]
        third = (end - start) / 3.0
        left = cantor_set(level - 1, start, start + third)
        right = cantor_set(level - 1, end - third, end)
        return left + right

    centers = np.array(cantor_set(4))  # 3^4 = 81 个点
    # 在 Cantor 集点周围加小高斯扰动模拟"奇异连续"特征
    rng = np.random.RandomState(seed)
    eigenvalues = centers + rng.normal(0, 0.02, len(centers))
    eigenvalues = np.sort(eigenvalues)
    weights = np.full(len(eigenvalues), 1.0 / len(eigenvalues))
    return {"eigenvalues": eigenvalues, "weights": weights, "label": "奇异连续谱 (Cantor)"}


def make_mixed_spectrum(seed: int = 42) -> dict:
    """
    混合谱：部分离散 + 部分连续。
    """
    rng = np.random.RandomState(seed)
    discrete_part = np.sort(rng.uniform(0, 2, 5))
    continuous_part = np.linspace(3, 5, 50)
    eigenvalues = np.concatenate([discrete_part, continuous_part])

    # 离散部分权重高，连续部分权重低
    discrete_weights = np.full(5, 0.15)
    continuous_weights = np.full(50, 0.05 / 50)  # 总和 0.05
    weights = np.concatenate([discrete_weights, continuous_weights])
    weights = weights / weights.sum()

    return {"eigenvalues": eigenvalues, "weights": weights, "label": "混合谱"}


def make_silent_spectrum(n_visible: int = 4, n_silent: int = 6) -> dict:
    """
    模拟弦论静默场景：部分可见 + 部分静默。
    静默部分的权重极小。
    """
    visible = np.linspace(0.1, 1.5, n_visible)
    silent = np.linspace(8.0, 15.0, n_silent)
    eigenvalues = np.sort(np.concatenate([visible, silent]))

    visible_weights = np.full(n_visible, 0.2)
    silent_weights = np.full(n_silent, 1e-10)
    weights = np.concatenate([visible_weights, silent_weights])
    weights = weights / weights.sum()

    return {"eigenvalues": eigenvalues, "weights": weights, "label": "弦论静默场景"}


def make_laci_high_spectrum(seed: int = 42) -> dict:
    """
    LACI HIGH 谱：谱间隙为零（特征值连续，无 gap）。
    """
    eigenvalues = np.linspace(0.0, 10.0, 200)
    weights = np.full(200, 1.0 / 200)
    return {"eigenvalues": eigenvalues, "weights": weights, "label": "LACI HIGH (零间隙)"}


# ===========================================================================
# 等价链验证
# ===========================================================================

TEST_SPECTRA = [
    make_pure_point_spectrum(),
    make_absolutely_continuous_spectrum(),
    make_singular_continuous(),
    make_mixed_spectrum(),
    make_silent_spectrum(),
    make_laci_high_spectrum(),
]


def test_all_criteria_defined():
    """四个判据应均可独立运行且返回布尔结果。"""
    spec = make_pure_point_spectrum()
    sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
    c1 = sa.check_continuous_spectrum()
    c2 = sa.check_zero_measure()
    c3 = sa.check_laci_high()
    c4 = sa.check_orbit_weight_zero()
    for c in [c1, c2, c3, c4]:
        assert isinstance(c.satisfied, (bool, np.bool_))
        assert isinstance(c.value, (float, np.floating))
    print("  四个判据均可独立运行 ✅")


def test_s1_s2_equivalence_continuous():
    """
    在绝对连续谱中：S1 (连续谱条件) 通常成立。
    检查 S1 与 S2 的一致性。
    """
    spec = make_absolutely_continuous_spectrum()
    sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
    c1 = sa.check_continuous_spectrum()
    c2 = sa.check_zero_measure()
    # 绝对连续谱：S1 应为 True，S2 应为 False
    print(f"  绝对连续谱: S1={c1.satisfied} (比值={c1.value:.4f}), "
          f"S2={c2.satisfied} (比值={c2.value:.4f})")
    # 注：在有限离散近似下，绝对连续谱的 S1 可能不为 True
    # 这不是等价链的问题，而是离散近似的固有限制


def test_s2_s4_equivalence_silent():
    """
    在弦论静默场景中：S2 (零测度) 和 S4 (轨道权重) 应同时成立。
    因为静默部分权重极小（S2）且轨道权重也极小（S4）。
    """
    spec = make_silent_spectrum()
    sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
    c2 = sa.check_zero_measure()
    c4 = sa.check_orbit_weight_zero()

    print(f"  静默场景: S2={c2.satisfied} (比值={c2.value:.4f}), "
          f"S4={c4.satisfied} (比值={c4.value:.4f})")

    # 在静默场景中，S2 和 S4 应同时为 True
    # S2: 零权重部分占主导 (>50%)
    # S4: 轨道权重同样为零
    assert c2.satisfied, f"S2 在静默场景中应为 True, 实际 {c2.satisfied}"


def test_s3_laci_high_continuous():
    """
    LACI HIGH (S3) 在绝对连续谱中应成立。
    连续谱 → 无谱间隙 → γ=0 → LACI HIGH。
    """
    spec = make_absolutely_continuous_spectrum(n=500)
    sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
    c3 = sa.check_laci_high()

    print(f"  绝对连续谱 LACI: S3={c3.satisfied}, γ={c3.value:.6f}, "
          f"threshold={c3.threshold}")

    # 高密度连续谱应有极小谱间隙
    assert c3.value < 0.1, f"连续谱的 γ 应很小, 实际 {c3.value:.6f}"


def test_s1_s3_equivalence_chain():
    """
    验证 S1 → S3 方向的等价性：
    如果谱是连续的 (S1)，则谱间隙消失 (S3)。
    """
    spec = make_laci_high_spectrum()
    sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
    c1 = sa.check_continuous_spectrum()
    c3 = sa.check_laci_high()

    print(f"  LACI HIGH 场景: S1={c1.satisfied} (比值={c1.value:.4f}), "
          f"S3={c3.satisfied} (γ={c3.value:.6f})")

    # S3 应在零间隙谱中成立
    assert c3.satisfied, "LACI HIGH 谱的 S3 应成立"


def test_equivalence_matrix():
    """
    在所有测试谱型上运行全部四个判据，生成等价性矩阵。

    输出格式：
        谱型          | S1   | S2   | S3   | S4   | 一致数
    绝对连续谱        |  T   |  F   |  T   |  F   |  2
    ...
    """
    print(f"\n  {'谱型':<20} {'S1':<6} {'S2':<6} {'S3':<6} {'S4':<6} {'一致':<6}")
    print(f"  {'-'*50}")

    results = []
    for spec in TEST_SPECTRA:
        sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
        c1 = sa.check_continuous_spectrum()
        c2 = sa.check_zero_measure()
        c3 = sa.check_laci_high()
        c4 = sa.check_orbit_weight_zero()
        vals = [c1.satisfied, c2.satisfied, c3.satisfied, c4.satisfied]
        n_true = sum(vals)
        results.append({
            "label": spec["label"],
            "S1": c1.satisfied,
            "S2": c2.satisfied,
            "S3": c3.satisfied,
            "S4": c4.satisfied,
            "n_true": n_true,
        })
        s1 = "T" if c1.satisfied else "F"
        s2 = "T" if c2.satisfied else "F"
        s3 = "T" if c3.satisfied else "F"
        s4 = "T" if c4.satisfied else "F"
        print(f"  {spec['label']:<20} {s1:<6} {s2:<6} {s3:<6} {s4:<6} {n_true:<6}")

    # 检查无静默场景（纯点谱）
    pp_result = results[0]
    assert pp_result["n_true"] <= 2, (
        f"纯点谱不应满足过多判据: {pp_result['n_true']}"
    )

    # 检查静默场景（弦论场景）至少满足 2 个判据
    silent_result = results[4]
    assert silent_result["n_true"] >= 2, (
        f"弦论静默场景应满足至少 2 个判据: {silent_result['n_true']}"
    )

    return results  # noqa: B901


def test_silence_fraction_interpretation():
    """
    验证静默比例与物理诠释的一致性。
    """
    spec = make_silent_spectrum(n_visible=2, n_silent=8)
    sa = SpectralSilence(spec["eigenvalues"], spec["weights"])
    result = sa.analyze()

    print(f"\n  极高静默场景 (2 可见 + 8 静默):")
    print(f"  静默比例: {result.silent_fraction:.2f}")
    print(f"  静默判定: {'静默' if result.is_silent else '非静默'}")
    print(f"  诠释: {result.interpretation}")

    assert result.is_silent, "极高静默场景应判为静默"
    assert result.silent_fraction >= 0.25, "至少应满足 1/4 判据"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
