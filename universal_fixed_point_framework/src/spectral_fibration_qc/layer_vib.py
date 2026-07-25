"""
layer_vib.py — Bun(Vib) 振动耦合纤维模块
===========================================
简谐振动谱 + Franck-Condon 因子计算。
实现振动纤维层，模拟分子振动模式对电子谱的调制。
"""

import numpy as np
from scipy import linalg
from scipy.special import factorial

from .layer_base import FiberLayer
from .utils import convert_numpy, gaussian_broaden, L_CORR_DEFAULT


# 典型振动频率 [eV] 与对应折合质量 [amu]
VIB_MODES = {
    "C-H_stretch": {"omega": 0.37, "mu": 1.0},   # ~3000 cm⁻¹
    "C=O_stretch": {"omega": 0.26, "mu": 12.0},  # ~2100 cm⁻¹
    "C-C_stretch": {"omega": 0.17, "mu": 6.0},   # ~1400 cm⁻¹
    "C-H_bend":    {"omega": 0.15, "mu": 1.0},   # ~1200 cm⁻¹
    "skeletal":    {"omega": 0.06, "mu": 24.0},  # ~500 cm⁻¹
}


def _fc_overlap(v, delta_q, omega, mu):
    """计算 Franck-Condon 重叠 <0|v>。

    使用移位谐振子模型：S = ½ μ ω (Δq)² / ħ
    FC(v) = exp(-S/2) * S^{v/2} / √(v!)

    Parameters
    ----------
    v : int
        振动量子数。
    delta_q : float
        平衡位置位移 [Å]。
    omega : float
        振动频率 [eV]。
    mu : float
        折合质量 [amu]。

    Returns
    -------
    fc : float
        Franck-Condon 因子 √(FC 强度)。
    """
    # amu → eV·s²/Å² 换算因子: 1 amu = 1.036427e-4 eV·s²/Å²
    mu_ev = mu * 1.036427e-4
    hbar = 6.582119569e-16  # eV·s
    S = 0.5 * mu_ev * omega * delta_q ** 2 / hbar
    if v < 0:
        return 0.0
    return np.exp(-S / 2) * (S ** (v / 2)) / np.sqrt(factorial(v))


class VibLayer(FiberLayer):
    """Bun(Vib) — 振动耦合纤维层。

    模拟 Franck-Condon 活性振动模式对电子谱的精细结构调制。
    """

    def __init__(self, modes=None, l_corr=L_CORR_DEFAULT, name="Vib"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=len(modes) if modes else len(VIB_MODES),
            spectral_gap=0.05,
            dissipation_gamma=0.02,
        )
        self.modes = modes if modes is not None else VIB_MODES.copy()
        self.l_corr = l_corr

    def compute_spectral_flow(self, xi_range):
        """计算振动谱流（总 FC 展宽包络）。

        Parameters
        ----------
        xi_range : ndarray
            能量网格 [eV]。

        Returns
        -------
        flow : ndarray
            展宽后的振动谱包络。
        """
        energies = []
        weights = []
        for mode_name, mode_params in self.modes.items():
            omega = mode_params["omega"]
            mu = mode_params["mu"]
            delta_q = self.l_corr * 0.5  # 位移与 ℓ_corr 关联
            n_quanta = min(int(omega / 0.06) + 2, 5)
            for v in range(n_quanta):
                E = v * omega
                fc = _fc_overlap(v, delta_q, omega, mu)
                energies.append(E)
                weights.append(fc ** 2)
        return gaussian_broaden(
            np.array(energies), np.array(weights), xi_range, sigma=0.02
        )

    def get_section(self, section_type="default"):
        """提取振动谱截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "modes", "fc_analysis"。

        Returns
        -------
        section : dict
        """
        x_grid = np.linspace(0, 1.0, 500)
        spectrum = self.compute_spectral_flow(x_grid)
        modes_out = {}
        for name, mp in self.modes.items():
            omega = mp["omega"]
            mu = mp["mu"]
            delta_q = self.l_corr * 0.5
            n_quanta = min(int(omega / 0.06) + 2, 5)
            fc_list = []
            for v in range(n_quanta):
                fc = _fc_overlap(v, delta_q, omega, mu)
                fc_list.append({"v": v, "E_eV": float(v * omega),
                                "FC_factor": float(fc)})
            modes_out[name] = fc_list
        return {
            "type": section_type,
            "energy_grid": x_grid.tolist(),
            "spectrum": spectrum.tolist(),
            "modes": convert_numpy(modes_out),
            "l_corr": self.l_corr,
        }

    def get_summary(self):
        """概要：返回振动模式和总 FC 活性。"""
        total_fc = 0.0
        n_modes = len(self.modes)
        for mp in self.modes.values():
            omega = mp["omega"]
            mu = mp["mu"]
            delta_q = self.l_corr * 0.5
            for v in range(5):
                fc = _fc_overlap(v, delta_q, omega, mu)
                total_fc += fc ** 2
        summary = super().get_summary()
        summary["n_modes"] = n_modes
        summary["total_fc_strength"] = float(min(total_fc, 1.0))
        summary["max_freq_eV"] = max(m["omega"] for m in self.modes.values())
        return summary
