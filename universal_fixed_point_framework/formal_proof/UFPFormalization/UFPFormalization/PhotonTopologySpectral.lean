import Mathlib.LinearAlgebra.Eigenspace.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace UFPFormalization

/-!
# PhotonTopologySpectral — P5-4 代数谱骨架：束缚带 ⊆ 谱 + 谱间隙集合表述（层次 B 代数层）

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
电离阈 13.6 eV 的 sSup 证明（序列上确界，数值层已锚定）；自伴性/谱 ⊆ ℝ 的 Hilbert 层。
-/

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

end UFPFormalization
