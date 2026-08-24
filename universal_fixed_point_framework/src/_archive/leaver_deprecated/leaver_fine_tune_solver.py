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
leaver_fine_tune_solver.py

从已知参考解出发进行微调——验证连分数系数是否正确。

核心思想：
1. 使用 Berti 表的精确值作为初始猜测
2. 进行少量 Newton-Raphson 迭代微调
3. 如果微调后结果与参考值一致，说明连分数系数正确
4. 如果偏离，说明连分数系数存在问题
"""

from __future__ import annotations

import numpy as np

from physics_open_problems_advanced import FullTeukolskyQNM


class LeaverFineTuneSolver:
    """
    从参考解出发进行微调。
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.teuk = FullTeukolskyQNM(M=M, a=a, s=s)
    
    def fine_tune(
        self,
        l: int,
        m: int,
        n: int = 0,
        initial_guess: complex = None,
        max_iter: int = 20,
        tol: float = 1e-12,
    ) -> dict:
        """从初始猜测出发进行微调。"""
        if initial_guess is None:
            omega = complex(0.373672 - 0.088962j)
        else:
            omega = complex(initial_guess)
        
        for iteration in range(max_iter):
            f = self.teuk.leaver_residual_full(omega, l, m)
            
            if abs(f) < tol:
                break
            
            eps = 1e-6
            f_re = self.teuk.leaver_residual_full(omega + eps, l, m)
            f_im = self.teuk.leaver_residual_full(omega + 1j * eps, l, m)
            
            df_dre = (f_re - f) / eps
            df_dim = (f_im - f) / eps
            
            jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
            rhs = -np.array([f.real, f.imag])
            
            try:
                delta = np.linalg.solve(jacobian, rhs)
            except np.linalg.LinAlgError:
                delta = -0.01 * rhs
            
            omega += complex(delta[0], delta[1])
        
        f_final = self.teuk.leaver_residual_full(omega, l, m)
        
        return {
            "omega": omega,
            "residual": abs(f_final),
            "converged": abs(f_final) < tol,
            "is_physical": omega.imag < -1e-10,
        }


def run_fine_tune_demo():
    """运行微调演示。"""
    print("=" * 70)
    print("Leaver 微调求解器演示")
    print("=" * 70)
    
    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.365 - 0.087j,
        (0.5, 2, 2, 0): 0.501 - 0.085j,
        (0.9, 2, 2, 0): 0.701 - 0.085j,
    }
    
    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print(f"\n--- a={a}, l={l}, m={m}, n={n} ---")
        print(f"  参考值: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
        
        solver = LeaverFineTuneSolver(M=1.0, a=a, s=-2)
        
        result = solver.fine_tune(l, m, n, ref_omega)
        
        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print(f"  微调后: ω = {omega.real:.6f} {omega.imag:.6f}i")
            print(f"  相对误差: {rel_error:.4e}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
            print(f"  一致性: {'✓' if rel_error < 1e-4 else '❌'}")
        else:
            print(f"  未收敛: ω = {result['omega']}")
            print(f"  残差: {result['residual']:.2e}")
    
    print("\n" + "=" * 70)
    
    print("\n【关键测试】验证连分数系数是否正确")
    print("如果从精确参考值出发微调后结果一致，说明连分数系数正确")
    print("如果微调后偏离，说明连分数系数存在问题")


if __name__ == "__main__":
    run_fine_tune_demo()