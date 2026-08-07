import UFPFormalization.RecCategory
import UFPFormalization.DecursionFunctor
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Abel

open CategoryTheory Matrix

namespace UFPFormalization

universe u

/-!
# Higher Rec₂ 2-Category (D28.4 / Phase 29) — 路径 B：D-拉回定义（v0.4，2026-08-04）

数学构造见 `notes/00_foundations/spectral_rec2_exchange_deviation.md` §4.3（定义 8）：

  RecTwoMorphism(f, g) := SpTwoMorphism(Df, Dg)  （Sp₂ 2-态射在谱化函子 D 下的拉回）

即 2-态射 α : f ⇒ g（f,g : X ⟶ Y）由单个 homotopy 矩阵 H ∈ Mat(X.T, Y.T; ℂ) 给出，
满足线性 homotopy 条件：

  transferMatrix g - transferMatrix f = stepMatrix X.step · H - H · stepMatrix Y.step

※ 版本说明（2026-08-04）：
  - v0.3 之前：RecTwoMorphism 采用 ℕ-指标矩阵族 + flow-diagonal 自然性
    α(n+1)[x,g(x)] = α(n)[x,f(x)]，逐点竖/横复合不满足自然性（3 处 sorry）；
    最小修正复合闭合自然性但**不满足结合律**（数值诊断 D7/D8，笔记 §7 开放问题 6）。
  - v0.4：选定路径 B（D-拉回）。homotopy 条件为 H 的**线性方程**，竖复合（homotopy 和）
    与横复合（whiskering）良定义且结合，交换律偏差由 Sp₂ 直接继承
    （镜像 `HigherSpCategory.lean` 已机器证明的 spExchangeLaw_* 定理族）。
  - 原 ℕ-指标 flow-diagonal 结构保留为 homotopy H 的"流分解"分析工具（笔记 §4.1/4.2），
    不进入本文件的复合定义。

**引力根源**：交换律偏差（recExchangeLaw_*）即引力（Paper XXXV §2）；本文件给出
Rec₂ 侧的机器证明形式，与 Sp₂ 侧（spExchangeLaw_*）经 D 相容。
-/

/-- Rec₂ 2-态射（D-拉回）：α : f ⇒ g 由 homotopy 矩阵 + 线性条件给出。 -/
@[ext]
structure RecTwoMorphism {X Y : RecObj} (f g : X ⟶ Y) where
  homotopy : Matrix X.T Y.T ℂ
  condition : transferMatrix g.toFun - transferMatrix f.toFun =
    stepMatrix X.step * homotopy - homotopy * stepMatrix Y.step

/-- 转移矩阵与步进矩阵的交换（RecHom 交织性质的矩阵形式）：
    T_f · A_Y = A_X · T_f（由 f.comm：f ∘ X.step = Y.step ∘ f）。 -/
lemma transferMatrix_step_comm {X Y : RecObj} (f : X ⟶ Y) :
    transferMatrix f.toFun * stepMatrix Y.step =
    stepMatrix X.step * transferMatrix f.toFun := by
  have h1 : transferMatrix (Y.step ∘ f.toFun) =
      transferMatrix f.toFun * stepMatrix Y.step := by
    simpa [stepMatrix] using (transferMatrix_comp (α := X.T) (β := Y.T) (γ := Y.T) f.toFun Y.step)
  have h2 : transferMatrix (f.toFun ∘ X.step) =
      stepMatrix X.step * transferMatrix f.toFun := by
    simpa [stepMatrix] using (transferMatrix_comp (α := X.T) (β := X.T) (γ := Y.T) X.step f.toFun)
  have hf : f.toFun ∘ X.step = Y.step ∘ f.toFun := by
    funext x
    exact f.comm x
  calc
    transferMatrix f.toFun * stepMatrix Y.step = transferMatrix (Y.step ∘ f.toFun) := by
      rw [← h1]
    _ = transferMatrix (f.toFun ∘ X.step) := by
      rw [hf]
    _ = stepMatrix X.step * transferMatrix f.toFun := by
      rw [← h2]

/-- 竖复合：homotopy 相加（条件线性，良定义）。 -/
def recVertComp {X Y : RecObj} {f g h : X ⟶ Y}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h) : RecTwoMorphism f h :=
  { homotopy := α.homotopy + β.homotopy
    condition := by
      suffices transferMatrix h.toFun - transferMatrix f.toFun =
          (stepMatrix X.step * β.homotopy - β.homotopy * stepMatrix Y.step) +
          (stepMatrix X.step * α.homotopy - α.homotopy * stepMatrix Y.step) by
        rw [this]
        ext i j
        simp [Matrix.mul_apply, Matrix.add_apply, Matrix.sub_apply, mul_add, add_mul,
          Finset.sum_add_distrib]
        ring
      rw [show transferMatrix h.toFun - transferMatrix f.toFun =
          (transferMatrix h.toFun - transferMatrix g.toFun) +
          (transferMatrix g.toFun - transferMatrix f.toFun) by
        ext i j
        simp [Matrix.sub_apply, Matrix.add_apply, sub_eq_add_neg, add_comm, add_assoc]]
      rw [β.condition, α.condition] }

/-- 横复合（whiskering）：homotopy := α.h · T_f' + T_g · β.h（良定义）。 -/
def recHorizComp {X Y Z : RecObj} {f g : X ⟶ Y} {f' g' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (α' : RecTwoMorphism f' g') :
    RecTwoMorphism (f ≫ f') (g ≫ g') :=
  { homotopy := α.homotopy * transferMatrix f'.toFun + transferMatrix g.toFun * α'.homotopy
    condition := by
      have hgY : transferMatrix g.toFun * stepMatrix Y.step =
          stepMatrix X.step * transferMatrix g.toFun := transferMatrix_step_comm g
      have hfZ : transferMatrix f'.toFun * stepMatrix Z.step =
          stepMatrix Y.step * transferMatrix f'.toFun := transferMatrix_step_comm f'
      calc
        transferMatrix (g ≫ g').toFun - transferMatrix (f ≫ f').toFun
            = transferMatrix g.toFun * transferMatrix g'.toFun
              - transferMatrix f.toFun * transferMatrix f'.toFun := by
                have hc1 : transferMatrix (g'.toFun ∘ g.toFun) =
                    transferMatrix g.toFun * transferMatrix g'.toFun := by
                  simpa using (transferMatrix_comp (α := X.T) (β := Y.T) (γ := Z.T) g.toFun g'.toFun)
                have hc2 : transferMatrix (f'.toFun ∘ f.toFun) =
                    transferMatrix f.toFun * transferMatrix f'.toFun := by
                  simpa using (transferMatrix_comp (α := X.T) (β := Y.T) (γ := Z.T) f.toFun f'.toFun)
                simp [RecHom.comp_toFun, hc1, hc2]
        _ = transferMatrix g.toFun * (transferMatrix g'.toFun - transferMatrix f'.toFun)
              + (transferMatrix g.toFun - transferMatrix f.toFun) * transferMatrix f'.toFun := by
                ext i j
                simp [Matrix.mul_apply, Matrix.sub_apply, Matrix.add_apply,
                  Finset.sum_add_distrib, Finset.sum_sub_distrib, mul_sub, sub_mul]
        _ = transferMatrix g.toFun * (stepMatrix Y.step * α'.homotopy - α'.homotopy * stepMatrix Z.step)
              + (stepMatrix X.step * α.homotopy - α.homotopy * stepMatrix Y.step) * transferMatrix f'.toFun := by
                rw [α'.condition, α.condition]
        _ = (transferMatrix g.toFun * stepMatrix Y.step * α'.homotopy
              - transferMatrix g.toFun * α'.homotopy * stepMatrix Z.step)
              + (stepMatrix X.step * α.homotopy * transferMatrix f'.toFun
              - α.homotopy * stepMatrix Y.step * transferMatrix f'.toFun) := by
                rw [Matrix.mul_sub, Matrix.sub_mul]
                simp [Matrix.mul_assoc]
        _ = (stepMatrix X.step * transferMatrix g.toFun * α'.homotopy
              - transferMatrix g.toFun * α'.homotopy * stepMatrix Z.step)
              + (stepMatrix X.step * α.homotopy * transferMatrix f'.toFun
              - α.homotopy * transferMatrix f'.toFun * stepMatrix Z.step) := by
                have hterm1 : transferMatrix g.toFun * stepMatrix Y.step * α'.homotopy =
                    stepMatrix X.step * transferMatrix g.toFun * α'.homotopy := by
                  calc
                    transferMatrix g.toFun * stepMatrix Y.step * α'.homotopy =
                        (transferMatrix g.toFun * stepMatrix Y.step) * α'.homotopy := rfl
                    _ = (stepMatrix X.step * transferMatrix g.toFun) * α'.homotopy := by rw [hgY]
                    _ = stepMatrix X.step * transferMatrix g.toFun * α'.homotopy := rfl
                have hterm2 : α.homotopy * stepMatrix Y.step * transferMatrix f'.toFun =
                    α.homotopy * transferMatrix f'.toFun * stepMatrix Z.step := by
                  calc
                    α.homotopy * stepMatrix Y.step * transferMatrix f'.toFun =
                        α.homotopy * (stepMatrix Y.step * transferMatrix f'.toFun) := by
                          simp [Matrix.mul_assoc]
                    _ = α.homotopy * (transferMatrix f'.toFun * stepMatrix Z.step) := by rw [← hfZ]
                    _ = α.homotopy * transferMatrix f'.toFun * stepMatrix Z.step := by
                          simp [Matrix.mul_assoc]
                rw [hterm1, hterm2]
        _ = (stepMatrix X.step * (transferMatrix g.toFun * α'.homotopy)
              - (transferMatrix g.toFun * α'.homotopy) * stepMatrix Z.step)
              + (stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun)
              - (α.homotopy * transferMatrix f'.toFun) * stepMatrix Z.step) := by
                simp [Matrix.mul_assoc]
        _ = stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun
              + transferMatrix g.toFun * α'.homotopy)
              - (α.homotopy * transferMatrix f'.toFun + transferMatrix g.toFun * α'.homotopy)
              * stepMatrix Z.step := by
                calc
                  (stepMatrix X.step * (transferMatrix g.toFun * α'.homotopy)
                      - (transferMatrix g.toFun * α'.homotopy) * stepMatrix Z.step)
                    + (stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun)
                      - (α.homotopy * transferMatrix f'.toFun) * stepMatrix Z.step)
                      = (stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun)
                        + stepMatrix X.step * (transferMatrix g.toFun * α'.homotopy))
                        - ((α.homotopy * transferMatrix f'.toFun) * stepMatrix Z.step
                        + (transferMatrix g.toFun * α'.homotopy) * stepMatrix Z.step) := by
                        calc
                          (stepMatrix X.step * (transferMatrix g.toFun * α'.homotopy)
                              - (transferMatrix g.toFun * α'.homotopy) * stepMatrix Z.step)
                            + (stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun)
                              - (α.homotopy * transferMatrix f'.toFun) * stepMatrix Z.step)
                              = (stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun)
                                + stepMatrix X.step * (transferMatrix g.toFun * α'.homotopy))
                                - ((transferMatrix g.toFun * α'.homotopy) * stepMatrix Z.step
                                + (α.homotopy * transferMatrix f'.toFun) * stepMatrix Z.step) := by
                                rw [← add_sub_add_comm]
                                simp [add_comm, add_left_comm, add_assoc]
                          _ = (stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun)
                                + stepMatrix X.step * (transferMatrix g.toFun * α'.homotopy))
                                - ((α.homotopy * transferMatrix f'.toFun) * stepMatrix Z.step
                                + (transferMatrix g.toFun * α'.homotopy) * stepMatrix Z.step) := by
                                simp [add_comm, add_left_comm, add_assoc]
                  _ = stepMatrix X.step * (α.homotopy * transferMatrix f'.toFun
                        + transferMatrix g.toFun * α'.homotopy)
                        - (α.homotopy * transferMatrix f'.toFun + transferMatrix g.toFun * α'.homotopy)
                        * stepMatrix Z.step := by
                        rw [Matrix.mul_add, ← Matrix.add_mul] }

/-- 恒等 2-态射 id_f : f ⇒ f（零 homotopy）。 -/
def recIdTwoMorphism {X Y : RecObj} (f : X ⟶ Y) : RecTwoMorphism f f :=
  { homotopy := 0
    condition := by simp }

/-- 竖复合结合律。 -/
theorem recVertComp_assoc {X Y : RecObj} {f g h k : X ⟶ Y}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h) (γ : RecTwoMorphism h k) :
    recVertComp (recVertComp α β) γ = recVertComp α (recVertComp β γ) := by
  ext
  simp [recVertComp, add_assoc]

/-- 横复合结合律（whiskering 标准性质，用 transferMatrix_comp 归并）。 -/
theorem recHorizComp_assoc {X Y Z W : RecObj}
    {f g : X ⟶ Y} {f' g' : Y ⟶ Z} {f'' g'' : Z ⟶ W}
    (α : RecTwoMorphism f g) (α' : RecTwoMorphism f' g') (α'' : RecTwoMorphism f'' g'') :
    recHorizComp (recHorizComp α α') α'' = recHorizComp α (recHorizComp α' α'') := by
  apply RecTwoMorphism.ext
  have hgg' : transferMatrix (g'.toFun ∘ g.toFun) =
      transferMatrix g.toFun * transferMatrix g'.toFun := by
    rw [transferMatrix_comp]
  have hff'' : transferMatrix (f''.toFun ∘ f'.toFun) =
      transferMatrix f'.toFun * transferMatrix f''.toFun := by
    rw [transferMatrix_comp]
  dsimp [recHorizComp]
  simp [Matrix.mul_add, Matrix.add_mul, Matrix.mul_assoc, hgg', hff'', add_assoc]

/-! ## 交换律偏差（引力根源，镜像 spExchangeLaw_*）

   严格交换律在弱谱框架中不成立（同 spExchangeLaw）；
   正确形式 = 偏差定理族（偏差 = 转移算子差驱动，严格极限下消失 = G_N → 0）。
   -/

/-- 交换律偏差（homotopy 分量）：
    LHS∘RHS 之差 = (T_h - T_g)·α'.h + β.h·(T_f' - T_g')。 -/
theorem recExchangeLaw_homotopy_deviation {X Y Z : RecObj}
    {f g h : X ⟶ Y} {f' g' h' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h)
    (α' : RecTwoMorphism f' g') (β' : RecTwoMorphism g' h') :
    (recHorizComp (recVertComp α β) (recVertComp α' β')).homotopy -
    (recVertComp (recHorizComp α α') (recHorizComp β β')).homotopy =
    (transferMatrix h.toFun - transferMatrix g.toFun) * α'.homotopy +
      β.homotopy * (transferMatrix f'.toFun - transferMatrix g'.toFun) := by
  calc
    (recHorizComp (recVertComp α β) (recVertComp α' β')).homotopy -
        (recVertComp (recHorizComp α α') (recHorizComp β β')).homotopy
        = ((α.homotopy + β.homotopy) * transferMatrix f'.toFun
            + transferMatrix h.toFun * (α'.homotopy + β'.homotopy)) -
          ((α.homotopy * transferMatrix f'.toFun + transferMatrix g.toFun * α'.homotopy)
            + (β.homotopy * transferMatrix g'.toFun + transferMatrix h.toFun * β'.homotopy)) := by
      simp [recHorizComp, recVertComp]
    _ = (transferMatrix h.toFun - transferMatrix g.toFun) * α'.homotopy +
        β.homotopy * (transferMatrix f'.toFun - transferMatrix g'.toFun) := by
      simp [Matrix.add_mul, Matrix.mul_add, Matrix.sub_mul, Matrix.mul_sub, add_assoc]
      abel

/-- 交换律偏差（转移算子部分对易子形式）：
    Δ = A_X·(β.h·α'.h) − 2·(β.h·(A_Y·α'.h)) + (β.h·α'.h)·A_Z，
    使用 β.condition 与 α'.condition。 -/
theorem recExchangeLaw_partial_commutator {X Y Z : RecObj}
    {f g h : X ⟶ Y} {f' g' h' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h)
    (α' : RecTwoMorphism f' g') (β' : RecTwoMorphism g' h') :
    (recHorizComp (recVertComp α β) (recVertComp α' β')).homotopy -
    (recVertComp (recHorizComp α α') (recHorizComp β β')).homotopy =
    stepMatrix X.step * (β.homotopy * α'.homotopy)
      - 2 • (β.homotopy * (stepMatrix Y.step * α'.homotopy))
      + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
  calc
    (recHorizComp (recVertComp α β) (recVertComp α' β')).homotopy -
        (recVertComp (recHorizComp α α') (recHorizComp β β')).homotopy
        = (transferMatrix h.toFun - transferMatrix g.toFun) * α'.homotopy +
            β.homotopy * (transferMatrix f'.toFun - transferMatrix g'.toFun) :=
          recExchangeLaw_homotopy_deviation α β α' β'
    _ = (stepMatrix X.step * β.homotopy - β.homotopy * stepMatrix Y.step) * α'.homotopy +
        β.homotopy * (-(stepMatrix Y.step * α'.homotopy - α'.homotopy * stepMatrix Z.step)) := by
      rw [β.condition]
      rw [show transferMatrix f'.toFun - transferMatrix g'.toFun =
          -(transferMatrix g'.toFun - transferMatrix f'.toFun) by simp]
      rw [α'.condition]
    _ = stepMatrix X.step * (β.homotopy * α'.homotopy)
        - 2 • (β.homotopy * (stepMatrix Y.step * α'.homotopy))
        + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
      calc
        (stepMatrix X.step * β.homotopy - β.homotopy * stepMatrix Y.step) * α'.homotopy +
            β.homotopy * (-(stepMatrix Y.step * α'.homotopy - α'.homotopy * stepMatrix Z.step))
            = (stepMatrix X.step * β.homotopy * α'.homotopy
                - β.homotopy * stepMatrix Y.step * α'.homotopy) +
              (-(β.homotopy * stepMatrix Y.step * α'.homotopy
                - β.homotopy * α'.homotopy * stepMatrix Z.step)) := by
              simp [Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_assoc]
        _ = stepMatrix X.step * (β.homotopy * α'.homotopy)
            - 2 • (β.homotopy * (stepMatrix Y.step * α'.homotopy))
            + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
              simp [Matrix.mul_assoc]
              abel

/-- 严格极限：homotopy 满足交织（β.h·A_Y = A_X·β.h、A_Y·α'.h = α'.h·A_Z）时
    偏差恒为 0——对应引力解耦 G_N → 0。 -/
theorem recExchangeLaw_strict_limit {X Y Z : RecObj}
    {f g h : X ⟶ Y} {f' g' h' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h)
    (α' : RecTwoMorphism f' g') (β' : RecTwoMorphism g' h')
    (hβ : β.homotopy * stepMatrix Y.step = stepMatrix X.step * β.homotopy)
    (hα' : stepMatrix Y.step * α'.homotopy = α'.homotopy * stepMatrix Z.step) :
    (recHorizComp (recVertComp α β) (recVertComp α' β')).homotopy -
    (recVertComp (recHorizComp α α') (recHorizComp β β')).homotopy = 0 := by
  rw [recExchangeLaw_partial_commutator α β α' β']
  calc
    stepMatrix X.step * (β.homotopy * α'.homotopy)
        - 2 • (β.homotopy * (stepMatrix Y.step * α'.homotopy))
        + (β.homotopy * α'.homotopy) * stepMatrix Z.step
        = stepMatrix X.step * (β.homotopy * α'.homotopy)
          - 2 • ((β.homotopy * stepMatrix Y.step) * α'.homotopy)
          + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
          simp [Matrix.mul_assoc]
    _ = stepMatrix X.step * (β.homotopy * α'.homotopy)
        - 2 • ((stepMatrix X.step * β.homotopy) * α'.homotopy)
        + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
        rw [hβ]
    _ = stepMatrix X.step * (β.homotopy * α'.homotopy)
        - 2 • (stepMatrix X.step * (β.homotopy * α'.homotopy))
        + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
        simp [Matrix.mul_assoc]
    _ = -(stepMatrix X.step * (β.homotopy * α'.homotopy))
        + (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
        abel
    _ = 0 := by
        have hmain : stepMatrix X.step * (β.homotopy * α'.homotopy) =
            (β.homotopy * α'.homotopy) * stepMatrix Z.step := by
          calc
            stepMatrix X.step * (β.homotopy * α'.homotopy)
                = (stepMatrix X.step * β.homotopy) * α'.homotopy := by simp [Matrix.mul_assoc]
            _ = (β.homotopy * stepMatrix Y.step) * α'.homotopy := by rw [← hβ]
            _ = β.homotopy * (stepMatrix Y.step * α'.homotopy) := by simp [Matrix.mul_assoc]
            _ = β.homotopy * (α'.homotopy * stepMatrix Z.step) := by rw [hα']
            _ = (β.homotopy * α'.homotopy) * stepMatrix Z.step := by simp [Matrix.mul_assoc]
        simp [hmain]

end UFPFormalization
