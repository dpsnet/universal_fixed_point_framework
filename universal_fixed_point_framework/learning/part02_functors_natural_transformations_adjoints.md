# Part 2：函子、自然变换与伴随

> 目标：掌握 UFPF 的四大核心范畴论工具——函子、自然变换、伴随对、单位/余单位，能够复述 Paper I 中 $D \dashv R$ 的构造逻辑。

## 2.1 函子

**定义 2.1**（协变函子）。函子 $F: \mathcal{C} \to \mathcal{D}$ 将：
- 对象映射到对象：$X \mapsto F(X)$
- 态射映射到态射：$f: X \to Y \mapsto F(f): F(X) \to F(Y)$

并满足：
- $F(\mathrm{id}_X) = \mathrm{id}_{F(X)}$
- $F(g \circ f) = F(g) \circ F(f)$

**定义 2.2**（反变函子）。反变函子 $F: \mathcal{C}^{\mathrm{op}} \to \mathcal{D}$ 反转复合顺序：$F(g \circ f) = F(f) \circ F(g)$。

### UFPF 实例：谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$

Paper I 定义 2.3.1：对 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R) \in \mathbf{Rec}_D$，

$$D(R) = (\mathcal{H}_R, A_R, \sigma(A_R))$$

其中 $A_R = -\log U_R$，$U_R$ 是 Koopman 演化算子。

对态射 $f: R_1 \to R_2$，$D(f)$ 是相应的谱空间映射。Paper I 命题 2.3.3 证明 $D$ 满足函子律。

### UFPF 实例：静态化函子 $\mathcal{L}: \mathbf{Rec} \to \mathbf{Rec}_{\text{id}}$

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

### UFPF 实例：谱对应自然同构

Paper I 定理 3.7a：在实正自伴情形下，

$$M_0 \cong L_0$$

其中 $M_0$ 是压缩算子的谱乘子，$L_0$ 是生成元谱。这一自然同构将数值等式 $\lambda_i = e^{-\mu_i}$ 提升为范畴论陈述。

Paper I 定理 3.7b：复耗散情形下为**辫子自然同构**：

$$M^{\text{br}} \cong_{\text{br}} L^{\text{br}}$$

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

### UFPF 实例：$D \dashv R$

Paper I 定理 2.4.5：谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 有右伴随 $R: \mathbf{Sp} \to \mathbf{Rec}_D$。

- $D$（左伴随）：将递归系统谱化，对应"向下归约"到谱数据
- $R$（右伴随）：从谱数据重建递归系统，对应"向上提升"

Paper I 哲学版将这一伴随提升为还原论/涌现论的数学对应。

### UFPF 实例：三层伴随对嵌套

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

### UFPF 实例

Paper I 证明 $D$ 是忠实函子（命题 2.3.3）。这意味着不同的递归系统态射不会谱化为相同的谱态射——谱化不丢失态射层面的信息。

## 2.5 等价与伴随的关系

若 $L \dashv R$ 且单位、余单位都是自然同构，则 $L$ 与 $R$ 构成范畴等价。在 UFPF 中，$D \dashv R$ 通常不是等价，因为：
- 不同的递归系统可能有相同谱（非忠实？不，$D$ 是忠实的但非完全）
- 谱范畴中的对象不一定都能由递归系统生成

这解释了为什么 $\mathbf{Sp}$ 是 $\mathbf{Rec}_D$ 的反射子范畴（命题 2.4.4），而非等价子范畴。

## 2.6 练习

1. 证明 Paper I 中 $D$ 的函子律：$D(\mathrm{id}_R) = \mathrm{id}_{D(R)}$ 与 $D(g \circ f) = D(g) \circ D(f)$。
2. 验证自然变换 $\eta_R: M_0 \to L_0$ 的交换图（Paper I §3.4a）。
3. 用伴随的 Hom 集合定义，解释为什么 $D \dashv R$ 中 $D$ 是左伴随、$R$ 是右伴随。
4. 在 Paper XIX 的三层伴随对嵌套中，指出每个左伴随和右伴随的"物理直觉"（如遗忘、构造、选择、溶解）。
5. 若 $D$ 是忠实但非完全的，说明 $\mathbf{Sp}$ 比 $\mathbf{Rec}_D$ "更大"还是"更小"？

## 2.7 关键要点

- **函子**是范畴之间的结构保持映射，UFPF 的核心操作（谱化、静态化、选择）都是函子。
- **自然变换**比较两个函子，UFPF 中的谱对应 $\lambda_i = e^{-\mu_i}$ 被提升为自然同构。
- **伴随对**是 UFPF 的哲学与数学核心，$D \dashv R$ 编码还原论/涌现论的对偶。
- 左伴随通常"构造/遗忘前结构"，右伴随通常"重建/添加结构"，但具体方向需由 Hom 集合定义验证。
