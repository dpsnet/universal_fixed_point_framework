/-
  DeltaInvarianceAudit.lean — R-m：α 与 δ 的不变群判别
  =====================================================================================

## 问题

§28 已判：耦合块分解成 `α·1 + β·F + γ·S + δ·A` 之后，`α` 是相似不变量（基无关、数值型），
`δ` 逃出相似类（基依赖、结构型）。但当时「逃出相似类」只给了一个具体见证
（`T = !![1,1;0,1]` 把 `S` 的 `δ` 从 0 变成 −1/2）。

本批要把这个单点提升为**不变群判别**：两者各自在多大的变换群里不变？

## 判据与答案

- `α`：在**任意可逆变换**（`GL(2,ℝ)`）下不变——这就是「迹」的性质。
- `δ`：在**保长度且保朝向**的变换（`TᵀT = 1` 且 `det T = +1`，即 `SO(2)`）下不变；
  在**保长度的反射**（`det T = −1`）下**翻号**；在**剪切**（非正交，即便 `det = 1`）下**改变**。

关键工具是一条**对一切 `T` 都成立**的闭式（无需正交、无需可逆）：

```
  δ(T·M·Tᵀ) = det(T) · δ(M)
```

（`δ(X) := (X₀₁ − X₁₀)/2`。）正交时 `Tᵀ = T⁻¹`，故上式即相似下的变换律；
非正交时 `Tᵀ ≠ T⁻¹`，上式不给出相似律——这正是 §28 见证（剪切，`det = 1` 但 `δ` 变）能成立的原因。

## 净结果

> `α` 的不变群 ⊇ `GL(2)`；`δ` 的不变群 = `SO(2)`（反射只翻号）。
> **两者的不变群不同，故类型不同——这不是分类口号，是可判定事实。**

对 §28 的直接后果：结构型参数 `δ` 的判据**不可能**来自「任意基变换下的不变性」
（那条路只有 `α` 能走）；它天然绑定「保长度」结构。这给下一批留了明确入口：
若对耦合块施加「保长度」约束，`δ` 的大小会与 `α` 的大小绑成一条圆。

## 诚实边界

1. 闭式只证**转置共轭** `T·M·Tᵀ`；一般相似 `T·M·T⁻¹` 的闭式（含 `T⁻¹` 分量）未做。
   正交情形由 `Tᵀ = T⁻¹` 桥接，非正交情形以 §28 见证反证。
2. 不声称 `δ` 的不变群**恰**为 `SO(2)`（只证了 `SO(2)` 内不变、`SO(2)` 外有反例），
   故用「⊇ / 有反例」表述，不用「=」。
3. 不新增常数、不新增公设。
-/

import MUFPFormalization.CouplingDecompAudit
import Mathlib.Tactic

namespace MUFPF.DeltaInvarianceAudit

open MUFPF.CouplingDecompAudit (alpha_survives_similarity delta_escapes_similarity)

/-- `δ(X) := (X₀₁ − X₁₀)/2`：耦合块的反对称读出（`rotGen` 方向系数）。 -/
noncomputable def dlt (X : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := (X 0 1 - X 1 0) / 2

/-- `α(X) := (X₀₀ + X₁₁)/2`：耦合块的标量读出（`1` 方向系数）。 -/
noncomputable def alp (X : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := (X 0 0 + X 1 1) / 2

/-- ★★ **对一切 `T` 的闭式**：`δ(T·M·Tᵀ) = det(T)·δ(M)`。

    不要求 `T` 正交、不要求 `T` 可逆。正交时 `Tᵀ = T⁻¹`，此式即相似变换律；
    非正交时 `Tᵀ ≠ T⁻¹`，此式不构成相似律（故 §28 的剪切见证不与此冲突）。 -/
theorem delta_transpose_conj (M T : Matrix (Fin 2) (Fin 2) ℝ) :
    dlt (T * M * T.transpose) = Matrix.det T * dlt M := by
  simp [dlt, Matrix.mul_apply, Fin.sum_univ_two, Matrix.det_fin_two, Matrix.transpose_apply]
  ring

/-- ★★ **保长度且保朝向（`SO(2)`）下 `δ` 不变**：
    `TᵀT = 1`（正交）且 `det T = 1` ⟹ `δ(T·M·Tᵀ) = δ(M)`。

    注意：闭式 `δ(T·M·Tᵀ) = det T·δ(M)` 对一切 `T` 成立，故**证明里没有引用正交性**；
    正交假设只承担「把 `Tᵀ` 读成 `T⁻¹`」的语义角色，使本条真正成为相似不变性。 -/
theorem delta_preserved_by_proper_orthogonal (M T : Matrix (Fin 2) (Fin 2) ℝ)
    (_horth : T.transpose * T = 1) (hdet : Matrix.det T = 1) :
    dlt (T * M * T.transpose) = dlt M := by
  rw [delta_transpose_conj, hdet]
  ring

/-- ★★ **保长度的反射（`det T = −1`）下 `δ` 翻号**：`δ(T·M·Tᵀ) = −δ(M)`。
    同上：闭式本身不引用正交性，正交假设只用于语义（`Tᵀ = T⁻¹`）。 -/
theorem delta_flips_by_reflection (M T : Matrix (Fin 2) (Fin 2) ℝ)
    (_horth : T.transpose * T = 1) (hdet : Matrix.det T = -1) :
    dlt (T * M * T.transpose) = -dlt M := by
  rw [delta_transpose_conj, hdet]
  ring

/-- ★★ **判决**：`α` 的不变群 ⊇ `GL(2)`（任意可逆），`δ` 的不变群 ⊇ `SO(2)`，
    且 `δ` 在 `SO(2)` 之外有反例（剪切 `det = 1` 仍改变 `δ`）。

    三者合取 ⟹ **`α` 与 `δ` 的不变群不同，类型不同**。 -/
theorem invariance_groups_differ :
    (∀ {M M' T U : Matrix (Fin 2) (Fin 2) ℝ},
        T * U = 1 → U * T = 1 → T * M' = M * T → alp M' = alp M) ∧
      (∀ (M T : Matrix (Fin 2) (Fin 2) ℝ),
        T.transpose * T = 1 → Matrix.det T = 1 → dlt (T * M * T.transpose) = dlt M) ∧
      (∃ (M M' T U : Matrix (Fin 2) (Fin 2) ℝ),
        T * U = 1 ∧ U * T = 1 ∧ T * M' = M * T ∧ dlt M ≠ dlt M') := by
  refine ⟨?_, ?_, ?_⟩
  · intro M M' T U hTU hUT h
    exact alpha_survives_similarity hTU hUT h
  · intro M T horth hdet
    exact delta_preserved_by_proper_orthogonal M T horth hdet
  · obtain ⟨M, M', T, U, h1, h2, h3, h4⟩ := delta_escapes_similarity
    exact ⟨M, M', T, U, h1, h2, h3, h4⟩

end MUFPF.DeltaInvarianceAudit
