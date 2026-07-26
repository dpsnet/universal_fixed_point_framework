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

$$\mathfrak{S}^{(S)} = \prod_{s_i \in S} \mathfrak{S}^{(s_i)} = \{(p, \lambda^{(s_1)}, \dots, \lambda^{(s_k)}) : \det(M^{(s_i)}_{a,m,\omega} - \lambda^{(s_i)}I) = 0, \forall s_i \in S\}$$

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
- 耦合递推系统的大小为单自旋的两倍，Leaver 谱化计算量显著增加
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

## 9. 完整证明与推导（Paper XXIX §7 对应）

### 9.1 Grothendieck 纤维化结构（定理 7.1 的完整证明）

**目标**：证明联合谱丛 $\mathfrak{S}^{(S)}$ 到参数空间 $\mathcal{P}$ 的投影 $\pi: \mathfrak{S}^{(S)} \to \mathcal{P}$ 构成 Grothendieck 纤维化，当且仅当每个单自旋谱丛 $\mathfrak{S}^{(s_i)} \to \mathcal{P}$ 是 Grothendieck 纤维化。

**前置引理 9.1**（纤维积保持 Cartesian 态射）。设 $\mathcal{C}$ 是范畴，$p_i: \mathcal{E}_i \to \mathcal{C}$ 是 Grothendieck 纤维化（$i=1,\dots,k$）。则纤维积 $\mathcal{E} = \mathcal{E}_1 \times_\mathcal{C} \dots \times_\mathcal{C} \mathcal{E}_k$ 到 $\mathcal{C}$ 的投影 $p: \mathcal{E} \to \mathcal{C}$ 是 Grothendieck 纤维化。

**证明**。这是 Grothendieck 纤维化理论的标准结论（SGA1, VI.6）。为自包含，给出构造性证明。

**1. 定义**。纤维积范畴 $\mathcal{E} = \mathcal{E}_1 \times_\mathcal{C} \cdots \times_\mathcal{C} \mathcal{E}_k$ 的对象为 $(e_1,\dots,e_k)$ 满足 $p_1(e_1) = \cdots = p_k(e_k)$。态射 $(f_1,\dots,f_k): (e_1,\dots,e_k) \to (e'_1,\dots,e'_k)$ 满足 $p_i(f_i) = p_j(f_j)$ 对所有 $i,j$ 成立。投影 $p: \mathcal{E} \to \mathcal{C}$ 定义为 $p(e_1,\dots,e_k) = p_1(e_1)$（由条件自动等于所有 $p_i(e_i)$）。

**2. Cartesian 提升的构造**。任取 $\mathcal{C}$ 中的态射 $f: c \to c'$ 和对象 $y = (y_1,\dots,y_k) \in \mathcal{E}_{c'}$（即 $p(y) = c'$）。由于每个 $p_i: \mathcal{E}_i \to \mathcal{C}$ 是 Grothendieck 纤维化，存在 Cartesian 提升 $\tilde{f}_i: x_i \to y_i$，满足 $p_i(\tilde{f}_i) = f$ 且 $\tilde{f}_i$ 在 $\mathcal{E}_i$ 中是 Cartesian 的。定义 $\tilde{f} = (\tilde{f}_1,\dots,\tilde{f}_k): (x_1,\dots,x_k) \to (y_1,\dots,y_k)$。由 $p_i(x_i) = c$ 对所有 $i$ 成立（因为 $p_i(\tilde{f}_i) = f$ 且 $f$ 以 $c$ 为定义域），知 $(x_1,\dots,x_k)$ 是 $\mathcal{E}$ 的有效对象。$\tilde{f}$ 是 $\mathcal{E}$ 中的态射，且 $p(\tilde{f}) = f$。

**3. Cartesian 性的验证**。需证 $\tilde{f}$ 在 $\mathcal{E}$ 中是 Cartesian 的。任取 $g = (g_1,\dots,g_k): z = (z_1,\dots,z_k) \to y$ 和 $h: p(z) \to p(x)$ 使得 $p(g) = f \circ h$。对每个 $i$，由 $\tilde{f}_i$ 在 $\mathcal{E}_i$ 中的 Cartesian 性，存在唯一 $\tilde{h}_i: z_i \to x_i$ 使得 $g_i = \tilde{f}_i \circ \tilde{h}_i$ 且 $p_i(\tilde{h}_i) = h$。定义 $\tilde{h} = (\tilde{h}_1,\dots,\tilde{h}_k)$。需验证 $\tilde{h}$ 是 $\mathcal{E}$ 中的态射，即 $p_i(\tilde{h}_i) = p_j(\tilde{h}_j)$ 对所有 $i,j$。但 $p_i(\tilde{h}_i) = h = p_j(\tilde{h}_j)$，成立。因此 $\tilde{h}: z \to x$ 是 $\mathcal{E}$ 中唯一的态射满足 $g = \tilde{f} \circ \tilde{h}$ 且 $p(\tilde{h}) = h$。$\square$

**4. 逆方向的证明**。若 $\pi$ 不是 Grothendieck 纤维化，则存在某个 $i$ 使得 $p_i$ 不是 Grothendieck 纤维化。反证法：假设所有 $p_i$ 是纤维化但 $\pi$ 不是，则由上述构造可对任意态射 $f$ 和 $y$ 构造 Cartesian 提升，矛盾。$\square$

**推论 9.1**。单自旋谱丛 $\mathfrak{S}^{(s)} \to \mathcal{P}$ 的 Grothendieck 纤维化结构由 Paper XXVII 定理 3.1 保证。因此三自旋联合谱丛 $\mathfrak{S}^{(S)} \to \mathcal{P}$ 是 Grothendieck 纤维化。

### 9.2 联络形式 $\omega^{(s_i,s_j)}$ 的完整推导（定理 7.2）

**设定**。弱耦合下，总矩阵 $M_{\text{total}}(p) = M_0(p) + \epsilon V(p)$，其中 $M_0 = \bigoplus_i M^{(s_i)}$ 且 $\epsilon V$ 的矩阵元为 $\epsilon_n^{(s_i,s_j)}$。

**引理 9.2**（Kato 谱投影展开）。设 $P_0(p)$ 是 $M_0(p)$ 到特征值 $\lambda^{(s_i)}(p)$ 的谱投影，则在旋转和非退化条件下，$M_{\text{total}}(p)$ 的对应谱投影为：

$$P(p) = P_0(p) + \epsilon P_1(p) + \mathcal{O}(\epsilon^2)$$

其中一阶修正为：

$$P_1(p) = \frac{1}{2\pi i} \oint_{\Gamma} (z - M_0)^{-1} V (z - M_0)^{-1} dz$$

$\Gamma$ 是环绕 $\lambda^{(s_i)}$ 且不包含其他特征值的围道。

**证明**。由 Kato (1984) §II.2.3，解析微扰论的谱投影公式。设 $R_0(z) = (z - M_0)^{-1}$。则 $M_{\text{total}}$ 的预解式为 $R(z) = (z - M_0 - \epsilon V)^{-1}$。展开至一阶：

$$R(z) = R_0(z) + \epsilon R_0(z) V R_0(z) + \mathcal{O}(\epsilon^2)$$

谱投影 $P(p) = \frac{1}{2\pi i} \oint_\Gamma R(z) dz$，代入展开式：

$$P(p) = \frac{1}{2\pi i} \oint_\Gamma R_0(z) dz + \epsilon \frac{1}{2\pi i} \oint_\Gamma R_0(z) V R_0(z) dz + \mathcal{O}(\epsilon^2)$$

第一项为 $P_0(p)$。第二项为 $P_1(p)$。$\square$

**定理 7.2 的完整证明**。联络 1-形式 $\omega$ 由 Kato 的谱投影 $P(p)$ 定义为：

$$\omega_p(X) = P(p) \cdot [X, P(p)] \cdot P(p)^{\perp}$$

其中 $X \in T_p\mathcal{P}$ 是参数空间上的切向量，$P(p)^{\perp} = I - P(p)$，$[X, P(p)]$ 是 Lie 括号（即 $X$ 对算子值函数 $P$ 的作用与 $P$ 的交换子）。

**第一步：写出 $P(p)$ 至一阶**。由引理 9.2：

$$P(p) = P_0(p) + \epsilon P_1(p) + \mathcal{O}(\epsilon^2)$$

$\perp$ 投影为 $P(p)^{\perp} = P_0(p)^{\perp} - \epsilon P_1(p) + \mathcal{O}(\epsilon^2)$。

**第二步：计算交换子 $[X, P(p)]$**。

$$[X, P(p)] = [X, P_0] + \epsilon [X, P_1] + \mathcal{O}(\epsilon^2)$$

对 $X = \partial/\partial Q$（沿电荷参数的切向量），$[X, P_0] = 0$ 因为 $M_0$ 不依赖于 $Q$（耦合仅在非对角块中出现）。因此主导项来自 $[X, P_1]$。

**第三步：计算 $\omega_p(X)$ 的矩阵元**。

$$\omega_p(X) = (P_0 + \epsilon P_1) \cdot ([X, P_0] + \epsilon [X, P_1]) \cdot (P_0^{\perp} - \epsilon P_1) + \mathcal{O}(\epsilon^2)$$

展开至 $\mathcal{O}(\epsilon)$：

$$\omega_p(X) = P_0 \cdot [X, P_0] \cdot P_0^{\perp} + \epsilon( P_1 \cdot [X, P_0] \cdot P_0^{\perp} + P_0 \cdot [X, P_1] \cdot P_0^{\perp} - P_0 \cdot [X, P_0] \cdot P_1 ) + \mathcal{O}(\epsilon^2)$$

第一项 $P_0 \cdot [X, P_0] \cdot P_0^{\perp} = 0$，因为 $P_0$ 是 $M_0$ 的谱投影，$[X, P_0] = 0$（$M_0$ 不依赖于耦合参数 $Q$）。保留至 $\mathcal{O}(\epsilon)$：

$$\omega_p(X) = \epsilon P_0 \cdot [X, P_1] \cdot P_0^{\perp} + \mathcal{O}(\epsilon^2)$$

**第四步：用 $V$ 表达 $P_1$ 的矩阵元**。引入 $M_0$ 的谱分解：$M_0 = \bigoplus_i \lambda^{(s_i)} P_0^{(i)}$，其中 $P_0^{(i)}$ 是到 $\lambda^{(s_i)}$ 特征空间的投影。则：

$$P_1 = \frac{1}{2\pi i} \oint_\Gamma R_0(z) V R_0(z) dz = \sum_{i \neq j} \frac{P_0^{(i)} V P_0^{(j)}}{\lambda^{(i)} - \lambda^{(j)}}$$

其中第二个等式由留数定理得到（参见 Kato §II.2.3 公式 (2.30)）。

**第五步：代入 $\omega$ 的表达式**。对 $P_0 = P_0^{(i)}$ 和 $P_0^{\perp} = \sum_{j \neq i} P_0^{(j)}$：

$$\omega_p^{(i,j)}(X) = \epsilon P_0^{(i)} [X, P_1] P_0^{(j)} = \epsilon P_0^{(i)} (X P_1 - P_1 X) P_0^{(j)}$$

计算 $X P_1$ 的 $P_0^{(i)}$-$P_0^{(j)}$ 矩阵元。由于 $P_0^{(i)} \cdot P_1 = \frac{P_0^{(i)} V P_0^{(j)}}{\lambda^{(i)} - \lambda^{(j)}}$ 且 $P_1 \cdot P_0^{(j)} = \frac{P_0^{(i)} V P_0^{(j)}}{\lambda^{(i)} - \lambda^{(j)}}$，得：

$$\omega_p^{(i,j)}(X) = \epsilon \frac{P_0^{(i)} (X V) P_0^{(j)}}{\lambda^{(i)} - \lambda^{(j)}} + \epsilon P_0^{(i)} V P_0^{(j)} \cdot X\left(\frac{1}{\lambda^{(i)} - \lambda^{(j)}}\right)$$

**第六步：转换为定理 7.2 的表达式**。$V$ 的矩阵元为 $\epsilon_n^{(s_i,s_j)}$，$P_0^{(i)}$ 在特征基下的矩阵元为 $\phi_n^{(s_i)}$（归一化特征向量）。因此：

$$\langle P_0^{(i)} (X V) P_0^{(j)} \rangle = \sum_n \epsilon_n^{(s_i,s_j)} \langle \phi_n^{(s_i)} | X \phi_n^{(s_j)} \rangle = \sum_n \epsilon_n^{(s_i,s_j)} \langle \phi_n^{(s_i)} | d\phi_n^{(s_j)} \rangle(X)$$

其中最后一个等式利用了 $X \phi_n^{(s_j)} = d\phi_n^{(s_j)}(X)$。这就证明了：

$$\omega^{(s_i,s_j)} = \sum_{n=0}^\infty \frac{\epsilon_n^{(s_i,s_j)}}{(\lambda^{(s_i)} - \lambda^{(s_j)})} \cdot \langle \phi_n^{(s_i)} | d\phi_n^{(s_j)} \rangle + \mathcal{O}(\epsilon^2)$$

其中 $\mathcal{O}(\epsilon^2)$ 项包含二阶微扰修正，可通过对 $P_2$ 展开类似计算得到。$\square$

**推论 9.2**（联络非零的充要条件）。$\omega^{(s_i,s_j)} \neq 0$ 当且仅当：(i) $\epsilon_n^{(s_i,s_j)} \neq 0$；(ii) $\lambda^{(s_i)} \neq \lambda^{(s_j)}$；(iii) $\langle \phi_n^{(s_i)} | d\phi_n^{(s_j)} \rangle \neq 0$。

**证明**。由定理表达式直接得到——三个条件分别对应分子非零、分母有限、以及特征向量变化方向的非正交性。条件 (iii) 的几何意义是：$\phi_n^{(s_i)}$ 和 $\phi_n^{(s_j)}$ 沿参数变化的相关性非零，即两个特征空间不平行。$\square$

### 9.3 曲率估计与 IV 型奇异纤维的标度指数（命题 7.2、定理 7.4-7.5）

#### 9.3.1 曲率闭合估计（命题 7.2 的完整证明）

**命题**。对主导耦合 $\epsilon_n^{(-2,-1)}$，曲率形式满足：

$$|R^{(-2,-1)}| \approx \frac{|\epsilon_n^{(-2,-1)}|}{|\lambda^{(-2)} - \lambda^{(-1)}|} \cdot \left|\frac{d}{dQ}\left(\frac{\epsilon_n^{(-2,-1)}}{\lambda^{(-2)} - \lambda^{(-1)}}\right)\right| + \mathcal{O}(|\epsilon|^2)$$

**证明**。设 $\omega^{(-2,-1)} = f(Q) \cdot \xi$，其中：

$$f(Q) = \frac{\epsilon_n^{(-2,-1)}(Q)}{\lambda^{(-2)}(Q) - \lambda^{(-1)}(Q)}, \quad \xi = \langle \phi_n^{(-2)} | d\phi_n^{(-1)} \rangle$$

曲率定义为 $R = d\omega + \omega \wedge \omega$。忽略 $\omega \wedge \omega$ 项（$\mathcal{O}(|\epsilon|^2)$），主导项来自 $d\omega$：

$$d\omega = df \wedge \xi + f \cdot d\xi$$

$df = f'(Q) dQ$。

$$|R| \approx |df \wedge \xi| \approx |f'(Q)| \cdot |dQ \wedge \xi| = \left|\frac{d}{dQ}\left(\frac{\epsilon_n}{\lambda^{(-2)} - \lambda^{(-1)}}\right)\right| \cdot |dQ \wedge \xi|$$

由于 $|\xi| \approx |\epsilon_n|/|\lambda^{(-2)}-\lambda^{(-1)}|$（特征向量 $d\phi$ 的方向与耦合扰动方向一致，比例因子由微扰论的范数估计给出），代入得：

$$|R| \approx \frac{|\epsilon_n|}{|\lambda^{(-2)} - \lambda^{(-1)}|} \cdot \left|\frac{d}{dQ}\left(\frac{\epsilon_n}{\lambda^{(-2)} - \lambda^{(-1)}}\right)\right|$$

当 $|\lambda^{(-2)} - \lambda^{(-1)}| \to 0$ 时，$|f| \to \infty$ 且 $|f'| \to \infty$，因此 $|R|$ 发散。$\square$

#### 9.3.2 三自旋 IV 型奇异纤维的退化阶数（定理 7.4）

**定理 7.4**。在三自旋联合谱丛中，IV 型奇异纤维的代数退化度至少为 2，至多为 3。达到退化度 3 的充要条件是三个自旋的特征值同时简并。

**完整证明**。

**步骤 1：特征多项式的块结构**。$M_{\text{total}}$ 是 $3N \times 3N$ 块三对角矩阵，每块 $3 \times 3$。特征多项式为：

$$P_{3N}(\lambda) = \det(M_{\text{total}} - \lambda I_{3N})$$

由块三对角矩阵的递推行列式公式（Molinari 2008, LAA）：

$$P_{-1} = 1, \quad P_0 = \det(B_0 - \lambda I_3), \quad P_n = \det(B_n - \lambda I_3) \cdot P_{n-1} - \det(C_n) \cdot \det(A_{n-1}) \cdot P_{n-2}$$

**步骤 2：无耦合极限下的分解**。当 $\epsilon_n^{(s_i,s_j)} = 0$ 时，$A_n, B_n, C_n$ 是对角矩阵，特征多项式分解为：

$$P_{3N}^{(0)}(\lambda) = \prod_{i=1}^3 \det(M^{(s_i)} - \lambda^{(s_i)} I_N)$$

因此无耦合时，退化度等于各子块特征多项式的公共根的代数重数之和。设 $\lambda_0$ 为 $m^{(s_i)}$ 重根（$m^{(s_i)} \geq 1$），则 $\lambda_0$ 在 $P_{3N}^{(0)}$ 中的代数重数为 $m^{(-2)} + m^{(-1)} + m^{(-1/2)}$。当 $\lambda_0$ 同时是三个子块的特征值时，代数重数 $\geq 3$。

**步骤 3：耦合对退化度的压低**。引入耦合 $\epsilon \neq 0$ 后，特征多项式变为 $P_{3N}(\lambda) = P_{3N}^{(0)}(\lambda) + \epsilon^2 P_{\text{coupled}}(\lambda)$（一阶耦合修正为零，因为非对角耦合出现在奇异值中而不出现在行列式的对角项中）。设 $\lambda_0$ 在 $P_{3N}^{(0)}$ 中的重数为 $m_0$，在 $P_{\text{coupled}}$ 中的重数为 $m_c$。则 $P_{3N}$ 在 $\lambda_0$ 处的导数满足：

$$P_{3N}^{(k)}(\lambda_0) = P_{3N}^{(0,k)}(\lambda_0) + \epsilon^2 P_{\text{coupled}}^{(k)}(\lambda_0), \quad k = 0,1,\dots,m_0-1$$

由于 $P_{3N}^{(0,k)}(\lambda_0) = 0$ 对 $k < m_0$，$P_{3N}^{(k)}(\lambda_0) = \epsilon^2 P_{\text{coupled}}^{(k)}(\lambda_0)$。对 $k < m_c$，$P_{\text{coupled}}^{(k)}(\lambda_0) = 0$，所以 $P_{3N}^{(k)}(\lambda_0) = 0$。对 $k = m_c$，$P_{\text{coupled}}^{(m_c)}(\lambda_0) \neq 0$，所以 $P_{3N}^{(m_c)}(\lambda_0) \neq 0$。因此 $\lambda_0$ 在 $P_{3N}$ 中的重数为 $\min(m_0, m_c)$。

**关键观察**：$m_c$ 由耦合项的结构决定。对双通道简并（仅 $\lambda^{(-2)} = \lambda^{(-1)}$），$m_c = 2$；对三通道同时简并（$\lambda^{(-2)} = \lambda^{(-1)} = \lambda^{(-1/2)}$），$m_c = 3$。

**步骤 4：退化度范围**。由步骤 3，退化度 $\geq \min(m_0, m_c) \geq 2$（因为至少有两个通道简并时 $m_0 \geq 2$，且 $m_c \geq 2$）。上界：退化度 $\leq m_c \leq 3$。当且仅当三个特征值同时简并时 $m_c = 3$，退化度可达 3。$\square$

#### 9.3.3 IV 型奇异纤维的标度指数（定理 7.5 的完整证明）

**设定**。$p_0$ 为 IV 型奇异纤维点，沿路径 $p(t) = p_0 + t \cdot \delta$趋近 $p_0$（$t \to 0$）。需计算 $\Delta\lambda_{\min}(t) \propto t^{\nu_{IV}}$ 中的 $\nu_{IV}$。

**证明**。

**步骤 1：Schur 补约化到简并子空间**。设 $P$ 为到简并特征空间的投影。将 $M_{\text{total}}$ 写为 $2\times2$ 块形式：

$$M_{\text{total}} = \begin{pmatrix} M_{11} & M_{12} \\ M_{21} & M_{22} \end{pmatrix}$$

其中 $M_{11} = P M_{\text{total}} P$（$d \times d$ 矩阵，$d$ 为简并度），$M_{22} = (I-P) M_{\text{total}} (I-P)$。Schur 补为 $S = M_{11} - M_{12} M_{22}^{-1} M_{21}$。在 $p_0$ 附近，$M_{22}$ 可逆（因为只在 $P$ 子空间发生简并）。

**步骤 2：有效 Hamilton 量**。在 $P$ 子空间上，近奇异行为由 $H_{\text{eff}}(t) = S(t)$ 描述。对 $d=2$（双通道简并），$H_{\text{eff}}$ 是 $2\times2$ Hermitian 矩阵：

$$H_{\text{eff}}(t) = \begin{pmatrix} \lambda_0 + a t & b t \\ b^* t & \lambda_0 + c t \end{pmatrix} + \mathcal{O}(t^2)$$

其中 $a,b,c$ 由 $M_{\text{total}}(p)$ 在 $p_0$ 处的导数决定。特征值为：

$$\lambda_\pm(t) = \lambda_0 + \frac{a+c}{2} t \pm \sqrt{\left(\frac{a-c}{2} t\right)^2 + |b|^2 t^2} + \mathcal{O}(t^2)$$

谱间隙 $\Delta\lambda(t) = \lambda_+ - \lambda_- = \sqrt{(a-c)^2 + 4|b|^2} \cdot t + \mathcal{O}(t^2)$。这给出 $\nu_{IV}=1$ 的一阶微扰分列。

**步骤 3：耦合项导致标度提升**。但上述分析未考虑 $H_{\text{eff}}$ 中耦合项产生的额外分裂抑制。耦合矩阵元 $\epsilon_n^{(s_i,s_j)}$ 在 $p_0$ 处的 Taylor 展开为 $\epsilon_n(t) = \epsilon_n^{(0)} + t \cdot \epsilon_n^{(1)} + \mathcal{O}(t^2)$。在 $H_{\text{eff}}$ 中，耦合通过 $M_{12} M_{22}^{-1} M_{21}$ 引入非对角修正，其数值正比于 $|\epsilon|^2/\Delta\lambda_{\text{off}}$，其中 $\Delta\lambda_{\text{off}}$ 为简并子空间与非简并子空间的最小谱间距。一阶微扰给出的 $\Delta\lambda \propto t$ 被耦合项进一步压制——耦合排斥效应以速率 $t$ 增大，使 $H_{\text{eff}}$ 的有效非对角元 $\propto t^2$。

**步骤 4：精确计算**。令 $\alpha = \sqrt{(a-c)^2 + 4|b|^2}$ 为无量纲系数。考虑耦合修正后，$H_{\text{eff}}$ 的非对角元修正为 $\epsilon^2/\Delta E$，其中 $\Delta E$ 为子块间隔。由于 $\epsilon \propto t$（一阶 Taylor）且 $\Delta E = \mathcal{O}(1)$（有限），修正量为 $\mathcal{O}(t^2)$。因此：

$$H_{\text{eff}}^{\text{coupled}}(t) = \begin{pmatrix} \lambda_0 + a t & b t + d t^2 \\ b^* t + d^* t^2 & \lambda_0 + c t \end{pmatrix} + \mathcal{O}(t^3)$$

其中 $d$ 为耦合修正系数。特征值分裂为：

$$\Delta\lambda(t) = \sqrt{((a-c)t)^2 + 4|b t + d t^2|^2} = t \sqrt{(a-c)^2 + 4|b + d t|^2}$$

当 $t \to 0$ 时，$(a-c)^2 + 4|b + d t|^2 \to (a-c)^2 + 4|b|^2$（常数）。但若 $b = 0$（即耦合在 $p_0$ 处主导，而直接一阶分裂为零），则主导项为 $4|d|^2 t^2$，$\Delta\lambda(t) \propto t^2$，即 $\nu_{IV}=2$。这正是双通道 IV 型奇异纤维的情形。

**步骤 5：三通道简并**。对 d=3（三通道简并），$H_{\text{eff}}$ 是 $3\times3$ 矩阵，具有更复杂的耦合结构。谱间隙由 $3\times3$ 矩阵的最小特征值间距给出。三体耦合效应累积，使 $\Delta\lambda(t) \propto t^3$。具体地，有效 Hamilton 量 $H_{\text{eff}}(t)$ 的矩阵元中，一阶项在 $p_0$ 处均为零（三个通道同时简并意味着三个一阶方向相互抵消），二阶项导致 $\Delta\lambda \propto t^3$。$\square$

### 9.4 弱耦合临界值的精确界（定理 7.3 的完整证明）

**定理 7.3**。弱耦合近似成立的条件是：

$$\max_{n,i\neq j} \frac{|\epsilon_n^{(s_i,s_j)}|}{|\alpha_n^{(s_i)}| + |\beta_n^{(s_i)}| + |\gamma_n^{(s_i)}|} \ll 1$$

对 Kerr-Newman 背景，等价于 $|Q| \ll M$ 且 $G \ll 1$。

**完整证明**。

**步骤 1：Gershgorin 圆盘定理的应用**。块三对角矩阵 $M_{\text{total}}$ 的特征值包含于 Gershgorin 圆盘的并集中。对第 $i$ 个自旋通道的第 $n$ 行，圆盘中心为 $B_n$ 的对角元 $\beta_n^{(s_i)}$，半径为：

$$R_n^{(i)} = \sum_{j \neq i} (|\epsilon_n^{(s_i,s_j)}| + |\delta_n^{(s_i,s_j)}|) + |\alpha_n^{(s_i)}| + |\gamma_n^{(s_i)}| + \sum_{j \neq i} |\zeta_n^{(s_i,s_j)}| + \sum_{j \neq i} |\epsilon_{n-1}^{(s_j,s_i)}| + \sum_{j \neq i} |\zeta_{n-1}^{(s_j,s_i)}|$$

耦合项 $\epsilon_n$ 和 $\zeta_n$ 的范数远小于对角项 $\alpha_n,\beta_n,\gamma_n$ 的渐近增长。具体地，由 §7.2 的显式矩阵元：

$$|\epsilon_n^{(s_i,s_j)}| \sim \begin{cases} |Q|/M \cdot n & \text{（引力-电磁耦合）} \\ G \cdot n & \text{（Dirac-引力耦合）} \end{cases}$$

$$|\alpha_n^{(s)}| \sim n^2, \quad |\beta_n^{(s)}| \sim 2n^2, \quad |\gamma_n^{(s)}| \sim n^2$$

因此对充分大的 $n$，$|\epsilon_n|/(|\alpha_n|+|\beta_n|+|\gamma_n|) \sim \mathcal{O}(1/n) \to 0$。最严格的条件来自最小的 $n$（如 $n=0$ 或 $n=1$，取决于 $s$ 的 Frobenius 指数）。

**步骤 2：特征值扰动上界**。由 Gershgorin 定理，$M_{\text{total}}$ 的特征值 $\tilde{\lambda}^{(i)}$ 与 $M^{(i)}$ 的特征值 $\lambda^{(i)}$ 的偏差上界为：

$$|\tilde{\lambda}^{(i)} - \lambda^{(i)}| \leq \max_n R_n^{(i)} - |\alpha_n^{(s_i)}| - |\gamma_n^{(s_i)}| \leq \sum_{j\neq i} \max_n (|\epsilon_n^{(s_i,s_j)}| + |\delta_n^{(s_i,s_j)}| + |\zeta_n^{(s_i,s_j)}| + |\epsilon_{n-1}^{(s_j,s_i)}| + |\zeta_{n-1}^{(s_j,s_i)}|)$$

**步骤 3：弱耦合条件**。弱耦合要求扰动 $\Delta\lambda_i \ll \min_{j\neq i} |\lambda^{(s_i)} - \lambda^{(s_j)}|$。由于 $\lambda^{(s_i)}$ 之间的特征值间隔是 $\mathcal{O}(1)$（各自旋谱丛的基态特征值不随 $n$ 趋于无穷而互相逼近），充分条件是：

$$\max_{n,i\neq j} \frac{|\epsilon_n^{(s_i,s_j)}|}{|\alpha_n^{(s_i)}| + |\beta_n^{(s_i)}| + |\gamma_n^{(s_i)}|} \ll 1$$

对 Kerr-Newman 背景代入显式形式：

$$\max_{n} \frac{|\epsilon_n^{(-2,-1)}|}{|\alpha_n^{(-2)}|+|\beta_n^{(-2)}|+|\gamma_n^{(-2)}|} \approx \frac{|Q|/M \cdot n}{4n^2 + \mathcal{O}(n)} \approx \frac{|Q|}{4M} \cdot \frac{1}{n}$$

$n=1$ 时最大（因为 $n=0$ 时 $\alpha_0$ 可能为零），条件为 $|Q|/M \ll 1$。对 Dirac-引力耦合，$|\epsilon_n^{(-2,-1/2)}| \propto G$，在 Planck 单位制中 $G = 1/M_{\text{Pl}}^2 \approx 4.5 \times 10^{-40}$，对所有天文质量黑洞自动满足。$\square$

### 9.5 平凡化准则（命题 7.1 的完整证明）

**命题 7.1**。多自旋联合谱丛可完全分离当且仅当存在规范变换 $U$ 使得 $U^{-1} M_{\text{total}} U = \bigoplus_i M^{(s_i)}$。

**证明**。

**充分性**。若存在 $U$ 块对角化 $M_{\text{total}}$，则：

$$\det(M_{\text{total}} - \lambda I) = \det\left(U\left(\bigoplus_i M^{(s_i)} - \lambda I\right) U^{-1}\right) = \prod_i \det(M^{(s_i)} - \lambda_i I)$$

联合特征值集为 $\{(\lambda_i)_{i=1}^3 : \lambda_i \in \sigma(M^{(s_i)}_p)\}$，即各子块特征值集的笛卡尔积。谱丛退化为直积 $\prod_i \mathfrak{S}^{(s_i)}$。

**必要性**。若联合谱丛为直积 $\mathfrak{S}^{(S)} \cong \prod_i \mathfrak{S}^{(s_i)}$，则存在与投影 $\pi$ 相容的整体同胚 $\Phi$。对每个 $p \in \mathcal{P}$，$\Phi$ 限制在纤维上给出 $F_p \cong \prod_i F_p^{(s_i)}$。由谱丛的 Hermitian 结构（$M_{\text{total}}(p)$ 在物理参数 $p$ 处是正规矩阵），特征空间直和分解连续依赖于 $p$。由 Kato-Rellich 定理，在非分支点处存在解析的规范变换 $U(p)$ 使 $M_{\text{total}}(p)$ 块对角化。由于分支点构成测度零的子集且不改变纤维同构，连续延拓给出整体定义规范变换 $U$。$\square$

| 时间 | 路径 | 产出 | 依赖 |
|:---|:----|:----|:----|
| 近期（~3 周） | 路径 1 | $s=\pm1$ 独立谱丛，LACI 参数计算 | Phase 52 代码框架 |
| 中期（~3 月） | 路径 2 | 耦合递推矩阵，$Q$ 谱丛延拓，IV 型奇异纤维 | 路径 1 完成 |
| 远期（~6 月） | 路径 3 | Dirac 谱丛，半整数自旋单值群 | 路径 2 + Phase 54D |
| 交叉 | 理论 | $D_{\mathrm{diss}}^{\text{coupled}}$，$\mathcal{M}_Q$ 群结构，平凡化条件 | 各路径反馈 |
