"""
causal_set_instance.py

因果集（Causal Set）离散时空实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 因果集不是理论核心，只是抽象框架在离散时空谱上的一个算例。

实例假设（MH-CausalSet）：
- 在 d 维 Minkowski 时空中随机撒点（Poisson sprinkling），得到偏序关系 ≺。
- 用每个元素的将来元素个数（future cardinality）作为离散几何的谱源。
- 用该谱构造谱算子 A，并验证 λ_i = exp(-μ_i)。
- 原型阶段固定随机种子以保证可重复性。
"""

from __future__ import annotations

import sys
from pathlib import Path
from dataclasses import dataclass, field
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from rec_category import RecObject
from spec_category import PositiveSpectralObject


@dataclass
class CausalSetInstance:
    """
    因果集实例：将离散时空因果结构的将来基数谱包装为递归系统。

    参数
    ----------
    n_elements : int
        因果集元素个数。
    spacetime_dimension : int
        时空维数 d（至少为 2，默认 1+1 维即 d=2）。
    seed : int | None
        随机撒点种子。为 None 时每次生成不同因果集。
    metadata : dict
        实例假设元数据。
    """
    n_elements: int = 20
    spacetime_dimension: int = 2
    seed: int | None = 42
    metadata: dict = field(default_factory=lambda: {
        "type": "causal_set",
        "discretization": "poisson_sprinkling",
        "geometry": "minkowski",
    })

    def __post_init__(self):
        if self.n_elements < 2:
            raise ValueError("n_elements 至少为 2")
        if self.spacetime_dimension < 2:
            raise ValueError("spacetime_dimension 至少为 2")
        self.metadata.setdefault("n_elements", self.n_elements)
        self.metadata.setdefault("spacetime_dimension", self.spacetime_dimension)
        self._rng = np.random.default_rng(self.seed)
        self._coordinates = self._sprinkle()
        self._causal_matrix = self._build_causal_matrix()

    def _sprinkle(self) -> np.ndarray:
        """在 Minkowski 时空中均匀撒点：第一列为时间，后续列为空间坐标。"""
        coords = self._rng.random((self.n_elements, self.spacetime_dimension))
        # 按时间排序，保证因果矩阵为上三角
        coords = coords[np.argsort(coords[:, 0])]
        return coords

    def _build_causal_matrix(self) -> np.ndarray:
        """
        构造因果矩阵 C，其中 C[i,j] = 1 当且仅当事件 i 严格在事件 j 的过去光锥内。
        """
        coords = self._coordinates
        n = self.n_elements
        C = np.zeros((n, n), dtype=int)
        times = coords[:, 0]
        spatial = coords[:, 1:]
        for i in range(n):
            for j in range(i + 1, n):
                dt = times[j] - times[i]
                dx = np.linalg.norm(spatial[j] - spatial[i])
                # i ≺ j 当且仅当 t_i < t_j 且空间距离不超过时间差（光速 c=1）
                if dx <= dt + 1e-12:
                    C[i, j] = 1
        return C

    def coordinates(self) -> np.ndarray:
        """返回时空坐标。"""
        return self._coordinates.copy()

    def causal_matrix(self) -> np.ndarray:
        """返回严格因果矩阵。"""
        return self._causal_matrix.copy()

    def future_cardinalities(self) -> np.ndarray:
        """每个元素的将来元素个数。"""
        return self._causal_matrix.sum(axis=1).astype(float)

    def causal_spectrum(self) -> np.ndarray:
        """因果谱：将来基数（非负）。"""
        return self.future_cardinalities()

    def transition_matrix(self) -> np.ndarray:
        """由将来基数构造 Koopman 矩阵 K = diag(future_i / future_max)。"""
        spectrum = self.causal_spectrum()
        max_val = spectrum.max()
        if max_val <= 0:
            return np.eye(self.n_elements)
        lambdas = spectrum / max_val
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def to_rec_object(self) -> RecObject:
        """将因果集递归表示为 Rec 对象。"""
        state_space = self.coordinates()
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_elements": self.n_elements,
                **self.metadata,
                "type": "causal_set",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将因果集谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_elements": self.n_elements,
            **self.metadata,
            "type": "causal_set_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回因果集实例摘要。"""
        spectrum = self.causal_spectrum()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "n_elements": self.n_elements,
                "spacetime_dimension": self.spacetime_dimension,
                "seed": self.seed,
            },
            "causal_relations": int(self._causal_matrix.sum()),
            "future_cardinalities": spectrum.tolist(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_causal_set_instance(n_elements: int = 20) -> CausalSetInstance:
    """便捷函数：创建并运行因果集实例。"""
    return CausalSetInstance(n_elements=n_elements)


if __name__ == "__main__":
    print("=" * 60)
    print("因果集实例（下游插件）")
    print("=" * 60)

    cs = run_causal_set_instance(n_elements=10)
    summary = cs.summary()

    print("\n[实例假设]")
    for key, value in cs.metadata.items():
        print(f"  {key}: {value}")

    print(f"\n[离散几何统计]")
    print(f"  元素数: {cs.n_elements}")
    print(f"  时空维数: {cs.spacetime_dimension}")
    print(f"  因果关系数: {summary['causal_relations']}")

    print("\n[将来基数谱]")
    print(f"  {summary['future_cardinalities']}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = cs.to_rec_object()
    spec_obj = cs.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
