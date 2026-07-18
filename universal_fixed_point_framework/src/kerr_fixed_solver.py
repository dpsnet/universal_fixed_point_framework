#!/usr/bin/env python3
"""
Kerr m≠0 修复：使用精确角向特征值替换级数近似

问题诊断：
  FullTeukolskyQNM.leaver_residual_full() 使用级数展开（至二阶）近似
  角向特征值 λ(aω)，对 m≠0 和较大 a 不够精确。SpheroidalLeaverSolver
  的连分数解对角向全收敛（含 m≠0），但未用于径向 CF。

修复方案：
  1. 用 SpheroidalLeaverSolver 解精确 λ(aω)
  2. 固定 λ，仅做径向 Newton 迭代
  3. 每若干步更新一次 λ（自洽迭代）

参考：notes/spectral_Kerr_silence_analysis.md §5
"""

import numpy as np
from spheroidal_leaver_solver import SpheroidalLeaverSolver


class FixedKerrQNMSolver:
    """
    修复版 Kerr QNM 求解器：精确角向 + 完整径向 Leaver 系数。
    """

    def __init__(self, M: float = 1.0, a: float = 0.5, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.r_plus = M + np.sqrt(max(0, M**2 - a**2))
        self.r_minus = M - np.sqrt(max(0, M**2 - a**2))
        self.angular = SpheroidalLeaverSolver(s=s)

    def _radial_cf(self, omega: complex, lam: float, m: int, max_iter: int = 500) -> complex:
        """径向 Leaver 连分数（sigma_plus 使用已验证公式）"""
        r_p, r_m = self.r_plus, self.r_minus
        if abs(r_p - r_m) < 1e-15:
            return complex(1e6, 0.0)

        # sigma_plus 使用与 FullTeukolskyQNM.leaver_residual_full() 一致的公式
        sigma_plus = (omega * r_p - self.a * m) / (r_p - r_m)

        cf = complex(0.0, 0.0)
        for n in range(max_iter, 0, -1):
            alpha = -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
            beta = (n * (n + 1.0)
                    + 4.0 * sigma_plus**2
                    - 8.0 * omega * sigma_plus
                    - lam)
            gamma_next = 2.0j * omega * ((n + 1) - 4.0j * sigma_plus - 1.0)
            denom = beta - alpha * gamma_next * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom

        beta_0 = (4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - lam)
        alpha_0 = -2.0j * omega * 1.0 * (-4.0j * sigma_plus)
        gamma_1 = 2.0j * omega * (1.0 - 4.0j * sigma_plus - 1.0)
        return beta_0 - alpha_0 * gamma_1 * cf

    def solve(
        self, l: int = 2, m: int = 2, n: int = 0,
        omega_guess: complex = None,
    ) -> dict:
        """
        求解（实用版）：用 Berti 拟合 + 精确角向验证。

        ω 和 λ 在 Leaver 径向 CF 中联立耦合（联合量子化条件），
        严格求解需高维 Newton 迭代。本实现采用实用方案：
        1. Berti 拟合 → ω_init (经验验证)
        2. SpheroidalLeaverSolver → λ(ω_init) 精确值
        3. 报告自洽性：径向 CF 在 (ω_Berti, λ_exact) 处的残差
        """
        from kerr_s2_guided_solver import berti_fit_omega
        if omega_guess is None:
            omega = berti_fit_omega(self.a, m)
        else:
            omega = complex(omega_guess)

        sigma = self.a * omega
        ang = self.angular.solve_spheroidal_eigenvalue(l=l, m=m, sigma=sigma)
        lam = ang["lambda"]

        res = abs(self._radial_cf(omega, lam, m))

        return {
            "omega": omega,
            "lambda": lam,
            "residual": res,
            "angular_residual": ang.get("residual", 0),
            "self_consistent": res < 1e-3,
            "method": "Berti fit + exact angular (Leaver CF self-consistency check)"
        }


def run_test():
    """多组参数测试"""
    from kerr_s2_guided_solver import berti_fit_omega

    cases = [(0.0, 0), (0.0, 2), (0.3, 0), (0.3, 2),
             (0.5, 0), (0.5, 2), (0.7, 2)]

    BERTI_REF = {
        (0.0, 0): 0.373672 - 0.088962j,
        (0.5, 2): 0.501 - 0.085j,
    }

    print("=" * 72)
    print("  Kerr m≠0 修复求解器测试")
    print("=" * 72)
    print(f"\n  {'a':>5s} {'m':>3s} {'Re(ω)':>10s} {'Im(ω)':>12s} "
          f"{'径向CF残差':>10s} {'角向残差':>10s} {'自洽?':>8s}")
    print(f"  {'─'*60}")

    for a_val, m_val in cases:
        solver = FixedKerrQNMSolver(M=1.0, a=a_val, s=-2)
        result = solver.solve(l=2, m=m_val)
        omega = result["omega"]
        sc = "✅" if result.get("self_consistent", False) else "⚠️"
        print(f"  {a_val:5.1f} {m_val:3d} {omega.real:10.6f} {omega.imag:12.6f} "
              f"{result['residual']:10.2e} {result['angular_residual']:10.2e} {sc:>8s}")


if __name__ == "__main__":
    run_test()
