-- §26.14 ginv 升指标的 Leibniz 修正（(β)-4 第二阶段缺口②，2026-09-12）

/-- sum4 逐点同余。 -/
lemma sum4_congr {f h : Fin 4 → ℝ} (he : ∀ i, f i = h i) : sum4 f = sum4 h := by
  simp only [sum4, he 0, he 1, he 2, he 3]

/-- **右 δ-解引理**：若 Σ_j A j·g x j s = B s（∀s），且 g/ginv 对称互逆
    （ginv·g = δ），则 A t = Σ_s B s·ginv x s t——即线性方程 A·g = B 在
    互逆对称下的显式解。证明：δ-插入（A j = Σ_s A j·g j s·ginv s t，
    其中 g·ginv = δ 由 g/ginv 双对称从 hctr 推出）+ sum_comm + 因子化。 -/
lemma solve_right (F : FrameRecObj) (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (A B : Fin 4 → ℝ) (x : F.X.T)
    (hAB : ∀ s, sum4 (fun j => A j * g x j s) = B s) (t : Fin 4) :
    A t = sum4 (fun s => B s * ginv x s t) := by
  have hdelta : ∀ j, sum4 (fun s => g x j s * ginv x s t) = if j = t then 1 else 0 := by
    intro j
    have e : sum4 (fun s => g x j s * ginv x s t)
        = sum4 (fun i => ginv x t i * g x i j) := by
      apply sum4_congr; intro i
      rw [mul_comm, hginv x i t, hg x i j]
    rw [e, hctr x t j]
  calc A t = sum4 (fun j => (if j = t then 1 else 0) * A j) :=
        (sum4_ite_eq' t A).symm
    _ = sum4 (fun j => sum4 (fun s => g x j s * ginv x s t) * A j) := by
        apply sum4_congr; intro j
        rw [hdelta j]
    _ = sum4 (fun s => sum4 (fun j => g x j s * ginv x s t * A j)) := by
        simp only [sum4_eq_finset_sum, Finset.sum_mul]
        rw [Finset.sum_comm (f := fun s j => (g x j s * ginv x s t) * A j)]
    _ = sum4 (fun s => B s * ginv x s t) := by
        apply sum4_congr; intro s
        rw [← hAB s]
        simp only [sum4_eq_finset_sum]
        rw [Finset.sum_mul]
        refine Finset.sum_congr rfl fun j _ => ?_
        ring

/-- **ginv 差分恒等式（左移位变体）**：∂̃_ρ ginv^{μν}(x)
    = −ginv^{μa}(step_ρ x)·∂̃_ρ g_{ab}(x)·ginv^{bν}(x)。
    逐点精确（双 δ + 双对称），连续对应 ∂(g^{-1}) = −g^{-1}∂g g^{-1}。 -/
theorem dginv_left (F : FrameRecObj) (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (ρ μ ν : Fin 4) (x : F.X.T) :
    ginv (F.stepD ρ x) μ ν - ginv x μ ν
    = -sum4 (fun a => sum4 (fun b => ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv x b ν)) := by
  have hAB : ∀ s, sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j) * g x j s)
      = -sum4 (fun a => ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a s - g x a s)) := by
    intro s
    have e1 := hctr (F.stepD ρ x) μ s
    have e2 := hctr x μ s
    have e3 : sum4 (fun j => ginv (F.stepD ρ x) μ j * g x j s)
        = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv (F.stepD ρ x) μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by
      unfold sum4; ring
    calc sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j) * g x j s)
        = sum4 (fun j => ginv (F.stepD ρ x) μ j * g x j s)
          - sum4 (fun j => ginv x μ j * g x j s) := by unfold sum4; ring
      _ = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv (F.stepD ρ x) μ j
            * (g (F.stepD ρ x) j s - g x j s))
          - sum4 (fun j => ginv x μ j * g x j s) := by rw [e3]
      _ = (if s = μ then 1 else 0)
          - sum4 (fun j => ginv (F.stepD ρ x) μ j
            * (g (F.stepD ρ x) j s - g x j s))
          - (if s = μ then 1 else 0) := by rw [e1, e2]
      _ = -sum4 (fun a => ginv (F.stepD ρ x) μ a
            * (g (F.stepD ρ x) a s - g x a s)) := by ring
  have hs := solve_right F g ginv hg hginv hctr
    (fun j => ginv (F.stepD ρ x) μ j - ginv x μ j)
    (fun s => -sum4 (fun a => ginv (F.stepD ρ x) μ a
      * (g (F.stepD ρ x) a s - g x a s)))
    x hAB ν
  rw [hs]
  simp only [sum4_eq_finset_sum]
  have step1 : (∑ i, (-∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν)
      = -∑ i, (∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl; intro i _
    ring
  have step2 : (∑ i, (∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν)
      = ∑ b, ∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv x b ν := by
    have e : (∑ i, (∑ a, ginv (F.stepD ρ x) μ a
          * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν)
        = ∑ i, ∑ a, ginv (F.stepD ρ x) μ a
          * (g (F.stepD ρ x) a i - g x a i) * ginv x i ν := by
      simp only [Finset.sum_mul]
    rw [e, Finset.sum_comm (f := fun i a => ginv (F.stepD ρ x) μ a
      * (g (F.stepD ρ x) a i - g x a i) * ginv x i ν)]
  rw [step1, step2, Finset.sum_comm (f := fun a b => ginv (F.stepD ρ x) μ a
    * (g (F.stepD ρ x) a b - g x a b) * ginv x b ν)]

/-- **ginv 差分恒等式（右移位变体）**：∂̃_ρ ginv^{μν}(x)
    = −ginv^{μa}(x)·∂̃_ρ g_{ab}(x)·ginv^{bν}(step_ρ x)。
    与 dginv_left 对称（在 step_ρ x 点解方程）。 -/
theorem dginv_right (F : FrameRecObj) (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (ρ μ ν : Fin 4) (x : F.X.T) :
    ginv (F.stepD ρ x) μ ν - ginv x μ ν
    = -sum4 (fun a => sum4 (fun b => ginv x μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv (F.stepD ρ x) b ν)) := by
  have hAB : ∀ s, sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j)
        * g (F.stepD ρ x) j s)
      = -sum4 (fun a => ginv x μ a * (g (F.stepD ρ x) a s - g x a s)) := by
    intro s
    have e1 := hctr (F.stepD ρ x) μ s
    have e2 := hctr x μ s
    have e3 : sum4 (fun j => ginv x μ j * g (F.stepD ρ x) j s)
        = sum4 (fun j => ginv x μ j * g x j s)
          + sum4 (fun j => ginv x μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by
      unfold sum4; ring
    calc sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j)
          * g (F.stepD ρ x) j s)
        = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv x μ j * g (F.stepD ρ x) j s) := by
          unfold sum4; ring
      _ = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv x μ j * g x j s)
          - sum4 (fun j => ginv x μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by rw [e3]; ring
      _ = (if s = μ then 1 else 0) - (if s = μ then 1 else 0)
          - sum4 (fun j => ginv x μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by rw [e1, e2]
      _ = -sum4 (fun a => ginv x μ a
            * (g (F.stepD ρ x) a s - g x a s)) := by ring
  have hs := solve_right F g ginv hg hginv hctr
    (fun j => ginv (F.stepD ρ x) μ j - ginv x μ j)
    (fun s => -sum4 (fun a => ginv x μ a
      * (g (F.stepD ρ x) a s - g x a s)))
    (F.stepD ρ x) hAB ν
  rw [hs]
  simp only [sum4_eq_finset_sum]
  have step1 : (∑ i, (-∑ a, ginv x μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν)
      = -∑ i, (∑ a, ginv x μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl; intro i _
    ring
  have step2 : (∑ i, (∑ a, ginv x μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν)
      = ∑ b, ∑ a, ginv x μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv (F.stepD ρ x) b ν := by
    have e : (∑ i, (∑ a, ginv x μ a
          * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν)
        = ∑ i, ∑ a, ginv x μ a
          * (g (F.stepD ρ x) a i - g x a i) * ginv (F.stepD ρ x) i ν := by
      simp only [Finset.sum_mul]
    rw [e, Finset.sum_comm (f := fun i a => ginv x μ a
      * (g (F.stepD ρ x) a i - g x a i) * ginv (F.stepD ρ x) i ν)]
  rw [step1, step2, Finset.sum_comm (f := fun a b => ginv x μ a
    * (g (F.stepD ρ x) a b - g x a b) * ginv (F.stepD ρ x) b ν)]

/-- **离散度规相容恒等式**：∂̃_ρ g_{μν}(x) = g_{μλ}(x)·Γ^λ_{ρν}(x)
    + g_{νλ}(x)·Γ^λ_{ρμ}(x)，对任何满足离散 Christoffel 公式
    Γ^r_{μn} = ½ ginv^{rl}(∂̃_μ g_{ln} + ∂̃_n g_{μl} − ∂̃_l g_{nμ}) 的 Γ
    逐点精确成立。纯 δ-代数（δ 在 x 点 + g/ginv 双对称），无场方程。
    连续对应 ∇_ρ g_{μν} = 0（Levi-Civita 相容性）的差分形态；
    升指标 ∇̃^μ = ginv^{μa}∇̃_a 的 Leibniz 修正由 dginv_left/right 给出。 -/
theorem discrete_metric_compatible (F : FrameRecObj)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (Gam : F.X.T → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (hGam : ∀ x r mu n, Gam x r mu n = (1/2:ℝ) * sum4 (fun l => ginv x r l *
        ((g (F.stepD mu x) l n - g x l n) + (g (F.stepD n x) mu l - g x mu l)
          - (g (F.stepD l x) n mu - g x n mu))))
    (ρ μ ν : Fin 4) (x : F.X.T) :
    g (F.stepD ρ x) μ ν - g x μ ν
    = sum4 (fun la => g x μ la * Gam x la ρ ν)
      + sum4 (fun la => g x ν la * Gam x la ρ μ) := by
  have key0 : ∀ (a : Fin 4) (T : Fin 4 → ℝ),
      sum4 (fun la => g x a la * sum4 (fun l => ginv x la l * T l)) = T a := by
    intro a T
    have hd : ∀ l, (∑ la : Fin 4, g x a la * ginv x la l)
        = if a = l then 1 else 0 := by
      intro l
      have e : (∑ la : Fin 4, g x a la * ginv x la l)
          = ∑ i : Fin 4, ginv x l i * g x i a := by
        apply Finset.sum_congr rfl; intro i _
        rw [mul_comm, hginv x i l, hg x i a]
      rw [e, ← sum4_eq_finset_sum]
      exact hctr x l a
    calc sum4 (fun la => g x a la * sum4 (fun l => ginv x la l * T l))
        = sum4 (fun l => sum4 (fun la => (g x a la * ginv x la l) * T l)) := by
          simp only [sum4_eq_finset_sum]
          rw [show (∑ la, g x a la * ∑ l, ginv x la l * T l)
              = ∑ la, ∑ l, g x a la * (ginv x la l * T l) from by
              refine Finset.sum_congr rfl fun la _ => ?_
              rw [Finset.mul_sum]]
          rw [Finset.sum_comm (f := fun la l => g x a la * (ginv x la l * T l))]
          refine Finset.sum_congr rfl fun l _ => ?_
          refine Finset.sum_congr rfl fun la _ => ?_
          ring
      _ = sum4 (fun l => (if a = l then 1 else 0) * T l) := by
          apply sum4_congr; intro l
          simp only [sum4_eq_finset_sum]
          rw [show (∑ la, g x a la * ginv x la l * T l)
              = (∑ la, g x a la * ginv x la l) * T l
              from (Finset.sum_mul _ _ _).symm, hd l]
      _ = T a := by
          have flip : sum4 (fun l => (if a = l then 1 else 0) * T l)
              = sum4 (fun l => (if l = a then 1 else 0) * T l) := by
            apply sum4_congr; intro l
            by_cases h : a = l
            · simp [h, eq_comm]
            · simp [h, eq_comm]
          rw [flip, sum4_ite_eq' a T]
  have key : ∀ (a : Fin 4) (T : Fin 4 → ℝ),
      sum4 (fun la => g x a la * ((1/2:ℝ) * sum4 (fun l => ginv x la l * T l)))
      = (1/2:ℝ) * T a := by
    intro a T
    have half : sum4 (fun la => g x a la * ((1/2:ℝ) *
          sum4 (fun l => ginv x la l * T l)))
        = (1/2:ℝ) * sum4 (fun la => g x a la * sum4 (fun l => ginv x la l * T l)) := by
      simp only [sum4_eq_finset_sum]
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun la _ => ?_
      ring
    rw [half, key0 a T]
  simp only [hGam]
  rw [key μ (fun l => (g (F.stepD ρ x) l ν - g x l ν)
      + (g (F.stepD ν x) ρ l - g x ρ l) - (g (F.stepD l x) ν ρ - g x ν ρ)),
    key ν (fun l => (g (F.stepD ρ x) l μ - g x l μ)
      + (g (F.stepD μ x) ρ l - g x ρ l) - (g (F.stepD l x) μ ρ - g x μ ρ))]
  rw [hg (F.stepD ρ x) ν μ, hg x ν μ, hg (F.stepD ν x) ρ μ, hg x ρ μ,
    hg (F.stepD μ x) ν ρ, hg x ν ρ]
  ring
