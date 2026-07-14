"""
geodesic_instance.py

引力测地线分形实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 引力测地线不是理论核心，只是抽象框架在强引力场几何下的一个算例。

实例假设（MH4）：
- 时空背景：Schwarzschild 或 Kerr 度规的离散化
- 递归系统：测地线方程的数值积分
- 谱对象：测地线偏差算子的 Lyapunov 指数谱 / 真实度规的 epicyclic 频率谱
- 轨道函子 O 由时空对称性诱导

本实现提供三种模式：
- "synthetic"：简化的测地线偏差压缩模型（保留原有行为）。
- "schwarzschild"：使用 Schwarzschild 圆轨道径向/垂直 epicyclic 频率作为谱源。
- "kerr"：使用 Kerr 圆轨道径向/垂直 epicyclic 频率作为谱源。
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

import schwarzschild_geodesic_verification as schw
import kerr_geodesic_verification as kerr
import geodesic_integrator as gint
import kerr_geodesic_integrator as kgint


@dataclass
class GeodesicInstance:
    """
    引力测地线实例：将测地线偏差方程 / 真实度规 epicyclic 频率包装为递归系统。

    参数
    ----------
    n_states : int
        synthetic 模式下的离散化状态数。
    curvature_coupling : float
        synthetic 模式下的曲率耦合强度。
    dt : float
        synthetic 模式下的固有时离散步长。
    metric : str
        度规模式："synthetic"、"schwarzschild" 或 "kerr"。
    radii : list[float] | None
        Schwarzschild / Kerr 模式下的圆轨道半径列表。若为空，使用默认半径。
    spin : float
        Kerr 模式下的无量纲自旋 a（|a| < 1）。
    metadata : dict
        实例假设元数据。
    """
    n_states: int = 4
    curvature_coupling: float = 0.1
    dt: float = 0.1
    metric: str = "synthetic"
    radii: list[float] | None = None
    spin: float = 0.0
    prograde: bool = True
    metadata: dict = field(default_factory=lambda: {
        "type": "gravitational_geodesic",
        "equation": "geodesic_deviation",
    })

    def __post_init__(self):
        if self.metric not in {"synthetic", "schwarzschild", "kerr"}:
            raise ValueError("metric 必须是 'synthetic'、'schwarzschild' 或 'kerr'")
        if self.metric == "synthetic":
            self.metadata.setdefault("spacetime", "synthetic_discretized")
        elif self.metric == "schwarzschild":
            if self.radii is None:
                self.radii = [7.0, 8.0, 10.0, 15.0]
            self.radii = [float(r) for r in self.radii]
            if any(r < schw.isco_radius() for r in self.radii):
                raise ValueError(f"Schwarzschild 稳定圆轨道要求 r >= {schw.isco_radius()}")
            self.n_states = 2 * len(self.radii)
            self.metadata.setdefault("spacetime", "Schwarzschild")
        else:  # kerr
            if not -1.0 < self.spin < 1.0:
                raise ValueError("Kerr 自旋 a 必须满足 |a| < 1")
            if self.radii is None:
                r_isco = kerr.isco_radius(self.spin)
                self.radii = [max(r_isco + 0.5, 6.0), 8.0, 10.0, 15.0]
            self.radii = [float(r) for r in self.radii]
            if any(r < kerr.isco_radius(self.spin) for r in self.radii):
                raise ValueError(
                    f"Kerr 顺行稳定圆轨道要求 r >= {kerr.isco_radius(self.spin):.4f}"
                )
            self.n_states = 2 * len(self.radii)
            self.metadata.setdefault("spacetime", "Kerr")
            self.metadata.setdefault("spin", self.spin)

    def deviation_matrix(self) -> np.ndarray:
        """
        synthetic 模式下构造简化的测地线偏差演化矩阵。
        """
        n = self.n_states
        K = -self.curvature_coupling * np.diag(np.arange(1, n + 1))
        M = np.eye(2 * n)
        M[:n, n:] += self.dt * np.eye(n)
        M[n:, :n] += self.dt * K
        M2 = M @ M
        position_block = M2[:n, :n]
        eigenvalues = np.linalg.eigvals(position_block)
        scale = np.max(np.abs(eigenvalues))
        if scale > 1.0:
            position_block = position_block / (scale + 1e-10)
        return position_block

    def _raw_frequencies(self) -> np.ndarray:
        """返回真实度规模式下用于构造谱的原始 epicyclic 频率。"""
        if self.metric == "schwarzschild":
            return schw.spectrum(self.radii)
        elif self.metric == "kerr":
            return kerr.spectrum(self.radii, self.spin, self.prograde)
        raise RuntimeError("_raw_frequencies 仅在 schwarzschild / kerr 模式下调用")

    def transition_matrix(self) -> np.ndarray:
        """返回用于 Rec 对象的转移矩阵（特征值在 (0,1]）。"""
        if self.metric == "synthetic":
            M = self.deviation_matrix()
            eigenvalues, eigenvectors = np.linalg.eig(M)
            eigenvalues = np.real(eigenvalues)
            eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
            return eigenvectors @ np.diag(eigenvalues) @ np.linalg.inv(eigenvectors)

        # 真实度规模式：K = exp(-frequency) 并归一化到最大特征值为 1
        frequencies = self._raw_frequencies()
        lambdas = np.exp(-frequencies)
        max_lambda = lambdas.max()
        if max_lambda > 0:
            lambdas = lambdas / max_lambda
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.linalg.eigvals(K)
        eigenvalues = np.real(eigenvalues)
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def lyapunov_exponents(self) -> np.ndarray:
        """
        返回谱对应的特征指数。

        - synthetic：μ_i = -ln(|λ_i|) / (2 dt)
        - 真实度规：原始 epicyclic 频率 Ω_r / Ω_θ
        """
        if self.metric == "synthetic":
            K = self.transition_matrix()
            eigenvalues = np.linalg.eigvals(K)
            return -np.log(np.abs(eigenvalues)) / (2 * self.dt)
        return np.sort(self._raw_frequencies())

    def numerical_validation(self, tolerance: float = 5e-2) -> dict | None:
        """
        对真实度规模型进行数值积分验证。

        - schwarzschild：调用 Schwarzschild 数值积分器。
        - kerr：调用 Kerr 数值积分器。
        - synthetic：返回 None。
        """
        if self.metric == "schwarzschild":
            return gint.validate_epicyclic_frequencies(self.radii, tolerance=tolerance)
        elif self.metric == "kerr":
            return kgint.validate_epicyclic_frequencies(
                self.radii, a=self.spin, prograde=self.prograde, tolerance=tolerance
            )
        return None

    def lyapunov_diagnosis(self, n_periods: int = 20) -> dict:
        """
        数值计算最大 Lyapunov 指数并输出 LACI 风格诊断。

        对可积测地线系统（Schwarzschild / Kerr），λ_max ≈ 0 → LACI LOW。

        返回
        -------
        dict：包含 λ_max、风险等级、解释。
        """
        r_test = self.radii[0] if self.radii else 10.0

        if self.metric == "schwarzschild":
            lyap = gint.maximum_lyapunov_exponent(r_test, n_periods=n_periods)
        elif self.metric == "kerr":
            lyap = kgint.maximum_lyapunov_exponent(
                r_test, a=self.spin, n_periods=n_periods, prograde=self.prograde
            )
        else:
            return {"lambda_max": np.nan, "risk": "N/A", "interpretation": "synthetic 模式不支持"}

        lambda_max = lyap["lambda_max"]
        abs_lam = abs(lambda_max)

        if abs_lam < 1e-8:
            risk = "low"
            interp = "Lyapunov 指数接近 0，系统可积，无混沌吸引子捕获风险。"
        elif abs_lam < 1e-4:
            risk = "medium"
            interp = "Lyapunov 指数中等，可能存在弱混沌或数值噪声。"
        else:
            risk = "high"
            interp = "Lyapunov 指数显著非零，可能存在混沌吸引子，过拟合风险高。"

        return {
            "lambda_max": lambda_max,
            "risk": risk,
            "interpretation": interp,
            "metric": self.metric,
            "r_test": r_test,
        }

    def to_rec_object(self) -> RecObject:
        """将测地线偏差演化表示为 Rec 对象。"""
        if self.metric == "synthetic":
            state_space = np.arange(self.n_states).reshape(-1, 1).astype(float)
        else:
            # 真实度规：状态空间用 (半径, 频率) 对表示
            radii = np.asarray(self.radii)
            freqs = self._raw_frequencies()
            state_space = np.column_stack([np.repeat(radii, 2), freqs])
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_states": self.n_states,
                **self.metadata,
                "type": "geodesic_deviation",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将测地线谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_states": self.n_states,
            **self.metadata,
            "type": "geodesic_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回引力测地线实例摘要。"""
        K = self.transition_matrix()
        A = self.spectral_operator()
        mu = np.diag(A)
        lambdas = np.diag(K) if K.ndim == 2 and K.shape[0] == K.shape[1] else np.linalg.eigvals(K)
        summary = {
            "parameters": {
                "metric": self.metric,
                "n_states": self.n_states,
            },
            "lyapunov_exponents": np.sort(self.lyapunov_exponents()).tolist(),
            "koopman_eigenvalues": np.sort(np.real(lambdas)).tolist(),
            "spectral_operator_eigenvalues": np.sort(mu).tolist(),
        }
        if self.metric != "synthetic":
            summary["parameters"]["radii"] = self.radii
            summary["numerical_validation"] = self.numerical_validation()
            if self.metric == "kerr":
                summary["parameters"]["spin"] = self.spin
        else:
            summary["parameters"]["curvature_coupling"] = self.curvature_coupling
            summary["parameters"]["dt"] = self.dt
        return summary


def run_geodesic_instance(metric: str = "synthetic", n_states: int = 4) -> GeodesicInstance:
    """便捷函数：创建并运行引力测地线实例。"""
    if metric == "synthetic":
        return GeodesicInstance(n_states=n_states)
    return GeodesicInstance(metric=metric)


if __name__ == "__main__":
    for metric in ("synthetic", "schwarzschild", "kerr"):
        print("=" * 60)
        print(f"引力测地线实例（下游插件）— metric = {metric}")
        print("=" * 60)

        if metric == "synthetic":
            geo = run_geodesic_instance(metric=metric, n_states=4)
        elif metric == "kerr":
            geo = run_geodesic_instance(metric=metric)
            geo.spin = 0.5
        else:
            geo = run_geodesic_instance(metric=metric)

        summary = geo.summary()

        print("\n[实例假设]")
        for key, value in geo.metadata.items():
            print(f"  {key}: {value}")

        print("\n[Lyapunov / epicyclic 指数]")
        for i, lyap in enumerate(summary["lyapunov_exponents"]):
            print(f"  模式 {i}: λ = {lyap:.4f}")

        print("\n[谱对应验证]")
        mu = np.array(summary["spectral_operator_eigenvalues"])
        lambdas = np.array(summary["koopman_eigenvalues"])
        lambdas_from_exp = np.sort(np.exp(-mu))
        print(f"  Koopman 特征值 λ_i: {np.round(lambdas, 4)}")
        print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
        diff = np.linalg.norm(lambdas - lambdas_from_exp)
        print(f"  差异 (Frobenius)   : {diff:.2e}")

        print("\n[抽象框架接口]")
        rec_obj = geo.to_rec_object()
        spec_obj = geo.to_spectral_object()
        print(f"  Rec 对象维数      : {rec_obj.n_points}")
        print(f"  Spectral 对象维数 : {spec_obj.dim}")
        print()
