-- ============================================================
-- GPEmergence.lean — G1（GP 切入点）：凝聚态谱生成元的范畴涌现
-- ============================================================

/-
# GPEmergence.lean — G1 部分闭合：A_GP = −log ρ 不再是假设，而是定理

背景：paper14 v1.6 的诚实标注指出全文最高层级为【谱公理】，G1（范畴 Δ
内生资产 → 凝聚态谱生成元的桥）为已登记开放问题。paper5 §5 的模板是
"Rec 子范畴约束 + 边界破缺 → 力生成元涌现"。本模块把同一模板的第一步
对凝聚态谱生成元闭合：**给定凝聚态密度算子 ρ（正谱 Hermitian 算子，
即正谱锥约束——Rec_D 的 Sp 侧对应），其谱生成元 A_GP := −log ρ 由谱构造
定理组给出，且与谱流方程精确相容**。于是 paper14 定理 4.1（GP-谱流等同）
中 "A_GP = −log ρ" 这一公理化输入获得机器证明的推导链：

  ρ（正谱密度算子，正谱锥约束 = Rec_D 的 Sp 侧对应）
    ──specGenerator（谱对数构造）──▶ A_GP
    ──specGenerator_exp──▶  ρ = e^{−A_GP}   （Paper I 谱对应 λ = e^{−μ} 求逆）
    ──specGenerator_charpoly──▶ σ(A_GP) = −log σ(ρ) ⊂ ℝ  （无质量生成元）
    ──specGenerator_flow──▶  ρ(t) = e^{−A_GP(t)} 与 dA/dt=[G,A] 精确相容
    ──trace_pow_mul_commutator_eq_zero（GPFlow）──▶ 全部迹幂守恒

数学内容（全部零 sorry）：
  §1 正谱锥约束 PosSpectrum（Rec_D 的 Sp 侧对应）
  §2 specGenerator：A_GP = −log ρ 的连续函数演算构造（cfc）
  §3 specGenerator_exp：exp(−A_GP) = ρ —— 谱对应求逆
  §4 specGenerator_charpoly：谱映射 σ(A_GP) = −log σ(ρ)
  §5 specGenerator_flow：谱流闭合（GP-谱流等同的代数核心）
  §6 守恒律衔接 + 开放登记（密度算子的 PF 不动点存在性、BCS/Hall 生成元）

说明：本模块只用 mathlib 的 Hermitian 连续函数演算（IsHermitian.cfc，
谱有限故无需连续性条件）+ 矩阵指数引理（exp_conj/exp_neg/exp_diagonal），
不依赖微分方程、场论或同伦基础设施。-/

import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import MUFPFormalization.SpectralDynamics
import MUFPFormalization.GPFlow

namespace MUFPF

variable {n : ℕ}

/-- §1：正谱锥约束——Rec_D（实正谱子范畴）的 Sp 侧对应。凝聚态密度算子 ρ
    的谱全部为正（严格正 ⇔ 未到达相变边界；最小本征值 → 0 即抵达正谱锥边界，
    对应 paper5 §5 的边界破缺图景）。 -/
def PosSpectrum (P : Matrix (Fin n) (Fin n) ℂ) (hP : P.IsHermitian) : Prop :=
  ∀ i, 0 < hP.eigenvalues i

/-- §2：谱生成元构造——A_GP := −log ρ。对正谱 Hermitian 密度算子 ρ，
    经 Hermitian 连续函数演算取 −log（谱有限，任意函数可定义，无需连续性）。 -/
noncomputable def specGenerator (P : Matrix (Fin n) (Fin n) ℂ)
    (hP : P.IsHermitian) : Matrix (Fin n) (Fin n) ℂ :=
  hP.cfc (fun x => -Real.log x)

/-- 负对角阵 = 对角的负（GPEmergence / BCSFermiEmergence 共用）。 -/
theorem diagonal_neg' (f : Fin n → ℂ) :
    -Matrix.diagonal f = Matrix.diagonal (fun i => -f i) := by
  apply Matrix.ext
  intro i j
  simp only [Matrix.neg_apply, Matrix.diagonal_apply]
  split_ifs with h
  · simp [h]
  · rw [neg_zero]

/-- §3：**谱对应求逆（G1 核心定理）**——对正谱 Hermitian 密度算子 ρ，
    exp(−A_GP) = ρ。即 Paper I 谱对应 λ = e^{−μ} 的精确求逆：密度算子由其
    谱生成元的负指数重构。paper14 定理 4.1 的输入 "ρ = e^{−A_GP}" 从假设
    升格为定理。 -/
theorem specGenerator_exp {P : Matrix (Fin n) (Fin n) ℂ}
    (hP : P.IsHermitian) (hpos : PosSpectrum P hP) :
    NormedSpace.exp (-(specGenerator P hP)) = P := by
  classical
  -- 酉对角化构件：U 为特征向量酉阵，hm/hm'/hstar/hunit 为其基本性质
  have hm : (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff.1 hP.eigenvectorUnitary.2
  have hm' : star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff'.1 hP.eigenvectorUnitary.2
  have hstar : star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      = (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)⁻¹ :=
    (Matrix.inv_eq_left_inv hm').symm
  have hunit : IsUnit (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) :=
    Units.isUnit (Units.mk (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      (star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)) hm hm')
  -- cfc 展开：A_GP = U · diag(−log λᵢ) · star U
  have ec : specGenerator P hP
      = (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => (-Real.log (hP.eigenvalues i) : ℂ))
        * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    simp only [specGenerator, Matrix.IsHermitian.cfc, Unitary.conjStarAlgAut_apply]
    congr 1
    congr 1
    apply Matrix.ext
    intro i j
    simp only [Matrix.diagonal_apply]
    split_ifs with h
    · simp [Complex.ofReal_neg]
    · simp
  -- 取负后指数化：exp(−A_GP) = U · exp(diag(log λᵢ)) · star U
  have e1 : NormedSpace.exp (-(specGenerator P hP))
      = (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * NormedSpace.exp (Matrix.diagonal (fun i => (Real.log (hP.eigenvalues i) : ℂ)))
        * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    have hneg : -(specGenerator P hP)
        = (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
          * (-Matrix.diagonal (fun i => (-Real.log (hP.eigenvalues i) : ℂ)))
          * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
      rw [ec, show -((hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
            * Matrix.diagonal (fun i => (-Real.log (hP.eigenvalues i) : ℂ))
            * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ))
          = (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
            * (-Matrix.diagonal (fun i => (-Real.log (hP.eigenvalues i) : ℂ)))
            * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
          from by noncomm_ring]
    rw [hneg, diagonal_neg', hstar, Matrix.exp_conj _ _ hunit]
    -- 对角元逐点恒等：−(−log λ) = log λ，使两侧对角函数语法层合一
    have hf : (fun i => - -((Real.log (hP.eigenvalues i) : ℂ)))
        = (fun i => ((Real.log (hP.eigenvalues i) : ℂ))) := by
      funext i
      simp [neg_neg]
    rw [hf]
  -- 对角元化简：exp(log λᵢ) = λᵢ
  have hexp_i (i : Fin n) :
      NormedSpace.exp ((Real.log (hP.eigenvalues i) : ℂ)) = (hP.eigenvalues i : ℂ) := by
    rw [← Complex.exp_eq_exp_ℂ, ← Complex.ofReal_exp, Real.exp_log (hpos i)]
  have hdiag : NormedSpace.exp (Matrix.diagonal (fun i => (Real.log (hP.eigenvalues i) : ℂ)))
      = Matrix.diagonal (fun i => (hP.eigenvalues i : ℂ)) := by
    rw [Matrix.exp_diagonal]
    congr 1
    funext i
    rw [Pi.coe_exp]
    exact hexp_i i
  rw [e1, hdiag]
  -- 谱定理收束：P = U · diag(λᵢ) · star U
  have e3 : (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * Matrix.diagonal (fun i => (hP.eigenvalues i : ℂ))
      * star (hP.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = P := by
    have hs := hP.spectral_theorem
    rw [Unitary.conjStarAlgAut_apply] at hs
    exact hs.symm
  exact e3

/-- §4：**谱映射定理**——A_GP 的特征多项式为 ∏ᵢ (X − C(−log λᵢ))，
    即 σ(A_GP) = −log σ(ρ)：生成元谱是密度谱的负对数像（无质量：谱为实）。 -/
theorem specGenerator_charpoly {P : Matrix (Fin n) (Fin n) ℂ}
    (hP : P.IsHermitian) :
    (specGenerator P hP).charpoly
      = ∏ i, (Polynomial.X - Polynomial.C ((fun x => -Real.log x) (hP.eigenvalues i) : ℂ)) := by
  unfold specGenerator
  rw [← Matrix.IsHermitian.cfc_eq]
  simpa using hP.charpoly_cfc_eq (fun x => -Real.log x)

/-- §5：**谱流闭合（GP-谱流等同的代数核心）**——生成元沿谱流方程
    dA/dt = [G, A] 演化时，密度恢复精确交换：
    exp(−spectralFlow A_GP G t) = spectralFlow ρ G t。
    即 paper14 定理 4.1 在"密度由生成元负指数重构 + 生成元满足谱流方程"
    层面的精确机器证明版本。 -/
theorem specGenerator_flow {P : Matrix (Fin n) (Fin n) ℂ}
    (hP : P.IsHermitian) (hpos : PosSpectrum P hP)
    (G : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    NormedSpace.exp (-(spectralFlow (specGenerator P hP) G t))
      = spectralFlow P G t := by
  classical
  set E : Matrix (Fin n) (Fin n) ℂ := NormedSpace.exp (t • G) with hE_def
  have hunit : IsUnit E := Matrix.isUnit_exp _
  have h1 : spectralFlow (specGenerator P hP) G t
      = E * specGenerator P hP * E⁻¹ := by
    rw [spectralFlow_satisfies_equation,
      show -t • G = -(t • G) from neg_smul t G, Matrix.exp_neg]
  have h2 : spectralFlow P G t = E * P * E⁻¹ := by
    rw [spectralFlow_satisfies_equation,
      show -t • G = -(t • G) from neg_smul t G, Matrix.exp_neg]
  rw [h1, show -(E * specGenerator P hP * E⁻¹)
      = E * (-(specGenerator P hP)) * E⁻¹ from by noncomm_ring,
    Matrix.exp_conj _ _ hunit, specGenerator_exp hP hpos, h2]

/-- §6：守恒律衔接——A_GP 的全部迹幂 tr(A_GP^k [G, A_GP]) = 0 沿谱流不变
    （GPFlow 谱流守恒核心对涌现生成元的直接实例化，涡旋荷守恒的谱代数根源）。 -/
theorem specGenerator_trace_pow_commutator_eq_zero {P : Matrix (Fin n) (Fin n) ℂ}
    (hP : P.IsHermitian) (G : Matrix (Fin n) (Fin n) ℂ) (k : ℕ) :
    ((specGenerator P hP) ^ k
      * (G * specGenerator P hP - specGenerator P hP * G)).trace = 0 :=
  trace_pow_mul_commutator_eq_zero G (specGenerator P hP) k

/-- §7a：生成元 Hermitian——specGenerator P hP 本身是 Hermitian（cfc 保自伴的
    直接实例；Hall 切入点的 Hall-Berry 接入依赖此包装）。 -/
theorem specGenerator_isHermitian {P : Matrix (Fin n) (Fin n) ℂ}
    (hP : P.IsHermitian) : (specGenerator P hP).IsHermitian :=
  Matrix.isHermitian_iff_isSelfAdjoint.2 (by
    unfold specGenerator
    rw [← Matrix.IsHermitian.cfc_eq]
    exact IsSelfAdjoint.cfc)

/- §7 开放登记（不占用 sorry，真证路径）：

  本模块闭合了 G1 的 GP 切入点：给定密度算子 ρ，其谱生成元的构造、谱对应
  求逆、谱映射、谱流相容与守恒律均为定理。以下完整内容登记为未来工作：

  1. **密度算子的不动点存在性**：ρ 作为 Koopman/转移算子的 Perron–Frobenius
     不动点（ErgodicTheory.lean 已登记）。ρ 的涌现 = Rec 系统在吸引子上的
     不变测度；闭合后 G1 的 GP 链 Δ → … → ρ → A_GP 完全内生。
  2. **正谱锥边界的破缺生成元**：ρ 的最小本征值 → 0（抵达正谱锥边界 ∂，类比
     paper5 定理 5.1 的 ∂Rec_D）时，边界方向导数给出相变处的有效生成元——
     凝聚态版"边界破缺涌现"定理，待微分基础设施。
  3. **BCS/Hall 生成元**：A_SC（配对不动点）、A_Hall（磁平移代数）的同类
     涌现构造。BCS 侧已有 WeaveBCS 数值锚点（r ≈ 0.874）；Hall 侧需磁平移
     投影的有限维代数模型。
  4. **生成元的 Hermitian 性**：（已闭合，specGenerator_isHermitian）
     specGenerator P hP 本身 Hermitian，cfc 保自伴的直接实例。

  已闭合（本模块，零 sorry）：PosSpectrum 约束 + specGenerator 构造 +
  specGenerator_exp（谱对应求逆）+ specGenerator_charpoly（谱映射）+
  specGenerator_flow（谱流闭合）+ 守恒律衔接。-/

end MUFPF
