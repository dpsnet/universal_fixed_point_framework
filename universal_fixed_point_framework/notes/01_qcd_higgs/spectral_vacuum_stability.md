# 谱 SM 的真空稳定性

标准模型中 Higgs 势的真空稳定性问题——$\lambda_H$ 在 $10^{10}\text{–}10^{12}\ \text{GeV}$ 附近变为负值——暗示着存在新物理。在谱框架中，谱截断 $\Lambda_{\max} = M_{\text{Pl}}$ 提供自然的 UV 边界条件，从根本上改变了真空稳定性的分析。

## 谱 Higgs 有效势

在谱语言中，Higgs 有效势包含经典项和谱量子修正项：

$$\boxed{V_{\text{eff}}(h) = -\mu^2 h^2 + \lambda_H h^4 + \delta V_{\text{spec}}(h)}.$$

前三项是标准 Higgs 势，第四项 $\delta V_{\text{spec}}(h)$ 是谱量子修正，来源于谱 QFT 中 Higgs 场的自相互作用和 Yukawa 耦合的谱圈图贡献。在谱截断 $\Lambda_{\max}$ 内的单圈近似下：

$$\delta V_{\text{spec}}(h) = \frac{1}{64\pi^2} \sum_i (-1)^{2s_i} (2s_i+1) \, M_i^4(h) \left( \ln\frac{M_i^2(h)}{\Lambda_{\max}^2} - \frac12 \right),$$

其中 $M_i(h)$ 是场依赖的质量本征值，$s_i$ 是自旋，求和遍及 SM 全部粒子（$W, Z, t, h$ 等）。

## 谱截断边界条件

谱 QFT 的自然紫外截断 $\Lambda_{\max} = M_{\text{Pl}}$ 提供了重整化群运行的物理 UV 边界：

$$\boxed{\lambda_H(\Lambda_{\max}) = \lambda_H^0},$$

其中 $\lambda_H^0$ 是谱间隙确定的裸耦合。从 $M_{\text{Pl}}$ 向低能标运行，$\lambda_H$ 的 RG 演化由 $\beta(\lambda_H)$ 函数控制。

## 重整化群运行

$\lambda_H$ 的 $\beta$ 函数在谱 SM 中为：

$$\beta(\lambda_H) = \frac{1}{16\pi^2} \left( 24\lambda_H^2 - 6y_t^4 + \frac{9}{8}g_2^4 + \frac{3}{8}g_1^4 + \frac{3}{4}g_2^2 g_1^2 - 6\lambda_H y_t^2 + \frac{3}{2}\lambda_H g_2^2 + \frac{1}{2}\lambda_H g_1^2 \right) + \mathcal{O}\left((16\pi^2)^{-2}\right).$$

从 $\Lambda_{\max} = M_{\text{Pl}} = 1.22 \times 10^{19}\ \text{GeV}$ 到 $M_Z = 91.19\ \text{GeV}$，使用谱边界条件 $\lambda_H(M_{\text{Pl}}) = \lambda_H^0$ 进行 RG 演化。若 $\lambda_H^0$ 使得 $\lambda_H(M_Z) > 0$，则真空是绝对稳定的；若 $\lambda_H(M_Z) < 0$ 但隧穿寿命大于宇宙年龄，则真空是亚稳态的。

## 准临界性分析

在谱框架中，$\Lambda_{\max}$ 提供了标准 QFT 所缺乏的自然 UV 完备化：

- 标准 QFT 的真空稳定性分析依赖于对 Planck 能标以上新物理的假设，通常需要引入 $B-L$ 对称性、超对称或额外维度来解释 UV 行为。
- 谱 SM 中，$\Lambda_{\max} = M_{\text{Pl}}$ 是谱截断公理 (A5) 的直接推论，不是人为引入的拟合参数。
- 谱边界条件 $\lambda_H(M_{\text{Pl}}) = \lambda_H^0$ 与顶质量 $m_t$ 的精确值共同决定真空类型。

若 $m_t = 172.69\ \text{GeV}$（当前实验中心值），谱 RG 运行显示 $\lambda_H$ 在 $10^{10}\text{–}10^{12}\ \text{GeV}$ 附近趋近于零，恰与标准 QFT 的"准临界性"(quasi-criticality) 一致。谱框架将此行为解释为谱间隙结构的自然结果：$\lambda_H^0$ 由 $A_H$ 的谱隙决定，其在 Planck 能标的取值恰好落在使低能 $\lambda_H(M_Z)$ 接近零的临界轨迹上。

## 要点

谱 SM 以 $\Lambda_{\max} = M_{\text{Pl}}$ 作为物理 UV 边界条件，将真空稳定性从"开放问题"转化为"谱边界条件的可计算结果"。真空稳定性（绝对稳定或亚稳态）完全由谱间隙结构决定，无需引入额外自由度。

---

*摘自 Paper XI §8.7*
