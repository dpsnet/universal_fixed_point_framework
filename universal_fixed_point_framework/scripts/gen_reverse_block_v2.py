# -*- coding: utf-8 -*-
"""生成反向翻译精确化 Lean 段 v2（SilenceModel.lean 末尾追加块）。

修复（相对 v1）：
- 裸 card → Finset.card（该环境裸 card 为 unknown identifier）
- 裸 ∅ → (∅ : Finset (Fin 15))（裸 ∅ 同样 unknown）
- layer_cover 在 union 目标下需 simpa [Finset.mem_union]
- Disjoint.union_right → 手推 disjoint_left 结构
- rcases union 成员需先 rw [Finset.mem_union]
"""
from itertools import product

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\gen_reverse_block_v2.txt"

E = "(∅ : Finset (Fin 15))"

L = []

L.append("""
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
-/""")

# --- 1. 层两两互斥（6 对） ---
pairs = [("layer1", "layer2"), ("layer1", "layer3"), ("layer1", "layer4"),
         ("layer2", "layer3"), ("layer2", "layer4"), ("layer3", "layer4")]
for a, b in pairs:
    L.append(f"""
/-- 层 {a[5:]} 与层 {b[5:]} 不相交。 -/
lemma {a}_disjoint_{b} : {a} ∩ {b} = {E} := by
  ext x
  fin_cases x <;> simp [{a}, {b}]
""")

# --- 2. 交保互斥 + 层分区 ---
L.append(f"""
/-- 交运算保互斥：A∩B=∅ ⟹ S∩A 与 S∩B 互斥。 -/
lemma inter_disjoint_of_layer_disjoint (S A B : Finset (Fin 15))
    (h : A ∩ B = {E}) : Disjoint (S ∩ A) (S ∩ B) := by
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
""")

# --- 3. card 满 ⟺ 层⊆S ---
L.append("""
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
""")

# --- 4. 每层贡献上界 ---
cardsizes = {0: 4, 1: 6, 2: 4, 3: 1}
for i in range(4):
    c = cardsizes[i]
    L.append(f"""
/-- 层 {i+1} 贡献上界：card (layer{i+1} ∩ S) + [层{i+1} 完全活跃] ≤ {c}
    （完全活跃 ⟹ 交为空 ⟹ card=0，贡献 1 ≤ {c}；非完全活跃 ⟹ 贡献 = card ≤ {c}）。 -/
lemma layer{i+1}_contrib_le (S : Finset (Fin 15)) :
    Finset.card (layer{i+1} ∩ S) + (if layer{i+1} ∩ S = {E} then 1 else 0) ≤ {c} := by
  by_cases h : layer{i+1} ∩ S = {E}
  · simp [h]
  · simp [h]
    have hle : Finset.card (layer{i+1} ∩ S) ≤ Finset.card layer{i+1} :=
      Finset.card_le_card (Finset.inter_subset_left (s₁ := layer{i+1}) (s₂ := S))
    have hc : Finset.card layer{i+1} = {c} := by native_decide
    omega
""")

# --- 5. 组合引理（嵌套 by_cases 16 叶，逐叶 omega） ---
def gen_branch_body(L, ind, b):
    f = sum(b)
    L.append(f"{ind}have hfac : fullActiveCount S = {f} := by simp [fullActiveCount, hb1, hb2, hb3, hb4]")
    L.append(f"{ind}have hS : S.card = {15 - f} := by omega")
    for i, c in cardsizes.items():
        L.append(f"{ind}have h{i+1}le : Finset.card (layer{i+1} ∩ S) ≤ {c} := by")
        L.append(f"{ind}  have hsub : layer{i+1} ∩ S ⊆ layer{i+1} := Finset.inter_subset_left (s₁ := layer{i+1}) (s₂ := S)")
        L.append(f"{ind}  have hle : Finset.card (layer{i+1} ∩ S) ≤ Finset.card layer{i+1} := Finset.card_le_card hsub")
        L.append(f"{ind}  have hc : Finset.card layer{i+1} = {c} := by native_decide")
        L.append(f"{ind}  omega")
    for i, bi in enumerate(b):
        if bi:
            L.append(f"{ind}have hc{i+1}_0 : Finset.card (layer{i+1} ∩ S) = 0 := by rw [hb{i+1}]; simp")
        else:
            L.append(f"{ind}have hc{i+1}_pos : 0 < Finset.card (layer{i+1} ∩ S) := by")
            L.append(f"{ind}  exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb{i+1})")
    if f == 0:
        L.append(f"{ind}apply Or.inl")
        L.append(f"{ind}apply Finset.eq_of_subset_of_card_le")
        L.append(f"{ind}· intro x hx")
        L.append(f"{ind}  exact Finset.mem_univ x")
        L.append(f"{ind}· rw [hS]")
        L.append(f"{ind}  simp")
    elif (not b[0]) and (not b[1]) and (not b[2]) and b[3]:
        L.append(f"{ind}have h14S : (14 : Fin 15) ∉ S := by")
        L.append(f"{ind}  intro h14")
        L.append(f"{ind}  have hmem : (14 : Fin 15) ∈ layer4 ∩ S := Finset.mem_inter.mpr ⟨by simp [layer4], h14⟩")
        L.append(f"{ind}  rw [hb4] at hmem")
        L.append(f"{ind}  simpa using hmem")
        L.append(f"{ind}apply Or.inr")
        L.append(f"{ind}apply Finset.eq_of_subset_of_card_le")
        L.append(f"{ind}· intro x hx")
        L.append(f"{ind}  by_cases hx14 : x = 14")
        L.append(f"{ind}  · exfalso")
        L.append(f"{ind}    subst x")
        L.append(f"{ind}    exact h14S hx")
        L.append(f"{ind}  · simp [Finset.mem_erase, hx14]")
        L.append(f"{ind}· rw [hS]")
        L.append(f"{ind}  simp")
    else:
        L.append(f"{ind}rw [card_eq_sum_layer_inter S] at hS")
        L.append(f"{ind}exfalso")
        L.append(f"{ind}omega")

def gen_nested(L, depth, ind, b):
    if depth == 4:
        gen_branch_body(L, ind, b)
        return
    L.append(f"{ind}by_cases hb{depth+1} : layer{depth+1} ∩ S = {E}")
    L.append(f"{ind}·")
    gen_nested(L, depth + 1, ind + "  ", b + [True])
    L.append(f"{ind}·")
    gen_nested(L, depth + 1, ind + "  ", b + [False])

L.append(f"""
/-- 组合引理：S.card + fullActiveCount S = 15 ⟺ S = univ ∨ S = univ.erase 14。
    ⟹ 向：16 分支（各层完全活跃与否）逐一 omega 定 card，再层满 ⟹ S 等式；
    ⟸ 向：univ 全静默（贡献 0）或 erase 14（层 1..3 满、层 4 空）。 -/
lemma card_add_fullActive_eq_15_iff (S : Finset (Fin 15)) :
    S.card + fullActiveCount S = 15 ↔ S = Finset.univ ∨ S = Finset.univ.erase 14 := by
  classical
  constructor
  · intro htot
""")
gen_nested(L, 0, "    ", [])

L.append(f"""
  · rintro (hS | hS)
    · rw [hS]
      native_decide
    · rw [hS]
      native_decide
""")

# --- 6. 静默⟺不动 ---
L.append("""
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
""")

# --- 8. 主定理 ---
L.append("""
/-- 反向翻译精确化主定理：orbitCount = 15 ⟺ S = univ ∨ S = univ.erase 14。
    "g=15 的实现" = 全静默 或 除层 4 天然不动点 14 外全静默。 -/
theorem orbitCount_eq_15_iff (S : Finset (Fin 15)) :
    orbitCount (silenceRec15_layered S) = 15 ↔ S = Finset.univ ∨ S = Finset.univ.erase 14 := by
  rw [orbitCount_layered S]
  exact card_add_fullActive_eq_15_iff S
""")

text = "\n".join(L)
with open(OUT, "w", encoding="utf-8") as fp:
    fp.write(text)
print(f"written {len(text)} chars to {OUT}")
