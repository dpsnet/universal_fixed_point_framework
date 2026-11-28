/-
  TwoWaySpectrumAudit.lean — R-z：反向耦合非零时载体谱是否还持有层值（§45 的载体代价）
  ==================================================================================

## 问题

§45 判「载体谱给全部、只缺归属」：`C = 0` 的上块三角载体，特征行列式 = 两层之积，
四根 `0, 2, 1, 1+Δλ_min` 齐全，且对耦合块 `B` 完全盲。但那一支只做了单向载体；
`C ≠ 0` 时特征行列式须经 Schur 补，§45.6 把这条登记为 `CARRIER_SPECTRUM_TWO_WAY`。
本批落地它，并判「谱的分离性是否以单向载体为代价」。

## 结果

1. 一般的谱平移分块式：`t • 1₄ − blk A B C D = blk (t • 1 − A) (−B) (−C) (t • 1 − D)`（`shift_blk_gen`）。
2. Schur 谱分解：`det (t • 1₄ − blk A B C D) = det (t • 1 − D) · det ((t • 1 − A) − (−B)·⅟(t • 1 − D)·(−C))`
   （`det_shift_blk_schur`，`[Invertible (t • 1 − D)]`）。
3. 对角 2×2 的一般可逆实例（`instDiagInv`），使 `⅟(diag2 a b) = diag2 a⁻¹ b⁻¹` 按定义归约。
4. **框架实例、恒等反向耦合**：`det (2 • 1₄ − blk A_GR 1 1 A_SM) = −1`（`two_way_reading_at_two`），
   而同一时刻单向载体（`C = 0`）的读数是 `0`（§45 `carrier_root_two`）。

## 判决

- 谱的「给全部」**以 `C = 0` 为载体代价**：恒等反向耦合一开，`t = 2` 的读数从 `0` 变成 `−1`
   ⟹ `2` 不再是双向载体的特征根，层值被耦合**推离**谱。
- 这与 §41 的 `det` 结论同向但更强：§41 说 `det` 读数混叠（量读不出），本批说**根本身**被移动
  （连「有哪些数」都变了）。故「谱是最强的标量读数」这一判断的适用范围是**单向载体**；
  双向载体上连谱也不再是层数据的忠实读数。
- 净结果：载体谱的可读性随耦合方向数单调退化——`C = 0`：根齐全、对 `B` 盲；
  `C ≠ 0`：根被推离，读数依赖耦合。这与 §38–§41（`det` 从「恒零」到「混叠」）构成同一条退化链。

## 诚实边界

1. 只算 `t = 2`（物理层的根）这一个时刻的框架实例；`t = 1 + Δλ_min` 时 `t • 1 − D` 恰奇异，
   Schur 律不适用（须换对角化顺序或另寻主轴），本批不做，登记 `SPECTRUM_TWO_WAY_AT_SM_ROOT`。
2. 只取恒等耦合 `B = C = 1` 作见证，不主张「任何 `C ≠ 0` 都移动全部根」——那是连续依赖问题，
   本批只给一个反例（反例足以否定「谱与耦合无关」的全称命题）。
3. 不判「双向载体是否仍是框架应有的载体」——§25 出口①的延伸，物理指认层。
4. 不新增常数、不新增公设；`Δλ_min` 只引用 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.CarrierSpectrumAudit
import MUFPFormalization.SchurCarrierAudit
import MUFPFormalization.TwoWayCarrierAudit
import MUFPFormalization.QuantizedDetAudit
import Mathlib.Tactic

-- 本批的 `⅟` 需按定义归约（`letI` 实例），且 `haveI`/simp 集会产生风格类提示；
-- 与 §41 同一处理：四类 linter 统一关闭，警告计数保持基线。
set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.TwoWaySpectrumAudit

open MUFPF.IntertwinerExistenceAudit (diag2 dlmin_in_unit_interval)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.CarrierDetAudit (det_diag2)
open MUFPF.CarrierSpectrumAudit (carrier_root_two)
open MUFPF.SchurCarrierAudit (det_blk_schur)
open MUFPF.TwoWayCarrierAudit (diag2_mul_diag2 diag2_sub_diag2 diag2_one_one)
open MUFPF.ScalarReadoutAudit (shift_diag2)
open MUFPF.QuantizedDetAudit (det_scalar_aligned)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)

abbrev M2 : Type := Matrix (Fin 2) (Fin 2) ℝ

/-! ## 一般的谱平移与 Schur 谱分解 -/

/-- 一般分块矩阵的谱平移：`t • 1₄ − blk A B C D = blk (t•1−A) (−B) (−C) (t•1−D)`。 -/
theorem shift_blk_gen (t : ℝ) (A B C D : M2) :
    t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) - blk A B C D =
      blk (t • (1 : M2) - A) (-B) (-C) (t • (1 : M2) - D) := by
  rw [CarrierSpectrumAudit.blk_smul_one, CarrierSpectrumAudit.blk_sub]
  simp

/-- ★★ **Schur 谱分解**：`det (t • 1₄ − blk A B C D)`
    `= det (t•1−D) · det ((t•1−A) − (−B)·⅟(t•1−D)·(−C))`。 -/
theorem det_shift_blk_schur (t : ℝ) (A B C D : M2) [Invertible (t • (1 : M2) - D)] :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) - blk A B C D) =
      Matrix.det (t • (1 : M2) - D) *
        Matrix.det (t • (1 : M2) - A - (-B) * ⅟(t • (1 : M2) - D) * (-C)) := by
  rw [shift_blk_gen, det_blk_schur]

/-! ## 对角 2×2 的一般可逆实例 -/

/-- `diag2 a b` 的可逆实例（`a ≠ 0`、`b ≠ 0`）：`⅟(diag2 a b)` 按定义即 `diag2 a⁻¹ b⁻¹`。 -/
noncomputable def instDiagInv (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) : Invertible (diag2 a b) where
  invOf := diag2 a⁻¹ b⁻¹
  invOf_mul_self := by
    rw [diag2_mul_diag2, inv_mul_cancel₀ ha, inv_mul_cancel₀ hb]
    exact diag2_one_one
  mul_invOf_self := by
    rw [diag2_mul_diag2, mul_inv_cancel₀ ha, mul_inv_cancel₀ hb]
    exact diag2_one_one

/-- 双负夹心：`(−1)·X·(−1) = X`（2×2 实矩阵）。 -/
theorem neg_one_sandwich (X : M2) : (-1 : M2) * X * (-1 : M2) = X := by
  rw [neg_one_mul, neg_mul, mul_neg, mul_one, neg_neg]

/-! ## 框架实例：t = 2 时的双向读数 -/

/-- 谱平移的两个框架实例：`2 • 1 − A_GR = diag2 2 0`。 -/
theorem shift_gr_two :
    (2 : ℝ) • (1 : M2) - diag2 (0 : ℝ) 2 = diag2 (2 : ℝ) 0 := by
  rw [shift_diag2 2 0 2]
  norm_num

/-- 谱平移的两个框架实例：`2 • 1 − A_SM = diag2 1 (1 − Δλ_min)`。 -/
theorem shift_sm_two :
    (2 : ℝ) • (1 : M2) - diag2 (1 : ℝ) (1 + dlmin) = diag2 (1 : ℝ) (1 - dlmin) := by
  rw [shift_diag2 2 1 (1 + dlmin)]
  rw [show (2 : ℝ) - 1 = 1 by norm_num, show (2 : ℝ) - (1 + dlmin) = 1 - dlmin by ring]

/-- ★★ **恒等反向耦合下 `t = 2` 的读数**：`det (2 • 1₄ − blk A_GR 1 1 A_SM) = −1`。
    对照单向载体（`C = 0`）同一时刻的读数 `0`（§45）。 -/
theorem two_way_reading_at_two :
    Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (1 : M2) (1 : M2) (diag2 (1 : ℝ) (1 + dlmin))) = -1 := by
  have hlt : dlmin < 1 := dlmin_in_unit_interval.2
  have hne : (1 : ℝ) - dlmin ≠ 0 := by intro hc; linarith
  rw [CarrierSpectrumAudit.blk_smul_one, CarrierSpectrumAudit.blk_sub]
  rw [show (2 : ℝ) • (1 : M2) - diag2 (0 : ℝ) 2 = diag2 (2 : ℝ) 0 from shift_gr_two,
    show (2 : ℝ) • (1 : M2) - diag2 (1 : ℝ) (1 + dlmin) =
      diag2 (1 : ℝ) (1 - dlmin) from shift_sm_two]
  letI := instDiagInv (1 : ℝ) (1 - dlmin) one_ne_zero hne
  rw [det_blk_schur]
  rw [show (0 : M2) - (1 : M2) = -(1 : M2) from by rw [zero_sub]]
  rw [show ⅟(diag2 (1 : ℝ) (1 - dlmin)) = diag2 ((1 : ℝ)⁻¹) ((1 - dlmin)⁻¹) from rfl]
  rw [neg_one_sandwich]
  rw [diag2_sub_diag2]
  simp only [det_diag2, inv_one]
  field_simp
  ring

/-- ★★ **`2` 不再是双向载体的特征根**：`det (2 • 1₄ − blk A_GR 1 1 A_SM) ≠ 0`。 -/
theorem two_not_in_two_way_spectrum :
    Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (1 : M2) (1 : M2) (diag2 (1 : ℝ) (1 + dlmin))) ≠ 0 := by
  rw [two_way_reading_at_two]
  norm_num

/-! ## 标量耦合下的谱因子化：Δλ_min 被隔离进单个因子 -/

/-- 双负夹心（一般块）：`(−A)·X·(−B) = A·X·B`。 -/
theorem neg_sandwich (A X B : M2) : (-A) * X * (-B) = A * X * B := by
  rw [neg_mul, neg_mul, mul_neg, neg_neg]

/-- ★★ **标量耦合 `B = C = s · 1` 下的谱因子化**（`t ≠ 1`、`t ≠ 1 + Δλ_min`）：
    `det (t • 1₄ − blk A_GR (s·1) (s·1) A_SM)`
    `= (t² − t − s²) · (t² − (3 + Δλ_min)·t + 2(1 + Δλ_min) − s²)`。

    第一个因子**完全不含 `Δλ_min`**——耦合只搬动第二个因子；第二个因子把 `Δλ_min` 全部吸收。 -/
theorem scalar_coupling_spectrum_factorization (t s : ℝ)
    (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 s s) (diag2 s s) (diag2 (1 : ℝ) (1 + dlmin))) =
      (t ^ 2 - t - s ^ 2) * (t ^ 2 - (3 + dlmin) * t + (2 * (1 + dlmin) - s ^ 2)) := by
  have hd1 : t - 1 ≠ 0 := sub_ne_zero.mpr h1
  have hd2 : t - (1 + dlmin) ≠ 0 := sub_ne_zero.mpr h2
  rw [shift_blk_gen]
  rw [show t • (1 : M2) - diag2 (0 : ℝ) 2 = diag2 t (t - 2) from by
        rw [shift_diag2 t 0 2, sub_zero]
      , show t • (1 : M2) - diag2 (1 : ℝ) (1 + dlmin) =
          diag2 (t - 1) (t - (1 + dlmin)) from by
        rw [shift_diag2 t 1 (1 + dlmin)]]
  letI := instDiagInv (t - 1) (t - (1 + dlmin)) hd1 hd2
  rw [det_blk_schur]
  rw [show ⅟(diag2 (t - 1) (t - (1 + dlmin))) =
      diag2 ((t - 1)⁻¹) ((t - (1 + dlmin))⁻¹) from rfl]
  rw [neg_sandwich, diag2_mul_diag2, diag2_mul_diag2, diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring

/-- **单位耦合（`s = 1`）的谱因子化**：`(t² − t − 1) · (t² − (3 + Δλ_min)·t + (1 + 2Δλ_min))`。
    第一因子是**金色因子**（根为 `φ = (1+√5)/2` 与 `−1/φ`），完全与 `Δλ_min` 无关。 -/
theorem unit_coupling_spectrum_factorization (t : ℝ)
    (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 1) (diag2 (1 : ℝ) 1)
          (diag2 (1 : ℝ) (1 + dlmin))) =
      (t ^ 2 - t - 1) * (t ^ 2 - (3 + dlmin) * t + (1 + 2 * dlmin)) := by
  have := scalar_coupling_spectrum_factorization t 1 h1 h2
  simpa [show (2 : ℝ) * (1 + dlmin) - 1 = 1 + 2 * dlmin from by ring] using this

/-- **一致性**：因子化在 `t = 2` 给出 `det = −1`（`(4−2−1)·(4−2(3+Δλ_min)+1+2Δλ_min) = −1`），
    与 `two_way_reading_at_two` 同值。 -/
theorem factorization_at_two :
    ((2 : ℝ) ^ 2 - 2 - 1) * ((2 : ℝ) ^ 2 - (3 + dlmin) * 2 + (1 + 2 * dlmin)) = -1 := by
  ring

/-- **一致性**：`t = 0` 的载体读数与 §41 纯标量同号组合同值（`1 − 2(1 + Δλ_min)`）。 -/
theorem carrier_det_at_zero :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (1 : M2) (1 : M2) (diag2 (1 : ℝ) (1 + dlmin))) =
      1 - 2 * (1 + dlmin) := by
  have hh : (1 + dlmin) ≠ 0 := by linarith [dlmin_pos]
  exact det_scalar_aligned (1 + dlmin) hh

/-! ## 汇总判决 -/

/-- **R-z 判决汇总**：
    ① `C = 0` 时 `t = 2` 读 `0`（根在场，§45）；
    ② `C = 1`、`B = 1` 时同一时刻读 `−1`（根被推离），且 `−1 ≠ 0`；
    ③ 故「谱给全部」只在单向载体上成立：反向耦合非零时层值被推离谱，谱不再是层数据的忠实读数。 -/
theorem two_way_spectrum_verdict :
    (Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (1 : M2) 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0) ∧
      (Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (1 : M2) (1 : M2) (diag2 (1 : ℝ) (1 + dlmin))) = -1) ∧
      ((-1 : ℝ) ≠ 0) :=
  ⟨carrier_root_two 1, two_way_reading_at_two, by norm_num⟩

end MUFPF.TwoWaySpectrumAudit
