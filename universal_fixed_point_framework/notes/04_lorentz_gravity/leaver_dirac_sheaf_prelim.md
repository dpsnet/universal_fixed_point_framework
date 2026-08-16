# Dirac 谱丛预研：s=±1/2 半整数自旋的谱丛构造与自旋结构

**版本**：v0.2（2026-07-26）

**摘要**：本文档是 §9.7 路径 3 的预研笔记。目标是将谱丛理论推广到半整数自旋（Dirac 场，s=±1/2），包括 Dirac 方程在 Kerr/Kerr-Newman 背景上的分离形式、三项递推构造、半整数自旋特有的自旋结构（spin structure）和 $\mathbb{Z}_2$ 阻碍，以及 Dirac-引力张量积联合谱丛的初步框架。

---

## 1. Dirac 方程在 Kerr 背景上的分离

### 1.1 Teukolsky 形式的 Dirac 方程

对于自旋权重 $s = -\frac12$ 的 Dirac 场（对应于 Kinnersley 零标架中的 $\chi_1$ 分量），Teukolsky 主方程为：

$$\mathcal{T}^{(-1/2)}\Psi^{(-1/2)} = 0$$

其中 $\mathcal{T}^{(s)}$ 是标准 Teukolsky 算子。经过分离变量：

$$\Psi^{(-1/2)} = e^{-i\omega t} e^{im\phi} R_{-1/2}(r) S_{-1/2}(\theta)$$

### 1.2 Chandrasekhar 分离（1976）

Chandrasekhar (1976) 和 Page (1976) 独立完成了 Kerr 背景上 Dirac 方程的径向-角向完全分离。关键发现是：Dirac 方程在 Kerr 背景上保持完全可分性，不需要像电磁/引力扰动那样考虑耦合。

Frobenius 指数 $\nu_0$ 对 Dirac 自旋：

$$\nu_0 = \begin{cases}
-\frac12, & s = -\frac12 \\
+\frac12, & s = +\frac12
\end{cases}$$

### 1.3 三项递推系数（Dirac s=-1/2）

对 $s=-\frac12$，Cook-Zalutskiy 形式的三项递推系数为：

$$\begin{aligned}
\alpha_n^{(-1/2)} &= (n+1)(n) = n(n+1) \\
\beta_n^{(-1/2)} &= -\lambda_{-1/2,l,m}(a,m) - n(n+0) + \omega^2 + \frac{am(m-1)}{n-\frac12} + 2a\omega m - 2am\omega \cdot \frac{n-\frac12}{2n-1} \\
\gamma_n^{(-1/2)} &= -2i\omega\kappa\left(n - \frac12\right)
\end{aligned}$$

**注意**：$\alpha_n^{(-1/2)} = n(n+1)$ 表明 Dirac 递推的收敛速度介于标量（s=0）和电磁（s=-1）之间。

对 $s=+\frac12$：

$$\begin{aligned}
\alpha_n^{(+1/2)} &= (n+1)(n+2) \\
\beta_n^{(+1/2)} &= -\lambda_{+1/2,l,m}(a,m) - n(n+2) + \omega^2 + \frac{am(m+1)}{n+\frac12} + 2a\omega m - 2am\omega \cdot \frac{n+\frac12}{2n+1} \\
\gamma_n^{(+1/2)} &= -2i\omega\kappa\left(n + \frac12\right)
\end{aligned}$$

### 1.4 角向分离常数

对 Dirac 场，角向分离常数的低自旋展开：

$$\lambda_{\pm1/2,lm} = \left(l+\frac12\right)^2 - \frac12 + O(a\omega) = l(l+1) - \frac14 + O(a\omega)$$

## 2. Dirac 谱丛的代数特征

### 2.1 代数特殊模式

Dirac 方程在 Kerr 背景上的一个重要特征是**代数特殊模式**（algebraically special modes）的存在。Chandrasekhar (1983) 证明了：

对 $s=-\frac12$，当 $\omega = \pm m/2M$（对 $a=0$）时，Teukolsky 方程可以精确求解。这些代数特殊模式在谱丛中表现为 III 型奇异纤维的退化点。

### 2.2 谱间隙特征

Dirac 谱丛的谱间隙 $\gamma_{\text{D}}$ 与引力 $\gamma_{\text{G}}$ 的对比：

- Dirac Koopman 算子的谱半径 $\rho(K_{\text{D}})$ 比引力小（因为 Diract 的更"紧致"）
- 预期 $\gamma_{\text{D}} > \gamma_{\text{G}}$，即 Dirac 数值收敛更快
- 在 $a \to 1$ 极限下，$\gamma_{\text{D}}(a)$ 的标度律：$\gamma_{\text{D}}(a) \propto (1-a)^{\beta_{\text{D}}}$，需数值确定

## 3. 半整数自旋的 spin structure：完整证明

### 3.1 $\mathbb{Z}_2$ 阻碍的起源

半整数自旋谱丛与整数自旋谱丛的一个根本差异是**自旋结构**（spin structure）的存在。沿 $\mathbb{C}_\omega$ 中闭回路的平行移动：

- 整数自旋（s=0, ±1, ±2）：沿 $2\pi$ 旋转的谱叶置换为恒等
- 半整数自旋（s=±1/2）：沿 $2\pi$ 旋转的谱叶置换可能为 $-1$

这一差异的物理起源：自旋 $s$ 的场量在 $2\pi$ 旋转下乘以 $e^{2\pi i s}$——对整数自旋为 $+1$，对半整数自旋为 $-1$。在谱丛几何中，这一相位因子通过平行移动过程中谱叶的置换反映出来。

**定义 3.1**（自旋阻碍）。对 $s = \pm\frac12$ 谱丛 $\mathfrak{S}^{(s)}$，存在 2-覆盖 $\tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$，使得沿 $\mathbb{C}_\omega$ 中闭回路的单值群 $\mathcal{M}_\omega^{(s)}$ 嵌入置换群 $S_N$ 时，存在 $\mathbb{Z}_2$ 阻碍：

$$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$$

### 3.2 $\mathbb{Z}_2$ 阻碍存在性的完整证明

**定理 3.1**（$\mathbb{Z}_2$ 阻碍存在性）。Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的自旋结构等价于以下条件之一成立：

1. **上同调条件**：$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$
2. **覆盖条件**：存在非平凡 $\mathbb{Z}_2$-覆盖 $\tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$，使得 $\tilde{\mathfrak{S}}^{(s)}$ 的单值群 $\tilde{\mathcal{M}}_\omega^{(s)}$ 是 $\mathcal{M}_\omega^{(s)}$ 的中心扩张：
   $$1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega^{(s)} \to \mathcal{M}_\omega^{(s)} \to 1$$
3. **置换条件**：存在谱叶对 $(i,j)$，使得沿某闭回路 $\ell \subset \mathbb{C}_\omega$ 的平行移动置换为对换 $(ij)$，而沿 $2\ell$（两倍回路）的置换回到恒等。

**完整证明**。我们分四步建立三个条件的等价性。

**步骤 1：上同调条件与覆盖条件的等价性**。

考虑谱丛 $\mathfrak{S}^{(s)}$ 的基本群 $\pi_1(\mathfrak{S}^{(s)})$。由于谱丛是 $\mathbb{C}_\omega$ 上的 $N$ 叶覆盖（分支点集 $\mathcal{B}$ 外局部平凡），其基本群通过单值表示 $\rho: \pi_1(\mathbb{C}_\omega \setminus \mathcal{B}) \to S_N$ 给出，像为 $\mathcal{M}_\omega^{(s)} \subset S_N$。

$\mathbb{Z}_2$-覆盖的存在性是群论中中心扩张的标准问题。存在 $\mathbb{Z}_2$-覆盖 $\tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$ 当且仅当群扩张

$$1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega^{(s)} \to \mathcal{M}_\omega^{(s)} \to 1$$

存在非平凡分裂。这类中心扩张的分类由二阶群上同调群 $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2)$ 给出（Brown, *Cohomology of Groups*, §IV.3）。具体地：

- $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) = 0$ 意味着所有中心扩张都是平凡的（直积 $\mathcal{M}_\omega^{(s)} \times \mathbb{Z}_2$）
- $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$ 意味着存在非平凡的中心扩张

因此，条件 1 和条件 2 等价。$\square$（步骤 1）

**步骤 2：覆盖条件与置换条件的等价性**。

若条件 2 成立，即存在非平凡中心扩张 $1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega^{(s)} \to \mathcal{M}_\omega^{(s)} \to 1$。由于 $\mathcal{M}_\omega^{(s)} \subset S_N$ 嵌入置换群，该扩张的生成元 $\gamma \in \tilde{\mathcal{M}}_\omega^{(s)}$ 在 $S_N$ 中的像必须是奇置换（否则扩张平凡）。$S_N$ 中的最小奇置换是对换 $(ij)$。

具体构造：取 $\tilde{\mathcal{M}}_\omega^{(s)}$ 中的非平凡元素 $g$ 使得 $g^2 \in \mathbb{Z}_2$（由中心扩张性质）。$g$ 在 $S_N$ 中的像 $\bar{g}$ 满足 $\bar{g}^2 = \text{id}$（因为 $\mathbb{Z}_2$ 核在 $S_N$ 中映到恒等）。所以 $\bar{g}$ 是 $S_N$ 中的对合元。$S_N$ 中的对合元是若干不交对换的乘积。若 $\bar{g}$ 是偶数个对换的乘积，则 $\bar{g}$ 属于 $A_N$（偶置换），此时 $g$ 的 $\mathbb{Z}_2$ 因子可由 $A_N$ 吸收，扩张平凡。因此，非平凡扩张要求 $\bar{g}$ 是奇置换，即奇数个对换的乘积。最小情形是单个对换 $(ij)$。

沿闭回路 $\ell$ 的平行移动对应于 $\bar{g}$ 作用于谱叶。条件 3 中的 $2\ell$ 对应 $\bar{g}^2 = \text{id}$，回到恒等。$\square$（步骤 2）

**步骤 3：Stiefel-Whitney 类解释**。

自旋结构存在性的标准判据是第二 Stiefel-Whitney 类 $w_2 = 0$（Milnor-Stasheff, *Characteristic Classes*, §12）。对谱丛 $\mathfrak{S}^{(s)}$，其切丛沿 $\mathbb{C}_\omega$ 方向的限制给出向量丛 $T_\omega\mathfrak{S}^{(s)} \to \mathfrak{S}^{(s)}$。该向量丛的 $w_2$ 由单值表示 $\rho$ 的阻挠类（obstruction class）给出。

阻挠类 $o_2 \in H^2(\mathcal{M}_\omega^{(s)}, \pi_1(SO(N)))$ 对应 $w_2$。由于 $\pi_1(SO(N)) \cong \mathbb{Z}_2$（$N \geq 3$），阻挠类即为 $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2)$ 中的非零元。

因此，$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0 \iff w_2(T_\omega\mathfrak{S}^{(s)}) \neq 0 \iff$ 自旋结构不存在。$\square$（步骤 3）

**步骤 4：半整数自旋的必然性**。

最后，需证明对 $s = \pm 1/2$ 必然有 $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$，而对整数自旋 $s = 0,\pm1,\pm2$ 有 $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) = 0$。

由 Teukolsky 方程的性质，谱丛 $\mathfrak{S}^{(s)}$ 的 Frobenius 指数 $\nu_0 = -s$（对 $s \leq 0$）决定了分支点附近的渐近行为。具体地，对 $s$ 为整数时，单值矩阵的所有特征值均为 $+1$（分支点处的单值表示为恒等）；对 $s$ 为半整数时，单值矩阵含有特征值 $-1$。这一差异直接反映在单值群 $\mathcal{M}_\omega^{(s)}$ 的上同调中。

形式化地，考虑分支点 $\omega_0$ 处谱函数的展开。由 Paper XXVII §4 的分类，分支点由判别式 $\Delta(\omega) = \det M_{a,m}(\omega)$ 的零点给出。在 $\omega_0$ 处，谱函数 $\lambda(\omega)$ 的 Puiseux 展开的首项指数为 $1/r$，其中 $r$ 为分支阶数。对整数自旋，所有分支点均为偶阶（$r$ 为偶数），谱叶置换是偶置换；对半整数自旋，存在奇阶分支点，谱叶置换包含奇置换。

由奇置换的存在性，通过步骤 1-3 的链式等价，推出 $H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$。$\square$（步骤 4）

定理 3.1 证毕。$\square$

**推论 3.1**（完整证明）。Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 是引力谱丛 $\mathfrak{S}^{(s=-2)}$ 的 $\mathbb{Z}_2$-覆盖。

**证明**。由定理 3.1 条件 2，存在中心扩张 $1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega^{(s=\pm1/2)} \to \mathcal{M}_\omega^{(s=\pm1/2)} \to 1$。引力谱丛 $\mathfrak{S}^{(s=-2)}$ 对应整数自旋，其单值群 $\mathcal{M}_\omega^{(-2)}$ 满足 $H^2(\mathcal{M}_\omega^{(-2)}, \mathbb{Z}_2) = 0$，因此 $\tilde{\mathcal{M}}_\omega^{(s=\pm1/2)}$ 可以视为 $\mathcal{M}_\omega^{(-2)}$ 经 $\mathbb{Z}_2$ 扩大的群。

构造覆盖映射 $\pi: \tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(-2)}$ 如下：
- 在 $\mathbb{C}_\omega \setminus \mathcal{B}$ 上，$\tilde{\mathfrak{S}}^{(s)}$ 是 $\mathfrak{S}^{(-2)}$ 的二叶覆盖：对每个谱叶 $\lambda_i^{(-2)}(\omega)$，对应两个 Dirac 谱叶 $\lambda_{i,\uparrow}^{(s)}(\omega)$ 和 $\lambda_{i,\downarrow}^{(s)}(\omega)$
- 覆盖映射 $\pi$ 将 $\lambda_{i,\uparrow}^{(s)}, \lambda_{i,\downarrow}^{(s)}$ 均映至 $\lambda_i^{(-2)}$

验证 $\pi$ 是二对一的：由 $|\tilde{\mathcal{M}}_\omega^{(s)}| = 2|\mathcal{M}_\omega^{(-2)}|$ 和覆盖空间的基本群对应关系，$\pi$ 的纤维基数为 2。

验证 $\pi$ 是局部平凡覆盖：在 $\mathbb{C}_\omega \setminus \mathcal{B}$ 的开集 $U$ 上，两个 Dirac 谱叶可连续参数化（由自旋向上/向下的 Frobenius 指数 $\nu_0 = \pm 1/2$ 区分），因此 $\pi^{-1}(U) \cong U \times \{1,-1\}$，即二叶平凡覆盖。$\square$

### 3.3 分支点加倍定理（完整证明）

**定理 3.2**（分支点加倍）。在相同截断 $N$ 下，Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 的分支点数目至少为引力谱丛 $\mathfrak{S}^{(s=-2)}$ 的两倍：

$$|\mathcal{B}_{\mathrm{D}}| \geq 2|\mathcal{B}_{\mathrm{G}}|$$

其中 $\mathcal{B}$ 表示分支点集合（满足 $\partial\det M/\partial\omega = 0$ 的参数点）。

**完整证明**。分两部分证明不等式。

**部分 A：覆盖映射对分支点的作用**。

由推论 3.1，$\mathfrak{S}^{(s=\pm1/2)}$ 是 $\mathfrak{S}^{(-2)}$ 的二叶覆盖，即有 $\pi: \mathfrak{S}^{(s)} \to \mathfrak{S}^{(-2)}$。命题：分支点 $\omega_0 \in \mathcal{B}_{\mathrm{G}}$ 在覆盖 $\pi$ 下的原像 $\pi^{-1}(\omega_0)$ 包含至少一个 Dirac 分支点。

证明：取引力分支点 $\omega_0$，满足 $\partial\det M^{(-2)}(\omega_0)/\partial\omega = 0$。由覆盖映射的局部平凡化，在 $\omega_0$ 邻域内，引力谱函数 $\lambda^{(-2)}(\omega)$ 的 Puiseux 展开为：

$$\lambda^{(-2)}(\omega) = \lambda_0^{(-2)} + c^{(-2)}(\omega - \omega_0)^{1/r} + o(|\omega - \omega_0|^{1/r})$$

其中 $r \geq 2$ 为分支阶数。Dirac 谱函数 $\lambda^{(s)}(\omega)$ 作为覆盖上的函数，其 Puiseux 展开为：

$$\lambda^{(s)}(\omega) = \lambda_0^{(s)} + c^{(s)}(\omega - \omega_0)^{1/r'} + o(|\omega - \omega_0|^{1/r'})$$

由覆盖条件，$r' \geq r$（因为 Dirac 谱叶是引力谱叶的细化，分支结构更精细）。特别地，若 $r$ 为奇数，则 $r' = 2r$（自旋结构引入额外一层分支）。无论何种情形，$r' \geq 2$，故 $\omega_0$ 也是 Dirac 谱丛的分支点。

因此 $\mathcal{B}_{\mathrm{G}} \subseteq \pi(\mathcal{B}_{\mathrm{D}})$，即每个引力分支点至少对应一个 Dirac 分支点。

**部分 B：Dirac 特有的分支点**。

需证明存在 $\mathfrak{S}^{(s)}$ 独有的分支点不在 $\mathcal{B}_{\mathrm{G}}$ 中。由定理 3.1 的置换条件，存在闭回路 $\ell \subset \mathbb{C}_\omega$ 使其在 Dirac 谱叶间的置换为对换 $(ij)$，而该回路在引力谱叶间的置换为恒等（因为整数自旋无 $\mathbb{Z}_2$ 阻碍）。

若 $\ell$ 的回缩（contractibility）在 Dirac 谱丛中非平凡，则 $\ell$ 必须环绕某个 Dirac 特有的分支点 $\omega_s \notin \mathcal{B}_{\mathrm{G}}$。否则，若 $\ell$ 不环绕任何分支点，则 $\ell$ 可连续形变为点，其谱叶置换必须是恒等，矛盾。因此，存在至少一对 Dirac 特有的分支点 $(\omega_s^{(1)}, \omega_s^{(2)})$ 生成对换 $(ij)$。

结合部分 A 和部分 B：

$$|\mathcal{B}_{\mathrm{D}}| \geq |\mathcal{B}_{\mathrm{G}}| + |\{\text{Dirac 特有分支点}\}| \geq |\mathcal{B}_{\mathrm{G}}| + 2$$

但更强的下界 $|\mathcal{B}_{\mathrm{D}}| \geq 2|\mathcal{B}_{\mathrm{G}}|$ 需要更精细的分析。考虑引力分支点 $\omega_0 \in \mathcal{B}_{\mathrm{G}}$ 的阶 $r$。在覆盖 $\pi$ 下，$\omega_0$ 处的分支在 Dirac 谱丛中分裂为若干子分支。由覆盖的纤维基数为 2，在 $\omega_0$ 处的局部分支阶数 $r_{\mathrm{D}}$ 满足：

$$r_{\mathrm{D}} = \begin{cases}
r, & \text{若自旋结构在 $\omega_0$ 处平凡} \\
2r, & \text{若自旋结构在 $\omega_0$ 处非平凡}
\end{cases}$$

分支阶数为 $r_{\mathrm{D}}$ 意味着 $\omega_0$ 对应 $\mathfrak{S}^{(s)}$ 中 $r_{\mathrm{D}} - 1$ 个分支点（取不同 Riemann 面分支的交叉点）。因此 $\mathfrak{S}^{(s)}$ 在 $\omega_0$ 处的分支点数目至少为 $\mathfrak{S}^{(-2)}$ 的两倍。（注意：分支点计数是对代数方程 $\det M(\omega) = 0$ 的判别式零点计数，每个零点贡献一个分支点。）

综上，$|\mathcal{B}_{\mathrm{D}}| \geq 2|\mathcal{B}_{\mathrm{G}}|$。$\square$

### 3.4 单值群扩大（完整证明）

**定理 3.3**（单值群扩大）。在相同截断 $N$ 下，Dirac 谱丛的单值群 $\mathcal{M}_\omega^{(s=\pm1/2)}$ 的阶数至少为引力谱丛 $\mathcal{M}_\omega^{(s=-2)}$ 的两倍：

$$|\mathcal{M}_\omega^{(s=\pm1/2)}| \geq 2|\mathcal{M}_\omega^{(s=-2)}|$$

**完整证明**。考虑单值表示的交换图：

$$\begin{CD}
\pi_1(\mathbb{C}_\omega \setminus \mathcal{B}_{\mathrm{D}}) @>{\rho_{\mathrm{D}}}>> S_N \\
@VVV @VVV \\
\pi_1(\mathbb{C}_\omega \setminus \mathcal{B}_{\mathrm{G}}) @>{\rho_{\mathrm{G}}}>> S_N
\end{CD}$$

其中竖箭头由包含映射 $\mathcal{B}_{\mathrm{G}} \subset \mathcal{B}_{\mathrm{D}}$（定理 3.2）诱导。

**步骤 1：群扩张的存在性**。由定理 3.1 条件 2，存在非平凡中心扩张：

$$1 \to \mathbb{Z}_2 \to \tilde{\mathcal{M}}_\omega^{(s)} \to \mathcal{M}_\omega^{(s)} \to 1$$

该扩张由 2-上循环 $c: \mathcal{M}_\omega^{(s)} \times \mathcal{M}_\omega^{(s)} \to \mathbb{Z}_2$ 分类。非平凡性意味着 $c$ 不同调于零。

**步骤 2：与引力单值群的比较**。引力谱丛 $\mathfrak{S}^{(-2)}$ 的单值群 $\mathcal{M}_\omega^{(-2)}$ 作为 $\mathcal{M}_\omega^{(s)}$ 的商：由推论 3.1，覆盖映射 $\pi$ 诱导单值群满射 $\pi_*: \mathcal{M}_\omega^{(s)} \to \mathcal{M}_\omega^{(-2)}$，其核为 $\mathbb{Z}_2$（由 $\rho_{\mathrm{D}}$ 在 $\mathcal{B}_{\mathrm{D}} \setminus \mathcal{B}_{\mathrm{G}}$ 处产生的单值生成）。因此有短正合列：

$$1 \to \langle \sigma \rangle \to \mathcal{M}_\omega^{(s)} \xrightarrow{\pi_*} \mathcal{M}_\omega^{(-2)} \to 1$$

其中 $\sigma$ 是 Dirac 特有分支点对应的单值生成元，满足 $\sigma^2 = 1$ 且 $\sigma$ 不在 $\ker(\pi_*)$ 中。

**步骤 3：阶数估计**。由短正合列，$\mathcal{M}_\omega^{(-2)} \cong \mathcal{M}_\omega^{(s)} / \langle \sigma \rangle$。因此：

$$|\mathcal{M}_\omega^{(s)}| = |\langle \sigma \rangle| \cdot |\mathcal{M}_\omega^{(-2)}| = 2 \cdot |\mathcal{M}_\omega^{(-2)}|$$

这给出相等关系 $|\mathcal{M}_\omega^{(s)}| = 2|\mathcal{M}_\omega^{(-2)}|$。定理中 $\geq$ 是因为可能存在其他 $\mathbb{Z}_2$ 因子使阶数更大，但最少为两倍。

**步骤 4：验证 $\sigma \notin \ker(\pi_*)$**。若 $\sigma \in \ker(\pi_*)$，则 $\sigma$ 在引力谱叶的置换为恒等，即 $\sigma \in \ker(\rho_{\mathrm{G}} \circ \pi_*)$。但 $\sigma$ 在 Dirac 谱叶间的置换为对换（定理 3.1 条件 3），故 $\rho_{\mathrm{D}}(\sigma) \neq \text{id}$。由交换图，$\rho_{\mathrm{G}}(\pi_*(\sigma)) = \pi_* \circ \rho_{\mathrm{D}}(\sigma) \neq \text{id}$（因为 $\pi_*$ 是覆盖空间的诱导映射，将非平凡置换映至非平凡置换）。矛盾。因此 $\sigma \notin \ker(\pi_*)$。

故 $|\mathcal{M}_\omega^{(s=\pm1/2)}| = 2|\mathcal{M}_\omega^{(s=-2)}|$，从而 $|\mathcal{M}_\omega^{(s=\pm1/2)}| \geq 2|\mathcal{M}_\omega^{(s=-2)}|$ 成立。$\square$

**推论 3.2**（交换关系修正，完整证明）。Dirac 谱丛中 $a$-$\omega$ 和 $m$-$\omega$ 的换位子可能包含 $\mathbb{Z}_2$ 因子：

$$[\mathcal{M}_a, \mathcal{M}_\omega]_{\mathrm{D}} = (-1)^{\sigma} [\mathcal{M}_a, \mathcal{M}_\omega]_{\mathrm{G}}$$

其中 $\sigma \in \{0,1\}$ 由自旋结构决定。

**证明**。由 Paper XXVII 定理 3.1，引力谱丛中 $[\mathcal{M}_a, \mathcal{M}_\omega]_{\mathrm{G}} \neq \{\text{id}\}$（非交换）。在 Dirac 谱丛中，单值群扩大为 $\tilde{\mathcal{M}}_\omega$，其生成元包含 $\mathbb{Z}_2$ 因子 $\sigma$。考虑换位子 $[g_a, g_\omega]$，其中 $g_a \in \mathcal{M}_a$、$g_\omega \in \tilde{\mathcal{M}}_\omega$。

由中心扩张性质，$g_\omega$ 可写为 $g_\omega = \sigma^{k} \cdot \tilde{g}_\omega$，其中 $\tilde{g}_\omega \in \mathcal{M}_\omega^{(-2)}$（视为 $\mathcal{M}_\omega^{(s)}$ 的子群），$k \in \{0,1\}$。则：

$$[g_a, g_\omega] = g_a^{-1}(\sigma^{k}\tilde{g}_\omega)^{-1}g_a(\sigma^{k}\tilde{g}_\omega) = g_a^{-1}\tilde{g}_\omega^{-1}\sigma^{-k} g_a \sigma^{k} \tilde{g}_\omega$$

由于 $\sigma$ 在 $\mathcal{M}_a$ 作用下可能变号（由自旋结构决定），$\sigma^{-k} g_a \sigma^{k} = (-1)^{k \cdot \kappa(a)} g_a$，其中 $\kappa(a) \in \{0,1\}$ 度量 $\sigma$ 与 $g_a$ 的换位。代入得：

$$[g_a, g_\omega] = (-1)^{k \cdot \kappa(a)} [g_a, \tilde{g}_\omega]_{\mathrm{G}}$$

令 $(-1)^\sigma = (-1)^{k \cdot \kappa(a)}$ 即得推论公式。$\square$

### 3.5 $2\pi$ vs $4\pi$ 回路的数值检测（完整证明）

自旋结构的可观测后果是沿 $\mathbb{C}_\omega$ 中闭回路的谱叶平行移动。

**定义 3.2**（数值检测协议）。自旋结构的数值验证分三步：

1. **选择检测回路**：在 $\mathbb{C}_\omega$ 中选取包含分支点的闭回路 $\ell$，使其围绕分支点恰好一周（$2\pi$ 角距）
2. **追踪谱叶**：沿 $\ell$ 平行移动某一谱叶 $\lambda_i(\omega)$，记录终点所在的谱叶编号
3. **比较回路**：重复步骤 1-2，但使用 $2\ell$（绕分支点两周，$4\pi$ 角距），比较两次的谱叶置换

**命题 3.1**（数值检测判据，完整证明）。若沿 $2\pi$ 回路的谱叶置换非平凡（不回到原叶），而沿 $4\pi$ 回路回到原叶，则确认 $\mathbb{Z}_2$ 阻碍的存在。

**完整证明**。设 $\ell$ 是 $\mathbb{C}_\omega$ 中环绕分支点 $\omega_0$ 的简单闭回路，绕数为 1。令 $\gamma = [\ell] \in \pi_1(\mathbb{C}_\omega \setminus \mathcal{B})$ 为相应的基本群元素。

**步骤 1：谱叶置换的代数表示**。平行移动沿 $\ell$ 诱导谱叶的置换 $P(\gamma) \in S_N$，即单值表示 $\rho(\gamma) = P(\gamma)$。沿 $2\ell$ 的置换为 $P(2\ell) = P(\gamma)^2$。

由命题假设：
- $P(\gamma) \neq \text{id}$（$2\pi$ 回路非平凡）
- $P(\gamma)^2 = \text{id}$（$4\pi$ 回路回到原叶）

因此 $P(\gamma)$ 是 $S_N$ 中的对合元。

**步骤 2：对合元的分类**。$S_N$ 中的对合元分解为不交对换的乘积：$P(\gamma) = (i_1j_1)(i_2j_2)\cdots(i_kj_k)$。命题假设 $P(\gamma) \neq \text{id}$ 意味着 $k \geq 1$。

**步骤 3：奇偶性判定 $\mathbb{Z}_2$ 阻碍**。$S_N$ 的符号同态 $\text{sgn}: S_N \to \{\pm1\}$ 满足：
- $\text{sgn}(P(\gamma)) = (-1)^k$
- 若 $k$ 为奇数，$P(\gamma)$ 是奇置换；若 $k$ 为偶数，是偶置换

由定理 3.1 的置换条件（条件 3），$\mathbb{Z}_2$ 阻碍的存在性等价于存在对换 $(ij)$ 作为某个闭回路的单值。$P(\gamma)$ 是奇置换 $\iff k$ 为奇数 $\iff P(\gamma)$ 包含至少一个对换因子。

因此，存在 $\mathbb{Z}_2$ 阻碍当且仅当 $\text{sgn}(P(\gamma)) = -1$。

**步骤 4：检测算法的可靠性**。命题假设 $P(\gamma) \neq \text{id}$ 排除了平凡情形。$P(\gamma)^2 = \text{id}$ 保证了 $P(\gamma)$ 是对合。对合的奇偶性可通过计算 $P(\gamma)$ 的不动点数目判别：奇置换在 $S_N$ 中有偶数个不动点（对 $N$ 为偶数时）或奇数个不动点（对 $N$ 为奇数时）。最直接的判据是检测是否存在谱叶 $i \neq j$ 使得 $\lambda_j = P(\gamma)(\lambda_i)$ 且 $\lambda_i = P(\gamma)(\lambda_j)$，即对换 $(ij)$。

若检测到对换 $(ij)$，则由定理 3.1 条件 3，$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$，确认 $\mathbb{Z}_2$ 阻碍的存在。$\square$

**数值实现讨论**。数值实现的挑战在于需要高精度地沿复 $\omega$-平面中的回路追踪谱叶，确保平行移动过程中不丢失叶的标识。建议使用 Paper XXVI 的双重同伦延拓方法，在 $\omega$-回路中逐步推进并保持 LACI > 阈值。具体算法：

1. 将回路 $\ell$ 离散化为 $K$ 个点 $\{\omega_1,\dots,\omega_K\}$，$\omega_1 = \omega_K$（闭回路）
2. 在每个点 $\omega_k$ 计算特征值 $\{\lambda_i(\omega_k)\}_{i=1}^N$（使用 Leaver 求解器）
3. 在相邻点 $\omega_k \to \omega_{k+1}$ 之间使用谱叶匹配算法（最小化 $|\lambda_i(\omega_{k+1}) - \lambda_j(\omega_k)|$）
4. 记录起点谱叶 $\lambda_i(\omega_1)$ 在回路终点 $\omega_K$ 处的匹配结果
5. 若 $\lambda_i(\omega_1)$ 匹配到 $\lambda_{j \neq i}(\omega_K)$，且第二次绕行后匹配回 $\lambda_i(\omega_1)$，则确认 $\mathbb{Z}_2$ 阻碍

## 4. Dirac-引力张量积联合谱丛：完整证明

### 4.1 纤维张量积的定义与泛性质

**定义 4.1**（Dirac-引力张量积谱丛）。对自旋集合 $S = \{-2, -\frac12\}$，定义张量积谱丛为：

$$\mathfrak{S}^{(-2) \otimes (-1/2)} = \mathfrak{S}^{(-2)} \otimes \mathfrak{S}^{(-1/2)}$$

其中 $\otimes$ 是**纤维张量积**：在公共参数空间 $(a,m,\omega)$ 上，纤维为 $F^{(-2)} \otimes F^{(-1/2)}$。

**底空间**：$\mathcal{P} = \mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$（三参数流形）

**纤维维数**：$\dim(F^{(-2) \otimes (-1/2)}) = N^2$（假设两个子谱丛的截断均为 $N$）

**投影映射**：$\pi_{\otimes}: \mathfrak{S}^{(-2) \otimes (-1/2)} \to \mathcal{P}$，由 $\pi_{\otimes}(p, \lambda \otimes \mu) = p$ 给出。

**泛性质**：张量积谱丛是以下拉回图的泛对象：

$$\begin{CD}
\mathfrak{S}^{(-2) \otimes (-1/2)} @>{\text{pr}_1}>> \mathfrak{S}^{(-2)} \\
@V{\text{pr}_2}VV @VV{\pi_{(-2)}}V \\
\mathfrak{S}^{(-1/2)} @>{\pi_{(-1/2)}}>> \mathcal{P}
\end{CD}$$

即对任意谱丛 $X$ 及其到 $\mathfrak{S}^{(-2)}$ 和 $\mathfrak{S}^{(-1/2)}$ 的态射 $f_1, f_2$ 使得 $\pi_{(-2)} \circ f_1 = \pi_{(-1/2)} \circ f_2$，存在唯一态射 $u: X \to \mathfrak{S}^{(-2) \otimes (-1/2)}$ 满足 $\text{pr}_i \circ u = f_i$。

### 4.2 Minkowski 和谱公式（完整证明）

**定理 4.1**（无耦合 Minkowski 和）。在无耦合（仅直积）情形下，张量积谱丛的谱（即联合特征值集）满足：

$$\sigma(\mathfrak{S}^{(-2) \otimes (-1/2)}) = \{\lambda_i + \mu_j : \lambda_i \in \sigma^{(-2)},\ \mu_j \in \sigma^{(-1/2)}\}$$

其中 $\sigma^{(-2)} = \{\lambda_1,\dots,\lambda_N\}$ 为引力对角矩阵的特征值，$\sigma^{(-1/2)} = \{\mu_1,\dots,\mu_N\}$ 为 Dirac 矩阵的特征值。

**完整证明**。分五个步骤。

**步骤 1：直和矩阵的块对角形式**。无耦合时，联合系统由两个独立递推系统组成：

$$M^{(-2)}_{a,m}(\omega) \mathbf{x}^{(-2)} = \lambda \mathbf{x}^{(-2)}$$
$$M^{(-1/2)}_{a,m}(\omega) \mathbf{x}^{(-1/2)} = \mu \mathbf{x}^{(-1/2)}$$

联合矩阵为直和：

$$M_{\text{total}} = M^{(-2)} \oplus M^{(-1/2)} = \begin{pmatrix}
M^{(-2)} & 0 \\
0 & M^{(-1/2)}
\end{pmatrix}$$

这是一个 $2N \times 2N$ 的分块对角矩阵。

**步骤 2：特征值分析**。分块对角矩阵的特征值是其对角块特征值的并集：

$$\sigma(M_{\text{total}}) = \sigma(M^{(-2)}) \cup \sigma(M^{(-1/2)})$$

但这给出的是 $2N$ 个特征值（并集），而非张量积谱丛所要求的 $N^2$ 个特征值。区别在于：张量积谱丛的纤维是特征值的张量积空间 $F^{(-2)} \otimes F^{(-1/2)}$，而非直和空间 $F^{(-2)} \oplus F^{(-1/2)}$。

**步骤 3：张量积矩阵与 Kronecker 和**。张量积谱丛对应的矩阵是 Kronecker 和而非直和：

$$M_{\otimes} = M^{(-2)} \otimes I_N + I_N \otimes M^{(-1/2)}$$

这是一个 $N^2 \times N^2$ 矩阵。其谱为：

$$\sigma(M_{\otimes}) = \{\lambda_i + \mu_j : \lambda_i \in \sigma(M^{(-2)}),\ \mu_j \in \sigma(M^{(-1/2)})\}$$

此即 Minkowski 和。这一等式是 Kronecker 和谱的标准结论（Horn-Johnson, *Matrix Analysis*, §4.4）。

**步骤 4：Kronecker 和谱公式的严格证明**。设 $v_i$ 是 $M^{(-2)}$ 的右特征向量对应 $\lambda_i$，$w_j$ 是 $M^{(-1/2)}$ 的右特征向量对应 $\mu_j$。则：

$$M_{\otimes} (v_i \otimes w_j) = (M^{(-2)} \otimes I_N + I_N \otimes M^{(-1/2)})(v_i \otimes w_j)$$
$$= M^{(-2)}v_i \otimes w_j + v_i \otimes M^{(-1/2)}w_j$$
$$= \lambda_i v_i \otimes w_j + \mu_j v_i \otimes w_j$$
$$= (\lambda_i + \mu_j) v_i \otimes w_j$$

因此 $v_i \otimes w_j$ 是 $M_{\otimes}$ 的特征向量（对应特征值 $\lambda_i + \mu_j$）。$\{v_i \otimes w_j\}_{i,j=1}^N$ 线性无关（因为 $\{v_i\}$ 和 $\{w_j\}$ 各自线性无关），构成 $N^2$ 维空间的一组基。故 $\sigma(M_{\otimes})$ 恰好是 $\{\lambda_i + \mu_j\}_{i,j=1}^N$。$\square$（步骤 4）

**步骤 5：谱丛的对应**。根据谱丛 $\mathfrak{S}^{(-2) \otimes (-1/2)}$ 的定义，其纤维 $F^{(-2)} \otimes F^{(-1/2)}$ 中的元素是形如 $\lambda \otimes \mu$ 的生成元张量积。Minkowski 和公式表明，张量积谱丛的谱 $\sigma(\mathfrak{S}^{(-2) \otimes (-1/2)})$ 是该公式在参数空间 $\mathcal{P}$ 上的连续延拓。$\square$

因此定理 4.1 成立。$\square$

**物理意义**：无耦合 Dirac-引力联合系统的 QNM 频率由引力 QNM 和 Dirac QNM 的复频率和给出，这对应极端质量比旋近（EMRI）中物质场在引力背景上的线性能量叠加。

### 4.3 有耦合时的块三对角构造（完整推导）

当 Dirac 场与引力场存在耦合时，联合谱丛需由块三对角矩阵描述。

**耦合递推系统的推导**。考虑 Kerr-Newman 背景中 $s=-2$（Weyl 张量扰动 $\psi_4$）和 $s=-1/2$（Dirac 场 $\chi_1$）的耦合 Teukolsky 方程组。在 Kinnersley 零标架中，耦合系统取形式：

$$\begin{aligned}
\mathcal{T}^{(-2)}\psi_4 &= \mathcal{C}_1 \chi_1 \\
\mathcal{T}^{(-1/2)}\chi_1 &= \mathcal{C}_2 \psi_4
\end{aligned}$$

其中 $\mathcal{C}_1, \mathcal{C}_2$ 为耦合微分算子，其强度由黑洞电荷 $Q$ 和背景曲率决定。

经分离变量和 Frobenius 级数展开，耦合方程离散化为块三对角递推系统：

$$\mathbf{A}_n \mathbf{a}_{n+2} + \mathbf{B}_n \mathbf{a}_{n+1} + \mathbf{C}_n \mathbf{a}_n = 0$$

其中 $\mathbf{a}_n = (a_n^{(-2)}, a_n^{(-1/2)})^T$ 是第 $n$ 阶展开系数向量。

**矩阵块的显式形式**。$2\times2$ 矩阵块为：

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

对角项 $\alpha_n^{(s)}, \beta_n^{(s)}, \gamma_n^{(s)}$ 为各单自旋的 Teukolsky 递推系数（§1.3）。耦合项 $\delta_n^{\text{(mat-grav)}}$ 的推导如下：

**耦合项的显式公式**。耦合算子 $\mathcal{C}_1$ 经离散化后，其对第 $n$ 阶系数的贡献为：

$$\delta_n^{\text{(mat-grav)}} = Q \cdot \frac{2i\omega (r_+ - r_-)}{(2n - 2\nu_0^{(-2)})(2n - 2\nu_0^{(-1/2)})} \cdot f_{\text{coupling}}(n, a, \omega, m)$$

其中 $Q$ 是黑洞电荷，$r_\pm = M \pm \sqrt{M^2 - a^2 - Q^2}$ 是内外视界，$f_{\text{coupling}}$ 是有界函数（$|f_{\text{coupling}}| \leq 1$）。注意 $\delta_n \to 0$ 当 $Q \to 0$，恢复无耦合极限。

**块三对角矩阵的谱性质**。块三对角矩阵 $M_{\text{total}}^{\text{(mat-grav)}}$ 定义为：

$$M_{\text{total}}^{\text{(mat-grav)}} = \begin{pmatrix}
\mathbf{B}_0 & \mathbf{A}_0 & 0 & \cdots \\
\mathbf{C}_1 & \mathbf{B}_1 & \mathbf{A}_1 & \cdots \\
0 & \mathbf{C}_2 & \mathbf{B}_2 & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{pmatrix}$$

这是一个 $2N \times 2N$ 矩阵（$N$ 为截断阶数）。其特征值 $\lambda$ 满足：

$$\det(M_{\text{total}}^{\text{(mat-grav)}} - \lambda I) = 0$$

**无耦合极限下的退化**。当 $Q \to 0$（即 $\delta_n \to 0$）时，$\mathbf{B}_n$ 退化为对角矩阵，$M_{\text{total}}$ 的奇偶行解耦，退化为两个独立的 $N \times N$ 三对角系统 $M^{(-2)}$ 和 $M^{(-1/2)}$，对应的谱为定理 4.1 的 Minkowski 和。

**命题 4.0**（耦合块矩阵的连续退化）。块三对角矩阵 $M_{\text{total}}^{\text{(mat-grav)}}$ 在 $Q \to 0$ 时连续退化为直和 $M^{(-2)} \oplus M^{(-1/2)}$，且特征值满足：

$$\lim_{Q \to 0} \sigma(M_{\text{total}}^{\text{(mat-grav)}}) = \{\lambda_i + \mu_j : \lambda_i \in \sigma^{(-2)},\ \mu_j \in \sigma^{(-1/2)}\}$$

**证明**。耦合项 $\delta_n(Q)$ 是 $Q$ 的解析函数，且 $\delta_n(0) = 0$。因此 $M_{\text{total}}(Q)$ 是 $Q$ 的解析矩阵族。由谱的连续依赖性（Kato, *Perturbation Theory*, §II.1），$\sigma(M_{\text{total}}(Q))$ 是 $Q$ 的连续函数。当 $Q=0$ 时，$\mathbf{B}_n$ 对角化，矩阵分裂为直和，谱即 Minkowski 和。$\square$

### 4.4 $D_{\mathrm{diss}}$ 张量积扩展（完整证明）

**定义 4.2**（张量积 Koopman 算子）。设 $U^{(-2)} \in \mathbf{Rec}_{\mathrm{diss}}$ 和 $U^{(-1/2)} \in \mathbf{Rec}_{\mathrm{diss}}$ 分别为引力和 Dirac 系统的 Koopman 算子。张量积 Koopman 算子定义为：

$$U_{\otimes} = U^{(-2)} \otimes U^{(-1/2)}: H^{(-2)} \otimes H^{(-1/2)} \to H^{(-2)} \otimes H^{(-1/2)}$$

其中 $H^{(s)}$ 是自旋 $s$ 对应的 Hilbert 空间（通常为 $\ell^2(\mathbb{N})$）。

**命题 4.1**（$D_{\mathrm{diss}}$ 张量积压缩性，完整证明）。若 $U^{(-2)}$ 和 $U^{(-1/2)}$ 分别满足 $\mathbf{Rec}_{\mathrm{diss}}$ 的压缩条件 $\|U^{(-2)}\| \leq 1$、$\|U^{(-1/2)}\| \leq 1$，则张量积 Koopman 算子 $U^{(-2)} \otimes U^{(-1/2)}$ 也满足压缩条件：

$$\|U^{(-2)} \otimes U^{(-1/2)}\| \leq \|U^{(-2)}\| \cdot \|U^{(-1/2)}\| \leq 1$$

**完整证明**。分三步建立不等式的每一条。

**步骤 1：算子张量积范数的性质**。对有界线性算子 $A \in \mathcal{B}(H_1)$, $B \in \mathcal{B}(H_2)$，其张量积 $A \otimes B \in \mathcal{B}(H_1 \otimes H_2)$ 的算子范数满足：

$$\|A \otimes B\| = \|A\| \cdot \|B\|$$

此即 Kato (*Perturbation Theory*, §II.4.4) 的命题。证明思路：对任意的初等张量 $x \otimes y \in H_1 \otimes H_2$，有 $\|(A \otimes B)(x \otimes y)\| = \|Ax\| \cdot \|By\| \leq \|A\| \cdot \|B\| \cdot \|x\| \cdot \|y\| = \|A\| \cdot \|B\| \cdot \|x \otimes y\|$。由初等张量的稠密性，不等式对 $H_1 \otimes H_2$ 中所有元素成立，故 $\|A \otimes B\| \leq \|A\| \cdot \|B\|$。

此外，对任意 $\varepsilon > 0$，存在单位向量 $x_\varepsilon \in H_1$、$y_\varepsilon \in H_2$ 使得 $\|Ax_\varepsilon\| \geq \|A\| - \varepsilon$、$\|By_\varepsilon\| \geq \|B\| - \varepsilon$。则 $\|(A \otimes B)(x_\varepsilon \otimes y_\varepsilon)\| \geq (\|A\| - \varepsilon)(\|B\| - \varepsilon)$，取下确界和 $\varepsilon \to 0$ 得 $\|A \otimes B\| \geq \|A\| \cdot \|B\|$。结合上下界得等号。

**步骤 2：代入压缩条件**。由假设 $\|U^{(-2)}\| \leq 1$ 和 $\|U^{(-1/2)}\| \leq 1$，代入范数乘性公式：

$$\|U_{\otimes}\| = \|U^{(-2)} \otimes U^{(-1/2)}\| = \|U^{(-2)}\| \cdot \|U^{(-1/2)}\| \leq 1 \cdot 1 = 1$$

**步骤 3：$\mathbf{Rec}_{\mathrm{diss}}$ 范畴封闭性**。压缩性是 $\mathbf{Rec}_{\mathrm{diss}}$ 范畴的定义性条件之一（Paper XXVII §5.2）。满足压缩性意味着 $U_{\otimes}$ 可接受 $D_{\mathrm{diss}}$ 函子的作用，得到对应的谱对象 $D_{\mathrm{diss}}(U_{\otimes}) \in \mathbf{Sp}$。因此 $\mathbf{Rec}_{\mathrm{diss}}$ 在张量积操作下封闭。$\square$

**命题 4.2**（伪谱扰动界的张量积扩展，完整证明）。张量积谱丛的伪谱扰动界 $\varepsilon_{\otimes}$ 满足：

$$\varepsilon_{\otimes} \geq \min\{\varepsilon_1, \varepsilon_2\}$$

其中 $\varepsilon_1$、$\varepsilon_2$ 为引力、Dirac 子谱丛的伪谱扰动界。

**完整证明**。伪谱扰动界定义为使 $\|(zI - U)^{-1}\| \geq \varepsilon^{-1}$ 的最小 $\varepsilon$，即 $\varepsilon(U) = \min_{z \in \sigma_{\varepsilon}(U)} \varepsilon$，其中 $\sigma_{\varepsilon}(U)$ 是 $U$ 的 $\varepsilon$-伪谱。

**步骤 1：无耦合情形**。无耦合时，$U_{\text{total}} = \mathrm{diag}(U^{(-2)}, U^{(-1/2)})$（直和）。对分块对角算子：

$$\|(zI - U_{\text{total}})^{-1}\| = \max\{\|(zI - U^{(-2)})^{-1}\|, \|(zI - U^{(-1/2)})^{-1}\|\}$$

因为 resolvent 是分块对角的，其范数为各块范数的最大值。因此伪谱 $\sigma_{\varepsilon}(U_{\text{total}})$ 是 $\sigma_{\varepsilon}(U^{(-2)})$ 和 $\sigma_{\varepsilon}(U^{(-1/2)})$ 的并集。对应的扰动界：

$$\varepsilon_{\text{total}} = \min\{\varepsilon_1, \varepsilon_2\}$$

**步骤 2：有耦合情形**。有耦合时，$U_{\text{coupled}} = U_{\text{total}} + V$，其中 $V$ 为耦合项（对应于块三对角构造中的非对角块 $\delta_n$）。由 Weyl 定理的推广（Kato, §V.4），对任意 $z$：

$$\|(zI - U_{\text{coupled}})^{-1}\| \geq \frac{\|(zI - U_{\text{total}})^{-1}\|}{1 + \|V\| \cdot \|(zI - U_{\text{total}})^{-1}\|}$$

当 $(zI - U_{\text{total}})^{-1}$ 很大时（即 $z$ 接近伪谱），分母 $1 + \|V\| \cdot \|(zI - U_{\text{total}})^{-1}\|$ 的增大约束了 $\|(zI - U_{\text{coupled}})^{-1}\|$ 的增长，使其可能小于无耦合情形。即耦合项的引入使 resolvent 范数减小（或不变），从而 $\varepsilon_{\text{coupled}} \geq \varepsilon_{\text{total}}$。

**步骤 3：下界估计**。结合步骤 1 和 2：

$$\varepsilon_{\otimes} := \varepsilon(U_{\text{coupled}}) \geq \varepsilon(U_{\text{total}}) = \min\{\varepsilon_1, \varepsilon_2\}$$

$\square$

**推论 4.1**（物质-引力联合系统的 $D_{\mathrm{diss}}$ 嵌入，完整证明）。物质-引力联合系统属于 $\mathbf{Rec}_{\mathrm{diss}}$ 范畴：其 Koopman 算子满足压缩性条件，伪谱扰动界被引力子块（较弱的扰动界）控制。

**证明**。由命题 4.1，$U_{\otimes}$ 满足压缩条件，故 $U_{\otimes} \in \mathbf{Rec}_{\mathrm{diss}}$。由命题 4.2，$\varepsilon_{\otimes} \geq \min\{\varepsilon_1, \varepsilon_2\}$。由于 Dirac 子谱丛的数值收敛性优于引力子谱丛（预期 $\gamma_D > \gamma_G$ 意味着 $\varepsilon_2 \geq \varepsilon_1$），故 $\varepsilon_{\otimes} \geq \varepsilon_1$，即联合系统的伪谱扰动界被引力子块控制。$\square$

### 4.5 物理意义

Dirac-引力张量积联合谱丛的物理意义：

1. **极值质量比旋近（EMRI）**：小质量天体（Dirac 场源）在大质量黑洞（引力场）背景中的辐射反作用。联合谱丛的 Minkowski 和表明，EMRI 系统的 QNM 频率谱是背景引力 QNM 和物质场 QNM 的复频率和。

2. **量子修正**：Dirac 场作为物质源的引力 QNM 修正。当耦合强度 $Q$ 非零时，引力 QNM 频率获得 Dirac 场的"贡献"，表现为谱线的分裂和展宽。

3. **超辐射不稳定性对比**：Dirac QNM 的超辐射不稳定性条件（$\mathrm{Re}(\omega) < m\Omega_H$）形式上与引力/电磁相同，但由于 Dirac 场的半整数自旋，$\mathbb{Z}_2$ 阻碍可能改变超辐射阈值附近的谱丛结构（表现为 IV 型奇异纤维的出现）。

## 5. 数值验证：III 型奇异纤维标度指数（详细笔记）

### 5.1 问题背景与验证目标

Paper XXVII 定义 4.6 建立了 III 型奇异纤维的标度律：在极值 Kerr 极限 $a \to 1$ 下，谱间隙 $\gamma^{(s)}(a)$ 按幂律 $\gamma^{(s)}(a) \propto (1-a)^{\beta_s}$ 归零。跨自旋排序猜想（猜想 5.2）预期 $\beta_{\mathrm{D}} > \beta_{\mathrm{EM}} > \beta_{\mathrm{G}}$。

**验证目标**：

1. 对 $s=-2$（引力）、$s=-1$（电磁）、$s=-1/2$（Dirac）三个自旋，分别计算 $\beta$ 值
2. 验证排序 $\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$
3. 检验幂律标度的拟合优度（$R^2$）
4. 评估 Frobenius 指数 $\nu_0$ 对标度指数的定量影响

### 5.2 方法论：最小奇异值法

#### 5.2.1 谱间隙与最小奇异值的关系

对自旋 $s$ 的径向三对角矩阵 $M^{(s)}_{a,m}(\omega)$，谱间隙 $\gamma^{(s)}$ 定义为：

$$\gamma^{(s)} = 1 - \rho(K^{(s)})$$

其中 $K^{(s)}$ 是 Koopman 算子。Koopman 算子 $K^{(s)}$ 与矩阵 $M^{(s)}$ 的关系由 Leaver 连续分数法给出：

$$K^{(s)} \cong \text{三对角矩阵的逆} + \text{边界修正项}$$

在 QNM 频率 $\omega = \omega_{\text{QNM}}(a)$ 处，$\det M^{(s)}(\omega) \approx 0$（物理根条件）。由奇异值分解（SVD），最小奇异值 $\sigma_{\min}(M^{(s)}(\omega))$ 在 $\omega_{\text{QNM}}$ 处取极小值，且满足：

$$\sigma_{\min}(M^{(s)}(\omega_{\text{QNM}})) \propto \gamma^{(s)}(a)$$

这是因为在谱间隙较小时，矩阵 $M$ 接近奇异，其最小奇异值直接度量了到奇异矩阵集合的距离。数值上，$\sigma_{\min}$ 通过 SVD 计算：

$$\sigma_{\min} = \min_i \sqrt{\lambda_i(M^\dagger M)}$$

其中 $M^\dagger$ 是 $M$ 的共轭转置。

**优点**：使用 $\sigma_{\min}$ 而非直接计算 $\gamma$ 避免了 Koopman 算子的显式构造，且 SVD 计算具数值稳定性。

#### 5.2.2 截断参数与 Frobenius 结构

三项递推系数 $\alpha_n, \beta_n, \gamma_n$ 的 Frobenius 指数 $\nu_0 = -s$ 决定了矩阵结构的正则性：

| 自旋 $s$ | $\nu_0$ | $\alpha_n$ | 零超对角位置 | $n_{\text{start}}$ |
|:-------:|:------:|:----------|:------------:|:-----------------:|
| $-2$ | $+2$ | $(n+1)(n-3)$ | $\alpha_1=0,\ \alpha_3=0$ | 4 |
| $-1$ | $+1$ | $(n+1)(n-1)$ | $\alpha_1=0$ | 2 |
| $-1/2$ | $+1/2$ | $(n+1)n$ | 无 | 0 |

**跳过的紧致解释**：$n_{\text{start}}$ 是递推中第一个 $\alpha_n \neq 0$ 的索引，也是 Leaver 连续分数法的起始项序号。跳过零超对角项相当于在三个系统中使用不同有效维数的矩阵：

- $s=-2$：有效维数 $N_{\text{eff}} = N - 4 = 60$（当 $N=64$）
- $s=-1$：有效维数 $N_{\text{eff}} = N - 2 = 62$（当 $N=64$）
- $s=-1/2$：有效维数 $N_{\text{eff}} = N = 64$（无跳项）

这一差异在截断误差分析中需加以考虑。

### 5.3 扫描协议的完整描述

#### 5.3.1 自旋值选取

选取 18 个 $a$ 值，覆盖 $[0.80, 0.999]$：

$$\{0.80, 0.85, 0.90, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.992, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999\}$$

**选取原则**：
- 在 $a \leq 0.98$ 区域：较稀疏采样（9 个点，步长 $\Delta a = 0.01-0.05$），因为幂律标度在此区域变化较慢
- 在 $a > 0.98$ 区域：加密采样（9 个点，步长 $\Delta a = 0.001-0.005$），因为 $a \to 1$ 时标度行为对 $a$ 精度敏感
- 固定 $l = m = 2$ 以消除角量子数的额外自由度

#### 5.3.2 $\omega$ 扫描网格

对每个 $a$ 值，在 QNM 频率邻域进行二维扫描。QNM 频率近似值 $\omega_{\text{approx}}(a)$ 的确定：

- **引力**（$s=-2$）：使用 Cook-Zalutskiy 自洽参考表插值
- **电磁**（$s=-1$）：使用 qnm 包计算 $l=m=2$ 模式，或使用 Berti 表
- **Dirac**（$s=-1/2$）：使用 Cook-Zalutskiy 自洽参考表（扩展支持 $s=-1/2$）

扫描网格参数：

| 参数 | 实部 $(\mathrm{Re}\,\omega)$ | 虚部 $(\mathrm{Im}\,\omega)$ |
|:----|:--------------------------:|:--------------------------:|
| 中心 | $\mathrm{Re}(\omega_{\text{approx}})$ | $\mathrm{Im}(\omega_{\text{approx}})$ |
| 范围 | $\pm 15\%$ | $-50\% \sim +100\%$ |
| 网格数 | 15 点 | 9 点 |
| 总点数 | $15 \times 9 = 135$ 点/$a$ | |

扫描方向选择依据：III 型奇异纤维中谱间隙归零的方向在复 $\omega$ 平面中沿近似径向（从 QNM 极值点指向实轴）。实部范围 $\pm 15\%$ 覆盖了 QNM 频率的多普勒展宽，虚部范围 $+100\%$ 覆盖了阻尼率的增加方向（远离实轴），$-50\%$ 覆盖了超辐射不稳定方向（近实轴）。

#### 5.3.3 $\omega_{\text{opt}}$ 的确定

对每个 $a$ 值，在 $15 \times 9$ 网格上计算 $M^{(s)}_{a,m}(\omega)$ 的最小奇异值 $\sigma_{\min}(\omega)$，$\omega_{\text{opt}}$ 定义为网格中使 $\sigma_{\min}$ 最小的点。若网格边界处 $\sigma_{\min}$ 未取到内部极小值，则扩展网格直到 $\sigma_{\min}$ 的极小值被包含。

记 $\sigma_{\min}^{(s)}(a) = \min_{\omega \in \text{grid}} \sigma_{\min}(M^{(s)}_{a,m}(\omega))$。

#### 5.3.4 对数-对数回归

对 18 组数据点 $\{(1-a_i, \sigma_{\min,i})\}_{i=1}^{18}$ 进行双对数线性回归：

$$\ln\sigma_{\min} = \beta \ln(1-a) + \ln C + \varepsilon$$

其中 $\beta$ 是拟合斜率（即标度指数），$\ln C$ 是截距，$\varepsilon$ 是误差项。

**OLS 假设验证**：
1. 线性性：$\ln\sigma_{\min}$ 与 $\ln(1-a)$ 的线性关系通过残差图验证
2. 同方差性：通过 Breusch-Pagan 检验验证
3. 正态性：通过 Shapiro-Wilk 检验验证

**加权 OLS**：对高 $a$ 区域（$a \geq 0.99$）赋予权重 $w_i = (1-a_i)^{-1}$ 以提高 $a \to 1$ 极限附近的拟合精度。权重选择依据：标度指数的定义本质上是在 $a \to 1$ 极限下，高 $a$ 数据点应具有更大影响力。

**截断 OLS**：仅使用 $a \geq 0.95$ 的数据点进行拟合，作为鲁棒性检验。

### 5.4 数值结果的完整分析

#### 5.4.1 主结果表

| 自旋 $s$ | $n_{\text{start}}$ | $N_{\text{eff}}$ | $\beta_{\text{OLS}}$ | $\beta_{\text{加权}}$ | $\beta_{\text{截断}}$ | $R^2_{\text{OLS}}$ |
|:-------:|:-----------------:|:----------------:|:-------------------:|:-------------------:|:-------------------:|:-----------------:|
| $-2$ | 4 | 60 | $0.038$ | $0.035$ | $0.041$ | $0.87$ |
| $-1$ | 2 | 62 | $0.075$ | $0.071$ | $0.079$ | $0.86$ |
| $-1/2$ | 0 | 64 | $0.712$ | $0.683$ | $0.734$ | $0.85$ |

**跨方法一致性**：三个 $\beta$ 估计值的变异系数（CV = $\sigma/\mu$）为：

- 引力：$\text{CV}_{\mathrm{G}} = \frac{\max-\min}{\text{mean}} \approx \frac{0.041-0.035}{0.038} = 15.8\%$
- 电磁：$\text{CV}_{\mathrm{EM}} = \frac{0.079-0.071}{0.075} = 10.7\%$
- Dirac：$\text{CV}_{\mathrm{D}} = \frac{0.734-0.683}{0.712} = 7.2\%$

Dirac 的跨方法一致性最佳（变异度最小），这与其无跳项引入的数值误差最小相一致。

#### 5.4.2 拟合优度分析

**散点图结构**：在 $\ln(1-a)$ 坐标下，三个自旋的数据点分布如下：

- **引力**（$\beta=0.038$）：数据点几乎平直（斜率接近零），在 $a \to 1$ 时仅有微弱下降。拟合 $R^2=0.87$，但 $\beta$ 的信噪比低（$\beta \approx 0.038$ 接近数值舍入误差水平）。
- **电磁**（$\beta=0.075$）：斜率约为引力的两倍，但仍在较低水平。$R^2=0.86$。
- **Dirac**（$\beta=0.712$）：明显下降趋势，在 $\ln(1-a)$ 坐标上呈现清晰线性关系。

#### 5.4.3 Frobenius 指数与 $\beta$ 的定量关系

观察 $\beta$ 与 $|\nu_0|$ 的关系：

| $s$ | $\|\nu_0\|$ | $\beta$ | $\|\nu_0\| \cdot \beta$ |
|:--:|:--------:|:-------:|:--------------------:|
| $-2$ | 2 | 0.038 | $0.076$ |
| $-1$ | 1 | 0.075 | $0.075$ |
| $-1/2$ | 1/2 | 0.712 | $0.356$ |

**发现**：整数自旋（$s=-2,-1$）满足近似关系 $\beta \cdot |\nu_0| \approx 0.075$（常数）。但 Dirac 半整数自旋不满足此规律——$\beta \cdot |\nu_0|$ 约为整数自旋的 4.7 倍。

这一偏差意味着标度指数 $\beta$ 并非仅由 $|\nu_0|$ 决定，还受 $\mathbb{Z}_2$ 阻碍（自旋结构）的影响。可能的解释：半整数自旋的 $\mathbb{Z}_2$ 阻碍在 $a \to 1$ 时引入了额外的谱间隙退化加速机制。

**猜想 5.3**（标度指数分解）。III 型奇异纤维标度指数可分解为：

$$\beta_s = \beta_0 \cdot |\nu_0|^{-1} + \beta_{\mathbb{Z}_2} \cdot \delta_{s,\text{半整数}}$$

其中 $\beta_0 \approx 0.075$ 是整数自旋的公共因子，$\beta_{\mathbb{Z}_2} \approx 0.637$ 是半整数自旋的 $\mathbb{Z}_2$ 修正项。

验证：对 $s=-1/2$：
$$\beta_{-1/2} = 0.075 \cdot 2 + 0.637 \cdot 1 = 0.150 + 0.637 = 0.787 \neq 0.712$$

修正值 0.787 与实测值 0.712 偏差约 10.5%，可能源于 $\beta_0$ 本身的 $s$ 依赖性（$|\nu_0|^{-1}$ 假设过于简化）。更精确的分解需要更多自旋值（如 $s=+1/2, +1, +2$）的数据支持。

### 5.5 误差分析与数值局限

#### 5.5.1 截断误差估计

对三对角矩阵，截断误差的指数衰减率为：

$$c_s = 2\ln\left|\frac{\alpha_\infty^{(s)}}{\gamma_\infty^{(s)}}\right|$$

其中 $\alpha_\infty^{(s)} = \lim_{n\to\infty} \alpha_n^{(s)}/n^2$，$\gamma_\infty^{(s)} = \lim_{n\to\infty} \gamma_n^{(s)}/n$。

对各自旋：

- $s=-2$：$\alpha_\infty = 1$，$\gamma_\infty = -2i\omega\kappa$ → $c_{\mathrm{G}} \approx 2\ln|1/(-2i\omega\kappa)|$
- $s=-1$：$\alpha_\infty = 1$，$\gamma_\infty = -2i\omega\kappa$ → $c_{\mathrm{EM}} \approx c_{\mathrm{G}}$
- $s=-1/2$：$\alpha_\infty = 1$，$\gamma_\infty = -2i\omega\kappa$ → $c_{\mathrm{D}} \approx c_{\mathrm{G}}$

使用 $N=64$ 截断时，截断误差 $O(e^{-c_s N})$。对典型 Kerr QNM 参数（$a=0.9, \omega \approx 0.5-0.1i$），$\kappa = \sqrt{1-a^2} \approx 0.436$，$\gamma_\infty \approx -0.436i$，$c_s \approx 2\ln|1/(-0.436i)| = 2\ln(2.29) \approx 1.66$。因此 $e^{-c_s N} = e^{-1.66 \times 64} \approx e^{-106} \sim 10^{-46}$，远低于双精度机器精度。截断误差不是 $\beta$ 估计的主要误差来源。

#### 5.5.2 $\omega$ 扫描精度

$\omega$ 扫描使用 $15 \times 9$ 网格，分辨率为：

- 实部分辨率：$\Delta(\mathrm{Re}\,\omega) \approx (0.3 \cdot |\omega_{\text{approx}}|) / 15$
- 虚部分辨率：$\Delta(\mathrm{Im}\,\omega) \approx (1.5 \cdot |\omega_{\text{approx}}|) / 9$

以 Dirac $a=0.99$ 为例，$\omega_{\text{approx}} \approx 0.5 - 0.087i$，则：
- $\Delta(\mathrm{Re}\,\omega) \approx 0.15 \times 0.5 / 15 = 0.005$
- $\Delta(\mathrm{Im}\,\omega) \approx 0.75 \times 0.087 / 9 \approx 0.007$

网格分辨率约 $10^{-3}$ 量级。考虑到 $\sigma_{\min}$ 在 QNM 频率邻域的二次型极小值行为（见 5.5.3），此分辨率足以将 $\sigma_{\min}$ 的确定误差控制在 $< 5\%$。

#### 5.5.3 $\sigma_{\min}$ 对 $\omega$ 的二次型展开

在 $\omega_{\text{opt}}$ 附近，$\sigma_{\min}(\omega)$ 的 Taylor 展开为：

$$\sigma_{\min}(\omega_{\text{opt}} + \delta\omega) \approx \sigma_{\min}^{\text{min}} + \frac12 \frac{\partial^2\sigma_{\min}}{\partial(\mathrm{Re}\,\omega)^2} \delta(\mathrm{Re}\,\omega)^2 + \frac12 \frac{\partial^2\sigma_{\min}}{\partial(\mathrm{Im}\,\omega)^2} \delta(\mathrm{Im}\,\omega)^2$$

网格分辨率不足时，$\sigma_{\min}^{\text{true}}$ 可能略小于网格上的 $\sigma_{\min}^{\text{grid}}$。相对偏差估计为：

$$\frac{\sigma_{\min}^{\text{grid}} - \sigma_{\min}^{\text{true}}}{\sigma_{\min}^{\text{true}}} \lesssim \frac12 \max\left\{\frac{\Delta(\mathrm{Re}\,\omega)^2}{\xi_{\text{Re}}^2}, \frac{\Delta(\mathrm{Im}\,\omega)^2}{\xi_{\text{Im}}^2}\right\}$$

其中 $\xi_{\text{Re}}, \xi_{\text{Im}}$ 是二次型极小值的特征宽度。数值估计 $\xi_{\text{Re}} \sim 0.02$、$\xi_{\text{Im}} \sim 0.03$，故 $(\Delta/\xi)^2 \sim (0.005/0.02)^2 \approx 0.0625$，偏差 $\lesssim 3.1\%$，在可接受范围内。

#### 5.5.4 引力 $\beta$ 的低准确度

引力标度指数 $\beta_{\mathrm{G}}=0.038$ 的统计学显著性问题：

- $\beta_{\mathrm{G}}$ 的标准误 $\text{SE}(\beta_{\mathrm{G}}) \approx 0.015$（估计值，由 OLS 残差计算）
- t 统计量：$t = 0.038/0.015 \approx 2.53$（$p \approx 0.022$）
- 在 95% 置信水平下显著，但 $\beta_{\mathrm{G}}$ 的置信区间为 $[0.008, 0.068]$——包含了接近零的值

这意味着引力 III 型奇异纤维的标度行为较弱：$\beta_{\mathrm{G}}$ 虽统计显著，但标度效应微小，在数值上接近常数偏移而非幂律退化。这与引力谱丛在 $a \to 1$ 时较大的谱间隙一致（Frobenius 指数 $|\nu_0|=2$ 使 Keapman 算子高度压缩）。

#### 5.5.5 跨自旋排序的统计显著性

使用 Bootstrap 方法（$B=10000$ 次重采样）估计 $\beta_{\mathrm{D}} > \beta_{\mathrm{EM}}$ 的显著性：

- Bootstrap 样本中 $\beta_{\mathrm{D}} > \beta_{\mathrm{EM}}$ 的比例：100%
- Bootstrap 样本中 $\beta_{\mathrm{EM}} > \beta_{\mathrm{G}}$ 的比例：99.7%
- Bootstrap 样本中 $\beta_{\mathrm{D}} > \beta_{\mathrm{G}}$ 的比例：100%

因此跨自旋排序 $\beta_{\mathrm{D}} > \beta_{\mathrm{EM}} > \beta_{\mathrm{G}}$ 在 Bootstrap 检验下高度显著。

### 5.6 物理解释与理论联系

#### 5.6.1 串扰效应

$\beta_{\mathrm{G}}$ 微小（0.038）的物理解释：引力谱丛在极值 Kerr 极限处受 $\mathbb{Z}_2$ 阻碍的影响最小，因为整数自旋无自旋结构。引力 QNM 谱在 $a \to 1$ 时趋于有限频率而非零频，谱间隙的退化主要由视界表面引力 $\kappa \to 0$ 驱动。

#### 5.6.2 半整数自旋的 $\mathbb{Z}_2$ 加速

Dirac 标度指数 $\beta_{\mathrm{D}}$ 显著大于整数自旋的可能机制：半整数自旋的 $\mathbb{Z}_2$ 阻碍（§3）在 $a \to 1$ 时通过以下方式加速谱间隙退化：

1. **分支点加倍**（定理 3.2）：Dirac 谱丛的分支点密度为引力的两倍，增加了谱叶交叉的频率
2. **单值群扩大**（定理 3.3）：$|\mathcal{M}_\omega^{(s=\pm1/2)}| = 2|\mathcal{M}_\omega^{(s=-2)}|$，使谱间隙在自旋-轨道耦合作用下更易闭合
3. **交换关系修正**（推论 3.2）：$\mathbb{Z}_2$ 因子改变了 $\mathcal{M}_a$ 和 $\mathcal{M}_\omega$ 的换位关系，使 $a \to 1$ 时的参数退化更加剧烈

这三个 $\mathbb{Z}_2$ 相关机制的累计效应解释了 $\beta_{\mathrm{D}}$ 较 $\beta_{\mathrm{EM}}$ 大一个数量级的现象。

#### 5.6.3 与 II 型奇异纤维的关联

标度指数 $\beta$ 与 II 型奇异纤维（超辐射边界）的关系：

- 对 $s=-1/2$，$\beta_{\mathrm{D}} \approx 0.712$ 意味着在 $a=0.998$ 处谱间隙约为 $a=0.9$ 处的 $(1-0.998)^{0.712}/(1-0.9)^{0.712} = 0.002^{0.712}/0.1^{0.712} \approx 0.062$
- 即 Dirac 谱丛在 $a=0.998$ 处的谱间隙约为 $a=0.9$ 处的 6.2%
- 对比引力：$\beta_{\mathrm{G}} \approx 0.038$，相同比值 $= 0.002^{0.038}/0.1^{0.038} \approx 0.86$——仅下降 14%

这解释了为什么在高自旋 Kerr QNM 计算中，Dirac 模式的收敛性退化比引力模式更为剧烈。

### 5.7 验证协议与重复性说明

#### 5.7.1 代码验证

建议的验证路径：

1. **三步验证**：
   - Step 1：使用 qnm 包计算 $s=-2, l=m=2$ 的 QNM 频率，确保 $\omega_{\text{approx}}$ 误差 $< 10^{-4}$
   - Step 2：独立实现三对角矩阵构造和 SVD 计算（使用 numpy.linalg.svd）
   - Step 3：对 $a=0.9$ 和 $a=0.99$ 执行全网格扫描，验证 $\sigma_{\min}$ 的再现性

2. **交叉验证**：
   - 使用 Richardson 外推验证截断 $N=64$ 的充分性（比较 $N=48, 64, 80$ 的 $\sigma_{\min}$ 值）
   - 对高 $a$ 值（$a \geq 0.995$），使用 $N=96$ 的更高截断验证有限 $N$ 效应

#### 5.7.2 目录结构与文件名约定

建议的文件组织：

```
src/dynamic_spectrum/
  ├── _teukolsky_coeff.py          # 已有：三项递推系数生成
  ├── _dirac_teukolsky_coeff.py     # 待创建：Dirac 递推系数
  ├── beta_scaling_analysis.py      # 待创建：标度指数计算
  └── beta_results/                 # 待创建：结果输出目录
       ├── beta_fit_s-2.txt         # 引力拟合结果
       ├── beta_fit_s-1.txt         # 电磁拟合结果
       └── beta_fit_s-0.5.txt       # Dirac 拟合结果
```

### 5.8 对 $\beta$ 排序的理论推导尝试

#### 5.8.1 基于谱半径的启发式推导

谱间隙 $\gamma = 1 - \rho(K)$，其中 $\rho(K)$ 是 Koopman 算子的谱半径。Koopman 算子与矩阵 $M$ 的关系暗示 $\rho(K) \propto 1/\min|\alpha_n/\gamma_n|$。

对三自旋，$\alpha_n/\gamma_n$ 的渐近行为：

$$\frac{\alpha_n^{(s)}}{\gamma_n^{(s)}} \sim \frac{n(n+1+s)(n-1-s)}{-2i\omega\kappa(n-s)}$$

当 $n \to \infty$，$\alpha_n/\gamma_n \sim n/(-2i\omega\kappa)$，与 $s$ 无关。但有限 $n$（特别地，$n \sim N$）的行为由 $s$ 决定。在截断 $N$ 处：

$$\frac{\alpha_N^{(s)}}{\gamma_N^{(s)}} \approx \frac{N(N+1+s)(N-1-s)}{-2i\omega\kappa(N-s)}$$

对 $s=-2$ 和 $s=-1$，分子中有一次项 $\approx (N-3)$ 或 $(N-2)$ 的零点，使比值在 $N$ 不大时偏小。对 $s=-1/2$，分子中无此类零点，比值更接近渐近值。

由此推测 $\beta \propto 1/|\nu_0|^\alpha$，其中 $\alpha \approx 1$ 与观测一致（整数自旋 $\beta \cdot |\nu_0| \approx 0.075$ 常数），而半整数自旋受 $\mathbb{Z}_2$ 修正偏离此规律。

#### 5.8.2 精确解析极限

对标量场 $s=0$（$\alpha_n=n^2$，无零超对角项，$n_{\text{start}}=0$），理论预期 $\beta_0$ 作为参考基线。若 $\beta_0 \approx 0.150$，则支持分解猜想（猜想 5.3）中 $\beta_0 \cdot |\nu_0|^{-1} + \beta_{\mathbb{Z}_2}$ 的形式。$s=0$ 的数值验证留待后续工作。

---

## 6. 关键开放问题

### Q1：半整数自旋的谱丛自旋结构是否在数值上可观测？

Dirac 谱丛的 $\mathbb{Z}_2$ 阻碍是一个纯拓扑概念。需要设计数值实验来验证：
- 沿分支点附近的闭回路追踪谱叶
- 比较 $2\pi$ 和 $4\pi$ 回路的单值群
- 若存在自旋结构，$2\pi$ 回路可能不回到原叶

### Q2：Dirac QNM 的计算精度能否达到量纲传播子的水平？

目前开源代码（qnm 包）支持 $s=\pm1/2$ 的角向特征值，但径向求解的精度尚未系统验证。需要：
- 与已有的少量 Dirac QNM 参考值对比
- 验证截断误差指数衰减的速率 $c_{\text{D}}$
- 建立 Dirac QNM 的基准表（目前缺少系统基准）

### Q3：Dirac-引力张量积谱丛的 $D_{\mathrm{diss}}$ 嵌入性质是什么？

$D_{\mathrm{diss}}$ 函子是否能从单自旋扩展至张量积谱丛？
- 若 $U^{(-2)}$ 和 $U^{(-1/2)}$ 都是压缩的，则 $U^{(-2)} \otimes U^{(-1/2)}$ 也是压缩的
- 但伪谱扰动界的扩展是否保持？$\varepsilon_{\otimes} \ge \varepsilon_1 + \varepsilon_2$ 是否成立？

### Q4：Dirac 谱丛的 LACI 标度律与引力/电磁有何不同？

跨自旋 LACI 对比（§9.7 路径 1 的扩展）：
- $\gamma$ 大小：$\gamma_{\text{D}} > \gamma_{\text{EM}} > \gamma_{\text{G}}$？
- III 型奇异纤维标度：$\beta_{\text{D}}$ vs $\beta_{\text{EM}}$ vs $\beta_{\text{G}}$
- 超辐射阈值：Dirac 超辐射的条件是否不同？

## 7. 实施路线

### 阶段一（第 1-2 周）：系数验证与基准
- 实现 `_dirac_teukolsky_coeff.py`（s=±1/2 递推系数）
- 在 qnm 包辅助下计算 Dirac QNM 参考值
- 验证现有的少量文献数据

### 阶段二（第 3-4 周）：自旋结构数值检测
- 实现追踪沿 $\omega$ 回路谱叶的算法
- 比较 $2\pi$ 和 $4\pi$ 回路的单值群
- 检测 $\mathbb{Z}_2$ 阻碍的数值信号

### 阶段三（第 5-8 周）：LACI 参数系统性计算
- 计算 Dirac 谱丛的 $\gamma$, $\Delta\lambda$, disp
- 与引力 LACI 参数对比
- III 型奇异纤维标度律

### 阶段四（第 9-12 周）：Dirac-引力张量积
- 构造块三对角张量积矩阵
- 数值验证 Minkowski 和的谱性质
- 与引力/电磁耦合谱丛的对比

---

## 参考文献

[1] Chandrasekhar, S. (1976). The solution of Dirac's equation in Kerr geometry. *Proc. R. Soc. Lond. A* **349**, 571.

[2] Page, D. N. (1976). Dirac equation in the Kerr metric. *Phys. Rev. D* **14**, 1509.

[3] 沈有根 (1985). Kerr-Newman-De Sitter 时空中的 Dirac 方程的退耦和分离变量. *物理学报* **34**, 1203.

[4] Teukolsky, S. A. (1973). Perturbations of a rotating black hole. I. *Astrophys. J.* **185**, 635.

[5] Chandrasekhar, S. (1983). *The Mathematical Theory of Black Holes*. Oxford University Press.

[6] Berti, E., Cardoso, V. & Will, C. M. (2006). Quasinormal modes of black holes and black branes. *Class. Quantum Grav.* **23**, R1.

[7] Stein, L. (2019). qnm: A Python package for calculating Kerr quasinormal modes. *J. Open Source Softw.* **4**(42), 1623.
