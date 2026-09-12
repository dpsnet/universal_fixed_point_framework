-- ============================================================
-- BCSFermiEmergence.lean — G1（BCS 切入点）：Fermi 密度 → BCS 谱生成元
-- ============================================================

/-
# BCSFermiEmergence.lean — G1 BCS 切入点：A_BCS = log(1+e^{βH}) = −log γ_F

paper5 §5 模板"子范畴约束 → 生成元涌现"的 BCS 实例。GP 侧（GPEmergence.lean）
从凝聚态密度 ρ 构造 A_GP = −log ρ。本模块给出平行的 Fermi 侧构造：对任意
Hermitian BdG Hamiltonian H（**无需任何谱正性条件**），

  γ_F := fermiDensity H hH β = cfc(Fermi 函数) H     —— Fermi 密度算子（正 Hermitian）
  A_BCS := bcsGenerator H hH β = cfc(log(1+e^{β·})) H —— BCS 谱生成元

定理链（全部零 sorry）：
  fermiDensity_isHermitian     γ_F Hermitian（cfc 保自伴）
  bcsGenerator_fermi_inverse   **Fermi 求逆**：exp(−A_BCS) = γ_F
                               （Paper I 谱对应 λ = e^{−μ} 的 Fermi 版求逆）
  bcsGenerator_charpoly        谱映射 σ(A_BCS) = {log(1+e^{βλ}) : λ ∈ σ(H)}
  bcsGenerator_flow            谱流闭合：exp(−spectralFlow A_BCS G t) = spectralFlow γ_F G t
  specGenerator_fermiDensity   **G1 会师定理**：specGenerator γ_F = A_BCS
                               （GP 模板与 Fermi 构造在同一对象上一致——
                                 G1 的 GP 链与 BCS 链在 γ_F 上会合）

数学说明：exp(−log(1+e^{βx})) = (1+e^{βx})⁻¹ 处处成立（1+e^{βx} > 0），
故本链对 H 的谱**无任何限制**（对比 GP 链需正谱约束）——T=0 的奇异极限
（γ 成为投影算子、谱触 0）由 β 有限性自动规避。H 本身（ξ_k、Δ_BCS）仍是
物理输入（结构性边界 §4），但"状态密度 → 谱生成元"的构造是定理而非假设。-/

import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import MUFPFormalization.SpectralDynamics
import MUFPFormalization.GPEmergence

namespace MUFPF

variable {n : ℕ}

/-- Fermi 函数（逆温度 β）：f(x) = (1 + e^{βx})⁻¹，处处连续、处处正。 -/
noncomputable def fermi (β : ℝ) (x : ℝ) : ℝ := (1 + Real.exp (β * x))⁻¹

/-- Fermi 密度算子：γ_F = f(H)，f 为 Fermi 函数。Hermitian、谱为正。 -/
noncomputable def fermiDensity (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) (β : ℝ) : Matrix (Fin n) (Fin n) ℂ :=
  hH.cfc (fermi β)

/-- BCS 谱生成元：A_BCS = L(H)，L(x) = log(1 + e^{βx})（= −log ∘ Fermi）。 -/
noncomputable def bcsGenerator (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) (β : ℝ) : Matrix (Fin n) (Fin n) ℂ :=
  hH.cfc (fun x => Real.log (1 + Real.exp (β * x)))

/-- γ_F 的 Hermitian 性（cfc 保自伴 + 矩阵 cfc 与 generic cfc 一致）。 -/
theorem fermiDensity_isHermitian (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) (β : ℝ) : (fermiDensity H hH β).IsHermitian :=
  Matrix.isHermitian_iff_isSelfAdjoint.2 (by
    unfold fermiDensity
    rw [← Matrix.IsHermitian.cfc_eq]
    exact IsSelfAdjoint.cfc)

/-- §1：**Fermi 求逆（G1-BCS 核心定理）**——exp(−A_BCS) = γ_F。
    Paper I 谱对应 λ = e^{−μ} 的 Fermi 版精确求逆：Fermi 密度算子由其谱
    生成元的负指数重构。对 H 的谱无任何条件（1+e^{βx} > 0 处处成立）。 -/
theorem bcsGenerator_fermi_inverse {H : Matrix (Fin n) (Fin n) ℂ}
    (hH : H.IsHermitian) (β : ℝ) :
    NormedSpace.exp (-(bcsGenerator H hH β)) = fermiDensity H hH β := by
  classical
  have hm : (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff.1 hH.eigenvectorUnitary.2
  have hm' : star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      * (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Matrix.mem_unitaryGroup_iff'.1 hH.eigenvectorUnitary.2
  have hstar : star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)⁻¹ :=
    (Matrix.inv_eq_left_inv hm').symm
  have hunit : IsUnit (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) :=
    Units.isUnit (Units.mk (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
      (star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)) hm hm')
  -- cfc 展开：A_BCS = U · diag(L λᵢ) · star U（L = log(1+e^{β·})）
  have ec : bcsGenerator H hH β
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => (Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    simp only [bcsGenerator, Matrix.IsHermitian.cfc, Unitary.conjStarAlgAut_apply]
    congr 1
  -- 对角元引理：exp(−log(1+e^{βλᵢ})) = (1+e^{βλᵢ})⁻¹ = fermi β λᵢ
  have hexp_i (i : Fin n) :
      NormedSpace.exp
          (-(Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ))
        = (((1 + Real.exp (β * hH.eigenvalues i) : ℝ)⁻¹ : ℂ)) := by
    rw [← Complex.exp_eq_exp_ℂ, ← Complex.ofReal_neg, ← Complex.ofReal_exp,
      Real.exp_neg,
      Real.exp_log (by positivity : (0:ℝ) < 1 + Real.exp (β * hH.eigenvalues i)),
      Complex.ofReal_inv]
  -- 组装：e1 取负形对角（exp(−A_BCS) 的本征值为 e^{−log yᵢ} = yᵢ⁻¹），efd 展开 γ_F
  have e1 : NormedSpace.exp (-(bcsGenerator H hH β))
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * NormedSpace.exp (Matrix.diagonal (fun i =>
            (-(Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ))))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    have hneg : -(bcsGenerator H hH β)
        = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
          * (-Matrix.diagonal (fun i =>
              (Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ)))
          * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
      rw [ec, show -((hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
            * Matrix.diagonal (fun i => (Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ))
            * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ))
          = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
            * (-Matrix.diagonal (fun i => (Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ)))
            * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
          from by noncomm_ring]
    rw [hneg, diagonal_neg', hstar, Matrix.exp_conj _ _ hunit]
  have efd : fermiDensity H hH β
      = (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
        * Matrix.diagonal (fun i => ((fermi β (hH.eigenvalues i)) : ℂ))
        * star (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ) := by
    simp only [fermiDensity, Matrix.IsHermitian.cfc, Unitary.conjStarAlgAut_apply]
    congr 1
  -- 对角元化简：exp(−log(1+e^{βλᵢ})) = (1+e^{βλᵢ})⁻¹ = fermi β λᵢ
  have hdiag : NormedSpace.exp (Matrix.diagonal (fun i =>
        (-(Real.log (1 + Real.exp (β * hH.eigenvalues i)) : ℂ))))
      = Matrix.diagonal (fun i => ((fermi β (hH.eigenvalues i)) : ℂ)) := by
    rw [Matrix.exp_diagonal]
    congr 1
    funext i
    rw [Pi.coe_exp, hexp_i]
    simp only [fermi, Complex.ofReal_inv]
  rw [e1, hdiag, efd]

/-- §2：谱映射——A_BCS 的特征多项式为 ∏ᵢ (X − C(L λᵢ))，
    即 σ(A_BCS) = log(1+e^{β·})(σ(H))。 -/
theorem bcsGenerator_charpoly {H : Matrix (Fin n) (Fin n) ℂ}
    (hH : H.IsHermitian) (β : ℝ) :
    (bcsGenerator H hH β).charpoly
      = ∏ i, (Polynomial.X - Polynomial.C
          ((fun x => Real.log (1 + Real.exp (β * x))) (hH.eigenvalues i) : ℂ)) := by
  unfold bcsGenerator
  rw [← Matrix.IsHermitian.cfc_eq]
  simpa using hH.charpoly_cfc_eq (fun x => Real.log (1 + Real.exp (β * x)))

/-- §3：**谱流闭合**——生成元沿谱流方程演化时 Fermi 求逆精确交换：
    exp(−spectralFlow A_BCS G t) = spectralFlow γ_F G t。 -/
theorem bcsGenerator_flow {H : Matrix (Fin n) (Fin n) ℂ}
    (hH : H.IsHermitian) (β : ℝ) (G : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    NormedSpace.exp (-(spectralFlow (bcsGenerator H hH β) G t))
      = spectralFlow (fermiDensity H hH β) G t := by
  classical
  set E : Matrix (Fin n) (Fin n) ℂ := NormedSpace.exp (t • G) with hE_def
  have hunit : IsUnit E := Matrix.isUnit_exp _
  have h1 : spectralFlow (bcsGenerator H hH β) G t
      = E * bcsGenerator H hH β * E⁻¹ := by
    rw [spectralFlow_satisfies_equation,
      show -t • G = -(t • G) from neg_smul t G, Matrix.exp_neg]
  have h2 : spectralFlow (fermiDensity H hH β) G t
      = E * fermiDensity H hH β * E⁻¹ := by
    rw [spectralFlow_satisfies_equation,
      show -t • G = -(t • G) from neg_smul t G, Matrix.exp_neg]
  rw [h1, show -(E * bcsGenerator H hH β * E⁻¹)
      = E * (-(bcsGenerator H hH β)) * E⁻¹ from by noncomm_ring,
    Matrix.exp_conj _ _ hunit, bcsGenerator_fermi_inverse hH β, h2]

/-- §4：**G1 会师定理**——Fermi 密度算子的谱对数生成元（GP 模板）与
    Fermi 函数演算构造（本模块）是同一对象：
    specGenerator γ_F = A_BCS。
    即 G1 的 GP 链（ρ → −log ρ）与 BCS 链（H → γ_F → −log γ_F）在 Fermi
    密度算子上会合——凝聚态两类生成元构造的统一性机器证明。 -/
theorem specGenerator_fermiDensity (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) (β : ℝ) :
    specGenerator (fermiDensity H hH β) (fermiDensity_isHermitian H hH β)
      = bcsGenerator H hH β := by
  classical
  have hsa : IsSelfAdjoint H := Matrix.isHermitian_iff_isSelfAdjoint.1 hH
  -- cfc 复合的连续性条件：−log 在 Fermi 像集上连续（Fermi 处处非零）
  have hne : ∀ x : ℝ, fermi β x ≠ 0 := fun x =>
    ne_of_gt (inv_pos.2 (by positivity : (0:ℝ) < 1 + Real.exp (β * x)))
  have hcont : Continuous (fermi β) := by
    have h1 : Continuous fun x : ℝ => 1 + Real.exp (β * x) :=
      continuous_const.add (Real.continuous_exp.comp (continuous_const.mul continuous_id'))
    exact h1.inv₀ fun x => ne_of_gt (by positivity : (0:ℝ) < 1 + Real.exp (β * x))
  have hg : ContinuousOn (fun x => -Real.log x) (fermi β '' spectrum ℝ H) := by
    apply ContinuousOn.neg (Real.continuousOn_log.mono _)
    rintro y ⟨x, _hx, rfl⟩
    exact hne x
  have hf : ContinuousOn (fermi β) (spectrum ℝ H) := hcont.continuousOn
  -- 三个 cfc 归一化到 generic cfc 后复合
  have e1 : (fermiDensity_isHermitian H hH β).cfc (fun x => -Real.log x)
      = cfc (fun x => -Real.log x) (fermiDensity H hH β) :=
    (Matrix.IsHermitian.cfc_eq _ _).symm
  have e2 : bcsGenerator H hH β
      = cfc (fun x => Real.log (1 + Real.exp (β * x))) H :=
    (Matrix.IsHermitian.cfc_eq _ _).symm
  rw [specGenerator, e1, e2]
  show cfc (fun x => -Real.log x) (hH.cfc (fermi β))
      = cfc (fun x => Real.log (1 + Real.exp (β * x))) H
  rw [← Matrix.IsHermitian.cfc_eq hH (fermi β),
    ← cfc_comp (g := fun x => -Real.log x) (f := fermi β) (a := H) hsa hg hf]
  -- 逐点：−log((1+e^{βx})⁻¹) = log(1+e^{βx})
  congr 1
  funext x
  simp only [Function.comp_apply, fermi]
  rw [Real.log_inv, neg_neg]

/- §5 开放登记（不占用 sorry，真证路径）：

  1. **PosSpectrum γ_F**：γ_F 的本征值为 Fermi 权重 f(λᵢ) > 0——按
     charpoly_cfc_eq 即得谱级正性；把 PosSpectrum 的 eigenvalues 索引
     与 cfc 特征多项式对齐需谱重排引理（包装工作）。闭合后
     specGenerator_exp/flow 可直接以 γ_F 实例化（当前由
     bcsGenerator_fermi_inverse / bcsGenerator_flow 以无正性条件的
     形式覆盖同一数学内容）。
  2. **T → 0 极限**：β → ∞ 时 γ_F → 谱投影（负能带占据数），−log γ_F →
     βH|_{负能}——奇异极限的算子收敛需泛函分析，登记为远期。
  3. **A_Hall**：磁平移代数投影的有限维模型，同模板待建。

  已闭合（本模块，零 sorry）：fermiDensity 构造与 Hermitian 性 +
  bcsGenerator_fermi_inverse（Fermi 求逆）+ bcsGenerator_charpoly（谱映射）+
  bcsGenerator_flow（谱流闭合）+ specGenerator_fermiDensity（G1 会师）。-/

end MUFPF
