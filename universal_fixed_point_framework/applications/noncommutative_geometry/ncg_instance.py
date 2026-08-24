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
ncg_instance.py

非交换几何（Connes 谱三元组）实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 非交换几何不是理论核心，只是抽象框架在谱三元组 Dirac 谱上的一个算例。

实例假设（MH-NCG）：
- 采用有限维谱三元组 (A, H, D)，其中 D 为 Dirac 算子（Hermitian）。
- 用 |D| 或 D² 的正本征值作为谱源，构造谱算子 A 并验证 λ_i = exp(-μ_i)。
- 原型阶段默认给出一组Dirac本征值（如 [0, 1, 2, 3, 4]），支持用户传入任意谱三元组本征值。
- 提供谱作用（spectral action）的离散近似接口：S_Λ(D) = Tr(f(D²/Λ²))。
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


def _default_dirac_eigenvalues(n: int) -> np.ndarray:
    """默认 Dirac 本征值：0, 1, 2, ..., n-1。"""
    return np.arange(n, dtype=float)


@dataclass
class NCGInstance:
    """
    非交换几何实例：将谱三元组 Dirac 本征值谱包装为递归系统。

    参数
    ----------
    n_points : int
        Dirac 本征值个数（当未提供 eigenvalues 时使用）。
    eigenvalues : list[float] | None
        可选自定义 Dirac 算子本征值列表。若提供，n_points 被忽略。
    cutoff : float
        谱作用截断 Λ（默认 2.0）。
    metadata : dict
        实例假设元数据。
    """
    n_points: int = 5
    eigenvalues: list[float] | None = None
    cutoff: float = 2.0
    metadata: dict = field(default_factory=lambda: {
        "type": "noncommutative_geometry",
        "structure": "spectral_triple",
        "operator": "Dirac",
    })

    def __post_init__(self):
        if self.eigenvalues is not None:
            self._eigenvalues = np.array(self.eigenvalues, dtype=float)
            self.n_points = len(self._eigenvalues)
        else:
            if self.n_points < 1:
                raise ValueError("n_points 必须为正整数")
            self._eigenvalues = _default_dirac_eigenvalues(self.n_points)
        if self.cutoff <= 0:
            raise ValueError("cutoff 必须为正")
        self.metadata.setdefault("n_points", self.n_points)
        self.metadata.setdefault("cutoff", self.cutoff)

    def dirac_eigenvalues(self) -> np.ndarray:
        """返回 Dirac 算子本征值。"""
        return self._eigenvalues.copy()

    def absolute_eigenvalues(self) -> np.ndarray:
        """返回 |D| 的本征值（非负）。"""
        return np.abs(self._eigenvalues)

    def transition_matrix(self) -> np.ndarray:
        """由 |D| 构造 Koopman 矩阵 K = diag(|λ_i| / |λ|_max)。"""
        abs_eigs = self.absolute_eigenvalues()
        max_eig = abs_eigs.max()
        if max_eig <= 0:
            return np.eye(self.n_points)
        lambdas = abs_eigs / max_eig
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def spectral_action(self, cutoff: float | None = None) -> float:
        """
        离散近似谱作用：S_Λ(D) = Σ_i f(λ_i² / Λ²)。

        这里取 f(x) = exp(-x) 作为光滑截断函数。
        """
        lam = cutoff if cutoff is not None else self.cutoff
        eigs = self.dirac_eigenvalues()
        return float(np.sum(np.exp(-(eigs / lam) ** 2)))

    def to_rec_object(self) -> RecObject:
        """将 NCG Dirac 谱递归表示为 Rec 对象。"""
        state_space = self.absolute_eigenvalues().reshape(-1, 1)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_points": self.n_points,
                **self.metadata,
                "type": "ncg_dirac_spectrum",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将 NCG Dirac 谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_points": self.n_points,
            **self.metadata,
            "type": "ncg_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回 NCG 实例摘要。"""
        eigs = self.dirac_eigenvalues()
        abs_eigs = self.absolute_eigenvalues()
        K = self.transition_matrix()
        A = self.spectral_operator()
        return {
            "parameters": {
                "n_points": self.n_points,
                "cutoff": self.cutoff,
            },
            "dirac_eigenvalues": eigs.tolist(),
            "absolute_eigenvalues": abs_eigs.tolist(),
            "spectral_action": self.spectral_action(),
            "koopman_eigenvalues": np.diag(K).tolist(),
            "spectral_operator_eigenvalues": np.diag(A).tolist(),
        }


def run_ncg_instance(n_points: int = 5) -> NCGInstance:
    """便捷函数：创建并运行 NCG 实例。"""
    return NCGInstance(n_points=n_points)


if __name__ == "__main__":
    print("=" * 60)
    print("非交换几何实例（下游插件）")
    print("=" * 60)

    ncg = run_ncg_instance(n_points=5)
    summary = ncg.summary()

    print("\n[实例假设]")
    for key, value in ncg.metadata.items():
        print(f"  {key}: {value}")

    print("\n[Dirac 本征值与谱作用]")
    for i, lam in enumerate(summary["dirac_eigenvalues"]):
        print(f"  λ_{i} = {lam:.4f}")
    print(f"  谱作用 S_Λ(D) ≈ {summary['spectral_action']:.4f}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = ncg.to_rec_object()
    spec_obj = ncg.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
