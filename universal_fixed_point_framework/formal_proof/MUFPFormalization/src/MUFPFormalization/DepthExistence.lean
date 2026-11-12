import Mathlib.Tactic
import Mathlib.Logic.Function.Iterate
import MUFPFormalization.RecCategory
import MUFPFormalization.RecTimeDepth
import MUFPFormalization.UniqueTerminalNecessity

/-!
# 第 50 批：深度函数 rho 的存在性——把「要求」换成「判据」

## 背景

第 48 批的 UniqueTerminalNecessity 把 |Fix| = 1 降为「时间单向」的推论，但把
rho（深度函数）的存在性登记为结构要求而非推论
（depth_is_a_requirement_not_a_consequence）。本批把这条登记换成真定理：

1. strict_depth_impossible：在有限对象上，严格递增的 rho 根本不存在。
   ⇒ 第 48 批 DepthData.hstep 里的 ∨ step x = x 分支不可省，
   不是笔误也不是宽松写法，而是有限性逼出来的唯一可行形式。
2. no_strict_pair：局部地，x 到 y 到 x 的 2-循环与「rho 在两点都严格递增」不相容。
   不依赖有限性，是纯序矛盾。
3. exists_repetition / exists_return：有限对象上，从任一点出发的轨道必然首次重复（抽屉原理）。
4. exists_fix_at：只要没有 k >= 2 周期，轨道在有限步内必然到达不动点。
5. depth_exists：主定理——无 k >= 2 周期 ⇒ 存在深度函数 rho。

⇒ 结论：第 48 批的登记位 depth_is_a_requirement_not_a_consequence 被替换为
「rho 存在 ⇐ 时间没有 k >= 2 的折返」，而反向（rho 存在 ⇒ 无折返）
由 no_strict_pair 型论证给出。rho 从「要求」变成「判据」。

## 诚实边界

主定理给的是递减约定（rho 沿 step 变小），与 DepthData.hprog 的递增约定差一次方向翻转
（rho 换成 card T - rho）。递增版未在本批单独写出，登记为 depth_exists_increasing_deferred。
-/

namespace MUFPF.DepthExistence

open MUFPF.RecTime MUFPF.UniqueTerminal

attribute [local instance] RecObj.fin RecObj.dec

/-- 「无非平凡周期」：轨道回到自身**只允许**因为已经停住。

形式化为：`step^[k] x = x`（k >= 2）⇒ `step x = x`。
即：长度 >= 2 的闭环只能是「撞在不动点上原地不动」，不允许「转一圈回到原处再继续」。
这是「时间不折返」的正确形式化——不动点算停住，不算折返。

注意：若写成 `step^[k] x ≠ x`（把不动点也排除），前提在有限对象上不可满足
（chain4 的 3 就是不动点），定理将变成空谈。 -/
def NoNontrivialCycle (R : RecObj) : Prop :=
  ∀ k : ℕ, 2 ≤ k → ∀ x : R.T, (R.step)^[k] x = x → R.step x = x

/-! ## 一、有限对象上严格递增深度不可能 -/

/-- 严格递增的深度函数在有限对象上不存在。

证明取 rho 的最大点 x0：∀x, rho x < rho (step x) 给出 rho x0 < rho (step x0)，
而最大性给出 rho (step x0) <= rho x0，矛盾。

⇒ 这条直接说明：DepthData.hstep 的 ∨ step x = x 分支是有限性的必然，
不是可省的宽松化。任何「每步都必须严格前进」的时间刻度在有限状态空间上不可能。 -/
theorem strict_depth_impossible (R : RecObj) (hne : Nonempty R.T) :
    ¬ ∃ ρ : R.T → ℕ, ∀ x, ρ x < ρ (R.step x) := by
  rintro ⟨ρ, h⟩
  obtain ⟨x₀, -, hmax⟩ :=
    Finset.exists_max_image (Finset.univ : Finset R.T) ρ Finset.univ_nonempty
  have h1 : ρ x₀ < ρ (R.step x₀) := h x₀
  have h2 : ρ (R.step x₀) ≤ ρ x₀ := hmax (R.step x₀) (Finset.mem_univ _)
  omega

/-- 推论：卡片数为正的 RecObj 上不存在「每步严格前进」的深度函数。 -/
theorem strict_depth_impossible_of_card_pos (R : RecObj) (hcard : 0 < Fintype.card R.T) :
    ¬ ∃ ρ : R.T → ℕ, ∀ x, ρ x < ρ (R.step x) := by
  have hne : Nonempty R.T := Fintype.card_pos_iff.mp hcard
  exact strict_depth_impossible R hne

/-! ## 二、局部 2-循环与严格递增不相容（不依赖有限性） -/

/-- 2-循环把严格递增直接掐死：若 x 到 y 到 x，则不存在 rho 同时在两点严格递增。

这条不依赖 Fintype，是纯序矛盾：rho x < rho y < rho x。
它是第 48 批 cycle_no_depth（针对 cyc3 的具体三步回环）的一般形式。 -/
theorem no_strict_pair (R : RecObj) (ρ : R.T → ℕ) {x y : R.T}
    (hx : R.step x = y) (hy : R.step y = x) :
    ¬ (ρ x < ρ (R.step x) ∧ ρ y < ρ (R.step y)) := by
  intro ⟨h1, h2⟩
  rw [hx] at h1
  rw [hy] at h2
  omega

/-- 更直白的版本：2-循环上「严格递增」这个要求本身自相矛盾。 -/
theorem loop_two_no_depth (R : RecObj) {x y : R.T}
    (hx : R.step x = y) (hy : R.step y = x) :
    ¬ ∃ ρ : R.T → ℕ, ∀ z, ρ z < ρ (R.step z) := by
  rintro ⟨ρ, h⟩
  exact no_strict_pair R ρ hx hy ⟨h x, h y⟩

/-! ## 三、有限对象上轨道必首次重复（构造 rho 的入口） -/

/-- 抽屉原理：有限对象上，从任一点出发的轨道 x, step x, step^[2] x, ...
在 card T + 1 步之内必然出现两次相同状态。 -/
theorem exists_repetition (R : RecObj) (x : R.T) :
    ∃ i j : Fin (Fintype.card R.T + 1), i ≠ j
      ∧ (R.step)^[i.val] x = (R.step)^[j.val] x := by
  have hlt : Fintype.card R.T < Fintype.card (Fin (Fintype.card R.T + 1)) := by
    rw [Fintype.card_fin]
    omega
  obtain ⟨i, j, hij, heq⟩ :=
    Fintype.exists_ne_map_eq_of_card_lt
      (fun i : Fin (Fintype.card R.T + 1) => (R.step)^[i.val] x) hlt
  exact ⟨i, j, hij, heq⟩

/-- 推论形式（带界）：存在 n < m <= card T 使 step^[n] x = step^[m] x。 -/
theorem exists_repetition_lt (R : RecObj) (x : R.T) :
    ∃ n m : ℕ, n < m ∧ m ≤ Fintype.card R.T ∧ (R.step)^[n] x = (R.step)^[m] x := by
  obtain ⟨i, j, hij, heq⟩ := exists_repetition R x
  have hval : i.val ≠ j.val := fun h => hij (Fin.ext h)
  have hi : i.val ≤ Fintype.card R.T := by have := i.isLt; omega
  have hj : j.val ≤ Fintype.card R.T := by have := j.isLt; omega
  rcases Nat.lt_or_gt_of_ne hval with hlt | hgt
  · exact ⟨i.val, j.val, hlt, hj, heq⟩
  · exact ⟨j.val, i.val, hgt, hi, heq.symm⟩

/-- 推论（带界）：轨道必出现一次「回到曾在过的状态」，回程步数 p 为正，
且出发步数 n 不超过 card T。 -/
theorem exists_return (R : RecObj) (x : R.T) :
    ∃ n p : ℕ, n ≤ Fintype.card R.T ∧ 0 < p
      ∧ (R.step)^[p] ((R.step)^[n] x) = (R.step)^[n] x := by
  obtain ⟨n, m, hlt, hmn, heq⟩ := exists_repetition_lt R x
  refine ⟨n, m - n, by omega, by omega, ?_⟩
  have hshift : (R.step)^[m] x = (R.step)^[(m - n)] ((R.step)^[n] x) := by
    calc (R.step)^[m] x = (R.step)^[(m - n) + n] x :=
          congrArg (fun k => (R.step)^[k] x) (by omega : m = m - n + n)
      _ = (R.step)^[(m - n)] ((R.step)^[n] x) :=
          Function.iterate_add_apply R.step (m - n) n x
  rw [hshift] at heq
  exact heq.symm

/-! ## 四、主定理：无 k >= 2 周期 ⇒ 存在深度函数 -/

/-- 轨道平移：`step^[k] (step x) = step^[k+1] x`。 -/
theorem iterate_shift (R : RecObj) (k : ℕ) (x : R.T) :
    (R.step)^[k] (R.step x) = (R.step)^[k + 1] x := by
  rw [show (R.step)^[k + 1] x = (R.step)^[k] ((R.step)^[1] x) from
      Function.iterate_add_apply R.step k 1 x]
  simp

/-- 轨道上必有一个停住点：只要不存在非平凡周期，
从任一点出发的轨道在有限步内一定到达某个不动点，且所需步数不超过 card T。

证明：exists_return 给出「走 n 步后，再走 p > 0 步回到原处」。
若 p >= 2，则 NoNontrivialCycle 直接给出 step y = y（y = step^[n] x），这就是目标；
若 p = 1，则 step y = y 就是 he 本身。 -/
theorem exists_fix_at (R : RecObj) (h : NoNontrivialCycle R) (x : R.T) :
    ∃ n : ℕ, n ≤ Fintype.card R.T ∧ R.step ((R.step)^[n] x) = (R.step)^[n] x := by
  obtain ⟨n, p, hn, hp, he⟩ := exists_return R x
  rcases Nat.lt_or_ge p 2 with h2 | h2
  · -- p = 1：he 本身就是「回到原处」，即停住
    have hp1 : p = 1 := by omega
    refine ⟨n, hn, ?_⟩
    rw [hp1] at he
    simpa using he
  · -- p >= 2：交给 NoNontrivialCycle
    exact ⟨n, hn, h p h2 ((R.step)^[n] x) he⟩

/-- 主定理：NoNontrivialCycle ⇒ 存在深度函数 rho，使每一点要么沿 step 变小、
要么已经停住。

构造：rho x := card T -（从 x 出发首次到达不动点所需的步数，Nat.find）。
rho x = 0 时 x 本身即不动点（右侧分支）；rho x > 0 时向前一步恰把所需步数减一
（左侧分支），这一步由 iterate_shift 与 Nat.find 的最小性给出。

⇒ 第 48 批的登记位 depth_is_a_requirement_not_a_consequence 在此被替换：
rho 的存在由「时间没有 k >= 2 的折返」保证，是可以证的。 -/
theorem depth_exists (R : RecObj) (h : NoNontrivialCycle R) :
    ∃ ρ : R.T → ℕ, ∀ x, ρ x < ρ (R.step x) ∨ R.step x = x := by
  classical
  have hex : ∀ x : R.T, ∃ n : ℕ,
      n ≤ Fintype.card R.T ∧ R.step ((R.step)^[n] x) = (R.step)^[n] x :=
    fun x => exists_fix_at R h x
  refine ⟨fun x => Fintype.card R.T - Nat.find (hex x), ?_⟩
  intro x
  have hspec := Nat.find_spec (hex x)
  have hbound := hspec.1
  have heqfix := hspec.2
  by_cases h0 : Nat.find (hex x) = 0
  · right
    rw [h0] at heqfix
    simpa using heqfix
  · left
    have hpos : 0 < Nat.find (hex x) := Nat.pos_of_ne_zero h0
    have hkey : Nat.find (hex (R.step x)) = Nat.find (hex x) - 1 := by
      apply le_antisymm
      · apply Nat.find_min' (hex (R.step x))
        refine ⟨by omega, ?_⟩
        have hs := iterate_shift R (Nat.find (hex x) - 1) x
        have e : Nat.find (hex x) - 1 + 1 = Nat.find (hex x) := Nat.sub_add_cancel hpos
        rw [hs, e]
        exact heqfix
      · by_contra hcon
        have hm : Nat.find (hex (R.step x)) < Nat.find (hex x) - 1 := Nat.lt_of_not_le hcon
        have hbad : R.step ((R.step)^[Nat.find (hex (R.step x)) + 1] x)
            = (R.step)^[Nat.find (hex (R.step x)) + 1] x := by
          have hspec2 := (Nat.find_spec (hex (R.step x))).2
          have hs := iterate_shift R (Nat.find (hex (R.step x))) x
          rw [hs] at hspec2
          exact hspec2
        exact (Nat.find_min (hex x)
          (by omega : Nat.find (hex (R.step x)) + 1 < Nat.find (hex x)))
          ⟨by omega, hbad⟩
    have hshow : Fintype.card R.T - Nat.find (hex x)
        < Fintype.card R.T - Nat.find (hex (R.step x)) := by
      rw [hkey]
      have h1 : Nat.find (hex x) ≤ Fintype.card R.T := hbound
      have h2 : 0 < Nat.find (hex x) := hpos
      have h3 : Nat.find (hex x) - 1 ≤ Fintype.card R.T := by omega
      omega
    exact hshow

/-! ## 五、配套引理：rho 沿轨道单调不减 -/

/-- 若 rho 满足「每步严格前进或已停住」，则 rho 沿整条轨道单调不减。

⇒ 这给出深度的物理读法：**时间不会让刻度倒退**。停住时相等，前进时严格变大。
这是把 rho 从「任意函数」升格为「时间刻度」的最小结构条件。 -/
theorem depth_mono (R : RecObj) (ρ : R.T → ℕ)
    (h : ∀ x, ρ x < ρ (R.step x) ∨ R.step x = x) :
    ∀ (x : R.T) (i : ℕ), ρ x ≤ ρ ((R.step)^[i] x) := by
  intro x i
  induction i with
  | zero => exact le_rfl
  | succ n ih =>
      have hstep : ρ ((R.step)^[n] x) ≤ ρ (R.step ((R.step)^[n] x)) := by
        rcases h ((R.step)^[n] x) with hlt | heq
        · exact le_of_lt hlt
        · exact le_of_eq (congrArg ρ heq.symm)
      calc ρ x ≤ ρ ((R.step)^[n] x) := ih
        _ ≤ ρ (R.step ((R.step)^[n] x)) := hstep
        _ = ρ ((R.step)^[n + 1] x) := by
              rw [← Function.iterate_succ_apply' R.step n x]

/-! ## 六、反向判据：rho 存在 ⇒ 时间不折返 -/

/-- 不动点的迭代仍是不动点。 -/
theorem iterate_of_fix (R : RecObj) {y : R.T} (hy : R.step y = y) (n : ℕ) :
    (R.step)^[n] y = y := by
  induction n with
  | zero => rfl
  | succ m ih =>
      rw [Function.iterate_succ_apply' R.step m y, ih, hy]

/-- 轨道拼接：先从 y 走 i 步、再走 k 步，等于从 y 一次走 k + i 步。 -/
theorem iterate_add_shift (R : RecObj) (k i : ℕ) (x : R.T) :
    (R.step)^[k] ((R.step)^[i] x) = (R.step)^[k + i] x :=
  (Function.iterate_add_apply R.step k i x).symm

/-- ★★★ **反向判据**：只要存在深度函数 rho（每步严格前进或已停住），
时间就不可能折返。

证明要点：设 f^[k] x = x（k >= 2）但 step x ≠ x。取 x 的最小正周期 p（p >= 2）。
周期内的任何一点都不能是不动点（否则在 p 步内回到 x 且该点停住，会把 p 逼小），
故周期内 p 步步步严格增大 rho；但 p 步后回到 x，rho 必须相等，矛盾。

⇒ 与 depth_exists 合起来：**rho 的存在 ⟺ 时间无 k >= 2 的折返**。
这正是第 48 批登记位 depth_is_a_requirement_not_a_consequence 所缺的判据。 -/
theorem no_cycle_of_depth (R : RecObj) (ρ : R.T → ℕ)
    (h : ∀ x, ρ x < ρ (R.step x) ∨ R.step x = x) :
    NoNontrivialCycle R := by
  classical
  intro k hk x hx
  by_contra hne
  have hex : ∃ n : ℕ, 0 < n ∧ (R.step)^[n] x = x := ⟨k, by omega, hx⟩
  set p := Nat.find hex with hpdef
  have hp1 : 0 < p := by rw [hpdef]; exact (Nat.find_spec hex).1
  have hpx : (R.step)^[p] x = x := by rw [hpdef]; exact (Nat.find_spec hex).2
  have hp2 : 2 ≤ p := by
    rcases Nat.lt_or_ge p 2 with hlt | hge
    · have hpe : p = 1 := by omega
      have hstep1 : R.step x = x := by
        have h1 : (R.step)^[1] x = x := by rw [← hpe]; exact hpx
        simpa using h1
      exact absurd hstep1 hne
    · exact hge
  -- 周期内的点都不是不动点
  have hnostop : ∀ i : ℕ, i < p → R.step ((R.step)^[i] x) ≠ (R.step)^[i] x := by
    intro i hi hstop
    have hsum : p - i + i = p := Nat.sub_add_cancel (by omega : i ≤ p)
    have h1 : (R.step)^[p - i] ((R.step)^[i] x) = x := by
      rw [iterate_add_shift R (p - i) i x, hsum, hpx]
    have h2 : (R.step)^[p - i] ((R.step)^[i] x) = (R.step)^[i] x :=
      iterate_of_fix R hstop (p - i)
    have hyx : (R.step)^[i] x = x := by rw [← h2, h1]
    rcases Nat.eq_or_lt_of_le (Nat.zero_le i) with hi0 | hipos
    · -- i = 0 时 y = x，直接得 step x = x，与 hne 矛盾
      rw [← hi0] at hstop
      exact hne (by simpa using hstop)
    · -- i > 0 时出现更小的正周期，与 p 最小矛盾
      exact (Nat.find_min hex (by omega : i < p)) ⟨hipos, hyx⟩
  -- 周期内步步严格增大
  have hstrict : ∀ i : ℕ, i < p → ρ ((R.step)^[i] x) < ρ ((R.step)^[i + 1] x) := by
    intro i hi
    rcases h ((R.step)^[i] x) with hlt | heq
    · rwa [← Function.iterate_succ_apply' R.step i x] at hlt
    · exact absurd heq (hnostop i hi)
  -- 于是 rho 在 p 步内至少增大 p
  have hchain : ∀ i : ℕ, i ≤ p → ρ x + i ≤ ρ ((R.step)^[i] x) := by
    intro i hi
    induction i with
    | zero => simp
    | succ n ih =>
        have hih := ih (by omega : n ≤ p)
        have hs := hstrict n (by omega : n < p)
        calc ρ x + (n + 1) = ρ x + n + 1 := by omega
          _ ≤ ρ ((R.step)^[n] x) + 1 := by omega
          _ ≤ ρ ((R.step)^[n + 1] x) := by omega
  have htop : ρ x + p ≤ ρ ((R.step)^[p] x) := hchain p (le_refl p)
  rw [hpx] at htop
  omega

/-! ## 七、登记：本批的边界 -/

/-- 登记位：本批主定理给的是「所需步数」的补（`ρ x = card T - 所需步数`），属**递增**形式，
与第 48 批 `DepthData.hprog : ρ x < ρ (R.step x)` 的约定一致。第一版曾写成递减形式
（`ρ := 所需步数`），机检同样通过但与 `DepthData` 反号，已改正。方向既然已定，
原先单列的 `depth_exists_increasing_deferred` 不再需要，其内容并入本条。
未做的部分：把 `depth_exists` 的 `ρ` 直接对接成 `DepthData` 实例
（缺 `hinj` 与 `htop`：`ρ` 只保证单调与有界，不保证单射与达最大）。 -/
theorem depth_exists_meets_depthdata_deferred : True := trivial

/-- 登记位：strict_depth_impossible 说明「严格递增深度」在有限对象上完全不可能，
因此第 48 批 DepthData 的 hstep 形式（允许停住）不是可选的宽松。 -/
theorem strict_depth_is_the_only_feasible_shape : True := trivial

end MUFPF.DepthExistence
