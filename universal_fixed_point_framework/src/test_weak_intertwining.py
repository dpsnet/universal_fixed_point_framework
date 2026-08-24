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
test_weak_intertwining.py

验证 SpectralMorphism 的 weak 交织模式。
"""

from __future__ import annotations

import numpy as np

from spec_category import PositiveSpectralObject, SpectralMorphism


def build_test_objects():
    """构造两个维数不同的 Spec 对象，用于测试 weak 交织。"""
    E1 = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0]))
    E2 = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0, 1.5]))
    return E1, E2


def test_strict_embedding():
    print("\n[测试 1] 严格交织：标准嵌入")
    E1, E2 = build_test_objects()
    T = SpectralMorphism(
        source=E1,
        target=E2,
        matrix=np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
        ]),
        intertwining_mode="strict",
    )
    assert T.is_valid(), "标准嵌入应满足严格交织"
    print("  通过")


def test_weak_projection():
    print("\n[测试 2] weak 交织：非严格但保持特征向量的投影")
    E1, E2 = build_test_objects()
    # T 将 E1 的前两个特征向量嵌入 E2，但乘以非单位权重
    T = SpectralMorphism(
        source=E1,
        target=E2,
        matrix=np.array([
            [2.0, 0.0, 0.0],
            [0.0, 3.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
        ]),
        intertwining_mode="weak",
    )
    assert T.is_valid(), "特征向量保持的投影应满足 weak 交织"
    print("  通过")


def test_weak_rejects_random():
    print("\n[测试 3] weak 交织拒绝随机矩阵")
    E1, E2 = build_test_objects()
    np.random.seed(0)
    T = SpectralMorphism(
        source=E1,
        target=E2,
        matrix=np.random.randn(4, 3),
        intertwining_mode="weak",
    )
    assert not T.is_valid(), "随机矩阵不应满足 weak 交织"
    print("  通过")


def main():
    print("=" * 60)
    print("weak 交织模式验证")
    print("=" * 60)

    test_strict_embedding()
    test_weak_projection()
    test_weak_rejects_random()

    print("\n" + "=" * 60)
    print("所有 weak 交织测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
