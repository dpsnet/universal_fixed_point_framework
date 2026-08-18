# Part 1：范畴论基础

> 目标：理解 UFPF 中 $\mathbf{Rec}$、$\mathbf{Sp}$、$\mathbf{Rec}_{\text{id}}$、$\Sigma$-$\mathbf{Rec}$ 等范畴的定义方式，能够判断一个构造是否构成范畴。

## 1.1 什么是范畴

**定义 1.1**（范畴）。一个范畴 $\mathcal{C}$ 由以下数据组成：

1. **对象类** $\mathrm{Ob}(\mathcal{C})$：研究对象的集合（通常是大类，避免 Russell 悖论）。
2. **态射类**：对任意两个对象 $X, Y \in \mathrm{Ob}(\mathcal{C})$，给定一个态射集合（或类）$\mathrm{Hom}_{\mathcal{C}}(X, Y)$。
3. **复合运算**：对任意 $f: X \to Y$ 与 $g: Y \to Z$，存在复合 $g \circ f: X \to Z$。
4. **单位态射**：每个对象 $X$ 有恒等态射 $\mathrm{id}_X: X \to X$。

满足：
- **结合律**：$h \circ (g \circ f) = (h \circ g) \circ f$
- **单位律**：$f \circ \mathrm{id}_X = f = \mathrm{id}_Y \circ f$

### UFPF 实例：递归系统范畴 $\mathbf{Rec}$

在 Paper I §2.1 中，$\mathbf{Rec}$ 的对象是四元组：

$$R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$$

其中：
- $\mathcal{S}_R$：状态空间
- $\Phi_R: \mathcal{S}_R \to \mathcal{S}_R$：全局自相似映射
- $\mathcal{T}_R \subseteq \mathbb{R}_{\ge 0}$：迭代半群
- $\mathcal{M}_R$：不变测度

态射是保持递归结构的映射。这正是一个范畴：对象有明确定义，态射有复合，恒等态射是恒等映射。

### UFPF 实例：谱范畴 $\mathbf{Sp}$

$\mathbf{Sp}$ 的对象是三元组：

$$E = (\mathcal{H}, A, \sigma(A))$$

其中 $\mathcal{H}$ 是 Hilbert 空间，$A$ 是自伴算子，$\sigma(A)$ 是谱。态射是保持谱结构的算子映射。

**思考题**：为什么 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 要将定义域限制为宽子范畴 $\mathbf{Rec}_D \subset \mathbf{Rec}$？（提示：并非所有递归系统都有良定义的谱化像。）

## 1.2 同构与等价

**定义 1.2**（同构）。态射 $f: X \to Y$ 称为同构，若存在 $g: Y \to X$ 使得：

$$g \circ f = \mathrm{id}_X, \quad f \circ g = \mathrm{id}_Y$$

**定义 1.3**（等价）。范畴 $\mathcal{C}$ 与 $\mathcal{D}$ 等价，若存在函子 $F: \mathcal{C} \to \mathcal{D}$ 与 $G: \mathcal{D} \to \mathcal{C}$ 使得 $G \circ F \cong \mathrm{id}_{\mathcal{C}}$ 且 $F \circ G \cong \mathrm{id}_{\mathcal{D}}$（自然同构）。

### UFPF 实例

Paper XIX 定理 3.3：$\mathbf{Rec}_{\text{id}} \cong \mathbf{Riemann}$（紧致 Riemann 流形范畴的等价）。这意味着通过恒等延拓，静态拓扑对象与紧致 Riemann 流形范畴没有范畴论差异。

## 1.3 子范畴与宽子范畴

**定义 1.4**（子范畴）。$\mathcal{D}$ 是 $\mathcal{C}$ 的子范畴，若：
- $\mathrm{Ob}(\mathcal{D}) \subseteq \mathrm{Ob}(\mathcal{C})$
- $\mathrm{Hom}_{\mathcal{D}}(X, Y) \subseteq \mathrm{Hom}_{\mathcal{C}}(X, Y)$
- 复合与单位在 $\mathcal{D}$ 中保持

**定义 1.5**（宽子范畴）。若子范畴保持全部对象，仅减少态射，则称为宽子范畴（wide subcategory）。

### UFPF 实例

- $\mathbf{Rec}_D \subset \mathbf{Rec}$：宽子范畴，对象为全部递归系统，但仅保留那些谱化像良定义的态射。
- $\mathbf{Rec}_{\text{id}} \subset \mathbf{Rec}$：全子范畴（full subcategory），对象为恒等延拓的静态流形，态射与 $\mathbf{Rec}$ 中相同。

## 1.4 对偶范畴与积范畴

**定义 1.6**（对偶范畴）。$\mathcal{C}^{\mathrm{op}}$ 与 $\mathcal{C}$ 有相同对象，但态射方向反转。

**定义 1.7**（积范畴）。$\mathcal{C} \times \mathcal{D}$ 的对象为 $(c, d)$，态射为 $(f, g)$。

### UFPF 实例

层论中的预层定义为反变函子 $F: \mathcal{C}^{\mathrm{op}} \to \mathbf{Set}$。在 Paper XVI 中，谱预层是 2-函子：

$$\mathcal{E}: \mathrm{Open}(M)^{\mathrm{op}} \to \mathbf{Cat}$$

这里的 $\mathrm{Open}(M)^{\mathrm{op}}$ 就是拓扑空间开集范畴的对偶范畴。

## 1.5 初始对象与终止对象

**定义 1.8**（初始/终止对象）。对象 $I$ 是初始的，若对任意 $X$ 存在唯一 $I \to X$。对象 $T$ 是终止的，若对任意 $X$ 存在唯一 $X \to T$。

**性质**：初始对象与终止对象在同构意义下唯一。

### 与极限的关系

初始对象实际上是空图（empty diagram）的极限，终止对象是空图的余极限。这将在 [part03_limits_colimits_monads.md](part03_limits_colimits_monads.md) 中进一步展开。

## 1.6 练习

1. 验证 $\mathbf{Set}$（集合范畴）、$\mathbf{Grp}$（群范畴）、$\mathbf{Vect}_{\mathbb{C}}$（复向量空间范畴）满足范畴公理。
2. 证明 Paper I 中定义的 $\mathbf{Rec}$ 满足单位律与结合律。
3. 为什么 $\mathbf{Rec}_{\text{id}}$ 是 $\mathbf{Rec}$ 的**全子范畴**而非宽子范畴？
4. 若 $F: \mathcal{C}^{\mathrm{op}} \to \mathbf{Set}$ 是预层，解释为什么 $F$ 在反向箭头上保持复合。

## 1.7 关键要点

- 范畴论研究的是**结构及其保持映射**，而非具体对象的内部构成。
- UFPF 的核心范畴 $\mathbf{Rec}$ 与 $\mathbf{Sp}$ 分别编码"递归动力学"与"谱数据"两种世界观。
- 宽子范畴与全子范畴是限制定义域的两种基本方式，在 UFPF 中均有重要应用。
