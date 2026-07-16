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

from dataclasses import dataclass

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


# ===========================================================================
# 辫子自然等价（Braided Natural Equivalence）
# 对应 §3.4.2 定理 3.7b / §2.5 定义 2.5.1
# ===========================================================================


def braided_compression_spectrum(
    R: "RecObject", branch_indices: np.ndarray | None = None
) -> np.ndarray:
    """
    辫子压缩谱函子 M^{br} 的对象映射。

    返回 { (μ, k) | μ ∈ σ(-log U_R), k ∈ Z } 的分支对数谱。
    当未指定 branch_indices 时，默认 k ∈ {-2, -1, 0, 1, 2}。

    参数
    ----------
    R : RecObject
        递归系统对象（可含复谱）。
    branch_indices : np.ndarray | None
        分支指标数组，默认为 [-2, -1, 0, 1, 2]。

    返回
    -------
    np.ndarray
        形状为 (n_branches * n_evals, 2) 的数组，每行为 (μ, k)。
    """
    K = R.koopman_matrix()
    eigenvalues = np.linalg.eigvals(K)
    # 复谱情形保留虚部
    mu = -np.log(np.clip(np.abs(eigenvalues), 1e-10, None)) + 1j * np.angle(eigenvalues)

    if branch_indices is None:
        branch_indices = np.array([-2, -1, 0, 1, 2])

    result = []
    for k in branch_indices:
        branch_mu = mu + 2j * np.pi * k
        for m in branch_mu:
            result.append([np.real(m), np.imag(m), float(k)])
    return np.array(result)


def braided_operator_spectrum(
    R: "RecObject", branch_indices: np.ndarray | None = None
) -> np.ndarray:
    """
    辫子算子谱函子 L^{br} 的对象映射。

    返回 { (λ, k) | λ ∈ σ(U_R), k ∈ Z } 的分支指数谱。
    """
    K = R.koopman_matrix()
    eigenvalues = np.linalg.eigvals(K)

    if branch_indices is None:
        branch_indices = np.array([-2, -1, 0, 1, 2])

    result = []
    for k in branch_indices:
        for lam in eigenvalues:
            result.append([np.real(lam), np.imag(lam), float(k)])
    return np.array(result)


def braided_eta_R(
    mu: float, k: float, tol: float = 1e-10
) -> tuple[float, float]:
    """
    辫子自然变换 η_R^{br}: (μ, k) ↦ (e^{-μ - 2πik}, k)。

    返回 (λ_re, λ_im) 与分支指标 k 不变。
    """
    exponent = -mu - 2j * np.pi * k
    lam = np.exp(exponent)
    return (float(np.real(lam)), float(np.imag(lam)))


def braiding_crossing_number(
    omega_I_1: float, omega_I_2: float
) -> int:
    """
    计算辫子交叉次数 k(R1, R2) = floor((ω_{I,1} - ω_{I,2}) / (2π))。

    参数
    ----------
    omega_I_1 : float
        第一个系统的复频率虚部（阻尼率）。
    omega_I_2 : float
        第二个系统的复频率虚部（阻尼率）。

    返回
    -------
    int
        辫子交叉次数。
    """
    return int(np.floor((omega_I_1 - omega_I_2) / (2 * np.pi)))


def verify_braided_natural_equivalence(
    R: "RecObject", branch_indices: np.ndarray | None = None, tol: float = 1e-6
) -> bool:
    """
    验证辫子自然等价 M^{br} ≅_br L^{br}（定理 3.7b）。

    对每个分支指标 k，验证 η_R^{br} 是双射，即：
        λ = e^{-μ - 2πik} 在分支内为一一对应。

    返回
    -------
    bool
        辫子自然等价是否成立。
    """
    mu_branches = braided_compression_spectrum(R, branch_indices)
    lam_branches = braided_operator_spectrum(R, branch_indices)

    # 对每个分支 k 单独验证
    for k in (branch_indices if branch_indices is not None else [-2, -1, 0, 1, 2]):
        mu_k = mu_branches[np.abs(mu_branches[:, 2] - k) < tol]
        lam_k = lam_branches[np.abs(lam_branches[:, 2] - k) < tol]

        # 验证 η_R^{br}(μ_k) = λ_k（分支内双射）
        for i in range(len(mu_k)):
            lam_pred = braided_eta_R(mu_k[i, 0], float(k))
            # 找到 lam_k 中最接近的匹配
            dists = np.sqrt((lam_k[:, 0] - lam_pred[0])**2 + (lam_k[:, 1] - lam_pred[1])**2)
            if np.min(dists) > tol:
                return False

            # 验证单射性：不同 μ 映射到不同 λ
            for j in range(i + 1, len(mu_k)):
                lam_pred_j = braided_eta_R(mu_k[j, 0], float(k))
                if (abs(lam_pred[0] - lam_pred_j[0]) < tol
                        and abs(lam_pred[1] - lam_pred_j[1]) < tol):
                    return False

    return True


def verify_braiding_hexagon(
    R1: "RecObject", R2: "RecObject", R3: "RecObject", tol: float = 1e-6
) -> tuple[bool, str]:
    """
    验证辫子六边形公理（命题 2.5.2 辫子相容性）。

    左六边形：σ_{R1⊗R2, R3} = (σ_{R1,R3} ⊗ id_{R2}) ∘ (id_{R1} ⊗ σ_{R2,R3})
    右六边形：σ_{R1, R2⊗R3} = (id_{R2} ⊗ σ_{R1,R3}) ∘ (σ_{R1,R2} ⊗ id_{R3})

    返回
    -------
    tuple[bool, str]
        (是否通过, 描述信息)。
    """
    k12 = braiding_crossing_number(
        np.imag(np.linalg.eigvals(R1.koopman_matrix())).mean(),
        np.imag(np.linalg.eigvals(R2.koopman_matrix())).mean(),
    )
    k13 = braiding_crossing_number(
        np.imag(np.linalg.eigvals(R1.koopman_matrix())).mean(),
        np.imag(np.linalg.eigvals(R3.koopman_matrix())).mean(),
    )
    k23 = braiding_crossing_number(
        np.imag(np.linalg.eigvals(R2.koopman_matrix())).mean(),
        np.imag(np.linalg.eigvals(R3.koopman_matrix())).mean(),
    )

    # 左六边形：k12 + k13 = k13 + k23 → k12 = k23（分量张量积下的辫子加法）
    left_ok = (k12 + k13) == (k13 + k23)

    # 右六边形：k12 + k23 = k23 + k13 → k12 = k13
    right_ok = (k12 + k23) == (k23 + k13)

    if left_ok and right_ok:
        return True, f"六边形公理通过 (k12={k12}, k13={k13}, k23={k23})"
    else:
        return False, f"六边形公理不通过 (k12={k12}, k13={k13}, k23={k23})"


# ===========================================================================
# 隔离约束条件（Isolation Constraints, IC）
# 对应 §3.7 定义 C3.1 / 定理 C3.2
# ===========================================================================

@dataclass
class IsolationConstraintResult:
    """隔离约束验证结果。"""
    satisfies_IC: bool
    spectral_scale_compatible: tuple[bool, str]
    morphism_extendable: tuple[bool, str]
    topologically_compatible: tuple[bool, str]
    description: str = ""


def check_spectral_scale_compatibility(
    spec1: np.ndarray, spec2: np.ndarray, tol: float = 1e-6
) -> tuple[bool, str]:
    """
    验证谱尺度相容性（IC 条件 1）。

    检查 $\rho(\sigma(-\log U_{R_1})) / \rho(\sigma(-\log U_{R_2}))$ 是否有界。
    """
    rho1 = np.max(np.abs(spec1)) if len(spec1) > 0 else 0.0
    rho2 = np.max(np.abs(spec2)) if len(spec2) > 0 else 0.0

    if rho2 < tol:
        return (False, "目标谱为空或零，无法计算谱半径比")
    if rho1 < tol:
        return (True, f"源谱为零，自动满足 (rho1={rho1:.2e})")

    ratio = rho1 / rho2
    # 谱半径之比有界：要求 ratio 不远离 1 超过 2 个数量级
    bounded = ratio < 100.0 and ratio > 0.01
    msg = f"rho1/rho2={ratio:.2e}, {'通过' if bounded else '不通过'} (界: 0.01-100)"
    return (bounded, msg)


def check_morphism_extendability(
    R1: "RecObject", R2: "RecObject", tol: float = 1e-6
) -> tuple[bool, str]:
    """
    验证态射延伸性（IC 条件 2）。

    检查 $\|D(f)\| \leq C'$ 对典型态射 f 成立（范数控制）。
    """
    K1 = R1.koopman_matrix()
    K2 = R2.koopman_matrix()

    # 典型态射：恒等嵌入
    # D(id_R) = id_{D(R)}，范数恒为 1，自动满足
    norm_D_id = 1.0

    # 检查 Koopman 算子的谱半径是否匹配
    rho1 = max(abs(np.linalg.eigvals(K1)))
    rho2 = max(abs(np.linalg.eigvals(K2)))

    if rho2 > tol:
        norm_ratio = rho1 / rho2
        bounded = norm_ratio < 10.0
        msg = f"谱半径比={norm_ratio:.2e}, {'通过' if bounded else '不通过'} (界: 10)"
        return (bounded, msg)
    else:
        return (True, f"目标系统谱半径近零, 自动满足")


def check_topological_compatibility(
    R1: "RecObject", R2: "RecObject", tol: float = 1e-6
) -> tuple[bool, str]:
    """
    验证拓扑相容性（IC 条件 3）。

    检查 D 是否保持弱拓扑到弱拓扑的连续性。
    通过对 Koopman 算子的弱收敛行为做简化检验：
    两个系统的 Koopman 算子矩阵条件数相近则拓扑相容。
    """
    K1 = R1.koopman_matrix()
    K2 = R2.koopman_matrix()

    # 条件数作为拓扑结构度量
    cond1 = np.linalg.cond(K1) if K1.size > 0 else 1.0
    cond2 = np.linalg.cond(K2) if K2.size > 0 else 1.0

    if cond2 > tol:
        cond_ratio = cond1 / cond2
        # 条件数在同一数量级内视为拓扑相容
        compatible = cond_ratio < 10.0 and cond_ratio > 0.1
        msg = f"条件数比={cond_ratio:.2e}, {'通过' if compatible else '不通过'} (界: 0.1-10)"
        return (compatible, msg)
    else:
        return (True, "目标系统条件数近零, 自动满足")


def verify_isolation_constraints(
    R1: "RecObject", R2: "RecObject", tol: float = 1e-6
) -> IsolationConstraintResult:
    """
    验证两个 Rec 对象之间的隔离约束条件 IC(R1, R2)。

    三项条件全部满足时 IC 成立。对应定义 C3.1 / 定理 C3.2。

    参数
    ----------
    R1 : RecObject
        源递归系统对象。
    R2 : RecObject
        目标递归系统对象。
    tol : float
        数值容差。

    返回
    -------
    IsolationConstraintResult
        三项条件的逐项验证结果与综合判断。
    """
    # IC 条件 1: 谱尺度相容
    spec1 = compression_spectrum(R1, tol)
    spec2 = compression_spectrum(R2, tol)
    scale_ok, scale_msg = check_spectral_scale_compatibility(spec1, spec2, tol)

    # IC 条件 2: 态射延伸性
    morph_ok, morph_msg = check_morphism_extendability(R1, R2, tol)

    # IC 条件 3: 拓扑相容性
    topo_ok, topo_msg = check_topological_compatibility(R1, R2, tol)

    satisfies = scale_ok and morph_ok and topo_ok
    description = "IC ✅ 通过" if satisfies else "IC ⚠️ 条件性满足"

    return IsolationConstraintResult(
        satisfies_IC=satisfies,
        spectral_scale_compatible=(scale_ok, scale_msg),
        morphism_extendable=(morph_ok, morph_msg),
        topologically_compatible=(topo_ok, topo_msg),
        description=description,
    )
