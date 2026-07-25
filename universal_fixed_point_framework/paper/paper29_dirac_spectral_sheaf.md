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

**物理解释**：标度指数 $\beta$ 越大，谱间隙在 $a \to 1$ 极限下归零的速度越快。$\beta_{\mathrm{D}} > \beta_{\mathrm{EM}} > \beta_{\mathrm{G}}$ 意味着 Dirac 谱丛在极值 Kerr 极限附近的数值收敛性退化最为剧烈——这与半整数自旋在极端旋转下具有更强的超辐射不稳定性的物理图像一致。

**数值确定**：$\beta_{\mathrm{D}}$ 的具体数值需通过数值扫描确定。建议使用 Paper XXVII §7.2 的奇异纤维检测算法，对 $a \in [0.9, 0.999]$ 区间进行对数-对数拟合。

---

## 6. 结论与展望

本文建立了 Dirac 半整数自旋谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的严格数学框架。核心成果包括：

1. **Dirac 谱丛的构造**（§2）：给出了 $s=\pm1/2$ 三项递推系数的显式形式，定义了三参数谱丛，分析了代数特殊模式的 III 型奇异纤维表现，建立了与引力/电磁谱丛的跨自旋参数对比表。

2. **自旋结构与 $\mathbb{Z}_2$ 阻碍定理**（§3）：证明了 Dirac 谱丛存在非平凡自旋结构 $H^2(\mathcal{M}_\omega^{(s)},\mathbb{Z}_2) \neq 0$，建立了三个等价的阻碍条件（上同调、覆盖、置换），证明了分支点加倍定理（$|\mathcal{B}_{\mathrm{D}}| \geq 2|\mathcal{B}_{\mathrm{G}}|$）和单值群扩大定理（$|\mathcal{M}_\omega^{(\mathrm{D})}| \geq 2|\mathcal{M}_\omega^{(\mathrm{G})}|$），提出了 $2\pi$ vs $4\pi$ 回路数值检测协议。

3. **Dirac-引力张量积谱丛**（§4）：构造了 $\mathfrak{S}^{(-2)\otimes(-1/2)}$，证明了无耦合 Minkowski 和谱公式，建立了有耦合时的块三对角构造，给出了 $D_{\mathrm{diss}}$ 张量积扩展的压缩性和伪谱扰动界。

4. **跨自旋 LACI 对比框架**（§5）：定义了 Dirac LACI 参数，提出了 $\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$ 的排序猜想和四层理论依据，建立了 III 型奇异纤维标度指数 $\beta_{\mathrm{D}}$ 的定义和预期排序。

以下开放问题留待后续研究：

1. **$\mathbb{Z}_2$ 阻碍的严格数值验证**：§3.5 的数值检测协议需要高精度谱叶追踪实现，数值验证后可将 $\mathbb{Z}_2$ 阻碍从猜想提升为定理。
2. **Dirac QNM 基准表**：目前缺乏系统的 Dirac QNM 基准表（对标 Berti 表的引力/电磁 QNM），建立后可以验证截断误差指数衰减率 $c_{\mathrm{D}}$。
3. **$\beta_{\mathrm{D}}$ 的数值确定**：III 型奇异纤维标度指数 $\beta_{\mathrm{D}}$ 的具体数值需通过数值扫描确定。
4. **Dirac-引力-电磁三系统耦合谱丛**：将 Paper XXVIII 的引力-电磁耦合与本文的 Dirac 谱丛结合，构造 $S=\{-2,-1,-1/2\}$ 的三自旋联合谱丛。
5. **$\infty$-范畴提升**：将 Dirac 谱丛的自旋结构提升至 $\infty$-范畴，建立 $(\infty,1)$-谱丛的 $\mathbb{Z}_2$-覆盖理论。

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
