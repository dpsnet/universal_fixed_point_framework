# 三对角谱丛结构的推广性分析

**版本**：v0.1（2026-07-25）

**摘要**：本笔记系统分析三对角谱丛结构在不同物理系统中的出现。第一部分提出度规层面的充要条件（G1–G3），检验 7 类黑洞度规。第二部分将分析扩展到非引力系统——非牛顿流变学的复杂黏度连分数和凝聚态物理的 NRG Wilson 链/记忆函数连分数——揭示三对角谱丛结构是三类不同物理系统共享的深层数学结构。本文是对 `notes/04_lorentz_gravity/spectral_sheaf_leaver.md` §6 开放问题 4 的完整回答与跨领域扩展。

---

## 第一部分：三对角谱丛结构的度规条件

### 1. 核心定理

**定理 1**（三对角谱丛结构存在性）：一个稳态轴对称黑洞度规的 Teukolsky 方程可化为三对角谱丛结构（即谱丛 $\mathcal{S} = \{(\omega, \lambda): \det(M(\omega) - \lambda I) = 0\}$ 中 $M(\omega)$ 为三对角矩阵族），当且仅当以下三个条件同时成立。

#### 条件 G1（分离变量性）

度规为 **Petrov D 型**（又称 Type D），且存在 Killing 向量场 $\partial_t$ 和 $\partial_\phi$，使得 Teukolsky 方程可分离变量：

$$\Psi = e^{-i\omega t} e^{im\phi} S(\theta) R(r)$$

径向方程和角向方程均为常微分方程，彼此通过分离常数 $\lambda$（自旋加权椭球谐函数特征值）耦合。

**物理起源**：Petrov D 型背景保证了 Newman-Penrose 形式中 Weyl 标量 $\Psi_0$ 和 $\Psi_4$ 的扰动方程可分离。Carter 常数的存在是这一性质的代数根源。

#### 条件 G2（三项递推性）

径向方程在 $r_+$（外视界）和 $r = \infty$ 处的渐近解形式为：

$$R(r) \sim e^{i\omega r_*} r^{(2M(\omega - \bar{\omega}) - 1)} \sum_{n=0}^\infty a_n \left(\frac{r - r_+}{r}\right)^n$$

其中 $r_*$ 为 tortoise 坐标。展开系数 $a_n$ 满足**三项递推关系**：

$$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0$$

且系数 $\alpha_n, \beta_n, \gamma_n$ 是 $\omega$ 的（有理）函数。此递推在边界条件（视界处向内传播、无穷远处向外传播）下唯一确定物理模式。

**反例说明**：若径向方程的奇点结构导致展开需两套基函数（如某些带标量场耦合的系统），或奇点阶数高于正则奇点，则可能出现四项或更高阶递推。

#### 条件 G3（多项式系数性）

递推系数 $\alpha_n, \beta_n, \gamma_n$ 是 $n$ 至多**二次**的**多项式**，且对 $\omega$ 至多二次依赖。具体而言，可写为以下 Cook-Zalutskiy 形式[^CZ2014]：

$$\begin{aligned}
\alpha_n(\omega) &= n^2 + (D_0(\omega) + 1)n + D_0(\omega) \\
\beta_n(\omega) &= -2n^2 + (D_1(\omega) + 2)n + D_3(\omega) \\
\gamma_n(\omega) &= n^2 + (D_2(\omega) - 3)n + D_4(\omega) - D_2(\omega) + 2
\end{aligned}$$

其中 $D_i(\omega)$ 是 $\omega$ 的多项式（至多 $\omega^2$）。此形式下，三对角矩阵 $M(\omega)$ 满足：

$$M(\omega) = M_0 + \omega M_1 + \omega^2 M_2$$

即**二次矩阵多项式**。行列式 $\det M(\omega)$ 是 $\omega$ 的 $2N$ 次多项式，QNM 条件 $\det M(\omega) = 0$ 对应 $2N$ 个复根。

---

### 2. 度规分类表格

| 度规 | G1 (Petrov D) | G2 (三项递推) | G3 (多项式系数) | 三对角结构 | 特殊说明 |
|:----:|:-------------:|:-------------:|:--------------:|:----------:|:--------|
| **Schwarzschild** | ✓ | ✓ | ✓ | **完全满足** | $\alpha_n = (n+1-2i\omega)^2$，最简形式；$a=0$ 时角向退化为球谐函数 |
| **Kerr** | ✓ | ✓ | ✓ | **完全满足** | Cook-Zalutskiy (2014) 多项式系数；三对角谱丛的二叉树纤维化完全成立 |
| **RN (Reissner-Nordström)** | ✓ | ✓ | ✓ | **完全满足** | 电荷 $Q$ 引入额外 $1/r$ 项，$D_i$ 系数修正但保持二次多项式形式 |
| **Kerr-Newman** | ✓ | ✓ | ✓ | **完全满足** | 自旋 $a$ + 电荷 $Q$，系数耦合 $aQ$，谱丛性质保持 |
| **Kerr-dS/AdS** | ✓ | ✓ | ✓ | **完全满足** | 宇宙常数 $\Lambda$ 引入四次多项式修饰，径向方程奇点结构改变但递推仍三项 |
| **Dilaton** | ✓ | ✓ | ? | **部分满足** | 标量场耦合导致系数可能为 $n$ 的高次多项式（见第二部分分析） |
| **动态时空 (非 Petrov D)** | ✗ | N/A | N/A | **不适用** | 非 Petrov D 型时空无法分离变量，无 Teukolsky 方程形式 |

---

### 3. RN 度规的详细分析

Reissner-Nordström 度规描述带电荷 $Q$ 的球对称黑洞。度规形式：

$$ds^2 = -\left(1 - \frac{2M}{r} + \frac{Q^2}{r^2}\right) dt^2 + \left(1 - \frac{2M}{r} + \frac{Q^2}{r^2}\right)^{-1} dr^2 + r^2 d\Omega^2$$

#### 3.1 分离变量性（G1 验证）

RN 度规也是 Petrov D 型（$a=0$ 的 Kerr-Newman 特例），Newman-Penrose 形式中 Weyl 张量仅有 $\Psi_2 \neq 0$。Teukolsky 方程可分离变量，径向和角向完全解耦。角向方程退化为自旋权球谐函数（无 spheroidal 畸变），分离常数 $\lambda = l(l+1) - s(s+1)$。

与 Kerr 的区别：RN 的 $\rho = -1/r$（而非 Kerr 的 $\rho = -1/(r - i a\cos\theta)$），角向方程不依赖 $\omega$。

#### 3.2 径向方程与三项递推（G2 验证）

RN 的 Teukolsky 径向方程为[^Ber06]：

$$\Delta^{-s} \frac{d}{dr}\left(\Delta^{s+1} \frac{dR}{dr}\right) + \left(\frac{K^2 - 2is(r-M)K}{\Delta} + 4is\omega r - \lambda\right) R = 0$$

其中 $\Delta = r^2 - 2Mr + Q^2$，$K = (r^2 + a^2)\omega - am$（RN 中 $a=0$，故 $K = r^2\omega$）。

外视界 $r_+ = M + \sqrt{M^2 - Q^2}$ 和内视界 $r_- = M - \sqrt{M^2 - Q^2}$。在 $r_+$ 处的渐近展开：

$$R \sim e^{i\omega r_*} (r - r_+)^{s - i\sigma_+} \sum_{n=0}^\infty a_n \left(\frac{r - r_+}{r}\right)^n$$

其中 $\sigma_+ = \frac{2\omega r_+^2}{r_+ - r_-}$。展开系数 $a_n$ 满足三项递推：

$$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0$$

#### 3.3 多项式系数形式（G3 验证）

RN 的 Cook-Zalutskiy 形式系数[^CZ2014_general]：

$$\begin{aligned}
D_0 &= 1 + s + 2i\sigma_+ \\
D_1 &= 4i\omega r_+ - 2(1 + s + i\sigma_+ + i\sigma_-) + (1 + s + 2i\sigma_-) - (1 + s + 2i\sigma_+) - 2 \\
D_2 &= 2(1 + s + i\sigma_+ + i\sigma_-) - (1 + s + 2i\sigma_-) + 2 \\
D_3 &= (1 + s + i\sigma_+ + i\sigma_-)\left(4i\omega r_+ - (1 + s + 2i\sigma_+)\right) \\
&\quad - \left[\lambda + \omega^2(r_+^2 + 2Mr_+ + 4r_+^2 - 2Q^2) - 8\omega^2\right] \\
D_4 &= (1 + s + i\sigma_+ + i\sigma_-)\left((1 + s + i\sigma_+ + i\sigma_-) - (1 + s + 2i\sigma_-) + 1\right)
\end{aligned}$$

其中 $\sigma_- = \frac{2\omega r_-^2}{r_- - r_+} = -\frac{2\omega r_-^2}{r_+ - r_-}$，$s$ 为自旋权重。

**关键观察**：电荷 $Q$ 仅通过修改 $r_\pm$ 影响 $D_i$ 系数。$D_i(\omega)$ 对 $\omega$ 的依赖仍然是至多二次的，$\alpha_n, \beta_n, \gamma_n$ 对 $n$ 的依赖仍然是二次多项式。**三对角谱丛结构保持**。

#### 3.4 RN 特有的谱丛性质

与 Schwarzschild 相比，RN 谱丛的差异：
1. 分支点位置受 $Q$ 调制：$\det M(\omega)$ 的零点在复 $\omega$ 平面中的分布因 $Q$ 而偏移
2. 两支视界 $r_\pm$ 导致 $\sigma_+$ 和 $\sigma_-$ 均含 $\omega$，谱丛曲率 $q'(\omega)$ 的解析结构更丰富
3. 极端 RN 极限 $Q \to M$ 时 $r_+ \to r_-$，$\sigma_+$ 发散，需重新标度展开——谱丛在此极限下退化

---

### 4. Kerr-Newman 联合推广

Kerr-Newman 度规同时包含自旋 $a$ 和电荷 $Q$，是 Kerr 和 RN 的最一般联合。度规形式（Boyer-Lindquist 坐标）：

$$ds^2 = -\frac{\Delta}{\Sigma}(dt - a\sin^2\theta d\phi)^2 + \frac{\Sigma}{\Delta}dr^2 + \Sigma d\theta^2 + \frac{\sin^2\theta}{\Sigma}\left[(r^2 + a^2)d\phi - a dt\right]^2$$

其中 $\Delta = r^2 - 2Mr + a^2 + Q^2$，$\Sigma = r^2 + a^2\cos^2\theta$。

#### 4.1 三条件验证

| 条件 | 验证 |
|:---|:----|
| **G1** | Kerr-Newman 是 Petrov D 型（Carter 1968）；Teukolsky 方程可分离变量；角向方程为自旋加权椭球谐函数方程，与 Kerr 同形式 |
| **G2** | 径向方程在 $r_+$ 处的渐近展开给出三项递推：$K = (r^2 + a^2)\omega - am$ 中 $r_\pm$ 由 $M, a, Q$ 共同决定；视界表面引力 $\kappa_+ = (r_+ - r_-)/(2(r_+^2 + a^2))$ 含 $Q$ 修正 |
| **G3** | Cook-Zalutskiy 多项式形式保持；$D_i$ 系数中 $a$ 和 $Q$ 通过 $r_\pm, \sigma_\pm$ 联合出现，存在交叉项 $aQ$，但整体仍为 $\omega$ 的二次多项式 |

#### 4.2 Kerr-Newman 的 D 系数

Kerr-Newman 的 $D_i$ 系数的完整形式（推广自 Cook-Zalutskiy 2014）：

$$\begin{aligned}
r_\pm &= M \pm \sqrt{M^2 - a^2 - Q^2} \\
\sigma_+ &= \frac{(r_+^2 + a^2)\omega - am}{r_+ - r_-} \\
\sigma_- &= \frac{(r_-^2 + a^2)\omega - am}{r_- - r_+} \\
D_0 &= 1 + s + 2i\sigma_+ \\
D_1 &= 4i\omega r_+ - 2(1 + s + i\sigma_+ + i\sigma_-) + (1 + s + 2i\sigma_-) - D_0 - 2 \\
D_2 &= 2(1 + s + i\sigma_+ + i\sigma_-) - (1 + s + 2i\sigma_-) + 2 \\
D_3 &= (1 + s + i\sigma_+ + i\sigma_-)\left(4i\omega r_+ - D_0\right) \\
&\quad - \left[\lambda + a^2\omega^2 - 2am\omega + \omega^2(r_+^2 + 2Mr_+ + 4r_+^2 - 2Q^2) - 8\omega^2\right] \\
D_4 &= (1 + s + i\sigma_+ + i\sigma_-)\left((1 + s + i\sigma_+ + i\sigma_-) - (1 + s + 2i\sigma_-) + 1\right)
\end{aligned}$$

#### 4.3 谱丛性质的保持

Kerr-Newman 谱丛的核心性质与 Kerr 定性一致：

1. **二叉树纤维化保持**：$M(\omega)$ 的三对角结构不变，off-diagonal rank-1 性质不变，Schur 补的递归分解仍然有效
2. **单值性保持**：双重同伦延拓（$a$ + $m$）直接适用；电荷 $Q$ 可作为第三同伦参数
3. **分支点密度受 $Q$ 影响**：$Q$ 增大时 $r_+ - r_-$ 减小，$\sigma_\pm$ 发散速度变化，分支点分布密度随之改变
4. **极端极限的谱丛退化**：$a^2 + Q^2 \to M^2$ 时两支视界合并，$r_+ - r_- \to 0$，$\sigma_+ \to \infty$，谱丛在该极限下的紧致化需谨慎

---

### 5. 度规条件的谱丛解释

谱丛结构 $\mathcal{S} = \{(\omega, \lambda): \det(M(\omega) - \lambda I) = 0\}$ 的几何性质由三个条件分别保证：

| 条件 | 谱丛解释 | 被违反时的后果 |
|:---|:--------|:------------|
| **G1**（分离变量性） | 底空间 $B$ 是 1 维的 $\mathbb{C}_\omega$（单复频率参数）；角向 $\lambda$ 是径向方程的"外部参数"而非底空间坐标 | 底空间维数 $\ge 2$，谱丛变为高维复流形，截面分析失去简单性 |
| **G2**（三项递推性） | 谱丛的纤维由**三对角矩阵** $M(\omega)$ 定义，即 $\lambda_i(\omega) \in \sigma(M(\omega))$ | 矩阵带宽 $\ge 2$，二叉树纤维化退化为 $k$-ary 树，失去了 off-diagonal rank-1 的关键简化 |
| **G3**（多项式系数性） | $M(\omega)$ 是**二次矩阵多项式**：$M_0 + \omega M_1 + \omega^2 M_2$；特征值代数曲线 $\det(M(\omega) - \lambda I) = 0$ 是 $\mathbb{C}^2$ 中的**代数曲线**，具有良好的代数几何性质 | $M(\omega)$ 对 $\omega$ 的依赖超越二次，行列式不是多项式，谱丛的分析性质退化 |

**定理 2**（谱丛良定义性）：若 G1–G3 均满足，则：
- $\det M(\omega)$ 是 $\omega$ 的 $2N$ 次多项式（$N$ 为矩阵截断维数）
- QNM 频率是 $\det M(\omega) = 0$ 的根——即谱丛 $\mathcal{S}$ 在 $\lambda=0$ 截面上与底空间的交点
- 谱丛的 Cech 上同调 $H^1(B, \mathcal{O}^*)$ 定义的分支点集非空但有限
- 单值群 $\mathcal{M} \subseteq S_N$ 有有限生成元

---

## 第二部分：非三对角推广的展望

### 1. Dilaton 度规的特殊性

Dilaton 引力（如 GHS/Garafinkle-Horowitz-Strominger 解）将 Maxwell 场与标量场 $\phi$ 耦合，度规形式[^GHS91]：

$$ds^2 = -\left(1 - \frac{2M}{r}\right) dt^2 + \left(1 - \frac{2M}{r}\right)^{-1} dr^2 + r(r - 2a\phi_0) d\Omega^2$$

其中标量场 $\phi$ 的非平凡背景破坏了 Einstein-Maxwell 理论的简单结构。

#### 1.1 条件验证问题

| 条件 | 状态 | 说明 |
|:---|:----|:----|
| **G1** | ✓ | Dilaton 黑洞在某些参数下仍为 Petrov D 型，Teukolsky 方程原则上可分离 |
| **G2** | ✓ | 径向方程在视界处的渐近展开仍产生三项递推（见下分析） |
| **G3** | **?** | 此为核心问题——标量场耦合可能破坏系数的二次多项式性质 |

#### 1.2 系数结构分析

Dilaton 耦合引进的修正：

1. **度规修饰**：$\Delta(r)$ 中含有标量场指数因子 $e^{-2\phi}$，不再是 $r$ 的二次多项式
2. **有效势变化**：径向 Teukolsky 方程中出现额外 $1/r^2$ 修饰项，来自标量场对曲率的反馈
3. **展开系数修正**：在 $r_+$ 处做 Frobenius 展开时，递推系数 $\alpha_n, \beta_n, \gamma_n$ 可能不再是 $n$ 的二次多项式

具体而言，设 Dilaton Teukolsky 径向方程为：

$$\Delta(r)^{-s} \frac{d}{dr}\left(\Delta(r)^{s+1} \frac{dR}{dr}\right) + \left(\frac{K(r)^2 - 2is\Delta(r)' K(r)}{\Delta(r)} + \text{标量修正项} - \lambda\right) R = 0$$

其中 $\Delta(r)$ 不再是 $r$ 的二次多项式（因标量场耦合），$K(r)$ 也可能含修饰项。此时 Frobenius 展开的递推关系可能变为：

$$\alpha_n^{(3)} a_{n+3} + \alpha_n^{(2)} a_{n+2} + \alpha_n^{(1)} a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0$$

即**四对角**或更高带宽的递推关系。

#### 1.3 谱丛结构退化

若 G3 被违反，谱丛结构发生以下退化：

1. **矩阵带宽增加**：$M(\omega)$ 从三对角变为五对角或更宽，失去 off-diagonal rank-1 性质
2. **二叉树 $\to$ $k$-ary 树**：Schur 补的递归分解中，每个节点分裂为 $k$ 个子节点（$k \ge 2$），不再是二叉树
3. **剪枝算法失效**：谱丛剪枝策略依赖于二叉树结构，带宽增加后复杂度从 $O(N)$ 升至 $O(N^k)$
4. **但仍可能存在广义谱丛理论**：只要递推是线性的且截断有限，仍可定义矩阵族 $M(\omega)$，但失去了三对角形式的核心简化

#### 1.4 Dilaton 保持三项递推的特殊情形

有文献[^PaLa96]指出，某些特定 Dilaton 耦合参数下，通过对径向变量做 Mobius 变换或重标度，三项递推可保持。此时 G3 的破坏仅体现在系数为 $n$ 的高次多项式（三次或四次），而非带宽增加。这属于"弱 G3 破坏"情形——谱丛仍为三对角，但 $M(\omega)$ 不再是二次矩阵多项式，代数几何性质退化。

---

### 2. 高维推广（BMPV、Myers-Perry）

#### 2.1 Myers-Perry 度规

$D$ 维 Myer-Perry 黑洞（旋转推广的 Schwarzschild-Tangherlini）在奇数维有 $(D-1)/2$ 个独立的旋转参数。Teukolsky 方程可推广到高维[^KuMa05]：

$$\Psi = e^{-i\omega t} e^{i\sum_j m_j \phi_j} S(\theta_1, \dots, \theta_{D-3}) R(r)$$

#### 2.2 谱丛结构的变化

| 性质 | 4D Kerr | $D$ 维 Myers-Perry |
|:---|:--------|:-----------------|
| Petrov 类型 | D 型 | 不一定为 D 型（$D>4$ 时 Petrov 分类不直接推广） |
| 分离变量 | ✓（Carter 常数） | 部分对称性下可行 |
| 径向递推 | 三项递推 | **三项递推保持**（对某些对称类） |
| 角向方程 | 自旋加权椭球谐函数 | 高维权球谐函数（无 spheroidal 畸变的简单形式） |
| 谱丛维数 | $\mathbb{C}_\omega$（1 维） | $\mathbb{C}^{D-1}_\omega$（多频率参数） |

#### 2.3 BMPV 黑洞的特殊性

BMPV（Breckenridge-Myers-Peet-Vafa）是 5 维超引力中的旋转带电黑洞：

$$\begin{aligned}
ds^2 &= -f^{-2/3}(dt + \omega)^2 + f^{1/3} ds^2_{\mathbb{R}^4} \\
\omega &= \frac{J}{2r^2}(\sin^2\theta d\phi_1 + \cos^2\theta d\phi_2)
\end{aligned}$$

- BMPV 也是 Petrov D 型（5 维意义下）
- 两个旋转参数 $J_1, J_2$ 导致两个独立的 azimuthal 角
- Teukolsky 方程在超对称框架下可分离
- 径向递推为三项，但系数涉及两个频率 $\omega_1, \omega_2$
- 谱丛 $\mathcal{S}$ 的全空间维数为 $D-1 = 4$（$\omega, \omega_1, \omega_2, m$），特征值代数曲线变为 $\mathbb{C}^4$ 中的超曲面

---

### 3. 结论

#### 3.1 三对角谱丛的适用范围

**凡是 Petrov D 型、稳态轴对称的 4 维黑洞时空**，Leaver 方法均适用，三对角谱丛结构保持。这包括：

- Schwarzschild（$a=0, Q=0$）
- Kerr（$a>0, Q=0$）
- RN（$a=0, Q>0$）
- Kerr-Newman（$a>0, Q>0$）
- Kerr-(dS/AdS)（加入宇宙常数 $\Lambda$）
- 带 NUT 参数的扩展（部分情形）

这些度规满足 G1–G3 条件，谱丛的二叉树纤维化、双重同伦延拓的单值性、LACI 判据全部成立。

#### 3.2 推广的边界

三对角谱丛结构的**边界**在：

1. **非 Petrov D 型时空**（如动态时空、双黑洞背景）：G1 失败，无法分离变量，无 Teukolsky 方程可写
2. **Dilaton 类度规（强标量场耦合）**：G3 可能失败，三对角退化为高带宽或高次多项式系数
3. **高维旋转黑洞**：径向三项递推保持，但谱丛底空间维数随 $D$ 增加

#### 3.3 基于此分析的建议

1. **当前框架**（Kerr 的三对角谱丛 + 双初始向量逆迭代法求解器）在 Kerr-Newman 和 RN 中**直接可用**，只需修改 $r_\pm$ 和 $D_i$ 系数
2. **Dilaton 类问题**需先判断弱 G3 破坏（三对角 + 高次多项式）还是强 G3 破坏（五对角以上）
3. **高维推广**需开发多参数谱丛理论，底空间从 $\mathbb{C}_\omega$ 推广到 $\mathbb{C}^{D-1}$
4. **非 Petrov D 型**需要全新的谱丛框架，Leaver 方法不再适用

---

## 第二部分：非引力系统的三对角谱丛推广

在引力系统中，三对角谱丛结构源于 Teukolsky 方程的 Leaver 求解。然而，相同的数学结构——$\omega$-参数化三对角矩阵族的二叉树纤维化——在非引力系统中以"连分数展开"的形式广泛存在。本部分将 G1-G3 条件推广到更一般的语境。

### 5. 谱丛条件的非引力推广

**定理 2**（一般三对角谱丛存在性）。一个物理系统可被赋予三对角谱丛结构 $\mathcal{S} = \{(\omega, \lambda): \det(M(\omega) - \lambda I) = 0\}$，其中 $M(\omega)$ 为三对角矩阵族，当且仅当以下推广条件成立：

| 条件 | 引力版本 | 非引力推广 | 物理含义 |
|:---:|:---------|:----------|:---------|
| G1' | Petrov D + 可分离变量 | 存在单频率参数的**线性响应理论** | 底空间 $\mathbb{C}_\omega$ 是 1 维的 |
| G2' | 三项递推系数 | 物理量的频率响应可展开为**连分数** | 三对角矩阵族 $M(\omega)$ 存在 |
| G3' | 多项式系数（至多二次） | 连分数系数具有规则的结构（至多多项式依赖） | 特征值代数曲线有良好解析性质 |

**证明**（构造性）。连分数 $f(\omega) = a_0 \Big/ \Big(b_0(\omega) + \frac{a_1(\omega)}{b_1(\omega) + \frac{a_2(\omega)}{\ddots}}\Big)$ 与三对角矩阵 $M(\omega)f(\omega) = e_1$ 等价——这是 Jacobi 连分数与连分式矩阵的标准对应（Wall 1948），且 $M(\omega)$ 的 off-diagonal rank-1 正对应连通分数的"相邻层耦合"。$\square$

### 5.1 非牛顿流变学

**实例 1**（流变谱丛）。广义 Maxwell 模型（$N$ 个 Maxwell 单元并联）的复数剪切模量：

$$G^*(\omega) = G_\infty + \sum_{i=1}^N \frac{G_i i\omega\tau_i}{1 + i\omega\tau_i}$$

等价于三对角谱丛 $\mathcal{S}_{\text{rheo}}$，其矩阵族由弛豫谱 $\{G_i, \tau_i\}$ 编码。

**定理 3**（流变-引力谱丛同构）。Kerr QNM 的 Leaver 三对角谱丛 $\mathcal{S}_{\text{Teuk}}$ 与非牛顿流变学的广义 Maxwell 谱丛 $\mathcal{S}_{\text{rheo}}$ 之间存在严格的范畴同构：

$$\boxed{\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{rheo}}}$$

**对应表**：

| 引力（Kerr QNM） | 非牛顿流变学 | 物理意义 |
|:----------------|:-----------|:---------|
| 复频率 $\omega$ | 角频率 $\omega$ | 谱丛底空间参数 |
| 径向展开系数 $a_n$ | Maxwell 单元权重 $G_i$ | 三对角矩阵元素 |
| QNM 频率 $\det M(\omega)=0$ | 黏弹性共振 $\epsilon''(\omega)$ 峰值 | 谱丛截面 $\lambda=0$ |
| 非物理根 | 非物理弛豫模 | 分支点叶间跳跃 |
| 连续分数 $R_0(\omega)=0$ | 复杂黏度连分数 $\eta^*(\omega)$ | 二叉树 Schur 补条件 |
| 分支点 $\omega_0$ | 流变学"非线性跃迁"临界频率 | 谱叶交换 |

**推论**：Leaver 连续分数法的全部谱丛工具——剪枝算法、单值群分析、双重同伦延拓——可直接迁移到流变学参数反演（从 $G^*(\omega)$ 数据提取 $H(\tau)$）。详见 Paper VI §9.3。

### 5.2 凝聚态物理：NRG Wilson 链

**实例 2**（NRG 谱丛）。数值重整化群（NRG）的 Wilson 链 Hamiltonian 是**显式三对角**的：

$$H_N = \sum_{n=0}^N \varepsilon_n f_n^\dagger f_n + \sum_{n=0}^{N-1} t_n (f_n^\dagger f_{n+1} + \text{h.c.})$$

在能量 $\omega$ 为参数时，杂质谱函数 $A(\omega) = -\frac{1}{\pi}\text{Im}\,G_{\text{imp}}(\omega)$ 可通过连分数求解：

$$G_{\text{imp}}(\omega) = \frac{1}{\omega - \varepsilon_0 - \frac{t_0^2}{\omega - \varepsilon_1 - \frac{t_1^2}{\ddots}}}$$

**定理 4**（NRG-引力谱丛同构）。NRG Wilson 链的谱函数连分数求解与 Leaver 三对角谱丛同构：

$$\boxed{\mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Teuk}}}$$

NRG 的"对数离散化"参数 $\Lambda$ 对应谱丛底空间 $\mathbb{C}_\omega$ 的局部坐标变换，NRG 递归对角化对应谱丛的逐叶遍历。

### 5.3 凝聚态物理：记忆函数连分数

**实例 3**（记忆函数谱丛）。光导率 $\sigma(\omega)$ 的记忆函数形式：

$$\sigma(\omega) = \frac{\sigma_0}{1 + i\omega\tau + M(\omega)}, \quad M(\omega) = \frac{\Delta_1^2}{i\omega + \gamma_1 + \frac{\Delta_2^2}{i\omega + \gamma_2 + \ddots}}$$

**定理 5**（记忆函数-引力谱丛同构）。记忆函数 $M(\omega)$ 的连分数展开与 Leaver 三对角谱丛同构。$M(\omega)$ 的极点对应三对角谱丛的分支点，行列式条件 $\det A_M(\omega_p) = 0$ 统一描述分支结构。

### 5.4 三类系统的谱丛统一

| 系统 | 参数 | 三对角来源 | 分支点物理意义 | 同构类型 |
|:----|:----|:----------|:-------------|:--------|
| Kerr QNM (Paper VIII/XXVI) | $\omega$ 复频率 | Leaver 三项递推 | 非物理根吸引域 | $\mathcal{S}_{\text{Teuk}}$ |
| 非牛顿流变学 (Paper VI §9.3) | $\omega$ 角频率 | Maxwell 模型连分数 | 非线性跃迁临界频率 | $\mathcal{S}_{\text{rheo}} \cong \mathcal{S}_{\text{Teuk}}$ |
| NRG 杂质谱 (Paper XIV §5.7) | $\omega$ 能量 | Wilson 链三对角 | Kondo 共振奇异点 | $\mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Teuk}}$ |
| 记忆函数 (Paper XIV §5.7) | $\omega$ 频率 | 记忆函数连分数 | 量子相变临界发散 | $\mathcal{S}_{\text{mem}} \cong \mathcal{S}_{\text{Teuk}}$ |

**核心结论**：三对角谱丛结构不是 Kerr QNM 的专有结构，而是**广义线性响应理论中连分数展开的必然几何投影**。Leaver 在引力微扰中发现的"非物理根-物理根"对偶，在流变学中对应"非物理解-物理解弛豫模"，在 NRG 中对应"非物理谱权重-物理谱函数"。这一统一揭示了谱丛理论作为计算数学通用工具的潜力。

---

## 版本记录

**v0.2（2026-07-25）**：新增第二部分"非引力系统的三对角谱丛推广"（§5-5.4），将分析扩展到非牛顿流变学（广义 Maxwell 连分数）、NRG Wilson 链三对角、记忆函数连分数三个新实例，建立四类系统的谱丛统一表，确立三对角谱丛结构作为"广义线性响应理论中连分数展开的几何投影"的统一视角。

**v0.1（2026-07-25）**：初版。提出三对角谱丛结构存在性的三个充要条件（G1–G3），逐一分析 Schwarzschild、Kerr、RN、Kerr-Newman、Kerr-dS/AdS、Dilaton 和动态时空，给出 RN 和 Kerr-Newman 的完整 D 系数形式，讨论 Dilaton 和高维推广的非三对角扩展。
