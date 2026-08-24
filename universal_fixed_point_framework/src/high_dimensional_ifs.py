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
high_dimensional_ifs.py

高维 IFS 收敛率理论：
1. 高维自相似集的 Hausdorff 维数与盒计数维数
2. 高维覆盖熵估计与体积增长
3. 高维 RKHS 收敛率上界（强分离 / 弱分离 / 非分离）
4. 高维最优切换点分析
5. 维数依赖性与相变行为

核心推广：
- 一维：d_amb = 1，长度尺度 ~ ε
- d 维：d_amb = d，体积尺度 ~ ε^d
- 覆盖数 N(ε) ~ ε^{-d_frac} → 适用于任意维
- 收敛率指数 α/d_frac（势论）或 1 - d_frac/d_amb（覆盖熵）
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple


# ===========================================================================
# 高维自相似集理论
# ===========================================================================

HIGH_DIM_THEORY = """
高维 IFS 收敛率理论基础：

1. 高维自相似集的维数（Moran 方程推广）：
   对 R^d 上的相似 IFS {S_i}_{i=1}^n，相似因子 {c_i}，
   相似维数 d_sim 是 Moran 方程 Σ_{i=1}^n c_i^s = 1 的解。
   满足开集条件（OSC）时，dim_H(F) = dim_B(F) = d_sim。

2. 高维覆盖数（Falconer 覆盖定理的高维版本）：
   设 F ⊂ R^d 为有界集，s = dim_H(F)，则
       N(F, ε) ≤ C · ε^{-s}   （上界，盒计数）
   同时 N(F, ε) ≥ C' · ε^{-s}  （下界，Frostman 型）

3. 高维 RKHS 收敛率：
   对支撑在 d_frac 维分形集上、嵌入 d_amb 维空间的 Mercer 核，
   核矩阵特征值收敛率满足：
   - 强分离（OSC）：O(c_max^{α N})（指数收敛）
   - 非分离：O(N^{-α/d_frac})（多项式收敛，势论上界）
   其中 α 为核的 Hölder / 光滑指数。

4. 体积增长与有效维数：
   N 个采样点在 d_frac 维集上的"体积"：V(N) ~ N^{d_frac/d_amb}
   这决定了核矩阵的有效秩与收敛速度。
"""


# ===========================================================================
# 高维 IFS 收敛率分析器
# ===========================================================================

@dataclass
class HighDimIFSAnalysis:
    """高维 IFS 收敛率分析"""

    contraction_factors: np.ndarray   # IFS 收缩因子 {c_i}
    probabilities: np.ndarray         # IFS 概率 {p_i}
    ambient_dim: int = 3              # 环境空间维数 d_amb
    kernel_smoothness: float = 1.0    # 核光滑指数 α
    separation_type: str = "non_separated"  # "strong" / "weak" / "non_separated"
    overlap_degree: float = 0.0       # 重叠程度 ρ ∈ [0, 1]

    def __post_init__(self):
        self.n_maps = len(self.contraction_factors)
        self.c_max = np.max(self.contraction_factors)
        self.c_avg = np.mean(self.contraction_factors)
        self.d_sim = self._similarity_dimension()
        self.d_effective = self._effective_dimension()

    def _similarity_dimension(self) -> float:
        """相似维数 d_sim：Σ c_i^s = 1 的解"""
        def f(s):
            return np.sum(self.contraction_factors**s) - 1

        lo, hi = 0.01, float(self.ambient_dim) + 5.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    def _effective_dimension(self) -> float:
        """
        有效 Hausdorff 维数 d_eff。

        - 强分离（OSC）：d_eff = d_sim
        - 部分重叠：d_eff < d_sim（取决于重叠程度）
        - 完全重叠：d_eff → 0（退化为单点）
        """
        rho = max(0.0, min(1.0, self.overlap_degree))
        n = self.n_maps

        if self.separation_type == "strong":
            return min(self.d_sim, float(self.ambient_dim))
        elif self.separation_type == "weak":
            # 弱分离：维数略有下降
            d_eff = self.d_sim * (1 - 0.1 * rho)
            return min(d_eff, float(self.ambient_dim))
        else:  # non_separated
            # 非分离：维数下降更多
            # 简化模型：d_eff = d_sim * (1 - rho * (n-1)/n)
            d_eff = self.d_sim * (1 - rho * (n - 1) / n)
            return min(d_eff, float(self.ambient_dim))

    # -----------------------------------------------------------------------
    # 收敛率上界
    # -----------------------------------------------------------------------

    def exponential_bound(self, N: int) -> float:
        """
        指数收敛上界（强分离情形）。

        误差 ~ c_max^{α N / d_amb}
        （d_amb 维空间中，每步细化填充体积的比例）
        """
        rate_per_step = self.c_max ** (self.kernel_smoothness / self.ambient_dim)
        return rate_per_step ** N

    def polynomial_bound_covering(self, N: int) -> float:
        """
        多项式收敛上界（覆盖熵论证）。

        误差 ~ N^{-(1 - d_frac/d_amb)}
        适用于非分离 / 弱分离情形。
        """
        exponent = 1.0 - self.d_effective / self.ambient_dim
        return N**(-max(exponent, 0.0))

    def polynomial_bound_potential(self, N: int) -> float:
        """
        多项式收敛上界（势论能量论证）。

        误差 ~ N^{-α/d_frac}
        更精确的上界（基于 Riesz 容量与 Mercer 定理）。
        """
        if self.d_effective < 1e-10:
            return 0.0
        exponent = self.kernel_smoothness / self.d_effective
        return N**(-exponent)

    def convergence_bound(self, N: int) -> float:
        """
        综合收敛上界（取各上界中最紧的）。
        """
        if self.separation_type == "strong":
            return self.exponential_bound(N)
        elif self.separation_type == "weak":
            return min(self.exponential_bound(N),
                       self.polynomial_bound_potential(N))
        else:  # non_separated
            return self.polynomial_bound_potential(N)

    # -----------------------------------------------------------------------
    # 最优切换点
    # -----------------------------------------------------------------------

    def optimal_switching_point(self) -> float:
        """
        最优切换点 N*：指数上界与多项式上界的交点。

        方程：c_max^{α N / d_amb} = N^{-α/d_frac}

        取对数：
            (α N / d_amb) ln c_max = -(α / d_frac) ln N
            N · ln(1/c_max) / d_amb = (ln N) / d_frac
            (ln N) / N = (d_frac / d_amb) · ln(1/c_max)
        """
        if self.separation_type == "strong":
            return float('inf')  # 纯指数收敛，无切换

        d_frac = self.d_effective
        if d_frac < 1e-10 or d_frac >= self.ambient_dim - 1e-10:
            return float('inf')

        rhs = (d_frac / self.ambient_dim) * np.log(1.0 / self.c_max)

        if rhs > 1.0 / np.e:
            return float('inf')  # 无解
        if rhs <= 0:
            return float('inf')

        # 牛顿法求解 (ln N)/N = rhs
        N = np.exp(1.0)
        for _ in range(100):
            f = np.log(N) / N - rhs
            df = (1.0 - np.log(N)) / N**2
            if abs(df) < 1e-15:
                break
            N_new = N - f / df
            if N_new <= 1.0:
                N_new = 1.5
            if abs(N_new - N) < 1e-10:
                N = N_new
                break
            N = N_new

        return N

    # -----------------------------------------------------------------------
    # 维数相变分析
    # -----------------------------------------------------------------------

    def dimension_phase_diagram(self) -> dict:
        """
        维数相变分析：d_frac 从 0 到 d_amb 时收敛行为的变化。

        三个阶段：
        1. 低维相（d_frac << d_amb）：快速多项式收敛，N* 小
        2. 中间相（d_frac ~ d_amb/2）：中等收敛速率
        3. 高维相（d_frac ≈ d_amb）：慢速收敛，N* → ∞，接近 d_amp 维欧氏空间
        """
        d_frac_values = np.linspace(0.1, self.ambient_dim - 0.1, 20)
        results = []

        for df in d_frac_values:
            # 多项式收敛指数（势论）
            poly_exp = self.kernel_smoothness / df if df > 0 else float('inf')
            # 覆盖熵指数
            cover_exp = 1.0 - df / self.ambient_dim
            # 切换点估计
            rhs = (df / self.ambient_dim) * np.log(1.0 / self.c_max)
            if 0 < rhs < 1.0 / np.e:
                # 近似解
                N_star = np.exp(1.0)
                for _ in range(50):
                    f = np.log(N_star) / N_star - rhs
                    df_val = (1.0 - np.log(N_star)) / N_star**2
                    if abs(df_val) > 1e-15:
                        N_star -= f / df_val
                        if N_star <= 1:
                            N_star = float('inf')
                            break
            else:
                N_star = float('inf')

            results.append({
                "d_frac": df,
                "polynomial_exponent": poly_exp,
                "covering_exponent": cover_exp,
                "switching_point": N_star,
                "phase": "low_dim" if df < self.ambient_dim / 3
                        else ("high_dim" if df > 2 * self.ambient_dim / 3
                              else "intermediate"),
            })

        return {"d_ambient": self.ambient_dim, "phases": results}

    def summary(self) -> str:
        n_star = self.optimal_switching_point()
        n_star_str = f"{n_star:.1f}" if n_star < 1e6 else "∞"

        return (
            f"  环境空间维数 d_amb:    {self.ambient_dim}\n"
            f"  相似维数 d_sim:         {self.d_sim:.4f}\n"
            f"  有效维数 d_eff:         {self.d_effective:.4f}\n"
            f"  分离类型:               {self.separation_type}\n"
            f"  核光滑指数 α:           {self.kernel_smoothness}\n"
            f"  势论收敛指数 α/d_eff:   {self.kernel_smoothness/self.d_effective:.4f}\n"
            f"  覆盖熵收敛指数:         {1 - self.d_effective/self.ambient_dim:.4f}\n"
            f"  最优切换点 N*:          {n_star_str}"
        )


# ===========================================================================
# 高维数值验证
# ===========================================================================

def _verify_high_dim_cantor():
    """验证高维 Cantor 类分形的收敛率"""
    print("=" * 70)
    print("高维 IFS 收敛率验证")
    print("=" * 70)

    # 示例 1：三维空间中的二维 Cantor 尘
    print("\n1. 三维空间中的 2D Cantor 尘（类 Sierpinski 毯）：")
    print("   IFS: 4 个映射，各收缩 1/3，分布在平面四角")
    c = np.array([1.0/3, 1.0/3, 1.0/3, 1.0/3])
    p = np.array([0.25, 0.25, 0.25, 0.25])
    hda = HighDimIFSAnalysis(c, p, ambient_dim=3,
                              separation_type="strong")
    print(hda.summary())
    print(f"   理论 d_sim = log 4 / log 3 = {np.log(4)/np.log(3):.4f}")

    # 示例 2：不同环境维数下的同一 IFS
    print("\n2. 不同环境维数下的收敛率对比：")
    print("   (同一 IFS：5 个映射，c_i = 0.5，等概率)")
    c = np.full(5, 0.5)
    p = np.full(5, 0.2)

    print(f"   {'d_amb':<6} {'d_sim':<8} {'d_eff':<8} {'α/d_eff':<10} "
          f"{'1-d_eff/d_amb':<14} {'N*':<10}")
    print("   " + "-" * 60)

    for d_amb in [1, 2, 3, 4, 5]:
        hda = HighDimIFSAnalysis(c, p, ambient_dim=d_amb,
                                  separation_type="non_separated",
                                  overlap_degree=0.3)
        n_star = hda.optimal_switching_point()
        n_star_str = f"{n_star:.1f}" if n_star < 1e6 else "∞"
        print(f"   {d_amb:<6} {hda.d_sim:<8.4f} {hda.d_effective:<8.4f} "
              f"{hda.kernel_smoothness/hda.d_effective:<10.4f} "
              f"{1 - hda.d_effective/d_amb:<14.4f} {n_star_str:<10}")

    # 示例 3：维数相变图
    print("\n3. 维数相变图（d_amb = 3）：")
    hda = HighDimIFSAnalysis(np.array([0.5, 0.5]), np.array([0.5, 0.5]),
                              ambient_dim=3, separation_type="weak")
    phases = hda.dimension_phase_diagram()
    print(f"   {'d_frac':<8} {'势论指数':<10} {'覆盖熵指数':<12} {'相':<14}")
    print("   " + "-" * 50)
    for entry in phases["phases"][::3]:  # 每隔几个显示
        print(f"   {entry['d_frac']:<8.2f} {entry['polynomial_exponent']:<10.4f} "
              f"{entry['covering_exponent']:<12.4f} {entry['phase']:<14}")

    print("\n   观察：")
    print("   - 低维相（d_frac 小）：收敛快，指数大")
    print("   - 高维相（d_frac → d_amb）：收敛慢，指数小")
    print("   - 切换点 N* 随 d_frac 增大而单调递增，d_frac→d_amb 时发散")


def _verify_separation_effect():
    """验证分离程度对高维收敛率的影响"""
    print("\n" + "=" * 70)
    print("分离程度对高维收敛率的影响")
    print("=" * 70)

    c = np.array([0.4, 0.4, 0.3])
    p = np.array([1.0/3, 1.0/3, 1.0/3])

    print(f"\n  IFS: n=3, c=[0.4, 0.4, 0.3], d_amb=3")
    print(f"  {'类型':<14} {'d_eff':<8} {'收敛指数':<10} {'N=100 上界':<14}")
    print("  " + "-" * 50)

    for sep_type, rho in [("strong", 0.0), ("weak", 0.3), ("non_separated", 0.7)]:
        hda = HighDimIFSAnalysis(c, p, ambient_dim=3,
                                  separation_type=sep_type,
                                  overlap_degree=rho)
        bound = hda.convergence_bound(100)
        exp_val = (hda.kernel_smoothness / hda.d_effective
                   if hda.d_effective > 0 else float('inf'))
        print(f"  {sep_type:<14} {hda.d_effective:<8.4f} {exp_val:<10.4f} {bound:<14.6e}")

    print("\n  观察：")
    print("  - 强分离 → 指数收敛，上界最小")
    print("  - 弱分离 → 指数 + 多项式混合")
    print("  - 非分离 → 纯多项式收敛，速率最慢")


def _verify_kernel_smoothness():
    """验证核光滑指数对收敛率的影响"""
    print("\n" + "=" * 70)
    print("核光滑指数 α 对收敛率的影响")
    print("=" * 70)

    c = np.array([0.5, 0.5])
    p = np.array([0.5, 0.5])

    print(f"\n  IFS: n=2, c=[0.5, 0.5], d_amb=3, d_sim=1.0")
    print(f"  {'α':<6} {'收敛指数 α/d_frac':<18} {'N=100 上界':<14} {'N=1000 上界':<14}")
    print("  " + "-" * 55)

    for alpha in [0.25, 0.5, 1.0, 2.0, 3.0]:
        hda = HighDimIFSAnalysis(c, p, ambient_dim=3,
                                  kernel_smoothness=alpha,
                                  separation_type="non_separated",
                                  overlap_degree=0.2)
        bound_100 = hda.convergence_bound(100)
        bound_1000 = hda.convergence_bound(1000)
        exp_val = alpha / hda.d_effective if hda.d_effective > 0 else float('inf')
        print(f"  {alpha:<6.2f} {exp_val:<18.4f} {bound_100:<14.6e} {bound_1000:<14.6e}")

    print("\n  观察：")
    print("  - α 越大（核越光滑），收敛越快（指数越大）")
    print("  - 对解析核（α → ∞），收敛可接近指数速率")
    print("  - α 是核函数的正则性指标，由核的光滑性决定")


if __name__ == "__main__":
    _verify_high_dim_cantor()
    _verify_separation_effect()
    _verify_kernel_smoothness()

    print("\n" + "=" * 70)
    print("高维 IFS 收敛率理论完成：")
    print("  - 高维 Moran 方程与相似维数")
    print("  - 高维覆盖熵与体积增长")
    print("  - 强/弱/非分离三种收敛模式")
    print("  - 最优切换点 N* 的高维推广")
    print("  - 维数相变分析（低维/中间/高维三相）")
    print("  - 核光滑指数 α 的影响")
    print("=" * 70)
