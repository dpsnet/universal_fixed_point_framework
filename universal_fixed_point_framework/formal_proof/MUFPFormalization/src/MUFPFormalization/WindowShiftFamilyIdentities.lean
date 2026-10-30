import MUFPFormalization.SevenPlusMinusOneIdentities

/-!
# P7-5e-289 ★ 207 VV/WW 家族化

对应 roadmap 207 ②/③ 未形式化项：WW1（D(m+8)−1=2^{m+7}(7m+58) 一般家族化）、
VV1（a_{2j+3}+w_{2j+3}=2b_j²=b_{2j+3} 窗口投影和 = 满格塔成员）、
TT（b_j²+1 = a_{2j+3} 起边界侧，−1 侧由 288 mersenne_chain 覆盖）。

核心结论（数值先证伪 66/66，残差 0）：
- ★ WW1：D(m+8)−1 = 2^(m+7)(7m+58)（m 一般；m=1 特例 D(9)−1=2⁸·65 交叉 286
  nn_d9_minus1；m=2 终边界 D(10)−1=2⁹·72 = 2¹²·9 = b₁₀·9）
- ★ VV1：w_{2j+3}+a_{2j+3} = 2b_j² = b_{2j+3}（63+65=128=b₅、255+257=512=b₇、…）
- TT 闭合：b_j²+1 = 2^(2j+4)+1 = a_{2j+3}（j=1 即 65=a₅）

诚实边界：全部为代数恒等 + 枚举事实；"窗口投影和 = 满格塔"的语义指认为观察级登记。
-/

namespace MUFPF.WindowShiftFamily

open Nat

/-- 满格塔成员 b_j = 2^(j+2)（引用 288 定义）。 -/
abbrev B (j : ℕ) : ℕ := 2^(j+2)

/-! ## §1 ★ WW1：D(m+8) 平移家族 -/

/-- ★ D(m+8)−1 = 2^(m+7)(7m+58)（Bott 周期步进下 D 线性平移；m=1 特例 2⁸·65 交叉 286）。 -/
theorem ww_shift (m : ℕ) : MUFPF.CoreConstantWindow.Dn (m+8) - 1 = 2^(m+7) * (7*m + 58) := by
  change 2^((m+8)-1) * (7*(m+8) + 2) + 1 - 1 = 2^(m+7) * (7*m + 58)
  rw [Nat.add_sub_cancel]
  rw [show (m+8) - 1 = m + 7 by omega]
  rw [show 7*(m+8) + 2 = 7*m + 58 by omega]

/-- m=1 特例交叉：D(9)−1 = 2⁸·65（286 nn_d9_minus1）。 -/
theorem ww_d9_dual : MUFPF.CoreConstantWindow.Dn 9 - 1 = 2^8 * 65 := by
  exact MUFPF.CoreConstantWindow.nn_d9_minus1

/-- m=2：D(10)−1 = 2⁹·72。 -/
theorem ww_d10 : MUFPF.CoreConstantWindow.Dn 10 - 1 = 2^9 * 72 := by
  change 2^(10-1) * (7*10 + 2) + 1 - 1 = 2^9 * 72
  rw [Nat.add_sub_cancel]

/-- ★ WW2 终边界：D(10)−1 = 2¹²·9 = b₁₀·9（平移代数 2⁹·72 = 2⁹·(8·9) = 2¹²·9）。 -/
theorem ww_d10_dual : MUFPF.CoreConstantWindow.Dn 10 - 1 = 2^12 * 9 := by
  change 2^(10-1) * (7*10 + 2) + 1 - 1 = 2^12 * 9
  rw [Nat.add_sub_cancel]
  norm_num

/-! ## §2 TT：b_j²±1 窗口投影闭合 -/

/-- 起边界侧：b_j²+1 = 2^(2j+4)+1 = a_{2j+3}（j=1 即 65=a₅）。 -/
theorem tt_plus (j : ℕ) : B j^2 + 1 = 2^(2*j + 4) + 1 := by
  unfold B
  rw [MUFPF.SevenPlusMinusOne.sq_pow j]
  rw [show 2*(j+2) = 2*j + 4 by omega]

/-- 宽度侧：b_j²−1 = 2^(2j+4)−1 = w_{2j+3}（引用 288 mersenne_chain）。 -/
theorem tt_minus_ref (j : ℕ) : B j^2 - 1 = 2^(2*j + 4) - 1 := by
  exact MUFPF.SevenPlusMinusOne.mersenne_chain j

/-! ## §3 ★ VV1：窗口投影和 = 满格塔 -/

/-- 幂和：2·b_j² = b_{2j+3}（B 塔代数）。 -/
theorem vv_sumB (j : ℕ) : 2 * B j^2 = B (2*j + 3) := by
  unfold B
  calc
    2 * (2^(j+2))^2 = 2 * 2^(2*(j+2)) := by rw [MUFPF.SevenPlusMinusOne.sq_pow j]
    _ = 2^(2*(j+2) + 1) := by
      rw [mul_comm]
      rw [← pow_succ]
    _ = 2^(2*j + 5) := by rw [show 2*(j+2) + 1 = 2*j + 5 by omega]
    _ = B (2*j + 3) := by
      unfold B
      rw [show (2*j + 3) + 2 = 2*j + 5 by omega]

/-- ★ 窗口投影和（显式幂形）：w_{2j+3}+a_{2j+3} = 2^(2j+5)。 -/
theorem vv_window (j : ℕ) : (2^(2*j+4) - 1) + (2^(2*j+4) + 1) = 2^(2*j+5) := by
  have ha : 1 ≤ 2^(2*j+4) := by
    exact Nat.succ_le_of_lt (by positivity)
  calc
    (2^(2*j+4) - 1) + (2^(2*j+4) + 1) = 2^(2*j+4) + 2^(2*j+4) := by omega
    _ = 2 * 2^(2*j+4) := by omega
    _ = 2^(2*j+4 + 1) := by
      rw [mul_comm]
      rw [← pow_succ]
    _ = 2^(2*j+5) := by rw [show 2*j+4+1 = 2*j+5 by omega]

/-- ★ VV1（b 形）：(b_j²−1)+(b_j²+1) = b_{2j+3}（63+65=128=b₅）。 -/
theorem vv_windowB (j : ℕ) : (B j^2 - 1) + (B j^2 + 1) = B (2*j + 3) := by
  rw [tt_minus_ref j, tt_plus j]
  unfold B
  rw [show (2*j + 3) + 2 = 2*j + 5 by omega]
  exact vv_window j

/-! ## §4 联合主定理 -/

/-- ★★ WW 双边界 + VV 首实例联合：D(9)−1=2⁸·65 ∧ D(10)−1=2¹²·9 ∧ 63+65=128=b₅。 -/
theorem vv_ww_duality :
    MUFPF.CoreConstantWindow.Dn 9 - 1 = 2^8 * 65 ∧
    MUFPF.CoreConstantWindow.Dn 10 - 1 = 2^12 * 9 ∧
    (B 1^2 - 1) + (B 1^2 + 1) = B 5 := by
  constructor
  · exact MUFPF.CoreConstantWindow.nn_d9_minus1
  · constructor
    · exact ww_d10_dual
    · unfold B
      norm_num

/-- ★★ VV/WW 家族主定理（j 一般）：D 平移家族与窗口投影和并存。 -/
theorem vv_ww_family (j : ℕ) :
    MUFPF.CoreConstantWindow.Dn (j+8) - 1 = 2^(j+7) * (7*j + 58) ∧
    (B j^2 - 1) + (B j^2 + 1) = B (2*j + 3) := by
  constructor
  · exact ww_shift j
  · exact vv_windowB j

end MUFPF.WindowShiftFamily
