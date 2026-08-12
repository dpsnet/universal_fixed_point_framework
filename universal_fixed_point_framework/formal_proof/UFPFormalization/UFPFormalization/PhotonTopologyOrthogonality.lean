import UFPFormalization.PhotonTopologyFunctorLaws
import Mathlib.CategoryTheory.LiftingProperties.Basic
import Mathlib.Tactic

namespace UFPFormalization

open CategoryTheory

/-!
# PhotonTopologyOrthogonality — P5-2 严格正交：范畴层 lifting 正交（双层统一之范畴层）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.5 P5-2
路线图: roadmap/phase62_photon_topology.md 62G（双层统一）

## 严格正交定义（非单点性代理）
范畴层严格正交（命题 1.2）= 法向态射类 N 对水平态射类 H 的**唯一 lifting 性质**：
∀ 方块 `CommSq f i p g`（i ∈ N、p ∈ H），存在**唯一**对角填充 d（d ≫ p = g 且 i ≫ d = f）。
mathlib `HasLiftingProperty` 提供存在性分量；唯一性分量由 Hom 集 subsingleton 保证（本模块证明）。

本模块具体实例（多能级子范畴，§3.3）：
- 法向类 N = {unfold i : A_i → P}（Rec→Sp 跳变/发射）；
- 水平类 H = {transition m k : A_m → A_k}（净跃迁，频率可加性 = 能量守恒）；
- 定理：unfold i ⊥ transition m k——存在且唯一的对角填充 = fold m（非平凡方块）。

## 双层统一（范畴-几何桥）
- 范畴层（本模块）：N ⊥ H 唯一 lifting 机器证明；
- 纤维丛层（#7 已闭合）：V⊥H 度量正交（`isCompl_orthogonal_standard`/`inf_eq_bot_of_inner_orthogonal`，
  PhotonTopologyFunctor.lean 机器证明）；
- 桥（登记）：法向↔V（垂直子空间）、水平↔H（水平子空间）——两层正交描述同一方向对，
  完整同构证明登记开放（需范畴-几何字典）。

**诚实边界**：H = {transition} 为 Δ 水平方向在 1-态射层的具体编码（桥的范畴侧实例）；
Δ 2-态射本身的严格定义（2-范畴结构）登记开放；"单点性"在本模块中仅作为**唯一性引理**
（Hom 集 subsingleton ⟹ 对角填充唯一），不冒充正交本身。
-/

/-! ## 范畴层严格正交：法向 ⊥ 水平（唯一 lifting 性质） -/

/-- **范畴层严格正交（存在性分量，mathlib lifting 性质）**：unfold i（法向）对 transition m k
    （水平）有左 lifting 性质——每个方块存在对角填充（= fold m）。非平凡实例（方块存在，
    与真空提升不同）。 -/
instance normalOrthogonalTransition {ι : Type u} (i m k : ι) :
    HasLiftingProperty (C := MultiObj ι) (MultiMor.unfold i) (MultiMor.transition m k) := by
  constructor
  intro f g _sq
  cases f
  cases g
  exact ⟨⟨MultiMor.fold m, by rfl, by rfl⟩⟩

/-- **严格正交 = 唯一 lifting（范畴层完整命题，命题 1.2 机器证明）**：法向 unfold i ⊥ 水平
    transition m k——每个方块的对角填充存在且唯一（唯一填充 = fold m；
    唯一性由 Hom(P, A_m) 单点性保证）。 -/
theorem normalOrthogonalTransitionUnique {ι : Type u} (i m k : ι) :
    ∀ (f : MultiMor (MultiObj.atom i) (MultiObj.atom m))
      (g : MultiMor MultiObj.photon (MultiObj.atom k))
      (_sq : CommSq (C := MultiObj ι) f (MultiMor.unfold i) (MultiMor.transition m k) g),
      ∃! l : MultiMor MultiObj.photon (MultiObj.atom m),
        multiComp (MultiMor.unfold i) l = f ∧ multiComp l (MultiMor.transition m k) = g := by
  intro f g _sq
  cases f
  cases g
  refine ⟨MultiMor.fold m, ?_, ?_⟩
  · constructor <;> rfl
  · intro l hl
    cases l
    rfl

/-- 唯一性来源（诚实归因）：Hom(P, A_m) 为 subsingleton（单点）⟹ 对角填充唯一。
    ——"单点性"在此是**唯一性引理**（严格正交的唯一分量），不是正交本身
    （存在分量由 lifting 性质 `normalOrthogonalTransition` 给出）。 -/
instance subsingleton_photon_to_atom {ι : Type u} (m : ι) :
    Subsingleton (MultiMor MultiObj.photon (MultiObj.atom m)) := by
  constructor
  intro a b
  cases a
  cases b
  rfl

end UFPFormalization
