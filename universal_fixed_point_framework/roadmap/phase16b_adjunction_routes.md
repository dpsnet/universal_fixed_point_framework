# Phase 16B 规划文档 — 广义 MUFPF 伴随 + 粗粒化并行路线

**日期**：2026-11-06
**状态**：规划阶段（未启动）
**前置依赖**：RAP5a_explicit_adjunction.lean 伴随边界定理链已机检，AdjunctionAnchor.lean Universe 诚实边界已登记

---

## 0. 立项背景与时机

本轮 Lean 形式化（S422-S425）完成了以下关键锚：

| 锚 | 状态 | 来源 |
|---|---|---|
| `DIm_full` / `DIm_faithful`（SpImD 层 full + faithful） | ✅ theorem，已机检 | RAP5a §6 |
| `no_global_right_adjoint`（全范畴无右伴随） | ✅ theorem，已机检 | RAP5a §9 |
| `DImAdjRIm`（SpImD 受限伴随存在） | ✅ theorem，已机检 | RAP5a §7 |
| SpImD 唯一性骨架 + Universe 诚实边界 | 📝 登记注释 | AdjunctionAnchor §1-2 |
| MeasurementAlgebra.lean（H6' 步骤 1-2） | ✅ 全 theorem，0 sorry | MeasurementAlgebra |

核心发现：**当前 Lean 原型（集合语义 Fintype 层）的伴随不存在，是 Rec/Sp 两边 Hom 集基数不兼容（有限 vs 不可数）的直接推论**。不是理论缺陷，是**尺度选择导致的边界**。

本阶段目标：**在广义 MUFPF 层（线性语义 + 无限维）或粗粒化层（有限截断）上恢复伴随存在性**，并正式登记两条可并行的路线。

---

## 1. 问题的精确结构

### 1.1 当前 Lean 原型的伴随边界

| 层级 | Rec 对象 | Sp 对象 | Rec Hom | Sp Hom | D⊣R |
|---|---|---|---|---|---|
| 当前 Lean | `RecObj`（Fintype + step） | `SpObj`（有限复矩阵） | **有限**（`k^m`） | **不可数**（`ℂ^n`） | ❌ 不可能 |
| SpImD 子范畴 | 同上 | 显式带 `conn : Iso(D src) tgt` | **有限**（= RecHom） | **有限**（SpImDMor.hom = RecHom） | ✅ 已机检 |

### 1.2 广义 MUFPF（Paper I 设计）的目标结构

| 层级 | Rec 对象 | Sp 对象 | Rec Hom | Sp Hom | D⊣R |
|---|---|---|---|---|---|
| 广义 MUFPF | Polish 空间 + 线性谱匹配态射 | Hilbert 算子 | **无限**（线性算子空间） | **无限**（线性算子空间） | ✅ 可能（Paper I 设计） |

关键：**两边都无限 → 基数矛盾消失 → 伴随可构造**。

### 1.3 粗粒化层（用户截断-精度对偶 M1 的实现）

| 层级 | Rec 对象 | Sp 对象 | Rec Hom | Sp Hom | D⊣R |
|---|---|---|---|---|---|
| 粗粒化层 | `RecObj`（不变） | `SpObj / ~`（按精度截断到有限类） | **有限** | **有限**（商后） | ✅ 可能 |

关键：**两边都有限 → 基数矛盾消失 → 伴随可构造**。粗粒化尺度由实验精度给出，不是手放的——这正是用户 M1 "截断-精度对偶"的数学实现。

---

## 2. 两条并行路线

### 路线 P：Polish 空间 + 线性谱匹配态射（Paper I 直接实现）

**改动范围**：RecCategory 升级（主要改动）+ SpCategory 升级（次要）+ DFunctor 升级 + 伴随构造

**详细步骤**：

| 步骤 | 模块 | 工作量 | 依赖 |
|---|---|---|---|
| P-1: SpObj 升级 universe-polymorphic | SpCategory.lean | 小（改 `structure SpObj` 加 universe 参数） | 无 |
| P-2: RecObj 升级为 PolishRecObj | RecCategory.lean 新结构 | 中 | Mathlib 的 PolishSpace / Measurable 结构 |
| P-3: DFunctor 升级 universe-polymorphic | DecursionFunctor.lean | 小（签名改动） | P-1, P-2 |
| P-4: D_gen 构造为 Koopman 算子 | 新模块 | 大 | Mathlib 的 Unitary / GroupHom / L2 空间 |
| P-5: R_gen（余伴随）构造 | 新模块 | 大 | Hille-Yosida（Agda postulate #6） |
| P-6: 三角恒等式机检 | 新模块 | 大 | Fuglede 定理（Agda postulate #4）、sup-comm（#11） |

**依赖项清单（Agda 11 postulate 需先降 theorem）**：

| Agda postulate | 名称 | Lean 依赖 | 用途 |
|---|---|---|---|
| #1 | spectral-rep-A | Mathlib spectral theorem（已存在） | 谱表示 |
| #2 | spectral-rep-B | Mathlib 有限维 spectral（已存在） | 有限维谱表示 |
| #3 | Fuglede 定理 | Mathlib Fuglede（已存在） | 算子谱性质 |
| #4 | Fuglede B | Mathlib Fuglede（已存在） | 同上 |
| #5 | Hille-Yosida 生成定理 | **Mathlib 无——需补** | Koopman 算子余伴随 |
| #6 | Hille-Yosida B | 同上 | 同上 |
| #7 | sup-comm | **Mathlib 无——需补** | 算子交换子性质 |
| #8 | von-Neumann 谱表示 | Mathlib spectral theorem | 算子谱性质 |
| #9 | Gelfand-Naimark | Mathlib C\*-algebra | 代数表示 |
| #10 | Borel 函数演算 | Mathlib BorelFuncCalc（已存在） | 函数演算 |
| #11 | sup-comm B | 同 #7 | 同上 |

**风险点**：
- Hille-Yosida 是实分析 + 泛函分析的大 theorem，Mathlib 需要大量前置建设
- Fuglede 定理已存在但应用到 Hilbert 算子需要 Hilbert 算子理论已建立
- 工作量估计：中（3-6 个月，需要大量新 Mathlib 组件）

**预期产出**：广义 MUFPF 层的 D_gen ⊣ R_gen 伴随存在定理，与 Lean 当前原型的 DIm ⊣ RIm 形成层间桥接。

---

### 路线 B：Sp 粗粒化商范畴（用户截断-精度对偶 M1）

**改动范围**：新建 SpCrudeCategory 模块（主要改动，RecCategory 不变）

**详细步骤**：

| 步骤 | 模块 | 工作量 | 依赖 |
|---|---|---|---|
| B-1: SpCrudeObj 定义 | 新模块 SpCrudeCategory.lean | 小（`structure SpCrudeObj where n : ℕ; class_id : Fin k`） | SpCategory |
| B-2: 粗粒化等价关系 ~ 定义 | 同 B-1 | 中（`def spCrudeEquiv : SpObj → SpObj → Prop`） | SpCategory |
| B-3: SpCrudeCategory 构造 | 同 B-1 | 中（范畴实例 + Hom 集定义 = RecHom） | B-1, B-2 |
| B-4: DCrude : RecObj ⥤ SpCrudeObj | 同 B-1 | 小（D obj → SpCrude obj 通过粗粒化） | DFunctor, B-1 |
| B-5: RCrude : SpCrudeObj ⥤ RecObj 构造 | 同 B-1 | 中（投影到 src 字段——SpCrudeObj 需携带身份标记） | B-3, DImAdjRIm |
| B-6: DCrude ⊣ RCrude 三角恒等式机检 | 同 B-1 | 中（利用 SpCrudeObj 身份标记 → 类似 SpImD 情况） | B-5 |

**物理对应**：

| 数学 | 物理 |
|---|---|
| `SpCrudeObj.class_id : Fin k` | 粗粒化后的有限个可分辨类 |
| `spCrudeEquiv` 的分辨率参数 | 实验精度 Δα⁻¹ |
| `k` 的上限 | 全态 16 = 可分辨的最大类数 |
| 粗粒化尺度 ~ 实验精度 | 用户 M1 "截断-精度对偶" 的数学实现 |

**风险点**：
- 粗粒化等价关系的定义需要物理输入（"两个谱态射在什么精度下不可分辨"）——这是诠释层选择
- SpCrudeObj 需携带身份标记（类似 SpImD 的 src + conn），否则 DCrude 无法 full
- 粗粒化尺度的**内生化**（从框架结构推出 Δ）是开放问题

**工作量估计**：小-中（2-3 周，主要是定义和三角恒等式机检）

**预期产出**：粗粒化层的 DCrude ⊣ RCrude 伴随存在定理，作为当前 Lean 原型和广义 MUFPF 层之间的中间桥接层。

---

### 路线等价性（登记探索点）

路线 P 和路线 B 在数学上可能等价：

> Polish 路线在某种**紧化/截断**下的有限部分 ≌ 粗粒化路线的有限商范畴

如果这个等价性成立，那么广义 MUFPF 其实有两条通向伴随存在的路线，而这两条路线在物理上对应同一个核心思想——截断、精度、有限维近似。

探索计划：
1. 从 B-3 开始，先构建 SpCrudeCategory（2-3 周）
2. 同时启动 P-1（SpObj universe 升级，1-2 天）
3. 在 B-6 和 P-2 完成后，检查 SpCrudeObj 是否可以嵌入 PolishRecObj 的有限截断部分
4. 如果嵌入成立，等价性证明方向明确；如果不成立，两条路线各自独立推进

---

## 3. Universe-polymorphic SpObj 升级（两条路线的共同前置）

**当前问题**：

```lean
-- SpCategory.lean L31
structure SpObj where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ
```

SpObj 固定 Type 0（n : ℕ 无 universe 参数），但 RecObj 是 universe-polymorphic：

```lean
-- RecCategory.lean L23-30
universe u
structure RecObj where
  T : Type u
  fin : Fintype T
  dec : DecidableEq T
  step : T → T
```

这导致 `∃ (X : RecObj.{u}), Iso (DFunctor_obj X) E` 对 E : SpObj（Type 0）**universe mismatch**。

**修复方案**（同时服务于路线 P 和路线 B）：

```lean
-- SpObj 升级为 universe-polymorphic
structure SpObj where
  n : ℕ
  V : Type u
  [Fintype V] : Fintype V
  [DecidableEq V] : DecidableEq V
  A : Matrix V V ℂ
```

**工作量**：小（1-2 天），但需要递归升级 DFunctor_obj / DFunctor_map / SpHom 的 universe 绑定。

**前置检查**：Lean 库里 `structure SpObj` 被多少地方引用——需要 grep 确认。

**风险**：全库 universe 推断可能变得更复杂（universe-polymorphic 结构增加 Lean 工作负载）。

---

## 4. 诚实边界与依赖声明

### 4.1 本阶段不做什么

- **不重新证明** DImAdjRIm / no_global_right_adjoint——它们在当前 Type 0 层已经机检
- **不解决** α⁻¹ 偏移链耦合（H6' 步骤 3 开放项）——需要投影特征定理，候选级
- **不升级** DFunctor_obj 之外的全库 universe——风险高收益低
- **不替代** arXiv 论文第四章 H6' 机制（论文先完成，本路线图后）

### 4.2 诚实边界

| 边界 | 类型 | 处理 |
|---|---|---|
| SpObj universe 升级可能引入全库推断问题 | 技术风险 | P-1 单独模块测试后再全库升级 |
| 路线 B 的粗粒化尺度物理输入 | 诠释层 | 登记为候选级扩展，数值不内生化 |
| 路线 P 的 Hille-Yosida 等 Mathlib 组件 | 依赖风险 | 先查 Mathlib 2025 版本进度，可能需要 Agda 侧先降 |
| 两条路线的数学等价性 | 开放探索点 | 不设为必须达成目标 |

### 4.3 时间窗口

| 里程碑 | 路线 | 时间 | 产出 |
|---|---|---|---|
| M1: Universe 升级 + SpCrude 基本定义 | B + P 共通 | 2 周 | SpObj.{u} 构建通过；SpCrudeCategory skeleton |
| M2: DCrude ⊣ RCrude 三角恒等式机检 | B | 再 2-3 周 | DCrude ⊣ RCrude theorem（粗粒化层伴随存在） |
| M3: DCrude → Im(D) 嵌入 + 等价性检查 | B | 再 1-2 周 | 粗粒化层与 SpImD 层的桥接 theorem |
| M4: RecObj universe-polymorphic + DFunctor_obj.{u} | P | 与 M2-M3 并行 | DFunctor_obj universe-polymorphic 版本构建通过 |
| M5: D_gen（Koopman 算子）构造 | P | 3-6 个月 | 依赖 Mathlib Hilbert 算子 + Hille-Yosida 降 theorem |

路线 B 全量 ~4-6 周可达 M3（粗粒化层伴随存在机检 + 桥接 SpImD）。
路线 P 至少需要 3-6 个月（依赖 Mathlib/Agda postulate 前置）。

两条路线并行——路线 B 是快速反馈线，路线 P 是长期完备化线。

---

## 5. 与已完成工作的桥接

本阶段建立在以下 Lean 库锚之上：

| 锚 | 本阶段用途 |
|---|---|
| `no_global_right_adjoint` | 精确刻画当前层边界（路线 P/B 的动机） |
| `DIm_full` + `DIm_faithful` | SpImD 层骨架（路线 B 的 DCrude 构造参考） |
| `DImAdjRIm` | SpImD 伴随已机检（路线 B 三角恒等式证明模式参考） |
| `SpImD` 结构 + `conn` 字段 | 身份标记条件 = SpImD 唯一性充要边界（路线 B 的 SpCrudeObj 需携带类似身份标记） |
| `AdjunctionAnchor.lean` Part 1-2 | 已机检 theorem 列表 + Universe 诚实边界登记 |
| `MeasurementAlgebra.lean` | H6' 三通道投影域作为粗粒化尺度的物理输入参考 |

---

*本文档是 Phase 16B 规划的初始版本，后续按里程碑更新。*
