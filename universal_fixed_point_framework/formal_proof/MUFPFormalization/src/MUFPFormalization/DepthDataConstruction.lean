import Mathlib.Tactic
import Mathlib.Logic.Function.Iterate
import Mathlib.Data.Fintype.EquivFin
import MUFPFormalization.DepthExistence

/-!
# 第 52 批：把 `DepthData` 从「结构要求」变成「可构造的判据产物」

## 背景

第 48 批 `UniqueTerminalNecessity` 定义了 `DepthData`（八个字段），并证出
「有 `DepthData` ⇒ `|Fix| = 1` ⇒ 签名 `(3,1)`」。第 50 批 `DepthExistence` 把
`rho` 的**存在性**从「要求」换成判据 `rho 存在 ⟺ 时间无 k >= 2 折返`，但把
「`depth_exists` 的 `rho` 直接对接成 `DepthData` 实例」登记为 `: True`
（`depth_exists_meets_depthdata_deferred`），自认缺 `hinj` 与 `htop`。
第 48 批 `depth_is_a_requirement_not_a_consequence` 也仍写着「`rho` 的存在性未证」。

本批把这两条登记位换成真定理：

1. `enc_inj`：纯算术编码的单射性——`A * c + p = B * c + q` 且 `p, q < c`
   拆成 `A = B ∧ p = q`。这是把「(层号, 层内编号)」压进一个 `Nat` 的全部依据。
2. `hnat_zero_iff` / `hnat_step`：`h x`（从 `x` 到不动点的步数）为零当且仅当
   `x` 本身是不动点；非停住时前进一步恰好把 `h` 减一。
3. `depthdata_exists`（主定理）：**无折返 + 唯一不动点 ⇒ 存在 `DepthData`**。
   构造 `rho x = (card - h x) * (card + 1) + idx x`，`M = rho m`。
   - `hinj` 由 `enc_inj` + `idx` 的单射性给出（第 50 批缺的第一项）；
   - `htop` 是 `rfl`（`M` 就取 `rho m`）；
   - `hmax` 靠唯一不动点：非 `m` 的点必不是不动点，故 `h >= 1`，层号严格小；
   - `hprog` 靠 `hnat_step`：非顶层必严格前进；
   - `hstep` 由 `hprog` 与停住分支合并。
4. `depthdata_implies_unique_terminal`（必要性）：`DepthData` 存在 ⇒ 唯一不动点。
   ⇒ 与 3 合起来给出**双向判据**：`DepthData 存在 ⟺ 无折返 ∧ 唯一不动点`。
5. `twofix_no_depthdata`：`twofix` 满足无折返却**没有** `DepthData` ⇒
   必要性那条不是形式上的弱条件，唯一终点是真正的额外结构。

## 与第 48 / 50 批的关系

- 第 48 批 `depth_is_a_requirement_not_a_consequence`：**已过时**。`rho` 的存在性
  第 50 批已证（无折返时），本批进一步给出**八个字段全齐**的构造。
- 第 50 批 `depth_exists_meets_depthdata_deferred`：本批闭合。
- `DepthData.hinj` 不是第 50 批所说「做不到」的项，而是需要换一个编码：
  第 50 批的 `rho` 只记层号（`card - h x`），层内多点必然碰撞；本批补上层内编号 `idx`。

## 诚实边界

- 本批**不给**「唯一不动点」的来由：它仍由 `DepthData` / 时间单向承载，
  而不是由 `RecObj` 的四个字段推出（`twofix` 就是 `RecObj` 上的反例）。
- `card = 0` 时无对象可取（`m : R.T` 需要非空），本批陈述要求 `m` 存在，等价于非空。
-/

namespace MUFPF.DepthDataConstruction

open MUFPF.RecTime MUFPF.UniqueTerminal MUFPF.DepthExistence MUFPF.ActiveFixSignature

attribute [local instance] RecObj.fin RecObj.dec

/-! ## 一、纯算术：把「层号 × 层内编号」压进一个自然数 -/

/-- ★★★ **编码单射**：`c > 0`、`p < c`、`q < c` 时，
`A * c + p = B * c + q ⇒ A = B ∧ p = q`。

这是「层号 `A` 与层内编号 `p` 拼成一个自然数」不丢信息的全部依据。
证明只做两次比较：若 `A > B`，则 `B * c + q < (B+1) * c ≤ A * c ≤ A * c + p`，
与等式直接冲突。 -/
theorem enc_inj {c A B p q : ℕ} (_hc : 0 < c) (hp : p < c) (hq : q < c)
    (h : A * c + p = B * c + q) : A = B ∧ p = q := by
  have hAB : A ≤ B := by
    by_contra hnot
    have hBA : B < A := Nat.lt_of_not_le hnot
    have h1 : B * c + q < (B + 1) * c := by
      rw [Nat.succ_mul]
      exact Nat.add_lt_add_left hq (B * c)
    have h2 : (B + 1) * c ≤ A * c :=
      Nat.mul_le_mul_right c (by omega : B + 1 ≤ A)
    have h3 : A * c ≤ A * c + p := Nat.le_add_right _ _
    have h4 : B * c + q < B * c + q := by
      calc B * c + q < (B + 1) * c := h1
        _ ≤ A * c := h2
        _ ≤ A * c + p := h3
        _ = B * c + q := h
    exact absurd h4 (Nat.lt_irrefl _)
  have hBA' : B ≤ A := by
    by_contra hnot
    have hAB' : A < B := Nat.lt_of_not_le hnot
    have h1 : A * c + p < (A + 1) * c := by
      rw [Nat.succ_mul]
      exact Nat.add_lt_add_left hp (A * c)
    have h2 : (A + 1) * c ≤ B * c :=
      Nat.mul_le_mul_right c (by omega : A + 1 ≤ B)
    have h3 : B * c ≤ B * c + q := Nat.le_add_right _ _
    have h4 : B * c + q < B * c + q := by
      calc B * c + q = A * c + p := h.symm
        _ < (A + 1) * c := h1
        _ ≤ B * c := h2
        _ ≤ B * c + q := h3
    exact absurd h4 (Nat.lt_irrefl _)
  have hAeqB : A = B := Nat.le_antisymm hAB hBA'
  have hpq : p = q := by
    rw [hAeqB] at h
    exact Nat.add_left_cancel h
  exact ⟨hAeqB, hpq⟩

/-! ## 二、层内编号 -/

/-- 层内编号：用 `Fintype.equivFin` 把状态空间与 `Fin (card T)` 对齐。 -/
noncomputable def idx (R : RecObj) (x : R.T) : ℕ := (Fintype.equivFin R.T x).val

/-- 编号不超过 `card T`。 -/
theorem idx_lt (R : RecObj) (x : R.T) : idx R x < Fintype.card R.T :=
  (Fintype.equivFin R.T x).isLt

/-- 编号相同则状态相同（`Fintype.equivFin` 的单射性）。 -/
theorem idx_inj (R : RecObj) {x y : R.T} (h : idx R x = idx R y) : x = y := by
  have hfin : Fintype.equivFin R.T x = Fintype.equivFin R.T y := Fin.ext h
  exact (Fintype.equivFin R.T).injective hfin

/-! ## 三、`h x`：到不动点的步数 -/

/-- 从 `x` 出发首次到达不动点所需的步数（存在性由 `exists_fix_at` 保证）。 -/
noncomputable def hnat (R : RecObj) (h : NoNontrivialCycle R) (x : R.T) : ℕ :=
  Nat.find (exists_fix_at R h x)

/-- ★★ **`h x = 0` 当且仅当 `x` 已是不动点**。

证明全程在 `Nat.find` 层做（`show` 先把目标换成展开形式），
避免在 `rw` 里匹配 `hnat` 这个名字（名字层重写会因伸缩不同而失败）。 -/
theorem hnat_zero_iff (R : RecObj) (h : NoNontrivialCycle R) (x : R.T) :
    hnat R h x = 0 ↔ R.step x = x := by
  show Nat.find (exists_fix_at R h x) = 0 ↔ R.step x = x
  constructor
  · intro h0
    have hspec := (Nat.find_spec (exists_fix_at R h x)).2
    rw [h0] at hspec
    simpa using hspec
  · intro hx
    have hle : Nat.find (exists_fix_at R h x) ≤ 0 :=
      Nat.find_min' (exists_fix_at R h x) ⟨Nat.zero_le _, by simpa using hx⟩
    omega

/-- ★★ **非停住时，`h` 恰好减一**。

两个方向都只用 `Nat.find` 的最小性：一层给「`h x - 1` 处已停住」，
一层用 `Nat.find_min` 排除「更早就停住」。 -/
theorem hnat_step (R : RecObj) (h : NoNontrivialCycle R) (x : R.T)
    (hx : R.step x ≠ x) : hnat R h (R.step x) = hnat R h x - 1 := by
  show Nat.find (exists_fix_at R h (R.step x)) = Nat.find (exists_fix_at R h x) - 1
  have hpos : 0 < Nat.find (exists_fix_at R h x) := by
    rcases Nat.eq_zero_or_pos (Nat.find (exists_fix_at R h x)) with h0 | h1
    · exact absurd ((hnat_zero_iff R h x).mp h0) hx
    · exact h1
  have hslack : Nat.find (exists_fix_at R h x) ≤ Fintype.card R.T :=
    (Nat.find_spec (exists_fix_at R h x)).1
  apply le_antisymm
  · apply Nat.find_min' (exists_fix_at R h (R.step x))
    refine ⟨by omega, ?_⟩
    have hshift : (R.step)^[Nat.find (exists_fix_at R h x) - 1] (R.step x)
        = (R.step)^[Nat.find (exists_fix_at R h x)] x := by
      have hs := iterate_add_shift R (Nat.find (exists_fix_at R h x) - 1) 1 x
      have e : Nat.find (exists_fix_at R h x) - 1 + 1 = Nat.find (exists_fix_at R h x) :=
        Nat.sub_add_cancel hpos
      rw [e] at hs
      simpa using hs
    rw [hshift]
    exact (Nat.find_spec (exists_fix_at R h x)).2
  · by_contra hcon
    have hm : Nat.find (exists_fix_at R h (R.step x)) < Nat.find (exists_fix_at R h x) - 1 :=
      Nat.lt_of_not_le hcon
    have hlt : Nat.find (exists_fix_at R h (R.step x)) + 1 < Nat.find (exists_fix_at R h x) := by
      omega
    have hbad : R.step ((R.step)^[Nat.find (exists_fix_at R h (R.step x)) + 1] x)
        = (R.step)^[Nat.find (exists_fix_at R h (R.step x)) + 1] x := by
      have hspec2 := (Nat.find_spec (exists_fix_at R h (R.step x))).2
      have hshift : (R.step)^[Nat.find (exists_fix_at R h (R.step x)) + 1] x
          = (R.step)^[Nat.find (exists_fix_at R h (R.step x))] (R.step x) := by
        have hs := iterate_add_shift R (Nat.find (exists_fix_at R h (R.step x))) 1 x
        have hone : (R.step)^[1] x = R.step x := by simp
        rw [hone] at hs
        exact hs.symm
      rw [hshift]
      exact hspec2
    have hle : Nat.find (exists_fix_at R h (R.step x)) + 1 ≤ Fintype.card R.T := by
      have hs2 : Nat.find (exists_fix_at R h (R.step x)) ≤ Fintype.card R.T :=
        (Nat.find_spec (exists_fix_at R h (R.step x))).1
      omega
    exact (Nat.find_min (exists_fix_at R h x) hlt) ⟨hle, hbad⟩

/-! ## 四、深度函数：层号与层内编号拼接 -/

/-- 递增深度：`rho x = (card T - h x) * (card T + 1) + idx x`。

`card T - h x` 是层号（离不动点越近层号越大），`idx x` 是层内编号
（保证同一层的不同状态不碰撞）。 -/
noncomputable def depthRho (R : RecObj) (h : NoNontrivialCycle R) : R.T → ℕ :=
  fun x => (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1) + idx R x

/-- `depthRho` 的精确表达式（便于重写）。 -/
theorem depthRho_apply (R : RecObj) (h : NoNontrivialCycle R) (x : R.T) :
    depthRho R h x
      = (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1) + idx R x := rfl

/-- ★★★ **`depthRho` 是单射**——第 50 批登记位缺的第一项。 -/
theorem depthRho_inj (R : RecObj) (h : NoNontrivialCycle R) :
    Function.Injective (depthRho R h) := by
  intro x y hxy
  have hcpos : 0 < Fintype.card R.T + 1 := by omega
  have hpx : idx R x < Fintype.card R.T + 1 := by have := idx_lt R x; omega
  have hpy : idx R y < Fintype.card R.T + 1 := by have := idx_lt R y; omega
  have hsplit := enc_inj (c := Fintype.card R.T + 1) hcpos hpx hpy hxy
  exact idx_inj R hsplit.2

/-! ## 五、主定理：`DepthData` 存在 -/

/-- ★★★ **无折返 + 唯一不动点 ⇒ 存在 `DepthData`**。

`DepthData` 的八个字段全部就位：
`ρ`（`depthRho`）、`M`（`depthRho m`）、`m`、`hinj`（`depthRho_inj`）、
`hmax`（唯一不动点逼出「非 `m` 的点层号严格小」）、`htop`（`rfl`）、
`hprog`（`hnat_step`）、`hstep`（`hprog` 与停住分支合并）。 -/
theorem depthdata_exists (R : RecObj) (h : NoNontrivialCycle R)
    (m : R.T) (hm : R.step m = m) (huniq : ∀ x : R.T, R.step x = x → x = m) :
    Nonempty (DepthData R) := by
  classical
  have hcard_pos : 0 < Fintype.card R.T := Fintype.card_pos_iff.mpr ⟨m⟩
  -- 非 `m` 的点必不是不动点，因此 `h >= 1`
  have hge_one : ∀ x : R.T, x ≠ m → 1 ≤ hnat R h x := by
    intro x hx
    rcases Nat.eq_zero_or_pos (hnat R h x) with h0 | h1
    · exact absurd (huniq x ((hnat_zero_iff R h x).mp h0)) hx
    · exact h1
  -- 层号 × (card+1) 的单项式上界
  have hlayer_le : ∀ x : R.T, x ≠ m →
      Fintype.card R.T - hnat R h x ≤ Fintype.card R.T - 1 := by
    intro x hx
    exact Nat.sub_le_sub_left (hge_one x hx) _
  have hmul_eq : (Fintype.card R.T - 1) * (Fintype.card R.T + 1)
        + (Fintype.card R.T + 1)
      = Fintype.card R.T * (Fintype.card R.T + 1) := by
    have hc : (Fintype.card R.T - 1) * (Fintype.card R.T + 1)
          + 1 * (Fintype.card R.T + 1)
        = ((Fintype.card R.T - 1) + 1) * (Fintype.card R.T + 1) :=
      (Nat.add_mul _ _ _).symm
    rw [Nat.one_mul, Nat.sub_add_cancel hcard_pos] at hc
    exact hc
  have hmax_aux : ∀ x : R.T, x ≠ m → depthRho R h x < depthRho R h m := by
    intro x hx
    have hIdxm : idx R m ≤ Fintype.card R.T := by have := idx_lt R m; omega
    have hIdx : idx R x ≤ Fintype.card R.T := by have := idx_lt R x; omega
    have hpx : idx R x < Fintype.card R.T + 1 := by have := idx_lt R x; omega
    have h1 : (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1)
        ≤ (Fintype.card R.T - 1) * (Fintype.card R.T + 1) :=
      Nat.mul_le_mul_right _ (hlayer_le x hx)
    have h2 : (Fintype.card R.T - 1) * (Fintype.card R.T + 1) + idx R x
        < (Fintype.card R.T) * (Fintype.card R.T + 1) := by
      rw [← hmul_eq]
      exact Nat.add_lt_add_left hpx
        ((Fintype.card R.T - 1) * (Fintype.card R.T + 1))
    have hstrict : (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1) + idx R x
        < Fintype.card R.T * (Fintype.card R.T + 1) :=
      lt_of_le_of_lt (Nat.add_le_add_right h1 (idx R x)) h2
    have h3 : depthRho R h m = Fintype.card R.T * (Fintype.card R.T + 1) + idx R m := by
      have hzero : hnat R h m = 0 := (hnat_zero_iff R h m).mpr hm
      simp [depthRho, hzero]
    calc depthRho R h x
        = (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1) + idx R x := rfl
      _ < Fintype.card R.T * (Fintype.card R.T + 1) := hstrict
      _ ≤ Fintype.card R.T * (Fintype.card R.T + 1) + idx R m :=
          Nat.le_add_right (Fintype.card R.T * (Fintype.card R.T + 1)) (idx R m)
      _ = depthRho R h m := h3.symm
  -- 非顶层（即非 `m`）必严格前进
  have hprog_aux : ∀ x : R.T, depthRho R h x ≠ depthRho R h m →
      depthRho R h x < depthRho R h (R.step x) := by
    intro x hne
    have hxm : x ≠ m := by
      intro hx
      exact hne (by rw [hx])
    have hnefix : R.step x ≠ x := fun hfix => hxm (huniq x hfix)
    have hstepn := hnat_step R h x hnefix
    have hpx : idx R x < Fintype.card R.T + 1 := by have := idx_lt R x; omega
    have hkey : Fintype.card R.T - hnat R h (R.step x)
        = Fintype.card R.T - hnat R h x + 1 := by
      rw [hstepn]
      have hle : hnat R h x ≤ Fintype.card R.T :=
        (Nat.find_spec (exists_fix_at R h x)).1
      have hge : 1 ≤ hnat R h x := by
        rcases Nat.eq_zero_or_pos (hnat R h x) with h0 | h1
        · exact absurd ((hnat_zero_iff R h x).mp h0) hnefix
        · exact h1
      omega
    calc depthRho R h x
        = (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1) + idx R x := rfl
      _ < (Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1)
            + (Fintype.card R.T + 1) := by
          exact Nat.add_lt_add_left hpx
            ((Fintype.card R.T - hnat R h x) * (Fintype.card R.T + 1))
      _ = (Fintype.card R.T - hnat R h x + 1) * (Fintype.card R.T + 1) := by
          rw [Nat.succ_mul]
      _ = (Fintype.card R.T - hnat R h (R.step x)) * (Fintype.card R.T + 1) := by
          rw [hkey]
      _ ≤ (Fintype.card R.T - hnat R h (R.step x)) * (Fintype.card R.T + 1)
            + idx R (R.step x) := Nat.le_add_right _ _
      _ = depthRho R h (R.step x) := rfl
  refine ⟨{ ρ := depthRho R h
            M := depthRho R h m
            m := m
            hinj := depthRho_inj R h
            hmax := ?_
            htop := rfl
            hprog := hprog_aux
            hstep := ?_ }⟩
  · intro x
    by_cases hx : x = m
    · rw [hx]
    · exact le_of_lt (hmax_aux x hx)
  · intro x
    by_cases hfix : R.step x = x
    · exact Or.inr hfix
    · left
      have hne : depthRho R h x ≠ depthRho R h m := by
        intro heq
        have hxm : x = m := depthRho_inj R h heq
        have : R.step x = x := by rw [hxm]; exact hm
        exact hfix this
      exact hprog_aux x hne

/-! ## 六、必要性：`DepthData` 存在 ⇒ 唯一不动点 -/

/-- ★★★ **必要性**：存在 `DepthData` 的对象只有一个不动点。

这是第 48 批 `top_is_fixpoint` 与 `eq_top_of_fixpoint` 的直接合并：
前者说顶层必停住，后者说不止一个不动点就矛盾。 -/
theorem depthdata_implies_unique_terminal (R : RecObj) (D : DepthData R) :
    ∀ x : R.T, R.step x = x → x = D.m :=
  fun _ hx => eq_top_of_fixpoint D hx

/-- ★★★ **双向判据**（在无折返前提下）：
`DepthData` 存在 ⟺ 唯一不动点。

正向：`depthdata_exists`；反向：`depthdata_implies_unique_terminal`。
⇒ 第 48 批的「`rho` 是结构要求」与第 50 批的「八个字段缺两项」两句均不再成立：
`DepthData` 完全是「无折返 + 唯一终点」的产物。 -/
theorem depthdata_nonempty_iff (R : RecObj) (h : NoNontrivialCycle R)
    (m : R.T) (hm : R.step m = m) :
    Nonempty (DepthData R) ↔ ∀ x : R.T, R.step x = x → x = m := by
  constructor
  · rintro ⟨D⟩ x hx
    have htop : D.m = m := (eq_top_of_fixpoint D hm).symm
    calc x = D.m := eq_top_of_fixpoint D hx
      _ = m := htop
  · intro huniq
    exact depthdata_exists R h m hm huniq

/-! ## 七、反例：`twofix` 无折返却没有 `DepthData` -/

/-- ★★★ **`twofix` 满足无折返，但不存在 `DepthData`**。

第 48 批已证 `twofix` 的冻结集有两个点（`1` 与 `3`）。若存在 `DepthData`，
必要性会把它压成一个点，矛盾。⇒ 唯一终点不是形式上的装饰，
它正是「时间只有一条」这件事在结构上的位置。 -/
theorem twofix_no_depthdata : ¬ Nonempty (DepthData twofix) := by
  rintro ⟨D⟩
  have hc : fixCount twofix = 1 := fixCount_eq_one D
  have h2 : fixCount twofix = 2 := twofix_fix_two
  omega

end MUFPF.DepthDataConstruction
