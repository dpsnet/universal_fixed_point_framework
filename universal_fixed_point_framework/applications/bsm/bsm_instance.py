"""
bsm_instance.py

超出标准模型（BSM）新费米子谱系的下游插件实现。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- BSM 新费米子不是理论核心，只是抽象框架在新规范群/新代数下的一个算例。

实例假设（MH5）：
- 在 SM 规范群基础上增加一个暗物质 U(1)_X 或 SU(2)_X
- 新增一个矢量型重费米子扇区（vector-like fermion，VLF）
- 轨道函子 O 在新增扇区上的取值由新规范群轨道决定
- 不需要重构 SM 推导链，只需调整实例假设层参数

本实现展示：从 SM 实例出发，仅更换轨道函子/扇区设置，
即可预言新的重费米子质量谱。
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

import bsm_experiment_constraints as constraints
import bsm_cross_sections as xs


@dataclass
class BSMInstance:
    """
    BSM 新费米子实例：通过调整轨道函子生成新的重费米子质量谱。

    参数
    ----------
    ifs_c, ifs_p : np.ndarray
        IFS 参数，与 SM 实例相同。
    q0 : float
        q 参数基准值。
    v_MeV : float
        Higgs VEV。
    bsm_charge : float
        新费米子在新规范群 U(1)_X 下的荷。
    n_generations : int
        新费米子的代次（通常为 3，与 SM 一致）。
    metadata : dict
        实例假设元数据。
    """
    ifs_c: np.ndarray = field(default_factory=lambda: np.array([0.3450, 0.2901]))
    ifs_p: np.ndarray = field(default_factory=lambda: np.array([0.9000, 0.1000]))
    q0: float = 0.3127
    v_MeV: float = 246000.0
    bsm_charge: float = 2.0
    n_generations: int = 3
    metadata: dict = field(default_factory=lambda: {
        "type": "BSM_vector_like_fermion",
        "new_gauge_group": "U(1)_X",
        "bsm_sector": "vector-like fermion",
    })

    def __post_init__(self):
        self.ifs_c = np.asarray(self.ifs_c, dtype=float)
        self.ifs_p = np.asarray(self.ifs_p, dtype=float)

    def sector_qs(self) -> np.ndarray:
        """
        扩展扇区 q 参数：SM 四个扇区 + BSM 重费米子扇区。
        BSM 扇区 q 由新规范荷决定：q_bsm = -bsm_charge * q0。
        """
        return np.array([
            -self.q0,           # Up
            self.q0,            # Down
            -3 * self.q0,       # Lepton
            -5 * self.q0,       # Neutrino
            -self.bsm_charge * self.q0,  # BSM
        ])

    def compute_sector_weights(self) -> np.ndarray:
        """计算扩展后的扇区测度。"""
        qs = self.sector_qs()
        weights = []
        for q in qs:
            w = np.sum(self.ifs_p ** q) if q != 0 else 1.0
            weights.append(w)
        weights = np.array(weights)
        return weights / np.sum(weights)

    def effective_contraction(self) -> np.ndarray:
        """计算各扇区有效收缩因子。"""
        qs = self.sector_qs()
        c_eff = np.zeros(len(qs))
        for s, q in enumerate(qs):
            p_q = self.ifs_p ** q
            c_eff[s] = np.sum(p_q * self.ifs_c) / np.sum(p_q)
        return c_eff

    def bsm_masses(self) -> dict[str, float]:
        """
        计算 BSM 新费米子的三代质量（简化模型）。

        假设新费米子质量标度由扇区测度和几何级数代内因子决定：
            m_{bsm,k} = y_bsm * (μ_bsm / μ_up) * (1/c_eff_bsm)^{k-1} * v / √2
        其中 y_bsm 取 top Yukawa 量级作为基准。
        """
        sector_weights = self.compute_sector_weights()
        c_eff = self.effective_contraction()
        bsm_index = 4

        # 以 top 质量为基准标度
        m_top = 173100.0
        y_top = m_top * np.sqrt(2.0) / self.v_MeV
        y_bsm = y_top * (sector_weights[0] / sector_weights[bsm_index])

        masses = {}
        k_arr = np.arange(1, self.n_generations + 1)
        intra = (1.0 / c_eff[bsm_index]) ** (k_arr - 1)
        for gen, k in enumerate(k_arr):
            m = y_bsm * intra[gen] * self.v_MeV / np.sqrt(2.0)
            masses[f"VLF_{gen+1}"] = m
        return masses

    def cross_sections(self, coupling: float = 1.0) -> dict:
        """
        计算最轻 BSM 粒子的近似截面/遗迹密度。

        返回热遗迹密度、LHC 对产生截面与自旋无关直接探测截面，
        便于与实验灵敏度快速对比。
        """
        masses = self.bsm_masses()
        if not masses:
            return {}
        lightest_mass_MeV = min(masses.values())
        return {
            "mass_MeV": lightest_mass_MeV,
            "mass_GeV": lightest_mass_MeV / 1_000.0,
            "thermal_relic_density": xs.thermal_relic_density(
                lightest_mass_MeV, coupling=coupling
            ),
            "lhc_pair_production": xs.lhc_pair_production_cross_section(
                lightest_mass_MeV
            ),
            "direct_detection_si": xs.direct_detection_si_cross_section(
                lightest_mass_MeV, coupling=coupling
            ),
        }

    def experimental_constraints(
        self,
        dark_matter_candidate_mass_MeV: float | None = None,
        annihilation_cross_section_cm3_per_s: float | None = None,
        spin_independent_cross_section_cm2: float | None = None,
        coupling: float = 1.0,
    ) -> dict:
        """
        与 LHC/暗物质实验约束对接。

        默认使用最轻的 BSM 粒子作为暗物质候选者。
        """
        return constraints.check_all(
            self.bsm_masses(),
            dark_matter_candidate_mass_MeV,
            annihilation_cross_section_cm3_per_s,
            spin_independent_cross_section_cm2,
            coupling,
        )

    def to_rec_object(self) -> RecObject:
        """将 BSM 实例的 IFS 结构表示为 Rec 对象。"""
        state_space = np.arange(len(self.ifs_c)).reshape(-1, 1).astype(float)
        K = np.column_stack([self.ifs_p for _ in range(len(self.ifs_p))])
        K = K / K.sum(axis=0, keepdims=True)
        return RecObject(
            state_space=state_space,
            evolution=K,
            time_semigroup="N",
            metadata={
                "bsm_charge": self.bsm_charge,
                **self.metadata,
                "type": "BSM_IFS",
            },
        )

    def to_spectral_object(self) -> PositiveSpectralObject:
        """将 BSM 质量谱表示为 Spec 对象。"""
        masses = self.bsm_masses()
        mass_values = np.array(list(masses.values()))
        mass_values = np.maximum(mass_values, 1e-30)
        max_mass = mass_values.max()
        lambdas = mass_values / max_mass
        mu = -np.log(lambdas)
        A = np.diag(mu)
        spec_obj = PositiveSpectralObject(operator_A=A)
        spec_obj.metadata = {
            "type": "BSM_mass_spectrum",
            "particles": list(masses.keys()),
            **self.metadata,
        }
        return spec_obj

    def summary(self) -> dict:
        """返回 BSM 实例摘要。"""
        sector_weights = self.compute_sector_weights()
        c_eff = self.effective_contraction()
        masses = self.bsm_masses()
        return {
            "parameters": {
                "ifs_c": self.ifs_c.tolist(),
                "ifs_p": self.ifs_p.tolist(),
                "q0": self.q0,
                "bsm_charge": self.bsm_charge,
                "n_generations": self.n_generations,
            },
            "sector_weights": sector_weights.tolist(),
            "effective_contraction": c_eff.tolist(),
            "bsm_masses_MeV": masses,
            "cross_sections": self.cross_sections(),
            "experimental_constraints": self.experimental_constraints(),
        }


def run_bsm_instance(bsm_charge: float = 2.0) -> BSMInstance:
    """便捷函数：创建并运行 BSM 实例。"""
    return BSMInstance(bsm_charge=bsm_charge)


if __name__ == "__main__":
    print("=" * 60)
    print("BSM 新费米子实例（下游插件）")
    print("=" * 60)

    bsm = run_bsm_instance(bsm_charge=2.0)
    summary = bsm.summary()

    print("\n[实例假设]")
    for key, value in bsm.metadata.items():
        print(f"  {key}: {value}")

    print("\n[扩展扇区测度]")
    sector_names = ["Up", "Down", "Lepton", "Neutrino", "BSM_VLF"]
    for s, name in enumerate(sector_names):
        print(f"  {name:<12}: μ = {summary['sector_weights'][s]:.6f}")

    print("\n[BSM 重费米子质量预测 / MeV]")
    for name, m in summary['bsm_masses_MeV'].items():
        print(f"  {name}: {m:.2f} MeV = {m/1000:.2f} GeV")

    print("\n[实验约束对接（原型近似）]")
    ec = summary["experimental_constraints"]
    print(f"  LHC VLF 下限: {ec['lhc']['limit_GeV']:.1f} GeV")
    for name, info in ec['lhc']['per_particle'].items():
        status = "通过" if info["pass"] else "排除"
        print(f"    {name}: {info['mass_GeV']:.1f} GeV — {status}")
    print(f"  遗迹密度通过: {ec['relic_density']['pass']}")
    print(f"  直接探测通过: {ec['direct_detection']['pass']}")
    print(f"  整体通过: {ec['overall_pass']}")

    print("\n[抽象框架接口]")
    rec_obj = bsm.to_rec_object()
    spec_obj = bsm.to_spectral_object()
    print(f"  Rec 对象维数      : {rec_obj.n_points}")
    print(f"  Spectral 对象维数 : {spec_obj.dim}")
