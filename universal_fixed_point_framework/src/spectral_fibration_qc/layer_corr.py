"""
layer_corr.py — Bun(Corr) 电子关联纤维模块
=============================================
实现谱间隙压制截断 + 关联修正逻辑，
参考 Fulvene 锥形交叉和 begusic 分析中的电子关联效应。
"""

import numpy as np
from scipy import linalg

from .layer_base import FiberLayer
from .utils import convert_numpy, L_CORR_DEFAULT, k_B_eV


class CorrLayer(FiberLayer):
    """Bun(Corr) — 电子关联纤维层。

    模拟 Fulvene 锥形交叉 2-态 2-模 LVC 模型，
    通过梯度差和导数耦合参数捕获电子关联对谱间隙的压制效应。
    """

    def __init__(self, kappa=1.0, lam=0.8, l_corr=L_CORR_DEFAULT,
                 T_K=300.0, name="Corr"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=2,
            spectral_gap=0.0,
            dissipation_gamma=0.05,
        )
        self.kappa = kappa          # 调谐模耦合强度 [eV/Å]
        self.lam = lam              # 耦合模强度 [eV/Å]
        self.l_corr = l_corr
        self.T_K = T_K

    def _h_eff(self, x, y):
        """Fulvene S0/S1 有效 Hamiltonian。"""
        return np.array([
            [self.kappa * x, self.lam * y],
            [self.lam * y, -self.kappa * x],
        ])

    def compute_spectral_flow(self, xi_range):
        """沿基坐标计算谱间隙压制流。

        在锥形交叉附近，谱间隙 δ_spec 被压制到极小值，
        产生 ⟨ℓ_corr⟩ 标度的关联修正。

        Parameters
        ----------
        xi_range : ndarray
            基坐标（围绕 CI 的角度参数）。

        Returns
        -------
        flow : ndarray
            关联修正因子 F_corr = 1 + exp(-δ_spec / kT)。
        """
        flow = []
        kT = k_B_eV * self.T_K
        for theta in xi_range:
            x = 0.1 * np.cos(theta)
            y = 0.1 * np.sin(theta)
            H = self._h_eff(x, y)
            eigvals = linalg.eigvalsh(H)
            delta = float(eigvals[1] - eigvals[0])
            if delta > 0:
                F_corr = 1.0 + np.exp(-delta / kT)
            else:
                F_corr = 2.0
            flow.append(F_corr)
        return np.array(flow)

    def get_section(self, section_type="default"):
        """提取关联修正截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "ci_scan", "gap_landscape"。

        Returns
        -------
        section : dict
        """
        if section_type == "ci_scan":
            theta_range = np.linspace(0, 2 * np.pi, 50)
            radii = [0.05, 0.1, 0.2]
            scans = {}
            for r in radii:
                gaps = []
                for theta in theta_range:
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                    H = self._h_eff(x, y)
                    eigvals = linalg.eigvalsh(H)
                    gaps.append(float(eigvals[1] - eigvals[0]))
                scans[f"r={r}"] = {
                    "theta": theta_range.tolist(),
                    "delta_spec": gaps,
                }
            return {"type": section_type, "scans": convert_numpy(scans),
                    "kappa": self.kappa, "lam": self.lam}
        else:
            x_grid = np.linspace(-0.5, 0.5, 30)
            y_grid = np.linspace(-0.5, 0.5, 30)
            X, Y = np.meshgrid(x_grid, y_grid)
            gap_map = np.zeros_like(X)
            for i in range(len(x_grid)):
                for j in range(len(y_grid)):
                    H = self._h_eff(X[i, j], Y[i, j])
                    eigvals = linalg.eigvalsh(H)
                    gap_map[i, j] = eigvals[1] - eigvals[0]
            return {
                "type": section_type,
                "x_grid": x_grid.tolist(),
                "y_grid": y_grid.tolist(),
                "gap_map": gap_map.tolist(),
                "kappa": self.kappa,
                "lam": self.lam,
            }

    def get_summary(self):
        """概要：返回 CI 参数和最小间隙。"""
        x_test = np.linspace(-0.3, 0.3, 20)
        y_test = np.linspace(-0.3, 0.3, 20)
        min_gap = np.inf
        for x in x_test:
            for y in y_test:
                H = self._h_eff(x, y)
                eigvals = linalg.eigvalsh(H)
                gap = eigvals[1] - eigvals[0]
                if gap < min_gap:
                    min_gap = gap
        self.spectral_gap = float(min_gap)
        summary = super().get_summary()
        summary["kappa"] = self.kappa
        summary["lam"] = self.lam
        summary["min_gap"] = float(min_gap)
        return summary
