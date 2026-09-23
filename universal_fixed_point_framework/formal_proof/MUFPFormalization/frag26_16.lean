-- §26.16 修正的收缩 Bianchi 恒等式（(β)-4 最后一步，2026-09-12）

/-- **修正的收缩 Bianchi 恒等式**（ginv 缩并 §26.12）：对
    Q_ν := Σ_{sμ} ginv^{sμ}Σ_r(∇̃_r R̂_{μν})^r_s（曲率的 ginv-缩并散度）、
    T1_ν := Σ_{sμ} ginv^{sμ}∂̃_μ Riĉ_{sν}、
    T2_ν := Σ_{sμ} ginv^{sμ}∂̃_ν Riĉ_{sμ}，
    有 Q_ν − T1_ν + T2_ν = Σ_{sμ} ginv^{sμ}(Cc3 − K2 − K3)_{sμν}（逐点，
    无假设——§26.12 点值恒等式的 ginv 加权求和）。连续对应
    g^{sμ}∇^ρR_{ρsμν} = ∇^μRic_{νμ} − ∇_νR 的缩并第二 Bianchi。
    数值端到端装配（phase16b_beta7）：连同 ∇̃^μRiĉ = T1 + ConnRic 与
    ∇̃^μG_{μν} = ∇̃^μRiĉ_{μν} − ½ ginv^{μa}∇̃_μ(g_{aν}R̂) 得
    E_ν = Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B（max 残差 2.8e-14）。 -/
theorem contracted_riemann_divergence (F : FrameRecObj) (Γf : GammaField F)
    (ginv : F.X.T → Fin 4 → Fin 4 → ℝ) (μ ν : Fin 4) (x : F.X.T) :
    sum4 (fun s => sum4 (fun μ' => ginv x s μ' *
      (sum4 (fun r => naiveNablaCurv F Γf r μ ν x r s)
        - (ricciTensor F Γf s ν (F.stepD μ x) - ricciTensor F Γf s ν x)
        + (ricciTensor F Γf s μ (F.stepD ν x) - ricciTensor F Γf s μ x))))
    = sum4 (fun s => sum4 (fun μ' => ginv x s μ' *
      (contractCorr F Γf μ ν x s - contractConn2 F Γf μ ν x s
        - contractConn3 F Γf μ ν x s))) := by
  have h := discrete_riemann_divergence F Γf μ ν x
  apply sum4_congr; intro s
  apply sum4_congr; intro μ'
  rw [h s]

/-- **标量曲率移位 Leibniz**：ginv-缩并的 ∂̃_ν 展开
    Σ_{sμ} ginv^{sμ}∂̃_νRiĉ_{sμ} = ∂̃_νR̂ − Σ_{sμ}∂̃_νginv^{sμ}·Riĉ_{sμ}(step_ν)——
    标量场 R̂ = ginv·Riĉ 的移位积规则（∂̃(AB)=∂̃A·B(step)+A·∂̃B 的缩并形态），
    纯代数（sum4 展开 + ring），无假设。配合 §26.14 dginv_left/right
    得 ∂̃ginv 的显式曲率项。 -/
theorem scalar_curvature_leibniz (F : FrameRecObj) (Γf : GammaField F)
    (ginv : F.X.T → Fin 4 → Fin 4 → ℝ) (ν : Fin 4) (x : F.X.T) :
    sum4 (fun s => sum4 (fun μ' => ginv x s μ'
      * (ricciTensor F Γf s μ' (F.stepD ν x) - ricciTensor F Γf s μ' x)))
    = scalarCurvature F Γf ginv (F.stepD ν x) - scalarCurvature F Γf ginv x
      - sum4 (fun s => sum4 (fun μ' => (ginv (F.stepD ν x) s μ' - ginv x s μ')
        * ricciTensor F Γf s μ' (F.stepD ν x))) := by
  unfold scalarCurvature
  unfold sum4
  ring
