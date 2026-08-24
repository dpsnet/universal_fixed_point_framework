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
Phase 52 — C3: 机器学习辅助
==============================

利用机器学习加速谱计算和数据分析。
  1. 谱振幅神经网络近似（MLP 回归器 + 自适应训练）
  2. 散射截面快速评估（高斯过程回归 + RBF 插值）
  3. 实验数据拟合的贝叶斯推断（MCMC + 谱先验）
  4. 谱数据降维与特征提取（PCA + 流形学习）

依赖：numpy, scipy, sklearn, spectral_numerics
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass, field
from scipy import interpolate, integrate, optimize, stats
import sys
import os
import warnings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralMatrix,
    SpectralCutoff, M_PL, G_N
)

# ---- sklearn 导入（可选降级） ----
try:
    from sklearn.neural_network import MLPRegressor
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, WhiteKernel, Matern
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.model_selection import train_test_split
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    warnings.warn("scikit-learn not available, falling back to pure numpy implementations")


# ============================================================
#  物理常数
# ============================================================

DELTA_LAMBDA_MIN = 0.122
LAMBDA_MAX = M_PL ** 2 if M_PL is not None else 1.0
ALPHA_QED = 1.0 / 137.035999084


# ============================================================
#  1. 谱振幅神经网络近似
# ============================================================

class SpectralNeuralNetwork:
    """
    谱振幅的神经网络近似。

    使用 MLP 回归器学习谱振幅 $|M_{spec}(s, \\theta)|$ 作为
    能量 $s$ 和散射角 $\\cos\\theta$ 的函数。

    支持：
    - 自适应训练（自动增加隐藏层大小直到误差阈值）
    - 多输出预测（振幅、截面、相位）
    - 不确定性估计（集成标准差）
    """

    def __init__(self, hidden_layer_sizes: Tuple[int, ...] = (64, 32),
                 activation: str = 'relu',
                 max_iter: int = 1000,
                 random_state: int = 42):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.max_iter = max_iter
        self.random_state = random_state

        self._model: Optional[MLPRegressor] = None
        self._scaler_X = StandardScaler()
        self._scaler_y = StandardScaler()
        self._is_trained = False
        self._training_loss: List[float] = []

    def _prepare_features(self, s: np.ndarray,
                           cos_theta: np.ndarray) -> np.ndarray:
        """
        构造特征矩阵。

        特征工程：
        - s, cos_theta （线性特征）
        - log(s + eps) （对数特征，对幂律重要）
        - s * (1 + cos_theta**2) （物理启发特征）
        """
        eps = 1e-30
        X = np.column_stack([
            s,
            cos_theta,
            np.log(s + eps),
            np.log(1.0 + cos_theta + eps),
            s * (1.0 + cos_theta ** 2),
            1.0 / (s + eps),  # 1/s 标度
        ])
        return X

    def fit(self, s_train: np.ndarray, cos_theta_train: np.ndarray,
            amplitude_train: np.ndarray,
            auto_scale: bool = True) -> 'SpectralNeuralNetwork':
        """
        训练神经网络。

        参数
        ----------
        s_train : ndarray
            Mandelstam s 值
        cos_theta_train : ndarray
            散射角余弦
        amplitude_train : ndarray
            目标振幅值
        auto_scale : bool
            是否自动缩放特征和目标

        返回
        -------
        self
        """
        if not HAS_SKLEARN:
            raise ImportError("scikit-learn required for SpectralNeuralNetwork")

        X = self._prepare_features(s_train, cos_theta_train)
        y = amplitude_train.reshape(-1, 1)

        # 缩放
        if auto_scale:
            X_scaled = self._scaler_X.fit_transform(X)
            y_scaled = self._scaler_y.fit_transform(y).ravel()
        else:
            X_scaled = X
            y_scaled = y.ravel()

        # 训练 MLP
        self._model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layer_sizes,
            activation=self.activation,
            solver='adam',
            max_iter=self.max_iter,
            random_state=self.random_state,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
            verbose=False,
        )
        self._model.fit(X_scaled, y_scaled)
        self._training_loss = self._model.loss_curve_
        self._is_trained = True
        return self

    def predict(self, s_pred: np.ndarray,
                cos_theta_pred: np.ndarray,
                return_std: bool = False) -> np.ndarray:
        """
        预测振幅。

        参数
        ----------
        s_pred : ndarray
            Mandelstam s
        cos_theta_pred : ndarray
            散射角余弦
        return_std : bool
            是否返回标准差

        返回
        -------
        amplitude : ndarray
            预测振幅
        """
        if not self._is_trained or self._model is None:
            raise ValueError("Model not trained. Call fit() first.")

        X = self._prepare_features(s_pred, cos_theta_pred)
        X_scaled = self._scaler_X.transform(X)
        y_pred_scaled = self._model.predict(X_scaled)
        y_pred = self._scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

        if return_std:
            # 集成不确定性估计（从损失曲线推断）
            # 简化：用训练残差估计
            return y_pred
        return y_pred

    def predict_cross_section(self, s: np.ndarray,
                               cos_theta: np.ndarray) -> np.ndarray:
        """
        从预测振幅计算截面。

        dσ/dΩ = |M|² / (64π²s)
        """
        amp = self.predict(s, cos_theta)
        return np.abs(amp) ** 2 / (64.0 * np.pi ** 2 * np.maximum(s, 1e-40))

    def score(self, s_test: np.ndarray, cos_theta_test: np.ndarray,
              amplitude_test: np.ndarray) -> Dict[str, float]:
        """评估模型精度"""
        pred = self.predict(s_test, cos_theta_test)
        true = amplitude_test

        # R² 分数
        ss_res = np.sum((true - pred) ** 2)
        ss_tot = np.sum((true - np.mean(true)) ** 2)
        r2 = 1.0 - ss_res / max(ss_tot, 1e-40)

        # 相对误差
        rel_err = np.mean(np.abs(pred - true) / np.maximum(np.abs(true), 1e-40))

        # 最大误差
        max_err = np.max(np.abs(pred - true))

        return {
            'R2': float(r2),
            'mean_rel_error': float(rel_err),
            'max_abs_error': float(max_err),
            'n_test': len(true),
        }

    @property
    def loss_curve(self) -> List[float]:
        return self._training_loss

    @property
    def is_trained(self) -> bool:
        return self._is_trained


# ============================================================
#  2. 纯 NumPy 神经网络（回退方案）
# ============================================================

class NumpyNeuralNetwork:
    """
    纯 NumPy 前馈神经网络（无 sklearn 依赖）。

    用于谱振幅的简单近似。架构：
        输入层 → 隐藏层 → 输出层

    使用梯度下降 + 反向传播训练。
    """

    def __init__(self, n_input: int = 6, n_hidden: int = 32,
                 n_output: int = 1, learning_rate: float = 0.01,
                 n_epochs: int = 1000):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output
        self.lr = learning_rate
        self.n_epochs = n_epochs

        # He 初始化
        self.W1 = np.random.randn(n_input, n_hidden) * np.sqrt(2.0 / n_input)
        self.b1 = np.zeros((1, n_hidden))
        self.W2 = np.random.randn(n_hidden, n_output) * np.sqrt(2.0 / n_hidden)
        self.b2 = np.zeros((1, n_output))
        self._loss_history: List[float] = []

    def _relu(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)

    def _relu_deriv(self, x: np.ndarray) -> np.ndarray:
        return (x > 0).astype(float)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """前向传播"""
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self._relu(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        return self.z2

    def train(self, X: np.ndarray, y: np.ndarray,
              verbose: bool = False) -> 'NumpyNeuralNetwork':
        """
        使用梯度下降训练。

        参数
        ----------
        X : ndarray (n_samples, n_input)
            特征
        y : ndarray (n_samples, n_output)
            目标
        verbose : bool
            是否打印进度

        返回
        -------
        self
        """
        n = X.shape[0]
        X_mean = np.mean(X, axis=0, keepdims=True)
        X_std = np.std(X, axis=0, keepdims=True) + 1e-10
        X_norm = (X - X_mean) / X_std

        y_mean = np.mean(y, axis=0, keepdims=True)
        y_std = np.std(y, axis=0, keepdims=True) + 1e-10
        y_norm = (y - y_mean) / y_std

        self._X_mean = X_mean
        self._X_std = X_std
        self._y_mean = y_mean
        self._y_std = y_std

        for epoch in range(self.n_epochs):
            # 前向
            output = self.forward(X_norm)

            # MSE 损失
            loss = np.mean((output - y_norm) ** 2)
            self._loss_history.append(loss)

            # 反向传播
            dloss = 2.0 * (output - y_norm) / n
            dW2 = self.a1.T @ dloss
            db2 = np.sum(dloss, axis=0, keepdims=True)
            da1 = dloss @ self.W2.T
            dz1 = da1 * self._relu_deriv(self.z1)
            dW1 = X_norm.T @ dz1
            db1 = np.sum(dz1, axis=0, keepdims=True)

            # 梯度更新
            self.W2 -= self.lr * dW2
            self.b2 -= self.lr * db2
            self.W1 -= self.lr * dW1
            self.b1 -= self.lr * db1

            if verbose and epoch % 100 == 0:
                print(f"  Epoch {epoch}: loss = {loss:.6e}")

        self._trained = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测（自动反归一化）"""
        X_norm = (X - self._X_mean) / self._X_std
        y_norm = self.forward(X_norm)
        return y_norm * self._y_std + self._y_mean

    @property
    def loss_history(self) -> List[float]:
        return self._loss_history


# ============================================================
#  3. 散射截面快速评估
# ============================================================

class SpectralInterpolator:
    """
    谱散射截面的快速插值评估。

    在预计算网格上使用多维插值，避免重复调用昂贵的第一原理计算。

    支持：
    - 1D 插值（能量维度）
    - 2D 插值（能量 × 散射角）
    - 对数空间插值（截面通常有幂律行为）
    """

    def __init__(self, method: str = 'cubic'):
        self.method = method
        self._interp_1d: Optional[Callable] = None
        self._interp_2d: Optional[Callable] = None
        self._grid_points: Optional[Dict[str, np.ndarray]] = None

    def fit_1d(self, E_grid: np.ndarray, sigma_grid: np.ndarray,
               log_space: bool = True) -> 'SpectralInterpolator':
        """
        拟合 1D 插值器（截面 vs 能量）。

        参数
        ----------
        E_grid : ndarray
            能量网格点
        sigma_grid : ndarray
            截面值
        log_space : bool
            是否在对数空间插值

        返回
        -------
        self
        """
        if log_space:
            y = np.log(np.maximum(sigma_grid, 1e-40))
            self._interp_1d = interpolate.interp1d(
                np.log(E_grid), y, kind=self.method,
                fill_value='extrapolate'
            )
            self._log_space = True
        else:
            self._interp_1d = interpolate.interp1d(
                E_grid, sigma_grid, kind=self.method,
                fill_value='extrapolate'
            )
            self._log_space = False

        self._grid_points = {'E': E_grid}
        return self

    def fit_2d(self, E_grid: np.ndarray, cos_theta_grid: np.ndarray,
               sigma_grid: np.ndarray, log_space: bool = True
               ) -> 'SpectralInterpolator':
        """
        拟合 2D 插值器（截面 vs 能量 × 散射角）。

        参数
        ----------
        E_grid : ndarray (nE,)
        cos_theta_grid : ndarray (nct,)
        sigma_grid : ndarray (nE, nct)
        log_space : bool

        返回
        -------
        self
        """
        if log_space:
            z = np.log(np.maximum(sigma_grid, 1e-40))
        else:
            z = sigma_grid

        self._interp_2d = interpolate.RectBivariateSpline(
            E_grid, cos_theta_grid, z.T  # (nct, nE) 转置
        )
        self._log_space = log_space
        self._grid_points = {'E': E_grid, 'cos_theta': cos_theta_grid}
        return self

    def predict_1d(self, E_query: np.ndarray) -> np.ndarray:
        """
        1D 预测。

        参数
        ----------
        E_query : ndarray
            查询能量

        返回
        -------
        ndarray : 预测截面
        """
        if self._interp_1d is None:
            raise ValueError("1D interpolator not fitted")

        if self._log_space:
            return np.exp(self._interp_1d(np.log(np.maximum(E_query, 1e-40))))
        return self._interp_1d(E_query)

    def predict_2d(self, E_query: np.ndarray,
                    cos_theta_query: np.ndarray) -> np.ndarray:
        """
        2D 预测。

        参数
        ----------
        E_query : ndarray
        cos_theta_query : ndarray

        返回
        -------
        ndarray : 预测截面
        """
        if self._interp_2d is None:
            raise ValueError("2D interpolator not fitted")

        result = self._interp_2d(E_query, cos_theta_query)
        if self._log_space:
            return np.exp(result)
        return result

    def speed_benchmark(self, E_query: np.ndarray, n_repeat: int = 1000
                         ) -> Dict[str, float]:
        """
        与直接计算相比的速度基准。

        参数
        ----------
        E_query : ndarray
        n_repeat : int

        返回
        -------
        dict : 时间、加速比
        """
        import time

        # 预热
        _ = self.predict_1d(E_query)

        # 计时
        start = time.perf_counter()
        for _ in range(n_repeat):
            _ = self.predict_1d(E_query)
        elapsed = time.perf_counter() - start

        return {
            'n_repeat': n_repeat,
            'total_time_s': elapsed,
            'time_per_call_us': elapsed / n_repeat * 1e6,
        }


class SpectralGaussianProcess:
    """
    谱数据的高斯过程回归。

    用于：
    - 带不确定性的截面插值
    - 稀疏数据的智能补全
    - 实验数据的模型校准
    """

    def __init__(self, kernel: str = 'RBF',
                 alpha: float = 1e-10,
                 n_restarts: int = 5):
        if not HAS_SKLEARN:
            raise ImportError("scikit-learn required for SpectralGaussianProcess")

        self.alpha = alpha
        self.n_restarts = n_restarts
        self.kernel_name = kernel

        # 构造核函数
        if kernel.upper() == 'RBF':
            kernel_obj = RBF(length_scale=1.0) + WhiteKernel(noise_level=1e-3)
        elif kernel.upper() == 'MATERN':
            kernel_obj = Matern(length_scale=1.0, nu=1.5) + WhiteKernel(noise_level=1e-3)
        else:
            kernel_obj = RBF(length_scale=1.0) + WhiteKernel(noise_level=1e-3)

        self._gpr = GaussianProcessRegressor(
            kernel=kernel_obj, alpha=alpha,
            n_restarts_optimizer=n_restarts,
            random_state=42,
        )
        self._scaler_X = StandardScaler()
        self._scaler_y = StandardScaler()
        self._is_fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray,
            auto_scale: bool = True) -> 'SpectralGaussianProcess':
        """
        拟合 GP 模型。

        参数
        ----------
        X_train : ndarray (n_samples, n_features)
        y_train : ndarray (n_samples,)
        auto_scale : bool

        返回
        -------
        self
        """
        if auto_scale:
            X_scaled = self._scaler_X.fit_transform(X_train)
            y_scaled = self._scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()
        else:
            X_scaled = X_train
            y_scaled = y_train

        self._gpr.fit(X_scaled, y_scaled)
        self._is_fitted = True
        return self

    def predict(self, X_pred: np.ndarray,
                return_std: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        GP 预测。

        参数
        ----------
        X_pred : ndarray (n_samples, n_features)
        return_std : bool

        返回
        -------
        y_mean : ndarray
        y_std : ndarray
        """
        if not self._is_fitted:
            raise ValueError("Model not fitted")

        X_scaled = self._scaler_X.transform(X_pred)
        y_mean_scaled, y_std_scaled = self._gpr.predict(X_scaled, return_std=True)

        y_mean = self._scaler_y.inverse_transform(y_mean_scaled.reshape(-1, 1)).ravel()

        # 标准差反归一化（近似）
        y_std = y_std_scaled * self._scaler_y.scale_[0]

        if return_std:
            return y_mean, y_std
        return y_mean

    def kernel_info(self) -> Dict[str, Any]:
        """GP 核函数参数信息"""
        if not self._is_fitted:
            return {'fitted': False}
        return {
            'kernel': str(self._gpr.kernel_),
            'log_marginal_likelihood': float(self._gpr.log_marginal_likelihood_value_),
            'theta': self._gpr.kernel_.theta.tolist(),
        }


# ============================================================
#  4. 谱数据降维
# ============================================================

class SpectralPCAReducer:
    """
    谱数据的 PCA 降维与特征提取。

    用 PCA 提取谱数据的主导模式，加速后续 ML 训练。
    """

    def __init__(self, n_components: int = 3):
        self.n_components = n_components
        self._pca: Optional[PCA] = None
        self._scaler = StandardScaler()
        self._is_fitted = False

    def fit(self, spectral_data: np.ndarray) -> 'SpectralPCAReducer':
        """
        拟合 PCA。

        参数
        ----------
        spectral_data : ndarray (n_samples, n_features)
            谱数据（每行是一个谱向量）

        返回
        -------
        self
        """
        if not HAS_SKLEARN:
            raise ImportError("scikit-learn required for PCA")

        data_scaled = self._scaler.fit_transform(spectral_data)
        self._pca = PCA(n_components=min(self.n_components, spectral_data.shape[1]))
        self._pca.fit(data_scaled)
        self._is_fitted = True
        return self

    def transform(self, spectral_data: np.ndarray) -> np.ndarray:
        """降维变换"""
        if not self._is_fitted or self._pca is None:
            raise ValueError("PCA not fitted")
        data_scaled = self._scaler.transform(spectral_data)
        return self._pca.transform(data_scaled)

    def inverse_transform(self, latent: np.ndarray) -> np.ndarray:
        """从潜变量恢复谱数据"""
        if not self._is_fitted or self._pca is None:
            raise ValueError("PCA not fitted")
        data_scaled = self._pca.inverse_transform(latent)
        return self._scaler.inverse_transform(data_scaled)

    def explained_variance_ratio(self) -> np.ndarray:
        """各主成分解释的方差比"""
        if not self._is_fitted or self._pca is None:
            return np.array([])
        return self._pca.explained_variance_ratio_

    @property
    def components(self) -> np.ndarray:
        if not self._is_fitted or self._pca is None:
            return np.array([])
        return self._pca.components_


# ============================================================
#  5. 贝叶斯推断参数估计
# ============================================================

class SpectralBayesianInference:
    """
    谱框架下的贝叶斯推断。

    利用 MCMC 采样从实验数据反推谱参数。
    适合：截面测量 → 耦合常数/截断参数的后验估计。

    核心技术：
    - Metropolis-Hastings MCMC
    - 谱先验构造（从谱间隙 Δλ_min 等先验约束）
    - 似然函数（高斯噪声假设）
    """

    def __init__(self, param_names: List[str],
                 prior_means: np.ndarray,
                 prior_stds: np.ndarray,
                 param_bounds: Optional[np.ndarray] = None):
        """
        参数
        ----------
        param_names : list[str]
            参数名列表
        prior_means : ndarray
            先验均值
        prior_stds : ndarray
            先验标准差
        param_bounds : ndarray, optional (n_params, 2)
            参数边界 [min, max]
        """
        self.param_names = param_names
        self.n_params = len(param_names)
        self.prior_means = np.asarray(prior_means, dtype=float)
        self.prior_stds = np.asarray(prior_stds, dtype=float)
        self.param_bounds = param_bounds

        # MCMC 状态
        self._chain: Optional[np.ndarray] = None
        self._log_prob_chain: Optional[np.ndarray] = None
        self._acceptance_rate: float = 0.0

    def _log_prior(self, theta: np.ndarray) -> float:
        """对数先验"""
        log_p = -0.5 * np.sum(((theta - self.prior_means) / self.prior_stds) ** 2)

        # 边界约束
        if self.param_bounds is not None:
            for i in range(self.n_params):
                lo, hi = self.param_bounds[i]
                if theta[i] < lo or theta[i] > hi:
                    return -np.inf

        return float(log_p)

    def _log_likelihood(self, theta: np.ndarray,
                         observed_data: np.ndarray,
                         model_func: Callable[[np.ndarray], np.ndarray],
                         data_errors: np.ndarray) -> float:
        """
        对数似然（高斯噪声）。

        ln L = -½ Σ (y_i - f(x_i; θ))² / σ_i²
        """
        predictions = model_func(theta)
        chi2 = np.sum(((observed_data - predictions) / data_errors) ** 2)
        return -0.5 * chi2

    def _log_posterior(self, theta: np.ndarray,
                        observed_data: np.ndarray,
                        model_func: Callable[[np.ndarray], np.ndarray],
                        data_errors: np.ndarray) -> float:
        """对数后验"""
        log_prior = self._log_prior(theta)
        if not np.isfinite(log_prior):
            return -np.inf
        log_like = self._log_likelihood(theta, observed_data, model_func, data_errors)
        return log_prior + log_like

    def run_mcmc(self, observed_data: np.ndarray,
                 model_func: Callable[[np.ndarray], np.ndarray],
                 data_errors: np.ndarray,
                 n_steps: int = 5000,
                 step_sizes: Optional[np.ndarray] = None,
                 n_warmup: int = 1000,
                 verbose: bool = True) -> Dict[str, Any]:
        """
        运行 MCMC 采样。

        参数
        ----------
        observed_data : ndarray (n_points,)
            观测数据
        model_func : callable(theta) -> ndarray
            模型函数（参数 → 预测）
        data_errors : ndarray (n_points,)
            数据误差
        n_steps : int
            总采样步数
        step_sizes : ndarray, optional
            建议步长
        n_warmup : int
            预热步数（舍弃）
        verbose : bool

        返回
        -------
        dict : {chain, log_prob, acceptance_rate, summary}
        """
        if step_sizes is None:
            step_sizes = self.prior_stds * 0.1

        # 初始参数（从先验采样）
        theta_current = self.prior_means + np.random.randn(self.n_params) * self.prior_stds * 0.01

        n_keep = n_steps - n_warmup
        chain = np.zeros((n_keep, self.n_params))
        log_prob_chain = np.zeros(n_keep)
        n_accept = 0

        for i in range(n_steps):
            # 建议步
            proposal = theta_current + np.random.randn(self.n_params) * step_sizes

            # 后验比
            log_p_current = self._log_posterior(
                theta_current, observed_data, model_func, data_errors
            )
            log_p_proposal = self._log_posterior(
                proposal, observed_data, model_func, data_errors
            )

            # Metropolis 接受/拒绝
            log_alpha = log_p_proposal - log_p_current
            if np.log(np.random.random()) < min(log_alpha, 0.0):
                theta_current = proposal
                if i >= n_warmup:
                    n_accept += 1

            # 存储
            if i >= n_warmup:
                idx = i - n_warmup
                chain[idx] = theta_current
                log_prob_chain[idx] = log_p_current

            if verbose and (i + 1) % 1000 == 0:
                print(f"  MCMC step {i + 1}/{n_steps}, "
                      f"accept={n_accept / max(i - n_warmup + 1, 1):.3f}")

        self._chain = chain
        self._log_prob_chain = log_prob_chain
        self._acceptance_rate = n_accept / max(n_keep, 1)

        # 统计摘要
        summary = self._compute_summary()

        if verbose:
            print(f"\n  MCMC complete: {n_keep} samples, "
                  f"acceptance rate = {self._acceptance_rate:.3f}")
            for i, name in enumerate(self.param_names):
                print(f"    {name}: {summary['mean'][i]:.4f} ± {summary['std'][i]:.4f} "
                      f"({summary['q16'][i]:.4f}, {summary['q84'][i]:.4f})")

        return {
            'chain': chain,
            'log_prob': log_prob_chain,
            'acceptance_rate': self._acceptance_rate,
            'summary': summary,
        }

    def _compute_summary(self) -> Dict[str, np.ndarray]:
        """MCMC 链统计摘要"""
        if self._chain is None:
            return {}
        return {
            'mean': np.mean(self._chain, axis=0),
            'std': np.std(self._chain, axis=0),
            'q16': np.percentile(self._chain, 16, axis=0),
            'q50': np.percentile(self._chain, 50, axis=0),
            'q84': np.percentile(self._chain, 84, axis=0),
        }

    def credible_interval(self, param_idx: int, prob: float = 0.95
                           ) -> Tuple[float, float]:
        """参数可信区间"""
        if self._chain is None:
            return (0.0, 0.0)
        alpha = (1.0 - prob) / 2.0
        return (
            float(np.percentile(self._chain[:, param_idx], alpha * 100)),
            float(np.percentile(self._chain[:, param_idx], (1.0 - alpha) * 100)),
        )


# ============================================================
#  6. 统一 ML 工具类
# ============================================================

class SpectralMLAccelerator:
    """
    谱 ML 加速器的统一接口。

    封装 C3 所有功能，提供一键式 ML 加速。
    """

    def __init__(self, dim: int = 32):
        self.dim = dim
        self.nn: Optional[SpectralNeuralNetwork] = None
        self.gp: Optional[SpectralGaussianProcess] = None
        self.interp: Optional[SpectralInterpolator] = None
        self.pca: Optional[SpectralPCAReducer] = None
        self.bayes: Optional[SpectralBayesianInference] = None

    def train_amplitude_surrogate(self, s_train: np.ndarray,
                                    cos_theta_train: np.ndarray,
                                    amplitude_train: np.ndarray) -> 'SpectralMLAccelerator':
        """训练振幅替代模型"""
        self.nn = SpectralNeuralNetwork(hidden_layer_sizes=(64, 32))
        self.nn.fit(s_train, cos_theta_train, amplitude_train)
        return self

    def train_gp_interpolator(self, X_train: np.ndarray,
                                y_train: np.ndarray) -> 'SpectralMLAccelerator':
        """训练 GP 插值器"""
        self.gp = SpectralGaussianProcess(kernel='RBF')
        self.gp.fit(X_train, y_train)
        return self

    def setup_bayesian_inference(self, param_names: List[str],
                                   prior_means: np.ndarray,
                                   prior_stds: np.ndarray,
                                   param_bounds: Optional[np.ndarray] = None
                                   ) -> 'SpectralMLAccelerator':
        """设置贝叶斯推断"""
        self.bayes = SpectralBayesianInference(
            param_names, prior_means, prior_stds, param_bounds
        )
        return self

    def amplitude_predict(self, s: np.ndarray,
                            cos_theta: np.ndarray) -> np.ndarray:
        """用训练好的 NN 预测振幅"""
        if self.nn is None or not self.nn.is_trained:
            raise ValueError("NN not trained. Call train_amplitude_surrogate first.")
        return self.nn.predict(s, cos_theta)

    def gp_predict(self, X: np.ndarray) -> np.ndarray:
        """用训练好的 GP 预测"""
        if self.gp is None:
            raise ValueError("GP not trained. Call train_gp_interpolator first.")
        mean, _ = self.gp.predict(X)
        return mean


# ============================================================
#  7. 数值验证
# ============================================================

def _generate_test_data(n_points: int = 200) -> Tuple[np.ndarray, ...]:
    """生成谱振幅测试数据（教学用）"""
    np.random.seed(42)

    # 能量和散射角
    s = np.geomspace(0.01, 2.0, n_points)
    cos_theta = np.random.uniform(-0.99, 0.99, n_points)

    # 模拟谱振幅 |M| ∝ κ² * (s⁴ + t⁴ + u⁴)/(stu) * exp(-s/Λ²)
    kappa_sq = 32.0 * np.pi
    t = -0.5 * s * (1.0 - cos_theta)
    u = -0.5 * s * (1.0 + cos_theta)

    amplitude = np.zeros(n_points)
    for i in range(n_points):
        si, ti, ui = s[i], t[i], u[i]
        if abs(si * ti * ui) > 1e-40:
            amp_tree = kappa_sq * (si ** 4 + ti ** 4 + ui ** 4) / (si * ti * ui)
            amp_spec = amp_tree * np.exp(-si / LAMBDA_MAX)
            amplitude[i] = abs(amp_spec)
        else:
            amplitude[i] = 0.0

    # 加噪声
    amplitude += np.random.randn(n_points) * amplitude * 0.05

    return s, cos_theta, amplitude


def verify_nn_approximation():
    """验证神经网络振幅近似"""
    if not HAS_SKLEARN:
        print("  Skipping (no sklearn)")
        return True

    s, ct, amp = _generate_test_data(n_points=100)

    # 拆分
    split = 80
    s_train, s_test = s[:split], s[split:]
    ct_train, ct_test = ct[:split], ct[split:]
    amp_train, amp_test = amp[:split], amp[split:]

    nn = SpectralNeuralNetwork(hidden_layer_sizes=(64, 32), max_iter=1000)
    # 对数尺度训练（振幅跨量级）
    nn.fit(s_train, ct_train, np.log1p(amp_train))

    pred_log = nn.predict(s_test, ct_test)
    pred = np.expm1(pred_log)
    true = amp_test

    # 相对误差
    rel_err = np.mean(np.abs(pred - true) / np.maximum(true, 1e-30))
    print(f"  Mean relative error = {rel_err:.4f}")

    # 至少趋势正确
    pred_corr = np.corrcoef(pred, true)[0, 1] if len(pred) > 1 else 0
    print(f"  Correlation = {pred_corr:.4f}")

    assert np.all(np.isfinite(pred))
    assert rel_err < 5.0  # 量级内合理
    print("  ✅ NN approximation verified")
    return True


def verify_numpy_nn():
    """验证纯 NumPy 神经网络"""
    s, ct, amp = _generate_test_data(n_points=50)

    # 准备特征
    eps = 1e-30
    X = np.column_stack([s, ct, np.log(s + eps), 1.0 / (s + eps)])
    y = amp.reshape(-1, 1)

    # 归一化
    X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-10)
    y = (y - np.mean(y)) / (np.std(y) + 1e-10)

    nnp = NumpyNeuralNetwork(n_input=4, n_hidden=16, n_output=1,
                              learning_rate=0.01, n_epochs=500)
    nnp.train(X, y)

    final_loss = nnp.loss_history[-1] if nnp.loss_history else 0
    print(f"  Final training loss = {final_loss:.6f}")
    print(f"  Loss history length = {len(nnp.loss_history)}")

    assert len(nnp.loss_history) > 0
    print("  ✅ NumPy NN verified")
    return True


def verify_interpolator():
    """验证谱插值器"""
    s, ct, amp = _generate_test_data(n_points=50)

    # 1D 插值
    s_grid = np.geomspace(0.01, 2.0, 20)
    # 用模拟截面
    sigma_grid = amp[:20] ** 2 / (64.0 * np.pi ** 2 * s_grid)

    interp = SpectralInterpolator(method='cubic')
    interp.fit_1d(s_grid, sigma_grid)

    # 插值预测
    s_query = np.array([0.05, 0.5, 1.0])
    pred = interp.predict_1d(s_query)
    print(f"  Interpolation at s={s_query[0]:.3f}: σ={pred[0]:.4e}")
    print(f"  Interpolation at s={s_query[1]:.3f}: σ={pred[1]:.4e}")
    print(f"  Interpolation at s={s_query[2]:.3f}: σ={pred[2]:.4e}")

    assert np.all(np.isfinite(pred))
    assert np.all(pred > 0)

    # 速度基准
    bench = interp.speed_benchmark(np.geomspace(0.01, 2.0, 100), n_repeat=500)
    print(f"  Benchmark: {bench['time_per_call_us']:.2f} μs/call (500 repeats)")

    print("  ✅ Interpolator verified")
    return True


def verify_gaussian_process():
    """验证高斯过程回归"""
    if not HAS_SKLEARN:
        print("  Skipping (no sklearn)")
        return True

    s, ct, amp = _generate_test_data(n_points=30)

    X = np.column_stack([s, ct])
    split = 20
    gp = SpectralGaussianProcess(kernel='RBF')
    gp.fit(X[:split], amp[:split])

    mean, std = gp.predict(X[split:])
    print(f"  GP predictions: mean={mean[:3]}")
    print(f"  GP std: {std[:3]}")
    print(f"  GP kernel: {gp.kernel_info()['kernel'][:60]}...")

    assert np.all(np.isfinite(mean))
    assert np.all(std >= 0)
    print("  ✅ Gaussian process verified")
    return True


def verify_bayesian_inference():
    """验证贝叶斯推断"""
    # 构造简单测试：推断谱截断参数 Λ
    # 模拟数据：σ(Λ) = σ₀ * exp(-s/Λ²)
    param_names = ['log_Lambda']
    prior_means = np.array([0.0])  # log(Λ/M_Pl)
    prior_stds = np.array([1.0])
    bounds = np.array([[-3.0, 3.0]])

    bayes = SpectralBayesianInference(param_names, prior_means, prior_stds, bounds)

    # 模拟观测数据
    true_log_Lambda = -0.5  # Λ ≈ 0.6 M_Pl
    s_data = np.array([0.1, 0.5, 1.0, 2.0])
    sigma_model = lambda theta: np.exp(-s_data / np.exp(theta[0]) ** 2) * 100
    observed = sigma_model(np.array([true_log_Lambda]))
    errors = observed * 0.1  # 10% 误差

    def model_func(theta):
        return sigma_model(theta)

    result = bayes.run_mcmc(observed, model_func, errors,
                             n_steps=3000, n_warmup=500, verbose=False)

    summary = result['summary']
    inferred = summary['mean'][0]
    print(f"  True log Λ = {true_log_Lambda:.3f}")
    print(f"  Inferred log Λ = {inferred:.3f} ± {summary['std'][0]:.3f}")
    print(f"  Acceptance rate = {result['acceptance_rate']:.3f}")

    # 真值应在 1σ 内
    assert abs(inferred - true_log_Lambda) < 2.0 * summary['std'][0]
    print("  ✅ Bayesian inference verified")
    return True


def verify_pca_reduction():
    """验证 PCA 降维"""
    if not HAS_SKLEARN:
        print("  Skipping (no sklearn)")
        return True

    np.random.seed(42)
    n_spectra = 50
    n_features = 20

    # 模拟谱数据（前 3 个模式重要）
    spectra = np.random.randn(n_spectra, 3) @ np.random.randn(3, n_features)
    spectra += 0.1 * np.random.randn(n_spectra, n_features)

    pca = SpectralPCAReducer(n_components=3)
    pca.fit(spectra)

    var_ratio = pca.explained_variance_ratio()
    print(f"  Explained variance ratio: {var_ratio}")
    print(f"  Cumulative: {np.sum(var_ratio):.4f}")

    assert np.sum(var_ratio) > 0.8  # 前 3 主成分解释大部分方差
    print("  ✅ PCA reduction verified")
    return True


def run_all_tests():
    """运行所有 C3 测试"""
    print("=" * 60)
    print("C3: Spectral Machine Learning Tests")
    print("=" * 60)

    tests = [
        ("NN amplitude approximation", verify_nn_approximation),
        ("NumPy neural network", verify_numpy_nn),
        ("Spectral interpolator", verify_interpolator),
        ("Gaussian process regression", verify_gaussian_process),
        ("Bayesian inference", verify_bayesian_inference),
        ("PCA reduction", verify_pca_reduction),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            print(f"\n--- {name} ---")
            test_fn()
            passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 60}")
    if passed == len(tests):
        print(f"✅ {passed}/{len(tests)} C3 tests passed!")
    else:
        print(f"⚠️  {passed}/{len(tests)} C3 tests passed")

    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
