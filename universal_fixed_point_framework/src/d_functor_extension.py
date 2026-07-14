"""
d_functor_extension.py

Phase 15B-1/2: D 函子定义域扩展 + Freyd 放宽条件构造

核心内容：
1. D 函子扩展到投影值谱测度（PVM）
2. 连续谱对象的 D 函子映射
3. Freyd 广义伴随函子定理放宽条件
4. 弱伴随关系验证
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm, logm

from rec_category import RecObject, RecMorphism
from spec_category import PositiveSpectralObject, SpectralMorphism
from decursion_functor import DecursionFunctor


class ProjectionValuedMeasure:
    """
    投影值谱测度（PVM）表示。

    对自伴算子 A，PVM E 满足：
    - E(∅) = 0, E(R) = I
    - E(Δ₁ ∩ Δ₂) = E(Δ₁)E(Δ₂)
    - A = ∫ λ dE(λ)
    """

    def __init__(self, eigenvalues: np.ndarray, eigenvectors: np.ndarray):
        """
        由离散谱构造 PVM。

        参数
        ----------
        eigenvalues : np.ndarray
            特征值数组（已排序）
        eigenvectors : np.ndarray
            特征向量矩阵，列向量为特征向量
        """
        self.eigenvalues = np.sort(eigenvalues)
        self.eigenvectors = eigenvectors
        self.n = len(eigenvalues)

    def project(self, interval: tuple[float, float]) -> np.ndarray:
        """
        计算区间 [a, b] 上的投影算子 E([a,b])。

        返回
        -------
        P : np.ndarray
            投影矩阵，形状 (n, n)
        """
        a, b = interval
        mask = (self.eigenvalues >= a) & (self.eigenvalues <= b)
        P = np.zeros((self.n, self.n))
        for i in np.where(mask)[0]:
            v = self.eigenvectors[:, i:i+1]
            P += v @ v.conj().T
        return P

    def spectral_integral(self, func: callable) -> np.ndarray:
        """
        计算谱积分 ∫ f(λ) dE(λ)。

        参数
        ----------
        func : callable
            作用在特征值上的函数

        返回
        -------
        A : np.ndarray
            ∫ f(λ) dE(λ) 的矩阵表示
        """
        A = np.zeros((self.n, self.n), dtype=complex)
        for i in range(self.n):
            lam = self.eigenvalues[i]
            v = self.eigenvectors[:, i:i+1]
            A += func(lam) * (v @ v.conj().T)
        return np.real_if_close(A)


class ContinuousSpectralObject:
    """
    连续谱对象：包含 PVM 和谱测度信息。

    与 PositiveSpectralObject 的区别：
    - PositiveSpectralObject：有限维离散谱
    - ContinuousSpectralObject：连续/混合谱，用 PVM 表示
    """

    def __init__(self, pvm: ProjectionValuedMeasure, spectral_type: str = "continuous"):
        """
        参数
        ----------
        pvm : ProjectionValuedMeasure
            投影值谱测度
        spectral_type : str
            谱类型："discrete", "continuous", "singular_continuous", "mixed"
        """
        self.pvm = pvm
        self.spectral_type = spectral_type
        self.dim = pvm.n

    @property
    def spectrum(self) -> np.ndarray:
        """返回离散近似谱。"""
        return self.pvm.eigenvalues

    @property
    def operator_A(self) -> np.ndarray:
        """返回 A = ∫ λ dE(λ)。"""
        return self.pvm.spectral_integral(lambda x: x)

    @property
    def koopman_matrix(self) -> np.ndarray:
        """返回 K = exp(-A) = ∫ exp(-λ) dE(λ)。"""
        return self.pvm.spectral_integral(lambda x: np.exp(-x))

    @classmethod
    def from_positive_spectral_object(cls, E: PositiveSpectralObject) -> "ContinuousSpectralObject":
        """从有限维正谱对象构造连续谱对象。"""
        eigenvalues, eigenvectors = np.linalg.eigh(E.operator_A)
        pvm = ProjectionValuedMeasure(eigenvalues, eigenvectors)
        return cls(pvm, spectral_type="discrete")

    @classmethod
    def from_continuous_spectrum(cls, n: int, spectral_type: str = "continuous",
                                seed: int = 42) -> "ContinuousSpectralObject":
        """
        生成连续谱对象。

        参数
        ----------
        n : int
            离散化维度
        spectral_type : str
            谱类型
        seed : int
            随机种子
        """
        rng = np.random.RandomState(seed)

        if spectral_type == "continuous":
            eigenvalues = np.sort(rng.uniform(0, 1, n))
        elif spectral_type == "singular_continuous":
            eigenvalues = np.sort(rng.power(2, n))
        elif spectral_type == "mixed":
            n_discrete = n // 2
            n_cont = n - n_discrete
            discrete_eig = np.array([0.1, 0.3, 0.5])[:min(n_discrete, 3)]
            cont_eig = np.sort(rng.uniform(0.6, 1.0, n_cont))
            eigenvalues = np.sort(np.concatenate([discrete_eig, cont_eig]))
        else:
            eigenvalues = np.sort(np.linspace(0.1, 1.0, n))

        eigenvectors = np.linalg.qr(rng.randn(n, n))[0]
        pvm = ProjectionValuedMeasure(eigenvalues, eigenvectors)
        return cls(pvm, spectral_type=spectral_type)


class ExtendedDecursionFunctor(DecursionFunctor):
    """
    扩展的 D 函子：支持连续谱对象和 PVM。

    核心扩展：
    1. 对象映射：D(R) 可返回 ContinuousSpectralObject（含 PVM）
    2. 态射映射：支持连续谱态射
    3. 谱积分：∫ f(λ) dE(λ) 的数值实现
    """

    @staticmethod
    def map_object_continuous(R: RecObject) -> ContinuousSpectralObject:
        """
        将递归系统 R 映射为连续谱对象（含 PVM）。

        实现：
        1. 计算 Koopman 矩阵 K_R；
        2. 特征分解得 PVM；
        3. 返回 ContinuousSpectralObject。
        """
        K = R.koopman_matrix()
        eigenvalues, eigenvectors = np.linalg.eigh(K)
        eigenvalues = np.clip(eigenvalues, 1e-10, 1.0)
        A_eigenvalues = -np.log(eigenvalues)

        pvm = ProjectionValuedMeasure(A_eigenvalues, eigenvectors)
        return ContinuousSpectralObject(pvm, spectral_type="discrete")

    @staticmethod
    def spectral_integral(R: RecObject, func: callable) -> np.ndarray:
        """
        计算谱积分 ∫ f(A) dE_A = ∫ f(λ) dE(λ)。

        参数
        ----------
        R : RecObject
            递归系统
        func : callable
            作用在谱上的函数

        返回
        -------
        integral : np.ndarray
            谱积分的矩阵表示
        """
        K = R.koopman_matrix()
        eigenvalues, eigenvectors = np.linalg.eigh(K)
        eigenvalues = np.clip(eigenvalues, 1e-10, 1.0)
        A_eigenvalues = -np.log(eigenvalues)

        n = len(A_eigenvalues)
        result = np.zeros((n, n), dtype=complex)
        for i in range(n):
            lam = A_eigenvalues[i]
            v = eigenvectors[:, i:i+1]
            result += func(lam) * (v @ v.conj().T)
        return np.real_if_close(result)

    @staticmethod
    def spectral_integral_direct(R: RecObject, func: callable) -> np.ndarray:
        """
        直接计算谱积分（用于验证）：通过构造 A 后计算 f(A)。

        参数
        ----------
        R : RecObject
            递归系统
        func : callable
            作用在谱上的函数

        返回
        -------
        integral : np.ndarray
            f(A) 的矩阵表示
        """
        K = R.koopman_matrix()
        eigenvalues, eigenvectors = np.linalg.eigh(K)
        eigenvalues = np.clip(eigenvalues, 1e-10, 1.0)
        A_eigenvalues = -np.log(eigenvalues)

        A_diag = np.diag(A_eigenvalues)
        A = eigenvectors @ A_diag @ eigenvectors.conj().T

        return func(A)


class FreydRelaxation:
    """
    Freyd 广义伴随函子定理放宽条件构造。

    标准 Freyd 定理要求：
    1. D 保持极限（连续）
    2. D 满足解集条件

    放宽条件（适用于有限维原型）：
    1. D 保持有限极限（有限连续）
    2. 近似解集条件（ε-解集）
    3. 弱伴随关系（η, ε 为近似自然变换）
    """

    def __init__(self):
        self.D = DecursionFunctor()

    def preserves_finite_limits(self, R1: RecObject, R2: RecObject) -> bool:
        """
        验证 D 保持有限极限（乘积）。

        有限极限保持：D(R1 × R2) ≅ D(R1) × D(R2)
        """
        product_state_space = np.kron(R1.state_space, R2.state_space)
        product_evolution = np.kron(R1.evolution, R2.evolution)
        R_product = RecObject(
            state_space=product_state_space,
            evolution=product_evolution,
            metadata={"type": "product"}
        )

        D_R1 = self.D.map_object(R1)
        D_R2 = self.D.map_object(R2)
        D_R_product = self.D.map_object(R_product)

        expected_A = np.kron(D_R1.operator_A, np.eye(D_R2.dim)) + np.kron(np.eye(D_R1.dim), D_R2.operator_A)

        return np.allclose(D_R_product.operator_A, expected_A, atol=1e-8)

    def epsilon_solution_set(self, E: PositiveSpectralObject, epsilon: float = 1e-6) -> bool:
        """
        验证近似解集条件。

        对任意谱对象 E，存在 Rec 对象 R 使得 D(R) 与 E 的距离 < ε。
        """
        A = E.operator_A
        K = expm(-A)
        n = E.dim
        state_space = np.eye(n)

        R = RecObject(
            state_space=state_space,
            evolution=K,
            metadata={"origin": "epsilon_solution"}
        )

        D_R = self.D.map_object(R)

        distance = np.linalg.norm(D_R.operator_A - A) / np.linalg.norm(A) if np.linalg.norm(A) > 0 else 0
        return distance < epsilon

    def weak_adjoint_pair(self, R: RecObject, E: PositiveSpectralObject,
                          epsilon: float = 1e-6) -> dict[str, bool]:
        """
        验证弱伴随关系。

        弱三角恒等式：
        1. ‖D(η_R) ∘ ε_{D(R)} - id_{D(R)}‖ < ε
        2. ‖R(ε_E) ∘ η_{R(E)} - id_{R(E)}‖ < ε
        """
        from decursion_functor import unit, counit, right_adjoint_on_object

        eta_R = unit(R)
        D_eta_R = self.D.map_morphism(eta_R)

        D_R = self.D.map_object(R)
        eps_D_R = counit(D_R)

        from spec_category import compose_spectral_morphisms as compose_spec
        left_triangle = compose_spec(D_eta_R, eps_D_R)
        left_error = np.linalg.norm(left_triangle.matrix - np.eye(D_R.dim))

        R_E = right_adjoint_on_object(E)
        eta_R_E = unit(R_E)

        eps_E = counit(E)
        from decursion_functor import right_adjoint_on_morphism
        R_eps_E = right_adjoint_on_morphism(eps_E)

        from rec_category import compose_morphisms as compose_rec
        right_triangle = compose_rec(R_eps_E, eta_R_E)
        right_error = np.linalg.norm(right_triangle.map - np.eye(R_E.n_points))

        return {
            "left_triangle_ok": left_error < epsilon,
            "right_triangle_ok": right_error < epsilon,
            "left_error": float(left_error),
            "right_error": float(right_error),
        }

    def verify_freyd_conditions(self, R: RecObject, E: PositiveSpectralObject,
                                epsilon: float = 1e-6) -> dict[str, bool]:
        """
        验证 Freyd 放宽条件的完整集合。

        返回
        -------
        results : dict
            包含各条件的验证结果
        """
        print("\n[测试] Freyd 放宽条件验证")

        result1 = self.preserves_finite_limits(R, R)
        print(f"  [1] 保持有限极限: {result1}")

        result2 = self.epsilon_solution_set(E, epsilon)
        print(f"  [2] ε-解集条件 (ε={epsilon}): {result2}")

        result3 = self.weak_adjoint_pair(R, E, epsilon)
        print(f"  [3] 弱伴随关系: 左三角={result3['left_triangle_ok']}, 右三角={result3['right_triangle_ok']}")

        all_ok = result1 and result2 and result3["left_triangle_ok"] and result3["right_triangle_ok"]
        print(f"  结论: Freyd 放宽条件验证 {'通过 ✓' if all_ok else '未通过 ✗'}")

        return {
            "preserves_finite_limits": result1,
            "epsilon_solution_set": result2,
            "weak_adjoint_pair": result3,
            "all_conditions_met": all_ok,
        }


def run_d_functor_extension_demo():
    """运行 D 函子扩展演示。"""
    print("=" * 70)
    print("Phase 15B-1/2: D 函子定义域扩展 + Freyd 放宽条件")
    print("=" * 70)

    n = 4
    rng = np.random.RandomState(42)
    state_space = np.eye(n)
    evolution = rng.rand(n, n)
    evolution = evolution / np.sum(evolution, axis=1, keepdims=True)

    R = RecObject(
        state_space=state_space,
        evolution=evolution,
        metadata={"name": "test_rec_object"}
    )

    E = PositiveSpectralObject(
        operator_A=np.diag(np.linspace(0.1, 1.0, n))
    )

    print("\n1. D 函子扩展到 PVM")
    ext_D = ExtendedDecursionFunctor()
    cont_E = ext_D.map_object_continuous(R)
    print(f"   连续谱对象维度: {cont_E.dim}")
    print(f"   谱类型: {cont_E.spectral_type}")
    print(f"   A 算子范数: {np.linalg.norm(cont_E.operator_A):.4f}")

    print("\n2. 谱积分演示")
    f = lambda x: x ** 2
    integral = ext_D.spectral_integral(R, f)
    print(f"   ∫ A² dE(A) 的迹: {np.trace(integral):.4f}")

    print("\n3. Freyd 放宽条件")
    freyd = FreydRelaxation()
    freyd.verify_freyd_conditions(R, E)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_d_functor_extension_demo()
