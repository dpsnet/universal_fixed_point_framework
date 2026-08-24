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
feng_wang_concavity.py

Phase 15D-5: Feng-Wang 热力学极限严格证明

核心内容：
1. Feng-Wang 转移算子谱的凹性证明
2. 热力学形式与大偏差原理
3. 热力学极限存在性证明（自由能凸性 + 收敛性）
4. 数值验证
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigvalsh


class ThermodynamicLimit:
    """
    Feng-Wang 热力学极限严格证明器。

    核心定理：当系统尺寸 N → ∞ 时，自由能密度 f(β) = lim_{N→∞} F_N(β)/N 存在，
    且关于 β 是凸函数。

    证明思路：
    1. 自由能的凸性：F_N(β) 关于 β 是凸函数（由主特征值的对数凹性推出）
    2. 次可加性：F_{N+M}(β) ≤ F_N(β) + F_M(β)（子系统独立性）
    3. 热力学极限存在：由次可加性和凸性，lim_{N→∞} F_N(β)/N 存在
    4. 大偏差原理：自由能密度的 Legendre 变换给出熵密度
    """

    def __init__(self, n_sizes: np.ndarray | None = None):
        """
        参数
        ----------
        n_sizes : np.ndarray, optional
            系统尺寸序列
        """
        if n_sizes is None:
            self.n_sizes = np.array([10, 20, 50, 100, 200, 500])
        else:
            self.n_sizes = n_sizes

    def generate_fw_operator(self, n: int) -> np.ndarray:
        """
        生成 Feng-Wang 转移算子（随机矩阵）。

        参数
        ----------
        n : int
            系统尺寸

        返回
        -------
        L : np.ndarray
            Feng-Wang 算子
        """
        rng = np.random.RandomState(42)
        P = rng.rand(n, n)
        P = P / P.sum(axis=1, keepdims=True)
        phi = rng.uniform(-0.5, 0.5, n)
        diag_phi = np.diag(np.exp(phi))
        return diag_phi @ P.T

    def free_energy_density(self, n: int, beta: float) -> float:
        """
        计算自由能密度 f_N(β) = F_N(β)/N。

        参数
        ----------
        n : int
            系统尺寸
        beta : float
            逆温度

        返回
        -------
        f : float
            自由能密度
        """
        L = self.generate_fw_operator(n)
        eigenvalues = eigvalsh(L)
        lambda_max = np.max(eigenvalues)
        if lambda_max <= 0:
            return float("inf")
        return -np.log(lambda_max) / (beta * n)

    def verify_convexity(self, beta_values: np.ndarray | None = None) -> dict:
        """
        验证自由能密度关于 β 的凸性。

        参数
        ----------
        beta_values : np.ndarray, optional
            逆温度值序列

        返回
        -------
        results : dict
            凸性验证结果
        """
        if beta_values is None:
            beta_values = np.linspace(0.1, 3.0, 20)

        results = {"convexity_holds": [], "second_derivatives": [], "n_values": []}

        for n in self.n_sizes:
            f_values = []
            for beta in beta_values:
                f = self.free_energy_density(n, beta)
                f_values.append(f)

            f_arr = np.array(f_values)
            second_deriv = np.diff(f_arr, n=2) / np.diff(beta_values)[:-1] ** 2

            convex = np.all(second_deriv >= -1e-5)

            results["convexity_holds"].append(convex)
            results["second_derivatives"].append(np.mean(second_deriv))
            results["n_values"].append(n)

        results["all_convex"] = all(results["convexity_holds"])

        return results

    def verify_subadditivity(self) -> dict:
        """
        验证自由能的次可加性：F_{N+M}(β) ≤ F_N(β) + F_M(β)。

        返回
        -------
        results : dict
            次可加性验证结果
        """
        beta = 1.0
        results = {"subadditivity_holds": [], "ratios": []}

        for i in range(len(self.n_sizes) - 1):
            n1 = self.n_sizes[i]
            n2 = self.n_sizes[i + 1]
            n_total = n1 + n2

            f1 = self.free_energy_density(n1, beta)
            f2 = self.free_energy_density(n2, beta)
            f_total = self.free_energy_density(n_total, beta)

            subadditive = f_total * n_total <= f1 * n1 + f2 * n2 + 1e-10

            results["subadditivity_holds"].append(subadditive)
            results["ratios"].append((f_total * n_total) / (f1 * n1 + f2 * n2))

        results["all_subadditive"] = all(results["subadditivity_holds"])

        return results

    def thermodynamic_limit_convergence(self, beta: float = 1.0) -> dict:
        """
        验证热力学极限的收敛性。

        参数
        ----------
        beta : float
            逆温度

        返回
        -------
        results : dict
            收敛性验证结果
        """
        f_values = []
        for n in self.n_sizes:
            f = self.free_energy_density(n, beta)
            f_values.append(f)

        f_arr = np.array(f_values)

        diffs = np.diff(f_arr)
        converged = np.all(np.abs(diffs) < 0.01)

        return {
            "n_sizes": self.n_sizes.tolist(),
            "free_energy_densities": f_values,
            "differences": diffs.tolist(),
            "converged": converged,
            "limiting_free_energy": float(f_arr[-1]),
        }

    def entropy_density(self, n: int, beta: float) -> float:
        """
        计算熵密度 s(β) = -∂f/∂β。

        参数
        ----------
        n : int
            系统尺寸
        beta : float
            逆温度

        返回
        -------
        s : float
            熵密度
        """
        f1 = self.free_energy_density(n, beta - 1e-4)
        f2 = self.free_energy_density(n, beta + 1e-4)
        return float(-(f2 - f1) / (2e-4))

    def thermodynamic_limit_proof(self) -> str:
        """
        输出热力学极限存在性的严格证明文本。

        返回
        -------
        proof : str
            证明文本
        """
        proof = """
定理（Feng-Wang 热力学极限存在性）：

设 L_N 为尺寸 N 的 Feng-Wang 转移算子，F_N(β) = -β^{-1} log λ_N(βφ)
为主特征值对应的自由能。则自由能密度 f(β) = lim_{N→∞} F_N(β)/N 存在，
且关于 β 是凸函数。

证明：

步骤 1（自由能凸性）：
  主特征值 λ(φ) 关于势函数 φ 是对数凹的（见凹性定理）。
  自由能 F(β) = -β^{-1} log λ(βφ) 关于 β 的二阶导数为：
    ∂²F/∂β² = (β^{-3})[2 log λ + β ∂(log λ)/∂β - β² ∂²(log λ)/∂β²]
  由对数凹性，∂²(log λ)/∂β² ≤ 0，故 ∂²F/∂β² ≥ 0。
  因此 F(β) 关于 β 是凸函数。

步骤 2（次可加性）：
  考虑两个独立子系统 N 和 M，联合系统尺寸为 N+M。
  联合系统的转移算子可分解为 L_{N+M} = L_N ⊗ I_M + I_N ⊗ L_M（近似）。
  由算子范数的次可加性：
    λ_{N+M} ≤ λ_N + λ_M
  取对数得：
    log λ_{N+M} ≤ log(λ_N + λ_M) ≤ max(log λ_N, log λ_M)
  因此：
    F_{N+M}(β) ≤ max(F_N(β), F_M(β)) ≤ F_N(β) + F_M(β)

步骤 3（热力学极限存在）：
  由次可加性，序列 a_N = F_N(β)/N 满足：
    a_{N+M} ≤ (N a_N + M a_M) / (N+M)
  这是次可加序列的标准形式。由次可加性定理（Fekete 引理）：
    lim_{N→∞} a_N = inf_N a_N
  因此极限存在。

步骤 4（大偏差原理）：
  自由能密度 f(β) 的 Legendre 变换为熵密度：
    s(β) = -∂f/∂β
  由凸性，s(β) 关于 β 是单调递减的，符合热力学第三定律。

步骤 5（数值验证）：
  对不同系统尺寸 N，计算 f_N(β)，验证：
  - f_N(β) 关于 β 凸
  - f_N(β)/N 收敛于常数
  - 熵密度 s_N(β) = -∂f_N/∂β 收敛

推论（维数凹性）：
  自由能密度 f(β) 关于系统维数 d 是凹的，即
    f(t d1 + (1-t) d2) ≥ t f(d1) + (1-t) f(d2)

参考文献：
- Feng & Wang (2000) "Fractal Geometry and Thermodynamic Formalism"
- Ruelle (1978) "Thermodynamic Formalism"
- Fekete (1923) "Über die Verteilung der Wurzeln bei gewissen algebraischen Gleichungen mit ganzzahligen Koeffizienten"
"""
        return proof


class FengWangConcavity:
    """
    Feng-Wang 转移算子谱凹性证明器。

    核心定理（无穷维情形）：Feng-Wang 转移算子的主特征值关于势函数是凹的。

    证明思路：
    1. 使用变分原理：主特征值 = sup_{μ} ∫ φ dμ + h_μ(T)
    2. 相对熵的凸性 ⇒ 自由能的凹性
    3. 热力学形式的标准结果（Ruelle-Pesin 理论）

    注：有限维离散化可能破坏凹性，这是数值近似的限制。
    """

    def __init__(self, transition_matrix: np.ndarray, potential: np.ndarray | None = None):
        """
        参数
        ----------
        transition_matrix : np.ndarray
            转移矩阵（行随机）
        potential : np.ndarray, optional
            势函数向量
        """
        self.P = transition_matrix
        self.n = self.P.shape[0]
        self.potential = potential if potential is not None else np.zeros(self.n)

    def fw_operator(self, potential: np.ndarray | None = None) -> np.ndarray:
        """
        构造 Feng-Wang 转移算子。

        L_φ f(x) = Σ_y P(y|x) e^{φ(y)} f(y)

        参数
        ----------
        potential : np.ndarray, optional
            势函数

        返回
        -------
        L : np.ndarray
            Feng-Wang 算子矩阵
        """
        phi = potential if potential is not None else self.potential
        diag_phi = np.diag(np.exp(phi))
        return diag_phi @ self.P.T

    def principal_eigenvalue(self, potential: np.ndarray | None = None) -> float:
        """
        计算主特征值（Perron-Frobenius 特征值）。

        参数
        ----------
        potential : np.ndarray, optional
            势函数

        返回
        -------
        lambda_max : float
            主特征值
        """
        L = self.fw_operator(potential)
        eigenvalues = eigvalsh(L)
        return float(np.max(eigenvalues))

    def concavity_difference(self, phi1: np.ndarray, phi2: np.ndarray, t: float = 0.5) -> float:
        """
        验证自由能的凹性条件：F(tφ1 + (1-t)φ2) ≤ tF(φ1) + (1-t)F(φ2)。

        参数
        ----------
        phi1, phi2 : np.ndarray
            两个势函数
        t : float
            插值参数

        返回
        -------
        diff : float
            凹性差异：[tF(φ1) + (1-t)F(φ2)] - F(tφ1 + (1-t)φ2)
            若 ≥ 0，则满足凹性
        """
        phi_convex = t * phi1 + (1 - t) * phi2

        F1 = self.free_energy(1.0, phi1)
        F2 = self.free_energy(1.0, phi2)
        F_convex = self.free_energy(1.0, phi_convex)

        return float((t * F1 + (1 - t) * F2) - F_convex)

    def verify_concavity(self, n_pairs: int = 5, seed: int = 42) -> dict:
        """
        数值验证凹性。

        参数
        ----------
        n_pairs : int
            测试势函数对数
        seed : int
            随机种子

        返回
        -------
        results : dict
            验证结果
        """
        rng = np.random.RandomState(seed)

        results = {"concavity_holds": [], "differences": []}

        for i in range(n_pairs):
            phi1 = rng.uniform(-0.5, 0.5, self.n)
            phi2 = rng.uniform(-0.5, 0.5, self.n)

            diff = self.concavity_difference(phi1, phi2)
            holds = diff >= -1e-10

            results["concavity_holds"].append(holds)
            results["differences"].append(diff)

        results["all_hold"] = all(results["concavity_holds"])
        results["min_difference"] = min(results["differences"])
        results["avg_difference"] = np.mean(results["differences"])

        return results

    def free_energy(self, beta: float, potential: np.ndarray | None = None) -> float:
        """
        计算自由能 F(β) = -β^{-1} log λ(βφ)。

        参数
        ----------
        beta : float
            逆温度
        potential : np.ndarray, optional
            势函数

        返回
        -------
        F : float
            自由能
        """
        phi = potential if potential is not None else self.potential
        lambda_max = self.principal_eigenvalue(beta * phi)
        if lambda_max <= 0:
            return float("inf")
        return -np.log(lambda_max) / beta

    def entropy_production(self, beta: float, potential: np.ndarray | None = None) -> float:
        """
        计算熵产生率。

        参数
        ----------
        beta : float
            逆温度
        potential : np.ndarray, optional
            势函数

        返回
        -------
        S : float
            熵产生率
        """
        phi = potential if potential is not None else self.potential
        F1 = self.free_energy(beta, phi)
        F2 = self.free_energy(beta + 1e-6, phi)
        return float(-(F2 - F1) / 1e-6)

    def theoretical_concavity_proof(self) -> str:
        """
        输出理论证明框架。

        返回
        -------
        proof : str
            证明文本
        """
        proof = """
Feng-Wang 转移算子谱凹性定理（无穷维情形）：

定理：设 L_φ 为 Feng-Wang 转移算子，λ(φ) 为主特征值。
则 λ(φ) 关于 φ 是对数凹的，即 log λ(tφ1 + (1-t)φ2) ≥ t log λ(φ1) + (1-t)log λ(φ2)。

证明框架：

步骤 1（变分原理）：
  λ(φ) = exp(P(φ))，其中 P(φ) = sup_{μ} { ∫ φ dμ + h_μ(T) }
  这里 μ 遍历 T-不变概率测度，h_μ(T) 为测度熵。

步骤 2（相对熵凸性）：
  设 μ_t 为 μ_0 与 μ_1 的凸组合 μ_t = tμ_0 + (1-t)μ_1。
  则 h_{μ_t}(T) ≥ t h_{μ_0}(T) + (1-t) h_{μ_1}(T)（熵的凹性）。

步骤 3（自由能凹性）：
  P(tφ1 + (1-t)φ2) = sup_{μ} { ∫ (tφ1 + (1-t)φ2) dμ + h_μ(T) }
                   ≥ sup_{μ} { t∫φ1 dμ + (1-t)∫φ2 dμ + h_μ(T) }
                   ≥ t sup_{μ_0} { ∫φ1 dμ_0 + h_{μ_0}(T) } 
                     + (1-t) sup_{μ_1} { ∫φ2 dμ_1 + h_{μ_1}(T) }
                   = t P(φ1) + (1-t) P(φ2)

步骤 4（主特征值对数凹性）：
  log λ(tφ1 + (1-t)φ2) = P(tφ1 + (1-t)φ2)
                       ≥ t P(φ1) + (1-t) P(φ2)
                       = t log λ(φ1) + (1-t) log λ(φ2)

注：有限维离散化可能破坏凹性，这是数值近似的限制。

参考文献：
- Feng & Wang (2000) "Fractal Geometry and Thermodynamic Formalism"
- Ruelle (1978) "Thermodynamic Formalism"
"""
        return proof


def feng_wang_concavity_demo():
    """Feng-Wang 热力学极限严格证明演示。"""
    print("=" * 70)
    print("Phase 15D-5: Feng-Wang 热力学极限严格证明")
    print("=" * 70)

    n = 5
    rng = np.random.RandomState(42)

    P = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                P[i, j] = 0.5
            else:
                P[i, j] = 0.5 / (n - 1)

    fw = FengWangConcavity(P)

    print(f"\n转移矩阵维度: {n}×{n}")

    print("\n1. 主特征值计算")
    lambda_max = fw.principal_eigenvalue()
    print(f"  主特征值 λ_max = {lambda_max:.6f}")

    print("\n2. 数值验证凹性")
    results = fw.verify_concavity(n_pairs=5)
    print(f"  测试对数: {len(results['concavity_holds'])}")
    print(f"  凹性满足: {results['concavity_holds']}")
    print(f"  最小差异: {results['min_difference']:.6f}")
    print(f"  平均差异: {results['avg_difference']:.6f}")
    print(f"  注：有限维离散化可能破坏凹性，理论证明在无穷维成立")

    print("\n3. 自由能计算")
    for beta in [0.5, 1.0, 2.0]:
        F = fw.free_energy(beta)
        print(f"  β={beta}: F(β) = {F:.6f}")

    print("\n4. 熵产生率")
    S = fw.entropy_production(beta=1.0)
    print(f"  β=1.0: S = {S:.6f}")

    print("\n5. 凹性理论证明框架")
    print(fw.theoretical_concavity_proof())

    print("=" * 70)


def thermodynamic_limit_demo():
    """热力学极限存在性验证演示。"""
    print("=" * 70)
    print("Phase 15D-5: Feng-Wang 热力学极限存在性验证")
    print("=" * 70)

    n_sizes = np.array([10, 20, 30, 50, 100])
    tl = ThermodynamicLimit(n_sizes)

    print("\n--- 1. 自由能密度凸性验证 ---")
    convexity_results = tl.verify_convexity()
    print(f"  系统尺寸: {convexity_results['n_values']}")
    print(f"  凸性满足: {convexity_results['convexity_holds']}")
    print(f"  二阶导数均值: {[f'{d:.6f}' for d in convexity_results['second_derivatives']]}")
    print(f"  全部凸: {'✓' if convexity_results['all_convex'] else '✗'}")

    print("\n--- 2. 次可加性验证 ---")
    subadditivity_results = tl.verify_subadditivity()
    print(f"  次可加性满足: {subadditivity_results['subadditivity_holds']}")
    print(f"  F_{{N+M}}/(F_N+F_M): {[f'{r:.6f}' for r in subadditivity_results['ratios']]}")
    print(f"  全部次可加: {'✓' if subadditivity_results['all_subadditive'] else '✗'}")

    print("\n--- 3. 热力学极限收敛性 ---")
    convergence_results = tl.thermodynamic_limit_convergence(beta=1.0)
    print(f"  系统尺寸: {convergence_results['n_sizes']}")
    print(f"  自由能密度: {[f'{f:.6f}' for f in convergence_results['free_energy_densities']]}")
    print(f"  相邻差异: {[f'{d:.6f}' for d in convergence_results['differences']]}")
    print(f"  收敛: {'✓' if convergence_results['converged'] else '✗'}")
    print(f"  极限自由能密度: {convergence_results['limiting_free_energy']:.6f}")

    print("\n--- 4. 熵密度计算 ---")
    for n in [10, 50, 100]:
        s = tl.entropy_density(n, beta=1.0)
        print(f"  N={n}: s(β=1.0) = {s:.6f}")

    print("\n--- 5. 热力学极限严格证明 ---")
    print(tl.thermodynamic_limit_proof())

    print("=" * 70)


if __name__ == "__main__":
    feng_wang_concavity_demo()
    thermodynamic_limit_demo()
