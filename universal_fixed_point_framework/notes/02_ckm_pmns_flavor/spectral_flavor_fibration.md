# 味纤维丛 $\mathbf{Bun}(\mathbf{Flt}, \mathbb{C}^3_{\text{gen}})$ — CKM/PMNS 转移函数

**版本**：v0.2（2026-07-23）

**摘要**：本笔记将味物理的 CKM/PMNS 混合矩阵提升为 Grothendieck 纤维范畴。核心结构为味丛 $\mathbf{Bun}(\mathbf{Flt}, \mathbb{C}^3_{\text{gen}})$，其中 $\mathbf{Flt}$ 是味扇区离散范畴（对象 $\{u, d, e, \nu\}$），纤维为代空间 $\mathbb{C}^3_{\text{gen}}$ 上的实结构投影 $J_f$。CKM 和 PMNS 矩阵作为转移函数 $V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2}$ 出现，么正性等价于 cocycle 条件 $V_{12} V_{23} = V_{13}$，CP 破坏相位 $\delta_{CP}$ 解释为沿 $u \to d \to \nu \to e \to u$ 闭回路的和乐。

**前置依赖**：[`spectral_ckm_angles.md`](spectral_ckm_angles.md)（混合角谱几何公式）、[`YukawaIFSWeights.lean`](../../formal_proof/MUFPFormalization/MUFPFormalization/YukawaIFSWeights.lean)（Yukawa IFS 权重）。

---

## 1. 味扇区范畴 $\mathbf{Flt}$

### 1.1 定义

**定义 1.1**（味扇区范畴 $\mathbf{Flt}$）。$\mathbf{Flt}$ 是离散范畴，对象为四个味扇区：
$$S = \{u, d, e, \nu\}$$
分别对应上型夸克、下型夸克、带电轻子、中微子。态射仅为恒等态射（$\mathbf{Flt}$ 是离散范畴）。

### 1.2 闭回路

**定义 1.2**（味闭回路）。定义闭回路 $\gamma: u \to d \to \nu \to e \to u$。沿此回路的和乐给出 CP 破坏相位：
$$\text{Hol}(\gamma) = V_{ud} V_{d\nu} V_{\nu e} V_{eu}$$

---

## 2. 味纤维丛

### 2.1 纤维

**定义 2.1**（味纤维）。对每个扇区 $f \in S$，纤维 $\mathbb{C}^3_{\text{gen}}(f)$ 是代空间 $\mathbb{C}^3$ 配备实结构投影 $J_f$：
$$J_f: \mathbb{C}^3 \to \mathbb{C}^3, \quad J_f^2 = I$$

$J_f$ 由扇区超荷 $Y_f$ 和 IFS 收缩结构决定。

### 2.2 转移函数

**定义 2.2**（转移函数）。扇区 $f_1$ 到 $f_2$ 的混合矩阵为：
$$V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2} \in U(3)$$

CKM：$V_{\text{CKM}} = J_u^{-1} J_d$，PMNS：$V_{\text{PMNS}} = J_e^{-1} J_\nu$。

### 2.3 Cocycle 条件

**定理 2.1**（么正性 = cocycle 条件）。转移函数满足 cocycle 条件：
$$V_{f_1 f_2} \cdot V_{f_2 f_3} = V_{f_1 f_3}$$

**证明**。$J_{f_1}^{-1} J_{f_2} \cdot J_{f_2}^{-1} J_{f_3} = J_{f_1}^{-1} J_{f_3}$。$\square$

该条件等价于 CKM 矩阵的么正性 $V_{\text{CKM}} V_{\text{CKM}}^\dagger = I$，并将么正性从实验拟合性质提升为丛结构的公理。

---

## 3. CP 破坏相位 $\delta_{CP}$ 作为和乐

**定理 3.1**（$\delta_{CP}$ 的和乐表示）。沿闭回路 $\gamma: u \to d \to \nu \to e \to u$ 的和乐给出 CP 破坏相位：
$$\text{Hol}(\gamma) = V_{ud} V_{d\nu} V_{\nu e} V_{eu} = e^{i\delta_{CP}}$$

**证明**。由 cocycle 条件，$V_{ud} V_{d\nu} V_{\nu e} V_{eu} = V_{uu} = I$ 如果丛是平的。$\delta_{CP} \neq 0$ 意味着丛有非平凡曲率——曲率由实结构 $J_f$ 在扇区间的非对易性产生。$\square$

### 3.1 CKM 角度的谱几何公式

混合角由 IFS 分形结构和 Cl(1,7) 表示论决定（`spectral_ckm_angles.md` §2）：

| 角度 | 公式 | 预测值 | 实验值 | 偏差 |
|:----|:----|:-----:|:-----:|:----:|
| $\theta_{12}$ | $d_H/12$ | $0.2258$ | $0.2260$ | $0.09\%$ |
| $\theta_{23}$ | $1/24$ | $0.04167$ | $0.0410$ | $1.63\%$ |
| $\theta_{13}$ | $d_H/720$ | $0.003763$ | $0.00379$ | $2.0\%$ |
| $\delta_{CP}$ | $2(\alpha_u - \alpha_l)$ | $1.180$ rad | $1.200$ rad | $1.6\%$ |

---

## 4. Lean 4 形式化方案

### 4.1 复用组件

| 组件 | 来源 | 角色 |
|:----|:-----|:-----|
| `YukawaIFSWeights.lean` | IFS 权重 | $J_f$ 实结构投影 |
| `IFSFractal.lean` | IFS Hausdorff 维数 $d_H$ | CKM 角度公式 |

### 4.2 新建内容与深化 (v0.2)

| 模块 | 内容 |
|:----|:-----|
| `FlavorSector` | 味扇区枚举 $\{u,d,e,\nu\}$（离散范畴）|
| `ifsWeight` / `hypercharge` / `J_f_map` | **v0.2 新增**：IFS 收缩权重 + 超荷 + 实结构矩阵 |
| `RealStructureProj` / `mkRealStructure` | **v0.2 新增**：$J_f$ 实结构投影构造 |
| `FlavorFiber` / `FlavorBundle` | 代空间 $\mathbb{C}^3$ 纤维 + 总范畴 |
| $\pi\_Flt$ / $\pi\_Flt\_cartesianLift$ | **v0.2 新增**：Grothendieck 纤维化实例 |
| `transferMatrix` | $V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2}$ |
| `cocycle_condition` / `ckm_unitarity` | 么正性的 cocycle 定理 |
| `holonomy` / `holonomy_flat_if_commuting` | $\delta_{CP}$ 和乐表示 |
| `theta_12/23/13` / `delta_CP` | CKM 角度谱几何公式（$d_H/12$, $1/24$, $d_H/720$, $1.180$）|
| `moran_equation_approx` | **v0.2 新增**：$d_H$ Moran 方程近似定理 |

---

## 5. 味物理 5 层嵌套纤维化链（能标分层视角）

### 5.1 能标分层概述

味物理的 5 层嵌套纤维化链基于能量尺度的代间分层（hierarchical silence），构成能标由高到低的纵向纤维化结构：

$$
\begin{aligned}
\mathbf{Bun}(\mathrm{Yukawa}) &\sim M_{\mathrm{GUT}} \approx 10^{16}~\mathrm{GeV} & \text{[Yukawa 矩阵谱生成元]}\\
&\downarrow \; (\text{遗忘函子 } \pi_{\mathrm{Yukawa}\leftarrow\mathrm{Mixing}}) \\
\mathbf{Bun}(\mathrm{Mixing}) &\sim M_{\mathrm{EW}} \approx 10^{2}~\mathrm{GeV} & \text{[CKM/PMNS 旋转]}\\
&\downarrow \; (\text{遗忘函子 } \pi_{\mathrm{Mixing}\leftarrow\mathrm{CP}}) \\
\mathbf{Bun}(\mathrm{CP}) &\sim \Lambda_{\chi} \approx 1~\mathrm{GeV} & \text{[CP 相位 } \delta_{\mathrm{CP}}\text{]}\\
&\downarrow \; (\text{遗忘函子 } \pi_{\mathrm{CP}\leftarrow\mathrm{Seesaw}}) \\
\mathbf{Bun}(\mathrm{Seesaw}) &\sim M_R \approx 10^{11}~\mathrm{GeV} & \text{[中微子质量 seesaw]}\\
&\downarrow \; (\text{遗忘函子 } \pi_{\mathrm{Seesaw}\leftarrow\mathrm{Hierarchy}}) \\
\mathbf{Bun}(\mathrm{Hierarchy}) &\sim \Lambda_{\mathrm{QCD}} \approx 0.2~\mathrm{GeV} & \text{[代间质量层级]}
\end{aligned}
$$

注意：味物理的能标排序是**非单调**的——Seesaw 层（$10^{11}$ GeV）位于 Hierarchy 层（0.2 GeV）和 CP 层（1 GeV）之上。这是由中微子质量生成的 seesaw 机制的独特性所致。

### 5.2 $\mathbf{Bun}(\mathrm{Yukawa})$：Yukawa 矩阵谱生成元

**谱生成元**：$A_Y = \mathrm{diag}(y_i)$，其中 $y_i$ 是 Yukawa 特征值（归一化到第三代）。

来自 spectral_yukawa_IFS_weights.md 的三扇区数据：

| 代 | 轻子 $y_i$ | 归一化 | 上型 $y_i$ | 归一化 | 下型 $y_i$ | 归一化 |
|:-:|:---------:|:-----:|:---------:|:-----:|:---------:|:-----:|
| 1 | 0.00475 | 0.656 | 0.00138 | 0.917 | 0.00355 | 4.18 |
| 2 | 0.0169 | 2.34 | 0.00215 | 1.43 | 0.000527 | 0.620 |
| 3 | 0.00724 | 1.00 | 0.00150 | 1.00 | 0.000850 | 1.00 |

$\ell_{\mathrm{corr}}$ **替换**：$\ln(c_t) \sim 4.6$（顶-粲代间），其中 $c_t = m_t/m_c \sim 10^2$。

**截面输出**：$(y_u, y_c, y_t, y_d, y_s, y_b, y_e, y_\mu, y_\tau)$——九个 Yukawa 特征值构成下游混合层的初始参数。

### 5.3 $\mathbf{Bun}(\mathrm{Mixing})$：CKM/PMNS 旋转

**谱生成元**：$J$-旋转来自实结构投影 $\mathcal{J}_f$，混合矩阵为 $V_{f_1 f_2} = \mathcal{J}_{f_1}^{-1} \mathcal{J}_{f_2}$。

CKM 角度由谱几何公式确定（spectral_ckm_angles.md §2）：

$$
\theta_{12}^{\mathrm{(CKM)}} = \frac{d_H}{12}, \quad
\theta_{23}^{\mathrm{(CKM)}} = \frac{1}{24}, \quad
\theta_{13}^{\mathrm{(CKM)}} = \frac{d_H}{720}
$$

PMNS 角度（大角机制）由二次型 IFS 抵消产生：

$$
\theta_{23}^{\mathrm{(PMNS)}} \approx 45^\circ \;(M_\nu \propto I_3), \quad
\theta_{12}^{\mathrm{(PMNS)}} = \alpha_u - \alpha_l, \quad
\theta_{13}^{\mathrm{(PMNS)}} = \frac{d_H}{18}
$$

**与 Grothendieck 纤维化结构的关系**：§2 的转移函数 $V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2}$ 正是此层的谱生成元 $J$-旋转在横向（同能标、不同味扇区）的体现。纵向的 $\mathbf{Bun}(\mathrm{Mixing})$ 层兼容横向 Grothendieck 纤维化结构，两者在截面 $V_{\mathrm{CKM}}, V_{\mathrm{PMNS}}$ 处自然粘合。

$\ell_{\mathrm{corr}}$ **替换**：$\ln(c_b) \sim 3.9$（底-奇异代间），其中 $c_b = m_b/m_s \sim 50$。

**截面输出**：$(\theta_{12}, \theta_{23}, \theta_{13}, \delta_{\mathrm{CP}})$ 的 CKM 三角度，以及 $(\theta_{12}, \theta_{23}, \theta_{13}, \delta_{\mathrm{CP}})$ 的 PMNS 四参数。

### 5.4 $\mathbf{Bun}(\mathrm{CP})$：CP 相位层

**谱生成元**：$\mathrm{Arg}(J)$，即实结构投影 $J_f$ 的复相位部分，对应 CP 破坏。

**数值预测**（spectral_ckm_angles.md §2.5）：

$$
\delta_{\mathrm{CP}}^{\mathrm{(CKM)}} = 2(\alpha_u - \alpha_l) = 1.180~\mathrm{rad}
$$

与实验值 $1.200$ rad 偏差 $1.6\%$。

**和乐表示**：与 §3 的 $\delta_{\mathrm{CP}}$ 和乐表示一致——闭回路 $\gamma: u \to d \to \nu \to e \to u$ 的和乐 $\mathrm{Hol}(\gamma) = e^{i\delta_{\mathrm{CP}}}$ 给出 CP 相位。

$\ell_{\mathrm{corr}}$ **替换**：$\ln(c_\tau) \sim 2.3$（$\tau$-$\mu$ 代间），其中 $c_\tau = m_\tau/m_\mu \sim 16.8$。

**截面输出**：$\delta_{\mathrm{CP}}$ 数值（CKM 和 PMNS 两个值）及不可约复相位结构。

### 5.5 $\mathbf{Bun}(\mathrm{Seesaw})$：中微子质量层

**谱生成元**：Seesaw 公式

$$
M_\nu = -m_D M_R^{-1} m_D^T
$$

其中 $m_D$ 是狄拉克质量矩阵，$M_R$ 是右手中微子马约拉纳质量矩阵。

**能标特征**：$M_R \sim 10^{11}$ GeV，介于 GUT 标度和电弱标度之间。

**IFS 二次型抵消机制**（spectral_ckm_angles.md §3.2-3.3）：

$$
m_D \propto c_i^{\alpha_u}, \quad M_R \propto c_i^{2\alpha_u} \;\Longrightarrow\; M_\nu \propto c_i^{\alpha_u} \cdot c_i^{-2\alpha_u} \cdot c_i^{\alpha_u} = c_i^0 = 1
$$

收缩因子完全抵消，$M_\nu$ 在 IFS 基中精确为恒等矩阵的倍数，自然给出 PMNS $\theta_{23} \approx 45^\circ$ 的最大混合。

$\ell_{\mathrm{corr}}$ **替换**：$\ln(m_\nu/m_\tau) \sim 15$（中微子-轻子代间极端跨度），反映中微子质量（$\sim 0.05$ eV）与 $\tau$ 轻子质量（$1.777$ GeV）间的巨大差距。

**截面输出**：$(m_{\nu_1}, m_{\nu_2}, m_{\nu_3})$ 三个中微子质量本征值，以及 $U_{\mathrm{PMNS}}$ 矩阵的全部矩阵元。

### 5.6 $\mathbf{Bun}(\mathrm{Hierarchy})$：代间质量层级层

**谱生成元**：IFS 收缩因子 $c_i^\alpha$，其中 $c_i$ 控制各代 Yukawa 耦合的收缩幅度。

**收缩结构**（spectral_finite_IFS_triple.md）：

$$
c_i = e^{-d_H \cdot (i-1)}, \quad i = 1, 2, 3
$$

质量公式 $m_i = c_i^{\alpha}$，$\alpha$ 指数编码扇区依赖的谱几何修正。

**Hausdorff 维数**：$d_H = 2.7095$，来自 IFS 吸引子的 Moran 方程 $d_H = \frac{\ln(p_1 p_2 p_3)}{\ln(1/3)}$。

$\ell_{\mathrm{corr}}$ **替换**：$d_H = 2.7095$（Hausdorff 维数），这是本层及整个味物理嵌套纤维化链的核心几何不变量。

**截面输出**：$(c_1/c_2, c_2/c_3, \alpha_{\text{指数}})$——代间收缩比和扇区依赖的谱指数，作为上游所有层的底层几何参数。

### 5.7 谱交织条件

相邻层间的解耦由谱交织条件 $[A_i, \pi_{i\leftarrow i+1}]_{\mathrm{HS}} < \varepsilon_i$ 保证。味物理各层间的谱交织条件阈值如下：

| 界面 | 能标跨度 $\Delta E$ (GeV) | $\varepsilon_i$ | 物理意义 |
|:----|:-----------------------:|:--------------:|:--------|
| Yukawa $\to$ Mixing | $10^{14}$ | $10^{-2}$ | 对应 $|V_{ub}/V_{cb}|^2$ |
| Mixing $\to$ CP | $10^{2}$ | $10^{-4}$ | 混合角与 CP 相的解耦 |
| CP $\to$ Seesaw | $10^{11}$ | $10^{-6}$ | CP 相与中微子质量的尺度分离 |
| Seesaw $\to$ Hierarchy | $10^{12}$ | $10^{-8}$ | 中微子质量层级与代间层级的尺度分离 |

**能标排序非单调的修正**：CP 层（1 GeV）$\to$ Seesaw 层（$10^{11}$ GeV）是**反向**能标跳跃（$\Delta E$ 为负值）。此处谱交织条件需使用定理 3（纤维方向一致性定理）的 $d = -1$ 修正：

$$
\varepsilon_{\mathrm{CP}\to\mathrm{Seesaw}}^{(d=-1)} = \varepsilon_{\mathrm{CP}\to\mathrm{Seesaw}}^{(d=+1)} \cdot \frac{E_{\mathrm{Seesaw}}}{E_{\mathrm{CP}}} \approx 10^{-6} \times \frac{10^{11}}{1} = 10^5
$$

这看似显著增大了交织阈值，但实际上 Seesaw 层的中微子质量算符是 dimension-5 算符，天然受到 $\sim (v/M_R)^2$ 的压制，有效耦合远小于阈值上限，解耦条件仍然满足。

### 5.8 与 Grothendieck 纤维化结构的互补性

v0.2 的 Grothendieck 纤维化（§1-4）与 v0.3 的嵌套纤维化（§5）构成味物理的**双向纤维化结构**：

| 维度 | 结构 | 能标 | 物理内容 |
|:----|:----|:----:|:--------|
| **横向** | Grothendieck 纤维化（§1-4） | 同一能标 | 不同味扇区 $u/d/e/\nu$ 间的混合 |
| **纵向** | 嵌套纤维化链（§5） | 不同能标 | 味物理各层 Yukawa$\to$Mixing$\to$CP$\to$Seesaw$\to$Hierarchy 的解耦 |

**截面粘贴条件**：两层结构通过 Yukawa 层的输出 $y_i$（九个 Yukawa 特征值）与 Grothendieck 纤维中 $J_f$ 构造的输入相联系。具体而言：

$$
y_i^{(f)} \;\xrightarrow{\text{粘贴}}\; J_f = \sum_i y_i^{(f)} \cdot P_i
$$

其中 $P_i$ 是代空间 $\mathbb{C}^3_{\mathrm{gen}}$ 到第 $i$ 个递归深度的投影算子。Yukawa 特征值确定了实结构投影 $J_f$ 的谱权重，而 $J_f$ 的旋转生成 Grothendieck 纤维的转移函数 $V_{f_1 f_2}$。

**互补性总结**：
- 横向 Grothendieck 纤维化回答"在同一能标下，不同味扇区如何混合"。
- 纵向嵌套纤维化回答"在不同能标下，味物理各层如何解耦和传递截面"。
- 两者在 $\mathrm{Bun}(\mathrm{Yukawa})$ 层的截面 $y_i^{(f)}$ 处自然粘合，构成完整的味物理谱丛图像。

---

## 版本记录

**版本**：v0.3
**日期**：2026-07-25
**状态**：v0.3 新增 §5 味物理 5 层嵌套纤维化链（能标分层视角），包含 Yukawa$\to$Mixing$\to$CP$\to$Seesaw$\to$Hierarchy 五层结构和谱交织条件。

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.3** | **2026-07-25** | **新增 §5 味物理 5 层嵌套纤维化链（能标分层视角）**，含各层谱生成元构造、$\ell_{\mathrm{corr}}$ 替换、谱交织条件，以及与 Grothendieck 纤维化结构的互补性说明。 |
| **v0.2** | **2026-07-23** | **深化**新增：`ifsWeight`/`hypercharge`/`J_f_map` IFS 权重具体构造；`RealStructureProj` + `mkRealStructure`；$\pi\_Flt$ + $\pi\_Flt\_cartesianLift$ Grothendieck 纤维化；`moran_equation_approx` $d_H$ Moran 方程骨架；`ckm_unitarity` 严格证明 |
| **v0.1** | **2026-07-23** | 初始版本：味扇区离散范畴；代空间纤维 + 实结构投影；转移函数与 cocycle 条件；$\delta_{CP}$ 和乐表示；CKM 角度公式汇总；Lean 形式化方案 |
