import MUFPFormalization.CoreConstantWindowIdentities

/-!
# P7-5e-287 ★ D(17) 家族成员幂检查（QQ：D(9)=a₆² 一般化）

对应 roadmap 205 下一步 QQ：D(9)=16641=129²=a₆² 家族成员平方的一般化——
检查 D(17) 是否家族成员幂。

结论（数值先证伪 60/60）：D(17) = 2¹⁶·(7·17+2)+1 = 2¹⁶·121+1 = 2816²+1 =
(2⁸·11)²+1 —— **"平方+1"家族成员**：D(17)−1 为纯平方 (2⁸·11)²=2816²，
与 D(9)=129² **纯平方**构成 ±1 对偶形态（呼应 285 LL ±1 对偶与 65 修正锚点）。

一般化（QQ 全貌）：7n+2 为平方（m ≡ ±3 mod 7，m 奇）的 n 序列
{1,17,41,89,137,...} 上 D(n)−1 = (2^((n−1)/2)·m)² 恒为平方；n=9 为唯一例外
（7·9+2=65 非平方，但 D(9) 本身为家族成员平方 129²）。

诚实边界：QQ 结论为代数恒等 + 枚举事实；"平方/平方+1 交替"的周期语义为观察级登记。
-/

namespace MUFPF.FamilySquare

open Nat

/-- D(n) 闭式（引用 286）：D(n) = 2^(n−1)(7n+2)+1。 -/
abbrev Dn := MUFPF.CoreConstantWindow.Dn

/-! ## §1 QQ：D(17) 平方+1 家族成员 -/

/-- 一般引理：2^(2n) = (2^n)²。 -/
theorem qq_square_expand2 (n : ℕ) : 2^(2*n) = (2^n)^2 := by
  rw [show 2 * n = n + n by omega, pow_add]
  rw [← pow_two]

/-- D(17) 数值 = 7929857。 -/
theorem qq_17_value : Dn 17 = 7929857 := by
  change 2^(17-1) * (7*17 + 2) + 1 = 7929857
  norm_num

/-- 7·17+2 = 11²（7n+2 平方族 n=17 成员：121 = 11²）。 -/
theorem qq_121 : 7*17 + 2 = 11^2 := by norm_num

/-- 2816 = 2⁸·11（家族段 2⁸ × 静默单元 11）。 -/
theorem qq_a17 : 2816 = 2^8 * 11 := by norm_num

/-- D(17)−1 = 2816² = (2⁸·11)²（代数链：2¹⁶·121 = 2¹⁶·11² = (2⁸·11)²）。 -/
theorem qq_17_square : Dn 17 - 1 = (2^8 * 11)^2 := by
  calc
    Dn 17 - 1 = 2^16 * (7*17 + 2) := by
      change 2^(17-1) * (7*17 + 2) + 1 - 1 = 2^16 * (7*17 + 2)
      norm_num
    _ = 2^16 * 11^2 := by
      rw [show 7*17 + 2 = 11^2 by norm_num]
    _ = (2^8 * 11)^2 := by
      have h16 : 2^16 = (2^8)^2 := by norm_num
      rw [h16]
      ring

/-- ★ D(17) = 2816²+1：平方+1 家族成员（对偶 D(9)=129² 纯平方）。 -/
theorem qq_17_plus1 : Dn 17 = 2816^2 + 1 := by
  change 2^(17-1) * (7*17 + 2) + 1 = 2816^2 + 1
  norm_num

/-- 2816² = 7929856。 -/
theorem qq_2816_sq : 2816^2 = 7929856 := by norm_num

/-! ## §2 一般化：7n+2 平方族 → D(n)−1 平方 -/

/-- n=1 成员：D(1)−1 = 9 = 3²。 -/
theorem qq_d1 : Dn 1 - 1 = 3^2 := by
  change 2^(1-1) * (7*1 + 2) + 1 - 1 = 3^2
  norm_num

/-- ★ 一般定理：n 奇且 7n+2 = m² ⇒ D(n)−1 = (2^((n−1)/2)·m)²。 -/
theorem qq_general {n m : ℕ} (hn : n % 2 = 1) (hm : 7*n + 2 = m^2) :
    Dn n - 1 = (2^((n-1)/2) * m)^2 := by
  have h2 : n - 1 = 2 * ((n - 1) / 2) := by omega
  have hpow : 2^(n-1) = 2^(2 * ((n-1)/2)) := by
    exact congrArg (fun x => 2^x) h2
  change 2^(n-1) * (7*n + 2) + 1 - 1 = (2^((n-1)/2) * m)^2
  rw [Nat.add_sub_cancel]
  calc
    2^(n-1) * (7*n + 2) = 2^(2 * ((n-1)/2)) * (7*n + 2) := by
      rw [hpow]
    _ = (2^((n-1)/2))^2 * (7*n + 2) := by
      rw [qq_square_expand2 ((n-1)/2)]
    _ = (2^((n-1)/2))^2 * m^2 := by
      rw [hm]
    _ = (2^((n-1)/2) * m)^2 := by
      rw [← mul_pow]

/-! ## §3 联合：±1 对偶形态（D(9) 纯平方 vs D(17) 平方+1） -/

/-- ★★ QQ 联合：D(9) = 129² 纯平方 ∧ D(17) = 2816²+1 平方+1（±1 对偶形态，呼应 65 修正锚点）。 -/
theorem qq_duality : Dn 9 = 129^2 ∧ Dn 17 = 2816^2 + 1 := by
  constructor
  · exact MUFPF.CoreConstantWindow.nn_d9_square
  · exact qq_17_plus1

end MUFPF.FamilySquare
