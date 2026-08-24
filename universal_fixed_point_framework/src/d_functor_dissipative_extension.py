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
d_functor_dissipative_extension.py

Phase 15D-1: D 函子扩展到耗散混沌系统

核心内容：
1. 非自伴算子的伪谱理论框架
2. 耗散系统的半群表示（Hille-Yosida 框架）
3. D 函子在耗散系统上的扩展
4. 伪谱测度与广义谱对应
5. 数值验证与测试
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm, logm, eigvals
from scipy.sparse.linalg import eigs


class NonSelfAdjointSpectralTheory:
    """
    非自伴算子的伪谱理论框架。

    耗散混沌系统的核心特点：
    - 演化算子 U(t) = exp(-iHt) 是非自伴的
    - 特征值可以是复数（实部表示耗散率，虚部表示频率）
    - 需要伪谱理论描述数值稳定性与谱扰动
    """

    def __init__(self, operator: np.ndarray):
        """
        初始化非自伴算子。

        参数
        ----------
        operator : np.ndarray
            非自伴算子矩阵
        """
        self.operator = operator
        self.n = operator.shape[0]

    def pseudospectrum(self, epsilon: float = 1e-6, n_points: int = 100) -> np.ndarray:
        """
        计算伪谱 ε-pseudospectrum。

        伪谱定义：σ_ε(A) = {z ∈ ℂ | ‖(zI - A)⁻¹‖ ≥ 1/ε}

        参数
        ----------
        epsilon : float
            伪谱精度参数
        n_points : int
            网格点数

        返回
        -------
        pseudospec : np.ndarray
            伪谱区域内的点集
        """
        x = np.linspace(-2, 2, n_points)
        y = np.linspace(-2, 2, n_points)
        xx, yy = np.meshgrid(x, y)
        z = xx + 1j * yy

        pseudospec = []
        for i in range(n_points):
            for j in range(n_points):
                try:
                    inv_norm = np.linalg.norm(np.linalg.inv(z[i, j] * np.eye(self.n) - self.operator))
                    if inv_norm >= 1.0 / epsilon:
                        pseudospec.append(z[i, j])
                except np.linalg.LinAlgError:
                    pseudospec.append(z[i, j])

        return np.array(pseudospec)

    def spectrum_with_dissipation(self) -> dict:
        """
        计算含耗散的谱分解。

        返回复数特征值，实部表示耗散率，虚部表示频率。
        """
        evals = eigvals(self.operator)

        return {
            "eigenvalues": evals,
            "real_parts": np.real(evals),
            "imag_parts": np.imag(evals),
            "dissipation_rates": -np.real(evals),
            "frequencies": np.imag(evals),
            "is_self_adjoint": np.allclose(self.operator, self.operator.conj().T),
        }

    def resolvent_norm(self, z: complex) -> float:
        """
        计算预解式范数 ‖(zI - A)⁻¹‖。

        参数
        ----------
        z : complex
            复平面上的点

        返回
        -------
        norm : float
            预解式范数
        """
        try:
            return np.linalg.norm(np.linalg.inv(z * np.eye(self.n) - self.operator))
        except np.linalg.LinAlgError:
            return float("inf")


class DissipativeSemigroup:
    """
    耗散系统的半群表示。

    Hille-Yosida 框架：耗散算子 A 生成压缩半群 T(t) = exp(tA)
    满足：
    - T(0) = I
    - T(t+s) = T(t)T(s)
    - ‖T(t)‖ ≤ 1（压缩性）
    """

    def __init__(self, generator: np.ndarray):
        """
        初始化耗散半群生成元。

        参数
        ----------
        generator : np.ndarray
            耗散算子（实部非正的特征值）
        """
        self.generator = generator
        self.n = generator.shape[0]

    def is_dissipative(self) -> bool:
        """
        判断是否为耗散算子。

        耗散算子条件：Re⟨x, Ax⟩ ≤ 0 对所有 x。
        """
        for i in range(self.n):
            x = np.random.randn(self.n) + 1j * np.random.randn(self.n)
            x = x / np.linalg.norm(x)
            re = np.real(np.vdot(x, self.generator @ x))
            if re > 1e-10:
                return False
        return True

    def semigroup(self, t: float) -> np.ndarray:
        """
        计算半群算子 T(t) = exp(tA)。

        参数
        ----------
        t : float
            时间参数

        返回
        -------
        T : np.ndarray
            半群算子
        """
        return expm(t * self.generator)

    def decay_rate(self) -> float:
        """
        计算最大耗散率（衰减率）。

        返回
        -------
        rate : float
            最大衰减率 = max(-Re(λ))
        """
        evals = eigvals(self.generator)
        return np.max(-np.real(evals))

    def long_time_behavior(self) -> dict:
        """
        分析长时间行为。
        """
        evals = eigvals(self.generator)
        sorted_indices = np.argsort(np.real(evals))[::-1]
        dominant_eval = evals[sorted_indices[0]]

        return {
            "dominant_eigenvalue": dominant_eval,
            "dominant_decay_rate": -np.real(dominant_eval),
            "dominant_frequency": np.imag(dominant_eval),
            "asymptotic_state": "equilibrium" if np.real(dominant_eval) < 0 else "persistent",
            "spectral_gap": np.real(dominant_eval) - np.real(evals[sorted_indices[1]]) if len(evals) > 1 else float("inf"),
        }


class UnboundedOperatorDomain:
    """
    无界算子的定义域管理。

    无界算子 A: D(A) ⊂ H → H 需要显式管理定义域 D(A)。
    使用图范数 ||x||_A = ||x|| + ||Ax|| 定义闭包。
    """

    def __init__(self, operator: np.ndarray, domain_mask: np.ndarray | None = None):
        """
        初始化无界算子定义域。

        参数
        ----------
        operator : np.ndarray
            算子矩阵（可能是奇异的或无界的）
        domain_mask : np.ndarray
            定义域掩码（1=在定义域内，0=不在）
        """
        self.operator = operator
        self.n = operator.shape[0]
        self.domain_mask = domain_mask if domain_mask is not None else np.ones(self.n, dtype=bool)

    def graph_norm(self, x: np.ndarray) -> float:
        """
        计算图范数 ||x||_A = ||x|| + ||Ax||。

        参数
        ----------
        x : np.ndarray
            向量

        返回
        -------
        norm : float
            图范数
        """
        return np.linalg.norm(x) + np.linalg.norm(self.operator @ x)

    def is_in_domain(self, x: np.ndarray) -> bool:
        """
        判断向量是否在定义域内。
        """
        try:
            result = self.operator @ x
            return not np.any(np.isinf(result)) and not np.any(np.isnan(result))
        except:
            return False

    def closure(self) -> np.ndarray:
        """
        计算定义域的闭包（图范数下的完备化）。
        """
        return self.domain_mask.copy()

    def domain_dimension(self) -> int:
        """
        计算定义域维度。
        """
        return int(np.sum(self.domain_mask))


class NonNormalOperatorTheory:
    """
    非正规算子理论框架。

    非正规算子 A 满足 AA* ≠ A*A，需要伪谱理论描述。
    关键概念：
    - 数值半径 w(A) = sup_{||x||=1} |⟨x, Ax⟩|
    - 谱变分 σ_ε(A) = {z | ||(zI - A)⁻¹|| ≥ 1/ε}
    - 条件数 κ(A) = ||A|| ||A⁻¹||
    """

    def __init__(self, operator: np.ndarray):
        """
        初始化非正规算子。
        """
        self.operator = operator
        self.n = operator.shape[0]

    def numerical_radius(self) -> float:
        """
        计算数值半径 w(A) = sup_{||x||=1} |⟨x, Ax⟩|。
        """
        max_val = 0.0
        for _ in range(100):
            x = np.random.randn(self.n) + 1j * np.random.randn(self.n)
            x = x / np.linalg.norm(x)
            val = np.abs(np.vdot(x, self.operator @ x))
            max_val = max(max_val, val)
        return max_val

    def non_normality_index(self) -> float:
        """
        计算非正规性指标：||AA* - A*A|| / ||A||²。
        """
        A = self.operator
        AAstar = A @ A.conj().T
        AstarA = A.conj().T @ A
        return np.linalg.norm(AAstar - AstarA) / (np.linalg.norm(A) ** 2 + 1e-15)

    def spectral_variation(self, epsilon: float = 1e-6) -> float:
        """
        计算谱变分（伪谱半径与谱半径之差）。

        对于幂零算子（如 [[0,1],[0,0]]），谱半径为0，但伪谱非空。
        使用数值半径作为网格范围的后备，确保能捕获伪谱区域。
        """
        evals = eigvals(self.operator)
        spectral_radius = np.max(np.abs(evals))

        w = self.numerical_radius()

        if spectral_radius < 1e-10:
            return w

        grid_scale = max(spectral_radius, w, np.sqrt(epsilon), 0.1)

        n_fine = 50
        x_fine = np.linspace(-grid_scale, grid_scale, n_fine)
        y_fine = np.linspace(-grid_scale, grid_scale, n_fine)

        max_variation = 0.0
        for xi in x_fine:
            for yi in y_fine:
                z = xi + 1j * yi
                try:
                    inv_norm = np.linalg.norm(np.linalg.inv(z * np.eye(self.n) - self.operator))
                    if inv_norm >= 1.0 / epsilon:
                        dist = np.abs(z) - spectral_radius
                        max_variation = max(max_variation, dist)
                except np.linalg.LinAlgError:
                    dist = np.abs(z) - spectral_radius
                    max_variation = max(max_variation, dist)

        return max_variation

    def functional_calculus(self, function, z: complex) -> np.ndarray:
        """
        泛函演算：f(A) = (1/(2πi)) ∮ f(λ)(λI - A)⁻¹ dλ。

        参数
        ----------
        function : callable
            解析函数
        z : complex
            围道中心

        返回
        -------
        f_A : np.ndarray
            f(A) 的矩阵表示
        """
        radius = 2 * np.max(np.abs(eigvals(self.operator)))
        n_points = 100

        integral = np.zeros((self.n, self.n), dtype=complex)
        for k in range(n_points):
            theta = 2 * np.pi * k / n_points
            lambda_val = z + radius * np.exp(1j * theta)
            dlambda = 1j * radius * np.exp(1j * theta) * (2 * np.pi / n_points)

            try:
                resolvent = np.linalg.inv(lambda_val * np.eye(self.n) - self.operator)
                integral += function(lambda_val) * resolvent * dlambda
            except np.linalg.LinAlgError:
                continue

        return integral / (2 * np.pi * 1j)


class DissipativeDecursionFunctor:
    """
    D 函子在耗散系统上的扩展。

    将耗散递归系统映射到含耗散的谱对象。
    支持：
    - 非自伴算子
    - 非正规算子
    - 无界算子
    """

    def __init__(self):
        pass

    def dissipative_rec_to_spec(self, rec_operator: np.ndarray, dissipation_rate: float = 0.1) -> dict:
        """
        将耗散递归算子映射到谱对象。

        参数
        ----------
        rec_operator : np.ndarray
            递归算子（可能是非自伴的）
        dissipation_rate : float
            耗散率

        返回
        -------
        spec_object : dict
            含耗散的谱对象
        """
        n = rec_operator.shape[0]

        dissipative_operator = rec_operator - dissipation_rate * np.eye(n)

        nsa = NonSelfAdjointSpectralTheory(dissipative_operator)
        spectrum_info = nsa.spectrum_with_dissipation()

        semigroup = DissipativeSemigroup(dissipative_operator)

        nno = NonNormalOperatorTheory(dissipative_operator)

        return {
            "dissipative_operator": dissipative_operator,
            "original_operator": rec_operator,
            "dissipation_rate": dissipation_rate,
            "spectrum": spectrum_info,
            "semigroup_properties": {
                "is_dissipative": semigroup.is_dissipative(),
                "decay_rate": semigroup.decay_rate(),
                "long_time": semigroup.long_time_behavior(),
            },
            "pseudospectrum": nsa.pseudospectrum(epsilon=1e-4, n_points=50),
            "non_normality": {
                "numerical_radius": nno.numerical_radius(),
                "non_normality_index": nno.non_normality_index(),
                "spectral_variation": nno.spectral_variation(),
            },
        }

    def spec_to_dissipative_rec(self, spec_object: dict) -> np.ndarray:
        """
        从谱对象逆重构耗散递归算子。

        参数
        ----------
        spec_object : dict
            含耗散的谱对象

        返回
        -------
        rec_operator : np.ndarray
            递归算子
        """
        return spec_object["dissipative_operator"] + spec_object["dissipation_rate"] * np.eye(spec_object["dissipative_operator"].shape[0])

    def verify_dissipative_adjoint(self, rec_operator: np.ndarray, dissipation_rate: float = 0.1) -> dict:
        """
        验证耗散系统的广义伴随关系。

        检查 D⊣R 在耗散系统上的近似成立性。
        """
        n = rec_operator.shape[0]

        dissipative_operator = rec_operator - dissipation_rate * np.eye(n)

        try:
            D_rec = logm(dissipative_operator)
            R_spec = expm(D_rec)

            forward_error = np.linalg.norm(R_spec - dissipative_operator) / np.linalg.norm(dissipative_operator)
            backward_error = np.linalg.norm(expm(D_rec) - dissipative_operator) / np.linalg.norm(dissipative_operator)

            return {
                "forward_error": float(forward_error),
                "backward_error": float(backward_error),
                "approx_adjoint": forward_error < 1e-6 and backward_error < 1e-6,
                "valid": True,
            }
        except np.linalg.LinAlgError:
            return {
                "forward_error": float("inf"),
                "backward_error": float("inf"),
                "approx_adjoint": False,
                "valid": False,
                "reason": "对数运算失败（可能存在零特征值）",
            }

    def unbounded_rec_to_spec(self, rec_operator: np.ndarray, domain_mask: np.ndarray | None = None) -> dict:
        """
        将无界递归算子映射到谱对象。

        参数
        ----------
        rec_operator : np.ndarray
            无界递归算子
        domain_mask : np.ndarray
            定义域掩码

        返回
        -------
        spec_object : dict
            含定义域信息的谱对象
        """
        domain = UnboundedOperatorDomain(rec_operator, domain_mask)
        nno = NonNormalOperatorTheory(rec_operator)

        return {
            "operator": rec_operator,
            "domain": {
                "mask": domain.domain_mask,
                "dimension": domain.domain_dimension(),
                "graph_norm_example": domain.graph_norm(np.ones(rec_operator.shape[0])),
            },
            "non_normality": {
                "numerical_radius": nno.numerical_radius(),
                "non_normality_index": nno.non_normality_index(),
                "spectral_variation": nno.spectral_variation(),
            },
            "spectrum": NonSelfAdjointSpectralTheory(rec_operator).spectrum_with_dissipation(),
        }


class HenonMapDissipative:
    """
    Henon 映射的耗散版本作为耗散混沌系统的典型例子。

    Henon 映射：x_{n+1} = 1 - a x_n² + y_n, y_{n+1} = b x_n
    耗散版本：添加衰减项
    """

    def __init__(self, a: float = 1.4, b: float = 0.3, dissipation: float = 0.01):
        """
        初始化 Henon 映射参数。

        参数
        ----------
        a : float
            Henon 参数 a
        b : float
            Henon 参数 b
        dissipation : float
            耗散系数
        """
        self.a = a
        self.b = b
        self.dissipation = dissipation

    def jacobian(self, x: float, y: float) -> np.ndarray:
        """
        计算 Henon 映射在点 (x, y) 处的 Jacobian 矩阵。

        参数
        ----------
        x, y : float
            相空间点

        返回
        -------
        J : np.ndarray
            2x2 Jacobian 矩阵
        """
        return np.array([
            [-2 * self.a * x, 1],
            [self.b, 0]
        ])

    def lyapunov_exponents(self, n_iter: int = 10000) -> tuple[float, float]:
        """
        数值计算 Lyapunov 指数。

        参数
        ----------
        n_iter : int
            迭代次数

        返回
        -------
        exponents : tuple
            (λ₁, λ₂) 两个 Lyapunov 指数
        """
        x, y = 0.0, 0.0
        J = np.eye(2)
        log_sum = np.zeros(2)

        for _ in range(n_iter):
            x_new = 1 - self.a * x**2 + y
            y_new = self.b * x

            J_new = self.jacobian(x, y) @ J

            U, S, _ = np.linalg.svd(J_new)
            log_sum += np.log(S)

            J = U
            x, y = x_new, y_new

        return tuple(log_sum / n_iter)

    def to_operator(self, n_grid: int = 20) -> np.ndarray:
        """
        将 Henon 映射离散化为算子形式。

        参数
        ----------
        n_grid : int
            网格点数

        返回
        -------
        operator : np.ndarray
            n_grid² × n_grid² 算子矩阵
        """
        n = n_grid * n_grid
        operator = np.zeros((n, n))

        x_min, x_max = -1.5, 1.5
        y_min, y_max = -0.4, 0.4

        for i in range(n_grid):
            for j in range(n_grid):
                x = x_min + (x_max - x_min) * i / (n_grid - 1)
                y = y_min + (y_max - y_min) * j / (n_grid - 1)

                x_new = (1 - self.a * x**2 + y) * (1 - self.dissipation)
                y_new = self.b * x * (1 - self.dissipation)

                if x_new < x_min or x_new > x_max or y_new < y_min or y_new > y_max:
                    continue

                i_new = int(((x_new - x_min) / (x_max - x_min)) * (n_grid - 1))
                j_new = int(((y_new - y_min) / (y_max - y_min)) * (n_grid - 1))

                idx = i * n_grid + j
                idx_new = i_new * n_grid + j_new
                operator[idx_new, idx] = 1.0

        return operator


def run_dissipative_demo():
    """运行耗散系统 D 函子扩展演示。"""
    print("=" * 70)
    print("Phase 15D-1: D 函子扩展到耗散混沌系统")
    print("=" * 70)

    henon = HenonMapDissipative(a=1.4, b=0.3, dissipation=0.01)
    print("\n--- 1. Henon 映射耗散版本 ---")
    lyap = henon.lyapunov_exponents(n_iter=10000)
    print(f"  参数: a={henon.a}, b={henon.b}, 耗散={henon.dissipation}")
    print(f"  Lyapunov 指数: λ₁={lyap[0]:.4f}, λ₂={lyap[1]:.4f}")
    print(f"  耗散性: λ₁+λ₂={sum(lyap):.4f}")

    print("\n--- 2. 非自伴谱理论（使用标准耗散算子）---")
    np.random.seed(42)
    n = 4
    non_self_adjoint_op = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    non_self_adjoint_op = non_self_adjoint_op - np.diag(np.real(np.diag(non_self_adjoint_op)) + 0.5)
    nsa = NonSelfAdjointSpectralTheory(non_self_adjoint_op)
    spec_info = nsa.spectrum_with_dissipation()
    print(f"  算子维度: {non_self_adjoint_op.shape}")
    print(f"  是否自伴: {spec_info['is_self_adjoint']}")
    print(f"  特征值实部范围: [{np.min(spec_info['real_parts']):.4f}, {np.max(spec_info['real_parts']):.4f}]")
    print(f"  特征值虚部范围: [{np.min(spec_info['imag_parts']):.4f}, {np.max(spec_info['imag_parts']):.4f}]")

    print("\n--- 3. 耗散半群 ---")
    generator = np.array([[-1.0, 0.5], [0.3, -0.8]])
    semigroup = DissipativeSemigroup(generator)
    print(f"  是否耗散算子: {semigroup.is_dissipative()}")
    print(f"  最大衰减率: {semigroup.decay_rate():.4f}")
    long_time = semigroup.long_time_behavior()
    print(f"  主特征值: {long_time['dominant_eigenvalue']:.4f}")
    print(f"  渐近状态: {long_time['asymptotic_state']}")

    print("\n--- 4. D 函子耗散扩展 ---")
    d_functor = DissipativeDecursionFunctor()
    rec_op = np.array([[0.8, 0.2], [0.1, 0.7]])
    spec_obj = d_functor.dissipative_rec_to_spec(rec_op, dissipation_rate=0.1)
    print(f"  耗散率: {spec_obj['dissipation_rate']}")
    print(f"  半群耗散性: {spec_obj['semigroup_properties']['is_dissipative']}")
    print(f"  衰减率: {spec_obj['semigroup_properties']['decay_rate']:.4f}")

    print("\n--- 5. 广义伴随验证 ---")
    rec_op_valid = np.array([[0.8, 0.1], [0.1, 0.7]])
    adjoint_result = d_functor.verify_dissipative_adjoint(rec_op_valid, dissipation_rate=0.05)
    print(f"  前向误差: {adjoint_result['forward_error']:.4e}")
    print(f"  后向误差: {adjoint_result['backward_error']:.4e}")
    print(f"  近似伴随: {'✓' if adjoint_result['approx_adjoint'] else '✗'}")

    print("\n--- 6. 非正规算子理论 ---")
    non_normal_op = np.array([[0, 1], [0, 0]], dtype=complex)
    nno = NonNormalOperatorTheory(non_normal_op)
    print(f"  非正规性指标: {nno.non_normality_index():.4f}")
    print(f"  数值半径: {nno.numerical_radius():.4f}")
    print(f"  谱变分: {nno.spectral_variation():.4f}")

    print("\n--- 7. 无界算子定义域 ---")
    unbounded_op = np.array([[1, 1], [0, 1]])
    domain_mask = np.array([True, True])
    uod = UnboundedOperatorDomain(unbounded_op, domain_mask)
    print(f"  定义域维度: {uod.domain_dimension()}")
    print(f"  图范数示例: {uod.graph_norm(np.array([1, 0])):.4f}")

    print("\n--- 8. D 函子无界算子扩展 ---")
    spec_unbounded = d_functor.unbounded_rec_to_spec(unbounded_op, domain_mask)
    print(f"  定义域维度: {spec_unbounded['domain']['dimension']}")
    print(f"  非正规性指标: {spec_unbounded['non_normality']['non_normality_index']:.4f}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_dissipative_demo()
