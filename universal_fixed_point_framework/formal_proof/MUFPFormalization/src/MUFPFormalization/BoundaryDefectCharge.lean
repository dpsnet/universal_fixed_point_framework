import MUFPFormalization.AreaOperatorSpectrum
import MUFPFormalization.HolographicAdjunctionBridge
import MUFPFormalization.HolographicEntropyDegeneration
import MUFPFormalization.SpinorFiberBridge

/-!
# BoundaryDefectCharge：15 计数载荷读数 + Bun(∂Rec_D) 纤维密度

对应物理论证层裁决采纳后的机检化路径（2026-10-24，用户"都采纳"）：
1. `boundaryDefect15_area_charge`：orbitCount = 15 ⟹ 面积读数落面积量子 15
   （面积以冻结态计数为量子——载荷物理等同，Cℓ(3,1) 确定一态后其余 15 态）。
2. `boundaryDefect15_entropy_charge`：orbitCount = 15 ⟹ 谱熵读数 = ln 15
   （微态计数 = 15——载荷三层统一口径 A 等权上界）。
3. ★ `boundaryDefect15_charge`：组合——面积 = 熵 = 15 计数读数
   （伴随推论 holographic_adjunction_identity + 面积/熵双读出）。
4. `bunFiberDensity2`：Bun(∂Rec_D) 纤维密度 codim=2 代入
   （quarterDensity_of_spinorFiber 的丛表述——纤维维数 2 ⟹ 每面积元密度 d/4）。
5. 物理论证接入点（注释性）：`relEntropyDisc = −2π·ℱ` 即 Bun(∂Rec_D) 的
   Noether 荷读出（HorizonFunctional.lean 已机检；丛语义指认于
   notes/04_lorentz_gravity/Bun∂RecD本体_对接论证.md，本文件不重复定理）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF

open MUFPF.PeriodicOrbitCount
open MUFPF.HolographicAdjunction
open MUFPF.EccentricOrbit
open MUFPF.AreaSpectrum
open MUFPF.HolographicEntropy
open MUFPF.ExplicitAdjunction
open MUFPF.SpinorFiber

/-- ★ 面积读数（15 计数）：orbitCount X = 15 ⟹ areaAt X 落在面积量子 15——
    物理面积以冻结态计数为量子（载荷物理等同：g = 15 = Cℓ(3,1) 其余态数）。 -/
theorem boundaryDefect15_area_charge (X : RecObj) (h : orbitCount X = 15) :
    areaAt X = areaQuantum 15 2 := by
  rw [area_quantization, h]

/-- 简并谱熵 = ln 15（uniform_entropy_eq_log_g 在 g=15 的实例）。 -/
theorem entropyOfRange15_eq_log15 : entropyOfRange 15 = Real.log (15 : ℝ) :=
  uniform_entropy_eq_log_g 15 (by norm_num)

/-- ★ 熵读数（15 计数）：orbitCount E.src = 15 ⟹ 谱熵读数 = ln 15
    （微态计数 15——载荷三层统一，等权上界；ln 15 ≈ 2.708）。 -/
theorem boundaryDefect15_entropy_charge (E : SpImD) (h : orbitCount E.src = 15) :
    entropyAt E = Real.log (15 : ℝ) := by
  unfold entropyAt
  rw [h]
  exact entropyOfRange15_eq_log15

/-- ★ 15 计数载荷读数（组合）：面积 = 熵 = 15 计数——
    伴随推论（面积=熵）+ 面积量子读数 + 熵读数三线合流。 -/
theorem boundaryDefect15_charge (X : RecObj) (hX : orbitCount X = 15)
    (hp : ∃ x : X.T, periodicPoint X x) :
    areaAt X = entropyAt (DIm_obj X) ∧
      areaAt X = areaQuantum 15 2 ∧
      entropyAt (DIm_obj X) = Real.log (15 : ℝ) := by
  constructor
  · exact holographic_adjunction_identity X hp
  · constructor
    · exact boundaryDefect15_area_charge X hX
    · unfold entropyAt DIm_obj
      rw [hX]
      exact entropyOfRange15_eq_log15

/-- Bun(∂Rec_D) 纤维密度（codim=2 代入）：2 维旋量纤维 ⟹ 每面积元密度 d/4
    （quarterDensity_of_spinorFiber 的丛表述——别名 area_eq_defect_div_four）。 -/
theorem bunFiberDensity2 (d : ℝ) :
    MUFPF.AreaOperator.normalizedArea d 2 = d / 4 := by
  exact MUFPF.AreaOperator.area_eq_defect_div_four d

end MUFPF
