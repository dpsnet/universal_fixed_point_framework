"""
example_attractor_distance.py

局部吸引子捕获指数（LACI）的测试用例。

对比两个系统：
1. 强压缩系统：谱间隙大，吸引子盆地唯一，LACI 低（不易过拟合）。
2. 弱压缩/双吸引子系统：谱间隙小，存在多个吸引子，LACI 高（易过拟合）。
"""

from typing import Tuple
import numpy as np
from fixed_point_solver import FixedPointSolver
from attractor_distance import compute_laci, diagnose_rec_object, spectral_gap


def build_strongly_contracting_system() -> Tuple[np.ndarray, np.ndarray]:
    """
    构造强压缩系统：列随机转移矩阵，次主导特征值远离 1。
    该系统有唯一吸引子，盆地明确。
    """
    K = np.array([
        [0.7, 0.2],
        [0.3, 0.8],
    ])
    # 已经是列随机
    mu = FixedPointSolver.solve_hutchinson_measure(K).fixed_point
    return K, mu


def build_multi_attractor_system() -> Tuple[np.ndarray, np.ndarray]:
    """
    构造双吸引子系统：2x2 转移矩阵，两个状态几乎不互相转移。
    每个状态自身是一个吸引子，系统存在多个局部吸引子。
    """
    K = np.array([
        [0.99, 0.01],
        [0.01, 0.99],
    ])
    K = K / K.sum(axis=0, keepdims=True)
    # 从一个初始点出发得到某个局部吸引子
    mu = FixedPointSolver.solve_hutchinson_measure(
        K, mu0=np.array([0.6, 0.4])
    ).fixed_point
    return K, mu


def test_spectral_gap():
    """验证强压缩系统的谱间隙大于弱压缩系统。"""
    print("\n[测试 1] 谱间隙对比")
    K_strong, _ = build_strongly_contracting_system()
    K_weak, _ = build_multi_attractor_system()

    gamma_strong = spectral_gap(K_strong)
    gamma_weak = spectral_gap(K_weak)

    print(f"  强压缩系统谱间隙: {gamma_strong:.6f}")
    print(f"  弱压缩系统谱间隙: {gamma_weak:.6f}")
    assert gamma_strong > gamma_weak, "强压缩系统应有更大谱间隙"
    print("  通过")


def test_laci_contrast():
    """验证强压缩系统 LACI 低，弱压缩/多吸引子系统 LACI 高。"""
    print("\n[测试 2] LACI 对比")
    K_strong, mu_strong = build_strongly_contracting_system()
    K_weak, mu_weak = build_multi_attractor_system()

    metrics_strong = compute_laci(K_strong, mu_strong)
    metrics_weak = compute_laci(K_weak, mu_weak)

    print("  强压缩系统:")
    print(f"    残差 rho      = {metrics_strong.residual:.2e}")
    print(f"    分散度 Delta  = {metrics_strong.dispersion:.2e}")
    print(f"    谱间隙 gamma  = {metrics_strong.spectral_gap:.6f}")
    print(f"    LACI          = {metrics_strong.laci:.4f}")

    print("  弱压缩/多吸引子系统:")
    print(f"    残差 rho      = {metrics_weak.residual:.2e}")
    print(f"    分散度 Delta  = {metrics_weak.dispersion:.2e}")
    print(f"    谱间隙 gamma  = {metrics_weak.spectral_gap:.6f}")
    print(f"    LACI          = {metrics_weak.laci:.4f}")

    assert metrics_strong.laci < metrics_weak.laci, "强压缩系统 LACI 应更低"
    print("  通过")


def test_sm_instance_diagnosis():
    """对标准模型实例的 IFS 转移矩阵进行过拟合诊断。"""
    print("\n[测试 3] 标准模型实例诊断")
    # 从 sm_instance 导入默认参数
    import sys
    from pathlib import Path
    sm_dir = Path(__file__).resolve().parents[1] / "applications" / "standard_model"
    if str(sm_dir) not in sys.path:
        sys.path.insert(0, str(sm_dir))
    from sm_instance import SMInstance

    sm = SMInstance()
    rec = sm.to_rec_object()
    K = rec.koopman_matrix()
    mu = FixedPointSolver.solve_hutchinson_measure(K).fixed_point

    diagnosis = diagnose_rec_object(K, mu)
    print(f"  SM 实例 IFS 诊断:")
    for key, value in diagnosis.items():
        print(f"    {key:<25}: {value}")

    assert diagnosis["residual"] < 1e-6, "Hutchinson 残差应很小"
    print("  通过")


def main():
    print("=" * 60)
    print("局部吸引子捕获指数（LACI）测试")
    print("=" * 60)

    test_spectral_gap()
    test_laci_contrast()
    test_sm_instance_diagnosis()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
