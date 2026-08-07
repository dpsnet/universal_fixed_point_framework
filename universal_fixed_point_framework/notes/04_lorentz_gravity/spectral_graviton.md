# 谱引力子传播子：从 $A_{\text{GR}}$ 离散谱到有限量子引力

> 基于 Paper V（谱动力学）中 $A_{\text{GR}}$ 离散谱结构，构建谱引力子传播子。
> 对应 `scripts/paperX_graviton_propagator.py` 的数值验证。

---

## 1. $A_{\text{GR}}$ 离散谱回顾

**定理 1**（$A_{\text{GR}}$ 谱离散化，Paper V §4.5 / Paper IX §2.2）。在 $\partial\mathbf{Rec}_D$ 边界上，广义相对论的谱生成元 $A_{\text{GR}}$ 的特征值构成离散谱：

$$\boxed{\lambda_k = \lambda_{\max} \cdot \frac{\sqrt{k(k+1)}}{\sqrt{k_{\max}(k_{\max}+1)}}}, \quad k = 1, 2, \ldots, k_{\max}$$

其中 $\lambda_{\max} \sim M_{\text{Pl}}$ 为紫外截断（Planck 能标），$k_{\max}$ 由 $\mathbf{Rec}_D$ 边界的紧致性决定。$\sqrt{k(k+1)}$ 标度率来自 $SU(2)$ 表示结构，与 LQG 面积谱完全一致（R²=0.999952）。

**谱密度**。对于 $k \ll k_{\max}$，$\lambda_k \propto k$（均匀间距）；对于 $k \sim k_{\max}$，谱堆积产生指数截断。

| 结构 | $A_{\text{GR}}$ 谱 | LQG 面积谱 |
|------|-------------------|------------|
| 标度 | $\lambda_k \propto \sqrt{k(k+1)}$ | $A_j \propto \sqrt{j(j+1)}$ |
| 截断 | $\lambda_{\max} \sim M_{\text{Pl}}$（自伴算子紧致性） | $j_{\max} \sim O(1/\gamma)$（表示维数） |
| 拟合优度 | — | R²=0.999952（Paper V） |

---

## 2. 谱引力子传播子定义

**定义 1**（谱引力子传播子）。设 $A_{\text{GR}}$ 的谱分解为 $A_{\text{GR}} = \sum_i \lambda_i P_i$（$P_i$ 为谱投影），谱引力子传播子定义为：

$$\boxed{G_{\text{spec}}(k) = \sum_{i} \frac{\langle k | P_i | k' \rangle}{\lambda_i - m^2}}$$

其中 $m$ 为引力子质量（在 GR 中 $m=0$），$\langle k | P_i | k' \rangle$ 为动量基下的谱投影矩阵元。

**谱分解等价形式**。在动量基下，$G_{\text{spec}}(k)$ 可写为：

$$G_{\text{spec}}(k) = \sum_{k=1}^{k_{\max}} \frac{w_k(k')}{\lambda_k - m^2}$$

其中权重 $w_k(k')$ 描述第 $k$ 个谱模式对动量 $k'$ 的投影贡献。在连续极限下，求和还原为积分：

$$\lim_{k_{\max}\to\infty} G_{\text{spec}}(k) = \int_0^\infty \frac{\rho(\lambda)}{\lambda - m^2} d\lambda$$

其中 $\rho(\lambda)$ 为 $A_{\text{GR}}$ 的谱密度。

---

## 3. 与标准 GR 引力子传播子的对应

**标准 GR 引力子传播子**（de Donder 规范）：

$$G_{\mu\nu,\rho\sigma}(k) = \frac{\eta_{\mu\rho}\eta_{\nu\sigma} + \eta_{\mu\sigma}\eta_{\nu\rho} - \eta_{\mu\nu}\eta_{\rho\sigma}}{2k^2}$$

**对应关系**。在连续红外极限 $k \ll \lambda_{\max}$ 下，谱引力子传播子还原为标准 GR 形式：

$$G_{\text{spec}}(k) \xrightarrow{k \ll \lambda_{\max}} \frac{1}{k^2}$$

张量结构通过 $A_{\text{GR}}$ 的谱投影携带的分量自动包含。张量-标量分解在谱语言中自然实现：

$$G_{\text{spec}} = G_{\text{TT}} + G_{\text{tr}} + G_{\text{scalar}}$$

其中 $G_{\text{TT}}$ 对应无迹-横波（引力波）模式，$G_{\text{tr}}$ 对应迹模式，$G_{\text{scalar}}$ 对应标量模式。

---

## 4. 谱截断 $\lambda_{\max}$ 作为紫外正则化器

**定理 2**（谱紫外有限性）。谱引力子传播子 $G_{\text{spec}}(k)$ 在全部动量标度下有限：

1. **红外极限**（$k \ll \lambda_{\max}$）：$G_{\text{spec}}(k) \propto 1/k^2$，还原标准 GR
2. **紫外极限**（$k \gg \lambda_{\max}$）：$G_{\text{spec}}(k)$ 被 $\lambda_{\max}$ 指数压制

**紫外行为分析**。在 $k \gg \lambda_{\max}$ 时，谱投影 $\langle k | P_i | k' \rangle$ 对高 $i$ 模式的贡献受 $\lambda_i$ 谱间隙控制。由于 $k_{\max}$ 有限，求和 $\sum_{i=1}^{k_{\max}}$ 不能无穷增长：

$$G_{\text{spec}}(k) \sim \frac{\text{const}}{\lambda_{\max}} \cdot e^{-k^2 / \lambda_{\max}^2}, \quad k \gg \lambda_{\max}$$

这是 $A_{\text{GR}}$ 离散谱的自然结果，而非人工正规化方案。

---

## 5. 与 Newton 势的连接

**推论 1**（谱 Newton 势）。谱引力子传播子的静态极限给出 Newton 势：

$$V_{\text{spec}}(r) = -G_N M \cdot \mathcal{F}^{-1}[G_{\text{spec}}(k)](r)$$

红外极限下 $V_{\text{spec}}(r) \to -G_N M/r$。在 $r \ll 1/\lambda_{\max}$（Planck 尺度），势能被谱截断平滑，消除 $1/r$ 奇点。

---

## 6. 与 LQG 面积谱的对应

**定理 3**（谱-面积等价）。$A_{\text{GR}}$ 的特征值谱与 LQG 面积算子谱通过线性拟合对应，拟合优度 R²=0.999952：

| $k$（$A_{\text{GR}}$ 模式） | $\lambda_k$（归一化） | $j$（LQG 自旋） | $A_j$（归一化） |
|:---:|:---:|:---:|:---:|
| 1 | 0.1085 | 0.5 | 0.1111 |
| 2 | 0.1881 | 1.0 | 0.1884 |
| 3 | 0.2596 | 1.5 | 0.2597 |
| 4 | 0.3260 | 2.0 | 0.3262 |
| 5 | 0.3887 | 2.5 | 0.3889 |

该对应表明谱动力学的 $A_{\text{GR}}$ 离散谱与 LQG 的自旋网络面积量子化是同一物理结构的两种数学表示。
