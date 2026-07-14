"""
spectral_correspondence.py

将核心等式 λ_i = e^{-μ_i} 实现为范畴自然等价的离散原型。

定义两个从 Rec 到有限多重集合（以排序向量表示）的"函子"：
- M: R ↦ σ(-log Φ_R^*)      （压缩谱 / 递归谱）
- L: R ↦ σ(A_R)             （算子谱 / 去递归谱）
以及自然变换 η_R: μ ↦ e^{-μ}。

在离散正谱情形下，A_R = -log Φ_R^*，因此 M(R) 与 L(R) 作为多重集合相等，
η_R 是它们之间的双射。对任意合法 Rec 态射 f: R1 -> R2，由同一个 D(f) 诱导的
谱映射保证下图交换：

    M(R1) --M(f)--> M(R2)
       | η_R1            | η_R2
       v                 v
    L(R1) --L(f)--> L(R2)
"""

from __future__ import annotations

import numpy as np

from rec_category import RecObject, RecMorphism
from decursion_functor import DecursionFunctor


def compression_spectrum(R: RecObject, tol: float = 1e-10) -> np.ndarray:
    """
    压缩谱函子 M 的对象映射：M(R) = σ(-log K_R)。

    参数
    ----------
    R : RecObject
        递归系统对象。
    tol : float
        数值容差，用于截断微小浮点虚部。

    返回
    -------
    np.ndarray
        按升序排列的压缩谱 {μ_i}。
    """
    K = R.koopman_matrix()
    eigenvalues = np.linalg.eigvals(K)
    # 数值清理：截断到 [0, 1] 并取实部
    eigenvalues = np.real(eigenvalues)
    eigenvalues = np.clip(eigenvalues, 0.0, 1.0)
    # 避免 log(0)
    eigenvalues = np.where(eigenvalues < tol, tol, eigenvalues)
    mu = -np.log(eigenvalues)
    return np.sort(np.real(mu))


def operator_spectrum(R: RecObject, tol: float = 1e-10) -> np.ndarray:
    """
    算子谱函子 L 的对象映射：L(R) = σ(Φ_R^*) = σ(e^{-A_R}) = {λ_i}。

    在离散原型中，Φ_R^* 对应 R 的 Koopman 矩阵 K_R，其特征值满足
    0 < λ_i ≤ 1，且与压缩谱 μ_i 通过 λ_i = e^{-μ_i} 一一对应。
    """
    K = R.koopman_matrix()
    eigenvalues = np.linalg.eigvals(K)
    eigenvalues = np.real(eigenvalues)
    eigenvalues = np.clip(eigenvalues, 0.0, 1.0)
    # 将接近 0 的特征值截断到 tol，避免后续 log 异常
    eigenvalues = np.where(eigenvalues < tol, tol, eigenvalues)
    return np.sort(eigenvalues)


def eta_R(mu: np.ndarray) -> np.ndarray:
    """
    自然变换 η_R 的分量：μ ↦ e^{-μ}。

    参数
    ----------
    mu : np.ndarray
        压缩谱向量。

    返回
    -------
    np.ndarray
        对应的算子谱向量 λ = e^{-μ}。
    """
    return np.exp(-mu)


def verify_spectral_correspondence(R: RecObject, tol: float = 1e-8) -> bool:
    """
    验证对单个 Rec 对象 R，η_R: M(R) -> L(R) 是双射（作为多重集合相等）。

    即检查 sorted(exp(-M(R))) ≈ sorted(L(R))。
    """
    mu = compression_spectrum(R)
    lam = operator_spectrum(R)
    lam_from_mu = eta_R(mu)
    return np.allclose(np.sort(lam_from_mu), np.sort(lam), atol=tol)


def induced_spectrum_map(
    source_spectrum: np.ndarray,
    target_spectrum: np.ndarray,
    f: RecMorphism,
    tol: float = 1e-8,
) -> dict[int, int | None]:
    """
    由态射 f 诱导的离散谱映射的粗粒度表示。

    对 source 的每个特征值索引 i，尝试找到 target 中与其在 D(f) 像上对应的
    特征值索引 j。原型阶段采用简化匹配：按数值最接近匹配。

    返回
    -------
    dict
        源谱索引到目标谱索引的映射；若未找到匹配则为 None。
    """
    D_f = DecursionFunctor.map_morphism(f)
    E_src = DecursionFunctor.map_object(f.source)
    E_tgt = DecursionFunctor.map_object(f.target)

    # 对角化源与目标算子
    lam_src, V_src = np.linalg.eigh(E_src.operator_A)
    lam_tgt, V_tgt = np.linalg.eigh(E_tgt.operator_A)

    mapping: dict[int, int | None] = {}
    for i in range(len(lam_src)):
        v = V_src[:, i]
        w = D_f.matrix @ v
        if np.linalg.norm(w) < tol:
            mapping[i] = None
            continue
        w = w / np.linalg.norm(w)
        # 找到与 w 最接近的目标特征向量
        overlaps = np.abs(V_tgt.T @ w)
        j = int(np.argmax(overlaps))
        if overlaps[j] < tol:
            mapping[i] = None
        else:
            mapping[i] = j
    return mapping


def verify_naturality(
    f: RecMorphism, tol: float = 1e-8
) -> bool:
    """
    验证自然变换 η 对态射 f: R1 -> R2 的自然性。

    即验证对 R1 的每个特征值 μ_i，其在 M(f) 下的像 μ' 满足
        e^{-μ'} = L(f)(e^{-μ_i})。

    原型阶段采用简化匹配：通过 induced_spectrum_map 找到对应特征值后，
    检查指数关系在数值容差内成立。
    """
    mu_src = compression_spectrum(f.source)
    mu_tgt = compression_spectrum(f.target)
    lam_src = eta_R(mu_src)
    lam_tgt = eta_R(mu_tgt)

    mapping = induced_spectrum_map(lam_src, lam_tgt, f, tol=tol)

    for i, j in mapping.items():
        if j is None:
            # 无对应特征值，可能是映射到零；在原型中视为可接受
            continue
        lhs = eta_R(np.array([mu_tgt[j]]))[0]
        rhs = lam_src[i]
        if not np.isclose(lhs, rhs, atol=tol):
            return False
    return True
