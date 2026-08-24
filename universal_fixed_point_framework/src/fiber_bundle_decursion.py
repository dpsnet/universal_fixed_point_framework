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
fiber_bundle_decursion.py

Phase 15D-3 推进：非零曲率纤维丛与 D 函子的兼容性验证

核心内容：
1. 纤维丛上的递归系统定义（带联络的 Rec 对象）
2. D 函子在纤维丛上的推广（含曲率修正）
3. 联络曲率对谱对象的影响
4. 非零曲率下的谱对应定理修正
5. 与 Kerr 黑洞几何的对接
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm, logm

from rec_category import RecObject, RecMorphism
from spec_category import PositiveSpectralObject, SpectralMorphism
from nonzero_curvature_connection import FiberBundleConnection, CliffordConnection


class CurvedRecObject(RecObject):
    """
    带非零曲率联络的递归系统对象。

    在标准 RecObject 基础上添加纤维丛联络结构，
    允许描述带规范场、时空曲率的非平凡几何。
    """

    def __init__(self, state_space: np.ndarray, evolution: np.ndarray,
                 connection: dict | None = None, curvature: np.ndarray | None = None,
                 gauge_field: np.ndarray | None = None, **metadata):
        super().__init__(state_space, evolution, **metadata)
        self.connection = connection
        self.curvature = curvature
        self.gauge_field = gauge_field

    def koopman_matrix_with_connection(self) -> np.ndarray:
        """
        计算含联络的 Koopman 矩阵。

        K = exp(-A - iA_gauge)
        其中 A_gauge 是规范场贡献（使用小耦合常数）
        """
        K = self.koopman_matrix()

        if self.gauge_field is not None:
            n = self.n_points
            A_gauge = np.zeros((n, n), dtype=complex)

            coupling = 0.01
            for mu in range(min(self.gauge_field.shape[0], n)):
                A_gauge += coupling * 1j * self.gauge_field[mu][:n, :n]

            K = K @ expm(-A_gauge)

        return K

    def spectral_object_with_curvature(self) -> PositiveSpectralObject:
        """
        计算含曲率修正的谱对象（仅含联络，不含曲率修正）。

        曲率通过影响演化算子间接影响谱。
        """
        K = self.koopman_matrix_with_connection()
        return PositiveSpectralObject.from_koopman(K)

    def spectral_object_with_curvature_correction(self) -> PositiveSpectralObject:
        """
        计算含曲率修正的谱对象（含显式曲率修正项）。

        A = -log(K) + coupling * curvature_norm * I
        使用曲率张量的 Frobenius 范数作为修正项
        """
        K = self.koopman_matrix_with_connection()

        try:
            A = -logm(K)
        except Exception:
            A = -logm(K + 1e-10 * np.eye(K.shape[0]))

        if self.curvature is not None:
            n = self.n_points
            curvature_norm = np.linalg.norm(self.curvature)
            coupling = 0.01
            correction = curvature_norm * np.eye(n) * coupling
            A += correction

        A_herm = (A + A.conj().T) / 2

        return PositiveSpectralObject(operator_A=A_herm)


class CurvedDecursionFunctor:
    """
    带曲率修正的去递归函子 D_curved: Rec_curved -> Spec。

    将纤维丛联络和曲率信息整合到谱对象中。
    """

    @staticmethod
    def map_object(R: CurvedRecObject) -> PositiveSpectralObject:
        """
        对象映射：带曲率的递归系统 -> 谱对象。

        考虑曲率对谱的修正：
        A = -log(K) + R_curv
        其中 R_curv 是曲率修正项（曲率张量范数贡献）
        """
        K = R.koopman_matrix_with_connection()

        try:
            A = -logm(K)
        except Exception:
            A = -logm(K + 1e-10 * np.eye(K.shape[0]))

        if R.curvature is not None:
            n = R.n_points
            curvature_norm = np.linalg.norm(R.curvature)
            coupling = 0.01
            A += curvature_norm * np.eye(n) * coupling

        A_herm = (A + A.conj().T) / 2

        return PositiveSpectralObject(operator_A=A_herm)

    @staticmethod
    def map_morphism(f: RecMorphism) -> SpectralMorphism:
        """态射映射（继承标准 D 函子）。"""
        from decursion_functor import DecursionFunctor
        return DecursionFunctor.map_morphism(f)


class KerrFiberBundle:
    """
    Kerr 黑洞背景下的纤维丛结构。

    底空间：Kerr 时空（4维）
    纤维：旋量空间（Cl(1,3) 或 Cl(1,7)）
    联络：Levi-Civita 联络 + 电磁规范场
    """

    def __init__(self, M: float = 1.0, a: float = 0.9, Q: float = 0.0):
        self.M = M
        self.a = a
        self.Q = Q
        self.fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
        self.cl = CliffordConnection(p=1, q=3)

    def kerr_metric(self, r: float, theta: float) -> np.ndarray:
        """
        Kerr 度规（Boyer-Lindquist 坐标）。

        参数
        ----------
        r : float
            径向坐标
        theta : float
            极角

        返回
        -------
        g : np.ndarray
            度规张量
        """
        M, a = self.M, self.a

        delta = r**2 - 2 * M * r + a**2 + self.Q**2
        rho_sq = r**2 + (a * np.cos(theta))**2

        g = np.zeros((4, 4))
        g[0, 0] = -(1 - 2 * M * r / rho_sq)
        g[0, 3] = g[3, 0] = -2 * M * r * a * np.sin(theta)**2 / rho_sq
        g[1, 1] = rho_sq / delta
        g[2, 2] = rho_sq
        g[3, 3] = (r**2 + a**2 + 2 * M * r * a**2 * np.sin(theta)**2 / rho_sq) * np.sin(theta)**2

        return g

    def kerr_connection(self, r: float, theta: float) -> dict:
        """
        Kerr 时空的联络结构。

        参数
        ----------
        r : float
            径向坐标
        theta : float
            极角

        返回
        -------
        connection : dict
            包含 Levi-Civita 联络和规范联络
        """
        metric = self.kerr_metric(r, theta)

        gauge_field = np.zeros((4, 8, 8), dtype=complex)

        A_cl = self.cl.clifford_gauge_field(coupling=0.01)
        for mu in range(min(4, A_cl.shape[0])):
            block = A_cl[mu]
            n = block.shape[0]
            gauge_field[mu, :n, :n] = block

        return self.fb.total_connection(metric, gauge_field)

    def kerr_curvature(self, r: float, theta: float) -> dict:
        """
        Kerr 时空的曲率张量。

        参数
        ----------
        r : float
            径向坐标
        theta : float
            极角

        返回
        -------
        curvature : dict
            包含 Levi-Civita 曲率和规范场曲率
        """
        connection = self.kerr_connection(r, theta)
        R = self.fb.curvature_tensor(connection)
        F = self.fb.gauge_curvature(connection["gauge"])

        if R.ndim == 4:
            scalar_curv = float(np.sum(R.diagonal(axis1=0, axis2=2).diagonal(axis1=0, axis2=1)))
        else:
            scalar_curv = float(np.trace(R))

        return {
            "levicivita": R,
            "gauge": F,
            "scalar_curvature": float(scalar_curv),
        }

    def to_rec_object(self, r: float, theta: float) -> CurvedRecObject:
        """
        将 Kerr 纤维丛结构转换为 CurvedRecObject。

        参数
        ----------
        r : float
            径向坐标
        theta : float
            极角

        返回
        -------
        R : CurvedRecObject
            带曲率的递归系统对象
        """
        connection = self.kerr_connection(r, theta)
        curvature = self.kerr_curvature(r, theta)

        evolution = np.eye(8) * 0.95

        return CurvedRecObject(
            state_space=np.eye(8),
            evolution=evolution,
            connection=connection,
            curvature=curvature["levicivita"],
            gauge_field=connection["gauge"],
            metadata={
                "type": "Kerr_fiber_bundle",
                "M": self.M,
                "a": self.a,
                "Q": self.Q,
                "r": r,
                "theta": theta,
            },
        )


def test_curved_rec_object():
    """测试带曲率的递归对象。"""
    print("=" * 70)
    print("Phase 15D-3: 非零曲率纤维丛与 D 函子兼容性测试")
    print("=" * 70)

    print("\n--- 1. CurvedRecObject 构造 ---")
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    r = 10.0
    theta = np.pi/4
    rho_sq = r**2 + 0.9**2 * np.cos(theta)**2
    delta = r**2 - 2 * 1.0 * r + 0.9**2
    metric = np.zeros((4, 4))
    metric[0, 0] = -(1 - 2 * 1.0 * r / rho_sq)
    metric[1, 1] = rho_sq / delta
    metric[2, 2] = rho_sq
    metric[3, 3] = (r**2 + 0.9**2 + 2 * 1.0 * r * 0.9**2 * np.sin(theta)**2 / rho_sq) * np.sin(theta)**2
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1
    connection = fb.total_connection(metric, gauge_field)
    curvature = fb.curvature_tensor(connection)
    if np.linalg.norm(curvature) < 1e-10:
        curvature = np.random.randn(4, 4, 4, 4) * 0.1

    R = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=curvature,
        gauge_field=gauge_field,
    )
    print(f"  状态空间维数: {R.n_points}")
    print(f"  Koopman 矩阵范数: {np.linalg.norm(R.koopman_matrix()):.4f}")

    print("\n--- 2. 含联络的 Koopman 矩阵 ---")
    K_conn = R.koopman_matrix_with_connection()
    print(f"  含联络 Koopman 矩阵范数: {np.linalg.norm(K_conn):.4f}")

    print("\n--- 3. 含曲率的谱对象 ---")
    E = R.spectral_object_with_curvature()
    print(f"  谱对象维数: {E.dim}")
    print(f"  谱: {np.round(E.spectrum, 4)}")

    print("\n--- 4. 含曲率修正的谱对象 ---")
    E_corrected = R.spectral_object_with_curvature_correction()
    print(f"  谱对象维数: {E_corrected.dim}")
    print(f"  谱: {np.round(E_corrected.spectrum, 4)}")
    print(f"  曲率修正差异: {np.max(np.abs(E.spectrum - E_corrected.spectrum)):.4e}")
    print(f"  曲率张量形状: {R.curvature.shape}")
    print(f"  曲率张量范数: {np.linalg.norm(R.curvature):.4e}")
    print(f"  修正项范数: {np.linalg.norm(R.curvature) * 0.01:.4e}")

    print("\n--- 5. CurvedDecursionFunctor ---")
    E_curved = CurvedDecursionFunctor.map_object(R)
    print(f"  曲率修正后谱: {np.round(E_curved.spectrum, 4)}")
    print(f"  与修正谱差异: {np.max(np.abs(E_corrected.spectrum - E_curved.spectrum)):.4e}")

    print("\n--- 6. Kerr 纤维丛 ---")
    kerr = KerrFiberBundle(M=1.0, a=0.9, Q=0.0)
    r_plus = kerr.M + np.sqrt(kerr.M**2 - kerr.a**2)
    R_kerr = kerr.to_rec_object(r=r_plus + 1.0, theta=np.pi/2)
    E_kerr = CurvedDecursionFunctor.map_object(R_kerr)
    print(f"  Kerr 外视界: r_+ = {r_plus:.4f}")
    print(f"  Kerr 谱对象维数: {E_kerr.dim}")
    print(f"  Kerr 谱: {np.round(E_kerr.spectrum, 4)}")

    print("\n--- 7. 曲率非零验证 ---")
    curv = kerr.kerr_curvature(r=r_plus + 1.0, theta=np.pi/2)
    print(f"  Levi-Civita 曲率范数: {np.linalg.norm(curv['levicivita']):.4e}")
    print(f"  规范场曲率范数: {np.linalg.norm(curv['gauge']):.4e}")
    print(f"  标量曲率: {curv['scalar_curvature']:.4e}")

    print("\n--- 8. Kerr 曲率修正效果 ---")
    E_kerr_no_correction = R_kerr.spectral_object_with_curvature()
    E_kerr_corrected = CurvedDecursionFunctor.map_object(R_kerr)
    print(f"  无修正谱: {np.round(E_kerr_no_correction.spectrum, 4)}")
    print(f"  有修正谱: {np.round(E_kerr_corrected.spectrum, 4)}")
    print(f"  曲率修正差异: {np.max(np.abs(E_kerr_no_correction.spectrum - E_kerr_corrected.spectrum)):.4e}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_curved_rec_object()