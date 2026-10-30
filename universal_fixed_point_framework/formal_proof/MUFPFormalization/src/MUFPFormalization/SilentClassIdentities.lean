import MUFPFormalization.SilentFamilyMechanismIdentities

/-!
# P7-5e-291 ★ D(n) 静默类归属 + 2 进分解

对应 209 系列（210 ZZ 静默类归属与 2 进幂集连接；与 290 CC3 构成姊妹定理）：
- 290 ★★★ cc3_silent 讲 D(n) 落入静默家族 2^m+1（线性因子 7n+2 是 2 的幂）；
- 本层 ★ zz2_decomp 讲 D(n) 自身的 2 进分解：n≥4 时 D(n)=8·2^(n−4)(7n+2)+1
  （k_n = 2^(n−4)(7n+2) 显式）——"2 进幂 × 线性因子"结构；
- ★ zz1_silent：n≥4 时 D(n) ≡ 1 mod 8（静默单元类 8k+1）；
- ★ zz1_d2 / zz1_d3_exc：D(2)=33≡1（静默类）、D(3)=93≡5（例外，196 U2 归因
  n≥4 时 2^(n−1) 含 2³ 因子）；
- ★ zz3_family：D(2)=2⁵+1（静默家族成员 m=5，290 cc3_d2 重述）∧ D(9)=129²
  （家族平方，286 nn_d9_square 跨文件引用）；
- ★ zz_judgement：联合主定理（分解 + 静默类 + 家族成员实例并置）。

数值先证伪 79/79，残差 0。诚实边界：全部代数恒等 + 模算术；
『D(n) 静默类是 186 2 进幂集组织在 B*(n) 分母层面的投影』为语义连接（观察级登记）。
-/

namespace MUFPF.SilentClass

open Nat

/-! ## §1 ★ zz2：2 进分解 -/

/-- ★ n≥4：D(n) = 8·2^(n−4)(7n+2)+1——k_n = 2^(n−4)(7n+2) 显式
    （D(n)−1 的"2 进幂 × 线性因子"结构，n 依赖完全显式）。 -/
theorem zz2_decomp (n : ℕ) (hn : 4 ≤ n) :
    MUFPF.CoreConstantWindow.Dn n = 8 * 2^(n-4) * (7*n + 2) + 1 := by
  unfold MUFPF.CoreConstantWindow.Dn
  have hpow : 2^(n-1) = 2^3 * 2^(n-4) := by
    rw [← pow_add]
    congr 1
    omega
  rw [hpow]
  ring

/-! ## §2 ★ zz1：静默类归属 -/

/-- ★ n≥4：D(n) ≡ 1 mod 8（静默单元类 8k+1）——D(n) 分母的类归属。 -/
theorem zz1_silent (n : ℕ) (hn : 4 ≤ n) : MUFPF.CoreConstantWindow.Dn n % 8 = 1 := by
  calc
    MUFPF.CoreConstantWindow.Dn n % 8 = (8 * 2^(n-4) * (7*n + 2) + 1) % 8 := by
      rw [zz2_decomp n hn]
    _ = (1 + 8 * (2^(n-4) * (7*n + 2))) % 8 := by
      congr 1
      ring
    _ = 1 % 8 := by
      rw [Nat.add_mul_mod_self_left 1 8 (2^(n-4) * (7*n + 2))]
    _ = 1 := by
      norm_num

/-- zz1 首实例：D(2)=33 ≡ 1 mod 8（静默类，290 cc3_d2 的同余投影）。 -/
theorem zz1_d2 : MUFPF.CoreConstantWindow.Dn 2 % 8 = 1 := by
  unfold MUFPF.CoreConstantWindow.Dn
  norm_num

/-- ★ 例外：D(3)=93 ≡ 5 mod 8（非静默类——196 U2 登记的 n=3 例外）。 -/
theorem zz1_d3_exc : MUFPF.CoreConstantWindow.Dn 3 % 8 = 5 := by
  unfold MUFPF.CoreConstantWindow.Dn
  norm_num

/-! ## §3 ★ zz3：家族成员 -/

/-- ★ D(2)=2⁵+1（静默家族成员 m=5）∧ D(9)=129²（家族平方，286 nn_d9_square）。
    —— 210 ZZ3 已知核对的 Lean 化。 -/
theorem zz3_family :
    MUFPF.CoreConstantWindow.Dn 2 = 2^5 + 1 ∧
    MUFPF.CoreConstantWindow.Dn 9 = 129^2 := by
  constructor
  · unfold MUFPF.CoreConstantWindow.Dn
    norm_num
  · exact MUFPF.CoreConstantWindow.nn_d9_square

/-! ## §4 联合主定理 -/

/-- ★★ 分解 × 静默类 × 家族成员联合：D(2)≡1 ∧ D(4)≡1 ∧ D(9)≡1 ∧
    D(3)≡5（例外）∧ D(9)=129² ∧ D(2)=2⁵+1 —— D(n) 静默类归属的数值主定理。 -/
theorem zz_judgement :
    MUFPF.CoreConstantWindow.Dn 2 % 8 = 1 ∧
    MUFPF.CoreConstantWindow.Dn 4 % 8 = 1 ∧
    MUFPF.CoreConstantWindow.Dn 9 % 8 = 1 ∧
    MUFPF.CoreConstantWindow.Dn 3 % 8 = 5 ∧
    MUFPF.CoreConstantWindow.Dn 9 = 129^2 ∧
    MUFPF.CoreConstantWindow.Dn 2 = 2^5 + 1 := by
  constructor
  · exact zz1_d2
  · constructor
    · exact zz1_silent 4 (by norm_num)
    · constructor
      · exact zz1_silent 9 (by norm_num)
      · constructor
        · exact zz1_d3_exc
        · constructor
          · exact MUFPF.CoreConstantWindow.nn_d9_square
          · unfold MUFPF.CoreConstantWindow.Dn
            norm_num

end MUFPF.SilentClass
