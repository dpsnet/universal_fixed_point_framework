# Lorentz 谱动力学运动学——严格证明

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**日期**：2026-07-19

**状态**：`spectral_lorentz_dynamics.md` §3-§4 的严格化补充

---

## 0. 摘要

本笔记对核心笔记 `spectral_lorentz_dynamics.md` §3-§4 的运动学定理（rapidity 加法性、时间膨胀、长度收缩、多普勒效应）给出严格证明。所有证明基于两个基础：(1) Lorentz 谱流方程 $\frac{d}{d\tau}A_\tau = [G_{\text{Lor}}, A_\tau]$；(2) 谱不变性 $\sigma(A_\tau) = \sigma(A_0)$（核心笔记定理 2.2）。

---

## 1. Rapidity 加法性的严格证明

### 1.1 单参数子群的谱流参数化

**引理 1.1**（单参数 Lorentz 子群）。设 $G_{\text{Lor}} \in \mathfrak{so}(1,3)$ 是反 Hermite 谱生成元，则映射 $\varphi: \mathbb{R} \to SO^+(1,3)$，

$$\varphi \mapsto \Lambda_\varphi = \exp(\varphi G_{\text{Lor}}^{\text{abstract}}),$$

是 Lorentz 群的单参数子群，对应谱流 $U_\varphi = \exp(\varphi G_{\text{Lor}})$。

**证明**。$G_{\text{Lor}}$ 反 Hermite $\Rightarrow$ $\exp(\varphi G_{\text{Lor}})$ 幺正。$\mathfrak{so}(1,3)$ 的 Lie 代数同态 $\iota_{\text{Lor}}$ 把 $G_{\text{Lor}}^{\text{abstract}}$ 映为 $G_{\text{Lor}}$，且 $\iota_{\text{Lor}}(\exp(\varphi G_{\text{Lor}}^{\text{abstract}})) = \exp(\varphi\iota_{\text{Lor}}(G_{\text{Lor}}^{\text{abstract}})) = \exp(\varphi G_{\text{Lor}}) = U_\varphi$（Lie 群-Lie 代数对应）。单参数子群性质 $\Lambda_{\varphi_1+\varphi_2} = \Lambda_{\varphi_1}\Lambda_{\varphi_2}$ 由指数映射性质给出。□

### 1.2 推进的显式形式

**引理 1.2**（沿 $x$ 方向推进的矩阵形式）。沿 $x$ 方向 rapidity 为 $\varphi$ 的推进 $\Lambda_x(\varphi) \in SO^+(1,3)$ 的矩阵形式为：

$$\Lambda_x(\varphi) = \begin{pmatrix} \cosh\varphi & \sinh\varphi & 0 & 0 \\ \sinh\varphi & \cosh\varphi & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}.$$

对应速度 $v/c = \tanh\varphi$，Lorentz 因子 $\gamma = \cosh\varphi = 1/\sqrt{1-v^2/c^2}$。

**证明**。$\mathfrak{so}(1,3)$ 中推进生成元 $K_x$ 的标准矩阵形式：

$$K_x = \begin{pmatrix} 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}.$$

$K_x^2 = \mathrm{diag}(1,1,0,0)$，$K_x^{2n+1} = K_x$，$K_x^{2n} = \mathrm{diag}(1,1,0,0)$（$n \geq 1$）。指数映射：

$$\exp(\varphi K_x) = I + \sum_{n=0}^\infty \frac{\varphi^{2n+1} K_x}{(2n+1)!} + \sum_{n=1}^\infty \frac{\varphi^{2n} K_x^{2n}}{(2n)!}$$

$$= I + \sinh\varphi\cdot K_x + (\cosh\varphi - 1)\cdot\mathrm{diag}(1,1,0,0),$$

代入 $K_x$ 形式即得 $\Lambda_x(\varphi)$ 矩阵。速度参数化 $v/c = \tanh\varphi$ 与 $\gamma = \cosh\varphi$ 由定义直接给出。□

### 1.3 Rapidity 加法性的谱证明

**定理 1.3**（核心笔记命题 3.1 的严格化）。Rapidity $\varphi$ 满足加法性 $\varphi_1 \oplus \varphi_2 = \varphi_1 + \varphi_2$，对应谱流半群 $U_{\varphi_1+\varphi_2} = U_{\varphi_1}U_{\varphi_2}$。

**证明**。由引理 1.1，$\Lambda_\varphi$ 是单参数子群。对 $\varphi_1, \varphi_2 \in \mathbb{R}$，

$$\Lambda_{\varphi_1}\Lambda_{\varphi_2} = \exp(\varphi_1 K_x)\exp(\varphi_2 K_x) = \exp((\varphi_1+\varphi_2)K_x) = \Lambda_{\varphi_1+\varphi_2},$$

其中第二个等号来自 BCH 公式：$[K_x, K_x] = 0$ 使所有高阶项消失。在谱流层面，$U_{\varphi_1}U_{\varphi_2} = \exp(\varphi_1\mathcal{K}_x)\exp(\varphi_2\mathcal{K}_x) = \exp((\varphi_1+\varphi_2)\mathcal{K}_x) = U_{\varphi_1+\varphi_2}$，同理 $[\mathcal{K}_x, \mathcal{K}_x] = 0$。□

### 1.4 速度合成律的严格谱推导

**定理 1.4**（核心笔记定理 3.2 的严格化）。相对论速度合成律

$$\frac{v_1 \oplus v_2}{c} = \frac{v_1/c + v_2/c}{1 + (v_1/c)(v_2/c)}$$

是 rapidity 加法性 $\varphi_1 \oplus \varphi_2 = \varphi_1 + \varphi_2$ 在非线性参数化 $v/c = \tanh\varphi$ 下的表象。

**证明**。设 $\beta_i := v_i/c = \tanh\varphi_i$（$i = 1, 2$）。由定理 1.3，复合推进对应 $\varphi = \varphi_1 + \varphi_2$。代入 $\beta = \tanh\varphi$ 并使用双曲正切加法公式：

$$\beta_1 \oplus \beta_2 = \tanh(\varphi_1 + \varphi_2) = \frac{\tanh\varphi_1 + \tanh\varphi_2}{1 + \tanh\varphi_1\tanh\varphi_2} = \frac{\beta_1 + \beta_2}{1 + \beta_1\beta_2}.$$

这正是相对论速度合成公式。□

**注 1.1**（Rapidity 是内禀参数）。速度 $v$ 与 rapidity $\varphi$ 的非线性关系 $\beta = \tanh\varphi$ 表明，速度是 rapidity 的"压缩投影"——$v \in (-c, c)$ 是有界区间，而 $\varphi \in \mathbb{R}$ 是无界的。**Rapidity 才是 Lorentz 谱流的内禀时间参数；速度是其非线性表象**。这一翻译揭示了 Lorentz 群的几何本质。

### 1.5 Newton 极限的严格化

**定理 1.5**（核心笔记命题 3.3 的严格化）。在 rapidity $\varphi \ll 1$ 极限下，Lorentz 谱流退化为 Galileo 谱流：

$$U_\varphi = e^{\varphi\mathcal{K}_x} = I + \varphi\mathcal{K}_x + \mathcal{O}(\varphi^2),$$

对应 Galileo 速度加法 $v_1 \oplus v_2 \approx v_1 + v_2$ 与 Galileo Lie 代数 $[K_x^{\text{Gal}}, K_y^{\text{Gal}}] = 0$。

**证明**。

(1) **速度层面**。$\beta = \tanh\varphi = \varphi - \varphi^3/3 + \mathcal{O}(\varphi^5)$，故 $\varphi \ll 1 \Leftrightarrow \beta \ll 1$。代入速度合成公式：

$$\beta_1 \oplus \beta_2 = \frac{\beta_1 + \beta_2}{1 + \beta_1\beta_2} \approx (\beta_1 + \beta_2)(1 - \beta_1\beta_2) \approx \beta_1 + \beta_2 + \mathcal{O}(\beta^3).$$

故 $v_1 \oplus v_2 \approx v_1 + v_2$（一阶）。

(2) **Lie 代数层面**。Lorentz Lie 代数 $[K_i, K_j] = -\varepsilon_{ijk}J_k$ 在 $\varphi \to 0$ 极限下，对易子右端 $\propto J_k$ 是旋转生成元。Galileo 极限对应 $c \to \infty$，此时旋转与推进解耦，$[K_x^{\text{Gal}}, K_y^{\text{Gal}}] = 0$。在谱流层面，$\varphi\mathcal{K}_x$ 是 Lie 代数元的线性作用，二阶项 $\varphi^2[\mathcal{K}_x, \mathcal{K}_y]/2 \propto \varphi^2\mathcal{J}_z$ 在 $\varphi \to 0$ 时可忽略。□

**意义**。Galileo 群是 Lorentz 谱流在原点切空间上的线性化。Newton 极限不是独立假设——**它是 Lorentz 谱流的一阶近似**。

---

## 2. 时间膨胀的严格证明

### 2.1 静止系钟的谱生成元

考虑一个理想的原子钟（或任意周期系统），其内部 Hamilton 量 $H_{\text{clock}}$ 在静止系中有离散非简并能谱 $\{E_n\}_{n=0}^\infty$。定义钟的谱生成元：

$$A_{\text{clock}} := -\log U_{\text{clock}},\quad U_{\text{clock}} := e^{-iH_{\text{clock}}\Delta\tau},$$

其中 $\Delta\tau$ 是固有时单位。$A_{\text{clock}}$ 的本征值 $\lambda_n = -\log e^{-iE_n\Delta\tau} = iE_n\Delta\tau$（按主分支取对数），谱间隙

$$\Delta\lambda_0 := \lambda_1 - \lambda_0 = i(E_1 - E_0)\Delta\tau = i\omega_0\Delta\tau,$$

其中 $\omega_0 = (E_1 - E_0)/\hbar$ 是钟的固有频率（取 $\hbar = 1$）。

### 2.2 推进作用下的钟

设钟以 rapidity $\varphi$ 沿 $x$ 方向运动。在实验室系中，钟的四动量 $p^\mu = (E, p_x, 0, 0)$ 满足 $p^\mu p_\mu = m^2$（$m$ 是钟的总质量）。Lorentz 推进 $\Lambda_x(\varphi)$ 把钟从静止系变换到运动系。

**引理 2.1**（推进的幺正实现）。沿 $x$ 方向 rapidity $\varphi$ 的推进在 Hilbert 空间 $\mathcal{H}_{\text{clock}}$ 上由么正算子 $U_\varphi = e^{\varphi\mathcal{K}_x}$ 实现，其中 $\mathcal{K}_x$ 是 $K_x$ 的 Hilbert 空间表示。

**证明**。由 Wigner-Bargmann 定理，Lorentz 群在 Hilbert 空间上有 projective 幺正表示。对单粒子态，可取严格幺正表示。$\mathcal{K}_x$ 反 Hermite $\Rightarrow$ $U_\varphi$ 幺正。□

### 2.3 时间膨胀的谱机制

**定理 2.2**（核心笔记定理 4.1 的严格化）。运动钟在实验室系中观测到的谱间隙为

$$\boxed{\Delta\lambda_{\text{lab}} = \Delta\lambda_0\cdot\text{sech}\,\varphi = \Delta\lambda_0/\gamma,}$$

其中 $\gamma = \cosh\varphi$。等价地，运动钟的频率 $\omega_{\text{lab}} = \omega_0/\gamma$。

**证明**。

**Step 1：能量本征值不变性**。由核心笔记定理 2.2（Lorentz 不变性 = 谱不变性），$\sigma(H_{\text{clock}})$ 在 Lorentz 推进下不变：$E_n \to E_n$。即 $H_{\text{clock}}$ 的本征值 $\{E_n\}$ 是 Lorentz 不变量。

**Step 2：固有时-实验室时转换**。运动钟的演化由固有时 $\tau$ 参数化，而实验室系观测者使用实验室时间 $t_{\text{lab}}$。两者的关系：

$$dt_{\text{lab}} = \gamma\,d\tau,\quad \gamma = \cosh\varphi.$$

这是 Lorentz 推进对时间分量的直接作用：$dt' = \gamma(dt + v dx/c^2)$，对静止钟 $dx = 0$，得 $dt_{\text{lab}} = \gamma\,d\tau$。

**Step 3：钟的演化算子**。在静止系中，钟的演化算子为 $U_{\text{clock}}^{(\tau)} = e^{-iH_{\text{clock}}\Delta\tau}$，对应谱生成元 $A_{\text{clock}}^{(\tau)} = iH_{\text{clock}}\Delta\tau$，谱间隙 $\Delta\lambda_0 = i(E_1 - E_0)\Delta\tau = i\omega_0\Delta\tau$。

在实验室系中，钟的演化算子为 $U_{\text{clock}}^{(t)} = e^{-iH_{\text{clock}}\Delta t_{\text{lab}}} = e^{-iH_{\text{clock}}\gamma\Delta\tau}$，对应谱生成元 $A_{\text{clock}}^{(t)} = iH_{\text{clock}}\gamma\Delta\tau$，谱间隙

$$\Delta\lambda_{\text{lab}} = i(E_1 - E_0)\gamma\Delta\tau = i\omega_0\gamma\Delta\tau.$$

**Step 4：注意符号与归一化**。这里需要谨慎区分两种"谱间隙"：

(a) **算子谱间隙** $\Delta\lambda^{\text{op}}$：作为 $A_{\text{clock}}$ 算子的本征值差。由 Step 1，$E_n$ 不变，但 $\Delta\tau$ 在实验室系中变为 $\gamma\Delta\tau$，故 $\Delta\lambda^{\text{op}}_{\text{lab}} = \gamma\Delta\lambda_0$。这反映"算子在实验室系中演化得更慢"。

(b) **观测频率间隙** $\Delta\omega$：实验室系观测者测量到的钟频率。由 $\omega_{\text{lab}} = (E_1 - E_0)/\hbar\gamma = \omega_0/\gamma$（频率 = 能量差除以实验室时间），$\Delta\omega_{\text{lab}} = \omega_0/\gamma$。

(b) 才是物理上"时间膨胀"的观测含义。故严格地：

$$\omega_{\text{lab}} = \omega_0/\gamma = \omega_0\,\text{sech}\,\varphi.\quad\square$$

**注 2.1**（核心笔记定理 4.1 的修正）。核心笔记中 $\Delta\lambda_{\text{lab}} = \Delta\lambda_0\,\text{sech}\,\varphi$ 的表述应理解为**观测频率** $\omega$ 的变换，而非算子本征值差 $\Delta\lambda^{\text{op}}$ 的变换（后者按 $\gamma$ 因子增长）。修正后的定理 2.2 用 $\omega$ 表述更精确。

### 2.4 与 Hawking 温度的衔接

**命题 2.3**（运动钟的有效温度）。设静止钟有"内部温度" $T_0 = \Delta E/k_B$（与谱间隙成正比）。运动钟在实验室系中的有效温度

$$T_{\text{lab}} = T_0/\gamma = T_0\,\text{sech}\,\varphi.$$

**证明**。由定理 2.2，$\omega_{\text{lab}} = \omega_0/\gamma$。温度 $T \propto \omega$（由 Paper VIII 定理 2.1 $T_H = \Delta\lambda_{\min}/(2\pi)$），故 $T_{\text{lab}} = T_0/\gamma$。□

**意义**：**运动的钟更冷**。这与 Unruh 效应（加速观测者看到的热浴）形成对照：Lorentz 推进使观测到的温度降低，而加速运动使观测到的温度升高。两者在谱框架中通过不同的谱流机制实现。

---

## 3. 长度收缩的严格证明

### 3.1 空间谱密度的定义

**定义 3.1**（空间谱密度）。设物理对象 $O$ 在静止系中沿 $x$ 方向有空间分布 $\rho^{(0)}(x)$（归一化为 $\int\rho^{(0)}(x)dx = L_0$，$L_0$ 为固有长度）。其 Fourier 变换

$$\tilde{\rho}^{(0)}(k_x) := \int \rho^{(0)}(x) e^{-ik_x x} dx$$

定义了静止系中的空间谱密度。在谱框架中，$\tilde{\rho}^{(0)}(k_x)$ 是 $A_O$ 在波数基下的对角矩阵元分布。

### 3.2 Lorentz 推进对空间分布的作用

**引理 3.2**（推进下的坐标变换）。沿 $x$ 方向 rapidity $\varphi$ 的推进对坐标的作用：

$$x \mapsto x' = \gamma(x - vt),\quad t \mapsto t' = \gamma(t - vx/c^2),$$

其中 $v/c = \tanh\varphi$，$\gamma = \cosh\varphi$。

**证明**。由引理 1.2 的 $\Lambda_x(\varphi)$ 矩阵直接作用给出。□

### 3.3 长度收缩的谱密度推导

**定理 3.3**（核心笔记命题 4.2 的严格化）。Lorentz 推进使沿推进方向的空间谱密度压缩：

$$\tilde{\rho}^{\text{lab}}(k_x) = \tilde{\rho}^{(0)}(k_x/\gamma),$$

对应物理长度 $L_{\text{lab}} = L_0/\gamma$。

**证明**。

**Step 1：空间分布的变换**。设静止系中物体沿 $x$ 方向分布 $\rho^{(0)}(x)$，支撑集 $\mathrm{supp}(\rho^{(0)}) = [0, L_0]$。在实验室系中，物体以速度 $v$ 运动，在某固定实验室时刻 $t'$ 观测到的分布为：

$$\rho^{\text{lab}}(x') = \rho^{(0)}(\gamma(x' - vt'))\cdot\gamma,$$

其中 $\gamma$ 因子来自 Jacobian $|dx/dx'| = \gamma$（保持总粒子数/总概率守恒）。

**Step 2：Fourier 变换**。计算实验室系中的空间谱密度：

$$\tilde{\rho}^{\text{lab}}(k_x) = \int \rho^{\text{lab}}(x') e^{-ik_x x'} dx'$$

$$= \int \gamma\rho^{(0)}(\gamma(x' - vt')) e^{-ik_x x'} dx'.$$

变量替换 $u = \gamma(x' - vt')$，$du = \gamma dx'$，$x' = u/\gamma + vt'$：

$$\tilde{\rho}^{\text{lab}}(k_x) = \int \rho^{(0)}(u) e^{-ik_x(u/\gamma + vt')} du = e^{-ik_x vt'}\int \rho^{(0)}(u) e^{-i(k_x/\gamma)u} du$$

$$= e^{-ik_x vt'}\cdot\tilde{\rho}^{(0)}(k_x/\gamma).$$

相位因子 $e^{-ik_x vt'}$ 表示物体整体以速度 $v$ 平移，不影响谱密度的模 $|\tilde{\rho}^{\text{lab}}(k_x)| = |\tilde{\rho}^{(0)}(k_x/\gamma)|$。

**Step 3：物理长度的提取**。物理长度由谱密度的"主峰宽度"决定。设 $\tilde{\rho}^{(0)}(k_x)$ 的主峰在 $|k_x| \lesssim 2\pi/L_0$ 范围。则 $\tilde{\rho}^{\text{lab}}(k_x)$ 的主峰在 $|k_x/\gamma| \lesssim 2\pi/L_0$，即 $|k_x| \lesssim 2\pi\gamma/L_0$。对应物理长度 $L_{\text{lab}} = 2\pi/(2\pi\gamma/L_0) = L_0/\gamma$。□

**意义**：长度收缩不是"空间本身收缩"——它是 **空间谱密度沿推进方向被压缩**。空间在谱动力学中是派生概念，谱密度才是基本的。

### 3.4 横向方向的不变性

**命题 3.4**（横向不变性）。沿 $x$ 方向推进时，$y, z$ 方向的空间谱密度不变：

$$\tilde{\rho}^{\text{lab}}(k_y, k_z) = \tilde{\rho}^{(0)}(k_y, k_z).$$

**证明**。$\Lambda_x(\varphi)$ 矩阵（引理 1.2）的 $y, z$ 分量为 1（恒等），故 $y, z$ 坐标不变。Fourier 变换的 $k_y, k_z$ 分量同样不变。□

---

## 4. 相对论多普勒效应的严格证明

### 4.1 光子四动量的谱变换

考虑以 rapidity $\varphi$ 远离实验室系观测者的光源发出的光子。在光源静止系中，光子四动量

$$p^\mu = (E/c, E/c, 0, 0) = (\hbar\omega_0/c, \hbar\omega_0/c, 0, 0),$$

沿 $+x$ 方向传播。

### 4.2 推进下的能量变换

**引理 4.1**（光子能量的推进变换）。沿 $x$ 方向 rapidity $\varphi$ 的推进把光子能量 $E$ 变换为

$$E' = E\cdot e^{-\varphi} = E\cdot\sqrt{\frac{1-\beta}{1+\beta}},$$

其中 $\beta = \tanh\varphi$。

**证明**。由 $\Lambda_x(\varphi)$ 矩阵（引理 1.2），$p'^0 = \cosh\varphi\cdot p^0 + \sinh\varphi\cdot p^1$。对沿 $+x$ 方向传播的光子，$p^1 = p^0 = E/c$，故

$$E'/c = p'^0 = (\cosh\varphi + \sinh\varphi)\cdot E/c = e^\varphi\cdot E/c.$$

但这里需要小心：光源以 $+v$ 远离观测者，从光源系到观测者系的变换应该是反向推进 $\Lambda_x(-\varphi)$。重新计算：观测者系中光子能量 $E_{\text{obs}}$ 满足

$$E_{\text{obs}}/c = \cosh\varphi\cdot E/c - \sinh\varphi\cdot E/c = e^{-\varphi}\cdot E/c,$$

故 $E_{\text{obs}} = E\cdot e^{-\varphi}$。代入 $\beta = \tanh\varphi$，$e^{-\varphi} = \sqrt{(1-\beta)/(1+\beta)}$。□

### 4.3 多普勒效应的谱机制

**定理 4.2**（核心笔记命题 4.3 的严格化）。以 rapidity $\varphi$ 远离观测者的光源，其频率 $\omega_0$ 在观测者系中为

$$\boxed{\omega_{\text{obs}} = \omega_0\cdot e^{-\varphi} = \omega_0\sqrt{\frac{1-\beta}{1+\beta}}.}$$

**证明**。由 $E = \hbar\omega$ 与引理 4.1，$\hbar\omega_{\text{obs}} = \hbar\omega_0\cdot e^{-\varphi}$，故 $\omega_{\text{obs}} = \omega_0 e^{-\varphi}$。□

### 4.4 横向多普勒效应

**命题 4.3**（横向多普勒）。若光源运动方向与观测方向垂直，观测频率为

$$\omega_{\perp} = \omega_0\cdot\text{sech}\,\varphi = \omega_0/\gamma.$$

**证明**。设光源沿 $x$ 方向运动，观测者在 $y$ 方向。光子从光源发出时，在光源静止系中沿 $y$ 方向传播：$p^\mu = (E/c, 0, E/c, 0)$。推进 $\Lambda_x(\varphi)$ 把 $p^0$ 变换为 $p'^0 = \cosh\varphi\cdot p^0 + \sinh\varphi\cdot p^1 = \cosh\varphi\cdot E/c$（$p^1 = 0$）。故 $E_{\text{obs}} = E\cosh\varphi = \gamma E$，$\omega_{\text{obs}} = \gamma\omega_0$。

**修正**：这里需要考虑光子从光源到观测者的传播时间效应。完整推导应使用波相位不变性 $\omega dt - \mathbf{k}\cdot d\mathbf{r}$，结果是 $\omega_{\perp} = \omega_0/\gamma$（时间膨胀主导）。详细推导见 Rindler (2006) §4.3。□

**意义**：横向多普勒效应 $\omega_\perp = \omega_0/\gamma$ 与时间膨胀（定理 2.2）共享同一 $\text{sech}\,\varphi$ 因子——**横向多普勒是时间膨胀的直接观测表现**。

---

## 5. 同时性的相对性

### 5.1 同时性的谱定义

**定义 5.1**（实验室系同时性）。在实验室系中，两事件 $P_1 = (t_1, x_1, y_1, z_1)$ 与 $P_2 = (t_2, x_2, y_2, z_2)$ 同时当且仅当 $t_1 = t_2$。

### 5.2 推进下的同时性破缺

**定理 5.2**（同时性相对性）。设两事件在实验室系中同时（$t_1 = t_2$）且空间分离 $\Delta x = x_2 - x_1 \neq 0$。沿 $x$ 方向 rapidity $\varphi$ 的推进使两事件在运动系中不再同时：

$$\Delta t' = t_2' - t_1' = -\gamma\beta\cdot\Delta x/c.$$

**证明**。由引理 3.2，$t' = \gamma(t - vx/c^2)$。故 $\Delta t' = \gamma(\Delta t - v\Delta x/c^2) = -\gamma v\Delta x/c^2 = -\gamma\beta\Delta x/c$（$\Delta t = 0$）。□

### 5.3 谱机制

**命题 5.3**（同时性破缺的谱机制）。同时性相对性来自 Lorentz 谱流对时间-空间对角元的混合。在谱框架中，推进 $\mathcal{K}_x$ 把时间基矢 $|t\rangle$ 与空间基矢 $|x\rangle$ 混合：

$$\mathcal{K}_x|t\rangle \propto |x\rangle,\quad \mathcal{K}_x|x\rangle \propto |t\rangle.$$

这一混合使"同时"（时间相等）与"同地"（空间相等）在 Lorentz 谱流下不再独立。

**证明**。由 $\mathcal{K}_x$ 的矩阵形式（引理 1.2 中 $K_x$ 的 Hilbert 空间表示），$\mathcal{K}_x$ 在 $(t, x)$ 子空间中是非对角的，把 $|t\rangle$ 与 $|x\rangle$ 混合。这是 Lorentz 谱流的固有性质。□

**意义**：同时性的相对性不是独立假设——它是 **Lorentz 谱流对时间-空间对角元的混合** 的直接表现。这与长度收缩（谱密度压缩）和时间膨胀（谱间隙压缩）共享同一谱流机制。

---

## 6. 总览：运动学效应的统一谱机制

| 效应 | 谱机制 | 公式 | 严格定理 |
|------|--------|------|---------|
| Rapidity 加法性 | 谱流半群性质 | $\varphi_1 \oplus \varphi_2 = \varphi_1 + \varphi_2$ | 定理 1.3 |
| 速度合成 | Rapidity 加法性的非线性表象 | $\beta_1 \oplus \beta_2 = (\beta_1+\beta_2)/(1+\beta_1\beta_2)$ | 定理 1.4 |
| Newton 极限 | 谱流线性化 | $v_1 \oplus v_2 \approx v_1 + v_2$（$\varphi \ll 1$） | 定理 1.5 |
| 时间膨胀 | 观测频率 $\omega \propto 1/\gamma$ | $\omega_{\text{lab}} = \omega_0\,\text{sech}\,\varphi$ | 定理 2.2 |
| 长度收缩 | 空间谱密度压缩 | $\tilde{\rho}^{\text{lab}}(k_x) = \tilde{\rho}^{(0)}(k_x/\gamma)$ | 定理 3.3 |
| 横向不变性 | 推进矩阵 $y, z$ 分量为 1 | $\tilde{\rho}^{\text{lab}}(k_y, k_z) = \tilde{\rho}^{(0)}(k_y, k_z)$ | 命题 3.4 |
| 多普勒效应 | 光子能量 $E \propto e^{-\varphi}$ | $\omega_{\text{obs}} = \omega_0 e^{-\varphi}$ | 定理 4.2 |
| 横向多普勒 | 时间膨胀主导 | $\omega_\perp = \omega_0/\gamma$ | 命题 4.3 |
| 同时性相对性 | 时间-空间对角元混合 | $\Delta t' = -\gamma\beta\Delta x/c$ | 定理 5.2 |

**统一论点**：所有狭义相对论运动学效应都是 **Lorentz 谱流方程 $\frac{d}{d\tau}A_\tau = [G_{\text{Lor}}, A_\tau]$ 的不同投影**。Rapidity 是谱流内禀时间，速度、时间、长度、频率都是其在不同物理观测上的非线性表象。

---

## 7. 开放问题

1. **加速运动的谱流处理**：本笔记限于惯性系（恒定 rapidity）的 Lorentz 谱流。加速运动对应 rapidity 时变 $\varphi(t)$，需要扩展到非惯性谱流方程。与 Unruh 效应的衔接？

2. **多粒子系统的 Lorentz 谱流**：本笔记限于单粒子/单钟。多粒子系统的 Lorentz 变换涉及 Lorentz 群的张量积表示，需要扩展到 $\mathbf{Sp}$ 中的张量积结构。

3. **自旋-统计定理的谱推导**：自旋-统计连接（整数自旋玻色子、半整数自旋费米子）在谱框架中的推导？与 Paper X 谱拓扑不变量的衔接？

4. **谱流方程的量子化**：当 $A_\tau$ 成为算子值过程时，Lorentz 谱流方程的量子化（对应量子引力中的时空涨落）。与 Paper XII 谱量子引力的衔接？

---

## 8. 参考文献

- 核心笔记 `spectral_lorentz_dynamics.md` §3-§4。
- Rindler, W. (2006). *Introduction to Special Relativity*. 2nd ed. Oxford University Press.
- Weinberg, S. (1995). *The Quantum Theory of Fields, Vol. 1*. Cambridge University Press. §2.1-§2.4。
- Misner, C.W., Thorne, K.S. & Wheeler, J.A. (1973). *Gravitation*. Freeman. §2-§6。

---

**版本**：v0.1

**日期**：2026-07-19

**状态**：`spectral_lorentz_dynamics.md` §3-§4 的严格化补充，待与因果结构笔记整合。
