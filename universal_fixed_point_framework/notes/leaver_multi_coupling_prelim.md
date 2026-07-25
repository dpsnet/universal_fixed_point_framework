# 多耦合谱丛预研笔记：引力+电磁+Dirac 耦合系统的谱丛构造

**版本**：v0.1（2026-07-25）

**摘要**：当前 Leaver 谱丛理论专注于单自旋 s=-2（引力扰动）的 Teukolsky 方程。实际黑洞物理中，引力、电磁和 Dirac 场在弯曲时空背景下存在复杂的耦合结构。本笔记预研将谱丛框架从单自旋推广到多自旋耦合系统的可行性与路径，系统梳理 Kerr-Newman 背景下的可分性问题、已有数学成果、谱丛几何的推广方向，以及与 UFPF 现有工作的衔接。

---

## 1. 背景与动机

### 1.1 当前谱丛框架的单自旋局限

现有谱丛理论（`notes/spectral_sheaf_leaver.md`, `notes/leaver_triple_parameter_sheaf.md`）的核心对象是单自旋 Teukolsky 方程的三项递推谱丛：

$$\mathfrak{S}^{(s=-2)} = \{(a,m,\omega,\lambda): \det(M^{(s=-2)}_{a,m}(\omega) - \lambda I) = 0\}$$

其中 $M^{(s)}_{a,m}(\omega)$ 是自旋权重为 $s$ 的 Teukolsky 径向方程离散化后得到的三对角矩阵族。该框架已成功处理以下内容：
- 三参数 $(a,m,\omega)$ 谱丛的纤维积构造
- I/II/III 型奇异纤维的完整分类（Phase 59A）
- $D_{\mathrm{diss}}$ 函子的嵌入验证
- LACI 公理化的严格化

然而，真实物理场景涉及多个自旋场的耦合。例如：
- **Kerr-Newman 黑洞**：引力扰动（s=±2）与电磁扰动（s=±1）在背景电磁场下相互耦合
- **引力-Dirac 系统**：s=±1/2 的费米场与 s=±2 的引力场的相互作用
- **Extreme Mass Ratio Inspiral (EMRI)** 中的辐射反作用问题需要同时处理多极多自旋的扰动模式

### 1.2 为什么需要多耦合谱丛

单自旋 Teukolsky 方程的可分性依赖于 Kerr 背景的高度对称性（Killing-Yano 张量）。当引入耦合后：

1. **可分性可能失效**：耦合项破坏径向-角向分离
2. **谱丛纤维结构复杂化**：耦合场的特征值系统不再是独立的谱丛，而是通过耦合参数连结成联合谱丛
3. **奇异纤维分类需要推广**：耦合参数引入新的退化机制

因此，建立多耦合谱丛框架是 Leaver 谱丛理论从"单通道"走向"多通道"的关键步骤。

---

## 2. Kerr-Newman 的可分性问题

### 2.1 标量场：已完全解决

**Carter (1968)** 首次证明了 Kerr-Newman-de Sitter 时空中标量场波动方程（s=0）的径向-角向完全可分性 [Carter, Phys. Rev. 174, 1559 (1968)]。这是通过发现 Kerr 时空的"第四运动常数"（Carter 常数）实现的。

标量场方程的分离变量形式：

$$\left[\frac{d}{dr}\Delta\frac{d}{dr} + \frac{(r^2+a^2)^2\omega^2 - 4aMrm\omega + a^2m^2}{\Delta} - \lambda_{lm}\right]R(r) = 0$$
$$\left[\frac{1}{\sin\theta}\frac{d}{d\theta}\sin\theta\frac{d}{d\theta} - \frac{m^2}{\sin^2\theta} + a^2\omega^2\cos^2\theta - 2a\omega s\cos\theta + \lambda_{lm}\right]S(\theta) = 0$$

其中 $\Delta = r^2 - 2Mr + a^2 + Q^2$，$\lambda_{lm}$ 为分离常数。对标量场，这种可分性对 Kerr、Kerr-Newman 及 Kerr-Newman-de Sitter 均成立。

### 2.2 电磁/引力扰动：仅对单自旋可分离

对于自旋 $s \neq 0$ 的场，在 Kerr 背景（$Q=0$）上，Teukolsky (1973) 证明了：

$$\mathcal{T}^{(s)}\Psi^{(s)} = 0$$

其中 $\mathcal{T}^{(s)}$ 是依赖于自旋权重 $s$ 的二阶偏微分算子。该方程对任意 $s$ 在 Kerr 背景上均可分离，$s=\pm\frac12, \pm1, \pm2$ 分别对应 Dirac、Maxwell 和引力扰动。

然而，在 **Kerr-Newman 背景**（$Q \neq 0$）上，**只有标量场和 Dirac 场（s=0, ±1/2）保持可分性**。电磁和引力扰动（s=±1, ±2）的方程不再可分离 [Khanal, Phys. Rev. D 28, 1291 (1983); Chandrasekhar, The Mathematical Theory of Black Holes (1983)]。

### 2.3 Kerr-Newman 全耦合系统的未解决状态

**核心开放问题**：Kerr-Newman 背景下，引力-电磁耦合系统的完备可分性至今未被证明存在。具体地：

1. **耦合机制**：背景电荷 $Q$ 通过电磁张量 $F_{\mu\nu}$ 引入额外的曲率耦合项，使 Weyl 张量扰动 $\psi_0, \psi_4$ 和 Maxwell 张量扰动 $\phi_0, \phi_2$ 之间产生不可忽略的交叉项
2. **Kinnersley 零标架下的耦合方程**（Chandrasekhar, 1983, §63-65）：
   - $s=+2$（$\psi_0$）与 $s=+1$（$\phi_0$）耦合
   - $s=-2$（$\psi_4$）与 $s=-1$（$\phi_2$）耦合
   - 耦合强度由黑洞电荷 $Q$ 控制
3. **目前进展**：Giorgi-Wan (2024) [arXiv:2407.10750] 在轴对称且在 $|a|\ll M$, $|Q|<M$ 条件下证明了对 Kerr-Newman Teukolsky 系统的有界性和多项式衰减，但**未涉及方程的完全分离**

---

## 3. 已有结果综述

### 3.1 Finster-Smoller (2007)：Schwarzschild 高自旋 Teukolsky 衰减

**Finster, Smoller** [arXiv:gr-qc/0607046] 证明了在 Schwarzschild 背景下，自旋 $s=1$（电磁）和 $s=2$（引力）的 Teukolsky 方程具紧支撑光滑初始数据时，解在 $L^\infty_{\mathrm{loc}}$ 意义下随时间衰减。这是首个对高自旋 Teukolsky 方程时间依赖解的严格数学结果，确立了 Schwarzschild 黑洞在线性电磁和引力扰动下的稳定性。

**技术突破**：使用 Whiting 形式的 Teukolsky 方程 → Jost 解构造 → Hamiltonian 公式化 → WKB 估计 → 围道变形到实轴 → 衰减证明。

**与谱丛理论的关系**：该工作证明了 Schwarzschild 背景下 $s=\pm1,\pm2$ 的系统级稳定性，为多自旋谱丛的**纤维一致性**提供了底层数学保证。

### 3.2 Dafermos-Holzegel-Rodnianski (2017)：Kerr 的 Teukolsky 有界性/衰减

**Dafermos, Holzegel, Rodnianski** [arXiv:1711.07944] 将结果推广到缓慢旋转 Kerr 背景（$|a| \ll M$）的 $s=\pm2$ Teukolsky 方程，证明了：
- 解的 **有界性**（boundedness）
- **多项式衰减**（polynomial decay）

**技术核心**：
- 推广了 Schwarzschild 情形中使用的高阶量 $P$ 和 $\underline{P}$
- 这些量的存在性与 Chandrasekhar 变换理论密切相关
- 使用 physical-space Morawetz 估计

**待推广**：全次极值参数范围 $|a|<M$ 的证明尚在推进中。

### 3.3 Berens-Gravely-Lupsasca (2023-2025)：Kerr 度规摄动的显式重构

**Berens, Gravely, Lupsasca** [arXiv:2403.20311] 系列工作完成了 Kerr 背景下线性度规摄动的显式重构：
- Part I：对给定 Weyl 标量的模式，显式写出辐射规范下的度规摄动
- Part II：包含宇宙学常数推广到 Kerr-(A)dS
- 无需 Hertz 势的中间步骤，直接使用分离的径向和角向模式
- 通过 Teukolsky-Starobinsky 恒等式消除模式函数的导数

**与谱丛理论的关系**：这项工作提供了从单自旋谱丛（s=-2 或 s=+2）完整重构物理度规摄动的"解码器"，是多耦合谱丛中引力部分的**输出端验证工具**。

### 3.4 Chandrasekhar 变换理论

**Chandrasekhar (1975-1983)** 建立的变换理论是理解耦合自旋之间关系的核心：

1. **Schwarzschild 情形**：Regge-Wheeler 方程（轴向）与 Zerilli 方程（极向）是**同谱的**（isospectral），通过 Chandrasekhar 变换（即 Darboux 变换）相连 [Glampedakis-Johnson-Kennefick, arXiv:1702.06459]
2. **Kerr 情形**：$s=+2$（$\psi_0$）和 $s=-2$（$\psi_4$）通过 Teukolsky-Starobinsky 恒等式相连
3. **$s=\pm2$ 变换的核心**：存在四阶微分算子 $\mathcal{D}$ 使得 $\mathcal{D} \psi_0 \propto \psi_4$，反之亦然

**谱丛视角**：Chandrasekhar 变换实质上是谱丛纤维之间的**自旋规范变换**——它将一个自旋权重的谱叶映射到另一个自旋权重的谱叶，而不改变特征值的谱集。这暗示了多自旋谱丛存在自然的"水平连接"。

---

## 4. 谱丛视角的推进

### 4.1 多自旋联合谱丛的直积构造

**定义 4.1**（多自旋联合谱丛）。对自旋指标集合 $S = \{s_1, s_2, \dots, s_k\}$，定义联合谱丛为各单自旋谱丛的**纤维积**（fibered product）：

$$\mathfrak{S}^{(S)} = \bigtimes_{\pi} \mathfrak{S}^{(s_i)} = \{(p, \lambda^{(s_1)}, \dots, \lambda^{(s_k)}) : \det(M^{(s_i)}_{a,m,\omega} - \lambda^{(s_i)}I) = 0, \forall s_i \in S\}$$

这里 $\pi$ 是到公共参数空间 $\mathcal{P} = (a,m,\omega,Q,\dots)$ 的投影。必须注意，这一定义仅在**无耦合**（各自旋独立演化）时成立。

**定义 4.2**（耦合修正）。当存在耦合（如 Kerr-Newman 中 $s=+2$ 与 $s=+1$ 的耦合）时，联合谱丛需由**耦合参数族** $\{M^{(s_i,s_j)}_{a,m,\omega,Q}\}$ 构造：

$$\mathfrak{S}^{(S)}_{\text{coupled}} = \{(p, \lambda): \det(M_{\text{total}}(p) - \lambda I) = 0\}$$

其中 $M_{\text{total}}$ 是耦合系统的**分块三对角矩阵**：

$$M_{\text{total}} = \begin{pmatrix}
M^{(s_1)} & C^{(s_1,s_2)} & \cdots \\
C^{(s_2,s_1)} & M^{(s_2)} & \cdots \\
\vdots & \vdots & \ddots
\end{pmatrix}$$

对角块 $M^{(s_i)}$ 为各单自旋的 Teukolsky 离散化；非对角块 $C^{(s_i,s_j)}$ 为耦合项（$Q$-相关）。

### 4.2 耦合项作为谱丛纤维间的联络

在谱丛几何中，耦合项可以自然地理解为**纤维之间的联络**（connection between fibers）：

- **无耦合情形**：各 $s$-纤维是独立的平直积 $F_{s_1} \times F_{s_2}$
- **弱耦合情形**（$|Q| \ll M$）：联络形式 $\omega^{(s_i,s_j)}$ 定义了纤维间的平行移动，将 $\mathfrak{S}^{(S)}_{\text{coupled}}$ 视为 $\mathfrak{S}^{(S)}$ 的形变
- **强耦合情形**（$|Q| \sim M$）：纤维间的联络不可忽略，联合谱丛不再是直积而成为真正的"编织"谱丛

**联结曲率**：耦合强度对应的曲率形式 $R^{(s_i,s_j)} = d\omega^{(s_i,s_j)} + \omega \wedge \omega$ 可能提供耦合系统奇异纤维的新分类指标。

### 4.3 可分性条件作为谱丛的平凡化条件

**命题 4.3**（平凡化准则）。多自旋联合谱丛可完全分离（即退化为各单自旋谱丛的直积）当且仅当存在规范变换 $U$ 使得：

$$U^{-1} M_{\text{total}} U = \bigoplus_{i} M^{(s_i)}$$

即耦合项被规范消除。

**物理对应**：
- **Kerr 背景**（$Q=0$）：耦合项为零 → 谱丛平凡化，各自旋独立
- **Kerr-Newman 背景**（$Q \neq 0$）：对 $s=0,\pm\frac12$ 仍可平凡化；对 $s=\pm1,\pm2$ 不可平凡化
- 平凡化失败意味着**耦合奇异纤维**（type IV 奇异纤维）的出现

---

## 5. 可行路径分析

### 5.1 路径 1（近期）：s=±1（电磁）谱丛的参数化和 LACI 验证

**目标**：在现有谱丛框架中建立电磁扰动（s=±1）的独立谱丛。

**步骤**：
1. 实现 $s=+1$ 和 $s=-1$ 的 Teukolsky 递推系数生成（与现有 $s=-2$ LeaverSolver 并行）
2. 在 Leaver 求解器框架中验证电磁 QNM 的计算精度（对照 Berti 表）
3. 计算 $s=\pm1$ 的 LACI 参数 $\gamma$、$\Delta\lambda$ 并与 $s=-2$ 对比
4. 分析电磁自旋的奇异纤维分布（尤其是超辐射区）

**预期困难**：
- $s=-1$ Teukolsky 方程较 $s=-2$ 收敛速度不同，截断参数需重新调优
- 电磁 QNM（光子 sphere modes）的阻尼率较引力 QNM 小，对数值精度要求更高

**预计工作量**：2-3 周

### 5.2 路径 2（中期）：s=±2 与 s=±1 的联合谱丛构造

**目标**：在 Kerr-Newman 背景（小电荷 $|Q| \ll M$）下构造引力-电磁耦合的联合谱丛。

**步骤**：
1. 推导 $s=+2$ 与 $s=+1$ 耦合系统的离散化递推矩阵（分块三对角形式）
2. 建立耦合强度 $Q$ 作为谱丛新参数的纤维延拓
3. 数值扫描 $Q$ 从 $0 \to Q_{\text{max}}$，观察联合谱丛的纤维形变
4. 分类耦合引入的新奇异纤维类型（tentatively: type IV — "耦合融合"）
5. 验证当 $Q \to 0$ 时是否连续退化为直积结构

**预期困难**：
- 耦合递推系统的大小为单自旋的两倍，Leaver 去递归计算量显著增加
- 需要建立耦合系统独有的渐近边界条件（涉及 $\psi_0, \phi_0$ 的双重入/出射条件）
- 耦合参数空间为 4 维（$a, m, \omega, Q$），数值扫描的维度增加

**预计工作量**：2-3 个月

### 5.3 路径 3（远期）：Dirac s=±1/2 的半整数自旋谱丛

**目标**：将谱丛框架推广到半整数自旋，覆盖 Dirac 场。

**背景**：
- Dirac 方程在 Kerr 背景上的分离（Chandrasekhar, 1976; Page, 1976）是已知的
- Kerr-Newman 中 Dirac 方程的可分性也已建立 [沈有根, 物理学报 34, 1203 (1985)]
- 但 Dirac QNM 的谱丛几何从未被系统研究

**核心问题**：
1. Dirac 方程转化为三项递推时的边界条件与整数自旋不同（涉及 Kinnersley 零标架中的旋量系数）
2. 半整数自旋的谱丛单值群是否存在 $2\pi$ 旋转的"自旋结构"（spin structure）？
3. Dirac 谱丛与引力谱丛的**张量积构造**能否形成统一的物质-引力联合谱丛？

**技术挑战**：
- Dirac QNM 的准确计算长期是开放问题（部分模式为"代数特殊"模式，与 Chandrasekhar 变换相关）
- 半整数自旋使谱丛的单值群产生额外的 $\mathbb{Z}_2$ 阻碍

**预计工作量**：6+ 个月

---

## 6. 与 UFPF 现有工作的衔接

### 6.1 Phase 59A 奇异纤维分类的推广

现有奇异纤维分类（`notes/leaver_singular_fibers.md`）的三分法对应单自旋系统：

| 类型 | 当前定义 | 耦合推广 |
|:----|:--------|:--------|
| **I 型**：分支交叉 | 单自旋谱叶交叉 | **推广 I'**：跨自旋分支交叉（不同 $s$ 的特征值交叉） |
| **II 型**：静默边界 | $\det M^{(s)} = 0$ | **推广 II'**：耦合系统的整体静默（$\det M_{\text{total}} = 0$） |
| **III 型**：零谱间隙退化 | $\gamma^{(s)} = 0$ | **推广 III'**：联合谱间隙为零 |
| — | | **新增 IV 型**：耦合融合（耦合强度导致的分块结构退化） |

新类型 IV 的物理对应：当耦合强度 $Q$ 达到某个临界值时，$M^{(s=+2)}$ 和 $M^{(s=+1)}$ 的谱带发生"融合"，产生新的集体模式。这可能对应 Chandrasekhar 变换理论中耦合系统的代数特殊解。

### 6.2 $D_{\mathrm{diss}}$ 函子在多自旋耦合系统的扩展

现有 $D_{\mathrm{diss}}$ 函子（`notes/leaver_diss_embedding.md`）是在单自旋 **Rec**$_{\text{diss}}$ 范畴上定义的。在多自旋耦合系统中：

1. **对象扩展**：从单个 Koopman 算子 $U^{(s)}$ 扩展到耦合系统 Koopman 算子 $U_{\text{total}}$（分块结构）
2. **态射扩展**：不同 $s$ 之间的 Chandrasekhar 变换成为范畴中的新态射
3. **函子的耦合适应性**：
   - 若 $D_{\mathrm{diss}}$ 函子在耦合系统的每个子块上独立保持其性质，则耦合系统可能继承单自旋的伪谱稳定性
   - 否则，耦合可能产生新的耗散结构，需定义 $D_{\mathrm{diss}}^{\text{coupled}}$

**猜想 6.1**（耦合耗散函子）。对 Kerr-Newman 背景（$|Q| < M$），存在耦合系统上的 $D_{\mathrm{diss}}^{\text{(coupled)}}$ 函子，使得谱丛的耗散结构在 $Q$ 的连续形变下保持稳定，退化仅发生在某些临界 $Q_c$ 处。

### 6.3 三重参数谱丛的扩展

当前谱丛是三重参数 $(a,m,\omega)$（`notes/leaver_triple_parameter_sheaf.md`）。耦合系统需要扩展为**四重参数** $(a,m,\omega,Q)$，其中 $Q$ 引入新的纤维维度和新的单值群 $\mathcal{M}_Q$。

四重参数谱丛的群扩张结构：

$$1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \times \mathcal{M}_Q \to 1$$

需要研究 $\mathcal{M}_Q$ 与 $\mathcal{M}_a,\mathcal{M}_m,\mathcal{M}_\omega$ 的换位关系：
- 在 Kerr 极限 $Q \to 0$ 下，$\mathcal{M}_Q$ 应退化
- 在极端电荷 $Q \to M$（极端 Reissner-Nordström 型）附近可能产生新的 III 型奇异

---

## 7. 参考文献

### 已搜索到的 arXiv 文献

1. **Carter, B.** (1968). Global structure of the Kerr family of gravitational fields. *Phys. Rev.* 174, 1559. [DOI: 10.1103/PhysRev.174.1559]
   - 首次证明 Kerr-Newman-de Sitter 中标量场波动方程的可分性

2. **Teukolsky, S. A.** (1973). Perturbations of a rotating black hole. I. Fundamental equations for gravitational, electromagnetic, and neutrino-field perturbations. *Astrophys. J.* 185, 635. [DOI: 10.1086/152444]
   - 建立了任意自旋在 Kerr 背景上的主方程

3. **Chandrasekhar, S.** (1983). *The Mathematical Theory of Black Holes*. Oxford University Press.
   - 标准参考书，包含 $s=\pm2$ 变换理论和 Kerr-Newman 耦合方程的详细推导

4. **Finster, F. & Smoller, J.** (2007). Decay of solutions of the Teukolsky equation for higher spin in the Schwarzschild geometry. [arXiv:gr-qc/0607046]
   - Schwarzschild 中 $s=1,2$ Teukolsky 方程的衰减证明

5. **Dafermos, M., Holzegel, G. & Rodnianski, I.** (2017). Boundedness and decay for the Teukolsky equation on Kerr spacetimes I: the case $|a| \ll M$. [arXiv:1711.07944]
   - 缓慢旋转 Kerr 中 $s=\pm2$ Teukolsky 方程的有界性和多项式衰减

6. **Glampedakis, K., Johnson, A. D. & Kennefick, D.** (2017). The Darboux transformation in black hole perturbation theory. [arXiv:1702.06459]
   - Chandrasekhar 变换作为 Darboux 变换的解释

7. **Berens, R., Gravely, T. & Lupsasca, A.** (2025). Gravitational waves on Kerr black holes I: Reconstruction of linearized metric perturbations. [arXiv:2403.20311]
   - Kerr 线性度规摄动显式重构

8. **Berens, R., Gravely, T. & Lupsasca, A.** (2025). Gravitational waves on Kerr black holes II: Metric reconstruction with cosmological constant. [arXiv:2510.07712]
   - 含宇宙学常数的度规摄动重构

9. **Giorgi, E. & Wan, J.** (2024). Boundedness and decay for the Teukolsky system in Kerr-Newman spacetime II: the case $|a|\ll M$, $|Q|<M$ in axial symmetry. [arXiv:2407.10750]
   - Kerr-Newman Teukolsky 系统在轴对称下的有界性和衰减

10. **Mei, J.** (2025). Fully separated metric perturbations over the Kerr background. [arXiv:2311.18409]
    - 使用 Killing-Yano 张量构造对称算子实现 Kerr 度规摄动的完全分离

11. **Nakajima, H. & Lin, W.** (2021). New Chandrasekhar transformation in Kerr spacetime. [arXiv:2111.05857]
    - 使用不同 tortoise 坐标的新型 Chandrasekhar 变换

12. **沈有根** (1985). Kerr-Newman-De Sitter 时空中的 Dirac 方程的退耦和分离变量. *物理学报* 34, 1203.
    - Dirac 方程在 Kerr-Newman-de Sitter 中的退耦与变量分离

---

## 8. 开放问题清单

### 问题 1：Kerr-Newman 全耦合系统是否存在"隐分离"机制？

Carter 常数来源于 Killing-Yano 张量，在 Kerr-Newman 背景中该张量仍然存在。为何标量场和 Dirac 场可利用这一对称性分离，而电磁/引力扰动不能？是否存在某种"高阶 Killing 张量"可以恢复电磁/引力扰动的完全可分性？

### 问题 2：耦合系统的谱丛是否具有"交叉同谱性"？

Chandrasekhar 变换证明了 $s=+2$ 和 $s=-2$ 在无耦合下是**同谱**的。当引入耦合后，这种同谱性是否被破坏？或者说，是否存在变换 $\mathcal{T}_{Q}$ 使得耦合系统中 $s=+2$ 和 $s=+1$ 的谱通过某种参数变换相关联？

### 问题 3：$D_{\mathrm{diss}}$ 函子是否能延拓到耦合谱丛？

在单自旋情形中，$D_{\mathrm{diss}}$ 函子保证了伪谱在阻尼条件下的稳定性。耦合系统的 Koopman 算子 $U_{\text{total}}$ 是否仍然满足压缩性条件？若满足，是否有新的伪谱结构（如"耦合诱导的非正规性"）出现？

### 问题 4：耦合谱丛的奇异纤维分类是否能产生新的拓扑不变量？

新增的 IV 型奇异纤维（耦合融合）可能给出的"耦合交叉数"是否构成耦合系统的拓扑不变量？它与 Chandrasekhar 变换的代数特殊解是否有对应关系？

### 问题 5：四重参数 $(a,m,\omega,Q)$ 谱丛的单值群结构如何？

单值群 $\mathcal{M}_Q$ 与 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 的换位关系尚未被研究。在 $Q \to 0$ 的极限下，四重单值群应退化到三重结构。这种退化是否保持群扩张的交换关系？

---

## 附录：多耦合谱丛研究路线图（示意）

| 时间 | 路径 | 产出 | 依赖 |
|:---|:----|:----|:----|
| 近期（~3 周） | 路径 1 | $s=\pm1$ 独立谱丛，LACI 参数计算 | Phase 52 代码框架 |
| 中期（~3 月） | 路径 2 | 耦合递推矩阵，$Q$ 谱丛延拓，IV 型奇异纤维 | 路径 1 完成 |
| 远期（~6 月） | 路径 3 | Dirac 谱丛，半整数自旋单值群 | 路径 2 + Phase 54D |
| 交叉 | 理论 | $D_{\mathrm{diss}}^{\text{coupled}}$，$\mathcal{M}_Q$ 群结构，平凡化条件 | 各路径反馈 |
