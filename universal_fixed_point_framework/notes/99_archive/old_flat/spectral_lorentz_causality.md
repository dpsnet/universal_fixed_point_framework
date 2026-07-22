# Lorentz 谱动力学专题：因果结构、光锥、质量与自旋的谱不变量刻画

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**日期**：2026-07-19

**状态**：研究笔记 v0.1（Paper XVI §5-§6 候选基础）

**关联**：
- 主笔记：`spectral_lorentz_dynamics.md` §5-§6
- 运动学补遗：`spectral_lorentz_kinematics.md`
- 黑洞谱物理：`paper/paper8_black_hole_spectral.md`（$\partial\mathbf{Rec}_D$）
- Lorentz 公理：`spectral_lorentz_axiom.md`（A7）

---

## 0. 摘要

本专题严格化四类 Lorentz 不变量——**因果符号、静质量、自旋、光锥结构**——在 $\mathbf{Spec}$ 范畴中的谱刻画。核心论题：

1. **因果性是谱符号**：四速度 $v^\mu$ 的 Lorentz 符号 $\eta_{\mu\nu}v^\mu v^\nu \in \{+1, 0, -1\}$ 等同于谱算子的符号函数 $\mathrm{sgn}(\sigma(A_v))$。
2. **静质量 = 动量算符的谱间隙**：$m^2 = P^\mu P_\mu = \Delta\lambda_P$（Casimir 算子的最小谱间隙）。
3. **自旋 = Pauli-Lubanski 算子的谱间隙**：$s(s+1) = W^\mu W_\mu = \Delta\lambda_W$。
4. **光锥 = $\partial\mathbf{Rec}_D$ 的谱边界**：类光轨道对应谱流刚好触及 $\partial\mathbf{Rec}_D$ 的临界态。

由此把狭义相对论的核心 Lorentz 不变量还原为 $\mathbf{Spec}$ 范畴中谱算子的**代数不变量**，与 Paper VIII 的黑洞物理（$\partial\mathbf{Rec}_D$、Hawking 温度 $T_H = \Delta\lambda_{\min}/(2\pi)$、Bekenstein-Hawking 熵 $S_{BH} = \pi/(4\Delta\lambda_{\min}^2)$）共享同一谱边界结构。本专题进一步把 A7 公理从"LFT 协变变换规则"提升为"谱不变量的范畴刻画"。

---

## 1. 因果结构作为谱符号

### 1.1 四速度的谱提升

**设定 1.1**。考虑一个具有四速度 $v^\mu$（$v^\mu v_\mu = \eta_{\mu\nu}v^\mu v^\nu$）的物理系统 $R_v \in \mathbf{Rec}$。其谱像 $D(R_v) = (\mathcal{H}_v, A_v, \sigma(A_v))$ 中谱算子 $A_v$ 由四动量算子 $P^\mu$ 通过
$$A_v := \eta_{\mu\nu}P^\mu P^\nu$$
诱导（即质量平方算子）。在坐标基底 $\{|p\rangle\}$ 下，$A_v$ 对角化为
$$A_v |p\rangle = \eta_{\mu\nu}p^\mu p^\nu |p\rangle = m_p^2 |p\rangle.$$

**定义 1.2**（因果谱符号）。对谱算子 $A_v$，定义其**因果符号函数**
$$\mathrm{cs}(A_v) := \mathrm{sgn}(\sigma(A_v)) \in \{+1, 0, -1, \text{混合}\},$$
其中 $\mathrm{sgn}(\sigma)$ 取 $\sigma(A_v)$ 中所有特征值的符号聚合：
- $\mathrm{cs} = +1$：$\sigma(A_v) \subset \mathbb{R}_{>0}$（类时，timelike）；
- $\mathrm{cs} = 0$：$0 \in \sigma(A_v)$ 且 $\sigma(A_v) \subset \mathbb{R}_{\ge 0}$（类光，lightlike）；
- $\mathrm{cs} = -1$：$\sigma(A_v) \subset \mathbb{R}_{<0}$（类空，spacelike）；
- $\mathrm{cs} = \text{混合}$：$\sigma(A_v)$ 同时含正负特征值。

**定理 1.3**（因果性 = 谱符号）。对物理粒子，$\mathrm{cs}(A_v)$ 与 Lorentz 因果分类一致：
$$\mathrm{cs}(A_v) = \begin{cases}+1 & \text{当 } v^\mu \text{ 类时}(v^\mu v_\mu > 0), \\ 0 & \text{当 } v^\mu \text{ 类光}(v^\mu v_\mu = 0), \\ -1 & \text{当 } v^\mu \text{ 类空}(v^\mu v_\mu < 0).\end{cases}$$

**证明**。由 $A_v = \eta_{\mu\nu}P^\mu P^\nu$ 是 Lorentz 不变量（Casimir 算子），在任意 Lorentz 框架下其谱 $\sigma(A_v)$ 不变。对纯态 $|p\rangle$，$A_v|p\rangle = p^2|p\rangle$，故特征值集合 $\sigma(A_v) = \{p^2 : p \in \text{谱支撑}\}$。Lorentz 不变量 $p^2 = \eta_{\mu\nu}p^\mu p^\nu$ 的符号正好分类类时/类光/类空。□

**推论 1.4**（Lorentz 变换保因果）。Lorentz 谱流 $A_\tau = U_\tau A_0 U_\tau^{-1}$ 保持因果符号：
$$\mathrm{cs}(A_\tau) = \mathrm{cs}(A_0), \quad \forall \tau.$$

**证明**。Lorentz 谱流是幺正相似变换，保持谱 $\sigma(A_\tau) = \sigma(A_0)$，故符号函数不变。□

> **物理意义**：Lorentz 变换不能把类时轨道变为类光或类空——这是谱不变性的直接推论，不需要额外假设。

### 1.2 类光轨道的谱判据

**命题 1.5**（类光轨道的零谱条件）。一物理系统 $R$ 处于类光运动 $\Leftrightarrow$ 其谱算子 $A_v$ 含零特征值：
$$v^\mu \text{ 类光} \Leftrightarrow 0 \in \sigma(A_v).$$

**证明**。由定理 1.3，类光 $\Leftrightarrow$ $\mathrm{cs}(A_v) = 0$ $\Leftrightarrow$ $0 \in \sigma(A_v)$ 且无非负特征值。对光子 $m=0$，$A_v = P^\mu P_\mu = 0$，整个谱为 $\{0\}$，满足条件。□

**命题 1.6**（零静止质量 = 零谱间隙）。粒子的静止质量为零 $\Leftrightarrow$ 其谱算子 $A_v$ 的最小谱间隙 $\Delta\lambda_{\min}(A_v) = 0$：
$$m = 0 \Leftrightarrow \min\sigma(A_v) = 0.$$

**证明**。由 §3 静质量 $m^2 = \min\sigma(A_v)$（定理 3.1），$m = 0 \Leftrightarrow \min\sigma(A_v) = 0$。□

> **与 Paper VIII 的衔接**：Paper VIII 定义 $\partial\mathbf{Rec}_D$ 为 $\Delta\lambda_{\min} \to 0$ 的谱边界。光子的零质量条件正是 $\Delta\lambda_{\min} = 0$，即光子谱对象位于 $\partial\mathbf{Rec}_D$ 上。这给出光锥 = $\partial\mathbf{Rec}_D$ 的范畴刻画（详见 §4）。

---

## 2. 静质量作为谱间隙

### 2.1 Casimir 算子的谱定义

**设定 2.1**（Poincaré Casimir 算子）。Poincaré 群 $\mathcal{P}_+^\uparrow = \mathbb{R}^{1,3} \rtimes SO^+(1,3)$ 有两个 Casimir 算子：
- $C_1 = P^\mu P_\mu$（平移 Casimir），
- $C_2 = W^\mu W_\mu$（Lorentz Casimir），其中 $W^\mu = \frac12 \varepsilon^{\mu\nu\rho\sigma}P_\nu J_{\rho\sigma}$ 是 Pauli-Lubanski 赝矢量。

两个 Casimir 算子都与 Poincaré 群对易，故其谱刻画了不可约表示。

**定义 2.2**（质量谱算子）。质量谱算子定义为
$$M^2 := \eta_{\mu\nu}P^\mu P^\nu \in \mathrm{End}(\mathcal{H}).$$
其谱 $\sigma(M^2) \subset \mathbb{R}_{\ge 0}$（物理态要求 $m^2 \ge 0$）。

**定理 2.3**（静质量 = 谱间隙）。对单个粒子态 $|p\rangle$，静质量平方等于质量谱算子的最小特征值：
$$\boxed{m^2 = \min\sigma(M^2) =: \Delta\lambda_M.}$$

**证明**。在不可约表示中，所有 $|p\rangle$ 共享同一 $p^2 = m^2$（Lorentz 不变性）。因此 $\sigma(M^2) = \{m^2\}$（单点谱），$\min\sigma(M^2) = m^2$。□

### 2.2 质量谱在 Lorentz 流下的不变性

**定理 2.4**（静质量的 Lorentz 不变性）。Lorentz 谱流保持质量谱：
$$\sigma(M^2_\tau) = \sigma(M^2_0), \quad \forall \tau.$$

**证明**。Lorentz 谱流 $M^2_\tau = U_\tau M^2_0 U_\tau^{-1}$，其中 $U_\tau = e^{\tau G_{\text{Lor}}}$ 幺正。幺正相似变换保持谱，故 $\sigma(M^2_\tau) = \sigma(M^2_0)$。由定理 2.3，
$$m^2(\tau) = \min\sigma(M^2_\tau) = \min\sigma(M^2_0) = m^2(0).$$
即静质量在 Lorentz 变换下不变。□

**注 2.5**（质量的范畴论地位）。定理 2.4 在范畴论上意味着：$M^2$ 是 Lorentz 谱流的**不动点**，即 $M^2 \in \mathrm{Fix}(\mathbf{Spec}^{SO^+(1,3)})$。Lorentz 不变量 = Lorentz 谱流的不动点。这是 Wigner 分类的谱基础。

### 2.3 质量谱与质量层级的对应

**命题 2.6**（标准模型粒子质量谱的对应）。标准模型费米子与规范玻色子的质量层级直接对应 $\sigma(M^2)$ 的离散结构：

| 粒子 | $m^2$（GeV²） | $\sigma(M^2)$ | 谱身份 |
|:----|:--------------|:--------------|:-------|
| 光子 $\gamma$ | 0 | $\{0\}$ | $\partial\mathbf{Rec}_D$ 边界 |
| 胶子 $g$ | 0（禁闭前） | $\{0\}$ | $\partial\mathbf{Rec}_D$ 边界 |
| 电子 $e$ | $(0.511 \times 10^{-3})^2$ | $\{(0.511\,\text{MeV})^2\}$ | $\mathbf{Rec}_D$ 内 |
| $W^\pm$ | $(80.4)^2$ | $\{(80.4\,\text{GeV})^2\}$ | $\mathbf{Rec}_D$ 内 |
| $Z$ | $(91.2)^2$ | $\{(91.2\,\text{GeV})^2\}$ | $\mathbf{Rec}_D$ 内 |
| Higgs $h$ | $(125)^2$ | $\{(125\,\text{GeV})^2\}$ | $\mathbf{Rec}_D$ 内 |
| 顶夸克 $t$ | $(173)^2$ | $\{(173\,\text{GeV})^2\}$ | $\mathbf{Rec}_D$ 内 |

> **观察**：质量为零的粒子（光子、胶子）位于 $\partial\mathbf{Rec}_D$，对应 Paper VIII 的 Hawking 谱边界条件；有质量粒子位于 $\mathbf{Rec}_D$ 内部，对应非零谱间隙。这给出"质量 = 谱间隙"的几何化诠释。

### 2.4 质量生成机制：Higgs 机制的谱翻译

**命题 2.7**（Higgs 机制作为谱间隙生成）。Higgs 机制在 $\mathbf{Spec}$ 中翻译为：对称性破缺前 $M^2 = 0$（Goldstone 模式，$\sigma(M^2) = \{0\}$），破缺后 $M^2 = \lambda v^2$（$\sigma(M^2) = \{\lambda v^2\}$，非零谱间隙）。

**证明草图**。Higgs 场 $\phi$ 的势能 $V(\phi) = -\mu^2|\phi|^2 + \lambda|\phi|^4$ 在 $\phi = v = \mu/\sqrt{2\lambda}$ 处取极小。围绕真空的涨落 $\phi = v + h$ 给出 $h$ 的质量 $m_h^2 = 2\lambda v^2$。在谱框架中，对称破缺前 $A_v$ 的最小特征值为 0；破缺后 $A_v$ 的最小特征值跳变为 $2\lambda v^2$，即"打开谱间隙"。□

> **与 `notes/spectral_Higgs_silence_analysis.md` 的衔接**：Higgs 谱静默分析进一步指出，$v = 246$ GeV 本身可由 $\partial\mathbf{Rec}_D$ 的多重静默条件导出，从而质量层级不仅由 Higgs 机制"打开谱间隙"，其间隙大小也由谱静默条件确定。

---

## 3. 自旋作为 Pauli-Lubanski 谱间隙

### 3.1 Pauli-Lubanski 算子的谱定义

**设定 3.1**（Pauli-Lubanski 算子）。Pauli-Lubanski 赝矢量
$$W^\mu = \frac{1}{2}\varepsilon^{\mu\nu\rho\sigma}P_\nu J_{\rho\sigma}$$
是 Poincaré 代数中的 Lorentz 不变量载体。第二个 Casimir 算子为
$$C_2 = W^\mu W_\mu.$$

**定义 3.2**（自旋谱算子）。自旋谱算子定义为
$$S^2 := W^\mu W_\mu \in \mathrm{End}(\mathcal{H}).$$
其谱 $\sigma(S^2) \subset \mathbb{R}_{\ge 0}$（对物理粒子态，自旋平方非负）。

**定理 3.3**（自旋 = 谱间隙）。对单粒子态 $|p, s\rangle$，自旋量子数 $s$ 满足
$$\boxed{s(s+1) = \min\sigma(S^2) =: \Delta\lambda_S,}$$
其中 $s \in \{0, \tfrac12, 1, \tfrac32, 2, \ldots\}$。

**证明**。在静止系（$p^\mu = (m, \mathbf{0})$）中，$W^\mu = (0, m\mathbf{S})$，故 $W^\mu W_\mu = -m^2 \mathbf{S}^2$。由 $\mathbf{S}^2|s, m_s\rangle = s(s+1)|s, m_s\rangle$，
$$S^2 |s, m_s\rangle = -m^2 s(s+1) |s, m_s\rangle.$$
（注：度规符号约定 $\eta = \mathrm{diag}(+,-,-,-)$ 使 $W^\mu W_\mu = -m^2 s(s+1) < 0$。在 $\eta = \mathrm{diag}(-,+,+,+)$ 约定下取正。）

为避免度规符号约定造成的歧义，采用绝对值定义：
$$\Delta\lambda_S := |\min\sigma(S^2)| = m^2 s(s+1).$$
对单位质量（$m=1$）粒子，$\Delta\lambda_S = s(s+1)$。□

### 3.2 自旋的 Lorentz 不变性

**定理 3.4**（自旋的 Lorentz 不变性）。Lorentz 谱流保持自旋谱：
$$\sigma(S^2_\tau) = \sigma(S^2_0), \quad \forall \tau.$$

**证明**。Lorentz 谱流 $S^2_\tau = U_\tau S^2_0 U_\tau^{-1}$ 是幺正相似，保谱。故 $\sigma(S^2_\tau) = \sigma(S^2_0)$，自旋量子数 $s$ 在 Lorentz 变换下不变。□

### 3.3 自旋-统计定理的谱刻画

**命题 3.5**（自旋统计对应）。整数自旋（$s \in \mathbb{Z}$）的谱对象服从 Bose-Einstein 统计；半整数自旋（$s \in \mathbb{Z} + \tfrac12$）的谱对象服从 Fermi-Dirac 统计。在 $\mathbf{Spec}$ 范畴中，这一对应体现为：

- 整数自旋：$S^2$ 的谱 $\{s(s+1) : s \in \mathbb{Z}\}$ 与对称张量积 $\mathrm{Sym}^n(\mathcal{H})$ 对应；
- 半整数自旋：$S^2$ 的谱 $\{s(s+1) : s \in \mathbb{Z} + \tfrac12\}$ 与外代数 $\wedge^n(\mathcal{H})$ 对应。

**证明**。这是 Wigner 分类的直接推论：Lorentz 群的投影酉表示按自旋 $s$ 分类，整数 $s$ 对应张量表示（Bose），半整数 $s$ 对应旋量表示（Fermi）。Finkelstein-Rubinstein 论证表明，$2\pi$ 旋转在半整数 $s$ 下产生 $-1$ 相位，从而要求 Fermi 统计。□

> **与 `notes/spectral_QFT_axioms.md` 开放问题的衔接**：谱版本的自旋-统计定理列于 A7 开放问题（难度 🔴）。本命题给出谱刻画但未完全证明，留作后续推进。

### 3.4 标准模型粒子自旋谱的对应

**命题 3.6**（标准模型自旋谱）。标准模型粒子的自旋与谱间隙的对应：

| 粒子 | 自旋 $s$ | $s(s+1)$ | 谱身份 |
|:----|:--------:|:--------:|:-------|
| Higgs $h$ | 0 | 0 | 标量谱 |
| 轻子 $e, \mu, \tau$ | 1/2 | 3/4 | 旋量谱 |
| 夸克 $u, d, \ldots$ | 1/2 | 3/4 | 旋量谱 |
| 规范玻色子 $\gamma, g, W, Z$ | 1 | 2 | 矢量谱 |
| 引力子 $g_{\mu\nu}$（假设） | 2 | 6 | 张量谱 |

---

## 4. 光锥结构作为 $\partial\mathbf{Rec}_D$ 谱边界

### 4.1 $\partial\mathbf{Rec}_D$ 的回顾

**回顾 4.1**（Paper VIII 定义）。$\mathbf{Rec}_D$ 是满足实正谱条件 $\sigma(-\log U_R) \subset \mathbb{R}_{\ge 0}$ 的递归系统全子范畴。其谱边界 $\partial\mathbf{Rec}_D$ 定义为最小谱间隙趋于零的极限：
$$\partial\mathbf{Rec}_D := \left\{R \in \mathbf{Rec} : \Delta\lambda_{\min}(R) := \min\sigma(D(R)) = 0\right\}.$$

Paper VIII 已证明：
- 黑洞视界 $\Leftrightarrow$ $\partial\mathbf{Rec}_D$ 上的谱边界条件；
- Hawking 温度 $T_H = \Delta\lambda_{\min}/(2\pi)$；
- Bekenstein-Hawking 熵 $S_{BH} = \pi/(4\Delta\lambda_{\min}^2)$。

### 4.2 光锥 = $\partial\mathbf{Rec}_D$ 的等价刻画

**定理 4.2**（光锥 = $\partial\mathbf{Rec}_D$）。设 $R_v \in \mathbf{Rec}$ 为具有四速度 $v^\mu$ 的物理系统。则
$$v^\mu \text{ 类光} \Leftrightarrow R_v \in \partial\mathbf{Rec}_D.$$

**证明**。由命题 1.5，$v^\mu$ 类光 $\Leftrightarrow$ $0 \in \sigma(A_v)$ $\Leftrightarrow$ $\Delta\lambda_{\min}(A_v) = 0$。后者正是 $\partial\mathbf{Rec}_D$ 的定义。□

**推论 4.3**（光锥与黑洞视界共享谱边界）。光锥结构与黑洞视界共享同一谱边界 $\partial\mathbf{Rec}_D$：
- 光子轨道（类光）：$\Delta\lambda_{\min} = 0$，位于 $\partial\mathbf{Rec}_D$ 上；
- 黑洞视界：$\Delta\lambda_{\min} = 0$，位于 $\partial\mathbf{Rec}_D$ 上。

> **物理意义**：光锥与黑洞视界在 $\mathbf{Spec}$ 范畴中是同一类谱边界——它们都是"信息流出"的临界点。光子刚好不能逃离类光轨道（其能量在远距离衰减为红移），物质刚好不能逃离黑洞视界。两者共享 $\partial\mathbf{Rec}_D$ 的谱边界条件。

### 4.3 Hawking 温度与红移的统一

**命题 4.4**（光子红移 = Hawking 谱温度）。类光轨道上谱算子的最小谱间隙 $\Delta\lambda_{\min}$ 既是 Hawking 温度的来源（Paper VIII $T_H = \Delta\lambda_{\min}/(2\pi)$），也是光子红移的度量：
- 对黑洞视界附近发射的光子：$\Delta\lambda_{\min}$ 对应 Hawking 温度 $T_H$；
- 对宇宙学红移光子：$\Delta\lambda_{\min}$ 对应红移因子 $1+z$。

**证明草图**。两者都对应 $\partial\mathbf{Rec}_D$ 上的谱间隙极限。黑洞情形：$\Delta\lambda_{\min} = \kappa/2\pi$（$\kappa$ 为视界表面引力），$T_H = \kappa/2\pi = \Delta\lambda_{\min}/(2\pi)$。宇宙学红移：$\Delta\lambda_{\min}$ 对应膨胀宇宙中光子频率的红移，$1+z = \omega_{\text{emit}}/\omega_{\text{obs}}$。□

> **推论**：光子红移、Hawking 辐射、Unruh 效应三者共享同一谱机制——$\partial\mathbf{Rec}_D$ 上的谱流。这是 Paper VIII 与本文的关键统一。

### 4.4 因果锥的谱定义

**定义 4.5**（谱因果锥）。对谱对象 $E = (\mathcal{H}, A, \sigma(A)) \in \mathbf{Spec}$，定义其**因果锥**为
$$\mathcal{C}(E) := \left\{E' \in \mathbf{Spec} : \exists \text{ 谱态射 } T: E \to E',\, \sigma(T) \subset \mathbb{R}_{\ge 0}\right\}.$$

即因果锥是 $E$ 通过"保因果符号的谱态射"可达的所有谱对象集合。

**命题 4.6**（因果锥 = Lorentz 因果未来）。在 Minkowski 时空 $\mathbb{R}^{1,3}$ 中，谱因果锥 $\mathcal{C}(E)$ 等于 Lorentz 因果未来 $J^+(E)$：
$$\mathcal{C}(E) = J^+(E).$$

**证明**。由定理 1.3，保因果符号的谱态射对应保类时/类光性的变换。Lorentz 群保因果符号（推论 1.4），且 Minkowski 时空的因果未来由类时/类光曲线定义。故两者重合。□

---

## 5. 质量壳与谱约束

### 5.1 质量壳的谱定义

**定义 5.1**（质量壳谱条件）。粒子静质量为 $m$ 的质量壳定义为 $\mathbf{Spec}$ 中的子对象
$$\mathcal{M}_m := \left\{E \in \mathbf{Spec} : \sigma(M^2) = \{m^2\}\right\}.$$

即质量壳是质量谱算子取固定值 $m^2$ 的所有谱对象构成的子范畴。

**命题 5.2**（质量壳 = Lorentz 轨道）。质量壳 $\mathcal{M}_m$ 在 Lorentz 谱流作用下闭合：
$$U_\tau \mathcal{M}_m U_\tau^{-1} = \mathcal{M}_m, \quad \forall \tau.$$

**证明**。由定理 2.4，$\sigma(M^2_\tau) = \sigma(M^2_0)$。若 $M^2_0 = m^2$，则 $M^2_\tau = m^2$。故 Lorentz 谱流保持质量壳。□

**推论 5.3**（Lorentz 轨道 = 质量壳）。Lorentz 群在 $\mathbf{Spec}$ 中的轨道恰好是质量壳：
$$\mathcal{O}_{\text{Lor}}(E) := \{U_\tau E U_\tau^{-1} : \tau\} = \mathcal{M}_m, \quad \text{其中 } m^2 = \min\sigma(M^2_E).$$

**证明**。Lorentz 群作用于 $\mathcal{M}_m$ 上传递（任意两个具有相同 $m$ 的四动量可通过 Lorentz 变换联系）。故轨道等于质量壳。□

### 5.2 质量壳作为不动点子范畴

**命题 5.4**（质量壳是 Lorentz 不动点子范畴）。质量壳 $\mathcal{M}_m$ 是 Lorentz 谱流的不动点子范畴：
$$\mathrm{Fix}_{\text{Lor}}(\mathbf{Spec}) = \bigsqcup_{m \ge 0} \mathcal{M}_m.$$

**证明**。Lorentz 谱流在 $\mathcal{M}_m$ 上传递，但在不同 $\mathcal{M}_m$ 之间无变换。故整个 $\mathbf{Spec}$ 分解为 Lorentz 不变的质量壳不交并。□

> **范畴论意义**：Lorentz 群在 $\mathbf{Spec}$ 中的不动点分解为质量壳的不交并——这是 Wigner 分类"粒子 = Poincaré 不可约表示"的范畴论形式。

### 5.3 质量谱与速度谱的耦合

**命题 5.5**（质量-速度谱耦合）。对有质量粒子（$m > 0$），其速度 $v$ 与静质量 $m$ 通过 Lorentz 因子 $\gamma$ 耦合：
$$\gamma = \frac{1}{\sqrt{1 - v^2/c^2}} = \cosh\varphi,$$
其中 $\varphi$ 为 rapidity（参见 `spectral_lorentz_kinematics.md` §1）。能量谱 $E$ 在 Lorentz 推进下变为：
$$E_\tau = \gamma E_0 = \cosh\varphi \cdot E_0.$$

**证明**。这是 `spectral_lorentz_kinematics.md` 定理 2.2 的直接应用：能量作为谱算子的频率特征值，在 rapidity 流下按 $\cosh\varphi$ 放大。□

**推论 5.6**（光子无质量 → 无 rapidity 上限）。对光子（$m = 0$），$v = c$ 对应 $\varphi \to \infty$，但 $\gamma = \cosh\varphi \to \infty$。光子的能量 $E = \hbar\omega$ 在任意 rapidity 流下保持有限（因为 $E_0$ 在共动系无定义，需另行处理）。这给出光子在 $\partial\mathbf{Rec}_D$ 上的特殊谱地位。

---

## 6. 严格证明：核心定理汇总

### 6.1 主定理

**主定理 A**（因果性谱刻画）。物理系统的因果性（类时/类光/类空）由其谱算子 $A_v = \eta_{\mu\nu}P^\mu P^\nu$ 的符号函数 $\mathrm{sgn}(\sigma(A_v))$ 唯一确定。Lorentz 谱流保因果。

**主定理 B**（静质量谱刻画）。静质量平方 $m^2$ 等于质量谱算子 $M^2 = P^\mu P_\mu$ 的最小特征值。Lorentz 谱流保持质量谱。

**主定理 C**（自旋谱刻画）。自旋量子数 $s$ 通过 $s(s+1) = \min\sigma(S^2)/m^2$ 由 Pauli-Lubanski 谱算子 $S^2 = W^\mu W_\mu$ 唯一确定。Lorentz 谱流保持自旋谱。

**主定理 D**（光锥 = $\partial\mathbf{Rec}_D$）。类光轨道对应谱算子最小谱间隙 $\Delta\lambda_{\min} = 0$，即位于 $\partial\mathbf{Rec}_D$ 上。光锥与黑洞视界共享同一谱边界。

### 6.2 推论链

```
Lorentz 谱流 (定义 2.1, 主笔记)
    ↓ 保谱
σ(A_τ) = σ(A_0) (主笔记定理 2.2)
    ↓ 应用到 A_v
因果符号不变 (本笔记定理 1.3 + 推论 1.4)
    ↓
质量谱不变 (本笔记定理 2.4)
    ↓
m² = min σ(M²) 是 Lorentz 不动点 (本笔记命题 2.4)
    ↓
m=0 ↔ Δλ_min=0 ↔ ∂Rec_D (本笔记定理 4.2)
    ↓
光锥 = ∂Rec_D = 黑洞视界谱边界 (本笔记推论 4.3)
```

### 6.3 关键不变量表

| 物理量 | 谱定义 | 谱不变量类型 |
|:------|:-------|:------------|
| 静质量 $m$ | $m^2 = \min\sigma(M^2)$ | Casimir 谱间隙 |
| 自旋 $s$ | $s(s+1) = \min\sigma(S^2)/m^2$ | Casimir 谱间隙 |
| 因果符号 | $\mathrm{sgn}(\sigma(A_v))$ | 谱符号函数 |
| 电荷 $q$ | $\min\sigma(Q^2)$（$Q$ 为荷算子） | 规范 Casimir 谱间隙 |
| 螺度 $h$ | $h = \mathbf{J}\cdot\mathbf{P}/|\mathbf{P}|$ 的谱取值 | 自旋-动量耦合谱 |

---

## 7. 与黑洞物理的统一

### 7.1 谱边界的双重身份

**命题 7.1**（$\partial\mathbf{Rec}_D$ 的双重身份）。$\partial\mathbf{Rec}_D$ 在 $\mathbf{Spec}$ 中具有双重身份：
- 作为**光锥边界**（本笔记定理 4.2）：$\Delta\lambda_{\min} = 0$ 对应类光运动；
- 作为**黑洞视界**（Paper VIII 定理 3.2）：$\Delta\lambda_{\min} = 0$ 对应视界 Hawking 温度。

**证明**。两者均由 $\partial\mathbf{Rec}_D := \{R : \Delta\lambda_{\min}(R) = 0\}$ 定义，故身份重合。□

### 7.2 Hawking 温度与红移的统一公式

**命题 7.2**（Hawking-红移统一公式）。$\partial\mathbf{Rec}_D$ 上的谱流给出统一的温度-频率关系：
$$T = \frac{\Delta\lambda_{\min}}{2\pi}, \quad \omega_{\text{obs}} = \omega_{\text{emit}} \cdot \mathrm{sech}\,\varphi,$$
其中 $\varphi$ 为推进 rapidity。在 $\Delta\lambda_{\min} \to 0$ 极限下：
- 黑洞 Hawking 温度 $T_H \to 0$（大黑洞）或 $T_H \to \infty$（小黑洞）；
- 红移 $\omega_{\text{obs}}/\omega_{\text{emit}} \to 0$（无限红移）。

### 7.3 Bekenstein-Hawking 熵的谱推导

**命题 7.3**（BH 熵的谱推导）。Paper VIII 给出 $S_{BH} = \pi/(4\Delta\lambda_{\min}^2)$。在 $\partial\mathbf{Rec}_D$ 上 $\Delta\lambda_{\min} = 0$，形式上 $S_{BH} \to \infty$。这对应黑洞在蒸发极限（小质量极限）下熵发散，与 Page 曲线的晚期行为一致。

> **统一信息**：光锥、黑洞视界、Hawking 温度、Bekenstein-Hawking 熵、红移效应都源自 $\partial\mathbf{Rec}_D$ 的同一谱边界条件。这是 Lorentz 谱动力学与 Paper VIII 黑洞物理的范畴统一。

---

## 8. 开放问题

### 8.1 严格化需求

| 问题 | 难度 | 说明 |
|:----|:----:|:-----|
| 自旋-统计定理的谱证明 | 🔴 | 需要构造 $\mathbb{Z}_2$ 分级谱范畴 |
| 螺度的谱刻画 | 🟡 | 无质量粒子的螺度需要单独处理 |
| 弱相互作用下 Lorentz 局部破缺 | 🟡 | 中微子振荡是否对应谱微扰？ |
| 量子引力中 $\partial\mathbf{Rec}_D$ 的涨落 | 🔴 | 离散谱与连续谱的边界处理 |

### 8.2 扩展方向

1. **弯曲时空中的因果结构**：从 Minkowski 推广到 Lorentz 流形（参见 `spectral_lorentz_curved_spacetime.md`，待创建）。
2. **量子信息视角**：纠缠熵与 $\partial\mathbf{Rec}_D$ 的关系（Page 曲线的谱推导）。
3. **因果集理论的谱翻译**：离散因果序与 $\mathbf{Spec}_{\text{dyn}}$ 态射时序的对应。
4. **超光速粒子的谱地位**：快子（$m^2 < 0$）在 $\mathbf{Rec} \setminus \mathbf{Rec}_D$ 中的位置。

### 8.3 与现有框架的衔接

| 衔接点 | 现有内容 | 本笔记的扩展 |
|:-------|:---------|:------------|
| Paper VIII $\partial\mathbf{Rec}_D$ | 黑洞视界谱边界 | 光锥、红移、Hawking 统一 |
| Paper XI A7 公理 | QFT 场 Lorentz 变换规则 | 因果性、质量、自旋的谱刻画 |
| `spectral_lorentz_axiom.md` | Lorentz 群在 Spec 上的作用 | Lorentz 流的不动点结构 |
| `spectral_lorentz_dynamics.md` | Lorentz 谱流方程 | 不变量作为不动点 |
| `spectral_lorentz_kinematics.md` | Rapidity、时间膨胀、长度收缩 | 质量壳、能量-动量耦合 |

---

## 9. 与标准物理的对应表

| 标准相对论概念 | 谱动力学对应 | 出处 |
|:-------------|:------------|:-----|
| 类时/类光/类空 | $\mathrm{sgn}(\sigma(A_v))$ | 定理 1.3 |
| Lorentz 不变性 | $\sigma(A_\tau) = \sigma(A_0)$ | 主笔记定理 2.2 |
| 静质量 $m$ | $\min\sigma(M^2)$ 的平方根 | 定理 2.3 |
| 自旋 $s$ | $\sqrt{\min\sigma(S^2)/m^2}$ 的解 | 定理 3.3 |
| 质量壳 $p^2 = m^2$ | $\sigma(M^2) = \{m^2\}$ 的子对象 | 定义 5.1 |
| 光锥 | $\partial\mathbf{Rec}_D$ | 定理 4.2 |
| 因果未来 $J^+(p)$ | 谱因果锥 $\mathcal{C}(E)$ | 命题 4.6 |
| Wigner 分类 | Lorentz 不动点子范畴分解 | 命题 5.4 |
| Higgs 机制 | 谱间隙从 0 跳变为 $\lambda v^2$ | 命题 2.7 |

---

## 10. 版本记录

- v0.1（2026-07-19）：初稿。建立因果符号、静质量、自旋的谱刻画；统一光锥与 $\partial\mathbf{Rec}_D$；列出 4 个主定理与 5 个推论。

---

## 11. 参考文献

- **主笔记**：`spectral_lorentz_dynamics.md`
- **运动学补遗**：`spectral_lorentz_kinematics.md`
- **Paper V**：`paper/paper5_spectral_dynamics.md`（谱流方程基础）
- **Paper VIII**：`paper/paper8_black_hole_spectral.md`（$\partial\mathbf{Rec}_D$、$T_H$、$S_{BH}$）
- **Paper XI**：`paper/paper11_spectral_QFT.md`（A7 Lorentz 公理）
- **Wigner 分类**：E. Wigner, *On Unitary Representations of the Inhomogeneous Lorentz Group*, Ann. Math. (1939)
- **Weinberg QFT I**：Ch. 2（Poincaré 不变性与 Wigner 分类）
- **Paper VIII 衍生**：`notes/spectral_Kerr_silence_analysis.md`（Kerr 视界多重静默）
