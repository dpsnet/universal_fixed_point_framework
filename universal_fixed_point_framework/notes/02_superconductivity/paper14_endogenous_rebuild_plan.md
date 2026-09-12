# 研究笔记：paper14 凝聚态谱表述的内生第一性重建——从范畴 Δ 出发的缺口分析与重建规划

**文档编号**：MUFPF-RN-ENDO-001
**日期**：2026-09-12
**版本**：v1.0
**状态**：G1–G6 全部建立有限维可证核心并登记开放项；paper14 v1.6 内生标注体系重建（第一轮）完成，逐节全面标注为持续工作
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
整性 C∈ℤ、TKNN 公式 σ_xy=(e²/h)C、陈数绝热不变性、规范不变性细节——需环面积分、
拓扑度/同伦、Kubo 线性响应等基础设施，属积分/场论形式化（远期）。

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
