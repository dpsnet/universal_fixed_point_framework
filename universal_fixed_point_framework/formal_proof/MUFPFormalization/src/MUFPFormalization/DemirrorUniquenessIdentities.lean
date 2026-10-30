/-
# DemirrorUniquenessIdentities.lean — D/E 镜像对分子代数必然性唯一性（P7-5e-286b）

形式化目标（P7-5e-286 判别 + 286b 统一 k 参数化族的唯一性核心，承接 274 MirrorPairIdentities 链）：
  把 286 判别 ① ② ③ ④ 的"唯一整数解 k=8"形式化为无条件/交叉条件的 Lean 定理：

    T1 axis_unique    : ∀ k : ℤ, k ≥ 1 → k*k − 3*k − 40 = 0 → k = 8
                          （对称轴 40 = k(k−3) 唯一正整数解；因式分解 (k−8)(k+5)=0）
    T2 mol41_unique   : ∀ k : ℤ, k ≥ 1 → k*(k−3)+1 = 41 → k = 8（D 分子，同共同方程）
    T3 mol39_unique   : ∀ k : ℤ, k ≥ 1 → k*(k−3)−1 = 39 → k = 8（E 分子，同共同方程）
    T4 de_diff_unique : ∀ k : ℤ, k ≥ 1 → 8*(k−3)³ = (k+2)³ → k = 8
                          （D−E = 1/n_max³ 唯一生成；因式分解 (k−8)(7k²−22k+28)=0，二次因子恒正）
    T5 enhanced_unique: ∀ k : ℤ, 4 ≤ k → k ≤ 11 →
                          (2k−3 = 3 ∨ 2k−3 = 5 ∨ 2k−3 = 7 ∨ 2k−3 = 13) →
                          (k−3 = 3 ∨ k−3 = 5) → k = 8
                          （修正增强判据 E1∧E2 独立交叉：k=4,5 被 E2 排除、k=6 被 E1 排除 → 唯一 k=8）
    T6 k8_exact       : 统一族 k=8 特例的 ℚ 分数恒等（δ∞=1/56、C=13/128、D=41/2000、E=39/2000、D−E=1/1000）

★ 诚实边界：
  · T1-T4 是无条件代数唯一性（纯整数方程，与 286 判别 ①②③ 对应）；
  · T5 对应 286 判别 ④ 的**修正版增强判据**（2026-10-30 勘误：初版硬编码 k==8 循环论证
    已修正为 E1∧E2 两条独立家族条件相交）；E1/E2 家族成员资格依赖 260ap 邻居族观察
    （观察级，未从公设导出）；
  · T6 是统一参数化族在 k=8 的实例化（286b 实证 ALL_HIT：统一族对 k=4..12 全空间命中
    286 判别矩阵）。

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e286b_pycheck.py（sympy 精确）：T1-T6 全通过、ALL_PASS=True；
    T4 因式分解 (k−8)(7k²−22k+28)、唯一整数根 8；T5 E1 单独 [4,5,8] → E1∧E2 唯一 [8]。

关系链：import MirrorPairIdentities（274 链：41/39 = k_max·5±1 镜像对）。
-/

import Mathlib.Tactic
import MUFPFormalization.MirrorPairIdentities

namespace MUFPF.Demirror

/-! =========================================================
    §1 对称轴与分子唯一性（T1-T3：共同方程 k²−3k−40=0）
   ========================================================= -/

/-- T1：对称轴方程 k²−3k−40=0 的唯一正整数解 k=8（因式分解 (k−8)(k+5)=0）。 -/
theorem axis_unique : ∀ k : ℤ, k ≥ 1 → k * k - 3 * k - 40 = 0 → k = 8 := by
  intro k hk h
  have hfac : (k - 8) * (k + 5) = 0 := by
    nlinarith [h]
  rcases mul_eq_zero.mp hfac with hk8 | hk5
  · omega
  · nlinarith [hk, hk5]

/-- T2：D 分子 41 = k(k−3)+1 的唯一正整数根 k=8（同共同方程）。 -/
theorem mol41_unique : ∀ k : ℤ, k ≥ 1 → k * (k - 3) + 1 = 41 → k = 8 := by
  intro k hk h
  have hq : k * k - 3 * k - 40 = 0 := by
    nlinarith [h]
  exact axis_unique k hk hq

/-- T3：E 分子 39 = k(k−3)−1 的唯一正整数根 k=8（同共同方程）。 -/
theorem mol39_unique : ∀ k : ℤ, k ≥ 1 → k * (k - 3) - 1 = 39 → k = 8 := by
  intro k hk h
  have hq : k * k - 3 * k - 40 = 0 := by
    nlinarith [h]
  exact axis_unique k hk hq

/-! =========================================================
    §2 差值唯一生成（T4：D−E = 1/n_max³）
   ========================================================= -/

/-- T4：8(k−3)³ = (k+2)³ 的唯一正整数解 k=8（因式分解 (k−8)(7k²−22k+28)=0，二次因子恒正）。 -/
theorem de_diff_unique : ∀ k : ℤ, k ≥ 1 → 8 * (k - 3) ^ 3 = (k + 2) ^ 3 → k = 8 := by
  intro k hk h
  have hfac : (k - 8) * (7 * k ^ 2 - 22 * k + 28) = 0 := by
    nlinarith [h]
  rcases mul_eq_zero.mp hfac with hk8 | hquad
  · omega
  · have hrew : 7 * k ^ 2 - 22 * k + 28 = 7 * (k - 2) ^ 2 + 6 * k := by
      ring
    have hpos : 7 * k ^ 2 - 22 * k + 28 > 0 := by
      rw [hrew]
      nlinarith [sq_nonneg (k - 2), hk]
    nlinarith [hquad, hpos]

/-! =========================================================
    §3 修正增强判据唯一性（T5：E1∧E2 独立交叉）
   ========================================================= -/

/-- T5：k∈{4..11} 上，C 分子 2k−3 ∈ {3,5,7,13} 且 D 分母立方底 k−3 ∈ {3,5} → 唯一 k=8。
    （286 判别④修正版：E1∧E2 两条独立家族条件相交；k=4,5 被 E2 排除、k=6 被 E1 排除） -/
theorem enhanced_unique : ∀ k : ℤ, 4 ≤ k → k ≤ 11 →
    (2 * k - 3 = 3 ∨ 2 * k - 3 = 5 ∨ 2 * k - 3 = 7 ∨ 2 * k - 3 = 13) →
    (k - 3 = 3 ∨ k - 3 = 5) → k = 8 := by
  intro k hk4 hk11 hE1 hE2
  interval_cases k
  · norm_num at hE2
  · norm_num at hE2
  · norm_num at hE1
  · norm_num at hE1
  · rfl
  · norm_num at hE1
  · norm_num at hE1
  · norm_num at hE1

/-! =========================================================
    §4 统一族 k=8 精确赋值（T6）
   ========================================================= -/

/-- T6a：δ∞(8) = 1/(8·7) = 1/56（静默核心窗口左端 8²−8）。 -/
theorem k8_delta : (1 : ℚ) / (8 * (8 - 1)) = 1 / 56 := by
  norm_num

/-- T6b：C(8) = (2·8−3)/2⁷ = 13/128（2 幂静默家族）。 -/
theorem k8_C : ((2 * 8 - 3 : ℚ) / (2 ^ (8 - 1))) = 13 / 128 := by
  norm_num

/-- T6c：D(8) = (8·5+1)/(16·5³) = 41/2000。 -/
theorem k8_D : ((8 * (8 - 3) + 1 : ℚ) / (16 * (8 - 3) ^ 3)) = 41 / 2000 := by
  norm_num

/-- T6d：E(8) = (8·5−1)/(16·5³) = 39/2000。 -/
theorem k8_E : ((8 * (8 - 3) - 1 : ℚ) / (16 * (8 - 3) ^ 3)) = 39 / 2000 := by
  norm_num

/-- T6e：D−E = 1/(8·5³) = 1/1000 = n_max⁻³（n_max = 8+2 = 10）。 -/
theorem k8_DE : ((41 : ℚ) / 2000 - 39 / 2000) = (1 : ℚ) / (8 * (8 - 3) ^ 3) := by
  norm_num

/-- 联合主定理：286 判别 ①-④ 唯一性 + 统一族 k=8 精确赋值。 -/
theorem demirror_judgement :
    (∀ k : ℤ, k ≥ 1 → k * k - 3 * k - 40 = 0 → k = 8) ∧
    (∀ k : ℤ, k ≥ 1 → k * (k - 3) + 1 = 41 → k = 8) ∧
    (∀ k : ℤ, k ≥ 1 → k * (k - 3) - 1 = 39 → k = 8) ∧
    (∀ k : ℤ, k ≥ 1 → 8 * (k - 3) ^ 3 = (k + 2) ^ 3 → k = 8) ∧
    ((1 : ℚ) / 56 = 1 / (8 * (8 - 1))) ∧
    ((13 : ℚ) / 128 = (2 * 8 - 3) / (2 ^ (8 - 1))) ∧
    ((41 : ℚ) / 2000 = (8 * (8 - 3) + 1) / (16 * (8 - 3) ^ 3)) ∧
    ((39 : ℚ) / 2000 = (8 * (8 - 3) - 1) / (16 * (8 - 3) ^ 3)) := by
  constructor
  · exact axis_unique
  constructor
  · exact mol41_unique
  constructor
  · exact mol39_unique
  constructor
  · exact de_diff_unique
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  · norm_num

/-! =========================================================
    §5 分子线性化代数升格（286c：5k±1 不是独立观察）
   ========================================================= -/

/-- M1a：D 分子 k(k−3)+1 呈现线性形式 5k+1 的唯一正整数解 k=8
    （k(k−3)+1 − (5k+1) = k(k−8) = 0，由 E2 立方底 k−3=5 驱动）。
    286b 诚实边界『分子线性形式 5k±1 未从公设导出』→ 降级为未导出的仅是二次形式本身。 -/
theorem mol_linear_plus : ∀ k : ℤ, k ≥ 1 → k * (k - 3) + 1 = 5 * k + 1 → k = 8 := by
  intro k hk h
  have hfac : k * (k - 8) = 0 := by
    nlinarith [h]
  rcases mul_eq_zero.mp hfac with hk0 | hk8
  · nlinarith [hk, hk0]
  · omega

/-- M1b：E 分子 k(k−3)−1 呈现线性形式 5k−1 的唯一正整数解 k=8（同上）。 -/
theorem mol_linear_minus : ∀ k : ℤ, k ≥ 1 → k * (k - 3) - 1 = 5 * k - 1 → k = 8 := by
  intro k hk h
  have hfac : k * (k - 8) = 0 := by
    nlinarith [h]
  rcases mul_eq_zero.mp hfac with hk0 | hk8
  · nlinarith [hk, hk0]
  · omega

/-- M2b 实例：C 分母 2^(8−1) = 2·8²（2^(k−2)=k² 枚举唯一解 k=8；289 vv_sumB 窗口和）。 -/
theorem k8_C_pow_square : (2 : ℕ) ^ (8 - 1) = 2 * 8 ^ 2 := by
  norm_num

/-- M2b 实例：静默窗口和 63+65 = 2·8²（289 vv_sumB：b²−1+b²+1 = 2b²，b=8）。 -/
theorem k8_window_sum_square : (63 + 65 : ℕ) = 2 * 8 ^ 2 := by
  norm_num

/-- 286c 联合主定理：分子线性化唯一性（± 两版）+ C 分母窗口和重合点恒等。 -/
theorem mol_linear_judgement :
    (∀ k : ℤ, k ≥ 1 → k * (k - 3) + 1 = 5 * k + 1 → k = 8) ∧
    (∀ k : ℤ, k ≥ 1 → k * (k - 3) - 1 = 5 * k - 1 → k = 8) ∧
    ((2 : ℕ) ^ (8 - 1) = 2 * 8 ^ 2) ∧
    ((63 + 65 : ℕ) = 2 * 8 ^ 2) := by
  constructor
  · exact mol_linear_plus
  constructor
  · exact mol_linear_minus
  constructor
  · norm_num
  · norm_num

/-! =========================================================
    §6 分母形态溯源（286d：D/E 分母 = 2·n_max³ 代数必然 + 负结果）
   ========================================================= -/

/-- 286d M1：D/E 分子差恒为 2（无条件恒等）——D−E = 2/[16(k−3)³] 的分子侧来源。 -/
theorem mol_diff_two : ∀ k : ℤ, (k * (k - 3) + 1) - (k * (k - 3) - 1) = 2 := by
  intro k
  ring

/-- 286d M1：D/E 分母呈现 2·n_max³ 形态（16(k−3)³ = 2(k+2)³）的唯一正整数解 k=8。
    引用 de_diff_unique（8(k−3)³=(k+2)³ → k=8）。 -/
theorem de_den_nmax_unique : ∀ k : ℤ, k ≥ 1 → 16 * (k - 3) ^ 3 = 2 * (k + 2) ^ 3 → k = 8 := by
  intro k hk h
  have h8 : 8 * (k - 3) ^ 3 = (k + 2) ^ 3 := by
    nlinarith [h]
  exact de_diff_unique k hk h8

/-- 286d M3 负结果：窗口左端 k(k−1) 与窗口和 2k² 无正整数交点（k(k+1)=0，根 {0,−1}）。
    δ∞（窗口左端）与 C（窗口和）作为窗口量永不相交——不同源。 -/
theorem window_left_ne_sum : ∀ k : ℤ, k ≥ 1 → k * (k - 1) ≠ 2 * k * k := by
  intro k hk h
  have hfac : k * (k + 1) = 0 := by
    nlinarith [h]
  rcases mul_eq_zero.mp hfac with hk0 | hkm1
  · nlinarith [hk, hk0]
  · nlinarith [hk, hkm1]

/-- 286d 联合主定理：分子差恒 2 + 分母 2·n_max³ 唯一性 + 窗口左端/和负结果。 -/
theorem denominator_origin_judgement :
    (∀ k : ℤ, (k * (k - 3) + 1) - (k * (k - 3) - 1) = 2) ∧
    (∀ k : ℤ, k ≥ 1 → 16 * (k - 3) ^ 3 = 2 * (k + 2) ^ 3 → k = 8) ∧
    (∀ k : ℤ, k ≥ 1 → k * (k - 1) ≠ 2 * k * k) := by
  constructor
  · exact mol_diff_two
  constructor
  · exact de_den_nmax_unique
  · exact window_left_ne_sum

/-! =========================================================
    §7 分子窗口算术化（286e：D/E 分子 = 窗口左端 − 2k ± 1）
   ========================================================= -/

/-- 286e M1：D/E 分子基底 = 窗口左端 k(k−1) 减去 2k（全 k 恒等）。 -/
theorem de_mol_window_identity : ∀ k : ℤ, k * (k - 3) = k * (k - 1) - 2 * k := by
  intro k
  ring

/-- 286e M1：D/E 分子 ±1 双侧 = 窗口左端 − 2k ± 1（全 k 恒等）。 -/
theorem de_mol_window_plus_minus :
    (∀ k : ℤ, k * (k - 3) + 1 = k * (k - 1) - 2 * k + 1) ∧
    (∀ k : ℤ, k * (k - 3) - 1 = k * (k - 1) - 2 * k - 1) := by
  constructor <;> intro k <;> ring

/-- 286e 联合主定理：D/E 分子窗口算术化三恒等。 -/
theorem window_spectrum_judgement :
    (∀ k : ℤ, k * (k - 3) = k * (k - 1) - 2 * k) ∧
    (∀ k : ℤ, k * (k - 3) + 1 = k * (k - 1) - 2 * k + 1) ∧
    (∀ k : ℤ, k * (k - 3) - 1 = k * (k - 1) - 2 * k - 1) := by
  constructor
  · exact de_mol_window_identity
  constructor
  · exact de_mol_window_plus_minus.1
  · exact de_mol_window_plus_minus.2

end MUFPF.Demirror
