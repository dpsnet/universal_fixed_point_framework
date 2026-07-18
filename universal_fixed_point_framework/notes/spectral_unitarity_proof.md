# S 矩阵幺正性的完整谱证明

本节在谱框架下给出 S 矩阵幺正性的完备证明，将谱 LSZ 公式、谱 Cutkosky 规则和谱光学定理统一为定理 9.1。

## 定理 9.1（谱 S 矩阵幺正性）

谱 S 矩阵 $S_{\text{spec}}$ 满足幺正条件：

$$\boxed{S_{\text{spec}}^\dagger S_{\text{spec}} = I}.$$

### 证明（五步法）

#### 第一步：谱 LSZ 约化与 S 矩阵元的谱表示

由 §9.1 的谱 LSZ 公式，S 矩阵元与谱关联函数的关系为：

$$\langle f | S_{\text{spec}} | i \rangle = \prod_{j=1}^{n_f} \frac{i}{\lambda_j - m^2 + i\varepsilon} \prod_{k=1}^{n_i} \frac{i}{\lambda_k - m^2 + i\varepsilon} \times G_{n_f+n_i}^{\text{spec}}(\lambda_1,\ldots,\lambda_{n_f+n_i})\Bigg|_{\lambda \to m^2}.$$

引入散射振幅 $M_{\text{spec}}$ 的标准分解 $S_{\text{spec}} = I + i T_{\text{spec}}$，其中 $T_{\text{spec}}$ 的矩阵元为：

$$\langle f | T_{\text{spec}} | i \rangle = (2\pi)^4 \delta^{(4)}(P_f - P_i) \cdot \mathcal{M}^{\text{spec}}(i \to f).$$

#### 第二步：谱 Cutkosky 规则与不连续性的态和表示

对 $i \to f$ 前向散射振幅 $\mathcal{M}^{\text{spec}}(i \to i)$，谱 Cutkosky 规则（§9.2）给出其虚部与中间态求和的关系。考虑二到二散射过程 $p_1 p_2 \to p_3 p_4$ 的单圈修正。谱自能图 $\Sigma^{\text{spec}}(s)$ 的不连续性为：

$$\operatorname{Disc} \Sigma^{\text{spec}}(s) = 2i \operatorname{Im} \Sigma^{\text{spec}}(s) = \sum_n \int d\Pi_n^{\text{spec}} \; \langle p_1 p_2 | T_{\text{spec}}^\dagger | n \rangle \langle n | T_{\text{spec}} | p_1 p_2 \rangle,$$

其中中间态求和 $n$ 遍历所有满足能动量守恒的 on-shell 多粒子态，谱相空间 $d\Pi_n^{\text{spec}}$ 为：

$$d\Pi_n^{\text{spec}} = \prod_{i=1}^n \frac{d^3 k_i}{(2\pi)^3 2E_i} \cdot (2\pi)^4 \delta^{(4)}\Bigl(\sum k_i - \sum p\Bigr).$$

#### 第三步：谱光学定理

从谱 Cutkosky 规则直接导出谱光学定理的精确形式（§9.3）。对前向散射 $i \to i$ 有：

$$\boxed{2\operatorname{Im} \mathcal{M}^{\text{spec}}(i \to i) = \sum_n \int d\Pi_n^{\text{spec}} \; |\mathcal{M}^{\text{spec}}(i \to n)|^2}.$$

这一关系等价于 $T_{\text{spec}}$ 的算符恒等式：

$$2\operatorname{Im} T_{\text{spec}} = T_{\text{spec}}^\dagger T_{\text{spec}}.$$

#### 第四步：谱完备性关系

谱光学定理的中间态求和在 $\mathbf{Spec}$ 范畴中具有谱完备性解释。谱中间态集合 $\{|n\rangle\}$ 构成谱 Hilbert 空间 $\mathcal{H}_{\text{spec}}$ 的一组广义正交基。定义谱单位算符的分解：

$$\boxed{I_{\text{spec}} = \sum_n \int d\Pi_n^{\text{spec}} \; |n\rangle \langle n|},$$

其中求和对所有粒子数 $n$ 以及所有 on-shell 动量构型进行。插入 $I_{\text{spec}}$ 到前向散射振幅中给出：

$$\sum_n \int d\Pi_n^{\text{spec}} \; \langle i | T_{\text{spec}}^\dagger | n \rangle \langle n | T_{\text{spec}} | i \rangle = \langle i | T_{\text{spec}}^\dagger T_{\text{spec}} | i \rangle.$$

结合谱光学定理 $2\operatorname{Im} \langle i | T_{\text{spec}} | i \rangle = \langle i | T_{\text{spec}}^\dagger T_{\text{spec}} | i \rangle$ 对所有 $|i\rangle$ 成立，可得算符恒等式：

$$T_{\text{spec}} - T_{\text{spec}}^\dagger = i T_{\text{spec}}^\dagger T_{\text{spec}}.$$

#### 第五步：幺正性的结论

由 $S_{\text{spec}} = I + i T_{\text{spec}}$ 计算：

$$
\begin{aligned}
S_{\text{spec}}^\dagger S_{\text{spec}} &= (I - i T_{\text{spec}}^\dagger)(I + i T_{\text{spec}}) \\
&= I + i(T_{\text{spec}} - T_{\text{spec}}^\dagger) + T_{\text{spec}}^\dagger T_{\text{spec}} \\
&= I - (T_{\text{spec}} - T_{\text{spec}}^\dagger - i T_{\text{spec}}^\dagger T_{\text{spec}}) \\
&= I \quad (\text{由第四步的恒等式}).
\end{aligned}
$$

类似地可验证 $S_{\text{spec}} S_{\text{spec}}^\dagger = I$，从而 $S_{\text{spec}}$ 是幺正算符。$\blacksquare$

## 推论 9.1（谱光学定理的等价性）

定理 9.1 的证明中第四步建立了谱完备性关系 $I_{\text{spec}} = \sum_n \int d\Pi_n^{\text{spec}} \, |n\rangle\langle n|$，该关系是谱框架下 S 矩阵幺正性的直接推论，也与 §9.3 的谱光学定理完全等价。

## 注释

本证明仅依赖于谱 LSZ 公式、谱 Cutkosky 规则和谱光学定理，这些结果已分别在 §9.1–§9.3 中建立并数值验证。因此定理 9.1 是谱 QFT 形式化的逻辑终点——它表明在 $\mathbf{Spec}$ 范畴中，S 矩阵幺正性不是额外假设而是谱关联函数结构的必然推论。

---

*摘自 Paper XI §9.6（定理 9.1）*
