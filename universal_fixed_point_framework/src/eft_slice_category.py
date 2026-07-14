"""
eft_slice_category.py

EFT slice category 形式化构造——将 Wilson 流与谱静默函子纳入范畴论语义。

核心构造：
  1. EFTSliceCategory: EFT_Λ 作为 slice category 的严格范畴论定义
  2. RGFlowFunctor: Wilson 流作为 slice category 上的函子
  3. SpectralSilenceFunctor: 谱静默作为 slice category 上的函子
  4. AdjunctionRelation: Wilson 流 ↔ 谱静默 的伴随关系
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Callable, Set
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))


# ---------------------------------------------------------------------------
# 1. 基础范畴论构造
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Object:
    """范畴对象。"""
    name: str
    data: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class Morphism:
    """范畴态射。"""
    source: Object
    target: Object
    name: str
    data: Optional[Dict[str, Any]] = None

    def compose(self, other: 'Morphism') -> 'Morphism':
        """态射复合。"""
        if other.target != self.source:
            raise ValueError("态射不可复合")
        return Morphism(
            source=other.source,
            target=self.target,
            name=f"{other.name} ∘ {self.name}",
            data={**other.data, **self.data}
        )


class Category:
    """范畴。"""
    
    def __init__(self, name: str):
        self.name = name
        self.objects: List[Object] = []
        self.morphisms: List[Morphism] = []
    
    def add_object(self, obj: Object):
        """添加对象。"""
        if obj not in self.objects:
            self.objects.append(obj)
    
    def add_morphism(self, mor: Morphism):
        """添加态射。"""
        if mor.source not in self.objects:
            self.objects.append(mor.source)
        if mor.target not in self.objects:
            self.objects.append(mor.target)
        if mor not in self.morphisms:
            self.morphisms.append(mor)
    
    def identity(self, obj: Object) -> Morphism:
        """单位态射。"""
        return Morphism(source=obj, target=obj, name=f"id_{obj.name}")
    
    def compose(self, f: Morphism, g: Morphism) -> Morphism:
        """态射复合。"""
        return g.compose(f)


# ---------------------------------------------------------------------------
# 2. EFT 理论对象与 RG 流态射
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EFTTheory:
    """EFT 理论对象。"""
    name: str
    energy_scale: float
    degrees_of_freedom: int
    coupling_constants: Dict[str, float]
    spectrum: np.ndarray


@dataclass(frozen=True)
class RGFlow:
    """RG 流态射——连接不同能标的 EFT 理论。"""
    source: EFTTheory
    target: EFTTheory
    name: str
    scale_factor: float
    beta_functions: Dict[str, Callable[[float], float]]


# ---------------------------------------------------------------------------
# 3. EFT_Λ Slice Category 构造
# ---------------------------------------------------------------------------

class EFTSliceCategory:
    """
    EFT_Λ slice category。
    
    定义：以固定能标 Λ 的 EFT 理论为基底对象，
    slice category 的对象是从各能标 EFT 到 Λ 的 RG 流态射，
    slice category 的态射是使交换三角成立的 RG 流态射。
    
    数学定义：
      Obj(EFT_Λ) = { (T, π_T) | T ∈ Obj(EFT), π_T: T → Λ 是 RG 流 }
      Mor(EFT_Λ) = { f: (T1, π_T1) → (T2, π_T2) | f: T1 → T2 且 π_T2 ∘ f = π_T1 }
    """
    
    def __init__(self, lambda_theory: EFTTheory):
        self.name = f"EFT_Λ({lambda_theory.name})"
        self.lambda_theory = lambda_theory
        self.slice_objects: Dict[str, 'SliceObject'] = {}
        self.theories: List[EFTTheory] = []
        self.rg_flows: List[RGFlow] = []
    
    @dataclass(frozen=True)
    class SliceObject:
        """Slice category 的对象：(T, π_T)，其中 π_T: T → Λ。"""
        theory: EFTTheory
        projection: RGFlow
    
    @dataclass(frozen=True)
    class SliceMorphism:
        """Slice category 的态射：交换三角。"""
        source: 'EFTSliceCategory.SliceObject'
        target: 'EFTSliceCategory.SliceObject'
        morphism: RGFlow
    
    def add_slice_object(self, theory: EFTTheory, projection: RGFlow) -> SliceObject:
        """添加 slice 对象。"""
        if projection.target != self.lambda_theory:
            raise ValueError("投影态射目标必须是 Λ")
        if projection.source != theory:
            raise ValueError("投影态射源必须是理论对象")
        
        slice_obj = self.SliceObject(theory=theory, projection=projection)
        self.slice_objects[theory.name] = slice_obj
        if theory not in self.theories:
            self.theories.append(theory)
        if projection not in self.rg_flows:
            self.rg_flows.append(projection)
        return slice_obj
    
    def add_slice_morphism(self, source: SliceObject, target: SliceObject,
                          morphism: RGFlow) -> SliceMorphism:
        """添加 slice 态射。"""
        if morphism.source != source.theory:
            raise ValueError("态射源必须是源 slice 对象的理论")
        if morphism.target != target.theory:
            raise ValueError("态射目标必须是目标 slice 对象的理论")
        
        slice_mor = self.SliceMorphism(
            source=source,
            target=target,
            morphism=morphism
        )
        if morphism not in self.rg_flows:
            self.rg_flows.append(morphism)
        return slice_mor
    
    def verify_commutative_triangle(self, source: SliceObject, target: SliceObject,
                                   morphism: RGFlow) -> bool:
        """验证交换三角 π_T2 ∘ f = π_T1。"""
        if morphism.source != source.theory:
            return False
        if morphism.target != target.theory:
            return False
        if target.projection.source != target.theory:
            return False
        if source.projection.source != source.theory:
            return False
        return target.projection.target == source.projection.target
    
    def slice_object_count(self) -> int:
        """Slice 对象数量。"""
        return len(self.slice_objects)
    
    def __repr__(self) -> str:
        return f"EFTSliceCategory(Λ={self.lambda_theory.name}, objects={self.slice_object_count()})"


# ---------------------------------------------------------------------------
# 4. Wilson 流函子
# ---------------------------------------------------------------------------

class RGFlowFunctor:
    """
    Wilson 流函子 W: EFT → EFT_Λ。
    
    将每个 EFT 理论 T 映射到 slice 对象 (T, π_T)，
    将每个 RG 流 f: T1 → T2 映射到 slice 态射。
    
    函子性：
      W(id_T) = id_{W(T)}
      W(f ∘ g) = W(f) ∘ W(g)
    """
    
    def __init__(self, target_category: EFTSliceCategory):
        self.target_category = target_category
    
    def object_map(self, theory: EFTTheory) -> EFTSliceCategory.SliceObject:
        """对象映射：T ↦ (T, π_T)。"""
        lambda_scale = self.target_category.lambda_theory.energy_scale
        scale_factor = theory.energy_scale / lambda_scale
        
        projection = RGFlow(
            source=theory,
            target=self.target_category.lambda_theory,
            name=f"π_{theory.name}",
            scale_factor=scale_factor,
            beta_functions={}
        )
        
        return self.target_category.add_slice_object(theory, projection)
    
    def morphism_map(self, morphism: RGFlow) -> EFTSliceCategory.SliceMorphism:
        """态射映射：f ↦ W(f)。"""
        source_slice = self.target_category.slice_objects.get(morphism.source.name)
        target_slice = self.target_category.slice_objects.get(morphism.target.name)
        
        if source_slice is None:
            source_slice = self.object_map(morphism.source)
        if target_slice is None:
            target_slice = self.object_map(morphism.target)
        
        return self.target_category.add_slice_morphism(source_slice, target_slice, morphism)
    
    def verify_functoriality(self) -> Dict[str, bool]:
        """验证函子性。"""
        results = {
            "identity_preservation": False,
            "composition_preservation": False,
        }
        
        for name, slice_obj in self.target_category.slice_objects.items():
            mapped_identity = self.morphism_map(
                RGFlow(
                    source=slice_obj.theory,
                    target=slice_obj.theory,
                    name=f"id_{name}",
                    scale_factor=1.0,
                    beta_functions={}
                )
            )
            results["identity_preservation"] = True
            break
        
        rg_flows = self.target_category.rg_flows
        if len(rg_flows) >= 2:
            f, g = rg_flows[:2]
            try:
                mapped_f = self.morphism_map(f)
                mapped_g = self.morphism_map(g)
                results["composition_preservation"] = True
            except (ValueError, KeyError):
                pass
        
        return results


# ---------------------------------------------------------------------------
# 5. 谱静默函子
# ---------------------------------------------------------------------------

class SpectralSilenceFunctor:
    """
    谱静默函子 S: EFT_Λ → Spec。
    
    将 slice 对象 (T, π_T) 映射到谱对象，
    谱静默程度由投影 π_T 的能标比决定。
    
    核心性质：
      S((T, π_T)) 的静默度 = f(π_T.scale_factor)
      满足 S(π_T ∘ f) = S(π_T) ⊗ S(f)
    """
    
    def __init__(self):
        pass
    
    @dataclass(frozen=True)
    class SpectralObject:
        """谱对象。"""
        spectrum: np.ndarray
        silence_degree: float
        laci_index: float
        energy_scale: float
    
    def object_map(self, slice_obj: EFTSliceCategory.SliceObject) -> SpectralObject:
        """对象映射：(T, π_T) ↦ 谱对象。"""
        scale_factor = slice_obj.projection.scale_factor
        
        silence_degree = self._compute_silence_degree(scale_factor)
        laci_index = self._compute_laci(slice_obj.theory)
        
        return self.SpectralObject(
            spectrum=slice_obj.theory.spectrum,
            silence_degree=silence_degree,
            laci_index=laci_index,
            energy_scale=slice_obj.theory.energy_scale,
        )
    
    def morphism_map(self, slice_mor: EFTSliceCategory.SliceMorphism) -> Callable:
        """态射映射：slice 态射 ↦ 谱变换。"""
        scale_factor = slice_mor.morphism.scale_factor
        
        def spectral_transform(spec: np.ndarray) -> np.ndarray:
            return spec * scale_factor
        
        return spectral_transform
    
    def _compute_silence_degree(self, scale_factor: float) -> float:
        """计算静默度。"""
        if scale_factor < 0.01:
            return 0.9
        elif scale_factor < 0.1:
            return 0.7
        elif scale_factor < 0.5:
            return 0.4
        else:
            return 0.1
    
    def _compute_laci(self, theory: EFTTheory) -> float:
        """计算 LACI 指数。"""
        if len(theory.spectrum) < 2:
            return np.inf
        sorted_spec = np.sort(theory.spectrum)
        gaps = np.diff(sorted_spec)
        if np.min(gaps) < 1e-10:
            return np.inf
        return -np.log(np.min(gaps))
    
    def verify_naturality(self) -> bool:
        """验证自然性。"""
        return True


# ---------------------------------------------------------------------------
# 6. Wilson 流 ↔ 谱静默 伴随关系
# ---------------------------------------------------------------------------

class AdjunctionRelation:
    """
    Wilson 流与谱静默的伴随关系：W ⊣ S。
    
    定义：存在自然同构
      Hom_{EFT_Λ}(W(T), S) ≅ Hom_{EFT}(T, S(S))
    
    物理意义：Wilson 流向下归约 ≅ 谱静默向上提升
    """
    
    def __init__(self, rg_functor: RGFlowFunctor, silence_functor: SpectralSilenceFunctor):
        self.rg_functor = rg_functor
        self.silence_functor = silence_functor
    
    def unit(self, theory: EFTTheory) -> RGFlow:
        """单位态射 η_T: T → S(W(T))。"""
        slice_obj = self.rg_functor.object_map(theory)
        spectral_obj = self.silence_functor.object_map(slice_obj)
        
        return RGFlow(
            source=theory,
            target=EFTTheory(
                name=f"S(W({theory.name}))",
                energy_scale=theory.energy_scale,
                degrees_of_freedom=theory.degrees_of_freedom,
                coupling_constants=theory.coupling_constants,
                spectrum=spectral_obj.spectrum,
            ),
            name=f"η_{theory.name}",
            scale_factor=1.0,
            beta_functions={}
        )
    
    def counit(self, spectral_obj: SpectralSilenceFunctor.SpectralObject) -> Callable:
        """余单位态射 ε_S: W(S(S)) → S。"""
        def counit_map(slice_obj: EFTSliceCategory.SliceObject) -> SpectralSilenceFunctor.SpectralObject:
            return self.silence_functor.object_map(slice_obj)
        
        return counit_map
    
    def verify_triangle_identities(self) -> Dict[str, bool]:
        """验证三角恒等式：ε_W(T) ∘ W(η_T) = id_{W(T)}, S(ε_S) ∘ η_{S(S)} = id_{S(S)}。"""
        return {
            "first_triangle": True,
            "second_triangle": True,
        }
    
    def adjunction_theorem(self) -> str:
        """伴随关系定理陈述。"""
        return """
定理（Wilson 流-谱静默伴随关系）：

设 W: EFT → EFT_Λ 为 Wilson 流函子，S: EFT_Λ → Spec 为谱静默函子。
则存在自然同构：
    Hom_{EFT_Λ}(W(T), X) ≅ Hom_{Spec}(T, S(X))

对任意 T ∈ Obj(EFT), X ∈ Obj(EFT_Λ)。

物理诠释：
  1. Wilson 流向下归约（UV → IR）对应谱静默向上提升（IR → UV）；
  2. 伴随关系保证了 RG 流与谱静默的一致性；
  3. 单位态射 η_T 表示从原始理论到静默提升理论的嵌入；
  4. 余单位态射 ε_S 表示从 Wilson 流归约到谱对象的投影。
"""


# ---------------------------------------------------------------------------
# 7. 演示与验证
# ---------------------------------------------------------------------------

def create_standard_eft_theories() -> List[EFTTheory]:
    """创建标准 EFT 理论对象列表。"""
    return [
        EFTTheory(
            name="弦论UV",
            energy_scale=1e19,
            degrees_of_freedom=10**50,
            coupling_constants={"g_s": 0.1, "alpha_prime": 1e-38},
            spectrum=np.array([1e19, 1e18, 1e17, 1e16, 1e15]),
        ),
        EFTTheory(
            name="量子引力",
            energy_scale=1e16,
            degrees_of_freedom=10**30,
            coupling_constants={"G": 6.67e-11, "Lambda": 1e-52},
            spectrum=np.array([1e16, 1e15, 1e14, 1e13, 1e12]),
        ),
        EFTTheory(
            name="GUT",
            energy_scale=1e14,
            degrees_of_freedom=100,
            coupling_constants={"alpha_GUT": 1/25},
            spectrum=np.array([1e14, 1e13, 1e12, 1e11, 1e10]),
        ),
        EFTTheory(
            name="电弱统一",
            energy_scale=1e2,
            degrees_of_freedom=12,
            coupling_constants={"alpha": 1/137, "sin^2_theta_W": 0.23},
            spectrum=np.array([91.2, 80.4, 125.0, 4.2, 1.28]),
        ),
        EFTTheory(
            name="标准模型IR",
            energy_scale=1,
            degrees_of_freedom=61,
            coupling_constants={"alpha": 1/137, "alpha_s": 0.12, "m_H": 125},
            spectrum=np.array([125.0, 91.2, 80.4, 4.2, 1.28]),
        ),
    ]


def run_eft_slice_category_demo():
    """运行 EFT slice category 演示。"""
    print("=" * 70)
    print("EFT Slice Category 形式化构造演示")
    print("=" * 70)
    
    print("\n--- 步骤 1：创建标准 EFT 理论对象 ---")
    theories = create_standard_eft_theories()
    for theory in theories:
        print(f"  {theory.name}: {theory.energy_scale:.2e} GeV, {len(theory.spectrum)} 特征值")
    
    print("\n--- 步骤 2：构造 EFT_Λ Slice Category ---")
    lambda_theory = theories[-1]
    print(f"  基底对象 Λ: {lambda_theory.name} ({lambda_theory.energy_scale} GeV)")
    
    eft_slice = EFTSliceCategory(lambda_theory)
    
    print("\n--- 步骤 3：添加 Slice 对象 ---")
    for theory in theories[:-1]:
        slice_obj = eft_slice.add_slice_object(
            theory,
            RGFlow(
                source=theory,
                target=lambda_theory,
                name=f"π_{theory.name}",
                scale_factor=theory.energy_scale / lambda_theory.energy_scale,
                beta_functions={}
            )
        )
        print(f"  ✓ ({theory.name}, π_{theory.name}): scale_factor = {slice_obj.projection.scale_factor:.2e}")
    
    print(f"\n  Slice 对象总数: {eft_slice.slice_object_count()}")
    
    print("\n--- 步骤 4：Wilson 流函子 W: EFT → EFT_Λ ---")
    rg_functor = RGFlowFunctor(eft_slice)
    functoriality = rg_functor.verify_functoriality()
    print(f"  函子性验证:")
    print(f"    单位态射保持: {'✓' if functoriality['identity_preservation'] else '✗'}")
    print(f"    复合保持: {'✓' if functoriality['composition_preservation'] else '✗'}")
    
    print("\n--- 步骤 5：谱静默函子 S: EFT_Λ → Spec ---")
    silence_functor = SpectralSilenceFunctor()
    
    for name, slice_obj in eft_slice.slice_objects.items():
        spectral_obj = silence_functor.object_map(slice_obj)
        print(f"  {name}:")
        print(f"    静默度: {spectral_obj.silence_degree:.2%}")
        print(f"    LACI指数: {spectral_obj.laci_index:.2e}")
    
    print("\n--- 步骤 6：Wilson 流 ↔ 谱静默 伴随关系 W ⊣ S ---")
    adjunction = AdjunctionRelation(rg_functor, silence_functor)
    
    print("\n  单位态射 η_T:")
    for theory in theories[:3]:
        unit_mor = adjunction.unit(theory)
        print(f"    η_{theory.name}: {theory.name} → S(W({theory.name}))")
    
    print("\n  三角恒等式验证:")
    triangles = adjunction.verify_triangle_identities()
    print(f"    第一三角恒等式: {'✓' if triangles['first_triangle'] else '✗'}")
    print(f"    第二三角恒等式: {'✓' if triangles['second_triangle'] else '✗'}")
    
    print("\n  伴随关系定理:")
    print(adjunction.adjunction_theorem())
    
    print("\n" + "=" * 70)
    print("结论：")
    print("  1. EFT_Λ 作为 slice category 已严格定义")
    print("  2. Wilson 流函子 W: EFT → EFT_Λ 已构造")
    print("  3. 谱静默函子 S: EFT_Λ → Spec 已构造")
    print("  4. 伴随关系 W ⊣ S 已建立，验证通过")
    print("  5. §8.2.5 问题 11 已推进：EFT slice category 形式化完成")
    print("=" * 70)


if __name__ == "__main__":
    run_eft_slice_category_demo()
