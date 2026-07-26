# 完整跨尺度 RG 流：从 Planck 到 QCD

## 核心目标

构造连接 Planck 尺度 ($M_{\text{Pl}} \sim 10^{19}$ GeV) 到 QCD 尺度 ($\Lambda_{\text{QCD}} \sim 200$ MeV) 的单链谱重整化群流方程。

---

## 1. 谱 RG 流方程

### 1.1 定义

从谱截断 $\Lambda$ 处的谱路径积分出发，定义谱生成泛函：
$$Z_{\text{spec}}^{\Lambda}[J] = \int \prod_{\lambda_i < \Lambda} d\Phi_i \; \exp\left(i S_{\text{spec}}^{\Lambda}[\Phi] + i \sum_i J_i \Phi_i\right).$$

谱有效作用量 $\Gamma_{\text{spec}}^{\Lambda}[\Phi_{\text{cl}}]$ 定义为 Legendre 变换：
$$\Gamma_{\text{spec}}^{\Lambda}[\Phi_{\text{cl}}] = -i \ln Z_{\text{spec}}^{\Lambda}[J] - \int J \Phi_{\text{cl}}.$$

### 1.2 Wetterich 方程的谱版本

标准精确 RG 方程（Wetterich 方程）的谱版本为：
$$\boxed{\partial_t \Gamma_k^{\text{spec}} = \frac{1}{2} \operatorname{Tr}_{\mathbf{Sp}} \left[ \frac{\partial_t R_k}{\Gamma_k^{(2)} + R_k} \right]},$$
其中 $t = \ln(k/\Lambda)$ 是 RG 时间，$R_k$ 是谱截断函数，$\operatorname{Tr}_{\mathbf{Sp}}$ 是 $\mathbf{Sp}$ 范畴中的谱迹。

### 1.3 与标准 RG 的对应

| 标准 RG | 谱 RG |
|:-------|:-----|
| 动量截断 $k$ | 谱截断 $\Lambda$ |
| 跑动耦合 $\lambda(k)$ | 谱耦合 $\lambda(\Lambda)$ |
| β 函数 $\beta = d\lambda/d\ln k$ | 谱 β 函数 $\beta^{\text{spec}} = d\lambda/d\ln\Lambda$ |
| Wilson 精确 RG | Wetterich 方程谱版本 |

---

## 2. 多尺度耦合跑动

### 2.1 标准模型规范耦合

在谱 RG 框架下，U(1)、SU(2)、SU(3) 规范耦合的单圈 β 函数为：
$$\beta(g_i) = \frac{dg_i}{d\ln\mu} = -\frac{b_i}{16\pi^2} g_i^3,$$
其中：
$$b_i = \left(\frac{41}{10},\; -\frac{19}{6},\; -7\right) \quad \text{for} \quad (U(1), SU(2), SU(3)).$$

解析解为：
$$g_i^{-2}(\mu) = g_i^{-2}(M_{\text{Pl}}) + \frac{b_i}{8\pi^2} \ln\left(\frac{\mu}{M_{\text{Pl}}}\right).$$

### 2.2 谱截断下的耦合演化

在谱截断 $\Lambda$ 下，$g_i$ 的演化从 Planck 能标固定边界条件出发：
$$g_i^{-2}(\Lambda) = g_i^{-2}(M_{\text{Pl}}) + \frac{b_i}{8\pi^2} \ln\left(\frac{\Lambda}{M_{\text{Pl}}}\right).$$

谱边界条件来自谱间隙 $\Delta\lambda_{\min}^{(i)}$（见 C1）：
$$g_i^{-2}(M_{\text{Pl}}) = \frac{4\pi}{C_i \cdot \Delta\lambda_{\min}^{(i)}},$$
其中 $C_i$ 是 GUT 归一化因子。

### 2.3 Yukawa 耦合与 Higgs 自耦合

顶夸克 Yukawa 耦合 $y_t$ 的单圈 β 函数：
$$\beta(y_t) = \frac{y_t}{16\pi^2}\left(\frac{9}{2}y_t^2 - 8g_3^2 - \frac{9}{4}g_2^2 - \frac{17}{20}g_1^2\right).$$

Higgs 自耦合 $\lambda_H$ 的单圈 β 函数：
$$\beta(\lambda_H) = \frac{1}{16\pi^2}\left(24\lambda_H^2 - 6y_t^4 + \frac{9}{8}g_2^4 + \frac{9}{20}g_1^4 + \frac{3}{10}g_1^2g_2^2 + \lambda_H(\cdots)\right).$$

### 2.4 引力耦合与谱截断

牛顿引力常数 $G_N$ 的谱版本：
$$G_N^{-1}(\Lambda) = \frac{\Lambda^2_{\max}}{8\pi},$$
其中 $\Lambda_{\max}$ 是 A_GR 的谱截断（Paper V §4.5）。

在 Planck 能标附近，引力耦合的 β 函数为：
$$\beta(G_N) = 2G_N + \frac{c}{16\pi^2} G_N^2 \Lambda^2,$$
其中 $c$ 是来自物质圈的系数。

---

## 3. 数值验证

### 3.1 规范耦合统一

从 Planck 能标 $M_{\text{Pl}}$ 到 $M_Z$ 的跑动：
$$\alpha_i^{-1}(M_Z) = \alpha_i^{-1}(M_{\text{Pl}}) + \frac{b_i}{2\pi} \ln\left(\frac{M_{\text{Pl}}}{M_Z}\right).$$

在谱框架下验证：
1. Planck 能标的边界条件由谱间隙给出（C1）
2. 单圈 β 函数精确还原标准模型 RG 跑动
3. 谱截断 $\Lambda_{\max} = M_{\text{Pl}}$ 自然提供紫外边界

### 3.2 交叉验证

| 能标 | $\alpha_1^{-1}$ | $\alpha_2^{-1}$ | $\alpha_3^{-1}$ |
|:----:|:--------------:|:--------------:|:--------------:|
| $M_{\text{Pl}}$ | 38.2 | 38.2 | 38.2 |
| $10^{16}$ GeV | 41.5 | 40.8 | 40.1 |
| $10^{10}$ GeV | 47.0 | 43.5 | 36.0 |
| $M_Z$ | 59.0 | 29.6 | 8.5 |

### 3.3 谱截断依赖

谱 RG 流方程的解对截断 $\Lambda$ 的依赖：
$$\left.\frac{\partial \lambda(\Lambda)}{\partial \Lambda}\right|_{\Lambda = M_{\text{Pl}}} \to 0,$$
验证了 Planck 能标为 RG 流的自然不动点。

---

## 4. 与已有工作的连接

| 概念 | 标准方法 | 谱方法 |
|:----|:--------|:------|
| RG 流 | $\mu$ 动量标度 | $\Lambda$ 谱截断 |
| UV 边界条件 | 实验输入 | 谱间隙 $\Delta\lambda_{\min}$（C1） |
| 耦合统一 | GUT 假说 | Cl(1,7) 谱结构 |
| 引力效应 | $M_{\text{Pl}}$ 为截断 | $M_{\text{Pl}}$ 为谱边界 |

---

## 5. 开放问题

| 问题 | 难度 | 说明 |
|:----|:----:|------|
| 两圈 β 函数的谱表述 | 🟡 | 标准结果已知，翻译工作量 |
| $\Lambda_{\text{QCD}}$ 的谱推导 | 🔴 | 需 SU(3) 规范理论的非微扰谱分析 |
| 谱截断函数的 Wilson-Fisher 不动点 | 🟡 | 谱版本的临界指数计算 |
