# UFPF v0.39 发布说明（Release Notes）

**版本**：v0.39（Git tag：`rap-errata-v0.39`）
**日期**：2026-08-13
**Commit**：`2c1f165fb4`（master = develop = origin，已推送）
**范围**：Lean 去重合并与登记册体系 + 口径偏差修正（21 文件，+658/-121）

---

## 1. 发布概览

本次发布围绕 **Lean 形式化代码库的重复建设治理与口径统一**，以论文为权威来源完成：
1. 全库扫描（96 文件 / 1505 顶层声明）→ 检出 25 组重名 → 核查确认 9 项重复建设候选；
2. 建立 **Lean-论文登记册**（`formal_proof/lean_deduplication_tracker.md`）与 **判定对比报告**（`formal_proof/lean_deduplication_report.md`），形成防复发机制；
3. 修正 3 项论文↔代码口径偏差 + Cl(9,1) 系列代数同构笔误。

---

## 2. 修正项

### 2.1 Lean 重复建设 9 项判定（依据论文来源与推导角色）

| # | 候选 | 判定 | 说明 |
|:--|:-----|:----:|:-----|
| ① | `LayerIndex`（BranchCounting 5 层 vs CategoryGeometryDictionary 4 层） | ✅ **合并** | 同一论文出处（paper31 J3 §4.1 层结构表 = 5 层）；CategoryGeometryDictionary 删本地定义，`import BranchCounting` 复用母定义，`isCoherenceLayer` 改 `.four`；`directionMap` 对任意层（含对象层）一致成立 |
| ② | d_H 常量（e/ln15/N_total/r/d_H_fit/delta_fit：BranchCounting vs DHStructuralAnalysis） | ❌ 不合并（已恢复） | 数值相同但**推导角色不同**：BranchCounting 侧为自底向上推导结论（`total_layers_count` 机器证明、定理 R1 谱静默因子），DHStructuralAnalysis 侧为自顶向下推导前提/纯常数。**曾误删，已 `git checkout` 恢复** |
| ③ | `GenSpace`（FlavorFiber vs Unified3Theorem） | ❌ 不合并 | Unified3Theorem 明确"为解除依赖链耦合的有意副本"，保留 + 交叉注释 |
| ④ | `k_max`/`k_max_value`（Unified3Theorem vs BottTower） | ❌ 不合并（已恢复） | 论文来源不同：k_max=8 = 统一 3 定理 2^N_active（paper20/21）vs BottTower = spinorDim 0（Bott 塔翻倍工作基准）。**曾误删，已恢复** |
| ⑤ | `frobeniusNorm`（RAP4 ℝ 桥接 vs Silence ℂ 自建） | ❌ 不合并 | 标量域不同（ℝ vs ℂ）、语义同族；注释标注"新增使用优先 mathlib ‖A‖" |
| ⑥ | `adjUnit`/`adjCounit`（Adjunction 抽象 vs RAP5a 实例） | ❌ 不合并 | 不同函子（DFunctor vs DIm），同一伴随概念两个实现层级 |
| ⑦ | 静默度三变体（S_D/silenceDegree/deltaSilence） | ❌ 不合并 | 同族公式、三种语义（对易子/投影/表示层）；注释统一同族结构 |
| ⑧ | SilenceLevel/SilenceLayer/LayerIndex 近名 | ❌ 不合并 | 近名不同义（分级/数据表/层索引）；双向交叉注释（命名信息偏差高风险源） |
| ⑨ | `spectralSilence` vs `spectralSilenceSimple` | ❌ 不合并 | 功能子集的有意简化变体；注释标注"勿扩展为第三个版本" |

**方法论沉淀**（登记册/报告）：数值/字面相同 ≠ 重复——判定须核查**论文出处与推导角色**（推导结论 / 推导前提 / 纯数学常数 / 唯象拟合）。

### 2.2 论文↔代码口径偏差修正（3 项）

| # | 偏差 | 修正 |
|:--|:-----|:-----|
| ① | SilenceHierarchy 头部"四层静默/定理 5.18"为旧口径 | paper1 §5.7 现为**五层**（S0 表示层 + S1-S4），严格层次为**定理 5.15**。修正：SilenceHierarchy.lean 头部 + 4 处定理编号；paper19 L720/L987 同步 |
| ② | Cl(1,7)≅M₈(ℝ)/旋量 8 旧记 | 权威口径 M₁₆(ℝ)/旋量 16（paper20 v0.6）。修正：SpectralGap、BottTower 表格、NoiseFiber、SignatureFiber（+同类 NoiseFiber/SignatureFiber 顺带修正） |
| ③ | FlavorFiber 注释"d_H from Paper XV"为笔误 | 实为 paper17 §3（d_H=ln15+δ）；修正注释 + 勘误标注 |

### 2.3 Cl(9,1) 系列延伸修正

- **SignatureFiber** `sig_91`：Cl(9,1)≅M₁₆(ℝ)（误）→ **M₃₂(ℝ)**（权威 paper20 L518/paper33 L122）；
- **BottTower** 表格：真实旋量（16/32/64/128）与工作基准 spinorDim(k)=8×2^k **分离标注**，消除"32 = 8×2¹"矛盾；
- **paper21** L735：Cl(17,1)≅M₅₁₂(ℝ)（笔误，512=2⁹）→ **M₆₄(ℝ)/64 维**（权威 paper20/33）。

### 2.4 登记册体系（新增资产）

- `formal_proof/lean_deduplication_tracker.md`：判定准则、论文索引、9 项判定、**全库 96 文件登记表**（8 组，论文出处+核心符号+推导角色）、防复发清单、口径偏差记录；
- `formal_proof/lean_deduplication_report.md`：9 项判定详细对比报告（新人查阅）、判定流程图、误删教训、变更时间线。

---

## 3. 测试结论

| 测试 | 结果 |
|:-----|:-----|
| **Lean 编译**（`lake build`） | ✅ **2454 jobs 零警告零 sorry** |
| **Python 数值回归**（run_all_tests.py，282 脚本） | ✅ **检查项 1300/1300 通过（100%）** |
| **范畴理论验证**（verify.run_all V1-V8） | ✅ **8/8 通过**（Sp 严格 4-范畴 / D 函子忠实 / D⊣R 三角恒等式 / 谱对应自然性 / 统一 3 定理 / 不等式链 / c₁<c₂<c₃ / Δ 代数形式） |

**6 个标 FAIL 脚本核查结论**（均与本次改动无关，本次零 .py 变更）：
- 5 个页岩（paper43）脚本：`?` 标注 = **诚实负结果登记**（负结果/根因诊断为论文设计的一部分），非代码错误；
- `verify.run_all`：集成运行环境性误报——单独运行 **V1-V8 8/8 通过**（exit code 来自 Python runpy 的 sys.modules 警告）。

**结论**：本次发布**未引入任何新错误**。全部改动为 Lean 注释层 + 论文/登记册 markdown；Lean 编译、范畴理论验证、Python 数值回归全绿。

---

## 4. 文件变更清单（21 文件，+658/-121）

**Lean 文件（14）**：修改 12——BottTower、DeviationBound、FlavorFiber、MultiSilenceMethodology、NoiseFiber、PhotonTopology2Lifting、RAP4、RAP5a、SignatureFiber、Silence、SilenceHierarchy、SpectralGap；新增 1——CategoryGeometryDictionary.lean（字典逐层化 + LayerIndex 合并）；删除 1——PhotonTopologyOrthogonality.lean（mathlib HasLiftingProperty 重复实例化包装）。注：BranchCounting.lean 曾误删后恢复，恢复后与历史版本一致（无净变更）。
**新增文档（2）**：lean_deduplication_tracker.md、lean_deduplication_report.md
**论文/笔记/路线图（5）**：paper19（定理 5.15 同步）、paper21（Cl(17,1) 修正）、paper44、phase62 路线图、photon_first_principle_origin.md

---

## 5. 发布状态

- 分支：`master` = `develop` = `origin`（fast-forward 合并，无分叉）；
- Tag：`rap-errata-v0.39` 已推送至 origin；
- 版本链：v0.38（paper44 引力时间膨胀）→ **v0.39**（Lean 去重与口径统一）。

**后续建议**：全库登记表已就绪，新建/修改 Lean 文件前查登记册 + grep 查重（防复发清单），确保不再出现"另起炉灶"。
