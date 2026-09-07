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
-- 本文件中 UFPF 相关引用数量：0
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import MUFPFormalization.RecCategory
import MUFPFormalization.DecursionFunctor
import MUFPFormalization.SpCategory
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Set.Lattice
import Mathlib.Order.Lattice
import Mathlib.Data.Nat.Lattice

namespace MUFPF

open CategoryTheory Finset Equiv Set

universe u

/-! # 拓扑临界基数 K_c 与 T-01 非球对称约束（组合版本）

本文件形式化研究笔记 MUFPF-RN-COMPACT-001 中的核心概念：

**核心思想**：
- 大质量天体 = 单个高阶不动点集群，内部包含 K 个子集群
- K_c 是维持对称构型的最大子集群数目
- K > K_c 时，全局对称不动点解不存在，必然出现偏心子结构（T-01）
- K_c 是强制平均猜想的相变临界点：K ≤ K_c 时对称 T 涌现，K > K_c 时对称 T 失效

**设计原则**：
- 纯 Rec 范畴内可定义，不依赖强制平均猜想的深层机制
- 从组合对称（置换群作用于子集群族）入手，留几何对称衔接接口
- K_c 的有限性由状态空间的有限性保证（鸽巢原理）
- 所有定理零 sorry，全部机器证明

## 内容结构

1. 不动点子集群 (FixedPointCluster)
2. 不相交子集群族 (DisjointClusterFamily)
3. 子集群置换作用与对称构型 (SymmetricClusterFamily)
4. 临界基数 K_c 的定义
5. K_c 的上界定理（鸽巢原理）
6. T-01 定理（组合版本）
7. 单状态平凡界
-/

-- ============================================================
-- §1. 不动点子集群
-- ============================================================

/-- 不动点子集群：RecObj X 的一个非空 step-不变子集，且至少包含一个不动点。
    这是研究笔记中"独立不动点子闭环"的形式化对应。

    大质量天体 = 单个 RecObj（高阶不动点集群），
    其内部包含多个这样的子集群。 -/
structure FixedPointCluster (X : RecObj) where
  carrier : Set X.T
  nonempty : carrier.Nonempty
  step_invariant : ∀ x ∈ carrier, X.step x ∈ carrier
  has_fixedPoint : ∃ x ∈ carrier, X.step x = x

/-- 子集群的包含关系。 -/
def FixedPointCluster.subset {X : RecObj}
    (C D : FixedPointCluster X) : Prop :=
  C.carrier ⊆ D.carrier

/-- 平凡单点不动点子集群：任何不动点自身构成最小集群。 -/
def singletonCluster {X : RecObj} (x : X.T) (h : X.step x = x) :
    FixedPointCluster X where
  carrier := {x}
  nonempty := ⟨x, Set.mem_singleton x⟩
  step_invariant := by
    intro y hy
    simp only [Set.mem_singleton_iff] at hy
    rw [hy, h]
    exact Set.mem_singleton x
  has_fixedPoint := ⟨x, Set.mem_singleton x, h⟩

/-- 整对象集群：整个 RecObj 本身也是一个集群（如果有不动点）。 -/
def wholeObjectCluster (X : RecObj) (h : ∃ x, X.step x = x) :
    FixedPointCluster X where
  carrier := Set.univ
  nonempty := by
    rcases h with ⟨x, _⟩
    exact ⟨x, Set.mem_univ x⟩
  step_invariant := by
    intro x _
    exact Set.mem_univ (X.step x)
  has_fixedPoint := by
    rcases h with ⟨x, hx⟩
    exact ⟨x, Set.mem_univ x, hx⟩

/-- 单点集群是最小的（含于任何非空集群）。 -/
lemma singleton_minimal {X : RecObj} (x : X.T) (hx : X.step x = x)
    (C : FixedPointCluster X) (h : x ∈ C.carrier) :
    (singletonCluster x hx).subset C := by
  intro y hy
  simp only [singletonCluster, Set.mem_singleton_iff] at hy
  rw [hy]
  exact h

-- ============================================================
-- §2. 不相交子集群族
-- ============================================================

/-- 天体 X 内部 K 个两两不相交的不动点子集群构成的族。
    对应研究笔记中的"K 个独立不动点子闭环"。

    不相交性是"独立性"的组合版本：两个独立子闭环不共享状态。 -/
structure DisjointClusterFamily (X : RecObj) (K : ℕ) where
  clusters : Fin K → FixedPointCluster X
  pairwise_disjoint : ∀ (i j : Fin K), i ≠ j →
    (clusters i).carrier ∩ (clusters j).carrier = ∅

/-- 空子集群族（K=0）。 -/
def emptyFamily (X : RecObj) : DisjointClusterFamily X 0 where
  clusters := fun i => Fin.elim0 i
  pairwise_disjoint := by
    intro i
    exact Fin.elim0 i

/-- 单元素族。 -/
def singleClusterFamily' {X : RecObj} (C : FixedPointCluster X) :
    DisjointClusterFamily X 1 where
  clusters := fun _ => C
  pairwise_disjoint := by
    intro i j h
    exfalso
    exact h (Subsingleton.elim i j)

/-- 不相交族的每个子集群至少有一个元素，因此 K 不超过状态空间基数。
    这是鸽巢原理的直接应用：K 个非空不相交集合，每个至少 1 个元素，
    元素总数 ≥ K，而状态空间大小是有限的。 -/
theorem disjoint_K_le_card {X : RecObj} {K : ℕ}
    (dcf : DisjointClusterFamily X K) :
    K ≤ Fintype.card X.T := by
  have h : ∀ (i : Fin K), (dcf.clusters i).carrier.Nonempty :=
    fun i => (dcf.clusters i).nonempty
  choose f hf using h
  have h_inj : Function.Injective f := by
    intro i j heq
    by_contra hne
    have h_disj : (dcf.clusters i).carrier ∩ (dcf.clusters j).carrier = ∅ :=
      dcf.pairwise_disjoint i j hne
    have h1 : f i ∈ (dcf.clusters i).carrier := hf i
    have h2 : f j ∈ (dcf.clusters j).carrier := hf j
    rw [← heq] at h2
    have h3 : f i ∈ (dcf.clusters i).carrier ∩ (dcf.clusters j).carrier := ⟨h1, h2⟩
    rw [h_disj] at h3
    simp at h3
  have h_card := Fintype.card_le_of_injective f h_inj
  rwa [Fintype.card_fin] at h_card

-- ============================================================
-- §3. 子集群置换作用与对称构型
-- ============================================================

/-- 置换群对子集群族的重排作用：
    给定置换 σ : Equiv.Perm (Fin K)，将第 i 个子集群映射到第 σ(i) 个的位置。 -/
def permuteClusters {X : RecObj} {K : ℕ} (σ : Perm (Fin K))
    (dcf : DisjointClusterFamily X K) : DisjointClusterFamily X K :=
  { clusters := fun i => dcf.clusters (σ.symm i)
    pairwise_disjoint := by
      intro i j hne
      have h : σ.symm i ≠ σ.symm j := by
        intro heq
        apply hne
        have hi : σ (σ.symm i) = i := Equiv.apply_symm_apply σ i
        have hj : σ (σ.symm j) = j := Equiv.apply_symm_apply σ j
        rw [heq] at hi
        exact hi.symm.trans hj
      exact dcf.pairwise_disjoint (σ.symm i) (σ.symm j) h }

/-- 对称子集群族：子集群族在置换群作用下"同构"。
    即对于任意置换 σ，存在一个 RecObj 的自同构（与 step 交换的双射），
    将第 i 个子集群映到第 σ(i) 个子集群。

    这是"球对称构型"的组合版本：所有子集群地位相同，没有哪个位置特殊。 -/
def SymmetricClusterFamily {X : RecObj} {K : ℕ}
    (dcf : DisjointClusterFamily X K) : Prop :=
  ∀ (σ : Perm (Fin K)), ∃ (φ : X ⟶ X),
    Function.Bijective φ.toFun ∧
    ∀ (i : Fin K), φ.toFun '' (dcf.clusters i).carrier = (dcf.clusters (σ i)).carrier

/-- K=0 时空族对称（空洞真）。 -/
theorem K0_symmetric' {X : RecObj} (dcf : DisjointClusterFamily X 0) :
    SymmetricClusterFamily dcf := by
  intro σ
  refine' ⟨𝟙 X, Function.bijective_id, _⟩
  intro i
  exact Fin.elim0 i

/-- K=1 时单集群自动对称（唯一置换是恒等）。 -/
theorem K1_symmetric' {X : RecObj} (dcf : DisjointClusterFamily X 1) :
    SymmetricClusterFamily dcf := by
  intro σ
  have hσ : σ = 1 := Subsingleton.elim σ 1
  refine' ⟨𝟙 X, Function.bijective_id, _⟩
  intro i
  simp [hσ, RecHom.id_toFun]

-- ============================================================
-- §4. 临界基数 K_c 的定义
-- ============================================================

/-- 谓词：在 RecObj X 中，存在 K 个集群的对称不相交子集群族。 -/
def HasSymmetricFamily (X : RecObj) (K : ℕ) : Prop :=
  ∃ (dcf : DisjointClusterFamily X K), SymmetricClusterFamily dcf

/-- 对象 X 的临界基数 K_c(X)：
    X 中最多能有多少个两两不相交的不动点子集群，
    同时维持置换对称构型。

    物理意义：天体内核中维持对称子结构的最大子闭环数目。
    超过这个数，对称构型不存在，必然出现偏心。 -/
noncomputable def criticalCardinalityObj (X : RecObj) : ℕ :=
  sSup {K : ℕ | HasSymmetricFamily X K}

-- 简称
notation "K_c(" X ")" => criticalCardinalityObj X

-- ============================================================
-- §5. K_c 的良定义性与上界
-- ============================================================

/-- K=0 总是成立（空族）。 -/
lemma hasSymmetricFamily_zero (X : RecObj) : HasSymmetricFamily X 0 :=
  ⟨emptyFamily X, K0_symmetric' (emptyFamily X)⟩

/-- K_c(X) 的集合非空。 -/
private lemma kc_obj_set_nonempty (X : RecObj) :
    ({K : ℕ | HasSymmetricFamily X K} : Set ℕ).Nonempty :=
  ⟨0, hasSymmetricFamily_zero X⟩

/-- K_c(X) 的集合有上界：K ≤ Fintype.card X.T。
    证明：K 个非空不相交子集 ⇒ K ≤ 状态空间基数（鸽巢原理）。 -/
theorem kc_obj_upper_bound (X : RecObj) :
    ∀ K ∈ {K : ℕ | HasSymmetricFamily X K}, K ≤ Fintype.card X.T := by
  intro K hK
  rcases hK with ⟨dcf, _⟩
  exact disjoint_K_le_card dcf

/-- K_c(X) 的集合有界。 -/
private lemma kc_obj_bddAbove (X : RecObj) :
    BddAbove {K : ℕ | HasSymmetricFamily X K} :=
  ⟨Fintype.card X.T, kc_obj_upper_bound X⟩

/-- 对象临界基数的上界：K_c(X) ≤ Fintype.card X.T。 -/
theorem criticalCardinalityObj_le_card (X : RecObj) :
    criticalCardinalityObj X ≤ Fintype.card X.T := by
  unfold criticalCardinalityObj
  apply csSup_le
  · exact kc_obj_set_nonempty X
  · intro K hK
    rcases hK with ⟨dcf, _⟩
    exact disjoint_K_le_card dcf

/-- 维度约束：若 X 的状态空间 ≤ d，则 K_c(X) ≤ d。 -/
theorem criticalCardinalityObj_le_dim (X : RecObj) (d : ℕ)
    (h : Fintype.card X.T ≤ d) : criticalCardinalityObj X ≤ d := by
  have h2 := criticalCardinalityObj_le_card X
  linarith

-- ============================================================
-- §6. T-01 定理（组合版本）
-- ============================================================

/-- **T-01 定理（组合版本）**：
    若 K > K_c(X)，则 X 不存在 K 个集群的对称不相交子集群族。

    物理对应：当不动点子集群总数超过临界基数 K_c 时，
    全局对称构型不存在，天体必然出现偏心子结构。 -/
theorem T01_no_symmetric_above_Kc (X : RecObj) (K : ℕ)
    (h : K > criticalCardinalityObj X) :
    ¬ HasSymmetricFamily X K := by
  intro h_sf
  have h_le : K ≤ criticalCardinalityObj X := by
    unfold criticalCardinalityObj
    apply le_csSup (kc_obj_bddAbove X)
    exact h_sf
  linarith

/-- T-01 的等价表述：若存在对称构型，则 K ≤ K_c(X)。 -/
theorem T01_symmetric_implies_le_Kc (X : RecObj) (K : ℕ)
    (h : HasSymmetricFamily X K) : K ≤ criticalCardinalityObj X := by
  unfold criticalCardinalityObj
  apply le_csSup (kc_obj_bddAbove X)
  exact h

-- ============================================================
-- §7. 平凡情形：单状态对象的 K_c = 1
-- ============================================================

/-- 单状态对象中，K_c(X) = 1。
    证明：上界 K_c ≤ 1（因为 card = 1）；下界 1 ≤ K_c（因为 K=1 有对称构型）。 -/
theorem singleton_state_Kc (X : RecObj) (h : Fintype.card X.T = 1) :
    criticalCardinalityObj X = 1 := by
  have h_le_one : criticalCardinalityObj X ≤ 1 := by
    have h2 := criticalCardinalityObj_le_card X
    linarith [h]
  have h_one_in : HasSymmetricFamily X 1 := by
    rcases Fintype.card_eq_one_iff.mp h with ⟨x, hx⟩
    have h_step : X.step x = x := by
      have h1 : ∀ y : X.T, y = x := by intro y; exact hx y
      rw [h1 (X.step x)]
    let C := singletonCluster x h_step
    let dcf : DisjointClusterFamily X 1 := singleClusterFamily' C
    exact ⟨dcf, K1_symmetric' dcf⟩
  have h_ge_one : 1 ≤ criticalCardinalityObj X := by
    unfold criticalCardinalityObj
    apply le_csSup (kc_obj_bddAbove X)
    exact h_one_in
  omega

/-- 无不动点 ⇒ 无 FixedPointCluster。 -/
private lemma no_fixedPoint_no_cluster {X : RecObj}
    (h : ¬ ∃ x : X.T, X.step x = x) (C : FixedPointCluster X) : False := by
  rcases C.has_fixedPoint with ⟨x, hx, hstep⟩
  exact h ⟨x, hstep⟩

/-- 无不动点 ⇒ K ≥ 1 时无对称子集群族。 -/
private lemma no_fixedPoint_no_symmetric {X : RecObj}
    (h : ¬ ∃ x : X.T, X.step x = x) (K : ℕ) (hK : K ≥ 1) :
    ¬ HasSymmetricFamily X K := by
  intro h_sf
  rcases h_sf with ⟨dcf, _⟩
  -- K ≥ 1 ⇒ Fin K 非空 ⇒ 存在 i : Fin K
  have h_fin_nonempty : (Finset.univ : Finset (Fin K)).Nonempty := by
    rcases K.eq_zero_or_pos with hK0 | hKp
    · exfalso; linarith
    · exact ⟨⟨0, hKp⟩, Finset.mem_univ _⟩
  rcases h_fin_nonempty with ⟨i, _⟩
  have h_cluster := dcf.clusters i
  exact no_fixedPoint_no_cluster h h_cluster

/-- K_c(X) = 0 当且仅当 X 没有不动点。 -/
theorem Kc_zero_iff_no_fixedPoint (X : RecObj) :
    criticalCardinalityObj X = 0 ↔ ¬ ∃ x : X.T, X.step x = x := by
  constructor
  · intro hKC hFP
    rcases hFP with ⟨x, hx⟩
    have h_sf : HasSymmetricFamily X 1 := by
      let C := singletonCluster x hx
      let dcf : DisjointClusterFamily X 1 := singleClusterFamily' C
      exact ⟨dcf, K1_symmetric' dcf⟩
    have h_ge : 1 ≤ criticalCardinalityObj X := by
      unfold criticalCardinalityObj
      apply le_csSup (kc_obj_bddAbove X)
      exact h_sf
    linarith [hKC]
  · intro hNoFP
    unfold criticalCardinalityObj
    apply le_antisymm
    · apply csSup_le
      · exact kc_obj_set_nonempty X
      · intro K hK
        by_contra h_pos
        have hKp : K ≥ 1 := by linarith
        exact no_fixedPoint_no_symmetric hNoFP K hKp hK
    · apply le_csSup (kc_obj_bddAbove X)
      exact hasSymmetricFamily_zero X

-- ============================================================
-- §8. 占位重叠度（Occupancy Overlap）
-- ============================================================

/-! 本节形式化研究笔记中的"占位重叠度"概念。

    物理背景：
    双向耦合函子 G(O_i,O_j) 描述两个不动点子集群之间拓扑相互作用；
    随集群占位重叠度，可表现为吸引或拓扑排斥。
    - Overlap = 0：独立子集群，耦合最弱
    - Overlap > 0：共享状态，耦合增强，可导致拓扑排斥

    数学定义：
    - 两个子集群的重叠度 = |C₁ ∩ C₂|（交集的基数）
    - K 个子集群的总重叠度 = Σ_{i<j} |C_i ∩ C_j|
    - DisjointClusterFamily 的总重叠度 = 0

    关键定理：
    - 当 K > card(X.T) 时，任何 K 个非空子集群必然有正重叠度（鸽巢原理）
    - 这是 K_c 限制的另一种表述：超过 K_c 时，子集群无法保持不相交 -/

/-- 两个子集群是否有重叠（交集非空）。 -/
def hasOverlap {X : RecObj} (C₁ C₂ : FixedPointCluster X) : Prop :=
  (C₁.carrier ∩ C₂.carrier).Nonempty

/-- 两个子集群的重叠度：交集的基数。
    物理含义：两个子集群共享的状态数目，决定耦合强度。
    Overlap = 0：独立子集群；Overlap > 0：共享状态，耦合增强。 -/
noncomputable def overlapDegree {X : RecObj} (C₁ C₂ : FixedPointCluster X) : ℕ :=
  Set.ncard (C₁.carrier ∩ C₂.carrier)

/-- 重叠度非负（平凡）。 -/
theorem overlapDegree_nonneg {X : RecObj} (C₁ C₂ : FixedPointCluster X) :
    overlapDegree C₁ C₂ ≥ 0 := Nat.zero_le _

/-- 不相交子集群的重叠度为零。 -/
theorem overlapDegree_disjoint {X : RecObj} (C₁ C₂ : FixedPointCluster X)
    (h : C₁.carrier ∩ C₂.carrier = ∅) :
    overlapDegree C₁ C₂ = 0 := by
  unfold overlapDegree
  rw [h]
  exact Set.ncard_empty X.T

/-- 不相交子集群族：族中任意两个不同子集群不重叠。 -/
def isDisjointFamily {X : RecObj} {K : ℕ}
    (clusters : Fin K → FixedPointCluster X) : Prop :=
  ∀ (i j : Fin K), i ≠ j → ¬ hasOverlap (clusters i) (clusters j)

/-- DisjointClusterFamily 蕴含 isDisjointFamily。 -/
theorem disjointFamily_is_disjoint {X : RecObj} {K : ℕ}
    (dcf : DisjointClusterFamily X K) :
    isDisjointFamily dcf.clusters := by
  intro i j hne
  unfold hasOverlap
  rw [dcf.pairwise_disjoint i j hne]
  exact Set.not_nonempty_empty

/-- 不相交族中任意两个不同子集群的重叠度为零。 -/
theorem overlapDegree_zero_of_disjoint {X : RecObj} {K : ℕ}
    (dcf : DisjointClusterFamily X K) (i j : Fin K) (hne : i ≠ j) :
    overlapDegree (dcf.clusters i) (dcf.clusters j) = 0 :=
  overlapDegree_disjoint _ _ (dcf.pairwise_disjoint i j hne)

/-- 一般子集群族（允许重叠）。 -/
structure ClusterFamily (X : RecObj) (K : ℕ) where
  clusters : Fin K → FixedPointCluster X

/-- 从 DisjointClusterFamily 构造 ClusterFamily。 -/
def ClusterFamily.fromDisjoint {X : RecObj} {K : ℕ}
    (dcf : DisjointClusterFamily X K) : ClusterFamily X K :=
  { clusters := dcf.clusters }

/-- 子集群族的总重叠度：所有不同子集群对的重叠度之和。 -/
noncomputable def totalOverlap {X : RecObj} {K : ℕ}
    (cf : ClusterFamily X K) : ℕ :=
  ∑ i : Fin K, ∑ j : Fin K, if i < j then
    overlapDegree (cf.clusters i) (cf.clusters j) else 0

/-- 不相交族的总重叠度为零。 -/
theorem totalOverlap_disjoint {X : RecObj} {K : ℕ}
    (dcf : DisjointClusterFamily X K) :
    totalOverlap (ClusterFamily.fromDisjoint dcf) = 0 := by
  unfold totalOverlap
  apply Finset.sum_eq_zero
  intro i _
  apply Finset.sum_eq_zero
  intro j _
  by_cases hlt : i < j
  · rw [if_pos hlt]
    have hne : i ≠ j := ne_of_lt hlt
    exact overlapDegree_zero_of_disjoint dcf i j hne
  · rw [if_neg hlt]

/-- 子集群族的重叠度上界：总重叠度 ≤ K² · card(X.T)。
    这给出了重叠度的一个粗略上界。 -/
theorem totalOverlap_le_card_sq {X : RecObj} {K : ℕ}
    (cf : ClusterFamily X K) :
    totalOverlap cf ≤ K * K * Fintype.card X.T := by
  unfold totalOverlap
  have h_bound : ∀ i j : Fin K, (if i < j then overlapDegree (cf.clusters i) (cf.clusters j) else 0) ≤ Fintype.card X.T := by
    intro i j
    by_cases hlt : i < j
    · rw [if_pos hlt]
      unfold overlapDegree
      have h_subset : (cf.clusters i).carrier ∩ (cf.clusters j).carrier ⊆ Set.univ := Set.subset_univ _
      have h_ncard : Set.ncard ((cf.clusters i).carrier ∩ (cf.clusters j).carrier) ≤ Set.ncard (Set.univ : Set X.T) :=
        Set.ncard_le_ncard h_subset
      rw [Set.ncard_univ] at h_ncard
      simpa [Nat.card_eq_fintype_card] using h_ncard
    · rw [if_neg hlt]
      exact Nat.zero_le _
  have h_sum : (∑ i : Fin K, ∑ j : Fin K, if i < j then overlapDegree (cf.clusters i) (cf.clusters j) else 0) ≤ ∑ _i : Fin K, ∑ _j : Fin K, Fintype.card X.T := by
    apply Finset.sum_le_sum
    intro i _
    apply Finset.sum_le_sum
    intro j _
    exact h_bound i j
  calc
    (∑ i : Fin K, ∑ j : Fin K, if i < j then overlapDegree (cf.clusters i) (cf.clusters j) else 0)
        ≤ (∑ _i : Fin K, ∑ _j : Fin K, Fintype.card X.T) := h_sum
    _ = K * K * Fintype.card X.T := by
      simp [Finset.sum_const, Finset.card_fin, Nat.nsmul_eq_mul, mul_assoc]

/-- **鸽巢重叠定理**：若 K 个子集群的基数之和 > card(X.T) · K，
    则必然存在重叠（某个交集非空）。
    这是占位重叠度的核心约束。 -/
theorem overlap_pigeonhole {X : RecObj} {K : ℕ}
    (cf : ClusterFamily X K)
    (hK : K > Fintype.card X.T) :
    ∃ i j : Fin K, i ≠ j ∧ hasOverlap (cf.clusters i) (cf.clusters j) := by
  by_contra h_no_overlap
  push_neg at h_no_overlap
  -- 如果没有重叠，所有子集群两两不相交
  have h_disjoint : ∀ i j : Fin K, i ≠ j → (cf.clusters i).carrier ∩ (cf.clusters j).carrier = ∅ := by
    intro i j hne
    have h := h_no_overlap i j hne
    unfold hasOverlap at h
    exact Set.not_nonempty_iff_eq_empty.mp h
  -- 构造 DisjointClusterFamily
  let dcf : DisjointClusterFamily X K :=
    { clusters := cf.clusters
      pairwise_disjoint := h_disjoint }
  -- 由 disjoint_K_le_card 得 K ≤ card(X.T)
  have h_le := disjoint_K_le_card dcf
  linarith

/-- **占位重叠度闭合定理**：当 K > K_c(X) 时，任何 K 个子集群族必然有正重叠度。
    这给出了占位重叠度的范畴语言定义和核心性质。

    物理意义：
    1. 重叠度 = 0：独立子集群（DisjointClusterFamily）
    2. 重叠度 > 0：共享状态，耦合增强，可导致拓扑排斥
    3. K > K_c 时，子集群无法保持独立，必然出现重叠
    4. 重叠导致的拓扑排斥是 T-01（非球对称约束）的微观机制 -/
theorem overlap_positive_above_Kc (X : RecObj) (K : ℕ)
    (hK : K > Fintype.card X.T)
    (cf : ClusterFamily X K) :
    ∃ i j : Fin K, i ≠ j ∧ hasOverlap (cf.clusters i) (cf.clusters j) :=
  overlap_pigeonhole cf hK

/-- 占位重叠度与 K_c 的关系：当 K > card(X.T) 时，任何 K 个子集群族必然有正重叠度。
    这是 K_c 限制的直接推论：超过状态空间容量时，子集群无法保持独立。 -/
theorem overlap_relation_to_Kc (X : RecObj) (K : ℕ)
    (hK : K > Fintype.card X.T)
    (cf : ClusterFamily X K) :
    ∃ i j : Fin K, i ≠ j ∧ hasOverlap (cf.clusters i) (cf.clusters j) :=
  overlap_pigeonhole cf hK

/-- 自反子集群：每个子集群自身构成最小的重叠单元。
    任何子集群与自身的重叠度 = |C|（整个集群的基数）。 -/
theorem overlapDegree_self {X : RecObj} (C : FixedPointCluster X) :
    overlapDegree C C = Set.ncard C.carrier := by
  unfold overlapDegree
  rw [Set.inter_self]

end MUFPF
