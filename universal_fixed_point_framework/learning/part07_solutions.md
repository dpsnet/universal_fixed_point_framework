# Part 7 习题：解答与提示

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

**提示**：画出 2-胞复合图。中间交换律（interchange law）说明先水平复合再垂直复合，等于先垂直复合再水平复合。

### 5.2 $D_2$ 的四条 2-函子公理

**提示**：
1. 保持对象
2. 保持 1-态射
3. 保持 2-态射的垂直复合
4. 保持 2-态射的水平复合

具体等式见 Paper V 定理 8.1 证明。

### 5.3 ∞-范畴与同伦

**提示**：所有高阶态射可逆意味着它们不是"真正不同的映射"，而是"映射之间的连续变形"。这正是同伦论的直觉。

### 6.1 Paper XXI 六个纤维化的物理截面

**提示示例**：
- **Temp**：$T \mapsto (T, A_T)$，可观测量 $T_c$
- **RG**：$\mu \mapsto (\mu, A_\mu)$，可观测量 $\alpha_s(\mu)$
- **Noise**：$\eta \mapsto (\eta, A_\eta)$，可观测量退相干率
- **Sig**：$(p,q) \mapsto ((p,q), \mathrm{Cl}(p,q))$，可观测量旋量表示
- **Kerr**：$(a, m) \mapsto ((a,m), \mathfrak{S}_{a,m})$，可观测量 QNM 频率
- **Flt**：味参数 $f \mapsto (f, A_f)$，可观测量 CKM/PMNS 矩阵元

### 6.2 三层伴随对嵌套图

**提示**：

```
        D ⊣ R
       /       \
   Rec -----> Sp

      L ⊣ iota
      /      \
  Rec ----> Rec_id

    Sel ⊣ Diss
     /        \
Rec -------> Sigma-Rec
```

其中左伴随在左/上，右伴随在右/下。

### 6.3 未来方向短文

**提示**：例如选择 **Kan 延拓**。UFPF 中不同参数空间（Temp、RG、Noise）上的谱丛目前分别构造。Kan 延拓可能给出一种统一方法，从局部定义的谱丛Functor延拓到全局，从而把 Paper XXI 的六个纤维化实例统一为某个 Kan 延拓问题的特例。

---

## 新增练习（第 6 题）提示

**题目**：从三向对照表中选一条，打开对应的 `.lean` 文件，找出其中与论文定理同名的定理/定义。

**示例答案**：
- 选择 Paper I §3 谱对应自然同构 → 打开 `SpectralCorrespondence.lean`
- 寻找定理名如 `spectralCorrespondence` 或 `lambda_mu_correspondence`
- 阅读其类型签名和证明结构，写出 3 行总结

---

## 关键要点

- 习题解答应帮助读者从具体例子过渡到抽象定义。
- Lean 4 代码片段应先从 `Mathlib` 已有结构模仿，再尝试自定义范畴。
- 不要只读解答：先尝试独立证明，再对照检查。
