-- §26.15 Einstein 张量构造层（(β)-4 缺口③第一阶段，2026-09-12）

/-- **离散标量曲率**：R̂(p) = ginv^{σν}·Riĉ_{σν}(p)（裸迹 Ricci 的度量缩并）。
    连续对应 R = g^{σν}R_{σν}。 -/
noncomputable def scalarCurvature (F : FrameRecObj) (Γf : GammaField F)
    (ginv : F.X.T → Fin 4 → Fin 4 → ℝ) (p : F.X.T) : ℝ :=
  sum4 (fun σ => sum4 (fun ν => ginv p σ ν * ricciTensor F Γf σ ν p))

/-- **Einstein 张量（场层级）**：G_{μν}(p) = Riĉ_{μν}(p) − ½ g_{μν}(p)R̂(p)。
    裸迹 Ricci 非对称（§26.13），故 G 亦非对称；不对称载体与 Riĉ 相同（PS）。 -/
noncomputable def einsteinTensor (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ) (μ ν : Fin 4) (p : F.X.T) : ℝ :=
  ricciTensor F Γf μ ν p - (1/2:ℝ) * g p μ ν * scalarCurvature F Γf ginv p

/-- **Einstein 迹恒等式**：ginv^{μν}G_{μν} = −R̂（4 维）。
    纯 δ-代数：ginv·Riĉ = R̂（定义）+ ginv^{μν}g_{μν} = 4
    （每 μ：Σ_ν ginv^{μν}g_{νμ} = δ^μ_μ = 1，经 g 对称改写后用 hctr；
    四方向求和得 4）⟹ R̂ − ½·4·R̂ = −R̂。 -/
theorem einstein_trace (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (p : F.X.T) :
    sum4 (fun μ => sum4 (fun ν => ginv p μ ν * einsteinTensor F Γf g ginv μ ν p))
    = -scalarCurvature F Γf ginv p := by
  unfold einsteinTensor
  have e1 : sum4 (fun μ => sum4 (fun ν => ginv p μ ν
        * (ricciTensor F Γf μ ν p
          - (1/2:ℝ) * g p μ ν * scalarCurvature F Γf ginv p)))
      = sum4 (fun μ => sum4 (fun ν => ginv p μ ν * ricciTensor F Γf μ ν p))
        - (1/2:ℝ) * (sum4 (fun μ => sum4 (fun ν => ginv p μ ν * g p μ ν))
          * scalarCurvature F Γf ginv p) := by
    unfold sum4; ring
  rw [e1]
  have e2 : sum4 (fun μ => sum4 (fun ν => ginv p μ ν * g p μ ν)) = 4 := by
    have per : ∀ μ, sum4 (fun ν => ginv p μ ν * g p μ ν) = 1 := fun μ => by
      have h : sum4 (fun ν => ginv p μ ν * g p μ ν)
          = sum4 (fun i => ginv p μ i * g p i μ) := by
        apply sum4_congr; intro ν
        rw [hg p μ ν]
      rw [h, hctr p μ μ]
      simp
    rw [show sum4 (fun μ => sum4 (fun ν => ginv p μ ν * g p μ ν))
        = sum4 (fun μ => (1:ℝ)) from sum4_congr per]
    unfold sum4; ring
  rw [e2]
  show scalarCurvature F Γf ginv p
      - (1/2:ℝ) * ((4:ℝ) * scalarCurvature F Γf ginv p)
    = -scalarCurvature F Γf ginv p
  ring

/-- **Einstein 不对称性 = Ricci 不对称性**：G_{μν} − G_{νμ} = Riĉ_{μν} − Riĉ_{νσ}
    （度量项对称，由 hg 相消）。结合 modified_ricci_symmetry，G 的不对称
    亦由 PS 精确承载。 -/
theorem einstein_asymmetry (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (μ ν : Fin 4) (p : F.X.T) :
    einsteinTensor F Γf g ginv μ ν p - einsteinTensor F Γf g ginv ν μ p
    = ricciTensor F Γf μ ν p - ricciTensor F Γf ν μ p := by
  unfold einsteinTensor
  rw [hg p μ ν]
  ring
