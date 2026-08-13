# Lean 重复建设 9 项判定详细对比报告

**日期**：2026-08-13
**范围**：UFPFormalization（96 个 Lean 文件，1505 个顶层声明，扫描检出 25 组重名，核查后确认 9 项候选）
**原则**：以论文为权威来源——数值/字面相同的符号**不等于重复**，须核查论文出处与推导角色（结论 vs 前提 vs 常数 vs 唯象拟合）。
**配套文件**：[lean_deduplication_tracker.md](lean_deduplication_tracker.md)（登记册：判定准则、论文索引、防复发清单、Lean→论文索引）

---

## 0. 判定方法论（新人必读）

重复建设的正确判定流程：

1. **扫描重名**：脚本提取各文件顶层声明（def/theorem/structure/inductive/class/abbrev），找跨文件同名；
2. **核查论文出处**：定位每个符号在论文中的登记——哪个论文、哪一节、什么角色；
3. **区分推导角色**（本报告核心）：
   - **推导结论**（自底向上）：从结构证明导出的值（如从归纳类型计数证出 N_total=5）；
   - **推导前提/输入**（自顶向下）：作为推导的假设参数（如"设均匀收缩率 r=e⁻¹"）；
   - **纯数学常数**：e、ln15 等与框架无关的常数定义；
   - **唯象拟合**：由实验/χ² 拟合的数值（如 d_H_fit=2.7095）；
4. **判定**：仅当"同一论文 + 同一角色 + 纯复制"才合并；否则保留 + 交叉注释。

**核心教训（2026-08-13 实证）**：BranchCounting 与 DHStructuralAnalysis 的 e/ln15/r 等**数值完全相同**，曾据此误判为重复而删除——实际两者推导角色不同（一为结论、一为前提），属来源不同的参数。已全部恢复。

---

## 1. 九项判定总览

| # | 候选 | 判定 | 处理 | 文件 |
|:--|:-----|:----:|:-----|:-----|
| ① | LayerIndex（5 层 vs 4 层） | ✅ 合并 | CategoryGeometryDictionary 复用 BranchCounting | ① |
| ② | d_H 常量（e/ln15/r/N_total/d_H_fit/delta_fit） | ❌ 不合并 | 已恢复 | ② |
| ③ | GenSpace（ℂ³ 双定义） | ❌ 不合并 | 保留 + 注释 | ③ |
| ④ | k_max/k_max_value | ❌ 不合并 | 已恢复 | ④ |
| ⑤ | frobeniusNorm（ℝ vs ℂ） | ❌ 不合并 | 保留 + 注释 | ⑤ |
| ⑥ | adjUnit/adjCounit（抽象 vs 实例） | ❌ 不合并 | 保留 + 注释 | ⑥ |
| ⑦ | 静默度三变体（S_D/silenceDegree/deltaSilence） | ❌ 不合并 | 保留 + 注释 | ⑦ |
| ⑧ | SilenceLevel/SilenceLayer/LayerIndex 近名 | ❌ 不合并 | 保留 + 注释 | ⑧ |
| ⑨ | spectralSilence vs spectralSilenceSimple | ❌ 不合并 | 保留 + 注释 | ⑨ |

---

## ① LayerIndex：✅ 合并（唯一合并项）

**定义位置**
- BranchCounting.lean:47：`inductive LayerIndex`（**5 层**：obj/one/two/three/four，层 0 对象 + 层 1-4 态射，`deriving DecidableEq, Fintype`）
- CategoryGeometryDictionary.lean:82（已删）：`inductive LayerIndex`（**4 层**：layer1/layer2/layer3/layer4）

**论文来源**：paper31 §4.1 层结构表 = **5 层**（层 0 对象 + 层 1-4；层 1-3 正交于 Δ、层 4 coherence = Δ 所在层）。BranchCounting 与之完全一致；CategoryGeometryDictionary 为 4 层子集（去层 0，paper44 语境）。

**角色对比**：两者均为"Sp 4-范畴态射层层索引"的同一概念，仅是否含对象层之差。

**判定依据**：同一论文出处（paper31 J3 §4.1）；BranchCounting 为完整 5 层实现，CategoryGeometryDictionary 为子集用法。层数差异（5 vs 4）源于是否含对象层，非语义分歧。

**处理（2026-08-13，用户确认）**：CategoryGeometryDictionary 删本地定义，`import UFPFormalization.BranchCounting` + open；`LayerIndex.isCoherenceLayer` 改 `.four`；`directionMap` 对任意层（含 obj 层）一致成立（字典核心不依赖层）。`lake build` 2454 jobs ✅。

---

## ② d_H 常量（e/ln15/N_total/r/d_H_fit/delta_fit）：❌ 不合并（曾误删，已恢复）

**定义位置**
- BranchCounting.lean:56/121/124/127/164/167（N_total/r/e/ln15/d_H_fit/delta_fit）
- DHStructuralAnalysis.lean:43/46/52/55/78/81/90（同名单常量）

**论文来源与角色对比**：

| 常量 | BranchCounting 侧（自底向上推导结论） | DHStructuralAnalysis 侧（自顶向下推导前提/常数） |
|:-----|:-------------------------------------|:------------------------------------------------|
| r = e⁻¹ | **定理 R1 推导值**（几何级数 + 生成元匹配 + 双重最优性，RAP 勘误 L74）；paper17："味物理选定的特例" | "均匀收缩率"推导**前提 2** |
| ln15 | 分支计数 + Moran/Bowen 方程**机器证明**结论（paper17 L49） | §1 纯数学常数定义（`Real.log 15`） |
| N_total=5 | 关联 `total_layers_count : Fintype.card LayerIndex = 5`（**归纳类型计数机器证明**） | d_H=ln15 结构推导的**前提输入** |
| d_H_fit=2.7095 | 唯象拟合登记 | 唯象拟合登记 |
| delta_fit | 偏差定义 | 偏差定义 |
| N_active=3 | — | 统一 3 定理推论（前提） |

**判定依据**：数值相同但**推导角色不同**——BranchCounting 侧是从结构证明导出的结论（删除会破坏"结构→参数"推导方向性），DHStructuralAnalysis 侧是推导的输入前提。不构成重复建设。

**处理**：2026-08-13 曾误删 BranchCounting 六定义（仅比较数值相等），用户裁定"来源不同的参数"，已 `git checkout c0edbb4fb1 -- BranchCounting.lean` 全部恢复。**此为判定方法论的负面案例，新人必读**。

---

## ③ GenSpace（ℂ³ 双定义）：❌ 不合并（有意副本）

**定义位置**
- FlavorFiber.lean:67：`abbrev GenSpace : Type := ℂ × ℂ × ℂ`（原定义）
- Unified3Theorem.lean:100：同名同内容 `abbrev GenSpace`（注释："为解除对损坏依赖链的耦合，此处本地定义（同一类型）"）

**判定依据**：Unified3Theorem 注释明确这是**有意的本地副本**（历史依赖链损坏时解除耦合的决策）。强制合并（改 import FlavorFiber）会把 FlavorFiber 的重依赖链（TempRGFiber/YukawaIFSWeights/IFSFractal）拉入核心推导路径，违背原设计。

**处理**：保留两处；FlavorFiber 侧补反向注释（"Unified3Theorem.lean 存在同型本地副本，为解除依赖链耦合的有意副本"）。

---

## ④ k_max / k_max_value：❌ 不合并（曾误删，已恢复）

**定义位置**
- Unified3Theorem.lean:220/223：`def k_max : ℕ := 8` + `k_max_value : k_max = 8 := by rfl`（数值定义）
- BottTower.lean:121/124（已恢复）：`def k_max : ℕ := spinorDim 0` + `k_max_value`（Bott 塔结构定义）

**论文来源**：
- **k_max=8 权威来源 = 统一 3 定理（2^N_active = 2³）机器证明 + 对偶网络（B = 2k_max−1）**——paper20 L439 / paper21 L734；
- BottTower 的 spinorDim(0)=8 = **Bott 塔翻倍"工作基准"**——paper2 L219 诠释 + 2026-08-07 勘误定位（"k_max=8 不再声称来自 Cl(1,7) Bott 分类"，勘误后为模型选择 + 统一 3 定理主动层数；spinorDim 保留为工作基准，见 BottTower 注释勘误注）。

**判定依据**：数值同为 8，但**论文来源不同**（统一 3 定理 vs Bott 塔翻倍工作基准），角色不同。合并会丢失 spinorDim 结构连接与勘误语义。

**处理**：已恢复（与 ② 同批次）。若未来需要连接两处，应在 BottTower 加结构连接定理（如 `k_max_eq_spinorDim_zero`），而非删除定义。

---

## ⑤ frobeniusNorm：❌ 不合并（不同标量域）

**定义位置**
- RAP4_silence_strictification.lean:45：`abbrev frobeniusNorm {m n} (A : Matrix (Fin m) (Fin n) ℝ) := ‖A‖`（mathlib 桥接，ℝ）
- Silence.lean:94：`def frobeniusNorm {n} (A : Matrix (Fin n) (Fin n) ℂ) := Real.sqrt (∑ Complex.normSq)`（自建，ℂ，早期实现）

**判定依据**：标量域不同（ℝ vs ℂ），实现路径不同（mathlib 类型类 vs 自建求和）。语义同族（均为 Frobenius 范数）。合并需泛化标量域，改动大且牵动多个证明。

**处理**：保留两处；Silence 侧注释"新增使用优先采用 mathlib `‖A‖`（泛化标量域），勿新增第三处定义"。

---

## ⑥ adjUnit / adjCounit：❌ 不合并（不同函子实例）

**定义位置**
- Adjunction.lean:49/63：`adjUnit (X : RecObj) : X ⟶ RFunctor (DFunctor.obj X)`（抽象伴随，显式构造）
- RAP5a_explicit_adjunction.lean:138/142：`adjUnit (S : RecObj) : S ⟶ (DIm.comp RIm).obj S := 𝟙 S`（线性语义 SpImD 实例，DIm/RIm 为本文件定义）

**判定依据**：同一伴随概念的两个**实现层级**——函子不同（DFunctor/RFunctor vs DIm/RIm）、目标类型不同。RAP5a 是 RAP-5a（显式余伴随构造清除循环论证）的专项实例，未 import Adjunction.lean（类型不直接兼容）。

**处理**：保留两处；RAP5a 侧注释"同一伴随概念两个实现层级；新增伴随结构应优先复用/实例化 Adjunction.lean 抽象定义"。

---

## ⑦ 静默度三变体（S_D / silenceDegree / deltaSilence）：❌ 不合并（同族公式、三种语义）

**定义位置**
- paper1 §5.7.9 `S_D(φ) = 1 − ‖P_Im(D)(φ)‖/‖φ‖`（**D-静默度**：投影到转移矩阵像 Im(D)，表示/编码层；论文级定义）
- RAP4_silence_strictification.lean:265 `silenceDegree = 1 − ‖P·Df‖/‖Df‖`（**投影剩余**：投影到子空间 P）
- Silence.lean:105 `deltaSilence = ‖[A,G]‖_F`（**对易子范数**：连续静默度）

**判定依据**：三者共享"范数比定义静默度"的同一数学形式，但**语义各自限定**（对易子缺陷 / 投影剩余 / 表示层可达性）。合并会混淆语义层级。

**处理**：保留三处；Silence `deltaSilence` 注释统一三者的同族结构（对易子/投影/表示层），指引后续查阅。

---

## ⑧ 层术语近名（SilenceLevel / SilenceLayer / LayerIndex）：❌ 不合并（近名不同义）

**定义位置与语义**：
| 名称 | 文件 | 语义 |
|:-----|:-----|:-----|
| `SilenceLevel` | RAP4_silence_strictification.lean:278 | 静默**严格性分级**（strict/asymptotic/epsilon） |
| `SilenceLayer` | MultiSilenceMethodology.lean:132 | 静默**层数据记录**（S1-S4，name/value/interpretation/categoricalLevel） |
| `LayerIndex` | BranchCounting.lean:47 | **4-范畴态射层索引**（obj/one/two/three/four） |

**判定依据**：三个名称高度相似但语义不同（分级 vs 数据表 vs 层索引）。这是**命名信息偏差的高风险源**——正是此类近名导致"另起炉灶"（新文件作者以为无实现而重写）。

**处理**：三处双向交叉注释，明确不同义 + 限定 namespace 引用指引。

---

## ⑨ spectralSilence vs spectralSilenceSimple：❌ 不合并（功能子集的有意简化）

**定义位置**
- Silence.lean:80 `spectralSilence`（**完整版**：S1-S4 判据，参数 τ w）
- SilenceHierarchy.lean:60 `spectralSilenceSimple`（**简化版**：仅 S1∧S2，单矩阵参数）

**判定依据**：简化变体为功能子集（SilenceHierarchy 注释已说明"此处保留单矩阵参数的简化变体"），服务于 SilenceHierarchy 的单矩阵使用场景。属有意简化，非无意重复。

**处理**：保留；注释标注"功能子集的有意简化变体，勿扩展为第三个版本，统一使用 Silence.spectralSilence 完整版"。

---

## 10. 防复发清单（新人操作指引）

新建/修改 Lean 文件前必查：

1. **查登记册**（[lean_deduplication_tracker.md](lean_deduplication_tracker.md)）：确认符号/概念是否已有论文登记；
2. **grep 符号名**：`Grep pattern="^def|^theorem|^structure|^inductive|^abbrev|^class" path=<UFPFormalization>` 确认不重复；
3. **核查论文来源**：数值/字面相同 ≠ 重复——须确认论文出处与推导角色（结论/前提/常数/唯象），禁止凭代码表面特征判定；
4. **import 而非重定义**：确认为纯复制时 `import UFPFormalization.<母文件>` + 限定名引用；
5. **合并后验证**：`lake build` 必须保持 2454 jobs 零警告零 sorry；
6. **跨上下文同步**：论文/笔记/路线图/RAP 引用被删符号处同步更新（参照 2026-08-13 PhotonTopologyOrthogonality 清理流程）。

**判定流程图**：

```
发现同名/近名定义
  → 查登记册 + 论文出处
  → 同一论文？ ──否──→ 不同论文：登记各自来源，保留
  → 同一推导角色？ ──否──→ 结论 vs 前提/常数：保留 + 交叉注释
  → 纯复制？ ──否──→ 有意副本/不同标量域/不同实例：保留 + 注释
  → 是：合并（保留母定义，import 引用）
```

---

## 附：变更时间线（2026-08-13）

| 提交 | 内容 |
|:-----|:-----|
| c33c5cadc4 | 首次去重合并（凭代码表面特征判定）——**含 ②④ 误删** |
| 7fd3c8149f | 全部恢复 + 登记册框架（以论文为权威） |
| f66a588531 | 登记册阶段 1（定理 R1 / k_max=8 / d_H=ln15 论文证据；②④ 判定不合并、① 倾向合并） |
| 3c02bba3bb | 登记册附录（Lean→论文初筛索引） |
| b4293ae8b3 | 最终判定执行：① 合并（用户确认）；⑤-⑨ 交叉注释 |
