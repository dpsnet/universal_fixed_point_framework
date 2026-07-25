"""
layer_intraionic.py — Bun(IntraIonic) 分子内 CT 纤维模块
===========================================================
复用 spectral_intraionic_dpa_model.py 的超交换逻辑：
  - D-π-A 推拉发色团紧束缚模型
  - McConnell 超交换机制
  - 提取有效耦合 J_eff 和电荷分离度 xi_intra
"""

import numpy as np
from scipy import linalg

from .layer_base import FiberLayer
from .utils import convert_numpy, L_CORR_DEFAULT


# D-π-A 体系典型参数
PARAMS = {
    "eps_D": 0.0,       # [eV] 给体位点能
    "eps_A": -1.2,      # [eV] 受体位点能
    "eps_B": 1.8,       # [eV] 桥位点能
    "t_DB": 1.2,        # [eV] 给体-桥耦合
    "t_BB": 2.0,        # [eV] 桥内相邻位点耦合
    "t_BA": 1.2,        # [eV] 桥-受体耦合
}

BRIDGE_PER_SITE_LENGTH = 2.4   # [Å] 每个 CH=CH 单元有效长度
BONUS_SITE_DIST = 4.0           # [Å] D-B1 / BN-A 间距


def _build_hamiltonian(N, params):
    """构建 D-N-Bridge-A 紧束缚 Hamiltonian (N+2 维矩阵)。"""
    dim = N + 2
    H = np.zeros((dim, dim))
    H[0, 0] = params["eps_D"]
    for i in range(1, N + 1):
        H[i, i] = params["eps_B"]
    H[N + 1, N + 1] = params["eps_A"]
    H[0, 1] = H[1, 0] = params["t_DB"]
    for i in range(1, N):
        H[i, i + 1] = H[i + 1, i] = params["t_BB"]
    H[N, N + 1] = H[N + 1, N] = params["t_BA"]
    return H


def _solve_dpa(N, params):
    """解 D-N-A 体系，返回有效耦合和 CT 特征。"""
    H = _build_hamiltonian(N, params)
    eigvals, eigvecs = linalg.eigh(H)
    E_GS = eigvals[0]
    E_CT = eigvals[1]
    J_eff = (E_CT - E_GS) / 2.0
    psi_GS = eigvecs[:, 0]
    rho_D = psi_GS[0] ** 2
    xi_intra = np.clip(1.0 - rho_D, 0.0, 1.0)
    return {
        "N_bridge": N,
        "E_GS": float(E_GS),
        "E_CT": float(E_CT),
        "J_eff": float(J_eff),
        "xi_intra": float(xi_intra),
        "hbar_omega_CT": float(E_CT - E_GS),
    }


def _compute_distance(N):
    """桥长度 N 对应的 D-A 距离。"""
    return BONUS_SITE_DIST + N * BRIDGE_PER_SITE_LENGTH


class IntraIonicLayer(FiberLayer):
    """Bun(IntraIonic) — 分子内电荷转移纤维层。

    基于 McConnell 超交换模型，模拟 D-π-A 推拉发色团中
    分子内 CT 耦合 J_intra 的指数衰减标度。
    """

    def __init__(self, params=None, l_corr=L_CORR_DEFAULT, name="IntraIonic"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=2,
            spectral_gap=0.0,
            dissipation_gamma=0.03,
        )
        self.params = params if params is not None else PARAMS.copy()
        self.l_corr = l_corr

    def compute_spectral_flow(self, xi_range):
        """沿桥长度 N（连续化）计算有效耦合流 J_eff(N)。

        Parameters
        ----------
        xi_range : ndarray
            连续化的桥长度 [Å]。

        Returns
        -------
        flow : ndarray
            有效耦合 J_eff [eV]。
        """
        flow = []
        for R in xi_range:
            N = max(1, int(round((R - BONUS_SITE_DIST) / BRIDGE_PER_SITE_LENGTH)))
            result = _solve_dpa(N, self.params)
            flow.append(result["J_eff"])
        return np.array(flow)

    def get_section(self, section_type="default"):
        """提取分子内 CT 截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "decay_scan", "sensitivity"。

        Returns
        -------
        section : dict
        """
        if section_type == "decay_scan":
            N_range = np.arange(1, 11)
            results = []
            for N in N_range:
                res = _solve_dpa(N, self.params)
                res["R_DA"] = _compute_distance(N)
                results.append(res)
            J_list = np.array([r["J_eff"] for r in results])
            coeffs = np.polyfit(N_range, np.log(np.abs(J_list) + 1e-30), 1)
            beta = -coeffs[0]
            l_corr_site = 1.0 / beta if beta > 0 else 0.0
            return {
                "type": section_type,
                "N_range": N_range.tolist(),
                "results": convert_numpy(results),
                "beta_per_site": float(beta),
                "l_corr_site": float(l_corr_site),
                "l_corr_angstrom": float(l_corr_site * BRIDGE_PER_SITE_LENGTH),
            }
        elif section_type == "sensitivity":
            Delta_E = self.params["eps_B"] - self.params["eps_D"]
            t_BB_range = np.linspace(0.3, 1.7, 8)
            sensitivity = []
            for t_BB in t_BB_range:
                p = self.params.copy()
                p["t_BB"] = t_BB
                J_t = [_solve_dpa(N, p)["J_eff"] for N in range(1, 11)]
                J_arr = np.array(J_t)
                coeffs = np.polyfit(np.arange(1, 11), np.log(np.abs(J_arr) + 1e-30), 1)
                beta = -coeffs[0]
                sensitivity.append({
                    "t_BB": float(t_BB),
                    "ratio_t_BB_DeltaE": float(t_BB / Delta_E),
                    "beta": float(beta),
                    "l_corr_A": float(BRIDGE_PER_SITE_LENGTH / beta),
                })
            return {"type": section_type,
                    "sensitivity": convert_numpy(sensitivity)}
        else:
            N_mid = 5
            res = _solve_dpa(N_mid, self.params)
            res["R_DA"] = _compute_distance(N_mid)
            return {"type": section_type,
                    "result": convert_numpy(res)}

    def get_summary(self):
        """概要：有效耦合衰减分析。"""
        N_range = np.arange(1, 11)
        J_list = np.array([_solve_dpa(N, self.params)["J_eff"]
                           for N in N_range])
        coeffs = np.polyfit(N_range, np.log(np.abs(J_list) + 1e-30), 1)
        beta = -coeffs[0]
        l_corr_A = BRIDGE_PER_SITE_LENGTH / beta if beta > 0 else 0.0
        self.spectral_gap = float(J_list[0])
        summary = super().get_summary()
        summary["beta_per_site"] = float(beta)
        summary["l_corr_angstrom"] = float(l_corr_A)
        summary["bridge_site_length"] = BRIDGE_PER_SITE_LENGTH
        return summary
