import Mathlib.Data.Fintype.Card
import Mathlib.Data.Finset.Card
import Mathlib.Logic.Function.Iterate

/-!
# 轨道动力学的最小骨架（S624——2026-11-10）

## 动机

论文 §3（C1 的尺度化）与引言佐证（三）两处登记同一开口：
「为何粗粒化必然在某个尺度上杀掉自由度，需耗散/热化动力学，本框架只给结构」。
本文件检验这条开口能否被**有限性**（而非耗散）关掉一半。

## 结论（三条定理 + 一条反例）

1. `exists_iterate_eq_of_fintype`：有限状态空间上的自映射，轨道必出现重复（鸽巢）。
   —— 纯组合事实，不需要任何动力学公设。
2. `exists_visible_repetition`：**只要观测空间有限**（不需要底层状态空间有限），
   任何轨道在任何有损投影下都会出现可观测重复。
   —— 即「可分辨的新状态不可能无限产出」。这才是论文「在某个尺度上不再产生
   可分辨的新状态」的严格对应物，且它是**必然的**，不依赖耗散。
3. `eventually_periodic_of_fintype`：重复即周期——存在 N、p > 0 使 step^[N+p] x = step^[N] x。
4. `swap_not_frozen`：**但「周期塌成不动点」不是必然的**——Bool 上的取反是有限集上的
   两循环，取恒等观测时永不冻结。

## 由此得到的边界（写入论文）

- 「必然有尽头」：有限性给出，已机检，不需要动力学。
- 「尽头是不是静止」：**不必然**，需要收缩机制（耗散/热化）——这才是动力学的职责。
- 论文原措辞把两件事合并推给「耗散动力学」，是把已可证的必然性与真正开放的
  收缩机制混为一谈。本文件把前者关掉，把后者精确留下。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF

/-- 有限状态空间上的自映射，其迭代轨道必出现重复（鸽巢原理）。

    这是「有尽头」的纯组合来源：只要状态空间有限，任何轨道都在有限步内回访
    某个已访问状态。不需要任何动力学公设、不需要耗散。 -/
theorem exists_iterate_eq_of_fintype {α : Type*} [Fintype α]
    (step : α → α) (x : α) :
    ∃ i j : ℕ, i < j ∧ step^[i] x = step^[j] x := by
  classical
  -- 取 card α + 1 个轨道点，落在只有 card α 个元素的状态空间里 ⇒ 必有两个相同
  obtain ⟨a, _, b, _, hne, heq⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to
      (s := Finset.range (Fintype.card α + 1))
      (t := (Finset.univ : Finset α))
      (f := fun n : ℕ => step^[n] x)
      (by simp)
      (by intro y _; simp)
  rcases Nat.lt_or_gt_of_ne hne with h | h
  · exact ⟨a, b, h, heq⟩
  · exact ⟨b, a, h, heq.symm⟩

/-- 重复即周期：有限状态空间上的轨道最终进入周期循环。

    注意这条只说「最终循环」，**不说**循环长度为 1。 -/
theorem eventually_periodic_of_fintype {α : Type*} [Fintype α]
    (step : α → α) (x : α) :
    ∃ N p : ℕ, 0 < p ∧ step^[N + p] x = step^[N] x := by
  obtain ⟨i, j, hij, heq⟩ := exists_iterate_eq_of_fintype step x
  refine ⟨i, j - i, Nat.sub_pos_of_lt hij, ?_⟩
  have hadd : i + (j - i) = j := Nat.add_sub_of_le (Nat.le_of_lt hij)
  rw [hadd]
  exact heq.symm

/-- 有限观测空间中的轨道必出现可观测重复：有损、有限像的尺度下，
    「可分辨的新状态」不可能无限产出。

    这条**不要求底层状态空间有限**（只要求观测值域 `Y` 有限）——它对应论文的
    说法：「在某个尺度上，它不再产生可分辨的新状态」。必然性来自观测的有限分辨率，
    不来自耗散。 -/
theorem exists_visible_repetition {α Y : Type*} [Fintype Y]
    (step : α → α) (obs : α → Y) (x : α) :
    ∃ i j : ℕ, i < j ∧ obs (step^[i] x) = obs (step^[j] x) := by
  classical
  obtain ⟨a, _, b, _, hne, heq⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to
      (s := Finset.range (Fintype.card Y + 1))
      (t := (Finset.univ : Finset Y))
      (f := fun n : ℕ => obs (step^[n] x))
      (by simp)
      (by intro y _; simp)
  rcases Nat.lt_or_gt_of_ne hne with h | h
  · exact ⟨a, b, h, heq⟩
  · exact ⟨b, a, h, heq.symm⟩

/-- 反例：**「周期塌成不动点」不是必然的**。

    Bool 上的取反（2 元有限集上的两循环）在恒等观测下永不冻结——
    每一步都产生可分辨的新状态（真→假→真…）。

    这条反例的作用：把「必然有尽头」（上一定理，真）与「必然静止」（本定理否定）
    分开。后者需要收缩机制，属动力学，不由有限性给出。 -/
theorem swap_not_frozen :
    ∃ (step : Bool → Bool) (obs : Bool → Bool), ¬ ∀ x, obs (step x) = obs x := by
  refine ⟨Bool.not, id, ?_⟩
  intro h
  have h1 : id (Bool.not true) = id true := h true
  simp at h1

end MUFPF
