/-
MUFPF · 第 85 批 R-r：赋号二分的真正原因 —— 标号置换破缺

第 84 批（`SignPinningAudit`）判定：赋号有判据（0 号槽的像落在哪一侧），但判据读的是槽标号，
故结论是「判据 = 标号约定」，与 §22 判 `T` 是登记约定同型。

本批把这句话变成**关于对称性的定理**，不再只是一个定性说法：

设 `swp = !![0,1;1,0]`（把两个槽互换的置换阵，即「标号重排」）。
若某个结构 `S` 对重排不变（`swp·S·swp = S`），它就**不可能**是 `rotGen` 或 `−rotGen`——
因为重排恰好把 `rotGen` 翻号。所以：

> 能定符号的对象必须**破缺**标号对称。

框架里确实有这种对象：反射生成元 `F = diag(1,−1)`（`swp·F·swp = −F ≠ F`）。
链于是闭合：定义（`F` 的条目写法）→ 破缺标号对称 → 定向 → 符号。
链上唯一的"选择"仍是 `F = diag(1,−1)` 这个写法本身，与 §22 的 `T` 同级。
-/
import MUFPFormalization.ChiralityGradingAudit

namespace MUFPF.OrientationBreakingAudit

open Matrix MUFPF.IntertwinerRepairAudit MUFPF.Isotropy MUFPF.ChiralityGradingAudit

/-- 标号置换：交换两个槽。`swp = !![0,1;1,0]`。 -/
def swp : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]

/-- 判①：置换是自逆的。`swp·swp = 1`。 -/
theorem swp_involutive : swp * swp = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [swp, Matrix.mul_apply, Fin.sum_univ_two]

/-- ★ 判②：重排把耦合发生器翻号。`swp·A·swp = −A`。
    即「换一下标号」就把朝向反过来——这条是整个判决的机检核心。 -/
theorem swp_conj_flips_rotGen : swp * rotGen * swp = -rotGen := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [swp, rotGen, Matrix.mul_apply, Fin.sum_univ_two, Matrix.neg_apply]

/-- ★ 判③：重排把反射生成元翻号。`swp·F·swp = −F`。
    故 `F` **破缺**标号对称——它是框架里那个"能看见方向"的对象。 -/
theorem swp_conj_flips_reflection : swp * Isotropy.F * swp = -Isotropy.F := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [swp, Isotropy.F, Matrix.mul_apply, Fin.sum_univ_two, Matrix.neg_apply]

/-- ★ 判④：`rotGen` 不是重排不变的（非退化）。 -/
theorem rotGen_not_swp_invariant : swp * rotGen * swp ≠ rotGen := by
  intro h
  have hflip := swp_conj_flips_rotGen
  rw [h] at hflip
  exact two_orientations_distinct hflip

/-- ★ 判⑤：`−rotGen` 同样不是重排不变的。 -/
theorem neg_rotGen_not_swp_invariant : swp * (-rotGen) * swp ≠ -rotGen := by
  intro h
  have hflip := swp_conj_flips_rotGen
  have h2 : swp * (-rotGen) * swp = rotGen := by
    calc swp * (-rotGen) * swp = -(swp * rotGen * swp) := by simp
      _ = -(-rotGen) := by rw [hflip]
      _ = rotGen := by simp
  rw [h2] at h
  exact two_orientations_distinct h

/-- ★ 判⑥：`F` 也不是重排不变的（破缺非退化）。 -/
theorem reflection_not_swp_invariant : swp * Isotropy.F * swp ≠ Isotropy.F := by
  intro h
  have hflip := swp_conj_flips_reflection
  rw [h] at hflip
  have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) hflip
  norm_num [Isotropy.F, Matrix.neg_apply] at h00

/-- ★★ **R-r 判决**：赋号二分之所以存在，是因为**标号对称必须被破缺**。
    五重合取：
    ① `swp` 自逆；
    ② 重排把 `rotGen` 翻号；
    ③ 重排把 `F` 翻号（`F` 是破缺对象）；
    ④ `±rotGen` 都不是重排不变的；
    ⑤ `F` 不是重排不变的。
    推论：任何尊重标号置换的结构都无法选中符号；框架里选中它的是 `F`，
    而 `F` 的写法（`diag(1,−1)`）是定义 ⟹ 链末端是定义，不是结构定理。 -/
theorem orientation_breaking_verdict :
    (swp * swp = 1) ∧
    (swp * rotGen * swp = -rotGen) ∧
    (swp * Isotropy.F * swp = -Isotropy.F) ∧
    (swp * rotGen * swp ≠ rotGen) ∧
    (swp * Isotropy.F * swp ≠ Isotropy.F) :=
  ⟨swp_involutive, swp_conj_flips_rotGen, swp_conj_flips_reflection,
    rotGen_not_swp_invariant, reflection_not_swp_invariant⟩

end MUFPF.OrientationBreakingAudit
