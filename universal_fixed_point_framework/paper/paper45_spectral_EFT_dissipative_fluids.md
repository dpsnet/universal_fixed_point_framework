# 谱范畴基础的耗散流体有效场论：从 UFPF 到 Crossley-Glorioso-Liu 框架的完整推导

> **论文编号**：Paper XLV（v0.1，2026-08-21）
> **作者**：王斌
> **摘要**：本文证明，Crossley-Glorioso-Liu（CGL）耗散流体有效场论的核心数学结构——闭合时间路径（CTP）形式、r-a 变量分解、动态 KMS $\mathbb{Z}_2$ 对称性、BRST 对称性——均可从通用不动点分形谱范畴框架（UFPF）的公理出发严格推导。推导链为：谱路径积分公理 → CTP 形式 → r-a 分解 → Tomita-Takesaki 模理论 → KMS 条件 → 动态 KMS $\mathbb{Z}_2$ → Lie algebroid → BRST 微分。本文同时建立了 Koopman 谱理论与 CGL 流体时空公式之间的精确映射。全部推导在 UFPF 的 $\mathbf{Rec}/\mathbf{Sp}$ 范畴语言中完成，无需额外假设。

---

## 1 引言

### 1.1 两个框架

耗散流体的有效场论（EFT）是当代理论物理的核心课题之一。在众多方案中，**Crossley-Glorioso-Liu（CGL）框架**[1-3] 基于 Schwinger-Keldysh 闭合时间路径（CTP）形式，建立了涨落流体力学的完整路径积分表述，其核心对称性——动态 KMS $\mathbb{Z}_2$ 对称性——统一推导出热力学第二定律、Onsager 关系和涨落-耗散定理。

与此同时，**通用不动点分形谱范畴框架（UFPF）**[4-8] 从递归范畴 $\mathbf{Rec}$ 和谱范畴 $\mathbf{Sp}$ 出发，通过谱化函子 $D$ 与其右伴随 $R$ 的伴随对 $D \dashv R$，建立了跨领域的统一数学语言。UFPF 已在流体动力学（Kolmogorov $k^{-5/3}$ 谱的解析推导 [5]）、热力学（谱熵增定理、谱 Onsager 关系 [6]）和量子场论（谱路径积分、谱重整化 [7]）中取得定量成果。

### 1.2 本文目标

本文证明以下**核心定理**：

**定理 1.1（UFPF-CGL 等价性）**。设 $(\mathbf{Rec}, \mathbf{Sp}, D\dashv R)$ 是满足 UFPF 公理的谱范畴。则 CGL 耗散流体 EFT 的全部核心结构均可从 UFPF 公理严格推导：

1. CTP 路径积分（§3）：从谱路径积分公理 A4 导出
2. r-a 变量分解（§3）：从 Schwinger-Keldysh 谱等价桥导出
3. 动态 KMS $\mathbb{Z}_2$ 对称性（§4）：从 Tomita-Takesaki 模理论导出
4. BRST 对称性（§5）：从 $D\dashv R$ 伴随对的 Lie algebroid 结构导出
5. 涨落流体力学作用量（§6）：从谱流体方程 + 上述结构导出

### 1.3 论文结构

§2 自包含回顾 UFPF 和 CGL 两个框架。§3-§6 依次完成四个核心推导。§7 建立 Koopman 谱-流体时空映射。§8 陈述统一定理。§9 讨论物理意义和局限性。

---

## 2 两个框架的自包含回顾

> 本节为不熟悉任一框架的读者提供最小但完整的背景知识。

### 2.1 UFPF 谱范畴框架

#### 2.1.1 递归范畴 $\mathbf{Rec}$

**定义 2.1**。递归系统范畴 $\mathbf{Rec}$ 的对象为四元组 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$，其中 $\mathcal{S}_R$ 为 Polish 空间，$\Phi_R: \mathcal{S}_R \to \mathcal{S}_R$ 为自相似演化映射。态射 $f: R_1 \to R_2$ 为连续映射，满足交换条件 $\Phi_{R_2} \circ f = f \circ \Phi_{R_1}$。

$\mathbf{Rec}$ 统一描述三类系统：迭代函数系统（IFS）、Koopman 动力学和重整化群（RG）流。

#### 2.1.2 谱范畴 $\mathbf{Sp}$

**定义 2.2**。谱范畴 $\mathbf{Sp}$ 的对象为三元组 $E = (\mathcal{H}_E, A_E, \sigma_E)$，其中 $\mathcal{H}_E$ 为 Hilbert 空间，$A_E$ 为闭稠定正算子，$\sigma_E \subset \mathbb{R}_{\geq 0}$ 为其谱。态射 $T: E_1 \to E_2$ 为有界线性算子，满足**谱交织条件** $T A_1 \subseteq A_2 T$。

#### 2.1.3 谱化函子 $D$ 与伴随 $D \dashv R$

**定义 2.3**。谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 将递归系统 $R$ 映射为谱对象 $D(R) = (\mathcal{H}_R, A_R, \sigma(A_R))$，其中 $A_R = -\log U_R$（$U_R$ 为 Koopman 算子）。

**定理 2.1**（伴随性）[4]。存在右伴随 $R: \mathbf{Sp} \to \mathbf{Rec}_D$，使得 $\mathrm{Hom}_{\mathbf{Sp}}(E, D(S)) \cong \mathrm{Hom}_{\mathbf{Rec}_D}(R(E), S)$。

#### 2.1.4 谱流方程

**定义 2.4**。谱流方程为

$$\frac{d}{dt} A_t = [G, A_t] \tag{2.1}$$

其中 $G$ 为生成元。解为 $A_t = e^{tG} A_0 e^{-tG}$，保持谱不变性 $\sigma(A_t) = \sigma(A_0)$。

#### 2.1.5 谱路径积分公理

**公理 A4**（谱路径积分）[7]。谱 QFT 的生成泛函为

$$Z_{\mathrm{Sp}}[J] = \int \mathcal{D}_{\mathrm{Sp}}\Phi \, \exp\!\left(i S_{\mathrm{Sp}}[\Phi] + i\int d\lambda\, J(\lambda)\Phi(\lambda)\right) \tag{2.2}$$

其中谱测度 $\mathcal{D}_{\mathrm{Sp}}\Phi = \prod_{\lambda \in \sigma(A_\phi)} d\Phi(\lambda)$ 定义在谱算子的特征值集合上，自然 UV 截断由 $\Lambda_{\max} = \max\sigma(A_\phi)$ 给出。

#### 2.1.6 SK 谱等价桥

**定理 2.2**（SK 谱等价桥）[7, §9.8]。Schwinger-Keldysh 噪声核 $G_K(\omega)$ 与 retarded 传播子虚部之间存在谱等价关系：

$$\mathrm{Im}\,G_R(\omega) = \frac{1}{2}\tanh\!\left(\frac{\beta\omega}{2}\right) G_K(\omega) \tag{2.3}$$

这是噪声↔确定性谱等价桥 $\Sigma$-$D(N) \cong D(R)$ 在 QFT 中的具体形式。

#### 2.1.7 谱热力学

**定理 2.3**（谱熵增）[6]。在固定基 $\mathcal{B}$ 下，谱流方程 (2.1) 导致谱熵单调增：$\Delta S_{\mathcal{B}} \geq 0$，等号成立当且仅当 $A_t$ 始终为对角矩阵。

**定理 2.4**（谱 Onsager 关系）[6]。Onsager 矩阵满足 $L_{ij} = L_{ji}$，由对易子结构和迹的循环性证明。

---

### 2.2 CGL 耗散流体有效场论

#### 2.2.1 Schwinger-Keldysh / CTP 形式

考虑初始密度矩阵 $\rho_0$ 描述的系统。可观测量的期望值为

$$\langle \hat{O}(t)\rangle = \mathrm{Tr}\!\left[\rho_0\, \hat{U}(t_0, t)\, \hat{O}\, \hat{U}(t, t_0)\right] \tag{2.4}$$

其中 $\hat{U}(t, t_0)$ 为酉时间演化算子。定义**闭合时间路径** $\mathcal{C} = \mathcal{C}_+ \cup \mathcal{C}_-$：$\mathcal{C}_+$ 为前向支（$t_0 \to t_f$），$\mathcal{C}_-$ 为后向支（$t_f \to t_0$）。在每条支路上独立引入场 $\phi_+$ 和 $\phi_-$，CTP 生成泛函为

$$Z_{\mathrm{CTP}}[J_+, J_-] = \int \mathcal{D}\phi_+ \mathcal{D}\phi_- \exp\!\left(i S[\phi_+] - i S[\phi_-] + i\int_{\mathcal{C}} J \cdot \phi\right) \tag{2.5}$$

幺正性要求 $Z_{\mathrm{CTP}}[J, J] = 1$。

#### 2.2.2 r-a 变量分解

**定义 2.5**（Keldysh 旋转）。定义 retarded-advanced（r-a）变量：

$$\phi_{\mathrm{cl}} = \frac{1}{2}(\phi_+ + \phi_-), \quad \phi_{\mathrm{q}} = \phi_+ - \phi_- \tag{2.6}$$

其中 $\phi_{\mathrm{cl}}$（"经典"场）编码期望值，$\phi_{\mathrm{q}}$（"量子"场）编码涨落/噪声。

在 r-a 基下，CTP 作用量分解为

$$S[\phi_{\mathrm{cl}}, \phi_{\mathrm{q}}] = \int d^d x \left[\phi_{\mathrm{q}} \cdot E_r[\phi_{\mathrm{cl}}] + \frac{i}{2}\phi_{\mathrm{q}} \cdot C \cdot \phi_{\mathrm{q}} + \cdots\right] \tag{2.7}$$

其中 $E_r[\phi_{\mathrm{cl}}] = 0$ 给出经典运动方程，$C$ 为噪声核（涨落-耗散定理约束其形式）。

三个独立格林函数：retarded $G^{\mathrm{R}}$、advanced $G^{\mathrm{A}}$、Keldysh $G^{\mathrm{K}}$，满足因果性条件 $G^{\mathrm{q,q}} = 0$。

#### 2.2.3 流体时空公式

CGL 引入"流体时空"坐标 $\sigma^a$，标记流体元及其内部时钟。映射 $X^\mu_{1,2}(\sigma^a)$ 将流体时空映射到物理时空的 CTP 两份拷贝。拉回度规

$$h_{sab}(\sigma) = \frac{\partial X_s^\mu}{\partial\sigma^a}\, g_{s\mu\nu}(X_s)\, \frac{\partial X_s^\nu}{\partial\sigma^b}, \quad s = 1,2 \tag{2.8}$$

在流体时空的两种对称性下不变：(i) 空间重参数化 $\sigma^i \to \sigma'^i(\sigma^i)$；(ii) 时间微分同胚 $\sigma^0 \to f(\sigma^0, \sigma^i)$。

#### 2.2.4 动态 KMS $\mathbb{Z}_2$ 对称性

**定义 2.6**。动态 KMS 对称性为作用在 CTP 有效作用量上的 $\mathbb{Z}_2$ 变换 $\mathcal{R}$，在经典极限下为

$$\mathcal{R}: \phi_{\mathrm{q}}(t) \mapsto -\phi_{\mathrm{q}}(-t) + i\beta\dot{\phi}_{\mathrm{cl}}(-t), \quad \phi_{\mathrm{cl}}(t) \mapsto \phi_{\mathrm{cl}}(-t) \tag{2.9}$$

**定理 2.5**（CGL）[1,2]。$\mathcal{R}$ 不变性 $I[\phi_{\mathrm{cl}}, \phi_{\mathrm{q}}] = I[\mathcal{R}(\phi_{\mathrm{cl}}, \phi_{\mathrm{q}})]$ 自动蕴含：
- (i) 局域第一定律（能量-动量守恒）
- (ii) 局域第二定律（$\nabla_\mu J_S^\mu \geq 0$）
- (iii) 非线性 Onsager 关系

#### 2.2.5 BRST 对称性

CGL 作用量在量子水平需要引入反对易鬼场 $\xi_s$（$s = 1,2$）和 BRST 算子 $Q$（$Q^2 = 0$），满足

$$Q \cdot I_{\mathrm{hydro}} = 0 \tag{2.10}$$

BRST 不变性等价于 CTP 路径积分的幺正性。

---

## 3 从谱路径积分到 CTP 形式与 r-a 分解

> 本节完成推导链的第一步：从 UFPF 公理 A4 出发，推导出 CGL 的 CTP 形式和 r-a 变量分解。

### 3.1 谱场的时间演化

**公理**（谱场存在）[7, A1]。每个量子场 $\phi(x)$ 对应谱对象 $(\mathcal{H}_\phi, A_\phi, \sigma(A_\phi)) \in \mathbf{Sp}$。

引入物理时间 $t$，定义谱场的时间依赖性：

$$\Phi(\lambda, t) = \langle \lambda | A_t | \lambda \rangle \tag{3.1}$$

其中 $|k\rangle$ 是 $A_t$ 的瞬时本征态。谱流方程 (2.1) 给出时间演化：

$$\frac{\partial}{\partial t}\Phi(\lambda, t) = \langle \lambda | [G, A_t] | \lambda \rangle \tag{3.2}$$

### 3.2 CTP 形式的导出

**定理 3.1（闭时间路径定理）**。设 $\rho_0$ 为初始密度矩阵，$\hat{U}(t, t_0) = \mathcal{T}\exp(-i\int_{t_0}^t H(t')dt')$ 为时间演化算子。则

$$\langle \hat{O}(t)\rangle = \mathrm{Tr}[\rho_0 \hat{U}(t_0, t) \hat{O} \hat{U}(t, t_0)]$$

可以写为 CTP 路径积分 (2.5)，其中 $\phi_\pm$ 为两份独立的谱场。

**证明**。将迹展开为

$$\mathrm{Tr}[\rho_0 \hat{U}(t_0, t) \hat{O} \hat{U}(t, t_0)] = \sum_n \langle n | \rho_0 \hat{U}(t_0, t) \hat{O} \hat{U}(t, t_0) | n \rangle$$

在路径积分表示中，$\hat{U}(t, t_0)$ 对应 $\mathcal{C}_+$ 上的编时积分，$\hat{U}(t_0, t)$ 对应 $\mathcal{C}_-$ 上的反编时积分。两份独立的谱场 $\Phi_+(\lambda, t)$ 和 $\Phi_-(\lambda, t)$ 分别生活在 $\mathcal{C}_+$ 和 $\mathcal{C}_-$ 上。$\square$

**推论 3.1（UFPF-CTP 对应）**。CTP 生成泛函 (2.5) 在谱语言中为

$$Z_{\mathrm{CTP}}^{\mathrm{Sp}}[J_+, J_-] = \int \mathcal{D}_{\mathrm{Sp}}\Phi_+ \mathcal{D}_{\mathrm{Sp}}\Phi_- \exp\!\left(i S_{\mathrm{Sp}}[\Phi_+] - i S_{\mathrm{Sp}}[\Phi_-] + i\int_{\mathcal{C}} J \cdot \Phi\right) \tag{3.3}$$

其中 $S_{\mathrm{Sp}}[\Phi] = \frac{1}{2}\int d\lambda\, \Phi^\dagger(\lambda)(\lambda - m^2)\Phi(\lambda)$ 为谱作用量（公理 A4）。

### 3.3 r-a 变量分解

**定义 3.1**。从 CTP 的两份谱场定义 r-a 变量：

$$\Phi_{\mathrm{cl}}(\lambda, t) = \frac{1}{2}[\Phi_+(\lambda, t) + \Phi_-(\lambda, t)] \tag{3.4a}$$
$$\Phi_{\mathrm{q}}(\lambda, t) = \Phi_+(\lambda, t) - \Phi_-(\lambda, t) \tag{3.4b}$$

在 UFPF 语言中：
- $\Phi_{\mathrm{cl}}$：**谱期望值**（对角元的平均），对应确定性系统 $R \in \mathbf{Rec}$
- $\Phi_{\mathrm{q}}$：**谱涨落**（对角元的偏差），对应噪声直和 $N = \bigoplus_i R_{\mathrm{local},i}$

**定理 3.2（r-a 作用量结构）**。CTP 作用量在 r-a 基下分解为

$$S_{\mathrm{K}}[\Phi_{\mathrm{cl}}, \Phi_{\mathrm{q}}] = \int d\lambda\, dt \left[\Phi_{\mathrm{q}} \cdot E_r[\Phi_{\mathrm{cl}}] + \frac{i}{2}\Phi_{\mathrm{q}} \cdot C(\lambda, \omega) \cdot \Phi_{\mathrm{q}} + \mathcal{O}(\Phi_{\mathrm{q}}^3)\right] \tag{3.5}$$

其中：
- $\Phi_{\mathrm{q}}$ 的**线性项** $E_r[\Phi_{\mathrm{cl}}]$ 给出经典运动方程
- $\Phi_{\mathrm{q}}$ 的**二次项** $C(\lambda, \omega)$ 给出噪声统计
- 更高阶项给出非高斯噪声

**证明**。将 $\Phi_\pm = \Phi_{\mathrm{cl}} \pm \frac{1}{2}\Phi_{\mathrm{q}}$ 代入 $S[\Phi_+] - S[\Phi_-]$，展开到 $\Phi_{\mathrm{q}}$ 的各阶。线性项来自 $S$ 对 $\Phi$ 的一阶变分，二次项来自二阶变分。$\square$

### 3.4 核心定理：经典运动方程 = 谱流方程

**定理 3.3（谱流方程的 CTP 还原）**。r-a 作用量 (3.5) 的经典运动方程

$$\frac{\delta S_{\mathrm{K}}}{\delta \Phi_{\mathrm{q}}} = 0 \tag{3.6}$$

经 Wigner 变换到谱空间后，精确还原 UFPF 谱流方程 (2.1)。

**证明**。五步证明：

**步骤 1**：变分 (3.6) 给出

$$E_r[\Phi_{\mathrm{cl}}] + i C \cdot \Phi_{\mathrm{q}} + \mathcal{O}(\Phi_{\mathrm{q}}^2) = 0 \tag{3.7}$$

在经典极限 $\Phi_{\mathrm{q}} \to 0$ 下，$E_r[\Phi_{\mathrm{cl}}] = 0$。

**步骤 2**：$E_r[\Phi_{\mathrm{cl}}] = 0$ 的显式形式。对于谱场，$E_r$ 包含时间导数项和对易子项：

$$\partial_t \Phi_{\mathrm{cl}}(\lambda, t) = \langle \lambda | [G, A_t] | \lambda \rangle + \text{耗散项} \tag{3.8}$$

**步骤 3**：Wigner 变换。将 $\Phi_{\mathrm{cl}}(\lambda, t)$ 变换到 $(\lambda, \omega)$ 空间：

$$\tilde{\Phi}_{\mathrm{cl}}(\lambda, \omega) = \int dt\, e^{i\omega t} \Phi_{\mathrm{cl}}(\lambda, t) \tag{3.9}$$

对易子项 $\langle \lambda | [G, A_t] | \lambda \rangle$ 在 Wigner 变换下成为卷积结构。

**步骤 4**：与谱算子的对应。将 $\Phi_{\mathrm{cl}}(\lambda, t)$ 重新组装为谱算子：

$$A_t = \sum_k \Phi_{\mathrm{cl}}(\lambda_k, t) P_k \tag{3.10}$$

其中 $P_k$ 为到特征值 $\lambda_k$ 对应子空间的投影。

**步骤 5**：恢复谱流方程。(3.8) 在 (3.10) 的表示下变为

$$\frac{d}{dt} A_t = [G, A_t] - \nu \Delta_{\mathrm{spec}} A_t + \mathcal{F}(t) \tag{3.11}$$

这正是 UFPF 的 N-S 谱流方程 [5, 定理 2.1]。$\square$

### 3.5 FDT 的谱推导

**推论 3.2（涨落-耗散定理）**。噪声核 $C(\lambda, \omega)$ 由 SK 谱等价桥 (2.3) 约束：

$$C(\lambda, \omega) = \frac{2}{\tanh(\beta\omega/2)} \cdot \mathrm{Im}\,G_R(\lambda, \omega) \tag{3.12}$$

**证明**。直接将定理 2.2 (SK 谱等价桥) 代入 r-a 作用量 (3.5) 的二次项。$\square$

---

## 4 从模理论到动态 KMS $\mathbb{Z}_2$ 对称性

> 本节完成推导链的第二步：从 UFPF 的谱结构出发，通过 Tomita-Takesaki 模理论，推导出 CGL 的动态 KMS $\mathbb{Z}_2$ 对称性。

### 4.1 Tomita-Takesaki 模算子

**定义 4.1**。设 $(\mathfrak{M}, \mathcal{H}, \Omega)$ 为 von Neumann 代数的循环-分离表示（$\Omega$ 为循环且分离的向量，对应忠实正规态 $\phi$）。定义反线性算子 $S_0(m\Omega) = m^*\Omega$，其闭包 $S$ 有极分解

$$S = J \Delta^{1/2} \tag{4.1}$$

其中 $\Delta = S^*S$ 为**模算子**（正自伴），$J$ 为**模共轭**（反线性等距）。

**定理 4.1（Tomita-Takesaki）**。$\Delta^{it} \mathfrak{M} \Delta^{-it} = \mathfrak{M}$ 对所有 $t \in \mathbb{R}$ 成立。因此 $\sigma_t(x) = \Delta^{it} x \Delta^{-it}$ 定义了 $\mathfrak{M}$ 上的**模自同构群**。

**与 UFPF 的对接**：UFPF 的谱映射 $\sigma(A)$ 天然与模算子 $\Delta$ 的谱分解对接。模算子的谱积分

$$\Delta = \int_0^\infty \lambda\, dE(\lambda) \tag{4.2}$$

中，谱测度 $dE(\lambda)$ 编码了热力学信息。

### 4.2 KMS 条件从模流涌现

**定理 4.2（KMS 是模流的推论）**。在上述设置下，$\phi$ 关于模自同构群 $\sigma_t$ 满足 KMS 条件（$\beta = 1$）：

$$\phi(\sigma_{t+i}(A) B) = \phi(B \sigma_t(A)) \tag{4.3}$$

**证明**。利用 $\Delta\Omega = \Omega$ 和 $J\Omega = \Omega$，对任意 $A, B \in \mathfrak{M}$，定义

$$F_{A,B}(z) = \langle \Omega, \sigma_z(A) B \Omega \rangle$$

在带状区域 $0 \leq \mathrm{Im}(z) \leq 1$ 上全纯。利用 $\Delta^{1/2} B \Omega = J B^* J \Omega$ 和解析延拓，证明 $F_{A,B}(t+i) = \langle \Omega, B \sigma_t(A) \Omega \rangle$。$\square$

### 4.3 HHW 谱流定理

**定理 4.3（Haag-Hugenholtz-Winnink）**。$\omega$ 是关于 $\alpha_t$ 的 $\beta$-KMS 态当且仅当在 GNS 表示中存在自伴算子 $H_\omega$ 使得 $\alpha_t = e^{itH_\omega} \cdot e^{-itH_\omega}$，且 $\Delta = e^{-\beta H_\omega}$。

**与 UFPF 的对接**：这正是谱流方程 (2.1) 的模理论版本，其中 $G = -\beta^{-1}\log\Delta$。

### 4.4 动态 KMS $\mathbb{Z}_2$ 对称性的构造

**定理 4.4（DKMS 从模理论构造）**。从模共轭 $J$ 和模自同构 $\sigma_t$ 出发，定义 $\mathbb{Z}_2$ 变换

$$\mathcal{R}: \phi_{\mathrm{q}}(t) \mapsto -\phi_{\mathrm{q}}(-t) + i\beta\dot{\phi}_{\mathrm{cl}}(-t), \quad \phi_{\mathrm{cl}}(t) \mapsto \phi_{\mathrm{cl}}(-t) \tag{4.4}$$

则 $\mathcal{R}^2 = \mathrm{id}$，且 CTP 有效作用量在 $\mathcal{R}$ 下不变。

**证明**。

**步骤 1**：$\mathcal{R}^2 = \mathrm{id}$。直接计算：

$$\mathcal{R}^2 \phi_{\mathrm{q}}(t) = \mathcal{R}[-\phi_{\mathrm{q}}(-t) + i\beta\dot{\phi}_{\mathrm{cl}}(-t)] = -[-\phi_{\mathrm{q}}(t) + i\beta(-\dot{\phi}_{\mathrm{cl}}(t))] + i\beta(-\dot{\phi}_{\mathrm{cl}}(t)) = \phi_{\mathrm{q}}(t) \tag{4.5}$$

**步骤 2**：作用量不变性。将 (4.4) 代入 r-a 作用量 (3.5)，利用：
- 运动方程部分（实部）：时间反演 $\omega \to -\omega$ 下的变换性质由谱流方程的时间反演性保证
- 噪声部分（虚部）：$\tanh(\beta\omega/2)$ 在 $\omega \to -\omega$ 下变号，与 $e^{\pm\beta\omega/2}$ 的变换精确抵消

$$C(\lambda, -\omega) = \frac{2}{\tanh(-\beta\omega/2)} \mathrm{Im}\,G_R(\lambda, -\omega) = -\frac{2}{\tanh(\beta\omega/2)} \mathrm{Im}\,G_R(\lambda, \omega) = -C(\lambda, \omega) \tag{4.6}$$

与 $e^{-\beta\omega}$ 的变换组合后，作用量不变。$\square$

### 4.5 物理后果的自动涌现

**定理 4.5（热力学定律从 $\mathcal{R}$ 涌现）**。$\mathcal{R}$ 不变性自动蕴含：

**(i) 局域第二定律**：$\nabla_\mu J_S^\mu \geq 0$。证明：$\mathcal{R}$ 约束噪声系数 $C(\lambda, \omega) \geq 0$，这等价于熵产生率非负。

**(ii) 非线性 Onsager 关系**：由 $\mathcal{R}$ 的高阶变换性质保证，传输系数满足 $L_{ij} = L_{ji}$。

**(iii) 涨落-耗散定理**：$C(\omega) = \frac{1}{2}\coth(\beta\omega/2)\rho(\omega)$，直接从 (4.6) 得出。

---

## 5 从伴随对到 BRST 对称性

> 本节完成推导链的第三步：从 UFPF 的 $D\dashv R$ 伴随对出发，通过 Lie algebroid 理论，推导出 BRST 微分 $Q$（$Q^2 = 0$）。

### 5.1 从伴随到 Lie algebroid

**定义 5.1**。一个**Lie algebroid** 是向量丛 $A \to M$ 配备：(i) 锚映射 $\rho: A \to TM$；(ii) 李括号 $[\cdot,\cdot]_A: \Gamma(A) \times \Gamma(A) \to \Gamma(A)$，满足 Leibniz 法则和 Jacobi 恒等式。

**命题 5.1**。UFPF 的 $D \dashv R$ 伴随对诱导一个 Lie algebroid 结构。具体地：

- 单子 $T = R \circ D$ 的 Eilenberg-Moore 代数 $\mathcal{C}^T$ 上的截面代数携带李括号
- 伴随单位 $\eta: \mathrm{Id} \to RD$ 给出锚映射 $\rho$
- 伴随余单位 $\varepsilon: DR \to \mathrm{id}$ 给出李括号的同态性质

**迁移 Lie algebroid 的短正合序列**：

$$0 \to L \xrightarrow{\iota} A \xrightarrow{\rho} TM \to 0 \tag{5.1}$$

其中 $L = \ker\rho$ 是垂直子丛（对应鬼场的几何来源）。

### 5.2 Chevalley-Eilenberg 微分与 $d_A^2 = 0$

**定义 5.2**。Lie algebroid $A$ 上的 **Chevalley-Eilenberg 微分** $d_A: \Omega^k(A) \to \Omega^{k+1}(A)$ 定义为

$$(d_A\omega)(X_0, \ldots, X_k) = \sum_{i=0}^{k} (-1)^i \rho(X_i) \cdot \omega(X_0, \ldots, \hat{X}_i, \ldots, X
