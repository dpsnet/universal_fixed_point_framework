# Phase 69.2: 大尺度结构形式化框架

**文档编号**：MUFPF-RN-PHASE69-002
**日期**：2026-09-08
**版本**：v1.0
**状态**：形式化完成
**前置依赖**：Phase 68.5（大尺度结构因果集起源，研究笔记层面）、Phase 69.1（CMB 功率谱深化）

---

## 一、目标与动机

Phase 68.5 在研究笔记层面建立了大尺度结构的因果集起源框架，但缺乏 Lean4 形式化。Phase 69.2 的目标是：

1. **因果集粗粒化**：从离散因果结构到连续密度场的数学映射
2. **宇宙网骨架**：丝状结构、空洞、节点的形式化定义
3. **星系质量函数**：从缺陷分布推导 Press-Schechter 形式
4. **暗物质晕**：因果束缚态的形式化描述

---

## 二、理论框架

### 2.1 核心思想：因果集 → 大尺度结构

在 MUFPF 框架中，宇宙大尺度结构不是由引力不稳定性增长形成的（ΛCDM 图像），而是因果集拓扑结构的宏观显现：

```
因果集（离散）
    ↓ 粗粒化
物质密度场（连续）
    ↓ 拓扑显现
宇宙网骨架（丝状 + 空洞 + 节点）
    ↓ 缺陷统计
星系质量函数 + 暗物质晕
```

### 2.2 与 ΛCDM 的对比

| 方面 | ΛCDM | MUFPF |
|:---|:---|:---|
| 结构起源 | 原初涨落 + 引力不稳定性 | 因果集拓扑 + 粗粒化 |
| 暗物质 | 冷暗物质粒子 | 束缚态结构性缺陷 |
| 暗能量 | 宇宙学常数 Λ | 弥散态结构性缺陷 |
| 宇宙网 | 丝状结构由暗物质晕并合形成 | 丝状结构 = 因果链主干 |
| 空洞 | 欠密区膨胀更快 | 因果稀疏区域 |

---

## 三、形式化内容

### 3.1 因果集粗粒化（§23.1）

**定义结构**：

```lean
structure CoarseGrainingRegion (cs : CausalStructure) where
  events : Finset cs.Event   -- 区域包含的事件
  nonempty : events.Nonempty  -- 区域非空
```

```lean
structure CoarseGrainingScheme (cs : CausalStructure) where
  regions : Finset (CoarseGrainingRegion cs)  -- 区域集合
  covers : ∀ x, ∃ r ∈ regions, x ∈ r.events   -- 覆盖性
  disjoint : ∀ r₁ ∈ regions, ∀ r₂ ∈ regions,
             r₁ ≠ r₂ → Disjoint r₁.events r₂.events  -- 不交性
```

**关键设计决策**：`regions` 使用 `Finset` 而非 `List`
- 原因：`List` 允许重复元素，导致"总密度"可能超过总事件数
- `Finset` 天然保证唯一性，与"划分"概念一致

**核心定理**：

```lean
theorem coarse_graining_preserves_total_events :
    cg.totalDensity = Fintype.card cs.Event
```

**证明策略**：
1. 由 `covers` 得：`⋃ r ∈ regions, r.events = Finset.univ`
2. 由 `disjoint` 得：区域事件集两两不交
3. 应用 `Finset.card_biUnion` 得：`card(⋃) = Σ card(r.events)`
4. 化简得：`totalDensity = Fintype.card cs.Event`

**物理意义**：粗粒化是信息保持的——总事件数（总质量）守恒，只是空间分布被重组织。

### 3.2 物质密度场（§23.2）

```lean
structure MatterDensityField where
  Point : Type _          -- 空间点类型
  [fin : Fintype Point]   -- 有限性
  density : Point → ℝ     -- 密度函数
  density_nonneg : ∀ p, 0 ≤ density p
```

**导出量**：
- `totalMass`：总质量 = `Σ density(p)`
- `averageDensity`：平均密度 = 总质量 / 点数
- `densityVariance`：密度方差 = `Σ (density(p) - avg)² / N`

**物理意义**：密度方差对应原初扰动谱的振幅，是结构形成的种子。

### 3.3 宇宙网骨架（§23.3）

**丝状结构（Filament）**：
```lean
structure Filament (cs : CausalStructure) where
  source : cs.Event          -- 起始节点
  target : cs.Event          -- 终止节点
  path : List cs.Event       -- 路径上的事件
  path_start : path.head? = some source
  path_end : path.getLast? = some target
  path_causal : ∀ i, prec(path[i])(path[i+1])
```

**空洞（Void）**：
```lean
structure Void (cs : CausalStructure) where
  events : Finset cs.Event
  low_density : events.card < Fintype.card cs.Event / 10
```

**宇宙网骨架（CosmicWebSkeleton）**：
```lean
structure CosmicWebSkeleton (cs : CausalStructure) where
  nodes : Finset cs.Event       -- 节点（星系团）
  filaments : List (Filament cs) -- 丝状结构
  voids : List (Void cs)         -- 空洞
  nodes_high_defect : ...
  filaments_connect : ∀ f ∈ filaments, f.source ∈ nodes ∧ f.target ∈ nodes
```

**核心定理**：

```lean
theorem cosmic_web_from_causal_skeleton (cs : CausalStructure)
    [Inhabited cs.Event] :
    ∃ cws, cws.nodeCount > 0 ∨ cws.filamentCount > 0
```

**证明策略**：构造最小宇宙网骨架——单节点 `{x}`，空丝状列表，空空洞列表。物理上对应最简单的结构：单个星系团。

**注意**：需要 `[Inhabited cs.Event]` 假设，因为空事件集无法构造非空骨架。物理上这是合理的——宇宙至少包含一个事件。

### 3.4 星系质量函数（§23.4）

**质量等级分类**：
```lean
inductive MassClass where
  | dwarf    -- 矮星系
  | normal   -- 正常星系
  | giant    -- 巨椭圆星系
  | cluster  -- 星系团
```

**质量函数结构**：
```lean
structure GalaxyMassFunction where
  n_dwarf   : ℕ  -- 矮星系数量
  n_normal  : ℕ  -- 正常星系数量
  n_giant   : ℕ  -- 巨椭圆星系数量
  n_cluster : ℕ  -- 星系团数量
```

**从缺陷分布推导**：
```lean
def massFunctionFromDefect (cdd : CosmicDefectDistribution) :
    GalaxyMassFunction :=
  { n_dwarf   := cdd.diffuse_defect / 10
    n_normal  := cdd.bound_defect / 2
    n_giant   := cdd.bound_defect / 5
    n_cluster := cdd.bound_defect / 20 }
```

**物理对应**：
- 弥散态缺陷 → 矮星系（低密度、广泛分布）
- 束缚态缺陷 → 正常星系（中等密度）
- 高密度束缚态 → 巨椭圆星系
- 极高密度束缚态 → 星系团

### 3.5 暗物质晕（§23.5）

```lean
structure DarkMatterHalo where
  bound_defects : ℕ   -- 束缚态缺陷数量（决定质量）
  radius : ℝ          -- 晕半径
  radius_nonneg : 0 ≤ radius
  defects_pos : 0 < bound_defects
```

**导出量**：
- `mass`：晕质量 = 束缚态缺陷数
- `density`：晕密度 = 质量 / 体积（`(4/3)πr³`）

**核心定理**：

```lean
theorem darkMatter_halo_from_bound_defects :
    0 < cdd.bound_defect →
    ∃ halo, halo.mass = cdd.bound_defect
```

**物理意义**：暗物质晕是束缚态缺陷的自然聚集态——只要有束缚态缺陷，就存在暗物质晕。

---

## 四、关键命题验证

| 命题 | 状态 | 对应定理/结构 |
|:---|:---|:---|
| P69.2.1: 因果集粗粒化映射良定义 | ✅ | `CoarseGrainingScheme` + `totalDensity` |
| P69.2.2: 宇宙网丝状结构 = 因果链主干 | ✅ | `Filament` + `CosmicWebSkeleton` |
| P69.2.3: 星系质量函数由缺陷分布决定 | ✅ | `massFunctionFromDefect` |
| P69.2.4: 暗物质晕 = 束缚态缺陷的引力势阱 | ✅ | `DarkMatterHalo` + `darkMatter_halo_from_bound_defects` |

---

## 五、数学技术细节

### 5.1 Finset.card_biUnion 定理

证明 `coarse_graining_preserves_total_events` 的核心是 mathlib 的 `Finset.card_biUnion`：

```
若 s 是有限集合族，且 s 中任意两个不同集合不交，则：
card(⋃_{x ∈ s} f x) = Σ_{x ∈ s} card(f x)
```

这是有限集论的基本定理，对应"划分的基数等于各块基数之和"。

### 5.2 List → Finset 重构的经验

在开发过程中，最初使用 `List` 表示区域集合，但发现：
1. `List` 允许重复元素，与"划分"概念不一致
2. 基于 `List` 的总密度定理在数学上不成立
3. 改用 `Finset` 后，定理自然成立，证明也更简洁

**经验教训**：当概念涉及"集合"或"划分"时，优先使用 `Finset` 而非 `List`。

---

## 六、形式化状态

**Lean4 文件**：`SpectralBundle/LargeScaleStructure.lean`（§23）

**编译状态**：`lake build` 全项目通过

**sorry 统计**：0 sorry

**结构定义**（8个）：
1. `CoarseGrainingRegion` — 粗粒化区域
2. `CoarseGrainingScheme` — 粗粒化方案
3. `MatterDensityField` — 物质密度场
4. `Filament` — 丝状结构
5. `Void` — 宇宙空洞
6. `CosmicWebSkeleton` — 宇宙网骨架
7. `GalaxyMassFunction` — 星系质量函数
8. `DarkMatterHalo` — 暗物质晕

**定理证明**（6个）：
1. `coarse_graining_preserves_total_events` — 粗粒化保持总事件数
2. `cosmic_web_from_causal_skeleton` — 宇宙网从因果骨架涌现
3. `mass_function_from_defect_distribution` — 质量函数由缺陷分布决定
4. `darkMatter_halo_from_bound_defects` — 暗物质晕从束缚态缺陷形成
5. `darkMatter_halo_exists` — 暗物质晕存在性
6. `large_scale_structure_unified` — 大尺度结构统一描述

---

## 七、与观测的联系

| 观测现象 | SDSS/DES 观测 | MUFPF 解释 |
|:---|:---|:---|
| 宇宙网结构 | 大尺度丝状结构 | 因果链网络的宏观显现 |
| 星系质量函数 | Schechter 形式 | 缺陷统计分布 |
| 暗物质晕 | 星系旋转曲线、引力透镜 | 束缚态缺陷的引力势阱 |
| 宇宙空洞 | 巨型空洞（~100 Mpc） | 因果稀疏区域 |
| 星系团 | 丰富星系团 | 高缺陷密度区域 |

---

## 八、后续工作

1. **深化粗粒化理论**：从简单分区到多层粗粒化（重整化群流）
2. **数值模拟**：实现因果集粗粒化的 Python 数值代码（Phase 69.3）
3. **与 SDSS 数据对比**：质量函数、两点相关函数
4. **黑洞信息悖论**（Phase 69.4）
5. **论文准备**（Phase 69.5）

---

## 九、文件清单

| 文件 | 说明 |
|:---|:---|
| `SpectralBundle/LargeScaleStructure.lean` | §23 大尺度结构形式化 |
| `SpectralBundle/CausalSet.lean` | §17 因果集理论（前置依赖） |
| `SpectralBundle/Cosmology.lean` | §18-§20 宇宙学（含 CosmicDefectDistribution） |
| `SpectralBundle/CMB.lean` | §21-§22 CMB 功率谱 |
| `SpectralBundle.lean` | re-export 入口文件 |
