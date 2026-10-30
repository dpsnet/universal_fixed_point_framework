import MUFPFormalization.SilentClassIdentities

/-!
# P7-5e-293 ★ k 族同族判别 + 种子交集（211 YY/AA）

对应 209 系列（211 ⑪ k 族同族判别与种子交集）：
- ★ YY 同族判别：后移窗口对合常数族 k_{2j+3}=6·4^j 不是新族——
  6·4^j = 3·2^{2j+1} = k_j 公式在下标 2j+3 的取值（k_j = 3·2^{j−2}）；
  重合窗口 {5,7} 在登记定义域内、{9,11,13,15} 是公式自然延伸——登记修正为"原族下标延伸"；
- ★ AA 种子交集：k_4 = 30 = 2·3·5（纯种子积，三种子 {2,3,5} 直接生成，n=4 单点）；
  k_9 = 2^5·65（65 = 7·9+2 线性因子命中修正锚点）；
- ★ 连接：D(n) − 1 = 8·kn(n)（n≥4，291 zz2_decomp 的 k_n 显式交叉）。

数值先证伪 66/66，残差 0。诚实边界：YY 为代数恒等（重命名事实）、
AA 为枚举核对——候选层未升定案层。
-/

namespace MUFPF.FamilyIndex

open Nat

/-! ## §1 定义 -/

/-- 窗口对合常数族 k_j = 3·2^(j−2)（窗口 2 家族段对合常数 c_j = 8k_j+1，
    j≥2；Nat 语义 j<2 时 j−2 钳为 0 仍良定义）。 -/
def kj (j : ℕ) : ℕ := 3 * 2^(j-2)

/-- D(n) 的 k_n = 2^(n−4)(7n+2)（291 zz2_decomp 的 k_n 显式，n≥4）。 -/
def kn (n : ℕ) : ℕ := 2^(n-4) * (7*n + 2)

/-! ## §2 ★ YY：同族判别 -/

/-- ★ k_{2j+3} = 6·4^j——后移窗口对合常数（窗口 5,7,9,11,13,15,…）非新族。 -/
theorem yy_shift (j : ℕ) : kj (2*j + 3) = 6 * 4^j := by
  unfold kj
  have hsub : 2*j + 3 - 2 = 2*j + 1 := by omega
  rw [hsub]
  calc
    3 * 2^(2*j + 1) = 3 * (2^(2*j) * 2) := by rw [pow_succ 2 (2*j)]
    _ = 6 * 2^(2*j) := by ring
    _ = 6 * 4^j := by
      congr 1
      rw [pow_mul]
      rw [show 4 = 2^2 by norm_num]

/-- ★ 6·4^j = 3·2^(2j+1)——后移对合常数的双表达恒等（"6·4^j 形式"与
    "k_j 公式在 2j+3 下标"形式同值）。 -/
theorem yy_six_form (j : ℕ) : 6 * 4^j = 3 * 2^(2*j + 1) := by
  calc
    6 * 4^j = 6 * 2^(2*j) := by
      congr 1
      rw [show 4 = 2^2 by norm_num]
      rw [← pow_mul]
    _ = 3 * (2^(2*j) * 2) := by ring
    _ = 3 * 2^(2*j + 1) := by
      rw [pow_succ 2 (2*j)]

/-- ★★ 同族判别合成：k_{2j+3} = 3·2^{2j+1}——后移对合常数就是 k_j 公式
    在窗口下标 2j+3 的取值（非新族，原族下标延伸）。 -/
theorem yy_same_family (j : ℕ) : kj (2*j + 3) = 3 * 2^(2*j + 1) := by
  rw [yy_shift j, yy_six_form j]

/-! ## §3 ★ AA：种子交集 -/

/-- ★ k_4 = 30 = 2·3·5（纯种子积——三种子 {2,3,5} 直接生成，n=4 单点）。 -/
theorem aa_seed4 : kn 4 = 30 ∧ 30 = 2 * 3 * 5 := by
  constructor
  · unfold kn
    norm_num
  · norm_num

/-- ★ k_9 = 2^5·65（65 = 7·9+2 线性因子命中修正锚点，k_n 奇部核对）。 -/
theorem aa_k9 : kn 9 = 2^5 * 65 := by
  unfold kn
  norm_num

/-- ★ 连接：D(n) − 1 = 8·kn(n)（n≥4）——291 zz2_decomp 的 k_n 显式交叉
    （2 进分解 D(n) = 8·k_n(n) + 1 的减一形式）。 -/
theorem aa_dn_kn (n : ℕ) (hn : 4 ≤ n) :
    MUFPF.CoreConstantWindow.Dn n - 1 = 8 * kn n := by
  unfold kn
  calc
    MUFPF.CoreConstantWindow.Dn n - 1
        = (8 * 2^(n-4) * (7*n + 2) + 1) - 1 := by
      rw [MUFPF.SilentClass.zz2_decomp n hn]
    _ = (8 * (2^(n-4) * (7*n + 2)) + 1) - 1 := by
      congr 1
      ring
    _ = 8 * (2^(n-4) * (7*n + 2)) := by
      rw [Nat.add_sub_cancel_right]

/-! ## §4 联合主定理 -/

/-- ★★ YY×AA 联合：同族判别（k_{2j+3}=6·4^j ∧ k_{2j+3}=3·2^{2j+1}）×
    种子交集（k_4=30=2·3·5）∧ 核对（k_9=2^5·65 ∧ D(4)−1=8·k_4）。
    —— 211 ⑪ 的数值主定理。 -/
theorem yy_aa_judgement :
    kj (2*1 + 3) = 6 * 4^1 ∧
    kj (2*1 + 3) = 3 * 2^(2*1 + 1) ∧
    kn 4 = 30 ∧ 30 = 2 * 3 * 5 ∧
    kn 9 = 2^5 * 65 ∧
    MUFPF.CoreConstantWindow.Dn 4 - 1 = 8 * kn 4 := by
  constructor
  · exact yy_shift 1
  · constructor
    · exact yy_same_family 1
    · constructor
      · exact aa_seed4.1
      · constructor
        · exact aa_seed4.2
        · constructor
          · exact aa_k9
          · exact aa_dn_kn 4 (by norm_num)

end MUFPF.FamilyIndex
