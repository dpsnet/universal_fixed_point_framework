/-
  QuotientBridgeAudit.lean — R-h：救桥的其余路线穷尽（商掉核 / 换不变量 / 换载体）
  =====================================================================================

## 接在什么后面

第 74 批（R-g，`IntertwinerRepairAudit`）判：把登记改成「`∃ T` 可逆 ∧ 交织」是循环，
框架谱隙实例上该登记为假；平均型 `T` 秩 2/4，结构性不可逆。
但那只是**一条**修补方向。本批判其余三条：

| 路线 | 主张 | 判什么 |
|:--|:--|:--|
| R-h1 商掉核 | 不要逆，只要「在商空间上诱导相等」——`T` 的核被商掉后可留信息 | 商上到底能传几个标量？框架实例传得动吗？ |
| R-h2 换不变量 | 迹要相等太强，换 `det`（或特征多项式）就绕开 | `det` 是否同样被前提吞掉 |
| R-h3 换载体 | 不比算子，比不变量子空间（子空间格） | 谱不交时公共不变量子空间是否只剩平凡两项 |

## 判决（本模块机检 R-h1、R-h2、R-h3 三条路线）

- **R-h1 商桥**：`groupAverage` 的商像只有 **2 个坐标**——`(迹, 旋度)`，其中旋度 = `T₀₁ − T₁₀`。
  所以任何「用平均类 T 做桥」的方案**最多传 2 个标量**（信息上界 2 实参数）。
  而框架谱隙实例 `diag(0,2)` / `diag(1, 1+Δλ_min)` 两侧旋度均为 0、迹差 `Δλ_min > 0`
  ⟹ 商像不等 ⟹ **商桥在框架实例上仍然失败**。
- **R-h2 换不变量**：`det` 与 `trace` 被同一个前提同时吞掉（可逆交织 ⟹ 两者皆相等），
  2×2 下迹 + 行列式决定特征多项式 ⟹ 换任何不变量都是同一处循环。
- **R-h3 换载体**：公共一维不变量子空间**存在**（`y` 轴，两侧都把它映成自己的倍数），
  但其上的标值 2 与 1+Δλ_min **不同** ⟹ 子空间格相同、标值不同：
  换载体只能传「结构」，不能传「数值」——正是 §18「钉数值不钉结构」的镜像。
- **R-h1 的正面价值**：这不是空判——它给出了「桥的可达信息维数」这一新量：
  核的精确刻画 `groupAverage T = 0 ↔ tr T = 0 ∧ T₀₁ = T₁₀` 说明商维数恰为 2，
  于是「桥最多能传什么」变成可数结论，而不再是笼统的「无信息」。

## 诚实边界

1. 商空间不引入 `Submodule.Quotient` 类型，直接用「像相等 ⟺ 两个坐标相等」机检
   （2 维情形下等价），不新建函子层。
2. R-h3 只机检「存在一个公共一维不变量子空间 + 其上标值不同」这一对陈述，
   不刻画「全部公共不变子空间格」（那需要子空间格/平行判据，属标准二维线性代数，本模块不引入）。
3. 2×2 下「迹 + 行列式决定特征多项式」不形式化（不新增多项式依赖）。
4. 不新增常数、不新增公设；`Δλ_min` 只引用 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.IntertwinerRepairAudit
import Mathlib.Tactic

namespace MUFPF.QuotientBridgeAudit

open MUFPF.Isotropy
open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.IntertwinerRepairAudit (rotGen offDiag)
open MUFPF.IntertwinerRepairAudit (groupAverage_general_form groupAverage_F_zero'
  groupAverage_offDiag_zero F_ne_offDiag)

/-! ## R-h1 判①：商的基底无关——`1` 与 `rotGen` 线性无关（故商恰 2 维） -/

/-- **`1` 与 `A = !![0,1;−1,0]` 线性无关**：`1` 不是 `A` 的标量倍（(0,0) 条目 1 vs 0）。
    这是「商像恰 2 维」的基底条件：`groupAverage T` 的两个系数因此唯一。 -/
theorem one_rotGen_indep :
    ¬ ∃ c : ℝ, (1 : Matrix (Fin 2) (Fin 2) ℝ) = c • rotGen := by
  rintro ⟨c, h⟩
  have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
  simp [rotGen, Matrix.smul_apply] at h00

/-! ## R-h1 判②：核的精确刻画 —— 核 = 对称无迹（2 维） -/

/-- ★★ **判②**：`groupAverage T = 0 ⟺ trace T = 0 ∧ T₀₁ = T₁₀`。
    即核恰是**对称无迹**子空间（`F = diag(1,−1)` 与 `S = !![0,1;1,0]` 张成），维数 2。 -/
theorem groupAverage_eq_zero_iff (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage T = 0 ↔ T 0 0 + T 1 1 = 0 ∧ T 0 1 = T 1 0 := by
  constructor
  · intro h
    have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
    have h01 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    rw [groupAverage_general_form T] at h00 h01
    simp [rotGen, Matrix.add_apply, Matrix.smul_apply, Matrix.zero_apply] at h00 h01
    exact ⟨by linarith, by linarith⟩
  · rintro ⟨h1, h2⟩
    have ha : (T 0 0 + T 1 1) / 2 = 0 := by linarith
    have hb : (T 0 1 - T 1 0) / 2 = 0 := by linarith
    rw [groupAverage_general_form T, ha, hb]
    simp

/-! ## R-h1 判③：商上至多 2 个坐标（信息上界） -/

/-- ★★ **判③**：两个矩阵在商上同像 ⟹ 它们的两个坐标（迹和、旋度）逐一相等。
    故「用平均类 `T` 做桥」**最多传递 2 个实标量**——这是桥的可达信息维数上界。 -/
theorem groupAverage_coords_of_eq (T T' : Matrix (Fin 2) (Fin 2) ℝ)
    (h : groupAverage T = groupAverage T') :
    T 0 0 + T 1 1 = T' 0 0 + T' 1 1 ∧ T 0 1 - T 1 0 = T' 0 1 - T' 1 0 := by
  have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
  have h01 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
  rw [groupAverage_general_form T, groupAverage_general_form T'] at h00 h01
  simp [rotGen, Matrix.add_apply, Matrix.smul_apply] at h00 h01
  exact ⟨by linarith, by linarith⟩

/-- **判③ 的反向**：两个坐标逐一同 ⟹ 商像相同。合起来即「商上恰 2 个自由度」。 -/
theorem eq_of_coords_eq (T T' : Matrix (Fin 2) (Fin 2) ℝ)
    (h1 : T 0 0 + T 1 1 = T' 0 0 + T' 1 1) (h2 : T 0 1 - T 1 0 = T' 0 1 - T' 1 0) :
    groupAverage T = groupAverage T' := by
  have ha : (T 0 0 + T 1 1) / 2 = (T' 0 0 + T' 1 1) / 2 := by linarith
  have hb : (T 0 1 - T 1 0) / 2 = (T' 0 1 - T' 1 0) / 2 := by linarith
  rw [groupAverage_general_form T, groupAverage_general_form T', ha, hb]

/-! ## R-h1 判④：框架谱隙实例上，商像仍然不等 -/

/-- ★★ **判④**：`groupAverage (diag(0,2)) ≠ groupAverage (diag(1, 1+Δλ_min))`。
    两侧旋度均为 0（对角），迹各为 `2` 与 `2 + Δλ_min` ⟹ 商上第 1 坐标即不等 ⟹ **商桥不成立**。 -/
theorem framework_quotient_still_fails :
    groupAverage (diag2 0 2) ≠ groupAverage (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) := by
  intro h
  have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
  rw [groupAverage_general_form (diag2 0 2),
    groupAverage_general_form (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))] at h00
  simp [diag2, rotGen, Matrix.add_apply, Matrix.smul_apply] at h00
  linarith [MUFPF.GNBridgeAudit.dlmin_pos]

/-! ## R-h2：换不变量（det）同样被前提吞掉 -/

/-- ★★ **判⑤**：`T` 双侧可逆且 `T·B = A·T` ⟹ `det B = det A`。
    证明：`B = U·A·T` ⟹ `det B = det U · det A · det T = (det U · det T)·det A = det(U·T)·det A = det A`。 -/
theorem det_eq_of_invertible_intertwine_real {A B T U : Matrix (Fin 2) (Fin 2) ℝ}
    (_hTU : T * U = 1) (hUT : U * T = 1) (h : T * B = A * T) :
    Matrix.det B = Matrix.det A := by
  have hB : B = U * A * T := by
    calc B = 1 * B := by simp
      _ = (U * T) * B := by rw [hUT]
      _ = U * (T * B) := by rw [Matrix.mul_assoc]
      _ = U * (A * T) := by rw [h]
      _ = U * A * T := by rw [Matrix.mul_assoc]
  have hd : Matrix.det U * Matrix.det T = 1 := by
    rw [← Matrix.det_mul, hUT, Matrix.det_one]
  rw [hB, Matrix.det_mul, Matrix.det_mul]
  calc Matrix.det U * Matrix.det A * Matrix.det T
      = (Matrix.det U * Matrix.det T) * Matrix.det A := by ring
    _ = 1 * Matrix.det A := by rw [hd]
    _ = Matrix.det A := one_mul _

/-- ★★ **判⑥ 换不变量全部无效**：可逆交织同时吞掉 `det` 与 `trace`（2×2 下二者决定特征多项式）⟹
    「换一个不变量当桥」不是新路，而是同一处循环的另一种写法。 -/
theorem invariant_swap_circular {A B T U : Matrix (Fin 2) (Fin 2) ℝ}
    (hTU : T * U = 1) (hUT : U * T = 1) (h : T * B = A * T) :
    Matrix.det B = Matrix.det A ∧ Matrix.trace B = Matrix.trace A :=
  ⟨det_eq_of_invertible_intertwine_real hTU hUT h,
   MUFPF.IntertwinerRepairAudit.trace_eq_of_invertible_intertwine_real hTU hUT h⟩
/-! ## R-h3：换载体（不变量子空间）—— 钉结构，不钉数值 -/

/-- 列向量 `w = ![0;1]`（`y` 轴方向）。 -/
def yAxis : Matrix (Fin 2) (Fin 1) ℝ := !![(0 : ℝ); 1]

/-- `w ≠ 0`。 -/
theorem yAxis_ne_zero : yAxis ≠ 0 := by
  intro h
  have h1 := congrArg (fun M : Matrix (Fin 2) (Fin 1) ℝ => M 1 0) h
  simp [yAxis] at h1

/-- ★★ **判⑦**：框架谱隙实例的**公共一维不变量子空间存在**——
    `diag(0,2) · w = 2 • w` 且 `diag(1, 1+Δλ_min) · w = (1+Δλ_min) • w`，`w = ![0;1] ≠ 0`。
    即：换载体（比不变量子空间）不比算子弱，子空间层面的「对应」确实存在。 -/
theorem common_invariant_yAxis :
    diag2 0 2 * yAxis = (2 : ℝ) • yAxis ∧
      diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin) * yAxis =
        (1 + MUFPF.GNBridgeAudit.dlmin) • yAxis := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [diag2, yAxis, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply]
  · ext i j
    fin_cases i <;> fin_cases j <;>
        simp [diag2, yAxis, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply]

/-- ★★ **判⑧**：同一公共不变量子空间上的**标值不同**：`2 ≠ 1 + Δλ_min`。
    与判⑦ 合起来：子空间格相同、标值不同 ⟹ 换载体只能传「结构」，不能传「数值」。
    这正是 §18「钉数值不钉结构」的镜像命题。 -/
theorem eigenvalue_on_common_subspace_differs :
    (2 : ℝ) ≠ 1 + MUFPF.GNBridgeAudit.dlmin := by
  intro h
  have h1 : MUFPF.GNBridgeAudit.dlmin < 1 :=
    MUFPF.IntertwinerExistenceAudit.dlmin_in_unit_interval.2
  linarith

/-! ## 汇总判决 -/

/-- **R-h 判决汇总**：
    ① `1` 与 `A` 线性无关 ⟹ 商像的坐标唯一（商恰 2 维）；
    ② 核 = 对称无迹（`groupAverage T = 0 ⟺ tr T = 0 ∧ T₀₁ = T₁₀`）；
    ③ 商上同像 ⟹ 两个坐标逐一相等（且反之），即**可达信息 ≤ 2 标量**；
    ④ 框架谱隙实例商像不等 ⟹ 商桥不成立；
    ⑤⑥ `det` 与 `trace` 被同一前提同时吞掉 ⟹ 换不变量无效。 -/
theorem quotient_route_verdict :
    (¬ ∃ c : ℝ, (1 : Matrix (Fin 2) (Fin 2) ℝ) = c • rotGen) ∧
      (groupAverage (diag2 0 2) ≠
        groupAverage (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) ∧
      (∀ T T' : Matrix (Fin 2) (Fin 2) ℝ, groupAverage T = groupAverage T' →
          T 0 0 + T 1 1 = T' 0 0 + T' 1 1 ∧ T 0 1 - T 1 0 = T' 0 1 - T' 1 0) ∧
      (∀ T : Matrix (Fin 2) (Fin 2) ℝ,
          groupAverage T = 0 ↔ T 0 0 + T 1 1 = 0 ∧ T 0 1 = T 1 0) ∧
      (yAxis ≠ 0 ∧
        diag2 0 2 * yAxis = (2 : ℝ) • yAxis ∧
        (2 : ℝ) ≠ 1 + MUFPF.GNBridgeAudit.dlmin) :=
  ⟨one_rotGen_indep, framework_quotient_still_fails, groupAverage_coords_of_eq,
    groupAverage_eq_zero_iff,
    ⟨yAxis_ne_zero, (common_invariant_yAxis).1, eigenvalue_on_common_subspace_differs⟩⟩

end MUFPF.QuotientBridgeAudit
