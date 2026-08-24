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
bsm_oblique_parameters.py

BSM 第4代轻子对电弱精密观测量（Peskin-Takeuchi S/T 参数）的贡献计算。

参考文献：
- Peskin & Takeuchi (1992), PRD 46, 381 — S/T/U 参数定义
- He, polonsky, Su (2001), PRD 64, 053004 — 第四代费米子对 S/T 的贡献
- PDG 2024 — 电弱精密拟合约束

公式：
    对质量 m₁, m₂ 的 SU(2) 双分量费米子：
    ΔS = (1/(6π)) · [1 - Y · log(m₁²/m₂²)]
    ΔT = (1/(16π s_w² c_w² m_Z²)) · [m₁² + m₂² - (2m₁²m₂²/(m₁²-m₂²))·log(m₁²/m₂²)]

    其中 Y = 2(Q - T₃) 是弱超荷，s_w² = sin²θ_W, c_w² = cos²θ_W。
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass


# ===========================================================================
# 标准模型电弱参数
# ===========================================================================

M_Z_GEV = 91.1876           # Z 玻色子质量
M_W_GEV = 80.379            # W 玻色子质量
ALPHA_EM = 1.0 / 127.955   # 精细结构常数 (Z pole)
SIN2_THETA_W = 0.23122     # 有效弱混合角 sin²θ_W
COS2_THETA_W = 1.0 - SIN2_THETA_W
S_W = np.sqrt(SIN2_THETA_W)
C_W = np.sqrt(COS2_THETA_W)

# PDG 2024 电弱拟合约束 (68% CL)
PDG_S_REF = 0.05     # S 参考值 (以 m_H=125 GeV, m_t=173 GeV 为基准)
PDG_T_REF = 0.08     # T 参考值
PDG_S_ERROR = 0.08   # S 误差
PDG_T_ERROR = 0.06   # T 误差
PDG_S_T_CORR = 0.93  # S-T 相关系数


@dataclass
class FourthGenFermionDoublet:
    """
    第四代费米子双分量 (ν₄, L₄) 对 S/T 参数的贡献。

    参数
    ----------
    m_l4 : float
        带电轻子质量 (GeV)，默认框架预言 1470 GeV
    m_nu4 : float
        中性轻子质量 (GeV)，默认与 L4 简并（SU(2) 对称性要求）
    y_l4 : float
        L4 的弱超荷（左手 SU(2) 双分量：Y = -1）
    y_nu4 : float
        ν₄ 的弱超荷（Y = -1，与 L4 在相同双分量中）
    """
    m_l4: float = 1470.0
    m_nu4: float = 1470.0
    y_l4: float = -1.0
    y_nu4: float = -1.0

    def delta_S(self) -> float:
        """
        第四代轻子对 S 参数的贡献。

        对 SU(2) 双分量 (ν₄, L₄)：
            ΔS = (1/(6π)) · [1 - Y · log(m_l4²/m_nu4²)]

        当 m_l4 = m_nu4 时，ΔS = 1/(6π) ≈ 0.053
        当质量分裂时，log 项贡献额外 S。
        """
        mass_ratio_sq = (self.m_l4 / self.m_nu4) ** 2
        if mass_ratio_sq <= 0:
            return 0.0
        log_term = np.log(mass_ratio_sq)

        # 双分量的 Y 平均
        y_avg = (self.y_l4 + self.y_nu4) / 2.0

        delta_s = (1.0 / (6.0 * np.pi)) * (1.0 - y_avg * log_term)
        return float(delta_s)

    def delta_T(self) -> float:
        """
        第四代轻子对 T 参数的贡献。

        ΔT = (N_c / (16π s_w² c_w² m_Z²)) ·
             [m_l4² + m_nu4² - (2 m_l4² m_nu4²/(m_l4² - m_nu4²)) · log(m_l4²/m_nu4²)]

        对色单态 (N_c = 1) 的轻子。
        当 m_l4 = m_nu4 时 ΔT = 0（SU(2) 对称性保护）。
        """
        N_c = 1  # 轻子是色单态
        m1_sq = self.m_l4 ** 2
        m2_sq = self.m_nu4 ** 2
        dm_sq = m1_sq - m2_sq

        if abs(dm_sq) < 1e-10:
            # 简并极限：ΔT = 0（SU(2) 对称性保护）
            return 0.0

        prefactor = N_c / (16.0 * np.pi * SIN2_THETA_W * COS2_THETA_W * M_Z_GEV ** 2)

        mass_term = m1_sq + m2_sq
        if abs(dm_sq) > 1e-10:
            mass_term -= (2.0 * m1_sq * m2_sq / dm_sq) * np.log(m1_sq / m2_sq)

        return float(prefactor * mass_term)

    def summary(self) -> dict:
        """
        完整 S/T 参数贡献报告。
        """
        ds = self.delta_S()
        dt = self.delta_T()

        # 与 PDG 约束的偏差（联合椭圆拟合）
        s_offset = ds - PDG_S_REF
        t_offset = dt - PDG_T_REF

        # 简化 χ²（不计 S-T 相关性）
        chi2_s = (s_offset / PDG_S_ERROR) ** 2
        chi2_t = (t_offset / PDG_T_ERROR) ** 2

        return {
            "m_l4_GeV": self.m_l4,
            "m_nu4_GeV": self.m_nu4,
            "delta_S": ds,
            "delta_T": dt,
            "PDG_S_REF": PDG_S_REF,
            "PDG_T_REF": PDG_T_REF,
            "S_offset": s_offset,
            "T_offset": t_offset,
            "chi2_S": chi2_s,
            "chi2_T": chi2_t,
            "chi2_total": chi2_s + chi2_t,
            "consistent": (chi2_s + chi2_t) < 5.99,  # 95% CL for 2 dof
        }


def mass_splitting_scan(m_l4_base: float = 1470.0,
                         splitting_ratios: np.ndarray | None = None) -> list[dict]:
    """
    质量分裂扫描：ΔT 随 m_nu4/m_l4 的变化。

    SU(2) 对称性要求双分量质量接近，但小分裂可通过
    seesaw 机制或额外 Yukawa 耦合产生。

    返回 ΔS, ΔT 与质量分裂比的关系。
    """
    if splitting_ratios is None:
        splitting_ratios = np.logspace(-3, 0, 10)  # 0.001 到 1

    results = []
    for ratio in splitting_ratios:
        m_nu4 = m_l4_base * ratio
        fg = FourthGenFermionDoublet(m_l4=m_l4_base, m_nu4=m_nu4)
        ds = fg.delta_S()
        dt = fg.delta_T()
        results.append({
            "m_l4_GeV": m_l4_base,
            "m_nu4_GeV": m_nu4,
            "mass_ratio": ratio,
            "delta_S": ds,
            "delta_T": dt,
        })
    return results


def exclusion_estimate(delta_S: float, delta_T: float) -> str:
    """
    基于 S/T 参数的电弱精密检验排除判断。

    PDG 2024 联合拟合约束（68% CL）：
        S = 0.05 ± 0.08, T = 0.08 ± 0.06, 相关系数 = 0.93

    使用 95% CL 椭圆约束进行粗略排除判断。
    """
    s_off = delta_S - PDG_S_REF
    t_off = delta_T - PDG_T_REF
    rho = PDG_S_T_CORR

    # 卡方统计量（含相关）
    denom = 1 - rho ** 2
    if denom <= 0:
        return "undefined"

    chi2 = (s_off ** 2 / PDG_S_ERROR ** 2 +
            t_off ** 2 / PDG_T_ERROR ** 2 -
            2 * rho * s_off * t_off / (PDG_S_ERROR * PDG_T_ERROR)) / denom

    if chi2 < 2.30:    # 68% CL for 2 dof
        return "allowed (68% CL)"
    elif chi2 < 5.99:  # 95% CL for 2 dof
        return "allowed (95% CL)"
    elif chi2 < 9.21:  # 99% CL for 2 dof
        return "tension (>95% CL)"
    else:
        return f"excluded (χ²={chi2:.1f}, >99% CL)"


if __name__ == "__main__":
    print("=" * 70)
    print("第四代轻子对电弱精密观测量 S/T 参数的贡献")
    print("=" * 70)

    # 默认参数（简并双分量）
    fg = FourthGenFermionDoublet()
    summary = fg.summary()
    print(f"\nL4 质量: {summary['m_l4_GeV']:.0f} GeV")
    print(f"ν4 质量: {summary['m_nu4_GeV']:.0f} GeV")
    print(f"ΔS = {summary['delta_S']:.4f}  (PDG ref: {PDG_S_REF})")
    print(f"ΔT = {summary['delta_T']:.4f}  (PDG ref: {PDG_T_REF})")
    print(f"χ² = {summary['chi2_total']:.2f}")

    status = exclusion_estimate(summary['delta_S'], summary['delta_T'])
    print(f"电弱精密检验: {status}")

    # 质量分裂扫描
    print(f"\n质量分裂扫描 (m_L4 固定 = {1470} GeV):")
    print(f"{'m_nu4/m_L4':<12} {'ΔS':<10} {'ΔT':<10} {'排除状态':<20}")
    print("-" * 55)
    for entry in mass_splitting_scan()[:6]:
        r = entry["mass_ratio"]
        ds = entry["delta_S"]
        dt = entry["delta_T"]
        status = exclusion_estimate(ds, dt)
        print(f"{r:<12.4f} {ds:<10.4f} {dt:<10.4f} {status:<20}")
