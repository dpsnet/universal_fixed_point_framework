import MUFPFormalization.FamilyIndexIdentities
import MUFPFormalization.SilentFamilyMechanismIdentities

/-!
# P7-5e-218 ★ NN：两 k 序列步进比 + OO：GG 族 m 闭式

对应 209 系列（218 ⑱ NN+OO 数值定案，2026-10-16）：

- ★ NN1 两 k 序列的 2 进步进：k_j 每步 ×2（指数系数 1：指数=j−2）、
  k_{2j+3} 每步 ×4（窗口对合族，指数系数 2：指数=2j+1）、k_n 2 进部分
  每步 ×2（指数系数 1：指数=n−4）；
- ★ NN2 DD2 族与窗口对合族共享指数/下标系数 2（指数步进 = 2×下标步进：
  DD2 3→6、Bott 8→16）；k_j/k_n 基础族系数 1；
- ★ NN3 Bott 周期 8 ↔ 指数步进 16（4^8 = 2^16 = 65536）——系数 2 使周期翻倍；
- ★ OO1 GG 族静默下标 m_k 闭式 m_k = (2^{3k+1}+21k−2)/7（k=1..7：
  5,24,155,1182,9377,74916,599207 全 True）；
- OO2 渐近主导项 (2/7)·8^k（2·8^k = 2^{3k+1}），余项 3k−2/7；
- OO3 m_{k+1}/m_k → 8 增长因子（4.8,6.46,7.63,7.93→8）。

数值先证伪（勿重跑）：`scripts/_phase102_p7_5e218_nn_oo_kseq_step_ratio_gg_m_closed.py`
+ 同目录 json（NN1~NN3/OO1 全 ok=true，2026-10-16）。

诚实边界：NN1 指数系数核对（序列定义）、NN2 系数观察（2 vs 1，形式观察）、
NN3 恒等核对（4^8=2^16）、OO1 代数化简（闭式恒等，290 gg_m_closed 等价）、
OO2/OO3 渐近分析（主导项/比值）——候选层未升定案层。
-/

namespace MUFPF.KSeqStepRatio

open Nat
open MUFPF.FamilyIndex
open MUFPF.SilentFamilyMechanism

/-! ## §0 定义 -/

/-- GG 族分母 n_k = (2^{3k+1}−2)/7（GG 族成员 n 下标；290 gg_dvd 保证整除）。 -/
def gg_n (k : ℕ) : ℕ := (2^(3*k+1) - 2) / 7

/-- GG 族静默下标 m_k = n_k + 3k（= 292 Gm 值函数；D(n_k)=2^{m_k}+1 的指数）。 -/
def gg_m (k : ℕ) : ℕ := gg_n k + 3*k

/-! ## §1 ★ NN：两 k 序列步进比 -/

/-- ★ k_j 每步 ×2（指数系数 1：指数=j−2，j≥2 定义域内）。 -/
theorem kj_step_double (j : ℕ) (hj : 2 ≤ j) : kj (j + 1) = 2 * kj j := by
  unfold kj
  have h1 : (j + 1) - 2 = j - 1 := by omega
  have h2 : j - 1 = (j - 2) + 1 := by omega
  rw [h1, h2]
  rw [pow_succ]
  ring

/-- ★ k_{2j+3} 每步 ×4（窗口对合族，指数系数 2：指数=2j+1——
    下标步进 2 ⟺ 值 ×4）。 -/
theorem win_step_quad (j : ℕ) : kj (2 * (j + 1) + 3) = 4 * kj (2 * j + 3) := by
  rw [yy_shift (j + 1), yy_shift j]
  rw [pow_succ]
  ring

/-- ★ k_n 2 进部分每步 ×2（指数系数 1：指数=n−4，n≥4 定义域内）。 -/
theorem kn_exp_step (n : ℕ) (hn : 4 ≤ n) : 2^(n + 1 - 4) = 2 * 2^(n - 4) := by
  have h1 : n + 1 - 4 = n - 3 := by omega
  have h2 : n - 3 = (n - 4) + 1 := by omega
  rw [h1, h2]
  rw [pow_succ]
  ring

/-! ## §2 ★ NN2/NN3：DD2 与窗口对合共享系数 2；Bott 周期 8 ↔ 指数 16 -/

/-- ★ DD2 族：下标步进 3 → 指数步进 6 = 2×3（系数 2：指数步进 = 2×下标步进）。 -/
theorem dd2_exp_step (j : ℕ) : (2 * (j + 3) + 4) = (2 * j + 4) + 2 * 3 := by
  ring

/-- ★ Bott：周期 8 → 指数步进 16 = 2×8（窗口对合族系数 2 使周期翻倍）。 -/
theorem bott_exp_step : 16 = 2 * 8 := by
  norm_num

/-- ★ NN3：Bott 周期 8 ↔ 指数步进 16——4^8 = 2^16 = 65536（恒等核对）。 -/
theorem four_pow_eight : 4^8 = 2^16 ∧ 2^16 = 65536 := by
  constructor <;> norm_num

/-! ## §3 ★ OO：GG 族 m 闭式 -/

/-- ★ OO1：m_k = (2^{3k+1}+21k−2)/7 精确闭式（290 gg_m_closed 的 m 函数形式）。 -/
theorem oo1_m_closed (k : ℕ) : gg_m k = (2^(3*k+1) + 21*k - 2) / 7 := by
  unfold gg_m gg_n
  exact gg_m_closed k

/-- OO1 乘法形式：7·m_k = 2^{3k+1} + 21k − 2（整除精确性，供差分运算）。 -/
theorem oo1_mul (k : ℕ) : 7 * gg_m k = 2^(3*k+1) + 21*k - 2 := by
  unfold gg_m gg_n
  have hdiv : 7 ∣ (2^(3*k+1) - 2) := gg_dvd k
  rcases hdiv with ⟨c, hc⟩
  have ha : 2 ≤ 2^(3*k+1) := by
    exact pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 1 ≤ 3*k+1)
  calc
    7 * ((2^(3*k+1) - 2) / 7 + 3*k) = 7 * (c + 3*k) := by
      congr 1
      rw [hc]
      rw [Nat.mul_div_right c (by norm_num : 0 < 7)]
    _ = 7*c + 21*k := by ring
    _ = (2^(3*k+1) - 2) + 21*k := by rw [← hc]
    _ = 2^(3*k+1) + 21*k - 2 := by omega

/-- OO1 加二形式：7·m_k + 2 = 2^{3k+1} + 21k（无减法，便于差分运算）。 -/
theorem oo1_plus (k : ℕ) : 7 * gg_m k + 2 = 2^(3*k+1) + 21*k := by
  rw [oo1_mul k]
  have hpow : 2 ≤ 2^(3*k+1) := by
    simpa using (pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 1 ≤ 3*k+1))
  have ha : 2 ≤ 2^(3*k+1) + 21*k := by
    omega
  omega

/-- OO1 实例：k=1..7 → 5,24,155,1182,9377,74916,599207（292 gm_instances 核对）。 -/
theorem oo1_instances :
    gg_m 1 = 5 ∧ gg_m 2 = 24 ∧ gg_m 3 = 155 ∧ gg_m 4 = 1182 ∧
    gg_m 5 = 9377 ∧ gg_m 6 = 74916 ∧ gg_m 7 = 599207 := by
  unfold gg_m gg_n
  norm_num

/-- ★ OO2：主导项 2·8^k = 2^{3k+1}（8=2^3 幂恒等——渐近 (2/7)·8^k 的幂内核）。 -/
theorem oo2_leading (k : ℕ) : 2 * 8^k = 2^(3*k + 1) := by
  calc
    2 * 8^k = 2 * 2^(3*k) := by
      rw [show 8 = 2^3 by norm_num]
      rw [pow_mul]
    _ = 2^(3*k + 1) := by
      rw [mul_comm]
      rw [← pow_succ]

/-- ★ OO3：m_{k+1} < 8·m_k（k≥1）——比值 (m_{k+1}/m_k) < 8 且单调趋 8（渐近增长因子）。 -/
theorem oo3_trend (k : ℕ) (hk : 1 ≤ k) : gg_m (k + 1) < 8 * gg_m k := by
  have hA : 7 * gg_m (k + 1) + 2 = 2^(3*k+4) + 21*k + 21 := by
    calc
      7 * gg_m (k + 1) + 2 = 2^(3*(k+1)+1) + 21*(k+1) := oo1_plus (k + 1)
      _ = 2^(3*k+4) + 21*k + 21 := by
        have hExp : 3 * (k + 1) + 1 = 3 * k + 4 := by omega
        rw [hExp]
        omega
  have hB : 7 * (8 * gg_m k) + 16 = 2^(3*k+4) + 168*k := by
    calc
      7 * (8 * gg_m k) + 16 = 8 * (7 * gg_m k) + 16 := by ring
      _ = 8 * (7 * gg_m k) + 8 * 2 := by norm_num
      _ = 8 * (7 * gg_m k + 2) := by rw [← Nat.mul_add]
      _ = 8 * (2^(3*k+1) + 21*k) := by rw [oo1_plus k]
      _ = 8 * 2^(3*k+1) + 168*k := by ring
      _ = 2^(3*k+4) + 168*k := by
        rw [show 8 = 2^3 by norm_num]
        rw [← pow_add]
        rw [show 3 + (3*k+1) = 3*k+4 by omega]
  have hA2 : 7 * (8 * gg_m k) + 16 = (7 * gg_m (k + 1) + 2) + (147*k - 21) := by
    rw [hB, hA]
    omega
  have hstep : 7 * gg_m (k + 1) + 7 + 16 ≤ 7 * (8 * gg_m k) + 16 := by
    rw [hA2]
    omega
  have hstep' : 7 * gg_m (k + 1) + 7 ≤ 7 * (8 * gg_m k) := by
    omega
  have hle' : 7 * (gg_m (k + 1) + 1) ≤ 7 * (8 * gg_m k) := by
    have hfac : 7 * (gg_m (k + 1) + 1) = 7 * gg_m (k + 1) + 7 := by
      rw [Nat.mul_add]
    rw [hfac]
    exact hstep'
  have hlt' : gg_m (k + 1) + 1 ≤ 8 * gg_m k :=
    Nat.le_of_mul_le_mul_left hle' (by norm_num : 0 < 7)
  omega

/-! ## §4 联合主定理 -/

/-- ★★ NN×OO 联合：步进比（k_j ×2、k_{2j+3} ×4、k_n 2 进 ×2）× 系数 2 共享
    （DD2 指数步进=2×3）× Bott 周期（4^8=2^16=65536）× GG m 闭式（首尾实例）×
    主导项（2·8^3=2^10）× 增长因子（m_2<8·m_1）。
    —— 218 ⑱ 的数值主定理。 -/
theorem nn_oo_judgement :
    kj (2 + 1) = 2 * kj 2 ∧
    kj (2 * (0 + 1) + 3) = 4 * kj (2 * 0 + 3) ∧
    2^(6 + 1 - 4) = 2 * 2^(6 - 4) ∧
    4^8 = 2^16 ∧ 2^16 = 65536 ∧
    gg_m 1 = 5 ∧ gg_m 7 = 599207 ∧
    2 * 8^3 = 2^(3*3 + 1) ∧
    gg_m (1 + 1) < 8 * gg_m 1 := by
  constructor
  · exact kj_step_double 2 (by norm_num)
  · constructor
    · exact win_step_quad 0
    · constructor
      · exact kn_exp_step 6 (by norm_num)
      · constructor
        · exact four_pow_eight.1
        · constructor
          · exact four_pow_eight.2
          · constructor
            · exact oo1_instances.1
            · constructor
              · exact oo1_instances.2.2.2.2.2.2
              · constructor
                · exact oo2_leading 3
                · exact oo3_trend 1 (by norm_num)

end MUFPF.KSeqStepRatio
