/-
  AlphaCrisisAudit.lean — R-e：α⁻¹ 危机的两条口径判决（旧机制式不达标 / S320 达标但装配盲）
  ====================================================================================

## 接在什么后面

§11、§18、§19、§20 四条机检各自判掉一种「从物理层逆向推出结构」的路。R-e 判清单里
最后一处真断裂：**α⁻¹ 危机**。它现在有两种口径并存：

| 口径 | 形式 | 本批判定 |
|:--|:--|:--|
| 六位判别值 | `α⁻¹ = 24(d_H+3)` ⟹ `137.036` | **不达标**（≈43.6 σ_score；S317 记 43.67） |
| 旧机制式 | `α⁻¹ = 136 + 17(√3−1)/12` = `136·(1+Δλ_min/16)` | **不达标**（≈5.1e4 σ_score） |
| S320 式 | `α⁻¹ = 72 + 24(ln15 + δ*)`，`δ* = 6σ³+4σ⁵+8σ⁷+5σ⁸` | 数值达标（0.027 σ_score），但**装配盲** |

## 判什么

| 编号 | 命题 | 判什么 |
|:--|:--|:--|
| ① | `137.037 ≤ 136 + 17(√3−1)/12` | 旧机制式偏高，且超出观测 1e-3 量级 |
| ② | `47000 ≤ (旧机制式 − α⁻¹_obs)/u`（`u = 2.1e-8`） | 旧式按 σ_score 口径**远不达标** |
| ③ | 相对偏差 `< 1e-5`（同一旧式） | 「0.0008% 观察级」只是百分比口径的错觉 |
| ④ | `∀ A`，`∃ δ*`，`72+24(ln15+δ*) = A` | 若 `δ*` 由观测反推，装配对**任何**观测值都精确命中 |
| ⑤ | 同上唯一性：`δ*` 由 `A` 唯一确定 | 反推无自由度 ⟹ 达标零信息 |

## 判决

**旧机制式不达标；S320 式的达标不含预言力。**

- ① ②：`136+17(√3−1)/12 = 137.0370719…`，与 `α⁻¹_obs = 137.035999084(21)` 差
  `1.0729e-3`，在 `u = 2.1e-8` 下 `σ_score ≈ 5.1e4`。旧文档把它记作「0.0008% 观察级」——
  ③ 表明这两个数**同时成立**：相对偏差 7.8e-6（看着像观察级）而 σ_score 5 万（判死）。
  这正是「百分比容差必须禁用」的机检证据。
- ④ ⑤：S320 式里的 `δ*` 最初由观测反推（`δ* = α⁻¹_obs/24 − 3 − ln15`）。而装配式
  `72 + 24(ln15 + δ*)` 对**任意** `A` 都恰有一个 `δ*` 让它精确等于 `A`。故「0.027σ 达标」
  这句话对任何 α⁻¹ 观测值都成立，信息量为零。
- S320 那批真正的数值内容是**级数到反推值的逼近**（`6σ³+4σ⁵+8σ⁷+5σ⁸` 与
  `δ*_obs` 相差 `2.3914e-11`，Python 侧可复现），不是装配式本身。这个逼近是候选级
  命中，其预言力要等「下一阶项由规则先验给出」才能建立——本模块不替它升格。

## 对本轮主问题的意义

α⁻¹ 是四处真断裂里唯一曾靠「换口径」从危机变达标的。本判定说明：换口径换掉的是
**可预言性**（机制式 ⟹ 反推+拟合式），不是断裂。装配盲定理（④）是 §20 的 `λ` 盲定理同型：
**一旦参数由观测反推，装配式对任何观测都成立，检验失效。**

## 诚实边界

1. `α⁻¹_obs = 137.035999084` 与 `u = 2.1e-8` 取 CODATA 2018（与本项目既有登记一致），
   仅用于 σ_score 对照，不作生成源。换 CODATA 2022 只会把 u 改小，σ_score 更大，判决方向不变。
2. 本模块**不判** S320 级数的系数/幂次规则（`{6,4,8,5}` / `{3,5,7,8}` 的框架身份）是否成立；
   那是 S333–S410 的锚化工作，超出本批范围。
3. 级数与 `δ*_obs` 的 `2.39e-11` 逼近是浮点复现（`scripts/alpha_crisis_audit_s72.py`），
   不在 Lean 内核（`Real.log 15` 的 1e-10 级数值界不在本模块证明范围）。
4. 本模块不新增常数、不新增公设；无 `sorry`。
-/

import MUFPFormalization.AlphaChain
import Mathlib.Tactic

namespace MUFPF.AlphaCrisisAudit

/-- 外部对照值：`α⁻¹_obs = 137.035999084`（CODATA 2018，**仅作 σ_score 对照**）。 -/
def obsAlphaInv : ℝ := 137.035999084

/-- 外部对照不确定度：`u = 2.1e-8`（CODATA 2018，1σ）。 -/
def obsUncertainty : ℝ := 2.1e-8

/-- 旧机制式：`α⁻¹ = 136·(1+Δλ_min/16) = 136 + 17(√3−1)/12`。 -/
noncomputable def oldMechValue : ℝ := 136 + 17 * (Real.sqrt 3 - 1) / 12

/-- **判①**：旧机制式 ≥ 137.037（偏高，超过观测 `137.036` 的千分之一量级）。 -/
theorem old_mech_exceeds :
    (137.037 : ℝ) ≤ oldMechValue := by
  unfold oldMechValue
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith [hsq, Real.sqrt_nonneg 3]

/-- **判①′**：旧机制式 ≤ 137.0371（上界——用于判③的相对偏差）。 -/
theorem old_mech_below :
    oldMechValue ≤ (137.0371 : ℝ) := by
  unfold oldMechValue
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith [hsq, Real.sqrt_nonneg 3]

/-- **判②**：旧机制式按 σ_score 口径 `σ_score = |pred − obs| / u ≥ 47000`——远不达标
    （用户纪律：≤1σ 达标 / 1–3σ 提示 / >3σ 否决）。 -/
theorem old_mech_sigma_at_least_47000 :
    (47000 : ℝ) ≤ (oldMechValue - obsAlphaInv) / obsUncertainty := by
  have hpos : (0 : ℝ) < obsUncertainty := by norm_num [obsUncertainty]
  rw [le_div_iff₀ hpos]
  have h1 : (137.037 : ℝ) ≤ oldMechValue := old_mech_exceeds
  have h2 : (47000 : ℝ) * obsUncertainty ≤ (137.037 : ℝ) - obsAlphaInv := by
    norm_num [obsUncertainty, obsAlphaInv]
  linarith

/-- **判③**：同一旧机制式的**相对**偏差 < 1e-5（`0.0008%` 的来源）——
    与判② 的 4.7e4σ 并存。故「百分比很小」与「σ_score 达标」是两件事。 -/
theorem old_mech_relative_below_1e5 :
    (oldMechValue - obsAlphaInv) / obsAlphaInv < (0.00001 : ℝ) := by
  have hpos : (0 : ℝ) < obsAlphaInv := by norm_num [obsAlphaInv]
  rw [div_lt_iff₀ hpos]
  have h1 : oldMechValue ≤ (137.0371 : ℝ) := old_mech_below
  have h2 : (137.0371 : ℝ) - obsAlphaInv < (0.00001 : ℝ) * obsAlphaInv := by
    norm_num [obsAlphaInv]
  linarith

/-- **判②′**：六位口径 `137.036`（`24(d_H+3)` 的判别值）在同一 `u` 下 `σ_score ≥ 43`
    （S317 记的 43.67σ 即此口径；精确比值 9.16e-7 / 2.1e-8 = 43.6）——同样否决。 -/
theorem discriminant_137036_sigma_at_least_43 :
    (43 : ℝ) ≤ ((137.036 : ℝ) - obsAlphaInv) / obsUncertainty := by
  have hpos : (0 : ℝ) < obsUncertainty := by norm_num [obsUncertainty]
  rw [le_div_iff₀ hpos]
  norm_num [obsUncertainty, obsAlphaInv]

/-- **判④**：装配式对**任意**观测值都精确命中——若 `δ*` 由观测反推，则
    `72 + 24(ln15 + δ*) = A` 对每个 `A` 都有解（检验必然通过）。 -/
theorem assembly_hits_any_observation (A : ℝ) :
    ∃ d : ℝ, (72 : ℝ) + 24 * (Real.log 15 + d) = A :=
  ⟨A / 24 - 3 - Real.log 15, by ring⟩

/-- **判④′**（展开形式，便于引用）：反推 `δ* = A/24 − 3 − ln15` 精确命中。 -/
theorem reverse_delta_star_exact (A : ℝ) :
    (72 : ℝ) + 24 * (Real.log 15 + (A / 24 - 3 - Real.log 15)) = A := by
  ring

/-- **判⑤**：反推无自由度——在装配式下 `δ*` 由 `A` 唯一确定。 -/
theorem delta_star_unique (A d : ℝ)
    (h : (72 : ℝ) + 24 * (Real.log 15 + d) = A) :
    d = A / 24 - 3 - Real.log 15 := by
  linarith

/-! ## S320 级数的有理骨架（引 `AlphaChain` 已证结果，不重复证明） -/

/-- S320 级数 `6σ³+4σ⁵+8σ⁷+5σ⁸` 的精确有理值。 -/
theorem delta_star_series_rational :
    (6 : ℝ) * (1 / 15) ^ 3 + 4 * (1 / 15) ^ 5 + 8 * (1 / 15) ^ 7 + 5 * (1 / 15) ^ 8
      = 36559 / 20503125 :=
  MUFPF.AlphaChain.delta_star_rational_decomp

/-- **R-e 判决汇总**：

    ① 旧机制式 ≥ 137.037（偏高）；
    ② σ_score ≥ 47000（否决）；
    ③ 相对偏差 < 1e-5（百分比口径的错觉，与② 并存）；
    ④ 装配式对任意观测值精确命中（`δ*` 由观测反推 ⟹ 检验失效）；
    ⑤ 反推唯一（无自由度）。 -/
theorem alpha_inv_crisis_verdict :
    (137.037 : ℝ) ≤ oldMechValue ∧
    (47000 : ℝ) ≤ (oldMechValue - obsAlphaInv) / obsUncertainty ∧
    (43 : ℝ) ≤ ((137.036 : ℝ) - obsAlphaInv) / obsUncertainty ∧
    (oldMechValue - obsAlphaInv) / obsAlphaInv < (0.00001 : ℝ) ∧
    (∀ A : ℝ, ∃ d : ℝ, (72 : ℝ) + 24 * (Real.log 15 + d) = A) ∧
    (∀ A d : ℝ, (72 : ℝ) + 24 * (Real.log 15 + d) = A → d = A / 24 - 3 - Real.log 15) :=
  ⟨old_mech_exceeds, old_mech_sigma_at_least_47000, discriminant_137036_sigma_at_least_43,
   old_mech_relative_below_1e5,
   assembly_hits_any_observation, delta_star_unique⟩

end MUFPF.AlphaCrisisAudit
