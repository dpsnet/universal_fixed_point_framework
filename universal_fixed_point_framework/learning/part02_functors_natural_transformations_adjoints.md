# Part 2：函子、自然变换与伴随

> 目标：掌握 MUFPF 的四大核心范畴论工具——函子、自然变换、伴随对、单位/余单位，能够复述 Paper I 中 $D \dashv R$ 的构造逻辑。

## 问题动机

既然 $\mathbf{Rec}$ 和 $\mathbf{Sp}$ 都是范畴，下一个自然的问题是：它们之间能不能“翻译”？谱化函子 $D$ 就是把递归系统翻译成谱数据的尝试。但“翻译”不是随意映射，它必须保持对象、态射和复合——这正是函子的定义。更进一步，如果两种翻译方式之间存在系统性的转换，我们就需要自然变换；如果一种翻译是另一种的“最佳近似”，我们就遇到了伴随。

本章要解决的问题是：**如何在一个范畴和另一个范畴之间建立保持结构的映射？什么情况下这种映射存在“最佳近似”？**

## 2.1 函子

**定义 2.1**（协变函子）。函子 $F: \mathcal{C} \to \mathcal{D}$ 将：
- 对象映射到对象：$X \mapsto F(X)$
- 态射映射到态射：$f: X \to Y \mapsto F(f): F(X) \to F(Y)$

并满足：
- $F(\mathrm{id}_X) = \mathrm{id}_{F(X)}$
- $F(g \circ f) = F(g) \circ F(f)$

**定义 2.2**（反变函子）。反变函子 $F: \mathcal{C}^{\mathrm{op}} \to \mathcal{D}$ 反转复合顺序：$F(g \circ f) = F(f) \circ F(g)$。

### MUFPF 实例：谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$

Paper I 定义 2.3.1：对 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R) \in \mathbf{Rec}_D$，

$$D(R) = (\mathcal{H}_R, A_R, \sigma(A_R))$$

其中 $A_R = -\log U_R$，$U_R$ 是 Koopman 演化算子。

对态射 $f: R_1 \to R_2$，$D(f)$ 是相应的谱空间映射。Paper I 命题 2.3.3 证明 $D$ 满足函子律。

### MUFPF 实例：静态化函子 $\mathcal{L}: \mathbf{Rec} \to \mathbf{Rec}_{\text{id}}$

Paper XIX 定义 4.1：$\mathcal{L}$ 遗忘动力学结构，将 $(\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$ 映为 $(M, \mathrm{id}_M, \mathbb{R}_{\ge 0}, \mu_M)$。

## 2.2 自然变换

**定义 2.3**（自然变换）。给定函子 $F, G: \mathcal{C} \to \mathcal{D}$，自然变换 $\alpha: F \Rightarrow G$ 为每个 $X \in \mathcal{C}$ 指定一个态射 $\alpha_X: F(X) \to G(X)$，使得对任意 $f: X \to Y$ 下图交换：

```
F(X) --α_X--> G(X)
 |              |
 |F(f)          |G(f)
 v              v
F(Y) --α_Y--> G(Y)
```

即 $G(f) \circ \alpha_X = \alpha_Y \circ F(f)$。

**定义 2.4**（自然同构）。若每个 $\alpha_X$ 都是同构，则称 $\alpha$ 为自然同构，记 $F \cong G$。

### MUFPF 实例：谱对应自然同构

Paper I 定理 3.7a：在实正自伴情形下，

$$M_0 \cong L_0$$

其中 $M_0$ 是压缩算子的谱乘子，$L_0$ 是生成元谱。这一自然同构将数值等式 $\lambda_i = e^{-\mu_i}$ 提升为范畴论陈述。

Paper I 定理 3.7b：复耗散情形下为**辫子自然同构**：

$$M^{\text{br}} \cong_{\text{br}} L^{\text{br}}$$

## 2.2a Yoneda 引理完整证明

Yoneda 引理是表示函子与自然变换之间的基本对应，也是理解 MUFPF 中"谱对应"为何能被提升为自然同构的理论背景。下面给出完整证明，可直接用于自检。

**引理 2.4**（Yoneda）。设 $\mathcal{C}$ 是局部小范畴，$F: \mathcal{C}^{\mathrm{op}} \to \mathbf{Set}$ 为反变函子。对任意 $A \in \mathcal{C}$，存在典范双射

$$\mathrm{Nat}(h_A, F) \;\cong\; F(A),$$

且该双射对 $A$ 与 $F$ 都是自然的。这里 $h_A = \mathrm{Hom}_{\mathcal{C}}(-, A)$ 是 $A$ 的表示函子。

**证明**。构造两个互逆映射。

1. **正向映射** $\Psi: \mathrm{Nat}(h_A, F) \to F(A)$：
   对自然变换 $\alpha: h_A \Rightarrow F$，定义
   $$\Psi(\alpha) := \alpha_A(\mathrm{id}_A) \in F(A).$$

2. **反向映射** $\Phi: F(A) \to \mathrm{Nat}(h_A, F)$：
   对 $u \in F(A)$，定义自然变换 $\alpha^u: h_A \Rightarrow F$，其分量为
   $$\alpha^u_X(f) := F(f)(u), \quad \forall f: X \to A.$$

   先验证 $\alpha^u$ 确实是自然变换。任取 $g: Y \to X$（即 $\mathcal{C}$ 中态射 $X \to Y$，因 $F$ 反变），须证下图交换：

   ```
   h_A(X) --α^u_X--> F(X)
     |                  |
     |h_A(g)            |F(g)
     v                  v
   h_A(Y) --α^u_Y--> F(Y)
   ```

   对任意 $f: X \to A$（即 $f \in h_A(X)$）：
   - 沿右侧再向下：$F(g)(F(f)(u)) = F(f \circ g)(u)$（由 $F$ 反变的函子律）；
   - 沿下侧再向右：$\alpha^u_Y(f \circ g) = F(f \circ g)(u)$。

   二者相等，故 $\alpha^u$ 自然。

3. **互逆验证**：
   - $\Psi(\Phi(u)) = \alpha^u_A(\mathrm{id}_A) = F(\mathrm{id}_A)(u) = u$。
   - 对 $\alpha: h_A \Rightarrow F$，任取 $X$ 与 $f: X \to A$，由自然性：
     $$\alpha_X(f) = \alpha_X(h_A(f)(\mathrm{id}_A)) = F(f)(\alpha_A(\mathrm{id}_A)) = F(f)(\Psi(\alpha)) = \Phi(\Psi(\alpha))_X(f).$$
     因此 $\Phi(\Psi(\alpha)) = \alpha$。

4. **自然性**：
   - **对 $A$ 自然**：对 $k: A \to B$，须证 $\Psi_B \circ \mathrm{Nat}(h_k, F) = F(k) \circ \Psi_A$。直接由自然变换复合与 $F(k)$ 的定义可得。
   - **对 $F$ 自然**：对 $\beta: F \Rightarrow G$，须证 $\Psi_G \circ \mathrm{Nat}(h_A, \beta) = \beta_A \circ \Psi_F$。这由 $\beta$ 的自然性直接得到。

因此 Yoneda 双射是自然同构。$\square$

**与 MUFPF 的关联**。Paper I 中的谱对应 $\lambda_i = e^{-\mu_i}$ 可视为"可表函子"思想的特例：将每个递归系统 $R$ 映到其谱集合的函子 $L_0, M_0$ 由 $R$ 本身（通过 $D$）表示，而自然同构 $M_0 \cong L_0$ 正是 Yoneda 意义下"同一对象的不同表示"给出的典范对应。

## 2.3 伴随对

**定义 2.5**（伴随对）。函子 $L: \mathcal{C} \to \mathcal{D}$ 与 $R: \mathcal{D} \to \mathcal{C}$ 构成伴随，记 $L \dashv R$，若存在自然同构：

$$\mathrm{Hom}_{\mathcal{D}}(L(X), Y) \cong \mathrm{Hom}_{\mathcal{C}}(X, R(Y))$$

对 $X \in \mathcal{C}, Y \in \mathcal{D}$ 自然成立。

**等价表述**：伴随对配备：
- **单位**（unit）$\eta: \mathrm{id}_{\mathcal{C}} \to R \circ L$
- **余单位**（counit）$\varepsilon: L \circ R \to \mathrm{id}_{\mathcal{D}}$

满足三角恒等式：

$$(\varepsilon L) \circ (L \eta) = \mathrm{id}_L$$
$$(R \varepsilon) \circ (\eta R) = \mathrm{id}_R$$

### MUFPF 实例：$D \dashv R$

Paper I 定理 2.4.5：谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 有右伴随 $R: \mathbf{Sp} \to \mathbf{Rec}_D$。

- $D$（左伴随）：将递归系统谱化，对应"向下归约"到谱数据
- $R$（右伴随）：从谱数据重建递归系统，对应"向上提升"

Paper I 哲学版将这一伴随提升为还原论/涌现论的数学对应。

## 2.3a $D \dashv R$ 三角等式显式验证

为了让 $D \dashv R$ 不只是“存在性”结论，本节给出右伴随 $R$ 的显式构造、单位/余单位，并逐条验证三角恒等式。所有结论均可对照 Paper I 构造 C2.2、定理 C2.3 以及命题 2.4.4 自检。

### 右伴随 $R(E)$ 的显式构造

对任意谱对象 $E = (\mathcal H_E, A_E, \sigma_E) \in \mathbf{Sp}$，定义递归系统

$$R(E) = (\mathcal S_{R(E)}, \Phi_{R(E)}, \mathcal T_{R(E)}, \mathcal M_{R(E)}) \in \mathbf{Rec}_D$$

如下：

- **状态空间**：$\mathcal S_{R(E)} = \mathcal D(A_E)$，即 $A_E$ 的稠定定义域，赋予图范数（graph norm）拓扑；
- **演化映射**：$\Phi_{R(E)} = e^{-A_E}|_{\mathcal D(A_E)}$，即 Hille–Yosida 压缩半群在 $t=1$ 时刻的限制；
- **时间半群**：$\mathcal T_{R(E)} = \mathbb R_{\ge 0}$；
- **附加结构**：$A_E$ 的谱测度 $E_{A_E}$，使得 $\sigma_E$ 可由它实现。

这一构造保证 $D(R(E))$ 与 $E$ 在谱范畴中典范同构：

$$D(R(E)) \;\cong\; E.$$

直观上，$R$ 把“谱数据”重新装配成一个以该谱生成元为动力学核心的递归系统；$D$ 再把它谱化回去时，由于谱由 $A_E$ 决定，得到的就是原来的 $E$。

### 单位与余单位

采用标准伴随记号 $D \dashv R$：

- **单位**（unit）是递归系统范畴中的自然变换

  $$\eta: \mathrm{id}_{\mathbf{Rec}_D} \longrightarrow R \circ D.$$

  对 $S \in \mathbf{Rec}_D$，分量 $\eta_S: S \to R(D(S))$ 是“谱坐标规范化嵌入”：它把 $S$ 的状态按 $D(S)$ 的谱坐标嵌入到 $R(D(S))$ 的定义域中，并使得演化在半群层面保持对应。Paper I 原稿把这一方向的映射记作“余单位”，这是与标准伴随记号相反的命名；这里采用标准记号，特此指出。

- **余单位**（counit）是谱范畴中的自然变换

  $$\varepsilon: D \circ R \longrightarrow \mathrm{id}_{\mathbf{Sp}}.$$

  对 $E \in \mathbf{Sp}$，分量 $\varepsilon_E: D(R(E)) \to E$ 取上述典范同构。由于构造直接保证 $D(R(E)) = E$（作为谱对象可典范等同于 $E$），因此可取

  $$\varepsilon_E = \mathrm{id}_E.$$

### Hom 集合同构的显式对应

$D \dashv R$ 的伴随同构

$$\mathrm{Hom}_{\mathbf{Sp}}(D(S), E) \;\cong\; \mathrm{Hom}_{\mathbf{Rec}_D}(S, R(E))$$

由单位、余单位显式给出：

- **右向**（谱态射 $u$ 诱导递归系统态射）：

  $$u: D(S) \to E \longmapsto S \xrightarrow{\eta_S} R(D(S)) \xrightarrow{R(u)} R(E).$$

- **左向**（递归系统态射 $v$ 诱导谱态射）：

  $$v: S \to R(E) \longmapsto D(S) \xrightarrow{D(v)} D(R(E)) \xrightarrow{\varepsilon_E} E.$$

两条映射互逆，正是由下面要验证的三角恒等式保证。

### 三角恒等式验证

伴随的两个三角恒等式在标准记号下写作：

1. $(\varepsilon D) \circ (D \eta) = \mathrm{id}_D$；
2. $(R \varepsilon) \circ (\eta R) = \mathrm{id}_R$。

逐条验证如下。

#### 第一条：$\varepsilon D \circ D\eta = \mathrm{id}_D$

取任意 $S \in \mathbf{Rec}_D$。需要证明

$$\varepsilon_{D(S)} \circ D(\eta_S) = \mathrm{id}_{D(S)}.$$

- 首先，$D(R(D(S))) = D(S)$。这是因为 $R$ 的构造保持谱不变：对谱对象 $D(S)$ 应用 $R$ 得到的新递归系统，再经 $D$ 谱化，得到的谱数据与原 $D(S)$ 相同。
- 因此余单位分量 $\varepsilon_{D(S)}: D(R(D(S))) \to D(S)$ 就是 $\varepsilon_{D(S)}: D(S) \to D(S)$，而由构造 $\varepsilon_{D(S)} = \mathrm{id}_{D(S)}$。
- 另一方面，单位分量 $\eta_S: S \to R(D(S))$ 的选取要求它在谱化后成为恒等，即 $D(\eta_S) = \mathrm{id}_{D(S)}$。这是 $
\eta$ 作为单位映射在谱层面的核心性质。

于是

$$\varepsilon_{D(S)} \circ D(\eta_S) = \mathrm{id}_{D(S)} \circ \mathrm{id}_{D(S)} = \mathrm{id}_{D(S)}.$$

#### 第二条：$R\varepsilon \circ \eta R = \mathrm{id}_R$

取任意 $E \in \mathbf{Sp}$。需要证明

$$R(\varepsilon_E) \circ \eta_{R(E)} = \mathrm{id}_{R(E)}.$$

- 由 $R(E)$ 的构造，$D(R(E)) = E$（典范等同），且 $\varepsilon_E: D(R(E)) \to E$ 就是 $\mathrm{id}_E$。
- 因此 $R(\varepsilon_E): R(D(R(E))) \to R(E)$ 就是 $R$ 作用在恒等谱态射上，故 $R(\varepsilon_E) = \mathrm{id}_{R(E)}$。
- 同时，$R(E)$ 本身正是某个谱对象 $E$ 经 $R$ 重建出来的递归系统，所以 $R(D(R(E))) = R(E)$。于是单位分量 $\eta_{R(E)}: R(E) \to R(D(R(E)))$ 的到达对象就是 $R(E)$ 本身。
- 由于 $\eta$ 是单位自然变换，且 $D(\eta_{R(E)}) = \mathrm{id}_{E}$（同上条理由），而 $D$ 是忠实函子（Paper I 命题 2.3.3），由

  $$D(\eta_{R(E)}) = \mathrm{id}_{D(R(E))} = \mathrm{id}_E$$

  可推出 $\eta_{R(E)} = \mathrm{id}_{R(E)}$。

因此

$$R(\varepsilon_E) \circ \eta_{R(E)} = \mathrm{id}_{R(E)} \circ \mathrm{id}_{R(E)} = \mathrm{id}_{R(E)}.$$

#### 关键观察：谱不变性与 $D$ 的忠实性

两条恒等式的成立都依赖一个核心事实：$R$ 的构造是**谱不变的**——反复应用 $D \circ R$ 不会引入新的谱信息。这正是命题 2.4.4 中 $\mathbf{Sp}$ 成为 $\mathbf{Rec}_D$ 反射子范畴的数学根源。

> **自检要点**。验证 $D \dashv R$ 时不必陷入无限递推：$R(E)$ 被显式构造为 $e^{-A_E}$ 在 $\mathcal D(A_E)$ 上的作用；三角恒等式随后只需检验 $D(R(D(S))) = D(S)$ 与 $D$ 的忠实性。Paper I 中把单位/余单位的名称与标准伴随记号相反，阅读时注意把“映射方向”与“标准定义”对应起来即可。

### MUFPF 实例：三层伴随对嵌套

Paper XIX 建立：

$$D \dashv R \;\subset\; \mathcal{L} \dashv \iota \;\subset\; \mathcal{S}el \dashv \mathcal{D}iss$$

- $\mathcal{L} \dashv \iota$：静态化函子与包含函子（Paper XIX 定理 4.2）
- $\mathcal{S}el \dashv \mathcal{D}iss$：选择-溶解伴随对（Paper XIX 命题 8.3）

这一嵌套结构实现动力学系统、静态拓扑、随机噪声之间的双向转化。

## 2.4 忠实、满、完全函子

**定义 2.6**：函子 $F: \mathcal{C} \to \mathcal{D}$：
- **忠实**（faithful）：$\mathrm{Hom}_{\mathcal{C}}(X, Y) \to \mathrm{Hom}_{\mathcal{D}}(F(X), F(Y))$ 是单射
- **满**（full）：上述映射是满射
- **完全**（fully faithful）：上述映射是双射

### MUFPF 实例

Paper I 证明 $D$ 是忠实函子（命题 2.3.3）。这意味着不同的递归系统态射不会谱化为相同的谱态射——谱化不丢失态射层面的信息。

## 2.5 等价与伴随的关系

若 $L \dashv R$ 且单位、余单位都是自然同构，则 $L$ 与 $R$ 构成范畴等价。在 MUFPF 中，$D \dashv R$ 通常不是等价，因为：
- 不同的递归系统可能有相同谱（非忠实？不，$D$ 是忠实的但非完全）
- 谱范畴中的对象不一定都能由递归系统生成

这解释了为什么 $\mathbf{Sp}$ 是 $\mathbf{Rec}_D$ 的反射子范畴（命题 2.4.4），而非等价子范畴。

## 2.8 程序员与形式化视角（选读）

本节把“函子—自然变换—伴随”翻译成代码直觉和 Lean 4 / Mathlib 的对应符号，帮助程序员自检是否把抽象定义落到了具体类型上。

### 从代码到函子

下表把函子相关概念与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这个函子在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 协变函子 $F: \mathcal{C} \to \mathcal{D}$ | 把一个类型结构转换成另一个类型结构，同时保持恒等映射和复合 | `Functor C D`（携带 `obj` 与 `map` 并满足 `map_id`、`map_comp`） |
| 反变函子 $F: \mathcal{C}^{\mathrm{op}} \to \mathcal{D}$ | 输入的箭头方向被反转，例如从“函数”变成“对偶函数” | `Functor Cᵒᵖ D` 或在 `CategoryTheory` 中使用 `op` 构造 |
| 常值函子 $\Delta_X$ | 不管什么输入都返回同一个对象/类型 | 用 `Functor.const` 实现 |
| 遗忘函子 | 把带结构的类型“遗忘”成底层类型 | `forget Group`、`forget Ring` 等具体范畴的遗忘函子 |
| 表示函子 $h_A = \mathrm{Hom}(-, A)$ | Yoneda：把对象 $A$ 编码成它发出的所有态射集合 | `yoneda.obj A` |

### MUFPF 中的具体函子

下表把 MUFPF 中的具体函子构造与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这些 MUFPF 函子在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ | 把递归动力系统“编译”成谱数据（算子、谱测度） | 对应 `Functor RecD Sp`，对象映射 $R \mapsto (\mathcal{H}_R, A_R, \sigma(A_R))$，需验证 `map_id` 与 `map_comp` |
| 静态化函子 $\mathcal{L}: \mathbf{Rec} \to \mathbf{Rec}_{\mathrm{id}}$ | 把动力系统“降级”为恒等动力学的静态空间 | 遗忘函子的实例，保留状态空间但把演化替换为 `id` |
| 包含函子 $\iota: \mathbf{Rec}_{\mathrm{id}} \hookrightarrow \mathbf{Rec}$ | 静态系统作为动力系统的子类嵌入 | 完全忠实的嵌入函子 |
| 选择/溶解函子 $\mathcal{S}el \dashv \mathcal{D}iss$ | 在随机/噪声结构里“选择样本”与“溶解为分布” | 可形式化为两个 `Functor` 并证明 `Adjunction` |

### 从代码到自然变换与伴随

下表把自然变换、伴随等概念与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这些构造在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 自然变换 $\alpha: F \Rightarrow G$ | 两个函子之间的“一致转换”，对每个对象给出一个态射，且与所有映射交换 | `NatTrans F G`，分量 `app X`，自然性由 `naturality` 字段保证 |
| 自然同构 $F \cong G$ | 每个分量都是同构的一致转换 | `NatIso F G` |
| 伴随 $L \dashv R$ | 两个函子之间的“最佳近似互逆”，左边通常构造/遗忘，右边通常重建/添加结构 | `Adjunction L R` 或 `L ⊣ R` |
| 单位 $\eta: \mathrm{id} \to R \circ L$ | 从左到右的“提升/嵌入” | `Adjunction.unit` |
| 余单位 $\varepsilon: L \circ R \to \mathrm{id}$ | 从右到左的“投影/归约” | `Adjunction.counit` |
| 三角恒等式 | 验证“提升后再投影”等于恒等 | `Adjunction.left_triangle` / `right_triangle` |

### 在 Mathlib 中快速定位相关概念

- `Mathlib.CategoryTheory.Functor`：`Functor`、`map_id`、`map_comp`
- `Mathlib.CategoryTheory.NatTrans`：`NatTrans`、`naturality`
- `Mathlib.CategoryTheory.Adjunction`：`Adjunction`、`unit`、`counit`、三角恒等式
- `Mathlib.CategoryTheory.Yoneda`：`yoneda`、`yonedaEquiv`（即 Yoneda 引理的 Lean 实现）
- `Mathlib.CategoryTheory.ConcreteCategory`：遗忘函子与具体范畴的通用框架

> **学习技巧**：把本节的表格与 Part 1 的“从代码到范畴”表格连起来看：范畴是纯接口 / 契约，对象是接口允许的类型，态射是接口承认的转换，函子是接口之间的兼容映射 / 类型转换器，自然变换是兼容映射之间的一致映射，伴随则是两套接口之间的最佳配对。MUFPF 的谱化/静态化/选择/溶解都可以依次被实现为 `Functor` 加 `Adjunction`。

## 2.6 练习

1. 证明 Paper I 中 $D$ 的函子律：$D(\mathrm{id}_R) = \mathrm{id}_{D(R)}$ 与 $D(g \circ f) = D(g) \circ D(f)$。
2. 验证自然变换 $\eta_R: M_0 \to L_0$ 的交换图（Paper I §3.4a）。
3. 用伴随的 Hom 集合定义，解释为什么 $D \dashv R$ 中 $D$ 是左伴随、$R$ 是右伴随。
4. 在 Paper XIX 的三层伴随对嵌套中，指出每个左伴随和右伴随的"物理直觉"（如遗忘、构造、选择、溶解）。
5. 若 $D$ 是忠实但非完全的，说明 $\mathbf{Sp}$ 比 $\mathbf{Rec}_D$ "更大"还是"更小"？

## 2.7 关键要点

- **函子**是范畴之间的结构保持映射，MUFPF 的核心操作（谱化、静态化、选择）都是函子。
- **自然变换**比较两个函子，MUFPF 中的谱对应 $\lambda_i = e^{-\mu_i}$ 被提升为自然同构。
- **伴随对**是 MUFPF 的哲学与数学核心，$D \dashv R$ 编码还原论/涌现论的对偶。
- 左伴随通常"构造/遗忘前结构"，右伴随通常"重建/添加结构"，但具体方向需由 Hom 集合定义验证。
