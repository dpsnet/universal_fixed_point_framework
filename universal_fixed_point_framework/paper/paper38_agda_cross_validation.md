# 通用不动点范畴框架 XXXVIII：Agda 独立交叉验证——UFPF 形式化体系的双实现证明

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**版本**：v0.1（2026-08-03）

**摘要**：本文系统说明 UFPF 形式化验证体系的 **Agda 独立重形式化**（路径 B）：目的、完成情况、与 Lean 4 主实现的双实现一致性，以及诚实标注的边界与剩余开放项。UFPF 的形式化验证采用**双实现协议**——Lean 4（CIC，`formal_proof/UFPFormalization/`，74 模块，核心 10 模块零 `sorry`）为主实现，Agda（Martin-Löf 依赖类型论，`agda_formalization/`，16 模块）为独立验证路径。纯结构部分（层双射、计数、Moran 方程绑定、层独立性、维数分解、伴随构造）在 Agda 中**直接证明**；ℝ 实数公理与解析定理以 `postulate` 声明（对应 Lean 侧 Mathlib 分析库，属于框架基础假设层）。2026-07-31 完成核心 8 模块（B1-B8）独立重形式化；随后按闭合路线图持续推进 T3 谱定理层，至 2026-08-03（v1.36）技术债清单 A 类（实质可闭合项）**全闭合**：E-σ-add 收敛、spec-int 单调收敛定理（MCT）构造化、fc-poly-le-spec-int 构造化（方案 A 收官，含依赖循环解决）、跨层谱对象映射（A/E/fc/exp-tA）完整闭合。`Everything.agda` 全量类型检查通过。本文逐项区分"可证 / 桥接登记 / 基础假设 / 待基础设施 / 结构性限制"，避免绝对化表述。

---
**记号与引用**：本文引用 RAP-Errata v0.8（宣称基线）。Agda 代码位于 `agda_formalization/`（`Everything.agda` 整体编译 exit=0）。本文自包含：路径 B 闭合账目、技术债分类（A/B/C/D）与推导要点均已内嵌正文，不依赖外部笔记或路线图文档。

---

## 1. 引言

### 1.1 为什么需要第二条验证路径

UFPF 的核心定理此前仅在 Lean 4 中形式化。Lean 4 是**单一实现**：其正确性依赖证明助理本身、Mathlib 库假设与形式化风格的无偏性。为消除单一实现偏差，路径 B（Agda 独立重形式化）于 2026-07-31 立项，原则为：

1. **消除单一实现偏差**：证明助理 bug、库假设、风格差异由第二实现独立检验。
2. **类型论体系正交**：Lean 依赖 CIC（归纳构造演算），Agda 用 Martin-Löf 依赖类型论。同一定理在两套类型论下通过，可信度高于单实现。
3. **结构真独立证据**：纯结构定理（层双射、计数、Moran 方程绑定、层独立性、维数分解）在 Agda 中直接证明（非 postulate），与 Lean 形成独立的结构证据。

### 1.2 定位边界

- Agda 侧是**验证路径**，不是理论扩展：定理签名与 Lean 一一对应，不引入新公理假设。
- ℝ 实数公理及解析定理（exp/log/rpow、谱论）以 `postulate` 声明，对应 Lean 侧 Mathlib 分析库——属于**基础假设层**，计入"基础假设"，不计入"开放项"。
- 路径 B 的立场（用户决议）：签名镜像不构成第二条验证路径；路径 B 必须**完整闭合**——Agda 侧以独立证明覆盖全部定理，含实分析层（T3）。

---

## 2. 架构与模块清单（16 模块）

`agda_formalization/`（`UFPF.agda-lib` 注册，name: UFPF）。**计数口径**：15 个业务模块 + `Everything.agda` 主入口 = 16 模块（另有 `Categories/` 基础库 3 模块：Category/Functor/NaturalTransformation）。

| 模块 | 编号 | 对应 Lean | 内容 |
|:-----|:----:|:----------|:-----|
| `Sp/SpCategory.agda` | B1 | `SpCategory.lean` | $\mathbf{Sp}$ 4-范畴（对象/1-态射/层结构/层对计数） |
| `Sp/HigherSpCategory.agda` | B2 | `HigherSpCategory.lean` | 2-/3-态射、交换律偏差结构 |
| `Rec/RecCategory.agda` | — | `RecCategory.lean` | Rec 范畴（有限状态 + 演化规则） |
| `NatArith/NatArith.agda` | — | — | ℕ 算术引理库（良基递归 §3，T1 闭合基础） |
| `DecursionFunctor/DecursionFunctor.agda` | B3 | `DecursionFunctor.lean` | D 函子 + 右伴随 R + 伴随对 D ⊣ R |
| `DHStructural/DHStructuralAnalysis.agda` | B4 | `DHStructuralAnalysis.lean` | d_H 不等式链（ln 15 < 65/24 < e < 3）+ ℝ 序代数基础 |
| `HilbertSpace/HilbertSpace.agda` | T4 | — | Hilbert 空间/拓扑层（内积→范数→有界算子→谱投影） |
| `Unified3/Unified3Theorem.agda` | B5 | `Unified3Theorem.lean` | 统一 3 定理（card = 3 双射 + GenSpace + Bott 截断） |
| `BottTower/BottTower.agda` | B6 | `BottTower.lean` | Bott 塔（旋量维数翻倍 + log₂ k_max = 3） |
| `CoherenceToBranching/CoherenceToBranching.agda` | B7 | `CoherenceToBranching.lean` | 分支计数 + 层独立性 + §11 向外推镜像 |
| `IFSFractal/IFSFractal.agda` | B8 | `IFSFractal.lean §6` | 物理 3-map IFS + c₁ < c₂ < c₃ 排序 |
| `Cardinality/Cardinality.agda` | P4 | — | 基数反例（D 不 full + 鸽笼无双射） |
| `P1Spectral/P1Spectral.agda` | P1 | — | 谱匹配有限维特例（定理 3 退化版 + 推论 4） |
| `SpectralTheory/SpectralTheory.agda` | T3 | — | 谱定理层（谱测度/Fuglede/Hille-Yosida/函数演算 fc） |
| `CrossLayer/CrossLayer.agda` | — | — | 跨层模型 Op → LinOp 点态对应证书（OpAlgPt/SpectralObjPt） |

### 2.1 与 Lean 的双实现一致性（核心 8 模块 B1-B8）

| # | Agda 中直接证明 | Agda 中 postulate |
|:-:|:---------------|:------------------|
| B1 | `B-eq-15 : layerPair-count ≡ 15`（refl） | `compose` 占位（T2 已闭合为矩阵构造） |
| B2 | 垂直/水平复合结合律、条件字段真实化、同伦构造 | — |
| B3 | 左三角恒等式、SpImD 对象层、`transferMatrix-inj`（D 忠实性） | R11 有限维态射层（S0 静默，§5.3） |
| B4 | `dimension-gap`（链传递） | ℝ 公理、`dH_from_branching` |
| B5 | `card-active-layers` 显式双射、层正交 9 情形枚举 | 层条件（已闭合） |
| B6 | `spinorDim-suc`（递归 refl）、`spinorDim-eq-pow`（归纳） | `log2` 公理（已闭合为良基递归） |
| B7 | `layers-distinct`（≃ Fin 5）、`branchIndex-dH-unique` 双向、层独立性、维数分解、§11 向外推 | ℝ 分析（已闭合） |
| B8 | `physicalIFS-n ≡ 3`（refl） | 收缩率正性/排序/Moran（已闭合） |

---

## 3. 交叉验证协议

1. **签名对应**：Agda 定理签名与 Lean 一一对应（如 `transferMatrix-inj` ↔ `transferMatrix_injective`、`dimension-gap` ↔ `dimension_gap`）。
2. **独立证明**：结构部分在 Agda 中直接证明，不引用 Lean 证明；分析部分以 `postulate` 声明并在公理纪律审计（SpectralTheory §15）中分类登记。
3. **整体编译**：每条闭合项完成后 `Everything.agda` 整体类型检查（exit=0），防模块间不一致。
4. **登记纪律**：每条 postulate 注明类别（D 降定理路径 / C 补充公理 / G 算子代数补充 / scoped 数值公理）与模型必然性。

---

## 4. 闭合历程与主要结果

### 4.1 闭合路线图（三层分类）

- **T1 纯 ℕ/组合**（5 项）：`layerPair-card-15`、`spacetime-dim-eq-category-order`、`dimension-counting-eq-two-mul`、`category-order-unique`、`log2`——2026-07-31 全部闭合（显式双射枚举 + ℕ 归纳 + 良基递归 WfRec）。
- **T2 结构增强**：B1-B3 占位真实化（ℤ/3 载体矩阵构造、`*mat-assoc` 矩阵乘法结合律、零矩阵吸收、2-/3-态射条件字段真实化、同伦构造、D 忠实性）——2026-07-31 全部闭合。唯一结构性例外：B3 R11 有限维态射层（§5.3，S0 表示静默）。
- **T3 实分析**：ℝ 序代数基础（阶段 0 登记）→ exp/log/rpow 逐层闭合（`exp-inj` 由三分律 + 单调性闭合，零新增公理）→ 谱定理层（阶段 6 起）。

### 4.2 T3 谱定理层（SpectralTheory.agda）

谱论基础公理（Borel 谓词谱测度 E/谱表示/谱积分线性/Fuglede/Hille-Yosida/函数演算 fc）登记后逐层降定理：

- **谱匹配核心零依赖完全可证**：引理 2 `Rec-to-σ`、定理 3、推论 4-∞、推论 5、P1-linear-closure——独立于 fc-integral 桥接。
- **函数演算 = 谱积分统一**（§5c `fc-integral`）+ fc 代数结构（§5d/§5e）+ 半群 = 函数演算（§13 exp-A-fc/exp-tA-fc）+ 态射保动力学（§14）。
- **Hilbert 层（T4）全链闭合**：内积 → Cauchy-Schwarz → 范数 → 有界算子 → C* 恒等 → 谱投影（E-hilb）→ E-σ-add 完整形式。

### 4.3 技术债清单 A 类全闭合（v1.17–v1.36）

数学层技术债清单将缺口分类为 A（实质可闭合）/B（结构性不可闭合）/C（待基础设施）。**A 类四项全部收官**：

| 版本 | 闭合项 | 结果 |
|:----:|:-------|:-----|
| v1.17-1.18 | E-σ-add 收敛 | 单调有界族结构全可证 + Vigier 强收敛桥接 ⟹ `E-σ-SOT-conv` |
| v1.19-1.20 | spec-int MCT 构造化 | ℝ-截断 `spec-int-R-trunc-conv`（零新增公理）+ ℕ-截断 `spec-int-trunc-ℕ-conv`（Archimedean 登记，原桥接删除） |
| v1.21 | 谱对象映射部分 | CrossLayer `SpectralObjPt`：E ↦ E-hilb、exp-tA ↦ exp-hilb-tA（10 字段性质保持） |
| v1.22-1.28 | 方案 A 阶段 1-4 | 正负分解重构：max-ℝ 族 → Op 减法 `_−ₒ_` → 一致性 → 非负一致性 → 钉住解析 → fc 侧分解 |
| v1.29-1.33 | 方案 A 阶段 4 余项 | dyadic 网格 → SimpleF 阶梯（disj/cover/Ω3/stair）→ 上界 ∫sₖ≤ₒ∫p⁺ → MCT（stair-int-full） |
| v1.34 | **方案 A 收官** | `fc-poly-le-spec-int` **依赖循环解决**：fc(p⁺)≤ₒ∫p⁺ 经 fc-continuous 自循环（结构性）→ 改用更基础 `fc-integral` 直接降为可证定理——桥接减一，fc 侧唯一剩余 D 类 = fc-integral |
| v1.35 | ln15-arith-ax 尝试 | 逻辑链完备（refl 级），组装触发 Agda 内存不足 → 确认为**工程计算资源不足**（非结构性），保留 scoped 公理 |
| v1.36 | 谱对象映射完整 | HilbertSpace §12' `A-hilb`/`fc-hilb`（谱定理降定理链端点桥接）+ SpectralObjPt 扩展 A/fc 字段——**谱对象映射（A/E/fc/exp-tA）完整闭合** |

### 4.4 关键技术决策

1. **方案 A 正负分解（∫f = ∫f⁺ −ₒ ∫f⁻）**：完全避开 sup 的加法/线性公理，`spec-int-general-decomp` 桥接 + 非负一致性（`spec-int-nonneg-consistent`）保证新旧定义对非负函数一致；定义重构破坏面过大，改走"decomp 显式化"路线（破坏面为零）。
2. **依赖循环解决（v1.34）**：fc(p⁺)≤ₒ∫p⁺ 经 fc-continuous 自循环为结构性（p⁺ 非多项式侧唯一工具是 fc-continuous/fc-integral），改用更基础 `fc-integral`（§5c，fc = ∫，谱定理函数演算，与 spec-int-A 同层 D 类）直接降 `fc-poly-le-spec-int`——桥接减一。
3. **术语统一（v1.35）**：scoped 数值公理（`ln15-arith-ax` 等）归类标注由"资源/实践静默"改为 **"工程计算资源不足"**（实测确认：refl 级闭合逻辑完备，但 2994494400 级大数归一化触发 `osCommitMemory: VirtualAlloc MEM_COMMIT failed`）。

---

## 5. 剩余开放项与登记公理

### 5.1 结构性限制（B 类，不可/不应闭合）

1. **funext 受限**（8-5b 算子层等式版公理 + 对象映射 op-lin 等式保结构）——库公理范围外。
2. ~~**`HigherSpCategory.lean` spExchangeLaw `sorry`**~~——✅ **已消除**（2026-08-04，改为偏差定理引用 `spExchangeLaw_homotopy_deviation`）。原概念特征（非技术缺口）：填补为等式 ⇒ $G_N \to 0$（物理错误），已由 `spExchangeLaw_deviation_partial_commutator` / `spExchangeLaw_homotopy_deviation` 覆盖。
3. **钉住 sup 语义**（spec-int-general 定义语义）——框架设计决策，已文档化（§1b）。

### 5.2 待基础设施（C 类，可自然闭合）

1. **`DeviationBound.lean` 2 个 `sorry`**——依赖 Mathlib `Matrix.Spectrum` 模块稳定。
2. **T3 阶段 3 scoped 数值公理**（`ln15-arith-ax`；`ln1615-lb` 与 `ln2-lt` **已于 2026-08-05 闭合为定理**：exp/log 级数机制 + 二进制 ℕ 算术）——纯有理/数值比较，逻辑完备但工程计算资源不足；降定理路径 = 算术决策机制/反射或更高效 ℕ 算术。

### 5.3 结构性障碍：R11 有限维态射层（S0 表示静默）

B3 R11 有限维 SpImD 态射层**结构性不可闭合**（基数反例）：2 状态平凡系统下 Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）vs Hom_Rec(X,Y) = 4（有限），无双射；P=[[1,0],[1,1]] 是合法谱态射但非转移矩阵（D 的 full 性为假）。闭合仅当态射限制为转移矩阵（平庸化）或转无限维（论文 R11 断言，需 T3 谱定理验证）。定性为 **S0 表示静默**——$P_{\mathrm{Im}(D)}(\varphi)=0$（谱态射在递归表示下不可达；编码前静默，与 S1–S4 的编码后不可观测平行独立），静默体系由四层扩为五层（S0 + S1–S4）。sieve 判定为**负**（S0 静默态射类不构成 sieve：左、右复合均破坏静默——复合后 S_D 中位数 0.294、73% 压到 <0.5），与 S1–S4（构成 sieve）形成静默体系内部"筛/非筛"二元结构。推进方向：P0 论文层范围修正（已执行）→ P1 R11 无限维严格验证（决定性：若无限维谱匹配断言成立则伴随在无限维闭合、S0 仅出现在有限维原型；若不成立则 S0 为结构性普遍现象）→ P2 静默筛理论结构、P3 物理对应研判、P4 基数反例形式化（均已执行）。

---

## 6. 声明边界与结论

**可诚实声称**：

1. Agda 16 模块全量类型检查通过（`Everything.agda` exit=0），与 Lean 主实现形成双类型论交叉验证。
2. 纯结构核心（B1-B8 组合/代数/集合结构）直接证明，无 postulate 依赖。
3. 谱匹配核心（theorem3/corollary4-∞/corollary5/P1-linear-closure）零桥接依赖完全可证。
4. 技术债清单 A 类（实质可闭合项）全闭合：E-σ-add 收敛、spec-int MCT、fc-poly-le-spec-int（方案 A）、谱对象映射（A/E/fc/exp-tA）。
5. Lean 侧核心模块 `lake build` 零错误；`spExchangeLaw` sorry 已消除（2026-08-04），`Adjunction.lean` 阶段 1 圈定后 sorry 从 8 处降至 4 处 + 1 处 axiom（对齐 Agda postulate）。

**不可声称**：

1. "全部闭合/零公理"——ℝ 公理体系是基础假设层；scoped 数值公理因工程计算资源不足保留登记；fc-integral 本身为谱定理层模型保证（D 类登记）。
2. R11 无限维态射层的完整闭合——有限维侧为 S0 结构性障碍，无限维侧断言（论文 R11）依赖 T3 谱定理，待严格验证。

**结论**：Agda 独立交叉验证是 UFPF 形式化体系可信度的关键组成部分。它在与 Lean 正交的类型论体系下独立证明纯结构核心，并以登记纪律将分析层假设透明化。技术债清单 A 类全闭合后，剩余开放项均为结构性限制（funext、概念特征、S0 静默）或待基础设施（Mathlib 稳定、大整数算术机制），无实质技术债遗留。

---

## 版本记录

| 版本 | 日期 | 主要变更 |
|:---:|:---:|:---|
| v0.1 | 2026-08-03 | 初版。系统说明 Agda 交叉验证目的、16 模块清单、双实现一致性、闭合历程（v1.17–v1.36 技术债 A 类全闭合）、剩余开放项与声明边界。内容自包含。 |
