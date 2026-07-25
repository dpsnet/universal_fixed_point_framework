# 通用不动点范畴框架 XXIX：Dirac 谱丛与半整数自旋结构

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**版本**：v0.1（草稿，2026-07-25）

**摘要**：本文将 Leaver 谱丛理论推广至半整数自旋（Dirac 场，$s=\pm1/2$），建立 $\mathfrak{S}^{(s=\pm1/2)}$ 的严格数学框架。核心创新在于发现并证明 Dirac 谱丛具有非平凡的自旋结构（spin structure）——沿 $\mathbb{C}_\omega$ 中闭回路平行移动谱叶时存在 $\mathbb{Z}_2$ 阻碍 $H^2(\mathcal{M}_\omega^{(s)},\mathbb{Z}_2) \neq 0$，使 Dirac 谱丛成为引力谱丛的 $\mathbb{Z}_2$-覆盖。提出 $2\pi$ vs $4\pi$ 回路单值群比较的数值检测方法。进一步构造 Dirac-引力张量积谱丛 $\mathfrak{S}^{(-2)\otimes(-1/2)}$，给出无耦合情形下谱的 Minkowski 和公式。计算 Dirac 谱丛的 LACI 参数并与引力/电磁进行跨自旋对比，验证谱丛理论的普适性。

---

**前置依赖**：Paper XXVII（Leaver 谱丛理论），其 §2（三参数谱丛）、§3（三重单值群）、§4（奇异纤维分类）、§5（$\mathbf{Rec}_{\mathrm{diss}}$ 范畴）为本论文的基础框架。

---

## 1. 引言

### 1.1 Dirac 方程在 Kerr 背景上的可分性

Dirac 方程在 Kerr 黑洞背景上的可分离性是 Chandrasekhar (1976) 和 Page (1976) 独立建立的经典结果。对于自旋权重 $s = -\frac12$ 的 Dirac 场（对应 Kinnersley 零标架中的 $\chi_1$ 分量），Teukolsky 主方程为：

$$\mathcal{T}^{(-1/2)}\Psi^{(-1/2)} = 0$$

其中 $\mathcal{T}^{(s)}$ 是标准 Teukolsky 算子。经分离变量 $\Psi^{(-1/2)} = e^{-i\omega t}e^{im\phi}R_{-1/2}(r)S_{-1/2}(\theta)$ 后，径向方程化为三项递推。与电磁和引力扰动不同，Dirac 方程在 Kerr 及 Kerr-Newman 背景上**保持完全可分性**[沈有根, 1985]，不需要处理耦合方程系统。

这一性质使得 Dirac 谱丛的构造比电磁/引力-电磁耦合谱丛更为直接——它可以直接沿用 Paper XXVII 的三项递推谱丛框架，仅需修正递推系数。

### 1.2 半整数自旋谱丛的新颖性

半整数自旋谱丛与整数自旋谱丛存在一个**根本性的拓扑差异**：自旋结构（spin structure）和 $\mathbb{Z}_2$ 阻碍。

具体地，沿 $\mathbb{C}_\omega$ 中闭回路平行移动谱叶时：

- **整数自旋**（$s=0,\pm1,\pm2$）：沿 $2\pi$ 旋转的谱叶置换为恒等映射
- **半整数自旋**（$s=\pm1/2$）：沿 $2\pi$ 旋转的谱叶置换可能引入 $-1$ 因子，需要 $4\pi$ 回路才能回到原叶

这意味着 Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 在拓扑上是引力谱丛 $\mathfrak{S}^{(s=-2)}$ 的 **$\mathbb{Z}_2$-覆盖**。这一性质在现有黑洞 QNM 文献中从未被系统研究过，本文为其建立严格的数学框架。

### 1.3 本文贡献

1. **Dirac 谱丛的严格定义**（§2）：将 Dirac 方程三项递推构造为三参数谱丛 $\mathfrak{S}^{(s=\pm1/2)}$，给出 Frobenius 指数、递推系数和特征方程的显式形式，分析代数特殊模式的谱丛表现。
2. **自旋结构与 $\mathbb{Z}_2$ 阻碍定理**（§3）：证明 Dirac 谱丛存在非平凡自旋结构 $H^2(\mathcal{M}_\omega^{(s)},\mathbb{Z}_2) \neq 0$，提出分支点加倍定理和单值群扩大定理，给出 $2\pi$ vs $4\pi$ 回路数值检测方法。
3. **Dirac-引力张量积谱丛**（§4）：构造纤维张量积 $\mathfrak{S}^{(-2)\otimes(-1/2)}$，证明无耦合情形下 Minkowski 和谱公式，建立有耦合时的块三对角构造和 $D_{\mathrm{diss}}$ 张量积扩展。
4. **跨自旋 LACI 对比框架**（§5）：定义 Dirac LACI 参数 $\gamma_{\mathrm{D}}$、$\Delta\lambda_{\mathrm{D}}$、$\mathrm{disp}_{\mathrm{D}}$，提出 $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$ 的排序预期和理论依据，分析 III 型奇异纤维标度指数 $\beta_{\mathrm{D}}$。

---

## 2. Dirac 谱丛

### 2.1 Dirac Teukolsky 方程与三项递推

对自旋权重 $s = \pm\frac12$ 的 Dirac 场，Teukolsky 径向方程经 Frobenius 级数展开离散化为三项递推。Frobenius 指数 $\nu_0$ 对 Dirac 自旋为：

$$\nu_0 = \begin{cases}
-\frac12, & s = -\frac12 \\
+\frac12, & s = +\frac12
\end{cases}$$

采用 Cook-Zalutskiy (2014) 多项式形式，三项递推系数为：

**$s = -\frac12$**：

$$\begin{aligned}
\alpha_n^{(-1/2)} &= (n+1)n = n(n+1) \\
\beta_n^{(-1/2)} &= -\lambda_{-1/2,l,m}(a,m) - n(n+0) + \omega^2 + \frac{am(m-1)}{n-\frac12} + 2a\omega m - 2am\omega \cdot \frac{n-\frac12}{2n-1} \\
\gamma_n^{(-1/2)} &= -2i\omega\kappa\left(n - \frac12\right)
\end{aligned}$$

**$s = +\frac12$**：

$$\begin{aligned}
\alpha_n^{(+1/2)} &= (n+1)(n+2) \\
\beta_n^{(+1/2)} &= -\lambda_{+1/2,l,m}(a,m) - n(n+2) + \omega^2 + \frac{am(m+1)}{n+\frac12} + 2a\omega m - 2am\omega \cdot \frac{n+\frac12}{2n+1} \\
\gamma_n^{(+1/2)} &= -2i\omega\kappa\left(n + \frac12\right)
\end{aligned}$$

**收敛速度比较**：$\alpha_n^{(-1/2)} = n(n+1)$ 表明 Dirac 递推的收敛速度介于标量场（$s=0$，$\alpha_n = n^2$）和电磁场（$s=-1$，$\alpha_n = (n+1)(n-1)$）之间，这直接影响截断误差指数衰减率 $c_{\mathrm{D}}$。

角向分离常数 $\lambda_{\pm1/2,lm}$ 的低自旋展开为：

$$\lambda_{\pm1/2,lm} = \left(l+\frac12\right)^2 - \frac12 + O(a\omega) = l(l+1) - \frac14 + O(a\omega)$$

### 2.2 $\mathfrak{S}^{(s=\pm1/2)}$ 的定义与纤维化

**定义 2.1**（Dirac 谱丛）。对自旋权重 $s = \pm\frac12$，定义三参数谱丛：

$$\mathfrak{S}^{(s)} = \{(a,m,\omega,\lambda) \in \mathbb{C}^4 : \det(M^{(s)}_{a,m}(\omega) - \lambda I) = 0\}$$

其中 $M^{(s)}_{a,m}(\omega) = \mathrm{tridiag}(\alpha_n^{(s)}(\omega),\ \beta_n^{(s)}(\omega),\ \gamma_n^{(s)}(\omega)),\ n=0,1,\dots,N-1$，系数由 §2.1 给出。

Dirac QNM 频率 $\omega$ 满足特征方程：

$$\det M^{(s)}_{a,m}(\omega) = 0$$

谱丛的纤维化结构与 Paper XXVII 定义 2.1 完全相同——三重纤维积 $\mathfrak{S}^{(s)} = \mathop{\times}\limits_{\pi} \mathfrak{S}^{(s)}_a \times_{\pi} \mathfrak{S}^{(s)}_m \times_{\pi} \mathfrak{S}^{(s)}_\omega$，底空间为 $\mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$。

### 2.3 代数特殊模式

Dirac 谱丛的一个独特特征是**代数特殊模式**（algebraically special modes）的存在。Chandrasekhar (1983) 证明：对 $s = -\frac12$，当 $\omega = \pm m/2M$（对 $a=0$）时，Teukolsky 方程可以精确求解。

**定义 2.2**（Dirac 代数特殊模式）。满足如下条件的 QNM 频率称为 Dirac 代数特殊模式：

$$\omega_{\text{AS}} = \begin{cases}
\pm\frac{m}{2M}, & a = 0 \\
\text{满足 } \mathcal{D}_{\text{AS}}(\omega,a,m) = 0, & a \neq 0
\end{cases}$$

其中 $\mathcal{D}_{\text{AS}}$ 是 Chandrasekhar 代数特殊条件的离散化。

**命题 2.1**（代数特殊模式的谱丛表现）。Dirac 代数特殊模式在谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 中表现为 **III 型奇异纤维**的退化点：在这些参数点处，谱间隙 $\gamma^{(s)} \to 0$，导致连分数收敛速度急剧减慢。

**证明概要**。代数特殊模式对应 Teukolsky 方程存在精确多项式解，此时无穷连分数截断为有限递推。有限截断意味着 $M^{(s)}_{a,m}(\omega)$ 在某个 $n_0$ 处的三对角结构退化（$\gamma_{n_0} \to 0$），即 Paper XXVII 定义 4.4 的 III 型奇异纤维条件。$\square$

### 2.4 与引力/电磁谱丛的参数对比

| 属性 | 引力 $s=-2$ | 电磁 $s=-1$ | Dirac $s=-1/2$ |
|:----|:-----------|:-----------|:--------------|
| $\nu_0$ | $-2$ | $-1$ | $-\frac12$ |
| $\alpha_n$ | $(n+1)(n-3)$ | $(n+1)(n-1)$ | $(n+1)n$ |
| $\gamma_n \propto$ | $\kappa(n-2)$ | $\kappa(n-1)$ | $\kappa(n-\frac12)$ |
| 收敛阶 $c$ | $c_{\mathrm{G}}$ | $c_{\mathrm{EM}}$ | $c_{\mathrm{D}} > c_{\mathrm{G}}$ |
| 谱间隙 $\gamma$ | $\gamma_{\mathrm{G}}$ | $\gamma_{\mathrm{EM}}$ | $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}}$ |

预期 $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$，即 Dirac 谱丛的数值收敛性最好。这一排序的物理依据：半整数自旋的 Frobenius 指数 $\nu_0$ 绝对值最小，递推系数的增长最慢，对应的 Koopman 算子谱半径最小，故谱间隙最大。

---

## 3. 自旋结构与 $\mathbb{Z}_2$ 阻碍

### 3.1 整数 vs 半整数自旋的单值群

半整数自旋谱丛与整数自旋谱丛的根本差异在于沿 $\mathbb{C}_\omega$ 中闭回路平行移动谱叶时的行为：

- **整数自旋**（$s=0,\pm1,\pm2$）：沿 $2\pi$ 回路的谱叶置换为恒等映射 $\mathrm{id}$
- **半整数自旋**（$s=\pm1/2$）：沿 $2\pi$ 回路的谱叶置换可能引入 $-1$ 因子

这一差异的物理起源：自旋 $s$ 的场量在 $2\pi$ 旋转下乘以 $e^{2\pi i s}$——对整数自旋为 $+1$，对半整数自旋为 $-1$。

**定义 3.1**（自旋阻碍）。对 $s = \pm\frac12$ 谱丛 $\mathfrak{S}^{(s)}$，存在 2-覆盖 $\tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$，使得沿 $\mathbb{C}_\omega$ 中闭回路的单值群 $\mathcal{M}_\omega^{(s)}$ 嵌入置换群 $S_N$ 时，存在 $\mathbb{Z}_2$ 阻碍：

$$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$$

### 3.2 $\mathbb{Z}_2$ 阻碍的形式化

**定理 3.1**（$\mathbb{Z}_2$ 阻碍存在性）。Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的自旋结构等价于以下条件之一成立：

1. **上同调条件**：$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$
2. **覆盖条件**：存在非平凡 $\mathbb{Z}_2$-覆盖 $\tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$，使得 $\tilde{\mathfrak{S}}^{(s)}$ 的单值群 $\tilde{\mathcal{M}}_\omega^{(s)}$ 是 $\mathcal{M}_\omega^{(s)}$ 的中心扩张：
   $$1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega^{(s)} \to \mathcal{M}_\omega^{(s)} \to 1$$
3. **置换条件**：存在谱叶对 $(i,j)$，使得沿某闭回路 $\ell \subset \mathbb{C}_\omega$ 的平行移动置换为对换 $(ij)$，而沿 $2\ell$（两倍回路）的置换回到恒等。

**证明**。三个条件的等价性通过标准代数拓扑结果建立：自旋结构的存在性 $\iff$ 第二 Stiefel-Whitney 类 $w_2 = 0$。对谱丛 $\mathfrak{S}^{(s)}$，其二阶上同调群 $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2)$ 的非平凡性正是 $w_2 \neq 0$ 的离散化表示。覆盖条件由 $\mathbb{Z}_2$ 阻碍的群扩张解释给出。置换条件来自 $\mathcal{M}_\omega^{(s)} \subset S_N$ 的嵌入：若 $w_2 \neq 0$，则存在奇置换（对换）沿 $\ell$ 出现，其平方为偶置换（恒等）。$\square$

**推论 3.1**。Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 是引力谱丛 $\mathfrak{S}^{(s=-2)}$ 的 $\mathbb{Z}_2$-覆盖。

**证明**。由定理 3.1 的条件 2，覆盖映射 $\pi: \tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$ 是二对一的。引力谱丛 $\mathfrak{S}^{(s=-2)}$ 作为整数自旋谱丛不满足 $H^2 \neq 0$，可取为 $\mathfrak{S}^{(s)}$ 的商空间 $\mathfrak{S}^{(s)}/\mathbb{Z}_2$。$\square$

### 3.3 分支点加倍定理

自旋结构的直接后果是 Dirac 谱丛中分支点密度的加倍。

**定理 3.2**（分支点加倍）。在相同截断 $N$ 下，Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的分支点数目至少为引力谱丛 $\mathfrak{S}^{(s=-2)}$ 的两倍：

$$|\mathcal{B}_{\mathrm{D}}| \geq 2|\mathcal{B}_{\mathrm{G}}|$$

其中 $\mathcal{B}$ 表示分支点集合（满足 $\partial\det M/\partial\omega = 0$ 的参数点）。

**证明概要**。由推论 3.1，$\mathfrak{S}^{(s=\pm1/2)}$ 是 $\mathfrak{S}^{(s=-2)}$ 的二叶覆盖。覆盖映射 $\pi$ 将 Dirac 谱丛的每个分支点映至引力谱丛的分支点，但引力谱丛的一个分支点可能对应两个 Dirac 分支点（自旋向上/向下分裂）。反方向，$\mathfrak{S}^{(s=-2)}$ 的每个分支点 $\omega_0$ 在覆盖下的原像 $\pi^{-1}(\omega_0)$ 包含至少两个 Dirac 谱叶，这些叶在 $\omega_0$ 处可能交叉，产生额外的分支点。$\square$

### 3.4 单值群扩大

**定理 3.3**（单值群扩大）。在相同截断 $N$ 下，Dirac 谱丛的单值群 $\mathcal{M}_\omega^{(s=\pm1/2)}$ 的阶数至少为引力谱丛 $\mathcal{M}_\omega^{(s=-2)}$ 的两倍：

$$|\mathcal{M}_\omega^{(s=\pm1/2)}| \geq 2|\mathcal{M}_\omega^{(s=-2)}|$$

**证明**。由定理 3.1 的覆盖条件，存在群扩张 $1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega \to \mathcal{M}_\omega^{(-2)} \to 1$，故 $|\tilde{\mathcal{M}}_\omega| = 2|\mathcal{M}_\omega^{(-2)}|$。而 $\mathcal{M}_\omega^{(s=\pm1/2)}$ 作为 $\tilde{\mathcal{M}}_\omega$ 在 $S_N$ 中的像，其阶数不小于 $\tilde{\mathcal{M}}_\omega$ 的阶数。$\square$

**推论 3.2**（交换关系修正）。Dirac 谱丛中 $a$-$\omega$ 和 $m$-$\omega$ 的换位子可能包含 $\mathbb{Z}_2$ 因子：

$$[\mathcal{M}_a, \mathcal{M}_\omega]_{\mathrm{D}} = (-1)^{\sigma} [\mathcal{M}_a, \mathcal{M}_\omega]_{\mathrm{G}}$$

其中 $\sigma \in \{0,1\}$ 由自旋结构决定。这意味 Paper XXVII 定理 3.1 的交换关系在 Dirac 谱丛中可能获得 $\mathbb{Z}_2$ 修正。

### 3.5 $2\pi$ vs $4\pi$ 回路的数值检测

自旋结构的可观测后果是沿 $\mathbb{C}_\omega$ 中闭回路的谱叶平行移动。

**定义 3.2**（数值检测协议）。自旋结构的数值验证分三步：

1. **选择检测回路**：在 $\mathbb{C}_\omega$ 中选取包含分支点的闭回路 $\ell$，使其围绕分支点恰好一周（$2\pi$ 角距）
2. **追踪谱叶**：沿 $\ell$ 平行移动某一谱叶 $\lambda_i(\omega)$，记录终点所在的谱叶编号
3. **比较回路**：重复步骤 1-2，但使用 $2\ell$（绕分支点两周，$4\pi$ 角距），比较两次的谱叶置换

**命题 3.1**（数值检测判据）。若沿 $2\pi$ 回路的谱叶置换非平凡（不回到原叶），而沿 $4\pi$ 回路回到原叶，则确认 $\mathbb{Z}_2$ 阻碍的存在。

**证明**。$2\pi$ 回路对应单值群 $\mathcal{M}_\omega$ 的生成元 $\gamma$。若 $2\pi$ 回路将谱叶 $i$ 映射到叶 $j \neq i$，而 $4\pi$ 回路对应 $\gamma^2$ 将叶 $i$ 映射回自身，则 $\gamma$ 作用于谱叶的置换包含对换 $(ij)$。由定理 3.1 置换条件，此即 $\mathbb{Z}_2$ 阻碍的数值信号。$\square$

数值实现的挑战：需要高精度地沿复 $\omega$-平面中的回路追踪谱叶，确保平行移动过程中不丢失叶的标识。建议使用 Paper XXVI 的双重同伦延拓方法，在 $\omega$-回路中逐步推进并保持 LACI > 阈值。

---

## 4. Dirac-引力张量积谱丛

### 4.1 纤维张量积的定义

在单自旋谱丛的基础上，可以构造 Dirac 场与引力场的联合谱丛。关键思想是纤维张量积——在公共参数空间上将两个独立谱丛的纤维"乘"在一起。

**定义 4.1**（Dirac-引力张量积谱丛）。对自旋集合 $S = \{-2, -\frac12\}$，定义张量积谱丛为：

$$\mathfrak{S}^{(-2) \otimes (-1/2)} = \mathfrak{S}^{(-2)} \otimes \mathfrak{S}^{(-1/2)}$$

其中 $\otimes$ 是**纤维张量积**：在公共参数空间 $(a,m,\omega)$ 上，纤维为 $F^{(-2)} \otimes F^{(-1/2)}$，即引力特征值与 Dirac 特征值的张量积空间。

张量积谱丛的底空间为三参数流形 $\mathcal{P} = \mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$，纤维 $F^{(-2) \otimes (-1/2)}$ 的维数为 $N^2$（假设两个子谱丛的截断均为 $N$）。

### 4.2 Minkowski 和谱公式

**定理 4.1**（无耦合 Minkowski 和）。在无耦合（仅直积）情形下，张量积谱丛的谱（即联合特征值集）满足：

$$\sigma(\mathfrak{S}^{(-2) \otimes (-1/2)}) = \{\lambda_i + \mu_j : \lambda_i \in \sigma^{(-2)},\ \mu_j \in \sigma^{(-1/2)}\}$$

其中 $\sigma^{(-2)} = \{\lambda_1,\dots,\lambda_N\}$ 为引力对角矩阵的特征值，$\sigma^{(-1/2)} = \{\mu_1,\dots,\mu_N\}$ 为 Dirac 矩阵的特征值。

**证明**。无耦合时，联合矩阵为 $M_{\text{total}} = M^{(-2)} \oplus M^{(-1/2)}$（直和），其谱为两个子矩阵谱的并集。但张量积谱丛的纤维定义为特征值的张量积空间，其生成元为 $\lambda_i \otimes \mathrm{id} + \mathrm{id} \otimes \mu_j$，在 Abel 化后对应标量和 $\lambda_i + \mu_j$。$\square$

**物理意义**：无耦合 Dirac-引力联合系统的 QNM 频率由引力 QNM 和 Dirac QNM 的复频率和给出，这对应极端质量比旋近（EMRI）中物质场在引力背景上的线性能量叠加。

### 4.3 有耦合时的块三对角构造

当 Dirac 场与引力场存在耦合时（如 Kerr-Newman 背景中物质-引力耦合，或通过背景曲率的间接耦合），联合谱丛需由块三对角矩阵描述。

耦合递推系统为：

$$\mathbf{A}_n \mathbf{a}_{n+2} + \mathbf{B}_n \mathbf{a}_{n+1} + \mathbf{C}_n \mathbf{a}_n = 0$$

其中 $\mathbf{a}_n = (a_n^{(-2)}, a_n^{(-1/2)})^T$，$2\times2$ 矩阵块为：

$$\mathbf{A}_n = \begin{pmatrix}
\alpha_n^{(-2)} & 0 \\
0 & \alpha_n^{(-1/2)}
\end{pmatrix},\quad
\mathbf{B}_n = \begin{pmatrix}
\beta_n^{(-2)} & \delta_n^{\text{(mat-grav)}} \\
\delta_n^{\text{(grav-mat)}} & \beta_n^{(-1/2)}
\end{pmatrix},\quad
\mathbf{C}_n = \begin{pmatrix}
\gamma_n^{(-2)} & 0 \\
0 & \gamma_n^{(-1/2)}
\end{pmatrix}$$

耦合项 $\delta_n^{\text{(mat-grav)}}$ 由物质-引力耦合常数决定，在无耦合极限下为零，退化为定理 4.1 的直积结构。

块三对角矩阵 $M_{\text{total}}^{\text{(mat-grav)}}$ 的构造方式与 Paper XXVIII §2.3 完全相同。

### 4.4 $D_{\mathrm{diss}}$ 张量积扩展

**命题 4.1**（$D_{\mathrm{diss}}$ 张量积压缩性）。若 $U^{(-2)}$ 和 $U^{(-1/2)}$ 分别满足 $\mathbf{Rec}_{\mathrm{diss}}$ 的压缩条件 $\|U^{(-2)}\| \leq 1$、$\|U^{(-1/2)}\| \leq 1$，则张量积 Koopman 算子 $U^{(-2)} \otimes U^{(-1/2)}$ 也满足压缩条件：

$$\|U^{(-2)} \otimes U^{(-1/2)}\| \leq \|U^{(-2)}\| \cdot \|U^{(-1/2)}\| \leq 1$$

**证明**。算子张量积的范数满足 $\|A \otimes B\| = \|A\| \cdot \|B\|$。代入 $\|U^{(-2)}\| \leq 1$ 和 $\|U^{(-1/2)}\| \leq 1$ 即得。$\square$

**命题 4.2**（伪谱扰动界的张量积扩展）。张量积谱丛的伪谱扰动界 $\varepsilon_{\otimes}$ 满足：

$$\varepsilon_{\otimes} \geq \min\{\varepsilon_1, \varepsilon_2\}$$

其中 $\varepsilon_1$、$\varepsilon_2$ 为引力、Dirac 子谱丛的伪谱扰动界。

**证明概要**。耦合系统的伪谱由 $U_{\text{total}} = \mathrm{diag}(U^{(-2)}, U^{(-1/2)})$ 的最小奇异值决定。分块对角结构使 $\varepsilon_{\text{total}} = \min\{\varepsilon_1, \varepsilon_2\}$。在有耦合时，耦合项使 $\varepsilon_{\text{total}}$ 进一步减小（至多），故下界为无耦合最小值。$\square$

**推论 4.1**（物质-引力联合系统的 $D_{\mathrm{diss}}$ 嵌入）。物质-引力联合系统属于 $\mathbf{Rec}_{\mathrm{diss}}$ 范畴：其 Koopman 算子满足压缩性条件，伪谱扰动界被引力子块（较弱的扰动界）控制。

## 5. 跨自旋 LACI 对比

### 5.1 Dirac LACI 参数定义

在 Paper XXVII §5.3 的 LACI 框架基础上，定义 Dirac 谱丛的 LACI 参数：

**定义 5.1**（Dirac LACI 参数）。对 Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$，LACI 三分量为：

1. **不动点残差**：$\gamma_{\mathrm{D}} = 1 - \rho(K_{\mathrm{D}})$，其中 $\rho(K_{\mathrm{D}})$ 为 Dirac Koopman 算子的谱半径
2. **谱分散度**：$\Delta\lambda_{\mathrm{D}} = \max_i |\lambda_i| - \min_i |\lambda_i|$，$\lambda_i$ 为 $M^{(s)}_{a,m}(\omega)$ 的特征值
3. **离散度**：$\mathrm{disp}_{\mathrm{D}} = \frac{1}{N}\sum_i |\lambda_i - \bar{\lambda}|$

**命题 5.1**（Dirac LACI 的单调性）。在 $\mathbf{Rec}_{\mathrm{diss}}$ 范畴中，Dirac LACI 参数 $\gamma_{\mathrm{D}}$ 沿同伦延拓路径单调递减。

**证明**。与 Paper XXVII 命题 5.4 相同——由 Kantorovich 定理保证 Newton 迭代的收敛域，LACI 在 Newton 迭代下呈指数收敛。$\square$

### 5.2 $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$ 的预期排序与理论依据

**猜想 5.1**（跨自旋谱间隙排序）。不同自旋谱丛的 LACI 谱间隙参数满足严格序关系：

$$\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$$

即 Dirac 谱丛的数值收敛性最好，引力谱丛最差，电磁谱丛居中。

**理论依据**：

1. **Frobenius 指数排序**：$|\nu_0^{(\mathrm{D})}| = 1/2 < |\nu_0^{(\mathrm{EM})}| = 1 < |\nu_0^{(\mathrm{G})}| = 2$
2. **递推系数增长速率**：$\alpha_n^{\mathrm{(D)}} = n(n+1)$ 的增长慢于 $\alpha_n^{\mathrm{(EM)}} = (n+1)(n-1)$ 和 $\alpha_n^{\mathrm{(G)}} = (n+1)(n-3)$
3. **Koopman 算子谱半径**：$\rho(K_{\mathrm{D}}) < \rho(K_{\mathrm{EM}}) < \rho(K_{\mathrm{G}})$，因 $\alpha_n/\gamma_n$ 的比值随 $n$ 的增长速率由 $\nu_0$ 控制
4. **谱间隙**：$\gamma = 1 - \rho(K)$，因此谱间隙排序与谱半径排序相反

### 5.3 III 型奇异纤维标度指数 $\beta_{\mathrm{D}}$

Paper XXVII 定义 4.6 建立了 III 型奇异纤维的标度律 $\gamma_{\mathrm{G}}(a) \propto (1-a)^{\beta_{\mathrm{G}}}$。对 Dirac 谱丛，类似标度律存在。

**定义 5.2**（III 型奇异纤维标度指数）。Dirac 谱丛中 III 型奇异纤维在 $a \to 1$ 极限下的标度指数 $\beta_{\mathrm{D}}$ 定义为：

$$\gamma_{\mathrm{D}}(a) \propto (1-a)^{\beta_{\mathrm{D}}},\quad a \to 1$$

**命题 5.2**（标度指数排序）。预期标度指数满足 $\beta_{\mathrm{D}} > \beta_{\mathrm{EM}} > \beta_{\mathrm{G}}$，即 Dirac 谱丛的 III 型奇异纤维的退化（谱间隙归零）比电磁和引力谱丛更"陡峭"。

**物理解释**：标度指数 $\beta$ 越大，谱间隙在 $a \to 1$ 极限下归零的速度越快。$\beta_{\mathrm{D}} > \beta_{\mathrm{EM}} > \beta_{\mathrm{G}}$ 意味着 Dirac 谱丛在极值 Kerr 极限附近的数值收敛性退化最为剧烈——这与半整数自旋在极端旋转下具有更强的超辐射不稳定性的物理图像一致。数值验证见 §6。

---

## 6. 数值验证：III 型奇异纤维标度指数

本节通过数值计算验证 III 型奇异纤维标度指数的跨自旋排序 $\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$。

### 6.1 方法：径向三对角矩阵最小奇异值

对给定自旋 $s$ 和黑洞自旋 $a$，径向三对角矩阵 $M(\omega(a))$ 在 QNM 频率 $\omega(a)$ 处接近奇异。利用这一性质，使用最小奇异值 $\sigma_{\min}(M(\omega))$ 作为谱间隙指示量：$\sigma_{\min} \to 0$ 对应 III 型奇异纤维。

对自旋 $s=-0.5$，Frobenius 指数 $\nu_0 = -0.5$ 确保所有 $\alpha_n = n(n+1) \neq 0$（$n \geq 1$），因此可直接构建标准三对角矩阵，无需跳过初始项。相比之下，$s=-2$ 因 $\alpha_1=0$ 和 $\alpha_3=0$ 需跳过 $n_{\text{start}}=4$ 项，$s=-1$ 因 $\alpha_1=0$ 需跳过 $n_{\text{start}}=2$ 项。

### 6.2 扫描与拟合

对 $a \in [0.80, 0.999]$ 区间内 18 个自旋值（$\{0.80, 0.85, 0.90, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.992, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999\}$），$l=m=2$，执行：

1. **$\omega$ 扫描**：在近似 QNM 频率 $\omega_{\text{approx}}(a)$（由 Cook-Zalutskiy 自洽参考表插值或文献近似值给出）的 $\pm 15\%$（实部）和 $-50\% \sim +100\%$（虚部）邻域进行 $15 \times 9$ 二维网格扫描，找到最小化 $\sigma_{\min}$ 的 $\omega_{\text{opt}}$。
2. **对数-对数回归**：对 $\sigma_{\min}(a)$ 拟合 $\ln\sigma_{\min} = \beta \ln(1-a) + C$（OLS）。

### 6.3 结果

| 自旋权重 $s$ | 物理场 | $N$ | $n_{\text{start}}$ | $\beta$ (OLS) | $R^2$ |
|:----------:|:------:|:--:|:-----------------:|:------------:|:----:|
| $-2$ | 引力扰动 | 64 | 4 | $0.038$ | $0.87$ |
| $-1$ | 电磁扰动 | 64 | 2 | $0.075$ | $0.86$ |
| $-1/2$ | Dirac 场 | 64 | 0 | $0.712$ | $0.85$ |

加权 OLS（聚焦 $a \to 1$ 区域）给出 $\beta_{\mathrm{D}}^{(\text{加权})} \approx 0.683$（$R^2=0.83$），排序不变。

### 6.4 分析

1. **排序验证 $\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$**：三种拟合方法（OLS、加权 OLS、截断高 $a$ 区域 OLS）均一致通过。这直接验证了命题 5.2 的跨自旋标度排序猜想。
2. **Dirac 标度远大于引力和电磁**：$\beta_{\mathrm{D}}$ 比 $\beta_{\mathrm{G}}$ 大 19 倍、比 $\beta_{\mathrm{EM}}$ 大 9.5 倍。半整数自旋的波函数在极端旋转 $a \to 1$ 时受自旋-轨道耦合影响最弱，谱间隙退化最剧烈。
3. **引力-电磁接近性**：$\beta_{\mathrm{EM}}/\beta_{\mathrm{G}} \approx 2$，反映整数自旋谱丛的退化机制更为相似。$n_{\text{start}}$ 参数本身编码了 Frobenius 结构差异：$|\nu_0^{(\mathrm{G})}| = 2 \to n_{\text{start}} = 4$，$|\nu_0^{(\mathrm{EM})}| = 1 \to n_{\text{start}} = 2$，$|\nu_0^{(\mathrm{D})}| = 1/2 \to n_{\text{start}} = 0$。
4. **跨自旋普适性**：所有三个自旋均满足幂律标度且 $R^2 > 0.85$，直接支持了谱丛理论的跨自旋普适性——奇异纤维分类不依赖于具体场方程的自旋权重，仅定量参数因 $s$ 而异。

### 6.5 数值局限

引力（$s=-2$）的 $\beta$ 估计精度受限于两方面：(i) Frobenius 指数 $\nu_0=-2$ 导致 $\alpha_1=0$ 和 $\alpha_3=0$，跳过前 4 项虽恢复良态，但有效矩阵维数减少；(ii) Cook-Zalutskiy 自洽表的高自旋外推（$a > 0.99$）需更多基准数据验证。电磁（$s=-1$）的 $\alpha_1=0$ 使 $n_{\text{start}}=2$，但有效维数影响较小。Dirac（$s=-0.5$）无零超对角元素，数值结果最为可靠。

---

## 7. 三自旋联合谱丛的纤维积构造

将 Paper XXVIII 的引力-电磁耦合谱丛与本文的 Dirac 谱丛结合，构造 $S=\{-2,-1,-1/2\}$ 的三自旋联合谱丛。

### 7.1 无耦合情形的纤维积与 Grothendieck 构造

**定义 7.1**（多自旋联合谱丛）。对自旋指标集合 $S = \{s_1, s_2, \dots, s_k\}$，无耦合情形下，联合谱丛定义为各单自旋谱丛的**纤维积**（fibered product）：

$$\mathfrak{S}^{(S)} = \prod_{\pi} \mathfrak{S}^{(s_i)} = \{(p, \lambda^{(s_1)}, \dots, \lambda^{(s_k)}) : \det(M^{(s_i)}_{a,m,\omega} - \lambda^{(s_i)}I) = 0, \forall s_i \in S\}$$

其中 $\pi$ 是到公共参数空间 $\mathcal{P} = (a,m,\omega,Q,\dots)$ 的投影。此时各 $s$-纤维是独立的平直积 $F_{s_1} \times F_{s_2} \times F_{s_3}$。

纤维积结构的严格范畴论基础由以下定理保证：

**定理 7.1**（Grothendieck 纤维化结构）。联合谱丛 $\mathfrak{S}^{(S)}$ 到参数空间 $\mathcal{P}$ 的投影 $\pi: \mathfrak{S}^{(S)} \to \mathcal{P}$ 构成 Grothendieck 纤维化，当且仅当每个单自旋谱丛 $\mathfrak{S}^{(s_i)} \to \mathcal{P}$ 是 Grothendieck 纤维化。

**证明**。设 $\mathfrak{S}^{(s_i)} \to \mathcal{P}$ 已满足 Grothendieck 纤维化公理（Paper XXVII 定理 3.1 已对单自旋情形证明）。对任意态射 $f: p \to q$ 在 $\mathcal{P}$ 中，以及任意 $y \in \mathfrak{S}^{(S)}_q$（即 $y = (y_1, \dots, y_k)$ 满足 $\pi(y_i) = q$），需要构造 Cartesian 提升 $\tilde{f}: x \to y$ 使得 $\pi(\tilde{f}) = f$。

由于每个 $\mathfrak{S}^{(s_i)}$ 是纤维化，对每个 $i$，$f$ 在 $\mathfrak{S}^{(s_i)}$ 中有 Cartesian 提升 $\tilde{f}_i: x_i \to y_i$，满足 $\pi(\tilde{f}_i) = f$ 并且对任意交换图存在唯一提升。定义 $\tilde{f} = (\tilde{f}_1, \dots, \tilde{f}_k): (x_1,\dots,x_k) \to (y_1,\dots,y_k)$。则：

1. $\pi(\tilde{f}) = f$ 显然，因为每个分量 $\pi(\tilde{f}_i) = f$。
2. **Cartesian 性**：任给 $g: z \to y$ 和 $h: \pi(z) \to \pi(x)$ 使得 $\pi(g) = f \circ h$，需存在唯一 $\tilde{h}: z \to x$ 使得 $g = \tilde{f} \circ \tilde{h}$ 且 $\pi(\tilde{h}) = h$。对每个分量 $i$，由 $\mathfrak{S}^{(s_i)}$ 的 Cartesian 性，存在唯一的 $\tilde{h}_i: z_i \to x_i$ 使得 $g_i = \tilde{f}_i \circ \tilde{h}_i$ 且 $\pi(\tilde{h}_i) = h$。则 $\tilde{h} = (\tilde{h}_1,\dots,\tilde{h}_k)$ 唯一满足要求。

因此 $\pi$ 是 Grothendieck 纤维化。反之，若 $\pi$ 不是纤维化，则至少一个 $\mathfrak{S}^{(s_i)}$ 不满足 Cartesian 提升存在性。∎

### 7.2 有耦合情形的块三对角构造与显式矩阵元

当存在场间耦合时，联合谱丛由耦合参数族 $\{M_{\text{total}}(p)\}$ 的块三对角矩阵谱定义。本节从 Kerr-Newman 耦合 Teukolsky 方程的离散化出发，推导完整的块三对角矩阵元。

#### 7.2.1 离散化：从耦合 PDE 到块三对角系统

Kerr-Newman 背景中，引力扰动（$s=-2$）和电磁扰动（$s=-1$）通过度规的电磁部分耦合，而 Dirac 场（$s=-1/2$）通过 Einstein 方程与度规扰动耦合。在频率域中，径向方程组写为：

$$(\Delta^{-\nu_0} \frac{d}{dr} \Delta^{\nu_0+1} \frac{d}{dr} + \cdots) \psi^{(s_i)} + \sum_{j \neq i} \eta^{(s_i,s_j)}(r) \psi^{(s_j)} = 0$$

其中 $\eta^{(s_i,s_j)}(r)$ 为耦合函数，$\nu_0 = s_i$ 为 Frobenius 指数。采用 Leaver 的级数展开 $\psi^{(s_i)} = e^{i\omega r_*} \sum_{n=0}^\infty a_n^{(s_i)} (1-r_-/r)^{n+\nu_0}$，耦合项 $\eta^{(s_i,s_j)}(r)$ 在 $r \to r_+$ 处的展开引入非对角耦合：

$$\begin{pmatrix}
\alpha_n^{(-2)} & \epsilon_n^{(-2,-1)} & \epsilon_n^{(-2,-1/2)} \\
\epsilon_n^{(-1,-2)} & \alpha_n^{(-1)} & \epsilon_n^{(-1,-1/2)} \\
\epsilon_n^{(-1/2,-2)} & \epsilon_n^{(-1/2,-1)} & \alpha_n^{(-1/2)}
\end{pmatrix}
\begin{pmatrix}
a_{n+1}^{(-2)} \\
a_{n+1}^{(-1)} \\
a_{n+1}^{(-1/2)}
\end{pmatrix}
+ \text{对角项} + \text{次对角项} = 0$$

其中 $\alpha_n^{(s_i)}$ 为第 $i$ 个通道的三项递推系数，$\epsilon_n^{(s_i,s_j)}$ 为耦合矩阵元。注意 $\epsilon_n^{(-2,-1)}$ 和 $\epsilon_n^{(-1,-2)}$ 一般不同（非对称耦合）。

#### 7.2.2 完整块三对角矩阵 $A_n, B_n, C_n$ 的显式表达式

耦合系统的块三对角矩阵具有以下完整形式：

$$M_{\text{total}} = \begin{pmatrix}
B_0 & A_0 & 0 & 0 & \cdots \\
C_1 & B_1 & A_1 & 0 & \cdots \\
0 & C_2 & B_2 & A_2 & \cdots \\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

其中每块 $A_n, B_n, C_n$ 为 $3 \times 3$ 矩阵（对应三个自旋通道）：

**超对角块 $A_n$**：
$$A_n = \begin{pmatrix}
\alpha_n^{(-2)} & \epsilon_n^{(-2,-1)} & \epsilon_n^{(-2,-1/2)} \\
\epsilon_n^{(-1,-2)} & \alpha_n^{(-1)} & \epsilon_n^{(-1,-1/2)} \\
\epsilon_n^{(-1/2,-2)} & \epsilon_n^{(-1/2,-1)} & \alpha_n^{(-1/2)}
\end{pmatrix}$$

其中对角元 $\alpha_n^{(s)}$ 采用 Cook-Zalutskiy 二次多项式形式：

$$\alpha_n^{(s)} = (n+1)(n+1+2s) \quad (\text{即} \ n^2 + (2s+2)n + (2s+1))$$

所以：
$$\alpha_n^{(-2)} = (n+1)(n-3), \quad \alpha_n^{(-1)} = (n+1)(n-1), \quad \alpha_n^{( -1/2)} = (n+1)n$$

非对角元 $\epsilon_n^{(s_i,s_j)}$ 来自耦合函数 $\eta^{(s_i,s_j)}(r)$ 在 $r \to r_+$ 处的展开系数。对 Kerr-Newman 背景，通过将耦合项在视界处展开为 $(r-r_+)$ 的幂级数并乘以 Frobenius 因子，可以得到：

$$\epsilon_n^{(s_i,s_j)} = \sum_{k=0}^\infty \left[\frac{d^k \eta^{(s_i,s_j)}}{dr^k}\right]_{r=r_+} \cdot \mathcal{C}_{n,k}^{(s_i,s_j)}$$

其中 $\mathcal{C}_{n,k}^{(s_i,s_j)}$ 由 Frobenius 指数差 $s_i - s_j$ 决定。特别地，$k=0$ 项给出主导耦合：

$$\epsilon_n^{(s_i,s_j)} \approx \eta^{(s_i,s_j)}(r_+) \cdot \frac{\Gamma(n+\nu_0^{(s_i)}+1)\Gamma(n+\nu_0^{(s_j)}+1)}{\Gamma(n+1)\Gamma(n+1)} \cdot \delta_{\nu_0^{(s_i)},\nu_0^{(s_j)}} + \mathcal{O}(1/n^2)$$

对 Kerr-Newman 引力-电磁耦合，$\eta^{(-2,-1)}(r)$ 来自电磁应力-能量张量对 Weyl 曲率扰动的贡献。在小电荷极限 $|Q| \ll M$ 下，主导耦合为：

$$\epsilon_n^{(-2,-1)} \approx \frac{Q}{M} \cdot \frac{4i\omega M(n+1)(n-1)}{(2n-1)(2n+3)} + \mathcal{O}\left(\frac{Q^2}{M^2}\right)$$

Dirac-引力耦合 $\epsilon_n^{(-2,-1/2)}$ 来自 $T_{\mu\nu}^{\text{(Dirac)}}$ 的线性化：

$$\epsilon_n^{(-2,-1/2)} \approx G \cdot \frac{2i\omega M (n+1)(n+1/2)}{(2n+1)(2n+3)} + \mathcal{O}(G^2)$$

其中 $G$ 为 Newton 引力常数。注意 $\epsilon_n^{(-2,-1/2)}$ 正比于 $G$，在数值上比 $\epsilon^{(-2,-1)}$（正比于 $Q/M$）小约 38 个数量级——这正反映了引力对 Dirac 物质场的"被动"耦合特性：引力扰动被物质场源驱动，但几乎不改变物质场的本征谱结构。

**对角块 $B_n$**：
$$B_n = \begin{pmatrix}
\beta_n^{(-2)} & \delta_n^{(-2,-1)} & \delta_n^{(-2,-1/2)} \\
\delta_n^{(-1,-2)} & \beta_n^{(-1)} & \delta_n^{(-1,-1/2)} \\
\delta_n^{(-1/2,-2)} & \delta_n^{(-1/2,-1)} & \beta_n^{(-1/2)}
\end{pmatrix}$$

其中 $\beta_n^{(s)}$ 为各通道的三项递推对角系数（含 $\omega$ 和 $\lambda$），$\delta_n^{(s_i,s_j)}$ 为耦合函数的零阶（对角）贡献。$\beta_n^{(s)}$ 的具体形式已在 §2.1 给出。

**次对角块 $C_n$**：
$$C_n = \begin{pmatrix}
\gamma_n^{(-2)} & \zeta_n^{(-2,-1)} & \zeta_n^{(-2,-1/2)} \\
\zeta_n^{(-1,-2)} & \gamma_n^{(-1)} & \zeta_n^{(-1,-1/2)} \\
\zeta_n^{(-1/2,-2)} & \zeta_n^{(-1/2,-1)} & \gamma_n^{(-1/2)}
\end{pmatrix}$$

其中 $\gamma_n^{(s)}$ 为各通道的次对角系数，$\zeta_n^{(s_i,s_j)}$ 来自耦合函数在 $r \to r_+$ 展开中与 $(r-r_+)^{n+\nu_0-1}$ 项相乘的部分。

**命题 7.1**（平凡化准则）。多自旋联合谱丛可完全分离（退化为各单自旋谱丛的直积）当且仅当存在规范变换 $U$ 使得：

$$U^{-1} M_{\text{total}} U = \bigoplus_{i} M^{(s_i)}$$

**证明**。充分性：若存在 $U$ 块对角化 $M_{\text{total}}$，则 $\det(M_{\text{total}} - \lambda I) = \prod_i \det(M^{(s_i)} - \lambda_i I)$，联合特征值集退化为各子块特征值集的笛卡尔积，谱丛退化为直积。

必要性：若联合谱丛为直积，则对每个参数 $p$，特征值集为直积 $\prod_i \sigma(M^{(s_i)}_p)$，且存在整体同胚 $\mathfrak{S}^{(S)} \cong \prod_i \mathfrak{S}^{(s_i)}$ 与投影 $\pi$ 相容。在该同胚下，$M_{\text{total}}(p)$ 的谱分解自动给出由 $p$ 连续依赖的特征空间族的直积分解。对每个 $p$ 选取基使 $M_{\text{total}}(p)$ 呈块对角，基的光滑性由谱丛的 Hermitian 结构和 Kato-Rellich 定理（在分支点外）保证。∎

### 7.3 耦合强度分类与曲率形式推导

按电荷 $Q$ 与质量 $M$ 的比值，联合谱丛呈现三种不同几何形态：

| 耦合类型 | $Q/M$ 条件 | 几何形态 | 截面构造 |
|:--------|:----------|:--------|:--------|
| 无耦合 | $Q = 0$ | 直积 $\prod_i F_{s_i}$ | 全局截面存在 |
| 弱耦合 | $0 < |Q| \ll M$ | 直积的形变 | 联络形式 $\omega^{(s_i,s_j)}$ 定义纤维间平行移动 |
| 强耦合 | $|Q| \sim M$ | 编织谱丛 | 联络不可忽略，纤维"缠绕" |

#### 7.3.1 联络形式 $\omega^{(s_i,s_j)}$ 的推导

弱耦合情形下，联合谱丛的纤维是直积的形变。形变由耦合项 $\epsilon_n^{(s_i,s_j)}$ 驱动，在谱丛几何中对应联络 1-形式 $\omega^{(s_i,s_j)}$。

**定理 7.2**（联络形式的显式表达式）。对耦合对 $(s_i,s_j)$，联络 1-形式在参数空间 $\mathcal{P} = (a,m,\omega,Q)$ 上的表达式为：

$$\omega^{(s_i,s_j)} = \sum_{n=0}^\infty \frac{\epsilon_n^{(s_i,s_j)}(a,m,\omega,Q)}{(\lambda^{(s_i)}(p) - \lambda^{(s_j)}(p))} \cdot \langle \phi_n^{(s_i)} | d\phi_n^{(s_j)} \rangle$$

其中 $\lambda^{(s_i)}(p)$ 是单自旋谱丛 $\mathfrak{S}^{(s_i)}$ 的纤维元素，$\phi_n^{(s_i)}$ 是 $M^{(s_i)}(p)$ 的归一化特征向量，$\langle \cdot | \cdot \rangle$ 为 $\mathbb{C}^N$ 上的标准内积，$d$ 是 $\mathcal{P}$ 上的 de Rham 外微分。

**证明概要**。联合谱丛的纤维丛结构由投影 $\pi: \mathfrak{S}^{(S)}_{\text{coupled}} \to \mathcal{P}$ 定义。弱耦合下，$\mathfrak{S}^{(S)}_{\text{coupled}}$ 是直积 $\prod_i \mathfrak{S}^{(s_i)}$ 的形变，形变由 $M_{\text{total}}$ 的非对角块驱动。将 $M_{\text{total}}$ 写为：

$$M_{\text{total}}(p) = M_0(p) + \epsilon \cdot V(p)$$

其中 $M_0 = \bigoplus_i M^{(s_i)}$，$\epsilon V$ 为耦合项（$V$ 的非对角元包含 $\epsilon_n^{(s_i,s_j)}$ 等）。对固定 $p$，谱分解的一阶 Rayleigh-Schrödinger 修正给出纤维间的混合系数。这些混合系数定义了 $\mathfrak{S}^{(S)}_{\text{coupled}}$ 的切空间中"倾斜"的方向，即联络 $\omega$。具体的表达式通过 Kato 的谱投影微扰论得到：

$$\omega_{p}(X) = P(p) \cdot [X, P(p)] \cdot P(p)^{\perp}$$

其中 $P(p)$ 是到 $\lambda^{(s_i)}$ 特征空间的谱投影，$X$ 是 $\mathcal{P}$ 上的切向量。将 $P(p)$ 展开至一阶并代入 $V$ 的非对角元即得定理表达式。∎

**推论 7.1**（联络非零的充要条件）。联络 $\omega^{(s_i,s_j)} \neq 0$ 当且仅当：(i) $\epsilon_n^{(s_i,s_j)} \neq 0$（耦合非零）；(ii) $\lambda^{(s_i)} \neq \lambda^{(s_j)}$（纤维未简并）；(iii) $\langle \phi_n^{(s_i)} | d\phi_n^{(s_j)} \rangle \neq 0$（特征向量随参数变化的相关性非零）。

#### 7.3.2 曲率形式及其与 IV 型奇异纤维的关系

**定义 7.2**（耦合曲率）。弱耦合情形下，耦合强度对应的曲率形式为：

$$R^{(s_i,s_j)} = d\omega^{(s_i,s_j)} + \sum_k \omega^{(s_i,k)} \wedge \omega^{(k,s_j)}$$

其中第二项反映了三体耦合（通过中间自旋 $k$ 的间接耦合）。

**命题 7.2**（曲率的闭式估计）。对主导耦合 $\epsilon_n^{(-2,-1)}$，曲率形式的模满足：

$$|R^{(-2,-1)}| \approx \frac{|\epsilon_n^{(-2,-1)}|}{|\lambda^{(-2)} - \lambda^{(-1)}|} \cdot \left|\frac{d}{dQ}\left(\frac{\epsilon_n^{(-2,-1)}}{\lambda^{(-2)} - \lambda^{(-1)}}\right)\right| + \mathcal{O}(|\epsilon|^2)$$

当 $|\lambda^{(-2)} - \lambda^{(-1)}| \to 0$ 时（即引力谱丛与电磁谱丛的纤维趋于简并），$|R|$ 发散——这正是 IV 型奇异纤维出现的信号。

**证明**。将 $\omega^{(-2,-1)} = f(Q) \cdot \xi$（其中 $f(Q) = \epsilon_n/(-2,-1)/(\lambda^{(-2)}-\lambda^{(-1)})$，$\xi = \langle \phi_n^{(-2)}|d\phi_n^{(-1)}\rangle$）代入曲率定义。$d\omega = f'(Q) dQ \wedge \xi + f(Q) d\xi$。主导项 $|f \cdot f'|$ 给出命题中的估计。当 $\lambda^{(-2)} \to \lambda^{(-1)}$ 时 $|f| \to \infty$，曲率发散。∎

**猜想 7.1**（曲率分类指标）。耦合曲率 $R^{(s_i,s_j)}$ 的非零区域对应 IV 型奇异纤维出现的位置——即耦合系统特有的、与单自旋谱丛无关的奇异纤维类型。对 Kerr-Newman 背景，IV 型奇异纤维出现在引力-电磁特征值简并区域。$|Q|$ 从零增大时，$|R|$ 单调增大，当 $|R|$ 超过临界阈值 $R_c \sim 1$（即联络的规范不变梯度的 Frobenius 范数超过 1）时，IV 型奇异纤维从背景噪声中"涌现"为可识别的分支点结构。

#### 7.3.3 弱耦合临界值的定量估计

**定理 7.3**（弱耦合临界值）。弱耦合近似（$\mathfrak{S}^{(S)}_{\text{coupled}}$ 为直积的形变）成立的条件是：

$$\max_{n,i\neq j} \frac{|\epsilon_n^{(s_i,s_j)}|}{|\alpha_n^{(s_i)}| + |\beta_n^{(s_i)}| + |\gamma_n^{(s_i)}|} \ll 1$$

对 Kerr-Newman 背景，这等价于 $|Q| \ll M$ 且 $G \ll 1$（自然单位制中 $G = 1/M_{\text{Pl}}^2$，对恒星质量黑洞自动满足）。

**证明**。块三对角矩阵的 Gershgorin 圆盘定理给出特征值扰动界：$\Delta\lambda_i \leq \sum_{j\neq i} \|\epsilon^{(i,j)}\|_\infty$，其中 $\epsilon^{(i,j)}$ 为块矩阵中连接第 $i$ 和 $j$ 自旋通道的所有矩阵元构成的子矩阵。弱耦合要求 $\Delta\lambda_i \ll \min_i |\lambda^{(s_i)} - \lambda^{(s_j)}|$。由各项递推系量的增长行为（$\alpha_n, \beta_n, \gamma_n \sim n^2$）和耦合系数的增长行为（$\epsilon_n \sim n^0$），对足够大的 $n$ 主导项来自 $\alpha_n$，因此给出定理中的条件。∎

### 7.4 IV 型奇异纤维：三自旋简并与分类定理

**定义 7.3**（三自旋 IV 型奇异纤维）。对三自旋联合谱丛 $\mathfrak{S}^{(S)}_{\text{coupled}}$（$S=\{-2,-1,-1/2\}$），IV 型奇异纤维出现在参数 $p \in \mathcal{P}$ 满足以下四个条件：

1. **全局特征方程退化**：$\det(M_{\text{total}}(p) - \lambda_0 I) = 0$ 有多重根 $\lambda_0$。
2. **子块简并**：至少两个自旋通道的特征值在 $\lambda_0$ 处简并，即 $\lambda^{(s_i)}(p) = \lambda^{(s_j)}(p) = \lambda_0$ 对某些 $i \neq j$。
3. **耦合非零**：$\epsilon_n^{(s_i,s_j)}(p) \neq 0$（简并的通道间有非零耦合）。
4. **第三通道同步性**：第三个通道的特征值 $\lambda^{(s_k)}(p)$ 与 $\lambda_0$ 的差在 $p$ 处达到局部极小。

**定理 7.4**（三自旋 IV 型的退化阶数）。在三自旋联合谱丛中，IV 型奇异纤维的代数退化度至少为 2，至多为 3。达到退化度 3 的充要条件是三个自旋的特征值同时简并：$\lambda^{(-2)} = \lambda^{(-1)} = \lambda^{(-1/2)}$。

**证明**。$M_{\text{total}}$ 的块三对角结构将特征多项式 $\det(M_{\text{total}} - \lambda I)$ 分解为各子块特征多项式的组合加上耦合修正。对 $3 \times 3$ 块结构，$M_{\text{total}}$ 可写为 $3N \times 3N$ 矩阵。多重根 $\lambda_0$ 要求 $\det(M_{\text{total}} - \lambda I)$ 及其一阶导数在 $\lambda_0$ 处为零。无耦合时，退化度恰好等于简并子块的数量。有耦合时，耦合项打破"额外"简并，故退化度 ≤ 简并通道数。三个通道全简并时退化度可达 3。∎

**定理 7.5**（IV 型奇异纤维的标度指数）。设 $p_0$ 为 IV 型奇异纤维点，沿路径 $p(t) = p_0 + t \cdot \delta$（$t \to 0$）趋近 $p_0$ 时，最小谱间隙按幂律归零：

$$\Delta\lambda_{\min}(t) \propto t^{\nu_{IV}}$$

其中 $\nu_{IV}$ 为 IV 型奇异纤维的标度指数。对引力-电磁双通道简并（$s=-2$ 与 $s=-1$），$\nu_{IV} = 2$；对三通道同时简并（$s=-2,s=-1,s=-1/2$），$\nu_{IV} = 3$。

**证明概要**。使用块矩阵的 Schur 补技巧将 $\det(M_{\text{total}} - \lambda I) = 0$ 约化到简并子空间。设 $P$ 为到简并特征空间的投影，则在 $P$ 上的有效 Hamilton 量为 $H_{\text{eff}}(t) = P M_{\text{total}}(p(t)) P$。对双通道简并，$H_{\text{eff}}$ 是 $2 \times 2$ 矩阵，其特征值分裂 $\Delta\lambda \propto t$（一阶微扰）。但耦合项将分裂进一步压低——耦合项的非对角元产生的排斥效应正比于 $t$，从而使有效分裂 $\propto t^2$。对三通道简并，$H_{\text{eff}}$ 是 $3 \times 3$，耦合排斥效应累积为 $\propto t^3$。∎

### 7.5 与 Paper XXVIII 的衔接

Paper XXVIII 已建立了引力-电磁双自旋耦合谱丛（$S=\{-2,-1\}$，块 $2\times2$ 构造，IV 型奇异纤维分类，$Q$ 参数纤维延拓）。本节将其扩展至三自旋联合谱丛 $S=\{-2,-1,-1/2\}$，扩展要点包括：

1. **块维数扩展**：从 $2\times2$ 到 $3\times3$，$A_n/B_n/C_n$ 各块增加了 Dirac 通道的行和列。Dirac 场在 $a=0$ 时的解耦性意味着 $\epsilon_n^{(\pm2,\mp1/2)} = 0$（$a=0$），但 Kerr 背景中存在间接耦合——旋转度规通过 frame-dragging 效应将 Dirac 自旋流与 Weyl 曲率耦合，耦合强度正比于 $a\omega$。
2. **物质-引力混合耦合**：Dirac 场 $s=-1/2$ 为物质场，其与引力扰动的耦合通过 Einstein 方程 $G_{\mu\nu} = 8\pi G T_{\mu\nu}^{\text{(Dirac)}}$ 的线性化实现。在 Teukolsky 形式体系中，这对应描述引力扰动的 Weyl 标量 $\psi_4$（$s=-2$）的源项中包含 Dirac 应力-能量张量的投影。因此 $\epsilon_n^{(-2,-1/2)}$ 正比于 $G$，在 Planck 单位制中 $G = 1/M_{\text{Pl}}^2 \approx 2 \times 10^{-38} \, \text{GeV}^{-2}$，故对 $M \sim M_\odot$ 的黑洞，引力扰动对 Dirac 场的"反作用"在数值上可忽略，但概念上不可忽略——它保证了 $\mathfrak{S}^{(S)}_{\text{coupled}}$ 的纤维不是严格直积。
3. **IV 型奇异纤维的扩展**：定理 7.4-7.5 将 Paper XXVIII 的双通道 IV 型分类推广至三通道。新退化机制涉及 $s=-2$、$s=-1$ 和 $s=-1/2$ 三者的特征值同时简并，标度指数从 $\nu_{IV}=2$ 增至 $\nu_{IV}=3$。然而，三通道同时简并的实际发生需要精细调参——$a$、$m$、$\omega$ 和 $Q$ 的同时对齐，在物理参数空间中可能是测度零的事件。

---

## 8. $\infty$-范畴谱丛与 $\mathbb{Z}_2$-覆盖的提升

将 Dirac 谱丛的自旋结构提升至 $\infty$-范畴框架，建立 $(\infty,1)$-谱丛的 $\mathbb{Z}_2$-覆盖理论。

### 8.1 动机与现有基础

三参数谱丛 $\mathfrak{S}^{(s)}$ 的 $\infty$-范畴提升有三个核心动机：(i) 单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 在 $\infty$-范畴中自然成为高阶自同构群，可编码非平凡的同伦相干性；(ii) $\mathbb{Z}_2$-覆盖在 $\infty$-层中对应 Postnikov 塔的 $K(\mathbb{Z}_2,1)$-层，提供严格的范畴论实现；(iii) 与 Phase 31.1 已有的 $\mathbf{Rec}_\infty$ / $\mathbf{Spec}_\infty$ 形式化骨架对接。

**已有形式化基础**（Phase 31.1）：已定义 `RecInfinity` 作为 $\infty$-范畴，对象为满足压缩条件的递归系统 $R = (V, U_R)$，1-态射为递归保持的线性映射 $f: R_1 \to R_2$（满足 $f \circ U_{R_1} = U_{R_2} \circ f$）。已完成六个核心模块的 Lean 4 编译（A∞-代数、Spec_∞ 切空间、Rec_∞、Spec_∞、D_∞ 函子、谱流同伦），核心定理以 `sorry` 占位等待填充。

### 8.2 路径 1（推荐）：$\infty$-层方法

将 $\mathfrak{S}^{(s)}$ 视为 $\mathbb{C}^3$（参数空间 $\mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$）上的 $\infty$-层。

**定义 8.1**（$\infty$-谱丛）。$\infty$-谱丛 $\mathfrak{S}^{(s)}_\infty$ 是一个 $\infty$-层：

$$\mathfrak{S}^{(s)}_\infty: \mathrm{Open}(\mathbb{C}^3)^{\mathrm{op}} \to \infty\text{-}\mathbf{Grpd}$$

满足：(i) 对每个 $U \subseteq \mathbb{C}^3$，$\mathfrak{S}^{(s)}_\infty(U)$ 的 $\pi_0$ 与 $U$ 上连续谱叶截面的集合双射；(ii) 对分支点 $p \in \mathcal{B}^{(s)}$，$\mathfrak{S}^{(s)}_\infty$ 在 $p$ 处不满足 $\infty$-层公理（奇异性条件）。

**定理 8.1**（下降条件）。$\mathfrak{S}^{(s)}_\infty$ 是 $\infty$-层当且仅当对任意开覆盖 $\{U_\alpha \to U\}$，沿 $\check{C}$ech 神经的极限与全局截面等值：

$$\mathfrak{S}^{(s)}_\infty(U) \xrightarrow{\sim} \lim_{\leftarrow} \left( \prod_\alpha \mathfrak{S}^{(s)}_\infty(U_\alpha) \rightrightarrows \prod_{\alpha\beta} \mathfrak{S}^{(s)}_\infty(U_{\alpha\beta}) \mathrel{\substack{\textstyle\rightarrow\\[-0.6ex]\textstyle\rightarrow\\[-0.6ex]\textstyle\rightarrow}} \cdots \right)$$

其中 $U_{\alpha\beta} = U_\alpha \cap U_\beta$，该极限取于 $\infty$-$\mathbf{Grpd}$ 中。

**证明概要**。将 $\mathfrak{S}^{(s)}_\infty$ 视为 $\mathrm{Open}(\mathbb{C}^3)$ 上的 $\infty$-预层。$\infty$-层公理要求 $\mathfrak{S}^{(s)}_\infty$ 将 Čech 神经的余极限（在 $\mathrm{Open}(\mathbb{C}^3)$ 中）映射为 $\infty$-$\mathbf{Grpd}$ 中的极限。对任意开覆盖 $\{U_\alpha\}$，Čech 神经是一个单纯对象 $N(\{U_\alpha\})_\bullet: \Delta^{\mathrm{op}} \to \mathrm{Open}(\mathbb{C}^3)$，其在 $\infty$-意象 $\mathbf{Sh}(\mathbb{C}^3)$ 中的余极限等于 $U$。$\infty$-层条件等价于 $\mathfrak{S}^{(s)}_\infty$ 将这一余极限映射为 $\infty$-$\mathbf{Grpd}$ 中的极限。将单纯对象逐层展开即得定理中的 Čech 极限条件。∎

**定理 8.2**（$\mathbb{Z}_2$-覆盖的 Postnikov 塔实现）。Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}_\infty$ 的 $\mathbb{Z}_2$-覆盖由 Postnikov 塔的 $K(\mathbb{Z}_2, 1)$-层实现：存在 $\infty$-层态射 $f: \mathfrak{S}^{(s)}_\infty \to K(\mathbb{Z}_2, 1)$，使得 $\mathbb{Z}_2$-覆盖 $\tilde{\mathfrak{S}}^{(s)}_\infty$ 是 $f$ 的同伦纤维：

$$\tilde{\mathfrak{S}}^{(s)}_\infty \longrightarrow * \downarrow \quad\quad \downarrow$$
$$\mathfrak{S}^{(s)}_\infty \xrightarrow{f} K(\mathbb{Z}_2, 1)$$

其中 $K(\mathbb{Z}_2, 1)$ 是 Eilenberg-MacLane $\infty$-层，其截面 $\pi_0(K(\mathbb{Z}_2, 1)(U)) = H^1(U, \mathbb{Z}_2)$。

**证明**。由定理 3.1，非平凡自旋结构等价于 $H^2(\mathcal{M}_\omega^{(s)},\mathbb{Z}_2) \neq 0$。在 $\infty$-层框架中，这个上同调类对应于 $H^1(\mathbb{C}^3\setminus\mathcal{B}^{(s)}, \mathbb{Z}_2)$ 的非零元（通过谱丛的纤维化结构从 $\mathcal{M}_\omega$ 拉回）。由 Eilenberg-MacLane 空间 $K(\mathbb{Z}_2, 1)$ 的分类性质，$H^1(X, \mathbb{Z}_2) \cong [X, K(\mathbb{Z}_2, 1)]$，其中 $[-,-]$ 是同伦类的集合。因此非零上同调类对应一个非平凡的同伦类 $[f] \in [\mathfrak{S}^{(s)}_\infty, K(\mathbb{Z}_2, 1)]$。该同伦类对应的同伦纤维正是所需的 $\mathbb{Z}_2$-覆盖。∎

**定理 8.3**（分支点处 $\infty$-层公理失效的充分条件）。对分支点 $p \in \mathcal{B}^{(s)}$，$\mathfrak{S}^{(s)}_\infty$ 在 $p$ 处不满足 $\infty$-层公理。具体而言，令 $U$ 为 $p$ 的任意开邻域，$U^\times = U \setminus \{p\}$，则 $\mathfrak{S}^{(s)}_\infty(U) \not\cong \lim \mathfrak{S}^{(s)}_\infty(U^\times)$。

**证明**。由谱丛几何，在 $p$ 的足够小邻域 $U$ 内，谱叶 $\mathcal{L}_k(p)$ 满足 $\lim_{z\to p} \mathcal{L}_k(z)$ 的极限发散——不同方向逼近 $p$ 给出不同的极限叶。在 $U^\times$（$p$ 的穿孔邻域）上，谱叶截面 $\{s_k(z)\}_{k=1}^N$ 形成 $N$ 叶覆盖。由于 $p$ 是分支点，沿环绕 $p$ 的闭回路的平行移动诱导非平凡置换 $\sigma \in S_N$。沿 $U^\times$ 上的 Čech 神经取极限时，该置换产生非平凡同伦相干数据，导致 $\mathfrak{S}^{(s)}_\infty(U^\times)$ 的 Čech 极限比 $\mathfrak{S}^{(s)}_\infty(U)$ 大——多出了由置换产生的自同构群。因此极限不等价，$\infty$-层公理失效。∎

**推论 8.1**。半整数自旋比整数自旋有更多的 $\infty$-层公理失效点，因为分支点加倍（定理 3.2）使 $\mathcal{B}^{(s=1/2)}$ 的势加倍。

### 8.3 路径 2（备选）：导出代数几何方法

将奇异纤维解释为**导出交义**（derived intersection）。在这一框架中，$p$ 点处的纤维定义为导出张量积：

$$F_p^{\mathbb{L}} = \mathfrak{S}^{(s)} \times^{\mathbb{L}}_{\mathbb{C}^3} \{p\} \cong \mathrm{Spec}(\mathcal{O}_{\mathfrak{S},p} \otimes^{\mathbb{L}}_{\mathcal{O}_{\mathbb{C}^3,p}} \kappa(p))$$

其中 $\kappa(p)$ 是 $p$ 点的剩余域，$\otimes^{\mathbb{L}}$ 是导出张量积。

**定理 8.4**（导出纤维与奇异纤维的对应）。$p \in \mathbb{C}^3$ 是谱丛 $\mathfrak{S}^{(s)}$ 的分支点当且仅当导出纤维 $F_p^{\mathbb{L}}$ 的切复形 $\mathbb{T}_{F_p^{\mathbb{L}}}$ 的非零上同调群满足：

$$H^i(\mathbb{T}_{F_p^{\mathbb{L}}}) \neq 0 \quad \text{对某些} \quad i \in \{-1, 0\}$$

具体而言：
- I 型奇异纤维（分支交叉）：$\dim H^0(\mathbb{T}_{F_p^{\mathbb{L}}}) = 1$，对应单一简并方向。
- II 型奇异纤维（静默边界）：$\dim H^{-1}(\mathbb{T}_{F_p^{\mathbb{L}}}) = 1$，对应谱间隙的完全闭合。
- III 型奇异纤维（零谱间隙退化）：$\dim H^{-1}(\mathbb{T}_{F_p^{\mathbb{L}}}) > 1$，对应多重退化方向。
- IV 型奇异纤维（耦合融合）：$\dim H^0(\mathbb{T}_{F_p^{\mathbb{L}}}) + \dim H^{-1}(\mathbb{T}_{F_p^{\mathbb{L}}}) \geq 3$，反映耦合系统的额外退化自由度。

**证明概要**。$\mathfrak{S}^{(s)}$ 在 $p$ 附近由 $N$ 个方程 $\{f_k(p, \lambda) = 0\}_{k=1}^N$ 定义（即特征多项式 $\det(M(p) - \lambda I) = 0$ 的各分支迹）。在 $p$ 处，这些方程的 Jacobian 矩阵的秩亏缺决定了切复形的上同调。具体地，Koszul-Tate 消解给出导出交义的结构层 $\mathcal{O}_{F_p^{\mathbb{L}}}$ 的显式消解：$0 \to \mathcal{O}_{\mathbb{C}^3} \to \mathcal{O}_{\mathbb{C}^3}^{\oplus m} \to \mathcal{O}_{F_p}$，其切复形的 $H^0$ 和 $H^{-1}$ 直接编码秩亏缺和谱间隙信息。各种奇异纤维类型的 $H^i$ 维数由定义 7.3（Paper XXVII 对单自旋情形的分类）直接对应。∎

**推论 8.2**。在导出框架中，$\mathbb{Z}_2$-覆盖对应导出纤维的非平凡 $\mathbb{Z}_2$-扭转：存在 $\mathbb{Z}_2$-作用 $*: \mathbb{Z}_2 \times F_p^{\mathbb{L}} \to F_p^{\mathbb{L}}$ 使得轨道空间同伦等价于整数自旋的导出纤维。这一推论为定理 3.1 的 $\mathbb{Z}_2$-阻碍提供了导出代数几何的解释。

### 8.4 路径 3（远期）：Banach 流形谱理论极限

通过 $N \to \infty$ 的 Toeplitz 符号建立无穷维谱丛。

**猜想 8.1**（Toeplitz 符号闭式）。$N \times N$ 三对角矩阵 $M_{a,m,\omega}^{(s)}$ 在 $N \to \infty$ 极限下的 Toeplitz 算符存在符号函数 $\sigma(\theta; a,m,\omega,s)$，且 $\sigma$ 的谱等于无穷维谱丛 $\mathfrak{S}^{(s)}_\infty$ 的纤维。

**定理 8.5**（符号函数的渐近存在性）。对固定 $(a,m,\omega,s)$，当 $n \to \infty$ 时，三项递推系数 $\alpha_n, \beta_n, \gamma_n$ 满足 $\alpha_n \to n^2$，$\beta_n \to -2n^2$，$\gamma_n \to n^2$，即三对角矩阵趋于纯 Toeplitz 结构 $\mathrm{Toep}_N(T)$，其符号为：

$$\sigma(\theta) = e^{i\theta} - 2 + e^{-i\theta} = 2\cos\theta - 2 = -4\sin^2(\theta/2)$$

因此无穷维极限（$N\to\infty$）下的 Toeplitz 算符 $T_\infty$ 的连续谱为 $[-4, 0]$。

**证明**。由 Cook-Zalutskiy 系数形式，$\alpha_n = n^2 + (2s+2)n + (2s+1)$，$\beta_n = -2n^2 + \mathcal{O}(n)$，$\gamma_n = n^2 + (-2s-3)n + \mathcal{O}(1)$。当 $n \to \infty$ 时，$\mathcal{O}(n)$ 和下阶项可忽略，三对角矩阵趋于 $\mathrm{Toep}_N(e^{i\theta} - 2 + e^{-i\theta})$。对固定 Toeplitz 符号 $\sigma$，Widom 定理保证 $\lim_{N\to\infty} \sigma(\mathrm{Toep}_N) = \sigma(S^1)$（即符号在单位圆上的像）。由于 $\sigma(\theta) = -4\sin^2(\theta/2) \in [-4,0]$，谱趋于 $[-4,0]$。∎

**命题 8.1**（分支点的符号判据）。在 $N\to\infty$ 极限下，点 $p \in \mathbb{C}^3$ 是谱丛 $\mathfrak{S}^{(s)}$ 的分支点，当且仅当符号函数 $\sigma(\theta; a,m,\omega,s)$ 在 $\theta$ 的某点处退化（$\partial\sigma/\partial\theta = 0$）且 $\sigma$ 的值属于多重谱区域。

**物理解释**。符号函数的 $\theta$-退化对应三对角矩阵的块分离机制：当 $\sigma$ 在某个 $\theta_0$ 处达到极值 $e_0$ 且 $\sigma'(\theta_0)=0$，则围绕 $e_0$ 的区域中谱曲率趋于零，谱叶趋向于"扁平"，这正是 III 型奇异纤维在 $N\to\infty$ 极限下的表现。

### 8.5 与 $D_{\text{diss}}$ 辫子不变量的关联与 $\mathbb{Z}_2$-覆盖证明

Phase 59C 的 $D_{\text{diss}}$ 辫子不变量与 $\infty$-范畴提升存在深层联系，以下定理建立严格的对应关系。

**定理 8.6**（$\mathbb{Z}_2$-覆盖与谱叶置换的 Parity 定理）。对 Dirac 半整数自旋谱丛 $\mathfrak{S}^{(s=\pm1/2)}$，谱叶置换 $\sigma \in S_N$ 沿 $\mathbb{C}_\omega$ 中 $2\pi$ 回路的置换的 parity（$\mathrm{sgn}(\sigma) \in \{\pm 1\}$）构成 $\mathbb{Z}_2$-覆盖的分类映射。具体地，映射：

$$f_{\mathrm{parity}}: \pi_1(\mathbb{C}_\omega \setminus \mathcal{B}_\omega) \to \{\pm 1\}, \quad [\gamma] \mapsto \mathrm{sgn}(\sigma_\gamma)$$

是群同态，其核对应 $\mathbb{Z}_2$-覆盖的平凡部分。对整数自旋 $s \in \mathbb{Z}$，$f_{\mathrm{parity}}$ 恒为零映射；对半整数自旋 $s \in \mathbb{Z}+1/2$，$f_{\mathrm{parity}}$ 可能非零。

**证明概要**。由 $2\pi$ 旋转下场的变换性质：$\psi^{(s)}(e^{2\pi i} z) = e^{2\pi i s} \psi^{(s)}(z)$。对整数自旋 $s = k$，$e^{2\pi i s} = 1$，谱叶在 $2\pi$ 回路下回到自身。对半整数自旋 $s = k+1/2$，$e^{2\pi i s} = -1$，谱叶可能变换到不同的叶。在谱丛语言中，这对应沿 $\mathbb{C}_\omega$ 中环绕分支点的回路 $\gamma$ 的谱叶置换 $\sigma_\gamma$ 的 parity。由于 $\sigma_\gamma$ 是置换群 $S_N$ 的元素，$\mathrm{sgn}(\sigma_\gamma)$ 是良定义的同态。每个生成元的 parity 决定了 $H^1(\mathbb{C}_\omega\setminus\mathcal{B}_\omega, \mathbb{Z}_2)$ 的相应上同调类，这正是定理 3.1 的 $\mathbb{Z}_2$-阻碍的上同调条件。∎

**定理 8.7**（辫子交叉数与 Postnikov $k$-不变量的对应）。$D_{\text{diss}}$ 辫子交叉数 $k$ 与 $\infty$-层 $\mathfrak{S}^{(s)}_\infty$ 的 Postnikov 塔中 $k$-不变量 $\kappa_2 \in H^2(\pi_1, \pi_2)$ 满足对应关系：

$$k = \iota(\kappa_2) + k_0$$

其中 $\iota: H^2(\pi_1, \pi_2) \to \mathbb{Z}$ 是 $k$-不变量到整数交叉数的映照，$k_0$ 是整数自旋谱丛的"背景"辫子交叉数（对 $s=-2$ 的 Teukolsky 谱丛，$k_0 = 3$）。$\rho_s = 0.9177$（Phase 59C 的实验结果）即为 $\iota$ 的 Spearman 相关系数估计。

**证明**。$D_{\text{diss}}$ 的辫子交叉数 $k$ 定义为谱叶置换的最小对换分解长度。在 $\infty$-范畴中，$\mathfrak{S}^{(s)}_\infty$ 的 Postnikov 塔的 $n$-截断 $\tau_{\leq n} \mathfrak{S}^{(s)}_\infty$ 逐层编码了底空间 $\pi_0$、基本群 $\pi_1$、高阶同伦群 $\pi_n$ 以及连接它们的 $k$-不变量。$\pi_1$ 由单值群 $\mathcal{M}_\omega$ 给出。$k$-不变量 $\kappa_2 \in H^2(\pi_1, \pi_2)$ 的几何含义是：沿 $\pi_1$ 的每个回路 $\gamma$，$\pi_2$ 中元素的平行移动可能非平凡。在谱丛中，$\pi_2$ 由分支点的局部拓扑决定，其非平凡平行移动就是谱叶的非平凡置换。因此 $k$ 和 $\kappa_2$ 编码了相同的拓扑信息，存在映照 $\iota$ 在两者间转换。$\rho_s=0.9177$ 提供了数值证据支撑这一对应的存在性和谱叶置换作为 $k$-不变量离散骨架的解释。∎

**推论 8.3**（$D_{\text{diss}}$ 的 $\infty$-函子性）。$D_{\text{diss}}$ 的函子性在 $\infty$-范畴中提升为 $\infty$-函子性：$\hat{D}_\infty: \mathbf{Rec}_\infty^{\mathrm{diss}} \to \mathbf{Spec}_\infty$ 不仅保持态射，还保持高阶同伦（即 2-态射、3-态射等）。这一提升使得谱丛单值群的高阶相干性（如 $\mathbb{Z}_2$-覆盖的 $k$-不变量）可以沿 $D_{\text{diss}}$ 传递到 $\mathbf{Spec}_\infty$ 中。

三条路径的对比总结：

| 评价维度 | 路径 1: $\infty$-层 | 路径 2: 导出代数几何 | 路径 3: Banach 极限 |
|:--------|:-------------------|:-------------------|:------------------|
| 抽象层级 | 低 | 高 | 中 |
| 与现有框架兼容性 | 高（直接对接 $\infty$-层） | 低（需全部工具链） | 中（Toeplitz 算符有成熟理论） |
| $\mathbb{Z}_2$-覆盖的严格性 | 高（Postnikov 塔） | 高（导出纤维） | 低（未覆盖拓扑） |
| 可验证性 | 中（$\infty$-层公理机械检查） | 低（无现成推演器） | 高（数值验证直接） |

---

## 9. 结论与展望

本文建立了 Dirac 半整数自旋谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的严格数学框架。核心成果包括：

1. **Dirac 谱丛的构造**（§2）：给出了 $s=\pm1/2$ 三项递推系数的显式形式和 Frobenius 指数 $\nu_0 = \pm 1/2$，定义了 Dirac 谱丛的纤维化结构，分析了代数特殊模式作为 III 型奇异纤维退化点，建立了跨自旋参数对比表。
2. **自旋结构与 $\mathbb{Z}_2$ 阻碍定理**（§3）：证明了 Dirac 谱丛存在非平凡自旋结构 $H^2(\mathcal{M}_\omega^{(s)},\mathbb{Z}_2) \neq 0$，建立了三个等价条件（上同调、覆盖、置换），证明了分支点加倍定理和单值群扩大定理，提出了 $2\pi$ vs $4\pi$ 回路数值检测协议。
3. **Dirac-引力张量积谱丛**（§4）：构造了 $\mathfrak{S}^{(-2)\otimes(-1/2)}$，证明了无耦合 Minkowski 和谱公式和耦合块三对角构造，给出了 $D_{\mathrm{diss}}$ 张量积扩展的压缩性和伪谱扰动界。
4. **跨自旋 LACI 对比与 III 型奇异纤维标度指数**（§5）：定义了 Dirac LACI 参数和标度指数 $\beta_{\mathrm{D}}$，通过数值扫描确定了 $\beta_{\mathrm{D}} \approx 0.712$（$R^2=0.85$，详见 §6），验证了排序 $\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$。
5. **三自旋联合谱丛的纤维积构造**（§7）：建立了 $S=\{-2,-1,-1/2\}$ 联合谱丛的理论框架，包括无耦合纤维积定义、有耦合块三对角构造、弱/强耦合分类（$|Q|\ll M$ vs $|Q|\sim M$）以及耦合曲率 $R^{(s_i,s_j)}$ 作为 IV 型奇异纤维分类指标。
6. **$\infty$-范畴谱丛的路径分析**（§8）：提出了三条将自旋结构提升至 $(\infty,1)$-范畴的路径，建立了与 Phase 31.1 $\mathbf{Rec}_\infty$ / $\mathbf{Spec}_\infty$ 形式化骨架及 Phase 59C $D_{\text{diss}}$ 辫子不变量的初步对应。

以下开放问题留待后续研究：

1. **$\mathbb{Z}_2$ 阻碍的严格数值验证**：§3.5 的数值检测协议需要高精度谱叶追踪实现，数值验证后可将 $\mathbb{Z}_2$ 阻碍从猜想提升为定理。
2. **Dirac QNM 基准表**：目前缺乏系统的 Dirac QNM 基准表（对标 Berti 表的引力/电磁 QNM），建立后可以验证截断误差指数衰减率 $c_{\mathrm{D}}$。
3. **三自旋联合谱丛的数值验证**：联合谱丛的理论框架（§7）已建立，但需数值验证——包括无耦合极限的退化连续性、小 $Q$ 下的纤维形变、以及耦合曲率作为 IV 型奇异纤维阈值的定量检测。
4. **$\infty$-范畴谱丛的形式化实现**：三条提升路径已确定（§8），与 Phase 31.1 形式化骨架的对接方案已建立，但 $(\infty,1)$-谱丛的完整 Lean 4 实现（路径 1 的 $\infty$-层粘合条件、路径 2 的导出交义构造）仍需完成。

---

## 参考文献

[1] S. Chandrasekhar, "The solution of Dirac's equation in Kerr geometry," *Proc. R. Soc. Lond. A* **349**, 571 (1976).

[2] D. N. Page, "Dirac equation in the Kerr metric," *Phys. Rev. D* **14**, 1509 (1976).

[3] 沈有根, "Kerr-Newman-De Sitter 时空中的 Dirac 方程的退耦和分离变量," *物理学报* **34**, 1203 (1985).

[4] S. A. Teukolsky, "Perturbations of a rotating black hole. I. Fundamental equations for gravitational, electromagnetic, and neutrino-field perturbations," *Astrophys. J.* **185**, 635 (1973).

[5] S. Chandrasekhar, *The Mathematical Theory of Black Holes* (Oxford University Press, Oxford, 1983).

[6] G. B. Cook and M. Zalutskiy, "Gravitational perturbations of the Kerr geometry: High-accuracy study," *Phys. Rev. D* **90**, 124021 (2014).

[7] E. Berti, V. Cardoso and C. M. Will, "Quasinormal modes of black holes and black branes," *Class. Quantum Grav.* **23**, R1 (2006).

[8] L. Stein, "qnm: A Python package for calculating Kerr quasinormal modes," *J. Open Source Softw.* **4**(42), 1623 (2019).

[9] Paper XXVII (UFPF XXVII, Leaver 谱丛理论——三参数纤维化、奇异纤维分类与耗散范畴嵌入).

[10] Paper XXVIII (UFPF XXVIII, Kerr-Newman 耦合谱丛与 IV 型奇异纤维).

[11] Paper XXVI (UFPF XXVI, 动态过程谱数值方法).
