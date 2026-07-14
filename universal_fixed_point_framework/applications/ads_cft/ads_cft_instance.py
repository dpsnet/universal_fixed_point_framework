"""
ads_cft_instance.py

AdS/CFT 对偶中 2D 共形场论算子谱实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- AdS/CFT 不是理论核心，只是抽象框架在共形场论谱上的一个算例。

实例假设（MH-AdS/CFT）：
- 2D CFT 由中心荷 c 与一组初级场 (h, \bar h) 描述。
- 标度维数 Δ = h + \bar h 构成谱源。
- 用 Δ_i 构造谱算子 A，并验证 λ_i = exp(-μ_i) 的谱对应。
- 原型阶段采用一个合成的、覆盖低维初级场的谱（identity、低自旋矢量、应力张量等）。
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
class AdSCFTInstance:
    """
    AdS/CFT 实例：将 2D CFT 初级场标度维数谱包装为递归系统。

    参数
    ----------
    central_charge : float
        中心荷 c。
    n_operators : int
        考虑的初级场数量。默认生成一组低维代表性算子。
    operator_dimensions : list[float] | None
        可选：直接传入标度维数列表 Δ_i。若提供，长度需等于 n_operators。
    metadata : dict
        实例假设元数据。
    """
    central_charge: float = 12.0
    n_operators: int = 6
    operator_dimensions: list[float] | None = None
    metadata: dict = field(default_factory=lambda: {
        "type": "ads_cft",
        "dimension": 2,
        "dual_geometry": "AdS_3",
        "operator_type": "primary_scaling_dimensions",
    })

    def __post_init__(self):
        if self.n_operators < 1:
            raise ValueError("n_operators 必须为正整数")
        if self.central_charge <= 0:
            raise ValueError("central_charge 必须为正")
        if self.operator_dimensions is not None:
            if len(self.operator_dimensions) != self.n_operators:
                raise ValueError("operator_dimensions 长度必须等于 n_operators")
            if any(d < 0 for d in self.operator_dimensions):
                raise ValueError("标度维数必须非负")
        else:
            self.operator_dimensions = self._default_dimensions().tolist()
        self.metadata.setdefault("central_charge", self.central_charge)

    def _default_dimensions(self) -> np.ndarray:
        """生成默认的低维初级场标度维数序列。"""
        dims = [0.0]  # identity
        delta = 1.0
        while len(dims) < self.n_operators:
            # 每个 Δ 层最多放两个手征配对 (h,0) 和 (0,h)，再补充对称 (h,h)
            remaining = self.n_operators - len(dims)
            if remaining >= 2 and delta > 0:
                dims.extend([delta, delta])
            else:
                dims.append(delta)
            delta += 1.0
        return np.array(dims[: self.n_operators])

    def scaling_dimensions(self) -> np.ndarray:
        """返回初级场标度维数 Δ_i。"""
        return np.array(self.operator_dimensions, dtype=float)

    def transition_matrix(self) -> np.ndarray:
        """由标度维数构造 Koopman 矩阵 K = diag(Δ_i / Δ_max)。"""
        dims = self.scaling_dimensions()
        max_dim = dims.max()
        if max_dim <= 0:
            # 只有 identity 的情形，退化为单位阵
            return np.eye(self.n_operators)
        lambdas = dims / max_dim
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def to_rec_object(self) -> RecObject:
        """将 CFT 算子谱递归表示为 Rec 对象。"""
        state_space = self.scaling_dimensions().reshape(-1, 1)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_operators": self.n_operators,
                **self.metadata,
                "type": "ads_cft_primary_spectrum",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将 CFT 算子谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_operators": self.n_operators,
            **self.metadata,
            "type": "ads_cft_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回 AdS/CFT 实例摘要。"""
        dims = self.scaling_dimensions()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "central_charge": self.central_charge,
                "n_operators": self.n_operators,
            },
            "scaling_dimensions": dims.tolist(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_ads_cft_instance(n_operators: int = 6) -> AdSCFTInstance:
    """便捷函数：创建并运行 AdS/CFT 实例。"""
    return AdSCFTInstance(n_operators=n_operators)


if __name__ == "__main__":
    print("=" * 60)
    print("AdS/CFT 实例（下游插件）")
    print("=" * 60)

    ads = run_ads_cft_instance(n_operators=6)
    summary = ads.summary()

    print("\n[实例假设]")
    for key, value in ads.metadata.items():
        print(f"  {key}: {value}")

    print("\n[CFT 初级场标度维数]")
    for i, delta in enumerate(summary["scaling_dimensions"]):
        print(f"  算子 {i}: Δ = {delta:.4f}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = ads.to_rec_object()
    spec_obj = ads.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
