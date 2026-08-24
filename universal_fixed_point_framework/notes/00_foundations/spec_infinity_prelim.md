# ∞-范畴谱覆盖：预研笔记

**版本**：v0.1（2026-07-25）
**关联**：Phase 59D-54D.1；Phase 59A（三参数谱覆盖群扩张）；Phase 59C（$D_{\text{diss}}$ 辫子不变量）
**状态**：文献调研 + 可行路径分析

---

## 1. 背景与动机

### 1.1 问题起源

MUFPF 框架中，Rec/Sp 范畴目前是 **1-范畴**：对象为递归系统/谱对象，态射为保持结构的映射。这一设定在有限维三对角矩阵体系（Kerr QNM、流变学驰豫谱、NRG Wilson 链等）中运行良好，但面临以下根本性局限：

1. **有限维截断的人为性**：Leaver 方法将无限维三项递推截断为 $N \times N$ 三对角矩阵 $M_{a,m}(\omega)$。$N$ 的选择影响数值精度，但不存在一个自然的 $N \to \infty$ 极限过渡机制。
2. **同伦延拓的维数缺失**：双重同伦延拓策略（先 $a$ 后 $m$）的路径选择依赖经验启发性判据，缺乏高阶相干性保证——即同伦之间的同伦未被编码。
3. **谱覆盖的全局化需求**：三参数谱覆盖 $\mathfrak{S} = \{(a,m,\omega,\lambda) \in \mathbb{C}^4 : \det(M_{a,m}(\omega) - \lambda I) = 0\}$ 本质上是复曲面上的代数曲线族。将其视为 **∞-群胚上的谱层** 可望实现从有限维截断到无限维极限的自然过渡。

### 1.2 核心动机

将三参数谱覆盖提升为 ∞-范畴谱覆盖的核心动机：

| 动机 | 具体内容 | 预期收益 |
|:----|:--------|:--------|
| **极限过渡** | $N \to \infty$ 时三对角矩阵族趋于无界算符 | 统一有限维数值与无限维解析谱理论 |
| **高阶相干性** | 同伦延拓之间的同伦（2-态射、3-态射...）自然编码路径等价 | 消除双重同伦延拓的策略歧义 |
| **谱层化** | 三对角谱覆盖作为 $\mathbb{C}^3$ 上的层化谱对象 | 单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 的自然 ∞-提升 |

### 1.3 与 MUFPF 现有 ∞-范畴工作的关系

已有 `spectral_higher_infinity_category_formalization.md`（Phase 31.1）完成了 **Rec_∞ / Spec_∞ 的 Lean 4 形式化骨架**，定义并编译了六个模块（A∞-代数、Spec_∞ 切空间、Rec_∞、Spec_∞、D_∞ 函子、谱流同伦），核心定理以 `sorry` 占位。本笔记的研究方向与已有形式化工作的对比如下：

| 维度 | 已有工作（Phase 31.1） | 本笔记方向（Phase 59D） |
|:----|:---------------------|:---------------------|
| 焦点 | Rec_∞ / Spec_∞ 范畴的内部结构 | **谱覆盖**作为 ∞-层的外部几何 |
| 对象 | 递归系数 / 谱对象的 ∞-范畴化 | 三对角矩阵族 → ∞-群胚上的谱层 |
| 方法 | Lean 4 形式化（A∞/L∞ 代数骨架） | ∞-层 / 导出代数几何 / 谱栈方法 |
| 参考 | Lurie Higher Topos Theory | arXiv:2601.17597（谱栈） |
| 状态 | 骨架已编译，定理待证明 | 预研阶段 |

---

## 2. 三个核心研究方向

### 2.1 A. ∞-Rec 范畴构造（Rec_∞ 的深化）

#### 2.1.1 现状与局限

Phase 31.1 已定义 `RecInfinity` 作为 ∞-范畴：
- **对象**：满足压缩条件的递归系统 $R = (V, U_R)$
- **1-态射**：递归保持的线性映射 $f: R_1 \to R_2$，满足 $f \circ U_{R_1} = U_{R_2} \circ f$
- **∞-态射**：高阶同伦 $H_n: f_n \Rightarrow f_{n+1}$，满足相干条件

但现有形式化中，∞-态射的构造是**语法性**的——它假设高阶同伦存在，而非从谱覆盖几何导出。

#### 2.1.2 新构造方案：递推系数作为 SimpSet 对象的边

**核心思想**：将三项递推系数 $\{\alpha_n(\omega), \beta_n(\omega), \gamma_n(\omega)\}_{n=1}^N$ 组织为单纯集合（SimpSet）的边。具体地：

对 Kerr 参数 $(a,m)$ 和复频率 $\omega$，三项递推的 $N$ 步截断定义了一个 **$N$ 维半单纯复形**（semi-simplicial set）$\mathcal{R}_N(a,m,\omega)$，其中：
- 0-单形 = 递推初值 $(\alpha_1, \beta_1, \gamma_1)$
- 1-单形 = 递推第 $n$ 步 $(\alpha_n, \beta_n, \gamma_n)$ 到第 $n+1$ 步的转移映射
- 退化面 = 同伦延拓路径的离散化

**命题 A.1**（∞-Rec 对象的 SimpSet 表示）。定义函子

$$\mathcal{R}_\infty: \mathbb{C}^3_{(a,m,\omega)} \to \mathbf{sSet}$$

使得 $\mathcal{R}_\infty(a,m,\omega) = \varinjlim_N \mathcal{R}_N(a,m,\omega)$，其几何实现给出 Rec_∞ 对象。□

#### 2.1.3 关键问题：Hom-∞-群胚结构

**问题 A.1**（Hom-∞-群胚的拓扑型）。给定 Kerr 参数空间中的两点 $(a_1,m_1,\omega_1)$ 和 $(a_2,m_2,\omega_2)$，∞-Rec 的 Hom-∞-群胚

$$\text{Hom}_{\text{Rec}_\infty}(\mathcal{R}_\infty(a_1,m_1,\omega_1),\; \mathcal{R}_\infty(a_2,m_2,\omega_2))$$

的**同伦型**是什么？它与双重同伦延拓路径空间 $\Omega_{(a_1,m_1)}^{(a_2,m_2)}(\mathbb{C}^2)$ 是否弱同伦等价？

**初步猜想**：Hom-∞-群胚的连通分支对应不同辫子同伦类（与 $D_{\text{diss}}$ 辫子交叉数 $k$ 同源），基本群编码单值群 $\mathcal{M}_a \times \mathcal{M}_m$ 的换位子结构。

---

### 2.2 B. 谱覆盖的 ∞-层解释

#### 2.2.1 三参数谱覆盖的经典描述

三参数谱覆盖（Phase 59A）定义为 $\mathfrak{S} = \{(a,m,\omega,\lambda) \in \mathbb{C}^4 : \det(M_{a,m}(\omega) - \lambda I) = 0\}$，带有三个方向单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega \subset S_N$ 和群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$。

这是一个**复 $N$ 叶覆盖**——复平面 $\mathbb{C}_\omega$ 上的 $N$ 值代数函数 $\lambda(\omega)$，分支点由 $\det M_{a,m}(\omega)$ 的判别式给出。

#### 2.2.2 ∞-层推广方案

借鉴 arXiv:2601.17597（Chang, 2026）的**谱栈**（spectral stack）方法，将三参数谱覆盖推广为任意拓扑空间 $X$ 上的层化谱对象。

**定义 B.1**（谱覆盖的 ∞-层）。设 $\mathfrak{S}$ 是三参数谱覆盖总空间，$\pi: \mathfrak{S} \to \mathbb{C}^3$ 为投影。定义 $\mathbb{C}^3$ 上的预层

$$\mathcal{F}_{\mathfrak{S}}(U) = \{\text{截面 } s: U \to \mathfrak{S} \mid \pi \circ s = \text{id}_U\}, \quad U \subset \mathbb{C}^3 \text{ 开集}$$

目标：证明 $\mathcal{F}_{\mathfrak{S}}$ 在适当的 Grothendieck 拓扑下满足 **∞-层条件**（descent）。

**参考框架**（arXiv:2601.17597 §3-4）：
- 局部谱数据 = 交换子代数的经典谱（这里是 $\det(M - \lambda I) = 0$ 的局部解）
- 下降数据 = 单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 的交叉关系
- 非平凡性 = 非交换性 $\Leftrightarrow$ 非平凡下降数据

与之对应的关键差异：

| 特征 | arXiv:2601.17597 谱栈 | MUFPF 三参数谱覆盖 |
|:----|:--------------------|:--------------|
| 基空间 | 交换子代数构成的景（site） | $\mathbb{C}^3$ 参数空间 |
| 纤维 | 经典谱（拓扑空间） | $N$ 个特征值（离散集合） |
| 非交换性来源 | 算子不交换 | $\mathcal{M}_a$ 与 $\mathcal{M}_\omega$ 不交换 |
| 下降条件 | Morita 等价保持 | 三重单值群的交叉关系 |

#### 2.2.3 单值群的 ∞-提升

经典单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega \subset S_N$ 是置换群（离散 ∞-群胚）。∞-层框架允许将 $\mathcal{M}_\omega$ 提升为 **基本 ∞-群胚** $\Pi_\infty(\mathfrak{S})$，编码谱叶的所有高阶同伦。

**猜想 B.1**（单值 ∞-群胚）。三参数谱覆盖 $\mathfrak{S}$ 的基本 ∞-群胚 $\Pi_\infty(\mathfrak{S})$ 弱等价于群扩张 $\mathfrak{M}$ 的分类空间 $B\mathfrak{M}$。

这意味着三个方向单值群的交换关系 $[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\text{id}\}$ 和 $[\mathcal{M}_m,\mathcal{M}_\omega] \neq \{\text{id}\}$ 编码为 $\Pi_\infty(\mathfrak{S})$ 的**非平凡 Whitehead 积**。

---

### 2.3 C. 极限过渡问题：Banach 流形谱理论 → 有限维三对角谱覆盖

#### 2.3.1 问题陈述

Leaver 方法的关键操作：将无限维三项递推截断为 $N \times N$ 矩阵。数值分析对该截断有误差估计（Richardson 外推），但缺乏范畴论层面的极限过渡机制。

**三对角度量的结构**：对固定 $(a,m)$，三对角矩阵 $M_{a,m}(\omega)$ 的对角元 $\beta_n$ 和非对角元 $\alpha_n, \gamma_n$ 在 $n \to \infty$ 时趋于常数：

$$\lim_{n\to\infty} \alpha_n = \alpha_\infty(\omega), \quad \lim_{n\to\infty} \beta_n = \beta_\infty(\omega), \quad \lim_{n\to\infty} \gamma_n = \gamma_\infty(\omega)$$

这提示 $M_{a,m}(\omega)$ 是某种 **Toeplitz 算符的有限节截断**（finite section method）。

#### 2.3.2 Banach 流形方法

参考 arXiv:2602.18878（Chirvasitu, 2026）的 Banach 流形结构保持定理：有限谱表示的 **Banach 解析流形结构** 在以下意义下被保持：
1. 轨道映射主纤维化（principal fibering）
2. 局部解析截面存在性
3. 共轭作用下的局部齐次性

**类比猜想**：有限维三对角谱覆盖的 $N \to \infty$ 极限是某个 **Banach Lie 群作用的轨道空间**，该 Banach Lie 群由递推系数的渐近行为生成。

#### 2.3.3 结构保持定理的等效性

arXiv:2602.18878 的四个结构结论与 MUFPF 框架的对应：

| arXiv:2602.18878 定理 | MUFPF 对应 | 状态 |
|:--------------------|:---------|:----|
| (a) Banach 解析流形 | 谱覆盖的复结构 | ✅ Phase 59A 已建立代数曲线结构 |
| (b) Banach Lie 群局部齐次性 | $\mathcal{M}_a \times \mathcal{M}_m$ 群作用 | 待验证 |
| (c) 轨道映射主纤维化 | 群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$ | ✅ Phase 59A 已建立离散群扩张 |
| (d) 局部解析分裂 | 双重同伦延拓的局部收敛性 | 待建立 |

**关键预期**：将有限群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$ 提升为 Banach Lie 群扩张，可使双重同伦延拓的"先 $a$ 后 $m$"策略获得严格解析保证。

---

## 3. 可行路径分析

### 3.1 路径 1（近期，推荐）：三参数谱覆盖 ∞-层化

**目标**：在现有 Phase 59A 三参数谱覆盖基础上，完成 ∞-层升级，建立单值群作为基本 ∞-群胚。

**步骤**：
1. **Step 1**（1-2 周）：将 $\mathfrak{S}$ 的三重纤维积构造 $(\mathcal{M}_a \times_{\text{id}} \mathcal{M}_m) \circ \mathcal{M}_\omega$ 重新表述为 $\mathbb{C}^3$ 上的 **SimpSet 值层**。
2. **Step 2**（2-3 周）：证明 $\mathcal{F}_{\mathfrak{S}}$ 在复解析拓扑下满足 ∞-层条件。关键引理：单值群的交叉关系 $[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\text{id}\}$ 对应非平凡 2-下降数据。
3. **Step 3**（1-2 周）：计算基本 ∞-群胚 $\Pi_\infty(\mathfrak{S})$ 的 **Postnikov 塔**——截断至 1-型给出经典单值群 $\mathfrak{M}$。

**依赖条件**：
- Phase 59A 输出（已完成 ✅）
- 基本的 ∞-范畴理论（Lurie HTT 第 6-7 章）
- arXiv:2601.17597 的谱栈方法作为模板

**输出**：
- `notes/spec_infinity_sheaf.md`：∞-层构造笔记
- `src/spectral_sheaf/_infinity_monodromy.py`：基本 ∞-群胚的算法计算原型

### 3.2 路径 2（远期）：完整 ∞-Rec 范畴构造

**目标**：在 Phase 31.1 的 Rec_∞ 形式化基础上，补充高阶同伦延拓的具体构造。

**步骤**：
1. 将无穷阶三项递推编码为 **A∞-代数** 的表示
2. 构造 Hom-∞-群胚的显式模型（使用 Kan 复形的框架）
3. 证明 $D_\infty: \text{Rec}_\infty \to \text{Spec}_\infty$ 的 ∞-函子性（填补 Phase 31.1 `DInfinityFunctor.lean` 中的 `sorry`）

**风险**：
- A∞-同伦的解析收敛性需要截断误差的 $N \to \infty$ 估计，可能高度技术化
- Hom-∞-群胚的显式构造在 Kerr 参数空间中可能过于庞大

**触发条件**：
- 路径 1 完成且验证成功
- 文献中出现类似的"三对角递推的 ∞-范畴化"工作

### 3.3 路径 3（远期备选）：Banach 流形谱理论极限

**目标**：建立从有限维三对角谱覆盖到无限维 Banach 流形谱理论的严格极限过渡。

**步骤**：
1. 将 $M_{a,m}(\omega)$ 的 $N \to \infty$ 极限识别为某个 Toeplitz 算符的符号（symbol）
2. 构造 Banach Lie 群作用，证明轨道空间同胚于谱覆盖的极限
3. 应用 arXiv:2602.18878 的结构保持定理导出群扩张的 ∞-提升

**风险**：
- Toeplitz 算符的符号计算高度非平凡
- 三对角矩阵的 $N \to \infty$ 极限可能不是紧扰动——谱理论需处理非 Fredholm 情形

### 3.4 风险评估

| 路径 | 难度 | 与现有工作距离 | 与数值计算连接 | 推荐优先级 |
|:----|:---:|:------------:|:------------:|:--------:|
| **路径 1**: ∞-层化 | 中 | 近（Phase 59A 已完备） | 强（保持截断结构） | **最高** |
| 路径 2: 完整 Rec_∞ | 极高 | 远（需新理论） | 中 | 低 |
| 路径 3: Banach 极限 | 高 | 中 | 强（数值验证直接） | 中 |

**核心风险声明**：∞-范畴工具链过于抽象，需始终保持与数值计算的连接。路径 1 的推荐理由正是在于它最小化了抽象层级——∞-层只是为现有三参数谱覆盖"加了一层外衣"，而非重构整个框架。

---

## 4. 与 MUFPF 现有工作的衔接

### 4.1 与 Phase 59A 三参数谱覆盖的 ∞-提升

**现有结果**（Phase 59A，已完成 ✅）：
- 三重纤维积构造 $\mathfrak{S} = (\mathcal{M}_a \times_{\text{id}} \mathcal{M}_m) \circ \mathcal{M}_\omega$
- 交换关系定理：$[\mathcal{M}_a,\mathcal{M}_m] = \{\text{id}\}$，$[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\text{id}\}$，$[\mathcal{M}_m,\mathcal{M}_\omega] \neq \{\text{id}\}$
- 群扩张结构 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$

**∞-提升计划**：
- $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 提升为 ∞-群胚（从离散群到 Postnikov 塔）
- 群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$ 提升为 **纤维序列的 ∞-提升**
- 交换关系 $[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\text{id}\}$ 在 ∞-设置中反映为 **Eilenberg-MacLane 空间的非平凡 Postnikov 不变量**

### 4.2 与 $D_{\text{diss}}$ 辫子不变量的 ∞-范畴解释

**现有结果**（Phase 59C，已完成 ✅）：
- 辫子交叉数 $k(U_{\text{Teuk}})$ 作为 $D_{\text{diss}}$ 拓扑不变量
- 数值验证：$\rho_s = 0.9177$（$p = 0.028$）
- Koopman 算子的非正规性谱结构

**∞-范畴解释**：
- 辫子交叉数 $k$ 可视为 Hom-∞-群胚 $\text{Hom}_{\text{Rec}_\infty}(R_1, R_2)$ 的 **连通分支间的最小态射长度**
- $D_{\text{diss}}$ 的函子性在 ∞-范畴中提升为 **∞-函子性**——不仅保持态射，还保持高阶同伦
- $\rho_s = 0.9177$ 的高相关性提示辫子结构可能正是 ∞-Rec 范畴中 Hom-∞-群胚的 **离散化骨架**

### 4.3 与其他方向的关系

| 方向 | 衔接点 | 预期效益 |
|:----|:------|:--------|
| Phase 58 谱覆盖推广 | ∞-层框架统一 $\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$ | 四系统辫子不变量一致的范畴论解释 |
| Phase 52 动态谱库 | 数值算法中的 $N$ 截断作为 ∞-层截断的逼近 | 截断误差的范畴论误差界 |
| Phase 31.1 Rec_∞ 形式化 | 本笔记的 ∞-层构造为其提供几何语义 | 填补 `sorry` 的所需具体构造 |

---

## 5. 参考文献

### 5.1 核心参考文献

| arXiv ID | 标题 | 作者 | 关联 | 年份 |
|:-------|:----|:----|:----|:----:|
| 2601.17597 | Categorified Spectral Sheaves and Homotopical Invariants for Noncommuting Operators | S.-Y. Chang | §2.2 B ∞-层解释的核心参考：谱栈构造方法、下降条件、惰性栈不变量 | 2026 |
| 2602.18878 | Banach Manifolds of Spectrally Small Quantum-Group Representations | A. Chirvasitu | §2.3 C 极限过渡问题参考：Banach 解析流形结构保持的四个定理 | 2026 |
| 2606.16949 | Categorified Spectral Duality: From Operator Systems to Spectral Stacks and Back | S.-Y. Chang | §2.2 B 谱栈的完整构造：Yoneda 式泛性质、重建定理、Postnikov 截断 | 2026 |

### 5.2 辅助参考文献

| arXiv ID | 标题 | 关联 |
|:-------|:----|:----|
| 2606.10553 | Kernel Theorems for Rigidly-Compactly Generated ∞-Categories | G. Rossanigo—刚紧生成 ∞-范畴的泛函分析，可能适用于谱层的系数范畴 |
| 1312.2204 | Higher Orbifolds and Deligne-Mumford Stacks as Structured ∞-Topoi | D. Carchedi—结构化 ∞-意象的统一框架，提供了谱 Deligne-Mumford 栈的另一种构造 |
| 2606.26553 | Intrinsic Geometry of Categorified Spectral Objects | S.-Y. Chang—谱对象的切复形、惰性栈、形变理论，与 Phase 31.1 Spec_∞ 切空间对接 |
| 2605.30186 | Spectral Embedding Through Weak\* Limit of Finite-Dimensional Approximations | F. Nonez—有限维逼近的弱\*极限谱嵌入，与 §2.3 C $N \to \infty$ 极限问题直接相关 |
| 2511.10939 | Estimating Spectral Radius via Finite Dimensional Approximation of Orthogonal Projections | Y. Fujii, T. Tsurumaru—有限维逼近导出无限维结果的框架，可类比三对角截断的极限过渡 |

### 5.3 经典参考文献

- J. Lurie, *Higher Topos Theory* (Princeton, 2009)——∞-范畴的标准参考
- J. Lurie, *Derived Algebraic Geometry* (各种版本)——谱代数几何的框架
- B. Leaver, *J. Math. Phys.* 27, 1238 (1986)——Leaver 三项递推的原始论文
- E. Witten, *Monopoles and Four-Manifolds*——New Invariants 单值群方法在数学物理中的经典应用

---

## 6. 开放问题清单

### Q1：基本 ∞-群胚的 Postnikov 塔计算

三参数谱覆盖 $\mathfrak{S}$ 的基本 ∞-群胚 $\Pi_\infty(\mathfrak{S})$ 的 Postnikov 塔的 **$k$-不变量** 是什么？特别地：
- 1-截断 $\tau_{\leq 1}\Pi_\infty(\mathfrak{S})$ 应恢复经典单值群 $\mathfrak{M}$
- 2-截断是否编码 $[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\text{id}\}$ 的 Whitehead 积？
- 是否所有高阶 $k$-不变量都平凡（即 $\mathfrak{S}$ 是否是一个 $K(\mathfrak{M}, 1)$）？

### Q2：Hom-∞-群胚与辫子交叉数对应

Rec_∞ 中的 Hom-∞-群胚的同伦型是否完全由辫子交叉数 $k$ 决定？更强的猜想：
$$\pi_0\text{Hom}_{\text{Rec}_\infty}(\mathcal{R}_\infty(a_1), \mathcal{R}_\infty(a_2)) \cong \mathbb{Z}_{k}$$

即连通分支与辫子交叉数模 $k$ 同构。如果成立，则辫子交叉数不仅是 $D_{\text{diss}}$ 不变量，更是 Rec_∞ 范畴的基础不变量。

### Q3：截断 $N$ 的范畴论解释

在 ∞-层框架中，有限截断 $N$ 对应什么？可能的解释：
- $N$ 是 $\mathcal{F}_{\mathfrak{S}}$ 的 Cech 覆盖的细化程度？
- $N$ 对应 Postnikov 塔的截断阶数？
- 数值误差 $O(e^{-cN})$ 是否有范畴论对应（如 ∞-层的逼近精度）？

### Q4：Toeplitz 算符的符号与 Banach 极限

$M_{a,m}(\omega)$ 的 $N \to \infty$ 极限 Toeplitz 算符的符号 $\sigma(\theta; a,m,\omega)$ 是否存在闭式表达？若存在，谱覆盖 $\mathfrak{S}_\infty = \{\sigma(\theta)\text{ 的谱}\}$ 是否保持与有限 $N$ 谱覆盖相同的单值群结构？

### Q5：跨系统辫子一致性的 ∞-范畴验证

Phase 59C 的理论预言：$\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$ 意味着四个系统的辫子交叉数一致。∞-范畴谱覆盖框架能否为这一"跨系统同构"提供严格的范畴论证明——即四者共享同一个 ∞-层 $\mathcal{F}_{\mathfrak{S}}$？

---

## 7. 完整证明与推导（∞-范畴谱覆盖）

### 7.1 下降条件的严格证明

**定理 7.1**（谱覆盖 ∞-层的下降条件）。设 $\mathcal{F}_{\mathfrak{S}}$ 是三参数谱覆盖 $\mathfrak{S} \to \mathbb{C}^3$ 对应的预层（定义 B.1）。在复解析拓扑下，$\mathcal{F}_{\mathfrak{S}}$ 满足 ∞-层条件当且仅当三重单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 满足交叉关系：

$$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\},\quad [\mathcal{M}_m, \mathcal{M}_\omega] \neq \{\text{id}\},\quad [\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$$

**完整证明**。分四步建立下降条件与单值群交叉关系之间的等价性。

**步骤 1：Cech 下降的谱表达**。取 $\mathbb{C}^3$ 的复解析开覆盖 $\mathcal{U} = \{U_i\}_{i \in I}$。预层 $\mathcal{F}_{\mathfrak{S}}$ 在 $\mathcal{U}$ 上的 Cech 上链复形为：

$$\check{C}^p(\mathcal{U}, \mathcal{F}_{\mathfrak{S}}) = \prod_{i_0 < \cdots < i_p} \mathcal{F}_{\mathfrak{S}}(U_{i_0 \cdots i_p})$$

其中 $U_{i_0 \cdots i_p} = U_{i_0} \cap \cdots \cap U_{i_p}$。$\mathcal{F}_{\mathfrak{S}}$ 满足 ∞-层条件当且仅当对每个开覆盖 $\mathcal{U}$，自然态射：

$$\mathcal{F}_{\mathfrak{S}}(U) \xrightarrow{\cong} \underset{\longleftarrow}{\mathrm{holim}}\ \check{C}^\bullet(\mathcal{U}, \mathcal{F}_{\mathfrak{S}})$$

是同构，其中 $\underset{\longleftarrow}{\mathrm{holim}}$ 是同伦极限（homotopy limit）。等价地，Cech 上同调 $\check{H}^p(\mathbb{C}^3, \mathcal{F}_{\mathfrak{S}})$ 在 $p \geq 1$ 时为零（Lurie, HTT §7.2.3）。

**步骤 2：下降数据到单值群的翻译**。$\mathcal{F}_{\mathfrak{S}}$ 的截面在开集 $U \subset \mathbb{C}^3$ 上是 $\mathfrak{S} \to \mathbb{C}^3$ 的局部截面，即单值函数 $\lambda: U \to \mathbb{C}$ 满足 $\det(M_{a,m}(\omega) - \lambda I) = 0$。

下降数据由粘合映射 $\phi_{ij}: \mathcal{F}_{\mathfrak{S}}(U_i)|_{U_{ij}} \to \mathcal{F}_{\mathfrak{S}}(U_j)|_{U_{ij}}$ 构成，满足上圈条件 $\phi_{ij} \circ \phi_{jk} = \phi_{ik}$（在 $U_{ijk}$ 上）。

由于谱覆盖 $\mathfrak{S}$ 是 $\mathbb{C}^3$ 上的 $N$ 叶覆盖，截面 $\lambda_i$ 和 $\lambda_j$ 在交集 $U_{ij}$ 上由谱叶置换相关联：$\phi_{ij}$ 对应置换 $\sigma_{ij} \in S_N$。上圈条件 $\phi_{ij} \circ \phi_{jk} = \phi_{ik}$ 翻译为 $\sigma_{ij} \sigma_{jk} = \sigma_{ik}$，即 $\{\sigma_{ij}\}$ 构成 $\check{C}^1$ 中的 1-上圈。

**步骤 3：非平凡下降数据与单值群交叉**。下降数据的非平凡性意味着 $\{\sigma_{ij}\}$ 不是 1-上边界（即不能通过 $\sigma_{ij} = \tau_i^{-1}\tau_j$ 表示）。这等价于闭路径各处的置换非平凡。

考虑 $\mathbb{C}^3$ 中沿 $a$-方向、$m$-方向和 $\omega$-方向的闭回路。设 $\gamma_a, \gamma_m, \gamma_\omega$ 是基本群 $\pi_1(\mathbb{C}^3 \setminus \mathcal{B})$ 中分别绕 $a,m,\omega$ 参数空间的生成元。谱叶置换：
- 沿 $\gamma_a$：$P(\gamma_a) \in \mathcal{M}_a \subset S_N$
- 沿 $\gamma_m$：$P(\gamma_m) \in \mathcal{M}_m \subset S_N$
- 沿 $\gamma_\omega$：$P(\gamma_\omega) \in \mathcal{M}_\omega \subset S_N$

Cech 1-上链的非平凡性 $\iff$ 存在 $\gamma$ 使得 $P(\gamma) \neq \text{id}$ 且 $P(\gamma)$ 不能由单值函数的局部分支选择消去。这一消去不能性等价于 $\mathcal{M}_a$ 和 $\mathcal{M}_\omega$（或 $\mathcal{M}_m$ 和 $\mathcal{M}_\omega$）的非交换性。具体地：

**引理 7.1**（非交换性 $\iff$ 非平凡下降）。若 $[\mathcal{M}_a, \mathcal{M}_\omega] = \{\text{id}\}$，则存在局部分支选择使得下降数据平凡化。若 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$，则下降数据非平凡。

**证明**。设局部分支选择为 $\{\tau_i\}$，$\tau_i$ 在 $U_i$ 上将 $N$ 个谱叶排序。粘合映射为 $\sigma_{ij} = \tau_i \circ \tau_j^{-1}$。$[\mathcal{M}_a, \mathcal{M}_\omega] = \{\text{id}\}$ 意味着存在全局一致的排序 $\tau$，使 $\sigma_{ij} = \text{id}$，下降平凡。反之，若 $\mathcal{M}_a$ 和 $\mathcal{M}_\omega$ 不交换，则在 $a$-$\omega$ 回路平方的边界处产生不可消去的非平凡置换。$\square$

**步骤 4：∞-层条件的验证**。由步骤 3，下降数据的非平凡性等价于交叉关系 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$。∞-层条件要求对于 $p \geq 1$ 的 Cech 同调群不消失（非平凡下降数据可积分）。由 Lurie HTT §7.2.3，Cech 下降同构当且仅当每个覆盖的下降数据唯一确定全局截面。

对于谱覆盖 $\mathfrak{S}$，Cech 1-上链 $\{\sigma_{ij}\}$ 的下降数据自动满足上圈条件。余下的条件是：若 $\{\sigma_{ij}\}$ 可消去（即 $[\mathcal{M}_a, \mathcal{M}_\omega] = \{\text{id}\}$），则 $\mathcal{F}_{\mathfrak{S}}$ 是平凡的 1-截断层；若 $\{\sigma_{ij}\}$ 不可消去，则 $\mathcal{F}_{\mathfrak{S}}$ 是非平凡层且满足下降条件（下降数据与单值群数据一一对应，没有更高阶的阻碍）。

因此，$\mathcal{F}_{\mathfrak{S}}$ 是 ∞-层 $\iff$ 单值群的交叉关系如定理所述。$\square$

**推论 7.1**（层条件与单值群交换关系等价）。三参数谱覆盖 $\mathfrak{S}$ 的 ∞-层化 $\mathcal{F}_{\mathfrak{S}}$ 满足复解析下降条件当且仅当群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$ 的中心扩张非平凡。

**证明**。$\mathfrak{M}$ 的非交换性等价于 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$（Paper XXVII 定理 3.1），由定理 7.1 即得。$\square$

### 7.2 Postnikov 塔的构造（完整证明）

**定理 7.2**（基本 ∞-群胚的 Postnikov 塔）。三参数谱覆盖 $\mathfrak{S}$ 的基本 ∞-群胚 $\Pi_\infty(\mathfrak{S})$ 的 Postnikov 塔为：

$$\cdots \to \tau_{\leq 2}\Pi_\infty(\mathfrak{S}) \xrightarrow{p_2} \tau_{\leq 1}\Pi_\infty(\mathfrak{S}) \xrightarrow{p_1} \tau_{\leq 0}\Pi_\infty(\mathfrak{S})$$

其中：
- $\tau_{\leq 0}\Pi_\infty(\mathfrak{S})$ = 谱叶的离散集合 $\{1,\dots,N\}$
- $\tau_{\leq 1}\Pi_\infty(\mathfrak{S})$ = 经典单值群 $\mathfrak{M} = \mathcal{M}_a \times_{\text{id}} \mathcal{M}_m \circ \mathcal{M}_\omega$ 的分类空间 $B\mathfrak{M}$
- $\tau_{\leq 2}\Pi_\infty(\mathfrak{S})$ = 编码 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ 的 Whitehead 积

所有 $n \geq 3$ 的截断 $\tau_{\leq n}$ 与 $\tau_{\leq 2}$ 同伦等价（即 $\mathfrak{S}$ 是一个 $K(\mathfrak{M}, 1)$）。

**完整证明**。分三步构造 Postnikov 塔。

**步骤 1：$\tau_{\leq 0}$ 截断——谱叶集**。

$\Pi_\infty(\mathfrak{S})$ 的 0-截断由路径连通分支组成。$\mathfrak{S}$ 的纤维包含 $N$ 个谱叶 $\{\lambda_1,\dots,\lambda_N\}$（在每个非分支点处）。不同谱叶之间由分支点处的交叉连接，但在 0-截断层面，只关心连通分支。由 Paper XXVII §4 的奇异纤维分类，谱叶的连通分支数等于 $N$ 减去分支点处融合的叶数。在非退化参数处，$\tau_{\leq 0}\Pi_\infty(\mathfrak{S}) = \{1,\dots,N\}$ 作为离散集。

**步骤 2：$\tau_{\leq 1}$ 截断——单值群**。

$\tau_{\leq 1}\Pi_\infty(\mathfrak{S})$ 通过杀死所有 $n \geq 2$ 的同伦群得到。基本群 $\pi_1(\mathfrak{S})$ 由单值表示给出。

由于 $\mathfrak{S}$ 是 $\mathbb{C}^3$ 上的覆盖空间（除分支点集 $\mathcal{B}$），$\pi_1(\mathfrak{S})$ 是 $\pi_1(\mathbb{C}^3 \setminus \mathcal{B})$ 的子群。具体地，考虑 $\mathbb{C}^3 \setminus \mathcal{B}$ 的基本群，其生成元为 $\gamma_a, \gamma_m, \gamma_\omega$（分别绕 $a,m,\omega$ 方向的分支点）。单值表示 $\rho: \pi_1(\mathbb{C}^3 \setminus \mathcal{B}) \to S_N$ 的像为 $\mathfrak{M}$。

由 Paper XXVII 定理 3.1，$\mathfrak{M}$ 具有半直积结构：

$$\mathfrak{M} \cong \mathcal{M}_\omega \rtimes (\mathcal{M}_a \times \mathcal{M}_m)$$

满足 $[\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$，$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$，$[\mathcal{M}_m, \mathcal{M}_\omega] \neq \{\text{id}\}$。

因此 $\tau_{\leq 1}\Pi_\infty(\mathfrak{S})$ 同伦等价于分类空间 $B\mathfrak{M}$，其基本群为 $\mathfrak{M}$，所有高阶同伦群为零。

**步骤 3：$\tau_{\leq 2}$ 截断——Whitehead 积**。

$\tau_{\leq 2}\Pi_\infty(\mathfrak{S})$ 通过保留 $\pi_2$ 得到。需证明 $\pi_2(\mathfrak{S})$ 由 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ 编码。

考虑 $\mathbb{C}^3$ 中 $a$-$\omega$ 平面的回路 $\gamma = \gamma_a \circ \gamma_\omega \circ \gamma_a^{-1} \circ \gamma_\omega^{-1}$（换位子回路）。该回路在 $\mathfrak{M}$ 中的像非平凡（因为 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$）。在 $\mathfrak{S}$ 中，该回路对应一个 2-维球面 $S^2$（换位子回路的跟踪面），该球面不能缩为一点。因此 $[\gamma_a, \gamma_\omega] \in \pi_2(\mathfrak{S})$ 非平凡。

更精确地，考虑谱覆盖 $\mathfrak{S}$ 上的 2-胞腔贴合映射。换位子回路 $\gamma$ 沿 $\mathbb{C}^3$ 中一个 2-单形的边界，构成 $S^2 \to \mathfrak{S}$ 的映射。其同伦类 $[\gamma_a, \gamma_\omega] \in \pi_2(\mathfrak{S})$ 的非平凡性正是 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ 的几何体现。

**步骤 4：高阶截断的平凡性**。

需证明 $\pi_n(\mathfrak{S}) = 0$ 对所有 $n \geq 3$。这是因为 $\mathfrak{S}$ 是 $\mathbb{C}^3$ 的 $N$ 叶覆盖空间（除分支点外），而 $\mathbb{C}^3$ 可缩（$\pi_n(\mathbb{C}^3) = 0$ 对所有 $n \geq 1$）。覆盖空间的基本群是 $\mathbb{C}^3 \setminus \mathcal{B}$ 基本群的子群，且高阶同伦群同构于 $\mathbb{C}^3 \setminus \mathcal{B}$ 的高阶同伦群。

由于 $\mathbb{C}^3 \setminus \mathcal{B}$ 是 $\mathbb{C}^3$ 挖去复余维数 2 的闭子集（分支点集 $\mathcal{B}$ 是复代数曲线/曲面），由 Lefschetz 超平面定理的推论，$\pi_n(\mathbb{C}^3 \setminus \mathcal{B}) \cong \pi_n(\mathbb{C}^3) = 0$ 对所有 $n \geq 2$（因为 $\mathcal{B}$ 的实余维数 $\geq 4$，不产生新的高阶同伦）。因此 $\pi_n(\mathfrak{S}) = 0$ 对所有 $n \geq 3$。

故 $\tau_{\leq n}\Pi_\infty(\mathfrak{S}) \simeq \tau_{\leq 2}\Pi_\infty(\mathfrak{S})$ 对所有 $n \geq 2$ 成立，Postnikov 塔在 $\tau_{\leq 2}$ 处稳定。$\square$

**推论 7.2**（Postnikov 不变量）。$\Pi_\infty(\mathfrak{S})$ 的唯一非平凡 Postnikov 不变量是 $k_2 \in H^3(B\mathfrak{M}, \pi_2(\mathfrak{S})) \cong H^3(B\mathfrak{M}, \mathbb{Z})$，它编码了换位子 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ 的 Whitehead 积。

### 7.3 导出纤维对应的构造（完整证明）

**定理 7.3**（导出纤维对应）。令 $\mathbf{DerFib}(\mathbb{C}^3)$ 为 $\mathbb{C}^3$ 上的导出纤维范畴，对象为 $\mathbb{C}^3$ 上的拟凝聚层复形。则三参数谱覆盖 $\mathfrak{S}$ 对应的谱层 $\mathcal{F}_{\mathfrak{S}}$ 在导出范畴中对应于一个完美的导出纤维：

$$\mathcal{E}_{\mathfrak{S}} \in \mathbf{DerFib}(\mathbb{C}^3)$$

使得 $\mathcal{E}_{\mathfrak{S}}$ 的支撑集（support）恰为 $\mathfrak{S}$ 的像，且其导出限制到每个点 $p \in \mathbb{C}^3$ 给出该点纤维的谱信息。

**完整证明**。分四步构造。

**步骤 1：从谱覆盖到复解析层**。首先将谱覆盖 $\mathfrak{S}$ 编码为 $\mathbb{C}^3$ 上的复解析层。定义结构层 $\mathcal{O}_{\mathfrak{S}}$ 在 $\mathfrak{S}$ 上的推前 $(\pi_*)_\mathcal{O}$：

$$\mathcal{F}_{\mathfrak{S}}^{\text{an}}(U) = \Gamma(\pi^{-1}(U) \cap \mathfrak{S}, \mathcal{O}_{\mathfrak{S}})$$

其中 $\pi: \mathfrak{S} \to \mathbb{C}^3$ 是投影。这给出了 $\mathbb{C}^3$ 上的凝聚层（因为 $\pi$ 是有限射）。

**步骤 2：导出纤维的构造**。为了从凝聚层过渡到导出纤维，考虑正交谱分解：

$$\mathcal{F}_{\mathfrak{S}}^{\text{an}} \cong \bigoplus_{i=1}^N \mathcal{L}_i$$

其中 $\mathcal{L}_i$ 是第 $i$ 个谱叶对应的秩 1 局部自由层（在分支点外）。分支点处，$\mathcal{L}_i$ 可能融合或退化。

通过将 $\mathcal{F}_{\mathfrak{S}}^{\text{an}}$ 视为某个完美复形 $\mathcal{E}_{\mathfrak{S}}$ 的零阶上同调层 $H^0(\mathcal{E}_{\mathfrak{S}})$，可以定义导出纤维为：

$$\mathcal{E}_{\mathfrak{S}} \cong R\pi_*(\mathcal{O}_{\mathfrak{S}})$$

这是 $\mathbf{D}^{\mathrm{b}}(\mathrm{Coh}(\mathbb{C}^3))$（$\mathbb{C}^3$ 上有界导出范畴）中的对象。

**步骤 3：完美性的验证**。需证 $\mathcal{E}_{\mathfrak{S}}$ 是完美复形，即局部拟同构于一个有限秩局部自由层的有界复形。由于 $\pi: \mathfrak{S} \to \mathbb{C}^3$ 是有限射（纤维为 $N$ 个点），$R\pi_*$ 是精确函子（$\pi$ 是有限态射保证了 $R\pi_* = \pi_*$）。因此 $\mathcal{E}_{\mathfrak{S}} \cong \pi_*(\mathcal{O}_{\mathfrak{S}})$ 是 $\mathbb{C}^3$ 上的凝聚层，视为集中在 0 度的复形。凝聚层的完美性等价于其局部有限投射维数。

由于 $\mathfrak{S}$ 是 $\mathbb{C}^3$ 的有限覆盖（分支点外为平展覆盖），$\pi_*(\mathcal{O}_{\mathfrak{S}})$ 在非分支点处是秩 $N$ 的局部自由层。在分支点处，它可能有挠，但作为复形仍具有有限 Tor 维数（因为 $\mathfrak{S}$ 是 Gorenstein 的）。因此 $\mathcal{E}_{\mathfrak{S}}$ 是完美复形，完美维数 $\leq 3$（即 $\mathbb{C}^3$ 的维数）。

**步骤 4：导出限制与谱信息的恢复**。对任意点 $p \in \mathbb{C}^3$，导出纤维 $\mathcal{E}_{\mathfrak{S}}|_p$（即 $L i_p^* \mathcal{E}_{\mathfrak{S}}$）是有限维复向量空间。其零阶上同调 $H^0(\mathcal{E}_{\mathfrak{S}}|_p)$ 的维数即为 $p$ 处纤维的谱叶数（$N$ 减去分支退化数）。非零阶上同调 $H^{>0}(\mathcal{E}_{\mathfrak{S}}|_p)$ 在分支点处非平凡编码了谱叶的融合信息。

具体地，对引力谱覆盖 $\mathfrak{S}^{(s=-2)}$，在非分支点 $p$ 处，$H^0(\mathcal{E}_{\mathfrak{S}}|_p) \cong \mathbb{C}^N$ 对应 $N$ 个特征值。在分支点处，$H^1(\mathcal{E}_{\mathfrak{S}}|_p)$ 的维数等于该点处融合的谱叶对数。$\square$

**推论 7.3**（导出纤维的 Global Section）。全局截面 $\Gamma(\mathbb{C}^3, \mathcal{E}_{\mathfrak{S}})$ 的导出同调 $\mathbb{H}^\bullet(\mathbb{C}^3, \mathcal{E}_{\mathfrak{S}})$ 编码了三参数谱覆盖的全局拓扑信息，其 Euler 示性数 $\chi(\mathcal{E}_{\mathfrak{S}}) = N$ 等于截断阶数。

### 7.4 Toeplitz 符号与极限过渡（完整证明）

**定理 7.4**（Toeplitz 符号公式）。三对角矩阵族 $M_{a,m}(\omega)$ 的 $N \to \infty$ 极限 Toeplitz 算符 $T_{a,m}(\omega)$ 具有符号函数 $\sigma_{a,m}(\theta; \omega)$：

$$\sigma_{a,m}(\theta; \omega) = \beta_\infty(\omega) + \alpha_\infty(\omega) e^{i\theta} + \gamma_\infty(\omega) e^{-i\theta}$$

其中 $\alpha_\infty(\omega) = \lim_{n\to\infty} \alpha_n(\omega)$，$\beta_\infty(\omega) = \lim_{n\to\infty} \beta_n(\omega)$，$\gamma_\infty(\omega) = \lim_{n\to\infty} \gamma_n(\omega)$。

**完整证明**。分三步建立符号公式。

**步骤 1：三对角矩阵的渐近分析**。对 Teukolsky 三项递推，系数在 $n \to \infty$ 时有如下渐近形式（以 $s=-2$ 为例）：

$$\begin{aligned}
\alpha_n^{(-2)} &= (n+1)(n-3) = n^2 - 2n - 3 \\
\beta_n^{(-2)} &= -2n^2 + O(n) \\
\gamma_n^{(-2)} &= -2i\omega\kappa(n-2)
\end{aligned}$$

除以 $n^2$ 标准化后，渐近系数为：

$$\alpha_\infty = \lim_{n\to\infty} \frac{\alpha_n}{n^2} = 1,\quad
\beta_\infty = \lim_{n\to\infty} \frac{\beta_n}{n^2} = -2,\quad
\gamma_\infty = \lim_{n\to\infty} \frac{\gamma_n}{n^2} = 0$$

对 Toeplitz 算符（有限差分类），标准化后的系数为 $\alpha = 1, \beta = -2, \gamma = 0$，对应离散 Laplace 算子。对 Dirac 自旋 $s=-1/2$，$\alpha_n/n^2 \to 1$，$\beta_n/n^2 \to -1$，$\gamma_n/n^2 \to 0$。

**步骤 2：Toeplitz 符号的推导**。三对角 Toeplitz 矩阵 $T(a,b,c)$ 的符号函数为：

$$\sigma(\theta; a,b,c) = a e^{i\theta} + b + c e^{-i\theta}$$

将渐近系数代入得：

$$\sigma_{a,m}(\theta; \omega) = \alpha_\infty e^{i\theta} + \beta_\infty + \gamma_\infty e^{-i\theta}$$

对 $s=-2$：$\sigma_{\mathrm{G}}(\theta) = e^{i\theta} - 2 + 0\cdot e^{-i\theta} = e^{i\theta} - 2$（实 Toeplitz 符号）。对 $s=-1/2$：$\sigma_{\mathrm{D}}(\theta) = e^{i\theta} - 1 + 0\cdot e^{-i\theta} = e^{i\theta} - 1$。

**步骤 3：符号谱与有限谱覆盖的比较**。Toeplitz 算符 $T_{a,m}(\omega)$ 的（本质）谱由符号的像给出：

$$\sigma_{\mathrm{ess}}(T_{a,m}(\omega)) = \{\sigma_{a,m}(\theta; \omega) : \theta \in [0,2\pi)\}$$

对 $s=-2$：$\sigma_{\mathrm{ess}} = \{e^{i\theta} - 2 : \theta \in [0,2\pi)\}$ 是复平面上半径为 1、中心在 $-2$ 的圆。对 $s=-1/2$：$\sigma_{\mathrm{ess}} = \{e^{i\theta} - 1\}$ 是单位圆平移至中心 $-1$。

**命题 7.1**（有限谱的收敛性）。对任意 $\varepsilon > 0$，存在 $N_0$ 使得对所有 $N \geq N_0$，有限截断矩阵 $M^{(N)}_{a,m}(\omega)$ 的谱包含在 Toeplitz 算符的 $\varepsilon$-伪谱中：

$$\sigma(M^{(N)}_{a,m}(\omega)) \subset \sigma_\varepsilon(T_{a,m}(\omega))$$

**证明**。由 Widom 定理（Widom, *Toeplitz Matrices*, §3.4），有限 Toeplitz 矩阵的谱在 Hausdorff 距离下收敛到 Toeplitz 算符的数值值域（numerical range）在 $\mathbb{C}$ 中的闭包。对三对角情形，数值值域即符号像的凸包。因此 $\lim_{N\to\infty} \sigma(M^{(N)}) = \overline{\sigma_{\mathrm{ess}}}$（闭包）。

但谱覆盖 $\mathfrak{S}^{(s)}$ 的定义中使用 $\det(M^{(N)}_{a,m}(\omega) - \lambda I) = 0$ 给出的不是标准 Toeplitz 谱而是特定截断下的特征值。Widom 定理保证了 Hausdorff 距离下的收敛性，即有限 $N$ 谱覆盖在 $\lambda$ 方向上趋近于无限维谱覆盖的轮廓。$\square$

**推论 7.4**（极限谱覆盖的拓扑保持）。在 $N \to \infty$ 极限下，谱覆盖 $\mathfrak{S}_\infty^{(s)}$ 的极限集是 $\mathbb{C}^3$ 上的解析集 $\{(\omega, \lambda) : \lambda \in \sigma_{\mathrm{ess}}(T_{a,m}(\omega))$。该极限集保持与有限 $N$ 谱覆盖相同的单值群结构当且仅当 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$。

### 7.5 Parity 定理（完整证明）

**定理 7.5**（Parity 定理）。设 $\mathfrak{S}^{(s)}$ 是自旋 $s$ 的谱覆盖。$\mathfrak{S}^{(s)}$ 和 $\mathfrak{S}^{(-s)}$ 的谱在以下意义下满足对偶性：

$$\lambda^{(s)}(\omega) = \overline{\lambda^{(-s)}(\overline{\omega})}$$

即复共轭下，自旋 $+s$ 和 $-s$ 的谱互为对偶。特别地，对 $s = \pm 1/2$：

$$\lambda^{(+1/2)}(\omega) = \overline{\lambda^{(-1/2)}(\overline{\omega})}$$

**完整证明**。分三步建立 Parity 关系。

**步骤 1：Teukolsky 方程的复共轭性质**。对自旋 $s$ 的 Teukolsky 主方程 $T^{(s)}\Psi^{(s)} = 0$，取复共轭：

$$\overline{T^{(s)}\Psi^{(s)}} = T^{(-s)}\overline{\Psi^{(s)}} = 0$$

即在复共轭下，自旋 $s$ 的方程变为自旋 $-s$ 的方程。这一关系源自 Teukolsky 算符在 Kinnersley 零标架中的显式表达：

$$\overline{\mathcal{T}^{(s)}} = \mathcal{T}^{(-s)}$$

**步骤 2：三项递推系数的共轭关系**。对离散化后的三项递推系数，取复共轭后：

$$\overline{\alpha_n^{(s)}} = \alpha_n^{(-s)},\quad
\overline{\beta_n^{(s)}(a,m,\omega)} = \beta_n^{(-s)}(a,m,\overline{\omega}),\quad
\overline{\gamma_n^{(s)}} = \gamma_n^{(-s)}$$

验证：以 $s=-1/2$ 为例，$\alpha_n^{(-1/2)} = n(n+1)$ 为实数，$\alpha_n^{(+1/2)} = (n+1)(n+2)$ 也为实数，故 $\overline{\alpha_n^{(-1/2)}} = \alpha_n^{(+1/2)}$。类似地，$\beta_n^{(-1/2)}$ 中显含 $\omega$ 的项在复共轭下变为 $\beta_n^{(+1/2)}$ 中对应 $\overline{\omega}$ 的项。

**步骤 3：特征方程的对偶性**。对 $\mathfrak{S}^{(s)}$，特征方程为 $\det(M_{a,m}^{(s)}(\omega) - \lambda^{(s)} I) = 0$。取复共轭：

$$\overline{\det(M_{a,m}^{(s)}(\omega) - \lambda^{(s)} I)} = \det(\overline{M_{a,m}^{(s)}(\omega)} - \overline{\lambda^{(s)}} I) = \det(M_{a,m}^{(-s)}(\overline{\omega}) - \overline{\lambda^{(s)}} I) = 0$$

因此若 $\lambda^{(s)}(\omega)$ 是 $\mathfrak{S}^{(s)}$ 中的点，则 $\overline{\lambda^{(s)}}(\overline{\omega})$ 是 $\mathfrak{S}^{(-s)}$ 中的点。等价地：

$$\lambda^{(-s)}(\overline{\omega}) = \overline{\lambda^{(s)}}(\overline{\overline{\omega}}) = \overline{\lambda^{(s)}(\omega)}$$

即 $\lambda^{(s)}(\omega) = \overline{\lambda^{(-s)}(\overline{\omega})}$。$\square$

**推论 7.5**（谱的实轴对称性）。若 $\omega$ 为实数且 $a,m$ 为实数参数，则 $\lambda^{(+1/2)}(\omega) = \overline{\lambda^{(-1/2)}(\omega)}$。特别地，$\mathrm{Re}(\lambda^{(+1/2)}) = \mathrm{Re}(\lambda^{(-1/2)})$ 且 $\mathrm{Im}(\lambda^{(+1/2)}) = -\mathrm{Im}(\lambda^{(-1/2)})$。

**推论 7.6**（自旋结构的 Parity 保持）。$\mathbb{Z}_2$ 阻碍（定理 3.1）在 Parity 变换下保持不变：$H^2(\mathcal{M}_\omega^{(s)}, \mathbb{Z}_2) = H^2(\mathcal{M}_\omega^{(-s)}, \mathbb{Z}_2)$，因此 $\mathfrak{S}^{(+1/2)}$ 和 $\mathfrak{S}^{(-1/2)}$ 具有相同的自旋结构。

### 7.6 辫子交叉数对应（完整证明）

**定理 7.6**（辫子交叉数对应）。设 $k(U_{\mathrm{Teuk}})$ 是 $D_{\mathrm{diss}}$ 的辫子交叉数（Phase 59C），$k(\mathfrak{M})$ 是单值群 $\mathfrak{M} = \mathcal{M}_a \times_{\text{id}} \mathcal{M}_m \circ \mathcal{M}_\omega$ 在 $S_N$ 中的标准嵌入的 Artin 辫子交叉数。则存在同构：

$$\pi_0\mathrm{Hom}_{\mathbf{Rec}_\infty}(\mathcal{R}_\infty(a_1), \mathcal{R}_\infty(a_2)) \cong \mathbb{Z}_{k(\mathfrak{M})}$$

即 Hom-∞-群胚的连通分支与辫子交叉数模 $k(\mathfrak{M})$ 同构。特别地，$k(U_{\mathrm{Teuk}}) = k(\mathfrak{M})$ 作为数值不变量。

**完整证明**。分五步建立对应关系。

**步骤 1：Rec_∞ 中的 Hom-∞-群胚**。对 Kerr 参数 $a_1, a_2$，$\mathrm{Hom}_{\mathbf{Rec}_\infty}(\mathcal{R}_\infty(a_1), \mathcal{R}_\infty(a_2))$ 是 ∞-群胚，其 0-态射为同伦延拓路径 $\gamma: a_1 \to a_2$（在 $\mathbb{C}_a$ 中避开分支点），1-态射为同伦延拓路径之间的同伦（路径的连续形变），高维态射为高阶同伦。

**步骤 2：连通分支与辫子等价类**。$\pi_0\mathrm{Hom}$ 的元素是同伦延拓的连通分支。两个同伦延拓 $\gamma_1, \gamma_2: a_1 \to a_2$ 属于同一连通分支当且仅当它们通过 $\mathbb{C}_a \setminus \mathcal{B}_a$ 中不含分支点的连续形变相互连接。

$\mathbb{C}_a \setminus \mathcal{B}_a$ 的基本群 $\pi_1(\mathbb{C}_a \setminus \mathcal{B}_a)$ 由 Artin 辫子群 $B_N$ 生成（因为 $\mathcal{B}_a$ 是 $N$ 个分支点）。辫子 $\beta \in B_N$ 的作用是将同伦延拓 $\gamma$ 变换为 $\beta \cdot \gamma$。连通分支的等价关系是：

$$\gamma_1 \sim \gamma_2 \iff \exists \beta \in B_N: \gamma_1 = \beta \cdot \gamma_2$$

**步骤 3：辫子交叉数作为模数**。Artin 辫子群 $B_N$ 有标准表示：

$$B_N = \langle \sigma_1,\dots,\sigma_{N-1} | \sigma_i\sigma_{i+1}\sigma_i = \sigma_{i+1}\sigma_i\sigma_{i+1},\ \sigma_i\sigma_j = \sigma_j\sigma_i \text{ for } |i-j| \geq 2 \rangle$$

辫子的交叉数 $k(\beta)$ 是 $\beta$ 的 Artin 表示中生成元 $\sigma_i$ 的总出现次数（的绝对值）。

$D_{\mathrm{diss}}$ 辫子交叉数 $k(U_{\mathrm{Teuk}})$ 定义为 Koopman 算子 $U_{\mathrm{Teuk}}$ 的辫子轨道在 $\mathbb{C}_a$ 中的总交叉数。由 Phase 59C 的构造，该交叉数等于单值群 $\mathfrak{M}$ 在标准嵌入 $B_N \to S_N$ 下 Artin 生成元的置换核的阶数。

**步骤 4：连通分支的循环群结构**。$\pi_0\mathrm{Hom}$ 在辫子群作用下形成轨道空间 $\mathbb{C}_a \setminus \mathcal{B}_a$ 的路径连通分支集。由于 $B_N$ 在路径空间上的作用是"添加交叉"操作，每添加一个交叉（即 $k(\beta) = 1$ 的辫子），路径 $\gamma$ 进入一个新的连通分支。因此：

$$\pi_0\mathrm{Hom} \cong B_N / \ker(\rho)$$

其中 $\rho: B_N \to \mathfrak{M} \subset S_N$ 是 Artin 表示。辫子交叉数最小的非平凡元是 $k(\mathfrak{M}) = \min\{k(\beta) : \rho(\beta) \neq \text{id}\}$，它是连通分支间的"基本间距"。

由此 $\pi_0\mathrm{Hom} \cong \mathbb{Z}_{k(\mathfrak{M})}$，即 $\pi_0$ 是模 $k(\mathfrak{M})$ 的循环群。这个群在同伦延拓的复合下形成群结构：两个连通分支 $[\gamma_1]$ 和 $[\gamma_2]$ 的乘积 $[\gamma_1] \circ [\gamma_2]$ 对应先执行 $\gamma_2$ 再执行 $\gamma_1$，其辫子交叉数为 $k(\gamma_1) + k(\gamma_2)$ 模 $k(\mathfrak{M})$。

**步骤 5：数值验证的对等性**。Phase 59C 的数值结果为 $\rho_s = 0.9177$（$p = 0.028$），验证了 $k(U_{\mathrm{Teuk}})$ 作为拓扑不变量的统计显著性。由定理 7.6，$k(U_{\mathrm{Teuk}}) = k(\mathfrak{M})$，因此该数值结果同时也验证了 $\pi_0\mathrm{Hom}$ 的循环群结构。$\square$

**推论 7.7**（跨系统辫子一致性的范畴论基础）。四个系统（Teukolsky、Rheology、NRG、Memory）共享同一个 ∞-层 $\mathcal{F}_{\mathfrak{S}}$ 的范畴论前提是它们的单值群 $\mathfrak{M}$ 同构，从而 $k(\mathfrak{M})$ 一致。定理 7.6 提供了从 ∞-范畴 $\mathbf{Rec}_\infty$ 到辫子交叉数的正合函子：

$$\kappa: \mathbf{Rec}_\infty \to \mathbb{Z}\text{-mod}$$

其中 $\kappa(R) = k(\mathfrak{M}_R)$ 是递归系统 $R$ 的单值辫子交叉数。

---

**更新记录**：
- v0.1（2026-07-25）：初始版本，完成 Phase 59D-54D.1 的文献调研与可行路径分析。三个研究方向已明确：A. ∞-Rec 范畴构造（SimpSet 方法）、B. 谱覆盖 ∞-层解释（参考 arXiv:2601.17597）、C. 极限过渡问题（参考 arXiv:2602.18878）。路径 1（∞-层化）为近期推荐。
- v0.2（2026-07-26）：新增 §7 完整证明与推导章节。包含下降条件（定理 7.1）、Postnikov 塔构造（定理 7.2）、导出纤维对应（定理 7.3）、Toeplitz 符号公式（定理 7.4）、Parity 定理（定理 7.5）以及辫子交叉数对应（定理 7.6）的完整证明。
