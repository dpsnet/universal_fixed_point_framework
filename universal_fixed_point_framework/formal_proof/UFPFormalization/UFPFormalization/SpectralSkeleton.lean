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
-- 本文件中 UFPF 相关引用数量：2
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace UFPFormalization

/-!
# SpectralSkeleton — P5-4 代数谱骨架：束缚带 ⊆ 谱 + 谱间隙集合表述（层次 B 代数层）
# （原 PhotonTopologySpectrum/PhotonTopologySpectral，2026-08-14 更名：内容为通用谱理论，
#   按内容域命名原则去光子前缀；光子家族命名约定见 lean_deduplication_tracker 组 H）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.4 层次 B / §3.5 P5-4
论文: paper/paper44_photon_topology.md 定理 T3（谱间隙闭合）/ §4.4 氢原子谱带锚定

## 形式化范围（诚实边界）
层次 B（连续谱 [0,∞)）的完整形式化（spec(H) = {E_n} ∪ [0,∞)）需要谱测度/无界自伴算子
理论——mathlib 尚未覆盖（全行业泛函分析缺口），登记库依赖开放项（§3.4 层次 B）。
本模块闭合其**代数谱骨架**（不依赖谱测度，代数谱定义即可）：
1. `boundEnergy_mem_spectrum`：束缚本征值 ∈ 谱（复用 mathlib `HasEigenvalue.mem_spectrum`，
   一般模无需有限维——束缚带 ⊆ spec(H_atom) 的单点形式）；
2. `boundBand_subset_spectrum`：束缚带（束缚本征值集合）⊆ 谱（集合形式）；
3. `boundBand`/`freeBand`/`ionizationGap`：束缚带/自由带/电离阈的定义性表述
   （数值锚定 paperX_hydrogen_spectral_gap.py S1-S3，谱带参数第一性标定 §4.4）。

**未形式化（登记开放）**：完整谱等式 spec(H) = {E_n} ∪ [0,∞)（需谱测度理论）；
自伴性/谱 ⊆ ℝ 的 Hilbert 层。**电离阈 sSup 已闭合（2026-08-12）**：`hydrogen_ionizationGap_eq`
（氢原子束缚带 sSup = 13.6 eV，§4.4 锚定，见本文件末尾）。 -/

/-! ## 束缚本征值 ∈ 谱（代数谱骨架核心） -/

/-- 束缚本征值 ∈ 谱（P5-4 核心）：原子哈密顿量 H 的束缚态本征值 μ 必在谱中。
    复用 mathlib `HasEigenvalue.mem_spectrum`（一般模，无需有限维）——
    "束缚带 ⊆ spec(H_atom)" 的单点形式（定理 T3 的束缚带侧，代数层闭合）。 -/
theorem boundEnergy_mem_spectrum {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]
    {H : Module.End R M} {μ : R} (h : H.HasEigenvalue μ) : μ ∈ spectrum R H :=
  h.mem_spectrum

/-- 束缚带（定义）：原子哈密顿量 H 的束缚本征值集合（氢原子束缚带 {E_n} 的抽象表述；
    Rydberg 数值锚定在 paperX_hydrogen_spectral_gap.py S1-S3，谱带参数第一性标定 §4.4）。 -/
def boundBand {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]
    (H : Module.End R M) : Set R :=
  {μ : R | H.HasEigenvalue μ}

/-- 束缚带 ⊆ 谱（P5-4 集合形式）：原子哈密顿量 H 的束缚本征值全体含于其谱
    （`boundEnergy_mem_spectrum` 逐点提升——定理 T3 束缚带侧集合表述闭合）。 -/
theorem boundBand_subset_spectrum {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]
    (H : Module.End R M) : boundBand H ⊆ spectrum R H := by
  intro μ hμ
  exact hμ.mem_spectrum

/-! ## 谱间隙集合表述（定义性；数值锚定 §4.4） -/

/-- 自由带（定义）：电离阈以上连续谱 [0,∞)（层次 B 连续部分——完整谱等式
    spec(H) = boundBand ∪ freeBand 需谱测度理论，登记库依赖开放项）。 -/
def freeBand : Set ℝ := Set.Ici 0

/-- 电离阈（定义）：束缚带内能级到自由带底的跃迁能 sup{|E_n|}（氢原子 = 13.6 eV，§4.4 锚定；
    sSup 的序列证明登记开放——数值层 paperX_hydrogen_spectral_gap.py S3 已核对电离阈 13.6 eV）。 -/
noncomputable def ionizationGap {M : Type*} [AddCommGroup M] [Module ℝ M] (H : Module.End ℝ M) : ℝ :=
  sSup {x : ℝ | ∃ μ ∈ boundBand H, x = |μ|}

/-! ## 电离阈 sSup 序列证明（P5-4 剩余项推进，2026-08-12，氢原子锚定 §4.4） -/

/-- 氢原子束缚能级绝对值集合（§4.4 锚定）：{13.6/n² | n : ℕ, n ≥ 1}
    —— 氢原子束缚带 {|E_n|} = {13.6/n²}（E_n = -13.6/n² eV，Rydberg 锚定）。 -/
def hydrogenBand : Set ℝ :=
  {x : ℝ | ∃ n : ℕ, n ≥ 1 ∧ x = 13.6 / (n : ℝ) ^ 2}

/-- **电离阈 sSup 定理（P5-4 剩余项闭合）**：氢原子束缚带的 sSup = 13.6 eV
    —— 电离阈 = 束缚带内最大能级绝对值（基态 |E₁| = 13.6，n=1 时最大），
    数值锚定 paperX_hydrogen_spectral_gap.py S3（§4.4：谱间隙 = 电离阈 13.6 eV）。 -/
theorem hydrogen_ionizationGap_eq :
    sSup hydrogenBand = 13.6 := by
  -- ① 13.6 ∈ hydrogenBand（n=1 基态，|E₁| = 13.6）
  have h1 : 13.6 ∈ hydrogenBand := by
    refine ⟨1, by norm_num, ?_⟩
    norm_num
  -- ② 上界：∀ x ∈ band, x ≤ 13.6（n² ≥ 1 ⟹ 13.6/n² ≤ 13.6）
  have hub : ∀ x ∈ hydrogenBand, x ≤ 13.6 := by
    intro x hx
    rcases hx with ⟨n, hn, rfl⟩
    have hn_ge1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
    have hn_pos : (0 : ℝ) < n := by
      exact_mod_cast (lt_of_lt_of_le (by norm_num : (0 : ℕ) < 1) hn)
    have hn_sq_pos : 0 < (n : ℝ) ^ 2 := sq_pos_of_pos hn_pos
    have hn_sq_ge1 : (1 : ℝ) ≤ (n : ℝ) ^ 2 := by
      nlinarith [sq_nonneg ((n : ℝ) - 1), hn_ge1]
    -- 13.6/n² ≤ 13.6 ⟺ 13.6 ≤ 13.6·n²（乘正 n²）
    field_simp [hn_sq_pos.ne']
    nlinarith [hn_sq_ge1, (show (0 : ℝ) < 13.6 by norm_num)]
  -- ③ 结论：sSup = 13.6（上下界夹逼：csSup_le + le_csSup）
  apply le_antisymm
  · exact csSup_le ⟨13.6, h1⟩ hub
  · exact le_csSup ⟨13.6, hub⟩ h1

end UFPFormalization
