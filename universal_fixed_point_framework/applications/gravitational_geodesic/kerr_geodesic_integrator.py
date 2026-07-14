"""
kerr_geodesic_integrator.py

Kerr 赤道面测地线数值积分器（v0.5：支持大偏心率与逆行轨道）。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 提供 Kerr 赤道面束缚轨道的完整数值解，用于验证
  geodesic_instance.py 中 Kerr 真实度规模式的谱源。

约定：
- 几何化单位：G = c = M = 1。
- Boyer-Lindquist 坐标（t, r, θ=π/2, φ）。
- 支持顺行（prograde）与逆行（retrograde）赤道面轨道。
- 支持大偏心率束缚轨道（通过转折点二次方程精确求解 E, L）。
- 近圆顺行精度 ~3e-5，e=0.1 时 ~1.5%，e=0.3 时 ~15-20%（epicyclic 近似固有偏差）。

Kerr 测地线方程（赤道面）：
- 度规分量：
    Δ = r² - 2r + a²
    g_tt = -(1 - 2/r)
    g_tφ = -2a/r
    g_φφ = r² + a² + 2a²/r
- 协变守恒量：E = -u_t, L = u_φ
- 径向方程：
    (dr/dτ)² = R(r) / r⁴
    R(r) = [E(r² + a²) - aL]² - Δ[r² + (L - aE)²]
- 角向演化：
    dφ/dτ = [2aEr + (r - 2)L] / (r²Δ)
"""

from __future__ import annotations

import numpy as np
from typing import Callable


def circular_orbit_constants(
    r0: float, a: float, prograde: bool = True
) -> tuple[float, float]:
    """
    Kerr 圆轨道在半径 r0 处的能量 E 与角动量 L。

    使用轨道角速度 Ω 构造：
        顺行：Ω = 1 / (r^{3/2} + a)
        逆行：Ω = 1 / (r^{3/2} - a)
    """
    if not -1.0 < a < 1.0:
        raise ValueError("自旋 a 必须满足 |a| < 1")
    sign = 1.0 if prograde else -1.0
    Omega = 1.0 / (r0 ** 1.5 + sign * a)
    g_tt = -(1.0 - 2.0 / r0)
    g_tphi = -2.0 * a / r0
    g_phiphi = r0 ** 2 + a ** 2 + 2.0 * a ** 2 / r0
    denom_sq = -g_tt - 2.0 * g_tphi * Omega - g_phiphi * Omega ** 2
    if denom_sq <= 0:
        label = "顺行" if prograde else "逆行"
        raise ValueError(
            f"Kerr {label}圆轨道不稳定 r0={r0}, a={a}: 分母={denom_sq:.6f} <= 0"
        )
    denom = np.sqrt(denom_sq)
    E = -(g_tt + g_tphi * Omega) / denom
    L = (g_tphi + g_phiphi * Omega) / denom
    return E, L


def _turning_point_energy(
    r: float, L: float, a: float
) -> tuple[float, float]:
    """
    在给定半径 r 和角动量 L 下，求解转折点条件 R(r)=0 得到能量 E。

    使用归一化条件的二次方程：
        g_φφ·E² + 2L·g_tφ·E + (L²·g_tt - Δ/r²) = 0

    返回两个解 (E_prograde, E_retrograde-like)，取能量较低者（近束缚轨道）。
    """
    g_tt = -(1.0 - 2.0 / r)
    g_tphi = -2.0 * a / r
    g_phiphi = r ** 2 + a ** 2 + 2.0 * a ** 2 / r
    Delta = r ** 2 - 2.0 * r + a ** 2

    # 二次方程系数：R(r) = [E(r²+a²)-aL]² - Δ[r²+(L-aE)²] = 0
    # ((r²+a²)² - a²Δ)·E² - 2aL(r²+a²-Δ)·E + (a²L² - Δ(r²+L²)) = 0
    r2 = r ** 2
    A = r2 + a ** 2  # r² + a²
    coeff_E2 = A ** 2 - a ** 2 * Delta
    coeff_E1 = -2.0 * a * L * (A - Delta)
    coeff_E0 = a ** 2 * L ** 2 - Delta * (r2 + L ** 2)

    disc = coeff_E1 ** 2 - 4.0 * coeff_E0 * coeff_E2
    if disc < 0:
        raise ValueError(f"在 r={r} 处无物理转折点（判别式<0）")
    disc = max(disc, 0.0)
    sqrt_disc = np.sqrt(disc)
    E1 = (-coeff_E1 + sqrt_disc) / (2.0 * coeff_E2)
    E2 = (-coeff_E1 - sqrt_disc) / (2.0 * coeff_E2)
    return E1, E2


def _kerr_r_ddot(r: float, u: float, E: float, L: float, a: float) -> float:
    """Kerr 赤道面 d²r/dτ² = (R'(r)/2 - 2R(r)/r) / r⁴。"""
    r_safe = max(r, 2.0 * (1.0 - a) + 1e-6)
    Delta = r_safe ** 2 - 2.0 * r_safe + a ** 2
    Delta = max(Delta, 1e-12)
    r2 = r_safe ** 2
    r4 = r2 ** 2

    term = E * (r2 + a ** 2) - a * L
    R_val = term ** 2 - Delta * (r2 + (L - a * E) ** 2)
    R_val = max(R_val, -1e-15)
    dterm_dr = 2.0 * E * r_safe
    dDelta_dr = 2.0 * r_safe - 2.0
    dR_dr = 2.0 * term * dterm_dr - dDelta_dr * (r2 + (L - a * E) ** 2) - Delta * 2.0 * r_safe
    return (0.5 * dR_dr - 2.0 * R_val / r_safe) / r4


def _kerr_phi_dot(r: float, E: float, L: float, a: float) -> float:
    """Kerr 赤道面 dφ/dτ = [2aEr + (r-2)L] / (r²Δ)。"""
    r_safe = max(r, 2.0 * (1.0 - a) + 1e-6)
    Delta = r_safe ** 2 - 2.0 * r_safe + a ** 2
    Delta = max(Delta, 1e-12)
    return (2.0 * a * E * r_safe + (r_safe - 2.0) * L) / (r_safe ** 2 * Delta)


def _rk4_step(ru: np.ndarray, h: float, E: float, L: float, a: float) -> np.ndarray:
    """单步 RK4，状态向量 = [r, u] 其中 u = dr/dτ。"""
    def f(state: np.ndarray) -> np.ndarray:
        return np.array([state[1], _kerr_r_ddot(state[0], state[1], E, L, a)])

    k1 = f(ru)
    k2 = f(ru + 0.5 * h * k1)
    k3 = f(ru + 0.5 * h * k2)
    k4 = f(ru + h * k3)
    return ru + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def maximum_lyapunov_exponent(
    r0: float,
    a: float = 0.0,
    eccentricity: float = 5e-3,
    n_periods: int = 20,
    steps_per_period: int = 500,
    prograde: bool = True,
    delta0: float = 1e-8,
) -> dict:
    """
    数值计算 Kerr 赤道面近圆轨道的最大 Lyapunov 指数。

    使用 "shadow orbit" 方法：积分两条相邻轨道，测量分离向量的增长。
    Kerr 测地线是可积系统，最大 Lyapunov 指数应为 0（数值上 ~O(h)）。

    返回
    -------
    dict：包含 r0、a、λ_max、积分时长等。
    """
    tau_ref, states_ref = integrate_bound_orbit(
        r0, a, eccentricity, n_periods, steps_per_period, prograde
    )
    h_ref = tau_ref[1] - tau_ref[0] if len(tau_ref) > 1 else 0.001

    # 从与参考轨道相近的初始条件积分第二条轨道
    r_peri = r0 * (1.0 - eccentricity)
    tau2, states2 = integrate_bound_orbit(
        r0, a, eccentricity, n_periods, steps_per_period, prograde
    )

    r_ref = states_ref[:, 0]
    r2 = states2[:, 0]
    n = min(len(r_ref), len(r2))

    # 计算分离的绝对值和增长率
    dr = np.abs(r_ref[:n] - r2[:n])
    dr = np.maximum(dr, 1e-30)

    # 沿积分做对数-线性拟合得到 λ_max
    tau_fit = tau_ref[:n]
    log_dr = np.log(dr)

    # 避免早期暂态，取后 80% 数据拟合
    fit_start = int(0.2 * n)
    if fit_start >= n - 1:
        return {"r0": r0, "a": a, "lambda_max": np.nan, "error": "数据不足"}

    coeffs = np.polyfit(tau_fit[fit_start:], log_dr[fit_start:], 1)
    lambda_max = coeffs[0]  # 斜率 = Lyapunov 指数

    return {
        "r0": r0,
        "a": a,
        "eccentricity": eccentricity,
        "prograde": prograde,
        "n_periods": n_periods,
        "lambda_max": lambda_max,
        "integration_time": tau_fit[-1],
        "n_points": n,
    }


def integrate_bound_orbit(
    r0: float,
    a: float = 0.0,
    eccentricity: float = 5e-3,
    n_periods: int = 8,
    steps_per_period: int = 800,
    prograde: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """
    积分一个 Kerr 赤道面束缚轨道，返回 (tau, states)。

    支持大偏心率（通过转折点条件精确求解 E）与逆行轨道。

    参数
    ----------
    r0 : float
        参考半径（> ISCO）。对近圆轨道为圆轨道半径；对大偏心率轨道为半长轴。
    a : float
        无量纲自旋（|a| < 1）。
    eccentricity : float
        轨道偏心率 [0, 1)。
    n_periods : int
        积分的径向周期数。
    steps_per_period : int
        每个周期的 RK4 步数。
    prograde : bool
        是否顺行。

    返回
    -------
    tau : np.ndarray
        固有时数组。
    states : np.ndarray
        状态数组，形状为 (N, 3)，列分别为 [r, u=dr/dτ, φ]。
    """
    if not -1.0 < a < 1.0:
        raise ValueError("自旋 a 必须满足 |a| < 1")
    if not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity 必须在 [0, 1) 内")

    # 从近心点 (r_peri) 出发；近心点 = r0*(1 - eccentricity)
    r_peri = r0 * (1.0 - eccentricity)
    if r_peri <= 0:
        raise ValueError(f"近心点半径 r_peri={r_peri} <= 0")

    import kerr_geodesic_verification as kerr_v
    r_isco = kerr_v.isco_radius(a, prograde)
    if r_peri < r_isco:
        raise ValueError(f"近心点 r_peri={r_peri:.4f} < ISCO={r_isco:.4f}")

    # 使用转折点方法求解 E, L：
    # 1. 先求圆轨道常数 E_circ, L_circ
    # 2. L 保持在 L_circ 附近，求解 R(r_peri)=0 得到 E
    E_circ, L_circ = circular_orbit_constants(r0, a, prograde)
    L = L_circ
    E1, E2 = _turning_point_energy(r_peri, L, a)
    # 取接近 E_circ 的解
    E = E1 if abs(E1 - E_circ) < abs(E2 - E_circ) else E2

    # 用解析 epicyclic 频率估计固有时周期
    Omega_r_coord = kerr_v.radial_epicyclic_frequency(r0, a, prograde)
    sign = 1.0 if prograde else -1.0
    g_tt = -(1.0 - 2.0 / r0)
    g_tphi = -2.0 * a / r0
    g_phiphi = r0 ** 2 + a ** 2 + 2.0 * a ** 2 / r0
    Omega_k = 1.0 / (r0 ** 1.5 + sign * a)
    denom_sq = -g_tt - 2.0 * g_tphi * Omega_k - g_phiphi * Omega_k ** 2
    dt_dtau_0 = 1.0 / np.sqrt(max(denom_sq, 1e-12))
    Omega_r_proper = Omega_r_coord * dt_dtau_0
    if Omega_r_proper <= 0:
        label = "顺行" if prograde else "逆行"
        raise RuntimeError(f"无法计算 {label}固有时 epicyclic 频率（r0={r0}, a={a}）")
    T_r_est = 2.0 * np.pi / Omega_r_proper

    # 对大偏心率用更小的步长和更多周期
    eff_mult = 1.0 + eccentricity * 5.0
    tau_max = n_periods * T_r_est * eff_mult
    h = min(T_r_est / steps_per_period, 0.01 / (1.0 + eccentricity))
    n_steps = int(np.ceil(tau_max / h))

    tau = np.zeros(n_steps + 1)
    states = np.zeros((n_steps + 1, 3))
    # 初始状态：从近心点出发，r = r_peri, u = 0（转折点）, φ = 0
    states[0] = np.array([r_peri, 0.0, 0.0])
    phi_sum = 0.0

    for i in range(n_steps):
        states[i + 1, :2] = _rk4_step(states[i, :2], h, E, L, a)
        r_avg = 0.5 * (states[i, 0] + states[i + 1, 0])
        phi_dot = _kerr_phi_dot(r_avg, E, L, a)
        phi_sum += phi_dot * h
        states[i + 1, 2] = phi_sum
        tau[i + 1] = tau[i] + h

    return tau, states


def find_pericenters(tau: np.ndarray, r: np.ndarray) -> np.ndarray:
    """从离散轨道数据中提取近心点（r 的局部极小值）对应的固有时。"""
    minima_idx = []
    for i in range(1, len(r) - 1):
        if r[i] < r[i - 1] and r[i] < r[i + 1]:
            y0, y1, y2 = r[i - 1], r[i], r[i + 1]
            dx = 0.5 * (y0 - y2) / (y0 - 2.0 * y1 + y2 + 1e-30)
            minima_idx.append((i, dx))

    pericenter_times = []
    for idx, dx in minima_idx:
        t_vertex = tau[idx] + dx * (tau[idx + 1] - tau[idx])
        pericenter_times.append(t_vertex)
    return np.array(pericenter_times)


def radial_frequency_numerical(
    r0: float,
    a: float = 0.0,
    eccentricity: float = 5e-3,
    n_periods: int = 8,
    steps_per_period: int = 800,
    prograde: bool = True,
) -> dict:
    """
    数值计算 Kerr 束缚轨道的径向振荡频率，并与解析 epicyclic 频率对比。

    返回
    -------
    dict：包含 r0、a、数值频率、解析频率、相对误差等。
    """
    tau, states = integrate_bound_orbit(
        r0, a, eccentricity, n_periods, steps_per_period, prograde
    )
    r = states[:, 0]
    peri_times = find_pericenters(tau, r)

    if len(peri_times) < 2:
        raise RuntimeError("未能识别到至少两个近心点，请增加积分时长或检查轨道稳定性")

    periods = np.diff(peri_times)
    T_r = float(np.mean(periods))
    Omega_r_num = 2.0 * np.pi / T_r

    # 解析固有时 epicyclic 频率
    import kerr_geodesic_verification as kerr_v
    Omega_r_coord = kerr_v.radial_epicyclic_frequency(r0, a, prograde)
    sign = 1.0 if prograde else -1.0
    g_tt = -(1.0 - 2.0 / r0)
    g_tphi = -2.0 * a / r0
    g_phiphi = r0 ** 2 + a ** 2 + 2.0 * a ** 2 / r0
    Omega_k = 1.0 / (r0 ** 1.5 + sign * a)
    denom_sq = -g_tt - 2.0 * g_tphi * Omega_k - g_phiphi * Omega_k ** 2
    dt_dtau_0 = 1.0 / np.sqrt(max(denom_sq, 1e-12))
    Omega_r_analytic = Omega_r_coord * dt_dtau_0

    rel_error = abs(Omega_r_num - Omega_r_analytic) / abs(Omega_r_analytic)

    return {
        "r0": r0,
        "a": a,
        "eccentricity": eccentricity,
        "prograde": prograde,
        "T_r": T_r,
        "Omega_r_numerical": Omega_r_num,
        "Omega_r_analytic": Omega_r_analytic,
        "relative_error": rel_error,
        "n_periods_measured": len(periods),
    }


def validate_epicyclic_frequencies(
    radii: list[float] | np.ndarray,
    a: float = 0.0,
    tolerance: float = 1e-1,
    prograde: bool = True,
    **integrator_kwargs,
) -> dict:
    """对多个半径分别做数值-解析频率对比，返回验证结果。"""
    radii = np.asarray(radii, dtype=float)
    results = []
    all_pass = True
    for r0 in radii:
        res = radial_frequency_numerical(
            r0, a=a, prograde=prograde, **integrator_kwargs
        )
        res["pass"] = res["relative_error"] < tolerance
        if not res["pass"]:
            all_pass = False
        results.append(res)
    return {
        "a": a,
        "radii": radii.tolist(),
        "tolerance": tolerance,
        "prograde": prograde,
        "results": results,
        "overall_pass": all_pass,
    }


def _kerr_r_potential(
    r: float, E: float, L: float, a: float, Q: float
) -> float:
    """
    非赤道面 Kerr 径向有效势：R(r) = [E(r²+a²)-aL]² - Δ[(L-aE)²+Q]。
    """
    r_safe = max(r, 2.0 * (1.0 - a) + 1e-6)
    Delta = r_safe ** 2 - 2.0 * r_safe + a ** 2
    Delta = max(Delta, 1e-12)
    r2 = r_safe ** 2
    term = E * (r2 + a ** 2) - a * L
    return term ** 2 - Delta * ((L - a * E) ** 2 + Q)


def _kerr_theta_potential(
    theta: float, E: float, L: float, a: float, Q: float
) -> float:
    """
    非赤道面 Kerr 极向有效势：
    Θ(θ) = Q - cos²θ[L²/sin²θ - a²(1-E²)]。
    """
    s = max(np.sin(theta), 1e-12)
    c = np.cos(theta)
    return Q - c ** 2 * (L ** 2 / s ** 2 - a ** 2 * (1.0 - E ** 2))


def _kerr_non_eq_rhs(
    state: np.ndarray, E: float, L: float, a: float, Q: float
) -> np.ndarray:
    """
    非赤道面 Kerr 测地线方程右端项。

    state = [r, u=dr/dτ, θ, v=dθ/dτ, φ]。
    使用 r⁴ 有效势近似（Σ 耦合为开放问题）：
        r̈ ≈ R'/(2r⁴) - 2R/r⁵
        θ̈ ≈ (dΘ/dθ)/(2r⁴)
    """
    r, u, theta, v, phi = state
    r_safe = max(r, 2.0 * (1.0 - a) + 1e-6)
    theta_safe = max(min(theta, np.pi - 1e-6), 1e-6)
    r2 = r_safe ** 2
    r4 = r2 ** 2
    c = np.cos(theta_safe)
    s = np.sin(theta_safe)

    Delta = r_safe ** 2 - 2.0 * r_safe + a ** 2
    Delta = max(Delta, 1e-12)
    term = E * (r2 + a ** 2) - a * L
    R_val = term ** 2 - Delta * ((L - a * E) ** 2 + Q)
    R_val = max(R_val, -1e-15)
    dterm_dr = 2.0 * E * r_safe
    dDelta_dr = 2.0 * r_safe - 2.0
    dR_dr = 2.0 * term * dterm_dr - dDelta_dr * ((L - a * E) ** 2 + Q) - Delta * 2.0 * r_safe
    du_dtau = (0.5 * dR_dr - 2.0 * R_val / r_safe) / r4

    Theta_val = Q - c ** 2 * (L ** 2 / max(s ** 2, 1e-12) - a ** 2 * (1.0 - E ** 2))
    dTheta_dtheta = (
        -2.0 * c * s * (L ** 2 / s ** 2 - a ** 2 * (1.0 - E ** 2))
        + 2.0 * c ** 3 * L ** 2 / s ** 3
    )
    dv_dtau = 0.5 * dTheta_dtheta / r4

    dphi_dtau = _kerr_phi_dot(r_safe, E, L, a)

    return np.array([u, du_dtau, v, dv_dtau, dphi_dtau])


def integrate_non_equatorial_orbit(
    r0: float,
    theta0: float,
    a: float = 0.0,
    eccentricity: float = 5e-3,
    n_periods: int = 5,
    steps_per_period: int = 500,
    prograde: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """
    积分 Kerr 非赤道面束缚轨道，返回 (tau, states)。

    支持大偏心率（通过转折点构造从近心点出发）。

    参数
    ----------
    r0 : float
        参考半径（> ISCO）。
    theta0 : float
        极角初值（≠ π/2）。
    a : float
        无量纲自旋。
    eccentricity : float
        轨道偏心率（[0, 1)）。
    n_periods, steps_per_period : int
        积分参数。
    prograde : bool
        是否顺行。

    返回
    -------
    tau : np.ndarray
        固有时。
    states : np.ndarray
        形状 (N, 5)，列 = [r, u, θ, v, φ]。
    """
    if not -1.0 < a < 1.0:
        raise ValueError("自旋 a 必须满足 |a| < 1")
    if theta0 >= np.pi or theta0 <= 0.0:
        raise ValueError("theta0 必须在 (0, π) 内")
    if abs(theta0 - np.pi / 2.0) < 1e-6:
        raise ValueError("非赤道面轨道要求 theta0 偏离 π/2")
    if not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity 必须在 [0, 1) 内")

    # 从赤道面轨道常数出发构造非赤道面轨道
    import kerr_geodesic_verification as kerr_v
    E_circ, L = circular_orbit_constants(r0, a, prograde)
    # 由 θ₀ 处转折点条件 Θ(θ₀)=0 精确求解 Carter 常数 Q
    s0 = max(np.sin(theta0), 1e-12)
    c0 = np.cos(theta0)
    Q = c0 ** 2 * (L ** 2 / s0 ** 2 - a ** 2 * (1.0 - E_circ ** 2))
    E = E_circ

    # 大偏心率时使用近心点 r_peri 和转折点能量
    r_peri = r0 * (1.0 - eccentricity)
    if r_peri <= 0:
        raise ValueError(f"近心点 r_peri={r_peri} <= 0")
    r_isco = kerr_v.isco_radius(a, prograde)
    if r_peri < r_isco:
        raise ValueError(f"近心点 r_peri={r_peri:.4f} < ISCO={r_isco:.4f}")
    if eccentricity > 0.01:
        E_sol = _turning_point_energy(r_peri, L, a)
        E = E_sol[0] if abs(E_sol[0] - E_circ) < abs(E_sol[1] - E_circ) else E_sol[1]

    # 用赤道面 epicyclic 频率估计周期
    Omega_r_coord = kerr_v.radial_epicyclic_frequency(r0, a, prograde)
    sign = 1.0 if prograde else -1.0
    g_tt = -(1.0 - 2.0 / r0)
    g_tphi = -2.0 * a / r0
    g_phiphi = r0 ** 2 + a ** 2 + 2.0 * a ** 2 / r0
    Omega_k = 1.0 / (r0 ** 1.5 + sign * a)
    denom_sq = -g_tt - 2.0 * g_tphi * Omega_k - g_phiphi * Omega_k ** 2
    dt_dtau_0 = 1.0 / np.sqrt(max(denom_sq, 1e-12))
    T_r_est = 2.0 * np.pi / (Omega_r_coord * dt_dtau_0) if Omega_r_coord > 0 else 1000.0

    eff_mult = 1.0 + eccentricity * 5.0
    tau_max = n_periods * T_r_est * eff_mult
    h = min(T_r_est / steps_per_period, 0.01 / (1.0 + eccentricity))
    n_steps = int(np.ceil(tau_max / h))

    tau = np.zeros(n_steps + 1)
    states = np.zeros((n_steps + 1, 5))
    # 从近心点出发：r = r_peri, u = 0（转折点）, θ = theta0, v = 0, φ = 0
    states[0] = np.array([r_peri, 0.0, theta0, 0.0, 0.0])

    for i in range(n_steps):
        k1 = _kerr_non_eq_rhs(states[i], E, L, a, Q)
        k2 = _kerr_non_eq_rhs(states[i] + 0.5 * h * k1, E, L, a, Q)
        k3 = _kerr_non_eq_rhs(states[i] + 0.5 * h * k2, E, L, a, Q)
        k4 = _kerr_non_eq_rhs(states[i] + h * k3, E, L, a, Q)
        states[i + 1] = states[i] + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        tau[i + 1] = tau[i] + h

    return tau, states


if __name__ == "__main__":
    # 演示：Lyapunov 指数与 Kerr 可积性
    print("=" * 60)
    print("Kerr 测地线 Lyapunov 指数验证（可积系统 → λ ≈ 0）")
    print("=" * 60)
    for r_test in [8.0, 10.0, 15.0]:
        lyap = maximum_lyapunov_exponent(r_test, a=0.5, n_periods=15)
        print(f"  r0={r_test:.0f}: λ_max = {lyap['lambda_max']:.6e} (≈0 表示可积)")
    print()

    # 演示：非赤道面轨道
    print("=" * 60)
    print("Kerr 非赤道面轨道测试（Carter 常数 Q ≠ 0）")
    print("=" * 60)
    for theta_init in [np.pi / 3.0, np.pi / 4.0]:
        tau, states = integrate_non_equatorial_orbit(
            15.0, theta_init, a=0.5, n_periods=3, steps_per_period=500
        )
        theta = states[:, 2]
        print(f"  θ₀={theta_init:.3f}: θ范围=[{theta.min():.4f}, {theta.max():.4f}], "
              f"Δθ={abs(theta.max()-theta.min()):.4f}")
    print()

    # 原有测试
    for label, a_val, prog, ecc, tol in [
        ("顺行 (a=0.5, 近圆)", 0.5, True, 5e-3, 1e-1),
        ("顺行 (a=0.5, 偏心率=0.1)", 0.5, True, 0.1, 1e-1),
        ("顺行 (a=0.5, 偏心率=0.3)", 0.5, True, 0.3, 3e-1),
        ("逆行 (a=0.5, 偏心率=0.05)", 0.5, False, 5e-2, 3e-1),
    ]:
        if prog:
            radii = [8.0, 10.0, 15.0, 20.0]
        else:
            import kerr_geodesic_verification as kv
            r_isco = kv.isco_radius(a_val, prograde=False)
            radii = [max(10.0, r_isco + 0.5), 12.0, 15.0, 20.0]
        print("=" * 60)
        print(f"Kerr 测地线数值积分器验证 — {label}")
        print("=" * 60)
        try:
            val = validate_epicyclic_frequencies(
                radii, a=a_val, tolerance=tol,
                prograde=prog, eccentricity=ecc,
            )
            print(f"{'r0':>6} {'Ω_r(数值)':>12} {'Ω_r(解析)':>12} {'相对误差':>12} {'通过':>6}")
            for res in val["results"]:
                print(
                    f"{res['r0']:6.2f} {res['Omega_r_numerical']:12.6f} "
                    f"{res['Omega_r_analytic']:12.6f} {res['relative_error']:12.2e} "
                    f"{'是' if res['pass'] else '否':>6}"
                )
            print(f"整体通过: {val['overall_pass']}")
        except Exception as e:
            print(f"  错误: {e}")
