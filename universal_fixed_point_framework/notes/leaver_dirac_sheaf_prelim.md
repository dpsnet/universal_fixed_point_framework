# Dirac 谱丛预研：s=±1/2 半整数自旋的谱丛构造与自旋结构

**版本**：v0.1（2026-07-25）

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

## 3. 半整数自旋的 spin structure

### 3.1 $\mathbb{Z}_2$ 阻碍的起源

半整数自旋谱丛与整数自旋谱丛的一个根本差异是**自旋结构**（spin structure）的存在。沿 $\mathbb{C}_\omega$ 中闭回路的平行移动：

- 整数自旋（s=0, ±1, ±2）：沿 $2\pi$ 旋转的谱叶置换为恒等
- 半整数自旋（s=±1/2）：沿 $2\pi$ 旋转的谱叶置换可能为 $-1$

**定义 3.1**（自旋阻碍）。对 $s = \pm\frac12$ 谱丛 $\mathfrak{S}^{(s)}$，存在 2-覆盖 $\tilde{\mathfrak{S}}^{(s)} \to \mathfrak{S}^{(s)}$，使得沿 $\mathbb{C}_\omega$ 中闭回路的单值群 $\mathcal{M}_\omega^{(s)}$ 嵌入置换群 $S_N$ 时，存在 $\mathbb{Z}_2$ 阻碍：

$$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) \neq 0$$

### 3.2 自旋结构的谱丛意义

自旋结构的出现意味着 Dirac 谱丛 $\mathfrak{S}^{(s=\pm1/2)}$ 是引力谱丛 $\mathfrak{S}^{(s=-2)}$ 的 $\mathbb{Z}_2$-覆盖。这产生两个重要后果：

1. **分支点加倍**：Dirac 谱丛中每个引力分支点对应两个 Dirac 分支点（自旋向上/向下的分裂）
2. **单值群扩大**：$|\mathcal{M}_\omega^{(s=\pm1/2)}| = 2|\mathcal{M}_\omega^{(s=-2)}|$（在相同截断下）
3. **交换关系修正**：$[\mathcal{M}_a, \mathcal{M}_\omega]$ 和 $[\mathcal{M}_m, \mathcal{M}_\omega]$ 的换位子可能包含 $\mathbb{Z}_2$ 因子

### 3.3 数值可检测性

自旋结构是否可以在数值上检测？

**命题 3.1**（自旋结构的数值诊断）。Dirac 谱丛的自旋结构可通过以下方式数值验证：

1. 沿 $\mathbb{C}_\omega$ 中分支点附近的闭回路追踪谱叶
2. 检测平行移动后谱叶是否回到原叶还是变为负号
3. 比较 $2\pi$ 回路与 $4\pi$ 回路的单值群结果

## 4. Dirac-引力张量积联合谱丛

### 4.1 张量积构造

**定义 4.1**（Dirac-引力张量积谱丛）。对自旋集合 $S = \{-2, -\frac12\}$，定义张量积谱丛为：

$$\mathfrak{S}^{(-2) \otimes (-1/2)} = \mathfrak{S}^{(-2)} \otimes \mathfrak{S}^{(-1/2)}$$

其中 $\otimes$ 是**纤维张量积**：在公共参数空间 $(a,m,\omega)$ 上，纤维为 $F^{(-2)} \otimes F^{(-1/2)}$。

### 4.2 联合谱丛的谱

张量积谱丛 $\mathfrak{S}^{(-2) \otimes (-1/2)}$ 的谱（即联合特征值）由以下方程给出：

$$\det(M_{\text{total}}^{\text{(mat-grav)}}(\omega) - \lambda I) = 0$$

其中 $M_{\text{total}}^{\text{(mat-grav)}}$ 是 $s=-2$ 和 $s=-\frac12$ 的块三对角矩阵（耦合项由物质-引力耦合常数决定）。

在无耦合（仅直积）情形下：

$$\sigma(\mathfrak{S}^{(-2) \otimes (-1/2)}) = \{\lambda_i + \mu_j : \lambda_i \in \sigma^{(-2)}, \mu_j \in \sigma^{(-1/2)}\}$$

即引力特征值与 Dirac 特征值的**Minkowski 和**。

### 4.3 物理意义

Dirac-引力张量积联合谱丛的物理意义：
- **极值质量比旋近（EMRI）**：小质量天体（Dirac 场源）在大质量黑洞（引力场）背景中的辐射反作用
- **量子修正**：Dirac 场作为物质源的引力 QNM 修正
- **超辐射**：Dirac QNM 的超辐射不稳定性是否不同于光子/引力子超辐射？

## 5. 关键开放问题

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

## 6. 实施路线

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
