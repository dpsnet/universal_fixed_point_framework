"""
kerr_geodesic_verification.py

Kerr 度规下测地线偏差/圆轨道频率的解析验证模块。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 提供 Kerr 圆轨道径向与垂直 epicyclic 频率的标准解析公式，
  用于与 geodesic_instance.py 的真实度规模式对接。

约定：
- 几何化单位：G = c = M = 1。
- 无量纲自旋 a ∈ (-1, 1)。
- 支持顺行（prograde）与逆行（retrograde）圆轨道。
- 顺行：Ω = 1 / (r^{3/2} + a)，逆行：Ω = 1 / (r^{3/2} - a)。
"""

from __future__ import annotations

import numpy as np


def _check_spin(a: float) -> None:
    if not -1.0 < a < 1.0:
        raise ValueError("无量纲自旋 a 必须满足 |a| < 1")


def isco_radius(a: float, prograde: bool = True) -> float:
    """
    Kerr 最内稳定圆轨道半径（Bardeen 公式）。

    顺行取减号，逆行取加号。
    """
    _check_spin(a)
    a_abs = abs(a)
    z1 = 1.0 + (1.0 - a_abs ** 2) ** (1.0 / 3.0) * (
        (1.0 + a_abs) ** (1.0 / 3.0) + (1.0 - a_abs) ** (1.0 / 3.0)
    )
    z2 = np.sqrt(3.0 * a_abs ** 2 + z1 ** 2)
    if prograde:
        return 3.0 + z2 - np.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))
    else:
        return 3.0 + z2 + np.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def orbital_frequency(
    r: float | np.ndarray,
    a: float = 0.0,
    prograde: bool = True,
) -> float | np.ndarray:
    """
    Kerr 圆轨道角频率。

    顺行：Ω = 1 / (r^{3/2} + a)
    逆行：Ω = 1 / (r^{3/2} - a)
    """
    _check_spin(a)
    r = np.asarray(r, dtype=float)
    if np.any(r <= 0):
        raise ValueError("半径 r 必须为正")
    sign = 1.0 if prograde else -1.0
    return 1.0 / (r ** 1.5 + sign * a)


def _epicyclic_sqrt_term(
    r: float | np.ndarray, a: float = 0.0, prograde: bool = True
) -> float | np.ndarray:
    """
    Kerr epicyclic 频率平方根内的表达式。

    径向：1 - 6/r + 8a/r^{3/2} - 3a²/r²
    垂直：1 + 4a/r^{3/2} - 3a²/r²

    逆行时 a → -a（等价于 prograde=False 公式中取 a 的相反符号）。
    """
    r = np.asarray(r, dtype=float)
    sign = 1.0 if prograde else -1.0
    a_eff = sign * a  # 逆行等价于 a→-a 的顺行
    return {
        "radial": 1.0 - 6.0 / r + 8.0 * a_eff / r ** 1.5 - 3.0 * a_eff ** 2 / r ** 2,
        "vertical": 1.0 + 4.0 * a_eff / r ** 1.5 - 3.0 * a_eff ** 2 / r ** 2,
    }


def radial_epicyclic_frequency(
    r: float | np.ndarray,
    a: float = 0.0,
    prograde: bool = True,
) -> float | np.ndarray:
    """Kerr 坐标时径向 epicyclic 频率。"""
    _check_spin(a)
    r = np.asarray(r, dtype=float)
    r_isco = isco_radius(a, prograde)
    if np.any(r < r_isco):
        label = "顺行" if prograde else "逆行"
        raise ValueError(
            f"Kerr {label}稳定圆轨道要求 r >= r_ISCO({a}) = {r_isco:.4f}"
        )
    Omega = orbital_frequency(r, a, prograde)
    sqrt_term = _epicyclic_sqrt_term(r, a, prograde)["radial"]
    # 防止负值（近 ISCO 处可能被截断）
    return Omega * np.sqrt(np.maximum(sqrt_term, 0.0))


def vertical_epicyclic_frequency(
    r: float | np.ndarray,
    a: float = 0.0,
    prograde: bool = True,
) -> float | np.ndarray:
    """Kerr 坐标时垂直 epicyclic 频率。"""
    _check_spin(a)
    r = np.asarray(r, dtype=float)
    r_isco = isco_radius(a, prograde)
    if np.any(r < r_isco):
        label = "顺行" if prograde else "逆行"
        raise ValueError(
            f"Kerr {label}稳定圆轨道要求 r >= r_ISCO({a}) = {r_isco:.4f}"
        )
    Omega = orbital_frequency(r, a, prograde)
    sqrt_term = _epicyclic_sqrt_term(r, a, prograde)["vertical"]
    return Omega * np.sqrt(np.maximum(sqrt_term, 0.0))


def epicyclic_frequencies(
    radii: list[float] | np.ndarray,
    a: float = 0.0,
    prograde: bool = True,
) -> np.ndarray:
    """
    返回给定半径列表的 (Ω_r, Ω_θ) 频率数组。

    返回形状：(len(radii), 2)
    """
    radii = np.asarray(radii, dtype=float)
    Omega_r = radial_epicyclic_frequency(radii, a, prograde)
    Omega_theta = vertical_epicyclic_frequency(radii, a, prograde)
    return np.column_stack([Omega_r, Omega_theta])


def spectrum(
    radii: list[float] | np.ndarray,
    a: float = 0.0,
    prograde: bool = True,
) -> np.ndarray:
    """将 epicyclic 频率展平为 1D 谱，便于构造 PositiveSpectralObject。"""
    freqs = epicyclic_frequencies(radii, a, prograde)
    return freqs.flatten()


if __name__ == "__main__":
    print("=" * 60)
    print("Kerr 圆轨道 epicyclic 频率验证（顺行 a=0.5）")
    print("=" * 60)
    a_val = 0.5
    radii = np.array([max(isco_radius(a_val), 6.0), 8.0, 10.0, 15.0])
    freqs = epicyclic_frequencies(radii, a_val, prograde=True)
    print(f"r_ISCO(prograde) = {isco_radius(a_val):.4f}")
    print(f"{'r':>6} {'Ω':>10} {'Ω_r':>10} {'Ω_θ':>10}")
    for r, (Or, Ot) in zip(radii, freqs):
        print(f"{r:6.2f} {orbital_frequency(r, a_val):10.4f} {Or:10.4f} {Ot:10.4f}")

    print("\n" + "=" * 60)
    print("Kerr 圆轨道 epicyclic 频率验证（逆行 a=0.5）")
    print("=" * 60)
    r_retro = isco_radius(a_val, prograde=False)
    radii_retro = np.array([max(r_retro, 7.0), 8.0, 10.0, 15.0])
    freqs_retro = epicyclic_frequencies(radii_retro, a_val, prograde=False)
    print(f"r_ISCO(retrograde) = {r_retro:.4f}")
    print(f"{'r':>6} {'Ω':>10} {'Ω_r':>10} {'Ω_θ':>10}")
    for r, (Or, Ot) in zip(radii_retro, freqs_retro):
        print(f"{r:6.2f} {orbital_frequency(r, a_val, False):10.4f} {Or:10.4f} {Ot:10.4f}")
