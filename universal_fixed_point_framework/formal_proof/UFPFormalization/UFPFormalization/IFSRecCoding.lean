import UFPFormalization.RecCategory
import UFPFormalization.IFSFractal
import Mathlib.Data.Fin.Basic

namespace UFPFormalization

noncomputable section

/-!
# IFS → Σ-Rec 符号编码（阶段 3 子任务 2，2026-08-05）

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
  3. `symbolicCoproductObj`：**coproduct 对象编码**——分量 = 各片
     （`components i = some (slice i)`，i ≥ n 时为 none），整体 = ⨁ᵢ Rᵢ
     （阶段 3"分形 = ⨁ Rᵢ"的对象层构造，自包含定义）。

核心引理：`symbolicStep_fixedPoint_eq_zero`——左移补 0 步进不动点的**必要方向**：
末位为 0（`symbolicStep_fixed_last_zero`）+ 平移链（`symbolicStep_fixed_shift`）
⟹ 不动点必为全零序列（转移矩阵的迹 = #Fix = 1，对应笔记 §4.4 的谱障碍公式
tr(T_f) = #Fix(f) 在符号层的结构实例；充分方向见 `symbolicStep_zero_fixed`）。

诚实边界：
  - 本文件给出**对象级构造**（RecObj / coproduct 编码）与不动点刻画；
  - 态射层（片嵌入 RecHom、符号转移与各片谱的精确关系）与 Weierstrass 谱隙的
    Lean 表述依赖有限维谱积分层（mathlib `ContinuousFunctionalCalculus` 桥接），
    留待阶段 3 子任务 3-4；
  - `NoiseCategory.lean` 的完整 Σ-Rec 范畴（SigmaRecObj/SigmaRecHom/ι_Σ）当前存在
    既有编译错误（缺 `CategoryTheory` import 等，2026-08-05 核实），本文件用自包含的
    `symbolicCoproductObj` 承载构造层；NoiseCategory 编译修复为独立任务。
-/

/-- 最小 coproduct 对象编码（自包含）：分量 i = Option RecObj，i ≥ n 时为 none。
    对齐 NoiseCategory.SigmaRecObj 的 components 结构。 -/
structure CoproductObj where
  /-- 分量：索引 i 处的 RecObj（none = 无对象）。 -/
  components : ℕ → Option RecObj

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

/-- coproduct 对象编码：分量 i = 第 i 片（symbolicSlice i），i ≥ n 时无对象。
    这是"分形 = ⨁ᵢ Rᵢ"（阶段 3）的对象层构造。 -/
def symbolicCoproductObj (n L : ℕ) (hn : 1 ≤ n) (hL : 1 ≤ L) : CoproductObj where
  components := fun i => if h : i < n then some (symbolicSlice n L hn hL ⟨i, h⟩) else none

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

end

end UFPFormalization
