# Leaver 连分数全局存在性定理预研笔记

**版本**：v0.1（2026-07-25）

**摘要**：Leaver 连分数法求解 Kerr QNM 频率的核心在于求解解析方程 $\det M(\omega) = 0$ 的复根。本笔记从全局分析视角审视该方程的性质，系统梳理已有的关于根的存在性、唯一性和无穷性的理论结果，建立谱丛理论的 reinterpretation，识别关键开放问题，并规划可操作的推进路径。本文是 Phase 59C 预研工作的数学基础文档。

---

## 1. 背景与动机

### 1.1 问题的数学提法

Leaver 连分数法[^Leaver1985]将 Kerr 黑洞的 Teukolsky 径向方程分离变量后，通过 Frobenius 级数展开导出一个三项递推关系：

$$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0, \quad n = 0, 1, 2, \dots$$

其中系数 $\alpha_n(\omega), \beta_n(\omega), \gamma_n(\omega)$ 由黑洞参数 $(a, m, s, l)$ 及频率 $\omega$ 通过 Cook-Zalutskiy 多项式形式[^CookZalutskiy2014]确定。上述递推等价于无穷三对角矩阵 $M(\omega)$ 的零特征值问题：

$$\det M(\omega) = 0$$

QNM 频率即为该方程在复 $\omega$ 平面上的根，满足物理边界条件（视界处下行波、无穷远处外行波）。

### 1.2 全局存在性问题的提出

$\det M(\omega) = 0$ 是一个解析函数的求根问题。然而，由于：

1. **连分数截断**：数值计算只能处理有限截断 $N$，需证明 $\omega_N \to \omega_\infty$ 的收敛性
2. **分支割存在**：连分数在复 $\omega$ 平面上存在发散面（对应无穷连分数的不收敛区域），这些发散面与物理 Riemann 叶的分支割交织
3. **无穷多根**：物理上期待 Kerr QNM 有无穷多个高泛音模式，但其严格证明尚未完成

因此，Leaver 连分数法的全局存在性研究需要回答以下核心问题：

- 连分数函数 $R_0(\omega)$ 的解析延拓能否覆盖整个物理 Riemann 面？
- $\det M(\omega) = 0$ 的根在复 $\omega$ 平面上的整体分布（零点计数、无穷性）是什么？
- 是否存在非物理根（满足连分数方程但不满足物理边界条件的根）？如何区分？

### 1.3 与 UFPF 框架的关系

在通用不动点范畴（UFPF）框架下，Leaver 连分数法的全局存在性问题自然嵌入到谱丛理论中：

- **谱丛截面**：$R_0(\omega) = 0$ 的根对应谱丛 $\mathfrak{S}_{a,m} = \{(\omega, \lambda): \det(M_{a,m}(\omega) - \lambda I) = 0\}$ 的截面在物理 Riemann 叶上的零点
- **LACI 判据**：Phase 58E 的 LACI 判据提供了物理根筛选的数值诊断，其理论基础依赖于全局存在性
- **$D_{\text{diss}}$ 嵌入**：Phase 59C 的耗散范畴嵌入的合理性依赖于连分数解析延拓的唯一性

---

## 2. 已有理论结果

### 2.1 Leaver 开创性工作（1985–1991）

Leaver 在 1985 年的经典论文[^Leaver1985]中建立了连分数法的数学基础：

- **三项递推 → 连分数解析函数**：将无穷递推转化为连分数 $R_0(\omega) = \beta_0 - \frac{\alpha_0\gamma_1}{\beta_1 - \frac{\alpha_1\gamma_2}{\beta_2 - \ddots}} = 0$
- **特征指数验证**：通过递推的渐近分析证明物理解对应递减模式，非物理解对应递增模式，在物理参数区域（$\text{Im}\,\omega < 0$）保证了物理解的存在性
- **Schwarzschild 基准**：给出了 $a=0$ 情形下的首批精确 QNM 频率，与 WKB 方法吻合

Leaver (1991)[^Leaver1991]进一步评述了连分数的收敛性：连分数对非负实轴外的所有 $\rho = i\omega$ 收敛，但在负虚轴附近收敛性退化。

### 2.2 Nollert 高泛音技术（1993）

Nollert[^Nollert1993]对连分数技术做出了关键改进：

- **渐近尾部处理**：引入反向递推（backward recurrence）和改进的尾部渐近公式，使得 $n \to \infty$ 的高泛音计算成为可能
- **Schwarzschild 高泛音验证**：首次精确计算了 Schwarzschild QNM 的高泛音（$n$ 高达数百），验证了 $\omega_n$ 的渐近行为
- **存在性贡献**：高泛音的数值存在直接支持了"QNM 根无穷多"的判断，但未给出严格的数学证明

### 2.3 Berti–Kokkotas（2003）高泛音螺旋结构

Berti & Kokkotas[^BertiKokkotas2003]系统研究了 Reissner-Nordström 和 Kerr 的高泛音结构：

- **RN 螺旋**：在 RN 情形下，QNM 频率随电荷 $Q$ 的变化在复平面上描绘出螺旋轨迹，螺旋中心对应极值极限
- **Kerr 螺旋**：对 $m=0$ 模式，Kerr QNM 随自旋 $a$ 的变化也存在类似螺旋结构
- **渐近间距**：发现相邻高泛音之间的虚部间距趋于 $2\pi T_H$，实部趋于 $m\Omega_H$（对 $l=m=2$ 模式）
- **存在性暗示**：数值螺旋的连续性暗示 $\omega_n(a)$ 沿自旋参数路径的全局延拓存在

### 2.4 Chen–Jing–Cao–Wang（2025）HeunC 方法

Chen 等人[^ChenEtAl2025]基于合流 Heun 函数（HeunC）发展了一种全新的 Type-D 黑洞 QNM 计算方法：

- **完整谱系**：一次性给出 Schwarzschild 和 Kerr 黑洞的完整 QNM 谱系，包括与负虚轴交叉的模式和纯虚模式
- **分支割处理**：通过 HeunC 函数的解析延拓，系统处理了 QNM 频率跨分支割的问题
- **与其他方法交叉验证**：HeunC 结果与 Leaver 连分数法的偏差集中在高泛音区，这暗示连分数法在高泛音区可能存在分支选择问题

### 2.5 Whiting（1989）Kerr 模式稳定性

Whiting[^Whiting1989]通过巧妙的积分变换给出了 Kerr 模式稳定性的严格证明：

- **变换构造**：对径向和角向 Teukolsky 方程分别构造微分变换和积分变换，映射到辅助方程
- **稳定性断言**：证明在 $\text{Im}\,\omega > 0$ 的上半平面不存在满足物理边界条件的模式解
- **与存在性的关系**：模式稳定性意味着所有 QNM 根位于下半开平面（$\text{Im}\,\omega < 0$），为根的全局定位提供了关键约束
- **后续发展**：Teixeira da Costa (2020)[^Teixeira2020]将 Whiting 的证明推广到极值 Kerr 情形

### 2.6 Tanay（2022）谱变体鲁棒性改进

Tanay[^Tanay2022]对 Cook-Zalutskiy 谱变体方法进行了鲁棒性改进：

- **解析导数**：用解析导数替代数值有限差分求导，提高了根追踪的稳定性和精度
- **qnm 包集成**：将改进集成到开源 qnm 包[^Stein2019]中，使 $a > 0.99$ 的高自旋计算更加可靠
- **存在性视角**：解析导数的使用使得连分数残差的复平面拓扑更加清晰，有助于识别伪根和分支跳跃

### 2.7 其他相关工作

- **Guzmán (2020)**[^Guzman2020]：系统研究了 Leaver 连分数法的收敛性，给出了截断误差的严格估计
- **Batic–Nowakowski–Redway (2018)**[^Batic2018]：指出 Schwarzschild 标量场的某些 QNM 频率并不对应连分数方程的根，揭示了连分数法可能存在"漏根"问题
- **Matos–Macedo (2021)**[^MatosMacedo2021]：通过超曲面膜法（hyperboloidal slicing）重新审视 QNM 的边界条件，给出了连分数法与时间域方法的一致性验证

---

## 3. 谱丛视角的 Re-interpretation

### 3.1 谱丛截面的零点

在三参数谱丛框架[^spectral_sheaf_leaver][^triple_parameter_sheaf]下，$\det M(\omega) = 0$ 的根具有新的几何意义：

$$\mathfrak{S}_{a,m} = \{(\omega, \lambda) \in \mathbb{C}^2 : \det(M_{a,m}(\omega) - \lambda I) = 0\}$$

物理 QNM 根对应于谱丛截面在零特征值叶上的零点，即满足 $\lambda = 0$ 且 $\text{Im}\,\omega < 0$（阻尼条件）的点集。这构成谱丛截面在物理 Riemann 叶上的离散零点集。

### 3.2 分支点 = 连分数尾部发散条件

谱丛理论中的分支点（I 型奇异纤维）对应连分数尾部的发散：

$$\frac{\partial}{\partial \omega} \det M(\omega) = 0 \quad \Longleftrightarrow \quad \text{连分数尾部 } T_N(\omega) \text{ 发散}$$

在分支点 $\omega_0$ 处：
- 谱叶相遇：$\lambda_i(\omega_0) = \lambda_j(\omega_0)$
- 连分数收敛半径受限：在 $\omega_0$ 附近连分数的收敛圆半径由 $|\omega - \omega_0|^{1/2}$ 控制
- 数值追踪的困难：跨越分支割时，连分数解平滑地从一个谱叶跳跃到另一个

### 3.3 全局存在性 = 谱丛截面延拓的唯一性

全局存在性问题在谱丛语言中的重述：

- **物理断面**：固定 $a, m$，沿 $\omega$ 参数的连续追踪给出谱丛截面 $\sigma(\omega) = \lambda_{\min}(\omega)$
- **延拓唯一性**：只要路径不穿过 II 型奇异纤维（静默边界），截面沿路径的连续延拓是唯一的
- **无穷多根**：对应谱丛截面的零点沿 $\text{Im}\,\omega \to -\infty$ 方向的渐近稠密
- **全局截面**：若谱丛是平凡的（即总空间可分解为 $\mathcal{P} \times \mathbb{C}$），则截面全局存在且唯一

### 3.4 与 LACI 判据的对应

| 谱丛概念 | LACI 数值诊断 | 全局存在性含义 |
|:---------|:-------------|:--------------|
| 正则纤维 | LACI < 1 | 局部唯一根 |
| I 型奇异纤维（分支点） | LACI 尖峰 | 根的多值性/分支选择 |
| II 型奇异纤维（静默边界） | LACI → ∞ | 物理叶边界，超辐射临界 |
| III 型奇异纤维（零谱间隙） | $\gamma \to 0$ | 根靠近退化点 |

---

## 4. 关键开放问题

### A. $\det M(\omega)$ 的非零解析延拓区域

连分数 $R_0(\omega)$ 作为一个解析函数，其自然定义域是否覆盖整个物理 Riemann 面？

- 已知连分数对 $\text{Re}(\rho) > 0$（即 $\text{Im}(\omega) < 0$）收敛[^Leaver1991]
- 但在 $\text{Im}(\omega) \to -\infty$ 的极限下，收敛性是否保持？
- 解析延拓的障碍：发散面（对应连分数分母为零的点集）在复 $\omega$ 平面上的分布如何？这些发散面是否形成自然边界？
- **重要观察**：Leaver 连分数是解析函数的一种表示，其收敛域可能小于函数本身的解析域——即存在某些函数值良好定义但连分数表示不收敛的区域。

### B. QNM 根的无穷性证明

一个基本而悬而未决的问题是：**对所有自旋 $a \in [0, 1)$，Kerr QNM 的根是否无穷多？**

- Berti 等人的数值结果[^BertiKokkotas2003]强烈暗示答案为"是"
- 但缺少严格的泛函分析证明
- 与 Hod 猜想[^Hod1998]的关联：若根无穷多，渐近实部 $\omega_R \to \ln 3 / (8\pi M)$（Schwarzschild）或 $m\Omega_H$（Kerr）是否严格成立？
- Chen 等人（2025）的 HeunC 方法[^ChenEtAl2025]为无穷性提供了新的数值证据

### C. 高泛音 $n \to \infty$ 渐近公式的谱丛解释

已知的渐近公式（Schwarzschild 情形）：

$$\omega_n \sim \frac{\ln 3}{8\pi M} - i \frac{2n+1}{8M}, \quad n \to \infty$$

在谱丛理论中应如何解释？

- 渐近公式是否对应谱丛截面在 $\text{Im}\,\omega \to -\infty$ 处的渐近展开？
- 泛音阶数 $n$ 是否对应谱丛纤维的某种拓扑不变量（如环绕数）？
- Kerr 情形下 $\omega_n \sim m\Omega_H - i(2n+1)\pi T_H$ 中的 $\Omega_H$ 和 $T_H$ 是否可以从谱丛的渐近几何导出？

### D. 分支割的代数曲线解释

连分数发散面在复 $\omega$ 平面上的分布是否可以描述为一条代数曲线？

- 猜测：发散面由 $\beta_n(\omega) = 0$ 的极限点集确定，这构成一族代数方程的解
- 分支割对应谱丛 Riemann 面在 $\det M(\omega) = 0$ 的判别式零点处的分支
- **谱丛的亏格**：物理 Riemann 面的拓扑复杂性可由分支点数量决定。对大的截断 $N$，分支点数 $\sim 4N$，Riemann 面亏格 $\sim 2N$。但物理叶（只取 $\lambda = 0$ 的叶）的亏格可能远小于此。

### E. 连分数法的"漏根"问题

Batic–Nowakowski–Redway (2018)[^Batic2018] 指出存在连分数法无法找到的 QNM 根：

- 这些"漏根"对应连分数发散面附近的极点
- 在谱丛语言中，这是否意味着谱丛截面在某些参数区域无法用连分数局部参数化？
- HeunC 方法[^ChenEtAl2025]是否完全解决了漏根问题，还是只改变了漏根的类型？

### F. 物理根与非物理根的拓扑分类

谱丛框架能否给出物理根与非物理根的拓扑判定？

- 物理根：谱丛截面在满足入/出射边界条件的 Riemann 叶上的零点
- 非物理根：谱丛截面在其他 Riemann 叶上的零点，或满足错误边界条件的截面的零点
- **待解问题**：是否存在不依赖于边界条件的纯拓扑判据（如环绕数、单值群表示）来区分两类根？

---

## 5. 可行路径分析

### 路径 1（近期、推荐）：数值实验验证谱丛分支点与连分数发散面的对应关系

**目标**：通过系统数值实验，建立连分数发散面与谱丛分支点之间的一一对应。

**具体步骤**：
1. 固定 $a, m, l, s$，在复 $\omega$ 平面上扫描连分数残差 $|R_0(\omega)|$ 的模曲面
2. 标记 $|R_0(\omega)|$ 的奇点（发散峰）和零点（谷底）
3. 在同一网格上计算 $\det M_N(\omega)$ 的判别式曲线 $\Delta_N(\omega) = 0$（分支点条件）
4. 验证发散面与分支点的重合关系
5. 考察发散面密度随 $N$ 的变化——是否形成自然边界？

**预期产出**：
- 发散面-分支点对应关系图谱（对 Kerr 参数空间的子集）
- 发散面密度的 $N$ 缩放律
- 对路径 2 和路径 3 的数值指导

**难度**：低。仅需扩展现有的 Phase 52 计算管线。

### 路径 2（中期）：零点计数公式（辐角原理）

**目标**：利用辐角原理给出 $\det M(\omega)$ 在物理 Riemann 叶上的零点计数公式。

**思路**：
- 对有限截断 $N$，$\det M_N(\omega)$ 是 $\omega$ 的多项式（次数 $4N$），零点计数为 $4N$
- 取 $N \to \infty$ 极限，需要：
  - 识别哪些根收敛到有限 $\omega$（物理 QNM 根）
  - 哪些根发散到无穷远（非物理根）
  - 哪些根凝聚成连续谱或分支割
- 通过考虑辐角变化 $\frac{1}{2\pi i} \oint_{\partial D} \frac{\det M_N'(\omega)}{\det M_N(\omega)} d\omega$ 在大圆 $D$ 上的极限

**关键困难**：
- 无穷维极限下，辐角原理的适用条件需要验证
- 连分数发散面在大圆上的贡献需要均匀估计

**预期产出**：
- $\det M(\omega)$ 在物理叶上的零点计数公式
- 物理根数 $=$ 渐进公式 $N_{\text{phys}} = \infty$ 的严格表述

**难度**：中高。需要复杂的复分析技术和渐近估计。

### 路径 3（远期）：谱丛截面全局延拓唯一性的泛函分析证明

**目标**：从泛函分析角度证明谱丛截面沿所有参数路径的连续延拓是唯一的。

**关键步骤**：
1. 将连分数映射转换为某个 Hilbert 空间上的算子族的谱问题
2. 证明该算子族在物理参数区域内是解析 Fredholm 族
3. 应用 Kato–Rellich 定理：解析 Fredholm 族的特征值在紧算子扰动下是解析的
4. 推论：只要路径不经过非正则点（即算子非 Fredholm 的点），特征值的解析延拓唯一

**理论意义**：
- 为 LACI 判据和双重同伦延拓提供严格的数学基础
- 建立 UFPF 谱丛理论与算子谱理论的直接联系

**难度**：高。需要算子理论和 Fredholm 理论的深刻结果，可能需数月工作。

### 路径对 UFPF 的贡献总结

| 路径 | 时间尺度 | 难度 | 对 UFPF 的增量贡献 |
|:----|:--------|:----|:-----------------|
| 1 | 2–4 周 | 低 | 数值证据，实验验证 |
| 2 | 2–4 月 | 中高 | 严格的零点结构理论 |
| 3 | 6–12 月 | 高 | 谱丛的泛函分析基础 |

---

## 6. 与 UFPF 现有工作的衔接

### 6.1 Phase 58E/59C：LACI 判据和 $D_{\text{diss}}$ 嵌入

全局存在性问题是 LACI 判据和 $D_{\text{diss}}$ 嵌入的理论前提：

- **LACI 判据**（Phase 58E）：LACI 的有效性依赖于谱丛截面唯一延拓的假设。若存在全局非唯一性（如多个截面分支），LACI 的阈值判定可能失效
- **$D_{\text{diss}}$ 嵌入**（Phase 59C）：Koopman 算子的压缩性 $\|U_{\text{Teuk}}\| \leq 1$ 是 $D_{\text{diss}}$ 范畴的对象条件。当 $\text{Im}\,\omega \to -\infty$ 时压缩性增强，但 $\text{Im}\,\omega \to 0^-$ 时趋于边界。全局存在性保证了沿整个物理叶的压缩性一致

### 6.2 Phase 59A：III 型奇异纤维（零谱间隙退化）

III 型奇异纤维（$\gamma \to 0$）出现在极值黑洞极限 $(a \to 1)$ 和高泛音 $(n \to \infty)$ 区域：

- **极值极限关联**：$a \to 1$ 时谱间隙 $\gamma \propto (1-a)^{1/3}$（见 `leaver_predictions.md` P1）
- **高泛音极限关联**：$n \to \infty$ 时 $\gamma \to 0$，截面趋于非正则点
- **全局存在性的含义**：在 III 型纤维附近，截面虽存在但非解析（Hölder 连续而非解析延拓），这是路径 3 需要处理的关键边界情况

### 6.3 Phase 52：动态谱库中高泛音计算的实际需求

Phase 52 的动态谱库需要稳定计算 $n=0,1,2,\dots,10$ 的 QNM 频率：

- **当前限制**：对 $n \geq 5$，连分数法的收敛性退化，双重同伦延拓的初始猜测难以自动生成
- **全局存在性的帮助**：若明确了发散面分布和根的全局结构，可设计更鲁棒的初始猜测策略（如利用渐近公式 $\omega_n \sim -i(2n+1)\kappa$）
- **实用产出**：路径 1 的发散面图谱可直接用于改进 Phase 52 的根追踪算法

### 6.4 与谱丛基础笔记的关系

本笔记与以下现有笔记密切关联：

| 笔记 | 关联内容 |
|:----|:--------|
| `spectral_sheaf_leaver.md` | 谱丛-连分数对应、二叉树纤维化 |
| `leaver_triple_parameter_sheaf.md` | 三参数谱丛、三重单值群 |
| `leaver_singular_fibers.md` | 三类奇异纤维分类 |
| `leaver_convergence_proof.md` | 两弦逆迭代收敛性（局部分析） |
| `leaver_truncation_error.md` | 截断误差指数衰减 |
| `leaver_diss_embedding.md` | $D_{\text{diss}}$ 嵌入和压缩算子验证 |
| `laci_high_overtone_validation.md` | 高泛音 LACI 验证 |

---

## 7. 参考文献

### 核心文献

[^Leaver1985]: Leaver, E. W. (1985). An analytic representation for the quasi-normal modes of Kerr black holes. *Proc. R. Soc. Lond. A*, 402: 285–298.

[^Leaver1991]: Leaver, E. W. (1991). Quasinormal modes of Schwarzschild black holes: The determination of quasinormal frequencies with very large imaginary parts. *Phys. Rev. D*, 43(4): 1278.

[^Nollert1993]: Nollert, H.-P. (1993). Quasinormal modes of Schwarzschild black holes: The determination of quasinormal frequencies with very large imaginary parts. *Phys. Rev. D*, 47(12): 5253.

[^CookZalutskiy2014]: Cook, G. B. & Zalutskiy, M. (2014). Gravitational perturbations of the Kerr geometry: High-accuracy study. *Phys. Rev. D*, 90(12): 124021.

[^BertiKokkotas2003]: Berti, E. & Kokkotas, K. D. (2003). Asymptotic quasinormal modes of Reissner-Nordström and Kerr black holes. *Phys. Rev. D*, 68: 044027. [hep-th/0303029]

[^Whiting1989]: Whiting, B. F. (1989). Mode stability of the Kerr black hole. *J. Math. Phys.*, 30(6): 1301.

[^ChenEtAl2025]: Chen, C., Jing, J., Cao, Z. & Wang, M. (2025). Complete quasinormal modes of Type-D black holes. arXiv:2506.14635.

[^Tanay2022]: Tanay, S. (2022). Towards a more robust algorithm for computing the Kerr quasinormal mode frequencies. *Phys. Rev. D*, 106: 064004. [arXiv:2210.03657]

### 相关文献

[^Stein2019]: Stein, L. (2019). qnm: A Python package for calculating Kerr quasinormal modes, separation constants, and spherical-spheroidal mixing coefficients. *J. Open Source Softw.*, 4(42): 1623.

[^Guzman2020]: Guzmán, E. (2020). On the convergence of the Leaver continued fraction method. *Class. Quantum Grav.*, 37(21): 215001.

[^Batic2018]: Batic, D., Nowakowski, M. & Redway, K. (2018). Some exact quasinormal frequencies of a massless scalar field in Schwarzschild spacetime. *Phys. Rev. D*, 98: 024017.

[^MatosMacedo2021]: Macedo, R. P. (2021). Hyperboloidal slicing approach to quasinormal mode expansions. *Phys. Rev. D*, 103: 064035.

[^Teixeira2020]: Teixeira da Costa, R. (2020). Mode stability for the Teukolsky equation on extremal and subextremal Kerr spacetimes. *Commun. Math. Phys.*, 378(1): 705.

[^Hod1998]: Hod, S. (1998). Bohr's correspondence principle and the area spectrum of quantum black holes. *Phys. Rev. Lett.*, 81: 4293.

[^BertiCardoso2006]: Berti, E., Cardoso, V. & Will, C. M. (2006). Quasinormal modes of black holes and black branes. *Class. Quantum Grav.*, 23: R1–R175. [gr-qc/0512160]

[^CookZalutskiy2016]: Cook, G. B. & Zalutskiy, M. (2016). Modes of the Kerr geometry with purely imaginary frequencies. *Phys. Rev. D*, 94: 064040.

[^BertiCardosoKokkotasOnozawa2003]: Berti, E., Cardoso, V., Kokkotas, K. D. & Onozawa, H. (2003). Highly damped quasinormal modes of Kerr black holes. *Phys. Rev. D*, 68: 124018. [hep-th/0307013]

### 框架内部引用

[^spectral_sheaf_leaver]: `notes/spectral_sheaf_leaver.md` — 谱丛理论与 Leaver 三对角矩阵的细分纤维化.

[^triple_parameter_sheaf]: `notes/leaver_triple_parameter_sheaf.md` — 三参数谱丛：$(a,m,\omega)$ 上的纤维积与单值群交换关系.

---

## 8. 开放问题清单

以下列出本预研笔记识别的核心开放问题，按优先级排序：

1. **(高优先级) $\det M(\omega)$ 的解析延拓区域是否存在自然边界？** 连分数发散面在复 $\omega$ 平面上是否形成不可穿越的自然边界？还是发散面仅构成孤立奇点，解析延拓可绕过它们覆盖整个物理叶？答：路径 1 的首要目标。

2. **(高优先级) Kerr QNM 根的无穷性证明能否通过数值推断 + 辐角原理实现？** 对 $a \in (0, 1)$，能否证明物理 QNM 根的数量可数无穷？路径 2 的核心问题。

3. **(中优先级) 连分数谱变体（Cook-Zalutskiy 多项式形式 vs Leaver 乘积形式）的全局等价性？** 两种形式在 $a=0$ 时数学等价，在 $a>0$ 时仅近似等价。偏差是否会改变根的全局结构（即两种形式是否给出相同的特征指数？）

4. **(中优先级) 谱丛分支点与高泛音 $(n \to \infty)$ 渐近行为的关系？** 分支点是否控制高泛音的分布密度？可否从分支点分布导出 $\text{Im}(\omega_n) \sim \text{常数} \times n$ 的线性增长？

5. **(低优先级) 非物理根与物理根的拓扑分类有无不依赖于边界条件的判据？** 在谱丛理论中，能否仅通过单值群表示或环绕数来区分两类根？这将是连接纯数学与物理应用的桥梁。

6. **(低优先级) 极值 Kerr $(a \to 1)$ 极限下，全局存在性是否退化？** 极值极限对应 III 型奇异纤维。在此极限下谱丛截面是否存在但非解析？这对 LACI 判据在 $a \to 1$ 区域的适用性有何影响？

---

## 9. 版本记录

- v0.1（2026-07-25）：初稿。系统梳理 Leaver 连分数全局存在性的理论基础、开放问题和推进路径。
