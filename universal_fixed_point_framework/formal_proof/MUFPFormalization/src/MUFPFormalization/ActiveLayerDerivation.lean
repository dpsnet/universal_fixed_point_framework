import Mathlib.Tactic
import MUFPFormalization.KMaxAlgebra

/-!
# ActiveLayerDerivation.lean — `N_active = 3` 的由来（不是注入）

## 问题

`N_active = 3` 在库里此前是 `def numActiveLayers : ℕ := 3`（公设 E3）。
本模块给出**另一条来由**：3 是两条**不含 3**的结构前提的**唯一结论**。

## 两条结构前提（都不含 3）

- **A｜Rec/Sp 幂-平方重合**：Rec 侧计数是 2 幂、Sp 侧几何是平方，
  两者在塔截断处必然重合 ⇒ `2^(k-2) = k²`。
  这是 `Rec ⊣ Sp` 对偶的代数读法（`4·k² = 2^k` 的等价形式）。
- **B｜Bott 翻倍**：截断指数是翻倍步数的 2 幂 ⇒ `k = 2^m`（`m` = 翻倍步数）。

## 结论链（两步都已机检）

1. `KMaxAlgebra.kmax_unique`：`2^(k-2) = k²` ⇒ `k = 8`（A 的**唯一**解）
2. 由 1 得 `2^m = 8`，再用 `KMaxAlgebra.two_pow_gt_linear`（`m ≥ 4` 时 `2^m > 2m+2 ≥ 10`）
   排除 `m ≥ 4`，`m ≤ 3` 穷举得 `m = 3`

⇒ **`m = 3` 是 A ∧ B 的唯一结论。3 不在任何前提里。**

## 不注入声明（可核对）

`active_layers_derived` 的证明体**只使用** `RecSpOverlap`、`BottDoubling`、`hk2 : 2 ≤ k`
与 `KMaxAlgebra` 的两条引理；**不引用** `Unified3Theorem.numActiveLayers`、
`DHStructuralAnalysis.N_active`、`ActiveMorphismLayer` 的任何构造子计数。
⇒ 3 不是被写死的，是被方程逼出来的。

## 边界（必须一并陈述）

- A 与 B 是**结构前提**，本模块**不证明**它们、也不把它们设为 axiom。
  本模块证的是：「若 A ∧ B 成立，则 `m = 3` **唯一**」。
- **`k_max = 8` 的地位随之改变**：不再是纯约定——A 一旦成立，`k = 8` 是 A 的唯一解
  （`kmax_forced_by_overlap` 机检）。这是对 `BottTower`「`k_max := spinorDim 0` 是约定」
  那一定位的**加强而非推翻**：约定仍在（`def k_max := spinorDim 0`），但 A 给出一条
  独立的强制路径。
- **退化解已排除**：`k = 1` 时 Nat 截断使 `1 - 2 = 0`，`2^0 = 1 = 1²` 也满足 A，
  且 `B` 给 `m = 0`。故陈述中必须带 `2 ≤ k`，否则 A ∧ B 有 `(k,m) = (1,0)` 这第二个解。
  数值扫描（`pr634na_derive.py`）曾漏掉 k=1，本模块把该反例显式钉在前提里。
- 本模块**不涉及**态射塔高（`SpTowerUnbounded.tower_height_unbounded_B` 仍是 ∞）——
  那说的是「层结构可递归构造到任意层」，与「翻倍步数 = 3」不是同一件事。
- **A 的候选空间已归位（第 27 批）**：新模块 `OverlapClosedLayerOrigin.lean` 机检了
  `OverlapClosedLayer.overlap_on_closed_layers`。依据是库里一条与本模块无关的既有定理
  `SigmaIntersectionBottTower.sigma_intersection_closed`：σ 交汇方程
  `N·(2j − N) = 2^j − 1` 的解只有 `j ∈ {1,2,4}`，即 `k_max = 2j ∈ {2,4,8}`。
  A 在该集合上**唯一**于 `k = 8` 成立（`overlap_neg_two` / `overlap_neg_four` /
  `overlap_pos_eight`）。⇒ A 从「对任意 k 的假设」降为「在三候选中筛选」。
  该定理配套的 `bound_prod : N·(2j−N) = j² − (N−j)² ≤ j²` 同时给出「Sp 侧平方」的
  代数来源：`j²` 是二次型的极大值，等号取在对称点 `N = j`。
  **A 仍未证**，且「为什么框架必须要求『二次型极值 = Rec 2 幂』」仍未闭合。
-/

namespace MUFPF.ActiveLayerDerivation

open MUFPF.BottTower

/-! ## 结构前提 -/

/-- **结构前提 A**：Rec 侧 2 幂 与 Sp 侧平方 在塔截断处重合（`4·k² = 2^k` 的等价形式）。 -/
def RecSpOverlap (k : ℕ) : Prop := 2 ^ (k - 2) = k ^ 2

/-- **结构前提 B**：截断指数是翻倍步数的 2 幂（`m` = Bott 翻倍步数）。 -/
def BottDoubling (k m : ℕ) : Prop := k = 2 ^ m

/-! ## 主定理 -/

/-- ★ **`N_active = 3` 的由来**：A ∧ B ∧ `2 ≤ k` ⟹ 翻倍步数 `m = 3`（唯一）。

    证明体不引用 `numActiveLayers` / `N_active` / `ActiveMorphismLayer`。
    `2 ≤ k` 用于排除退化解 `(k,m) = (1,0)`（见模块头「边界」段）。 -/
theorem active_layers_derived {k m : ℕ}
    (hA : RecSpOverlap k) (hB : BottDoubling k m) (hk2 : 2 ≤ k) : m = 3 := by
  -- 第 1 步：A 的唯一解是 k = 8
  have hk8 : k = 8 := MUFPF.KMaxAlgebra.kmax_unique k hk2 hA
  -- 第 2 步：由 B 与 k = 8 得 2^m = 8
  have hpow : 2 ^ m = 8 := by
    rw [← hB, hk8]
  -- 第 3 步：排除 m ≥ 4（2^m 增长快于 2m+2）
  have hle : m ≤ 3 := by
    by_contra h
    have h4 : 4 ≤ m := by omega
    have hgt : 2 ^ m > 2 * m + 2 := MUFPF.KMaxAlgebra.two_pow_gt_linear m h4
    omega
  -- 第 4 步：m ≤ 3 穷举
  interval_cases m
  · norm_num at hpow
  · norm_num at hpow
  · norm_num at hpow
  · rfl

/-- **`k_max = 8` 由 A 强制**：A 一旦成立，截断指数只能是 `k_max`。

    这把 `k_max = 8` 从「纯约定」加强为「A 的唯一解」。
    约定仍在（`def k_max := spinorDim 0`），但 A 给出独立强制路径。 -/
theorem kmax_forced_by_overlap {k : ℕ} (hk2 : 2 ≤ k) (hA : RecSpOverlap k) :
    k = k_max :=
  MUFPF.KMaxAlgebra.kmax_is_unique_solution k hk2 hA

/-- 与既有公设的一致性：A ∧ B ∧ `k = k_max` 时，得到的 `m` 等于 `3`，
    且 `3 = Fintype.card Unified3.ActiveMorphismLayer`（既有构造子计数）。

    本条只做**一致性衔接**，不构成本模块的推导依据。 -/
theorem derived_matches_carded {m : ℕ}
    (hA : RecSpOverlap k_max) (hB : BottDoubling k_max m) : m = 3 ∧
    3 = Fintype.card MUFPF.Unified3.ActiveMorphismLayer := by
  refine ⟨?_, MUFPF.KMaxAlgebra.power_unique_matches_active_layers⟩
  exact active_layers_derived hA hB (by norm_num [k_max_value])

end MUFPF.ActiveLayerDerivation

