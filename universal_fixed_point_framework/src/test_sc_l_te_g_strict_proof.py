"""
test_sc_l_te_g_strict_proof.py

Phase 15A-4: SC-L/TE-G 严格证明测试。

验证：
1. SC-L Ledrappier-Young 维数分解
2. SC-L 谱测度维数计算
3. SC-L IFS 验证（与 Moran 维数对比）
4. TE-G IFS 验证
5. TE-G Markov IFS 验证
6. SC-L/TE-G 组合验证
"""

from __future__ import annotations

import numpy as np
import pytest

from sc_l_te_g_strict_proof import SCLStrictProof, TEGStrictProof


def test_scl_ledrappier_young():
    """SC-L: Ledrappier-Young 维数分解。"""
    scl = SCLStrictProof()

    dim = scl.ledrappier_young_dimension(entropy=0.693, positive_lyapunov=0.693, negative_lyapunov=0.0)
    assert np.isclose(dim, 1.0), "纯扩张系统维数应为 1"

    dim = scl.ledrappier_young_dimension(entropy=0.693, positive_lyapunov=0.693, negative_lyapunov=0.693)
    assert np.isclose(dim, 2.0), "双曲系统维数应为 2"


def test_scl_spectral_dimension():
    """SC-L: 谱测度维数计算。"""
    scl = SCLStrictProof()

    result = scl.spectral_dimension_scl(entropy=0.693, positive_lyapunov=0.693)
    assert result["valid"]
    assert np.isclose(result["D1"], 1.0)
    assert np.isclose(result["dH_upper_bound"], 1.0)


def test_scl_ifs_verification():
    """SC-L: IFS 验证（与 Moran 维数对比）。"""
    scl = SCLStrictProof()

    contraction = np.array([0.5, 0.5])
    probabilities = np.array([0.5, 0.5])

    result = scl.verify_scl_ifs(contraction, probabilities)

    assert result["entropy"] > 0
    assert result["positive_lyapunov"] > 0
    assert result["D_KY"] > 0
    assert result["moran_dimension"] > 0
    assert result["relative_difference"] < 0.3, "D_KY 与 Moran 维数差异应 <30%"


def test_scl_ifs_different_params():
    """SC-L: 不同 IFS 参数验证。"""
    scl = SCLStrictProof()

    test_cases = [
        (np.array([0.4, 0.3]), np.array([0.5, 0.5])),
        (np.array([0.6, 0.3, 0.2]), np.array([0.33, 0.33, 0.34])),
        (np.array([0.7, 0.2]), np.array([0.6, 0.4])),
    ]

    for contraction, probabilities in test_cases:
        result = scl.verify_scl_ifs(contraction, probabilities)
        assert result["D_KY"] > 0
        assert result["moran_dimension"] > 0


def test_teg_ifs_verification():
    """TE-G: IFS 验证。"""
    teg = TEGStrictProof()

    contraction = np.array([0.5, 0.3])
    probabilities = np.array([0.5, 0.5])

    result = teg.verify_te_g_ifs(contraction, probabilities)

    assert result["topological_entropy"] > 0
    assert 0 <= result["spectral_gap"] <= 1
    assert result["product"] <= 1.0 + 1e-10, "TE-G 不等式应满足"


def test_teg_markov_verification():
    """TE-G: Markov IFS 验证。"""
    teg = TEGStrictProof()

    transition_matrix = np.array([[0.8, 0.2], [0.3, 0.7]])

    result = teg.verify_te_g_markov(transition_matrix)

    assert result["valid"]
    assert result["lambda1"] > 0
    assert 0 <= result["gamma"] <= 1


def test_teg_multiple_cases():
    """TE-G: 多组参数验证。"""
    teg = TEGStrictProof()

    test_cases = [
        (np.array([0.6, 0.4]), np.array([0.5, 0.5])),
        (np.array([0.7, 0.3]), np.array([0.6, 0.4])),
        (np.array([0.8, 0.5, 0.3]), np.array([0.3, 0.4, 0.3])),
    ]

    for contraction, probabilities in test_cases:
        result = teg.verify_te_g_ifs(contraction, probabilities)
        assert result["satisfied"], f"TE-G 不等式应满足: {result}"


def test_scl_teg_combined():
    """SC-L/TE-G 组合验证。"""
    scl = SCLStrictProof()
    teg = TEGStrictProof()

    contraction = np.array([0.5, 0.4])
    probabilities = np.array([0.5, 0.5])

    scl_result = scl.verify_scl_ifs(contraction, probabilities)
    teg_result = teg.verify_te_g_ifs(contraction, probabilities)

    assert scl_result["D_KY"] > 0, "D_KY 应大于零"
    assert teg_result["satisfied"], "TE-G 应满足"


def test_scl_boundary_case():
    """SC-L: 边界情况（零熵）。"""
    scl = SCLStrictProof()

    contraction = np.array([0.5])
    probabilities = np.array([1.0])

    result = scl.verify_scl_ifs(contraction, probabilities)

    assert np.isclose(result["entropy"], 0.0)
    assert result["D_KY"] >= 0


def test_teg_boundary_case():
    """TE-G: 边界情况（单收缩因子）。"""
    teg = TEGStrictProof()

    contraction = np.array([0.5])
    probabilities = np.array([1.0])

    result = teg.verify_te_g_ifs(contraction, probabilities)

    assert result["spectral_gap"] == 1.0
    assert result["topological_entropy"] == 0.0


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15A-4: SC-L/TE-G 严格证明测试")
    print("=" * 60)

    test_scl_ledrappier_young()
    print("  [1] Ledrappier-Young 维数分解 ✓")
    test_scl_spectral_dimension()
    print("  [2] 谱测度维数计算 ✓")
    test_scl_ifs_verification()
    print("  [3] SC-L IFS 验证 ✓")
    test_scl_ifs_different_params()
    print("  [4] SC-L 不同参数 ✓")
    test_teg_ifs_verification()
    print("  [5] TE-G IFS 验证 ✓")
    test_teg_markov_verification()
    print("  [6] TE-G Markov 验证 ✓")
    test_teg_multiple_cases()
    print("  [7] TE-G 多参数 ✓")
    test_scl_teg_combined()
    print("  [8] SC-L/TE-G 组合 ✓")
    test_scl_boundary_case()
    print("  [9] SC-L 边界情况 ✓")
    test_teg_boundary_case()
    print("  [10] TE-G 边界情况 ✓")

    print("\n" + "=" * 60)
    print("全部 SC-L/TE-G 严格证明测试通过。")
    print("=" * 60)
