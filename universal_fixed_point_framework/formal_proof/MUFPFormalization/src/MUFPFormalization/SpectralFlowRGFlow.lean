-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
-- ============================================================

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic
import MUFPFormalization.SpectralFlowDynamicsRG

open Real

namespace MUFPF

/-!
# SpectralFlowRGFlow.lean — 谱流 RG 流单参数族（Paper LVII §8.7#5 动力学层第二注入）

§8.6d（`SpectralFlowRG.lean`）把自洽倍率钉在**单个物理点** c₀ = a_BCS³·4π 上：
k₁·k₂ = r*。§8.7#5 的"多级常演化"若要有连续意义，k₁·k₂ = r* 必须能沿
**整个谱流 RG 族**扫掠而不破坏——本文件把该折叠推广为**以闭合常数 c 为参数
的单参数流族**：

   c  ↦  ρ(c) := 自洽方程 f(r) = c 在 [0,∞) 的唯一正实根，
   f(r) = (1 + √3·√r)·r，ρ(c) = f⁻¹(c)。

对任意 c > 0，§8.6d 的折叠沿线成立：

   k₁·k₂(c) = √3 · (ρ(c)/√3) = ρ(c),

且电磁中间级锚 Δλ_min^(EM) = Δλ_min/√3 **不随流参数 c 演化**（纯规范普朗克锚，
所有 c 依赖全在 BCS 动力学因子 k₂(c)）。这就是"多级常演化"的流族读法：
**折叠结构不变量沿流保持，流动的全部自由度被唯一地装入动力学因子 k₂(c)**。

本文件同时把运行反常维度（`SpectralFlowDynamicsRG.lean` §1）沿流升级为单参数族
的**β 通量**直证：

   β(r) := 1/ζ(r) = (1+√3·√r)/(1 + (3/2)√3·√r) ∈ (2/3, 1),

即 d ln r / d ln c 的闭式。因 ρ(c) = f⁻¹(c)，β-形式 ODE

   d ln r / d ln c = 1/ζ(r)   (等价地 d ln c / d ln r = ζ(r))

的**积分解恰是流族自身**：轨迹为 f 的水平簇 c = f(r)，id `flow_closure`（f∘ρ = id）
与 `flow_inverse_point`（ρ∘f = id）把"ρ 是 f 的逆、水平簇即流轨迹"写为代数恒等式。
ζ(r) = r f'(r)/f(r) 是 a_BCS 相关项，闭式已由 `anom_dim` 给出。

诚实边界（动力学层第二注入，延续 §8.6d / §8.6f）：
- 本文件闭合的是**谱流方程的流族结构**：ρ(c) 的唯一性、沿 c 单调性、折叠不变性、
  β 通量的 (2/3,1) 有界性与运行指数沿流单调。β-形式 ODE 以**逆流代数形式**
  （水平簇即轨迹）闭合，未展开 d/dc 的柯西-Lipschitz 存在性细节。
- **仍开放**：EM 中间级由*自身独立*谱流方程涌现（而非经同一 c 的逆向重标度）；
  材料特定 δ_SC 需要把材料能量尺度落入谱流族（即用一个独立能量锚选定 c 截线）。
- a_BCS、E_F 仍是物理输入；范畴 Δ 内生的是 Δλ_min、Δλ_min^(EM)、ρ(c) 的方程唯一性。
-/

/-! ## Section 1: 谱流 RG 流单参数族 ρ(c) = f⁻¹(c) -/

/-- 谱流 RG 流族：对给定闭合常数 c > 0，ρ(c) 是 f(r)=c 在 [0,∞) 的唯一正实根。
    由 `WeaveBCS.selfConsFunc_existsUnique` 保证存在唯一。 -/
noncomputable def r_star_flow (c : ℝ) (hc : 0 < c) : ℝ :=
  Classical.choose (selfConsFunc_existsUnique c hc)

/-- 流族处满足自洽方程组：ρ(c) ≥ 0 且 f(ρ(c)) = c。 -/
theorem r_star_flow_spec (c : ℝ) (hc : 0 < c) :
    0 ≤ r_star_flow c hc ∧ selfConsFunc (r_star_flow c hc) = c :=
  (Classical.choose_spec (selfConsFunc_existsUnique c hc)).1

/-- **流闭合**：f(ρ(c)) = c（ρ 是 f 的右逆——f∘ρ = id）。 -/
theorem r_star_flow_closure (c : ℝ) (hc : 0 < c) :
    selfConsFunc (r_star_flow c hc) = c :=
  (r_star_flow_spec c hc).2

/-- 流族非负。 -/
theorem r_star_flow_nonneg (c : ℝ) (hc : 0 < c) : 0 ≤ r_star_flow c hc :=
  (r_star_flow_spec c hc).1

/-- 流族严格为正（f(0)=0 ≠ c>0，故正根非零）。 -/
theorem r_star_flow_pos (c : ℝ) (hc : 0 < c) : 0 < r_star_flow c hc := by
  rcases r_star_flow_spec c hc with ⟨hnn, hclose⟩
  rcases lt_or_eq_of_le hnn with h | h
  · exact h
  · exfalso
    have hz : r_star_flow c hc = 0 := h.symm
    have h0 : selfConsFunc (r_star_flow c hc) = 0 := by
      rw [hz]
      simp [selfConsFunc]
    have hc0 : c = 0 := hclose.symm.trans h0
    linarith [hc, hc0]

/-- **物理点锚定**：在 c₀ = a_BCS³·4π 处，流族 ρ(c₀) 恰为 §8.6b 的自洽根 r*。
    即 §8.6 的全部结果(δ_SC、ρ₀、T_c)都是流族 ρ(c) 在物理截线 c = c₀ 处的提取。 -/
theorem r_star_flow_at_physical : r_star_flow selfConsC selfConsC_pos = r_star := rfl

/-- **流单调性（沿 c 严格递增）**：正根 ρ(c) 随闭合常数 c 严格上升——
    因 f 在 [0,∞) 严格递增，f⁻¹ 亦然。这保证流族可被 c 单调参数化。 -/
theorem r_star_flow_lt {c₁ c₂ : ℝ} (h1 : 0 < c₁) (h2 : 0 < c₂) (hc : c₁ < c₂) :
    r_star_flow c₁ h1 < r_star_flow c₂ h2 := by
  have hspec1 := r_star_flow_spec c₁ h1
  have hspec2 := r_star_flow_spec c₂ h2
  by_contra h
  have hge : r_star_flow c₂ h2 ≤ r_star_flow c₁ h1 := not_lt.mp h
  rcases lt_or_eq_of_le hge with hlt | heq
  · have hs := selfConsFunc_strictMonoOn_Ici hspec2.1 hspec1.1 hlt
    rw [hspec2.2, hspec1.2] at hs
    linarith
  · rw [heq] at hspec2
    have heqcl : c₁ = c₂ := (hspec1.2).symm.trans hspec2.2
    linarith

/-- **逆流/积分解**：ρ(f(r)) = r（ρ 是 f 的左逆——ρ∘f = id）。
    对任意 r > 0，其为自洽根，故流族沿 f 的水平簇自成轨迹而"回射"到自身。
    这是 β-形式 ODE 的水平簇积分表述（轨迹即 c = f(r)）。 -/
theorem flow_inverse_point {r : ℝ} (hr : 0 < r) :
    r_star_flow (selfConsFunc r) (selfConsFunc_pos hr) = r := by
  have huniq : ∀ y : ℝ, (0 ≤ y ∧ selfConsFunc y = selfConsFunc r) →
      y = r_star_flow (selfConsFunc r) (selfConsFunc_pos hr) :=
    (Classical.choose_spec (selfConsFunc_existsUnique (selfConsFunc r) (selfConsFunc_pos hr))).2
  exact (huniq r ⟨hr.le, rfl⟩).symm

/-! ## Section 2: 流不变折叠 / EM 锚定 -/

/-- 辅助恒等式：√3 · √(1/3) = 1。 -/
private theorem sqrt3_mul_sqrt13_flow : Real.sqrt 3 * Real.sqrt (1 / 3 : ℝ) = 1 := by
  have h13 : Real.sqrt (1 / 3 : ℝ) = (Real.sqrt 3)⁻¹ := by
    rw [show (1 / 3 : ℝ) = (3 : ℝ)⁻¹ by norm_num, Real.sqrt_inv]
  rw [h13]
  field_simp [ne_of_gt (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3))]

/-- 流族第 1 级倍率：k₁ = √3 **恒定**（纯规范表示因子，SU(2) Casimir 锚，不随 c 演化）。 -/
theorem flow_k1_constant : RG_k1 = Real.sqrt 3 := RG_k1_eq_sqrt3

/-- 流族动力学因子：k₂(c) := Δλ_min^(EM)/δ_SC(c) = ρ(c)/√3。
    所有 c 依赖集中于此（BCS 谱流动力学因子）；c ↗ 时 k₂(c) 严格上升。 -/
noncomputable def flow_k2 (c : ℝ) (hc : 0 < c) : ℝ :=
  Real.sqrt (1 / 3 : ℝ) * r_star_flow c hc

/-- 流族动力因子严格为正：k₂(c) > 0。 -/
theorem flow_k2_pos (c : ℝ) (hc : 0 < c) : 0 < flow_k2 c hc := by
  unfold flow_k2
  exact mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3)) (r_star_flow_pos c hc)

/-- 动力学因子沿流单调：k₂(c₁) < k₂(c₂)（c₁ < c₂）。 -/
theorem flow_k2_lt {c₁ c₂ : ℝ} (h1 : 0 < c₁) (h2 : 0 < c₂) (hc : c₁ < c₂) :
    flow_k2 c₁ h1 < flow_k2 c₂ h2 := by
  unfold flow_k2
  exact mul_lt_mul_of_pos_left (r_star_flow_lt h1 h2 hc)
    (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3))

/-- **流折叠（沿线折叠不变式）**：k₁·k₂(c) = ρ(c)。
    §8.6d 的 `RG_telescoping` 从单物理点推广到整条流族——折叠结构不变量沿线保持。 -/
theorem flow_telescoping (c : ℝ) (hc : 0 < c) : RG_k1 * flow_k2 c hc = r_star_flow c hc := by
  unfold flow_k2
  rw [flow_k1_constant, ← mul_assoc, sqrt3_mul_sqrt13_flow]
  ring

/-- **EM 中间级锚定（流不变性）**：Δλ_min^(EM) = Δλ_min/√3 是 c-无关常量——
    普朗克规范谱间隙的普适锚点，不参与流动。所有 c 依赖被唯一地装入 k₂(c)。 -/
theorem flow_em_anchor_constant : dl_min_EM = Real.sqrt (1 / 3 : ℝ) * dl_min := by
  unfold dl_min_EM dl_1
  rfl

/-- **锚定-动力学正交分解**：δ_SC 的 c-依赖因子即流族 spec 比 ρ(c)，严格递增；
    而普朗克锚与规范因子 k₁ 完全不依赖 c。这是"多级常演化"的结构正交性。 -/
theorem flow_anchor_orthogonal (c : ℝ) (hc : 0 < c) :
    Real.sqrt 3 * flow_k2 c hc = r_star_flow c hc := by
  rw [← flow_k1_constant]
  exact flow_telescoping c hc

/-- 物理截线细化：流族动力因子在 c₀ 处回归 §8.6d 的 k₂——k₂(c₀) = RG_k2。 -/
theorem flow_k2_at_physical : flow_k2 selfConsC selfConsC_pos = RG_k2 := by
  unfold flow_k2
  simp [r_star_flow_at_physical, RG_k2_eq]

/-! ## Section 3: β 通量（运行指数之逆）与沿流单调 -/

/-- **β 通量**：β(r) := 1/ζ(r) = (1+√3·√r)/(1 + (3/2)√3·√r) ∈ (2/3, 1)。
    即 d ln r / d ln c 沿谱流族的闭式（ζ = d ln c / d ln r 为运行反常维度）。 -/
noncomputable def rg_beta (r : ℝ) : ℝ := 1 / anom_dim r

/-- 运行反常维度 ζ(r) > 0（β 可逆性）。 -/
theorem anom_dim_pos {r : ℝ} (hr : 0 < r) : 0 < anom_dim r := by
  have h := anom_dim_gt_one hr
  linarith

/-- **β 下界**：β(r) > 2/3（因 ζ < 3/2）。 -/
theorem rg_beta_gt_two_thirds {r : ℝ} (hr : 0 < r) : (2 : ℝ) / 3 < rg_beta r := by
  unfold rg_beta
  have hd : 0 < anom_dim r := anom_dim_pos hr
  rw [lt_div_iff₀ hd]
  nlinarith [anom_dim_lt_threehalf hr]

/-- **β 上界**：β(r) < 1（因 ζ > 1）。 -/
theorem rg_beta_lt_one {r : ℝ} (hr : 0 < r) : rg_beta r < 1 := by
  unfold rg_beta
  have hd : 0 < anom_dim r := anom_dim_pos hr
  rw [div_lt_iff₀ hd]
  nlinarith [anom_dim_gt_one hr]

/-- **β 有界（分量式）**：β(r) ∈ (2/3, 1)（谱流族处处良定义、非标度不变的有界通量）。 -/
theorem rg_beta_interior {r : ℝ} (hr : 0 < r) :
    (2 : ℝ) / 3 < rg_beta r ∧ rg_beta r < 1 :=
  ⟨rg_beta_gt_two_thirds hr, rg_beta_lt_one hr⟩

/-- **运行反常维度沿 r 严格递增**：ζ(r₁) < ζ(r₂)（r₁ < r₂，r 正）。
    几何事实：谱流方程随 r 越大越偏离标度不变（ζ ↗ 3/2）。 -/
theorem anom_dim_strictMono {r₁ r₂ : ℝ} (h1 : 0 < r₁) (h2 : 0 < r₂) (hr : r₁ < r₂) :
    anom_dim r₁ < anom_dim r₂ := by
  unfold anom_dim
  have hs1 : 0 < Real.sqrt r₁ := Real.sqrt_pos_of_pos h1
  have hs2 : 0 < Real.sqrt r₂ := Real.sqrt_pos_of_pos h2
  have hsq : Real.sqrt r₁ < Real.sqrt r₂ := by
    have hrsq1 : (Real.sqrt r₁) ^ 2 = r₁ := Real.sq_sqrt h1.le
    have hrsq2 : (Real.sqrt r₂) ^ 2 = r₂ := Real.sq_sqrt h2.le
    by_contra h'
    have hle : Real.sqrt r₂ ≤ Real.sqrt r₁ := not_lt.mp h'
    have hrsq_le : (Real.sqrt r₂) ^ 2 ≤ (Real.sqrt r₁) ^ 2 :=
      pow_le_pow_left₀ (Real.sqrt_nonneg r₂) hle 2
    have : r₂ ≤ r₁ := by
      rw [← hrsq2, ← hrsq1]
      exact hrsq_le
    linarith [hr, this]
  have hx1 : 0 < Real.sqrt 3 * Real.sqrt r₁ :=
    mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3)) hs1
  have hx2 : 0 < Real.sqrt 3 * Real.sqrt r₂ :=
    mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3)) hs2
  have hxlt : Real.sqrt 3 * Real.sqrt r₁ < Real.sqrt 3 * Real.sqrt r₂ :=
    mul_lt_mul_of_pos_left hsq (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3))
  have hd1 : 0 < 1 + Real.sqrt 3 * Real.sqrt r₁ := by linarith [hx1]
  have hd2 : 0 < 1 + Real.sqrt 3 * Real.sqrt r₂ := by linarith [hx2]
  rw [div_lt_div_iff₀ hd1 hd2]
  nlinarith [hxlt]

/-- **运行指数沿流单调**：c ↗ 时 ρ(c) ↗（`r_star_flow_lt`），且 ζ 在 ρ 上严格增——
    故沿流族运行反常维度 ζ(ρ(c)) 严格上升：偏离标度不变性随 c 单调放大。 -/
theorem flow_anom_dim_lt {c₁ c₂ : ℝ} (h1 : 0 < c₁) (h2 : 0 < c₂) (hc : c₁ < c₂) :
    anom_dim (r_star_flow c₁ h1) < anom_dim (r_star_flow c₂ h2) :=
  anom_dim_strictMono (r_star_flow_pos c₁ h1) (r_star_flow_pos c₂ h2) (r_star_flow_lt h1 h2 hc)

/-- **β 通量沿流有界**：在流族任意点，β(ρ(c)) ∈ (2/3, 1)。 -/
theorem flow_rg_beta_interior (c : ℝ) (hc : 0 < c) :
    (2 : ℝ) / 3 < rg_beta (r_star_flow c hc) ∧ rg_beta (r_star_flow c hc) < 1 :=
  rg_beta_interior (r_star_flow_pos c hc)

/-- **β 通量沿流单调**：c ↗ 时 ρ ↗、ζ ↗，故 β = 1/ζ 严格递减。
    这量化"谱流方程越强耦合越偏离标度不变"的流族（ζ 从 1 跑向 3/2，β 从 1 跑向 2/3）。 -/
theorem flow_rg_beta_gt {c₁ c₂ : ℝ} (h1 : 0 < c₁) (h2 : 0 < c₂) (hc : c₁ < c₂) :
    rg_beta (r_star_flow c₁ h1) > rg_beta (r_star_flow c₂ h2) := by
  unfold rg_beta
  have hz1 : 0 < anom_dim (r_star_flow c₁ h1) := anom_dim_pos (r_star_flow_pos c₁ h1)
  have hz2 : 0 < anom_dim (r_star_flow c₂ h2) := anom_dim_pos (r_star_flow_pos c₂ h2)
  have hζlt : anom_dim (r_star_flow c₁ h1) < anom_dim (r_star_flow c₂ h2) :=
    flow_anom_dim_lt h1 h2 hc
  -- 1/ζ₂ < 1/ζ₁ ⟺ ζ₁ < ζ₂（ζ 均正）
  have h : 1 / anom_dim (r_star_flow c₂ h2) < 1 / anom_dim (r_star_flow c₁ h1) := by
    rw [div_lt_div_iff₀ hz2 hz1]
    nlinarith [hζlt]
  exact h

end MUFPF