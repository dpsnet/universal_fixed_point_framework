#!/usr/bin/env python3
"""
UFPF 多通道感知竞争 toy model：McGurk 效应、视觉-前庭冲突与通道主导
=====================================================================

在单通道 toy model（paperX_sensory_time_ruler.py）基础上，引入多感觉通道
（视觉 V、前庭 Vb、听觉 A、本体觉 P）的谱流竞争。每个通道 i 用目标态
ρ_i 与强度 s_i(t) 描述；全局神经状态 A(t) 被所有通道共同牵引，并通过
softmax 权重 w_i(t) 实现动态竞争。

模型方程（toy 扩展）：

    dA/dt = [G_int, A]
            + Σ_i w_i(t) · s_i(t) · (ρ_i - A)
            + κ(t) · (D(A) - A)

其中：
  - ρ_i      : 通道 i 的目标谱对象（如 /ba/、/ga/、/da/ 的听觉-视觉原型）
  - s_i(t)   : 通道 i 的刺激强度（0=关闭，1=满强度）
  - w_i(t)   : 基于信息贡献的 softmax 竞争权重
  - κ(t)     : 全局测量强度，保证系统坍缩到确定知觉态
  - D(A)     : 固定基对角化投影（同 paper10 M2）

竞争权重：
    info_i(t) = s_i(t) · ||ρ_i - A(t)||_HS          （与目标态的偏差 = 惊讶度）
    w_i(t)    = exp(β·info_i) / Σ_j exp(β·info_j)

关键场景：
  1. 听觉主导：A 强，V 弱        → A → /ba/
  2. 视觉主导：V 强，A 弱        → A → /ga/
  3. McGurk 融合：A=/ba/ + V=/ga/ → A → /da/（第三融合态）
  4. 视觉-前庭冲突：V=前进，Vb=静止 → 高熵、长时间竞争

参考：
  - paperX_sensory_time_ruler.py（单通道 toy model）
  - paper7 固定基谱熵 S_B 与熵增定理
  - paper10 M2/M4（测量谱流与分支选择）

诚实边界：本脚本为框架内 toy model，目标态 ρ_i 是人工设定的感知原型；
          不对应真实语音/运动神经编码，仅演示"多通道竞争 → 融合/冲突"的
          谱流机制。
"""

import os
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
from typing import Callable, List, Dict, Tuple

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'


class MultiChannelSpectralIntegrator:
    """
    多通道谱流竞争积分器。

    每个通道 i 对应一个目标谱对象 ρ_i（d×d 密度矩阵）和刺激强度函数 s_i(t)。
    全局状态 A(t) 同时受所有通道牵引，并通过 softmax 权重竞争。
    """

    def __init__(self, dim: int = 6, beta: float = 4.0, seed: int = 42):
        self.dim = dim
        self.beta = beta
        np.random.seed(seed)
        # 内部记忆/预测生成元：反 Hermite 小扰动
        G_int = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
        self.G_int = (G_int - G_int.conj().T) / 2.0
        # 固定基投影 P_i
        self.P = [np.outer(np.eye(dim)[:, i], np.eye(dim)[:, i])
                  for i in range(dim)]

    def diagonal_projection(self, A: np.ndarray) -> np.ndarray:
        D = np.zeros_like(A)
        for P in self.P:
            D += P @ A @ P
        return D

    def spectral_entropy(self, A: np.ndarray) -> float:
        diag = np.diag(A).real
        diag = np.abs(diag)
        total = np.sum(diag)
        if total < 1e-15:
            return 0.0
        p = diag / total
        p = p[p > 1e-15]
        return -np.sum(p * np.log(p))

    def channel_weights(self, A: np.ndarray,
                        targets: List[np.ndarray],
                        strengths: List[float]) -> np.ndarray:
        """
        基于各通道与目标态的 HS 偏差计算 softmax 竞争权重。
        偏差越大 = 惊讶度越高 = 权重越大。
        """
        infos = []
        for rho, s in zip(targets, strengths):
            if s > 1e-12:
                diff = rho - A
                infos.append(s * np.linalg.norm(diff, 'fro'))
            else:
                infos.append(0.0)
        infos = np.array(infos)
        # 防止全零导致数值不稳定
        max_info = np.max(infos)
        if max_info < 1e-15:
            return np.ones(len(targets)) / len(targets)
        scaled = self.beta * (infos - max_info)
        exp = np.exp(scaled)
        return exp / (np.sum(exp) + 1e-30)

    def variational_free_energy(self, weights: np.ndarray,
                                infos: np.ndarray) -> float:
        """
        变分自由能：F(w) = -Σ w_i·info_i + (1/β)·Σ w_i·log w_i。

        第一项为负的期望预测误差（最小化 F 等价于最大化加权信息）；
        第二项为熵正则，防止退化到单一通道。
        """
        weights = np.asarray(weights)
        infos = np.asarray(infos)
        # 忽略零权重的熵项
        mask = weights > 1e-15
        entropy_term = 0.0
        if np.any(mask):
            entropy_term = (1.0 / self.beta) * np.sum(weights[mask] * np.log(weights[mask]))
        return -np.sum(weights * infos) + entropy_term

    def step(self, A: np.ndarray,
             targets: List[np.ndarray],
             strengths: List[float],
             kappa: float,
             dt: float) -> Tuple[np.ndarray, np.ndarray]:
        """单步演化，返回 (A_next, weights)。"""
        # 内部幺正演化
        U = expm(dt * self.G_int)
        A_prime = U @ A @ U.conj().T

        # 通道竞争牵引
        w = self.channel_weights(A_prime, targets, strengths)
        drift = np.zeros_like(A_prime)
        for rho, s, wi in zip(targets, strengths, w):
            drift += wi * s * (rho - A_prime)

        # 全局测量/坍缩
        A_next = A_prime + dt * (drift + kappa * (self.diagonal_projection(A_prime) - A_prime))
        A_next = (A_next + A_next.conj().T) / 2.0
        return A_next, w

    def evolve(self,
               A0: np.ndarray,
               t_span: Tuple[float, float],
               dt: float,
               targets: List[np.ndarray],
               strength_funcs: List[Callable[[float], float]],
               kappa_func: Callable[[float], float]) -> Dict:
        """
        多通道谱流演化。

        Parameters
        ----------
        targets : list of d×d 密度矩阵，每个通道的目标态
        strength_funcs : list of func(t)，每个通道的刺激强度
        kappa_func : func(t)，全局采样/测量强度
        """
        t0, tf = t_span
        t_array = np.arange(t0, tf + dt, dt)
        n_steps = len(t_array) - 1

        A = A0.copy()
        records = {
            't': [], 'A': [], 'S_B': [], 'weights': [],
            'kappa': [], 'strengths': []
        }
        records['t'].append(t0)
        records['A'].append(A.copy())
        records['S_B'].append(self.spectral_entropy(A))
        records['weights'].append(self.channel_weights(A, targets, [f(t0) for f in strength_funcs]))
        records['kappa'].append(kappa_func(t0))
        records['strengths'].append([f(t0) for f in strength_funcs])

        for i in range(n_steps):
            t = t_array[i]
            strengths = [f(t) for f in strength_funcs]
            kappa = kappa_func(t)
            A, w = self.step(A, targets, strengths, kappa, dt)
            records['t'].append(t_array[i + 1])
            records['A'].append(A.copy())
            records['S_B'].append(self.spectral_entropy(A))
            records['weights'].append(w)
            records['kappa'].append(kappa_func(t_array[i + 1]))
            records['strengths'].append([f(t_array[i + 1]) for f in strength_funcs])

        for key in records:
            records[key] = np.array(records[key])
        return records


def make_speech_targets(dim: int = 8) -> Dict[str, np.ndarray]:
    """
    构造语音感知原型（人工 target 态）。
    /ba/、/ga/、/da/ 放在尽量正交的低维子空间上，以突出融合与竞争。
    """
    assert dim >= 6, "dim 至少为 6"
    rho_ba = np.zeros((dim, dim), dtype=complex)
    rho_ba[0, 0] = 0.95
    rho_ba[1, 1] = 0.05
    rho_ba /= np.trace(rho_ba)

    rho_ga = np.zeros((dim, dim), dtype=complex)
    rho_ga[4, 4] = 0.92
    rho_ga[5, 5] = 0.08
    rho_ga /= np.trace(rho_ga)

    # /da/ 作为 /ba/ 与 /ga/ 之间的融合态，占据独立的中间维度
    rho_da = np.zeros((dim, dim), dtype=complex)
    rho_da[2, 2] = 0.80
    rho_da[3, 3] = 0.10
    rho_da[6, 6] = 0.10
    rho_da /= np.trace(rho_da)
    return {'ba': rho_ba, 'ga': rho_ga, 'da': rho_da}


def make_motion_targets(dim: int = 6) -> Dict[str, np.ndarray]:
    """
    构造运动感知原型。
    视觉通道："前进"；前庭通道："静止"。
    """
    rho_forward = np.zeros((dim, dim), dtype=complex)
    rho_forward[0, 0] = 0.90
    rho_forward[1, 1] = 0.10
    rho_forward /= np.trace(rho_forward)

    rho_stationary = np.zeros((dim, dim), dtype=complex)
    rho_stationary[3, 3] = 0.90
    rho_stationary[4, 4] = 0.10
    rho_stationary /= np.trace(rho_stationary)
    return {'forward': rho_forward, 'stationary': rho_stationary}


def fidelity(A: np.ndarray, B: np.ndarray) -> float:
    """Hilbert-Schmidt 内积作为 fidelity 代理。"""
    return np.real(np.trace(A.conj().T @ B))


def run_mcgurk_scenario(dim: int = 8, t_span: Tuple[float, float] = (0.0, 6.0), dt: float = 0.01) -> Dict:
    """McGurk 效应：听觉 /ba/ + 视觉 /ga/ → 融合 /da/。"""
    integrator = MultiChannelSpectralIntegrator(dim=dim, beta=4.0)
    targets = make_speech_targets(dim)
    target_list = [targets['ba'], targets['ga'], targets['da']]

    # 听觉 /ba/ 与视觉 /ga/ 同时驱动；/da/ 作为冲突门控的融合通道
    # 当听觉与视觉输入同时存在且强度相近（最大冲突）时，/da/ 通道被激活
    def s_aud(t): return 1.0 if t > 0.5 else 0.0
    def s_vis(t): return 1.0 if t > 0.5 else 0.0
    def s_da(t):
        if t <= 0.5:
            return 0.0
        s_a, s_v = s_aud(t), s_vis(t)
        # 冲突门控：两者同时激活且强度接近时，融合通道最强
        balance = 1.0 - abs(s_a - s_v)
        return 5.0 * s_a * s_v * balance

    def kappa(t): return 2.0

    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 = psi0 / np.linalg.norm(psi0)
    A0 = np.outer(psi0, psi0.conj())

    res = integrator.evolve(A0, t_span, dt, target_list,
                            [s_aud, s_vis, s_da], kappa)

    # 计算终点与三个 target 的 fidelity
    A_end = res['A'][-1]
    fids = {k: fidelity(A_end, targets[k]) for k in targets}
    res['name'] = 'McGurk 融合'
    res['labels'] = ['听觉 /ba/', '视觉 /ga/', '融合 /da/']
    res['fidelity'] = fids
    res['targets'] = targets
    return res


def run_channel_dominance_scenarios(dim: int = 8, t_span: Tuple[float, float] = (0.0, 6.0), dt: float = 0.01) -> Tuple[Dict, Dict]:
    """听觉主导 vs. 视觉主导。"""
    integrator = MultiChannelSpectralIntegrator(dim=dim, beta=4.0)
    targets = make_speech_targets(dim)
    target_list = [targets['ba'], targets['ga']]

    def kappa(t): return 2.0

    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 = psi0 / np.linalg.norm(psi0)
    A0 = np.outer(psi0, psi0.conj())

    # 听觉主导
    def s_aud_strong(t): return 1.0 if t > 0.5 else 0.0
    def s_vis_weak(t): return 0.2 if t > 0.5 else 0.0
    res_aud = integrator.evolve(A0, t_span, dt, target_list,
                                [s_aud_strong, s_vis_weak], kappa)
    res_aud['name'] = '听觉主导（A强/V弱）'
    res_aud['labels'] = ['听觉 /ba/', '视觉 /ga/']
    res_aud['fidelity'] = {k: fidelity(res_aud['A'][-1], targets[k]) for k in ['ba', 'ga']}
    res_aud['targets'] = targets

    # 视觉主导
    def s_aud_weak(t): return 0.2 if t > 0.5 else 0.0
    def s_vis_strong(t): return 1.0 if t > 0.5 else 0.0
    res_vis = integrator.evolve(A0, t_span, dt, target_list,
                                [s_aud_weak, s_vis_strong], kappa)
    res_vis['name'] = '视觉主导（A弱/V强）'
    res_vis['labels'] = ['听觉 /ba/', '视觉 /ga/']
    res_vis['fidelity'] = {k: fidelity(res_vis['A'][-1], targets[k]) for k in ['ba', 'ga']}
    res_vis['targets'] = targets

    return res_aud, res_vis


def run_vis_vestibular_conflict(dim: int = 8, t_span: Tuple[float, float] = (0.0, 8.0), dt: float = 0.01) -> Dict:
    """视觉-前庭冲突：视觉前进 vs. 前庭静止。"""
    integrator = MultiChannelSpectralIntegrator(dim=dim, beta=3.0)
    motion = make_motion_targets(dim)
    target_list = [motion['forward'], motion['stationary']]

    def s_vis(t): return 1.0 if t > 0.5 else 0.0
    def s_vest(t): return 1.0 if t > 0.5 else 0.0
    def kappa(t): return 1.5

    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 = psi0 / np.linalg.norm(psi0)
    A0 = np.outer(psi0, psi0.conj())

    res = integrator.evolve(A0, t_span, dt, target_list,
                            [s_vis, s_vest], kappa)
    res['name'] = '视觉-前庭冲突'
    res['labels'] = ['视觉 前进', '前庭 静止']
    res['fidelity'] = {k: fidelity(res['A'][-1], motion[k]) for k in motion}
    res['targets'] = motion
    return res


def plot_multi_channel_results(results: List[Dict],
                               save_path: str = 'figs/paperX_multichannel_sensory_time_ruler.png'):
    """绘制多通道竞争结果。"""
    out_dir = os.path.dirname(save_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    n = len(results)
    fig, axes = plt.subplots(n, 3, figsize=(14, 4 * n))
    if n == 1:
        axes = axes.reshape(1, -1)

    for idx, res in enumerate(results):
        t = res['t']
        weights = res['weights']
        S_B = res['S_B']
        strengths = res['strengths']
        labels = res['labels']
        name = res['name']

        # (a) 通道强度
        ax = axes[idx, 0]
        for i, lab in enumerate(labels):
            ax.plot(t, strengths[:, i], label=lab, lw=2)
        ax.set_xlabel('物理时间 $t$')
        ax.set_ylabel('通道刺激强度 $s_i(t)$')
        ax.set_title(f'{name}\n(a) 通道输入强度')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # (b) 竞争权重
        ax = axes[idx, 1]
        for i, lab in enumerate(labels):
            ax.plot(t, weights[:, i], label=lab, lw=2)
        ax.set_xlabel('物理时间 $t$')
        ax.set_ylabel('竞争权重 $w_i(t)$')
        ax.set_title(f'(b) 动态竞争权重')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # (c) 谱熵与主观时间
        ax = axes[idx, 2]
        t_subj = S_B - S_B[0]
        ax.plot(t, S_B, label='$S_{\\mathcal{B}}(t)$', lw=2)
        ax.plot(t, t_subj, label='$t_{\\rm subj}^{(S)}=\\Delta S_{\\mathcal{B}}$', lw=2)
        ax.set_xlabel('物理时间 $t$')
        ax.set_ylabel('谱熵 / 主观时间')
        ax.set_title(f'(c) 谱熵与主观时间')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"  图已保存至 {save_path}")
    return fig


def print_summary(results: List[Dict]):
    print("\n=== 多通道场景终点 fidelity 摘要 ===")
    for res in results:
        print(f"\n{res['name']}:")
        for k, v in res['fidelity'].items():
            print(f"  与 target [{k}] 的 fidelity = {v:.4f}")


def run_checks():
    print("\n=== 多通道模型基础自检 ===")
    dim = 4
    integrator = MultiChannelSpectralIntegrator(dim=dim, beta=4.0)

    # 1. 单通道主导应收敛到对应目标
    rho1 = np.zeros((dim, dim), dtype=complex)
    rho1[0, 0] = 1.0
    rho2 = np.zeros((dim, dim), dtype=complex)
    rho2[1, 1] = 1.0

    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 = psi0 / np.linalg.norm(psi0)
    A0 = np.outer(psi0, psi0.conj())

    def kappa(t): return 2.0
    res1 = integrator.evolve(A0, (0.0, 5.0), 0.01, [rho1, rho2],
                             [lambda t: 1.0, lambda t: 0.0], kappa)
    f1 = fidelity(res1['A'][-1], rho1)
    f2 = fidelity(res1['A'][-1], rho2)
    assert f1 > f2, "单通道1主导时应更接近 target1"
    print(f"  ✓ 通道1主导：fidelity target1={f1:.4f} > target2={f2:.4f}")

    # 2. 权重和为 1
    w_sum = np.sum(res1['weights'][-1])
    assert abs(w_sum - 1.0) < 1e-12, "softmax 权重和应为 1"
    print(f"  ✓ 权重和 = {w_sum:.6f}")

    # 3. 谱熵非减
    dS = res1['S_B'][-1] - res1['S_B'][0]
    assert dS >= -1e-10, f"谱熵应非减，得到 ΔS={dS}"
    print(f"  ✓ 谱熵增量 ΔS_B = {dS:.3e}")

    # 4. softmax 权重最小化变分自由能
    A_mid = res1['A'][len(res1['A']) // 2]
    infos = []
    for rho, s in zip([rho1, rho2], [1.0, 0.0]):
        infos.append(s * np.linalg.norm(rho - A_mid, 'fro'))
    infos = np.array(infos)
    w_soft = integrator.channel_weights(A_mid, [rho1, rho2], [1.0, 0.0])
    F_soft = integrator.variational_free_energy(w_soft, infos)
    # 与均匀权重、随机权重比较
    w_uniform = np.ones(2) / 2.0
    F_uniform = integrator.variational_free_energy(w_uniform, infos)
    w_random = np.array([0.8, 0.2])
    F_random = integrator.variational_free_energy(w_random, infos)
    assert F_soft < F_uniform and F_soft < F_random, "softmax 权重应最小化变分自由能"
    print(f"  ✓ 变分自由能：softmax={F_soft:.4f} < uniform={F_uniform:.4f} < random={F_random:.4f}")


def main():
    print("UFPF 多通道感知竞争 toy model\n" + "=" * 40)
    run_checks()

    res_mcgurk = run_mcgurk_scenario()
    res_aud, res_vis = run_channel_dominance_scenarios()
    res_conflict = run_vis_vestibular_conflict()

    results = [res_aud, res_vis, res_mcgurk, res_conflict]
    print_summary(results)
    plot_multi_channel_results(results)
    print("\n完成。")
    return results


if __name__ == '__main__':
    main()
