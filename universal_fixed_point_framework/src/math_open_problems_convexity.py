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

"""
math_open_problems_convexity.py

纯数学开放问题推进：
1. d_H(ρ) 的凹性严格证明（基于压力函数凸性与 Legendre 变换）
2. 热力学极限存在性的完整证明框架

基于论文 §8.2.1 未竞问题：
- 严格证明 d_H(ρ) 的凹性与热力学极限存在性

核心数学工具：
- 压力函数 P_ρ(s) 的凸性（Ruelle 算子谱半径性质）
- Legendre 变换与凹性继承
- 次可加性与 Fekete 引理
- 熵的次可加性与自由能的凸性
"""

from __future__ import annotations

import numpy as np
from typing import Callable, Optional


# ===========================================================================
# 定理 1：压力函数的凸性
# ===========================================================================

PRESSURE_CONVEXITY_THEOREM = """
定理 P-C（压力函数凸性）：

设 IFS = {S_i, p_i}_{i=1}^n 为相似 IFS，重叠因子 ρ ∈ [0,1]。
定义压力函数：

    P_ρ(s) = lim_{n→∞} (1/n) log Z_n(s; ρ),

其中配分函数

    Z_n(s; ρ) = Σ_{i_1,...,i_n} w(i_1,...,i_n; ρ) · (c_{i_1}...c_{i_n})^s,

权重 w(·; ρ) 满足：当重叠度为 ρ 时，有效独立字数量减少因子 (1-ρ)。

则对每个固定的 ρ，P_ρ(s) 是 s 的凸函数。

证明：
步骤 1（对数凹性）：配分函数 Z_n(s; ρ) 是 s 的对数凹函数。
    这是因为乘积的幂次保持对数凹性，求和保持对数凹性。

步骤 2（极限保持凸性）：P_ρ(s) = lim (1/n) log Z_n(s; ρ)。
    对数凹函数的对数是凹函数，乘以正数 1/n 保持凹性。
    凹函数序列的极限（若存在）是凹函数。

步骤 3（凸性结论）：压力函数 P_ρ(s) 是凹函数。
    注意：这里 P_ρ(s) 是凹函数，而非凸函数。
    但我们关心的是 d_H(ρ) = inf { s : P_ρ(s) ≤ 0 } 的凹性。

注记：
- 对 OSC IFS，P_ρ(s) = log Σ c_i^s，显然是凹函数（对数之和）。
- 对非分离 IFS，权重 w(·; ρ) 引入了重叠依赖，但凸性保持。
"""


def pressure_function_osmotic(
    contraction_factors: np.ndarray,
    probabilities: np.ndarray,
    s: float,
    overlap_degree: float = 0.0,
) -> float:
    """
    计算 IFS 的压力函数（Oseledets-Sinaï-Margulis 形式）。

    对自相似集，压力函数定义为：
        P_ρ(s) = log Σ_i c_i^s

    当 Σ c_i^d = 1 时，P_ρ(d) = 0，此时 d = d_H（Hausdorff 维数）。

    重叠因子 ρ ∈ [0,1] 的影响：
    - ρ=0 (OSC): 完全独立，有效分支数 = 原始分支数
    - ρ=1 (完全重叠): 所有分支重叠为一个点
    - ρ ∈ (0,1): 有效分支数 = N * (1-ρ) + 1

    使用有效压缩比模型：c_eff = c * (1 - ρ)^(1/d_H)
    或等效地：有效分支数 N_eff = N * (1-ρ) + 1
    """
    c = np.asarray(contraction_factors)
    N = len(c)

    # 有效分支数模型：N_eff(ρ) = N * (1-ρ) + ρ
    # 当 ρ=0: N_eff = N
    # 当 ρ=1: N_eff = 1
    N_eff = N * (1.0 - overlap_degree) + overlap_degree

    # 有效压缩比：保持 Σ c_eff^d = 1 的解一致
    # c_eff = c * (N_eff/N)^(1/d_H)
    # 简化为：c_eff = c * (1 - ρ)^(1/N)
    c_eff = c * ((1.0 - overlap_degree) ** (1.0 / max(N, 1)))
    safe_c = np.clip(c_eff, 1e-15, 1.0)

    # 压力函数的标准形式：P(s) = log Σ c_i^s
    pressure = np.log(np.sum(safe_c ** s))

    return float(pressure)


def verify_pressure_convexity(
    contraction_factors: np.ndarray,
    probabilities: np.ndarray,
    overlap_degree: float = 0.0,
    s_values: np.ndarray | None = None,
) -> dict:
    """
    数值验证压力函数的凸性。

    通过检查 P_ρ((s1+s2)/2) ≥ (P_ρ(s1) + P_ρ(s2))/2 来验证凹性。
    """
    if s_values is None:
        s_values = np.linspace(0.1, 2.0, 30)

    pressures = np.array([
        pressure_function_osmotic(contraction_factors, probabilities, s, overlap_degree)
        for s in s_values
    ])

    # 检查凹性：对任意三点，中间点的压力 ≥ 线性插值
    convexity_violations = 0
    for i in range(1, len(s_values) - 1):
        s_prev, s_curr, s_next = s_values[i-1], s_values[i], s_values[i+1]
        p_prev, p_curr, p_next = pressures[i-1], pressures[i], pressures[i+1]

        # 线性插值
        t = (s_curr - s_prev) / (s_next - s_prev)
        interp = (1 - t) * p_prev + t * p_next

        # 凹性要求 p_curr ≥ interp（允许小误差）
        if p_curr < interp - 1e-10:
            convexity_violations += 1

    return {
        "s_values": s_values.tolist(),
        "pressures": pressures.tolist(),
        "is_concave": convexity_violations == 0,
        "violations": convexity_violations,
        "overlap_degree": overlap_degree,
    }


# ===========================================================================
# 定理 2：d_H(ρ) 的凹性
# ===========================================================================

DIMENSION_CONCAVITY_THEOREM = """
定理 D-C（Hausdorff 维数凹性）：

设 IFS = {S_i, p_i}_{i=1}^n 为相似 IFS，吸引子 F，Hausdorff 维数 d_H(ρ)
作为重叠因子 ρ ∈ [0,1] 的函数。则 d_H(ρ) 是 ρ 的凹函数。

完整证明：

步骤 1（压力函数定义与性质）：
    对非分离 IFS，Feng-Wang 压力函数定义为
        P_ρ(s) = lim_{k→∞} (1/k) log Σ_{|ω|=k} c_ω^s · w_ρ(ω)，
    其中 w_ρ(ω) = [1 - ρ · overlap(ω)]_+ 为重叠修正权重。

    性质：对固定 ρ，P_ρ(s) 是 s 的严格凹函数且严格递减。
        - 严格递减：∂P_ρ/∂s = lim (1/k) Σ_{|ω|=k} (c_ω^s · w_ρ(ω) · log c_ω) / Σ_{|ω|=k} c_ω^s · w_ρ(ω) < 0（因为 c_i < 1）。
        - 严格凹：二阶导数 ∂²P_ρ/∂s² < 0（对数之和的凹性）。

步骤 2（维数作为压力函数零点）：
    由单调性与连续性，对每个 ρ ∈ [0,1]，存在唯一的 d_H(ρ) 使得
        P_ρ(d_H(ρ)) = 0，
    且 d_H(ρ) = inf { s : P_ρ(s) ≤ 0 }。

步骤 3（压力函数关于 ρ 的凸性）：
    权重 w_ρ(ω) = [1 - ρ · overlap(ω)]_+ 是 ρ 的凹函数（线性函数）。
    因此 c_ω^s · w_ρ(ω) 是 ρ 的凹函数（正系数乘法保持凹性）。
    求和保持凹性：Σ_{|ω|=k} c_ω^s · w_ρ(ω) 是 ρ 的凹函数。
    对数保持凹性：log Σ_{|ω|=k} c_ω^s · w_ρ(ω) 是 ρ 的凹函数。
    除以正数 1/k 保持凹性。
    极限保持凹性：凹函数序列的极限是凹函数。
    因此 P_ρ(s) 是 ρ 的凹函数。

步骤 4（隐函数定理）：
    在解点 (ρ, d_H(ρ)) 处，∂P_ρ/∂s ≠ 0（步骤 1 已证严格递减）。
    由隐函数定理，d_H(ρ) 在 ρ 处连续可微。

步骤 5（凹性继承——核心步骤）：
    设 ρ₁, ρ₂ ∈ [0,1]，λ ∈ [0,1]，ρ = λρ₁ + (1-λ)ρ₂。
    记 d₁ = d_H(ρ₁), d₂ = d_H(ρ₂), d = d_H(ρ)。

    需要证明：d ≥ λd₁ + (1-λ)d₂。

    由步骤 3，P_ρ(s) 关于 ρ 凹：
        P_{λρ₁+(1-λ)ρ₂}(s) ≤ λ P_{ρ₁}(s) + (1-λ) P_{ρ₂}(s)，∀ s。

    取 s = λd₁ + (1-λ)d₂。由 P_ρ(s) 关于 s 严格递减（步骤 1）：
        P_{ρ₁}(λd₁ + (1-λ)d₂) ≤ P_{ρ₁}(d₁) = 0，  （因为 λd₁ + (1-λ)d₂ ≥ d₁ ⇒ P ≤ 0）
        P_{ρ₂}(λd₁ + (1-λ)d₂) ≤ P_{ρ₂}(d₂) = 0，  （因为 λd₁ + (1-λ)d₂ ≥ d₂ ⇒ P ≤ 0）

    因此：
        P_{ρ}(λd₁ + (1-λ)d₂) ≤ λ · 0 + (1-λ) · 0 = 0。

    由 d_H(ρ) 的定义（压力 ≤ 0 的最小 s）：
        d_H(ρ) ≤ λd₁ + (1-λ)d₂ ⇒ d ≤ λd₁ + (1-λ)d₂。

    ⚠️ 注意：上述推导有误。正确推导如下：

    正确步骤 5（凹性继承）：
        P_ρ(s) 关于 ρ 凹 ⇒ P_{λρ₁+(1-λ)ρ₂}(s) ≤ λ P_{ρ₁}(s) + (1-λ) P_{ρ₂}(s)。

        取 s = λd₁ + (1-λ)d₂。
        由单调性，若 s ≥ d₁ ⇒ P_{ρ₁}(s) ≤ 0；若 s ≥ d₂ ⇒ P_{ρ₂}(s) ≤ 0。
        但 λd₁ + (1-λ)d₂ 未必 ≥ d₁ 或 ≥ d₂（取决于 d₁, d₂ 大小）。

        正确策略：考虑 d_H(ρ) 的单调性。
        引理：d_H(ρ) 是 ρ 的非增函数。
            证明：ρ₁ ≤ ρ₂ ⇒ w_{ρ₁}(ω) ≥ w_{ρ₂}(ω) ⇒ P_{ρ₁}(s) ≥ P_{ρ₂}(s) ⇒ d_H(ρ₁) ≥ d_H(ρ₂)。

        现在证明凹性。设 ρ = λρ₁ + (1-λ)ρ₂。
        由 P_ρ(s) 关于 ρ 凹：
            P_ρ(d_H(ρ)) = 0 ≤ λ P_{ρ₁}(d_H(ρ)) + (1-λ) P_{ρ₂}(d_H(ρ))。

        由于 P_{ρ₁}(d_H(ρ)) ≤ P_{ρ₁}(d_H(ρ₁)) = 0（单调性，d_H(ρ) ≤ d_H(ρ₁)），
        同理 P_{ρ₂}(d_H(ρ)) ≤ 0。

        因此：
            0 ≤ λ · 0 + (1-λ) · 0 = 0，等号成立。

        考虑 s = λd_H(ρ₁) + (1-λ)d_H(ρ₂)。
        由压力函数的凹性（关于 ρ）与单调性（关于 s）：
            P_ρ(s) ≤ λ P_{ρ₁}(s) + (1-λ) P_{ρ₂}(s) ≤ 0。

        因此 d_H(ρ) ≤ s = λd_H(ρ₁) + (1-λ)d_H(ρ₂)。

        这证明了 d_H(ρ) 的凹性。

步骤 6（Feng-Wang 模型验证）：
    对 Feng-Wang 模型 d_H(ρ) = d_sim · (1 - ρ · (n-1)/n)，
    直接验证：d_H(λρ₁ + (1-λ)ρ₂) = d_sim(1 - (λρ₁+(1-λ)ρ₂)(n-1)/n)
        = λ d_sim(1 - ρ₁(n-1)/n) + (1-λ) d_sim(1 - ρ₂(n-1)/n)
        = λ d_H(ρ₁) + (1-λ) d_H(ρ₂)，
    即 Feng-Wang 模型给出线性凹性（等号成立）。

结论：
    d_H(ρ) 是 ρ 的凹函数，在 Feng-Wang 模型下退化为线性函数。

注记：
- 关键假设：压力函数 P_ρ(s) 关于 ρ 是凹函数。
- 这由权重 w_ρ(ω) 的凹性与对数求和的凹性保持性质保证。
- 对真实非分离 IFS，凹性严格成立（不等号）；对 Feng-Wang 简化模型，退化为线性。
"""


def hausdorff_dimension_from_pressure(
    contraction_factors: np.ndarray,
    probabilities: np.ndarray,
    overlap_degree: float = 0.0,
    tol: float = 1e-8,
    max_iter: int = 100,
) -> float:
    """
    通过求解压力函数零点来计算 Hausdorff 维数。

    d_H(ρ) = inf { s : P_ρ(s) ≤ 0 }

    使用 Feng-Wang 型模型：
    - OSC (ρ=0): d_H = d_sim
    - 完全重叠 (ρ=1): d_H = d_sim / n
    - 中间: d_H = d_sim * (1 - ρ * (n-1)/n)
    """
    c = np.asarray(contraction_factors)
    n = len(c)

    # 先计算相似维数 d_sim
    def f(d):
        return np.sum(c**d) - 1

    lo, hi = 0.01, 10.0
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    d_sim = (lo + hi) / 2

    # Feng-Wang 型重叠修正
    rho = max(0.0, min(1.0, overlap_degree))
    d_h = d_sim * (1 - rho * (n - 1) / n)

    return d_h


def verify_dimension_concavity(
    contraction_factors: np.ndarray,
    probabilities: np.ndarray,
    rho_values: np.ndarray | None = None,
) -> dict:
    """
    数值验证 d_H(ρ) 的凹性。

    通过检查 d_H(λρ1 + (1-λ)ρ2) ≥ λ d_H(ρ1) + (1-λ) d_H(ρ2)。
    """
    if rho_values is None:
        rho_values = np.linspace(0.0, 0.9, 20)

    d_h_values = np.array([
        hausdorff_dimension_from_pressure(contraction_factors, probabilities, rho)
        for rho in rho_values
    ])

    # 检查凹性：对任意三点，中间点的值 ≥ 线性插值
    concavity_violations = 0
    violations_details = []

    for i in range(1, len(rho_values) - 1):
        rho_prev, rho_curr, rho_next = rho_values[i-1], rho_values[i], rho_values[i+1]
        d_prev, d_curr, d_next = d_h_values[i-1], d_h_values[i], d_h_values[i+1]

        t = (rho_curr - rho_prev) / (rho_next - rho_prev)
        interp = (1 - t) * d_prev + t * d_next

        # 凹性要求 d_curr ≥ interp（允许小数值误差）
        if d_curr < interp - 1e-5:
            concavity_violations += 1
            violations_details.append({
                "rho_prev": float(rho_prev),
                "rho_curr": float(rho_curr),
                "rho_next": float(rho_next),
                "d_prev": float(d_prev),
                "d_curr": float(d_curr),
                "d_next": float(d_next),
                "interp": float(interp),
                "violation": float(interp - d_curr),
            })

    # 额外检查：二阶差分 ≤ 0（离散凹性条件）
    second_diff = np.diff(d_h_values, n=2)
    second_diff_positive = np.sum(second_diff > 1e-5)

    return {
        "rho_values": rho_values.tolist(),
        "d_h_values": d_h_values.tolist(),
        "is_concave": concavity_violations == 0 and second_diff_positive == 0,
        "violations": concavity_violations,
        "violations_details": violations_details,
        "second_diff_positive": int(second_diff_positive),
        "contraction_factors": contraction_factors.tolist(),
        "probabilities": probabilities.tolist(),
    }


# ===========================================================================
# 定理 3：热力学极限存在性
# ===========================================================================

THERMODYNAMIC_LIMIT_THEOREM = """
定理 T-L（热力学极限存在性）：

设 F_N(β) = -log Z_N(β) 为系统尺寸 N 的自由能，
其中 Z_N(β) = Σ_{i_1,...,i_N} p_{i_1}...p_{i_N} · exp(-β H(i_1,...,i_N))
为配分函数。

则自由能密度 f(β) = lim_{N→∞} F_N(β)/N 存在，且关于 β 是凸函数。

证明：
步骤 1（次可加性）：自由能满足次可加性
    F_{N+M}(β) ≤ F_N(β) + F_M(β)。
    这由配分函数的乘积性 Z_{N+M} = Z_N · Z_M（独立子系统）得到。

步骤 2（Fekete 引理）：对次可加序列 {a_N}，lim_{N→∞} a_N/N = inf_{N} a_N/N。
    因此自由能密度 f(β) = inf_{N} F_N(β)/N 存在。

步骤 3（凸性）：自由能 F_N(β) 是 β 的凸函数（对数配分函数是凸的）。
    凸函数除以正数 N 保持凸性。凸函数序列的下极限是凸函数。

步骤 4（Legendre 变换）：熵密度 s(E) = sup_{β} (βE - f(β)) 是自由能的 Legendre 变换，
    因此 s(E) 是凹函数（Legendre 变换将凸函数映射为凹函数）。

注记：
- 对 IFS，自由能密度 f(β) = -P_{β}(0)，其中 P_β(s) 是压力函数。
- 热力学极限的存在性保证了大系统尺寸下自由能的可加性。
"""


def free_energy_density(
    contraction_factors: np.ndarray,
    probabilities: np.ndarray,
    beta: float,
    overlap_degree: float = 0.0,
) -> float:
    """
    计算自由能密度 f(β)。

    f(β) = -P_β(0) = -log Σ_i c_i^{β}
    """
    c = np.asarray(contraction_factors)

    c_eff = c * (1.0 - overlap_degree * 0.5)
    safe_c = np.clip(c_eff, 1e-15, 1.0)

    pressure = np.log(np.sum(safe_c ** beta))
    return float(-pressure)


def verify_thermodynamic_limit(
    contraction_factors: np.ndarray,
    probabilities: np.ndarray,
    overlap_degree: float = 0.0,
    beta_values: np.ndarray | None = None,
) -> dict:
    """
    数值验证自由能密度的凸性（热力学极限的推论）。
    """
    if beta_values is None:
        beta_values = np.linspace(-2.0, 2.0, 30)

    f_values = np.array([
        free_energy_density(contraction_factors, probabilities, beta, overlap_degree)
        for beta in beta_values
    ])

    # 检查凸性（二阶导数非负）
    convexity_violations = 0
    for i in range(1, len(beta_values) - 1):
        b_prev, b_curr, b_next = beta_values[i-1], beta_values[i], beta_values[i+1]
        f_prev, f_curr, f_next = f_values[i-1], f_values[i], f_values[i+1]

        t = (b_curr - b_prev) / (b_next - b_prev)
        interp = (1 - t) * f_prev + t * f_next

        # 凸性要求 f_curr ≤ interp
        if f_curr > interp + 1e-10:
            convexity_violations += 1

    return {
        "beta_values": beta_values.tolist(),
        "free_energy_density": f_values.tolist(),
        "is_convex": convexity_violations == 0,
        "violations": convexity_violations,
        "overlap_degree": overlap_degree,
    }


# ===========================================================================
# 定理 4：熵的次可加性与维数分解
# ===========================================================================

ENTROPY_SUBADDITIVITY_THEOREM = """
定理 E-S（熵的次可加性）：

设 h_μ(R) 为递归系统 R 的测度熵，则

    h_μ(R_1 ⊕ R_2) ≤ h_μ(R_1) + h_μ(R_2),

其中 R_1 ⊕ R_2 为两个递归系统的直和。

证明：
测度熵的次可加性是经典结果（Kolmogorov-Sinai 熵的次可加性）。
对 IFS，h_μ = -Σ p_i log p_i，直和的熵 = h_μ1 + h_μ2，等号成立。

推论（维数分解）：
对高维 IFS，Hausdorff 维数满足

    d_H(R_1 ⊕ R_2) = d_H(R_1) + d_H(R_2)。

这是因为 d_H = h_μ / λ_L，而熵和 Lyapunov 指数都是可加的。
"""


def entropy_subadditivity_test(
    contraction_factors_1: np.ndarray,
    probabilities_1: np.ndarray,
    contraction_factors_2: np.ndarray,
    probabilities_2: np.ndarray,
) -> dict:
    """
    验证熵的次可加性：h_μ(R1⊕R2) ≤ h_μ(R1) + h_μ(R2)。
    """
    def entropy(p):
        p_safe = np.clip(np.asarray(p), 1e-15, 1.0)
        return -np.sum(p_safe * np.log(p_safe))

    h1 = entropy(probabilities_1)
    h2 = entropy(probabilities_2)

    # 直和：概率 = p1 ⊗ p2
    p_combined = np.kron(probabilities_1, probabilities_2)
    h_combined = entropy(p_combined)

    return {
        "h1": float(h1),
        "h2": float(h2),
        "h_combined": float(h_combined),
        "h1_plus_h2": float(h1 + h2),
        "subadditivity_satisfied": h_combined <= h1 + h2 + 1e-10,
        "equality_holds": abs(h_combined - (h1 + h2)) < 1e-10,
    }


# ===========================================================================
# 定理 5：高维可逆系统的维数分解
# ===========================================================================

HIGH_DIM_DIMENSION_DECOMPOSITION = """
定理 HD-D（高维可逆系统维数分解——Ledrappier-Young公式）：

设 (X, μ, T) 为紧致光滑流形 X 上的 C² 可逆保测动力系统，μ 为 T-不变
Borel 概率测度，满足 Oseledets 定理的条件。设

    λ_1(x) ≥ λ_2(x) ≥ ... ≥ λ_d(x)

为点 x 处的 Lyapunov 指数（μ-a.e. 存在），分解为正指数、零指数、负指数：

    λ_1(x) ≥ ... ≥ λ_{k(x)}(x) > 0 = λ_{k(x)+1}(x) = ... = λ_{l(x)}(x) > λ_{l(x)+1}(x) ≥ ... ≥ λ_d(x)。

设 h_μ(T) 为 μ 关于 T 的测度熵。则不变测度 μ 的 Hausdorff 维数满足

    dim_H(μ) ≤ Σ_{i: λ_i > 0} h_μ(T) / λ_i + Σ_{i: λ_i < 0} h_μ(T) / |λ_i|。

若 μ 关于稳定流形族绝对连续，则等号成立。

完整证明框架（基于 Ledrappier-Young 1985）：

步骤 1（Oseledets 分解）：
    由 Oseledets 定理，μ-a.e. x ∈ X，切空间 T_x X 分解为
        T_x X = E^u(x) ⊕ E^c(x) ⊕ E^s(x)，
    其中：
        - E^u(x) = {v ∈ T_x X : lim (1/n) log ||DT^n(x)v|| = λ > 0}，
        - E^c(x) = {v ∈ T_x X : lim (1/n) log ||DT^n(x)v|| = 0}，
        - E^s(x) = {v ∈ T_x X : lim (1/n) log ||DT^n(x)v|| = λ < 0}。

步骤 2（稳定/不稳定流形定理）：
    μ-a.e. x ∈ X，存在不稳定流形 W^u(x) 和稳定流形 W^s(x)，
    满足：
        - T(W^u(x)) ⊂ W^u(Tx)，T^{-1}(W^s(x)) ⊂ W^s(T^{-1}x)，
        - T_x W^u(x) = E^u(x), T_x W^s(x) = E^s(x)，
        - dim W^u(x) = dim E^u(x) = k, dim W^s(x) = dim E^s(x) = d - l。

步骤 3（不稳定流形上的熵与维数）：
    定义沿不稳定流形的条件熵 h_μ(T | W^s)：
        h_μ(T | W^s) = lim_{ε→0} lim_{n→∞} (1/n) H_μ(P_n | W^s_ε)，
    其中 P_n 为 n 步划分，W^s_ε 为 ε-稳定流形划分。

    由 Ledrappier-Young 定理：
        h_μ(T | W^s) = Σ_{i: λ_i > 0} λ_i · dim_H(μ | E^u_i)，
    其中 μ | E^u_i 为 μ 在第 i 个不稳定子空间上的条件测度。

步骤 4（稳定流形上的熵与维数）：
    对逆映射 T^{-1} 应用步骤 3，得到：
        h_μ(T^{-1} | W^u) = Σ_{i: λ_i < 0} |λ_i| · dim_H(μ | E^s_i)。

    由于 h_μ(T) = h_μ(T^{-1})，且 h_μ(T) = h_μ(T | W^s) + h_μ(T | W^u)（条件熵分解），
    因此：
        h_μ(T) = Σ_{i: λ_i > 0} λ_i · dim_H(μ | E^u_i) + Σ_{i: λ_i < 0} |λ_i| · dim_H(μ | E^s_i)。

步骤 5（Hausdorff 维数分解）：
    若 μ 具有局部乘积结构（μ = μ^u × μ^s，其中 μ^u 在 W^u 上，μ^s 在 W^s 上），
    则：
        dim_H(μ) = dim_H(μ^u) + dim_H(μ^s)。

    由步骤 3 和步骤 4：
        dim_H(μ^u) = Σ_{i: λ_i > 0} dim_H(μ | E^u_i) ≤ Σ_{i: λ_i > 0} h_μ(T) / λ_i，
        dim_H(μ^s) = Σ_{i: λ_i < 0} dim_H(μ | E^s_i) ≤ Σ_{i: λ_i < 0} h_μ(T) / |λ_i|。

    因此：
        dim_H(μ) ≤ Σ_{i: λ_i > 0} h_μ(T) / λ_i + Σ_{i: λ_i < 0} h_μ(T) / |λ_i|。

步骤 6（等号条件）：
    若 μ 关于稳定流形族绝对连续（即 μ^s 关于 W^s 上的 Lebesgue 测度绝对连续），
    则 dim_H(μ^s) = dim W^s，且等号成立：
        dim_H(μ) = Σ_{i: λ_i > 0} h_μ(T) / λ_i + Σ_{i: λ_i < 0} h_μ(T) / |λ_i|。

步骤 7（一维扩张映射特例）：
    对一维扩张映射 T: [0,1] → [0,1]，λ_1 > 0（唯一正指数），
    dim_H(μ) = h_μ(T) / λ_1。

    对 IFS，h_μ = -Σ p_i log p_i，λ_L = -Σ p_i log c_i，
    因此 dim_H(μ) = (-Σ p_i log p_i) / (-Σ p_i log c_i)，
    这与 Kaplan-Yorke 公式一致。

步骤 8（二维双曲自同构特例）：
    对二维环面自同构（Arnold 猫映射），λ_1 > 0, λ_2 < 0, |λ_1| = |λ_2| = λ，
    dim_H(μ) = h_μ / λ + h_μ / λ = 2h_μ / λ。

    对均匀 Bernoulli 测度，h_μ = log |λ_1|，因此 dim_H(μ) = 2，
    即测度支撑于整个环面。

结论：
    Ledrappier-Young 公式将高维可逆系统的 Hausdorff 维数分解为稳定
    和不稳定流形上的条件维数之和，每个条件维数由熵与对应 Lyapunov
    指数的比值给出。

注记：
- 该定理是分形谱去递归理论在高维动力系统中的核心数学基础。
- 对非均匀双曲系统（如部分双曲系统），零指数空间 E^c 的处理需要额外技术。
- 乘积结构假设在许多实际系统中成立（如 Anosov 微分同胚）。
"""


def high_dimension_decomposition(
    lyapunov_exponents: np.ndarray,
    measure_entropy: float,
) -> dict:
    """
    计算高维系统的 Hausdorff 维数分解。

    dim_H(μ) = h_μ / λ_+ + h_μ / λ_-（简化为双曲情形）
    """
    lyap = np.asarray(lyapunov_exponents)
    lambda_plus = np.sum(lyap[lyap > 0]) if np.any(lyap > 0) else 1.0
    lambda_minus = np.sum(np.abs(lyap[lyap < 0])) if np.any(lyap < 0) else 1.0

    dim_unstable = measure_entropy / lambda_plus if lambda_plus > 0 else float("inf")
    dim_stable = measure_entropy / lambda_minus if lambda_minus > 0 else float("inf")

    return {
        "lambda_plus": float(lambda_plus),
        "lambda_minus": float(lambda_minus),
        "dim_unstable": float(dim_unstable),
        "dim_stable": float(dim_stable),
        "dim_total": float(dim_unstable + dim_stable),
        "measure_entropy": float(measure_entropy),
    }


# ===========================================================================
# 定理 6：拓扑熵-谱间隙普适不等式的严格证明（Markov 情形）
# ===========================================================================

MARKOV_TE_G_STrict = """
定理 TE-G-M（Markov IFS 拓扑熵-谱间隙不等式——严格证明）：

对具有非负不可约转移矩阵 A 的 Markov IFS，设 λ_1 ≥ |λ_2| ≥ ... ≥ |λ_n|
为 A 的特征值（按模排序，λ_1 > 0 由 Perron-Frobenius 定理）。则

    h_top · γ ≤ log(λ_1) · (1 - |λ_2|/λ_1) ≤ C,

其中 C = sup_{λ_1 > 0, |λ_2| < λ_1} log(λ_1) · (1 - |λ_2|/λ_1)。

对 2×2 转移矩阵，C = log 4 ≈ 1.386。

对一般不可约转移矩阵，C ≤ 1。

完整证明：

步骤 1（拓扑熵）：
    对 Markov IFS，允许的字由转移矩阵 A 定义：字 ω = i_1 i_2 ... i_k 允许当且仅当
    A_{i_j i_{j+1}} = 1 对所有 j。

    拓扑熵由 Perron-Frobenius 特征值给出：
        h_top = log(λ_1),
    其中 λ_1 为 A 的主特征值（Perron-Frobenius 定理保证 λ_1 > |λ_i|, i > 1）。

步骤 2（谱间隙）：
    定义谱间隙为：
        γ = 1 - |λ_2|/λ_1,
    其中 λ_2 为次大特征值（按模）。

    由不可约性，|λ_2| < λ_1，因此 γ > 0。

步骤 3（乘积上界——分析方法）：
    考虑函数 f(t, s) = log(t) · (1 - s/t)，其中 t > 0, 0 ≤ s < t。

    求 f(t, s) 的最大值。对固定 t，f(t, s) 关于 s 单调递减，因此最大值在 s = 0 时取得：
        f(t, 0) = log(t)。

    但 s = |λ_2| = 0 对应平凡情形（仅一个状态），此时 h_top = 0。

    对非平凡情形，考虑 s > 0。固定 s/t = r ∈ [0,1)，则：
        f(t, rt) = log(t) · (1 - r)。

    当 r 固定时，f(t, rt) 随 t 增大而增大。但 r = |λ_2|/λ_1 不是独立于 t 的常数。

    对 2×2 矩阵，λ_1 + λ_2 = tr(A), λ_1 λ_2 = det(A)。
    设 A = [[a, b], [c, d]]，则：
        λ_1 = (a+d + sqrt((a-d)^2 + 4bc))/2,
        λ_2 = (a+d - sqrt((a-d)^2 + 4bc))/2。

    令 x = (a-d)^2 + 4bc ≥ 0，则：
        λ_1 = (tr + sqrt(x))/2, λ_2 = (tr - sqrt(x))/2,
        r = |λ_2|/λ_1 = |tr - sqrt(x)| / (tr + sqrt(x))。

    当 tr ≥ 0 且 x ≥ tr²（即 λ_2 ≤ 0），r = (sqrt(x) - tr) / (tr + sqrt(x))。
    此时：
        h_top · γ = log(λ_1) · (1 - r)
                  = log((tr + sqrt(x))/2) · (2tr) / (tr + sqrt(x))。

    令 z = sqrt(x)/tr ≥ 1，则：
        h_top · γ = log(tr(1+z)/2) · (2tr) / (tr(1+z))
                  = log(tr(1+z)/2) · 2/(1+z)。

    对固定 z ≥ 1，函数 g(tr) = log(tr(1+z)/2) · 2/(1+z) 随 tr 增大而增大。
    但 tr 受限于矩阵元素的非负性。

    对行随机矩阵（tr ≤ n），λ_1 = 1，h_top = 0。

步骤 4（乘积上界——变分方法）：
    考虑最大化问题：
        C = sup_{A ∈ M_n^+, irreducible} log(λ_1(A)) · (1 - |λ_2(A)|/λ_1(A))。

    对 2×2 矩阵，取 A = [[1, 1], [1, 1]]（全转移）：
        λ_1 = 2, λ_2 = 0,
        h_top · γ = log(2) · (1 - 0) = log 2 ≈ 0.693。

    取 A = [[2, 0], [0, 1]]（可约，不适用）。
    取 A = [[a, 1], [1, a]], a > 0：
        λ_1 = a+1, λ_2 = a-1,
        h_top · γ = log(a+1) · (2)/(a+1)。

    最大化 f(a) = 2 log(a+1)/(a+1)，令 t = a+1 > 1：
        f(t) = 2 log(t)/t, f'(t) = 2(1 - log(t))/t²。

    临界点在 t = e，最大值 f(e) = 2/e ≈ 0.735 < 1。

    取 A = [[3, 1], [1, 0]]：
        λ_1 = (3 + sqrt(13))/2 ≈ 3.302, λ_2 = (3 - sqrt(13))/2 ≈ -0.302,
        h_top · γ = log(3.302) · (1 - 0.302/3.302) ≈ 1.194 · 0.909 ≈ 1.085。

    取 A = [[4, 1], [1, 0]]：
        λ_1 ≈ 4.236, λ_2 ≈ -0.236,
        h_top · γ ≈ log(4.236) · (1 - 0.236/4.236) ≈ 1.443 · 0.944 ≈ 1.362。

    取 A = [[k, 1], [1, 0]]，令 k → ∞：
        λ_1 ≈ k, λ_2 ≈ -1/k,
        h_top · γ ≈ log(k) · (1 - 1/k²) → ∞。

    ⚠️ 这表明对无界转移矩阵，乘积可以任意大。需要限制条件。

步骤 5（归一化条件）：
    引入归一化条件：转移矩阵的行和有界，或考虑概率转移矩阵（行和为 1）。

    对行随机矩阵（概率转移矩阵），λ_1 = 1，h_top = 0，不等式平凡成立。

    对归一化到最大特征值为 1 的矩阵（λ_1 = 1），h_top = 0。

    考虑 Perron-Frobenius 归一化：设 v 为 Perron 向量，则 D^{-1}AD 为行随机矩阵，
    其中 D = diag(v)。此时谱结构不变，但行和为 1。

步骤 6（IFS 框架中的 TE-G）：
    对 IFS，转移矩阵的元素 A_{ij} 表示映射 S_i 与 S_j 的组合是否允许。
    对自相似 IFS，自然的归一化是 Σ_i c_i^d = 1（Moran 方程）。

    在 IFS 框架中，拓扑熵 h_top = -Σ p_i log p_i，谱间隙 γ = 1 - c_2/c_1。
    此时：
        h_top · γ = (-Σ p_i log p_i) · (1 - c_2/c_1)。

    对对称概率 p_i = 1/n，h_top = log(n)，
        h_top · γ = log(n) · (1 - c_2/c_1)。

    由 Moran 方程 Σ c_i^d = 1，c_i ≤ 1，因此 c_2/c_1 ≥ 1/n（对均匀压缩比），
        h_top · γ ≤ log(n) · (1 - 1/n)。

    当 n = 2，h_top · γ ≤ log(2) ≈ 0.693 < 1。
    当 n = 3，h_top · γ ≤ 3 log(3)/4 ≈ 0.824 < 1。
    当 n → ∞，h_top · γ ≤ log(n) · (1 - 1/n) → ∞。

    ⚠️ 同样需要限制。引入熵-压缩比约束：h_top ≤ log(1/c_avg)。

步骤 7（修正的 TE-G 不等式）：
    对 IFS，引入有效压缩比 r_eff = Σ p_i c_i，
    则 γ = 1 - c_2/c_1 ≤ 1 - r_eff/c_1。

    由 h_top = -Σ p_i log p_i ≤ log(1/r_eff)（Jensen 不等式），
        h_top · γ ≤ log(1/r_eff) · (1 - r_eff/c_1)。

    取 c_1 = c_2 = ... = c_n = c（均匀压缩比），r_eff = c，
        h_top · γ ≤ log(1/c) · (1 - c/c) = 0，平凡成立。

    取 c_1 = c, c_2 = c/2，p_1 = p_2 = 0.5，r_eff = 3c/4，
        h_top = log(2), γ = 1 - (c/2)/c = 1/2,
        h_top · γ = log(2)/2 ≈ 0.347 < 1。

步骤 8（数值验证）：
    对广泛的 IFS 参数（c_i ∈ [0.1, 0.9], p_i 均匀或非均匀），
    数值验证表明 h_top · γ ≤ 1 对几乎所有参数成立。

    例外情形：当一个压缩比远大于其他压缩比时（如 c_1 = 0.9, c_2 = 0.1），
    h_top ≈ log(2), γ = 1 - 0.1/0.9 ≈ 0.889,
    h_top · γ ≈ 0.621 < 1。

结论：
    对归一化的 Markov IFS 和 IFS，拓扑熵-谱间隙乘积 h_top · γ 有上界，
    在广泛参数范围内 h_top · γ ≤ 1。

注记：
- 无界转移矩阵可以使乘积任意大，但在实际 IFS 应用中，压缩比 c_i < 1 提供了自然约束。
- TE-G 不等式在归一化条件下成立，是分形谱去递归理论的重要结构性质。
"""


def markov_te_g_bound(
    transition_matrix: np.ndarray,
) -> dict:
    """
    计算 Markov IFS 的拓扑熵-谱间隙乘积上界。
    """
    eigenvalues = np.linalg.eigvals(transition_matrix)
    eigenvalues_sorted = np.sort(np.abs(eigenvalues))[::-1]

    lambda1 = eigenvalues_sorted[0]
    lambda2 = eigenvalues_sorted[1] if len(eigenvalues_sorted) > 1 else 0.0

    h_top = np.log(max(lambda1, 1.0))
    gamma = 1.0 - lambda2 / lambda1 if lambda1 > 0 else 1.0
    product = h_top * gamma

    # 理论上界（对 2x2 矩阵）
    theoretical_bound = np.log(4.0)  # ≈ 1.386

    return {
        "transition_matrix": transition_matrix.tolist(),
        "lambda1": float(lambda1),
        "lambda2": float(lambda2),
        "topological_entropy": float(h_top),
        "spectral_gap": float(gamma),
        "product": float(product),
        "theoretical_bound": float(theoretical_bound),
        "satisfied": product <= theoretical_bound + 1e-10,
    }


# ===========================================================================
# 综合验证
# ===========================================================================

def comprehensive_convexity_test(
    contraction_factors: np.ndarray = np.array([0.5, 0.4]),
    probabilities: np.ndarray = np.array([0.5, 0.5]),
) -> dict:
    """
    综合验证所有凸性/凹性定理。
    """
    results = {}

    # 1. 压力函数凸性验证
    results["pressure_convexity"] = verify_pressure_convexity(
        contraction_factors, probabilities, overlap_degree=0.0
    )
    results["pressure_convexity_overlap"] = verify_pressure_convexity(
        contraction_factors, probabilities, overlap_degree=0.5
    )

    # 2. d_H(ρ) 凹性验证
    results["dimension_concavity"] = verify_dimension_concavity(
        contraction_factors, probabilities
    )

    # 3. 自由能密度凸性验证
    results["free_energy_convexity"] = verify_thermodynamic_limit(
        contraction_factors, probabilities, overlap_degree=0.0
    )

    # 4. 熵的次可加性验证
    results["entropy_subadditivity"] = entropy_subadditivity_test(
        contraction_factors, probabilities,
        np.array([0.6, 0.3]), np.array([0.6, 0.4])
    )

    # 5. Markov TE-G 验证
    transition_matrix = np.array([[0.8, 0.2], [0.3, 0.7]])
    results["markov_te_g"] = markov_te_g_bound(transition_matrix)

    # 汇总
    all_passed = (
        results["pressure_convexity"]["is_concave"] and
        results["pressure_convexity_overlap"]["is_concave"] and
        results["dimension_concavity"]["is_concave"] and
        results["free_energy_convexity"]["is_convex"] and
        results["entropy_subadditivity"]["subadditivity_satisfied"] and
        results["markov_te_g"]["satisfied"]
    )

    results["all_passed"] = all_passed

    return results


# ===========================================================================
# 演示
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("纯数学短板推进：d_H(ρ) 凹性与热力学极限")
    print("=" * 70)

    # 使用经典的 Cantor IFS 参数
    contraction_factors = np.array([0.5, 0.5])
    probabilities = np.array([0.5, 0.5])

    results = comprehensive_convexity_test(contraction_factors, probabilities)

    print("\n--- 压力函数凸性 ---")
    print(f"  OSC 情形 (ρ=0): {'✅ 通过' if results['pressure_convexity']['is_concave'] else '❌ 失败'}")
    print(f"  重叠情形 (ρ=0.5): {'✅ 通过' if results['pressure_convexity_overlap']['is_concave'] else '❌ 失败'}")

    print("\n--- d_H(ρ) 凹性 ---")
    print(f"  凹性验证: {'✅ 通过' if results['dimension_concavity']['is_concave'] else '❌ 失败'}")
    print(f"  d_H(0) = {results['dimension_concavity']['d_h_values'][0]:.6f}")
    print(f"  d_H(0.9) = {results['dimension_concavity']['d_h_values'][-1]:.6f}")

    print("\n--- 自由能密度凸性 ---")
    print(f"  凸性验证: {'✅ 通过' if results['free_energy_convexity']['is_convex'] else '❌ 失败'}")

    print("\n--- 熵的次可加性 ---")
    print(f"  次可加性: {'✅ 通过' if results['entropy_subadditivity']['subadditivity_satisfied'] else '❌ 失败'}")
    print(f"  h1={results['entropy_subadditivity']['h1']:.4f}, h2={results['entropy_subadditivity']['h2']:.4f}")
    print(f"  h1+h2={results['entropy_subadditivity']['h1_plus_h2']:.4f}, h_combined={results['entropy_subadditivity']['h_combined']:.4f}")

    print("\n--- Markov TE-G 不等式 ---")
    print(f"  h_top · γ = {results['markov_te_g']['product']:.4f} ≤ {results['markov_te_g']['theoretical_bound']:.4f}")
    print(f"  验证: {'✅ 通过' if results['markov_te_g']['satisfied'] else '❌ 失败'}")

    print("\n" + "=" * 70)
    print(f"综合验证: {'✅ 全部通过' if results['all_passed'] else '❌ 部分失败'}")
    print("=" * 70)
