import MUFPFormalization.MerFermatDualityIdentities

/-!
# P7-5e-286 ★ 核心常数窗口与家族平方 Lean 形式化

对应 roadmap 205（NN+OO）与 209（XX）：
- NN ★ D(9)=16641=129²=a₆² 家族成员平方（D(m+8) 序列家族平方化）+ D(3)=93=3·M₅；
- OO ★ 65·63=M₁₂、7×(8±1) 对偶（56=7·8 vs 63=7·9）、核心常数窗口 [56,63,64,65]=8²−{8,1,0,−1}、
  1/65−1/63=−2/M₁₂；
- XX ★ D(n)=2^(n−1)(7n+2)+1 闭式、1/B*(n)=D(n)/(7·2^n)（有理恒等，n≥1）。

诚实边界：OO 的"修正锚点与 δ∞ 互锁"（OO5）为语义指认，本模块只形式化代数恒等；
NN3"平方化仅 n=9"为枚举事实（需 D(n) 全表），本模块形式化 D(9) 平方恒等与 D(3) 因子。
-/

namespace MUFPF.CoreConstantWindow

open Nat

/-! ## §1 NN：D(n) 闭式与家族平方 -/

/-- D(n) = 2^(n−1)(7n+2)+1（209 XX1 闭式）。 -/
def Dn (n : ℕ) : ℕ := 2^(n-1) * (7*n + 2) + 1

/-- 家族平方展开：a_n² = (2^n+1)² = 2^(2n) + 2^(n+1) + 1（NN3 家族平方化的一般形式）。 -/
theorem nn_square_expand (n : ℕ) : (2^n + 1)^2 = 2^(2*n) + 2^(n+1) + 1 := by
  have hpow2 : 2^(2*n) = 2^n * 2^n := by
    rw [show 2 * n = n + n by omega, pow_add]
  have hsucc : 2^(n+1) = 2 * 2^n := by
    rw [pow_succ]
    exact Nat.mul_comm (2^n) 2
  calc
    (2^n + 1)^2 = (2^n + 1) * (2^n + 1) := by ring
    _ = 2^n * 2^n + 2 * 2^n + 1 := by ring
    _ = 2^(2*n) + 2^(n+1) + 1 := by
      rw [← hpow2]
      rw [← hsucc]

/-- 家族段 a₆ = 2⁷+1 = 129（205 NN2 锚点）。 -/
theorem nn_a6 : 2^7 + 1 = 129 := by norm_num

/-- D(9) 数值 = 16641。 -/
theorem nn_d9_value : Dn 9 = 16641 := by
  unfold Dn
  norm_num

/-- D(9) = 129²（NN2：家族成员平方——唯一平方成员 n=9 的实例）。 -/
theorem nn_d9_square : Dn 9 = 129^2 := by
  unfold Dn
  norm_num

/-- ★ D(9) = a₆² = (2⁷+1)²（代数链：2⁸·65+1 = 2¹⁴+2⁸+1 = (2⁷+1)²）。 -/
theorem nn_d9_a6 : Dn 9 = (2^7 + 1)^2 := by
  unfold Dn
  norm_num

/-- D(9)−1 = 2⁸·65 = b₆·65（209 XX1 实例：256·65 = 2¹⁴+2⁸）。 -/
theorem nn_d9_minus1 : Dn 9 - 1 = 2^8 * 65 := by
  unfold Dn
  norm_num

/-- D(3) = 93 = 3·(2⁵−1) = 3·M₅（NN4：非平凡 Mersenne 因子实例）。 -/
theorem nn_d3_mersenne : Dn 3 = 3 * (2^5 - 1) := by
  unfold Dn
  norm_num

/-- M₅ = 2⁵−1 = 31。 -/
theorem nn_m5 : 2^5 - 1 = 31 := by norm_num

/-! ## §2 OO：65·63 = M₁₂、7×(8±1) 对偶、核心常数窗口 -/

/-- ★ 65·63 = 2¹²−1 = M₁₂（OO1；285 ll3_prod n=6 引用）。 -/
theorem oo1_prod : 65 * 63 = 2^12 - 1 := by
  rw [← MUFPF.MerFermatDuality.ll5_a5, ← MUFPF.MerFermatDuality.ll5_w5]
  exact MUFPF.MerFermatDuality.ll3_prod 6

/-- M₁₂ 数值 = 4095。 -/
theorem oo1_m12 : 2^12 - 1 = 4095 := by norm_num

/-- 7×(8±1) 对偶：56 = 7·8（域宽×满格）∧ 63 = 7·9（域宽×静默单元 9）。 -/
theorem oo2_dual : 7 * 8 = 56 ∧ 7 * 9 = 63 := by constructor <;> norm_num

/-- ★ 核心常数窗口 [56,63,64,65] = 8²−{8,1,0,−1}（OO6）：δ∞ 分母/宽度/满格平方/修正锚点。 -/
theorem oo6_window :
    8^2 - 8 = 56 ∧ 8^2 - 1 = 63 ∧ 8^2 = 64 ∧ 8^2 + 1 = 65 := by
  constructor <;> constructor <;> constructor <;> norm_num

/-- 窗口连续结构：56+7=63（域宽步进）、63+1=64、64+1=65（+1 连续）。 -/
theorem oo6_chain : 56 + 7 = 63 ∧ 63 + 1 = 64 ∧ 64 + 1 = 65 := by
  constructor <;> constructor <;> norm_num

/-- ★ 1/65 − 1/63 = −2/4095 = −2/M₁₂（OO3 有理恒等）。 -/
theorem oo3_frac : (1:ℚ)/65 - (1:ℚ)/63 = -(2:ℚ)/4095 := by
  norm_num

/-- 修正锚点与差恒等互锁（65−63=2，285 ll2_diff 实例同源）。 -/
theorem oo5_diff : 65 - 63 = 2 := by norm_num

/-- 56+9=65：δ∞ 分母 + 根对合常数 9 = 修正锚点（OO5 代数侧实例）。 -/
theorem oo5_bridge : 56 + 9 = 65 := by norm_num

/-! ## §3 XX：闭式有理恒等 1/B*(n) = D(n)/(7·2^n)（209 XX2） -/

/-- D(n) 闭式定义恒等（XX1）。 -/
theorem xx1_dn (n : ℕ) : Dn n = 2^(n-1) * (7*n + 2) + 1 := by rfl

/-- 1/B*(3) = D(3)/(7·2³)：3/2+1/7+1/56 = 93/56。 -/
theorem xx2_n3 : (3:ℚ)/2 + (1:ℚ)/7 + (1:ℚ)/(7*2^3) = (Dn 3 : ℚ)/(7*2^3) := by
  unfold Dn
  norm_num

/-- 1/B*(9) = D(9)/(7·2⁹)：9/2+1/7+1/(7·2⁹) = 16641/3584。 -/
theorem xx2_n9 : (9:ℚ)/2 + (1:ℚ)/7 + (1:ℚ)/(7*2^9) = (Dn 9 : ℚ)/(7*2^9) := by
  unfold Dn
  norm_num

/-! ## §4 联合主定理 -/

/-- ★★ NN×OO×XX 联合：家族平方 ∧ M₁₂ 积 ∧ 7×(8±1) 对偶 ∧ 核心窗口 ∧ 有理差分恒等 ∧ 闭式。 -/
theorem nn_oo_judgement :
    Dn 9 = (2^7 + 1)^2 ∧
    65 * 63 = 2^12 - 1 ∧
    (7 * 8 = 56 ∧ 7 * 9 = 63) ∧
    (8^2 - 8 = 56 ∧ 8^2 - 1 = 63 ∧ 8^2 = 64 ∧ 8^2 + 1 = 65) ∧
    (1:ℚ)/65 - (1:ℚ)/63 = -(2:ℚ)/4095 ∧
    (3:ℚ)/2 + (1:ℚ)/7 + (1:ℚ)/(7*2^3) = (Dn 3 : ℚ)/(7*2^3) := by
  constructor
  · exact nn_d9_a6
  constructor
  · exact oo1_prod
  constructor
  · exact oo2_dual
  constructor
  · exact oo6_window
  constructor
  · exact oo3_frac
  · exact xx2_n3

end MUFPF.CoreConstantWindow
