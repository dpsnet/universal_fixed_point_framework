import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.LinearAlgebra.Matrix.PosDef
import MUFPFormalization.Clifford

-- fin_cases 分支相同操作时 linter 误报（unnecessarySeqFocus）；部分分支被 simp 闭合时
-- ring/abel 仅服务剩余分支（unusedTactic/unreachableTactic 误报），关闭该风格检查
set_option linter.unnecessarySeqFocus false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

open Matrix

namespace MUFPF.Isotropy

/-!
## 强制平均各向同性（§7.6① 机检化）

笔记 `mass_time_deflection_intuition.md` §7.6①："强制平均（O(n) 等变）⟹ 各向同性 ⟹
全方向偏转代价相等（m_i = m_g ⟺ 谱交织 ⟺ 等效原理各向同性版）"，且自标
"三项形式化待证之一"（边界①：前提 = 强制平均等变）。

本模块闭合其数学核心（对称张量/代价度量版）：
  ★ groupAverage_isotropy：C₄ 等变平均（群平均实现）作用于对称张量 ⟹ λI（各向同性）；
  ★ isotropy_of_rotation_invariant_symmetric：任意旋转不变的对称张量 ⟹ λI
    （各向同性张量的唯一形式，Schur/单参数计算）。
数值先证伪 `scripts/force_average_isotropy_probe.py`：对称 T 10 组 λI 残差 <1e-16 ALL PASS；
一般 T ⟹ λI + μJ（对称前提的必要性，证伪捕获边界）。
-/

/-- SO(2) 旋转矩阵 rot θ = [[cosθ, -sinθ; sinθ, cosθ]]。 -/
noncomputable def rot (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, -Real.sin θ; Real.sin θ, Real.cos θ]

/-- 旋转的正交性：(rot θ)ᵀ · rot θ = 1。 -/
theorem rot_orthogonal (θ : ℝ) : (rot θ)ᵀ * rot θ = 1 := by
  rw [show (rot θ)ᵀ = !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ] by
    ext i j <;> fin_cases i <;> fin_cases j <;> rfl]
  rw [show rot θ = !![Real.cos θ, -Real.sin θ; Real.sin θ, Real.cos θ] by rfl]
  rw [Matrix.mul_fin_two]
  ext i j; fin_cases i <;> fin_cases j <;> simp
  · nlinarith [Real.sin_sq_add_cos_sq θ]
  · ring
  · ring
  · nlinarith [Real.sin_sq_add_cos_sq θ]

/-- C₄ 旋转四元：{R0, R1, R2, R3} = rot(0, π/2, π, −π/2)。 -/
noncomputable def R0 : Matrix (Fin 2) (Fin 2) ℝ := rot 0
noncomputable def R1 : Matrix (Fin 2) (Fin 2) ℝ := rot (Real.pi / 2)
noncomputable def R2 : Matrix (Fin 2) (Fin 2) ℝ := rot Real.pi
noncomputable def R3 : Matrix (Fin 2) (Fin 2) ℝ := rot (-(Real.pi / 2))

theorem R0_eq_one : R0 = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [R0, rot, Real.cos_zero, Real.sin_zero]

theorem R2_eq_neg_one : R2 = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [R2, rot, Real.cos_pi, Real.sin_pi]

theorem R1_transpose : (R1)ᵀ = R3 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [R1, R3, rot, Real.cos_pi_div_two,
    Real.sin_pi_div_two, Real.cos_neg, Real.sin_neg]

theorem R2_transpose : (R2)ᵀ = R2 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [R2, rot, Real.cos_pi, Real.sin_pi]

theorem R3_transpose : (R3)ᵀ = R1 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [R3, R1, rot, Real.cos_pi_div_two,
    Real.sin_pi_div_two, Real.cos_neg, Real.sin_neg]

/-- C₄ 群平均（强制平均 = 等变平均的离散实现）。 -/
noncomputable def groupAverage (T : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  (1 / 4 : ℝ) • (R0 * T * (R0)ᵀ + R1 * T * (R1)ᵀ + R2 * T * (R2)ᵀ + R3 * T * (R3)ᵀ)

/-- ★★ 强制平均各向同性（离散实现）：对称张量（代价/度量）的 C₄ 等变平均 ⟹ λI。
    对应笔记 §7.6① "强制平均（O(n) 等变）⟹ 各向同性"。 -/
theorem groupAverage_isotropy {T : Matrix (Fin 2) (Fin 2) ℝ} (hsym : Tᵀ = T) :
    groupAverage T = (((T 0 0 + T 1 1) / 2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ)) := by
  have h01 : T 0 1 = T 1 0 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 0) hsym
    simpa [Matrix.transpose] using h
  have hc0 : R0 * T * (R0)ᵀ = T := by
    rw [R0_eq_one]
    simp
  have hc2 : R2 * T * (R2)ᵀ = T := by
    rw [R2_eq_neg_one]
    simp
  have hc1 : R1 * T * (R1)ᵀ = !![T 1 1, -(T 1 0); -(T 0 1), T 0 0] := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [R1, rot, Real.cos_pi_div_two,
      Real.sin_pi_div_two, Matrix.mul_apply, Matrix.vecMul, Fin.sum_univ_two]
    all_goals rfl
  have hc3 : R3 * T * (R3)ᵀ = !![T 1 1, -(T 1 0); -(T 0 1), T 0 0] := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [R3, rot, Real.cos_pi_div_two,
      Real.sin_pi_div_two, Real.cos_neg, Real.sin_neg, Matrix.mul_apply, Matrix.vecMul,
      Fin.sum_univ_two]
    all_goals rfl
  rw [groupAverage]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [hc0, hc1, hc2, hc3, h01]
  all_goals field_simp
  all_goals ring

/-- ★★ 各向同性张量的唯一形式：任意旋转不变的对称张量 ⟹ λI（连续 SO(2) 版）。
    单参数计算：取特例 θ = π/2 代入旋转不变等式，解出对角相等、非对角为零。 -/
theorem isotropy_of_rotation_invariant_symmetric {A : Matrix (Fin 2) (Fin 2) ℝ}
    (hrot : ∀ θ : ℝ, rot θ * A * (rot θ)ᵀ = A) (hsym : Aᵀ = A) :
    A = (A 0 0 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  have h01 : A 0 1 = A 1 0 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 0) hsym
    simpa [Matrix.transpose] using h
  have hπ2 : rot (Real.pi / 2) * A * (rot (Real.pi / 2))ᵀ = A := hrot (Real.pi / 2)
  have hdiag : A 0 0 = A 1 1 := by
    calc
      A 0 0 = (rot (Real.pi / 2) * A * (rot (Real.pi / 2))ᵀ) 0 0 := by rw [hπ2]
      _ = A 1 1 := by
        simp [rot, Real.cos_pi_div_two, Real.sin_pi_div_two, Matrix.mul_apply,
          Matrix.vecMul, Fin.sum_univ_two]
        rfl
  have h01neg : A 0 1 = -(A 1 0) := by
    calc
      A 0 1 = (rot (Real.pi / 2) * A * (rot (Real.pi / 2))ᵀ) 0 1 := by rw [hπ2]
      _ = -(A 1 0) := by
        simp [rot, Real.cos_pi_div_two, Real.sin_pi_div_two, Matrix.mul_apply,
          Matrix.vecMul, Fin.sum_univ_two]
        rfl
  have h01zero : A 0 1 = 0 := by
    nlinarith [h01neg, h01]
  have h10zero : A 1 0 = 0 := by
    rw [← h01]
    exact h01zero
  ext i j
  fin_cases i <;> fin_cases j
  · simp
  · simp [h01zero]
  · simp [h10zero]
  · simp [hdiag]

/-! ## 开放口推进：等变平均的旋转不变性（§7.6① 三项形式化待证之第 1 项）

笔记 `mass_time_deflection_intuition.md` §7.6① 边界①："必然"是条件式（前提 = 强制平均等变）。
弥漫结构强制平均（C₄ 群平均的离散实现）的结果必须在参考系旋转下不变——
即 `groupAverage (Rᵢᵀ · T · Rᵢ) = groupAverage T`（先转后均 = 直接均）。
这是"等变平均 ⟹ 各向同性"链（groupAverage_isotropy 已闭合）的旋转不变前提；
与 isotropy_of_rotation_invariant_symmetric 一起构成：
**强制平均（等变）⟹ 旋转不变 ⟹ 对称张量 λI（各向同性）⟹ 全方向代价相等 ⟹ m_i = m_g（谱交织）**。
数值先证伪 `scripts/group_average_rotation_invariant_probe.py`：500 组（对称/反对称/一般混合）
× 4 元 = 2000 检查，最差残差 7.8e-14，ALL PASS。
证明策略：条目级展开（ext + fin_cases + simp + ring，与 rot_orthogonal 同模式），
C₄ 群乘法重排由标量 ring 归一化处理（避开矩阵结合/转置嵌套重排陷阱）。
-/

/-- 等变平均旋转不变（R0 情形）：trivial（R0 = 1）。 -/
theorem groupAverage_rot0_invariant (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage ((R0)ᵀ * T * R0) = groupAverage T := by
  simp [R0_eq_one]

/-- 等变平均旋转不变（R1 情形）：先沿 90° 共轭再平均 = 直接平均（C₄ 群乘法重排）。 -/
theorem groupAverage_rot1_invariant (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage ((R1)ᵀ * T * R1) = groupAverage T := by
  unfold groupAverage
  ext i j
  fin_cases i <;> fin_cases j
  <;> simp [R0, R1, R2, R3, rot, Real.cos_pi_div_two, Real.sin_pi_div_two,
            Real.cos_pi, Real.sin_pi, Real.cos_neg, Real.sin_neg, Matrix.mul_apply,
            Matrix.vecMul, Matrix.vecHead, Matrix.vecTail, Matrix.cons_val_zero,
            Fin.sum_univ_two]
  <;> ring

/-- 等变平均旋转不变（R2 情形）：π 旋转共轭（R2 = −1）。 -/
theorem groupAverage_rot2_invariant (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage ((R2)ᵀ * T * R2) = groupAverage T := by
  unfold groupAverage
  ext i j
  fin_cases i <;> fin_cases j
  <;> simp [R0, R1, R2, R3, rot, Real.cos_pi_div_two, Real.sin_pi_div_two,
            Real.cos_pi, Real.sin_pi, Real.cos_neg, Real.sin_neg, Matrix.mul_apply,
            Matrix.vecMul, Matrix.vecHead, Matrix.vecTail, Matrix.cons_val_zero,
            Fin.sum_univ_two]
  <;> ring

/-- 等变平均旋转不变（R3 情形）：−90° 共轭（与 R1 对称）。 -/
theorem groupAverage_rot3_invariant (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage ((R3)ᵀ * T * R3) = groupAverage T := by
  unfold groupAverage
  ext i j
  fin_cases i <;> fin_cases j
  <;> simp [R0, R1, R2, R3, rot, Real.cos_pi_div_two, Real.sin_pi_div_two,
            Real.cos_pi, Real.sin_pi, Real.cos_neg, Real.sin_neg, Matrix.mul_apply,
            Matrix.vecMul, Matrix.vecHead, Matrix.vecTail, Matrix.cons_val_zero,
            Fin.sum_univ_two]
  <;> ring

/-- ★★ 等变平均旋转不变（C₄ 全元）：先沿任意 C₄ 旋转共轭再平均 = 直接平均。
    即 E∘R = E（平均结果不依赖参考系旋转），"等变平均 ⟹ 旋转不变"机检。 -/
theorem groupAverage_rotation_invariant_all (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage ((R0)ᵀ * T * R0) = groupAverage T ∧
    groupAverage ((R1)ᵀ * T * R1) = groupAverage T ∧
    groupAverage ((R2)ᵀ * T * R2) = groupAverage T ∧
    groupAverage ((R3)ᵀ * T * R3) = groupAverage T := by
  exact ⟨groupAverage_rot0_invariant T, groupAverage_rot1_invariant T,
    groupAverage_rot2_invariant T, groupAverage_rot3_invariant T⟩

/-! ## 旋转群封闭：弥漫结构携带群作用的存在性（2026-10-25 追加）

回答"弥漫结构为什么携带群作用"的代数层补钉：SO(2) 旋转在复合下封闭
（★`rot_add`：rot(θ₁+θ₂)=rotθ₁·rotθ₂——旋转构成群，非仅集合），
C₄ 子群乘法表封闭（R1·R1=R2、R1·R2=R3、R1·R3=R0、R2·R2=R0——90° 元
生成 4 阶循环群）。连同 groupAverage_rotation_invariant_all
（等变平均在 C₄ 下不变）与 ForceAverageIsotropy 主线：
**弥漫结构携带群作用（C₄/SO(2)，封闭）⟹ 等变平均（幂等投影）⟹ 旋转不变 ⟹ 各向同性 λI**。
数值先证伪 `scripts/rotation_group_probe.py`：rot_add 最差残差 1.1e-16、
C₄ 乘法表残差 <2.5e-16，ALL PASS。
-/

/-- ★★ 旋转复合封闭：rot(θ₁+θ₂) = rotθ₁·rotθ₂——SO(2) 旋转在复合下构成群（群作用存在）。 -/
theorem rot_add (θ₁ θ₂ : ℝ) : rot (θ₁ + θ₂) = rot θ₁ * rot θ₂ := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    (simp [rot, Real.cos_add, Real.sin_add]; try ring)

/-- C₄ 封闭：R1·R1 = R2（90° 复合 90° = 180°）。 -/
theorem R1_mul_R1 : R1 * R1 = R2 := by
  unfold R1 R2
  rw [← rot_add]
  congr 1
  ring

/-- C₄ 封闭：R1·R2 = R3（90° 复合 180° = 270° ≡ −90°，cos/sin 周期）。 -/
theorem R1_mul_R2 : R1 * R2 = R3 := by
  unfold R1 R2 R3
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rot, Real.cos_neg, Real.sin_neg, Real.cos_pi_div_two, Real.sin_pi_div_two,
      Real.cos_pi, Real.sin_pi]

/-- C₄ 封闭：R1·R3 = R0（90° 复合 −90° = 0）。 -/
theorem R1_mul_R3 : R1 * R3 = R0 := by
  unfold R1 R3 R0
  rw [← rot_add]
  congr 1
  ring

/-- C₄ 封闭：R2·R2 = R0（180° 复合 180° = 360° ≡ 0，cos/sin 周期）。 -/
theorem R2_mul_R2 : R2 * R2 = R0 := by
  unfold R2 R0
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rot, Real.cos_pi, Real.sin_pi, Real.cos_zero, Real.sin_zero]

/-! ## 强制平均的投影性质（§7.6① 三项形式化待证之第 2 项前哨，2026-10-25 追加）

笔记 §7.6① (ii)："等变平均（Karcher/谱测度积分）保正交"。本段闭合其可机检核心：
  ★ groupAverage_idempotent：groupAverage(groupAverage T)=groupAverage T——
    C₄ 群平均是幂等投影（T 从"给定结构"到"结构涌现"的投影签名，坐实 L183
    "T = 弥漫层间结构的谱测度强制平均"的代数一步）；
  ★ groupAverage_preserves_symmetric：对称输入 ⟹ 对称输出——共轭平均保对称。
数值先证伪 `scripts/group_average_idempotent_probe.py`（500 组随机）：
  幂等最差残差 4.4e-16（=0，投影）、保对称 0.0e+00（=0，保持）、
  **保正交最差残差 1.0e+00（≠0，反证）**——欧氏群平均（算术平均）不保正交，
  正保正交须 Karcher/谱测度型平均（黎曼几何平均），该必要性获数值反证证据；
  "保正交"的黎曼表述留论证/指认层（诚实边界）。
-/

/-- ★★ 强制平均幂等：groupAverage(groupAverage T) = groupAverage T——C₄ 群平均是投影。
    证明：展开 16 个 (j,i) 组合，C₄ 封闭（R_j·R_i 复合仍在 C₄）使每项
    (1/16)R_k·T·R_kᵀ 出现 4 次 ⟹ 归并为 (1/4)Σ_k（条目级 ring 归一化）。 -/
theorem groupAverage_idempotent (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage (groupAverage T) = groupAverage T := by
  unfold groupAverage
  ext i j
  fin_cases i <;> fin_cases j
  <;> simp [R0, R1, R2, R3, rot, Real.cos_pi_div_two, Real.sin_pi_div_two,
            Real.cos_pi, Real.sin_pi, Real.cos_neg, Real.sin_neg,
            Matrix.mul_apply, Matrix.vecMul, Matrix.vecHead, Matrix.vecTail,
            Matrix.cons_val_zero, Fin.sum_univ_two, Matrix.transpose]
  <;> ring

/-- ★★ 强制平均保对称：对称输入 ⟹ 对称输出——共轭平均保持对称性
    （(R·T·Rᵀ)ᵀ = R·Tᵀ·Rᵀ，逐项共轭保对称）。 -/
theorem groupAverage_preserves_symmetric {T : Matrix (Fin 2) (Fin 2) ℝ} (hsym : Tᵀ = T) :
    (groupAverage T)ᵀ = groupAverage T := by
  have h01 : T 0 1 = T 1 0 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 0) hsym
    simpa [Matrix.transpose] using h
  unfold groupAverage
  ext i j
  fin_cases i <;> fin_cases j
  <;> simp [R0, R1, R2, R3, rot, Real.cos_pi_div_two, Real.sin_pi_div_two,
            Real.cos_pi, Real.sin_pi, Real.cos_neg, Real.sin_neg,
            Matrix.mul_apply, Matrix.vecMul, Matrix.vecHead, Matrix.vecTail,
            Matrix.cons_val_zero, Fin.sum_univ_two, Matrix.transpose]
  · nlinarith [h01]
  · nlinarith [h01]

/-! ## T 涌现完整形态：弥漫平均保持谱交织（§7.6① (iii) 有效谱交织等式，2026-10-25 追加）

笔记 §7.6① (iii)："该平均满足有效谱交织等式"——T = 弥漫结构强制平均（groupAverage）
从"给定结构"翻转为"结构涌现"的完整形态：若种子 B 满足谱交织（A_GR·B = B·A_SM）
且两侧算符旋转不变（各向同性前提），则平均 T = groupAverage B 仍满足
**有效谱交织** A_GR·T = T·A_SM——弥漫平均（等变投影）不破坏谱交织，
弱等效的"宏观涌现"代数闭环（与 MassEquivalenceBridge 取迹桥 + 统计弱等效合流）。
数值先证伪 `scripts/rotation_invariant_intertwine_probe.py`（500 组随机，
旋转不变族 A=aI+bJ）：(a) left 1.3e-15、(b) right 8.9e-16、(c) 交织保持 8.9e-16，ALL PASS。
-/

/-- 旋转不变 ⟹ 与旋转交换：rotθ·A·(rotθ)ᵀ = A ⟹ A·rotθ = rotθ·A。 -/
theorem rot_comm_of_invariant (A : Matrix (Fin 2) (Fin 2) ℝ) (θ : ℝ)
    (hA : rot θ * A * (rot θ)ᵀ = A) : A * rot θ = rot θ * A := by
  calc
    A * rot θ = (rot θ * A * (rot θ)ᵀ) * rot θ := by rw [hA]
    _ = (rot θ * A) * ((rot θ)ᵀ * rot θ) := by rw [Matrix.mul_assoc]
    _ = (rot θ * A) * 1 := by rw [rot_orthogonal]
    _ = rot θ * A := by simp

/-- 旋转矩阵的转置 = 负角旋转：(rot θ)ᵀ = rot (-θ)。 -/
theorem rot_transpose (θ : ℝ) : (rot θ)ᵀ = rot (-θ) := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [rot, Real.cos_neg, Real.sin_neg]

/-- 旋转不变 ⟹ 与旋转转置交换：A·(rotθ)ᵀ = (rotθ)ᵀ·A。 -/
theorem rotT_comm_of_invariant (A : Matrix (Fin 2) (Fin 2) ℝ) (θ : ℝ)
    (hA : ∀ θ : ℝ, rot θ * A * (rot θ)ᵀ = A) : A * (rot θ)ᵀ = (rot θ)ᵀ * A := by
  rw [rot_transpose]
  exact rot_comm_of_invariant A (-θ) (hA (-θ))

/-- ★ 等变投影与不变算符左交换：A 旋转不变 ⟹ A·groupAverage(B) = groupAverage(A·B)
    （弥漫平均与参考系旋转不变的算符可交换）。 -/
theorem groupAverage_left_comm_of_invariant (A B : Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ θ : ℝ, rot θ * A * (rot θ)ᵀ = A) :
    A * groupAverage B = groupAverage (A * B) := by
  have hsmul : ∀ (c : ℝ) (S : Matrix (Fin 2) (Fin 2) ℝ), A * (c • S) = c • (A * S) := by
    intro c S
    ext i j
    simp [Matrix.mul_apply, Fin.sum_univ_two]
    ring
  unfold groupAverage
  rw [hsmul]
  rw [mul_add, mul_add, mul_add]
  have hstep : ∀ (R : Matrix (Fin 2) (Fin 2) ℝ) (θ : ℝ), R = rot θ →
      A * (R * B * (R)ᵀ) = R * (A * B) * (R)ᵀ := by
    intro R θ hR
    rw [hR]
    calc
      A * (rot θ * B * (rot θ)ᵀ) = ((A * rot θ) * B) * (rot θ)ᵀ := by group
      _ = ((rot θ * A) * B) * (rot θ)ᵀ := by rw [rot_comm_of_invariant A θ (hA θ)]
      _ = (rot θ * (A * B)) * (rot θ)ᵀ := by group
      _ = rot θ * (A * B) * (rot θ)ᵀ := by group
  rw [hstep R0 0 rfl, hstep R1 (Real.pi / 2) rfl, hstep R2 Real.pi rfl, hstep R3 (-(Real.pi / 2)) rfl]

/-- ★ 等变投影与不变算符右交换：A 旋转不变 ⟹ groupAverage(B·A) = groupAverage(B)·A。 -/
theorem groupAverage_right_comm_of_invariant (A B : Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ θ : ℝ, rot θ * A * (rot θ)ᵀ = A) :
    groupAverage (B * A) = groupAverage B * A := by
  have hsmul : ∀ (c : ℝ) (S : Matrix (Fin 2) (Fin 2) ℝ), (c • S) * A = c • (S * A) := by
    intro c S
    ext i j
    simp [Matrix.mul_apply, Fin.sum_univ_two]
    ring
  unfold groupAverage
  rw [hsmul]
  rw [add_mul, add_mul, add_mul]
  have hstepR : ∀ (R : Matrix (Fin 2) (Fin 2) ℝ) (θ : ℝ), R = rot θ →
      (R * B * (R)ᵀ) * A = R * (B * A) * (R)ᵀ := by
    intro R θ hR
    rw [hR]
    calc
      (rot θ * B * (rot θ)ᵀ) * A = (rot θ * B) * ((rot θ)ᵀ * A) := by group
      _ = (rot θ * B) * (A * (rot θ)ᵀ) := by rw [rotT_comm_of_invariant A θ hA]
      _ = rot θ * (B * A) * (rot θ)ᵀ := by group
  rw [hstepR R0 0 rfl, hstepR R1 (Real.pi / 2) rfl, hstepR R2 Real.pi rfl, hstepR R3 (-(Real.pi / 2)) rfl]

/-- ★★ 弥漫平均保持谱交织（(iii) 有效谱交织等式机检）：A_GR、A_SM 旋转不变
    （各向同性前提）+ 种子交织 A_GR·B = B·A_SM ⟹ 平均 T = groupAverage B 满足
    A_GR·T = T·A_SM——弥漫结构强制平均（等变投影）不破坏谱交织，
    T 从"给定结构"翻转为"结构涌现"且有效交织自动成立。 -/
theorem groupAverage_preserves_intertwine {A_GR A_SM B : Matrix (Fin 2) (Fin 2) ℝ}
    (hGR : ∀ θ : ℝ, rot θ * A_GR * (rot θ)ᵀ = A_GR)
    (hSM : ∀ θ : ℝ, rot θ * A_SM * (rot θ)ᵀ = A_SM)
    (h : A_GR * B = B * A_SM) :
    A_GR * groupAverage B = groupAverage B * A_SM := by
  rw [groupAverage_left_comm_of_invariant A_GR B hGR]
  rw [h]
  rw [groupAverage_right_comm_of_invariant A_SM B hSM]

/-! ## 李群连续层指认 + 各向同性⟹交织反向（开放项收口，2026-10-25 追加）

离散 C₄ 旋转群（rot 0/π/2/π/−π/2）⟹ 连续 SO(2) 李群的指认底座：
J = [[0,-1],[1,0]] 为反交换生成元（J²=−1），旋转矩阵即指数形态
rot θ = cosθ·1 + sinθ·J（exp(θJ)=cosθ·1+sinθ·J 的有限维实现）；
rotExp 满足指数律（可加性 = 李群同态指认），J 与全体旋转交换（中心元素，
"弥漫结构携带群作用"的代数中心）；同时闭合"各向同性⟹交织"反向缺口：
λI（各向同性质量算符）与任意谱流 B 交换——弱等效链的双向性。
数值先证伪 `scripts/continuous_layer_probe.py`（500 组随机）：
(a) J²=−I 0、(b) rotExp=rot 0、(c) 指数律 1.7e-15、(d) J 中心交换 0、(e) λI·B=B·λI 0，ALL PASS。
-/

/-- J = [[0,-1],[1,0]]：旋转群反交换生成元（SO(2) 的无穷小生成元矩阵实现）。 -/
def J : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]

/-- ★ J² = −1：反交换生成元的平方为负单位阵（exp(θJ)=cosθ·1+sinθ·J 的代数根）。 -/
theorem J_mul_J : J * J = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [J, Matrix.mul_apply, Fin.sum_univ_two]

/-- ★ 旋转矩阵 = 指数形态线性组合：rot θ = cosθ·1 + sinθ·J（SO(2) 连续层指认底座）。 -/
theorem rot_eq_linear (θ : ℝ) :
    rot θ = (Real.cos θ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) + (Real.sin θ) • J := by
  ext i j <;> fin_cases i <;> fin_cases j
  <;> simp [rot, J, Matrix.smul_apply]
  <;> ring

/-- rotExp：连续旋转的显式指数形态（cosθ·1 + sinθ·J，即 exp(θJ) 的实现）。 -/
noncomputable def rotExp (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  (Real.cos θ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) + (Real.sin θ) • J

/-- rotExp 与旋转矩阵同一：rotExp θ = rot θ。 -/
theorem rotExp_eq_rot (θ : ℝ) : rotExp θ = rot θ := by
  rw [rot_eq_linear]
  rfl

/-- ★ 指数律（李群同态）：rotExp(θ₁+θ₂) = rotExp θ₁·rotExp θ₂——连续层可加性指认。 -/
theorem rotExp_add (θ₁ θ₂ : ℝ) : rotExp (θ₁ + θ₂) = rotExp θ₁ * rotExp θ₂ := by
  rw [rotExp_eq_rot, rotExp_eq_rot, rotExp_eq_rot]
  exact rot_add θ₁ θ₂

/-- ★ J 与全体旋转交换（中心元素）：J·rot θ = rot θ·J——群作用的代数中心。 -/
theorem J_comm_rot (θ : ℝ) : J * rot θ = rot θ * J := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [J, rot, Matrix.mul_apply, Fin.sum_univ_two]

/-- ★ 各向同性⟹交织反向：λI（各向同性质量算符）与任意谱流 B 交换。 -/
theorem scalar_comm_all (lam : ℝ) (B : Matrix (Fin 2) (Fin 2) ℝ) :
    (lam • (1 : Matrix (Fin 2) (Fin 2) ℝ)) * B = B * (lam • 1) := by
  ext i j <;> simp [Matrix.mul_apply, Matrix.one_apply] <;> ring

/-- ★★ 各向同性⟹交织（反向缺口闭合）：质量算符各向同性（∝ λI）⟹ 与任意谱流
    自动交织——弱等效链 m_i=m_g 的"直接必然"（与谱交织⟹m_i=m_g 构成双向）。 -/
theorem isotropy_implies_intertwine (lam : ℝ) (B : Matrix (Fin 2) (Fin 2) ℝ) :
    (lam • (1 : Matrix (Fin 2) (Fin 2) ℝ)) * B = B * (lam • 1) :=
  scalar_comm_all lam B

/-! ## 粗粒化机制：弥漫平均=粗粒化算符（保迹，2026-10-25 追加）

笔记"粗粒化=微观对象在更大尺度下的整体表现、平均效应，进而推导各向同性必然"的代数核心：
T ↦ gA(T)（弥漫结构强制平均）即粗粒化算符——幂等投影（groupAverage_idempotent）、
输出旋转不变（groupAverage_rotation_invariant_all，各向同性必然）、且 **保迹**（trace(gA(T))=trace(T)）：
微观对象在更大尺度下的整体平均不改变宏观读数（涌现稳定性/粗粒化守恒）。
"递归层计数（离散 ℕ）→谱层参数（连续 ℝ）→观测时间"的粗粒化，其读数层级即由保迹性质锚定：
粗粒化前后质量读数（谱间隙/trace）同一。数值先证伪 `scripts/coarse_graining_probe.py`
（500 组随机）：(a) 保迹 4.4e-16、(a2) 旋转不变族 0、(b) 旋转不变输出 4.4e-16、(c) 幂等 4.4e-16，ALL PASS。
-/

/-- ★★ 粗粒化保迹（涌现稳定性）：trace(groupAverage T) = trace(T)——弥漫平均
    （粗粒化算符）不改变宏观读数；与输出旋转不变合流 = "粗粒化⟹各向同性且读数守恒"。 -/
theorem groupAverage_trace_eq (T : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace (groupAverage T) = Matrix.trace T := by
  unfold groupAverage
  rw [Matrix.trace_smul]
  rw [Matrix.trace_add, Matrix.trace_add, Matrix.trace_add]
  have ht : ∀ (R : Matrix (Fin 2) (Fin 2) ℝ) (θ : ℝ), R = rot θ →
      Matrix.trace (R * T * (R)ᵀ) = Matrix.trace T := by
    intro R θ hR
    rw [hR]
    calc
      Matrix.trace (rot θ * T * (rot θ)ᵀ) = Matrix.trace ((rot θ)ᵀ * (rot θ * T)) := by
        rw [Matrix.trace_mul_comm]
      _ = Matrix.trace ((rot θ)ᵀ * rot θ * T) := by rw [← Matrix.mul_assoc]
      _ = Matrix.trace (1 * T) := by rw [rot_orthogonal]
      _ = Matrix.trace T := by simp
  rw [ht R0 0 rfl, ht R1 (Real.pi / 2) rfl, ht R2 Real.pi rfl, ht R3 (-(Real.pi / 2)) rfl]
  ring

/-! ## SO(2) 全群满射表征（开放项收口，2026-10-25 追加）

连续旋转层（rot θ）覆盖全部 SO(2)（正交 + 单位行列式）：
(i) 结构形态必要——正交 det=1 ⟹ A00=A11 ∧ A01=-A10 ∧ A00²+A01²=1（单参数单位圆结构，
    (d-a)²+(b+c)²=(a²+c²+b²+d²)-2(ad-bc)=0 即"平方和归零 ⟹ 逐项零"）；
(ii) 结构形态充分——a=d、b=-c、a²+b²=1 ⟹ 正交 ∧ det=1；
(iii) 满射——正交 det=1 ⟹ ∃θ A=rot θ（θ=arcsin(-A01) 对 A00≥0，θ=π-arcsin(-A01) 对 A00<0；
    sinθ=c、cosθ=a 的 arcsin 分支构造）。
至此 {rot θ | θ∈ℝ} = SO(2)（与 rotExp 指数形态、rot_add 封闭、J 中心交换合流）。
数值先证伪 `scripts/so2_surjective_probe.py`（500 组随机）：(a) 必要 2.2e-16、(b) 充分 2.2e-16、
(c) 满射重构 1.4e-14、(d) rot 保正交 det1 2.2e-16，ALL PASS。
-/

/-- ★ 结构形态必要：正交（Aᵀ·A=1）+ 单位行列式 ⟹ A00=A11 ∧ A01=-A10 ∧ A00²+A01²=1
    （SO(2) 单参数单位圆结构；(d-a)²+(b+c)²=0 由正交+det 恒等式归零）。 -/
theorem so2_structural_necessary {A : Matrix (Fin 2) (Fin 2) ℝ}
    (horth : Aᵀ * A = 1) (hdet : A.det = 1) :
    A 0 0 = A 1 1 ∧ A 0 1 = -(A 1 0) ∧ (A 0 0)^2 + (A 0 1)^2 = 1 := by
  let a := A 0 0
  let b := A 0 1
  let c := A 1 0
  let d := A 1 1
  have hA : A = !![a, b; c, d] := by
    ext i j <;> fin_cases i <;> fin_cases j <;> simp [a, b, c, d]
  have h00 : a^2 + c^2 = 1 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) horth
    simpa [a, b, c, d, pow_two, Matrix.mul_apply, Matrix.transpose_apply, Matrix.one_apply, Fin.sum_univ_two] using h
  have h11 : b^2 + d^2 = 1 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 1) horth
    simpa [a, b, c, d, pow_two, Matrix.mul_apply, Matrix.transpose_apply, Matrix.one_apply, Fin.sum_univ_two] using h
  have hd1 : a * d - b * c = 1 := by
    rw [hA] at hdet
    simpa [Matrix.det_fin_two] using hdet
  have hsq : (d - a)^2 + (b + c)^2 = 0 := by
    nlinarith [h00, h11, hd1]
  have hd0 : d - a = 0 := by
    nlinarith [sq_nonneg (d - a), sq_nonneg (b + c), hsq]
  have hbc0 : b + c = 0 := by
    nlinarith [sq_nonneg (d - a), sq_nonneg (b + c), hsq]
  have hd_eq : d = a := by linarith
  have hb_eq : b = -c := by linarith [hbc0]
  have hnorm : a^2 + b^2 = 1 := by nlinarith [h00, hb_eq]
  constructor
  · simp [a, d, hd_eq]
  · constructor
    · simp [b, c, hb_eq]
    · simpa [a, b, c, d] using hnorm

/-- ★ 结构形态充分：a=d、b=-c、a²+b²=1 ⟹ [[a,-b],[b,a]] 正交 ∧ det=1
    （单参数单位圆形态必为 SO(2) 元）。 -/
theorem so2_structural_sufficient {a b : ℝ} (hn : a^2 + b^2 = 1) :
    (!![a, -b; b, a] : Matrix (Fin 2) (Fin 2) ℝ)ᵀ *
        (!![a, -b; b, a] : Matrix (Fin 2) (Fin 2) ℝ) = 1 ∧
      (!![a, -b; b, a] : Matrix (Fin 2) (Fin 2) ℝ).det = 1 := by
  constructor
  · ext i j <;> fin_cases i <;> fin_cases j
    <;> simp [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_two]
    <;> nlinarith [hn]
  · simp [Matrix.det_fin_two]; nlinarith [hn]

/-- ★★ SO(2) 满射：正交 + 单位行列式 ⟹ ∃θ A=rot θ（arcsin 分支构造：
    θ=-arcsin(A01) 对 A00≥0、θ=π+arcsin(A01) 对 A00<0；sinθ=-A01、cosθ=A00；
    与数值探针 arcsin(-A01)/π-arcsin(-A01) 等价（arcsin 奇函数））。
    {rot θ | θ∈ℝ} 覆盖全部 SO(2)。 -/
theorem so2_surjective {A : Matrix (Fin 2) (Fin 2) ℝ}
    (horth : Aᵀ * A = 1) (hdet : A.det = 1) :
    ∃ θ : ℝ, A = rot θ := by
  let a := A 0 0
  let b := A 0 1
  let c := A 1 0
  let d := A 1 1
  have hstruct := so2_structural_necessary horth hdet
  have hd : A 1 1 = a := by simpa [a] using hstruct.1.symm
  have hc : A 1 0 = -b := by
    have h2 := hstruct.2.1
    simpa [b] using (by linarith : A 1 0 = -A 0 1)
  have hn : a^2 + b^2 = 1 := by simpa [a, b] using hstruct.2.2
  have hb2 : b^2 ≤ 1 := by nlinarith [sq_nonneg a, hn]
  have hb_l : -1 ≤ b := by nlinarith [sq_nonneg (b + 1), hb2]
  have hb_u : b ≤ 1 := by nlinarith [sq_nonneg (1 - b), hb2]
  have hsb : Real.sin (Real.arcsin b) = b := by
    rw [Real.sin_arcsin hb_l hb_u]
  by_cases ha : 0 ≤ a
  · refine ⟨-Real.arcsin b, ?_⟩
    have hcb : Real.cos (Real.arcsin b) = a := by
      rw [Real.cos_arcsin]
      rw [show 1 - b^2 = a^2 by nlinarith [hn]]
      rw [Real.sqrt_sq_eq_abs]
      exact abs_of_nonneg ha
    ext i j <;> fin_cases i <;> fin_cases j
    · simp [rot, hcb, a]
    · simp [rot, hsb, b]
    · simp [rot, hsb, hc]
    · simp [rot, hcb, hd]
  · refine ⟨Real.pi + Real.arcsin b, ?_⟩
    have hsa : Real.sin (Real.pi + Real.arcsin b) = -b := by
      rw [Real.sin_add]
      simp [Real.cos_pi, Real.sin_pi]
      rw [Real.sin_arcsin hb_l hb_u]
    have hca : Real.cos (Real.pi + Real.arcsin b) = a := by
      rw [Real.cos_add]
      simp [Real.cos_pi, Real.sin_pi]
      rw [Real.cos_arcsin]
      rw [show 1 - b^2 = a^2 by nlinarith [hn]]
      rw [Real.sqrt_sq_eq_abs]
      rw [abs_of_neg]
      · ring
      · exact not_le.mp ha
    ext i j <;> fin_cases i <;> fin_cases j
    · simp [rot, hca, a]
    · simp [rot, hsa, b]
    · simp [rot, hsa, hc]
    · simp [rot, hca, hd]

/-- ★★ 等变平均在旋转群元上=恒等（Karcher/几何平均表述第一步机检）：
    SO(2) 阿贝尔 ⟹ C₄ 共轭 R(θ)·R(φ)·R(θ)ᵀ=R(φ) ⟹ groupAverage(rot φ)=rot φ
    ——弥漫平均对旋转结构自平均不动、自动保正交（群元样本上 Karcher 平凡成立）。
    （Karcher 开放项第一步：在群元上"平均不破坏正交结构"平凡真；非群元的
    保正交仍需黎曼化，欧氏平均反证已证必要性。） -/
theorem groupAverage_preserves_rotation (φ : ℝ) :
    groupAverage (rot φ) = rot φ := by
  unfold groupAverage
  unfold R0 R1 R2 R3
  have hk : ∀ (θ : ℝ), rot θ * rot φ * (rot θ)ᵀ = rot φ := by
    intro θ
    rw [rot_transpose]
    rw [← rot_add]
    rw [← rot_add]
    rw [show (θ + φ) + -θ = φ by ring]
  rw [hk 0, hk (Real.pi / 2), hk Real.pi, hk (-(Real.pi / 2))]
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [rot] <;> ring_nf

/-- rot θ 单位行列式（SO(2) 满射表征 (d) 复核句）：det(rot θ)=1。 -/
theorem rot_det_eq_one (θ : ℝ) : (rot θ).det = 1 := by
  simp [rot, Matrix.det_fin_two]
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-- 反射生成元 F=diag(1,-1)：手性/宇称翻转（det=-1，O(2)\SO(2) 代表元）。 -/
noncomputable def F : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- F 与旋转的翻转共轭：F·rot θ = rot(-θ)·F（反射翻转旋转方向；O(2) 半直积结构）。 -/
theorem F_mul_rot (θ : ℝ) : F * rot θ = rot (-θ) * F := by
  ext i j <;> fin_cases i <;> fin_cases j <;> simp [F, rot]

/-- ★★ 反射元湮灭：groupAverage(rot θ·F)=0——C₄ 等变平均对 O(2) 非旋转元（手性）自抵消；
    等变平均在 O(2) 上的作用完全刻画：SO(2) 元恒等（groupAverage_preserves_rotation）、
    反射元精确归零（手性在粗粒化下湮灭）。Karcher 开放项续：非群元（反射类）的
    "保正交"不成立——不是近似而是精确湮灭。 -/
theorem groupAverage_reflection_annihilates (θ : ℝ) :
    groupAverage (rot θ * F) = 0 := by
  unfold groupAverage
  unfold R0 R1 R2 R3
  have hk : ∀ (α : ℝ), rot α * (rot θ * F) * (rot α)ᵀ = F * rot (-θ - 2*α) := by
    intro α
    rw [rot_transpose]
    rw [← Matrix.mul_assoc]
    rw [← rot_add]
    rw [show α + θ = -(-(α + θ)) by ring]
    rw [← F_mul_rot]
    rw [Matrix.mul_assoc]
    rw [← rot_add]
    rw [show -(α + θ) + -α = -θ - 2*α by ring]
  rw [hk 0, hk (Real.pi / 2), hk Real.pi, hk (-(Real.pi / 2))]
  have hcp : ∀ x : ℝ, Real.cos (x - Real.pi) = -Real.cos x := by
    intro x
    rw [Real.cos_sub]
    simp [Real.cos_pi, Real.sin_pi]
  have hcs : ∀ x : ℝ, Real.sin (x - Real.pi) = -Real.sin x := by
    intro x
    rw [Real.sin_sub]
    simp [Real.cos_pi, Real.sin_pi]
  have hcps : ∀ x : ℝ, Real.cos (Real.pi - x) = -Real.cos x := by
    intro x
    rw [Real.cos_sub]
    simp [Real.cos_pi, Real.sin_pi]
  have hsps : ∀ x : ℝ, Real.sin (Real.pi - x) = Real.sin x := by
    intro x
    rw [Real.sin_sub]
    simp [Real.cos_pi, Real.sin_pi]
  ext i j <;> fin_cases i <;> fin_cases j
  · simp [F, rot]
    rw [show -θ - 2 * (Real.pi / 2) = -θ - Real.pi by ring]
    rw [show -θ + 2 * (Real.pi / 2) = Real.pi - θ by ring]
    rw [hcp (-θ), hcps θ]
    simp <;> ring
  · simp [F, rot]
    rw [show -θ - 2 * (Real.pi / 2) = -θ - Real.pi by ring]
    rw [show -θ + 2 * (Real.pi / 2) = Real.pi - θ by ring]
    rw [hcs (-θ), hsps θ]
    simp <;> ring
  · simp [F, rot]
    rw [show -θ - 2 * (Real.pi / 2) = -θ - Real.pi by ring]
    rw [show -θ + 2 * (Real.pi / 2) = Real.pi - θ by ring]
    rw [hcs (-θ), hsps θ]
    simp <;> ring
  · simp [F, rot]
    rw [show -θ - 2 * (Real.pi / 2) = -θ - Real.pi by ring]
    rw [show -θ + 2 * (Real.pi / 2) = Real.pi - θ by ring]
    rw [hcp (-θ), hcps θ]
    simp <;> ring

/-- ★★ 层间桥代数核心（递归层时钟读出谱流）：指数律的整数幂版本——
    离散 n 步复合 (rotExp θ)^n = 谱参数 n·θ 一步到位 rotExp(n·θ)。
    "每次递归 = 时间递进一层"的代数实现：递归层时钟 n 步读出 = 谱层 rapidity 线性累积
    （每步 Δφ ⟹ n 步 = n·Δφ）。 -/
theorem rotExp_nat_mul (θ : ℝ) : ∀ n : ℕ, rotExp ((n : ℝ) * θ) = (rotExp θ) ^ n := by
  intro n
  induction n with
  | zero =>
      simp [rotExp, Real.cos_zero, Real.sin_zero]
  | succ n ih =>
      have hstep : ((Nat.succ n : ℝ) * θ) = (n : ℝ) * θ + θ := by
        rw [Nat.cast_succ]
        ring
      rw [hstep]
      rw [rotExp_add]
      rw [ih]
      rw [← pow_succ]

/-- ★ 层间桥推论（旋转形态）：rot(n·θ) = (rot θ)^n——离散时钟步进
    ⟷ 谱参数线性累积的旋转版本（rotExp_eq_rot 桥）。 -/
theorem rot_nat_mul (θ : ℝ) (n : ℕ) : rot ((n : ℝ) * θ) = (rot θ) ^ n := by
  have h := rotExp_nat_mul θ n
  simpa [rotExp_eq_rot] using h

/-- rot 双侧正交（转置侧）：rot θ·(rot θ)ᵀ = 1——方阵左右逆合一
    （由 rot_orthogonal (-θ) + rot_transpose 导出）。 -/
theorem rot_mul_transpose (θ : ℝ) : rot θ * (rot θ)ᵀ = 1 := by
  have h := rot_orthogonal (-θ)
  rw [rot_transpose] at h
  rw [rot_transpose]
  simpa using h

/-- ★★ 各向同性质量读数为正：T 对称正定 ⟹ groupAverage(T) = (trace T / 2)•1 且 0 < trace T / 2
    ——正定 ⟹ trace>0（质量读数为正）+ 保迹 + 各向同性 λI 合流：
    宏观质量读数 λ = trace(T)/2 > 0（各向同性且正）。 -/
theorem groupAverage_posdef_isotropy_pos {T : Matrix (Fin 2) (Fin 2) ℝ}
    (hpd : T.PosDef) :
    0 < (Matrix.trace T / 2 : ℝ) ∧ groupAverage T = (Matrix.trace T / 2 : ℝ) • 1 := by
  have hsym : Tᵀ = T := by simpa [Matrix.IsHermitian] using hpd.1
  have hg := groupAverage_isotropy hsym
  have htr : (T 0 0 + T 1 1) / 2 = Matrix.trace T / 2 := by
    simp [Matrix.trace, Fin.sum_univ_two]
  have hpos : 0 < Matrix.trace T := Matrix.PosDef.trace_pos hpd
  constructor
  · exact div_pos hpos (by norm_num)
  · simpa [htr] using hg

/-- ★★ 粗粒化保正定：T 对称正定 ⟹ groupAverage(T) 正定
    ——各向同性闭包 λI（λ=trace/2>0）⟹ λI 正定 ⟹ gA(T) 正定；
    粗粒化保持能量/质量谱正性（物理：宏观张量不因平均失去正定性）。 -/
theorem groupAverage_preserves_posdef {T : Matrix (Fin 2) (Fin 2) ℝ}
    (hpd : T.PosDef) : (groupAverage T).PosDef := by
  refine PosDef.of_dotProduct_mulVec_pos ?sym ?qform
  · have hsym : Tᵀ = T := by simpa [Matrix.IsHermitian] using hpd.1
    simpa [Matrix.IsHermitian] using groupAverage_preserves_symmetric hsym
  · intro x hx
    have hiso := groupAverage_posdef_isotropy_pos hpd
    rcases hiso with ⟨hlam, hg⟩
    rw [hg]
    simp [smul_mulVec, one_mulVec, smul_eq_mul]
    have hdp' : 0 < x 0 * x 0 + x 1 * x 1 := by
      by_cases h0 : x 0 = 0
      · have h1 : x 1 ≠ 0 := by
          intro h
          apply hx
          ext i
          fin_cases i <;> simp [h0, h]
        nlinarith [mul_self_pos.mpr h1]
      · nlinarith [mul_self_pos.mpr h0, mul_self_nonneg (x 1)]
    exact mul_pos hlam hdp'

/-- 标量中心共轭不动：rot θ·(a•1)·(rot θ)ᵀ = a•1——标量矩阵与任意旋转交换。 -/
theorem scalar_conj_rotation (a : ℝ) (θ : ℝ) :
    rot θ * (a • 1) * (rot θ)ᵀ = a • 1 := by
  simp [rot_mul_transpose]

/-- ★★ 离散平均涌现连续旋转对称：C₄ 等变平均的输出对任意连续旋转不变
    ——gA(T)=λI（各向同性）⟹ λI 与任意 rot θ 交换（标量中心）；
    "统计涌现"的连续侧：离散群平均 ⟹ 连续 O(2) 不变（粗粒化涌现连续对称）。 -/
theorem groupAverage_continuous_rotation_invariant {T : Matrix (Fin 2) (Fin 2) ℝ}
    (hsym : Tᵀ = T) (θ : ℝ) :
    rot θ * groupAverage T * (rot θ)ᵀ = groupAverage T := by
  have hg := groupAverage_isotropy hsym
  rw [hg]
  exact scalar_conj_rotation ((T 0 0 + T 1 1) / 2) θ

/-- ★★ Clifford 双向量 = 旋转生成元：Cℓ(0,1) 单位双向量 e_01 = !![0,-1;1,0]
    **恰为旋转生成元 J**（rotExp θ = cosθ·1 + sinθ·J 中的 J）。
    ——"Δ 携带群作用"的几何生成元指认：换位子结构（Pauli/非平凡）⟹ 平面旋转生成元。 -/
theorem e01_eq_J : e_01 (rfl : 2 = 2) = J := by
  rfl

/-- ★★ 双向量指数生成旋转单参子群：rotExp θ = cosθ·1 + sinθ·e_01
    ——Cℓ(0,1) ≅ ℂ 的矩阵表示：exp(θ·e_01) 即平面旋转（SO(2) 李群同态）。 -/
theorem rotExp_eq_cos_sin_e01 (θ : ℝ) :
    rotExp θ =
      Real.cos θ • (1 : Matrix (Fin 2) (Fin 2) ℝ) + Real.sin θ • e_01 (rfl : 2 = 2) := by
  rw [e01_eq_J]
  rfl

/-- ★★ 等变平均的投影完整刻画：对称张量是 C₄ 等变平均的不动点 ⟺ 它是各向同性张量 λI
    ——粗粒化算符的像空间 = 不动点空间 = 一维标量中心 {λI}；
    一切非各向同性部分被平均消除（强制平均 ⟹ 各向同性 的投影几何完成态）。 -/
theorem groupAverage_fixed_iff_scalar {T : Matrix (Fin 2) (Fin 2) ℝ} (hsym : Tᵀ = T) :
    groupAverage T = T ↔ ∃ lam : ℝ, T = lam • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  constructor
  · intro hfix
    have hg := groupAverage_isotropy hsym
    have hg' : T = ((T 0 0 + T 1 1) / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
      rw [hfix] at hg
      exact hg
    exact ⟨(T 0 0 + T 1 1) / 2, hg'⟩
  · rintro ⟨lam, rfl⟩
    have hsym' : (lam • (1 : Matrix (Fin 2) (Fin 2) ℝ))ᵀ = lam • 1 := by simp
    have hg := groupAverage_isotropy hsym'
    have ht : Matrix.trace (lam • (1 : Matrix (Fin 2) (Fin 2) ℝ)) / 2 = lam := by
      simp [Matrix.trace]
    simpa [ht] using hg

/-- ★★ 粗粒化的机制无关唯一性：任意"输出各向同性 + 保迹"的粗粒化机制 P
    在对称张量上与 C₄ 等变平均给出同一输出。
    ——统计涌现的普适性：弱等效读数与机制无关（离散 C₄ 平均/连续平均/其他
    各向同性保迹机制 ⟹ 同一 λI，λ=trace/2）。 -/
theorem unique_isotropic_average {T : Matrix (Fin 2) (Fin 2) ℝ} (hsym : Tᵀ = T)
    (P : Matrix (Fin 2) (Fin 2) ℝ → Matrix (Fin 2) (Fin 2) ℝ)
    (hPiso : ∀ S : Matrix (Fin 2) (Fin 2) ℝ, Sᵀ = S →
      ∃ lam : ℝ, P S = lam • (1 : Matrix (Fin 2) (Fin 2) ℝ))
    (hPtrace : ∀ S : Matrix (Fin 2) (Fin 2) ℝ, Matrix.trace (P S) = Matrix.trace S) :
    P T = groupAverage T := by
  rcases hPiso T hsym with ⟨lam, hPT⟩
  have ht : Matrix.trace (P T) = Matrix.trace T := hPtrace T
  rw [hPT] at ht
  have htr : Matrix.trace (lam • (1 : Matrix (Fin 2) (Fin 2) ℝ)) = 2 * lam := by
    simp [Matrix.trace]
  rw [htr] at ht
  have hlam : lam = Matrix.trace T / 2 := by
    linarith
  rw [hPT, hlam]
  have ht2 : (T 0 0 + T 1 1) / 2 = Matrix.trace T / 2 := by
    simp [Matrix.trace, Fin.sum_univ_two]
  rw [← ht2]
  exact (groupAverage_isotropy hsym).symm

/-- ★★ 对称张量的正交无迹分解：T = (trace/2)·1 + T₀，T₀ 无迹
    ——标量部分（宏观读数/相空间）与无迹部分（各向异性/Cl 结构）直和。 -/
theorem symmetric_traceless_decomp {T : Matrix (Fin 2) (Fin 2) ℝ} :
    ∃ T₀ : Matrix (Fin 2) (Fin 2) ℝ,
      T = (Matrix.trace T / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) + T₀ ∧ Matrix.trace T₀ = 0 := by
  refine ⟨T - (Matrix.trace T / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ), ?_, ?_⟩
  · abel
  · rw [Matrix.trace_sub]
    have htr : Matrix.trace ((Matrix.trace T / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ)) =
        Matrix.trace T := by
      simp [Matrix.trace]
      ring_nf
    rw [htr]
    simp

/-- ★★ 标量中心与无迹部分正交：矩阵内积 ⟨A,B⟩=trace(AᵀB) 下，
    trace((a·1)ᵀ·T₀) = 0 当 trace T₀ = 0——"相空间读数"与"各向异性结构"正交。 -/
theorem scalar_orthogonal_traceless (a : ℝ) {T₀ : Matrix (Fin 2) (Fin 2) ℝ}
    (ht0 : Matrix.trace T₀ = 0) :
    Matrix.trace ((a • (1 : Matrix (Fin 2) (Fin 2) ℝ))ᵀ * T₀) = 0 := by
  rw [Matrix.transpose_smul, Matrix.transpose_one]
  rw [Matrix.smul_mul]
  rw [Matrix.one_mul]
  rw [Matrix.trace_smul]
  rw [ht0]
  simp

/-- ★★ 粗粒化的补投影湮灭各向异性：trace(T − gA(T)) = 0
    ——gA 保留标量（各向同性/相空间读数），id−gA 保留无迹（各向异性/Cl 结构）：
    两个互补正交投影（"态射/右伴随的两正交投影"直觉的代数对应）。 -/
theorem groupAverage_complement_traceless {T : Matrix (Fin 2) (Fin 2) ℝ} :
    Matrix.trace (T - groupAverage T) = 0 := by
  rw [Matrix.trace_sub]
  rw [groupAverage_trace_eq]
  simp

/-- ★★ 粗粒化的伴随性（Karcher 开放项①：正交投影几何第一步）：
    (gA T)ᵀ = gA(Tᵀ)——C₄ 等变平均与转置交换（逐项 (R·T·Rᵀ)ᵀ=R·Tᵀ·Rᵀ，
    (Rᵀ)ᵀ=R 还原，无需 C₄ 转置闭包）。伴随性质：gA 是矩阵空间上
    迹内积正交投影的必要构件（自伴随幂等）。 -/
theorem groupAverage_adjoint (T : Matrix (Fin 2) (Fin 2) ℝ) :
    (groupAverage T)ᵀ = groupAverage (Tᵀ) := by
  unfold groupAverage
  have ha0 : (R0 * T * (R0)ᵀ)ᵀ = R0 * Tᵀ * (R0)ᵀ := by
    rw [Matrix.transpose_mul]
    rw [transpose_transpose]
    rw [Matrix.transpose_mul]
    rw [Matrix.mul_assoc]
  have ha1 : (R1 * T * (R1)ᵀ)ᵀ = R1 * Tᵀ * (R1)ᵀ := by
    rw [Matrix.transpose_mul]
    rw [transpose_transpose]
    rw [Matrix.transpose_mul]
    rw [Matrix.mul_assoc]
  have ha2 : (R2 * T * (R2)ᵀ)ᵀ = R2 * Tᵀ * (R2)ᵀ := by
    rw [Matrix.transpose_mul]
    rw [transpose_transpose]
    rw [Matrix.transpose_mul]
    rw [Matrix.mul_assoc]
  have ha3 : (R3 * T * (R3)ᵀ)ᵀ = R3 * Tᵀ * (R3)ᵀ := by
    rw [Matrix.transpose_mul]
    rw [transpose_transpose]
    rw [Matrix.transpose_mul]
    rw [Matrix.mul_assoc]
  rw [Matrix.transpose_smul]
  rw [Matrix.transpose_add, Matrix.transpose_add, Matrix.transpose_add]
  rw [ha0, ha1, ha2, ha3]

/-- ★★ 粗粒化 = 迹内积正交投影（Karcher 开放项① 核心）：
    ⟨gA T, S⟩ = ⟨T, gA S⟩（⟨A,B⟩=trace(AᵀB)）——gA 在迹内积下自伴随。
    ——"相空间读数"与"各向异性结构"的内积分离由 gA 的自伴随性保证：
    幂等（groupAverage_idempotent）+ 自伴随 ⟹ 正交投影；
    平坦迹内积层的投影几何完成态（Karcher 几何平均是其正定流形推广，
    欧氏平均反证已证非群元保正交必要性）。 -/
theorem groupAverage_orthogonal_projection (T S : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace ((groupAverage T)ᵀ * S) = Matrix.trace (Tᵀ * groupAverage S) := by
  rw [groupAverage_adjoint]
  unfold groupAverage
  simp [Matrix.add_mul, Matrix.mul_add]
  have hcycle : ∀ (R A : Matrix (Fin 2) (Fin 2) ℝ),
      Matrix.trace ((R * A * (R)ᵀ) * S) = Matrix.trace (A * (R)ᵀ * S * R) := by
    intro R A
    rw [Matrix.trace_mul_comm]
    rw [← Matrix.mul_assoc, ← Matrix.mul_assoc]
    rw [Matrix.trace_mul_comm]
    rw [← Matrix.mul_assoc]
    rw [Matrix.trace_mul_comm]
    simp [Matrix.mul_assoc]
  have hp0 : Matrix.trace ((R0 * Tᵀ * (R0)ᵀ) * S) = Matrix.trace (Tᵀ * ((R0 * S) * (R0)ᵀ)) := by
    rw [hcycle R0 (Tᵀ)]
    rw [R0_eq_one]
    simp
  have hp1 : Matrix.trace ((R1 * Tᵀ * (R1)ᵀ) * S) = Matrix.trace (Tᵀ * ((R3 * S) * (R3)ᵀ)) := by
    rw [hcycle R1 (Tᵀ)]
    rw [R1_transpose]
    rw [R3_transpose]
    simp [Matrix.mul_assoc]
  have hp2 : Matrix.trace ((R2 * Tᵀ * (R2)ᵀ) * S) = Matrix.trace (Tᵀ * ((R2 * S) * (R2)ᵀ)) := by
    rw [hcycle R2 (Tᵀ)]
    rw [R2_transpose]
    simp [Matrix.mul_assoc]
  have hp3 : Matrix.trace ((R3 * Tᵀ * (R3)ᵀ) * S) = Matrix.trace (Tᵀ * ((R1 * S) * (R1)ᵀ)) := by
    rw [hcycle R3 (Tᵀ)]
    rw [R3_transpose]
    rw [R1_transpose]
    simp [Matrix.mul_assoc]
  have hsum : ((4⁻¹ : ℝ) * Matrix.trace ((R0 * Tᵀ * (R0)ᵀ) * S)
      + (4⁻¹ : ℝ) * Matrix.trace ((R1 * Tᵀ * (R1)ᵀ) * S)
      + (4⁻¹ : ℝ) * Matrix.trace ((R2 * Tᵀ * (R2)ᵀ) * S)
      + (4⁻¹ : ℝ) * Matrix.trace ((R3 * Tᵀ * (R3)ᵀ) * S))
      = ((4⁻¹ : ℝ) * Matrix.trace (Tᵀ * ((R0 * S) * (R0)ᵀ))
      + (4⁻¹ : ℝ) * Matrix.trace (Tᵀ * ((R1 * S) * (R1)ᵀ))
      + (4⁻¹ : ℝ) * Matrix.trace (Tᵀ * ((R2 * S) * (R2)ᵀ))
      + (4⁻¹ : ℝ) * Matrix.trace (Tᵀ * ((R3 * S) * (R3)ᵀ))) := by
    rw [hp0, hp1, hp2, hp3]
    ring
  rw [hsum]

end MUFPF.Isotropy
