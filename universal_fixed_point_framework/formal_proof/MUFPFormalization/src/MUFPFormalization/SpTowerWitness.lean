-- ============================================================
-- B 相层 2–5 的具体实例链（塔高 ≥ 5 的机检见证）
-- ============================================================
-- `SpFiveLayer.lean` 补了层 5 的结构与「判据层号无关」，但层 2–5 从未在 B 相
-- 被**逐层串起来**——「塔高 ≥ 5」当时只能靠判据同形外推。本模块把 R4 构造
-- （A_X = A_Y = A_Z = J₃、Q = 1 + J₃、h = diag(0,1,2)）在 Lean 里显式落地：
--
--   P = 1, Q = 1 + J₃            (两个 SpHom)
--   2-态射：α.homotopy = diag(0,1,2)、β.homotopy = diag(0,1,2) + J₃
--   3-态射：secondHomotopy 取同一对取值（diag(0,1,2) / +J₃）
--   4-态射：thirdHomotopy 同上
--   5-态射：fourthHomotopy = diag(0,1,2) ≠ 0        ⇒ 层 5 有非零态射
--
-- 关键代数事实（层 2 的 condition）：
--   ad_{J₃}(diag(0,1,2)) = J₃（D36 已证）
--   ad_{J₃}(J₃) = 0      （`jordan3_mem_ker`）
--   ⇒ ad_{J₃}(diag(0,1,2) + J₃) = J₃  ⇒ 两个 2-态射的 condition 都满足
--
-- 边界：本模块证明的是「层 5 存在非零态射」⇒ B 相塔高 **≥ 5**；不证明「层 6 不可穿」
-- （库内无层 6 结构），故「恰为 5」同样不入定理。
-- ============================================================

import MUFPFormalization.SpFiveLayer

namespace MUFPF

open Matrix MUFPFormalization

/-- B 相的对象：`A = J₃`。用 `abbrev`（`def` 会让 `Fin n` 上的 `OfNat` 无法 synth）。 -/
abbrev jordan3SpObj : SpObj := ⟨3, jordan3⟩

/-- 层 2 的左端：`ad_{J₃}(diag(0,1,2) + J₃) = J₃`。
    `ad` 线性 + `ad_{J₃}(J₃) = 0` ⇒ 结论。 -/
lemma adLin_jordan3_shiftDiag3_add :
    adLin jordan3 (shiftDiag3 + jordan3) = jordan3 := by
  have hker : adLin jordan3 jordan3 = 0 := by simpa using jordan3_mem_ker
  rw [map_add, adLin_jordan3_shiftDiag3, hker]
  simp

/-- 恒等 `SpHom`（`P = 1`）。 -/
def idJ3 : SpHom jordan3SpObj jordan3SpObj where
  P := 1
  intertwine := by simp

/-- `Q = 1 + J₃`（R4 构造里的 `Q`）：与 `A = J₃` 交换——展开后两侧同为 `J₃ + J₃²`，无需幂零性。 -/
def qJ3 : SpHom jordan3SpObj jordan3SpObj where
  P := 1 + jordan3
  intertwine := by
    show (1 + jordan3) * jordan3 = jordan3 * (1 + jordan3)
    rw [Matrix.mul_add, Matrix.add_mul, Matrix.one_mul, Matrix.mul_one]

/-- 层 2 态射 α：`homotopy = diag(0,1,2)`。 -/
def two0 : SpTwoMorphism (idJ3 : SpHom jordan3SpObj jordan3SpObj) qJ3 where
  homotopy := shiftDiag3
  condition := by
    show (1 + jordan3) - (1 : Matrix (Fin 3) (Fin 3) ℂ) =
      jordan3 * shiftDiag3 - shiftDiag3 * jordan3
    rw [show (1 + jordan3) - (1 : Matrix (Fin 3) (Fin 3) ℂ) = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3.symm

/-- 层 2 态射 β：`homotopy = diag(0,1,2) + J₃`（仍在 `ker` 之外但 condition 相同）。 -/
def two1 : SpTwoMorphism (idJ3 : SpHom jordan3SpObj jordan3SpObj) qJ3 where
  homotopy := shiftDiag3 + jordan3
  condition := by
    show (1 + jordan3) - (1 : Matrix (Fin 3) (Fin 3) ℂ) =
      jordan3 * (shiftDiag3 + jordan3) - (shiftDiag3 + jordan3) * jordan3
    rw [show (1 + jordan3) - (1 : Matrix (Fin 3) (Fin 3) ℂ) = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3_add.symm

/-- 层 3 态射 Ξ：`secondHomotopy = diag(0,1,2)`，右端 `β − α = J₃`。 -/
def three0 : SpThreeMorphism two0 two1 where
  secondHomotopy := shiftDiag3
  condition := by
    show (shiftDiag3 + jordan3) - shiftDiag3 =
      jordan3 * shiftDiag3 - shiftDiag3 * jordan3
    rw [show (shiftDiag3 + jordan3) - shiftDiag3 = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3.symm

/-- 层 3 态射 Τ：`secondHomotopy = diag(0,1,2) + J₃`。 -/
def three1 : SpThreeMorphism two0 two1 where
  secondHomotopy := shiftDiag3 + jordan3
  condition := by
    show (shiftDiag3 + jordan3) - shiftDiag3 =
      jordan3 * (shiftDiag3 + jordan3) - (shiftDiag3 + jordan3) * jordan3
    rw [show (shiftDiag3 + jordan3) - shiftDiag3 = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3_add.symm

/-- 层 4 态射 Χ：`thirdHomotopy = diag(0,1,2)`。 -/
def four0 : SpFourMorphism three0 three1 where
  thirdHomotopy := shiftDiag3
  condition := by
    show (shiftDiag3 + jordan3) - shiftDiag3 =
      jordan3 * shiftDiag3 - shiftDiag3 * jordan3
    rw [show (shiftDiag3 + jordan3) - shiftDiag3 = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3.symm

/-- 层 4 态射 Ω：`thirdHomotopy = diag(0,1,2) + J₃`。 -/
def four1 : SpFourMorphism three0 three1 where
  thirdHomotopy := shiftDiag3 + jordan3
  condition := by
    show (shiftDiag3 + jordan3) - shiftDiag3 =
      jordan3 * (shiftDiag3 + jordan3) - (shiftDiag3 + jordan3) * jordan3
    rw [show (shiftDiag3 + jordan3) - shiftDiag3 = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3_add.symm

/-- **层 5 存在非零态射（B 相塔高 ≥ 5）**：`fourthHomotopy = diag(0,1,2) ≠ 0`。

    这是「塔高 ≥ 5」的机检见证——不再是判据同形的外推，而是一条具体的、
    逐层串起来的层 2 → 3 → 4 → 5 实例链。 -/
def five0 : SpFiveMorphism four0 four1 where
  fourthHomotopy := shiftDiag3
  condition := by
    show (shiftDiag3 + jordan3) - shiftDiag3 =
      jordan3 * shiftDiag3 - shiftDiag3 * jordan3
    rw [show (shiftDiag3 + jordan3) - shiftDiag3 = jordan3 from by abel]
    simpa [adLin] using adLin_jordan3_shiftDiag3.symm

/-- `diag(0,1,2)` 非零 ⇒ 层 5 见证确实非平凡。 -/
lemma shiftDiag3_ne_zero : shiftDiag3 ≠ 0 := by
  intro h
  have h01 : shiftDiag3 1 1 = (0 : Matrix (Fin 3) (Fin 3) ℂ) 1 1 := by rw [h]
  simp [shiftDiag3, Matrix.of_apply] at h01

/-- **B 相塔高 ≥ 5**：存在层 5 态射，其 `fourthHomotopy` 非零。 -/
theorem tower_height_at_least_five_B :
    ∃ Ψ : SpFiveMorphism four0 four1, Ψ.fourthHomotopy ≠ 0 :=
  ⟨five0, by simpa [five0] using shiftDiag3_ne_zero⟩

end MUFPF
