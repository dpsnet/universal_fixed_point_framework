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
string_instance.py

弦论拓扑递归实例的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 弦论不是理论核心，只是抽象框架在 Cl(9,1) / 超对称签名下的一个算例。

实例假设（MH3）：
- Clifford 签名 (p,q) = (9,1)（或 (10,0) 视超对称选择）
- 递归系统为 Eynard-Orantin 拓扑递归
- 谱曲线（spectral curve）诱导分形谱
- 轨道函子 O 由弦世界面模空间的对称性诱导

本实现采用简化模型：用弦振动模式的 Regge 轨迹作为离散谱，
展示拓扑递归的谱对应 λ_i = exp(-μ_i)。
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
import string_scattering_amplitude as scatt


@dataclass
class StringInstance:
    """
    弦论实例：将弦振动模式 / 拓扑递归包装为递归系统。

    参数
    ----------
    n_modes : int
        考虑的弦振动模式数。
    string_tension : float
        弦张力参数 α'。
    string_type : str
        "open" 或 "closed"，分别对应 Veneziano 与 Virasoro-Shapiro 振幅约定。
    metadata : dict
        实例假设元数据。
    """
    n_modes: int = 10
    string_tension: float = 1.0
    string_type: str = "open"
    metadata: dict = field(default_factory=lambda: {
        "type": "string_topological_recursion",
        "clifford_signature": (9, 1),
        "spectral_curve": "y^2 = x^2 - a^2",
        "moduli_space": "M_{g,n}",
    })

    def __post_init__(self):
        if self.string_type not in {"open", "closed"}:
            raise ValueError("string_type 必须是 'open' 或 'closed'")
        self.metadata.setdefault("string_type", self.string_type)

    def regge_spectrum(self) -> np.ndarray:
        """
        弦振动模式的 Regge 轨迹质量平方。

        open  : m_n^2 = (n - 1) / α'
        closed: m_n^2 = 4 (n - 1) / α'

        这里从 n=1 开始，基态为无质量粒子；n=0 对应快子，已被截断。
        """
        n = np.arange(1, self.n_modes + 1)
        if self.string_type == "open":
            return (n - 1) / self.string_tension
        return 4.0 * (n - 1) / self.string_tension

    def transition_matrix(self) -> np.ndarray:
        """
        构造弦模式递推的 Koopman 矩阵。
        简化为逐代衰减：K = diag(1, c, c^2, ...)。
        """
        masses2 = self.regge_spectrum()
        masses2 = np.maximum(masses2, 1e-30)
        max_mass2 = masses2.max()
        lambdas = masses2 / max_mass2
        # 将 λ 映射到 (0, 1]
        lambdas = np.clip(lambdas, 1e-12, 1.0)
        return np.diag(lambdas)

    def spectral_operator(self) -> np.ndarray:
        """由 K 计算谱算子 A = -log(K)。"""
        K = self.transition_matrix()
        eigenvalues = np.diag(K).copy()
        eigenvalues = np.clip(eigenvalues, 1e-12, 1.0)
        return np.diag(-np.log(eigenvalues))

    def tachyon_mass_squared(self) -> float:
        """当前约定下快子质量平方。"""
        if self.string_type == "open":
            return -1.0 / self.string_tension
        return -4.0 / self.string_tension

    def scattering_amplitude(self, s: float, t: float) -> float:
        """
        调用解析散射振幅。

        open  返回 Veneziano 振幅；closed 返回 Virasoro-Shapiro 振幅。
        """
        if self.string_type == "open":
            return scatt.veneziano_amplitude(s, t, alpha_prime=self.string_tension)
        return scatt.virasoro_shapiro_amplitude(s, t, alpha_prime=self.string_tension)

    def scattering_pole_masses(self) -> np.ndarray:
        """散射振幅 Regge 极点的物理质量平方（去掉快子）。"""
        return scatt.physical_pole_masses_squared(
            alpha_prime=self.string_tension,
            string_type=self.string_type,
            n_modes=self.n_modes,
        )

    def to_rec_object(self) -> RecObject:
        """将弦模式递归表示为 Rec 对象。"""
        state_space = np.arange(self.n_modes).reshape(-1, 1).astype(float)
        K = self.transition_matrix()
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "n_modes": self.n_modes,
                **self.metadata,
                "type": "string_modes",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将弦模式谱表示为 Spec 对象。"""
        A = self.spectral_operator()
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "n_modes": self.n_modes,
            **self.metadata,
            "type": "string_spectrum",
        }
        return spec_obj

    def summary(self) -> dict:
        """返回弦论实例摘要。"""
        masses2 = self.regge_spectrum()
        K = self.transition_matrix()
        A = self.spectral_operator()
        mu = np.diag(A)
        lambdas = np.diag(K)
        return {
            "parameters": {
                "n_modes": self.n_modes,
                "string_tension": self.string_tension,
                "string_type": self.string_type,
            },
            "mass_squared": masses2.tolist(),
            "scattering_pole_masses": self.scattering_pole_masses().tolist(),
            "koopman_eigenvalues": lambdas.tolist(),
            "spectral_operator_eigenvalues": mu.tolist(),
        }


def run_string_instance(n_modes: int = 10) -> StringInstance:
    """便捷函数：创建并运行弦论实例。"""
    return StringInstance(n_modes=n_modes)


if __name__ == "__main__":
    print("=" * 60)
    print("弦论实例（下游插件）")
    print("=" * 60)

    st = run_string_instance(n_modes=8)
    summary = st.summary()

    print("\n[实例假设]")
    for key, value in st.metadata.items():
        print(f"  {key}: {value}")

    print("\n[弦振动模式质量平方]")
    for i, m2 in enumerate(summary["mass_squared"]):
        print(f"  模式 {i}: m^2 = {m2:.4f}")

    print("\n[谱对应验证]")
    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    print(f"  Koopman 特征值 λ_i: {np.round(np.sort(lambdas), 4)}")
    print(f"  exp(-μ_i)          : {np.round(lambdas_from_exp, 4)}")
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)
    print(f"  差异 (Frobenius)   : {diff:.2e}")

    print("\n[散射振幅对接]")
    s_sample, t_sample = 0.3, 0.5
    amp = st.scattering_amplitude(s_sample, t_sample)
    print(f"  类型              : {st.string_type}")
    print(f"  快子质量平方      : {st.tachyon_mass_squared():.4f}")
    print(f"  A(s={s_sample}, t={t_sample})  : {amp:.4f}")
    print(f"  散射极点质量平方  : {np.round(summary['scattering_pole_masses'], 4)}")
    print(f"  Regge 谱质量平方  : {np.round(summary['mass_squared'], 4)}")
    pole_diff = np.linalg.norm(np.array(summary["mass_squared"]) - st.scattering_pole_masses())
    print(f"  极点-谱差异       : {pole_diff:.2e}")

    print("\n[抽象框架接口]")
    rec_obj = st.to_rec_object()
    spec_obj = st.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
