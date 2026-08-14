import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Algebra.Group.Idempotent
import Mathlib.Tactic

namespace UFPFormalization

/-!
# MourreSkeleton — Mourre 估计的代数骨架（A4 涌现不可逆候选锚点 2 的 a.c. 谱前提）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.7 自伴性闭合方案 (ii) 边界条件段
论文: paper/paper44_photon_topology.md §7.5 开放问题 7（RAGE 谱逃逸的条件性骨架）
数值: scripts/paperX_mourre_ac_spectrum.py（5/5，推导级 + 数值佐证）

## 目标
对自由无质量玻色子 H₀=|k|（质量门=0，光子）与膨胀生成元 A=½(XP+PX)，
形式化 Mourre 方法（Mourre 1981）的**代数核心**：
  · 恒等式 i[H₀,A] = H₀（标度齐次性 U_sH₀U_s†=e^{-s}H₀ 的一阶展开，或动量空间直接计算）；
  · Mourre 估计 E_I·i[H₀,A]·E_I ≥ a·E_I（I=[a,b]⊂(0,∞)，E_I 为谱投影）
    ⟹ 自由带 [0,∞) 无嵌入本征值、无奇异连续谱 ⟹ 纯绝对连续谱。
这是开放问题 7 锚点 2（RAGE 谱逃逸：χ_K e^{-iHt} P_ac ψ → 0）的谱论前提之一
（另两前提：H 自伴 = Kato–Rellich，见 KatoRellichSkeleton；位置表示 = 标准）。

## 骨架状态（诚实边界）
mathlib 尚无无界自伴算子/谱测度理论（闭算子域为全行业缺口，笔记 §3.5 P5-4 已登记）。
本文件为**骨架**，两层结构：

1. **代数核心（本文件已闭合，零 sorry）**——不依赖谱测度即可成立的纯代数步：
   - `spectralProjection_window_restrict`：谱投影与 H 交换（E_H H = H E_H）+ 幂等
     ⟹ E_I·H·E_I = H·E_I（窗口限制的代数核心——E_I i[H,A] E_I = E_I H E_I 的传输步）；
   - `commutator_conj`：对易子的相似变换 U[H,A]U⁻¹ = [UHU⁻¹, UAU⁻¹]——标度相似性
     （U_s=e^{-iAs}，U_sH₀U_s†=e^{-s}H₀）论证的代数骨架；
   - `mourre_estimate_of_lower_bound`：**核心定理**——若 i[H,A]=H（恒等式，由标度
     齐次性在分析层给出）且谱投影像内 H ≥ a（能量窗口下限），则 Mourre 估计
     a‖E_I x‖² ≤ ⟨E_I x, i[H,A] E_I x⟩ 成立。Mourre 估计 ⟸ 能量下限的纯代数传递。
2. **无界完整定理（`mourreAc` 的完整陈述）**：H₀=|k| 的 a.c. 谱确认需无界谱论
   （单参数酉群求导、谱投影 E_I、Borel 泛函演算），登记库依赖开放项
   （见 `mourreAc` 文档的路线图）。本文件已闭合其代数核心；无界版本待数学库，不占用 sorry。

**数值注记（诚实，与 paperX_mourre_ac_spectrum.py 同步）**：|k| 在 k=0 有尖点，
有限格点上谱导数非求导（Leibniz 律不成立），格点对易子有 O(1) 混叠差——i[H₀,A]=H₀
为**解析精确**（标准谱理论事实），数值内容经恒等式化为精确对角 E_I H₀ E_I = diag(|k_j|)
（S2 精确验证，min eig = a）。耦合（WW/Friedrichs）情形 a.c. 谱保持为文献标准结果
（Fröhlich–Griesemer–Sigal–Spohn 线），登记开放，未独立证明。
-/

noncomputable section

universe u

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-! ## 定义：Mourre 共轭对易子 / 标度相似性 / 谱投影 / 能量下限 / Mourre 估计 -/

/-- i·[H,A]（Mourre 共轭对易子，逐点形式）：i(H∘A − A∘H)。
    恒等式 i[H,A] = H 对自由光子 H₀=|k|、A=½(XP+PX) 解析成立
    （标度齐次性 U_sH₀U_s†=e^{-s}H₀ 一阶展开，或动量空间 [H₀,A]=−iH₀ 直接计算）。 -/
def mourreCommutatorI (H A : E →ₗ[ℂ] E) (x : E) : E :=
  Complex.I • ((H ∘ A) x - (A ∘ H) x)

/-- 标度相似性：U H U⁻¹ = c·H（degree-1 齐次的相似形式）。
    自由光子 H₀ 满足 U_sH₀U_s†=e^{-s}H₀（c=e^{-s}，U_s=e^{-iAs} 膨胀）——
    一阶展开给出 i[H₀,A]=H₀（分析层，见 `mourreAc` 路线图 (1)）。 -/
def ScaledSimilarity (U Uinv : E →ₗ[ℂ] E) (H : E →ₗ[ℂ] E) (c : ℂ) : Prop :=
  U ∘ H ∘ Uinv = c • H

/-- 谱投影的代数性质（P 的像 = 窗口子空间 E_I·E）：幂等 + 自伴。
    （与 RAP4 `IsOrthogonalProjection`（矩阵层 ℝ 结构）区分：本处为内积空间线性映射层
    一般性质，命名 IsSpectralProjection 避免重名。） -/
def IsSpectralProjection (P : E →ₗ[ℂ] E) : Prop :=
  IsIdempotentElem P ∧ ∀ x y : E, inner ℂ (P x) y = inner ℂ x (P y)

/-- 能量窗口下限：谱投影 P 的像内 H ≥ a（∀v∈im P：a‖v‖² ≤ ⟨v,Hv⟩）。
    数值对应：E_I H₀ E_I = diag(|k_j|) 窗口内 min eig = a（paperX_mourre_ac_spectrum.py S2）。
    （⟨v,Hv⟩ 为 ℂ 值；H 自伴时取实部。实数比较用 .re。） -/
def EnergyLowerBound (H P : E →ₗ[ℂ] E) (a : ℝ) : Prop :=
  ∀ v : E, v ∈ LinearMap.range P → a * ‖v‖ ^ 2 ≤ (inner ℂ v (H v)).re

/-- Mourre 估计（标准形式）：a‖E_I x‖² ≤ ⟨E_I x, i[H,A] E_I x⟩（E_I·i[H,A]·E_I ≥ a·E_I 的二次型形式）。 -/
def MourreEstimate (H A P : E →ₗ[ℂ] E) (a : ℝ) : Prop :=
  ∀ x : E, a * ‖P x‖ ^ 2 ≤ (inner ℂ (P x) (mourreCommutatorI H A (P x))).re

/-! ## 代数核心（已闭合）：谱投影窗口限制 + 对易子相似变换 + Mourre 估计传递 -/

/-- 谱投影窗口限制：P 与 H 交换 + 幂等 ⟹ P·H·P = H·P（E_I H E_I = H E_I）。
    这是"Mourre 估计 E_I i[H,A] E_I ≥ a E_I"传输步的代数核心
    （E_I 与 H 交换 + 幂等 ⟹ 窗口限制下 i[H,A] 还原为 H）。 -/
theorem spectralProjection_window_restrict {P H : E →ₗ[ℂ] E}
    (hcommute : P * H = H * P) (hidem : IsIdempotentElem P) :
    P * H * P = H * P := by
  ext x
  have hPH : (P * H) (P x) = (H * P) (P x) := DFunLike.congr_fun hcommute (P x)
  have hPP : (P * P) x = P x := DFunLike.congr_fun hidem x
  calc
    (P * H * P) x = (P * H) (P x) := rfl
    _ = (H * P) (P x) := hPH
    _ = H (P (P x)) := rfl
    _ = H (P x) := by exact congrArg H hPP
    _ = (H * P) x := rfl

/-- 对易子的相似变换：U[H,A]U⁻¹ = [UHU⁻¹, UAU⁻¹]（Uinv∘U = id 时）。
    标度相似性论证的代数骨架：U_s=e^{-iAs} 下 U_sH₀U_s†=e^{-s}H₀ 的离散相似结构
    （一阶展开给出对易子恒等式，见 `mourreAc` 路线图 (1)）。 -/
theorem commutator_conj (U H A Uinv : E →ₗ[ℂ] E)
    (hUinv : Uinv * U = (LinearMap.id : E →ₗ[ℂ] E)) :
    (U * ((H * A) - (A * H)) * Uinv) =
      ((U * H * Uinv) * (U * A * Uinv) - (U * A * Uinv) * (U * H * Uinv)) := by
  ext x
  have hpt : ∀ y : E, Uinv (U y) = y := by
    intro y
    exact DFunLike.congr_fun hUinv y
  simp [hpt, map_sub]

/-- **核心定理（Mourre 估计的代数传递）**：若 i[H,A] = H（恒等式，由标度齐次性在
    分析层给出，见 `mourreAc` 路线图 (1)）且谱投影像内 H ≥ a（能量窗口下限），
    则 Mourre 估计 a‖E_I x‖² ≤ ⟨E_I x, i[H,A] E_I x⟩ 成立——
    **Mourre 估计 ⟸ 能量下限的纯代数传递**（无需谱测度；E_I i[H,A] E_I = E_I H E_I）。 -/
theorem mourre_estimate_of_lower_bound {H A P : E →ₗ[ℂ] E} {a : ℝ}
    (hcomm : ∀ x : E, mourreCommutatorI H A x = H x)
    (hlower : EnergyLowerBound H P a) :
    MourreEstimate H A P a := by
  intro x
  rw [hcomm (P x)]
  exact hlower (P x) (LinearMap.mem_range_self P x)

/-! ## 主定理（Mourre 方法：自由光子 a.c. 谱；代数核心已闭合，无界完整陈述见路线图） -/

/-- Mourre 方法结论（代数核心闭合版）：自由光子情形"恒等式 i[H₀,A]=H₀（标度齐次性
    一阶展开/动量空间直接计算，分析层）+ 窗口能量下限（精确对角 diag(|k_j|) ≥ a）"
    ⟹ **Mourre 估计在窗口 I 上成立**（E_I·i[H₀,A]·E_I ≥ a·E_I 的二次型形式）。
    完整叙述（无界谱论层）：
    设 H₀=|k|（无质量，质量门=0）自伴、A=½(XP+PX) 膨胀生成元自伴，
    (1) 恒等式 i[H₀,A] = H₀（标度齐次性 U_sH₀U_s†=e^{-s}H₀ 一阶展开，或动量空间
        [H₀,A]=−iH₀ 直接计算——分析层，无界算子微分）；
    (2) E_I 为 I=[a,b]⊂(0,∞) 的谱投影（与 H₀ 交换：E_I H₀ = H₀ E_I，`IsSpectralProjection`
        代数性质；E_I H₀ E_I = H₀ E_I，`spectralProjection_window_restrict`）；
    (3) 窗口能量下限 E_I H₀ E_I = diag(|k_j|) ≥ a·E_I（`EnergyLowerBound`；数值精确对角
        验证 paperX_mourre_ac_spectrum.py S2，min eig = a）。
    则 **Mourre 估计在 I 上成立**（`MourreEstimate`，`mourre_estimate_of_lower_bound`）
    ⟹ I∩spec(H₀) 无嵌入本征值、无奇异连续谱 ⟹ 自由带 [0,∞) 为纯绝对连续谱
    （RAGE 谱逃逸前提 (2)，结合自伴 Kato–Rellich + 位置表示三前提齐备）。

    **无界完整证明路线**（Kato 1980 / Mourre 1981 / Reed–Simon 标准谱理论）：
    (1) 单参数酉群 U_s=e^{-iAs} 的强连续性与 H₀ 的 degree-1 齐次性
        （U_sH₀U_s†=e^{-s}H₀）⟹ 对 s 求导得 i[H₀,A]=H₀（无界算子微分，域 D(A)∩D(H₀)）；
    (2) 谱投影 E_I（Borel 泛函演算）与 H₀ 交换（谱定理）；
    (3) Mourre 不等式 E_I i[H₀,A] E_I ≥ a E_I（经 (1) 化为 E_I H₀ E_I ≥ a E_I，窗口下限）；
    (4) Mourre 方法主定理（H 对 A 满足正则性 ⟹ I 无嵌入本征值/奇异连续谱 ⟹ 纯 a.c.）；
    (5) RAGE 定理（a.c. 分量谱逃逸 χ_K e^{-iHt} P_ac ψ → 0）。
    谱测度/无界算子/泛函演算不在 mathlib 覆盖内——登记库依赖开放项
    （笔记 §3.5 P5-4 / §3.7 / 论文 §7.5 开放问题 7）。耦合（WW/Friedrichs）情形
    a.c. 谱保持为文献标准结果（Fröhlich–Griesemer–Sigal–Spohn 线），未独立证明。 -/
theorem mourreAc {H A P : E →ₗ[ℂ] E} {a : ℝ}
    (hcomm : ∀ x : E, mourreCommutatorI H A x = H x)
    (hlower : EnergyLowerBound H P a) :
    MourreEstimate H A P a :=
  mourre_estimate_of_lower_bound hcomm hlower

end

end UFPFormalization
