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
test_eft_inverse_reconstruction.py

Phase 15C-3：EFT 逆重构唯一性数值验证。

验证：
1. 完备静默信息 → 唯一重构
2. 不完备静默信息 → 非唯一重构
3. 唯一性边界阈值分析
4. SM IR → UV 重构示例
5. 双向重构一致性验证
"""

from __future__ import annotations

import numpy as np
import pytest

from eft_equivalence_framework import EFTInverseReconstruction


def test_silence_info_complete():
    """完备静默信息判断。"""
    rec = EFTInverseReconstruction()

    complete = {"silence_degree": 0.7, "energy_ratio": 0.05, "laci_index": 20, "orbit_weight": 0.3}
    assert rec.is_silence_info_complete(complete), "完备静默信息应返回 True"

    incomplete_r = {"silence_degree": 0.7, "energy_ratio": 0.2, "laci_index": 20, "orbit_weight": 0.3}
    assert not rec.is_silence_info_complete(incomplete_r), "能标比 > 0.1 应不完备"

    incomplete_s = {"silence_degree": 0.4, "energy_ratio": 0.05, "laci_index": 20, "orbit_weight": 0.3}
    assert not rec.is_silence_info_complete(incomplete_s), "静默度 < 0.5 应不完备"

    incomplete_gamma = {"silence_degree": 0.7, "energy_ratio": 0.05, "laci_index": 5, "orbit_weight": 0.3}
    assert not rec.is_silence_info_complete(incomplete_gamma), "LACI < 10 应不完备"

    incomplete_w = {"silence_degree": 0.7, "energy_ratio": 0.05, "laci_index": 20, "orbit_weight": 0.6}
    assert not rec.is_silence_info_complete(incomplete_w), "轨道权重 > 0.5 应不完备"


def test_unique_reconstruction():
    """完备静默信息下的唯一性重构。"""
    rec = EFTInverseReconstruction()
    ir_spectrum = np.array([1.0, 2.0, 3.0])

    silence_info = {
        "silence_degree": 0.7,
        "energy_ratio": 0.1,
        "laci_index": 20.0,
        "orbit_weight": 0.3,
        "dof_ir": 3,
    }

    result = rec.reconstruct_uv_unique(ir_spectrum, silence_info)
    assert result["unique"], "完备静默信息应给出唯一重构"

    uv_spectrum = np.array(result["uv_spectrum"])
    expected = ir_spectrum / 0.1
    assert np.allclose(uv_spectrum, expected), "UV 谱应等于 IR 谱 / 能标比"


def test_non_unique_reconstruction():
    """不完备静默信息下的非唯一性重构。"""
    rec = EFTInverseReconstruction()
    ir_spectrum = np.array([1.0, 2.0, 3.0])

    incomplete_info = {"silence_degree": 0.7, "energy_ratio": 0.2, "laci_index": 20.0, "orbit_weight": 0.3}

    result = rec.reconstruct_uv_unique(ir_spectrum, incomplete_info)
    assert not result["unique"], "不完备静默信息应返回非唯一"

    result = rec.reconstruct_uv_non_unique(ir_spectrum, incomplete_info, n_candidates=3)
    assert result["n_candidates"] == 3, "应生成 3 个候选"
    assert len(result["candidates"]) == 3


def test_uniqueness_boundary():
    """唯一性边界阈值分析。"""
    rec = EFTInverseReconstruction()
    ir_spectrum = np.array([1.0, 2.0, 3.0])

    result = rec.uniqueness_boundary(ir_spectrum)
    thresholds = result["uniqueness_thresholds"]

    assert "energy_ratio_threshold" in thresholds
    assert "silence_degree_threshold" in thresholds
    assert "laci_threshold" in thresholds
    assert "orbit_weight_threshold" in thresholds

    r_thresh = thresholds["energy_ratio_threshold"]
    assert 0.09 < r_thresh < 0.11, f"能标比阈值应接近 0.1，实际 {r_thresh}"

    s_thresh = thresholds["silence_degree_threshold"]
    assert 0.49 < s_thresh < 0.51, f"静默度阈值应接近 0.5，实际 {s_thresh}"

    gamma_thresh = thresholds["laci_threshold"]
    assert 9 < gamma_thresh < 11, f"LACI 阈值应接近 10，实际 {gamma_thresh}"

    w_thresh = thresholds["orbit_weight_threshold"]
    assert 0.49 < w_thresh < 0.51, f"轨道权重阈值应接近 0.5，实际 {w_thresh}"


def test_sm_reconstruction():
    """SM IR → UV 重构示例。"""
    rec = EFTInverseReconstruction()

    sm_ir_spectrum = np.array([91.2, 80.4, 125.0])

    silence_info = {
        "silence_degree": 0.8,
        "energy_ratio": 0.01,
        "laci_index": 100.0,
        "orbit_weight": 0.1,
        "dof_ir": 3,
    }

    result = rec.reconstruct_uv_unique(sm_ir_spectrum, silence_info)
    assert result["unique"]

    uv_spectrum = np.array(result["uv_spectrum"])
    expected = sm_ir_spectrum / 0.01
    assert np.allclose(uv_spectrum, expected), "SM UV 谱应等于 SM IR 谱 / 0.01"

    assert result["dof_uv"] == 30, "UV 自由度应 = IR 自由度 / 轨道权重"


def test_bidirectional_consistency():
    """双向重构一致性验证：UV → IR → UV 应一致。"""
    rec = EFTInverseReconstruction()

    original_uv = np.array([100.0, 200.0, 300.0])
    r = 0.1

    ir_spectrum = original_uv * r

    silence_info = {
        "silence_degree": 0.7,
        "energy_ratio": r,
        "laci_index": 20.0,
        "orbit_weight": 0.3,
        "dof_ir": 3,
    }

    result = rec.reconstruct_uv_unique(ir_spectrum, silence_info)
    assert result["unique"]

    reconstructed_uv = np.array(result["uv_spectrum"])
    assert np.allclose(reconstructed_uv, original_uv), "重构 UV 应等于原始 UV"


def test_boundary_case():
    """边界情况：刚好满足四判据。"""
    rec = EFTInverseReconstruction()
    ir_spectrum = np.array([1.0, 2.0, 3.0])

    boundary_info = {
        "silence_degree": 0.51,
        "energy_ratio": 0.099,
        "laci_index": 10.1,
        "orbit_weight": 0.49,
        "dof_ir": 3,
    }

    result = rec.reconstruct_uv_unique(ir_spectrum, boundary_info)
    assert result["unique"], "边界情况应仍为唯一"


def test_zero_spectrum():
    """零谱情况处理。"""
    rec = EFTInverseReconstruction()
    ir_spectrum = np.array([0.0, 0.0, 0.0])

    silence_info = {
        "silence_degree": 0.7,
        "energy_ratio": 0.1,
        "laci_index": 20.0,
        "orbit_weight": 0.3,
        "dof_ir": 3,
    }

    result = rec.reconstruct_uv_unique(ir_spectrum, silence_info)
    assert result["unique"]

    uv_spectrum = np.array(result["uv_spectrum"])
    assert np.allclose(uv_spectrum, [0.0, 0.0, 0.0]), "零 IR 谱应得到零 UV 谱"


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15C-3: EFT 逆重构唯一性测试")
    print("=" * 60)

    test_silence_info_complete()
    print("  [1] 完备静默信息判断 ✓")
    test_unique_reconstruction()
    print("  [2] 唯一性重构 ✓")
    test_non_unique_reconstruction()
    print("  [3] 非唯一性重构 ✓")
    test_uniqueness_boundary()
    print("  [4] 唯一性边界阈值 ✓")
    test_sm_reconstruction()
    print("  [5] SM IR → UV 重构 ✓")
    test_bidirectional_consistency()
    print("  [6] 双向重构一致性 ✓")
    test_boundary_case()
    print("  [7] 边界情况 ✓")
    test_zero_spectrum()
    print("  [8] 零谱处理 ✓")

    print("\n" + "=" * 60)
    print("全部 EFT 逆重构唯一性测试通过。")
    print("=" * 60)
