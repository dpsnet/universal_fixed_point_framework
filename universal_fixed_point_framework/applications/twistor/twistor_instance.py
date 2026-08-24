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
twistor_instance.py

扭量理论（Twistor）散射运动学实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 扭量理论不是理论核心，只是抽象框架在 4D 无质量散射运动学谱上的一个算例。

实例假设（MH-Twistor）：
- 4D 无质量动量用旋量表示：p_{α\dot α} = λ_α \tilde λ_{\dot α}。
- 由旋量生成一组无质量外腿的动量，并计算 Lorentz 不变运动学量 s_{ij} = <ij>[ij]。
- 用角度旋量括号 |<ij>| 的取值作为谱源，构造谱算子 A 并验证 λ_i = exp(-μ_i)。
- 提供与弦论散射振幅模块的联动接口：用 (s,t) 调用 Veneziano / Virasoro-Shapiro 振幅。
"""

from __future__ import annotations

import sys
from pathlib import Path
from dataclasses import dataclass, field
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
_STRING_DIR = _PROJECT_ROOT / "applications" / "string_theory"
for _dir in (_SRC_DIR, _STRING_DIR):
    if str(_dir) not in sys.path:
        sys.path.insert(0, str(_dir))

from rec_category import RecObject
from spec_category import PositiveSpectralObject
import string_scattering_amplitude as scatt


_EPSILON = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


@dataclass
class TwistorInstance:
    """
    扭量实例：将 4D 无质量散射旋量运动学包装为递归系统。

    参数
    ----------
    n_particles : int
        外腿粒子数（至少为 2，默认 4）。
    seed : int | None
        旋量生成随机种子。
    metadata : dict
        实例假设元数据。
    """
    n_particles: int = 4
    seed: int | None = 42
    metadata: dict = field(default_factory=lambda: {
        "type": "twistor",
        "dimension": 4,
        "massless": True,
    })

    def __post_init__(self):
        if self.n_particles < 2:
            raise ValueError("n_particles 至少为 2")
        self.metadata.setdefault("n_particles", self.n_particles)
        self._rng = np.random.default_rng(self.seed)
        self._left_spinors = self._generate_spinors()
        # 对实动量，右手旋量取为左手旋量的副本（允许相差一个相位），
        # 以保证 p_i = λ_i \tilde λ_i^† 为 Hermitian 且 det(p_i)=0。
        self._right_spinors = self._left_spinors.copy()

    def _generate_spinors(self) -> np.ndarray:
        """生成 2 x n_particles 的复旋量矩阵，每列代表一个无质量外腿旋量。"""
        spinors = self._rng.standard_normal((2, self.n_particles)) + \
                  1j * self._rng.standard_normal((2, self.n_particles))
        # 归一化每列
        norms = np.linalg.norm(spinors, axis=0)
        norms = np.where(norms == 0, 1.0, norms)
        return spinors / norms

    def left_spinors(self) -> np.ndarray:
        """返回 λ_α（左手旋量）。"""
        return self._left_spinors.copy()

    def right_spinors(self) -> np.ndarray:
        """返回 \tilde λ_{\dot α}（右手旋量）。"""
        return self._right_spinors.copy()

    def momenta(self) -> np.ndarray:
        """
        返回 4D 动量张量，形状为 (n_particles, 2, 2)。
        每个 p_i = λ_i \tilde λ_i^† 是 2x2 Hermitian 矩阵。
        """
        momenta = np.zeros((self.n_particles, 2, 2), dtype=complex)
        for i in range(self.n_particles):
            momenta[i] = np.outer(self._left_spinors[:, i], self._right_spinors[:, i].conj())
        return momenta

    def angle_bracket(self, i: int, j: int) -> complex:
        """角度旋量括号 <ij> = λ_i^T ε λ_j。"""
        return complex(self._left_spinors[:, i].T @ _EPSILON @ self._left_spinors[:, j])

    def square_bracket(self, i: int, j: int) -> complex:
        """平方旋量括号 [ij] = \tilde λ_i^T ε \tilde λ_j。"""
        return complex(self._right_spinors[:, i].T @ _EPSILON @ self._right_spinors[:, j])

    def kinematic_invariant(self, i: int, j: int) -> float:
        """Mandelstam 型不变量 s_{ij} = |<ij>[ij]|。"""
        return float(np.abs(self.angle_bracket(i, j) * self.square_bracket(i, j)))

    def twistor_spectrum(self) -> np.ndarray:
        """返回所有无序旋量对的 |<ij>| 作为谱源。"""
        pairs = []
        for i in range(self.n_particles):
            for j in range(i + 1, self.n_particles):
                pairs.append(np.abs(self.angle_bracket(i, j)))
        return np.array(pairs, dtype=float)

    def transition_matrix(self) -> np.ndarray:
        """由角度旋量括号谱构造 Koopman 矩阵 K = diag(|<ij>| / max)。"""
        spectrum = self.twistor_spectrum()
        max_val = spectrum.max()
        if max_val <= 0:
            return np.eye(len(spectrum))
        lambdas = spectrum / max_val
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def scattering_amplitude(self, s: float, t: float, string_type: str = "open") -> float:
        """
        与弦论散射振幅模块联动。

        对给定 Mandelstam 变量 (s,t)，调用 Veneziano（open）或 Virasoro-Shapiro（closed）振幅。
        """
        if string_type == "open":
            return scatt.veneziano_amplitude(s, t)
        elif string_type == "closed":
            return scatt.virasoro_shapiro_amplitude(s, t)
        else:
            raise ValueError("string_type 必须是 'open' 或 'closed'")

    def to_rec_object(self) -> RecObject:
        """将扭量运动学谱递归表示为 Rec 对象。"""
        state_space = self.twistor_spectrum().reshape(-1, 1)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_particles": self.n_particles,
                **self.metadata,
                "type": "twistor_kinematics",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将扭量运动学谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_particles": self.n_particles,
            **self.metadata,
            "type": "twistor_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回扭量实例摘要。"""
        spectrum = self.twistor_spectrum()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "n_particles": self.n_particles,
                "seed": self.seed,
            },
            "twistor_spectrum": spectrum.tolist(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_twistor_instance(n_particles: int = 4) -> TwistorInstance:
    """便捷函数：创建并运行扭量实例。"""
    return TwistorInstance(n_particles=n_particles)


if __name__ == "__main__":
    print("=" * 60)
    print("扭量理论实例（下游插件）")
    print("=" * 60)

    tw = run_twistor_instance(n_particles=4)
    summary = tw.summary()

    print("\n[实例假设]")
    for key, value in tw.metadata.items():
        print(f"  {key}: {value}")

    print("\n[旋量运动学谱 |<ij>|]")
    print(f"  {np.round(summary['twistor_spectrum'], 4)}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[与弦论散射振幅联动]")
    s, t = 0.3, 0.5
    amp_open = tw.scattering_amplitude(s, t, string_type="open")
    amp_closed = tw.scattering_amplitude(s, t, string_type="closed")
    print(f"  A_open({s}, {t})   = {amp_open:.4f}")
    print(f"  A_closed({s}, {t}) = {amp_closed:.4f}")

    print("\n[抽象框架接口]")
    rec_obj = tw.to_rec_object()
    spec_obj = tw.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
