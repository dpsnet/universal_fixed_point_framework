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
-- 本文件中 UFPF 相关引用数量：5
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.RecCategory
import UFPFormalization.IsolationConstraints
import Mathlib.Data.Matrix.Basic

open UFPFormalization

namespace UFPFormalization

/-!
# IC Decidability (Phase 16C)

In the finite-dimensional prototype, the isolation constraint IC(R₁, R₂)
is always satisfied (`universal_IC_coverage_finite`). This module marks
`isolationConstraint` as `Decidable` for the finite case.

For general (infinite-dimensional) Rec objects, IC decidability is an
open problem (Paper III §7.2, Problem 1). The three sub-conditions have
different decidability statuses:

| Sub-condition | Finite prototype | General case | Decidable? |
|---------------|-----------------|--------------|------------|
| (i) Spectral scale | trivial | bounded ratio of spectral radii | ✅ Yes (computable) |
| (ii) Morphism extendability | trivial | existence of intertwining operator T | ⚠️ Semi-decidable (Sylvester equation) |
| (iii) Topological compatibility | trivial | continuity of the spectral projection | ❌ Undecidable in general |

The finite prototype lumps all three into a single always-true proposition.
The general case reduces to the decidability of spectral radius ratios
and the solvability of operator Sylvester equations.
-/

/--
IC is decidable in the finite prototype: it's always true.
-/
instance (R₁ R₂ : RecObj) : Decidable (isolationConstraint R₁ R₂) :=
  isTrue (by simp [isolationConstraint, spectralScaleCompatible, morphismExtendable, topologicallyCompatible])

/--
Spectral scale compatibility is decidable for finite matrices:
it reduces to computing and comparing spectral radii.
-/
noncomputable def spectralScaleCompatibleDecidable {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) : Bool :=
  let r₁ := spectralRadius A₁
  let r₂ := spectralRadius A₂
  if h : r₂ = 0 then true
  else r₁ / r₂ ≤ 1

/--
Morphism extendability (existence of intertwining operator T) for
finite matrices reduces to solving the Sylvester equation A₁T = TA₂.
This is a linear system in n² variables, decidable by Gaussian elimination.

For the general case, this is semi-decidable: existence of bounded
solutions to operator equations is not computable in general.
-/
def morphismExtendableDecidable {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) : Bool :=
  -- In the finite prototype, T = 0 always works (trivial solution).
  -- The non-trivial case requires solving A₁T - TA₂ = 0.
  true

/--
Topological compatibility is trivially decidable in the finite prototype
(所有有限维空间都是 Polish 空间，拓扑性质自动可判定；spectralRadius 已在 IsolationConstraints 中声明)。
-/
def topologicallyCompatibleDecidable {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) : Bool :=
  true

end UFPFormalization
