import Mathlib.Tactic
import MUFPFormalization.SilenceModel

/-!
# 静默单调定理（S303——2026-10-28）

静默度-轨道数单调：S ⊆ S' ⟹ orbitCount(silentStep S) ≤ orbitCount(silentStep S')。

物理对应（S302 机制候选）：θ_F 距奇异极限（15°=SigmaInv°——m_e=0）的
偏离 δ ≈ 静默⁻² 是'静默未满'的度量——静默越满轨道数越大（4 → 15）——
'静默满额 → 恒等（orbitCount=15）'的连续谱离散骨架。

数值先证伪（scripts/s303_silence_monotone_check.py）：26000 组随机
S ⊆ S' 零违例（端点 orbitCount(∅)=4、orbitCount(univ)=15、边界解集
univ.erase 14=15 全对）——模式 8 满足——投入证明。

证明路径：
1. `layer_g_eq_of_not_mem`：层交集 if 项在 insert 下相等（x 不在该层）
2. `layer_g_le_insert_add_one`：受影响层 if 项 ≤ 新项 + 1
3. `fullActiveCount_le_insert_add_one`：静默窗口加入 ⟹ 完全活跃层数最多减 1
4. `silenceMonotone_single`：单窗口静默 ⟹ orbitCount 不减少（S.card +1 抵消）
5. `silenceMonotone`：S ⊆ S' 归纳（S' \ S 上的 Finset.induction_on + generalizing S）

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.PeriodicOrbitCount

open MUFPF

/-- 层不相交辅助：x ∈ L1 且 L1∩L2=∅ ⟹ x ∉ L2。 -/
lemma layer_disjoint_not_mem {x : Fin 15} {L1 L2 : Finset (Fin 15)}
    (hx : x ∈ L1) (hdis : L1 ∩ L2 = ∅) : x ∉ L2 := by
  intro hx2
  have hmem : x ∈ L1 ∩ L2 := Finset.mem_inter.mpr ⟨hx, hx2⟩
  simpa [hdis] using hmem

/-- 层交集 if 项相等：x 不在该层 ⟹ L∩(insert x S) = L∩S（项不变）。 -/
lemma layer_g_eq_of_not_mem (S : Finset (Fin 15)) {x : Fin 15} (L : Finset (Fin 15))
    (hx : x ∉ L) :
    (if L ∩ insert x S = (∅ : Finset (Fin 15)) then 1 else 0)
      = (if L ∩ S = (∅ : Finset (Fin 15)) then 1 else 0) := by
  have hinter : L ∩ insert x S = L ∩ S := by
    ext y
    by_cases hyx : y = x
    · subst hyx
      simp [hx]
    · simp [hyx, Finset.mem_insert]
  rw [hinter]

/-- 受影响层 if 项 ≤ 新项 + 1（原项 ∈ {0,1}——平凡界）。 -/
lemma layer_g_le_insert_add_one (S : Finset (Fin 15)) (x : Fin 15)
    (L : Finset (Fin 15)) :
    (if L ∩ S = (∅ : Finset (Fin 15)) then 1 else 0)
      ≤ (if L ∩ insert x S = (∅ : Finset (Fin 15)) then 1 else 0) + 1 := by
  by_cases hnew : L ∩ insert x S = (∅ : Finset (Fin 15))
  <;> by_cases hold : L ∩ S = (∅ : Finset (Fin 15))
  <;> simp [hnew, hold]

/-- 静默窗口加入 ⟹ 完全活跃层数最多减 1：仅 x 所在层可能从完全活跃变非完全
    （其他层项相等——layer_g_eq_of_not_mem；受影响层平凡界——layer_g_le）。 -/
lemma fullActiveCount_le_insert_add_one (S : Finset (Fin 15)) (x : Fin 15) :
    fullActiveCount S ≤ fullActiveCount (insert x S) + 1 := by
  unfold fullActiveCount
  rcases layer_cover x with h1 | h2 | h3 | h4
  · -- x ∈ layer1：层 2/3/4 项相等、层 1 项 ≤ 新项 + 1
    have e2 := layer_g_eq_of_not_mem S layer2 (layer_disjoint_not_mem h1 layer1_disjoint_layer2)
    have e3 := layer_g_eq_of_not_mem S layer3 (layer_disjoint_not_mem h1 layer1_disjoint_layer3)
    have e4 := layer_g_eq_of_not_mem S layer4 (layer_disjoint_not_mem h1 layer1_disjoint_layer4)
    have l1 := layer_g_le_insert_add_one S x layer1
    omega
  · -- x ∈ layer2
    have e1 := layer_g_eq_of_not_mem S layer1 (layer_disjoint_not_mem h2 (by rw [Finset.inter_comm, layer1_disjoint_layer2]))
    have e3 := layer_g_eq_of_not_mem S layer3 (layer_disjoint_not_mem h2 layer2_disjoint_layer3)
    have e4 := layer_g_eq_of_not_mem S layer4 (layer_disjoint_not_mem h2 layer2_disjoint_layer4)
    have l2 := layer_g_le_insert_add_one S x layer2
    omega
  · -- x ∈ layer3
    have e1 := layer_g_eq_of_not_mem S layer1 (layer_disjoint_not_mem h3 (by rw [Finset.inter_comm, layer1_disjoint_layer3]))
    have e2 := layer_g_eq_of_not_mem S layer2 (layer_disjoint_not_mem h3 (by rw [Finset.inter_comm, layer2_disjoint_layer3]))
    have e4 := layer_g_eq_of_not_mem S layer4 (layer_disjoint_not_mem h3 layer3_disjoint_layer4)
    have l3 := layer_g_le_insert_add_one S x layer3
    omega
  · -- x ∈ layer4
    have e1 := layer_g_eq_of_not_mem S layer1 (layer_disjoint_not_mem h4 (by rw [Finset.inter_comm, layer1_disjoint_layer4]))
    have e2 := layer_g_eq_of_not_mem S layer2 (layer_disjoint_not_mem h4 (by rw [Finset.inter_comm, layer2_disjoint_layer4]))
    have e3 := layer_g_eq_of_not_mem S layer3 (layer_disjoint_not_mem h4 (by rw [Finset.inter_comm, layer3_disjoint_layer4]))
    have l4 := layer_g_le_insert_add_one S x layer4
    omega

/-- 单窗口静默 ⟹ orbitCount 不减少：S.card +1 且 fullActiveCount 最多 −1——净 ≥ 0。 -/
lemma silenceMonotone_single {S : Finset (Fin 15)} {x : Fin 15} (hx : x ∉ S) :
    orbitCount (silenceRec15_layered S) ≤ orbitCount (silenceRec15_layered (insert x S)) := by
  rw [orbitCount_layered, orbitCount_layered]
  have hc : (insert x S).card = S.card + 1 := Finset.card_insert_of_notMem hx
  have hf : fullActiveCount S ≤ fullActiveCount (insert x S) + 1 := fullActiveCount_le_insert_add_one S x
  rw [hc]
  omega

/-- ★ 静默单调定理：静默窗口增多 ⟹ 周期轨道数不减少。
    静默度-轨道数单调——'静默满额 → 恒等（orbitCount=15）'的连续谱
    离散骨架——对应 θ_F 距奇异极限（15°=SigmaInv°——m_e=0）的
    静默未满度（S302/S303——数值 26000 组零违例）。 -/
theorem silenceMonotone {S S' : Finset (Fin 15)} (hSS' : S ⊆ S') :
    orbitCount (silenceRec15_layered S) ≤ orbitCount (silenceRec15_layered S') := by
  classical
  have hSA : S ∪ (S' \ S) = S' := by
    ext x
    by_cases hx : x ∈ S
    · simp [hx]
      exact hSS' hx
    · simp [hx]
  let Q : Finset (Fin 15) → Prop := fun A =>
    (∀ x ∈ A, x ∉ S) → orbitCount (silenceRec15_layered S) ≤
      orbitCount (silenceRec15_layered (S ∪ A))
  have hAll : ∀ x ∈ S' \ S, x ∉ S := by
    intro x hx
    exact (Finset.mem_sdiff.mp hx).2
  have hQ : Q (S' \ S) := by
    refine Finset.induction_on (S' \ S) ?h0 ?hstep
    · -- 空差集：S ∪ ∅ = S
      intro _
      rw [Finset.union_empty]
    · -- 加回一个窗口 x：Q A ⟹ Q (insert x A)
      intro x A hxA ih
      intro hAll'
      have hxS : x ∉ S := hAll' x (by simp)
      have hsubA : ∀ y ∈ A, y ∉ S := fun y hy => hAll' y (by simp [hy])
      have ihA := ih hsubA
      have hsingle := silenceMonotone_single (S := S ∪ A) (x := x) (by simp [hxS, hxA])
      have hins : insert x (S ∪ A) = S ∪ insert x A := by
        ext y
        simp [Finset.mem_insert, Finset.mem_union]
      calc
        orbitCount (silenceRec15_layered S) ≤
            orbitCount (silenceRec15_layered (S ∪ A)) := ihA
        _ ≤ orbitCount (silenceRec15_layered (insert x (S ∪ A))) := hsingle
        _ = orbitCount (silenceRec15_layered (S ∪ insert x A)) := by rw [hins]
  rw [← hSA]
  exact hQ hAll

/-- 传递链：S ⊆ S' ⊆ S'' ⟹ orbitCount 逐级不减少（静默度单调传递）。 -/
theorem silenceMonotone_trans {S S' S'' : Finset (Fin 15)}
    (h1 : S ⊆ S') (h2 : S' ⊆ S'') :
    orbitCount (silenceRec15_layered S) ≤ orbitCount (silenceRec15_layered S'') := by
  exact le_trans (silenceMonotone h1) (silenceMonotone h2)

end MUFPF.PeriodicOrbitCount
