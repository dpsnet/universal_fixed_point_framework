# 范畴论圈定与兼容性扩张规划

> **来源**：R11 态射层语义分岔（`spectral_R11_morphism_layer.md` §8）的后续推进。
> 对应 P1 线性语义裁决后的理论圈定与分层扩张需求。
>
> **日期**：2026-08-04
> **状态**：规划草案（阶段 1 圈定 ✅、阶段 2 分层 ✅、**RAP5a RIm_map 闭合 ✅（2026-08-04）**）

---

## 1. 问题背景

### 1.1 语义分岔

`spectral_R11_morphism_layer.md` §8 裁决：D ⊣ R 伴随的闭合取决于 Rec 态射语义。

| 语义 | 谱匹配双射 | 伴随闭合 | S0 静默地位 |
|:--|:--|:--|:--|
| **线性**（Rec_D 态射 = 有界线性谱匹配算子） | ✅ 成立（恒等双射） | ✅ 无限维闭合 | 仅有限维伪影 |
| **集合**（Rec_D 态射 = 连续映射，即 `RecHom.toFun`） | ❌ 不成立 | ❌ 结构性不可闭合 | 结构性普遍现象 |

推荐裁决：采用**线性语义**作无限维闭合路径。但这引入两个张力：

- **张力 A**：S0 静默从"结构性现象"降为"有限维伪影"——静默理论的物理基础需重新审视。
- **张力 B**：非线性分形函数被排除在 D ⊣ R 伴随范围外——分形-谱对应路径需另构造。

### 1.2 安全性核查

D ⊣ R 伴随（`DAdjR`/`adjUnit`/`adjCounit`）在整个形式化框架中是**孤立的**：

- 仅出现在 `Adjunction.lean`（定义）、`RAP5a_explicit_adjunction.lean`（SpImD 修复）、`InfinityReflection.lean`（独立无限维版本）、`TestCategoryTheory.lean`（存在性测试）。
- **没有任何物理定理依赖 D ⊣ R 伴随的全范围声明。** 强子质量谱、β 函数、CHSH、引力偏差等全部使用 D functor 的对象映射和有限维矩阵代数。

因此，圈定 D ⊣ R 伴随的有效范围**不影响任何已有物理结论**。

---

## 2. 理论圈定：当前层的有效范围

### 2.1 显式声明

**D ⊣ R 伴随的有效范围 = Rec_lin(SpImD)**，其中：

- **Rec_lin**：Rec 范畴中态射为线性谱匹配映射的满子范畴
  - 有限维：转移矩阵（`transferMatrix : (T → T) → Matrix`，已是线性算子）
  - 无限维：有界线性算子 $f \in \mathcal{L}(\mathcal{H}_E, \mathcal{H}_S)$ 满足 $f \circ e^{-A_E} = e^{-A_S} \circ f$
- **SpImD**：D 的像子范畴 = $\{(\text{src}, \text{tgt}, \text{Iso}(D(\text{src}), \text{tgt}))\}$（RAP5a 已定义）

在此范围内：
- 谱匹配双射 = 恒等映射（定理 3，Agda T3 已形式化）
- 左三角恒等式：`refl` 闭合（Agda 已证）
- 右三角恒等式：线性语义下可证（Agda `postulate`，依赖 T3 谱定理公理）
- Fuglede 方向：已降为可证定理（Agda §5g）

### 2.2 论文层限定修正

需在以下位置显式注明限定：

- **Paper I 定理 C2.3**（态射对应断言）：注明"受限态射层 = 线性连续谱匹配映射"
- **Paper I 定理 2.4.5**（伴随构造）：注明"D ⊣ R 伴随在 SpImD 上严格成立"
- **Paper XIX 定理 13.1**（三层伴随嵌套）：注明每层的有效态射层

这是 P0（论文层范围修正）的姊妹修正，不改变任何定理的数学内容，只显式化有效范围。

### 2.3 形式化层对应

| 形式化层 | 当前状态 | 圈定后状态 |
|:--|:--|:--|
| `Adjunction.lean` DAdjR | `axiom`（全 Rec 声明） | ✅ SpImD 上的构造（RAP5a `DImAdjRIm`，2026-08-04 闭合） |
| `Adjunction.lean` adjUnit | ✅ 已移植（常零函数，§4） | 保持 |
| `Adjunction.lean` adjCounit | ✅ 已移植（零矩阵，§4） | 保持 |
| `RAP5a` RIm_map | ✅ 已闭合（2026-08-04） | 线性语义下 = 恒等提取（SpImD 上） |
| `RAP5a` DAdjR_SpImD | ✅ 已构造（`DImAdjRIm`） | SpImD 上的完整伴随（对象层 + 态射层均闭合） |

---

## 3. 兼容性扩张：静默与分形的分层路径

### 3.1 范畴分层结构

```
Rec_set（集合语义：连续映射）
  ├── Rec_lin（线性语义：有界线性算子）← D ⊣ R 伴随在此闭合
  └── Rec_silence（静默态射：非线性谱匹配映射）← 不在伴随范围内
        ↑
    通过 Diss/Sel η 流参数化与 Rec_lin 关联
```

- **Rec_lin 是 Rec_set 的满子范畴**（wide subcategory）：线性映射是特殊的连续映射
- **Rec_silence = Rec_set \ Rec_lin**：满足交换条件但不满足线性条件的谱匹配映射
- **inclusion functor** $I : \text{Rec\_lin} \hookrightarrow \text{Rec\_set}$：忠实 functor

### 3.2 静默的重新定位

**当前**：S0 静默 = "结构性普遍现象"（集合语义下，跨维度存在）

**圈定后**：S0 静默 = "Rec_lin 与 Rec_set 边界上的层间现象"

具体地：
- 在 Rec_lin 内：静默 = 0（线性谱匹配映射必在 SpImD 的像中，无静默）
- 在 Rec_silence 中：静默态射 = 满足 $f \circ e^{-A_E} = e^{-A_S} \circ f$ 但非线性的连续映射
- 静默的出现 = Rec_lin 的"线性近似"失效点，可通过 η 流参数化

**物理诠释**：静默不是"被否定"，而是被**定位**——它是线性谱框架的边界标识，标示了非线性效应（分形、噪声）进入的临界点。这与 `criticalNoiseThreshold`（NoiseCategory §17.5, η_c）的概念一致。

### 3.3 分形的扩张路径

非线性分形函数（Weierstrass、Cantor 等）不满足线性条件，不在 Rec_lin 中。扩张路径：

**路径：IFS 分解 → Σ-Rec coproduct → 线性片的组合**

1. **IFS 分解**（`IFSFractal.lean` + `HutchinsonAttractor.lean` 已有基础设施）：
   - 分形函数 $f$ 通过 IFS 吸引子分解为局部线性片 $\{f_i\}_{i \in I}$
   - 每片 $f_i$ 在局部尺度上是线性的（压缩仿射映射）

2. **Σ-Rec 编码**（`NoiseCategory.lean` §15 已有定义）：
   - 分形 = ⨁_{i∈I} R_i，每个 R_i ∈ Rec_lin
   - Σ-Rec = Rec 的 countable coproduct cocompletion

3. **Diss/Sel 伴随**（`NoiseCategory.lean` §17 已有定义）：
   - Diss : Rec × NoiseData → Σ-Rec（溶解为噪声 coproduct）
   - Sel : Σ-Rec → Rec（选取主分量）
   - η 流参数化：η = 0 纯线性，η → ∞ 纯噪声

4. **谱对应**：
   - D 在每片 R_i 上保持线性谱对应
   - 整体谱 = 各片谱的 coproduct（σ_D(⨁ R_i) = ⨁ σ_D(R_i)）
   - 分形的谱性质（如 Weierstrass 函数的谱隙）从 IFS 压缩比导出

**关键**：这不需要 D ⊣ R 伴随在全 Rec 上成立——分形的谱对应走"局部线性 + 全局 coproduct"路径，不经过右三角恒等式。

### 3.4 与现有形式化的兼容性

| 现有组件 | 在分层中的角色 | 需要修改 |
|:--|:--|:--|
| `NoiseCategory.lean` Σ-Rec | Rec_silence 的载体 | 无（已为此设计） |
| `NoiseCategory.lean` Diss/Sel | Rec_lin ↔ Rec_silence 的桥 | 无（η 流已定义） |
| `NoiseCategory.lean` η_c | 静默出现的临界点 | 语义升级：从"噪声阈值"到"线性层边界" |
| `IFSFractal.lean` | 分形 IFS 分解 | 无（已有基础设施） |
| `Silence.lean` | S0 静默形式化 | 诠释更新：从"结构性现象"到"层间现象" |
| `Adjunction.lean` DAdjR | Rec_lin 上的伴随 | 圈定到 SpImD |
| `RAP5a` SpImD | Rec_lin 的形式化载体 | RIm_map 改为恒等构造 |

---

## 4. 阶段规划

### 阶段 1：圈定（可立即执行）

**目标**：显式声明 D ⊣ R 伴随的有效范围，消除孤立 sorry

**任务**：
1. 移植 Agda 的 `adjUnit`（常零函数）和 `adjCounit`（零矩阵）构造到 `Adjunction.lean`，消除 3 处 sorry
2. 将 `RAP5a` 的 `RIm_map` 从 `sorry` 改为 SpImD 上的恒等构造（线性语义），消除 1 处 sorry
3. 将 `DAdjR` 从全 Rec 上的 `sorry` 改为 SpImD 上的构造（或 `axiom` 注明谱定理依赖），消除 1 处 sorry
4. 在 `Adjunction.lean` 顶部注释中显式声明有效范围

**验证**：`lake build` 全量通过，零 sorry

**风险**：无（已确认无物理定理依赖 DAdjR 全范围）

### 阶段 2：分层（依赖阶段 1）— ✅ 已完成（2026-08-04）

**目标**：形式化 Rec_lin / Rec_silence 的子范畴结构

**任务**：
1. 在 Lean 中定义 `RecLinHom`（线性 Rec 态射）为 `RecHom` 的子类型
2. 构造 inclusion functor `Rec_lin ⥤ Rec`
3. 在 `NoiseCategory.lean` 中将 Rec_silence 链接到 Diss/Sel 的 η 流
4. 将 `criticalNoiseThreshold` 的诠释从"噪声阈值"升级为"线性层边界"

**验证**：子范畴构造编译通过，inclusion functor 满足 functor laws

**产出**：
- 实现笔记：`notes/00_foundations/spectral_phase2_stratification_implementation.md`
- 形式化载体：`formal_proof/UFPFormalization/UFPFormalization/NoiseCategory.lean` §18
- `lake build` 通过（2454 jobs，零 sorry）

**关键结果**：
- 选择 **Sp 层** 作为分层切入点（等价于 Rec 层，但 D 的像在 Sp 层有具体刻画 `isTransferMatrix`）
- 态射分层结构：`SpLinearHom` / `SpSilentHom` + 分层定理 `spHom_stratify`
- 静默桥接定理：`transfer_zero_silence`（δ=0）+ `silent_positive_silence`（δ>0，需 `h_noncomm` 假设）
- Σ-Rec / Σ-Spec 范畴实例完成（`@[ext]` + 列表 flatMap/map 实现 component-wise composition）
- Σ-D 函子 `sigmaDFunctor` 完成，保持 coproduct（§15.3）

**遗留**（阶段 3 衔接）：
- `SpLinearCat` 当前为类型别名，完整 `Category` 实例待阶段 3
- `dissSilent` 为占位实现，阶段 3 升级为 IFS 分解
- `criticalNoiseThreshold` 形式化定义待阶段 3 升级

### 阶段 3：扩张（依赖阶段 2 + 有限维谱积分层）

**目标**：分形函数的谱对应走"局部线性 + coproduct"路径

**任务**：
1. 桥接 `IFSFractal.lean` 的 IFS 分解到 `NoiseCategory.lean` 的 Σ-Rec
2. 构造分形 → Σ-Rec 的编码（每片 = Rec_lin 对象）
3. 证明 D 在 Σ-Rec 上保持 coproduct（σ_D(⨁ R_i) = ⨁ σ_D(R_i)，已有 §15.3 定理）
4. 将 Weierstrass/Cantor 函数的谱性质从 IFS 压缩比导出

**验证**：至少 1 个分形函数（Weierstrass）的谱隙从 IFS 参数导出

**进度（2026-08-05）**：
- ✅ **子任务 1（数值层）**：`paperX_ifs_sigma_rec_spectral.py`（7/7 检查，已注册 `run_all_tests.py`）+ 笔记 `spectral_phase3_fractal_expansion.md`（v0.2）——Σ-Rec coproduct 谱保持（S3）、Cantor 谱有效秩随维数单调（S4）、**Weierstrass 谱隙从 IFS 参数导出（S5，验证目标命中，gap: 0.0142→0.0043 vs d: 0.904→1.904）**；
- ✅ **子任务 2（Lean 符号编码，v0.2）**：`IFSRecCoding.lean`（`lake build` 通过，零 `sorry`）——`symbolicRecObj`（符号动力学 RecObj，左移补 0 步进）、`symbolicSlice`（局部线性片）、**`symbolicSigmaRecObj`（正式 `SigmaRecObj` coproduct 编码，替代 v0.1 自包含 `CoproductObj`）**、**`symbolicSliceInjection`（片注入态射 `SigmaRecHom`）**、`symbolicStep_fixedPoint_iff`（唯一不动点 = 全零，完整等价：谱障碍 tr = #Fix = 1 的符号层实例）；
- ⏳ 子任务 3-4：D 保持 coproduct 的 Lean 侧 + Weierstrass 谱隙的 Lean 命题（依赖有限维谱积分层）；
- ✅ **障碍清除（2026-08-05）**：`NoiseCategory.lean` 既有编译错误**全部闭合**（`lake build` 3172 jobs 通过，零 `sorry`）——Σ-Rec/Σ-Spec Category 律、`sigmaRecInclusion`（map 语义修正 + `Faithful` 诚实修正，`Full` 在无约束 Hom 下不成立）、`Inhabited SpObj` 对齐、Σ-D 对象-态射层构造（`sigmaDFunctorObj`/`sigmaDFunctorMap`/`sigmaD_preserves_coproduct`）。残余：Σ-D 的 Functor 律（`map_id`/`map_comp`）因类型转换 cast 暂以函数层承载（诚实边界）。

**依赖**：mathlib `ContinuousFunctionalCalculus` 桥接（有限维谱积分层）

### 阶段 4：统一（长期）

**目标**：静默 = η > η_c 时 Diss 产物的范畴论刻画

**任务**：
1. 在 Σ-Rec 上构造"谱静默函子"：η > η_c 时 Diss 产物的谱连续化
2. 将 S0 静默的物理诠释统一为"线性层边界现象"
3. 更新 `Silence.lean` / `SilenceHierarchy.lean` 的形式化以反映分层诠释

**验证**：静默的范畴论刻画与已有数值结果（`paperX_silence_dimensions.py` 等）一致

**依赖**：无限维谱定理（mathlib 社区前沿）

---

## 5. 与已有路线图的对接

| 路线图条目 | 当前状态 | 本规划对接 |
|:--|:--|:--|
| P0（论文层范围修正） | 待执行 | 阶段 1 的论文层限定是 P0 的姊妹修正 |
| T3 测度论完整层 | 唯一剩余 D 类桥接，P0 级 | 阶段 3 的前置依赖（有限维桥接可先行） |
| S0 R11 无限维验证 | "有限维结构性障碍"，P1 级 | 阶段 1 将"障碍"重新定性为"圈定"，阶段 2-4 分层扩张 |
| spExchangeLaw | 偏差 = 谱隙引力起源，已闭合 | 不受影响（2-范畴层面，独立于 1-范畴圈定） |

---

## 6. 关联文件索引

| 文件 | 角色 |
|:--|:--|
| `notes/00_foundations/spectral_R11_morphism_layer.md` | P1 语义分岔裁决（本规划的前置） |
| `notes/00_foundations/spectral_T3_analysis_foundation.md` | T3 谱定理层规划 |
| `notes/00_foundations/spectral_noise_category.md` | Σ-Rec / Diss / Sel 框架 |
| `notes/00_foundations/spectral_representation_silence.md` | S0 静默理论 |
| `formal_proof/.../Adjunction.lean` | D ⊣ R 伴随定义（阶段 1 修改对象） |
| `formal_proof/.../RAP5a_explicit_adjunction.lean` | SpImD 子范畴方案（阶段 1 修改对象） |
| `formal_proof/.../NoiseCategory.lean` | Σ-Rec / Diss / Sel（阶段 2-3 载体） |
| `formal_proof/.../IFSFractal.lean` | IFS 分解基础设施（阶段 3 依赖） |
| `agda_formalization/DecursionFunctor/DecursionFunctor.agda` | Agda 侧 adjUnit/adjCounit/right-triangle（阶段 1 移植源） |
| `agda_formalization/SpectralTheory/SpectralTheory.agda` | T3 谱定理公理化（阶段 3-4 参考） |
| `roadmap/phase60_category_verification.md` | 范畴验证路线图 |
| `roadmap/phase61_physics_advancement.md` | 物理推进路线图（L186 S0 R11 条目需更新） |
