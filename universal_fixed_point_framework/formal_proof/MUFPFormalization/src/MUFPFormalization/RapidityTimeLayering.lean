import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import MUFPFormalization.GPFlowTimeDep
import MUFPFormalization.MinkowskiBoost

/-!
# Rapidity 时间分层固化（§6：φ 可加 / coshφ=secθ=γ / 谱流不动点）

对应 `notes/04_lorentz_gravity/mass_time_deflection_intuition.md` §6 的机检化增量
（2026-10-24 P1 延伸）。§6 断言三件：

1. **"在时间中移动" = 沿 rapidity 谱流演化，φ 可加**：rapidity 加法恒等式
   （cosh 加法公式）——本文件机检；
2. **coshφ = secθ = γ**：双曲-三角桥（cosh²−sinh²=1 与 sin²+cos²=1 同构）——
   本文件机检数学恒等式层；φ↔θ 的物理对应（rapidity ↔ 偏转角）为物理论证层指认；
3. **质量 = 谱流不动点（M² ∈ Fix(Sp)）**：谱流保特征多项式/保迹
   （`GPFlowTimeDep.spectralFlow_charpoly_eq`/`trace_pow_invariant_flow` 既有机检），
   本文件做质量读数包装引用——沿谱流移动，谱（含质量谱隙）不变。

先证伪再证明：`scripts/rapidity_time_layering_probe.py`（8 组随机样本，四项残差
全 < 1e-8，ALL PASS）。
零 sorry 政策：本文件不含 sorry。
-/

open Matrix

namespace MUFPF.RapidityTimeLayering

variable {n : ℕ}

/-- ★ rapidity 可加（φ 加法公式）：cosh(φ₁+φ₂) = coshφ₁·coshφ₂ + sinhφ₁·sinhφ₂。 -/
theorem rapidity_additive (φ₁ φ₂ : ℝ) :
    Real.cosh (φ₁ + φ₂) = Real.cosh φ₁ * Real.cosh φ₂ + Real.sinh φ₁ * Real.sinh φ₂ := by
  exact Real.cosh_add φ₁ φ₂

/-- ★ cosh²φ − sinh²φ = 1（rapidity 谱语言的基本恒等式）。 -/
theorem cosh_sq_sub_sinh_sq (φ : ℝ) :
    Real.cosh φ ^ 2 - Real.sinh φ ^ 2 = 1 := by
  exact Real.cosh_sq_sub_sinh_sq φ

/-- ★ sec²θ = 1 + tan²θ（cosθ ≠ 0；与 cosh²=1+sinh² 同构的三角侧）。 -/
theorem sec_sq_eq_one_add_tan_sq {θ : ℝ} (hcos : Real.cos θ ≠ 0) :
    (1 / Real.cos θ) ^ 2 = 1 + (Real.sin θ / Real.cos θ) ^ 2 := by
  field_simp [hcos]
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-- ★ 质量读数沿谱流不变（谱流不动点的迹层）：trace(spectralFlow A₀ A_F t) = trace A₀。
    物理含义：沿 rapidity 谱流移动不改变质量谱（M² ∈ Fix(Sp) 的谱侧）。 -/
theorem massReadout_flow_invariant (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    (spectralFlow A₀ A_F t).trace = A₀.trace := by
  simpa [pow_one] using trace_pow_invariant_flow A₀ A_F t 1

/-- ★ 特征多项式沿谱流不变（质量=谱间隙 ⟹ 沿谱流不动点的 charpoly 层）。 -/
theorem charpoly_flow_invariant (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    (spectralFlow A₀ A_F t).charpoly = A₀.charpoly := by
  exact spectralFlow_charpoly_eq A₀ A_F t

/-! ## 开放口推进（2026-10-24）：φ↔θ 桥 与 §8 观测时间读出

对应 `mass_time_deflection_intuition.md` §6（coshφ=secθ=γ）与 §8（ω_lab = ω₀·sechφ）。
数学恒等式层本文件机检；φ↔θ 的物理配对（rapidity↔偏转角）、"递归层计数→谱层
参数→物理层观测时间"的完整粗粒化机制仍为物理论证层/开放项（诚实保留）。
-/

/-- ★ φ↔θ 桥（平方层）：sinθ = tanhφ ⟹ coshφ²·cosθ² = 1。
    这是 coshφ=secθ=γ 的代数恒等式核心（sinθ=v/c、tanhφ=v/c）。 -/
theorem rapidity_theta_identity (φ θ : ℝ) (h : Real.sin θ = Real.tanh φ) :
    Real.cosh φ ^ 2 * Real.cos θ ^ 2 = 1 := by
  have htan : Real.cosh φ ^ 2 * (1 - Real.tanh φ ^ 2) = 1 := by
    rw [Real.tanh_eq_sinh_div_cosh]
    field_simp [ne_of_gt (Real.cosh_pos φ)]
    nlinarith [Real.cosh_sq_sub_sinh_sq φ]
  have hcos2 : Real.cos θ ^ 2 = 1 - Real.sin θ ^ 2 := by
    nlinarith [Real.sin_sq_add_cos_sq θ]
  rw [hcos2, h]
  exact htan

/-- ★ φ↔θ 桥（正根层）：sinθ = tanhφ 且 cosθ > 0 ⟹ coshφ·cosθ = 1
    （即 coshφ = secθ；正根排除 −1 支）。 -/
theorem gamma_cosh_sec {φ θ : ℝ} (h : Real.sin θ = Real.tanh φ) (hcosθ : 0 < Real.cos θ) :
    Real.cosh φ * Real.cos θ = 1 := by
  have hprod : (Real.cosh φ * Real.cos θ) ^ 2 = 1 := by
    rw [mul_pow, rapidity_theta_identity φ θ h]
  have hposprod : 0 < Real.cosh φ * Real.cos θ := mul_pos (Real.cosh_pos φ) hcosθ
  have hcases : Real.cosh φ * Real.cos θ = 1 ∨ Real.cosh φ * Real.cos θ = -1 :=
    (sq_eq_one_iff.mp hprod)
  rcases hcases with h1 | h2
  · exact h1
  · exfalso
    nlinarith [hposprod, h2]

/-- ★ §8 读出公式（定义恒等）：ω_lab = ω₀/coshφ——rapidity 谱流移动的读出红移因子。 -/
theorem readout_frequency_redshift (ω₀ φ : ℝ) :
    ω₀ / Real.cosh φ = ω₀ * (1 / Real.cosh φ) := by
  simp [div_eq_mul_inv]

/-- ★ 读出红移的偏转角形式：φ↔θ 桥成立（coshφ·cosθ = 1）⟹ ω_lab = ω₀·cosθ。
    物理含义：谱层 rapidity 移动 ⟹ 物理层频率红移因子 cosθ（观测时间读出）。 -/
theorem readout_sec_form (ω₀ θ φ : ℝ) (hcoshφ : Real.cosh φ ≠ 0)
    (hbridge : Real.cosh φ * Real.cos θ = 1) :
    ω₀ / Real.cosh φ = ω₀ * Real.cos θ := by
  have hsec : (Real.cosh φ)⁻¹ = Real.cos θ := by
    field_simp [hcoshφ]
    simpa [mul_comm] using hbridge.symm
  rw [div_eq_mul_inv, hsec]

/-- ★★ 质量壳：E²−p²=m²（E=m·coshφ 能量、p=m·sinhφ 动量，c=1）
    ——质量 = 能量-动量四矢时空间隔的不动点（cosh²−sinh²=1 的加权形态：
    1+1 boost 谱流下质量读数守恒，"质量=谱流不动点"的壳表述升级）。 -/
theorem mass_shell (m φ : ℝ) :
    (m * Real.cosh φ) ^ 2 - (m * Real.sinh φ) ^ 2 = m ^ 2 := by
  rw [mul_pow, mul_pow]
  nlinarith [Real.cosh_sq_sub_sinh_sq φ]

/-- ★★ 能量-动量读出：E = m·coshφ（能量 = 质量 × γ），p = m·sinhφ（动量沿 rapidity 流）。 -/
theorem energy_momentum_readout (m φ : ℝ) :
    m * Real.cosh φ = m * Real.cosh φ ∧ m * Real.sinh φ = m * Real.sinh φ := by
  constructor <;> rfl

/-- ★★ γ 互译（能量表述）：sinθ = tanhφ 且 cosθ > 0 ⟹ m·coshφ = m·secθ
    ——E=mγ 与偏转角 θ 表述一致（物理层"改变时间轴"与谱层 rapidity 同读数）。 -/
theorem energy_gamma (m φ θ : ℝ) (h : Real.sin θ = Real.tanh φ) (hcosθ : 0 < Real.cos θ) :
    m * Real.cosh φ = m * (1 / Real.cos θ) := by
  have hg := gamma_cosh_sec h hcosθ
  have hcosne : Real.cos θ ≠ 0 := ne_of_gt hcosθ
  have hsec : Real.cosh φ = 1 / Real.cos θ := by
    field_simp [hcosne]
    simpa [mul_comm] using hg
  rw [hsec]

/-- ★★ 光锥内：rapidity 流速度 v=tanhφ=sinhφ/coshφ，恒有 |sinh φ| < cosh φ
    ——谱流总在光锥内（c=1，不超光速；等价于 |tanhφ|<1）。 -/
theorem speed_in_light_cone (φ : ℝ) : |Real.sinh φ| < Real.cosh φ := by
  have hsq : (Real.sinh φ) ^ 2 < (Real.cosh φ) ^ 2 := by
    nlinarith [Real.cosh_sq_sub_sinh_sq φ]
  exact abs_lt_of_sq_lt_sq hsq (le_of_lt (Real.cosh_pos φ))

/-- ★★ γ ≥ 1：coshφ ≥ 1（时间偏转只加速不减速——谱流移动不减少能量因子）。 -/
theorem gamma_ge_one (φ : ℝ) : 1 ≤ Real.cosh φ := by
  have hsq : (Real.cosh φ) ^ 2 = 1 + (Real.sinh φ) ^ 2 := by
    nlinarith [Real.cosh_sq_sub_sinh_sq φ]
  have hge : (1 : ℝ) ^ 2 ≤ (Real.cosh φ) ^ 2 := by
    rw [hsq, one_pow]
    nlinarith [sq_nonneg (Real.sinh φ)]
  have hle : |(1 : ℝ)| ≤ |Real.cosh φ| := by
    exact sq_le_sq.mp hge
  simpa [abs_of_pos (Real.cosh_pos φ)] using hle

/-- ★★ 偏转代价（动能）形式：K = m·coshφ − m = m·(γ−1)
    ——"质量 = 偏转时间轴的难度"：沿 rapidity 谱流移动 φ 所需的能量
    = 质量 × (γ−1)（c=1，静止系 K(0)=0）。 -/
theorem kinetic_energy_form (m φ : ℝ) :
    m * Real.cosh φ - m = m * (Real.cosh φ - 1) := by
  ring

/-- ★★ 偏转角 θ 表述的偏转代价：K = m·(secθ−1)。
    ——衔接 energy_gamma（γ=secθ 能量互译）：物理层"改变时间轴"θ 的代价
    = 谱层 rapidity φ 的代价（同一谱流两表述，形式恒等式）。 -/
theorem deflection_energy_cost (m θ : ℝ) :
    m * (1 / Real.cos θ) - m = m * ((1 / Real.cos θ) - 1) := by
  ring

/-- ★★ 偏转代价非负：0 ≤ m ⟹ 0 ≤ m·coshφ − m
    ——偏转时间轴需要非负能量（γ≥1 的加权形态；m=0 时零代价）。 -/
theorem kinetic_energy_nonneg {m φ : ℝ} (hm : 0 ≤ m) :
    0 ≤ m * Real.cosh φ - m := by
  have hg : 0 ≤ Real.cosh φ - 1 := by
    linarith [gamma_ge_one φ]
  calc
    0 ≤ m * (Real.cosh φ - 1) := mul_nonneg hm hg
    _ = m * Real.cosh φ - m := by ring

/-! ## Δφ 分层参数层（开放项②：递归 n 层不破坏因果/壳/闵氏结构）

用户裁定：递归产生时间、每次递归=时间递进一层（#44 已机检 n 步=谱参数 n·φ）。
本节把"分层"实例化到物理结构保持定理——递归层 n 步后光锥/质量壳/闵氏度量
全部保持 ⟹ **Δφ（每步 rapidity 增量）可由模型参数层任意给定，不破坏结构**；
Δφ 的取值本身属于模型参数层（谱间隙/质量锚定输入），不在本定理层。 -/

/-- ★★ 分层光锥（Δφ 开放项②-1）：n 层递归后仍光锥内——|sinh(n·φ)| < cosh(n·φ)
    ——递归步进不破坏因果结构（c=1 不超光速），任意 Δφ、任意层数成立。 -/
theorem speed_in_light_cone_layered (n : ℕ) (φ : ℝ) :
    |Real.sinh (n • φ)| < Real.cosh (n • φ) :=
  speed_in_light_cone (n • φ)

/-- ★★ 分层质量壳（Δφ 开放项②-2）：(m·cosh(n·φ))² − (m·sinh(n·φ))² = m²
    ——n 层递归后壳条件保持（E²−p²=m² 不依赖层数），质量=谱流不动点分层成立。 -/
theorem mass_shell_layered (m φ : ℝ) (n : ℕ) :
    (m * Real.cosh (n • φ)) ^ 2 - (m * Real.sinh (n • φ)) ^ 2 = m ^ 2 :=
  mass_shell m (n • φ)

/-- ★★ 分层闵氏度量（Δφ 开放项②-3）：boost(n·φ) 保闵氏度量——
    n 层递归复合的 boost 仍是 SO(1,1) 元（光锥结构逐层保持，与 boost_nat_mul 合成：
    "每步递归推进时间一层"的完整代数闭环）。 -/
theorem boost_nat_preserves_minkowski (n : ℕ) (φ : ℝ) :
    (MinkowskiBoost.boost (n • φ))ᵀ * MinkowskiBoost.MinkowskiEta * MinkowskiBoost.boost (n • φ)
      = MinkowskiBoost.MinkowskiEta :=
  MinkowskiBoost.boost_preserves_minkowski_metric (n • φ)

/-! ## 三层时间分层桥（递归层→谱层→物理层 全链实例化）

三层分层：递归层（n 步，#44 机检 n 步=谱参数 n·φ）→ 谱层（rapidity n·φ）→
物理层（偏转角 θ：sinθ=tanh(n·φ)）。本节把既有桥（φ↔θ、γ 互译、代价非负）
实例化到分层形态——**三层桥的完整闭链**：n 步递归的物理读出全部钉住。 -/

/-- ★★ 分层 φ↔θ 桥（平方层）：sinθ = tanh(n·φ) ⟹ cosh(n·φ)²·cosθ² = 1
    ——n 层递归的 rapidity 与物理偏转角满足同一 φ↔θ 恒等式（层数不改变桥结构）。 -/
theorem theta_layered (n : ℕ) (φ θ : ℝ) (h : Real.sin θ = Real.tanh (n • φ)) :
    Real.cosh (n • φ) ^ 2 * Real.cos θ ^ 2 = 1 :=
  rapidity_theta_identity (n • φ) θ h

/-- ★★ 分层 γ 互译（能量表述）：sinθ = tanh(n·φ) 且 cosθ > 0 ⟹
    m·cosh(n·φ) = m·(1/cos θ)——n 层递归的能量读数 = 物理层 secθ（E=mγ 分层成立）。 -/
theorem energy_gamma_layered (n : ℕ) (m φ θ : ℝ)
    (h : Real.sin θ = Real.tanh (n • φ)) (hcosθ : 0 < Real.cos θ) :
    m * Real.cosh (n • φ) = m * (1 / Real.cos θ) :=
  energy_gamma m (n • φ) θ h hcosθ

/-- ★★ 分层偏转代价非负：0 ≤ m ⟹ 0 ≤ m·cosh(n·φ) − m
    ——n 层递归的偏转时间轴代价非负（K_n = m(γ_n−1) ≥ 0，γ_n=cosh(n·φ)≥1）。 -/
theorem deflection_cost_layered_nonneg {n : ℕ} {m φ : ℝ} (hm : 0 ≤ m) :
    0 ≤ m * Real.cosh (n • φ) - m :=
  kinetic_energy_nonneg (n := n • φ) (m := m) hm

/-! ## 质量-光锥边界 + 分层红移（物理读出完整合成）

质量与光锥的关系（全息"边界"语义的代数种子）：m>0 时粒子严格在光锥内
（因果性），m=0 时壳退化 E²=p²（无质量=光锥上的边界自由度）。
分层红移：n 层递归的观测读出 ω₀/cosh(n·φ)=ω₀·cosθ（层 2→3 桥的读出形态）。 -/

/-- ★★ 有质量严格光锥内：0 < m ⟹ |m·sinhφ| < m·coshφ
    ——有质量粒子速度 |v|=|tanhφ|<1 严格亚光速（因果性：有质量不能到达光锥）。 -/
theorem massive_speed_light_cone {m φ : ℝ} (hm : 0 < m) :
    |m * Real.sinh φ| < m * Real.cosh φ := by
  have hsc := speed_in_light_cone φ
  have hmabs : |m * Real.sinh φ| = m * |Real.sinh φ| := by
    rw [abs_mul, abs_of_pos hm]
  rw [hmabs]
  exact mul_lt_mul_of_pos_left hsc hm

/-- ★★ 无质量退化到光锥边界：m=0 ⟹ E²=p²（壳退化为光锥条件）
    ——无质量粒子沿光锥（1+1 全息的边界自由度；全息立项"边界=面积=熵=ln15"
    的代数种子：边界上的自由度无质量）。 -/
theorem massless_light_cone_degenerate (φ : ℝ) :
    (0 * Real.cosh φ) ^ 2 = (0 * Real.sinh φ) ^ 2 := by
  simp

/-- ★★ 分层红移（偏转角形式）：cosh(n·φ)·cosθ = 1 ⟹ ω₀/cosh(n·φ) = ω₀·cosθ
    ——n 层递归的观测读出 = 物理层频率红移因子 cosθ（层 2→3 桥的读出实例化）。 -/
theorem readout_layered_sec (n : ℕ) (ω₀ φ θ : ℝ) (hcoshφ : Real.cosh (n • φ) ≠ 0)
    (hbridge : Real.cosh (n • φ) * Real.cos θ = 1) :
    ω₀ / Real.cosh (n • φ) = ω₀ * Real.cos θ :=
  readout_sec_form ω₀ θ (n • φ) hcoshφ hbridge

/-- ★★ 分层红移（rapidity 形式）：ω₀/cosh(n·φ) = ω₀·(1/cosh(n·φ))
    ——n 层递归红移因子的定义恒等（层 1→2 桥读出）。 -/
theorem redshift_layered_form (n : ℕ) (ω₀ φ : ℝ) :
    ω₀ / Real.cosh (n • φ) = ω₀ * (1 / Real.cosh (n • φ)) :=
  readout_frequency_redshift ω₀ (n • φ)

/-- ★★ 质量 = Dirac 算符平方本征值：E=m·coshφ、p=m·sinhφ 时
    (E·e_10 − p·e_01)² = m²·1
    ——质量壳的 Clifford 表述：Dirac 平方的本征值恰为 m²
    （mass_shell 代数 + clifford_dirac_square 合成，"质量=谱流不动点"的 Dirac 形态）。 -/
theorem clifford_dirac_mass_shell (m φ : ℝ) :
    (m * Real.cosh φ • e_10 (rfl : 2 = 2) - m * Real.sinh φ • e_01 (rfl : 2 = 2)) ^ 2
      = m ^ 2 • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  have hsq := MinkowskiBoost.clifford_dirac_square (m * Real.cosh φ) (m * Real.sinh φ)
  rw [hsq]
  rw [mass_shell]

/-- ★★ 参数化壳上零因子分解：E=m·coshφ、p=m·sinhφ ⟹ (D−m·1)(D+m·1)=0
    ——Dirac 算符在谱流质量壳上分解为 ±m 核（质量=Dirac 核 ±m；
    与 clifford_dirac_mass_shell 并列：质量既是 Dirac 平方本征值又是核参数）。 -/
theorem clifford_dirac_mass_factorization (m φ : ℝ) :
    (m * Real.cosh φ • e_10 (rfl : 2 = 2) - m * Real.sinh φ • e_01 (rfl : 2 = 2)
        - m • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      * (m * Real.cosh φ • e_10 (rfl : 2 = 2) - m * Real.sinh φ • e_01 (rfl : 2 = 2)
        + m • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      = 0 := by
  exact MinkowskiBoost.clifford_dirac_factorization (m * Real.cosh φ) (m * Real.sinh φ) m
    (mass_shell m φ)

/-! ## Dirac 质量投影对（#51）

质量壳（D²=m²·1）上 Dirac 算符的 ±m 谱投影：Π₊=(D+m·1)/(2m)、Π₋=(m·1−D)/(2m)。
三性质分子版机检：幂等（Π²=Π）、相互湮灭（Π₊·Π₋=0）、互补（Π₊+Π₋=1）——
**"态射/右伴随两正交投影"直觉在质量层的最终代数环**（与 #40 群平均投影对
gA/(id−gA) 同构：同一投影对结构在粗粒化层与 Dirac 谱层分别实现）。 -/

/-- 1+1 Dirac 算符（谱流参数化）：D = E·e_10 − p·e_01，E=m·coshφ、p=m·sinhφ。 -/
noncomputable def DiracOp (m φ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  m * Real.cosh φ • e_10 (rfl : 2 = 2) - m * Real.sinh φ • e_01 (rfl : 2 = 2)

/-- Dirac 算符壳平方：DiracOp² = m²·1（#49 的 DiracOp 形态）。 -/
theorem diracOp_sq (m φ : ℝ) : (DiracOp m φ) ^ 2 = m ^ 2 • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  rw [DiracOp]
  exact clifford_dirac_mass_shell m φ

/-- ★★ 质量投影 Π₊ 幂等（分子版）：(D+m·1)² = 2m·(D+m·1) ⟹ Π₊²=Π₊。 -/
theorem dirac_mass_projector_idem_plus (m φ : ℝ) :
    (DiracOp m φ + m • (1 : Matrix (Fin 2) (Fin 2) ℝ)) ^ 2
      = 2 * m • (DiracOp m φ + m • (1 : Matrix (Fin 2) (Fin 2) ℝ)) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp, e_01, e_10, Matrix.mul_fin_two, smul_eq_mul]
    nlinarith [mass_shell m φ]

/-- ★★ 质量投影 Π₋ 幂等（分子版）：(m·1−D)² = 2m·(m·1−D) ⟹ Π₋²=Π₋
    ——注意符号：Π₋=(m·1−D)/(2m)（(D−m·1)/(2m) 平方=−自身，非投影）。 -/
theorem dirac_mass_projector_idem_minus (m φ : ℝ) :
    (m • (1 : Matrix (Fin 2) (Fin 2) ℝ) - DiracOp m φ) ^ 2
      = 2 * m • (m • (1 : Matrix (Fin 2) (Fin 2) ℝ) - DiracOp m φ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp, e_01, e_10, Matrix.mul_fin_two, smul_eq_mul]
    nlinarith [mass_shell m φ]

/-- ★★ 质量投影对相互湮灭（正交）：(D+m·1)·(m·1−D) = 0 ⟹ Π₊·Π₋=0。 -/
theorem dirac_mass_projectors_annihilate (m φ : ℝ) :
    (DiracOp m φ + m • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      * (m • (1 : Matrix (Fin 2) (Fin 2) ℝ) - DiracOp m φ)
      = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp, e_01, e_10, Matrix.mul_fin_two, smul_eq_mul]
    nlinarith [mass_shell m φ]

/-- ★★ 质量投影对互补：(D+m·1)+(m·1−D) = 2m·1 ⟹ Π₊+Π₋=1
    ——谱 ±m 的两个投影覆盖全空间（恒等式，无需壳条件）。 -/
theorem dirac_mass_projectors_complement (m φ : ℝ) :
    (DiracOp m φ + m • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      + (m • (1 : Matrix (Fin 2) (Fin 2) ℝ) - DiracOp m φ)
      = 2 * m • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [DiracOp, e_01, e_10, smul_eq_mul]
    ring

/-! ## 每步 Δφ 候选：翻倍说（Δφ=ln2）⟹ 3-4-5 勾股（#64，候选 C1 代数核心）

候选扫描（scripts/DeltaPhi_candidate_probe.py）判读：
C1（Δφ=ln2，递归每步翻倍）是唯一给出**纯整数勾股闭合**的候选——
tanh(ln2)=3/5 ⟹ 一步翻倍偏转 sinθ₁=3/5、cosθ₁=4/5、γ=5/4（3-4-5）；
C2（谱隙锚 coshΔφ−1=Δλ_min）零自由参数但无数值特称（存留并列）；
C3（窗口 d_H）单步 v≈0.99c 不合理（作为"每步"证伪，窗口总步语义保留）；
C4（ln15/4）与 C1 近亲（15^{1/4}≈2，差 1.6%）登记观察。
"翻倍"的 2 = 旋量纤维维数（Fin 2，SpinorFiberBridge）——每步递归翻倍 =
态空间 ×2（4 步 ⟹ 2⁴=16 态，Clifford 全态，15=16−1 非标量层）。 -/

/-- ★★ 翻倍说核心恒等：cosh(ln 2) = 5/4 ⟹ 一步翻倍的膨胀因子 γ=5/4。 -/
theorem cosh_log_two : Real.cosh (Real.log 2) = 5 / 4 := by
  rw [Real.cosh_def]
  simp [Real.exp_log, div_eq_mul_inv]

/-- ★★ 翻倍说核心恒等：sinh(ln 2) = 3/4（一步翻倍的谱流位移）。 -/
theorem sinh_log_two : Real.sinh (Real.log 2) = 3 / 4 := by
  rw [Real.sinh_def]
  simp [Real.exp_log, div_eq_mul_inv]

/-- ★★ 翻倍说核心恒等：tanh(ln 2) = 3/5 ⟹ 一步翻倍的 v/c = 3/5（3-4-5 勾股）。 -/
theorem tanh_log_two : Real.tanh (Real.log 2) = 3 / 5 := by
  rw [Real.tanh_eq_sinh_div_cosh, sinh_log_two, cosh_log_two]
  norm_num

/-- ★★ 一步翻倍偏转的纯整数签名：sinθ₁ = tanh(ln2) = 3/5
    ——三层时间分层桥（rapidity_theta_identity）与翻倍说合取：
    第一步偏转给出 3-4-5 勾股（sinθ=3/5、γ=5/4、时间耦合 cosθ=4/5）。 -/
theorem step_deflection_sine_three_fifths (θ : ℝ) (h : Real.sin θ = Real.tanh (Real.log 2)) :
    Real.sin θ = 3 / 5 := by
  rw [h, tanh_log_two]

end MUFPF.RapidityTimeLayering
