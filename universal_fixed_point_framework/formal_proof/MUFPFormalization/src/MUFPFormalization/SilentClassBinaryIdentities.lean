import MUFPFormalization.SilentClassIdentities
import MUFPFormalization.DenominatorPrimacyIdentities

/-!
# P7-5e-210 ★ ZZ 静默类归属与 2 进幂集连接——ZZ4 k_n 2 进分解 + CONN 联合闭式

291 姊妹模块（291 SilentClassIdentities 已覆盖 ZZ1/ZZ2/ZZ3：zz2_decomp /
zz1_silent / zz1_d2 / zz1_d3_exc / zz3_family / zz_judgement）；
本模块覆盖 210 登记的 ZZ4（k_n 2 进分解）与 CONN（1/B* 联合闭式 + 186 连接）。

数值先证伪（勿重跑）：`scripts/_phase102_p7_5e210_dn_silent_class_binary.py` + 同目录 json
（79/79 全 ok=true，2026-10-16）。

核心内容（登记原文 210 ⑩）：
- ZZ4：k_n = 2^(n−4)·(7n+2)——"2 进幂 × 线性因子"；k_9=2^5·65（修正锚点 65 出现于 k_9）、
  k_10=2^9·9、k_13=2^9·93、k_16=2^13·57；n 偶时 7n+2 偶 ⇒ k_n 含额外 2 因子；
- CONN：1/B*(n) = D(n)/(7·2^n) = (8k_n+1)/(7·2^n)——分子落静默单元类 8k+1、
  分母 M_3×2^n（186『2 进幂集组织』在 B*(n) 分母层面的投影）。

诚实边界：ZZ4 枚举 + 2 进分解、CONN 代数恒等（209/291 组合）——候选层未升定案层；
『186 投影』为语义连接（观察级登记，不形式化）。
-/

namespace MUFPF.SilentClassBinary

open MUFPF.CoreConstantWindow
open MUFPF.DenominatorPrimacy

/-- k_n = 2^(n−4)·(7n+2)（n≥4 域；291 zz2_decomp 的 k 参数显式，210 ZZ2 的伴随量）。 -/
def k_n (n : ℕ) : ℕ := 2^(n-4) * (7*n + 2)

/-! ## §1 ★ ZZ4：k_n 2 进分解（2 进幂 × 线性因子，n 偶含额外 2 因子） -/

/-- k_9 = 2^5·65——修正锚点 65 出现于 k_9（n 奇：7·9+2=65 奇数，线性因子完整保留）。 -/
theorem zz4_k9 : k_n 9 = 2^5 * 65 := by
  unfold k_n
  norm_num

/-- k_10 = 2^9·9——7·10+2=72=8·9=2^3·9 含额外 2^3 因子（n 偶 ⇒ 7n+2 偶）。 -/
theorem zz4_k10 : k_n 10 = 2^9 * 9 := by
  unfold k_n
  norm_num

/-- k_13 = 2^9·93（n 奇：7·13+2=93 奇数）。 -/
theorem zz4_k13 : k_n 13 = 2^9 * 93 := by
  unfold k_n
  norm_num

/-- k_16 = 2^13·57——7·16+2=114=2·57 含额外 2 因子（n 偶）。 -/
theorem zz4_k16 : k_n 16 = 2^13 * 57 := by
  unfold k_n
  norm_num

/-- ★ n 偶 ⇒ 7n+2 偶（ZZ4『n 偶 ⇒ k_n 含额外 2 因子』的模算术根源：7≡1 mod 2）。 -/
theorem zz4_even_v2 (n : ℕ) (hn : n % 2 = 0) : (7 * n + 2) % 2 = 0 := by
  rw [Nat.add_mod, Nat.mul_mod]
  rw [hn]

/-! ## §2 ★ CONN：1/B*(n) 联合闭式（分子静默类 × 分母 M_3×2^n） -/

/-- ★ n≥1：1/B*(n) = D(n)/(7·2^n)——209 bstar_closed_den 的 n 一般化（n−1 代入）。 -/
theorem conn_bstar_den (n : ℕ) (hn : 1 ≤ n) :
    bstarClosed n = (Dn n : ℚ) / (7 * (2 : ℚ) ^ n) := by
  have h := bstar_closed_den (n - 1)
  have hn' : (n - 1) + 1 = n := Nat.sub_add_cancel hn
  simpa [hn'] using h

/-- ★ n≥4：1/B*(n) = (8·k_n+1)/(7·2^n) = (8·2^(n−4)(7n+2)+1)/(7·2^n)
    ——分子落静默单元类 8k+1、分母 M_3×2^n（186 投影的代数内核，291 zz2_decomp 组合）。 -/
theorem conn_k_union (n : ℕ) (hn : 4 ≤ n) :
    bstarClosed n = ((8 * 2^(n-4) * (7*n + 2) + 1 : ℕ) : ℚ) / (7 * (2 : ℚ) ^ n) := by
  rw [conn_bstar_den n (by omega)]
  congr 1
  norm_cast
  exact MUFPF.SilentClass.zz2_decomp n hn

/-! ## §3 联合主定理 -/

/-- ★★ ZZ4×CONN 联合：k_n 四实例 2 进分解 + 偶性根源 + 1/B*(9) 联合闭式 + 291 家族成员
    （210 ZZ 收尾的数值主定理，八项并置）。 -/
theorem zz_binary_judgement :
    k_n 9 = 2^5 * 65 ∧
    k_n 10 = 2^9 * 9 ∧
    k_n 13 = 2^9 * 93 ∧
    k_n 16 = 2^13 * 57 ∧
    (7 * 10 + 2) % 2 = 0 ∧
    bstarClosed 9 = ((8 * 2^(9 - 4) * (7*9 + 2) + 1 : ℕ) : ℚ) / (7 * (2 : ℚ) ^ 9) ∧
    Dn 2 = 2^5 + 1 ∧
    Dn 9 = 129^2 := by
  constructor
  · exact zz4_k9
  · constructor
    · exact zz4_k10
    · constructor
      · exact zz4_k13
      · constructor
        · exact zz4_k16
        · constructor
          · exact zz4_even_v2 10 (by norm_num)
          · constructor
            · exact conn_k_union 9 (by norm_num)
            · exact MUFPF.SilentClass.zz3_family

end MUFPF.SilentClassBinary
