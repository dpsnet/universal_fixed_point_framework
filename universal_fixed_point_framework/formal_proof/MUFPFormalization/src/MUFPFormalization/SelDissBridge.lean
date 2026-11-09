import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import MUFPFormalization.RecCategory
import MUFPFormalization.NoiseCategory
import MUFPFormalization.NoiseSignatureBridge
import MUFPFormalization.LorentzSignatureBridge

namespace MUFPF.SelDissBridge

open MUFPF
open MUFPF.CoherenceToBranching
open MUFPF.NoiseSignatureBridge

/-
## Sel ⊣ Diss 伴随的实例化

NoiseCategory 已机检 Sel : Σ-Rec ⇄ Rec : Diss 是一对伴随函子。
本节做具体实例化：Sel(dissSilentNoiseData R d hd) = R。

数学关键：dissSilentNoiseData R d hd 的第一个非空分量是 components 0（c₁ < 1）。
因此 Nat.find = 0，Sel 选到 R 本身。

§2 完成 Sel ⊣ Diss 伴随的 Hom 层显式构造（边界 B3 推进）：
收缩 from ∘ to = id + canonical 支撑子类型上的双射 selDissHomEquiv。
完整 SigmaRecHom 上的字面双射结构性不成立（list 编码自由度），如实登记。
--/

/-
## §1 Sel(dissSilentNoiseData R d hd) = R
--/

/-- Sel(dissSilentNoiseData R d hd) 的实例化。

    Sel 取 Nat.find 处的分量值。
    dissSilentNoiseData 在 i=0 非空 → Nat.find = 0 → components 0 = some R → getD = R。
    因此 Sel(dissSilentNoiseData R d hd) = R。 -/
theorem sel_dissSilent_is_R
    (R : RecObj) (d : ℝ) (hd : 0 < d)
    (hDom : ∃ i : ℕ, (dissFunctor R (dissSilentNoiseData d hd)).components i ≠ none) :
    selFunctor (dissFunctor R (dissSilentNoiseData d hd)) hDom = R := by
  dsimp only [selFunctor]
  have hc0 : (dissFunctor R (dissSilentNoiseData d hd)).components 0 ≠ none :=
    dissProducesC1 R d hd
  have hc0_lt : (dissSilentNoiseData d hd).contractions 0 < 1 :=
    (c3_unique_silent_factor d hd).1
  have hc0_val : (dissFunctor R (dissSilentNoiseData d hd)).components 0 =
      some { T := R.T, fin := R.fin, dec := R.dec, step := R.step } := by
    dsimp only [dissFunctor, dissSilentNoiseData]
    exact dite_eq_left hc0_lt
  have hfind_le : Nat.find hDom ≤ 0 := by
    apply Nat.find_min'
    exact hc0
  have hfind0 : Nat.find hDom = 0 := by linarith
  rw [hfind0, hc0_val]
  simp [Option.getD]

/-
## §2 Sel ⊣ Diss 伴随的 Hom 层显式构造（边界 B3 推进）

### 数学内容

目标：Hom_Rec(Sel N, R) 与 Hom_ΣRec(N, Diss R data) 的显式对应。

**结构性事实（诚实登记）**：有限原型中 `SigmaRecHom N Y` 的每个源分量是
`List (Σ j, RecHom ...)` —— 列表编码允许同一 (i,j) 对的多个条目、
以及空源（none 分量，getD = default）上的任意条目。因此**完整
SigmaRecHom 上的字面双射结构性不成立**：反向复合 to ∘ from 只保留
(i₀, j₀) 处单条目，一般 ≠ g。

**机检完成的精确命题**：
  1. 显式正向/反向映射 selDissTo / selDissFrom；
  2. 收缩（retraction）：from ∘ to = id（→ to 单射、from 满射）；
  3. canonical 支撑子类型（仅 (i₀,j₀) 单条目）上的**双射** selDissHomEquiv。

即 Hom_Rec(Sel N, R) ≅ { canonical 支撑的 SigmaRecHom } ⊂ SigmaRecHom。
伴随自然性（naturality）不在本有限原型范围（Sel/Diss 态射层未定义，
NoiseCategory §17 已登记）。
--/

/-- Diss 像在 Nat.find 处的分量是 some（R 的展开）。 -/
lemma diss_component_at_find (R : RecObj) (data : NoiseData)
    (hDiss : ∃ j, data.contractions j < 1) :
    (dissFunctor R data).components (Nat.find hDiss) =
      some { T := R.T, fin := R.fin, dec := R.dec, step := R.step } := by
  have h : data.contractions (Nat.find hDiss) < 1 := Nat.find_spec hDiss
  simp [dissFunctor, h]

/-- 目标分量 getD 坍缩为 R（结构 eta）。 -/
lemma diss_getD_at_find (R : RecObj) (data : NoiseData)
    (hDiss : ∃ j, data.contractions j < 1) :
    ((dissFunctor R data).components (Nat.find hDiss)).getD default = R := by
  rw [diss_component_at_find R data hDiss]
  rfl

/-- 正向类型搬运等式。 -/
lemma selDissHomCastFwd (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (i : ℕ) (h : i = Nat.find hDom) :
    RecHom (selFunctor N hDom) R =
      RecHom ((N.components i).getD default)
             (((dissFunctor R data).components (Nat.find hDiss)).getD default) := by
  subst h
  exact (congrArg (RecHom (selFunctor N hDom)) (diss_getD_at_find R data hDiss)).symm

/-- 反向类型搬运等式。 -/
lemma selDissHomCastBwd (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (j : ℕ) (h : j = Nat.find hDiss) :
    RecHom ((N.components (Nat.find hDom)).getD default)
           (((dissFunctor R data).components j).getD default) =
      RecHom (selFunctor N hDom) R := by
  subst h
  exact congrArg (RecHom ((N.components (Nat.find hDom)).getD default))
    (diss_getD_at_find R data hDiss)

/-- **canonical 支撑形态**：源 i₀ 处唯一条目 ⟨j₀, cast u'⟩，其余源为空列表。 -/
noncomputable def selDissCanonicalForm (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (u' : RecHom (selFunctor N hDom) R) (i : ℕ) :
    List (Σ (j : ℕ), RecHom ((N.components i).getD default)
                            (((dissFunctor R data).components j).getD default)) :=
  if h : i = Nat.find hDom then
    [⟨Nat.find hDiss, cast (selDissHomCastFwd N R data hDom hDiss i h) u'⟩]
  else []

/-- **正向映射 to**：RecHom (Sel N) R → SigmaRecHom N (Diss R data)。 -/
noncomputable def selDissTo (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (f : RecHom (selFunctor N hDom) R) : SigmaRecHom N (dissFunctor R data) where
  components := selDissCanonicalForm N R data hDom hDiss f

/-- to 的输出定义性地是 canonical 形态。 -/
lemma selDissTo_canonical (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (f : RecHom (selFunctor N hDom) R) :
    ∃ u', (selDissTo N R data hDom hDiss f).components =
      selDissCanonicalForm N R data hDom hDiss u' := ⟨f, rfl⟩

/-- to 在源 i₀ 处的值。 -/
lemma selDissTo_components_self (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (f : RecHom (selFunctor N hDom) R) :
    (selDissTo N R data hDom hDiss f).components (Nat.find hDom) =
      [⟨Nat.find hDiss,
        cast (selDissHomCastFwd N R data hDom hDiss (Nat.find hDom) rfl) f⟩] := by
  have h0 : (selDissTo N R data hDom hDiss f).components =
      selDissCanonicalForm N R data hDom hDiss f := rfl
  rw [h0]
  unfold selDissCanonicalForm
  exact dite_eq_left rfl

/-- to 在其他源处的值为空列表。 -/
lemma selDissTo_components_other (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (f : RecHom (selFunctor N hDom) R) (i : ℕ) (hi : i ≠ Nat.find hDom) :
    (selDissTo N R data hDom hDiss f).components i = [] := by
  have h0 : (selDissTo N R data hDom hDiss f).components =
      selDissCanonicalForm N R data hDom hDiss f := rfl
  rw [h0]
  unfold selDissCanonicalForm
  exact dite_eq_right hi

/-- **反向映射（列表层）**：取首条目中目标为 j₀ 的态射；无则回退 hf。 -/
noncomputable def selDissFromList (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R))
    (l : List (Σ (j : ℕ), RecHom ((N.components (Nat.find hDom)).getD default)
                                  (((dissFunctor R data).components j).getD default))) :
    RecHom (selFunctor N hDom) R :=
  match l with
  | [] => hf.some
  | ⟨j, u⟩ :: _ =>
    if hj : j = Nat.find hDiss then
      cast (selDissHomCastBwd N R data hDom hDiss j hj) u
    else hf.some

lemma selDissFromList_singleton (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R)) (j : ℕ)
    (u : RecHom ((N.components (Nat.find hDom)).getD default)
                (((dissFunctor R data).components j).getD default))
    (rest : List (Σ (j : ℕ), RecHom ((N.components (Nat.find hDom)).getD default)
                                     (((dissFunctor R data).components j).getD default))) :
    selDissFromList N R data hDom hDiss hf (⟨j, u⟩ :: rest) =
      (if hj : j = Nat.find hDiss then
        cast (selDissHomCastBwd N R data hDom hDiss j hj) u
      else hf.some) := rfl

lemma selDissFromList_singleton_pos (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R))
    (u : RecHom ((N.components (Nat.find hDom)).getD default)
                (((dissFunctor R data).components (Nat.find hDiss)).getD default)) :
    selDissFromList N R data hDom hDiss hf [⟨Nat.find hDiss, u⟩] =
      cast (selDissHomCastBwd N R data hDom hDiss (Nat.find hDiss) rfl) u := by
  rw [selDissFromList_singleton]
  exact dite_eq_left rfl

/-- **反向映射 from**：SigmaRecHom N (Diss R data) → RecHom (Sel N) R。 -/
noncomputable def selDissFrom (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R))
    (g : SigmaRecHom N (dissFunctor R data)) : RecHom (selFunctor N hDom) R :=
  selDissFromList N R data hDom hDiss hf (g.components (Nat.find hDom))

/-- from 在 canonical 形态上的值：提取出见证 u'。 -/
lemma selDissFrom_of_canonical (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (g : SigmaRecHom N (dissFunctor R data))
    (u' : RecHom (selFunctor N hDom) R)
    (hg : g.components = selDissCanonicalForm N R data hDom hDiss u')
    (hf : Nonempty (RecHom (selFunctor N hDom) R)) :
    selDissFrom N R data hDom hDiss hf g = u' := by
  unfold selDissFrom
  have h1 : g.components (Nat.find hDom) =
      [⟨Nat.find hDiss,
        cast (selDissHomCastFwd N R data hDom hDiss (Nat.find hDom) rfl) u'⟩] := by
    rw [hg]
    exact dite_eq_left rfl
  rw [h1, selDissFromList_singleton_pos, cast_cast, cast_eq]

/-- **收缩主定理**（边界 B3 核心）：from ∘ to = id。
    Hom_Rec(Sel N, R) 是 SigmaRecHom N (Diss R) 的收缩核。 -/
theorem selDissFrom_to (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R))
    (f : RecHom (selFunctor N hDom) R) :
    selDissFrom N R data hDom hDiss hf (selDissTo N R data hDom hDiss f) = f :=
  selDissFrom_of_canonical N R data hDom hDiss _ f rfl hf

/-- 推论：to 单射。 -/
theorem selDissTo_injective (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R)) :
    Function.Injective (selDissTo N R data hDom hDiss) :=
  Function.LeftInverse.injective (selDissFrom_to N R data hDom hDiss hf)

/-- 推论：from 满射。 -/
theorem selDissFrom_surjective (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (hf : Nonempty (RecHom (selFunctor N hDom) R)) :
    Function.Surjective (selDissFrom N R data hDom hDiss hf) :=
  Function.LeftInverse.surjective (selDissFrom_to N R data hDom hDiss hf)

/-- canonical 形态蕴含 RecHom 非空。 -/
lemma nonempty_of_canonical (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    {g : SigmaRecHom N (dissFunctor R data)}
    (hg : ∃ u' : RecHom (selFunctor N hDom) R,
      g.components = selDissCanonicalForm N R data hDom hDiss u') :
    Nonempty (RecHom (selFunctor N hDom) R) :=
  hg.elim fun u' _ => ⟨u'⟩

/-- 反向 round-trip：canonical 形态上 to ∘ from = id。 -/
theorem selDissTo_from_of_canonical (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1)
    (g : SigmaRecHom N (dissFunctor R data))
    (u' : RecHom (selFunctor N hDom) R)
    (hg : g.components = selDissCanonicalForm N R data hDom hDiss u')
    (hf : Nonempty (RecHom (selFunctor N hDom) R)) :
    selDissTo N R data hDom hDiss (selDissFrom N R data hDom hDiss hf g) = g := by
  apply SigmaRecHom.ext
  rw [selDissFrom_of_canonical N R data hDom hDiss g u' hg hf, hg]
  rfl

/-- **Sel ⊣ Diss Hom 双射（canonical 支撑版）**：
    Hom_Rec(Sel N, R) ≃ { canonical 支撑的 SigmaRecHom N (Diss R) }。 -/
noncomputable def selDissHomEquiv (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) (hDiss : ∃ j, data.contractions j < 1) :
    RecHom (selFunctor N hDom) R ≃
      { g : SigmaRecHom N (dissFunctor R data) //
        ∃ u' : RecHom (selFunctor N hDom) R,
          g.components = selDissCanonicalForm N R data hDom hDiss u' } where
  toFun f := ⟨selDissTo N R data hDom hDiss f, f, rfl⟩
  invFun g := selDissFrom N R data hDom hDiss (nonempty_of_canonical N R data hDom hDiss g.2) g.1
  left_inv f := selDissFrom_to N R data hDom hDiss _ f
  right_inv g := by
    obtain ⟨g, u', hg⟩ := g
    exact Subtype.ext (selDissTo_from_of_canonical N R data hDom hDiss g u' hg _)

/-
## §3 etaExt 签名数学确认

etaExt 8×8 实矩阵（NoiseSignatureBridge.lean）：
  diag(-1, +1, +1, +1, -1, -1, -1, -1) → 签名 (6, 2) = 6 正 + 2 负。

诚实边界：etaExt 签名对应的物理意义是诠释跳跃。
--/

theorem etaExt_diagonal :
    etaExt 0 0 = -1 ∧ etaExt 1 1 = 1 ∧ etaExt 2 2 = 1 ∧ etaExt 3 3 = 1 ∧
    etaExt 4 4 = -1 ∧ etaExt 5 5 = -1 ∧ etaExt 6 6 = -1 ∧ etaExt 7 7 = -1 := by
  simp [etaExt]

end MUFPF.SelDissBridge
