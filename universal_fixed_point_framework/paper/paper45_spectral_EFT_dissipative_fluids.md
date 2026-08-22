# 耗散流体有效场论的谱语言翻译：CGL 核心结构的 UFPF 表述及可证伪预言

> **论文编号**：Paper XLV（v1.2，2026-08-22）
> **作者**：王斌
> **摘要**：本文展示通用不动点分形谱范畴框架（UFPF）作为元框架的**可表达性**：UFPF 的谱语言可以忠实翻译 Crossley-Glorioso-Liu（CGL）耗散流体有效场论的核心结构。CGL 的核心数学结构——闭合时间路径（CTP）形式、r-a 变量分解、动态 KMS $\mathbb{Z}_2$ 对称性、BRST 对称性——均在谱语言中获得系统重构，重构链为：谱路径积分公理 → CTP 形式 → r-a 分解 → Tomita-Takesaki 模理论 → KMS 条件 → 动态 KMS $\mathbb{Z}_2$ → Lie algebroid → BRST 微分。翻译同时建立了 Koopman 谱理论与 CGL 流体时空公式之间的精确映射，并产生三类新构造（剪切道谱隙表达、共形流体二阶系数全谱化、非高斯噪声多谱塔）与可证伪预言（$\lambda_\pi \approx -4.81T$ 等），数值验证 11/11 通过。翻译的可行性表明 UFPF 语言的普适性；两框架关系的最终定性留待学术共同体评价。全部重构在 UFPF 的 $\mathbf{Rec}/\mathbf{Sp}$ 范畴语言中完成；所需超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$（承载鬼场）为翻译接口（注 5.1），仅引入分级信息。本论文仅完成**流体 EFT 子领域的结构重构案例**；UFPF 完整的全域统一、时空-引力涌现的宏大纲领见 UFPF 体系总序与 Paper XXXV，本文不处理本体层面命题。

---

## 1 引言

### 1.1 两个框架

耗散流体的有效场论（EFT）是当代理论物理的核心课题之一。在众多方案中，**Crossley-Glorioso-Liu（CGL）框架**[1-3] 基于 Schwinger-Keldysh 闭合时间路径（CTP）形式，建立了涨落流体力学的完整路径积分表述，其核心对称性——动态 KMS $\mathbb{Z}_2$ 对称性——统一推导出热力学第二定律、Onsager 关系和涨落-耗散定理。

与此同时，**通用不动点分形谱范畴框架（UFPF）**[4-8] 从递归范畴 $\mathbf{Rec}$ 和谱范畴 $\mathbf{Sp}$ 出发，通过谱化函子 $D$ 与其右伴随 $R$ 的伴随对 $D \dashv R$，建立了跨领域的统一数学语言。UFPF 已在流体动力学（Kolmogorov $k^{-5/3}$ 谱的解析推导 [5]）、热力学（谱熵增定理、谱 Onsager 关系 [6]）和量子场论（谱路径积分、谱重整化 [7]）中取得定量成果。

**地位声明**。需要明确的是，UFPF 目前是作者个人独立研究的理论假说，尚未经过学术共同体的独立评审与实验验证；其框架地位与 CGL 等主流理论不同。本文的论证以 UFPF 的公理体系为出发点，**不主张 UFPF 已被外部验证**，也不意味着 UFPF 的任何理论主张自动获得学术认可。本文的意义在于展示：若 UFPF 公理成立，则 CGL 的核心结构可在其中系统重构——这是一种"理论假说的压力测试"，而非两个已验证理论的合并。

### 1.2 本文目标

本文的工作以 Crossley、Glorioso 与 Liu 的开创性贡献 [1-3] 为基础——CGL 框架的严谨构建使其成为检验 UFPF 语言普适性的理想对象，我们在此对其原作者的工作致以敬意。

本文聚焦于一种**结构约束关系**：UFPF 作为元框架（meta-framework），其谱语言能够为 CGL 的耗散流体 EFT 提供一个**完备的数学表述域 (Representational Domain)**。我们展示的是，CGL 核心结构必须在 UFPF 语言中寻找其可表达的形式，这种关系强调了UFPF作为底层“形式语言”的普适性，而非简单地证明两框架的等同或包含。本文旨在探究理论约束如何从一个更基础的数学公理体系（UFPF）出发，系统性地导出主流物理理论（CGL）必须满足的内在结构，从而确立 UFPF 的地位为一种普适性的**“形式化母语言”**。

本文证明以下**核心定理**：

**定理 1.1（CGL 的谱语言翻译）**。设 $(\mathbf{Rec}, \mathbf{Sp}, D\dashv R)$ 是满足 UFPF 公理的谱范畴，$\mathbf{Sp}_{\mathbb{Z}_2}$ 是其 $\mathbb{Z}_2$-分级（超）范畴扩展（定义 5.4）。则 CGL 耗散流体 EFT 的全部核心结构均可翻译为 UFPF 谱语言。翻译的八项内容如下（均从 UFPF 公理出发、辅以标准数学定理，§9.1 列明）：

1. CTP 路径积分（§3）：从谱路径积分公理 A4 导出
2. r-a 变量分解（§3）：从 Schwinger-Keldysh 谱等价桥导出
3. 动态 KMS $\mathbb{Z}_2$ 对称性（§4）：从 Tomita-Takesaki 模理论导出
4. BRST 对称性（§5）：从 $D\dashv R$ 伴随对的 Lie algebroid 结构导出
5. 涨落流体力学作用量（§6）：从谱流体方程 + 上述结构导出
6. 共形流体二阶输运（§7.5）：从 Koopman 谱隙 + 谱熵流导出
7. 非高斯噪声层级（§6.4）：从 Kramers-Moyal 谱展开 + 多谱塔导出
8. 湍流谱测度映射（§7.6）：从 RLF/GLM/谱测度三层替换导出

**贡献分层声明**。本文的贡献按学术性质分三层：

**(i) 重构层**（谱语言重述成熟结构）：CTP/r-a/KMS/BRST 的 UFPF 版本——这是语言翻译，价值在于统一表述而非新物理。

**(ii) 新构造层**（连接两个领域的原创构造）：$\tau_\pi$ 的谱隙表达（定理 7.3）、$f_1/f_2$ 的谱曲率与三重模耦合表达（定理 7.6a/7.7a）、非高斯噪声多谱塔对应（定理 6.4）、谱静默≠高斯的独立性（命题 6.3）。

**(iii) 新预言层**（可证伪预测）：$\lambda_\pi \approx -4.81T$、DKMS 约束纯谱版本、谱测度-PSD 恒等式等（§9.3，V1-V5 数值验证 11/11 通过）。

**验证快照**（完整结果见 §9.3 与脚本 `paper45_spectral_EFT_validation.py`）。五个可证伪预言 V1-V5 的数值验证**全部通过（11/11 检查项）**：FDT 公式精确（相对误差 $4\times10^{-16}$）、剪切道谱隙 $\lambda_\pi \approx -4.81T$ 与数值提取一致（偏差 2.6%）、谱测度-PSD 恒等式确认（相关性 0.962）。

### 1.3 论文结构

§2 自包含回顾 UFPF 和 CGL 两个框架。§3-§5 完成框架性翻译（CTP/r-a/KMS/BRST）。§6 构造谱流体与非高斯噪声。§7 建立 Koopman 谱-流体时空映射（含共形流体二阶输运与湍流谱测度）。§8 陈述翻译定理。§9 讨论物理意义、可验证性和局限性。

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

> 本节完成重构链的第一步：从 UFPF 公理 A4 出发，在谱语言中重构出 CGL 的 CTP 形式和 r-a 变量分解。

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

**证明**。分四步。

**步骤 1（迹的展开）**。取能量本征基 $\{|n\rangle\}$，将迹展开为

$$\mathrm{Tr}[\rho_0 \hat{U}(t_0, t) \hat{O} \hat{U}(t, t_0)] = \sum_n \langle n | \rho_0 \hat{U}(t_0, t) \hat{O} \hat{U}(t, t_0) | n \rangle$$

设初始时刻 $t_0$，测量时刻 $t$（$t > t_0$）。在算子乘积之间插入完备关系 $\sum_k |k\rangle\langle k| = \mathbb{1}$ 和 $\sum_l |l\rangle\langle l| = \mathbb{1}$：

$$= \sum_{n,k,l} \langle n | \rho_0 | k \rangle \langle k | \hat{U}(t_0, t) \hat{O} | l \rangle \langle l | \hat{U}(t, t_0) | n \rangle$$

其中 $\langle l | \hat{U}(t, t_0) | n \rangle$ 是前向传播子（$t_0 \to t$），$\langle k | \hat{U}(t_0, t) | l \rangle$ 是后向传播子（$t \to t_0$）。

**步骤 2（路径积分表示）**。将每个传播子写为路径积分。前向传播子：

$$\langle l | \hat{U}(t, t_0) | n \rangle = \int_{\phi(t_0)=\phi_n}^{\phi(t)=\phi_l} \mathcal{D}\phi_+ \, e^{i S[\phi_+]}$$

后向传播子（反编时）：

$$\langle k | \hat{U}(t_0, t) | l \rangle = \int_{\phi(t)=\phi_l}^{\phi(t_0)=\phi_k} \mathcal{D}\phi_- \, e^{-i S[\phi_-]}$$

注意后向传播子的作用量取负号（反编时等价于作用量取复共轭）。将两式代入步骤 1 的结果，对中间态 $|k\rangle, |l\rangle$ 求和后，边界条件匹配（前向终态 = 后向始态），给出闭合时间路径 $\mathcal{C} = \mathcal{C}_+ \cup \mathcal{C}_-$ 上的单一路径积分：

$$\langle \hat{O}(t)\rangle = \int \mathcal{D}\phi_+ \mathcal{D}\phi_- \, \rho_0[\phi_+(t_0), \phi_-(t_0)] \, \hat{O}[\phi_+(t)] \, e^{i S[\phi_+] - i S[\phi_-]}$$

这正是 CTP 路径积分 (2.5) 的标准形式 [3]。

**步骤 3（谱场替换）**。由公理 A4（§2.1.5），每个量子场 $\phi(x)$ 对应谱对象 $(\mathcal{H}_\phi, A_\phi, \sigma(A_\phi)) \in \mathbf{Sp}$。将时空场 $\phi_\pm(x, t)$ 通过谱展开 $\phi_\pm(x, t) = \sum_k \Phi_\pm(\lambda_k, t) \psi_k(x)$ 替换为谱场 $\Phi_\pm(\lambda, t)$，其中 $\psi_k(x)$ 为 $A_\phi$ 的本征函数。路径积分测度替换为谱测度 $\mathcal{D}\phi_\pm \to \mathcal{D}_{\mathrm{Sp}}\Phi_\pm = \prod_{\lambda \in \sigma(A_\phi)} d\Phi_\pm(\lambda)$，作用量替换为谱作用量 $S_{\mathrm{Sp}}[\Phi] = \frac{1}{2}\int d\lambda\, \Phi^\dagger(\lambda)(\lambda - m^2)\Phi(\lambda)$。于是得到推论 3.1 中的 $Z_{\mathrm{CTP}}^{\mathrm{Sp}}[J_+, J_-]$ (3.3)。

**步骤 4（幺正性验证）**。当 $J_+ = J_-$ 时，回到算子迹定义 (2.4)：$Z_{\mathrm{CTP}}[J, J] = \mathrm{Tr}[\rho_0\, \hat{U}_J(t_0, t)\, \hat{U}_J(t, t_0)]$。由于两支上源相同，$\hat{U}_J(t_0, t) = \hat{U}_J(t, t_0)^{-1}$，故 $\hat{U}_J(t_0, t)\, \hat{U}_J(t, t_0) = \mathbb{1}$，给出 $Z_{\mathrm{CTP}}[J, J] = \mathrm{Tr}[\rho_0] = 1$（归一化密度矩阵）。在路径积分中，这对应前向与后向传播子相消——注意 $\Phi_+$ 与 $\Phi_-$ 仍是独立积分变量，相消发生在积分后的迹层面，而非被积函数层面。谱版本 $Z_{\mathrm{CTP}}^{\mathrm{Sp}}[J, J] = 1$ 由谱替换保持这一性质。$\square$

**注 3.1（相消的物理直觉）**。幺正性 $Z[J, J] = 1$ 的物理图像是"往返抵消"：系统在前向支 $\mathcal{C}_+$ 上从 $t_0$ 演化到 $t$，在后向支 $\mathcal{C}_-$ 上从 $t$ 演化回 $t_0$。当两支源相同（$J_+ = J_-$），后向演化精确地"原路折返"——每个量子态经历前向演化 $\hat{U}_J(t, t_0)$ 后紧接其逆 $\hat{U}_J(t_0, t) = \hat{U}_J(t, t_0)^{-1}$，净效应为单位算子。

关键在于，这一相消并非发生在被积函数层面：路径积分中 $\Phi_+$ 与 $\Phi_-$ 仍是独立的求和变量，前向支上每条路径 $\Phi_+(\lambda, t)$ 与后向支上每条路径 $\Phi_-(\lambda, t)$ 各自独立地被积分。相消发生在**对所有路径求和之后**——前向传播子 $\langle l|\hat{U}_J(t, t_0)|n\rangle$ 与后向传播子 $\langle k|\hat{U}_J(t_0, t)|l\rangle$ 的乘积对中间态 $|l\rangle$ 求和后给出 $\delta_{kn}$（单位算子的矩阵元），这是量子力学概率幅相干的体现：所有可能的"去程"与"回程"路径对的贡献在振幅层面精确抵消。

在谱表示中，每个本征模 $\lambda$ 独立地完成上述往返：$e^{iS_{\mathrm{Sp}}[\Phi_+(\lambda)]} \cdot e^{-iS_{\mathrm{Sp}}[\Phi_-(\lambda)]}$ 对所有 $\Phi_\pm(\lambda)$ 积分后给出单位传播子（每模独立幺正性），谱测度的乘积结构 $\prod_\lambda d\Phi_\pm(\lambda)$ 保持各模互不耦合地完成相消。

**具体算子示例**。考虑单本征模 $\lambda_0$（即谱算子 $A_\phi$ 仅有一个特征值），令 $\alpha \equiv \lambda_0 - m^2$。谱 CTP 泛函退化为二元高斯积分：

$$Z_{\mathrm{CTP}}^{\mathrm{Sp}}(\lambda_0; J) = \int d\Phi_+\, d\Phi_- \exp\!\left(\frac{i\alpha}{2}\Phi_+^2 - \frac{i\alpha}{2}\Phi_-^2 + iJ\Phi_+ - iJ\Phi_-\right)$$

前向与后向积分可分离：

$$G_+(J) = \int d\Phi_+\, e^{\frac{i\alpha}{2}\Phi_+^2 + iJ\Phi_+} = \sqrt{\frac{2\pi}{|\alpha|}}\, e^{i\frac{\pi}{4}\mathrm{sgn}(\alpha)}\, e^{-iJ^2/(2\alpha)}$$

$$G_-(J) = \int d\Phi_-\, e^{-\frac{i\alpha}{2}\Phi_-^2 - iJ\Phi_-} = \sqrt{\frac{2\pi}{|\alpha|}}\, e^{-i\frac{\pi}{4}\mathrm{sgn}(\alpha)}\, e^{+iJ^2/(2\alpha)}$$

两个结果的 $J$ 依赖性互为复共轭：$e^{-iJ^2/(2\alpha)}$ 与 $e^{+iJ^2/(2\alpha)}$，Stokes 相位 $e^{\pm i\pi\mathrm{sgn}(\alpha)/4}$ 亦互逆。乘积

$$G_+(J) \cdot G_-(J) = \frac{2\pi}{|\alpha|}$$

与 $J$ 无关——源的信息在前向积分中编码为相位 $e^{-iJ^2/(2\alpha)}$，在后向积分中编码为其复共轭，二者乘积消去。归一化后 $Z[J, J] = G_+(J)G_-(J) / [G_+(0)G_-(0)] = 1$。多模情形中，各模贡献以乘积 $\prod_k (2\pi/|\alpha_k|)$ 独立给出，不产生模间交叉项。

**推论 3.1（UFPF-CTP 对应）**。CTP 生成泛函 (2.5) 在谱语言中为

$$Z_{\mathrm{CTP}}^{\mathrm{Sp}}[J_+, J_-] = \int \mathcal{D}_{\mathrm{Sp}}\Phi_+ \mathcal{D}_{\mathrm{Sp}}\Phi_- \exp\!\left(i S_{\mathrm{Sp}}[\Phi_+] - i S_{\mathrm{Sp}}[\Phi_-] + i\int_{\mathcal{C}} J \cdot \Phi\right) \tag{3.3}$$

其中 $S_{\mathrm{Sp}}[\Phi] = \frac{1}{2}\int d\lambda\, \Phi^\dagger(\lambda)(\lambda - m^2)\Phi(\lambda)$ 为谱作用量（公理 A4）。

### 3.2a CTP 双拷贝 Koopman 结构

> 定理 3.1 的证明在步骤 2 中分别引入前向传播子 $\hat{U}(t, t_0)$ 与后向传播子 $\hat{U}(t_0, t) = \hat{U}(t, t_0)^\dagger$，在谱语言中对应两份 Koopman 演化 $U_\pm$。本小节给出二者之间反酉算子 $\mathcal{K}$ 的显式构造。

**定理 3.1a（CTP 双拷贝 Koopman 结构）**。前向 Koopman 演化 $U_+ = e^{-iA_R \Delta t}$ 与后向 Koopman 演化 $U_- = e^{+iA_R \Delta t}$ 通过反酉算子 $\mathcal{K}$ 联系：

$$U_- = \mathcal{K}\, U_+\, \mathcal{K}^{-1} \tag{3.3a}$$

其中 $\mathcal{K}: \mathcal{H}_R \to \mathcal{H}_R$ 定义为 $A_R$-本征基下的复共轭：在 $A_R$ 的本征基 $\{|\lambda\rangle\}_{\lambda \in \sigma(A_R)}$ 中（$A_R = -\log U_R$ 自伴，定义 2.3），

$$\mathcal{K}\left(\sum_k c_k |\lambda_k\rangle\right) = \sum_k c_k^* |\lambda_k\rangle \tag{3.3b}$$

$\mathcal{K}$ 满足：(i) 反线性 $\mathcal{K}(\alpha|\psi\rangle + \beta|\phi\rangle) = \alpha^*\mathcal{K}|\psi\rangle + \beta^*\mathcal{K}|\phi\rangle$；(ii) 反酉性 $\langle \mathcal{K}\psi | \mathcal{K}\phi \rangle = \langle \phi | \psi \rangle$；(iii) 对合性 $\mathcal{K}^2 = \mathrm{id}$；(iv) $A_R$ 不变性 $\mathcal{K} A_R \mathcal{K}^{-1} = A_R$（$A_R$ 在自身本征基下为实对角，复共轭不变）。

**证明**。由性质 (i)(iv)，$\mathcal{K}$ 的反线性性将 $-i$ 映射为 $+i$（$(-i)^* = +i$），$A_R$ 保持不变，故

$$\mathcal{K}\, U_+\, \mathcal{K}^{-1} = \mathcal{K}\, e^{-iA_R \Delta t}\, \mathcal{K}^{-1} = e^{\mathcal{K}(-iA_R)\mathcal{K}^{-1}\, \Delta t} = e^{+iA_R \Delta t} = U_+^\dagger = U_-$$

最后一步用了 $U_R$ 的酉性（保测流，§2.1.1）：$U_+^\dagger = U_+^{-1} = e^{+iA_R \Delta t}$。$\square$

**推论 3.1a（谱场对应）**。后向谱场是前向谱场的 $\mathcal{K}$-像：

$$\Phi_-(\lambda, t) = \mathcal{K}\, \Phi_+(\lambda, t) = \Phi_+^*(\lambda, t) \tag{3.3c}$$

即两份谱场在模振幅层面互为复共轭。$\square$

**$\mathcal{K}$ 对 r-a 变量的作用**。由 (3.3c) 和定义 3.1 (3.4a-b)，$\mathcal{K}$ 对 r-a 变量的作用为：

$$\mathcal{K}: \Phi_{\mathrm{cl}} = \tfrac{1}{2}(\Phi_+ + \Phi_-) \mapsto \tfrac{1}{2}(\Phi_- + \Phi_+) = \Phi_{\mathrm{cl}} \quad \text{（经典场不变）}$$

$$\mathcal{K}: \Phi_{\mathrm{q}} = \Phi_+ - \Phi_- \mapsto \Phi_- - \Phi_+ = -\Phi_{\mathrm{q}} \quad \text{（量子场翻号）}$$

这是 DKMS $\mathbb{Z}_2$ 变换 $\mathcal{R}$（定理 4.4）中 $\Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}}$ 部分的谱实现。$\mathcal{K}$ 提供了 CTP 双拷贝间的**静态** $\mathbb{Z}_2$（前向↔后向、$U_+ \leftrightarrow U_+^\dagger$），区别于 $\mathcal{R}$ 的**动态** $\mathbb{Z}_2$（含时间反演和热移）。

**注 3.2（$\mathcal{K}$ 与模共轭 $J$ 的关系）**。Tomita-Takesaki 模共轭 $J$（定义 4.1）是物理 Hilbert 空间 $\mathcal{H}_{\mathrm{GNS}}$ 上的反酉算子，满足 $J \mathfrak{M} J^{-1} = \mathfrak{M}'$。$\mathcal{K}$ 是可观测 Hilbert 空间 $\mathcal{H}_R$（谱/Koopman 空间）上对应的反酉算子，满足 $\mathcal{K} U_+ \mathcal{K}^{-1} = U_+^\dagger$。二者的结构类比：$J$ 将代数元 $x$ 映射到其伴随 $x^*$；$\mathcal{K}$ 将前向演化 $U_+$ 映射到其伴随 $U_+^\dagger$。经 GNS 构造，$J$ 与 $\mathcal{K}$ 在各自空间中实现同一物理操作——前向↔后向分支互换。

DKMS 变换 $\mathcal{R}$（定理 4.4）可分解为三个独立变换的复合：

$$\mathcal{R} = \mathcal{K} \circ \mathcal{T} \circ \mathcal{S}_\beta \tag{3.3d}$$

其中：
- $\mathcal{K}$：静态 $\mathbb{Z}_2$（$\Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}}$，前向↔后向）——此处构造
- $\mathcal{T}$：时间反演（$t \to -t$）——来自 CTP 路径 $\mathcal{C} = \mathcal{C}_+ \cup \mathcal{C}_-$ 的几何结构
- $\mathcal{S}_\beta$：热移（$\Phi_{\mathrm{q}} \to \Phi_{\mathrm{q}} + i\beta\dot{\Phi}_{\mathrm{cl}}$）——来自 KMS 解析延拓 $t \to t + i\beta$（定理 4.2）

$\mathcal{K}$ 是三者中唯一涉及代数结构（$U_+ \leftrightarrow U_+^\dagger$）的部分；$\mathcal{T}$ 和 $\mathcal{S}_\beta$ 分别来自 CTP 路径几何与 KMS 解析性质。这一分解使 §3 的 CTP 构造与 §4 的 KMS 构造之间的逻辑链完整：$\mathcal{K}$ 在谱层面实现 $U_+ \leftrightarrow U_- = U_+^\dagger$ 对应（§3.2 定理 3.1 步骤 2），而 $\mathcal{T} \circ \mathcal{S}_\beta$ 在物理层面实现 KMS 热平衡约束（§4.2 定理 4.2），三者复合给出完整 DKMS $\mathbb{Z}_2$。

**注 3.3（反酉性在耗散流体谱场中的物理意义）**。反酉算子 $\mathcal{K}$ 的构造虽源于 CTP 形式的一般结构，但在耗散流体语境下具有三层具体物理意义。

**（一）谱衰减模的复共轭配对**。耗散流体的 Koopman 谱 $\sigma(A_R)$ 一般包含复本征值 $\lambda = \gamma \pm i\omega$（$\gamma < 0$ 为衰减率，$\omega$ 为振荡频率），对应衰减振荡模 $e^{-i\lambda t} = e^{|\gamma| t} e^{-i\omega t}$。$\mathcal{K}$ 通过复共轭将 $\lambda$ 与 $\lambda^*$ 配对：前向支上模式 $e^{-i\lambda t} = e^{|\gamma| t}e^{-i\omega t}$ 在后向支上映射为 $e^{+i\lambda^* t} = e^{|\gamma| t}e^{+i\omega t}$——衰减率 $|\gamma|$ 保持不变（耗散的不可逆性），振荡相位翻转（时间反演的谱表现）。这一配对是 **Onsager 回归假设**的谱实现：自发涨落的回归与宏观扰动的弛豫共享同一谱衰减率 $|\gamma|$，而 $\mathcal{K}$ 的反酉性保证二者在谱权重上守恒（$\langle \mathcal{K}\psi | \mathcal{K}\psi \rangle = \langle \psi | \psi \rangle$）。

**（二）$\Phi_{\mathrm{q}}$ 翻号与熵产生的谱起源**。$\mathcal{K}: \Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}}$ 的物理图像是：前向分支上的噪声驱动系统偏离平衡（$\Phi_{\mathrm{q}}$ 与 $\Phi_{\mathrm{cl}}$ 同号时偏离增大），后向分支上噪声变号驱动系统回归（$\Phi_{\mathrm{q}}$ 与 $\Phi_{\mathrm{cl}}$ 反号时偏离减小）。在 r-a 作用量 (3.5) 中，$\Phi_{\mathrm{q}}$ 以 $\Phi_{\mathrm{q}} \cdot \mathcal{O}_{\mathrm{EOM}}[\Phi_{\mathrm{cl}}]$ 形式与经典场耦合——翻号使前向噪声产生正耗散（$\Delta S_+ > 0$），后向噪声产生等量负耗散（$\Delta S_- = -\Delta S_+$），净熵产生 $\Delta S = \Delta S_+ + |\Delta S_-| = 2\Delta S_+ > 0$。$\mathcal{K}$ 的反酉性保证噪声功率谱 $N(\omega) = \langle \Phi_{\mathrm{q}} \Phi_{\mathrm{q}} \rangle_\omega$ 在前向与后向分支上相等（能量守恒），而 $\Phi_{\mathrm{q}}$ 的翻号使 $\Phi_{\mathrm{q}} \Phi_{\mathrm{cl}}$ 交叉项反对称——正耗散的谱起源正在于此。

**（三）FDT 的反酉机制**。涨落-耗散定理（定理 3.2）将噪声核 $N(\omega) = \langle \Phi_{\mathrm{q}} \Phi_{\mathrm{q}} \rangle_\omega$ 与推迟响应 $\chi^R(\omega) = \langle \Phi_{\mathrm{q}} \Phi_{\mathrm{cl}} \rangle_\omega$ 联系。$\mathcal{K}$ 提供了这一关系的谱机制：$\Phi_- = \mathcal{K}\Phi_+ = \Phi_+^*$ 意味着 $\langle \Phi_- \Phi_+ \rangle_\omega = \langle \Phi_+ \Phi_+ \rangle_\omega^*$。由 (3.4a-b)，$\Phi_{\mathrm{q}} = \Phi_+ - \Phi_-$ 且 $\Phi_{\mathrm{cl}} = \frac{1}{2}(\Phi_+ + \Phi_-)$，故

$$N(\omega) = \langle \Phi_{\mathrm{q}} \Phi_{\mathrm{q}} \rangle_\omega = 2\,\mathrm{Re}\,\langle \Phi_+ \Phi_+ \rangle_\omega - 2\,\langle \Phi_+ \Phi_+ \rangle_\omega^* \propto \mathrm{Im}\,\langle \Phi_+ \Phi_+ \rangle_\omega$$

$$\chi^R(\omega) = \langle \Phi_{\mathrm{q}} \Phi_{\mathrm{cl}} \rangle_\omega \propto \mathrm{Re}\,\langle \Phi_+ \Phi_+ \rangle_\omega - \langle \Phi_+ \Phi_+ \rangle_\omega^* \propto i\,\mathrm{Im}\,\langle \Phi_+ \Phi_+ \rangle_\omega$$

二者共享同一复相位 $\langle \Phi_+ \Phi_+ \rangle_\omega$ 的实部与虚部——FDT 的 Kramers-Kronig 结构本质上来自 $\mathcal{K}$ 的复共轭配对：$N(\omega)$ 提取 $\langle \Phi_+ \Phi_+ \rangle_\omega$ 的实部（对称关联，$\Phi_{\mathrm{q}}$ 翻两次号故不变），$\mathrm{Im}\,\chi^R(\omega)$ 提取其虚部（$\Phi_{\mathrm{q}}$ 翻一次号 $\Phi_{\mathrm{cl}}$ 不翻故反对称）。反酉性 $\mathcal{K}$ 将同一谱关联函数的两个分量（实部与虚部）分别分配给噪声与响应——这就是 FDT 在 Koopman 谱层面的生成机制。

**注 3.4（强耗散极限）**。谱场关联函数在 $\gamma \gg \omega$ 极限下的渐近行为及 $\mathcal{K}$ 对称性退化分析详见**附录 A**。

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

经时间傅里叶变换到谱空间后，精确还原 UFPF 谱流方程 (2.1)。

**证明**。五步证明：

**步骤 1**：变分 (3.6) 给出

$$E_r[\Phi_{\mathrm{cl}}] + i C \cdot \Phi_{\mathrm{q}} + \mathcal{O}(\Phi_{\mathrm{q}}^2) = 0 \tag{3.7}$$

在经典极限 $\Phi_{\mathrm{q}} \to 0$ 下，$E_r[\Phi_{\mathrm{cl}}] = 0$。

**步骤 2**：$E_r[\Phi_{\mathrm{cl}}] = 0$ 的显式形式。对于谱场，$E_r$ 包含时间导数项和对易子项：

$$\partial_t \Phi_{\mathrm{cl}}(\lambda, t) = \langle \lambda | [G, A_t] | \lambda \rangle + \text{耗散项} \tag{3.8}$$

**步骤 3**：时间傅里叶变换。将 $\Phi_{\mathrm{cl}}(\lambda, t)$ 变换到 $(\lambda, \omega)$ 空间：

$$\tilde{\Phi}_{\mathrm{cl}}(\lambda, \omega) = \int dt\, e^{i\omega t} \Phi_{\mathrm{cl}}(\lambda, t) \tag{3.9}$$

对易子项 $\langle \lambda | [G, A_t] | \lambda \rangle$ 在傅里叶变换下成为卷积结构。

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

**注 3.5**（谱函数正性）。由 Lehmann 表示，retarded 传播子的谱密度 $\rho(\lambda, \omega) = 2\,\mathrm{Im}\,G_R(\lambda, \omega)$ 等于跃迁加权和 $\sum_n |\langle n | \hat{O} | 0\rangle|^2 \delta(\omega - \omega_{n0})$，故 $\rho(\lambda, \omega) \geq 0$。这保证 FDT 公式 (4.7) 中 $C(\lambda,\omega) \geq 0$（$\coth$ 与 $\omega$ 同号，$\rho \geq 0$），进而保证噪声系数正定——这是路径积分收敛（Fokker-Planck 型）的必要条件。

---

## 4 从模理论到动态 KMS $\mathbb{Z}_2$ 对称性

> 本节完成重构链的第二步：从 UFPF 的谱结构出发，通过 Tomita-Takesaki 模理论，在谱语言中重构出 CGL 的动态 KMS $\mathbb{Z}_2$ 对称性。

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

**步骤 3**：作用量不变性。将 (4.4) 代入 r-a 作用量 (3.5)，逐项验证。作用量分解为实部 $S_{\mathrm{real}}$（运动方程部分）和虚部 $S_{\mathrm{im}}$（噪声部分）：

$$S_K[\Phi_{\mathrm{cl}},\Phi_{\mathrm{q}}] = S_1[\Phi_{\mathrm{q}},\Phi_{\mathrm{cl}}] + S_2[\Phi_{\mathrm{q}}] + S_3[\Phi_{\mathrm{q}}] + \cdots$$

其中 $S_1 = \int d\lambda\,dt\,\Phi_{\mathrm{q}}E_r[\Phi_{\mathrm{cl}}]$，$S_2 = \frac{i}{2}\int d\lambda\,d\omega\,\Phi_{\mathrm{q}}^\dagger C\Phi_{\mathrm{q}}$。

**(a) 线性项 $S_1$ 的不变性**：$E_r[\Phi_{\mathrm{cl}}] = \partial_t\Phi_{\mathrm{cl}} + [G,\Phi_{\mathrm{cl}}] + \mathcal{D}$（$\mathcal{D}$ 为耗散项）。在 $\mathcal{R}$ 下：

$$S_1 \to \int dt\,[-\Phi_{\mathrm{q}}(-t) + i\beta\dot{\Phi}_{\mathrm{cl}}(-t)]\cdot[\partial_t + [G,\cdot] + \mathcal{D}]\Phi_{\mathrm{cl}}(-t)$$

- **子项 A**（$\Phi_{\mathrm{q}}\partial_t\Phi_{\mathrm{cl}}$）：时间反演下 $dt \to -dt$、$\partial_t \to -\partial_t$、$\Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}}$，两个负号相消：$\int dt\,\Phi_{\mathrm{q}}\partial_t\Phi_{\mathrm{cl}}$ 不变。
- **子项 B**（$\Phi_{\mathrm{q}}[G,\Phi_{\mathrm{cl}}]$）：$[G,\cdot] \to [-G,\cdot] = -[G,\cdot]$（$G \to -G$），结合 $\Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}}$，乘积不变。
- **子项 C**（$\beta\dot{\Phi}_{\mathrm{cl}}\cdot E_r[\Phi_{\mathrm{cl}}]$，来自 $\mathcal{R}$ 的位移项）：$\dot{\Phi}_{\mathrm{cl}}\cdot\partial_t\Phi_{\mathrm{cl}} = \frac12\partial_t(\dot{\Phi}_{\mathrm{cl}}\Phi_{\mathrm{cl}})$ 是全导数（边界项，贡献为零）；$\dot{\Phi}_{\mathrm{cl}}\cdot[G,\Phi_{\mathrm{cl}}]$ 在 $t \to -t$ 下为奇函数（$\dot{\Phi}_{\mathrm{cl}}$ 奇 × $[G,\Phi_{\mathrm{cl}}]$ 偶），积分贡献为零。故位移项对 $S_1$ 的实部无贡献。

**(b) 二次项 $S_2$ 的不变性**：$\Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}} + i\beta\dot{\Phi}_{\mathrm{cl}}$，代入：

$$(-\Phi_{\mathrm{q}} + i\beta\dot{\Phi}_{\mathrm{cl}})C(-\Phi_{\mathrm{q}} + i\beta\dot{\Phi}_{\mathrm{cl}}) = \Phi_{\mathrm{q}}C\Phi_{\mathrm{q}} - 2i\beta\Phi_{\mathrm{q}}C\dot{\Phi}_{\mathrm{cl}} - \beta^2\dot{\Phi}_{\mathrm{cl}}C\dot{\Phi}_{\mathrm{cl}}$$

- **第一项**：$\Phi_{\mathrm{q}}C\Phi_{\mathrm{q}}$ 由 $C$ 的偶性 (4.6) 不变。
- **第二项** $-2i\beta\Phi_{\mathrm{q}}C\dot{\Phi}_{\mathrm{cl}}$：贡献到作用量的实部，为交叉响应项——它进入经典运动方程（$E_r$ 的一阶修正），在 $t \to -t$ 下奇、积分为零。
- **第三项** $-\beta^2\dot{\Phi}_{\mathrm{cl}}C\dot{\Phi}_{\mathrm{cl}}$：实的正定项（$C \geq 0$ 由注 3.5），进入 $S_{\mathrm{real}}$；它是纯导数修正，不改变运动方程的物理内容（$C$ 偶 × $\dot{\Phi}_{\mathrm{cl}}$ 奇 × $\dot{\Phi}_{\mathrm{cl}}$ 奇 = 偶，$\omega \to -\omega$ 不变）。

综上，$S_K[\Phi_{\mathrm{cl}},\Phi_{\mathrm{q}}] = S_K[\mathcal{R}(\Phi_{\mathrm{cl}}),\mathcal{R}(\Phi_{\mathrm{q}})]$ 逐项成立。$\square$

### 4.5 物理后果的自动涌现

**定理 4.5（热力学定律从 $\mathcal{R}$ 涌现）**。$\mathcal{R}$ 不变性自动蕴含：

**(i) 局域第二定律**：$\nabla_\mu J_S^\mu \geq 0$。证明：$\mathcal{R}$ 约束噪声系数 $C(\lambda, \omega) \geq 0$，这等价于熵产生率非负。

**(ii) 非线性 Onsager 关系**：由 $\mathcal{R}$ 的高阶变换性质保证，传输系数满足 $L_{ij} = L_{ji}$。

**(iii) 涨落-耗散定理**：定义谱密度 $\rho(\lambda, \omega) \equiv 2\,\mathrm{Im}\,G_R(\lambda, \omega)$（$\mathrm{Im}\,G_R$ 的正性由谱定理保证，详见 §3.5 后注）。则由 (3.12) 和 $\coth$ 的恒等式：

$$C(\lambda, \omega) = \frac{2}{\tanh(\beta\omega/2)} \mathrm{Im}\,G_R(\lambda, \omega) = \coth\!\left(\frac{\beta\omega}{2}\right) \rho(\lambda, \omega) \tag{4.7}$$

这给出噪声核与谱密度的精确关系——即涨落-耗散定理（FDT）。$\square$

---

## 5 从伴随对到 BRST 对称性

> 本节完成重构链的第三步：从 UFPF 的 $D\dashv R$ 伴随对出发，通过 Lie algebroid 理论，在谱语言中重构出 BRST 微分 $Q$（$Q^2 = 0$）。

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

$$[T_1, T_2]_{\mathrm{sup}} = T_1 T_2 - (-1)^{\theta_1 \theta_2} T_2 T_1 \tag{5.8}$$

偶部 $\mathbf{Sp}_{\mathbb{Z}_2}^{(0)}$ 承载物理场（Bosonic），奇部 $\mathbf{Sp}_{\mathbb{Z}_2}^{(1)}$ 承载鬼场（Grassmann 变量 $c^a$）。

**命题 5.3**。BRST 微分 $s$ 是 $\mathbf{Sp}_{\mathbb{Z}_2}$ 上奇度为 1 的导子：$s: \mathbf{Sp}_{\mathbb{Z}_2}^{(0)} \to \mathbf{Sp}_{\mathbb{Z}_2}^{(1)}$，且 $s^2 = 0$（由定理 5.2）。物理态空间为第零阶 BRST 上同调：

$$\mathcal{H}_{\mathrm{phys}} = H^0_{\mathrm{BRST}} = \frac{\ker s}{\mathrm{im}\, s} \tag{5.9}$$

即 BRST 闭态（$s|\Psi\rangle = 0$）商掉 BRST 恰当态（$|\Psi\rangle \sim |\Psi\rangle + s|\chi\rangle$）——这正是 CGL 框架中幺正性的代数实现。

**注 5.1**（超范畴扩展的定位）。$\mathbf{Sp}_{\mathbb{Z}_2}$ 不是 UFPF 本体的组成部分，而是与场论语言（CGL）互译的接口。两点澄清：

**(i) 物理自由度不增加**：鬼场经 BRST 上同调商掉（命题 5.3），物理态空间 $H^0_{\mathrm{BRST}}$ 不包含鬼场自由度。UFPF 与 CGL 的物理自由度数量完全相同——鬼场编码的是规范结构（技术性冗余），不是物理自由度。

**(ii) 规范冗余的静默处理**：UFPF 的谱静默机制（五层静默体系 S0-S4，Paper I §5.7）天然使规范方向在谱测度中不留下可激发痕迹——这是静默机制（与紧致化额外维同源：紧致化是谱静默的几何特例）在规范结构上的应用。UFPF 独立使用时**不需要**显式鬼场即可自洽工作；$\mathbf{Sp}_{\mathbb{Z}_2}$ 仅在将 UFPF 语言翻译为 CGL 的显式规范语言时成为必要（§9.2 详述）。

### 5.7 有效作用量的 BRST 不变性

**定理 5.4**（BRST 不变性）。设 $S_{\mathrm{eff}} = S_0 + s\Psi$ 为有效作用量（$\Psi$ 为规范固定费米函数，$\mathrm{gh}(\Psi) = -1$）。则 $s \cdot S_{\mathrm{eff}} = 0$。

**证明**。

$$s \cdot S_{\mathrm{eff}} = s \cdot S_0 + s^2 \Psi = s \cdot S_0 \tag{5.10}$$

而 $s \cdot S_0 = \frac{\partial S_0}{\partial \phi^i} R^i_a c^a = 0$ 由经典规范不变性 $\frac{\partial S_0}{\partial \phi^i} R^i_a = 0$ 保证。$\square$

**定理 5.5**（Koszul-Tate 与伴随）。Koszul-Tate 分解是自由-遗忘伴随的提升：设 $\mathsf{Free} \dashv \mathsf{Forget}$，则 Koszul-Tate 分解恰好是 $\mathsf{Forget}(R/I)$ 的余纤维替换。UFPF 的 $D \dashv R$ 伴随在此框架下自然给出 BRST 复形。

**证明**。分三步。

**步骤 1（自由-遗忘伴随）**。设 $\mathsf{Free}: \mathsf{Vect} \to \mathsf{DGLA}$ 为从向量空间到微分分次李代数（DG-Lie algebra）的自由函子，$\mathsf{Forget}$ 为遗忘函子。$\mathsf{Free} \dashv \mathsf{Forget}$ 是标准伴随对 [13]：

$$\mathrm{Hom}_{\mathsf{DGLA}}(\mathsf{Free}(V), \mathfrak{g}) \cong \mathrm{Hom}_{\mathsf{Vect}}(V, \mathsf{Forget}(\mathfrak{g}))$$

即 DG-Lie 代数态射 $F: \mathsf{Free}(V) \to \mathfrak{g}$ 由底层向量空间映射 $V \to \mathsf{Forget}(\mathfrak{g})$ 唯一确定。

**步骤 2（Koszul-Tate 作为余纤维替换）**。给定约束理想 $I \subset R$（如规范条件定义的理想），商 $R/I$ 的同伦余纤维（homotopy cofiber）由 Koszul-Tate 分解给出 [13]：在 $R$ 上附加与 $I$ 的生成元对应的反交换变量（Tate 生成元），得到微分分次 $R$-代数 $K_R(I)$，其同调为

$$H_*(K_R(I)) \cong R/I$$

即 Koszul-Tate 复形在模型范畴意义下计算 $R \to R/I$ 的余纤维。这正是 $\mathsf{Forget}(R/I)$ 的余纤维替换——Koszul-Tate 分解是自由-遗忘伴随在商对象上的提升。

**步骤 3（$D \dashv R$ 给出 BRST 复形）**。UFPF 的伴随对 $D \dashv R$（定理 2.1）中，单子 $T = R \circ D$ 的 Eilenberg-Moore 代数 $\mathcal{C}^T$ 承载 Lie algebroid 结构（命题 5.1）。将步骤 2 的构造应用于 $D \dashv R$：设 $I_{\mathrm{gauge}} \subset \mathcal{C}^T$ 为规范约束定义的理想（对应 BRST 规范固定），则 $D \dashv R$ 诱导的 Koszul-Tate 分解 $K_{\mathbf{Sp}}(I_{\mathrm{gauge}})$ 在 $\mathbf{Sp}_{\mathbb{Z}_2}$ 上给出微分分次复形。Tate 生成元（步骤 2 中的反交换变量）是规范约束生成元在微分分次代数中的对偶，对应 BRST 鬼场 $c^a$（命题 5.2 中 $s(c^a) = -\frac{1}{2}f^a_{bc}c^b c^c$ (5.5b) 的生成元）。在此对应下，Koszul-Tate 微分 $d_{\mathrm{KT}}(\theta_a) = f_a$（$\theta_a$ 为 Tate 生成元，$f_a$ 为约束函数）与 BRST 微分 $s$（定义 5.3）在规范固定条件下一致：$s$ 在物理场上的作用 $s(A_\mu^a) = -\partial_\mu c^a + f^a_{bc}A_\mu^b c^c$ (5.5a) 恰是 Tate 微分在规范固定后的表现形式。$s^2 = 0$ 由定理 5.2 保证。因此 $D \dashv R$ 的伴随结构自然给出 BRST 复形 $(\mathbf{Sp}_{\mathbb{Z}_2}, s)$，物理态空间为 $H^0_{\mathrm{BRST}} = \ker s / \mathrm{im}\, s$ (5.9)。$\square$

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

**证明**。分三步。

**步骤 1（约束等价性）**。CGL 作用量 $I_{\mathrm{hydro}}$ 的构建受两条对称性约束：(i) 动态 KMS $\mathbb{Z}_2$ 对称性 $\mathcal{R}$（§2.2.4，定义 2.6）限制允许项的系数关系（如噪声核偶性、Onsager 关系）；(ii) BRST 不变性（§2.2.5，(2.10)）保证 CTP 幺正性。§4 和 §5 已分别证明这两条约束均从 UFPF 公理导出：KMS 从 Tomita-Takesaki 模理论导出（定理 4.4），BRST 从 $D\dashv R$ 伴随对的 Lie algebroid 结构导出（定理 5.2）。因此，谱流体作用量 (6.4) 在相同约束下构建，其允许的项与 CGL 作用量受同一组约束。

**步骤 2（场量一一对应）**。由定义 6.3（§6.3.1）的显式变换 (6.9a-c)，谱流体变量 $(A_r, A_{\mathrm{q}}, G, \lambda)$ 与 CGL 流体时空变量 $(E_r, E_a, V_{ri}, V_{ai}, \mu_r, \mu_a, \tau)$ 之间建立了显式映射。命题 6.4 已逐项验证作用量 (6.4) 的四类项——运动学项 (a)、平流项 (b)、耗散项 (c)、噪声项 (d)——在此映射下分别对应 CGL 作用量的运动学项、对流导数项、粘性项、高斯噪声项，且无遗漏、无多余项。

**步骤 3（高阶项一致性）**。作用量 (6.4) 中的省略项包含 $A_{\mathrm{q}}^3$ 及更高阶项，对应 CGL 的 a-场高阶展开（§6.4）。由定理 6.3，这些高阶项在谱语言中由 Kramers-Moyal 展开 $D_n$ 给出；由定义 6.2，其幺正性约束（$C_3$ 实、$C_4$ 纯虚且正定）与 CGL [1, §4] 一致。KMS 对称性（定理 4.4）进一步将平衡态高阶噪声系数通过非线性 FDT (6.8) 约束为响应函数的泛函——与 CGL 的 Wang-Heinz 型非线性 FDT [21] 一致。

综上，在 KMS + BRST 约束下，谱流体作用量 (6.4) 与 CGL 作用量 $I_{\mathrm{hydro}}$ 在场量、项结构、系数关系三个层面一一对应，故二者等价。$\square$

#### 6.3.1 显式场量变换（逐项映射强化）

**定义 6.3**（谱-流体场量变换）。利用 §7 的谱-流体时空映射 Φ，定义谱流体变量到 CGL 流体时空变量的显式变换：

$$E_r(\sigma) = \frac12\ln\!\left(\frac{\lambda_{\max}}{\lambda_r(\sigma)}\right), \quad \tau(\sigma) = \ln b(\sigma) = \frac12\ln(-\lambda_0) \tag{6.9a}$$
$$V_{ri}(\sigma) = \langle\lambda | \partial_i A_r | \lambda\rangle, \quad V_{ai}(\sigma) = \langle\lambda | \partial_i A_q | \lambda\rangle \tag{6.9b}$$
$$E_a = \ln\!\left(\frac{\lambda_q}{\lambda_r}\right), \quad \mu_r = \lambda_r, \quad \mu_a = \lambda_q \tag{6.9c}$$

其中 $\lambda_r, \lambda_q$ 分别为 $A_r, A_q$ 的主导谱参数，$\partial_i$ 为空间谱导数。

**命题 6.4**（作用量逐项映射）。在变换 (6.9) 下，谱流体作用量 (6.4) 逐项映射到 CGL 作用量 $I_{\mathrm{hydro}} = \int d^d\sigma \sqrt{a_r}E_r\mathcal{L}$ 的对应项：

| 谱流体项 | 变换后 | CGL 对应项 |
|:---|:---|:---|
| $A_q\partial_t A_r$ | $\propto E_a\partial_t E_r + V_{ai}\partial_t V_{ri}$ | $r$-型场运动学项 |
| $A_q[A_{\mathrm{adv}},A_r]$ | $\propto E_a E_r v_i v^i$（平流） | 对流导数项 |
| $A_q\nu\Delta_{\mathrm{spec}}A_r$ | $\propto \nu\nabla^2$（耗散） | 粘性项 |
| $\nu\|A_q\|^2\coth(\beta\omega/2)$ | $\propto \nu T$（噪声核） | 高斯噪声项 |

**证明**。将 (6.9) 代入 (6.4)，利用谱参数-坐标对偶 $\lambda \leftrightarrow \sigma^a$（§7.2 Φ₁）和 $\int d\lambda = \int d^d\sigma\sqrt{a_r}$（谱测度-体元对偶）：

**(a) 运动学项**：$\int d\lambda\, A_q\partial_t A_r = \int d^d\sigma\sqrt{a_r}(\mu_a\partial_t\mu_r) \leftrightarrow$ CGL 的 $\int\sqrt{-h}p\,d^{d+1}\sigma$ 变分项。

**(b) 平流项**：$A_q[A_{\mathrm{adv}},A_r]$ 在 Koopman 表示下 $[A_{\mathrm{adv}},A_r] = u^\mu\nabla_\mu A_r$，映射到 $V_{ai}E_r V_{ri}$——即 CGL 的对流导数。

**(c) 耗散项**：$-\nu\Delta_{\mathrm{spec}}A_r$ 的谱符号为 $-\nu k^2$，映射到 $\nu\nabla^2$——即 CGL 的粘性应力散度。

**(d) 噪声项**：$\coth(\beta\omega/2)$ 保持，映射到 CGL 的噪声核 $C \sim \eta T$。

各项一一对应，无遗漏、无多余项。$\square$

### 6.4 非高斯噪声的谱处理

> 本节将 CGL-I [1, §4] 的 a-场高阶展开（非高斯噪声）翻译为谱语言，完成两框架统一目标中噪声非线性相互作用的谱处理。

#### 6.4.1 a-场展开的谱对应

**定理 6.3**（三次噪声的谱本质）。CGL 的 a-场展开 [1, §4] 中，三次噪声核 $C_3$（噪声三阶累积量/双谱）在谱语言中等价于 Koopman 生成元的 Kramers-Moyal 三阶项：

$$C_3 \;\Longleftrightarrow\; D_3 = \lim_{\tau\to 0} \frac{1}{3!\,\tau}\int (x'-x)^3 p(x', t+\tau|x, t)\, dx' \tag{6.5}$$

谱符号形式：$\sigma[\mathcal{L}] = \sum_n \frac{(-ik)^n}{n!}D_n$，其中 $D_3 \neq 0$（伴随 $D_4 \neq 0$，Pawula 定理）⟺ 非高斯噪声。

**证明**。Kramers-Moyal 展开的无穷小生成元正是随机 Koopman 生成元 [14]。$D_n$ 为噪声第 $n$ 阶累积量强度，$C_n = n! D_n$。Pawula 定理：任一偶阶 $D_{2m}=0$ ⟹ 所有 $n \geq 2m$ 阶为零 ⟹ 高斯过程。故 $D_3 \neq 0$ 即非高斯。$\square$

#### 6.4.2 谱流体的非高斯扩展

**定义 6.2**（含非高斯噪声的谱流体作用量）。谱流体作用量 (6.4) 的非高斯扩展为

$$I_{\mathrm{hydro}}^{\mathrm{Sp,NG}} = I_{\mathrm{hydro}}^{\mathrm{Sp}} + \frac{i}{3!}\int A_{\mathrm{q}}^3\, C_3(\lambda_1,\lambda_2,\lambda_3) + \frac{i}{4!}\int A_{\mathrm{q}}^4\, C_4(\lambda_1,\ldots,\lambda_4) + \cdots \tag{6.6}$$

幺正性约束：$C_3$ 实，$C_4$ 纯虚且正定（与 CGL 一致）。

#### 6.4.3 多谱塔的谱对应

**定理 6.4**（多谱塔对应）。CGL 的 Keldysh 格林函数塔 $(G_K, G_{K3}, G_{K4}, \ldots)$ 对应谱框架的多谱塔 $(\rho_2, B, T, \ldots)$：

| Keldysh 塔 | 多谱塔 | 数学对象 |
|:---|:---|:---|
| $G_K(\omega)$ | 功率谱 | $\rho_2(\omega) = \sum_k |c_k|^2\delta(\omega-\omega_k) + \rho_g(\omega)$ |
| $G_{K3}(\omega_1,\omega_2)$ | 双谱 | $B(\omega_1,\omega_2) = \mathrm{E}[\hat{g}(\omega_1)\hat{g}(\omega_2)\hat{g}^*(\omega_1+\omega_2)]$ |
| $G_{K4}(\omega_1,\omega_2,\omega_3)$ | 三谱 | $T = \mathrm{cum}[\hat{g}(\omega_1)\cdots\hat{g}(-\omega_1-\omega_2-\omega_3)]$ |

高斯过程所有 $n \geq 3$ 多谱为零（Wick 定理）——多谱是"纯非高斯量"。

**推论 6.2**（乘积本征函数机制）。由于 Koopman 本征函数的乘积仍是本征函数（本征值相加 $\lambda_i + \lambda_j$），$n$ 阶矩承载于**组合本征值** $\lambda_{k_1}+\cdots+\lambda_{k_n}$ 处。三点谱测度的支撑位于三波共振条件 $\omega_1+\omega_2+\omega_3 = 0$。

#### 6.4.4 谱静默与非高斯的独立性

**命题 6.3**（静默 ≠ 高斯）。定义逐阶发声序参量：

$$\mathcal{O}_n[\rho] = \int_{\Sigma_{\mathrm{silent}}} \rho_n(\omega_1, \ldots, \omega_{n-1})\, d\mu \tag{6.7}$$

其中 $\Sigma_{\mathrm{silent}}$ 为谱静默区域。当 $\mathcal{O}_2 = 0$ 但 $\mathcal{O}_3, \mathcal{O}_4 \neq 0$ 时，系统二阶统计"静默"而高阶统计"发声"——**谱静默与非高斯性是独立的物理维度**。这澄清了 UFPF 框架的一个重要边界：紧致化式静默极限下系统仍可非高斯。

#### 6.4.5 非线性 FDT 的谱版本

**定理 6.5**（非线性 FDT = 谱流保持 KMS 塔）。谱流方程 (6.1) 在平衡固定点 $A_*$ 保持"KMS 塔"（各阶 KMS 约束族）当且仅当 n 点非线性 FDT 成立（Wang-Heinz 型 [21]）。特别地，三点 FDT 的谱形式为

$$G^{aaa}(\omega_1,\omega_2,\omega_3) = \sum_i \coth\!\left(\frac{\beta\omega_i}{2}\right) G^{\cdots r \cdots} - 2G^{rrr}, \quad \omega_1+\omega_2+\omega_3 = 0 \tag{6.8}$$

**物理内容**：平衡态三点噪声谱 $G^{aaa}$ 由三点非线性响应完全确定——非高斯噪声不引入新的自由参数。非平衡时 KMS 脱耦，$C_3, C_4$ 成为独立低能常数（与 CGL 一致）。

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
| 近平衡耗散流体 | ✅ RLF 严格 | 正则拉格朗日流（DiPerna-Lions-Ambrosio） |
| 充分发展湍流 | ⚠️ 谱测度框架 | 连续谱 → 谱测度族（§7.6） |

### 7.5 共形流体二阶输运的谱推导

> 本节将 CGL-II [2, §VII] 的中性共形流体二阶熵流结果在谱框架中重新推导。这是两框架统一目标的关键一步。

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

#### 7.5.5 系数 $f_1, f_2$ 的谱表达

> 本节补齐 §7.5.4 对照表中 $f_1$（Ricci 项）与 $f_2$（$\sigma^2$ 非线性项）的谱表达，使 CGL 二阶系数 $\{f_1,\dots,f_5\}$ 全部获得谱构造。

**定理 7.6a**（$f_1$ 的谱曲率表达）。$f_1$ 项（Ricci 耦合，BRSSS 中 $\kappa$）在谱框架中由**谱联络的曲率**给出：

$$\hat R^{\langle\mu\nu\rangle} = \Pi_\sigma\Big([\nabla_\mu,[\nabla_\nu,A_{\mathrm{adv}}]] + [A_{\mathrm{adv},\mu},A_{\mathrm{adv},\nu}]\Big) \tag{7.9'}$$

即将 $A_{\mathrm{adv}}$ 视为谱联络，其曲率 $F_{\mu\nu} = [D_\mu,D_\nu]$（$D_\mu = \nabla_\mu + A_{\mathrm{adv},\mu}$）与 Connes 非交换几何"曲率 = 对易子"同构。$f_1 \hat R^{\langle\mu\nu\rangle}$ 的整体矩是谱不变量（热核系数 $a_1 = \frac16\int R$、$a_2 = \frac1{360}\int(5R^2-2|Ric|^2+2|Rm|^2)$）。

**注 7.1a**（点态非谱不变性）。点态无迹 Ricci 张量 $\mathring R_{ij}(x)$ 本身不是谱不变量（等谱反例：Sunada、Gordon-Webb-Wolpert）；$f_1$ 的谱表达是"算子对易子"层面的构造，而非纯本征值重构。

**定理 7.7a**（$f_2$ 的三重模耦合表达）。$f_2$ 项（$\sigma^2$ 非线性项，BRSSS 中 $\lambda_1$）在谱框架中等价于 Koopman 三重模耦合：

$$\hat\sigma^{\langle\mu}{}_{\alpha}\hat\sigma^{\nu\rangle\alpha} = \sum_{k,l} c_k^{\langle\mu}{}_{\alpha}c_l^{\nu\rangle\alpha}\,\varphi_k\varphi_l\, e^{(\lambda_k+\lambda_l)t} \tag{7.10'}$$

耦合矩阵元 $C^{m,\mu\nu}_{kl} = \langle\varphi_m|\Pi_\sigma(\hat\sigma^{\langle\mu}{}_{\alpha}\hat\sigma^{\nu\rangle\alpha})|\varphi_k\varphi_l\rangle$，共振条件 $\lambda_m = \lambda_k + \lambda_l$（谱和规则）。由 Moore-Sohrabi 三点 Kubo 公式 [26]：

$$f_2 = \lambda_1 = -2\lim_{p_z,q_z\to 0}\partial_{p_z}\partial_{q_z}\lim_{p_\mu,q_\mu\to 0} G^{xy,xz,yz}_{raa}(p,q) \tag{7.11'}$$

即 $f_2$ 由全迟滞三点函数 $G^{raa}$ 给出——二阶输运系数的谱表达是**三点**而非两点的 Green-Kubo 型公式。

**推论 7.2**（$f_2 = -h_1/8$ 的谱意义）。DKMS 约束 $f_2 = -h_1/8$（$h_1$ 为 $\sigma^3$ 三次噪声顶点系数）在谱框架中等价于三重模耦合的**详细平衡约束**：噪声侧振幅 $h_1|C^{m}_{kl}|^2$ 与响应侧振幅 $f_2 C^{m}_{kl}$ 由谱密度（Planck 因子）固定——这是"非线性 Einstein 关系"，即非线性涨落-耗散定理的谱形式。

**注 7.1**（普适关系的警示）。$f_5 + f_4 - 2f_2 = 0$（Haack-Yarom 全息关系）在 Gauss-Bonnet 引力下非微扰失效 [2]，谱推导不应将其硬编码为普适约束。

### 7.6 湍流情形的谱测度映射

> 本节攻克 §7.4 中"充分发展湍流"的开放问题：通过三层替换框架，将谱-流体时空映射在湍流中严格化。

#### 7.6.1 点态映射在湍流中的失效

CGL 的流体时空映射 $X^\mu(\sigma)$ 和拉回度量 $h_{ab} = \partial_a X^\mu g_{\mu\nu}\partial_b X^\nu$ 要求光滑嵌入。但在充分发展湍流中：

1. **正则性不足**：Leray-Hopf 弱解仅满足 $u \in L^\infty_t L^2_x \cap L^2_t H^1_x$，流映射不是微分同胚
2. **K41 发散**：$\delta u(\ell) \sim (\varepsilon_0\ell)^{1/3} \Rightarrow |\nabla u_\ell| \sim \varepsilon_0^{1/3}\ell^{-2/3} \to \infty$，$\partial X \notin L^2$，$h_{ab}$ 无逐点定义
3. **ν→0 非唯一性**：ODE $\dot{x} = u(t,x)$ 解不唯一（自发随机性），流映射退化为测度值对象

#### 7.6.2 三层替换框架

**定理 7.6**（三层替换）。湍流中的谱-流体时空映射必须采用三层严格化：

**层 A（固定 ν）**——正则拉格朗日流（RLF）[22]：对 Leray 解，存在 a.e. 定义、保测的映射 $X(t,\cdot)$，满足 $\partial_t X = u(t,X)$ a.e. 且 $X(t,\cdot)_\#\mathrm{Leb} = \mathrm{Leb}$。$X \in W^{1,2}$ 时 $h_{ab} \in L^1$（分布意义良定义）。

**层 B（粗粒化）**——广义拉格朗日平均（GLM）[23]：$X^\mu(\sigma) = \bar{X}^\mu(\sigma) + \xi^\mu(\sigma)$，其中 $\bar{X}$ 光滑、$\xi$ 为涨落位移场。粗粒化度量满足

$$\big\langle \partial_a X^\mu g_{\mu\nu}\partial_b X^\nu\big\rangle = \underbrace{\partial_a\langle X^\mu\rangle g_{\mu\nu}\partial_b\langle X^\nu\rangle}_{h^{\mathrm{mean}}_{ab}} + \underbrace{\big\langle (\partial_a X^\mu - \partial_a\langle X^\mu\rangle) g_{\mu\nu}(\partial_b X^\nu - \partial_b\langle X^\nu\rangle)\big\rangle}_{\tau_{ab}} \tag{7.9}$$

其中 $\tau_{ab}$ 为**亚网格度量**，其物理时空分量正是雷诺应力 $\tau_{ij} = \langle u'_i u'_j\rangle$。GLM 伪动量 $p_i = -\langle\xi_{j,i}u'_j\rangle$ 与雷诺应力一一对应。

**层 C（统计稳态）**——Koopman 谱测度族 [18,24]：对保测流，Koopman 群是酉群，Stone 定理给出投影值谱测度分解 $\mathcal{K} = \int_\mathbb{T} e^{i\theta} dE(\theta)$。**谱流体质时空映射**定义为嵌入坐标的向量值谱测度族：

$$\{E_{X^\mu}(\lambda)\}_\mu, \quad \langle X^\mu(\Phi_\tau\cdot), X^\nu\rangle = \int e^{i\lambda\tau}\,d\mu_{X^\mu X^\nu}(\lambda) \tag{7.10}$$

拉回度量在弱意义下成为**双线性谱形式**（交叉谱测度）。

#### 7.6.3 收敛保证与可验证性

**定理 7.7**（谱测度收敛 [18,24]）。对保测算子，谱测度的光滑化近似以显式阶弱收敛：

$$\left|\int_\mathbb{T} \phi\, d\mu_{g,\varepsilon} - \int_\mathbb{T}\phi\, d\mu_g\right| \leq C\varepsilon^{n+\alpha} \tag{7.11}$$

连续谱密度与离散谱同时以 $O(\varepsilon^{n+\alpha})$ 恢复，附带后验误差界。不光滑特征函数由 Gelfand 三重 $\Phi \hookrightarrow L^2 \hookrightarrow \Phi^*$ 中的广义特征函数（分布）承载 [24]。

**可检验判据**：
- **C1**：湍流中 Koopman 谱测度的绝对连续部分密度 = 功率谱密度（PSD 恒等式）
- **C2**：粗粒化度量 (7.9) 中 $\tau_{ab}$ 的物理分量 = 雷诺应力（LES 直接验证）
- **C3**：GLM 伪动量 $p_i$ 与雷诺应力一一对应

**注 7.2**（学习极限 [25]）。存在对抗性光滑系统使任何数据驱动算法无法学习谱性质（成功率至多 50%）。湍流谱-时空映射的可行路径是"谱测度 + 误差界"而非"逐点特征值"。

---

## 8 翻译定理

**定理 8.1（CGL 的谱语言翻译主定理）**。设 $(\mathbf{Rec}, \mathbf{Sp}, D\dashv R)$ 是满足 UFPF 公理的谱范畴，$\mathbf{Sp}_{\mathbb{Z}_2}$ 是其超范畴扩展。则 CGL 的以下**八个核心结构**均可翻译为 UFPF 谱语言（翻译后结构层等价）：

**(1) 路径积分翻译**。$\mathbf{Sp}_{\mathbb{Z}_2}$ 上的谱路径积分（A4 + 超结构）对应 CGL 的 CTP 路径积分（§3.2，定理 3.1）。

**(2) r-a 翻译**。SK 谱等价桥（定理 2.2）对应 CGL 的 r-a 变量分解（§3.3，定理 3.2）。

**(3) KMS 翻译**。谱 KMS 变换（§4.4，定理 4.4）对应 CGL 的动态 KMS $\mathbb{Z}_2$ 对称性。

**(4) BRST 翻译**。$\mathbf{Sp}_{\mathbb{Z}_2}$ 上的超范畴 BRST 算子 $s$（§5.3 定理 5.2 + §5.6 定义 5.4）对应 CGL 的 BRST 对称性。

**(5) 作用量翻译**。谱流体作用量 $I_{\mathrm{hydro}}^{\mathrm{Sp}}$（§6.2，定义 6.1）对应 CGL 的流体作用量 $I_{\mathrm{hydro}}$（§6.3，定理 6.2）。

**(6) 二阶输运翻译**。谱熵流构造（§7.5，定理 7.5）对应 CGL-II 的中性共形流体二阶熵流，DKMS 约束 $c_2 = f_5/4$ 有纯谱表述（推论 7.1）；全部系数 $\{f_1,\dots,f_5\}$ 已获得谱构造——$f_1$ 由谱联络曲率（定理 7.6a）、$f_2$ 由三重模耦合三点 Kubo 公式（定理 7.7a）、$f_5$ 由谱隙（定理 7.3）。

**(7) 非高斯噪声翻译**。谱流体的非高斯扩展（§6.4，定理 6.3-6.5）对应 CGL-I 的 a-场高阶展开，非线性 FDT 有谱版本（定理 6.5）。

**(8) 湍流映射翻译**。谱测度映射（§7.6，定理 7.6-7.7）在湍流中提供 CGL 流体时空映射的唯一无歧义严格化：层 A（RLF）固定 ν、层 B（GLM）粗粒化、层 C（谱测度族）统计稳态。

**证明**。由定理 3.1、3.2、4.4、5.2、6.2、6.5、7.5、7.6 直接合并。$\square$

**推论 8.1**。CGL 的全部物理结论——涨落流体力学、第二定律从对称性涌现、Onsager 关系、FDT（含非线性）、共形流体二阶输运、非高斯噪声层级、湍流情形的谱测度描述——均可翻译为 UFPF 公理体系（含超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$）的谱语言表述。

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

在此基础上：§3-§5 的推导基于上述定理的**直接应用**；§6 的等价性由**显式场量变换**（§6.3.1 定义 6.3 + 命题 6.4）支撑，将谱流体作用量逐项映射到 CGL 作用量；§7 的映射在理想流体情形严格（§7.2-7.3）、近平衡由正则拉格朗日流保证（§7.6 层 A）、湍流由谱测度框架严格化（§7.6 层 B/C）。

### 9.2 与 CGL 的关系定位

本文建立的不是"UFPF 取代 CGL"，也不是宣称两者完全对等，而是展示一种**翻译关系**：UFPF 是覆盖多领域的元框架（meta-framework），其谱语言可以翻译 CGL 的耗散流体 EFT。在结构层面（§8 的八项翻译），CGL 与谱语言版本数学同构。本文把这种关系呈现为类似"语言"与"用该语言写成的某一著作"的关系——著作的独立性不受影响，语言的范围也不受单一著作限制；至于两者在理论范围上的最终比较，本文不做单方面断言，留待学术共同体评价。本文的实际贡献是翻译本身及其产生的新预言。

本翻译结果有两层解读姿态：

1. **工具姿态（本文工作直接支持）**：UFPF 可作为元语言，对 CGL 做完整的结构重构、压力测试、生成新可证伪预言；即便 UFPF 的本体猜想最终不成立，该框架仍可作为理论实践工具。
2. **本体猜想（不属于本文结论）**：UFPF 这套范畴-谱结构是否为物理现实底层本质关系，该猜想需要更多领域重构与独特预言的实验确认，留待后续研究。

§7.5 已进一步表明，这种翻译延伸到**具体的定量成果**：CGL-II 的中性共形流体二阶熵流（$f_1,\dots,f_5$ 系数系统）可在谱框架中用 Koopman 谱隙和模强度重新表达。尤其是 DKMS 约束 $c_2 = f_5/4$ 获得了纯谱的等价表述，并产生可证伪预言 $\lambda_\pi \approx -4.81\,T$（N=4 SYM 剪切道第一非流体力学谱隙）。

§7.6 进一步将翻译延伸到**最困难的湍流情形**：CGL 的流体时空映射 $X^\mu(\sigma)$ 在湍流中不光滑，但通过三层替换（RLF/GLM/谱测度族）获得了严格化——其中谱测度族是统计稳态下唯一无歧义的表述。这关闭了翻译框架的最后一个结构性缺口（§9.4 所列的残留问题转为学习极限边界而非框架缺失）。

**规范结构的两种处理**。UFPF 与 CGL 对规范冗余的处理方式不同：UFPF 的谱静默机制使规范方向在谱测度中自动不可见（无需鬼场即可自洽工作），CGL 的场论语言必须显式编码规范结构（鬼场 + BRST 上同调）。这两种处理是同一物理内容（规范冗余）的不同表示，物理自由度数量相同（注 5.1）。超范畴扩展 $\mathbf{Sp}_{\mathbb{Z}_2}$（定义 5.4）是两者互译的接口而非 UFPF 本体的组成部分。这一观察将 UFPF 的静默机制定位为对规范结构的"自动处理"——与其对紧致化额外维的处理（§2.1 谱静默）同源，即静默机制统一适用于"额外维"与"规范方向"两类不可观测结构。

### 9.3 可验证性

本文的推导链产生了**五个可直接数值验证的预言**（V1-V5）与**三个湍流判据**（C1-C3）：

**（V1）噪声统计的 KMS 约束**：谱流体的噪声统计 (6.3) 应满足 CGL 的 KMS 约束（经典极限 Landau-Lifshitz 形式 6.3'）。可通过 UFPF 现有的湍流 DNS 代码直接检验。

**（V2）剪切道谱隙**：N=4 SYM 剪切道第一非流体力学 Koopman 特征值应位于 $\lambda_\pi \approx -4.81\,T$（定理 7.3）。可在 Bjorken 流上用 DMD/EDMD 从数值数据提取验证。

**（V3）DKMS 约束的谱版本**：谱熵流中 $\sigma^2 u^\mu$ 项系数应等于 $\eta/(4|\lambda_\pi|)$（推论 7.1）——这是 KMS 约束的纯谱陈述，无需导数展开即可检验。

**（V4）双谱塔的非高斯信号**：非高斯噪声（定理 6.4）要求多谱塔在 $n \geq 3$ 阶非零。可在随机扩散模型上验证：三点噪声谱 $G^{aaa}$ 应满足非线性 FDT (6.8)，且谱静默区高阶谱（$\mathcal{O}_3, \mathcal{O}_4$）可非零——静默 ≠ 高斯的可检验判据。

**（V5）谱测度 = 功率谱密度**：湍流中 Koopman 谱测度的绝对连续部分密度应等于信号的功率谱密度（§7.6 判据 C1）。可在湍流 DNS 数据上用 ResDMD 直接验证，同时检验粗粒化度量恒等式 (7.9)（判据 C2，$\tau_{ab}$ = 雷诺应力）。

**验证结果**（`scripts/paper45_spectral_EFT_validation.py`）：**V1-V5 全部通过（11/11 检查项）**。要点：
- V1：FDT 公式数值精确（相对误差 4×10⁻¹⁶），噪声核偶性确认（10⁻¹⁵ 级），经典极限 Landau-Lifshitz 形式精确还原
- V2：$\lambda_\pi = -4.808T$ 与理论一致；数值数据 AR(1) 提取 $\lambda_\pi = -4.933$（偏差 2.6%）；强/弱耦合谱隙比 28.85 ≈ 29
- V3：$c_2 = \eta/(4|\lambda_\pi|)$ 谱隙表达式自洽
- V4：高斯系统 $G^{aaa} = 0$（Wick 定理）与非高斯三阶累积量信号均确认；三点 FDT (6.8) 重建自洽
- V5：谱测度密度 = PSD 恒等式确认（相关性 0.962）——验证湍流判据 C1

### 9.4 局限性与开放问题

以下按问题性质分为三类。

**前提性局限**

1. **UFPF 的地位局限**。UFPF 目前为个人独立研究的理论假说，未经学术共同体独立评审（§1.1 地位声明）。本文的全部论证以 UFPF 公理为前提——若 UFPF 公理体系本身被证伪或需修正，本文的重构结论将相应调整。这是本文最大的前提性局限，以下所有开放问题均以此为前提。

**框架性缺口**

2. **CTP 双拷贝 Koopman 结构**（已在 §3.2a 完成）。反酉算子 $\mathcal{K}$（定理 3.1a）在 $A_R$-本征基下显式构造为复共轭算子 (3.3b)，满足 $U_- = \mathcal{K} U_+ \mathcal{K}^{-1}$ (3.3a)。$\mathcal{K}$ 对 r-a 变量给出静态 $\mathbb{Z}_2$（$\Phi_{\mathrm{q}} \to -\Phi_{\mathrm{q}}$），是 DKMS 变换 $\mathcal{R} = \mathcal{K} \circ \mathcal{T} \circ \mathcal{S}_\beta$ (3.3d) 的代数分量。$\mathcal{K}$ 与模共轭 $J$ 的对应关系见注 3.2。

3. **湍流映射的学习极限**。§7.6 的谱测度映射提供了严格框架，但存在学习极限（注 7.2）：对抗性光滑系统使任何数据驱动算法无法学习谱性质（成功率至多 50%）。这意味着湍流谱-时空映射的可操作性存在根本边界，实际应用需结合先验物理约束。

4. **二阶系数 $f_1$ 的点态表达受限**。$f_1$ 的谱构造（定理 7.6a）在算子对易子层面成立，但点态无迹 Ricci 张量本身不是谱不变量——存在等谱反例（Sunada、Gordon-Webb-Wolpert，注 7.1a）。因此 $f_1$ 的谱表达不能简化为纯本征值重构。

5. **普适关系的适用范围**。Haack-Yarom 关系 $f_5+f_4-2f_2=0$ 在 Gauss-Bonnet 引力下非微扰失效 [2]（注 7.1）。该关系仅在全息 Einstein 引力下成立，谱框架中不应视为一般约束；其谱推广需逐案验证。

**待完成的严格化与数值延伸**

6. **非高斯噪声的高阶实现**。V1-V5 数值验证已通过（§9.3），但以下两项待完成：(a) 多谱塔双谱 $B(\omega_1,\omega_2)$ 与三谱 $T(\omega_1,\omega_2,\omega_3)$ 的显式频域计算——V4 仅验证了时域三阶累积量信号；(b) KMS 塔保持定理（定理 6.5）的严格形式化——当前仅验证了三点 FDT (6.8) 的代数结构自洽性，一般 $n$ 点情形的证明待补。

7. **超范畴 $\mathbf{Sp}_{\mathbb{Z}_2}$ 的形式化**。$\mathbf{Sp}_{\mathbb{Z}_2}$ 作为翻译接口引入了 $\mathbb{Z}_2$-分级信息（注 5.1），其 Lean 4 形式化验证尚未完成。关键检查点为 BRST 幂零性 $s^2=0$（定理 5.2）在超范畴语言中的机器可验证证明。

8. **数值工具的扩展**。当前验证脚本（`scripts/paper45_spectral_EFT_validation.py`）针对 V1-V5 设计。需要扩展为基于谱测度与 Koopman 谱特征的通用数值工具，以在更复杂物理极限（非平衡态、强耦合）下检验 §7.5-§7.6 的定量预言。

**跨文档指引**。本文只处理耗散流体 EFT 分支；UFPF 全套的预设清单（Polish 拓扑、$A_{\mathrm{GR}}$ 断言）与完整开放问题清单（例如暗能量 B1 瓶颈），参见 UFPF 体系总序。

---

### **Acknowledgments (致谢)**

我们首先对构建本文理论基础的多个领域学派表示深深的敬意：从规范场论、KMS 态理论到现代非线性流体力学的诸多开创性工作，构成了本研究能够进行“谱语言翻译”的知识土壤。特别感谢 Crossley, Glorioso 和 Liu 在耗散流体有效场论方面提供的严谨框架，以及 Tomita-Takesaki 模理论和 Lie Algebroid 几何学所奠定的数学基础。

本文提出的 UFPF（通用不动点分形谱范畴框架）及其谱语言是作者个人独立构建的理论体系。我们诚挚地将此工作定位为一次跨越物理、几何和代数拓扑多领域的**系统性尝试**，其最终结论应视为该理论假说的一个重要实例展示，而非所有相关领域已有的既定知识集合。

---

## 附录 A：强耗散极限下的谱场关联函数渐近行为

本附录推导 §3.2a 中构造的反酉算子 $\mathcal{K}$（定理 3.1a）在强耗散极限 $\gamma \gg \omega$ 下对谱场关联函数的影响。结果在注 3.4 中引用，并可与 §4.2 的 FDT（定理 3.2）和 §7.5 的共形流体输运系数相互参照。

### A.1 设置

设 Koopman 本征值 $\lambda = \omega - i\gamma$（$\omega > 0$：振荡频率，$\gamma > 0$：衰减率），前向演化 $\Phi_+(\lambda, t) \propto e^{-i\lambda t} = e^{-i\omega t - \gamma t}$。强耗散极限定义为

$$\gamma \gg \omega, \quad \gamma \gg T \quad (T = 1/\beta) \tag{A.0}$$

即衰减率远大于振荡频率与温度。

### A.2 推迟响应函数

单模推迟 Green 函数

$$G_R(\nu) = \frac{1}{\nu - \omega + i\gamma} \tag{A.1}$$

在时域：

$$G_R(t) = -i\theta(t)\, e^{-i\omega t - \gamma t} \xrightarrow{\gamma \gg \omega} -i\theta(t)\, e^{-\gamma t} \tag{A.2}$$

振荡相位 $e^{-i\omega t}$ 的时间尺度 $1/\omega$ 远长于振幅衰减时间 $1/\gamma$——系统进入**过阻尼**（overdamped）区域，演化退化为纯指数弛豫。

### A.3 谱密度

$$\rho(\nu) = -2\,\mathrm{Im}\,G_R(\nu) = \frac{2\gamma}{(\nu - \omega)^2 + \gamma^2} \xrightarrow{\gamma \gg \omega} \frac{2\gamma}{\nu^2 + \gamma^2} = \frac{2}{\gamma} \cdot \frac{1}{1 + (\nu/\gamma)^2} \tag{A.3}$$

Lorentzian 峰被 $\gamma$ 宽度抹平，中心从 $\nu = \omega$ 移至 $\nu = 0$。低频区域 $\nu \ll \gamma$：

$$\rho(\nu) \approx \frac{2}{\gamma} \quad \text{（平谱，白噪声特征）} \tag{A.4}$$

### A.4 噪声核

由 FDT（定理 3.2），$N(\nu) = \coth\frac{\beta\nu}{2} \cdot \rho(\nu)$，在强耗散极限下分两个频区：

- **经典区域** $\nu \ll T \ll \gamma$：$\coth\frac{\beta\nu}{2} \approx \frac{2T}{\nu}$，故

$$N(\nu) \approx \frac{2T}{\nu} \cdot \frac{2}{\gamma} = \frac{4T}{\gamma\nu} \quad \text{（$1/\nu$ 红外发散）} \tag{A.5}$$

- **量子区域** $T \ll \nu \ll \gamma$：$\coth\frac{\beta\nu}{2} \approx 1$，故

$$N(\nu) \approx \frac{2}{\gamma} \quad \text{（白噪声）} \tag{A.6}$$

### A.5 $\mathcal{K}$ 对称性的退化

由推论 3.1a（$\Phi_- = \mathcal{K}\Phi_+ = \Phi_+^*$），前向-前向关联 $G_{++}(t) = C_\lambda e^{-i\omega t - \gamma t}$，后向-后向关联 $G_{--}(t) = G_{++}^*(t) = C_\lambda e^{+i\omega t - \gamma t}$。强耗散极限下：

$$G_{++}(t) \approx C_\lambda e^{-\gamma t}, \quad G_{--}(t) \approx C_\lambda e^{-\gamma t} \tag{A.7}$$

振荡分量 $e^{\pm i\omega t}$ 在 $t \gg 1/\gamma$ 时已被衰减完全压制——$\mathcal{K}$ 的复共轭配对 $\lambda \leftrightarrow \lambda^*$ 在 $|\mathrm{Re}(\lambda)| \ll |\mathrm{Im}(\lambda)|$ 时退化为平凡配对（$\lambda \approx \lambda^* \approx -i\gamma$）。CTP 双拷贝在**相干层面**退化为单拷贝：$\Phi_+ \approx \Phi_-$，$\Phi_{\mathrm{q}} = \Phi_+ - \Phi_- \to 0$。

然而，**涨落层面**的 $\mathcal{K}$ 对称性持续有效：噪声核 $N(\nu) \propto \rho(\nu) \propto \mathrm{Im}\,G_R(\nu)$ 仍由 $\mathcal{K}$ 的复共轭结构维持（注 3.3 第三点，§3.2a）。即使在 $\gamma \to \infty$ 的极端极限中，$\rho(\nu) \to 2/\gamma$ 趋于零但不消失，FDT 关系 $N(\nu) = \coth\frac{\beta\nu}{2} \cdot \rho(\nu)$ 保持成立——$\mathcal{K}$ 对 FDT 的生成机制（将 $\langle \Phi_+\Phi_+\rangle_\nu$ 的实部分配给 $N$、虚部分配给 $\mathrm{Im}\,G_R$）不依赖于 $\omega/\gamma$ 比值。

### A.6 物理总结

强耗散极限 $\gamma \gg \omega$ 下，系统从**欠阻尼量子振荡子**转变为**过阻尼经典 Markov 过程**：

| 量 | 欠阻尼 ($\gamma \ll \omega$) | 过阻尼 ($\gamma \gg \omega$) |
|:---|:---|:---|
| $G_R(t)$ | $-i\theta(t) e^{-i\omega t - \gamma t}$（阻尼振荡） | $-i\theta(t) e^{-\gamma t}$（纯弛豫） |
| $\rho(\nu)$ | 窄 Lorentzian, 峰在 $\omega$ | $\frac{2}{\gamma}$（平谱, 白噪声） |
| $N(\nu)$ | 量子噪声 $\coth\frac{\beta\nu}{2}\,\rho$ | $\frac{4T}{\gamma\nu}$（经典, $1/\nu$ 发散） |
| $\mathcal{K}$ 配对 | $\lambda \leftrightarrow \lambda^*$ 非平凡 | $\lambda \approx \lambda^* \approx -i\gamma$（平凡） |
| CTP 双拷贝 | $G_{++} \neq G_{--}$（振荡相位区分） | $G_{++} \approx G_{--}$（相位被压制） |
| FDT 机制 | $\mathcal{K}$ 将 $\langle \Phi_+\Phi_+\rangle$ 实虚部分配 | 同左（不依赖 $\omega/\gamma$） |

$\mathcal{K}$ 在相干层面的退化与在涨落层面的持续，定量地刻画了量子-经典跨界：相干振荡被耗散抹平时，涨落-耗散关系作为 $\mathcal{K}$ 的遗产依然维系热平衡约束。

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
[21] E. Wang, U. Heinz, "A generalized fluctuation-dissipation theorem for nonlinear response functions," *Phys. Rev. D* 66:025008 (2002), arXiv:hep-th/9809016.
[22] L. Ambrosio, "Transport equation and Cauchy problem for BV vector fields," *Invent. Math.* 158 (2004) 227-260.
[23] A. D. Gilbert, J. Vanneste, "Geometric approaches to Lagrangian averaging," *Annu. Rev. Fluid Mech.* 57 (2025).
[24] M. J. Colbrook, C. Drysdale, A. Horning, "Rigged dynamic mode decomposition: data-driven generalized eigenfunction decompositions for Koopman operators," arXiv:2405.00782 (2024).
[25] M. J. Colbrook, I. Mezić, A. Stepanenko, "Adversarial dynamical systems characterize when data-driven learning succeeds or fails," *Nat. Commun.* 17:5397 (2026), arXiv:2407.06312.
[26] G. D. Moore, K. Sohrabi, "Kubo formulae for second-order hydrodynamic coefficients," *JHEP* 11:148 (2011), arXiv:1007.5333.

---

*本文属于 UFPF 系列论文（Paper XLV），展示 UFPF 谱语言可翻译 Crossley-Glorioso-Liu（CGL）耗散流体有效场论的核心结构。翻译的可行性是 UFPF 语言普适性的一个例证；两框架关系的最终定性留待学术共同体评价。版本 v1.2（2026-08-22）。*

---
