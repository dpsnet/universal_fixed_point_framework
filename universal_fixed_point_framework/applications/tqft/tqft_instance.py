"""
tqft_instance.py

拓扑量子场论（TQFT）/ 任意子融合范畴实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- TQFT 不是理论核心，只是抽象框架在拓扑不变量谱上的一个算例。

实例假设（MH-TQFT）：
- 采用模张量范畴 / 任意子模型的量子维度作为谱源。
- 默认提供 Ising 任意子模型（1, σ, ψ），量子维度为 [1, √2, 1]。
- 支持用户传入任意一组拓扑不变量（如量子维度、配边不变量取值）。
- 用量子维度谱构造谱算子 A，并验证 λ_i = exp(-μ_i)。
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


def _ising_quantum_dimensions() -> np.ndarray:
    """Ising 任意子模型的量子维度：1, √2, 1。"""
    return np.array([1.0, np.sqrt(2.0), 1.0])


def _fibonacci_quantum_dimensions(n: int = 2) -> np.ndarray:
    """
    Fibonacci 任意子模型的量子维度（按 F_n 序列）。
    对标准 Fibonacci 范畴 n=2，返回 [1, φ]。
    """
    phi = 0.5 * (1.0 + np.sqrt(5.0))
    return np.array([1.0, phi])


@dataclass
class TQFTInstance:
    """
    TQFT 实例：将任意子量子维度 / 拓扑不变量谱包装为递归系统。

    参数
    ----------
    model : str
        预置模型名称："ising" 或 "fibonacci"；也可设为 "custom"。
    n_anyons : int
        任意子类型数。对 "ising" 固定为 3，"fibonacci" 固定为 2；
        对 "custom" 由 user_invariants 长度决定。
    user_invariants : list[float] | None
        自定义拓扑不变量取值（如量子维度）。当 model="custom" 时必须提供。
    metadata : dict
        实例假设元数据。
    """
    model: str = "ising"
    n_anyons: int | None = None
    user_invariants: list[float] | None = None
    metadata: dict = field(default_factory=lambda: {
        "type": "tqft",
        "structure": "modular_tensor_category",
        "invariant": "quantum_dimension",
    })

    def __post_init__(self):
        if self.model not in {"ising", "fibonacci", "custom"}:
            raise ValueError("model 必须是 'ising'、'fibonacci' 或 'custom'")
        if self.model == "custom":
            if self.user_invariants is None or len(self.user_invariants) == 0:
                raise ValueError("model='custom' 时必须提供 user_invariants")
            self._invariants = np.array(self.user_invariants, dtype=float)
            self.n_anyons = len(self._invariants)
        elif self.model == "ising":
            self._invariants = _ising_quantum_dimensions()
            self.n_anyons = len(self._invariants)
        else:  # fibonacci
            self._invariants = _fibonacci_quantum_dimensions()
            self.n_anyons = len(self._invariants)
        if np.any(self._invariants <= 0):
            raise ValueError("拓扑不变量必须为正")
        self.metadata.setdefault("model", self.model)
        self.metadata.setdefault("n_anyons", self.n_anyons)

    def topological_spectrum(self) -> np.ndarray:
        """返回拓扑不变量谱（默认是量子维度）。"""
        return self._invariants.copy()

    def transition_matrix(self) -> np.ndarray:
        """由拓扑不变量谱构造 Koopman 矩阵 K = diag(d_i / d_max)。"""
        invariants = self.topological_spectrum()
        max_inv = invariants.max()
        lambdas = invariants / max_inv
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def to_rec_object(self) -> RecObject:
        """将 TQFT 拓扑谱递归表示为 Rec 对象。"""
        state_space = self.topological_spectrum().reshape(-1, 1)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_anyons": self.n_anyons,
                **self.metadata,
                "type": "tqft_quantum_dimensions",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将 TQFT 拓扑谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_anyons": self.n_anyons,
            **self.metadata,
            "type": "tqft_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回 TQFT 实例摘要。"""
        inv = self.topological_spectrum()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "model": self.model,
                "n_anyons": self.n_anyons,
            },
            "topological_invariants": inv.tolist(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_tqft_instance(model: str = "ising") -> TQFTInstance:
    """便捷函数：创建并运行 TQFT 实例。"""
    return TQFTInstance(model=model)


if __name__ == "__main__":
    print("=" * 60)
    print("TQFT / 任意子融合范畴实例（下游插件）")
    print("=" * 60)

    tqft = run_tqft_instance(model="ising")
    summary = tqft.summary()

    print("\n[实例假设]")
    for key, value in tqft.metadata.items():
        print(f"  {key}: {value}")

    print("\n[拓扑不变量谱（量子维度）]")
    for i, d in enumerate(summary["topological_invariants"]):
        print(f"  任意子 {i}: d = {d:.4f}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = tqft.to_rec_object()
    spec_obj = tqft.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
