# Part 7：习题：解答与提示

> 本文件为 [part07_exercises_lean.md](part07_exercises_lean.md) 中分级习题提供解答、提示与部分 Lean 4 代码片段。建议先独立完成，再查阅本文件。

---

## Level 1：入门

### 1.1 验证 $\mathbf{Set}$ 满足范畴公理

**解答要点**：
- **对象**：任意集合
- **态射**：集合之间的函数
- **复合**：函数复合
- **恒等**：恒等函数 $\mathrm{id}_A(x) = x$

**结合律**：$(h \circ g) \circ f = h \circ (g \circ f)$ 由函数复合定义直接得到。

**单位律**：$f \circ \mathrm{id}_A = f$ 因为对任意 $x \in A$：

$$(f \circ \mathrm{id}_A)(x) = f(\mathrm{id}_A(x)) = f(x)$$

同理 $\mathrm{id}_B \circ f = f$。

### 1.2 初始对象在同构意义下唯一

**解答**：设 $I, J$ 都是范畴 $\mathcal{C}$ 的初始对象。由定义，存在唯一态射 $f: I \to J$ 和唯一态射 $g: J \to I$。

考虑 $g \circ f: I \to I$。由于 $I$ 是初始对象，存在唯一态射 $I \to I$，即 $\mathrm{id}_I$。因此 $g \circ f = \mathrm{id}_I$。

同理 $f \circ g = \mathrm{id}_J$。

故 $I \cong J$。

### 1.3 $\mathbf{Rec}$ 中的恒等态射

**解答**：对 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$，恒等态射是状态空间上的恒等映射：

$$\mathrm{id}_R: \mathcal{S}_R \to \mathcal{S}_R, \quad \mathrm{id}_R(x) = x$$

验证单位律：对任意态射 $f: R_1 \to R_2$，

$$f \circ \mathrm{id}_{R_1} = f = \mathrm{id}_{R_2} \circ f$$

由函数复合的恒等律直接得到。

### 2.1 自然同构的逆也是自然变换

**解答**：设 $\alpha: F \Rightarrow G$ 是自然同构，对每个 $X$ 给定 $\alpha_X: F(X) \to G(X)$ 是同构。定义 $\beta_X = \alpha_X^{-1}: G(X) \to F(X)$。

需验证 $\beta$ 是自然变换，即对任意 $f: X \to Y$：

$$F(f) \circ \beta_X = \beta_Y \circ G(f)$$

由 $\alpha$ 的自然性：$G(f) \circ \alpha_X = \alpha_Y \circ F(f)$。

两边左复合 $\beta_Y$、右复合 $\beta_X$：

$$\beta_Y \circ G(f) \circ \alpha_X \circ \beta_X = \beta_Y \circ \alpha_Y \circ F(f) \circ \beta_X$$

化简：$\beta_Y \circ G(f) = F(f) \circ \beta_X$。

### 2.2 伴随对的两种定义等价

**解答要点**：

**(Hom 集合定义 → 单位/余单位定义)**：
- 对 $X \in \mathcal{C}$，取 $\eta_X: X \to R(L(X))$ 为 $\mathrm{id}_{L(X)} \in \mathrm{Hom}_{\mathcal{D}}(L(X), L(X))$ 在 Hom 同构下的像
- 对 $Y \in \mathcal{D}$，取 $\varepsilon_Y: L(R(Y)) \to Y$ 为 $\mathrm{id}_{R(Y)} \in \mathrm{Hom}_{\mathcal{C}}(R(Y), R(Y))$ 在 Hom 同构下的像
- 三角恒等式由 Hom 同构的自然性推出

**(单位/余单位定义 → Hom 集合定义)**：
- 给定 $f: L(X) \to Y$，定义 $\tilde{f}: X \to R(Y)$ 为 $R(f) \circ \eta_X$
- 给定 $g: X \to R(Y)$，定义 $\hat{g}: L(X) \to Y$ 为 $\varepsilon_Y \circ L(g)$
- 三角恒等式保证这两个映射互逆

### 2.3 $D \dashv R$ 中单位与余单位的物理含义

**解答**：
- **单位** $\eta: \mathrm{id}_{\mathbf{Rec}_D} \to R \circ D$：将递归系统 $R$ 嵌入到"先谱化再递归化"的系统中。可理解为：从原始递归系统到其谱重建版本的**规范化嵌入**。
- **余单位** $\varepsilon: D \circ R \to \mathrm{id}_{\mathbf{Sp}}$：从"先递归化再谱化"的谱对象到原始谱对象的**投影**。由于谱化可能丢失信息（如相位、基选择），余单位体现了**谱像只携带尺度信息**的特征。

---

## Level 2：进阶

### 3.1 $\mathbf{Set}$ 中的积与余积

**积**：集合 $A, B$ 的积是 Cartesian 积：

$$A \times B = \{(a, b) \mid a \in A, b \in B\}$$

投影为 $\pi_A(a,b) = a$，$\pi_B(a,b) = b$。

泛性质：对任意集合 $C$ 和函数 $f: C \to A$、$g: C \to B$，存在唯一 $h: C \to A \times B$ 使得 $\pi_A \circ h = f$，$\pi_B \circ h = g$。取 $h(c) = (f(c), g(c))$。

**余积**：集合 $A, B$ 的余积是不交并：

$$A \sqcup B = (A \times \{0\}) \cup (B \times \{1\})$$

注入为 $i_A(a) = (a, 0)$，$i_B(b) = (b, 1)$。

泛性质：对任意集合 $C$ 和函数 $f: A \to C$、$g: B \to C$，存在唯一 $h: A \sqcup B \to C$ 使得 $h \circ i_A = f$，$h \circ i_B = g$。取 $h(a,0) = f(a)$，$h(b,1) = g(b)$。

### 3.2 等化子 + 有限积 ⟹ 拉回

**解答**：拉回是如下图表的极限：

```
P --→ A
|     |
v     v
B --→ C
```

可构造为 $A \times B$ 的等化子，其中两个态射为：

$$A \times B \;\xrightarrow{\pi_A}\; A \;\xrightarrow{f}\; C$$

和

$$A \times B \;\xrightarrow{\pi_B}\; B \;\xrightarrow{g}\; C$$

即：

$$P = \{(a, b) \in A \times B \mid f(a) = g(b)\}$$

### 3.3 Eilenberg-Moore 范畴满足范畴公理

**解答要点**：
- **对象**：$T$-代数 $(X, \alpha: T(X) \to X)$
- **态射**：$f: (X, \alpha) \to (Y, \beta)$ 是满足 $f \circ \alpha = \beta \circ T(f)$ 的态射 $f: X \to Y$
- **恒等**：$\mathrm{id}_X$ 显然是 $T$-代数态射
- **复合**：若 $f, g$ 是 $T$-代数态射，验证 $g \circ f$ 满足相容条件

### 3.4 $T = \mathcal{L} \circ \iota$ 是恒等函子

**解答**：$\mathcal{L}: \mathbf{Rec} \to \mathbf{Rec}_{\text{id}}$ 是静态化函子，$\iota: \mathbf{Rec}_{\text{id}} \to \mathbf{Rec}$ 是包含函子。

对 $R \in \mathbf{Rec}_{\text{id}}$，$R$ 已经是恒等延拓对象，静态化不改变它：$\mathcal{L}(\iota(R)) = R$。

因此 $T = \mathcal{L} \circ \iota = \mathrm{id}_{\mathbf{Rec}_{\text{id}}}$。

单位 $\eta = \mathrm{id}$，乘法 $\mu = \mathrm{id}$。

Eilenberg-Moore 范畴与 $\mathbf{Rec}_{\text{id}}$ 同构：每个对象 $R$ 对应 $T$-代数 $(R, \mathrm{id}_R)$。

### 4.1 常值预层是层

**解答**：设 $\mathcal{F}(U) = S$ 对所有开集 $U$，限制映射为恒等。

- **局域性**：若 $s, t \in S$ 在每个覆盖元上限制相等，则 $s = t$
- **粘合性**：给定相容族 $s_i \in S$，由于所有限制都是恒等，所有 $s_i$ 必须相等，定义 $s = s_i$ 即可

### 4.2 一个预层但不是层的例子

**解答**：在 $S^1$ 上考虑预层：

$$\mathcal{F}(U) = \{f: U \to \mathbb{R} \mid f \text{ 是有界连续函数}\}$$

这不是层，因为局部有界函数可以粘合成整体无界函数（例如 $1/(\theta - \theta_0)$ 在 $S^1$ 上去掉一点后局部有界，但整体上无界）。

### 4.3 Cartesian 提升的万有性质

**解答**：给定 Grothendieck 纤维化 $\pi: \mathcal{E} \to \mathcal{B}$，对象 $e \in \mathcal{E}$ 满足 $\pi(e) = b'$，以及基范畴中态射 $f: b \to b'$。

Cartesian 提升是 $\tilde{f}: e' \to e$ 满足 $\pi(\tilde{f}) = f$。

万有性质：任意其他提升 $g: e'' \to e$（即 $\pi(g) = f$）唯一分解为：

$$e'' \xrightarrow{u} e' \xrightarrow{\tilde{f}} e$$

其中 $\pi(u) = \mathrm{id}_b$。这正是"提升在纤维内唯一"的严格表述。

### 4.4 Temp 纤维化的一个实例

**解答**：
- **基对象**：$T = 300 \text{ K}$
- **纤维对象**：固定 $T$ 处的 QCD 谱对象 $(\mathcal{H}_T, A_T, \sigma(A_T))$
- **截面**：$T \mapsto (T, A_T)$，即每个温度对应一个谱算子
- **Cartesian 提升**：沿温度变化 $T_1 \to T_2$，谱算子 $A_{T_1} \to A_{T_2}$ 由谱流方程演化

---

## Level 3：精通

### 5.1 2-范畴中的水平与垂直复合

**完整解答**。2-范畴 $\mathcal{K}$ 中：

- **对象**仍是通常意义的对象；
- **1-态射** $f: A \to B$ 之间可有 **2-胞**（2-cell）$\alpha: f \Rightarrow g$；
- 2-胞有两种复合方式：
  - **垂直复合** $\beta \circ_v \alpha: f \Rightarrow h$，当 $f \xrightarrow{\alpha} g \xrightarrow{\beta} h$ 同终点时；
  - **水平复合** $\delta \circ_h \gamma: (k \circ f) \Rightarrow (l \circ g)$，当 $f, g: A \to B$，$k, l: B \to C$ 且 $f \xrightarrow{\gamma} g$，$k \xrightarrow{\delta} l$ 时。

设 1-态射与 2-胞如下：

```
A --f--> B --h--> C
  \\α⇒   \\β⇒
   g      k
```

则中间交换律（interchange law）断言：

$$(\beta' \circ_v \beta) \circ_h (\alpha' \circ_v \alpha)
= (\beta' \circ_h \alpha') \circ_v (\beta \circ_h \alpha).$$

**物理直觉**：在 UFPF 的谱流中，1-态射是参数点之间的谱映射，2-胞是同一参数路径上的不同谱流（由不同的规范选择或截断方案诱导）。垂直复合表示“先执行一个再执行另一个规范变换”，水平复合表示“把两段参数路径上的规范变换拼接”。中间交换律保证这两种拼接顺序给出的最终谱流一致。

**常见错误**：
- 把水平复合和垂直复合的条件搞混：垂直复合要求源和目标 1-态射相同；水平复合要求 1-态射可前后拼接。
- 忽视 interchange law，误以为"先垂直再水平"和"先水平再垂直"会给出不同结果。

### 5.2 $D_2$ 的四条 2-函子公理

**完整解答**。设 $D_2: \mathcal{K} \to \mathcal{L}$ 是两个 2-范畴之间的 2-函子。它必须保持以下四类结构：

1. **对象映射**：对每个对象 $X \in \mathcal{K}$，指定 $D_2(X) \in \mathcal{L}$。
2. **1-态射映射**：对 $f: X \to Y$，指定 $D_2(f): D_2(X) \to D_2(Y)$，且
   $$D_2(\mathrm{id}_X) = \mathrm{id}_{D_2(X)}, \qquad D_2(g \circ f) = D_2(g) \circ D_2(f).$$
3. **2-态射的垂直复合保持**：对可垂直复合的 2-胞 $\alpha: f \Rightarrow g$、$\beta: g \Rightarrow h$，
   $$D_2(\beta \circ_v \alpha) = D_2(\beta) \circ_v D_2(\alpha).$$
4. **2-态射的水平复合保持**：对可水平复合的 2-胞 $\alpha: f \Rightarrow g$（$f,g: X \to Y$）和 $\beta: h \Rightarrow k$（$h,k: Y \to Z$），
   $$D_2(\beta \circ_h \alpha) = D_2(\beta) \circ_h D_2(\alpha).$$

Paper V 定理 8.1 的证明本质上是逐项验证这些等式。

**常见错误**：
- 只验证对象与 1-态射，忘记验证 2-胞的两种复合。
- 把 $D_2(g \circ f) = D_2(g) \circ D_2(f)$ 写成反方向（适用于反变 2-函子时需注意，但 $D_2$ 是协变的）。
- 混淆垂直/水平复合符号，导致等式左右两边的复合顺序写错。

### 5.3 $\infty$-范畴与同伦

**完整解答**。$\infty$-范畴可以粗略理解为：对象、1-态射、2-态射、3-态射……直至所有高阶态射，且所有高于 1 阶的态射都是**可逆的**（这种特殊情形常称为 **$\infty$-群胚**）。

**标准例子**：拓扑空间 $X$ 的**基本 $\infty$-群胚** $\Pi_\infty(X)$：

- 对象是 $X$ 中的点；
- 1-态射是点之间的路径；
- 2-态射是路径之间的同伦；
- 3-态射是同伦之间的同伦；
- 依此类推。

更高阶态射可逆的直觉是：任何同伦都可以反向进行，因此"高阶映射"不是真正的不可逆箭头，而只是"低阶映射之间的连续变形"。

在 UFPF 的高阶形式化中，$\infty$-范畴提供了一种语言：不同截断方案、重正化群流、规范选择之间的等价关系可以被编码为高一阶的可逆态射。

**常见错误**：
- 认为 $\infty$-范畴中所有态射都可逆：实际上通常只要求高于 1 阶的态射可逆（形成 $(\infty,1)$-范畴）。
- 把高阶同伦的"可逆"理解为严格相等：同伦只是等价关系，通常需要在同伦等价意义下理解相等。
- 忽视具体模型（拟范畴、单纯范畴）与直观之间的区别。

### 6.1 Paper XXI 六个纤维化的物理截面

**完整解答**。下表给出 Paper XXI 中六个参数谱丛的基空间、纤维、投影、典型截面与可观测量。

| 谱丛 | 基空间 | 纤维 | 截面 | 物理可观测量 |
|---|---|---|---|---|
| **Temp** | 温度参数 $T \in \mathbb R$ | 固定 $T$ 的谱对象 $E_T$ | $T \mapsto (T, E_T)$ | 临界温度 $T_c$、谱隙随 $T$ 的变化 |
| **RG** | 能标参数 $\mu$ | 固定 $\mu$ 的谱对象 $E_\mu$ | $\mu \mapsto (\mu, E_\mu)$ | 耦合常数 $\alpha_s(\mu)$、跑动质量 |
| **Noise** | 噪声强度 $\eta$ | 固定 $\eta$ 的谱对象 $E_\eta$ | $\eta \mapsto (\eta, E_\eta)$ | 退相干率、噪声导致的谱漂移 |
| **Sig** | Clifford 签名 $(p,q)$ | $\mathrm{Cl}(p,q)$ 的表示谱 | $(p,q) \mapsto ((p,q), \mathrm{Cl}(p,q))$ | 旋量表示的维数与电荷共轭矩阵 |
| **Kerr** | 黑洞参数 $(a,m)$ | 三对角矩阵族 / $N$ 叶谱覆盖 | $(a,m) \mapsto ((a,m), \mathfrak S_{a,m})$ | QNM 频率 $\omega_{lmn}$、谱覆盖的分支点 |
| **Flt** | 味参数 $f$ | 味扇区谱对象 $E_f$ | $f \mapsto (f, E_f)$ | CKM/PMNS 矩阵元、味破坏效应 |

**Cartesian 提升的共同形式**：在分裂纤维化假设下，沿基映射 $p_1 \to p_2$ 的 Cartesian 提升通常取为 $(p_1, E_{p_2}) \to (p_2, E_{p_2})$，谱部分为恒等或参数诱导的显式谱同构。例如 RG 中，$\mu_1 \to \mu_2$ 的提升把 $E_{\mu_2}$ 拉到能标 $\mu_1$ 处而不改变谱数据本身，只改变参数标签。

**常见错误**：
- 把"基空间"和"纤维"混为一谈：基是参数，纤维是该参数点处的谱对象。
- 认为截面必须对应一个可计算的物理量：截面只是函子，它把每个参数点映到总范畴中的一个对象；物理量是从该截面中读出的函数。
- 忽视不同谱丛之间的参数耦合：真实物理系统中温度、能标、噪声可能同时变化，这对应基空间的乘积或更一般的参数空间。

### 6.2 三层伴随对嵌套图

**完整解答**。Paper XIX 中的三层伴随可画为三层"左伴随在左/上、右伴随在右/下"的对应：

```
        D ⊣ R
   Rec_D --------> Sp
        L ⊣ ι
     Rec --------> Rec_id
       Sel ⊣ Diss
   Rec --------> Σ-Rec
```

更精确的方向约定：

- $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 是左伴随，$R: \mathbf{Sp} \to \mathbf{Rec}_D$ 是右伴随；
- $\mathcal L: \mathbf{Rec} \to \mathbf{Rec}_{\text{id}}$ 是左伴随，$\iota: \mathbf{Rec}_{\text{id}} \to \mathbf{Rec}$ 是右伴随；
- $\mathcal Sel: \mathbf{Rec} \to \boldsymbol{\Sigma}\text{-}\mathbf{Rec}$ 是左伴随，$\mathcal Diss: \boldsymbol{\Sigma}\text{-}\mathbf{Rec} \to \mathbf{Rec}$ 是右伴随。

**物理直觉**：

- $D \dashv R$：还原论（谱化）与涌现论（谱重建）的对偶。
- $\mathcal L \dashv \iota$：静态化（遗忘动力学）与包含（只看恒等系统）的对偶。
- $\mathcal Sel \dashv \mathcal Diss$：选择（从噪声中选取信息）与溶解（把系统浸入噪声环境）的对偶。

嵌套关系指的是这些伴随在 UFPF 的大范畴架构中互相衔接：谱化/重建是最内层，静态化/包含是中间层，选择/溶解是最外层处理随机结构。

**常见错误**：
- 把左右伴随方向画反。记忆口诀：**左伴随通常“构造/遗忘前结构”并指向更抽象的右端，右伴随“重建/包含”回到更具体的左端**。
- 把三个伴随误认为是同一范畴之间的伴随：它们分别作用在不同范畴对上。
- 混淆 $\mathcal Sel$ 与 $\mathcal Diss$ 的物理直觉：选择是"从随机中抽取确定性信息"，溶解是"把确定性系统嵌入随机环境"。

### 6.3 未来方向短文

**完整解答示例**。选择 **Kan 延拓**作为未来方向。

**问题陈述**：Paper XXI 给出了六个具体的参数谱丛（Temp、RG、Noise、Sig、Kerr、Flt），但它们目前是分别构造的。一个自然的问题是：能否把不同参数空间上的局部谱丛数据统一地延拓到一个更大的参数空间上？

**Kan 延拓的角色**：Kan 延拓是范畴论中"最佳逼近延拓"的通用构造。给定一个子参数空间 $S \subseteq P$ 上的谱丛 Functor $F: S \to \mathbf{Sp}$，其左/右 Kan 延拓 $\mathrm{Lan}_K F$ 或 $\mathrm{Ran}_K F$ 给出整个参数空间 $P$ 上的"最佳逼近"谱丛。

**与 UFPF 的联系**：

- **Temp + Noise**：把温度和噪声强度组合成二维参数空间，Kan 延拓可把仅在固定噪声下定义的温度谱丛延拓到噪声-温度联合空间。
- **RG + Kerr**：把黑洞参数空间中的局部谱覆盖通过 Kan 延拓拼接到更大范围的参数区域，帮助处理分支点附近的解析延拓。

**研究价值**：如果 Kan 延拓能与 UFPF 的谱流方程相容，它将成为一个统一工具，把 Paper XXI 的六个纤维化实例视为某个全局 Kan 延拓问题的局部片段。

**常见错误**：
- 把 Kan 延拓等同于普通函数延拓：Kan 延拓是范畴意义下的最佳逼近，未必在逐点意义下给出唯一值。
- 忽略左/右 Kan 延拓的区别：左延拓更"自由"，右延拓更"受限"，选择取决于物理上需要保持哪些结构。
- 没有验证延拓后的对象仍落在 $\mathbf{Sp}$ 中：在实际应用中需要检查谱条件和伴随条件是否保持。

---

## 新增练习（第 6 题）提示

**题目**：从三向对照表中选一条，打开对应的 `.lean` 文件，找出其中与论文定理同名的定理/定义。

**示例答案**：
- 选择 Paper I §3 谱对应自然同构 → 打开 `SpectralCorrespondence.lean`
- 寻找定理名如 `spectralCorrespondence` 或 `lambda_mu_correspondence`
- 阅读其类型签名和证明结构，写出 3 行总结

**完整步骤**：

1. 在 `lean/` 目录下找到与所选论文对应的 `.lean` 文件（文件名通常与论文主题对应，如 `SpectralCorrespondence.lean`、`FractalSpectralDerecursion.lean` 等）。
2. 使用文件搜索工具或浏览目录结构定位文件。
3. 打开文件后，寻找 `theorem`、`lemma`、`def` 等关键字。
4. 记录定理/定义的名称、类型签名（参数和结论）以及证明中使用的核心策略（如 `rw`、`simp`、`exact`、`apply`）。
5. 用 3 行文字总结：该结果在论文中的数学含义、Lean 中如何表达、证明的核心思路。

**常见错误**：
- 只看文件名猜测，不打开文件核对。
- 把 `def`（定义）和 `theorem`（定理）混淆。
- 没有注意 Lean 中的 universe 参数和类型类实例，导致对签名的理解出现偏差。

---

## 关键要点

- 习题解答应帮助读者从具体例子过渡到抽象定义。
- Lean 4 代码片段应先从 `Mathlib` 已有结构模仿，再尝试自定义范畴。
- 不要只读解答：先尝试独立证明，再对照检查。
- **自检建议**：每个解答读完后遮住文字，只看题目，能否在 5 分钟内复述出核心步骤和等式？

---

## 7 程序员与形式化视角（选读）

> 本节帮助读者把前六章的习题解答当作“从纸笔证明到 Lean 4 代码”的翻译练习。每个解答中的等式、泛性质、图表，在 Lean 里几乎都对应一个 `def`、`instance` 或 `theorem`。

### 7.1 解答中的范畴论概念与代码对应

下表把前六章习题解答中出现的范畴论概念与程序员熟悉的类型/结构对应起来。这不是严格定义，而是帮助你快速找到“这些解答在代码里长什么样”的直觉：

| 范畴论概念 | 代码直觉 | 在 Lean 4 / Mathlib 中的对应 |
|------------|----------|------------------------------|
| 验证 $\mathbf{Set}$ 满足范畴公理 | 定义一个类型类实例：对象、态射、复合、恒等并证明律 | `Category (Type u)` 实例，`Category` 类型类 |
| 初始对象在同构意义下唯一 | 利用唯一性构造同构，证明逆 | `IsInitial` 与 `isoOfInitial` 类结论 |
| 自然同构的逆也是自然变换 | 对每个对象取逆，验证正方形仍交换 | `NatIso.inv`、自然性 `naturality` |
| 伴随对的两种定义等价 | Hom-集同构 ↔ 单位/余单位 + 三角恒等式 | `Adjunction` 的两种构造器、`Adjunction.mkOfUnitCounit` |
| $\mathbf{Set}$ 中的积与余积 | Cartesian 积 / 不交并，实现投影/注入与泛性质 | `Types.HasProducts`、`Types.HasCoproducts` |
| 等化子 + 有限积 ⟹ 拉回 | 先用 `product` 构造积，再用 `equalizer` 构造等化子 | `limit` 在 `WalkingCospan` 上的实现、`pullback` |
| Eilenberg-Moore 范畴满足范畴公理 | 把代数结构封装成新范畴 | `Monad.Algebra`、EM 范畴 `Monad.EilenbergMoore` |
| $T = \mathcal{L} \circ \iota$ 是恒等函子 | 检查复合后对象不变，得到恒等 | `Functor.id` 与 `Functor.comp` 的自然同构 |
| 常值预层是层 | 验证局域性与粘合条件 | `TopCat.Presheaf.isSheaf`、常值预层 `TopCat.Sheaf.const` |
| Cartesian 提升的万有性质 | 实现“覆盖给定基映射且唯一”的提升 | `IsGrothendieckFibration` 中的 Cartesian 条件 |
| 2-范畴中的水平/垂直复合 | 高阶同构也有两种组合方向 | `CategoryTheory.Bicategory` 中的 `whiskerLeft`、`whiskerRight`、`⊟` |
| $D_2$ 的四条 2-函子公理 | 验证映射保持对象、1-态射、2-态射及两种复合 | `StrictlyUnitaryLaxFunctor` 或自定义伪函子 |
| $\infty$-范畴与同伦 | 把同伦当作可逆高阶映射的近似 | 当前 Mathlib 对 ∞-范畴支持有限，可用 `CategoryTheory.SimplicialObject` 探索 |
| Paper XXI 六个谱丛的截面 | 把参数映射实现为函子，每点返回谱对象 | `Functor` 在参数范畴上的实现，`Prefunctor`/`Functor` |
| 三层伴随对嵌套图 | 三个 `Adjunction` 实例，检查可组合性 | 连续伴随复合 `Adjunction.comp` |
| Kan 延拓作为未来方向 | 给定部分参数空间的 Functor，求最佳逼近延拓 | `Lan`、`Ran`、`pointwiseLeftKanExtension` |

### 7.2 从解答反查 Lean 代码的推荐路径

1. **定位主题**：先看本文件解答属于哪个 Level（范畴基础 / 伴随 / 极限 / 层 / 高阶 / UFPF 应用）。
2. **找到关键词**：上表第三列给出 Mathlib 中的典型定义名，到本地 Lean 库或 [Mathlib 文档](https://leanprover-community.github.io/mathlib4_docs/)搜索。
3. **对照类型签名**：把解答中的数学等式与 Lean 的 `theorem ... : ... :=` 类型签名比较，确认参数和结论的对应关系。
4. **看证明策略**：注意 `rfl`、`simp`、`rw`、`exact`、`apply` 等策略与纸笔证明步骤的对应。

### 7.3 自检小练习

- 对 Level 1 的 $\mathbf{Set}$ 验证，尝试在 Lean 中写出 `Category (Type u)` 实例的四个字段骨架（不强制完成证明）。
- 对 Level 3 的 Kan 延拓，尝试描述 `Lan K F` 在 UFPF 参数空间 $P = T \times \eta$ 上的类型签名。
- 对第 6 题，任选 Paper I–XXI 中的一个定理，写出其对应的 Lean `theorem` 名称猜测、参数列表、返回类型。

> **学习技巧**：把 Part 7 当作“参考答案”使用。读完一个解答后，立刻去查对应的 Mathlib 定义，尝试用 `def`/`theorem` 把解答的核心等式“直译”成 Lean 代码。无需一次性证完，重点是建立“纸笔证明 ↔ 类型签名 ↔ 证明策略”的三向直觉。
