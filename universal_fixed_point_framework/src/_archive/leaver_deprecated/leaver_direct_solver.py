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
leaver_direct_solver.py

直接求解 Leaver 连分数——基于 physics_open_problems_advanced.py 的残差函数。

核心思想：
1. 使用 physics_open_problems_advanced.py 中的 FullTeukolskyQNM 残差函数
2. 使用 least_squares 进行稳定的非线性最小化
3. 使用多个初始猜测提高成功率
4. 利用物理约束限制搜索空间
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from physics_open_problems_advanced import FullTeukolskyQNM


class LeaverDirectSolver:
    """
    直接求解 Leaver 连分数。
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.teuk = FullTeukolskyQNM(M=M, a=a, s=s)
    
    def _residual_fun(self, x: np.ndarray, l: int, m: int) -> np.ndarray:
        """残差函数——使用 FullTeukolskyQNM。"""
        omega = complex(x[0], x[1])
        f = self.teuk.leaver_residual_full(omega, l, m)
        return np.array([f.real, f.imag])
    
    def solve_direct(
        self,
        l: int,
        m: int,
        n: int = 0,
        initial_guess: np.ndarray | None = None,
    ) -> dict:
        """使用 least_squares 直接求解。"""
        if initial_guess is None:
            x0 = np.array([0.4, -0.1])
        else:
            x0 = initial_guess
        
        result = least_squares(
            self._residual_fun,
            x0,
            args=(l, m),
            method='trf',
            ftol=1e-12,
            xtol=1e-12,
            gtol=1e-12,
            max_nfev=500,
        )
        
        omega = complex(result.x[0], result.x[1])
        residual_norm = result.cost
        
        return {
            "omega": omega,
            "residual": residual_norm,
            "converged": result.success,
            "nfev": result.nfev,
            "is_physical": self._is_physical_root(omega),
        }
    
    def _is_physical_root(self, omega: complex) -> bool:
        """判断根是否为物理 QNM。"""
        if omega.imag >= -1e-10:
            return False
        if abs(omega.real) > 2.0:
            return False
        if abs(omega.imag) > 1.0:
            return False
        return True
    
    def solve_with_multi_start(
        self,
        l: int,
        m: int,
        n: int = 0,
    ) -> dict:
        """使用多个初始猜测求解。"""
        freq_guesses = np.linspace(0.2, 0.8, 7)
        decay_guesses = np.linspace(-0.15, -0.02, 5)
        
        best_result = None
        best_residual = np.inf
        
        for freq in freq_guesses:
            for decay in decay_guesses:
                x0 = np.array([freq, decay])
                
                try:
                    result = self.solve_direct(l, m, n, x0)
                    
                    if result["converged"] and result["is_physical"]:
                        if result["residual"] < best_residual:
                            best_result = result
                            best_residual = result["residual"]
                except Exception:
                    continue
        
        if best_result is None:
            result = self.solve_direct(l, m, n)
            return result
        
        return best_result


def run_direct_solver_demo():
    """运行直接求解器演示。"""
    print("=" * 70)
    print("Leaver 直接求解器演示（基于 FullTeukolskyQNM）")
    print("=" * 70)
    
    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.365 - 0.087j,
        (0.5, 2, 2, 0): 0.501 - 0.085j,
        (0.9, 2, 2, 0): 0.701 - 0.085j,
    }
    
    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print(f"\n--- a={a}, l={l}, m={m}, n={n} ---")
        solver = LeaverDirectSolver(M=1.0, a=a, s=-2)
        result = solver.solve_with_multi_start(l, m, n)
        
        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print(f"  求解: ω = {omega.real:.6f} {omega.imag:.6f}i")
            print(f"  参考: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
            print(f"  相对误差: {rel_error:.4f}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  函数调用次数: {result.get('nfev', 0)}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
            print(f"  收敛: {'✓' if rel_error < 0.1 else '⚠'}")
        else:
            print(f"  未收敛: ω = {result['omega']}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_direct_solver_demo()