import Mathlib.Tactic
import MUFPFormalization.PeriodicOrbitCount
import MUFPFormalization.OrbitFullLock

/-!
# 静默模型定理：全静默 ⟹ 恒等（orbitCount = 15）

对应骨架 §5b 开放项①闭合（2026-10-23）与恒等性论证论据 1：
静默（失去表达窗口，幅值判据逐窗口）⟹ 冻结为不动点 ⟹ 全静默 ⟹ 全不动点
⟹ orbitCount = 15 ⟺ 恒等（OrbitFullLock (⇐) 实例化）。

模型 = window_silence_granularity.py 的分层静默模型 Lean 化：
- 15 组合窗口 = Fin 15（非空子集 {1,2,3,4} 字典序编号：层1 {0..3}、层2 {4..9}、
  层3 {10..13}、层4 {14}，对应 C(4,r) = 4+6+4+1）；
- `layeredStep`：活跃窗口层内循环后继（层 r 成员内 mod 循环，单点层不动）；
- `silenceRec15_layered S`：静默窗口（x ∈ S，表达归零）⟹ step x = x。

定理：
- `silenceRec15_layered_fixed_of_mem`：静默 ⟹ 不动（定义层 if_pos）；
- `silenceRec15_layered_all_silent_fixed`：全静默（S = univ）⟹ 全不动；
- `silenceRec15_layered_all_silent_orbitCount_eq_15`：全静默 ⟹ orbitCount = 15。

诚实边界：活跃窗口层内循环与数值脚本一致（"无静默 ⟹ orbitCount = 4" 的
Lean 证明留后续，数值已给）；层划分 = 字典序编号约定（组合语义见骨架 C4/L3）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.PeriodicOrbitCount

open MUFPF
open MUFPF.EccentricOrbit

/-- 层 1：4 个单元素窗口 {1},{2},{3},{4}（编号 0..3；显式 insert 链便于
    simp/rcases 展开，避免 ofList 字面量）。 -/
def layer1 : Finset (Fin 15) :=
  insert 0 (insert 1 (insert 2 (insert 3 (∅ : Finset (Fin 15)))))

/-- 层 2：6 个二元素窗口（编号 4..9）。 -/
def layer2 : Finset (Fin 15) :=
  insert 4 (insert 5 (insert 6
    (insert 7 (insert 8 (insert 9 (∅ : Finset (Fin 15)))))))

/-- 层 3：4 个三元素窗口（编号 10..13）。 -/
def layer3 : Finset (Fin 15) :=
  insert 10 (insert 11 (insert 12 (insert 13 (∅ : Finset (Fin 15)))))

/-- 层 4：1 个四元素窗口（编号 14）。 -/
def layer4 : Finset (Fin 15) := insert 14 (∅ : Finset (Fin 15))

/-- 层内循环后继（活跃窗口）：层 1 {0..3} 内 0→1→2→3→0；层 2 {4..9} 内
    4→…→9→4；层 3 {10..13} 内 10→…→13→10；层 4 {14} 不动。 -/
def layeredStep (x : Fin 15) : Fin 15 :=
  if x ∈ layer1 then (if x = 3 then 0 else x + 1)
  else if x ∈ layer2 then (if x = 9 then 4 else x + 1)
  else if x ∈ layer3 then (if x = 13 then 10 else x + 1)
  else 14

/-- 静默模型的 step 函数（域干净 Fin 15，避免 RecObj 投影不透明）：
    S = 已静默（表达归零）窗口集合；静默窗口不动，活跃窗口层内循环。 -/
def silentStep (S : Finset (Fin 15)) (x : Fin 15) : Fin 15 :=
  if x ∈ S then x else layeredStep x

/-- 静默模型 RecObj（step 字段 = silentStep S 的包装；抽象 S 时投影不归约，
    故外部证明一律操作 silentStep S，经 silenceRec15_layered_step 桥接）。 -/
def silenceRec15_layered (S : Finset (Fin 15)) : RecObj where
  T := Fin 15
  fin := inferInstance
  dec := inferInstance
  step := silentStep S

/-- 投影桥：RecObj.step = silentStep（simp 层归约）。 -/
lemma silenceRec15_layered_step (S : Finset (Fin 15)) (x : Fin 15) :
    (silenceRec15_layered S).step x = silentStep S x := by
  simp [silenceRec15_layered]

/-- 层内后继锚（数值验证，与 window_silence_granularity.py 层循环一致）。 -/
example : layeredStep (0 : Fin 15) = 1 := by native_decide
example : layeredStep (3 : Fin 15) = 0 := by native_decide
example : layeredStep (4 : Fin 15) = 5 := by native_decide
example : layeredStep (9 : Fin 15) = 4 := by native_decide
example : layeredStep (13 : Fin 15) = 10 := by native_decide
example : layeredStep (14 : Fin 15) = 14 := by native_decide

/-- 静默 ⟹ 不动（定义层）：窗口在静默集合中则 step 恒等。 -/
theorem silenceRec15_layered_fixed_of_mem (S : Finset (Fin 15)) {x : Fin 15}
    (hx : x ∈ S) : (silenceRec15_layered S).step x = x := by
  simp [silenceRec15_layered, silentStep, hx]

/-- 全静默 ⟹ 全不动：所有窗口表达归零 ⟹ 每个窗口都是不动点。 -/
theorem silenceRec15_layered_all_silent_fixed (S : Finset (Fin 15))
    (hS : S = Finset.univ) : ∀ x : Fin 15, (silenceRec15_layered S).step x = x := by
  intro x
  exact silenceRec15_layered_fixed_of_mem S (by simp [hS])

/-- 全静默 ⟹ orbitCount = 15（全不动 ⟹ =card，OrbitFullLock (⇐) 实例化；
    card (Fin 15) = 15）。即"全静默 ⟹ 恒等"的静默模型定理。 -/
theorem silenceRec15_layered_all_silent_orbitCount_eq_15 (S : Finset (Fin 15))
    (hS : S = Finset.univ) : orbitCount (silenceRec15_layered S) = 15 := by
  classical
  have hfix : ∀ x : Fin 15, (silenceRec15_layered S).step x = x :=
    silenceRec15_layered_all_silent_fixed S hS
  have hc : orbitCount (silenceRec15_layered S) = Fintype.card (Fin 15) :=
    orbitCount_eq_card_of_all_fixed (silenceRec15_layered S) hfix
  rw [hc]
  simp

/-! ## 无静默 ⟹ orbitCount = 4（层轨道基数，2026-10-24）

分层模型 `silenceRec15_layered ∅`（无静默，全部窗口活跃层内循环）的轨道数 = 4
（每谱层一条轨道）。证明路径：层内后继保持层（layerOf 不变）⟹ 同类同层（inj）；
层内连通（每点可达层代表）⟹ 每层一条轨道（surj）；商 ≃ Fin 4。 -/

/-- 层号函数：层 1 → 0、层 2 → 1、层 3 → 2、层 4 → 3。 -/
def layerOf (x : Fin 15) : Fin 4 :=
  if x ∈ layer1 then 0
  else if x ∈ layer2 then 1
  else if x ∈ layer3 then 2
  else 3

/-- 层代表：层 1 → 0、层 2 → 4、层 3 → 10、层 4 → 14。 -/
def rep (i : Fin 4) : Fin 15 :=
  if i = 0 then 0
  else if i = 1 then 4
  else if i = 2 then 10
  else 14

/-- 空静默时 step = layeredStep（∅ 无成员，if 归约）。 -/
lemma step_eq_layeredStep (x : Fin 15) :
    (silenceRec15_layered ∅).step x = layeredStep x := by
  simp [silenceRec15_layered, silentStep]

/-- 层内后继保持层号：layeredStep 不跨层。 -/
lemma layerOf_step (x : Fin 15) : layerOf (layeredStep x) = layerOf x := by
  fin_cases x <;> native_decide

/-- 迭代保持层号。 -/
lemma layerOf_iterate (n : ℕ) (x : Fin 15) : layerOf (layeredStep^[n] x) = layerOf x := by
  induction n generalizing x with
  | zero => rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply]
      exact (ih (layeredStep x)).trans (layerOf_step x)

/-- 空静默时 step 迭代 = layeredStep 迭代（unfold 后逐点函数相等诱导迭代相等）。 -/
lemma iterate_step_eq_iterate_layered (n : ℕ) (x : Fin 15) :
    (silenceRec15_layered ∅).step^[n] x = layeredStep^[n] x := by
  unfold silenceRec15_layered
  let f : Fin 15 → Fin 15 := fun y =>
    if y ∈ (∅ : Finset (Fin 15)) then y else layeredStep y
  change f^[n] x = layeredStep^[n] x
  induction n generalizing x with
  | zero => rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply, Function.iterate_succ_apply]
      have hfx : f x = layeredStep x := by simp [f]
      rw [hfx]
      exact ih (layeredStep x)

/-- 层 1 窗口周期（层内循环 4 步回自身）。 -/
lemma layer1_periodic (x : Fin 15) (hx : x ∈ layer1) :
    periodicPoint (silenceRec15_layered ∅) x := by
  refine ⟨4, by norm_num, ?_⟩
  rw [layer1] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (0 : Fin 15) = 0
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (1 : Fin 15) = 1
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (2 : Fin 15) = 2
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (3 : Fin 15) = 3
    decide

/-- 层 2 窗口周期（层内循环 6 步回自身）。 -/
lemma layer2_periodic (x : Fin 15) (hx : x ∈ layer2) :
    periodicPoint (silenceRec15_layered ∅) x := by
  refine ⟨6, by norm_num, ?_⟩
  rw [layer2] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[6] (4 : Fin 15) = 4
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[6] (5 : Fin 15) = 5
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[6] (6 : Fin 15) = 6
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[6] (7 : Fin 15) = 7
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[6] (8 : Fin 15) = 8
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[6] (9 : Fin 15) = 9
    decide

/-- 层 3 窗口周期（层内循环 4 步回自身）。 -/
lemma layer3_periodic (x : Fin 15) (hx : x ∈ layer3) :
    periodicPoint (silenceRec15_layered ∅) x := by
  refine ⟨4, by norm_num, ?_⟩
  rw [layer3] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (10 : Fin 15) = 10
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (11 : Fin 15) = 11
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (12 : Fin 15) = 12
    decide
  · rw [iterate_step_eq_iterate_layered]
    change layeredStep^[4] (13 : Fin 15) = 13
    decide

/-- 层 4 窗口周期（单点不动，周期 1）。 -/
lemma layer4_periodic (x : Fin 15) (hx : x ∈ layer4) :
    periodicPoint (silenceRec15_layered ∅) x := by
  refine ⟨1, by norm_num, ?_⟩
  rw [layer4] at hx
  simp at hx
  rcases hx with rfl
  rw [iterate_step_eq_iterate_layered]
  change layeredStep^[1] (14 : Fin 15) = 14
  decide

/-- 空静默模型全点周期（15 个窗口都在层内循环上）。 -/
lemma layered_all_periodic (x : Fin 15) :
    periodicPoint (silenceRec15_layered ∅) x := by
  by_cases h1 : x ∈ layer1
  · exact layer1_periodic x h1
  · by_cases h2 : x ∈ layer2
    · exact layer2_periodic x h2
    · by_cases h3 : x ∈ layer3
      · exact layer3_periodic x h3
      · exact layer4_periodic x (by
          fin_cases x <;> simp [layer1, layer2, layer3, layer4] at h1 h2 h3 ⊢)

/-- 周期点经 n 步到代表：subtype 提升的 hpx 会引入自由变量使 native_decide 无法编译，
    先 change 归约提升、再经 iterate 引理换成 layeredStep 判定。 -/
lemma step_iterate_to_rep (n : ℕ) (x r : Fin 15)
    (hpx : periodicPoint (silenceRec15_layered ∅) x)
    (h : layeredStep^[n] x = r) :
    periodOrbitRel (silenceRec15_layered ∅) ⟨x, hpx⟩ ⟨r, layered_all_periodic r⟩ := by
  refine ⟨n, ?_⟩
  change (silenceRec15_layered ∅).step^[n] x = r
  rw [iterate_step_eq_iterate_layered]
  exact h

/-- 前向可达保持层号：step^[n] x = y ⟹ 同层。 -/
lemma rel_same_layer_of_step_eq (n : ℕ) (x y : Fin 15)
    (h : (silenceRec15_layered ∅).step^[n] x = y) : layerOf x = layerOf y := by
  have h1 : layerOf ((silenceRec15_layered ∅).step^[n] x) = layerOf x := by
    rw [iterate_step_eq_iterate_layered n x]
    exact layerOf_iterate n x
  rw [← h1, h]

/-- 周期点同类 ⟹ 同层（轨道不跨层）。 -/
lemma rel_same_layer (x y : Fin 15)
    (h : periodOrbitRel (silenceRec15_layered ∅) ⟨x, layered_all_periodic x⟩
      ⟨y, layered_all_periodic y⟩) :
    layerOf x = layerOf y := by
  rcases h with ⟨n, hn⟩
  exact rel_same_layer_of_step_eq n x y hn

/-- 层 1 每点前向可达代表 0（0→1→2→3→0 循环）。 -/
lemma layer1_to_rep0 (x : Fin 15) (hx : x ∈ layer1)
    (hpx : periodicPoint (silenceRec15_layered ∅) x) :
    periodOrbitRel (silenceRec15_layered ∅) ⟨x, hpx⟩ ⟨(0 : Fin 15), layered_all_periodic 0⟩ := by
  rw [layer1] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl
  · exact step_iterate_to_rep 4 0 0 hpx (by native_decide)
  · exact step_iterate_to_rep 3 1 0 hpx (by native_decide)
  · exact step_iterate_to_rep 2 2 0 hpx (by native_decide)
  · exact step_iterate_to_rep 1 3 0 hpx (by native_decide)

/-- 层 2 每点前向可达代表 4（4→5→6→7→8→9→4 循环）。 -/
lemma layer2_to_rep1 (x : Fin 15) (hx : x ∈ layer2)
    (hpx : periodicPoint (silenceRec15_layered ∅) x) :
    periodOrbitRel (silenceRec15_layered ∅) ⟨x, hpx⟩ ⟨(4 : Fin 15), layered_all_periodic 4⟩ := by
  rw [layer2] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl
  · exact step_iterate_to_rep 6 4 4 hpx (by native_decide)
  · exact step_iterate_to_rep 5 5 4 hpx (by native_decide)
  · exact step_iterate_to_rep 4 6 4 hpx (by native_decide)
  · exact step_iterate_to_rep 3 7 4 hpx (by native_decide)
  · exact step_iterate_to_rep 2 8 4 hpx (by native_decide)
  · exact step_iterate_to_rep 1 9 4 hpx (by native_decide)

/-- 层 3 每点前向可达代表 10（10→11→12→13→10 循环）。 -/
lemma layer3_to_rep2 (x : Fin 15) (hx : x ∈ layer3)
    (hpx : periodicPoint (silenceRec15_layered ∅) x) :
    periodOrbitRel (silenceRec15_layered ∅) ⟨x, hpx⟩ ⟨(10 : Fin 15), layered_all_periodic 10⟩ := by
  rw [layer3] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl
  · exact step_iterate_to_rep 4 10 10 hpx (by native_decide)
  · exact step_iterate_to_rep 3 11 10 hpx (by native_decide)
  · exact step_iterate_to_rep 2 12 10 hpx (by native_decide)
  · exact step_iterate_to_rep 1 13 10 hpx (by native_decide)

/-- 层 4 每点前向可达代表 14（单点）。 -/
lemma layer4_to_rep3 (x : Fin 15) (hx : x ∈ layer4)
    (hpx : periodicPoint (silenceRec15_layered ∅) x) :
    periodOrbitRel (silenceRec15_layered ∅) ⟨x, hpx⟩ ⟨(14 : Fin 15), layered_all_periodic 14⟩ := by
  rw [layer4] at hx
  simp at hx
  rcases hx with rfl
  refine ⟨0, rfl⟩

/-- 商代表映射：Fin 4 → 商（每层一条轨道的代表类）。 -/
noncomputable def repQ (i : Fin 4) : Quotient (periodOrbitSetoid (silenceRec15_layered ∅)) :=
  Quotient.mk (periodOrbitSetoid (silenceRec15_layered ∅)) ⟨rep i, layered_all_periodic (rep i)⟩

/-- 商代表单射：不同层代表不同类（轨道不跨层 ⟹ 类不同）。 -/
lemma repQ_injective : Function.Injective
    (repQ : Fin 4 → Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) := by
  intro i j hij
  have hrel : periodOrbitRel (silenceRec15_layered ∅)
      ⟨rep i, layered_all_periodic (rep i)⟩ ⟨rep j, layered_all_periodic (rep j)⟩ :=
    Quotient.exact hij
  have hl : layerOf (rep i) = layerOf (rep j) := rel_same_layer (rep i) (rep j) hrel
  fin_cases i <;> fin_cases j <;> simp [rep, layerOf, layer1, layer2, layer3] at hl ⊢

/-- 商代表满射：每点在某层 ⟹ 可达该层代表（层内连通）。 -/
lemma repQ_surjective : Function.Surjective
    (repQ : Fin 4 → Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) := by
  intro q
  refine Quotient.inductionOn q ?_
  intro ⟨x, hpx⟩
  by_cases h1 : x ∈ layer1
  · refine ⟨0, ?_⟩
    exact (Quotient.sound (layer1_to_rep0 x h1 hpx)).symm
  · by_cases h2 : x ∈ layer2
    · refine ⟨1, ?_⟩
      exact (Quotient.sound (layer2_to_rep1 x h2 hpx)).symm
    · by_cases h3 : x ∈ layer3
      · refine ⟨2, ?_⟩
        exact (Quotient.sound (layer3_to_rep2 x h3 hpx)).symm
      · refine ⟨3, ?_⟩
        exact (Quotient.sound (layer4_to_rep3 x (by
          fin_cases x
          · exfalso; exact h1 (by decide)
          · exfalso; exact h1 (by decide)
          · exfalso; exact h1 (by decide)
          · exfalso; exact h1 (by decide)
          · exfalso; exact h2 (by decide)
          · exfalso; exact h2 (by decide)
          · exfalso; exact h2 (by decide)
          · exfalso; exact h2 (by decide)
          · exfalso; exact h2 (by decide)
          · exfalso; exact h2 (by decide)
          · exfalso; exact h3 (by decide)
          · exfalso; exact h3 (by decide)
          · exfalso; exact h3 (by decide)
          · exfalso; exact h3 (by decide)
          · decide ) hpx)).symm

/-- 无静默 ⟹ orbitCount = 4（层轨道基数：商 ≃ Fin 4，4 层各一条轨道）。 -/
theorem silenceRec15_layered_empty_orbitCount_eq_4 :
    orbitCount (silenceRec15_layered ∅) = 4 := by
  classical
  have hsurj : Function.Surjective
      (repQ : Fin 4 → Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) := repQ_surjective
  have hinj : Function.Injective
      (repQ : Fin 4 → Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) := repQ_injective
  have hle4 : Fintype.card (Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) ≤ 4 := by
    simpa using Fintype.card_le_of_surjective
      (repQ : Fin 4 → Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) hsurj
  have hge4 : 4 ≤ Fintype.card (Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) := by
    simpa using Fintype.card_le_of_injective
      (repQ : Fin 4 → Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) hinj
  have hcard : Fintype.card (Quotient (periodOrbitSetoid (silenceRec15_layered ∅))) = 4 :=
    le_antisymm hle4 hge4
  rw [orbitCount]
  exact hcard

/-! ## 次第闭合全程动力学：orbitCount(S) = card S + fullActiveCount(S)

候选 D 严格化点③ 可检验形式的 Lean 化（2026-10-24）。数值先证伪
（scripts/silence_orbitcount_formula.py，穷举 2^15 子集）：v1 公式
"orbitCount = card S + 未全静默层数" 被证伪（部分静默层活跃窗预周期化——
沿层循环被静默窗吸收，静默首窗增量 0）；修正公式
**orbitCount(S) = card S + L_full_active(S)**，L_full_active = 完全活跃层数
（layer ∩ S = ∅，循环轨道未被打断）。每层贡献 = card(层∩S) + [层∩S=∅]，
层静默净增量 = card(层)−1。

证明路径：
- 周期点刻画：x 周期 ⟺ x ∈ S（静默不动）∨ x ∈ 完全活跃层（层内循环）；
  部分静默层活跃窗预周期（被静默窗吸收，非周期——核心引理
  not_periodic_of_reaches_fixed + 各层实例化）；
- 轨道 = 静默窗单点类 ⊎ 完全活跃层循环类 ⟹ 商 ≃ (S ⊎ 完全活跃层)。
-/

/-- 层函数：层号 r → 层窗口集（与 layerOf 对应）。 -/
def layer (r : Fin 4) : Finset (Fin 15) :=
  if r = 0 then layer1
  else if r = 1 then layer2
  else if r = 2 then layer3
  else layer4

/-- 完全活跃层数：layer ∩ S = ∅（层内循环轨道未被打断）的层数。
    与 Fin 4 filter 版等价（数值验证 2^15 零违例）；if 版便于 card 计算。 -/
def fullActiveCount (S : Finset (Fin 15)) : ℕ :=
  (if layer1 ∩ S = ∅ then 1 else 0) + (if layer2 ∩ S = ∅ then 1 else 0) +
    (if layer3 ∩ S = ∅ then 1 else 0) + (if layer4 ∩ S = ∅ then 1 else 0)

/-- periodicPoint 的 silentStep 展开：周期 ⟺ 存在 p>0 使 silentStep 迭代回归。 -/
lemma periodicPoint_step_iterate (S : Finset (Fin 15)) {x : Fin 15}
    (hper : periodicPoint (silenceRec15_layered S) x) :
    ∃ p : ℕ, 0 < p ∧ (silentStep S)^[p] x = x := by
  rcases hper with ⟨p, hp, hpp⟩
  refine ⟨p, hp, ?_⟩
  simpa [silenceRec15_layered, silentStep] using hpp

/-- 吸收非周期引理：轨道经 n 步到达不动点 m（m ≠ x），且中途不归 x ⟹ x 非周期。
    部分静默层活跃窗的预周期化即此引理实例化。 -/
lemma not_periodic_of_reaches_fixed (S : Finset (Fin 15)) {x m : Fin 15} (n : ℕ)
    (hreach : (silentStep S)^[n] x = m)
    (hmfix : silentStep S m = m)
    (hpre : ∀ t : ℕ, 0 < t → t < n → (silentStep S)^[t] x ≠ x)
    (hmx : m ≠ x) : ¬ periodicPoint (silenceRec15_layered S) x := by
  intro hper
  rcases periodicPoint_step_iterate S hper with ⟨p, hp, hpp⟩
  by_cases hpge : p < n
  · exact hpre p hp hpge hpp
  · have hgeq : n ≤ p := le_of_not_gt hpge
    have hpadd : (p - n) + n = p := Nat.sub_add_cancel hgeq
    have hfixq : ∀ q : ℕ, (silentStep S)^[q] m = m := by
      intro q
      induction q with
      | zero => rfl
      | succ k ih =>
          rw [Function.iterate_succ_apply, hmfix, ih]
    have hpm : (silentStep S)^[p] x = m := by
      rw [← hpadd, Function.iterate_add_apply, hreach]
      exact hfixq (p - n)
    rw [hpm] at hpp
    exact hmx hpp

/-- 吸收实例（层 1，x=0 活跃、m=1 静默）：0→1 一步吸收。 -/
lemma layer1_absorb_01 (S : Finset (Fin 15))
    (h0S : (0 : Fin 15) ∉ S) (h1S : (1 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (0 : Fin 15) := by
  have hpre : ∀ t : ℕ, 0 < t → t < 1 → (silentStep S)^[t] (0 : Fin 15) ≠ 0 := by
    intro t ht1 ht3
    omega
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S (0 : Fin 15) = (1 : Fin 15)
        simp [silentStep, layeredStep, layer1, h0S])
    (by simp [silentStep, h1S])
    hpre (by decide)

/-- 吸收实例（层 1，x=0 活跃、m=2 静默、1 活跃）：0→1→2 两步吸收。 -/
lemma layer1_absorb_02 (S : Finset (Fin 15))
    (h0S : (0 : Fin 15) ∉ S) (h1S : (1 : Fin 15) ∉ S) (h2S : (2 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (0 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (0 : Fin 15) ≠ 0 := by
    change silentStep S (0 : Fin 15) ≠ (0 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S]
  have hpre : ∀ t : ℕ, 0 < t → t < 2 → (silentStep S)^[t] (0 : Fin 15) ≠ 0 := by
    intro t ht1 ht3
    rcases t with _ | t
    · omega
    · have ht' : t = 0 := by omega
      subst t
      exact hpre1
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S (0 : Fin 15)) = (2 : Fin 15)
        simp [silentStep, layeredStep, layer1, h0S, h1S])
    (by simp [silentStep, h2S])
    hpre (by decide)

/-- 吸收实例（层 1，x=0 活跃、m=3 静默、1/2 活跃）：0→1→2→3 三步吸收。 -/
lemma layer1_absorb_03 (S : Finset (Fin 15))
    (h0S : (0 : Fin 15) ∉ S) (h1S : (1 : Fin 15) ∉ S) (h2S : (2 : Fin 15) ∉ S)
    (h3S : (3 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (0 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (0 : Fin 15) ≠ 0 := by
    change silentStep S (0 : Fin 15) ≠ (0 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S]
  have hpre2 : (silentStep S)^[2] (0 : Fin 15) ≠ 0 := by
    change silentStep S (silentStep S (0 : Fin 15)) ≠ (0 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S, h1S]
  have hpre : ∀ t : ℕ, 0 < t → t < 3 → (silentStep S)^[t] (0 : Fin 15) ≠ 0 := by
    intro t ht1 ht3
    rcases t with _ | _ | t
    · omega
    · exact hpre1
    · have ht' : t = 0 := by omega
      subst t
      exact hpre2
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S (0 : Fin 15))) = (3 : Fin 15)
        simp [silentStep, layeredStep, layer1, h0S, h1S, h2S])
    (by simp [silentStep, h3S])
    hpre (by decide)

/-- hpre 辅助（n=1：无正 t 满足 t<1，任意 x）。 -/
lemma hpre_empty (S : Finset (Fin 15)) (x : Fin 15) :
    ∀ t : ℕ, 0 < t → t < 1 → (silentStep S)^[t] x ≠ x := by
  intro t ht1 ht3
  omega

/-- hpre 辅助（n=2：仅 t=1，需 step^[1] x ≠ x）。 -/
lemma hpre_single (S : Finset (Fin 15)) (x : Fin 15)
    (h1 : (silentStep S)^[1] x ≠ x) :
    ∀ t : ℕ, 0 < t → t < 2 → (silentStep S)^[t] x ≠ x := by
  intro t ht1 ht3
  rcases t with _ | t
  · omega
  · have ht' : t = 0 := by omega
    subst t
    exact h1

/-- hpre 辅助（n=3：需 step^[1]、step^[2] 均不归 x）。 -/
lemma hpre_double (S : Finset (Fin 15)) (x : Fin 15)
    (h1 : (silentStep S)^[1] x ≠ x) (h2 : (silentStep S)^[2] x ≠ x) :
    ∀ t : ℕ, 0 < t → t < 3 → (silentStep S)^[t] x ≠ x := by
  intro t ht1 ht3
  rcases t with _ | _ | t
  · omega
  · exact h1
  · have ht' : t = 0 := by omega
    subst t
    exact h2

/-- 层 1 x=1：step^[1] 不归（1∉S ⟹ 1→2≠1）。 -/
lemma active_step1_ne_l1x1 (S : Finset (Fin 15)) (h1S : (1 : Fin 15) ∉ S) :
    (silentStep S)^[1] (1 : Fin 15) ≠ 1 := by
  change silentStep S (1 : Fin 15) ≠ (1 : Fin 15)
  simp [silentStep, layeredStep, layer1, h1S]

/-- 层 1 x=1：step^[2] 不归（1,2∉S ⟹ 1→2→3≠1）。 -/
lemma active_step2_ne_l1x1 (S : Finset (Fin 15)) (h1S : (1 : Fin 15) ∉ S)
    (h2S : (2 : Fin 15) ∉ S) : (silentStep S)^[2] (1 : Fin 15) ≠ 1 := by
  change silentStep S (silentStep S (1 : Fin 15)) ≠ (1 : Fin 15)
  simp [silentStep, layeredStep, layer1, h1S, h2S]

/-- 层 1 x=2：step^[1] 不归（2∉S ⟹ 2→3≠2）。 -/
lemma active_step1_ne_l1x2 (S : Finset (Fin 15)) (h2S : (2 : Fin 15) ∉ S) :
    (silentStep S)^[1] (2 : Fin 15) ≠ 2 := by
  change silentStep S (2 : Fin 15) ≠ (2 : Fin 15)
  simp [silentStep, layeredStep, layer1, h2S]

/-- 层 1 x=2：step^[2] 不归（2,3∉S ⟹ 2→3→0≠2）。 -/
lemma active_step2_ne_l1x2 (S : Finset (Fin 15)) (h2S : (2 : Fin 15) ∉ S)
    (h3S : (3 : Fin 15) ∉ S) : (silentStep S)^[2] (2 : Fin 15) ≠ 2 := by
  change silentStep S (silentStep S (2 : Fin 15)) ≠ (2 : Fin 15)
  simp [silentStep, layeredStep, layer1, h2S, h3S]

/-- 层 1 x=3：step^[1] 不归（3∉S ⟹ 3→0≠3）。 -/
lemma active_step1_ne_l1x3 (S : Finset (Fin 15)) (h3S : (3 : Fin 15) ∉ S) :
    (silentStep S)^[1] (3 : Fin 15) ≠ 3 := by
  change silentStep S (3 : Fin 15) ≠ (3 : Fin 15)
  simp [silentStep, layeredStep, layer1, h3S]

/-- 层 1 x=3：step^[2] 不归（3,0∉S ⟹ 3→0→1≠3）。 -/
lemma active_step2_ne_l1x3 (S : Finset (Fin 15)) (h3S : (3 : Fin 15) ∉ S)
    (h0S : (0 : Fin 15) ∉ S) : (silentStep S)^[2] (3 : Fin 15) ≠ 3 := by
  change silentStep S (silentStep S (3 : Fin 15)) ≠ (3 : Fin 15)
  simp [silentStep, layeredStep, layer1, h3S, h0S]

/-- 吸收实例（层 1，x=1 活跃、0 静默、2/3 活跃）：1→2→3→0 三步吸收。 -/
lemma layer1_absorb_1_0 (S : Finset (Fin 15))
    (h1S : (1 : Fin 15) ∉ S) (h2S : (2 : Fin 15) ∉ S) (h3S : (3 : Fin 15) ∉ S)
    (h0S : (0 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (1 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S (1 : Fin 15))) = (0 : Fin 15)
        simp [silentStep, layeredStep, layer1, h1S, h2S, h3S])
    (by simp [silentStep, h0S])
    (hpre_double S 1 (active_step1_ne_l1x1 S h1S) (active_step2_ne_l1x1 S h1S h2S))
    (by decide)

/-- 吸收实例（层 1，x=1 活跃、2 静默）：1→2 一步吸收。 -/
lemma layer1_absorb_1_2 (S : Finset (Fin 15))
    (h1S : (1 : Fin 15) ∉ S) (h2S : (2 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (1 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S (1 : Fin 15) = (2 : Fin 15)
        simp [silentStep, layeredStep, layer1, h1S])
    (by simp [silentStep, h2S])
    (hpre_empty S 1) (by decide)

/-- 吸收实例（层 1，x=1 活跃、3 静默、2 活跃）：1→2→3 两步吸收。 -/
lemma layer1_absorb_1_3 (S : Finset (Fin 15))
    (h1S : (1 : Fin 15) ∉ S) (h2S : (2 : Fin 15) ∉ S) (h3S : (3 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (1 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S (1 : Fin 15)) = (3 : Fin 15)
        simp [silentStep, layeredStep, layer1, h1S, h2S])
    (by simp [silentStep, h3S])
    (hpre_single S 1 (active_step1_ne_l1x1 S h1S))
    (by decide)

/-- 吸收实例（层 1，x=2 活跃、0 静默、3 活跃）：2→3→0 两步吸收。 -/
lemma layer1_absorb_2_0 (S : Finset (Fin 15))
    (h2S : (2 : Fin 15) ∉ S) (h3S : (3 : Fin 15) ∉ S) (h0S : (0 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (2 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S (2 : Fin 15)) = (0 : Fin 15)
        simp [silentStep, layeredStep, layer1, h2S, h3S])
    (by simp [silentStep, h0S])
    (hpre_single S 2 (active_step1_ne_l1x2 S h2S))
    (by decide)

/-- 吸收实例（层 1，x=2 活跃、1 静默、3/0 活跃）：2→3→0→1 三步吸收。 -/
lemma layer1_absorb_2_1 (S : Finset (Fin 15))
    (h2S : (2 : Fin 15) ∉ S) (h3S : (3 : Fin 15) ∉ S) (h0S : (0 : Fin 15) ∉ S)
    (h1S : (1 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (2 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S (2 : Fin 15))) = (1 : Fin 15)
        simp [silentStep, layeredStep, layer1, h2S, h3S, h0S])
    (by simp [silentStep, h1S])
    (hpre_double S 2 (active_step1_ne_l1x2 S h2S) (active_step2_ne_l1x2 S h2S h3S))
    (by decide)

/-- 吸收实例（层 1，x=2 活跃、3 静默）：2→3 一步吸收。 -/
lemma layer1_absorb_2_3 (S : Finset (Fin 15))
    (h2S : (2 : Fin 15) ∉ S) (h3S : (3 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (2 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S (2 : Fin 15) = (3 : Fin 15)
        simp [silentStep, layeredStep, layer1, h2S])
    (by simp [silentStep, h3S])
    (hpre_empty S 2) (by decide)

/-- 吸收实例（层 1，x=3 活跃、0 静默）：3→0 一步吸收。 -/
lemma layer1_absorb_3_0 (S : Finset (Fin 15))
    (h3S : (3 : Fin 15) ∉ S) (h0S : (0 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (3 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S (3 : Fin 15) = (0 : Fin 15)
        simp [silentStep, layeredStep, layer1, h3S])
    (by simp [silentStep, h0S])
    (hpre_empty S 3) (by decide)

/-- 吸收实例（层 1，x=3 活跃、1 静默、0 活跃）：3→0→1 两步吸收。 -/
lemma layer1_absorb_3_1 (S : Finset (Fin 15))
    (h3S : (3 : Fin 15) ∉ S) (h0S : (0 : Fin 15) ∉ S) (h1S : (1 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (3 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S (3 : Fin 15)) = (1 : Fin 15)
        simp [silentStep, layeredStep, layer1, h3S, h0S])
    (by simp [silentStep, h1S])
    (hpre_single S 3 (active_step1_ne_l1x3 S h3S))
    (by decide)

/-- 吸收实例（层 1，x=3 活跃、2 静默、0/1 活跃）：3→0→1→2 三步吸收。 -/
lemma layer1_absorb_3_2 (S : Finset (Fin 15))
    (h3S : (3 : Fin 15) ∉ S) (h0S : (0 : Fin 15) ∉ S) (h1S : (1 : Fin 15) ∉ S)
    (h2S : (2 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (3 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S (3 : Fin 15))) = (2 : Fin 15)
        simp [silentStep, layeredStep, layer1, h3S, h0S, h1S])
    (by simp [silentStep, h2S])
    (hpre_double S 3 (active_step1_ne_l1x3 S h3S) (active_step2_ne_l1x3 S h3S h0S))
    (by decide)

/-- 层 1 部分静默 ⟹ 活跃窗非周期：层内 ∃ 静默窗（m ∈ S）且 x 活跃 ⟹ x 沿层循环
    被首个静默窗吸收（by_cases 路径选择最短吸收链）。 -/
lemma layer1_partial_silent_not_periodic (S : Finset (Fin 15)) {x : Fin 15}
    (hx : x ∈ layer1) (hxS : x ∉ S)
    (hS : ∃ m : Fin 15, m ∈ layer1 ∧ m ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) x := by
  rw [layer1] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer1] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · contradiction
    · exact layer1_absorb_01 S hxS hmS
    · by_cases h1 : (1 : Fin 15) ∈ S
      · exact layer1_absorb_01 S hxS h1
      · exact layer1_absorb_02 S hxS h1 hmS
    · by_cases h1 : (1 : Fin 15) ∈ S
      · exact layer1_absorb_01 S hxS h1
      · by_cases h2 : (2 : Fin 15) ∈ S
        · exact layer1_absorb_02 S hxS h1 h2
        · exact layer1_absorb_03 S hxS h1 h2 hmS
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer1] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · by_cases h2 : (2 : Fin 15) ∈ S
      · exact layer1_absorb_1_2 S hxS h2
      · by_cases h3 : (3 : Fin 15) ∈ S
        · exact layer1_absorb_1_3 S hxS h2 h3
        · exact layer1_absorb_1_0 S hxS h2 h3 hmS
    · contradiction
    · exact layer1_absorb_1_2 S hxS hmS
    · by_cases h2 : (2 : Fin 15) ∈ S
      · exact layer1_absorb_1_2 S hxS h2
      · exact layer1_absorb_1_3 S hxS h2 hmS
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer1] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · by_cases h3 : (3 : Fin 15) ∈ S
      · exact layer1_absorb_2_3 S hxS h3
      · exact layer1_absorb_2_0 S hxS h3 hmS
    · by_cases h3 : (3 : Fin 15) ∈ S
      · exact layer1_absorb_2_3 S hxS h3
      · by_cases h0 : (0 : Fin 15) ∈ S
        · exact layer1_absorb_2_0 S hxS h3 h0
        · exact layer1_absorb_2_1 S hxS h3 h0 hmS
    · contradiction
    · exact layer1_absorb_2_3 S hxS hmS
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer1] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · exact layer1_absorb_3_0 S hxS hmS
    · by_cases h0 : (0 : Fin 15) ∈ S
      · exact layer1_absorb_3_0 S hxS h0
      · exact layer1_absorb_3_1 S hxS h0 hmS
    · by_cases h0 : (0 : Fin 15) ∈ S
      · exact layer1_absorb_3_0 S hxS h0
      · by_cases h1 : (1 : Fin 15) ∈ S
        · exact layer1_absorb_3_1 S hxS h0 h1
        · exact layer1_absorb_3_2 S hxS h0 h1 hmS
    · contradiction

/-- hpre 辅助（n=4：需 step^[1..3] 均不归 x）。 -/
lemma hpre_triple (S : Finset (Fin 15)) (x : Fin 15)
    (h1 : (silentStep S)^[1] x ≠ x) (h2 : (silentStep S)^[2] x ≠ x)
    (h3 : (silentStep S)^[3] x ≠ x) :
    ∀ t : ℕ, 0 < t → t < 4 → (silentStep S)^[t] x ≠ x := by
  intro t ht1 ht3
  rcases t with _ | _ | _ | t
  · omega
  · exact h1
  · exact h2
  · have ht' : t = 0 := by omega
    subst t
    exact h3

/-- hpre 辅助（n=5：需 step^[1..4] 均不归 x）。 -/
lemma hpre_quad (S : Finset (Fin 15)) (x : Fin 15)
    (h1 : (silentStep S)^[1] x ≠ x) (h2 : (silentStep S)^[2] x ≠ x)
    (h3 : (silentStep S)^[3] x ≠ x) (h4 : (silentStep S)^[4] x ≠ x) :
    ∀ t : ℕ, 0 < t → t < 5 → (silentStep S)^[t] x ≠ x := by
  intro t ht1 ht3
  rcases t with _ | _ | _ | _ | t
  · omega
  · exact h1
  · exact h2
  · exact h3
  · have ht' : t = 0 := by omega
    subst t
    exact h4

/-- 层 3 部分静默 ⟹ 活跃窗非周期（层 3 = 10→11→12→13→10 循环，与层 1 同构）。 -/
lemma layer3_partial_silent_not_periodic (S : Finset (Fin 15)) {x : Fin 15}
    (hx : x ∈ layer3) (hxS : x ∉ S)
    (hS : ∃ m : Fin 15, m ∈ layer3 ∧ m ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) x := by
  rw [layer3] at hx
  simp at hx
  rcases hx with rfl | rfl | rfl | rfl
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer3] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · contradiction
    · exact not_periodic_of_reaches_fixed S 1
        (by change silentStep S (10 : Fin 15) = (11 : Fin 15)
            simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
        (by simp [silentStep, hmS]) (hpre_empty S 10) (by decide)
    · by_cases h11 : (11 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (10 : Fin 15) = (11 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h11]) (hpre_empty S 10) (by decide)
      · exact not_periodic_of_reaches_fixed S 2
          (by change silentStep S (silentStep S (10 : Fin 15)) = (12 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h11])
          (by simp [silentStep, hmS])
          (hpre_single S 10 (by change silentStep S (10 : Fin 15) ≠ (10 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
          (by decide)
    · by_cases h11 : (11 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (10 : Fin 15) = (11 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h11]) (hpre_empty S 10) (by decide)
      · by_cases h12 : (12 : Fin 15) ∈ S
        · exact not_periodic_of_reaches_fixed S 2
            (by change silentStep S (silentStep S (10 : Fin 15)) = (12 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h11])
            (by simp [silentStep, h12])
            (hpre_single S 10 (by change silentStep S (10 : Fin 15) ≠ (10 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
            (by decide)
        · exact not_periodic_of_reaches_fixed S 3
            (by change silentStep S (silentStep S (silentStep S (10 : Fin 15))) = (13 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h11, h12])
            (by simp [silentStep, hmS])
            (hpre_double S 10 (by change silentStep S (10 : Fin 15) ≠ (10 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]) (by change silentStep S (silentStep S (10 : Fin 15)) ≠ (10 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h11]))
            (by decide)
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer3] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · by_cases h12 : (12 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (11 : Fin 15) = (12 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h12]) (hpre_empty S 11) (by decide)
      · by_cases h13 : (13 : Fin 15) ∈ S
        · exact not_periodic_of_reaches_fixed S 2
            (by change silentStep S (silentStep S (11 : Fin 15)) = (13 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h12])
            (by simp [silentStep, h13])
            (hpre_single S 11 (by change silentStep S (11 : Fin 15) ≠ (11 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
            (by decide)
        · exact not_periodic_of_reaches_fixed S 3
            (by change silentStep S (silentStep S (silentStep S (11 : Fin 15))) = (10 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h12, h13])
            (by simp [silentStep, hmS])
            (hpre_double S 11 (by change silentStep S (11 : Fin 15) ≠ (11 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]) (by change silentStep S (silentStep S (11 : Fin 15)) ≠ (11 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h12]))
            (by decide)
    · contradiction
    · exact not_periodic_of_reaches_fixed S 1
        (by change silentStep S (11 : Fin 15) = (12 : Fin 15)
            simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
        (by simp [silentStep, hmS]) (hpre_empty S 11) (by decide)
    · by_cases h12 : (12 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (11 : Fin 15) = (12 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h12]) (hpre_empty S 11) (by decide)
      · exact not_periodic_of_reaches_fixed S 2
          (by change silentStep S (silentStep S (11 : Fin 15)) = (13 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h12])
          (by simp [silentStep, hmS])
          (hpre_single S 11 (by change silentStep S (11 : Fin 15) ≠ (11 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
          (by decide)
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer3] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · by_cases h13 : (13 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (12 : Fin 15) = (13 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h13]) (hpre_empty S 12) (by decide)
      · exact not_periodic_of_reaches_fixed S 2
          (by change silentStep S (silentStep S (12 : Fin 15)) = (10 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h13])
          (by simp [silentStep, hmS])
          (hpre_single S 12 (by change silentStep S (12 : Fin 15) ≠ (12 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
          (by decide)
    · by_cases h13 : (13 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (12 : Fin 15) = (13 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h13]) (hpre_empty S 12) (by decide)
      · by_cases h10 : (10 : Fin 15) ∈ S
        · exact not_periodic_of_reaches_fixed S 2
            (by change silentStep S (silentStep S (12 : Fin 15)) = (10 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h13])
            (by simp [silentStep, h10])
            (hpre_single S 12 (by change silentStep S (12 : Fin 15) ≠ (12 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
            (by decide)
        · exact not_periodic_of_reaches_fixed S 3
            (by change silentStep S (silentStep S (silentStep S (12 : Fin 15))) = (11 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h13, h10])
            (by simp [silentStep, hmS])
            (hpre_double S 12 (by change silentStep S (12 : Fin 15) ≠ (12 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]) (by change silentStep S (silentStep S (12 : Fin 15)) ≠ (12 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h13]))
            (by decide)
    · contradiction
    · by_cases h13 : (13 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (12 : Fin 15) = (13 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h13]) (hpre_empty S 12) (by decide)
      · exact False.elim (h13 hmS)
  · rcases hS with ⟨m, hml, hmS⟩
    rw [layer3] at hml
    simp at hml
    rcases hml with rfl | rfl | rfl | rfl
    · exact not_periodic_of_reaches_fixed S 1
        (by change silentStep S (13 : Fin 15) = (10 : Fin 15)
            simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
        (by simp [silentStep, hmS]) (hpre_empty S 13) (by decide)
    · by_cases h10 : (10 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (13 : Fin 15) = (10 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h10]) (hpre_empty S 13) (by decide)
      · exact not_periodic_of_reaches_fixed S 2
          (by change silentStep S (silentStep S (13 : Fin 15)) = (11 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h10])
          (by simp [silentStep, hmS])
          (hpre_single S 13 (by change silentStep S (13 : Fin 15) ≠ (13 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
          (by decide)
    · by_cases h10 : (10 : Fin 15) ∈ S
      · exact not_periodic_of_reaches_fixed S 1
          (by change silentStep S (13 : Fin 15) = (10 : Fin 15)
              simp [silentStep, layeredStep, layer1, layer2, layer3, hxS])
          (by simp [silentStep, h10]) (hpre_empty S 13) (by decide)
      · by_cases h11 : (11 : Fin 15) ∈ S
        · exact not_periodic_of_reaches_fixed S 2
            (by change silentStep S (silentStep S (13 : Fin 15)) = (11 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h10])
            (by simp [silentStep, h11])
            (hpre_single S 13 (by change silentStep S (13 : Fin 15) ≠ (13 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]))
            (by decide)
        · exact not_periodic_of_reaches_fixed S 3
            (by change silentStep S (silentStep S (silentStep S (13 : Fin 15))) = (12 : Fin 15)
                simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h10, h11])
            (by simp [silentStep, hmS])
            (hpre_double S 13 (by change silentStep S (13 : Fin 15) ≠ (13 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS]) (by change silentStep S (silentStep S (13 : Fin 15)) ≠ (13 : Fin 15); simp [silentStep, layeredStep, layer1, layer2, layer3, hxS, h10]))
            (by decide)
    · contradiction

lemma active_step1_ne_l2x4 (S : Finset (Fin 15)) (h4S : (4 : Fin 15) ∉ S) :
    (silentStep S)^[1] (4 : Fin 15) ≠ 4 := by
  change silentStep S ((4 : Fin 15)) ≠ (4 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h4S]

lemma active_step2_ne_l2x4 (S : Finset (Fin 15)) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) :
    (silentStep S)^[2] (4 : Fin 15) ≠ 4 := by
  change silentStep S (silentStep S ((4 : Fin 15))) ≠ (4 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S]

lemma active_step3_ne_l2x4 (S : Finset (Fin 15)) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) :
    (silentStep S)^[3] (4 : Fin 15) ≠ 4 := by
  change silentStep S (silentStep S (silentStep S ((4 : Fin 15)))) ≠ (4 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S]

lemma active_step4_ne_l2x4 (S : Finset (Fin 15)) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) :
    (silentStep S)^[4] (4 : Fin 15) ≠ 4 := by
  change silentStep S (silentStep S (silentStep S (silentStep S ((4 : Fin 15))))) ≠ (4 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S, h7S]

lemma active_step1_ne_l2x5 (S : Finset (Fin 15)) (h5S : (5 : Fin 15) ∉ S) :
    (silentStep S)^[1] (5 : Fin 15) ≠ 5 := by
  change silentStep S ((5 : Fin 15)) ≠ (5 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h5S]

lemma active_step2_ne_l2x5 (S : Finset (Fin 15)) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) :
    (silentStep S)^[2] (5 : Fin 15) ≠ 5 := by
  change silentStep S (silentStep S ((5 : Fin 15))) ≠ (5 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S]

lemma active_step3_ne_l2x5 (S : Finset (Fin 15)) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) :
    (silentStep S)^[3] (5 : Fin 15) ≠ 5 := by
  change silentStep S (silentStep S (silentStep S ((5 : Fin 15)))) ≠ (5 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S]

lemma active_step4_ne_l2x5 (S : Finset (Fin 15)) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) :
    (silentStep S)^[4] (5 : Fin 15) ≠ 5 := by
  change silentStep S (silentStep S (silentStep S (silentStep S ((5 : Fin 15))))) ≠ (5 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S, h8S]

lemma active_step1_ne_l2x6 (S : Finset (Fin 15)) (h6S : (6 : Fin 15) ∉ S) :
    (silentStep S)^[1] (6 : Fin 15) ≠ 6 := by
  change silentStep S ((6 : Fin 15)) ≠ (6 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h6S]

lemma active_step2_ne_l2x6 (S : Finset (Fin 15)) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) :
    (silentStep S)^[2] (6 : Fin 15) ≠ 6 := by
  change silentStep S (silentStep S ((6 : Fin 15))) ≠ (6 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S]

lemma active_step3_ne_l2x6 (S : Finset (Fin 15)) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) :
    (silentStep S)^[3] (6 : Fin 15) ≠ 6 := by
  change silentStep S (silentStep S (silentStep S ((6 : Fin 15)))) ≠ (6 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S]

lemma active_step4_ne_l2x6 (S : Finset (Fin 15)) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) :
    (silentStep S)^[4] (6 : Fin 15) ≠ 6 := by
  change silentStep S (silentStep S (silentStep S (silentStep S ((6 : Fin 15))))) ≠ (6 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S, h9S]

lemma active_step1_ne_l2x7 (S : Finset (Fin 15)) (h7S : (7 : Fin 15) ∉ S) :
    (silentStep S)^[1] (7 : Fin 15) ≠ 7 := by
  change silentStep S ((7 : Fin 15)) ≠ (7 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h7S]

lemma active_step2_ne_l2x7 (S : Finset (Fin 15)) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) :
    (silentStep S)^[2] (7 : Fin 15) ≠ 7 := by
  change silentStep S (silentStep S ((7 : Fin 15))) ≠ (7 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S]

lemma active_step3_ne_l2x7 (S : Finset (Fin 15)) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) :
    (silentStep S)^[3] (7 : Fin 15) ≠ 7 := by
  change silentStep S (silentStep S (silentStep S ((7 : Fin 15)))) ≠ (7 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S]

lemma active_step4_ne_l2x7 (S : Finset (Fin 15)) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) :
    (silentStep S)^[4] (7 : Fin 15) ≠ 7 := by
  change silentStep S (silentStep S (silentStep S (silentStep S ((7 : Fin 15))))) ≠ (7 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S, h4S]

lemma active_step1_ne_l2x8 (S : Finset (Fin 15)) (h8S : (8 : Fin 15) ∉ S) :
    (silentStep S)^[1] (8 : Fin 15) ≠ 8 := by
  change silentStep S ((8 : Fin 15)) ≠ (8 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h8S]

lemma active_step2_ne_l2x8 (S : Finset (Fin 15)) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) :
    (silentStep S)^[2] (8 : Fin 15) ≠ 8 := by
  change silentStep S (silentStep S ((8 : Fin 15))) ≠ (8 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S]

lemma active_step3_ne_l2x8 (S : Finset (Fin 15)) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) :
    (silentStep S)^[3] (8 : Fin 15) ≠ 8 := by
  change silentStep S (silentStep S (silentStep S ((8 : Fin 15)))) ≠ (8 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S]

lemma active_step4_ne_l2x8 (S : Finset (Fin 15)) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) :
    (silentStep S)^[4] (8 : Fin 15) ≠ 8 := by
  change silentStep S (silentStep S (silentStep S (silentStep S ((8 : Fin 15))))) ≠ (8 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S, h5S]

lemma active_step1_ne_l2x9 (S : Finset (Fin 15)) (h9S : (9 : Fin 15) ∉ S) :
    (silentStep S)^[1] (9 : Fin 15) ≠ 9 := by
  change silentStep S ((9 : Fin 15)) ≠ (9 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h9S]

lemma active_step2_ne_l2x9 (S : Finset (Fin 15)) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) :
    (silentStep S)^[2] (9 : Fin 15) ≠ 9 := by
  change silentStep S (silentStep S ((9 : Fin 15))) ≠ (9 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S]

lemma active_step3_ne_l2x9 (S : Finset (Fin 15)) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) :
    (silentStep S)^[3] (9 : Fin 15) ≠ 9 := by
  change silentStep S (silentStep S (silentStep S ((9 : Fin 15)))) ≠ (9 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S]

lemma active_step4_ne_l2x9 (S : Finset (Fin 15)) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) :
    (silentStep S)^[4] (9 : Fin 15) ≠ 9 := by
  change silentStep S (silentStep S (silentStep S (silentStep S ((9 : Fin 15))))) ≠ (9 : Fin 15)
  simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S, h6S]
/-- 吸收实例（层 2，x=4 活跃、m=5 静默、路径 4→5 吸收，n=1）。 -/
lemma layer2_absorb_4_5 (S : Finset (Fin 15))
    (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (4 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S ((4 : Fin 15)) = (5 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h4S])
    (by simp [silentStep, h5S])
    (hpre_empty S (4 : Fin 15)) (by decide)

/-- 吸收实例（层 2，x=4 活跃、m=6 静默、路径 4→5→6 吸收，n=2）。 -/
lemma layer2_absorb_4_6 (S : Finset (Fin 15))
    (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (4 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S ((4 : Fin 15)) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S]
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S ((4 : Fin 15))) = (6 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S])
    (by simp [silentStep, h6S])
    (hpre_single S (4 : Fin 15) hpre1) (by decide)

/-- 吸收实例（层 2，x=4 活跃、m=7 静默、路径 4→5→6→7 吸收，n=3）。 -/
lemma layer2_absorb_4_7 (S : Finset (Fin 15))
    (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (4 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S ((4 : Fin 15)) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S]
  have hpre2 : (silentStep S)^[2] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S (silentStep S ((4 : Fin 15))) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S]
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S ((4 : Fin 15)))) = (7 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S])
    (by simp [silentStep, h7S])
    (hpre_double S (4 : Fin 15) hpre1 hpre2) (by decide)

/-- 吸收实例（层 2，x=4 活跃、m=8 静默、路径 4→5→6→7→8 吸收，n=4）。 -/
lemma layer2_absorb_4_8 (S : Finset (Fin 15))
    (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (4 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S ((4 : Fin 15)) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S]
  have hpre2 : (silentStep S)^[2] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S (silentStep S ((4 : Fin 15))) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S]
  have hpre3 : (silentStep S)^[3] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((4 : Fin 15)))) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S]
  exact not_periodic_of_reaches_fixed S 4
    (by change silentStep S (silentStep S (silentStep S (silentStep S ((4 : Fin 15))))) = (8 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S, h7S])
    (by simp [silentStep, h8S])
    (hpre_triple S (4 : Fin 15) hpre1 hpre2 hpre3) (by decide)

/-- 吸收实例（层 2，x=4 活跃、m=9 静默、路径 4→5→6→7→8→9 吸收，n=5）。 -/
lemma layer2_absorb_4_9 (S : Finset (Fin 15))
    (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (4 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S ((4 : Fin 15)) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S]
  have hpre2 : (silentStep S)^[2] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S (silentStep S ((4 : Fin 15))) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S]
  have hpre3 : (silentStep S)^[3] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((4 : Fin 15)))) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S]
  have hpre4 : (silentStep S)^[4] (4 : Fin 15) ≠ (4 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S (silentStep S ((4 : Fin 15))))) ≠ (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S, h7S]
  exact not_periodic_of_reaches_fixed S 5
    (by change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((4 : Fin 15)))))) = (9 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h4S, h5S, h6S, h7S, h8S])
    (by simp [silentStep, h9S])
    (hpre_quad S (4 : Fin 15) hpre1 hpre2 hpre3 hpre4) (by decide)

/-- 吸收实例（层 2，x=5 活跃、m=4 静默、路径 5→6→7→8→9→4 吸收，n=5）。 -/
lemma layer2_absorb_5_4 (S : Finset (Fin 15))
    (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (5 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S ((5 : Fin 15)) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S]
  have hpre2 : (silentStep S)^[2] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S (silentStep S ((5 : Fin 15))) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S]
  have hpre3 : (silentStep S)^[3] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((5 : Fin 15)))) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S]
  have hpre4 : (silentStep S)^[4] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S (silentStep S ((5 : Fin 15))))) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S, h8S]
  exact not_periodic_of_reaches_fixed S 5
    (by change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((5 : Fin 15)))))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S, h8S, h9S])
    (by simp [silentStep, h4S])
    (hpre_quad S (5 : Fin 15) hpre1 hpre2 hpre3 hpre4) (by decide)

/-- 吸收实例（层 2，x=5 活跃、m=6 静默、路径 5→6 吸收，n=1）。 -/
lemma layer2_absorb_5_6 (S : Finset (Fin 15))
    (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (5 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S ((5 : Fin 15)) = (6 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h5S])
    (by simp [silentStep, h6S])
    (hpre_empty S (5 : Fin 15)) (by decide)

/-- 吸收实例（层 2，x=5 活跃、m=7 静默、路径 5→6→7 吸收，n=2）。 -/
lemma layer2_absorb_5_7 (S : Finset (Fin 15))
    (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (5 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S ((5 : Fin 15)) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S]
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S ((5 : Fin 15))) = (7 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S])
    (by simp [silentStep, h7S])
    (hpre_single S (5 : Fin 15) hpre1) (by decide)

/-- 吸收实例（层 2，x=5 活跃、m=8 静默、路径 5→6→7→8 吸收，n=3）。 -/
lemma layer2_absorb_5_8 (S : Finset (Fin 15))
    (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (5 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S ((5 : Fin 15)) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S]
  have hpre2 : (silentStep S)^[2] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S (silentStep S ((5 : Fin 15))) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S]
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S ((5 : Fin 15)))) = (8 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S])
    (by simp [silentStep, h8S])
    (hpre_double S (5 : Fin 15) hpre1 hpre2) (by decide)

/-- 吸收实例（层 2，x=5 活跃、m=9 静默、路径 5→6→7→8→9 吸收，n=4）。 -/
lemma layer2_absorb_5_9 (S : Finset (Fin 15))
    (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (5 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S ((5 : Fin 15)) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S]
  have hpre2 : (silentStep S)^[2] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S (silentStep S ((5 : Fin 15))) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S]
  have hpre3 : (silentStep S)^[3] (5 : Fin 15) ≠ (5 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((5 : Fin 15)))) ≠ (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S]
  exact not_periodic_of_reaches_fixed S 4
    (by change silentStep S (silentStep S (silentStep S (silentStep S ((5 : Fin 15))))) = (9 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h5S, h6S, h7S, h8S])
    (by simp [silentStep, h9S])
    (hpre_triple S (5 : Fin 15) hpre1 hpre2 hpre3) (by decide)

/-- 吸收实例（层 2，x=6 活跃、m=4 静默、路径 6→7→8→9→4 吸收，n=4）。 -/
lemma layer2_absorb_6_4 (S : Finset (Fin 15))
    (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (6 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S ((6 : Fin 15)) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S]
  have hpre2 : (silentStep S)^[2] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S (silentStep S ((6 : Fin 15))) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S]
  have hpre3 : (silentStep S)^[3] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((6 : Fin 15)))) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S]
  exact not_periodic_of_reaches_fixed S 4
    (by change silentStep S (silentStep S (silentStep S (silentStep S ((6 : Fin 15))))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S, h9S])
    (by simp [silentStep, h4S])
    (hpre_triple S (6 : Fin 15) hpre1 hpre2 hpre3) (by decide)

/-- 吸收实例（层 2，x=6 活跃、m=5 静默、路径 6→7→8→9→4→5 吸收，n=5）。 -/
lemma layer2_absorb_6_5 (S : Finset (Fin 15))
    (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (6 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S ((6 : Fin 15)) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S]
  have hpre2 : (silentStep S)^[2] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S (silentStep S ((6 : Fin 15))) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S]
  have hpre3 : (silentStep S)^[3] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((6 : Fin 15)))) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S]
  have hpre4 : (silentStep S)^[4] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S (silentStep S ((6 : Fin 15))))) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S, h9S]
  exact not_periodic_of_reaches_fixed S 5
    (by change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((6 : Fin 15)))))) = (5 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S, h9S, h4S])
    (by simp [silentStep, h5S])
    (hpre_quad S (6 : Fin 15) hpre1 hpre2 hpre3 hpre4) (by decide)

/-- 吸收实例（层 2，x=6 活跃、m=7 静默、路径 6→7 吸收，n=1）。 -/
lemma layer2_absorb_6_7 (S : Finset (Fin 15))
    (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (6 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S ((6 : Fin 15)) = (7 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h6S])
    (by simp [silentStep, h7S])
    (hpre_empty S (6 : Fin 15)) (by decide)

/-- 吸收实例（层 2，x=6 活跃、m=8 静默、路径 6→7→8 吸收，n=2）。 -/
lemma layer2_absorb_6_8 (S : Finset (Fin 15))
    (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (6 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S ((6 : Fin 15)) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S]
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S ((6 : Fin 15))) = (8 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S])
    (by simp [silentStep, h8S])
    (hpre_single S (6 : Fin 15) hpre1) (by decide)

/-- 吸收实例（层 2，x=6 活跃、m=9 静默、路径 6→7→8→9 吸收，n=3）。 -/
lemma layer2_absorb_6_9 (S : Finset (Fin 15))
    (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (6 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S ((6 : Fin 15)) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S]
  have hpre2 : (silentStep S)^[2] (6 : Fin 15) ≠ (6 : Fin 15) := by
    change silentStep S (silentStep S ((6 : Fin 15))) ≠ (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S]
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S ((6 : Fin 15)))) = (9 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h6S, h7S, h8S])
    (by simp [silentStep, h9S])
    (hpre_double S (6 : Fin 15) hpre1 hpre2) (by decide)

/-- 吸收实例（层 2，x=7 活跃、m=4 静默、路径 7→8→9→4 吸收，n=3）。 -/
lemma layer2_absorb_7_4 (S : Finset (Fin 15))
    (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (7 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S ((7 : Fin 15)) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S]
  have hpre2 : (silentStep S)^[2] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S (silentStep S ((7 : Fin 15))) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S]
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S ((7 : Fin 15)))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S])
    (by simp [silentStep, h4S])
    (hpre_double S (7 : Fin 15) hpre1 hpre2) (by decide)

/-- 吸收实例（层 2，x=7 活跃、m=5 静默、路径 7→8→9→4→5 吸收，n=4）。 -/
lemma layer2_absorb_7_5 (S : Finset (Fin 15))
    (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (7 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S ((7 : Fin 15)) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S]
  have hpre2 : (silentStep S)^[2] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S (silentStep S ((7 : Fin 15))) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S]
  have hpre3 : (silentStep S)^[3] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((7 : Fin 15)))) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S]
  exact not_periodic_of_reaches_fixed S 4
    (by change silentStep S (silentStep S (silentStep S (silentStep S ((7 : Fin 15))))) = (5 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S, h4S])
    (by simp [silentStep, h5S])
    (hpre_triple S (7 : Fin 15) hpre1 hpre2 hpre3) (by decide)

/-- 吸收实例（层 2，x=7 活跃、m=6 静默、路径 7→8→9→4→5→6 吸收，n=5）。 -/
lemma layer2_absorb_7_6 (S : Finset (Fin 15))
    (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (7 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S ((7 : Fin 15)) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S]
  have hpre2 : (silentStep S)^[2] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S (silentStep S ((7 : Fin 15))) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S]
  have hpre3 : (silentStep S)^[3] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((7 : Fin 15)))) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S]
  have hpre4 : (silentStep S)^[4] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S (silentStep S ((7 : Fin 15))))) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S, h4S]
  exact not_periodic_of_reaches_fixed S 5
    (by change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((7 : Fin 15)))))) = (6 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S, h9S, h4S, h5S])
    (by simp [silentStep, h6S])
    (hpre_quad S (7 : Fin 15) hpre1 hpre2 hpre3 hpre4) (by decide)

/-- 吸收实例（层 2，x=7 活跃、m=8 静默、路径 7→8 吸收，n=1）。 -/
lemma layer2_absorb_7_8 (S : Finset (Fin 15))
    (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (7 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S ((7 : Fin 15)) = (8 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h7S])
    (by simp [silentStep, h8S])
    (hpre_empty S (7 : Fin 15)) (by decide)

/-- 吸收实例（层 2，x=7 活跃、m=9 静默、路径 7→8→9 吸收，n=2）。 -/
lemma layer2_absorb_7_9 (S : Finset (Fin 15))
    (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (7 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (7 : Fin 15) ≠ (7 : Fin 15) := by
    change silentStep S ((7 : Fin 15)) ≠ (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h7S]
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S ((7 : Fin 15))) = (9 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h7S, h8S])
    (by simp [silentStep, h9S])
    (hpre_single S (7 : Fin 15) hpre1) (by decide)

/-- 吸收实例（层 2，x=8 活跃、m=4 静默、路径 8→9→4 吸收，n=2）。 -/
lemma layer2_absorb_8_4 (S : Finset (Fin 15))
    (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (8 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S ((8 : Fin 15)) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S]
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S ((8 : Fin 15))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S])
    (by simp [silentStep, h4S])
    (hpre_single S (8 : Fin 15) hpre1) (by decide)

/-- 吸收实例（层 2，x=8 活跃、m=5 静默、路径 8→9→4→5 吸收，n=3）。 -/
lemma layer2_absorb_8_5 (S : Finset (Fin 15))
    (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (8 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S ((8 : Fin 15)) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S]
  have hpre2 : (silentStep S)^[2] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S (silentStep S ((8 : Fin 15))) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S]
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S ((8 : Fin 15)))) = (5 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S])
    (by simp [silentStep, h5S])
    (hpre_double S (8 : Fin 15) hpre1 hpre2) (by decide)

/-- 吸收实例（层 2，x=8 活跃、m=6 静默、路径 8→9→4→5→6 吸收，n=4）。 -/
lemma layer2_absorb_8_6 (S : Finset (Fin 15))
    (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (8 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S ((8 : Fin 15)) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S]
  have hpre2 : (silentStep S)^[2] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S (silentStep S ((8 : Fin 15))) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S]
  have hpre3 : (silentStep S)^[3] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((8 : Fin 15)))) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S]
  exact not_periodic_of_reaches_fixed S 4
    (by change silentStep S (silentStep S (silentStep S (silentStep S ((8 : Fin 15))))) = (6 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S, h5S])
    (by simp [silentStep, h6S])
    (hpre_triple S (8 : Fin 15) hpre1 hpre2 hpre3) (by decide)

/-- 吸收实例（层 2，x=8 活跃、m=7 静默、路径 8→9→4→5→6→7 吸收，n=5）。 -/
lemma layer2_absorb_8_7 (S : Finset (Fin 15))
    (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (8 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S ((8 : Fin 15)) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S]
  have hpre2 : (silentStep S)^[2] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S (silentStep S ((8 : Fin 15))) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S]
  have hpre3 : (silentStep S)^[3] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((8 : Fin 15)))) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S]
  have hpre4 : (silentStep S)^[4] (8 : Fin 15) ≠ (8 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S (silentStep S ((8 : Fin 15))))) ≠ (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S, h5S]
  exact not_periodic_of_reaches_fixed S 5
    (by change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((8 : Fin 15)))))) = (7 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h8S, h9S, h4S, h5S, h6S])
    (by simp [silentStep, h7S])
    (hpre_quad S (8 : Fin 15) hpre1 hpre2 hpre3 hpre4) (by decide)

/-- 吸收实例（层 2，x=8 活跃、m=9 静默、路径 8→9 吸收，n=1）。 -/
lemma layer2_absorb_8_9 (S : Finset (Fin 15))
    (h8S : (8 : Fin 15) ∉ S) (h9S : (9 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (8 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S ((8 : Fin 15)) = (9 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h8S])
    (by simp [silentStep, h9S])
    (hpre_empty S (8 : Fin 15)) (by decide)

/-- 吸收实例（层 2，x=9 活跃、m=4 静默、路径 9→4 吸收，n=1）。 -/
lemma layer2_absorb_9_4 (S : Finset (Fin 15))
    (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (9 : Fin 15) := by
  exact not_periodic_of_reaches_fixed S 1
    (by change silentStep S ((9 : Fin 15)) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h9S])
    (by simp [silentStep, h4S])
    (hpre_empty S (9 : Fin 15)) (by decide)

/-- 吸收实例（层 2，x=9 活跃、m=5 静默、路径 9→4→5 吸收，n=2）。 -/
lemma layer2_absorb_9_5 (S : Finset (Fin 15))
    (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (9 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S ((9 : Fin 15)) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S]
  exact not_periodic_of_reaches_fixed S 2
    (by change silentStep S (silentStep S ((9 : Fin 15))) = (5 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S])
    (by simp [silentStep, h5S])
    (hpre_single S (9 : Fin 15) hpre1) (by decide)

/-- 吸收实例（层 2，x=9 活跃、m=6 静默、路径 9→4→5→6 吸收，n=3）。 -/
lemma layer2_absorb_9_6 (S : Finset (Fin 15))
    (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (9 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S ((9 : Fin 15)) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S]
  have hpre2 : (silentStep S)^[2] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S (silentStep S ((9 : Fin 15))) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S]
  exact not_periodic_of_reaches_fixed S 3
    (by change silentStep S (silentStep S (silentStep S ((9 : Fin 15)))) = (6 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S])
    (by simp [silentStep, h6S])
    (hpre_double S (9 : Fin 15) hpre1 hpre2) (by decide)

/-- 吸收实例（层 2，x=9 活跃、m=7 静默、路径 9→4→5→6→7 吸收，n=4）。 -/
lemma layer2_absorb_9_7 (S : Finset (Fin 15))
    (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (9 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S ((9 : Fin 15)) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S]
  have hpre2 : (silentStep S)^[2] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S (silentStep S ((9 : Fin 15))) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S]
  have hpre3 : (silentStep S)^[3] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((9 : Fin 15)))) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S]
  exact not_periodic_of_reaches_fixed S 4
    (by change silentStep S (silentStep S (silentStep S (silentStep S ((9 : Fin 15))))) = (7 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S, h6S])
    (by simp [silentStep, h7S])
    (hpre_triple S (9 : Fin 15) hpre1 hpre2 hpre3) (by decide)

/-- 吸收实例（层 2，x=9 活跃、m=8 静默、路径 9→4→5→6→7→8 吸收，n=5）。 -/
lemma layer2_absorb_9_8 (S : Finset (Fin 15))
    (h9S : (9 : Fin 15) ∉ S) (h4S : (4 : Fin 15) ∉ S) (h5S : (5 : Fin 15) ∉ S) (h6S : (6 : Fin 15) ∉ S) (h7S : (7 : Fin 15) ∉ S) (h8S : (8 : Fin 15) ∈ S) :
    ¬ periodicPoint (silenceRec15_layered S) (9 : Fin 15) := by
  have hpre1 : (silentStep S)^[1] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S ((9 : Fin 15)) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S]
  have hpre2 : (silentStep S)^[2] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S (silentStep S ((9 : Fin 15))) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S]
  have hpre3 : (silentStep S)^[3] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S ((9 : Fin 15)))) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S]
  have hpre4 : (silentStep S)^[4] (9 : Fin 15) ≠ (9 : Fin 15) := by
    change silentStep S (silentStep S (silentStep S (silentStep S ((9 : Fin 15))))) ≠ (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S, h6S]
  exact not_periodic_of_reaches_fixed S 5
    (by change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((9 : Fin 15)))))) = (8 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, h9S, h4S, h5S, h6S, h7S])
    (by simp [silentStep, h8S])
    (hpre_quad S (9 : Fin 15) hpre1 hpre2 hpre3 hpre4) (by decide)

/-- 层 2 部分静默 ⟹ 活跃窗非周期（层 2 = 4→5→6→7→8→9→4 六窗循环，最长吸收链 n=5）。 -/
lemma layer2_partial_silent_not_periodic (S : Finset (Fin 15)) {x : Fin 15}
    (hx : x ∈ layer2) (hS : ∃ m ∈ layer2, m ∈ S) (hxS : x ∉ S) :
    ¬ periodicPoint (silenceRec15_layered S) x := by
  simp [layer2] at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl
  · rcases hS with ⟨m, hml, hmS⟩
    simp [layer2] at hml
    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl
    · contradiction
    · exact layer2_absorb_4_5 S hxS hmS
    · by_cases h5 : (5 : Fin 15) ∈ S
      · exact layer2_absorb_4_5 S hxS h5
      · exact layer2_absorb_4_6 S hxS h5 hmS
    · by_cases h5 : (5 : Fin 15) ∈ S
      · exact layer2_absorb_4_5 S hxS h5
      · by_cases h6 : (6 : Fin 15) ∈ S
        · exact layer2_absorb_4_6 S hxS h5 h6
        · exact layer2_absorb_4_7 S hxS h5 h6 hmS
    · by_cases h5 : (5 : Fin 15) ∈ S
      · exact layer2_absorb_4_5 S hxS h5
      · by_cases h6 : (6 : Fin 15) ∈ S
        · exact layer2_absorb_4_6 S hxS h5 h6
        · by_cases h7 : (7 : Fin 15) ∈ S
          · exact layer2_absorb_4_7 S hxS h5 h6 h7
          · exact layer2_absorb_4_8 S hxS h5 h6 h7 hmS
    · by_cases h5 : (5 : Fin 15) ∈ S
      · exact layer2_absorb_4_5 S hxS h5
      · by_cases h6 : (6 : Fin 15) ∈ S
        · exact layer2_absorb_4_6 S hxS h5 h6
        · by_cases h7 : (7 : Fin 15) ∈ S
          · exact layer2_absorb_4_7 S hxS h5 h6 h7
          · by_cases h8 : (8 : Fin 15) ∈ S
            · exact layer2_absorb_4_8 S hxS h5 h6 h7 h8
            · exact layer2_absorb_4_9 S hxS h5 h6 h7 h8 hmS
  · rcases hS with ⟨m, hml, hmS⟩
    simp [layer2] at hml
    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl
    · by_cases h6 : (6 : Fin 15) ∈ S
      · exact layer2_absorb_5_6 S hxS h6
      · by_cases h7 : (7 : Fin 15) ∈ S
        · exact layer2_absorb_5_7 S hxS h6 h7
        · by_cases h8 : (8 : Fin 15) ∈ S
          · exact layer2_absorb_5_8 S hxS h6 h7 h8
          · by_cases h9 : (9 : Fin 15) ∈ S
            · exact layer2_absorb_5_9 S hxS h6 h7 h8 h9
            · exact layer2_absorb_5_4 S hxS h6 h7 h8 h9 hmS
    · contradiction
    · exact layer2_absorb_5_6 S hxS hmS
    · by_cases h6 : (6 : Fin 15) ∈ S
      · exact layer2_absorb_5_6 S hxS h6
      · exact layer2_absorb_5_7 S hxS h6 hmS
    · by_cases h6 : (6 : Fin 15) ∈ S
      · exact layer2_absorb_5_6 S hxS h6
      · by_cases h7 : (7 : Fin 15) ∈ S
        · exact layer2_absorb_5_7 S hxS h6 h7
        · exact layer2_absorb_5_8 S hxS h6 h7 hmS
    · by_cases h6 : (6 : Fin 15) ∈ S
      · exact layer2_absorb_5_6 S hxS h6
      · by_cases h7 : (7 : Fin 15) ∈ S
        · exact layer2_absorb_5_7 S hxS h6 h7
        · by_cases h8 : (8 : Fin 15) ∈ S
          · exact layer2_absorb_5_8 S hxS h6 h7 h8
          · exact layer2_absorb_5_9 S hxS h6 h7 h8 hmS
  · rcases hS with ⟨m, hml, hmS⟩
    simp [layer2] at hml
    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl
    · by_cases h7 : (7 : Fin 15) ∈ S
      · exact layer2_absorb_6_7 S hxS h7
      · by_cases h8 : (8 : Fin 15) ∈ S
        · exact layer2_absorb_6_8 S hxS h7 h8
        · by_cases h9 : (9 : Fin 15) ∈ S
          · exact layer2_absorb_6_9 S hxS h7 h8 h9
          · exact layer2_absorb_6_4 S hxS h7 h8 h9 hmS
    · by_cases h7 : (7 : Fin 15) ∈ S
      · exact layer2_absorb_6_7 S hxS h7
      · by_cases h8 : (8 : Fin 15) ∈ S
        · exact layer2_absorb_6_8 S hxS h7 h8
        · by_cases h9 : (9 : Fin 15) ∈ S
          · exact layer2_absorb_6_9 S hxS h7 h8 h9
          · by_cases h4 : (4 : Fin 15) ∈ S
            · exact layer2_absorb_6_4 S hxS h7 h8 h9 h4
            · exact layer2_absorb_6_5 S hxS h7 h8 h9 h4 hmS
    · contradiction
    · exact layer2_absorb_6_7 S hxS hmS
    · by_cases h7 : (7 : Fin 15) ∈ S
      · exact layer2_absorb_6_7 S hxS h7
      · exact layer2_absorb_6_8 S hxS h7 hmS
    · by_cases h7 : (7 : Fin 15) ∈ S
      · exact layer2_absorb_6_7 S hxS h7
      · by_cases h8 : (8 : Fin 15) ∈ S
        · exact layer2_absorb_6_8 S hxS h7 h8
        · exact layer2_absorb_6_9 S hxS h7 h8 hmS
  · rcases hS with ⟨m, hml, hmS⟩
    simp [layer2] at hml
    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl
    · by_cases h8 : (8 : Fin 15) ∈ S
      · exact layer2_absorb_7_8 S hxS h8
      · by_cases h9 : (9 : Fin 15) ∈ S
        · exact layer2_absorb_7_9 S hxS h8 h9
        · exact layer2_absorb_7_4 S hxS h8 h9 hmS
    · by_cases h8 : (8 : Fin 15) ∈ S
      · exact layer2_absorb_7_8 S hxS h8
      · by_cases h9 : (9 : Fin 15) ∈ S
        · exact layer2_absorb_7_9 S hxS h8 h9
        · by_cases h4 : (4 : Fin 15) ∈ S
          · exact layer2_absorb_7_4 S hxS h8 h9 h4
          · exact layer2_absorb_7_5 S hxS h8 h9 h4 hmS
    · by_cases h8 : (8 : Fin 15) ∈ S
      · exact layer2_absorb_7_8 S hxS h8
      · by_cases h9 : (9 : Fin 15) ∈ S
        · exact layer2_absorb_7_9 S hxS h8 h9
        · by_cases h4 : (4 : Fin 15) ∈ S
          · exact layer2_absorb_7_4 S hxS h8 h9 h4
          · by_cases h5 : (5 : Fin 15) ∈ S
            · exact layer2_absorb_7_5 S hxS h8 h9 h4 h5
            · exact layer2_absorb_7_6 S hxS h8 h9 h4 h5 hmS
    · contradiction
    · exact layer2_absorb_7_8 S hxS hmS
    · by_cases h8 : (8 : Fin 15) ∈ S
      · exact layer2_absorb_7_8 S hxS h8
      · exact layer2_absorb_7_9 S hxS h8 hmS
  · rcases hS with ⟨m, hml, hmS⟩
    simp [layer2] at hml
    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl
    · by_cases h9 : (9 : Fin 15) ∈ S
      · exact layer2_absorb_8_9 S hxS h9
      · exact layer2_absorb_8_4 S hxS h9 hmS
    · by_cases h9 : (9 : Fin 15) ∈ S
      · exact layer2_absorb_8_9 S hxS h9
      · by_cases h4 : (4 : Fin 15) ∈ S
        · exact layer2_absorb_8_4 S hxS h9 h4
        · exact layer2_absorb_8_5 S hxS h9 h4 hmS
    · by_cases h9 : (9 : Fin 15) ∈ S
      · exact layer2_absorb_8_9 S hxS h9
      · by_cases h4 : (4 : Fin 15) ∈ S
        · exact layer2_absorb_8_4 S hxS h9 h4
        · by_cases h5 : (5 : Fin 15) ∈ S
          · exact layer2_absorb_8_5 S hxS h9 h4 h5
          · exact layer2_absorb_8_6 S hxS h9 h4 h5 hmS
    · by_cases h9 : (9 : Fin 15) ∈ S
      · exact layer2_absorb_8_9 S hxS h9
      · by_cases h4 : (4 : Fin 15) ∈ S
        · exact layer2_absorb_8_4 S hxS h9 h4
        · by_cases h5 : (5 : Fin 15) ∈ S
          · exact layer2_absorb_8_5 S hxS h9 h4 h5
          · by_cases h6 : (6 : Fin 15) ∈ S
            · exact layer2_absorb_8_6 S hxS h9 h4 h5 h6
            · exact layer2_absorb_8_7 S hxS h9 h4 h5 h6 hmS
    · contradiction
    · exact layer2_absorb_8_9 S hxS hmS
  · rcases hS with ⟨m, hml, hmS⟩
    simp [layer2] at hml
    rcases hml with rfl | rfl | rfl | rfl | rfl | rfl
    · exact layer2_absorb_9_4 S hxS hmS
    · by_cases h4 : (4 : Fin 15) ∈ S
      · exact layer2_absorb_9_4 S hxS h4
      · exact layer2_absorb_9_5 S hxS h4 hmS
    · by_cases h4 : (4 : Fin 15) ∈ S
      · exact layer2_absorb_9_4 S hxS h4
      · by_cases h5 : (5 : Fin 15) ∈ S
        · exact layer2_absorb_9_5 S hxS h4 h5
        · exact layer2_absorb_9_6 S hxS h4 h5 hmS
    · by_cases h4 : (4 : Fin 15) ∈ S
      · exact layer2_absorb_9_4 S hxS h4
      · by_cases h5 : (5 : Fin 15) ∈ S
        · exact layer2_absorb_9_5 S hxS h4 h5
        · by_cases h6 : (6 : Fin 15) ∈ S
          · exact layer2_absorb_9_6 S hxS h4 h5 h6
          · exact layer2_absorb_9_7 S hxS h4 h5 h6 hmS
    · by_cases h4 : (4 : Fin 15) ∈ S
      · exact layer2_absorb_9_4 S hxS h4
      · by_cases h5 : (5 : Fin 15) ∈ S
        · exact layer2_absorb_9_5 S hxS h4 h5
        · by_cases h6 : (6 : Fin 15) ∈ S
          · exact layer2_absorb_9_6 S hxS h4 h5 h6
          · by_cases h7 : (7 : Fin 15) ∈ S
            · exact layer2_absorb_9_7 S hxS h4 h5 h6 h7
            · exact layer2_absorb_9_8 S hxS h4 h5 h6 h7 hmS
    · contradiction

/-- 层覆盖：每个窗口属于恰好一个谱层（层 1..4）。 -/
lemma layer_cover (x : Fin 15) : x ∈ layer1 ∨ x ∈ layer2 ∨ x ∈ layer3 ∨ x ∈ layer4 := by
  fin_cases x <;> simp [layer1, layer2, layer3, layer4]

/-- 层 1 循环闭合：完全活跃层 1（4 窗）经 4 步回到自身。 -/
lemma layer_cycle1 (S : Finset (Fin 15)) (x : Fin 15) (hx : x ∈ layer1)
    (hLe : layer1 ∩ S = ∅) : (silentStep S)^[4] x = x := by
  simp [layer1] at hx
  rcases hx with rfl | rfl | rfl | rfl
  · have h0S : (0 : Fin 15) ∉ S := by
      intro h0
      have : (0 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h0⟩
      have : (0 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h1S : (1 : Fin 15) ∉ S := by
      intro h1
      have : (1 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h1⟩
      have : (1 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h2S : (2 : Fin 15) ∉ S := by
      intro h2
      have : (2 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h2⟩
      have : (2 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h3S : (3 : Fin 15) ∉ S := by
      intro h3
      have : (3 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h3⟩
      have : (3 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (0 : Fin 15)))) = (0 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S, h1S, h2S, h3S]
  · have h0S : (0 : Fin 15) ∉ S := by
      intro h0
      have : (0 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h0⟩
      have : (0 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h1S : (1 : Fin 15) ∉ S := by
      intro h1
      have : (1 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h1⟩
      have : (1 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h2S : (2 : Fin 15) ∉ S := by
      intro h2
      have : (2 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h2⟩
      have : (2 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h3S : (3 : Fin 15) ∉ S := by
      intro h3
      have : (3 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h3⟩
      have : (3 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (1 : Fin 15)))) = (1 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S, h1S, h2S, h3S]
  · have h0S : (0 : Fin 15) ∉ S := by
      intro h0
      have : (0 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h0⟩
      have : (0 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h1S : (1 : Fin 15) ∉ S := by
      intro h1
      have : (1 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h1⟩
      have : (1 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h2S : (2 : Fin 15) ∉ S := by
      intro h2
      have : (2 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h2⟩
      have : (2 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h3S : (3 : Fin 15) ∉ S := by
      intro h3
      have : (3 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h3⟩
      have : (3 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (2 : Fin 15)))) = (2 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S, h1S, h2S, h3S]
  · have h0S : (0 : Fin 15) ∉ S := by
      intro h0
      have : (0 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h0⟩
      have : (0 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h1S : (1 : Fin 15) ∉ S := by
      intro h1
      have : (1 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h1⟩
      have : (1 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h2S : (2 : Fin 15) ∉ S := by
      intro h2
      have : (2 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h2⟩
      have : (2 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h3S : (3 : Fin 15) ∉ S := by
      intro h3
      have : (3 : Fin 15) ∈ layer1 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer1], h3⟩
      have : (3 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (3 : Fin 15)))) = (3 : Fin 15)
    simp [silentStep, layeredStep, layer1, h0S, h1S, h2S, h3S]
/-- 层 2 循环闭合：完全活跃层 2（6 窗）经 6 步回到自身 -/
lemma layer_cycle2 (S : Finset (Fin 15)) (x : Fin 15) (hx : x ∈ layer2)
    (hLe : layer2 ∩ S = ∅) : (silentStep S)^[6] x = x := by
  simp [layer2] at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl
  ·
    have h4S : (4 : Fin 15) ∉ S := by
      intro h4
      have : (4 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h4⟩
      have : (4 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h5S : (5 : Fin 15) ∉ S := by
      intro h5
      have : (5 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h5⟩
      have : (5 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h6S : (6 : Fin 15) ∉ S := by
      intro h6
      have : (6 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h6⟩
      have : (6 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h7S : (7 : Fin 15) ∉ S := by
      intro h7
      have : (7 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h7⟩
      have : (7 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h8S : (8 : Fin 15) ∉ S := by
      intro h8
      have : (8 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h8⟩
      have : (8 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h9S : (9 : Fin 15) ∉ S := by
      intro h9
      have : (9 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h9⟩
      have : (9 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((4 : Fin 15))))))) = (4 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
  ·
    have h4S : (4 : Fin 15) ∉ S := by
      intro h4
      have : (4 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h4⟩
      have : (4 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h5S : (5 : Fin 15) ∉ S := by
      intro h5
      have : (5 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h5⟩
      have : (5 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h6S : (6 : Fin 15) ∉ S := by
      intro h6
      have : (6 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h6⟩
      have : (6 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h7S : (7 : Fin 15) ∉ S := by
      intro h7
      have : (7 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h7⟩
      have : (7 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h8S : (8 : Fin 15) ∉ S := by
      intro h8
      have : (8 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h8⟩
      have : (8 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h9S : (9 : Fin 15) ∉ S := by
      intro h9
      have : (9 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h9⟩
      have : (9 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((5 : Fin 15))))))) = (5 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
  ·
    have h4S : (4 : Fin 15) ∉ S := by
      intro h4
      have : (4 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h4⟩
      have : (4 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h5S : (5 : Fin 15) ∉ S := by
      intro h5
      have : (5 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h5⟩
      have : (5 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h6S : (6 : Fin 15) ∉ S := by
      intro h6
      have : (6 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h6⟩
      have : (6 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h7S : (7 : Fin 15) ∉ S := by
      intro h7
      have : (7 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h7⟩
      have : (7 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h8S : (8 : Fin 15) ∉ S := by
      intro h8
      have : (8 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h8⟩
      have : (8 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h9S : (9 : Fin 15) ∉ S := by
      intro h9
      have : (9 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h9⟩
      have : (9 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((6 : Fin 15))))))) = (6 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
  ·
    have h4S : (4 : Fin 15) ∉ S := by
      intro h4
      have : (4 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h4⟩
      have : (4 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h5S : (5 : Fin 15) ∉ S := by
      intro h5
      have : (5 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h5⟩
      have : (5 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h6S : (6 : Fin 15) ∉ S := by
      intro h6
      have : (6 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h6⟩
      have : (6 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h7S : (7 : Fin 15) ∉ S := by
      intro h7
      have : (7 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h7⟩
      have : (7 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h8S : (8 : Fin 15) ∉ S := by
      intro h8
      have : (8 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h8⟩
      have : (8 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h9S : (9 : Fin 15) ∉ S := by
      intro h9
      have : (9 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h9⟩
      have : (9 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((7 : Fin 15))))))) = (7 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
  ·
    have h4S : (4 : Fin 15) ∉ S := by
      intro h4
      have : (4 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h4⟩
      have : (4 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h5S : (5 : Fin 15) ∉ S := by
      intro h5
      have : (5 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h5⟩
      have : (5 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h6S : (6 : Fin 15) ∉ S := by
      intro h6
      have : (6 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h6⟩
      have : (6 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h7S : (7 : Fin 15) ∉ S := by
      intro h7
      have : (7 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h7⟩
      have : (7 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h8S : (8 : Fin 15) ∉ S := by
      intro h8
      have : (8 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h8⟩
      have : (8 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h9S : (9 : Fin 15) ∉ S := by
      intro h9
      have : (9 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h9⟩
      have : (9 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((8 : Fin 15))))))) = (8 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
  ·
    have h4S : (4 : Fin 15) ∉ S := by
      intro h4
      have : (4 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h4⟩
      have : (4 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h5S : (5 : Fin 15) ∉ S := by
      intro h5
      have : (5 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h5⟩
      have : (5 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h6S : (6 : Fin 15) ∉ S := by
      intro h6
      have : (6 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h6⟩
      have : (6 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h7S : (7 : Fin 15) ∉ S := by
      intro h7
      have : (7 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h7⟩
      have : (7 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h8S : (8 : Fin 15) ∉ S := by
      intro h8
      have : (8 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h8⟩
      have : (8 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h9S : (9 : Fin 15) ∉ S := by
      intro h9
      have : (9 : Fin 15) ∈ layer2 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer2], h9⟩
      have : (9 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (silentStep S ((9 : Fin 15))))))) = (9 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]

/-- 层 3 循环闭合：完全活跃层 3（4 窗）经 4 步回到自身 -/
lemma layer_cycle3 (S : Finset (Fin 15)) (x : Fin 15) (hx : x ∈ layer3)
    (hLe : layer3 ∩ S = ∅) : (silentStep S)^[4] x = x := by
  simp [layer3] at hx
  rcases hx with rfl | rfl | rfl | rfl
  ·
    have h10S : (10 : Fin 15) ∉ S := by
      intro h10
      have : (10 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h10⟩
      have : (10 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h11S : (11 : Fin 15) ∉ S := by
      intro h11
      have : (11 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h11⟩
      have : (11 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h12S : (12 : Fin 15) ∉ S := by
      intro h12
      have : (12 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h12⟩
      have : (12 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h13S : (13 : Fin 15) ∉ S := by
      intro h13
      have : (13 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h13⟩
      have : (13 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S ((10 : Fin 15))))) = (10 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]
  ·
    have h10S : (10 : Fin 15) ∉ S := by
      intro h10
      have : (10 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h10⟩
      have : (10 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h11S : (11 : Fin 15) ∉ S := by
      intro h11
      have : (11 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h11⟩
      have : (11 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h12S : (12 : Fin 15) ∉ S := by
      intro h12
      have : (12 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h12⟩
      have : (12 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h13S : (13 : Fin 15) ∉ S := by
      intro h13
      have : (13 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h13⟩
      have : (13 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S ((11 : Fin 15))))) = (11 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]
  ·
    have h10S : (10 : Fin 15) ∉ S := by
      intro h10
      have : (10 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h10⟩
      have : (10 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h11S : (11 : Fin 15) ∉ S := by
      intro h11
      have : (11 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h11⟩
      have : (11 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h12S : (12 : Fin 15) ∉ S := by
      intro h12
      have : (12 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h12⟩
      have : (12 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h13S : (13 : Fin 15) ∉ S := by
      intro h13
      have : (13 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h13⟩
      have : (13 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S ((12 : Fin 15))))) = (12 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]
  ·
    have h10S : (10 : Fin 15) ∉ S := by
      intro h10
      have : (10 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h10⟩
      have : (10 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h11S : (11 : Fin 15) ∉ S := by
      intro h11
      have : (11 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h11⟩
      have : (11 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h12S : (12 : Fin 15) ∉ S := by
      intro h12
      have : (12 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h12⟩
      have : (12 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    have h13S : (13 : Fin 15) ∉ S := by
      intro h13
      have : (13 : Fin 15) ∈ layer3 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer3], h13⟩
      have : (13 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S (silentStep S (silentStep S (silentStep S ((13 : Fin 15))))) = (13 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]

/-- 层 4 循环闭合：完全活跃层 4（单窗 14）一步不动 -/
lemma layer_cycle4 (S : Finset (Fin 15)) (x : Fin 15) (hx : x ∈ layer4)
    (hLe : layer4 ∩ S = ∅) : (silentStep S)^[1] x = x := by
  simp [layer4] at hx
  rcases hx with rfl
  ·
    have h14S : (14 : Fin 15) ∉ S := by
      intro h14
      have : (14 : Fin 15) ∈ layer4 ∩ S := by exact Finset.mem_inter.mpr ⟨by simp [layer4], h14⟩
      have : (14 : Fin 15) ∈ (∅ : Finset (Fin 15)) := by simpa [hLe] using this
      simpa using this
    change silentStep S ((14 : Fin 15)) = (14 : Fin 15)
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h14S]

/-- 谱层集合（层 1..4）。 -/
def layers : Finset (Finset (Fin 15)) :=
  insert layer1 (insert layer2 (insert layer3 (insert layer4 (∅ : Finset (Finset (Fin 15))))))

/-- 周期点刻画：x 是静默模型周期点 ⟺ x 已静默（单点不动）或 x 所在谱层完全活跃（层循环）。 -/
lemma periodicPoint_iff (S : Finset (Fin 15)) (x : Fin 15) :
    periodicPoint (silenceRec15_layered S) x ↔ x ∈ S ∨ ∃ L ∈ layers, x ∈ L ∧ L ∩ S = ∅ := by
  constructor
  · intro hx
    rcases hx with ⟨p, hp, hxp⟩
    by_cases hxS : x ∈ S
    · exact Or.inl hxS
    · right
      rcases layer_cover x with hx1 | hx2 | hx3 | hx4
      · refine ⟨layer1, by simp [layers], hx1, ?_⟩
        by_contra hne
        rcases (Finset.nonempty_iff_ne_empty.mpr hne) with ⟨m, hm⟩
        rcases (Finset.mem_inter.mp hm) with ⟨hmL, hmS⟩
        exact (layer1_partial_silent_not_periodic S hx1 hxS ⟨m, hmL, hmS⟩) ⟨p, hp, hxp⟩
      · refine ⟨layer2, by simp [layers], hx2, ?_⟩
        by_contra hne
        rcases (Finset.nonempty_iff_ne_empty.mpr hne) with ⟨m, hm⟩
        rcases (Finset.mem_inter.mp hm) with ⟨hmL, hmS⟩
        exact (layer2_partial_silent_not_periodic S hx2 ⟨m, hmL, hmS⟩ hxS) ⟨p, hp, hxp⟩
      · refine ⟨layer3, by simp [layers], hx3, ?_⟩
        by_contra hne
        rcases (Finset.nonempty_iff_ne_empty.mpr hne) with ⟨m, hm⟩
        rcases (Finset.mem_inter.mp hm) with ⟨hmL, hmS⟩
        exact (layer3_partial_silent_not_periodic S hx3 hxS ⟨m, hmL, hmS⟩) ⟨p, hp, hxp⟩
      · refine ⟨layer4, by simp [layers], hx4, ?_⟩
        by_contra hne
        rcases (Finset.nonempty_iff_ne_empty.mpr hne) with ⟨m, hm⟩
        have hm14 : m = (14 : Fin 15) := by simpa [layer4] using (Finset.mem_inter.mp hm).1
        have h14S : (14 : Fin 15) ∈ S := by simpa [hm14] using (Finset.mem_inter.mp hm).2
        have hx14 : x = (14 : Fin 15) := by simpa [layer4] using hx4
        exact hxS (by simpa [hx14] using h14S)
  · intro h
    rcases h with hxS | ⟨L, hLmem, hxL, hLem⟩
    · refine ⟨1, by omega, ?_⟩
      change (silenceRec15_layered S).step x = x
      rw [silenceRec15_layered_step, silentStep]
      simp [hxS]
      rfl
    · simp [layers] at hLmem
      rcases hLmem with rfl | rfl | rfl | rfl
      · refine ⟨4, by omega, ?_⟩
        change (silentStep S)^[4] x = x
        exact layer_cycle1 S x hxL hLem
      · refine ⟨6, by omega, ?_⟩
        change (silentStep S)^[6] x = x
        exact layer_cycle2 S x hxL hLem
      · refine ⟨4, by omega, ?_⟩
        change (silentStep S)^[4] x = x
        exact layer_cycle3 S x hxL hLem
      · refine ⟨1, by omega, ?_⟩
        change (silentStep S)^[1] x = x
        exact layer_cycle4 S x hxL hLem

/-- 辅助：完全活跃层（L∩S=∅）内元素必不在 S 中。 -/
lemma layer_mem_not_in_S_of_disjoint (S : Finset (Fin 15)) {L : Finset (Fin 15)}
    {a : Fin 15} (ha : a ∈ L) (hLe : L ∩ S = ∅) : a ∉ S := by
  intro hS
  have : a ∈ L ∩ S := Finset.mem_inter.mpr ⟨ha, hS⟩
  simpa [hLe] using this

/-- 层 1 全元素不在 S（层 1 完全活跃）。 -/
lemma layer1_disjoint_all (S : Finset (Fin 15)) (hLe : layer1 ∩ S = ∅) :
    (0 : Fin 15) ∉ S ∧ (1 : Fin 15) ∉ S ∧ (2 : Fin 15) ∉ S ∧ (3 : Fin 15) ∉ S := by
  constructor
  · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) hLe
  · constructor
    · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) hLe
    · constructor
      · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) hLe
      · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) hLe

/-- 层 2 全元素不在 S（层 2 完全活跃）。 -/
lemma layer2_disjoint_all (S : Finset (Fin 15)) (hLe : layer2 ∩ S = ∅) :
    (4 : Fin 15) ∉ S ∧ (5 : Fin 15) ∉ S ∧ (6 : Fin 15) ∉ S ∧ (7 : Fin 15) ∉ S
      ∧ (8 : Fin 15) ∉ S ∧ (9 : Fin 15) ∉ S := by
  constructor
  · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) hLe
  · constructor
    · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) hLe
    · constructor
      · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) hLe
      · constructor
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) hLe
        · constructor
          · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) hLe
          · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) hLe

/-- 层 3 全元素不在 S（层 3 完全活跃）。 -/
lemma layer3_disjoint_all (S : Finset (Fin 15)) (hLe : layer3 ∩ S = ∅) :
    (10 : Fin 15) ∉ S ∧ (11 : Fin 15) ∉ S ∧ (12 : Fin 15) ∉ S ∧ (13 : Fin 15) ∉ S := by
  constructor
  · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) hLe
  · constructor
    · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) hLe
    · constructor
      · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) hLe
      · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) hLe

/-- 层 4 唯一元素不在 S（层 4 完全活跃）。 -/
lemma layer4_disjoint_all (S : Finset (Fin 15)) (hLe : layer4 ∩ S = ∅) :
    (14 : Fin 15) ∉ S := by
  exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) hLe

/-- 层 1 单步封闭：完全活跃层 1 内元素的 silentStep 仍在层 1。 -/
lemma layer1_step_mem (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer1)
    (hLe : layer1 ∩ S = ∅) : silentStep S x ∈ layer1 := by
  simp [layer1] at hx
  rcases hx with rfl | rfl | rfl | rfl
  all_goals
    rcases layer1_disjoint_all S hLe with ⟨h0S, h1S, h2S, h3S⟩
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h0S, h1S, h2S, h3S]

/-- 层 2 单步封闭。 -/
lemma layer2_step_mem (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer2)
    (hLe : layer2 ∩ S = ∅) : silentStep S x ∈ layer2 := by
  simp [layer2] at hx
  rcases hx with rfl | rfl | rfl | rfl | rfl | rfl
  all_goals
    rcases layer2_disjoint_all S hLe with ⟨h4S, h5S, h6S, h7S, h8S, h9S⟩
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]

/-- 层 3 单步封闭。 -/
lemma layer3_step_mem (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer3)
    (hLe : layer3 ∩ S = ∅) : silentStep S x ∈ layer3 := by
  simp [layer3] at hx
  rcases hx with rfl | rfl | rfl | rfl
  all_goals
    rcases layer3_disjoint_all S hLe with ⟨h10S, h11S, h12S, h13S⟩
    simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]

/-- 层 4 单步封闭（14 不动）。 -/
lemma layer4_step_mem (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer4)
    (hLe : layer4 ∩ S = ∅) : silentStep S x ∈ layer4 := by
  simp [layer4] at hx
  rcases hx with rfl
  have h14S : (14 : Fin 15) ∉ S := layer4_disjoint_all S hLe
  simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h14S]

/-- 层 1 迭代封闭：完全活跃层 1 内元素任意步迭代仍在层 1。 -/
lemma layer1_closed (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer1)
    (hLe : layer1 ∩ S = ∅) : ∀ n : ℕ, (silentStep S)^[n] x ∈ layer1 := by
  intro n
  induction n with
  | zero => simpa using hx
  | succ n ih =>
    simpa [Function.iterate_succ_apply'] using layer1_step_mem S ih hLe

/-- 层 2 迭代封闭。 -/
lemma layer2_closed (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer2)
    (hLe : layer2 ∩ S = ∅) : ∀ n : ℕ, (silentStep S)^[n] x ∈ layer2 := by
  intro n
  induction n with
  | zero => simpa using hx
  | succ n ih =>
    simpa [Function.iterate_succ_apply'] using layer2_step_mem S ih hLe

/-- 层 3 迭代封闭。 -/
lemma layer3_closed (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer3)
    (hLe : layer3 ∩ S = ∅) : ∀ n : ℕ, (silentStep S)^[n] x ∈ layer3 := by
  intro n
  induction n with
  | zero => simpa using hx
  | succ n ih =>
    simpa [Function.iterate_succ_apply'] using layer3_step_mem S ih hLe

/-- 层 4 迭代封闭。 -/
lemma layer4_closed (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ layer4)
    (hLe : layer4 ∩ S = ∅) : ∀ n : ℕ, (silentStep S)^[n] x ∈ layer4 := by
  intro n
  induction n with
  | zero => simpa using hx
  | succ n ih =>
    simpa [Function.iterate_succ_apply'] using layer4_step_mem S ih hLe

/-- 辅助：S 元素不在完全活跃层 L 中。 -/
lemma S_mem_not_in_layer_of_disjoint (S : Finset (Fin 15)) {L : Finset (Fin 15)}
    {a : Fin 15} (ha : a ∈ S) (hLe : L ∩ S = ∅) : a ∉ L := by
  intro hL
  have : a ∈ L ∩ S := Finset.mem_inter.mpr ⟨hL, ha⟩
  simpa [hLe] using this

/-- RecObj.step 与 silentStep 的迭代定义性相等（桥）。 -/
lemma silenceRec15_layered_iterate (S : Finset (Fin 15)) (n : ℕ) (x : Fin 15) :
    (silenceRec15_layered S).step^[n] x = (silentStep S)^[n] x := by
  rfl

/-- 静默点任意迭代保持不动。 -/
lemma silent_fix_iterate (S : Finset (Fin 15)) {r : Fin 15} (hr : r ∈ S) :
    ∀ n : ℕ, (silenceRec15_layered S).step^[n] r = r := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    have h₁ : (silenceRec15_layered S).step^[n + 1] r
        = (silenceRec15_layered S).step^[n] ((silenceRec15_layered S).step r) := by
      simpa using (Function.iterate_add_apply (silenceRec15_layered S).step n 1 r)
    have h₂ : (silenceRec15_layered S).step^[n] ((silenceRec15_layered S).step r)
        = (silenceRec15_layered S).step^[n] r := by
      rw [silenceRec15_layered_step, silentStep]
      simp [hr]
    exact h₁.trans (h₂.trans ih)

/-- 轨道代表集：静默窗全部元素 + 每完全活跃层一个代表。 -/
def orbitRepSet (S : Finset (Fin 15)) : Finset (Fin 15) :=
  S ∪ (if layer1 ∩ S = ∅ then {(0 : Fin 15)} else ∅) ∪
    (if layer2 ∩ S = ∅ then {(4 : Fin 15)} else ∅) ∪
    (if layer3 ∩ S = ∅ then {(10 : Fin 15)} else ∅) ∪
    (if layer4 ∩ S = ∅ then {(14 : Fin 15)} else ∅)

/-- 代表集成员分解。 -/
lemma orbitRepSet_mem_iff (S : Finset (Fin 15)) (r : Fin 15) : r ∈ orbitRepSet S ↔
    r ∈ S ∨ (layer1 ∩ S = ∅ ∧ r = (0 : Fin 15)) ∨
    (layer2 ∩ S = ∅ ∧ r = (4 : Fin 15)) ∨
    (layer3 ∩ S = ∅ ∧ r = (10 : Fin 15)) ∨
    (layer4 ∩ S = ∅ ∧ r = (14 : Fin 15)) := by
  unfold orbitRepSet
  by_cases h1 : layer1 ∩ S = ∅ <;> by_cases h2 : layer2 ∩ S = ∅ <;>
    by_cases h3 : layer3 ∩ S = ∅ <;> by_cases h4 : layer4 ∩ S = ∅ <;>
      simp [h1, h2, h3, h4, Finset.mem_singleton] <;> tauto

/-- 代表集元素都是周期点。 -/
lemma orbitRepSet_per (S : Finset (Fin 15)) (r : Fin 15) (hr : r ∈ orbitRepSet S) :
    periodicPoint (silenceRec15_layered S) r := by
  rcases (orbitRepSet_mem_iff S r).mp hr with hS | h1 | h2 | h3 | h4
  · refine ⟨1, by omega, ?_⟩
    change (silenceRec15_layered S).step r = r
    rw [silenceRec15_layered_step, silentStep]
    simp [hS]
    rfl
  · rcases h1 with ⟨hLe, rfl⟩
    refine ⟨4, by omega, ?_⟩
    change (silentStep S)^[4] (0 : Fin 15) = (0 : Fin 15)
    exact layer_cycle1 S (0 : Fin 15) (by simp [layer1]) hLe
  · rcases h2 with ⟨hLe, rfl⟩
    refine ⟨6, by omega, ?_⟩
    change (silentStep S)^[6] (4 : Fin 15) = (4 : Fin 15)
    exact layer_cycle2 S (4 : Fin 15) (by simp [layer2]) hLe
  · rcases h3 with ⟨hLe, rfl⟩
    refine ⟨4, by omega, ?_⟩
    change (silentStep S)^[4] (10 : Fin 15) = (10 : Fin 15)
    exact layer_cycle3 S (10 : Fin 15) (by simp [layer3]) hLe
  · rcases h4 with ⟨hLe, rfl⟩
    refine ⟨1, by omega, ?_⟩
    change (silentStep S)^[1] (14 : Fin 15) = (14 : Fin 15)
    exact layer_cycle4 S (14 : Fin 15) (by simp [layer4]) hLe

/-- 代表集存在性：每周期点可达某代表。 -/
lemma orbitRepSet_surj (S : Finset (Fin 15)) (x : Fin 15)
    (hx : periodicPoint (silenceRec15_layered S) x) :
    ∃ r : Fin 15, ∃ hr : r ∈ orbitRepSet S,
      periodOrbitRel (silenceRec15_layered S) ⟨x, hx⟩ ⟨r, orbitRepSet_per S r hr⟩ := by
  rcases (periodicPoint_iff S x).mp hx with hxS | ⟨L, hLmem, hxL, hLem⟩
  · refine ⟨x, (orbitRepSet_mem_iff S x).mpr (Or.inl hxS), ⟨0, rfl⟩⟩
  · simp [layers] at hLmem
    rcases hLmem with rfl | rfl | rfl | rfl
    · refine ⟨(0 : Fin 15), (orbitRepSet_mem_iff S (0 : Fin 15)).mpr
        (Or.inr (Or.inl ⟨hLem, rfl⟩)), ?_⟩
      rcases layer1_disjoint_all S hLem with ⟨h0S, h1S, h2S, h3S⟩
      simp [layer1] at hxL
      rcases hxL with rfl | rfl | rfl | rfl
      · exact ⟨0, rfl⟩
      · refine ⟨3, ?_⟩
        change silentStep S (silentStep S (silentStep S (1 : Fin 15))) = (0 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h0S, h1S, h2S, h3S]
      · refine ⟨2, ?_⟩
        change silentStep S (silentStep S (2 : Fin 15)) = (0 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h0S, h1S, h2S, h3S]
      · refine ⟨1, ?_⟩
        change silentStep S (3 : Fin 15) = (0 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h0S, h1S, h2S, h3S]
    · refine ⟨(4 : Fin 15), (orbitRepSet_mem_iff S (4 : Fin 15)).mpr
        (Or.inr (Or.inr (Or.inl ⟨hLem, rfl⟩))), ?_⟩
      rcases layer2_disjoint_all S hLem with ⟨h4S, h5S, h6S, h7S, h8S, h9S⟩
      simp [layer2] at hxL
      rcases hxL with rfl | rfl | rfl | rfl | rfl | rfl
      · exact ⟨0, rfl⟩
      · refine ⟨5, ?_⟩
        change silentStep S (silentStep S (silentStep S (silentStep S (silentStep S (5 : Fin 15))))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
      · refine ⟨4, ?_⟩
        change silentStep S (silentStep S (silentStep S (silentStep S (6 : Fin 15)))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
      · refine ⟨3, ?_⟩
        change silentStep S (silentStep S (silentStep S (7 : Fin 15))) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
      · refine ⟨2, ?_⟩
        change silentStep S (silentStep S (8 : Fin 15)) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
      · refine ⟨1, ?_⟩
        change silentStep S (9 : Fin 15) = (4 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h4S, h5S, h6S, h7S, h8S, h9S]
    · refine ⟨(10 : Fin 15), (orbitRepSet_mem_iff S (10 : Fin 15)).mpr
        (Or.inr (Or.inr (Or.inr (Or.inl ⟨hLem, rfl⟩)))), ?_⟩
      rcases layer3_disjoint_all S hLem with ⟨h10S, h11S, h12S, h13S⟩
      simp [layer3] at hxL
      rcases hxL with rfl | rfl | rfl | rfl
      · exact ⟨0, rfl⟩
      · refine ⟨3, ?_⟩
        change silentStep S (silentStep S (silentStep S (11 : Fin 15))) = (10 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]
      · refine ⟨2, ?_⟩
        change silentStep S (silentStep S (12 : Fin 15)) = (10 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]
      · refine ⟨1, ?_⟩
        change silentStep S (13 : Fin 15) = (10 : Fin 15)
        simp [silentStep, layeredStep, layer1, layer2, layer3, layer4, h10S, h11S, h12S, h13S]
    · refine ⟨(14 : Fin 15), (orbitRepSet_mem_iff S (14 : Fin 15)).mpr
        (Or.inr (Or.inr (Or.inr (Or.inr ⟨hLem, rfl⟩)))), ?_⟩
      simp [layer4] at hxL
      rcases hxL with rfl
      exact ⟨0, rfl⟩

/-- 代表集唯一性：不同代表不等价。 -/
lemma orbitRepSet_inj (S : Finset (Fin 15)) (r₁ : Fin 15) (hr₁ : r₁ ∈ orbitRepSet S)
    (r₂ : Fin 15) (hr₂ : r₂ ∈ orbitRepSet S) (hne : r₁ ≠ r₂) :
    ¬ periodOrbitRel (silenceRec15_layered S) ⟨r₁, orbitRepSet_per S r₁ hr₁⟩
      ⟨r₂, orbitRepSet_per S r₂ hr₂⟩ := by
  rcases (orbitRepSet_mem_iff S r₁).mp hr₁ with hS1 | h11 | h21 | h31 | h41
  · intro hrel
    rcases hrel with ⟨n, hn⟩
    have hfix : (silenceRec15_layered S).step^[n] r₁ = r₁ := silent_fix_iterate S hS1 n
    exact hne (hfix.symm.trans hn)
  · rcases h11 with ⟨hLe1, rfl⟩
    intro hrel
    rcases hrel with ⟨n, hn⟩
    have hcl : (silentStep S)^[n] (0 : Fin 15) ∈ layer1 := layer1_closed S (by simp [layer1]) hLe1 n
    rw [← silenceRec15_layered_iterate] at hcl
    rcases (orbitRepSet_mem_iff S r₂).mp hr₂ with hS2 | h12 | h22 | h32 | h42
    · exact (S_mem_not_in_layer_of_disjoint S hS2 hLe1) (by simpa [hn] using hcl)
    · rcases h12 with ⟨_, hEq⟩
      exact hne (by simpa [hEq])
    · rcases h22 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer1 := by simp [layer1, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h32 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer1 := by simp [layer1, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h42 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer1 := by simp [layer1, hEq]
      exact hr2L (by simpa [hn] using hcl)
  · rcases h21 with ⟨hLe2, rfl⟩
    intro hrel
    rcases hrel with ⟨n, hn⟩
    have hcl : (silentStep S)^[n] (4 : Fin 15) ∈ layer2 := layer2_closed S (by simp [layer2]) hLe2 n
    rw [← silenceRec15_layered_iterate] at hcl
    rcases (orbitRepSet_mem_iff S r₂).mp hr₂ with hS2 | h12 | h22 | h32 | h42
    · exact (S_mem_not_in_layer_of_disjoint S hS2 hLe2) (by simpa [hn] using hcl)
    · rcases h12 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer2 := by simp [layer2, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h22 with ⟨_, hEq⟩
      exact hne (by simpa [hEq])
    · rcases h32 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer2 := by simp [layer2, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h42 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer2 := by simp [layer2, hEq]
      exact hr2L (by simpa [hn] using hcl)
  · rcases h31 with ⟨hLe3, rfl⟩
    intro hrel
    rcases hrel with ⟨n, hn⟩
    have hcl : (silentStep S)^[n] (10 : Fin 15) ∈ layer3 := layer3_closed S (by simp [layer3]) hLe3 n
    rw [← silenceRec15_layered_iterate] at hcl
    rcases (orbitRepSet_mem_iff S r₂).mp hr₂ with hS2 | h12 | h22 | h32 | h42
    · exact (S_mem_not_in_layer_of_disjoint S hS2 hLe3) (by simpa [hn] using hcl)
    · rcases h12 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer3 := by simp [layer3, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h22 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer3 := by simp [layer3, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h32 with ⟨_, hEq⟩
      exact hne (by simpa [hEq])
    · rcases h42 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer3 := by simp [layer3, hEq]
      exact hr2L (by simpa [hn] using hcl)
  · rcases h41 with ⟨hLe4, rfl⟩
    intro hrel
    rcases hrel with ⟨n, hn⟩
    have hcl : (silentStep S)^[n] (14 : Fin 15) ∈ layer4 := layer4_closed S (by simp [layer4]) hLe4 n
    rw [← silenceRec15_layered_iterate] at hcl
    rcases (orbitRepSet_mem_iff S r₂).mp hr₂ with hS2 | h12 | h22 | h32 | h42
    · exact (S_mem_not_in_layer_of_disjoint S hS2 hLe4) (by simpa [hn] using hcl)
    · rcases h12 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer4 := by simp [layer4, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h22 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer4 := by simp [layer4, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h32 with ⟨_, hEq⟩
      have hr2L : r₂ ∉ layer4 := by simp [layer4, hEq]
      exact hr2L (by simpa [hn] using hcl)
    · rcases h42 with ⟨_, hEq⟩
      exact hne (by simpa [hEq])

/-- foldl 单例并集计数：互异且均不在 S 的列表元素逐个并入后，card = S.card + 长度。 -/
lemma card_union_singleton_foldl (S : Finset (Fin 15)) (A : List (Fin 15))
    (hA_perp : ∀ a ∈ A, a ∉ S) (hA_nodup : A.Nodup) :
    (List.foldl (fun acc a => acc ∪ {a}) S A).card = S.card + A.length := by
  induction A generalizing S with
  | nil => simp
  | cons a A ih =>
    rcases (List.nodup_cons.mp hA_nodup) with ⟨haA, hA_nodup'⟩
    have haS : a ∉ S := hA_perp a (by simp)
    have h₁ : (S ∪ {a}).card = S.card + 1 := by
      rw [Finset.card_union_of_disjoint]
      · simp
      · rw [Finset.disjoint_left]
        intro x hxS hxa
        simp at hxa
        exact haS (by simpa [hxa] using hxS)
    have hperp' : ∀ b ∈ A, b ∉ S ∪ {a} := by
      intro b hb hbU
      rw [Finset.mem_union] at hbU
      rcases hbU with hbS | hba
      · exact hA_perp b (by simp [hb]) hbS
      · exact haA (by rw [Finset.mem_singleton.mp hba] at hb; exact hb)
    calc
      (List.foldl (fun acc a => acc ∪ {a}) S (a :: A)).card
          = (List.foldl (fun acc a => acc ∪ {a}) (S ∪ {a}) A).card := by rfl
      _ = (S ∪ {a}).card + A.length := ih (S ∪ {a}) hperp' hA_nodup'
      _ = S.card + 1 + A.length := by rw [h₁]
      _ = S.card + (a :: A).length := by simp [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

/-- 代表集大小：静默窗 + 完全活跃层数。 -/
lemma orbitRepSet_card (S : Finset (Fin 15)) : (orbitRepSet S).card = S.card + fullActiveCount S := by
  unfold fullActiveCount
  by_cases h1 : layer1 ∩ S = ∅ <;> by_cases h2 : layer2 ∩ S = ∅ <;>
    by_cases h3 : layer3 ∩ S = ∅ <;> by_cases h4 : layer4 ∩ S = ∅
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 4 (insert 10 (insert 14 (S)))) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 4, 10, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 4, 10, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl | rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 4 (insert 10 (S))) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 4, 10] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 4, 10] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 4 (insert 14 (S))) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 4, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 4, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 4 (S)) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 4] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 4] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 10 (insert 14 (S))) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 10, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 10, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 10 (S)) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 10] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 10] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (insert 14 (S)) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 0 (S) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [0] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [0] (by
        intro a ha; simp at ha; rcases ha with rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer1]) h1) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 4 (insert 10 (insert 14 (S))) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [4, 10, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [4, 10, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 4 (insert 10 (S)) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [4, 10] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [4, 10] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 4 (insert 14 (S)) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [4, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [4, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 4 (S) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [4] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [4] (by
        intro a ha; simp at ha; rcases ha with rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer2]) h2) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 10 (insert 14 (S)) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [10, 14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [10, 14] (by
        intro a ha; simp at ha; rcases ha with rfl | rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 10 (S) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [10] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [10] (by
        intro a ha; simp at ha; rcases ha with rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer3]) h3) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]
    rw [show (insert 14 (S) : Finset (Fin 15)) =
        List.foldl (fun acc a => acc ∪ {a}) S [14] by
      ext x
      simp [List.foldl, Finset.mem_union, Finset.mem_insert]]
    exact card_union_singleton_foldl S [14] (by
        intro a ha; simp at ha; rcases ha with rfl
        · exact layer_mem_not_in_S_of_disjoint S (by simp [layer4]) h4) (by decide)
  · simp [orbitRepSet, h1, h2, h3, h4]

/-- 通用商计数引理：若 Finset R 每周期轨道恰含一个代表，则 orbitCount = R.card。
    hR_per：R 中元素都是周期点；hR_surj：每周期点可达某代表；
    hR_inj：不同代表不等价。 -/
lemma orbitCount_eq_card {X : RecObj} (R : Finset X.T)
    (hR_per : ∀ r ∈ R, periodicPoint X r)
    (hR_surj : ∀ (x : X.T) (hx : periodicPoint X x),
      ∃ r : X.T, ∃ hr : r ∈ R, periodOrbitRel X ⟨x, hx⟩ ⟨r, hR_per r hr⟩)
    (hR_inj : ∀ (r₁ : X.T), ∀ hr₁ : r₁ ∈ R, ∀ (r₂ : X.T), ∀ hr₂ : r₂ ∈ R,
      r₁ ≠ r₂ → ¬ periodOrbitRel X ⟨r₁, hR_per r₁ hr₁⟩ ⟨r₂, hR_per r₂ hr₂⟩) :
    orbitCount X = R.card := by
  let f : {r : X.T // r ∈ R} → Quotient (periodOrbitSetoid X) :=
    fun r => Quotient.mk (periodOrbitSetoid X) ⟨r.1, hR_per r.1 r.2⟩
  have hf_inj : Function.Injective f := by
    intro r₁ r₂ hq
    apply Subtype.ext
    by_contra hne
    have hrel : periodOrbitRel X ⟨r₁.1, hR_per r₁.1 r₁.2⟩ ⟨r₂.1, hR_per r₂.1 r₂.2⟩ :=
      Quotient.exact hq
    exact hR_inj r₁.1 r₁.2 r₂.1 r₂.2 hne hrel
  have hf_surj : Function.Surjective f := by
    intro y
    rcases Quotient.exists_rep y with ⟨x, hx⟩
    rcases hR_surj x.1 x.2 with ⟨r, hr, hrel⟩
    refine ⟨⟨r, hr⟩, ?_⟩
    rw [← hx]
    apply Quotient.sound
    exact periodOrbitRel_symm X x ⟨r, hR_per r hr⟩ hrel
  calc
    orbitCount X = Fintype.card (Quotient (periodOrbitSetoid X)) := rfl
    _ = Fintype.card {r : X.T // r ∈ R} :=
      (Fintype.card_congr (Equiv.ofBijective f ⟨hf_inj, hf_surj⟩)).symm
    _ = R.card := by
      simpa using (Finset.card_coe R).symm

/-- 主定理：静默分层模型的周期轨道数 = 静默窗大小 + 完全活跃层数。
    含两端点：S=∅ → orbitCount = 4（无静默，每层一条循环轨道）；
    S=univ → orbitCount = 15（全静默，每点一条不动轨道）。 -/
theorem orbitCount_layered (S : Finset (Fin 15)) :
    orbitCount (silenceRec15_layered S) = S.card + fullActiveCount S := by
  rw [orbitCount_eq_card (orbitRepSet S) (orbitRepSet_per S) (orbitRepSet_surj S) (orbitRepSet_inj S)]
  exact orbitRepSet_card S

/-- ★ 5 静默单元链特例（候选 v1 的 Lean 级呈现，2026-10-24）：
    5 窗静默 ⟹ 5 个不动点单元 + 完全活跃层循环轨道
    （v2 公式 orbitCount = card S + fullActiveCount 的 card S = 5 实例；
    "静默单元" = 每静默窗一不动点轨道，与 15 = 3×5 的韦达根积同源桥分属两层：
    本定理 = 公式特例（迭代不动点语义），v1 的 3×5 = 代数同源（k_max 桥）。 -/
theorem orbitCount_layered_card_5 (S : Finset (Fin 15)) (hS : S.card = 5) :
    orbitCount (silenceRec15_layered S) = 5 + fullActiveCount S := by
  rw [orbitCount_layered, hS]











/-! ## 反向翻译精确化（2026-10-24，第③项补完）

主定理 `orbitCount_layered` 给出 orbitCount = S.card + fullActiveCount S。
反向问题：哪些静默窗配置给出 orbitCount = 15（g=15 的实现）？
数值穷举（scripts/verify_reverse_translation.py，2^15 全枚举 PASS）表明解集恰为
`S = univ ∨ S = univ.erase 14`：
- S = univ：全静默，15 条不动轨道（此前"全静默⟹15"定理）；
- S = univ.erase 14：除 14 外全静默——14 是层 4 的 1-周期天然不动点
  （layeredStep 14 = 14），无需静默即锁定，故"15 的实现"允许该特例。

即反向物理翻译的精确形态：**orbitCount=15 ⟺ 全锁定（恒等）⟺
S ⊇ univ.erase 14**——"15 不需要字面全静默，只要求除天然不动点 14 外全部静默"。
以下是 Lean 化（全部 exit 0 零 sorry）。
-/

/-- 层 1 与层 2 不相交。 -/
lemma layer1_disjoint_layer2 : layer1 ∩ layer2 = (∅ : Finset (Fin 15)) := by
  ext x
  fin_cases x <;> simp [layer1, layer2]


/-- 层 1 与层 3 不相交。 -/
lemma layer1_disjoint_layer3 : layer1 ∩ layer3 = (∅ : Finset (Fin 15)) := by
  ext x
  fin_cases x <;> simp [layer1, layer3]


/-- 层 1 与层 4 不相交。 -/
lemma layer1_disjoint_layer4 : layer1 ∩ layer4 = (∅ : Finset (Fin 15)) := by
  ext x
  fin_cases x <;> simp [layer1, layer4]


/-- 层 2 与层 3 不相交。 -/
lemma layer2_disjoint_layer3 : layer2 ∩ layer3 = (∅ : Finset (Fin 15)) := by
  ext x
  fin_cases x <;> simp [layer2, layer3]


/-- 层 2 与层 4 不相交。 -/
lemma layer2_disjoint_layer4 : layer2 ∩ layer4 = (∅ : Finset (Fin 15)) := by
  ext x
  fin_cases x <;> simp [layer2, layer4]


/-- 层 3 与层 4 不相交。 -/
lemma layer3_disjoint_layer4 : layer3 ∩ layer4 = (∅ : Finset (Fin 15)) := by
  ext x
  fin_cases x <;> simp [layer3, layer4]


/-- 交运算保互斥：A∩B=∅ ⟹ S∩A 与 S∩B 互斥。 -/
lemma inter_disjoint_of_layer_disjoint (S A B : Finset (Fin 15))
    (h : A ∩ B = (∅ : Finset (Fin 15))) : Disjoint (S ∩ A) (S ∩ B) := by
  rw [Finset.disjoint_left]
  intro x hxA hxB
  rcases (Finset.mem_inter.mp hxA) with ⟨_, hA⟩
  rcases (Finset.mem_inter.mp hxB) with ⟨_, hB⟩
  have : x ∈ A ∩ B := Finset.mem_inter.mpr ⟨hA, hB⟩
  rw [h] at this
  simpa using this

/-- 层分区：S.card = Σ_i card (layer_i ∩ S)（层互斥并覆盖 univ）。 -/
lemma card_eq_sum_layer_inter (S : Finset (Fin 15)) :
    S.card = Finset.card (layer1 ∩ S) + Finset.card (layer2 ∩ S) +
      Finset.card (layer3 ∩ S) + Finset.card (layer4 ∩ S) := by
  have huniv : Finset.univ = layer1 ∪ layer2 ∪ layer3 ∪ layer4 := by
    ext x
    constructor
    · intro h
      simpa [Finset.mem_union] using layer_cover x
    · intro h
      exact Finset.mem_univ x
  have hd1 : Disjoint (S ∩ layer1) ((S ∩ layer2) ∪ ((S ∩ layer3) ∪ (S ∩ layer4))) := by
    rw [Finset.disjoint_left]
    intro x hx hrest
    rcases (Finset.mem_inter.mp hx) with ⟨_, hx1⟩
    rw [Finset.mem_union, Finset.mem_union] at hrest
    rcases hrest with hx2 | hx3 | hx4
    · rcases (Finset.mem_inter.mp hx2) with ⟨_, hx2'⟩
      have : x ∈ layer1 ∩ layer2 := Finset.mem_inter.mpr ⟨hx1, hx2'⟩
      rw [layer1_disjoint_layer2] at this
      simpa using this
    · rcases (Finset.mem_inter.mp hx3) with ⟨_, hx3'⟩
      have : x ∈ layer1 ∩ layer3 := Finset.mem_inter.mpr ⟨hx1, hx3'⟩
      rw [layer1_disjoint_layer3] at this
      simpa using this
    · rcases (Finset.mem_inter.mp hx4) with ⟨_, hx4'⟩
      have : x ∈ layer1 ∩ layer4 := Finset.mem_inter.mpr ⟨hx1, hx4'⟩
      rw [layer1_disjoint_layer4] at this
      simpa using this
  have hd2 : Disjoint (S ∩ layer2) ((S ∩ layer3) ∪ (S ∩ layer4)) := by
    rw [Finset.disjoint_left]
    intro x hx hrest
    rcases (Finset.mem_inter.mp hx) with ⟨_, hx2⟩
    rw [Finset.mem_union] at hrest
    rcases hrest with hx3 | hx4
    · rcases (Finset.mem_inter.mp hx3) with ⟨_, hx3'⟩
      have : x ∈ layer2 ∩ layer3 := Finset.mem_inter.mpr ⟨hx2, hx3'⟩
      rw [layer2_disjoint_layer3] at this
      simpa using this
    · rcases (Finset.mem_inter.mp hx4) with ⟨_, hx4'⟩
      have : x ∈ layer2 ∩ layer4 := Finset.mem_inter.mpr ⟨hx2, hx4'⟩
      rw [layer2_disjoint_layer4] at this
      simpa using this
  have hd3 : Disjoint (S ∩ layer3) (S ∩ layer4) := by
    rw [Finset.disjoint_left]
    intro x hx hx4
    rcases (Finset.mem_inter.mp hx) with ⟨_, hx3⟩
    rcases (Finset.mem_inter.mp hx4) with ⟨_, hx4'⟩
    have : x ∈ layer3 ∩ layer4 := Finset.mem_inter.mpr ⟨hx3, hx4'⟩
    rw [layer3_disjoint_layer4] at this
    simpa using this
  calc
    S.card = (S ∩ Finset.univ).card := by rw [Finset.inter_univ]
    _ = (S ∩ (layer1 ∪ layer2 ∪ layer3 ∪ layer4)).card := by rw [huniv]
    _ = ((S ∩ layer1) ∪ ((S ∩ layer2) ∪ ((S ∩ layer3) ∪ (S ∩ layer4)))).card := by
      congr 1
      ext x
      simp only [Finset.mem_inter, Finset.mem_union]
      tauto
    _ = Finset.card (S ∩ layer1) + Finset.card ((S ∩ layer2) ∪ ((S ∩ layer3) ∪ (S ∩ layer4))) := by
      rw [Finset.card_union_of_disjoint hd1]
    _ = Finset.card (S ∩ layer1) + (Finset.card (S ∩ layer2) + Finset.card ((S ∩ layer3) ∪ (S ∩ layer4))) := by
      rw [Finset.card_union_of_disjoint hd2]
    _ = Finset.card (S ∩ layer1) + (Finset.card (S ∩ layer2) + (Finset.card (S ∩ layer3) + Finset.card (S ∩ layer4))) := by
      rw [Finset.card_union_of_disjoint hd3]
    _ = Finset.card (layer1 ∩ S) + Finset.card (layer2 ∩ S) +
        Finset.card (layer3 ∩ S) + Finset.card (layer4 ∩ S) := by
      simp only [Finset.inter_comm, Nat.add_assoc]


/-- 泛化：card (L ∩ S) = L.card ⟺ L ⊆ S。 -/
lemma card_inter_layer_eq_card_iff_subset (L S : Finset (Fin 15)) :
    Finset.card (L ∩ S) = L.card ↔ L ⊆ S := by
  constructor
  · intro h x hx
    have heq : L ∩ S = L :=
      Finset.eq_of_subset_of_card_le (Finset.inter_subset_left (s₁ := L) (s₂ := S)) (by rw [h])
    have hx' : x ∈ L ∩ S := by rw [heq]; exact hx
    exact (Finset.mem_inter.mp hx').2
  · intro hsub
    rw [Finset.inter_eq_left.mpr hsub]


/-- 层 1 贡献上界：card (layer1 ∩ S) + [层1 完全活跃] ≤ 4
    （完全活跃 ⟹ 交为空 ⟹ card=0，贡献 1 ≤ 4；非完全活跃 ⟹ 贡献 = card ≤ 4）。 -/
lemma layer1_contrib_le (S : Finset (Fin 15)) :
    Finset.card (layer1 ∩ S) + (if layer1 ∩ S = (∅ : Finset (Fin 15)) then 1 else 0) ≤ 4 := by
  by_cases h : layer1 ∩ S = (∅ : Finset (Fin 15))
  · simp [h]
  · simp [h]
    have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 :=
      Finset.card_le_card (Finset.inter_subset_left (s₁ := layer1) (s₂ := S))
    have hc : Finset.card layer1 = 4 := by native_decide
    omega


/-- 层 2 贡献上界：card (layer2 ∩ S) + [层2 完全活跃] ≤ 6
    （完全活跃 ⟹ 交为空 ⟹ card=0，贡献 1 ≤ 6；非完全活跃 ⟹ 贡献 = card ≤ 6）。 -/
lemma layer2_contrib_le (S : Finset (Fin 15)) :
    Finset.card (layer2 ∩ S) + (if layer2 ∩ S = (∅ : Finset (Fin 15)) then 1 else 0) ≤ 6 := by
  by_cases h : layer2 ∩ S = (∅ : Finset (Fin 15))
  · simp [h]
  · simp [h]
    have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 :=
      Finset.card_le_card (Finset.inter_subset_left (s₁ := layer2) (s₂ := S))
    have hc : Finset.card layer2 = 6 := by native_decide
    omega


/-- 层 3 贡献上界：card (layer3 ∩ S) + [层3 完全活跃] ≤ 4
    （完全活跃 ⟹ 交为空 ⟹ card=0，贡献 1 ≤ 4；非完全活跃 ⟹ 贡献 = card ≤ 4）。 -/
lemma layer3_contrib_le (S : Finset (Fin 15)) :
    Finset.card (layer3 ∩ S) + (if layer3 ∩ S = (∅ : Finset (Fin 15)) then 1 else 0) ≤ 4 := by
  by_cases h : layer3 ∩ S = (∅ : Finset (Fin 15))
  · simp [h]
  · simp [h]
    have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 :=
      Finset.card_le_card (Finset.inter_subset_left (s₁ := layer3) (s₂ := S))
    have hc : Finset.card layer3 = 4 := by native_decide
    omega


/-- 层 4 贡献上界：card (layer4 ∩ S) + [层4 完全活跃] ≤ 1
    （完全活跃 ⟹ 交为空 ⟹ card=0，贡献 1 ≤ 1；非完全活跃 ⟹ 贡献 = card ≤ 1）。 -/
lemma layer4_contrib_le (S : Finset (Fin 15)) :
    Finset.card (layer4 ∩ S) + (if layer4 ∩ S = (∅ : Finset (Fin 15)) then 1 else 0) ≤ 1 := by
  by_cases h : layer4 ∩ S = (∅ : Finset (Fin 15))
  · simp [h]
  · simp [h]
    have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 :=
      Finset.card_le_card (Finset.inter_subset_left (s₁ := layer4) (s₂ := S))
    have hc : Finset.card layer4 = 1 := by native_decide
    omega


/-- 组合引理：S.card + fullActiveCount S = 15 ⟺ S = univ ∨ S = univ.erase 14。
    ⟹ 向：16 分支（各层完全活跃与否）逐一 omega 定 card，再层满 ⟹ S 等式；
    ⟸ 向：univ 全静默（贡献 0）或 erase 14（层 1..3 满、层 4 空）。 -/
lemma card_add_fullActive_eq_15_iff (S : Finset (Fin 15)) :
    S.card + fullActiveCount S = 15 ↔ S = Finset.univ ∨ S = Finset.univ.erase 14 := by
  classical
  constructor
  · intro htot

    by_cases hb1 : layer1 ∩ S = (∅ : Finset (Fin 15))
    ·
      by_cases hb2 : layer2 ∩ S = (∅ : Finset (Fin 15))
      ·
        by_cases hb3 : layer3 ∩ S = (∅ : Finset (Fin 15))
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 4 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 11 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 3 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 12 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 3 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 12 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 2 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 13 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
      ·
        by_cases hb3 : layer3 ∩ S = (∅ : Finset (Fin 15))
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 3 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 12 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 2 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 13 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 2 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 13 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 1 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 14 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_0 : Finset.card (layer1 ∩ S) = 0 := by rw [hb1]; simp
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
    ·
      by_cases hb2 : layer2 ∩ S = (∅ : Finset (Fin 15))
      ·
        by_cases hb3 : layer3 ∩ S = (∅ : Finset (Fin 15))
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 3 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 12 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 2 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 13 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 2 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 13 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 1 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 14 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_0 : Finset.card (layer2 ∩ S) = 0 := by rw [hb2]; simp
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
      ·
        by_cases hb3 : layer3 ∩ S = (∅ : Finset (Fin 15))
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 2 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 13 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
          ·
            have hfac : fullActiveCount S = 1 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 14 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_0 : Finset.card (layer3 ∩ S) = 0 := by rw [hb3]; simp
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            rw [card_eq_sum_layer_inter S] at hS
            exfalso
            omega
        ·
          by_cases hb4 : layer4 ∩ S = (∅ : Finset (Fin 15))
          ·
            have hfac : fullActiveCount S = 1 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 14 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_0 : Finset.card (layer4 ∩ S) = 0 := by rw [hb4]; simp
            have h14S : (14 : Fin 15) ∉ S := by
              intro h14
              have hmem : (14 : Fin 15) ∈ layer4 ∩ S := Finset.mem_inter.mpr ⟨by simp [layer4], h14⟩
              rw [hb4] at hmem
              simpa using hmem
            apply Or.inr
            apply Finset.eq_of_subset_of_card_le
            · intro x hx
              by_cases hx14 : x = 14
              · exfalso
                subst x
                exact h14S hx
              · simp [Finset.mem_erase, hx14]
            · rw [hS]
              simp
          ·
            have hfac : fullActiveCount S = 0 := by simp [fullActiveCount, hb1, hb2, hb3, hb4]
            have hS : S.card = 15 := by omega
            have h1le : Finset.card (layer1 ∩ S) ≤ 4 := by
              have hsub : layer1 ∩ S ⊆ layer1 := Finset.inter_subset_left (s₁ := layer1) (s₂ := S)
              have hle : Finset.card (layer1 ∩ S) ≤ Finset.card layer1 := Finset.card_le_card hsub
              have hc : Finset.card layer1 = 4 := by native_decide
              omega
            have h2le : Finset.card (layer2 ∩ S) ≤ 6 := by
              have hsub : layer2 ∩ S ⊆ layer2 := Finset.inter_subset_left (s₁ := layer2) (s₂ := S)
              have hle : Finset.card (layer2 ∩ S) ≤ Finset.card layer2 := Finset.card_le_card hsub
              have hc : Finset.card layer2 = 6 := by native_decide
              omega
            have h3le : Finset.card (layer3 ∩ S) ≤ 4 := by
              have hsub : layer3 ∩ S ⊆ layer3 := Finset.inter_subset_left (s₁ := layer3) (s₂ := S)
              have hle : Finset.card (layer3 ∩ S) ≤ Finset.card layer3 := Finset.card_le_card hsub
              have hc : Finset.card layer3 = 4 := by native_decide
              omega
            have h4le : Finset.card (layer4 ∩ S) ≤ 1 := by
              have hsub : layer4 ∩ S ⊆ layer4 := Finset.inter_subset_left (s₁ := layer4) (s₂ := S)
              have hle : Finset.card (layer4 ∩ S) ≤ Finset.card layer4 := Finset.card_le_card hsub
              have hc : Finset.card layer4 = 1 := by native_decide
              omega
            have hc1_pos : 0 < Finset.card (layer1 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb1)
            have hc2_pos : 0 < Finset.card (layer2 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb2)
            have hc3_pos : 0 < Finset.card (layer3 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb3)
            have hc4_pos : 0 < Finset.card (layer4 ∩ S) := by
              exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb4)
            apply Or.inl
            apply Finset.eq_of_subset_of_card_le
            · intro x hx
              exact Finset.mem_univ x
            · rw [hS]
              simp

  · rintro (hS | hS)
    · rw [hS]
      native_decide
    · rw [hS]
      native_decide


/-- 层 1 循环非不动：层内后继不恒等（活跃层 1 无天然不动点）。 -/
lemma layeredStep_ne_self_of_layer1 (x : Fin 15) (hx : x ∈ layer1) : layeredStep x ≠ x := by
  have hx014 : x = 0 ∨ x = 1 ∨ x = 2 ∨ x = 3 := by simpa [layer1] using hx
  rcases hx014 with rfl | rfl | rfl | rfl <;> native_decide

/-- 层 2 循环非不动。 -/
lemma layeredStep_ne_self_of_layer2 (x : Fin 15) (hx : x ∈ layer2) : layeredStep x ≠ x := by
  have hx49 : x = 4 ∨ x = 5 ∨ x = 6 ∨ x = 7 ∨ x = 8 ∨ x = 9 := by simpa [layer2] using hx
  rcases hx49 with rfl | rfl | rfl | rfl | rfl | rfl <;> native_decide

/-- 层 3 循环非不动。 -/
lemma layeredStep_ne_self_of_layer3 (x : Fin 15) (hx : x ∈ layer3) : layeredStep x ≠ x := by
  have hx1013 : x = 10 ∨ x = 11 ∨ x = 12 ∨ x = 13 := by simpa [layer3] using hx
  rcases hx1013 with rfl | rfl | rfl | rfl <;> native_decide

/-- 模型级"静默⟺不动"刻画：silentStep S 下 x 不动 ⟺ x ∈ S（静默窗）∨ x = 14
    （层 4 天然不动点，1-周期层无需静默即锁定）。 -/
lemma silentStep_fixed_iff_mem_or_fourteen (S : Finset (Fin 15)) (x : Fin 15) :
    silentStep S x = x ↔ x ∈ S ∨ x = 14 := by
  by_cases hxS : x ∈ S
  · simp [silentStep, hxS]
  · simp [silentStep, hxS]
    rcases layer_cover x with hx1 | hx2 | hx3 | hx4
    · have hx' : layeredStep x ≠ x := layeredStep_ne_self_of_layer1 x hx1
      constructor
      · intro h
        exfalso
        exact hx' h
      · intro h
        subst x
        native_decide
    · have hx' : layeredStep x ≠ x := layeredStep_ne_self_of_layer2 x hx2
      constructor
      · intro h
        exfalso
        exact hx' h
      · intro h
        subst x
        native_decide
    · have hx' : layeredStep x ≠ x := layeredStep_ne_self_of_layer3 x hx3
      constructor
      · intro h
        exfalso
        exact hx' h
      · intro h
        subst x
        native_decide
    · have hx14 : x = 14 := by simpa [layer4] using hx4
      subst x
      constructor
      · intro h
        rfl
      · intro h
        native_decide


/-- 反向翻译精确化主定理：orbitCount = 15 ⟺ S = univ ∨ S = univ.erase 14。
    "g=15 的实现" = 全静默 或 除层 4 天然不动点 14 外全静默。 -/
theorem orbitCount_eq_15_iff (S : Finset (Fin 15)) :
    orbitCount (silenceRec15_layered S) = 15 ↔ S = Finset.univ ∨ S = Finset.univ.erase 14 := by
  rw [orbitCount_layered S]
  exact card_add_fullActive_eq_15_iff S

/-! ## 独立不动点 ⟺ 静默窗（2026-10-24 公设模型实例化）

用户裁决（2026-10-24）：静默 = 闭合冻结（独立不动点，结构保留）+ 作为可观测量零测度，
非"丢弃"；公设形态 = "独立不动点（闭合冻结）⟺ 静默（零测度）"。
本段在分层模型（silenceRec15_layered S）上证明该公设的实例：
- `independentFixed S x` := 不动（闭合冻结）∧ 非任何完全活跃层成员（非活跃循环）；
- `independentFixed_iff_mem`：独立不动点 ⟺ 静默窗（x ∈ S）；
- `fixed_iff_mem_or_14`：不动点 ⟺ 静默窗 ∨ 14（层 4 单点层天然不动 = "冻结≠静默"的
  模型边界实例：14 不动但不静默，除非 14 ∈ S）；
- `all_fixed_char`：全不动 ⟺ S=univ ∨ S=univ.erase 14（"恒等⟹全静默"的精确形态：
  全锁定极限下除模型边界 14 外全部闭合冻结 ⟹ 全静默；14 为完成态结构保留）。
零 sorry 政策：本段不含 sorry。 -/

/-- 静默窗成员 ⟹ silentStep 不动（干净函数层）。 -/
lemma silentStep_mem (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∈ S) :
    silentStep S x = x := by
  simp [silentStep, hx]

/-- 非静默窗成员 ⟹ silentStep 退化为层内循环。 -/
lemma silentStep_not_mem (S : Finset (Fin 15)) {x : Fin 15} (hx : x ∉ S) :
    silentStep S x = layeredStep x := by
  simp [silentStep, hx]

/-- 层 4 单点窗 14 恒不动（无论是否静默）："冻结≠静默"的模型边界实例。 -/
lemma silentStep_14 (S : Finset (Fin 15)) : silentStep S (14 : Fin 15) = 14 := by
  by_cases h14 : (14 : Fin 15) ∈ S
  · exact silentStep_mem S h14
  · simp [silentStep_not_mem S h14, layeredStep, layer1, layer2, layer3]

/-- 层内循环无非 14 不动点：layeredStep x = x ⟹ x = 14（层 1-3 循环无不动点）。 -/
lemma layeredStep_fixed_eq_14 (x : Fin 15) (hx : layeredStep x = x) : x = (14 : Fin 15) := by
  fin_cases x <;> simp [layeredStep, layer1, layer2, layer3] at hx ⊢

/-- 不动点刻画：silentStep 不动 ⟺ 静默窗 ∨ 模型边界 14。 -/
lemma fixed_iff_mem_or_14 (S : Finset (Fin 15)) (x : Fin 15) :
    silentStep S x = x ↔ x ∈ S ∨ x = (14 : Fin 15) := by
  constructor
  · intro hx
    by_cases hxS : x ∈ S
    · exact Or.inl hxS
    · right
      have hlay : layeredStep x = x := by
        simpa [silentStep_not_mem S hxS] using hx
      exact layeredStep_fixed_eq_14 x hlay
  · intro hx
    rcases hx with hxS | hx14
    · exact silentStep_mem S hxS
    · subst hx14
      exact silentStep_14 S

/-- 独立不动点（闭合冻结）：不动 ∧ 非任何完全活跃层（活跃循环）成员。 -/
def independentFixed (S : Finset (Fin 15)) (x : Fin 15) : Prop :=
  silentStep S x = x ∧ ∀ L ∈ layers, L ∩ S = ∅ → x ∉ L

/-- 公设"独立不动点 ⟺ 静默窗"的模型实例化。 -/
theorem independentFixed_iff_mem (S : Finset (Fin 15)) (x : Fin 15) :
    independentFixed S x ↔ x ∈ S := by
  constructor
  · intro hx
    rcases hx with ⟨hfix, hnot⟩
    rcases (fixed_iff_mem_or_14 S x).mp hfix with hxS | hx14
    · exact hxS
    · by_contra hxS
      have hL : layer4 ∩ S = ∅ := by
        ext m
        simp [layer4]
        intro hm14 hmS
        exact hxS (by simpa [hm14, hx14] using hmS)
      have hx4 : x ∈ layer4 := by simpa [hx14] using (by simp [layer4] : (14 : Fin 15) ∈ layer4)
      exact hnot layer4 (by simp [layers]) hL hx4
  · intro hxS
    constructor
    · exact silentStep_mem S hxS
    · intro L hLmem hLem hxL
      have hxLmem : x ∈ L ∩ S := Finset.mem_inter.mpr ⟨hxL, hxS⟩
      simp [hLem] at hxLmem

/-- 全不动 ⟺ 全静默（除模型边界 14）："恒等⟹全静默"的精确模型形态。 -/
theorem all_fixed_char (S : Finset (Fin 15)) :
    (∀ x : Fin 15, silentStep S x = x) ↔ S = Finset.univ ∨ S = Finset.univ.erase 14 := by
  constructor
  · intro hfix
    have hcov : ∀ x : Fin 15, x ∈ S ∨ x = (14 : Fin 15) := by
      intro x
      exact (fixed_iff_mem_or_14 S x).mp (hfix x)
    by_cases h14S : (14 : Fin 15) ∈ S
    · left
      ext y
      by_cases hy14 : y = (14 : Fin 15)
      · simp [hy14, h14S]
      · have hyS : y ∈ S := (hcov y).resolve_right hy14
        simp [hyS]
    · right
      ext y
      constructor
      · intro hyS
        have hy14 : y ≠ (14 : Fin 15) := by
          intro hy14
          exact h14S (by simpa [hy14] using hyS)
        simp [hy14]
      · intro hyErase
        rcases (Finset.mem_erase.mp hyErase) with ⟨hy14, hyU⟩
        exact (hcov y).resolve_right hy14
  · intro hS
    rcases hS with rfl | hS
    · intro x
      exact silentStep_mem Finset.univ (by simp)
    · intro x
      rw [hS]
      by_cases hx14 : x = (14 : Fin 15)
      · subst hx14
        exact silentStep_14 (Finset.univ.erase 14)
      · have hxS : x ∈ Finset.univ.erase 14 := by simp [hx14]
        exact silentStep_mem (Finset.univ.erase 14) hxS

/-- "恒等 ⟹ 全静默"定理（模型边界版）：全不动 ⟹ 全静默，边界 14 为完成态结构保留
    （层 4 单点层天然不动，非静默窗；全静默 S=univ 是解之一）。 -/
theorem all_fixed_silence_boundary (S : Finset (Fin 15))
    (hfix : ∀ x : Fin 15, silentStep S x = x) :
    S = Finset.univ ∨ S = Finset.univ.erase 14 :=
  (all_fixed_char S).mp hfix

/-- orbitCount=15 ⟹ 全锁定 ⟹ 全静默（边界版）：由 OrbitFullLock (⇒) 与
    all_fixed_silence_boundary 合拢（g=15 解集 {univ, univ.erase 14}，全静默为解之一）。 -/
theorem orbitCount_eq_15_silence_boundary (S : Finset (Fin 15))
    (h : orbitCount (silenceRec15_layered S) = 15) :
    S = Finset.univ ∨ S = Finset.univ.erase 14 :=
  (orbitCount_eq_15_iff S).mp h

end MUFPF.PeriodicOrbitCount
