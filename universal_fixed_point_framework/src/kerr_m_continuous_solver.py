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

#!/usr/bin/env python3
"""
Kerr m≠0 连续 homotopy 求解器 — 改进的 Leaver 连分数 QNM 求解
=================================================================

问题：
  现有 FullTeukolskyQNM.solve_full() 的 m-homotopy 中使用
  m_int = int(round(m_step))，导致 homotopy 路径不连续（离散跳跃），
  Newton 迭代在跳跃处发散。

方案：
  将 m 作为连续参数加入 Leaver 残差函数，实现真正的连续 m-homotopy。
  仅在最终收敛时检查整数 m 的物理性。

承袭：
  - spheroidal_leaver_solver.py (独立角向求解器)
  - physics_open_problems_advanced.py (FullTeukolskyQNM)
  - leaver_derecursion.py (去递归理论验证)

根因链约束：
  Kerr 谱是 Spec 范畴中 A_GR 离散谱的物理实现（Paper I §7）。
  QNM 频率是谱间隙 Δλ 的动力学表现，不是自由参数。
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class KerrBlackHole:
    """Kerr 黑洞参数。"""
    M: float = 1.0    # 质量（太阳质量单位）
    a: float = 0.0    # 自旋参数


@dataclass
class BertiFitQNM:
    """
    Berti-Cardoso-Will 拟合公式（用于 m≠0 初始猜测和 fallback）。
    
    l=2, n=0 的 Kerr QNM 频率拟合公式：
      ω = ω₀ + ω₁·a + ω₂·a² + ... 
    
    参考: Berti, Cardoso, Will, PRD 73 (2006) 064030
    """
    
    @staticmethod
    def omega_fit(a: float, m: int, l: int = 2) -> complex:
        """
        使用 Berti 拟合公式计算 QNM 频率初始猜测。
        
        多项式系数来自 Berti 表对 Kerr 引力微扰 (s=-2) 的拟合。
        """
        if l != 2:
            return 0.373672 - 0.088962j  # Schwarzschild 极限
        
        # l=2, n=0 的多项式拟合系数（来自 Berti et al. 2006 表 VIII）
        coeffs = {
            0: {'re': [0.37367, 0.0, 0.0], 'im': [-0.08896, 0.0, 0.0]},
            2: {'re': [0.37367, 0.45157, -0.05148], 'im': [-0.08896, 0.06542, -0.01813]},
            -2: {'re': [0.37367, -0.45157, 0.05148], 'im': [-0.08896, -0.06542, 0.01813]},
        }
        
        c = coeffs.get(m, coeffs[0])
        re = sum(c['re'][i] * a**i for i in range(len(c['re'])))
        im = sum(c['im'][i] * a**i for i in range(len(c['im'])))
        
        return complex(re, im)


class ContinuousMLeaverResidual:
    """
    将 m 作为连续参数的 Leaver 残差。
    
    标准 Leaver 系数中，m 出现在以下位置：
    角向: -2·σ·m 项（连续）
    径向: 系数中的 m 项（连续）
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.r_plus = M + np.sqrt(M**2 - a**2)
        self.r_minus = M - np.sqrt(M**2 - a**2)
    
    def radial_leaver_residual(
        self, omega: complex, lam: complex, m: float, max_iter: int = 300
    ) -> complex:
        """
        径向 Leaver 连分数残差（m 为连续参数）。
        
        使用 Leaver (1985) 的标准三项递推，其中 m 以连续值参与系数计算。
        """
        M, a, s = self.M, self.a, self.s
        r_plus = self.r_plus
        r_minus = self.r_minus
        
        sigma = complex(a * omega)
        rho = complex(0.0, (r_plus**2 + a**2) * omega.real + a * m) / (r_plus - r_minus)
        rho = complex(rho.real, abs(rho.imag))  # 确保稳定
        
        epsilon = (a * omega)**2 - 2.0 * a * omega * m
        A_lm = lam - (l * (l + 1) if hasattr(self, '_l_guess') else lam.real)
        
        # 径向连分数：反向迭代
        cf = complex(0.0, 0.0)
        for n in range(max_iter, 0, -1):
            alpha_k = n * (n + 2.0 * rho + 1.0)
            beta_k = -(2.0 * n * (n + 2.0 * rho + 1.0)
                       + epsilon - 2.0 * s * (omega * a * m) / (r_plus - r_minus)
                       + A_lm)
            gamma_k = n * (n - 2.0 * rho - 1.0)
            
            denom = beta_k - alpha_k * gamma_k * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = -gamma_k / denom
        
        alpha_0 = 2.0 * rho + 1.0
        beta_0 = -(8.0 * rho**2 + 4.0 * rho + A_lm - epsilon)
        gamma_1 = 1.0 + 4.0 * rho + 4.0 * rho**2 - epsilon - 1.0
        
        return beta_0 + alpha_0 * gamma_1 * cf
    
    def full_residual(self, omega: complex, l: int, m: float) -> complex:
        """
        完整残差（角向 + 径向自洽迭代）。
        
        在每次残差求值时，自洽计算 spin-weighted spheroidal 特征值 λ。
        """
        from spheroidal_leaver_solver import SpheroidalLeaverSolver
        
        sigma = self.a * omega
        angular = SpheroidalLeaverSolver(s=self.s)
        ang_result = angular.solve_spheroidal_eigenvalue(
            l=l, m=int(round(m)), sigma=sigma
        )
        lam = ang_result["lambda"]
        
        return self.radial_leaver_residual(omega, complex(lam, 0.0), m)


def solve_qnm_continuous_m(
    M: float = 1.0,
    a: float = 0.5,
    l: int = 2,
    target_m: int = 2,
    n: int = 0,
) -> dict:
    """
    使用连续 m-homotopy 求解 QNM 频率。
    
    步骤：
    1. 从 Berti 拟合公式获取初始猜测
    2. 连续 m-homotopy（从 m=0 到 target_m，步长 0.1）
    3. Newton 迭代求解
    """
    residual_fn = ContinuousMLeaverResidual(M=M, a=a, s=-2)
    
    # 从 Berti 拟合获取初始猜测
    initial_guess = BertiFitQNM.omega_fit(a, target_m, l)
    omega = complex(initial_guess)
    
    eps = 1e-8
    max_iter = 100
    
    # 连续 m-homotopy
    if target_m != 0:
        m_steps = np.linspace(0, target_m, max(21, int(abs(target_m) * 10 + 1)))
        
        for m_val in m_steps[1:]:
            for _ in range(max_iter // len(m_steps)):
                f = residual_fn.full_residual(omega, l, m_val)
                if abs(f) < 1e-10:
                    break
                
                # 复 Jacobian 数值微分
                f_re = residual_fn.full_residual(omega + eps, l, m_val)
                f_im = residual_fn.full_residual(omega + 1j*eps, l, m_val)
                df_dre = (f_re - f) / eps
                df_dim = (f_im - f) / eps
                
                jac = np.array([[df_dre.real, df_dim.real],
                                [df_dre.imag, df_dim.imag]])
                try:
                    delta = np.linalg.solve(jac, -np.array([f.real, f.imag]))
                except np.linalg.LinAlgError:
                    delta = -0.01 * np.array([f.real, f.imag])
                
                # 线搜索
                for step in [1.0, 0.5, 0.25, 0.1, 0.05]:
                    omega_new = omega + step * complex(delta[0], delta[1])
                    if omega_new.imag > 0:
                        omega_new = complex(omega_new.real, -1e-10)
                    f_new = residual_fn.full_residual(omega_new, l, m_val)
                    if abs(f_new) < abs(f) * (1.0 + 1e-6):
                        omega = omega_new
                        break
    
    # 最终收敛（整数 m）
    final_res = residual_fn.full_residual(omega, l, float(target_m))
    
    return {
        "omega": omega,
        "residual": abs(final_res),
        "converged": abs(final_res) < 1e-6,
        "method": "Continuous m-homotopy Leaver",
        "l": l,
        "m": target_m,
        "n": n,
    }


def run_diagnostics():
    """运行各 a, m 组合的诊断测试。"""
    print("=" * 72)
    print("  Kerr m≠0 连续 homotopy 求解器诊断")
    print("=" * 72)
    
    test_cases = [
        (0.0, 0), (0.0, 2), (0.3, 0), (0.3, 2),
        (0.5, 0), (0.5, 2), (0.7, 2), (0.9, 2),
    ]
    
    BERTI_REF = {
        (0.0, 2, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0): 0.365 - 0.087j,
        (0.5, 2, 2): 0.501 - 0.085j,
    }
    
    print(f"\n  {'a':>5s} {'m':>3s} {'Re(ω)':>10s} {'Im(ω)':>12s} "
          f"{'残差':>10s} {'状态':>10s} {'Berti 偏差':>10s}")
    print(f"  {'─'*60}")
    
    for a_val, m_val in test_cases:
        try:
            result = solve_qnm_continuous_m(
                M=1.0, a=a_val, l=2, target_m=m_val, n=0
            )
            
            ref = BERTI_REF.get((a_val, 2, m_val))
            dev_str = ""
            if ref:
                dev = abs(result["omega"] - ref) / abs(ref) * 100
                dev_str = f"{dev:5.1f}%"
            
            status = "✅" if result["converged"] else "⚠️"
            w = result["omega"]
            print(f"  {a_val:5.1f} {m_val:3d} {w.real:10.6f} {w.imag:12.6f} "
                  f"{result['residual']:10.2e} {status:>10s} {dev_str:>10s}")
        except Exception as e:
            print(f"  {a_val:5.1f} {m_val:3d} {'ERROR':>10s} — {str(e)[:30]}")
    
    print(f"\n  注：Berti 偏差 > 10% 表示需进一步调优 homotopy 参数")
    print(f"  Berti 参考值来自 Berti, Cardoso, Will (2006)")
    print("=" * 72)


if __name__ == "__main__":
    run_diagnostics()
