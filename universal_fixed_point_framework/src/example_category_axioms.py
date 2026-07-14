"""
example_category_axioms.py

验证 Rec 与 Spec 两个范畴的公理：
1. 结合律：(h ∘ g) ∘ f = h ∘ (g ∘ f)
2. 单位律：id ∘ f = f = f ∘ id
3. 复合的存在条件
"""

from typing import Tuple
import numpy as np

from rec_category import (
    RecObject,
    RecMorphism,
    identity_morphism,
    compose_morphisms,
)
from spec_category import (
    PositiveSpectralObject,
    SpectralMorphism,
    identity_spectral_morphism,
    compose_spectral_morphisms,
)


def build_rec_chain() -> Tuple[RecObject, RecObject, RecObject]:
    """构造三个可复合的 Rec 对象：R1 -> R2 -> R3 -> R4。"""
    R1 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    R2 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.8, 0.2], [0.2, 0.8]]),
    )
    R3 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.7, 0.3], [0.3, 0.7]]),
    )
    return R1, R2, R3


def build_rec_morphisms(R1, R2, R3) -> Tuple[RecMorphism, RecMorphism, RecMorphism]:
    """构造三个 Rec 态射 f: R1->R2, g: R2->R3, h: R3->R1。"""
    f = RecMorphism(
        source=R1,
        target=R2,
        map=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    g = RecMorphism(
        source=R2,
        target=R3,
        map=np.array([[0.8, 0.2], [0.2, 0.8]]),
    )
    h = RecMorphism(
        source=R3,
        target=R1,
        map=np.array([[0.7, 0.3], [0.3, 0.7]]),
    )
    return f, g, h


def build_spec_chain() -> Tuple[PositiveSpectralObject, PositiveSpectralObject, PositiveSpectralObject]:
    """构造三个可复合的 Spec 对象，其中 E1 ⊂ E2 ⊂ E3。"""
    E1 = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5]))
    E2 = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0]))
    E3 = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0, 1.5]))
    return E1, E2, E3


def build_spec_morphisms(E1, E2, E3) -> Tuple[SpectralMorphism, SpectralMorphism, SpectralMorphism]:
    """构造三个 Spec 态射 T: E1->E2, U: E2->E3, V: E3->E1（投影）。"""
    # T: 将 E1 嵌入 E2 的前两个维度
    T = SpectralMorphism(
        source=E1,
        target=E2,
        matrix=np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]),
    )
    # U: 将 E2 嵌入 E3 的前三个维度
    U = SpectralMorphism(
        source=E2,
        target=E3,
        matrix=np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
        ]),
    )
    # V: 将 E3 投影回 E1 的前两个维度
    V = SpectralMorphism(
        source=E3,
        target=E1,
        matrix=np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ]),
    )
    return T, U, V


def test_rec_associativity():
    print("\n[测试 1] Rec 范畴结合律")
    R1, R2, R3 = build_rec_chain()
    f, g, h = build_rec_morphisms(R1, R2, R3)

    left = compose_morphisms(h, compose_morphisms(g, f))
    right = compose_morphisms(compose_morphisms(h, g), f)

    assert np.allclose(left.map, right.map), "Rec 结合律不成立"
    print("  (h ∘ g) ∘ f == h ∘ (g ∘ f): True")
    print("  通过")


def test_rec_identity():
    print("\n[测试 2] Rec 范畴单位律")
    R1, R2, _ = build_rec_chain()
    f, _, _ = build_rec_morphisms(R1, R2, R1)

    id_R1 = identity_morphism(R1)
    id_R2 = identity_morphism(R2)

    left = compose_morphisms(f, id_R1)
    right = compose_morphisms(id_R2, f)

    assert np.allclose(left.map, f.map), "左单位律不成立"
    assert np.allclose(right.map, f.map), "右单位律不成立"
    print("  f ∘ id = f = id ∘ f: True")
    print("  通过")


def test_rec_composition_condition():
    print("\n[测试 3] Rec 复合存在条件")
    R1, R2, R3 = build_rec_chain()
    f, g, _ = build_rec_morphisms(R1, R2, R3)

    # 合法复合: g ∘ f: R1 -> R3
    gf = compose_morphisms(g, f)
    assert gf.source is R1
    assert gf.target is R3

    # 非法复合：构造状态空间维度不匹配的对象
    R_bad = RecObject(
        state_space=np.array([[0.0], [1.0], [2.0]]),
        evolution=np.eye(3),
    )
    # bad_morphism: R1 -> R_bad, map 形状 (3, 2)
    bad_map = np.zeros((3, 2))
    bad_morphism = RecMorphism(source=R1, target=R_bad, map=bad_map)
    try:
        # g: R2 -> R3, bad_morphism: R1 -> R_bad
        # g ∘ bad_morphism 非法，因为 bad_morphism.target = R_bad ≠ g.source = R2
        compose_morphisms(g, bad_morphism)
        raise AssertionError("应该抛出维度不匹配错误")
    except ValueError as e:
        print(f"  非法复合被正确拒绝: {e}")
    print("  通过")


def test_spec_associativity():
    print("\n[测试 4] Spec 范畴结合律")
    E1, E2, E3 = build_spec_chain()
    T, U, V = build_spec_morphisms(E1, E2, E3)

    left = compose_spectral_morphisms(V, compose_spectral_morphisms(U, T))
    right = compose_spectral_morphisms(compose_spectral_morphisms(V, U), T)

    assert np.allclose(left.matrix, right.matrix), "Spec 结合律不成立"
    print("  (V ∘ U) ∘ T == V ∘ (U ∘ T): True")
    print("  通过")


def test_spec_identity():
    print("\n[测试 5] Spec 范畴单位律")
    E1, E2, E3 = build_spec_chain()
    T, _, _ = build_spec_morphisms(E1, E2, E3)

    id_E1 = identity_spectral_morphism(E1)
    id_E2 = identity_spectral_morphism(E2)

    # T: E1 -> E2, id_E1: E1 -> E1, id_E2: E2 -> E2
    left = compose_spectral_morphisms(T, id_E1)   # T ∘ id_E1: E1 -> E2
    right = compose_spectral_morphisms(id_E2, T)  # id_E2 ∘ T: E1 -> E2

    assert np.allclose(left.matrix, T.matrix), "左单位律不成立"
    assert np.allclose(right.matrix, T.matrix), "右单位律不成立"
    print("  T ∘ id = T = id ∘ T: True")
    print("  通过")


def test_spec_intertwining():
    print("\n[测试 6] Spec 态射强交织条件")
    E1, E2, E3 = build_spec_chain()
    T, _, _ = build_spec_morphisms(E1, E2, E3)

    assert T.is_valid(), "T 不满足强交织条件"
    print("  T A_1 = A_2 T: True")
    print("  通过")


def main():
    print("=" * 60)
    print("范畴公理验证测试")
    print("=" * 60)

    test_rec_associativity()
    test_rec_identity()
    test_rec_composition_condition()
    test_spec_associativity()
    test_spec_identity()
    test_spec_intertwining()

    print("\n" + "=" * 60)
    print("所有范畴公理测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
