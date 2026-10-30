import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.Order.Ring.Int

/-!
# S307：模流闭合条件机检（谱点层——'闭合 ⟺ M 谱整数化'）

背景（登记级命题——《模流周期2pi命题化_笔记.md》§3）：
BW 定理 Δ_mod = e^{−2πM}（2310.12185 式 34）使模流 t ↦ Δ^{it} 的
闭合条件为：
  Δ^{i(t+T)} = Δ^{it} ⇔ e^{−2πi·M·T} = 1 ⇔ M·T ∈ ℤ（M 谱以整数为单位）
本文件把该条件在**标量/谱点层**机检（谱点 λ = 谱值、T = 模流周期）：
  ★ 定理 A：e^{−2πi·λ·T} = 1 ⟺ λ·T ∈ ℤ（闭合 ⟺ 谱整数化——同一事实两面）
  ★ 定理 B：谱整数化（λ = n ∈ ℤ）⟹ T = 1 闭合（最小正）
  ★ 定理 C：0 < T < 1 不闭合（谱含 1 时 T=1 为最小正闭合周期）
数值先证伪（模式 8——scripts/s307_modflow_closure.py + s307b）：
  正向（λT∈ℤ ⟹ 闭合）30 组零违例（残差 1e-16 级）；偏离响应线性
  （|e^{−2πi(1+δ)}−1| = 2π|δ|）；扫描闭合仅发生在整数处——全通过。

诚实边界：谱点层机检——算子层（自伴 M 的谱定理提升）为登记级注释；
物理层 M 谱整数化条件的'物理单位'（为什么谱以整数为单位）不在本文件
范围（框架语义——待生成链论证）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.ModFlowClosure

/-- 模流谱点闭合条件（谱值 lam、周期 T）：e^{−2πi·lam·T} = 1。 -/
def modflowClosure (lam T : ℝ) : Prop :=
  Complex.exp (-2 * Real.pi * Complex.I * (lam * T)) = 1

/-- 谱整数化条件：lam·T ∈ ℤ（M 谱以整数为单位——谱点层）。 -/
def spectrumInteger (lam T : ℝ) : Prop :=
  ∃ n : ℤ, lam * T = (n : ℝ)

/-- ★ 定理 A：模流闭合 ⟺ 谱整数化（同一事实两面——谱点层机检）。 -/
theorem modflow_closure_iff_spectrum_integer (lam T : ℝ) :
    modflowClosure lam T ↔ spectrumInteger lam T := by
  constructor
  · intro h
    rcases (Complex.exp_eq_one_iff.mp h) with ⟨n, hn⟩
    -- hn : -2 * Real.pi * Complex.I * (lam * T) = ↑n * (2 * ↑Real.pi * Complex.I)
    have hIm := congrArg Complex.im hn
    -- 化简 hIm 的两边（虚部提取）
    simp [Complex.mul_im, Complex.ofReal_im] at hIm
    -- hIm : -(2 * Real.pi * (lam * T)) = (n : ℝ) * (2 * Real.pi)
    -- 除以 2π（非零）消去：-(lam * T) = n
    have hpi : (2 * Real.pi : ℝ) ≠ 0 := by positivity
    have hIm' : -(lam * T) = (n : ℝ) := by
      field_simp [hpi] at hIm
      -- field_simp 后 hIm 应化简为 -(lam * T) = n；若形式不同则 exact hIm
      simpa using hIm
    -- 目标：∃ m : ℤ, lam * T = m——取 m = -n
    refine ⟨-n, ?_⟩
    -- 从 -(lamT) = n 得 lamT = -n = ↑(-n)
    calc
      lam * T = -(-(lam * T)) := by ring
      _ = -(n : ℝ) := by rw [hIm']
      _ = ↑(-n) := by norm_num
  · intro h
    rcases h with ⟨n, hn⟩
    -- 目标：modflowClosure lam T——展开定义
    change Complex.exp (-2 * Real.pi * Complex.I * (lam * T)) = 1
    -- 合并 coercion：↑lam * ↑T = ↑(lam * T)
    rw [← Complex.ofReal_mul]
    -- lamT = n：重写指数参数
    rw [hn]
    -- 目标：Complex.exp (-2 * Real.pi * Complex.I * (n : ℝ)) = 1
    rw [Complex.exp_eq_one_iff]
    -- 找 m : ℤ 使 -2πi·n = m·2πi——m = -n
    refine ⟨-n, ?_⟩
    -- -2π·I·(n:ℝ) = ↑(-n)·(2·↑π·I)——ℂ 层 ring
    norm_num
    ring

/-- ★ 定理 B：谱整数化（λ = n ∈ ℤ、T = 1）⟹ 闭合——T=1 是闭合周期。 -/
theorem integer_spectrum_period_one : ∀ n : ℤ, modflowClosure (n : ℝ) 1 := by
  intro n
  rw [modflow_closure_iff_spectrum_integer]
  refine ⟨n, ?_⟩
  ring

/-- ★ 定理 C：0 < T < 1 不闭合——谱含 1 时 T=1 为最小正闭合周期。 -/
theorem period_one_minimal : ∀ T : ℝ, 0 < T → T < 1 →
    ¬ modflowClosure 1 T := by
  intro T hT0 hT1 hclosed
  rcases (modflow_closure_iff_spectrum_integer 1 T).mp hclosed with ⟨n, hn⟩
  -- hn : 1 * T = (n : ℝ)——即 T = n
  have hT' : (n : ℝ) = T := by simpa using hn.symm
  have hn0 : (0 : ℝ) < (n : ℝ) := by rwa [hT']
  have hn1 : (n : ℝ) < 1 := by rwa [hT']
  have hn0z : 0 < n := by exact_mod_cast hn0
  have hn1z : n < 1 := by exact_mod_cast hn1
  omega

/-- 推论：T=1 闭合（谱整数化 + λ=1）且 T∈(0,1) 无闭合——最小正性。 -/
theorem period_one_is_minimal_positive :
    modflowClosure 1 1 ∧ ∀ T : ℝ, 0 < T → T < 1 → ¬ modflowClosure 1 T := by
  constructor
  · simpa using integer_spectrum_period_one 1
  · exact period_one_minimal

end MUFPF.ModFlowClosure
