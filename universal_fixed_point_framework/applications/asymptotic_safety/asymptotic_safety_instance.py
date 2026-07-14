"""
asymptotic_safety_instance.py

渐近安全（Asymptotic Safety）重整化群不动点实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 渐近安全不是理论核心，只是抽象框架在 RG 不动点谱上的一个算例。

实例假设（MH-AS）：
- 在 UV 固定点处，耦合常数 g* 满足 beta(g*) = 0。
- 线性化稳定性矩阵的本征值给出临界指数（critical exponents）θ_i。
- 用 |Re(θ_i)| 作为谱源构造谱算子 A，并验证 λ_i = exp(-μ_i)。
- 原型阶段默认给出一组合成临界指数，支持用户传入真实 RG 计算结果。
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


def _default_critical_exponents(n: int) -> np.ndarray:
    """默认合成临界指数：交替正负、以绝对值作为谱源。"""
    # 生成 [-1.5, 1.0, -0.5, 2.0, ...] 的实部
    values = np.array([(-1.0) ** i * (0.5 + 0.5 * i) for i in range(n)])
    return np.abs(values)


@dataclass
class AsymptoticSafetyInstance:
    """
    渐近安全实例：将 RG 不动点临界指数谱包装为递归系统。

    参数
    ----------
    n_couplings : int
        耦合常数个数。当未提供 critical_exponents 时使用。
    critical_exponents : list[float] | None
        可选自定义临界指数列表（实部）。若提供，n_couplings 被忽略。
    metadata : dict
        实例假设元数据。
    """
    n_couplings: int = 4
    critical_exponents: list[float] | None = None
    metadata: dict = field(default_factory=lambda: {
        "type": "asymptotic_safety",
        "fixed_point_equation": "beta(g*) = 0",
        "operator": "stability_matrix",
    })

    def __post_init__(self):
        if self.critical_exponents is not None:
            self._exponents = np.array(self.critical_exponents, dtype=float)
            self.n_couplings = len(self._exponents)
        else:
            if self.n_couplings < 1:
                raise ValueError("n_couplings 必须为正整数")
            self._exponents = _default_critical_exponents(self.n_couplings)
        if np.any(self._exponents < 0):
            raise ValueError("临界指数必须非负（已取实部绝对值）")
        self.metadata.setdefault("n_couplings", self.n_couplings)

    def critical_exponent_spectrum(self) -> np.ndarray:
        """返回临界指数谱 |Re(θ_i)|。"""
        return self._exponents.copy()

    def transition_matrix(self) -> np.ndarray:
        """由临界指数构造 Koopman 矩阵 K = diag(θ_i / θ_max)。"""
        exponents = self.critical_exponent_spectrum()
        max_exp = exponents.max()
        if max_exp <= 0:
            return np.eye(self.n_couplings)
        lambdas = exponents / max_exp
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def to_rec_object(self) -> RecObject:
        """将渐近安全谱递归表示为 Rec 对象。"""
        state_space = self.critical_exponent_spectrum().reshape(-1, 1)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_couplings": self.n_couplings,
                **self.metadata,
                "type": "asymptotic_safety_spectrum",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将渐近安全谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_couplings": self.n_couplings,
            **self.metadata,
            "type": "asymptotic_safety_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回渐近安全实例摘要。"""
        exponents = self.critical_exponent_spectrum()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "n_couplings": self.n_couplings,
            },
            "critical_exponents": exponents.tolist(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_asymptotic_safety_instance(n_couplings: int = 4) -> AsymptoticSafetyInstance:
    """便捷函数：创建并运行渐近安全实例。"""
    return AsymptoticSafetyInstance(n_couplings=n_couplings)


if __name__ == "__main__":
    print("=" * 60)
    print("渐近安全实例（下游插件）")
    print("=" * 60)

    a_s = run_asymptotic_safety_instance(n_couplings=5)
    summary = a_s.summary()

    print("\n[实例假设]")
    for key, value in a_s.metadata.items():
        print(f"  {key}: {value}")

    print("\n[RG 不动点临界指数谱]")
    for i, theta in enumerate(summary["critical_exponents"]):
        print(f"  θ_{i} = {theta:.4f}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = a_s.to_rec_object()
    spec_obj = a_s.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
