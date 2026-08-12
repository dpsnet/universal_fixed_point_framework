import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Int.Cast.Defs
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Tactic
import UFPFormalization.SpCategory

namespace UFPFormalization

open CategoryTheory

/-!
# PhotonTopologyExterior — 外显结构形式化（§6.17/§6.19/§6.20）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §6.17–§6.20

## 形式化范围（诚实边界）
本模块形式化外显结构的**代数骨架**（可机器证明部分）：
1. `Z2Charge`：σ Z₂ 值拓扑荷 = 加法幺半群同态 (α, +, 0) → (ZMod 2, +, 0)
   —— σ(X⊗Y) = σ(X) + σ(Y)（§6.17 保复合）+ σ(0) = 0（保单位元）。
   注：ZMod 2 加法经同构 0↦+1、1↦−1 对应乘法 ±1 的 σ，故加法形式即乘法形式
   （§6.10①"复合可加性 = 模 2 加法 = 乘法"）；
2. σ² = 1 自逆（ZMod 2 特征 2）：σ(x) + σ(x) = 0（§6.17 S3 / §7.28 S4 离散层类比）；
3. 环绕数模型实例（§6.10①）：σ(n) = n mod 2、⊗ = 加法——σ(n₁+n₂) = σ(n₁) + σ(n₂)；
4. `ObsChannel`（Obs 范畴对象，§6.20 S1：时间通道/力通道）；
5. `ExteriorData`（外显函子 E: Sp→Obs 对象层数据：σ + channel）。

**未形式化（登记开放项，§6.20 诚实边界）**：
- SpObj 上的 ⊗ 结构（§6.11① 开放项）——Z2Charge 在谱对象上的实例待其定义；
- 外显函子在**完整** Sp 范畴上的函子律——`exterior_functor_obstructed` 已证通道阻碍
  （须限制于 channel 保持子范畴，完整函子仍开放）；
- channel 的物理定义（观测通道选择的严格构造）。

**已形式化**：Obs 范畴实例 `obsCategory`（PLift 提升 Prop 值 Hom）；完整函子律的
通道阻碍定理 `exterior_functor_obstructed`（维度奇偶 channel 具体实例）。
-/

/-! ## §6.9/§6.17/§6.20：σ Z₂ 值拓扑荷 = 加法幺半群同态 -/

/-- Z₂ 值拓扑荷结构：σ : α → ZMod 2 为加法幺半群同态
    （保复合 σ(X⊗Y) = σ(X) + σ(Y) + 保单位元 σ(0) = 0；ZMod 2 加法经同构
    0↦+1、1↦−1 对应乘法 ±1 的 σ——§6.17 σ 幺半群同态 (Sp,⊗)→(Z₂,·)）。 -/
structure Z2Charge (α : Type) [AddMonoid α] where
  sigma : α → ZMod 2
  sigma_add : ∀ x y : α, sigma (x + y) = sigma x + sigma y
  sigma_zero : sigma 0 = 0

namespace Z2Charge

variable {α : Type} [AddMonoid α]

/-- 保复合（⊗）：σ(X⊗Y) = σ(X) + σ(Y)（ZMod 2 加法 = 乘法 ±1 下的 σ(X)·σ(Y)，§6.17）。 -/
theorem sigma_tensor (C : Z2Charge α) (x y : α) :
    C.sigma (x + y) = C.sigma x + C.sigma y :=
  C.sigma_add x y

/-- 保单位元：σ(0) = 0（平凡对象荷为零，§6.20 保恒等对象层）。 -/
theorem sigma_unit (C : Z2Charge α) :
    C.sigma 0 = 0 :=
  C.sigma_zero

/-- σ² = 1（Z₂ 自逆，§6.17 S3 / §7.28 S4 离散层）：σ(x) + σ(x) = 0
    （ZMod 2 特征 2；乘法 ±1 下即 (±1)² = 1——离散标记对偶闭合）。 -/
theorem sigma_self_inverse (C : Z2Charge α) (x : α) :
    C.sigma x + C.sigma x = 0 := by
  rw [← two_mul]
  have h2 : (2 : ZMod 2) = 0 := by
    decide
  rw [h2, zero_mul]

end Z2Charge

/-! ## §6.10①：环绕数模型实例——σ(n) = n mod 2、⊗ = 加法 -/

/-- 环绕数模型（§6.10①/§6.17 S4）：σ(n) = n mod 2、⊗ = ℤ 加法。
    σ(n₁+n₂) = σ(n₁) + σ(n₂)（模 2 加法 = 乘法 ±1 的 σ(n₁)·σ(n₂)）。 -/
def windingCharge : Z2Charge ℤ where
  sigma n := (n : ZMod 2)
  sigma_add x y := by
    -- ((x + y : ℤ) : ZMod 2) = (x : ZMod 2) + (y : ZMod 2)
    exact Int.cast_add x y
  sigma_zero := by
    rfl

/-- 环绕数模型 σ(0) = 0（平凡环绕数荷为零）。 -/
theorem winding_sigma_zero : windingCharge.sigma 0 = 0 := by
  rfl

/-- 环绕数模型 σ² = 1：σ(n) + σ(n) = 0（§6.17 S3 实例：光子环绕模 2 自逆）。 -/
theorem winding_self_inverse (n : ℤ) :
    windingCharge.sigma n + windingCharge.sigma n = 0 := by
  exact Z2Charge.sigma_self_inverse windingCharge n

/-! ## §6.20 S1：Obs 范畴——对象 = 观测通道（离散范畴） -/

/-- 观测通道（Obs 范畴对象，§6.20 S1）：时间通道 / 力通道。 -/
inductive ObsChannel where
  | time
  | force
deriving DecidableEq, Repr

/-- Obs 离散范畴实例（§6.20 S1 定义候选）：Hom X Y := PLift (X = Y)
    （PLift 将 Prop 值 Hom 提升为 Type 0，满足 mathlib `Category` 对 Hom : Type v 的要求；
    态射 = 恒等——通道投影 π_t/π_f 为外显函子 E 的态射作用，方向 Sp→Obs，不在 Obs 内部）。 -/
instance obsCategory : Category.{0, 0} ObsChannel where
  Hom X Y := PLift (X = Y)
  id X := ⟨rfl⟩
  comp := by
    intro X Y Z hXY hYZ
    exact ⟨hXY.1.trans hYZ.1⟩
  id_comp := by
    intro X Y f
    cases f
    rfl
  comp_id := by
    intro X Y f
    cases f
    rfl
  assoc := by
    intro W X Y Z f g h
    cases f
    cases g
    cases h
    rfl

/-! ## §6.20 S1-S2：外显函子 E: Sp→Obs 的对象层数据 -/

/-- 外显函子 E: Sp→Obs 的对象层数据（§6.20 定义候选）：
    σ（Z₂ 值离散标记）+ channel（观测通道选择）。
    ⊗ 结构未定义于 SpObj（§6.11① 开放项），σ 的幺半群同态律在抽象加法幺半群
    `Z2Charge` 上形式化；SpObj 实例待 ⊗ 定义后补（§6.20 诚实边界）。 -/
structure ExteriorData where
  sigma : SpObj → ZMod 2
  channel : SpObj → ObsChannel

/-- 外显函子对象映射（E_obj，§6.20）：谱对象 → 观测通道（channel 分量）。 -/
def exteriorObject (E : ExteriorData) (X : SpObj) : ObsChannel :=
  E.channel X

/-- 外显函子 σ 分量：E(X) = (σ(X), channel(X)) 的离散标记分量（§6.20 S2）。
    σ 的幺半群同态律（保复合/保单位元/自逆）由 `Z2Charge` 定理给出
    （抽象加法幺半群层，`windingCharge` 为具体实例）。 -/
def exteriorSigma (E : ExteriorData) (X : SpObj) : ZMod 2 :=
  E.sigma X

/-! ## §6.20 诚实边界：完整函子律的通道阻碍（实例证明） -/

/-- 维度奇偶外显数据候选：σ(X) = n mod 2（Z₂ 离散标记）、
    channel(X) = n 奇偶 → 力/时间通道（具体实现，非物理定义）。 -/
def dimParityExterior : ExteriorData where
  sigma X := (X.n : ZMod 2)
  channel X := if X.n % 2 = 0 then ObsChannel.time else ObsChannel.force

/-- 通道阻碍态射：Sp 对象 (1, 0) ⟶ (2, 0) 间的交织态射（A = 0，交织条件平凡）。
    channel(1,0) = force（1 奇）、channel(2,0) = time（2 偶）——两端通道不同。 -/
def channelObstructionMorphism : (⟨1, (0 : Matrix (Fin 1) (Fin 1) ℂ)⟩ : SpObj) ⟶
    ⟨2, (0 : Matrix (Fin 2) (Fin 2) ℂ)⟩ :=
  ⟨0, by simp⟩

/-- 完整函子律阻碍定理（§6.20 诚实边界"完整函子律"）：dimParityExterior 下存在
    Sp 态射 f，其两端通道不同——Obs 态射 Hom = PLift (channel 相等) 为空，
    故外显函子 E 不能在**完整** Sp 范畴上定义为函子（须限制于 channel 保持子范畴）。 -/
theorem exterior_functor_obstructed :
    ∃ (X Y : SpObj) (_f : X ⟶ Y),
      dimParityExterior.channel X ≠ dimParityExterior.channel Y := by
  refine ⟨⟨1, (0 : Matrix (Fin 1) (Fin 1) ℂ)⟩,
    ⟨2, (0 : Matrix (Fin 2) (Fin 2) ℂ)⟩, channelObstructionMorphism, ?_⟩
  norm_num [dimParityExterior]
  decide

end UFPFormalization
