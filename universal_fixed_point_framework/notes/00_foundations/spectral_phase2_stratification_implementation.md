# 阶段 2 形式化实现：Sp 态射线性/静默分层

> **来源**：`spectral_category_scope_stratification.md` 阶段 2 任务。
> **日期**：2026-08-04
> **状态**：已完成（`lake build` 通过，零 sorry）
> **载体**：`formal_proof/UFPFormalization/UFPFormalization/NoiseCategory.lean` §18

---

## 1. 实现路径选择

路线图阶段 2 原文以 **Rec 层** 为主（定义 `RecLinHom` 为 `RecHom` 子类型）。实际实现选择 **Sp 层** 作为分层切入点，理由：

- D 的像在 Sp 层有具体刻画：`isTransferMatrix f := ∃ g, f.P = transferMatrix g`
- Rec 层"线性谱匹配映射"在有限维原型中等价于"经 D 映射后为转移矩阵"，二者通过 `DFunctor_image_is_transfer` 桥接
- Sp 层分层直接落地到 `Silence.lean` 的 `deltaSilence`（交换子 Frobenius 范数），物理诠释更直接

两者等价性：在有限维原型中，Rec_lin ↔ SpImD 通过 D functor 建立 1-1 对应（RAP5a 已闭合）。

## 2. 核心构造

### 2.1 态射分层结构

```lean
def isTransferMatrix {S T : SpObj} (f : S ⟶ T) : Prop :=
  ∃ (g : Fin S.n → Fin T.n), f.P = transferMatrix g

structure SpLinearHom (S T : SpObj) where
  hom : S ⟶ T
  is_transfer : isTransferMatrix hom

structure SpSilentHom (S T : SpObj) where
  hom : S ⟶ T
  is_not_transfer : ¬ isTransferMatrix hom
```

### 2.2 分层定理

- `spHom_stratify`：每个 SpHom 要么线性要么静默（排中律直接应用）
- `DFunctor_image_is_transfer`：D 的像落在线性层（构造性证明，witness = `equivFin ∘ f.toFun ∘ equivFin.symm`）

### 2.3 Σ-Rec / Σ-Spec 范畴实例

完成 `SigmaRecObj` 与 `SigmaSpObj` 的 `Category` 实例，关键设计：

- 态射 = `List (Σ j, Hom)` 的逐分量族（有限支撑，对应 coproduct 的"每列有限非零"约束）
- `id` = 每分量单元素列表 `[(⟨i, 𝟙 _⟩)]`
- `comp` = `flatMap` + `map` 实现矩阵乘法的列表版本
- `@[ext]` 属性 + `ext i` 策略闭合 `id_comp` / `comp_id` / `assoc`

辅助引理：
- `list_flatMap_singleton_eq_map`：`l.flatMap (fun a => [f a]) = l.map f`
- `list_map_flatMap'`：`(l.map f).flatMap g = l.flatMap (fun a => g (f a))`

### 2.4 Σ-D 函子

```lean
noncomputable def sigmaDFunctor : SigmaRecObj ⥤ SigmaSpObj where
  obj X := { components := fun i => Option.map DFunctor.obj (X.components i) }
  map f := { components := fun i => (f.components i).map (fun p => ⟨p.1, DFunctor.map p.2⟩) }
```

`map_id` / `map_comp` 通过 `ext i; simp` 闭合。

## 3. 静默桥接定理

### 3.1 线性层静默为零

```lean
theorem transfer_zero_silence {S : SpObj} (f : SpLinearHom S S) :
    deltaSilence S.A f.hom.P = 0
```

证明路径：`deltaSilence_eq_zero_iff` ↔ `ad f.hom.P S.A = 0` ↔ `f.hom.P * S.A - S.A * f.hom.P = 0`，由 `f.hom.intertwine : f.hom.P * S.A = S.A * f.hom.P` 直接给出。

### 3.2 静默层严格正（需非交换假设）

```lean
theorem silent_positive_silence {S : SpObj} (φ : SpSilentHom S S)
    (hA : S.A ≠ 0)
    (h_noncomm : φ.hom.P * S.A ≠ S.A * φ.hom.P) :
    deltaSilence S.A φ.hom.P > 0
```

**关键注释**：non-transfer **不蕴含** non-commuting。例如 `2·I` 是非转移矩阵但与任何 A 交换。`h_noncomm` 是正确的充分条件，不是 `is_not_transfer` 的推论。

证明采用反证法：δ ≤ 0 与 δ ≥ 0（`Real.sqrt_nonneg`）共同给出 δ = 0，由 `deltaSilence_eq_zero_iff` 推出 `ad = 0`，即 `P*A = A*P`，矛盾于 `h_noncomm`。

### 3.3 物理诠释

- 线性态射 = D 像内态射，δ = 0，与 A 交换（谱匹配成立）
- 静默态射 = D 像外态射，若额外不与 A 交换则 δ > 0（谱匹配失效）
- 静默态射中"与 A 交换但非转移"的子类（如标量倍单位阵）是边界态射，物理上对应"平凡噪声"

## 4. 溶解构造

```lean
noncomputable def dissSilent {S T : SpObj} (φ : SpSilentHom S T) : SigmaRecObj
```

将静默态射映射为 Σ-Rec 对象：单分量 `RecObj`（状态空间 `Fin S.n`，单位步）。这是阶段 3 IFS 分解的占位实现——完整版应将 `S.n` 维分解为局部线性片。

## 5. 与路线图的对应

| 路线图任务（阶段 2） | 实现状态 | 实现位置 |
|:--|:--|:--|
| 定义线性 Rec 态射子类型 | ✅（Sp 层等价实现） | `SpLinearHom` |
| 构造 inclusion functor | △（类型别名 `SpLinearCat`，完整 Category 实例待阶段 3） | `NoiseCategory.lean` L474 |
| Rec_silence 链接 Diss/Sel η 流 | ✅（`dissSilent` 占位，η 流已在 §17.5 定义） | `NoiseCategory.lean` L456 |
| `criticalNoiseThreshold` 语义升级 | △（注释已升级，形式化定义未改） | `NoiseCategory.lean` L333 |

## 6. 验证结果

- `lake build`：✅ 通过（2454 jobs，exit code 0）
- `NoiseCategory.lean` 零 sorry
- 仅余警告：其他文件（`HigherSpCategory.lean`、`SpectralFlowHomotopy.lean`、`DInfinityFunctor.lean`）的 unused simp 参数 lint，与本阶段无关

## 7. 阶段 3 衔接点

阶段 3（分形扩张）的入口已就绪：

1. `dissSilent` 升级为 IFS 分解：调用 `IFSFractal.lean` 的压缩映射族，将 `Fin S.n` 分解为局部线性片
2. `sigmaDFunctor` 已验证保持 coproduct（`sigmaD_preserves_coproduct`，§15.3）
3. `criticalNoiseThreshold` 从占位 `0` 改为 `min_i Δλ_i / ⟨δA_N⟩_i` 的实际计算

阶段 3 的前置依赖（有限维谱积分层）仍需评估 mathlib `ContinuousFunctionalCalculus` 的可用性。

## 8. 关联文件

| 文件 | 角色 |
|:--|:--|
| `formal_proof/.../NoiseCategory.lean` §18 | 阶段 2 主载体 |
| `formal_proof/.../SpCategory.lean` | SpObj / SpHom 基础定义 |
| `formal_proof/.../DecursionFunctor.lean` | D functor + `transferMatrix` |
| `formal_proof/.../AInfinityAlgebra.lean` | `ad`（交换子）定义 |
| `formal_proof/.../Silence.lean` | `deltaSilence` + `deltaSilence_eq_zero_iff` |
| `notes/00_foundations/spectral_category_scope_stratification.md` | 阶段规划（本笔记的前置） |
