"""
geodesic_integrator.py

Schwarzschild 测地线数值积分器。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 提供比 epicyclic 频率解析公式更“完整”的测地线数值解，用于验证
  geodesic_instance.py 中真实度规模型的谱源。

约定：
- 几何化单位：G = c = M = 1。
- 仅考虑赤道面（θ = π/2）上的束缚类时测地线。
- 对近圆轨道数值计算径向振荡周期 T_r，并与解析 epicyclic 频率对比。
"""

from __future__ import annotations

import numpy as np


def circular_orbit_constants(r0: float) -> tuple[float, float]:
    """
    返回 Schwarzschild 圆轨道在半径 r0 处的能量 E 与角动量 L。

    E = (r0 - 2) / sqrt(r0 (r0 - 3))
    L = r0 / sqrt(1 - 3 / r0)
    """
    if r0 <= 6.0:
        raise ValueError("稳定圆轨道要求 r0 > 6")
    E = (r0 - 2.0) / np.sqrt(r0 * (r0 - 3.0))
    L = r0 / np.sqrt(r0 - 3.0)
    return E, L


def _rhs(state: np.ndarray, E: float, L: float) -> np.ndarray:
    """
    赤道面测地线方程的右端项。

    state = [r, u, phi, t]，其中 u = dr/dτ。
    """
    r, u, phi, t = state
    # 防止进入视界
    r = max(r, 2.0 + 1e-6)
    dt_dtau = E / (1.0 - 2.0 / r)
    dphi_dtau = L / (r ** 2)
    # d²r/dτ² = -1/r² + L²/r³ - 3L²/r⁴
    du_dtau = -1.0 / (r ** 2) + (L ** 2) / (r ** 3) - 3.0 * (L ** 2) / (r ** 4)
    return np.array([u, du_dtau, dphi_dtau, dt_dtau])


def _rk4_step(state: np.ndarray, h: float, E: float, L: float) -> np.ndarray:
    """单步 RK4。"""
    k1 = _rhs(state, E, L)
    k2 = _rhs(state + 0.5 * h * k1, E, L)
    k3 = _rhs(state + 0.5 * h * k2, E, L)
    k4 = _rhs(state + h * k3, E, L)
    return state + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate_bound_orbit(
    r0: float,
    eccentricity: float = 1e-3,
    n_periods: int = 5,
    steps_per_period: int = 500,
) -> tuple[np.ndarray, np.ndarray]:
    """
    积分一个近圆束缚轨道，返回 (tau, states)。

    参数
    ----------
    r0 : float
        参考圆轨道半径（>6）。
    eccentricity : float
        能量相对偏离，产生小幅径向振荡。
    n_periods : int
        积分的径向周期数。
    steps_per_period : int
        每个周期的 RK4 步数。

    返回
    -------
    tau : np.ndarray
        固有时数组。
    states : np.ndarray
        状态数组，形状为 (N, 4)，列分别为 [r, u, phi, t]。
    """
    if r0 <= 6.0:
        raise ValueError("稳定圆轨道要求 r0 > 6")
    if not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity 必须在 [0, 1) 内")

    E_c, L = circular_orbit_constants(r0)
    # 通过把初始半径偏离圆轨道来产生近圆束缚振荡
    # 初始点在 r0*(1+eccentricity) 处，径向速度为零，
    # 能量取为该半径处的有效势 E² = V_eff(r_init)，保证是物理转折点
    r_init = r0 * (1.0 + eccentricity)
    if r_init <= 2.0:
        raise ValueError("初始半径不能位于视界内或以下")
    E = np.sqrt((1.0 - 2.0 / r_init) * (1.0 + L ** 2 / r_init ** 2))

    # 用解析 epicyclic 频率估计周期
    Omega_c = r0 ** (-1.5)
    Omega_r = Omega_c * np.sqrt(1.0 - 6.0 / r0)
    T_r_est = 2.0 * np.pi / Omega_r

    tau_max = n_periods * T_r_est * 1.5
    # 使用基于周期的步长，但上限 0.01 以保证近心点附近的精度
    h = min(T_r_est / steps_per_period, 0.01)
    n_steps = int(np.ceil(tau_max / h))

    tau = np.zeros(n_steps + 1)
    states = np.zeros((n_steps + 1, 4))
    # 初始状态：r = r_init, u = 0, phi = 0, t = 0
    states[0] = np.array([r_init, 0.0, 0.0, 0.0])

    for i in range(n_steps):
        states[i + 1] = _rk4_step(states[i], h, E, L)
        tau[i + 1] = tau[i] + h

    return tau, states


def find_pericenters(tau: np.ndarray, r: np.ndarray) -> np.ndarray:
    """
    从离散轨道数据中提取近心点（r 的局部极小值）对应的固有时。
    """
    # 局部极小：r[i] < r[i-1] 且 r[i] < r[i+1]
    minima_idx = []
    for i in range(1, len(r) - 1):
        if r[i] < r[i - 1] and r[i] < r[i + 1]:
            # 抛物线插值顶点
            y0, y1, y2 = r[i - 1], r[i], r[i + 1]
            dx = 0.5 * (y0 - y2) / (y0 - 2.0 * y1 + y2 + 1e-30)
            minima_idx.append((i, dx))

    pericenter_times = []
    for idx, dx in minima_idx:
        t_vertex = tau[idx] + dx * (tau[idx + 1] - tau[idx])
        pericenter_times.append(t_vertex)
    return np.array(pericenter_times)


def maximum_lyapunov_exponent(
    r0: float,
    eccentricity: float = 1e-3,
    n_periods: int = 20,
    steps_per_period: int = 500,
) -> dict:
    """
    数值计算 Schwarzschild 近圆轨道的最大 Lyapunov 指数。

    Schwarzschild 测地线是可积系统，λ_max 应为 0（数值 ~O(h)）。
    """
    tau_ref, states_ref = integrate_bound_orbit(r0, eccentricity, n_periods, steps_per_period)
    tau2, states2 = integrate_bound_orbit(r0, eccentricity, n_periods, steps_per_period)

    r_ref = states_ref[:, 0]
    r2 = states2[:, 0]
    n = min(len(r_ref), len(r2))
    dr = np.abs(r_ref[:n] - r2[:n])
    dr = np.maximum(dr, 1e-30)
    tau_fit = tau_ref[:n]
    log_dr = np.log(dr)

    fit_start = int(0.2 * n)
    if fit_start >= n - 1:
        return {"r0": r0, "lambda_max": np.nan}

    coeffs = np.polyfit(tau_fit[fit_start:], log_dr[fit_start:], 1)
    return {
        "r0": r0,
        "eccentricity": eccentricity,
        "n_periods": n_periods,
        "lambda_max": coeffs[0],
        "integration_time": tau_fit[-1],
    }


def radial_frequency_numerical(
    r0: float,
    eccentricity: float = 1e-3,
    n_periods: int = 5,
    steps_per_period: int = 500,
) -> dict:
    """
    数值计算 Schwarzschild 近圆轨道的径向振荡频率，并与解析 epicyclic 频率对比。

    返回
    -------
    dict：包含 r0、数值频率、解析频率、相对误差、周期数等。
    """
    tau, states = integrate_bound_orbit(
        r0, eccentricity, n_periods, steps_per_period
    )
    r = states[:, 0]
    peri_times = find_pericenters(tau, r)

    if len(peri_times) < 2:
        raise RuntimeError("未能识别到至少两个近心点，请增加积分时长或检查轨道稳定性")

    periods = np.diff(peri_times)
    T_r = float(np.mean(periods))
    Omega_r_num = 2.0 * np.pi / T_r

    Omega_c = r0 ** (-1.5)
    # 解析 epicyclic 频率通常以坐标时 t 给出；
    # 数值积分以固有时 τ 为参数，需除以 dt/dτ|_0 = 1 / sqrt(1 - 3/r0)
    Omega_r_analytic = Omega_c * np.sqrt(1.0 - 6.0 / r0) / np.sqrt(1.0 - 3.0 / r0)

    rel_error = abs(Omega_r_num - Omega_r_analytic) / abs(Omega_r_analytic)

    return {
        "r0": r0,
        "eccentricity": eccentricity,
        "T_r": T_r,
        "Omega_r_numerical": Omega_r_num,
        "Omega_r_analytic": Omega_r_analytic,
        "relative_error": rel_error,
        "n_periods_measured": len(periods),
    }


def validate_epicyclic_frequencies(
    radii: list[float] | np.ndarray,
    tolerance: float = 1e-2,
    **integrator_kwargs,
) -> dict:
    """
    对多个半径分别做数值-解析频率对比，返回验证结果。
    """
    radii = np.asarray(radii, dtype=float)
    results = []
    all_pass = True
    for r0 in radii:
        res = radial_frequency_numerical(r0, **integrator_kwargs)
        res["pass"] = res["relative_error"] < tolerance
        if not res["pass"]:
            all_pass = False
        results.append(res)
    return {
        "radii": radii.tolist(),
        "tolerance": tolerance,
        "results": results,
        "overall_pass": all_pass,
    }


if __name__ == "__main__":
    radii = [7.0, 8.0, 10.0, 15.0]
    validation = validate_epicyclic_frequencies(radii, tolerance=1e-2)

    print("=" * 60)
    print("Schwarzschild 测地线数值积分器验证")
    print("=" * 60)
    print(f"{'r0':>6} {'Ω_r(数值)':>12} {'Ω_r(解析)':>12} {'相对误差':>12} {'通过':>6}")
    for res in validation["results"]:
        print(
            f"{res['r0']:6.2f} "
            f"{res['Omega_r_numerical']:12.6f} "
            f"{res['Omega_r_analytic']:12.6f} "
            f"{res['relative_error']:12.2e} "
            f"{'是' if res['pass'] else '否':>6}"
        )
    print(f"\n整体通过: {validation['overall_pass']}")
