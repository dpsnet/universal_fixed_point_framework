-- §26.17 度规项散度的 δ 缩并（(β) 新阶段，2026-09-12）

/-- (0,2)-张量协变差分（(β)-链移位混合约定，与数值链 nabla02 一致）：
    (∇̃_ρ T)_{σν}(x) = ∂̃_ρ T_{σν}
      + Σ_b [Γ^b_{ρσ}(x)T_{bν}(step_ρ x) + Γ^b_{ρν}(x)T_{σb}(step_ρ x)
             − Γ^b_{ρσ}(step_ρ x)T_{bν}(x) − Γ^b_{ρν}(step_ρ x)T_{σb}(x)]。 -/
def covDiff02 (F : FrameRecObj) (Γf : GammaField F)
    (T : F.X.T → Fin 4 → Fin 4 → ℝ) (ρ σ ν : Fin 4) (x : F.X.T) : ℝ :=
  (T (F.stepD ρ x) σ ν - T x σ ν)
  + sum4 (fun b => Γf.γ x b ρ σ * T (F.stepD ρ x) b ν
      + Γf.γ x b ρ ν * T (F.stepD ρ x) σ b
      - Γf.γ (F.stepD ρ x) b ρ σ * T x b ν
      - Γf.γ (F.stepD ρ x) b ρ ν * T x σ b)

/-- **度规项散度的 δ 缩并**：ginv-升指标的度规项散度
    Σ_{μa} ginv^{μa}∇̃_μ(g_{aν}R̂) = ∂̃_νR̂ + 度规相容型修正（5 项显式）。
    ∂̃(gR̂) 移位分裂后，g_{aν}(x)·∂̃_μR̂ 项经 Σ_a ginv^{μa}g_{aν} = δ^μ_ν
    （hctr，无需对称）化为 ∂̃_νR̂；其余为 ginv·∂̃g·R̂ 与 ginv·Γ·g·R̂ 型修正
    （连续极限 O(a) artifact）。数值（phase16b_beta8）：2.8e-14。 -/
theorem metric_term_divergence (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (ν : Fin 4) (x : F.X.T) :
    sum4 (fun μ => sum4 (fun a => ginv x μ a *
        covDiff02 F Γf (fun y c d => g y c d * scalarCurvature F Γf ginv y) μ a ν x))
    = (scalarCurvature F Γf ginv (F.stepD ν x) - scalarCurvature F Γf ginv x)
      + sum4 (fun μ => sum4 (fun a => ginv x μ a *
          ((g (F.stepD μ x) a ν - g x a ν) * scalarCurvature F Γf ginv (F.stepD μ x)
            + sum4 (fun b =>
                Γf.γ x b μ a * g (F.stepD μ x) b ν
                  * scalarCurvature F Γf ginv (F.stepD μ x)
                + Γf.γ x b μ ν * g (F.stepD μ x) a b
                  * scalarCurvature F Γf ginv (F.stepD μ x)
                - Γf.γ (F.stepD μ x) b μ a * g x b ν * scalarCurvature F Γf ginv x
                - Γf.γ (F.stepD μ x) b μ ν * g x a b * scalarCurvature F Γf ginv x)))) := by
  -- 第一步：逐 (μ,a) 分裂 covDiff02 = 修正载体 + g_{aν}(x)·∂̃_μR̂
  have splitTerm : ∀ μ a,
      covDiff02 F Γf (fun y c d => g y c d * scalarCurvature F Γf ginv y) μ a ν x
      = ((g (F.stepD μ x) a ν - g x a ν) * scalarCurvature F Γf ginv (F.stepD μ x)
          + sum4 (fun b =>
              Γf.γ x b μ a * g (F.stepD μ x) b ν
                * scalarCurvature F Γf ginv (F.stepD μ x)
              + Γf.γ x b μ ν * g (F.stepD μ x) a b
                * scalarCurvature F Γf ginv (F.stepD μ x)
              - Γf.γ (F.stepD μ x) b μ a * g x b ν * scalarCurvature F Γf ginv x
              - Γf.γ (F.stepD μ x) b μ ν * g x a b * scalarCurvature F Γf ginv x))
        + g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
            - scalarCurvature F Γf ginv x) := fun μ a => by
    simp only [covDiff02]
    rw [show g (F.stepD μ x) a ν * scalarCurvature F Γf ginv (F.stepD μ x)
          - g x a ν * scalarCurvature F Γf ginv x
        = (g (F.stepD μ x) a ν - g x a ν) * scalarCurvature F Γf ginv (F.stepD μ x)
          + g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
            - scalarCurvature F Γf ginv x) from by ring]
    rw [show sum4 (fun b => Γf.γ x b μ a
            * (g (F.stepD μ x) b ν * scalarCurvature F Γf ginv (F.stepD μ x))
            + Γf.γ x b μ ν
              * (g (F.stepD μ x) a b * scalarCurvature F Γf ginv (F.stepD μ x))
            - Γf.γ (F.stepD μ x) b μ a * (g x b ν * scalarCurvature F Γf ginv x)
            - Γf.γ (F.stepD μ x) b μ ν * (g x a b * scalarCurvature F Γf ginv x))
        = sum4 (fun b =>
            Γf.γ x b μ a * g (F.stepD μ x) b ν
              * scalarCurvature F Γf ginv (F.stepD μ x)
            + Γf.γ x b μ ν * g (F.stepD μ x) a b
              * scalarCurvature F Γf ginv (F.stepD μ x)
            - Γf.γ (F.stepD μ x) b μ a * g x b ν * scalarCurvature F Γf ginv x
            - Γf.γ (F.stepD μ x) b μ ν * g x a b * scalarCurvature F Γf ginv x)
        from by apply sum4_congr; intro b; ring]
    ring
  -- 第二步：求和分配——LHS = S_main + S_delta
  have eLHS : sum4 (fun μ => sum4 (fun a => ginv x μ a *
        covDiff02 F Γf (fun y c d => g y c d * scalarCurvature F Γf ginv y) μ a ν x))
      = sum4 (fun μ => sum4 (fun a => ginv x μ a *
          ((g (F.stepD μ x) a ν - g x a ν) * scalarCurvature F Γf ginv (F.stepD μ x)
            + sum4 (fun b =>
                Γf.γ x b μ a * g (F.stepD μ x) b ν
                  * scalarCurvature F Γf ginv (F.stepD μ x)
                + Γf.γ x b μ ν * g (F.stepD μ x) a b
                  * scalarCurvature F Γf ginv (F.stepD μ x)
                - Γf.γ (F.stepD μ x) b μ a * g x b ν * scalarCurvature F Γf ginv x
                - Γf.γ (F.stepD μ x) b μ ν * g x a b * scalarCurvature F Γf ginv x))))
        + sum4 (fun μ => sum4 (fun a => ginv x μ a *
          (g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
            - scalarCurvature F Γf ginv x)))) := by
    rw [show sum4 (fun μ => sum4 (fun a => ginv x μ a *
          covDiff02 F Γf (fun y c d => g y c d * scalarCurvature F Γf ginv y) μ a ν x))
        = sum4 (fun μ => sum4 (fun a => ginv x μ a *
            (((g (F.stepD μ x) a ν - g x a ν) * scalarCurvature F Γf ginv (F.stepD μ x)
                + sum4 (fun b =>
                    Γf.γ x b μ a * g (F.stepD μ x) b ν
                      * scalarCurvature F Γf ginv (F.stepD μ x)
                    + Γf.γ x b μ ν * g (F.stepD μ x) a b
                      * scalarCurvature F Γf ginv (F.stepD μ x)
                    - Γf.γ (F.stepD μ x) b μ a * g x b ν * scalarCurvature F Γf ginv x
                    - Γf.γ (F.stepD μ x) b μ ν * g x a b * scalarCurvature F Γf ginv x))
              + g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
                - scalarCurvature F Γf ginv x))))
        from by
        apply sum4_congr; intro μ
        apply sum4_congr; intro a
        rw [splitTerm μ a]]
    unfold sum4
    ring
  -- 第三步：δ 缩并 S_delta = ∂̃_νR̂
  have eS2 : sum4 (fun μ => sum4 (fun a => ginv x μ a *
        (g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
          - scalarCurvature F Γf ginv x))))
      = scalarCurvature F Γf ginv (F.stepD ν x) - scalarCurvature F Γf ginv x := by
    have fac : ∀ μ, sum4 (fun a => ginv x μ a *
          (g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
            - scalarCurvature F Γf ginv x)))
        = (sum4 (fun a => ginv x μ a * g x a ν))
          * (scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x) :=
      fun μ => by unfold sum4; ring
    rw [show sum4 (fun μ => sum4 (fun a => ginv x μ a *
          (g x a ν * (scalarCurvature F Γf ginv (F.stepD μ x)
            - scalarCurvature F Γf ginv x))))
        = sum4 (fun μ => (sum4 (fun a => ginv x μ a * g x a ν))
          * (scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x))
        from sum4_congr fac]
    rw [show sum4 (fun μ => (sum4 (fun a => ginv x μ a * g x a ν))
          * (scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x))
        = sum4 (fun μ => (if ν = μ then 1 else 0)
          * (scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x))
        from by
        apply sum4_congr; intro μ
        rw [hctr x μ ν]]
    have flip : sum4 (fun μ => (if ν = μ then 1 else 0)
          * (scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x))
        = sum4 (fun μ => (if μ = ν then 1 else 0)
          * (scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x)) := by
      apply sum4_congr; intro μ
      by_cases h : ν = μ
      · simp [h, eq_comm]
      · simp [h, eq_comm]
    rw [flip, sum4_ite_eq' ν (fun μ =>
      scalarCurvature F Γf ginv (F.stepD μ x) - scalarCurvature F Γf ginv x)]
  rw [eLHS, eS2]
  unfold sum4
  ring
