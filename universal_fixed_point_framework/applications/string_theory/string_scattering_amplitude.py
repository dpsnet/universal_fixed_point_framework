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
string_scattering_amplitude.py

弦论 4-快子散射振幅的解析实现，用于与通用不动点范畴框架的弦论实例对接。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 提供 Veneziano（开弦）与 Virasoro-Shapiro（闭弦）两种标准振幅的数值计算，
  并将散射振幅的 Regge 极点与 string_instance.py 中的离散谱进行比对。

约定：
- 开弦 Regge 轨迹：α(s) = 1 + α' s，基态快子 m² = -1/α'，质量less 在 s = 0。
- 闭弦 Regge 轨迹：α(s) = 1 + α' s / 4，基态快子 m² = -4/α'，质量less 在 s = 0。
- 这些约定与 string_instance.py 中 m_n² 的构造保持一致（open/closed 选项）。
"""

from __future__ import annotations

import numpy as np
from scipy.special import gamma

DEFAULT_ALPHA_PRIME = 1.0


def open_regge_trajectory(s: float | np.ndarray, alpha_prime: float = DEFAULT_ALPHA_PRIME) -> float | np.ndarray:
    """开弦 Regge 轨迹 α(s) = 1 + α' s。"""
    return 1.0 + alpha_prime * s


def closed_regge_trajectory(s: float | np.ndarray, alpha_prime: float = DEFAULT_ALPHA_PRIME) -> float | np.ndarray:
    """闭弦 Regge 轨迹 α(s) = 1 + α' s / 4。"""
    return 1.0 + alpha_prime * s / 4.0


def _beta(a, b):
    """Euler Beta 函数 B(a,b) = Γ(a)Γ(b)/Γ(a+b)。"""
    return gamma(a) * gamma(b) / gamma(a + b)


def _regularize(z, eps: float = 1e-12):
    """在实轴极点处加入微小虚部，避免 Γ 函数发散导致数值中断。"""
    if isinstance(z, (int, float)):
        return complex(z, eps)
    return z.astype(complex) + 1j * eps


def veneziano_amplitude(
    s: float | np.ndarray,
    t: float | np.ndarray,
    alpha_prime: float = DEFAULT_ALPHA_PRIME,
    g2: float = 1.0,
    eps: float = 1e-12,
) -> float | np.ndarray:
    """
    开弦 4-快子 Veneziano 振幅。

    对 4 个等质量快子，运动学约束为 s + t + u = 4 m²_ tachyon = -4 / α'。
    振幅为三项 Beta 函数之和：
        A(s,t) = g² [B(-α(s), -α(t)) + B(-α(t), -α(u)) + B(-α(u), -α(s))]
    """
    m2_tachyon = -1.0 / alpha_prime
    kinematic_sum = 4.0 * m2_tachyon
    u = kinematic_sum - s - t

    a = _regularize(-open_regge_trajectory(s, alpha_prime), eps)
    b = _regularize(-open_regge_trajectory(t, alpha_prime), eps)
    c = _regularize(-open_regge_trajectory(u, alpha_prime), eps)

    amp = g2 * (_beta(a, b) + _beta(b, c) + _beta(c, a))
    return np.real(amp)


def virasoro_shapiro_amplitude(
    s: float | np.ndarray,
    t: float | np.ndarray,
    alpha_prime: float = DEFAULT_ALPHA_PRIME,
    g2: float = 1.0,
    eps: float = 1e-12,
) -> float | np.ndarray:
    """
    闭弦 4-快子 Virasoro-Shapiro 振幅。

    运动学约束为 s + t + u = 4 m²_tachyon = -16 / α'。
    振幅为：
        A(s,t) = g² Γ(-α(s)) Γ(-α(t)) Γ(-α(u))
                     / [Γ(1+α(s)) Γ(1+α(t)) Γ(1+α(u))]
    """
    m2_tachyon = -4.0 / alpha_prime
    kinematic_sum = 4.0 * m2_tachyon
    u = kinematic_sum - s - t

    a = _regularize(-closed_regge_trajectory(s, alpha_prime), eps)
    b = _regularize(-closed_regge_trajectory(t, alpha_prime), eps)
    c = _regularize(-closed_regge_trajectory(u, alpha_prime), eps)

    numerator = gamma(a) * gamma(b) * gamma(c)
    denominator = gamma(1.0 + a) * gamma(1.0 + b) * gamma(1.0 + c)
    amp = g2 * numerator / denominator
    return np.real(amp)


def pole_masses_squared(
    alpha_prime: float = DEFAULT_ALPHA_PRIME,
    string_type: str = "open",
    n_poles: int = 10,
) -> np.ndarray:
    """
    返回 Regge 轨迹上从 α(s)=0 开始的极点质量平方列表（含快子）。

    open : m² = (k - 1) / α'，k = 0, 1, ..., n_poles-1
    closed : m² = 4 (k - 1) / α'，k = 0, 1, ..., n_poles-1
    """
    if string_type not in {"open", "closed"}:
        raise ValueError("string_type 必须是 'open' 或 'closed'")
    k = np.arange(n_poles)
    if string_type == "open":
        return (k - 1) / alpha_prime
    return 4.0 * (k - 1) / alpha_prime


def physical_pole_masses_squared(
    alpha_prime: float = DEFAULT_ALPHA_PRIME,
    string_type: str = "open",
    n_modes: int = 10,
) -> np.ndarray:
    """
    返回与 string_instance.py 中 Regge 谱对应的物理极点质量平方（去掉快子）。

    对 n_modes 个振动模式，从基态（质量less）开始，对应 α(s)=1,2,...,n_modes。
    """
    all_poles = pole_masses_squared(alpha_prime, string_type, n_poles=n_modes + 1)
    # 去掉 α(s)=0 对应的快子，保留 α(s)≥1 的物理态
    return all_poles[1:]


def amplitude_grid(
    amplitude_func,
    s_range: tuple[float, float] = (-1.0, 4.0),
    t_range: tuple[float, float] = (-1.0, 4.0),
    n_points: int = 100,
    alpha_prime: float = DEFAULT_ALPHA_PRIME,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    在 (s,t) 平面上生成散射振幅网格，便于可视化极点结构。

    返回
    ------
    s_grid, t_grid, amplitude_values : 形状均为 (n_points, n_points)
    """
    s_vals = np.linspace(s_range[0], s_range[1], n_points)
    t_vals = np.linspace(t_range[0], t_range[1], n_points)
    s_grid, t_grid = np.meshgrid(s_vals, t_vals)
    amp_values = amplitude_func(s_grid, t_grid, alpha_prime=alpha_prime, **kwargs)
    return s_grid, t_grid, amp_values
