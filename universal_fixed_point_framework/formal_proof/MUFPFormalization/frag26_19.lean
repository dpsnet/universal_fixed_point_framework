-- §26.19 EinsteinDivergenceFree 的最终显式陈述（(β) 新阶段收官，2026-09-12）

/-- **Einstein 协变散度**（场层级，方向指标化）：
    E_ν(x) := Σ_{μa} ginv^{μa}(∇̃_μG)_{aν}(x)，G = Riĉ − ½gR̂。 -/
noncomputable def einsteinDiv (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ) (ν : Fin 4) (x : F.X.T) : ℝ :=
  sum4 (fun μ => sum4 (fun a => ginv x μ a *
    covDiff02 F Γf (fun y c d => einsteinTensor F Γf g ginv c d y) μ a ν x))

/-- **EinsteinDivergenceFree 的最终显式陈述**（Q/T2 抵消形态 + 全曲率原语）：
    E_ν = T1_ν + K_ν − ½(∂̃_νR̂ + 修正_ν)，其中
      T1_ν   = Σ_{μa} ginv^{μa}∂̃_μRiĉ_{aν}（Ricci 方向化散度的 ∂̃ 载体），
      K_ν    = Σ_{μabr} ginv^{μa}[Γ^b_{μa}(x)R̂_{rbrν}(step) + Γ^b_{μν}(x)R̂_{rar b}(step)
               − Γ^b_{μa}(step)R̂_{rbrν}(x) − Γ^b_{μν}(step)R̂_{rar b}(x)]
               （ConnRic 的 K 型四重和，§26.18），
      修正_ν = Σ_{μa} ginv^{μa}(∂̃g_{aν}·R̂(step) + 4 项 Γ·g·R̂ 移位修正)
               （度规项 δ 缩并，§26.17，需 hctr 逆缩并，无需 g 对称）。
    推导：E = Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B（beta7 装配，
    §26.16）代入收缩 Bianchi ginv·(Cc3−K2−K3) = Q − T1 + T2 后 Q、T2 抵消。
    连续极限下修正族 O(a) 消失，退化到经典 ∇^μG_{μν} = 0。
    数值（phase16b_beta9，seed 43）：抵消形态 2.8e-14，全显式形态 3.2e-14。 -/
theorem einstein_divergence_explicit (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (ν : Fin 4) (x : F.X.T) :
    einsteinDiv F Γf g ginv ν x
    = sum4 (fun μ => sum4 (fun a => ginv x μ a *
        (ricciTensor F Γf a ν (F.stepD μ x) - ricciTensor F Γf a ν x)))
      + sum4 (fun μ => sum4 (fun a => ginv x μ a * sum4 (fun b => sum4 (fun r =>
          Γf.γ x b μ a * naiveCurv F Γf (F.stepD μ x) r b r ν
          + Γf.γ x b μ ν * naiveCurv F Γf (F.stepD μ x) r a r b
          - Γf.γ (F.stepD μ x) b μ a * naiveCurv F Γf x r b r ν
          - Γf.γ (F.stepD μ x) b μ ν * naiveCurv F Γf x r a r b))))
      - (1/2:ℝ) * ((scalarCurvature F Γf ginv (F.stepD ν x)
          - scalarCurvature F Γf ginv x)
        + sum4 (fun μ => sum4 (fun a => ginv x μ a *
            ((g (F.stepD μ x) a ν - g x a ν) * scalarCurvature F Γf ginv (F.stepD μ x)
              + sum4 (fun b =>
                  Γf.γ x b μ a * g (F.stepD μ x) b ν
                    * scalarCurvature F Γf ginv (F.stepD μ x)
                  + Γf.γ x b μ ν * g (F.stepD μ x) a b
                    * scalarCurvature F Γf ginv (F.stepD μ x)
                  - Γf.γ (F.stepD μ x) b μ a * g x b ν * scalarCurvature F Γf ginv x
                  - Γf.γ (F.stepD μ x) b μ ν * g x a b * scalarCurvature F Γf ginv x))))) := by
  unfold einsteinDiv
  -- 第一步：逐点线性 covDiff02(G) = covDiff02(Riĉ) − ½ covDiff02(gR̂)，再求和分配
  have e1 : sum4 (fun μ => sum4 (fun a => ginv x μ a *
        covDiff02 F Γf (fun y c d => einsteinTensor F Γf g ginv c d y) μ a ν x))
      = sum4 (fun μ => sum4 (fun a => ginv x μ a *
          covDiff02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x))
        - (1/2:ℝ) * sum4 (fun μ => sum4 (fun a => ginv x μ a *
            covDiff02 F Γf (fun y c d => g y c d * scalarCurvature F Γf ginv y)
              μ a ν x)) := by
    rw [show sum4 (fun μ => sum4 (fun a => ginv x μ a *
          covDiff02 F Γf (fun y c d => einsteinTensor F Γf g ginv c d y) μ a ν x))
        = sum4 (fun μ => sum4 (fun a =>
            ginv x μ a * covDiff02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x
            - (1/2:ℝ) * (ginv x μ a * covDiff02 F Γf
                (fun y c d => g y c d * scalarCurvature F Γf ginv y) μ a ν x)))
        from by
        apply sum4_congr; intro μ
        apply sum4_congr; intro a
        simp only [covDiff02, einsteinTensor]
        unfold sum4
        ring]
    unfold sum4
    ring
  rw [e1]
  -- 第二步：covDiff02(Riĉ) = ∂̃Riĉ + conn02(Riĉ)，求和分配
  have e2 : sum4 (fun μ => sum4 (fun a => ginv x μ a *
        covDiff02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x))
      = sum4 (fun μ => sum4 (fun a => ginv x μ a *
          (ricciTensor F Γf a ν (F.stepD μ x) - ricciTensor F Γf a ν x)))
        + sum4 (fun μ => sum4 (fun a => ginv x μ a *
            conn02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x)) := by
    rw [show sum4 (fun μ => sum4 (fun a => ginv x μ a *
          covDiff02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x))
        = sum4 (fun μ => sum4 (fun a => ginv x μ a *
            ((ricciTensor F Γf a ν (F.stepD μ x) - ricciTensor F Γf a ν x)
              + conn02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x)))
        from by
        apply sum4_congr; intro μ
        apply sum4_congr; intro a
        rfl]
    unfold sum4
    ring
  rw [e2]
  -- 第三步：代入 §26.18（ConnRic 的 K 型展开）与 §26.17（度规项 δ 缩并）
  rw [connric_curvature_expand F Γf g ginv ν x]
  rw [metric_term_divergence F Γf g ginv hctr ν x]
