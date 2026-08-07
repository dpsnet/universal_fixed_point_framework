"""
paperX_dns_turbulence_gpu.py — GPU 加速 3D 伪谱 DNS 求解器 (CuPy)

基于 paperX_dns_turbulence.py 的 GPU 移植版本。
主要修改:
  - numpy → cupy (GPU 数组)
  - numpy.fft → cupyx.scipy.fft (GPU FFT)
  - 添加 CPU-GPU 数据传输管理
  - 利用 GPU 并行加速非线性项和投影算子

性能预期 (RTX 5060):
  N=128: ~15-20x CPU 加速 → ~2-3 小时/轮
  N=256: ~30-50x CPU 加速 → ~8-12 小时/轮
"""

import cupy as cp
import cupyx.scipy.fft as cp_fft
import numpy as np
import time
from dataclasses import dataclass, asdict
from typing import Optional

# ============================================================
# 1. 配置（与 CPU 版共享）
# ============================================================

from paperX_dns_turbulence import DNSConfig, EnergySpectrumAnalyzer


class PseudoSpectralDNS3DGPU:
    """
    GPU 加速的三维伪谱 DNS 求解器。

    与 CPU 版保持 API 兼容，内部使用 CuPy 数组。
    使用 float32 以减少 GPU 显存占用 (N=128: ~1GB, N=256: ~8GB)。
    """

    def __init__(self, config: DNSConfig, dtype=cp.float64):
        self.cfg = config
        self.dtype = dtype
        cp.random.seed(config.seed)

        self.N = config.N
        self.L = config.L

        # GPU 上的波数网格
        k_vec = [cp.fft.fftfreq(self.N, d=self.L/(2*cp.pi*self.N)) for _ in range(3)]
        self.kx, self.ky, self.kz = cp.meshgrid(k_vec[0], k_vec[1], k_vec[2], indexing='ij')
        self.k2 = self.kx**2 + self.ky**2 + self.kz**2
        self.k = cp.sqrt(self.k2)

        # Dealiasing mask
        self.dealias_mask = (
            (cp.abs(self.kx) < config.dealias_fraction * self.N/2) &
            (cp.abs(self.ky) < config.dealias_fraction * self.N/2) &
            (cp.abs(self.kz) < config.dealias_fraction * self.N/2)
        ).astype(dtype)

        # 投影算子 (GPU)
        eps = cp.float64(1e-10)
        self.P = cp.zeros((3, 3) + self.kx.shape, dtype=dtype)
        k_comp = [self.kx, self.ky, self.kz]
        for i in range(3):
            for j in range(3):
                self.P[i, j] = (dtype(1.0) if i == j else dtype(0.0)) - \
                    k_comp[i] * k_comp[j] / (self.k2 + eps)

        # 粘性项
        self.nu_k2 = cp.float64(config.nu) * self.k2

        # 时间参数
        self.dt = config.dt
        self.t = 0.0
        self.step_count = 0

        # 统计 (CPU 端存储)
        self.energy_history = []
        self.dissipation_history = []
        self.spectra_history = []
        self.spectra_times = []

        # 初始化
        self._init_forcing_modes()
        self._init_velocity()

        # GPU stream 用于异步操作
        self.stream = cp.cuda.Stream()

    def _init_forcing_modes(self):
        """初始化 forcing 模式 (GPU)"""
        kf = self.cfg.force_kf
        mask_k = ((self.k > 0) & (self.k <= kf + 0.5)).astype(self.dtype)
        self.forcing_mask = mask_k

        rng = cp.random.RandomState(self.cfg.seed + 1)
        self.forcing_amp = cp.zeros((3,) + (self.N, self.N, self.N), dtype=cp.complex128)
        for i in range(3):
            phase = 2 * cp.pi * rng.rand(self.N, self.N, self.N, dtype=cp.float64)
            self.forcing_amp[i] = cp.exp(1j * phase) * mask_k

    def _randomize_forcing_phases(self):
        """刷新随机相位"""
        for i in range(3):
            phase = 2 * cp.pi * cp.random.rand(self.N, self.N, self.N, dtype=cp.float64)
            self.forcing_amp[i] = cp.exp(1j * phase) * self.forcing_mask

    def _init_velocity(self):
        """初始化速度场 (GPU)"""
        if self.cfg.force_type in ("energy_controlled", "deterministic_controlled"):
            E_target = self.cfg.target_energy
        else:
            L_f = 2 * cp.pi / max(self.cfg.force_kf, 0.5)
            E_target = (self.cfg.force_amp * L_f / 1.5)**(2/3)
        E_target = max(E_target, 0.001)

        u_hat = cp.zeros((3,) + (self.N, self.N, self.N), dtype=cp.complex128)
        for i in range(3):
            u_hat[i] = cp.random.randn(self.N, self.N, self.N, dtype=cp.float64) + \
                       1j * cp.random.randn(self.N, self.N, self.N, dtype=cp.float64)

        u_hat = self._apply_projection(u_hat)
        kf_mask = (self.k < self.cfg.force_kf * 1.5 + 0.5).astype(self.dtype)
        for i in range(3):
            u_hat[i] *= kf_mask

        E0 = self._compute_energy(u_hat)
        scale = cp.sqrt(E_target / max(E0, 1e-20))
        self.u_hat = u_hat * scale

    def _apply_projection(self, u_hat):
        """GPU 投影算子 — 向量化版本"""
        u_proj = cp.zeros_like(u_hat)
        for i in range(3):
            for j in range(3):
                u_proj[i] += self.P[i, j] * u_hat[j]
        return u_proj

    def _compute_energy(self, u_hat=None):
        """GPU 能量计算"""
        if u_hat is None:
            u_hat = self.u_hat
        E = cp.float64(0.0)
        for i in range(3):
            E += cp.sum(cp.abs(u_hat[i])**2)
        return float(0.5 * E / (self.N**6))

    def _forcing(self):
        """GPU 强迫项"""
        n_modes = max(int(cp.sum(self.forcing_mask > 0)), 1)
        E_current = cp.float64(self._compute_energy())

        if self.cfg.force_type == "stochastic":
            self._randomize_forcing_phases()
            amp = cp.float64(self.cfg.force_amp) * self.N**3 / n_modes
        elif self.cfg.force_type == "energy_controlled":
            self._randomize_forcing_phases()
            scale = max(0.0, self.cfg.target_energy - E_current) / max(self.cfg.target_energy, 1e-10)
            amp = cp.float64(self.cfg.force_amp) * cp.float64(scale) * self.N**3 / n_modes
        elif self.cfg.force_type == "deterministic_controlled":
            # 确定性能量控制: 固定相位(产生相干结构) + 能量反馈(防止爆炸)
            # 固定强度用 force_amp, 目标能量用 target_energy
            scale = max(0.0, self.cfg.target_energy - E_current) / max(self.cfg.target_energy, 1e-10)
            amp = cp.float64(self.cfg.force_amp) * cp.float64(scale) * self.N**3 / n_modes
        elif self.cfg.force_type == "energy_injection":
            u_rms = cp.sqrt(2 * max(E_current, 1e-10) / 3)
            u_rms = max(float(u_rms), 0.01)
            amp = cp.float64(self.cfg.force_amp) / cp.float64(u_rms) * self.N**3 / n_modes
            self._randomize_forcing_phases()
        elif self.cfg.force_type == "linear":
            return cp.float64(self.cfg.force_amp) * self.u_hat
        else:  # deterministic
            amp = cp.float64(self.cfg.force_amp) * self.N**3 / n_modes

        f_hat = amp * self.forcing_amp
        return self._apply_projection(f_hat)

    def _compute_nonlinear(self, u_hat_in):
        """GPU 非线性项 — 利用 GPU 并行加速"""
        N_cp = self.N

        # IFFT 到实空间
        u = cp.zeros((3,) + (N_cp, N_cp, N_cp), dtype=cp.float64)
        for i in range(3):
            u[i] = cp.real(cp_fft.ifftn(u_hat_in[i]))

        # 梯度计算 + 实空间乘积 (GPU 向量化)
        N = cp.zeros((3,) + (N_cp, N_cp, N_cp), dtype=cp.float64)
        k_comp = [self.kx, self.ky, self.kz]

        for i in range(3):
            # 向量化: 同时计算所有方向上的梯度
            grad = cp.zeros((3,) + (N_cp, N_cp, N_cp), dtype=cp.float64)
            for j in range(3):
                grad[j] = cp.real(cp_fft.ifftn(1j * k_comp[j] * u_hat_in[i]))

            # N_i = Σ_j u_j * ∂_j u_i (向量化点积)
            for j in range(3):
                N[i] += u[j] * grad[j]

        # FFT 变换回谱空间
        N_hat = cp.zeros_like(u_hat_in)
        for i in range(3):
            N_hat[i] = cp_fft.fftn(N[i]) * self.dealias_mask / (N_cp**3)

        return N_hat

    def _rhs(self, u_hat):
        """GPU RHS"""
        N_hat = self._compute_nonlinear(u_hat)
        N_hat_proj = self._apply_projection(N_hat)
        rhs = -self.nu_k2 * u_hat - N_hat_proj
        rhs += self._forcing()
        return rhs

    def step(self):
        """GPU RK4 步进"""
        u = self.u_hat
        dt = self.dt

        def dealias(v):
            for i in range(3):
                v[i] *= self.dealias_mask
            return v

        k1 = self._rhs(u)
        k2 = self._rhs(dealias(u + 0.5 * dt * k1))
        k3 = self._rhs(dealias(u + 0.5 * dt * k2))
        k4 = self._rhs(dealias(u + dt * k3))

        self.u_hat = u + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        for i in range(3):
            self.u_hat[i] *= self.dealias_mask

        self.t += dt
        self.step_count += 1

    def compute_energy_spectrum(self, u_hat=None):
        """GPU 能谱计算"""
        if u_hat is None:
            u_hat = self.u_hat

        max_k = int(cp.sqrt(3) * self.N / 2) + 1
        E_k = cp.zeros(max_k, dtype=cp.float64)
        k_int = cp.round(self.k).astype(cp.int32)

        for i in range(3):
            mag2 = cp.abs(u_hat[i])**2
            # GPU 上的直方图操作
            for ki in range(1, max_k):
                mask = (k_int == ki)
                E_k[ki] += cp.sum(mag2[mask])

        vol_norm = self.N**6
        for ki in range(1, max_k):
            E_k[ki] = 0.5 * E_k[ki] / vol_norm

        k_shells = cp.arange(max_k)
        return cp.asnumpy(k_shells), cp.asnumpy(E_k)

    def run(self, verbose=True):
        """运行 DNS (GPU 版本)"""
        t_start = time.time()
        n_steps = int(self.cfg.T_total / self.cfg.dt)

        if verbose:
            print(f"{'='*65}")
            print(f"3D 伪谱 DNS 求解器 (GPU)")
            print(f"{'='*65}")
            print(f"  分辨率: {self.N}³ = {self.N**3:,} 网格点")
            print(f"  GPU: {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")
            print(f"  ν: {self.cfg.nu:.6f}, dt: {self.cfg.dt}")
            print(f"  总步数: {n_steps}, 统计起始: t={self.cfg.T_stats_start}")
            print(f"{'='*65}\n")

        E0 = self._compute_energy()
        if verbose:
            print(f"  步数   t       E(t)       ε(t)      耗时(s)")
            print(f"  {0:6d}  {self.t:.2f}  {E0:.6e}  {'---':>10s}  {0:.1f}")

        for step in range(1, n_steps + 1):
            self.step()
            E = self._compute_energy()

            _, Ek = self.compute_energy_spectrum()
            epsilon = 2 * self.cfg.nu * np.sum(np.arange(len(Ek))**2 * Ek)

            self.energy_history.append((self.t, E))
            self.dissipation_history.append((self.t, epsilon))

            if step % 500 == 0 or step == n_steps:
                _, Ek = self.compute_energy_spectrum()
                self.spectra_history.append(Ek.copy())
                self.spectra_times.append(self.t)

            if verbose and (step % 500 == 0 or step == n_steps):
                elapsed = time.time() - t_start
                print(f"  {step:6d}  {self.t:.2f}  {E:.6e}  {epsilon:.6e}  {elapsed:.1f}")

        t_elapsed = time.time() - t_start
        if verbose:
            print(f"\n  完成! 总耗时: {t_elapsed:.1f}s")
        return {"t_final": self.t, "t_elapsed": t_elapsed, "n_steps": n_steps, "energy_final": E}

    def get_time_averaged_spectrum(self):
        """获取时间平均能谱（结果转为 CPU）"""
        if len(self.spectra_history) < 2:
            return None, None
        k, _ = self.compute_energy_spectrum()
        valid_spectra = [Ek for t, Ek in zip(self.spectra_times, self.spectra_history)
                         if t >= self.cfg.T_stats_start]
        if len(valid_spectra) < 1:
            return None, None
        Ek_avg = np.mean(valid_spectra, axis=0)
        return k, Ek_avg


# ============================================================
# 测试
# ============================================================

def test_gpu_vs_cpu():
    """GPU 与 CPU 版本结果对比验证"""
    from paperX_dns_turbulence import PseudoSpectralDNS3D

    cfg = DNSConfig(N=32, Re_lambda=100.0, nu=0.01,
        dt=0.005, T_total=2.0, T_stats_start=1.0,
        force_kf=1.0, force_amp=0.5,
        force_type="energy_controlled", target_energy=0.05, seed=42)

    print("CPU 运行中...")
    dns_cpu = PseudoSpectralDNS3D(cfg)
    cpu_start = time.time()
    dns_cpu.run(verbose=False)
    cpu_time = time.time() - cpu_start
    cpu_E = dns_cpu._compute_energy()
    print(f"  CPU 耗时: {cpu_time:.1f}s, 最终能量: {cpu_E:.6e}")

    print("GPU 运行中...")
    dns_gpu = PseudoSpectralDNS3DGPU(cfg)
    gpu_start = time.time()
    dns_gpu.run(verbose=False)
    gpu_time = time.time() - gpu_start
    gpu_E = dns_gpu._compute_energy()
    print(f"  GPU 耗时: {gpu_time:.1f}s, 最终能量: {gpu_E:.6e}")

    print(f"\n  加速比: {cpu_time/gpu_time:.1f}x")
    print(f"  能量偏差: {abs(cpu_E - gpu_E)/max(cpu_E, 1e-10)*100:.2f}%")
    return cpu_time, gpu_time, cpu_E, gpu_E


if __name__ == "__main__":
    test_gpu_vs_cpu()
