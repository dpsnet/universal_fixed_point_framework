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
layer_reac.py — Bun(Reac) 电子基态纤维模块
==============================================
复用 spectral_hh2_reaction.py 的谱分析逻辑：
  - 3-中心 Hückel 模型 + H₂ / H₃ 参数化
  - HOMO-LUMO 谱间隙 δ_spec(s) 沿 IRC
  - 光谱修正因子 F_spec = 1 + exp(-δ_spec/kT)
"""

import numpy as np
from scipy import linalg

from .layer_base import FiberLayer
from .utils import (
    k_B_eV, L_CORR_DEFAULT, convert_numpy, spectral_gap_from_eigenvalues
)


# ── H₂ / H₃ 分子参数 ──
R_eq = 0.741        # [Å] H₂ 平衡键长
BETA_0 = -6.3       # [eV] Hückel 跳跃积分 @ R_eq
ALPHA_0 = -13.6     # [eV] H 1s 库仑积分
R_TS = 0.93         # [Å] H₃ 过渡态 H-H 距离
R_limit = 6.0       # [Å] 渐近极限
SIGMA = 0.3         # IRC 宽度参数


def _irc_params(s):
    """共线 Ha--Hb--Hc 的 IRC 路径参数化。"""
    c = np.arctanh(1 - 2 * (R_TS - R_eq) / (R_limit - R_eq))
    R_ab = R_eq + (R_limit - R_eq) * (1 - np.tanh(s / SIGMA + c)) / 2
    R_bc = R_eq + (R_limit - R_eq) * (1 - np.tanh(-s / SIGMA + c)) / 2
    return R_ab, R_bc, R_ab + R_bc


def _hopping(R, l_corr):
    """β(R) = β₀ exp(-(R - R_eq) / ℓ_corr)"""
    if R < 0.3:
        R = 0.3
    return BETA_0 * np.exp(-(R - R_eq) / l_corr)


def _solve_h3(R_ab, R_bc, l_corr=L_CORR_DEFAULT):
    """求解 H₃ 3-中心 Hückel Hamiltonian。"""
    R_ac = R_ab + R_bc
    H = np.array([
        [ALPHA_0, _hopping(R_ab, l_corr), _hopping(R_ac, l_corr) * 0.3],
        [_hopping(R_ab, l_corr), ALPHA_0, _hopping(R_bc, l_corr)],
        [_hopping(R_ac, l_corr) * 0.3, _hopping(R_bc, l_corr), ALPHA_0],
    ])
    return linalg.eigh(H)


class ReacLayer(FiberLayer):
    """Bun(Reac) — 电子基态（反应）纤维层。

    使用 3-中心 Hückel 模型模拟 H + H₂ 反应沿 IRC 的谱演变。
    """

    def __init__(self, l_corr=L_CORR_DEFAULT, T_K=300.0, name="Reac"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=3,
            spectral_gap=0.0,
            dissipation_gamma=0.01,
        )
        self.l_corr = l_corr
        self.T_K = T_K

    def compute_spectral_flow(self, xi_range):
        """沿 IRC 坐标 s 计算谱流 F_spec(s)。

        Parameters
        ----------
        xi_range : ndarray
            IRC 坐标 s 数组。

        Returns
        -------
        flow : ndarray
            每个 s 点的 F_spec 值。
        """
        flow = []
        kT = k_B_eV * self.T_K
        for s in xi_range:
            R_ab, R_bc, _ = _irc_params(s)
            eigvals, _ = _solve_h3(R_ab, R_bc, self.l_corr)
            delta = spectral_gap_from_eigenvalues(eigvals)
            if delta > 0:
                F_spec = 1.0 + np.exp(-delta / kT)
            else:
                F_spec = 2.0
            flow.append(F_spec)
        return np.array(flow)

    def get_section(self, section_type="default"):
        """提取反应 IRC 截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "ts", "irc_scan"。

        Returns
        -------
        section : dict
        """
        s_range = np.linspace(-4, 4, 80)
        results = []
        for s in s_range:
            R_ab, R_bc, R_ac = _irc_params(s)
            eigvals, eigvecs = _solve_h3(R_ab, R_bc, self.l_corr)
            delta = spectral_gap_from_eigenvalues(eigvals)
            results.append({
                "s": float(s),
                "R_ab": float(R_ab),
                "R_bc": float(R_bc),
                "R_ac": float(R_ac),
                "delta_spec": delta,
                "eigvals": eigvals.tolist(),
            })
        ts_idx = int(np.argmin(np.abs(s_range)))
        return {
            "type": section_type,
            "l_corr": self.l_corr,
            "T_K": self.T_K,
            "irc_results": convert_numpy(results),
            "ts_index": ts_idx,
            "ts_delta": results[ts_idx]["delta_spec"],
        }

    def get_summary(self):
        """返回概要字典，包含反应参数和 TS 谱间隙。"""
        s_range = np.linspace(-4, 4, 80)
        ts_idx = int(np.argmin(np.abs(s_range)))
        R_ab, R_bc, _ = _irc_params(s_range[ts_idx])
        eigvals, _ = _solve_h3(R_ab, R_bc, self.l_corr)
        delta = spectral_gap_from_eigenvalues(eigvals)
        self.spectral_gap = delta
        summary = super().get_summary()
        summary["l_corr"] = self.l_corr
        summary["T_K"] = self.T_K
        return summary
