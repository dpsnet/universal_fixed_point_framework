import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Data.Matrix.Basic

/-!
# 谱熵退化定理：简并基态谱熵 = ln g（全息定理化·推荐组合 1a+1b）

对应 `notes/04_lorentz_gravity/全息定理化_语义缺口候选清单.md` 缺口 1：1a 谱熵（Paper VII §5.1，
S = −Tr(A ln A) 的有限维权重口径）与 1b 简并度熵（S = ln g₀）的桥接。

物理：简并基态 g 个等概率态 ρ = (1/g)·I_g ⊕ 0，谱熵 S = −Σ pᵢ ln pᵢ
      = −g·(1/g)·ln(1/g) = ln g —— "1b 是 1a 在简并谱上的特例"的机器验证。

本文件只处理**权重口径**（谱熵对权重向量的定义），矩阵版（Matrix.diagonal +
HermitianFunctionalCalculus）为后续扩展——对应 BCSFermiEmergence 的既有
（Real.log 1+exp 类）模板，但谱熵需要 log 对密度矩阵的作用，暂以权重版先行。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.HolographicEntropy

/-- 谱熵（权重口径）：S = −∑ᵢ wᵢ·log(wᵢ)（Paper VII §5.1 有限维退化；0·log0 项自动为 0） -/
noncomputable def entropyOfRange (g : ℕ) : ℝ :=
  - (Finset.range g).sum (fun _ : ℕ => (1 : ℝ) / (g : ℝ) * Real.log ((1 : ℝ) / (g : ℝ)))

/-- 简并基态谱熵：S = ln g（0 < g）。ρ = (1/g)·I_g ⊕ 0 的熵。 -/
theorem uniform_entropy_eq_log_g (g : ℕ) (hg : 0 < g) :
    entropyOfRange g = Real.log (g : ℝ) := by
  unfold entropyOfRange
  -- ∑ 含 g 个相同项：(Finset.range g).sum 常数 c = g·c
  have hcard : (Finset.range g).card = g := Finset.card_range g
  rw [Finset.sum_const, hcard]
  -- 目标：-(g:ℝ) * ((1:ℝ)/(g:ℝ) * Real.log ((1:ℝ)/(g:ℝ))) = Real.log (g:ℝ)
  have hg0 : (0 : ℝ) < (g : ℝ) := by exact_mod_cast hg
  have hgne : (g : ℝ) ≠ 0 := ne_of_gt hg0
  -- log(1/g) = -log g（(1/g) = (g)⁻¹）
  have hlog : Real.log ((1 : ℝ) / (g : ℝ)) = -Real.log (g : ℝ) := by
    rw [one_div]
    rw [Real.log_inv]
  -- 化简 (g:ℝ)·(1/(g:ℝ)) = 1 后 ring 收尾
  rw [hlog]
  rw [nsmul_eq_mul]
  rw [← mul_assoc]
  have hone : (g : ℝ) * ((1 : ℝ) / (g : ℝ)) = 1 := by
    field_simp [hgne]
  rw [hone]
  ring

/-- 系数量化（1b 数值形态）：g=2 时 S = ln 2；g=4 时 S = ln 4 = 2·ln 2（BH 简并口径） -/
theorem entropy_log_two (hg : 0 < 2) :
    entropyOfRange 2 = Real.log 2 := by
  exact uniform_entropy_eq_log_g 2 hg

theorem entropy_log_four :
    entropyOfRange 4 = Real.log 4 := by
  exact uniform_entropy_eq_log_g 4 (by norm_num)

/-! ## τ 全冻结简并熵（S127——2026-10-27，质量锚链 ↔ 全息骨架桥）

E_τ 主导 16ln15 = 全冻结态数 15^16 的简并熵（质量锚链 S123-S126 的
熵身份——τ = 全冻结端点——简并度 g = 15^16）——全息骨架已机检定理
uniform_entropy_eq_log_g 的直接应用："为何 τ 对应全态熵"的桥——
τ 的简并度 = 全冻结态数 ⟹ 简并熵 = ln(15^16) = 16ln15 = E_τ 主导。
诚实边界："为何 τ 的简并度 = 15^16（全冻结）"仍开放（谱端点语义）。
-/

/-- τ 全冻结简并熵：entropyOfRange(15^16) = 16·ln15（全冻结态数的简并熵 =
E_τ 主导——质量锚 ↔ 全息熵桥）。 -/
theorem tau_full_freeze_entropy :
    entropyOfRange (15 ^ 16) = (16 : ℝ) * Real.log 15 := by
  rw [uniform_entropy_eq_log_g (15 ^ 16) (pow_pos (by norm_num : (0 : ℕ) < 15) 16)]
  have hcast : ((15 ^ 16 : ℕ) : ℝ) = (15 : ℝ) ^ 16 := by
    norm_num [Nat.cast_pow]
  rw [hcast]
  rw [Real.log_pow]
  norm_num

/-! ## 矩阵版谱熵代数骨架（S590——2026-10-30，文件头'矩阵版后续扩展'缺口的
代数核先行）

文件头登记：权重口径（entropyOfRange）先行，矩阵版（Matrix.diagonal +
HermitianFunctionalCalculus）为后续扩展。本段锚定矩阵口径的**代数骨架**
（不依赖矩阵对数——HermitianFunctionalCalculus 为后续）：
  ① 对角矩阵的迹 = 对角元素和（Matrix.diagonal——迹的代数核）
  ② 简并密度矩阵 ρ = (1/g)·I_g 的归一化：Tr(ρ) = g·(1/g) = 1
  ③ 矩阵口径谱熵 −Tr(ρ·ln ρ) = ln g 的特征值基础：ρ 的特征值谱
     = {1/g 重数 g}——谱熵 −Σλ·ln λ 与权重口径 entropyOfRange
     同一物理量（特征值即权重——对角密度矩阵）
诚实边界：Matrix.log（HermitianFunctionalCalculus）未引入——
完整矩阵版谱熵定理（−Tr(ρ·ln ρ) = ln g 的矩阵形式）为后续扩展。
-/

/-- 对角矩阵的迹 = 对角元素和（S590——Matrix.diagonal 的迹代数核——
  密度矩阵 Tr(ρ) = Σᵢ(1/g) 的基础——矩阵口径谱熵的特征值求和）。 -/
theorem diag_trace_sum {n : ℕ} (v : Fin n → ℝ) :
    (Matrix.diagonal v).trace = ∑ i : Fin n, v i := by
  simp [Matrix.trace, Matrix.diagonal]

/-- 简并密度矩阵归一化：ρ = (1/g)·I_g 的迹 = 1（g 个等概率态——S590——
  矩阵口径谱熵 −Tr(ρ·ln ρ) = ln g 的归一化条件——Tr(ρ) = 1）。 -/
theorem density_trace_unit (g : ℕ) (hg : 0 < g) :
    ((1 : ℝ) / (g : ℝ)) * (g : ℝ) = 1 := by
  field_simp [ne_of_gt (by exact_mod_cast hg : (0 : ℝ) < (g : ℝ))]

/-- 对角简并密度矩阵归一化（S590——组合）：ρ = (1/g)·I_g 的迹 = 1——
  diag_trace_sum + density_trace_unit 的组合——矩阵口径谱熵的归一化
  密度矩阵。 -/
theorem density_matrix_trace_unit (g : ℕ) (hg : 0 < g) :
    (Matrix.diagonal (fun _ : Fin g => (1 : ℝ) / (g : ℝ))).trace = 1 := by
  rw [diag_trace_sum]
  rw [Finset.sum_const, Finset.card_fin]
  rw [nsmul_eq_mul]
  rw [mul_comm]
  exact density_trace_unit g hg

/-! ## 矩阵版谱熵对角定理（S592——2026-10-30，文件头'矩阵版后续扩展'的
核心闭合——显式逐点对数口径）

矩阵版谱熵的完整定理（对角密度矩阵口径）：ρ = (1/g)·I_g（对角）——
谱熵 S_mat = −Tr(ρ · log ρ)——**对角矩阵的对数 = 逐点对数**
（diag(v)·diag(w) = diag(v·w)——不含矩阵对数/泛函演算——
对角矩阵的对数作用可显式定义）。于是
  S_mat = −Tr(diag(1/g) · diag(log(1/g)))
        = −Tr(diag((1/g)·log(1/g)))
        = −g·(1/g)·log(1/g) = −log(1/g) = log g
——与权重口径 uniform_entropy_eq_log_g 同一物理量的矩阵实现。
诚实边界：非对角一般密度矩阵需 HermitianFunctionalCalculus
（Matrix.log）——本段闭合对角情况（简并基态恰是对角）。
-/

/-- 矩阵版谱熵（对角密度矩阵口径——显式逐点对数，不含泛函演算）：
   S_mat(ρ) = −Tr(ρ·log_diag(ρ))——ρ = (1/g)·I_g（对角）——
   diag 乘法 = 逐点积——迹 = g·(1/g)·log(1/g) = −ln g。 -/
noncomputable def entropyMatrixDiag (g : ℕ) : ℝ :=
  - (Matrix.diagonal (fun _ : Fin g => (1 : ℝ) / (g : ℝ)) *
     Matrix.diagonal (fun _ : Fin g => Real.log ((1 : ℝ) / (g : ℝ)))).trace

/-- 对角矩阵乘积 = 逐点积（S592——矩阵版谱熵的代数核：
   diag(v)·diag(w) = diag(v·w)——对角矩阵对数显式化的基础）。 -/
theorem diagonal_mul_diagonal (g : ℕ) (v w : Fin g → ℝ) :
    Matrix.diagonal v * Matrix.diagonal w =
      Matrix.diagonal (fun i : Fin g => v i * w i) := by
  ext i j
  by_cases hij : i = j
  · simp [Matrix.diagonal, Matrix.mul_apply, hij]
  · simp [Matrix.diagonal, Matrix.mul_apply, hij]

/-- 矩阵版谱熵对角定理：S_mat(ρ) = −Tr(diag(1/g)·diag(log(1/g))) = ln g——
  简并基态密度矩阵 ρ = (1/g)·I_g 的矩阵口径谱熵（S592——文件头
  '矩阵版后续扩展'的核心闭合——对角情况完整证明）。 -/
theorem entropy_matrix_diag_eq_log_g (g : ℕ) (hg : 0 < g) :
    entropyMatrixDiag g = Real.log (g : ℝ) := by
  unfold entropyMatrixDiag
  -- diag(1/g)·diag(log(1/g)) = diag((1/g)·log(1/g))
  rw [diagonal_mul_diagonal]
  -- 迹 = 对角元素和
  rw [diag_trace_sum]
  -- ∑ (fun _ => c) over Fin g = g·c
  rw [Finset.sum_const, Finset.card_fin]
  rw [nsmul_eq_mul]
  -- 目标：-( (g:ℝ) * ((1/g)·log(1/g)) ) = log g
  rw [← mul_assoc]
  have hg0 : (0 : ℝ) < (g : ℝ) := by exact_mod_cast hg
  have hgne : (g : ℝ) ≠ 0 := ne_of_gt hg0
  have hone : (g : ℝ) * ((1 : ℝ) / (g : ℝ)) = 1 := by
    field_simp [hgne]
  rw [hone]
  have hlog : Real.log ((1 : ℝ) / (g : ℝ)) = -Real.log (g : ℝ) := by
    rw [one_div]
    rw [Real.log_inv]
  rw [hlog]
  simp

/-- τ 全冻结简并熵——矩阵口径（S593——2026-10-30，S127 权重口径
  tau_full_freeze_entropy 与 S592 矩阵口径 entropy_matrix_diag_eq_log_g
  的两口径等价）：ρ_τ = (1/15^16)·I(15^16) 的矩阵谱熵 =
  −Tr(diag(1/15^16)·diag(log(1/15^16))) = 16·ln15 = E_τ 主导——
  全息熵（矩阵口径）⟺ 质量锚链（权重口径）同一物理量。 -/
theorem tau_full_freeze_entropy_matrix :
    entropyMatrixDiag (15 ^ 16) = (16 : ℝ) * Real.log 15 := by
  rw [entropy_matrix_diag_eq_log_g (15 ^ 16) (pow_pos (by norm_num : (0 : ℕ) < 15) 16)]
  have hcast : ((15 ^ 16 : ℕ) : ℝ) = (15 : ℝ) ^ 16 := by
    norm_num [Nat.cast_pow]
  rw [hcast]
  rw [Real.log_pow]
  norm_num

end MUFPF.HolographicEntropy
