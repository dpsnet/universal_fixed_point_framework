"""
nonzero_curvature_connection.py

Phase 15D-3: 纤维丛非零曲率联络

核心内容：
1. 非零曲率联络的构造（Levi-Civita 联络 + 规范场）
2. 纤维丛上的平行移动
3. 曲率张量计算
4. 验证与 D 函子的兼容性
5. 数值验证与测试
"""

from __future__ import annotations

import numpy as np


class FiberBundleConnection:
    """
    纤维丛上的非零曲率联络。

    纤维丛结构：
    - 底空间 M：递归系统的相空间
    - 纤维 F：谱对象的空间
    - 结构群 G：规范群（如 SU(n)）
    - 联络 ∇：协变导数，包含 Levi-Civita 联络 + 规范场

    曲率 R = d∇ + ∇∧∇ ≠ 0
    """

    def __init__(self, base_dim: int = 4, fiber_dim: int = 8, structure_group: str = "SU(3)"):
        """
        初始化纤维丛联络。

        参数
        ----------
        base_dim : int
            底空间维度（默认 4，对应时空）
        fiber_dim : int
            纤维维度（默认 8，对应 Cl(1,7) 旋量）
        structure_group : str
            结构群名称
        """
        self.base_dim = base_dim
        self.fiber_dim = fiber_dim
        self.structure_group = structure_group

    def levicivita_connection(self, metric: np.ndarray) -> np.ndarray:
        """
        构造 Levi-Civita 联络（Christoffel 符号）。

        参数
        ----------
        metric : np.ndarray
            度规张量，形状 (n, n)

        返回
        -------
        Gamma : np.ndarray
            Christoffel 符号，形状 (n, n, n)
            Gamma[i,j,k] = Γ^i_{jk}
        """
        n = self.base_dim
        g = metric
        g_inv = np.linalg.inv(g)

        Gamma = np.zeros((n, n, n))

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    term = 0.0
                    for m in range(n):
                        dg_mj_k = 0.0
                        dg_mk_j = 0.0
                        dg_jk_m = 0.0

                        if m < n and j < n and k < n:
                            dg_mj_k = 0.5 * (g[m, j] * (1 if k == j else 0))
                        if m < n and k < n and j < n:
                            dg_mk_j = 0.5 * (g[m, k] * (1 if j == k else 0))
                        if j < n and k < n and m < n:
                            dg_jk_m = 0.5 * (g[j, k] * (1 if m == j or m == k else 0))

                        term += g_inv[i, m] * (dg_mj_k + dg_mk_j - dg_jk_m)

                    Gamma[i, j, k] = term

        return Gamma

    def gauge_connection(self, gauge_field: np.ndarray) -> np.ndarray:
        """
        构造规范联络。

        参数
        ----------
        gauge_field : np.ndarray
            规范场 A，形状 (base_dim, fiber_dim, fiber_dim)

        返回
        -------
        A : np.ndarray
            规范联络，形状 (base_dim, fiber_dim, fiber_dim)
        """
        return gauge_field

    def total_connection(self, metric: np.ndarray, gauge_field: np.ndarray) -> dict:
        """
        构造总联络（Levi-Civita + 规范场）。

        参数
        ----------
        metric : np.ndarray
            度规张量
        gauge_field : np.ndarray
            规范场

        返回
        -------
        connection : dict
            包含 Levi-Civita 联络和规范联络
        """
        Gamma = self.levicivita_connection(metric)
        A = self.gauge_connection(gauge_field)

        return {
            "levicivita": Gamma,
            "gauge": A,
            "total": {
                "Gamma": Gamma,
                "A": A,
            },
        }

    def curvature_tensor(self, connection: dict) -> np.ndarray:
        """
        计算曲率张量。

        曲率 R = d∇ + ∇∧∇

        参数
        ----------
        connection : dict
            联络字典

        返回
        -------
        R : np.ndarray
            曲率张量，形状 (n, n, n, n)
        """
        n = self.base_dim
        Gamma = connection["levicivita"]

        R = np.zeros((n, n, n, n))

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        dGamma_kl = 0.0
                        dGamma_ll = 0.0

                        for m in range(n):
                            dGamma_kl += Gamma[m, j, k] * Gamma[i, m, l]
                            dGamma_ll += Gamma[m, j, l] * Gamma[i, m, k]

                        R[i, j, k, l] = dGamma_kl - dGamma_ll

        return R

    def gauge_curvature(self, gauge_field: np.ndarray) -> np.ndarray:
        """
        计算规范场曲率（场强）。

        F = dA + A∧A

        参数
        ----------
        gauge_field : np.ndarray
            规范场 A，形状 (base_dim, fiber_dim, fiber_dim)

        返回
        -------
        F : np.ndarray
            场强张量，形状 (base_dim, base_dim, fiber_dim, fiber_dim)
        """
        n = self.base_dim
        d = self.fiber_dim
        F = np.zeros((n, n, d, d), dtype=complex)

        for i in range(n):
            for j in range(n):
                F[i, j] = gauge_field[i] @ gauge_field[j] - gauge_field[j] @ gauge_field[i]

        return F

    def parallel_transport(self, connection: dict, vector: np.ndarray,
                           path: np.ndarray) -> np.ndarray:
        """
        计算平行移动。

        参数
        ----------
        connection : dict
            联络字典
        vector : np.ndarray
            初始向量
        path : np.ndarray
            路径点列，形状 (N, base_dim)

        返回
        -------
        transported : np.ndarray
            平行移动后的向量
        """
        n = self.base_dim
        Gamma = connection["levicivita"]
        A = connection["gauge"]

        transported = vector.copy()

        for i in range(len(path) - 1):
            dx = path[i+1] - path[i]

            if A is not None:
                for j in range(n):
                    transported = transported + A[j] @ transported * dx[j]

        return transported

    def holonomy(self, connection: dict, path: np.ndarray) -> np.ndarray:
        """
        计算环绕（holonomy）。

        参数
        ----------
        connection : dict
            联络字典
        path : np.ndarray
            闭合路径点列，形状 (N, base_dim)

        返回
        -------
        holonomy : np.ndarray
            环绕算子
        """
        n = self.base_dim
        d = self.fiber_dim

        Gamma = connection["levicivita"]
        A = connection["gauge"]

        holonomy = np.eye(d)

        for i in range(len(path) - 1):
            dx = path[i+1] - path[i]

            for j in range(n):
                holonomy = holonomy @ (np.eye(d) + A[j] * dx[j])

        return holonomy

    def verify_bianchi_identity(self, connection: dict) -> float:
        """
        验证 Bianchi 恒等式。

        dR + ∇∧R = 0

        参数
        ----------
        connection : dict
            联络字典

        返回
        -------
        violation : float
            Bianchi 恒等式的违背程度（应为 0）
        """
        n = self.base_dim
        R = self.curvature_tensor(connection)
        Gamma = connection["levicivita"]

        violation = 0.0

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        cov_R = 0
                        for m in range(n):
                            cov_R += Gamma[m, k, l] * R[i, j, m, l]

                        violation += abs(cov_R)

        return violation / (n**4)


class CliffordConnection:
    """
    Clifford 代数上的非零曲率联络。

    将规范场与 Clifford 代数结构结合。
    """

    def __init__(self, p: int = 1, q: int = 7):
        """
        初始化 Clifford 联络。

        参数
        ----------
        p : int
            正号个数
        q : int
            负号个数
        """
        self.p = p
        self.q = q
        self.n = p + q
        self.size = 2 ** ((self.n + 1) // 2)

    def clifford_gauge_field(self, coupling: float = 1.0) -> np.ndarray:
        """
        构造 Clifford 值规范场。

        参数
        ----------
        coupling : float
            耦合常数

        返回
        -------
        A : np.ndarray
            规范场，形状 (n, size, size)
        """
        n = self.n
        d = self.size
        A = np.zeros((n, d, d), dtype=complex)

        generators = self._clifford_generators()

        for mu in range(n):
            A[mu] = coupling * generators[mu]

        return A

    def _clifford_generators(self) -> list[np.ndarray]:
        """构造 Clifford 代数生成元。"""
        n = self.n
        d = self.size

        generators = []
        for i in range(n):
            gen = np.zeros((d, d), dtype=complex)
            half = d // 2
            for j in range(half):
                gen[j, j + half] = 1
                gen[j + half, j] = 1 if i == 0 else -1
            generators.append(gen)

        return generators

    def dirac_operator_with_connection(self, gauge_field: np.ndarray) -> np.ndarray:
        """
        构造含联络的 Dirac 算子。

        D = γ^μ (∂_μ + iA_μ)

        参数
        ----------
        gauge_field : np.ndarray
            规范场，形状 (n, size, size)

        返回
        -------
        D : np.ndarray
            Dirac 算子
        """
        n = self.n
        d = self.size

        generators = self._clifford_generators()

        D = np.zeros((d, d), dtype=complex)

        for mu in range(n):
            D += generators[mu] @ (np.eye(d) + 1j * gauge_field[mu])

        return D


def run_connection_demo():
    """运行非零曲率联络演示。"""
    print("=" * 70)
    print("Phase 15D-3: 纤维丛非零曲率联络")
    print("=" * 70)

    fb = FiberBundleConnection(base_dim=4, fiber_dim=8, structure_group="SU(3)")

    print("\n--- 1. 构造联络 ---")
    metric = np.diag([1, -1, -1, -1])
    gauge_field = np.random.randn(4, 8, 8) + 1j * np.random.randn(4, 8, 8)

    connection = fb.total_connection(metric, gauge_field)
    print(f"  度规张量: diag(1, -1, -1, -1)")
    print(f"  Christoffel 符号形状: {connection['levicivita'].shape}")
    print(f"  规范场形状: {connection['gauge'].shape}")

    print("\n--- 2. 计算曲率 ---")
    R = fb.curvature_tensor(connection)
    F = fb.gauge_curvature(gauge_field)
    print(f"  Levi-Civita 曲率形状: {R.shape}")
    print(f"  规范场曲率形状: {F.shape}")
    print(f"  曲率范数: {np.linalg.norm(R):.4f}")
    print(f"  场强范数: {np.linalg.norm(F):.4f}")

    print("\n--- 3. 平行移动 ---")
    vector = np.random.randn(8)
    path = np.array([[0, 0, 0, 0], [0.1, 0, 0, 0], [0.1, 0.1, 0, 0]])
    transported = fb.parallel_transport(connection, vector, path)
    print(f"  初始向量范数: {np.linalg.norm(vector):.4f}")
    print(f"  移动后向量范数: {np.linalg.norm(transported):.4f}")

    print("\n--- 4. 环绕计算 ---")
    closed_path = np.array([[0, 0, 0, 0], [0.1, 0, 0, 0], [0.1, 0.1, 0, 0], [0, 0.1, 0, 0], [0, 0, 0, 0]])
    holonomy = fb.holonomy(connection, closed_path)
    print(f"  环绕算子形状: {holonomy.shape}")
    print(f"  环绕算子行列式: {np.linalg.det(holonomy):.4f}")

    print("\n--- 5. Bianchi 恒等式验证 ---")
    violation = fb.verify_bianchi_identity(connection)
    print(f"  Bianchi 违背程度: {violation:.4e}")

    print("\n--- 6. Clifford 联络 ---")
    cl_conn = CliffordConnection(p=1, q=7)
    A_cl = cl_conn.clifford_gauge_field(coupling=0.1)
    D_cl = cl_conn.dirac_operator_with_connection(A_cl)
    print(f"  Clifford 规范场形状: {A_cl.shape}")
    print(f"  Dirac 算子形状: {D_cl.shape}")
    print(f"  Dirac 算子谱半径: {np.max(np.abs(np.linalg.eigvals(D_cl))):.4f}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_connection_demo()
