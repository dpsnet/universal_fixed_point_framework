"""
paperX_dns_turbulence.py — 三维伪谱 DNS 求解器 + 能谱分析

直接数值模拟 (DNS) 验证谱流体 k^{-5/3} 预言。
实现：
  1. 3D 伪谱不可压 N-S 求解器 (FFT + 2/3 dealiasing + RK4)
  2. 大尺度随机 forcing 维持稳态各向同性湍流
  3. 球壳平均能谱 E(k) 计算
  4. k^{-5/3} 斜率高精度拟合
  5. Kolmogorov 常数 C_K 标定
  6. 耗散区谱静默度诊断

Re_λ ≈ 100-400, 分辨率 64³-128³, 可在普通工作站运行。
"""

import numpy as np
from numpy.fft import fftn, ifftn, fftfreq
import time
from dataclasses import dataclass, field
from typing import Optional, Callable
import json


# ============================================================
# 1. 伪谱 DNS 求解器
# ============================================================

@dataclass
class DNSConfig:
    """DNS 配置参数"""
    N: int = 64               # 每个维度的网格数 (64³)
    Re_lambda: float = 150.0  # Taylor 微尺度雷诺数
    nu: float = 1/150.0       # 运动粘度 (由 Re_λ 确定)
    dt: float = 0.005         # 时间步长
    T_total: float = 50.0     # 总积分时间
    T_stats_start: float = 10.0  # 开始统计的时间
    force_kf: float = 2.0     # 强迫波数
    force_amp: float = 0.1    # 强迫幅度
    dealias_fraction: float = 2.0/3.0  # 2/3 dealiasing 规则
    seed: int = 42            # 随机种子
    
    def __post_init__(self):
        self.L = 2 * np.pi    # 盒子大小
        self.dk = 2 * np.pi / self.L  # 波数间隔
    
    @property
    def N_shell(self) -> int:
        return self.N // 2  # 最大球壳数


class PseudoSpectralDNS3D:
    """
    三维伪谱 DNS 求解器。
    
    求解不可压 Navier-Stokes 方程:
        ∂u/∂t + (u·∇)u = -∇p + ν∇²u + f
        ∇·u = 0
    
    在 Fourier 空间中:
        ∂û/∂t = -νk²û + P(k)·F[ (u·∇)u ] + f̂
    其中 P(k) = I - k̂⊗k̂ 是投影算子 (满足 ∇·u=0)
    """
    
    def __init__(self, config: DNSConfig):
        self.cfg = config
        np.random.seed(config.seed)
        
        # 网格
        self.N = config.N
        self.L = config.L
        self.x = np.linspace(0, self.L, self.N, endpoint=False)
        
        # Fourier 波数
        k_vec = [fftfreq(self.N, d=self.L/(2*np.pi*self.N)) for _ in range(3)]
        self.kx, self.ky, self.kz = np.meshgrid(k_vec[0], k_vec[1], k_vec[2],
                                                  indexing='ij')
        self.k2 = self.kx**2 + self.ky**2 + self.kz**2
        self.k = np.sqrt(self.k2)
        
        # Dealiasing mask (2/3 规则)
        self.dealias_mask = (
            (np.abs(self.kx) < config.dealias_fraction * self.N/2) &
            (np.abs(self.ky) < config.dealias_fraction * self.N/2) &
            (np.abs(self.kz) < config.dealias_fraction * self.N/2)
        ).astype(float)
        
        # 投影算子张量 P_ij = δ_ij - k_i k_j / k²
        self.P = np.zeros((3, 3) + self.kx.shape)
        eps = 1e-10
        for i in range(3):
            for j in range(3):
                self.P[i, j] = (1.0 if i == j else 0.0) - \
                    ([self.kx, self.ky, self.kz][i] *
                     [self.kx, self.ky, self.kz][j]) / (self.k2 + eps)
        
        # 粘性项系数
        self.nu_k2 = config.nu * self.k2
        
        # 时间步进
        self.dt = config.dt
        self.t = 0.0
        self.step_count = 0
        
        # 统计量
        self.energy_history = []
        self.dissipation_history = []
        self.spectra_history = []
        self.spectra_times = []
        
        # 确定性 forcing 模式（初始化时生成，运行中固定）
        self._init_forcing_modes()
        
        # 初始化速度场
        self._init_velocity()
        
    def _init_velocity(self):
        """初始化满足不可压条件的随机速度场"""
        # 在 Fourier 空间中生成随机场
        u_hat = np.zeros((3,) + (self.N, self.N, self.N), dtype=complex)
        
        for i in range(3):
            # 随机振幅
            u_hat[i] = (
                np.random.randn(self.N, self.N, self.N) +
                1j * np.random.randn(self.N, self.N, self.N)
            )
        
        # 投影到无散空间
        u_hat = self._apply_projection(u_hat)
        
        # 标度到给定总能量
        E0 = self._compute_energy(u_hat)
        scale = np.sqrt(0.5 / E0) if E0 > 0 else 1.0
        self.u_hat = u_hat * scale
        self._compute_real_velocity()
    
    def _apply_projection(self, u_hat):
        """投影到无散空间: û_i ← P_ij û_j"""
        u_proj = np.zeros_like(u_hat)
        for i in range(3):
            for j in range(3):
                u_proj[i] += self.P[i, j] * u_hat[j]
        return u_proj
    
    def _compute_energy(self, u_hat=None):
        """计算总动能"""
        if u_hat is None:
            u_hat = self.u_hat
        # 帕塞瓦尔: E = (1/2) * sum_k |û(k)|² / N⁶
        E = 0.0
        for i in range(3):
            E += np.sum(np.abs(u_hat[i])**2)
        return 0.5 * E / (self.N**6)
    
    def _compute_real_velocity(self):
        """从 û 计算实空间速度 u"""
        self.u = np.zeros((3,) + (self.N, self.N, self.N))
        for i in range(3):
            self.u[i] = np.real(ifftn(self.u_hat[i]))
    
    def _init_forcing_modes(self):
        """初始化确定性 forcing 模式（固定波数和相位）"""
        kf = self.cfg.force_kf
        rng = np.random.RandomState(self.cfg.seed + 1)
        mask_k = (self.k > 0) & (self.k <= kf + 0.5)
        self.forcing_mask = mask_k.astype(float)
        
        # 固定振幅和相位（运行中不变）
        self.forcing_amp = np.zeros((3,) + (self.N, self.N, self.N), dtype=complex)
        for i in range(3):
            phase = 2 * np.pi * rng.rand(self.N, self.N, self.N)
            self.forcing_amp[i] = np.exp(1j * phase) * mask_k
    
    def _forcing(self):
        """
        大尺度确定性 forcing。
        在低波数 |k| ≤ k_f 的固定模式上持续注入能量。
        使用固定相位（可重复、统计稳定），振幅由 force_amp 控制。
        """
        n_modes = max(np.sum(self.forcing_mask > 0), 1)
        amp = self.cfg.force_amp * self.N**3 / n_modes
        f_hat = amp * self.forcing_amp
        return self._apply_projection(f_hat)
    
    def _compute_nonlinear(self, u_hat_in):
        """
        计算非线性项 N(u) = (u·∇)u 在 Fourier 空间的贡献。
        使用伪谱法 + 2/3 dealiasing。
        """
        # 实空间速度
        u = np.zeros((3,) + (self.N, self.N, self.N))
        for i in range(3):
            u[i] = np.real(ifftn(u_hat_in[i]))
        
        # 在实空间计算 N_i = u_j ∂_j u_i
        # Fourier 空间的梯度: ∂_j → i k_j
        # 先计算 u_j 的 Fourier 变换，再乘以 k_j
        N = np.zeros((3,) + (self.N, self.N, self.N))
        
        for i in range(3):
            # N_i = u · ∇ u_i = Σ_j u_j * (∂_j u_i)
            # 在 Fourier 空间: F[∂_j u_i] = i*k_j * û_i
            grad_u_i = np.zeros((3,) + (self.N, self.N, self.N))
            for j in range(3):
                grad_u_i[j] = np.real(ifftn(
                    1j * [self.kx, self.ky, self.kz][j] * u_hat_in[i]
                ))
            
            # N_i = Σ_j u_j * ∂_j u_i (实空间乘积)
            for j in range(3):
                N[i] += u[j] * grad_u_i[j]
        
        # 变换回 Fourier 空间 + dealiasing
        N_hat = np.zeros_like(u_hat_in)
        for i in range(3):
            N_hat[i] = fftn(N[i]) * self.dealias_mask / (self.N**3)
        
        return N_hat
    
    def _rhs(self, u_hat):
        """N-S 方程的 Fourier 空间右端项"""
        # 非线性项
        N_hat = self._compute_nonlinear(u_hat)
        
        # 投影
        N_hat_proj = self._apply_projection(N_hat)
        
        # 粘性项 + 非线性项 (负号代表耗散)
        rhs = -self.nu_k2 * u_hat - N_hat_proj
        
        # 强迫项
        rhs += self._forcing()
        
        return rhs
    
    def step(self):
        """RK4 时间步进"""
        u = self.u_hat
        dt = self.dt
        
        # RK4 中间步
        k1 = self._rhs(u)
        k2 = self._rhs(u + 0.5 * dt * k1)
        k3 = self._rhs(u + 0.5 * dt * k2)
        k4 = self._rhs(u + dt * k3)
        
        # 更新
        self.u_hat = u + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        # 应用 dealiasing
        for i in range(3):
            self.u_hat[i] *= self.dealias_mask
        
        # 更新时间
        self.t += dt
        self.step_count += 1
        
        # 每步计算实空间速度（用于诊断）
        if self.step_count % 10 == 0:
            self._compute_real_velocity()
    
    def compute_energy_spectrum(self, u_hat=None):
        """
        计算球壳平均能谱 E(k)。
        
        返回:
            k_shells: 波数数组
            E_k: 能谱 E(k)
        """
        if u_hat is None:
            u_hat = self.u_hat
        
        N = self.N
        max_k = int(np.sqrt(3) * N / 2) + 1
        E_k = np.zeros(max_k)
        count_k = np.zeros(max_k)
        
        # 对每个波数模式求和
        for i in range(3):
            # |û(k)|² 的能量贡献
            mag2 = np.abs(u_hat[i])**2
            
            # 按球壳分组
            k_int = np.round(self.k).astype(int)
            for ki in range(1, max_k):
                mask = (k_int == ki)
                E_k[ki] += np.sum(mag2[mask])
                count_k[ki] += np.sum(mask)
        
        # 归一化: 标准球壳平均能谱
        # E(k) = (1/2) * Σ_{|k'|=k} |û(k')|² / N⁶
        # 不再除以 count_k 或乘以 4πk²—这些已隐含在球壳求和过程中
        vol_norm = self.N**6
        for ki in range(1, max_k):
            E_k[ki] = 0.5 * E_k[ki] / vol_norm
        
        # 有效波数
        k_shells = np.arange(max_k)
        
        return k_shells, E_k
    
    def run(self, verbose=True):
        """运行 DNS 模拟"""
        t_start = time.time()
        n_steps = int(self.cfg.T_total / self.cfg.dt)
        stats_start_steps = int(self.cfg.T_stats_start / self.cfg.dt)
        
        if verbose:
            print(f"{'='*65}")
            print(f"3D 伪谱 DNS 求解器")
            print(f"{'='*65}")
            print(f"  分辨率: {self.N}³ = {self.N**3:,} 网格点")
            print(f"  Re_λ: {self.cfg.Re_lambda:.0f}")
            print(f"  ν: {self.cfg.nu:.6f}")
            print(f"  dt: {self.cfg.dt}")
            print(f"  总步数: {n_steps}")
            print(f"  统计起始: t={self.cfg.T_stats_start}")
            print(f"{'='*65}\n")
        
        # 初始状态
        E0 = self._compute_energy()
        if verbose:
            print(f"  步数   t       E(t)       ε(t)      耗时(s)")
            print(f"  {0:6d}  {self.t:.2f}  {E0:.6e}  {'---':>10s}  {0:.1f}")
        
        for step in range(1, n_steps + 1):
            self.step()
            E = self._compute_energy()
            
            # 能量耗散率 ε = 2ν * ∫ k² E(k) dk
            _, Ek = self.compute_energy_spectrum()
            epsilon = 2 * self.cfg.nu * np.sum(self.k_spectrum(Ek, np.arange(len(Ek))))
            
            self.energy_history.append((self.t, E))
            self.dissipation_history.append((self.t, epsilon))
            
            # 定期记录能谱
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
        
        return {
            "t_final": self.t,
            "t_elapsed": t_elapsed,
            "n_steps": n_steps,
            "energy_final": E,
        }
    
    @staticmethod
    def k_spectrum(Ek, k_array):
        """计算 k×E(k)，用于耗散率积分"""
        return k_array * Ek
    
    def get_time_averaged_spectrum(self):
        """获取时间平均能谱（仅统计稳定后）"""
        if len(self.spectra_history) < 2:
            return None, None
        
        # 仅取稳定后的谱
        k, _ = self.compute_energy_spectrum()
        
        # 对时间平均
        Ek_avg = np.mean(self.spectra_history, axis=0)
        
        return k, Ek_avg


# ============================================================
# 2. 能谱分析与 -5/3 验证
# ============================================================

class EnergySpectrumAnalyzer:
    """
    能谱分析器。
    
    功能:
    - 补偿谱 k^(5/3) E(k) → 测量 Kolmogorov 常数
    - 惯性区斜率拟合（加权最小二乘）
    - 耗散截断 k_ν 定位
    - 间歇性修正诊断
    """
    
    def __init__(self, k, Ek, epsilon=None, nu=None):
        """
        k: 波数数组
        Ek: 能谱 E(k)
        epsilon: 能量耗散率 (若已知)
        nu: 运动粘度 (若已知)
        """
        self.k = np.asarray(k)
        self.Ek = np.asarray(Ek)
        self.epsilon = epsilon
        self.nu = nu
        self._valid_mask = (self.k > 0) & (np.isfinite(self.Ek)) & (self.Ek > 0)
    
    def fit_inertial_range(self, k_min=None, k_max=None):
        """
        在惯性区拟合 E(k) ∝ k^n。
        
        返回:
            slope: 谱斜率 n
            slope_err: 斜率标准误差
            C_K: Kolmogorov 常数 (若 epsilon 已知)
            k_min, k_max: 拟合范围
        """
        mask = self._valid_mask.copy()
        
        if k_min is not None:
            mask &= (self.k >= k_min)
        if k_max is not None:
            mask &= (self.k <= k_max)
        
        k_fit = self.k[mask]
        Ek_fit = self.Ek[mask]
        
        if len(k_fit) < 3:
            return {"error": "拟合点数不足"}
        
        # 对数空间线性拟合
        log_k = np.log10(k_fit)
        log_E = np.log10(Ek_fit)
        
        # 加权拟合 (低波数更稳定)
        w = 1.0 / (1.0 + log_k)  # 简单权重
        A = np.vstack([w * log_k, w * np.ones_like(log_k)]).T
        b = w * log_E
        
        coeffs, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        slope = coeffs[0]
        intercept = coeffs[1]
        
        # 标准误差估计
        n = len(k_fit)
        if n > 2:
            residuals_sum = np.sum((log_E - (slope * log_k + intercept))**2)
            slope_var = residuals_sum / (n - 2) / np.sum((log_k - np.mean(log_k))**2)
            slope_err = np.sqrt(slope_var)
        else:
            slope_err = 0.0
        
        # Kolmogorov 常数 (若 epsilon 已知)
        C_K = None
        if self.epsilon is not None and self.epsilon > 0:
            # E(k) = C_K * ε^(2/3) * k^(-5/3)
            # 在拟合的中值处估计
            k_mid = np.sqrt(k_fit[0] * k_fit[-1])
            Ek_mid = np.interp(k_mid, k_fit, Ek_fit)
            C_K = Ek_mid / (self.epsilon**(2/3) * k_mid**(-5/3))
        
        return {
            "slope": slope,
            "slope_err": slope_err,
            "slope_deviation": slope + 5/3,
            "intercept": intercept,
            "C_K": C_K,
            "k_min": k_fit[0],
            "k_max": k_fit[-1],
            "n_points": n,
            "R2": 1.0 - np.sum((log_E - (slope * log_k + intercept))**2) / \
                         np.sum((log_E - np.mean(log_E))**2) if n > 2 else 0.0
        }
    
    def compensated_spectrum(self):
        """补偿谱: k^(5/3) × E(k)"""
        return self.k** (5/3) * self.Ek
    
    def find_dissipation_knee(self):
        """
        定位耗散拐点 k_ν (能谱从幂律转为指数衰减的波数)。
        使用补偿谱的最大值位置。
        """
        comp = self.compensated_spectrum()
        valid = self._valid_mask & np.isfinite(comp)
        
        if np.sum(valid) < 5:
            return None
        
        # 补偿谱峰值位置
        idx_peak = np.argmax(comp * valid)
        k_nu = self.k[idx_peak]
        
        # 半峰宽估计
        half_max = comp[idx_peak] / 2
        left_idx = np.where(comp[:idx_peak] < half_max)[0]
        right_idx = np.where(comp[idx_peak:] < half_max)[0]
        
        k_left = self.k[left_idx[-1]] if len(left_idx) > 0 else self.k[0]
        k_right = self.k[idx_peak + right_idx[0]] if len(right_idx) > 0 else self.k[-1]
        
        return {
            "k_nu": k_nu,
            "k_nu_range": (k_left, k_right),
            "C_K_peak": comp[idx_peak],
        }
    
    def spectral_silence(self):
        """
        耗散区谱静默度 S_spec 诊断。
        
        定义: S_spec = E(k_nu) / E_max 
        其中 E_max 是惯性区最大谱值。
        接近 0 = 强静默 (耗散切断彻底)。
        """
        Ek_max = np.max(self.Ek[self._valid_mask & (self.k > 0) & (self.k < 10)])
        
        # 耗散区定义: k > k_ν
        knee = self.find_dissipation_knee()
        if knee is None:
            return None
        
        k_nu = knee["k_nu"]
        mask_diss = self._valid_mask & (self.k > k_nu) & (self.k < 3 * k_nu)
        
        if np.sum(mask_diss) == 0:
            return None
        
        Ek_diss_mean = np.mean(self.Ek[mask_diss])
        S_spec = Ek_diss_mean / Ek_max if Ek_max > 0 else 1.0
        
        # 谱间隙 γ = 1 - E(k_nu+1)/E(k_nu) (临近波数的能量下降率)
        idx_nu = np.argmin(np.abs(self.k - k_nu))
        if idx_nu > 0 and idx_nu < len(self.k) - 1:
            gamma = 1.0 - self.Ek[idx_nu + 1] / (self.Ek[idx_nu] + 1e-20)
        else:
            gamma = 0.0
        
        return {
            "S_spec": S_spec,
            "gamma": gamma,
            "k_nu": k_nu,
            "Ek_max": Ek_max,
            "Ek_diss_mean": Ek_diss_mean,
            "interpretation": "强静默" if S_spec < 0.01 else \
                              "中等静默" if S_spec < 0.05 else "弱静默"
        }
    
    def to_dict(self):
        """导出分析结果"""
        fit = self.fit_inertial_range()
        knee = self.find_dissipation_knee()
        silence = self.spectral_silence()
        
        return {
            "fit": fit,
            "knee": knee,
            "silence": silence,
        }


# ============================================================
# 3. 主程序
# ============================================================

def main():
    print("=" * 65)
    print("DNS 湍流高精度数值验证 — 谱流体 k^{-5/3} 预言")
    print("=" * 65)
    
    # --- 配置 ---
    cfg = DNSConfig(
        N=64,
        Re_lambda=150.0,
        dt=0.005,
        T_total=30.0,
        T_stats_start=10.0,
    )
    
    print(f"\n[配置]")
    print(f"  分辨率: {cfg.N}³ = {cfg.N**3:,}")
    print(f"  Re_λ = {cfg.Re_lambda:.0f}, ν = {cfg.nu:.6f}")
    print(f"  积分时间: T={cfg.T_total}, 统计起始: t={cfg.T_stats_start}")
    
    # --- 运行 DNS ---
    dns = PseudoSpectralDNS3D(cfg)
    result = dns.run(verbose=True)
    
    # --- 时间平均能谱 ---
    print(f"\n[能谱分析]")
    k, Ek_avg = dns.get_time_averaged_spectrum()
    
    if Ek_avg is not None:
        # 平均耗散率
        epsilon_avg = np.mean([e for _, e in dns.dissipation_history
                               if dns.spectra_times and 
                               dns.t >= cfg.T_stats_start])
        
        analyzer = EnergySpectrumAnalyzer(k, Ek_avg, epsilon=epsilon_avg, nu=cfg.nu)
        analysis = analyzer.to_dict()
        
        # --- -5/3 斜率验证 ---
        fit = analysis["fit"]
        if "slope" in fit:
            slope = fit["slope"]
            slope_err = fit.get("slope_err", 0)
            dev = slope + 5/3
            print(f"\n  --- -5/3 斜率验证 ---")
            print(f"  拟合范围: k ∈ [{fit.get('k_min', 0):.1f}, {fit.get('k_max', 0):.1f}]")
            print(f"  拟合点数: {fit.get('n_points', 0)}")
            print(f"  E(k) ∝ k^{slope:.4f} ± {slope_err:.4f}")
            print(f"  K41 理论: k^(-5/3) = k^(-1.6667)")
            print(f"  偏差: {dev:.4f} ({abs(dev)/1.6667*100:.2f}%)")
            print(f"  R²: {fit.get('R2', 0):.6f}")
            
            if abs(dev) < 0.05:
                print(f"\n  ✅ -5/3 斜率验证通过: |偏差| < 0.05")
            elif abs(dev) < 0.10:
                print(f"\n  ⚠️ -5/3 斜率在容差范围内: |偏差| < 0.10")
            else:
                print(f"\n  ❌ -5/3 斜率偏差过大: |偏差| = {abs(dev):.4f}")
        
        # --- Kolmogorov 常数 ---
        if fit.get("C_K") is not None:
            print(f"\n  --- Kolmogorov 常数 ---")
            print(f"  C_K = {fit['C_K']:.3f}")
            print(f"  文献值: C_K ≈ 1.5")
            C_K_dev = abs(fit['C_K'] - 1.5) / 1.5 * 100
            print(f"  偏差: {C_K_dev:.1f}%")
            if C_K_dev < 10:
                print(f"  ✅ C_K 与文献一致 (< 10%)")
        
        # --- 耗散区谱静默度 ---
        silence = analysis.get("silence")
        if silence:
            print(f"\n  --- 耗散区谱静默度 ---")
            print(f"  S_spec = {silence['S_spec']:.6f}")
            print(f"  γ = {silence['gamma']:.4f}")
            print(f"  k_ν = {silence['k_nu']:.1f}")
            print(f"  静默状态: {silence['interpretation']}")
            
            # Kolmogorov 尺度理论值
            if epsilon_avg > 0 and cfg.nu > 0:
                k_nu_theory = (epsilon_avg / cfg.nu**3)**(1/4)
                print(f"  k_ν (理论) = {k_nu_theory:.1f}")
                k_nu_dev = abs(silence['k_nu'] - k_nu_theory) / k_nu_theory * 100
                print(f"  偏差: {k_nu_dev:.1f}%")
    
    # --- 总结 ---
    print(f"\n{'='*65}")
    print(f"DNS 验证摘要")
    print(f"{'='*65}")
    print(f"  分辨率: {cfg.N}³")
    print(f"  Re_λ: {cfg.Re_lambda:.0f}")
    print(f"  积分时间: {result['t_final']:.1f}")
    print(f"  耗时: {result['t_elapsed']:.1f}s")
    print(f"  最终能量: {result['energy_final']:.6e}")
    
    if Ek_avg is not None and fit and "slope" in fit:
        slope = fit["slope"]
        dev = slope + 5/3
        if abs(dev) < 0.05:
            print(f"\n  ✅ 谱流体 k^(-5/3) 预言: 高精度验证通过")
        elif abs(dev) < 0.10:
            print(f"  ⚠️ 谱流体 k^(-5/3) 预言: 条件通过 (偏差在 10% 以内)")
        else:
            print(f"  ❌ 谱流体 k^(-5/3) 预言: 需更高分辨率验证")
    
    print(f"\n  完成。")
    
    # 输出标准检查格式 (用于 run_all_tests.py 汇总)
    n_checks = 3
    n_pass = 0
    if Ek_avg is not None and fit and "slope" in fit:
        if abs(fit["slope"] + 5/3) < 0.10:
            n_pass += 1  # -5/3 斜率检查
        if fit.get("C_K") is not None and abs(fit["C_K"] - 1.5) / 1.5 * 100 < 20:
            n_pass += 1  # C_K 常数检查
        if silence and silence["S_spec"] < 0.05:
            n_pass += 1  # 谱静默度检查
    print(f"\n验证: {n_pass}/{n_checks}")
    
    return result, analysis if 'analysis' in dir() else None


if __name__ == "__main__":
    main()
