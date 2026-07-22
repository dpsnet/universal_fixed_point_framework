# 谱规范理论：BRST、鬼场与 Ward 恒等式

## 核心目标

在 T1 的谱 YM 拉格朗日量基础上，建立谱版本的规范固定、FP 鬼场、BRST 对称性和 Ward 恒等式，完善谱非交换规范场论。

---

## 1. 谱规范固定

### 1.1 规范冗余的谱表述

在标准 YM 理论中，规范变换 $A_\mu \to g^{-1}A_\mu g + g^{-1}\partial_\mu g$ 导致路径积分发散。谱版本中规范变换对应于 $\mathbf{Spec}$ 范畴中的态射共轭：

$$\mathcal{A} \to g^{-1} \mathcal{A} g + g^{-1} [\nabla, g],$$

其中 $\nabla$ 是谱联络，$g \in \mathcal{G}$ 是谱规范群对象。

### 1.2 谱 $R_\xi$ 规范固定

谱版本的规范固定项为（类比标准 $R_\xi$ 规范）：

$$\mathcal{L}_{\text{gf}}^{\text{spec}} = -\frac{1}{2\xi} \operatorname{Tr}_{\mathfrak{g}} \left( [\nabla^\mu, \mathcal{A}_\mu] \star [\nabla^\nu, \mathcal{A}_\nu] \right),$$

其中 $[\nabla^\mu, \mathcal{A}_\mu]$ 是谱版本的规范条件（$\partial^\mu A_\mu = 0$ 的谱翻译），$\xi$ 是规范参数。

**谱 Feynman 规范** ($\xi = 1$) 下，谱规范传播子简化为：

$$D_{\mu\nu}^{ab}(k) = -\frac{i\delta^{ab}}{k^2 + i\varepsilon} \left( g_{\mu\nu} - (1-\xi)\frac{k_\mu k_\nu}{k^2} \right).$$

在谱表示下：

$$D_{\mu\nu}^{ab}(\lambda) = -\frac{i\delta^{ab}}{\lambda + i\varepsilon} \left( g_{\mu\nu} - (1-\xi)\frac{k_\mu k_\nu}{\lambda} \right).$$

### 1.3 谱规范固定拉格朗日量

完整谱规范固定拉格朗日量为：

$$\mathcal{L}_{\text{YM+gf}}^{\text{spec}} = -\frac{1}{4} \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F}_{\mu\nu}\mathcal{F}^{\mu\nu}) - \frac{1}{2\xi} \operatorname{Tr}_{\mathfrak{g}}([\nabla^\mu,\mathcal{A}_\mu]^2).$$

---

## 2. 谱 FP 鬼场

### 2.1 鬼场的谱翻译

Faddeev-Popov 行列式 $\det(\delta G/\delta \alpha)$ 的谱版本通过 Grassmann 值谱鬼场引入：

$$\mathcal{L}_{\text{ghost}}^{\text{spec}} = \operatorname{Tr}_{\mathfrak{g}} \left( \bar{c}^a [\nabla^\mu, D_\mu c]^a \right),$$

其中：
- $c^a(\lambda)$: 谱鬼场（Grassmann 奇值的 $\mathbf{Spec}$ 对象）
- $\bar{c}^a(\lambda)$: 谱反鬼场
- $D_\mu c = \partial_\mu c + g[\mathcal{A}_\mu, c]$: 谱协变导数

### 2.2 谱鬼场传播子

在 $\xi$ 规范下，谱鬼场传播子为：

$$G_{\text{ghost}}^{ab}(\lambda) = \frac{i\delta^{ab}}{\lambda + i\varepsilon}.$$

与标量谱传播子形式一致，但具有 Grassmann 统计（奇 $\mathbb{Z}_2$ 分级）。

### 2.3 谱鬼场顶点

鬼-胶子相互作用顶点：

$$\Gamma_{\bar{c}Ac}^{abc}(\lambda_1, \lambda_2, \lambda_3) = -g f^{abc} \cdot \delta(\lambda_1 + \lambda_2 + \lambda_3),$$

其中 $f^{abc}$ 是李代数结构常数。

---

## 3. 谱 BRST 对称性

### 3.1 BRST 变换的谱形式

标准 BRST 变换 $s$ 的谱版本为：

$$s\mathcal{A}_\mu = [\nabla_\mu, c], \quad sc = \frac{g}{2}[c, c], \quad s\bar{c} = \frac{[\nabla^\mu, \mathcal{A}_\mu]}{\xi}, \quad s\Phi = -g c \Phi.$$

其中 $s$ 是 Graded 导子（奇 $\mathbb{Z}_2$ 分级，与谱对象的分级结构一致）。

### 3.2 BRST 不变性

**定理 1**（谱 BRST 不变性）。完整规范固定拉格朗日量在 BRST 变换下不变：

$$s\left( \mathcal{L}_{\text{YM+gf+ghost}}^{\text{spec}} \right) = 0.$$

**证明**。分为三步：
1. $s\mathcal{L}_{\text{YM}}^{\text{spec}} = 0$: YM 项在规范变换下不变，BRST 是规范变换的代数版本
2. $s\mathcal{L}_{\text{gf}}^{\text{spec}} + s\mathcal{L}_{\text{ghost}}^{\text{spec}} = 0$: 规范固定项的 BRST 变化被鬼场项抵消
3. $s^2 = 0$: BRST 算子幂零（谱 $\mathbb{Z}_2$ 分级的自然结果）

### 3.3 BRST 荷的谱表示

BRST 荷 $Q_{\text{BRST}}$ 在 $\mathbf{Spec}$ 中的表示为：

$$Q_{\text{BRST}} = \int d\lambda \, c(\lambda) \left( [\nabla^\mu, \mathcal{A}_\mu](\lambda) + \frac{g}{2}[\bar{c}, c](\lambda) \right),$$

满足 $Q_{\text{BRST}}^2 = 0$。物理态空间为 $Q_{\text{BRST}}$-上同调：

$$\mathcal{H}_{\text{phys}} = \ker Q_{\text{BRST}} / \operatorname{im} Q_{\text{BRST}}.$$

---

## 4. 谱 Ward 恒等式（Slavnov-Taylor 恒等式）

### 4.1 生成泛函的 BRST 变换

谱生成泛函的 BRST 变换给出：

$$\int \mathcal{D}_{\text{Spec}}[\mathcal{A}, c, \bar{c}] \; s(\cdots) e^{iS_{\text{eff}}} = 0,$$

其中 $S_{\text{eff}} = S_{\text{YM}} + S_{\text{gf}} + S_{\text{ghost}}$。

### 4.2 谱 Ward 恒等式

对规范传播子的 Ward 恒等式：

$$k^\mu \tilde{D}_{\mu\nu}^{ab}(k) = \xi \cdot (\text{ghost 贡献}),$$

在谱语言中：

$$\lambda \cdot \tilde{D}_{\mu\nu}^{ab}(\lambda) = \xi \cdot \delta^{ab} \frac{k_\mu k_\nu}{\lambda^2} + \mathcal{O}(g).$$

**推论**（物理极化）。物理散射振幅仅依赖于横向极化模式，纵向/类时模式被鬼场抵消。

### 4.3 谱耦合跑动与 Ward 恒等式

Ward 恒等式保证了规范耦合的重整化与规范参数 $\xi$ 无关：

$$\beta(g) = \frac{dg}{d\ln\mu} = -\frac{b_0}{16\pi^2} g^3,$$

其中 $b_0 = \frac{11}{3}C_2(G) - \frac{4}{3}T(R)n_f$。

**定理 2**（谱 Ward 恒等式的函子不变性）。Ward 恒等式在谱去递归函子 $D: \mathbf{Rec}_D \to \mathbf{Spec}$ 下保持：

$$D(\text{Ward}_{\text{std}}) = \text{Ward}_{\text{spec}}.$$

---

## 5. 与标准规范理论的对应

| 概念 | 标准 QFT | 谱版本 |
|:----|:---------|:-------|
| 规范固定 | $\mathcal{L}_{\text{gf}} = -\frac{1}{2\xi}(\partial^\mu A_\mu)^2$ | $\mathcal{L}_{\text{gf}}^{\text{spec}} = -\frac{1}{2\xi}\operatorname{Tr}_{\mathfrak{g}}([\nabla^\mu,\mathcal{A}_\mu]^2)$ |
| FP 鬼场 | $\bar{c}^a \partial^\mu D_\mu c^a$ | $\bar{c}^a [\nabla^\mu, D_\mu c]^a$ |
| BRST 变换 | $sA_\mu = D_\mu c$ | $s\mathcal{A}_\mu = [\nabla_\mu, c]$ |
| BRST 幂零性 | $s^2 = 0$ | $s^2 = 0$（$\mathbf{Spec}$ $\mathbb{Z}_2$ 分级） |
| Ward 恒等式 | $k^\mu D_{\mu\nu} = \xi \cdot (\cdots)$ | $\lambda \tilde{D}_{\mu\nu}(\lambda) = \xi \cdot (\cdots)$ |

---

## 6. 数值验证

### 6.1 谱规范传播子

验证谱规范传播子在不同规范参数 $\xi$ 下的行为：
- $\xi = 0$ (Landau 规范): 横向量子数仅横向传播
- $\xi = 1$ (Feynman 规范): 传播子 $D_{\mu\nu} = -ig_{\mu\nu}/k^2$
- $\xi \to \infty$ (幺正规范): 非物理极化退耦

### 6.2 谱鬼场传播子

验证谱鬼场传播子与标量谱传播子形式一致（$\delta^{ab}/(k^2 + i\varepsilon)$）。

### 6.3 BRST 不变性

数值验证 BRST 变换下规范固定拉格朗日量的不变性（在离散谱截断下）。

---

## 7. 开放问题

| 问题 | 难度 | 说明 |
|:----|:----:|------|
| 谱版本的 Gribov 复制问题 | 🔴 | 非微扰规范固定中的 Gribov 副本在 $\mathbf{Spec}$ 中的表现 |
| 谱瞬子与 $\theta$ 真空 | 🔴 | 瞬子解的谱翻译与 $\theta$ 项的谱表示 |
| 谱反常（Adler-Bell-Jackiw） | 🟡 | 三角图 anomalies 的谱版本与 $\mathbf{Spec}$ 上同调 |
| 谱规范理论的严格 BRST 上同调 | 🟡 | $\mathbf{Spec}$ 范畴中的 BRST 上同调计算 |
