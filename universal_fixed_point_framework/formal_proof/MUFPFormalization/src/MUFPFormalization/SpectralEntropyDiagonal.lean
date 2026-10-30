import Mathlib.Tactic
import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import MUFPFormalization.SpectralEntropy

/-!
# 谱熵对角归约（S1 阶段 2 收口，2026-10-24）

开放目标（登记于 SpectralEntropy.lean）：对角 Hermitian 的矩阵谱熵（特征值口径）
= 对角口径 densityEntropy。本文件闭合该目标：

**证明链（multiset 重排，不依赖特征值排序）**：
1. `roots_charpoly_eq_eigenvalues`（mathlib）：A.charpoly.roots = 特征值 multiset
   （Multiset.map (ofReal ∘ hA.eigenvalues) univ.val）；
2. `Matrix.charpoly_diagonal`（mathlib）：charpoly (diagonal d) = ∏ᵢ (X - C (d i))；
3. `Polynomial.roots_prod` + `roots_X_sub_C`：∏ᵢ (X - C (w i)) 的根 multiset
   = 对角元 multiset（bind 保留重数，无需互素假设）；
⟹ **特征值 multiset = 对角元 multiset（ℂ 层）**——排序无关；
4. multiset 相等 ⟹ 逐点求和相等（Finset.sum_val + Multiset.map_map）；
5. F(z) = z.re·log z.re 延拓：左侧 = Σ λᵢ·log λᵢ，右侧 = Σ wᵢ·log wᵢ
   （wᵢ=0 分支由 Real.log_zero 吸收：0·log0 = 0）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.SpectralEntropy

open Polynomial

/-- ★ 对角归约：对角 Hermitian 矩阵的谱熵（特征值口径）= 对角口径 densityEntropy。
    特征值 multiset 与对角元 multiset 相等（排序无关重排），
    S1 阶段 1（对角口径）与阶段 2（任意 Hermitian 口径）在此一致。 -/
theorem spectralEntropy_diagonal_eq_densityEntropy {n : ℕ} (w : Fin n → ℝ)
    (hA : (Matrix.diagonal (fun i : Fin n => (w i : ℂ))).IsHermitian) :
    matrixSpectralEntropy (Matrix.diagonal (fun i : Fin n => (w i : ℂ))) hA = densityEntropy w := by
  classical
  let F : ℂ → ℝ := fun z => z.re * Real.log z.re
  -- 特征值 multiset = 对角元 multiset（ℂ 层，排序无关）
  have hms : (Finset.univ.val.map (fun i : Fin n => (hA.eigenvalues i : ℂ)))
      = (Finset.univ.val.map (fun i : Fin n => (w i : ℂ))) := by
    calc
      (Finset.univ.val.map (fun i : Fin n => (hA.eigenvalues i : ℂ)))
          = (Matrix.diagonal (fun i : Fin n => (w i : ℂ))).charpoly.roots := by
              simpa using (hA.roots_charpoly_eq_eigenvalues).symm
      _ = (∏ i : Fin n, (X - C ((w i : ℂ)))).roots := by
              rw [Matrix.charpoly_diagonal]
      _ = (Finset.univ.val.map (fun i : Fin n => (w i : ℂ))) := by
              rw [Polynomial.roots_prod (fun i : Fin n => (X - C ((w i : ℂ)))) Finset.univ]
              · simp_rw [Polynomial.roots_X_sub_C]
                rw [Multiset.bind_singleton]
              · exact Finset.prod_ne_zero_iff.mpr
                  (fun i _ => Polynomial.X_sub_C_ne_zero ((w i : ℂ)))
  -- F 延拓一致：左侧
  have hF_left : ∀ i : Fin n,
      F ((hA.eigenvalues i : ℂ)) = hA.eigenvalues i * Real.log (hA.eigenvalues i) := by
    intro i
    simp [F]
  -- F 延拓一致：右侧（w=0 分支由 Real.log_zero 吸收）
  have hF_right : ∀ i : Fin n,
      F ((w i : ℂ)) = if w i = 0 then 0 else w i * Real.log (w i) := by
    intro i
    by_cases h0 : w i = 0
    · simp [F, h0, Real.log_zero]
    · simp [F, h0]
  -- multiset 相等 ⟹ 逐点求和相等
  have hsumF : (Finset.univ.sum (fun i : Fin n => F ((hA.eigenvalues i : ℂ))))
      = (Finset.univ.sum (fun i : Fin n => F ((w i : ℂ)))) := by
    change (Finset.univ.val.map (F ∘ (fun i : Fin n => (hA.eigenvalues i : ℂ)))).sum =
      (Finset.univ.val.map (F ∘ (fun i : Fin n => (w i : ℂ)))).sum
    rw [← Multiset.map_map, ← Multiset.map_map, hms]
  -- 组装：负号两侧消去
  rw [matrixSpectralEntropy, densityEntropy]
  apply congrArg Neg.neg
  calc
    (Finset.univ.sum (fun i : Fin n => hA.eigenvalues i * Real.log (hA.eigenvalues i)))
        = (Finset.univ.sum (fun i : Fin n => F ((hA.eigenvalues i : ℂ)))) := by
            apply Finset.sum_congr rfl
            intro i hi
            exact (hF_left i).symm
    _ = (Finset.univ.sum (fun i : Fin n => F ((w i : ℂ)))) := hsumF
    _ = (Finset.univ.sum (fun i : Fin n => if w i = 0 then 0 else w i * Real.log (w i))) := by
            apply Finset.sum_congr rfl
            intro i hi
            exact hF_right i

end MUFPF.SpectralEntropy
