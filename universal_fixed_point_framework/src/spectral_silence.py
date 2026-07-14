"""
spectral_silence.py

谱静默（Spectral Silence）：高维递归系统的低维不可见性机制。

核心思想：额外维度的不可观测性不是因为空间被卷曲（紧致化），
而是因为高维谱成分在谱测度中处于"静默"状态——无离散本征态可激发。

四个静默判据：
  1. 连续谱条件：Σ_silent ⊆ σ_ac(A)  （无离散本征态）
  2. 零测度条件：μ_E(Σ_silent) = 0   （谱测度中权重为零）
  3. LACI 高条件：γ = 0               （谱间隙消失，不可稳定捕获）
  4. 轨道权重条件：O(H_silent) = 0    （规范群作用下无不变量）

对应 Paper I §4.5 与 Paper II §5.4。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
import numpy as np


# ---------------------------------------------------------------------------
# 1. 谱型分类
# ---------------------------------------------------------------------------

SpectrumType = Literal["pure_point", "absolutely_continuous", "singular_continuous", "mixed"]


def classify_spectrum_type(
    eigenvalues: np.ndarray,
    eigenvalue_weights: np.ndarray | None = None,
    degeneracy_tol: float = 1e-8,
    continuous_tol: float = 1e-6,
) -> SpectrumType:
    """
    对给定谱进行类型分类。

    判据：
    - 纯点谱：所有特征值有明确权重 > 0，且无连续背景
    - 绝对连续谱：特征值密集分布（间距 < continuous_tol），权重平滑分布
    - 奇异连续谱：特征值密集但支撑在零 Lebesgue 测度集上（分形谱）
    - 混合谱：同时含有离散部分和连续部分

    参数
    ----------
    eigenvalues : np.ndarray
        谱值（升序）。
    eigenvalue_weights : np.ndarray, optional
        各特征值对应的谱测度权重。若未提供，取均匀权重。
    degeneracy_tol : float
        判断特征值是否简并的容差。
    continuous_tol : float
        判断特征值间距是否构成连续谱的容差。
    """
    n = len(eigenvalues)
    if n == 0:
        return "pure_point"

    if eigenvalue_weights is None:
        eigenvalue_weights = np.ones(n) / n

    # 计算特征值间距
    gaps = np.diff(eigenvalues)

    # 间距小于阈值的比例
    dense_ratio = np.mean(gaps < continuous_tol)

    # 权重分布：纯点谱权重集中在少数大值上
    weight_entropy = -np.sum(
        eigenvalue_weights * np.log(eigenvalue_weights + 1e-30)
    )
    max_entropy = np.log(n)
    normalized_entropy = weight_entropy / max_entropy if max_entropy > 0 else 0

    if dense_ratio < 0.3:
        # 大部分间距较大 → 离散谱
        return "pure_point"
    elif normalized_entropy > 0.8:
        # 权重均匀分布 → 绝对连续
        return "absolutely_continuous"
    else:
        # 密集但权重不均匀 → 奇异连续
        return "singular_continuous"


# ---------------------------------------------------------------------------
# 2. 谱静默判据
# ---------------------------------------------------------------------------

@dataclass
class SilenceCriterion:
    """单个静默判据的检测结果。"""
    name: str
    satisfied: bool
    value: float
    threshold: float
    description: str


@dataclass
class SpectralSilenceResult:
    """谱静默分析完整结果。"""
    is_silent: bool
    criteria: list[SilenceCriterion] = field(default_factory=list)
    silent_fraction: float = 0.0
    spectrum_type: str = "unknown"
    interpretation: str = ""

    def summary(self) -> str:
        lines = [f"谱静默分析结果: {'静默' if self.is_silent else '非静默'}"]
        lines.append(f"  谱型: {self.spectrum_type}")
        lines.append(f"  静默比例: {self.silent_fraction:.4f}")
        for c in self.criteria:
            status = "✓" if c.satisfied else "✗"
            lines.append(
                f"  [{status}] {c.name}: value={c.value:.6e}, "
                f"threshold={c.threshold:.6e}"
            )
        lines.append(f"  解读: {self.interpretation}")
        return "\n".join(lines)


class SpectralSilence:
    """
    谱静默分析器。

    对给定谱对象，检测其是否满足静默条件，并给出物理诠释。

    用法
    -----
    >>> analyzer = SpectralSilence(eigenvalues, weights)
    >>> result = analyzer.analyze()
    >>> print(result.summary())
    """

    def __init__(
        self,
        eigenvalues: np.ndarray,
        eigenvalue_weights: np.ndarray | None = None,
        orbit_weights: np.ndarray | None = None,
        tol: float = 1e-12,
    ):
        """
        参数
        ----------
        eigenvalues : np.ndarray
            谱算子 A 的特征值 μ_i（升序）。
        eigenvalue_weights : np.ndarray, optional
            各特征值的谱测度权重 μ_E({μ_i})。若未提供，取均匀权重。
        orbit_weights : np.ndarray, optional
            各特征子空间的轨道权重 O(H_{μ_i})。若未提供，默认为 1。
        tol : float
            数值容差。
        """
        self.eigenvalues = np.sort(np.asarray(eigenvalues, dtype=float))
        self.n = len(self.eigenvalues)

        if eigenvalue_weights is None:
            eigenvalue_weights = np.ones(self.n) / self.n
        self.weights = np.asarray(eigenvalue_weights, dtype=float)

        if orbit_weights is None:
            orbit_weights = np.ones(self.n)
        self.orbit_weights = np.asarray(orbit_weights, dtype=float)

        self.tol = tol

        # Koopman 特征值 λ_i = e^{-μ_i}
        self.koopman_eigenvalues = np.exp(-self.eigenvalues)

    # ------------------------------------------------------------------
    # 判据 1：连续谱条件
    # ------------------------------------------------------------------

    def check_continuous_spectrum(
        self,
        dense_tol: float = 1e-6,
        dense_ratio_threshold: float = 0.5,
    ) -> SilenceCriterion:
        """
        连续谱条件：静默子集 ⊆ σ_ac(A)。

        判据：特征值间距中，小于 dense_tol 的比例超过 dense_ratio_threshold。
        """
        if self.n < 2:
            return SilenceCriterion(
                name="连续谱条件",
                satisfied=False,
                value=0.0,
                threshold=dense_ratio_threshold,
                description="谱维数 < 2，无法判定连续性。",
            )

        gaps = np.diff(self.eigenvalues)
        # 归一化间距（相对于谱范围）
        spectral_range = self.eigenvalues[-1] - self.eigenvalues[0]
        if spectral_range < self.tol:
            # 所有特征值相同 → 高度简并 → 视为连续
            dense_ratio = 1.0
        else:
            normalized_gaps = gaps / spectral_range
            dense_ratio = float(np.mean(normalized_gaps < dense_tol))

        return SilenceCriterion(
            name="连续谱条件",
            satisfied=dense_ratio >= dense_ratio_threshold,
            value=dense_ratio,
            threshold=dense_ratio_threshold,
            description=f"间距小于 {dense_tol} 的比例 = {dense_ratio:.4f}",
        )

    # ------------------------------------------------------------------
    # 判据 2：零测度条件
    # ------------------------------------------------------------------

    def check_zero_measure(
        self,
        weight_threshold: float = 1e-8,
    ) -> SilenceCriterion:
        """
        零测度条件：μ_E(Σ_silent) = 0。

        判据：谱测度权重中，小于 weight_threshold 的总占比。
        """
        total_weight = self.weights.sum()
        if total_weight < self.tol:
            zero_fraction = 1.0
        else:
            normalized = self.weights / total_weight
            zero_fraction = float(np.sum(normalized < weight_threshold) / self.n)

        # 零测度条件：大部分权重接近零
        is_zero_measure = zero_fraction >= 0.5 or total_weight < self.tol

        return SilenceCriterion(
            name="零测度条件",
            satisfied=is_zero_measure,
            value=zero_fraction,
            threshold=0.5,
            description=f"权重 < {weight_threshold} 的比例 = {zero_fraction:.4f}",
        )

    # ------------------------------------------------------------------
    # 判据 3：LACI 高条件
    # ------------------------------------------------------------------

    def check_laci_high(
        self,
        gamma_threshold: float = 1e-6,
    ) -> SilenceCriterion:
        """
        LACI 高条件：谱间隙 γ = 0。

        判据：Koopman 特征值谱间隙 γ = 1 - λ₂/λ₁ 小于 gamma_threshold。
        当 γ → 0 时，LACI → ∞，谱不可稳定捕获。
        """
        lambdas = self.koopman_eigenvalues

        if len(lambdas) < 2:
            gamma = 1.0
        else:
            # 谱间隙 = 1 - λ₂/λ₁（λ₁ = max eigenvalue）
            lambda_max = lambdas[-1]
            if lambda_max < self.tol:
                gamma = 1.0
            else:
                # 找第二大的
                lambda_second = lambdas[-2] if len(lambdas) >= 2 else 0.0
                gamma = float(1.0 - lambda_second / max(lambda_max, self.tol))

        # 限制 gamma 到 [0, 1]
        gamma = max(0.0, min(1.0, gamma))

        return SilenceCriterion(
            name="LACI 高条件",
            satisfied=gamma < gamma_threshold,
            value=gamma,
            threshold=gamma_threshold,
            description=f"谱间隙 γ = {gamma:.6e}（γ → 0 ⇒ LACI → ∞）",
        )

    # ------------------------------------------------------------------
    # 判据 4：轨道权重条件
    # ------------------------------------------------------------------

    def check_orbit_weight_zero(
        self,
        orbit_threshold: float = 1e-8,
    ) -> SilenceCriterion:
        """
        轨道权重条件：O(H_silent) = 0。

        判据：轨道权重中，小于 orbit_threshold 的比例。
        """
        zero_orbit_fraction = float(
            np.sum(self.orbit_weights < orbit_threshold) / self.n
        )

        return SilenceCriterion(
            name="轨道权重条件",
            satisfied=zero_orbit_fraction >= 0.5,
            value=zero_orbit_fraction,
            threshold=0.5,
            description=f"轨道权重 < {orbit_threshold} 的比例 = {zero_orbit_fraction:.4f}",
        )

    # ------------------------------------------------------------------
    # 综合分析
    # ------------------------------------------------------------------

    def analyze(self) -> SpectralSilenceResult:
        """
        执行全部四个静默判据，给出综合结论。

        静默条件：四个判据中至少满足一个即为"静默"。
        满足越多，静默程度越高。
        """
        c1 = self.check_continuous_spectrum()
        c2 = self.check_zero_measure()
        c3 = self.check_laci_high()
        c4 = self.check_orbit_weight_zero()

        criteria = [c1, c2, c3, c4]
        satisfied_count = sum(1 for c in criteria if c.satisfied)

        # 谱型分类
        spectrum_type = classify_spectrum_type(
            self.eigenvalues, self.weights
        )

        # 静默比例：满足判据的比例
        silent_fraction = satisfied_count / 4.0

        # 综合判定：至少满足一个判据
        is_silent = satisfied_count >= 1

        # 物理诠释
        if satisfied_count >= 3:
            interpretation = (
                "高度静默：谱成分在低维中几乎完全不可见。"
                "对应额外维度的完全静默——替代紧致化。"
            )
        elif satisfied_count >= 2:
            interpretation = (
                "中度静默：谱成分在低维中大部分不可见。"
                "对应额外维度的主要静默——部分可观测残留。"
            )
        elif satisfied_count >= 1:
            interpretation = (
                "弱静默：谱成分在低维中部分不可见。"
                "对应额外维度的条件性静默——特定能标下可观测。"
            )
        else:
            interpretation = (
                "非静默：谱成分在低维中完全可观测。"
                "对应无额外维度或额外维度完全可见。"
            )

        return SpectralSilenceResult(
            is_silent=is_silent,
            criteria=criteria,
            silent_fraction=silent_fraction,
            spectrum_type=spectrum_type,
            interpretation=interpretation,
        )


# ---------------------------------------------------------------------------
# 3. 高维→低维谱静默映射
# ---------------------------------------------------------------------------

@dataclass
class DimensionalSilenceResult:
    """高维→低维谱静默映射结果。"""
    high_dim: int
    low_dim: int
    silent_eigenvalues: np.ndarray
    visible_eigenvalues: np.ndarray
    silence_ratio: float
    equivalence_holds: bool
    interpretation: str = ""


def dimensional_silence_map(
    high_dim_eigenvalues: np.ndarray,
    low_dim_eigenvalues: np.ndarray,
    high_dim_weights: np.ndarray | None = None,
    low_dim_weights: np.ndarray | None = None,
    tol: float = 1e-6,
) -> DimensionalSilenceResult:
    """
    高维→低维谱静默映射。

    分析高维谱中哪些成分在低维中"静默"（消失/不可见）。

    定理（谱静默等价性）：
      1. 几何图像：高维自由度在低维中不可见
      2. 谱图像：高维谱与低维谱的差集即为静默子集
      3. LACI 图像：高维 LACI 在低维限制下发生跳变

    参数
    ----------
    high_dim_eigenvalues : np.ndarray
        高维谱（全部特征值）。
    low_dim_eigenvalues : np.ndarray
        低维谱（可见特征值）。
    high_dim_weights, low_dim_weights : np.ndarray, optional
        各谱的测度权重。
    tol : float
        匹配容差。
    """
    high = np.sort(np.asarray(high_dim_eigenvalues, dtype=float))
    low = np.sort(np.asarray(low_dim_eigenvalues, dtype=float))

    # 找到高维谱中在低维谱里"静默"的特征值
    # （高维有但低维没有的）
    silent_mask = np.ones(len(high), dtype=bool)
    for i, h_val in enumerate(high):
        # 在低维谱中寻找匹配
        if len(low) > 0:
            distances = np.abs(low - h_val)
            if np.min(distances) < tol:
                silent_mask[i] = False

    silent_eigenvalues = high[silent_mask]
    visible_eigenvalues = high[~silent_mask]

    silence_ratio = float(len(silent_eigenvalues) / max(len(high), 1))

    # 检验谱静默等价性
    # 等价性成立条件：静默子集的 LACI 为 HIGH
    if len(silent_eigenvalues) > 0:
        silent_analyzer = SpectralSilence(silent_eigenvalues)
        silent_result = silent_analyzer.analyze()
        equivalence_holds = silent_result.is_silent
    else:
        equivalence_holds = True  # 无静默子集，平凡成立

    # 物理诠释
    high_dim = len(high)
    low_dim = len(low)
    if silence_ratio > 0.9:
        interp = (
            f"维度 {high_dim}→{low_dim}：{silence_ratio:.1%} 的谱静默。"
            f"额外维度几乎完全静默，低维观测者仅看到 {low_dim} 个自由度。"
        )
    elif silence_ratio > 0.5:
        interp = (
            f"维度 {high_dim}→{low_dim}：{silence_ratio:.1%} 的谱静默。"
            f"大部分额外维度静默，低维残留少量可观测信号。"
        )
    elif silence_ratio > 0:
        interp = (
            f"维度 {high_dim}→{low_dim}：{silence_ratio:.1%} 的谱静默。"
            f"少量额外维度静默，大部分可观测。"
        )
    else:
        interp = (
            f"维度 {high_dim}→{low_dim}：无谱静默。"
            f"高维与低维谱完全一致。"
        )

    return DimensionalSilenceResult(
        high_dim=high_dim,
        low_dim=low_dim,
        silent_eigenvalues=silent_eigenvalues,
        visible_eigenvalues=visible_eigenvalues,
        silence_ratio=silence_ratio,
        equivalence_holds=equivalence_holds,
        interpretation=interp,
    )


# ---------------------------------------------------------------------------
# 4. 谱静默与紧致化的对比
# ---------------------------------------------------------------------------

def compare_with_compactification() -> dict:
    """
    谱静默与弦论紧致化的系统对比。

    返回对比表与物理预言差异。
    """
    comparison = {
        "基本实体": {
            "紧致化": "几何流形（Calabi-Yau）",
            "谱静默": "谱对象（Rec/Spec）",
        },
        "不可见机制": {
            "紧致化": "空间被卷曲得太小（R ~ l_P）",
            "谱静默": "谱在测度中权重为零/连续谱",
        },
        "可激发性": {
            "紧致化": "KK 模式质量 ~ 1/R，大质量不可激发",
            "谱静默": "连续谱/零测度 → 无离散态可激发",
        },
        "唯一性": {
            "紧致化": "Landscape: 10^500+ 个 CY",
            "谱静默": "由 η_R 测度同构唯一确定",
        },
        "维度假设": {
            "紧致化": "需要额外维度是紧致流形",
            "谱静默": "不需要额外维度有流形结构",
        },
        "规范群导出": {
            "紧致化": "需要额外假设（规范场从几何导出）",
            "谱静默": "轨道函子 O 自然导出规范群",
        },
        "可证伪性": {
            "紧致化": "预言 KK 塔等间距质量谱",
            "谱静默": "预言无离散谱（连续背景/零测度），"
                      "若加速器在 TeV 发现连续谱背景而非 KK 塔则支持谱静默",
        },
    }

    return comparison


# ---------------------------------------------------------------------------
# 5. 物理实例
# ---------------------------------------------------------------------------

def demo_string_theory_silence() -> dict:
    """
    物理实例 1：弦论高维 → 低维谱静默。

    弦论 10 维 Cl(9,1) → SM 4 维 Cl(1,7)：
    - 高维：10 维谱（含额外 6 维自由度）
    - 低维：4 维可见谱
    - 静默：6 维对应的谱成分在低维中不可见
    """
    # 模拟 10 维谱（10 个特征值）
    # 前 4 个对应低维可见谱，后 6 个对应额外维度
    np.random.seed(42)
    low_dim_spectrum = np.array([0.1, 0.3, 0.5, 1.2])  # 4 维可见
    extra_dim_spectrum = np.array([8.5, 9.2, 10.1, 11.3, 12.7, 15.0])  # 6 维额外

    high_dim_spectrum = np.sort(np.concatenate([low_dim_spectrum, extra_dim_spectrum]))

    # 额外维度的谱权重很小（静默）
    high_dim_weights = np.concatenate([
        np.array([0.3, 0.25, 0.2, 0.15]),  # 低维可见，权重大
        np.array([1e-10] * 6),               # 额外维度，权重几乎为零
    ])

    # 分析高维谱的静默性
    analyzer = SpectralSilence(high_dim_spectrum, high_dim_weights)
    result = analyzer.analyze()

    # 维度静默映射
    dim_result = dimensional_silence_map(
        high_dim_spectrum, low_dim_spectrum,
        high_dim_weights=high_dim_weights,
    )

    return {
        "scenario": "弦论 Cl(9,1) → Cl(1,7) 谱静默",
        "high_dim_spectrum": high_dim_spectrum,
        "low_dim_spectrum": low_dim_spectrum,
        "silence_analysis": result,
        "dimensional_silence": dim_result,
        "conclusion": (
            f"10→4 维谱静默: {dim_result.silence_ratio:.1%} 的谱静默。"
            f"6 个额外维度对应的谱成分在低维中静默（权重 ~0）。"
            f"等价性检验: {'通过' if dim_result.equivalence_holds else '未通过'}。"
        ),
    }


def demo_holographic_silence() -> dict:
    """
    物理实例 2：全息 bulk → boundary 谱静默。

    AdS/CFT 中 bulk（体）的某些谱在 boundary（边界）上静默：
    - bulk 谱：包含体内部自由度（连续谱）
    - boundary 谱：CFT 算子谱（离散）
    - 静默：bulk 连续谱部分在 boundary 上不可见
    """
    # 模拟 bulk 谱：离散部分 + 连续部分
    np.random.seed(123)
    discrete_part = np.array([0.5, 1.0, 2.0, 3.5])  # CFT 算子谱
    continuous_part = np.linspace(5.0, 15.0, 50)    # bulk 连续谱

    bulk_spectrum = np.sort(np.concatenate([discrete_part, continuous_part]))

    # 权重：离散部分权重高，连续部分权重极低
    bulk_weights = np.concatenate([
        np.array([0.25, 0.20, 0.15, 0.10]),    # 离散部分
        np.full(50, 1e-8),                       # 连续部分静默
    ])

    # boundary 谱仅含离散部分
    boundary_spectrum = discrete_part

    analyzer = SpectralSilence(bulk_spectrum, bulk_weights)
    result = analyzer.analyze()

    dim_result = dimensional_silence_map(
        bulk_spectrum, boundary_spectrum,
        high_dim_weights=bulk_weights,
    )

    return {
        "scenario": "全息 bulk → boundary 谱静默",
        "bulk_spectrum_size": len(bulk_spectrum),
        "boundary_spectrum_size": len(boundary_spectrum),
        "silence_analysis": result,
        "dimensional_silence": dim_result,
        "conclusion": (
            f"bulk→boundary 谱静默: {dim_result.silence_ratio:.1%} 的谱静默。"
            f"bulk 连续谱部分在 boundary CFT 上静默。"
            f"等价性检验: {'通过' if dim_result.equivalence_holds else '未通过'}。"
        ),
    }


def demo_sm_gravity_silence() -> dict:
    """
    物理实例 3：GR+SM 统一谱中的引力静默。

    引力谱与物质谱的统一中，引力部分在低能下相对静默：
    - 统一谱：引力谱 + SM 谱
    - 低能观测：主要看到 SM 谱
    - 静默：引力谱在低能下权重极小（G_N 极小）
    """
    # SM 谱（13 维统一算子中的物质部分）
    sm_spectrum = np.array([0.1, 0.2, 0.35, 0.5, 0.8, 1.2, 1.7])
    # 引力谱（高频/高能，低能不可见）
    gravity_spectrum = np.array([20.0, 35.0, 50.0])

    unified_spectrum = np.sort(np.concatenate([sm_spectrum, gravity_spectrum]))

    # 引力部分轨道权重极小（G_N ~ 10^{-38} m_p^{-2}）
    unified_weights = np.concatenate([
        np.array([0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.10]),  # SM
        np.array([1e-38, 1e-38, 1e-38]),                         # 引力静默
    ])

    # 引力部分的轨道权重为零
    orbit_weights = np.concatenate([
        np.ones(7),        # SM 部分有规范群作用
        np.zeros(3),       # 引力部分无规范群不变量
    ])

    # 分析整体谱
    overall_analyzer = SpectralSilence(
        unified_spectrum, unified_weights, orbit_weights
    )
    overall_result = overall_analyzer.analyze()

    # 单独分析引力子谱（引力子空间本身的静默性）
    gravity_orbit_weights = np.zeros(3)  # 引力部分轨道权重全为零
    gravity_weights = np.array([1e-38, 1e-38, 1e-38])
    gravity_analyzer = SpectralSilence(
        gravity_spectrum, gravity_weights, gravity_orbit_weights
    )
    gravity_result = gravity_analyzer.analyze()

    # 维度静默映射：统一谱 → SM 谱
    dim_result = dimensional_silence_map(
        unified_spectrum, sm_spectrum,
        high_dim_weights=unified_weights,
    )

    return {
        "scenario": "GR+SM 统一谱中的引力静默",
        "unified_spectrum": unified_spectrum,
        "sm_spectrum": sm_spectrum,
        "gravity_spectrum": gravity_spectrum,
        "overall_analysis": overall_result,
        "gravity_subspace_analysis": gravity_result,
        "dimensional_silence": dim_result,
        "conclusion": (
            f"引力子空间静默: {gravity_result.silent_fraction:.0%} 的判据满足。"
            f" 引力谱（G_N ~ 10^{{-38}}）在低能下完全静默"
            f"（轨道权重=0, 测度权重~0）。"
            f" 维度映射: {dim_result.silence_ratio:.1%} 的统一谱在 SM 低能下静默。"
        ),
    }


# ---------------------------------------------------------------------------
# 6. 主入口
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 7. M理论层级谱静默转化
# ---------------------------------------------------------------------------

def m_theory_hierarchy_silence() -> dict:
    """
    M理论层级谱静默转化：M(11) → 超弦(10) → 弦论(10) → GR+SM(4)。
    
    完整层级转化过程：
    1. M理论(11维) → 超弦(10维)：第11维静默
    2. 超弦(10维) → 弦论(10维)：超对称破缺（谱等价，无静默）
    3. 弦论(10维) → GR+SM(4维)：6个额外维度静默
    
    返回各层级的静默分析结果。
    """
    m_theory_spectrum = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5])
    superstring_spectrum = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    string_spectrum = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    sm_spectrum = np.array([0.5, 1.0, 1.5, 2.0])
    
    m_theory_weights = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1e-8])
    superstring_weights = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    string_weights = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    sm_weights = np.array([0.25, 0.25, 0.25, 0.25])
    
    step1 = dimensional_silence_map(
        m_theory_spectrum, superstring_spectrum,
        high_dim_weights=m_theory_weights,
    )
    
    step2 = dimensional_silence_map(
        superstring_spectrum, string_spectrum,
        high_dim_weights=superstring_weights,
        low_dim_weights=string_weights,
    )
    
    step3 = dimensional_silence_map(
        string_spectrum, sm_spectrum,
        high_dim_weights=string_weights,
        low_dim_weights=sm_weights,
    )
    
    m_theory_analyzer = SpectralSilence(m_theory_spectrum, m_theory_weights)
    m_theory_result = m_theory_analyzer.analyze()
    
    superstring_analyzer = SpectralSilence(superstring_spectrum, superstring_weights)
    superstring_result = superstring_analyzer.analyze()
    
    string_analyzer = SpectralSilence(string_spectrum, string_weights)
    string_result = string_analyzer.analyze()
    
    sm_analyzer = SpectralSilence(sm_spectrum, sm_weights)
    sm_result = sm_analyzer.analyze()
    
    total_silence_ratio = step1.silence_ratio * step2.silence_ratio * step3.silence_ratio
    total_effective_silence = step1.silence_ratio + (1 - step1.silence_ratio) * step3.silence_ratio
    
    return {
        "hierarchy": [
            {
                "step": "M理论(11维) → 超弦(10维)",
                "source_dim": len(m_theory_spectrum),
                "target_dim": len(superstring_spectrum),
                "silence_ratio": step1.silence_ratio,
                "equivalence_holds": step1.equivalence_holds,
                "interpretation": step1.interpretation,
                "silent_dimensions": 1,
                "reason": "第11维（膜维度）静默",
            },
            {
                "step": "超弦(10维) → 弦论(10维)",
                "source_dim": len(superstring_spectrum),
                "target_dim": len(string_spectrum),
                "silence_ratio": step2.silence_ratio,
                "equivalence_holds": step2.equivalence_holds,
                "interpretation": step2.interpretation,
                "silent_dimensions": 0,
                "reason": "超对称破缺，谱等价（同构转化）",
            },
            {
                "step": "弦论(10维) → GR+SM(4维)",
                "source_dim": len(string_spectrum),
                "target_dim": len(sm_spectrum),
                "silence_ratio": step3.silence_ratio,
                "equivalence_holds": step3.equivalence_holds,
                "interpretation": step3.interpretation,
                "silent_dimensions": 6,
                "reason": "6个额外维度（Calabi-Yau）静默",
            },
        ],
        "spectral_analysis": {
            "m_theory": m_theory_result,
            "superstring": superstring_result,
            "string": string_result,
            "sm": sm_result,
        },
        "total_silence_ratio": total_silence_ratio,
        "total_effective_silence": total_effective_silence,
        "summary": {
            "total_dimensions_start": 11,
            "total_dimensions_end": 4,
            "silenced_dimensions": 7,
            "silenced_ratio": 7 / 11,
            "conclusion": (
                f"M理论(11维)经多层谱静默逐级约化为GR+SM(4维)。"
                f"总静默比={total_effective_silence:.1%}，"
                f"共静默7个维度（1个膜维度+6个Calabi-Yau维度）。"
                f"超弦→弦论为同构转化，无静默损失。"
            ),
        },
    }


def run_all_demos() -> dict:
    """运行全部谱静默演示。"""
    results = {}

    print("=" * 70)
    print("谱静默（Spectral Silence）演示")
    print("=" * 70)

    # 实例 1：弦论
    print("\n--- 实例 1：弦论高维 → 低维谱静默 ---")
    r1 = demo_string_theory_silence()
    print(r1["silence_analysis"].summary())
    print(r1["conclusion"])
    results["string_theory"] = r1

    # 实例 2：全息
    print("\n--- 实例 2：全息 bulk → boundary 谱静默 ---")
    r2 = demo_holographic_silence()
    print(r2["silence_analysis"].summary())
    print(r2["conclusion"])
    results["holographic"] = r2

    # 实例 3：GR+SM
    print("\n--- 实例 3：GR+SM 统一谱中的引力静默 ---")
    r3 = demo_sm_gravity_silence()
    print("  [整体谱分析]")
    print(r3["overall_analysis"].summary())
    print("  [引力子空间分析]")
    print(r3["gravity_subspace_analysis"].summary())
    print(r3["conclusion"])
    results["sm_gravity"] = r3

    # 对比表
    print("\n--- 谱静默 vs 紧致化 对比 ---")
    comparison = compare_with_compactification()
    for key, val in comparison.items():
        print(f"  {key}:")
        print(f"    紧致化: {val['紧致化']}")
        print(f"    谱静默: {val['谱静默']}")
    results["comparison"] = comparison

    # 实例 4：M理论层级谱静默转化
    print("\n--- 实例 4：M理论层级谱静默转化 ---")
    r4 = m_theory_hierarchy_silence()
    print("  M理论层级转化路径:")
    for step in r4["hierarchy"]:
        print(f"    {step['step']}:")
        print(f"      静默比: {step['silence_ratio']:.1%}")
        print(f"      静默维度: {step['silent_dimensions']}")
        print(f"      原因: {step['reason']}")
        print(f"      等价性检验: {'通过' if step['equivalence_holds'] else '未通过'}")
    print(f"  总静默比: {r4['total_effective_silence']:.1%}")
    print(f"  起始维度: {r4['summary']['total_dimensions_start']}维")
    print(f"  终止维度: {r4['summary']['total_dimensions_end']}维")
    print(f"  静默维度: {r4['summary']['silenced_dimensions']}维")
    print(f"  结论: {r4['summary']['conclusion']}")
    results["m_theory_hierarchy"] = r4

    print("\n" + "=" * 70)
    print("结论：谱静默作为紧致化的替代概念，在框架中自然实现。")
    print("额外维度的不可见性源于谱测度中的静默，而非几何紧致化。")
    print("M理论经多层谱静默逐级约化为GR+SM，共静默7个维度。")
    print("=" * 70)

    return results


if __name__ == "__main__":
    run_all_demos()
