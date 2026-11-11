-- ============================================================
-- ③B 裁决锚点：`Sp` 语义分层（自伴层 `SpHerm` vs 复谱层 `SpC`）
-- ============================================================
-- 裁决（2026-11-11）：走方案③（双范畴）、论文用 B 写法。
--
-- 论文 `paper1_fractal_spectral_derecursion.md` 命题 2.4.4 证明 L211 明写
-- 「`A_R` 已取为 Hermitian，故 `D` 的像始终在 `Sp` 中」。该句在两个不同的
-- `Sp` 之间滑动了：
--   * 自伴层 `Sp`（L207 的 A_R = ½(−log U_R + (−log U_R)*)）——本库 `SpHermObj`；
--   * 复谱层 `Sp_ℂ`（定义 5.11 L852、定理 7.31 L1330 的 D_diss）——本库 `SpObj`。
-- 本库 `SpObj` 只有 `n` 与 `A`，是后者。
--
-- 本模块把 B 写法需要的两句落成机检：
--   (1) `D` 的像确实越出自伴层（存在非自伴像）；
--   (2) 更强：**不存在**把 `D` 提升进 `SpHerm` 且与 `DFunctor` 逐对象相容的函子。
--     (2) 是 B 写法最需要的支撑——它堵死「像始终在自伴层」的解读，
--     而不只是在值域里挑一个反例。
--
-- 依赖：`SpDFunctorDichotomy`（`cyclicRec` / `DFunctor_obj_cyclic_nonhermitian`）
--       `SpHermCategory`（`SpHermObj` / `isHerm`）
-- ============================================================

import MUFPFormalization.SpDFunctorDichotomy
import MUFPFormalization.SpHermCategory

namespace MUFPF

open CategoryTheory

/-- **`D` 的像越出自伴层**：存在 `RecObj` 其 `D` 像非自伴。

这是 B 写法在值域层面的正面锚点：`DFunctor` 的值域不全在 `SpHerm` 内。
（与 D40 的二分定理相容：值域内自伴像与非自伴像并存。） -/
theorem DFunctor_range_escapes_hermitian_layer :
    ∃ Y : RecObj.{0}, ¬ IsHermitian (DFunctor.obj Y) :=
  ⟨cyclicRec, DFunctor_obj_cyclic_nonhermitian⟩

/-- **`D` 不能被提升进自伴层**：不存在函子 `F : RecObj ⥤ SpHerm` 使它的对象像
在 `SpObj` 层面与 `DFunctor` 逐点相同。

证明：取 3-循环系统 `cyclicRec`。若这样的 `F` 存在，则 `F.obj cyclicRec` 携带
自伴见证 `isHerm`；由相容性把该见证搬到 `DFunctor.obj cyclicRec` 上，与
`DFunctor_obj_cyclic_nonhermitian` 矛盾。

⇒ 「`D` 的像始终在自伴层」不是「尚未证明」，而是**与机检结论不相容**。
这也是论文 B 写法（把 L211 的 `Sp` 明确为 `Sp_ℂ`）的形式化依据。 -/
theorem no_functor_lifts_DFunctor_into_SpHerm :
    ¬ ∃ F : RecObj.{0} ⥤ SpHermObj, ∀ X : RecObj.{0}, (F.obj X).toSp = DFunctor.obj X := by
  rintro ⟨F, hF⟩
  have hcomp := hF cyclicRec
  have hherm : IsHermitian (F.obj cyclicRec).toSp := (F.obj cyclicRec).isHerm
  rw [hcomp] at hherm
  exact DFunctor_obj_cyclic_nonhermitian hherm

/-- 两个 `Sp` 层不同构：复谱层严格大于自伴层（对象层面）。

与 D35 的 `forgetFunctor_not_surjective_on_objects` 同源，此处以「层内/层外
各有一个代表」的显式对偶形式给出，便于论文直接引用。 -/
theorem two_Sp_layers_are_distinct :
    (∃ E : SpObj, IsHermitian E) ∧ (∃ E : SpObj, ¬ IsHermitian E) :=
  ⟨⟨diag3HermObj.toSp, diag3HermObj.isHerm⟩, ⟨cyclic3SpObj, cyclic3SpObj_not_hermitian⟩⟩

end MUFPF
