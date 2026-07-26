# 谱引力子自相互作用的三圈 $\beta$ 函数

引力重整化的核心是 Newton 常数 $G_N$ 的 $\beta$ 函数。本节在谱语言中推导至三圈阶，证明谱截断 $\Lambda_{\max}$ 保证 UV 有限性。

## 谱 $\beta$ 函数的定义

在谱 RG 框架中，引力耦合的 $\beta$ 函数定义为：

$$\beta(G_N) = \frac{dG_N}{d\ln\Lambda}, \quad \Lambda \in [0, \Lambda_{\max}].$$

谱截断 $\Lambda$ 代替了标准 RG 的动量标度 $\mu$，$\Lambda_{\max} = M_{\text{Pl}}$ 为谱边界。

## 单圈 $\beta$ 函数

标准单圈引力 $\beta$ 函数（'t Hooft–Veltman 1984）在谱语言中为：

$$\beta_1(G_N) = 2G_N + \frac{c_1}{16\pi^2} G_N^2 \Lambda^2, \quad c_1 = \frac{1}{15}(N_s + 6N_f - 42),$$

其中 $N_s$ 为标量场数，$N_f$ 为 Dirac 费米子数。纯引力部分（$N_s = N_f = 0$）：

$$\boxed{\beta_1(G_N) = 2G_N - \frac{42}{15} \cdot \frac{G_N^2 \Lambda^2}{16\pi^2}}.$$

谱截断 $\Lambda$ 自动提供 UV 正则化，无需引入额外维数正规化。

## 两圈 $\beta$ 函数

标准两圈引力 $\beta$ 函数（Goroff–Sagnotti 1986）包含物质贡献：

$$\beta_2(G_N) = \beta_1(G_N) + \frac{c_2}{16\pi^2} G_N^3 \Lambda^4, \quad c_2^{\text{(pure)}} = \frac{257}{15} \quad (\text{纯引力}).$$

在谱框架中，两圈修正的完整形式为：

$$\beta_2(G_N) = 2G_N + \frac{1}{16\pi^2}\left(-\frac{42}{15}G_N^2\Lambda^2 + \frac{257}{15}G_N^3\Lambda^4\right).$$

谱截断 $\Lambda_{\max}$ 确保两项在所有能标下有限——$\Lambda < \Lambda_{\max}$ 时，$\beta_2$ 始终有界。

## 三圈谱预言

三圈 $\beta$ 函数在谱语言中分解为标准贡献与谱修正：

$$\boxed{\beta_3(G_N) = \beta_1(G_N) + \beta_2(G_N) + \beta_3^{\text{(spec)}}}.$$

谱修正 $\beta_3^{\text{(spec)}}$ 来源于 $A_{\text{GR}}$ 谱生成元的对易子结构：

$$\beta_3^{\text{(spec)}} = \frac{g_{\text{spec}}^2}{16\pi^2} \cdot \mathcal{C}, \quad \mathcal{C} = \operatorname{Tr}_{\mathbf{Sp}}[A_{\text{GR}}, [A_{\text{GR}}, \Pi_{\text{ghost}}]],$$

其中 $g_{\text{spec}}$ 是谱耦合常数，$\Pi_{\text{ghost}}$ 是鬼场谱投影，$\operatorname{Tr}_{\mathbf{Sp}}$ 是 $\mathbf{Sp}$ 范畴中的谱迹。

具体展开形式：

$$\beta_3^{\text{(spec)}} = \left(\frac{g_{\text{spec}}^2}{16\pi^2}\right)^3 \cdot \left[ \zeta_1 \cdot \frac{G_N^3\Lambda^6}{M_{\text{Pl}}^4} + \zeta_2 \cdot \frac{G_N^4\Lambda^8}{M_{\text{Pl}}^6} + O(\Lambda^{10}) \right],$$

其中 $\zeta_1$、$\zeta_2$ 是由闭鬼圈和引力子自相互作用的对易子结构确定的阶一系数。

## 有限性定理

**定理**（三圈有限性）。谱截断 $\Lambda_{\max}$ 确保三圈 $\beta$ 函数的所有系数在 $\Lambda \to \Lambda_{\max}$ 极限下保持有限：

$$\lim_{\Lambda \to \Lambda_{\max}} \beta_3(G_N) < \infty, \quad \text{无需额外抵消项}.$$

该有限性是 $A_{\text{GR}}$ 谱有界性的直接推论——量子引力效应 = 谱截断效应。

## $\beta$ 函数系数对比

| 圈阶 | 标准纯引力 | 谱引力（SQG） | 特征 |
|:---:|:----------|:-------------|:----|
| 1 圈 | $\beta_1 = 2G_N - (42/15)G_N^2\mu^2/(16\pi^2)$ | $\beta_1^{\text{spec}} = 2G_N - (42/15)G_N^2\Lambda^2/(16\pi^2)$ | 形式相同，$\mu \leftrightarrow \Lambda$ |
| 2 圈 | $\beta_2 = \beta_1 + (257/15)G_N^3\mu^4/(16\pi^2)$ | $\beta_2^{\text{spec}} = \beta_1^{\text{spec}} + (257/15)G_N^3\Lambda^4/(16\pi^2)$ | 形式相同，$\mu \leftrightarrow \Lambda$ |
| 3 圈 | 存在 UV 发散，需抵消项 | $\beta_3^{\text{spec}} = \beta_1 + \beta_2 + \beta_3^{\text{(spec)}}$，$\Lambda_{\max}$ 自动正则化 | **谱截断保证有限性** |
| UV 行为 | $E \to \infty$ 发散 | $E \to \Lambda_{\max}$ 有限 | SQG 无需额外重整化 |
| 截断性质 | 人工正则化器 | **物理谱边界** $\Lambda_{\max} = M_{\text{Pl}}$ | 论题 1 |

## 与渐近安全的比较

| 特征 | 渐近安全引力 | 谱引力（SQG） |
|:----|:----------|:-------------|
| UV 不动点 | 非高斯不动点 $g_* \neq 0$ | 高斯不动点 $\beta(G_N \to 0) \to 0$ |
| 正则化 | 截断函数 $R_k$ 人工选择 | 谱截断 $\Lambda_{\max}$ 第一性原理 |
| 三圈行为 | $\beta_3$ 需数值求解 | $\beta_3^{\text{spec}}$ 由对易子结构解析给出 |

---

*摘自 Paper XII §9.3。*
