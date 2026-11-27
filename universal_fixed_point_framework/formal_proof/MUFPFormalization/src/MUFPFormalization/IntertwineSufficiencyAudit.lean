/-
  IntertwineSufficiencyAudit.lean — R-c：充分性骨架「交织 ⟹ 迹/特征多项式相等」的效力判定
  ==================================================================================

## 接在什么后面

§11 判掉「从物理层逆向推出范畴层」（依赖图二分：不含常数 ⟹ 零约束力；
含常数 ⟹ 污染），§18 判掉唯一干净入口（钉数值不钉结构）。两条都是**否定**结论。
R-c 是**正向**的一次尝试：不问「能不能逆向」，而问「若物理侧真的给出交织条件
`A_GR · T = T · A_SM`，它能不能把范畴侧的谱不变量钉住」。

## 骨架

设 `n` 维实矩阵 `A`（引力侧 `A_GR`）、`B`（标准模型侧 `A_SM`）、`T`（谱交织）。
抽象为

    Intertwines A B T  :≡  A * T = T * B

若能找到 `S` 使 `T * S = 1` 且 `S * T = 1`（双侧逆），则

    A = T * B * S   ⟹   A.charpoly = B.charpoly  （且 A.trace = B.trace）

这就是「交织 ⟹ 谱相等」的充分性骨架。

## 本模块判什么

| 编号 | 命题 | 判什么 |
|:--|:--|:--|
| ① | 双侧逆 ⟹ `charpoly` 相等（谱完全转移） | 骨架在强假设下确实成立 |
| ② | 双侧逆 ⟹ `trace` 相等 | 骨架的最弱不变量也成立 |
| ③ | 无双侧逆 ⟹ 失效（n=1、`T = 0` 反例） | 逆假设不可省 |
| ④ | ① ∧ ③ 合取 | 骨架是**条件式**，条件即「T 可逆」 |

## 判决（先给）

**骨架成立，但它的前提比「T 存在」更强。**

- ① 成立：只要 `T` 有双侧逆，谱（特征多项式）整体转移。
- ③ 成立：`n = 1`、`A = 1`、`B = 0`、`T = 0`，交织 `1*0 = 0*0` 成立，而 `trace 1 = 1 ≠ 0 = trace 0`。
  故「交织」本身不含逆，不能单独推出任何谱不变量。
- ⇒ 骨架的假设是「`T` 可逆」，而框架内登记的是「`T` 存在」（CONJECTURE，§1 清单 C1）。
  可逆严格强于存在，故骨架的前提**不但未被证，且比待证项更强**。R-c 因此不构成
  「从物理侧推出范畴侧」的通路：它把待证项换成一个更强的待证项。

## 附带结论（与本轮主线一致）

即使骨架完整成立（① 全谱转移），转移到的也只是**特征多项式 / 迹**这类数值型谱不变量；
§18 已证同一数值可有三个结构来源。所以「谱相等」不传递「这是哪个范畴结构」。
R-c 的正向结论与 §11、§18 的否定结论在这一点上收敛：**谱是数值层，结构不在谱里。**

## 诚实边界

1. 用 `Matrix n n ℝ` 而非一般环/一般范畴：ℝ 上 `charpoly_mul_comm` 与 `trace_mul_comm` 直接可用，
   若换到任意交换环需检查 `charpoly` 的系数环假设；本模块不覆盖非交换情形。
2. 「双侧逆」用显式 `S` 表述（`T * S = 1 ∧ S * T = 1`），不用 `IsUnit det` / `A⁻¹`
   的等价形式；两者在本设定下等价（`Matrix.mul_nonsing_inv` 已核存在），但本模块只证显式版。
3. 反例只在 `n = 1`。更高维的反例不需要：判③只需一个反例即可否掉无条件命题。
4. 本模块不新增常数、不新增公设；全部结论为 `calc` + Mathlib 引理，无 `sorry`。
-/

import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

namespace MUFPF.IntertwineSufficiencyAudit

/-- 谱交织条件的抽象形式：`A_GR · T = T · A_SM`。 -/
def Intertwines {n : Type} [Fintype n] [DecidableEq n] (A B T : Matrix n n ℝ) : Prop :=
  A * T = T * B

variable {n : Type} [Fintype n] [DecidableEq n]

/-! =========================================================
    §1 骨架成立：双侧逆 ⟹ 迹相等
   =========================================================
-/

/-- **判②**：双侧逆下，交织推出迹相等。 -/
theorem intertwine_trace_eq (A B T S : Matrix n n ℝ)
    (hTS : T * S = 1) (hST : S * T = 1) (h : Intertwines A B T) :
    A.trace = B.trace := by
  have hEq : A * T = T * B := h
  have hA : A = T * B * S := by
    calc A = A * (T * S) := by rw [hTS, mul_one]
      _ = (A * T) * S := by rw [← mul_assoc]
      _ = (T * B) * S := by rw [hEq]
  rw [hA]
  calc (T * B * S).trace = (S * (T * B)).trace := Matrix.trace_mul_comm (T * B) S
    _ = ((S * T) * B).trace := by rw [← mul_assoc]
    _ = (1 * B).trace := by rw [hST]
    _ = B.trace := by rw [one_mul]

/-! =========================================================
    §2 骨架成立：双侧逆 ⟹ 特征多项式相等（全谱转移）
   =========================================================
-/

/-- **判①**：双侧逆下，交织推出特征多项式相等（谱完全转移）。 -/
theorem intertwine_charpoly_eq (A B T S : Matrix n n ℝ)
    (hTS : T * S = 1) (hST : S * T = 1) (h : Intertwines A B T) :
    A.charpoly = B.charpoly := by
  have hEq : A * T = T * B := h
  have hA : A = T * B * S := by
    calc A = A * (T * S) := by rw [hTS, mul_one]
      _ = (A * T) * S := by rw [← mul_assoc]
      _ = (T * B) * S := by rw [hEq]
  rw [hA]
  calc (T * B * S).charpoly = (S * (T * B)).charpoly := Matrix.charpoly_mul_comm (T * B) S
    _ = ((S * T) * B).charpoly := by rw [← mul_assoc]
    _ = (1 * B).charpoly := by rw [hST]
    _ = B.charpoly := by rw [one_mul]

/-! =========================================================
    §3 逆假设不可省：无双侧逆时骨架失效
   =========================================================
-/

/-- **判③**：反例。`n = 1`，`A = 1`、`B = 0`、`T = 0`：
    交织 `1 * 0 = 0 * 0` 成立，却 `trace 1 = 1 ≠ 0 = trace 0`。
    故「交织」本身不含逆，单独推不出任何谱不变量。 -/
theorem no_inverse_no_trace :
    ∃ (A B T : Matrix (Fin 1) (Fin 1) ℝ), Intertwines A B T ∧ A.trace ≠ B.trace := by
  refine ⟨1, 0, 0, ?_, ?_⟩
  · show (1 : Matrix (Fin 1) (Fin 1) ℝ) * 0 = 0 * (0 : Matrix (Fin 1) (Fin 1) ℝ)
    simp
  · show (1 : Matrix (Fin 1) (Fin 1) ℝ).trace ≠ (0 : Matrix (Fin 1) (Fin 1) ℝ).trace
    norm_num [Matrix.trace_one, Matrix.trace_zero]

/-! =========================================================
    §4 判决汇总
   =========================================================
-/

/-- **判④**：骨架是**条件式**——有双侧逆则全谱转移，无则失效。

    ⇒ 骨架的前提「`T` 可逆」严格强于框架内登记的「`T` 存在」（CONJECTURE），
      故 R-c 不构成从物理侧推出范畴侧的通路：它把待证项换成了更强的待证项。 -/
theorem sufficiency_skeleton_verdict :
    (∀ (m : Type) [Fintype m] [DecidableEq m] (A B T S : Matrix m m ℝ),
      T * S = 1 → S * T = 1 → Intertwines A B T → A.charpoly = B.charpoly) ∧
    (∃ (A B T : Matrix (Fin 1) (Fin 1) ℝ), Intertwines A B T ∧ A.trace ≠ B.trace) :=
  ⟨fun _ _ _ A B T S hTS hST h => intertwine_charpoly_eq A B T S hTS hST h,
   no_inverse_no_trace⟩

end MUFPF.IntertwineSufficiencyAudit
