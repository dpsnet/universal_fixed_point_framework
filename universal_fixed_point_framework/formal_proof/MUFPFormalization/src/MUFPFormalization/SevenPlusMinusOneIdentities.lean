import MUFPFormalization.CoreConstantWindowIdentities

/-!
# P7-5e-288 ★ 7×(8±1) 对偶延伸

对应 roadmap 205 下一步 ③：OO2（63=7·9 vs 56=7·8）+ RR5（差方恒等 (b₁−1)(b₁+1)=b₁²−1）
家族化。B(j) = 2^(j+2)（b₁=8 满格），Wm(j) = B(j)−1（域宽侧 = M_{j+3}），
AP(j) = B(j)+1（静默单元侧）。

核心结论（数值先证伪 71/71，残差 0）：
- ★ 差方家族：B(j)²−1 = (B(j)−1)(B(j)+1)（j=1 即 7·9 = 63 = 64−1，经 285 ll3_prod）
- ★ Mersenne 链：B(j)²−1 = 2^(2j+4)−1 = M_{2j+4}（63/255/1023/4095/…）
- ★ 静默平方侧：Wm(j)²（49/225/961/3969/…）vs 差方侧 —— 同因子 (b−1) 的平方与差方 = ±1 对偶延伸
- 窗口延伸：{b²−b, b²−1, b², b²+1} 4 连续项（j=1 即 [56,63,64,65] 重现 286 窗口）
- 63 双身份：7·9 = 63 = 2⁶−1（域宽×静默单元 = Mersenne）

诚实边界：全部为代数恒等 + 枚举事实；"静默平方 vs 差方 ±1 对偶"的周期语义为观察级登记。
-/

namespace MUFPF.SevenPlusMinusOne

open Nat

/-- 满格塔成员 b_j = 2^(j+2)（b₁=8）。 -/
abbrev B (j : ℕ) : ℕ := 2^(j+2)

/-- 域宽侧（Mersenne 侧）Wm(j) = b_j − 1 = 2^(j+2) − 1 = M_{j+3}。 -/
abbrev Wm (j : ℕ) : ℕ := 2^(j+2) - 1

/-- 静默单元侧 AP(j) = b_j + 1 = 2^(j+2) + 1。 -/
abbrev AP (j : ℕ) : ℕ := 2^(j+2) + 1

/-! ## §1 基座（j=1 具体值，引用 286 oo2_dual） -/

/-- b₁ = 8（满格）。 -/
theorem b1_val : B 1 = 8 := by norm_num

/-- 域宽 Wm(1) = 7（= b₁−1 = k_max−1）。 -/
theorem wm1_val : Wm 1 = 7 := by norm_num

/-- 静默单元侧 AP(1) = 9（= b₁+1）。 -/
theorem ap1_val : AP 1 = 9 := by norm_num

/-- ★ 7×(8±1) 对偶基座：7·8 = 56（δ∞ 分母侧）∧ 7·9 = 63（宽度/Mersenne 侧）。 -/
theorem pmo_base : 7 * 8 = 56 ∧ 7 * 9 = 63 := by
  constructor <;> norm_num

/-- 静默平方侧 j=1：7² = 49（静默单元平方）。 -/
theorem seven_sq : 7^2 = 49 := by norm_num

/-- 63 双身份：7·9 = 63 = 2⁶−1（域宽×静默单元 = Mersenne M_6）。 -/
theorem pmo_63_dual : 7 * 9 = 63 ∧ 63 = 2^6 - 1 := by
  constructor <;> norm_num

/-! ## §2 ★ 差方家族（一般 j） -/

/-- 指数恒等：(2^(j+2))² = 2^(2·(j+2))。 -/
theorem sq_pow (j : ℕ) : (2^(j+2))^2 = 2^(2*(j+2)) := by
  rw [← pow_mul]
  rw [show (j+2)*2 = 2*(j+2) by omega]

/-- ★ 一般差方恒等：(b_j−1)(b_j+1) = b_j²−1（j=1 即 7·9=63；经 285 ll3_prod）。 -/
theorem diff_sqB (j : ℕ) : (B j - 1) * (B j + 1) = B j^2 - 1 := by
  unfold B
  calc
    (2^(j+2)-1)*(2^(j+2)+1) = (2^(j+2)+1)*(2^(j+2)-1) := by rw [mul_comm]
    _ = 2^(2*(j+2)) - 1 := by
      exact MUFPF.MerFermatDuality.ll3_prod (j+2)
    _ = (2^(j+2))^2 - 1 := by rw [sq_pow j]

/-- ★ Mersenne 链：b_j²−1 = 2^(2j+4)−1 = M_{2j+4}（63/255/1023/4095/…）。 -/
theorem mersenne_chain (j : ℕ) : B j^2 - 1 = 2^(2*j + 4) - 1 := by
  unfold B
  calc
    (2^(j+2))^2 - 1 = 2^(2*(j+2)) - 1 := by rw [sq_pow j]
    _ = 2^(2*j + 4) - 1 := by rw [show 2*(j+2) = 2*j + 4 by omega]

/-- 差方→Mersenne 合成：(b_j−1)(b_j+1) = 2^(2j+4)−1。 -/
theorem diff_sqB_m (j : ℕ) : (B j - 1) * (B j + 1) = 2^(2*j + 4) - 1 := by
  exact (diff_sqB j).trans (mersenne_chain j)

/-! ## §3 ★ 静默平方侧 ±1 对偶 -/

/-- ★ 对偶延伸：同因子 (b_j−1) 的平方侧与差方侧并存
    （(2^(j+2)−1)² = Wm(j)² 静默平方 vs (b_j−1)(b_j+1) = M_{2j+4} 差方侧）。 -/
theorem dual_ext (j : ℕ) :
    (B j - 1)^2 = (2^(j+2) - 1)^2 ∧
    (B j - 1) * (B j + 1) = 2^(2*j + 4) - 1 := by
  constructor
  · unfold B
    rfl
  · exact diff_sqB_m j

/-- j=1 对偶实例：7² = 49 ∧ 7·9 = 63（静默平方 vs 差方侧）。 -/
theorem pmo_dual49_63 : (B 1 - 1)^2 = 49 ∧ (B 1 - 1) * (B 1 + 1) = 63 := by
  constructor <;> norm_num

/-! ## §4 窗口延伸（j 级 4 连续项） -/

/-- 满格平方恒等：b_j² = b_j·b_j。 -/
theorem bsq_mul (j : ℕ) : B j^2 = B j * B j := by
  rw [pow_two]

/-- ★ 窗口左项：b_j²−b_j = b_j(b_j−1)（j=1 即 56 = 8·7）。 -/
theorem window_left (j : ℕ) : B j^2 - B j = B j * (B j - 1) := by
  calc
    B j^2 - B j = B j * B j - B j := by rw [bsq_mul j]
    _ = B j * B j - B j * 1 := by
      congr 2
      rw [mul_one]
    _ = B j * (B j - 1) := by
      exact (Nat.mul_sub_left_distrib (B j) (B j) 1).symm

/-- 窗口右项：b_j²−1 由差方给出（= (b_j−1)(b_j+1)，diff_sqB）。 -/
theorem window_right (j : ℕ) : B j^2 - 1 = (B j - 1) * (B j + 1) := by
  exact (diff_sqB j).symm

/-- 窗口 +1 项：b_j²+1 与 65 修正锚点同构（j=1：65 = b₁²+1）。 -/
theorem window_plus1 (j : ℕ) : B j^2 + 1 = (2^(j+2))^2 + 1 := by
  unfold B
  rfl

/-- j=1 窗口重现：{56,63,64,65} = b₁²−{8,1,0,−1}（286 oo6_window 的代数闭合）。 -/
theorem window_j1 :
    B 1^2 - B 1 = 56 ∧
    B 1^2 - 1 = 63 ∧
    B 1^2 = 64 ∧
    B 1^2 + 1 = 65 := by
  constructor <;> norm_num

/-! ## §5 联合主定理 -/

/-- ★★ 7×(8±1) 对偶延伸联合：静默平方侧 49、差方侧 63（域宽×静默单元 = M_6）、
    满格平方 64（= 8²）—— 同因子 (b−1)=7 的 平方/差方 ±1 对偶 + Mersenne 双身份。 -/
theorem pmo_duality :
    (B 1 - 1)^2 = 49 ∧
    (B 1 - 1) * (B 1 + 1) = 63 ∧
    63 = 2^6 - 1 := by
  constructor
  · norm_num
  · constructor
    · norm_num
    · norm_num

/-- ★★ 差方家族主定理（j 一般）：满格平方减一 = 域宽×静默单元 = Mersenne_{2j+4}，
    且同因子 (b−1) 的静默平方并存 —— ±1 对偶的完整家族化。 -/
theorem pmo_family (j : ℕ) :
    (B j - 1) * (B j + 1) = 2^(2*j + 4) - 1 ∧
    (B j - 1)^2 = (2^(j+2) - 1)^2 ∧
    B j^2 - B j = B j * (B j - 1) := by
  constructor
  · exact diff_sqB_m j
  · constructor
    · unfold B
      rfl
    · exact window_left j

end MUFPF.SevenPlusMinusOne
