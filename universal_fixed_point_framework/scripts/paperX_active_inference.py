#!/usr/bin/env python3
"""
UFPF 主动推断 toy model：通过动作改变外部目标态以降低预测误差
=========================================================

在预测编码/active inference 框架中，系统不仅被动地最小化内部表征的预测误差，
还可以通过动作改变外部输入，使外部世界匹配内部预测。本节用谱流语言实现一个
极简的主动推断 toy model：

  - 内部预测（prior/desired）：ρ_desired（例如"静止"）
  - 外部目标态：ρ_ext(α) = α·ρ_forward + (1-α)·ρ_desired
  - 动作参数 α(t)：系统通过学习调整 α，使当前状态 A(t) 尽可能接近 ρ_desired

演化方程：
    dA/dt = [G_ext, A] + [G_int, A] + κ·(D(A) - A) + s_ext·(ρ_ext(α) - A)
    dα/dt = -γ · ∂F/∂α

其中：
  - F = ||ρ_desired - A||_HS 为预测误差
  - γ 为动作学习率
  - s_ext 为外部目标牵引强度

场景：视觉-前庭冲突
  - 初始：视觉通道说"前进"（α=1），前庭/内部预测希望"静止"（ρ_desired=ρ_stationary）
  - 动作目标：降低 α，让外部目标态从"前进"滑向"静止"，从而匹配内部预测
  - 结果：预测误差随时间下降，系统通过动作解决感知冲突

参考：
  - Friston et al. (2017) Active inference: a process theory
  - notes/04_lorentz_gravity/sensory_integration_time_ruler.md §4.8
"""

import os
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


class ActiveInferenceIntegrator:
    """主动推断谱流积分器。动作参数 α 控制外部目标态 ρ_ext(α) 的插值。"""

    def __init__(self, dim: int = 6, gamma: float = 1.0, kappa: float = 1.0,
                 s_ext: float = 1.5, seed: int = 42):
        self.dim = dim
        self.gamma = gamma
        self.kappa = kappa
        self.s_ext = s_ext
        np.random.seed(seed)

        # 内部记忆/预测生成元
        G_int = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
        self.G_int = (G_int - G_int.conj().T) / 2.0

        # 外部驱动生成元
        G_ext = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
        self.G_ext = (G_ext - G_ext.conj().T) / 2.0

        # 固定基投影
        self.P = [np.outer(np.eye(dim)[:, i], np.eye(dim)[:, i])
                  for i in range(dim)]

        # 目标态：前进 vs 静止
        rho_forward = np.zeros((dim, dim), dtype=complex)
        rho_forward[0, 0] = 0.90
        rho_forward[1, 1] = 0.10
        rho_forward /= np.trace(rho_forward)
        self.rho_forward = rho_forward

        rho_desired = np.zeros((dim, dim), dtype=complex)
        rho_desired[3, 3] = 0.90
        rho_desired[4, 4] = 0.10
        rho_desired /= np.trace(rho_desired)
        self.rho_desired = rho_desired

    def external_target(self, alpha: float) -> np.ndarray:
        """外部目标态随动作参数 α 插值：α·ρ_forward + (1-α)·ρ_desired。"""
        return alpha * self.rho_forward + (1.0 - alpha) * self.rho_desired

    def diagonal_projection(self, A: np.ndarray) -> np.ndarray:
        D = np.zeros_like(A)
        for P in self.P:
            D += P @ A @ P
        return D

    def prediction_error(self, A: np.ndarray) -> float:
        """预测误差：目标态与当前态的 HS 偏差。"""
        return np.linalg.norm(self.rho_desired - A, 'fro')

    def step(self, A: np.ndarray, alpha: float, dt: float) -> np.ndarray:
        """单步谱流演化（不含主动推断更新）。"""
        G_tot = self.G_ext + self.G_int
        U = expm(dt * G_tot)
        A_prime = U @ A @ U.conj().T
        rho_ext = self.external_target(alpha)
        A_next = (A_prime
                  + dt * self.kappa * (self.diagonal_projection(A_prime) - A_prime)
                  + dt * self.s_ext * (rho_ext - A_prime))
        A_next = (A_next + A_next.conj().T) / 2.0
        return A_next

    def evolve(self, A0: np.ndarray, alpha0: float, t_span: tuple, dt: float,
               active: bool = True) -> dict:
        """
        演化主动推断系统。

        active=True 时，α 随预测误差更新；active=False 时 α 固定为 alpha0。
        """
        t0, tf = t_span
        t_array = np.arange(t0, tf + dt, dt)
        n_steps = len(t_array) - 1

        A = A0.copy()
        alpha = alpha0
        records = {'t': [], 'A': [], 'alpha': [], 'error': [], 'active': active}
        records['t'].append(t0)
        records['A'].append(A.copy())
        records['alpha'].append(alpha)
        records['error'].append(self.prediction_error(A))

        for i in range(n_steps):
            A = self.step(A, alpha, dt)

            if active:
                err_current = self.prediction_error(A)
                # 短视域有限差分估计 ∂F/∂α
                delta_alpha = 0.05
                alpha_plus = min(alpha + delta_alpha, 1.0)
                A_pert = A.copy()
                for _ in range(3):
                    A_pert = self.step(A_pert, alpha_plus, dt)
                err_plus = self.prediction_error(A_pert)
                dF_dalpha = (err_plus - err_current) / delta_alpha
                alpha = alpha - self.gamma * dF_dalpha * dt
                alpha = float(np.clip(alpha, 0.0, 1.0))

            records['t'].append(t_array[i + 1])
            records['A'].append(A.copy())
            records['alpha'].append(alpha)
            records['error'].append(self.prediction_error(A))

        for key in ['t', 'A', 'alpha', 'error']:
            records[key] = np.array(records[key])
        return records


def run_active_inference_demo(dim: int = 6, t_span: tuple = (0.0, 8.0), dt: float = 0.01) -> tuple:
    """运行主动推断与被动对照两组实验。"""
    integrator = ActiveInferenceIntegrator(dim=dim)

    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 = psi0 / np.linalg.norm(psi0)
    A0 = np.outer(psi0, psi0.conj())

    alpha0 = 1.0  # 初始外部目标为"前进"

    res_active = integrator.evolve(A0, alpha0, t_span, dt, active=True)
    res_passive = integrator.evolve(A0, alpha0, t_span, dt, active=False)

    return res_active, res_passive


def plot_results(res_active: dict, res_passive: dict,
                 save_path: str = 'figs/paperX_active_inference.png'):
    """绘制主动推断与被动对照结果。"""
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # (a) 动作参数 α(t)
    ax = axes[0]
    ax.plot(res_active['t'], res_active['alpha'], lw=2.5, color='#2ca02c',
            label='主动推断 (active)')
    ax.plot(res_passive['t'], res_passive['alpha'], lw=2.5, color='#d62728',
            linestyle='--', label='被动对照 (passive)')
    ax.set_xlabel('物理时间 t')
    ax.set_ylabel('动作参数 alpha(t)')
    ax.set_title('(a) 动作参数演化')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # (b) 预测误差
    ax = axes[1]
    ax.plot(res_active['t'], res_active['error'], lw=2.5, color='#2ca02c',
            label='主动推断')
    ax.plot(res_passive['t'], res_passive['error'], lw=2.5, color='#d62728',
            linestyle='--', label='被动对照')
    ax.set_xlabel('物理时间 t')
    ax.set_ylabel('预测误差 ||rho_desired - A(t)||_HS')
    ax.set_title('(b) 预测误差下降')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # (c) 总代价（误差 + 动作能量惩罚）
    ax = axes[2]
    action_cost_active = 0.5 * (res_active['alpha'] - 0.0) ** 2
    F_active = res_active['error'] + action_cost_active
    F_passive = res_passive['error'] + 0.5 * (res_passive['alpha'] - 0.0) ** 2
    ax.plot(res_active['t'], F_active, lw=2.5, color='#2ca02c', label='主动推断')
    ax.plot(res_passive['t'], F_passive, lw=2.5, color='#d62728', linestyle='--',
            label='被动对照')
    ax.set_xlabel('物理时间 t')
    ax.set_ylabel('总代价 F_total = 误差 + 动作代价')
    ax.set_title('(c) 主动推断总代价更低')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"  图已保存至 {save_path}")
    return fig


def main():
    print("UFPF 主动推断 toy model\n" + "=" * 40)
    res_active, res_passive = run_active_inference_demo(dim=6, t_span=(0.0, 8.0), dt=0.01)

    print("\n=== 终点统计 ===")
    print(f"主动推断：α 终点 = {res_active['alpha'][-1]:.4f}, "
          f"预测误差终点 = {res_active['error'][-1]:.4f}")
    print(f"被动对照：α 终点 = {res_passive['alpha'][-1]:.4f}, "
          f"预测误差终点 = {res_passive['error'][-1]:.4f}")

    plot_results(res_active, res_passive)
    print("\n完成。")
    return res_active, res_passive


if __name__ == '__main__':
    main()
