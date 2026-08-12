import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Int.Cast.Defs
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
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
- SpObj 上的**完整** ⊗ 结构（Kronecker 矩阵内容 + 幺半群结合律的 Fin 维度管道）——§6.11①
  开放项；其**维度分量**的 Z₂ 同态结构已澄清（`Z2ChargeMul`/`dimParityCharge`）；
- channel 的物理定义（观测通道选择的严格构造）。

**已形式化**：Obs 范畴实例 `obsCategory`（PLift 提升 Prop 值 Hom）；完整函子律的
通道阻碍定理 `exterior_functor_obstructed`（维度奇偶 channel 具体实例）；channel
保持子范畴 `SpChan` + 外显函子正向构造 `exteriorFunctorChan`（map_id/map_comp
机器证明）+ 阻碍态射不在子范畴 `obstruction_not_in_subcategory`；⊗ 结构候选的
Z₂ 同态结构澄清——乘法目标 `Z2ChargeMul` + 维度奇偶实例 `dimParityCharge`
（σ(n)=n mod 2 为 ℕ 乘法同态）+ `winding_not_multiplicative_target`
（环绕数模型为加法目标、非乘法目标——框架 σ 非平凡性要求加法型 ⊗）；
§6.10 S5 三层次区分形式化——`Particle`（光子/费米子）+ `statistics`（统计类）
+ `windingClass`（环绕模 2 类）+ `projectionValue`（投影值）+ 
`photon_statistics_independent_of_winding`（统计类独立于环绕类，防混淆机器证明）
+ `winding_same_for_opposite`（投影值 ±1 → 同一环绕类，层级 1→2）。
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

/-! ## §6.20 诚实边界：channel 保持子范畴上的外显函子（正向构造） -/

/-- channel 保持子范畴对象：谱对象（channel 由 dimParityExterior 决定，无需额外数据）。 -/
structure SpChan where
  obj : SpObj

/-- channel 保持子范畴态射：Sp 态射 + channel 保持条件（两端通道相同）。 -/
@[ext]
structure SpChanHom (X Y : SpChan) where
  mor : X.obj ⟶ Y.obj
  chan : dimParityExterior.channel X.obj = dimParityExterior.channel Y.obj

instance spChanCategory : Category.{0, 0} SpChan where
  Hom X Y := SpChanHom X Y
  id X := ⟨𝟙 X.obj, rfl⟩
  comp f g := ⟨f.mor ≫ g.mor, f.chan.trans g.chan⟩
  id_comp := by
    intro X Y f
    ext; simp
  comp_id := by
    intro X Y f
    ext; simp
  assoc := by
    intro W X Y Z f g h
    ext; simp

/-- channel 保持子范畴上的外显函子 E: SpChan → Obs（§6.20 正向构造）：
    对象映射 = channel、态射映射 = PLift (channel 相等)（由 SpChanHom.chan 提供）。
    map_id/map_comp 机器证明——§6.20 诚实边界第 2 项正向闭合
    （完整 Sp 范畴不可行由 exterior_functor_obstructed 阻碍定理证明）。 -/
def exteriorFunctorChan : SpChan ⥤ ObsChannel where
  obj X := dimParityExterior.channel X.obj
  map {X Y} (f : X ⟶ Y) := ⟨f.chan⟩
  map_id _ := rfl
  map_comp _ _ := rfl

/-- 阻碍态射不在 channel 保持子范畴中：SpChanHom (1,0) (2,0) 为空
    （chan 条件要求两端通道相同，与阻碍定理矛盾）——阻碍定理与子范畴正向构造自洽
    （完整 Sp 范畴受阻、channel 保持子范畴可行，两定理互补闭合 §6.20 诚实边界第 2 项）。 -/
theorem obstruction_not_in_subcategory :
    ¬ Nonempty (SpChanHom ⟨⟨1, (0 : Matrix (Fin 1) (Fin 1) ℂ)⟩⟩
      ⟨⟨2, (0 : Matrix (Fin 2) (Fin 2) ℂ)⟩⟩) := by
  rintro ⟨f⟩
  have hneq : dimParityExterior.channel ⟨1, (0 : Matrix (Fin 1) (Fin 1) ℂ)⟩ ≠
      dimParityExterior.channel ⟨2, (0 : Matrix (Fin 2) (Fin 2) ℂ)⟩ := by
    norm_num [dimParityExterior]
    decide
  exact hneq f.chan

/-! ## §6.11① 推进：⊗ 结构候选的 Z₂ 同态结构澄清 -/

/-- 乘法目标 Z₂ 值拓扑荷：σ : α → ZMod 2 为**乘法**幺半群同态
    （σ(X⊗Y) = σ(X)·σ(Y) + σ(1) = 1——ZMod 2 乘法目标，对应维度/秩奇偶类
    在维度相乘的 ⊗（Kronecker 型）下的结构；与 `Z2Charge`（加法目标，±1 乘法
    同构下即框架 σ 的乘法形式）的环绕数模型（⊗=加法）互补）。 -/
structure Z2ChargeMul (α : Type) [Monoid α] where
  sigma : α → ZMod 2
  sigma_mul : ∀ x y : α, sigma (x * y) = sigma x * sigma y
  sigma_one : sigma 1 = 1

namespace Z2ChargeMul

variable {α : Type} [Monoid α]

/-- 保复合（⊗，乘法目标）：σ(X⊗Y) = σ(X)·σ(Y)（ZMod 2 乘法）。 -/
theorem sigma_tensor (C : Z2ChargeMul α) (x y : α) :
    C.sigma (x * y) = C.sigma x * C.sigma y :=
  C.sigma_mul x y

/-- 保单位元：σ(1) = 1（乘法单位元）。 -/
theorem sigma_unit (C : Z2ChargeMul α) :
    C.sigma 1 = 1 :=
  C.sigma_one

end Z2ChargeMul

/-- 维度奇偶 σ(n) = n mod 2：ℕ 乘法幺半群上的乘法目标同态
    （§6.11① SpObj ⊗ 候选的维度分量——Kronecker 型 ⊗ 维度相乘 ⟹ σ 乘法保持）。 -/
def dimParityCharge : Z2ChargeMul ℕ where
  sigma n := (n : ZMod 2)
  sigma_mul x y := by
    exact Nat.cast_mul x y
  sigma_one := by
    rfl

/-- 维度奇偶乘法保持：σ(n·m) = σ(n)·σ(m)（Kronecker 维度相乘的 Z₂ 结构）。 -/
theorem dimParity_sigma_mul (x y : ℕ) :
    dimParityCharge.sigma (x * y) = dimParityCharge.sigma x * dimParityCharge.sigma y :=
  dimParityCharge.sigma_mul x y

/-- 维度奇偶保单位元：σ(1) = 1。 -/
theorem dimParity_sigma_one : dimParityCharge.sigma 1 = 1 := by
  rfl

/-- 环绕数模型非乘法目标：σ(1+1) ≠ σ(1)·σ(1)（加法型 ⊗ 不满足 ZMod 2 乘法目标
    同态）——环绕数为**加法目标**同态（`Z2Charge`，±1 乘法同构下即框架 σ 的
    σ(X⊗Y)=σ(X)·σ(Y)），与维度奇偶的**乘法目标**（`Z2ChargeMul`）互补。 -/
theorem winding_not_multiplicative_target :
    windingCharge.sigma (1 + 1) ≠ windingCharge.sigma 1 * windingCharge.sigma 1 := by
  norm_num [windingCharge]
  decide

/-! ## §6.10 S5：三层次区分形式化（投影值 / 环绕模 2 类 / 统计类） -/

/-- 粒子类型（代数骨架）：光子（整数自旋玻色子）/ 费米子（半整数自旋）。 -/
inductive Particle where
  | photon
  | fermion

/-- 统计类（层级 3）：玻色子 +1（ZMod 2 记 0）、费米子 −1（记 1）——自旋-统计定理
    （整数/半整数自旋，交换对称/反对称）。 -/
def statistics (p : Particle) : ZMod 2 :=
  match p with
  | Particle.photon => 0
  | Particle.fermion => 1

/-- 环绕模 2 类（层级 2）：光子 s=±1 模 2 同值（非平凡类）、费米子旋量 Z₂ 变号（非平凡类）。 -/
def windingClass (p : Particle) : ZMod 2 :=
  match p with
  | Particle.photon => 1
  | Particle.fermion => 1

/-- 投影值（层级 1）：光子螺旋度 s=±1、费米子旋量 ±1/2——二元投影值（N_pts=2，§6.8②）。 -/
def projectionValue (p : Particle) : ZMod 2 :=
  match p with
  | Particle.photon => 0
  | Particle.fermion => 1

/-- 三层次区分定理（§6.10 S5）：光子统计类（玻色子 +1）≠ 环绕模 2 类（非平凡）
    ——统计类独立于环绕类（光子为玻色子但环绕非平凡，不可混为一谈）。 -/
theorem photon_statistics_independent_of_winding :
    statistics Particle.photon ≠ windingClass Particle.photon := by
  norm_num [statistics, windingClass]

/-- 费米子统计类 = 环绕类（均 −1）：费米子统计（反对称 −1）与其旋量 Z₂ 变号（非平凡）
    一致——但三层次仍区分（投影值层级 ≠ 统计/环绕类层级，§6.10 S5）。 -/
theorem fermion_statistics_eq_winding :
    statistics Particle.fermion = windingClass Particle.fermion := by
  norm_num [statistics, windingClass]

/-- 光子环绕模 2 同值（§6.10② S2 / S5 层级 1→2）：环绕数 n 与 −n 的 σ 值相同
    （ZMod 2 特征 2，−a = a）——投影值 s=±1 对应**同一**环绕模 2 类（层级 1 两值 → 层级 2 单值）。 -/
theorem winding_same_for_opposite (n : ℤ) :
    windingCharge.sigma n = windingCharge.sigma (-n) := by
  dsimp [windingCharge]
  rw [Int.cast_neg]
  symm
  rw [neg_eq_iff_add_eq_zero]
  rw [← two_mul]
  have h2 : (2 : ZMod 2) = 0 := by
    decide
  rw [h2, zero_mul]

end UFPFormalization
