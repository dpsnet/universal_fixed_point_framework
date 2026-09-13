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
  occupiedProjection_*   占据带谱投影（Hermitian + 幂等 + Berry 曲率实值接入
                         + [H,P]=0 交换性；后者为 Sylvester 方程前提）
  weyl_trace_orth        Weyl 迹正交性 Tr(U^a V^b) = n·δ_{a≡0}δ_{b≡0}
                         （Weyl 基 Hilbert-Schmidt 正交；私有链 clock_pow /
                           shift_pow / fin_add_nat_succ / omega_primitive /
                           omega_geom_sum）
  weyl_basis_linearIndep Weyl 基线性无关 {U^a V^b}_{a,b<n}（对偶配对
                         Tr(W_p D_q) = n·δ_{pq}；私有链 clock_shift_weyl_gen /
                           clock_pow_shift_weyl / clock_shift_pow_weyl /
                           shift_pow_clock_weyl / weyl_scalar / weyl_mul_dual /
                           weyl_pairing / nat_add_sub_mod_eq_zero /
                           trace_sum_smul_fin）
  weyl_span_top          Weyl 基定理：{U^a V^b}_{a,b<n} 张成 Mₙ(ℂ)
                         （磁平移代数 ≅ Mₙ(ℂ) 结构定理的向量空间形式，维数
                           n² = finrank；线性无关 + 基数 = finrank 论证）
  magAlgEquiv            磁平移结构定理（表示论层）：磁平移商代数 ≃ₐ Mₙ(ℂ)
                         （ℂ⟨U,V⟩/(UV−ωVU, Uⁿ−1, Vⁿ−1) 的 ℂ-代数同构；
                           私有链 magneticAlgebra/magRel + magWeyl/magPowX/magPowY
                           关系保持 + magXShiftWeyl/magXpowShiftWeyl/magYpowXpow
                           幂次换位 + magWeylElem_* 单型元 + magL_mul_mem/magAlg_span
                           张成定理 + magHom 泛性质下降 + magHom_surjective +
                           magBasisMap_surjective/magFinite/magFinrank_eq 等维）

数学说明：Weyl 关系 + 幺正性是磁平移代数的代数核心（Hall 侧"子范畴约束"）；
生成元构造 H → γ_F → A_Hall 复用 BCSFermiEmergence 模板（同一谱对应求逆）。
Weyl 迹正交性给出磁平移代数 ≅ Mₙ(ℂ) 的迹形式（Weyl 基 {U^a V^b}
Hilbert-Schmidt 正交，范数平方 = n）；Weyl 基定理（线性无关 + 张成）
给出结构定理的向量空间形式——n² 个 Weyl 元构成 Mₙ(ℂ) 的基，即
"唯一不可约表示 = Landau 能级载体"的代数根源（中心平凡 + 迹配对非退化）。
完整陈数理论（整性、TKNN 场论形式）登记为开放；谱投影切向量的
**约束代数层**已由 BerryChern §2.5 四定理 + 本模块 occupiedProjection_commute
闭合（[H,P]=0 + 带内消没 + 带间化简 + 双交换子形式），切向量的**分析构造**
（cfc 对参数的可微性，Kato 微扰论）仍开放（见 §末注释）。结构定理表示论层
已由 magAlgEquiv 闭合。
-/

import Mathlib.Algebra.FreeAlgebra
import Mathlib.Algebra.RingQuot
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute
import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
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

/-- **谱投影交换性**：H·P = P·H——占据带是 H 的约化谱子空间（谱投影定义性质
    的矩阵层闭合），绝热微扰 Sylvester 方程 [H, Ṗ] = [P, Ḣ] 左端交换性的
    前提。证明：泛函演算交换性——与 H 交换的元与 cfc f H 交换（selfadjoint
    commute_cfc），取 f = occFn。 -/
theorem occupiedProjection_commute (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) :
    H * occupiedProjection H hH = occupiedProjection H hH * H := by
  have h1 : Commute (cfc occFn H) H :=
    IsSelfAdjoint.commute_cfc hH.isSelfAdjoint (Commute.refl H) occFn
  rw [Matrix.IsHermitian.cfc_eq hH occFn] at h1
  exact h1.eq.symm

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

/-- Weyl 关系（n ≥ 1 全情形）：n = 1 时 U = V = 1、ω₁ = 1 退化情形并入。 -/
private theorem clock_shift_weyl_gen {n : ℕ} [NeZero n] :
    clock n * shift n = (omega n) • (shift n * clock n) := by
  by_cases hn : 2 ≤ n
  · exact clock_shift_weyl hn
  · push_neg at hn
    have hn0 : n ≠ 0 := NeZero.ne n
    have hn1 : n = 1 := by omega
    subst hn1
    have hc : clock 1 = 1 := by
      ext i j
      rw [clock, Matrix.diagonal_apply, Matrix.one_apply]
      split_ifs with hij
      · have hi : (i : ℕ) = 0 := Nat.lt_one_iff.1 i.2
        rw [hi, pow_zero]
      · rfl
    have hs : shift 1 = 1 := by
      ext i j
      rw [shift, Matrix.one_apply]
      have hjj : (j + 1 : Fin 1) = j := by
        apply Fin.ext
        rw [Fin.val_add, Fin.val_one', Nat.mod_self, Nat.add_zero, Nat.mod_eq_of_lt j.2]
      by_cases hij : i = j + 1
      · rw [if_pos hij, if_pos (hjj ▸ hij)]
      · rw [if_neg hij, if_neg (fun h => hij (hjj.symm ▸ h))]
    rw [hc, hs]
    have hw : omega 1 = 1 := by
      simpa [omega, omegaArg] using (Complex.exp_nat_mul_two_pi_mul_I 1)
    rw [hw]
    simp

/-- 幂次 Weyl 换位（一）：U^a V = ω^a · V U^a（归纳提升 clock_shift_weyl_gen）。 -/
private theorem clock_pow_shift_weyl {n : ℕ} [NeZero n] (a : ℕ) :
    clock n ^ a * shift n = (omega n ^ a : ℂ) • shift n * clock n ^ a := by
  induction a with
  | zero => simp
  | succ b ih =>
    rw [pow_succ, Matrix.mul_assoc, clock_shift_weyl_gen, mul_smul_comm,
      ← Matrix.mul_assoc (clock n ^ b) (shift n) (clock n), ih,
      smul_mul_assoc (omega n ^ b) (shift n) (clock n ^ b),
      smul_mul_assoc (omega n ^ b) (shift n * clock n ^ b) (clock n),
      Matrix.mul_assoc (shift n) (clock n ^ b) (clock n),
      smul_smul, ← pow_succ',
      ← smul_mul_assoc (omega n ^ (b + 1)) (shift n) (clock n ^ b * clock n)]

/-- 幂次 Weyl 换位（二）：U^a V^c = ω^{ac} · V^c U^a（对 shift 幂归纳）。 -/
private theorem clock_shift_pow_weyl {n : ℕ} [NeZero n] (a c : ℕ) :
    clock n ^ a * shift n ^ c
      = (omega n ^ (a * c) : ℂ) • shift n ^ c * clock n ^ a := by
  induction c with
  | zero => simp
  | succ b ih =>
    rw [Nat.mul_succ, pow_succ, ← Matrix.mul_assoc (clock n ^ a) (shift n ^ b) (shift n), ih,
      smul_mul_assoc (omega n ^ (a * b)) (shift n ^ b) (clock n ^ a),
      smul_mul_assoc (omega n ^ (a * b)) (shift n ^ b * clock n ^ a) (shift n),
      Matrix.mul_assoc (shift n ^ b) (clock n ^ a) (shift n),
      clock_pow_shift_weyl a,
      ← Matrix.mul_assoc (shift n ^ b) ((omega n ^ a) • shift n) (clock n ^ a),
      mul_smul_comm (omega n ^ a) (shift n ^ b) (shift n),
      smul_mul_assoc (omega n ^ a) (shift n ^ b * shift n) (clock n ^ a),
      smul_smul,
      pow_add (omega n),
      smul_mul_assoc (omega n ^ (a * b) * omega n ^ a) (shift n ^ b * shift n) (clock n ^ a)]

/-- 幂次 Weyl 换位（三）：V^c U^d = ω^{cd}⁻¹ · U^d V^c（由（二）取逆）。 -/
private theorem shift_pow_clock_weyl {n : ℕ} [NeZero n] (c d : ℕ) :
    shift n ^ c * clock n ^ d
      = ((omega n ^ (c * d) : ℂ))⁻¹ • clock n ^ d * shift n ^ c := by
  have h := clock_shift_pow_weyl (n := n) d c
  rw [Nat.mul_comm] at h
  have hne : (omega n ^ (c * d) : ℂ) ≠ 0 := pow_ne_zero _ (Complex.exp_ne_zero _)
  rw [smul_mul_assoc, h, ← smul_mul_assoc, smul_smul, inv_mul_cancel₀ hne, one_smul]

/-- 配对标量化简：ω^{ac}·(ω^{c(a+n−a')})⁻¹ = ω^{ca'}——指数差 c·n 经 ω^n = 1 吸收。 -/
private theorem weyl_scalar {n : ℕ} [NeZero n] {a a' c : ℕ} (ha' : a' ≤ n) :
    (omega n ^ (a * c)) * (omega n ^ (c * (a + (n - a'))))⁻¹
      = omega n ^ (c * a') := by
  have hA : a' + (a + (n - a')) = a + n := by omega
  have hn1 : 1 ≤ n := Nat.one_le_iff_ne_zero.2 (NeZero.ne n)
  have hne : (omega n ^ (c * (a + (n - a'))) : ℂ) ≠ 0 := pow_ne_zero _ (Complex.exp_ne_zero _)
  have hcn : (omega n ^ (c * n)) = 1 := by
    rw [show c * n = n * c from Nat.mul_comm c n, pow_mul, omega_pow hn1, one_pow]
  have h1 : (omega n ^ (c * a))
      = (omega n ^ (c * a')) * (omega n ^ (c * (a + (n - a')))) := by
    calc (omega n ^ (c * a)) = (omega n ^ (c * a)) * 1 := (mul_one _).symm
      _ = (omega n ^ (c * a)) * omega n ^ (c * n) := by rw [hcn]
      _ = omega n ^ (c * a + c * n) := by rw [pow_add]
      _ = omega n ^ (c * a' + c * (a + (n - a'))) := by
          rw [show c * a + c * n = c * a' + c * (a + (n - a')) from by
            rw [← Nat.mul_add, ← Nat.mul_add, hA]]
      _ = _ := by rw [pow_add]
  rw [show a * c = c * a from Nat.mul_comm a c, h1, mul_assoc, mul_inv_cancel₀ hne, mul_one]

/-- Weyl 元 × 对偶元 = 标量 × U^{a+n−a'} V^{b+n−b'}（磁平移对合的配对重排）。 -/
private theorem weyl_mul_dual {n : ℕ} [NeZero n] (a b a' b' : Fin n) :
    (clock n ^ (a : ℕ) * shift n ^ (b : ℕ))
      * (shift n ^ (n - (b' : ℕ)) * clock n ^ (n - (a' : ℕ)))
    = (omega n ^ (((b : ℕ) + (n - (b' : ℕ))) * (a' : ℕ))) •
        (clock n ^ ((a : ℕ) + (n - (a' : ℕ)))
          * shift n ^ ((b : ℕ) + (n - (b' : ℕ)))) := by
  rw [Matrix.mul_assoc,
    ← Matrix.mul_assoc (shift n ^ (b : ℕ)) (shift n ^ (n - (b' : ℕ)))
      (clock n ^ (n - (a' : ℕ))),
    ← pow_add (shift n) (b : ℕ) (n - (b' : ℕ)),
    ← Matrix.mul_assoc (clock n ^ (a : ℕ)) (shift n ^ ((b : ℕ) + (n - (b' : ℕ))))
      (clock n ^ (n - (a' : ℕ))),
    clock_shift_pow_weyl (a : ℕ) ((b : ℕ) + (n - (b' : ℕ))),
    smul_mul_assoc (omega n ^ ((a : ℕ) * ((b : ℕ) + (n - (b' : ℕ)))))
      (shift n ^ ((b : ℕ) + (n - (b' : ℕ)))) (clock n ^ (a : ℕ)),
    smul_mul_assoc (omega n ^ ((a : ℕ) * ((b : ℕ) + (n - (b' : ℕ)))))
      (shift n ^ ((b : ℕ) + (n - (b' : ℕ))) * clock n ^ (a : ℕ))
      (clock n ^ (n - (a' : ℕ))),
    Matrix.mul_assoc (shift n ^ ((b : ℕ) + (n - (b' : ℕ)))) (clock n ^ (a : ℕ))
      (clock n ^ (n - (a' : ℕ))),
    ← pow_add (clock n) (a : ℕ) (n - (a' : ℕ)),
    shift_pow_clock_weyl ((b : ℕ) + (n - (b' : ℕ))) ((a : ℕ) + (n - (a' : ℕ))),
    smul_mul_assoc ((omega n ^ (((b : ℕ) + (n - (b' : ℕ))) * ((a : ℕ) + (n - (a' : ℕ)))))⁻¹)
      (clock n ^ ((a : ℕ) + (n - (a' : ℕ))))
      (shift n ^ ((b : ℕ) + (n - (b' : ℕ)))),
    smul_smul, weyl_scalar (le_of_lt (a'.2))]

/-- 加性模吸收：a, a' < n 时 (a + (n − a')) % n = 0 ⟹ a = a'——配对离对角判别。 -/
private theorem nat_add_sub_mod_eq_zero {n a a' : ℕ} (hn : 0 < n) (ha : a < n) (ha' : a' < n)
    (h : (a + (n - a')) % n = 0) : a = a' := by
  have h2 : a + n - a' = a + (n - a') := by omega
  rw [← h2] at h
  obtain ⟨k, hk⟩ := (Nat.dvd_iff_mod_eq_zero).2 h
  have hpos : 0 < a + n - a' := by omega
  have hlt : a + n - a' < 2 * n := by omega
  have h2n : n * k < n * 2 := by rw [← hk, Nat.mul_comm]; exact hlt
  have hk2 : k < 2 := (Nat.mul_lt_mul_left hn).1 h2n
  have hk0 : k ≠ 0 := by
    rintro rfl
    rw [Nat.mul_zero] at hk
    omega
  have hk1 : k = 1 := by omega
  rw [hk1, Nat.mul_one] at hk
  omega

/-- **Weyl 对偶配对**：Tr(W_p · D_q) = n·δ_{pq}——迹形式下的对偶基配对
    （D_q = V^{n−b'} U^{n−a'}；对角 n、离对角 0）。 -/
private theorem weyl_pairing {n : ℕ} [NeZero n] (p q : Fin n × Fin n) :
    ((clock n ^ (p.1 : ℕ) * shift n ^ (p.2 : ℕ))
      * (shift n ^ (n - (q.2 : ℕ)) * clock n ^ (n - (q.1 : ℕ)))).trace
      = if p = q then (n : ℂ) else 0 := by
  obtain ⟨a, b⟩ := p
  obtain ⟨a', b'⟩ := q
  dsimp only
  by_cases heq : a = a' ∧ b = b'
  · obtain ⟨rfl, rfl⟩ := heq
    rw [if_pos rfl, weyl_mul_dual, Matrix.trace_smul, weyl_trace_orth]
    have han : (a : ℕ) + (n - (a : ℕ)) = n := Nat.add_sub_cancel' (Nat.le_of_lt a.2)
    have hbn : (b : ℕ) + (n - (b : ℕ)) = n := Nat.add_sub_cancel' (Nat.le_of_lt b.2)
    rw [han, hbn, pow_mul, omega_pow (Nat.one_le_iff_ne_zero.2 (NeZero.ne n)), one_pow,
      one_smul, Nat.mod_self, if_pos (show (0 : ℕ) = 0 ∧ (0 : ℕ) = 0 from ⟨rfl, rfl⟩)]
  · rw [if_neg (show ¬(⟨a, b⟩ : Fin n × Fin n) = ⟨a', b'⟩ from fun h => by
        rw [Prod.mk.injEq] at h; exact heq h)]
    rw [weyl_mul_dual, Matrix.trace_smul, weyl_trace_orth]
    have hcond : ¬(((a : ℕ) + (n - (a' : ℕ))) % n = 0 ∧ ((b : ℕ) + (n - (b' : ℕ))) % n = 0) :=
      fun h => heq ⟨Fin.ext (nat_add_sub_mod_eq_zero (NeZero.pos n) a.2 a'.2 h.1),
        Fin.ext (nat_add_sub_mod_eq_zero (NeZero.pos n) b.2 b'.2 h.2)⟩
    rw [if_neg hcond, smul_zero]

/-- trace 的有限和-标量引理：Tr(∑ g p • M p) = ∑ g p · Tr(M p)。 -/
private theorem trace_sum_smul_fin {n : ℕ} {ι : Type*} [Fintype ι]
    (g : ι → ℂ) (M : ι → Matrix (Fin n) (Fin n) ℂ) :
    (∑ p, g p • M p).trace = ∑ p, g p * (M p).trace :=
  calc (∑ p, g p • M p).trace
      = Matrix.traceLinearMap (Fin n) ℂ ℂ (∑ p, g p • M p) :=
        (Matrix.traceLinearMap_apply (Fin n) ℂ ℂ _).symm
    _ = ∑ p, Matrix.traceLinearMap (Fin n) ℂ ℂ (g p • M p) :=
        map_sum (Matrix.traceLinearMap (Fin n) ℂ ℂ) (fun p => g p • M p) Finset.univ
    _ = ∑ p, g p * (M p).trace := by
        refine Finset.sum_congr rfl fun p _ => ?_
        rw [map_smul, smul_eq_mul, Matrix.traceLinearMap_apply]

/-- **Weyl 基线性无关**：{U^a V^b}_{a,b<n} 在 ℂ 上线性无关——Hilbert-Schmidt
    迹配对 ⟨W_p, D_q⟩ = n·δ_{pq} 的直接推论。 -/
theorem weyl_basis_linearIndependent {n : ℕ} [NeZero n] :
    LinearIndependent ℂ fun p : Fin n × Fin n =>
      clock n ^ (p.1 : ℕ) * shift n ^ (p.2 : ℕ) := by
  classical
  rw [Fintype.linearIndependent_iff]
  intro g hg q
  have htr := congrArg Matrix.trace
    (congrArg (fun X : Matrix (Fin n) (Fin n) ℂ =>
      X * (shift n ^ (n - (q.2 : ℕ)) * clock n ^ (n - (q.1 : ℕ)))) hg)
  rw [Matrix.zero_mul, Matrix.trace_zero, Finset.sum_mul,
    Finset.sum_congr rfl fun i _ =>
      smul_mul_assoc (g i) (clock n ^ (i.1 : ℕ) * shift n ^ (i.2 : ℕ))
        (shift n ^ (n - (q.2 : ℕ)) * clock n ^ (n - (q.1 : ℕ))),
    trace_sum_smul_fin,
    Finset.sum_congr rfl fun p _ => by rw [weyl_pairing p q]] at htr
  have h2 := Finset.sum_eq_single (s := Finset.univ)
    (f := fun p : Fin n × Fin n => g p * (if p = q then (n : ℂ) else 0))
    (a := q)
    (fun p _ hpq => by rw [if_neg hpq, mul_zero])
    (fun hcontra => absurd (Finset.mem_univ _) hcontra)
  rw [h2, if_pos rfl] at htr
  have hn0 : (n : ℂ) ≠ 0 := by exact_mod_cast NeZero.ne n
  rcases mul_eq_zero.1 htr with h | h
  · exact h
  · exact absurd h hn0

/-- **Weyl 基定理**：{U^a V^b}_{a,b<n} 张成 Mₙ(ℂ)——磁平移代数 ≅ Mₙ(ℂ) 结构定理的
    向量空间形式：n² 个 Weyl 元构成 Mₙ(ℂ) 的基（中心平凡 + 迹配对非退化 ⟹ 忠实作用
    于唯一的 n 维不可约表示 = Landau 能级载体的代数根源）。 -/
theorem weyl_span_top {n : ℕ} [NeZero n] :
    Submodule.span ℂ (Set.range fun p : Fin n × Fin n =>
      clock n ^ (p.1 : ℕ) * shift n ^ (p.2 : ℕ)) = ⊤ :=
  weyl_basis_linearIndependent.span_eq_top_of_card_eq_finrank (by
    rw [Fintype.card_prod, Fintype.card_fin,
      show Module.finrank ℂ (Matrix (Fin n) (Fin n) ℂ) = n * n from by
        rw [Module.finrank_matrix, Fintype.card_fin, Module.finrank_self, Nat.mul_one]])

-- ============================================================
-- 结构定理表示论层：磁平移商代数 ℂ⟨U,V⟩/(UV−ωVU, Uⁿ−1, Vⁿ−1) ≅ Mₙ(ℂ)
-- ============================================================

/-- 磁平移自由生成元：商代数 ℂ⟨U,V⟩ 的两个生成元（Fin 2 标记）。 -/
private noncomputable def magX (n : ℕ) : FreeAlgebra ℂ (Fin 2) :=
  FreeAlgebra.ι ℂ (0 : Fin 2)

private noncomputable def magY (n : ℕ) : FreeAlgebra ℂ (Fin 2) :=
  FreeAlgebra.ι ℂ (1 : Fin 2)

/-- 磁平移关系：XY ~ ω·YX、Xⁿ ~ 1、Yⁿ ~ 1（Landau 规范磁通对合的生成关系，
    n = 0 时形式退化但类型良定义；全部定理在 NeZero n 下陈述）。 -/
private def magRel (n : ℕ) : FreeAlgebra ℂ (Fin 2) → FreeAlgebra ℂ (Fin 2) → Prop :=
  fun x y => (x = magX n * magY n - (omega n) • (magY n * magX n) ∧ y = 0)
    ∨ (x = magX n ^ n - 1 ∧ y = 0)
    ∨ (x = magY n ^ n - 1 ∧ y = 0)

/-- **磁平移商代数**：ℂ⟨U,V⟩/(UV−ωVU, Uⁿ−1, Vⁿ−1)——磁平移代数的抽象呈现
    （abbrev 以保证 ℂ-代数/环实例在类型类推断下可见）。 -/
abbrev magneticAlgebra (n : ℕ) : Type :=
  RingQuot (magRel n)

/-- 商中的 U：生成元 X 的像。 -/
private noncomputable def magXb (n : ℕ) : magneticAlgebra n :=
  RingQuot.mkAlgHom ℂ (magRel n) (magX n)

/-- 商中的 V：生成元 Y 的像。 -/
private noncomputable def magYb (n : ℕ) : magneticAlgebra n :=
  RingQuot.mkAlgHom ℂ (magRel n) (magY n)

/-- 商中 Weyl 单型元：W_{a,b} = U^a V^b（a, b < n）。 -/
private noncomputable def magWeylElem (n : ℕ) (p : Fin n × Fin n) : magneticAlgebra n :=
  magXb n ^ (p.1 : ℕ) * magYb n ^ (p.2 : ℕ)

/-- 下标模 n 加法：(a, b) ↦ (a % n, b % n)。 -/
private def magAddIdx (n : ℕ) [NeZero n] (a b : ℕ) : Fin n × Fin n :=
  (⟨a % n, Nat.mod_lt _ (NeZero.pos n)⟩, ⟨b % n, Nat.mod_lt _ (NeZero.pos n)⟩)

/-- 商中的 Weyl 关系：U V = ω · V U（由生成关系经泛性质下降，n ≥ 1 全范围
    含 n = 1 退化情形）。 -/
private theorem magWeyl {n : ℕ} [NeZero n] :
    magXb n * magYb n = (omega n) • (magYb n * magXb n) := by
  have h0 : RingQuot.mkAlgHom ℂ (magRel n)
      (magX n * magY n - (omega n) • (magY n * magX n))
      = RingQuot.mkAlgHom ℂ (magRel n) 0 :=
    RingQuot.mkAlgHom_rel ℂ (Or.inl ⟨rfl, rfl⟩)
  rw [Algebra.smul_def] at h0
  rw [map_sub, map_mul, map_mul, map_mul, AlgHom.commutes, ← Algebra.smul_def, map_zero,
    sub_eq_zero] at h0
  exact h0

/-- 商中幂关系：Uⁿ = 1。 -/
private theorem magPowX {n : ℕ} [NeZero n] : magXb n ^ n = 1 := by
  have h0 : RingQuot.mkAlgHom ℂ (magRel n) (magX n ^ n - 1)
      = RingQuot.mkAlgHom ℂ (magRel n) 0 :=
    RingQuot.mkAlgHom_rel ℂ (Or.inr (Or.inl ⟨rfl, rfl⟩))
  rwa [map_sub, map_pow, map_one, map_zero, sub_eq_zero] at h0

/-- 商中幂关系：Vⁿ = 1。 -/
private theorem magPowY {n : ℕ} [NeZero n] : magYb n ^ n = 1 := by
  have h0 : RingQuot.mkAlgHom ℂ (magRel n) (magY n ^ n - 1)
      = RingQuot.mkAlgHom ℂ (magRel n) 0 :=
    RingQuot.mkAlgHom_rel ℂ (Or.inr (Or.inr ⟨rfl, rfl⟩))
  rwa [map_sub, map_pow, map_one, map_zero, sub_eq_zero] at h0

/-- 商中降幂：U^a = U^(a % n)。 -/
private theorem magXpow_mod {n : ℕ} [NeZero n] (a : ℕ) :
    magXb n ^ a = magXb n ^ (a % n) := by
  conv_lhs => rw [← Nat.mod_add_div a n, pow_add, pow_mul]
  rw [magPowX, one_pow, mul_one]

/-- 商中降幂：V^a = V^(a % n)。 -/
private theorem magYpow_mod {n : ℕ} [NeZero n] (a : ℕ) :
    magYb n ^ a = magYb n ^ (a % n) := by
  conv_lhs => rw [← Nat.mod_add_div a n, pow_add, pow_mul]
  rw [magPowY, one_pow, mul_one]

/-- 商中幂次 Weyl 换位（一）：U^a V = ω^a · V U^a（对 a 归纳提升 magWeyl）。 -/
private theorem magXShiftWeyl {n : ℕ} [NeZero n] (a : ℕ) :
    magXb n ^ a * magYb n = (omega n ^ a) • (magYb n * magXb n ^ a) := by
  induction a with
  | zero => simp
  | succ b ih =>
    rw [pow_succ, mul_assoc (magXb n ^ b) (magXb n) (magYb n), magWeyl,
      mul_smul_comm (omega n) (magXb n ^ b) (magYb n * magXb n),
      ← mul_assoc (magXb n ^ b) (magYb n) (magXb n), ih,
      smul_mul_assoc (omega n ^ b) (magYb n * magXb n ^ b) (magXb n),
      smul_smul, mul_assoc (magYb n) (magXb n ^ b) (magXb n), ← pow_succ, ← pow_succ']

/-- 商中幂次 Weyl 换位（二）：U^a V^c = ω^{ac} · V^c U^a（对 c 归纳，用（一））。 -/
private theorem magXpowShiftWeyl {n : ℕ} [NeZero n] (a c : ℕ) :
    magXb n ^ a * magYb n ^ c = (omega n ^ (a * c)) • (magYb n ^ c * magXb n ^ a) := by
  induction c with
  | zero => simp
  | succ b ih =>
    rw [pow_succ, ← mul_assoc (magXb n ^ a) (magYb n ^ b) (magYb n), ih,
      smul_mul_assoc (omega n ^ (a * b)) (magYb n ^ b * magXb n ^ a) (magYb n),
      mul_assoc (magYb n ^ b) (magXb n ^ a) (magYb n), magXShiftWeyl,
      mul_smul_comm (omega n ^ a) (magYb n ^ b) (magYb n * magXb n ^ a),
      ← mul_assoc (magYb n ^ b) (magYb n) (magXb n ^ a), ← pow_succ, smul_smul, ← pow_add,
      show a * b + a = a * (b + 1) from by rw [Nat.mul_succ]]

/-- 商中幂次 Weyl 换位（三）：V^b U^c = ω^{−bc} · U^c V^b（由（二）取逆）。 -/
private theorem magYpowXpow {n : ℕ} [NeZero n] (b c : ℕ) :
    magYb n ^ b * magXb n ^ c
      = ((omega n ^ (b * c) : ℂ))⁻¹ • (magXb n ^ c * magYb n ^ b) := by
  have h := magXpowShiftWeyl (n := n) c b
  rw [Nat.mul_comm] at h
  have hne : (omega n ^ (b * c) : ℂ) ≠ 0 := pow_ne_zero _ (Complex.exp_ne_zero _)
  rw [h, smul_smul, inv_mul_cancel₀ hne, one_smul]

/-- 单型元归一：W_{0,0} = 1。 -/
private theorem magWeylElem_zero {n : ℕ} [NeZero n] :
    magWeylElem n (⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩,
      ⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩) = 1 := by
  show magXb n ^ (((⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩ : Fin n) : ℕ))
    * magYb n ^ (((⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩ : Fin n) : ℕ)) = 1
  rw [show ((⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩ : Fin n) : ℕ) = 0 from rfl, pow_zero,
    pow_zero, one_mul]

/-- 单型元归一：W_{1%n, 0%n} = U（经降幂 1 % n 吸收）。 -/
private theorem magWeylElem_left {n : ℕ} [NeZero n] :
    magWeylElem n (⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩,
      ⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩) = magXb n := by
  show magXb n ^ (((⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ))
    * magYb n ^ (((⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ)) = magXb n
  rw [show ((⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ) = 1 % n from rfl,
    show ((⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ) = 0 % n from rfl,
    ← magXpow_mod 1, Nat.zero_mod, pow_zero, mul_one, pow_one]

/-- 单型元归一：W_{0%n, 1%n} = V。 -/
private theorem magWeylElem_right {n : ℕ} [NeZero n] :
    magWeylElem n (⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩,
      ⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩) = magYb n := by
  show magXb n ^ (((⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ))
    * magYb n ^ (((⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ)) = magYb n
  rw [show ((⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ) = 0 % n from rfl,
    show ((⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩ : Fin n) : ℕ) = 1 % n from rfl,
    Nat.zero_mod, pow_zero, one_mul, ← magYpow_mod 1, pow_one]

/-- 单型张子模：L = span{U^a V^b}_{a,b<n}。 -/
private noncomputable def magL (n : ℕ) [NeZero n] : Submodule ℂ (magneticAlgebra n) :=
  Submodule.span ℂ (Set.range (magWeylElem n))

/-- 1 ∈ L：W_{0,0} 的归属。 -/
private theorem magOne_mem {n : ℕ} [NeZero n] : (1 : magneticAlgebra n) ∈ magL n := by
  have h : magWeylElem n (⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩,
      ⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩) ∈ magL n :=
    Submodule.subset_span ⟨_, rfl⟩
  rwa [magWeylElem_zero] at h

/-- U ∈ L：W_{1%n, 0%n} 的归属。 -/
private theorem magX_mem {n : ℕ} [NeZero n] :
    (RingQuot.mkAlgHom ℂ (magRel n) (FreeAlgebra.ι ℂ (0 : Fin 2))) ∈ magL n := by
  have h : magWeylElem n (⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩,
      ⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩) ∈ magL n :=
    Submodule.subset_span ⟨_, rfl⟩
  rwa [magWeylElem_left] at h

/-- V ∈ L：W_{0%n, 1%n} 的归属。 -/
private theorem magY_mem {n : ℕ} [NeZero n] :
    (RingQuot.mkAlgHom ℂ (magRel n) (FreeAlgebra.ι ℂ (1 : Fin 2))) ∈ magL n := by
  have h : magWeylElem n (⟨0 % n, Nat.mod_lt _ (NeZero.pos n)⟩,
      ⟨1 % n, Nat.mod_lt _ (NeZero.pos n)⟩) ∈ magL n :=
    Submodule.subset_span ⟨_, rfl⟩
  rwa [magWeylElem_right] at h

/-- 单型元乘积封闭：W_p · W_q = ω^{−b c} · W_{(a+c)%n, (b+d)%n}——L 乘法封闭性的
    生成元核心（幂次换位 magYpowXpow + 降幂）。 -/
private theorem magWeylElem_mul {n : ℕ} [NeZero n] (p q : Fin n × Fin n) :
    magWeylElem n p * magWeylElem n q
      = ((omega n ^ ((p.2 : ℕ) * (q.1 : ℕ)) : ℂ))⁻¹
        • magWeylElem n (magAddIdx n ((p.1 : ℕ) + (q.1 : ℕ)) ((p.2 : ℕ) + (q.2 : ℕ))) := by
  have key : magWeylElem n p * magWeylElem n q
      = ((omega n ^ ((p.2 : ℕ) * (q.1 : ℕ)) : ℂ))⁻¹
        • (magXb n ^ ((p.1 : ℕ) + (q.1 : ℕ)) * magYb n ^ ((p.2 : ℕ) + (q.2 : ℕ))) := by
    rw [magWeylElem, magWeylElem,
      mul_assoc (magXb n ^ (p.1 : ℕ)) (magYb n ^ (p.2 : ℕ))
        (magXb n ^ (q.1 : ℕ) * magYb n ^ (q.2 : ℕ)),
      ← mul_assoc (magYb n ^ (p.2 : ℕ)) (magXb n ^ (q.1 : ℕ)) (magYb n ^ (q.2 : ℕ)),
      magYpowXpow,
      smul_mul_assoc ((omega n ^ ((p.2 : ℕ) * (q.1 : ℕ)))⁻¹)
        (magXb n ^ (q.1 : ℕ) * magYb n ^ (p.2 : ℕ)) (magYb n ^ (q.2 : ℕ)),
      mul_smul_comm ((omega n ^ ((p.2 : ℕ) * (q.1 : ℕ)))⁻¹) (magXb n ^ (p.1 : ℕ))
        ((magXb n ^ (q.1 : ℕ) * magYb n ^ (p.2 : ℕ)) * magYb n ^ (q.2 : ℕ)),
      mul_assoc (magXb n ^ (q.1 : ℕ)) (magYb n ^ (p.2 : ℕ)) (magYb n ^ (q.2 : ℕ)),
      ← mul_assoc (magXb n ^ (p.1 : ℕ)) (magXb n ^ (q.1 : ℕ))
        (magYb n ^ (p.2 : ℕ) * magYb n ^ (q.2 : ℕ)),
      ← pow_add, ← pow_add]
  rw [key, magXpow_mod ((p.1 : ℕ) + (q.1 : ℕ)), magYpow_mod ((p.2 : ℕ) + (q.2 : ℕ))]
  exact rfl

/-- L 对乘法封闭（生成元情形由 magWeylElem_mul，双侧 span 归纳）。 -/
private theorem magL_mul_mem {n : ℕ} [NeZero n] {x y : magneticAlgebra n}
    (hx : x ∈ magL n) (hy : y ∈ magL n) : x * y ∈ magL n := by
  refine Submodule.span_induction (p := fun x _ => x * y ∈ magL n) ?_ ?_ ?_ ?_ hx
  · rintro _ ⟨p, rfl⟩
    refine Submodule.span_induction (p := fun z _ => magWeylElem n p * z ∈ magL n)
      ?_ ?_ ?_ ?_ hy
    · rintro _ ⟨q, rfl⟩
      rw [magWeylElem_mul]
      exact Submodule.smul_mem _ _
        (Submodule.subset_span (Set.mem_range_self
          (magAddIdx n ((p.1 : ℕ) + (q.1 : ℕ)) ((p.2 : ℕ) + (q.2 : ℕ)))))
    · simpa using (Submodule.zero_mem (magL n))
    · intro a b _ _ iha ihb
      rw [mul_add]
      exact add_mem iha ihb
    · intro r a _ iha
      rw [mul_smul_comm]
      exact Submodule.smul_mem _ _ iha
  · simpa using (Submodule.zero_mem (magL n))
  · intro a b _ _ iha ihb
    rw [add_mul]
    exact add_mem iha ihb
  · intro r a _ iha
    rw [smul_mul_assoc]
    exact Submodule.smul_mem _ _ iha

/-- **商代数张成定理**：L = ⊤——商中任意元都是 Weyl 单型元的线性组合
    （FreeAlgebra.induction：1/生成元/乘/加四情形，乘法情形由 magL_mul_mem）。 -/
private theorem magAlg_span {n : ℕ} [NeZero n] : magL n = ⊤ := by
  apply eq_top_iff.2
  rintro z -
  obtain ⟨w, rfl⟩ := RingQuot.mkAlgHom_surjective ℂ (magRel n) z
  induction w using FreeAlgebra.induction with
  | grade0 r =>
      rw [AlgHom.commutes, Algebra.algebraMap_eq_smul_one]
      exact Submodule.smul_mem _ _ magOne_mem
  | grade1 i =>
      fin_cases i
      · exact magX_mem
      · exact magY_mem
  | mul a b ha hb =>
      rw [map_mul]
      exact magL_mul_mem ha hb
  | add a b ha hb =>
      rw [map_add]
      exact add_mem ha hb

/-- clock 的幂终结：Uⁿ = diag(ω^{n·i}) = 1。 -/
private theorem clock_pow_one {n : ℕ} [NeZero n] : clock n ^ n = 1 := by
  rw [clock_pow]
  ext i j
  simp only [Matrix.diagonal_apply, Matrix.one_apply]
  by_cases hij : i = j
  · subst hij
    rw [if_pos rfl, if_pos rfl, pow_mul, omega_pow (Nat.one_le_iff_ne_zero.2 (NeZero.ne n)),
      one_pow]
  · rw [if_neg hij, if_neg hij]

/-- shift 的幂终结：Vⁿ = 1（循环移 n 步 = 恒等）。 -/
private theorem shift_pow_one {n : ℕ} [NeZero n] : shift n ^ n = 1 := by
  ext i j
  rw [shift_pow n i j]
  have hof : Fin.ofNat n n = (0 : Fin n) := by
    apply Fin.ext
    show n % n = 0
    exact Nat.mod_self n
  rw [Matrix.one_apply, hof, add_zero]

/-- Mₙ(ℂ) 侧生成元指派：0 ↦ U = clock、1 ↦ V = shift。 -/
private noncomputable def magGen (n : ℕ) [NeZero n] : Fin 2 → Matrix (Fin n) (Fin n) ℂ := fun i =>
  if i = (0 : Fin 2) then clock n else shift n

private theorem magGen_zero (n : ℕ) [NeZero n] : magGen n 0 = clock n := rfl

private theorem magGen_one (n : ℕ) [NeZero n] : magGen n 1 = shift n := rfl

/-- 泛性质提升：自由代数 → Mₙ(ℂ)（生成元按 magGen 指派）。 -/
private noncomputable def magLift (n : ℕ) [NeZero n] :
    FreeAlgebra ℂ (Fin 2) →ₐ[ℂ] Matrix (Fin n) (Fin n) ℂ :=
  FreeAlgebra.lift ℂ (magGen n)

/-- **结构同态**：magneticAlgebra → Mₙ(ℂ)（泛性质下降——三个生成关系分别由
    clock_shift_weyl_gen（n ≥ 1 全范围）与 clock_pow_one / shift_pow_one 保持）。 -/
noncomputable def magHom (n : ℕ) [NeZero n] :
    magneticAlgebra n →ₐ[ℂ] Matrix (Fin n) (Fin n) ℂ :=
  RingQuot.liftAlgHom ℂ ⟨magLift n, fun x y h => by
    rcases h with ⟨hx, hy⟩ | ⟨hx, hy⟩ | ⟨hx, hy⟩
    · subst hx; subst hy
      simp only [Algebra.smul_def, map_sub, map_mul, map_mul, map_zero, magX, magY, magLift,
        FreeAlgebra.lift_ι_apply, magGen_zero, magGen_one, AlgHom.commutes]
      rw [← Algebra.smul_def, clock_shift_weyl_gen, sub_self]
    · subst hx; subst hy
      simp only [map_sub, map_pow, map_one, map_zero, magX, magLift,
        FreeAlgebra.lift_ι_apply, magGen_zero]
      rw [clock_pow_one, sub_self]
    · subst hx; subst hy
      simp only [map_sub, map_pow, map_one, map_zero, magY, magLift,
        FreeAlgebra.lift_ι_apply, magGen_one]
      rw [shift_pow_one, sub_self]⟩

/-- 结构同态的泛性质计算式：magHom (mk w) = lift w。 -/
private theorem magHom_apply {n : ℕ} [NeZero n] (w : FreeAlgebra ℂ (Fin 2)) :
    magHom n (RingQuot.mkAlgHom ℂ (magRel n) w) = magLift n w := by
  rw [magHom]
  exact RingQuot.liftAlgHom_mkAlgHom_apply ℂ _ _ w

/-- 结构同态保 Weyl 单型元：magHom (W_p) = clock^a · shift^b。 -/
private theorem magHom_map_weyl {n : ℕ} [NeZero n] (p : Fin n × Fin n) :
    magHom n (magWeylElem n p) = clock n ^ (p.1 : ℕ) * shift n ^ (p.2 : ℕ) := by
  simp only [magWeylElem, magXb, magYb, magX, magY, map_mul, map_pow, magHom_apply, magLift,
    FreeAlgebra.lift_ι_apply, magGen_zero, magGen_one]

/-- **结构同态满射**：Weyl 基 {clock^a shift^b} ⊆ range ⟹ span = Mₙ(ℂ) ⊆ range
    （weyl_span_top 的直接推论）。 -/
theorem magHom_surjective {n : ℕ} [NeZero n] : Function.Surjective (magHom n) := by
  intro M
  have hM : M ∈ Submodule.span ℂ (Set.range fun p : Fin n × Fin n =>
      clock n ^ (p.1 : ℕ) * shift n ^ (p.2 : ℕ)) := by
    rw [weyl_span_top]; exact Submodule.mem_top
  have hsub : Submodule.span ℂ (Set.range fun p : Fin n × Fin n =>
      clock n ^ (p.1 : ℕ) * shift n ^ (p.2 : ℕ))
      ≤ LinearMap.range (magHom n).toLinearMap := by
    rw [Submodule.span_le]
    rintro _ ⟨p, rfl⟩
    rw [SetLike.mem_coe, LinearMap.mem_range]
    exact ⟨magWeylElem n p, magHom_map_weyl (n := n) p⟩
  have hr : M ∈ LinearMap.range (magHom n).toLinearMap := hsub hM
  rw [LinearMap.mem_range] at hr
  exact hr

/-- 商代数的坐标映射：(Fin n × Fin n → ℂ) →ₗ magneticAlgebra，按 Weyl 基展开。 -/
noncomputable def magBasisMap (n : ℕ) [NeZero n] :
    (Fin n × Fin n → ℂ) →ₗ[ℂ] magneticAlgebra n where
  toFun := fun c => ∑ p, c p • magWeylElem n p
  map_add' := fun c d => by
    simp only [Pi.add_apply, add_smul, Finset.sum_add_distrib]
  map_smul' := fun r c => by
    simp only [Pi.smul_apply, smul_assoc, Finset.smul_sum, RingHom.id_apply]

/-- 单点支撑求和：∑_p (if p = p₀ then r else 0) • W_p = r • W_{p₀}。 -/
private theorem magSum_single {n : ℕ} [NeZero n] (p0 : Fin n × Fin n) (r : ℂ) :
    (∑ p : Fin n × Fin n, (if p = p0 then r else 0) • magWeylElem n p)
      = r • magWeylElem n p0 := by
  have h1 : (∑ p : Fin n × Fin n, (if p = p0 then r else 0) • magWeylElem n p)
      = ∑ p : Fin n × Fin n, (if p = p0 then r • magWeylElem n p else 0) := by
    refine Finset.sum_congr rfl fun p _ => ?_
    by_cases h : p = p0 <;> simp [h]
  rw [h1, Finset.sum_ite_eq', if_pos (Finset.mem_univ _)]

/-- **Weyl 基展开满射**：magBasisMap 满射（商代数张成定理 + 单点支撑坐标）。 -/
theorem magBasisMap_surjective {n : ℕ} [NeZero n] :
    Function.Surjective (magBasisMap n) := by
  intro z
  have hsub : magL n ≤ LinearMap.range (magBasisMap n) := by
    rw [magL, Submodule.span_le]
    rintro _ ⟨p, rfl⟩
    rw [SetLike.mem_coe, LinearMap.mem_range]
    exact ⟨fun q => if q = p then (1 : ℂ) else 0, by
      show (∑ q : Fin n × Fin n, (if q = p then (1 : ℂ) else 0) • magWeylElem n q)
        = magWeylElem n p
      rw [magSum_single, one_smul]⟩
  rw [magAlg_span] at hsub
  have hz : z ∈ LinearMap.range (magBasisMap n) := hsub (Submodule.mem_top)
  rw [LinearMap.mem_range] at hz
  exact hz

/-- 商代数的 ℂ-有限性：Weyl 基展开满射 + 坐标空间有限。 -/
noncomputable instance magFinite {n : ℕ} [NeZero n] :
    Module.Finite ℂ (magneticAlgebra n) :=
  Module.Finite.of_surjective (magBasisMap n) (magBasisMap_surjective (n := n))

/-- finrank 上界：finrank(磁平移商代数) ≤ n²（Weyl 基展开满射）。 -/
private theorem magFinrank_le {n : ℕ} [NeZero n] :
    Module.finrank ℂ (magneticAlgebra n) ≤ n * n := by
  have h := LinearMap.finrank_le_finrank_of_surjective (magBasisMap_surjective (n := n))
  rw [Module.finrank_fintype_fun_eq_card, Fintype.card_prod, Fintype.card_fin] at h
  exact h

/-- **finrank 等维**：finrank(磁平移商代数) = finrank(Mₙ(ℂ)) = n²（双边夹：
    上界 Weyl 基展开满射，下界结构同态满射）。 -/
private theorem magFinrank_eq {n : ℕ} [NeZero n] :
    Module.finrank ℂ (magneticAlgebra n) = Module.finrank ℂ (Matrix (Fin n) (Fin n) ℂ) := by
  have h5 : Module.finrank ℂ (Matrix (Fin n) (Fin n) ℂ) = n * n := by
    rw [Module.finrank_matrix, Fintype.card_fin, Module.finrank_self, Nat.mul_one]
  rw [h5]
  have h3 : n * n ≤ Module.finrank ℂ (magneticAlgebra n) := by
    have h4 : Module.finrank ℂ (Matrix (Fin n) (Fin n) ℂ)
        ≤ Module.finrank ℂ (magneticAlgebra n) :=
      LinearMap.finrank_le_finrank_of_surjective (f := (magHom n).toLinearMap)
        (magHom_surjective (n := n))
    rw [h5] at h4
    exact h4
  exact le_antisymm magFinrank_le h3

/-- **磁平移结构定理（表示论层）**：磁平移商代数 ≅ Mₙ(ℂ)——泛性质下降给出满射
    代数同态 magHom，等维（finrank 双边夹 n²）给出单射，合成 ℂ-代数同构：
    ℂ⟨U,V⟩/(UV−ωVU, Uⁿ−1, Vⁿ−1) 的唯一 n 维不可约表示即 Landau 能级载体
    （结构定理三层：迹 weyl_trace_orth / 向量空间 weyl_span_top / 表示论本定理）。 -/
noncomputable def magAlgEquiv (n : ℕ) [NeZero n] :
    magneticAlgebra n ≃ₐ[ℂ] Matrix (Fin n) (Fin n) ℂ :=
  AlgEquiv.ofBijective (magHom n)
    ⟨(LinearMap.injective_iff_surjective_of_finrank_eq_finrank
        (f := (magHom n).toLinearMap) magFinrank_eq).2 (magHom_surjective (n := n)),
      magHom_surjective (n := n)⟩

/- §末开放登记（不占用 sorry，真证路径）：

  1. **陈数整性与 TKNN**：C = (1/2π)∫F ∈ ℤ 与 σ_xy = (e²/h)C 需环面积分/
     拓扑度/Kubo 线性响应基础设施（BerryChern 已登记）。
  2. **谱投影切向量——约束代数层已闭合，分析构造开放**：约束方程解的代数
     后件已由 BerryChern §2.5 四定理闭合（projTangent_intraBand_zero 带内
     消没 / trace_proj_commutator_interband 带间化简 / berryCurvature_interband
     / trace_proj_commutator_twoCommutator 双交换子形式），本模块
     occupiedProjection_commute 给出 [H,P]=0（Sylvester 方程左端交换性前提）。
     残余开放：A = ∂ₓP、B = ∂ᵧP 的**构造**（投影族参数导数，cfc 对参数可微性/
     Kato 微扰论）属微积分基础设施；当前 occupied_berry_im_eq_zero 以任意
     厄米切向量为假设接入。
  3. **Harper 谱隙**：Hofstadter Butterfly 的谱隙结构（通量 p/q 时 q 能带）
     需具体谱计算，数值层已有载体。
  4. **结构定理表示论层——已闭合**：磁平移商代数 → Mₙ(ℂ) 的 ℂ-代数同构由
     magAlgEquiv 闭合（magHom 泛性质下降满射 + magFinrank_eq 等维单射，
     RingQuot 商 ℂ⟨U,V⟩/(UV−ωVU, Uⁿ−1, Vⁿ−1) ≃ₐ Mₙ(ℂ)）。残余开放：唯一
     不可约表示的 Schur 唯一性（任意 n 维不可约表示等价于标准表示）需
     Burnside/稠密性定理基础设施——本定理已给出"存在唯一 n 维不可约表示
     （即 Landau 能级载体）"的代数同构形态，Schur 唯一性是其推论级强化。

  已闭合（本模块，零 sorry）：Weyl 关系 + clock/shift 幺正性 + Harper Hermitian
  + Hall 生成元链（Fermi 求逆 + 三链会师）+ 占据投影（Hermitian/幂等/[H,P]=0
  交换性）+ Hall-Berry 曲率实值接入 + Weyl 迹正交性（weyl_trace_orth：Weyl 基
  Hilbert-Schmidt 正交）+ Weyl 基定理（weyl_basis_linearIndependent 线性无关
  + weyl_span_top 张成 Mₙ(ℂ)——磁平移代数 ≅ Mₙ(ℂ) 结构定理的向量空间形式）
  + 结构定理表示论层（magAlgEquiv：磁平移商代数 ≃ₐ Mₙ(ℂ)，泛性质下降满射
  + 等维单射——"唯一不可约表示 = Landau 能级载体"的代数同构形态）。
  G1 的三个切入点（GP/BCS/Hall）至此全部闭合。 -/

end MUFPF
