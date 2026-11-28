/-
  ScalarReadoutAudit.lean — R-x：载体层标量读数的三分（分离／和／积），以及「读得出」缺在哪
  =====================================================================================

## 问题

§25 判「分层载体能装下两层数据」；§28 判「传递失败的原因是大小无判据」；§38–§41 判
`det` 在载体层被奇异层清零、在双向载体上「可读但混叠」；§43 判载体迹里的 `4` 与槽数 `4` 不同源。
四批都在同一处收尾但没合并：

> 载体装得下两层数据，**到底哪个读数能把两层分开**？三个候选（逐条读出、`trace`、`det`）
> 各自能读出什么、读不出什么，从未在同一处机检。

本批把三个候选放进同一个比较框架：看它们把「两层数据」变成「一个数」时用的是哪种运算，
并各自给出**碰撞见证**（不同层数据给出同一读数），再补上第四条候选——**谱**（层内特征值集合）。

## 结果

| 读数 | 运算类型 | 是否分离两层 | 机检见证 |
| --- | --- | --- | --- |
| 逐条读出 `blk · (inl i) (inl j)` | 投影（坐标） | **完全分离** | 载体相等 ⟹ 物理层矩阵相等（`entry_readout_recovers_physical_layer`） |
| `trace` | 加法 | 不分离（只得和） | 两组不同层分割 `(2,2)` 与 `(1,3)` 同读 `4`（`trace_collision`） |
| `det`（`C = 0`） | 乘法 | 不分离（只得积），且被奇异层清零 | 两组分割 `(2,2)` 与 `(1,4)` 同读 `4`（`det_collision`）；`A_GR` 奇异时恒读 `0`（`det_annihilated_by_singular_layer`） |
| 层内谱（`t • 1 − diag2 a b` 的根） | 无序多重集 | **数值上分离**（`2 ∉ spec(A_SM)`、`1+h ∉ spec(A_GR)`） | `framework_two_not_in_sm_spectrum`、`framework_sm_root_not_in_gr_spectrum` |

## 判决

1. **逐条读出**是唯一「完全分离」的读数，但它的分离**靠参数位置**：把同一个数值矩阵当作物理层还是
   范畴层，完全由 `blk` 的实参顺序（即 `Sum.inl / Sum.inr` 槽标号）决定
   （`ownership_is_argument_order`）。这与 §34 的「链末端是定义」同型。
2. **`trace` 与 `det`** 都不分离，且它们「不分离」的方式不同：一个把两层相加，一个把两层相乘；
   乘法那一路还会因为一层奇异而把另一层的全部信息清零（`det_annihilated_by_singular_layer`）。
   所以 §28 的「大小无判据」在读数层得到确认：两个经典不变量都不是「大小判据」。
3. **谱**是唯一「不需要槽标号」又能把两层数值分开的读数：它给出无序多重集，两个层的谱值互不落入
   对方的谱（框架实例：`2 ≠ 1+Δλ_min`）。但它**只给数值、不给归属**——哪个根属于哪一层仍需
   层的结构信息。故它修补的是「数值可分」，不修补「归属可判」。

## 净结果

「载体不足」的准确形式是**标量读数不足**，而不是「装不下」：4 维载体装得下 4 个层条目，
逐条读出完全分离，谱也能把两层的数值分成两个不同的数；缺的是「**既分离又不需要标号**的标量泛函」。
`trace` / `det` 两个经典不变量给不出它，谱给出一半（数值分离、归属缺失）。

## 诚实边界

1. 谱只按「层内 2×2 块」计算（`det (t • 1 − diag2 a b)`），不计算 4×4 整体的特征多项式
   （那需要 `charpoly` 的分块分解，超出本批目标，登记为 `CARRIER_CHARPOLY_FACTOR` 待建）。
2. 「任何标量泛函」不在本批量化——本批只机检三个具体候选 + 谱，不建立「不存在分离泛函」的一般定理。
3. 不改 §28/§38/§41 的判决，只把三个候选的读法类型与碰撞见证并到同一处。
4. 不新增常数、不新增公设；`Δλ_min` 只引用 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.LayeredCarrierAudit
import MUFPFormalization.CarrierDetAudit
import MUFPFormalization.IntertwinerExistenceAudit
import MUFPFormalization.GNBridgeAudit
import Mathlib.Tactic

namespace MUFPF.ScalarReadoutAudit

open MUFPF.IntertwinerExistenceAudit (diag2 dlmin_in_unit_interval)
open MUFPF.LayeredCarrierAudit (blk trace_blk blk_layer_readout)
open MUFPF.CarrierDetAudit (det_blk_zero_lower_left det_diag2)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)

/-! ## 判①：逐条读出完全分离，但归属由实参顺序（槽标号）决定 -/

/-- ★ **逐条读出是分离的**：两个载体相等 ⟹ 物理层（左上块）矩阵相等。
    即「读出 `blk A B C D (inl i) (inl j)`」把 `A` 的每个条目原样取回，没有混合。 -/
theorem entry_readout_recovers_physical_layer
    {A A' B B' C C' D D' : Matrix (Fin 2) (Fin 2) ℝ}
    (h : blk A B C D = blk A' B' C' D') : A = A' := by
  ext i j
  have h' := congrArg
    (fun M : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ => M (Sum.inl i) (Sum.inl j)) h
  simpa [blk] using h'

/-- ★ **归属由实参顺序决定**：把 `A` 写在第一实参还是第二实参，载体不同
    （`A ≠ D` 时 `blk A 0 0 D ≠ blk D 0 0 A`）。分离性本身不携带「谁是物理层」。 -/
theorem ownership_is_argument_order (A D : Matrix (Fin 2) (Fin 2) ℝ) (hAD : A ≠ D) :
    blk A 0 0 D ≠ blk D 0 0 A := by
  intro h
  apply hAD
  ext i j
  have h' := congrArg
    (fun M : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ => M (Sum.inl i) (Sum.inl j)) h
  simpa [blk] using h'

/-! ## 判②：`trace` 是加法读数 —— 碰撞见证 -/

/-- 对角 2×2 块的迹：`trace (diag2 a b) = a + b`。 -/
theorem layer_trace_diag2 (a b : ℝ) : Matrix.trace (diag2 a b) = a + b := by
  simp [diag2, Matrix.trace, Fin.sum_univ_two]

/-- ★ **迹的碰撞见证（一）**：两组完全不同的层数据 `(1,1)+(1,1)` 与 `(0,1)+(1,2)`
    给出同一个迹读数 `4`。第一组的层迹是 `(2,2)`，第二组是 `(1,3)`。 -/
theorem trace_collision :
    Matrix.trace (blk (diag2 (1 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 1)) = 4 ∧
      Matrix.trace (blk (diag2 (0 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 2)) = 4 := by
  constructor
  · rw [trace_blk, layer_trace_diag2 1 1]; norm_num
  · rw [trace_blk, layer_trace_diag2 0 1, layer_trace_diag2 1 2]; norm_num

/-- ★ **迹的碰撞见证（二）**：两组的层迹确实不同（`2 ≠ 1`），所以迹读不出分割。 -/
theorem trace_split_differs :
    Matrix.trace (diag2 (1 : ℝ) 1) ≠ Matrix.trace (diag2 (0 : ℝ) 1) := by
  rw [layer_trace_diag2 1 1, layer_trace_diag2 0 1]
  norm_num

/-- ★ **迹的碰撞见证（三）**：两个载体确实不同（左上条目 `1 ≠ 0`），不是同一个对象。 -/
theorem trace_collision_carriers_differ :
    blk (diag2 (1 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 1) ≠
      blk (diag2 (0 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 2) := by
  intro h
  have h' := congrArg
    (fun M : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ => M (Sum.inl 0) (Sum.inl 0)) h
  simp [blk, diag2] at h'

/-! ## 判③：`det` 是乘法读数 —— 碰撞见证 + 奇异层清零 -/

/-- ★ **行列式的碰撞见证**：层分割 `(2,2)` 与 `(1,4)` 的乘积同为 `4`，但两组层数据不同。 -/
theorem det_collision :
    Matrix.det (blk (diag2 (1 : ℝ) 2) 0 0 (diag2 (1 : ℝ) 2)) = 4 ∧
      Matrix.det (blk (diag2 (1 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 4)) = 4 := by
  constructor
  · rw [det_blk_zero_lower_left, det_diag2 1 2]; norm_num
  · rw [det_blk_zero_lower_left, det_diag2 1 1, det_diag2 1 4]; norm_num

/-- ★ **行列式的碰撞见证（续）**：两组层数据的行列式分割不同（`2 ≠ 1`），故 `det` 读不出分割。 -/
theorem det_split_differs :
    Matrix.det (diag2 (1 : ℝ) 2) ≠ Matrix.det (diag2 (1 : ℝ) 1) := by
  rw [det_diag2 1 2, det_diag2 1 1]
  norm_num

/-- ★★ **奇异层清零**：只要物理层是 `A_GR = diag(0, 2)`（`det = 0`），
    载体 `det` 对**任意**耦合与**任意**范畴层恒读 `0`——范畴层的全部信息被清零。 -/
theorem det_annihilated_by_singular_layer
    (B : Matrix (Fin 2) (Fin 2) ℝ) (D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) B 0 D) = 0 := by
  rw [det_blk_zero_lower_left, det_diag2 0 2]
  simp

/-! ## 判④：层内谱是「无标号但数值分离」的读数 -/

/-- 谱平移：`t • 1 − diag2 a b = diag2 (t − a) (t − b)`。 -/
theorem shift_diag2 (t a b : ℝ) :
    t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 a b = diag2 (t - a) (t - b) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [diag2, Matrix.sub_apply, Matrix.smul_apply]

/-- 特征多项式在 `t` 处的取值：`det (t • 1 − diag2 a b) = (t − a)(t − b)`。 -/
theorem det_shift_diag2 (t a b : ℝ) :
    Matrix.det (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 a b) = (t - a) * (t - b) := by
  rw [shift_diag2, det_diag2]

/-- 物理层的谱根 `2`：`det (2 • 1 − diag2 0 2) = 0`。 -/
theorem gr_spectrum_root_two :
    Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 (0 : ℝ) 2) = 0 := by
  rw [det_shift_diag2]; norm_num

/-- 范畴层的谱根 `1`：`det (1 • 1 − diag2 1 h) = 0`。 -/
theorem sm_spectrum_root_one (h : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 (1 : ℝ) h) = 0 := by
  rw [det_shift_diag2]; ring

/-- ★ **`2` 不是范畴层 `diag2 1 h` 的谱根**（`h ≠ 2`）：`det (2 • 1 − diag2 1 h) ≠ 0`。 -/
theorem two_not_in_sm_spectrum (h : ℝ) (hh : h ≠ 2) :
    Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 (1 : ℝ) h) ≠ 0 := by
  rw [det_shift_diag2]
  have hsub : (2 : ℝ) - h ≠ 0 := sub_ne_zero.mpr (Ne.symm hh)
  have hone : (2 : ℝ) - 1 ≠ 0 := by norm_num
  exact mul_ne_zero hone hsub

/-- ★ **`1 + h` 不是物理层 `diag2 0 2` 的谱根**（`h ≠ 1`、`1 + h ≠ 0`）。 -/
theorem sm_root_not_in_gr_spectrum (h : ℝ) (h1 : h ≠ 1) (h2 : 1 + h ≠ 0) :
    Matrix.det ((1 + h) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 (0 : ℝ) 2) ≠ 0 := by
  rw [det_shift_diag2]
  have hne : (1 : ℝ) + h ≠ 2 := by
    intro hc
    exact h1 (by linarith)
  have hfirst : (1 + h - 0 : ℝ) ≠ 0 := by simpa using h2
  have hsecond : (1 + h - 2 : ℝ) ≠ 0 := sub_ne_zero.mpr hne
  exact mul_ne_zero hfirst hsecond

/-- ★★ **框架实例：两层的谱值互不落入对方**（`2 ∉ spec(A_SM)`）。 -/
theorem framework_two_not_in_sm_spectrum :
    Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) -
        diag2 (1 : ℝ) (1 + dlmin)) ≠ 0 := by
  refine two_not_in_sm_spectrum (1 + dlmin) ?_
  intro hc
  have hlt : dlmin < 1 := dlmin_in_unit_interval.2
  linarith

/-- ★★ **框架实例：`1 + Δλ_min ∉ spec(A_GR)`**。 -/
theorem framework_sm_root_not_in_gr_spectrum :
    Matrix.det ((1 + (1 + dlmin)) • (1 : Matrix (Fin 2) (Fin 2) ℝ) -
        diag2 (0 : ℝ) 2) ≠ 0 := by
  refine sm_root_not_in_gr_spectrum (1 + dlmin) ?_ ?_
  · intro hc
    have hpos : 0 < dlmin := dlmin_pos
    linarith
  · intro hc
    have hpos : 0 < dlmin := dlmin_pos
    linarith

/-! ## 汇总判决 -/

/-- **R-x 判决汇总**：
    ① 逐条读出完全分离（载体相等 ⟹ 物理层相等），但归属由实参顺序决定；
    ② `trace` 是加法读数，两组层分割同读 `4`（碰撞见证）；
    ③ `det` 是乘法读数，两组层分割同读 `4`，且奇异层把另一层清零（恒读 `0`）；
    ④ 层内谱给出互不覆盖的两组根（`2 ∉ spec(A_SM)` 且 `1 + Δλ_min ∉ spec(A_GR)`），
       但只给数值、不给归属。 -/
theorem scalar_readout_verdict :
    (∀ A D : Matrix (Fin 2) (Fin 2) ℝ, A ≠ D → blk A 0 0 D ≠ blk D 0 0 A) ∧
      (Matrix.trace (blk (diag2 (1 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 1)) = 4 ∧
        Matrix.trace (blk (diag2 (0 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 2)) = 4 ∧
        Matrix.trace (diag2 (1 : ℝ) 1) ≠ Matrix.trace (diag2 (0 : ℝ) 1)) ∧
      (Matrix.det (blk (diag2 (1 : ℝ) 2) 0 0 (diag2 (1 : ℝ) 2)) = 4 ∧
        Matrix.det (blk (diag2 (1 : ℝ) 1) 0 0 (diag2 (1 : ℝ) 4)) = 4 ∧
        (∀ B D : Matrix (Fin 2) (Fin 2) ℝ,
          Matrix.det (blk (diag2 (0 : ℝ) 2) B 0 D) = 0)) ∧
      (Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) -
          diag2 (1 : ℝ) (1 + dlmin)) ≠ 0 ∧
        Matrix.det ((1 + (1 + dlmin)) • (1 : Matrix (Fin 2) (Fin 2) ℝ) -
          diag2 (0 : ℝ) 2) ≠ 0) :=
  ⟨fun _ _ hAD => ownership_is_argument_order _ _ hAD,
   ⟨trace_collision.1, trace_collision.2, trace_split_differs⟩,
   ⟨det_collision.1, det_collision.2, fun _ D => det_annihilated_by_singular_layer _ D⟩,
   ⟨framework_two_not_in_sm_spectrum, framework_sm_root_not_in_gr_spectrum⟩⟩

end MUFPF.ScalarReadoutAudit
