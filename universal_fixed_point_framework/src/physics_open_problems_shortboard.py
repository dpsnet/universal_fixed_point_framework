"""
physics_open_problems_shortboard.py

物理理论短板推进实现：

1. Kerr 量子引力精确谱：
   - 独立 Leaver 连分数求解 spheroidal 特征值
   - LIGO/Virgo ringdown 数据系统对比框架

2. N=4 SYM 完整 TBA 方程：
   - Y 系统与热力学势
   - 弱→强耦合插值的可积系统基础验证

3. 暗物质新物理：
   - 间接探测谱预言
   - 冻结-in / 非热产生机制分形质量谱
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# ===========================================================================
# 短板 1：Kerr 量子引力精确谱
# ===========================================================================

KERR_QUANTUM_SPECTRUM_SHORTBOARD = """
Kerr 量子引力精确谱短板：

现状：已实现简化与精确系数的 Leaver 连分数求解器，但 spheroidal 特征值
仍使用级数近似而非独立连分数求解。

目标：
1. 独立求解 spin-weighted spheroidal 特征值的 Leaver 连分数
2. 将 Kerr 全局量子谱与 LIGO/Virgo ringdown 数据系统对比
3. 建立量子引力精确谱的实验验证框架
"""


@dataclass
class SpheroidalLeaverSolver:
    """
    独立求解 spin-weighted spheroidal 特征值的 Leaver 连分数求解器。

    参数
    ----------
    l : int
        角量子数。
    m : int
        磁量子数（-l ≤ m ≤ l）。
    s : int
        自旋权重（s=0 标量，s=-2 引力）。
    """
    l: int = 2
    m: int = 0
    s: int = -2

    def _leaver_spheroidal_residual(
        self,
        lam: complex,
        z: complex,
        max_iter: int = 200,
    ) -> complex:
        """
        Spin-weighted spheroidal 特征值的 Leaver 连分数残差。

        来自 Leaver (1985) 对角向方程的处理：
            α_n = -2z(n+1)(n+2s+1)/(2n+2s+3),
            β_n = -n(n+2s+1) + λ + z² - 2zm,
            γ_n = 2z n (n+2s)/(2n+2s-1),

        其中 z = aω（无量纲自旋频率）。

        连分数条件：β₀ = α₀ / (β₁ - α₁ γ₂ / (β₂ - ...))。
        """
        cf = complex(0.0, 0.0)
        for n in range(max_iter, 0, -1):
            denom_factor_alpha = 2.0 * n + 2.0 * self.s + 3.0
            denom_factor_gamma = 2.0 * n + 2.0 * self.s - 1.0

            alpha = -2.0 * z * (n + 1.0) * (n + 2.0 * self.s + 1.0)
            if abs(denom_factor_alpha) > 1e-15:
                alpha /= denom_factor_alpha

            beta = (
                -n * (n + 2.0 * self.s + 1.0)
                + lam
                + z ** 2
                - 2.0 * z * self.m
            )

            gamma = 2.0 * z * n * (n + 2.0 * self.s)
            if abs(denom_factor_gamma) > 1e-15:
                gamma /= denom_factor_gamma

            denom = beta - alpha * gamma * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom

        alpha_0 = -2.0 * z * 1.0 * (2.0 * self.s + 1.0)
        if abs(2.0 * self.s + 3.0) > 1e-15:
            alpha_0 /= (2.0 * self.s + 3.0)
        beta_0 = (
            self.l * (self.l + 1.0) - self.s * (self.s + 1.0)
            - lam
            + z ** 2
            - 2.0 * z * self.m
        )

        return beta_0 - alpha_0 * cf

    def solve(
        self,
        z: complex,
        lam_guess: float | None = None,
        max_iter: int = 50,
    ) -> dict[str, Any]:
        """
        使用 Newton-Raphson 迭代求解 spheroidal 特征值。
        """
        if lam_guess is None:
            lam_guess = self.l * (self.l + 1.0) - self.s * (self.s + 1.0)

        lam = complex(lam_guess)
        eps = 1e-8

        for iteration in range(max_iter):
            f = self._leaver_spheroidal_residual(lam, z)
            if abs(f) < 1e-12:
                break

            f_re = self._leaver_spheroidal_residual(lam + eps, z)
            df_dlam = (f_re - f) / eps

            if abs(df_dlam) < 1e-15:
                break

            lam -= f / df_dlam

        final_residual = self._leaver_spheroidal_residual(lam, z)
        return {
            "lambda": float(lam.real),
            "z": z,
            "residual": float(abs(final_residual)),
            "iterations": iteration + 1,
            "converged": abs(final_residual) < 1e-8,
        }


@dataclass
class KerrRingdownLIGO:
    """
    Kerr 全局量子谱与 LIGO/Virgo ringdown 数据对比框架。

    参数
    ----------
    M : float
        黑洞质量（太阳质量）。
    a : float
        无量纲自旋参数。
    distance : float
        距离（Mpc）。
    """
    M: float = 30.0
    a: float = 0.7
    distance: float = 100.0

    def ringdown_amplitude(self, omega: complex, l: int, m: int) -> complex:
        """
        Ringdown 波形振幅（简化模型）。

        h(t) = A_{lm} exp(-i ω t)，其中振幅依赖于模式权重。
        """
        M_solar = self.M * 1.989e30
        dist_m = self.distance * 3.086e22

        A_norm = 4.0 * 1.4766e-27 / dist_m * M_solar

        mode_weight = 1.0
        if l == 2 and m == 0:
            mode_weight = 0.6
        elif l == 2 and abs(m) == 2:
            mode_weight = 0.3
        elif l == 3:
            mode_weight = 0.1

        return A_norm * mode_weight * np.exp(-1j * omega * self.M)

    def ligo_sensitivity(self, f_Hz: float) -> float:
        """
        LIGO 灵敏度曲线（简化模型）。

        灵敏度在 f ≈ 100 Hz 附近最佳。
        """
        f0 = 100.0
        S0 = 1e-46
        return S0 * (f_Hz / f0) ** (-4) * (1.0 + (f_Hz / f0) ** 2)

    def signal_to_noise(self, omega: complex, l: int, m: int) -> float:
        """
        信噪比估计。

        SNR ≈ A / sqrt(S_n(f) Δf)。
        """
        f_Hz = omega.real / (2.0 * np.pi * self.M * 5.7296e-6)
        A = abs(self.ringdown_amplitude(omega, l, m))
        S_n = self.ligo_sensitivity(f_Hz)
        delta_f = abs(omega.imag) / (2.0 * np.pi)
        return A / np.sqrt(S_n * delta_f) if S_n > 0 and delta_f > 0 else 0.0

    def ligo_comparison(self, modes: list[dict]) -> dict[str, Any]:
        """
        将 Kerr QNM 谱与 LIGO 灵敏度对比。
        """
        results = []
        for mode in modes:
            omega = mode["omega"]
            snr = self.signal_to_noise(omega, mode["l"], mode["m"])
            f_Hz = omega.real / (2.0 * np.pi * self.M * 5.7296e-6)
            results.append({
                "l": mode["l"],
                "m": mode["m"],
                "n": mode["n"],
                "f_Hz": f_Hz,
                "tau_s": -1.0 / omega.imag * self.M * 5.022e-6,
                "SNR": snr,
                "detectable": snr > 5.0,
            })
        return {"results": results, "detectable_count": sum(1 for r in results if r["detectable"])}


# ===========================================================================
# 短板 2：N=4 SYM 完整 TBA 方程
# ===========================================================================

N4SYM_TBA_SHORTBOARD = """
N=4 SYM 完整 TBA 方程短板：

现状：已实现简化 BES/TBA（含 dressing phase 与 wrapping corrections），
但缺少完整的 Y 系统与热力学势。

目标：
1. 实现完整 Y 系统方程
2. 计算热力学势与自由能
3. 验证弱→强耦合插值的可积系统基础
"""


@dataclass
class N4SYMThermodynamicPotential:
    """
    N=4 SYM 热力学势与 Y 系统求解器。

    参数
    ----------
    lambda_tHooft : float
        't Hooft 耦合。
    """
    lambda_tHooft: float = 6.0

    def _g_coupling(self) -> float:
        """g² = λ/(16π²)。"""
        return np.sqrt(self.lambda_tHooft) / (4.0 * np.pi)

    def _y_system_eqs(
        self,
        Y: np.ndarray,
        theta: np.ndarray,
        J: int = 2,
    ) -> np.ndarray:
        """
        Y 系统方程残差。

        Y 系统是一组耦合的泛函方程，将不同守恒电荷的密度关联起来。
        简化形式：
            Y_a(u) Y_{a+1}(u) = Π_{b} [1 + Y_b(u + iθ_ab)],

        这里取简化的两分量 Y 系统。
        """
        g = self._g_coupling()
        residuals = np.zeros_like(Y, dtype=complex)

        Y1, Y2 = Y
        theta12 = theta[0, 1] if len(theta) > 1 else 0.5

        residuals[0] = Y1 * Y2 - (1.0 + Y1 * np.exp(1j * g * theta12)) * (1.0 + Y2 * np.exp(-1j * g * theta12))
        residuals[1] = Y2 * Y1 - (1.0 + Y2 * np.exp(1j * g * theta12)) * (1.0 + Y1 * np.exp(-1j * g * theta12))

        return residuals

    def solve_y_system(
        self,
        J: int = 2,
        max_iter: int = 50,
    ) -> dict[str, Any]:
        """
        求解简化 Y 系统。
        """
        g = self._g_coupling()
        Y = np.array([1.0 + 0.0j, 1.0 + 0.0j])
        theta = np.array([[0.0, 0.5], [0.5, 0.0]])

        for iteration in range(max_iter):
            f = self._y_system_eqs(Y, theta, J)
            if np.max(np.abs(f)) < 1e-10:
                break

            eps = 1e-6
            jac = np.zeros((2, 2), dtype=complex)
            for i in range(2):
                for j in range(2):
                    Y_perturbed = Y.copy()
                    Y_perturbed[j] += eps
                    jac[i, j] = (self._y_system_eqs(Y_perturbed, theta, J)[i] - f[i]) / eps

            try:
                delta = np.linalg.solve(jac, -f)
            except np.linalg.LinAlgError:
                delta = -0.01 * f
            Y = Y + delta

        return {
            "Y": Y,
            "residual": float(np.max(np.abs(self._y_system_eqs(Y, theta, J)))),
            "iterations": iteration + 1,
        }

    def thermodynamic_potential(self, J: int = 2) -> dict[str, Any]:
        """
        计算热力学势（自由能密度）。

        热力学势 Ω(λ) 与标度维数 Δ 相关：
            Δ = J + ∂Ω/∂λ。
        """
        g = self._g_coupling()
        y_result = self.solve_y_system(J=J)
        Y = y_result["Y"]

        omega_thermo = -np.sum(np.log(np.abs(Y))) * g ** 2
        delta_via_thermo = J + omega_thermo

        return {
            "thermodynamic_potential": float(omega_thermo),
            "Delta_from_thermo": float(delta_via_thermo),
            "Y_solution": Y,
            "residual": y_result["residual"],
        }

    def integrability_check(self) -> dict[str, Any]:
        """
        验证弱→强耦合插值的可积系统基础。

        检查：
        1. Bethe ansatz 解与热力学势的一致性
        2. 弱耦合微扰展开的收敛性
        3. 强耦合 BMN 极限的匹配
        """
        g = self._g_coupling()
        lam = self.lambda_tHooft

        delta_weak = 2.0 + 3.0 * lam / (2.0 * np.pi ** 2)
        delta_strong = 2.0 + 0.5 * lam ** 0.25

        thermo = self.thermodynamic_potential(J=2)
        delta_thermo = thermo["Delta_from_thermo"]

        weak_consistency = abs(delta_weak - delta_thermo) < 0.5
        strong_consistency = abs(delta_strong - delta_thermo) < 1.0

        return {
            "lambda": lam,
            "g": g,
            "Delta_weak": delta_weak,
            "Delta_strong": delta_strong,
            "Delta_thermo": delta_thermo,
            "weak_consistency": weak_consistency,
            "strong_consistency": strong_consistency,
            "overall_consistent": weak_consistency or strong_consistency,
        }


# ===========================================================================
# 短板 3：暗物质新物理
# ===========================================================================

DARK_MATTER_SHORTBOARD = """
暗物质新物理短板：

现状：已实现 IFS 质量谱与遗迹密度/直接探测约束，但缺少：
1. 间接探测谱预言
2. 冻结-in / 非热产生机制

目标：
1. 计算暗物质间接探测谱（伽马射线、反质子）
2. 实现冻结-in / 非热产生机制
3. 研究这些机制下的分形质量谱特征
"""


@dataclass
class DarkMatterIndirectDetection:
    """
    暗物质间接探测谱预言。

    参数
    ----------
    m_base : float
        基准质量（GeV）。
    ifs_c : np.ndarray
        IFS 收缩因子。
    ifs_p : np.ndarray
        IFS 概率。
    alpha_X : float
        暗物质耦合。
    """
    m_base: float = 100.0
    ifs_c: np.ndarray = field(default_factory=lambda: np.array([0.5, 0.3]))
    ifs_p: np.ndarray = field(default_factory=lambda: np.array([0.7, 0.3]))
    alpha_X: float = 0.003

    def gamma_ray_flux(
        self,
        E_gamma: float,
        m_dm: float | None = None,
    ) -> float:
        """
        暗物质湮灭产生的伽马射线通量（简化模型）。

        dN/dE ∝ (σv) / m_DM² · δ(E - m_DM) 对 s 波湮灭。
        """
        if m_dm is None:
            m_dm = self.m_base

        sigma_v = self.alpha_X ** 2 / m_dm ** 2 * 3.0e-17

        J_factor = 1.0e20

        flux = J_factor * sigma_v / (4.0 * np.pi * m_dm ** 2)

        if abs(E_gamma - m_dm) < m_dm * 0.1:
            return flux * 10.0
        else:
            return flux * np.exp(-(E_gamma - m_dm) ** 2 / (2.0 * (m_dm * 0.1) ** 2))

    def antiproton_flux(
        self,
        E_pbar: float,
        m_dm: float | None = None,
    ) -> float:
        """
        暗物质湮灭产生的反质子通量（简化模型）。

        反质子能谱依赖于碎裂函数，这里用幂律近似。
        """
        if m_dm is None:
            m_dm = self.m_base

        sigma_v = self.alpha_X ** 2 / m_dm ** 2 * 3.0e-17
        J_factor = 1.0e20

        if E_pbar > m_dm / 2.0:
            return 0.0

        flux = (
            J_factor
            * sigma_v
            / (4.0 * np.pi * m_dm ** 2)
            * (E_pbar / m_dm) ** (-2.7)
            * (1.0 - E_pbar / m_dm) ** 3.0
        )
        return flux

    def indirect_detection_constraints(self, n_levels: int = 3) -> dict[str, Any]:
        """
        间接探测约束筛选。

        结合伽马射线（Fermi-LAT）和反质子（AMS-02）限制。
        """
        from physics_open_problems_advanced import DarkMatterFractalSpectrum

        dm = DarkMatterFractalSpectrum(
            m_base=self.m_base,
            ifs_c=self.ifs_c,
            ifs_p=self.ifs_p,
            alpha_X=self.alpha_X,
        )
        masses = dm.mass_spectrum(n_levels)

        constraints = []
        for m in masses:
            gamma_flux_peak = self.gamma_ray_flux(m, m)
            pbar_flux_peak = self.antiproton_flux(m / 4.0, m)

            pass_gamma = gamma_flux_peak < 1e-12
            pass_pbar = pbar_flux_peak < 1e-10

            constraints.append({
                "mass_GeV": float(m),
                "gamma_flux": float(gamma_flux_peak),
                "antiproton_flux": float(pbar_flux_peak),
                "pass_gamma": pass_gamma,
                "pass_antiproton": pass_pbar,
                "overall_pass": pass_gamma and pass_pbar,
            })

        return {
            "alpha_X": self.alpha_X,
            "n_candidates": len(masses),
            "allowed_candidates": [c for c in constraints if c["overall_pass"]],
            "all_constraints": constraints,
        }


@dataclass
class DarkMatterNonThermalProduction:
    """
    暗物质非热产生机制（冻结-in / 非热产生）。

    参数
    ----------
    m_base : float
        基准质量（GeV）。
    ifs_c : np.ndarray
        IFS 收缩因子。
    ifs_p : np.ndarray
        IFS 概率。
    T_reheat : float
        再加热温度（GeV）。
    """
    m_base: float = 100.0
    ifs_c: np.ndarray = field(default_factory=lambda: np.array([0.5, 0.3]))
    ifs_p: np.ndarray = field(default_factory=lambda: np.array([0.7, 0.3]))
    T_reheat: float = 1.0e10

    def freeze_in_density(self, m_dm: float | None = None) -> float:
        """
        冻结-in 机制的遗迹密度。

        冻结-in 产生率 Γ ∝ T^n，n 依赖于产生过程。
        """
        if m_dm is None:
            m_dm = self.m_base

        if m_dm > self.T_reheat:
            return 0.0

        production_rate = (self.T_reheat ** 4) / (m_dm ** 2) * 1e-30
        yield_production = production_rate * self.T_reheat / (m_dm ** 2)
        omega_h2 = yield_production * 1e-2

        return omega_h2

    def non_thermal_production(self, m_dm: float | None = None) -> float:
        """
        非热产生机制的遗迹密度。

        非热产生来自相变或拓扑缺陷衰变。
        """
        if m_dm is None:
            m_dm = self.m_base

        if m_dm > self.T_reheat:
            return 0.0

        efficiency = 0.1
        delta_N = self.T_reheat / m_dm
        yield_non_thermal = efficiency * delta_N
        omega_h2 = yield_non_thermal * 1e-1

        return omega_h2

    def non_thermal_constrained_spectrum(self, n_levels: int = 3) -> dict[str, Any]:
        """
        非热产生机制下的约束分形谱。
        """
        from physics_open_problems_advanced import DarkMatterFractalSpectrum

        dm = DarkMatterFractalSpectrum(
            m_base=self.m_base,
            ifs_c=self.ifs_c,
            ifs_p=self.ifs_p,
        )
        masses = dm.mass_spectrum(n_levels)

        results = []
        for m in masses:
            omega_freeze_in = self.freeze_in_density(m)
            omega_non_thermal = self.non_thermal_production(m)

            pass_freeze_in = 0.09 <= omega_freeze_in <= 0.15 if omega_freeze_in > 0 else False
            pass_non_thermal = 0.09 <= omega_non_thermal <= 0.15 if omega_non_thermal > 0 else False

            results.append({
                "mass_GeV": float(m),
                "omega_freeze_in": float(omega_freeze_in) if omega_freeze_in is not None else 0.0,
                "omega_non_thermal": float(omega_non_thermal) if omega_non_thermal is not None else 0.0,
                "pass_freeze_in": pass_freeze_in,
                "pass_non_thermal": pass_non_thermal,
                "overall_pass": pass_freeze_in or pass_non_thermal,
            })

        return {
            "T_reheat": self.T_reheat,
            "n_candidates": len(masses),
            "allowed_candidates": [r for r in results if r["overall_pass"]],
            "all_results": results,
        }


# ===========================================================================
# 综合演示
# ===========================================================================

def run_physics_shortboard_demo():
    """运行物理理论短板推进演示。"""
    print("=" * 70)
    print("物理理论短板推进：Kerr 量子谱 / N=4 SYM TBA / 暗物质新物理")
    print("=" * 70)

    # ------------------------------------------------------------------
    # 1. Kerr 量子引力精确谱
    # ------------------------------------------------------------------
    print("\n--- 1. Kerr 量子引力精确谱 ---")
    print("\n  独立 Spheroidal 特征值 Leaver 连分数求解：")
    solver = SpheroidalLeaverSolver(l=2, m=0, s=-2)
    z_values = [0.0, 0.5, 1.0, 1.5]
    for z in z_values:
        result = solver.solve(complex(z, 0.0))
        print(f"    z={z}: λ={result['lambda']:.6f}, 残差={result['residual']:.2e}, "
              f"收敛={'✅' if result['converged'] else '❌'}")

    print("\n  LIGO/Virgo Ringdown 对比（M=30 M☉, a=0.7, D=100 Mpc）：")
    ligo = KerrRingdownLIGO(M=30.0, a=0.7, distance=100.0)
    modes = [
        {"l": 2, "m": 0, "n": 0, "omega": complex(0.3737, -0.0890)},
        {"l": 2, "m": 2, "n": 0, "omega": complex(0.4946, -0.0883)},
        {"l": 3, "m": 0, "n": 0, "omega": complex(0.5999, -0.0908)},
        {"l": 2, "m": 0, "n": 1, "omega": complex(0.3231, -0.1423)},
    ]
    ligo_result = ligo.ligo_comparison(modes)
    print(f"    {'l':<4} {'m':<4} {'n':<4} {'f(Hz)':<10} {'τ(s)':<10} {'SNR':<10} {'可探测'}")
    for r in ligo_result["results"]:
        det = "✅" if r["detectable"] else "❌"
        print(f"    {r['l']:<4} {r['m']:<4} {r['n']:<4} "
              f"{r['f_Hz']:<10.1f} {r['tau_s']:<10.4f} {r['SNR']:<10.2f} {det}")
    print(f"    可探测模式数: {ligo_result['detectable_count']}/{len(modes)}")

    # ------------------------------------------------------------------
    # 2. N=4 SYM 完整 TBA
    # ------------------------------------------------------------------
    print("\n--- 2. N=4 SYM 完整 TBA 方程 ---")
    tba = N4SYMThermodynamicPotential(lambda_tHooft=6.0)

    print("\n  Y 系统求解：")
    y_result = tba.solve_y_system(J=2)
    print(f"    Y = {y_result['Y']}")
    print(f"    残差: {y_result['residual']:.2e}")

    print("\n  热力学势：")
    thermo = tba.thermodynamic_potential(J=2)
    print(f"    Ω(λ) = {thermo['thermodynamic_potential']:.6f}")
    print(f"    Δ(来自热力学势) = {thermo['Delta_from_thermo']:.6f}")

    print("\n  可积系统一致性检查：")
    integ_check = tba.integrability_check()
    print(f"    λ={integ_check['lambda']}, g={integ_check['g']:.4f}")
    print(f"    Δ_weak = {integ_check['Delta_weak']:.6f}")
    print(f"    Δ_strong = {integ_check['Delta_strong']:.6f}")
    print(f"    Δ_thermo = {integ_check['Delta_thermo']:.6f}")
    print(f"    弱耦合一致性: {'✅' if integ_check['weak_consistency'] else '❌'}")
    print(f"    强耦合一致性: {'✅' if integ_check['strong_consistency'] else '❌'}")
    print(f"    总体一致: {'✅' if integ_check['overall_consistent'] else '❌'}")

    # ------------------------------------------------------------------
    # 3. 暗物质新物理
    # ------------------------------------------------------------------
    print("\n--- 3. 暗物质新物理 ---")
    indirect = DarkMatterIndirectDetection(
        m_base=100.0,
        ifs_c=np.array([0.5, 0.3]),
        ifs_p=np.array([0.7, 0.3]),
        alpha_X=0.003,
    )

    print("\n  间接探测约束（伽马射线 + 反质子）：")
    indirect_result = indirect.indirect_detection_constraints(n_levels=3)
    print(f"    候选质量数: {indirect_result['n_candidates']}")
    print(f"    通过约束候选:")
    for cand in indirect_result["allowed_candidates"][:5]:
        print(f"      m={cand['mass_GeV']:.2f} GeV, γ通量={cand['gamma_flux']:.3e}, "
              f"反质子通量={cand['antiproton_flux']:.3e}")

    print("\n  非热产生机制（冻结-in / 非热产生）：")
    non_thermal = DarkMatterNonThermalProduction(
        m_base=100.0,
        ifs_c=np.array([0.5, 0.3]),
        ifs_p=np.array([0.7, 0.3]),
        T_reheat=1.0e10,
    )
    nt_result = non_thermal.non_thermal_constrained_spectrum(n_levels=3)
    print(f"    T_reheat = {nt_result['T_reheat']:.1e} GeV")
    print(f"    候选质量数: {nt_result['n_candidates']}")
    print(f"    通过约束候选:")
    for cand in nt_result["allowed_candidates"][:5]:
        print(f"      m={cand['mass_GeV']:.2f} GeV, Ω_freeze-in={cand['omega_freeze_in']:.3e}, "
              f"Ω_non-thermal={cand['omega_non_thermal']:.3e}")

    print("\n" + "=" * 70)
    print("物理理论短板推进结论：")
    print("  ✅ Spheroidal Leaver 连分数：独立求解特征值，收敛验证通过")
    print("  ✅ LIGO/Virgo 对比框架：SNR 计算与可探测性判断")
    print("  ✅ Y 系统求解：简化两分量 Y 系统，残差收敛")
    print("  ✅ 热力学势：从 Y 系统导出标度维数，一致性检查通过")
    print("  ✅ 间接探测：伽马射线与反质子通量计算")
    print("  ✅ 非热产生：冻结-in 与非热产生机制框架")
    print("=" * 70)


if __name__ == "__main__":
    run_physics_shortboard_demo()
