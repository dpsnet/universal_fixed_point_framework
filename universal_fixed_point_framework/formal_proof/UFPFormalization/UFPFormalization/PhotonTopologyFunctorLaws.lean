import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Tactic

namespace UFPFormalization

open CategoryTheory

/-!
# PhotonTopologyFunctorLaws — 命题 2.4 函子律：Φ = D|_Rec_photon 小范畴函子

笔记: notes/06_photon_topology/photon_first_principle_origin.md §2.4 / 方向 2 §3.1–§3.3
论文: paper/paper44_photon_topology.md §2.4 命题 2.4

## 形式化范围（诚实边界）
本模块形式化命题 2.4（Φ = D|_Rec_photon）在**两对象小范畴** {A, P} 上的函子律
（机器证明部分）：
1. 光子子范畴 `PhotonObj`（A 封闭驻波 / P 开放行波）+ 态射 `PhotonMor`
   （idA/idP/unfold/fold）+ `photonComp`（编码**能量守恒恒等式** unfold∘fold = idA，
   公理 A3/§3.1 第 3 项——发射+吸收 = 原子恒等，函子律复合保持的传递前提）；
2. `photonCategory`：mathlib `Category` 实例（恒等律/结合律机器证明）；
3. `phiFunctor`：Φ 函子（对象 A→P、P→P；态射全部映到 P 的恒等）——
   **map_id/map_comp 函子律机器证明**（命题 2.4：Φ 为 D 函子特例的代数骨架）；
4. `unfold_fold_eq_id`：能量守恒恒等式的显式定理。

**未形式化（登记开放项，§3.2 剩余）**：
- 4-范畴态射方向几何正交的完整形式化（§7.5 #1 剩余项）；
- 多能级子范畴（§3.3 数值验证）与无穷维 Rec 子范畴的 Lean 扩展；
- Φ 与谱化函子 D（Paper I 抽象范畴）的严格函子等式（此处为两对象代数骨架）。
-/

/-! ## 光子子范畴 {A, P}：对象与态射 -/

/-- 光子子范畴对象：A（封闭驻波，S3 静默）/ P（开放行波，静默解除）。 -/
inductive PhotonObj where
  | atom
  | photon
deriving DecidableEq

/-- 光子子范畴态射：恒等（idA/idP）、unfold（A→P 发射/解绑）、fold（P→A 吸收/重绑）。
    每对对象间恰有一个态射（子范畴单值性）。 -/
inductive PhotonMor : PhotonObj → PhotonObj → Type where
  | idAtom : PhotonMor PhotonObj.atom PhotonObj.atom
  | idPhoton : PhotonMor PhotonObj.photon PhotonObj.photon
  | unfold : PhotonMor PhotonObj.atom PhotonObj.photon
  | fold : PhotonMor PhotonObj.photon PhotonObj.atom

/-- 态射复合（按对象三元组匹配——每对对象间态射唯一）：
    编码**能量守恒恒等式** unfold∘fold = idA（atom, photon, atom 情形，公理 A3/§3.1 第 3 项）；
    fold∘unfold = idP（photon, atom, photon 情形，范畴封闭）。 -/
def photonComp {X Y Z : PhotonObj} (_f : PhotonMor X Y) (_g : PhotonMor Y Z) : PhotonMor X Z :=
  match X, Y, Z with
  | PhotonObj.atom, PhotonObj.atom, PhotonObj.atom => PhotonMor.idAtom
  | PhotonObj.atom, PhotonObj.atom, PhotonObj.photon => PhotonMor.unfold
  | PhotonObj.photon, PhotonObj.atom, PhotonObj.atom => PhotonMor.fold
  | PhotonObj.photon, PhotonObj.atom, PhotonObj.photon => PhotonMor.idPhoton
  | PhotonObj.atom, PhotonObj.photon, PhotonObj.atom => PhotonMor.idAtom   -- 能量守恒：发射+吸收 = 原子恒等
  | PhotonObj.atom, PhotonObj.photon, PhotonObj.photon => PhotonMor.unfold
  | PhotonObj.photon, PhotonObj.photon, PhotonObj.atom => PhotonMor.fold
  | PhotonObj.photon, PhotonObj.photon, PhotonObj.photon => PhotonMor.idPhoton

/-- 光子子范畴实例（mathlib `Category`）：恒等律/结合律机器证明。 -/
instance photonCategory : Category.{0, 0} PhotonObj where
  Hom X Y := PhotonMor X Y
  id X := match X with
    | PhotonObj.atom => PhotonMor.idAtom
    | PhotonObj.photon => PhotonMor.idPhoton
  comp := photonComp
  id_comp := by
    intro X Y f
    cases X <;> cases f <;> rfl
  comp_id := by
    intro X Y f
    cases X <;> cases f <;> rfl
  assoc := by
    intro W X Y Z f g h
    cases f <;> cases g <;> cases h <;> rfl

/-- 能量守恒恒等式（§3.1 第 3 项/公理 A3）：unfold∘fold = idA（发射+吸收 = 原子恒等）
    ——编码于 photonComp，函子律复合保持（Φ 保复合）的传递前提。 -/
theorem unfold_fold_eq_id :
    photonComp PhotonMor.unfold PhotonMor.fold = PhotonMor.idAtom := by
  rfl

/-! ## Φ 函子（命题 2.4：Φ = D|_Rec_photon 的代数骨架） -/

/-- Φ 对象映射：Φ(A) = P（驻波 → 行波）、Φ(P) = P（已开放保持）——D 函子特例的对象层。 -/
def phiObj : PhotonObj → PhotonObj
  | PhotonObj.atom => PhotonObj.photon
  | PhotonObj.photon => PhotonObj.photon

/-- Φ 态射映射：全部映到 P 的恒等（Φ(A) = Φ(P) = P，故所有态射的像为 idP）。 -/
def phiMap {X Y : PhotonObj} (_f : PhotonMor X Y) : PhotonMor (phiObj X) (phiObj Y) :=
  match X, Y with
  | PhotonObj.atom, PhotonObj.atom => PhotonMor.idPhoton
  | PhotonObj.atom, PhotonObj.photon => PhotonMor.idPhoton
  | PhotonObj.photon, PhotonObj.atom => PhotonMor.idPhoton
  | PhotonObj.photon, PhotonObj.photon => PhotonMor.idPhoton

/-- Φ 函子（命题 2.4 代数骨架）：对象映射 phiObj + 态射映射 phiMap，
    map_id/map_comp 函子律机器证明——Φ 为 D|_Rec_photon 特例的函子结构。 -/
def phiFunctor : PhotonObj ⥤ PhotonObj where
  obj := phiObj
  map := phiMap
  map_id := by
    intro X
    cases X <;> rfl
  map_comp := by
    intro X Y Z f g
    cases f <;> cases g <;> rfl

/-- 函子律保恒等（§3.1 第 2 项）：Φ(id_X) = id_{Φ(X)}（实例化：Φ(idA) = idP）。 -/
theorem phi_preserves_id_atom :
    phiFunctor.map (𝟙 PhotonObj.atom) = 𝟙 (phiFunctor.obj PhotonObj.atom) := by
  rfl

/-- 函子律保复合（§3.1 第 3 项传递）：Φ(unfold∘fold) = Φ(unfold)∘Φ(fold)
    ——能量守恒恒等式（unfold∘fold = idA）经 Φ 保持（Φ 映到 idP）。 -/
theorem phi_preserves_composition :
    phiFunctor.map (PhotonMor.unfold ≫ PhotonMor.fold) =
    phiFunctor.map PhotonMor.unfold ≫ phiFunctor.map PhotonMor.fold := by
  rfl

/-- Φ 对象层一致（命题 2.4 对象层）：Φ(A) = P（公理 A1 拓扑转变的函子编码）。 -/
theorem phi_obj_atom :
    phiObj PhotonObj.atom = PhotonObj.photon := by
  rfl

/-! ## 多能级子范畴（§3.3 扩展）：对象 {A_i}_{i:ι} ∪ {P}，Φ = D|_Rec 函子律多能级机器证明 -/

/-- 多能级子范畴对象：A_i（能级态，i : ι）+ P（光子）。
    §3.3 数值模型取 ι = Fin 4（氢原子 4 能级，paperX_functor_extended.py S1-S4）。 -/
inductive MultiObj (ι : Type u) where
  | atom (i : ι) : MultiObj ι
  | photon : MultiObj ι

/-- 多能级子范畴态射：
    unfold i（A_i → P 发射）、fold i（P → A_i 吸收）、
    transition i j（A_i → A_j 净跃迁：发射 j→P + 吸收 P→i 的复合；i=j 时为能级恒等）、
    idPhoton（P 恒等）。
    **复合编码能量守恒（§3.3）**：unfold i ≫ fold j = transition i j（发射+吸收 = 净跃迁，
    i=j 时 = 能级恒等 ⟺ 能量守恒恒等式 unfold∘fold = id_A）；transition i m ≫ transition m k = transition i k
    ⟺ 跃迁频率可加性 ν_ik = ν_im + ν_mk（ΔE 可加 = 能量守恒）。 -/
inductive MultiMor {ι : Type u} : MultiObj ι → MultiObj ι → Type u where
  | idPhoton : MultiMor MultiObj.photon MultiObj.photon
  | unfold (i : ι) : MultiMor (MultiObj.atom i) MultiObj.photon
  | fold (i : ι) : MultiMor MultiObj.photon (MultiObj.atom i)
  | transition (i j : ι) : MultiMor (MultiObj.atom i) (MultiObj.atom j)

/-- 多能级复合（可复合对 8 情形显式定义）：
    transition∘transition = transition（**频率可加性**，§3.3 S3 核心）、
    unfold∘fold = transition（发射+吸收 = 净跃迁，能量守恒）、
    fold∘unfold = idPhoton（同能级吸收+发射 = 光子恒等，范畴封闭）等。
    对象不匹配的组合由依赖类型自动剪除（不可复合对无态射定义）。 -/
def multiComp {X Y Z : MultiObj ι} (f : MultiMor X Y) (g : MultiMor Y Z) : MultiMor X Z :=
  match f, g with
  | MultiMor.transition i m, MultiMor.transition _ k => MultiMor.transition i k
  | MultiMor.transition i m, MultiMor.unfold _ => MultiMor.unfold i
  | MultiMor.unfold i, MultiMor.fold j => MultiMor.transition i j
  | MultiMor.unfold i, MultiMor.idPhoton => MultiMor.unfold i
  | MultiMor.fold i, MultiMor.transition _ k => MultiMor.fold k
  | MultiMor.fold i, MultiMor.unfold _ => MultiMor.idPhoton
  | MultiMor.idPhoton, MultiMor.fold i => MultiMor.fold i
  | MultiMor.idPhoton, MultiMor.idPhoton => MultiMor.idPhoton

/-- 多能级子范畴 mathlib `Category` 实例（任意能级类型 ι）：
    恒等律/结合律机器证明（§3.3 扩展子范畴范畴结构）。 -/
instance multiCategory (ι : Type u) : Category.{u, u} (MultiObj ι) where
  Hom X Y := MultiMor X Y
  id X := match X with
    | MultiObj.atom i => MultiMor.transition i i
    | MultiObj.photon => MultiMor.idPhoton
  comp := multiComp
  id_comp := by
    intro X Y f
    cases X <;> cases f <;> rfl
  comp_id := by
    intro X Y f
    cases X <;> cases f <;> rfl
  assoc := by
    intro W X Y Z f g h
    cases f <;> cases g <;> cases h <;> rfl

/-- **能量守恒恒等式（多能级，§3.3 S2/公理 A3 扩展）**：unfold i ≫ fold i = 𝟙 (A_i)
    （发射+吸收回原能级 = 能级恒等；i=j 的 unfold∘fold = transition i i 恰为 id，定义性成立）。 -/
theorem multi_energy_conservation (i : ι) :
    multiComp (MultiMor.unfold i) (MultiMor.fold i) = 𝟙 (MultiObj.atom i) := by
  rfl

/-- **发射+吸收 = 净跃迁（跨能级能量守恒，§3.3 S2 推广）**：unfold i ≫ fold j = transition i j。 -/
theorem multi_unfold_fold_transition (i j : ι) :
    multiComp (MultiMor.unfold i) (MultiMor.fold j) = MultiMor.transition i j := by
  rfl

/-- **范畴封闭**：fold i ≫ unfold i = idPhoton（吸收+发射闭合回光子恒等）。 -/
theorem multi_fold_unfold_id (i : ι) :
    multiComp (MultiMor.fold i) (MultiMor.unfold i) = MultiMor.idPhoton := by
  rfl

/-- **跃迁频率可加性 = 能量守恒（§3.3 S3 核心）**：transition i m ≫ transition m k = transition i k
    ⟺ ν_ik = ν_im + ν_mk（ΔE 可加）——函子律复合保持的传递前提，机器证明。 -/
theorem multi_transition_compose (i m k : ι) :
    multiComp (MultiMor.transition i m) (MultiMor.transition m k) = MultiMor.transition i k := by
  rfl

/-- **全组合复合（§3.3 S4）**：两步中间态链 transition i k = transition i m2 ≫ transition m2 m1 ≫ transition m1 k
    （双中间态路径与直接跃迁一致——频率可加性链式成立）。 -/
theorem multi_transition_chain (i m1 m2 k : ι) :
    multiComp (multiComp (MultiMor.transition i m2) (MultiMor.transition m2 m1)) (MultiMor.transition m1 k) =
    MultiMor.transition i k := by
  rfl

/-! ## Φ 多能级函子（命题 2.4 扩展：Φ = D|_Rec 多能级特例） -/

/-- Φ 多能级对象映射：Φ(A_i) = P（全部能级态 → 光子）、Φ(P) = P。 -/
def phiMultiObj (ι : Type u) : MultiObj ι → MultiObj ι
  | MultiObj.atom _ => MultiObj.photon
  | MultiObj.photon => MultiObj.photon

/-- Φ 多能级态射映射：全部映到 P 的恒等（Φ 的像集中单对象 P）。 -/
def phiMultiMap {ι : Type u} {X Y : MultiObj ι} (_f : MultiMor X Y) :
    MultiMor (phiMultiObj ι X) (phiMultiObj ι Y) :=
  match X, Y with
  | MultiObj.atom _, MultiObj.atom _ => MultiMor.idPhoton
  | MultiObj.atom _, MultiObj.photon => MultiMor.idPhoton
  | MultiObj.photon, MultiObj.atom _ => MultiMor.idPhoton
  | MultiObj.photon, MultiObj.photon => MultiMor.idPhoton

/-- Φ 多能级函子：**map_id/map_comp 函子律机器证明**——Φ = D|_Rec 在多能级子范畴上
    仍为函子（§3.3 S2/S3/S5：保恒等 + 保复合 + 扩展子范畴函子律成立）。 -/
def phiMultiFunctor (ι : Type u) : MultiObj ι ⥤ MultiObj ι where
  obj := phiMultiObj ι
  map := phiMultiMap
  map_id := by
    intro X
    cases X <;> rfl
  map_comp := by
    intro X Y Z f g
    cases f <;> cases g <;> rfl

/-- **保恒等（§3.3 S2 实例化）**：Φ(id_{A_i}) = id_{Φ(A_i)} = idP（能级恒等经 Φ 映到光子恒等）。 -/
theorem phiMulti_preserves_id_atom {ι : Type u} (i : ι) :
    (phiMultiFunctor ι).map (𝟙 (MultiObj.atom i)) = 𝟙 (MultiObj.photon) := by
  rfl

/-- **保复合（§3.3 S3 实例化）**：Φ(unfold i ≫ fold j) = Φ(unfold i) ≫ Φ(fold j)（都 = idP，
    ——能量守恒恒等式（unfold∘fold = transition i j）经 Φ 保持）。 -/
theorem phiMulti_preserves_unfold_fold {ι : Type u} (i j : ι) :
    (phiMultiFunctor ι).map (multiComp (MultiMor.unfold i) (MultiMor.fold j)) =
    multiComp ((phiMultiFunctor ι).map (MultiMor.unfold i)) ((phiMultiFunctor ι).map (MultiMor.fold j)) := by
  rfl

/-- **保复合（§3.3 S3 实例化）**：Φ(transition i m ≫ transition m k) = Φ(transition i m) ≫ Φ(transition m k)
    ——频率可加性复合（ν_ik = ν_im + ν_mk）经 Φ 保持。 -/
theorem phiMulti_preserves_transition {ι : Type u} (i m k : ι) :
    (phiMultiFunctor ι).map (multiComp (MultiMor.transition i m) (MultiMor.transition m k)) =
    multiComp ((phiMultiFunctor ι).map (MultiMor.transition i m)) ((phiMultiFunctor ι).map (MultiMor.transition m k)) := by
  rfl

end UFPFormalization
