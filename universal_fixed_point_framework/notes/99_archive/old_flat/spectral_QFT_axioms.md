# 谱 QFT 公理系统草案

## 核心目标

从 T1-T3 翻译中发现的规律，提炼为谱 QFT 的公理系统，作为 **Paper XI** 的基础。

---

## 公理 A1：谱场存在公理

**定义**。对每个量子场 $\phi(x)$，存在对应的谱对象 $(\mathcal{H}_\phi, A_\phi, \sigma(A_\phi)) \in \mathbf{Spec}$，其中：
- $\mathcal{H}_\phi$ 是场的 Hilbert 空间
- $A_\phi$ 是谱算子（场的"谱生成元"）
- $\sigma(A_\phi) \subset \mathbb{R}$ 是 $A_\phi$ 的谱

**自由谱场**的谱作用量为：
$$S_{\text{free}}^{\text{spec}}[\Phi] = \frac12 \int d\lambda \, \Phi^\dagger(\lambda) (\lambda - m^2) \Phi(\lambda).$$

**来源**：T1 谱拉格朗日量翻译中的 KG/Dirac/YM 场的谱表示。

---

## 公理 A2：谱传播子公理

**定义**。谱 Feynman 传播子由谱算子的 Green 函数给出：
$$D_F^{\text{spec}}(\lambda, \lambda') = \langle 0 | T\Phi(\lambda)\Phi^\dagger(\lambda') | 0 \rangle = \delta(\lambda - \lambda') \cdot \frac{i}{\lambda - m^2 + i\varepsilon}.$$

**来源**：T2 谱 Feynman 规则翻译。

---

## 公理 A3：谱相互作用公理

**定义**。谱相互作用项由谱拉格朗日量中的非二次项给出。对 $\phi^4$ 理论：
$$\mathcal{L}_{\text{int}}^{\text{spec}} = -\frac{\lambda}{4!} \operatorname{Tr}_{\mathcal{H}}(\Phi^4),$$
这定义谱顶点：
$$V_4(\lambda_1, \lambda_2, \lambda_3, \lambda_4) = -i\lambda \cdot \delta(\lambda_1 + \lambda_2 + \lambda_3 + \lambda_4).$$

**来源**：T1 + T2。

---

## 公理 A4：谱路径积分公理

**定义**。谱 QFT 的生成泛函为：
$$Z_{\text{spec}}[J] = \int \mathcal{D}_{\text{Spec}}\Phi \; \exp\left(i S_{\text{spec}}[\Phi] + i \int d\lambda \, J(\lambda)\Phi(\lambda)\right),$$
其中谱测度为：
$$\mathcal{D}_{\text{Spec}}\Phi = \prod_{\lambda \in \sigma(A_\phi)} d\Phi(\lambda).$$

在有限维截断下退化为 Gaussian 积分。

**来源**：T3 谱路径积分翻译。

---

## 公理 A5：谱截断正则化公理

**定义**。谱 QFT 的自然紫外截断由谱算子 $A_\phi$ 的最大特征值 $\Lambda_{\max} = \max \sigma(A_\phi)$ 给出。谱截断版本为：
$$Z_{\text{spec}}^{\Lambda}[J] = \int \prod_{\lambda_i < \Lambda} d\Phi_i \; \exp\left(i S_{\text{spec}}^{\Lambda}[\Phi] + i \sum_i J_i \Phi_i\right).$$

当 $\Lambda = \Lambda_{\max} \sim M_{\text{Pl}}^2$ 时恢复完整理论。谱截断 $\Lambda$ 同时是紫外正则化器和物理边界。

**来源**：T3 谱重整化翻译 + Paper V A_GR 谱结构。

---

## 公理 A6：谱重整化公理

**定义**。谱重整化通过减除条件定义：
$$\Gamma^{(R)}(p^2 = \mu^2) = \Gamma_{\text{tree}},$$
其中 $\mu$ 是谱减除点。重整化耦合的谱 $\beta$ 函数为：
$$\beta(\lambda_R) = \frac{d\lambda_R}{d\ln\mu}.$$

对 $\lambda\phi^4$ 的单圈结果：
$$\beta(\lambda_R) = \frac{3\lambda_R^2}{16\pi^2}.$$

**来源**：T3 谱重整化翻译 + 数值验证。

---

## 从公理到定理

### 定理 1（谱 Wick 定理）。谱场的时序乘积等于所有配对缩并的和：
$$\langle 0 | T \Phi(\lambda_1) \cdots \Phi(\lambda_{2n}) | 0 \rangle = \sum_{\text{pairings}} \prod_{\text{pairs}} i D_F^{\text{spec}}(\lambda_a, \lambda_b).$$

**证明**：A4（谱路径积分）的微扰展开 + A2（谱传播子定义）。

### 定理 2（谱 Dyson 级数）。散射振幅的谱 Dyson 展开为：
$$\mathcal{M}^{\text{spec}} = \sum_{n=0}^\infty \mathcal{M}_n^{\text{spec}},$$
其中 $\mathcal{M}_n^{\text{spec}}$ 由 $n$ 个谱顶点和 $n-1$ 个内线谱传播子构成。

**证明**：A3 + A4 的微扰论展开。

### 定理 3（谱 $\beta$ 函数定理）。谱 $\beta$ 函数由谱截断 $\Lambda$ 的连续变化生成：
$$\beta(\lambda) = \left.\frac{d\lambda}{d\ln\Lambda}\right|_{\text{physical}}.$$

**证明**：A5（谱截断）的连续极限 + A6（谱重整化条件）。

---

## 与标准 QFT 公理系统的对应

| 标准 QFT (Wightman/Osterwalder-Schrader) | 谱 QFT |
|:----------------------------------------|:-------|
| 场算子 $\phi(x)$ 的存在性 | A1: 谱对象 $(\mathcal{H}, A, \sigma(A))$ |
| Wightman 函数 $W_n(x_1,\ldots,x_n)$ | A2+A3: 谱关联函数 $G_n(\lambda_1,\ldots,\lambda_n)$ |
| 路径积分测度 $\mathcal{D}\phi$ | A4: 谱测度 $\mathcal{D}_{\text{Spec}}\Phi$ |
| 重整化程序 | A5+A6: 谱截断 + 谱减除 |

---

## 开放问题：谱 QFT 公理的严格化方向

| 问题 | 难度 | 说明 |
|:----|:----:|------|
| 谱场的 Lorentz 协变变换规则 | 🟡 | 需将 Lorentz 群作用翻译为 $\mathbf{Spec}$ 范畴态射 |
| 谱版本的自旋-统计定理 | 🔴 | 谱 $\mathbb{Z}_2$ 分级结构 |
| 谱 CPT 定理 | 🔴 | 谱时间反演态射的存在性 |
| 谱 LSZ 约化公式 | 🟡 | 从谱关联函数到 S-矩阵的提取 |
| 无限维谱测度的严格定义 | 🔴 | $\sigma(A_\phi)$ 为连续谱时的测度论 |
