/-
# DivisorClosureIdentities.lean — 'why D = n = N_gen' 双源重合形式化（Phase 104az-132）

判别结论（132）：D=n=3 是双源重合——
  源 1（代数）：D = (对合域²−1)/不动点² = (7²−1)/4² = 48/16 = 3 ——
              由框架定义量 (7,4) 唯一锁定（d_unique：7²−D·4²=1 ⟹ D=3）
  源 2（结构）：N_gen = 3 = 2^m = 2m+2 唯一解（k_max=8=2³；264/266 机器证明 power_unique）
  ——两个独立来源的 3 重合，无需 Paper 47 仿形感应叙事（Google AI 建议不采纳）。

新发现（132 Q1）：框架量平方差整除闭包——
  k_max²−1 = 对合域×N_gen²   （8²−1 = 63 = 7·9）
  对合域²−1 = N_gen×不动点²   （7²−1 = 48 = 3·16）
  N_gen²−1 = 幂基×幂基²       （3²−1 = 8 = 2·4）
  ——商闭包循环 8→7→3→2（商全落框架量集）。

数值先证伪（_phase104az132_d_identity.py）：Q1 商闭包 3 对精确整除、
Q2 D=2..12 唯一 D=3、Q3 2^m=2m+2 m=0..20 唯一解 m=3——全 PASS。
-/

import Mathlib.Tactic

namespace MUFPF.DivisorClosure

def kMax : ℕ := 8
def nGen : ℕ := 3
def involution : ℕ := 7
def fixedPoint : ℕ := 4
def powerBase : ℕ := 2

/-! 商闭包 1：k_max²−1 = 对合域×N_gen²（63 = 7·9）。 -/
theorem kmax_sq_minus_one : kMax ^ 2 - 1 = involution * nGen ^ 2 := by
  norm_num [kMax, involution, nGen]

/-! 商闭包 2：对合域²−1 = N_gen×不动点²（48 = 3·16）。 -/
theorem involution_sq_minus_one : involution ^ 2 - 1 = nGen * fixedPoint ^ 2 := by
  norm_num [involution, nGen, fixedPoint]

/-! 商闭包 3：N_gen²−1 = 幂基×幂基²（8 = 2·4）。 -/
theorem ngen_sq_minus_one : nGen ^ 2 - 1 = powerBase * powerBase ^ 2 := by
  norm_num [nGen, powerBase]

/-! 商闭包循环（商全落框架量集，闭合链 8→7→3→2）。 -/
theorem quotient_chain : 
    (kMax ^ 2 - 1) / (nGen ^ 2) = involution ∧
    (involution ^ 2 - 1) / (fixedPoint ^ 2) = nGen ∧
    (nGen ^ 2 - 1) / (powerBase ^ 2) = powerBase := by
  constructor
  · norm_num [kMax, nGen, involution]
  constructor
  · norm_num [involution, nGen, fixedPoint]
  · norm_num [nGen, powerBase]

/-! ★★★ D 唯一性：7²−D·4²=1 的唯一自然数解 D=3（=N_gen）。
    （Q2：D=2..12 扫描唯一 D=3——此处形式化一般 D 的唯一性） -/
theorem d_unique (D : ℕ) : involution ^ 2 - D * fixedPoint ^ 2 = 1 → D = nGen := by
  intro h
  norm_num [involution, fixedPoint] at h
  have hle : D * 16 ≤ 49 := by
    by_contra hn
    have hzero : 49 - D * 16 = 0 := Nat.sub_eq_zero_of_le (le_of_not_ge hn)
    rw [hzero] at h
    norm_num at h
  have h49 : 49 = D * 16 + 1 := by
    omega
  norm_num [nGen]
  omega

/-! 双源重合：代数商 D=3 ∧ 结构方程 2^N_gen = 2·N_gen+2（数字验证；
    唯一性由 266 KMaxAlgebra.power_unique 机器证明，此处只并置）。 -/
theorem double_source_coincidence :
    (involution ^ 2 - 1) / (fixedPoint ^ 2) = nGen ∧ 2 ^ nGen = 2 * nGen + 2 := by
  constructor
  · norm_num [involution, nGen, fixedPoint]
  · norm_num [nGen]

/-! 联合主定理：商闭包 ∧ D 唯一性 ∧ 双源重合。 -/
theorem divisor_closure_judgement :
    (kMax ^ 2 - 1 = involution * nGen ^ 2 ∧
     involution ^ 2 - 1 = nGen * fixedPoint ^ 2 ∧
     nGen ^ 2 - 1 = powerBase * powerBase ^ 2) ∧
    (∀ D : ℕ, involution ^ 2 - D * fixedPoint ^ 2 = 1 → D = nGen) ∧
    ((involution ^ 2 - 1) / (fixedPoint ^ 2) = nGen ∧ 2 ^ nGen = 2 * nGen + 2) := by
  constructor
  · constructor
    · exact kmax_sq_minus_one
    · constructor
      · exact involution_sq_minus_one
      · exact ngen_sq_minus_one
  · constructor
    · intro D hD
      exact d_unique D hD
    · exact double_source_coincidence

end MUFPF.DivisorClosure
