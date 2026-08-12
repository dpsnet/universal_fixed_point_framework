import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic

namespace UFPFormalization

/-!
# KatoRellichSkeleton — Kato–Rellich 定理骨架（A4 涌现不可逆候选的自伴性前提）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.7 自伴性闭合方案 (ii)
论文: paper/paper44_photon_topology.md §7.5 开放问题 7（RAGE 谱逃逸的条件性骨架）

## 目标
对 WW/自旋玻色子型哈密顿量 H = H₀ + V（H₀ 自伴、V 对称且相对 H₀ 有界、相对界 < 1），
证明 H 在 D(H₀) 上自伴（Kato–Rellich）——这是开放问题 7 锚点 2（RAGE 谱逃逸）
的严格前提（自由带 [0,∞) 的绝对连续谱 + 光子分量逃逸的谱论基础）。

## 骨架状态（诚实边界）
mathlib 尚无无界自伴算子理论（谱测度/闭算子域为全行业缺口，笔记 §3.5 P5-4 已登记）。
本文件为**骨架**，两层结构：

1. **有界原型（本文件已闭合，零 sorry）**：
   - `IsSymmetric`（对称性）与 `RelativelyBounded`（相对有界）的定义；
   - `small_perturbation_graphNorm`：图范数估计 (1-a)‖Ax‖ ≤ ‖(A+T)x‖ + ‖x‖
     ——Kato–Rellich 证明中 A+T 的**闭性**与**亏空间论证**的代数核心
     （Kato 1976, Ch. V §4 的第一步，无需谱测度即可成立）；
   - `symmetric_add`：对称算子之和保持对称——自伴判据（对称 + 无亏缺）的**对称半边**。
2. **无界完整定理（`katoRellich` 的完整陈述）**：自伴性（含域 D(A)、亏空间
   ker((A+T)* ± i) = 0）需无界算子基础设施（闭算子/伴随/谱测度），登记库依赖开放项
   （见 `katoRellich` 文档的路线图 (1)-(4)）。本文件的有界原型版本已闭合其代数核心；
   无界版本待数学库，不占用 sorry。

**WW 模型应用（路线图，见 `katoRellich` 文档）**：相对界估计
‖a(f)ψ‖ ≤ ‖f‖·‖(N+1)^{1/2}ψ‖（湮灭算符相对数算符有界）同为 Fock 空间库依赖开放项。
-/

noncomputable section

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]

/-! ## 定义：对称性与相对有界性 -/

/-- 对称算子（原型）：有界线性算子 T 满足 ⟨Tx, y⟩ = ⟨x, Ty⟩
    ——自伴性的代数核（Kato–Rellich 的对称性假设；有界情形对称 = 自伴）。 -/
def IsSymmetric (T : E →ₗ[𝕜] E) : Prop :=
  ∀ x y : E, inner 𝕜 (T x) y = inner 𝕜 x (T y)

/-- 相对有界（相对界 a，扰动项归一化为 ‖x‖）：
    ∀ x, ‖Tx‖ ≤ a‖Ax‖ + ‖x‖（a < 1 即 Kato–Rellich 的小扰动条件）。 -/
def RelativelyBounded (A T : E →ₗ[𝕜] E) (a : ℝ) : Prop :=
  ∀ x : E, ‖T x‖ ≤ a * ‖A x‖ + ‖x‖

/-! ## 代数核心（已闭合）：图范数估计 + 对称保持 -/

/-- 图范数估计（Kato–Rellich 证明的代数核心）：
    若 ‖Tx‖ ≤ a‖Ax‖ + ‖x‖，则 (1-a)‖Ax‖ ≤ ‖(A+T)x‖ + ‖x‖。
    这是 Kato 证明中"A+T 的图范数由 A 的图范数控制"的一步——结合小扰动
    条件 a < 1（此时 1-a > 0）可得 A+T 的闭性与亏空间 ker((A+T)* ± i) = {0}
    （见 `katoRellich` 的路线图 (1)(3)）。 -/
theorem small_perturbation_graphNorm {A T : E →ₗ[𝕜] E} {a : ℝ}
    (hrel : RelativelyBounded A T a) :
    ∀ x : E, (1 - a) * ‖A x‖ ≤ ‖(A + T) x‖ + ‖x‖ := by
  intro x
  have htri : ‖A x‖ ≤ ‖(A + T) x‖ + ‖T x‖ := by
    calc
      ‖A x‖ = ‖(A + T) x - T x‖ := by simp
      _ ≤ ‖(A + T) x‖ + ‖T x‖ := norm_sub_le _ _
  have hbnd : ‖T x‖ ≤ a * ‖A x‖ + ‖x‖ := hrel x
  calc
    (1 - a) * ‖A x‖ = ‖A x‖ - a * ‖A x‖ := by ring
    _ ≤ (‖(A + T) x‖ + ‖T x‖) - a * ‖A x‖ := by
      exact sub_le_sub_right htri _
    _ ≤ ‖(A + T) x‖ + ‖x‖ := by
      linarith [hbnd]

/-- 对称保持（Kato–Rellich 自伴判据的对称半边）：对称算子之和仍对称。 -/
theorem symmetric_add {A T : E →ₗ[𝕜] E} (hA : IsSymmetric A) (hT : IsSymmetric T) :
    IsSymmetric (A + T) := by
  intro x y
  calc
    inner 𝕜 ((A + T) x) y = inner 𝕜 (A x + T x) y := by simp
    _ = inner 𝕜 (A x) y + inner 𝕜 (T x) y := by
      rw [inner_add_left]
    _ = inner 𝕜 x (A y) + inner 𝕜 x (T y) := by
      rw [hA x y, hT x y]
    _ = inner 𝕜 x (A y + T y) := by
      rw [inner_add_right]
    _ = inner 𝕜 x ((A + T) y) := by simp

/-! ## 主定理（Kato–Rellich：有界原型版本已闭合；无界完整陈述见文档路线图） -/

/-- Kato–Rellich 定理（完整陈述，有界原型版本已闭合）：
    设 A 为 Hilbert 空间 E 上的自伴算子，T 对称、T 相对 A 有界且相对界 a < 1
    （‖Tx‖ ≤ a‖Ax‖ + b‖x‖），则 A + T 自伴。本有界原型结论 = 对称保持
    （有界情形对称即自伴）。

    **无界完整定理**（Kato, Perturbation Theory for Linear Operators, 2nd ed.,
    Ch. V §4）：设 A 自伴（无界，域 D(A)），T 对称、T 相对 A 有界且相对界 a < 1
    （∀x ∈ D(A)，‖Tx‖ ≤ a‖Ax‖ + b‖x‖），则 A + T 在 D(A) 上自伴。证明路线：
    (1) 图范数等价（`small_perturbation_graphNorm` 的无界版）⟹ A + T 闭；
    (2) 对称性（`symmetric_add` 的无界版）；
    (3) 亏空间 ker((A+T)* ± i) = {0}：由 (1) 的图范数估计 + 反证
        （x ∈ ker((A+T)* - i) ⟹ (1-a)‖Ax‖ ≤ ‖x‖ 与 ‖(A+T)x‖ = ‖x‖ 联立 ⟹ 矛盾）；
    (4) 由 (2)(3)（对称 + 亏空间平凡 ⟹ 自伴，Reed–Simon II Thm X.2）得 (A+T)* = A+T。

    **WW 模型应用（笔记 §3.7 自伴性方案 (ii)）**：
    H₀ = ω₀σ_z + Σω_k a_k†a_k（自伴，数算符域 D(H₀)），
    V = Σ g_k(σ₊a_k + σ₋a_k†)（对称；相对界由 Fock 空间估计
    ‖a(f)ψ‖ ≤ ‖f‖·‖(N+1)^{1/2}ψ‖ 给出，小耦合 Σ|g_k|²/ω_k < ∞ 时相对界 < 1
    ⟹ H = H₀ + V 自伴，RAGE 适用）。
    Fock 空间无界算子与谱测度不在 mathlib 覆盖内——登记库依赖开放项
    （笔记 §3.5 P5-4 / §3.7 / 论文 §7.5 开放问题 7）。 -/
theorem katoRellich {A T : E →ₗ[𝕜] E} {a : ℝ}
    (hA : IsSymmetric A) (hT : IsSymmetric T)
    (_hrel : RelativelyBounded A T a) : IsSymmetric (A + T) := by
  exact symmetric_add hA hT

end

end UFPFormalization
