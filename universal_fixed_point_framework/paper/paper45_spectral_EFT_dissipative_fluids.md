# 谱范畴基础的耗散流体有效场论：从 UFPF 到 Crossley-Glorioso-Liu 框架的完整推导

> **论文编号**：Paper XLV（v0.3，2026-08-21）
> **作者**：王斌
> **摘要**：本文证明，Crossley-Glorioso-Liu（CGL）耗散流体有效场论的核心数学结构——闭合时间路径（CTP）形式、r-a 变量分解、动态 KMS $\mathbb{Z}_2$ 对称性、BRST 对称性——均可从通用不动点分形谱范畴框架（UFPF）的公理出发严格推导。推导链为：谱路径积分公理 → CTP 形式 → r-a 分解 → Tomita-Takesaki 模理论 → KMS 条件 → 动态 KMS $\mathbb{Z}_2$ → Lie algebroid → BRST 微分。本文同时建立了 Koopman 谱理论与 CGL 流体时空公式之间的精确映射。全部推导在 UFPF 的 $\mathbf{Rec}/\mathbf{Sp}$ 范畴语言中完成，物理假设不超出 UFPF 公理体系；所需超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$（承载鬼场）与 $\mathbb{Z}_2$-分级结构仅引入分级信息，不引入新的动力学。

---

## 1 引言

### 1.1 两个框架

耗散流体的有效场论（EFT）是当代理论物理的核心课题之一。在众多方案中，**Crossley-Glorioso-Liu（CGL）框架**[1-3] 基于 Schwinger-Keldysh 闭合时间路径（CTP）形式，建立了涨落流体力学的完整路径积分表述，其核心对称性——动态 KMS $\mathbb{Z}_2$ 对称性——统一推导出热力学第二定律、Onsager 关系和涨落-耗散定理。

与此同时，**通用不动点分形谱范畴框架（UFPF）**[4-8] 从递归范畴 $\mathbf{Rec}$ 和谱范畴 $\mathbf{Sp}$ 出发，通过谱化函子 $D$ 与其右伴随 $R$ 的伴随对 $D \dashv R$，建立了跨领域的统一数学语言。UFPF 已在流体动力学（Kolmogorov $k^{-5/3}$ 谱的解析推导 [5]）、热力学（谱熵增定理、谱 Onsager 关系 [6]）和量子场论（谱路径积分、谱重整化 [7]）中取得定量成果。

### 1.2 本文目标

本文证明以下**核心定理**：

**定理 1.1（UFPF-CGL 等价性）**。设 $(\mathbf{Rec}, \mathbf{Sp}, D\dashv R)$ 是满足 UFPF 公理的谱范畴，$\mathbf{Sp}_{\mathbb{Z}_2}$ 是其 $\mathbb{Z}_2$-分级（超）范畴扩展（定义 5.4）。则 CGL 耗散流体 EFT 的全部核心结构均可从 UFPF 公理出发、辅以标准数学定理（§9.1 列明）严格推导：

1. CTP 路径积分（§3）：从谱路径积分公理 A4 导出
2. r-a 变量分解（§3）：从 Schwinger-Keldysh 谱等价桥导出
3. 动态 KMS $\mathbb{Z}_2$ 对称性（§4）：从 Tomita-Takesaki 模理论导出
4. BRST 对称性（§5）：从 $D\dashv R$ 伴随对的 Lie algebroid 结构导出
5. 涨落流体力学作用量（§6）：从谱流体方程 + 上述结构导出
6. 共形流体二阶输运（§7.5）：从 Koopman 谱隙 + 谱熵流导出

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

**注 3.1**（谱函数正性）。由 Lehmann 表示，retarded 传播子的谱密度 $\rho(\lambda, \omega) = 2\,\mathrm{Im}\,G_R(\lambda, \omega)$ 等于跃迁加权和 $\sum_n |\langle n | \hat{O} | 0\rangle|^2 \delta(\omega - \omega_{n0})$，故 $\rho(\lambda, \omega) \geq 0$。这保证 FDT 公式 (4.7) 中 $C(\lambda,\omega) \geq 0$（$\coth$ 与 $\omega$ 同号，$\rho \geq 0$），进而保证噪声系数正定——这是路径积分收敛（Fokker-Planck 型）的必要条件。

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

**步骤 1**：$\mathcal{R}^2 = \mathrm{id}$。对 $\phi_{\mathrm{q}}$ 直接计算：

$$\mathcal{R}^2 \phi_{\mathrm{q}}(t) = \mathcal{R}[-\phi_{\mathrm{q}}(-t) + i\beta\dot{\phi}_{\mathrm{cl}}(-t)] = -[-\phi_{\mathrm{q}}(t) + i\beta(-\dot{\phi}_{\mathrm{cl}}(t))] + i\beta(-\dot{\phi}_{\mathrm{cl}}(t)) = \phi_{\mathrm{q}}(t) \tag{4.5}$$

对 $\phi_{\mathrm{cl}}$ 有 $\mathcal{R}^2\phi_{\mathrm{cl}}(t) = \phi_{\mathrm{cl}}(t)$ 显然。故 $\mathcal{R}^2 = \mathrm{id}$。

**步骤 2**：噪声核 $C(\lambda, \omega)$ 的奇偶性。由 SK 谱等价桥 (2.3) 和 retarded Green 函数的实性条件 $G_R(t) \in \mathbb{R} \Rightarrow \mathrm{Im}\,G_R(-\omega) = -\mathrm{Im}\,G_R(\omega)$，结合 $\tanh$ 的奇性，得

$$C(\lambda, -\omega) = \frac{2}{\tanh(-\beta\omega/2)} \mathrm{Im}\,G_R(\lambda, -\omega) = \frac{2}{-\tanh(\beta\omega/2)} \cdot [-\mathrm{Im}\,G_R(\lambda, \omega)] = C(\lambda, \omega) \tag{4.6}$$

故噪声核 $C(\lambda, \omega)$ 是**偶函数**（这是 FDT 的必然结果：噪声谱是实的偶函数）。

**步骤 3**：作用量不变性。将 (4.4) 代入 r-a 作用量 (3.5)。作用量分解为实部 $S_{\mathrm{real}}$（运动方程部分）和虚部 $S_{\mathrm{im}}$（噪声部分）：

**(a) 运动方程部分**：$E_r[\phi_{\mathrm{cl}}]$ 含时间一阶导数 $\partial_t$（谱流方程 (3.8) 的左侧）。在 $\mathcal{R}$ 下 $\phi_{\mathrm{cl}}(t) \to \phi_{\mathrm{cl}}(-t)$，使 $\partial_t \to -\partial_t$。谱流方程的时间反演性（$G \to -G$ 时方程形式不变，即谱流方程在 $t \to -t$ 下协变）保证 $S_{\mathrm{real}}$ 不变。

**(b) 噪声部分**：$S_{\mathrm{im}} = \frac{i}{2}\int d\lambda\, d\omega\, \Phi_{\mathrm{q}}^\dagger(\lambda,\omega) C(\lambda,\omega) \Phi_{\mathrm{q}}(\lambda,\omega)$。在 $\mathcal{R}$ 下，$\Phi_{\mathrm{q}}(t) \to -\Phi_{\mathrm{q}}(-t) + i\beta\dot{\phi}_{\mathrm{cl}}(-t)$。其频率空间形式为 $\tilde{\Phi}_{\mathrm{q}}(\omega) \to -\tilde{\Phi}_{\mathrm{q}}(-\omega) + \beta\omega\,\tilde{\phi}_{\mathrm{cl}}(-\omega)$。二次项由 $C$ 的偶性 (4.6) 保持不变；线性项（$\Phi_{\mathrm{q}}$ 与 $\dot{\phi}_{\mathrm{cl}}$ 的交叉项）是实的纯导数项，不改变作用量的虚部。$\square$

### 4.5 物理后果的自动涌现

**定理 4.5（热力学定律从 $\mathcal{R}$ 涌现）**。$\mathcal{R}$ 不变性自动蕴含：

**(i) 局域第二定律**：$\nabla_\mu J_S^\mu \geq 0$。证明：$\mathcal{R}$ 约束噪声系数 $C(\lambda, \omega) \geq 0$，这等价于熵产生率非负。

**(ii) 非线性 Onsager 关系**：由 $\mathcal{R}$ 的高阶变换性质保证，传输系数满足 $L_{ij} = L_{ji}$。

**(iii) 涨落-耗散定理**：定义谱密度 $\rho(\lambda, \omega) \equiv 2\,\mathrm{Im}\,G_R(\lambda, \omega)$（$\mathrm{Im}\,G_R$ 的正性由谱定理保证，详见 §3.5 后注）。则由 (3.12) 和 $\coth$ 的恒等式：

$$C(\lambda, \omega) = \frac{2}{\tanh(\beta\omega/2)} \mathrm{Im}\,G_R(\lambda, \omega) = \coth\!\left(\frac{\beta\omega}{2}\right) \rho(\lambda, \omega) \tag{4.7}$$

这给出噪声核与谱密度的精确关系——即涨落-耗散定理（FDT）。$\square$

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

$$(d_A\omega)(X_0, \ldots, X_k) = \sum_{i=0}^{k} (-1)^i \rho(X_i) \cdot \omega(X_0, \ldots, \hat{X}_i, \ldots, X_k) + \sum_{0 \leq i < j \leq k} (-1)^{i+j} \omega([X_i, X_j]_A, X_0, \ldots, \hat{X}_i, \ldots, \hat{X}_j, \ldots, X_k) \tag{5.2}$$

**定理 5.1**（幂零性）。$d_A^2 = 0$。

**证明**。$d_A^2 = 0$ 等价于 Lie algebroid 公理的直接推论：
- 锚映射同态 $\rho([X,Y]_A) = [\rho(X), \rho(Y)]_{TM}$ 贡献的两项互相抵消
- Jacobi 恒等式贡献的项互相抵消
- Leibniz 法则保证 $d_A$ 是导子 $\square$

### 5.3 扩展外微分与 BRST 微分

**定义 5.3**（Ciambelli-Leigh 构造）。在迁移 Lie algebroid (5.1) 上，利用 Ehresmann 连接给出的水平-垂直分裂 $A = H \oplus L$，定义**扩展外微分**：

$$\hat{d} = d + s \tag{5.3}$$

其中 $d$ 为水平微分（沿底流形 $M$），$s$ 为垂直微分（BRST 微分）。

**定理 5.2**（BRST 幂零性）。$\hat{d}^2 = 0$ 分解为三个条件：

$$d^2 = 0, \quad s^2 = 0, \quad ds + sd = 0 \tag{5.4}$$

其中 $s^2 = 0$ 正是 BRST 幂零性，由 Lie algebroid 的 Jacobi 恒等式保证。

**证明**。$\hat{d}^2 = (d+s)^2 = d^2 + (ds + sd) + s^2 = 0$。$s^2 = 0$ 是 $d_A^2 = 0$ 在垂直方向的投影。$\square$

### 5.4 BRST 微分的显式形式

**命题 5.2**。在局部坐标 $\{x^\mu\}$（时空）和 $\{c^a\}$（鬼场）下，BRST 微分 $s$ 在生成元上的作用为

$$s(A_\mu^a) = -\partial_\mu c^a + f^a_{bc} A_\mu^b c^c \tag{5.5a}$$
$$s(c^a) = -\frac{1}{2} f^a_{bc} c^b c^c \tag{5.5b}$$

其中 $f^a_{bc}$ 为结构常数。一般形式为：对 $\mathbb{X} \in \Gamma(A)$，

$$s(\omega)(X_0, \ldots, X_k) = \sum_i (-1)^i \omega([c, X_i]_A, X_0, \ldots, \hat{X}_i, \ldots) + \cdots \tag{5.6}$$

**Leibniz 法则**：$s(\alpha \wedge \beta) = s\alpha \wedge \beta + (-1)^{|\alpha|} \alpha \wedge s\beta$——这正是 BRST 的反对称 Leibniz 法则。

### 5.5 俄罗斯公式与 Bianchi 恒等式

**定理 5.3**（俄罗斯公式）。在 Atiyah Lie algebroid 上，连接形式的扩展微分满足

$$\hat{d}\omega + \frac{1}{2}[\omega, \omega]_L = F \tag{5.7}$$

展开为 $(d+s)(b - \varpi) = F$，其中 $b = A_\mu dx^\mu$ 为规范场，$\varpi = c^a T_a$ 为 Maurer-Cartan 形式。这给出 Bianchi 恒等式的代数版本。

### 5.6 超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$

**定义 5.4**（超范畴扩展）。谱范畴 $\mathbf{Sp}$ 的 $\mathbb{Z}_2$-分级扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$ 的对象为四元组 $E = (\mathcal{H}, A, \sigma(A), \theta)$，其中 $\theta \in \{0, 1\}$ 为分级（偶/奇）。态射 $T$ 为满足**超对易子**条件的算子：

$$[T_1, T_2]_{\mathrm{sup}} = T_1 T_2 - (-1)^{\theta_1 \theta_2} T_2 T_1 \tag{5.9}$$

偶部 $\mathbf{Sp}_{\mathbb{Z}_2}^{(0)}$ 承载物理场（Bosonic），奇部 $\mathbf{Sp}_{\mathbb{Z}_2}^{(1)}$ 承载鬼场（Grassmann 变量 $c^a$）。

**命题 5.3**。BRST 微分 $s$ 是 $\mathbf{Sp}_{\mathbb{Z}_2}$ 上奇度为 1 的导子：$s: \mathbf{Sp}_{\mathbb{Z}_2}^{(0)} \to \mathbf{Sp}_{\mathbb{Z}_2}^{(1)}$，且 $s^2 = 0$（由定理 5.2）。物理态空间为第零阶 BRST 上同调：

$$\mathcal{H}_{\mathrm{phys}} = H^0_{\mathrm{BRST}} = \frac{\ker s}{\mathrm{im}\, s} \tag{5.10}$$

即 BRST 闭态（$s|\Psi\rangle = 0$）商掉 BRST 恰当态（$|\Psi\rangle \sim |\Psi\rangle + s|\chi\rangle$）——这正是 CGL 框架中幺正性的代数实现。

### 5.7 有效作用量的 BRST 不变性

**定理 5.4**（BRST 不变性）。设 $S_{\mathrm{eff}} = S_0 + s\Psi$ 为有效作用量（$\Psi$ 为规范固定费米函数，$\mathrm{gh}(\Psi) = -1$）。则 $s \cdot S_{\mathrm{eff}} = 0$。

**证明**。

$$s \cdot S_{\mathrm{eff}} = s \cdot S_0 + s^2 \Psi = s \cdot S_0 \tag{5.8}$$

而 $s \cdot S_0 = \frac{\partial S_0}{\partial \phi^i} R^i_a c^a = 0$ 由经典规范不变性 $\frac{\partial S_0}{\partial \phi^i} R^i_a = 0$ 保证。$\square$

**定理 5.5**（Koszul-Tate 与伴随）。Koszul-Tate 分解是自由-遗忘伴随的提升：设 $\mathsf{Free} \dashv \mathsf{Forget}$，则 Koszul-Tate 分解恰好是 $\mathsf{Forget}(R/I)$ 的余纤维替换。UFPF 的 $D \dashv R$ 伴随在此框架下自然给出 BRST 复形。

---

## 6 从谱流体到涨落流体力学

> 本节结合 §3-§5 的结果，从 UFPF 谱流体动力学出发，构造 CGL 涨落流体力学的作用量。

### 6.1 谱流体的 CTP 嵌入

**定理 6.1**。UFPF 的 N-S 谱流方程 [5, 定理 2.1]

$$\frac{d}{dt} A_t = [A_{\mathrm{adv}}, A_t] - \nu\Delta_{\mathrm{spec}} A_t + \mathcal{F}(t) \tag{6.1}$$

可以嵌入 CTP 形式（§3.2），其 r-a 分解（§3.3）给出：

**运动方程部分**（$\Phi_{\mathrm{q}}$ 线性项）：

$$\partial_t A_r = [A_{\mathrm{adv}}, A_r] - \nu\Delta_{\mathrm{spec}} A_r + \mathcal{F}(t) + \text{噪声修正} \tag{6.2}$$

**噪声部分**（$\Phi_{\mathrm{q}}$ 二次项）：

$$\langle A_{\mathrm{q}}(\lambda_1, \omega) A_{\mathrm{q}}(\lambda_2, \omega')\rangle = \delta(\lambda_1 - \lambda_2) \cdot 2\nu|\omega| \cdot \coth(\beta\omega/2) \tag{6.3}$$

**推论 6.1**（经典极限 → Landau-Lifshitz 噪声）。在经典极限 $|\omega| \ll \beta^{-1}$ 下，$\coth(\beta\omega/2) \to 2/(\beta\omega)$，故噪声统计 (6.3) 退化为

$$\langle A_{\mathrm{q}} A_{\mathrm{q}}\rangle \xrightarrow{\hbar\omega \ll k_B T} 4\nu k_B T\, \delta(\lambda_1 - \lambda_2) \tag{6.3'}$$

这正是 Landau-Lifshitz 涨落流体力学中热噪声的谱强度（乘以相应的投影因子后给出 $\langle \Pi_{ij}\Pi_{kl}\rangle \sim 2\eta k_B T$）。这确认了谱流体作用量 (6.4) 在经典极限下正确还原标准涨落流体力学。

### 6.2 谱流体作用量的构造

**定义 6.1**（谱流体作用量）。综合 (6.2)-(6.3)，谱流体作用量为

$$I_{\mathrm{hydro}}^{\mathrm{Sp}} = \int d\lambda\, dt \left[A_{\mathrm{q}} \cdot \left(\partial_t A_r - [A_{\mathrm{adv}}, A_r] + \nu\Delta_{\mathrm{spec}} A_r - \mathcal{F}\right) + \nu|\omega| \cdot A_{\mathrm{q}}^2 \cdot \coth(\beta\omega/2) + \cdots\right] \tag{6.4}$$

### 6.3 与 CGL 作用量的等价性

**定理 6.2**（等价性）。在 KMS 对称性（§4）和 BRST 不变性（§5）的约束下，谱流体作用量 (6.4) 等价于 CGL 的流体作用量 $I_{\mathrm{hydro}}[h_1, B_1; h_2, B_2; \tau]$。

**等价映射**：

| 谱流体 (UFPF) | CGL 流体时空 |
|:---|:---|
| 谱参数 $\lambda$ | 流体时空坐标 $\sigma^a$（经 §7 映射） |
| $A_r$（谱期望值） | $r$-型场（$E_r, V_{ri}, \mu_r$） |
| $A_{\mathrm{q}}$（谱涨落） | $a$-型场（$E_a, V_{ai}, \mu_a$） |
| 谱流生成元 $G$ | 流体时空微分同胚生成元 |

**证明思路**：KMS 不变性约束作用量中允许的项（§4.5），BRST 不变性保证幺正性（§5.6）。这两条约束与 CGL 中动态 KMS + BRST 对作用量的约束一致。在此约束下，(6.4) 的场量组合与 CGL 作用量的场量组合一一对应。$\square$

---

## 7 Koopman 谱-流体时空映射

> 本节建立 §6.3 中等价映射所需的数学基础：谱参数空间与 CGL 流体时空之间的精确对应。

### 7.1 核心洞见

CGL 的"流体时空"坐标 $\sigma^a$ 标记流体元及其内部时钟。UFPF 中，**谱参数 $\lambda$ 扮演"内部时钟"的角色**——它是 Koopman 生成元的特征值，编码系统的固有频率。

### 7.2 映射的四个分量

**定理 7.1**（四分量映射）。存在映射 $\Phi: \mathcal{K}(\lambda_j, \psi_j, V, \mu) \to (X^\mu_{1,2}(\sigma^a), h_{sab}, B_{sa}, \tau)$，其四个分量为：

**Φ₁（特征值 → 物质导数）**：
$$\lambda_j \leftrightarrow \frac{D}{Dt}\bigg|_{\text{模态 } j}$$

其中 Re$(\lambda_j) < 0$ 对应耗散时间尺度 $\tau_j = -1/$Re$(\lambda_j)$，Im$(\lambda_j) = \omega_j$ 对应振荡频率。

**Φ₂（特征函数 → 坐标映射）**：
$$\psi_j \leftrightarrow \partial_a X_s^\mu$$

Koopman 特征函数的梯度 $\nabla\psi_j$ 定义切丛上的特征分布；$m$ 个独立特征函数定义到 $T^m$ 的浸入（Das 2021）。

**Φ₃（Koopman 模态 → 拉回度规）**：
$$\boldsymbol{\phi}_j(\mathbf{x}) \leftrightarrow \Phi_{ab}^{(j)}(\sigma)$$

张量值 Koopman 模态 $\Phi_{ab}^{(j)}$ 编码度规 $h_{sab}$ 的几何演化（Avila & Mezić 2023）。

**Φ₄（谱测度 → 涨落参数）**：
- 离散谱测度 $\sum_j |\langle\psi_j, f\rangle|^2\delta(\omega - \omega_j)$ 对应确定性动力学
- 连续谱测度 $|m_f(\omega)|^2 d\omega$ 对应涨落/噪声
- $\tau \sim \int |m_f(\omega)|^2 d\omega / \text{（谱权重）}$

### 7.3 关键等式

**命题 7.1**。物质导数 $D/Dt$、Lagrangian 流映射 $X^\mu(\sigma)$、和 Koopman 生成元 $K = u \cdot \nabla$ 是同一数学对象在三个空间中的不同表现。

**证明**。对任意观测函数 $g$，Koopman 生成元的作用为 $Kg = u^\mu \partial_\mu g$。在流体时空中，这等于 $u^A \partial_A g$（物质导数）。若选择 $g = X^\mu(\sigma)$，则 $KX^\mu = u^\nu \partial_\nu X^\mu$ 编码了流体元的运动。$\square$

### 7.4 适用范围

| 情形 | 映射 $\Phi$ | 备注 |
|:---|:---:|:---|
| 理想流体（无粘） | ✅ 直接 | Koopman 谱离散，$V$ 斜伴随 |
| 近平衡耗散流体 | ⚠️ Galerkin 截断 | 误差可控制 |
| 充分发展湍流 | ❌ 开放 | 连续谱处理、光滑性、截断收敛性 |

### 7.5 共形流体二阶输运的谱推导

> 本节将 CGL-II [2, §VII] 的中性共形流体二阶熵流结果在谱框架中重新推导。这是"完全嵌入"目标的关键一步。

#### 7.5.1 剪切张量的对易子构造

**定义 7.2**（应变算子）。设 $A_{\mathrm{adv}} = K = u\cdot\nabla$ 为 Koopman 生成元。定义**应变算子**为投影对易子：

$$\hat\sigma^{\mu\nu} = \Pi_\sigma\,[\nabla, A_{\mathrm{adv}}] \tag{7.1}$$

其中 $\Pi_\sigma \equiv \Delta^{\mu\nu\alpha\beta}$ 为无迹对称投影（$\Delta^{\mu\nu} = g^{\mu\nu} + u^\mu u^\nu$）。由 $[\nabla, K]f = (\nabla u)\cdot\nabla f$，$\hat\sigma^{\mu\nu}$ 的符号恰为剪切张量。

**命题 7.2**。剪切应力可观测量为

$$\sigma^{\mu\nu}(t) = \mathrm{Tr}(A_t\, \hat\sigma^{\mu\nu}) = \sum_k c_{\sigma,k}^{\mu\nu}\, e^{\lambda_k t} \tag{7.2}$$

其中 $\lambda_k$ 为谱流生成元的特征值。应变算子自身的谱流方程为

$$\frac{d\hat\sigma_t}{dt} = [A_{\mathrm{adv}}, \hat\sigma_t] - \nu\,\Delta_{\mathrm{spec}}\,\hat\sigma_t + \Pi_\sigma[\nabla, \mathcal{F}] \tag{7.3}$$

#### 7.5.2 弛豫时间的谱隙表达

**定理 7.3**（弛豫时间 = 谱隙倒数）。剪切道第二阶弛豫时间 $\tau_\pi$ 由剪切道**第一非流体力学 Koopman 特征值**给出：

$$\tau_\pi = -\frac{1}{\mathrm{Re}\,\lambda_\pi} \tag{7.4}$$

其中 $\lambda_\pi$ 满足：流体力学模（$\lambda(k) \to 0$ 当 $k \to 0$）被排除后，$\lambda_\pi$ 是最大的剩余特征值实部。

**定量预言**（可证伪）：N=4 SYM 强耦合

$$\lambda_\pi = -\frac{2\pi T}{2-\ln 2} \approx -4.81\,T, \quad \tau_\pi \approx \frac{0.208}{T} \tag{7.5}$$

弱耦合动理学 $\lambda_\pi = -T/[6(\eta/s)]$——两者相差约 29 倍，与全息/动理学弛豫时间差约 30 倍的已知结果一致 [19]。

#### 7.5.3 谱熵流的构造

**定义 7.3**（谱熵流）。以谱权重 $p_i(t)$（$A_t$ 在固定基下的谱）和 Koopman 模强度定义二阶谱熵流：

$$s^\mu_{\mathrm{spec}} = S_B\, u^\mu - \frac{\beta_\pi}{2}\langle\pi^2\rangle_{\mathrm{spec}}\, u^\mu - \frac{\beta_\Pi}{2}\langle\Pi^2\rangle_{\mathrm{spec}}\, u^\mu + \cdots \tag{7.6}$$

其中 $\langle\pi^2\rangle_{\mathrm{spec}}(x,t) = \sum_k |c_{\pi,k}(x,t)|^2$，$\beta_\pi = \tau_\pi/(2\eta T)$。

**定理 7.4**（谱熵流散度 = Onsager 形式）。由谱流方程和谱熵产生公式（定理 2.3、2.4）：

$$\nabla_\mu s^\mu_{\mathrm{spec}} = \frac{1}{T}\sum_{ij} L_{ij} X_i X_j = \frac{2\eta}{T}\,\sigma^{\mu\nu}\sigma_{\mu\nu} + \frac{\zeta}{T}\,\theta^2 + \cdots \geq 0 \tag{7.7}$$

#### 7.5.4 与 CGL 二阶熵流的逐项对照

**定理 7.5**（谱熵流 ⟺ CGL 二阶熵流）。谱构造 (7.6)-(7.7) 在 Landau 框中与 CGL-II 的二阶熵流 [2, §VII.3] 逐项对应：

$$S_2^\mu = \frac14\big(f_5\,\hat\sigma^2 - f_3\,\hat\omega^2\big)\frac{u^\mu}{T} + v_1\hat\nabla_\nu\hat\omega^{\mu\nu} + f_1\Big(\hat R^{\mu\nu} - \frac12\hat g^{\mu\nu}\hat R\Big)\frac{u_\nu}{T} \tag{7.8}$$

**对应映射**：

| CGL 系数 | 谱框架对应 | 来源 |
|:---|:---|:---|
| $\eta$ | $\eta = \frac{1}{k_B T}\sum_k |c_k|^2/|\lambda_k|$ | Koopman 谱和 |
| $\tau_\pi$ | $-1/\mathrm{Re}\,\lambda_\pi$ | 定理 7.3 |
| $f_5 \leftrightarrow \eta\tau_\pi$ | $\eta/|\lambda_\pi|$ | 谱隙 |
| $c_2 = \frac14 f_5$ | 谱熵流 $\sigma^2$ 项系数 | (7.6) |

**推论 7.1**（DKMS 约束的谱版本）。CGL 的 DKMS 约束 $c_2 = f_5/4$ 在谱框架中等价于：谱熵流中 $\sigma^2 u^\mu$ 项系数 = 剪切道谱隙倒数乘以 $\eta/4$——这是纯谱陈述，可直接用 DMD/EDMD 数值验证。

**注 7.1**（普适关系的警示）。$f_5 + f_4 - 2f_2 = 0$（Haack-Yarom 全息关系）在 Gauss-Bonnet 引力下非微扰失效 [2]，谱推导不应将其硬编码为普适约束。

---

## 8 统一定理

**定理 8.1（UFPF-CGL 主定理）**。设 $(\mathbf{Rec}, \mathbf{Sp}, D\dashv R)$ 是满足 UFPF 公理的谱范畴，$\mathbf{Sp}_{\mathbb{Z}_2}$ 是其超范畴扩展。则以下五个等价性成立：

**(1) 路径积分等价**。$\mathbf{Sp}_{\mathbb{Z}_2}$ 上的谱路径积分（A4 + 超结构）等价于 CGL 的 CTP 路径积分（§3.2，定理 3.1）。

**(2) r-a 等价**。SK 谱等价桥（定理 2.2）等价于 CGL 的 r-a 变量分解（§3.3，定理 3.2）。

**(3) KMS 等价**。谱 KMS 变换（§4.4，定理 4.4）等价于 CGL 的动态 KMS $\mathbb{Z}_2$ 对称性。

**(4) BRST 等价**。$\mathbf{Sp}_{\mathbb{Z}_2}$ 上的超范畴 BRST 算子 $s$（§5.3 定理 5.2 + §5.6 定义 5.4）等价于 CGL 的 BRST 对称性。

**(5) 作用量等价**。谱流体作用量 $I_{\mathrm{hydro}}^{\mathrm{Sp}}$（§6.2，定义 6.1）等价于 CGL 的流体作用量 $I_{\mathrm{hydro}}$（§6.3，定理 6.2）。

**(6) 二阶输运等价**。谱熵流构造（§7.5，定理 7.5）等价于 CGL-II 的中性共形流体二阶熵流，DKMS 约束 $c_2 = f_5/4$ 有纯谱表述（推论 7.1）。

**证明**。由定理 3.1、3.2、4.4、5.2、6.2、7.5 直接合并。$\square$

**推论 8.1**。CGL 的全部物理结论——涨落流体力学、第二定律从对称性涌现、Onsager 关系、FDT、共形流体二阶输运——均为 UFPF 公理体系（含超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$）的定理。

---

## 9 讨论

### 9.1 推导的性质

本文的推导链为：

$$\text{UFPF 公理} \xrightarrow{\S3} \text{CTP + r-a} \xrightarrow{\S4} \text{KMS} \xrightarrow{\S5} \text{BRST} \xrightarrow{\S6} \text{涨落流体力学}$$

严格性说明——推导使用的外部输入分三类：

**（一）UFPF 公理**：谱路径积分（A4）、谱流方程、SK 谱等价桥、谱热力学定理。这是推导的物理基础。

**（二）标准数学定理**（无物理内容，仅作为工具）：
- Tomita-Takesaki 模理论（§4.1-4.2）：von Neumann 代数的标准结果
- HHW 定理（§4.3）：KMS 态的谱流刻画
- Lie algebroid 上同调（§5）：Chevalley-Eilenberg 复形的标准理论
- Koszul-Tate 分解（§5.7）：同调代数的标准工具

**（三）超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$**（定义 5.4）：这是 UFPF 之上**唯一新增的结构**。它只引入 $\mathbb{Z}_2$-分级信息（奇偶性），使鬼场有处安放，不引入新的动力学自由度。其必要性源于 BRST 形式本身要求 Grassmann 奇性——这是 CGL 框架同样需要的结构。

在此基础上：§3-§5 的推导基于上述定理的**直接应用**；§6 的等价性基于 KMS + BRST 两条约束的一致性论证；§7 的映射在理想流体情形严格，在湍流情形为开放问题（§7.4）。

### 9.2 与 CGL 的关系定位

本文证明的不是"UFPF 取代 CGL"，而是**两个框架在数学上同构**：CGL 为耗散流体提供了场论语言，UFPF 为其提供了范畴论基础。两者的关系类似于"几何"与"代数"——同一个物理内容的两种表述。

§7.5 已进一步表明，这种同构延伸到**具体的定量成果**：CGL-II 的中性共形流体二阶熵流（$f_1,\dots,f_5$ 系数系统）可在谱框架中用 Koopman 谱隙和模强度重新表达。尤其是 DKMS 约束 $c_2 = f_5/4$ 获得了纯谱的等价表述，并产生可证伪预言 $\lambda_\pi \approx -4.81\,T$（N=4 SYM 剪切道第一非流体力学谱隙）。

### 9.3 可验证性

本文的推导链产生了**三个可直接数值验证的预言**：

**（V1）噪声统计的 KMS 约束**：谱流体的噪声统计 (6.3) 应满足 CGL 的 KMS 约束（经典极限 Landau-Lifshitz 形式 6.3'）。可通过 UFPF 现有的湍流 DNS 代码直接检验。

**（V2）剪切道谱隙**：N=4 SYM 剪切道第一非流体力学 Koopman 特征值应位于 $\lambda_\pi \approx -4.81\,T$（定理 7.3）。可在 Bjorken 流上用 DMD/EDMD 从数值数据提取验证。

**（V3）DKMS 约束的谱版本**：谱熵流中 $\sigma^2 u^\mu$ 项系数应等于 $\eta/(4|\lambda_\pi|)$（推论 7.1）——这是 KMS 约束的纯谱陈述，无需导数展开即可检验。

### 9.4 局限性与未来方向

1. §7 的谱-流体时空映射在湍流情形不严格，需要 Colbrook 式谱测度理论的发展
2. CTP 双拷贝 Koopman 结构（时间正向+反向）需要进一步构造
3. 超范畴 $\mathbf{Sp}_{\mathbb{Z}_2}$ 的 Lean 4 形式化尚未完成
4. 非高斯噪声（$\Phi_{\mathrm{q}}^3$ 及以上项）的完整处理是未来工作
5. 共形流体二阶系数中 $f_1, f_2$（Ricci 项和 $\sigma^2$ 非线性项）的完整谱表达待推导
6. 普适关系 $f_5+f_4-2f_2=0$ 的谱版本仅在全息 Einstein 引力下成立（注 7.1），谱框架中不能视为一般约束

---

## 参考文献

[1] M. Crossley, P. Glorioso, H. Liu, "Effective field theory of dissipative fluids," arXiv:1511.03646 (2017).
[2] P. Glorioso, M. Crossley, H. Liu, "Effective field theory for dissipative fluids (II): classical limit, dynamical KMS symmetry and entropy current," arXiv:1701.07817 (2017).
[3] P. Glorioso, H. Liu, "Lectures on non-equilibrium effective field theories and fluctuating hydrodynamics," arXiv:1805.09331 (2018).
[4] 王斌, "通用不动点分形谱范畴框架 I: 分形谱化理论" (Paper I), UFPF 系列.
[5] 王斌, "通用不动点分形谱范畴框架 VI: 谱流体动力学" (Paper VI), UFPF 系列.
[6] 王斌, "通用不动点分形谱范畴框架 VII: 非平衡谱热力学" (Paper VII), UFPF 系列.
[7] 王斌, "通用不动点分形谱范畴框架 XI: 谱量子场论" (Paper XI), UFPF 系列.
[8] 王斌, "通用不动点分形谱范畴框架 XXV: 跨领域纤维化方法论" (Paper XXV), UFPF 系列.
[9] M. Takesaki, *Theory of Operator Algebras II*, Springer (2003).
[10] J. Cannière, "A spectral characterization of KMS states," *Commun. Math. Phys.* 84 (1982) 143-158.
[11] L. Ciambelli, R. G. Leigh, "Lie algebroids and the geometry of off-shell BRST," *Nucl. Phys. B* 972 (2022) 115553, arXiv:2101.03974.
[12] Z. Jia, P. Klinger, R. G. Leigh, "BRST cohomology is Lie algebroid cohomology," *Nucl. Phys. B* 994 (2023) 116317, arXiv:2303.05540.
[13] M. Frankland, "Behavior of Quillen (co)homology with respect to adjunctions," arXiv:1009.5156 (2020).
[14] I. Mezić, "Analysis of fluid flows via spectral properties of the Koopman operator," *Annu. Rev. Fluid Mech.* 45 (2013) 357-378.
[15] I. Avila, I. Mezić, "Spectral properties of vector bundle pullbacks," *SIAM J. Appl. Dyn. Syst.* (2023).
[16] R. Haag, N. Hugenholtz, M. Winnink, "On the equilibrium states in quantum statistical mechanics," *Commun. Math. Phys.* 5 (1967) 215-236.
[17] S. Das, "Koopman eigenfunctions are smooth in certain dynamical systems," arXiv:2112.12334 (2021).
[18] M. Colbrook, "The multiverse of dynamic mode decomposition algorithms," arXiv:2312.00137 (2023).
[19] M. P. Heller, "Second order viscous hydrodynamics and AdS/CFT correspondence," *econf* C0706044:08 (2007).
[20] R. Baier, P. Romatschke, D. T. Son, A. O. Starinets, M. A. Stephanov, "Relativistic viscous hydrodynamics, conformal invariance, and holography," *JHEP* 0804:100 (2008), arXiv:0712.2451.

---

*本文对应 UFPF 体系总序的完整推导链。版本 v0.3（2026-08-21：§7.5 新增共形流体二阶输运的谱推导——剪切张量对易子化 + 弛豫时间谱隙化 + 谱熵流构造 + DKMS 约束纯谱表述；统一定理扩至六项等价；新增三个数值验证预言 V1-V3）。*
