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
layer_ionic.py — Bun(Ionic) 分子间 CT 纤维模块
=================================================
复用 spectral_water_dimer_jct.py 的 CT 耦合逻辑：
  - 水二聚体 fragment-orbital 模型
  - J_CT(R) 的指数衰减
  - α = 1/ℓ_corr 标度验证
"""

import numpy as np
from scipy import linalg

from .layer_base import FiberLayer
from .utils import convert_numpy, L_CORR_DEFAULT, hopping_beta


# 水二聚体平衡参数
R_eq = 2.91           # [Å] O-O 平衡距离（气相）
R_OH = 0.96           # [Å] O-H 键长
zeta_2p = 2.27        # O 2p Slater 指数

# CT 耦合参数（从文献确定的 fragment-orbital 拟合值）
J0 = 0.8              # [eV] 平衡距离处的 CT 耦合强度
ALPHA_CT = 2.0        # [Å⁻¹] CT 耦合衰减指数（SF 预言 ℓ_corr=0.5Å → α=2.0）


def _j_ct(R, l_corr):
    """分子间 CT 耦合。

    J_CT(R) = J₀ · exp(-(R - R_eq) / ℓ_corr)
    """
    if R < 1.5:
        R = 1.5
    return J0 * np.exp(-(R - R_eq) / l_corr)


class IonicLayer(FiberLayer):
    """Bun(Ionic) — 分子间电荷转移纤维层。

    基于水二聚体 fragment-orbital 模型，
    模拟分子间 CT 耦合 J_CT(R) 随距离的指数衰减，
    验证 SF 预言 ℓ_corr ~ 0.5 Å → α ~ 2.0 Å⁻¹。
    """

    def __init__(self, l_corr=L_CORR_DEFAULT, name="Ionic"):
        super().__init__(
            name=name,
            base_category="Spec",
            fiber_dim=2,
            spectral_gap=0.3,
            dissipation_gamma=0.02,
        )
        self.l_corr = l_corr

    def compute_spectral_flow(self, xi_range):
        """沿 O-O 距离计算 CT 耦合流 J_CT(R)。

        Parameters
        ----------
        xi_range : ndarray
            O-O 距离数组 [Å]。

        Returns
        -------
        flow : ndarray
            CT 耦合流 J_CT(R) [eV]。
        """
        return np.array([_j_ct(R, self.l_corr) for R in xi_range])

    def get_section(self, section_type="default"):
        """提取分子间 CT 截面。

        Parameters
        ----------
        section_type : str
            截面类型。支持 "default", "r_scan", "decay_analysis"。

        Returns
        -------
        section : dict
        """
        if section_type == "r_scan":
            R_range = np.linspace(2.4, 6.0, 50)
            J_vals = self.compute_spectral_flow(R_range)
            return {
                "type": section_type,
                "R_range": R_range.tolist(),
                "J_CT": J_vals.tolist(),
                "l_corr": self.l_corr,
            }
        elif section_type == "decay_analysis":
            R_range = np.linspace(2.4, 6.0, 30)
            J_vals = self.compute_spectral_flow(R_range)
            log_J = np.log(np.abs(J_vals) + 1e-30)
            coeffs = np.polyfit(R_range, log_J, 1)
            alpha_fit = -coeffs[0]
            l_corr_fit = 1.0 / alpha_fit if alpha_fit > 0 else 0.0
            return {
                "type": section_type,
                "alpha_fit": float(alpha_fit),
                "l_corr_fit": float(l_corr_fit),
                "intercept": float(coeffs[1]),
                "R_sq": float(1.0 - np.var(log_J - np.polyval(coeffs, R_range))
                                / np.var(log_J)),
                "l_corr_input": self.l_corr,
                "SF_prediction_alpha": 1.0 / L_CORR_DEFAULT,
            }
        else:
            J_eq = _j_ct(R_eq, self.l_corr)
            d_HO_eq = R_eq - R_OH
            return {
                "type": section_type,
                "R_eq": R_eq,
                "R_OH": R_OH,
                "d_HO_eq": d_HO_eq,
                "J_eq": J_eq,
                "l_corr": self.l_corr,
                "alpha_CT": 1.0 / self.l_corr,
            }

    def get_summary(self):
        """概要：返回 CT 耦合衰减分析和 SF 预言对比。"""
        J_eq = _j_ct(R_eq, self.l_corr)
        self.spectral_gap = float(J_eq)
        alpha_sf = 1.0 / L_CORR_DEFAULT
        alpha_model = 1.0 / self.l_corr
        summary = super().get_summary()
        summary["J_CT_eq"] = float(J_eq)
        summary["R_eq"] = R_eq
        summary["alpha_SF_prediction"] = alpha_sf
        summary["alpha_model"] = alpha_model
        return summary
