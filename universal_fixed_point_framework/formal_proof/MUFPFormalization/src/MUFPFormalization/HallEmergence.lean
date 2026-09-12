-- ============================================================
-- HallEmergence.lean — G1（Hall 切入点）：磁平移代数 → Hall 谱生成元
-- ============================================================

/-
# HallEmergence.lean — G1 Hall 切入点：Weyl 磁平移对的生成元涌现

paper5 §5 模板"子范畴约束 → 生成元涌现"的 Hall 实例。GP 侧从密度算子 ρ
出发（需正谱锥约束），BCS 侧从 Hamiltonian H 出发（无谱条件）。本模块给出
Hall 侧：Landau 规范磁平移代数（clock/shift Weyl 对）的有限维模型——

  ωₙ = e^{2πi/n}                —— 磁通量子
  U = clock n                    —— 对角磁平移 diag(ω^i)
  V = shift n                    —— 循环移位 V eⱼ = e_{j+1}
  H_Harper = U + U† + V + V†    —— Harper 磁平移 Hamiltonian（Hermitian）

定理链（全部零 sorry）：
  clock_shift_weyl       Weyl 关系 UV = ω VU（磁平移对合关系，n ≥ 2）
  clock_star_mul_self    U 幺正（对角元共轭自逆：e^{−iθ}·e^{iθ} = 1）
  shift_star_mul_self    V 幺正（循环置换矩阵，n ≥ 1）
  shift_mul_star_self    V 幺正（另一序）
  harper_isHermitian     H_Harper Hermitian（四项各自 Hermitian 之和）
  hallGenerator_*        Hall 链 Fermi 求逆 + GP-BCS-Hall 三链会师
                         （BCSFermiEmergence 模板在 Harper Hamiltonian 上的实例）
  occupiedProjection_*   占据带谱投影（Hermitian + 幂等 + Berry 曲率实值接入）
  weyl_trace_orth        Weyl 迹正交性 Tr(U^a V^b) = n·δ_{a≡0}δ_{b≡0}
                         （Weyl 基 Hilbert-Schmidt 正交；私有链 clock_pow /
                           shift_pow / fin_add_nat_succ / omega_primitive /
                           omega_geom_sum）

数学说明：Weyl 关系 + 幺正性是磁平移代数的代数核心（Hall 侧"子范畴约束"）；
生成元构造 H → γ_F → A_Hall 复用 BCSFermiEmergence 模板（同一谱对应求逆）。
Weyl 迹正交性给出磁平移代数 ≅ Mₙ(ℂ) 的迹形式（Weyl 基 {U^a V^b}
Hilbert-Schmidt 正交，范数平方 = n），是 Landau 能级单不可约表示的
结构定理的迹层面。完整陈数理论（整性、TKNN 场论形式）、"唯一不可约
表示 = Landau 能级载体"的表示论结构定理、谱投影对参数的导数
（Berry 切向量的构造层）登记为开放（见 §末注释）。
-/

import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Data.Complex.Basic
import MUFPFormalization.SpectralDynamics
import MUFPFormalization.GPEmergence
import MUFPFormalization.BCSFermiEmergence
import MUFPFormalization.BerryChern

namespace MUFPF

open Matrix Complex

variable {n : ℕ}

/-- ωₙ 的辐角：z = 2πi/n（纯虚数）。 -/
noncomputable def omegaArg (n : ℕ) : ℂ := 2 * ↑Real.pi * Complex.I / ↑n

/-- ωₙ = e^{2πi/n}：Landau 规范磁通量子。 -/
noncomputable def omega (n : ℕ) : ℂ := Complex.exp (omegaArg n)

/-- conj(ω^i) · ω^i = 1：对角磁平移元共轭自逆（e^{−iθ}·e^{iθ} = 1）。 -/
private theorem conj_omega_pow_mul_self (n : ℕ) (i : Fin n) :
    star (omega n ^ (i : ℕ)) * omega n ^ (i : ℕ) = 1 := by
  have hstar : star (omega n) = (omega n)⁻¹ := by
    simp only [omega]
    rw [Complex.star_def, ← Complex.exp_conj, ← Complex.exp_neg]
    congr 1
    rw [Complex.ext_iff]
    refine ⟨?_, ?_⟩
    · simp [omegaArg]
    · simp [omegaArg, div_neg, neg_div]
  have hone : omega n ^ (i : ℕ) ≠ 0 := pow_ne_zero _ (Complex.exp_ne_zero _)
  rw [star_pow, hstar, inv_pow, inv_mul_cancel₀ hone]

/-- ωₙ^n = 1（n ≥ 1）。 -/
theorem omega_pow (hn : 1 ≤ n) : (omega n) ^ n = 1 := by
  have hn0 : ((n : ℕ) : ℂ) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt (Nat.lt_of_lt_of_le Nat.zero_lt_one hn))
  simp only [omega]
  rw [← Complex.exp_nat_mul]
  have hz : (↑n * omegaArg n : ℂ) = 2 * ↑Real.pi * Complex.I := by
    simp only [omegaArg]
    field_simp
  rw [hz]
  simpa using (Complex.exp_nat_mul_two_pi_mul_I 1)

/-- 降幂引理：ω^a = ω^(a % n)（n ≥ 1）——Weyl 关系指数模约化的基础。 -/
theorem omega_pow_mod (hn : 1 ≤ n) (a : ℕ) : omega n ^ a = omega n ^ (a % n) := by
  conv_lhs => rw [← Nat.mod_add_div a n, pow_add, pow_mul]
  rw [omega_pow hn, one_pow, mul_one]

/-- clock 算子（对角磁平移）：U = diag(ω^i)。 -/
noncomputable def clock (n : ℕ) : Matrix (Fin n) (Fin n) ℂ :=
  Matrix.diagonal (fun i : Fin n => omega n ^ (i : ℕ))

/-- shift 算子（循环移位磁平移）：V eⱼ = e_{j+1}（Fin n 模加法）。 -/
def shift (n : ℕ) [NeZero n] : Matrix (Fin n) (Fin n) ℂ :=
  fun i j => if i = j + 1 then 1 else 0

/-- **Weyl 关系**：UV = ω · VU（n ≥ 2）——磁平移代数的对合关系，
    Hall 侧"子范畴约束"的代数核心。 -/
theorem clock_shift_weyl {n : ℕ} [NeZero n] (hn : 2 ≤ n) :
    clock n * shift n = (omega n) • (shift n * clock n) := by
  ext i j
  simp only [clock, shift, Matrix.smul_apply, Matrix.diagonal_mul, Matrix.mul_diagonal,
    smul_eq_mul]
  split_ifs with h
  · have hpow : omega n ^ ((j + 1 : Fin n) : ℕ)
        = omega n * omega n ^ ((j : Fin n) : ℕ) := by
      rw [Fin.val_add, Fin.val_one', Nat.mod_eq_of_lt (by omega : (1 : ℕ) < n),
        ← omega_pow_mod (by omega : 1 ≤ n), pow_succ, mul_comm]
    rw [h, mul_one, one_mul, hpow]
  · simp

/-- clock 幺正：U†U = 1（对角元 e^{−iθ}·e^{iθ} = 1）。 -/
theorem clock_star_mul_self (n : ℕ) : star (clock n) * clock n = 1 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.one_apply, clock, Matrix.star_apply,
    Matrix.diagonal_apply, apply_ite star, star_one, star_zero, mul_ite, mul_one,
    mul_zero]
  have hsum : (∑ j_1 : Fin n,
        if j_1 = j then (if j_1 = i then star (omega n ^ (j_1 : ℕ)) else 0)
          * omega n ^ (j_1 : ℕ) else 0)
      = if i = j then star (omega n ^ (i : ℕ)) * omega n ^ (i : ℕ) else 0 := by
    have hs : (∑ j_1 : Fin n,
          if j_1 = j then (if j_1 = i then star (omega n ^ (j_1 : ℕ)) else 0)
            * omega n ^ (j_1 : ℕ) else 0)
        = if j = j then (if j = i then star (omega n ^ (j : ℕ)) else 0)
            * omega n ^ (j : ℕ) else 0 :=
      Finset.sum_eq_single (s := Finset.univ)
        (f := fun j_1 : Fin n => if j_1 = j then
          (if j_1 = i then star (omega n ^ (j_1 : ℕ)) else 0) * omega n ^ (j_1 : ℕ) else 0)
        (a := j) (fun k _ hkj => by rw [if_neg hkj])
        (fun hcontra => absurd (Finset.mem_univ j) hcontra)
    rw [hs, if_pos rfl]
    by_cases hij : i = j
    · subst hij
      rw [if_pos rfl, if_pos rfl]
    · rw [if_neg (fun h => hij h.symm), zero_mul, if_neg hij]
  rw [hsum]
  split_ifs
  · exact conj_omega_pow_mul_self n i
  · rfl

/-- +1 在 Fin n 上单射——循环移位的置换性基础。 -/
private theorem fin_add_one_injective {n : ℕ} [NeZero n] :
    Function.Injective fun x : Fin n => x + 1 := by
  intro a b h
  change a + 1 = b + 1 at h
  have hval := congrArg Fin.val h
  rw [Fin.val_add, Fin.val_add, Fin.val_one'] at hval
  have hn0 : n ≠ 0 := Nat.ne_of_gt (Fin.pos a)
  rcases Nat.lt_or_ge n 2 with hn2 | hn2
  · have hn1 : n = 1 := by omega
    subst hn1
    exact Subsingleton.elim a b
  · rw [Nat.mod_eq_of_lt hn2] at hval
    have ha1 : (a : ℕ) + 1 ≤ n := by omega
    have hb1 : (b : ℕ) + 1 ≤ n := by omega
    by_cases h1 : (a : ℕ) + 1 < n
    · rw [Nat.mod_eq_of_lt h1] at hval
      by_cases h2 : (b : ℕ) + 1 < n
      · rw [Nat.mod_eq_of_lt h2] at hval
        omega
      · have hb1' : (b : ℕ) + 1 = n := by omega
        rw [hb1', Nat.mod_self] at hval
        omega
    · have h1' : (a : ℕ) + 1 = n := by omega
      rw [h1', Nat.mod_self] at hval
      by_cases h2 : (b : ℕ) + 1 < n
      · rw [Nat.mod_eq_of_lt h2] at hval
        omega
      · omega

/-- +1 的原像引理：(a + (n−1)) + 1 = a（Fin n 模加法）。 -/
private theorem fin_add_pred_add_one {n : ℕ} [NeZero n] (a : Fin n) :
    ((a + (⟨(n : ℕ) - 1, Nat.sub_lt (Fin.pos a) Nat.zero_lt_one⟩ : Fin n)) + 1) = a := by
  apply Fin.ext
  rw [Fin.val_add, Fin.val_add, Fin.val_one']
  change ((((a : ℕ) + ((n : ℕ) - 1)) % n + 1 % n) % n) = (a : ℕ)
  rw [← Nat.add_mod]
  by_cases ha : (a : ℕ) = 0
  · rw [ha, Nat.zero_add]
    have h2 : (n : ℕ) - 1 + 1 = n := by omega
    rw [h2, Nat.mod_self]
  · rw [show (a : ℕ) + ((n : ℕ) - 1) + 1 = (a : ℕ) + n from by omega,
      Nat.add_mod_right, Nat.mod_eq_of_lt a.2]

/-- shift 求和核：∑ₖ δ_{a,k+1} δ_{b,k+1} = δ_{ab}（磁平移矩阵元的正交性）。 -/
private theorem shift_sum_ite {n : ℕ} [NeZero n] (a b : Fin n) :
    ∑ k : Fin n, ((if a = k + 1 then 1 else 0) * (if b = k + 1 then 1 else 0) : ℂ)
      = if a = b then 1 else 0 := by
  classical
  have hkp := fin_add_pred_add_one (n := n) a
  have hs : (∑ k : Fin n, ((if a = k + 1 then 1 else 0) * (if b = k + 1 then 1 else 0) : ℂ))
      = ((if a = a + (⟨(n : ℕ) - 1, Nat.sub_lt (Fin.pos a) Nat.zero_lt_one⟩ : Fin n) + 1
          then (1 : ℂ) else 0)
        * (if b = a + (⟨(n : ℕ) - 1, Nat.sub_lt (Fin.pos a) Nat.zero_lt_one⟩ : Fin n) + 1
          then 1 else 0)) :=
    Finset.sum_eq_single (s := Finset.univ)
      (f := fun k : Fin n => ((if a = k + 1 then 1 else 0) * (if b = k + 1 then 1 else 0) : ℂ))
      (a := a + (⟨(n : ℕ) - 1, Nat.sub_lt (Fin.pos a) Nat.zero_lt_one⟩ : Fin n))
      (fun k _ hkk₀ => by
        have hna : ¬ a = k + 1 := fun hka => hkk₀ (by
          apply fin_add_one_injective
          change k + 1
            = a + (⟨(n : ℕ) - 1, Nat.sub_lt (Fin.pos a) Nat.zero_lt_one⟩ : Fin n) + 1
          rw [← hka, hkp])
        rw [if_neg hna, zero_mul])
      (fun hcontra => absurd (Finset.mem_univ _) hcontra)
  rw [hs, hkp, if_pos rfl, one_mul]
  by_cases hab : a = b
  · subst hab
    rw [if_pos rfl]
  · rw [if_neg (fun h => hab h.symm), if_neg hab]

/-- shift 求和核（翻转形）：∑ₖ δ_{k,a+1} δ_{k,b+1} = δ_{ab}（star 在左侧时的形态）。 -/
private theorem shift_sum_ite' {n : ℕ} [NeZero n] (a b : Fin n) :
    ∑ k : Fin n, ((if k = a + 1 then 1 else 0) * (if k = b + 1 then 1 else 0) : ℂ)
      = if a = b then 1 else 0 := by
  classical
  have hs : (∑ k : Fin n, ((if k = a + 1 then 1 else 0) * (if k = b + 1 then 1 else 0) : ℂ))
      = ((if a + 1 = a + 1 then (1 : ℂ) else 0) * (if a + 1 = b + 1 then 1 else 0)) :=
    Finset.sum_eq_single (s := Finset.univ)
      (f := fun k : Fin n => ((if k = a + 1 then 1 else 0) * (if k = b + 1 then 1 else 0) : ℂ))
      (a := a + 1)
      (fun k _ hkk₀ => by rw [if_neg hkk₀, zero_mul])
      (fun hcontra => absurd (Finset.mem_univ _) hcontra)
  rw [hs, if_pos rfl, one_mul]
  by_cases hab : a = b
  · subst hab
    rw [if_pos rfl, if_pos rfl]
  · rw [if_neg (fun h => hab (fin_add_one_injective h)), if_neg hab]

/-- shift 幺正：V†V = 1（循环置换矩阵）。 -/
theorem shift_star_mul_self {n : ℕ} [NeZero n] : star (shift n) * shift n = 1 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.one_apply, shift, Matrix.star_apply, apply_ite star,
    star_one, star_zero]
  rw [shift_sum_ite' i j]

/-- shift 幺正：VV† = 1。 -/
theorem shift_mul_star_self {n : ℕ} [NeZero n] : shift n * star (shift n) = 1 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.one_apply, shift, Matrix.star_apply, apply_ite star,
    star_one, star_zero]
  rw [shift_sum_ite i j]

/-- Harper 磁平移 Hamiltonian：H = U + U† + V + V†（最近邻磁平移之和）。 -/
noncomputable def harper (n : ℕ) [NeZero n] : Matrix (Fin n) (Fin n) ℂ :=
  clock n + star (clock n) + shift n + star (shift n)

/-- H_Harper Hermitian：star(U + U† + V + V†) = U + U† + V + V†。 -/
theorem harper_isHermitian (n : ℕ) [NeZero n] : (harper n).IsHermitian :=
  Matrix.isHermitian_iff_isSelfAdjoint.2 (by
    show star (harper n) = harper n
    simp only [harper, star_add, star_star]
    abel)

/-- Hall 谱生成元：A_Hall = bcsGenerator H_Harper（磁平移 Hamiltonian 的谱生成元；
    T → 0 极限下 γ_F → 占据投影、A_Hall → 占据 Hamiltonian 的谱对数）。 -/
noncomputable def hallGenerator (n : ℕ) [NeZero n] (β : ℝ) : Matrix (Fin n) (Fin n) ℂ :=
  bcsGenerator (harper n) (harper_isHermitian n) β

/-- Hall 链 Fermi 求逆：exp(−A_Hall) = γ_F(H_Harper)（BCS 模板实例）。 -/
theorem hallGenerator_fermi_inverse (n : ℕ) [NeZero n] (β : ℝ) :
    NormedSpace.exp (-(hallGenerator n β))
      = fermiDensity (harper n) (harper_isHermitian n) β :=
  bcsGenerator_fermi_inverse _ _

/-- GP-BCS-Hall 三链会师：specGenerator γ_F(H_Harper) = A_Hall。 -/
theorem hallGenerator_spec_meeting (n : ℕ) [NeZero n] (β : ℝ) :
    specGenerator (fermiDensity (harper n) (harper_isHermitian n) β)
      (fermiDensity_isHermitian _ _ β) = hallGenerator n β :=
  specGenerator_fermiDensity _ _ _

/-- 占据示性函数（T = 0）：负能占据 occFn x = if x < 0 then 1 else 0。 -/
noncomputable def occFn (x : ℝ) : ℝ := if x < 0 then 1 else 0

/-- occFn 幂等：occFn² = occFn（谱投影的函数层根源）。 -/
theorem occFn_idem (x : ℝ) : occFn x * occFn x = occFn x := by
  classical
  unfold occFn
  split_ifs <;> ring

/-- 占据带谱投影：P = cfc(occFn) H（T = 0 极限的谱投影有限维载体）。 -/
noncomputable def occupiedProjection (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) : Matrix (Fin n) (Fin n) ℂ :=
  hH.cfc occFn

/-- 占据投影 Hermitian。 -/
theorem occupiedProjection_isHermitian (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) : (occupiedProjection H hH).IsHermitian :=
  Matrix.isHermitian_iff_isSelfAdjoint.2 (by
    unfold occupiedProjection
    rw [← Matrix.IsHermitian.cfc_eq]
    exact IsSelfAdjoint.cfc)

/-- 占据投影的共轭转置形（BerryChern 主定理 hP 参数的形态）。 -/
theorem occupiedProjection_conjTranspose (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) : Matrix.conjTranspose (occupiedProjection H hH)
      = occupiedProjection H hH :=
  occupiedProjection_isHermitian H hH

/-- 占据投影幂等：P² = P（cfc 乘法保持 + occFn 幂等的谱对角化）。 -/
theorem occupiedProjection_idempotent (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) :
    occupiedProjection H hH * occupiedProjection H hH = occupiedProjection H hH := by
  classical
  have hm : (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff.1 hH.eigenvectorUnitary.2
  have hm' : star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff'.1 hH.eigenvectorUnitary.2
  have ec : occupiedProjection H hH
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    simp only [occupiedProjection, Matrix.IsHermitian.cfc, Unitary.conjStarAlgAut_apply]
    congr 1
  rw [ec]
  have hmul : ((hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ))
      * ((hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ))
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
        * (star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
          * (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ))
        * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    noncomm_ring
  have h1 : (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
      * 1 * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
      * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * (Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ))
          * Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i)) : ℂ)))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    noncomm_ring
  have hdd : Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i) : ℝ) : ℂ)
        * ((occFn (hH.eigenvalues i) : ℝ) : ℂ))
      = Matrix.diagonal (fun i => ((occFn (hH.eigenvalues i) : ℝ) : ℂ)) := by
    congr 1
    funext i
    exact_mod_cast occFn_idem (hH.eigenvalues i)
  rw [hmul, hm', h1, Matrix.diagonal_mul_diagonal, hdd]

/-- **Hall-Berry 接入**：占据带投影的 Berry 曲率实值——BerryChern 主定理
    （`berryCurvature_im_eq_zero`）在 Hall 占据投影上的实例，Hall 电导可观测
    （σ_xy 为实数）的代数根源在磁平移模型内闭合。 -/
theorem occupied_berry_im_eq_zero (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) (A B : Matrix (Fin n) (Fin n) ℂ)
    (hA : A = Matrix.conjTranspose A) (hB : B = Matrix.conjTranspose B) :
    (berryCurvature (occupiedProjection H hH) A B).im = 0 :=
  berryCurvature_im_eq_zero _ _ _ (occupiedProjection_conjTranspose H hH).symm hA hB

/-- clock 的幂：U^a = diag(ω^{a·i})（对角元的幂次结构）。 -/
private theorem clock_pow (n : ℕ) (a : ℕ) :
    clock n ^ a = Matrix.diagonal (fun i : Fin n => omega n ^ (a * (i : ℕ))) := by
  induction a with
  | zero =>
    ext i j
    simp only [pow_zero, Matrix.one_apply, Matrix.diagonal_apply, zero_mul]
  | succ b ih =>
    rw [pow_succ, ih]
    simp only [clock, Matrix.diagonal_mul_diagonal, Pi.mul_apply, Nat.succ_mul, pow_add]

/-- Fin 加法交换引理：j + 1 + ofNat b = j + ofNat (b+1)（val 层的模同余搬移，
    Nat.ModEq 按定义即 % 相等，故可直接搬运 % 等式）。 -/
private theorem fin_add_nat_succ {n : ℕ} [NeZero n] (j : Fin n) (b : ℕ) :
    j + 1 + Fin.ofNat n b = j + Fin.ofNat n (b + 1) := by
  apply Fin.ext
  have e1 : ((j.val + 1 % n) + b % n) % n = (j.val + 1 + b) % n :=
    (((Nat.ModEq.refl j.val).add (Nat.mod_modEq 1 n)).add (Nat.mod_modEq b n))
  have e2 : (j.val + (b + 1) % n) % n = (j.val + (b + 1)) % n :=
    (Nat.ModEq.refl j.val).add (Nat.mod_modEq (b + 1) n)
  have hmid : j.val + 1 + b = j.val + (b + 1) := by rw [Nat.add_assoc, Nat.add_comm 1 b]
  have hmid' : (j.val + 1 + b) % n = (j.val + (b + 1)) % n :=
    congrArg (fun x => x % n) hmid
  rw [Fin.val_add, Fin.val_add, Fin.val_add,
    (show (Fin.ofNat n b).val = b % n from rfl),
    (show (Fin.ofNat n (b + 1)).val = (b + 1) % n from rfl), Fin.val_one']
  rw [Nat.mod_add_mod]
  exact (e1.trans hmid').trans e2.symm

/-- shift 的幂：(V^b)_{ij} = δ_{i, j+ofNat b}——循环移位幂次的置换性刻画。 -/
private theorem shift_pow {n : ℕ} [NeZero n] (b : ℕ) :
    ∀ i j : Fin n, (shift n ^ b) i j = if i = j + Fin.ofNat n b then (1 : ℂ) else 0 := by
  induction b with
  | zero =>
    intro i j
    simp only [pow_zero, Matrix.one_apply]
    rw [show j + Fin.ofNat n 0 = j from by
      apply Fin.ext
      rw [Fin.val_add, (show (Fin.ofNat n 0).val = 0 from rfl), Nat.add_zero,
        Nat.mod_eq_of_lt j.2]]
  | succ b ih =>
    intro i j
    rw [pow_succ, Matrix.mul_apply]
    have hshift : ∀ k : Fin n, shift n k j = if k = j + 1 then (1 : ℂ) else 0 := fun k => rfl
    rw [show (∑ k : Fin n, (shift n ^ b) i k * shift n k j)
        = ∑ k : Fin n, (shift n ^ b) i k * (if k = j + 1 then (1 : ℂ) else 0)
      from Finset.sum_congr rfl fun k _ => by rw [hshift k]]
    have hs : (∑ k : Fin n, (shift n ^ b) i k * (if k = j + 1 then (1 : ℂ) else 0))
        = (shift n ^ b) i (j + 1) * (if j + 1 = j + 1 then (1 : ℂ) else 0) :=
      Finset.sum_eq_single (s := Finset.univ)
        (f := fun k : Fin n => (shift n ^ b) i k * (if k = j + 1 then (1 : ℂ) else 0))
        (a := j + 1) (fun k _ hkj => by rw [if_neg hkj, mul_zero])
        (fun hcontra => absurd (Finset.mem_univ _) hcontra)
    rw [hs, ih, if_pos rfl, mul_one, fin_add_nat_succ j b]

/-- ωₙ 是 n 次本原单位根（磁通量子的代数地位：生成全体 n 次单位根）。 -/
private theorem omega_primitive {n : ℕ} [NeZero n] : IsPrimitiveRoot (omega n) n := by
  rw [omega, show omegaArg n = 2 * (↑Real.pi : ℂ) * Complex.I * (1 / ↑n) from by
    rw [omegaArg, div_eq_mul_inv, one_div]]
  simpa only [Nat.cast_one] using
    Complex.isPrimitiveRoot_exp_of_coprime 1 n (NeZero.ne n) (Nat.coprime_one_left n)

/-- 本原根几何和：∑_{i<n} (ω^a)^i = n·δ_{a≡0}——迹正交性的谱权重核心。 -/
private theorem omega_geom_sum {n : ℕ} [NeZero n] (a : ℕ) :
    ∑ i : Fin n, (omega n ^ a) ^ (i : ℕ) = if a % n = 0 then (n : ℂ) else 0 := by
  rw [Fin.sum_univ_eq_sum_range]
  have hprim := omega_primitive (n := n)
  by_cases ha : a % n = 0
  · rw [if_pos ha]
    have h1 : omega n ^ a = 1 := by
      obtain ⟨m, hm⟩ := (Nat.dvd_iff_mod_eq_zero).2 ha
      rw [hm, pow_mul, omega_pow (Nat.one_le_iff_ne_zero.2 (NeZero.ne n)), one_pow]
    simp [h1]
  · rw [if_neg ha]
    have hne : omega n ^ a ≠ 1 := by
      have hiff := hprim.pow_eq_one_iff_dvd a
      rw [Nat.dvd_iff_mod_eq_zero] at hiff
      exact fun h => ha (hiff.1 h)
    rw [geom_sum_eq hne]
    have hpow : (omega n ^ a) ^ n = 1 := by
      rw [← pow_mul, Nat.mul_comm, pow_mul, omega_pow (Nat.one_le_iff_ne_zero.2 (NeZero.ne n)),
        one_pow]
    rw [hpow, sub_self, zero_div]

/-- **Weyl 迹正交性**：Tr(U^a V^b) = n·δ_{a≡0(mod n)}·δ_{b≡0(mod n)}——磁平移代数
    ≅ Mₙ(ℂ) 的结构定理（Weyl 基 {U^a V^b} 的 Hilbert-Schmidt 正交性；中心平凡 ⟹
    唯一不可约表示 = Landau 能级载体的代数根源）。 -/
theorem weyl_trace_orth {n : ℕ} [NeZero n] (a b : ℕ) :
    (clock n ^ a * shift n ^ b).trace
      = if a % n = 0 ∧ b % n = 0 then (n : ℂ) else 0 := by
  classical
  rw [Matrix.trace]
  simp only [Matrix.diag_apply]
  have hmul : ∀ i : Fin n, (clock n ^ a * shift n ^ b) i i
      = omega n ^ (a * (i : ℕ)) * ((shift n ^ b) i i) := by
    intro i
    rw [Matrix.mul_apply]
    have hs : (∑ k : Fin n, (clock n ^ a) i k * (shift n ^ b) k i)
        = (clock n ^ a) i i * (shift n ^ b) i i :=
      Finset.sum_eq_single (s := Finset.univ)
        (f := fun k : Fin n => (clock n ^ a) i k * (shift n ^ b) k i)
        (a := i)
        (fun k _ hki => by
          rw [clock_pow, Matrix.diagonal_apply, if_neg (fun h => hki h.symm), zero_mul])
        (fun hcontra => absurd (Finset.mem_univ _) hcontra)
    rw [hs, clock_pow, Matrix.diagonal_apply, if_pos rfl]
  rw [Finset.sum_congr rfl fun i _ => hmul i]
  have hdiag : ∀ i : Fin n, (shift n ^ b) i i = if b % n = 0 then (1 : ℂ) else 0 := by
    intro i
    rw [shift_pow b i i]
    by_cases hb : b % n = 0
    · rw [if_pos hb, if_pos]
      apply Fin.ext
      rw [Fin.val_add, (show (Fin.ofNat n b).val = b % n from rfl), hb, Nat.add_zero,
        Nat.mod_eq_of_lt i.2]
    · rw [if_neg hb, if_neg]
      rintro he
      have hval := congrArg Fin.val he
      rw [Fin.val_add, (show (Fin.ofNat n b).val = b % n from rfl)] at hval
      have hlt : b % n < n := Nat.mod_lt b (NeZero.pos n)
      have h1 := Nat.div_add_mod (i.val + b % n) n
      rw [← hval] at h1
      have hc : b % n = n * ((i.val + b % n) / n) := by omega
      have hq0 : (i.val + b % n) / n = 0 := by
        by_contra hq0
        have hq1 : (1 : ℕ) ≤ (i.val + b % n) / n := Nat.one_le_iff_ne_zero.2 hq0
        nlinarith [NeZero.pos n, hlt, hc]
      rw [hq0, Nat.mul_zero] at hc
      exact hb hc
  rw [Finset.sum_congr rfl fun i _ => by rw [hdiag i]]
  by_cases hb : b % n = 0
  · rw [Finset.sum_congr rfl fun i _ => by rw [if_pos hb, mul_one],
      Finset.sum_congr rfl fun i _ => by rw [pow_mul], omega_geom_sum a]
    by_cases ha : a % n = 0
    · rw [if_pos (show a % n = 0 ∧ b % n = 0 from ⟨ha, hb⟩), if_pos ha]
    · rw [if_neg (show ¬(a % n = 0 ∧ b % n = 0) from fun h => ha h.1), if_neg ha]
  · rw [Finset.sum_congr rfl fun i _ => by rw [if_neg hb, mul_zero],
      if_neg (show ¬(a % n = 0 ∧ b % n = 0) from fun h => hb h.2)]
    simp

/- §末开放登记（不占用 sorry，真证路径）：

  1. **陈数整性与 TKNN**：C = (1/2π)∫F ∈ ℤ 与 σ_xy = (e²/h)C 需环面积分/
     拓扑度/Kubo 线性响应基础设施（BerryChern 已登记）。
  2. **谱投影切向量**：A = ∂ₓP、B = ∂ᵧP 的构造（投影族参数导数）属微积分
     基础设施；当前 occupied_berry_im_eq_zero 以任意厄米切向量为假设接入。
  3. **Harper 谱隙**：Hofstadter Butterfly 的谱隙结构（通量 p/q 时 q 能带）
     需具体谱计算，数值层已有载体。
  4. **唯一不可约表示**：磁平移代数 ≅ Mₙ(ℂ) 的表示论结构定理
     （唯一 n 维不可约表示 = Landau 能级载体）——迹层面已由
     weyl_trace_orth 闭合，表示层需 Schur/矩阵代数表示论基础设施。

  已闭合（本模块，零 sorry）：Weyl 关系 + clock/shift 幺正性 + Harper Hermitian
  + Hall 生成元链（Fermi 求逆 + 三链会师）+ 占据投影（Hermitian/幂等）
  + Hall-Berry 曲率实值接入 + Weyl 迹正交性（weyl_trace_orth：Weyl 基
  Hilbert-Schmidt 正交，磁平移代数 ≅ Mₙ(ℂ) 结构定理的迹形式）。
  G1 的三个切入点（GP/BCS/Hall）至此全部闭合。 -/

end MUFPF
