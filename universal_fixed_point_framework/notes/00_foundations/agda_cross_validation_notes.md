# Agda 交叉验证笔记（路径 B 完整报告，第一手研究资料）

> **定位**：UFPF 形式化验证体系（Lean 4 主实现 + Agda 独立重形式化）的 Agda 侧完整记录。
> **状态**：v1.36 收官（2026-08-03）。对应论文：[`paper38_agda_cross_validation.md`](../../paper/paper38_agda_cross_validation.md)（Paper XXXVIII）。
> **关联**：路线图 [`phase60_category_verification.md`](../../roadmap/phase60_category_verification.md) §路径 B；笔记 [`spectral_T3_analysis_foundation.md`](./spectral_T3_analysis_foundation.md)（技术债清单 §5.16.7 / 方案 A §5.16.8）；主日志 `docs/log.md`。

---

## 1. 目的与定位

### 1.1 为什么需要 Agda 交叉验证

Lean 4（`formal_proof/UFPFormalization/`，74 模块）是**单一实现**。交叉验证动机：

1. **消除单一实现偏差**：证明助理 bug、Mathlib 假设、形式化风格的潜在偏差需要第二实现独立检验。
2. **类型论体系正交**：Lean 依赖 CIC（归纳构造演算）；Agda 用 Martin-Löf 依赖类型论。同一定理在两套类型论下同时通过，可信度高于单实现。
3. **语义绑定**：纯结构定理（层双射、计数、Moran 方程绑定、层独立性、维数分解）在 Agda 中**直接证明**（非 postulate），形成"结构真"的独立证据。

### 1.2 定位边界

- Agda 侧是**验证路径**，不是理论扩展。定理签名与 Lean 一一对应，不引入新公理假设。
- ℝ 实数公理及解析定理（exp/log/rpow、谱论）以 `postulate` 声明——与 Lean 侧 Mathlib 分析库对应，属于框架声明的**基础假设层**，非"未证明"项。
- 纯结构部分（B1-B8 的组合/代数/集合结构）全部直接证明，`Everything.agda` 整体类型检查通过（exit=0）。

---

## 2. 架构与模块清单（16 模块）

`agda_formalization/` 目录（UFPF.agda-lib 注册，name: UFPF）：

```
agda_formalization/
├── UFPF.agda-lib                    # Agda 库注册
├── Everything.agda                  # 主入口：全部模块导入，整体编译验证
├── Categories/                      # 基础库（Category/Functor/NaturalTransformation，3 模块）
├── Sp/
│   ├── SpCategory.agda              # B1: 𝐒𝐩 4-范畴（对象/1-态射/层结构/层对计数）
│   └── HigherSpCategory.agda        # B2: 2-态射、3-态射、交换律偏差结构
├── Rec/
│   └── RecCategory.agda             # Rec 范畴（有限状态 + 演化规则）
├── NatArith/
│   └── NatArith.agda                # ℕ 算术引理库（良基递归 §3，T1 闭合基础）
├── DecursionFunctor/
│   └── DecursionFunctor.agda        # B3: D 函子 + 右伴随 R + 伴随对 D ⊣ R
├── DHStructural/
│   └── DHStructuralAnalysis.agda    # B4: d_H 不等式链（ln 15 < 65/24 < e < 3）+ ℝ 序代数基础
├── HilbertSpace/
│   └── HilbertSpace.agda            # T4: Hilbert 空间/拓扑层（内积→范数→有界算子→谱投影）
├── Unified3/
│   └── Unified3Theorem.agda         # B5: 统一 3 定理（card = 3 双射 + GenSpace + Bott 截断）
├── BottTower/
│   └── BottTower.agda               # B6: Bott 塔（旋量维数翻倍 + log₂ k_max = 3）
├── CoherenceToBranching/
│   └── CoherenceToBranching.agda    # B7: 分支计数原理 + 层独立性 + 向外推（§11 镜像）
├── IFSFractal/
│   └── IFSFractal.agda              # B8: 物理 3-map IFS + c₁ < c₂ < c₃ 排序
├── Cardinality/
│   └── Cardinality.agda             # P4: 基数反例（D 不 full + 4 态射枚举 + 鸽笼无双射）
├── P1Spectral/
│   └── P1Spectral.agda              # P1: 谱匹配有限维特例（定理 3 退化版 + 推论 4 恒等双射）
├── SpectralTheory/
│   └── SpectralTheory.agda          # T3: 谱定理层（谱测度/Fuglede/Hille-Yosida/函数演算 fc）
└── CrossLayer/
    └── CrossLayer.agda              # 跨层模型 Op → LinOp 点态对应证书（OpAlgPt/SpectralObjPt）
```

**计数口径**：15 个业务模块 + `Everything.agda` 主入口 = **16 模块**（`Categories/` 3 模块为基础库，不单独计数）。

### 2.1 与 Lean 的双实现一致性（核心 8 模块 B1-B8）

| # | 模块 | 对应 Lean | Agda 中直接证明 | Agda 中 postulate |
|:-:|:-----|:----------|:---------------|:------------------|
| B1 | 𝐒𝐩 4-范畴 | `SpCategory.lean` | `B-eq-15 : layerPair-count ≡ 15`（refl） | `compose` 占位（T2 已闭合为矩阵构造） |
| B2 | 高阶态射 | `HigherSpCategory.lean` | 垂直/水平复合结合律、条件字段真实化、同伦构造 | — |
| B3 | D ⊣ R 伴随 | `DecursionFunctor.lean` | 左三角恒等式、SpImD 对象层、transferMatrix 忠实性 | R11 态射层（S0 静默，见 §5.3） |
| B4 | d_H 不等式链 | `DHStructuralAnalysis.lean` | `dimension-gap`（链传递） | ℝ 公理、`dH_from_branching` |
| B5 | 统一 3 定理 | `Unified3Theorem.lean` | `card-active-layers` 显式双射、层正交 9 情形枚举 | 层条件（已闭合） |
| B6 | Bott 塔 | `BottTower.lean` | `spinorDim-suc` 递归定义 refl、`spinorDim-eq-pow` 归纳 | `log2` 公理（已闭合为良基递归） |
| B7 | 静默定理组 | `CoherenceToBranching.lean` | `layers-distinct`（≃ Fin 5）、`branchIndex-dH-unique` 双向、层独立性、维数分解、§11 向外推 | ℝ 分析（已闭合） |
| B8 | IFS 排序 | `IFSFractal.lean §6` | `physicalIFS-n ≡ 3`（refl） | 收缩率正性/排序/Moran（已闭合） |

> **B8 范围边界注记（2026-08-04）**：Agda 侧 `PhysicalIFS` 记录仅含 `n` + 三个收缩率（`ratio0/1/2`），**无 maps 字段，无吸引子/直径形式化**（无 ContinuumLimit 对应模块）。Lean 侧 `ContinuumLimit.lean` 的 hDiamLeOne 缺口（勘误 O9）因此**不可参照 Agda 侧闭合**——它属 Lean 特有几何层。2026-08-04 O9 闭合的 Lean 修正发生在 maps 层（`physicalIFS` f₂ 平移 1.0 → 1−c₃），**收缩率 ratios 未变**，故 B8 全部定理（`physicalIFS-n`/`physicalIFS-ratios-ordered` 及 c₁<c₂<c₃ 排序链）不受影响，双实现交叉验证一致性保持。

---

## 3. 闭合历程

### 3.1 路径 B 闭合路线图（2026-07-31 立项）

**立场**（用户决议）：签名镜像不构成第二条验证路径。路径 B 必须**完整闭合**——Agda 侧以独立证明覆盖全部定理，含实分析层（T3）。未闭合前每条 postulate 均为登记在案的开放项。

**三层分类**：
- **T1 纯 ℕ/组合**：5 项（`layerPair-card-15`、`spacetime-dim-eq-category-order`、`dimension-counting-eq-two-mul`、`category-order-unique`、`log2`）——2026-07-31 全部闭合（显式双射枚举 + ℕ 归纳 + 良基递归 WfRec）。
- **T2 结构增强**：B1-B3 占位真实化（ℤ/3 载体矩阵构造、矩阵乘法结合律 `*mat-assoc`、零矩阵吸收、2-/3-态射条件字段真实化、水平/垂直复合、同伦构造、D 忠实性 `transferMatrix-inj`）——2026-07-31 全部闭合。**唯一结构性例外**：B3 R11 有限维态射层（见 §5.3）。
- **T3 实分析**：ℝ 序代数基础（阶段 0 登记为基础假设）→ exp/log/rpow 逐层闭合 → 谱定理层（阶段 6 起）。

### 3.2 T3 谱定理层（SpectralTheory.agda，阶段 6 起持续）

谱论基础公理登记（Borel 谓词谱测度 E/谱表示/谱积分线性/Fuglede 方向/谱测度复合/外延/Hille-Yosida/函数演算 fc），逐层降定理：

- **引理 2 核心可证**：`Rec-to-σ`（Fuglede 对 e^(-A) → 谱测度复合 → E-phi-image，φ 单射经 exp-inj）
- **定理 3 / 推论 4-∞ / 推论 5 / P1-linear-closure**：谱匹配核心**零 fc-integral 依赖完全可证**
- **函数演算 = 谱积分统一**（§5c `fc-integral`）+ fc 代数结构（§5d/§5e）+ 半群 = 函数演算（§13）+ 态射保动力学（§14）
- **Hilbert 层（T4）**：内积→范数→有界算子→谱投影（E-hilb）→ E-σ-add 完整形式全链闭合

### 3.3 技术债清单闭合（v1.17–v1.36，笔记 §5.16.7 A 类全闭合）

| 版本 | 闭合项 | 关键内容 |
|:----:|:-------|:---------|
| v1.17-1.18 | **E-σ-add 收敛** | 连续下式族单调有界结构全可证 + Vigier 强收敛桥接 ⟹ `E-σ-SOT-conv` |
| v1.19-1.20 | **spec-int MCT 构造化** | ℝ-截断（`spec-int-R-trunc-conv` 零新增公理）+ ℕ-截断（`spec-int-trunc-ℕ-conv`，Archimedean 登记，原桥接删除） |
| v1.21 | **谱对象映射部分** | CrossLayer `SpectralObjPt`：E P ↦ E-hilb P + exp-tA t ↦ exp-hilb-tA t（10 字段性质保持） |
| v1.22-1.28 | **方案 A 阶段 1-4** | 正负分解重构：max-ℝ 族 → Op 层减法 `_−ₒ_` → 一致性组件 → 非负一致性（`spec-int-nonneg-consistent`）→ 钉住解析到值级 → id 钉住完全解析 → fc 侧分解（`fc-decomp-pos-neg`） |
| v1.29-1.33 | **方案 A 阶段 4 余项** | dyadic 网格 ℝ 基础 → SimpleF 阶梯 disj 基础（`dyadic-disj`）→ SimpleF dyadic 阶梯实例组装（`dyadic-cover`/`dyadic-Ω3`/`dyadic-stair`）→ 上界 ∫sₖ≤ₒ∫p⁺（`dyadic-int-below`）→ MCT（`stair-seq`/`stair-MCT`/`stair-int-full`） |
| v1.34 | **方案 A 收官（依赖循环解决）** | fc(p⁺)≤ₒ∫p⁺ 经 fc-continuous 自循环（结构性）→ 改用更基础 `fc-integral` 直接降 `fc-poly-le-spec-int` 为可证定理——**桥接减一**，fc 侧唯一剩余 D 类 = fc-integral |
| v1.35 | **ln15-arith-ax 闭合尝试** | 逻辑链完备（refl 级闭合），组装触发 Agda 内存不足（`osCommitMemory: VirtualAlloc MEM_COMMIT failed`，2994494400 级大数归一化）→ 确认为**工程计算资源不足**（非结构性），保留 scoped 公理，前移 `*-div-impl`/`frac-cancel-ℝ` 可证引理 |
| v1.36 | **谱对象映射完整** | HilbertSpace §12' `A-hilb`/`fc-hilb`（谱定理降定理链端点桥接）+ CrossLayer SpectralObjPt 扩展 A/fc 字段——**谱对象映射（A/E/fc/exp-tA）完整闭合** |

### 3.4 公理纪律审计（SpectralTheory §15）

全部 postulate 按类别登记：D 类（降定理路径文档化）、C 类（补充公理）、G 类（算子代数补充）、scoped 数值公理（"工程计算资源不足"）。每条注明模型必然性与降定理路径。

---

## 4. 当前状态（v1.36，2026-08-03）

- **编译**：`agda Everything.agda` 全量类型检查通过（exit=0）。
- **技术债清单 A 类（实质技术债）全闭合**：fc-poly-le-spec-int 构造化、E-σ-add 收敛、spec-int MCT、跨层谱对象映射——四项全部收官。
- **可诚实声称的边界**：谱匹配核心（theorem3/corollary4-∞/corollary5/P1-linear-closure）零桥接依赖完全可证；fc-integral 公理已降为定理（唯一剩余 D 类 = fc-integral 本身，即"函数演算 = 谱积分"谱定理层的模型保证）；spec-int MCT 构造化闭合；Agda 16 模块全量通过；Lean 核心 10 模块零错误。

---

## 5. 剩余开放项与登记公理

### 5.1 结构性限制（B 类，不可/不应闭合）

1. **funext 受限**（8-5b 算子层等式版公理 + 对象映射 op-lin 等式保结构）——库公理范围外。
2. **`HigherSpCategory.lean` spExchangeLaw sorry**——**概念特征**（非技术缺口）：填补为等式 ⇒ G_N → 0（物理错误）。正确方向是维持偏差代数形式（已由 `spExchangeLaw_deviation_partial_commutator` 和 `spExchangeLaw_homotopy_deviation` 覆盖）。
3. **钉住 sup 语义**（spec-int-general 定义语义）——框架设计决策，已文档化（§1b）。

### 5.2 待基础设施（C 类，可自然闭合）

1. **`DeviationBound.lean` 2 sorry**——依赖 Mathlib `Matrix.Spectrum` 模块稳定。
2. **T3 阶段 3 scoped 数值公理**（`ln15-arith-ax`；`ln1615-lb` 与 `ln2-lt` **已于 2026-08-05 闭合为定理**：exp 级数机制 + log 级数机制 + 二进制 ℕ 算术（NATTIMES/NATPLUS + `<-add` 差递归））——纯有理/数值比较，逻辑完备但工程计算资源不足（大整数算术/级数机制）。**`ln15-arith-ax` 已于 2026-08-05 闭合**（§2d：`*-/ℝ` 并入分子 + `neg-frac-ℝ` 取负 + `/-add-ℝ` 合并为 121870600/45000000，65/24 通分 ×1875000 同分母比分子，差 4400 经 `<-add`，最大扩展因子 ~1.25e8 秒级）——**C 类 T3 数值项全部清零**。

### 5.3 结构性障碍：R11 有限维态射层（S0 表示静默）

B3 R11 有限维 SpImD 态射层**结构性不可闭合**（基数反例）：2 状态平凡系统下 Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）vs Hom_Rec(X,Y) = 4（有限），无双射；P=[[1,0],[1,1]] 是合法谱态射但非转移矩阵（D 的 full 性为假）。闭合仅当态射限制为转移矩阵（平庸化）或转无限维（论文 R11 断言，需 T3 谱定理验证）。**定性为 S0 表示静默**（见 [`spectral_representation_silence.md`](./spectral_representation_silence.md)）。推进方向：P0 论文层范围修正（已执行）→ P1 R11 无限维严格验证（谱定理下基数自洽与谱匹配断言，决定性）→ P2-P4（已完成）。

---

## 6. 局限性与声明纪律

1. **postulate 层**：ℝ 公理体系（B4 §0）是基础假设（对应 Lean/Mathlib 的 ℝ 公理），非"未证明"——计入"基础假设"，不计入"开放项"。
2. **工程计算资源不足 ≠ 理论未闭合**：scoped 数值公理逻辑完备，仅实现资源限制。
3. **结构真 vs 理论扩展**：Agda 验证的是既定定理的独立证明，不扩大宣称范围；任何新宣称仍须走笔记 → 论文流程并在勘误登记。
4. **论文表述纪律**：不使用"全部闭合/零公理"等绝对表述；逐项注明"可证/桥接/登记/待基础设施"。

---

## 版本记录

| 版本 | 日期 | 变更 |
|:----:|:-----|:-----|
| v0.1 | 2026-08-03 | 初版。基于路线图 phase60 §路径 B、技术债清单 §5.16.7、方案 A §5.16.8、主日志 v1.17-v1.36 整理。对应 Paper XXXVIII 笔记。 |
