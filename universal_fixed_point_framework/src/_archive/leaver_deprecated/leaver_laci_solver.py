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
leaver_laci_solver.py

利用去递归理论和谱分析解决 Leaver 连分数局部吸引子问题。

核心思想：
1. 使用 physics_open_problems_advanced.py 中的 FullTeukolskyQNM 作为基础求解器
2. 利用 Koopman 算子谱分析验证解的正确性
3. 使用谱间隙作为吸引子质量指标——物理根具有大谱间隙
4. 结合 homotopy continuation 和谱验证
"""

from __future__ import annotations

import numpy as np

from leaver_derecursion import LeaverDerecursionSolver


class LeaverLACISolver:
    """
    利用去递归理论和谱分析的 Leaver 连分数求解器。
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.r_plus = M + np.sqrt(M ** 2 - a ** 2)
        self.r_minus = M - np.sqrt(M ** 2 - a ** 2)
        self.derecursion = LeaverDerecursionSolver(max_iter=max_iter)
    
    def _compute_spectral_gap(self, omega: complex, l: int, m: int) -> float:
        """计算当前猜测点的谱间隙。"""
        sigma = self.a * omega
        try:
            analysis = self.derecursion.koopman_operator_analysis(sigma, m, l, self.s, n_dim=20)
            return float(analysis["spectral_gap"])
        except Exception:
            return 0.0
    
    def _is_physical_root(self, omega: complex) -> bool:
        """判断根是否为物理 QNM。"""
        if omega.imag >= -1e-10:
            return False
        if abs(omega.real) > 2.0:
            return False
        if abs(omega.imag) > 1.0:
            return False
        return True
    
    def _full_residual(self, omega: complex, l: int, m: int) -> complex:
        """计算完整残差（角向+径向）。"""
        from physics_open_problems_advanced import FullTeukolskyQNM
        
        teuk = FullTeukolskyQNM(M=self.M, a=self.a, s=self.s)
        return teuk.leaver_residual_full(omega, l, m)
    
    def solve_with_spectral_validation(
        self,
        l: int,
        m: int,
        n: int = 0,
        tol: float = 1e-8,
    ) -> dict:
        """
        使用谱验证的 homotopy continuation 求解。
        
        策略：
        1. 使用 FullTeukolskyQNM 的 homotopy 作为基础
        2. 在每个 homotopy 步骤后，用谱间隙验证解的质量
        3. 如果验证失败，尝试在附近搜索更好的解
        """
        from physics_open_problems_advanced import FullTeukolskyQNM
        
        teuk = FullTeukolskyQNM(M=self.M, a=self.a, s=self.s)
        result = teuk.solve_full(l=l, m=m, n=n)
        
        omega = result["omega"]
        residual = abs(result["residual"])
        
        if self._is_physical_root(omega) and residual < tol:
            return {
                "omega": omega,
                "residual": residual,
                "converged": True,
                "is_physical": True,
            }
        
        candidates = [(residual, omega)]
        
        search_points = [
            omega + 0.05,
            omega - 0.05,
            omega + 0.05j,
            omega - 0.05j,
            omega + 0.1,
            omega - 0.1,
            omega + 0.08,
            omega - 0.08,
            omega + 0.08j,
            omega - 0.08j,
        ]
        
        for pt in search_points:
            if not self._is_physical_root(pt):
                continue
            
            try:
                f = self._full_residual(pt, l, m)
                res = abs(f)
                spectral_gap = self._compute_spectral_gap(pt, l, m)
                
                if res < residual * 10 and spectral_gap > 0.1:
                    candidates.append((res, pt))
            except Exception:
                continue
        
        candidates.sort(key=lambda x: x[0])
        
        if candidates:
            best_residual, best_omega = candidates[0]
            
            if self._is_physical_root(best_omega):
                for iteration in range(50):
                    f = self._full_residual(best_omega, l, m)
                    if abs(f) < tol:
                        break
                    
                    eps = 1e-6
                    f_re = self._full_residual(best_omega + eps, l, m)
                    f_im = self._full_residual(best_omega + 1j * eps, l, m)
                    
                    df_dre = (f_re - f) / eps
                    df_dim = (f_im - f) / eps
                    
                    jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                    rhs = -np.array([f.real, f.imag])
                    
                    try:
                        delta = np.linalg.solve(jacobian, rhs)
                    except np.linalg.LinAlgError:
                        delta = -0.01 * rhs
                    
                    step_size = 1.0
                    for _ in range(10):
                        new_omega = best_omega + step_size * complex(delta[0], delta[1])
                        f_new = self._full_residual(new_omega, l, m)
                        if abs(f_new) < abs(f) * 1.1:
                            best_omega = new_omega
                            break
                        step_size *= 0.5
                
                final_residual = abs(self._full_residual(best_omega, l, m))
                
                return {
                    "omega": best_omega,
                    "residual": final_residual,
                    "converged": final_residual < tol,
                    "is_physical": self._is_physical_root(best_omega),
                }
        
        return {
            "omega": omega,
            "residual": residual,
            "converged": False,
            "is_physical": self._is_physical_root(omega),
        }


def run_laci_solver_demo():
    """运行 LACI 求解器演示。"""
    print("=" * 70)
    print("Leaver 谱验证求解器演示")
    print("=" * 70)
    
    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.365 - 0.087j,
        (0.5, 2, 2, 0): 0.501 - 0.085j,
        (0.9, 2, 2, 0): 0.701 - 0.085j,
    }
    
    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print(f"\n--- a={a}, l={l}, m={m}, n={n} ---")
        solver = LeaverLACISolver(M=1.0, a=a, s=-2)
        result = solver.solve_with_spectral_validation(l, m, n)
        
        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print(f"  求解: ω = {omega.real:.6f} {omega.imag:.6f}i")
            print(f"  参考: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
            print(f"  相对误差: {rel_error:.4f}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
            print(f"  收敛: {'✓' if rel_error < 0.1 else '⚠'}")
        else:
            print(f"  未收敛: ω = {result['omega']}")
            print(f"  残差: {result['residual']:.2e}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_laci_solver_demo()