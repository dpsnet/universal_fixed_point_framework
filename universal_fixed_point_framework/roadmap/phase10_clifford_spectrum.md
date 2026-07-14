# Phase 10：Clifford 值谱的完整理论

> 本阶段目标：建立 Clifford 代数 $\mathrm{Cl}(p,q)$ 值自伴算子的谱理论，定义左谱、右谱与双向谱，
> 验证 $e^{-\mu}$ 在 Clifford 值谱上的函子性，并分析 SM（$\mathrm{Cl}(1,7)$）与
> 弦论（$\mathrm{Cl}(9,1)$）实例中是否只需标量谱。

---

## 1. 当前状态与局限

当前框架谱范畴 $\mathbf{Spec}$ 定义为标量正自伴算子 $A_R = -\log K_R$。但以下实例具有 Clifford 结构：

| 实例 | Clifford 代数 | 来源 | 当前处理 |
|---|---|---|---|
| SM 费米子质量 | $\mathrm{Cl}(1,7)$ | Clifford 签名 $(1,7) = 1$ 时间 + 7 空间维度 | 仅用标量谱 |
| 弦论 | $\mathrm{Cl}(9,1)$ | 10 维时空的 Clifford 表示 | 仅用标量谱 |

**缺失的理论**：
1. Clifford 值自伴算子的谱定义（左谱、右谱、双向谱）
2. $\lambda_i = e^{-\mu_i}$ 在 Clifford 值谱上的推广
3. 何时标量谱（当前做法）足够？何时需要全 Clifford 谱？

---

## 2. Clifford 代数与自伴算子

### 2.1 Clifford 代数 $\mathrm{Cl}(p,q)$

**定义 2.1**。Clifford 代数 $\mathrm{Cl}(p,q)$ 是由 $p+q$ 个生成元 $\{e_1,\dots,e_{p+q}\}$ 生成的实结合代数，满足：

$$e_i e_j + e_j e_i = 2\eta_{ij}, \quad \eta = \operatorname{diag}(\underbrace{1,\dots,1}_p, \underbrace{-1,\dots,-1}_q).$$

**表示**：$\mathrm{Cl}(p,q) \cong M_{2^{\lfloor (p+q)/2\rfloor}}(\mathbb{R})$ 或 $\mathbb{C}$ 或 $\mathbb{H}$（取决于 $p-q \bmod 8$）。

**迹**：Clifford 代数上存在正则迹 $\mathrm{Tr}_{\mathrm{Cl}} = \mathrm{Tr} \circ \rho$，其中 $\rho$ 是到矩阵代数的表示。

### 2.2 左谱、右谱与双向谱

**定义 2.2**（Clifford 值算子的谱）。设 $\mathcal{A} = \mathrm{Cl}(p,q)$，$T$ 是 Hilbert $\mathcal{A}$-模 $\mathcal{H}$ 上的有界 $\mathcal{A}$-线性算子。

- **左谱** $\sigma_L(T)$：$\{\lambda \in \mathcal{A} : \lambda I - T \text{ 不是左可逆的}\}$
- **右谱** $\sigma_R(T)$：$\{\lambda \in \mathcal{A} : \lambda I - T \text{ 不是右可逆的}\}$
- **双向谱** $\sigma(T) = \sigma_L(T) \cup \sigma_R(T)$

**定理 2.3**（标量约化）。设 $T$ 是 $\mathcal{A}$-线性自伴算子。若 $\mathcal{A}$ 是矩阵代数 $M_n(\mathbb{R})$，则

$$\sigma_L(T) = \sigma_R(T) = \sigma(T) \subseteq \mathbb{R},$$

且 $\sigma(T)$ 与 $T$ 在标量约化下的谱一致。

**证明**。对 $\mathcal{A} \cong M_n(\mathbb{R})$，左可逆等价于右可逆。自伴条件 $T = T^*$ 保证谱为实数。取 $\mathcal{A} \cong \mathbb{R}^n$（通过正则表示），得标量谱的对应。□

> **注**：对 $\mathrm{Cl}(1,7) \cong M_8(\mathbb{R})$，左谱 = 右谱 = 双向谱，且等于标量谱。
> 这解释了为什么 SM 实例中只取标量谱是充分的。

### 2.3 $\mathrm{Cl}(1,7)$ 与 $\mathrm{Cl}(9,1)$ 的具体结构

| 代数 | 矩阵同构 | 签名差 $p-q$ | Bott 周期 |
|---|---|---|---|
| $\mathrm{Cl}(1,7)$ | $M_8(\mathbb{R})$ | $-6 \equiv 2 \bmod 8$ | 复型 |
| $\mathrm{Cl}(9,1)$ | $M_{16}(\mathbb{R})$ | $8 \equiv 0 \bmod 8$ | 实型 |

**命题 2.4**。$\mathrm{Cl}(1,7) \cong M_8(\mathbb{R})$ 和 $\mathrm{Cl}(9,1) \cong M_{16}(\mathbb{R})$ 均为实矩阵代数。因此其上自伴算子的谱等于标量谱，当前框架中标量谱的处理是充分的。

---

## 3. $e^{-\mu}$ 的 Clifford 值函子性

**定义 3.1**（Clifford 值谱对应）。设 $K_R$ 是 $\mathcal{A}$-线性自伴压缩算子，$A_R = -\log K_R$（在 $\mathcal{A}$-值意义下）。谱对应 $\lambda_i = e^{-\mu_i}$ 在 Clifford 值意义下为

$$\sigma_{\mathcal{A}}(K_R) = e^{-\sigma_{\mathcal{A}}(A_R)} := \{e^{-\mu} : \mu \in \sigma_{\mathcal{A}}(A_R)\},$$

其中指数函数在 Clifford 代数上通过幂级数定义：

$$e^x = \sum_{n=0}^\infty \frac{x^n}{n!}, \quad x \in \mathcal{A}.$$

**定理 3.2**（Clifford 值谱映射定理）。设 $\mathcal{A}$ 是有限维实 $C^*$ 代数，$A$ 是 $\mathcal{A}$-线性自伴算子。则

$$\sigma_{\mathcal{A}}(e^{-A}) = e^{-\sigma_{\mathcal{A}}(A)}.$$

**证明**。由 $C^*$ 代数的谱映射定理：对任意全纯函数 $f$ 在 $\sigma(A)$ 的邻域上，$\sigma(f(A)) = f(\sigma(A))$。取 $f(\mu) = e^{-\mu}$ 即得。□

**推论 3.3**（标量谱的充分性）。对 $\mathcal{A} = \mathrm{Cl}(1,7)$ 或 $\mathrm{Cl}(9,1)$，$\mathcal{A} \cong M_n(\mathbb{R})$ 是有限维实 $C^*$ 代数，谱映射定理成立，且 $\sigma_{\mathcal{A}}$ 等同于标量谱。因此无需区分左谱、右谱与双向谱，也无需扩展当前框架。

---

## 4. 数值验证

### 4.1 $\mathrm{Cl}(1,7)$ 的矩阵表示

$\mathrm{Cl}(1,7)$ 的生成元 $\{e_1,\dots,e_8\}$ 可通过 $8\times 8$ 实矩阵表示。自伴算子 $A$ 的谱计算为 $A$ 的矩阵特征值。

**验证内容**：
1. $\mathrm{Cl}(1,7)$ 生成元的矩阵表示构造
2. Clifford 值自伴算子 $A$ 的左谱 = 右谱 = 标量谱
3. $e^{-A}$ 的谱 = $e^{-\sigma(A)}$

### 4.2 SM 质量谱的 Clifford 结构

SM 的 Dirac 算子 $D$ 在 Clifford 丛上作用，其谱三元组 $(A, H, D)$ 的自然结构由 Connes 给出。
当前 SM 实例仅取 $|D|$ 的标量谱（费米子质量谱），这是 $\mathrm{Cl}(1,7)$ 值谱在标量约化下的投影。

---

## 5. 与框架核心公理的关系

| Clifford 谱结果 | 支撑的公理/定理 |
|---|---|
| 左谱 = 右谱 = 双向谱（矩阵代数） | 定理 2.3 |
| $\sigma_{\mathcal{A}}(e^{-A}) = e^{-\sigma_{\mathcal{A}}(A)}$ | 定理 3.2（谱映射定理） |
| SM/弦论只需标量谱 | 推论 3.3 |

---

## 6. 结论

对当前框架涉及的 $\mathrm{Cl}(1,7)$ 与 $\mathrm{Cl}(9,1)$ 实例：

- **左谱 = 右谱 = 双向谱**，且等于标量谱（因为两者均为实矩阵代数）
- **谱映射定理**在 $C^*$ 代数框架下直接适用
- **当前标量谱处理是充分的**，无需扩展 $\mathbf{Spec}$ 范畴的定义

因此 §2.6 Clifford 值谱理论**不影响当前框架的完备性**。如需扩展至一般 Clifford 代数（如 $\mathrm{Cl}(0,2) \cong \mathbb{H}$，四元数谱），则需进一步的范畴构造。

---

## 7. 版本记录

- v0.1（2026-07-12）：初稿，建立 Clifford 值谱理论基础，证明 SM/弦论标量谱的充分性。
