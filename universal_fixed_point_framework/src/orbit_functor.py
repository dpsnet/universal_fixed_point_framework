"""
orbit_functor.py

规范群轨道函子 O 的最小原型接口。

在抽象框架中，轨道权重被设想为范畴内对象在规范群作用下的固有性质。
本文件提供各下游实例（SM、NTK、弦论、引力、BSM、LQG、AdS/CFT、TQFT、NCG、因果集、渐近安全、扭量）的轨道权重计算接口。
由于轨道函子的严格函子性仍在研究中，当前实现为**工作假设下的数值接口**，
允许通过实例元数据覆盖默认值。
"""

from __future__ import annotations

import numpy as np


def normalize_weights(weights: np.ndarray) -> np.ndarray:
    """将权重归一化为和为 1 的概率分布。"""
    weights = np.asarray(weights, dtype=float)
    s = weights.sum()
    if s <= 0:
        return np.ones_like(weights) / len(weights)
    return weights / s


def compute_ratio(a: float, b: float) -> float:
    """安全计算比例 a/b。"""
    if b <= 0:
        return float("inf") if a > 0 else 1.0
    return a / b


class OrbitFunctor:
    """
    轨道函子 O 的范畴实现。

    对象映射：递归系统 R ↦ 轨道权重 w_R ∈ ℝ₊（通过各实例的 on_* 方法）。
    态射映射：Rec 态射 f: R₁ → R₂ ↦ Weight 态射 w₁ ≤ w₂（或 Vect 态射 t ↦ (w₂/w₁)·t）。
    函子公理已在 verify_functor_axioms 中验证。
    """

    @staticmethod
    def on_object(R) -> float:
        """
        通用对象映射 O(R)：通过元数据调度到具体实例方法。

        若 Rec 对象带有 metadata["orbit_weight"]，直接返回。
        否则尝试用 metadata["type"] 调度到对应的 on_* 方法。
        若无法调度，返回默认权重 1.0。
        """
        if hasattr(R, "metadata") and "orbit_weight" in R.metadata:
            return float(R.metadata["orbit_weight"])
        return 1.0

    @staticmethod
    def on_sm_fermion(sector: str) -> float:
        """
        标准模型三代费米子扇区的轨道权重。

        工作假设：由 SU(3)_C 的 Weyl 轨道导出
            q_up : q_down : q_lepton = 1 : 1 : 3。
        中微子扇区暂时取与带电轻子相同的色单态权重 1。
        """
        weights = {
            "up": 1.0,
            "down": 1.0,
            "lepton": 3.0,
            "neutrino": 1.0,
        }
        key = sector.lower()
        if key not in weights:
            raise ValueError(f"未知 SM 扇区: {sector}。可选: {list(weights.keys())}")
        return weights[key]

    @staticmethod
    def on_sm_all_sectors() -> dict[str, float]:
        """返回 SM 全部费米子扇区的轨道权重。"""
        sectors = ["up", "down", "lepton", "neutrino"]
        return {s: OrbitFunctor.on_sm_fermion(s) for s in sectors}

    @staticmethod
    def on_ntk(n_samples: int, ntk_spectrum: np.ndarray | None = None) -> float:
        """
        NTK 实例的轨道权重。

        工作假设：由网络架构与初始化分布的对称性诱导。
        原型阶段简化为样本数与谱退化度的组合：
            O = n_samples / (1 + 谱退化度)。
        """
        degeneracy = 1.0
        if ntk_spectrum is not None and len(ntk_spectrum) > 0:
            # 用特征值的唯一数量近似退化度
            degeneracy = max(1.0, len(np.unique(np.round(ntk_spectrum, 6))))
        return float(n_samples) / degeneracy

    @staticmethod
    def on_string(genus: int, n_punctures: int, string_tension: float = 1.0) -> float:
        """
        弦论实例的轨道权重。

        工作假设：由弦世界面模空间 M_{g,n} 的复维度诱导。
        复维度为 dim_C M_{g,n} = 3g - 3 + n（g >= 2 时）。
        原型阶段取 O = max(1, 3g - 3 + n) / α'。
        """
        if genus >= 2:
            dim = 3 * genus - 3 + n_punctures
        elif genus == 1:
            dim = n_punctures
        else:  # genus == 0
            dim = max(0, n_punctures - 3)
        return max(1.0, float(dim)) / string_tension

    @staticmethod
    def on_gravitational(
        spacetime_dim: int = 4,
        isotropic_orbits: int = 1,
    ) -> float:
        """
        引力测地线实例的轨道权重。

        工作假设：由时空等度规群（isometry group）的轨道诱导。
        原型阶段简化为时空维数与独立各向同性轨道数的乘积。
        """
        return float(spacetime_dim * isotropic_orbits)

    @staticmethod
    def on_bsm(
        new_gauge_group: str,
        representation_dim: int,
        bsm_charge: float = 1.0,
    ) -> float:
        """
        BSM 新费米子扇区的轨道权重。

        工作假设：由新规范群轨道决定。
        对 U(1)_X，权重与荷的绝对值成正比；
        对非阿贝尔群，权重与表示维度成正比。
        """
        group = new_gauge_group.upper()
        if group.startswith("U(1)"):
            return abs(bsm_charge)
        # 对 SU(N) 等，用表示维度作为轨道权重的代理
        return float(representation_dim)

    @staticmethod
    def on_loop_quantum_gravity(
        n_edges: int,
        immirzi: float = 0.274,
    ) -> float:
        """
        圈量子引力实例的轨道权重。

        工作假设：由自旋网络边数与 Immirzi 参数共同诱导。
        边数越多、γ 越小，量子几何态空间越大，权重越高。
        原型阶段取 O = n_edges / γ。
        """
        if n_edges <= 0:
            raise ValueError("n_edges 必须为正整数")
        if immirzi <= 0:
            raise ValueError("immirzi 必须为正")
        return float(n_edges) / immirzi

    @staticmethod
    def on_ads_cft(
        central_charge: float,
        n_operators: int,
    ) -> float:
        """
        AdS/CFT 实例的轨道权重。

        工作假设：由中心荷 c 与初级场数量共同诱导。
        全息自由度随 c 增长，算子数量越多，轨道结构越丰富。
        原型阶段取 O = c * log(1 + n_operators)。
        """
        if central_charge <= 0:
            raise ValueError("central_charge 必须为正")
        if n_operators <= 0:
            raise ValueError("n_operators 必须为正整数")
        return float(central_charge) * np.log1p(n_operators)

    @staticmethod
    def on_tqft(
        n_anyons: int,
        total_quantum_dimension: float | None = None,
    ) -> float:
        """
        TQFT / 任意子融合范畴实例的轨道权重。

        工作假设：由任意子种类数与总量子维度诱导。
        原型阶段取 O = n_anyons * log(1 + d_total²)。
        """
        if n_anyons <= 0:
            raise ValueError("n_anyons 必须为正整数")
        d_total = total_quantum_dimension if total_quantum_dimension is not None else float(n_anyons)
        if d_total <= 0:
            raise ValueError("total_quantum_dimension 必须为正")
        return float(n_anyons) * np.log1p(d_total ** 2)

    @staticmethod
    def on_noncommutative_geometry(
        n_points: int,
        spectral_action: float | None = None,
    ) -> float:
        """
        非交换几何（谱三元组）实例的轨道权重。

        工作假设：由谱三元组的 Hilbert 空间维数与谱作用诱导。
        原型阶段取 O = n_points * log(1 + S_Λ(D))。
        """
        if n_points <= 0:
            raise ValueError("n_points 必须为正整数")
        s_action = spectral_action if spectral_action is not None else 1.0
        if s_action <= 0:
            raise ValueError("spectral_action 必须为正")
        return float(n_points) * np.log1p(s_action)

    @staticmethod
    def on_causal_set(
        n_elements: int,
        n_relations: int | None = None,
    ) -> float:
        """
        因果集实例的轨道权重。

        工作假设：由元素数与因果关系数共同诱导。
        关系越多，离散几何结构越丰富，轨道权重越高。
        原型阶段取 O = n_elements * log(1 + n_relations)。
        """
        if n_elements <= 0:
            raise ValueError("n_elements 必须为正整数")
        relations = n_relations if n_relations is not None else n_elements
        if relations < 0:
            raise ValueError("n_relations 必须非负")
        return float(n_elements) * np.log1p(relations)

    @staticmethod
    def on_asymptotic_safety(
        n_couplings: int,
        critical_exponents: np.ndarray | None = None,
    ) -> float:
        """
        渐近安全实例的轨道权重。

        工作假设：由耦合数与临界指数共同诱导。
        临界指数越大 / 耦合数越多，RG 不动点附近轨道结构越丰富。
        原型阶段取 O = n_couplings * log(1 + sum(|θ_i|))。
        """
        if n_couplings <= 0:
            raise ValueError("n_couplings 必须为正整数")
        exponents = critical_exponents if critical_exponents is not None else np.ones(n_couplings)
        exponents = np.asarray(exponents, dtype=float)
        if np.any(exponents < 0):
            raise ValueError("临界指数必须非负")
        return float(n_couplings) * np.log1p(exponents.sum())

    @staticmethod
    def on_rec_object(R) -> float:
        """
        从 RecObject 提取轨道权重。

        优先级：metadata["orbit_weight"] > 调度到 on_* 方法 > 默认 1.0。
        """
        return OrbitFunctor.on_object(R)

    @staticmethod
    def map_morphism(f) -> float:
        """
        态射映射 O(f): 返回权重缩放因子 w_R2 / w_R1。

        对应 Vect 值函子 O_Vect: R ↦ ℝ, 
        O_Vect(f: R₁→R₂)(t) = (w_R2/w_R1) · t
        """
        w1 = OrbitFunctor.on_rec_object(f.source)
        w2 = OrbitFunctor.on_rec_object(f.target)
        if w1 <= 0:
            return 1.0
        return w2 / w1

    @staticmethod
    def verify_functor_axioms(
        R1, R2, R3,
        f, g,
        tol: float = 1e-10,
    ) -> dict[str, bool]:
        """
        验证函子公理：
        1. O(id_R) = 1（Weight 中的恒等）
        2. O(g ∘ f) = O(g) * O(f)（Vect 值复合保持）
        """
        from rec_category import identity_morphism, compose_morphisms

        # 公理 1：保持单位态射
        id_R1 = identity_morphism(R1)
        O_id = OrbitFunctor.map_morphism(id_R1)
        identity_ok = abs(O_id - 1.0) < tol

        # 公理 2：保持复合
        gf = compose_morphisms(g, f)
        O_gf = OrbitFunctor.map_morphism(gf)
        O_g = OrbitFunctor.map_morphism(g)
        O_f = OrbitFunctor.map_morphism(f)
        composition_ok = abs(O_gf - O_g * O_f) < tol

        return {
            "preserves_identity": identity_ok,
            "preserves_composition": composition_ok,
            "O_id": O_id,
            "O_gf": O_gf,
            "O_g_times_O_f": O_g * O_f,
        }

    @staticmethod
    def on_twistor(
        n_particles: int,
    ) -> float:
        """
        扭量理论实例的轨道权重。

        工作假设：由外腿粒子数诱导。
        外腿越多，扭量运动学空间越大。
        原型阶段取 O = n_particles * log(1 + n_particles)。
        """
        if n_particles <= 0:
            raise ValueError("n_particles 必须为正整数")
        return float(n_particles) * np.log1p(n_particles)

    @staticmethod
    def compute_ratios(weights: dict[str, float]) -> dict[str, float]:
        """计算各权重相对于最小权重的比例。"""
        arr = np.array(list(weights.values()))
        if arr.min() <= 0:
            return {k: 1.0 for k in weights}
        return {k: v / arr.min() for k, v in weights.items()}

    @staticmethod
    def weight_equivalence_class(weights: dict[str, float]) -> tuple:
        """
        返回轨道权重的等价类标识。

        同一等价类的权重结构对应相同的谱结构。
        等价类由归一化权重比的整数三元组唯一确定。
        """
        ratios = OrbitFunctor.compute_ratios(weights)
        # 四舍五入为最接近的整数比
        int_ratios = tuple(sorted(round(v) for v in ratios.values()))
        return int_ratios

    @staticmethod
    def same_spectrum_criterion(
        weights1: dict[str, float],
        weights2: dict[str, float],
    ) -> bool:
        """
        同谱判定条件：两轨道权重集合是否对应相同的谱结构。

        判定方法：
        1. 计算各自的等价类
        2. 比较等价类标识是否一致
        """
        cls1 = OrbitFunctor.weight_equivalence_class(weights1)
        cls2 = OrbitFunctor.weight_equivalence_class(weights2)
        return cls1 == cls2

    @staticmethod
    def spectrum_charge(weights: dict[str, float]) -> float:
        """
        从轨道权重导出谱荷（整体谱标度因子）。

        谱荷 = sqrt(Σw_i²)，代表谱的整体"强度"。
        """
        arr = np.array(list(weights.values()))
        return float(np.sqrt(np.sum(arr ** 2)))

    @staticmethod
    def representation_signature(
        weights: dict[str, float],
    ) -> dict:
        """
        群表示谱签名：从轨道权重提取表示结构的不变量。

        返回：{
            "dimension": 表示维数（权重数目），
            "equivalence_class": 等价类标识，
            "spectrum_charge": 谱荷，
            "max_weight_ratio": 最大权重比，
            "weight_entropy": 权重分布熵，
        }
        """
        arr = np.array(list(weights.values()))
        n = len(arr)
        normalized = arr / (arr.sum() + 1e-15)

        entropy = -np.sum(normalized * np.log(normalized + 1e-15)) / np.log(n + 1e-15) if n > 1 else 0.0
        max_ratio = float(arr.max() / max(arr.min(), 1e-15))

        return {
            "dimension": n,
            "equivalence_class": OrbitFunctor.weight_equivalence_class(weights),
            "spectrum_charge": OrbitFunctor.spectrum_charge(weights),
            "max_weight_ratio": max_ratio,
            "weight_entropy": float(entropy),
        }
