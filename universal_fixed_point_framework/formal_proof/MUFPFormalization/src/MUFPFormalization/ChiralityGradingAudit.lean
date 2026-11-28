/-
MUFPF · 第 83 批 R-p：朝向比特的内生来源（手性分级）

第 82 批（`QuarterTurnQuantizationAudit`）把耦合块压到 0 个连续参数 + 1 个比特：
`B ∈ {1, −1, rotGen, −rotGen}`，非平凡耦合只剩「朝向」。

本批只问一件事：这个比特在框架内有没有判据，还是纯粹的外部赋号？
答案只用框架**已有**的反射生成元 `Isotropy.F = diag(1, −1)`（`ForceAverageIsotropy` L607，
原文即标为「手性/宇称翻转、`det = −1`、`O(2)\SO(2)` 代表元」），不引入任何新对象、新数。

结论：`F` 共轭把 `±1` 固定、把 `±rotGen` 互换 ⟹ 朝向比特 = `F`-共轭下的二分类（手性分级）；
且框架里 `Isotropy.J = −rotGen`，即两种朝向**本来就都在框架内**（互为相反数），
故 "哪一个为真" 是**赋号约定**而非数值缺口——本批把它明确登记为剩余二分。
-/
import MUFPFormalization.QuarterTurnQuantizationAudit
import MUFPFormalization.ForceAverageIsotropy

namespace MUFPF.ChiralityGradingAudit

open Matrix MUFPF.IntertwinerRepairAudit MUFPF.Isotropy

/-- ★ 判①：`F` 共轭固定单位阵。`F·1·F = 1`（因 `F² = 1`）。 -/
theorem conj_fixes_identity :
    Isotropy.F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * Isotropy.F = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Isotropy.F, Matrix.mul_apply, Fin.sum_univ_two]

/-- ★ 判②：`F` 共轭把耦合发生器翻号。`F·A·F = −A`（`A = rotGen`）。
    这正是「手性翻转」在矩阵层的最小见证：反射与旋转反交换。 -/
theorem conj_flips_rotGen :
    Isotropy.F * rotGen * Isotropy.F = -rotGen := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Isotropy.F, rotGen, Matrix.mul_apply, Fin.sum_univ_two, Matrix.neg_apply]

/-- ★ 判③：`F` 共轭在 `span{1, A}` 上是「翻 `δ` 号」。对任意 `a d : ℝ`，
    `F·(a·1+d·A)·F = a·1+(−d)·A`。故手性作用是**分级**而非一般线性变换。 -/
theorem conj_preserves_decomposition (a d : ℝ) :
    Isotropy.F * (a • (1 : Matrix (Fin 2) (Fin 2) ℝ) + d • rotGen) * Isotropy.F
      = a • (1 : Matrix (Fin 2) (Fin 2) ℝ) + (-d) • rotGen := by
  rw [Matrix.mul_add]
  rw [Matrix.mul_smul, Matrix.mul_smul]
  rw [Matrix.add_mul]
  rw [Matrix.smul_mul, Matrix.smul_mul]
  rw [conj_fixes_identity, conj_flips_rotGen]
  rw [smul_neg, neg_smul]

/-- 判③的推论：手性作用是**对合**（作用两次复原）。 -/
theorem chirality_involution (a d : ℝ) :
    Isotropy.F * (Isotropy.F *
        (a • (1 : Matrix (Fin 2) (Fin 2) ℝ) + d • rotGen) * Isotropy.F) * Isotropy.F
      = a • (1 : Matrix (Fin 2) (Fin 2) ℝ) + d • rotGen := by
  rw [conj_preserves_decomposition a d]
  simpa using conj_preserves_decomposition a (-d)

/-- ★ 判④：框架里两种朝向本来就都在。`Isotropy.J = −rotGen`。
    即 `J` 与 `rotGen` 只差一个整体符号——「朝向」不是新数，是符号约定的二选一。 -/
theorem J_eq_neg_rotGen : Isotropy.J = -rotGen := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Isotropy.J, rotGen, Matrix.neg_apply]

/-- 判⑤：`rotGen` 与其相反数**不同**（朝向比特非退化，不是同一个对象换写法）。 -/
theorem two_orientations_distinct : rotGen ≠ -rotGen := by
  intro h
  have h01 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
  norm_num [rotGen, Matrix.neg_apply] at h01

/-- 判⑥：非平凡耦合的**像集**恰是共轭对 `{rotGen, −rotGen}`，且 `F` 把它们互换。
    即第 82 批的比特在这组数据下表现为 `F`-共轭下的交换对。 -/
theorem conjugation_exchanges_nonrivial :
    Isotropy.F * rotGen * Isotropy.F = -(rotGen) ∧
      Isotropy.F * (-rotGen) * Isotropy.F = rotGen := by
  refine ⟨conj_flips_rotGen, ?_⟩
  have h := conj_flips_rotGen
  calc Isotropy.F * (-rotGen) * Isotropy.F
      = -(Isotropy.F * rotGen * Isotropy.F) := by simp
    _ = -(-rotGen) := by rw [h]
    _ = rotGen := by simp

/-- ★★ **判决**：朝向比特的判据**在框架内已有**（`F`-共轭分级），但符号本身是约定。
    四重合取：
    ① `F·1·F = 1`（标量类被固定）；
    ② `F·A·F = −A`（耦合类被翻号）；
    ③ `J = −A`（两种朝向都在框架内）；
    ④ 手性作用是对合。
    结论：这不是数值缺口，而是一条**赋号二分**——第 82 批的比特到此被解释为
    「反射共轭下的二分类」，无需外部数据；但 `+δ` 与 `−δ` 谁被实现，框架不偏置。 -/
theorem chirality_verdict :
    (Isotropy.F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * Isotropy.F = 1) ∧
    (Isotropy.F * rotGen * Isotropy.F = -rotGen) ∧
    (Isotropy.J = -rotGen) ∧
    (∀ a d : ℝ, Isotropy.F * (Isotropy.F *
        (a • (1 : Matrix (Fin 2) (Fin 2) ℝ) + d • rotGen) * Isotropy.F) * Isotropy.F
      = a • (1 : Matrix (Fin 2) (Fin 2) ℝ) + d • rotGen) :=
  ⟨conj_fixes_identity, conj_flips_rotGen, J_eq_neg_rotGen, chirality_involution⟩

end MUFPF.ChiralityGradingAudit
