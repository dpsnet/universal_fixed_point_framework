#!/usr/bin/env python3
"""
UFPF 知觉相变 toy model：双稳态决策的临界慢化
=================================================

把知觉双稳态决策（如 Necker 立方体、运动竞争点）简化为一个序参量 m(t) 的
Landau-Ginzburg 型随机动力学。控制参数 δ 调节知觉 A/B 之间的对称性破缺：

    dm/dt = κ·(δ·m - c·m³) + σ·ξ(t)

- δ = 0：系统处于临界/对称点，m=0 不稳定，两个稳态 m=±√(δ/c)（当 δ>0 时）
  简并；
- δ > 0：A 态占优，系统从 m≈0 弛豫到 m=+√(δ/c)；
- δ < 0：B 态占优，弛豫到 m=-√(|δ|/c)。

测量从 m≈0 附近出发、首次越过决策阈值 |m|>m_th 所需的平均时间 τ(δ)。
在临界点附近，平均场理论预测临界慢化：

    τ(δ) ~ |δ|^{-γ},   γ ≈ 1。

本脚本实现：
  1. 经典 Landau-Ginzburg 模型，提取 γ；
  2. 一个"谱流启发"的非局域修正模型，其中恢复力含状态依赖因子 |m|^{-α}，
     展示非局域性可能改变临界指数 γ；
  3. 一个"谱流-分数阶记忆核"标度代理模型，基于 Caputo 分数阶弛豫的解析
     标度律 τ(δ)=C·δ^{-1/β}，演示 UFPF 第一性原理路线图的预测形式；
  4. 比较三种模型的结果，并讨论如何从 UFPF 严格导出该指数。

参考：
  - notes/04_lorentz_gravity/sensory_integration_time_ruler.md §7.5, §7.6
  - UFPF 临界现象统一框架
"""

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


def classical_relaxation(delta: float, c: float = 1.0, kappa: float = 1.0,
                         sigma: float = 0.05, dt: float = 0.001,
                         threshold: float = 0.6, max_steps: int = 200000,
                         seed: int = None) -> tuple:
    """
    经典 Landau-Ginzburg 的一次轨迹：dm = κ(δm - cm³)dt + σdW。

    返回（决策时间, 最终标签, 最终 m）。
    最终标签：+1 = A（m>0），-1 = B（m<0），0 = 未决策。
    """
    if seed is not None:
        np.random.seed(seed)
    m = sigma * np.random.randn()  # 初始在 0 附近
    for step in range(max_steps):
        dW = np.random.randn() * np.sqrt(dt)
        dm = kappa * (delta * m - c * m ** 3) * dt + sigma * dW
        m += dm
        if abs(m) > threshold:
            return (step + 1) * dt, int(np.sign(m)), m
    return max_steps * dt, 0, m


def measure_classical(deltas: np.ndarray, c: float = 1.0, kappa: float = 1.0,
                      sigma: float = 0.05, n_trials: int = 200, dt: float = 0.001,
                      threshold: float = 0.6, max_steps: int = 200000) -> tuple:
    """对每个 δ 测量经典模型的平均决策时间与选择概率。"""
    taus = []
    tau_stds = []
    P_As = []
    for delta in deltas:
        times = []
        choices = []
        for trial in range(n_trials):
            t, choice, _ = classical_relaxation(delta, c, kappa, sigma, dt,
                                                threshold, max_steps,
                                                seed=None)
            if choice != 0:
                times.append(t)
                choices.append(choice)
        times = np.array(times)
        taus.append(np.mean(times))
        tau_stds.append(np.std(times))
        P_As.append(np.mean(np.array(choices) == 1))
    return np.array(taus), np.array(tau_stds), np.array(P_As)


def spectral_memory_relaxation(delta: float, alpha: float = 0.5, c: float = 1.0,
                               kappa: float = 1.0, sigma: float = 0.05,
                               dt: float = 0.001, threshold: float = 0.6,
                               max_steps: int = 200000, seed: int = None) -> tuple:
    """
    谱流启发的非局域动力学：恢复力含状态依赖因子。

    采用离散近似：
        dm/dt = κ·(δ·m - c·m³)·|m|^{-α} + σ·ξ(t)

    其中 α∈[0,1) 为"谱非局域指数"。当 α→0 时回到经典模型；α>0 时，
    系统在原点附近受到抑制，临界慢化更强。
    """
    if seed is not None:
        np.random.seed(seed)
    m = sigma * np.random.randn()
    for step in range(max_steps):
        dW = np.random.randn() * np.sqrt(dt)
        factor = (max(abs(m), 1e-6)) ** (-alpha)
        dm = kappa * (delta * m - c * m ** 3) * factor * dt + sigma * dW
        m += dm
        if abs(m) > threshold:
            return (step + 1) * dt, int(np.sign(m)), m
    return max_steps * dt, 0, m


def measure_spectral_memory(deltas: np.ndarray, alpha: float = 0.3, c: float = 1.0,
                            kappa: float = 1.0, sigma: float = 0.05,
                            n_trials: int = 200, dt: float = 0.001,
                            threshold: float = 0.6, max_steps: int = 200000) -> tuple:
    """对每个 δ 测量非局域谱流启发模型的平均决策时间与选择概率。"""
    taus = []
    tau_stds = []
    P_As = []
    for delta in deltas:
        times = []
        choices = []
        for trial in range(n_trials):
            t, choice, _ = spectral_memory_relaxation(delta, alpha, c, kappa, sigma,
                                                     dt, threshold, max_steps,
                                                     seed=None)
            if choice != 0:
                times.append(t)
                choices.append(choice)
        times = np.array(times)
        taus.append(np.mean(times))
        tau_stds.append(np.std(times))
        P_As.append(np.mean(np.array(choices) == 1))
    return np.array(taus), np.array(tau_stds), np.array(P_As)


def fractional_scaling_trial(delta: float, beta: float = 0.7, C: float = 5.0,
                             sigma: float = 0.05, seed: int = None) -> tuple:
    """
    Caputo 分数阶 Landau-Ginzburg 弛豫的**标度代理模型**。

    对线性化方程 D^β m = κδm，Mittag-Leffler 解给出弛豫时间满足
        τ(δ) = C · δ^{-1/β}。

    本函数直接按该标度律生成一次"试验"的决策时间，并加入相对噪声 σ。
    它不是逐时间步模拟，而是作为"若 UFPF 谱测度给出幂律记忆，则
    临界指数应为 1/β"的数值占位演示。

    返回（决策时间, 最终标签, 最终 m）。
    """
    if seed is not None:
        np.random.seed(seed)
    tau = C * (delta ** (-1.0 / beta))
    tau *= 1 + sigma * np.random.randn()
    label = +1 if delta > 0 else (-1 if delta < 0 else 0)
    return tau, label, 0.0


def measure_fractional(deltas: np.ndarray, beta: float = 0.7, C: float = 5.0,
                       sigma: float = 0.05, n_trials: int = 200) -> tuple:
    """对每个 δ 测量分数阶标度模型的平均决策时间与选择概率。"""
    taus = []
    tau_stds = []
    P_As = []
    for delta in deltas:
        times = []
        choices = []
        for trial in range(n_trials):
            t, choice, _ = fractional_scaling_trial(delta, beta, C, sigma, seed=None)
            if choice != 0:
                times.append(t)
                choices.append(choice)
        times = np.array(times)
        taus.append(np.mean(times))
        tau_stds.append(np.std(times))
        P_As.append(np.mean(np.array(choices) == 1))
    return np.array(taus), np.array(tau_stds), np.array(P_As)


def deterministic_relaxation_time(delta: float, c: float, kappa: float,
                                 m0: float = 1e-3, dt: float = 0.001,
                                 threshold: float = 0.20,
                                 max_steps: int = 500000) -> float:
    """
    无噪声确定性 Landau-Ginzburg 弛豫时间：dm/dt = κ(δm - cm³)。

    从 m0 出发，测量首次越过 threshold 的时间。理论预测 τ ~ 1/(κδ)。
    """
    m = m0
    for step in range(max_steps):
        dm = kappa * (delta * m - c * m ** 3) * dt
        m += dm
        if abs(m) > threshold:
            return (step + 1) * dt
    return max_steps * dt


def measure_deterministic(deltas: np.ndarray, c: float = 0.25, kappa: float = 1.0,
                          threshold: float = 0.20) -> np.ndarray:
    """对每个 δ 测量确定性弛豫时间。"""
    taus = []
    for delta in deltas:
        t = deterministic_relaxation_time(delta, c, kappa, threshold=threshold)
        taus.append(t)
    return np.array(taus)


def fit_power_law(deltas: np.ndarray, taus: np.ndarray) -> tuple:
    """对 τ(δ)=C·δ^{-γ} 取对数线性拟合。"""
    valid = (~np.isnan(taus)) & (deltas > 0) & (taus > 0)
    x = np.log(deltas[valid])
    y = np.log(taus[valid])
    if len(x) < 2:
        return np.nan, np.nan, valid
    coeffs = np.polyfit(x, y, deg=1)
    gamma = -coeffs[0]
    C = np.exp(coeffs[1])
    return gamma, C, valid


def run_phase_transition_demo() -> dict:
    """运行经典、非局域与分数阶三种模型的临界慢化扫描。"""
    # δ 范围：0.02~0.20，c=0.25 使稳态 m*=2√δ 在 [0.28, 0.89] 之间，阈值 0.20 可达
    deltas = np.linspace(0.02, 0.20, 12)
    threshold = 0.20

    print("经典 Landau-Ginzburg 模型 ...")
    tau_cl, std_cl, P_A_cl = measure_classical(deltas, c=0.25, kappa=1.0, sigma=0.05,
                                               n_trials=200, dt=0.001, threshold=threshold)
    gamma_cl, C_cl, _ = fit_power_law(deltas, tau_cl)
    print(f"  经典模型：γ = {gamma_cl:.4f}, C = {C_cl:.4f}")

    print("谱流启发非局域模型 ...")
    tau_sp, std_sp, P_A_sp = measure_spectral_memory(deltas, alpha=0.3, c=0.25,
                                                      kappa=1.0, sigma=0.05,
                                                      n_trials=200, dt=0.001,
                                                      threshold=threshold)
    gamma_sp, C_sp, _ = fit_power_law(deltas, tau_sp)
    print(f"  非局域模型：γ = {gamma_sp:.4f}, C = {C_sp:.4f}")

    print("谱流-分数阶记忆核标度代理模型（β=0.7，理论 γ=1/β≈1.429）...")
    tau_frac, std_frac, P_A_frac = measure_fractional(deltas, beta=0.7, C=5.0,
                                                      sigma=0.05, n_trials=200)
    gamma_frac, C_frac, _ = fit_power_law(deltas, tau_frac)
    print(f"  分数阶模型：γ = {gamma_frac:.4f}, C = {C_frac:.4f}")

    print("确定性（无噪声）Landau-Ginzburg 弛豫 ...")
    tau_det = measure_deterministic(deltas, c=0.25, kappa=1.0, threshold=threshold)
    gamma_det, C_det, _ = fit_power_law(deltas, tau_det)
    print(f"  确定性模型：γ = {gamma_det:.4f}, C = {C_det:.4f}（理论 γ=1）")

    return {
        'deltas': deltas,
        'tau_classical': tau_cl, 'std_classical': std_cl, 'P_A_classical': P_A_cl,
        'gamma_classical': gamma_cl, 'C_classical': C_cl,
        'tau_spectral': tau_sp, 'std_spectral': std_sp, 'P_A_spectral': P_A_sp,
        'gamma_spectral': gamma_sp, 'C_spectral': C_sp,
        'tau_fractional': tau_frac, 'std_fractional': std_frac, 'P_A_fractional': P_A_frac,
        'gamma_fractional': gamma_frac, 'C_fractional': C_frac,
        'tau_deterministic': tau_det,
        'gamma_deterministic': gamma_det, 'C_deterministic': C_det,
    }


def plot_results(results: dict, save_path: str = 'figs/paperX_perceptual_phase_transition.png'):
    """绘制临界慢化曲线。"""
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    deltas = results['deltas']
    tau_cl = results['tau_classical']
    tau_sp = results['tau_spectral']
    tau_frac = results['tau_fractional']
    tau_det = results['tau_deterministic']
    gamma_cl = results['gamma_classical']
    gamma_sp = results['gamma_spectral']
    gamma_frac = results['gamma_fractional']
    gamma_det = results['gamma_deterministic']
    C_cl = results['C_classical']
    C_sp = results['C_spectral']
    C_frac = results['C_fractional']
    C_det = results['C_deterministic']

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # (a) 线性坐标
    ax = axes[0]
    ax.plot(deltas, tau_det, '^-', color='#2ca02c', lw=2,
            label=f'确定性（理论 γ=1，拟合 γ={gamma_det:.3f})')
    ax.plot(deltas, tau_cl, 'o-', color='#1f77b4', lw=2, label=f'经典随机 γ={gamma_cl:.3f}')
    ax.plot(deltas, tau_sp, 's-', color='#ff7f0e', lw=2, label=f'非局域 γ={gamma_sp:.3f}')
    ax.plot(deltas, tau_frac, 'd-', color='#9467bd', lw=2,
            label=f'分数阶 β=0.7（理论 γ≈1.43，拟合 γ={gamma_frac:.3f})')
    ax.set_xlabel('控制参数 δ')
    ax.set_ylabel('平均决策/弛豫时间 τ')
    ax.set_title('(a) 知觉决策临界慢化 τ(δ)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # (b) 对数坐标拟合
    ax = axes[1]
    valid_det = (~np.isnan(tau_det)) & (tau_det > 0)
    valid_cl = (~np.isnan(tau_cl)) & (tau_cl > 0)
    valid_sp = (~np.isnan(tau_sp)) & (tau_sp > 0)
    valid_frac = (~np.isnan(tau_frac)) & (tau_frac > 0)
    ax.loglog(deltas[valid_det], tau_det[valid_det], '^', color='#2ca02c',
              label=f'确定性 γ={gamma_det:.3f}')
    ax.loglog(deltas[valid_cl], tau_cl[valid_cl], 'o', color='#1f77b4',
              label=f'经典随机 γ={gamma_cl:.3f}')
    ax.loglog(deltas[valid_sp], tau_sp[valid_sp], 's', color='#ff7f0e',
              label=f'非局域 γ={gamma_sp:.3f}')
    ax.loglog(deltas[valid_frac], tau_frac[valid_frac], 'd', color='#9467bd',
              label=f'分数阶 γ={gamma_frac:.3f}')

    delta_fine = np.linspace(deltas.min(), deltas.max(), 200)
    if not (np.isnan(gamma_det) or np.isnan(C_det)):
        ax.loglog(delta_fine, C_det * delta_fine ** (-gamma_det), 'g--', lw=1.5,
                  alpha=0.7)
    if not (np.isnan(gamma_cl) or np.isnan(C_cl)):
        ax.loglog(delta_fine, C_cl * delta_fine ** (-gamma_cl), 'b--', lw=1.5,
                  alpha=0.7)
    if not (np.isnan(gamma_sp) or np.isnan(C_sp)):
        ax.loglog(delta_fine, C_sp * delta_fine ** (-gamma_sp), 'r--', lw=1.5,
                  alpha=0.7)
    if not (np.isnan(gamma_frac) or np.isnan(C_frac)):
        ax.loglog(delta_fine, C_frac * delta_fine ** (-gamma_frac), 'm--', lw=1.5,
                  alpha=0.7)

    ax.set_xlabel('控制参数 δ（对数）')
    ax.set_ylabel('τ（对数）')
    ax.set_title('(b) 对数坐标临界拟合')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"\n  图已保存至 {save_path}")
    return fig


def main():
    print("UFPF 知觉相变 toy model\n" + "=" * 40)
    results = run_phase_transition_demo()
    plot_results(results)
    print("\n完成。")
    return results


if __name__ == '__main__':
    main()
