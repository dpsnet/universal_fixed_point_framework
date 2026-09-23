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
-- 本文件中 UFPF 相关引用数量：0
-- ============================================================

import Mathlib.Algebra.Quaternion
import Mathlib.Algebra.Algebra.Equiv
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.Tactic

open Matrix
open scoped Quaternion

namespace MUFPF

/-!
# QuaternionTensorIndex.lean — V5 两个决定性结构语句

对应 RN-ENDO-010 §8.19（路径1 代数桥探查）的机器封闭目标：

  1. `dim_ℝ(ℍ ⊗_ℝ ℍ) = 16`：四元数代数的两副本实张量积，实维数为 16。
  2. `M₄(ℝ) ≇ M₁₆(ℝ)`（对象级否定）：4×4 实矩阵代数与 16×16 实矩阵代数
     不存在 ℝ-代数同构。

## 语义（判定 Chain B 的 16 内源）

- 语句 1 给出 `dim_ℝℍ² = 16` 的**代数真值**：ℍ⊗_ℝℍ 与 M₄(ℝ) 同实维数 16。
- 语句 2 判定**对象级级别**：`ℍ⊗_ℝℍ ≅ M₄(ℝ)`（如数值探查所支持）所落的宿主
  M₄(ℝ) 是 4×4 对象，而 Cl(1,7) 的旋量模宿主是 M₁₆(ℝ)（16×16 对象）；
  `M₄(ℝ) ≇ M₁₆(ℝ)`。故 `16 = dim_ℝℍ²` 只是**维数恒等/模分解巧合**，
  不是宿主对象的代数内源 —— 与 §8.19 判定结论一致。

## 诚实边界

- 本文件仅封闭上述**两个 finrank/对象级命题**。
- 正向同构 `ℍ⊗_ℝℍ ≅ M₄(ℝ)` 未在本文件构造（其为对象内部结构，需显式基同构，
  由 `chainB_hH_algebra_bridge.py` 数值支持；本文件不伪称）。
- `Cl(1,7) ≅ M₁₆(ℝ)`（Clifford 周期）与旋量 16 = 2·k_max 均依赖外部 Clifford
  签名事实，不在本文件重证。
-/

/-! ### 语句 1：`dim_ℝ(ℍ ⊗_ℝ ℍ) = 16` -/

/-- **dim_ℝℍ = 4**：四元数代数（Mathlib `Quaternion ℝ`）作为实模作用于自身的维数为 4。
    复用 mathlib `Quaternion.finrank_eq_four`（`ℍ[R]` 记为 split 四元数代数，c₁=c₂=c₃）。
    这即 Chain B 里 `dim_ℝℍ = 4` 的形式化基础。 -/
lemma quaternion_real_finrank :
    Module.finrank ℝ (Quaternion ℝ) = 4 := by
  exact Quaternion.finrank_eq_four

/-- **dim_ℝ(ℍ ⊗_ℝ ℍ) = 16**：`dim_ℝℍ² = 4×4 = 16`。
    张量积实维数乘法：`finrank ℝ (M ⊗[ℝ] M) = finrank ℝ M * finrank ℝ M`，
    代入 dim_ℝℍ = 4 得 16。 -/
lemma quaternion_sq_tensor_finrank :
    Module.finrank ℝ (TensorProduct ℝ (Quaternion ℝ) (Quaternion ℝ)) = 16 := by
  simp [Module.finrank_tensorProduct, Quaternion.finrank_eq_four]

/-! ### 语句 2：`M₄(ℝ) ≇ M₁₆(ℝ)`（对象级否定） -/

/-- **dim_ℝ M₄(ℝ) = 16**：4×4 实矩阵代数的实维数为 4×4 = 16。
    （与 `dim_ℝ(ℍ ⊗_ℝ ℍ) = 16` 同值，故维数不足以区分二者与宿主。） -/
lemma matrix4_real_finrank :
    Module.finrank ℝ (Matrix (Fin 4) (Fin 4) ℝ) = 16 := by
  simp [Module.finrank_matrix, Module.finrank_self]

/-- **dim_ℝ M₁₆(ℝ) = 256**：16×16 实矩阵代数（Cl(1,7) 的宿主）实维数为 16×16 = 256。 -/
lemma matrix16_real_finrank :
    Module.finrank ℝ (Matrix (Fin 16) (Fin 16) ℝ) = 256 := by
  simp [Module.finrank_matrix, Module.finrank_self]

/-- **对象级否定**：`M₄(ℝ) ≇ M₁₆(ℝ)`。
    ℝ-代数同构 `e` 是实线性等价 `e.toLinearEquiv`，而维度量 `finrank` 是
    实线性等价的**不变量**（`LinearEquiv.finrank_eq`）。若存在这样的同构，
    则 16 = dim_ℝ M₄(ℝ) = dim_ℝ M₁₆(ℝ) = 256，矛盾（norm_num）。 -/
theorem matrix4_ne_matrix16_no_algEquiv
    (e : Matrix (Fin 4) (Fin 4) ℝ ≃ₐ[ℝ] Matrix (Fin 16) (Fin 16) ℝ) : False := by
  have hfin : Module.finrank ℝ (Matrix (Fin 4) (Fin 4) ℝ) =
      Module.finrank ℝ (Matrix (Fin 16) (Fin 16) ℝ) := e.toLinearEquiv.finrank_eq
  rw [matrix4_real_finrank, matrix16_real_finrank] at hfin
  norm_num at hfin

/-- 汇总版（可读陈述）：不存在 `M₄(ℝ) ≃ₐ[ℝ] M₁₆(ℝ)` 的同构。 -/
theorem no_algEquiv_matrix4_to_matrix16 :
    ¬ Nonempty (Matrix (Fin 4) (Fin 4) ℝ ≃ₐ[ℝ] Matrix (Fin 16) (Fin 16) ℝ) := by
  rintro ⟨e⟩
  exact matrix4_ne_matrix16_no_algEquiv e

end MUFPF