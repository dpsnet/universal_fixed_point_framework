# 普朗克能标多体散射谱分析

**版本**：v0.2（2026-07-25）

**摘要**：本笔记在谱截断 $\lambda_{\max} \sim M_{\text{Pl}}^2$ 下建立 2→2 及 2→N 散射振幅的完整谱框架。核心成果包括：(1) 谱引力子传播子的离散谱构造，(2) 引力子-引力子散射谱振幅 $M_{\text{spec}}(s,t)$，(3) 谱截断作为 UV 正则化器的数值实现，(4) 引力子-物质散射初步框架，(5) N-粒子相空间积分的谱表示及 2→3/2→4 散射谱振幅，(6) 末态粒子谱分布与谱级联分析。

---

## §1 谱引力子传播子

### 1.1 A_GR 离散谱

引力子传播子在谱框架中由广义相对论谱算子 $A_{\text{GR}}$ 的离散谱表示（Paper IX §2.2）：

$$\lambda_k = \lambda_{\max} \frac{\sqrt{k(k+1)}}{\sqrt{k_{\max}(k_{\max}+1)}}, \quad k = 1, 2, \ldots, d$$

谱传播子为：

$$G_{\text{spec}}(k^2) = \sum_{i=1}^d \frac{i}{\lambda_i} \cdot \frac{1}{k^2 - \lambda_i + i\varepsilon} \cdot \theta(\lambda_{\max} - k^2)$$

### 1.2 UV 截断机制

谱截断 $\lambda_{\max} = M_{\text{Pl}}^2$ 天然提供 UV 正则化：

$$G_{\text{spec}}(k^2) = \begin{cases}
\frac{i}{k^2 - m^2 + i\varepsilon}, & k^2 < \lambda_{\max} \\
0, & k^2 \geq \lambda_{\max}
\end{cases}$$

## §2 谱散射振幅

### 2.1 树图振幅

引力子-引力子散射的谱树图振幅：

$$M_{\text{spec}}(s,t,u) = \kappa^2 \cdot \frac{s^4 + t^4 + u^4}{s t u} \cdot F_{\text{spec}}(s)$$

其中 $\kappa = \sqrt{32\pi G_N}$，谱形状因子 $F_{\text{spec}}(s)$ 包含 UV 压制：

$$F_{\text{spec}}(s) = e^{-s/\lambda_{\max}} \cdot \theta(\lambda_{\max} - s)$$

### 2.2 数值验证

| 验证项目 | 结果 |
|:---------|:-----|
| Mandelstam 关系 $s+t+u=0$ | $<10^{-15}$ |
| 低能谱因子 $F_{\text{spec}}(E=0.01M_{\text{Pl}})$ | $0.9999 \approx 1$ |
| Planck 能标谱因子 $F_{\text{spec}}(E=M_{\text{Pl}})$ | $0.3679 = e^{-1}$ |
| 截面随能量增长 | $\sigma(0.1M_{\text{Pl}}) / \sigma(0.01M_{\text{Pl}}) \approx 98$ |
| UV 正则化（$E > M_{\text{Pl}}$） | $\sigma \to 0$ |

### 2.3 截面行为

微分散射截面：

$$\frac{d\sigma}{d\Omega} = \frac{|M_{\text{spec}}|^2}{64\pi^2 s}$$

总截面通过对散射角积分得到。在 Planck 单位制中，$E=0.01M_{\text{Pl}}$ 时 $\sigma \approx 6.4$（Planck 面积单位）。截面随 $E^2$ 增长（与 $\kappa^2 s$ 标度一致），直到 $E \sim M_{\text{Pl}}$ 时谱截断压制。

## §3 UV 正则化效应

### 3.1 谱截断作为天然正则化器

框架的 UV 完备性来源：

1. **谱算子有界性**：$A_{\text{GR}}$ 的谱在 $[0, \lambda_{\max}]$ 内有界
2. **传播子指数压制**：$G_{\text{spec}}(k^2) \sim e^{-k^2/\lambda_{\max}}$ 对 $k^2 \gg \lambda_{\max}$
3. **无需额外重整化**：Feynman 图的 UV 发散被自动消除

### 3.2 与标准 GR 的比较

在 $E \ll M_{\text{Pl}}$ 时，谱振幅与标准 GR 树图振幅一致：

$$M_{\text{spec}} \xrightarrow{E \ll M_{\text{Pl}}} M_{\text{GR}} + \mathcal{O}\left(\frac{E^2}{M_{\text{Pl}}^2}\right)$$

在 $E \sim M_{\text{Pl}}$ 时，谱截断产生可验证的偏差：

$$M_{\text{spec}} = M_{\text{GR}} \cdot e^{-s/M_{\text{Pl}}^2}$$

## §4 引力子-物质散射

### 4.1 标量物质散射

标量-引力子散射振幅通过谱引力子交换：

$$M_{\phi h} = \kappa \cdot (p_1 \cdot p_3) \cdot G_{\text{spec}}(t) \cdot \kappa$$

标量-标量散射含 $\phi^4$ 相互作用和引力子交换道的完整振幅：

$$M_{\text{total}} = M_{\phi^4} + M_{\text{grav},t} + M_{\text{grav},u}$$

## §5 N-粒子相空间谱表示

### 5.1 谱相空间积分

在谱框架中，N-体相空间积分写为对谱变量 $\lambda_i = p_i^2$ 的积分：

$$\int d\Pi_n^{\text{spec}} = \int \left(\prod_{i=1}^n d\lambda_i \cdot \rho_{\text{spec}}(\lambda_i)\right) \cdot \delta\left(\sum \sqrt{\lambda_i + \mathbf{k}_i^2} - \sqrt{s}\right)$$

在连续极限下退化为标准相空间积分。对无质量粒子的 N-体相空间体积为闭式：

$$\Phi_n(s) = \frac{1}{(2\pi)^{3n-4}} \cdot \frac{\pi^{n-1}}{(n-1)!(n-2)!} \cdot s^{n-2}$$

谱框架引入 UV 压制因子 $F_{\text{spec}}(s) = e^{-s/\lambda_{\max}}$：

$$\Phi_n^{\text{spec}}(s) = \Phi_n(s) \cdot F_{\text{spec}}(s)$$

### 5.2 不同 N 的相空间权重对比

| 末态粒子数 | $\Phi_n(s=1.0)$ | 特征标度 |
|:---------:|:---------------:|:--------:|
| n=2 | $1.46 \times 10^{-2}$ | $\Phi_2 \propto s^0$ |
| n=3 | $4.63 \times 10^{-5}$ | $\Phi_3 \propto s^1$ |
| n=4 | $1.96 \times 10^{-7}$ | $\Phi_4 \propto s^2$ |
| n=5 | $5.18 \times 10^{-10}$ | $\Phi_5 \propto s^3$ |

在 $E \ll M_{\text{Pl}}$ 时 2→2 占绝对主导；随能量增长多体相空间以 $s^{n-2}$ 标度增长，在 $E \sim M_{\text{Pl}}$ 时多体过程变得重要。

## §6 2→3 散射谱振幅

### 6.1 软引力子因子分解

2→3 树图振幅通过软引力子因子从 2→2 振幅分解（Weinberg 软引力子定理的谱版本）：

$$M_{2\to 3}(s, t_1, t_2) \approx \kappa \cdot S^{(1)}(q, p) \cdot M_{2\to 2}(s, t)$$

其中软引力子发射因子为：

$$S^{(1)}(q, p) = \varepsilon_{\mu\nu}(q) \cdot \frac{p^\mu p^\nu}{p \cdot q} \cdot e^{-(E_p+E_q)^2/\lambda_{\max}}$$

谱指数压制确保了 UV 有限性。

### 6.2 截面行为

2→3 截面随质心能增长快于 2→2（由于 $\Phi_3 \propto s^1$ 标度）：

$$\frac{\sigma_{2\to 3}}{\sigma_{2\to 2}} \sim \frac{\kappa^2}{s} \cdot \frac{s}{256\pi^3} \approx \frac{\kappa^2}{256\pi^3}$$

在 Planck 单位中 $\kappa^2 = 32\pi$，比值 $\sim 0.04$，数值验证中 $E=0.1 M_{\text{Pl}}$ 时 $\sigma_{23}/\sigma_{22} \approx 0.023$。

## §7 2→4 散射谱振幅

### 7.1 双重软因子分解

2→4 振幅通过双重软因子分解：

$$M_{2\to 4} \approx \kappa^2 \cdot S^{(1)} \cdot S^{(2)} \cdot M_{2\to 2}$$

截面为：

$$\sigma_{2\to 4} = \frac{1}{3!} \cdot \frac{1}{2s} \int |M_{2\to 4}|^2 \, d\Pi_4$$

对称因子 $1/3!$ 来自末态全同粒子。

### 7.2 截面对比

| 过程 | $E=0.01 M_{\text{Pl}}$ | $E=0.1 M_{\text{Pl}}$ | $E=0.5 M_{\text{Pl}}$ | $E=1.0 M_{\text{Pl}}$ |
|:---:|:---------------------:|:--------------------:|:--------------------:|:--------------------:|
| 2→2 | $6.44$ | $631$ | $1.57\times 10^4$ | $8.71\times 10^3$ |
| 2→3 | $1.53\times 10^{-3}$ | $14.8$ | $6.08\times 10^3$ | $3.70\times 10^3$ |
| 2→4 | $1.02\times 10^{-5}$ | $9.78$ | $8.93\times 10^4$ | $1.51\times 10^5$ |

在 $E \sim 0.5 M_{\text{Pl}}$ 时 2→4 超过 2→2 成为主导过程（软引力子发射的红外增强 + 大相空间）。

## §8 末态粒子谱分布

### 8.1 多重度分布

末态粒子数分布 $P(n)$ 由相空间权重 × 振幅平方确定：

$$P(n) \propto \Phi_n(s) \cdot \kappa^{2(n-2)} \cdot \left(\frac{E_{\text{cm}}}{\Delta\lambda_{\min}}\right)^{2(n-2)}$$

其中红外增强因子 $(\frac{E}{\Delta\lambda_{\min}})^{2(n-2)}$ 补偿软引力子发射的 $\frac{1}{E_{\text{soft}}^2}$ 发散。在 Planck 能标，最概然末态粒子数为 $n=4$。

| 能标 | $\langle n \rangle$ | 主导过程 |
|:----:|:------------------:|:--------:|
| $0.01 M_{\text{Pl}}$ | 2.00 | 2→2 |
| $0.1 M_{\text{Pl}}$ | 2.08 | 2→2 |
| $0.5 M_{\text{Pl}}$ | 4.47 | 2→4 |
| $1.0 M_{\text{Pl}}$ | 5.88 | 2→4 |

### 8.2 软引力子谱

软引力子发射谱的谱表示为：

$$\frac{dN}{dE_{\text{soft}}} \sim \frac{\kappa^2}{\pi^2} \cdot \frac{1}{E_{\text{soft}}} \cdot e^{-E_{\text{soft}}/\Delta\lambda_{\min}}$$

谱间隙 $\Delta\lambda_{\min} = 0.122 M_{\text{Pl}}$ 提供天然红外正则化，无需引入人工红外截止。

### 8.3 谱级联

在 Planck 能标附近，初始 2→N 散射后末态粒子可再次散射，形成谱级联：

$$E_{\text{cm}}^{(0)} \xrightarrow{2\to N_1} E_{\text{cm}}^{(1)} \xrightarrow{2\to N_2} E_{\text{cm}}^{(2)} \xrightarrow{2\to N_3} \cdots$$

数值模拟显示 $E_{\text{cm}} = 1.0 M_{\text{Pl}}$ 时经 4 步级联后能量降至亚 Planck 区间。级联的多重度从 $n=2$ 增长至 $n=4$，体现了谱框架对非微扰多粒子过程的自然描述能力。

### 8.4 物理图像总结

| 能标区间 | 主导过程 | 物理图像 |
|:--------:|:--------|:---------|
| $E \ll 0.01 M_{\text{Pl}}$ | 2→2 | 微扰引力，单引力子交换 |
| $0.01 < E < 0.3 M_{\text{Pl}}$ | 2→2 + 2→3 | 微扰修正，软引力子发射 |
| $0.3 < E < 1.0 M_{\text{Pl}}$ | 2→4 主导 | 多体末态占优，谱级联开始 |
| $E > 1.0 M_{\text{Pl}}$ | UV 压制 | 谱截断 $\lambda_{\max}$ 指数压制 |

## §9 开放问题

1. **高自旋散射振幅**：引力子-费米子散射的 Dirac 谱结构
2. **圈图修正的谱表示**：单圈振幅的谱 Dyson 级数求和
3. **与弦论散射振幅对比**：谱截断与弦论 $1/s$ 软行为的对应关系
4. **N>4 末态的精确相空间采样**：蒙特卡洛谱相空间积分
5. **谱级联的连续谱流方程**：从离散级联到连续谱能流
6. **与 LIGO 随机引力波背景的对接**：普朗克能标散射的 GW 背景谱

## 关联文件

- `src/dynamic_spectrum/planck_scattering_2to2.py` — B1 实现
- `src/dynamic_spectrum/planck_scattering_2ton.py` — B2 实现
- `src/dynamic_spectrum/spectral_numerics.py` — C1 基础框架
- `paperX_graviton_propagator.py` — 谱引力子传播子数值验证
- `notes/00_foundations/spectral_feynman_rules.md` — 谱 Feynman 规则
- `notes/00_foundations/spectral_path_integral.md` — 谱路径积分
