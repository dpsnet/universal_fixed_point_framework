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
layer_solv.py — Bun(Solv) 溶剂纤维模块
=========================================
介电连续模型 + 摩擦提升效应。
模拟溶剂环境对电子谱的介电屏蔽和摩擦修正。
"""

import numpy as np
from scipy import linalg

from .layer_base import FiberLayer
from .utils import convert_numpy, L_CORR_DEFAULT, k_B_eV


# 常见溶剂的介电常数和摩擦参数
SOLVENT_PARAMS = {
    "water":       {"epsilon_r": 78.4, "eta_cP": 0.89, "n_D": 1.333},
    "methanol":    {"epsilon_r": 32.7, "eta_cP": 0.54, "n_D": 1.329},
    "acetonitrile": {"epsilon_r": 37.5, "eta_cP": 0.37, "n_D": 1.344},
    "toluene":     {"epsilon_r": 2.38, "eta_cP": 0.56, "n_D": 1.497},
    "hexane":      {"epsilon_r": 1.88, "eta_cP": 0.30, "n_D": 1.375},
    "vacuum":      {"epsilon_r": 1.0,  "eta_cP": 0.0,  "n_D": 1.0},
}


class SolvLayer(FiberLayer):
    """Bun(Solv) — 溶剂纤维层。

    使用介电连续模型（Onsager 反应场 + Lippert-Mataga）估算
    溶剂对电子谱间隙的极化修正，以及溶剂摩擦对谱流 dissipation 的提升。
    """

    def __init__(self, solvent="water", l_corr=L_CORR_DEFAULT,
                 T_K=300.0, name="Solv"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=1,
            spectral_gap=0.0,
            dissipation_gamma=0.0,
        )
        self.solvent = solvent
        self.solvent_params = SOLVENT_PARAMS.get(
            solvent, SOLVENT_PARAMS["water"]
        )
        self.l_corr = l_corr
        self.T_K = T_K

    def _on_sager_reaction_field(self, mu_D=5.0, a0=3.0):
        """Onsager 反应场修正 [eV]。

        ΔE_solv = -(mu_D² / a₀³) · (ε_r - 1) / (2ε_r + 1)
        其中 mu_D 为气相偶极矩 [Debye]，a₀ 为腔半径 [Å]。
        """
        # Debye → e·Å: 1 D = 0.2082 e·Å
        mu_eA = mu_D * 0.2082
        eps = self.solvent_params["epsilon_r"]
        factor = (eps - 1.0) / (2.0 * eps + 1.0)
        # 能量单位：e·Å → eV 换算：1 e·Å 对应 14.4 eV
        return - (mu_eA ** 2 / a0 ** 3) * factor * 14.4

    def compute_spectral_flow(self, xi_range):
        """沿介电响应参数计算溶剂修正流。

        Parameters
        ----------
        xi_range : ndarray
            溶剂坐标（如介电常数的函数）。

        Returns
        -------
        flow : ndarray
            溶剂修正因子 F_solv。
        """
        kT = k_B_eV * self.T_K
        eps = self.solvent_params["epsilon_r"]
        eta = self.solvent_params["eta_cP"]
        flow = []
        for xi in xi_range:
            # 摩擦提升：eta 越大，dissipation 越强
            gamma_solv = eta * 0.01 * (1.0 + 0.1 * xi)
            # 介电屏蔽修正
            shielding = 1.0 + (eps - 1.0) / (2.0 * eps + 1.0) * np.exp(-abs(xi))
            F_solv = 1.0 + gamma_solv * shielding * kT
            flow.append(F_solv)
        return np.array(flow)

    def get_section(self, section_type="default"):
        """提取溶剂纤维截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "polarization", "friction"。

        Returns
        -------
        section : dict
        """
        delta_E = self._on_sager_reaction_field()
        if section_type == "polarization":
            mu_range = np.linspace(1, 10, 20)
            energies = []
            for mu in mu_range:
                e = self._on_sager_reaction_field(mu_D=mu)
                energies.append(e)
            return {
                "type": section_type,
                "mu_D_range": mu_range.tolist(),
                "delta_E_solv": energies,
                "solvent": self.solvent,
                "epsilon_r": self.solvent_params["epsilon_r"],
            }
        elif section_type == "friction":
            eta_range = np.linspace(0.0, 2.0, 20)
            xi_grid = np.linspace(-2, 2, 10)
            friction_profiles = {}
            for eta in eta_range:
                params = dict(self.solvent_params)
                params["eta_cP"] = eta
                self.solvent_params = params
                f_profile = self.compute_spectral_flow(xi_grid)
                friction_profiles[f"eta={eta:.2f}"] = f_profile.tolist()
            self.solvent_params = SOLVENT_PARAMS.get(
                self.solvent, SOLVENT_PARAMS["water"]
            )
            return {
                "type": section_type,
                "xi_grid": xi_grid.tolist(),
                "friction_profiles": friction_profiles,
                "base_solvent": self.solvent,
            }
        else:
            return {
                "type": section_type,
                "solvent": self.solvent,
                "epsilon_r": self.solvent_params["epsilon_r"],
                "viscosity_cP": self.solvent_params["eta_cP"],
                "refractive_index": self.solvent_params["n_D"],
                "on_sager_delta_E_eV": float(delta_E),
                "l_corr": self.l_corr,
                "T_K": self.T_K,
            }

    def get_summary(self):
        """概要：溶剂极化修正和摩擦参数。"""
        delta_E = self._on_sager_reaction_field()
        eta = self.solvent_params["eta_cP"]
        self.dissipation_gamma = eta * 0.01
        self.spectral_gap = float(abs(delta_E))
        summary = super().get_summary()
        summary["solvent"] = self.solvent
        summary["epsilon_r"] = self.solvent_params["epsilon_r"]
        summary["viscosity_cP"] = eta
        summary["on_sager_delta_E"] = float(delta_E)
        return summary
