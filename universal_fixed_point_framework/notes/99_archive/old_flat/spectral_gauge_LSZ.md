# 谱规范的 LSZ 公式

规范理论的散射振幅提取需要在 BRST 框架下进行，以确保物理幺正性。谱 BRST 形式建立在 §6 的 BRST 幂零性 $s^2 = 0$ 基础之上。

## 谱 BRST 算符

谱 BRST 算符 $s_{\text{BRST}}$ 在 $\mathbf{Spec}$ 范畴中的显式作用定义为：

$$s_{\text{BRST}} \Phi = [Q_{\text{BRST}}, \Phi]_{\pm},$$

其中 $Q_{\text{BRST}}$ 是谱 BRST 荷（见 §6.5），$[\cdot,\cdot]_{\pm}$ 根据场的 $\mathbb{Z}_2$ 分级取对易子（玻色子）或反对易子（费米子）。谱 BRST 算符满足幂零性：

$$\boxed{s_{\text{BRST}}^2 = 0}.$$

## 谱 BRST 上同调与物理态空间

物理态空间定义为谱 BRST 算符的零阶上同调群：

$$\boxed{\mathcal{H}_{\text{phys}} = \ker s_{\text{BRST}} / \operatorname{im} s_{\text{BRST}} = H_{\text{BRST}}^0(\mathbf{Spec})}.$$

具体而言：
- $\ker s_{\text{BRST}}$：所有 BRST 闭链（BRST-不变态），即满足 $s_{\text{BRST}}|\psi\rangle = 0$ 的态。
- $\operatorname{im} s_{\text{BRST}}$：所有 BRST 边缘态（可写为 $s_{\text{BRST}}|\chi\rangle$ 的态）。

物理态对应于 BRST 闭链模去 BRST 精确项：$|\psi\rangle_{\text{phys}} \in H_{\text{BRST}}^0(\mathbf{Spec})$。

## 规范固定的谱 LSZ 公式

对于规范理论，谱 LSZ 约化公式必须将外线态投影到 BRST 上同调类上。这保证了 S 矩阵元仅依赖于物理自由度，而非物理鬼场和纵向模式自动消去。

规范固定的谱 LSZ 公式为：

$$\boxed{\langle p_1,\ldots,p_n^{\text{out}} | k_1,\ldots,k_m^{\text{in}} \rangle_{\text{phys}} = P_{\text{BRST}} \circ \langle p_1,\ldots,p_n^{\text{out}} | k_1,\ldots,k_m^{\text{in}} \rangle_{\text{spec}}},$$

其中 $P_{\text{BRST}}$ 是从未约化谱 Hilbert 空间到 $H_{\text{BRST}}^0(\mathbf{Spec})$ 的规范投射：

$$P_{\text{BRST}}: \mathcal{H}_{\text{spec}} \longrightarrow H_{\text{BRST}}^0(\mathbf{Spec}).$$

对每个外线态，有对应的 BRST 投射因子：

$$\langle p |_{\text{phys}} = P_{\text{BRST}}^{(p)} \circ \lim_{\lambda_p \to m^2} \frac{i}{\lambda_p - m^2 + i\varepsilon} \int d\lambda \, e^{i\lambda x} G_n^{\text{spec}}(\lambda_1,\ldots,\lambda_n),$$

其中 $P_{\text{BRST}}^{(p)}$ 作用在第 $p$ 个外线上。

## 非物理态的自动退耦

谱 BRST 投射 $P_{\text{BRST}}$ 确保非物理自由度的自动退耦：

- **鬼场**：鬼场 $c(\lambda), \bar{c}(\lambda)$ 的谱关联函数在 BRST 上同调中为零，因为 $c$ 处于 BRST 非平凡表示而 $\bar{c}$ 是 BRST 精确项：$\bar{c} = s_{\text{BRST}} \tilde{c}$。
- **纵向规范模式**：规范场的纵向分量 $A_L^{\mu}(\lambda)$ 在 BRST 闭链空间中与鬼场配对，因此投射后贡献为零。
- **时序鬼场 (Faddeev-Popov 行列式)**：Faddeev-Popov 行列式在谱语言中对应鬼圈求和，BRST 上同调确保其与纵向模式的贡献精确抵消。

### 命题 9.1（谱 BRST 退耦）

对任意包含鬼场或非物理极化状态的谱散射振幅 $\mathcal{M}_{\text{unphys}}$，有：

$$P_{\text{BRST}}(\mathcal{M}_{\text{unphys}}) = 0.$$

**证明**：由于 $H_{\text{BRST}}^0(\mathbf{Spec})$ 仅包含 BRST 不变的规范单态，任何含鬼场量子数的态在 $H_{\text{BRST}}^0(\mathbf{Spec})$ 中的投影为零。

## Yang-Mills 理论的显式形式

对 $SU(N)$ Yang-Mills 理论，谱 BRST 协变的 LSZ 公式取以下显式形式。设规范场 $A_\mu^a(\lambda)$、鬼场 $c^a(\lambda)$、反鬼场 $\bar{c}^a(\lambda)$、物质场 $\psi_i(\lambda)$。谱关联函数为：

$$G_{n_g,n_f,n_{\bar{c}},n_c}^{\text{spec}} = \langle 0 | T A_{\mu_1}^{a_1}(\lambda_1) \cdots \psi_{i_1}(\lambda_{i_1}) \cdots \bar{c}^{b_1}(\mu_1) \cdots c^{c_1}(\nu_1) \cdots | 0 \rangle.$$

物理 S 矩阵元从 $G^{\text{spec}}$ 通过以下步骤提取：

1. **谱 LSZ 约化（极点提取）**：对每个外线施加：
   $$\prod_{\text{外线}} \frac{i}{\lambda - m^2 + i\varepsilon} \; G^{\text{spec}} \;\Bigg|_{\lambda \to m^2}.$$

2. **极化与 BRST 投射组合**：对每个规范玻色子外线，将极化矢量 $\varepsilon_\mu^{(r)}(p)$ 与 BRST 投射组合：
   $$\mathcal{M}_{\text{phys}} = P_{\text{BRST}} \circ \sum_{\{r\}} \prod_{\text{规范玻色子}} \varepsilon_{\mu_r}^{(r)}(p_r) \cdot \prod_{\text{旋量}} \bar{u}(p) / v(p) \cdot \text{谱 LSZ 余项}.$$

3. **物理极化求和**：
   $$\sum_{\text{物理极化}} \varepsilon_\mu^{(r)}(p) \varepsilon_\nu^{(r)*}(p) = -g_{\mu\nu} + \frac{p_\mu n_\nu + p_\nu n_\mu}{p\cdot n},$$
   在 BRST 上同调中与鬼场贡献互补，确保 $P_{\text{BRST}}$ 投射后总结果与规范无关。

---

*摘自 Paper XI §9.5*
