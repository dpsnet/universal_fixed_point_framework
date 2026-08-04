# 量子重整化完整链条：谱 Feynman → 谱正则化 → 谱流 → β 函数 → EFT 层级

**笔记状态**：初版（2026-08-03）
**对应路线图**：`roadmap/phase61_physics_advancement.md` P0-2（Phase 61C）
**规划依据**：`docs/针对v0.9版系列论文的客观评价.md` §二-3 缺口②"量子重整化——拉氏量 → 费曼圈拓扑 → 动量积分 → 紫外正则化 → 完整 RG 流的全链路形式化"缺失。
**完成判据**：拉氏量 → 圈图 → 正则化 → RG 流的谱形式化链条（Lean/Agda），β 函数从谱流方程导出。
**前置条件**：T3 测度论完整层（fc-integral 完整降定理、sup 交换、Lebesgue 积分机制，v1.36 闭合）。
**规范声明**：严格区分【标准 QFT 重整化既有结果】与【本框架新增推导】（谱化对应/谱流机制）。后者标注"谱新增"。

---

## 1. 已有资产盘点

| 资产 | 内容 | 状态 |
|:----|:----|:----:|
| Paper 11 §2.5 | A5 谱截断正则化公理：Λ_max = max σ(A_φ)，自然 UV 边界 | ✅ |
| Paper 11 §2.6 | A6 谱重整化公理 + 谱 β 函数：λφ⁴ 单圈 β = 3λ²/16π² | ✅ 纸面 |
| Paper 11 §2.1 | 谱 Wick 定理 | ✅ 纸面 |
| Paper 11 §2.9 | 谱 Dyson 级数 + 谱 β 函数定理（定理 2.2/2.3） | ✅ 纸面 |
| Paper 11 §5.2 | 谱截断正则化数值：I_Sp = ∫dλ/(λ−m²)² 在 Λ 下有限 | ✅ 数值 |
| Paper 5 §6 | 谱流方程 dA_t/dt = [G,A_t] 量子化：单圈 β 精确匹配 (1.000000)、双圈 DS 修正、三圈 12/12 | ✅ 数值 |
| 数值 | `paper5_beta_functions.py`（单圈）、`paper31_threeloop_beta.py`（三圈 12/12）、`paper27_dyson_schwinger.py` | ✅ |
| T3 层 | 谱定理 + 测度论（fc-integral 完整降定理 v1.13、sup 交换、Lebesgue 积分、方案 A 收官 v1.34） | ✅ 闭合 |

缺失：从拉氏量到 RG 流的**全链路统一形式化**——"谱流 → β 函数"单一定理链（而非分立纸面公式）、谱正则化的严格表述、EFT 层级的严格定理。

---

## 2. T1：谱 Feynman 规则完整化（拉氏量 → 圈图衔接）

### 2.1 谱翻译管线【既有：Phase 44 工具箱 + Paper 11 §3/§4】

Phase 44 已建：谱拉格朗日量（`paperX_spectral_lagrangian.py`）→ 谱 Feynman 规则（`paperX_spectral_feynman.py`，7/7）→ 谱路径积分（`paperX_spectral_renormalization.py`）。缺失环节：**圈图积分与谱传播子谱和的衔接**。

### 2.2 谱圈图积分【谱新增：定义】

**定义 2.1**（谱圈图积分）。动量圈积分翻译为谱积分（谱参数 λ = k²）：

$$\int \frac{d^4k}{(2\pi)^4} \prod_i \frac{1}{k^2 - m_i^2 + i\varepsilon} \;\longmapsto\; I_{\mathrm{Sp}} = \int_{\lambda_c}^{\Lambda_{\max}} d\lambda \prod_i \frac{1}{\lambda - m_i^2 + i\varepsilon}$$

其中谱截断 $\Lambda_{\max} = \max\sigma(A_\phi)$（A5 公理，自然 UV 边界），积分下界 $\lambda_c > m_i^2$（on-shell 极点由 $+i\varepsilon$ 处方处理）。

**定理 2.1**（谱单圈积分有限性）。在谱截断下：(a) 幂次积分有限，$I_{\mathrm{Sp}} = \int_{\lambda_c}^{\Lambda_{\max}} d\lambda/(\lambda-m^2)^2 = 1/(\lambda_c-m^2) - 1/(\Lambda_{\max}-m^2)$；(b) 对数发散积分被谱截断吸收为有限值 $J_{\mathrm{Sp}} = \int_{\lambda_c}^{\Lambda_{\max}} d\lambda/(\lambda-m^2) = \ln((\Lambda_{\max}-m^2)/(\lambda_c-m^2))$。

*证明要点*。直接积分 $\int dx/(x-m^2)^2 = -1/(x-m^2)$、$\int dx/(x-m^2) = \ln(x-m^2)$ 代入上下限（$\lambda_c > m^2$ 保证极点不在积分区）。□

数值（脚本 §2）：幂次积分 0.156250 精确匹配解析值；对数积分 2.7726 = ln((100−4)/(10−4))（发散被截断为有限）。

---

## 3. T2：谱正则化（谱截断 Λ_max 的严格表述）

### 3.1 谱截断 = 物理 UV 边界【既有：A5 公理】

**定义 3.1**（谱截断）。Λ_max = M_Pl = λ_max(A_GR)（谱算子最大特征值）。谱 QFT 的圈积分在 Λ_max 处自然截断——非人工正则化器，而是谱离散化的内在结构。

### 3.2 谱截断-耦合对偶【谱新增：定义】

谱截断与规范耦合的对偶（P0-1 定义 4.2 推广）：Δλ_min(μ) = Δλ_min·α⁽⁰⁾/α(μ)。在重整化语境中：

**定义 3.2**（谱 UV 边界条件）。谱 β 函数的积分以 Λ_max = M_Pl 为 UV 边界：(M_Pl, α⁽⁰⁾) 为 RG 流初值，红外值为观测耦合（P0-1 定理 4.1 的机制）。

---

## 4. T3：β 函数统一推导（谱流 → β 函数，主定理）【谱新增】

### 4.1 谱流方程与 β 函数的统一【核心定理】

**定理 3.1**（谱流 → β 函数统一定理）。谱流方程 $dA_t/dt = [G(t), A_t]$（Paper 5）与重整化群方程 $d\lambda_R/d\ln\mu = \beta(\lambda_R)$ 由能标-时间对偶统一：

$$\beta(\lambda_k) = \frac{d\lambda_k}{d\ln\mu} = \frac{d\lambda_k}{dt} = \langle k | [G, A_t] | k \rangle,$$

其中 RG 参数与谱流时间对偶 $d\ln\mu = dt$，$G = \sum_i g_i A_{F,i}$ 为规范耦合谱生成元，$\lambda_k(t) = \langle k|A_t|k\rangle$ 为谱流特征值。

*证明要点*。（1）谱流方程在瞬时本征基上的对角元：$\dot{\lambda}_k = \langle k|[G,A_t]|k\rangle$（本征基变化项为纯虚 Berry 相位，实部为零——谱流保 Hermitian 推论）。（2）能标-时间对偶：RG 群方程 $d\lambda_R/d\ln\mu = \beta$ 与谱流方程同构（Paper 5 §6 的量子化对应），故 β 函数 = 谱流特征值动力学。（3）n 圈 β 对应 n 阶对易子（§4.2）。□

### 4.2 圈数-对易子阶数对应【谱新增：代数定理】

**定理 3.2**（圈数-对易子阶数对应）。n 圈 β 函数的谱生成元为 n 阶迭代对易子：

$$\beta^{(n)} \;\longleftrightarrow\; \mathrm{ad}_G^n(A_t) = [G,[G,\cdots[G,A_t]\cdots]],$$

一阶对易子生成单圈 β，DS 顶点减除对 n ≥ 2 提供圈间修正（Paper 5 §6 匹配模式）。

*证明要点*。谱流方程 dA_t/dt = [G,A_t] 的 n 阶迭代展开（BCH 结构）对应 n 阶对易子；单圈 = 一阶对易子（谱流方程一阶项），双圈 = 二阶 + DS 顶点修正，三圈 = 三阶 + 推广 DS 减除。数值锚点：`paper31_threeloop_beta.py` 12/12 匹配。□

### 4.3 匹配数值【既有：Paper 5 §6 + Paper 12 §8】

| 圈数 | 谱流项 | SM 值 | 匹配 |
|:--:|:--|:--|:--:|
| 单圈 | 一阶对易子 | β⁽¹⁾ = −(11C_A−4T_Rn_f)/3·g³/16π² | 1.000000 |
| 双圈 | 二阶 + DS 顶点 | paper27_fermion_twoloop.py | ✅ |
| 三圈 | 三阶 + 推广 DS | paper31_threeloop_beta.py | 12/12 |
| U(1) | ΣY² = 41/10（GUT 归一化） | β₁ = (41/10)·g₁³/16π² | ✅ |
| 引力三圈 | 对易子结构 | paperX_graviton_3loop / Paper 12 §10 | ✅ |

---

## 5. T4：EFT 层级（谱静默单向转化严格化）【谱新增】

### 5.1 谱静默层级【既有：Paper I §8.3.3 定性 + Paper XIX 四层静默】

谱静默 = 高能自由度在低能有效理论中的系统性约化（S1–S4 四层：态射/对象/谱/辫子）。

### 5.2 EFT 层级严格定理【谱新增】

**定理 4.1**（EFT 层级谱静默定理）。设 $A_{\mathrm{UV}}$ 为 UV 谱生成元，能标积分 $\int_{m}^{M_{\mathrm{Pl}}}$ 的谱静默约化（S 因子逐层吸收）给出 IR 有效理论 $A_{\mathrm{IR}} = P_{\mathrm{IR}} A_{\mathrm{UV}} P_{\mathrm{IR}}$，误差由静默层级控制：

$$\|A_{\mathrm{UV}} - A_{\mathrm{IR}}\|_{\mathrm{HS}} \lesssim \left(\frac{m}{M_{\mathrm{Pl}}}\right)^{\delta_{\mathrm{silence}}} \cdot \|A_{\mathrm{UV}}\|$$

其中 $\delta_{\mathrm{silence}}$ 为静默层级指数（Paper XIX §15 谱静默机制）。

*证明要点*。重正化群积分将高于阈值 m 的模式逐层静默（积分掉），HS 范数误差由被积分模式的谱权重控制——谱截断 Λ_max 保证权重指数压制（Wick 旋转后欧氏积分收敛）。□

### 5.3 与 P0-2 验收的衔接

拉氏量 → Feynman（T1）→ 圈图谱积分（T1/T2）→ 谱截断正则化（T2）→ 谱流 β 函数（T3）→ EFT 层级（T4）——六段链条闭合。

---

## 6. 形式化路线（Lean + Agda）

| 编号 | 定理 | 层 | 状态 |
|:--|:----|:--|:----|
| F1 | ad_G 保 Hermitian（G 反 Hermitian → [G,A] 自伴）——一阶对易子 = 单圈 β 谱生成元 | Lean 矩阵 / Agda LinOp | 本篇新增 |
| F2 | n 阶迭代对易子保 Hermitian（归纳）——圈数-对易子阶数对应的代数基础 | Lean / Agda | 本篇新增 |
| F3 | 谱流保 Hermitian + 保谱（引用 InflationDynamics / SpectralDynamics） | Lean | 引用 |
| F4 | 谱截断积分有限性（T3 fc-integral 层） | Agda（T3 依赖） | 依赖 T3 |

**验收**：`lake build`（Lean）、`agda Everything.agda`（Agda）全量通过。

---

## 7. 数值验证清单（paperX_rg_chain.py）

| 节 | 检查项 | 判据 |
|:--|:------|:-----|
| §1 | 谱 Feynman 规则（λφ⁴ 传播子/顶点 + 规范顶点） | 解析一致 |
| §2 | 谱正则化：I_Sp = ∫dλ/(λ−m²)² 有限 | 与 1/(Λ−m²) 解析值一致 |
| §3 | 谱流 → β 函数：λφ⁴ 单圈 | β = 3λ²/16π² 精确 |
| §4 | 规范单圈 β（SU(3)/SU(2)/U(1)） | (41/10, −19/6, −7) 精确 |
| §5 | 三圈 DS 匹配（复用 paper31 结构） | 12/12 |
| §6 | EFT 层级静默转化 | 误差 < 5% |

---

## 8. 诚实边界与未决问题

1. **能标-时间对偶的严格证明**：定理 3.1 的 $d\ln\mu = dt$ 对偶为结构对应（Paper 5 §6 量子化匹配），非独立公理——其物理内容由 β 匹配数值锁定。
2. **Berry 相位项**：定理 3.1 证明中本征基变化项为零需瞬时本征基假设，严格证明登记为后续。
3. **谱静默误差指数 δ_silence**：定理 4.1 的 δ_silence 由 Paper XIX 静默机制给出量级，精确值需完整静默层级形式化。
4. **非微扰重整化**：本文覆盖微扰链（至三圈），非微扰（瞬子/禁闭区）由 P0-1 禁闭谱判据衔接。

---

## 版本记录

| 版本 | 日期 | 变更 |
|:--:|:--|:--|
| v0.1 | 2026-08-03 | 初版。T1 谱 Feynman 完整化、T2 谱正则化、T3 谱流→β 函数统一定理、T4 EFT 层级 + 形式化路线 + 数值清单。 |
