-- ============================================================
-- ③B 的正面半边与它的边界：自伴化投影只能逐对象，不能做函子
-- ============================================================
-- ③B 裁决（`SpHermLayerDecision.lean`）给出否定半边：`D` 扛不进自伴层。
-- 本模块补正面半边，并钉死它止步的位置。
--
-- 论文命题 2.4.4 L207 的自伴化口径是
--   A_R = ½(−log U_R + (−log U_R)*)，
-- 本库 `DFunctor` 的像 `A = stepMatrix` 是实 0/1 矩阵，故自伴化退化为对称化
--   symPart M = ½(M + Mᵀ)（实矩阵下 M* = Mᵀ）。
--
-- 两个结论：
--  (1) **对象层可行**：`symPart M` 恒自伴（`symPart_isHermitian`），
--    所以「自伴化之后落在自伴层」在对象层是真的——论文那一句的对象层读法站得住。
--  (2) **态射层不可行**：`sym_projection_not_functorial` 表明自伴化**破坏交织等式**，
--    所以它不能构成一个函子 `Rec ⥤ SpHerm`。
--
-- (2) 的数值先检（`pr634hermfun.py` / `pr634hermfun.txt`，穷举非抽样）：
--   n, m ∈ {1,2,3} 全部 step 与全部 f，筛出满足交换性 step_Y ∘ f = f ∘ step_X 的
--   2166 个三元组；原像交织 2166/2166 成立（自检通过，说明脚本与 `DFunctor` 一致），
--   自伴化后 **1789/2166 破坏**（82.6%）。
--   最小反例 n=1, m=2 的残差恰为 0.5（精确值，非浮点噪声）——本模块即证此例。
--
-- 结论：论文 L207 的「投影到自伴谱内容」是**逐对象操作**，不是函子。
-- 这一条防止把「自伴化口径」误当作「存在一个自伴化函子」。
-- ============================================================

import MUFPFormalization.DecursionFunctor
import MUFPFormalization.SpCategory

namespace MUFPF

open Matrix

/-- 对称化（自伴化）投影：`½(M + Mᴴ)`。

对实 0/1 矩阵（`stepMatrix` 的值域）`Mᴴ = Mᵀ`，故与论文 L207 的
`½(−log U + (−log U)*)` 同形——这里的 `M` 扮演 `−log U` 的位置。 -/
noncomputable def symPart {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  (2 : ℂ)⁻¹ • (M + Matrix.conjTranspose M)

/-- **对象层可行**：自伴化后的矩阵恒自伴。

⇒ 论文「自伴化之后落在自伴层」在对象层成立，无需任何谱条件。 -/
theorem symPart_isHermitian {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) :
    symPart M = Matrix.conjTranspose (symPart M) := by
  unfold symPart
  rw [Matrix.conjTranspose_smul, Matrix.conjTranspose_add, Matrix.conjTranspose_conjTranspose]
  rw [add_comm]
  simp

/-- **态射层不可行**：自伴化投影不保交织等式，故不构成函子。

否证一个全称：对一切 `n, m`、一切 `step`、一切满足交换性的 `f`，交织等式在
自伴化后仍成立 —— 假。最小反例 `n = 1, m = 2`，残差 `½`。 -/
theorem sym_projection_not_functorial :
    ¬ ∀ (n m : ℕ) (sx : Fin n → Fin n) (sy : Fin m → Fin m) (f : Fin n → Fin m),
        (∀ i, sy (f i) = f (sx i)) →
        transferMatrix f * symPart (stepMatrix sy)
          = symPart (stepMatrix sx) * transferMatrix f := by
  intro h
  -- 最小反例：单点恒等源 / 两点常值靶 / 唯一映射
  have h1 := h 1 2 (id : Fin 1 → Fin 1) (fun _ => (0 : Fin 2)) (fun _ => (0 : Fin 2))
    (by intro i; rfl)
  -- 取 (0, 1) 元比较
  have h01 := congrFun (congrFun h1 (0 : Fin 1)) (1 : Fin 2)
  simp [transferMatrix, stepMatrix, symPart, Matrix.mul_apply] at h01

end MUFPF
