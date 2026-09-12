# 研究笔记：paper14 凝聚态谱表述的内生第一性重建——从范畴 Δ 出发的缺口分析与重建规划

**文档编号**：MUFPF-RN-ENDO-001
**日期**：2026-09-12
**版本**：v1.0
**状态**：重建进行中；G5（NoiseCategory 真证）、G6（IQHE RG 常数裁定）、G2（谱流自洽方程正实根存在唯一性）已闭合（见 §8），其余按 §5 路线推进
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

---

## 5. 重建路线（Phase 建议）

**近期（补证据最痛处）**：
1. G5：NoiseCategory 占位定理真证 + ε_eff 闭式 Lean 化（Paper XIV §3.4 是全文唯一自称"第一性原理推导"的推导，名实差距最大）。
2. G6 路线 (b)：若 (a) 短期不可行，先把定理 3.2/3.3 的措辞改为现象学声明。

**中期（桥与拓扑）**：
3. G2：r 的弱耦合极限定理化（WeaveBCS 已给出方程与数值锚点 r ≈ 0.874）。
4. G3：陈数模块（Berry 曲率 → 第一陈数 → TKNN 谱公式）。
5. G4：GP-谱流等同的形式化条件 + 涡旋荷守恒。

**远期（真内生链）**：
6. G1：Paper XX 链泛化到凝聚态谱生成元，与 G2 会师，形成 Δ → … → Δ_BCS → ρ₀ → T_c 标度的全内生链。

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

**G5 遗留**：ε_eff 闭式的 Lean 化（§3.4 纸面解析推导）未在本轮做——它是 paper14 §3.4
的专属对象，并入重建阶段与措辞重定级一并处理，不单独立项。

全链闭合与证伪处置记录见 `formal_proof/MUFPFormalization/sorry_closure_roadmap.md` §6。

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
