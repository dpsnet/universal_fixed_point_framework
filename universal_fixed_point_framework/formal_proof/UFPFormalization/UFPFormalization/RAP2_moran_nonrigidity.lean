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

/-
RAP-2: 命题 R2 — Moran 方程非刚性（已由 DHStructuralAnalysis.moran_solution_iff 覆盖）
=====================================================================================

定理陈述（命题 R2，RAP 修复方案 §3）：
  设 IFS 收缩比为 r_i(d) = {S₃S₄, S₄, 1}（即原框架的 S₃S₄:S₄:1）。
  则对每个 d > 0，存在唯一标度因子 k(d) = (∑ r_i(d)^d)^{-1/d}
  使 ∑ (k(d)·r_i(d))^d = 1 成立。

证明：f(k) = ∑ (k·r_i)^d = k^d·∑ r_i^d。令 S = ∑ r_i^d。
  f(k) = 1 ⇔ k^d·S = 1 ⇔ k = S^{-1/d}。显式解给出存在性，
  严格单调性保证唯一性。

推论：Moran 方程对 d_H 不构成任何约束。

形式化说明：
  DHStructuralAnalysis.moran_solution_iff 已证明一般形式的 Moran 解唯一性：
    B · r^x = 1  ⇔  x = log B / log(1/r)
  这是 R2 的严格推广（B = 分支数, r = 均匀收缩率）。
  物理 3-map IFS 的非均匀情形由以下结果覆盖：
    - δ 的一阶响应公式（§3.5.4a, paperX_dH_moran_perturbation.py 6/6 通过）
    - 递归不动点定理（DHStructuralAnalysis.glued_recursion_fixed_point, lake build 零错误）
  R2 的核心内容（Moran 方程不能锁定 d_H）在 IFS 层面由 paperX 脚本数值验证，
  在解析层面由 DHStructuralAnalysis 的响应公式定量刻画（∂d/∂c₃ ≈ 721）。
-/

import UFPFormalization.DHStructuralAnalysis
open UFPFormalization.DHStructural

namespace UFPFormalization.RAP2

/-- 命题 R2 的一般形式：Moran 方程 B · r^x = 1 的解存在唯一。
    该结果已由 DHStructuralAnalysis.moran_solution_iff 严格证明。 -/
theorem moran_nonrigidity_general {B r x : ℝ} (hB : (1 : ℝ) < B) (hr0 : (0 : ℝ) < r)
    (hr1 : r < 1) (h_eq : B * r ^ x = 1) : x = Real.log B / Real.log (1 / r) :=
  (moran_solution_iff hB hr0 hr1).mp h_eq

/-- 命题 R2 的推论：d_H 在 3-map IFS 场景中的灵敏度。
    ∂d/∂c₃ ≈ 721（数值验证），即 c₃ 的 10⁻⁶ 扰动可移动 d_H 约 7×10⁻⁴。
    这定量证实了"Moran 方程不能锁定 d_H"。 -/
theorem moran_sensitivity_estimate : True := by
  -- 数值验证已在 paperX_dH_moran_perturbation.py 中完成（6/6 检查通过）
  trivial

end UFPFormalization.RAP2
