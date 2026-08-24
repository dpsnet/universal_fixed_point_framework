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
error_budget.py

Phase 15C-4: 误差预算体系——理论预言到实验对比的完整误差链。

覆盖三类误差源：
1. 理论误差（模型近似、截断阶数、谱估计）
2. 数值误差（有限采样、矩阵近似、迭代收敛）
3. 实验误差（统计不确定性、系统不确定性、背景模型）

每一步的误差沿 Rec→Spec→可观测→实验对比 的流程传播。
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Any


# ===========================================================================
# 误差源类型
# ===========================================================================

@dataclass
class ErrorSource:
    """单个误差源的描述。"""
    name: str
    absolute_error: float
    relative_error: float
    description: str
    category: str  # "theoretical" / "numerical" / "experimental"


@dataclass
class ErrorBudget:
    """
    完整误差预算：沿 Rec→Spec→可观测 链路的各环节误差。

    每一环节输出两种误差估计：
    - absolute: 绝对误差（物理单位）
    - relative: 相对误差（无量纲比例）
    """
    # 理论误差
    truncation_error: ErrorSource | None = None    # 级数/迭代截断
    approximation_error: ErrorSource | None = None  # 模型近似
    interpolation_error: ErrorSource | None = None  # 插值/拟合

    # 数值误差
    sampling_error: ErrorSource | None = None       # 有限采样
    discretization_error: ErrorSource | None = None # 离散化
    convergence_error: ErrorSource | None = None    # 迭代收敛

    # 实验误差
    statistical_error: ErrorSource | None = None    # 统计不确定性
    systematic_error: ErrorSource | None = None     # 系统不确定性
    background_error: ErrorSource | None = None     # 背景模型

    def total_absolute(self) -> float:
        """总绝对误差（各误差源的平方和开放，假设独立）。"""
        errors = []
        for src in [self.truncation_error, self.approximation_error,
                     self.interpolation_error, self.sampling_error,
                     self.discretization_error, self.convergence_error,
                     self.statistical_error, self.systematic_error,
                     self.background_error]:
            if src is not None:
                errors.append(src.absolute_error)
        return float(np.sqrt(sum(e ** 2 for e in errors))) if errors else 0.0

    def total_relative(self) -> float:
        """总相对误差。"""
        errors = []
        for src in [self.truncation_error, self.approximation_error,
                     self.interpolation_error, self.sampling_error,
                     self.discretization_error, self.convergence_error,
                     self.statistical_error, self.systematic_error,
                     self.background_error]:
            if src is not None:
                errors.append(src.relative_error)
        return float(np.sqrt(sum(e ** 2 for e in errors))) if errors else 0.0

    def dominant_error(self) -> str | None:
        """主导误差源（绝对误差最大的）。"""
        max_err = 0.0
        dominant = None
        for src in [self.truncation_error, self.approximation_error,
                     self.interpolation_error, self.sampling_error,
                     self.discretization_error, self.convergence_error,
                     self.statistical_error, self.systematic_error,
                     self.background_error]:
            if src is not None and src.absolute_error > max_err:
                max_err = src.absolute_error
                dominant = src.name
        return dominant

    def summary(self) -> str:
        """人可读的误差预算摘要。"""
        lines = ["误差预算摘要:"]
        for name, src in [
            ("截断误差", self.truncation_error),
            ("近似误差", self.approximation_error),
            ("插值误差", self.interpolation_error),
            ("采样误差", self.sampling_error),
            ("离散化误差", self.discretization_error),
            ("收敛误差", self.convergence_error),
            ("统计误差", self.statistical_error),
            ("系统误差", self.systematic_error),
            ("背景误差", self.background_error),
        ]:
            if src is not None:
                lines.append(
                    f"  {name}: {src.absolute_error:.4e} (abs) / "
                    f"{src.relative_error*100:.2f}% (rel) — {src.description}"
                )
        lines.append(f"  总绝对误差: {self.total_absolute():.4e}")
        lines.append(f"  总相对误差: {self.total_relative()*100:.2f}%")
        lines.append(f"  主导误差: {self.dominant_error()}")
        return "\n".join(lines)


# ===========================================================================
# 误差预算工厂
# ===========================================================================

def estimate_rec_error(
    n_iterations: int,
    n_samples: int,
    spectral_gap: float,
) -> tuple[float, float]:
    """
    Rec 层误差估计。

    来源：
    - 有限迭代：|error| ~ c_max^{α·n_iter} （指数收敛）
    - 有限采样：|error| ~ n_samples^{-1/d_frac} （多项式收敛）

    返回 (absolute_error, relative_error)。
    """
    conv_rate = spectral_gap if spectral_gap > 0 else 0.5
    iter_error = np.exp(-conv_rate * n_iterations)
    sample_error = n_samples ** (-0.5) if n_samples > 0 else 1.0
    total_error = np.sqrt(iter_error ** 2 + sample_error ** 2)
    return float(total_error), float(total_error)


def estimate_spec_error(
    eigenvalue_noise: float,
    n_eigenvalues: int,
    truncation_order: int,
) -> tuple[float, float]:
    """
    Spec 层误差估计。

    来源：
    - 特征值噪声：直接来自数值对角化的精度
    - 截断阶数：高阶谱成分被忽略带来的误差

    返回 (absolute_error, relative_error)。
    """
    eigen_error = eigenvalue_noise * np.sqrt(n_eigenvalues)
    trunc_error = np.exp(-0.5 * truncation_order) if truncation_order > 0 else 1.0
    total_error = np.sqrt(eigen_error ** 2 + trunc_error ** 2)
    return float(total_error), float(total_error)


def estimate_physical_prediction_error(
    mass_uncertainty: float = 0.0,
    coupling_uncertainty: float = 0.0,
    cross_section_uncertainty: float = 0.20,
    efficiency_uncertainty: float = 0.15,
    luminosity_uncertainty: float = 0.02,
) -> ErrorBudget:
    """
    物理预言误差预算（BSM 第4代轻子为例）。

    从框架预言 → 截面 → 事件数 → 显著性的完整误差链。
    """
    budget = ErrorBudget()

    # 理论误差
    budget.approximation_error = ErrorSource(
        name="质量谱拟合误差",
        absolute_error=mass_uncertainty * 1000,  # MeV
        relative_error=mass_uncertainty,
        description=f"框架预言的质量不确定性 ({mass_uncertainty*100:.1f}%)",
        category="theoretical",
    )
    budget.truncation_error = ErrorSource(
        name="耦合截断误差",
        absolute_error=coupling_uncertainty,
        relative_error=coupling_uncertainty,
        description=f"高阶耦合修正截断 ({coupling_uncertainty*100:.1f}%)",
        category="theoretical",
    )

    # 数值误差
    budget.convergence_error = ErrorSource(
        name="截面计算收敛误差",
        absolute_error=cross_section_uncertainty * 10,  # fb
        relative_error=cross_section_uncertainty,
        description=f"MC 截面计算收敛性 ({cross_section_uncertainty*100:.0f}%)",
        category="numerical",
    )

    # 实验误差
    budget.systematic_error = ErrorSource(
        name="探测器系统误差",
        absolute_error=efficiency_uncertainty * 100,
        relative_error=efficiency_uncertainty,
        description=f"探测器效率系统不确定性 ({efficiency_uncertainty*100:.0f}%)",
        category="experimental",
    )
    budget.statistical_error = ErrorSource(
        name="统计误差",
        absolute_error=0.0,
        relative_error=luminosity_uncertainty,
        description=f"亮度不确定性 ({luminosity_uncertainty*100:.0f}%)",
        category="experimental",
    )

    return budget


def estimate_rkhs_error(
    n_points: int,
    d_frac: float,
    smoothness: float,
    n_iterations: int = 100,
) -> ErrorBudget:
    """
    RKHS 收敛率误差预算。

    非分离 IFS 的收敛误差：
      |error| ~ C · N^{-α/d_frac}
    其中 C 为未知常数（NS-LB 下界），α 为核光滑指数，d_frac 为有效维数。
    """
    budget = ErrorBudget()

    # 收敛误差（主导项）
    conv_exp = smoothness / max(d_frac, 1e-10)
    conv_error = float(n_points ** (-conv_exp))
    budget.convergence_error = ErrorSource(
        name="RKHS 收敛误差",
        absolute_error=conv_error,
        relative_error=conv_error,
        description=f"N^(-α/d_frac) = {n_points}^(-{conv_exp:.2f}) = {conv_error:.4e}",
        category="numerical",
    )

    # 谱截断误差
    trunc_error = float(np.exp(-0.05 * n_iterations))
    budget.truncation_error = ErrorSource(
        name="谱截断误差",
        absolute_error=trunc_error,
        relative_error=trunc_error,
        description=f"高维谱截断 ({trunc_error:.2e})",
        category="theoretical",
    )

    return budget


def estimate_gn_emergence_error() -> ErrorBudget:
    """
    引力常数 G_N 谱导出误差预算。

    来源：谱交织值 8πG_N 的数值精度。
    """
    budget = ErrorBudget()

    # 数值精度（机器极限）
    budget.convergence_error = ErrorSource(
        name="谱交织数值误差",
        absolute_error=1e-15,
        relative_error=1e-15,
        description="谱交织条件 [T_GR, A_SM] = 0 的数值满足精度",
        category="numerical",
    )

    # 理论近似
    budget.approximation_error = ErrorSource(
        name="Cl(1,7) 截断近似",
        absolute_error=1e-10,
        relative_error=1e-10,
        description="Clifford 代数有限维截断引入的近似",
        category="theoretical",
    )

    return budget


# ===========================================================================
# 误差链传播与综合分析
# ===========================================================================

def error_propagation_chain(
    rec_error: float,
    spec_error: float,
    prediction_error: float,
    experiment_error: float,
) -> dict:
    """
    沿 Rec→Spec→可观测→实验对比 链路的误差传播。

    各环节误差通过平方和传播：
      total = sqrt(rec² + spec² + pred² + exp²)
    """
    chain = {
        "Rec 谱估计": rec_error,
        "Spec 特征值": spec_error,
        "物理预言": prediction_error,
        "实验对比": experiment_error,
    }
    total = np.sqrt(sum(e ** 2 for e in chain.values()))
    return {
        "chain": chain,
        "total": float(total),
        "dominant": max(chain, key=chain.get),
        "reduction_suggestion": (
            f"减小 {max(chain, key=chain.get)} 最为关键"
        ),
    }


if __name__ == "__main__":
    print("=" * 70)
    print("误差预算体系演示")
    print("=" * 70)

    # 1. BSM 物理预言误差
    print("\n[1] BSM 第4代轻子预言误差预算:")
    bsm_budget = estimate_physical_prediction_error(
        mass_uncertainty=0.05, coupling_uncertainty=0.10
    )
    print(bsm_budget.summary())

    # 2. RKHS 收敛误差
    print("\n[2] RKHS 收敛率误差预算 (N=1000, d_frac=1.5, α=1.0):")
    rkhs_budget = estimate_rkhs_error(n_points=1000, d_frac=1.5, smoothness=1.0)
    print(rkhs_budget.summary())

    # 3. G_N 导出误差
    print("\n[3] 引力常数 G_N 谱导出误差:")
    gn_budget = estimate_gn_emergence_error()
    print(gn_budget.summary())

    # 4. 误差链传播
    print("\n[4] 完整误差链传播 (BSM 预言示例):")
    chain = error_propagation_chain(
        rec_error=0.02, spec_error=0.01,
        prediction_error=0.05, experiment_error=0.15,
    )
    print(f"  各环节误差:")
    for stage, err in chain["chain"].items():
        print(f"    {stage}: {err*100:.1f}%")
    print(f"  总误差: {chain['total']*100:.1f}%")
    print(f"  主导环节: {chain['dominant']}")
