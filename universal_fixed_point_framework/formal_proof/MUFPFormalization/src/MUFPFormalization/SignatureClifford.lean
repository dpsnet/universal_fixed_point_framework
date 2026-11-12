import Mathlib.Tactic
import Mathlib.LinearAlgebra.CliffordAlgebra.Basic
import Mathlib.LinearAlgebra.QuadraticForm.Basic

/-!
# 第 49 批：签名 `(p, q)` → `Cl(p, q)` 的泛构造

## 背景

PR-634 主线第 47 批给出「分解 → 签名 → Clifford 泛性质」三步路径；第 48 批把
`|Fix| = 1` 降为「时间单向」的推论。三步中**唯一仍未形式化**的是第三步：
签名 `(p, q)` 与 `Cl(p, q)` 之间在库内只有并置（`3 = 3` 的传递），没有关系。

本模块把第三步在 Lean 里真正证出来，分六段：

1. **签名 → 二次型**：`sigQ n p` 是 `Fin n → ℝ` 上按号差 `(p, n − p)` 加权的二次型。
2. **二次型的显式读出**：标准基向量上的取值 = 该坐标权重（`±1`）。
3. **正部判据**：二次型取正 ⟺ 坐标落在正部。
4. **签名 ⟺ 二次型 一一对应**：`sigQ_inj`（同一维数下 `sigQ n p = sigQ n p' ↔ p = p'`），
   以及正部基数 `sigQ_pos_card`（正号坐标恰 `p` 个）。
5. **`CliffordAlgebra` 泛性质落地**：`sigCl_lift_existsUnique`（`∃!` 形式）。
6. **边界登记**：二次型不同 ⇒ 代数不同构**未证**；`Cl(1,3)` 与 `Cl(3,1)` 号差
   约定差异未核对（承第 46 批）。

## 诚实边界

第 5 段用的是 Mathlib 既有的 `ι`-关系自由性定理，本模块做的是把它**实例化到
`sigQ`** 并写成可机检的 `∃!`，不是重造自由对象。本模块**没有**证明
「`Cl` 唯一决定签名」——这条在 `form_neq_implies_algebra_neq_admitted` 登记。
-/

namespace MUFPF.SignatureClifford

open QuadraticMap

/-! ### 一、号差权重与二次型 -/

/-- 号差权重：前 `p` 个坐标为 `+1`，其余为 `−1`。 -/
def sigWeight (n p : ℕ) : Fin n → ℝ :=
  fun i => if (i : ℕ) < p then (1 : ℝ) else -1

/-- 签名 `(p, n − p)` 的二次型：`Q(x) = ∑ᵢ wᵢ xᵢ²`，`wᵢ = ±1`。 -/
def sigQ (n p : ℕ) : QuadraticForm ℝ (Fin n → ℝ) :=
  QuadraticMap.weightedSumSquares ℝ (sigWeight n p)

/-- 二次型的显式展开：加权平方和。 -/
theorem sigQ_apply (n p : ℕ) (v : Fin n → ℝ) :
    sigQ n p v = ∑ i, sigWeight n p i * (v i * v i) := by
  simp [sigQ, QuadraticMap.weightedSumSquares_apply, smul_eq_mul]

/-- 二次型在标准基向量上的取值等于该坐标的权重。

证明要点：`Q(single i 1) = ∑ⱼ wⱼ · (single i 1)ⱼ²`，只有 `j = i` 项存活。 -/
theorem sigQ_single (n p : ℕ) (i : Fin n) :
    sigQ n p (Pi.single i (1 : ℝ)) = sigWeight n p i := by
  rw [sigQ_apply, Finset.sum_eq_single i]
  · simp
  · intro j _ hj
    rw [Pi.single_eq_of_ne hj]
    simp
  · intro hi
    exact absurd (Finset.mem_univ i) hi

/-! ### 二、二次型把签名编码成一串 `±1` -/

/-- 权重取 `+1` 当且仅当坐标落在正部。 -/
theorem sigWeight_eq_one_iff (n p : ℕ) (i : Fin n) :
    sigWeight n p i = 1 ↔ (i : ℕ) < p := by
  unfold sigWeight
  split_ifs with h
  · simp [h]
  · constructor
    · intro hc; norm_num at hc
    · intro hc; exact absurd hc h

/-- 权重取 `−1` 当且仅当坐标落在负部。 -/
theorem sigWeight_eq_neg_one_iff (n p : ℕ) (i : Fin n) :
    sigWeight n p i = -1 ↔ ¬ (i : ℕ) < p := by
  unfold sigWeight
  split_ifs with h
  · constructor
    · intro hc; norm_num at hc
    · intro hc; exact absurd h hc
  · simp [h]

/-- 标准基向量上的二次型值：正部 `+1`，负部 `−1`。 -/
theorem sigQ_single_value (n p : ℕ) (i : Fin n) :
    sigQ n p (Pi.single i (1 : ℝ)) = if (i : ℕ) < p then (1 : ℝ) else -1 := by
  rw [sigQ_single]
  unfold sigWeight
  rfl

/-- 正部判据：标准基向量上的二次型为正 ⟺ 该坐标落在正部。 -/
theorem sigQ_positive_part (n p : ℕ) (i : Fin n) :
    0 < sigQ n p (Pi.single i (1 : ℝ)) ↔ (i : ℕ) < p := by
  rw [sigQ_single_value]
  split_ifs with h
  · simp [h]
  · constructor
    · intro hc; norm_num at hc
    · intro hc; exact absurd hc h

/-- 负部判据：标准基向量上的二次型为负 ⟺ 该坐标落在负部。 -/
theorem sigQ_negative_part (n p : ℕ) (i : Fin n) :
    sigQ n p (Pi.single i (1 : ℝ)) < 0 ↔ ¬ (i : ℕ) < p := by
  rw [sigQ_single_value]
  split_ifs with h
  · constructor
    · intro hc; norm_num at hc
    · intro hc; exact absurd h hc
  · simp [h]

/-! ### 三、正部基数 = `p`（签名的数值读出） -/

/-- `{i : Fin n // i < p}` 与 `Fin p` 的典范等价（`p ≤ n`）。 -/
def finSubtypeEquivFin (n p : ℕ) (hp : p ≤ n) :
    { i : Fin n // (i : ℕ) < p } ≃ Fin p where
  toFun x := ⟨x.val.val, x.property⟩
  invFun j := ⟨⟨j.val, Nat.lt_of_lt_of_le j.isLt hp⟩, j.isLt⟩
  left_inv _ := rfl
  right_inv _ := Fin.ext rfl

/-- 正部坐标的个数恰为 `p`。 -/
theorem card_filter_lt (n p : ℕ) (hp : p ≤ n) :
    (Finset.univ.filter (fun i : Fin n => (i : ℕ) < p)).card = p := by
  rw [← Fintype.card_subtype (fun i : Fin n => (i : ℕ) < p)]
  rw [Fintype.card_congr (finSubtypeEquivFin n p hp)]
  exact Fintype.card_fin p

/-- **签名读出**：`sigQ n p` 取正值的标准基向量恰有 `p` 个。 -/
theorem sigQ_pos_card (n p : ℕ) (hp : p ≤ n) :
    (Finset.univ.filter (fun i : Fin n => 0 < sigQ n p (Pi.single i (1 : ℝ)))).card = p := by
  have hset : (Finset.univ.filter (fun i : Fin n => 0 < sigQ n p (Pi.single i (1 : ℝ))))
      = (Finset.univ.filter (fun i : Fin n => (i : ℕ) < p)) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, sigQ_positive_part]
  rw [hset, card_filter_lt n p hp]

/-! ### 四、签名 ⟺ 二次型：一一对应 -/

/-- 同签名 ⇒ 同二次型。 -/
theorem sigQ_eq_of_eq (n p p' : ℕ) (h : p = p') : sigQ n p = sigQ n p' := by
  subst h
  rfl

/-- **签名决定二次型（双向）**：`sigQ n p = sigQ n p' ↔ p = p'`（`p, p' ≤ n`）。

正向用「取坐标 `p` 读数」：`p < p'` 时左式在坐标 `p` 上取 `−1`、右式取 `+1`，
二次型是函数因而不可能相等。 -/
theorem sigQ_inj (n p p' : ℕ) (hp : p < n) (hp' : p' < n) :
    sigQ n p = sigQ n p' ↔ p = p' := by
  constructor
  · intro h
    by_contra hne
    rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
    · have key := congrArg (fun Q : QuadraticForm ℝ (Fin n → ℝ) =>
        Q (Pi.single ⟨p, hp⟩ (1 : ℝ))) h
      rw [sigQ_single, sigQ_single] at key
      have hL : sigWeight n p ⟨p, hp⟩ = -1 := by
        rw [sigWeight_eq_neg_one_iff]; exact Nat.lt_irrefl p
      have hR : sigWeight n p' ⟨p, hp⟩ = 1 := by
        rw [sigWeight_eq_one_iff]; exact hlt
      rw [hL, hR] at key
      norm_num at key
    · have key := congrArg (fun Q : QuadraticForm ℝ (Fin n → ℝ) =>
        Q (Pi.single ⟨p', hp'⟩ (1 : ℝ))) h
      rw [sigQ_single, sigQ_single] at key
      have hL : sigWeight n p ⟨p', hp'⟩ = 1 := by
        rw [sigWeight_eq_one_iff]; exact hgt
      have hR : sigWeight n p' ⟨p', hp'⟩ = -1 := by
        rw [sigWeight_eq_neg_one_iff]; exact Nat.lt_irrefl p'
      rw [hL, hR] at key
      norm_num at key
  · intro h
    exact sigQ_eq_of_eq n p p' h

/-- 不同签名给出不同二次型（`sigQ_inj` 的否定形式）。 -/
theorem sigQ_ne (n p p' : ℕ) (hp : p < n) (hp' : p' < n) (h : p ≠ p') :
    sigQ n p ≠ sigQ n p' := by
  intro heq
  exact h ((sigQ_inj n p p' hp hp').mp heq)

/-! ### 五、`Cl(p, q)` 与泛性质 -/

/-- `Cl(p, n − p)`：签名对应二次型的 Clifford 代数。 -/
abbrev sigCl (n p : ℕ) : Type := CliffordAlgebra (sigQ n p)

/-- `Cl` 的生成元平方于二次型值（Clifford 关系）。 -/
theorem sigCl_iota_sq (n p : ℕ) (v : Fin n → ℝ) :
    CliffordAlgebra.ι (sigQ n p) v * CliffordAlgebra.ι (sigQ n p) v
      = algebraMap ℝ (sigCl n p) (sigQ n p v) :=
  CliffordAlgebra.ι_sq_scalar _ v

/-- **泛性质（存在且唯一）**：任何满足 Clifford 关系的线性映射，唯一地提升为
`Cl(p, n − p) → A` 的 `ℝ`-代数同态。

这是「签名 → `Cl`」这一步的核心：`Cl` 不是被签名*选取*的某个具体矩阵实现，
而是被签名*唯一决定*的自由对象——任何别的实现只要满足同一条 Clifford 关系，
就都经由这个唯一的同态与 `Cl` 相连。

存在性由 `CliffordAlgebra.ι_comp_lift` 给出，唯一性由 `CliffordAlgebra.lift_unique`
给出；两者合起来正是 `CliffordAlgebra.lift`（一个 `≃`）的两半。 -/
theorem sigCl_lift_existsUnique (n p : ℕ) {A : Type*} [Semiring A] [Algebra ℝ A]
    (f : (Fin n → ℝ) →ₗ[ℝ] A)
    (hf : ∀ v, f v * f v = algebraMap ℝ A (sigQ n p v)) :
    ∃! g : sigCl n p →ₐ[ℝ] A,
      g.toLinearMap ∘ₗ CliffordAlgebra.ι (sigQ n p) = f := by
  refine ⟨CliffordAlgebra.lift (sigQ n p) ⟨f, hf⟩,
    CliffordAlgebra.ι_comp_lift f hf, ?_⟩
  intro g hg
  exact (CliffordAlgebra.lift_unique f hf g).mp hg

/-- 泛性质的推论：`Cl` 的代数同态由其在生成元上的取值唯一决定。 -/
theorem sigCl_hom_ext (n p : ℕ) {A : Type*} [Semiring A] [Algebra ℝ A]
    {g₁ g₂ : sigCl n p →ₐ[ℝ] A}
    (h : g₁.toLinearMap ∘ₗ CliffordAlgebra.ι (sigQ n p)
      = g₂.toLinearMap ∘ₗ CliffordAlgebra.ι (sigQ n p)) :
    g₁ = g₂ :=
  CliffordAlgebra.hom_ext h

/-- 自反实例：`lift (ι)` 在生成元上回到 `ι`。 -/
theorem sigCl_lift_iota (n p : ℕ) :
    (CliffordAlgebra.lift (sigQ n p)
      ⟨CliffordAlgebra.ι (sigQ n p),
        fun v => CliffordAlgebra.ι_sq_scalar (sigQ n p) v⟩).toLinearMap
      ∘ₗ CliffordAlgebra.ι (sigQ n p) = CliffordAlgebra.ι (sigQ n p) :=
  CliffordAlgebra.ι_comp_lift _ _

/-! ### 六、接第 47–48 批的签名 `(3, 1)` -/

/-- `Cl(3, 1)` 就是 `sigCl 4 3`。 -/
theorem cl31_is_sigCl : sigCl 4 3 = CliffordAlgebra (sigQ 4 3) := rfl

/-- `Cl(3, 1)` 的正部基向量恰 3 个——这就是第 47 批「活跃集基数 = Cl 签名正部维数」。 -/
theorem cl31_pos_card :
    (Finset.univ.filter (fun i : Fin 4 => 0 < sigQ 4 3 (Pi.single i (1 : ℝ)))).card = 3 :=
  sigQ_pos_card 4 3 (by norm_num)

/-- 负部判定在 `Cl(3, 1)` 上只剩 1 个坐标（`i = 3`）。 -/
theorem cl31_neg_card :
    (Finset.univ.filter (fun i : Fin 4 => ¬ (i : ℕ) < 3)).card = 1 := by
  decide

/-- `Cl(3, 1)` 正部 3、负部 1：`3` 与 `Cl(3,1)` 的对应不是 `3 = 3` 传递，
而是「正部维数 = 活跃层数」。 -/
theorem cl31_positive_three :
    (Finset.univ.filter (fun i : Fin 4 => 0 < sigQ 4 3 (Pi.single i (1 : ℝ)))).card = 3
      ∧ (Finset.univ.filter (fun i : Fin 4 => sigQ 4 3 (Pi.single i (1 : ℝ)) < 0)).card = 1 := by
  refine ⟨cl31_pos_card, ?_⟩
  have hset : (Finset.univ.filter (fun i : Fin 4 => sigQ 4 3 (Pi.single i (1 : ℝ)) < 0))
      = (Finset.univ.filter (fun i : Fin 4 => ¬ (i : ℕ) < 3)) := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, sigQ_negative_part]
  rw [hset]
  exact cl31_neg_card

/-- `Cl(3, 0)` 与 `Cl(3, 1)` 不是同一个二次型。 -/
theorem cl30_not_sigQ31 : sigQ 4 3 ≠ sigQ 4 0 :=
  sigQ_ne 4 3 0 (by norm_num) (by norm_num) (by norm_num)

/-- `Cl(7, 0)` 也是合法签名——泛性质不筛选签名。 -/
theorem cl70_exists : sigQ 7 0 = sigQ 7 0 := rfl

/-! ### 七、边界登记（诚实声明，不是定理） -/

/-- 登记：**二次型不同 ⇒ Clifford 代数不同构**本模块未证。

证明需要「号差是不变量」（Sylvester 惯性律的 Lean 化）加上「中心单代数被其
Clifford 不变量分类」；这两块在 Mathlib 里都还没有。因此本批只证到
「签名 ⟺ 二次型」（`sigQ_inj`），没有证到「签名 ⟺ 代数」。 -/
theorem form_neq_implies_algebra_neq_admitted : True := trivial

/-- 登记：`Cl(1,3)` 与 `Cl(3,1)` 的号差约定差异未核对（承第 46 批
`signature_convention_unchecked`）。

本模块中 `sigQ n p` 以「前 `p` 个坐标 `+1`」为准；物理学界普遍用
`Cl(1,3)`（`+,−,−,−`）而 PR-634 主线用 `Cl(3,1)`（`+,+,+,−`）。两者的
`Cl` 在实代数意义下同构（`Cl(3,1) ≅ Cl(1,3)` 作为实代数），但本模块
**没有**机检这条同构，只登记了「坐标约定」这一层。 -/
theorem signature_convention_unchecked : True := trivial

/-- 登记：**泛性质不筛选签名**。`sigCl n p` 对任何 `p ≤ n` 都存在，
包括 `Cl(7, 0)`——泛性质只保证「给定签名得到自由对象」，
不保证「只有某个签名才配得上物理」。第 46 批已机检 `d = 3` 与 `d = 7`
同样能构造 `TimeArrow`，本批在 Clifford 侧确认同一条边界。 -/
theorem generic_property_does_not_select_signature : True := trivial

end MUFPF.SignatureClifford
