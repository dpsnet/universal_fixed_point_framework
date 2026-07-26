#!/usr/bin/env python3
"""
_dirac_qnm_shooting.py —— Dirac QNM 直接积分法（Phase 59F）

使用一阶 Dirac 方程组 + RK4 直接积分，求解 Schwarzschild 背景
的 Dirac QNM 频率。不依赖连分数法或有效势近似。

理论框架
========
Chandrasekhar (1983) 推导的一阶 Dirac 方程组：
    dP/dr* - (κ√f/r)·P = ωQ
    dQ/dr* + (κ√f/r)·Q = -ωP

其中 f = 1-2M/r，κ = l+1/2。

边界条件：
- 视界 (r* → -∞)：√f → 0，P ∝ e^{-iωr*}, Q = -iP (ingoing)
- 无穷远 (r* → +∞)：√f → 1，P ∝ e^{+iωr*}, Q = +iP (outgoing)

流程：
1. 从视界附近向外积分一阶 Dirac 方程组
2. 从无穷远向内积分一阶 Dirac 方程组
3. 匹配点计算线性相关性，搜索零点

参考：
    Chandrasekhar (1983) "The Mathematical Theory of Black Holes" §100
    Schutz & Will (1985) ApJ 291, L33-L36
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any, Tuple


# ============================================================
# 1. 一阶 Dirac 方程组
# ============================================================

def dirac_first_order(r_star: float, y: np.ndarray,
                      kappa: float, omega: complex,
                      M: float = 1.0) -> np.ndarray:
    """
    一阶 Dirac 方程组右侧。

    y = [P, Q]
    返回 dy/dr* = [dP/dr*, dQ/dr*]

    方程：
    dP/dr* = ωQ + (κ√f/r)·P
    dQ/dr* = -ωP - (κ√f/r)·Q
    """
    P, Q = y[0], y[1]

    # 从 r* 反解 r
    r = r_from_tortoise(r_star, M)

    if r <= 2.0 * M:
        # 视界内，√f=0
        dP = omega * Q
        dQ = -omega * P
    else:
        f = 1.0 - 2.0 * M / r
        sqrt_f = np.sqrt(f)
        W = kappa * sqrt_f / r  # superpotential

        dP = omega * Q + W * P
        dQ = -omega * P - W * Q

    return np.array([dP, dQ], dtype=complex)


def tortoise_coord(r: float, M: float = 1.0) -> float:
    """tortoise 坐标 r* = r + 2M·ln(r/2M - 1)。"""
    if r <= 2.0 * M:
        return -np.inf
    return float(r + 2.0 * M * np.log(r / (2.0 * M) - 1.0))


def r_from_tortoise(r_star: float, M: float = 1.0) -> float:
    """从 tortoise 坐标反解径向坐标 r（Newton 法）。"""
    if r_star > 100.0 * M:
        # r* ≈ r 当 r >> 2M
        return r_star
    if r_star < -100.0 * M:
        # r* ≈ 2M·ln(r/2M - 1) 当 r→2M
        return 2.0 * M + 2.0 * M * np.exp(r_star / (2.0 * M) - 1.0)

    r_guess = max(2.0 * M + 1e-6, r_star * 0.5 + M)
    for _ in range(100):
        arg = r_guess / (2.0 * M) - 1.0
        if arg <= 1e-15:
            r_guess = 2.0 * M + 1e-10
            arg = 1e-10
        f_val = r_guess + 2.0 * M * np.log(arg) - r_star
        fp = 1.0 + 2.0 * M / (r_guess - 2.0 * M)
        if abs(fp) < 1e-15:
            fp = 1e-15
        dr = f_val / fp
        r_guess -= dr
        if r_guess <= 2.0 * M:
            r_guess = 2.0 * M + 1e-10
        if abs(dr) < 1e-12:
            break
    return r_guess


# ============================================================
# 2. 边界条件
# ============================================================

def horizon_bc_first_order(r_star_near: float, kappa: float,
                           omega: complex, M: float = 1.0
                           ) -> Tuple[complex, complex]:
    """
    视界附近的一阶 Dirac 边界条件。

    当 √f → 0（r→2M），方程简化为：
    dP/dr* = ωQ, dQ/dr* = -ωP

    Ingoing 解：P ∝ e^{-iωr*}, Q = -iP
    """
    P0 = np.exp(-1j * omega * r_star_near)
    Q0 = -1j * P0
    return P0, Q0


def infinity_bc_first_order(r_star_far: float, kappa: float,
                            omega: complex, M: float = 1.0
                            ) -> Tuple[complex, complex]:
    """
    无穷远的一阶 Dirac 边界条件。

    当 r→∞，√f→1，W→0，方程简化为：
    dP/dr* = ωQ, dQ/dr* = -ωP

    Outgoing 解：P ∝ e^{+iωr*}, Q = +iP
    """
    P0 = np.exp(1j * omega * r_star_far)
    Q0 = 1j * P0
    return P0, Q0


# ============================================================
# 3. 数值积分
# ============================================================

def integrate_first_order(rs_start: float, rs_end: float,
                          kappa: float, omega: complex,
                          M: float = 1.0, n_steps: int = 2000,
                          direction: int = 1
                          ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    积分一阶 Dirac 方程组。

    参数:
        direction: 1=从视界向外，-1=从无穷远向内
    返回:
        rs_grid, P_grid, Q_grid
    """
    if direction > 0:
        P0, Q0 = horizon_bc_first_order(rs_start, kappa, omega, M)
    else:
        P0, Q0 = infinity_bc_first_order(rs_start, kappa, omega, M)

    y = np.array([P0, Q0], dtype=complex)
    h = (rs_end - rs_start) / n_steps

    rs_grid = np.array([rs_start])
    P_grid = np.array([P0])
    Q_grid = np.array([Q0])

    r_star = rs_start
    for _ in range(n_steps):
        r_star += h

        # RK4
        k1 = dirac_first_order(r_star, y, kappa, omega, M)
        k2 = dirac_first_order(r_star + h / 2, y + h / 2 * k1, kappa, omega, M)
        k3 = dirac_first_order(r_star + h / 2, y + h / 2 * k2, kappa, omega, M)
        k4 = dirac_first_order(r_star + h, y + h * k3, kappa, omega, M)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        rs_grid = np.append(rs_grid, r_star)
        P_grid = np.append(P_grid, y[0])
        Q_grid = np.append(Q_grid, y[1])

        if abs(r_star) > 50.0 * M:
            break

    return rs_grid, P_grid, Q_grid


def matching_function(omega: complex, kappa: float, M: float = 1.0,
                      r_match: float = 5.0, n_steps: int = 2000
                      ) -> Tuple[complex, complex, complex, complex]:
    """
    在匹配点计算两侧的 (P, Q) 值。

    返回:
        (P_h, Q_h, P_i, Q_i): 视界侧和无穷远侧的 P, Q
    """
    rs_match = tortoise_coord(r_match, M)

    # 从视界积分
    rs_hor = rs_match - 20.0
    _, P_hor, Q_hor = integrate_first_order(
        rs_hor, rs_match, kappa, omega, M, n_steps, direction=1
    )
    P_h = P_hor[-1]
    Q_h = Q_hor[-1]

    # 从无穷远积分
    rs_inf = rs_match + 20.0
    _, P_inf, Q_inf = integrate_first_order(
        rs_inf, rs_match, kappa, omega, M, n_steps, direction=-1
    )
    P_i = P_inf[-1]
    Q_i = Q_inf[-1]

    return P_h, Q_h, P_i, Q_i


def linear_dependence(P_h: complex, Q_h: complex,
                      P_i: complex, Q_i: complex) -> complex:
    """
    线性相关判定函数。

    一阶 Dirac 方程组的 Wronskian：
    W = P_h·Q_i - P_i·Q_h

    对 QNM ω，两侧积分解在匹配点应线性相关（W=0）。
    """
    W = P_h * Q_i - P_i * Q_h

    # 归一化
    norm = max(abs(P_h), abs(Q_h), abs(P_i), abs(Q_i), 1e-30)
    return W / norm


def find_dirac_qnm_shooting(kappa: float, M: float = 1.0,
                            omega_guess: complex = complex(0.4, -0.1),
                            r_match: float = 5.0,
                            n_steps: int = 2000,
                            max_iter: int = 30) -> Dict[str, Any]:
    """
    使用一阶 Dirac 方程组 + Müller 法求解 QNM 频率。

    参数:
        kappa: κ = l + 1/2
        M: 黑洞质量
        omega_guess: 频率初值
        r_match: 匹配点（推荐 4-8M）
        n_steps: 积分步数
        max_iter: 最大 Müller 迭代次数

    返回:
        {'omega': complex, 'W': complex, 'converged': bool, ...}
    """
    def mismatch(omega):
        P_h, Q_h, P_i, Q_i = matching_function(
            omega, kappa, M, r_match, n_steps
        )
        return linear_dependence(P_h, Q_h, P_i, Q_i)

    # Müller 法
    w0 = complex(omega_guess)
    w1 = complex(omega_guess * 1.02 + 0.01j)
    w2 = complex(omega_guess * 0.98 - 0.01j)

    f0 = mismatch(w0)
    f1 = mismatch(w1)
    f2 = mismatch(w2)

    converged = False

    for n_iter in range(max_iter):
        h1 = w1 - w0
        h2 = w2 - w1
        d1 = (f1 - f0) / h1 if abs(h1) > 1e-30 else 0.0
        d2 = (f2 - f1) / h2 if abs(h2) > 1e-30 else 0.0
        a = (d2 - d1) / (h2 + h1) if abs(h2 + h1) > 1e-30 else 0.0

        b = d1 + a * h1
        c = f0

        disc = np.sqrt(b ** 2 - 4.0 * a * c)
        denom1 = b + disc
        denom2 = b - disc
        dw = -2.0 * c / denom1 if abs(denom1) > abs(denom2) else -2.0 * c / denom2

        w_new = w0 + dw
        f_new = mismatch(w_new)

        w0, w1, w2 = w1, w2, w_new
        f0, f1, f2 = f1, f2, f_new

        if abs(dw) < 1e-8 and abs(f_new) < 1e-8:
            converged = True
            omega = w_new
            break

        omega = w_new

    # 最终结果
    P_h, Q_h, P_i, Q_i = matching_function(omega, kappa, M, r_match, n_steps)
    W_final = linear_dependence(P_h, Q_h, P_i, Q_i)

    return {
        'omega': omega,
        'W': W_final,
        'converged': converged,
        'iterations': n_iter + 1,
        'kappa': kappa,
        'M': M,
        'r_match': r_match,
        'n_steps': n_steps,
        'P_horizon': P_h,
        'Q_horizon': Q_h,
        'P_infinity': P_i,
        'Q_infinity': Q_i,
    }


# ============================================================
# 4. 基准测试
# ============================================================

DIRAC_QNM_REF = {
    (1, 0): (complex(0.378721, -0.096458), "Dolan 2006"),
    (2, 0): (complex(0.522988, -0.089964), "Dolan 2006"),
    (3, 0): (complex(0.640418, -0.091694), "Dolan 2006"),
    (4, 0): (complex(0.743499, -0.092667), "Jing 2005"),
    (1, 1): (complex(0.347678, -0.293755), "Dolan 2006"),
    (2, 1): (complex(0.508146, -0.271327), "Jing 2005"),
    (3, 1): (complex(0.630256, -0.274928), "Jing 2005"),
}


def test_benchmark_shooting():
    """运行 Dirac QNM 打靶法基准测试。"""
    print("=" * 90)
    print("Dirac QNM 一阶方程组直接积分：Schwarzschild (a=0)")
    print("=" * 90)
    print(f"  {'κ':<4} {'l':<5} {'n':<4} "
          f"{'Re(ω_shoot)':<14} {'Im(ω_shoot)':<14} "
          f"{'Re(ω_ref)':<14} {'Im(ω_ref)':<14} "
          f"{'|W|':<12} {'迭代':<6} {'状态':<8}")
    print(f"  {'─'*4} {'─'*5} {'─'*4} "
          f"{'─'*14} {'─'*14} {'─'*14} {'─'*14} "
          f"{'─'*12} {'─'*6} {'─'*8}")

    test_cases = [(1, 0), (2, 0), (3, 0), (1, 1)]
    for kappa, n_mode in test_cases:
        ref_key = (kappa, n_mode)
        omega_guess = DIRAC_QNM_REF[ref_key][0] if ref_key in DIRAC_QNM_REF \
                      else complex(0.4, -0.1)

        result = find_dirac_qnm_shooting(
            kappa, omega_guess=omega_guess,
            r_match=5.0, n_steps=2000, max_iter=20
        )

        omega = result['omega']
        W_val = result['W']
        converged = result['converged']

        omega_ref = DIRAC_QNM_REF[ref_key][0]
        status = "✓" if converged else "✗"
        l_val = kappa - 0.5
        print(f"  {kappa:<4d} {l_val:<+4.1f} {n_mode:<4d} "
              f"{omega.real:<14.6f} {omega.imag:<+14.6f} "
              f"{omega_ref.real:<14.6f} {omega_ref.imag:<+14.6f} "
              f"{abs(W_val):<12.2e} {result['iterations']:<6d} {status}")

    print()
    print("打靶法用一阶 Dirac 方程组 + RK4 积分 + Müller 求根。")
    print("若未收敛，需增加 n_steps 或调整 r_match 参数。")
    print()


def test_wronskian_scan():
    """沿实轴扫描线性相关函数。"""
    print("=" * 90)
    print("线性相关函数 |W| 扫描 (κ=1)")
    print("=" * 90)
    print(f"  {'Re(ω)':<12} {'Im(ω)':<12} {'|W|':<14} {'Re(W)':<16} {'Im(W)':<16}")
    print(f"  {'─'*12} {'─'*12} {'─'*14} {'─'*16} {'─'*16}")

    ref = DIRAC_QNM_REF[(1, 0)][0]

    # 沿虚轴固定，实轴扫描
    for di in [-0.06, -0.03, 0.0, 0.03]:
        for re_w in np.linspace(0.2, 0.6, 5):
            omega_test = complex(re_w, ref.imag + di)
            try:
                P_h, Q_h, P_i, Q_i = matching_function(
                    omega_test, 1, r_match=5.0, n_steps=2000
                )
                W = linear_dependence(P_h, Q_h, P_i, Q_i)
                print(f"  {omega_test.real:<12.4f} {omega_test.imag:<+12.4f} "
                      f"{abs(W):<14.2e} {W.real:<+16.6e} {W.imag:<+16.6e}")
            except Exception as e:
                print(f"  {omega_test.real:<12.4f} {omega_test.imag:<+12.4f} "
                      f"{'ERR':<14} {str(e)[:30]}")
    print()


def test_convergence_steps():
    """测试不同积分步数下的收敛性。"""
    print("=" * 90)
    print("打靶法收敛性测试 (κ=1, n=0)：不同 n_steps 的影响")
    print("=" * 90)
    print(f"  {'n_steps':<10} {'Re(ω)':<14} {'Im(ω)':<14} {'|W|':<14} {'迭代':<6}")
    print(f"  {'─'*10} {'─'*14} {'─'*14} {'─'*14} {'─'*6}")

    ref = DIRAC_QNM_REF[(1, 0)][0]
    for n_steps in [500, 1000, 2000, 4000]:
        result = find_dirac_qnm_shooting(
            1, omega_guess=ref,
            r_match=5.0, n_steps=n_steps, max_iter=15
        )
        omega = result['omega']
        W_val = result['W']
        print(f"  {n_steps:<10d} {omega.real:<14.6f} {omega.imag:<+14.6f} "
              f"{abs(W_val):<14.2e} {result['iterations']:<6d}")

    print()


if __name__ == "__main__":
    test_benchmark_shooting()
    print()
    test_wronskian_scan()
    test_convergence_steps()
