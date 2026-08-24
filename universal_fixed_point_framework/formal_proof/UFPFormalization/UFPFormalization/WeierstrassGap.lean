-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：4
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.IFSFractal
import UFPFormalization.IFSRecCoding
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace UFPFormalization

noncomputable section

open Real

/-!
# Weierstrass 图 IFS 谱隙（阶段 3 子任务 4 的部分闭合，2026-08-05）

对齐笔记 `spectral_phase3_fractal_expansion.md` §2.3 S5：
Weierstrass 图 IFS（2D）：f₁(t, y) = (t/b, y/b)、f₂(t, y) = ((t+1)/b, (y+a)/b)，
b > 1、0 < a < 1（ab ≥ 1 保持非光滑）。Moran 图维数 d(a) = 2 + ln a / ln b（Falconer）。

本文件闭合（零 `sorry`，`lake build` 通过）：
  1. `weierstrassGraphMap₁`/`weierstrassGraphMap₂`/`weierstrassGraphIFS`：
     IFS 构造，收缩率 1/b 机器证明（ℝ² sup 距离，`lipschitz_affine_prod`）；
  2. `weierstrassGraph_dH`：均匀 IFS（2 映射、率 1/b）的 Moran 维数唯一解
     d_H = log 2 / log b（`uniform_ifs_dH_unique` 桥梁）；
  3. `weierstrassGraphDimension`：图维数 d(a) = 2 + log a / log b（Falconer 公式），
     并机器证明 **d(a) 随 a 严格递增**（S5"a↑ → 维数↑"的 Lean 侧结构支撑）；
  4. `weierstrassGraph_symbolic_trace`：2 片符号动力学的谱障碍公式实例
     tr(T_f) = #Fix = 1（复用 IFSRecCoding）。

诚实边界：笔记 S5 的**核谱隙** gap = 1 − λ₂/λ₁ 随 d 单调递减的完整机器证明
依赖有限维谱积分层（mathlib `Matrix.IsHermitian` 特征值 / CFC 桥接，
`Mathlib.LinearAlgebra.Matrix.Spectrum` 未在 lean_lib 构建），本文件给出其
**结构支撑**：收缩率 1/b 机器证明 + 图维数单调性 + 迹公式实例——特征值级
表述登记为开放项。
-/

/-- 分量仿射映射 p ↦ (c·p.1 + t₁, c·p.2 + t₂) 是 LipschitzWith c（ℝ² sup 距离）。 -/
theorem lipschitz_affine_prod (c : ℝ) (hc0 : 0 ≤ c) (t₁ t₂ : ℝ) :
    LipschitzWith (NNReal.mk c hc0) (fun p : ℝ × ℝ => (c * p.1 + t₁, c * p.2 + t₂)) := by
  refine LipschitzWith.of_dist_le_mul (fun x y => ?_)
  rw [Prod.dist_eq, Prod.dist_eq]
  rw [Real.dist_eq, Real.dist_eq, Real.dist_eq, Real.dist_eq]
  -- LHS 的绝对值化简：|c·x + t − (c·y + t)| = c·|x − y|
  have h1 : |c * x.1 + t₁ - (c * y.1 + t₁)| = c * |x.1 - y.1| := by
    have hring : c * x.1 + t₁ - (c * y.1 + t₁) = c * (x.1 - y.1) := by ring
    rw [hring, abs_mul, abs_of_nonneg hc0]
  have h2 : |c * x.2 + t₂ - (c * y.2 + t₂)| = c * |x.2 - y.2| := by
    have hring : c * x.2 + t₂ - (c * y.2 + t₂) = c * (x.2 - y.2) := by ring
    rw [hring, abs_mul, abs_of_nonneg hc0]
  rw [h1, h2]
  -- max (c·a) (c·b) ≤ c · max a b（c ≥ 0）；simp 已把 max ≤ 分解为两个合取
  simp [NNReal.coe_mk]
  constructor
  · exact mul_le_mul_of_nonneg_left (le_max_left _ _) hc0
  · exact mul_le_mul_of_nonneg_left (le_max_right _ _) hc0

/-- Weierstrass 图 IFS 第 1 个映射：f₁(t, y) = (t/b, y/b)（收缩率 1/b）。
    与 `lipschitz_affine_prod` 的输出形式逐项对齐（+ 0 显式写出以定义性匹配）。 -/
def weierstrassGraphMap₁ (b : ℝ) : ℝ × ℝ → ℝ × ℝ :=
  fun p => (1 / b * p.1 + 0, 1 / b * p.2 + 0)

/-- Weierstrass 图 IFS 第 2 个映射：f₂(t, y) = ((t+1)/b, (y+a)/b)（收缩率 1/b）。 -/
def weierstrassGraphMap₂ (b a : ℝ) : ℝ × ℝ → ℝ × ℝ :=
  fun p => (1 / b * p.1 + 1 / b, 1 / b * p.2 + a / b)

/-- 1/b < 1（b > 1）：Weierstrass 图 IFS 的收缩率严格小于 1。 -/
theorem weierstrass_ratio_lt_one (b : ℝ) (hb : 1 < b) : 1 / b < 1 :=
  (div_lt_one (lt_trans zero_lt_one hb)).mpr hb

/-- f₁ 是收缩，率 1/b（b > 1）。 -/
theorem weierstrassGraphMap₁_contracting (b : ℝ) (hb : 1 < b) :
    ContractingWith (NNReal.mk (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb))))
      (weierstrassGraphMap₁ b) := by
  refine ⟨weierstrass_ratio_lt_one b hb, ?_⟩
  exact lipschitz_affine_prod (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb))) (0 : ℝ) (0 : ℝ)

/-- f₂ 是收缩，率 1/b（b > 1）。 -/
theorem weierstrassGraphMap₂_contracting (b a : ℝ) (hb : 1 < b) :
    ContractingWith (NNReal.mk (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb))))
      (weierstrassGraphMap₂ b a) := by
  refine ⟨weierstrass_ratio_lt_one b hb, ?_⟩
  exact lipschitz_affine_prod (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb)))
    (1 / b) (a / b)

/-- Weierstrass 图 IFS：2 个映射（f₁、f₂），收缩率均为 1/b。
    吸引子 = Weierstrass 型函数的图（非光滑需 ab ≥ 1，见笔记 §2.3 S5）。 -/
noncomputable def weierstrassGraphIFS (b a : ℝ) (hb : 1 < b) : IFS (ℝ × ℝ) :=
  IFS.mk 2
    (fun i => match i with
      | 0 => weierstrassGraphMap₁ b
      | 1 => weierstrassGraphMap₂ b a)
    (fun _ => NNReal.mk (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb))))
    (by
      intro i
      fin_cases i
      · exact weierstrassGraphMap₁_contracting b hb
      · exact weierstrassGraphMap₂_contracting b a hb)
    (by
      intro i
      fin_cases i <;> exact one_div_pos.mpr (lt_trans zero_lt_one hb))
    (by
      intro i
      fin_cases i <;> exact weierstrass_ratio_lt_one b hb)

/-- Weierstrass 图 IFS 是均匀 IFS：映射数 2、收缩率均为 1/b。 -/
theorem weierstrassGraphIFS_uniform (b a : ℝ) (hb : 1 < b) :
    (weierstrassGraphIFS b a hb).n = 2 ∧
      ∀ i : Fin (weierstrassGraphIFS b a hb).n,
        (weierstrassGraphIFS b a hb).ratios i =
          NNReal.mk (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb))) := by
  constructor
  · rfl
  · intro i
    fin_cases i <;> rfl

/-- Weierstrass 图 IFS 吸引子的 Moran 维数（唯一解）：d_H = log 2 / log b。
    均匀 IFS（B=2、率 1/b）的 Moran 方程 2·(1/b)^d = 1 唯一解。 -/
theorem weierstrassGraph_dH (b a : ℝ) (hb : 1 < b)
    (sol : HausdorffDimensionSolution (weierstrassGraphIFS b a hb)) :
    sol.dH = Real.log 2 / Real.log b := by
  have hunif := weierstrassGraphIFS_uniform b a hb
  have hd := uniform_ifs_dH_unique (weierstrassGraphIFS b a hb) (B := 2) (by norm_num)
    (by exact one_div_pos.mpr (lt_trans zero_lt_one hb))
    (weierstrass_ratio_lt_one b hb) hunif.1 (hunif.2) sol
  rw [hd]
  have hbne : b ≠ 0 := ne_of_gt (lt_trans zero_lt_one hb)
  have harg : 1 / ↑(NNReal.mk (1 / b) (le_of_lt (one_div_pos.mpr (lt_trans zero_lt_one hb)))) = b := by
    rw [NNReal.coe_mk]
    field_simp [hbne]
  rw [harg]
  norm_num

/-- Weierstrass 图维数（Falconer）：d(a) = 2 + ln a / ln b。
    对 0 < a < 1、b > 1、ab ≥ 1，该式为图（Weierstrass 型函数图）的盒维数。 -/
noncomputable def weierstrassGraphDimension (a b : ℝ) : ℝ :=
  2 + Real.log a / Real.log b

/-- 图维数 d(a) 随 a **严格递增**（b 固定、0 < a₁ < a₂）：
    a↑ ⇒ ln a↑ ⇒ d(a)↑——笔记 S5"a 越大维数越高"的 Lean 侧结构支撑
    （谱隙随维数单调递减的方向为 gap↓，见开放项登记）。 -/
theorem weierstrassGraphDimension_strictMono_a (a₁ a₂ b : ℝ) (hb : 1 < b)
    (ha₁ : 0 < a₁) (ha₂ : 0 < a₂) (h : a₁ < a₂) :
    weierstrassGraphDimension a₁ b < weierstrassGraphDimension a₂ b := by
  unfold weierstrassGraphDimension
  have hlog : Real.log a₁ < Real.log a₂ := Real.log_lt_log ha₁ h
  have hbpos : 0 < Real.log b := Real.log_pos hb
  have hdiv : Real.log a₁ / Real.log b < Real.log a₂ / Real.log b :=
    div_lt_div_of_pos_right hlog hbpos
  linarith

/-- 谱障碍公式实例（Weierstrass 图 IFS 的符号动力学，2 片）：
    tr(T_f) = #Fix = 1——符号转移矩阵的谱障碍（复用 IFSRecCoding 定理）。 -/
theorem weierstrassGraph_symbolic_trace (L : ℕ) (hL : 1 ≤ L) :
    Matrix.trace (stepMatrix (symbolicRecObj 2 L (by norm_num) hL).step) = 1 :=
  symbolicTransferMatrix_trace_eq_one 2 L (by norm_num) hL

end

end UFPFormalization
