/-
  GNBridgeAudit.lean — R-d：`G_N` ↔ `Δλ_min` 桥的效力判定（系数 = 谱隙平方的倒数 ⟹ 0 比特）
  ==============================================================================

## 接在什么后面

§1 清单里 C1 是唯一还带「[论文]」标记的引力侧约束：

    G_N = 18(2+√3)·(Δλ_min)²/M_Pl²          （paper35 定理 2.1；paper49 §6.1）

§19 判掉「交织 ⟹ 谱相等」这条路（前提比待证项更强）。R-d 判 C1 这条桥本身：
它到不到范畴层？能不能反过来把 `Δλ_min` 定出来？

## 两个因子来自两条不同的链（先承认）

| 因子 | 值 | 来处 |
|:--|:--|:--|
| `c_Planck` | `18(2+√3)` | Cl(1,7) 旋量纤维系数（paper35 / paper49 §6.1） |
| `Δλ_min` | `(√3−1)/6` | SU(2) Casimir 谱 `λ₂−λ₁`（paper20 定理 6.1） |

两者**不是**从同一个公式里拆出来的。所以「乘积 = 1」不是同义反复——
它是两条独立链的数值在 1 处**精确对上**。

## 但正因为它对上了，它就不再是约束

机检三件事：

| 编号 | 命题 | 判什么 |
|:--|:--|:--|
| ① | `18(2+√3) = 1/(Δλ_min)²`（精确相等） | 系数恰是谱隙平方的倒数 —— 两因子互锁 |
| ② | `∀ λ ≠ 0`，`(1/λ²)·λ² = 1` | 一旦系数取成「谱隙平方的倒数」，乘积必为 1（与谱隙具体值无关） |
| ③ | `∀ C > 0`，`∃ λ > 0`，`C·λ² = 1` | `G_N = 1` 只钉住乘积，不钉住 `(C, λ)` 这一对 |

## 判决

**C1 这条桥是 0 比特。**

- 由 ①：`c_Planck` 与 `Δλ_min²` 互为倒数（精确恒等式，不是拟合）。故一旦谱隙由 Casimir 链定住，
  系数就被代数强制为 `1/Δλ_min²`；反过来一旦系数由 Cl(1,7) 定住，谱隙就被强制为
  `√(1/c_Planck)`。「两条链在 1 处对上」这句话**没有自由度可供它失败**。
- 由 ②：把系数写成「谱隙平方的倒数」后，乘积恒为 1——对**任意**非零谱隙成立。
  所以这条公式不是「谱隙取 (√3−1)/6 的物理证据」：换任何 λ，同样的写法照样给 1。
- 由 ③：内部自然单位制下 `G_N·M_Pl² = 1` 是归一化（不是测量），一个归一化只钉乘积，
  钉不住因子。外部 CODATA 反解 `Δλ_min = √(G_N M_Pl²/(18(2+√3)))` 只能把同一个数重算一遍，
  不构成独立检验（无自由参数可被否证）。

## 对主问题的意义

主问题是「能否从物理层逆向推出范畴层」。C1 曾被视为引力侧对谱层的**约束**。
本判定的结论是：C1 只能给出「两个已由其它链确定的数互锁」这一条一致性事实，
不含可供逆向的结构信息。这与 §11（含常数 ⟹ 污染）、§18（钉数值不钉结构）、
§19（谱相等不传递结构）同向：**数值对上不等于结构被推出。**

## 诚实边界

1. 本节**不否认** `18(2+√3) · ((√3−1)/6)² = 1` 是两条独立链的精确会合；它确实是一条
   有价值的自洽性结果。本节的判决只针对它的**约束力/逆向力**，不针对它的真值。
2. ① 的「互锁」是代数事实；把它说成「两条链其实是一条」需要额外论证（本模块不做）。
3. ③ 只证「归一化钉不住因子」，不证「外部 CODATA 数据不支持该框架」——那是 σ_score 口径的事
   （本模块不涉及外部数据）。
4. 本模块不新增常数、不新增公设；全部结论为 `field_simp` / `norm_num` / `nlinarith` 级别，无 `sorry`。
-/

import MUFPFormalization.PlanckSpectralIdentity
import Mathlib.Tactic

namespace MUFPF.GNBridgeAudit

/-- 框架谱隙 `Δλ_min = (√3−1)/6`（SU(2) Casimir 链）。 -/
noncomputable def dlmin : ℝ := (Real.sqrt 3 - 1) / 6

/-- Cl(1,7) 侧系数 `c_Planck = 18(2+√3)`（paper35 定理 2.1 的系数）。 -/
noncomputable def cPlanck : ℝ := 18 * (2 + Real.sqrt 3)

/-- 内部自然单位制下的引力常数（`M_Pl = 1`）：`G_N = c_Planck · Δλ_min²`。 -/
noncomputable def gnInternal : ℝ := cPlanck * dlmin ^ 2

/-- `Δλ_min > 0`。 -/
theorem dlmin_pos : 0 < dlmin := by
  unfold dlmin
  have h1 : (1 : ℝ) < Real.sqrt 3 := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 1)]
    norm_num
  linarith

/-- `Δλ_min² = (2−√3)/18`（与 `MassChain.dlmin_sq_explicit` 同值，本模块独立陈述）。 -/
theorem dlmin_sq_eq : dlmin ^ 2 = (2 - Real.sqrt 3) / 18 := by
  unfold dlmin
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith [hsq]

/-- 框架谱定恒等式：`c_Planck · Δλ_min² = 1`（`MassChain.planck_spectral_identity` 的本模块形式）。 -/
theorem bridge_product_one : cPlanck * dlmin ^ 2 = 1 := by
  simpa [cPlanck, dlmin] using MUFPF.MassChain.planck_spectral_identity

/-- **判①**：系数恰是谱隙平方的倒数——两因子精确互锁。 -/
theorem coefficient_eq_inv_gap_sq : cPlanck = 1 / dlmin ^ 2 := by
  have hne : dlmin ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt dlmin_pos)
  rw [eq_div_iff hne]
  exact bridge_product_one

/-- **判②**：系数取成「谱隙平方的倒数」时，乘积恒为 1——对任意非零谱隙成立，
    与谱隙的具体值无关。故该公式不能作为「谱隙 = (√3−1)/6」的证据。 -/
theorem gn_normalization_lambda_blind (lam : ℝ) (h : lam ≠ 0) :
    (1 / lam ^ 2) * lam ^ 2 = 1 := by
  field_simp

/-- **判③**：`G_N = 1` 只钉住乘积，钉不住 `(c, λ)` 这一对：任何正系数都有对应的谱隙。 -/
theorem gn_one_does_not_pin_gap (C : ℝ) (hC : 0 < C) :
    ∃ lam : ℝ, 0 < lam ∧ C * lam ^ 2 = 1 := by
  refine ⟨Real.sqrt (1 / C), ?_, ?_⟩
  · exact Real.sqrt_pos_of_pos (by positivity)
  · rw [Real.sq_sqrt (by positivity)]
    field_simp

/-- **R-d 判决汇总**：桥成立（`G_N` 内部 = 1），但它是 0 比特的。

    ① 系数 = 谱隙平方的倒数（精确互锁）；
    ② 对任意非零谱隙，「系数取倒数」写法下乘积恒为 1（λ 盲）；
    ③ 反之任何正系数都能配出一个谱隙使乘积为 1（因子不可辨）。 -/
theorem gn_bridge_verdict :
    gnInternal = 1 ∧
    cPlanck = 1 / dlmin ^ 2 ∧
    (∀ lam : ℝ, lam ≠ 0 → (1 / lam ^ 2) * lam ^ 2 = 1) ∧
    (∀ C : ℝ, 0 < C → ∃ lam : ℝ, 0 < lam ∧ C * lam ^ 2 = 1) :=
  ⟨bridge_product_one, coefficient_eq_inv_gap_sq,
   gn_normalization_lambda_blind, gn_one_does_not_pin_gap⟩

end MUFPF.GNBridgeAudit
