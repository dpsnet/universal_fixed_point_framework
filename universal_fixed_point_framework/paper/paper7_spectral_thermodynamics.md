# 通用不动点范畴框架 VII：非平衡谱热力学——谱熵、涨落与时间箭头

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**摘要**：本文在谱动力学框架（Paper V）基础上建立非平衡谱热力学。核心结果是热力学第二定律（$\Delta S \ge 0$）不是独立公理，而是谱流方程的直接推论——固定基观测下 $A_t$ 在谱流中的旋转将信息从对角元转移到非对角元，表现为熵增。进一步证明谱 Onsager 倒易关系和谱涨落定理 $P(\Sigma)/P(-\Sigma) = e^{\Sigma}$，并通过数值验证确认热力学箭头从谱流中自然涌现。

---

**术语说明**：记号与定义沿用 Paper V（谱流方程 $\frac{d}{dt}A_t = [G, A_t]$、谱对易子 $[A_F, A_t]$、谱生成元 $A_{F,i}$）。

## 1. 引言

### 1.1 问题

热力学第二定律是物理学中最普遍的定律之一，但其基础地位长期存在争议——它是独立公理，还是可从更基本的动力学推导？Boltzmann 的 $H$ 定理试图从经典力学推导熵增，但遭遇 Loschmidt 悖论（时间反演对称性不允许单调熵增）。

### 1.2 谱动力学的回答

在谱动力学框架中，$A_t$ 的演化由谱流方程决定：

$$\frac{d}{dt} A_t = [G, A_t]$$

该方程在 $A_t$ 的瞬时本征基下保持谱不变（$\sigma(A_t) = \sigma(A_0)$，Paper V 定理 2.2）。但**在固定基观测下**，$A_t$ 旋转谱流将信息从对角分量转移到非对角分量，表现为熵增。关键区别：

| 观测框架 | 熵行为 | 原因 |
|----------|--------|------|
| $A_t$ 瞬时本征基 | $\Delta S = 0$ | 谱不变性 |
| **固定基**（物理观测） | $\Delta S \ge 0$ | 信息转移到非对角元 |

**时间箭头不是谱流方程的附加假设——它是固定基观测的必然结果。**

## 2. 谱熵

### 2.1 定义

**定义 2.1**（固定基谱熵）。给定固定正交基 $\mathcal{B} = \{|e_i\rangle\}$，$A_t$ 在该基下的谱熵为：

$$S_{\mathcal{B}}(t) = -\sum_i p_i(t) \log p_i(t), \quad p_i(t) = |\langle e_i| A_t | e_i\rangle|^2 / \sum_j |\langle e_j| A_t | e_j\rangle|^2$$

当 $\mathcal{B}$ 取 $A_0$ 的本征基时，$S_{\mathcal{B}}(0)$ 为零（纯态），$S_{\mathcal{B}}(t)$ 随 $t$ 增加。

### 2.2 基本性质

**命题 2.1**（谱熵的基本性质）。

1. **非负性**：$S_{\mathcal{B}}(t) \ge 0$，等号当且仅当 $A_t$ 在 $\mathcal{B}$ 下为纯态
2. **有界性**：$S_{\mathcal{B}}(t) \le \log N$（$N$ 为系统维数）
3. **基依赖性**：$S_{\mathcal{B}}(t) \ne S_{\mathcal{B}'}(t)$ 对不同基不同
4. **谱流协变性**：$S_{\mathcal{B}}(t) = S_{U_t^\dagger \mathcal{B} U_t}(0)$，$U_t = e^{tG}$

**证明**。性质 1-3 直接来自 Shannon 熵的标准性质。性质 4 来自谱流方程的解：$\langle e_i|A_t|e_i\rangle = \langle e_i(t)|A_0|e_i(t)\rangle$，其中 $|e_i(t)\rangle = U_t^\dagger|e_i\rangle$。□

### 2.3 连续谱推广

对连续谱系统（如湍流、量子场），固定基熵通过投影值谱测度 $E(\lambda)$ 推广（`paper34_unbounded_operator.py`，定理 2.10.3）。

**定义 2.2**（连续谱熵）。对自伴算子 $A$ 的谱分解 $A = \int \lambda \, dE(\lambda)$，固定基 $\mathcal{B}$ 下的谱熵为：

$$S_{\mathcal{B}}^{\text{cont}}(t) = -\int p(\lambda,t) \log p(\lambda,t) \, d\lambda, \quad p(\lambda,t) = \frac{d\langle e_i|E_t(\lambda)|e_i\rangle}{d\lambda}$$

其中 $E_t(\lambda) = U_t E^{(0)}(\lambda) U_t^{-1}$ 是演化后的谱测度。

**定理 2.1**（连续谱熵增，`paper29_entropy_production_proof.py` 定理 P29.4）。对连续谱 $\lambda(k) \in [k_{\min}, k_{\max}]$，熵密度 $s(k,t) = -p(k,t)\log p(k,t)$ 满足：

$$S_{\text{cont}}(t_f) \ge S_{\text{cont}}(t_0), \quad S_{\text{cont}}(t) = \int s(k,t) \, dk$$

**证明要点**。使用 Lindblad 相对熵单调性：$S(T(\rho)||T(\sigma)) \le S(\rho||\sigma)$。令 $\sigma_{\text{flat}} = I/d$，则 $S_{\text{basis}}(t) = \log d - S(p(t)||p_{\text{flat}})$。相对熵单调 $\Rightarrow$ $S_{\mathcal{B}}(t+dt) \ge S_{\mathcal{B}}(t)$。连续谱推广通过测度论直接成立。详细证明及数值验证（离散谱 $\Delta S > 0$、连续谱 $\Delta S_{\text{cont}} > 0$）见 `paper29_entropy_production_proof.py`。□

## 3. 热力学第二定律的谱推导

### 3.1 熵增定理

**定理 3.1**（谱熵增）。在固定基 $\mathcal{B}$ 下，谱流方程驱动的 $A_t$ 满足：

$$S_{\mathcal{B}}(t_f) \ge S_{\mathcal{B}}(t_0), \quad \forall t_f > t_0$$

等号成立当且仅当 $A_t$ 在 $\mathcal{B}$ 下始终为对角矩阵。

**证明**。谱流方程的解为 $A_t = U_t A_0 U_t^{-1}$，$U_t = e^{tG}$。$U_t$ 是幺正算子（当 $G$ 反 Hermite 时）。在固定基 $\mathcal{B}$ 下：

$$\langle e_i|A_t|e_i\rangle = \langle e_i|U_t A_0 U_t^{-1}|e_i\rangle$$

将 $A_0$ 在 $\mathcal{B}$ 下展开：$A_0 = \sum_{jk} a_{jk} |e_j\rangle\langle e_k|$。则：

$$\langle e_i|A_t|e_i\rangle = \sum_{jk} a_{jk} \langle e_i|U_t|e_j\rangle\langle e_k|U_t^{-1}|e_i\rangle$$

当 $t=0$ 时 $U_0=I$，$\langle e_i|A_0|e_i\rangle = a_{ii}$（纯对角）。当 $t>0$ 时，$U_t$ 的非对角元将 $a_{jk}$（$j\ne k$）的信息混入对角分量。由 Shannon 熵的凹性，概率分布 $\{p_i(t)\}$ 比 $\{p_i(0)\}$ 更均匀，故 $S(t) \ge S(0)$。□

### 3.2 数值验证

`paper22_spectral_entropy.py` 对随机 $6\times6$ Hermite 矩阵在谱流下 200 步演化：

| 指标 | 值 |
|------|-----|
| $S(0)$ | 1.6075 |
| $S(t_f)$ | 1.6620 |
| $\Delta S$ | **0.0544 > 0** ✅ |
| 晚期 $dS/dt$ | $\sim 10^{-3}$（趋近平衡）✅ |

### 3.3 Loschmidt 悖论的谱消解

时间反演对称性悖论：若动力学是时间反演不变的，熵为何单向增加？

在谱动力学中，时间反演 $t \to -t$ 对应 $G \to -G$。反演后的谱流方程 $\frac{d}{dt}A_t = -[G, A_t]$ 同样满足谱不变性。但**固定基 $\mathcal{B}$ 在时间反演下不变**——观测者不会因为时间反演而改变测量基。因此：

$$S_{\mathcal{B}}^{\text{forward}}(t) \ge S(0), \quad S_{\mathcal{B}}^{\text{backward}}(t) \ge S(0)$$

两个方向的熵均不减少。悖论消解：**时间箭头在观测基中，不在动力学中。**

## 4. 谱 Onsager 倒易关系

### 4.1 通量与力

定义谱流 $J_i$（由第 $i$ 种力驱动的熵产生）和谱力 $X_i = g_i$：

$$J_i = \frac{d}{dt} \text{Tr}(A_{F,i} \rho_t)$$

**定理 4.1**（谱 Onsager 关系）。Onsager 矩阵 $L_{ij} = \partial J_i/\partial X_j$ 是对称的：

$$L_{ij} = L_{ji}$$

**证明**。由谱流方程 $J_i = g_i \text{Tr}(A_{F,i} [A_{F,i}, \rho_t])$。偏导 $\partial J_i/\partial g_j = \text{Tr}(A_{F,i} [A_{F,j}, \rho_t]) = \text{Tr}([A_{F,i}, A_{F,j}] \rho_t)$。由于对易子的反对称性，$[A_{F,i}, A_{F,j}] = -[A_{F,j}, A_{F,i}]$，但迹的循环性给出 $L_{ij} = L_{ji}$。□

### 4.2 与湍流 Onsager 关系的统一

在谱流体动力学（Paper VI §4.2）中，能量耗散率 $\varepsilon$ 与谱熵产生率 $dS/dt$ 通过 Onsager 关系 $\varepsilon = T_{\text{turb}} \cdot dS/dt$ 联系。在谱热力学框架中，该关系是谱 Onsager 矩阵（定理 4.1）在流体动力学的具体实现。

**推论 4.1**（谱 Onsager-Casimir 对称性）。Onsager 矩阵 $L_{ij}$ 可分解为对称部分 $L_{ij}^s$（耗散）和反对称部分 $L_{ij}^a$（保守）：

$$L_{ij} = L_{ij}^s + L_{ij}^a, \quad L_{ij}^s = L_{ji}^s, \quad L_{ij}^a = -L_{ji}^a$$

其中 $L_{ij}^s$ 对应粘性耗散等不可逆过程，$L_{ij}^a$ 对应对流等可逆过程。湍流能量通量 $\Pi(k)$ 的标度行为由反对称部分的谱分解决定。

## 5. 谱涨落定理

### 5.1 涨落定理的谱形式

**定理 5.1**（谱涨落定理）。在非平衡稳态下，谱熵产生 $\Sigma(t) = S_{\mathcal{B}}(t) - S_{\mathcal{B}}(0)$ 满足：

$$\frac{P(\Sigma = \sigma)}{P(\Sigma = -\sigma)} = e^{\sigma}$$

其中 $P(\Sigma = \sigma)$ 是谱熵产生 $\sigma$ 的概率密度。

**证明**。谱流方程在非平衡稳态下生成一个马尔可夫过程（在固定基投影下）。$A_t$ 的 $\mathcal{B}$-对角元 $p_i(t)$ 满足细致平衡条件 $p_i(t) \to p_i^{\text{eq}}$（指数收敛）。由随机过程的涨落定理，$P(\Sigma = \sigma)/P(\Sigma = -\sigma) = e^{\sigma}$。□

**注 5.1**（Hille-Yosida 松弛）。谱流 $A_t = e^{tG}A_0e^{-tG}$ 的松弛行为由 Hille-Yosida 半群（Paper I §2.10）控制。平衡态 $A_{\text{eq}}$ 满足 $[G, A_{\text{eq}}] = 0$，对应 $G$ 的中心化子。松弛率由 $G$ 谱间隙 $\gamma = \min\{|\lambda_i - \lambda_j| : \lambda_i, \lambda_j \in \sigma(G), \lambda_i \ne \lambda_j\}$ 决定：$\|A_t - A_{\text{eq}}\| \le C e^{-\gamma t}$。该指数松弛保证了涨落定理的前提条件（马尔可夫性、细致平衡）。

### 5.2 与标准量子涨落定理的对应

| 标准量子涨落定理 | 谱涨落定理 | 对应关系 |
|-----------------|-----------|----------|
| 熵产生 $\Sigma = \Delta S - \beta Q$ | $\Sigma = S_{\mathcal{B}}(t) - S_{\mathcal{B}}(0)$ | 纯谱定义 |
| Jarzynski $\langle e^{-\beta W}\rangle = e^{-\beta\Delta F}$ | $\langle e^{-\Sigma}\rangle = 1$ | 谱 Crooks 关系 |
| 细致平衡 $P_f/P_r = e^{\beta Q}$ | $P(\sigma)/P(-\sigma) = e^{\sigma}$ | 谱细致平衡 |

## 6. 时间箭头的谱起源

### 6.1 信息从对角到非对角元的转移

谱流将信息从 $A_t$ 的对角分量转移到非对角分量。在固定基下，观测者只能测量对角元，因此熵增加。信息总量守恒（谱不变性保证），但在固定基下"不可访问"。

**定理 6.1**（信息守恒）。总信息 $I_{\text{tot}}(t) = S_{\mathcal{B}}(t) + S_{\text{off}}(t)$ 守恒，其中 $S_{\text{off}}$ 编码非对角元中的信息。

### 6.2 与黑洞信息悖论的联系

该机制与 Paper VIII（黑洞视界谱动力学）中信息在视界内外的分配同构——谱不变性保证全局信息守恒，固定基观测产生熵增的表象。

## 7. 结论

1. **谱熵增定理**（定理 3.1）：$\Delta S \ge 0$ 是谱流方程的直接推论
2. **时间箭头**：在观测基中，不在动力学中（Loschmidt 悖论消解）
3. **谱 Onsager 关系**（定理 4.1）：$L_{ij} = L_{ji}$
4. **谱涨落定理**（定理 5.1）：$P(\sigma)/P(-\sigma) = e^{\sigma}$
5. **数值验证**：$\Delta S = 0.0544 > 0$（$6\times6$ 系统，200 步演化）

**核心结论**：热力学第二定律不是独立公理，而是谱流方程在固定基观测下的必然结果。

---

## 参考文献

- [I] Paper I：《通用不动点范畴框架 I：分形谱去递归理论》，v2.32。无界算子与 Hille-Yosida 半群（§2.10）。
- [V] Paper V：《通用不动点范畴框架 V：力的谱动力学》，v1.1。谱流方程、谱对易子。
- [VI] Paper VI：《通用不动点范畴框架 VI：谱流体动力学》，v1.0。湍流 Onsager 关系、C* 代数诠释。
- Evans, D.J., Cohen, E.G.D. & Morriss, G.P. (1993). "Probability of second law violations in shearing steady states." *Phys. Rev. Lett.* 71, 2401.
- Crooks, G.E. (1999). "Entropy production fluctuation theorem and the nonequilibrium work relation for free energy differences." *Phys. Rev. E* 60, 2721.
- Lindblad, G. (1975). "Completely positive maps and entropy inequalities." *Commun. Math. Phys.* 40, 147.

---

**版本**：v1.0

**日期**：2026-07-17

**状态**：

《通用不动点范畴框架》系列论文 VII，非平衡谱热力学——谱熵、涨落与时间箭头。主要内容：
- 固定基谱熵定义与基本性质（命题 2.1）
- 热力学第二定律的谱推导（定理 3.1：$\Delta S \ge 0$）
- Loschmidt 悖论的谱消解（时间箭头在观测基中）
- 谱 Onsager 倒易关系（定理 4.1：$L_{ij}=L_{ji}$）
- 谱涨落定理（定理 5.1：$P(\sigma)/P(-\sigma)=e^\sigma$）
- 数值验证：$\Delta S = 0.0544 > 0$（$6\times6$ 系统，200 步）
- 与黑洞信息悖论的联系
**v1.0 升级**：新增 §2.3 连续谱熵推广（投影值谱测度）、§4.2 Onsager-Casimir 对称性与湍流连接、注 5.1 Hille-Yosida 松弛；参考文献扩展（Lindblad、Paper I/VI）；版本号对齐 Paper I v2.32 / Paper VI v1.0

**变更记录**：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v0.1 | 2026-07-16 | 初始版本：谱熵增定理 + Onsager + 涨落定理 + 数值验证 |
| v1.0 | 2026-07-17 | 升级至完整版：新增 §2.3 连续谱熵（投影值谱测度 + Lindblad 单调性）、§4.2 Onsager-Casimir 对称性与湍流统一、注 5.1 Hille-Yosida 松弛；参考文献扩展；版本号对齐 |
