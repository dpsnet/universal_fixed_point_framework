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
lqg_instance.py

圈量子引力（Loop Quantum Gravity）面积谱实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- LQG 不是理论核心，只是抽象框架在离散几何谱上的一个算例。

实例假设（MH-LQG）：
- 自旋网络边携带 SU(2) 不可约表示，标记为半整数或整数自旋 j。
- 面积算子本征值由 A_j = 8 π γ √(j(j+1)) 给出，γ 为 Immirzi 参数。
- 用面积谱构造谱算子 A，并验证 λ_i = exp(-μ_i) 的谱对应。
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
class LQGInstance:
    """
    圈量子引力实例：将自旋网络面积谱包装为递归系统。

    参数
    ----------
    n_edges : int
        考虑的自旋网络边数。
    immirzi : float
        Immirzi 参数 γ（默认取 0.274，来自黑洞熵拟合）。
    spin_step : float
        自旋增量。半整数谱取 0.5（默认），整数谱取 1.0。
    metadata : dict
        实例假设元数据。
    """
    n_edges: int = 6
    immirzi: float = 0.274
    spin_step: float = 0.5
    metadata: dict = field(default_factory=lambda: {
        "type": "loop_quantum_gravity",
        "clifford_signature": (3, 1),
        "gauge_group": "SU(2)",
        "operator": "area_spectrum",
    })

    def __post_init__(self):
        if self.n_edges < 1:
            raise ValueError("n_edges 必须为正整数")
        if self.immirzi <= 0:
            raise ValueError("immirzi 参数必须为正")
        if self.spin_step not in {0.5, 1.0}:
            raise ValueError("spin_step 目前仅支持 0.5（半整数）或 1.0（整数）")
        self.metadata.setdefault("immirzi", self.immirzi)
        self.metadata.setdefault("spin_step", self.spin_step)

    def spins(self) -> np.ndarray:
        """返回 n_edges 条边对应的自旋序列 j = spin_step, 2*spin_step, ..."""
        return self.spin_step * np.arange(1, self.n_edges + 1)

    def area_spectrum(self) -> np.ndarray:
        """
        面积算子本征值：
            A_j = 8 π γ √(j(j+1))
        这里 ℓ_P² = 1（Planck 单位）。
        """
        j = self.spins()
        return 8.0 * np.pi * self.immirzi * np.sqrt(j * (j + 1.0))

    def transition_matrix(self) -> np.ndarray:
        """由面积谱构造 Koopman 矩阵 K = diag(A_j / A_max)。"""
        areas = self.area_spectrum()
        max_area = areas.max()
        lambdas = areas / max_area
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def to_rec_object(self) -> RecObject:
        """将 LQG 面积谱递归表示为 Rec 对象。"""
        state_space = self.area_spectrum().reshape(-1, 1)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_edges": self.n_edges,
                **self.metadata,
                "type": "lqg_area_spectrum",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将 LQG 面积谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_edges": self.n_edges,
            **self.metadata,
            "type": "lqg_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回 LQG 实例摘要。"""
        areas = self.area_spectrum()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "n_edges": self.n_edges,
                "immirzi": self.immirzi,
                "spin_step": self.spin_step,
            },
            "spins": self.spins().tolist(),
            "area_spectrum": areas.tolist(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_lqg_instance(n_edges: int = 6) -> LQGInstance:
    """便捷函数：创建并运行 LQG 实例。"""
    return LQGInstance(n_edges=n_edges)


if __name__ == "__main__":
    print("=" * 60)
    print("圈量子引力实例（下游插件）")
    print("=" * 60)

    lqg = run_lqg_instance(n_edges=5)
    summary = lqg.summary()

    print("\n[实例假设]")
    for key, value in lqg.metadata.items():
        print(f"  {key}: {value}")

    print("\n[自旋网络面积谱]")
    for j, area in zip(summary["spins"], summary["area_spectrum"]):
        print(f"  j = {j:.1f}: A = {area:.4f} ℓ_P²")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = lqg.to_rec_object()
    spec_obj = lqg.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
