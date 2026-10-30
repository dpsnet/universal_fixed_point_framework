import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import MUFPFormalization.PeriodicOrbitCount

/-!
# 全锁定定理 OrbitFullLock：orbitCount = card ⟺ 恒等（全不动点）

对应 `notes/04_lorentz_gravity/偏心-周期轨道-简并度_论证骨架.md` §5b 候选 D 先证伪
（2026-10-23）。审阅发现：数值观察"g=15 ⟺ 全锁定极限"（15 只出现在全不动/近全不动）
实为可机检的**组合定理**：

> 定理（orbitCount_eq_card_iff_all_fixed）：有限自映射 X 上，
> orbitCount X = Fintype.card X.T  ⟺  ∀ x, X.step x = x（恒等）。

推论（物理对接）：在 15 窗口模型上，g = orbitCount = 15 ⟺ 窗口演化映射恒等
⟺ 15 个非平凡窗口**全部锁定且互不耦合**（各自不动点、无环、无共享轨道）。
任何非平凡映射（存在窗口转移/共享轨道）给 orbitCount ≤ card X.T − 1（≤ 14 on 15）。

证明结构：
- (⇒) all_fixed_of_orbitCount_eq_card：
  ① 全元素周期点：若有非周期点 x0，则周期点集真包含 ⟹ card < card X.T
     （Finset 真包含），又 orbitCount ≤ card P ⟹ 矛盾；
  ② 商集 card = P card（h + card P = card X.T）；
  ③ 固定 x：x 与 step x 同类（可达 n=1，step x 仍周期点）。反证不同 ⟹
     代表选择 g（右逆）单射、像 Finset 真包含 ⟹ card 矛盾 ⟹ 同类 ⟹ 相等。
- (⇐) orbitCount_eq_card_of_all_fixed：全不动点 ⟹ 全周期点（周期 1）⟹
  同类 ⟺ 同值（可达 ⟹ step^n x = x = y）⟹ 商 ≃ X.T ⟹ card 相等。

先证伪（数值，scripts/window_closure_explore_v2.py）：M1 恒等 =15、M9 近全不动 =15率
10%、任何自然模型 ≤14——与定理一致。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.PeriodicOrbitCount

open MUFPF.EccentricOrbit

/-- 周期点保持性：x 是周期点 ⟹ step x 也是周期点（同周期 p）。 -/
lemma step_periodic_of_periodic (X : RecObj) (x : X.T) (h : periodicPoint X x) :
    periodicPoint X (X.step x) := by
  rcases h with ⟨p, hp, hxp⟩
  refine ⟨p, hp, ?_⟩
  -- 辅助：step 与自身的任意次迭代交换（归纳，对一切 y）
  have hswap : ∀ k : ℕ, ∀ y : X.T, X.step^[k] (X.step y) = X.step (X.step^[k] y) := by
    intro k
    induction k with
    | zero => intro y; simp
    | succ k ih =>
      intro y
      calc
        X.step^[k.succ] (X.step y) = X.step^[k] (X.step (X.step y)) :=
          Function.iterate_succ_apply X.step k (X.step y)
        _ = X.step (X.step^[k] (X.step y)) := ih (X.step y)
        _ = X.step (X.step^[k.succ] y) := by
          rw [Function.iterate_succ_apply X.step k y]
  calc
    X.step^[p] (X.step x) = X.step (X.step^[p] x) := hswap p x
    _ = X.step x := by rw [hxp]

/-- 不动点迭代保持：全不动点 ⟹ 任意次迭代恒等。 -/
lemma iterate_id_of_all_fixed (X : RecObj) (hfix : ∀ x : X.T, X.step x = x)
    (n : ℕ) (x : X.T) : X.step^[n] x = x := by
  induction n with
  | zero => rfl
  | succ n ih =>
    calc
      X.step^[n.succ] x = X.step^[n] (X.step x) := Function.iterate_succ_apply X.step n x
      _ = X.step^[n] x := by rw [hfix x]
      _ = x := ih

/-- (⇐) 全不动点 ⟹ orbitCount = card X.T：商 ≃ X.T。 -/
theorem orbitCount_eq_card_of_all_fixed (X : RecObj)
    (hfix : ∀ x : X.T, X.step x = x) : orbitCount X = Fintype.card X.T := by
  classical
  have hall : ∀ x : X.T, periodicPoint X x := fun x => fixedPoint_is_periodicPoint X x (hfix x)
  -- 商映射单射：同类 ⟹ 同值（可达 + 全不动点 ⟹ 终点 = 起点）
  have hinjQ : Function.Injective
      (Quotient.mk (periodOrbitSetoid X) : {z : X.T // periodicPoint X z} → Quotient (periodOrbitSetoid X)) := by
    intro a b hab
    apply Subtype.ext
    have hrel : periodOrbitRel X a b := Quotient.exact hab
    rcases hrel with ⟨n, hn⟩
    calc
      a.1 = X.step^[n] a.1 := (iterate_id_of_all_fixed X hfix n a.1).symm
      _ = b.1 := hn
  have hsurjQ : Function.Surjective
      (Quotient.mk (periodOrbitSetoid X) : {z : X.T // periodicPoint X z} → Quotient (periodOrbitSetoid X)) :=
    quotient_mk_surj X
  have hcardQ : Fintype.card (Quotient (periodOrbitSetoid X)) =
      Fintype.card {z : X.T // periodicPoint X z} := by
    exact (Fintype.card_congr (Equiv.ofBijective (Quotient.mk (periodOrbitSetoid X)) ⟨hinjQ, hsurjQ⟩)).symm
  -- 全周期点 ⟹ P ≃ X.T（值投影双射）
  let p : {z : X.T // periodicPoint X z} → X.T := fun z => z.1
  have hinjP : Function.Injective p := by
    intro a b hab
    apply Subtype.ext
    exact hab
  have hsurjP : Function.Surjective p := by
    intro x
    exact ⟨⟨x, hall x⟩, rfl⟩
  have hcardP : Fintype.card {z : X.T // periodicPoint X z} = Fintype.card X.T := by
    exact Fintype.card_congr (Equiv.ofBijective p ⟨hinjP, hsurjP⟩)
  rw [orbitCount]
  exact hcardQ.trans hcardP

/-- (⇒) orbitCount = card X.T ⟹ 全不动点（恒等）。
    关键推论：任何非平凡映射（存在窗口转移）给 orbitCount < card X.T。 -/
theorem all_fixed_of_orbitCount_eq_card (X : RecObj)
    (h : orbitCount X = Fintype.card X.T) : ∀ x : X.T, X.step x = x := by
  classical
  -- ① 全元素周期点：若有非周期点 x0，则周期点集真包含（card_subtype_lt）
  --     ⟹ card P < card X.T ⟹ orbitCount < card X.T 矛盾
  have hall : ∀ x : X.T, periodicPoint X x := by
    by_contra hnotall
    rw [not_forall] at hnotall
    rcases hnotall with ⟨x0, hx0⟩
    have hcardP_lt : Fintype.card {z : X.T // periodicPoint X z} < Fintype.card X.T :=
      Fintype.card_subtype_lt (p := fun z : X.T => periodicPoint X z) (x := x0) hx0
    have hQ_le : Fintype.card (Quotient (periodOrbitSetoid X)) ≤
        Fintype.card {z : X.T // periodicPoint X z} :=
      Fintype.card_le_of_surjective (Quotient.mk (periodOrbitSetoid X)) (quotient_mk_surj X)
    have hlt : Fintype.card (Quotient (periodOrbitSetoid X)) < Fintype.card X.T :=
      lt_of_le_of_lt hQ_le hcardP_lt
    have hEQ : Fintype.card (Quotient (periodOrbitSetoid X)) = Fintype.card X.T := by
      rw [orbitCount] at h
      exact h
    exact (lt_irrefl (Fintype.card X.T)) (hEQ.symm ▸ hlt)
  -- ② card P = card X.T（全周期点 ⟹ P ≃ X.T）
  have hcardP : Fintype.card {z : X.T // periodicPoint X z} = Fintype.card X.T := by
    let p : {z : X.T // periodicPoint X z} → X.T := fun z => z.1
    have hinjP : Function.Injective p := by
      intro a b hab
      apply Subtype.ext
      exact hab
    have hsurjP : Function.Surjective p := by
      intro x
      exact ⟨⟨x, hall x⟩, rfl⟩
    exact Fintype.card_congr (Equiv.ofBijective p ⟨hinjP, hsurjP⟩)
  have hcardQ : Fintype.card (Quotient (periodOrbitSetoid X)) =
      Fintype.card {z : X.T // periodicPoint X z} := by
    rw [orbitCount] at h
    exact h.trans hcardP.symm
  -- ③ 固定 x：x 与 step x 同类（可达 n=1）⟹ 代表选择单射 + 像真包含 ⟹ 同类 ⟹ 相等
  intro x
  let a : {z : X.T // periodicPoint X z} := ⟨x, hall x⟩
  let b : {z : X.T // periodicPoint X z} := ⟨X.step x, step_periodic_of_periodic X x (hall x)⟩
  have hRel : periodOrbitRel X a b := by
    refine ⟨1, ?_⟩
    simp [a, b]
  have hmk : Quotient.mk (periodOrbitSetoid X) a = Quotient.mk (periodOrbitSetoid X) b :=
    Quotient.sound hRel
  have hab : a = b := by
    by_contra hne
    -- 代表选择 g：每个商类取一个代表（右逆，单射）
    let g : Quotient (periodOrbitSetoid X) → {z : X.T // periodicPoint X z} :=
      fun q => Classical.choose (quotient_mk_surj X q)
    have hg_spec (q : Quotient (periodOrbitSetoid X)) :
        Quotient.mk (periodOrbitSetoid X) (g q) = q :=
      Classical.choose_spec (quotient_mk_surj X q)
    have hg_inj : Function.Injective g := by
      intro q1 q2 hq
      calc
        q1 = Quotient.mk (periodOrbitSetoid X) (g q1) := (hg_spec q1).symm
        _ = Quotient.mk (periodOrbitSetoid X) (g q2) := by rw [hq]
        _ = q2 := hg_spec q2
    -- 像 Finset
    let t : Finset {z : X.T // periodicPoint X z} := Finset.univ.image g
    have ht_card : t.card = Fintype.card (Quotient (periodOrbitSetoid X)) := by
      simpa using Finset.card_image_of_injective (Finset.univ : Finset (Quotient (periodOrbitSetoid X))) hg_inj
    -- a、b 同类且 a ≠ b ⟹ 至少一个不在 g 像中
    have hab_img_false : a ∈ Set.range g ∧ b ∈ Set.range g → False := by
      intro habimg
      rcases habimg with ⟨⟨q1, hq1⟩, ⟨q2, hq2⟩⟩
      have hq1' : q1 = Quotient.mk (periodOrbitSetoid X) a := by
        calc
          q1 = Quotient.mk (periodOrbitSetoid X) (g q1) := (hg_spec q1).symm
          _ = Quotient.mk (periodOrbitSetoid X) a := by rw [hq1]
      have hq2' : q2 = Quotient.mk (periodOrbitSetoid X) b := by
        calc
          q2 = Quotient.mk (periodOrbitSetoid X) (g q2) := (hg_spec q2).symm
          _ = Quotient.mk (periodOrbitSetoid X) b := by rw [hq2]
      have hqeq : q1 = q2 := by
        rw [hq1', hq2', hmk]
      have : a = b := by
        rw [← hq1, ← hq2, hqeq]
      exact hne this
    let c : {z : X.T // periodicPoint X z} := if hc : a ∈ Set.range g then b else a
    have hc_not_img : c ∉ Set.range g := by
      by_cases hc : a ∈ Set.range g
      · have hc_eq : c = b := by simp [c, hc]
        rw [hc_eq]
        intro hb_img
        exact hab_img_false ⟨hc, hb_img⟩
      · have hc_eq : c = a := by simp [c, hc]
        rw [hc_eq]
        exact hc
    have hc_not_t : c ∉ t := by
      intro hct
      rcases Finset.mem_image.mp hct with ⟨q, _hquniv, hq⟩
      exact hc_not_img ⟨q, hq⟩
    have ht_lt : t.card < (Finset.univ : Finset {z : X.T // periodicPoint X z}).card := by
      apply Finset.card_lt_card
      rw [Finset.ssubset_iff_subset_ne]
      constructor
      · intro z hz
        exact Finset.mem_univ z
      · intro ht_eq
        have : c ∈ t := by
          rw [ht_eq]
          exact Finset.mem_univ c
        exact hc_not_t this
    have ht_lt_cardP : t.card < Fintype.card {z : X.T // periodicPoint X z} := by
      simpa using ht_lt
    have ht_card' : t.card = Fintype.card {z : X.T // periodicPoint X z} := by
      rw [ht_card]
      exact hcardQ
    exact (lt_irrefl (Fintype.card {z : X.T // periodicPoint X z})) (ht_card' ▸ ht_lt_cardP)
  have hx : x = X.step x := by
    simpa [a, b] using congrArg Subtype.val hab
  exact hx.symm

/-- 主定理：orbitCount = card ⟺ 恒等（全锁定）。
    审阅发现（2026-10-23）：候选 D 先证伪数值观察"g=15 ⟺ 全锁定"的定理版。 -/
theorem orbitCount_eq_card_iff_all_fixed (X : RecObj) :
    orbitCount X = Fintype.card X.T ↔ ∀ x : X.T, X.step x = x := by
  constructor
  · exact all_fixed_of_orbitCount_eq_card X
  · exact orbitCount_eq_card_of_all_fixed X

end MUFPF.PeriodicOrbitCount
