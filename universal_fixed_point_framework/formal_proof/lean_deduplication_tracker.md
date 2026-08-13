# Lean 去重合并跟踪（Lean Deduplication Tracker）

**目的**：跟踪 UFPFormalization 中重复建设（"另起炉灶"）的合并进度，防止丢失上下文后继续产生重复定义。
**规则**：任何新 Lean 文件在定义顶层符号前，必须先 grep 该符号是否已存在（含 mathlib）；母定义一律保留，子文件 import + 限定名引用。

## 合并方案总表

| # | 重复项 | 母定义（保留） | 重复处（合并） | 状态 | 备注 |
|:--|:-------|:--------------|:---------------|:----:|:-----|
| ① | `LayerIndex` 双定义 | BranchCounting（5 层：obj+one/two/three/four） | CategoryGeometryDictionary（4 层：layer1-4） | ✅ 已完成 | CategoryGeometryDictionary 删本地定义，import BranchCounting；`isCoherenceLayer` 改 `.four`；directionMap 对 obj 层一致成立（字典核心不依赖层） |
| ② | d_H 结构常数批量复制（e/ln15/N_total/N_active/B/B_eq_15/r/d_H_fit/delta_fit/dH_from_branching） | DHStructuralAnalysis | BranchCounting（子 namespace 重定义） | ✅ 已完成 | BranchCounting 删 e/ln15/r/d_H_fit/delta_fit/N_total 6 个重定义 + `open DHStructural`；B/B_eq_15（LayerIndex 计数推导）与 dH_from_branching（无参数形式）保留为独立推导 |
| ③ | `GenSpace` 双定义（ℂ³） | FlavorFiber | Unified3Theorem（注释已标"原定义在 FlavorFiber"） | ✅ 已核查保留 | **有意副本**（Unified3Theorem 注释"为解除对损坏依赖链的耦合"）；FlavorFiber 侧补反向注释，不强制 import（避免拉入重依赖链） |
| ④ | `k_max`/`k_max_value` 双定义 | Unified3Theorem | BottTower | ✅ 已完成 | BottTower 删 k_max/k_max_value，open Unified3；新增 `k_max_eq_spinorDim_zero` 保留"k_max = Bott 塔基础层旋量维数"结构连接 |
| ⑤ | `frobeniusNorm` 双实现 | RAP4（mathlib `‖A‖` 桥接，ℝ） | Silence（自建 `Real.sqrt ∑normSq`，ℂ） | ✅ 已核查保留 | 标量域不同（ℝ vs ℂ）；Silence 侧注释标注"勿新增第三处，优先 mathlib `‖A‖`" |
| ⑥ | `adjUnit`/`adjCounit` 双实现 | Adjunction（抽象伴随） | RAP5a（线性语义 SpImD 实例） | ✅ 已核查保留 | 不同函子（DFunctor/RFunctor vs DIm/RIm），同一概念两个实现层级；RAP5a 侧注释"新增优先复用 Adjunction 抽象定义" |
| ⑦ | 静默度三变体（S_D / silenceDegree / deltaSilence） | —（同一公式三处命名） | RAP4 `silenceDegree` + Silence `deltaSilence` | ✅ 已核查保留 | Silence `deltaSilence` 注释统一三者的"范数比定义静默度"同族结构（对易子/投影/表示层） |
| ⑧ | 层术语混乱（SilenceLevel / SilenceLayer / LayerIndex / categoricalLevel） | — | 四处近名不同义 | ✅ 已核查保留 | RAP4 `SilenceLevel` ↔ MultiSilenceMethodology `SilenceLayer` 双向交叉注释，明确与 `LayerIndex` 不同义 |
| ⑨ | `spectralSilence` vs `spectralSilenceSimple` | Silence `spectralSilence`（S1-S4 完整） | SilenceHierarchy `spectralSilenceSimple`（S1∧S2 子集） | ✅ 已核查保留 | 功能子集的有意简化；注释标注"勿扩展为第三个版本" |

## 执行记录（变更日志）

| 日期 | 项 | 变更 | lake build | 备注 |
|:-----|:---|:-----|:----------:|:-----|
| 2026-08-13 | — | 全库扫描（96 文件/1505 声明，25 组重名），核查确认 9 项重复建设 | 2454 jobs ✅（基线） | 临时脚本 scan_lean_dupes.py 已删除 |
| 2026-08-13 | ② | BranchCounting 删 e/ln15/r/d_H_fit/delta_fit/N_total 重定义 + `open UFPFormalization.DHStructural` | 2454 jobs ✅ | — |
| 2026-08-13 | ④ | BottTower 删 k_max/k_max_value，新增 k_max_eq_spinorDim_zero 结构连接 | 2454 jobs ✅ | — |
| 2026-08-13 | ① | CategoryGeometryDictionary 删本地 LayerIndex，import BranchCounting + open，isCoherenceLayer 改 `.four` | 2454 jobs ✅ | 层数约定统一为 5 层母定义 |
| 2026-08-13 | ③ | FlavorFiber.GenSpace 补反向注释（确认有意副本，不合并） | 2454 jobs ✅ | — |
| 2026-08-13 | ⑤⑦ | Silence.lean：frobeniusNorm 与 deltaSilence 注释（同族标注 + 勿新增第三处） | 2454 jobs ✅ | — |
| 2026-08-13 | ⑥ | RAP5a adjUnit 注释（与 Adjunction 两个实现层级） | 2454 jobs ✅ | — |
| 2026-08-13 | ⑧ | RAP4 SilenceLevel ↔ MultiSilenceMethodology SilenceLayer 双向注释 | 2454 jobs ✅ | — |
| 2026-08-13 | ⑨ | SilenceHierarchy spectralSilenceSimple 注释（功能子集有意简化） | 2454 jobs ✅ | — |

## 防复发清单（新建/修改 Lean 文件前必查）

1. **grep 符号名**：`Grep pattern="^def|^theorem|^structure|^inductive|^abbrev|^class" path=UFPFormalization` 确认不重复；
2. **同概念近名检查**：Layer/Level/Silence/Degree/Norm 等词根可能近名不同义，优先复用母定义 + namespace 限定；
3. **import 而非重定义**：需要既有定义时 `import UFPFormalization.<母文件>` + 限定名引用，禁止复制到新 namespace；
4. **合并后验证**：每项合并后 `lake build` 必须保持 2454 jobs 零警告零 sorry；
5. **跨上下文同步**：论文/笔记/路线图/RAP 中引用被删符号处同步更新（参照 2026-08-13 PhotonTopologyOrthogonality 清理流程）。
