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
import MUFPFormalization.KMaxAlgebra

namespace MUFPF.Demirror

open MUFPF.BottTower  -- k_max/k_max_value（BottTower 结构常数；KMaxAlgebra 同源）

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

/-! =========================================================
    §8 窗口结构 + n_max³ 窗口连接（286f）
   ========================================================= -/

/-- 286f M3：n_max³ 窗口连接恒等 (k+2)³ − k(2k²−3) = (8−k)(k+1)²。 -/
theorem nmax_window_identity : ∀ k : ℤ, (k + 2) ^ 3 - k * (2 * k * k - 3) = (8 - k) * (k + 1) ^ 2 := by
  intro k
  ring

/-- 286f M3：n_max³ = k·(窗口和−3) 的唯一正整数解 k=8
    （因式分解 (8−k)(k+1)²，(k+1)²=0 → k=−1 被 k≥2 排除）。 -/
theorem nmax_cube_unique : ∀ k : ℤ, k ≥ 2 → (k + 2) ^ 3 = k * (2 * k * k - 3) → k = 8 := by
  intro k hk h
  have hident : (k + 2) ^ 3 - k * (2 * k * k - 3) = (8 - k) * (k + 1) ^ 2 := by
    exact nmax_window_identity k
  have hzero : (8 - k) * (k + 1) ^ 2 = 0 := by
    nlinarith [hident, h]
  rcases mul_eq_zero.mp hzero with h8 | hsq
  · nlinarith [h8]
  · have hkp1 : k + 1 = 0 := by
      exact sq_eq_zero_iff.mp hsq
    nlinarith [hk, hkp1]

/-- 286f 联合主定理：n_max³ 窗口连接恒等 + 唯一性。 -/
theorem window_structure_judgement :
    (∀ k : ℤ, (k + 2) ^ 3 - k * (2 * k * k - 3) = (8 - k) * (k + 1) ^ 2) ∧
    (∀ k : ℤ, k ≥ 2 → (k + 2) ^ 3 = k * (2 * k * k - 3) → k = 8) := by
  constructor
  · exact nmax_window_identity
  · exact nmax_cube_unique

/-! =========================================================
    §9 窗口单参数生成 + C 分母窗口算术唯一性（286g）
   ========================================================= -/

/-- 286g M1a：窗口左端 = 对称轴 k(k−3) 按步长 k 前进两步（S+2k，全 k 恒等）。
    δ∞ 分母 k(k−1) 由此获得对称轴步进生成规则（公设侧连接；k=8 时 56 = 40+16）。 -/
theorem window_left_axis_identity : ∀ k : ℤ, k * (k - 1) = k * (k - 3) + 2 * k := by
  intro k
  ring

/-- 286g M1b：窗口中心 = 对称轴前进三步（S+3k，全 k 恒等；k=8 时 64 = 40+24）。 -/
theorem window_center_axis_identity : ∀ k : ℤ, k * k = k * (k - 3) + 3 * k := by
  intro k
  ring

/-- 286g M2：C 分母 2^(k−1) = 2k²（窗口中间两项和）唯一正整数解 k=8。
    等价约化 2^(k−1)=2k² ⟺ 2^(k−2)=k²（k≥2），k≤8 枚举排除、k≥9 由
    KMaxAlgebra.two_pow_subtwo_gt_sq（266）矛盾——C 分母唯一性与 k_max=8 代数必然性同根。 -/
theorem c_pow_window_sum_unique : ∀ k : ℕ, 2 ≤ k → 2 ^ (k - 1) = 2 * k ^ 2 → k = 8 := by
  intro k hk h
  by_cases hle : k ≤ 8
  · interval_cases k <;> norm_num at h <;> try omega
  · have hge : 9 ≤ k := by omega
    have hgt : 2 ^ (k - 2) > k ^ 2 := MUFPF.KMaxAlgebra.two_pow_subtwo_gt_sq k hge
    have hsub : k - 2 + 1 = k - 1 := by omega
    have hpow : 2 ^ (k - 1) = 2 * (2 ^ (k - 2)) := by
      rw [← hsub, pow_succ]
      rw [Nat.mul_comm]
    rw [hpow] at h
    have hpos : (0 : ℕ) < 2 := by norm_num
    have hgt' : 2 * k ^ 2 < 2 * (2 ^ (k - 2)) := Nat.mul_lt_mul_of_pos_left hgt hpos
    exact False.elim (ne_of_lt hgt' h.symm)

/-- 286g 联合主定理：窗口单参数生成两恒等 + C 分母唯一性 + k=8 交点实例。 -/
theorem window_axis_pow_judgement :
    (∀ k : ℤ, k * (k - 1) = k * (k - 3) + 2 * k) ∧
    (∀ k : ℤ, k * k = k * (k - 3) + 3 * k) ∧
    (∀ k : ℕ, 2 ≤ k → 2 ^ (k - 1) = 2 * k ^ 2 → k = 8) ∧
    ((2 : ℕ) ^ (8 - 1) = 2 * 8 ^ 2) := by
  constructor
  · exact window_left_axis_identity
  constructor
  · exact window_center_axis_identity
  constructor
  · exact c_pow_window_sum_unique
  · norm_num

/-! =========================================================
    §10 E 项闭式升格：双唯一性组装 39/2000（286h）
   ========================================================= -/

/-- 286h M1a：E 项分子 k(k−3)−1 唯一正整数根 k=8。
    39 = k(k−3)−1 → k(k−3)=40 → (k−8)(k+5)=0（286① 对称轴唯一性同根）。 -/
theorem e_numerator_axis_unique : ∀ k : ℤ, k ≥ 2 → k * (k - 3) - 1 = 39 → k = 8 := by
  intro k hk h
  have hsq : k * (k - 3) = 40 := by
    nlinarith
  have hfac : (k - 8) * (k + 5) = k * (k - 3) - 40 := by
    ring
  have hq : (k - 8) * (k + 5) = 0 := by
    rw [hfac]
    nlinarith [hsq]
  rcases mul_eq_zero.mp hq with h8 | hn5
  · omega
  · nlinarith [hk, hn5]

/-- 286h M1b：E 项分母 16(k−3)³ 唯一正整数根 k=8。
    16(k−3)³=2000 → (k−3)³=125=5³ → k−3=5（286d n_max 代数必然 + 286f nmax_cube_unique 同根）。
    k≤9 枚举排除；k≥10 时 (k−3)≥7 → 16(k−3)³≥16·7³=5488>2000 矛盾。 -/
theorem e_denominator_cube_unique : ∀ k : ℕ, 2 ≤ k → 16 * (k - 3) ^ 3 = 2000 → k = 8 := by
  intro k hk h
  by_cases hle : k ≤ 9
  · interval_cases k <;> norm_num at h <;> omega
  · have hge : 10 ≤ k := by omega
    have hk3 : 7 ≤ k - 3 := by omega
    have hpow : 7 ^ 3 ≤ (k - 3) ^ 3 := Nat.pow_le_pow_left hk3 3
    have hlb : 5488 ≤ 16 * (k - 3) ^ 3 := by
      nlinarith [Nat.mul_le_mul_left 16 hpow]
    nlinarith [hlb, h]

/-- 286h M2：E 项闭式值 E(8) = 39/2000（双唯一性同根组装，无自由参数）。 -/
theorem e_closed_form_value : ((8 * (8 - 3) - 1 : ℚ) / (16 * (8 - 3) ^ 3)) = (39 : ℚ) / 2000 := by
  norm_num

/-- 286h 联合主定理：E 项分子唯一性 ∧ 分母唯一性 ∧ 闭式值 39/2000（判别④代数侧升格）。 -/
theorem e_closed_judgement :
    (∀ k : ℤ, k ≥ 2 → k * (k - 3) - 1 = 39 → k = 8) ∧
    (∀ k : ℕ, 2 ≤ k → 16 * (k - 3) ^ 3 = 2000 → k = 8) ∧
    ((8 * (8 - 3) - 1 : ℚ) / (16 * (8 - 3) ^ 3) = (39 : ℚ) / 2000) := by
  constructor
  · exact e_numerator_axis_unique
  constructor
  · exact e_denominator_cube_unique
  · exact e_closed_form_value

/-! =========================================================
    §11 E1/E2 家族资格构造侧：k_max 邻域结构 + 对称轴取值连接（286i）
   ========================================================= -/

/-- 286i M1a：E1 家族 k 集 {3,4,5,8} → C 分子 2k−3 ∈ {3,5,7,13}
    = {k_max−5, k_max−3, k_max−1, k_max+5}（k_max=8 邻域结构；实例枚举）。 -/
theorem e1_k_membership : ∀ k : ℤ,
    (k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 8) →
    (2 * k - 3 = 3 ∨ 2 * k - 3 = 5 ∨ 2 * k - 3 = 7 ∨ 2 * k - 3 = 13) := by
  intro k hk
  rcases hk with rfl | rfl | rfl | rfl <;> norm_num

/-- 286i M1b：E2 家族 k 集 {6,8} → k−3 ∈ {3,5} = E1 集合初始段
    （k_max−2=6 恰为 266 方程 2^(k−2)=k² 的指数参数底；E1 跳过、E2 持有）。 -/
theorem e2_k_membership : ∀ k : ℤ,
    (k = 6 ∨ k = 8) → (k - 3 = 3 ∨ k - 3 = 5) := by
  intro k hk
  rcases hk with rfl | rfl <;> norm_num

/-- 286i M3：E1 k 集 {3,4,5,8} ∩ E2 k 集 {6,8} 唯一公共元 k=8
    （E1 覆盖 {k_max−5,−4,−3,k_max}、E2 覆盖 {k_max−2,k_max}，E1 跳过 k_max−2
     → 交叉唯一性 = 判别设计的结构实现）。 -/
theorem e1e2_cross_unique_k8 : ∀ k : ℤ,
    (k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 8) → (k = 6 ∨ k = 8) → k = 8 := by
  intro k h1 h2
  rcases h1 with hk3 | hk4 | hk5 | hk8
  · subst hk3
    omega
  · subst hk4
    omega
  · subst hk5
    omega
  · subst hk8
    omega

/-- 286i M4：E1/E2 对称轴取值和关于窗口左端（δ∞ 分母）对称差 ±2
    E1 轴值和 = S(3)+S(4)+S(5)+S(8) = 54 = 8·(8−1) − 2
    E2 轴值和 = S(6)+S(8) = 58 = 8·(8−1) + 2
    ±2 = D/E 分子差恒 2（286d mol_diff_two）——E1/E2 与 δ∞ 分母 + D/E 分子差连接。 -/
theorem axis_sum_window_left_pair :
    ((3 * (3 - 3) + 4 * (4 - 3) + 5 * (5 - 3) + 8 * (8 - 3) : ℤ) = 8 * (8 - 1) - 2) ∧
    ((6 * (6 - 3) + 8 * (8 - 3) : ℤ) = 8 * (8 - 1) + 2) := by
  constructor <;> norm_num

/-- 286i 联合主定理：E1/E2 家族 k 集成员资格 + 交叉唯一性 + 轴值和窗口左端对称对。 -/
theorem e1e2_neighborhood_judgement :
    (∀ k : ℤ, (k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 8) →
      (2 * k - 3 = 3 ∨ 2 * k - 3 = 5 ∨ 2 * k - 3 = 7 ∨ 2 * k - 3 = 13)) ∧
    (∀ k : ℤ, (k = 6 ∨ k = 8) → (k - 3 = 3 ∨ k - 3 = 5)) ∧
    (∀ k : ℤ, (k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 8) → (k = 6 ∨ k = 8) → k = 8) ∧
    ((3 * (3 - 3) + 4 * (4 - 3) + 5 * (5 - 3) + 8 * (8 - 3) : ℤ) = 8 * (8 - 1) - 2) ∧
    ((6 * (6 - 3) + 8 * (8 - 3) : ℤ) = 8 * (8 - 1) + 2) := by
  constructor
  · exact e1_k_membership
  constructor
  · exact e2_k_membership
  constructor
  · exact e1e2_cross_unique_k8
  constructor
  · exact axis_sum_window_left_pair.1
  · exact axis_sum_window_left_pair.2

/-! =========================================================
    §12 E1/E2 家族资格构造侧（第二方向）：两层筛唯一性 + E 项分子素因子连接（286i）
   ========================================================= -/

/-- 286i（第二方向）M1：E1/E2 两层筛交叉唯一性（全 ℕ 域，析取成员 + omega）。
    E1 判据 2k−3 ∈ {3,5,7,13}（k 集 {3,4,5,8}）、E2 判据 k−3 ∈ {3,5}（k 集 {6,8}）；
    E2 分支 k=6 时 2k−3=9 落 E1 判据外（矛盾），k=8 直接命中。与 §11 e1e2_cross_unique_k8
    及 297 T5 enhanced_unique 同源，此处以全 ℕ 域证明（非区间枚举）。 -/
theorem e1_e2_cross_unique :
    ∀ k : ℕ, 2 ≤ k →
    (2 * k - 3 = 3 ∨ 2 * k - 3 = 5 ∨ 2 * k - 3 = 7 ∨ 2 * k - 3 = 13) →
    (k - 3 = 3 ∨ k - 3 = 5) → k = 8 := by
  intro k hk h1 h2
  rcases h2 with hk6 | hk8
  · have hk6' : k = 6 := by omega
    subst k
    omega
  · omega

/-- 286i（第二方向）M3：E 项分子 39 素因子连接——39 = 3·13（E1 值集首项 3 × 末项 13）。 -/
theorem e_39_factor_pair : (39 : ℕ) = 3 * 13 := by
  norm_num

/-- 286i（第二方向）M2：E2 值集 {3,5} ⊆ E1 值集 {3,5,7,13}（初始段，§11 M1 观察的机检化）。 -/
theorem e2_values_in_e1 :
    (3 = 3 ∨ 3 = 5 ∨ 3 = 7 ∨ 3 = 13) ∧
    (5 = 3 ∨ 5 = 5 ∨ 5 = 7 ∨ 5 = 13) := by
  norm_num

/-- 286i（第二方向）联合主定理：两层筛交叉唯一性 ∧ 39=3·13 素因子对 ∧ E2 值集初始段。 -/
theorem e1e2_construction_judgement :
    (∀ k : ℕ, 2 ≤ k →
      (2 * k - 3 = 3 ∨ 2 * k - 3 = 5 ∨ 2 * k - 3 = 7 ∨ 2 * k - 3 = 13) →
      (k - 3 = 3 ∨ k - 3 = 5) → k = 8) ∧
    ((39 : ℕ) = 3 * 13) ∧
    ((3 = 3 ∨ 3 = 5 ∨ 3 = 7 ∨ 3 = 13) ∧ (5 = 3 ∨ 5 = 5 ∨ 5 = 7 ∨ 5 = 13)) := by
  constructor
  · exact e1_e2_cross_unique
  constructor
  · exact e_39_factor_pair
  · exact e2_values_in_e1

/-! =========================================================
    §13 13 生成链通式恒等 + 闭式 m 通式组装（286o）
   ========================================================= -/

/-- 286o M1：13 生成链通式恒等——2k−3 = k+(k−3)（任意 k；k=8 时 = k+5，E2 值集末项视角，
    与 §11 E1/E2 家族资格及 39=3·13 素因子连接同构）。闭式/Lean 规范化表达 2k−3（框架成员和）。 -/
theorem thirteen_sum_identity : ∀ k : ℚ, 2 * k - 3 = k + (k - 3) := by
  intro k
  ring

/-- 286o M2：判别④闭式 1/B*(m) 的 m 通式 k_max 组装恒等（k_max=8 实例）——
    五个系数逐项等于统一族 k=8 组装表达（k8_C/D/E），∀ m : ℚ 无条件成立（逐项系数恒等，不涉除法条件）。 -/
theorem closed_form_kmax_assembly (m : ℚ) :
    m / 2 + 1 / 8 + ((13 : ℚ) / 128) / m + ((41 : ℚ) / 2000) / m ^ 2 - ((39 : ℚ) / 2000) / m ^ 3
      = m / 2 + 1 / 8 + ((2 * 8 - 3 : ℚ) / (2 ^ (8 - 1))) / m
        + ((8 * (8 - 3) + 1 : ℚ) / (16 * (8 - 3) ^ 3)) / m ^ 2
        - ((8 * (8 - 3) - 1 : ℚ) / (16 * (8 - 3) ^ 3)) / m ^ 3 := by
  rw [← k8_C, ← k8_D, ← k8_E]

/-- 286o 联合主定理：13 通式恒等 ∧ 闭式 m 通式 k_max 组装（判别④ E 项内生组装恒等的形式化闭环）。 -/
theorem closed_form_assembly_judgement :
    (∀ k : ℚ, 2 * k - 3 = k + (k - 3)) ∧
    (∀ m : ℚ,
      m / 2 + 1 / 8 + ((13 : ℚ) / 128) / m + ((41 : ℚ) / 2000) / m ^ 2 - ((39 : ℚ) / 2000) / m ^ 3
        = m / 2 + 1 / 8 + ((2 * 8 - 3 : ℚ) / (2 ^ (8 - 1))) / m
          + ((8 * (8 - 3) + 1 : ℚ) / (16 * (8 - 3) ^ 3)) / m ^ 2
          - ((8 * (8 - 3) - 1 : ℚ) / (16 * (8 - 3) ^ 3)) / m ^ 3) := by
  constructor
  · exact thirteen_sum_identity
  · exact closed_form_kmax_assembly

/-! =========================================================
    §14 G1/G2 推进：碗形链-窗口恒等（286r，2026-10-31）
   ========================================================= -/

/-- G2：线性项系数 1/2 = k_max²/2^(k_max−1)（窗口中心 k_max² / 2 幂分母，
    与 C 项共享分母 2^(k_max−1)=128；m/2 = m·k_max²/2^(k_max−1)）。 -/
theorem linear_coeff_window_pow : (k_max : ℚ) ^ 2 / (2 : ℚ) ^ (k_max - 1) = 1 / 2 := by
  norm_num [k_max_value]

/-- G2：常数项 1/8 = k_max²/2^(k_max+1)（窗口中心 / 2^(k_max+1)=512，
    与碗形候选 3/512 共享分母 512=2^(k_max+1)，BowlLayer bowl_den_512 同谱）。 -/
theorem constant_coeff_window_pow : (k_max : ℚ) ^ 2 / (2 : ℚ) ^ (k_max + 1) = 1 / 8 := by
  norm_num [k_max_value]

/-- G1：C 项碗形链恒等——13/128 = h(2)·(k_max+5)/(2·(k_max−1))（h(2)=(k_max−1)/2^(k_max−2)
    消去 (k_max−1) 后 = (k_max+5)/2^(k_max−1)——C 与碗形链第一层 h(2) 同 2 幂分母谱）。 -/
theorem c_bowlchain_h2_scale : ((7 : ℚ) / 64) * (k_max + 5 : ℚ) / (2 * (k_max - 1) : ℚ) = 13 / 128 := by
  norm_num [k_max_value]

/-- G1：C 项框架形式 (k_max+5)/2^(k_max−1) = 13/128（与 k8_C 的 2k−3 表达同值——
    13 双表达判别 06b1578：2k−3=k+(k−3) 通式恒等，k_max=8 时 = k_max+5）。 -/
theorem c_dual_form_pow : (k_max + 5 : ℚ) / (2 : ℚ) ^ (k_max - 1) = 13 / 128 := by
  norm_num [k_max_value]

/-- G1：E 项碗形链放大恒等——39/2000 = i(2)·(N_gen/2)³（i(2)=13/2250 候选，
    (3/2)³=27/8；框架形式 (k_max+5)·N_gen/(2⁴·(k_max−3)³)，i2_cand2_kmax 同族）。 -/
theorem e_bowlchain_i2_scale : ((13 : ℚ) / 2250) * (3 / 2 : ℚ) ^ 3 = 39 / 2000 := by
  norm_num

/-- G1：E 项双形式同值（碗形链 × 窗口）——(k_max−5)(k_max+5)/(2⁴·(k_max−3)³) = 39/2000
    （分子 39=(k_max−5)(k_max+5)，BowlLayer e39_factor；分母与 k8_E 同）。 -/
theorem e_dual_form_same : ((k_max - 5) * (k_max + 5) : ℚ) / ((2 : ℚ) ^ 4 * (k_max - 3 : ℚ) ^ 3) = 39 / 2000 := by
  norm_num [k_max_value]

/-- G1：39 双身份交叉唯一性——∀k≥1，(k−5)(k+5)=k(k−3)−1 ⟹ k=8
    （左−右 = 3(k−8)：BowlLayer 平方差身份（39=k_max²−5²）与 286h 窗口身份（39=k_max(k_max−3)−1）
    同值的唯一根 k_max=8，E 项分子双生成链的唯一性判别）。 -/
theorem e_dual_identity_unique : ∀ k : ℤ, k ≥ 1 → (k - 5) * (k + 5) = k * (k - 3) - 1 → k = 8 := by
  intro k hk h
  have hid : (k - 5) * (k + 5) - (k * (k - 3) - 1) = 3 * (k - 8) := by ring
  have hz : (k - 5) * (k + 5) - (k * (k - 3) - 1) = 0 := by
    rw [h]
    ring
  have hd : 3 * (k - 8) = 0 := by linarith
  have hk8 : k - 8 = 0 := by
    exact (mul_eq_zero.mp hd).resolve_left (by norm_num : (3 : ℤ) ≠ 0)
  omega

/-- G1：D 项碗形链层序-幂次对应反例登记——D/h′(2) = 123/130（含 41 素因子，非框架量）。
    层序-幂次强对应假说（h↔1/m、h′↔1/m²、i↔1/m³ 三负幂全部由碗形链三层导出）
    被 D 反例部分证伪——D 保持窗口表达（对称轴 40+1）。 -/
theorem d_bowlchain_counter : ((41 : ℚ) / 2000) / ((13 : ℚ) / 600) = 123 / 130 := by
  norm_num

/-- 286r 联合主定理：线性/常数项窗口中心 2 幂谱 ∧ C↔h(2) ∧ E↔i(2)·(N_gen/2)³ ∧
    39 双身份唯一性 ∧ D 反例登记（G1/G2 碗形链-闭式恒等判别，数值先证伪 23/23 ALL_PASS）。 -/
theorem bowlchain_scale_judgement :
    ((k_max : ℚ) ^ 2 / (2 : ℚ) ^ (k_max - 1) = 1 / 2) ∧
    ((k_max : ℚ) ^ 2 / (2 : ℚ) ^ (k_max + 1) = 1 / 8) ∧
    (((7 : ℚ) / 64) * (k_max + 5 : ℚ) / (2 * (k_max - 1) : ℚ) = 13 / 128) ∧
    (((13 : ℚ) / 2250) * (3 / 2 : ℚ) ^ 3 = 39 / 2000) ∧
    (∀ k : ℤ, k ≥ 1 → (k - 5) * (k + 5) = k * (k - 3) - 1 → k = 8) ∧
    (((41 : ℚ) / 2000) / ((13 : ℚ) / 600) = 123 / 130) := by
  constructor
  · exact linear_coeff_window_pow
  constructor
  · exact constant_coeff_window_pow
  constructor
  · exact c_bowlchain_h2_scale
  constructor
  · exact e_bowlchain_i2_scale
  constructor
  · exact e_dual_identity_unique
  · exact d_bowlchain_counter

/-! =========================================================
    §15 G3 推进：E1/E2 家族资格角色完备性连接（286r-g3，2026-10-31）
   ========================================================= -/

/-- G3 A1+A2：E1 值集成员 3 与 5 的代数端角色——3·13=39（E 项素因子通道，§12 e_39_factor_pair
    同族；39=(k_max−5)(k_max+5)）且 5=k_max−3（D/E 分母立方底，5³=125）。 -/
theorem e1_role_algebra_ends :
    ((3 : ℚ) * 13 = 39) ∧ ((5 : ℚ) = k_max - 3) := by
  constructor
  · norm_num
  · norm_num [k_max_value]

/-- G3 A3：E1 值集成员 7 的碗形链层1分子角色——7=k_max−1（塔顶，286e S604）且
    h(2)=(k_max−1)/2^(k_max−2)=7/64（§14 c_bowlchain_h2_scale 的 h(2) 分子同值）。 -/
theorem e1_role_layer1 :
    ((7 : ℚ) = k_max - 1) ∧ ((7 : ℚ) / 64 = (k_max - 1 : ℚ) / (2 : ℚ) ^ (k_max - 2)) := by
  constructor
  · norm_num [k_max_value]
  · norm_num [k_max_value]

/-- G3 A4：E1 值集成员 13 的 C 与层2·3 分子角色——13=k_max+5（窗口右端 65 素因子）且
    C=(k_max+5)/2^(k_max−1)=13/128（§14 c_dual_form_pow 同值；层2/3 分子 13/600、13/2250
    见 hprime_over_i2 / i2_cand2 族）。 -/
theorem e1_role_c13 :
    ((13 : ℚ) = k_max + 5) ∧ ((13 : ℚ) / 128 = (k_max + 5 : ℚ) / (2 : ℚ) ^ (k_max - 1)) := by
  constructor
  · norm_num [k_max_value]
  · norm_num [k_max_value]

/-- G3 联合主定理：E1 值集 {3,5,7,13} 角色完备性——E 素因子（3·13=39）∧ D/E 分母底
    （5=k_max−3）∧ 碗形链层1分子（7=k_max−1=h(2) 分子）∧ C 分子（13=k_max+5）；
    E2 值集 {3,5} = 代数端角色子集（素因子通道 + 分母因子，不含层分子 7/13）。
    G3 从"判别设计非公设生成（观察级）"推进为"判别设计+角色完备性连接"
    （数值先证伪 11/11 ALL_PASS；偏移选择自由仍非公设生成，286i M4 平凡性限定保留）。 -/
theorem family_role_judgement :
    (((3 : ℚ) * 13 = 39) ∧ ((5 : ℚ) = k_max - 3)) ∧
    (((7 : ℚ) = k_max - 1) ∧ ((7 : ℚ) / 64 = (k_max - 1 : ℚ) / (2 : ℚ) ^ (k_max - 2))) ∧
    (((13 : ℚ) = k_max + 5) ∧ ((13 : ℚ) / 128 = (k_max + 5 : ℚ) / (2 : ℚ) ^ (k_max - 1))) := by
  constructor
  · exact e1_role_algebra_ends
  constructor
  · exact e1_role_layer1
  · exact e1_role_c13

-- §16 G4：B*(m)↔γ 桥接收敛假设判别（286j 诚实边界①——3D/2D Landau 化收敛非已证恒等）
-- 闭式 1/B*(m)=m/2+1/8+13/(128·m)+41/(2000·m²)−39/(2000·m³)（§13 closed_form_kmax_assembly）；
-- 数值先证伪 `scripts/p7_5e286r_g4_convergence.py` 9/9 ALL_PASS（谱单调/归约点谱内性/判据分层）。

/-- G4 B1：闭式谱跨越——1/B*(1)<1<1/B*(2)：2D Landau 归约点 γ=1（B=B₀，ħωc=2Ry 锚）
    落于闭式谱的 (1,2) 通道内（m*≈1.6180，非谱点；B₀ 为谱覆盖内标尺）。 -/
theorem bstar_span_cross_one :
    ((1 : ℚ) / 2 + 1 / 8 + 13 / (128 * (1 : ℚ)) + 41 / (2000 * (1 : ℚ) ^ 2)
        - 39 / (2000 * (1 : ℚ) ^ 3) < 1) ∧
    (1 < (2 : ℚ) / 2 + 1 / 8 + 13 / (128 * (2 : ℚ)) + 41 / (2000 * (2 : ℚ) ^ 2)
        - 39 / (2000 * (2 : ℚ) ^ 3)) := by
  constructor
  · norm_num
  · norm_num

/-- G4 A2 首步：1/B* 谱单调递增的谱域首步——Δ(1)=1/B*(2)−1/B*(1)>0
    （14429/32000；γ* 谱递减的必要结构，m=1..11 全正见数值判别）。 -/
theorem bstar_first_diff_positive :
    0 < (2 : ℚ) / 2 + 1 / 8 + 13 / (128 * (2 : ℚ)) + 41 / (2000 * (2 : ℚ) ^ 2)
      - 39 / (2000 * (2 : ℚ) ^ 3)
      - ((1 : ℚ) / 2 + 1 / 8 + 13 / (128 * (1 : ℚ)) + 41 / (2000 * (1 : ℚ) ^ 2)
          - 39 / (2000 * (1 : ℚ) ^ 3)) := by
  norm_num

/-- G4 联合主定理：桥接收敛假设必要条件——闭式谱跨越 B₀ 归约点（γ=1 谱内）∧
    谱单调首步正（γ* 递减结构）——与 σ_score 达标口径（286k σ_score=0.05）
    及收敛容差 Δ=1e-3（286j M4）分层登记：Δ 为 3D→2D 数值归约收敛容差（假设判据），
    非达标口径；3D→2D Landau 化收敛恒等证明仍开放（G4 登记升级非关闭；
    数值巧合候选 m*≈φ 偏差 17.5 ppm 登记不升格）。 -/
theorem g4_bridge_judgement :
    (((1 : ℚ) / 2 + 1 / 8 + 13 / (128 * (1 : ℚ)) + 41 / (2000 * (1 : ℚ) ^ 2)
        - 39 / (2000 * (1 : ℚ) ^ 3) < 1) ∧
     (1 < (2 : ℚ) / 2 + 1 / 8 + 13 / (128 * (2 : ℚ)) + 41 / (2000 * (2 : ℚ) ^ 2)
        - 39 / (2000 * (2 : ℚ) ^ 3))) ∧
    (0 < (2 : ℚ) / 2 + 1 / 8 + 13 / (128 * (2 : ℚ)) + 41 / (2000 * (2 : ℚ) ^ 2)
      - 39 / (2000 * (2 : ℚ) ^ 3)
      - ((1 : ℚ) / 2 + 1 / 8 + 13 / (128 * (1 : ℚ)) + 41 / (2000 * (1 : ℚ) ^ 2)
          - 39 / (2000 * (1 : ℚ) ^ 3))) := by
  constructor
  · exact bstar_span_cross_one
  · exact bstar_first_diff_positive

end MUFPF.Demirror
