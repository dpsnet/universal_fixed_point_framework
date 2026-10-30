import Mathlib.Tactic
import MUFPFormalization.HorizonFunctional
import MUFPFormalization.SpinorFiberBridge
import MUFPFormalization.AreaOperatorNormalization

/-!
# 视界泛函 = Bun(∂Rec_D) 纤维截面泛函：机检化封装（2026-10-24）

对应物理论证层裁决采纳（`Bun∂RecD本体_对接论证.md`）后的机检化路径：
"视界泛函 ℱ = 纤维截面泛函"等同。本文件把 `HorizonFunctional.lean` 的模板对象
显式封装为 Bun(∂Rec_D) 的丛要素（底空间采样点 / 截面 / 纤维二次型 / 荷读出）：

- `bunSection us φ`：Bun(∂Rec_D) 的**截面**（底空间 = 视界采样点集 us，
  每点截面值 φ(U)——类型同 φ，语义指认）；
- `sectionQuadraticForm us φ := horizonFunctionalDisc us φ`：**纤维上的二次型**
  （ℱ[c·φ] = c²·ℱ[φ]，二次性由 horizonFunctionalDisc_smul 机检）；
- ★ `horizonFunctional_eq_sectionForm`：**视界泛函 = 截面二次型**（rfl——
  "模板 = 本体"的指认恒等）；
- ★ `relEntropy_as_bundleCharge`：**相对熵 = 丛荷读出** −2π·Q[φ]
  （−2π = KMS 周期×旋量结构——2310 附录 B19–B21 守恒荷模板）；
- `sectionDensity_readout`：截面密度 d/4（纤维维数 2 ⟹ 每面积元密度 1/4）。

诚实边界：本文件是**语义封装别名**（rfl/定义级恒等）——把已机检的代数对象
显式命名为丛要素；"Bun(∂Rec_D) 即物理视界丛"的物理指认属物理论证层
（已裁决采纳，见 `Bun∂RecD本体_对接论证.md`）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.HorizonFunctionalBundle

open MUFPF.HorizonFunctional
open MUFPF.SpinorFiber

/-- Bun(∂Rec_D) 截面：底空间 = 视界采样点集 us，每点截面值 φ(U)
    （类型同 φ : ℝ → ℝ——语义指认：φ 为丛截面，不再视为裸函数）。 -/
def bunSection (us : Finset ℝ) (φ : ℝ → ℝ) : ℝ → ℝ := φ

/-- 纤维二次型（截面聚合）：Q[φ] := Σ U·φ(U)² = ℱ[φ]
    （纤维上二次型——二次性由 horizonFunctionalDisc_smul 机检）。 -/
noncomputable def sectionQuadraticForm (us : Finset ℝ) (φ : ℝ → ℝ) : ℝ :=
  horizonFunctionalDisc us φ

/-- ★ 视界泛函 = 截面二次型（"模板 = 本体"的指认恒等：
    ℱ[φ] 即 Bun(∂Rec_D) 纤维截面上的二次型）。 -/
theorem horizonFunctional_eq_sectionForm (us : Finset ℝ) (φ : ℝ → ℝ) :
    horizonFunctionalDisc us φ = sectionQuadraticForm us φ := by
  unfold sectionQuadraticForm
  rfl

/-- ★ 相对熵 = 丛荷读出：S^rel = −2π·Q[φ]（−2π 前缀 = KMS 周期×旋量结构，
    Noether 荷读出——2310 附录 B19–B21 守恒荷 = 自同构 × 辛积反对称模板）。 -/
theorem relEntropy_as_bundleCharge (us : Finset ℝ) (φ : ℝ → ℝ) :
    relEntropyDisc us φ = -((2 : ℝ) * Real.pi) * sectionQuadraticForm us φ := by
  unfold relEntropyDisc sectionQuadraticForm
  rfl

/-- ★ 截面密度读出：Bun(∂Rec_D) 纤维密度（codim=2）= d/4——纤维维数 2
    （Fin 2 旋量）⟹ 每面积元密度 1/4（bunFiberDensity2 引用的丛表述）。 -/
theorem sectionDensity_readout (d : ℝ) :
    MUFPF.AreaOperator.normalizedArea d 2 = d / 4 := by
  exact MUFPF.AreaOperator.area_eq_defect_div_four d

end MUFPF.HorizonFunctionalBundle
