import Mathlib.Tactic
import MUFPFormalization.RecCategory
import MUFPFormalization.PeriodicOrbitCount
import MUFPFormalization.OrbitFullLock

/-!
# 窗口计数边界：orbitCount ∈ [1, 15]（指认 C 的边界机检）

对应骨架 §5b 指认 C（2026-10-23，用户裁决方向 C：先攻边界，"=15"留待映射构造）。

- `windowRec15_id`：15 窗口状态模型（对象级：非平凡窗口 = 4 维方向非空子集，语义见
  骨架 C4/L3），step = id；
- `windowRec15_next`：同状态空间，step = Fin 15 循环后继（偏心实例）；
- `windowRec15_id_orbitCount_le`：**orbitCount ≤ 15**（上界机检：orbitCount_le_card +
  Fin 15 基数）；
- `windowRec15_next_ecc` + `windowRec15_next_orbitCount_pos`：**偏心 ⟹ orbitCount ≥ 1**
  （下界机检：orbitCount_pos_of_eccentric 实例化）；
- `windowRec15_id_orbitCount_eq_15`：**上界可达性（定理级，2026-10-23 追加）**——全不动
  （step = id）⟹ orbitCount = card = 15，OrbitFullLock (⇐) 方向实例化（无需自建
  Quotient 双射）。原"登记级/平凡真"标注升级：`orbitCount = 15 ⟺ 全锁定` 的 15 窗口
  具体实现成立，且由 OrbitFullLock 反向亦得"=15 ⟹ 恒等"。

结论：g = orbitCount ∈ [1, 15]（机检边界）；上界 15 可达已定理级（全锁定模型）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.PeriodicOrbitCount

open MUFPF
open MUFPF.EccentricOrbit

/-- 15 窗口状态模型（对象级：非平凡窗口，语义 = 4 维方向非空子集，16−1 = 2⁴−1 = 15）。
    step = id：上界演示（平凡真）。 -/
def windowRec15_id : RecObj where
  T := Fin 15
  fin := inferInstance
  dec := inferInstance
  step := fun i => i

/-- 15 窗口偏心模型：step = Fin 15 循环后继（i ↦ i+1 mod 15，偏心实例）。 -/
def windowRec15_next : RecObj where
  T := Fin 15
  fin := inferInstance
  dec := inferInstance
  step := fun i => i + 1

/-- 上界：orbitCount(id) ≤ 15（orbitCount_le_card + Fintype.card (Fin 15) = 15）。 -/
theorem windowRec15_id_orbitCount_le : orbitCount windowRec15_id ≤ 15 := by
  classical
  exact orbitCount_le_card windowRec15_id

/-- 偏心模型：∃ x, step x ≠ x（循环后继非恒等）。 -/
lemma windowRec15_next_ecc : ∃ x : Fin 15, windowRec15_next.step x ≠ x := by
  refine ⟨0, ?_⟩
  simp [windowRec15_next]

/-- 下界：偏心 ⟹ orbitCount ≥ 1（orbitCount_pos_of_eccentric 实例化）。 -/
theorem windowRec15_next_orbitCount_pos : 0 < orbitCount windowRec15_next :=
  orbitCount_pos_of_eccentric windowRec15_next windowRec15_next_ecc

/-- 上界可达性（定理级）：15 窗口全锁定模型 orbitCount = 15。
    全不动（step = id）⟹ orbitCount = Fintype.card（OrbitFullLock (⇐) 实例化）
    + card (Fin 15) = 15。原登记级标注（WindowCountBounds v1 注释"平凡真/过度工程"）
    升级：商级验证无需自建双射，通用引理直接覆盖。 -/
theorem windowRec15_id_orbitCount_eq_15 : orbitCount windowRec15_id = 15 := by
  classical
  have hfull : ∀ x : Fin 15, windowRec15_id.step x = x := by
    intro x
    rfl
  have hc : orbitCount windowRec15_id = Fintype.card (Fin 15) :=
    orbitCount_eq_card_of_all_fixed windowRec15_id hfull
  rw [hc]
  simp

end MUFPF.PeriodicOrbitCount
