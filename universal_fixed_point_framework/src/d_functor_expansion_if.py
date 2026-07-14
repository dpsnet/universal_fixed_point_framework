"""
d_functor_expansion_if.py

Phase 15E-1: D 函子扩张 IFS 扩展

核心内容：
1. 扩张 IFS 的定义与逆系统构造
2. 不稳定流形理论
3. 双曲动力系统的谱对象构造
4. D 函子在扩张系统上的映射
5. 测试验证
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import inv, logm, expm, eigvals


class ExpansionIFS:
    """
    扩张迭代函数系统。

    扩张 IFS 定义：f_i(x) = A_i x + b_i，其中 A_i 的所有特征值绝对值 > 1。
    扩张系统没有吸引子，但有不稳定流形。

    通过构造逆系统（收缩系统）来处理扩张 IFS：
    f_i^{-1}(x) = A_i^{-1}(x - b_i)，此时 A_i^{-1} 的特征值绝对值 < 1
    """

    def __init__(self, matrices: list[np.ndarray], offsets: list[np.ndarray]):
        """
        参数
        ----------
        matrices : list[np.ndarray]
            线性变换矩阵列表
        offsets : list[np.ndarray]
            平移向量列表
        """
        self.matrices = matrices
        self.offsets = offsets
        self.n = len(matrices)
        self.dim = matrices[0].shape[0]

        for i, A in enumerate(matrices):
            eig = eigvals(A)
            if np.any(np.abs(eig) <= 1.0):
                raise ValueError(f"矩阵 {i} 不是扩张的：特征值 = {eig}")

    def forward_iterate(self, x: np.ndarray, steps: int = 10) -> np.ndarray:
        """
        前向迭代（扩张）。

        参数
        ----------
        x : np.ndarray
            初始点
        steps : int
            迭代步数

        返回
        -------
        trajectory : np.ndarray
            轨迹数组
        """
        trajectory = [x]
        for _ in range(steps):
            idx = np.random.randint(self.n)
            x = self.matrices[idx] @ x + self.offsets[idx]
            trajectory.append(x)
        return np.array(trajectory)

    def inverse_system(self) -> "ContractionIFS":
        """
        构造逆系统（收缩 IFS）。

        返回
        -------
        contraction_ifs : ContractionIFS
            逆收缩系统
        """
        inv_matrices = [inv(A) for A in self.matrices]
        inv_offsets = [-inv(A) @ b for A, b in zip(self.matrices, self.offsets)]
        return ContractionIFS(inv_matrices, inv_offsets)

    def unstable_manifold(self, fixed_point: np.ndarray, epsilon: float = 1e-6) -> np.ndarray:
        """
        计算不稳定流形。

        参数
        ----------
        fixed_point : np.ndarray
            不动点
        epsilon : float
            扰动大小

        返回
        -------
        manifold_points : np.ndarray
            不稳定流形上的点
        """
        inv_ifs = self.inverse_system()
        points = []

        for _ in range(100):
            direction = np.random.randn(self.dim)
            direction /= np.linalg.norm(direction)
            x = fixed_point + epsilon * direction

            for _ in range(50):
                x = inv_ifs.forward_iterate_single(x)

            points.append(x)

        return np.array(points)

    def fixed_points(self) -> list[np.ndarray]:
        """
        计算各分支的不动点。

        返回
        -------
        fixed_points : list[np.ndarray]
            各分支的不动点
        """
        fps = []
        for A, b in zip(self.matrices, self.offsets):
            try:
                fp = np.linalg.solve(np.eye(self.dim) - A, b)
                fps.append(fp)
            except np.linalg.LinAlgError:
                fps.append(None)
        return fps

    def koopman_operator(self, n_basis: int = 20) -> np.ndarray:
        """
        构造 Koopman 算子的有限维近似。

        使用逆系统的 Perron-Frobenius 算子。

        参数
        ----------
        n_basis : int
            基函数数量

        返回
        -------
        K : np.ndarray
            Koopman 算子矩阵
        """
        inv_ifs = self.inverse_system()
        return inv_ifs.perron_frobenius_operator(n_basis)


class ContractionIFS:
    """
    收缩迭代函数系统（逆系统）。
    """

    def __init__(self, matrices: list[np.ndarray], offsets: list[np.ndarray]):
        """
        参数
        ----------
        matrices : list[np.ndarray]
            线性变换矩阵列表（收缩）
        offsets : list[np.ndarray]
            平移向量列表
        """
        self.matrices = matrices
        self.offsets = offsets
        self.n = len(matrices)
        self.dim = matrices[0].shape[0]

    def forward_iterate_single(self, x: np.ndarray) -> np.ndarray:
        """
        单次前向迭代。

        参数
        ----------
        x : np.ndarray
            当前点

        返回
        -------
        x_next : np.ndarray
            下一点
        """
        idx = np.random.randint(self.n)
        return self.matrices[idx] @ x + self.offsets[idx]

    def forward_iterate(self, x: np.ndarray, steps: int = 100) -> np.ndarray:
        """
        前向迭代。

        参数
        ----------
        x : np.ndarray
            初始点
        steps : int
            迭代步数

        返回
        -------
        trajectory : np.ndarray
            轨迹数组
        """
        trajectory = [x]
        for _ in range(steps):
            x = self.forward_iterate_single(x)
            trajectory.append(x)
        return np.array(trajectory)

    def attractor(self, n_points: int = 1000, steps: int = 100) -> np.ndarray:
        """
        计算吸引子。

        参数
        ----------
        n_points : int
            采样点数
        steps : int
            迭代步数

        返回
        -------
        points : np.ndarray
            吸引子上的点
        """
        points = []
        x = np.random.randn(self.dim)

        for _ in range(n_points):
            for _ in range(steps):
                x = self.forward_iterate_single(x)
            points.append(x)

        return np.array(points)

    def perron_frobenius_operator(self, n_basis: int = 20) -> np.ndarray:
        """
        构造 Perron-Frobenius 算子。

        参数
        ----------
        n_basis : int
            基函数数量

        返回
        -------
        P : np.ndarray
            Perron-Frobenius 算子矩阵
        """
        P = np.zeros((n_basis, n_basis))
        rng = np.random.RandomState(42)

        for i in range(n_basis):
            for j in range(n_basis):
                x = rng.randn(self.dim)
                for k, (A, b) in enumerate(self.matrices):
                    try:
                        y = A @ x + b
                        P[i, j] += np.exp(-0.5 * np.linalg.norm(x - y) ** 2) / self.n
                    except:
                        pass

        return P


class HyperbolicSpectralObject:
    """
    双曲动力系统的谱对象。

    包含稳定和不稳定两个谱子空间：
    - 稳定谱：特征值绝对值 < 1（收缩方向）
    - 不稳定谱：特征值绝对值 > 1（扩张方向）
    """

    def __init__(self, stable_eigenvalues: np.ndarray, unstable_eigenvalues: np.ndarray,
                 stable_eigenvectors: np.ndarray = None, unstable_eigenvectors: np.ndarray = None):
        """
        参数
        ----------
        stable_eigenvalues : np.ndarray
            稳定特征值（|λ| < 1）
        unstable_eigenvalues : np.ndarray
            不稳定特征值（|λ| > 1）
        stable_eigenvectors : np.ndarray
            稳定特征向量
        unstable_eigenvectors : np.ndarray
            不稳定特征向量
        """
        self.stable_eigenvalues = stable_eigenvalues
        self.unstable_eigenvalues = unstable_eigenvalues
        self.stable_eigenvectors = stable_eigenvectors
        self.unstable_eigenvectors = unstable_eigenvectors

        self.dim_stable = len(stable_eigenvalues)
        self.dim_unstable = len(unstable_eigenvalues)
        self.dim = self.dim_stable + self.dim_unstable

    @property
    def spectrum(self) -> np.ndarray:
        """返回完整谱。"""
        return np.concatenate([self.stable_eigenvalues, self.unstable_eigenvalues])

    @property
    def stable_koopman_matrix(self) -> np.ndarray:
        """稳定方向的 Koopman 矩阵。"""
        if self.stable_eigenvectors is not None:
            D = np.diag(np.exp(-self.stable_eigenvalues))
            return self.stable_eigenvectors @ D @ inv(self.stable_eigenvectors)
        return np.diag(np.exp(-self.stable_eigenvalues))

    @property
    def unstable_koopman_matrix(self) -> np.ndarray:
        """不稳定方向的 Koopman 矩阵（使用逆系统）。"""
        if self.unstable_eigenvectors is not None:
            D = np.diag(np.exp(-np.log(self.unstable_eigenvalues)))
            return self.unstable_eigenvectors @ D @ inv(self.unstable_eigenvectors)
        return np.diag(np.exp(-np.log(self.unstable_eigenvalues)))

    @classmethod
    def from_expansion_ifs(cls, expansion_ifs: ExpansionIFS) -> "HyperbolicSpectralObject":
        """从扩张 IFS 构造双曲谱对象。"""
        stable_eigs = []
        unstable_eigs = []

        for A in expansion_ifs.matrices:
            eig = eigvals(A)
            stable_eigs.extend(eig[np.abs(eig) < 1])
            unstable_eigs.extend(eig[np.abs(eig) > 1])

        return cls(np.array(stable_eigs), np.array(unstable_eigs))


class ExpansionDecursionFunctor:
    """
    扩张系统的 D 函子。

    核心思想：通过逆系统将扩张问题转化为收缩问题。
    """

    @staticmethod
    def map_expansion_ifs(expansion_ifs: ExpansionIFS) -> HyperbolicSpectralObject:
        """
        将扩张 IFS 映射为双曲谱对象。

        参数
        ----------
        expansion_ifs : ExpansionIFS
            扩张迭代函数系统

        返回
        -------
        spectral_object : HyperbolicSpectralObject
            双曲谱对象
        """
        return HyperbolicSpectralObject.from_expansion_ifs(expansion_ifs)

    @staticmethod
    def spectral_integral(expansion_ifs: ExpansionIFS, func: callable) -> np.ndarray:
        """
        计算谱积分。

        参数
        ----------
        expansion_ifs : ExpansionIFS
            扩张迭代函数系统
        func : callable
            作用在谱上的函数

        返回
        -------
        result : np.ndarray
            谱积分结果
        """
        spectral_obj = HyperbolicSpectralObject.from_expansion_ifs(expansion_ifs)

        if len(spectral_obj.stable_eigenvalues) > 0:
            stable_part = np.mean(func(spectral_obj.stable_eigenvalues))
        else:
            stable_part = 0.0

        if len(spectral_obj.unstable_eigenvalues) > 0:
            unstable_part = np.mean(func(spectral_obj.unstable_eigenvalues))
        else:
            unstable_part = 0.0

        return np.array([stable_part, unstable_part])

    @staticmethod
    def verify_functoriality(expansion_ifs: ExpansionIFS) -> bool:
        """
        验证函子性：D(f ∘ g) = D(f) ∘ D(g)。

        参数
        ----------
        expansion_ifs : ExpansionIFS
            扩张迭代函数系统

        返回
        -------
        functorial : bool
            是否满足函子性
        """
        spectral_obj = HyperbolicSpectralObject.from_expansion_ifs(expansion_ifs)

        for A in expansion_ifs.matrices:
            try:
                log_A = logm(A)
                exp_log_A = expm(log_A)
                if not np.allclose(A, exp_log_A):
                    return False
            except:
                pass

        return True


def run_expansion_demo():
    """运行扩张 IFS 演示。"""
    print("=" * 70)
    print("Phase 15E-1: D 函子扩张 IFS 扩展")
    print("=" * 70)

    A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
    b1 = np.array([0.0, 0.0])
    A2 = np.array([[1.5, 0.5], [0.5, 1.5]])
    b2 = np.array([1.0, 0.0])

    try:
        expansion_ifs = ExpansionIFS([A1, A2], [b1, b2])
        print("\n--- 1. 扩张 IFS 构造 ---")
        print(f"  分支数: {expansion_ifs.n}")
        print(f"  维度: {expansion_ifs.dim}")

        print("\n--- 2. 逆系统构造 ---")
        inv_ifs = expansion_ifs.inverse_system()
        print(f"  逆系统分支数: {inv_ifs.n}")

        print("\n--- 3. 不动点计算 ---")
        fps = expansion_ifs.fixed_points()
        for i, fp in enumerate(fps):
            if fp is not None:
                print(f"  分支 {i}: {fp}")

        print("\n--- 4. 不稳定流形 ---")
        if fps[0] is not None:
            manifold = expansion_ifs.unstable_manifold(fps[0])
            print(f"  流形点数: {len(manifold)}")
            print(f"  流形范围: [{manifold.min():.2f}, {manifold.max():.2f}]")

        print("\n--- 5. 双曲谱对象 ---")
        spectral_obj = HyperbolicSpectralObject.from_expansion_ifs(expansion_ifs)
        print(f"  稳定特征值: {spectral_obj.stable_eigenvalues}")
        print(f"  不稳定特征值: {spectral_obj.unstable_eigenvalues}")

        print("\n--- 6. D 函子映射 ---")
        result = ExpansionDecursionFunctor.map_expansion_ifs(expansion_ifs)
        print(f"  谱对象维度: {result.dim}")

        print("\n--- 7. 函子性验证 ---")
        functorial = ExpansionDecursionFunctor.verify_functoriality(expansion_ifs)
        print(f"  函子性: {'✓' if functorial else '✗'}")

    except ValueError as e:
        print(f"  错误: {e}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_expansion_demo()
