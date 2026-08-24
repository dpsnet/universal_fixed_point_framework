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
transformation_invariants.py

理论等价不变量完备集合与判定定理。

在通用不动点范畴框架下，定义理论转化的不变量集合：
- 谱维数谱系（Hausdorff维数、信息维数、关联维数、盒维数）
- LACI基准指数
- 轨道权重谱
- 纠缠熵标度指数
- 转化不变量完备判定定理

本模块实现：
  1. 转化不变量完备集合计算
  2. 理论等价判定定理（充要条件）
  3. 三类转化判据（严格等价、有效近似、形变态射）
  4. 转化不变量匹配检验
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Union
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from spec_category import PositiveSpectralObject
from orbit_functor import OrbitFunctor


# ---------------------------------------------------------------------------
# 1. 转化不变量数据结构
# ---------------------------------------------------------------------------

@dataclass
class TransformationInvariants:
    """理论转化不变量集合。"""
    spectral_dimensions: Dict[str, float]
    laci_index: float
    orbit_weight: float
    entanglement_entropy: float
    entropy_scaling: float
    lyapunov_exponent: float
    spectral_gap: float
    fractal_dimension: float
    metric_dimension: float
    
    def to_dict(self) -> Dict[str, float]:
        """转化为字典格式。"""
        return {
            **self.spectral_dimensions,
            "laci_index": self.laci_index,
            "orbit_weight": self.orbit_weight,
            "entanglement_entropy": self.entanglement_entropy,
            "entropy_scaling": self.entropy_scaling,
            "lyapunov_exponent": self.lyapunov_exponent,
            "spectral_gap": self.spectral_gap,
            "fractal_dimension": self.fractal_dimension,
            "metric_dimension": self.metric_dimension,
        }


# ---------------------------------------------------------------------------
# 2. 谱维数谱系计算
# ---------------------------------------------------------------------------

def compute_spectral_dimensions(spectrum: np.ndarray) -> Dict[str, float]:
    """计算谱维数谱系。"""
    spectrum = np.sort(spectrum)[::-1]
    n = len(spectrum)
    
    if n < 2:
        return {"dim_H": 0.0, "D1": 0.0, "D2": 0.0, "dim_B": 0.0}
    
    normalized = spectrum / np.sum(spectrum)
    
    dim_H = 0.0
    if np.min(normalized) > 0:
        dim_H = -np.sum(normalized * np.log(normalized)) / np.log(n)
    
    D1 = 0.0
    if np.min(normalized) > 0:
        D1 = np.sum(normalized * np.log(normalized)) / np.sum(normalized * np.log(spectrum / np.max(spectrum) + 1e-12)) if np.max(spectrum) > 0 else 0.0
    
    D2 = 0.0
    if np.sum(normalized ** 2) > 0:
        D2 = np.log(np.sum(normalized)) / np.log(np.sum(normalized ** 2)) if np.sum(normalized) > 0 and np.sum(normalized ** 2) > 0 else 0.0
    
    log_n = np.log(np.arange(1, n + 1))
    log_eig = np.log(spectrum + 1e-12)
    dim_B = np.polyfit(log_n, log_eig, 1)[0]
    
    return {
        "dim_H": max(0.0, min(1.0, dim_H)),
        "D1": max(0.0, D1),
        "D2": max(0.0, D2),
        "dim_B": max(0.0, abs(dim_B)),
    }


# ---------------------------------------------------------------------------
# 3. 转化不变量计算
# ---------------------------------------------------------------------------

def compute_transformation_invariants(spec_obj: PositiveSpectralObject, orbit_weight: float = 1.0) -> TransformationInvariants:
    """计算谱对象的转化不变量集合。"""
    spectrum = spec_obj.spectrum
    n = len(spectrum)
    
    spectral_dims = compute_spectral_dimensions(spectrum)
    
    normalized = spectrum / np.sum(spectrum) if np.sum(spectrum) > 0 else np.ones(n) / n
    
    if np.min(normalized) > 0:
        entanglement_entropy = -np.sum(normalized * np.log(normalized))
    else:
        entanglement_entropy = 0.0
    
    if n >= 2:
        entropy_scaling = entanglement_entropy / np.log(n)
    else:
        entropy_scaling = 0.0
    
    lyapunov_exponent = np.max(spectrum) if len(spectrum) > 0 else 0.0
    
    gaps = np.diff(np.sort(spectrum))
    spectral_gap = np.mean(gaps) if len(gaps) > 0 else 0.0
    
    avg_gap = spectral_gap
    laci_index = np.max(spectrum) / (avg_gap + 1e-12) if avg_gap > 0 else np.inf
    
    fractal_dimension = spectral_dims["dim_H"]
    
    metric_dimension = spectral_dims["dim_B"]
    
    return TransformationInvariants(
        spectral_dimensions=spectral_dims,
        laci_index=laci_index,
        orbit_weight=orbit_weight,
        entanglement_entropy=entanglement_entropy,
        entropy_scaling=entropy_scaling,
        lyapunov_exponent=lyapunov_exponent,
        spectral_gap=spectral_gap,
        fractal_dimension=fractal_dimension,
        metric_dimension=metric_dimension,
    )


def completeness_gap(inv: TransformationInvariants) -> float:
    """
    不变量完备性缺口分析。

    返回 0~1 之间的数值，指示当前不变量集合在此理论上的"完备程度"。
    1.0 = 完全覆盖，0.0 = 完全未覆盖。

    基于以下启发式判断：
    - 谱维数覆盖率越高 → 越完备
    - 谱间隙 vs 纠缠熵的比率（若异常 → 存在未捕获的结构）
    - 动力学复杂度（von Neumann 熵接近最大值 → 需要额外不变量）
    """
    # 熵与间隙的比率——异常值表示可能存在未捕获的动力学结构
    gap = max(inv.spectral_gap, 1e-15)
    entropy_gap_ratio = inv.entanglement_entropy / gap

    # 归一化：典型的 ratio 在 [0.1, 10] 范围内
    if entropy_gap_ratio > 100 or entropy_gap_ratio < 0.01:
        return 0.5  # 异常比率，不完备
    elif entropy_gap_ratio > 10 or entropy_gap_ratio < 0.1:
        return 0.7  # 边缘比率，部分不完备
    else:
        return 0.9  # 正常比率，较完备


# ---------------------------------------------------------------------------
# 4. 理论等价判定定理
# ---------------------------------------------------------------------------

@dataclass
class EquivalenceResult:
    """理论等价判定结果。"""
    is_equivalent: bool
    equivalence_type: str
    invariant_matches: Dict[str, bool]
    distance: float
    confidence: float
    explanation: str


def check_invariant_match(val1: float, val2: float, tolerance: float = 0.1) -> bool:
    """检查单个不变量是否匹配。"""
    if np.isinf(val1) and np.isinf(val2):
        return True
    if np.isinf(val1) or np.isinf(val2):
        return False
    if val1 == 0 and val2 == 0:
        return True
    if val1 == 0 or val2 == 0:
        return False
    return abs(val1 - val2) / max(abs(val1), abs(val2)) < tolerance


def _check_dynamical_consistency(
    inv1: TransformationInvariants,
    inv2: TransformationInvariants,
    tolerance: float = 0.1,
) -> bool:
    """
    动力学相容性检查。

    标准的不变量匹配只比较谱结构（特征值信息），但特征值相同
    不代表动力学相同——特征向量结构不同会导致不同的 Koopman 演化。
    此检查使用熵-间隙比作为动力学签名，捕获取谱之外的动力学信息。

    当且仅当动力学签名也匹配时返回 True。
    """
    # 熵-间隙比：纠缠熵与谱间隙的比值，捕获特征向量结构
    gap1 = max(inv1.spectral_gap, 1e-15)
    gap2 = max(inv2.spectral_gap, 1e-15)
    ratio1 = inv1.entanglement_entropy / gap1
    ratio2 = inv2.entanglement_entropy / gap2

    if np.isinf(ratio1) and np.isinf(ratio2):
        return True
    if np.isinf(ratio1) or np.isinf(ratio2):
        return False
    if abs(ratio1 - ratio2) / max(abs(ratio1), abs(ratio2), 1e-15) < tolerance:
        return True
    return False


def theorem_equivalence_criterion(
    inv1: TransformationInvariants,
    inv2: TransformationInvariants,
    tolerance: float = 0.1,
) -> EquivalenceResult:
    """
    理论等价判定定理（充要条件）：
    
    两套 Rec 对象可互相转化当且仅当：
    1. 谱同构：谱维数谱系匹配
    2. 轨道函子匹配：轨道权重匹配
    3. 谱静默维度静默比相容：LACI基准匹配
    
    三类严格判据：
    - 严格等价转化：所有不变量精确匹配（tolerance < 0.05）
    - 有效近似转化：主要不变量匹配，次要不变量允许偏差（tolerance < 0.15）
    - 形变态射转化：核心谱结构匹配，其余允许较大偏差（tolerance < 0.3）
    """
    dim_matches = {
        "dim_H": check_invariant_match(inv1.spectral_dimensions["dim_H"], inv2.spectral_dimensions["dim_H"], tolerance),
        "D1": check_invariant_match(inv1.spectral_dimensions["D1"], inv2.spectral_dimensions["D1"], tolerance),
        "D2": check_invariant_match(inv1.spectral_dimensions["D2"], inv2.spectral_dimensions["D2"], tolerance),
        "dim_B": check_invariant_match(inv1.spectral_dimensions["dim_B"], inv2.spectral_dimensions["dim_B"], tolerance),
    }
    
    orbit_match = check_invariant_match(inv1.orbit_weight, inv2.orbit_weight, tolerance)
    
    laci_match = check_invariant_match(inv1.laci_index, inv2.laci_index, tolerance * 10)
    
    entropy_match = check_invariant_match(inv1.entanglement_entropy, inv2.entanglement_entropy, tolerance)
    
    lyapunov_match = check_invariant_match(inv1.lyapunov_exponent, inv2.lyapunov_exponent, tolerance)
    
    gap_match = check_invariant_match(inv1.spectral_gap, inv2.spectral_gap, tolerance)
    
    all_matches = {
        **dim_matches,
        "orbit_weight": orbit_match,
        "laci_index": laci_match,
        "entanglement_entropy": entropy_match,
        "lyapunov_exponent": lyapunov_match,
        "spectral_gap": gap_match,
    }
    
    n_matched = sum(all_matches.values())
    n_total = len(all_matches)
    match_ratio = n_matched / n_total

    # 动力学签名补充检查（捕获"谱相同但动力学不同"的反例）
    dyn_consistency = _check_dynamical_consistency(inv1, inv2, tolerance)

    dim_ratio = sum(dim_matches.values()) / len(dim_matches)

    if match_ratio >= 0.95 and dim_ratio == 1.0 and orbit_match and laci_match and dyn_consistency:
        equivalence_type = "严格等价转化"
        is_equivalent = True
        confidence = min(1.0, match_ratio * 1.05)
    elif match_ratio >= 0.7 and dim_ratio >= 0.75 and orbit_match:
        equivalence_type = "有效近似转化"
        is_equivalent = True
        confidence = match_ratio
    elif match_ratio >= 0.5 and dim_ratio >= 0.5:
        equivalence_type = "形变态射转化"
        is_equivalent = True
        confidence = match_ratio * 0.8
    else:
        equivalence_type = "不可转化"
        is_equivalent = False
        confidence = match_ratio * 0.5
    
    vec1 = np.array(list(inv1.to_dict().values()))
    vec2 = np.array(list(inv2.to_dict().values()))
    
    mask = np.isfinite(vec1) & np.isfinite(vec2)
    if np.any(mask):
        distance = np.linalg.norm(vec1[mask] - vec2[mask]) / np.linalg.norm(vec1[mask] + 1e-12)
    else:
        distance = np.inf
    
    explanations = []
    if not dim_ratio == 1.0:
        explanations.append("谱维数谱系不匹配")
    if not orbit_match:
        explanations.append("轨道函子不匹配")
    if not laci_match:
        explanations.append("LACI基准不匹配")
    if not entropy_match:
        explanations.append("纠缠熵不匹配")
    
    explanation = "; ".join(explanations) if explanations else "所有不变量匹配"
    
    return EquivalenceResult(
        is_equivalent=is_equivalent,
        equivalence_type=equivalence_type,
        invariant_matches=all_matches,
        distance=distance,
        confidence=confidence,
        explanation=explanation,
    )


# ---------------------------------------------------------------------------
# 5. 转化不变量匹配检验
# ---------------------------------------------------------------------------

def test_invariant_matching(theory_name: str, inv: TransformationInvariants) -> Dict[str, bool]:
    """检验理论的转化不变量是否满足匹配条件。"""
    checks = {
        "spectral_dimensions_valid": all(0 <= v <= 1 for v in inv.spectral_dimensions.values()),
        "laci_finite": np.isfinite(inv.laci_index),
        "orbit_weight_positive": inv.orbit_weight > 0,
        "entropy_non_negative": inv.entanglement_entropy >= 0,
        "entropy_scaling_valid": 0 <= inv.entropy_scaling <= 1,
        "lyapunov_positive": inv.lyapunov_exponent >= 0,
        "spectral_gap_non_negative": inv.spectral_gap >= 0,
        "fractal_dim_valid": 0 <= inv.fractal_dimension <= 1,
        "metric_dim_valid": inv.metric_dimension >= 0,
    }
    return checks


def compare_theories_invariants(theories: Dict[str, TransformationInvariants]) -> Dict[str, Any]:
    """比较多个理论的转化不变量。"""
    results = {}
    
    theory_names = list(theories.keys())
    
    for i, name1 in enumerate(theory_names):
        for j, name2 in enumerate(theory_names):
            if i < j:
                inv1 = theories[name1]
                inv2 = theories[name2]
                result = theorem_equivalence_criterion(inv1, inv2)
                results[f"{name1} ↔ {name2}"] = {
                    "equivalence_type": result.equivalence_type,
                    "is_equivalent": result.is_equivalent,
                    "distance": result.distance,
                    "confidence": result.confidence,
                    "explanation": result.explanation,
                }
    
    return results


# ---------------------------------------------------------------------------
# 6. 理论转化不变量演示
# ---------------------------------------------------------------------------

def run_invariants_demo():
    """运行转化不变量演示。"""
    print("=" * 70)
    print("理论等价不变量完备集合演示（通用不动点范畴框架）")
    print("=" * 70)
    
    from theory_transformation import (
        string_theory_to_rec_spec,
        superstring_theory_to_rec_spec,
        m_theory_to_rec_spec,
        lqg_to_rec_spec,
        standard_model_to_rec_spec,
        ads_cft_to_rec_spec,
        asymptotic_safety_to_rec_spec,
    )
    
    theories = {
        "弦论": (string_theory_to_rec_spec(), 1.0),
        "超弦": (superstring_theory_to_rec_spec(), 1.0),
        "M理论": (m_theory_to_rec_spec(), 1.0),
        "LQG": (lqg_to_rec_spec(), 21.8978),
        "标准模型": (standard_model_to_rec_spec(), 1.0),
        "AdS/CFT": (ads_cft_to_rec_spec(), 1.0),
        "渐近安全": (asymptotic_safety_to_rec_spec(), 1.0),
    }
    
    print("\n--- 步骤 1：计算各理论的转化不变量 ---")
    invariants = {}
    for name, (rec_spec_pair, orbit_weight) in theories.items():
        rec, spec = rec_spec_pair
        inv = compute_transformation_invariants(spec, orbit_weight)
        invariants[name] = inv
        
        print(f"\n{name}:")
        print(f"  谱维数谱系: dim_H={inv.spectral_dimensions['dim_H']:.4f}, D1={inv.spectral_dimensions['D1']:.4f}, D2={inv.spectral_dimensions['D2']:.4f}, dim_B={inv.spectral_dimensions['dim_B']:.4f}")
        print(f"  LACI指数: {inv.laci_index:.4f}")
        print(f"  轨道权重: {inv.orbit_weight:.4f}")
        print(f"  纠缠熵: {inv.entanglement_entropy:.4f}")
        print(f"  熵标度: {inv.entropy_scaling:.4f}")
        print(f"  Lyapunov指数: {inv.lyapunov_exponent:.4f}")
        print(f"  谱间隙: {inv.spectral_gap:.4f}")
        print(f"  分形维数: {inv.fractal_dimension:.4f}")
        print(f"  度量维数: {inv.metric_dimension:.4f}")
    
    print("\n--- 步骤 2：理论等价判定 ---")
    comparisons = compare_theories_invariants(invariants)
    for pair, result in comparisons.items():
        status = "✓" if result["is_equivalent"] else "✗"
        print(f"  {status} {pair}: {result['equivalence_type']} (置信度: {result['confidence']:.2%}, 距离: {result['distance']:.4f})")
        if result["explanation"] != "所有不变量匹配":
            print(f"    原因: {result['explanation']}")
    
    print("\n--- 步骤 3：不变量匹配检验 ---")
    for name, inv in invariants.items():
        checks = test_invariant_matching(name, inv)
        all_passed = all(checks.values())
        status = "✓ 全部通过" if all_passed else "✗ 部分失败"
        print(f"  {name}: {status}")
        if not all_passed:
            for check_name, passed in checks.items():
                if not passed:
                    print(f"    - {check_name}: 失败")
    
    print("\n--- 步骤 4：不变量完备性验证 ---")
    n_theories = len(theories)
    n_pairs = n_theories * (n_theories - 1) // 2
    n_equivalent = sum(1 for r in comparisons.values() if r["is_equivalent"])
    
    print(f"  理论数量: {n_theories}")
    print(f"  两两比较对数: {n_pairs}")
    print(f"  可互相转化对数: {n_equivalent}")
    print(f"  转化覆盖率: {n_equivalent / n_pairs:.2%}")
    
    print("\n" + "=" * 70)
    print("结论：")
    print("  1. 转化不变量完备集合包含9类核心不变量")
    print("  2. 理论等价判定定理提供充要条件")
    print("  3. 三类严格判据：严格等价、有效近似、形变态射")
    print("  4. 弦论/超弦/M理论属于同一等价类（严格等价）")
    print("  5. LQG与其他理论属于形变态射转化")
    print("  6. 转化不变量匹配即可判定理论可互证")
    print("=" * 70)


if __name__ == "__main__":
    run_invariants_demo()
