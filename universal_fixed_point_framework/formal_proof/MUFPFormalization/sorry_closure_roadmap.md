# MUFPF 形式化 sorry 清零路线图

**文档编号**：MUFPF-SORRY-ROADMAP-001
**日期**：2026-09-11
**版本**：v1.0
**配套**：ENV_GUIDE.md v1.2 §9（统计口径）、§12（API 修复模式）

---

## 一、总览

| 日期 | 实际 sorry（剥离注释） | 显式 axiom | 状态 |
|:-----|:----------------------:|:----------:|:-----|
| 2026-09-10（修复前统计口径修正前） | 误报 ~41 | 4 | 口径错误，含注释提及 |
| 2026-09-11 上午 | 3 | 4 | 全库 0 error（ec5b4c9） |
| **2026-09-11（本路线图提交时）** | **1** | 4 | PinchTopology ×2 已清零 |

**统计口径（重要）**：匹配 `\bsorry\b` 前必须先剥离 Lean 注释
（`/- -/` 可嵌套 + `--` 行注释）。原始 grep 的 ~41 处中 38 处为注释里的
缺口登记/历史记录。构建期 "declaration uses sorry" 警告可能来自
对含 sorry 模块的**下游依赖**，不代表该文件直接使用。

---

## 二、已闭合项详录（2026-09-11）

### 2.1 `kleinBottle_self_intersection`（PinchTopology.lean）— 真命题，已闭合

- **原状**：`step^[2] s0 ≠ s0` 以 sorry 占位，注释称 "decide 无法处理 iterate 求值"。
- **实际**：`step^[2] s0` 归约为 `KleinState.s2`，与 `s0` 是不同构造子，
  `intro h; cases h`（依靠 no-confusion）即闭合。
- **教训**：4 态归纳类型上，decide 受限时优先 `cases` 反证，比 decide 可靠。

### 2.2 `kleinBottle_has_pinch`（PinchTopology.lean）— **原陈述恒假**，已勘误重建

- **原陈述**：`∃ x y, x ≠ y ∧ step^[2] x = step^[2] y`，见证 s0/s2。
- **证伪**：`kleinStep` 是 4-循环，**任意次迭代都是双射**，
  `step^[2] s0 = s2`、`step^[2] s2 = s0`，而 `s2 ≠ s0` —— 命题恒假，
  旧注释 "rfl 无法处理 iterate 求值" 系误诊。
- **物理根源**：克莱因瓶自交是**几何**现象（两个离散层位于同一几何点），
  不是动力学碰撞（step 非单射）。4-循环模型中 step 永不非单射，
  "step 迭代相等" 无法刻画自交。
- **勘误方案**：新增几何投影（商映射）
  `kleinGeometricPoint : KleinState → Fin 2`（s0/s2→0，s1/s3→1），
  捏点/自交改述为 `∃ x y, x ≠ y ∧ kleinGeometricPoint x = kleinGeometricPoint y`，
  见证 s0/s2，一行 `rfl` 闭合。
- **下游同步**：`kleinBottle_3d_embedding_self_intersection` 同步改述
  （它是 kleinBottle_has_pinch 的直接引用，无其他依赖方）。
- **保留不变**：`hasPinchPoint`（step 非单射定义）本身不动——它用于
  连通和 `connectedSumRecObj` 等真正非单射的模型，那些定理独立成立。

---

## 三、剩余 1 项：Einstein 散度自由（SpectralMetric.lean:732）

### 3.1 目标

```lean
theorem einstein_divergence_free_from_bianchi (Γ : ChristoffelSymbol)
    (g : MetricTensor) (n : Fin 4) :
    einsteinDivergenceSum4 g (ricciFromChristoffel Γ)
      (scalarCurvature g (ricciFromChristoffel Γ)) n = 0
```

即 `Σ_m G_mn = 0`（G = Ric − ½Rg），是 Einstein 场方程自洽性的核心：
能动量守恒的先决条件。

### 3.2 已有基础设施（全部已闭合）

| 组件 | 状态 |
|:-----|:-----|
| `sum4` 显式 4 项和 + `sum4_eq_finset_sum` 桥接 | ✅ |
| `firstBianchiExplicit`（第一 Bianchi） | ✅ |
| `second_bianchi_discrete`（第二 Bianchi 离散形式，~48 个三次单项式，`simp only [tf]; ring_nf` 闭合） | ✅ |
| `einsteinDivergence_eq`（sum4 ↔ Finset.sum 桥接） | ✅ |
| `ricciFromChristoffel` / `scalarCurvature` / `einsteinTensor` 定义链 | ✅ |

### 3.3 瓶颈定位

`scalarCurvature` 展开为 `Σ_m Ric_mm` 后，Einstein 张量的
`g_mn × R` 项在 `n` 固定、m 遍历 4 值时展开为 **4 × 64 = 256 个单项式**，
`ring`/`ring_nf` 在该规模下无法在合理时间完成（kernel 归约爆炸）。

### 3.4 闭合路径（按推荐排序）

**路径 A（推荐）：trace-reversed 分而治之**
数学恒等式 `∇^μ G_μν = ∇^μ R_μν − ½ ∇_ν R`。分两个引理：

1. `lemma ricci_divergence_eq_half_scalar_gradient`：
   `Σ_m ∇R_mn = ½ ∇_n R`（第二 Bianchi 缩并的离散形式）。
   在离散骨架（无偏导数项）下即为 `sum4` 层面的恒等式，
   单项式规模 ~48–128，`simp only [discreteSecondBianchi, tf]; ring_nf` 模式
   已验证可行（同 `second_bianchi_discrete`）。
2. `lemma einstein_div_split`：
   用 `einsteinTensor` 定义拆分 `Σ_m G_mn = Σ_m Ric_mn − ½ Σ_m g_mn R`，
   代入引理 1 后 `Σ_m g_mn R = R`（度规归一，`fin_cases n` 后逐项验证），
   剩余 `½ R − ½ R = 0`。
单引理规模均 ≤128 单项式，绕开 256 项整攻。

**路径 B：对 m 分指标攻击**
`fin_cases n` 后 `fin_cases` 每个 m 的求和索引，把 256 项拆成 4 组 64 项
分别 `ring`。组内仍偏大，必要时再按 Γ 指标对拆分。机械但可靠。

**路径 C：线性组合策略**
`linear_combination`（Mathlib.Tactic.LinearCombination）以
`second_bianchi_discrete` 的实例为系数基底构造证明。
适合路径 A 的两引理形式。

**路径 D：升级计算引擎**
引入 `polyrith`（Sage 后端，需网络）或把骨架迁移到 `MvPolynomial` 商环
做可判定等式检查。工程量大，仅当 A–C 均失败时考虑。

### 3.5 验证标准

闭合后 `lake build MUFPFormalization.SpectralMetric` 无 sorry 警告，
且 ENV_GUIDE §9.1 的 sorry 计数更新为 0。同时应回查 `energy_momentum_conservation`
（SpectralMetric.lean:767）等下游声明是否从 sorry 占位升级为可证。

---

## 四、显式 axiom 登记（4 项，非 sorry，属 open 问题占位）

| # | 声明 | 文件 | 关闭路径 |
|:-:|:-----|:-----|:---------|
| 1 | `layer2_statistical_spectral_correspondence_open` | EDRNCrossFramework.lean:128 | Layer-2 统计谱对应需无穷维算子谱理论（Phase 16B） |
| 2 | `layer3_silence_discordance_full_equivalence_open` | EDRNCrossFramework.lean:140 | Layer-3 静默-失谐全等价，同上 |
| 3 | `D_partial` | GeneralMetaTheoremFramework.lean:89 | 一般递归系统的部分 D 函子，需极限/稠密性论证 |
| 4 | `D_partial_spec` | GeneralMetaTheoremFramework.lean:92 | D_partial 的规范公理，随 #3 一并关闭 |

**原则**：axiom 保持显式（不伪装成 sorry/theorem），命名带 `_open` 后缀，
关闭时逐条转为定理并删除。

---

## 五、防回归检查清单

- [ ] 新增 sorry 必须在旁注原因 + 在本文件登记 + 更新 ENV_GUIDE §9 计数
- [ ] 统计 sorry 必须用注释剥离口径（§一），禁止原始 grep 直接报数
- [ ] 定理陈述被证伪时（如 §2.2），勘误需保留原陈述与证伪记录
- [ ] 每闭合一项即运行 `lake build MUFPFormalization` 全库验证
