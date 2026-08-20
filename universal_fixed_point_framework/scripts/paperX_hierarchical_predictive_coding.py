#!/usr/bin/env python3
"""
UFPF 层级预测编码 toy model：自上而下预测与自下而上误差
=========================================================

实现一个极简的两层预测编码网络：
  - L1（感觉层）：接收外部输入 rho_ext，同时被 L2 的预测 rho_pred = A2 牵引
  - L2（预测层/关联层）：根据 L1 的当前状态更新自身，并维持 /ba/ 先验

动力学：
    dA1/dt = [G_ext, A1] + [G_int1, A1] + κ(D(A1)-A1)
             + s_ext·(rho_ext - A1) + s_pred·(A2 - A1)

    dA2/dt = [G_int2, A2] + κ(D(A2)-A2)
             + s_err·(A1 - A2) + s_prior·(rho_ba - A2)

其中：
  - s_ext：外部输入强度（自下而上）
  - s_pred：自上而下预测强度
  - s_err：预测误差驱动 L2 更新的强度
  - s_prior：L2 维持 /ba/ 先验的强度
  - A2 直接作为 L2 对 L1 的预测

场景：模棱两可输入的感知解决
  - 外部输入 rho_ext 是 /ba/ 与 /da/ 的等比例混合（50/50）
  - L2 先验初始偏向 /ba/，并通过 s_prior 维持该先验
  - 当 s_pred >> s_ext 时，系统按先验解释为 /ba/（自上而下主导）
  - 当 s_ext >> s_pred 时，系统按外部输入解释为混合态/不确定（自下而上主导）

参考：
  - Rao & Ballard (1999) Predictive coding in the visual cortex
  - Friston (2005) A free energy principle for the brain
  - notes/04_lorentz_gravity/sensory_integration_time_ruler.md §4.9
"""

import os
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


class HierarchicalPredictiveCoder:
    """两层预测编码谱流积分器。"""

    def __init__(self, dim: int = 8, kappa: float = 0.5, seed: int = 42):
        self.dim = dim
        self.kappa = kappa
        np.random.seed(seed)

        # 各层内部生成元（弱谱流项，让漂移项占主导）
        for name in ['G_int1', 'G_int2', 'G_ext']:
            G = 0.1 * (np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim))
            setattr(self, name, (G - G.conj().T) / 2.0)

        # 固定基投影
        self.P = [np.outer(np.eye(dim)[:, i], np.eye(dim)[:, i])
                  for i in range(dim)]

        # 感知原型：/ba/、/da/，以及 50/50 混合的模糊输入
        rho_ba = np.zeros((dim, dim), dtype=complex)
        rho_ba[0, 0] = 0.95
        rho_ba[1, 1] = 0.05
        rho_ba /= np.trace(rho_ba)
        self.rho_ba = rho_ba

        rho_da = np.zeros((dim, dim), dtype=complex)
        rho_da[4, 4] = 0.90
        rho_da[5, 5] = 0.10
        rho_da /= np.trace(rho_da)
        self.rho_da = rho_da

        self.rho_mixed = 0.5 * rho_ba + 0.5 * rho_da

    def diagonal_projection(self, A: np.ndarray) -> np.ndarray:
        D = np.zeros_like(A)
        for P in self.P:
            D += P @ A @ P
        return D

    def step(self, A1: np.ndarray, A2: np.ndarray, rho_ext: np.ndarray,
             s_ext: float, s_pred: float, s_err: float, s_prior: float, dt: float) -> tuple:
        """单步演化 L1 和 L2。s_prior 为 L2 维持 /ba/ 先验的强度。"""
        # L1: 外部输入 + 自上而下预测
        G_tot1 = self.G_ext + self.G_int1
        U1 = expm(dt * G_tot1)
        A1_prime = U1 @ A1 @ U1.conj().T
        A1_next = (A1_prime
                   + dt * self.kappa * (self.diagonal_projection(A1_prime) - A1_prime)
                   + dt * s_ext * (rho_ext - A1_prime)
                   + dt * s_pred * (A2 - A1_prime))
        A1_next = (A1_next + A1_next.conj().T) / 2.0

        # L2: 自下而上预测误差 + 先验维持
        G_tot2 = self.G_int2
        U2 = expm(dt * G_tot2)
        A2_prime = U2 @ A2 @ U2.conj().T
        A2_next = (A2_prime
                   + dt * self.kappa * (self.diagonal_projection(A2_prime) - A2_prime)
                   + dt * s_err * (A1_next - A2_prime)
                   + dt * s_prior * (self.rho_ba - A2_prime))
        A2_next = (A2_next + A2_next.conj().T) / 2.0

        return A1_next, A2_next

    def evolve(self, A1_0: np.ndarray, A2_0: np.ndarray, rho_ext: np.ndarray,
               s_ext: float, s_pred: float, s_err: float, s_prior: float,
               t_span: tuple, dt: float) -> dict:
        """演化两层网络并返回记录。"""
        t0, tf = t_span
        t_array = np.arange(t0, tf + dt, dt)
        n_steps = len(t_array) - 1

        A1 = A1_0.copy()
        A2 = A2_0.copy()
        records = {'t': [], 'A1': [], 'A2': [], 'err12': [],
                   'fidelity_ba': [], 'fidelity_da': []}
        records['t'].append(t0)
        records['A1'].append(A1.copy())
        records['A2'].append(A2.copy())
        records['err12'].append(np.linalg.norm(A1 - A2, 'fro'))
        records['fidelity_ba'].append(np.real(np.trace(A1.conj().T @ self.rho_ba)))
        records['fidelity_da'].append(np.real(np.trace(A1.conj().T @ self.rho_da)))

        for i in range(n_steps):
            A1, A2 = self.step(A1, A2, rho_ext, s_ext, s_pred, s_err, s_prior, dt)
            records['t'].append(t_array[i + 1])
            records['A1'].append(A1.copy())
            records['A2'].append(A2.copy())
            records['err12'].append(np.linalg.norm(A1 - A2, 'fro'))
            records['fidelity_ba'].append(np.real(np.trace(A1.conj().T @ self.rho_ba)))
            records['fidelity_da'].append(np.real(np.trace(A1.conj().T @ self.rho_da)))

        for key in records:
            records[key] = np.array(records[key])
        return records


def make_initial_states(dim: int = 8) -> tuple:
    """生成 L1 随机初始态，L2 偏向 /ba/ 的先验态。"""
    np.random.seed(123)
    psi1 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi1 = psi1 / np.linalg.norm(psi1)
    A1_0 = np.outer(psi1, psi1.conj())

    # L2 初始为 /ba/ 先验
    rho_ba = np.zeros((dim, dim), dtype=complex)
    rho_ba[0, 0] = 0.95
    rho_ba[1, 1] = 0.05
    rho_ba /= np.trace(rho_ba)
    A2_0 = rho_ba.copy()
    return A1_0, A2_0


def run_hierarchical_demo(dim: int = 8, t_span: tuple = (0.0, 10.0), dt: float = 0.01) -> dict:
    """运行三组对比实验。"""
    coder = HierarchicalPredictiveCoder(dim=dim)
    A1_0, A2_0 = make_initial_states(dim)

    results = {}

    # 场景 A：强自上而下预测，弱外部输入 → L1 被 L2 先验牵引到 /ba/
    results['top_down'] = coder.evolve(A1_0, A2_0, coder.rho_mixed,
                                       s_ext=0.5, s_pred=4.0, s_err=1.0, s_prior=4.0,
                                       t_span=t_span, dt=dt)

    # 场景 B：强自下而上输入，弱预测 → L1 被外部混合态牵引
    results['bottom_up'] = coder.evolve(A1_0, A2_0, coder.rho_mixed,
                                        s_ext=4.0, s_pred=0.5, s_err=2.0, s_prior=4.0,
                                        t_span=t_span, dt=dt)

    # 场景 C：平衡 → L1 在混合态与先验之间折中
    results['balanced'] = coder.evolve(A1_0, A2_0, coder.rho_mixed,
                                       s_ext=2.0, s_pred=2.0, s_err=1.5, s_prior=4.0,
                                       t_span=t_span, dt=dt)

    return results


def plot_results(results: dict,
                 save_path: str = 'figs/paperX_hierarchical_predictive_coding.png'):
    """绘制三层场景结果。"""
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(3, 3, figsize=(14, 12))

    labels = {
        'top_down': 'A: 自上而下主导 (s_pred=4.0, s_ext=0.5)',
        'bottom_up': 'B: 自下而上主导 (s_pred=0.5, s_ext=4.0)',
        'balanced': 'C: 平衡 (s_pred=2.0, s_ext=2.0)'
    }
    colors = {'top_down': '#2ca02c', 'bottom_up': '#1f77b4', 'balanced': '#ff7f0e'}

    for idx, key in enumerate(['top_down', 'bottom_up', 'balanced']):
        res = results[key]

        # (idx, 0) A1 的 /ba/ fidelity
        ax = axes[idx, 0]
        ax.plot(res['t'], res['fidelity_ba'], lw=2.5, color=colors[key],
                label='L1 对 /ba/ 的 fidelity')
        ax.axhline(y=0.95, color='gray', linestyle='--', alpha=0.5, label='/ba 原型=0.95')
        ax.set_xlabel('物理时间 t')
        ax.set_ylabel('fidelity')
        ax.set_title(f"{labels[key]}\n(a) L1 对 /ba/ 的 fidelity")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # (idx, 1) A1 的 /da/ fidelity
        ax = axes[idx, 1]
        ax.plot(res['t'], res['fidelity_da'], lw=2.5, color=colors[key],
                label='L1 对 /da/ 的 fidelity')
        ax.axhline(y=0.90, color='gray', linestyle='--', alpha=0.5, label='/da 原型=0.90')
        ax.set_xlabel('物理时间 t')
        ax.set_ylabel('fidelity')
        ax.set_title('(b) L1 对 /da/ 的 fidelity')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # (idx, 2) 层间预测误差
        ax = axes[idx, 2]
        ax.plot(res['t'], res['err12'], lw=2.5, color=colors[key],
                label='||A1 - A2||_HS')
        ax.set_xlabel('物理时间 t')
        ax.set_ylabel('层间预测误差')
        ax.set_title('(c) L1-L2 预测误差')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"  图已保存至 {save_path}")
    return fig


def print_summary(results: dict):
    """打印终点统计。"""
    print("\n=== 层级预测编码终点统计 ===")
    print(f"{'场景':<20} {'/ba/ fidelity':<12} {'/da/ fidelity':<12} {'L1-L2 误差':<12}")
    for key, label in [('top_down', '自上而下主导'),
                       ('bottom_up', '自下而上主导'),
                       ('balanced', '平衡')]:
        res = results[key]
        print(f"{label:<20} {res['fidelity_ba'][-1]:<12.4f} "
              f"{res['fidelity_da'][-1]:<12.4f} {res['err12'][-1]:<12.4f}")


def main():
    print("UFPF 层级预测编码 toy model\n" + "=" * 40)
    results = run_hierarchical_demo(dim=8, t_span=(0.0, 10.0), dt=0.01)
    print_summary(results)
    plot_results(results)
    print("\n完成。")
    return results


if __name__ == '__main__':
    main()
