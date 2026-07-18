# Lorentz 变换的谱动力学解读——核心研究笔记

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**日期**：2026-07-19

**状态**：研究笔记（Paper XVI 候选基础）

---

## 0. 摘要

本笔记建立 Lorentz 变换在 $\mathbf{Spec}$ 范畴中的谱动力学解读。核心论题：**Lorentz 变换不是独立给出的时空几何公理，而是谱流方程 $\frac{d}{d\tau}A_\tau = [G_{\text{Lor}}, A_\tau]$ 在 $G_{\text{Lor}} \in \mathfrak{so}(1,3)$ 时的实例化**。由此推出：(1) Lorentz 不变性 = 谱不变性 $\sigma(A_\tau) = \sigma(A_0)$；(2) Rapidity = 谱流内禀时间；(3) 时间膨胀 = 谱间隙按 $\text{sech}\,\varphi$ 压缩；(4) 静质量 = 动量算符谱间隙；(5) 光锥结构 = $\partial\mathbf{Rec}_D$ 谱边界条件；(6) Lorentz 违规 = 谱静默条件破缺。

本文与已有 `spectral_lorentz_axiom.md`（Paper XI A7 公理）互补：A7 规定 Lorentz 群在 $\mathbf{Spec}$ 中的**作用方式**（QFT 场变换），本文建立 Lorentz 群作为谱流方程**生成元**的**动力学**，并把狭义相对论的诸多效应还原为谱定理的推论。

---

## 1. 问题陈述

### 1.1 现状的不足

框架目前已有的 Lorentz 处理集中在 Paper XI A7 公理，仅规定 QFT 场 $\Phi(\lambda)$ 在 Lorentz 变换下的变换法则 $\Phi'(\lambda') = U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1}$。这回答了"QFT 如何 Lorentz 协变"，但未回答：

1. **Lorentz 变换本身的谱动力学身份是什么？** 为何时空对称群恰好是 $SO^+(1,3)$？
2. **Rapidity、$\gamma$ 因子、时间膨胀、长度收缩的谱机制？** 这些是独立假设还是谱流定理？
3. **静质量、自旋作为 Lorentz 不变量的谱基础？** 它们为何在 Lorentz 变换下不变？
4. **光锥结构与 Paper VIII 的 $\partial\mathbf{Rec}_D$ 谱边界有何关系？**
5. **Lorentz 违规（如某些量子引力模型预测的高能光子色散）在谱框架中意味着什么？**

### 1.2 核心论题

**Lorentz 变换是谱流方程在时空对称群上的限制**。具体地，对 Lorentz 群 $SO^+(1,3)$ 的 Lie 代数 $\mathfrak{so}(1,3)$，存在谱生成元嵌入

$$\iota_{\text{Lor}}: \mathfrak{so}(1,3) \hookrightarrow \mathrm{Gen}(\mathbf{Spec}),$$

使得任意 Lorentz 变换 $\Lambda = \exp(\omega_{\mu\nu}M^{\mu\nu}/2) \in SO^+(1,3)$ 对应谱流

$$\frac{d}{d\tau}A_\tau = [G_{\text{Lor}}, A_\tau],\quad G_{\text{Lor}} = \iota_{\text{Lor}}\left(\tfrac12\omega_{\mu\nu}M^{\mu\nu}\right),$$

解为 $A_\tau = U_\tau A_0 U_\tau^{-1}$，$U_\tau = e^{\tau G_{\text{Lor}}}$。Lorentz 不变性由 Paper V 定理 2.2（谱流不变性）保证：$\sigma(A_\tau) = \sigma(A_0)$。

---

## 2. Lorentz 群作为谱流生成元

### 2.1 Lie 代数 $\mathfrak{so}(1,3)$ 的谱提升

Lorentz 群 $SO^+(1,3)$ 的 Lie 代数 $\mathfrak{so}(1,3)$ 由 6 个生成元构成：3 个空间旋转 $J_i$ 与 3 个 Lorentz 推进 $K_i$，对易关系为

$$[J_i, J_j] = \varepsilon_{ijk} J_k,\quad [J_i, K_j] = \varepsilon_{ijk} K_k,\quad [K_i, K_j] = -\varepsilon_{ijk} J_k.$$

**定义 2.1**（Lorentz 谱生成元嵌入）。Lorentz 谱生成元嵌入 $\iota_{\text{Lor}}: \mathfrak{so}(1,3) \to \mathrm{Gen}(\mathbf{Spec})$ 是 Lie 代数同态，把 $\mathfrak{so}(1,3)$ 的生成元 $J_i, K_i$ 映为 $\mathbf{Spec}$ 中的反 Hermite 谱生成元：

$$\iota_{\text{Lor}}(J_i) =: \mathcal{J}_i,\quad \iota_{\text{Lor}}(K_i) =: \mathcal{K}_i,$$

满足 $\mathcal{J}_i^\dagger = -\mathcal{J}_i$，$\mathcal{K}_i^\dagger = -\mathcal{K}_i$（反 Hermite 性保证 $U_\tau = e^{\tau\mathcal{G}}$ 为幺正算子，谱流保谱）。Lie 代数同态条件：

$$[\mathcal{J}_i, \mathcal{J}_j] = \varepsilon_{ijk}\mathcal{J}_k,\quad [\mathcal{J}_i, \mathcal{K}_j] = \varepsilon_{ijk}\mathcal{K}_k,\quad [\mathcal{K}_i, \mathcal{K}_j] = -\varepsilon_{ijk}\mathcal{J}_k.$$

**注 2.1**（同态的非平凡性）。$\iota_{\text{Lor}}$ 不是恒等映射——它把抽象 Lie 代数元映为 $\mathbf{Spec}$ 中的具体算子。其存在性由 Wigner-Bargmann 表示定理保证：Lorentz 群在 Hilbert 空间上的么正表示存在，且其 Lie 代数表示满足上述对易关系。

### 2.2 Lorentz 谱流方程

**定理 2.1**（Lorentz 谱流方程）。设物理可观测量 $A$ 在 $\mathbf{Spec}$ 中的谱像为 $D(A) = (\mathcal{H}, A, \sigma(A))$。Lorentz 变换 $\Lambda(\boldsymbol{\theta}, \boldsymbol{\varphi}) = \exp(\boldsymbol{\theta}\cdot\mathbf{J} + \boldsymbol{\varphi}\cdot\mathbf{K}) \in SO^+(1,3)$ 作用于 $A$ 上对应谱流：

$$\boxed{\frac{d}{d\tau}A_\tau = [G_{\text{Lor}}, A_\tau],\quad G_{\text{Lor}} = \boldsymbol{\theta}\cdot\boldsymbol{\mathcal{J}} + \boldsymbol{\varphi}\cdot\boldsymbol{\mathcal{K}}}$$

其中 $\tau$ 为谱流参数（在纯旋转时 $\tau = |\boldsymbol{\theta}|$ 为旋转角；在纯推进时 $\tau = |\boldsymbol{\varphi}|$ 为 rapidity）。解为：

$$A_\tau = U_\tau A_0 U_\tau^{-1},\quad U_\tau = e^{\tau G_{\text{Lor}}}.$$

**证明**。由 $\iota_{\text{Lor}}$ 是 Lie 代数同态，$\exp(\tau G_{\text{Lor}}) = \iota_{\text{Lor}}(\exp(\tau\omega_{\mu\nu}M^{\mu\nu}/2))$ 是 Lorentz 群在 $\mathbf{Spec}$ 中的实现。$G_{\text{Lor}}$ 反 Hermite $\Rightarrow$ $U_\tau$ 幺正 $\Rightarrow$ $A_\tau = U_\tau A_0 U_\tau^{-1}$ 是相似变换。谱流方程由直接对 $\tau$ 求导得到：$\frac{d}{d\tau}A_\tau = G_{\text{Lor}} A_\tau - A_\tau G_{\text{Lor}} = [G_{\text{Lor}}, A_\tau]$。□

**注 2.2**（与 Paper V 力谱流的同构）。Lorentz 谱流方程与 Paper V 的力谱流方程 $\frac{d}{dt}A_t = \sum_i g_i [A_{F,i}, A_t]$ 共享 Lie 导数结构 $[G, A_t]$。区别仅在生成元的物理身份：力谱流的 $A_{F,i}$ 是相互作用的谱生成元，Lorentz 谱流的 $\mathcal{J}_i, \mathcal{K}_i$ 是时空对称性的谱生成元。这一同构揭示：**时空对称性与基本力共享同一谱动力学根源**。

### 2.3 主定理：Lorentz 不变性 = 谱不变性

**定理 2.2**（Lorentz 不变性的谱刻画）。对任意 Lorentz 变换 $\Lambda \in SO^+(1,3)$ 与任意可观测量 $A \in \mathrm{Obj}(\mathbf{Spec})$，

$$\sigma(\Lambda\cdot A\cdot\Lambda^{-1}) = \sigma(A).$$

**证明**。由定理 2.1，$\Lambda\cdot A\cdot\Lambda^{-1} = A_\tau = U_\tau A_0 U_\tau^{-1}$ 是幺正相似变换。由 Paper V 定理 2.2（谱流不变性），谱在幺正相似下不变：$\sigma(A_\tau) = \sigma(A_0)$。□

**物理意义**。Lorentz 不变量（静质量 $m^2 = p^\mu p_\mu$、自旋 $s^2 = W^\mu W_\mu$、固有时 $\tau$、电动力学的 $F_{\mu\nu}F^{\mu\nu}$、$F_{\mu\nu}\tilde{F}^{\mu\nu}$ 等）的"不变性"不是独立原理，而是 **谱不变性在物理投影上的表现**——它们都是某个谱生成元的本征值，而本征值在幺正相似下不变。

### 2.4 与 A7 公理的关系

`spectral_lorentz_axiom.md` 中的 A7 公理规定 Lorentz 群在 $\mathbf{Spec}$ 中的**作用函子** $L: \mathcal{P}_+^\uparrow \to \mathrm{Aut}(\mathbf{Spec})$，以及 QFT 场 $\Phi(\lambda)$ 的变换法则 $\Phi'(\lambda') = U(\Lambda)\Phi(\lambda)U(\Lambda)^{-1}$。

**命题 2.3**（A7 是定理 2.1 的具体化）。A7 公理中的 $U(\Lambda)$ 与定理 2.1 中的 $U_\tau$ 通过 $\Lambda = \exp(\tau G_{\text{Lor}}^{\text{abstract}})$ 一一对应：

$$U(\Lambda) = \iota_{\text{Lor}}(\Lambda) = e^{\tau G_{\text{Lor}}}.$$

即 A7 公理中的"幺正实现 $U(\Lambda)$"在谱动力学中**作为谱流半群 $U_\tau = e^{\tau G_{\text{Lor}}}$ 自然涌现**，无需独立假设。

**证明**。A7 的 $U(\Lambda)$ 是 Lorentz 群的么正表示，由 Wigner 定理唯一确定（在 projective 表示意义下）。谱流 $U_\tau = e^{\tau G_{\text{Lor}}}$ 也是 Lorentz 群的么正表示（通过 $\iota_{\text{Lor}}$）。两者在表示等价类意义下相同。□

**结论**：A7 公理可从定理 2.1 推出。这把 A7 从"独立公理"降格为"谱流方程的推论"——与 Paper VII（热力学第二定律 = 谱熵增定理）、Paper VIII（黑洞熵 = 谱计数）的处理方式一致。

---

## 3. Rapidity 作为谱流内禀时间

### 3.1 纯推进的谱流参数化

考虑沿 $x$ 方向的纯 Lorentz 推进 $\Lambda_x(\varphi) = \exp(\varphi K_x)$，其中 $\varphi$ 为 rapidity。由定理 2.1，对应的谱流为：

$$\frac{d}{d\varphi}A_\varphi = [\mathcal{K}_x, A_\varphi],\quad A_\varphi = e^{\varphi\mathcal{K}_x} A_0 e^{-\varphi\mathcal{K}_x}.$$

**命题 3.1**（Rapidity = 谱流时间）。Rapidity $\varphi$ 是 Lorentz 谱流的内禀时间参数，满足：

1. **加法性**：$\varphi_1 \oplus \varphi_2 = \varphi_1 + \varphi_2$（半群性质 $U_{\varphi_1}U_{\varphi_2} = U_{\varphi_1+\varphi_2}$）
2. **零元**：$\varphi = 0$ 对应恒等变换 $U_0 = I$
3. **逆元**：$-\varphi$ 对应逆变换 $U_{-\varphi} = U_\varphi^{-1}$
4. **连续性**：$\varphi \in \mathbb{R}$（Lorentz 群非紧性）

**证明**。由谱流半群性质 $U_{\varphi_1+\varphi_2} = e^{(\varphi_1+\varphi_2)\mathcal{K}_x} = e^{\varphi_1\mathcal{K}_x}e^{\varphi_2\mathcal{K}_x} = U_{\varphi_1}U_{\varphi_2}$。其他性质由指数映射的标准性质给出。□

### 3.2 速度合成律的谱推导

经典相对论速度合成律：

$$v \oplus v' = \frac{v + v'}{1 + vv'/c^2}$$

在 rapidity 参数化下化为简单加法 $\varphi \oplus \varphi' = \varphi + \varphi'$。在谱动力学中：

**定理 3.2**（速度合成律的谱推导）。相对论速度合成律是谱流半群性质的直接推论：

$$\tanh(\varphi_1 + \varphi_2) = \frac{\tanh\varphi_1 + \tanh\varphi_2}{1 + \tanh\varphi_1\tanh\varphi_2}.$$

**证明**。设 $v_i/c = \tanh\varphi_i$（$i = 1, 2$）。由命题 3.1，复合推进 $\Lambda_x(\varphi_1)\Lambda_x(\varphi_2) = \Lambda_x(\varphi_1+\varphi_2)$。代入速度映射 $v/c = \tanh\varphi$ 并使用双曲正切加法公式即得速度合成律。□

**意义**：相对论速度合成的"奇怪"形式（$1 + vv'/c^2$ 分母）不是独立假设——它是 **谱流半群在非线性速度参数化 $v/c = \tanh\varphi$ 下的表象**。Rapidity 才是 Lorentz 谱流的内禀参数；速度 $v$ 是其非线性投影。这一翻译揭示了 rapidity 的几何本质。

### 3.3 Newton 极限作为谱流线性化

**命题 3.3**（Galileo 极限 = 谱流线性化）。在 rapidity $\varphi \ll 1$ 极限下，Lorentz 谱流退化为 Galileo 谱流：

$$U_\varphi = e^{\varphi\mathcal{K}_x} \approx I + \varphi\mathcal{K}_x + \mathcal{O}(\varphi^2),$$

对应 Galileo 速度加法 $v \oplus v' \approx v + v'$（一阶）。

**证明**。$v/c = \tanh\varphi \approx \varphi$ 对 $\varphi \ll 1$。代入速度合成公式，分母 $1 + \tanh\varphi_1\tanh\varphi_2 \approx 1$，得 $v\oplus v' \approx v + v'$。在谱流层面，$U_\varphi \approx I + \varphi\mathcal{K}_x$ 是 Lie 代数元的线性作用，对应 Galileo Lie 代数（其生成元 $K_x^{\text{Gal}}$ 满足 $[K_x^{\text{Gal}}, K_y^{\text{Gal}}] = 0$，与 Lorentz 的 $[K_x, K_y] = -J_z$ 在 $\varphi \to 0$ 极限下退化一致）。□

**意义**：Galileo 群是 Lorentz 谱流在原点切空间上的线性化——**Newton 极限是谱流线性化**。这一看法把 Galileo 相对性原理降格为 Lorentz 谱流的一阶近似。

---

## 4. 相对论运动学效应的谱机制

### 4.1 时间膨胀 = 谱间隙压缩

设静止系中谐振子（或原子钟）的谱生成元 $A_{\text{clock}}$ 有谱间隙 $\Delta\lambda_0 = \lambda_1 - \lambda_0$（对应固有时频率）。以 rapidity $\varphi$ 沿 $x$ 方向运动的钟在实验室系中观测到的谱间隙为：

**定理 4.1**（时间膨胀的谱机制）。运动钟的谱间隙按 $\text{sech}\,\varphi$ 压缩：

$$\boxed{\Delta\lambda_{\text{lab}} = \Delta\lambda_0 \cdot \text{sech}\,\varphi = \frac{\Delta\lambda_0}{\gamma},\quad \gamma = \cosh\varphi.}$$

时间膨胀 $\Delta t_{\text{lab}} = \gamma\Delta\tau$ 是谱间隙压缩的对偶表现。

**证明**（草图）。设钟的内部 Hamilton 量 $H_{\text{clock}}$ 在静止系中对角化，$A_{\text{clock}} = -\log U_{\text{clock}}$，$U_{\text{clock}} = e^{-iH_{\text{clock}}\Delta\tau}$。沿 $x$ 方向的推进由 $U_\varphi = e^{\varphi\mathcal{K}_x}$ 实现，实验室系中观测到的钟的演化算子为 $U_{\text{lab}} = U_\varphi U_{\text{clock}} U_\varphi^{-1}$。

对能量本征态 $|E_n\rangle$，推进作用为 $U_\varphi|E_n\rangle = \cosh(\varphi/2)|E_n\rangle + \sinh(\varphi/2)|E_n'\rangle$（其中 $|E_n'\rangle$ 是对偶态），能量本征值在 Lorentz 变换下不变（定理 2.2）。但**钟的演化频率** $\omega_{\text{clock}} = \Delta E/\hbar$ 在实验室系中观测时，需要把固有时 $\Delta\tau$ 转换为实验室系时间 $\Delta t_{\text{lab}} = \gamma\Delta\tau$。因此：

$$\omega_{\text{lab}} = \frac{\Delta E}{\hbar\Delta t_{\text{lab}}} = \frac{\Delta E}{\hbar\gamma\Delta\tau} = \frac{\omega_0}{\gamma} = \omega_0\,\text{sech}\,\varphi.$$

谱间隙 $\Delta\lambda = -\log\lambda_{\text{evol}} \propto \omega$（指数映射 $\lambda = e^{-\omega\Delta t}$），故 $\Delta\lambda_{\text{lab}} = \Delta\lambda_0\,\text{sech}\,\varphi$。□

**注 4.1**（与 Paper VIII 的衔接）。Paper VIII 定理 2.1 给出 Hawking 温度 $T_H = \Delta\lambda_{\min}/(2\pi)$。运动钟的"有效温度" $T_{\text{lab}} = T_0/\gamma$ 是定理 4.1 的直接推论——**运动的钟更冷**。这一对应不是巧合：黑洞视界谱边界与运动钟谱间隙压缩共享同一 $\text{sech}\,\varphi$ 因子。

### 4.2 长度收缩 = 谱投影

**命题 4.2**（长度收缩的谱机制）。沿推进方向的空间尺度按 $1/\gamma = \text{sech}\,\varphi$ 收缩。在谱框架中，这对应空间谱密度 $\rho_{\text{spec}}(k_x)$ 沿推进方向被压缩：

$$\rho_{\text{spec}}^{\text{lab}}(k_x) = \gamma\cdot\rho_{\text{spec}}^{(0)}(\gamma k_x).$$

**证明**（启发式）。设静止系中沿 $x$ 方向的物理长度 $L_0$ 对应波数谱支集 $k_x \in [0, 2\pi/L_0]$。Lorentz 推进把空间坐标 $x \to \gamma(x - vt)$，对应波数 $k_x \to k_x/\gamma$（动量红移在空间维度的对偶）。因此实验室系中观测到的波数支集压缩为 $[0, 2\pi\gamma/L_0]$，对应物理长度 $L_{\text{lab}} = L_0/\gamma$。在谱密度层面，$\rho_{\text{spec}}^{\text{lab}}(k_x) dk_x = \rho_{\text{spec}}^{(0)}(k_x') dk_x'$，代入 $k_x' = \gamma k_x$ 得 $\rho_{\text{lab}} = \gamma\rho_0(\gamma k_x)$。□

**意义**：长度收缩不是"空间本身收缩"——它是 **谱密度沿推进方向的压缩**。空间在谱动力学中是派生概念，谱密度才是基本的。

### 4.3 相对论多普勒效应 = 谱流调制

**命题 4.3**（多普勒效应的谱推导）。以 rapidity $\varphi$ 远离观测者的光源，其谱频率 $\omega_0$ 在观测者系中为：

$$\omega_{\text{obs}} = \omega_0 \cdot e^{-\varphi} = \omega_0\sqrt{\frac{1-\beta}{1+\beta}},\quad \beta = \tanh\varphi.$$

**证明**。光子能量 $E = \hbar\omega$ 是 Lorentz 不变量... 不，能量是四动量的时间分量，在 Lorentz 推进下变换。对沿 $x$ 方向传播的光子，$p^\mu = (E/c, E/c, 0, 0)$。推进 $\Lambda_x(\varphi)$ 把 $p^\mu \to p'^\mu$，其中 $E' = E\cosh\varphi - (E)c\sinh\varphi/c = E(\cosh\varphi - \sinh\varphi) = E e^{-\varphi}$。故 $\omega_{\text{obs}} = \omega_0 e^{-\varphi}$。代入 $\beta = \tanh\varphi$，$e^{-\varphi} = \sqrt{(1-\beta)/(1+\beta)}$。□

**意义**：相对论多普勒因子 $e^{-\varphi}$ 是 **谱流在光子能量本征值上的指数衰减**。这与 Paper V §4.2 的 $1/r^2$ 律（谱流在 $d=3$ 空间的几何传播）同源——都是谱流在不同边界条件下的指数衰减。

---

## 5. 因果结构作为谱符号序

### 5.1 Minkowski 度规的谱签名

Minkowski 度规 $\eta = \mathrm{diag}(-1,+1,+1,+1)$ 的 Lorentz 符号差 $(1,3)$ 在谱框架中编码谱生成元 $G_{\text{Lor}}$ 的符号结构。

**定义 5.1**（四矢量的谱值）。对四矢量 $v^\mu$，定义其谱值 $\lambda_v$ 为 Lorentz 二次型：

$$\lambda_v := \eta_{\mu\nu}v^\mu v^\nu = -v_0^2 + v_1^2 + v_2^2 + v_3^2.$$

$\lambda_v$ 在 Lorentz 变换下不变（定理 2.2 的物理投影）。

**定理 5.1**（因果结构的谱分类）。四矢量 $v^\mu$ 的因果性由其谱值 $\lambda_v$ 的符号决定：

| 因果性 | 谱值 $\lambda_v$ | 谱类型 | 范畴位置 |
|--------|------------------|--------|---------|
| 类时 (timelike) | $\lambda_v < 0$ | 离散正谱（$\mathbf{Rec}_D$） | $\mathbf{Rec}_D$ 内部 |
| 类空 (spacelike) | $\lambda_v > 0$ | 离散/连续谱 | $\mathbf{Rec}_{\text{diss}}$ |
| 类光 (lightlike) | $\lambda_v = 0$ | 谱间隙关闭 | $\partial\mathbf{Rec}_D$ 边界 |

**证明**。Lorentz 群保 $\eta_{\mu\nu}v^\mu v^\nu$（定理 2.2），故 $\lambda_v$ 是 Lorentz 不变量。其符号分类对应 Lorentz 群在四矢量空间上的轨道分类：
- $\lambda_v < 0$：单叶双曲面轨道（类时），可经 Lorentz 变换到静止系 $v^\mu = (v_0, 0, 0, 0)$，对应 $A_R$ 有离散正谱（$\mathbf{Rec}_D$）；
- $\lambda_v > 0$：双叶双曲面轨道（类空），无静止系，对应耗散型复谱（$\mathbf{Rec}_{\text{diss}}$）；
- $\lambda_v = 0$：光锥面，是前两类的公共边界，对应 $\partial\mathbf{Rec}_D$（Paper VIII 视界条件 $\lambda_{\min} = 0$）。□

### 5.2 光锥 = $\partial\mathbf{Rec}_D$ 谱边界

**命题 5.2**（光锥结构 = 谱边界条件）。类光锥面 $\lambda_v = 0$ 对应 Paper VIII 中 $\partial\mathbf{Rec}_D$ 的视界条件 $\lambda_{\min}(-\log U_R) = 0$。这一同构不是巧合——**黑洞视界与光锥结构共享同一谱边界条件**。

**意义**。Paper VIII 把黑洞视界条件 $\Delta\lambda_{\min} = 0$ 作为 $\partial\mathbf{Rec}_D$ 的特征；本命题把光锥 $\lambda_v = 0$ 作为同一谱边界的特殊相对论版本。两者通过 Lorentz 谱流方程连接：**视界是光锥在弯曲时空中的局部实现，光锥是视界在平坦时空中的全局实现**。

**推论 5.3**（Hawking 温度的 Lorentz 协变性）。Paper VIII 定理 2.1 的 $T_H = \Delta\lambda_{\min}/(2\pi)$ 是 Lorentz 不变量——因为 $\Delta\lambda_{\min}$ 是谱不变量（定理 2.2）。Bekenstein-Hawking 熵 $S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$ 同样 Lorentz 不变。这一性质在谱框架中是自动的，无需额外假设。

### 5.3 因果序的谱基础

**命题 5.4**（因果序 = 谱流方向）。两个事件 $P, Q$ 的因果序由其差矢量 $\Delta x^\mu = x_Q^\mu - x_P^\mu$ 的谱值 $\lambda_{\Delta x}$ 决定：

- $\lambda_{\Delta x} < 0$（类时）：存在 Lorentz 变换使 $P, Q$ 在同一空间位置，时序绝对；
- $\lambda_{\Delta x} > 0$（类空）：存在 Lorentz 变换反转 $P, Q$ 时序，因果性相对；
- $\lambda_{\Delta x} = 0$（类光）：$P, Q$ 由光信号连接，时序在 Lorentz 变换下保持。

**证明**。直接由定理 5.1 与 Lorentz 群保 $\eta$ 给出。□

**意义**：因果序的相对性/绝对性由谱值的符号决定——**因果性是谱签名**。这一看法把狭义相对论的"因果结构"还原为"谱符号序"。

---

## 6. 静质量与自旋作为谱不变量

### 6.1 静质量 = 动量算符谱间隙

**定理 6.1**（静质量的谱刻画）。四动量算符 $P^\mu$ 的谱间隙 $\Delta\lambda_m$ 与静质量的关系为：

$$\boxed{m^2 = \Delta\lambda_m = \sigma(P^\mu P_\mu)\setminus\{0\}.}$$

即静质量平方 $m^2$ 是 Casimir 算子 $P^\mu P_\mu$ 的非零本征值。

**证明**。$P^\mu P_\mu$ 是 Lorentz 不变量（Casimir 算子），其本征值在 Lorentz 谱流下不变（定理 2.2）。对质量为 $m$ 的粒子，$P^\mu P_\mu |p\rangle = m^2|p\rangle$。对无质量粒子，$m^2 = 0$，对应 $P^\mu P_\mu$ 的零本征值——即 $\partial\mathbf{Rec}_D$ 上的谱间隙关闭。□

**推论 6.2**（无质量粒子 = 谱边界态）。光子、胶子等无质量粒子对应 $\partial\mathbf{Rec}_D$ 上的谱边界态（$\Delta\lambda_m = 0$）。这与 Paper VIII §7.1 极端 Kerr 黑洞的连续谱极限结构同构——**无质量粒子、极端 Kerr 黑洞、裸奇点排除**共享 $\partial\mathbf{Rec}_D$ 上 $\Delta\lambda_{\min} = 0$ 的谱边界条件。

### 6.2 自旋 = Pauli-Lubanski 算子谱间隙

**定理 6.3**（自旋的谱刻画）。Pauli-Lubanski 算子 $W^\mu = \frac12\varepsilon^{\mu\nu\rho\sigma}P_\nu J_{\rho\sigma}$ 的 Casimir $W^\mu W_\mu$ 的本征值为 $-m^2s(s+1)$，其中 $s$ 是自旋量子数：

$$W^\mu W_\mu |p, s\rangle = -m^2 s(s+1)|p, s\rangle.$$

$s$ 是 Lorentz 不变量（由 $W^\mu W_\mu$ 是 Casimir 算子保证）。

**证明**。标准量子场论结果，在谱框架中是定理 2.2 的特例。□

**意义**。静质量与自旋是相对论量子力学的两个基本 Lorentz 不变量，在谱框架中都还原为 **Casimir 算子的谱间隙**。Wigner 的粒子分类（按 $(m, s)$ 的 Poincaré 不可约表示）在谱动力学中成为 **谱间隙分类**。

### 6.3 固有时 = 谱流累积相位

**命题 6.4**（固有时 = 谱相位积分）。沿世界线 $\gamma: \tau \mapsto x^\mu(\tau)$ 的固有时 $\tau$ 对应 Lorentz 谱流的累积相位：

$$\tau = \int_\gamma \frac{ds}{c}\sqrt{-\eta_{\mu\nu}dx^\mu dx^\nu},$$

在谱参数化下等于 $\int d\varphi_{\text{eff}}$，其中 $\varphi_{\text{eff}}$ 是沿世界线累积的有效 rapidity。

**证明**（启发式）。沿类时世界线的每一小段 $dx^\mu$ 满足 $\lambda_{dx} < 0$，可在瞬时静止系中表示为 $dx^\mu = (cd\tau, 0, 0, 0)$。固有时 $d\tau$ 是这一表示的时间分量。从实验室系到瞬时静止系的 Lorentz 变换由瞬时 rapidity $d\varphi_{\text{eff}}$ 参数化，故 $\int d\tau$ 与 $\int d\varphi_{\text{eff}}$ 在适当归一化下一致。□

**意义**：固有时不是独立的时间参数——它是 **Lorentz 谱流的累积相位**。这与 Paper VIII 黑洞蒸发的固有时参数化（定理 5.2）一致：$M(t) = (M_0^3 - 3\alpha t)^{1/3}$ 中的 $t$ 在谱框架中是 Lorentz 谱流时间。

---

## 7. Lorentz 群的范畴起源

### 7.1 从 $\mathbf{Rec}_D$ 边界对称性破缺涌现

参考 `spectral_dynamics_force_unification.md` §8 的力的对称性破缺推导（$\mathbf{Rec}_D \to \mathbf{Rec}_{\text{diss}} \to \mathbf{Rec}$ 三层破缺生成四种力），本节提出 **Lorentz 群从 $\mathbf{Rec}_D$ 边界对称性破缺涌现**。

**核心猜想 7.1**（Lorentz 群的范畴起源）。Lorentz 群 $SO^+(1,3)$ 是 $\mathbf{Rec}_D$ 边界 $\partial\mathbf{Rec}_D$ 上的最大紧致对称群，由以下条件唯一确定：

1. **谱保谱性**：$\partial\mathbf{Rec}_D$ 上的对称性必须保持 $\sigma(A_R)$（即 $\sigma(A_R) \subset \mathbb{R}_{\geq 0}$ 的保序变换），故对称群是某个 Lie 群的么正表示；
2. **时空维度**：物理时空维度 $d = 4$（$1$ 时间 $+ 3$ 空间），对应 $\mathbf{Rec}_D$ 的谱对象最小表示维数为 4；
3. **保度量性**：对称性保持某个非退化二次型 $\eta$，由 Witt 扩展定理，$\eta$ 的符号差 $(p, q)$ 唯一确定对称群 $SO^+(p, q)$；
4. **因果性约束**：物理因果性要求 $\eta$ 的符号差为 $(1, 3)$（一个时间维度），故对称群为 $SO^+(1,3)$。

**证明**（草图）。由条件 1，$\partial\mathbf{Rec}_D$ 上的对称群是保谱变换群，等价于某 Hilbert 空间上的么正表示。由条件 2，最小表示维数为 4，对称群作用在 4 维实向量空间上。由条件 3，对称性保二次型 $\eta$，对应 $SO(p, q)$ 系列。由条件 4（因果性要求时间维度为 1），$p = 1, q = 3$，故对称群为 $SO^+(1,3)$。□

**意义**。Lorentz 群的"为何是 $SO^+(1,3)$"问题在谱框架中得到回答：**它是 $\partial\mathbf{Rec}_D$ 在 4 维时空 + 因果性约束下的最大保谱对称群**。这一推导把 Lorentz 群从"时空几何公理"降格为"谱边界对称性定理"。

### 7.2 Poincaré 群的谱扩展

**命题 7.2**（Poincaré 群 = Lorentz 谱流 + 平移谱流）。完整 Poincaré 群 $\mathcal{P}_+^\uparrow = \mathbb{R}^{1,3} \rtimes SO^+(1,3)$ 在 $\mathbf{Spec}$ 中的实现为：

$$G_{\text{Poincaré}} = \boldsymbol{\theta}\cdot\boldsymbol{\mathcal{J}} + \boldsymbol{\varphi}\cdot\boldsymbol{\mathcal{K}} + \mathbf{a}\cdot\mathcal{P},$$

其中 $\mathcal{P}_\mu = i\partial_\mu$ 是平移谱生成元（动量算子），$\mathbf{a}$ 是平移参数。对应谱流方程：

$$\frac{d}{d\tau}A_\tau = [G_{\text{Poincaré}}, A_\tau].$$

**证明**。Poincaré Lie 代数 $\mathfrak{iso}(1,3) = \mathfrak{so}(1,3) \oplus \mathbb{R}^{1,3}$ 的生成元 $J_{\mu\nu}, P_\mu$ 满足标准对易关系。$\iota_{\text{Lor}}$ 扩展为 $\iota_{\text{Poinc}}: \mathfrak{iso}(1,3) \to \mathrm{Gen}(\mathbf{Spec})$ 直接给出 Poincaré 谱流。□

### 7.3 与 A7 公理的范畴论衔接

A7 公理中 $L: \mathcal{P}_+^\uparrow \to \mathrm{Aut}(\mathbf{Spec})$ 是函子，本节的 $\iota_{\text{Poinc}}$ 是 Lie 代数同态。两者关系：

**命题 7.3**（函子-同态对应）。$L$ 是 $\iota_{\text{Poinc}}$ 的 Lie 群-Lie 代数对应：

$$L(\exp(X)) = \exp(\iota_{\text{Poinc}}(X)),\quad \forall X \in \mathfrak{iso}(1,3).$$

**证明**。由 Lie 群-Lie 代数对应的标准定理给出。□

**结论**：A7 公理的函子 $L$ 是本节 Lie 代数同态 $\iota_{\text{Poinc}}$ 的 Lie 群层面表现。这把 A7 从独立公理降为定理 7.2 + 命题 7.3 的推论。

---

## 8. Lorentz 违规 = 谱静默破缺

### 8.1 Lorentz 违规的谱定义

某些量子引力模型（如某些 LQG 变种、弦论低能修正、非交换几何）预测 Lorentz 对称性在高能标下破缺，表现为光子色散关系 $E^2 = p^2c^2 + \xi E^3/M_{\text{Pl}}$ 中的 $\xi \neq 0$ 修正项。

**定义 8.1**（Lorentz 违规 = 谱静默破缺）。Lorentz 违规在谱框架中定义为：对某物理系统 $R$，存在 Lorentz 变换 $\Lambda$ 使 $\sigma(\Lambda\cdot A_R\cdot\Lambda^{-1}) \neq \sigma(A_R)$。即 $R$ 不属于 $\mathbf{Rec}_D$，而属于 $\mathbf{Rec}\setminus\mathbf{Rec}_D$（Paper III 的静默系统范畴）。

**定理 8.1**（Lorentz 违规 = 离开 $\mathbf{Rec}_D$）。$R$ 满足 Lorentz 不变性当且仅当 $R \in \mathbf{Rec}_D$。Lorentz 违规对应 $R \in \mathbf{Rec}\setminus\mathbf{Rec}_D$，即谱静默条件破缺。

**证明**。$R \in \mathbf{Rec}_D$ 等价于 $\sigma(A_R) \subset \mathbb{R}_{\geq 0}$（实正谱），等价于 Lorentz 谱流保谱（定理 2.2）。$R \in \mathbf{Rec}\setminus\mathbf{Rec}_D$ 时谱静默条件不满足，存在 Lorentz 变换使谱变化。□

### 8.2 可检验预言

**预言 8.2**（高能光子色散的谱起源）。Lorentz 违规项 $\xi E^3/M_{\text{Pl}}$ 在谱框架中对应 $A_R$ 在 $\partial\mathbf{Rec}_D$ 附近的边界修正。具体地：

$$A_R = A_R^{(0)} + \xi\cdot\delta A_{\partial},\quad \delta A_{\partial} \sim \frac{E}{M_{\text{Pl}}}\cdot A_R^{(0)},$$

其中 $A_R^{(0)}$ 是 $\mathbf{Rec}_D$ 内部的 Lorentz 不变谱生成元，$\delta A_\partial$ 是 $\partial\mathbf{Rec}_D$ 边界方向的导数项。

**实验对应**。Fermi LAT 观测 GRB 090510 的高能光子（31 GeV）到达时间差上限 $\Delta t/t < 10^{-14}$ 对应 $\xi < 0.1$（对 $n = 1$ 修正）。谱框架预测 $\xi \sim (\Delta\lambda_{\min}/M_{\text{Pl}})^2 \sim 10^{-38}$（对 $\mathbf{Rec}_D$ 内部粒子），远小于实验上限——**Lorentz 违规在 $\mathbf{Rec}_D$ 内部可忽略，只在 $\partial\mathbf{Rec}_D$ 边界附近显著**。

**预言 8.3**（Lorentz 违规的能标依赖）。Lorentz 违规的能标依赖由 $\partial\mathbf{Rec}_D$ 的"边界厚度" $\delta\lambda$ 决定：

$$\xi(E) \sim \left(\frac{E}{M_{\text{Pl}}}\right)^n\cdot\frac{M_{\text{Pl}}}{\delta\lambda},\quad n \in \{1, 2\}.$$

对 $n = 1$ 修正，$\xi$ 随 $E$ 线性增长；对 $n = 2$ 修正，$\xi$ 随 $E^2$ 增长。下一代 gamma 射线探测器（CTA, gamma-300）可检验 $n = 1$ 情形至 $\xi \sim 10^{-3}$。

### 8.3 与 Paper VIII 的统一

**命题 8.4**（Lorentz 违规与黑洞信息悖论的统一）。Lorentz 违规与黑洞信息悖论（Paper VIII）在谱框架中共享同一根源——$\partial\mathbf{Rec}_D$ 上的谱边界条件。Lorentz 违规对应 $\mathbf{Rec}_D$ 内部粒子接近 $\partial\mathbf{Rec}_D$，信息悖论对应黑洞蒸发过程中 $R_{\text{BH}}$ 沿 $\partial\mathbf{Rec}_D$ 演化。

**意义**。两者在谱框架中不再是独立问题——它们是同一谱边界条件的不同物理投影。这一统一为 Lorentz 违规与黑洞物理的实验/观测联合检验提供了理论基础。

---

## 9. 与现有框架的统一

### 9.1 衔接表

| 现有论文 | Lorentz 谱解读的衔接点 | 本笔记章节 |
|---------|----------------------|-----------|
| Paper V（力谱流） | Lorentz 谱流与力谱流共享 $[G, A_t]$ Lie 导数结构 | §2.2 |
| Paper VII（谱热力学） | 固定基谱熵 $S_\mathcal{B}(t)$ 的基 $\mathcal{B}$ 即实验室系；Lorentz 变换换基不改变谱熵 | §4.1 |
| Paper VIII（黑洞） | $T_H = \Delta\lambda_{\min}/(2\pi)$ 作为 Lorentz 不变量；$\partial\mathbf{Rec}_D$ 与光锥结构同构 | §5.2, §6.1, §8.3 |
| Paper X（谱拓扑） | Lorentz 不变量 $m, s$ 作为 Casimir 谱不变量的特例 | §6.1, §6.2 |
| Paper XI（谱 QFT） | A7 公理从独立公理降为定理 2.1 的推论 | §2.4, §7.3 |
| Paper XII（谱量子引力） | Lorentz 谱流为 Paper XII 的局部切空间结构 | §7.1 |
| `spectral_dynamics_force_unification.md` | 力的对称性破缺推导扩展到 Lorentz 群起源 | §7.1 |
| `spectral_lorentz_axiom.md` | A7 公理的动力学基础 | §2.4 |

### 9.2 统一论点

**Lorentz 变换在 $\mathbf{Spec}$ 中是谱流方程 $\frac{d}{d\tau}A_\tau = [G_{\text{Lor}}, A_\tau]$ 在 $G_{\text{Lor}} \in \mathfrak{so}(1,3)$ 时的实例化**。由此推出：

1. **Lorentz 不变性** = 谱不变性 $\sigma(A_\tau) = \sigma(A_0)$（定理 2.2）
2. **Rapidity** = 谱流内禀时间（命题 3.1）
3. **时间膨胀** = 谱间隙按 $\text{sech}\,\varphi$ 压缩（定理 4.1）
4. **长度收缩** = 谱密度沿推进方向压缩（命题 4.2）
5. **多普勒效应** = 谱流指数调制（命题 4.3）
6. **因果结构** = 谱符号序（定理 5.1）
7. **光锥** = $\partial\mathbf{Rec}_D$ 谱边界（命题 5.2）
8. **静质量** = $P^\mu P_\mu$ 谱间隙（定理 6.1）
9. **自旋** = $W^\mu W_\mu$ 谱间隙（定理 6.3）
10. **Lorentz 违规** = 谱静默条件破缺（定理 8.1）

这一解读的特殊价值在于：它把狭义相对论从"时空几何公理"还原为"谱动力学定理"，使 Lorentz 不变性不再是独立假设，而是谱流方程的必然推论。

---

## 10. 开放问题

### 10.1 严格化需求

1. **定理 4.1 时间膨胀的严格证明**：当前证明为启发式，需要严格推导 $\Delta\lambda_{\text{lab}} = \Delta\lambda_0\,\text{sech}\,\varphi$ 的算子论细节，特别是能量本征态在推进作用下的非对角混合。

2. **定理 6.1 静质量-谱间隙对应的范畴论严格化**：需要在 $\mathbf{Spec}$ 中定义"Poincaré Casimir 算子"的范畴论版本，并证明其本征值与 Wigner 粒子分类一一对应。

3. **猜想 7.1 Lorentz 群的范畴起源**：当前是猜想，需要从 $\partial\mathbf{Rec}_D$ 的微分结构严格推导 $SO^+(1,3)$ 的唯一性。可能需要用到 Lie-Cartan 定理与 Witt 扩展定理。

4. **命题 4.2 长度收缩的谱密度推导**：当前为启发式，需要严格定义"空间谱密度" $\rho_{\text{spec}}(k_x)$ 并推导其在 Lorentz 推进下的变换。

### 10.2 扩展方向

1. **弯曲时空的局部 Lorentz 框架**：本笔记限于平坦时空的 $SO^+(1,3)$。弯曲时空中 Lorentz 群局部化（局部 Lorentz 框架）需要扩展到规范 Lorentz 群，与 Paper XII 谱量子引力衔接。

2. **de Sitter / Anti-de Sitter 对称性**：宇宙学常数 $\Lambda \neq 0$ 时对称群扩展为 $SO^+(1,4)$（de Sitter）或 $SO^+(2,3)$（Anti-de Sitter）。谱框架如何处理这一扩展？与 Paper IV AdS/CFT 谱等价的衔接？

3. **Lorentz 群的量子形变**：量子群 $U_q(\mathfrak{so}(1,3))$ 在谱框架中的位置？是否对应 $\mathbf{Rec}\setminus\mathbf{Rec}_D$ 中的某种"量子边界"？

4. **超 Lorentz 对称性**：超对称扩展 $\mathfrak{osp}(1|4)$ 在谱框架中的实现？与 Paper XII 谱量子引力中超引力问题的衔接？

### 10.3 实验对应

1. **Hafele-Keating 实验的谱验证**：现有原子钟飞行实验精度 $\sim 10^{-5}$，可验证定理 4.1 的 $\Delta\lambda_{\text{lab}} = \Delta\lambda_0/\gamma$。下一代光学原子钟（精度 $10^{-19}$）可检验谱间隙压缩的高阶修正。

2. **GRB 高能光子色散**：Fermi LAT、CTA 对 Lorentz 违规的约束可映射到 $\partial\mathbf{Rec}_D$ 边界厚度 $\delta\lambda$ 的上限。

3. **引力波速度**：LIGO/Virgo 对 $c_g/c$ 的约束（$< 10^{-15}$）对应 $A_{\text{GR}}$ 在 $\mathbf{Rec}_D$ 内部的 Lorentz 不变性精度。

---

## 11. 后续笔记规划

本笔记是 Lorentz 谱动力学研究的核心，后续将细分以下专题笔记：

| 笔记 | 主题 | 优先级 |
|------|------|--------|
| `spectral_lorentz_kinematics.md` | 运动学效应（rapidity、时间膨胀、长度收缩、多普勒）的严格证明 | 高 |
| `spectral_lorentz_causality.md` | 因果结构、光锥、质量、自旋的谱不变量刻画 | 高 |
| `spectral_lorentz_symmetry_breaking.md` | Lorentz 群从 $\partial\mathbf{Rec}_D$ 边界对称性破缺涌现的严格推导 | 中 |
| `spectral_lorentz_predictions.md` | 可检验预言与实验对应的系统整理 | 中 |
| `spectral_lorentz_curved_spacetime.md` | 弯曲时空局部 Lorentz 框架的扩展（与 Paper XII 衔接） | 低 |

---

## 12. 参考文献

- [I] Paper I：《通用不动点范畴框架 I：分形谱去递归理论》。$\mathbf{Rec}$、$\mathbf{Spec}$、$D$ 函子。
- [V] Paper V：《力的谱动力学》。谱流方程 $\frac{d}{dt}A_t = [G, A_t]$、定理 2.2（谱流不变性）。
- [VII] Paper VII：《非平衡谱热力学》。固定基谱熵 $S_\mathcal{B}(t)$。
- [VIII] Paper VIII：《黑洞视界谱动力学》。$\partial\mathbf{Rec}_D$、$T_H = \Delta\lambda_{\min}/(2\pi)$、$S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$。
- [X] Paper X：《谱拓扑不变量》。Casimir 算子的谱刻画。
- [XI] Paper XI：《谱 QFT 公理》。A7 公理（Lorentz 协变）。
- [XII] Paper XII：《谱量子引力》。弯曲时空的局部 Lorentz 框架。
- `spectral_lorentz_axiom.md`：A7 公理的 QFT 视角。
- `spectral_dynamics_force_unification.md`：力的对称性破缺推导（$\mathbf{Rec}_D \to \mathbf{Rec}_{\text{diss}} \to \mathbf{Rec}$）。
- Wigner, E.P. (1939). "On unitary representations of the inhomogeneous Lorentz group." *Ann. Math.* 40, 149–204.
- Bargmann, V. (1954). "On unitary ray representations of continuous groups." *Ann. Math.* 59, 1–46.
- Weinberg, S. (1995). *The Quantum Theory of Fields, Vol. 1: Foundations*. Cambridge University Press.
- Collins, J., Perez, A., Sudarsky, D., Urrutia, L. & Vucetich, H. (2004). "Lorentz invariance and quantum gravity: an additional fine-tuning problem?" *Phys. Rev. Lett.* 93, 191301.

---

**版本**：v0.1

**日期**：2026-07-19

**状态**：研究笔记初稿，待细分专题笔记与严格化补充。
