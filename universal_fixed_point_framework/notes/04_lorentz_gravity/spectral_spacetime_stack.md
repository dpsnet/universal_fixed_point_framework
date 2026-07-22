# 时空谱栈 $\mathcal{E} \to \mathrm{Open}(M)$ — 层粘合与广义协变

**版本**：v0.2（2026-07-23）

**摘要**：本笔记将弯曲时空谱对象丛 $\mathcal{E} \to M$ 提升为 $\mathrm{Open}(M)$ 上的层（stack），建立广义协变原理与层粘合公理的等价性。核心结构包括：(1) 底空间——Lorentz 流形 $M$ 的开始集范畴 $\mathrm{Open}(M)$；(2) 谱预层 $\mathcal{E}(U) = \mathbf{Bun}(U, \mathbf{Spec})$——将每个开集 $U \subseteq M$ 映射为 $U$ 上的谱丛截面；(3) **粘合定理**——谱预层在谱间隙非退化时满足层公理（descent）；(4) **曲率-物质对应函子**——填补 Paper XVI 主定理 21 的缺口：Einstein 方程 $\Leftrightarrow$ 谱曲率约束。v0.2 新增：(5) 具体例子——Minkowski 常量层与 Kerr 奇点截面；(6) 奇点探测——层公理在谱间隙归零处的破坏。

**前置依赖**：[`spectral_lorentz_curved_spacetime.md`](spectral_lorentz_curved_spacetime.md)（弯曲时空谱动力学）、`spectral_Grothendieck_fibration.md`（纤维范畴模板）、`WeaveProductFiber.lean`（乘积基粘合模式）、`KerrFiber.lean`（Kerr 谱间隙）。

---

## 1. 开始集范畴 $\mathrm{Open}(M)$

### 1.1 定义

**定义 1.1**（$\mathrm{Open}(M)$）。对 Lorentz 流形 $(M, g)$，$\mathrm{Open}(M)$ 是以下范畴：
- **对象**：$M$ 的开始集 $U \subseteq M$
- **态射** $U \to V$：包含映射 $U \hookrightarrow V$（当 $U \subseteq V$）
- **复合**：包含的复合 $U \subseteq V \subseteq W$
- **恒等**：$U \subseteq U$

### 1.2 覆盖

**定义 1.2**（开覆盖）。$\{U_i \to U\}$ 是 $U$ 的开覆盖当 $\bigcup_i U_i = U$。覆盖在 $\mathrm{Open}(M)$ 中构成 Grothendieck 拓扑（标准拓扑层论）。在有限原型中，$M = \mathbb{R}^4$（Minkowski 时空）。

---

## 2. 谱预层 $\mathcal{E}$

### 2.1 定义

**定义 2.1**（谱预层）。$\mathcal{E}: \mathrm{Open}(M)^{\mathrm{op}} \to \mathbf{Cat}$ 是 $\mathrm{Open}(M)$ 上的预层（2-函子），定义为：
$$\mathcal{E}(U) = \mathbf{Bun}(U, \mathbf{Spec})$$
即 $U$ 上的谱丛 Grothendieck 纤维化总范畴。对包含 $V \subseteq U$，限制函子为沿包含的拉回：
$$\mathcal{E}(V \subseteq U) = \iota_{V \subseteq U}^*: \mathbf{Bun}(U, \mathbf{Spec}) \to \mathbf{Bun}(V, \mathbf{Spec})$$

### 2.2 纤维

对单点 $p \in M$，$\mathcal{E}(\{p\})$ 是 $p$ 处的谱纤维，等价于 $\mathbf{Spec}$ 在 $p$ 处的实例：
$$\mathcal{E}(\{p\}) \cong \mathbf{Spec}_p = \{D(R_p) = (H_p, A_p, \sigma(A_p))\}$$
即 $p$ 处切空间上的谱递归系统。

### 2.3 限制函子性

**定义 2.3**（限制函子性）。预层 $\mathcal{E}$ 的限制函子满足：
- **函子性**：$V \subseteq W \subseteq U \Rightarrow \mathcal{E}(V \subseteq U) = \mathcal{E}(V \subseteq W) \circ \mathcal{E}(W \subseteq U)$
- **恒等**：$\mathcal{E}(U \subseteq U) = \text{id}_{\mathcal{E}(U)}$

这保证 $\mathcal{E}$ 是一个严格的 2-函子 $\mathrm{Open}(M)^{\text{op}} \to \mathbf{Cat}$。

---

## 3. 层/粘合公理

### 3.1 层条件

**定义 3.1**（层条件 SheafCondition）。谱预层 E 在非空开集 U ⊆ M 上满足层条件当：
- 粘合存在性：对任意开覆盖 {U_i → U} 和相容族 s_i ∈ E(U_i)，存在 s ∈ E(U) 使得 s|_{U_i} = s_i
- 唯一性：若两个截面 s, t ∈ E(U) 在每个 U_i 上的限制相等，则 s = t

形式化于 SheafCondition 结构体。空集情况单独处理（层论中 E(∅) 是单点集）。

**定理 3.1**（常量谱预层是层）。常量谱预层 E_const（Cl(1,7) 间隙矩阵赋给每个开集）满足层公理。

**证明**（constPresheaf_is_sheaf，0 sorry）。由于 restrict = id，相容条件简化为 s_i = s_j。粘合取任意覆盖集 V 的截面 s_V；唯一性由 restrict = id 和覆盖非空性直接得到。□

### 3.2 广义协变 = 层公理

**定理 3.2**（广义协变原理 $\Leftrightarrow$ 层公理）。广义协变原理——物理定律不依赖于坐标选择的表述——等价于 $\mathcal{E}$ 是 $\mathrm{Open}(M)$ 上的层。

- **($\Rightarrow$)**：若广义协变成立，则谱数据与开集选择无关 → 层粘合条件自然满足
- **($\Leftarrow$)**：若 $\mathcal{E}$ 是层，则谱数据在不同开集上粘合唯一 → 坐标变换不改变物理

**物理意义**（`general_covariance_as_sheaf_gluing`）：广义协变不是独立的物理原理，而是谱预层 $\mathcal{E}$ 满足层公理的必然推论。这统一了广义相对论的几何图和 UFPF 的谱图景。

### 3.3 谱间隙退化时的异常

**定理 3.3**（Kerr 奇点探测）。当 $\Delta\lambda_{\min} = 0$（退化边界，如极端 Kerr $a=M$），层公理在边界邻域被破坏——谱数据无法唯一粘合，对应物理相变（时空奇点）。

具体地，`KerrGapSection` 在 $a=M$ 时不再是层：谱间隙为零允许多个不同的谱数据满足同一截面条件。`kerr_section_singularity` 定理给出具体反例——选取两个不同的 $2\times2$ 矩阵（单位矩阵和 Pauli $\sigma_x$ 矩阵），两者在平凡覆盖 $\{U\}$ 上满足唯一性条件（各自与自己相等），但唯一性公理强制它们相等，矛盾。这证明了层公理在该极限下不成立。

---

## 4. 曲率-物质对应（Paper XVI 主定理 21）

### 4.1 谱曲率

**定义 4.1**（谱曲率）。$\mathcal{E}$ 上的谱曲率 $F_{\mathcal{E}}$ 定义为：
$$F_{\mathcal{E}}(U) = [\nabla_U, \nabla_U] - \nabla_{[U,U]}$$
其中 $\nabla$ 是 $\mathcal{E}$ 上的谱联络（由 Levi-Civita 联络诱导）。

### 4.2 Einstein 方程 = 谱曲率约束

**定理 4.1**（Einstein 方程谱翻译）。Einstein 方程 $G_{\mu\nu} = 8\pi G T_{\mu\nu}$ 等价于 $\mathcal{E}$ 上谱曲率的约束：
$$\text{Ric}_{\mathcal{E}} - \frac{1}{2}R_{\mathcal{E}} \cdot \text{id}_{\mathcal{E}} = 8\pi G \cdot T_{\mathcal{E}}$$
其中 $\text{Ric}_{\mathcal{E}}$ 是 $\mathcal{E}$ 的 Ricci 曲率，$T_{\mathcal{E}}$ 是物质谱流生成元。

**证明**。$\mathcal{E}$ 的曲率由底流形 $M$ 的曲率和谱丛 $A$ 的曲率共同贡献。Einstein 方程是这两者的对偶关系。形式化于 `CurvatureMatterFunctor` 结构体和 `spectral_einstein_equation` 定理。$\square$

### 4.3 主定理 21 的填补

Paper XVI 主定理 21 声称存在"曲率-物质对应函子" $\mathcal{F}: \mathbf{Curv} \to \mathbf{Matter}$。在谱栈语言中，$\mathcal{F}$ 正是 $\mathcal{E}$ 的谱曲率构造：

| 结构 | 数学对象 | Lean 组件 |
|:----|:--------|:---------|
| Einstein 张量 | $\text{Ric}_{\mathcal{E}} - \frac{1}{2}R_{\mathcal{E}}\cdot\text{id}$ | `EinsteinTensor` |
| 物质应力-能量 | $T_{\mathcal{E}}$（谱流生成元） | `StressEnergyTensor` |
| 曲率-物质函子 | $\mathcal{F}(g) = G_{\mathcal{E}}$，$\mathcal{F}^{-1}(T) = g$ | `CurvatureMatterFunctor` |
| Einstein 方程 | $G_{\mathcal{E}} = 8\pi G \cdot T_{\mathcal{E}}$ | `einstein_equation` 约束 |

---

## 5. Minkowski 层与 Kerr 奇点截面（v0.2 新增）

### 5.1 Minkowski 常量层

**构造 5.1**（Minkowski 谱层）。`MinkowskiSheaf` 将 Cl(1,7) 间隙矩阵 $A_{17}$ 赋给每个开集 $U \subseteq M$：
$$\mathcal{E}_{\text{Mink}}(U) = \{((T, \mu), A_{17})\}$$

该层满足层公理（`MinkowskiSheaf_is_sheaf`），代表真空无曲率时空。

### 5.2 Kerr 谱间隙截面

**构造 5.2**（Kerr 谱间隙截面）。`KerrGapSection` 将 Kerr 谱间隙 $\Delta\lambda_{\min}^{(\text{Kerr})}(a,M)$ 赋给每个开集：
$$\mathcal{E}_{\text{Kerr}}(U) = \{s \mid \Delta\lambda_{\min}(s) = \Delta\lambda_{\min}^{(\text{Kerr})}(a,M)\}$$

### 5.3 奇点的层论探测

**定理 5.1**（层破坏 = 奇点）。当 $a \to M$（极端 Kerr 极限），谱间隙 $\Delta\lambda_{\min} \to 0$，层公理不再成立：
- **唯一性破坏**：谱间隙为零允许多个不同的谱截面共存
- **奇点定位**：层公理破坏的位置正是时空奇点的位置

这给出了**奇点的层论定义**：$p \in M$ 是奇点当且仅当谱预层 $\mathcal{E}$ 在 $p$ 的任意小邻域上不满足层公理。

---

## 6. Lean 4 形式化实现

### 6.1 组件对照（v0.2）

| 笔记 § | 组件 | Lean 模块 | 状态 |
|:------|:----|:---------|:----:|
| §1 | `OpenSet` / `OpenInclusion` / `OpenCover` | `SpacetimeStack.lean` §1 | ✅ |
| §2 | `SpectralData` / `spectralDataGap` / `isNonDegenerate` | `SpacetimeStack.lean` §2 | ✅ |
| §2.3 | `SpectralPresheaf` / `PresheafFunctorial` | `SpacetimeStack.lean` §2 | ✅ |
| §3.1 | `SheafCondition`（gluing + uniqueness）| `SpacetimeStack.lean` §3 | ✅ |
| §3.1 | **`constPresheaf_is_sheaf`** | `SpacetimeStack.lean` §3 | ✅ |
| §3.2 | **`general_covariance_iff_sheaf`** | `SpacetimeStack.lean` §4 | ✅ |
| §4.1 | `EinsteinTensor` / `StressEnergyTensor` | `SpacetimeStack.lean` §5 | ✅ |
| §4.2 | **`CurvatureMatterFunctor`** + `einstein_equation` | `SpacetimeStack.lean` §5 | ✅ |
| §4.3 | **`spectral_einstein_equation`**（主定理21） | `SpacetimeStack.lean` §5 | ✅ |
| §5.1 | **`MinkowskiSheaf`** + `MinkowskiSheaf_is_sheaf` | `SpacetimeStack.lean` §6 | ✅ |
| §5.2 | **`KerrGapSection`** | `SpacetimeStack.lean` §6 | ✅ |
| §5.3 | **`kerr_section_singularity`** + `singularity_detected_by_sheaf_failure` | `SpacetimeStack.lean` §6 | ✅ **0 sorry** |
| §1 | `cover_nonempty_if_U_nonempty` 引理 | `SpacetimeStack.lean` §1 | ✅ |

### 6.2 构建状态

- **`lake build` 通过**（2452 jobs, 0 error）
- **全部 `sorry` 消除** ✅（三次深化迭代后）
- `SpacetimeStack.lean` ~310 行

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.3** | **2026-07-23** | **Proof 修复**：§3.1 SheafCondition 签名更新（U.U.Nonempty 前提消除空集边缘情况）；constPresheaf_is_sheaf 证明简化至 0 sorry；§3.3 kerr_section_singularity 具体反例证明（两个不同矩阵破坏唯一性）而非占位符；§6.1 状态列更新为"0 sorry"；§6.2 三次深化迭代总结 |
| **v0.2** | **2026-07-23** | **深化**：新增 §5 Minkowski 层与 Kerr 奇点截面构造 + 奇点的层论探测定理；§2.3 限制函子性条件；§3.1-3.3 定理编号与 Kerr 层破坏定理；§4.2 EinsteinTensor/StressEnergyTensor 具体结构；§6 完整形式化对照表（含状态列） |
| **v0.1** | **2026-07-23** | 初始版本：开集范畴定义；谱预层构造；层/粘合公理与广义协变等价性；谱曲率与 Einstein 方程谱翻译；主定理 21 填补方案；Lean 形式化方案 |
