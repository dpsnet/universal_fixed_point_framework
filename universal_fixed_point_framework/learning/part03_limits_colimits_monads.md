# Part 3：极限、余极限与单子

> 目标：理解 UFPF 中 $\Sigma$-$\mathbf{Rec}$ 可数直和余完备化、单子 $T = \mathcal{L} \circ \iota$、以及 Freyd 伴随定理在 $D \dashv R$ 存在性证明中的作用。

## 3.1 图表与锥

**定义 3.1**（图表）。函子 $J: \mathcal{I} \to \mathcal{C}$ 称为 $\mathcal{C}$ 中的一个图表，$\mathcal{I}$ 是索引范畴。

**定义 3.2**（锥）。图表 $J$ 上的一个锥（cone）由对象 $C \in \mathcal{C}$ 和一族态射 $\{\psi_i: C \to J(i)\}_{i \in \mathcal{I}}$ 组成，使得对任意 $f: i \to j$ 有 $J(f) \circ \psi_i = \psi_j$。

**定义 3.3**（极限）。极限是图表 $J$ 的**终锥**（terminal cone），即对任意其他锥都存在唯一到终锥的态射。

**定义 3.4**（余锥与余极限）。对偶地，余锥由 $\{J(i) \to C\}$ 组成，余极限是初始余锥。

### UFPF 实例：完备性

Paper I 命题 C2.1：$\mathbf{Rec}_D$ 具有显式构造的（余）极限。这是应用 Freyd 伴随定理证明 $D$ 有右伴随的前提之一。

## 3.2 常见极限与余极限

| 概念 | 极限 | 余极限 |
|------|------|--------|
| 空图 | 终止对象 | 初始对象 |
| 离散图 | 积 $\prod_i X_i$ | 余积 $\coprod_i X_i$ |
| 等化子图 | 等化子（equalizer） | 余等化子（coequalizer） |
| 拉回图 | 拉回（pullback） | 推出（pushout） |

### UFPF 实例：可数直和

Paper XIX §7 中，随机噪声系统嵌入 $\Sigma$-$\mathbf{Rec}$，后者是 $\mathbf{Rec}$ 的**可数直和余完备化**（free countable coproduct completion）。对象形如：

$$\bigoplus_{i \in \mathbb{N}} R_i$$

其中每个 $R_i \in \mathbf{Rec}$。这对应于将白噪声分解为可数个局部微型递归系统的统计叠加。

## 3.3 完备性与余完备性

**定义 3.5**（完备范畴）。若范畴对所有小极限存在，称完备。

**定义 3.6**（余完备范畴）。若对所有小余极限存在，称余完备。

### UFPF 实例

- $\mathbf{Set}$ 完备且余完备。
- $\mathbf{Rec}_D$ 在 Paper I 中通过显式构造证明（余）极限存在。
- $\mathbf{Rec}_{\text{id}} \cong \mathbf{Riemann}$ 在纤维积、拉回等操作下封闭（Paper I 附录）。

## 3.4 Freyd 伴随定理

**定理 3.7**（Freyd 伴随函子定理）。设 $G: \mathcal{D} \to \mathcal{C}$ 是函子，若：
- $\mathcal{D}$ 完备
- $G$ 保持极限
- 满足**解集条件**（solution set condition）

则 $G$ 有左伴随。

### UFPF 实例：$D \dashv R$ 的存在性

Paper I 命题 2.4.2：验证 Freyd 伴随定理的前提在 $\mathbf{Rec}_D$ 与 $\mathbf{Sp}$ 之间成立，从而证明右伴随 $R$ 存在（定理 2.4.5）。

解集条件的构造见 Paper I 附录引理 A.3（Yoneda 引理的可表函子版本）：$G_E \cong \mathrm{Hom}_{\mathbf{Rec}_D}(R(E), -)$ 由伴随给出。

## 3.5 单子

**定义 3.8**（单子）。范畴 $\mathcal{C}$ 上的单子 $(T, \eta, \mu)$ 由：
- 自函子 $T: \mathcal{C} \to \mathcal{C}$
- 单位自然变换 $\eta: \mathrm{id}_{\mathcal{C}} \to T$
- 乘法自然变换 $\mu: T^2 \to T$

满足结合律与单位律：

$$\mu \circ T\mu = \mu \circ \mu T$$
$$\mu \circ T\eta = \mathrm{id}_T = \mu \circ \eta T$$

### UFPF 实例：$T = R \circ D$

Paper I 注 2.4.6：复合函子 $T = R \circ D$ 配备单位与乘法构成单子，编码从一般 Koopman 算子的自伴投影到生成元谱的全过程。其 Eilenberg-Moore 范畴 $\mathbf{Rec}^T$ 研究"可被谱化完整描述"的递归系统。

### UFPF 实例：平凡单子

Paper XIX 定理 4.4：复合函子 $T = \mathcal{L} \circ \iota: \mathbf{Rec}_{\text{id}} \to \mathbf{Rec}_{\text{id}}$ 是恒等函子，定义了一个**平凡单子**。其 Eilenberg-Moore 范畴 $\mathbf{Rec}^T$ 同构于 $\mathbf{Rec}_{\text{id}}$。

## 3.6 Kleisli 范畴与 Eilenberg-Moore 范畴

**定义 3.9**（Kleisli 范畴）。单子的 Kleisli 范畴 $\mathcal{C}_T$ 对象为 $\mathcal{C}$ 的对象，态射 $X \to Y$ 为 $\mathcal{C}$ 中 $X \to T(Y)$ 的态射。

**定义 3.10**（Eilenberg-Moore 范畴）。对象为 $T$-代数 $(X, \alpha: T(X) \to X)$，满足代数公理。

### UFPF 实例

Paper I 中单子 $T = R \circ D$ 的 Eilenberg-Moore 范畴 $\mathbf{Rec}^T$ 可用于分类那些"谱化信息足够"的递归系统。这在静默理论中有潜在应用：静默系统可能对应于 $T$-代数结构被破坏的层级。

## 3.7 Comonad 与余单子

对偶地，余单子（comonad）$(G, \varepsilon, \delta)$ 满足：

$$\delta \circ G\delta = \delta \circ \delta G$$
$$\delta \circ G\varepsilon = \mathrm{id}_G = \delta \circ \varepsilon G$$

### UFPF 实例

由伴随 $L \dashv R$ 产生的余单子 $G = L \circ R$ 在 UFPF 中可用于研究谱范畴到递归系统的"分解"操作。Paper I 附录中的 slice category 构造 $W \dashv S$（Wilson 流函子与谱静默函子）可产生相应的单子和余单子结构。

## 3.8 练习

1. 证明初始对象是空图的余极限，终止对象是空图的极限。
2. 在 $\mathbf{Set}$ 中验证积、余积、等化子、余等化子的具体构造。
3. 为什么 Paper XIX 中需要**可数**直和余完备化，而不是有限直和？（提示：白噪声需要无穷多局部 Rec 对象。）
4. 验证 Paper XIX 中 $T = \mathcal{L} \circ \iota$ 是恒等函子，并写出其单位与乘法。
5. 解释 Freyd 伴随定理的三个条件在 $D \dashv R$ 证明中分别对应什么。

## 3.9 关键要点

- **（余）极限**统一了积、和、拉回、推出等构造，是范畴论中"泛性质"的核心体现。
- **余完备化**允许将随机系统、无穷结构嵌入原范畴，是 UFPF 扩展框架的关键技术。
- **Freyd 伴随定理**是证明 $D \dashv R$ 存在性的主要工具。
- **单子**从伴随中提取出自函子结构，$T = R \circ D$ 编码谱化的"闭包操作"。
