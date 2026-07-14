"""
rec_category.py

递归系统范畴 (Rec) 的最小原型实现。

对象：RecObject，包含有限状态空间、演化规则、时间半群、附加元数据。
态射：RecMorphism，状态空间之间的结构保持映射，满足
    Φ_target ∘ f = f ∘ Φ_source
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Union, Any
import numpy as np


@dataclass
class RecObject:
    """
    递归系统范畴 Rec 的对象。

    参数
    ----------
    state_space : np.ndarray
        有限采样点集 X_R，形状为 (n, d)，n 为点数，d 为每点维度。
        当 d=1 时可退化为 (n,)。
    evolution : Union[np.ndarray, Callable[[np.ndarray], np.ndarray]]
        一步演化规则 Φ_R。可以是：
        - np.ndarray: 转移矩阵 K（Koopman/Frobenius-Perron 算子的离散表示），
          形状 (n, n)，满足 K[i, j] 表示从 x_j 到 x_i 的转移权重。
        - Callable: 显式映射 f: X_R -> X_R，接受并返回 np.ndarray。
    time_semigroup : str
        时间半群，"N" 表示离散迭代，"R+" 表示连续时间（原型阶段主要为 "N"）。
    metadata : dict
        附加结构集合，用于区分递归系统类型（IFS、NN、RG 等）。
    """
    state_space: np.ndarray
    evolution: Union[np.ndarray, Callable[[np.ndarray], np.ndarray]]
    time_semigroup: str = "N"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        # 统一 state_space 为二维数组 (n, d)
        if self.state_space.ndim == 1:
            self.state_space = self.state_space.reshape(-1, 1)
        if self.time_semigroup not in {"N", "R+"}:
            raise ValueError("time_semigroup 必须是 'N' 或 'R+'")

    @property
    def n_points(self) -> int:
        return self.state_space.shape[0]

    @property
    def dim(self) -> int:
        return self.state_space.shape[1]

    def step(self, x: np.ndarray) -> np.ndarray:
        """应用一步演化规则 Φ_R。"""
        if isinstance(self.evolution, np.ndarray):
            # 转移矩阵作用：y = K @ x（按列向量的组合）
            # 这里约定 evolution 为 Koopman 算子的矩阵表示
            return self.evolution @ x
        else:
            return self.evolution(x)

    def koopman_matrix(self, estimate_error: bool = False) -> np.ndarray | tuple[np.ndarray, float]:
        """
        返回 Koopman 算子的离散矩阵表示。

        若 evolution 已是矩阵，则直接返回；
        若 evolution 是 Callable，则在 state_space 上逐点求值并构造最近邻插值矩阵。

        参数
        ----------
        estimate_error : bool
            若为 True，返回 (K, max_relative_error) 元组，
            其中 max_relative_error 为最大最近邻距离与平均点间距之比。
        """
        if isinstance(self.evolution, np.ndarray):
            if estimate_error:
                return self.evolution, 0.0
            return self.evolution
        # Callable 情形：构造基函数 e_i 在 Φ_R 下的像
        n = self.n_points
        K = np.zeros((n, n))
        images = self.evolution(self.state_space)  # 形状 (n, d)
        # 简单最近邻索引映射：找到 image 在 state_space 中最接近的点
        max_rel_error = 0.0
        # 计算平均点间距
        if n > 1:
            spacings = []
            for i in range(n):
                dists_to_others = np.linalg.norm(
                    self.state_space - self.state_space[i], axis=1
                )
                positive_dists = dists_to_others[dists_to_others > 1e-15]
                if len(positive_dists) > 0:
                    spacings.append(np.min(positive_dists))
            avg_spacing = np.mean(spacings) if spacings else 1.0
        else:
            avg_spacing = 1.0
        for j in range(n):
            dists = np.linalg.norm(self.state_space - images[j], axis=1)
            i = np.argmin(dists)
            min_dist = dists[i]
            if avg_spacing > 0:
                rel_error = min_dist / avg_spacing
                if rel_error > max_rel_error:
                    max_rel_error = rel_error
            K[i, j] = 1.0
        if estimate_error:
            return K, float(max_rel_error)
        return K


@dataclass
class RecMorphism:
    """
    递归系统范畴 Rec 的态射 f: source -> target。

    参数
    ----------
    source, target : RecObject
    map : np.ndarray
        状态空间映射，形状为 (n_target, n_source)。
        对有限点集，map 通常是索引映射或插值矩阵。
    """
    source: RecObject
    target: RecObject
    map: np.ndarray

    def __post_init__(self):
        expected_shape = (self.target.n_points, self.source.n_points)
        if self.map.shape != expected_shape:
            raise ValueError(
                f"map 形状应为 {expected_shape}，实际为 {self.map.shape}"
            )

    def apply(self, x: np.ndarray) -> np.ndarray:
        """将态射作用于状态向量 x。"""
        return self.map @ x

    def is_valid(self, tol: float = 1e-10) -> bool:
        """
        验证是否满足交换图条件：
            Φ_target ∘ f = f ∘ Φ_source
        在矩阵表示下即：
            K_target @ map = map @ K_source
        """
        K_src = self.source.koopman_matrix()
        K_tgt = self.target.koopman_matrix()
        residual = K_tgt @ self.map - self.map @ K_src
        return np.linalg.norm(residual, ord="fro") < tol


def _rec_objects_equal(
    a: RecObject, b: RecObject, tol: float = 1e-10
) -> bool:
    """
    判断两个 Rec 对象是否足够接近，以允许态射复合。

    范畴论上，复合 g ∘ f 要求 f.target 与 g.source 是同一个对象。
    在离散原型中允许等价的不同实例，但等价必须同时检查：
    1. 状态空间点集一致；
    2. 演化规则一致（对矩阵形式进行数值比较）。
    """
    if a is b:
        return True
    if a.n_points != b.n_points or a.dim != b.dim:
        return False
    if not np.allclose(a.state_space, b.state_space, atol=tol):
        return False
    # 演化规则必须一致：矩阵可直接比较；Callable 无法可靠比较，保守视为不等。
    if isinstance(a.evolution, np.ndarray) and isinstance(b.evolution, np.ndarray):
        return np.allclose(a.evolution, b.evolution, atol=tol)
    return False


def compose_morphisms(
    g: RecMorphism, f: RecMorphism
) -> RecMorphism:
    """
    复合态射 g ∘ f: source(f) -> target(g)。

    范畴论要求：复合仅在 f.target 与 g.source 是同一个对象（或等价实例）时有定义。
    等价性同时检查状态空间与演化规则，避免仅因采样点相同而误认为对象相等。
    """
    if not _rec_objects_equal(f.target, g.source):
        raise ValueError(
            "f.target 与 g.source 不是同一个 RecObject，且其状态空间或演化规则不一致"
        )
    composed_map = g.map @ f.map
    return RecMorphism(source=f.source, target=g.target, map=composed_map)


def identity_morphism(R: RecObject) -> RecMorphism:
    """返回对象 R 上的单位态射。"""
    return RecMorphism(
        source=R,
        target=R,
        map=np.eye(R.n_points),
    )


def nearest_neighbor_map(
    source: RecObject, target: RecObject
) -> np.ndarray:
    """
    辅助函数：构造从 source.state_space 到 target.state_space 的最近邻映射矩阵。
    map[i, j] = 1 当 target.state_space[i] 是 source.state_space[j] 的最近邻。
    """
    n_src = source.n_points
    n_tgt = target.n_points
    M = np.zeros((n_tgt, n_src))
    for j in range(n_src):
        dists = np.linalg.norm(target.state_space - source.state_space[j], axis=1)
        i = np.argmin(dists)
        M[i, j] = 1.0
    return M
