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
schwarzschild_geodesic_verification.py

Schwarzschild 度规下测地线偏差/圆轨道频率的解析验证模块。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 提供 Schwarzschild 圆轨道径向与垂直 epicyclic 频率的标准解析公式，
  用于与 geodesic_instance.py 的真实度规模式对接。

约定：
- 几何化单位：G = c = M = 1。
- 圆轨道半径 r 必须大于最内稳定圆轨道 r_ISCO = 6。
- 径向 epicyclic 频率：Ω_r = Ω sqrt(1 - 6/r)
- 垂直 epicyclic 频率：Ω_θ = Ω
  其中 Ω = r^{-3/2} 为圆轨道角频率。
"""

from __future__ import annotations

import numpy as np


def orbital_frequency(r: float | np.ndarray) -> float | np.ndarray:
    """Schwarzschild 圆轨道角频率 Ω = r^{-3/2}。"""
    r = np.asarray(r, dtype=float)
    if np.any(r <= 0):
        raise ValueError("半径 r 必须为正")
    return r ** (-1.5)


def radial_epicyclic_frequency(r: float | np.ndarray) -> float | np.ndarray:
    """径向 epicyclic 频率 Ω_r = Ω sqrt(1 - 6/r)。"""
    r = np.asarray(r, dtype=float)
    if np.any(r < 6.0):
        raise ValueError("Schwarzschild 稳定圆轨道要求 r >= 6（ISCO）")
    Omega = orbital_frequency(r)
    return Omega * np.sqrt(1.0 - 6.0 / r)


def vertical_epicyclic_frequency(r: float | np.ndarray) -> float | np.ndarray:
    """垂直 epicyclic 频率 Ω_θ = Ω。"""
    return orbital_frequency(r)


def epicyclic_frequencies(radii: list[float] | np.ndarray) -> np.ndarray:
    """
    返回给定半径列表的 (Ω_r, Ω_θ) 频率数组。

    返回形状：(len(radii), 2)
    """
    radii = np.asarray(radii, dtype=float)
    Omega_r = radial_epicyclic_frequency(radii)
    Omega_theta = vertical_epicyclic_frequency(radii)
    return np.column_stack([Omega_r, Omega_theta])


def spectrum(radii: list[float] | np.ndarray) -> np.ndarray:
    """将 epicyclic 频率展平为 1D 谱，便于构造 PositiveSpectralObject。"""
    freqs = epicyclic_frequencies(radii)
    return freqs.flatten()


def isco_radius() -> float:
    """最内稳定圆轨道半径。"""
    return 6.0


if __name__ == "__main__":
    radii = np.array([7.0, 8.0, 10.0, 15.0, 30.0])
    freqs = epicyclic_frequencies(radii)

    print("=" * 60)
    print("Schwarzschild 圆轨道 epicyclic 频率验证")
    print("=" * 60)
    print(f"{'r':>6} {'Ω':>10} {'Ω_r':>10} {'Ω_θ':>10}")
    for r, (Or, Ot) in zip(radii, freqs):
        print(f"{r:6.2f} {orbital_frequency(r):10.4f} {Or:10.4f} {Ot:10.4f}")
