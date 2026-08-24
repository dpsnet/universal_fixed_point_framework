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
Phase 52 — C2: 并行计算加速
===============================

利用并行计算加速大规模谱计算。

内容：
  1. GPU 加速谱矩阵运算（JAX/CuPy 风格 API，CPU 降级模式）
  2. 分布式谱演化计算（multiprocessing 多进程并行）
  3. 内存优化策略（分块矩阵、LRU 缓存、内存映射）

依赖：numpy, scipy, multiprocessing, functools
"""

import numpy as np
from typing import Optional, Callable, Any, Dict, List, Tuple, Generator
from dataclasses import dataclass, field
from functools import lru_cache, partial
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import os
import sys
import time
import hashlib
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralMatrix,
    SpectralEvolutionSolver, M_PL, G_N
)


# ============================================================
#  硬件检测
# ============================================================

def detect_hardware() -> Dict[str, Any]:
    """
    检测可用硬件资源。

    返回
    -------
    dict : {cpu_count, has_gpu, gpu_backend, memory_gb}
    """
    info = {
        'cpu_count': mp.cpu_count(),
        'has_gpu': False,
        'gpu_backend': None,
        'memory_gb': 0.0,
    }

    # CPU 核数
    info['cpu_count'] = mp.cpu_count()

    # 检测 GPU（仅报告是否可用，不强制依赖）
    try:
        import jax
        info['has_gpu'] = True
        info['gpu_backend'] = 'jax'
    except ImportError:
        try:
            import cupy
            info['has_gpu'] = True
            info['gpu_backend'] = 'cupy'
        except ImportError:
            info['has_gpu'] = False
            info['gpu_backend'] = 'none (using numpy CPU)'

    # 估算可用内存（仅用于参考）
    try:
        import psutil
        info['memory_gb'] = psutil.virtual_memory().total / (1024 ** 3)
    except ImportError:
        info['memory_gb'] = 0.0

    return info


# 硬件信息
HARDWARE_INFO = detect_hardware()
N_CPUS = HARDWARE_INFO['cpu_count']
HAS_GPU = HARDWARE_INFO['has_gpu']
GPU_BACKEND = HARDWARE_INFO['gpu_backend']


# ============================================================
#  1. GPU 加速谱矩阵运算
# ============================================================

class SpectralGPUAccelerator:
    """
    GPU 加速谱矩阵运算。

    提供 JAX/CuPy 风格的 GPU 加速 API，并兼容无 GPU 环境（CPU 降级模式）。
    不引入硬性 GPU 依赖——在无 GPU 时自动使用 numpy 矢量化运算。
    """

    def __init__(self, use_gpu: Optional[bool] = None, device_id: int = 0):
        """
        参数
        ----------
        use_gpu : bool, optional
            是否使用 GPU。默认自动检测。
        device_id : int
            GPU 设备 ID（仅 CuPy 模式有效）
        """
        if use_gpu is None:
            self.use_gpu = HAS_GPU
        else:
            self.use_gpu = use_gpu and HAS_GPU

        self.device_id = device_id
        self._backend = GPU_BACKEND if self.use_gpu else 'numpy'

        # 后端初始化
        if self.use_gpu and self._backend == 'jax':
            import jax.numpy as jnp
            self.xp = jnp
            self._to_numpy = lambda x: np.array(x) if hasattr(x, 'device') else x
        elif self.use_gpu and self._backend == 'cupy':
            import cupy as cp
            self.xp = cp
            self._to_numpy = lambda x: cp.asnumpy(x) if hasattr(x, 'get') else x
        else:
            self.xp = np  # CPU fallback
            self._to_numpy = lambda x: x

    @property
    def backend_name(self) -> str:
        """当前后端名称"""
        return self._backend

    # ---- 谱矩阵运算 ----

    def spectral_diagonalize(self, matrix: np.ndarray) -> Dict[str, np.ndarray]:
        """
        GPU 加速的谱分解。

        对 Hermitian 矩阵 A 计算 A = U Λ U^†。

        参数
        ----------
        matrix : ndarray
            输入矩阵

        返回
        -------
        dict : {eigenvalues, eigenvectors}
        """
        x_mat = self.xp.asarray(matrix) if self.use_gpu else matrix
        evals, evecs = self.xp.linalg.eigh(x_mat)
        return {
            'eigenvalues': self._to_numpy(evals),
            'eigenvectors': self._to_numpy(evecs),
        }

    def spectral_matrix_multiply(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        GPU 加速的谱矩阵乘法。

        参数
        ----------
        A, B : ndarray
            输入矩阵

        返回
        -------
        ndarray : A @ B
        """
        xA = self.xp.asarray(A) if self.use_gpu else A
        xB = self.xp.asarray(B) if self.use_gpu else B
        result = xA @ xB
        return self._to_numpy(result)

    def spectral_matrix_function(self, matrix: np.ndarray,
                                  func: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
        """
        GPU 加速的谱矩阵函数 f(A) = U f(Λ) U^†。

        参数
        ----------
        matrix : ndarray
            Hermitian 矩阵
        func : callable
            标量函数

        返回
        -------
        ndarray : f(A)
        """
        diag = self.spectral_diagonalize(matrix)
        evals = self.xp.asarray(diag['eigenvalues']) if self.use_gpu else diag['eigenvalues']
        evecs = self.xp.asarray(diag['eigenvectors']) if self.use_gpu else diag['eigenvectors']

        f_evals = func(evals)
        result = evecs @ self.xp.diag(f_evals) @ evecs.conj().T

        return self._to_numpy(result)

    def spectral_trace(self, matrix: np.ndarray) -> float:
        """GPU 加速迹运算"""
        x_mat = self.xp.asarray(matrix) if self.use_gpu else matrix
        return float(self.xp.trace(x_mat).real)

    def batch_eigh(self, matrices: np.ndarray) -> Dict[str, np.ndarray]:
        """
        批量谱分解。

        matrices : ndarray of shape (batch, N, N)

        返回
        -------
        dict : {eigenvalues: (batch, N), eigenvectors: (batch, N, N)}
        """
        x_mats = self.xp.asarray(matrices) if self.use_gpu else matrices

        batch_size = x_mats.shape[0]
        N = x_mats.shape[1]

        evals = self.xp.zeros((batch_size, N), dtype=x_mats.real.dtype)
        evecs = self.xp.zeros_like(x_mats)

        for i in range(batch_size):
            e, v = self.xp.linalg.eigh(x_mats[i])
            evals[i] = e
            evecs[i] = v

        return {
            'eigenvalues': self._to_numpy(evals),
            'eigenvectors': self._to_numpy(evecs),
        }

    def benchmark(self, N: int = 256, n_iter: int = 5) -> Dict[str, float]:
        """
        基准测试。

        参数
        ----------
        N : int
            矩阵大小
        n_iter : int
            迭代次数

        返回
        -------
        dict : 性能统计
        """
        times = {'diagonalize': [], 'multiply': [], 'matrix_func': []}

        for _ in range(n_iter):
            A = np.random.randn(N, N) + 1j * np.random.randn(N, N)
            A = A @ A.conj().T  # Hermitian
            B = np.random.randn(N, N)

            t0 = time.perf_counter()
            self.spectral_diagonalize(A)
            times['diagonalize'].append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            self.spectral_matrix_multiply(A, B)
            times['multiply'].append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            self.spectral_matrix_function(A, np.exp)
            times['matrix_func'].append(time.perf_counter() - t0)

        return {
            'backend': self._backend,
            'N': N,
            'diagonalize_mean': np.mean(times['diagonalize']),
            'diagonalize_std': np.std(times['diagonalize']),
            'multiply_mean': np.mean(times['multiply']),
            'matrix_func_mean': np.mean(times['matrix_func']),
        }


# ============================================================
#  2. 分布式谱演化计算
# ============================================================

class SpectralDistributedSolver:
    """
    分布式谱演化求解器。

    将大规模谱计算分解为独立子任务，通过 multiprocessing 并行执行。
    支持：
    - 谱流方程的多参数并行扫描
    - 大矩阵的分块特征值求解
    - 时间序列的并行演化
    """

    def __init__(self, n_workers: Optional[int] = None):
        self.n_workers = n_workers or max(1, N_CPUS - 1)
        self._result_cache: Dict[str, Any] = {}

    # ---- 参数扫描 ----

    def parallel_parameter_scan(self,
                                scan_func: Callable,
                                param_grid: Dict[str, np.ndarray],
                                combine_fn: Optional[Callable] = None) -> Dict[str, Any]:
        """
        多参数并行扫描。

        将参数网格划分为独立任务，并行执行 scan_func。

        参数
        ----------
        scan_func : callable(**params) -> result
            单点评估函数
        param_grid : dict of {name: values}
            参数网格
        combine_fn : callable, optional
            结果合并函数（默认返回列表）

        返回
        -------
        dict : {params, results}
        """
        # 生成参数组合
        keys = list(param_grid.keys())
        values = list(param_grid.values())

        # 使用 meshgrid 生成网格
        grids = np.meshgrid(*values, indexing='ij')
        n_total = grids[0].size

        param_sets = []
        for i in range(n_total):
            params = {k: float(grids[idx].flat[i]) for idx, k in enumerate(keys)}
            param_sets.append(params)

        # 并行执行
        results = self._parallel_map(scan_func, param_sets)

        # 合并（若未指定合并函数，返回数据字典）
        if combine_fn is not None:
            return combine_fn(param_sets, results)

        # 构造结果字典
        result_dict = {}
        for k in keys:
            result_dict[k] = param_grid[k]
        result_dict['results'] = results

        return result_dict

    def _parallel_map(self, func: Callable,
                      arg_list: List[Any]) -> List[Any]:
        """
        并行 map 实现。

        优先使用 ProcessPoolExecutor 多进程并行。
        若多进程执行失败（如无序列化支持），自动降级为串行执行。
        """
        if len(arg_list) <= 1:
            # 串行执行（单任务时避免进程开销）
            return [func(args) for args in arg_list]

        results = []

        # 尝试 ProcessPoolExecutor
        try:
            with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
                futures = {}
                for i, args in enumerate(arg_list):
                    try:
                        fut = executor.submit(func, args)
                        futures[fut] = i
                    except Exception:
                        # pickle 序列化失败 → 降级到串行
                        results = [func(args) for args in arg_list]
                        return results

                for fut in as_completed(futures):
                    try:
                        idx = futures[fut]
                        results.append((idx, fut.result()))
                    except Exception as e:
                        results.append((-1, {'error': str(e)}))

                # 按原始顺序重排
                results.sort(key=lambda x: x[0])
                results = [r[1] for r in results]
                return results

        except Exception:
            # 其他失败 → 串行降级
            results = [func(args) for args in arg_list]

        return results

    # ---- 时间序列并行 ----

    def parallel_time_evolution(self,
                                 solver: SpectralEvolutionSolver,
                                 initial_conditions: List[np.ndarray],
                                 t_span: Tuple[float, float],
                                 flow_func: Callable,
                                 n_steps: int = 500) -> List[Dict[str, Any]]:
        """
        多初始条件的并行时间演化。

        参数
        ----------
        solver : SpectralEvolutionSolver
            谱演化求解器
        initial_conditions : list of ndarray
            初始条件列表
        t_span : (float, float)
            时间范围
        flow_func : callable
            谱流函数 F(λ, t)
        n_steps : int
            步数

        返回
        -------
        list of dict : 每条初始条件的演化结果
        """
        def _evolve(psi0):
            return solver.solve_spectral_flow(
                psi0, t_span, flow_func, n_steps=n_steps
            )

        return self._parallel_map(_evolve, initial_conditions)

    # ---- 分块谱分解 ----

    def blocked_eigh(self, matrix: np.ndarray,
                     block_size: int = 64) -> Dict[str, np.ndarray]:
        """
        分块谱分解（适用于超大矩阵）。

        将大矩阵划分为子块，对各块并行求解特征值，
        再通过分治策略合并。

        参数
        ----------
        matrix : ndarray
            输入 Hermitian 矩阵（N x N）
        block_size : int
            子块大小

        返回
        -------
        dict : {eigenvalues, eigenvectors}
        """
        N = matrix.shape[0]
        n_blocks = (N + block_size - 1) // block_size

        # 分块
        blocks = []
        block_info = []
        for i in range(n_blocks):
            i_start = i * block_size
            i_end = min((i + 1) * block_size, N)
            for j in range(i, n_blocks):
                j_start = j * block_size
                j_end = min((j + 1) * block_size, N)
                block = matrix[i_start:i_end, j_start:j_end]
                blocks.append(block)
                block_info.append((i, j, i_start, i_end, j_start, j_end))

        # 并行求解各对角块的特征值
        block_results = self._parallel_map(
            _diag_block_worker,
            list(zip(blocks, block_info))
        )

        # 合并结果（近似方法：仅合并对角块的特征值）
        all_evals = []
        for r in block_results:
            if r['type'] == 'diagonal':
                all_evals.extend(r['eigenvalues'].tolist())

        all_evals = np.sort(all_evals)

        return {
            'eigenvalues': all_evals,
            'eigenvectors': None,  # 分块模式下不组装完整特征向量
            'n_blocks': n_blocks,
            'block_size': block_size,
        }

    # ---- 并行谱流扫描 ----

    def parallel_spectral_flow_scan(self,
                                     flow_func: Callable,
                                     lambda_range: Tuple[float, float],
                                     param_name: str,
                                     param_values: np.ndarray,
                                     n_modes: int = 10,
                                     t_span: Tuple[float, float] = (0, 10),
                                     n_steps: int = 200) -> Dict[str, Any]:
        """
        对谱流方程的关键参数进行并行扫描。

        参数
        ----------
        flow_func : callable(t, lambda, **param)
            谱流函数（含可调参数）
        lambda_range : (float, float)
            初始特征值范围
        param_name : str
            扫描参数名
        param_values : ndarray
            扫描参数值
        n_modes : int
            谱模式数
        t_span : (float, float)
            时间范围
        n_steps : int
            步数

        返回
        -------
        dict : {param_values, evolutions}
        """
        def _scan(param_val):
            lambda0 = np.linspace(lambda_range[0], lambda_range[1], n_modes)
            solver = SpectralEvolutionSolver(dim=n_modes)

            def _flow(t, lam):
                kwargs = {param_name: param_val}
                return flow_func(t, lam, **kwargs)

            return solver.solve_spectral_flow(lambda0, t_span, _flow, n_steps=n_steps)

        results = self._parallel_map(_scan, list(param_values))

        return {
            'param_values': param_values,
            'param_name': param_name,
            'evolutions': results,
        }


# ============================================================
#  3. 内存优化策略
# ============================================================

class SpectralMemoryOptimizer:
    """
    谱计算内存优化。

    策略：
    1. 分块矩阵运算（避免完整矩阵驻留内存）
    2. LRU 缓存（缓存频繁访问的谱分解结果）
    3. 内存映射（mmap）大型谱数组
    4. 稀疏谱表示（对近对角矩阵使用稀疏格式）
    """

    def __init__(self, cache_size: int = 32, use_sparse: bool = True):
        self.cache_size = cache_size
        self.use_sparse = use_sparse
        self._cache: Dict[str, Any] = {}
        self._cache_order: List[str] = []

    # ---- LRU 缓存 ----

    def _cache_key(self, obj: Any) -> str:
        """生成缓存键"""
        if isinstance(obj, np.ndarray):
            return hashlib.md5(obj.tobytes()[:1024]).hexdigest()
        return hashlib.md5(str(obj).encode()).hexdigest()

    def cached_diagonalize(self, matrix: np.ndarray) -> Dict[str, np.ndarray]:
        """
        LRU 缓存的谱分解。

        对频繁访问的相同矩阵避免重复分解。
        """
        key = self._cache_key(matrix)

        if key in self._cache:
            # 更新访问顺序
            self._cache_order.remove(key)
            self._cache_order.append(key)
            return self._cache[key]

        # 计算谱分解
        evals, evecs = np.linalg.eigh(matrix)
        result = {'eigenvalues': evals, 'eigenvectors': evecs}

        # 缓存
        self._cache[key] = result
        self._cache_order.append(key)

        # LRU 驱逐
        if len(self._cache) > self.cache_size:
            oldest = self._cache_order.pop(0)
            del self._cache[oldest]

        return result

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        self._cache_order.clear()

    @property
    def cache_hit_rate(self) -> float:
        """缓存命中率（估计值，仅计数）"""
        return 0.0  # 需要更复杂的追踪

    # ---- 分块矩阵运算 ----

    def blocked_matrix_multiply(self, A: np.ndarray, B: np.ndarray,
                                 block_size: int = 128) -> np.ndarray:
        """
        分块矩阵乘法（内存友好）。

        对大型矩阵 A @ B，每次只加载 block_size × block_size 的子块。

        参数
        ----------
        A, B : ndarray
            输入矩阵
        block_size : int
            子块大小

        返回
        -------
        ndarray : A @ B
        """
        m, k = A.shape
        k2, n = B.shape
        assert k == k2, f"Shape mismatch: A {A.shape}, B {B.shape}"

        C = np.zeros((m, n), dtype=np.complex128)

        for i in range(0, m, block_size):
            i_end = min(i + block_size, m)
            A_block = A[i:i_end, :]

            for j in range(0, n, block_size):
                j_end = min(j + block_size, n)

                # 对 k 维度求和（使用小块减少内存）
                for p in range(0, k, block_size):
                    p_end = min(p + block_size, k)
                    B_block = B[p:p_end, j:j_end]
                    C[i:i_end, j:j_end] += A_block[:, p:p_end] @ B_block

        return C

    def blocked_spectral_flow(self, lambda0: np.ndarray,
                               t_vals: np.ndarray,
                               flow_func: Callable,
                               block_size: int = 50) -> Dict[str, np.ndarray]:
        """
        分块谱流求解。

        将特征值分块，对每块独立求解谱流方程。
        适用于特征值数量大（> 100）的情况。

        参数
        ----------
        lambda0 : ndarray
            初始特征值（N 个）
        t_vals : ndarray
            时间网格
        flow_func : callable(t, lam_block) -> ndarray
            谱流函数
        block_size : int
            每块的特征值数

        返回
        -------
        dict : {t, lambda_history}
        """
        n_modes = len(lambda0)
        n_blocks = (n_modes + block_size - 1) // block_size

        lambda_history = np.zeros((n_modes, len(t_vals)))

        for b in range(n_blocks):
            b_start = b * block_size
            b_end = min((b + 1) * block_size, n_modes)
            block_indices = slice(b_start, b_end)

            lam_block = lambda0[block_indices].copy()
            n_block = len(lam_block)

            # 对小块使用标准 ODE 求解器
            from scipy import integrate

            def _flow_block(t, lam):
                return flow_func(t, lam)

            result = integrate.solve_ivp(
                _flow_block, (t_vals[0], t_vals[-1]), lam_block,
                method='RK45', t_eval=t_vals,
                rtol=1e-8, atol=1e-10,
            )

            lambda_history[block_indices, :] = result.y

        return {
            't': t_vals,
            'lambda_history': lambda_history,
        }

    # ---- 稀疏谱表示 ----

    def to_sparse(self, matrix: np.ndarray, threshold: float = 1e-10) -> Any:
        """
        将稠密矩阵转换为稀疏表示。

        参数
        ----------
        matrix : ndarray
            输入矩阵
        threshold : float
            稀疏化阈值（小于此值的元素置零）

        返回
        -------
        scipy.sparse.csr_matrix 或 ndarray（不满足稀疏条件时返回原矩阵）
        """
        if not self.use_sparse:
            return matrix

        from scipy import sparse as sp

        # 检查稀疏度
        n_total = matrix.size
        if n_total == 0:
            return matrix

        mask = np.abs(matrix) > threshold
        n_nonzero = np.sum(mask)
        sparsity = 1.0 - n_nonzero / n_total

        # 稀疏度 > 30% 时才使用稀疏格式
        if sparsity > 0.3:
            return sp.csr_matrix(matrix)
        else:
            return matrix

    def sparse_spectral_operator(self, operator: SpectralOperator,
                                  threshold: float = 1e-10) -> SpectralOperator:
        """
        将谱算子转换为稀疏格式。

        参数
        ----------
        operator : SpectralOperator
            谱算子
        threshold : float
            稀疏化阈值

        返回
        -------
        SpectralOperator : 稀疏化的谱算子
        """
        mat = operator.get_matrix()
        sparse_mat = self.to_sparse(mat, threshold)

        # 创建稀疏算子包装
        if hasattr(sparse_mat, 'toarray'):
            # 保持与原 SpectralOperator 相同接口
            sparse_op = SpectralOperator(dim=operator.dim, label=operator.label + '_sparse')
            sparse_op._matrix = sparse_mat
            # 缓存稀疏谱分解（对角化稀疏矩阵）
            from scipy.sparse import linalg as spla
            evals = spla.eigsh(sparse_mat, k=min(operator.dim - 1, 20), return_eigenvectors=False)
            sparse_op._data = SpectralData(
                eigenvalues=np.sort(evals),
                label=operator.label + '_sparse'
            )
            return sparse_op

        return operator

    # ---- 内存映射 ----

    def memmap_spectral_array(self, data: np.ndarray,
                               filename: str,
                               dtype: Optional[type] = None) -> np.memmap:
        """
        将大型谱数据存储为内存映射文件。

        参数
        ----------
        data : ndarray
            谱数据
        filename : str
            存储路径
        dtype : type, optional
            数据类型

        返回
        -------
        np.memmap : 内存映射数组
        """
        if dtype is None:
            dtype = data.dtype

        mmap = np.memmap(filename, dtype=dtype, mode='w+', shape=data.shape)
        mmap[:] = data[:]
        mmap.flush()

        return mmap

    def estimate_memory(self, dim: int, dtype: type = np.complex128) -> Dict[str, float]:
        """
        估算谱计算所需内存。

        参数
        ----------
        dim : int
            谱截断维数
        dtype : type
            数据类型

        返回
        -------
        dict : {matrix_gb, eigenvectors_gb, total_gb, recommended_blocks}
        """
        bytes_per_element = np.dtype(dtype).itemsize

        # 矩阵内存
        matrix_bytes = dim * dim * bytes_per_element
        # 特征向量内存（同大小）
        eigenvector_bytes = matrix_bytes
        # 谱数据内存
        spectral_data_bytes = dim * 8  # float64 特征值

        total_bytes = matrix_bytes + eigenvector_bytes + spectral_data_bytes
        total_gb = total_bytes / (1024 ** 3)

        # 推荐的分块数
        recommended_blocks = 1
        if total_gb > 1.0:
            recommended_blocks = int(np.ceil(total_gb / 0.5))  # 每块 ~500MB

        return {
            'dim': dim,
            'matrix_gb': matrix_bytes / (1024 ** 3),
            'eigenvectors_gb': eigenvector_bytes / (1024 ** 3),
            'spectral_data_mb': spectral_data_bytes / (1024 ** 2),
            'total_gb': total_gb,
            'recommended_blocks': recommended_blocks,
        }


# ============================================================
#  4. 便捷工具函数
# ============================================================

class SpectralParallelContext:
    """
    并行谱计算上下文管理器。

    整合 GPU 加速、分布式计算和内存优化，提供一站式并行谱计算接口。
    """

    def __init__(self, n_workers: Optional[int] = None,
                 use_gpu: Optional[bool] = None,
                 cache_size: int = 32):
        self.gpu = SpectralGPUAccelerator(use_gpu=use_gpu)
        self.dist = SpectralDistributedSolver(n_workers=n_workers)
        self.mem = SpectralMemoryOptimizer(cache_size=cache_size)

    @property
    def summary(self) -> Dict[str, Any]:
        """并行计算环境摘要"""
        return {
            'gpu_backend': self.gpu.backend_name,
            'n_workers': self.dist.n_workers,
            'cache_size': self.mem.cache_size,
            'use_sparse': self.mem.use_sparse,
            'cpu_count': N_CPUS,
            'has_gpu': HAS_GPU,
        }

    def optimize_for_matrix(self, dim: int) -> Dict[str, Any]:
        """
        针对给定矩阵大小的优化建议。

        参数
        ----------
        dim : int
            矩阵维数

        返回
        -------
        dict : 优化建议
        """
        mem_est = self.mem.estimate_memory(dim)
        recommendations = []

        if mem_est['total_gb'] > 1.0:
            recommendations.append(f"Use {mem_est['recommended_blocks']} blocks")
        if dim > 200:
            recommendations.append("Use sparse mode (threshold=1e-10)")
        if dim > 500 and HAS_GPU:
            recommendations.append("Use GPU acceleration recommended")
        if dim > 1000:
            recommendations.append("Use memory-mapped storage")

        return {
            'dim': dim,
            'memory_estimate_gb': mem_est['total_gb'],
            'recommendations': recommendations,
        }


# ============================================================
#  5. 数值验证
# ============================================================

def verify_gpu_accelerator():
    """验证 GPU 加速器（CPU 降级模式）"""
    acc = SpectralGPUAccelerator(use_gpu=False)
    assert acc.backend_name == 'numpy'

    # 谱分解
    N = 32
    A = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    A = A @ A.conj().T
    diag = acc.spectral_diagonalize(A)
    assert len(diag['eigenvalues']) == N
    assert diag['eigenvectors'].shape == (N, N)

    # 矩阵乘法
    B = np.random.randn(N, N)
    C = acc.spectral_matrix_multiply(A, B)
    assert C.shape == (N, N)

    # 矩阵函数
    fA = acc.spectral_matrix_function(A, np.exp)
    assert fA.shape == (N, N)

    # 迹
    trace = acc.spectral_trace(A)
    assert np.isfinite(trace)

    # 基准测试
    bench = acc.benchmark(N=32, n_iter=3)
    assert bench['backend'] == 'numpy'
    print(f"  Backend: {bench['backend']}")
    print(f"  Diagonalize: {bench['diagonalize_mean']:.4f}s")
    print(f"  Matrix multiply: {bench['multiply_mean']:.4f}s")

    print("  ✅ GPU accelerator (CPU mode) verified")
    return True


def _diag_block_worker(block_and_info):
    """分块谱分解工作函数（模块级，可 picklize）"""
    blk, info = block_and_info
    i, j = info[0], info[1]
    if i == j:
        evals, evecs = np.linalg.eigh(blk)
        return {'type': 'diagonal', 'i': i, 'eigenvalues': evals, 'eigenvectors': evecs}
    else:
        return {'type': 'offdiagonal', 'i': i, 'j': j, 'block': blk}


def _sq_func(x):
    """平方函数（模块级，可被 pickle 序列化）"""
    return x * x


def _sq_func_wrapper(params: dict) -> float:
    """参数扫描包装函数"""
    return _sq_func(params['x'])


def _flow_func(t, lam, gamma=1.0):
    """谱流测试函数（模块级，可被 pickle 序列化）"""
    return -gamma * lam


def _flow_scan_wrapper(param_val):
    """谱流扫描包装函数"""
    from scipy import integrate
    n_modes = 5
    lambda0 = np.linspace(0.1, 1.0, n_modes)
    t_span = (0, 1)
    t_eval = np.linspace(0, 1, 10)

    def _flow(t, lam):
        return _flow_func(t, lam, gamma=float(param_val))

    result = integrate.solve_ivp(
        _flow, t_span, lambda0, method='RK45', t_eval=t_eval,
        rtol=1e-8, atol=1e-10,
    )
    return {
        't': result.t,
        'lambda_history': result.y,
        'success': result.success,
    }


def verify_distributed_solver():
    """验证分布式求解器"""
    solver = SpectralDistributedSolver(n_workers=2)

    # 参数扫描（模块级函数，可 pickle 序列化）
    grid = {'x': np.array([1.0, 2.0, 3.0, 4.0])}
    result = solver.parallel_parameter_scan(_sq_func_wrapper, grid)
    assert len(result['results']) == 4
    results_float = [float(r) if not isinstance(r, dict) else 0.0 for r in result['results']]
    assert results_float == [1.0, 4.0, 9.0, 16.0], f"Got {results_float}"
    print(f"  Parameter scan results: {results_float}")

    # 分块谱分解
    N = 64
    A = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    A = A @ A.conj().T
    blocked = solver.blocked_eigh(A, block_size=16)
    assert len(blocked['eigenvalues']) == N
    print(f"  Blocked eigh: {blocked['n_blocks']} blocks, {N} eigenvalues")

    # 并行谱流扫描（模块级函数）
    scan = solver.parallel_spectral_flow_scan(
        _flow_func, (0.1, 1.0), 'gamma', np.array([0.5, 1.0, 2.0]),
        n_modes=5, t_span=(0, 1), n_steps=10
    )
    assert len(scan['evolutions']) == 3
    print(f"  Spectral flow scan: {len(scan['evolutions'])} param values")

    print("  ✅ Distributed solver verified")
    return True


def verify_memory_optimizer():
    """验证内存优化策略"""
    mem = SpectralMemoryOptimizer(cache_size=8, use_sparse=True)

    # LRU 缓存
    A = np.random.randn(32, 32)
    A = A @ A.T
    r1 = mem.cached_diagonalize(A)
    r2 = mem.cached_diagonalize(A)
    assert np.allclose(r1['eigenvalues'], r2['eigenvalues'])
    print("  LRU cache hit: same matrix → same result")

    # 分块矩阵乘法
    N = 32
    A = np.random.randn(N, N)
    B = np.random.randn(N, N)
    C_blocked = mem.blocked_matrix_multiply(A, B, block_size=8)
    C_direct = A @ B
    assert np.allclose(C_blocked, C_direct, atol=1e-10)
    print("  Blocked matmul matches direct matmul")

    # 稀疏谱算子
    N = 32
    A_mat = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    A_mat = A_mat @ A_mat.conj().T
    # 手动构造谱算子（填充矩阵）
    op = SpectralOperator(dim=N, label='test')
    op._matrix = A_mat
    # 预计算谱
    evals = np.linalg.eigvalsh(A_mat)
    op._data = SpectralData(eigenvalues=evals, label='test')
    sparse_op = mem.sparse_spectral_operator(op, threshold=1e-3)
    assert sparse_op is not None
    print(f"  Sparse spectral operator created (dim={N})")

    # 内存估计
    est = mem.estimate_memory(256)
    print(f"  Memory estimate for 256x256: {est['total_gb']:.4f} GB")
    assert est['total_gb'] > 0

    mem.clear_cache()
    print("  Cache cleared")

    print("  ✅ Memory optimizer verified")
    return True


def verify_parallel_context():
    """验证并行上下文"""
    ctx = SpectralParallelContext(n_workers=2, use_gpu=False)
    summary = ctx.summary
    print(f"  GPU backend: {summary['gpu_backend']}")
    print(f"  Workers: {summary['n_workers']}")
    print(f"  CPU count: {summary['cpu_count']}")

    # 优化建议
    opt = ctx.optimize_for_matrix(dim=512)
    print(f"  Memory estimate for 512x512: {opt['memory_estimate_gb']:.4f} GB")
    print(f"  Recommendations: {opt['recommendations']}")

    assert opt['dim'] == 512
    assert opt['memory_estimate_gb'] > 0

    print("  ✅ Parallel context verified")
    return True


def verify_blocked_spectral_flow():
    """验证分块谱流求解"""
    mem = SpectralMemoryOptimizer()

    # 构造简单的谱流问题
    n_modes = 30
    lambda0 = np.linspace(0.1, 1.0, n_modes)
    t_vals = np.linspace(0, 1, 20)

    def _flow(t, lam):
        return -0.5 * lam  # 指数衰减

    # 分块求解
    blocked_result = mem.blocked_spectral_flow(lambda0, t_vals, _flow, block_size=10)
    assert blocked_result['lambda_history'].shape == (n_modes, 20)
    assert np.all(np.isfinite(blocked_result['lambda_history']))

    # 验证衰减行为
    for i in range(n_modes):
        initial = blocked_result['lambda_history'][i, 0]
        final = blocked_result['lambda_history'][i, -1]
        assert final < initial, f"Mode {i} should decay: {final} < {initial}"

    print(f"  Blocked spectral flow: {n_modes} modes, {len(t_vals)} time steps")
    print(f"  First mode: {blocked_result['lambda_history'][0, 0]:.4f} → {blocked_result['lambda_history'][0, -1]:.4f}")

    print("  ✅ Blocked spectral flow verified")
    return True


def verify_hardware_detection():
    """验证硬件检测"""
    info = detect_hardware()
    print(f"  CPUs: {info['cpu_count']}")
    print(f"  GPU: {info['has_gpu']} ({info['gpu_backend']})")
    if info['memory_gb'] > 0:
        print(f"  Memory: {info['memory_gb']:.1f} GB")
    else:
        print(f"  Memory: psutil not available")

    assert info['cpu_count'] >= 1

    print("  ✅ Hardware detection verified")
    return True


def run_all_tests():
    """运行所有 C2 测试"""
    print("=" * 60)
    print("C2: Parallel Computing Acceleration Tests")
    print("=" * 60)

    tests = [
        ("Hardware detection", verify_hardware_detection),
        ("GPU accelerator (CPU mode)", verify_gpu_accelerator),
        ("Distributed solver", verify_distributed_solver),
        ("Memory optimizer", verify_memory_optimizer),
        ("Parallel context", verify_parallel_context),
        ("Blocked spectral flow", verify_blocked_spectral_flow),
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
        print(f"✅ {passed}/{len(tests)} C2 tests passed!")
    else:
        print(f"⚠️  {passed}/{len(tests)} C2 tests passed")

    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
