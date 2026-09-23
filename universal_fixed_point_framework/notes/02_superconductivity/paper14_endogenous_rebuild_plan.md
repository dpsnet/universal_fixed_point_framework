# 研究笔记：paper14 凝聚态谱表述的内生第一性重建——从范畴 Δ 出发的缺口分析与重建规划

**文档编号**：MUFPF-RN-ENDO-001
**日期**：2026-09-12
**版本**：v1.3
**状态**：G1–G6 全部建立有限维可证核心并登记开放项；**§4 新增"起点分层"（2026-09-18 记档）：凝聚态侧工作起点=规范/表示层（对易子→SU(2)→Casimir→spectralGap，不经 Δ，Lean 全证独立），范畴 Δ 支降级为远期"运输函子 𝒯"统一目标（结构同一未成立，仅共享对易子原语 + spectralGap 标记，互不推导）；§3 G1 起点标注据此改判；RN-ENDO-010 §8.19 判定 `16=dim_ℝℍ²` 为维数恒等/模分解巧合、非代数内源，作为本判定的数值实例支撑**；G2 定量桥在"代数谱系"层面闭合（SuperfluidBridge.lean，2026-09-17），在"多级因子分解"层面闭合（SpectralFlowRG.lean，§8.7#5 代数因子分解层，Paper LVII v1.6），并进一步在"三级/多带谱隙谱系"层面闭合（MultibandSpectralBridge.lean，§8.6e 多带隙比保持 + Casimir 三级塔，Paper LVII v1.7），再在"尺度动力学诊断"层面落地（SpectralFlowDynamicsRG.lean，§8.6f 运行反常维度 + 非标度不变 + EM 残差流闭合，Paper LVII v1.8）；paper14 v1.6 内生标注体系重建（第一轮）完成，逐节全面标注为持续工作；**2026-09-19：G5（NoiseEffectiveEpsilon，paper14 v1.7）与 G4 代数核心（GPVortex，paper14 v1.8）双闭合**，详见 §8 尾部进度条目
**研究目标**：以「内生推导第一性」为标准重建 Paper XIV（凝聚态物理的谱表述）——每条推导链的起点必须是范畴 Δ（Sp 4-范畴交换律偏差，Paper XXXV）或由其已证的谱间隙资产，物理输入只允许出现在明确的边界上。

---

## 0. 动机

2026-09-12 的覆盖度核查（对照 Lean 库与数值资产）得出两个结论：

1. **Paper XIV 的"第一性推导"名不副实**。其推导链起点是输入的物理对象（BCS 平均场 Hamiltonian、材料参数），"第一性"的准确含义是「从谱公理（Paper V 谱流方程）出发」，而非「从范畴 Δ 出发」。按 paper54 定下的严谨标准，措辞需要修正或补链。
2. **真正从范畴 Δ 内生完成的全链只有引力侧**（paper54 涌现映射 L0→L6，Lean 全证）。凝聚态侧在「范畴谱间隙 ≡ 凝聚态序参量」这座桥面前集体止步。

本笔记立档重建目标，登记缺口，划定诚实边界，供后续 Phase 规划引用。

---

## 1. 三层起点的诚实核查（证据固化）

### 1.1 Paper XIV §2（BCS 能隙 = 谱间隙）

- 起点：`H_BCS` 平均场 Hamiltonian——标准物理输入；谱像 `D(H_BCS)` 翻译它。
- 论文自身有符号约定脚注：Δ_BCS 显式区别于 MUFPF 结构常数 Δ（Paper XXXV）。
- 性质：**翻译**，不是推导。谱流不动点条件 `dA_SC/dt = [A_pair, A_SC] = 0` 是自洽方程的重述。

### 1.2 Phase 70 超流刚度（SuperfluidStiffness.lean，零 sorry）

- 起点：Paper XIV §2.1 的 `A_SC = ξ_k σ_z + Δ σ_x`——Δ 作为给定参数。
- ρ₀ = Δ²/(2E_F) 与 T_c ∝ √ρ₀ 是**条件推导**（条件 = 谱间隙已给定、E_F 为输入）。
- 性质：谱公理层的干净推导，但未触及范畴 Δ。

### 1.3 WeaveBCS（Phase 55D，最接近内生的尝试）

- 锚点 `dl_min = spectralGap 8` 确实来自范畴-代数侧（Cl(1,7)/Bott，有 `SpectralGap`/`BottTower`/`CliffordSpectralType` 支撑）。
- 但桥 `r = dl_min / dl_BCS` 被定义为「基本自由参数」，由谱流自洽方程**数值解出** r ≈ 0.874（文件内 2026-08-04 开放项登记；注释记录若干原定理为伪陈述已降级）。
- 性质：**假设 + 数值闭合**，不是推导。这是 G2 缺口的直接证据。

---

## 2. 现有可锚定的内生资产

| 资产 | 状态 | 重建中的角色 |
|:---|:---|:---|
| 引力涌现映射 Δ → Hermitian → 度规 → 曲率 → Einstein（paper54，L0→L6） | Lean 全证（45 定理零 sorry） | 证明「Δ 内生」范式可行；方法论模板 |
| Paper XX 谱间隙第一性推导（Rec/Sp → SU(2) Casimir → Cl(1,7) → 谱间隙） | v0.5；Cl(1,7)/Bott/SpectralGap 段有 Lean 件 | 凝聚态内生链的代数前段（G1 的底料） |
| `WeaveBCS.lean` | 零 sorry（5 处 sorry 字样在注释中）；r 参数数值自洽 | G2 的正式化载体 |
| `SuperfluidStiffness.lean` | 零 sorry（未提交） | 重建后 §2 下游段的接收端 |
| SU(2) Casimir C₂=3/4、Cl(1,7) 谱间隙比 | `WeaveBCS`/`BottTower` 已证 | 预言 6.1 的内生基础 |
| IQHE 数值资产 | `src/iqhe_dual_param_rge.py`、`iqhe_critical_tmm_validation.py`、16 组数据 | G6 的验证工具 |
| EDRN 稳定岛独立验证 | notes + ED 计算（N=14/16），6 项 P-CM 裁决 | §5.8 无需重建（已是独立验证范式） |

---

## 3. 缺口清单（分级）

- **G1（核心）**：Δ → 谱间隙的凝聚态版推导链。Paper XX 链是引力版（v0.5）；需证明/泛化：同一范畴 Δ 经 SU(2) Casimir 谱与 Cl(1,7) 代数给出的谱间隙资产对凝聚态谱生成元同样适用。
- **G2（核心）**：范畴谱间隙 `dl_min` ≡ BCS 配对隙 `Δ_BCS` 的桥。现状：r 为自由参数 + 数值自洽（WeaveBCS 开放项）。目标：把 r 从「数值解」提升为「定理」——哪怕只在弱耦合极限或普适比值层面。
- **G3**：陈数/拓扑模块空白。Lean 库 grep `Chern/陈数` 零命中，TKNN 谱公式（定理 3.1）与陈数绝热不变性（命题 3.1）无法内生。需新建拓扑模块（Berry 曲率 → 第一陈数 → TKNN）。
- **G4**：GP 方程/涡旋模块空白。定理 4.1 的证明是启发式 sketch（A_GP = −log ρ + 连续性方程代入），命题 4.2（涡旋 = 规范分支）无载体。需形式化 GP-谱流等同的条件与涡旋拓扑荷守恒。
- **G5**：噪声范畴 ε_eff 占位定理真证。`NoiseCategory.lean` 的 `spectral_sequence_convergence`、`sel_diss_adjunction`、`noise_spectral_flow_eq` 均为 `True := trivial` 占位；ε_eff 闭式在 Lean 中零命中。Paper XIV §3.4 自称的"第一性原理推导"目前只是纸面解析推导。
- **G6**：IQHE RG 常数的地位裁定。定理 3.2/3.3 的 α≈1.16、ε₀≈2.58、γ₂≈0.06、ζ₀≈10⁻⁶ 为拟合常数。两条路：(a) 从谱投影尺子响应推导（理想）；(b) 明确降级为现象学输入并改措辞（诚实）。重建时必须二选一，不允许继续悬挂"第一性"措辞。

---

## 4. 结构性边界（诚实声明，不可逾越）

范畴 Δ 内生推导**只能产出普适量**：谱间隙比、Casimir 量化序列、无量纲标度指数、a_BCS 类普适比值、拓扑不变量。

**材料特定参数永远是输入侧**：E_F（Fermi 能）、n_imp（杂质浓度）、V（配对势强度）、m*（有效质量）、T_c 的数值。这些携带样品/材料信息，原则上不可由纯范畴结构给出。

因此「完全内生」的可达范围是：**普适结构层面**（无量纲比值、标度律形式、拓扑分类、量化规则），**不是数值预测层面**（具体材料的 T_c、Δ 值）。Paper XIV 重建后，每个命题必须带起点类型标注：

- 【内生-范畴】：从 Δ 或已证谱间隙资产出发；
- 【谱公理】：从谱流方程 + 明确物理输入出发（现状的大部分）；
- 【输入-现象学】：拟合/经验参数进入（须显式声明）。

**起点分层（2026-09-18 记档，v1.2；修正 G1"每条推导链起点必须是范畴 Δ"研究目标表述）**：

"从范畴 Δ 出发"须拆成两个被框架特意区分开的含义，二者是同一事实的两面，**不是二选一**：

- **共享"对易子原语"（已证）**：规范场（表示层）与范畴 Δ 同根——`CategoryRepBridge` 的 `G_GR=ad(G)(A)=[G,A]`（对易子）与其起点，正是范畴 Δ（spExchangeLaw 偏差）的代数内核（`commutator_trace_zero`、`commutator_diag_zero_of_diagonal`、`delta2Cell_commutator_*`）。同一根（对易子），两支（Δ 支 / 规范支）。
- **规范支"不从 Δ 出发"（已证，非妥协）**：结构推导路径 `对易子 → SU(2) → Casimir → agEigenvalue → spectralGap` 已被机器证明**独立于** Δ——`CategoryRepBridge` header 不 import DeviationBound/Δ，SU(2) 由 `[Jᵢ,Jⱼ]=iεᵢⱼₖ·Jₖ` 直接涌现，完全不经 spExchangeLaw。

**裁定 `Δ↔Casimir` 只建立语言同一 + 数值相容，结构同一未成立**（§8.9/RN-ENDO-010 v1.7 复核）：两支仅共享 `spectralGap` 标记，互不推导。据此**工作起点=规范/表示层**（谱公理 + 表示层，唯一有 Lean 证据、可落地的层面，全部比值级成果已在此闭合）；**范畴 Δ 支降级为远期统一目标**——唯一未闭合步骤是"范畴→表示"运输函子 𝒯（§8.7#5 核心），在该步骤落地前，数值内源问题不押在"从范畴 Δ 出发"上。

> 数值实例支撑：RN-ENDO-010 §8.19 判定 `16=dim_ℝℍ²` 为**维数恒等/模分解巧合、非代数内源**——"16"数值真、非同构内源；宿主 16 内源=既有 `2·k_max=spinorDim(Cl(1,7))`。此正说明"从范畴 Δ 强找数值内源"在**代数同构意义**上被裁定为不成立，与"规范/表示层是工作起点"的判定一致。

---

## 5. 重建路线（Phase 建议）

> **起点总标注（2026-09-18 同步，v1.2）**：本表各 Phase 已按 §4"起点分层"改判——**工作起点=规范/表示层**（对易子→SU(2)→Casimir→agEigenvalue→spectralGap，不经 Δ，Lean 已证独立），全部可落地成果汇入此层；范畴 Δ 支仅保留为远期"运输函子 𝒯"统一目标（结构同一未成立，见 §4）。下表凡标注【起点-规范/表示层】者直接可推进，标注【Δ支·远期𝒯】者须待 𝒯 落地。

**近期（补证据最痛处）**：
1. G5：NoiseCategory 占位定理真证 + ε_eff 闭式 Lean 化（Paper XIV §3.4 是全文唯一自称"第一性原理推导"的推导，名实差距最大）。**【起点-规范/表示层】**
2. G6 路线 (b)：若 (a) 短期不可行，先把定理 3.2/3.3 的措辞改为现象学声明。

**中期（桥与拓扑）**：
3. G2：r 的弱耦合极限定理化（WeaveBCS 已给出方程与数值锚点 r ≈ 0.874）。**→ 2026-09-17 已在"代数谱系"层面闭合**：δ_SC = Δλ_min/r* 的定理化（SuperfluidBridge.lean，零 sorry），详见 §8 尾；并在"多级因子分解"层面闭合（SpectralFlowRG.lean，§8.6d）、"三级/多带谱隙谱系"层面闭合（MultibandSpectralBridge.lean，§8.6e，Paper XIV §6.1 多带隙比预言定理化）、"尺度动力学诊断"层面落地（SpectralFlowDynamicsRG.lean，§8.6f：运行反常维度落带 + 非标度不变 + EM 残差流闭合）与"**谱流 RG 流单参数族**"层面落地（SpectralFlowRGFlow.lean，§8.6g：流不变折叠沿线保持 + β 通量∈(2/3,1) + β-形式 ODE 逆流解 + 运行指数沿流单调）；残余开放为 EM 尺度独立谱流方程（§8.7#5 核心）、独立能量锚选 $c$ 截线（§8.7#5）与带辨认对应（§8.7#8）。**【起点-规范/表示层：已闭合部分经 Lemma 不需 Δ；残余 EM 谱流/能量锚/带辨认属输入侧】**
4. G3：陈数模块（Berry 曲率 → 第一陈数 → TKNN 谱公式）。**【起点-规范/表示层】**
5. G4：GP-谱流等同的形式化条件 + 涡旋荷守恒。**【起点-规范/表示层：代数核心已在 2026-09-19 闭合】**——涡旋＝谱规范分支 + 拓扑荷守恒（`GPVortex.lean`，零 sorry：谱流幺正规范协变 `spectralFlow_unitary_conj` + 规范分支保迹幂 `vortex_trace_gaugeInvariant` + 涡旋荷守恒 `vortex_charge_conservation`，命题 4.2/推论 4.2 的谱代数根源，paper14 v1.8）；真实 winding 荷 $n\in\mathbb{Z}$ 的严格定义与 GP-谱流等同的 PDE 层面需连续场论，登记开放

**远期（真内生链，按 §4 起点分层改判）**：
6. G1：Paper XX 链泛化到凝聚态谱生成元，与 G2 会师，形成 对易子→…→Δ_BCS→ρ₀→T_c 标度的全内生链。**【起点-规范/表示层（主链）】**；"从范畴 Δ 出发"的表述收回——Δ 支保留为远期 𝒯 统一目标（§8.7#5 核心：范畴→表示运输函子），仅在 𝒯 落地后才可作为内源起点，数值内源不押于此（§8.19 判定 `16=dim_ℝℍ²` 为维数恒等/模分解巧合、非代数内源即一实例）。见 §4"起点分层"。

---

## 6. Paper XIV 自身待修问题（重建时一并处理）

1. 版本不一致：文首 v1.5（2026-08-16），文尾版本块 v1.4（2026-07-25），变更记录缺 v1.5 条目。
2. 工作区存在未提交的并行改动（超流刚度工作线所致），重建前需先合并定版。
3. §3.4/§3.3 的"第一性"措辞按 §4 标注体系重定级。

---

## 7. 引用文件

- `paper/paper14_spectral_condensed_matter.md`（重建对象，v1.5）
- `paper/paper54_emergence_map.md`（内生范式模板：Δ → Einstein 全链 Lean 证）
- `formal_proof/MUFPFormalization/src/MUFPFormalization/WeaveBCS.lean`（G2 载体，r 开放项在 §3 注释）
- `formal_proof/MUFPFormalization/src/MUFPFormalization/NoiseCategory.lean`（G5，占位定理清单）
- `formal_proof/MUFPFormalization/src/MUFPFormalization/SuperfluidStiffness.lean`（Phase 70，零 sorry，未提交）
- `roadmap/phase70_superfluid_stiffness.md`（Phase 70 规划）
- `notes/02_superconductivity/spectral_superfluid_stiffness.md`（MUFPF-RN-RHO0-001，谱公理层推导的范本）


---

## 8. 执行进度

### 2026-09-12：G5 闭合（NoiseCategory 占位定理真证）

**结果**：6 个 `: True := trivial` 占位定理全部处置完毕，全库 `lake build MUFPFormalization`
3688 jobs 通过，零 sorry。

**真证闭合（6 项）**：
- Thm 16.1 `sigmaRec_decomposition_unique`（新增 `IsComponentReorder`，恒等重排唯一）
- Thm 16.2 `spectral_sequence_convergence`（新增 `truncateComponents`，有限支撑 ⟹ 有限步精确稳定）
- Thm 16.3 `sigmaD_preserves_inductive_limit`（逐分量最终相等）
- Thm 17.2 `ext_degenerates_to_sel`（见下"意外收获"）
- Thm 17.7 `noise_spectral_flow_eq`（迹导数版：d Tr(A+η·D)/dη = Tr(D)）
- `dissSilent_component_size`

**意外收获（对 paper14 重建有直接影响）**：原 `extFunctor` 以 `Finset.range 10`
截断扫描——第 10 个分量以后的非空分量被忽略、且 `min'` 与 `Nat.find` 选择规则不同，
存在 ext ≠ sel 反例。即 **Thm 17.2 原陈述不可证明是定义性 bug 而非定理为假**。
已改为全 ℕ `Nat.find`，此后定理 trivially 成立。若带入重建，以"修正后实现"为准。

**删除并登记开放（4 项，不 axiomatize）**：
- Thm 17.3 Ext 收敛率 O(1/√N)（需概率论语义，有限原型不可陈述）
- Thm 17.8 逆谱流噪声过滤（需局域化算子 F + 谱测度）
- Thm 17.7 本征值投影版（需谱投影 P_λ，迹版已真证）
- Thm 16.2 完整 TV 距离界（需截断谱测度基础设施）

**登记为 `def ...Open : Prop`（1 项）**：`SelDissAdjunctionOpen`（Prop 17.1，Hom 集同构，
关闭需 list-编码 Hom 显式逆构造）。

**G5 遗留 → 已闭合（2026-09-19）**：ε_eff 闭式的 Lean 化（§3.4 纸面解析推导）——
新建 `NoiseEffectiveEpsilon.lean`（零 sorry）封闭退化值/远程主导分解/θ 因子/连续性退化
极限/ε_c^eff 单调递减等判别性命题，无穷远精确渐近 ε_eff~n_imp·ξ² 登记开放；
paper14 升 v1.7、roadmap §七记档。详见下方 2026-09-19 进度条目。

全链闭合与证伪处置记录见 `formal_proof/MUFPFormalization/sorry_closure_roadmap.md` §6（NoiseCategory）与 §7（NoiseEffectiveEpsilon）。

### 2026-09-12：G6 闭合（IQHE RG 常数地位裁定，走路线 b）

**裁定**：定理 3.2 的 α≈1.16、ε₀≈2.58 与定理 3.3 的 ζ₀≈10⁻⁶、γ₂≈0.06、ε_c（及 §3.4 的
ε_c⁽⁰⁾≈10.0）确认为对开放渠道 16 组实验数据的**现象学拟合常数**，非第一性推导产物。
路线 (a)（从谱投影尺子响应推导）短期不可行，按 §3 缺口清单走路线 (b)。

**已改 paper14 措辞（工作区，未提交）**：
- §3.3 引言："推导出连续插值公式"→"以谱投影尺子 P_ξ 的面密度响应为物理动机，提出…"；
  新增一句总声明"函数形式与端点是谱公理层模型假设，α、ε₀ 是现象学拟合，本节不含从
  范畴 Δ 或谱流方程到这些常数的第一性推导"。
- 定理 3.2 后新增"**常数地位【输入-现象学】**"段：α、ε₀ 为最小二乘拟合参数；端点
  ν=1、ν≈2.35 是物理输入（Pruisken 标度）非拟合自由度；明确"不得称 α、ε₀ 为推导结果"。
- 定理 3.3 组分表后新增"**常数地位【输入-现象学】**"段：ζ₀、γ₂、ε_c、ε_c⁽⁰⁾ 同为拟合
  参数；ν_std=2.35 是输入端点；β 函数形式与三不动点结构是谱公理层假设。

**端点的层级归属（裁定细节）**：ν=1（清洁极限）保留为谱公理层的框架预言（谱框架独有），
ν≈2.35 是输入的标准标度物理端点——两者均非拟合自由度，与 α、ε₀、γ₂、ζ₀ 区分标注。

**未提交原因**：paper14 工作区同时含超流刚度工作线的并行改动（§2 BCS 段、§3.2，8 个
hunk），git 无法按行拆分提交；按 §6 第 2 条"重建前需先合并定版"，paper14 的 G6 修订
随重建阶段与并行改动统一提交。修订已固化在工作区文件 + 本笔记双备份。

**下一步**：G2——WeaveBCS r 参数弱耦合极限定理化（§5 中期路线第 3 项，G2 有 WeaveBCS
方程与数值锚点 r≈0.874 可直接承接）。

### 2026-09-12：G2 部分闭合（谱流自洽方程正实根存在唯一性）

**新增**（`WeaveBCS.lean` Section 3，`selfConsFunc` 定义 + 6 引理/定理，全零 sorry）：
`selfConsFunc r := (1 + √3·√r)·r` 及其连续性、正性、严格单调性（Ici 0）、下界 f(x)≥x，
与主定理 **`selfConsFunc_existsUnique`**：对任意 c > 0，方程 f(r) = c 在 [0,∞) 存在**唯一**
正实根 r*（IVT + StrictMonoOn.injOn 证明，无 sorry）。

**定理化的地位（诚实边界）**：这把 r 从"硬编码数值 r_self_consistent := 8740/10000"
提升为"由普适输入 c = a_BCS³·4π（BCS 弱耦合普适比值，物理输入）经显式方程**唯一确定**
的普适比值"——确立了 r 的方程确定性与普适性，是 G2「哪怕只在普适比值层面」目标的
最低诚实达成。

**未闭合（如实登记）**：
1. 精确数值等式 r* = 0.8740 在 Lean 实数层仍不可证（√3、√r* 的无理性，数值逼近），
   保留 2026-08-04 开放项登记，数值由 Python 层（spectral_BCS_v2_comprehensive.py Q1）给出；
2. **dl_min ≡ Δ_BCS 的完整桥未触及**——本定理确立的是"r 由方程唯一确定"，没有证明
   范畴谱间隙 dl_min 数值上等于 BCS 配对隙。后者需更多物理输入，归 G1/远期范畴。

**对重建的意义**：paper14 §2 的"r 为基本自由参数"措辞在重建时应改为"r 为由普适
自洽方程唯一确定的普适比值（定理：WeaveBCS.selfConsFunc_existsUnique），其数值由
Python 层解出 ≈0.874"。

全库 `lake build MUFPFormalization` 3688 jobs 通过，零 sorry。

### 2026-09-12：G3 部分闭合（Berry 曲率代数核心，新建 BerryChern.lean）

**背景**：paper14 定理 3.1（TKNN）与命题 3.1（陈数绝热不变性）此前零 Lean 载体
（库内 grep Chern/陈数零命中），是 §3 缺口里工作量最大的一项。

**已建**（`BerryChern.lean`，零 sorry，全库 3689 jobs 通过）：
- `berryCurvature P A B := -i · Tr(P [A, B])`——Berry 曲率投影公式（P 孤立能带
  谱投影，A=∂ₓP、B=∂ᵧP 厄米切向量），第一陈数密度的被积函数；
- `trace_proj_commutator_skewAdjoint`：对厄米 P、A、B，`Tr(P[A,B])` 斜伴随
  （star T = −T，纯虚）。证明只用迹循环性 + 厄米性 + 共轭转置反自同构，
  **不依赖幂等性**；
- **主定理 `berryCurvature_im_eq_zero`**：Berry 曲率实值（im = 0）——陈数良定义
  （被积函数实值、积分为实数量子数）与 Hall 电导可观测的代数根源。

**技术说明**：厄米性取显式等式假设 `hP : P = Pᴴ`（等价 Matrix.IsHermitian，但避其
结构包装使 rw 直接可用）；mathlib 无现成 Chern/Berry 基础设施，模块自包含
（Mathlib.Data.Complex + LinearAlgebra.Matrix.Trace）。

**未闭合（§3 开放登记，不占用 sorry）**：第一陈数积分定义 C=(1/2π)∫_{T²}F、
整性 C∈ℤ、TKNN 公式 σ_xy=(e²/h)C、陈数绝热不变性——需环面积分、
拓扑度/同伦、Kubo 线性响应等基础设施，属积分/场论形式化（远期）。
规范不变性：**代数核心（酉稳定化不变）已于 2026-09-19 闭合**（BerryChern §2.6，
`berryCurvature_unitary_conj`，见 §8 尾部进度条目），联络层面（$u\mapsto e^{i\theta}u$、
$F=dA$）仍开放。

**根文件接线**：`import MUFPFormalization.BerryChern` 已加入根文件并完成全库验证；
因根文件同时含未提交的超流刚度 import（SuperfluidStiffness），提交时**只提交
BerryChern.lean**，根文件随重建阶段与该线统一提交。

### 2026-09-12：G4 部分闭合（谱流守恒律代数核心，新建 GPFlow.lean）

**背景**：定理 4.1（GP-谱流等同）证明是启发式 sketch，命题 4.2（涡旋=谱规范分支）、
推论 4.2（涡旋荷 dn/dt=0）无载体。GP 方程是连续 PDE，完整形式化需场论/同伦。

**已建**（`GPFlow.lean`，零 sorry，全库 3690 jobs 通过）：
- `trace_commutator_eq_zero`：迹消去交换子 tr [G, A] = 0；
- **谱流守恒核心 `trace_pow_mul_commutator_eq_zero`**：tr(A^k·[G, A]) = 0——迹幂
  函数在李括号方向 [G,A] 上消失，即 tr(A^k) 沿谱流方程 dA/dt=[G,A] 不变（谱
  不变性）。纯代数证明（迹循环性），不依赖幂等/厄米，对任意复方阵成立。
  **这是推论 4.2「涡旋拓扑荷守恒」的谱代数根源**（拓扑荷由谱决定，谱不变⟹荷不变）。

**未闭合（§3 开放登记）**：时间依赖守恒律（需矩阵幂导数规则，mathlib HasDerivAt.mul
可归纳构造）、谱不变性经 Newton 恒等式、涡旋 winding 拓扑荷（需同伦提升）、
GP-谱流等同（定理 4.1，需 PDE）、规范协变性——属微积分/场论/同伦基础设施。

**根文件接线**：`import MUFPFormalization.GPFlow` 已加入并完成全库验证；同 G3，
提交时只提交 GPFlow.lean，根文件随重建统一提交。

**下一步**：G1——Paper XX 链泛化到凝聚态谱生成元（远期核心，与 G2 会师形成
Δ→…→Δ_BCS→ρ₀→T_c 全内生链）。

### 2026-09-12：G1 部分闭合（谱不变量相似不变性，新建 SpectralInvariant.lean）

**背景**：G1 是远期核心——把 Paper XX 链（Δ→SU(2) Casimir→Cl(1,7)→谱间隙）
泛化到凝聚态。其数学前提是：若两个谱生成元由保持谱的映射（Sp 同构=可逆交织）
联系，则共享全部谱不变量（含谱间隙）。

**已建**（`SpectralInvariant.lean`，零 sorry，全库 3691 jobs 通过）：
- `conj_pow_eq`：相似幂公式 (Q·A·P)^k = Q·A^k·P（Q·P=1 且 P·Q=1）；
- **G1 核心 `trace_pow_similar`**：相似（Sp 同构的矩阵内容）保持全部迹幂
  tr((QAP)^k) = tr(A^k)。迹幂经 Newton 恒等式完全决定谱（计重数），故相似保持
  谱进而保持谱间隙。纯代数证明（conj_pow_eq + 迹循环性），不依赖厄米/幂等。

**未闭合（§3 开放登记）**：Newton 恒等式到谱间隙的翻译、酉共轭特例（谱定理）、
**凝聚态桥的具体构造**（A_SC=ξσ_z+Δσ_x 与 Paper XX SU(2)/Cl(1,7) 生成元的显式
Sp 同构——G1 完整目标，框架级研究）、范畴 Δ 泛性质（SU(2) Casimir 谱与 Cl(1,7)
谱间隙是 Δ 的泛性质结果，与引力/凝聚态无关）。

**G1-G6 小结**：六个缺口全部建立有限维可证核心并登记开放项——G5（NoiseCategory
6 真证 + 4 开放登记）、G6（RG 常数现象学降级，paper14 措辞已改）、G2（自洽方程
根存在唯一性）、G3（Berry 曲率实值性）、G4（谱流守恒 tr(A^k[G,A])=0）、G1（谱
不变量相似不变性）。形式化侧的内生推导第一性证据链已就位。

**下一步**：重建 paper14（内生标注体系）——按 §4 三级标注【内生-范畴】/【谱公理】/
【输入-现象学】重排全文，正文只留成果、轨迹归笔记、不引用笔记。

### 2026-09-12：paper14 v1.6 内生标注体系重建（第一轮，完成）

paper14 从 v1.5 重建为 **v1.6（2026-09-12，内生推导标注体系重建版）**，落实以下动作：

1. **文首插入内生标注体系图例**（术语说明后、§1 前）：定义三级标注【内生-范畴】/
   【谱公理】/【输入-现象学】+ 诚实边界声明（范畴 Δ 只产普适量、材料参数永为输入）
   + v1.6 形式化支撑清单（四个新模块 + NoiseCategory，全库零 sorry）。
2. **"第一性原理推导"重定级**（G5/G6 遗留）：摘要第 (4) 条、§3.4 引言、结论清单
   三处"第一性原理推导"改为"谱公理层推导"并显式标注名实差距；§3.3/3.5 的 RG
   常数标注已在 G6 完成。
3. **§2 补 r 参数谱公理层标注**：δ_SC=Δ_BCS 是翻译非推导；r 由普适自洽方程唯一
   确定（引 `selfConsFunc_existsUnique`），非范畴 Δ 内生（范畴桥为已登记开放）。
4. **§4 补层级标注**：定理 4.1 是 GP-谱流翻译【谱公理】；推论 4.2 涡旋荷守恒的
   谱代数根源已闭合（引 `GPFlow.trace_pow_mul_commutator_eq_zero`），winding 严格
   定义为已登记开放。
5. **版本块统一**：文首版本号 v1.5→v1.6；变更记录补 v1.6 重建条目 + v1.5 补全
   §5.8 内容（原漏记）+ 勘正 v1.5 日期不一致（文首 08-16 vs 文尾 08-24）；重排为
   倒序（v1.6→v1.0），删除重复悬挂的 v1.5 行。

**重建完成度（诚实）**：标注体系建立 + 关键措辞重定级 + 版本一致 + 形式化接入已完成；
**逐节全面标注**（§3.6-3.8、§5.1-5.8 各预言/结论 C1-C6 的起点标注）为持续工作，
可后续按同一句式模板批量补齐。**根文件与并行改动**：根文件 MUFPFFormalization.lean
的 BerryChern/GPFlow/SpectralInvariant import 与 SuperfluidStiffness import 同属未
提交状态，随该线统一提交；paper14 工作区含超流刚度线的并行文本改动（§2/§3.2，
8 hunk），本次随重建一并定版提交。

**研究目标达成度**：「内生推导第一性」证据链——G1-G6 全部建立有限维可证核心，
paper14 按三级标注诚实分层，名实差距显式标注。残余开放（完整陈数场论、GP-PDE、
Δ→凝聚态具体桥、数值常数精确等式）均已登记为开放问题，非未识别的隐藏缺口。

### 2026-09-12：paper14 v1.6 重建第二轮（批量标注补齐，完成）

在第一轮（图例+重定级+§2/§4 标注+版本统一，已提交 `4e82fbf`）基础上，对第一轮未覆盖的
条目按同一句式模板（`**层级标注【X】**。一句理由`）批量补齐起点标注：

| 条目 | 判定 |
|------|------|
| 命题 3.1（陈数绝热不变性） | 【谱公理】；代数核心 Berry 曲率实值性已形式化（`BerryChern.berryCurvature_im_eq_zero`），完整陈数场论开放 |
| 定理 3.4（谱化闭式解） | 【谱公理】（不动点方程闭式代数推演，非 Δ 内生）；数值验证属独立数值验证层 |
| §3.7（16 组实验对比） | 【输入-现象学】（数据映射验证） |
| §3.8（倾斜磁场） | 【谱公理】框架 +【输入-现象学】具体角度数值（θ_c≈75.6° 等） |
| 谱诠释 5.1–5.4 | 均【谱公理】（谱流方程+物理输入的诠释） |
| 谱预言 6.2（CdGM Casimir 修正） | 【谱公理】 |
| 谱预言 6.3（QH 纠缠熵振荡） | 【谱公理】 |
| 谱预言 6.4（TI 边界态 k_max=8） | 【内生-范畴】序列 +【谱公理】映射（同 6.1 句式：Cl(1,7) Bott 已内生，谱-物映射是谱公理假设） |
| 谱预言 6.5（IQHE ν→1） | 【谱公理】+【输入-现象学】；**实质措辞修改**：原"(2) Sigmoid 过渡陡度由谱投影尺子唯一决定，非拟合参数"与 G6 裁定（α 为拟合常数）矛盾，软化为"陡度关联谱投影结构，但数值参数目前按现象学拟合处理，第一性推导为开放问题（见 §12 问题 G6 的裁定）" |
| 命题 5.7（记忆函数-谱丛等同） | 【谱公理】（极点=分支点为谱丛定义直接推论） |
| §5.8（稳定岛） | 【独立数值验证】（§5.8.5 已有诚实边界，仅加一句层级标注） |
| 结论 C1–C6 | 层级总注（插在结论表后）：C1-C5【谱公理】（C2 的 RG 常数部分【输入-现象学】）、C6【独立数值验证】；明确"本文无一结论属【内生-范畴】"及原因（G1 范畴桥开放） |

**本轮发现的实质张力点**：仅谱预言 6.5 一处措辞与已闭合问题（G6）矛盾，已修正；其余均为
纯标注增补，无内容改动。版本块 v1.6 条目追加"重建第二轮"摘要。

**完成度**：paper14 全部定理/命题/预言/诠释/实验节/结论均带起点标注，三级体系全文无盲区。

### 2026-09-12：G1 切入点闭合（GP 生成元涌现，新建 GPEmergence.lean，零 sorry）

**任务转向**：用户指出 v1.6 重建"在原版上做妥协"（只标注未推导）。要求不做妥协、
直接攻 G1 本体。本条目记录 GP 切入点的真证闭合。

**新建模块 `GPEmergence.lean`**（根文件已 import，全库 3698 jobs 构建通过）：

| 内容 | 定理 | 数学内容 |
|------|------|----------|
| §1 | `PosSpectrum` | 正谱锥约束（Rec_D 的 Sp 侧对应，凝聚态密度算子 ρ 的谱全正） |
| §2 | `specGenerator` | A_GP := cfc(−log)——谱生成元的连续函数演算构造 |
| §3 | `specGenerator_exp` | **谱对应求逆**：exp(−A_GP) = ρ（Paper I λ=e^{−μ} 精确求逆） |
| §4 | `specGenerator_charpoly` | **谱映射**：σ(A_GP) = −log σ(ρ)（无质量生成元，谱为实） |
| §5 | `specGenerator_flow` | **谱流闭合**：ρ(t)=e^{−A_GP(t)} 与 dA/dt=[G,A] 精确相容 |
| §6 | `specGenerator_trace_pow_commutator_eq_zero` | 守恒律实例化（GPFlow 核心直接适用） |

**技术要点**（备查）：
- 用 `Matrix.IsHermitian.cfc`（mathlib Analysis/Matrix/HermitianFunctionalCalculus），
  谱有限故任意函数（含 log）无需连续性条件；谱映射用同文件 `charpoly_cfc_eq`。
- 酉对角化三件套：`Matrix.mem_unitaryGroup_iff/iff'` + `Matrix.inv_eq_left_inv`
  （star U = U⁻¹）+ `Units.mk ... .isUnit`；共轭指数化用 `Matrix.exp_conj/exp_neg`。
- 坑：项目 mathlib 处于 module 过渡期，`open Matrix/...` 批量 open 失效（裸名
  变 autoImplicit），一律用全限定名；`NormedSpace.exp` 在 Pi 上逐点用 `Pi.coe_exp`；
  `Complex.exp_eq_exp_ℂ` 需显式 import `Mathlib.Analysis.SpecialFunctions.Exponential`。
- `noncomm_ring` 处理 −(U·D·U⁻¹) = U·(−D)·U⁻¹ 的符号搬移。

**paper14 同步升级（v1.6 第三轮）**：§4 标注 →【内生-范畴】+【谱公理】混合
（生成元构造链内生；GP-PDE 翻译仍谱公理层）；结论 C3 同步升级；总注从
"本文无一结论属【内生-范畴】"改为"首次出现内生-范畴成分（C3 生成元构造链）"；
图例形式化支撑清单补 GPEmergence 四定理；版本记录 v1.6 追加第三轮摘要。

**G1 残余开放**（已登记于模块 §7 注释）：ρ 的 PF 不动点存在性（ErgodicTheory 已登记）、
正谱锥边界破缺生成元（类比 paper5 定理 5.1，待微分基础设施）、A_SC/A_Hall 同类
涌现构造、specGenerator 的 Hermitian 性包装。BCS 侧下一切入点：WeaveBCS 的
r ≈ 0.874 锚点 + 谱对数构造模板推广。

### 2026-09-12：G1 第二切入点闭合（BCS 生成元涌现，新建 BCSFermiEmergence.lean，零 sorry）

承接 GP 切入点（见上条），按同一 paper5 §5 模板"子范畴约束 → 生成元涌现"的 BCS 实例
完成 G1 的第二个切入点。GP 链从**密度算子 ρ** 出发（需正谱锥约束）；BCS 链从
**Hamiltonian H** 出发——exp(−log(1+e^{βx})) = (1+e^{βx})⁻¹ 处处成立（1+e^{βx} > 0），
故**对 H 的谱无任何限制**，且 T=0 奇异极限（γ 成为投影、谱触 0）由 β 有限性自动规避。

**新建模块 `BCSFermiEmergence.lean`**（namespace MUFPF，根文件已 import，
全库 3699 jobs 构建通过，零 sorry）：

| 内容 | 定理/定义 | 数学内容 |
|------|-----------|----------|
| — | `fermi β x := (1+e^{βx})⁻¹`、`fermiDensity` | γ_F = hH.cfc(Fermi)——Fermi 密度算子 |
| — | `bcsGenerator` | A_BCS = hH.cfc(log(1+e^{β·}))——BCS 谱生成元 |
| §1 | `fermiDensity_isHermitian` | γ_F Hermitian（cfc 保自伴） |
| §2 | `bcsGenerator_fermi_inverse` | **Fermi 求逆**：exp(−A_BCS) = γ_F（核心，对 σ(H) 无正性条件） |
| §3 | `bcsGenerator_charpoly` | 谱映射：σ(A_BCS) = log(1+e^{β·})(σ(H)) |
| §4 | `bcsGenerator_flow` | 谱流闭合：exp(−spectralFlow A_BCS G t) = spectralFlow γ_F G t |
| §5 | `specGenerator_fermiDensity` | **G1 会师**：specGenerator γ_F = A_BCS——GP 模板（ρ→−logρ）与 Fermi 构造（H→γ_F→−logγ_F）在 γ_F 上统一 |

**关键技术要点**（在 GP 条坑清单之上新增）：
- `GPEmergence.diagonal_neg'` 原声明为 `private`，跨模块不可见——已去 private
  供两模块共享（负对角阵 = 对角的负，负指数化收束用）。
- 符号结构（重要）：A_BCS 本征值为 **+**log(1+e^{βλᵢ})，exp(−A_BCS) 的对角化
  对角元必须取 **−**log（e^{−log y} = y⁻¹ = Fermi 权重）。写成 +log 则 e1 步
  证出的是 1+e^{βH} ≠ γ_F——编译器残差目标 `↑y = ↑(fermi β λ)`（y ≠ y⁻¹）暴露。
  GP 侧无此问题因为 specGenerator = cfc(−log ρ) 本征值本就是 −log λ。
- 复数化链处理参数内负号：`NormedSpace.exp (−↑(log y))` → `← Complex.exp_eq_exp_ℂ`
  → `← Complex.ofReal_neg`（−↑x → ↑(−x)）→ `← Complex.ofReal_exp` → `Real.exp_neg`
  → `Real.exp_log` → 得 `↑(y⁻¹)`，与 `(↑y)⁻¹` 差一个 `Complex.ofReal_inv`。
- `Real.log_inv` **无 ≠0 侧条件**（mathlib 约定 log 0 = 0），单参数 `(x : ℝ)`；
  误传假设会报 "expected ℝ"。rw 的显式参数需与目标语法匹配（`fermi β x ≠ 0` 与
  `(1+e^{βx})⁻¹ ≠ 0` 仅 defeq 不相通）。
- `cfc_comp`（generic cfc 复合）需 `IsSelfAdjoint` + 两侧 `ContinuousOn`；
  Fermi 函数的连续性用手工 `h1.inv₀` 组装（continuity tactic 对 def 的 ≠0 侧
  条件搞不定）；矩阵 cfc 与 generic cfc 互换：`Matrix.IsHermitian.cfc_eq` 方向
  注意（forward : cfc f A = hA.cfc f）。
- 矩阵 cfc 展开的 simp 归一形：`simp only [def名, Matrix.IsHermitian.cfc,
  Unitary.conjStarAlgAut_apply]` 后目标两侧通常已 defeq，单个 `congr 1` 即全闭
  （comp/beta 叶子由 congr 的 rfl 自动关闭）——多写的第二个 `congr 1` 报
  "No goals to be solved"，Matrix.ext 下探是过度结构。

**paper14 同步升级（v1.6 第四轮）**：§2 层级标注 →【谱公理】+【内生-范畴】混合
（A_SC 翻译仍谱公理层；"状态密度 → 谱生成元"构造 H→γ_F→A_BCS 已机器证明，
属内生-范畴层，H 本身及 ξ/Δ 仍是物理输入——结构性边界）；结论 C1 同步升级；
总注更新（C1/C3 内生-范畴成分，G1 状态：GP、BCS 两切入点闭合且经会师定理统一，
Hall 侧开放）；文首形式化支撑清单补 BCSFermiEmergence 四定理；版本记录 v1.6
追加第四轮摘要。

**G1 残余开放**：Hall 侧 A_Hall 磁平移投影有限维模型（第三切入点，未动工）；
PosSpectrum γ_F 与 cfc 特征多项式的 eigenvalues 索引对齐（谱重排包装工作，
当前由无正性条件的 inverse/flow 覆盖同一数学内容）；specGenerator 的
Hermitian 性包装（GP 侧已登记）；ρ 的 PF 不动点存在性；T→0 奇异极限的
算子收敛（泛函分析，远期）。

### 2026-09-12：G1 第三切入点闭合（Hall 生成元涌现，新建 HallEmergence.lean，零 sorry）——G1 三切入点全闭合

承接 GP、BCS 切入点（见上两条），按同一 paper5 §5 模板完成 G1 的最后一个
切入点。Hall 侧从**磁平移代数**出发——Landau 规范磁通量子 ωₙ = e^{2πi/n} 上的
Weyl 对（clock 对角磁平移 / shift 循环移位），与 GP 侧（需正谱锥约束）、BCS 侧
（无谱条件）三足并立：磁平移代数的 Weyl 关系 + 幺正性即 Hall 侧"子范畴约束"
的代数核心。

**新建模块 `HallEmergence.lean`**（namespace MUFPF，根文件已 import，
全库 3700 jobs 构建通过，零 sorry）：

| 内容 | 定理/定义 | 数学内容 |
|------|-----------|----------|
| — | `omegaArg`/`omega`、`omega_pow`/`omega_pow_mod` | 磁通量子 ωₙ = e^{2πi/n}，ωₙ^n = 1 与降幂 ω^a = ω^(a % n) |
| — | `clock`/`shift` | Weyl 对：U = diag(ω^i)，V = 循环移位（Fin n 模加法） |
| §1 | `clock_shift_weyl` | **Weyl 关系**：UV = ωₙ·VU（n ≥ 2）——磁平移代数对合关系 |
| §2 | `clock_star_mul_self`/`shift_star_mul_self`/`shift_mul_star_self` | clock/shift 幺正性 U†U = V†V = VV† = 1 |
| §3 | `harper`/`harper_isHermitian` | Harper Hamiltonian H = U+U†+V+V† 的 Hermitian 性 |
| §4 | `hallGenerator_fermi_inverse` | Hall 链 Fermi 求逆：exp(−A_Hall) = γ_F(H_Harper)（BCS 模板实例） |
| §5 | `hallGenerator_spec_meeting` | **GP-BCS-Hall 三链会师**：specGenerator γ_F(H_Harper) = A_Hall |
| §6 | `occFn`/`occupiedProjection` + `_isHermitian`/`_idempotent` | T=0 占据带谱投影：Hermitian + 幂等 |
| §7 | `occupied_berry_im_eq_zero` | **Hall-Berry 接入**：占据带 Berry 曲率实值（σ_xy ∈ ℝ 的代数根源） |

另补 `GPEmergence.specGenerator_isHermitian`（specGenerator 的 Hermitian 性包装，
GP 侧登记项闭合）。

**关键技术要点**（在 GP/BCS 条坑清单之上新增）：
- `Fin n` 的 `+` 需要 `NeZero n` 实例：`haveI : NeZero n := ⟨Nat.ne_of_gt (by omega)⟩`
  从 `hn : 1 ≤ n` 现场构造；`Fin.val_one' (n) [NeZero n] : ((1:Fin n):ℕ) = 1 % n`
  （无 val_one，1 < n 时自己接 `Nat.mod_eq_of_lt`）。
- `Finset.sum_eq_single (s/f/a := ...)` 的三个隐参必须显式给 `f`——否则 h₀ 里
  的目标退化为 `?m.137 k = 0`（f 为 metaviable），tactic 块无法 rw；给了 `f :=` 后
  `a` 仍需 `(a := j)`，否则结论 `∑ = f ?a` 与 ascribed 类型合一失败。
- 求和核用 `Finset.sum_eq_single` 取唯一非零点（而非 `Finset.sum_ite_eq'`——
  该引理在本版 mathlib 化出 `if a ∈ univ` 形态，且 univ 版行为不稳定）；
  两种条件方向（`a = k+1` 与 `k = a+1`，后者为 star 在左的形态）各证一版
  （`shift_sum_ite`/`shift_sum_ite'`）。
- 唯一性论证走 `fin_add_one_injective`（+1 在 Fin n 单射；n = 1 用
  `Subsingleton.elim`）+ 原像引理 `fin_add_pred_add_one`（(a+(n−1))+1 = a，
  模数 % 先用手工 `Nat.mod_*` 消掉再 omega——**omega 不处理变量模数**）。
- `Complex.conj` 在本版 mathlib **不存在**：`conj` 是 `ComplexConjugate` scope 内
  记号（`starRingEnd ℂ`）。绕法：全程用 `star` 表述
  （`rw [Complex.star_def, ← Complex.exp_conj, ← Complex.exp_neg]`），
  re/im 分量用 `Complex.ext_iff` + `simp [omegaArg, div_neg, neg_div]` 关闭。
- `Matrix.IsHermitian A` 定义为 `Aᴴ = A`（`LinearAlgebra/Matrix/Hermitian.lean:44`），
  但 `ᴴ` 记号在本文件 `open Matrix` 下仍不解析（原因未查明，BerryChern 同 setup
  可用）——稳妥写法：一律用 `Matrix.conjTranspose` 全称。
- `rw` 语法匹配不透 def（`omega`/`shift`/`occFn`），需 `simp only [omega]` 或
  have+默认透明度；`congr 1` 常把 defeq 叶子 rfl 全闭，多写报 "No goals"。
- 幂等定理的矩阵结合：中间步骤显式写成 `U * (D * D) * star U`（noncomm_ring
  可证任意真实结合等式），给 `Matrix.diagonal_mul_diagonal` 留出
  `diagonal ?d₁ * diagonal ?d₂` 的语法子项——左结合形 `(U*D)*D` 中 D、D 不构成
  乘积子项，rw 匹配失败。

**paper14 同步升级（v1.6 第五轮）**：§3 新增层级标注段 →【内生-范畴】+
【谱公理】混合（磁平移代数 Weyl 关系/幺正性、Harper 生成元链、占据投影、
Berry 曲率实值已机器证明属内生-范畴层；陈数积分定义/整性/TKNN 场论仍谱公理层）；
结论 C2 同步升级；总注更新（C1/C2/C3 内生-范畴成分，**G1 状态：GP、BCS、Hall
三切入点全部闭合，经 GP-BCS 会师与 GP-BCS-Hall 三链会师统一，G1 本体完成**）；
文首形式化支撑清单补 HallEmergence 七定理；§2 末"Hall 侧开放"改为已闭合；
版本记录 v1.6 追加第五轮摘要。

**G1 至此三切入点全闭合（GP/BCS/Hall）**。残余开放（均已登记）：
Weyl 迹正交性 Tr(U^a V^b) = n·δ_{a≡0}δ_{b≡0}（磁平移代数 ≅ Mₙ(ℂ) 结构定理，
需复单位根几何和包装）；陈数整性 C = (1/2π)∫F ∈ ℤ 与 TKNN 场论形式（需环面
积分/拓扑度/Kubo 基础设施）；谱投影参数导数（Berry 切向量构造层，当前以任意
厄米切向量为假设接入）；Harper 谱隙/Hofstadter Butterfly（需具体谱计算，数值层
有载体）；ρ 的 PF 不动点存在性；T→0 算子收敛（泛函分析，远期）。

### 2026-09-13：Weyl 迹正交性闭合（HallEmergence §8，零 sorry）

**交付定理**（`HallEmergence.lean` 新增，全库 3700 jobs 编译通过）：

| 名称 | 可见性 | 内容 |
|------|--------|------|
| `weyl_trace_orth` | public | Tr(U^a V^b) = if a%n=0 ∧ b%n=0 then n else 0——Weyl 基 {U^a V^b} Hilbert-Schmidt 正交（范数平方 = n），磁平移代数 ≅ Mₙ(ℂ) 结构定理的迹形式 |
| `clock_pow` | private | clock n ^ a = Matrix.diagonal (fun i => ω^(a·i))——clock 幂的对角化显式形 |
| `shift_pow` | private | (shift n ^ b) i j = if i = j + Fin.ofNat n b then 1 else 0——shift 幂的置换形 |
| `fin_add_nat_succ` | private | j + 1 + Fin.ofNat n b = j + Fin.ofNat n (b+1)（Fin 加法 + 模数吸收） |
| `omega_primitive` | private | IsPrimitiveRoot (ω n) n（本原性，经 Complex.isPrimitiveRoot_exp_of_coprime） |
| `omega_geom_sum` | private | ∑_{i< n} (ω^a)^i = if a%n=0 then n else 0（几何和判别，分母零情形的根级处理） |

证明主线：trace = ∑ᵢ (clock^a)ᵢᵢ · (shift^b)ᵢᵢ（sum_eq_single 逐行对角化）→ 对角元
对 b%n=0 分支判别（b%n≠0 时 Fin.ext 导出矛盾，q=0 用 div_add_mod + nlinarith）→
幂化 (ω^a)^i 的几何和 → ω 本原性判 (a, n) 关系。Weyl 迹正交性从"开放登记第 1 条"
移出；§末开放登记同步增补第 4 条"唯一不可约表示"（表示论结构定理，迹层面已闭合）。

**技术要点（本版 mathlib 新踩实）**：

- **`NatCast (Fin n)` 实例已移除**（新版 mathlib/Lean core）：`(b : Fin n)`、
  `Nat.cast b`、`Fin.ofNat'` 全部不可用；替代 `Fin.ofNat n a`（core，val = a%n 是 rfl）。
- **omega 对含变量除法原子的目标不可靠**（把 n·q 当独立原子）：b%n = n·q 推出
  q=0 须 `Nat.div_add_mod` + `rw [← hval] at h1`（方向！）+ `nlinarith`，不要用 omega。
- **`rw [if_pos ⟨ha, hb⟩]` 匿名构造器对 metaviable 条件会 elaboration 失败**：
  必须 `rw [if_pos (show a%n=0 ∧ b%n=0 from ⟨ha, hb⟩)]` 显式标注。
- `Finset.sum_eq_single` 隐参 s/f/a 必须显式，否则 f 退化为 metaviable 导致 h₀ 内无法 rw；
  `rw [Finset.sum_congr rfl fun i _ => by rw […]]` 可用（f 从目标合一确定）。
- `geom_sum_eq`（root 级，open Finset）、`IsPrimitiveRoot.pow_eq_one_iff_dvd`、
  `Nat.mod_modEq`/`Nat.ModEq.refl/.add`、`Nat.mod_add_mod`、`NeZero.pos/.ne` 均可用。

**paper14 同步（v1.6 第六轮）**：文首形式化支撑清单 Hall 条目追加 weyl_trace_orth
并把 Weyl 迹正交性移出开放清单（"唯一不可约表示"表示论结构定理登记开放）；§3
层级标注段改述（Weyl 迹正交性已机器证明）；结论 C2 残余开放列举同步；版本记录
v1.6 追加第六轮摘要。

**残余开放（均已登记，Weyl 迹正交性已移出）**：陈数整性 C = (1/2π)∫F ∈ ℤ 与
TKNN 场论形式（需环面积分/拓扑度/Kubo 基础设施）；唯一不可约表示 = Landau 能级
载体的表示论结构定理（Schur/矩阵代数表示论）；谱投影参数导数（Berry 切向量构造
层）；Harper 谱隙/Hofstadter Butterfly；ρ 的 PF 不动点存在性；T→0 算子收敛（远期）。

### 2026-09-13：Weyl 基定理闭合（HallEmergence，线性无关 + 张成 Mₙ(ℂ)，零 sorry）

**交付定理**（`HallEmergence.lean` 新增，全库 3700 jobs 编译通过）：

| 名称 | 可见性 | 内容 |
|------|--------|------|
| `weyl_basis_linearIndependent` | public | {U^a V^b}_{a,b<n} 在 ℂ 上线性无关（LinearIndependent，索引 Fin n × Fin n） |
| `weyl_span_top` | public | span ℂ {U^a V^b} = ⊤——n² 个 Weyl 元张成 Mₙ(ℂ)（线性无关 + Fintype.card = finrank 论证，经 LinearIndependent.span_eq_top_of_card_eq_finrank） |
| `weyl_pairing` | private | 对偶配对 Tr(W_p · D_q) = n·δ_{pq}，D_q = V^{n−b'}U^{n−a'}——线性无关的核心 |
| `weyl_mul_dual` | private | W_p · D_q = ω^{c·a'} • (U^{a+n−a'} V^{b+n−b'})，c = b+(n−b')（配对重排） |
| `clock_shift_weyl_gen` | private | Weyl 关系全 n ≥ 1 情形（n=1 退化 U=V=1、ω₁=1 并入，by_cases + Fin 1 平凡性） |
| `clock_pow_shift_weyl`/`clock_shift_pow_weyl`/`shift_pow_clock_weyl` | private | 幂次 Weyl 换位：U^aV = ω^a·VU^a；U^aV^c = ω^{ac}·V^cU^a；V^cU^d = ω^{cd}⁻¹·U^dV^c（归纳 + 取逆） |
| `weyl_scalar` | private | ω^{ac}·(ω^{c(a+n−a')})⁻¹ = ω^{ca'}——指数差 c·n 经 ω^n = 1 吸收（calc + pow_add/pow_mul） |
| `nat_add_sub_mod_eq_zero` | private | a,a'<n 时 (a+(n−a'))%n = 0 ⟹ a = a'（dvd 分解 n·k，0<a+n−a'<2n ⟹ k=1） |
| `trace_sum_smul_fin` | private | Tr(∑ g p • M p) = ∑ g p · Tr(M p)（经 Matrix.traceLinearMap 的 map_sum/map_smul） |

**证明主线**：迹配对 ⟨W_p, D_q⟩ = Tr(W_p D_q)——W_p D_q 经两次幂次换位化为
ω^{c·a'} • U^{a+n−a'} V^{b+n−b'}（c = b+(n−b')；标量化简靠 ω^{c·n} = (ω^n)^c = 1），
再用 weyl_trace_orth 判 (a+n−a')%n、(b+n−b')%n：对角 n、离对角 0。线性无关取
g 使 ∑ g p • W p = 0，右乘 D_q 取 trace 得 g q · n = 0 ⟹ g q = 0。
张成由 LinearIndependent.span_eq_top_of_card_eq_finrank：card(Fin n × Fin n) = n² =
finrank Mₙ(ℂ)（Module.finrank_matrix + finrank_self）。

**技术要点（本轮新踩实）**：

- **`•` 优先级高于 `*`**：`r • x * y` = (r • x) * y；rw 链中凡涉及 smul 与 mul
  混合重排，**一律用显式参数的 smul_mul_assoc/mul_smul_comm/← smul_mul_assoc**，
  无参 rw 会在求和体/• 混合型上 "pattern not found"。
- **rw 的显式实例参数**：`rw [Finset.sum_mul]` 等在求和体内失配时，改
  `rw [Finset.sum_congr rfl fun i _ => smul_mul_assoc (g i) (W i) Dq]` 形式。
- **omega 不从 `NeZero n` 实例提取 n ≠ 0**：`1 ≤ n` 须显式
  `Nat.one_le_iff_ne_zero.2 (NeZero.ne n)`。
- **Nat 截断减法**：`(a + (n − a'))` 与 `(a + n − a')` 语法不同但 a' ≤ n 时相等，
  引理间传递需显式 `have h2 : a + n - a' = a + (n - a') := by omega` 桥接。
- **Fin 投影规约**：`rcases p with ⟨a, b⟩` 后目标里残留 `(⟨a,b⟩ : _).1`，
  需 `dsimp only` 规约，否则后续 rw/have 模式失配。
- **traceLinearMap 显式参数**：`Matrix.traceLinearMap` 的 (n α R) 为显式参数，
  应用须写全称 `Matrix.traceLinearMap (Fin n) ℂ ℂ`（@[simps] 生成 _apply 引理）。
- `Nat.dvd_iff_mod_eq_zero`（本版无 Nat.mod_eq_zero_iff_dvd）；
  `Nat.add_sub_cancel'`（(a:ℕ)+(n−(a:ℕ)) = n，免 omega 直接给）；
  `Nat.mul_lt_mul_left (h : 0 < m)` 为 iff（.1 得 k < 2）。
- `map_sum` 方向：f (∑) = ∑ f（不要 .symm，按 calc 步骤方向取用）。

**paper14 同步（v1.6 第七轮）**：文首形式化支撑清单 Hall 条目追加 Weyl 基定理
（weyl_basis_linearIndependent + weyl_span_top）；§3 层级标注段改述（结构定理
向量空间形式闭合）；结论 C2 同步；版本记录 v1.6 追加第七轮摘要。

**残余开放（均已登记）**：陈数整性 C = (1/2π)∫F ∈ ℤ 与 TKNN 场论形式；
结构定理表示论层（商代数 ℂ⟨U,V⟩/(UV−ωVU, Uⁿ−1, Vⁿ−1) → Mₙ(ℂ) 代数同构 +
Schur 唯一性，需商代数基础设施）；谱投影参数导数（Berry 切向量构造层）；
Harper 谱隙/Hofstadter Butterfly；ρ 的 PF 不动点存在性；T→0 算子收敛（远期）。

### 2026-09-13：商代数同构闭合——结构定理表示论层（magAlgEquiv）

**定理（零 sorry，`HallEmergence.lean`，全库 3701 jobs 编译通过）**：

- `magneticAlgebra n : Type`（abbrev）：磁平移商代数 `RingQuot (magRel n)`，即
  `ℂ⟨U,V⟩/(UV − ωₙVU, Uⁿ − 1, Vⁿ − 1)`。取 abbrev 而非 def——否则 ℂ-代数实例
  在类型类推断下不可见（`magL` 的 span 与 smul_mem 全部失实例）。
- `magHom n : magneticAlgebra n →ₐ[ℂ] Mₙ(ℂ)`：泛性质下降。`RingQuot.liftAlgHom`
  需对三条生成关系逐条验证像满足同一关系：① Weyl 关系由
  `clock_shift_weyl_gen`（n ≥ 1 全范围）承担；②③ 幺幂关系由新证
  `clock_pow_one`（`(ωⁿ)^i = 1` 直接 pow_mul + omega_pow，**勿用 Nat.mul_comm**）
  与 `shift_pow_one`（循环移 n 步 = 恒等，`shift_pow n i j` + Fin.ofNat n n = 0）。
- `magHom_surjective`：Weyl 基像族 ⊆ range 且 span = Mₙ(ℂ)（weyl_span_top）
  ⟹ range = ⊤。
- `magBasisMap n : (Fin n × Fin n → ℂ) →ₗ[ℂ] magneticAlgebra n`（按 Weyl 基展开）
  满射：`magAlg_span`（商代数张成定理：L = ⊤）+ 单点支撑坐标 `magSum_single`。
- `magFinite`（Module.Finite ℂ）→ `magFinrank_le`（≤ n²）+ 结构同态满射下界
  → `magFinrank_eq`（finrank 商代数 = finrank Mₙ(ℂ) = n²，双边夹）。
- `magAlgEquiv n : magneticAlgebra n ≃ₐ[ℂ] Matrix (Fin n) (Fin n) ℂ`：
  `AlgEquiv.ofBijective`，单射由 `LinearMap.injective_iff_surjective_of_finrank_eq_finrank`
  （命名参数 `f := (magHom n).toLinearMap`——隐参 f 不显式给出会因 AlgHom/LinearMap
  两层 coe 无法合一报错）+ 满射合成。

**private 引理链**：`magWeyl`（UV=ωVU，商关系，mkAlgHom_rel + Or.inl 析取 +
`rw [map_sub, map_mul×3, AlgHom.commutes, ← Algebra.smul_def, map_zero, sub_eq_zero]
at h0`）→ `magPowX`/`magPowY`（Uⁿ=Vⁿ=1，Or.inr 两支）→ `magXpow_mod`/
`magYpow_mod`（降幂：conv_lhs `rw [← Nat.mod_add_div, pow_add, pow_mul]` +
幺幂引理 + one_pow/mul_one）→ `magXShiftWeyl`（单变量归纳）→ `magXpowShiftWeyl`
（双变量归纳）→ `magYpowXpow`（取逆）→ `magWeylElem_zero/left/right`（单型元
归一：`show` 归一 + `← magXpow_mod 1` 等吸收模幂）→ `magWeylElem_mul`
（W_p·W_q = ω^{−bc}·W_{(a+c)%n,(b+d)%n}：magYpowXpow 换位 + smul_mul_assoc/
mul_smul_comm 显参重排 + 降幂）→ `magL_mul_mem`（L 乘法封闭，双侧
span_induction）→ `magAlg_span`（FreeAlgebra.induction 四情形）。

**技术要点（本轮新踩实）**：

- **本版 Mathlib `smul_smul` 方向为 `a • b • x = (a*b) • x`（合并方向）**：
  `rw [smul_smul]` 把 `a⁻¹ • (a • x)` 压成 `(a⁻¹*a) • x`——与旧版记忆相反，
  本轮 magYpowXpow 最初按 `← smul_smul` 写，报 pattern `(?a₁*?a₂)•?b` not found；
  587 行既有成功用例（clock_shift_weyl_gen 链）即为正向前例。
- **`Submodule.smul_mem` 三显参** `(p)(r)(h)`：`Submodule.smul_mem _ _ iha`。
- **新版 `Submodule.span_induction` 是依赖 motive**：
  `refine Submodule.span_induction (p := fun x _ => ...) ?_ ?_ ?_ ?_ hx` 后按
  mem/zero/add/smul 顺序 `·` bullets。
- **`eq_top_iff.2` 给出 `∀ x ∈ ⊤, x ∈ p`（⊤ ≤ p 形态）**：`intro z _` 留下的
  `_ : z ∈ ⊤` 会进上下文并被 `induction` 泛化进 motive（ha 变成
  `mk a ∈ ⊤ → mk a ∈ L` 的箭头类型、mul/add 情形全部失配）——必须
  `rintro z -` 立即清除，motive 才干净。
- **RingQuot 的 add/mul 非 defeq**：凡 `mk (a*b)` 与 `mk a * mk b` 转换一律
  `rw [map_mul]`/`rw [map_add]`（magAlg_span 的 mul/add 情形；add 情形本轮
  补 map_add）。
- **`Submodule.span_le` 后的 range 目标是 SetLike coe**：goal `x ∈ ↑(range f)`
  须 `rw [SetLike.mem_coe, LinearMap.mem_range]` 再 exact ⟨...⟩。
- **`shift_pow` 的第一个显参是幂次 b : ℕ**：`rw [shift_pow i j]` 会把 Fin 的 i
  经 coercion 当成 b = ↑i 而失配——必须 `rw [shift_pow n i j]`。
- 隐参定理调用一律命名参数：`(magHom_surjective (n := n))` 等——直接跟 `n` 会被
  解析成 Surjective 的 ∀-参数 b。
- `Set.mem_range_self`（比 `⟨_, rfl⟩` 好用：后者类型无法确定）。
- magGen/magBasisMap/magFinite 均需 `noncomputable`（依赖 exp/clock）。

**paper14 同步（v1.6 第八轮）**：文首形式化支撑清单 Hall 条目追加 magAlgEquiv；
§3 层级标注段（第五轮建立，第六、七、八轮升级）追加表示论层闭合段；结论 C2
同步；版本记录 v1.6 追加第八轮摘要。

**残余开放（均已登记）**：陈数整性 C = (1/2π)∫F ∈ ℤ 与 TKNN 场论形式；
Schur 唯一性（任意 n 维不可约表示等价于标准表示，需 Burnside/稠密性定理
基础设施——magAlgEquiv 已给"存在唯一 n 维不可约表示"的代数同构形态）；
谱投影参数导数（Berry 切向量构造层）；Harper 谱隙/Hofstadter Butterfly；
ρ 的 PF 不动点存在性；T→0 算子收敛（远期）。

### 2026-09-13：谱投影切向量代数层闭合

**定理（BerryChern.lean 新增 §2.5"投影切向量的代数层"，全部零 sorry）**：

| 定理 | 陈述 | 角色 |
|---|---|---|
| `projTangent_intraBand_zero` | P²=P ∧ A = P·A + A·P ⟹ P·A·P = 0 ∧ (1−P)·A·(1−P) = 0 | 约束方程解的带内消没（Berry 联络的规范结构） |
| `trace_proj_commutator_interband` | Tr(P[A,B]) = Tr(PA(1−P)B) − Tr(PB(1−P)A) | 曲率只依赖带间矩阵元 |
| `berryCurvature_interband` | 曲率的带间形式封装 | 曲率层接入 |
| `trace_proj_commutator_twoCommutator` | Tr(P[[P,A],[P,B]]) = −Tr(P[A,B]) | 双交换子形式（标准 Berry 曲率写法） |

**HallEmergence 新增**：`occupiedProjection_commute`：H·P = P·H（[H,P]=0）。
证法一行核心：`IsSelfAdjoint.commute_cfc hH.isSelfAdjoint (Commute.refl H) occFn`
（泛函演算交换性：与 H 交换的元与 cfc f H 交换），再经
`Matrix.IsHermitian.cfc_eq hH occFn` 把 cfc occFn H 换回占据投影。
角色：绝热微扰 Sylvester 方程 [H, Ṗ] = [P, Ḣ] 左端交换性前提。

**技术要点（本轮确立，勿忘）**：
- `rw` 每步只重写首个实例化匹配项的全部出现；b、c 不同的乘法分配须
  `simp only [mul_sub]` 迭代到不动点，再逐 kill 显式 `rw` 链。
- `noncomm_ring` 的右结合正规形会隐藏 P·P 相邻模式——关系 kill 必须显式
  `rw`，不能指望 simp 集。
- kill 模式范例：`rw [(mul_assoc P (P*A*P) B).symm, hPAP, mul_zero, zero_mul]`
  （association 修复 + 关系 kill + 零元清理）。
- `conv_lhs => rw [hA]` 防止 hA 改写 RHS（x = x+x ⟹ x = 0 的消去步）。
- 曲率封装用 `calc ... := rfl` 起步展开定义，再 `rw [h]`（h 为显式参数的
  have）——直接 `rw [trace_proj_commutator_interband hPAP hPBP]` 会因
  metavars 未实例化失败（已踩过）。
- dot 投影坑：`hH.isSelfAdjoint.commute_cfc ...` 报 "Invalid field"——
  `IsSelfAdjoint` 是 `star a = a` 的 def，结构投影不可用；改显式常量调用
  `IsSelfAdjoint.commute_cfc hH.isSelfAdjoint ...`。
- 需 `import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute`
  （该常量所在模块不被 `HermitianFunctionalCalculus` 传递引入）。
- 之前的谱定理证法（`rw [hH.spectral_theorem]`）撞 motive 问题（H 出现在
  hH 类型里，structure projection 使 motive 不 type correct）——确认无解，
  勿回头。

**paper14 同步（v1.6 第九轮）**：文首形式化支撑清单 Hall 条目追加
occupiedProjection_commute + BerryChern §2.5 四定理；§3 层级标注段升级
（"第六、七、八轮升级"→"第六、七、八、九轮升级"，残余句改写：切向量约束
代数层闭合、分析构造开放）；结论 C2 补记第九轮；版本记录 v1.6 行末追加
第九轮摘要。全库零 sorry，3705 jobs 编译通过。

**残余开放（更新）**：陈数整性场论；Schur 唯一性；**切向量分析构造**
（∂ₓP 存在性，cfc 参数可微性/Kato 微扰论——接替原"谱投影参数导数"条目，
约束层已闭合）；Harper 谱隙；ρ 的 PF 不动点；T→0 算子收敛（远期）。

### 2026-09-13：Harper 谱对称层闭合（谱隙首层）

**定理（HallEmergence.lean 新增，全部零 sorry）**：

| 定理 | 陈述 | 角色 |
|---|---|---|
| `omega_pow_half_eq_neg_one` | n ≥ 2 偶 ⟹ ω_n^{n/2} = −1 | 谱对称相位核心（本原性排除 +1） |
| `clock/shift_commute_star` | Commute U U† / V V† | 幂次幺正性的交换性前提 |
| `clock/shift_pow_mul/star_self`（4 条） | U^c(U^c)† = (U^c)†U^c = 1 等 | 幂次幺正性（W 酉性的构件） |
| `shift_pow_conj_clock` | V^c U (V^c)† = ω^{−c} • U | 共轭作用（一） |
| `clock_pow_conj_shift` | U^a V (U^a)† = ω^a • V | 共轭作用（二） |
| `harper_conj_unit` | W = U^{n/2}V^{n/2} 酉（W W† = W†W = 1） | 谱对称酉元 |
| `harper_conjugate_neg` | n 偶 ⟹ W H W† = −H | **谱对称核心**：σ(H) = −σ(H) |
| `harper_trace_odd_pow_zero` | n 偶 ⟹ Tr(H^{2k+1}) = 0 | 迹推论：奇次谱矩消失（k=0 给出 Tr H = 0） |

**证明路径**：ω^{n/2} 是 1 的平方根（ω^n = 1）且本原性
（`IsPrimitiveRoot.pow_eq_one_iff_dvd` + `Nat.not_dvd_of_pos_of_lt`）排除 +1；
z² = 1 ∧ z ≠ 1 在 ℂ 中 ⟹ z = −1（`sq_sub_sq`/`mul_eq_zero`）。共轭作用由
Weyl 幂次换位（`shift_pow_clock_weyl`/`clock_pow_shift_weyl`）右乘 (V^c)† 得。
迹推论：`trace_pow_similar`（SpectralInvariant）给出
Tr((W H W†)^m) = Tr(H^m)，代入 W H W† = −H 与奇幂负性
（`(−H)^{2k+1} = −H^{2k+1}`：`pow_succ`/`pow_mul`/`neg_sq`/`mul_neg`）得
Tr = −Tr，2 无零因子（`two_ne_zero`）⟹ Tr = 0。

**技术要点（本轮确立，勿忘）**：
- **矩阵不是 `GroupWithZero`**：`mul_inv_cancel₀`/`inv_mul_cancel₀` 不可用——
  一切 `X * X⁻¹` 必须改写为 `X * star X`（幺正性 + `Matrix.mul_eq_one_comm`
  互推两侧）。
- **`smul_mul_assoc` 的模式是 `?r • ?x * ?y`（左结合）**：`A * (r • X) * B`
  形（ smul 在第二个因子）不是其子项——先 `mul_smul_comm`（x * r•y = r•(x*y)）
  或先用显式参数 `mul_assoc` 重组使 `r • X * B` 成为真子项。
- **star 展开的顺序敏感**：`rw [star_mul]` 裸跑会先命中内层 `star (clock^a *
  shift^a)` 而非外层——多 star 嵌套时一律显式参数
  `star_mul (W * clock) (star W)` 等逐层指定。
- `mul_eq_one_comm` 在**根命名空间**（非 Matrix.），需 `IsDedekindFiniteMonoid`
  （Mₙ(ℂ) 满足）。
- `Commute.mul_pow` 的幂次是显参：`(h).mul_pow c`；`Commute` 结构可用
  `h₁.trans h₂.symm` 构造（defeq 到等式）。
- `SpectralInvariant` 此前**无任何模块导入**——HallEmergence 已补
  `import MUFPFormalization.SpectralInvariant`。
- 最终纯加法恒等式（分配后求和 = 负和）`noncomm_ring` 报"try abel"——
  用 `abel`。
- 隐参定理裸调用遇 typeclass stuck：`harper_conj_unit (n := n)`。

**paper14 同步（v1.6 第十轮）**：文首形式化支撑清单 Hall 条目追加谱对称层；
§3 层级标注段升"十轮"并追加 Harper 谱结构第一定理段；结论 C2 补记第十轮；
版本记录 v1.6 行末追加第十轮摘要。全库零 sorry，3705 jobs 编译通过。

**残余开放（更新）**：Harper 谱隙收窄为**谱带定位/谱隙宽度**（中心对称 +
奇次谱矩消失已闭合）；陈数整性场论；Schur 唯一性；切向量分析构造；
ρ 的 PF 不动点；T→0 算子收敛（远期）。

### 2026-09-17：G2 定量桥"代数谱系"层面闭合（SuperfluidBridge.lean）+ Paper LVII v1.3

**任务背景**：用户明确"重建目标是真正的内生第一性推导，而不是仅止于标注或妥协"。此前
G2 的 `selfConsFunc_existsUnique` 确立了 $r$ 由方程唯一确定，但 **δ_SC = Δλ_min 的定量数值
桥未触及**——§8.6a 诚实自承"没有定量推导链从 Δλ_min 到 δ_SC"。本轮把该链补成定理。

**新建模块 `SuperfluidBridge.lean`**（namespace MUFPF，`lake build` 3132 jobs 通过，零 sorry）：

| 内容 | 定理/定义 | 数学内容 |
|------|-----------|----------|
| — | `selfConsC` | 自洽方程物理输入 c = a_BCS³·4π（恒正） |
| — | `a_BCS_pos`/`selfConsC_pos` | c > 0（可解性前提） |
| §2 | `r_star`/`r_star_spec`/`r_star_pos`/`r_star_closure` | 自洽唯一正根 r*=the r≥0 with f(r)=c：非负 + 严格正 + 方程闭合 |
| §3 | `deltaSC_categorical`/`deltaSC_explicit`/`deltaSC_categorical_pos`/`gap_ratio_categorical` | **定量跨尺度桥**：δ_SC = Δλ_min/r*，δ_SC/Δλ_min = 1/r* |
| §4 | `stiffness_categorical`/`stiffness_gap_genealogy`/`Tc_scaling_from_categorical` | 全链折叠：ρ₀ = (Δλ_min/r*)²/(2E_F)，T_c = γ√ρ₀（ρ₀ 的谱间隙因子取范畴谱间隙） |

**对 §8.6a"缺定量推导链"的闭合**（诚实边界，与 §4 一致）：范畴 Δ 内生贡献
Δλ_min 本身（`dl_min_pos`）、r* 的方程确定性与唯一性、代数谱系结构本身；物理输入
保留 a_BCS = 1/1.764（弱耦合普适比值）与 E_F（材料参数）。**残余开放**：把单一自洽
倍率 r* 分解为谱流 RG 多级常演化（Δλ_min→Δλ_min^EM→δ_SC）仍是在§8.7#5 登记的长程方向，
非本轮断言的计算内容。这标志 G2 从"结构关联"推进为"方程级定量谱系"（Paper LVII v1.3，
§8.6b 新增）。

**Paper LVII 同步（v1.2→v1.3）**：元数据版本/状态更新；形式化清单补 SuperfluidBridge；
§8.6a "没有定量推导链"改写为指向 §8.6b；新增 §8.6b 定量谱间隙谱系（式 8.10–8.15）；
§8.6#3、§8.7#5、§9.1 item 4a、§9.3、§9.4 全部同步。

**G2 至此的层级归属**：δ_SC 对 Δλ_min 的**无量纲倍率 1/r*** 已定理化（方程级定量谱系）；
δ_SC 的**绝对能标数值**（~meV）仍取决于物理输入（E_F 系、a_BCS），符合 §4 的诚实边界
"范畴 Δ 只产普适量"。模 G1 代数值的精确等式 r* = 0.874 在 Lean 实数层仍不可证（√3/√r*
无理性，Python 层独立给出），沿 2026-08-04 开放项登记。

### 2026-09-17（二）：G2 绝对能标——1.764 的内生谱来源（RN-ENDO-002）

**任务**：用户要求推导 `a_BCS = 1/1.764` 的内生来源，风险是过去一直把它当"BCS 全程物理锚"。

**推导（笔记 `spectral_origin_of_bcs_constant.md`，MUFPF-RN-ENDO-002）**：1.764 = π·e^{−γ_E}
（因 2Δ₀/k_BT_c = 2πe^{−γ_E} = 3.528，弱耦合精确）。分解：

- **e^{γ_E} 是谱 ζ 正则化常数**——调和谱求和 Σ1/k 在平凡极上的有限部，正是 MUFPF 谱 ζ 资产对象（非 BCS 特有）；
- **π 是费米型谱权重因子**——奇数频率 Matsubara 求和 Σ(−1)ⁿ/(n+1/2) = π/2 的结构因子（超导=配对的谱签名）。

**Lean 普适性定理 `universal_ratio_cancellation`**（新模块 `BCSConstantOrigin.lean`，零 sorry）：
两处隙-闭合 `exp(1/λ)=2ω_D/Δ₀` 与 `exp(1/λ)=a0·ω_D/T_c` 共享同一 exp(1/λ)，交叉消去 ω_D ⟹
**临界比 Δ₀/T_c = 2/a0 与耦合 λ、截断 ω_D 无关**。即 1.764 的普适性是被证明（λ、ω_D 无关），
而非被预设为锚。

**归级（含不伪称）**：
- ✅ 普适性（聚类/截断无关，临界比=2/a0）——Lean4 定理
- ✅ 分解 1.764 = πe^{−γ_E}（两个全域普适谱常数）——推导+数值
- ✅ e^{γ_E} 机制 = 谱 ζ/Mellin 有限部（MUFPF 谱资产）
- ❌ π、e^{γ_E} **数值**由范畴 Δ 单独钉死——不伪称（全域常数 + 费米谱权重是输入）
- ❌ 1/1.764 = πe^{−γ_E}（超验）在 Lean 实数层多项求值——不伪称，数值由分析层给出

**对 G2 的影响**：绝对能标从"单一 BCS 锚 1.764"内化为"π×e^{−γ_E} 两个全域谱常数的分解"，
且普适性由定理保证。范畴 Δ 只产普适量这一边界不变，但 1.764 的普适性现为**证明件**而非**预设件**。
**残余**：π、e^{γ_E} 数值的范畴 Δ 闭合（需从 Cl(1,7) 内生导出费米谱权重 s=1 与奇数频率求和才可）——本讲明确不伪称。

### 2026-09-17（三）：G2 比值级收口——ρ₀ 链的无量纲普适折叠（Paper LVII v1.5）

**任务**：把整条谱刚度链 $\rho_0 \to \sqrt{\rho_0} \to T_c$ 折叠为无量纲普适比，证明 $T_c/\Delta_{\text{BCS}}$ 与一切材料能标（$E_F$、$k_B$）无关。

**形式化**（`SuperfluidStiffness.lean` §5，三定理零 `sorry`，构建 4078 jobs）：
- `universal_ratio_collapse_dimensionless`：把 $\rho_0 = \Delta^2/(2E_F)$、$\gamma = \sqrt{2E_F}\cdot a_{\text{BCS}}$ 代入，关键恒等式 $\sqrt{2E_F}\cdot\sqrt{\Delta^2/(2E_F)} = \Delta$ 使 $E_F$ 恰好约掉 → $\gamma\sqrt{\rho_0}/\Delta = a_{\text{BCS}}$
- `Tc_dimensionless_universal_ratio`：经标度律链 $T_c/\Delta_{\text{BCS}} = a_{\text{BCS}} = 1/1.764$（与材料能标无关的纯普适常数）
- `dimensionless_ratio_at_fundamental_gap`：在 Cl(1,7) 基本谱间隙处 $T_c(dl_{\min})/dl_{\min} = a_{\text{BCS}}$

**对 G2 的层级影响**：范畴 Δ 内生推出的所有无量纲比——$\Delta\lambda_{\min}$、$r^*$、$T_c/\Delta_{\text{BCS}}$——已全部闭合，构成 G2 绝对能标的"**比值级收口**"。与 §8.6c 的守恒普适性（耦合/截断无关）互补，本节是**能标普适性**（Fermi 能、单位制无关）。剩余绝对能标数值 $E_F$ 为定义级物理输入，不伪称可约化；与 π/e^{γ_E} 数值的范畴闭合（上条残余）一并保留为 §8.7#6。

### 2026-09-17（四）：G2 谱流 RG 多级常演化——代数因子分解层闭合（Paper LVII v1.6，RN-ENDO-004）

**任务**：推进 §8.7#5——把单一自洽倍率 $1/r^*$ 分解为谱流 RG 多级常演化，把"代数骨架"显式化为"纯规范表示因子 × BCS 谱流动力学因子"的两级链。

**分解**（`SpectralFlowRG.lean`，12 定义/定理零 `sorry`，编译通过）：
- 电磁中间级 $\Delta\lambda_{\min}^{(\text{EM})} = \Delta\lambda_{\min}/\sqrt{3}$（SU(2) Casimir 谱间隙比 $\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = 1/\sqrt{3}:1:\sqrt{2}$ 的第一分量，**非自由参数**）
- 降级倍率 $k_1 = \sqrt{3}$（纯规范表示）、$k_2 = r^*/\sqrt{3}$（BCS 动力学）；**折叠不变式** $k_1k_2 = r^*$（`RG_telescoping`）
- 链一致 $f_1 = 1/\sqrt{3}$、$f_2 = \sqrt{3}/r^*$，$f_1f_2 = 1/r^* = \delta_{\text{SC}}/\Delta\lambda_{\min}$（`gap_ratio_telescoping`/`gap_ratio_multistage_eq_single`/`RG_chain_reproduces_single`）
- 数值核验：`verify_spectral_flow_RG_multistage.py`（mpmath 50 位，相对偏差 < 10⁻⁴⁵）全过

**对 G2 的层级影响**：§8.7#5 的开放方向被**显式拆分**为两层——
- ✅ **代数因子分解层**（已闭合）：$1/r^*$ 不再是一个黑箱倍率，而是"规范表示因子 $1/\sqrt{3}$ × 动力学因子 $\sqrt{3}/r^*$"的产物，两级路径与单级自洽代数一致（两个不变式定理化）。
- ⚠️ **动力学 RG 层**（仍开放）：把逐级倍率 $k_1,k_2$ 由谱流方程在中间级处**逐步重新求解**内生涌现（而非后验写成 $r^*/\sqrt{3}$），需要跨尺度谱流方程 RG，登记 §8.7#5 剩余方向；且 $\Delta\lambda_{\min}^{(\text{EM})} < \Delta\lambda_{\min} < \delta_{\text{SC}}$ 不按能标单调排列，"常演化"指固定倍率的两级因子分解。

**Paper LVII 同步（v1.5→v1.6）**：新增 §8.6d 谱流 RG 多级常演化（式 8.18–8.21）、§4 主要结果 4c、更新形式化清单、更新 §8.7#5/§8.6a 展望/§8.6b 结尾/结论 9.3/9.4 为"代数层闭合、动力学层开放"。路线图 phase70 同步形式化表与开放问题 #5。推导笔记：`spectral_flow_rg_multistage_evolution.md`（MUFPF-RN-ENDO-004）。

**G2 至此的完整层级**：无量纲倍率 $1/r^*$（§8.6b）→ 绝对能标 $1.764 = \pi e^{-\gamma_E}$（§8.6c）→ 比值级收口 $T_c/\Delta = a_{\text{BCS}}$（v1.5）→ **多级因子分解 $1/r^* = (1/\sqrt{3})\cdot(\sqrt{3}/r^*)$**（§8.6d）→ **三级/多带谱隙谱系 $1/\sqrt3:1:\sqrt2$**（§8.6e）。剩余：$E_F$ 数值（定义级输入）、π/e^{γ_E} 数值（RN-ENDO-003 §5 不伪称）、动力学 RG 逐级重解（§8.7#5 剩余方向）、带辨认对应（§8.7#8）。

### 2026-09-17（五）：G2 三级/多带谱系——SU(2) Casimir 谱间隙比三分支推广闭合（Paper LVII v1.7）

**任务**：把 §8.6d 的两级链推广到三级/多带谱系——沿 SU(2) Casimir 谱间隙比 $\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = \sqrt{1/3}:1:\sqrt2$ 的全部三个分量，构造三分支多带谱间隙谱系。

**分解**（`MultibandSpectralBridge.lean`，22 定义/定理零 `sorry`，编译通过 3134 jobs）：
- 三分支带隙（共享唯一自洽根）$\delta_{\text{SC}}^{(i)} = \Delta\lambda_i/r^*$，其中 $\Delta\lambda_1 = \sqrt{1/3}\,\Delta\lambda_{\min}$、$\Delta\lambda_2 = \Delta\lambda_{\min}$、$\Delta\lambda_3 = \sqrt2\,\Delta\lambda_{\min}$；带2 谱间隙即 §8.6b 单级桥 $\delta_{\text{SC}}$（`deltaSC_band2_eq_categorical`）
- **多带隙比保持**（核心不变式，[Paper XIV §6.1] 预言定理化）：三分支经统一 ÷$r^*$ 后隙比 = Casimir 分量比 = $1/\sqrt3:1:\sqrt2$（`band_ratio_1_over_2`=$\sqrt{1/3}$、`band_ratio_3_over_2`=$\sqrt2$、`band_ratio_3_over_1`=$\sqrt6$、`band_ratio_matches_casimir_12`/`band_ratio_matches_casimir_32`）
- **Casimir 升序三级塔**：$k_{12} = \Delta\lambda_2/\Delta\lambda_1 = \sqrt3$（即 §8.6d 的 $k_1$）、$k_{23} = \Delta\lambda_3/\Delta\lambda_2 = \sqrt2$、乘积闭合 $k_{12}k_{23} = \sqrt6$（`casimir_tower_2_over_1`/`casimir_tower_3_over_2`/`casimir_tower_3_over_1`/`casimir_tower_product_closure`）
- 数值核验：`verify_multiband_spectral.py`（mpmath 50 位，相对偏差 < 10⁻⁴⁵）全过

**对 G2 的层级影响**：§8.6d 只用了 Casimir 谱间隙比**第一分量**作 EM 中间级；§8.6e 沿全部三分支推广，把 Paper XIV §6.1 的"多带隙比 SU(2) Casimir 量化"**预言升级为定理**。
- ✅ **代数多带因子分解**（已闭合）：带隙 = Casimir 分量 ÷ 唯一根；隙比保持 + 三级塔为定理（零 `sorry`），与 §8.6d 折叠 $k_1k_2=r^*$ 同类（"多级连乘 = 单级比值"代数不变式）。
- ⚠️ **带辨认对应**（仍开放）：三个分支谱间隙与具体材料的带辨认对应（如 MgB₂ 两带、铁基多带）待物理层，登记 §8.7#8；动力学逐级重解（§8.7#5 剩余方向）仍开放。

**Paper LVII 同步（v1.6→v1.7）**：新增 §8.6e 三级/多带谱系（式 8.22–8.24）、§4 主要结果 4d、更新形式化清单、更新 §8.7#8 多带预言状态（定理化完成、带辨认开放）、结论与跨尺度关联段落。路线图 phase70 同步形式化表。推导笔记：`spectral_flow_rg_multistage_evolution.md`（MUFPF-RN-ENDO-004，v1.1 新增 §10 多带推广）。

### 2026-09-17（六）：G2 谱流方程尺度动力学第一注入——动力学 RG 层诊断（Paper LVII v1.8，RN-ENDO-004）

**任务**：对 §8.7#5 的**动力学 RG 层**给出第一注入——不改变 $k_2$ 的定义，而把"动力学"内容钉在谱流自洽方程自身的尺度结构上，量化诊断"为何多级常演化只能是有限两级代数骨架"。

**分解**（`SpectralFlowDynamicsRG.lean`，15 定义/定理零 `sorry`，编译通过 3134 jobs）：

- 运行反常维度 $\zeta(r) = \dfrac{r f'(r)}{f(r)} = \dfrac{1 + \tfrac32\sqrt3\sqrt r}{1+\sqrt3\sqrt r}$ 严格落入 $(1,\tfrac32)$（`anom_dim_gt_one`/`anom_dim_lt_threehalf`/`anom_dim_interior`）且单调 $1\to\tfrac32$ ⇒ $f$ **非标度不变**（无连续重整化流）
- EM 残差流 $f_{\text{EM}}(u) = f(\sqrt3 u)$：**闭合** $f_{\text{EM}}(k_2) = f(r^*) = c$（`em_residual_closure`），且 $k_2$ 是 $f_{\text{EM}}=c$ 的唯一正根（`em_residual_root_unique`）——闭常数 $c$ 在规范因子 $\sqrt3$ 缩放下 RG 不变（`closed_constant_rg_invariant`）
- 数值核验 `verify_spectral_flow_dynamics_RG.py`（mpmath 60 位，15 项全过）：$\zeta(r^*)=1.3091088\ldots$，端点 $\zeta\to1$、$\zeta\to\tfrac32$，$\zeta$ 单调，非标度不变两项反例判据，残差流闭合三项全过

**归级**：
- ✅ **尺度诊断**（定理）：运行反常维度落带 + 非标度不变反例判据（无连续重整化流，是"常演化只能是代数骨架"的定量判据）
- ✅ **规范缩放坐标下残差流重构**（定理）：$f_{\text{EM}}(k_2)=c=f(r^*)$、$k_2$ 唯一正根
- ⚠️ **仍开放**（§8.7#5 核心）：$k_2$ 由 EM 尺度自身**独立**谱流方程（带新物理锚）自洽涌现，而非由单一 $c$ 的反向重标度——需真正发展跨尺度谱流方程重整化群方法

**Paper LVII 同步（v1.7→v1.8）**：新增 §8.6f 谱流方程的尺度动力学（运行反常维度 + 非标度不变 + EM 残差流闭合）、§4 主要结果 4e、更新形式化清单、更新 §8.7#5 为"动力学层第一注入已落地、EM 独立谱流方程仍需发展"。路线图 phase70 同步形式化表与开放问题 #5。推导笔记：`spectral_flow_rg_multistage_evolution.md`（MUFPF-RN-ENDO-004，v1.2 新增 §11）。

**G2 至此的完整层级**：无量纲倍率 $1/r^*$（§8.6b）→ 绝对能标 $1.764=\pi e^{-γ_E}$（§8.6c）→ 比值级收口（v1.5）→ 多级因子分解 $1/r^* = (1/\sqrt3)(\sqrt3/r^*)$（§8.6d）→ 三级/多带谱隙谱系（§8.6e）→ **尺度动力学诊断（运行反常维度 + 残差流闭合，§8.6f）**。剩余：$E_F$ 数值、π/e^{γ_E} 数值（不伪称）、EM 尺度独立谱流方程（§8.7#5 核心开放项）、带辨认对应（§8.7#8）。

### 2026-09-17（七）：G2 谱流 RG 流单参数族第二注入——折叠的流族读法（Paper LVII v1.9，RN-ENDO-004）

**任务**：把 §8.6d 钉在单一物理点 $c_0$ 的折叠 $k_1k_2=r^*$ 推广为**以闭合常数 $c$ 为参数的单参数流族**，让"多级常演化"获得连续读法，并把 §8.6f 的运行反常维度沿流升级为 **β 通量**直证。

**分解**（`SpectralFlowRGFlow.lean`，23 定义/定理零 `sorry`，编译通过 3135 jobs）：

- 流族 $\rho(c) = f^{-1}(c)$：`r_star_flow_spec`/`r_star_flow_closure`（$f\circ\rho=\mathrm{id}$）、`flow_inverse_point`（$\rho\circ f=\mathrm{id}$，水平簇即轨迹）、`r_star_flow_pos`、`r_star_flow_at_physical`（$\rho(c_0)=r^*$，§8.6b 全是 $c=c_0$ 截线）
- **流不变折叠**：`flow_telescoping`（$k_1k_2(c)=\rho(c)$ 沿线保持）、`flow_em_anchor_constant`（EM 锚 $\Delta\lambda_{\min}^{(\text{EM})}=\Delta\lambda_{\min}/\sqrt3$ 不随 $c$ 演化）、`flow_anchor_orthogonal`（所有 $c$ 依赖唯一装入动力学因子 $k_2(c)=\rho(c)/\sqrt3$）、`flow_k2_at_physical`
- 流单调：`r_star_flow_lt`、`flow_k2_lt`（$c_1<c_2\Rightarrow\rho/k_2$ 严格上升）
- **β 通量**：`rg_beta = 1/\zeta$`，`rg_beta_gt_two_thirds`/`rg_beta_lt_one`/`rg_beta_interior`（$\in(\tfrac23,1)$）；β-形式 ODE $d\ln r/d\ln c=1/\zeta(r)$ 的**逆流积分解**恰是流族自身
- 运行指数沿流单调：`anom_dim_strictMono`（$\zeta$ 在 $r$ 上严格增）、`flow_anom_dim_lt`（沿流严格上升 $1\to\tfrac32$）、`flow_rg_beta_gt`（β 沿流严格递减 $1\to\tfrac23$）
- 数值核验 `verify_spectral_flow_RG_flow.py`（mpmath 50 位，50/50 全过）：$\rho(c_0)=r^*\approx0.874037$、折叠沿线保持、β∈(2/3,1)、β-ODE 中心差分 12 节点 $10^{-6}$ 精度、端点 $\zeta\to1/\tfrac32$

**归级**：
- ✅ **流族结构**（定理）：$\rho(c)$ 唯一性、沿 $c$ 单调性、流不变折叠沿线保持、β 通量有界与沿流单调；β-ODE 以**逆流代数形式**闭合（水平簇即轨迹），未展开柯西–Lipschitz 存在性
- ⚠️ **仍开放**（§8.7#5 核心）：EM 中间级由*自身独立*谱流方程自洽涌现（而非经同一 $c$ 的逆向重标度）；用**独立能量锚选定 $c$ 截线**把材料能量尺度落入谱流族——真正发展跨尺度谱流方程重整化群方法

**Paper LVII 同步（v1.8→v1.9）**：新增 §8.6g 谱流 RG 流单参数族、§4 主要结果 4f、更新形式化清单、更新 §8.7#5/§9 跨尺度关联段落为"第二注入已落地、开放项收窄为 EM 独立谱流方程 + 独立能量锚选截线"。路线图 phase70 同步形式化表与开放问题 #5。推导笔记：`spectral_flow_rg_multistage_evolution.md`（MUFPF-RN-ENDO-004，v1.3 新增 §12）。

**G2 至此的完整层级**：无量纲倍率 $1/r^*$（§8.6b）→ 绝对能标 $1.764=\pi e^{-γ_E}$（§8.6c）→ 比值级收口（v1.5）→ 多级因子分解（§8.6d）→ 三级/多带谱隙谱系（§8.6e）→ 尺度动力学诊断（§8.6f）→ **谱流 RG 流单参数族（流不变折叠沿线保持 + β 通量 + 逆流 ODE 解，§8.6g）**。剩余：$E_F$ 数值、π/e^{γ_E} 数值（不伪称）、EM 尺度独立谱流方程 + 独立能量锚选 $c$ 截线（§8.7#5 核心开放项）、带辨认对应（§8.7#8）。

### 2026-09-17（八）：断点最早化审计——最早断点钉死为"选 √3 / 选 Δλ_min"两行 def（RN-ENDO-009）

**任务转向（响应"先研究最早的断点而不先旁推约束原理"）**：在"不得妥协的内生第一性"前提下，对
§8.6b/e/f/g 全线做**断点最早化扫描**，取代"再开新层/再折叠"的惯性。审计对照已形式化 Lean 源得出：
- **最早断点精确落在两行定义**：`WeaveBCS.dl_min := spectralGap 8`（选世界点）与
  `WeaveBCS.dl_1 := √(1/3)·dl_min`（选 √3）。下游（`dl_min_EM := dl_1`、`RG_k1=√3`、`k₂=r*/√3`、
  多带隙比、Casimir 塔、残差流、流族）全部只是这两行**定义展开的代数后果**，无独立内容。
- **铁证**：`MultibandSpectralBridge` 全部 `casimir_tower_*`/`band_ratio_*` 定理的证明体即
  `unfold dl_1` + 消去 dl_min，**无一从 `C₂=3/4` 或 Δ 导出 `√(1/3)`**；`WeaveBCS:68` 注释
  【2026-08-06 修复】√(2/3)→√(1/3) 证明该系数曾作为可调公设被编辑。
- **优先级反转（坐实）**：E1·锚自反性作用在 `dl_1` 之后的 c₀ 上，降为次位；**"选 √3 → 导出"为第一战线**
  （把 `dl_1` 系数由定义提升为定理，`√(1/3)` 由 Δ / `C₂=3/4` 长出）；其次 E3、E2、E1 按新顺位。
- π/e^{γ_E} 数值仍按"未闭合"处理（不得妥协：不因现状未证而冒充"必然不可达"）。
衍生笔记：`endogenous_earliest_breakpoint.md`（MUFPF-RN-ENDO-009）。

### 2026-09-17（九）：攻导出初报——1/√3 既有 λ_k 推导被发现，残余"选"下沉（RN-ENDO-009 v1.1）

对（八）登记目标首次攻击，核验 `scripts/paperX_ratio_fix.py` 发现：**1/√3 数值本身已有**良构推导
（SU(2) Casimir 特征值归一化 λ_k=√(k(k+1))）：
Δλ₁:Δλ₂:Δλ₃ = √2:√6:√12 = 1/√3:1:√2，其中 1/√3 = λ₁/λ₂ = √(1·2)/√(2·3)。**关键修正**：该推导用
**整数表示 C₂={2,6,12}(j=1,2,3)**，**非**基本表示 C₂=3/4（后者喂的是另一个 √3——编织度
d_BCS=2√(3/4)=√3，规范生成元守恒，`WeaveBCS.d_BCS`）。故框架内有两个来源不同的 √3。
- **1/√3 数值诚意为表示论定理（非待证）**；真正残余"选"下沉为**两个假设 + Δ 缺失**：(A) 扇区→表示
  赋值（为何 U(1)-EM↦j=1）；(B) 比例假设 gap∝√C₂；(C) 整个推导是纯 SU(2) 表示论，Δ(Sp 4-范畴)未出现。
- **公式化缺口**：dl_1 在 Lean 仍是 `def`；λ_k 推导只在分析层，非机器检查。
- **攻目标收紧**：不再重推数值；改从 Δ 导出赋值(A)+比例(B)（把"谱→耦合映射"从假设降为定理）；
  §4 的"由 C₂=3/4 长出"误判已纠正。RN-ENDO-009 升至 v1.1。

### 2026-09-17（十）：探 (A) 裁决 + v1.1 勘误（RN-ENDO-009 v1.2）

对"为何 U(1)-EM 落在最小 j 级"作可判定探访（据 `spectral_color_dynamics.md §8.4` 权威块 + 三脚本）：
- **v1.1 勘误**：§8.4 原文 λ_k∝√(k(k+1)) **k=2j** ⟹ 三级是 **j=1/2,1,3/2**（非整数 1,2,3）；且 λ_k=√(2j(2j+1)) **≠**√C₂=√(j(j+1))。比值 1/√3=√2/√6 只依赖 k=1,2，仍严格；受影响的是标签。
- **裁决：U(1)→最小级无 Δ 内推导**。§8.4 只推导"给定梯子 {k=1,2,3} 后的比值"，从未推导为何 U(1) 落 k=1；赋值属脚本自承"谱→耦合映射是框架假设（保留）"。Δ(Sp 4-范畴)全程不在场。
- **并列选定输入**：扇区排序、算子 A_GR 身份（为何特征值恰 √(k(k+1))）、k_max=8（P3 已自承"无非循环第一性来源——为模型输入"）三者为并列假设，无一条 Δ 内推导。
- **真内生目标（缺失）**：∃Δ→构造使 EM 扇区自然涌现于梯子最小级 + A_GR=√(4j(j+1)) 同源 + k_max 秩原理导出（"Δ→扇区→层级"三相合一）。RN-ENDO-009 升 v1.2。

### 2026-09-17（十一）：三相合一构造——λ=√(d(d-1)) 维数实现 + Δ 单调性候选（RN-ENDO-010）

推进三相合一，不再止于欠定。**重构（核验通过，`sector_hierarchy_check.py`）**：λ_k=√(k(k+1))，k=2j
令 d=2j+1 ⟹ **λ_j=√(d(d-1))，d=2,3,4**（维数坐标统一，j 记号隐藏了它）；d=2,3,4 → √2:√6:√12
→ 中项归一 1/√3:1:√2（残差<1e-30）；中项 d=3 配对计数=3=dim su(2)=**SU(2) 伴随表示**。
- **三相压缩**：扇区按非交换度 U(1)<SU(2)<SU(3) 与梯子按维数 2<3<4 **同向** ⟹ 若 Δ(Sp 4-范畴交换律
  偏差)单调，则单条原理自动给 U(1)↦d=2、SU(2)↦d=3、SU(3)↦d=4——**直接解探(A)裁决**。
- **三相现形**：待证原理 P（Δ 对非交换度/维数单调增）+ 候选 C₂（A_GR=√(2·配对计数)，闭式已给）
  + 候选 C₃（k_max=2^{N_active}=2³）。
- **诚实边界**：重构与压缩为已交货成果；P 未证（Δ 工作定义待落实为可判别结构量后证伪/证实）；
  C₂/C₃ 仍候选。推进入口 = 落实 Δ 定义 → 验 P 单调性 → 分成立/证伪两途。
衍生笔记：`sector_hierarchy_construction.md`（MUFPF-RN-ENDO-010）。

### 2026-09-17（十二）：Δ 现存定义挖出 + 交换偏差桥（RN-ENDO-010 v1.1）

挖出 Δ 现存工作定义并转译成可验结构量（`paper35` + `paperX_epsilon_delta_derivation.py`）：
- **Δ = spExchangeLaw 偏差**（4-范畴结构常数，paper35 定理 2.1，机器证明）；强度 ‖Δ‖_F²=r_cat·Δλ_min²≈6.01e-4
  （Δλ_min=(√3−1)/6 精确闭式，r_cat≈0.040404 Cl(1,7) MC）——**全局单标量**。
- **循环告警**：Δλ_min 已含 √3，直接用现存量推导 √3 为循环，须另建逐扇区 Δ。
- **交换偏差桥（非循环，核验通过，`delta_exchange_bridge_check.py`）**：交换偏差=反称部维数
  dimΛ²(V_d)=d(d-1)/2=N_pairs ⟹ λ=√(2dimΛ²)=√(d(d-1))。d=2,3,4 → dimΛ²=1,3,6 严格递增，
  λ 归一 1/√3:1:√2（残差<1e-30）。序 P 变可验：dimΛ² 单调 ⟹ Δ_i∝f(Λ²) 单调 ⟹ P 成立，不预设 √3。
- **静默平凡层排除**：d=1（全交换 dimΛ²=0）=静默层被框架原生排除 ⟹ U(1)(最交换活性扇区)→d=2。
- **未交货（真问题）**：逐扇区 Δ_i(Λ²) 的显示表达式（把 paper35 spExchangeLaw 偏差按扇区/维数解析），
  方能实测 d=2,3,4 单调性且独立于 √3。RN-ENDO-010 升 v1.1。

### 2026-09-17（十三）：深挖 spExchangeLaw——逐扇区 Δ 非单纯计算，需运输函子（RN-ENDO-010 v1.2）

读 paper35 定理 2.1：Δ=X.A·H−2β.h·Y.A·α'.h+H·Z.A，H=β.h·α'.h，对 X.A/Y.A/Z.A 各一次幂线性。两条结构性发现：
- **① paper35 三指标是空间层（anisotropy），非规范扇区**：X.A≠Y.A≠Z.A 表层刚度各向异性，且 GR 严格极限
  =X.A=Y.A=Z.A——映射到 U(1)/SU(2)/SU(3) 会与梯子 X≠Y≠Z（1/√3:1:√2）冲突。不同三指标，直接映射是混淆。
- **② 本质"交换"≠表示翻转**：spExchangeLaw 是范畴高阶态射复合交换律（部分交换子）；§8.3 τ 是表示翻转
  V⊗V 的对称/反称分裂（Λ²）。同名异义。表示层桥 λ=√(2dimΛ²) 严格成立，但未与 paper35 范畴 Δ 关联。
- **修正真问题**：per-sector Δ_i(Λ²) 非"解析 paper35 偏差"，而需**范畴→表示运输函子**
  𝒯:(spExchangeLaw 线性偏差, V_d)↦f(dimΛ²(V_d))（f 单调增 ⟹ P 成立）。该运输不存在——三相合一止于
  表示层的精确原因。RN-ENDO-010 升 v1.2（诚实登记，不伪称 per-sector Δ）。

### 2026-09-17（十四）：读规范一手论文收敛三相互一（RN-ENDO-010 v1.3）

用户提示转读规范一手 paper40/46，决定性收敛：
- **现行修正谱间隙比 = 1/√3:1:√2（SU(2) 特征值归一化，v0.29 修正）**；Lean dl_1=√(1/3) 落修正侧，
  证实 RN-ENDO-009 断点审计正确。κ 只依赖 Δλ₃/Δλ_min=√2（鲁棒）。
- **梯子 λ=√(d(d-1)), d=2,3,4 精确再导出 1/√3:1:√2**——§8.3 维数梯子不是红鲱鱼，获一手确认。
- **扇区索引=SU(2) 表示维数(2,3,4) ≅ n-旋转轴(1,2,3)（paper46 定理 9.1 函子等价）**；U(1)→最小确认
  （paper46"U(1) 拓扑强度最小"；其"α₁>α₂>α₃"为笔误）。
- **k_max=8=Cl(1,7) 底空间维数（paper32 机器证明）**——C₃ 第一性来源优于纯秩猜想。
- **残留开放**：① paper35 范畴 Δ→表示层运输 𝒯 仍缺失（三相合一能否闭环于 Δ 的真欠定）；
  ② 两处 √3（谱间隙比 vs 超荷嵌入 Y=(1/2√3)(H₃+√3H₄)）是否同源未查（更深 √3 起源）。
- **⚠️ paper40 L96 内部不一致**：正文仍写过期 √(2/3):1:√2，与自身 v0.29 修正矛盾，建议修订为 1/√3。
RN-ENDO-010 升 v1.3。

### 2026-09-17（十五）：修订 paper40 L96 + 判定两处 √3 不同源（RN-ENDO-010 v1.4）

- **paper40 定义 4.1 已修订**：√(2/3):1:√2 → √(1/3):1:√2 = 1/√3:1:√2，加修正史标注 + 三分量数值
  （Δλ₁=0.0704、Δλ₂=0.122、Δλ₃=0.1725）。其余 √(2/3) 均在 §8 修正史（保留）；Lean 已落修正侧；
  QCD 链只依赖 Δλ₃/Δλ_min=√2 不受影响。
- **两处 √3 不同源（关闭 ②）**：谱间隙比 1/√3 = √(d₁(d₁-1)/d₂(d₂-1)) = √2/√6 是 SU(2) 表示特征值之比；
  超荷 √3 出自 su(3) Gell-Mann/Cartan 归一化 λ₈ ∝ diag(1,1,-2)/√3，是绝对结构常数（非比值）。
  二者等式互相不能由共同假设推出；同处 Cl(1,7) 不足以证同源。电弱 sin²θ_W≈3/8 由二者独立共喂佐证。
- **残留开放收敛为单一真欠定 ①**：范畴 Δ→表示层运输 𝒯（统一猜想"单一根系统原理同时强制两 √3"并入 ①）。
RN-ENDO-010 升 v1.4。

### 2026-09-17（十六）：攻运输 𝒯——运输已存在但机制是 Casimir 非 Λ²（RN-ENDO-010 v1.5）

- **`CategoryRepBridge.lean` 已机器证明运输 𝒯**（零 sorry）：category geometry（G_GR=ad(G)(A)）
  → SU(2) 生成元 → Casimir C₂=ΣLᵢ² → 特征值 √{j(j+1)} → agEigenvalue=√{k(k+1)}/√{k_max(k_max+1)}。
  `agEigenvalue_is_casimir_ratio` 等定理闭环。故"从零构造运输"框架大体瓦解。
- **我的 §8.3"Λ²/维数梯子"与已证 Casimir 梯子数字相同、机制不同**：√{k(k+1)} k=1,2,3(=d-1)
  = √2,√6,√12 = 归一 1/√3:1:√2——数字逐项相等，但框架用的是 **SU(2) Casimir 特征值（平方和）**，
  不是我 §8.3 的表示翻转 τ 反称部 Λ²。`ExteriorFunctor.lean` 是 Z₂ 拓扑荷/环绕数（σ=n mod 2），
  **与 Λ² 无关**。故 §8.3/§8.5 的 Λ² 机制须诚实修正为非框架的巧合替代。
- **残留真欠定收窄**：CategoryRepBridge 的 SU(2)/Casimir 涌现来自 adjoint/对易结构（G_GR=ad(G)(A)），
  **非 spExchangeLaw**。唯一未闭环问题：paper35 范畴 spExchangeLaw 偏差 Δ 是否恰是 Casimir 涌现的来源
  （Δ↔Casimir 连接）。这是关闭于 Δ 的最后一步。
RN-ENDO-010 升 v1.5。

### 2026-09-17（十七）：Δ↔Casimir 连接机器证明——同源 + 被谱间隙钉住，残留收敛为单一 hNorm（RN-ENDO-010 v1.6）

读 `DeviationBound.lean`（spExchangeLaw 偏差机器实现）三点铁证：
- **同原语**：Δ 的代数内核=矩阵对易子（`commutator_trace_zero`、`commutator_diag_zero_of_diagonal`，
  范畴-几何桥 `delta2Cell_commutator_*`）；CategoryRepBridge 的 SU(2) 涌现 `ad(G)(A)=[G,A]` 同为对易子。
  §8.5"Δ 与 Casimir 独立输入"忧不复成立——同一原语两种体现。
- **定量连接（机器证明）**：`deviation_spectral_bound`：‖Δ‖² ≤ (4·spectralGap 8)²·‖β.h‖²·‖α'.h‖²，
  把 Casimir 梯子基序 spectralGap(=Δλ_min=agEigenvalue 基) 注入交换律结构。
- **透过单一 hNorm 注入**：`hNorm : 24‖S.A‖²≤(4·spectralGap 8)²`（Cl(1,7) 谱算子归一化），诚实标注为
  物理模型断言非定理。
- **残留输入收敛为单一 hNorm**：从三相合一追下的所有欠定（选 √3、扇区序、Λ² 机制、两处 √3、运输 𝒯、
  Δ↔Casimir）最终落到单一、载于 Lean 的 hNorm 归一化假说——内生第一性最后闸门。
RN-ENDO-010 升 v1.6。

### 2026-09-17（十八）：复核 Δ↔Casimir——§8.9"同源/被钉住/单一闸门"过度推伸（RN-ENDO-010 v1.7）

应复核独立重查 §8.9。查明：
- `CategoryRepBridge.lean` header import 仅 AInfinityAlgebra、SpectralDynamics，**无 DeviationBound/Δ**；
  L288 自陈链 = CategoryRepBridge → SU(2) Casimir → agEigenvalue → SpectralGap；L218 SU(2) 由
  ad(G)(A)=[J_i,J_j]=iε_ijk·J_k 直接涌现，**完全不经 Δ**。
- 实存**两条分离链**仅共用 spectralGap：Chain A（对易子→SU(2)→Casimir→agEigenvalue，不经 Δ）；
  Chain B（spExchangeLaw 偏差 Δ 被 (4·spectralGap 8)² 经 hNorm 界住）。
- §8.9 三处过度声明纠正：①"同源"→"同向"（仅语言同一，无结构推导）；②"被谱间隙钉住"→单边范数上界
  （数值相容非结构必然）；③"单一 hNorm 闸门"→**两个并列残留输入**（Chain A 的 ad(G)(A) 输入 + Chain B 的 hNorm）。
- 落回语言同一 vs 物理同一：Δ↔Casimir 仅建立语言同一 + 数值相容，**结构同一未成立**；统一是待完成的一步，
  非已完成前提。
RN-ENDO-010 升 v1.7。

### 2026-09-17（十九）：两链内生化终判——残留输入无内生衍生（RN-ENDO-010 v1.8）

按两链内生化方案逐条攻，均未能收口：
- **Chain A（n=2/Pauli 纯 stipulation）**：`CategoryRepBridge.lean` L57-96 `pauliSU2 {n}{hn:n=2}`
  把 n=2 作输入假设，显式构造 L_i=(1/2)σ_i 并验证对易；**无任何从 Δ/范畴推导"为何 n=2"之论证**，
  header 叙事 G_GR=ad(G)(A) 未入构造。此 n=2 钉死 Δλ₁/Δλ₂=√(1/3)——最深"选 √3"无脚手架。
- **Chain B（hNorm 纯 stipulation）**：`DeviationBound.lean` L436 `hNorm:24‖S.A‖²≤(4·spectralGap 8)²`；
  "24"=8(不等式链常数)×3(偏差项数)，非 Cl(1,7) 结构量；唯一有来源是 spectralGap 8 指数 8=k_max；
  "4·"与 ‖S.A‖≤√(2/3)·Δλ_min≈0.0996 均无规定，代码标"物理归一化断言"。
- **诚实终点**：两残留输入均为"结构层选定"，按不得妥协原则按"未闭合"处理，不做"必然不可达"断言；
  进一步须真正构造"范畴→n=2"或"范畴→hNorm"新机制，目前不存在。
RN-ENDO-010 升 v1.8。

### 2026-09-18（二十）：起点分层判定记档——工作起点=规范/表示层，范畴 Δ 支降级为远期 𝒯（本笔记 v1.2）

**任务背景**：用户质询重建起点——"从范畴 Δ 出发的是否成立？还是说要从规范场出发？""规范场根植于范畴层，只是不需要从 Δ 出发？"。前者经判读：**"从范畴 Δ 出发"范式成立（引力侧 paper54 L0→L6 全证）但凝聚态侧未闭合**；后者经判读：**"根植于范畴层"仅在对易子原语同一层成立、"不从 Δ 出发"是现状必然而非妥协**。据此对 §3 G1 / §4 边界落档（写在 §4，见上文"起点分层"）。

**判定（两半，不二选一）**：
- ① **范式成立的一半**：范畴 Δ 内生只产普适量（谱间隙比、Casimir 序列、无量纲指数、拓扑不变量）；引力侧 Δ→Einstein 已 Lean 全证，证明范式可达。
- ② **凝聚态数值/结构内源未闭合的一半**：§8.19 裁定 `16=dim_ℝℍ²` 为维数恒等/模分解巧合、非代数内源；Chain A 深处 `n=2` 被 `pauliSU2` 当输入假设（无任何从 Δ 推导"为何 n=2"）；Chain B `hNorm` 为纯 stipulation（"24"=8×3 非 Cl(1,7) 结构量）。`Δ↔Casimir` 只建立语言同一 + 数值相容，结构同一未成立。

**对重建路线的改判**（落 §4，非 §5 路线表）：
- 工作起点 = **规范/表示层**（谱公理 + 表示层：对易子→SU(2)→Casimir→agEigenvalue→spectralGap，不经 Δ，Lean 已证独立）——唯一有 Lean 证据、可落地的层面，全部比值级成果已在此闭合。
- 范畴 Δ 支 = **远期统一目标**——唯一未闭合步骤是"范畴→表示"运输函子 𝒯（§8.7#5 核心）；在 𝒯 落地前，数值内源问题不押在"从范畴 Δ 出发"上。
- 记档精炼公式：**同一根（对易子），两支（Δ 支 / 规范支），仅共享 spectralGap 标记，互不推导。**

**投诉关闭**：§1.1/§1.3 及 §3 G1 的"起点必须是范畴 Δ"表述已由 §4"起点分层"定号修正；§3.1 缺口清单 G1 起点标注（"每条推导链起点必须是范畴 Δ"）按工作起点=规范/表示层改判。建议后续 Phase 引用于 §5 时以 §4 起点分层为准。

### 2026-09-19：G5 遗留闭合——ε_eff 闭式 Lean 化（NoiseEffectiveEpsilon.lean）

**闭合对象**（§3 缺口清单 G5 的遗留部分，[G5 遗留注记]→已闭合）：paper14 §3.4 噪声范畴
$\mathbf{Noise}$ 的谱公理层修正公式 `ε_eff(ξ) = n_imp·[ℓ_B² + ξ²·θ(ξ²/(2ℓ_B²))]`、
`θ(t) = 1 − e^{−t}`、`ε_c^eff = ε_c^(0)/(1 + ξ/ℓ_B)²` 的 Lean 化。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/NoiseEffectiveEpsilon.lean`，
零 sorry、零 warning，`lake build` 3048 jobs 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| θ(0) = 0 | `theta_zero` |
| 退化值：ξ=0 ⟹ ε_eff = n_imp·ℓ_B²（＝短程情形点值） | `effEpsilon_zero` |
| 远程因子非负 0≤θ(t) / 严格上界 θ(t)<1 / 单调不减 | `theta_nonneg` / `theta_lt_one` / `theta_mono` |
| 远程主导分解 ε_eff = n_imp·ℓ_B² + n_imp·ξ²·θ（`ring`） | `effEpsilon_decompose` |
| 远程修正项非负（n_imp≥0, ξ²≥0, 0≤θ） | `effEpsilon_remote_correction_nonneg` |
| θ 处处连续 | `continuous_theta` |
| 退化极限：ξ→0 ⟹ ε_eff→n_imp·ℓ_B²（连续性） | `effEpsilon_tendsto_zero` |
| 临界阈值 ε_c^eff 对 ξ 单调递减（AntitoneOn ⩾0） | `effCriticalEpsilon_antitone` |

**API 要点**（roadmap §7.2 记档）：`Real.exp_le_exp` 是等价命题 `exp x≤exp y ↔ x≤y`
而非函数，须用 `.mpr` 方向；`sq_le_sq` 同为等价，分母平方单调以
`nlinarith [mul_nonneg _ (sub_nonneg.mpr _)]` 处理；`gcongr` 自动闭合分母正性与比较
子目标，bullet 须按实际剩余子目标数写。

**诚实边界**：无穷远精确渐近 `ε_eff ~ n_imp·ξ² (ξ→∞)` 依赖 e^{−t}→0 与 Fatou 两条
比较引理的再交织，本模块以"上界 + 单调"给出定性/定界判别（足以支持"远程更强无序"
与"ε_c^eff 单调下移"），精确渐近**登记开放**，不 axiomatize。

**同步**：paper14 升 **v1.7**（版本记录 + 文首形式化支撑清单 + §3.4 正文形式化指针）；
roadmap 新增 §七。G5 至此**全部闭合**（NoiseCategory 6 真证 + NoiseEffectiveEpsilon 11 定理）。

### 2026-09-19：G4 代数核心闭合——涡旋＝谱规范分支 + 拓扑荷守恒（GPVortex.lean）

**闭合对象**（§3 缺口清单 G4 的代数核心部分，命题 4.2/推论 4.2 的谱代数根源）：谱流
方程 $dA/dt=[G,A]$ 在幺正规范变换下的**规范协变**、规范分支**保全部迹幂**、以及由此
推出的**涡旋荷守恒**。真实涡旋拓扑荷 $n\in\mathbb{Z}$ 的严格 winding-number 定义与同伦
不变性仍须连续场论，**登记开放**（不动摇本闭合）。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/GPVortex.lean`，零 sorry、
零 warning，`lake build` 3188 jobs 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| 谱流幺正规范协变：幺正 $U$ 下规范分支 $(U^\dagger A_0 U,\, U^\dagger A_F U)$ 的谱流 = 原谱流的规范共轭（规范变换与谱流映射交换） | `spectralFlow_unitary_conj` |
| 规范分支保全部迹幂：$\mathrm{tr}\big((U^\dagger A U)^k\big)=\mathrm{tr}(A^k)$（经 `SpectralInvariant.trace_pow_similar` 实例化） | `vortex_trace_gaugeInvariant` |
| 涡旋荷守恒：规范分支谱流与原谱流每时刻 $t$ 的全迹幂全等（推论 4.2 $dn/dt=0$ 的有限维代数版本） | `vortex_charge_conservation` |

**API 要点**（roadmap §8.1 记档）：`NormedSpace.exp_conj` 需 `IsUnit` 前提 + `hVin`；
`(U*E0*U... )` 乘积整理用 `noncomm_ring`；`(−t)•A_F` 非定义等于 `−(t•A_F)`，须
`rw [neg_smul]` 统一。迹幂不变量经 `trace_pow_similar`（`SpectralInvariant`）**一介复用**，
无需重证。

**诚实边界**：闭合的是**谱代数根源**（规范分支保谱流结构 + 保迹幂/谱）；真实涡旋
拓扑荷 $n\in\mathbb{Z}$ 的严格 winding-number 定义（$U_n=e^{in\phi}$）与同伦不变性须连续
场论，**登记开放**。

**同步**：paper14 升 **v1.8**（版本记录 + 文首形式化支撑清单 + §4.2 层级标注段补记）；
roadmap 新增 §八。G4 代数核心至此**闭合**；G4 残余（GP-谱流等同的 PDE 层面、真实
winding 荷）属连续场论基础设施，暂不推进。

### 2026-09-19：G4 残余闭合——谱流的时间依赖守恒律（GPFlowTimeDep.lean）

**闭合对象**（GPFlow §3 开放登记第 1 项「时间依赖守恒律 $d/dt\,\mathrm{tr}(A(t)^k)=0$」）：
谱流方程 $dA/dt=[A_F,A]$ 的解 $A(t)=\mathrm{exp}(tA_F)\,A_0\,\mathrm{exp}(-tA_F)$ 满足
**比 $d/dt=0$ 更强的点式恒等**——$\mathrm{tr}(A(t)^k)=\mathrm{tr}(A_0^k)$ 对所有 $t$
成立，故函数 $t\mapsto\mathrm{tr}(A(t)^k)$ 为常值，导数处处为 $0$。这是推论 4.2
「涡旋拓扑荷守恒 $dn/dt=0$」的**逐时刻谱版本**：守恒沿解曲线逐点成立，无需微分。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/GPFlowTimeDep.lean`，零 sorry、
零 warning，`lake build MUFPFormalization.GPFlowTimeDep` 3188 jobs 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| exp 双侧逆：$\mathrm{exp}(tA)\mathrm{exp}(-tA)=1$ 且 $\mathrm{exp}(-tA)\mathrm{exp}(tA)=1$（矩阵非 DivisionRing，用 `Matrix.exp_add_of_commute` + `neg_smul` + `exp_zero`） | `exp_smul_mul_exp_neg_smul` / `exp_neg_smul_mul_exp_smul` |
| **谱流点式保迹幂（核心）**：$\mathrm{tr}(\mathrm{spectralFlow}\,A_0 A_F t^k)=\mathrm{tr}(A_0^k)$ 对所有 $t$（经 `SpectralInvariant.trace_pow_similar`，Newton 恒等式蕴含同谱） | `trace_pow_invariant_flow` |
| **谱特征多项式层**：$\mathrm{charpoly}(A(t))=\mathrm{charpoly}(A_0)$ 逐点恒定；谱流解即 $A_0$ 相似矩阵（exp 对打包为 $u\in M_n(\mathbb{C})^\times$，`Matrix.charpoly_units_conj` 直接闭合）——比迹幂守恒更强一层，直接是"谱沿解曲线恒定"的代数落点 | `spectralFlow_charpoly_eq` |
| 时间依赖守恒律（微分形式）：$d/dt\,\mathrm{tr}(A(t)^k)=0$（常值函数借 `hasDerivAt_const`） | `trace_pow_flow_conservation` |

**诚实边界**：闭合的是**守恒律本身**及**特征多项式沿解曲线逐点恒定**；**生成元级时间导数** $dA/dt=[A_F,A]$ 需
$\mathrm{exp}$ 的导数，此 mathlib 版本对 `NormedSpace.exp` 缺席 Fréchet/级数导数引理，
矩阵非 `DivisionRing` 亦阻断 `exp_neg` 路径——登记开放（基础设施缺口，不 axiomatize）。
特征多项式 → 特征值多重集（根多重数基础设施）、依赖时间的幺正规范势（$U^\dagger\dot U$）亦登记开放。

**同步**：paper14 升 **v1.9**（版本记录 + 文首形式化支撑清单 + §4.2 层级标注段补记）；
roadmap 新增 §九。G4 至此**全部闭合**——代数核心（涡旋规范分支 + 荷守恒）与时间
依赖守恒律均已 Lean 化，G2/G4 伴随的谱流线性代数层完成系联。

### 2026-09-19：G3 残余闭合——Berry 曲率规范不变性（BerryChern.lean §2.6）

**闭合对象**（BerryChern §3 开放登记第 5 项「规范不变性」）：本征矢态 $u$ 的
$U(1)$ 相位与基选取不影响 Berry 曲率，即曲率只依赖占据带谱投影 $P$ 而非
本征态基/相位。命题形式：对酉验证 $U^\dagger U=1$，规范变换
$(P,A,B)\mapsto(UPU^\dagger, UAU^\dagger, UBU^\dagger)$ 不改变曲率
$F(UPU^\dagger, UAU^\dagger, UBU^\dagger)=F(P,A,B)$。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.6，
零 sorry、零 warning，`lake build` 全库 6376 jobs 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| 酉共轭乘积整理：$(UAU^\dagger)(UBU^\dagger)=U(AB)U^\dagger$（用 $U^\dagger U=1$ 消去中间一对，`noncomm_ring` 展开） | `conj_mul_unitary` |
| 酉共轭迹不变：$\mathrm{Tr}(UXU^\dagger)=\mathrm{Tr}(X)$（迹循环性 `trace_mul_comm` + 结合律 + 单位消去） | `trace_conj_unitary` |
| **规范不变性（核心）**：$F(UPU^\dagger, UAU^\dagger, UBU^\dagger)=F(P,A,B)$（$rfl$ 展开曲率定义 → `hM` 差核酉化简 → `trace_conj_unitary` 剥离酉共轭） | `berryCurvature_unitary_conj` |
| 规范无关实值性：规范变换后曲率仍实值 $\mathrm{Im}\,F(UPU^\dagger,\cdot,\cdot)=0$（不变性归约 + `berryCurvature_im_eq_zero` 一行合成） | `berryCurvature_unitary_conj_im_eq_zero` |

**诚实边界**：闭合的是**曲率的酉共轭（稳定化）不变性代数核心**；**联络层面**
$u\mapsto e^{i\theta}u$ 的 $U(1)$ 局域规范、$F=dA$ 的微分形式恒等式仍属微分形式
基础设施（此 mathlib 版本缺口），登记开放。完整陈数理论（积分定义、整性 $C\in\mathbb{Z}$、
TKNN 线积分）此前已登记开放，不受影响。

**同步**：paper14 升 **v1.10**（版本记录 + 文首形式化支撑清单 + 顶部版本号）；
roadmap 新增 §十。G3 的 **规范不变性代数核心闭合**（对应 §8 第 21 行入口条目的
开放性说明改判）；曲率实值性（`berryCurvature_im_eq_zero`）、切向量约束代数层
（§2.5）、规范无关性（§2.6）三级构成陈数良定义的代数链条。

### 2026-09-19：G4 谱层补全——特征值多重集逐点恒定 + 行列式守恒（GPFlowTimeDep.lean §6）

**闭合对象**（GPFlowTimeDep §6 开放登记第 1 项「特征值（计重数）逐点恒定」）：
v1.9 已将特征多项式沿解曲线逐点恒定（`spectralFlow_charpoly_eq`）；本层用
`Polynomial.roots`（ℂ 代数闭域，`IsAlgClosed ℂ`）把恒等落到**谱集本身**——特征值
多重集逐点不变——并导出行列式（特征值乘积）守恒。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/GPFlowTimeDep.lean` §6，
零 sorry、零 warning，`lake build` 全库 6376 jobs、单模块 3460 jobs 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| 特征值多重集定义：$A.\mathrm{charpoly}.\mathrm{roots}$（非计算性，`Polynomial.roots`） | `spectrum_mulset` |
| **特征值多重集逐点恒定（核心）**：$\mathrm{multiset}\,A(t)=\mathrm{multiset}\,A_0$——由 `spectralFlow_charpoly_eq` + `congrArg Polynomial.roots`（`exact`，非战术）一行闭合 | `spectralFlow_roots_eq` |
| **行列式守恒（特征值乘积）**：$\det A(t)=\det A_0$——`Matrix.det_eq_prod_roots_charpoly`（ℂ 代数闭前置 `[IsAlgClosed ℂ]`）三步 `calc` | `spectralFlow_det_eq` |

**要点**：`congrArg` 是**项**非战术，`by` 中须 `exact congrArg f h`；
`det_eq_prod_roots_charpoly` 需显式应用矩阵参数 `(Matrix.det_eq_prod_roots_charpoly A)`；
`IsAlgClosed ℂ` 实例来自 `Mathlib.Analysis.Complex.Polynomial.Basic`（漏 import 则类型类
无法合成）。

**诚实边界**：闭合的是谱恒定的**多重集/标量落点**（特征值计重数 + 行列式），与 v1.9
迹幂同一（`trace_pow_invariant_flow`）为同一定义面的等价路（特征多项式 ⟷ 全部迹幂，
Newton 恒等式），此处显式落多重集而无需 Newton 分解。仍开放：生成元级时间导数
$dA/dt=[A_F,A]$（需 exp 导数）、依赖时间的幺正规范势、特征多项式 ⟹ 谱投影/谱隙的
更细谱结构（需谱测度/同伦投影基础设施）。

**同步**：paper14 升 **v1.11**（版本记录 + 文首形式化支撑清单 + 顶部版本号）；
roadmap 新增 §十一。G4 谱层在守恒律（瞬时+时间依赖+行列式）之外补全谱集/标量面。
G4 至此含：涡旋规范分支（v1.8）+ 时间依赖守恒律（v1.9）+ 特征值多重集/行列式（v1.11）。

### 2026-09-20：A2（Thm 17.7 本征值投影版）代数前提闭合 + A3（Sel ⊣ Diss）诚实边界登记（NoiseCategory.lean §17.5-A2）

**闭合对象（A2）**：Noise 谱流 §17.7 迹导数公式的本征值级落点。迹导数
`noise_spectral_flow_eq` 给出 $d/d\eta\,\mathrm{Tr}(A_\eta)=\mathrm{Tr}(\delta A)$，
但 Thm 17.7 投影版要求落到**本征值带重数**层面（谱投影 $P_\lambda$ 本征值级微扰）。
本层以 ℂ 代数闭的 `Polynomial.roots` 构造特征值多重集，并建立「谱一阶矩 = 特征值
多重集之和」，把迹导数与本征值之和的微扰耦合闭合，即 $\sum_\lambda d\lambda_\eta/d\eta
=\mathrm{Tr}(\delta A)$。

**登记（A3）**：`SelDissAdjunctionOpen` 经核查为**非普遍双射**——`selFunctor` 抽取
单一分量而 `dissFunctor` 产出多份拷贝，Hom 集势不等（普遍伴随双射不成立）。不造伪证，
登记为范畴层**启发式声明**，注明需在受限子类重构后才能升级为真定理。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/NoiseCategory.lean` §17.5-A2，
零 sorry、零 warning，`lake build` 全库通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| 特征值多重集（计重数）：$A$ 的复特征值带重数多重集约等于 $A.\mathrm{charpoly}.\mathrm{roots}$（非计算性，`Polynomial.roots`） | `noiseEigenMultiset` |
| **谱一阶矩 = 本征值之和（核心）**：$\mathrm{Tr}(A)=\sum_\lambda\lambda$（计重数）——`Matrix.trace_eq_sum_roots_charpoly`（ℂ 代数闭前置 `[IsAlgClosed ℂ]`）一行 | `noise_spectral_flow_roots_trace` |

**要点**：谱一阶矩与特征值和耦合（`noise_spectral_flow_roots_trace`）把迹导数公式落
到本征值层，构成 $P_\lambda$ 投影形式的**代数前提**；完整谱投影本征值级扰动仍需
谱测度/微扰论的连续谱选择（La 算子级，登记开放）。`IsAlgClosed ℂ` 实例来自
`Mathlib.Analysis.Complex.Polynomial.Basic`。

**诚实边界**：A2 闭合的是特征值多重集与迹的耦合（代数前提）；**谱投影 $P_\lambda$
的连续谱选择**（本征值级扰动公式的完整 $P_\lambda$ 形式）仍开放，需谱测度/微扰论。
A3 的 `SelDissAdjunctionOpen` 明确登记为**非普遍双射的启发式声明**，不视为已证定理。

**同步**：paper14 升 **v1.12**（版本记录 + 文首形式化支撑清单 + 顶部版本号）；
roadmap §6.2 第 3 项标注「A2 代数前提已闭合（2026-09-20，§17.5-A2）」，并追加
`SelDissAdjunctionOpen` 诚实边界说明。

### 2026-09-20：G3 陈数残余——被积函数 2-形式结构闭合（BerryChern.lean §2.7）

**闭合对象**（BerryChern §3 开放登记第 1 项「第一陈数积分定义
$C=(1/2\pi)\int_{T^2}F\,d^2k$」的**代数前提**）：环面积分需 MeasureTheory + 流形
积分（登记开放），但被积函数的**代数刻画**可在有限维原型内闭合——Berry 曲率
$F$ 必须是切向量 $(\partial_x,\partial_y)$ 上的**实值反对称双线性 2-形式**
（$d^2k=dk_x\wedge dk_y$ 反对称），且只依赖切向量的**带间分量**。至此 §2 实值性、
§2.5 切向量带间形态、§2.6 酉稳定化不变、§2.7 反对称/双线性/带内平移不贡献，
构成"陈数密度可作 2-形式积分"的完整代数链条。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.7，
零 sorry、零 warning，`lake build` 全库 6376 jobs、单模块 3048 jobs 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| 带内算子不贡献曲率迹核：$[P,X]=0\Rightarrow\mathrm{Tr}(P[X,B])=0$（迹循环性绕环 + $PX=XP$ 换序，9 步 calc） | `trace_comm_commutator_zero` |
| **反对称性（核心）**：$F(P,B,A)=-F(P,A,B)$（$F_{xy}=-F_{yx}$，2-形式积分 $d^2k=dk_x\wedge dk_y$ 的代数基础；`noncomm_ring` 证 $[B,A]=-[A,B]$） | `berryCurvature_antisymm` |
| 左线性：$F(P,A+X,B)=F(P,A,B)+F(P,X,B)$ | `berryCurvature_add_left` |
| 右线性：$F(P,A,B+X)=F(P,A,B)+F(P,A,X)$ | `berryCurvature_add_right` |
| **带内平移不贡献**：$[P,X]=0\Rightarrow F(P,A+X,B)=F(P,A,B)$（左线性拆分 + `trace_comm_commutator_zero`） | `berryCurvature_shift_commute` |
| 常数平移特例：$F(P,A+c\cdot 1,B)=F(P,A,B)$（$[P,c\cdot 1]=0$，标量阵与一切矩阵交换） | `berryCurvature_shift_const` |

**要点**：迹循环链 `trace_mul_comm` 每次绕环一步 + `← mul_assoc` 重结合，末步需
`rw [Matrix.trace_mul_comm, ← mul_assoc]` 两步（单步后留下 $(P\cdot B\cdot X).trace=
(P\cdot(B\cdot X)).trace$ 需再结合）；矩阵非交换，交换子反对称必须 `noncomm_ring`，
`ring` 失败（"no progress"）。

**诚实边界**：闭合的是被积函数的**代数结构**（实值 + 反对称 + 双线性 + 带内平移
不贡献），与 §2.5（切向量本身是带间的）互补构成"TKNN 只需带间矩阵元"论断的完整
形式；**环面积分本身**（MeasureTheory + 流形积分）、$F$ 连续性（⇐ $P$ 光滑）、
整性 $C\in\mathbb{Z}$（度理论）、TKNN（Kubo/泵浦）、绝热不变性（同伦）仍开放，
均需连续场论/同伦基础设施。

**同步**：paper14 升 **v1.13**（版本记录 + 文首形式化支撑清单 + 顶部版本号）；
roadmap 新增 §十二。G3 至此含：曲率实值性（§2）+ 切向量约束代数层（§2.5）+
规范不变性（§2.6）+ 2-形式结构（§2.7），陈数良定义的代数链条完整；残余开放项
收敛到连续场论/同伦层（积分、整性、TKNN、绝热不变性）。

### 2026-09-20：G3 陈数残余——整性与绝热不变性的代数种子闭合（BerryChern.lean §2.8）

**闭合对象**（BerryChern §3 开放登记第 2 项「整性定理 $C\in\mathbb{Z}$」与第 4 项
「陈数绝热不变性（paper14 命题 3.1）」的**代数种子**）：陈数整性的物理根源是
**占据带的整值占据数**——占据带谱投影 $P$ 的迹（占据数）等于其秩（占据带维数
/Landau 能级数），整数；绝热不变性的代数种子是谱投影沿**相似变换**（谱流/绝热
演化的代数形式，$P\mapsto UPU^{-1}$）保持幂等且秩不变——占据数沿绝热形变守恒。
完整整性（度理论/同伦提升）与同伦不变性（谱间隙不闭合的参数形变的同伦论证）
仍登记开放。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.8，
零 sorry、零 warning，`lake build` 全库通过、单模块 3049 jobs）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| **幂等阵迹 = 秩 ∈ ℤ（整性代数种子）**：$P^2=P\Rightarrow\mathrm{Tr}\,P=\mathrm{rank}\,P\in\mathbb{Z}$（占据数 = 占据带维数；$P.\mathrm{toLin}'$ 幂等 → `LinearMap.isProj_range_iff_isIdempotentElem`（mpr 方向）→ `IsProj.trace`（幂等线性映射迹 = 值域维数）→ `Matrix.trace_toLin'_eq`/`rank_eq_finrank_range_toLin` 桥接） | `trace_eq_rank_of_idempotent` |
| **共轭保持幂等**：$U^{-1}U=1\Rightarrow(UPU^{-1})^2=UPU^{-1}$（`noncomm_ring` 重排 + $U^{-1}U$ 消去中间对，只需单边可逆条件） | `idempotent_conj_inv` |
| **相似变换秩守恒（绝热不变性代数种子）**：$\mathrm{rank}(UPU^{-1})=\mathrm{rank}\,P$（幂等保持 `idempotent_conj_inv` + 相似迹不变 `SpectralInvariant.trace_pow_similar`（k=1）+ 秩=迹 `trace_eq_rank_of_idempotent`） | `rank_conj_inv_idempotent` |

**要点**：整性证明路径「幂等线性映射 → 到值域的投影 → 迹=值域维数 → 矩阵桥接」，
关键两步：`Matrix.rank_eq_finrank_range_toLin` 需先 `rw [Matrix.toLin_eq_toLin']`
把 `toLin` 显式转 `toLin'` 才能匹配（否则 hrank 无法闭合）；`IsProj.trace` 由
`LinearMap.isProj_range_iff_isIdempotentElem` 的 **mpr 方向**提供（`.2 hidem`，
`IsIdempotentElem.isProj_range` 别名不存在）。共轭保幂等的 calc 末步必须用
**显式参数** `rw [mul_assoc U P P, hPP]`（先结合内层 $P\cdot P$ 再应用 $P^2=P$）；
泛化 `mul_assoc` 会把最外层结合成 $U\cdot P\cdot(P\cdot U^{-1})$ 导致 $P\cdot P$
不出现、`hPP` 失配。`idempotent_conj_inv` 只需单边 $U^{-1}U=1$，未用的
$UU^{-1}=1$（hUU）按 linter 移除；`rank_conj_inv_idempotent` 保留全部可逆条件
（hUU 供 `trace_pow_similar` 的 hQP 使用）。

**诚实边界**：闭合的是**占据数的整性与相似守恒**（有限维代数层）；完整陈数
$C=(1/2\pi)\int F\,d^2k$ 的整性（度理论/同伦提升，如 Atiyah-Singer 指标特殊化）
与环面绝热演化（谱间隙不闭合的参数形变的同伦不变性）仍开放，需连续场论/同伦
基础设施。

**同步**：paper14 升 **v1.14**（版本记录 + 文首形式化支撑清单 + 顶部版本号）；
roadmap §6.2 第 4 项标注「整性/绝热不变性代数种子已闭合（2026-09-20，§2.8）」。
G3 至此含：曲率实值性（§2）+ 切向量约束代数层（§2.5）+ 规范不变性（§2.6）+
2-形式结构（§2.7）+ 整性/绝热不变性代数种子（§2.8）；残余开放项收敛到
连续场论/同伦层（积分、整性提升、TKNN、同伦不变性）。

### 2026-09-20：G3 同伦层首个基建模块——离散 S¹ 绕行的代数底胞闭合（BerryChern.lean §2.9）

**闭合对象**（BerryChern §3 开放登记第 1/2/4 项——环面积分、度理论整性、同伦
不变）在 §2.8 后明确收敛到连续场论/同伦层；开启同伦层前，先闭合其**离散 S¹
绕行的代数底胞**——占据带与空带的**互补守恒**。这是同伦层首个基建模块：陈数
扰动在占据/空带间转移（参数沿闭回绕行、能带交叉、占据数在带间跳变）时，任何
时刻占据数（秩）仍是整数且与空秩相加恒为总带数 $n$。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.9，
零 sorry、零 warning，`lake build` 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| **补投影仍幂等**：$(1-P)^2=1-P$（占据带投影 $P^2=P$ 时，空带/导带谱投影 $1-P$ 亦为幂等；`noncomm_ring` 展开 $(1-P)^2=1-P-P+P^2$ 后落入 $P^2=P$） | `complement_idempotent` |
| **占据数 + 空数 = 总带数 $n$（总荷守恒）**：$\mathrm{rank}\,P+\mathrm{rank}(1-P)=n\in\mathbb{Z}$（补投影幂等 + 幂等阵迹=秩 `trace_eq_rank_of_idempotent` + 矩阵迹线性 $\mathrm{Tr}(P+(1-P))=\mathrm{Tr}\,1=n$，经 `exact_mod_cast` 落回 $\mathbb{Z}$） | `rank_add_complement_idempotent` |
| **补秩**：$\mathrm{rank}(1-P)=n-\mathrm{rank}\,P$（加和形式先 `rw [add_comm]` 换序再 `Nat.eq_sub_of_add_eq` 直接推出） | `complement_rank` |

**要点**：三条证明**无需子空间直和/秩-零度基础设施**，只复用 §2.8 的
`trace_eq_rank_of_idempotent`（幂等阵迹=秩）+ 矩阵迹的线性平凡
$\mathrm{Tr}(P+(1-P))=\mathrm{Tr}\,1=n$。`complement_rank` 中
`Nat.eq_sub_of_add_eq` 期望 $a+b=c$ 形式而定理给出 $P.rank+(1-P).rank=n$，
须先 `rw [add_comm] at hadd` 交换加项。

**与同伦层的关系**：本层给出离散绕行的**总荷守恒**与**整值占据数**的代数细胞；
完整**连续 S¹/环面**绕行的陈数积分、度理论整性（同秩投影酉等价 → $K_0(\mathbb{C})\cong\mathbb{Z}$ → 陈指数，新增开放登记 §3 #7）与同伦不变性仍登记开放，
属后续同伦层基建。

**同步**：BerryChern §3 开放登记新增第 7 项「同秩投影酉等价（$K_0=\mathbb{Z}$ 度理论
整性核心）」并在该项标注「离散 S¹ 代数底胞已闭合（2026-09-20，§2.9）」；已闭合
清单追加 §2.9 三条定理。paper14 升 **v1.15**（版本记录 + 文首形式化支撑清单 +
顶部版本号）；roadmap 新增 §十四「同伦层首个基建模块」。

### 2026-09-20：G3 连续 S¹ 环绕数孢子 + 环面陈数积分承载形式闭合（BerryChern.lean §2.10）

**背景**：§2.9 闭合离散 S¹ 绕行的代数底胞（总荷守恒/整值占据数）后，跨入
**连续积分/度理论层**。陈数整性 $C\in\mathbb{Z}$ 的物理根源之一是**环绕数取整值**
（恒等映射 $S^1\to S^1$ 的度 = 1）。mathlib 提供 `CircleIntegral`（单参数环路
积分 $\oint_{|z-c|=R}$，含核心引理 `circleIntegral.integral_sub_center_inv`：
$(z-w)^{-1}$ 当 $|w-c|<R$ 时积分为 $2\pi i$）与 `TorusIntegral`（多参数环面积分
$\iint_{T^2}$）基础设施，故连续层最小孢子可在真证下闭合。

**闭合对象**（BerryChern §3 开放登记第 1 项——第一陈数积分定义的连续层底座）；
本层闭合**连续 S¹ 恒等映射的度/环绕数 = 1 ∈ ℤ**（积分/度理论层首块）。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.10，
定义层 `chernIntegralTorus` 标记 `noncomputable`——因 `torusIntegral` 非计算；
零 sorry、零 warning，`lake build` 通过）：

| 判别性命题 | Lean 定理/定义 |
|:-----------|:----------|
| **单位圆留数孢子**：$\oint_{|z|=1} z^{-1}dz = 2\pi i$（`circleIntegral.integral_sub_center_inv`，中心 0、半径 1，$(z-0)^{-1}=z^{-1}$） | `unitCircle_integral_inv` |
| **归一化环绕数 = 1 ∈ ℤ**：$(2\pi i)^{-1}\oint z^{-1}dz = 1$（留数孢子 + `inv_mul_cancel₀`，归一化因子 $2\pi i\neq 0$ 由 `mul_ne_zero` 组合 $2,\pi,\mathrm{i}$ 三者非零） | `unitCircle_windingNumber_eq_one` |
| **环面陈数被积积分形式**（定义留档，`torusIntegral` 双参数）：$\iint_{T^2=\{|z_i|=1\}} F\,d^2z$（ℂ² 参数 $\theta\in[0,2\pi]^2$） | `noncomputable def chernIntegralTorus` |

**要点**：`unitCircle_windingNumber_eq_one` 是陈数整性 $C\in\mathbb{Z}$ 在连续层的第一块
真证基石——度理论整值 $=1$ 的最简实例（恒等映射 $S^1\to S^1$ 的拓扑度），连接离散
§2.9（总荷守恒）与环面整性。`chernIntegralTorus` 提供 §3 #1 的积分承载形式，但环面上
$F$ 的可积性/光滑性（⇐ P 光滑）与完整归一化陈数仍开放。

**诚实边界**：闭合的是**连续 S¹ 恒等映射的度/环绕数 = 1 ∈ ℤ**；环面 $T^2$ 上的第一陈数
$C=(1/2\pi)\int F\,d^2k$ 的**完整整性**（同秩投影酉等价 → $K_0(\mathbb{C})\cong\mathbb{Z}$ → 陈指数，
§3 #7）与 TKNN 场论形式仍登记开放，属后续同伦层/度理论基建。

**同步**：BerryChern §3 开放登记第 1 项标注「连续 S¹ 环绕数孢子已闭合（2026-09-20，§2.10）」
并录入 `chernIntegralTorus` 承载形式；已闭合清单追加 §2.10 三条定理/定义。paper14 升 **v1.16**
（版本记录 + 文首形式化支撑清单 + 顶部版本号）；roadmap 新增 §十五「同伦层连续 S¹ 环绕数孢子与环面积分承载形式」。

### 2026-09-20：G3 同秩投影的 K₀ 迹同态种子闭合（BerryChern.lean §2.11）

**背景**：§3 #7「同秩投影酉等价（K₀ = ℤ 度理论整性核心）」的完整论证需完整酉群
U(n)/同伦与 K₀ 表示论（等距等价、子空间直和）等大型基建。按项目纪律**只闭合真实
可达内容、不作伪证**，完整酉等价保持开放登记。但 K₀(ℂ)≅ℤ 的**秩定类性质**有一块
完全在现有代数工具内的真实种子：**迹同态**——K₀ 到 ℤ 的显式同构由 $\mathrm{Tr}$
（$K_0(\mathbb{C})\ni[\mathbb{C}^r]\mapsto r\in\mathbb{Z}$）实现。

**闭合对象**（BerryChern §3 开放登记第 7 项的迹特征/互补类对称）；本层闭合
「同秩幂等投影必然同迹 ∈ ℤ」与「同秩投影的补投影亦同秩」。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.11，
零 sorry、零 warning，`lake build` 通过）：

| 判别性命题 | Lean 定理 |
|:-----------|:----------|
| **同秩幂等投影迹类一致**：$\mathrm{rank}\,P=\mathrm{rank}\,Q\Rightarrow\mathrm{Tr}\,P=\mathrm{Tr}\,Q\in\mathbb{Z}$（两边各自 `trace_eq_rank_of_idempotent` + `congrArg` 转换） | `trace_eq_of_rank_eq_idempotent` |
| **同秩投影互补类对称**：$\mathrm{rank}\,P=\mathrm{rank}\,Q\Rightarrow\mathrm{rank}(1-P)=\mathrm{rank}(1-Q)$（两侧各自 `complement_rank` + `congrArg` 传递） | `complement_rank_eq_of_rank_eq` |

**要点**：两条定理是「秩唯一决定 K₀ 类」的**迹特征**与**占/空互补类对称**在有限维
矩阵层的代数细胞：占据带投影的迹（占据数）只由秩决定、与具体谱投影无关；同秩投影
的空带"空数"亦对称确定。衔接 §2.8（迹=秩）与 §2.9（补秩互补）。

**诚实边界**：闭合的是同秩 ⇒ 同迹（秩决定迹类）与同秩 ⇒ 补同秩的**类一致性**种子；
真正的**酉等价构造**（∃ 酉 U，Q=U·P·U†）与**相似共轭构造**（∃ 可逆 S，Q=S·P·S⁻¹）
在连续 S¹/环面上仍登记开放（§3 #7），需完整等距/酉群/K₀ 基建。

**同步**：BerryChern §3 开放登记第 7 项标注「迹类一致/互补类对称已闭合（2026-09-20，§2.11）」；
已闭合清单追加 §2.11 两条定理。paper14 升 **v1.17**（版本记录 + 文首形式化支撑清单 +
顶部版本号）；roadmap 新增 §十六「同秩投影的 K₀ 迹同态种子」。

### 2026-09-20：G3 一维退化环面环绕数孢子闭合（BerryChern.lean §2.12）

**背景**：§3 #1 的环面积分定义层有了 §2.10 的 `chernIntegralTorus`（双参数承载）。
将 §2.10 的单位圆环绕数孢子（$\oint_{|z|=1}z^{-1}dz=2\pi i$ → 整值 1 ∈ ℤ）推广到
环面，mathlib 的 `torusIntegral_dim1` 证得**一维环面积分 = 圆周积分**（单参数环面
与圆周 $C(c_0,R_0)$ 等价），故最真实可达的第一块是**一维退化环面**：环面 $T^2$ 在
$n=1$（单参数）时的切面恰为圆周 $S^1$，§2.10 的留数孢子可直接继承到环面。

**闭合对象**（BerryChern §3 开放登记第 1 项的环面绕行整值孢子——$T^1$ 退化面）；
本层闭合**一维退化环面的环绕数整值**。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.12，
零 sorry、零 warning，`lake build` 通过；实现过程修复一处叙述层 bug：`∯ z in T(...),`
已绑定 `z`，不得再写内层 `fun z : Fin 1 → ℂ => ...`，否则被积值域退化为函数
类型导致 `NormedAddCommGroup ((Fin 1 → ℂ) → ℂ)` 合成失败——改用绑定变量 `(z 0)⁻¹`）：

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:----------|
| **一维退化环面留数孢子**：$1$-参数环面（中心 0、半径 1）被积 $1/z_0$ 的积分 = 单位圆留数 $2\pi i$ | `torusIntegral_dim1_winding` | `torusIntegral_dim1` 一维环面 = 圆周积分 + `unitCircle_integral_inv`（§2.10） |
| **一维退化环面归一化环绕数 = 1 ∈ ℤ** | `torusIntegral_dim1_windingNumber_eq_one` | 退化种子 + `inv_mul_cancel₀`（归一化因子 $2\pi i\neq 0$） |

**要点**：这是 §2.10 环绕数整值向**环面**转移的第一块真证基石——环面在一维
退化的切面（圆周 $S^1$）上恒等映射的度/环绕数仍取整值 1，为二维环面整性陈数
提供一维退化边界条件。

**诚实边界**：闭合的是**一维退化环面**的环绕数整值（$T^1$ 侧）；二维 $T^2$ 被积
$F$ 的完整归一化陈数与整性（§3 #1）仍登记开放，需完整等距/度理论基建与 $F$ 的
可积性（⇐ $P$ 光滑）。

**同步**：BerryChern §3 开放登记第 1 项标注「一维退化环面环绕数孢子已闭合
（2026-09-20，§2.12）」；已闭合清单追加 §2.12 两条定理。paper14 升 **v1.18**
（版本记录 + 文首形式化支撑清单 + 顶部版本号）；roadmap 新增 §十七「同伦层
一维退化环面环绕数孢子」。

### 2026-09-20：G3 二维环面双留数孢子闭合（BerryChern.lean §2.13）

在 BerryChern.lean 新增 \`torusIntegral_dim2_double_inv\`（\`torusIntegral\` 定义展开，
参数立方 Jacobi 因子 $\prod_i e^{\theta_i i}$ 与被积倒数消约成常数 $-1$，立方体积
$(2\pi)^2$，$\iint_{T^2}z_0^{-1}z_1^{-1}d^2z=(2\pi i)^2$）与
\`torusIntegral_dim2_windingNumber_eq_one\`（$(2\pi i)^{-2}$ 归一化 $=1\in\mathbb{Z}$）。
诚实边界：闭合双极点被积 $z_0^{-1}z_1^{-1}$ 的留数环值；完整 $T^2$ 上一般被积陈数密度
$F$ 的整性仍开放。所有 \`lake build\` 通过、零 sorry。

### 2026-09-20（后续）：G3 同秩投影酉等价的线性共轭支柱闭合（BerryChern.lean §2.14）

在 BerryChern.lean 新增 §2.14，为 §3 #7「同秩投影酉等价」提供**线性共轭支柱**：
（1）**自伴幂等正交分解** \`selfAdjoint_idempotent_ker_eq_orthogonal\`——自伴幂等
投影满足 $\ker=(\operatorname{range})^\perp$（\`IsSymmetric.orthogonal_range\`），确立
「自伴幂等 ⟺ 正交投影」，是酉等价 K₀ 稳定化的酉前提；（2）**同秩幂等投影相似共轭构造**
\`similar_conj_projections_of_eq_finrank\`——任意两个同秩幂等投影 P、Q 相似
$\exists\,S:E\simeq_\mathbb{C}E,\ S\circ P=Q\circ S$：幂等分解 \`IsIdempotentElem.isCompl\`
拆像/核直和 + \`prodEquivOfIsCompl\` 空间等价，经 finrank 加性（\`Module.finrank_prod\`）
析出核同维，\`LinearEquiv.ofFinrankEq\` 分块线性等价 → \`LinearEquiv.prod\` 合成显式
可逆 S，辅以 \`idempotent_apply_of_mem_range\`/\`_mem_ker\` 对角化验证——「秩唯一决定
相似类」的线性共轭闭合。
诚实边界（随登）：闭合的是**相似共轭**（可逆线性 S）；**酉（等距）强化**——把 S 升级为
保内积的 \`LinearIsometryEquiv\`（$Q=U\cdot P\cdot U^\dagger$，$U^\dagger=U^{-1}$）——
需「同维子空间间等距等价（紧致自伴对角化）+ 正交直和合成」基建，登记开放；环面上完整
第一陈数整性另需连续场论/度理论基建。所有 \`lake build\` 通过、零 sorry。

### 2026-09-20（后续）：G3 同秩投影酉等价的酉（等距）强化闭合（BerryChern.lean §2.14）

**背景**：§2.14 已闭合相似共轭（可逆线性 S）。本条目把 S 升级为**保内积酉**（等距
等价 \`LinearIsometryEquiv\`），闭合 §3 #7「完整酉等价 $\exists\,U:\,Q=U\cdot P\cdot U^\dagger$」
在有限维内积层的**代数 + 等距层**。

**交付**（\`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean\` §2.14，
零 sorry，\`lake build\` 通过）：

| 名称 | 主张 | 基建 |
|------|------|------|
| \`exists_isometry_of_eq_finrank\`（引理 A） | $\operatorname{range}P\simeq_{\mathbb C}\operatorname{range}Q$（同维子空间间等距等价） | \`stdOrthonormalBasis\` + \`Equiv.cast\` + \`OrthonormalBasis.equiv\` |
| \`linearIsometryEquiv_of_submodule\`（引理 B） | $S\to T$ 等距延伸为 $E\simeq_{\mathbb C}E$ | \`LinearIsometry.extend\` + \`toLinearIsometryEquiv\` |
| \`linearIsometryEquiv_of_submodule_apply\`（作用） | $U|_{S}=e$ | \`LinearIsometry.extend_apply\` |
| \`linearIsometryEquiv_of_submodule_mem_orthogonal\`（引理 C） | $U(S^\perp)\subseteq T^\perp$ | 等距保内积 + e 满射拉回 + \`mem_orthogonal'\` |
| \`same_rank_selfAdjoint_idempotent_unitary_conj\`（主定理） | $\operatorname{rank}P=\operatorname{rank}Q\Rightarrow\exists$ 酉 $U:E\simeq_{\mathbb C}E,\ Q\circ U=U\circ P$ | \`selfAdjoint_idempotent_ker_eq_orthogonal\`（$\ker=(\operatorname{range})^\perp$）+ 引理 A/B/C，正交直和 $E=\operatorname{range}P\oplus\ker P$ 上逐段验证（P 在 range 恒等、ker 为零，\`idempotent_apply_of_mem_range\`/\`_mem_ker\`） |

**实现要点**：主定理用 \`prodEquivOfIsCompl\` 正交直和系数化并 \`rcases eP.surjective\`
展开任意 $x$，引理 A/C 分别落定 range/核分量（$U(a)=e a$、$U(b)\in T^\perp=\ker Q$），
逐段验证 $Q\circ U=U\circ P$ 经 \`LinearIsometryEquiv.inner_map_map\` 与幂等对角化闭合。

**修复的一处编译错误**：相似共轭构造中 \`isoR.prod isoK\` 的 \`.prod\` 被 dot-notation 解析为
\`LinearMap.prod\`（产出**线性映射**而非线性等价），导致合成类型不匹配；改将 S 构造成
LinearEquiv 复合 \`eP.symm.trans ((isoR.prodCongr isoK).trans eQ)\`（乘积用 \`LinearEquiv.prodCongr\`），
\`hSa\`/\`hSb\` 用 \`change\` + \`simp [eP,eQ,LinearEquiv.prodCongr_apply,coe_prodEquivOfIsCompl']\`
展开闭合，消除 linter 警告。

**诚实边界（随登）**：有限维层酉等价（显式 \`LinearIsometryEquiv\` 酉构造）已闭合；
完整 $K_0(\mathbb{C})\cong\mathbb{Z}$（生成/自由交换群结构、$U(n)$ 酉群/同伦类与秩一一对应）
与环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升、§3 #4 绝热不变性）仍需完整
连续场论/度理论基建，登记开放。

**同步**：BerryChern §3 开放登记第 7 项将「诚实边界（随登）」中「酉强化登记开放」更新为
「有限维层酉等价已闭合（§2.14）」，已闭合清单追加 §2.14 引理A/B/C+主定理；paper14 升 **v1.21**
（版本行 + 文首形式化支撑清单 + 变更日志 v1.21 行）。

### 2026-09-20（后续）：G3 K₀ 秩映射的直和加性种子闭合（BerryChern.lean §2.15）

**背景**：§2.14 闭合「秩唯一决定酉等价类」（`same_rank_selfAdjoint_idempotent_unitary_conj`），
给出 $K_0(\mathbb{C})\cong\mathbb{Z}$ 秩映射的**分类半边**。K₀ 是加法幺半/群，其加法结构沿直和
相加；本轮把秩映射提升到**直和加性**（$\operatorname{rank}(P\oplus Q)=\operatorname{rank}P
+\operatorname{rank}Q$），为 $K_0(\mathbb{C})\cong\mathbb{Z}$ 的**群同态**提供加法结构种子。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.15，
零 sorry、零 warning，`lake build` 通过）：

| 名称 | 主张 | 基建 |
|------|------|------|
| `prodSubmoduleLinearEquiv` | 子空间乘积 `Submodule.prod S T` 线性等价于类型级乘积 `S × T` | `Submodule.mem_prod` 双向判定 + 逐分量线性验证 + `ext <;> rfl` |
| `directSum_idempotent` | 幂等 $P,Q$ 的直和 `P.prodMap Q`（块对角）仍幂等 | `LinearMap.prodMap_mul`（直和乘法 = 分量乘法） |
| `directSum_rank_add` | $\operatorname{rank}(P\oplus Q)=\operatorname{rank}P+\operatorname{rank}Q$ | `LinearMap.range_prodMap` + `prodSubmoduleLinearEquiv`（其 `finrank_eq` 收紧）+ `Module.finrank_prod` |

**实现要点**：`directSum_rank_add` 是三层 `calc` 链条——`rw [LinearMap.range_prodMap]` 把直和像识别
为分量像之子空间乘积；经 `prodSubmoduleLinearEquiv` 的 `finrank_eq` 把子空间乘积的 `Module.finrank`
转写到类型级乘积（收紧点：Submodule.prod 维度在 mathlib 中非预结算的"分量之和"，需显式线性等价
桥接）；`Module.finrank_prod` 结算类型级乘积加性。纯代数变量与内积空间变量分 section 隔离，
避免作用域冲突。

**诚实边界（随登）**：闭合的是**秩的加法属性**（幂等直和仍幂等 + 秩沿直和相加），而非
$K_0(\mathbb{C})\cong\mathbb{Z}$ 完整幺半同构（Grothendieck 群构造/自由交换群）、$U(n)$ 酉群/
同伦类与秩一一对应，及环面上陈数密度 $F$ 的连续场论/度理论整性——后者仍需完整连续场论/度理论
基建，登记开放。

**同步**：BerryChern §3 开放登记第 7 项标注「K₀ 秩映射直和加性种子已闭合（§2.15）」并描述其在
$K_0(\mathbb{C})\cong\mathbb{Z}$ 群同态中的作用；`sorry_closure_roadmap.md` 追加 §二十一；paper14
升 **v1.23**（版本行 + 文首形式化支撑清单 + 变更日志 v1.23 行）。

### 2026-09-22：G3 K₀ 生成/自由交换群结构的基底闭合（BerryChern.lean §2.16）

**背景**：§2.14 闭合「秩 ⇔ 酉类」逐对显式双射（`same_rank_iff_unitary_conj`），§2.15 闭合直和
加性（`directSum_rank_add`）。本轮把连接目标落实为 **K₀(ℂ)≅ℤ 的生成/自由交换群结构基底**：
自由交换群在**单个生成元**（占据带类别 `PUnit`）上同构于 ℤ。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.16，
零 sorry、零 warning，`lake build` 通过）：

| 名称 | 主张 | 基建 |
|------|------|------|
| `single_generator_freeAbelian_iso_int` | $\operatorname{FreeAbelianGroup}(\mathrm{PUnit})\cong\mathbb{Z}$（单生成元自由交换群 ≃ ℤ） | mathlib `FreeAbelianGroup.uniqueEquiv`（`lift fun _ ↦ 1`） |
| `rank_signature_lift` | 任意占据带生成元 ↦ 整数唯一扩展为群同态：`(Fin r → ℤ) → FreeAbelianGroup (Fin r) →+ ℤ` | `FreeAbelianGroup.lift` 泛性质 |
| `rank_signature_single_eq` | 单生成元秩签名取 $1\in\mathbb{Z}$ | `rw` + `rfl` |
| `single_signature_unique` | 签名唯一性：`(PUnit → ℤ) ≃ FreeAbelianGroup (PUnit) →+ ℤ` | `FreeAbelianGroup.lift` 泛性质 |

**实现要点**：`FreeAbelianGroup.uniqueEquiv T`（`T` 满足 `Unique`）把单生成元自由交换群同构于
$\mathbb{Z}$，正向 `lift fun _ ↦ 1`（生成元 ↦ 1）、反向 `n • of default`——单生成元签名取 $1$
由 `uniqueEquiv` 定义展开（`rw [single_generator_freeAbelian_iso_int]; rfl`）闭合。纯代数、不依赖
Grothendieck 商构造。

**诚实边界（随登）**：闭合的是**纯代数自由交换群层**（单生成元 ≃ ℤ + 秩签名 lift 泛性质）；
把同秩酉类的**实际商幺半群**形成 + **Grothendieck 化**（split-exact 关系商）+ $U(n)$ 酉群/
同伦类与秩一一对应，以实现完整 K₀(ℂ)≅ℤ 的**群结构同构**，及环面上陈数密度 $F$ 的连续场论/
度理论整性——仍需完整商/群论/同伦/连续场论基建，登记开放。

**同步**：BerryChern §3 开放登记第 7 项标注「K₀ 生成/自由交换群结构基底已闭合（§2.16）」并追加
已闭合清单；`sorry_closure_roadmap.md` 追加 §二十二；paper14 升 **v1.24**（版本行 + 文首形式化
支撑清单 + 变更日志 v1.24 行）。

### 2026-09-23：G3 同秩酉类的商幺半群载体闭合（BerryChern.lean §2.17）

**背景**：§2.16 闭合生成/自由交换群基底（单生成元 ≃ ℤ），其诚实边界把「把同秩酉类的**实际商
幺半群**形成」列为开放。本轮落实该**商载体构建**：把同秩自伴幂等（正交）投影的**酉等价形式化
为 `Setoid`**，构造**商类型**并把**秩映射下降为商上的良定义完全不变量**——完整 K₀(ℂ)≅ℤ
（Grothendieck 化）的第一块基石：酉类=秩的商对象存在且秩是其良定义分类函数。

**交付**（`formal_proof/MUFPFormalization/src/MUFPFormalization/BerryChern.lean` §2.17，
零 sorry、零 warning，`lake build` 全库通过）：

| 名称 | 主张 | 基建 |
|------|------|------|
| `SelfAdjointIdemProj E` | 自伴幂等（正交）投影子类型 `${P : E →ₗ[ℂ] E // IsIdempotentElem P ∧ P.IsSymmetric}` | 正交投影的代数特征 |
| `ProjUnitaryRel P Q` | 酉等价关系 `∃ U : E ≃ₗᵢ E, Q ∘ₗ U = U ∘ₗ P`（Q=U·P·U†，U†=U⁻¹） | 保内积酉算子 |
| `projUnitaryRel_refl/symm/trans` | 反身/对称/传递（U=1 / U⁻¹ / U₁.trans U₂） | `LinearIsometryEquiv` 等距性质 |
| `projUnitarySetoid E` | 酉等价为 `Setoid`（等价关系）⟹ 可作商 | 上三条合成 `iseqv` |
| `rank_well_defined_on_quotient` | 同酉类的投影同秩（完全不变量） | `finrank_eq_of_unitary_conj`（§2.14） |
| `quotientRank` | 商类型上秩函数 `Quotient (...) → ℕ` | `Quotient.lift` + 上条良定义 |

**实现要点**：酉等价关系用保内积酉算子 $U\in E\simeq_\mathrm{LI}E$ 共轭 $Q=U\circ P\circ U^\dagger$
定义；反身取恒等、对称取 $U^{-1}$（`symm_apply_apply` 拼接）、传递取 `U₁.trans U₂` 复合
（先 U₁ 后 U₂，`simp` 展开 `coe_trans` 验证）；三个等价性引理都在纯
`[NormedAddCommGroup E][InnerProductSpace ℂ E]` 假设下成立。`rank_well_defined_on_quotient`
直接复用 §2.14 `finrank_eq_of_unitary_conj`，**不依赖**投影幂等/自伴/有限维假设，确保其在商构造
中的普适性；`quotientRank` 加 `[FiniteDimensional ℂ E]`，经 `Quotient.lift` 把秩良定义下降
为商上的完全不变量分类器。

**诚实边界（随登）**：闭合的是**商载体**（等价关系三条 + 商类型存在 + 秩良定义完全不变量）；
在商上定义**加法**（跨空间直和 P⊕Q 的商良定性）并给商赋 `AddCommMonoid`/`AddGroup` 结构、
**Grothendieck 化**（split-exact 关系商，把可加幺半群对称化为群）+ $U(n)$ 酉群/同伦类与秩
一一对应，以实现完整 K₀(ℂ)≅ℤ 的**群结构同构**，及环面上陈数密度 $F$ 的连续场论/度理论整性
——仍需完整商加法/群论/同伦/连续场论基建，登记开放。

**同步**：BerryChern §3 开放登记第 7 项标注「同秩酉类的商幺半群载体已闭合（§2.17）」并追加
已闭合清单；`sorry_closure_roadmap.md` 追加 §二十三；paper14 升 **v1.25**（版本行 + 文首形式化
支撑清单 + 变更日志 v1.25 行）。

### 2026-09-23（后续）：G3 商秩的单射完全不变量强化闭合（BerryChern.lean §2.18）

**背景**：§2.17 闭合商载体后，把「秩唯一决定酉等价类」从**逐对显式双射**（§2.14
`same_rank_iff_unitary_conj`）升级为**函数级完全不变量**：`quotientRank` 在商上**单射**（不同
酉类必有不同秩，商上无"同秩异类"），合并良定义为**可扩性/等值判定**（商相等 ⟺ 同秩），并给出
**值域上界**（秩 ≤ dim E）。这是「酉类=秩」在商层的完全锁定，是 Grothendieck 化的**分类器落点**。

**交付**（`BerryChern.lean` §2.18，零 sorry、全库通过）：`quotientRank_injective`（商秩单射，
`same_rank_iff_unitary_conj` 前向 + `Quotient.sound`）、`quotientRank_ext`（同秩 ⟺ 商相等，
良定义 + 单射合并）、`quotientRank_le_dim`（值域上界，`Submodule.finrank_le`）。

**诚实边界（随登）**：闭合的是**商秩的完全不变量强化**（单射 + 可扩性 + 值域界）；在商上定义
**加法**（跨空间直和 P⊕Q 的商良定性）+ 商构成 **AddCommMonoid/Group** + 完整 **Grothendieck 化**
（split-exact 关系商）+ $U(n)$ 酉群/同伦类与秩一一对应，登记开放。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.18；`sorry_closure_roadmap.md` 追加
§二十四；paper14 升 **v1.26**（版本行 + 文首形式化支撑清单 + 变更日志 v1.26 行）。

### 2026-09-23（后续）：G3 商加法的载体——跨空间直和 P⊕Q 的商良定性闭合（BerryChern.lean §2.19）

**背景**：§2.18 把商秩锁定为单射完全不变量后，落实商加法的**对象层载体与商线性**：在商上定义
加法 $[P]\oplus[Q]:=[P\oplus Q]$ 及其**商良定性**（$P\sim P'∧Q\sim Q'⟹P\oplus Q\sim P'\oplus Q'$）。
对象载体取两空间 $E,F$ 的 **L²-乘积** `WithLp 2 (E×F)`（mathlib 对原始二元乘积 $E\times F$ 不自动
捆绑内积，需显式转移到 `WithLp 2 (E×F)`，其上注册 `InnerProductSpace`）；在 $E\times F$ 上定义
块对角投影 $P\oplus Q:=P.\mathrm{prodMap}\,Q$（§2.15 载体），经 `toL2`/`fromL2` 线性等价提升到
L²-乘积。这是 Grothendieck 化的**商加法对象载体**。

**交付**（`BerryChern.lean` §2.19，零 sorry、全库 6376 jobs 通过）：

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `toL2`/`fromL2` | 原始乘积 ⟷ L²-乘积的提升线性等价 | `WithLp.linearEquiv` |
| `projDirectSumMap` | 块对角投影 $P\oplus Q$（L²-乘积上） | `toL2.comp ((P.prodMap Q).comp fromL2)` |
| `projDirectSumMap_idempotent/symmetric` | 幂等、自伴直和仍幂等、自伴（落 `SelfAdjointIdemProj`） | `prodMap` 分量 + 共轭保内积 |
| `projDirectSum` | 跨空间直和的 `SelfAdjointIdemProj` 包装（商加法对象构造） | 上两条 |
| `projDirectSumMap_rank_add` | `rank(P⊕Q)=rankP+rankQ` | `toL2.submoduleMap` 保 finrank + §2.15 |
| `quotientRank_projDirectSum_add` | 商秩直和加性 $[\mathbb{C}^r]\oplus[\mathbb{C}^s]\mapsto r+s$ | 上条 + `quotientRank` 展开 |
| `projDirectSum_wellDefined` | $P\sim P'∧Q\sim Q'⟹(P⊕Q)\sim(P'\oplus Q')$（商线性） | §2.14 `same_rank_iff_unitary_conj` + 秩加性 |

**实现要点**：幂等/自伴在 `fromL2` 下逐分量验证（`WithLp.prod_inner_apply` L²-内积分量相加
`inner_toL2`）；秩加性先证像集的 `toL2`-映射等式（`hrange`），再经 `toL2.submoduleMap` 的
`finrank_eq` 归约到 §2.15 `directSum_rank_add`；`projDirectSum_wellDefined` 免构造乘积等距：
分量同秩 ⟹ 直和同秩（秩加性）⟹ §2.14 酉等价。子类型展开用显式 `change` 规避 `rw` 在 `implicit`
透明层下的 coercion 匹配失败。

**诚实边界（随登）**：闭合的是**商加法的对象层商线性**（直和幂等/自伴封闭 + 秩加性 +
`projDirectSum_wellDefined`）；把商构成 **AddCommMonoid/Group**（商类型上加法封闭/结合/单位）、
完整 **Grothendieck 化**（split-exact 关系商），以及 $U(n)$ 酉群/同伦类与秩一一对应，仍需完整
商/群/同伦基建，登记开放。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.19（把 §2.18 边界中「跨空间直和
商良定性」从开放改为闭合）；`sorry_closure_roadmap.md` 追加 §二十五；paper14 升 **v1.27**（版本行
+ 文首形式化支撑清单 + 变更日志 v1.27 行）。

### 2026-09-23（后续）：G3 商构成群的 Grothendieck 群完成——ℕ 的 split-exact 完成 ≅ ℤ（BerryChern.lean §2.20）

**背景**：§2.19 闭合商加法的对象层载体（跨空间直和 $P\oplus Q$ 的商良定性）后，落实完整
Grothendieck 化：把加性幺半群 ℕ 的 split-exact 完成形式化为差对等价，所得商**构成可加交换群**
且 ≅ ℤ。商秩分类器 `quotientRank` 把投影商类映到 ℕ 的差对，故 ℕ 的 Grothendieck 完成是
K₀(ℂ)≅ℤ 在**群层**的最简模型：`GrothQuot ≃+ ℤ`。§2.19 诚实边界中「把商构成
AddCommGroup + Grothendieck 化（split-exact 关系商）」自此闭合。

**交付**（`BerryChern.lean` §2.20，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **Grothendieck 关系（秩层）** `GrothRel`（$\mathbb{N}\times\mathbb{N}$ 上
  $(a,b)\sim(c,d)\iff a+d=b+c$）+ `grothRel_refl`/`_symm`/`_trans` + `grothSetoid`（反身+对称+
  传递 ⟹ `Setoid`，商类型合法存在）+ 商类型 `GrothQuot`。
- **秩差同态** `grothToInt`（`Quotient.lift` 商上良定义 $[(a,b)]\mapsto a-b$）+
  `grothToInt_injective` 单射（零差唯一决定差类）/ `grothToInt_surjective` 满射（非负取 $(r,0)$、
  负取 $(0,s)$，`Int.toNat_of_nonneg`）⟹ 双射 `grothToIntEquiv : GrothQuot ≃ ℤ`。
- **商构成 AddCommGroup** `grothQuotAddCommGroup`（经单射 `grothToInt` 从 ℤ 传送
  `Function.Injective.addCommGroup`）+ 群同态 `grothIntHom` + **群同构
  `grothToIntIso : GrothQuot ≃+ ℤ`**（`AddEquiv.ofBijective`）——K₀(ℂ)≅ℤ 在 Grothendieck 群层的实现。
- **群运算良定** `grothToInt_add` 加法保持 / `grothAdd_mk_eq`（自然加法=逐分量共合
  $[a]+[c]=[a_1+c_1,a_2+c_2]$）/ `grothNeg_mk_eq`（$-[a,b]=[b,a]$）/ `grothZero_eq`（$0=[0,0]$）——
  商加/负/零良定义。
- **与 §2.16 会师** `grothQuot_to_freeAbelian : GrothQuot ≃+ FreeAbelianGroup PUnit`（经
  `grothToIntIso` 与 `single_generator_freeAbelian_iso_int` 复合）——K₀(ℂ)≅ℤ 的 Grothendieck 完成
  与自由交换群两条实现路径一致。
- **连接分类器** `projGrothRel`（投影层 split-exact 差对 $P\oplus Q'\sim_{\text{酉}}P'\oplus Q$）+
  `projGrothRel_iff`（投影 Groth 关系 ⇔ 秩层加法等式，经 `quotientRank_projDirectSum_add` 直和秩加性）
  / `grothToInt_of_rank_diff`（商秩差对送到 `grothToInt`=秩之差）——投影层 Grothendieck 关系正是
  `GrothRel` 经 `quotientRank` 的精确实现。

**诚实边界（随登）**：闭合的是**秩层 ℕ 的 Grothendieck 群完成**（`GrothQuot` 构成 `AddCommGroup`、
`grothToIntIso : GrothQuot ≃+ ℤ`）与投影层 Grothendieck 关系在秩层的判据（`projGrothRel_iff`）；
把**投影商类本身**（自伴幂等投影的酉类商，§2.17/§2.19）作为 Grothendieck 群的对象层完整 K₀ 结构
（商加法沿商类型构成幺半群/群、投影类的 Grothendieck 群 ≅ ℤ）、$U(n)$ 酉群/同伦类与秩一一对应
（把逐对双射提升到群结构层，§3 #7 的商/群/同伦基建）仍登记开放，留待后续。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.20（把 §2.19 边界中「把商构成
AddCommMonoid/Group + Grothendieck 化」从开放改为闭合）；`sorry_closure_roadmap.md` 追加 §二十六；
paper14 升 **v1.28**（版本行 + 文首形式化支撑清单 + 变更日志 v1.28 行）。

### 2026-09-23（后续）：G3 投影商类作为对象层的完整 K₀ 结构闭合（BerryChern.lean §2.21）

**背景**：§2.20 闭合秩层 ℕ 的 Grothendieck 群完成（`GrothQuot ≃+ ℤ`）并把投影层差对关系
`projGrothRel_iff`（⇔ 秩层加法等式）建立在秩层判据上。本轮落实 §2.20 诚实边界中登记的对象层缺环：
把投影层差对关系 `projGrothRel` 构造为**商**，定义**对象层秩差完全不变量** `projToInt`，并验证其
经 §2.20 `grothToInt` 因子分解与秩层 Grothendieck 群一致——即**投影商类作为对象层 K₀ 结构的分类器层**。

**交付**（`BerryChern.lean` §2.21，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **Grothendieck 关系构成 Setoid** `projGrothRel_refl`/`_symm`/`_trans`（经 `projGrothRel_iff` 降到
  秩层加法等式，复用 §2.20 `GrothRel` 的反身/对称/传递）⟹ 实例化 `projGrothSetoid`——
  **投影差对象商类型合法存在**。
- **对象层差商类型** `ProjDiffQuot E := Quotient (projGrothSetoid E)`（差对象 $[P]-[Q]$）+ 代表元构造
  `projMk`。
- **秩差完全不变量（对象层分类器）** `projToInt E : ProjDiffQuot E → ℤ`（`Quotient.lift` 商上良定义，
  $[(P,Q)]\mapsto \mathrm{rank}P-\mathrm{rank}Q$）+ `projToInt_mk` 代表元计算 + `projToInt_injective`
  单射（不同差对象 ⟹ 不同秩差，`Quotient.sound` + `grothToInt_injective` + `Quotient.exact`）。
- **与秩层 Grothendieck 群交接** `projToInt_eq_grothToInt`：$\mathrm{projToInt}\,[P-Q]=\mathrm{grothToInt}
  \,[(r_P,r_Q)]$——对象层分类器经 §2.20 `grothToInt` 因子分解（`grothToInt_of_rank_diff`），
  嵌入 `GrothQuot ≃+ ℤ`，即对象层秩差不变量与秩层语义一致。
- **加性/群同态种子** `projToInt_projDirectSum_add`：分类器沿跨空间直和
  分解（$[(P\oplus Q,\,P'\oplus Q')]\mapsto [P-P']+[Q-Q']$，§2.19 `quotientRank_projDirectSum_add`）——
  K₀ 群同态的对象层基础。

**诚实边界（随登）**：闭合的是**对象层投影商类的分类器层**——投影差对商 `ProjDiffQuot E` 合法存在，
`projToInt` 是**单射**完全不变量（对象层秩差不变量与秩层 Grothendieck 群一致）。仍登记开放：
① `projToInt` 目前是**单射嵌入** $\mathbb{Z}$ 的有界子结构（固定空间 $E$）而非双射——真正的
`ProjDiffQuot ≃+ ℤ` 需把空间 $E$ 的维数取遍（沿所有有限维空间直和闭包，`projToInt_isEmbedding`
为思考路径）；② **对象层商加法本身**（在 `ProjDiffQuot E` 上定义加法并验证结合/交换/单位）未在本层
逐公理构造——当前加性由分类器沿跨空间直和的**加性种子**承载，商上的内乘法尚缺完整幺半/群结构；
③ $U(n)$ 酉群/同伦类与秩的一一对应仍需完整等距/酉群基建。即投影商类作为**完整对象层 K₀ 群结构**
（其 Grothendieck 群 ≅ ℤ）仍登记开放。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.21（把 §2.20 边界中「把投影商类本身……
作为 Grothendieck 群的对象层完整 K₀ 结构（商加法沿商类型构成幺半群/群、投影类的 Grothendieck 群
≅ ℤ）」中**分类器层部分**从开放改为闭合，保留完整群结构的开放登记）；`sorry_closure_roadmap.md`
追加 §二十七；paper14 升 **v1.29**（版本行 + 文首形式化支撑清单 + 变更日志 v1.29 行）。

### 2026-09-23（后续）：G3 对象层分类器的精确值域——各秩投影可实现 + 像恰为有界整数区间（BerryChern.lean §2.22）

**背景**：§2.21 诚实边界①把 `projToInt` 记账为「**单射嵌入 $\mathbb{Z}$ 的有界子结构**而非双射」——
固定有限维空间 $E$ 内秩差被界于 $[-\dim E,\dim E]$。本轮把这条有界单射的**值域精确刻画**出来：
证明各秩 $k\le\dim E$ 的投影**确实可实现**（进而 `projToInt` 的像**恰为**整数区间 $[-\dim E,\dim E]$），
并显式演示为何该像只是**有界区间、而非 $\mathbb{Z}$ 的加法子幺半群**——为跨维度 Grothendieck 群补足
秩可实现基建。

**交付**（`BerryChern.lean` §2.22，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **各秩投影可实现** `projOfRank`：对 $k\le\dim E$，取标准正交基 `stdOrthonormalBasis` 前 $k$ 个基向量
  张成子空间 $U_k$，其正交投影 $U_k.\mathrm{starProjection}$ 幂等且自伴（`Submodule.isSymmetricProjection_starProjection`）
  ⟹ 落在 `SelfAdjointIdemProj E`；且 $\operatorname{finrank}U_k=k$（标准正交基诱导线性无关 +
  `finrank_span_eq_card`、`range_starProjection`）⟹ **秩恰为 $k$** `projOfRank_rankE`（商上取值
  `projOfRank_rank`，秩 0 特例 `projZero_rank`）。
- **整数值可达（分类器满射到区间底座）**：$r\ge0$ 取 $[P_k]-[0]$、$r<0$ 取 $[0]-[P_{(-r)}]$ ⟹
  **非负可达** `projToInt_reaches_nat`（= $k$）+ **负可达** `projToInt_reaches_neg`（= $-k$）。
- **值域上界** `projToInt_mem_range_Icc`：对任意差对象 $y$，$-\dim E\le\mathrm{projToInt}\,E\,y\le\dim E$
  （两枚投影秩各被界于 $[0,\dim E]$，`quotientRank_le_dim` + 非负性的差）。
- **值域恰为有界区间** `projToInt_range_Icc`：$\mathrm{range}\,(\mathrm{projToInt}\,E)
  =\{r\in\mathbb{Z}\mid -α\le r\le α\}$（$α=\dim E$）。左包含（$\subseteq$）用 `projToInt_mem_range_Icc`；
  右包含（$\supseteq$）由整数值可达分正负构造。⟹ `projToInt` 是**到有界区间的双射**
  （单射已由 §2.21 `projToInt_injective`）。
- **闭会展碍 / 非加法子幺半群** `projToInt_range_not_submonoid`（需 $\dim E\ge1$）：取 $a=b=α$
  则 $a,b$ 都在像中而 $a+b=2α\notin[-α,α]$ ⟹ 像**不是 $\mathbb{Z}$ 的加法子幺半群**——固定空间内
  差对象加法无法在值域内封闭（跨维度直和闭包 / Grothendieck 群完成的必要性所在）。

**诚实边界（随登）**：闭合的是**值域精确刻画 + 各秩投影可实现性**——即 `projToInt` 的像**如实等于**
$[-\dim E,\dim E]\cap\mathbb{Z}$，从而 `projToInt` 是**到有界区间的双射**，其像作为 $\mathbb{Z}$
子集**非加法子幺半群**（闭会展碍）。仍登记开放：① 把**投影商类本身**构成跨空间直和闭包下的**完整对象层群**
$\mathrm{ProjDiffQuot}\cong\mathbb{Z}$（本层只演示单空间闭会展碍，未构造沿所有有限维空间的直和并集）；
② 对象层**商加法在同一个商类型上逐公理构成幺半群/群**（§2.21 诚实边界②，须把差对象加法翻译回同一商类型，
闭会展碍使单空间不可行）；③ $U(n)$ 酉群/同伦类与秩一一对应。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.22（把 §2.21 诚实边界①「`projToInt`
单射嵌入 $\mathbb{Z}$ 的有界子结构」中的**值域侧**从开放改为闭合、标注其像**恰为** $[-\dim E,\dim E]$；
保留单空间不等于跨维度、完整 `ProjDiffQuot ≃+ ℤ` 及商加法逐公理结构的开放登记）；
`sorry_closure_roadmap.md` 追加 §二十八；paper14 升 **v1.30**（版本行 + 文首形式化支撑清单 + 变更日志 v1.30 行）。

### 2026-09-23（终）：K₀(ℂ)≅ℤ 的跨维度分组/生成基座——秩-1 类生成 + 跨维度满射到 ℤ（BerryChern.lean §2.23）

**背景**：§2.22 把 `projToInt` 做成**到有界区间** $[-\dim E,\dim E]\cap\mathbb{Z}$ 的双射并演示闭会展碍
（单空间像**非**加法子幺半群），诚实边界①②将其归结为：完整对象层群必须**跨维度直和闭包**。本轮把
"维数取遍"落成显式构造——以 `EuclideanSpace ℂ (Fin n)` 作跨维度标准空间，证**秩-1 类 $[\mathbb{C}^1]$
生成整个 Grothendieck 群**、**每个整数都被某维数空间投影类实现**（跨维度满射到 $\mathbb{Z}$）、并给出
对象层分类器与秩的直接等式——为「整体秩是 $\mathbb{Z}$ 双射（跨维度单射 §2.21 + 满射本层 + 加法 §2.19）」
的收口补足生成/分组基建。

**交付**（`BerryChern.lean` §2.23，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **跨维度标准空间** `canonicalSpace n = EuclideanSpace ℂ (Fin n)` 及其确切维数 `canonicalSpace_finrank`
  （$\operatorname{finrank}_{\mathbb{C}}(\mathbb{C}^n)=n$，`simp`）。
- **秩-1 类取 1 / 跨维度一致**：`rankOne_class_projToInt`（$[\mathbb{C}^1]\mapsto 1$）+ `rankOne_class_any_dim`
  （任何 $\ge1$ 维空间的秩-1 投影类秩差都是 1——"所有 $\mathbb{C}^1$ 同构类一致"在分类器层体现）。
- **跨维度满射到 ℤ** `crossDim_reaches_any`：对每个整数 $r$，$r\ge0$ 取 $\mathbb{C}^r$、$r<0$ 取 $\mathbb{C}^{-r}$，
  都有秩可达投影类 `projToInt = r`（`Int.toNat_of_nonneg`/`neg_neg`）——由此 §2.22 单空间有界像的**维数上界被解除**。
- **Grothendieck 群由秩-1 类生成** `grothQuot_generated_by_one`：每个类都是 $[(1,0)]\in\mathrm{GrothQuot}$ 的
  $\mathbb{Z}$ 倍（$k\cdot[\mathbb{C}^1]=[(k,0)]$；`grothToIntIso` 单射 + `map_zsmul` + `grothToInt_grothOneClass`）——
  K₀(ℂ)≅ℤ 的**生成元层**真语句：一切投影类都在秩-1 类的整倍中。
- **对象层分类器即秩** `projClass_int_eq_rank`：$\mathrm{projToInt}\,E\,[P,0]=\operatorname{rank}P$
  （`projToInt_mk` + `quotientRank, Quotient.lift_mk` + `projOfRank_rank`）。

**诚实边界（随登）**：闭合的是**秩层的跨维度分组/生成基底**——即"整体秩是 $\mathbb{Z}$ 双射"的
**满射侧**（跨维度）与**秩-1 生成**：`projToInt` 跨维度可到达**每个**整数（§2.23 `crossDim_reaches_any`），
且 Grothendieck 群由 $[\mathbb{C}^1]$ 生成；配合 §2.21 `projToInt` 单射（跨维度单射侧）与 §2.19 直和秩加性
（加法侧），整体（跨所有有限维空间并集的）秩分类是 ℤ 双射。仍登记开放：① **同一商类型的完整对象层
`AddCommGroup`**——把 `ProjDiffQuot ≃+ ℤ` 做成对象层到整个 $\mathbb{Z}$ 的显式同构（跨所有有限维空间
直和并集；载体由 §2.20 `grothToIntIso`/§2.16 `grothQuot_to_freeAbelian` 提供，但对象层直和**封闭**需
具体取并集商类型，未构造）；② $U(n)$ 酉群/同伦类与秩一一对应（逐对双射提升到群结构层）。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.23（把 §2.22 诚实边界①②「完整对象层群
需跨维度直和闭包」「单空间商加法不封闭」中原"跨维度满射 + 秩-1 生成"侧改为闭合，保留"同一商类型完整
$AddCommGroup$ 结构"与 $U(n)$ 对应的开放登记）；`sorry_closure_roadmap.md` 追加 §二十九；
paper14 升 **v1.31**（版本行 + 文首形式化支撑清单 + 变更日志 v1.31 行）。

### 2026-09-23（收口）：对象层 K₀ 群——跨维度直和闭包下的 `ProjClass ≃+ ℤ`（BerryChern.lean §2.24）

**背景**：§2.23 把"维数取遍"落到**分类器层**（跨维度满射 + 秩-1 生成），但仍登记"同一商类型的完整
对象层 `AddCommGroup` 结构"开放。本轮把这一缺口在**对象层群结构**上收口：构造跨维度和型等距，把
§2.19 直和投影搬回规范空间，从而在跨维度对象层载体上定义**由直和诱导的加法**，按秩作商得对象层
K₀ 类 `ProjClass`，证其构成可加交换群并**群同构于 ℤ**，且**类加法恰由直和实现**。

**交付**（`BerryChern.lean` §2.24，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **跨维度和型等距** `canonicalSpaceAddIso : ℂ^{n+m} ≃ₗᵢ WithLp 2 (ℂ^n × ℂ^m)`（`LinearIsometryEquiv.piLpCongrLeft`
  指标重排 + mathlib `PiLp.sumPiLpEquivProdLpPiLp`）。
- **沿等距共轭投影** `conjProj`（`P ↦ e∘P∘e⁻¹` 仍自伴幂等：幂等由复合消约，自伴由
  `LinearMap.isSymmetric_linearIsometryEquiv_conj_iff`）+ **共轭保秩** `conjProj_rank`
  （像集 `(range P).map e` + `LinearEquiv.finrank_map_eq`）。
- **规范直和投影** `projDirectSumCanon`（§2.19 `projDirectSum` 沿等距搬回 `ℂ^{n+m}`）+
  **秩加性** `projDirectSumCanon_rank` + **分类器加性** `projToInt_projDirectSumCanon_add`
  （归约 §2.19 `quotientRank_projDirectSum_add`）。
- **跨维度对象层载体** `ProjPoint = Σ n, ProjDiffQuot (ℂ^n)` + **直和加法** `+`（`projDiffSumCanon`，
  双重商 `Quotient.lift₂` 良定经 `projToInt` 单射）+ **整体秩分类器** `projPointRank` +
  **直和加性** `projPointRank_add`。
- **对象层 K₀ 类** `ProjClass`（按 `projPointRank` 相等作商）+ `projClassRank` **单射**/**满射**
  （满射用 §2.23 `crossDim_reaches_any`）⟹ **`projClassEquiv : ProjClass ≃ ℤ`**；
  **对象层群结构** `projClassAddCommGroup`（`Function.Injective.addCommGroup` 从 ℤ 传送）+
  **群同态** `projClassRankHom` + **群同构** `projClassRankIso : ProjClass ≃+ ℤ`。
- **自然性** `projClassMk_add`：类加法**恰由跨维度直和实现** `[a] + [b] = [a ⊕ b]`
  （`projPointRank` 沿直和加性）——§2.20 秩层 Grothendieck 群 `GrothQuot ≃+ ℤ` 的**对象层显式实现**。

**诚实边界（随登）**：闭合的是**对象层完整群结构 ≅ ℤ**——载体 `ProjPoint`/`ProjClass` + 由直和
诱导的加法 + 群公理（`projClassAddCommGroup`）+ 与 ℤ 的**群同构**（`projClassRankIso`）+
**类加法即直和的自然性**（`projClassMk_add`）。由此 §2.22/§2.23 登记"同一商类型的完整对象层
`AddCommGroup`（`ProjDiffQuot ≃+ ℤ` 跨维度直和闭包）"由开放改为闭合（载体取跨维度 `Σ n, ProjDiffQuot (ℂ^n)`
并商、加法由直和诱导）。仍登记开放：① $U(n)$ 酉群/同伦类与秩一一对应（把逐对双射提升到群结构层）；
② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.24（把"同一商类型的完整对象层
`AddCommGroup` 结构"从开放改为闭合、记录 `ProjClass ≃+ ℤ` 与 `projClassMk_add` 自然性；
保留 $U(n)$ 对应与陈数连续场论整性的开放登记）；`sorry_closure_roadmap.md` 追加 §三十；
paper14 升 **v1.32**（版本行 + 文首形式化支撑清单 + 变更日志 v1.32 行）。

### 2026-09-23（后续）：酉群作用层——`U(E)` 共轭作用、轨道 = 秩类、轨道空间 ≃ 秩集（BerryChern.lean §2.25）

**背景**：§2.14/§2.21 已把「同秩 ⇔ 酉等价」做成**逐对显式双射**，§2.17 把酉等价形式化为 `Setoid`，
§2.24 把对象层 K₀ 群结构 ≅ ℤ 收口。本轮转向剩余开放项①（$U(n)$ 与秩一一对应），把**逐对**结论
升级到**群结构层**：把酉群在投影上的共轭作用做成真正的 `MulAction`，证明**轨道 = 秩类**，并给出
**轨道空间 ≃ 秩集**——即 $U(E)$ 的轨道与秩 $0,\dots,\dim E$ 一一对应（轨道数 $=\dim E+1$）。

**交付**（`BerryChern.lean` §2.25，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **酉群** `unitaryEnd E := E ≃ₗᵢ[ℂ] E`（mathlib `Group` 实例）+ 逆应用引理
  `unitaryEnd_symm_one`（单位）、`unitaryEnd_symm_mul`（乘积反序）。
- **共轭作用** `unitaryConjAct : MulAction (unitaryEnd E) (SelfAdjointIdemProj E)`，
  `u • P := conjProj u P`（复用 §2.24 `conjProj`）；作用律 `unitaryConjAct_smul`。
- **作用保秩** `unitaryConjAct_rank`（`conjProj_rank`）+ **保持酉类** `unitaryConjAct_rel`
  （`ProjUnitaryRel P (u • P)`，作用在商 `Quotient (projUnitarySetoid E)` 上平凡）。
- **轨道 = 秩类** `mem_orbit_iff_same_rank`（$Q$ 在 $P$ 的酉轨道中 ⟺ 秩相等）+ `orbit_eq_rankClass`
  （轨道作为集合 = 秩类）+ **轨道相等 ⟺ 秩相等** `orbit_eq_iff_same_rank`。
- **轨道空间 ≃ 秩集** `orbitQuotEquivRankSet : Quotient (orbitRel) ≃ {k : ℕ // k ≤ dim E}`：
  单射（轨道关系 = 秩相等）+ 满射（`exists_projRank_eq`，用 §2.22 `projOfRank` 实现每个秩）。

**诚实边界（随登）**：闭合的是**轨道层**的对应——即把 §2.21 的**逐对**酉双射提升为**轨道分解**
（轨道 = 秩类、轨道空间 ≃ 秩集）。仍登记开放：① $U(n)$ **同伦层**（$U(n)$ 路径连通 / 投影空间的
连通分量与秩对应，需拓扑/同伦基建）；② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.25（把「$U(n)$ 酉群与秩一一对应」的
**轨道层**从开放改为闭合、记录 `orbitQuotEquivRankSet` 与轨道 = 秩类；保留**同伦层**与陈数连续
场论整性的开放登记）；`sorry_closure_roadmap.md` 追加 §三十一；paper14 升 **v1.33**（版本行 +
文首形式化支撑清单 + 变更日志 v1.33 行）。

### 2026-09-23（后续）：对象层 K₀ 的等距自然性——差类映射、分类器不变量、函子性与酉作用平凡（BerryChern.lean §2.26）

**背景**：§2.21 造出对象层差对象商 `ProjDiffQuot E` 与秩差分类器 `projToInt`（单射），§2.24 造出
跨维度对象层群 `ProjClass ≃+ ℤ`，§2.25 给出酉群共轭作用与轨道 = 秩类。本轮补齐**自然性**：把 §2.24
的等距共轭 `conjProj` 沿对象层下降为差类映射，证明其与分类器交换、是双射、满足函子性，并得出
**酉群在对象层 K₀ 上作用平凡**（K₀ 是酉不变量）。

**交付**（`BerryChern.lean` §2.26，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **分类器等距不变量** `projToInt_conjProj`：
  $\mathrm{projToInt}\,F\,[(ePe^{-1})-(eQe^{-1})]=\mathrm{projToInt}\,E\,[P-Q]$（经 §2.24 `conjProj_rank` 保秩）。
- **等距诱导差类映射** `conjProjQuot e : ProjDiffQuot E → ProjDiffQuot F`（`Quotient.lift` 良定，
  经 `projToInt` 单射 + 等距不变量）+ 代表元计算 `conjProjQuot_mk`。
- **与分类器交换** `conjProjQuot_projToInt`：$\mathrm{projToInt}\,F\,(\mathrm{conjProjQuot}\,e\,x)=\mathrm{projToInt}\,E\,x$。
- **双射** `conjProjQuot_injective`/`_surjective` ⟹ `conjProjQuotEquiv : ProjDiffQuot E ≃ ProjDiffQuot F`
  （逆用 `e.symm` 诱导的映射）。
- **函子性** `conjProj_trans`（共轭对复合相容）+ `conjProj_refl`（对恒等相容）+ `conjProjQuot_trans`
  （`conjProjQuot (e₁.trans e₂) = conjProjQuot e₂ ∘ conjProjQuot e₁`）+ `conjProjQuot_refl`（`conjProjQuot 1 = id`）。
- **酉作用平凡** `conjProjQuot_unitary_fixed`：`conjProjQuot u x = x`（`u : unitaryEnd E`）——
  对象层 K₀ 是**酉不变量**，与 §2.17「酉等价 = 秩」、§2.21「`projToInt` 只依赖秩」一致。

**诚实边界（随登）**：闭合的是**对象层 K₀ 的等距自然性**（差类映射 + 分类器交换 + 双射 + 函子性 +
酉作用平凡）。仍登记开放：① $U(n)$ **同伦层**（路径连通 / 投影空间连通分量与秩对应，需拓扑/同伦
基建；已确认 mathlib 尚无酉群连通性结果）；② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.26（记录 `conjProjQuot`/`conjProjQuotEquiv`/
`conjProjQuot_unitary_fixed` 等自然性结论）；`sorry_closure_roadmap.md` 追加 §三十二；paper14 升
**v1.34**（版本行 + 文首形式化支撑清单 + 变更日志 v1.34 行）。

### 2026-09-23（后续）：酉群连通性的拓扑基建第一层——局部路径连通与连通性归约（BerryChern.lean §2.27）

**背景**：§2.25/§2.26 已闭合酉群作用的轨道层与对象层 K₀ 自然性，但「$U(n)$ 与秩一一对应」的
**同伦层**一直登记开放（此前确认 mathlib `LinearAlgebra/Matrix` 无酉群连通性结果）。本轮实地勘查
发现 **两个关键事实**，据此铺基建：(i) mathlib 已有
`Mathlib/Analysis/CStarAlgebra/Unitary/Connected.lean`——C\*-代数酉群的**局部路径连通**理论与
「路径分量 = 自伴指数乘积」刻画；(ii) `Matrix n n ℂ` 在 L²-算子范数下**是 C\*-代数**
（`Matrix.instCStarAlgebra`，经 `open scoped Matrix.Norms.L2Operator` 激活）。二者相合，可把 mathlib
酉群拓扑理论**直接实例化到矩阵酉群** `Matrix.unitaryGroup n ℂ`。

**交付**（`BerryChern.lean` §2.27，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **局部路径连通** `unitaryGroup_locallyPathConnected`（mathlib `Unitary.instLocallyPathConnectedSpace`）
  ——同伦层核心局部输入。
- **小距离路径连通** `unitaryGroup_joined`：`‖v - u‖ < 2` 的酉元可用显式路径连接
  （mathlib `Unitary.joined`，路径 `t ↦ expUnitary (t • argSelfAdjoint (v * star u)) * u`）。
- **小球路径连通** `unitaryGroup_isPathConnected_ball`（mathlib `Unitary.isPathConnected_ball`）。
- **路径分量 = 自伴指数乘积** `mem_pathComponent_one_iff_products`：`1` 的路径分量恰为**有限个自伴指数
  之积**（mathlib `Unitary.mem_pathComponentOne_iff`）——把"连通"转为纯代数陈述。
- **有界性** `unitaryGroup_entry_norm_le_one`（mathlib `entry_norm_bound_of_unitary`，紧性输入）。
- **连通性归约** `pathConnectedSpace_unitaryGroup_of_products`：**若每个酉阵是有限个自伴指数之积，则
  `U(n)` 路径连通**——把全局连通性归约为"指数积覆盖"。

**诚实边界（随登）**：闭合的是**局部拓扑基建 + 连通性归约**（局部路径连通 + 小球路径连通 + 路径分量
刻画 + 归约定理 + 有界性）。仍登记开放：① $U(n)$ **全局连通性**本体——归约到「每个酉阵 = 有限个自伴
指数之积」，即酉阵的**正规谱定理/对数存在性**（mathlib 目前仅有 Hermitian 谱定理
`Matrix.IsHermitian.eigenvectorUnitary`，正规情形缺）；② 环面上陈数密度 $F$ 的连续场论/度理论整性。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.27（记录拓扑基建第一层与连通性归约；
把开放项 a) 由「$U(n)$ 同伦层（需拓扑基建）」改写为「全局连通性本体（需正规谱定理）」）；
`sorry_closure_roadmap.md` 追加 §三十三；paper14 升 **v1.35**（版本行 + 文首形式化支撑清单 +
变更日志 v1.35 行）。

### 2026-09-23（后续）：全局连通性归约强化——`pathComponent 1` 是子群 + 「避开 -1」子类（BerryChern.lean §2.28）

**背景**：§2.27 把 $U(n)$ 全局连通性归约为「指数积覆盖」（`mem_pathComponentOne_iff`）。本轮把该
归约**强化为可操作形式**，为补正规谱定理铺最后一层基建：证明指数积集合 `pathComponent 1` 是**子群**，
从而全局连通性化归为**单一群论命题**；并证明**「避开 `-1`」子类**已落入该子群。

**交付**（`BerryChern.lean` §2.28，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **指数取逆公式** `expUnitary_neg`：`expUnitary (-x) = (expUnitary x)⁻¹`。
- **`pathComponent 1` 是子群**：`expUnitary_mem_pathComponent_one`（单指数）+
  `one_mem_pathComponent_one`（单位）+ `mul_mem_pathComponent_one`（乘法，经 `Joined.mul`）+
  `inv_mem_pathComponent_one`（逆，经列表技巧 `reverse_map_neg_prod_mul_prod`：**逆序取负**的指数积
  即原积之逆）。
- **「避开 `-1`」子类闭合** `mem_pathComponent_one_of_norm_sub_lt_two`：`‖u - 1‖ < 2`（⇔ `-1 ∉ spectrum u`）
  时 `u = expUnitary (argSelfAdjoint u)` 落入 `pathComponent 1`。
- **连通性判据** `pathConnectedSpace_unitaryGroup_of_mem_pathComponent_one`：
  `(∀ u, u ∈ pathComponent 1) ⟹ PathConnectedSpace`。

**诚实边界（随登）**：闭合的是**归约强化**（子群结构 + 判据 + 已知子类）；全局连通性本体仍归约为
**单一命题** `∀ u : Matrix.unitaryGroup n ℂ, u ∈ pathComponent 1`（= 每个酉阵是有限个自伴指数之积），
其完整证明需**酉阵的正规谱定理/对数存在性**（mathlib 仅有 Hermitian 谱定理），登记开放；两条可行路径：
(i) 正规矩阵酉对角化（特征向量 + 正交补不变性 + 维数归纳）；(ii) 「旋转 + 指数」技巧（取单位标量 ζ
使 `-ζ ∉ spectrum u`，需 `spectrum u` 有限，则 `u = (ζ·1)·(ζ⁻¹u)` 为两枚「避开 `-1`」酉元之积）。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.28（记录子群结构与判据，并把开放项 a)
精确化为单一命题 + 两条可行路径）；`sorry_closure_roadmap.md` 追加 §三十四；paper14 升 **v1.36**
（版本行 + 文首形式化支撑清单 + 变更日志 v1.36 行）。

### 2026-09-23（后续）：矩阵谱有限性——"旋转 + 指数"路线的最后一块基建（BerryChern.lean §2.29）

**背景**：§2.28 给出闭合 $U(n)$ 全局连通性的两条路径。其中**「旋转 + 指数」路线**最省力，唯一缺口是
**矩阵谱有限性**（用于在单位圆上选出旋转标量 `ζ` 使 `-ζ ∉ spectrum u`）。本轮补齐它。

**交付**（`BerryChern.lean` §2.29，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **矩阵谱有限性** `matrix_spectrum_finite`：`(spectrum ℂ A).Finite`（`A : Matrix n n ℂ`）。
  数学要点：谱 = **特征多项式根集**（mathlib `Matrix.mem_spectrum_iff_isRoot_charpoly`：
  `r ∈ spectrum ℂ A ↔ IsRoot A.charpoly r`），由 `charpoly A ≠ 0`（首一 `charpoly_monic.ne_zero`）
  与 `mem_roots` 得根集是有限多重集支撑。
- **`Finite` 类型类形式** `matrix_spectrum_finite'`：本版本 mathlib 中 `Set.Finite s` 即子类型上的
  `Finite s`，故同一结果可直接作类型类使用（`haveI`）。
- **酉元谱有限性** `unitary_spectrum_finite`：`u : Matrix.unitaryGroup n ℂ` 时谱有限。

**诚实边界（随登）**：本层闭合的是**谱有限性基建**——「旋转 + 指数」路线的最后一块就位。补齐后该路线
仍需两块：(i) **单位圆无穷 ⟹ 存在单位标量 `ζ` 使 `-ζ ∉ spectrum u`**（需 `Circle`/`sphere` 无穷）；
(ii) **标量谱变换** `spectrum ℂ (c • A) = c • spectrum ℂ A`（`c ≠ 0`；mathlib 无现成引理，可由
`charpoly` 与行列式重推）。二者与 §2.28 `mem_pathComponent_one_of_norm_sub_lt_two` 合用即可闭合全局
连通性。另一条路（正规矩阵酉对角化）不受本层影响，仍登记开放。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.29（记录谱有限性；把开放项 a) 的
「旋转 + 指数」路线剩余缺口精确化为两块）；`sorry_closure_roadmap.md` 追加 §三十五；paper14 升
**v1.37**（版本行 + 文首形式化支撑清单 + 变更日志 v1.37 行）。

### 2026-09-24：全局连通性收口——U(n) 路径连通（BerryChern.lean §2.30，K₀ 同伦层闭合）

**背景**：§2.27–§2.29 已备齐连通性归约的全部零件，仅剩两块基建。本轮一次性补完并**收口**。

**交付**（`BerryChern.lean` §2.30，零 sorry、全库 build 通过、BerryChern 零 warning）：
- **单位圆无穷** `unitCircle_infinite`：半圆参数化 `x ↦ (x, √(1-x²))`（`x ∈ (-1,1)`）落在单位圆上
  且单射，而 `(-1,1)` 无穷 ⟹ 单位圆无穷（避免依赖 `Circle` 的现成无穷性，mathlib 无此引理）。
- **标量谱变换** `smul_mem_spectrum_iff`：`z ∈ spectrum ℂ (c • a) ↔ c⁻¹ z ∈ spectrum ℂ a`（`c ≠ 0`）。
  经 `spectrum.mem_iff` 化为 `IsUnit` 判定 + 因式分解 `z • 1 - c • a = c • (c⁻¹z • 1 - a)`
  （辅助引理 `isUnit_algebraMap_mul_iff`：标量因子可提出单位判定）。
- **选取引理** `exists_norm_eq_one_notMem_neg`：`S` 有限 ⟹ 存在单位圆上 `ζ` 使 `ζ ≠ -z`（∀z ∈ S）。
- **标量酉元落点** `neg_one_notMem_spectrum_smul_one` + `smul_unitary_mem_unitary` +
  `scalar_smul_one_mem_pathComponent_one`：`ζ • 1 ∈ pathComponent 1`（`‖ζ‖=1`、`ζ ≠ -1`）。
- **旋转落点** `smul_unitary_mem_pathComponent_one`：`c • u ∈ pathComponent 1`
  （`‖c‖=1`、`-c⁻¹ ∉ spectrum u`）。
- **主定理** `mem_pathComponent_one_unitary`：**每个酉元都是有限个自伴指数之积**——
  「旋转 + 指数」：`u = (ζ • 1) · (ζ⁻¹ • u)`，两因子各由 §2.28 判据落入，乘法封闭即得。
- **指数积表示** `exists_expUnitary_prod_eq` + **`pathConnectedSpace_unitaryGroup`**（$U(n)$ **路径连通**）
  + `connectedSpace_unitaryGroup`。

**诚实边界（随登）**：本层**闭合** $U(n)$ 全局连通性（路径连通）与等价的指数积覆盖定理，从而闭合
§3 #7 登记的「$U(n)$ 酉群/同伦类与秩一一对应」的**连通性/同伦层**。**仍未闭合**：环面上陈数密度 $F$
的连续场论/度理论整性（含同伦提升，§3 #4）——需 `F` 的可积性/光滑性与环面积分层面的度理论，与群拓扑
连通性相互独立。另一条路线（正规矩阵酉对角化）未采用，成为冗余路径。

**同步**：BerryChern §3 开放登记第 7 项 + 已闭合清单标注 §2.30；`sorry_closure_roadmap.md` 追加
§三十六；paper14 升 **v1.38**（版本行 + 文首形式化支撑清单 + 变更日志 v1.38 行）。

### 2026-09-24（后续）：陈数整性的环绕数层（BerryChern.lean §2.31，§3 #2/#4 连续积分层第二块基石）

**背景**：用户指定推进 §3 #4（陈数绝热不变性）/#2（陈数整性）。本轮先做**实地勘查**并交付可达的
第一层。

**勘查结论（重要）**：mathlib **完全缺失** `windingNumber` 与度理论基建——`Mathlib/Analysis/Complex`
下无任何 `windingNumber`、无 `IsInteger`、无「`Homotopic` + 环路积分」引理。故一般度理论
（一般 $S^1\to S^1$ 映射的度 ∈ ℤ、路径提升、度的同伦不变性）须**从零搭建**，属远期工程。

**交付**（`BerryChern.lean` §2.31，零 sorry、全库 build 通过、BerryChern 零 warning）：
- `circleIntegral_const_mul_inv`：圆周积分常数倍线性 $\oint n/z = n\oint 1/z$
  （`circleIntegral.integral_const_mul` + §2.10 `unitCircle_integral_inv`）。
- `logDeriv_pow`：**`z ↦ z^n` 的对数导数** $f'/f = n/z$（`z ≠ 0`；`n = 0` 两边为 0，
  `n ≥ 1` 经 `deriv_pow`（`(z^n)' = n z^{n-1}`）+ `div_eq_div_iff` 交叉相乘）。
- `unitCircle_windingNumber_pow`：**`z ↦ z^n` 的环绕数 = n ∈ ℤ**——陈数整性在连续积分层的
  **首个非平凡模型族**（§2.10 仅覆盖 $n = 1$ 的恒等映射）。

**诚实边界（随登）**：闭合的是**模型族的环绕数整值**。§3 #2（一般连续映射的陈数整性）与 §3 #4
（陈数绝热不变性）仍开放，且本轮已确认为**从零搭建**级工程：① 一般度理论（路径提升
$S^1\to\mathbb R$、度的同伦不变性、$T^2$ 上双参数版本）；② 曲率被积 $F$ 的可积性/光滑性
（⇐ 投影族 $P(k)$ 光滑，属 Kato 微扰论层）。

**同步**：BerryChern §3 开放登记 #4（并注明 #2）标注 §2.31；paper14 升 **v1.39**（变更日志行）。
