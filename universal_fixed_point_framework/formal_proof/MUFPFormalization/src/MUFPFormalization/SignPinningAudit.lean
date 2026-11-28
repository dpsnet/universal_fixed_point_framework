/-
MUFPF · 第 84 批 R-q：赋号二分的判据 —— 符号由「标号定向」锁定，而非由结构决定

第 83 批（`ChiralityGradingAudit`）判定：朝向比特的**判据机制**在框架内已有（`F`-共轭分级），
缺的是**赋号**——`+δ` 与 `−δ` 谁被实现，框架不偏置。

本批把「缺赋号」再逼一步：给出一条**可判定的赋号判据**，并检查它究竟依赖什么。

判据取最朴素的一条：耦合把「0 号槽」送到「±1 号槽」的哪一边
（即 `(0,0)` 条目为 `0` 时，看 `(1,0)` 条目是 `+1` 还是 `−1`）。
这是矩阵层唯一还剩的自由——两个条目位置。

（核对象实值：`rotGen = !![0,1;−1,0]`，故 `rotGen 1 0 = −1`；`(−rotGen) 1 0 = +1`。
即 `rotGen = −J`，把 0 号槽送向「负」的一侧。）

结论：这条判据**确实**把符号锁死（`−1` ⟹ `rotGen`，`+1` ⟹ `−rotGen`），
即赋号不再是"无判据"，而是"判据是**标号定向**"。标号定向（哪个槽记作 0）是载体标号的约定，
不是结构定理 ⟹ 符号归根到底仍是约定，与 §22「`T` 是登记约定」同型。
-/
import MUFPFormalization.ChiralityGradingAudit

namespace MUFPF.SignPinningAudit

open Matrix MUFPF.IntertwinerRepairAudit MUFPF.ChiralityGradingAudit
  MUFPF.QuarterTurnQuantizationAudit

/-- 判①：`rotGen` 把 0 号槽送到 −1 号槽：`(0,0)` 条目为 `0`、`(1,0)` 条目为 `−1`。 -/
theorem rotGen_image_of_first_slot : rotGen 0 0 = 0 ∧ rotGen 1 0 = -1 := by
  constructor <;> simp [rotGen]

/-- 判②：`−rotGen` 把 0 号槽送到 +1 号槽：`(0,0)` 条目为 `0`、`(1,0)` 条目为 `+1`。 -/
theorem neg_rotGen_image_of_first_slot : (-rotGen) 0 0 = 0 ∧ (-rotGen) 1 0 = 1 := by
  constructor <;> simp [rotGen, Matrix.neg_apply]

/-- ★ 判③：**定向判据锁符号（−）**。若 `B` 满足全部结构条件且 `(1,0)` 条目为 `−1`，
    则 `B = rotGen`。四个候选值逐一排除，只剩 `rotGen`。 -/
theorem sign_pinned_by_orientation (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hgram : B.transpose * B = 1) (hdet : Matrix.det B = 1) (h4 : B ^ 4 = 1)
    (h00 : B 0 0 = 0) (h10 : B 1 0 = -1) : B = rotGen := by
  rcases coupling_four_values B hgram hdet h4 with h | h | h | h
  · rw [h] at h00
    norm_num [Matrix.one_apply] at h00
  · rw [h] at h00
    norm_num [Matrix.one_apply, Matrix.neg_apply] at h00
  · exact h
  · rw [h] at h10
    norm_num [rotGen, Matrix.neg_apply] at h10

/-- ★ 判④：**定向判据锁符号（+）**。若 `(1,0)` 条目为 `+1`，则 `B = −rotGen`。 -/
theorem reverse_orientation_pins_neg (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hgram : B.transpose * B = 1) (hdet : Matrix.det B = 1) (h4 : B ^ 4 = 1)
    (h00 : B 0 0 = 0) (h10 : B 1 0 = 1) : B = -rotGen := by
  rcases coupling_four_values B hgram hdet h4 with h | h | h | h
  · rw [h] at h00
    norm_num [Matrix.one_apply] at h00
  · rw [h] at h00
    norm_num [Matrix.one_apply, Matrix.neg_apply] at h00
  · rw [h] at h10
    norm_num [rotGen] at h10
  · exact h

/-- ★ 判⑤：两种标号定向**分别**锁定相反的符号，且两符号不同 ⟹
    赋号判据存在，但它是一个「二选一」的约定读法，不是结构强制。 -/
theorem orientation_pins_opposite_signs :
    (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 → Matrix.det B = 1 → B ^ 4 = 1 →
          B 0 0 = 0 → B 1 0 = -1 → B = rotGen) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 → Matrix.det B = 1 → B ^ 4 = 1 →
          B 0 0 = 0 → B 1 0 = 1 → B = -rotGen) ∧
      rotGen ≠ -rotGen :=
  ⟨sign_pinned_by_orientation, reverse_orientation_pins_neg, two_orientations_distinct⟩

/-- 判⑥：定向判据的**输入**只有两个条目位，二者由槽标号给出，不由任何结构量给出。 -/
theorem orientation_data_is_entrywise :
    (rotGen 0 0 = 0 ∧ rotGen 1 0 = -1) ∧ ((-rotGen) 0 0 = 0 ∧ (-rotGen) 1 0 = 1) :=
  ⟨rotGen_image_of_first_slot, neg_rotGen_image_of_first_slot⟩

/-- ★★ **R-q 判决**：
    ① 赋号判据存在（0 号槽的像落在 `±1` 号槽哪一边）；
    ② 该判据把「−」锁定到 `rotGen`、「+」锁定到 `−rotGen`；
    ③ 但判据的输入是**槽标号**（哪个槽记为 0），与 §31 的载体槽数同源，都是标号约定；
    ④ 故符号不是被结构决定的数值，而是被约定决定的读法——与 §22 `T` 的登记同型。
    合取之：赋号二分**不再是缺口**，但也不能升级为定理。 -/
theorem sign_pinning_verdict :
    (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 → Matrix.det B = 1 → B ^ 4 = 1 →
          B 0 0 = 0 → B 1 0 = -1 → B = rotGen) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 → Matrix.det B = 1 → B ^ 4 = 1 →
          B 0 0 = 0 → B 1 0 = 1 → B = -rotGen) ∧
      (rotGen 0 0 = 0 ∧ rotGen 1 0 = -1) ∧
      ((-rotGen) 0 0 = 0 ∧ (-rotGen) 1 0 = 1) :=
  ⟨sign_pinned_by_orientation, reverse_orientation_pins_neg,
    rotGen_image_of_first_slot, neg_rotGen_image_of_first_slot⟩

end MUFPF.SignPinningAudit
