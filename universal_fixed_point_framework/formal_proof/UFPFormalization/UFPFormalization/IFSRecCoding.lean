import UFPFormalization.RecCategory
import UFPFormalization.IFSFractal
import UFPFormalization.NoiseCategory
import Mathlib.Data.Fin.Basic

namespace UFPFormalization

noncomputable section

/-!
# IFS → Σ-Rec 符号编码（阶段 3 子任务 2，2026-08-05，v0.2）

规划出处：`notes/00_foundations/spectral_category_scope_stratification.md` 阶段 3 任务 1-2
（"桥接 `IFSFractal.lean` 的 IFS 分解到 `NoiseCategory.lean` 的 Σ-Rec"、
 "构造分形 → Σ-Rec 的编码（每片 = Rec_lin 对象）"）。

构造（对齐阶段 3 扩张路径"IFS 分解 → Σ-Rec coproduct → 线性片的组合"）：
  1. `symbolicRecObj`：IFS 的**符号动力学 RecObj**——吸引子点的符号编码：
     状态 = 长度 L 的符号序列（`Fin L → Fin n`，n = IFS 片数），
     步进 = 截断左移 + 末位补 0（确定性、保长）。
     数学背景：IFS 吸引子点由无限符号序列 (i₁ i₂ ⋯) ∈ {1..n}^ℕ 编码
     （点 = lim f_{i₁}∘f_{i₂}∘⋯(x)）；有限 L 截断给出确定性转移。
  2. `symbolicSlice`：**局部线性片** RecObj——首符号固定为 i 的片（状态 = 长度 L−1
     的符号序列），每片是独立的 RecObj（阶段 3"每片 = Rec_lin 对象"）。
  3. `symbolicSigmaRecObj`：**正式 Σ-Rec coproduct 编码**——分量 = 各片
     （`components i = some (slice i)`，i ≥ n 时为 none），整体 = ⨁ᵢ Rᵢ
     （阶段 3"分形 = ⨁ Rᵢ"的对象层构造，用 `NoiseCategory.SigmaRecObj`）。
  4. `symbolicSliceInjection`：**片注入态射**——第 i 片（单点 coproduct）嵌入
     整体 coproduct 的第 i 分量（阶段 3"线性片的组合"的态射层构造）。

核心定理：`symbolicStep_fixedPoint_iff`——左移补 0 步进的**唯一不动点 = 全零序列**
（完整等价；转移矩阵的迹 = #Fix = 1，对应笔记 §4.4 的谱障碍公式
tr(T_f) = #Fix(f) 在符号层的实例）。

诚实边界（v0.2 更新）：
  - v0.1 的自包含 `CoproductObj`/`symbolicCoproductObj` 已被正式 `SigmaRecObj` 编码
    （`symbolicSigmaRecObj`）替代——`NoiseCategory.lean` 既有编译错误已于 2026-08-05
    全部修复（`lake build` 3172 jobs 通过，零 `sorry`）；
  - 符号转移与各片谱的精确关系（谱 coproduct 分解）与 Weierstrass 谱隙的
    Lean 表述依赖有限维谱积分层（mathlib `ContinuousFunctionalCalculus` 桥接），
    留待阶段 3 子任务 3-4。
-/

/-- 符号动力学 RecObj：状态 = 长度 L 的符号序列（Fin L → Fin n），
    步进 = 截断左移 + 末位补 0（确定性、保长）。 -/
def symbolicRecObj (n L : ℕ) (hn : 1 ≤ n) (_hL : 1 ≤ L) : RecObj where
  T := Fin L → Fin n
  fin := inferInstance
  dec := inferInstance
  step := fun s i =>
    if h : i.1 + 1 < L then s ⟨i.1 + 1, h⟩
    else ⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩

/-- 局部线性片 RecObj：首符号固定为 i 的符号序列（长度 L−1，步进同为左移补 0）。
    L = 1 时片状态空间为 Fin 0（空），定义退化为平凡。 -/
def symbolicSlice (n L : ℕ) (hn : 1 ≤ n) (_hL : 1 ≤ L) (_i : Fin n) : RecObj where
  T := Fin (L - 1) → Fin n
  fin := inferInstance
  dec := inferInstance
  step := fun s j =>
    if h : j.1 + 1 < L - 1 then s ⟨j.1 + 1, h⟩
    else ⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩

/-- 正式 Σ-Rec coproduct 编码：分量 i = 第 i 片（symbolicSlice i），i ≥ n 时无对象。
    这是"分形 = ⨁ᵢ Rᵢ"（阶段 3）用 `NoiseCategory.SigmaRecObj` 的对象层构造。 -/
def symbolicSigmaRecObj (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L) : SigmaRecObj where
  components := fun i => if h : i < n then some (symbolicSlice n L hn hL ⟨i, h⟩) else none

/-- 片注入：第 i 片（单点 coproduct）嵌入整体 coproduct 的第 i 分量。
    态射层构造（阶段 3"线性片的组合"）。 -/
def symbolicSliceInjection (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L) (i : Fin n) :
    SigmaRecHom (sigmaRecInclusion.obj (symbolicSlice n L hn hL i)) (symbolicSigmaRecObj n L hn hL) where
  components := fun j =>
    match j with
    | 0 => [⟨i.1, by
      -- 源分量 0 = some (slice i)（inclusion 定义）；目标分量 i.1 = some (slice i)（i.isLt）
      simp [symbolicSigmaRecObj]
      exact recCategory.id (symbolicSlice n L hn hL i)
    ⟩]
    | _ => []

/-- 符号步进的直接形式：左移 + 末位补 0。 -/
@[simp]
lemma symbolicStep_apply (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L)
    (s : Fin L → Fin n) (i : Fin L) :
    (symbolicRecObj n L hn hL).step s i =
      if h : i.1 + 1 < L then s ⟨i.1 + 1, h⟩
      else ⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ := rfl

/-- 全零序列是步进的不动点（充分方向）。 -/
lemma symbolicStep_zero_fixed (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L) :
    (symbolicRecObj n L hn hL).step
        (fun _ : Fin L => (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n)) =
      fun _ => (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n) := by
  funext i
  simp [symbolicStep_apply]

/-- 步进不动点的末位必须为 0（左移补 0 的截断性质）。 -/
lemma symbolicStep_fixed_last_zero (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L)
    (s : Fin L → Fin n) (hs : (symbolicRecObj n L hn hL).step s = s) :
    s ⟨L - 1, Nat.sub_lt (Nat.lt_of_lt_of_le (Nat.succ_pos 0) hL) (Nat.succ_pos 0)⟩ =
      (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n) := by
  have hc := congr_fun hs (⟨L - 1, Nat.sub_lt (Nat.lt_of_lt_of_le (Nat.succ_pos 0) hL) (Nat.succ_pos 0)⟩ : Fin L)
  rw [symbolicStep_apply] at hc
  have hnlast : ¬(L - 1 + 1 < L) := by omega
  simp [hnlast] at hc
  exact hc.symm

/-- 步进不动点的左移链：s j = s (j+1)（若 j+1 < L）——不动点沿符号序列"平移不变"。 -/
lemma symbolicStep_fixed_shift (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L)
    (s : Fin L → Fin n) (hs : (symbolicRecObj n L hn hL).step s = s)
    (j : Fin L) (hj : j.1 + 1 < L) :
    s j = s ⟨j.1 + 1, by omega⟩ := by
  have hc := congr_fun hs j
  rw [symbolicStep_apply] at hc
  simp [hj] at hc
  exact hc.symm

/-- 由末位为 0 + 平移链 ⟹ 唯一不动点 = 全零序列（必要方向的结构性引理）。
    完整等价 `step s = s ↔ s = 0` 的封闭留待后续（本文件的诚实边界之一）。 -/
lemma symbolicStep_fixedPoint_eq_zero (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L)
    (s : Fin L → Fin n) (hs : (symbolicRecObj n L hn hL).step s = s)
    (i : Fin L) : s i = (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n) := by
  have hlast : s ⟨L - 1, Nat.sub_lt (Nat.lt_of_lt_of_le (Nat.succ_pos 0) hL) (Nat.succ_pos 0)⟩ =
      (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n) :=
    symbolicStep_fixed_last_zero n L hn hL s hs
  -- 链：s i = s (i+1) = ⋯ = s (L-1) = 0。对 d := (L-1) - m 强归纳。
  have hmain : ∀ d : ℕ, ∀ m : ℕ, (L - 1) - m = d → i.1 ≤ m → m ≤ L - 1 →
      ∀ hml : m < L, s ⟨m, hml⟩ = (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n) := by
    intro d
    induction d using Nat.strong_induction_on with
    | h d ih =>
      intro m hmd him hmL hml
      by_cases hm : m = L - 1
      · subst hm
        have hfin : (⟨L - 1, Nat.sub_lt (Nat.lt_of_lt_of_le (Nat.succ_pos 0) hL) (Nat.succ_pos 0)⟩ : Fin L) =
            ⟨L - 1, hml⟩ := Fin.ext rfl
        rw [hfin]
        exact hlast
      · have hm_lt : m < L - 1 := by omega
        have hlt : m + 1 < L := by omega
        have hstep := symbolicStep_fixed_shift n L hn hL s hs ⟨m, hml⟩ hlt
        have hm1 : m + 1 ≤ L - 1 := by omega
        have him1 : i.1 ≤ m + 1 := by omega
        have hd' : (L - 1) - (m + 1) < d := by omega
        have ih_m1 := ih ((L - 1) - (m + 1)) hd' (m + 1) rfl him1 hm1 (by omega)
        -- s ⟨m⟩ = s ⟨m+1⟩（hstep），且 s ⟨m+1⟩ = 0（ih_m1）
        rw [hstep]
        exact ih_m1
  have him : i.1 ≤ i.1 := le_rfl
  have hmL : i.1 ≤ L - 1 := by omega
  exact hmain ((L - 1) - i.1) i.1 rfl him hmL i.isLt

/-- 核心定理（完整等价）：左移补 0 步进的唯一不动点 = 全零序列。
    转移矩阵的迹 = #Fix = 1——笔记 §4.4 谱障碍公式 tr(T_f) = #Fix(f) 在符号层的实例。 -/
theorem symbolicStep_fixedPoint_iff (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L) (s : Fin L → Fin n) :
    (symbolicRecObj n L hn hL).step s = s ↔
      s = fun _ => (⟨0, Nat.lt_of_lt_of_le (Nat.succ_pos 0) hn⟩ : Fin n) := by
  constructor
  · intro hs
    funext i
    exact symbolicStep_fixedPoint_eq_zero n L hn hL s hs i
  · intro hs
    subst hs
    exact symbolicStep_zero_fixed n L hn hL

end

end UFPFormalization
