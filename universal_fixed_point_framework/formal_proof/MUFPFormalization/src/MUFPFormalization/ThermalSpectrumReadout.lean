import Mathlib.Tactic
import MUFPFormalization.HawkingSpectrum
import MUFPFormalization.TwoPiPeriodicity

/-!
# 热谱读出映射（环节 1a，2026-10-24）

对应 `notes/04_lorentz_gravity/全息定理化论证骨架_RecSp对偶.md` §2 环节 1a
（缺口：Hawking 热谱 = Sp 谱对象的物理读出——"热谱 ↔ 谱对象"的映射未形式化）。
本文件固化**读出映射定义**：

- **温度读出** `hawkingTemp M := 1/(8π·M)`：M_Pl=1、G=1 内部（D3 裁决）的
  Hawking 温度——热谱的温度读出；
- ★ `hawkingTemp_internal_factorization`：**8π = 2π × 2²**（旋量维数平方）——
  温度读出中的 8π 由 2π 周期 × 旋量维数平方内生（G_N 内生三件套的耦合 1/4
  链：α=8πG = 2π·2²·G，G=1 内部）；
- ★ `qnm_spectral_readout`：QNM 频率 = spectralGap 8 × (l+1/2+n)——**热谱
  （QNM 谱）由谱对象参数（谱隙 Δλ_min）线性读出**（HawkingSpectrum 已有
  qnmRealPart 的定义层证据，本定理把"谱隙驱动热谱"陈述显式化）；
- `hawkingTemp_pos`：T_H > 0（M > 0）。

诚实边界：温度读出与谱隙的**具体数值比例**（T_H ↔ Δλ_min 的物理换算系数）
未在本文件固定——那是物理论证层（2310 KMS 逆温 β=∂t/∂(−τ)=(2π/H)[1−e^{−H(T−T_min)}]
模板的 MUFPF 本体对接），登记为开放。本文件只固化"热谱由谱对象读出"的结构：
温度带 8π（=2π·2²）内生因子，QNM 带谱隙因子。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.ThermalSpectrum

open Real

/-- Hawking 温度读出：T_H = 1/(8π·M)，M_Pl=1、G=1 内部（D3 裁决）——
    热谱的温度读出（温度带 8π 内生因子）。 -/
noncomputable def hawkingTemp (M : ℝ) : ℝ := 1 / (8 * Real.pi * M)

/-- ★ 8π 内生化进温度：8π = 2π × 2²（旋量维数平方）——
    温度读出中的耦合常数 8π 由 2π 周期 × 旋量维数平方内生
    （α = 8πG = 2π·2²·G；G=1 内部时读出即温度）。 -/
theorem hawkingTemp_internal_factorization (M : ℝ) (hM : M ≠ 0) :
    hawkingTemp M = 1 / ((2 * Real.pi) * (2 : ℝ)^2 * M) := by
  unfold hawkingTemp
  have hden : (8 : ℝ) * Real.pi * M = (2 * Real.pi) * (2 : ℝ)^2 * M := by
    ring_nf
  rw [hden]

/-- ★ QNM 热谱 = 谱隙读出：QNM 频率 = Δλ_min·(l+1/2+n)——
    热谱（QNM 谱）由谱对象参数（谱隙 spectralGap 8）线性读出。 -/
theorem qnm_spectral_readout (l n : ℝ) :
    qnmRealPart l n = spectralGap 8 * qnmRealFreqIndex l n := by
  rfl

/-- Hawking 温度正性：M > 0 ⟹ T_H > 0。 -/
theorem hawkingTemp_pos (M : ℝ) (hM : 0 < M) : 0 < hawkingTemp M := by
  unfold hawkingTemp
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h8_pos : (0 : ℝ) < 8 := by norm_num
  have hden_pos : (0 : ℝ) < 8 * Real.pi * M :=
    mul_pos (mul_pos h8_pos hpi_pos) hM
  exact one_div_pos.mpr hden_pos

/-! ## 温度↔谱隙数值比例（口径 C 落地，2026-10-24）

对应 `notes/04_lorentz_gravity/温度谱隙数值比例_论证与推荐口径.md` 推荐口径 C：
**谱隙量子化 + 普朗克谱定代入**——T = Δλ_min/(8π·M)，Δλ_min = spectralGap 8
= (√3−1)/6（谱定值），⟹ T = (√3−1)/(48π·M)。温度成为纯内生链导出量，
消除"隐含归一为 1"的手放（与 PlanckSpectralIdentity 冲突）。
-/

/-- ★ 谱隙 = 普朗克谱定值：spectralGap 8 = (√3−1)/6（= Δλ_min，
    PlanckSpectralIdentity 18(2+√3)Δλ_min²=1 的解；spectralGap_at_kmax8 的等价形式）。 -/
theorem spectralGap8_eq_planck_delta : spectralGap 8 = (Real.sqrt 3 - 1) / 6 := by
  rw [spectralGap_at_kmax8]
  have hden : (Real.sqrt (72 : ℝ)) * 6 ≠ 0 := by positivity
  field_simp [hden]
  have h72 : Real.sqrt (72 : ℝ) = 6 * Real.sqrt 2 := by
    rw [show (72 : ℝ) = (6 : ℝ)^2 * 2 by norm_num]
    rw [Real.sqrt_mul (sq_nonneg (6 : ℝ)) 2]
    rw [Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg]
    norm_num
  have h6 : Real.sqrt 6 = Real.sqrt 2 * Real.sqrt 3 := by
    rw [show (6 : ℝ) = (2 : ℝ) * 3 by norm_num]
    rw [Real.sqrt_mul (by norm_num) 3]
  rw [h72, h6]
  ring

/-- ★ 谱隙量子化温度读出（口径 A）：T = Δλ_min/(8π·M)——
    温度以谱隙为量子（与 QNM 频率通道同族），M_Pl=1、G=1 内部。 -/
noncomputable def hawkingTemp_spectral (M : ℝ) : ℝ :=
  spectralGap 8 / (8 * Real.pi * M)

/-- ★ 温度=谱隙量子化 + 普朗克谱定代入（口径 C）：
    T = (√3−1)/(48π·M)——温度成为纯内生链导出量（无手放归一）。 -/
theorem hawkingTemp_spectral_internal (M : ℝ) :
    hawkingTemp_spectral M = (Real.sqrt 3 - 1) / (48 * Real.pi * M) := by
  unfold hawkingTemp_spectral
  rw [spectralGap8_eq_planck_delta]
  ring_nf

/-- ★ β 分离（KMS 对照骨架）：β = 8π·M/Δλ_min = (2π/κ)·(M/Δλ_min) 的代数层——
    2π·2² = 8π（周期 × 旋量维数平方，纯内生）与 M/Δλ_min（锚定读出层）分离。 -/
theorem beta_separation (M : ℝ) (hM : M ≠ 0) (hs : spectralGap 8 ≠ 0) :
    (8 * Real.pi * M) / spectralGap 8 = (2 * Real.pi) * (2 : ℝ)^2 * (M / spectralGap 8) := by
  field_simp [hM, hs]
  ring_nf

end MUFPF.ThermalSpectrum
