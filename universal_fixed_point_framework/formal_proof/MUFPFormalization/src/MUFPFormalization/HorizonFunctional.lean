import Mathlib.Tactic

/-!
# 视界泛函模板：边界自由度密度的数学形态（环节 2a，2026-10-24）

对应 `notes/04_lorentz_gravity/全息定理化论证骨架_RecSp对偶.md` §2 环节 2a
（"边界自由度密度"的 MUFPF 定义未固化）与 2510.24491 对照表 §7 建议 1：
把式 (12) 的积分形式形式化为"视界泛函" ℱ[φ] := ∫ U·(∂_Uφ)² dU dvol_S。

本文件固化**离散模板**（Finset 求和，U 为视界采样点，U ∈ [-2ℓ, 0] 即 U ≤ 0）：

- `horizonFunctionalDisc us φ = Σ_{U∈us} U·φ(U)²`：视界泛函（2510 式 12 被积形态）；
- `relEntropyDisc us φ = -2π·ℱ`：**相对熵的离散形态**（式 12：S^rel = −2π∫U(∂_Uφ)²）；
- `relEntropyDisc_nonneg`：U ≤ 0（视界区）⟹ **相对熵 ≥ 0**——正性来源
  （对应 2311.13990 式 11 的 manifestly positive）；
- `horizonFunctionalDisc_smul`：**二次性**——ℱ[c·φ] = c²·ℱ[φ]（相干激发相对熵
  是 φ 的二次型，对应 2311 式 7 的双重对易子形态）。

诚实边界：本文件是**外部模板的数学形态固化**（离散化 + 正性 + 二次性）；
"边界自由度密度 = 视界泛函"的 MUFPF 本体语义（Rec 侧 Bun(∂Rec_D) 对接）未在此声明，
仍是语义缺口 2a。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.HorizonFunctional

/-- 视界泛函（离散模板）：ℱ[φ] = Σ_{U∈us} U·φ(U)²（2510 式 12 被积形态；
    U ∈ [-2ℓ, 0] 视界区，U ≤ 0）。 -/
noncomputable def horizonFunctionalDisc (us : Finset ℝ) (φ : ℝ → ℝ) : ℝ :=
  us.sum (fun U : ℝ => U * (φ U) ^ 2)

/-- 相对熵离散形态：S^rel = −2π·ℱ[φ]（2510 式 12：S^rel = −2π∫U(∂_Uφ)² dU dvol）。 -/
noncomputable def relEntropyDisc (us : Finset ℝ) (φ : ℝ → ℝ) : ℝ :=
  -((2 : ℝ) * Real.pi) * horizonFunctionalDisc us φ

/-- ★ 相对熵正性：视界区（U ≤ 0）⟹ S^rel ≥ 0（2311 式 11 manifestly positive 的
    离散模板；正性来源 = 视界 U 因子与 −2π 前缀）。 -/
theorem relEntropyDisc_nonneg (us : Finset ℝ) (φ : ℝ → ℝ)
    (hU : ∀ U ∈ us, U ≤ 0) : 0 ≤ relEntropyDisc us φ := by
  unfold relEntropyDisc horizonFunctionalDisc
  have hsum_nonpos : us.sum (fun U : ℝ => U * (φ U) ^ 2) ≤ 0 := by
    apply Finset.sum_nonpos
    intro U hU'
    have hU0 : U ≤ 0 := hU U hU'
    have hsq : 0 ≤ (φ U) ^ 2 := sq_nonneg (φ U)
    exact mul_nonpos_of_nonpos_of_nonneg hU0 hsq
  have hneg_sum : 0 ≤ -us.sum (fun U : ℝ => U * (φ U) ^ 2) := by linarith
  have hstep : 0 ≤ (2 : ℝ) * Real.pi * (-us.sum (fun U : ℝ => U * (φ U) ^ 2)) := by
    exact mul_nonneg (by positivity) hneg_sum
  calc
    0 ≤ (2 : ℝ) * Real.pi * (-us.sum (fun U : ℝ => U * (φ U) ^ 2)) := hstep
    _ = -((2 : ℝ) * Real.pi) * us.sum (fun U : ℝ => U * (φ U) ^ 2) := by ring

/-- ★ 二次性：ℱ[c·φ] = c²·ℱ[φ]（相干激发相对熵是 φ 的二次型，
    对应 2311 式 7 双重对易子形态）。 -/
theorem horizonFunctionalDisc_smul (us : Finset ℝ) (φ : ℝ → ℝ) (c : ℝ) :
    horizonFunctionalDisc us (fun U : ℝ => c * φ U) = c ^ 2 * horizonFunctionalDisc us φ := by
  unfold horizonFunctionalDisc
  calc
    us.sum (fun U : ℝ => U * (c * φ U) ^ 2)
        = us.sum (fun U : ℝ => c ^ 2 * (U * (φ U) ^ 2)) := by
          apply Finset.sum_congr rfl
          intro U hU'
          ring
    _ = c ^ 2 * us.sum (fun U : ℝ => U * (φ U) ^ 2) := by
      rw [Finset.mul_sum]

end MUFPF.HorizonFunctional
