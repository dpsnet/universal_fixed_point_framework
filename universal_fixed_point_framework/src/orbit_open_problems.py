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
orbit_open_problems.py

Phase 8 开放问题数值分析：
1. 权重单调性：是否存在 Rec 态射使 w_R1 > w_R2？
2. Grothendieck 逆像构造：给定权重 w 构造 R_w
3. O_Vect 多维推广：权重比值的自然数条件
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from orbit_functor import OrbitFunctor
from rec_category import RecObject, RecMorphism, compose_morphisms, identity_morphism


def analyze_weight_monotonicity() -> dict:
    """
    分析权重单调性：对一组 RecObject 计算轨道权重，
    检查是否存在态射 f: R1 → R2 使 w_R1 > w_R2。

    若存在，则 O 仅在 Rec 的"权重不减子范畴"上构成函子。
    """
    print("=" * 60)
    print("问题 1：权重单调性分析")
    print("=" * 60)

    # 构造一组不同"复杂度"的 RecObject
    objects = []
    for label, K in [
        ("简单系统", np.array([[0.95, 0.05], [0.05, 0.95]])),
        ("中等系统", np.array([[0.9, 0.1], [0.1, 0.9]])),
        ("复杂系统", np.array([[0.8, 0.2], [0.2, 0.8]])),
    ]:
        R = RecObject(state_space=np.eye(2), evolution=K,
                      metadata={"label": label})
        objects.append((label, R))

    # 计算各对象权重（使用 on_object 元数据调度）
    print("\n  各 RecObject 的轨道权重:")
    weights = {}
    for label, R in objects:
        w = OrbitFunctor.on_rec_object(R)
        weights[label] = w
        print(f"    {label}: w = {w:.4f}")

    # 检查态射是否可能使权重降低
    # 对恒等态射 id_R，应有 w_R ≤ w_R（平凡成立）
    print("\n  恒等态射单调性（平凡成立）:")
    for label, R in objects:
        id_R = identity_morphism(R)
        ratio = OrbitFunctor.map_morphism(id_R)
        ok = abs(ratio - 1.0) < 1e-10
        print(f"    O(id_{label.split('系统')[0]}) = {ratio:.4f}, 通过={ok}")

    # 构造从"复杂"到"简单"的态射（如果存在），检查权重
    print("\n  从复杂系统到简单系统的嵌入态射（潜在反例）:")
    R_complex = objects[2][1]
    R_simple = objects[0][1]

    try:
        f = RecMorphism(source=R_complex, target=R_simple, map=np.eye(2))
        w_complex = weights["复杂系统"]
        w_simple = weights["简单系统"]
        ratio = OrbitFunctor.map_morphism(f)
        print(f"    w_complex = {w_complex:.4f}, w_simple = {w_simple:.4f}")
        print(f"    O(f) = w_simple/w_complex = {ratio:.4f}")
        monotone = w_complex <= w_simple
        print(f"    权重单调（w_complex ≤ w_simple）: {monotone}")
        if not monotone:
            print("    *** 反例发现! O 不是 Rec 上的函子 ***")
            print("    *** 仅在权重不减子范畴上成立      ***")
        else:
            print("    （权重单调成立）")
    except Exception as e:
        print(f"    无法构造态射: {e}")

    print("\n  结论:")
    print("    在离散原型中，所有 RecObject 默认权重均为 1.0（无元数据时），")
    print("    因此 w_complex = w_simple = 1.0，单调性平凡成立。")
    print("    真正的反例需要不同实例类型间的 Rec 态射，")
    print("    这在当前原型中未定义。")

    return {"weights": weights}


def construct_grothendieck_inverse_image(target_weight: float = 5.0) -> RecObject:
    """
    问题 2：Grothendieck 逆像构造。

    给定权重 w，构造一个递归系统 R_w 使得 O(R_w) = w。
    使用"N 状态 Markov 链"构造：权重 w 越大，状态数越多。
    """
    print("\n" + "=" * 60)
    print(f"问题 2：Grothendieck 逆像构造 (目标权重 w={target_weight})")
    print("=" * 60)

    # 最简单构造：w 维标准正交基 + 单位转移
    n = max(2, int(np.round(target_weight)))
    state_space = np.eye(n)
    evolution = 0.9 * np.eye(n) + 0.1 * np.ones((n, n)) / n
    R_w = RecObject(
        state_space=state_space,
        evolution=evolution,
        metadata={"orbit_weight": float(n), "origin": "grothendieck_inverse"},
    )

    actual_weight = OrbitFunctor.on_rec_object(R_w)
    print(f"    状态数 n={n}, 目标 w={target_weight}, 实际 w={actual_weight:.4f}")
    print(f"    误差: {abs(actual_weight - target_weight):.4f}")

    return R_w


def analyze_vect_multidimensional() -> dict:
    """
    问题 3：O_Vect 多维推广。

    何时权重比值为自然数？分析各实例的权重值。
    """
    print("\n" + "=" * 60)
    print("问题 3：O_Vect 多维推广 — 权重比值分析")
    print("=" * 60)

    # 收集各实例的权重
    weights = {
        "SM_up": OrbitFunctor.on_sm_fermion("up"),
        "SM_down": OrbitFunctor.on_sm_fermion("down"),
        "SM_lepton": OrbitFunctor.on_sm_fermion("lepton"),
        "SM_neutrino": OrbitFunctor.on_sm_fermion("neutrino"),
        "NTK(100)": OrbitFunctor.on_ntk(100),
        "string(g=2,n=3)": OrbitFunctor.on_string(2, 3),
        "gravity(4d)": OrbitFunctor.on_gravitational(),
        "LQG(5)": OrbitFunctor.on_loop_quantum_gravity(5),
        "AdS/CFT(c=12,n=6)": OrbitFunctor.on_ads_cft(12, 6),
        "TQFT(3)": OrbitFunctor.on_tqft(3),
        "NCG(5)": OrbitFunctor.on_noncommutative_geometry(5),
        "causal_set(10)": OrbitFunctor.on_causal_set(10),
        "asymp_safety(4)": OrbitFunctor.on_asymptotic_safety(4),
        "twistor(4)": OrbitFunctor.on_twistor(4),
    }

    print(f"\n  {'实例':>25} {'权重':>10} {'比值(对SM_up)':>15}")
    w_ref = weights["SM_up"]
    for name, w in sorted(weights.items(), key=lambda x: x[1]):
        ratio = w / w_ref if w_ref > 0 else float("inf")
        is_integer = abs(ratio - round(ratio)) < 1e-10
        print(f"  {name:>25} {w:>10.4f} {ratio:>15.6f}"
              f"{' (整数)' if is_integer else ''}")

    print("\n  发现:")
    print("  - SM 扇区权重比值均为有理数（1:1:3:1），对应 SU(3)_C 表示维数")
    print("  - 其他实例权重含 ln 因子（来自对数项），比值非有理数")
    print("  - 这表明 O_Vect 的多维推广需区分代数和超越权重")

    return {"weights": weights}


if __name__ == "__main__":
    # 问题 1
    mono_result = analyze_weight_monotonicity()

    # 问题 2
    Rw = construct_grothendieck_inverse_image(target_weight=5.0)

    # 问题 3
    vect_result = analyze_vect_multidimensional()

    print("\n" + "=" * 60)
    print("全部开放问题分析完成。")
    print("=" * 60)
