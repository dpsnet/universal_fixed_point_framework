import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import MUFPFormalization.RecCategory
import MUFPFormalization.EccentricPeriodicOrbit

/-!
# 周期轨道计数 orbitCount：A 层定义的机器基底

对应 `notes/04_lorentz_gravity/偏心-周期轨道-简并度_论证骨架.md` §5
（2026-10-23，用户裁决 A+B+C：A = g = 周期轨道数 = 锁定窗口数）。

本文件机检候选 A 的**定义锚**：
- `periodic_iterate_mul`：周期点引理（周期 p ⟹ 迭代 p·k 次不动）；
- `periodOrbitRel`：周期点前向可达（同一循环）；
- 三性质：refl / symm / trans —— **周期点可达性 = 等价关系**（数值先证伪 5000 组随机
  自映射零违例，scripts/orbitcount_verify.py）；
- `periodOrbitSetoid` / `orbitCount X = Fintype.card (Quotient (periodOrbitSetoid X))`：
  周期轨道数；
- `orbitCount_pos`（有周期点 ⟹ 0 < orbitCount）、`orbitCount_le_card`
  （orbitCount ≤ |P| ≤ card X.T）、`orbitCount_pos_of_eccentric`
  （**偏心结构 ⟹ 至少一个锁定窗口**——候选 A 的机器版本）。

诚实边界：orbitCount 是定义锚（g 的身份），"g = orbitCount"的物理对应（锁定窗口
↔ 简并度）与 g=15 动机（B 层）仍为物理论证（骨架 §5 诚实边界 1/2）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.PeriodicOrbitCount

open MUFPF.EccentricOrbit

/-- 周期点引理：x 是周期 p 的周期点 ⟹ step 迭代 p·k 次仍不动。 -/
lemma periodic_iterate_mul (X : RecObj) (p k : ℕ) (x : X.T) (_hp : p > 0)
    (h : X.step^[p] x = x) : X.step^[p * k] x = x := by
  induction k with
  | zero => simp
  | succ k ih =>
    calc
      X.step^[p * (k + 1)] x = X.step^[p * k + p] x := by rw [Nat.mul_succ]
      _ = X.step^[p * k] (X.step^[p] x) := by
        exact Function.iterate_add_apply X.step (p * k) p x
      _ = X.step^[p * k] x := by rw [h]
      _ = x := ih

/-- 周期点前向可达（同一循环）：x、y 均为周期点，x 经有限步可到 y。 -/
def periodOrbitRel (X : RecObj) (x y : {z : X.T // periodicPoint X z}) : Prop :=
  ∃ n : ℕ, X.step^[n] x.1 = y.1

lemma periodOrbitRel_refl (X : RecObj) (x : {z : X.T // periodicPoint X z}) :
    periodOrbitRel X x x :=
  ⟨0, rfl⟩

lemma periodOrbitRel_symm (X : RecObj) (x y : {z : X.T // periodicPoint X z})
    (h : periodOrbitRel X x y) : periodOrbitRel X y x := by
  rcases h with ⟨n, hn⟩
  rcases x.2 with ⟨p, hp, hxp⟩
  let k := p * (n + 1) - n
  refine ⟨k, ?_⟩
  have hkn : k + n = p * (n + 1) := by
    dsimp [k]
    exact Nat.sub_add_cancel
      (le_trans (Nat.le_succ n) (by simpa [Nat.mul_comm] using Nat.le_mul_of_pos_right (n + 1) hp))
  calc
    X.step^[k] y.1 = X.step^[k] (X.step^[n] x.1) := by rw [hn]
    _ = X.step^[k + n] x.1 := by
      exact (Function.iterate_add_apply X.step k n x.1).symm
    _ = X.step^[p * (n + 1)] x.1 := by rw [hkn]
    _ = x.1 := by
      exact periodic_iterate_mul X p (n + 1) x.1 hp hxp

lemma periodOrbitRel_trans (X : RecObj) (x y z : {w : X.T // periodicPoint X w})
    (hxy : periodOrbitRel X x y) (hyz : periodOrbitRel X y z) : periodOrbitRel X x z := by
  rcases hxy with ⟨n, hn⟩
  rcases hyz with ⟨m, hm⟩
  refine ⟨n + m, ?_⟩
  calc
    X.step^[n + m] x.1 = X.step^[m] (X.step^[n] x.1) := by
      rw [show n + m = m + n by omega]
      exact Function.iterate_add_apply X.step m n x.1
    _ = X.step^[m] y.1 := by rw [hn]
    _ = z.1 := hm

/-- 周期轨道等价（Setoid）：周期点在"同一循环"下商。 -/
noncomputable def periodOrbitSetoid (X : RecObj) :
    Setoid {z : X.T // periodicPoint X z} where
  r := periodOrbitRel X
  iseqv := ⟨periodOrbitRel_refl X, @periodOrbitRel_symm X, @periodOrbitRel_trans X⟩

lemma quotient_mk_surj (X : RecObj) :
    Function.Surjective (Quotient.mk (periodOrbitSetoid X) :
      {z : X.T // periodicPoint X z} → Quotient (periodOrbitSetoid X)) := by
  intro q
  rcases Quotient.exists_rep q with ⟨a, ha⟩
  exact ⟨a, ha⟩

noncomputable instance periodOrbitFintype (X : RecObj) :
    Fintype (Quotient (periodOrbitSetoid X)) := by
  classical
  exact Fintype.ofSurjective (Quotient.mk (periodOrbitSetoid X)) (quotient_mk_surj X)

/-- 周期轨道数（orbitCount）：周期点商集大小 = 循环数（候选 A 的 g）。 -/
noncomputable def orbitCount (X : RecObj) : ℕ := by
  classical
  exact Fintype.card (Quotient (periodOrbitSetoid X))

/-- 有周期点 ⟹ orbitCount > 0（商非空）。 -/
theorem orbitCount_pos (X : RecObj) (h : ∃ x : X.T, periodicPoint X x) :
    0 < orbitCount X := by
  classical
  rw [orbitCount, Fintype.card_pos_iff]
  rcases h with ⟨x, hx⟩
  exact ⟨Quotient.mk (periodOrbitSetoid X) ⟨x, hx⟩⟩

/-- orbitCount ≤ |周期点集| ≤ card X.T（每个循环至少一个元素）。 -/
theorem orbitCount_le_card (X : RecObj) : orbitCount X ≤ Fintype.card X.T := by
  classical
  rw [orbitCount]
  have h1 : Fintype.card (Quotient (periodOrbitSetoid X)) ≤
      Fintype.card {z : X.T // periodicPoint X z} := by
    exact Fintype.card_le_of_surjective (Quotient.mk (periodOrbitSetoid X))
      (quotient_mk_surj X)
  have h2 : Fintype.card {z : X.T // periodicPoint X z} ≤ Fintype.card X.T := by
    exact Fintype.card_subtype_le (fun z : X.T => periodicPoint X z)
  exact h1.trans h2

/-- 偏心结构 ⟹ 至少一个锁定窗口（周期轨道）——候选 A 的机器版本。 -/
theorem orbitCount_pos_of_eccentric (X : RecObj) (hecc : ∃ x : X.T, X.step x ≠ x) :
    0 < orbitCount X :=
  orbitCount_pos X (eccentric_has_periodic_point X hecc)

end MUFPF.PeriodicOrbitCount
