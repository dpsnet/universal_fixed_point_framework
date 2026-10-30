import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import MUFPFormalization.RecCategory

/-!
# 偏心元素 ↔ 周期轨道：论证骨架的机器基底

对应 `notes/04_lorentz_gravity/偏心-周期轨道-简并度_论证骨架.md`（2026-10-23）。

背景：全息定理化链条剩余唯一物理输入 = defectMeasure(X_∂) = 4·ln g
（边界缺陷度量 ↔ 简并度关系）。候选论证路径（既有文档叙事，
compact_pulsar_gw_causal_chain.md）：偏心元素（defectMeasure 计数）→
偏心子集群绕质心做**周期轨道运动**（T-02 因果链第 2 步，已形式化）→
周期轨道 ↔ 谱静默锁定窗口 ↔ 简并度 g（S3B ln15 家族）。

本文件机检**数学基底**：
- `orbit_eventually_periodic`：有限状态空间上，非不动点元素（偏心元素）的
  迭代轨道**最终进入周期**（轨道最终自交；周期可平凡 = 1，即落入不动点）。
  这是"偏心元素做周期运动"的最小真命题（鸽巢原理）。
- 候选 A（论证骨架 §5，用户裁决 A+B+C，2026-10-23）周期点基础：
  `periodicPoint`（周期点定义，含 p=1 不动点）、`exists_periodic_point`
  （任一元素轨道最终含周期点）、`eccentric_has_periodic_point`
  （偏心结构 ⟹ 周期点存在）、`fixedPoint_is_periodicPoint`（不动点 = 周期 1 点，
  连接 GroundDegeneracy 计数与轨道计数）。

诚实边界（§3 论证骨架）：
- "非不动点 ⟹ 存在非平凡周期点（周期 > 1）"是**假命题**——反例：
  step: a→b, b→b（a 非不动点，唯一周期点 b 周期 1）。本文件不证该假命题；
- 物理对接"偏心子集群做周期轨道运动"用的是**集群整体的动力学轨道**
  （整个偏心集群最终周期性调制），与逐点周期不同——论证见骨架文档 §2。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.EccentricOrbit

open Function

/-- 轨道最终周期化（鸽巢）：有限状态空间上**任意**元素 x 的迭代轨道必自交，
    即 ∃ n < m，step 迭代 n 次与 m 次重合。
    该陈述不依赖 x 是否偏心（非不动点）——对一切 x 成立（更强）。
    物理论证中的语义对应（偏心元素轨道最终周期化）见
    `notes/04_lorentz_gravity/偏心-周期轨道-简并度_论证骨架.md` §3。 -/
theorem orbit_eventually_periodic (X : RecObj) (x : X.T) :
    ∃ n m : ℕ, n < m ∧ X.step^[n] x = X.step^[m] x := by
  let f : Fin (Fintype.card X.T + 1) → X.T := fun i => X.step^[i.1] x
  have hnotinj : ¬ Function.Injective f := by
    intro hinj
    have hle : Fintype.card (Fin (Fintype.card X.T + 1)) ≤ Fintype.card X.T :=
      Fintype.card_le_of_injective f hinj
    have hcard : Fintype.card (Fin (Fintype.card X.T + 1)) = Fintype.card X.T + 1 :=
      Fintype.card_fin _
    omega
  have hpair : ∃ i j : Fin (Fintype.card X.T + 1), i ≠ j ∧ f i = f j := by
    by_contra h
    apply hnotinj
    intro a b hab
    by_contra hne
    exact (h ⟨a, b, hne, hab⟩)
  rcases hpair with ⟨i, j, hne, heq⟩
  have hval : i.1 ≠ j.1 := by
    intro hij
    apply hne
    ext
    exact hij
  rcases lt_or_gt_of_ne hval with hlt | hgt
  · refine ⟨i.1, j.1, ?_, ?_⟩
    · exact hlt
    · simpa [f] using heq
  · refine ⟨j.1, i.1, ?_, ?_⟩
    · exact hgt
    · simpa [f] using heq.symm

/-- 周期点：x 是 step 的周期点，即存在正周期 p 使 step 迭代 p 次回到自身
    （p = 1 即不动点，含于其中）。对应论证骨架候选 A 的"锁定窗口承载元素"。 -/
def periodicPoint (X : RecObj) (x : X.T) : Prop :=
  ∃ p : ℕ, p > 0 ∧ X.step^[p] x = x

/-- 任一元素的轨道最终进入周期：轨道自交（orbit_eventually_periodic）处
    取 y = step^[n] x 即周期点（周期 m−n > 0）。 -/
theorem exists_periodic_point (X : RecObj) (x : X.T) :
    ∃ y : X.T, periodicPoint X y := by
  rcases orbit_eventually_periodic X x with ⟨n, m, hlt, heq⟩
  refine ⟨X.step^[n] x, ?_⟩
  refine ⟨m - n, ?_, ?_⟩
  · omega
  · calc
      X.step^[m - n] (X.step^[n] x) = X.step^[(m - n) + n] x := by
        exact (Function.iterate_add_apply X.step (m - n) n x).symm
      _ = X.step^[m] x := by
        rw [show (m - n) + n = m by omega]
      _ = X.step^[n] x := heq.symm

/-- 偏心结构保证周期点存在：存在非不动点（defectMeasure > 0 的组合内容）
    ⟹ 至少一个周期点（不动点或真周期点）。 -/
theorem eccentric_has_periodic_point (X : RecObj)
    (hecc : ∃ x : X.T, X.step x ≠ x) :
    ∃ y : X.T, periodicPoint X y := by
  rcases hecc with ⟨x, hx⟩
  exact exists_periodic_point X x

/-- 不动点即周期点（周期 1）。简并度 A 层计数（GroundDegeneracy 计数不动点
    满壳层 1-本征态）与周期轨道（含周期 1）的连接引理。 -/
theorem fixedPoint_is_periodicPoint (X : RecObj) (x : X.T) (h : X.step x = x) :
    periodicPoint X x := by
  refine ⟨1, Nat.succ_pos 0, ?_⟩
  simp [h]

end MUFPF.EccentricOrbit
