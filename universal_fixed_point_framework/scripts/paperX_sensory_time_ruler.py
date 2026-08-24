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
# 本文件中 UFPF 相关引用数量：4
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
UFPF 感知时间标尺 toy model：谱流积分器 + 采样率调制
====================================================

将神经系统对力/加速度信号的积分过程建模为有限维谱流方程：

    dA/dt = [G_ext(t), A] + [G_int, A] + κ(t)·(D(A) - A)

其中：
  - A(t) ∈ Hermitian(d)  为神经系统的谱对象（编码感知状态）
  - G_ext(t)             为外部刺激驱动的反 Hermite 谱生成元
  - G_int                为内部记忆/自我模型的固定谱生成元
  - κ(t)                 为采样/测量强度（对应唤醒度、注意力）
  - D(A) = Σ_i P_i A P_i 为固定基下的对角化投影（测量操作，见 paper10 M2）

主观时间标尺：
  (1) 采样计数模型：t_subj = ∫ κ(t) dt
  (2) UFPF 谱熵模型：t_subj = ∫ (dS_B/dt) dt = ΔS_B
      其中 S_B(A) = -Σ p_i log p_i 为 paper7 固定基谱熵

模型(2)给出 §4.3"采样密度 × 信息增量"双因子模型的谱流实现：
  信息增量/次采样  ≈ (dS_B/dt)/κ(t)
  主观时间变化率   = κ(t) × [(dS_B/dt)/κ(t)] = dS_B/dt

参考：
  - paper7 §2.1/§3.1：固定基谱熵 S_B 与熵增定理 ΔS_B ≥ 0
  - paper10 §2.2/§3：测量谱流方程与坍缩时间 τ_collapse = ln(1/ε)/κ
  - notes/04_lorentz_gravity/sensory_integration_time_ruler.md

注意：本脚本为 toy model，用于演示框架内一致性，不声称生物尺度可观测的
      量子/谱修正（ε² ~ 1e-33，见 force 笔记 §9.5）。
"""

import os
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
from typing import Callable, Tuple, Dict

# 中文字体与数学符号渲染（项目惯例）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


class SpectralSensoryIntegrator:
    """
    谱流感官积分器。

    数值积分采用算子分裂 + Hermite 投影：
      1. 幺正步：A'  = expm(dt·G_tot) @ A @ expm(-dt·G_tot)
      2. 测量步：A'' = A' + dt·κ(t)·(D(A') - A')
      3. Hermite 投影：(A + A†)/2
    其中 G_tot = G_ext(t) + G_int。
    """

    def __init__(self, dim: int = 6, seed: int = 42):
        self.dim = dim
        np.random.seed(seed)
        # 固定测量基：标准基
        self.P = [np.outer(np.eye(dim)[:, i], np.eye(dim)[:, i].conj())
                  for i in range(dim)]
        # 内部记忆/自我模型生成元：固定反 Hermite 小扰动
        self.G_int = self._random_antihermitian(dim, scale=0.05)

    @staticmethod
    def _random_antihermitian(dim: int, scale: float = 1.0) -> np.ndarray:
        """生成随机反 Hermite 矩阵。"""
        X = scale * (np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim))
        return (X - X.conj().T) / 2.0

    def diagonal_projection(self, A: np.ndarray) -> np.ndarray:
        """固定基对角化投影 D(A) = Σ_i P_i A P_i。"""
        D = np.zeros_like(A)
        for P in self.P:
            D += P @ A @ P
        return D

    def spectral_entropy(self, A: np.ndarray) -> float:
        """
        固定基谱熵 S_B(A) = -Σ p_i log p_i。

        p_i 取 A 对角元模方归一化，对应 paper7 固定基观测下的信息分布。
        """
        diag = np.diag(A).real
        # 取非负并归一化
        diag = np.abs(diag)
        total = np.sum(diag)
        if total < 1e-15:
            return 0.0
        p = diag / total
        p = p[p > 1e-15]
        return -np.sum(p * np.log(p))

    def step(self,
             A: np.ndarray,
             G_ext: np.ndarray,
             kappa: float,
             dt: float) -> np.ndarray:
        """单步谱流演化。"""
        G_tot = G_ext + self.G_int
        # 幺正步
        U = expm(dt * G_tot)
        A_prime = U @ A @ U.conj().T
        # 测量步
        A_next = A_prime + dt * kappa * (self.diagonal_projection(A_prime) - A_prime)
        # Hermite 投影
        A_next = (A_next + A_next.conj().T) / 2.0
        return A_next

    def evolve(self,
               A0: np.ndarray,
               t_span: Tuple[float, float],
               dt: float,
               G_ext_func: Callable[[float], np.ndarray],
               kappa_func: Callable[[float], float]) -> Dict:
        """
        演化谱流方程并记录物理时间、采样计数、谱熵与主观时间。

        Returns
        -------
        dict with keys:
          t: 物理时间数组
          A: 谱对象序列
          S_B: 固定基谱熵序列
          kappa: 采样强度序列
          N_sample: 累积采样计数 ∫κdt
          t_subj_count: 采样计数模型主观时间
          t_subj_entropy: 谱熵模型主观时间 ΔS_B
        """
        t0, tf = t_span
        n_steps = int(round((tf - t0) / dt))
        t_array = np.linspace(t0, tf, n_steps + 1)

        A = A0.copy()
        t_list, S_list, k_list = [t0], [self.spectral_entropy(A0)], [kappa_func(t0)]
        A_list = [A0.copy()]

        for i in range(n_steps):
            t = t_array[i]
            kappa = kappa_func(t)
            G_ext = G_ext_func(t)
            A = self.step(A, G_ext, kappa, dt)
            t_list.append(t_array[i + 1])
            S_list.append(self.spectral_entropy(A))
            k_list.append(kappa_func(t_array[i + 1]))
            A_list.append(A.copy())

        t_array = np.array(t_list)
        S_array = np.array(S_list)
        k_array = np.array(k_list)

        # 采样计数模型
        N_sample = np.cumsum(k_array) * dt
        # 谱熵模型：主观时间 = ΔS_B(t)
        t_subj_entropy = S_array - S_array[0]

        return {
            't': t_array,
            'A': np.array(A_list),
            'S_B': S_array,
            'kappa': k_array,
            'N_sample': N_sample,
            't_subj_count': N_sample,
            't_subj_entropy': t_subj_entropy,
        }


def make_external_drive(dim: int,
                        base_scale: float = 0.5,
                        novelty_freqs: Tuple[float, ...] = (1.0, 3.7, 7.1),
                        noise_level: float = 0.1) -> Tuple[np.ndarray, Callable[[float], np.ndarray]]:
    """
    构造外部刺激生成元 G_ext(t)。

    可预测刺激：单一低频；新异刺激：多频叠加 + 噪声。
    G_ext(t) = base_scale·[Σ sin(2π f_i t) + noise(t)]·G_base，其中 G_base 为固定反 Hermite 矩阵。
    """
    G_base = SpectralSensoryIntegrator._random_antihermitian(dim, scale=1.0)

    def G_ext_func(t: float) -> np.ndarray:
        signal = 0.0
        for f in novelty_freqs:
            signal += np.sin(2.0 * np.pi * f * t)
        # 加性随机游走噪声（低带宽）
        signal += noise_level * np.sin(2.0 * np.pi * 0.7 * t) * np.cos(2.0 * np.pi * 11.3 * t)
        return base_scale * signal * G_base

    return G_base, G_ext_func


def make_kappa_profile(t: np.ndarray,
                       baseline: float = 1.0,
                       fear_window: Tuple[float, float] = (2.0, 4.0),
                       fear_boost: float = 3.5,
                       flow_window: Tuple[float, float] = (6.0, 8.0),
                       flow_boost: float = 2.0,
                       aging_factor: float = 0.4) -> np.ndarray:
    """
    构造三段式唤醒度/采样率曲线：
      - 恐惧期：高 κ + 高信息输入（新异）
      - 心流期：高 κ + 低信息输入（可预测）
      - 衰老/重复期：低 κ + 低信息输入
    """
    kappa = np.full_like(t, baseline * aging_factor)
    # 恐惧窗口
    mask_fear = (t >= fear_window[0]) & (t <= fear_window[1])
    kappa[mask_fear] = baseline * fear_boost
    # 心流窗口
    mask_flow = (t >= flow_window[0]) & (t <= flow_window[1])
    kappa[mask_flow] = baseline * flow_boost
    # 平滑过渡
    from scipy.ndimage import gaussian_filter1d
    kappa = gaussian_filter1d(kappa, sigma=2.0)
    return kappa


def run_scenarios(dim: int = 6,
                  t_span: Tuple[float, float] = (0.0, 10.0),
                  dt: float = 0.005) -> Dict:
    """
    运行三类场景并返回结果字典。

    场景设置：
      恐惧：高 κ，外部驱动高带宽（novelty_freqs 多 + 噪声）
      心流：高 κ，外部驱动低带宽（单一低频，可预测）
      衰老：低 κ，外部驱动低带宽

    关键设计：三类场景使用相同的物理时间窗口，但采样率 κ(t) 与
    外部驱动带宽不同，从而分离"采样密度"与"信息增量"两个因子。
    """
    integrator = SpectralSensoryIntegrator(dim=dim)

    # 初始态：在测量基下的随机叠加态
    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 = psi0 / np.linalg.norm(psi0)
    A0 = np.outer(psi0, psi0.conj())

    t = np.arange(t_span[0], t_span[1] + dt, dt)

    # 外部驱动构造
    _, G_ext_fear = make_external_drive(dim, base_scale=0.8,
                                        novelty_freqs=(0.8, 2.3, 4.1, 6.7, 9.2),
                                        noise_level=0.4)
    _, G_ext_flow = make_external_drive(dim, base_scale=0.3,
                                        novelty_freqs=(0.5,),
                                        noise_level=0.05)
    _, G_ext_aging = make_external_drive(dim, base_scale=0.25,
                                         novelty_freqs=(0.5,),
                                         noise_level=0.05)

    # 三类场景采样率曲线：恐惧/心流均为高 κ，衰老为低 κ
    kappa_fear = make_kappa_profile(t,
                                    baseline=1.0,
                                    fear_window=(0.0, 10.0),
                                    fear_boost=3.5,
                                    flow_window=(0.0, 0.0),
                                    flow_boost=1.0,
                                    aging_factor=1.0)
    kappa_flow = kappa_fear.copy()
    kappa_aging = make_kappa_profile(t,
                                     baseline=1.0,
                                     fear_window=(0.0, 0.0),
                                     fear_boost=1.0,
                                     flow_window=(0.0, 0.0),
                                     flow_boost=1.0,
                                     aging_factor=0.35)

    def kappa_func_factory(kappa_arr: np.ndarray):
        def kappa_func(t_val: float) -> float:
            idx = int(round((t_val - t_span[0]) / dt))
            idx = max(0, min(idx, len(kappa_arr) - 1))
            return kappa_arr[idx]
        return kappa_func

    res_fear = integrator.evolve(A0, t_span, dt, G_ext_fear, kappa_func_factory(kappa_fear))
    res_flow = integrator.evolve(A0, t_span, dt, G_ext_flow, kappa_func_factory(kappa_flow))
    res_aging = integrator.evolve(A0, t_span, dt, G_ext_aging, kappa_func_factory(kappa_aging))

    return {
        'fear': res_fear,
        'flow': res_flow,
        'aging': res_aging,
    }


def plot_results(results: Dict, save_path: str = 'figs/paperX_sensory_time_ruler.png'):
    """绘制三类场景的主观时间曲线与对比。"""
    # 确保输出目录存在
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    colors = {'fear': '#d62728', 'flow': '#2ca02c', 'aging': '#1f77b4'}
    labels = {'fear': '恐惧/紧急', 'flow': '专注/心流', 'aging': '衰老/重复'}

    # (a) 采样率 κ(t)
    ax = axes[0, 0]
    for key in results:
        ax.plot(results[key]['t'], results[key]['kappa'], color=colors[key], label=labels[key], lw=2)
    ax.set_xlabel('物理时间 $t$')
    ax.set_ylabel('采样强度 $\\kappa(t)$')
    ax.set_title('(a) 唤醒度/采样率曲线')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # (b) 谱熵 S_B(t)
    ax = axes[0, 1]
    for key in results:
        ax.plot(results[key]['t'], results[key]['S_B'], color=colors[key], label=labels[key], lw=2)
    ax.set_xlabel('物理时间 $t$')
    ax.set_ylabel('固定基谱熵 $S_B(t)$')
    ax.set_title('(b) 谱熵累积（paper7 固定基观测）')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # (c) 采样计数模型主观时间
    ax = axes[1, 0]
    for key in results:
        ax.plot(results[key]['t'], results[key]['t_subj_count'],
                color=colors[key], label=labels[key], lw=2)
    ax.plot(results[key]['t'], results[key]['t'], 'k--', alpha=0.5, label='物理时间')
    ax.set_xlabel('物理时间 $t$')
    ax.set_ylabel('主观时间 $t_{\\rm subj}^{(\\kappa)}$')
    ax.set_title('(c) 采样计数模型：主观时间 = $\\int \\kappa dt$')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # (d) 谱熵模型主观时间
    ax = axes[1, 1]
    for key in results:
        ax.plot(results[key]['t'], results[key]['t_subj_entropy'],
                color=colors[key], label=labels[key], lw=2)
    ax.plot(results[key]['t'], results[key]['t'], 'k--', alpha=0.5, label='物理时间')
    ax.set_xlabel('物理时间 $t$')
    ax.set_ylabel('主观时间 $t_{\\rm subj}^{(S)} = \\Delta S_B$')
    ax.set_title('(d) UFPF 谱熵模型：主观时间 = 累积信息增量')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"  图已保存至 {save_path}")
    return fig


def print_summary(results: Dict):
    """打印三类场景的终点统计。"""
    print("\n=== 三类场景终点统计 ===")
    print(f"{'场景':<12} {'物理时间':<10} {'κ-主观时间':<12} {'熵-主观时间':<12} {'ΔS_B 总熵增':<12}")
    for key, label in [('fear', '恐惧/紧急'), ('flow', '专注/心流'), ('aging', '衰老/重复')]:
        res = results[key]
        t_end = res['t'][-1]
        t_k = res['t_subj_count'][-1]
        t_s = res['t_subj_entropy'][-1]
        dS = res['S_B'][-1] - res['S_B'][0]
        print(f"{label:<12} {t_end:<10.2f} {t_k:<12.3f} {t_s:<12.3f} {dS:<12.3f}")


def run_checks():
    """基础自检：熵增、Hermite 保持、测量收敛。"""
    print("\n=== 基础自检 ===")
    dim = 4
    integrator = SpectralSensoryIntegrator(dim=dim)

    # 1. 初始纯态熵应为 0
    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1.0
    A = np.outer(psi, psi.conj())
    S0 = integrator.spectral_entropy(A)
    assert abs(S0) < 1e-12, f"初始纯态熵应为 0，得到 {S0}"
    print(f"  ✓ 初始纯态谱熵 = {S0:.3e}")

    # 2. 测量流下非对角元衰减（κ 大）
    # 构造一个有效的密度矩阵（半正定、迹 1）
    psi_rand = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi_rand = psi_rand / np.linalg.norm(psi_rand)
    A_rand = np.outer(psi_rand, psi_rand.conj())
    # 加入少量非对角相干以观察衰减
    off = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    off = (off + off.conj().T) / 2.0
    np.fill_diagonal(off, 0.0)
    A_rand = A_rand + 0.05 * off
    A_rand = A_rand / np.trace(A_rand)

    zero_G = lambda t: np.zeros((dim, dim), dtype=complex)
    res = integrator.evolve(A_rand, (0.0, 3.0), 0.01, zero_G, lambda t: 10.0)
    off0 = np.linalg.norm(res['A'][0] - np.diag(np.diag(res['A'][0])), 'fro')
    off1 = np.linalg.norm(res['A'][-1] - np.diag(np.diag(res['A'][-1])), 'fro')
    assert off1 < off0, "测量流下非对角范数应衰减"
    print(f"  ✓ 测量流非对角范数 {off0:.3f} -> {off1:.3e}")

    # 3. 谱熵随测量流非减（paper7 定理 3.1 的数值表现）
    dS = res['S_B'][-1] - res['S_B'][0]
    assert dS >= -1e-10, f"固定基谱熵应非减，得到 ΔS = {dS}"
    print(f"  ✓ 固定基谱熵增量 ΔS_B = {dS:.3e} >= 0")


def main():
    print("UFPF 感知时间标尺 toy model\n" + "=" * 40)
    run_checks()
    results = run_scenarios(dim=6, t_span=(0.0, 10.0), dt=0.005)
    print_summary(results)
    fig = plot_results(results)
    print("\n完成。")
    return results, fig


if __name__ == '__main__':
    main()
