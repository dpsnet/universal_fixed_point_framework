import Mathlib.Tactic
import MUFPFormalization.AreaOperatorNormalization
import MUFPFormalization.BoundaryDefect
import MUFPFormalization.HolographicAdjunctionBridge

/-!
# 面积算符谱（环节 2c，2026-10-24）

对应 `notes/04_lorentz_gravity/全息定理化论证骨架_RecSp对偶.md` §2 环节 2c
（缺口核心：面积算符的谱定义未固化）。本文件给出**面积算符谱的可机检定义**：

- **面积量子** `areaQuantum k codim := normalizedArea (boundaryDefect k) codim`：
  k 个锁定窗口（周期轨道）在 codim 维旋量纤维归一化下的面积值（codim=2 ⟹ /4）；
- **面积算符谱（codim=2）** `areaSpectrum2 := {a | ∃ k, a = areaQuantum k 2}`：
  可能面积值的量子化集合——面积是**离散谱量**，量子数 = 轨道计数 k（Rec 侧结构性量子化）；
- ★ `area_quantization`：X 的面积 = areaQuantum (orbitCount X) 2——物理面积落在谱上，
  量子数即 orbitCount；
- `area_mem_spectrum` / `areaSpectrum_countable`：面积 ∈ 谱、谱可数（离散化证据）。

物理论证边界：本文件固化"面积算符谱 = 量子化面积集合"的**结构定义**（面积取值
由 Rec 生成链离散计数决定）；"该谱与视界面积算符物理谱（2310 式 34/79、2311 式 24
面积变分）等同"仍为语义缺口（2a 本体 + 载荷等同），留物理论证层。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.AreaSpectrum

open MUFPF.PeriodicOrbitCount
open MUFPF.HolographicAdjunction

/-- 面积量子：k 个锁定窗口（周期轨道）在 codim 维旋量纤维归一化下的面积值。 -/
noncomputable def areaQuantum (k : ℕ) (codim : ℕ) : ℝ :=
  MUFPF.AreaOperator.normalizedArea (MUFPF.boundaryDefect k) codim

/-- 面积算符谱（codim=2）：可能面积值的量子化集合（量子数 = 轨道计数 k）。 -/
def areaSpectrum2 : Set ℝ := {a : ℝ | ∃ k : ℕ, a = areaQuantum k 2}

/-- ★ 面积量子化：X 的面积 = 量子数 orbitCount X 对应的面积量子——
    物理面积落在量子化面积谱上（Rec 侧结构性量子化，连续物理量由离散计数生成）。 -/
theorem area_quantization (X : RecObj) : areaAt X = areaQuantum (orbitCount X) 2 := by
  unfold areaAt areaQuantum
  rfl

/-- 面积 ∈ 面积算符谱：对任意 Rec 对象 X，其面积是谱元素。 -/
theorem area_mem_spectrum (X : RecObj) : areaAt X ∈ areaSpectrum2 := by
  unfold areaSpectrum2
  refine ⟨orbitCount X, ?_⟩
  exact area_quantization X

/-- 面积算符谱可数（离散化证据）：谱由 ℕ 经面积量子满射生成。 -/
theorem areaSpectrum_countable : (areaSpectrum2 : Set ℝ).Countable := by
  have hne : (areaSpectrum2 : Set ℝ).Nonempty := by
    refine ⟨areaQuantum 1 2, ?_⟩
    unfold areaSpectrum2
    exact ⟨1, rfl⟩
  refine (Set.countable_iff_exists_surjective hne).mpr ?_
  let f : ℕ → (areaSpectrum2 : Set ℝ) :=
    fun k => ⟨areaQuantum k 2, by
      unfold areaSpectrum2
      exact ⟨k, rfl⟩⟩
  refine ⟨f, ?_⟩
  intro ⟨a, ha⟩
  rcases ha with ⟨k, hk⟩
  refine ⟨k, ?_⟩
  ext
  exact hk.symm

end MUFPF.AreaSpectrum
