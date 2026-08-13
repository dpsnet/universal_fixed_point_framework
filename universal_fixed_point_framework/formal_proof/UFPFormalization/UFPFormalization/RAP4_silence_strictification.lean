/-
RAP-4: 态射静默的正交投影严格化（定义 R4、命题 R5、定理 R6/R8/R9）
========================================================================

RAP 修复方案 §10–11 的形式化实现。

### 定义 R4（Λ-态射静默）
  设 f: R₁ → R₂，D(f): H_{R₁} → H_{R₂}。
  V_Λ = E_{A₂}([0,Λ]) H_{R₂} 为谱子空间。
  f 是 Λ-严格静默 ⇔ P_{V_Λ} D(f) = 0 ⇔ ran D(f) ⊆ V_Λ^⊥。

### 命题 R5（严格 ⇒ 渐近，反向不成立）
  若 V_Λ ≠ 0，则 P_V D(f) = 0 蕴含 D(f) 有零奇异值（inf σ = 0）。
  反之，存在 inf σ = 0 但 P_V D(f) ≠ 0 的算子。

### 定理 R6（静默筛 / 左理想）
  Λ-严格静默态射对预复合封闭：P_V D(f) = 0 ⇒ P_V D(f ∘ g) = 0。
  对后复合一般不封闭。

### 定义 R7（可见性函数）
  v(f) := ||P_V D(f)|| / ||D(f)|| ∈ [0,1]

### 定理 R8（渐近静默的半群封闭）
  若 D(f_{t+s}) = D(f_t) D(f_s) 且 v(f_t) ≤ Ce^{-γt}，
  则 v(f_{t+s}) ≤ C e^{-γt}（半群压缩 ∥D(f)∥ ≤ 1 下）。

### 定理 R9 机制Ⅰ（超收缩 / IFS 型）
  对角收缩矩阵 W_n 驱动 v(f_n) ≤ C·c_max^n。

本文件在有限维实矩阵上形式化以上结果。
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Determinant
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open scoped Matrix.Norms.Frobenius

noncomputable section

namespace Matrix

/-- Frobenius 范数（当前 mathlib 以 ‖·‖ 类型类提供，此处桥接旧 API `Matrix.frobeniusNorm`）。 -/
abbrev frobeniusNorm {m n : ℕ} (A : Matrix (Fin m) (Fin n) ℝ) : ℝ := ‖A‖

/-- Frobenius 范数次乘性（对应旧 API `Matrix.frobeniusNorm_mul_le`）。 -/
theorem frobeniusNorm_mul_le {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℝ) :
    frobeniusNorm (A * B) ≤ frobeniusNorm A * frobeniusNorm B :=
  norm_mul_le A B

/-- Frobenius 范数非负（对应旧 API `Matrix.frobeniusNorm_nonneg`）。 -/
theorem frobeniusNorm_nonneg {m n : ℕ} (A : Matrix (Fin m) (Fin n) ℝ) :
    0 ≤ frobeniusNorm A :=
  norm_nonneg A

end Matrix

open Matrix
open Real

namespace UFPFormalization.RAP4

/-!#############################################################################
  定义 R4：Λ-严格静默
  #############################################################################-/

/-- 正交投影的结构条件：幂等且对称（自伴）。 -/
structure IsOrthogonalProjection {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ) : Prop where
  idempotent : P * P = P
  symmetric : Pᵀ = P

/-- 非零正交投影：P ≠ 0 且满足 IsOrthogonalProjection。 -/
structure NonzeroProjection {n : ℕ} (P : Matrix (Fin n) (Fin n) ℝ) : Prop where
  is_proj : IsOrthogonalProjection P
  nonzero : P ≠ 0

/-- Definition R4: Λ-严格静默条件。
    f 是 Λ-严格静默 ⇔ P_{V_Λ} · D(f) = 0，
    即 D(f) 的值域完全落在 V_Λ 的正交补中。 -/
def strictSilence {m n : ℕ} (Df : Matrix (Fin m) (Fin n) ℝ) (P : Matrix (Fin m) (Fin m) ℝ) : Prop :=
  P * Df = 0

/-!#############################################################################
  命题 R5：严格 ⇒ 渐近（奇异），反向不成立
  #############################################################################-/

/-- 方阵的奇异（非可逆）性：行列式为零。 -/
def isSingular {n : ℕ} (A : Matrix (Fin n) (Fin n) ℝ) : Prop :=
  det A = 0

/-- 渐近静默（原 M3 在有限维下的等价条件）：D(f) 奇异（有零奇异值）。
    在有限维中 inf σ(D(f)^* D(f)) = 0 ⇔ det(D(f)) = 0（方阵情形）。 -/
def asymptoticSilence {n : ℕ} (Df : Matrix (Fin n) (Fin n) ℝ) : Prop :=
  isSingular Df

/-- 命题 R5（正向）：严格静默且投影非零 ⇒ D(f) 奇异（渐近静默）。
    证明：若 Df 可逆（det ≠ 0），则右乘 Df⁻¹ 得 P = P·Df·Df⁻¹ = 0·Df⁻¹ = 0，
    与 P ≠ 0 矛盾。故 Df 不可逆，即 det(Df) = 0。 -/
theorem strict_implies_asymptotic {n : ℕ} (Df : Matrix (Fin n) (Fin n) ℝ)
    (P : Matrix (Fin n) (Fin n) ℝ) (hP : NonzeroProjection P)
    (hstrict : strictSilence Df P) : asymptoticSilence Df := by
  -- 用反证法：若 Df 可逆（det ≠ 0），则 P = 0 矛盾
  unfold asymptoticSilence isSingular
  by_contra! h_det_ne_zero
  have h_det_ne_zero' : det Df ≠ 0 := h_det_ne_zero
  haveI : Invertible (det Df) := invertibleOfNonzero h_det_ne_zero'
  haveI : Invertible Df := Matrix.invertibleOfDetInvertible (A := Df)
  have h_inv : Df * (Df⁻¹) = 1 := by
    simpa using (Matrix.mul_inv_cancel_right_of_invertible
      (B := (1 : Matrix (Fin n) (Fin n) ℝ)))
  -- P * Df = 0 右乘 Df⁻¹
  have hP_mul : (P * Df) * Df⁻¹ = 0 * Df⁻¹ := by rw [hstrict]
  -- 左侧：P * (Df * Df⁻¹) = P * 1 = P
  have hP_eq_zero : P = 0 := by
    calc
      P = P * (Df * Df⁻¹) := by
        rw [h_inv, Matrix.mul_one]
      _ = (P * Df) * Df⁻¹ := by rw [Matrix.mul_assoc]
      _ = 0 * Df⁻¹ := by rw [hstrict]
      _ = 0 := by simp
  -- P ≠ 0 矛盾
  exact hP.nonzero hP_eq_zero

/-- 命题 R5（反向：渐近 ⇏ 严格）：存在 Df 奇异但 P·Df ≠ 0 的反例。
    反例构造：取 P = [[1,0],[0,0]]（到 x 轴的投影），
    Df = [[0,0],[0,0]]（零矩阵，奇异）。
    则 P·Df = 0，不构成反例。

    更精细的构造：取 P = diag(1,0)（到第一坐标的投影），
    Df = [[0,0],[1,0]]（秩 1，有零奇异值）。
    则 P·Df = [[0,0],[0,0]] = 0，仍然不成立。

    有意义的反例需要 ran(Df) 与 V 非正交但 Df 奇异。
    即：Df 奇异（det=0）但 ran(Df) 不全在 V^⊥ 中。

    取 P = [[1,0],[0,0]]（到 e₁ 的投影），
    Df = [[0,1],[0,0]]（幂零，det=0 即奇异）。
    则 P·Df = [[0,1],[0,0]] ≠ 0，且 Df 奇异。
    这满足：Df 奇异但 P·Df ≠ 0。 -/
theorem asymptotic_not_implies_strict :
    ∃ (Df P : Matrix (Fin 2) (Fin 2) ℝ),
      NonzeroProjection P ∧ asymptoticSilence Df ∧ ¬strictSilence Df P := by
  let Df : Matrix (Fin 2) (Fin 2) ℝ :=
    fun i j => match i, j with | 0, 0 => 0 | 0, 1 => 1 | 1, 0 => 0 | 1, 1 => 0
  let P : Matrix (Fin 2) (Fin 2) ℝ :=
    fun i j => match i, j with | 0, 0 => 1 | 0, 1 => 0 | 1, 0 => 0 | 1, 1 => 0
  refine ⟨Df, P, ?_, ?_, ?_⟩
  · -- 证明 P 是非零投影
    refine {
      is_proj := {
        idempotent := by
          funext i j; fin_cases i <;> fin_cases j <;> simp [P, Matrix.mul_apply]
        symmetric := by
          funext i j; fin_cases i <;> fin_cases j <;> simp [P]
      }
      nonzero := by
        intro hzero
        have h00 : P 0 0 = 0 := congrFun (congrFun hzero 0) 0
        simp [P] at h00
    }
  · -- Df 奇异：det = 0
    unfold asymptoticSilence isSingular
    simp [Df, Matrix.det_fin_two]
  · -- P·Df ≠ 0（非严格静默）
    unfold strictSilence
    intro hzero
    have h01 : (P * Df) 0 1 = 0 := by rw [hzero]; rfl
    have hcalc : (P * Df) 0 1 = 1 := by norm_num [P, Df, Matrix.mul_apply]
    rw [hcalc] at h01
    norm_num at h01

/-!#############################################################################
  定理 R6：静默筛 / 左理想
  Λ-严格静默态射对预复合封闭。
  #############################################################################-/

/-- 定理 R6（左理想）：若 f 是严格静默（P·Df = 0），
    则对任意可复合的 g，f∘g 也是严格静默（P·(Df·Dg) = 0）。
    证明：P·(Df·Dg) = (P·Df)·Dg = 0·Dg = 0。 -/
theorem silence_is_left_ideal {m n p : ℕ} (Df : Matrix (Fin m) (Fin n) ℝ)
    (Dg : Matrix (Fin n) (Fin p) ℝ) (P : Matrix (Fin m) (Fin m) ℝ)
    (hstrict : strictSilence Df P) : strictSilence (Df * Dg) P := by
  unfold strictSilence at *
  calc
    P * (Df * Dg) = (P * Df) * Dg := by rw [Matrix.mul_assoc]
    _ = (0 : Matrix (Fin m) (Fin n) ℝ) * Dg := by rw [hstrict]
    _ = 0 := by simp

/-- 后复合一般保持：若 f 严格静默，则 g∘f 不一定严格静默。
    因为 P_V·(Dg·Df) = (P_V·Dg)·Df，若 P_V·Dg ≠ 0，即使 P_V·Df = 0，
    乘积也可能非零。后复合在 Dg 值域被 P_V 杀死时才保持。 -/
theorem silence_not_right_ideal :
    ∃ (Df Dg P : Matrix (Fin 2) (Fin 2) ℝ),
      NonzeroProjection P ∧ strictSilence Df P ∧ ¬strictSilence (Dg * Df) P := by
  -- 反例：取 P = [[1,0],[0,0]], Df = 0（严格静默），Dg = I（恒等映射）
  -- 则 Dg·Df = 0，仍是严格静默——不构成反例。
  -- 需要 Df 被 PV 杀死（P·Df=0）但 Dg·Df 不被 PV 杀死。
  -- 这是不可能的，因为矩阵乘法是结合的：
  -- P·(Dg·Df) = (P·Dg)·Df。若 P·Df=0 但 Df 非零，且 P·Dg 非零：
  -- 取 P = [[1,0],[0,0]], Df = [[0],[1]] (2×1), Dg = [[1,0],[0,0]] (2×2).
  -- 则 P·Df = [[1,0],[0,0]]·[[0],[1]] = [[0],[0]] = 0.
  -- P·(Dg·Df) = P·([[1,0],[0,0]]·[[0],[1]]) = P·[[0],[0]] = 0. 仍然被杀。
  --
  -- 实际上，当 Df 被 P 杀死时，对任意 Dg，P·Dg·Df = (P·Dg)·Df 不一定为零
  -- 因为 (P·Dg) 的值域可能不在 ran(Df) 的补空间中... 但 P 在左边，所以
  -- 如果 P·Df = 0，则 P 的值域与 ran(Df) 正交，那么 (P·Dg)·Df 将 ran(Df)
  -- 映射到与 P 正交的空间... 实际上这不成立。
  --
  -- 反例：取 P = [[1,0,0],[0,0,0],[0,0,0]] (到 e₁ 的投影, 3×3)
  -- Df = [[0,0],[1,0],[0,0]] (3×2, ran = span(e₂))
  -- Dg = [[0,1,0],[0,0,0]] (2×3)
  -- P·Df = [[0,0],[0,0],[0,0]] = 0 (严格静默)
  -- P·(Dg·Df) = P·([[0,1,0],[0,0,0]]·[[0,0],[1,0],[0,0]]) = P·[[1,0],[0,0]]
  --   = [[1,0,0],[0,0,0],[0,0,0]]·[[1,0],[0,0],[0,0]] = [[1,0],[0,0],[0,0]] ≠ 0。
  --
  -- 简化：n=2, m=2, p=2
  -- P = [[1,0],[0,0]], Df = [[0,0],[1,0]], Dg = [[0,1],[0,0]]
  -- P·Df = 0 ✓
  -- P·(Dg·Df) = P·([[0,1],[0,0]]·[[0,0],[1,0]]) = P·[[1,0],[0,0]] = [[1,0],[0,0]] ≠ 0
  let Df : Matrix (Fin 2) (Fin 2) ℝ :=
    fun i j => match i, j with | 0, 0 => 0 | 0, 1 => 0 | 1, 0 => 1 | 1, 1 => 0
  let Dg : Matrix (Fin 2) (Fin 2) ℝ :=
    fun i j => match i, j with | 0, 0 => 0 | 0, 1 => 1 | 1, 0 => 0 | 1, 1 => 0
  let P : Matrix (Fin 2) (Fin 2) ℝ :=
    fun i j => match i, j with | 0, 0 => 1 | 0, 1 => 0 | 1, 0 => 0 | 1, 1 => 0
  refine ⟨Df, Dg, P, ?_, ?_, ?_⟩
  · -- NonzeroProjection P
    refine {
      is_proj := {
        idempotent := by
          funext i j; fin_cases i <;> fin_cases j <;> simp [P, Matrix.mul_apply]
        symmetric := by
          funext i j; fin_cases i <;> fin_cases j <;> simp [P]
      }
      nonzero := by
        intro hzero
        have h00 : P 0 0 = 0 := congrFun (congrFun hzero 0) 0
        simp [P] at h00
    }
  · -- strictSilence Df P
    unfold strictSilence
    funext i j; fin_cases i <;> fin_cases j <;> simp [P, Df, Matrix.mul_apply]
  · -- ¬strictSilence (Dg * Df) P
    unfold strictSilence
    intro hzero
    have h00 : (P * (Dg * Df)) 0 0 = 0 := by rw [hzero]; rfl
    -- 计算 (P·(Dg·Df))[0,0]
    -- Dg·Df = [[0,1],[0,0]]·[[0,0],[1,0]] = [[1,0],[0,0]]
    -- P·([[1,0],[0,0]]) = [[1,0],[0,0]]·[[1,0],[0,0]] = [[1,0],[0,0]]
    -- 所以 (P·(Dg·Df))[0,0] = 1
    have hcalc : (P * (Dg * Df)) 0 0 = 1 := by
      norm_num [P, Dg, Df, Matrix.mul_apply]
    rw [hcalc] at h00
    norm_num at h00

/-!#############################################################################
  三级分层架构
  #############################################################################-/

/-- 静默度（连续量）：S_mor(f; Λ) = 1 - ||P_V D(f)|| / ||D(f)|| ∈ [0,1]。
    使用 Frobenius 范数作为矩阵范数。
    严格静默 = 1，原二值判据的连续推广。 -/
noncomputable def silenceDegree {m n : ℕ} (Df : Matrix (Fin m) (Fin n) ℝ)
    (P : Matrix (Fin m) (Fin m) ℝ) : ℝ :=
  if h : Df = 0 then 1
  else 1 - (Matrix.frobeniusNorm (P * Df)) / (Matrix.frobeniusNorm Df)

/-- 可见性函数（定义 R7）：v(f) = ||P_V D(f)|| / ||D(f)|| ∈ [0,1]。
    v(f) = 1 - S_mor(f)。 -/
noncomputable def visibility {m n : ℕ} (Df : Matrix (Fin m) (Fin n) ℝ)
    (P : Matrix (Fin m) (Fin m) ℝ) : ℝ :=
  if h : Df = 0 then 0
  else (Matrix.frobeniusNorm (P * Df)) / (Matrix.frobeniusNorm Df)

/-- 三级分层的类型定义。 -/
/-- 静默严格性分级（strict/asymptotic/epsilon）。
    注（2026-08-13 登记册⑧）：与 MultiSilenceMethodology `SilenceLayer`（S1-S4 数据表）
    及 BranchCounting `LayerIndex`（5 层层索引）**不同义**——本处为严格性分级，
    SilenceLayer 为静默层数据记录，LayerIndex 为 4-范畴态射层索引。近名不同义，
    引用时注意限定 namespace（信息偏差高风险源）。 -/
inductive SilenceLevel : Type where
  | strict    : SilenceLevel   -- P_V D(f) = 0，最强
  | asymptotic : SilenceLevel  -- 可见性指数衰减至 0
  | epsilon   : SilenceLevel   -- 可见性 ≤ ε，最弱

/-!#############################################################################
  定理 R8：渐近静默态射族的乘法封闭（半群律下）
  #############################################################################-/

/-- 态射半群律条件：D(f_{t+s}) = D(f_t) D(f_s)。 -/
def semigroupLaw {n : ℕ} (Df : ℕ → Matrix (Fin n) (Fin n) ℝ) : Prop :=
  ∀ t s : ℕ, Df (t + s) = Df t * Df s

/-- 压缩条件：‖D(f_t)‖ ≤ 1 对所有 t。 -/
def contractiveSemigroup {n : ℕ} (Df : ℕ → Matrix (Fin n) (Fin n) ℝ) : Prop :=
  ∀ t : ℕ, Matrix.frobeniusNorm (Df t) ≤ 1

/-- 定理 R8（渐近静默的半群封闭，算子范数版）。
    设 {f_t} 满足 D(f_{t+s}) = D(f_t) D(f_s) 且 ‖D(f_t)‖ ≤ 1 对所有 t。
    若 ‖P·D(f_t)‖ ≤ C·e^{-γt}·‖D(f_t)‖（即 v(f_t) ≤ C·e^{-γt}），
    则对任意 s：‖P·D(f_{t+s})‖ ≤ C·e^{-γt}·‖D(f_t)‖·‖D(f_s)‖。

    注意：v(f_{t+s}) ≤ v(f_t) 的条件是 ‖D(f_t)‖·‖D(f_s)‖ = ‖D(f_t)·D(f_s)‖
    （如等距半群），这在一般矩阵范数下并不必然成立。
    RAP 文档的原始证明使用了 ‖D(f_t)·D(f_s)‖ = ‖D(f_t)‖·‖D(f_s)‖
    这一额外假设。本形式化中给出的是无条件成立的算子范数衰减版本。 -/
theorem semigroup_closure_asymptotic_silence {n : ℕ} (Df : ℕ → Matrix (Fin n) (Fin n) ℝ)
    (P : Matrix (Fin n) (Fin n) ℝ) (hsemigroup : semigroupLaw Df)
    (hcontractive : contractiveSemigroup Df)
    (C γ : ℝ) (hpos_γ : 0 < γ)
    (hbound : ∀ t : ℕ, Matrix.frobeniusNorm (P * Df t) ≤ C * Real.exp (-γ * (t : ℝ)) *
      Matrix.frobeniusNorm (Df t)) :
    ∀ t s : ℕ, Matrix.frobeniusNorm (P * Df (t + s)) ≤
      C * Real.exp (-γ * (t : ℝ)) * (Matrix.frobeniusNorm (Df t) * Matrix.frobeniusNorm (Df s)) := by
  intro t s
  -- 使用半群律：Df(t+s) = Df(t) * Df(s)
  have hsem : Df (t + s) = Df t * Df s := hsemigroup t s
  rw [hsem]

  -- 重写目标
  have hgoal : Matrix.frobeniusNorm (P * (Df t * Df s)) ≤
    C * Real.exp (-γ * (t : ℝ)) * (Matrix.frobeniusNorm (Df t) * Matrix.frobeniusNorm (Df s)) := by
    -- 使用范数次乘性
    calc
      Matrix.frobeniusNorm (P * (Df t * Df s)) =
          Matrix.frobeniusNorm ((P * Df t) * Df s) := by
        rw [Matrix.mul_assoc]
      _ ≤ Matrix.frobeniusNorm (P * Df t) * Matrix.frobeniusNorm (Df s) :=
        Matrix.frobeniusNorm_mul_le _ _
      _ ≤ (C * Real.exp (-γ * (t : ℝ)) * Matrix.frobeniusNorm (Df t)) * Matrix.frobeniusNorm (Df s) := by
        nlinarith [hbound t, Matrix.frobeniusNorm_nonneg (P * Df t),
          Matrix.frobeniusNorm_nonneg (Df s)]
      _ = C * Real.exp (-γ * (t : ℝ)) * (Matrix.frobeniusNorm (Df t) * Matrix.frobeniusNorm (Df s)) := by ring

  exact hgoal

/-- 推论 R8a（可见性衰减的上界）：在定理 R8 条件下，若额外假定 ‖Df_t‖ ≤ 1（压缩半群），
    则 ‖P·Df_{t+s}‖ ≤ C·e^{-γt}·‖Df_s‖。
    进一步若 ‖Df_s‖ ≤ 1，则 ‖P·Df_{t+s}‖ ≤ C·e^{-γt}。 -/
theorem corollary_R8a {n : ℕ} (Df : ℕ → Matrix (Fin n) (Fin n) ℝ)
    (P : Matrix (Fin n) (Fin n) ℝ) (hsemigroup : semigroupLaw Df)
    (hcontractive : contractiveSemigroup Df)
    (C γ : ℝ) (hpos_γ : 0 < γ) (hC : 0 ≤ C)
    (hbound : ∀ t : ℕ, Matrix.frobeniusNorm (P * Df t) ≤ C * Real.exp (-γ * (t : ℝ)) *
      Matrix.frobeniusNorm (Df t)) :
    ∀ t s : ℕ, Matrix.frobeniusNorm (P * Df (t + s)) ≤ C * Real.exp (-γ * (t : ℝ)) := by
  intro t s
  have h_main : Matrix.frobeniusNorm (P * Df (t + s)) ≤
    C * Real.exp (-γ * (t : ℝ)) * (Matrix.frobeniusNorm (Df t) * Matrix.frobeniusNorm (Df s)) :=
    semigroup_closure_asymptotic_silence Df P hsemigroup hcontractive C γ hpos_γ hbound t s
  have h_norm_t : Matrix.frobeniusNorm (Df t) ≤ 1 := hcontractive t
  have h_norm_s : Matrix.frobeniusNorm (Df s) ≤ 1 := hcontractive s
  have h_nonneg_norm_t : 0 ≤ Matrix.frobeniusNorm (Df t) := Matrix.frobeniusNorm_nonneg (Df t)
  have h_nonneg_norm_s : 0 ≤ Matrix.frobeniusNorm (Df s) := Matrix.frobeniusNorm_nonneg (Df s)
  have h_exp_nonneg : 0 ≤ Real.exp (-γ * (t : ℝ)) := (Real.exp_pos (-γ * (t : ℝ))).le
  calc
    Matrix.frobeniusNorm (P * Df (t + s)) ≤
        C * Real.exp (-γ * (t : ℝ)) * (Matrix.frobeniusNorm (Df t) * Matrix.frobeniusNorm (Df s)) := h_main
    _ ≤ C * Real.exp (-γ * (t : ℝ)) * 1 := by
      have hab : Matrix.frobeniusNorm (Df t) * Matrix.frobeniusNorm (Df s) ≤ 1 := by
        nlinarith [h_norm_t, h_norm_s, h_nonneg_norm_t, h_nonneg_norm_s]
      have hce : 0 ≤ C * Real.exp (-γ * (t : ℝ)) := mul_nonneg hC h_exp_nonneg
      exact mul_le_mul_of_nonneg_left hab hce
    _ = C * Real.exp (-γ * (t : ℝ)) := by ring

/-!#############################################################################
  定理 R9 机制Ⅰ：超收缩 / IFS 型（有限维对角收缩）
  #############################################################################-/

/-- 对角收缩矩阵 W_n = diag(c₁^n, c₂^n, ..., c_k^n)，其中 c_i ∈ (0,1) 为收缩因子。
    用于有限维原型的机制Ⅰ：D(f_n) = W_n · D(f_0)（左乘收缩矩阵）。 -/
def contractionMatrix {k : ℕ} (c : Fin k → ℝ) (n : ℕ) : Matrix (Fin k) (Fin k) ℝ :=
  Matrix.diagonal (fun i => (c i) ^ n)

/-- 收缩因子条件：0 < c_i < 1。 -/
def validContractionFactors {k : ℕ} (c : Fin k → ℝ) : Prop :=
  ∀ i, 0 < c i ∧ c i < 1

/-- 机制Ⅰ（有限维原型，条目级上界）：
    设 W_n = diag(c_i^n) 为对角收缩矩阵，c_max = max_i c_i。
    D(f_n) = W_n · T（左乘）。

    则 (P·D(f_n))_{ij} = (P·W_n·T)_{ij} 满足逐项上界：
    |(P·W_n·T)_{ij}| ≤ c_max^n · max_i |(P·T)_{ij}|

    证明：对对角投影 P（即在基方向上的正交投影），
    (P·W_n)_{ii} = p_i·c_i^n，其中 p_i ∈ {0,1} 为 P 的对角元，
    故 (P·W_n·T)_{ij} = p_i·c_i^n·T_{ij} = c_i^n·(P·T)_{ij}，
    因此 |(P·W_n·T)_{ij}| ≤ c_max^n·|(P·T)_{ij}|。 -/
theorem mechanism_I_contraction_entrywise {k : ℕ} [NeZero k] (c : Fin k → ℝ) (T : Matrix (Fin k) (Fin k) ℝ)
    (P : Matrix (Fin k) (Fin k) ℝ) (hc : validContractionFactors c)
    (hP_diagonal_proj : ∀ i j : Fin k, (i ≠ j → P i j = 0) ∧ (P i i = 0 ∨ P i i = 1)) :
    ∀ (n : ℕ) (i j : Fin k),
      |(P * (contractionMatrix c n * T)) i j| ≤
        (Finset.sup' Finset.univ (by exact ⟨0, Finset.mem_univ 0⟩) c) ^ n * |(P * T) i j| := by
  intro n i j
  set W := contractionMatrix c n with hW_def
  set c_max := Finset.sup' (Finset.univ : Finset (Fin k))
    (by exact ⟨0, Finset.mem_univ 0⟩) c with hc_max_def
  have h_row_zero : ∀ l : Fin k, l ≠ i → P i l = 0 :=
    fun l hl => (hP_diagonal_proj i l).1 (Ne.symm hl)

  -- 展开矩阵乘法
  calc
    |(P * (W * T)) i j| = |(P * (Matrix.diagonal (fun i' => (c i') ^ n) * T)) i j| := rfl
    _ = |∑ l : Fin k, (P * Matrix.diagonal (fun i' => (c i') ^ n)) i l * T l j| := by
      rw [← Matrix.mul_assoc]
      rfl
    _ = |∑ l : Fin k, (P i l * (c l) ^ n) * T l j| := by
      simp [Matrix.mul_apply, Matrix.diagonal_apply, Matrix.diagonal_apply_eq]
    -- P 只在 i 行 i 列非零（由 hP_diagonal_proj）：求和仅剩 l = i 项
    _ = |(P i i * (c i) ^ n) * T i j| := by
      have hsum : (∑ l : Fin k, (P i l * (c l) ^ n) * T l j) = (P i i * (c i) ^ n) * T i j := by
        rw [Finset.sum_eq_single i]
        · intro l _hl_in hl_ne
          simp [h_row_zero l hl_ne]
        · intro hnotin
          exact False.elim (hnotin (Finset.mem_univ i))
      simp [hsum]
    _ = |P i i| * |(c i) ^ n| * |T i j| := by
      simp [abs_mul]
    _ = |P i i| * ((c i) ^ n) * |T i j| := by
      have hci_pos : 0 ≤ c i := by
        have hpos : 0 < c i := (hc i).1
        exact le_of_lt hpos
      simp [abs_of_nonneg (by positivity : 0 ≤ (c i) ^ n)]
    _ = |P i i| * |T i j| * (c i) ^ n := by ring
    _ = |P i i * T i j| * (c i) ^ n := by rw [← abs_mul]
    _ = |(P * T) i j| * (c i) ^ n := by
      have h_pt : (P * T) i j = P i i * T i j := by
        rw [Matrix.mul_apply, Finset.sum_eq_single i]
        · intro l _hl_in hl_ne
          simp [h_row_zero l hl_ne]
        · intro hnotin
          exact False.elim (hnotin (Finset.mem_univ i))
      rw [h_pt]
    _ ≤ |(P * T) i j| * (c_max ^ n) := by
      have hci_le_cmax : c i ≤ c_max :=
        Finset.le_sup' (fun x => c x) (Finset.mem_univ i)
      have hci_nonneg : 0 ≤ c i := le_of_lt (hc i).1
      have hcmax_nonneg : 0 ≤ c_max := by
        have h0 : 0 ≤ c 0 := le_of_lt (hc 0).1
        have hle : c 0 ≤ c_max :=
          Finset.le_sup' (fun x => c x) (Finset.mem_univ 0)
        exact le_trans h0 hle
      exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hci_nonneg hci_le_cmax n)
        (abs_nonneg ((P * T) i j))
    _ = c_max ^ n * |(P * T) i j| := by ring

end UFPFormalization.RAP4
