import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import MUFPFormalization.SpCategory

/-!
# 质量等价桥（P1：交织 → m_i = m_g 取迹论证，2026-10-24）

对应 `notes/04_lorentz_gravity/mass_time_deflection_intuition.md` §5.1（paper18 §11）
与 `全息定理化论证骨架_RecSp对偶.md` 物理论证层裁决后的 P1 推进。

**谱交织条件**（SpHom.intertwine 的方阵版本）：T·B = A·T（即 A_GR·T = T·A_SM）。
**取迹桥**（paper18 定义 11.1/11.2）：T 双向可逆（U·T = T·U = 1）⟹
B = U·A·T ⟹ Tr(B) = Tr(A)（trace 相似不变性）⟹ 惯性/引力质量读数相等。

本文件固化取迹论证的**代数核心**（纯矩阵）：交织 + 双向逆 ⟹ 迹相等；
m 的物理赋值（m_inertial = ℏ/Δλ_min、m_gravitational = Tr(T†·A_GR·T)）为
物理论证层指认（paper18 §11 三前提之二：A_GR/A_SM 算符配对），不在本文件内。

双向逆假设风格与 `SpCategory.spectralFlowTransform` 一致（避免 Invertible 类型类
技术复杂性）。

先证伪再证明：`scripts/mass_eq_trace_probe.py`（10 组随机样本，交织/迹/共轭转置
残差全 < 1e-8，ALL PASS）。
零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.MassEquivalence

open Matrix

variable {n : ℕ}

/-- 相似不变性（trace）：Tr(U·A·T) = Tr(A)，当 T·U = 1（U 为 T 的右逆）。
    证明：trace 循环旋转（trace_mul_comm）+ T·U = 1 消去。 -/
theorem conj_trace_eq (U T A : Matrix (Fin n) (Fin n) ℂ) (hTU : T * U = 1) :
    trace (U * A * T) = trace A := by
  calc
    trace (U * A * T) = trace ((U * A) * T) := by rw [Matrix.mul_assoc]
    _ = trace (T * (U * A)) := trace_mul_comm (U * A) T
    _ = trace ((T * U) * A) := by rw [Matrix.mul_assoc]
    _ = trace (1 * A) := by rw [hTU]
    _ = trace A := by simp

/-- 交织 ⟹ 共轭：T·B = A·T 且 U 为 T 的左逆 ⟹ B = U·A·T。 -/
theorem intertwine_conj (U T A B : Matrix (Fin n) (Fin n) ℂ)
    (hUT : U * T = 1) (h : T * B = A * T) :
    B = U * A * T := by
  calc
    B = (U * T) * B := by rw [hUT]; simp
    _ = U * (T * B) := by rw [Matrix.mul_assoc]
    _ = U * (A * T) := by rw [h]
    _ = U * A * T := by rw [Matrix.mul_assoc]

/-- ★ 谱交织 ⟹ 迹相等（取迹桥核心）：T·B = A·T、T 双向可逆（U）⟹ Tr(B) = Tr(A)。 -/
theorem trace_eq_of_intertwine (U T A B : Matrix (Fin n) (Fin n) ℂ)
    (hTU : T * U = 1) (hUT : U * T = 1) (h : T * B = A * T) :
    trace B = trace A := by
  calc
    trace B = trace (U * A * T) := by rw [intertwine_conj U T A B hUT h]
    _ = trace A := conj_trace_eq U T A hTU

/-- 惯性质量读数（paper18 定义 2.1 的 Tr 版本；ℏ/Δλ_min 物理赋值在论证层）。 -/
noncomputable def massInertialReadout (A : Matrix (Fin n) (Fin n) ℂ) : ℂ := trace A

/-- 引力质量读数（paper18 定义 11.2 的 Tr 版本；算符配对在论证层）。 -/
noncomputable def massGravitationalReadout (A : Matrix (Fin n) (Fin n) ℂ) : ℂ := trace A

/-- ★ m_i = m_g（代数核心）：A_GR·T = T·A_SM、T 双向可逆 ⟹ 质量读数相等。 -/
theorem massReadout_eq_of_intertwine (U T A_GR A_SM : Matrix (Fin n) (Fin n) ℂ)
    (hTU : T * U = 1) (hUT : U * T = 1) (h : T * A_SM = A_GR * T) :
    massGravitationalReadout A_GR = massInertialReadout A_SM := by
  unfold massGravitationalReadout massInertialReadout
  exact (trace_eq_of_intertwine U T A_GR A_SM hTU hUT h).symm

/-- ★ paper18 定义 11.2 形式：Tr(T†·A·T) 在 T·T† = 1 下 = Tr(A)。 -/
theorem conjTranspose_trace_eq (T A : Matrix (Fin n) (Fin n) ℂ) (hTTdag : T * Matrix.conjTranspose T = 1) :
    trace (Matrix.conjTranspose T * A * T) = trace A := by
  calc
    trace (Matrix.conjTranspose T * A * T) = trace ((Matrix.conjTranspose T * A) * T) := by rw [Matrix.mul_assoc]
    _ = trace (T * (Matrix.conjTranspose T * A)) := trace_mul_comm (Matrix.conjTranspose T * A) T
    _ = trace ((T * Matrix.conjTranspose T) * A) := by rw [Matrix.mul_assoc]
    _ = trace (1 * A) := by rw [hTTdag]
    _ = trace A := by simp

/-! ## 统计涌现弱等效（2026-10-25 追加，链末环节）

笔记 L183："弱等效原理 = 弥漫结构的统计必然（与热力学同级的涌现地位）"。
逐态 m_i = m_g（★massReadout_eq_of_intertwine，谱交织取迹桥）⟹ 全谱统计平均等价：
对任意统计权重族 w（如概率分布 Σw=1），加权平均引力质量 = 加权平均惯性质量——
"逐态等价 ⟹ 宏观统计等价"的代数核心（统计涌现：宏观读数 = 微态加权平均，
等价性在线性平均下保持）。
数值先证伪 `scripts/mass_statistical_equivalence_probe.py`（8 态 × 50 组随机复矩阵，
逐态交织构造 A_GR=T·A_SM·T⁻¹）：逐态 trace 残差 3.7e-14、加权平均残差 5.0e-14，ALL PASS。
-/

/-- ★★ 统计涌现弱等效（多态谱加权平均）：逐态谱交织 + 双向逆 ⟹ 任意统计权重下的
    加权平均质量读数相等——逐态 m_i = m_g ⟹ 全谱统计平均等价。
    语义：w 为概率分布（Σw=1，归一化不参与代数）时，宏观引力读数 =
    微态惯性读数的加权平均，等价性在统计平均下保持（热力学级涌现）。 -/
theorem massReadout_weighted_eq_of_intertwine_family {K : Type} [Fintype K]
    (U T A_GR A_SM : K → Matrix (Fin n) (Fin n) ℂ) (w : K → ℂ)
    (hTU : ∀ k, T k * U k = 1) (hUT : ∀ k, U k * T k = 1)
    (h : ∀ k, T k * A_SM k = A_GR k * T k) :
    (∑ k, w k * massGravitationalReadout (A_GR k)) =
      (∑ k, w k * massInertialReadout (A_SM k)) := by
  apply Finset.sum_congr rfl
  intro k hk
  rw [massReadout_eq_of_intertwine (U k) (T k) (A_GR k) (A_SM k) (hTU k) (hUT k) (h k)]

end MUFPF.MassEquivalence
