"""
test_orbit_functor.py

验证轨道函子 O 的最小原型接口。
"""

from __future__ import annotations

import numpy as np

from orbit_functor import OrbitFunctor
from rec_category import RecObject, RecMorphism, identity_morphism, compose_morphisms


def test_sm_orbit_weights():
    print("\n[测试 1] SM 费米子扇区轨道权重")
    weights = OrbitFunctor.on_sm_all_sectors()
    ratios = OrbitFunctor.compute_ratios(weights)
    print(f"  权重: {weights}")
    print(f"  比例: {ratios}")

    # 验证 q_u : q_d : q_l = 1 : 1 : 3
    assert np.isclose(weights["up"], 1.0)
    assert np.isclose(weights["down"], 1.0)
    assert np.isclose(weights["lepton"], 3.0)
    assert abs(ratios["lepton"] / ratios["up"] - 3.0) < 1e-6
    print("  通过")


def test_ntk_orbit_weight():
    print("\n[测试 2] NTK 轨道权重")
    n_samples = 50
    spectrum = np.array([1.0, 0.5, 0.5, 0.25])
    O = OrbitFunctor.on_ntk(n_samples, spectrum)
    print(f"  O(NTK) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_string_orbit_weight():
    print("\n[测试 3] 弦论轨道权重")
    O = OrbitFunctor.on_string(genus=2, n_punctures=3)
    print(f"  O(string, g=2, n=3) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_gravitational_orbit_weight():
    print("\n[测试 4] 引力测地线轨道权重")
    O = OrbitFunctor.on_gravitational(spacetime_dim=4, isotropic_orbits=2)
    print(f"  O(gravity) = {O:.4f}")
    assert O == 8.0
    print("  通过")


def test_bsm_orbit_weight():
    print("\n[测试 5] BSM 新规范群轨道权重")
    O_u1 = OrbitFunctor.on_bsm("U(1)_X", representation_dim=1, bsm_charge=2.0)
    O_su2 = OrbitFunctor.on_bsm("SU(2)_X", representation_dim=2)
    print(f"  O(U(1)_X, q=2) = {O_u1:.4f}")
    print(f"  O(SU(2)_X, dim=2) = {O_su2:.4f}")
    assert O_u1 == 2.0
    assert O_su2 == 2.0
    print("  通过")


def test_lqg_orbit_weight():
    print("\n[测试 6] 圈量子引力轨道权重")
    O = OrbitFunctor.on_loop_quantum_gravity(n_edges=6, immirzi=0.274)
    print(f"  O(LQG) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_ads_cft_orbit_weight():
    print("\n[测试 7] AdS/CFT 轨道权重")
    O = OrbitFunctor.on_ads_cft(central_charge=12.0, n_operators=6)
    print(f"  O(AdS/CFT) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_tqft_orbit_weight():
    print("\n[测试 8] TQFT 轨道权重")
    O = OrbitFunctor.on_tqft(n_anyons=3, total_quantum_dimension=2.4142)
    print(f"  O(TQFT) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_ncg_orbit_weight():
    print("\n[测试 9] 非交换几何轨道权重")
    O = OrbitFunctor.on_noncommutative_geometry(n_points=5, spectral_action=2.25)
    print(f"  O(NCG) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_causal_set_orbit_weight():
    print("\n[测试 10] 因果集轨道权重")
    O = OrbitFunctor.on_causal_set(n_elements=20, n_relations=100)
    print(f"  O(CausalSet) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_asymptotic_safety_orbit_weight():
    print("\n[测试 11] 渐近安全轨道权重")
    O = OrbitFunctor.on_asymptotic_safety(
        n_couplings=4,
        critical_exponents=np.array([0.5, 1.0, 1.5, 2.0]),
    )
    print(f"  O(AsymptoticSafety) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_twistor_orbit_weight():
    print("\n[测试 12] 扭量理论轨道权重")
    O = OrbitFunctor.on_twistor(n_particles=4)
    print(f"  O(Twistor) = {O:.4f}")
    assert O > 0
    print("  通过")


def test_orbit_functor_morphism_mapping():
    print("\n[测试 13] 轨道函子态射映射 O(f)")
    R1 = RecObject(state_space=np.eye(2), evolution=np.array([[0.9, 0.1], [0.1, 0.9]]))
    R2 = RecObject(state_space=np.eye(2), evolution=np.array([[0.8, 0.2], [0.2, 0.8]]))
    f = RecMorphism(source=R1, target=R2, map=np.eye(2))

    ratio = OrbitFunctor.map_morphism(f)
    print(f"  O(R1)={OrbitFunctor.on_rec_object(R1):.4f}, O(R2)={OrbitFunctor.on_rec_object(R2):.4f}")
    print(f"  O(f)=w_R2/w_R1 = {ratio:.4f}")
    assert ratio > 0
    print("  通过")


def test_orbit_functor_axioms():
    print("\n[测试 14] 轨道函子公理验证")
    R1 = RecObject(state_space=np.eye(2), evolution=np.array([[0.9, 0.1], [0.1, 0.9]]))
    R2 = RecObject(state_space=np.eye(2), evolution=np.array([[0.8, 0.2], [0.2, 0.8]]))
    R3 = RecObject(state_space=np.eye(2), evolution=np.array([[0.7, 0.3], [0.3, 0.7]]))
    f = RecMorphism(source=R1, target=R2, map=np.eye(2))
    g = RecMorphism(source=R2, target=R3, map=np.eye(2))

    results = OrbitFunctor.verify_functor_axioms(R1, R2, R3, f, g)
    print(f"  O(id_R) = 1: {results['preserves_identity']} (O_id={results['O_id']:.4f})")
    print(f"  O(g∘f) = O(g)·O(f): {results['preserves_composition']} "
          f"(O_gf={results['O_gf']:.4f}, O_g·O_f={results['O_g_times_O_f']:.4f})")
    assert results["preserves_identity"]
    assert results["preserves_composition"]
    print("  通过")


def test_weight_equivalence_class():
    """轨道权重的等价类应能区分不同的谱结构。"""
    sm = OrbitFunctor.on_sm_all_sectors()
    cls = OrbitFunctor.weight_equivalence_class(sm)
    print(f"  SM 等价类: {cls}")
    # SM 权重 {1,1,3,1} → 整数比 {1,1,3,1}
    assert 3 in cls
    assert 1 in cls

    # 相同权重结构的不同理论应有相同等价类
    sm2 = {"up": 1.0, "down": 1.0, "lepton": 3.0, "neutrino": 1.0}
    cls2 = OrbitFunctor.weight_equivalence_class(sm2)
    assert cls == cls2, "相同结构的等价类应一致"

    # 不同结构
    different = {"a": 1.0, "b": 2.0, "c": 4.0}
    cls3 = OrbitFunctor.weight_equivalence_class(different)
    assert cls != cls3, "不同结构的等价类应不同"
    print("  通过")


def test_same_spectrum_criterion():
    """同谱判定条件应正确识别等价/不等价的谱结构。"""
    sm1 = OrbitFunctor.on_sm_all_sectors()
    sm2 = {"up": 1, "down": 1, "lepton": 3, "neutrino": 1}
    diff = {"a": 1, "b": 2, "c": 3}

    assert OrbitFunctor.same_spectrum_criterion(sm1, sm2), "相同结构的谱应判定为同谱"
    assert not OrbitFunctor.same_spectrum_criterion(sm1, diff), "不同结构的谱应判定为不同谱"
    print("  通过")


def test_spectrum_charge():
    """谱荷应随权重规模单调增长。"""
    small = {"a": 1.0, "b": 1.0}
    large = {"a": 3.0, "b": 3.0}

    c_small = OrbitFunctor.spectrum_charge(small)
    c_large = OrbitFunctor.spectrum_charge(large)

    assert c_small < c_large, "谱荷应随权重增长"
    assert abs(c_small - np.sqrt(2)) < 1e-10, f"sqrt(1+1) = sqrt(2) ≈ {c_small}"
    print(f"  sqrt(2) = {c_small:.6f} ✅")
    print("  通过")


def test_representation_signature():
    """表示签名应包含完整的结构信息。"""
    sm = OrbitFunctor.on_sm_all_sectors()
    sig = OrbitFunctor.representation_signature(sm)

    assert "dimension" in sig
    assert "equivalence_class" in sig
    assert "spectrum_charge" in sig
    assert "max_weight_ratio" in sig
    assert "weight_entropy" in sig

    # SM 有 4 个扇区
    assert sig["dimension"] == 4
    # 最大权重比 = 3/1
    assert abs(sig["max_weight_ratio"] - 3.0) < 1e-10
    # 谱荷 = sqrt(1+1+9+1) = sqrt(12)
    expected_charge = float(np.sqrt(1**2 + 1**2 + 3**2 + 1**2))
    assert abs(sig["spectrum_charge"] - expected_charge) < 1e-10

    print(f"  SM 表示签名: {sig}")
    print("  通过")


def test_compute_ratio():
    """compute_ratio 应安全处理边界值。"""
    from orbit_functor import compute_ratio
    assert abs(compute_ratio(3.0, 1.0) - 3.0) < 1e-10
    assert compute_ratio(5.0, 0.0) == float("inf")
    assert compute_ratio(0.0, 0.0) == 1.0
    print("  通过")


def main():
    print("=" * 60)
    print("轨道函子 O 的最小原型验证")
    print("=" * 60)

    test_sm_orbit_weights()
    test_ntk_orbit_weight()
    test_string_orbit_weight()
    test_gravitational_orbit_weight()
    test_bsm_orbit_weight()
    test_lqg_orbit_weight()
    test_ads_cft_orbit_weight()
    test_tqft_orbit_weight()
    test_ncg_orbit_weight()
    test_causal_set_orbit_weight()
    test_asymptotic_safety_orbit_weight()
    test_twistor_orbit_weight()
    test_orbit_functor_morphism_mapping()
    test_orbit_functor_axioms()
    test_weight_equivalence_class()
    test_same_spectrum_criterion()
    test_spectrum_charge()
    test_representation_signature()
    test_compute_ratio()

    print("\n" + "=" * 60)
    print("所有轨道函子测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
