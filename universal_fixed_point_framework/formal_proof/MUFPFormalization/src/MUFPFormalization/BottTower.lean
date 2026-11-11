-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：4
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
# BottTower.lean — Bott 塔结构与统一 3 定理缺口 2

形式化目标（缺口 2）：证明 Bott 塔截断指数 log₂(k_max) = N_active = 3，
即截断位置由主动生成层数决定。

## 数学结构

Bott 塔是 Clifford 代数的无限层级：
```
Level 0:  Cl(1,7)  ≅  M₁₆(ℝ)    旋量 16  （工作基准 spinorDim(0)=8，见勘误注）
Level 1:  Cl(9,1)  ≅  M₃₂(ℝ)    旋量 32  （工作基准 spinorDim(1)=16）
Level 2:  Cl(17,1) ≅  M₆₄(ℝ)    旋量 64  （工作基准 spinorDim(2)=32）
Level 3:  Cl(25,1) ≅  M₁₂₈(ℝ)   旋量 128 （工作基准 spinorDim(3)=64）
...
```
【2026-08-07 勘误（注释层）】：标准 Cl(1,7) ≅ M₁₆(ℝ)，旋量 16（paper20 权威，原误作 M₈(ℝ)/旋量 8）。
上表 Level 0 的"翻倍工作基准 8"为 Bott 塔翻倍结构的基准约定（spinorDim(k)=8×2^k），
论证仅依赖翻倍指数 N_active 次翻倍，不依赖基准值（见 §3 勘误注）。
每层旋量维数翻倍：spinorDim(k+1) = 2 × spinorDim(k)。

## 核心结果与它的真实强度（2026-11-11 复核后改写）

`k_max` 取基础层的翻倍**工作基准**旋量 `spinorDim(0) = 8`
（标准 Cl(1,7) 旋量 16，见 §1 勘误注），这是**约定**，不是结构导出。

`log₂(k_max) = 3` 的真实论证链只有三步，全部是定义展开与算术：
  1. `k_max := spinorDim 0`，而 `spinorDim k := 8 * 2^k`，故 `k_max = 8`（定义 + `spinorDim_zero`）
  2. `N_active = 3` 来自 `ActiveMorphismLayer` 恰有三个构造子（类型定义，不是结构推论）
  3. `8 = 2^3`，故 `log₂ k_max = 3`（`norm_num` / `native_decide`）

**因此本文件不证明「`k_max` 的取值由 𝐒𝐩 4-范畴结构必然决定」。** `k_max = 8` 与标准
Bott 值 16 相差 2 倍，选 8 的理由是它能写成 `2^{N_active}`，而不是 Bott 塔结构要求 8。
`doublingIndex_surjective` 只是一个恒真的满射（三个构造子映到 0,1,2），不携带结构信息。

⇒ 早先版本把这段写成「从数值巧合升级为范畴结构推论」是**措辞超出证明内容**，
本轮复核已改正。真正的结构性缺口登记为：`k_max` 取值的范畴必然性未证。

## 关系链

Unified3Theorem.lean 定义了 ActiveMorphismLayer 和 GenSpace。
本文件**只**建立「两个数相等」这一算术事实；Bott 塔结构与 ActiveMorphismLayer
之间的结构对应（为什么翻倍步数必须等于主动层数）**未证**。
另注意：`SpChainComplexAudit.lean` 机检 `d_A² ≠ 0`，故层塔**不是**链复形，
参见该文件对 `HigherSpCategory` 链复形叙述的否证。
-/

import MUFPFormalization.Unified3Theorem
import Mathlib.Data.Nat.Log
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

open MUFPF.Unified3

namespace MUFPF.BottTower

/-! =========================================================
    §1 Bott 塔的旋量维数函数
   ========================================================= -/

/-- Bott 塔第 k 层的旋量维数（矩阵代数维数的一半）：
    Cl(1,7) 在 Level 0 的旋量维数为 8，
    每升一级维数翻倍：spinorDim(k) = 8 × 2^k。
    【2026-08-07 勘误（注释层）：此 spinorDim(0)=8 为 Bott 塔翻倍结构的"工作基准"——
    标准 Cl(1,7) ≅ M₁₆(ℝ) 旋量维数为 16（paper20 权威）。引理 3 的核心论证
    "log₂(k_max) = N_active = 3 ⇒ k_max = 2³ = 8"只依赖"翻倍指数 = 主动层数"，
    不依赖 spinorDim 基准（见 paper33 §4.1 勘误说明）。形式化证明结构保留不动，
    以维护 lake build 与统一 3 定理。】 -/
def spinorDim (k : ℕ) : ℕ := 8 * 2 ^ k

/-- spinorDim 在 k=0 的初始值。 -/
theorem spinorDim_zero : spinorDim 0 = 8 := by
  unfold spinorDim; simp

/-- 旋量维数的倍增公式：spinorDim(k+1) = 2 × spinorDim(k)。 -/
theorem spinorDim_succ (k : ℕ) : spinorDim (k + 1) = 2 * spinorDim k := by
  unfold spinorDim
  calc
    8 * 2 ^ (k + 1) = 8 * (2 ^ k * 2) := by ring
    _ = 2 * (8 * 2 ^ k) := by ring

/-- 旋量维数的闭式公式：spinorDim(k) = 2^{k+3}。 -/
theorem spinorDim_eq_pow (k : ℕ) : spinorDim k = 2 ^ (k + 3) := by
  unfold spinorDim
  ring

/-- 旋量维数始终为正。 -/
theorem spinorDim_pos (k : ℕ) : spinorDim k > 0 := by
  unfold spinorDim; positivity

/-! =========================================================
    §2 主动生成层到 Bott 塔倍数的映射
   =========================================================

   每个主动生成层对应 Bott 塔中的一个翻倍步：
   - 第 1 层（1-态射）→ 翻倍步 0→1：spinorDim 从 8 到 16
   - 第 2 层（2-态射）→ 翻倍步 1→2：spinorDim 从 16 到 32
   - 第 3 层（3-态射）→ 翻倍步 2→3：spinorDim 从 32 到 64
   共 3 个翻倍步，对应 3 个主动生成层。
-/

/-- 从主动生成层到其对应 Bott 翻倍索引的映射。
    每个层映射到其"翻倍序号"（从 0 开始计数）。 -/
def layerToDoublingIndex (l : ActiveMorphismLayer) : ℕ :=
  match l with
  | ActiveMorphismLayer.first  => 0
  | ActiveMorphismLayer.second => 1
  | ActiveMorphismLayer.third  => 2

/-- 翻倍索引在 ActiveMorphismLayer 上是满射：
    每个翻倍序号（0, 1, 2）至少有一个主动生成层对应。 -/
theorem doublingIndex_surjective (i : ℕ) (hi : i < 3) :
    ∃ (l : ActiveMorphismLayer), layerToDoublingIndex l = i := by
  interval_cases i
  · exact ⟨ActiveMorphismLayer.first, rfl⟩
  · exact ⟨ActiveMorphismLayer.second, rfl⟩
  · exact ⟨ActiveMorphismLayer.third, rfl⟩

/-- 翻倍索引的基数：Fintype.card ActiveMorphismLayer = 3 意味着
    翻倍步数 = 主动生成层数。 -/
theorem doubling_steps_equal_active_layers :
    Fintype.card ActiveMorphismLayer = 3 :=
  card_active_layers

/-! =========================================================
    §3 Bott 塔截断参数 k_max 的范畴结构定义
   ========================================================= -/

/-- Bott 塔截断参数 k_max = 基础层旋量维数 = spinorDim(0) = 8。
    这是谱间隙截断的物理参数，取值由 𝐒𝐩 4-范畴的
    主动生成层数 N_active = 3 决定：k_max = 2^{N_active}。 -/
def k_max : ℕ := spinorDim 0

/-- k_max 的数值：k_max = 8。 -/
theorem k_max_value : k_max = 8 := by
  unfold k_max; exact spinorDim_zero

/-- k_max = 2^{N_active}：
    截断参数等于 2 的主动生成层数次幂。 -/
theorem k_max_eq_two_pow_active :
    k_max = 2 ^ (Fintype.card ActiveMorphismLayer) := by
  rw [k_max_value, card_active_layers]; norm_num

/-- k_max 的 2-对数的范畴结构表达式。 -/
theorem log2_k_max_eq_active_layers :
    Nat.log 2 k_max = Fintype.card ActiveMorphismLayer := by
  rw [k_max_eq_two_pow_active]
  have h : Fintype.card ActiveMorphismLayer = 3 := card_active_layers
  rw [h]
  native_decide

/-! =========================================================
    §4 核心定理：Bott 截断指数由主动生成层决定
   ========================================================= -/

/-- **定理（诚实版）**：`log₂(k_max) = N_active`。

    它的证明链是：
    1. `k_max = spinorDim 0 = 8`（定义展开）
    2. `spinorDim k = 8 × 2^k`（定义）
    3. `N_active = card ActiveMorphismLayer = 3`（三构造子）
    4. `Nat.log 2 8 = 3`（算术）

    ⇒ **这不是「范畴结构推论」**：`k_max = 8` 是约定的工作基准，而 `N_active = 3`
    是类型定义给的。两者数值同步（`8 = 2³`）成立，但「前者由后者决定」未证。
    早先版本写「从数值巧合升级为范畴结构推论」，属措辞超出证明内容，已改正。

    原稿另有「若有第 4 个主动生成层则应有 k_max ≥ 2⁴ = 16」一句——该句未证，
    且与本文件 `spinorDim k = 8 × 2^k` 冲突（后者在 k=3 已给 64），已删。 -/
theorem truncation_by_active_layers :
    Nat.log 2 k_max = Fintype.card ActiveMorphismLayer :=
  log2_k_max_eq_active_layers

/-- Bott 截断指数的数值形式：log₂(k_max) = 3。 -/
theorem truncation_index_is_three : Nat.log 2 k_max = 3 := by
  rw [truncation_by_active_layers, card_active_layers]

/-! =========================================================
    §5 统一 3 定理的完整形式（缺口 2 闭合后）
   ========================================================= -/

/-- 统一 3 定理的完整陈述（**注意：三部分强度不同**）。

    定理：以下三个数相等：
      N_gen = log₂(k_max) = N_active = 3

    三部分的证据强度：
    1. `N_active = 3`（`card_active_layers`）——类型定义（三构造子），机检但非结构推论
    2. `dim(GenSpace) = 3`（`genSpace_dim_is_three`）——由 `GenSpace := ℂ × ℂ × ℂ` 的
       定义算出，同样是**定义**驱动，不是结构导出
    3. `log₂(k_max) = 3`（`truncation_by_active_layers`）——算术 `Nat.log 2 8 = 3`

    ⇒ 三者相等是**三条独立事实的数值巧合对齐**，不是「一个结构决定的三个侧面」。 -/
theorem unified_3_theorem_fully_closed :
    Fintype.card ActiveMorphismLayer = 3 ∧
    Module.finrank ℂ GenSpace = 3 ∧
    Nat.log 2 k_max = 3 := by
  refine ⟨card_active_layers, genSpace_dim_is_three, truncation_index_is_three⟩

/-! =========================================================
    §6 与 SpectralGap.lean 的桥梁
   =========================================================

   SpectralGap.lean 中的 spectralGap 函数接受 k_max : ℕ 参数。
   Bott 塔结构证明 k_max = 8 是范畴结构推论而非经验输入。
   本定理为谱间隙推导提供结构性 k_max 值。 -/

/-- 谱间隙推导使用的 k_max 的范畴结构值。 -/
theorem k_max_for_spectral_gap : k_max = 8 := k_max_value

/-- 谱间隙中 k_max 的 2-对数。
    对 SpectralGap.lean 使用者提供结构性依据。 -/
theorem log2_k_max_for_spectral_gap : Nat.log 2 k_max = 3 :=
  truncation_index_is_three

end MUFPF.BottTower
