-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：5
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
# WeaveBCS.lean — Phase 55D BCS Spectral Weave Formalization

Formalizes the BCS superconductivity spectral weave analysis from
  spectral_BCS_weave.md v0.9

Five components:
  1. BCS parameters and spectral weave degree of freedom d_BCS = √3·√r
  2. Spectral flow self-consistency closure (§5.5): a_BCS³ = (1+√3√r)·r/(4π)
  3. Strong coupling two-step scheme (§7.3): Z=1+λ, GK r correction
  4. Connection to WeaveProductFiber: BCS weave sections on Temp × RG
  5. Numerical verification constants (Pb, Hg, Al, Sn, Nb)

Based on:
  spectral_BCS_weave.md v0.9
  SpectralGap.lean (dl_min, spectralGap 8)
  WeaveProductFiber.lean (product base, pullback functors)
  TempRGFiber.lean (BCSSection_cl17, QCDSection_cl17)
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Tactic
import MUFPFormalization.TempRGFiber
import MUFPFormalization.SpectralGap
import MUFPFormalization.WeaveProductFiber

open CategoryTheory
open Real

namespace MUFPF

/-! =========================================================
    Section 1: BCS Universal Constants — Parameter Structure
   ========================================================= -/

/-- Standard BCS universal ratio: a_BCS = T_c / Δ_0 = 1/1.764.
    This is the universal BCS prediction, independent of material parameters. -/
noncomputable def a_BCS : ℝ := 1 / 1.764

/-- The Cl(1,7) fundamental spectral gap: dl_min = spectralGap 8.
    This is the basic spectral gap used in both QCD and BCS spectral frameworks. -/
noncomputable def dl_min : ℝ := spectralGap 8

/-- SU(3) spectral gap: dl_3 = √2 · dl_min (from Cl(1,7) spectral embedding).
    In the spectral framework, the three gauge group gaps satisfy:
    dl_1 : Δλ_2 : dl_3 = √(1/3) : 1 : √2    【2026-08-06 修复】√(2/3)→√(1/3)
    where Δλ_2 = dl_min (SU(2) Casimir spectral gap). -/
noncomputable def dl_3 : ℝ := Real.sqrt 2 * dl_min

/-- U(1) spectral gap: dl_1 = √(1/3) · dl_min.
    【2026-08-06 修复】第一分量由 √(2/3) 更正为 √(1/3)：SU(2) Casimir 特征值归一化
    λ_k = √(k(k+1)) 严格给出 Δλ₁:Δλ₂:Δλ₃ = 1/√3:1:√2（见 scripts/paperX_ratio_fix.py
    与笔记 spectral_color_dynamics.md §8.4 修复子节）。原 √(2/3) 为拼凑值。 -/
noncomputable def dl_1 : ℝ := Real.sqrt (1/3) * dl_min

/-- SU(2) representation Casimir: C₂(𝔰𝔲(2)_fund) = 3/4. -/
noncomputable def C2_su2_fund : ℝ := (3 : ℝ)/4

/-- Lorentz Casimir: C₂(𝔰𝔬(1,1)) = -1.
    In the spectral framework, the absolute value is used for norm calculations. -/
noncomputable def C2_so11 : ℝ := -1

/-! =========================================================
    Section 2: Spectral Weave Degree of Freedom d_BCS
   ========================================================= -/

/-- Spectral gap ratio r = dl_min / dl_BCS.
    This is the fundamental parameter determining the BCS spectral weave. -/
noncomputable def r (dl_BCS : ℝ) : ℝ := dl_min / dl_BCS

/-- BCS spectral weave degree of freedom from spectral flow generator norm conservation.
    d_BCS = g_s · √(C₂(𝔰𝔲(2)_fund)/|C₂(𝔰𝔬(1,1))|) · √r = √3 · √r
    where g_s = 2 (spin degeneracy), C₂(𝔰𝔲(2)_fund) = 3/4, |C₂(𝔰𝔬(1,1))| = 1.
    
    Reference: spectral_BCS_weave.md §5.5.4 Theorem 5.3. -/
noncomputable def d_BCS (dl_BCS : ℝ) : ℝ := Real.sqrt 3 * Real.sqrt (r dl_BCS)

/-- BCS spectral framework ratio a_SC formula (cube root form).
    a_SC((e_ch, C_ch, N_ch), (dl_min, dl_BCS), d_BCS, Z) =
      ((e_ch·C_ch + d_BCS/Z)/(4π·N_ch) · (dl_min/dl_BCS))^{1/3}
    
    For s-wave single-channel BCS: e_ch = 1, C_ch = 1, N_ch = 1.
    Reference: spectral_BCS_weave.md (2.1), (7.4). -/
noncomputable def a_SC (dl_BCS : ℝ) (Z : ℝ) : ℝ :=
  ((1 + d_BCS dl_BCS / Z) / (4 * Real.pi) * (r dl_BCS))

/-- a_SC with Z = 1 (no wavefunction renormalization):
    used for the weak-coupling BCS universal comparison. -/
noncomputable def a_SC_weak (dl_BCS : ℝ) : ℝ := a_SC dl_BCS 1

/-! =========================================================
    Section 3: Spectral Flow Self-Consistency Closure (§5.5.4)
   ========================================================= -/

/-
※ 开放项登记（2026-08-04 正本清源）：谱流自洽方程
    a_BCS³ · 4π = (1 + √3·√r)·r
    的数值解为 r ≈ 0.8740（对应 dl_BCS ≈ 0.1396）。
    原 `theorem spectral_flow_self_consistency_numerical ... := by sorry` 以精确等式
    陈述该近似（a_BCS³·4π ≈ 2.2899 而 RHS ≈ 2.2892，差值 < 0.001 但非精确相等），
    在 Lean 实数层不可证，且作为"定理"是伪陈述。数值验证在 Python 层完成：
    spectral_BCS_v2_comprehensive.py Q1。此处不再以假定理形式保留。
-/

/-- 谱流自洽函数 f(r) = (1 + √3·√r)·r（G2 定理化载体）。
    谱流自洽方程 a_BCS³·4π = f(r) 的正实根即谱间隙比 r = dl_min/dl_BCS。 -/
noncomputable def selfConsFunc (r : ℝ) : ℝ := (1 + Real.sqrt 3 * Real.sqrt r) * r

/-- 自洽函数在 r > 0 处严格为正。 -/
theorem selfConsFunc_pos {r : ℝ} (hr : 0 < r) : 0 < selfConsFunc r := by
  have h1 : 0 < 1 + Real.sqrt 3 * Real.sqrt r :=
    lt_of_lt_of_le zero_lt_one
      (le_add_of_nonneg_right (mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)))
  exact mul_pos h1 hr

/-- 自洽函数在 [0,∞) 连续。 -/
theorem selfConsFunc_continuous : Continuous selfConsFunc := by
  have harg : Continuous fun r : ℝ => (1 : ℝ) + Real.sqrt 3 * Real.sqrt r :=
    continuous_const.add (continuous_const.mul Real.continuous_sqrt)
  exact harg.mul continuous_id'

/-- 辅助：g(r) = √r·r 在 [0,∞) 严格递增。 -/
theorem sqrt_mul_self_strictMonoOn_Ici :
    StrictMonoOn (fun r : ℝ => Real.sqrt r * r) (Set.Ici 0) := by
  intro a ha b hb hab
  have hsqrt_le : Real.sqrt a ≤ Real.sqrt b := Real.sqrt_le_sqrt hab.le
  have hbpos : 0 < b := lt_of_le_of_lt ha hab
  have hsqrt_b_pos : 0 < Real.sqrt b := Real.sqrt_pos_of_pos hbpos
  have h1 : Real.sqrt a * a ≤ Real.sqrt b * a := mul_le_mul_of_nonneg_right hsqrt_le ha
  have h2 : Real.sqrt b * a < Real.sqrt b * b := mul_lt_mul_of_pos_left hab hsqrt_b_pos
  exact lt_of_le_of_lt h1 h2

/-- 自洽函数在 [0,∞) 严格递增。 -/
theorem selfConsFunc_strictMonoOn_Ici : StrictMonoOn selfConsFunc (Set.Ici 0) := by
  intro a ha b hb hab
  have hg := sqrt_mul_self_strictMonoOn_Ici ha hb hab
  have h3pos : 0 < Real.sqrt 3 := Real.sqrt_pos_of_pos (by norm_num : (0:ℝ) < 3)
  have hterm : 0 < Real.sqrt 3 * (Real.sqrt b * b - Real.sqrt a * a) :=
    mul_pos h3pos (sub_pos.mpr hg)
  have key : selfConsFunc b - selfConsFunc a
      = (b - a) + Real.sqrt 3 * (Real.sqrt b * b - Real.sqrt a * a) := by
    simp only [selfConsFunc]; ring
  have hdiff : 0 < selfConsFunc b - selfConsFunc a := by
    rw [key]; linarith [sub_pos.mpr hab, hterm]
  exact sub_pos.mp hdiff

/-- 自洽函数的下界：x ≥ 0 时 f(x) ≥ x（因 1 + √3·√x ≥ 1）。 -/
theorem selfConsFunc_ge_of_nonneg {x : ℝ} (hx : 0 ≤ x) : x ≤ selfConsFunc x := by
  have h1 : (1:ℝ) ≤ 1 + Real.sqrt 3 * Real.sqrt x :=
    le_add_of_nonneg_right (mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
  calc x = 1 * x := (one_mul x).symm
    _ ≤ (1 + Real.sqrt 3 * Real.sqrt x) * x := mul_le_mul_of_nonneg_right h1 hx

/-- **G2 定理（谱流自洽方程正实根的存在唯一性）**：对任意 c > 0，方程
    f(r) = c 在 [0,∞) 上存在唯一解 r*。取 c = a_BCS³·4π（BCS 弱耦合普适比值，
    物理输入）时，r* 即谱间隙比——r 由此从"数值解出的自由参数"提升为
    "由普适输入经显式方程唯一确定的普适比值"。精确数值等式 r* = 0.8740
    在 Lean 实数层不可证（见上方 2026-08-04 开放项登记），此处确立其
    方程确定性与唯一性，数值值由 Python 层独立给出。 -/
theorem selfConsFunc_existsUnique (c : ℝ) (hc : 0 < c) :
    ∃! r : ℝ, 0 ≤ r ∧ selfConsFunc r = c := by
  have hcont := selfConsFunc_continuous
  -- 无界性：每个 c > 0 都有 R > 0 使 c ≤ f R
  have hunbounded : ∃ R : ℝ, 0 < R ∧ c ≤ selfConsFunc R := by
    refine ⟨max c 1, lt_max_of_lt_left hc, ?_⟩
    have hR0 : (0:ℝ) ≤ max c 1 := le_max_of_le_left hc.le
    calc c ≤ max c 1 := le_max_left _ _
      _ ≤ selfConsFunc (max c 1) := selfConsFunc_ge_of_nonneg hR0
  obtain ⟨R, _hRpos, hRc⟩ := hunbounded
  -- IVT on [0, R]
  have h0 : selfConsFunc 0 = 0 := by simp [selfConsFunc]
  have h0c : selfConsFunc 0 ≤ c := by rw [h0]; exact hc.le
  have hivt := intermediate_value_Icc (by linarith : (0:ℝ) ≤ R) hcont.continuousOn
  obtain ⟨r, hricc, hfeq⟩ := hivt ⟨h0c, hRc⟩
  -- r > 0：f 0 = 0 ≠ c
  have hrpos : 0 < r := by
    rcases (lt_or_eq_of_le hricc.1) with h | h
    · exact h
    · exfalso
      rw [← h] at hfeq
      rw [h0] at hfeq
      linarith
  refine ⟨r, ⟨hricc.1, hfeq⟩, ?_⟩
  rintro r' ⟨hr'0, hr'eq⟩
  by_contra hne
  rcases lt_trichotomy r r' with h | h | h
  · have hs := selfConsFunc_strictMonoOn_Ici hricc.1 hr'0 h
    rw [hfeq, hr'eq] at hs; exact lt_irrefl _ hs
  · exact hne h.symm
  · have hs := selfConsFunc_strictMonoOn_Ici hr'0 hricc.1 h
    rw [hr'eq, hfeq] at hs; exact lt_irrefl _ hs

/-- The BCS self-consistent spectral gap dl_BCS = dl_min / r_self_consistent.
    r_self_consistent = 0.8740 from spectral flow closure.
    dl_BCS = 0.122 / 0.8740 ≈ 0.1396. -/
noncomputable def r_self_consistent : ℝ := (8740 : ℝ)/10000

noncomputable def dl_BCS_self_consistent : ℝ := dl_min / r_self_consistent

/-- The self-consistent spectral weave degree of freedom:
    d_BCS = √3·√r ≈ √3·0.935 = 1.619. -/
noncomputable def d_BCS_self_consistent : ℝ := d_BCS dl_BCS_self_consistent

/-
※ 开放项登记（2026-08-04 正本清源）：自洽 BCS 比值
    a_SC(dl_BCS_self_consistent, 1) ≈ 0.567 与标准 BCS 值 1/1.764 相符
    （偏差 < 0.1%，Python 验证 spectral_BCS_v2_comprehensive.py Q1 → a = 0.5669）。
    原 `theorem a_SC_self_consistent_matches_BCS ... := by sorry` 以精确等式陈述
    该近似，在 Lean 实数层不可证（涉及立方根方程与 Real.sqrt/Real.pi 数值计算）。
    此处不再以假定理形式保留。
-/

/-! =========================================================
    Section 4: Strong Coupling — Eliashberg Two-Step Scheme (§7.3)
   ========================================================= -/

/-- Wavefunction renormalization factor Z = 1 + λ from Eliashberg theory.
    This is the static limit Z(0) = 1 + λ of the Eliashberg self-energy.
    Reference: spectral_BCS_weave.md §7.3 Theorem 7.4. -/
noncomputable def Z_BCS (lam : ℝ) : ℝ := 1 + lam

/-- Geilikman-Kresin (GK) spectral gap ratio correction for strong coupling.
    r_strong = r_w · exp(-β · (T_c/ω_log)² · ln(ω_log/(2·T_c)))
    
    Reference: spectral_BCS_weave.md §7.3 Eq. (7.3). -/
noncomputable def r_strong (r_w β T_c ω_log : ℝ) : ℝ :=
  r_w * Real.exp (-β * (T_c / ω_log) ^ 2 * Real.log (ω_log / (2 * T_c)))

/-- Strong coupling BCS ratio from the two-step scheme.
    a_SC_two_step = ((1 + √3·√r_strong/(1+λ))/(4π) · r_strong)^{1/3}
    
    Reference: spectral_BCS_weave.md §7.3 Eq. (7.4). -/
noncomputable def a_SC_two_step (r_w β T_c ω_log lam : ℝ) : ℝ :=
  ((1 + Real.sqrt 3 * Real.sqrt (r_strong r_w β T_c ω_log) / Z_BCS lam) /
    (4 * Real.pi) * r_strong r_w β T_c ω_log)

/-- Strong coupling parameter structure for a specific material. -/
structure StrongCouplingParams where
  /-- Eliashberg coupling strength λ. -/
  lam : ℝ
  /-- Debye frequency ω_D (in K). -/
  ω_D : ℝ
  /-- Logarithmic average phonon frequency ω_log ≈ ω_D/1.2. -/
  ω_log : ℝ
  /-- Critical temperature T_c (in K). -/
  T_c : ℝ
  /-- Experimental a value a_exp = T_c/Δ_0. -/
  a_exp : ℝ
  /-- GK correction parameter β. -/
  β : ℝ
  /-- Weak-coupling spectral gap ratio r_w. -/
  r_w : ℝ

/-- Predefined material parameters for the five BCS superconductors
    used in the spectral framework validation.
    Reference: spectral_BCS_weave.md §7.4.1 Table. -/
noncomputable def Pb_params : StrongCouplingParams :=
  { lam := 1.55, ω_D := 105, ω_log := 105/1.2, T_c := 7.2, a_exp := 0.415,
    β := 15.2422, r_w := r_self_consistent }

noncomputable def Al_params : StrongCouplingParams :=
  { lam := 0.40, ω_D := 428, ω_log := 428/1.2, T_c := 1.2, a_exp := 0.576,
    β := 15.2422, r_w := r_self_consistent }

noncomputable def Sn_params : StrongCouplingParams :=
  { lam := 0.70, ω_D := 200, ω_log := 200/1.2, T_c := 3.7, a_exp := 0.542,
    β := 15.2422, r_w := r_self_consistent }

noncomputable def Nb_params : StrongCouplingParams :=
  { lam := 1.00, ω_D := 275, ω_log := 275/1.2, T_c := 9.3, a_exp := 0.519,
    β := 15.2422, r_w := r_self_consistent }

noncomputable def Hg_params : StrongCouplingParams :=
  { lam := 1.00, ω_D := 95, ω_log := 95/1.2, T_c := 4.2, a_exp := 0.438,
    β := 24.9, r_w := r_self_consistent }

/-
※ 开放项登记（2026-08-04 正本清源）：Pb 两步方案数值闭合
    a_SC_two_step(Pb_params) ≈ 0.4150，与实验值 a_exp = 0.415 相符（偏差 0.00%，
    Python 验证 eliashberg_spectral_solver.py §5）。该结果是近似数值恒等式
    （涉及 Real.exp、Real.log、Real.pi、Real.sqrt 的浮点计算），在 Lean 实数层
    不可精确证明。原 `theorem Pb_two_step_closure_matches_experiment ... := by sorry`
    以精确等式陈述，是伪陈述，此处不再保留。
-/

/-
※ 开放项登记（2026-08-04 正本清源）：Al 两步方案偏差
    a_SC_two_step(Al_params) ≈ 0.531 vs a_exp = 0.576（偏差 ≈ 7.86%，归因于
    Einstein 单峰简化 α²F(ω)）。原 `theorem Al_two_step_deviation_percent ... := by sorry`
    以精确等式 `7.86 = ...` 陈述舍入值，是伪陈述，此处不再保留。
    数值验证见 eliashberg_spectral_solver.py §5。
-/

/-! =========================================================
    Section 5: BCS Weave on the Product Base Temp × RG
   ========================================================= -/

/-- BCS spectral weave section on the product base Bun(Temp × RG, Spec).
    When restricted along ι_T (fixing μ), this gives the BCS Temp-section.
    When restricted along ι_μ (fixing T), this gives the BCS RG-section. -/
noncomputable def BCSWeaveSection (T : TempObj) (μ : RGObj) : SpectralBundleProd :=
  { base := { T := T, μ := μ }
    fiberData := { n := 2, A := cl17GapMatrix } }

/-- Theorem: The BCS weave section is a section of π_Tμ.
    π_Tμ(BCSWeaveSection T μ) = (T, μ). -/
theorem BCSWeaveSection_is_section (T : TempObj) (μ : RGObj) :
    π_Tμ.obj (BCSWeaveSection T μ) = { T := T, μ := μ } := rfl

/-- Theorem: The pullback of the BCS weave section along ι_T (fixing μ = μ₀)
    recovers the existing BCSSection_cl17 over Temp. -/
theorem BCSWeaveSection_pullback_ι_T (T : TempObj) (μ₀ : RGObj) :
    (pullback_ι_T μ₀).obj (BCSWeaveSection T μ₀) = BCSSection_cl17.obj T := by
  unfold BCSWeaveSection pullback_ι_T BCSSection_cl17 QCDSection_cl17
  simp

/-- Theorem: The pullback of the BCS weave section along ι_μ (fixing T = T₀)
    gives the RG analog of the BCS weave section.
    This corresponds to the HP section over RG when T₀ = 0 (critical limit). -/
theorem BCSWeaveSection_pullback_ι_μ (T₀ : TempObj) (μ : RGObj) :
    (pullback_ι_μ T₀).obj (BCSWeaveSection T₀ μ) =
      { base := μ, fiberData := { n := 2, A := cl17GapMatrix } } := by
  unfold BCSWeaveSection pullback_ι_μ
  simp

/-
The spectral weave equality along ∂Rec_D:
S_spec(Λ_QCD, 0) = S_spec(0, T_c).

※ 开放项登记（2026-08-04）：原 `weave_boundary_BCS_QCD` 声明
`(pullback_ι_μ T_c).obj ... = (pullback_ι_T Λ_QCD).obj ...` 类型不成立——
左侧是 SpectralBundleRG，右侧是 SpectralBundleTemp，不同范畴对象无法直接相等
（与 WeaveProductFiber 中同类问题一致）。边界识别需经 T_hat_Riem 桥接。
-/
-- theorem weave_boundary_BCS_QCD (T_c : TempObj) (Λ_QCD : RGObj) :
--     (pullback_ι_μ T_c).obj (BCSWeaveSection T_c Λ_QCD) =
--     (pullback_ι_T Λ_QCD).obj (BCSWeaveSection T_c Λ_QCD) := by
--   unfold BCSWeaveSection pullback_ι_μ pullback_ι_T
--   simp

/-! =========================================================
    Section 6: Spectral Gap Ratio Candidates for BCS (§5.2)
   ========================================================= -/

/-
Three candidates for dl_BCS from the Cl(1,7) spectral gap structure.
Reference: spectral_BCS_weave.md §5.2 Table.
-/

/-- Candidate (a): Pure U(1) spectral gap.
    dl_BCS = dl_1 = √(2/3)·dl_min ≈ 0.0996
    This gives a_SC ≈ 0.679 (19.7% deviation from 0.567). -/
noncomputable def candidate_a_dl_BCS : ℝ := dl_1

/-- Candidate (b): U(1) × SU(2) arithmetic mean.
    dl_BCS = (dl_1 + dl_3)/2 ≈ 0.136
    This gives a_SC ≈ 0.591 (4.2% deviation from 0.567). -/
noncomputable def candidate_b_dl_BCS : ℝ := (dl_1 + dl_3) / 2

/-- Candidate (c): Self-consistent solved value (back-matching a_BCS = 0.567).
    dl_BCS ≈ 0.1497
    This gives a_SC = 0.567 exactly (0% deviation). -/
noncomputable def candidate_c_dl_BCS : ℝ := 1497/10000

/-
※ 开放项登记（2026-08-04 正本清源）：最终自洽闭合 dl_BCS ≈ 0.1396（§5.5.4 定理 5.3，
    a_SC = 0.567，偏差 < 0.1%）。精确值 dl_BCS_self_consistent = dl_min/0.874
    = ((√6−√2)/√72)/0.874 ≈ 0.1396…，与舍入值 1396/10000 并非精确相等，
    故原 `theorem dl_BCS_self_consistent_value ... := by sorry` 是伪陈述，
    此处不再保留。数值验证见 spectral_BCS_v2_comprehensive.py Q1。
-/

/-! =========================================================
    Section 7: η_c vs a_BCS Consistency Check
   ========================================================= -/

/-
Theorem: The critical noise threshold η_c and the BCS ratio a_BCS
both derive from the same Cl(1,7) spectral gap structure.

※ 开放项登记（2026-08-04）：原 Section 7（`eta_c_and_a_BCS_share_spectral_gap_source`
与 `eta_c_over_a_BCS`）引用 `NoiseFiber.criticalNoiseEta_from_cl17`，但本文件
未 import NoiseFiber（NoiseFiber 依赖链独立）。为避免跨文件耦合与依赖阻塞，
此处登记开放项；η_c = 4·spectralGap 8 的陈述见 NoiseFiber.lean
（criticalEta_spectralGap_relation）。
-/
-- theorem eta_c_and_a_BCS_share_spectral_gap_source :
--     criticalNoiseEta_from_cl17.η = (4 : ℝ) * dl_min := by
--   calc
--     criticalNoiseEta_from_cl17.η = (4 : ℝ) * (spectralGap 8) := criticalEta_spectralGap_relation
--     _ = (4 : ℝ) * dl_min := by rfl

-- noncomputable def eta_c_over_a_BCS : ℝ :=
--   criticalNoiseEta_from_cl17.η / a_BCS

end MUFPF
