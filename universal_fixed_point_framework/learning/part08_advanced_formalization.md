# Part 8：形式化仓库中的高级范畴结构

> 目标：理解 UFPF 形式化仓库 `UFPFormalization` 中超出论文主线的范畴论构造，包括幺半范畴、对偶、表示桥接与同伦方法。

## 8.1 幺半范畴与辫子结构

**定义 8.1**（幺半范畴）。范畴 $\mathcal{C}$ 配备：
- 张量积函子 $\otimes: \mathcal{C} \times \mathcal{C} \to \mathcal{C}$
- 单位对象 $I \in \mathcal{C}$
- 结合约束 $\alpha_{X,Y,Z}: (X \otimes Y) \otimes Z \cong X \otimes (Y \otimes Z)$
- 左右单位约束 $\lambda_X: I \otimes X \cong X$，$\rho_X: X \otimes I \cong X$

满足五边形方程与三角形方程。

**定义 8.2**（辫子幺半范畴）。幺半范畴配备自然同构（辫子）

$$\beta_{X,Y}: X \otimes Y \to Y \otimes X$$

满足六边形方程。

### UFPF 实例：`Braided.lean`

Paper I §2.5 定义 2.11a：$\mathbf{Rec}$ 上定义张量积为状态空间的 Cartesian 积，演化规则为分量乘积：

$$(R_1 \otimes R_2).\text{step}(x, y) = (R_1.\text{step}(x), R_2.\text{step}(y))$$

辫子由因子交换给出，交换数 $k$ 编码复谱辐角的缠绕数。`Braided.lean` 形式化了这一结构，并验证积范畴中的投影、提升等泛性质。

## 8.2 范畴等价与对偶

**定义 8.3**（范畴等价）。函子 $F: \mathcal{C} \to \mathcal{D}$ 与 $G: \mathcal{D} \to \mathcal{C}$ 构成等价，若 $G \circ F \cong \mathrm{id}_{\mathcal{C}}$ 且 $F \circ G \cong \mathrm{id}_{\mathcal{D}}$。

**定义 8.4**（对偶性）。对偶是范畴之间的反变等价（contravariant equivalence）。典型例子：
- Pontryagin 对偶：局部紧 Abel 群 ↔ 其对偶群
- Gelfand 对偶：交换 C*-代数 ↔ 紧致 Hausdorff 空间

### UFPF 实例：`SpectralEquivalence.lean`

Paper III §3：递归系统 $R_1, R_2$ 称为谱等价的，若 $D(R_1) \cong D(R_2)$ 在 $\mathbf{Sp}$ 中。形式化中定义：

```lean
def spectralEquivalence (R₁ R₂ : RecObj) : Prop :=
  Nonempty (DFunctor.obj R₁ ≅ DFunctor.obj R₂)
```

并验证其反射性、对称性、传递性。这是**由范畴同构诱导的等价关系**的标准构造。

### UFPF 实例：`GelfandDuality.lean`

Paper XIX 开放问题 #2：$D^{\text{id}}(M) = (\mathcal{H}_M, \Delta_M, \sigma(\Delta_M))$ 与 Gelfand 对偶的对应。

Gelfand 对偶：$C(M) \;\leftrightarrow\; M$（交换 C*-代数 ↔ 紧致 Hausdorff 空间）

UFPF 的 $D^{\text{id}}$：$\mathcal{H}_M \;\leftrightarrow\; \sigma(\Delta_M)$（Hilbert 空间 ↔ Laplace 谱）

`GelfandDuality.lean` 将 $D^{\text{id}}$ 定位为 Gelfand 对偶的"谱几何类比"：前者重建拓扑空间，后者重建 Laplace 谱。

## 8.3 表示范畴与几何范畴

**定义 8.5**（表示）。群/代数 $G$ 在向量空间 $V$ 上的表示是态射 $\rho: G \to \mathrm{End}(V)$。表示构成范畴，对象为 $(V, \rho)$，态射为等变线性映射。

**定义 8.6**（几何范畴）。几何对象（如流形、概形、谱三元组）及其保持结构的映射构成范畴。

### UFPF 实例：`CategoryRepBridge.lean`

UFPF 框架需要在范畴语言与表示论语言之间建立桥接：
- 递归系统 $R$ 的 Koopman 算子 $U_R$ 是 $\mathcal{S}_R$ 上函数的"表示"
- 谱化函子 $D$ 将该表示翻译为谱数据
- 表示论的不可约分解 ↔ 谱范畴中的直和分解

`CategoryRepBridge.lean` 形式化这一桥接，使 UFPF 能够利用表示论工具（特征标、不可约分解）分析递归系统。

### UFPF 实例：`CategoryGeometry.lean`

将 UFPF 中的几何对象（紧致流形、Clifford 丛、谱三元组）组织为范畴，建立：
- 几何对象 ↔ 谱对象 的字典
- 几何态射 ↔ 谱交织条件的对应
- 曲率、联络、规范场在范畴论中的表达

这是 Paper I §6 和 Paper XVI 中几何-谱对应的形式化支撑。

## 8.4 同伦与谱流同伦不变性

**定义 8.7**（同伦）。两个连续映射 $f, g: X \to Y$ 同伦，若存在连续映射 $H: X \times [0,1] \to Y$ 使得 $H(-,0) = f$，$H(-,1) = g$。

**定义 8.8**（谱流）。一族自伴算子 $\{A_t\}_{t \in [0,1]}$ 的谱流是特征值穿过零点时符号变化的总数。

### UFPF 实例：`SpectralFlowHomotopy.lean`

Paper V / Paper I §3：谱流方程

$$\frac{d}{dt} A_t = [G, A_t]$$

的解 $A_t$ 可视为算子空间中的路径。`SpectralFlowHomotopy.lean` 形式化：
- 两条同伦的谱流路径给出相同的谱不变量
- 辫子交叉数作为同伦不变量
- 耗散系统中的非自伴谱流同伦类

这支撑了 Paper I 中"辫子静默"作为拓扑缠绕推广的概念。

## 8.5 函子律验证的方法论

在 Lean 4 中验证一个构造是函子，通常需要证明：

```lean
map_id : F.map (𝟙 X) = 𝟙 (F.obj X)
map_comp : F.map (f ≫ g) = F.map f ≫ F.map g
```

### UFPF 实例：`PhotonTopologyFunctor.lean` / `PhotonTopologyFunctorLaws.lean`

Paper XLIV 将光子拓扑结构构造为函子。形式化中：
- 定义 `PhotonTopologyFunctor` 的对象映射和态射映射
- 在 `PhotonTopologyFunctorLaws.lean` 中验证 `map_id` 与 `map_comp`
- 这是"把物理结构范畴化"的标准流程

### UFPF 实例：`DecursionFunctor.lean`

"反递归"函子 $D_{\text{dec}}$ 将谱对象映射回递归系统。形式化验证其函子律，是 $D \dashv R$ 伴随构造的组件之一。

## 8.6 其他高级构造速览

| 文件 | 概念 | 说明 |
|------|------|------|
| `HigherRecCategory.lean` / `HigherSpCategory.lean` | 2-范畴 | Rec/Sp 的 2-范畴提升 |
| `InfinityCategory.lean` / `AInfinityAlgebra.lean` | ∞-范畴 / A∞ 代数 | 高阶括号与同伦结构 |
| `RecInfinity.lean` / `SpecInfinity.lean` | 无穷维版本 | Rec/Sp 的 ∞-范畴/泛函分析扩展 |
| `SpacetimeStack.lean` | 栈 | 时空上的谱栈 |
| `EFTCodomainFiber.lean` | Slice 范畴 / 纤维化 | 有效场论余域纤维 |

## 8.7 练习

### Level 4：形式化专项

1. 在 `Braided.lean` 的框架下，验证 $\mathbf{Rec}$ 中两个递归系统张量积的结合约束满足五边形方程。
2. 解释 `SpectralEquivalence.lean` 中为什么用 `Nonempty (D(R₁) ≅ D(R₂))` 而不是直接定义 `D(R₁) = D(R₂)` 来刻画谱等价。
3. 比较 Gelfand 对偶与 $D^{\text{id}}$：两者分别"重建"了什么对象？UFPF 的谱几何方法比 Gelfand 对偶少了什么信息？
4. 在 `CategoryRepBridge.lean` 的视角下，Koopman 算子 $U_R$ 是哪种代数/群的表示？
5. 写出验证一个函子律所需的两个等式，并说明 `PhotonTopologyFunctorLaws.lean` 中如何证明它们。

## 8.8 关键要点

- **幺半范畴/辫子结构**使 UFPF 能够讨论递归系统的组合与交换对称性。
- **范畴等价/对偶**是 UFPF 与经典数学（Gelfand 对偶、谱等价）建立联系的语言。
- **表示桥接**让 Koopman 算子、谱分解等工具在范畴论下统一。
- **同伦方法**为谱流、辫子静默、耗散系统提供拓扑不变量。
- **函子律验证**是形式化工作中最基础、最常见的任务。
