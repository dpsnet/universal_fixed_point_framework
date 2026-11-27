/-
  IntertwinerExistenceAudit.lean — R-f：`T 存在`（C1 猜想）的地位审计
  ==========================================================================

## 接在什么后面

§19（R-c）判：`交织 + T 可逆 ⟹ 全谱转移`，但前提「T 可逆」严格强于框架登记的「T 存在」。
§20/§21 判了两处「参数由观测反推 ⟹ 装配恒真」。四处真断裂里只剩这一处没判：

    A_GR · T = T · A_SM                （谱交织条件，C1）
    T 存在                              （CONJECTURE 级登记）

框架自己在 `notes/04_lorentz_gravity/φθ谱交织指认_等变平均旋转不变.md` L183 给出 T 的
**身份**：T = 弥漫层间结构的谱测度强制平均 = `groupAverage`（C₄ 群平均，`ForceAverageIsotropy.lean`
已机检其幂等、自伴随、保迹、保交织）。故「T 存在」不是空的猜想，它有具体候选。

## 判什么（三条，均机检）

| 编号 | 命题 | 判什么 |
|:--|:--|:--|
| ① | `sylvester_diag_forced_zero` | 两个**不交谱**对角算符之间，唯一交织子是 0 |
| ② | `trivial_case_T_exists` / `diag_intertwine_witness` | 谱相同（或部分相交）时非零 T 确实存在 |
| ③ | `framework_T_kernel_nontrivial` + `framework_T_no_left_inverse` | 框架的 T（强制平均）核非平凡 ⟹ 不可逆 |

## 判决

**「T 存在」与「桥有信息」互斥（2×2 对角情形机检）：**

- ①：谱完全不交 ⟹ `X = 0` 是唯一解。这恰是框架**要用**交织子的场合——两侧谱不同才需要转移。
  于是「存在非零 T」在这一场合不成立。
- ②：谱相同（或一个本征值重合）时非零 T 存在；但此时 `A_GR = T·A_SM·T⁻¹` 只是把同一谱换个写法，
  转移无信息（§19 已判）；部分重合时（`diag_intertwine_witness` + `partial_overlap_no_trace_transfer`）
  T 存在但迹不等 ⟹ 迹桥（`MassEquivalenceBridge.trace_eq_of_intertwine`）不成立。
- ③：框架自己给出的 T = 强制平均是**投影**（幂等 + 自伴随，`ForceAverageIsotropy` 已机检），
  其核含全部无迹部分（`F = diag(1,−1)` 满足 `groupAverage F = 0`）。核非平凡 ⟹ 不存在左逆
  ⟹ §19 的转移引理在框架自己的 T 上**恒不适用**。

⇒ C1 的真问题不是「T 是否存在」（可构造），而是：

    T 存在时转移退化（同谱 / 部分谱），T 需要转移时不存在（不交谱）；
    框架给出的那一个 T 又恰是奇异的投影。

这与 §19 的形式结论完全对齐：§19 说「转移需要 T 可逆」；本批说「框架的 T 不可逆、且可逆的场合无信息」。

## 诚实边界

1. ① 只在 2×2 对角算符上机检（Sylvester 方程的一般结论「谱不交 ⟹ 唯一解 0」是标准线性代数定理，
   本模块不形式化一般 n；选 2×2 是因为框架的轻子/谱隙层恰是二维块）。
2. ② 的「非零 T 存在」用显式见证（`E₁₁`、`F`），不是存在性公理。
3. ③ 的「不可逆」机检形式是「不存在左逆函数」——在有限维、线性的语境下与「不可逆」等价；
   本模块不引入线性映射类型，只在矩阵函数层判（避免为一行结论新建函子层）。
4. 本模块不判 `groupAverage` 是否为「物理上正确的 T」——那是 L183 的物理指认层，非机检范围。
5. 本模块不新增常数、不新增公设；`dlmin` 只引用 `GNBridgeAudit.dlmin`（`(√3−1)/6`）。
-/

import MUFPFormalization.ForceAverageIsotropy
import MUFPFormalization.GNBridgeAudit
import Mathlib.Tactic

namespace MUFPF.IntertwinerExistenceAudit

open MUFPF.Isotropy

/-- 对角算符 `diag(a, b) = !![a, 0; 0, b]`（2×2 谱块的标准形态）。 -/
def diag2 (a b : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a, 0; 0, b]

/-- 谱隙常数在 (0, 1) 内：`0 < Δλ_min < 1`（`Δλ_min = (√3−1)/6 ≈ 0.122`）。 -/
theorem dlmin_in_unit_interval :
    0 < MUFPF.GNBridgeAudit.dlmin ∧ MUFPF.GNBridgeAudit.dlmin < 1 := by
  constructor
  · exact MUFPF.GNBridgeAudit.dlmin_pos
  · have h2 : Real.sqrt 3 < (2 : ℝ) := by
      rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 2)]
      norm_num
    unfold MUFPF.GNBridgeAudit.dlmin
    linarith

/-- **判①**：两个**不交谱**对角算符之间，交织子只能是 0。
    （`diag2 a₁ a₂ · X = X · diag2 b₁ b₂` 的第 (i,j) 条目给出 `(a_i − b_j) x_ij = 0`。） -/
theorem sylvester_diag_forced_zero {a1 a2 b1 b2 : ℝ}
    (h11 : a1 ≠ b1) (h12 : a1 ≠ b2) (h21 : a2 ≠ b1) (h22 : a2 ≠ b2)
    {X : Matrix (Fin 2) (Fin 2) ℝ} (h : diag2 a1 a2 * X = X * diag2 b1 b2) :
    X = 0 := by
  have e00 : a1 * X 0 0 = X 0 0 * b1 := by
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
    simpa [diag2, Matrix.mul_apply, Fin.sum_univ_two] using this
  have e01 : a1 * X 0 1 = X 0 1 * b2 := by
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    simpa [diag2, Matrix.mul_apply, Fin.sum_univ_two] using this
  have e10 : a2 * X 1 0 = X 1 0 * b1 := by
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 0) h
    simpa [diag2, Matrix.mul_apply, Fin.sum_univ_two] using this
  have e11 : a2 * X 1 1 = X 1 1 * b2 := by
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 1) h
    simpa [diag2, Matrix.mul_apply, Fin.sum_univ_two] using this
  have z00 : X 0 0 = 0 := by
    have hz : (a1 - b1) * X 0 0 = 0 := by rw [sub_mul, e00]; ring
    exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr h11)
  have z01 : X 0 1 = 0 := by
    have hz : (a1 - b2) * X 0 1 = 0 := by rw [sub_mul, e01]; ring
    exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr h12)
  have z10 : X 1 0 = 0 := by
    have hz : (a2 - b1) * X 1 0 = 0 := by rw [sub_mul, e10]; ring
    exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr h21)
  have z11 : X 1 1 = 0 := by
    have hz : (a2 - b2) * X 1 1 = 0 := by rw [sub_mul, e11]; ring
    exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr h22)
  ext i j
  fin_cases i <;> fin_cases j <;> simp [z00, z01, z10, z11]

/-- **判①的框架实例**：取 `A_GR = diag(0, 2)`、`A_SM = diag(1, 1 + Δλ_min)`
    （谱距 = 框架谱隙），则唯一交织子是 0——「存在非零 T」在此场合不成立。 -/
theorem no_T_between_gapped_spectra
    {X : Matrix (Fin 2) (Fin 2) ℝ}
    (h : diag2 0 2 * X = X * diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) :
    X = 0 := by
  have hgap := dlmin_in_unit_interval
  refine sylvester_diag_forced_zero (a1 := 0) (a2 := 2) (b1 := 1)
    (b2 := 1 + MUFPF.GNBridgeAudit.dlmin) ?_ ?_ ?_ ?_ h
  · norm_num
  · intro hc
    linarith [hgap.1]
  · norm_num
  · intro hc
    linarith [hgap.2]

/-- **判②（同谱）**：谱相同或有一个本征值重合时，`E₁₁` 是非零交织子。
    （`a₁ = b₁` ⟹ `diag(a₁,a₂) · E₁₁ = E₁₁ · diag(b₁,b₂)`。） -/
theorem diag_intertwine_witness {a1 a2 b1 b2 : ℝ} (hab : a1 = b1) :
    diag2 a1 a2 * !![(1 : ℝ), 0; 0, 0] = !![(1 : ℝ), 0; 0, 0] * diag2 b1 b2 := by
  subst hab
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Fin.sum_univ_two]

/-- `E₁₁` 非零（判② 的见证非退化）。 -/
theorem E11_ne_zero : (!![(1 : ℝ), 0; 0, 0] : Matrix (Fin 2) (Fin 2) ℝ) ≠ 0 := by
  intro h
  have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
  simp at hh

/-- `E₁₁` 奇异：`det E₁₁ = 0`——判② 的见证**不可逆**（§19 转移引理同样不适用）。 -/
theorem E11_singular : (!![(1 : ℝ), 0; 0, 0] : Matrix (Fin 2) (Fin 2) ℝ).det = 0 := by
  simp [Matrix.det_fin_two]

/-- **判②（部分重合时迹桥失效）**：一个本征值重合（T 存在）而另一对不重合 ⟹
    `trace A_GR ≠ trace A_SM` ⟹ `MassEquivalenceBridge.trace_eq_of_intertwine` 的前提不可满足。 -/
theorem partial_overlap_no_trace_transfer {a1 a2 b2 : ℝ} (h : a2 ≠ b2) :
    Matrix.trace (diag2 a1 a2) ≠ Matrix.trace (diag2 a1 b2) := by
  intro heq
  have he : a1 + a2 = a1 + b2 := by
    simpa [diag2, Matrix.trace, Fin.sum_univ_two] using heq
  exact h (by linarith)

/-- `F = diag(1, −1)` 非零（判③ 的核见证）。 -/
theorem F_ne_zero : F ≠ (0 : Matrix (Fin 2) (Fin 2) ℝ) := by
  intro h
  have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
  simp [F] at hh

/-- 强制平均湮灭反射元：`groupAverage F = 0`（`F` 无迹 ⟹ 平均后为 `trace/2 • 1 = 0`）。 -/
theorem groupAverage_F_zero : groupAverage F = 0 := by
  have hsym : Matrix.transpose F = F := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [F]
  have hg := groupAverage_isotropy hsym
  simpa [F] using hg

/-- **判③（核非平凡）**：`groupAverage F = 0` 而 `F ≠ 0`——
    框架的 T（强制平均）有非平凡核（全部无迹/各向异性部分被投影湮灭）。 -/
theorem framework_T_kernel_nontrivial :
    ∃ Z : Matrix (Fin 2) (Fin 2) ℝ, Z ≠ 0 ∧ groupAverage Z = 0 :=
  ⟨F, F_ne_zero, groupAverage_F_zero⟩

/-- **判③（不可逆）**：不存在左逆函数 `inv`（`∀ T, inv (groupAverage T) = T`）。
    证明：`groupAverage F = 0` 与 `groupAverage 0 = 0` 同时成立，会把 `F` 与 `0` 压成同值。 -/
theorem framework_T_no_left_inverse :
    ¬ ∃ inv : (Matrix (Fin 2) (Fin 2) ℝ → Matrix (Fin 2) (Fin 2) ℝ),
        ∀ T : Matrix (Fin 2) (Fin 2) ℝ, inv (groupAverage T) = T := by
  rintro ⟨inv, hinv⟩
  have hF : inv (groupAverage F) = F := hinv F
  have h0 : inv (groupAverage (0 : Matrix (Fin 2) (Fin 2) ℝ)) = 0 := hinv 0
  have hg0 : groupAverage (0 : Matrix (Fin 2) (Fin 2) ℝ) = 0 := by
    simp [groupAverage]
  rw [groupAverage_F_zero] at hF
  rw [hg0] at h0
  exact F_ne_zero (hF.symm.trans h0)

/-- **判②（非零交织子确实存在——不是猜想）**：取 `A_GR = A_SM = 1`，则 `T = F ≠ 0` 满足交织。
    （退化情形：两侧算符相同，交织子承不承载信息是另一回事。） -/
theorem trivial_case_T_exists :
    ∃ T : Matrix (Fin 2) (Fin 2) ℝ,
      T ≠ 0 ∧ (1 : Matrix (Fin 2) (Fin 2) ℝ) * T = T * (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  refine ⟨F, F_ne_zero, ?_⟩
  simp

/-- **R-f 判决汇总**：

    ① 不交谱 ⟹ 唯一交织子 = 0（框架「需要转移」的场合不存在非零 T）；
    ①′ 框架实例（谱距 = Δλ_min > 0）同上；
    ② 同谱/部分重合 ⟹ 非零 T 存在（`E₁₁`），但部分重合时迹不等 ⟹ 迹桥失效；
    ③ 框架的 T（强制平均）核非平凡 ⟹ 无左逆 ⟹ §19 转移引理恒不适用；
    ②″ 非零交织子确实存在（退化情形），故「T 存在」本身不是猜想。 -/
theorem intertwiner_existence_verdict :
    (∀ X : Matrix (Fin 2) (Fin 2) ℝ,
        diag2 0 2 * X = X * diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin) → X = 0) ∧
    (∀ (a1 a2 b2 : ℝ), a2 ≠ b2 →
        Matrix.trace (diag2 a1 a2) ≠ Matrix.trace (diag2 a1 b2)) ∧
    (∃ T : Matrix (Fin 2) (Fin 2) ℝ,
        T ≠ 0 ∧ (1 : Matrix (Fin 2) (Fin 2) ℝ) * T = T * (1 : Matrix (Fin 2) (Fin 2) ℝ)) ∧
    (∃ Z : Matrix (Fin 2) (Fin 2) ℝ, Z ≠ 0 ∧ groupAverage Z = 0) ∧
    (¬ ∃ inv : (Matrix (Fin 2) (Fin 2) ℝ → Matrix (Fin 2) (Fin 2) ℝ),
        ∀ T : Matrix (Fin 2) (Fin 2) ℝ, inv (groupAverage T) = T) ∧
    (!![(1 : ℝ), 0; 0, 0] : Matrix (Fin 2) (Fin 2) ℝ).det = 0 :=
  ⟨fun X h => no_T_between_gapped_spectra (X := X) h,
   fun a1 a2 b2 hh => partial_overlap_no_trace_transfer (a1 := a1) (a2 := a2) (b2 := b2) hh,
   trivial_case_T_exists, framework_T_kernel_nontrivial, framework_T_no_left_inverse,
   E11_singular⟩

end MUFPF.IntertwinerExistenceAudit
