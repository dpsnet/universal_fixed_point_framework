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

#!/usr/bin/env python3
"""
Phase 52 — C1: 谱数值计算框架
================================

动态过程谱数值库的基础框架，提供：
  1. 谱算子构造与操作（离散/连续/混合谱）
  2. 稀疏谱矩阵运算与特征值求解
  3. 谱演化方程求解器（ODE/PDE 的谱表示）
  4. 数值精度控制与误差估计
  5. 谱截断与正则化工具

依赖：numpy, scipy.sparse, scipy.integrate
"""

import numpy as np
from typing import Callable, Optional, Union, Tuple, Any, Dict, List
from scipy import sparse as sp
from scipy.sparse import linalg as spla
from scipy import integrate
from dataclasses import dataclass, field


# ============================================================
#  物理常数（Planck 单位制）
# ============================================================

M_PL = 1.0                     # Planck 质量
G_N = 1.0                      # Newton 常数（Planck 单位）
L_PL = 1.0 / M_PL              # Planck 长度


# ============================================================
#  1. 谱数据类型与基础算子
# ============================================================

@dataclass
class SpectralData:
    """谱数据容器"""
    eigenvalues: np.ndarray           # 特征值 λ_i
    eigenvectors: Optional[np.ndarray] = None  # 特征向量（可选）
    weights: Optional[np.ndarray] = None       # 谱权重
    label: str = ""                            # 标签

    @property
    def dim(self) -> int:
        return len(self.eigenvalues)

    @property
    def gap(self) -> float:
        """最小谱间隙"""
        return float(np.min(np.diff(np.sort(self.eigenvalues))))

    @property
    def spectral_range(self) -> Tuple[float, float]:
        """谱范围 (λ_min, λ_max)"""
        return float(np.min(self.eigenvalues)), float(np.max(self.eigenvalues))


class SpectralOperator:
    """
    谱算子基类。
    
    表示作用在 Hilbert 空间上的谱算子 A，其谱分解为：
        A = Σ_i λ_i |e_i⟩⟨e_i|
    
    支持离散谱、连续谱和混合谱。
    """
    
    def __init__(self, 
                 dim: int = 32,
                 spectral_type: str = 'discrete',
                 label: str = ""):
        """
        参数
        ----------
        dim : int
            谱截断维数
        spectral_type : str
            'discrete' | 'continuous' | 'mixed'
        label : str
            算子标签
        """
        self.dim = dim
        self.spectral_type = spectral_type
        self.label = label
        self._data: Optional[SpectralData] = None
        self._matrix: Optional[np.ndarray] = None
    
    def build_spectrum(self) -> SpectralData:
        """构造谱数据（子类实现）"""
        raise NotImplementedError
    
    def get_spectrum(self) -> SpectralData:
        if self._data is None:
            self._data = self.build_spectrum()
        return self._data
    
    def get_matrix(self) -> np.ndarray:
        """获取矩阵表示（离散截断下）"""
        if self._matrix is None:
            data = self.get_spectrum()
            if data.eigenvectors is not None:
                # A = U diag(λ) U^†
                self._matrix = data.eigenvectors @ np.diag(data.eigenvalues) @ data.eigenvectors.conj().T
            else:
                self._matrix = np.diag(data.eigenvalues)
        return self._matrix
    
    def apply(self, vec: np.ndarray) -> np.ndarray:
        """谱算子应用于向量 A|ψ⟩"""
        data = self.get_spectrum()
        if data.eigenvectors is not None:
            return data.eigenvectors @ (data.eigenvalues * (data.eigenvectors.conj().T @ vec))
        else:
            return data.eigenvalues * vec
    
    def trace(self) -> float:
        """迹 Tr(A)"""
        return float(np.sum(self.get_spectrum().eigenvalues))
    
    def det(self) -> float:
        """行列式 det(A)"""
        return float(np.prod(self.get_spectrum().eigenvalues))


# ============================================================
#  2. 谱矩阵运算
# ============================================================

class SpectralMatrix:
    """
    谱矩阵运算封装。
    
    支持：
    - 稀疏/稠密谱矩阵
    - 谱分解与截断
    - 矩阵函数（指数、对数、幂）
    - 迹距离、HS 范数等度量
    """
    
    def __init__(self, matrix: np.ndarray, cutoff: Optional[float] = None):
        """
        参数
        ----------
        matrix : ndarray
            矩阵表示
        cutoff : float, optional
            谱截断（超过 cutoff 的模式被丢弃）
        """
        self._full = np.asarray(matrix, dtype=np.complex128)
        self.cutoff = cutoff
        self._eigendata: Optional[Dict] = None
    
    @property
    def dim(self) -> int:
        return self._full.shape[0]
    
    def _compute_eigensystem(self):
        """计算谱分解"""
        if self._eigendata is None:
            evals, evecs = np.linalg.eigh(self._full)
            if self.cutoff is not None:
                mask = np.abs(evals) < self.cutoff
                evals = evals[mask]
                evecs = evecs[:, mask]
            self._eigendata = {
                'eigenvalues': evals,
                'eigenvectors': evecs,
            }
        return self._eigendata
    
    def eigenvalues(self) -> np.ndarray:
        return self._compute_eigensystem()['eigenvalues']
    
    def eigenvectors(self) -> np.ndarray:
        return self._compute_eigensystem()['eigenvectors']
    
    def truncated(self, dim: int) -> 'SpectralMatrix':
        """截断到 dim 维"""
        data = self._compute_eigensystem()
        evals = data['eigenvalues'][:dim]
        evecs = data['eigenvectors'][:, :dim]
        truncated_mat = evecs @ np.diag(evals) @ evecs.conj().T
        return SpectralMatrix(truncated_mat)
    
    def matrix_function(self, func: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
        """矩阵函数 f(A) = U f(Λ) U^†"""
        data = self._compute_eigensystem()
        return data['eigenvectors'] @ np.diag(func(data['eigenvalues'])) @ data['eigenvectors'].conj().T
    
    def exp(self) -> np.ndarray:
        """矩阵指数 exp(A)"""
        return self.matrix_function(np.exp)
    
    def log(self) -> np.ndarray:
        """矩阵对数 log(A)"""
        return self.matrix_function(np.log)
    
    def power(self, alpha: float) -> np.ndarray:
        """矩阵幂 A^α"""
        return self.matrix_function(lambda x: x ** alpha)
    
    def hs_norm(self) -> float:
        """Hilbert-Schmidt 范数 ||A||_HS = sqrt(Tr(A^† A))"""
        return float(np.sqrt(np.sum(np.abs(self._full) ** 2)))
    
    def trace_distance(self, other: 'SpectralMatrix') -> float:
        """迹距离 (1/2) Tr|A - B|"""
        diff = self._full - other._full
        _, s, _ = np.linalg.svd(diff)
        return 0.5 * float(np.sum(s))
    
    def commutator(self, other: 'SpectralMatrix') -> np.ndarray:
        """对易子 [A, B]"""
        return self._full @ other._full - other._full @ self._full
    
    def commutator_norm(self, other: 'SpectralMatrix') -> float:
        """对易子的 HS 范数 ||[A, B]||_HS"""
        return SpectralMatrix(self.commutator(other)).hs_norm()


# ============================================================
#  3. 谱演化方程求解器
# ============================================================

class SpectralEvolutionSolver:
    """
    谱演化方程求解器。
    
    求解形如 dψ/dt = -i H(t) ψ 或更一般的谱流方程：
        dλ_i/dt = F_i(λ, t)
    
    支持：
    - 固定/自适应步长 ODE 求解
    - 谱流方程（特征值演化）
    - 谱纠缠演化
    """
    
    def __init__(self, 
                 dim: int,
                 method: str = 'RK45',
                 rtol: float = 1e-10,
                 atol: float = 1e-13):
        """
        参数
        ----------
        dim : int
            谱截断维数
        method : str
            求解方法：'rk45' | 'rk23' | 'dop853' | 'fixed_step'
        rtol, atol : float
            相对/绝对容差
        """
        self.dim = dim
        self.method = method
        self.rtol = rtol
        self.atol = atol
        self._history: List[Dict] = []
    
    def _ode_rhs(self, t: float, y: np.ndarray, 
                  ham_func: Callable[[float], np.ndarray]) -> np.ndarray:
        """Schrödinger 方程 RHS: dψ/dt = -i H(t) ψ"""
        H_t = ham_func(t)
        return -1j * H_t @ y
    
    def solve_schrodinger(self, 
                          psi0: np.ndarray,
                          t_span: Tuple[float, float],
                          ham_func: Callable[[float], np.ndarray],
                          n_steps: int = 1000) -> Dict[str, Any]:
        """
        求解 Schrödinger 方程。
        
        参数
        ----------
        psi0 : ndarray
            初始态向量
        t_span : (float, float)
            时间范围
        ham_func : callable(t) -> ndarray
            哈密顿量矩阵函数
        n_steps : int
            输出步数
            
        返回
        -------
        dict : {t, psi, eigenvalues, overlaps}
        """
        t_eval = np.linspace(t_span[0], t_span[1], n_steps)
        
        if self.method != 'fixed_step':
            result = integrate.solve_ivp(
                lambda t, y: self._ode_rhs(t, y, ham_func),
                t_span, psi0,
                method=self.method,
                t_eval=t_eval,
                rtol=self.rtol, atol=self.atol,
            )
        else:
            result = self._fixed_step_solve(psi0, t_span, n_steps, ham_func)
        
        return {
            't': result.t,
            'psi': result.y,
            'success': result.success,
            'message': result.message,
        }
    
    def _fixed_step_solve(self, psi0, t_span, n_steps, ham_func):
        """固定步长 Crank-Nicolson 求解"""
        dt = (t_span[1] - t_span[0]) / n_steps
        t_vals = np.linspace(t_span[0], t_span[1], n_steps + 1)
        psi_vals = np.zeros((self.dim, n_steps + 1), dtype=np.complex128)
        psi_vals[:, 0] = psi0
        
        for i in range(n_steps):
            t_mid = t_vals[i] + 0.5 * dt
            H_mid = ham_func(t_mid)
            # Crank-Nicolson: (I + i dt H/2) ψ_{n+1} = (I - i dt H/2) ψ_n
            A = np.eye(self.dim) + 0.5j * dt * H_mid
            B = np.eye(self.dim) - 0.5j * dt * H_mid
            psi_vals[:, i + 1] = np.linalg.solve(A, B @ psi_vals[:, i])
        
        return type('Result', (), {
            't': t_vals,
            'y': psi_vals,
            'success': True,
            'message': 'fixed step completed',
        })()
    
    def solve_spectral_flow(self,
                            lambda0: np.ndarray,
                            t_span: Tuple[float, float],
                            flow_func: Callable[[float, np.ndarray], np.ndarray],
                            n_steps: int = 1000) -> Dict[str, Any]:
        """
        求解谱流方程 dλ_i/dt = F_i(λ, t)。
        
        参数
        ----------
        lambda0 : ndarray
            初始特征值向量
        t_span : (float, float)
            时间范围
        flow_func : callable(t, lambda) -> ndarray
            流函数 F(λ, t)
        n_steps : int
            输出步数
            
        返回
        -------
        dict : {t, lambda_history, gaps, spectral_range}
        """
        t_eval = np.linspace(t_span[0], t_span[1], n_steps)
        
        result = integrate.solve_ivp(
            lambda t, lam: flow_func(t, lam),
            t_span, lambda0,
            method=self.method,
            t_eval=t_eval,
            rtol=self.rtol, atol=self.atol,
        )
        
        # 计算谱间隙历史
        gaps = np.diff(np.sort(result.y, axis=0), axis=0)
        min_gaps = np.min(np.abs(gaps), axis=0) if gaps.shape[0] > 0 else np.zeros(len(result.t))
        
        return {
            't': result.t,
            'lambda_history': result.y,
            'min_gaps': min_gaps,
            'spectral_range': np.array([np.min(result.y, axis=0), np.max(result.y, axis=0)]),
            'success': result.success,
            'message': result.message,
        }
    
    def compute_spectral_entanglement(self,
                                      psi: np.ndarray,
                                      subsystem_dim: int) -> float:
        """
        计算谱纠缠熵。
        
        S_ent = -Tr(ρ_A log ρ_A) 其中 ρ_A = Tr_B(|ψ⟩⟨ψ|)
        """
        total_dim = len(psi)
        psi_mat = psi.reshape(subsystem_dim, total_dim // subsystem_dim)
        rho_A = psi_mat @ psi_mat.conj().T
        rho_A = rho_A / np.trace(rho_A)
        evals = np.linalg.eigvalsh(rho_A)
        evals = evals[evals > 1e-15]
        return -float(np.sum(evals * np.log(evals)))


# ============================================================
#  4. 谱截断与正则化
# ============================================================

class SpectralCutoff:
    """
    谱截断工具。
    
    基于谱框架的天然 UV/IR 截断机制：
    - UV 截断：谱最大特征值 λ_max ~ M_Pl^2
    - IR 截断：谱最小间隙 Δλ_min
    """
    
    def __init__(self, lambda_min: float = 0.122, lambda_max: float = 1.0):
        """
        参数
        ----------
        lambda_min : float
            最小谱间隙（谱框架基本间隙 Δλ_min = 0.122 M_Pl）
        lambda_max : float
            紫外截断（默认 Planck 标度）
        """
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
    
    def truncate_spectrum(self, eigenvalues: np.ndarray) -> np.ndarray:
        """截断谱：仅保留 [λ_min, λ_max] 内的模式"""
        return eigenvalues[(eigenvalues >= self.lambda_min) & 
                          (eigenvalues <= self.lambda_max)]
    
    def regularize_propagator(self, 
                              k_sq: np.ndarray,
                              mass: float = 0.0) -> np.ndarray:
        """
        谱截断正则化传播子。
        
        G_spec(k) = i / (k² - m² + iε) · θ(λ_max - k²)
        """
        propagator = 1.0j / (k_sq - mass**2 + 1j * self.lambda_min)
        propagator[k_sq > self.lambda_max] = 0.0
        return propagator
    
    def form_factor(self, k_sq: np.ndarray, n: int = 2) -> np.ndarray:
        """
        谱形状因子（UV 压制）。
        
        F(k²) = exp(-(k²/λ_max)^n)
        """
        return np.exp(-(k_sq / self.lambda_max) ** n)


# ============================================================
#  5. 谱精度控制
# ============================================================

@dataclass
class AccuracyReport:
    """精度报告"""
    max_abs_error: float
    max_rel_error: float
    rms_error: float
    n_modes_converged: int
    total_modes: int
    condition_number: float
    
    @property
    def convergence_ratio(self) -> float:
        return self.n_modes_converged / self.total_modes if self.total_modes > 0 else 0.0


class SpectralAccuracy:
    """
    谱数值精度控制。
    
    提供：
    - 截断误差估计（基于谱衰减率）
    - 收敛性诊断
    - 自适应维数选择
    """
    
    def __init__(self, tolerance: float = 1e-10):
        self.tolerance = tolerance
    
    def estimate_truncation_error(self, 
                                   eigenvalues: np.ndarray,
                                   decay_rate: float = 2.0) -> AccuracyReport:
        """
        估计截断误差。
        
        假设谱衰减 ~ k^{-decay_rate}，估计尾部误差。
        """
        n = len(eigenvalues)
        if n < 2:
            return AccuracyReport(0, 0, 0, n, n, 1.0)
        
        sorted_vals = np.sort(np.abs(eigenvalues))
        
        # 条件数
        cond = sorted_vals[-1] / max(sorted_vals[0], 1e-30)
        
        # 尾部衰减拟合
        tail = sorted_vals[-max(1, n // 4):]
        if len(tail) > 1:
            k = np.arange(1, len(tail) + 1)
            coeffs = np.polyfit(np.log(k), np.log(tail), 1)
            fitted_decay = -coeffs[0]
        else:
            fitted_decay = decay_rate
        
        # 截断误差估计
        tail_sum = np.sum(sorted_vals[-max(1, n // 4):])
        total_sum = np.sum(sorted_vals)
        rel_error = tail_sum / total_sum if total_sum > 0 else 0.0
        
        # 收敛模式数（相对误差 < tolerance）
        cumulative = np.cumsum(sorted_vals[::-1])[::-1]
        converged = int(np.sum(cumulative / total_sum > self.tolerance))
        
        return AccuracyReport(
            max_abs_error=tail_sum,
            max_rel_error=rel_error,
            rms_error=rel_error / np.sqrt(n),
            n_modes_converged=min(converged, n),
            total_modes=n,
            condition_number=cond,
        )
    
    def adaptive_dimension(self, 
                           spectrum_func: Callable[[int], np.ndarray],
                           max_dim: int = 256,
                           target_accuracy: float = 1e-8) -> int:
        """
        自适应选择谱截断维数。
        
        逐步增加维数直到截断误差低于目标精度。
        """
        for dim in [8, 16, 32, 64, 128, max_dim]:
            evals = spectrum_func(dim)
            report = self.estimate_truncation_error(evals)
            if report.max_rel_error < target_accuracy:
                return dim
        return max_dim


# ============================================================
#  6. 预定义谱算子
# ============================================================

class HarmonicOscillatorSpectral(SpectralOperator):
    """谐振子谱算子 A_HO = ω (a^† a + 1/2)"""
    
    def __init__(self, omega: float = 1.0, dim: int = 32):
        super().__init__(dim=dim, label=f"HO(ω={omega})")
        self.omega = omega
    
    def build_spectrum(self) -> SpectralData:
        n = np.arange(self.dim, dtype=np.float64)
        eigenvalues = self.omega * (n + 0.5)
        return SpectralData(eigenvalues=eigenvalues, label=self.label)


class KeplerianSpectral(SpectralOperator):
    """Kepler 轨道谱算子（束缚态）"""
    
    def __init__(self, n_max: int = 32, mu: float = 1.0):
        super().__init__(dim=n_max, label=f"Kepler(μ={mu})")
        self.mu = mu
    
    def build_spectrum(self) -> SpectralData:
        n = np.arange(1, self.dim + 1, dtype=np.float64)
        # E_n = -μ / (2n²)
        eigenvalues = -self.mu / (2.0 * n ** 2)
        return SpectralData(eigenvalues=eigenvalues, label=self.label)


class PNHamiltonianSpectral(SpectralOperator):
    """
    后牛顿哈密顿量谱算子。
    
    对双星系统，PN 哈密顿量 H_PN = H_Newton + H_1PN + H_2PN + ...
    在轨道角动量基矢下的谱表示。
    """
    
    def __init__(self, 
                 mass_ratio: float = 1.0,
                 total_mass: float = 1.0,
                 spin1: float = 0.0,
                 spin2: float = 0.0,
                 pn_order: int = 3,
                 dim: int = 32):
        """
        参数
        ----------
        mass_ratio : float
            质量比 q = m₁/m₂ (>= 1)
        total_mass : float
            总质量 M = m₁ + m₂（Planck 单位）
        spin1, spin2 : float
            无量纲自旋参数
        pn_order : int
            PN 阶数 (0=Newton, 1=1PN, ...)
        dim : int
            谱截断维数
        """
        super().__init__(dim=dim, label=f"PN(q={mass_ratio}, order={pn_order})")
        self.mass_ratio = mass_ratio
        self.total_mass = total_mass
        self.spin1 = spin1
        self.spin2 = spin2
        self.pn_order = pn_order
        
        # 约化质量
        q = mass_ratio
        self.mu = q / (1.0 + q) ** 2 * total_mass
        self.nu = self.mu / total_mass  # 对称质量比
    
    def build_spectrum(self) -> SpectralData:
        """构造 PN 哈密顿量的离散谱近似"""
        n = np.arange(1, self.dim + 1, dtype=np.float64)
        
        # Newton 项：E_n = -μ (M π G_N)² / (2 n²) （在 Planck 单位中 G_N = 1）
        E_newton = -self.mu * self.total_mass**2 / (2.0 * n ** 2)
        
        if self.pn_order == 0:
            return SpectralData(eigenvalues=E_newton, label=self.label)
        
        # 1PN 修正：E_1PN ∝ ν E_newton / (c² n²)
        # 在 Planck 单位 c = 1
        E_1pn = E_newton * self.nu * (1.0 / n ** 2)
        
        # 2PN 修正
        E_2pn = E_newton * self.nu ** 2 * (1.0 / n ** 4)
        
        # 3PN 修正（含自旋-轨道耦合）
        spin_correction = 1.0 + 0.5 * (self.spin1 + self.spin2) / n
        E_3pn = E_newton * self.nu ** 3 * (1.0 / n ** 6) * spin_correction
        
        total = E_newton
        if self.pn_order >= 1:
            total += E_1pn
        if self.pn_order >= 2:
            total += E_2pn
        if self.pn_order >= 3:
            total += E_3pn
        
        return SpectralData(eigenvalues=total, label=self.label)


# ============================================================
#  7. 测试与验证
# ============================================================

def test_spectral_operator():
    """验证谱算子基本功能"""
    op = HarmonicOscillatorSpectral(omega=1.0, dim=10)
    data = op.get_spectrum()
    assert len(data.eigenvalues) == 10
    assert abs(data.eigenvalues[0] - 0.5) < 1e-15
    assert abs(data.gap - 1.0) < 1e-15
    
    # 矩阵表示
    mat = op.get_matrix()
    assert mat.shape == (10, 10)
    assert abs(mat[0, 0] - 0.5) < 1e-15
    print("  ✅ SpectralOperator: basic operations pass")


def test_spectral_matrix():
    """验证谱矩阵运算"""
    mat = np.diag(np.array([1.0, 2.0, 3.0]))
    sm = SpectralMatrix(mat)
    
    # 特征值
    evals = sm.eigenvalues()
    assert np.allclose(evals, [1.0, 2.0, 3.0])
    
    # HS 范数
    assert abs(sm.hs_norm() - np.sqrt(1 + 4 + 9)) < 1e-15
    
    # 对易子
    mat2 = np.diag(np.array([3.0, 2.0, 1.0]))
    sm2 = SpectralMatrix(mat2)
    comm_norm = sm.commutator_norm(sm2)
    assert comm_norm < 1e-15  # 对角矩阵对易
    
    print("  ✅ SpectralMatrix: matrix operations pass")


def test_evolution_solver():
    """验证谱演化求解器"""
    dim = 10
    solver = SpectralEvolutionSolver(dim=dim, method='RK45')
    
    # 简单谐振子时间演化
    omega = 1.0
    psi0 = np.zeros(dim, dtype=np.complex128)
    psi0[0] = 1.0  # 基态
    
    def ham_func(t):
        return np.diag(omega * (np.arange(dim) + 0.5))
    
    result = solver.solve_schrodinger(
        psi0, (0.0, 10.0), ham_func, n_steps=100
    )
    
    assert result['success']
    assert len(result['t']) > 50
    print("  ✅ SpectralEvolutionSolver: Schrödinger evolution passes")


def test_spectral_cutoff():
    """验证谱截断工具"""
    cutoff = SpectralCutoff(lambda_min=0.1, lambda_max=10.0)
    
    k_sq = np.array([0.01, 0.1, 1.0, 10.0, 100.0])
    truncated = cutoff.truncate_spectrum(k_sq)
    assert np.all(truncated == np.array([0.1, 1.0, 10.0]))
    
    propagator = cutoff.regularize_propagator(k_sq)
    assert propagator[0] != 0.0  # IR 通过
    assert propagator[-1] == 0.0  # UV 截止
    
    print("  ✅ SpectralCutoff: truncation and regularization pass")


def test_pn_hamiltonian():
    """验证 PN 哈密顿量谱算子"""
    # 等质量双星
    pn = PNHamiltonianSpectral(mass_ratio=1.0, total_mass=1.0, pn_order=3, dim=10)
    data = pn.get_spectrum()
    
    assert len(data.eigenvalues) == 10
    # Newton 项应为负
    assert np.all(data.eigenvalues < 0)
    # 基态（n=1）能量最小
    assert data.eigenvalues[0] < data.eigenvalues[-1]
    
    print(f"  ✅ PNHamiltonianSpectral: PN spectrum computed (E_0={data.eigenvalues[0]:.6f})")


def run_all_tests():
    """运行所有 C1 测试"""
    print("Running C1: Spectral Numerics Framework tests...")
    test_spectral_operator()
    test_spectral_matrix()
    test_evolution_solver()
    test_spectral_cutoff()
    test_pn_hamiltonian()
    print("✅ All C1 tests passed!")


if __name__ == "__main__":
    run_all_tests()
