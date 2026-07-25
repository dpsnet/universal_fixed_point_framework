"""
layer_spin.py — Bun(Spin) 自旋耦合纤维模块
=============================================
SOC（自旋-轨道耦合）估算。
模拟重金属/自由基体系的旋轨耦合对谱间隙的修正。
"""

import numpy as np
from scipy import linalg

from .layer_base import FiberLayer
from .utils import convert_numpy, L_CORR_DEFAULT


# 原子 SOC 常数 [eV]
SOC_CONSTANTS = {
    "H":  0.0,
    "C":  0.006,    # C 2p
    "N":  0.011,    # N 2p
    "O":  0.019,    # O 2p
    "F":  0.034,    # F 2p
    "S":  0.052,    # S 3p
    "Cl": 0.073,    # Cl 3p
    "Se": 0.36,     # Se 4p
    "Br": 0.39,     # Br 4p
    "I":  0.63,     # I 5p
    "Ru": 0.12,     # Ru 4d
    "Pt": 0.45,     # Pt 5d
    "Au": 0.51,     # Au 6s
}

# 典型自由基的自旋密度分布
RADICAL_FRAGMENTS = {
    "methyl":     {"C": 0.7, "H": 0.1},
    "phenoxyl":   {"O": 0.4, "C": 0.15},
    "nitroxide":  {"N": 0.5, "O": 0.3},
    "benzyl":     {"C_alpha": 0.6, "ring_C": 0.1},
}


class SpinLayer(FiberLayer):
    """Bun(Spin) — 自旋耦合纤维层。

    估算重原子 SOC 和自由基自旋密度对谱间隙的修正，
    基于单中心 SOC 近似：Δ_{SOC} = Σ_i ζ_i · ρ_i，
    其中 ζ_i 为原子 SOC 常数，ρ_i 为自旋密度。
    """

    def __init__(self, atoms=None, soc_constants=None,
                 l_corr=L_CORR_DEFAULT, name="Spin"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=2,
            spectral_gap=0.02,
            dissipation_gamma=0.01,
        )
        self.atoms = atoms if atoms is not None else ["C", "H", "O"]
        self.soc_constants = (soc_constants if soc_constants is not None
                              else SOC_CONSTANTS)
        self.l_corr = l_corr

    def _compute_soc_gap(self):
        """估算 SOC 修正后的谱间隙。

        使用有效单中心 SOC 公式：
          Δ_{SOC} = √(Δ₀² + (Σ_i ζ_i·ρ_i)²) - Δ₀
        其中 Δ₀ 为未修正间隙。
        """
        delta_0 = 0.5  # 基准谱间隙 [eV]
        soc_sum = 0.0
        for atom in self.atoms:
            zeta = self.soc_constants.get(atom, 0.0)
            rho = 0.2  # 典型自旋密度
            soc_sum += zeta * rho
        delta_soc = np.sqrt(delta_0 ** 2 + soc_sum ** 2) - delta_0
        return delta_soc

    def compute_spectral_flow(self, xi_range):
        """沿 SOC 强度参数计算自旋修正流。

        Parameters
        ----------
        xi_range : ndarray
            SOC 缩放因子数组。

        Returns
        -------
        flow : ndarray
            自旋修正因子 F_spin。
        """
        delta_0 = 0.5
        base_soc = self._compute_soc_gap()
        flow = []
        for xi in xi_range:
            scaling = 1.0 + xi * 0.1
            soc_eff = base_soc * scaling
            gap = delta_0 + soc_eff
            F_spin = 1.0 + np.exp(-gap / 0.025)  # ~300K thermal
            flow.append(F_spin)
        return np.array(flow)

    def get_section(self, section_type="default"):
        """提取自旋耦合截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "atom_analysis", "soc_scan"。

        Returns
        -------
        section : dict
        """
        if section_type == "atom_analysis":
            atom_data = []
            for atom in self.atoms:
                zeta = self.soc_constants.get(atom, 0.0)
                atom_data.append({
                    "atom": atom,
                    "soc_constant_eV": zeta,
                    "soc_contribution": zeta * 0.2,
                })
            return {"type": section_type,
                    "atoms": convert_numpy(atom_data)}
        elif section_type == "soc_scan":
            zeta_range = np.linspace(0, 0.5, 30)
            soc_gaps = []
            for zeta in zeta_range:
                delta_0 = 0.5
                rho = 0.2
                soc_sum = zeta * rho
                gap = np.sqrt(delta_0 ** 2 + soc_sum ** 2) - delta_0
                soc_gaps.append(float(gap))
            return {
                "type": section_type,
                "zeta_range": zeta_range.tolist(),
                "soc_gaps": soc_gaps,
            }
        else:
            soc_gap = self._compute_soc_gap()
            heavy_atoms = [
                a for a in self.atoms
                if self.soc_constants.get(a, 0.0) > 0.05
            ]
            return {
                "type": section_type,
                "atoms": self.atoms,
                "soc_constants": {
                    a: self.soc_constants.get(a, 0.0)
                    for a in self.atoms
                },
                "delta_SOC": float(soc_gap),
                "n_heavy_atoms": len(heavy_atoms),
                "l_corr": self.l_corr,
            }

    def get_summary(self):
        """概要：SOC 修正和有效自旋间隙。"""
        soc_gap = self._compute_soc_gap()
        self.spectral_gap = float(0.5 + soc_gap)
        summary = super().get_summary()
        summary["delta_SOC"] = float(soc_gap)
        summary["heavy_atoms"] = [
            a for a in self.atoms
            if self.soc_constants.get(a, 0.0) > 0.05
        ]
        return summary
