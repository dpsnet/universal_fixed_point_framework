# 谱 QFT 形式化严格化：LSZ、幺正性与 Cutkosky 规则

## 核心目标

完善谱 QFT 的基础形式化——建立谱版本的 LSZ 约化公式、S 矩阵幺正性和 Cutkosky 切割规则，闭合从谱关联函数到物理散射截面的完整推导链。

---

## 1. 谱 LSZ 约化公式

### 1.1 标准 LSZ 公式回顾

标准 LSZ 约化公式将 S 矩阵元与关联函数的极点残差关联：

$$\langle p_1,\ldots,p_n^{\text{out}} | k_1,\ldots,k_m^{\text{in}} \rangle = \prod_{i=1}^n \frac{i}{p_i^2 - m^2 + i\varepsilon} \prod_{j=1}^m \frac{i}{k_j^2 - m^2 + i\varepsilon} \times G_{n+m}(p_1,\ldots,-k_1,\ldots),$$

其中 $G_{n+m}$ 是 $(n+m)$-点关联函数。

### 1.2 谱 LSZ 公式

在谱语言中，动量壳条件 $p_i^2 = m^2$ 对应谱条件 $\lambda_i = m^2$：

$$\boxed{\langle p_1,\ldots,p_n^{\text{out}} | k_1,\ldots,k_m^{\text{in}} \rangle_{\text{spec}} = \prod_{i=1}^n \frac{i}{\lambda_i - m^2 + i\varepsilon} \prod_{j=1}^m \frac{i}{\lambda_j - m^2 + i\varepsilon} \times G_{n+m}^{\text{spec}}(\lambda_1,\ldots,\lambda_{n+m})}.$$

**定理 1**（谱 LSZ 等价性）。谱 LSZ 公式在谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 下与标准 LSZ 公式等价：

$$D(\text{LSZ}_{\text{std}}) = \text{LSZ}_{\text{spec}}.$$

### 1.3 从谱关联函数提取 S 矩阵元

算法步骤：
1. 计算谱关联函数 $G_n^{\text{spec}}(\lambda_1,\ldots,\lambda_n)$
2. 在每个外腿的 $\lambda_i = m^2$ 处取残差
3. 乘以波函数重整化因子 $Z^{1/2}$（从谱传播子的极点残差读取）

---

## 2. 谱 S 矩阵幺正性

### 2.1 幺正条件

S 矩阵的幺正性 $S^\dagger S = I$ 在谱语言中为：

$$\sum_n \int d\Pi_n^{\text{spec}} \langle f | n \rangle_{\text{spec}} \langle n | i \rangle_{\text{spec}}^* = \delta_{fi},$$

其中谱相空间 $d\Pi_n^{\text{spec}}$ 为：

$$d\Pi_n^{\text{spec}} = \prod_{i=1}^n \frac{d^3 p_i}{(2\pi)^3 2E_i} \cdot \delta_{\text{spec}}(\Sigma \lambda_i),$$

$\delta_{\text{spec}}$ 是谱能量-动量守恒。

### 2.2 谱光学定理

光学定理 $2\operatorname{Im} \mathcal{M}(s) = \sum_n \int d\Pi_n |\mathcal{M}_n|^2$ 的谱版本：

$$2\operatorname{Im} \mathcal{M}^{\text{spec}}(s) = \int d\Pi_2^{\text{spec}} |\mathcal{M}^{\text{spec}}|^2 + \int d\Pi_3^{\text{spec}} |\mathcal{M}^{\text{spec}}|^2 + \cdots.$$

对 $\phi^4$ 理论的 $2\to2$ 散射（leading order）：

$$2\operatorname{Im} \mathcal{M}^{\text{spec}}(s) = \frac{1}{2} \int \frac{d^3 p_1 d^3 p_2}{(2\pi)^6 4E_1 E_2} (2\pi)^4 \delta^{(4)}(p_1+p_2-k_1-k_2) \cdot |\mathcal{M}_{\text{tree}}|^2.$$

---

## 3. 谱 Cutkosky 规则

### 3.1 切割规则

Cutkosky 规则将 Feynman 图的割不连续性与相空间积分关联：

$$\operatorname{Disc} \mathcal{M}(s) = 2i \operatorname{Im} \mathcal{M}(s) = \sum_{\text{cuts}} \int d\Pi_{\text{cut}} \prod_{\text{cut propagators}} \left( \frac{i}{p^2 - m^2 + i\varepsilon} \right)^*,$$

其中切割传播子被替换为 delta 函数：

$$\frac{i}{p^2 - m^2 + i\varepsilon} \to 2\pi \delta_+(p^2 - m^2).$$

### 3.2 谱 Cutkosky 规则

在谱语言中：

$$\boxed{\operatorname{Disc}^{\text{spec}} \mathcal{M}^{\text{spec}}(\lambda) = \sum_{\text{cuts}} \int d\Pi_{\text{cut}}^{\text{spec}} \prod_{\text{cut propagators}} 2\pi \delta_+(\lambda_i - m^2)}.$$

谱切割传播子：

$$D_F^{\text{spec}}(\lambda) = \frac{i}{\lambda - m^2 + i\varepsilon} \quad \Longrightarrow \quad \operatorname{Cut} D_F^{\text{spec}}(\lambda) = 2\pi \delta(\lambda - m^2).$$

### 3.3 谱单圈切割验证

对 $\phi^4$ 的 $s$-道单圈图，不连续性的谱形式：

$$\operatorname{Disc} \mathcal{M}_{\text{1-loop}}^{\text{spec}}(s) = \frac{\lambda^2}{2} \int \frac{d^4 k}{(2\pi)^4} 2\pi \delta_+(k^2 - m^2) 2\pi \delta_+((p-k)^2 - m^2).$$

这给出标准结果：

$$\operatorname{Im} \mathcal{M}_{\text{1-loop}}(s) = \frac{\lambda^2}{32\pi} \sqrt{1 - \frac{4m^2}{s}} \cdot \Theta(s - 4m^2).$$

---

## 4. 谱 Källén-Lehmann 表示

### 4.1 谱密度函数

全谱传播子的 Källén-Lehmann 表示为：

$$D_F^{\text{spec}}(\lambda) = \int_0^\infty d\mu^2 \frac{\rho(\mu^2)}{\lambda - \mu^2 + i\varepsilon},$$

其中谱密度函数 $\rho(\mu^2)$ 由谱函数定义：

$$\rho(\mu^2) = \sum_n \delta(\mu^2 - m_n^2) |\langle 0 | \Phi(0) | n \rangle|^2.$$

### 4.2 谱密度求和规则

谱密度函数的归一化条件（谱求和规则）：

$$\int_0^\infty d\mu^2 \rho(\mu^2) = 1.$$

对单粒子态 + 连续谱：

$$\rho(\mu^2) = Z \delta(\mu^2 - m^2) + \rho_{\text{cont}}(\mu^2) \Theta(\mu^2 - 4m^2),$$

其中 $Z$ 是波函数重整化因子。

---

## 5. 与标准 QFT 的对应

| 概念 | 标准 QFT | 谱版本 |
|:----|:---------|:-------|
| LSZ 约化公式 | $\prod i/(p^2-m^2) \times G$ | $\prod i/(\lambda-m^2) \times G^{\text{spec}}$ |
| 壳条件 | $p^2 = m^2$ | $\lambda = m^2$ |
| 光学定理 | $2\operatorname{Im} M = \sum \int d\Pi |M|^2$ | 同左，$d\Pi^{\text{spec}}$ |
| Cutkosky 规则 | $D_F \to 2\pi\delta_+(p^2-m^2)$ | $D_F^{\text{spec}} \to 2\pi\delta(\lambda-m^2)$ |
| Källén-Lehmann | $\int \rho(\mu^2)/(p^2-\mu^2)$ | $\int \rho(\mu^2)/(\lambda-\mu^2)$ |
| 求和规则 | $\int \rho(\mu^2)d\mu^2 = 1$ | 同左 |

---

## 6. 数值验证

### 6.1 LSZ 残差提取

从谱二点函数提取极点残差 $Z$：
$$G_2^{\text{spec}}(\lambda) = \frac{iZ}{\lambda - m^2 + i\varepsilon} + \text{连续谱}.$$

### 6.2 Cutkosky 规则

数值验证 $\phi^4$ 单圈图的割不连续性与 Im 部分的关系。

### 6.3 光学定理

验证 $2\operatorname{Im} M^{\text{spec}}(s) = \sigma_{\text{tot}}(s) \cdot s$ 在阈能以上的行为。

---

## 7. 开放问题

| 问题 | 难度 | 说明 |
|:----|:----:|------|
| 谱规范的 LSZ 公式 | 🟡 | 需引入谱 BRST 上同调与物理态投射 |
| 谱 Landau 方程 | 🔴 | 奇点结构与谱参数的 Landau 曲线 |
| 谱色散关系与因果性 | 🟡 | $\operatorname{Re} M \sim \int \operatorname{Im} M/(s'-s)$ 的谱翻译 |
| 谱重整化与求和规则的一致性 | 🟡 | 谱求和规则在谱截断下的保持 |
