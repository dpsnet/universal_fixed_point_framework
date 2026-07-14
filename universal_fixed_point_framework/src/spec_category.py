"""
spec_category.py

谱范畴 (Spec) 的最小原型实现。

对象：PositiveSpectralObject，包含有限维 Hilbert 空间、正半定谱算子 A、谱集合。
态射：SpectralMorphism，满足谱交织条件 T A_1 = A_2 T 的有界线性算子。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
import numpy as np
from scipy.linalg import expm


@dataclass
class PositiveSpectralObject:
    """
    谱范畴 Spec 的对象（原型阶段限制为正半定谱算子）。

    参数
    ----------
    operator_A : np.ndarray
        Hermitian 正半定矩阵，形状 (n, n)，其中 n = dim(H)。
    hilbert_space_basis : np.ndarray, optional
        标准正交基，形状 (n, n)。若未提供，默认取单位矩阵。
    spectrum : np.ndarray, optional
        预计算的谱 σ(A)。若未提供，在构造时自动计算。

    约定
    ----
    - A 的特征值按升序排列：spectrum[0] <= spectrum[1] <= ... <= spectrum[n-1]。
    - 0 特征值允许存在，对应不变子空间。
    """
    operator_A: np.ndarray
    hilbert_space_basis: np.ndarray | None = None
    spectrum: np.ndarray | None = None

    def __post_init__(self):
        n = self.operator_A.shape[0]
        if self.operator_A.shape != (n, n):
            raise ValueError("operator_A 必须是方阵")
        if not np.allclose(self.operator_A, self.operator_A.conj().T):
            raise ValueError("operator_A 必须是 Hermitian 矩阵")
        if self.hilbert_space_basis is None:
            self.hilbert_space_basis = np.eye(n)
        if self.spectrum is None:
            self.spectrum = np.linalg.eigvalsh(self.operator_A)
        self.spectrum = np.sort(self.spectrum)
        if np.any(self.spectrum < -1e-10):
            raise ValueError("operator_A 必须是正半定矩阵")
        # 将微小负特征值截断为 0
        self.spectrum = np.where(self.spectrum < 1e-10, 0.0, self.spectrum)

    @property
    def dim(self) -> int:
        return self.operator_A.shape[0]

    @property
    def koopman_matrix(self) -> np.ndarray:
        """
        返回与 A 对应的 Koopman 算子矩阵：
            K = exp(-A)
        特征值满足 0 < λ_i = exp(-μ_i) <= 1。
        """
        return expm(-self.operator_A)

    @classmethod
    def from_koopman(
        cls,
        koopman_matrix: np.ndarray,
        tol: float = 1e-10,
    ) -> PositiveSpectralObject:
        """
        由 Koopman 算子 K 构造正谱对象，其中 A = -log(K)。

        实现策略（按优先级）：
        1. 优先尝试特征分解（K 可对角化且特征值在 (0,1] 时）；
        2. 退化为 scipy.linalg.logm（处理不可对角化或复特征值情形）；
        3. 最终取 A ← (A + A^†)/2 保证 Hermitian 性。

        注：logm 适用于任何可逆矩阵，但不可对角化时实部需单独提取。
        """
        n = koopman_matrix.shape[0]
        if koopman_matrix.shape != (n, n):
            raise ValueError("koopman_matrix 必须是方阵")

        # 策略 1：尝试特征分解
        eigenvalues, eigenvectors = np.linalg.eig(koopman_matrix)
        ev_real = np.real(eigenvalues)
        ev_clipped = np.clip(ev_real, 0.0, 1.0)
        ev_imag_ok = np.all(np.abs(np.imag(eigenvalues)) < tol)
        ev_range_ok = np.all(ev_real > -tol) and np.all(ev_real < 1.0 + tol)
        ev_pos = np.all(ev_real > tol)

        if ev_imag_ok and ev_range_ok and ev_pos:
            # 特征分解路径：矩阵可对角化且特征值良好
            log_ev = -np.log(ev_clipped)
            A = eigenvectors @ np.diag(log_ev) @ np.linalg.inv(eigenvectors)
        else:
            # 策略 2：用 logm 处理不可对角化/复特征值情形
            # logm 返回 -log(K) 的主支
            from scipy.linalg import logm
            try:
                A = -logm(koopman_matrix)
            except Exception:
                # 如果 logm 失败（例如 K 奇异），取对称部分的特征分解
                K_sym = 0.5 * (koopman_matrix + koopman_matrix.T)
                ev_sym = np.linalg.eigvalsh(K_sym)
                ev_sym = np.clip(ev_sym, tol, 1.0)
                log_ev_sym = -np.log(ev_sym)
                A = K_sym @ np.diag(log_ev_sym) @ np.linalg.inv(K_sym)

        # 保证 Hermitian 性：谱对象的算子必须是自伴的
        A = 0.5 * (A + A.conj().T)
        return cls(operator_A=A)


@dataclass
class SpectralMorphism:
    """
    谱范畴 Spec 的态射 T: source -> target。

    参数
    ----------
    source, target : PositiveSpectralObject
    matrix : np.ndarray
        有界线性算子 T: H_source -> H_target，形状 (n_target, n_source)。
    intertwining_mode : Literal["strict", "weak"]
        "strict" 要求 T A_source = A_target T（原型阶段默认）。
        "weak" 仅要求保持谱测度（原型阶段不实现，仅预留接口）。
    """
    source: PositiveSpectralObject
    target: PositiveSpectralObject
    matrix: np.ndarray
    intertwining_mode: Literal["strict", "weak"] = "strict"

    def __post_init__(self):
        expected_shape = (self.target.dim, self.source.dim)
        if self.matrix.shape != expected_shape:
            raise ValueError(
                f"matrix 形状应为 {expected_shape}，实际为 {self.matrix.shape}"
            )
        if self.intertwining_mode not in {"strict", "weak"}:
            raise ValueError("intertwining_mode 必须是 'strict' 或 'weak'")

    def apply(self, v: np.ndarray) -> np.ndarray:
        """将态射作用于向量 v。"""
        return self.matrix @ v

    def is_valid(self, tol: float = 1e-10) -> bool:
        """
        验证是否满足谱交织条件。
        strict 模式：T A_source = A_target T
        weak 模式：T 将 source 的特征向量近似映射到 target 的特征向量，
                  即不要求精确交换，但要求保持谱对应关系。
        """
        if self.intertwining_mode == "strict":
            residual = (
                self.matrix @ self.source.operator_A
                - self.target.operator_A @ self.matrix
            )
            return np.linalg.norm(residual, ord="fro") < tol
        else:
            return self._is_valid_weak(tol=tol)

    def _is_valid_weak(self, tol: float = 1e-10, eigenvalue_tol: float = 1e-6) -> bool:
        """
        weak 交织条件的离散实现。

        对 source 的每个特征值 μ，将 source 的 μ 特征空间投影 P_src(μ) 经 T 映射后，
        要求像完全落在 target 的 μ 特征空间 P_tgt(μ) 中。即验证
            ||T P_src(μ) - P_tgt(μ) T P_src(μ)||_F < tol
        对所有 μ 成立。
        """
        A_src = self.source.operator_A
        A_tgt = self.target.operator_A
        T = self.matrix

        lam_src, V_src = np.linalg.eigh(A_src)
        lam_tgt, V_tgt = np.linalg.eigh(A_tgt)

        # 按特征值分组（考虑数值容差）
        src_values = np.unique(np.round(lam_src / eigenvalue_tol) * eigenvalue_tol)

        for mu in src_values:
            # source 的 μ 特征空间投影
            indices_src = np.where(np.abs(lam_src - mu) < eigenvalue_tol)[0]
            if len(indices_src) == 0:
                continue
            P_src = V_src[:, indices_src] @ V_src[:, indices_src].T

            # target 的 μ 特征空间投影
            indices_tgt = np.where(np.abs(lam_tgt - mu) < eigenvalue_tol)[0]
            if len(indices_tgt) == 0:
                # source 有 μ 而 target 没有，weak 条件要求该子空间被映射到零
                if np.linalg.norm(T @ P_src, ord="fro") > tol:
                    return False
                continue
            P_tgt = V_tgt[:, indices_tgt] @ V_tgt[:, indices_tgt].T

            residual = T @ P_src - P_tgt @ T @ P_src
            if np.linalg.norm(residual, ord="fro") > tol:
                return False
        return True


def is_morphism(
    matrix: np.ndarray,
    source: PositiveSpectralObject,
    target: PositiveSpectralObject,
    mode: Literal["strict", "weak"] = "strict",
    tol: float = 1e-10,
) -> bool:
    """便捷函数：判断给定矩阵是否为合法的 SpectralMorphism。"""
    morph = SpectralMorphism(
        source=source, target=target, matrix=matrix, intertwining_mode=mode
    )
    return morph.is_valid(tol=tol)


def _spectral_objects_equal(
    a: PositiveSpectralObject, b: PositiveSpectralObject, tol: float = 1e-10
) -> bool:
    """
    判断两个 Spec 对象是否足够接近，以允许态射复合。

    范畴论上，复合 V ∘ U 要求 U.target 与 V.source 是同一个对象。
    在离散原型中允许等价的不同实例，但等价必须同时检查：
    1. Hilbert 空间维数一致；
    2. 谱算子 A 一致（数值容差内）。
    """
    if a is b:
        return True
    if a.dim != b.dim:
        return False
    return np.allclose(a.operator_A, b.operator_A, atol=tol)


def compose_spectral_morphisms(
    g: SpectralMorphism, f: SpectralMorphism
) -> SpectralMorphism:
    """
    复合态射 g ∘ f: source(f) -> target(g)。

    范畴论要求：复合仅在 f.target 与 g.source 是同一个对象（或等价实例）时有定义。
    等价性同时检查空间维数与谱算子 A，避免仅因维数相同而误认为对象相等。
    """
    if not _spectral_objects_equal(f.target, g.source):
        raise ValueError(
            "f.target 与 g.source 不是同一个 PositiveSpectralObject，"
            "且其维数或谱算子 A 不一致"
        )
    composed_matrix = g.matrix @ f.matrix
    return SpectralMorphism(
        source=f.source,
        target=g.target,
        matrix=composed_matrix,
        intertwining_mode=f.intertwining_mode,
    )


def identity_spectral_morphism(E: PositiveSpectralObject) -> SpectralMorphism:
    """返回谱对象 E 上的单位态射。"""
    return SpectralMorphism(
        source=E,
        target=E,
        matrix=np.eye(E.dim),
    )


def spectral_embedding_matrix(
    source_dim: int, target_dim: int
) -> np.ndarray:
    """
    辅助函数：构造从低维谱空间嵌入到高维谱空间的平凡嵌入矩阵。
    例如 source_dim=2, target_dim=4 时返回 [[1,0],[0,1],[0,0],[0,0]]。
    """
    T = np.zeros((target_dim, source_dim))
    k = min(source_dim, target_dim)
    T[:k, :k] = np.eye(k)
    return T
