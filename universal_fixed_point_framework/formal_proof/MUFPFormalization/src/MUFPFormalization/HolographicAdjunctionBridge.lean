import Mathlib.Tactic
import MUFPFormalization.EccentricPeriodicOrbit
import MUFPFormalization.PeriodicOrbitCount
import MUFPFormalization.RAP5a_explicit_adjunction
import MUFPFormalization.AreaEntropySynthesis

/-!
# 全息伴随桥：面积=熵挂到 D⊣R 伴随（环节 3c，2026-10-24）

对应 `notes/04_lorentz_gravity/全息定理化论证骨架_RecSp对偶.md` §2 环节 3c
（**缺口核心（语义层）**：算术恒等式 ≠ 伴随同构推论——"面积算符/熵算符作为
同构两侧函子载荷"的定义未固化）。本文件给出**函子载荷**：

- **面积算符（Rec 侧载荷）** `areaAt X := normalizedArea (boundaryDefect (orbitCount X)) 2`：
  Rec 对象 X 的边界缺陷度（Rec→Sp 对数映射定律）经旋量纤维归一化（codim=2 ⟹ 1/4）；
- **熵算符（Sp 侧载荷）** `entropyAt E := entropyOfRange (orbitCount E.src)`：
  SpImD 元素 E 的 Rec 源对象简并度谱熵（经 RIm 投影读出，熵在谱侧统计）；
- ★ **伴随对象对应**：伴随 DIm ⊣ RIm（RAP5a 已机检）把 Rec 对象 X 送到谱像
  (X, D(X), iso)——`holographic_adjunction_identity`：areaAt X = entropyAt (DIm_obj X)
  ——**面积=熵成为伴随对象对应的推论**；`holographic_adjunction_on_iso`：对任意
  SpImD 元素 E（不必是 DIm 像），areaAt (RIm_obj E) = entropyAt E——伴随同构
  DR_iso : DIm(RIm E) ≅ E 两侧读数一致。

诚实边界：函子载荷（面积=defect 归一化、熵=简并谱熵）为**指认级**（物理论证）；
本文件把载荷显式化并证明其在伴随对象对应下的一致性（算术层由
`AreaEntropySynthesis.area_entropy_identity` 提供）；"载荷即物理面积/熵"的等同
仍为语义缺口 1c/2c。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.HolographicAdjunction

open MUFPF.EccentricOrbit
open MUFPF.PeriodicOrbitCount
open MUFPF.ExplicitAdjunction

/-- 面积算符（Rec 侧载荷）：X 的边界缺陷度（4·ln g）经旋量纤维归一化
    （normalizedArea codim=2 ⟹ /4）。 -/
noncomputable def areaAt (X : RecObj) : ℝ :=
  MUFPF.AreaOperator.normalizedArea (MUFPF.boundaryDefect (orbitCount X)) 2

/-- 熵算符（Sp 侧载荷）：SpImD 元素 E 的 Rec 源对象简并度谱熵（经 RIm 投影读出）。 -/
noncomputable def entropyAt (E : SpImD) : ℝ :=
  MUFPF.HolographicEntropy.entropyOfRange (orbitCount E.src)

/-- ★ 伴随对象对应：DIm 把 Rec 对象 X 送到谱像 (X, D(X), iso)，
    Rec 侧面积 = 谱侧熵（面积=熵成为伴随对应的推论）。 -/
theorem holographic_adjunction_identity (X : RecObj) (h : ∃ x : X.T, periodicPoint X x) :
    areaAt X = entropyAt (DIm_obj X) := by
  unfold areaAt entropyAt DIm_obj
  exact MUFPF.Holographic.area_entropy_identity (orbitCount X) (orbitCount_pos X h)

/-- ★ 伴随同构两侧一致：对任意 SpImD 元素 E（不必是 DIm 像），
    Rec 源对象面积 = E 的熵——DR_iso : DIm(RIm E) ≅ E 两侧读数相同
    （全息=定理形态：伴随对象同构 ⟹ 面积=熵）。 -/
theorem holographic_adjunction_on_iso (E : SpImD) (h : ∃ x : E.src.T, periodicPoint E.src x) :
    areaAt (RIm_obj E) = entropyAt E := by
  unfold areaAt entropyAt RIm_obj
  exact MUFPF.Holographic.area_entropy_identity (orbitCount E.src) (orbitCount_pos E.src h)

end MUFPF.HolographicAdjunction
