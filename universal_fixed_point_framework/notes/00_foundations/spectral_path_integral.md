# 谱路径积分与谱重整化

## 核心目标

将标准 QFT 的路径积分和重整化程序翻译为谱语言，建立从谱拉格朗日量到散射振幅计算的完整体系。

---

## 1. 谱路径积分

### 1.1 定义

**定义 1**（谱路径积分）。对于谱标量场 $\Phi(\lambda)$，谱路径积分为对谱算子 $A_\phi$ 的谱分解模式的泛函积分：

$$Z_{\text{spec}}[J] = \int \mathcal{D}_{\text{Spec}}\Phi \; \exp\left(i S_{\text{spec}}[\Phi] + i \int d\lambda \, J(\lambda) \Phi(\lambda)\right),$$

其中谱测度 $\mathcal{D}_{\text{Spec}}\Phi$ 是 $\mathbf{Sp}$ 范畴中谱对象 $A_\phi$ 的所有态射变分的积：

$$\mathcal{D}_{\text{Spec}}\Phi = \prod_{\lambda \in \sigma(A_\phi)} d\Phi(\lambda).$$

在有限维截断下（$d$ 个离散谱模式），谱路径积分退化为 $d$ 维 Gaussian 积分：

$$Z_{\text{spec}}[J] = \int \prod_{i=1}^d d\Phi_i \; \exp\left(i S_{\text{spec}}[\{\Phi_i\}] + i \sum_i J_i \Phi_i\right).$$

### 1.2 自由谱生成泛函

对自由谱标量场，谱作用量为：

$$S_{\text{free}}^{\text{spec}}[\Phi] = \frac12 \int d\lambda \, \Phi(\lambda) (\lambda - m^2) \Phi(\lambda).$$

谱路径积分可直接计算：

$$Z_{\text{free}}^{\text{spec}}[J] = \exp\left(-\frac12 \iint d\lambda d\lambda' \, J(\lambda) D_F^{\text{spec}}(\lambda, \lambda') J(\lambda')\right),$$

其中 $D_F^{\text{spec}}(\lambda, \lambda') = \delta(\lambda - \lambda') \cdot \frac{i}{\lambda - m^2 + i\varepsilon}$ 是谱 Feynman 传播子（T2）。

### 1.3 关联函数的谱表示

谱关联函数由对 $J$ 的泛函导数得到：

$$G_n^{\text{spec}}(\lambda_1, \ldots, \lambda_n) = \frac{1}{i^n} \frac{\delta^n Z_{\text{spec}}[J]}{\delta J(\lambda_1) \cdots \delta J(\lambda_n)} \bigg|_{J=0}.$$

两点关联函数为：

$$G_2^{\text{spec}}(\lambda, \lambda') = i D_F^{\text{spec}}(\lambda, \lambda').$$

### 1.4 谱路径积分的微扰展开

当相互作用项 $S_{\text{int}}^{\text{spec}}[\Phi] = -\frac{\lambda}{4!} \int d\lambda \, \Phi^4(\lambda)$ 存在时：

$$Z_{\text{spec}}[J] = \exp\left(i S_{\text{int}}^{\text{spec}}\left[\frac{1}{i} \frac{\delta}{\delta J}\right]\right) Z_{\text{free}}^{\text{spec}}[J].$$

谱 Wick 定理：谱场的时序乘积等于所有配对缩并的和，每个缩并贡献一个谱传播子：

$$\langle 0 | T \Phi(\lambda_1) \cdots \Phi(\lambda_{2n}) | 0 \rangle = \sum_{\text{pairings}} \prod_{\text{pairs }(a,b)} i D_F^{\text{spec}}(\lambda_a, \lambda_b).$$

---

## 2. 谱重整化

### 2.1 谱截断正则化

谱路径积分天然提供 UV 正则化机制：谱算子 $A_\phi$ 的谱 $\sigma(A_\phi)$ 有最大特征值 $\lambda_{\max} \sim M_{\text{Pl}}^2$。谱路径积分的截断版本为：

$$Z_{\text{spec}}^{\Lambda}[J] = \int \prod_{\lambda_i < \Lambda} d\Phi_i \; \exp\left(i S_{\text{spec}}^{\Lambda}[\Phi] + i \sum_i J_i \Phi_i\right),$$

其中谱截断 $\Lambda$ 自动切断高能模式——无需手动引入 cutoff 或 dimensional regularization。

### 2.2 谱二点函数的单圈修正

谱二点函数的单圈修正为：

$$\Pi^{\text{spec}}(p^2) = \frac{\lambda}{2} \int_0^{\Lambda^2} d\lambda' \frac{1}{\lambda' - m^2 + i\varepsilon}.$$

在谱截断 $\Lambda$ 下：

$$\Pi^{\text{spec}}(p^2) = \frac{\lambda}{2} \ln\left(\frac{\Lambda^2 - m^2}{-m^2}\right) \approx \frac{\lambda}{2} \ln\left(\frac{\Lambda^2}{m^2}\right).$$

谱重整化条件：在 $p^2 = \mu^2$ 处减除：

$$\Pi_R^{\text{spec}}(p^2) = \Pi^{\text{spec}}(p^2) - \Pi^{\text{spec}}(\mu^2) = \frac{\lambda}{2} \ln\left(\frac{p^2}{\mu^2}\right).$$

### 2.3 谱四点函数与单圈 β 函数

谱四点函数（$\phi^4$ 耦合）的单圈修正来自 $s$、$t$、$u$ 三道：

$$\Gamma_4^{\text{spec}}(s, t, u) = -i\lambda + \frac{3\lambda^2}{32\pi^2} \ln\left(\frac{\Lambda^2}{s}\right) + \text{交叉项} + \mathcal{O}(\lambda^3).$$

谱重整化后在 $s = \mu^2$ 处减除，定义重整化耦合 $\lambda_R(\mu)$：

$$\lambda_R(\mu) = \lambda + \frac{3\lambda^2}{32\pi^2} \ln\left(\frac{\Lambda^2}{\mu^2}\right).$$

由此得到 **单圈 β 函数**：

$$\boxed{\beta(\lambda_R) = \frac{d\lambda_R}{d\ln\mu} = \frac{3\lambda_R^2}{16\pi^2}}.$$

这与标准 QFT 的 $\lambda\phi^4$ 单圈 β 函数完全一致。

### 2.4 谱重整化方案

| 标准 QFT | 谱版本 |
|---------|-------|
| Dimensional Regularization $d = 4 - \varepsilon$ | 谱截断 $\lambda_{\max} \sim M_{\text{Pl}}^2$ |
| $\overline{\text{MS}}$ 减除方案 | 谱减除点 $\mu^2$ |
| Counter-term $\delta\mathcal{L} = \delta_Z \partial_\mu\phi\partial^\mu\phi + \delta_m m^2\phi^2 + \delta_\lambda \phi^4$ | 谱 Counter-term $\delta\mathcal{L}^{\text{spec}} = \delta_Z \Phi(\lambda - m^2)\Phi + \delta_\lambda \Phi^4$ |
| β 函数 $\beta = 3\lambda^2/16\pi^2$ | 谱 β 函数 $\beta^{\text{spec}} = 3\lambda_R^2/16\pi^2$ |

### 2.5 谱传播子的单圈修正

质量壳重整化后的谱传播子为：

$$D_F^{(R)}(p^2) \approx \frac{i}{p^2 - m_R^2 + \Sigma_R(p^2) + i\varepsilon},$$

其中 $\Sigma_R(p^2) \propto \ln(p^2/\mu^2)$ 来自单圈自能图。

---

## 3. 与标准 QFT 的对应

| 标准 QFT | 谱版本 |
|---------|-------|
| 路径积分 $\int \mathcal{D}\phi \, e^{iS[\phi]}$ | 谱路径积分 $\int \mathcal{D}_{\text{Spec}}\Phi \, e^{iS_{\text{spec}}[\Phi]}$ |
| 生成泛函 $Z[J]$ | $Z_{\text{spec}}[J]$ |
| 两点函数 $\langle 0|T\phi(x)\phi(y)|0\rangle$ | $G_2^{\text{spec}}(\lambda, \lambda') = i D_F^{\text{spec}}(\lambda, \lambda')$ |
| UV 截断 $\Lambda_{\text{UV}}$ | 谱截断 $\lambda_{\max}$ |
| Counter-term 减除 | 谱减除条件 $\Gamma^{(R)}(p^2 = \mu^2) = \Gamma_{\text{tree}}$ |
| β 函数 $\beta = 3\lambda^2/16\pi^2$ | 谱 β 函数 $\beta^{\text{spec}} = 3\lambda_R^2/16\pi^2$ |

---

## 4. 数值验证

配套脚本 `paperX_spectral_renormalization.py` 验证以下内容：

1. **自由谱路径积分**：Gaussian 积分在离散谱下的精确性
2. **谱截断正则化**：$\int_0^{\Lambda^2} d\lambda/(\lambda - m^2)$ 有限性
3. **单圈二点函数**：$\Pi(p^2) \propto \ln(\Lambda^2/m^2)$ 标度
4. **单圈四点函数**：$\Gamma_4(s) \propto \ln(s/\mu^2)$ 标度
5. **β 函数还原**：$\beta(\lambda_R) \approx 3\lambda_R^2/16\pi^2$（相对误差 < 5%）

---

## 5. 开放问题

| 问题 | 说明 |
|------|------|
| 谱路径积分的测度定义 | 无限维极限下的泛函测度严格化 |
| 谱重整化群流方程 | 谱截断 $\Lambda$ 连续变化的 RG 方程 |
| 多圈重整化 | 两圈及以上的谱 Feynman 图翻译 |
| 规范场重整化 | 谱版本的 FP 鬼场和 Ward 恒等式 |
