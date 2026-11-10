/-
# 「链复形」叙述的代数前提检验：`d_A` 不是微分

## 背景

`HigherSpCategory.lean` 的模块注释把 Sp 高阶范畴描述为「具有链复形结构，每层的缺陷由同一个交换子
`[A, ·]` 给出」，并由此列出层 1/2/3（后来扩到层 4）。若该叙述成立，则 `d_A` 应当是一个链复形微分，
即必须满足 `d_A ∘ d_A = 0`。本文件检验这一前提。

## 本文件机检的结论

取 `A_X = A_Y = J = !![0,1;0,0]`（2×2 幂零 Jordan 块），一元化算子
`dJ H := J * H - H * J` 满足：

* `dJ matE21 = !![1,0;0,-1]`；
* `dJ (dJ matE21) = -(2 : ℂ) • J`，而 `J ≠ 0`，故 `dJ (dJ matE21) ≠ 0`。

即 `d_A` **不满足** `d² = 0`，不是链复形微分。数值侧同口径复核（对角同谱、两个不同对角、随机 8 组
一律给出 `max|d²| ≠ 0`）显示 `d² = 0` 只在 `A_X = A_Y = c • 1`（同一标量）时成立——而该情形下
`d_A ≡ 0`，层 2 的右端项只能为零，`P = Q`，无非平凡 2-态射。

因此「链复形结构给出恰三层非平凡态射」这一叙述在代数前提上不成立：`d² = 0`（真微分）与「存在非平凡
的高阶态射」互斥。层塔的截断只能来自定义时停止写新类型，而不是来自微分结构的自然终止。

## 边界（不作正面断言）

* 层 5 及以上的态射类型在库内未定义，故「层塔可无限延续」在库内无法形式化；本条是**定义边界**，
  不是定理。
* 「`A_X = A_Y = c • 1 ⇒ d_A ≡ 0`」是初等代数事实，本文件未机检；它只用于说明互斥性的另一侧。
-/

import MUFPFormalization.SpLayerNonCollapse

namespace MUFPF

open CategoryTheory Matrix

/-- 一元化交换子算子：`A_X = A_Y = J` 时 `d_A(H) = [J, H]`。 -/
def dJ (H : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  jordanMat * H - H * jordanMat

/-- 矩阵单位 `E₂₁ = !![0,0;1,0]`（本文件的反例输入）。 -/
def matE21 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 0; 1, 0]

/-- `dJ` 作用于 `E₂₁` 给出 `diag(1,-1)`。 -/
theorem dJ_E21 : dJ matE21 = !![1, 0; 0, -1] := by
  show jordanMat * matE21 - matE21 * jordanMat = !![1, 0; 0, -1]
  rw [jordan_commutator_apply]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [matE21]

/-- `dJ` 的平方作用于 `E₂₁` 给出 `-2 • J`（`J ≠ 0`）。 -/
theorem dJ_dJ_E21 : dJ (dJ matE21) = -(2 : ℂ) • jordanMat := by
  rw [dJ_E21]
  show jordanMat * !![1, 0; 0, -1] - !![1, 0; 0, -1] * jordanMat = -(2 : ℂ) • jordanMat
  rw [jordan_commutator_apply]
  ext i j
  fin_cases i <;> fin_cases j <;> (simp [jordanMat, Matrix.smul_apply] <;> norm_num)

/-- `dJ ∘ dJ ≠ 0`：`d_A` 不是链复形微分。 -/
theorem dJ_dJ_E21_ne_zero : dJ (dJ matE21) ≠ 0 := by
  rw [dJ_dJ_E21]
  intro h
  have h01 := congrFun (congrFun h 0) 1
  simp [jordanMat, Matrix.smul_apply, Matrix.zero_apply] at h01

/-- 结论：存在 `H` 使 `dJ (dJ H) ≠ 0`，故 `d_A` 不满足链复形微分的 `d² = 0`。 -/
theorem dJ_not_differential :
    ∃ H : Matrix (Fin 2) (Fin 2) ℂ, dJ (dJ H) ≠ 0 :=
  ⟨matE21, dJ_dJ_E21_ne_zero⟩

end MUFPF
