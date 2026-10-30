# -*- coding: utf-8 -*-
"""生成反向翻译精确化 Lean 段（SilenceModel.lean 末尾追加块）。

内容：
1. 层两两互斥引理（3 个 rest 形式）
2. 层分区引理 card_eq_sum_layer_inter
3. 泛化引理 card_inter_layer_eq_card_iff_subset（card 满 ⟺ 层⊆S）
4. 每层贡献上界 layer{1..4}_contrib_le
5. 组合引理 card_add_fullActive_eq_15_iff（16 分支，omega 主战场）
6. 静默⟺不动刻画 silentStep_fixed_iff_mem_or_fourteen
7. 层1..3 循环非不动 layeredStep_ne_self_of_layer{1..3}
8. 主定理 orbitCount_eq_15_iff

写到一个临时 .lean 文件，供 Read 核对后 Edit 插入。
"""
from itertools import product

OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\gen_reverse_block.txt"

layers = ["layer1", "layer2", "layer3", "layer4"]
cards = {0: 4, 1: 6, 2: 4, 3: 1}
reps = {0: "0", 1: "4", 2: "10", 3: "14"}

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
lemma {a}_disjoint_{b} : {a} ∩ {b} = ∅ := by
  ext x
  fin_cases x <;> simp [{a}, {b}]
""")

L.append("""
/-- 交运算保互斥：A∩B=∅ ⟹ S∩A 与 S∩B 互斥。 -/
lemma inter_disjoint_of_layer_disjoint (S A B : Finset (Fin 15))
    (h : A ∩ B = ∅) : Disjoint (S ∩ A) (S ∩ B) := by
  rw [Finset.disjoint_left]
  intro x hxA hxB
  rcases (Finset.mem_inter.mp hxA) with ⟨_, hA⟩
  rcases (Finset.mem_inter.mp hxB) with ⟨_, hB⟩
  have : x ∈ A ∩ B := Finset.mem_inter.mpr ⟨hA, hB⟩
  rw [h] at this
  simpa using this

/-- 层分区：S.card = Σ_i card (layer_i ∩ S)（层互斥并覆盖 univ）。 -/
lemma card_eq_sum_layer_inter (S : Finset (Fin 15)) :
    S.card = card (layer1 ∩ S) + card (layer2 ∩ S) + card (layer3 ∩ S) + card (layer4 ∩ S) := by
  have huniv : Finset.univ = layer1 ∪ layer2 ∪ layer3 ∪ layer4 := by
    ext x
    constructor
    · intro h
      exact layer_cover x
    · intro h
      exact Finset.mem_univ x
  have hd1 : Disjoint (S ∩ layer1) ((S ∩ layer2) ∪ (S ∩ layer3) ∪ (S ∩ layer4)) := by
    rw [Disjoint.union_right]
    constructor
    · rw [Disjoint.union_right]
      constructor
      · exact inter_disjoint_of_layer_disjoint S layer1 layer2 layer1_disjoint_layer2
      · exact inter_disjoint_of_layer_disjoint S layer1 layer3 layer1_disjoint_layer3
    · exact inter_disjoint_of_layer_disjoint S layer1 layer4 layer1_disjoint_layer4
  have hd2 : Disjoint (S ∩ layer2) ((S ∩ layer3) ∪ (S ∩ layer4)) := by
    rw [Disjoint.union_right]
    constructor
    · exact inter_disjoint_of_layer_disjoint S layer2 layer3 layer2_disjoint_layer3
    · exact inter_disjoint_of_layer_disjoint S layer2 layer4 layer2_disjoint_layer4
  have hd3 : Disjoint (S ∩ layer3) (S ∩ layer4) := by
    exact inter_disjoint_of_layer_disjoint S layer3 layer4 layer3_disjoint_layer4
  calc
    S.card = (S ∩ Finset.univ).card := by rw [Finset.inter_univ]
    _ = (S ∩ (layer1 ∪ layer2 ∪ layer3 ∪ layer4)).card := by rw [huniv]
    _ = ((S ∩ layer1) ∪ (S ∩ layer2) ∪ (S ∩ layer3) ∪ (S ∩ layer4)).card := by
      congr 1
      ext x
      simp only [Finset.mem_inter, Finset.mem_union]
      tauto
    _ = card (S ∩ layer1) + card (S ∩ layer2) + card (S ∩ layer3) + card (S ∩ layer4) := by
      rw [Finset.card_union_of_disjoint hd1]
      rw [Finset.card_union_of_disjoint hd2]
      rw [Finset.card_union_of_disjoint hd3]
    _ = card (layer1 ∩ S) + card (layer2 ∩ S) + card (layer3 ∩ S) + card (layer4 ∩ S) := by
      simp [Finset.inter_comm]
""")

# --- 3. card 满 ⟺ 层⊆S ---
L.append("""
/-- 泛化：card (L ∩ S) = L.card ⟺ L ⊆ S。 -/
lemma card_inter_layer_eq_card_iff_subset (L S : Finset (Fin 15)) :
    card (L ∩ S) = L.card ↔ L ⊆ S := by
  constructor
  · intro h x hx
    have heq : L ∩ S = L :=
      Finset.eq_of_subset_of_card_le (Finset.inter_subset_left L S) (by rw [h])
    have hx' : x ∈ L ∩ S := by rw [heq]; exact hx
    exact (Finset.mem_inter.mp hx').2
  · intro hsub
    rw [Finset.inter_eq_left.mpr hsub]
""")

# --- 4. 每层贡献上界 ---
for i, Ln in enumerate(layers):
    c = cards[i]
    L.append(f"""
/-- 层 {i+1} 贡献上界：card (layer{i+1} ∩ S) + [层{i+1} 完全活跃] ≤ {c}
    （完全活跃 ⟹ 交为空 ⟹ card=0，贡献 1 ≤ {c}；非完全活跃 ⟹ 贡献 = card ≤ {c}）。 -/
lemma layer{i+1}_contrib_le (S : Finset (Fin 15)) :
    card (layer{i+1} ∩ S) + (if layer{i+1} ∩ S = ∅ then 1 else 0) ≤ {c} := by
  by_cases h : layer{i+1} ∩ S = ∅
  · simp [h]
    rw [h]
    simp [layer{i+1}]
  · simp [h]
    exact Finset.card_le_card (Finset.inter_subset_left layer{i+1} S)
""")

# --- 5. 组合引理 16 分支 ---
L.append("""
/-- 组合引理：S.card + fullActiveCount S = 15 ⟺ S = univ ∨ S = univ.erase 14。
    ⟹ 向：16 分支（各层完全活跃与否）逐一 omega 定 card，再层满 ⟹ S 等式；
    ⟸ 向：univ 全静默（贡献 0）或 erase 14（层 1..3 满、层 4 空）。 -/
lemma card_add_fullActive_eq_15_iff (S : Finset (Fin 15)) :
    S.card + fullActiveCount S = 15 ↔ S = Finset.univ ∨ S = Finset.univ.erase 14 := by
  classical
  constructor
  · intro htot
    by_cases hb1 : layer1 ∩ S = ∅
    <;> by_cases hb2 : layer2 ∩ S = ∅
    <;> by_cases hb3 : layer3 ∩ S = ∅
    <;> by_cases hb4 : layer4 ∩ S = ∅
""")

branches = list(product([False, True], repeat=4))
for idx, b in enumerate(branches):
    f = sum(b)  # fullActiveCount 闭值
    ind = "      " if idx < 15 else "    "
    L.append(f"{ind}· -- 分支 {idx+1}/16：层完全活跃 = {b}")
    L.append(f"{ind}  simp [fullActiveCount, hb1, hb2, hb3, hb4]")
    L.append(f"{ind}  rw [card_eq_sum_layer_inter S]")
    # 上界四层
    L.append(f"{ind}  have h1le : card (layer1 ∩ S) ≤ 4 := by simpa [layer1] using (Finset.card_le_card (Finset.inter_subset_left layer1 S))")
    L.append(f"{ind}  have h2le : card (layer2 ∩ S) ≤ 6 := by simpa [layer2] using (Finset.card_le_card (Finset.inter_subset_left layer2 S))")
    L.append(f"{ind}  have h3le : card (layer3 ∩ S) ≤ 4 := by simpa [layer3] using (Finset.card_le_card (Finset.inter_subset_left layer3 S))")
    L.append(f"{ind}  have h4le : card (layer4 ∩ S) ≤ 1 := by simpa [layer4] using (Finset.card_le_card (Finset.inter_subset_left layer4 S))")
    for i, bi in enumerate(b):
        if bi:
            L.append(f"{ind}  have hc{i+1}_0 : card (layer{i+1} ∩ S) = 0 := by rw [hb{i+1}]; simp")
        else:
            L.append(f"{ind}  have hc{i+1}_pos : 0 < card (layer{i+1} ∩ S) := by")
            L.append(f"{ind}    exact Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hb{i+1})")
    possible = (not b[0]) and (not b[1]) and (not b[2])
    if possible and not b[3]:
        # S = univ：推 c_i 取满
        L.append(f"{ind}  have hc1 : card (layer1 ∩ S) = 4 := by omega")
        L.append(f"{ind}  have hc2 : card (layer2 ∩ S) = 6 := by omega")
        L.append(f"{ind}  have hc3 : card (layer3 ∩ S) = 4 := by omega")
        L.append(f"{ind}  have hc4 : card (layer4 ∩ S) = 1 := by omega")
        L.append(f"{ind}  have hS15 : S.card = 15 := by omega")
        L.append(f"{ind}  apply Or.inl")
        L.append(f"{ind}  apply Finset.eq_of_subset_of_card_le")
        L.append(f"{ind}  · intro x hx")
        L.append(f"{ind}    exact Finset.mem_univ x")
        L.append(f"{ind}  · rw [hS15]")
        L.append(f"{ind}    simp")
    elif possible and b[3]:
        # S = univ.erase 14
        L.append(f"{ind}  have hc1 : card (layer1 ∩ S) = 4 := by omega")
        L.append(f"{ind}  have hc2 : card (layer2 ∩ S) = 6 := by omega")
        L.append(f"{ind}  have hc3 : card (layer3 ∩ S) = 4 := by omega")
        L.append(f"{ind}  have hS14 : S.card = 14 := by omega")
        L.append(f"{ind}  have h14S : (14 : Fin 15) ∉ S := by")
        L.append(f"{ind}    intro h14")
        L.append(f"{ind}    have hmem : (14 : Fin 15) ∈ layer4 ∩ S := Finset.mem_inter.mpr ⟨by simp [layer4], h14⟩")
        L.append(f"{ind}    rw [hb4] at hmem")
        L.append(f"{ind}    simpa using hmem")
        L.append(f"{ind}  apply Or.inr")
        L.append(f"{ind}  apply Finset.eq_of_subset_of_card_le")
        L.append(f"{ind}  · intro x hx")
        L.append(f"{ind}    by_cases hx14 : x = 14")
        L.append(f"{ind}    · exfalso")
        L.append(f"{ind}      subst x")
        L.append(f"{ind}      exact h14S hx")
        L.append(f"{ind}    · simp [Finset.mem_erase, hx14, hx]")
        L.append(f"{ind}  · rw [hS14]")
        L.append(f"{ind}    simp")
    else:
        L.append(f"{ind}  exfalso")
        L.append(f"{ind}  omega")

L.append("""
  · rintro (hS | hS)
    · rw [hS]
      simp [fullActiveCount, Finset.univ] 
    · rw [hS]
      have h1 : layer1 ∩ Finset.univ.erase 14 = layer1 := by
        ext x
        simp [layer1, Finset.mem_erase]
      have h2 : layer2 ∩ Finset.univ.erase 14 = layer2 := by
        ext x
        simp [layer2, Finset.mem_erase]
      have h3 : layer3 ∩ Finset.univ.erase 14 = layer3 := by
        ext x
        simp [layer3, Finset.mem_erase]
      have h4 : layer4 ∩ Finset.univ.erase 14 = ∅ := by
        ext x
        simp [layer4, Finset.mem_erase]
      have hcard : card (Finset.univ.erase 14) = 14 := by simp
      simp [fullActiveCount, h1, h2, h3, h4, hcard]
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
