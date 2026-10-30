import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import MUFPFormalization.SpCategory
import MUFPFormalization.HolographicEntropyDegeneration

/-!
# 基态简并度（S3 语义立项·候选 A 计数口径打底）

对应 `notes/00_foundations/S3简并度语义_立项.md`（2026-10-23 用户裁决 D 组合：A 打底 + B 数值锚 + C 目标口径）。
用户裁决原文："D 组合（推荐）"——A 计数口径打底（本文件）、B 静默层拓扑熵数值锚、C 面积元目标口径。

本文件（A 打底）：
- `groundDegeneracy E`：Sp 对象谱对角元中本征值 1 的个数（纯态系综 0/1 谱）。
  物理对应：谱静默锁定窗口/满壳层态数（photon_first_principle_origin.md:279，
  "满壳层（简并度 2n²）构成稳定静默配置"）。
- `groundDegeneracy_eq_count`：计数对齐（对角元恰前 g 个为 1、其余非 1 且 g ≤ n ⟹ 计数 = g）。
- `degeneracy_entropy_alignment`：简并熵对齐（计数 = g ⟹ entropyOfRange(计数) = ln g，
  把 S1 熵算符的 Sp 对象版桥接到既有权重熵机检件）。
- `area_eq_entropy_via_degeneracy`：组装句（d=4·ln g 的 g 由计数给出时，面积 = 熵）。

B 数值锚（静默层来源：ln15 家族、静默单元 5、韦达 15、三代质量指数 {0, ln15, ln15+3}）与
C 目标口径（每面积元 1/4 比特，ln g = A/4）见立项文档，不在此设 axiom（零 sorry 政策）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.HolographicSilence

open CategoryTheory

/-- 基态简并度（候选 A 计数口径）：g = 谱对角元中本征值 1 的个数（纯态系综 0/1 谱）。 -/
noncomputable def groundDegeneracy (E : SpObj) : ℕ :=
  Finset.card (Finset.univ.filter (fun i : Fin E.n => E.A i i = 1))

/-- 计数对齐定理：若谱对角元恰在前 g 个位置为 1、其余非 1（g ≤ n），则简并度计数 = g。 -/
theorem groundDegeneracy_eq_count {E : SpObj} {g : ℕ} (hg : g ≤ E.n)
    (hA : ∀ i : Fin E.n, (E.A i i = 1 ↔ i.1 < g)) :
    groundDegeneracy E = g := by
  unfold groundDegeneracy
  have hfilter : Finset.univ.filter (fun i : Fin E.n => E.A i i = 1) =
      Finset.univ.filter (fun i : Fin E.n => i.1 < g) := by
    ext i
    simp [hA i]
  rw [hfilter]
  -- card {i : Fin E.n | i.1 < g} = g（当 g ≤ E.n）
  let f : Fin g → Fin E.n := fun j => ⟨j.1, lt_of_lt_of_le j.2 hg⟩
  have hinj : Function.Injective f := by
    intro a b hab
    apply Fin.ext
    simpa [f] using congrArg Fin.val hab
  have himage : Finset.univ.image f = Finset.univ.filter (fun i : Fin E.n => i.1 < g) := by
    ext i
    constructor
    · intro hmem
      rw [Finset.mem_image] at hmem
      rcases hmem with ⟨j, _hj, hf⟩
      simp [f, ← hf, j.2]
    · intro hi
      rw [Finset.mem_filter] at hi
      rcases hi with ⟨_, hi⟩
      let j : Fin g := ⟨i.1, hi⟩
      exact Finset.mem_image.mpr ⟨j, by simp, by simp [f, j]⟩
  rw [← himage]
  rw [Finset.card_image_of_injective _ hinj]
  simp

/-- 简并熵对齐（A 打底 → 熵算符 S1 桥接）：简并度计数 = g ⟹ 权重熵 = ln g。
    这是 S1（spEntropy on SpObj）在简并口径上的既有机检件连接。 -/
theorem degeneracy_entropy_alignment {E : SpObj} {g : ℕ} (hg : 0 < g)
    (hcnt : groundDegeneracy E = g) :
    MUFPF.HolographicEntropy.entropyOfRange (groundDegeneracy E) = Real.log (g : ℝ) := by
  rw [hcnt]
  exact MUFPF.HolographicEntropy.uniform_entropy_eq_log_g g hg

/-- 组装句：d = 4·ln g 的 g 由简并度计数给出时，面积 = 熵（桥归约闭环，codim=2、M_Pl=1）。
    依赖 d=4·ln g（开放物理输入，见 AdjunctionHolographicBridge 归约）。 -/
theorem area_eq_entropy_via_degeneracy {E : SpObj} {d : ℝ} {g : ℕ} (hg : 0 < g)
    (hcnt : groundDegeneracy E = g) (hd : d = 4 * Real.log (g : ℝ)) :
    d / 4 = MUFPF.HolographicEntropy.entropyOfRange (groundDegeneracy E) := by
  have hS : MUFPF.HolographicEntropy.entropyOfRange (groundDegeneracy E) = Real.log (g : ℝ) :=
    degeneracy_entropy_alignment hg hcnt
  rw [hS, hd]
  norm_num

end MUFPF.HolographicSilence
