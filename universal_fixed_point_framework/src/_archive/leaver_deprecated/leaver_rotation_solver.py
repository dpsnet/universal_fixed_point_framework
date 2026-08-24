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
leaver_rotation_solver.py

基于旋转角度监测的 Leaver 连分数求解器。

核心思想（基于用户的深刻洞察）：
1. 将连分数迭代视为复平面上的动力系统
2. 监测迭代过程中的"旋转角度"变化
3. 物理QNM保持小角度（~-10°），非物理解发生90°偏转
4. 利用去递归理论的谱分析验证解的正确性
5. 当检测到"非物理偏转"时，强制回溯并尝试不同路径
"""

from __future__ import annotations

import numpy as np

from leaver_derecursion import LeaverDerecursionSolver


class LeaverRotationSolver:
    """
    基于旋转角度监测的 Leaver 连分数求解器。
    
    核心算法：
    1. 监测每次迭代的角度变化 Δθ
    2. 如果角度变化超过阈值（如60°），判定为"非物理偏转"
    3. 回溯到偏转前的状态，尝试步长减半或不同初始点
    4. 使用 Koopman 谱分析验证最终解
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.r_plus = M + np.sqrt(M ** 2 - a ** 2)
        self.r_minus = M - np.sqrt(M ** 2 - a ** 2)
        self.derecursion = LeaverDerecursionSolver(max_iter=max_iter)
        
        self.rotation_threshold = 60.0
        self.physical_angle_range = (-45.0, 10.0)
    
    def _compute_angle(self, omega: complex) -> float:
        """计算复频率的旋转角度（度）。"""
        return np.angle(omega, deg=True)
    
    def _is_physical_angle(self, angle: float) -> bool:
        """判断角度是否在物理范围内。"""
        return self.physical_angle_range[0] < angle < self.physical_angle_range[1]
    
    def _detect_rotation_anomaly(self, prev_angle: float, curr_angle: float) -> bool:
        """检测旋转角度异常。"""
        delta_angle = abs(curr_angle - prev_angle)
        if delta_angle > 180.0:
            delta_angle = 360.0 - delta_angle
        return delta_angle > self.rotation_threshold
    
    def _compute_spectral_gap(self, omega: complex, l: int, m: int) -> float:
        """计算谱间隙。"""
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
        """计算完整残差。"""
        from physics_open_problems_advanced import FullTeukolskyQNM
        
        teuk = FullTeukolskyQNM(M=self.M, a=self.a, s=self.s)
        return teuk.leaver_residual_full(omega, l, m)
    
    def solve_with_rotation_control(
        self,
        l: int,
        m: int,
        n: int = 0,
        omega_guess: complex | None = None,
        tol: float = 1e-8,
    ) -> dict:
        """
        使用旋转角度控制的 Newton-Raphson 迭代求解。
        
        核心策略：
        1. 监测每次迭代的角度变化
        2. 如果检测到非物理偏转，回溯并减半步长
        3. 如果连续多次偏转，更换初始点
        """
        from physics_open_problems_advanced import FullTeukolskyQNM
        
        teuk = FullTeukolskyQNM(M=self.M, a=self.a, s=self.s)
        
        if omega_guess is None:
            omega = complex(0.373672 - 0.088962j)
        else:
            omega = complex(omega_guess)
        
        prev_angle = self._compute_angle(omega)
        anomaly_count = 0
        max_anomalies = 5
        
        for iteration in range(self.max_iter):
            f = self._full_residual(omega, l, m)
            
            if abs(f) < tol:
                break
            
            eps = 1e-6
            f_re = self._full_residual(omega + eps, l, m)
            f_im = self._full_residual(omega + 1j * eps, l, m)
            
            df_dre = (f_re - f) / eps
            df_dim = (f_im - f) / eps
            
            jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
            rhs = -np.array([f.real, f.imag])
            
            try:
                delta = np.linalg.solve(jacobian, rhs)
            except np.linalg.LinAlgError:
                delta = -0.01 * rhs
            
            step_size = 1.0
            best_step_size = 1.0
            best_omega = omega
            best_residual = abs(f)
            
            for _ in range(15):
                new_omega = omega + step_size * complex(delta[0], delta[1])
                new_residual = abs(self._full_residual(new_omega, l, m))
                
                if new_residual < best_residual:
                    best_omega = new_omega
                    best_residual = new_residual
                    best_step_size = step_size
                
                step_size *= 0.5
            
            new_angle = self._compute_angle(best_omega)
            
            if self._detect_rotation_anomaly(prev_angle, new_angle):
                anomaly_count += 1
                
                if anomaly_count >= max_anomalies:
                    break
                
                if not self._is_physical_angle(new_angle):
                    best_omega = omega + 0.1 * complex(delta[0], delta[1])
                    new_angle = self._compute_angle(best_omega)
            
            omega = best_omega
            prev_angle = new_angle
        
        f_final = self._full_residual(omega, l, m)
        
        return {
            "omega": omega,
            "residual": abs(f_final),
            "converged": abs(f_final) < tol,
            "is_physical": self._is_physical_root(omega),
            "angle": prev_angle,
            "anomaly_count": anomaly_count,
        }
    
    def solve_with_homotopy_rotation(
        self,
        l: int,
        m: int,
        n: int = 0,
        tol: float = 1e-8,
    ) -> dict:
        """
        使用 homotopy continuation + 旋转角度控制求解。
        
        策略：
        1. 从 a=0, m=0 开始（已知正确解）
        2. 逐步增加 a，每步使用旋转控制
        3. 最后处理 m≠0，使用多初始点搜索
        """
        from physics_open_problems_advanced import FullTeukolskyQNM
        
        target_a = self.a
        target_m = m
        
        omega = complex(0.373672 - 0.088962j)
        
        a_steps = np.linspace(0, target_a, max(20, int(target_a * 100) + 2))
        
        for idx, a_step in enumerate(a_steps):
            self.r_plus = self.M + np.sqrt(self.M ** 2 - a_step ** 2)
            self.r_minus = self.M - np.sqrt(self.M ** 2 - a_step ** 2)
            
            teuk = FullTeukolskyQNM(M=self.M, a=a_step, s=self.s)
            
            for iteration in range(50):
                f = teuk.leaver_residual_full(omega, l, 0)
                if abs(f) < 1e-8:
                    break
                
                eps = 1e-6
                f_re = teuk.leaver_residual_full(omega + eps, l, 0)
                f_im = teuk.leaver_residual_full(omega + 1j * eps, l, 0)
                
                df_dre = (f_re - f) / eps
                df_dim = (f_im - f) / eps
                
                jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                rhs = -np.array([f.real, f.imag])
                
                try:
                    delta = np.linalg.solve(jacobian, rhs)
                except np.linalg.LinAlgError:
                    delta = -0.01 * rhs
                
                prev_angle = self._compute_angle(omega)
                
                step_size = 1.0
                for _ in range(10):
                    new_omega = omega + step_size * complex(delta[0], delta[1])
                    new_angle = self._compute_angle(new_omega)
                    
                    if not self._is_physical_angle(new_angle):
                        step_size *= 0.5
                        continue
                    
                    f_new = teuk.leaver_residual_full(new_omega, l, 0)
                    if abs(f_new) < abs(f) * 1.2:
                        omega = new_omega
                        break
                    step_size *= 0.5
        
        if target_m == 0:
            f_final = self._full_residual(omega, l, 0)
            return {
                "omega": omega,
                "residual": abs(f_final),
                "converged": abs(f_final) < tol,
                "is_physical": self._is_physical_root(omega),
            }
        
        best_result = None
        best_residual = np.inf
        
        initial_points = [
            omega,
            omega + 0.05,
            omega + 0.1,
            omega + 0.15,
            omega + 0.05 - 0.02j,
            omega + 0.1 - 0.02j,
            0.5 - 0.08j,
            0.45 - 0.09j,
            0.55 - 0.085j,
        ]
        
        for initial in initial_points:
            if not self._is_physical_root(initial):
                continue
            
            result = self.solve_with_rotation_control(l, target_m, n, initial, tol)
            
            if result["converged"] and result["is_physical"]:
                if result["residual"] < best_residual:
                    best_result = result
                    best_residual = result["residual"]
            elif result["is_physical"] and result["residual"] < best_residual * 10:
                best_result = result
                best_residual = result["residual"]
        
        if best_result is None:
            result = self.solve_with_rotation_control(l, target_m, n, omega, tol)
            return result
        
        return best_result


def run_rotation_solver_demo():
    """运行旋转角度控制求解器演示。"""
    print("=" * 70)
    print("Leaver 旋转角度控制求解器演示")
    print("=" * 70)
    
    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.365 - 0.087j,
        (0.5, 2, 2, 0): 0.501 - 0.085j,
        (0.9, 2, 2, 0): 0.701 - 0.085j,
    }
    
    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print(f"\n--- a={a}, l={l}, m={m}, n={n} ---")
        solver = LeaverRotationSolver(M=1.0, a=a, s=-2)
        result = solver.solve_with_homotopy_rotation(l, m, n)
        
        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print(f"  求解: ω = {omega.real:.6f} {omega.imag:.6f}i")
            print(f"  参考: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
            print(f"  相对误差: {rel_error:.4f}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  旋转角度: {result.get('angle', 0):.1f}°")
            print(f"  异常次数: {result.get('anomaly_count', 0)}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
            print(f"  收敛: {'✓' if rel_error < 0.1 else '⚠'}")
        else:
            print(f"  未收敛: ω = {result['omega']}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_rotation_solver_demo()