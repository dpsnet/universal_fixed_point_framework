/-
  BranchCounting.lean — 𝐒𝐩 4-范畴的分支计数与 d_H = ln(15) 推导
  ===========================================================

  本文件形式化 d_H = ln(15) 推导中的分支计数部分：

  1. 𝐒𝐩 严格 4-范畴的层次结构 → 5 个总层
  2. 主动生成层（非平凡态射层）计数 → 3
  3. 有效分支数 B = N_active × N_total = 15
  4. 条件定理：若 B = 15 且均匀收缩 r = e⁻¹，则 d_H = ln 15

  本文件不依赖交换律（specExchangeLaw），仅依赖层次结构计数。
-/

import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.DeriveFintype
import UFPFormalization.Unified3Theorem
import UFPFormalization.HigherSpCategory
import UFPFormalization.SpCategory
import UFPFormalization.DHStructuralAnalysis

open CategoryTheory
open UFPFormalization.Unified3
open UFPFormalization.DHStructural

namespace UFPFormalization.BranchCounting

/-! =========================================================
    §1 层次结构定义
   =========================================================

   𝐒𝐩 严格 4-范畴的完整层次结构：

    层 0: SpObj（对象）           ❌ 非主动（不生成态射自由度）
    层 1: SpHom（1-态射）         ✅ 主动（谱流映射）
    层 2: SpTwoMorphism（2-态射） ✅ 主动（同伦变换）
    层 3: SpThreeMorphism（3-态射） ✅ 主动（高阶变换）
    层 4: 4-态射（coherence）     ❌ 非主动（仅 coherence 条件）

   总层数 N_total = 5
   主动层数 N_active = 3
-/

/-- 𝐒𝐩 严格 4-范畴的层索引。 -/
inductive LayerIndex : Type
  | obj    : LayerIndex    -- 层 0：对象
  | one    : LayerIndex    -- 层 1：1-态射
  | two    : LayerIndex    -- 层 2：2-态射
  | three  : LayerIndex    -- 层 3：3-态射
  | four   : LayerIndex    -- 层 4：coherence
  deriving DecidableEq, Fintype

/-- 总层数 = 5（N_total 复用 DHStructural.N_total，母定义，2026-08-13 去重）。 -/

/-- 总层数等于 5 的验证。 -/
theorem total_layers_count : Fintype.card LayerIndex = 5 := by
  native_decide

/-- 层是否为主动生成层（即非平凡的态射层）。 -/
def isActive (l : LayerIndex) : Bool :=
  match l with
  | LayerIndex.obj   => false
  | LayerIndex.one   => true
  | LayerIndex.two   => true
  | LayerIndex.three => true
  | LayerIndex.four  => false

/-- 主动生成层集合。 -/
def ActiveLayers : Finset LayerIndex :=
  {LayerIndex.one, LayerIndex.two, LayerIndex.three}

/-- 主动生成层数 = 3（计数验证）。 -/
theorem active_layers_count : (ActiveLayers : Finset LayerIndex).card = 3 := by
  native_decide

/-- 主动生成层数等于统一 3 定理中的主动生成层数。 -/
theorem active_layers_eq_unified3 : Fintype.card ActiveMorphismLayer = (ActiveLayers : Finset LayerIndex).card := by
  rw [card_active_layers]
  native_decide

/-! =========================================================
   第二章 有效分支数 B
   =========================================================

   核心假设（分支组合原理）：
     IFS 吸引子的有效分支数 B 等于
       主动生成层数 × 总层数
        = 3 × 5 = 15

   理由：每个主动生成层（1-态射、2-态射、3-态射）产生一个
   独立的 IFS 收缩映射，而该映射在 5 个范畴层次上各有独立
   的固定点分支。由于 𝐒𝐩 是严格 n-范畴（每个层级的对象和
   态射都有明确的代数结构），这些分支在范畴等价意义下互不重叠。
-/

/-- 有效分支数 B = N_active × N_total。 -/
def B : ℕ := (ActiveLayers : Finset LayerIndex).card * N_total

/-- B = 15 的计算验证。 -/
theorem B_eq_15 : B = 15 := by
  unfold B N_total
  have h_active : (ActiveLayers : Finset LayerIndex).card = 3 := active_layers_count
  rw [h_active]

/-! =========================================================
   第三章 Moran 方程与 d_H = ln 15
   =========================================================

   在等权分支 + 均匀收缩的零阶近似下：
     Moran 方程：Σ_{k=1}^{B} r^{d_H} = B · r^{d_H} = 1
     均匀收缩率：r = e⁻¹（信息论最优静默因子，定理 R1）
     代入：15 · (e⁻¹)^{d_H} = 1
          → e^{d_H} = 15 → d_H = ln 15

   本节的"条件定理"形式化该推论：若假设成立，则 d_H = ln 15。
-/

/-- 均匀收缩率 r = e⁻¹、自然对数的底 e、ln(15) 复用 DHStructuralAnalysis
    （DHStructural.r / e / ln15，母定义，2026-08-13 去重）。 -/

/-- 条件定理：若有效分支数为 B = 15 且均匀收缩率为 r = e⁻¹，
    则 Moran 方程 B · r^{d_H} = 1 的解为 d_H = ln 15。
    （2026-07-27：改写为调用 `DHStructural.dH_moran_solution_unique`
    的唯一性定理，消除对不存在引理 `Real.exp_mul` 的依赖。） -/
theorem dH_from_branching :
    let B' : ℝ := (B : ℝ)
    let d_H : ℝ := ln15
    B' * (r ^ d_H) = 1 := by
  intro B' d_H
  have hB : B' = (15 : ℝ) := by
    have hB_nat : B = 15 := B_eq_15
    simpa using congrArg (fun n : ℕ => (n : ℝ)) hB_nat
  rw [hB]
  exact DHStructural.dH_moran_solution_unique.mpr rfl

/-- 条件定理的等价形式：e^{d_H} = 15。 -/
theorem exp_dH_eq_15 : Real.exp (ln15 : ℝ) = (15 : ℝ) :=
  calc
    Real.exp (ln15 : ℝ) = Real.exp (Real.log (15 : ℝ)) := rfl
    _ = (15 : ℝ) := Real.exp_log (by norm_num : (0 : ℝ) < (15 : ℝ))

/-! =========================================================
   第四章 偏差分析
   =========================================================

   观测值 d_H_fit ≈ 2.7095 与 ln15 ≈ 2.70805 的偏差
   δ ≈ 0.00145 源于四方面：

   1. 分支非等权：实际 IFS 的 3 个收缩映射权重不同
      （c₁ = S₃·S₄, c₂ = S₄, c₃ ≈ 1）
   2. 物理唯象修正：规范耦合、质量层级的差异
   3. 偏差量级 O(10⁻³) 与三代质量层级一致
-/

/-- d_H 的唯象拟合值 d_H_fit 与偏差 delta_fit = d_H_fit - ln15 复用
    DHStructuralAnalysis（DHStructural.d_H_fit / delta_fit，母定义，2026-08-13 去重）。 -/

/-- δ < 0.01（范畴底线偏差不超过 1%）。
    （2026-07-27：由 `DHStructural.ln15_gt_2708`（ln 15 > 2.708）闭合，
    消除 sorry。） -/
theorem delta_bound : delta_fit < (1 : ℝ) / 100 := by
  have h1 : (2.708 : ℝ) < Real.log 15 := DHStructural.ln15_gt_2708
  unfold delta_fit d_H_fit ln15
  linarith

/-! =========================================================
   第五章 与统一 3 定理的桥梁
   =========================================================

   统一 3 定理声明四个等式相等：
     d = N_gen = log₂(k_max) = N_active = 3

   本文件证明：
     B = N_active × N_total = 3 × 5 = 15
     ⇒ d_H = ln(15)（在零阶近似下）

   因此 d_H 的"范畴本质" ln(15) 是统一 3 定理在
   Hausdorff 维数上的体现：
     N_active = 3  ⇒  B = 15  ⇒  d_H ≈ ln(15)
-/

/-- 统一 3 定理与分支计数的桥梁。 -/
theorem bridge_to_unified3 : Fintype.card ActiveMorphismLayer = 3 ∧ B = 15 :=
  ⟨card_active_layers, B_eq_15⟩

end UFPFormalization.BranchCounting
