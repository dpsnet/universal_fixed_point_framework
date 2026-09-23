-- §26.18 ConnRic 的曲率迹展开（(β) 新阶段，2026-09-12）

/-- (0,2)-张量协变差分的联络部分（移位混合约定，无 ∂̃ 项）：
    (conn_ρ T)_{σν}(x) = Σ_b [Γ^b_{ρσ}(x)T_{bν}(step_ρ x) + Γ^b_{ρν}(x)T_{σb}(step_ρ x)
        − Γ^b_{ρσ}(step_ρ x)T_{bν}(x) − Γ^b_{ρν}(step_ρ x)T_{σb}(x)]。
    covDiff02 = ∂̃ + conn02（移位分裂的联络载体）。 -/
def conn02 (F : FrameRecObj) (Γf : GammaField F)
    (T : F.X.T → Fin 4 → Fin 4 → ℝ) (ρ σ ν : Fin 4) (x : F.X.T) : ℝ :=
  sum4 (fun b => Γf.γ x b ρ σ * T (F.stepD ρ x) b ν
      + Γf.γ x b ρ ν * T (F.stepD ρ x) σ b
      - Γf.γ (F.stepD ρ x) b ρ σ * T x b ν
      - Γf.γ (F.stepD ρ x) b ρ ν * T x σ b)

/-- **ConnRic 的曲率迹展开**：ginv-升指标的 Ricci 联络散度
    Σ_{μa} ginv^{μa}(conn_μRiĉ)_{aν} 展开为 ginv·Γ·naiveCurv 四重和（K 型）：
    Σ_{μab r} ginv^{μa}[Γ^b_{μa}(x)R̂_{r b r ν}(step) + Γ^b_{μν}(x)R̂_{r a r b}(step)
        − Γ^b_{μa}(step)R̂_{r b r ν}(x) − Γ^b_{μν}(step)R̂_{r a r b}(x)]。
    纯 ricciTensor 定义展开 + 因子入和，无 ∇̃/∂̃——ConnRic 的可 Lean 化形态，
    EinsteinDivergenceFree 显式陈述的最后一个纯代数构件。
    数值（phase16b_beta8）：2.1e-14。 -/
theorem connric_curvature_expand (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ) (ν : Fin 4) (x : F.X.T) :
    sum4 (fun μ => sum4 (fun a => ginv x μ a *
        conn02 F Γf (fun y c d => ricciTensor F Γf c d y) μ a ν x))
    = sum4 (fun μ => sum4 (fun a => ginv x μ a * sum4 (fun b => sum4 (fun r =>
        Γf.γ x b μ a * naiveCurv F Γf (F.stepD μ x) r b r ν
        + Γf.γ x b μ ν * naiveCurv F Γf (F.stepD μ x) r a r b
        - Γf.γ (F.stepD μ x) b μ a * naiveCurv F Γf x r b r ν
        - Γf.γ (F.stepD μ x) b μ ν * naiveCurv F Γf x r a r b)))) := by
  apply sum4_congr; intro μ
  apply sum4_congr; intro a
  simp only [conn02, ricciTensor]
  congr 1
  apply sum4_congr; intro b
  unfold sum4
  ring
