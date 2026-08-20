# Part 4：层、Grothendieck 纤维化与栈

> 目标：理解 UFPF 中谱丛、谱预层、Grothendieck 纤维化的构造，能够复述 Paper XXI 中 Temp/RG/Noise 等参数谱丛的定义。

## 问题动机

UFPF 中的物理参数（温度、能标、噪声强度、黑洞参数）会变化，因此我们需要研究“一族谱对象随参数变化”的结构。同时，谱数据往往先在局部开集上定义，再被粘合为全局对象。层的语言让我们把局部信息粘合为全局信息；Grothendieck 纤维化则让我们把一族范畴整体地参数化在一个基范畴上。

本章要解决的问题是：**当物理参数变化时，如何一致地描述一族对象？如何用局部数据恢复全局结构？**

## 4.1 预层与层

**定义 4.1**（预层）。拓扑空间 $M$ 上的预层是反变函子：

$$\mathcal{F}: \mathrm{Open}(M)^{\mathrm{op}} \to \mathbf{Set}$$

即对每个开集 $U$ 赋予集合 $\mathcal{F}(U)$，对包含 $V \subseteq U$ 赋予**限制映射**$\rho_{UV}: \mathcal{F}(U) \to \mathcal{F}(V)$。

**定义 4.2**（层）。预层 $\mathcal{F}$ 是层，若满足：
- **局域性**：若 $\{U_i\}$ 覆盖 $U$，且 $s, t \in \mathcal{F}(U)$ 在每个 $U_i$ 上限制相等，则 $s = t$
- **粘合性**：若在 $U_i$ 上给定相容的局部截面 $s_i$，则存在全局截面 $s \in \mathcal{F}(U)$ 使其限制到每个 $U_i$ 为 $s_i$

### UFPF 实例：谱预层

Paper XVI 定义 10.3：谱预层是 2-函子：

$$\mathcal{E}: \mathrm{Open}(M)^{\mathrm{op}} \to \mathbf{Cat}$$

将每个开集 $U \subseteq M$ 映为 $U$ 上的谱丛 Grothendieck 纤维化总范畴。限制函子性由定义 10.5 给出。

Paper XVI 定理 10.1：常量谱预层是层。定理 10.2：**广义协变原理等价于层公理**。

## 4.2 茎与层化

**定义 4.3**（茎）。预层在点 $p \in M$ 处的茎为：

$$\mathcal{F}_p = \varinjlim_{U \ni p} \mathcal{F}(U)$$

即所有含 $p$ 开集上截面的正向极限。

**定义 4.4**（层化）。任意预层可通过层化函子 $a: \mathbf{PSh}(M) \to \mathbf{Sh}(M)$ 构造其伴随层。

### UFPF 实例

Paper XVI 定义 10.10：奇点 = 层公理被破坏的位置。在切触条件下，谱预层自动满足层公理（命题 10.15）。这为 UFPF 中的时空奇点提供了层论刻画。

## 4.3 Grothendieck 纤维化

**定义 4.5**（Cartesian 提升）。函子 $\pi: \mathcal{E} \to \mathcal{B}$ 称为 Grothendieck 纤维化，若对任意 $e \in \mathcal{E}$ 和 $\mathcal{B}$ 中态射 $f: b \to \pi(e)$，存在 $\mathcal{E}$ 中态射 $\tilde{f}: e' \to e$（称为 Cartesian 提升）满足：
- $\pi(\tilde{f}) = f$
- 万有性质：任何其他提升唯一分解通过 $\tilde{f}$

> **术语说明**：UFPF 此前使用 **"Cartan 提升"**，现已统一为标准术语 **"Cartesian 提升"**（对应标准范畴论文献中的 *Cartesian lifting*）。

**定义 4.6**（分裂纤维化）。若 Cartesian 提升的选择可规范化为函子（恒等保持、复合保持），则称分裂 Grothendieck 纤维化。

### UFPF 实例：谱丛总范畴

Paper XXI 定义 2.1-2.2：Grothendieck 纤维化是"一族对象随参数变化"的严格数学语言。UFPF 中所有物理实例均为分裂纤维化：

- **Temp**：温度参数谱丛 $\pi_T: \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \to \mathbf{Temp}$
- **RG**：能标参数谱丛 $\pi_\mu: \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp}) \to \mathbf{RG}$
- **Noise**：噪声强度谱丛 $\pi_\eta$
- **Sig**：Clifford 签名谱丛
- **Kerr**：黑洞参数谱丛
- **Flt**：味扇区谱丛

## 4.3a Cartesian 提升显式例子：参数谱丛

下面给出一个与 UFPF 谱丛直接对应的、可手算验证的 Cartesian 提升例子。它既展示 Grothendieck 纤维化的核心机制，也解释为什么 Paper XXI 中的 Temp/RG/Noise 等谱丛都是**分裂**的。

### 基范畴与总范畴

取温度参数空间为偏序集

$$\mathbf{Temp} = (\mathbb R, \le),$$

其中对象是一个温度值 $T \in \mathbb R$，当且仅当 $T' \le T$ 时存在唯一态射 $T' \to T$。

总范畴 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ 的对象为

$$(T, E_T), \qquad T \in \mathbb R, \; E_T \in \mathbf{Sp}.$$

态射 $(T', E_{T'}) \to (T, E_T)$ 由满足 $T' \le T$ 的参数映射 $T' \to T$ 连同谱范畴中的态射 $u: E_{T'} \to E_T$ 组成。投影函子为

$$\pi(T, E_T) = T.$$

直观上，总范畴把“每个温度点处的谱对象”粘合成一个参数化谱族。

### Cartesian 提升的构造

设给定：

- 基范畴中一个态射 $f: T' \to T$（即 $T' \le T$）；
- 总范畴中一个位于 $T$ 的对象 $e = (T, E_T)$。

我们要构造 $f$ 的 **Cartesian 提升**

$$\tilde f: e' \to e, \qquad e' = (T', E_{T'}),$$

使得 $\pi(\tilde f) = f$。

在这个例子里，谱数据不随温度改变而“额外扭曲”，于是取

$$E_{T'} = E_T,$$

并让谱部分的态射为恒等映射 $\mathrm{id}_{E_T}$。因此提升为

$$\tilde f = (f, \mathrm{id}_{E_T}): (T', E_T) \longrightarrow (T, E_T).$$

投影显然满足

$$\pi(\tilde f) = T' \to T = f.$$

### 万有性质验证

Cartesian 提升的核心要求是下面的万有性质：对任意对象 $e'' = (T'', E_{T''})$ 和任意提升 $h: e'' \to e$ 且 $\pi(h)$ 可分解为 $T'' \le T' \le T$，存在唯一的 $g: e'' \to e'$ 使得下图交换：

```
e'' --g--> e'
 |        |
 |        | f~
 v        v
 e ====== e
```

更精确地，在基范畴中有 $T'' \le T' \le T$，于是 $h$ 的谱部分是一个态射 $u: E_{T''} \to E_T$。我们需要找到唯一的

$$g = (T'' \to T', v): e'' \to e'$$

使得 $\tilde f \circ g = h$。

- 基范畴部分：$T'' \le T'$ 已经给定，因此存在唯一的基映射；复合 $T' \le T$ 后得到 $T'' \le T$，与 $h$ 的基部分一致。
- 谱范畴部分：要求

  $$\mathrm{id}_{E_T} \circ v = u.$$

  因此唯一取 $v = u: E_{T''} \to E_T = E_{T'}$ 即可。

这就证明了 $\tilde f$ 是 Cartesian 提升。

### 为什么这是“分裂”的

在上面的构造中，我们实际上选择了一个**严格 cleavage**：

- 恒等态射 $T \to T$ 的提升取为恒等态射 $\mathrm{id}_{(T,E_T)}$；
- 复合 $T'' \le T' \le T$ 的提升取为相应恒等映射的复合，仍然是恒等。

因此这个 Grothendieck 纤维化是**分裂的**，符合 Paper XXI 中“UFPF 物理实例均为分裂纤维化”的断言。

### 与 UFPF 实例的对应

这个例子可直接迁移到 Paper XXI 中的具体谱丛：

- **Temp**：温度参数谱丛。$T \in \mathbb R$ 替换为温度区间，纤维 $E_T$ 是该温度下的谱对象。
- **RG**：能标参数谱丛。参数 $\mu$ 代替温度，重正化群流 $d/d\mu$ 给出基范畴中的态射；Cartesian 提升把谱对象沿能标方向“平行移动”。
- **Noise**：噪声强度谱丛。参数 $\eta$ 控制噪声大小；Cartesian 提升保持谱结构，仅改变噪声参数标签。

在所有这些情形中，Cartesian 提升的谱部分都可以规范地取为恒等（或一个由参数变化诱导的显式谱同构），从而得到分裂纤维化。

> **自检要点**。判断一个提升是否是 Cartesian，关键是验证万有性质：给定任何“先走基映射再走提升”的分解可能，纤维分量是否唯一确定。在上述例子中，由于谱部分取恒等，唯一性自动成立；这正是分裂纤维化的典型特征。

## 4.4 纤维与截面

**定义 4.7**（纤维）。对 $b \in \mathcal{B}$，纤维 $\mathcal{E}_b$ 是 $\pi^{-1}(b)$ 构成的子范畴。

**定义 4.8**（截面）。截面是函子 $\sigma: \mathcal{B} \to \mathcal{E}$ 使得 $\pi \circ \sigma = \mathrm{id}_{\mathcal{B}}$。

### UFPF 实例

Paper XXI §1.1：物理系统是参数空间上的谱族。截面编码物理可观测量作为参数的函数，如 $T_c$、$\Delta\lambda_{\min}$、QNM 频率等。

Paper XXII §2：Cartesian 提升的谱流形式为：

$$\frac{d}{d\xi} A = [G_\xi, A] - \gamma_\xi \cdot \Delta_{\text{spec}} A$$

这是将基空间参数变化提升为谱数据演化的统一物理载体。

## 4.5 谱栈

**定义 4.9**（栈）。栈是满足下降条件（descent condition）的层取值 2-范畴（或更一般地，取值于某种高阶范畴）。

### UFPF 实例

Paper XXI §6：谱栈是谱丛在开集范畴上的层论推广。$\mathrm{Open}(M)$ 上的谱栈允许在重叠开集上粘合谱丛数据，处理弯曲时空中的局域-整体关系。

## 4.6 谱覆盖与层

Paper XXVII（Leaver 谱覆盖理论）将 Kerr 黑洞三参数空间 $(a, m, \omega)$ 上的三对角矩阵族构造为**三参数谱覆盖** $\mathfrak{S}$。这是 Grothendieck 纤维化在复参数空间上的实例：

- 基空间：$(a, m)$ 参数平面
- 纤维：固定 $(a, m)$ 处的谱集（$\omega$ 的 $N$ 叶覆盖）
- 单值群：$\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$

## 4.9 程序员与形式化视角（选读）

本节把层论、Grothendieck 纤维化与谱丛翻译成代码直觉，并给出 Lean 4 / Mathlib 中的对应符号。建议先回顾 Part 2 的“函子/自然变换”表格，因为预层本质上就是反变函子。

### 从代码到层

下表把层与预层相关概念与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这个层在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 预层 $\mathcal{F}: \mathrm{Open}(M)^{\mathrm{op}} \to \mathbf{Set}$ | 每个开集对应一个“局部数据集合”，包含映射给出限制/收缩操作 | `TopCat.Presheaf X (Type u)` 或更一般地 `Presheaf C X` |
| 限制映射 $\rho_{UV}$ | 把大图上的截面限制到小开集 | `TopCat.Presheaf.map`（由反变函子结构给出） |
| 层（sheaf） | 局部相容的数据可以唯一粘合；像带有“粘贴协议”的依赖类型 | `TopCat.Sheaf X (Type u)`，满足 `IsSheaf` 条件 |
| 茎 $\mathcal{F}_p$ | 某点处所有局部数据的“极限/并集”，即局域行为 | `TopCat.Presheaf.stalk F p` |
| 层化 $a: \mathbf{PSh} \to \mathbf{Sh}$ | 把任意预层“补全”为满足层公理的对象；类似自由完备化 | `Sheafification J` 或 `sheafify`（取决于具体位象/site） |
| 取值于范畴的预层 / 2-预层 | 每个开集不再是一个集合，而是一个范畴；限制是函子 | `Presheaf (Cat.{v,u}) X` 或 2-范畴上的 `Functor` 实现 |

### UFPF 中的层实例

下表把 UFPF 中的层实例与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这些 UFPF 层构造在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 谱预层 $\mathcal{E}: \mathrm{Open}(M)^{\mathrm{op}} \to \mathbf{Cat}$ | 每个开集对应一个谱丛范畴，重叠开集上通过限制函子衔接 | 定义 `Functor (Open M)ᵒᵖ Cat`；层公理由 `IsSheafOfTypes` 的适当范畴版本验证 |
| 常量谱预层 | 每个开集都返回同一个谱范畴，限制函子为恒等 | 常值函子的直接实现；定理 10.1 断言它是层 |
| 奇点 = 层公理被破坏的位置 | 某些开集上局部相容的数据无法粘合为全局对象 | 形式化时即 `IsSheaf` 条件不成立的点 |

### 从代码到纤维化与谱丛

下表把 Grothendieck 纤维化与谱丛相关概念与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这个纤维化在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 投影函子 $\pi: \mathcal{E} \to \mathcal{B}$ | 把“总空间”里的对象映射到其参数标签 | `Functor E B` |
| 纤维 $\mathcal{E}_b = \pi^{-1}(b)$ | 固定参数 $b$ 处的所有对象，像依赖类型 $\pi^{-1}(b)$ | 取 `StructuredArrow` 或子范畴 `FiberCategory` |
| Cartesian 提升 | 沿基映射把纤维里的对象“拉回/重索引”到另一个纤维 | `IsCartesian` 态射；Mathlib 中可见 `CategoryTheory.Functor.IsFibered` |
| Grothendieck 纤维化 | 所有基映射都有 Cartesian 提升；即参数族可沿参数变化重新索引 | `IsGrothendieckFibration` / `IsFibered` |
| 分裂纤维化 | Cartesian 提升可规范选择，且恒等/复合保持；适合编程实现 | `Cleavage` / `Split` 结构；常值提升给出平凡 cleavage |
| 截面 $\sigma: \mathcal{B} \to \mathcal{E}$ | 对每个参数选择一个纤维对象；像“参数化对象” | `Functor B E` 且满足 `π ⋙ σ = Functor.id B` |
| Grothendieck 构造（总范畴） | 由伪函子 $F: \mathcal{B}^{\mathrm{op}} \to \mathbf{Cat}$ 拼出总范畴 | `CategoryTheory.Grothendieck F` |

### UFPF 中的谱丛实例

下表把 UFPF 中的谱丛实例与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这些 UFPF 谱丛在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| **Temp**：温度谱丛，基 $\mathbf{Temp} = (\mathbb R, \le)$，纤维为谱对象 | 每个温度 $T$ 返回一个谱；沿 $T' \le T$ 的限制是恒等或规范同构 | 基范畴作为 `Preorder` / `Category` 实例；参数变化由 `Functor.map` 处理 |
| **RG**：能标谱丛，基为能标范畴，纤维为谱对象 | 重正化群流给出基映射；Cartesian 提升给出谱的“平行移动” | `IsGrothendieckFibration` 中验证 Cartesian 提升存在 |
| **Noise**：噪声谱丛，基为噪声强度，纤维为谱对象 | 噪声参数变化时谱结构不变，仅标签改变 | 常值/分裂纤维化的典型例子；限制函子为恒等 |
| **Sig**：签名谱丛，基为 Clifford 签名，纤维为谱对象 | 签名参数变化诱导谱的规范提升 | 分裂纤维化；限制函子由签名范畴的 `Functor` 给出 |
| **Kerr**：黑洞参数谱丛，基为 $(a, m)$，纤维为固定参数处的 $\omega$ 谱集（$N$ 叶覆盖） | 复参数空间上的谱覆盖；分支点处层公理可能破坏 | `TopCat.Presheaf` / `Sheaf` 在复参数空间上的实现；分支点对应 `IsSheaf` 失败 |
| **Flt**：味扇区谱丛，基为味参数，纤维为谱对象 | 味参数决定谱族 | 参数范畴上的 `Functor`；截面给出味选择 |

### 从代码到栈

下表把栈与下降条件相关概念与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这个栈在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 栈（stack） | 取值于高阶范畴的层：对象可在重叠开集上“粘合”到同构意义 | 在 Lean 中常通过 `FiberedCategory` 加下降条件形式化；Mathlib 代数几何部分有 `IsStackFor` |
| 下降条件 | 局域数据若满足同构相容性，则可粘合为全局对象（允许唯一同构） | `DescentData` / `IsStack` |
| 谱栈 | 谱丛在开集范畴上的层论推广 | 2-层 / 高阶层的实现，需处理开集重叠时的谱同构 |

### 在 Mathlib 中快速定位相关概念

- `Mathlib.Topology.Sheaves.Presheaf`：`TopCat.Presheaf X C`
- `Mathlib.Topology.Sheaves.Sheaf`：`TopCat.Sheaf X C`、`IsSheaf`
- `Mathlib.Topology.Sheaves.Stalk`：`Presheaf.stalk`、`stalkMap`
- `Mathlib.CategoryTheory.Sites.Sheafification`：`sheafify`、`Sheafification`
- `Mathlib.CategoryTheory.Grothendieck`：Grothendieck 构造总范畴
- `Mathlib.CategoryTheory.FiberedCategory.*`：纤维范畴、Cartesian 态射、分裂纤维化等（名称随 Mathlib 版本可能变化）

> **学习技巧**：把层想象成“带粘贴规则的依赖映射”，把 Grothendieck 纤维化想象成“依赖类型族 $b \mapsto \mathcal{E}_b$”，Cartesian 提升就是沿基映射的 coercion/reindexing。UFPF 的 Temp/RG/Noise 等谱丛都是最简单的情形：纤维不随参数变化，限制函子是恒等，因此分裂性自动满足。Kerr 谱覆盖则是非平凡例子，分支点处需要仔细处理茎与单值群。

## 4.7 练习

1. 验证常值预层 $\mathcal{F}(U) = S$（$S$ 为固定集合）是层。
2. 解释为什么 Paper XVI 中"广义协变原理等价于层公理"在物理上意味着什么。
3. 写出 Paper XXI 中 Grothendieck 纤维化的五个组成要素：基空间、纤维、投影、Cartesian 提升、截面。
4. 在 Kerr 谱覆盖中，基空间是什么？纤维是什么？分支点对应什么物理现象？
5. 为什么 UFPF 中所有物理纤维化都是**分裂**的？非分裂纤维化可能出现在什么场景？

## 4.8 关键要点

- **预层**是反变函子，**层**额外满足局域性与粘合性。
- **Grothendieck 纤维化**是 UFPF 上层建筑的核心，统一了温度、能标、噪声、签名等参数化谱族。
- **截面**是物理可观测量的范畴论对应，**Cartesian 提升**是参数演化的谱流方程。
- **谱栈/谱覆盖**将纤维化与层论结合，处理弯曲时空与多参数物理系统的局域-整体结构。
