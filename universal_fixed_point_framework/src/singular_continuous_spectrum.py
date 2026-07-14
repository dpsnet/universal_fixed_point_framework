"""
singular_continuous_spectrum.py

奇异连续谱的系统刻画：
1. 经典例子：Cantor 谱、Sierpinski 谱（混沌游戏采样）
2. 谱维数：盒计数、相关维数、信息维数
3. 谱型分类：纯点 / 绝对连续 / 奇异连续
4. 物理意义：凝聚态、量子混沌、量子引力
5. 框架对应：谱对应保持谱型
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple
from enum import Enum


class SpectrumType(Enum):
    PURE_POINT = "pure_point"
    ABSOLUTELY_CONTINUOUS = "absolutely_continuous"
    SINGULAR_CONTINUOUS = "singular_continuous"
    MIXED = "mixed"


# ===========================================================================
# 分形谱构造（混沌游戏采样 — 正确反映自相似测度）
# ===========================================================================

def cantor_measure_sample(n_points: int, n_levels: int = 8) -> np.ndarray:
    """
    用混沌游戏采样 Cantor 测度的支撑点。

    经典 Cantor 三分集：两个映射 S_0(x) = x/3, S_1(x) = (x+2)/3
    等概率选择，随机游走生成的点集服从自相似测度。
    """
    # 用多级细分 + 随机选择生成点
    points = []
    for _ in range(n_points):
        x = 0.5  # 起点
        # 每级随机选左段或右段
        for level in range(n_levels):
            segment_len = 1.0 / (3 ** level)
            if np.random.rand() < 0.5:
                # 左段：[0, 1/3] 对应上一级 [0, 1]
                x = x / 3.0
            else:
                # 右段：[2/3, 1]
                x = (x + 2.0) / 3.0
        points.append(x)
    return np.sort(np.array(points))


def sierpinski_triangle_sample(n_points: int, n_iter: int = 8) -> np.ndarray:
    """
    混沌游戏采样 Sierpinski 三角形，然后投影到一维谱。

    三个顶点，每次随机选一个顶点向其移动 1/2 距离。
    """
    vertices = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.5, np.sqrt(3.0) / 2.0]
    ])

    points = np.zeros((n_points, 2))
    point = np.array([0.5, 0.3])  # 起点

    # burn-in
    for _ in range(20):
        v = vertices[np.random.randint(3)]
        point = 0.5 * (point + v)

    # 采样
    for i in range(n_points):
        v = vertices[np.random.randint(3)]
        point = 0.5 * (point + v)
        points[i] = point

    # 投影到一维：使用 x 坐标（自然排序）
    # 为了更"谱"的感觉，用 x 坐标排序
    spectrum = points[:, 0]
    return np.sort(spectrum)


def devil_staircase_sample(n_points: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    生成 Cantor 函数（魔鬼阶梯）的采样点。

    Cantor 函数 F(x) = 自相似测度的累积分布函数。
    通过逆变换采样：如果 U ~ Uniform[0,1]，则 F^{-1}(U) ~ Cantor 测度。
    """
    # 用二进制展开 → 三进制展开的转换
    # Cantor 函数的逆：将 U 的二进制展开中的 1 映射为三进制的 2
    x_values = []
    F_values = []

    for _ in range(n_points):
        u = np.random.rand()
        # 将 u 展开为二进制，然后映射到三进制（1→2）
        # 这给出 Cantor 函数的反函数
        x = 0.0
        f_val = 0.0
        remaining = u
        for i in range(1, 20):
            bit = int(remaining * 2)
            remaining = remaining * 2 - bit
            if bit == 1:
                x += 2.0 / (3 ** i)
                f_val += 1.0 / (2 ** i)
        x_values.append(x)
        F_values.append(f_val)

    idx = np.argsort(x_values)
    return np.array(x_values)[idx], np.array(F_values)[idx]


# ===========================================================================
# 谱维数计算
# ===========================================================================

@dataclass
class SpectrumDimensions:
    """谱测度的各种维数"""
    hausdorff_lower_bound: float = 0.0
    box_counting: float = 0.0
    correlation_D2: float = 0.0
    information_D1: float = 0.0

    def summary(self) -> str:
        return (f"  盒计数维数 dim_B:     {self.box_counting:.4f}\n"
                f"  信息维数 D_1:         {self.information_D1:.4f}\n"
                f"  相关维数 D_2:         {self.correlation_D2:.4f}\n"
                f"  Hausdorff 下界:       {self.hausdorff_lower_bound:.4f}\n"
                f"  （D_2 ≤ D_1 ≤ dim_H ≤ dim_B, 这里顺序因数值误差可能略有不同）")


def _box_counting_1d(spectrum: np.ndarray, eps: float) -> int:
    """一维盒计数"""
    spectrum = np.sort(spectrum)
    n_boxes = 0
    i = 0
    n = len(spectrum)
    while i < n:
        n_boxes += 1
        current = spectrum[i]
        while i < n and spectrum[i] - current <= eps:
            i += 1
    return n_boxes


def compute_box_counting_dimension(spectrum: np.ndarray,
                                   n_scales: int = 15) -> float:
    """盒计数维数：N(ε) ∝ ε^{-d_B}"""
    spectrum = np.sort(spectrum)
    lo = (spectrum[-1] - spectrum[0]) / len(spectrum) * 2
    hi = (spectrum[-1] - spectrum[0]) * 0.5
    eps_list = np.logspace(np.log10(lo), np.log10(hi), n_scales)

    counts = []
    for eps in eps_list:
        counts.append(_box_counting_1d(spectrum, eps))

    # 线性回归
    valid = np.array(counts) > 1
    log_eps = np.log(eps_list[valid])
    log_N = np.log(np.array(counts)[valid])

    if len(log_eps) < 3:
        return float('nan')

    d, _ = np.polyfit(-log_eps, log_N, 1)
    return d


def compute_correlation_dimension(spectrum: np.ndarray,
                                  n_scales: int = 15) -> float:
    """
    相关维数 D_2：C_2(r) ∝ r^{D_2}

    使用固定数量的采样点加速计算。
    """
    n_total = len(spectrum)
    n_sample = min(n_total, 500)

    if n_total > n_sample:
        idx = np.sort(np.random.choice(n_total, n_sample, replace=False))
        spec = spectrum[idx]
    else:
        spec = spectrum

    # 计算两两距离
    dists = []
    for i in range(n_sample):
        for j in range(i + 1, n_sample):
            dists.append(abs(spec[i] - spec[j]))
    dists = np.sort(np.array(dists))

    if len(dists) < 10:
        return float('nan')

    # 去掉最小和最大的 5%
    n_dists = len(dists)
    lo_idx = int(n_dists * 0.05)
    hi_idx = int(n_dists * 0.5)  # 只用小 r 区域
    r_lo = dists[lo_idx]
    r_hi = dists[hi_idx]

    r_list = np.logspace(np.log10(r_lo), np.log10(r_hi), n_scales)
    C2 = []
    total_pairs = n_sample * (n_sample - 1) / 2

    for r in r_list:
        count = np.searchsorted(dists, r)
        C2.append(max(count, 1) / total_pairs)

    log_r = np.log(r_list)
    log_C2 = np.log(np.array(C2))

    valid = np.isfinite(log_C2)
    if np.sum(valid) < 3:
        return float('nan')

    d, _ = np.polyfit(log_r[valid], log_C2[valid], 1)
    return d


def compute_information_dimension(spectrum: np.ndarray,
                                  n_scales: int = 15) -> float:
    """
    信息维数 D_1：I(ε) = -Σ p_i log p_i ∝ D_1 log(1/ε)
    """
    spectrum = np.sort(spectrum)
    lo = (spectrum[-1] - spectrum[0]) / len(spectrum) * 2
    hi = (spectrum[-1] - spectrum[0]) * 0.5
    eps_list = np.logspace(np.log10(lo), np.log10(hi), n_scales)

    entropies = []
    n = len(spectrum)

    for eps in eps_list:
        # 计算每个盒子的点数
        box_counts = []
        i = 0
        while i < n:
            current = spectrum[i]
            count = 0
            while i < n and spectrum[i] - current <= eps:
                count += 1
                i += 1
            if count > 0:
                box_counts.append(count)

        if len(box_counts) < 2:
            entropies.append(float('nan'))
            continue

        p_i = np.array(box_counts, dtype=float) / n
        p_i = p_i[p_i > 0]
        entropy = -np.sum(p_i * np.log(p_i))
        entropies.append(entropy)

    # 回归：I ~ D_1 * log(1/ε)
    valid = np.isfinite(entropies)
    if np.sum(valid) < 3:
        return float('nan')

    log_eps_inv = -np.log(eps_list[valid])
    I = np.array(entropies)[valid]

    d, _ = np.polyfit(log_eps_inv, I, 1)
    return d


def compute_all_dimensions(spectrum: np.ndarray) -> SpectrumDimensions:
    """计算谱的所有维数"""
    dims = SpectrumDimensions()
    dims.box_counting = compute_box_counting_dimension(spectrum)
    dims.correlation_D2 = compute_correlation_dimension(spectrum)
    dims.information_D1 = compute_information_dimension(spectrum)

    # Hausdorff 维数 ≥ 相关维数
    # 这里用相关维数作为下界估计
    dims.hausdorff_lower_bound = dims.correlation_D2

    return dims


# ===========================================================================
# 谱型分类
# ===========================================================================

@dataclass
class LebesgueDecomposition:
    """谱测度的 Lebesgue 分解估计"""
    pure_point_weight: float = 0.0
    absolutely_continuous_weight: float = 0.0
    singular_continuous_weight: float = 0.0
    dominant_type: SpectrumType = SpectrumType.MIXED

    def summary(self) -> str:
        return (f"  纯点谱估计权重:      {self.pure_point_weight*100:.1f}%\n"
                f"  绝对连续谱估计权重:  {self.absolutely_continuous_weight*100:.1f}%\n"
                f"  奇异连续谱估计权重:  {self.singular_continuous_weight*100:.1f}%\n"
                f"  主导谱型:            {self.dominant_type.value}")


def classify_spectrum(spectrum: np.ndarray) -> LebesgueDecomposition:
    """
    基于谱维数和间距统计的谱型分类。

    判断准则：
    - 纯点谱：有限个离散点，盒维数 = 0（或接近 0）
    - 绝对连续谱：盒维数 = 1（对一维支撑），间距分布均匀
    - 奇异连续谱：盒维数在 (0, 1) 之间，分形结构
    """
    n = len(spectrum)
    dims = compute_all_dimensions(spectrum)
    d_box = dims.box_counting

    # 计算间距统计
    gaps = np.diff(np.sort(spectrum))
    mean_gap = np.mean(gaps) if len(gaps) > 0 else 1.0

    # 1. 纯点判据：点数少，或间距有数量级差异
    if n <= 20:
        pp_weight = 1.0
        ac_weight = 0.0
        sc_weight = 0.0
    else:
        # 纯点程度：大间隙的比例（与平均间隙比）
        large_gap_ratio = np.sum(gaps > 5 * mean_gap) / len(gaps)
        pp_weight = min(1.0, large_gap_ratio * 5.0)

        # 绝对连续：盒维数接近整数（支撑维数）
        ac_weight = max(0.0, 1.0 - abs(d_box - 1.0) * 3.0)

        # 奇异连续：盒维数在 (0, 1) 之间，且不是纯点
        if 0.1 < d_box < 0.95:
            sc_weight = 1.0 - pp_weight
        else:
            sc_weight = max(0.0, 1.0 - pp_weight - ac_weight)

    # 归一化
    total = pp_weight + ac_weight + sc_weight
    if total > 0:
        pp_weight /= total
        ac_weight /= total
        sc_weight /= total

    # 确定主导类型
    weights = {
        SpectrumType.PURE_POINT: pp_weight,
        SpectrumType.ABSOLUTELY_CONTINUOUS: ac_weight,
        SpectrumType.SINGULAR_CONTINUOUS: sc_weight,
    }
    dominant = max(weights, key=weights.get)

    return LebesgueDecomposition(
        pure_point_weight=pp_weight,
        absolutely_continuous_weight=ac_weight,
        singular_continuous_weight=sc_weight,
        dominant_type=dominant,
    )


# ===========================================================================
# 物理意义
# ===========================================================================

PHYSICAL_APPLICATIONS = """
奇异连续谱的物理意义与应用场景：

1. 凝聚态物理：
   - 准晶（quasicrystals）：长程有序但无平移对称，电子能谱为奇异连续
   - Harper 方程 / Hofstadter 蝴蝶：无理磁通下的分形谱
   - 一维无序系统：Anderson 迁移率边处的谱

2. 量子混沌：
   - 伪可积系统：介于可积与混沌之间，谱为奇异连续
   - 分形量子阱：分形几何中的量子态

3. 动力系统：
   - 临界准周期系统：金属-绝缘体转变临界点
   - 奇怪吸引子上的 Koopman 算子谱

4. 量子引力候选：
   - 因果集：离散时空的谱维随尺度变化
   - 自旋泡沫 / 圈量子引力：面积/体积算子谱

5. 本框架内对应：
   - 非分离 IFS → 吸引子上的分形谱 → 奇异连续分量
   - 谱对应 λ = e^{-μ}：η_R 是保测度同构，保持谱型
   - 分形 RKHS：核的 Mercer 展开支撑在分形集上
"""


# ===========================================================================
# 谱对应保持谱型验证
# ===========================================================================

def verify_spectral_correspondence_preserves_type(
    mu_spectrum: np.ndarray) -> Dict:
    """验证谱对应 λ = e^{-μ} 保持谱型"""
    lambda_spectrum = np.exp(-mu_spectrum)

    dims_mu = compute_all_dimensions(mu_spectrum)
    dims_lambda = compute_all_dimensions(lambda_spectrum)

    type_mu = classify_spectrum(mu_spectrum)
    type_lambda = classify_spectrum(lambda_spectrum)

    return {
        "mu_dimensions": dims_mu,
        "lambda_dimensions": dims_lambda,
        "mu_type": type_mu,
        "lambda_type": type_lambda,
        "type_preserved": type_mu.dominant_type == type_lambda.dominant_type,
    }


# ===========================================================================
# 数值验证
# ===========================================================================

def _demo_cantor_spectrum():
    """Cantor 谱的维数计算与分类"""
    print("=" * 70)
    print("1. Cantor 三分集谱（混沌游戏采样）")
    print("=" * 70)

    np.random.seed(42)
    cantor = cantor_measure_sample(2000, n_levels=10)

    print(f"\n  采样点数: {len(cantor)}")
    print(f"  范围: [{cantor[0]:.6f}, {cantor[-1]:.6f}]")

    dims = compute_all_dimensions(cantor)
    print("\n  谱维数:")
    print(dims.summary())
    print(f"\n  理论值 dim_H = log 2 / log 3 = {np.log(2)/np.log(3):.4f}")

    spec_type = classify_spectrum(cantor)
    print("\n  谱型分类:")
    print(spec_type.summary())

    # Cantor 函数
    print("\n  Cantor 函数（魔鬼阶梯）:")
    x_cantor, F_cantor = devil_staircase_sample(500)
    print(f"    F(0) = {F_cantor[0]:.4f}, F(1) = {F_cantor[-1]:.4f}")
    print(f"    单调递增: {np.all(np.diff(F_cantor) >= -1e-12)}")


def _demo_sierpinski_spectrum():
    """Sierpinski 三角形谱的维数计算"""
    print("\n" + "=" * 70)
    print("2. Sierpinski 三角形谱（混沌游戏采样，x 轴投影）")
    print("=" * 70)

    np.random.seed(42)
    sierp = sierpinski_triangle_sample(2000)

    print(f"\n  采样点数: {len(sierp)}")
    print(f"  范围: [{sierp[0]:.6f}, {sierp[-1]:.6f}]")

    dims = compute_all_dimensions(sierp)
    print("\n  谱维数:")
    print(dims.summary())
    # 注意：投影到 x 轴的维数不是 Sierpinski 三角形本身的维数
    # 投影维数 ≤ 原维数，通常 x 轴投影 ~ 1（因为 x 范围覆盖 [0,1]）
    print(f"\n  （注：x 轴投影的维数不是 Sierpinski 三角形本身的维数）")
    print(f"    Sierpinski 三角形理论 dim_H = log 3 / log 2 = {np.log(3)/np.log(2):.4f}")
    print(f"    x 轴投影因支撑充满 [0,1]，盒维数接近 1")

    spec_type = classify_spectrum(sierp)
    print("\n  谱型分类:")
    print(spec_type.summary())


def _demo_lebesgue_comparison():
    """三种谱型的对比"""
    print("\n" + "=" * 70)
    print("3. 三种谱型对比")
    print("=" * 70)

    np.random.seed(42)

    # 纯点：少量离散能级
    pure_point = np.array([0.1, 0.25, 0.4, 0.55, 0.7, 0.85, 0.95])

    # 绝对连续：均匀随机
    abs_cont = np.sort(np.random.rand(500))

    # 奇异连续：Cantor 测度
    sing_cont = cantor_measure_sample(500, n_levels=10)

    print("\n  (a) 纯点谱（7 个离散能级）:")
    print(classify_spectrum(pure_point).summary())

    print("\n  (b) 绝对连续谱（均匀随机 500 点）:")
    print(classify_spectrum(abs_cont).summary())

    print("\n  (c) 奇异连续谱（Cantor 测度 500 点）:")
    print(classify_spectrum(sing_cont).summary())


def _demo_spectral_correspondence():
    """谱对应保持谱型验证"""
    print("\n" + "=" * 70)
    print("4. 谱对应 λ = e^{-μ} 保持谱型")
    print("=" * 70)

    np.random.seed(42)
    # μ 侧：Cantor 测度映射到正实轴
    cantor_01 = cantor_measure_sample(1000, n_levels=10)
    mu_side = -np.log(cantor_01 * 0.5 + 0.25)  # 映射到 μ > 0

    result = verify_spectral_correspondence_preserves_type(mu_side)

    print("\n  μ-侧（Cantor 测度，μ > 0）:")
    print(f"    盒维数: {result['mu_dimensions'].box_counting:.4f}")
    print(f"    谱型:   {result['mu_type'].dominant_type.value}")

    print("\n  λ-侧（λ = e^{-μ}）:")
    print(f"    盒维数: {result['lambda_dimensions'].box_counting:.4f}")
    print(f"    谱型:   {result['lambda_type'].dominant_type.value}")

    print(f"\n  谱型保持: {result['type_preserved']}")
    print("  （η_R 是测度空间同构，保持谱型不变）")


if __name__ == "__main__":
    _demo_cantor_spectrum()
    _demo_sierpinski_spectrum()
    _demo_lebesgue_comparison()
    _demo_spectral_correspondence()

    print("\n" + "=" * 70)
    print("奇异连续谱刻画完成：")
    print("  - 构造：Cantor / Sierpinski 分形谱（混沌游戏采样）")
    print("  - 维数：盒计数、信息维数 D_1、相关维数 D_2")
    print("  - 分类：纯点 / 绝对连续 / 奇异连续 三分类")
    print("  - 物理：准晶、量子混沌、因果集、自旋泡沫")
    print("  - 框架：谱对应保持谱型（η_R 保测度同构）")
    print("=" * 70)
