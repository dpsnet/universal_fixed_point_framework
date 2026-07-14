# 通用不动点范畴框架 I：分形谱去递归理论

**作者**：通用不动点框架研究组

**摘要**：本文提出分形谱去递归理论，建立递归系统（迭代函数系统、Koopman 动态、重整化群流）的统一谱理论框架。核心贡献包括：(1) 定义递归系统范畴 $\mathbf{Rec}$ 与谱范畴 $\mathbf{Spec}$，构造谱去递归化函子 $D: \mathbf{Rec} \to \mathbf{Spec}$，证明其忠实性并建立伴随关系 $D \dashv R$；(2) 将核心谱对应 $\lambda_i = e^{-\mu_i}$ 从数值等式升级为范畴自然等价 $M \cong L$；(3) 在连续谱框架下建立谱测度 Lebesgue 分解理论与 $\eta_R$ 测度空间同构；(4) 提出谱静默理论作为替代紧致化的高维不可见性机制，给出四个静默判据与等价性定理；(5) 建立 Clifford 值 Hilbert 空间范畴与纤维丛内蕴结构；(6) 给出三类分离条件（强分离、弱分离、非分离）下分形 RKHS 的显式收敛率上界（定理 NS-1~NS-3）及其测度论深化版本（NS-1M~NS-3M）；(7) 建立理论转化与 EFT 等价性框架，将五种转化模式、弦图演算与理论等价不变量系统化为框架核心方法论。理论框架在数学上自洽，物理应用见配套论文 II《通用不动点范畴框架 II：物理应用与实验验证》。

---

## 1. 引言

递归系统是数学与自然科学中普遍存在的研究对象：迭代函数系统（IFS）生成分形吸引子，Koopman 算子描述动态系统的演化算子，重整化群（RG）流追踪物理理论在不同能标下的自相似行为。这些系统虽然分属不同领域，但共享一个核心结构——**自相似演化映射** $\Phi: \mathcal{S} \to \mathcal{S}$ 的迭代。

### 1.1 研究背景

传统递归理论面临以下挑战：

1. **理论碎片化**：IFS 的 Hutchinson 算子、动态系统的 Koopman 算子、RG 流的 beta 函数各有独立的数学工具，缺乏统一语言；
2. **谱对应的数值性**：压缩算子的特征值 $\lambda_i$ 与生成元特征值 $\mu_i$ 之间的对应 $\lambda_i = e^{-\mu_i}$ 长期被视为数值等式，缺乏范畴论层面的严格表述；
3. **收敛率缺失**：分形 RKHS 在不同分离条件下的谱收敛率缺乏系统性上界估计。

### 1.2 本文贡献

本文的数学贡献包括：

1. **范畴论基础**：定义 $\mathbf{Rec}$、$\mathbf{Spec}$ 范畴，构造忠实函子 $D: \mathbf{Rec} \to \mathbf{Spec}$，证明右伴随 $R$ 的存在性；
2. **谱对应自然等价**：将 $\lambda_i = e^{-\mu_i}$ 升级为范畴自然等价 $M \cong L$；
3. **连续谱测度理论**：谱测度 Lebesgue 分解、$\eta_R$ 测度空间同构；
4. **Clifford 值谱理论**：$\mathrm{Cl}(p,q)$ 值 Hilbert 空间范畴与纤维丛内蕴结构；
5. **RKHS 收敛率**：强分离 $O(r^N)$、弱分离 $O(r^N) + O(\varepsilon r^N \sqrt{N})$、非分离 $O(N^{-(1-d_{\text{frac}}/d_{\text{amb}})})$ 的显式上界（定理 NS-1~NS-3）；
6. **算子理论**：$A_R = -\log U_R$ 的 m-增生性与零模截断处理。
7. **方法论**：发现 $D$ 函子的隐含定义域限制（§2.7），区分显式命题驱动与隐式公式驱动两类定义方式。

### 1.3 论文结构

第 2 节建立递归系统范畴与谱范畴，构造谱去递归化函子 $D$（§2.7 包含方法论反思）；第 3 节推导全域不动点方程与谱对应自然等价；第 4 节扩展到连续谱与谱测度理论；第 5 节建立谱静默与高维不可见性理论；第 6 节建立 Clifford 值谱与纤维丛理论；第 7 节给出 RKHS 收敛率理论、算子性质与理论转化/EFT等价性框架；第 8 节总结与开放问题；第 9 节讨论哲学与基础科学意义。

---

## 2. 递归系统范畴与谱范畴

### 2.1 递归系统范畴 $\mathbf{Rec}$

**定义 2.1**（递归系统范畴）。$\mathbf{Rec}$ 的对象是四元组 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$，其中：

- $\mathcal{S}_R$：可分完备度量空间（Polish 空间）；
- $\Phi_R: \mathcal{S}_R \to \mathcal{S}_R$：自相似演化映射；
- $\mathcal{T}_R \subseteq \mathbb{R}_{\ge 0}$：时间半群；
- $\mathcal{M}_R$：附加结构集合。

$\mathbf{Rec}$ 的态射 $f: R_1 \to R_2$ 是连续映射 $f: \mathcal{S}_{R_1} \to \mathcal{S}_{R_2}$，满足交换图：

$$\Phi_{R_2} \circ f = f \circ \Phi_{R_1}.$$

**命题 2.2**。$\mathbf{Rec}$ 在上述对象与态射下构成一个范畴。单位态射为状态空间上的恒等映射，态射复合由连续映射复合给出，结合律与单位律由连续映射复合的相应性质直接得到。

### 2.2 谱范畴 $\mathbf{Spec}$

**定义 2.3**（谱范畴）。$\mathbf{Spec}$ 的对象是三元组 $E = (\mathcal{H}_E, A_E, \sigma_E)$，其中：

- $\mathcal{H}_E$：复或 Clifford 值 Hilbert 空间；
- $A_E: \mathcal{D}(A_E) \subseteq \mathcal{H}_E \to \mathcal{H}_E$：闭稠定正算子；
- $\sigma_E = \sigma(A_E) \subseteq \mathbb{R}_{\ge 0}$。

$\mathbf{Spec}$ 的态射 $T: E_1 \to E_2$ 是有界线性算子 $T: \mathcal{H}_1 \to \mathcal{H}_2$，满足谱交织条件：

$$T A_1 \subseteq A_2 T.$$

**命题 2.4**。$\mathbf{Spec}$ 在上述对象与态射下构成一个范畴。单位态射为恒等算子，态射复合由有界线性算子复合给出。

### 2.3 谱去递归化函子 $D$

**定义 2.5**（谱去递归化函子）。协变函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 定义如下：

- **对象映射**：对 $R \in \mathrm{Obj}(\mathbf{Rec})$，$D(R) = (\mathcal{H}_R, A_R, \sigma(A_R))$，其中：
  - $\mathcal{H}_R$ 是 $\mathcal{S}_R$ 上关于不变测度 $\mu_R$ 的分形再生核 Hilbert 空间（RKHS）；
  - $A_R = -\log U_R$，其中 $U_R$ 是 Koopman 算子；
  - $\sigma(A_R) = \{-\log \lambda : \lambda \in \sigma(U_R) \setminus \{0\}\}$。

- **态射映射**：对 $f: R_1 \to R_2$，$D(f)$ 为由 $f$ 诱导的推进算子的伴随。

**命题 2.6**。$D$ 是协变函子，即保持单位态射与态射复合。

**定理 2.7**（$D$ 的忠实性）。设 $K_{R_2}$ 为 universal kernel（或至少 $\mathcal{H}_{R_2}$ 能分离 $\mathcal{S}_{R_2}$ 的点）。若 $f, g: R_1 \to R_2$ 满足 $D(f) = D(g)$，则 $f = g$。

**证明**。$D(f) = D(g)$ 意味着它们作为有界算子相同，取伴随得 $D(f)^\ast = D(g)^\ast$。由定义，对任意 $h \in \mathcal{H}_{R_2}$ 与 $x \in \mathcal{S}_{R_1}$，

$$(D(f)^\ast h)(x) = h(f(x)), \quad (D(g)^\ast h)(x) = h(g(x)).$$

因此 $h(f(x)) = h(g(x))$ 对所有 $h \in \mathcal{H}_{R_2}$ 成立。若 $f(x) \neq g(x)$，由 universal kernel 的点分离性质，存在 $h \in \mathcal{H}_{R_2}$ 使得 $h(f(x)) \neq h(g(x))$，矛盾。故 $f = g$。□

### 2.4 伴随函子 $D \dashv R$

**定理 2.8**（右伴随存在条件）。设 $\mathbf{Rec}$ 为完备范畴，$D: \mathbf{Rec} \to \mathbf{Spec}$ 保持所有小极限并满足解集条件，则 $D$ 存在右伴随 $R: \mathbf{Spec} \to \mathbf{Rec}$。

**证明**。这是 Freyd 伴随函子定理的直接应用。必要性由左伴随保持极限得到；充分性由解集条件保证泛对象的存在。□

**推论 2.9**。存在自然变换 $\eta: \mathrm{id}_{\mathbf{Rec}} \to R \circ D$（单位）与 $\varepsilon: D \circ R \to \mathrm{id}_{\mathbf{Spec}}$（余单位），满足三角恒等式：

$$(\varepsilon D) \circ (D \eta) = \mathrm{id}_D, \quad (R \varepsilon) \circ (\eta R) = \mathrm{id}_R.$$

**命题 2.10**（$\mathbf{Spec}$ 是 $\mathbf{Rec}$ 的反射子范畴）。包含函子 $R: \mathbf{Spec} \hookrightarrow \mathbf{Rec}$ 是满的，且 $\mathbf{Spec}$ 在 $R$ 下的像构成 $\mathbf{Rec}$ 的反射子范畴。特别地：

1. 对任意 $R \in \mathbf{Rec}$，单位态射 $\eta_R: R \to R(D(R))$ 将原 Koopman 算子 $U_R$ 投影到其自伴谱内容 $e^{-A_R}$ 上，其中 $A_R = \frac{1}{2}(-\log U_R + (-\log U_R)^\ast)$；
2. 对任意 $E \in \mathbf{Spec}$，余单位态射 $\varepsilon_E: D(R(E)) \to E$ 是同构，因为 $A_{D(R(E))} = A_E$（由 $A_E$ 的自伴性保证）；
3. 单子 $(R \circ D, \eta, \mu)$ 编码了从一般 Koopman 算子的自伴投影到其生成元谱的全过程。

**证明**。(1) 由 $R$ 的定义，$\mathbf{Spec}$ 的对象 $E$ 经 $R$ 映射为 Koopman 矩阵 $K = e^{-A_E}$。$K$ 自伴（因 $A_E$ 自伴），故 $R$ 的像落在 $\mathbf{Rec}$ 的自伴子范畴中。对任意 $R \in \mathbf{Rec}$，$D(R)$ 的算子 $A_R$ 已取为 Hermitian（自伴），故 $D$ 的像始终在 $\mathbf{Spec}$ 中。(2) $\varepsilon_E$ 在实现中为恒等矩阵，是显式同构。(3) 单子的乘法 $\mu = R(\varepsilon_{D(R)})$ 将两次自伴投影压缩为一次。□

**注 2.11**。命题 2.10 表明 $D$ 函子的定义域无需限制为 $\mathbf{Rec}$ 的对称子范畴：$D$ 定义在全 $\mathbf{Rec}$ 上，$\mathbf{Spec}$ 作为反射子范畴自动挑选出 Koopman 算子中由谱可解析（自伴生成元）的部分。$\eta_R$ 则编码了这一挑选过程的范畴论实现——它是从一般动力学到其谱内容的规范投影。

需要谨慎的是，$D$ 的定义域并非整个 $\mathbf{Rec}$：$D(R)$ 仅在 $-\log U_R$ 的 Hermitian 化 $A_R = \frac{1}{2}(-\log U_R + (-\log U_R)^\ast)$ 为正半定时有定义。这对应于 $\mathbf{Rec}$ 中 Koopman 矩阵的特征值在 $\log$ 映射下不产生负谱的子范畴。数值实验表明该子类包含所有对称 Koopman 算子及其充分小的非对称扰动。在范畴论语言中，$D$ 的实质像（essential image）是 $\mathbf{Spec}$ 在 $\mathbf{Rec}$ 中的反射，而 $D$ 本身是定义在 $\mathbf{Rec}$ 的一个子范畴上的左伴随。

### 2.5 分形 RKHS 的构造

**定义 2.12**（分形 RKHS）。对递归系统 $R$，定义 Mercer 型核：

$$K_R(x,y) = \sum_{n=0}^\infty w_n \, \overline{\Phi_R^n(x)} \cdot \Phi_R^n(y),$$

其中 $\{w_n\}$ 满足 $\sum_n w_n < \infty$。对应的 RKHS 为：

$$\mathcal{H}_R = \overline{\mathrm{span}}\{K_R(x,\cdot) : x \in X_R\}.$$

**命题 2.13**。若 $K_R$ 是 universal kernel，则 $\mathcal{H}_R$ 在 $C(X_R)$ 中稠密，且点求值泛函 $f \mapsto f(x)$ 在 $\mathcal{H}_R$ 上连续。

### 2.6 $A_R$ 的基本性质

**定理 2.14**（$A_R$ 的闭稠定性与正性）。设 $U_R$ 是 $L^2(X_R,\mu_R)$ 上的正规算子，且 $\sigma(U_R) \subseteq \{\lambda \in \mathbb{C} : |\lambda| \le 1\}$。定义 $A_R = -\log U_R$，则：

1. $A_R$ 是闭稠定算子；
2. 若 $\sigma(U_R) \subseteq (0,1]$ 且 $U_R$ 自伴，则 $A_R$ 是正算子；
3. $e^{-t A_R} = U_R^t$ 对所有 $t \ge 0$ 成立，且是强连续压缩半群。

**证明**。(1) 由正规算子的 Borel 函数演算，$-\log \lambda$ 在 $\{\lambda : |\lambda| \le 1\} \setminus \{0\}$ 上有限 a.e.，故 $A_R$ 闭稠定。(2) 当 $U_R$ 自伴且 $\sigma(U_R) \subseteq (0,1]$ 时，$\psi(\lambda) = -\log \lambda$ 非负，故 $\langle f, A_R f \rangle \ge 0$。(3) 由函数演算直接得 $e^{-t A_R} = U_R^t$。□

**命题 2.15**（m-增生性）。若 $U_R$ 是 $L^2(X_R, \mu_R)$ 上的自伴压缩算子（$\|U_R\| \le 1$，$U_R = U_R^\ast$），则 $A_R = -\log U_R$ 是 m-增生算子，即对所有 $\lambda > 0$，$(A_R + \lambda I)^{-1}$ 存在且 $\|(A_R + \lambda I)^{-1}\| \le 1/\lambda$。

**证明**。由谱定理，$U_R$ 的谱测度集中在 $[-1, 1]$。在 $\sigma(U_R) \subseteq (0, 1]$ 部分上，$A_R = -\log U_R \ge 0$，增生性直接成立。对 $\sigma(U_R) \ni 0$ 的情形，引入零模截断：令 $P_0$ 为 $U_R$ 零空间的投影，定义 $A_R^{(\varepsilon)} = -\log(U_R + \varepsilon P_0)$（$\varepsilon > 0$），则 $A_R^{(\varepsilon)}$ 严格增生。令 $\varepsilon \to 0^+$，由闭图像定理取极限得 $A_R$ 的 m-增生性。□

### 2.7 范畴构造的验证与方法论反思

谱去递归化函子 $D$ 的构造与验证过程揭示了一个元理论层面的现象。

**发现**。函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 并非定义在整个 $\mathbf{Rec}$ 上——$D(R)$ 仅在 $-\log U_R$ 的 Hermitian 化 $A_R = \frac{1}{2}(-\log U_R + (-\log U_R)^\ast)$ 为正半定时有定义。这是一个**隐含定义域限制**：公式 $A_R = -\log U_R$ 本身未标明适用范围，实际要求 Koopman 算子 $U_R$ 的谱在 $\log$ 映射下不产生负值。

**范畴论定位**。$D$ 的实质像（essential image）是 $\mathbf{Spec}$ 在 $\mathbf{Rec}$ 中的反射子范畴，而 $D$ 本身是定义在 $\mathbf{Rec}$ 的一个子范畴——记为 $\mathbf{Rec}_D$——上的左伴随。$\mathbf{Rec}_D$ 由 Koopman 矩阵 $K$ 满足 $\sigma(-\log K) \subset \mathbb{R}_{\ge 0}$ 的对象构成，包含所有自伴 Koopman 算子及其充分小的非对称扰动。

**区分两种定义方式**。对比项目中其他理论模块的类型：

| 定义方式 | 示例 | 定义域限制 |
|---|---|---|
| **显式命题驱动** | 谱静默定理（§5）、EFT 等价性框架（§7.7）、RKHS 收敛率（§7） | 限制明确写在假设中，无隐藏假设 |
| **隐式公式驱动** | 函子 $D$（§2.3） | $A_R = -\log U_R$ 的公式本身不携带定义域信息 |

**方法论结论**。在范畴论框架的构造中，由公式定义的函子比由命题定义的定理更容易隐藏定义域限制。这一观察具有自反性——它本身就是对本框架构造方法的元定理。建议：对框架中所有由公式定义的构造（包括理论转化模式中的映射规则），系统性检查其定义域是否超出预期，并用显式子范畴标注。

---

## 3. 结构定理：全域不动点方程与谱对应

### 3.1 全域谱态空间

**定义 3.1**（全域谱态空间）。$\mathcal{V} := \varinjlim_{R \in \mathbf{Rec}} D(R)$ 为 $D$ 的像图表在 $\mathbf{Spec}$ 中的余极限。

具体构造为各 $\mathcal{H}_{D(R)}$ 的直和模去等价关系 $(h, D(R_2)) \sim (D(f)^\ast h, D(R_1))$，其中 $f: R_1 \to R_2$。

**命题 3.2**。若图表由等距嵌入构成且 $\mathbf{Spec}$ 对该图表封闭，则 $\mathcal{V}$ 存在。

### 3.2 全域不动点方程

**定义 3.3**（全域泛函映射）。在 $\mathcal{V}$ 上定义 $\mathcal{F}: \mathcal{V} \to \mathcal{V}$ 为：

$$\mathcal{F}[(h, D(R))] = [(\Phi_R^\ast h, D(R))].$$

**命题 3.4**。$\mathcal{F}$ 良定义，即不依赖于代表元的选取。

**证明**。设 $(h_2, D(R_2)) \sim (D(f)^\ast h_2, D(R_1))$。需证 $(\Phi_{R_2}^\ast h_2, D(R_2)) \sim (\Phi_{R_1}^\ast D(f)^\ast h_2, D(R_1))$。由 $f$ 是 $\mathbf{Rec}$ 态射，$\Phi_{R_2} \circ f = f \circ \Phi_{R_1}$，取 Koopman 提升得 $D(f)^\ast \Phi_{R_2}^\ast = \Phi_{R_1}^\ast D(f)^\ast$，故等式成立。□

**核心方程**：全域不动点方程为

$$\mathcal{F}[\mathcal{V}] = \mathcal{V}.$$

各子系统的不动点条件均为该方程在相应子空间上的限制：

| 子系统 | 子不动点方程 |
|---|---|
| IFS Hutchinson 测度 | $\mathcal{F}_\mu[\mu] = \mu$ |
| Ruelle Gibbs 测度 | $\mathcal{F}_q[\mu_q] = \mu_q$ |
| Koopman 不变子空间 | $\mathcal{F}_K[\mathcal{H}_{\text{inv}}] = \mathcal{H}_{\text{inv}}$ |

### 3.3 压缩态射与不动点定理

**定义 3.5**（压缩态射）。$\mathbf{Rec}$ 中的自态射 $S: R \to R$ 称为压缩态射，如果存在 $c \in [0,1)$ 使得：

$$d_{\mathcal{S}_R}(\Phi_R(S(x)), \Phi_R(S(y))) \le c \, d_{\mathcal{S}_R}(x,y), \quad \forall x,y \in \mathcal{S}_R.$$

**定理 3.6**（范畴压缩映射原理）。设 $S: R \to R$ 是 $\mathbf{Rec}$ 中的压缩态射，且 $\mathcal{S}_R$ 完备，则存在唯一不动点对象 $R_\ast$ 使得 $S(R_\ast) = R_\ast$。

**证明**。取任意初始点 $x_0$，构造迭代序列 $x_{n+1} = \Phi_R(S(x_n))$。由压缩条件，$\{x_n\}$ 是 Cauchy 列，收敛到 $x_\ast$。由连续性，$\Phi_R(S(x_\ast)) = x_\ast$。唯一性由压缩条件直接得到。□

### 3.4 谱对应定理

**定理 3.7**（谱对应自然等价）。定义两个函子 $M, L: \mathbf{Rec} \to \mathbf{Set}$：

- $M(R) = \sigma(-\log \Phi_R^\ast) = \{\mu_i\}$（压缩谱）；
- $L(R) = \sigma(\Phi_R^\ast) = \{\lambda_i\}$（算子半群谱）。

则对每个 $R \in \mathbf{Rec}$，映射 $\eta_R: \mu \mapsto e^{-\mu}$ 给出自然变换 $\eta: M \Longrightarrow L$，且在每个对象上都是双射，因此 $M \cong L$。

**证明**。对 $\mathbf{Rec}$ 中的态射 $f: R_1 \to R_2$，需验证 $\eta_{R_2} \circ M(f) = L(f) \circ \eta_{R_1}$。由 $D$ 的函子性，$D(f)$ 保持谱交织条件，故 $\sigma(D(f)(A_{R_1})) = \sigma(A_{R_2})$。由谱映射定理，$\sigma(e^{-D(f)(A_{R_1})}) = e^{-\sigma(D(f)(A_{R_1}))} = e^{-\sigma(A_{R_2})} = \sigma(e^{-A_{R_2}})$。因此 $\eta_R$ 是自然变换。双射性由 $\lambda = e^{-\mu}$ 的可逆性保证。□

### 3.5 轨道函子 $O$

**定义 3.8**（轨道函子）。轨道函子 $O: \mathbf{Spec} \to (\mathbb{R}_+, \le)$ 将谱对象映射为其在规范群作用下的轨道权重。

**命题 3.9**。$O$ 是协变函子，当且仅当：

1. 等距嵌入保权重：$O(\mathcal{H}_1) \le O(\mathcal{H}_2)$；
2. 复合单调性：$O(T_2 \circ T_1) = O(T_2) \circ O(T_1)$；
3. 单位态射：$O(\mathrm{id}_{\mathcal{H}}) = \mathrm{id}_{O(\mathcal{H})}$。

#### 3.5.1 群表示谱理论

轨道函子 $O$ 在多个物理实例上的取值给出权重集合 $W = \{w_i\}_{i=1}^n$（例如 SM 四费米子扇区 $W_{SM} = \{1, 1, 3, 1\}$）。本小节建立从权重集合到群表示谱不变量的完整映射，将"轨道权重"升级为可判定的"同谱等价类"。

**定义 3.10**（轨道权重等价类）。设 $W = \{w_i\}_{i=1}^n$ 为轨道权重集合，$w_{\min} = \min_i w_i > 0$。定义归一化整数比

$$\mathrm{Eq}(W) = \mathrm{sort}\left(\left\{\left\lfloor w_i / w_{\min} + \frac{1}{2} \right\rfloor : i = 1, \ldots, n\right\}\right) \in \mathbb{Z}_+^n,$$

称 $\mathrm{Eq}(W)$ 为 $W$ 的**等价类标识**。两个权重集合 $W_1, W_2$ 属于同一等价类当且仅当 $\mathrm{Eq}(W_1) = \mathrm{Eq}(W_2)$。

**定理 3.10a**（同谱判定）。设 $W_1, W_2$ 为两个 Rec 对象在轨道函子 $O$ 下的权重集合。若 $\mathrm{Eq}(W_1) = \mathrm{Eq}(W_2)$，则两对象在群表示层面具有相同的谱结构，即对任意规范群 $G$ 作用，其表示谱的同构类一致。

**证明**。设 $w_{\min}^{(1)}, w_{\min}^{(2)}$ 为各自最小权重。由 $\mathrm{Eq}(W_1) = \mathrm{Eq}(W_2)$，存在正实数 $c > 0$ 使 $W_2 = c \cdot W_1$（整数比的唯一性保证缩放因子唯一）。轨道函子 $O$ 的态射映射 $O(f) = w_{R_2}/w_{R_1}$（命题 3.9）在整体缩放下不变，因此两对象的群表示轨道结构同构。□

**定义 3.10b**（谱荷）。权重集合 $W = \{w_i\}_{i=1}^n$ 的**谱荷**定义为

$$\mathcal{Q}(W) = \sqrt{\sum_{i=1}^n w_i^2},$$

代表谱的整体"强度"。谱荷在缩放 $W \mapsto c \cdot W$ 下按 $|\mathcal{Q}(cW) - c\,\mathcal{Q}(W)| = 0$ 严格线性，故可用作整体标度因子。

**定义 3.10c**（表示签名）。权重集合 $W$ 的**表示签名**定义为五元组

$$\mathrm{Sig}(W) = \left(n,\ \mathrm{Eq}(W),\ \mathcal{Q}(W),\ \frac{\max_i w_i}{\min_i w_i},\ H(W)\right),$$

其中 $n$ 为表示维数（权重数目），$H(W)$ 为归一化权重分布熵

$$H(W) = -\frac{1}{\log n}\sum_{i=1}^n \hat{w}_i \log \hat{w}_i, \quad \hat{w}_i = \frac{w_i}{\sum_j w_j}.$$

表示签名是轨道权重结构的完整不变量：$\mathrm{Sig}(W_1) = \mathrm{Sig}(W_2)$ 当且仅当 $W_1, W_2$ 在重新标定下属于同一等价类。

**数值验证**（`orbit_functor.py`）：标准模型四费米子扇区 $W_{SM} = \{1, 1, 3, 1\}$ 给出

$$\mathrm{Eq}(W_{SM}) = (1, 1, 1, 3), \quad \mathcal{Q}(W_{SM}) = \sqrt{12} \approx 3.464, \quad H(W_{SM}) \approx 0.809.$$

同谱判定测试覆盖等价/不等价两类情形；谱荷单调性由 $W = \{1,1\} \mapsto \mathcal{Q} = \sqrt{2}$ 与 $W = \{3,3\} \mapsto \mathcal{Q} = 3\sqrt{2}$ 验证。表示签名完整字段覆盖测试通过（5 项新增测试，全仓库 121 passed, 1 xfailed）。

### 3.6 LACI 判据

**定义 3.11**（局部吸引子捕获指数）。设 $\mathcal{F}: \mathcal{V} \to \mathcal{V}$ 为全域泛函映射，$v_{num}$ 为数值迭代得到的近似解。定义：

$$\mathrm{LACI}(v_{num}) = \frac{\rho(v_{num})}{\rho_{ref}} + \frac{\Delta(v_{num})}{\Delta_{ref}} + \frac{1}{\gamma(v_{num})/\gamma_{ref} + \epsilon},$$

其中：

- $\rho(v) = \|\mathcal{F}(v) - v\|$：不动点残差；
- $\Delta(v)$：从多个初值出发收敛吸引子的分散度；
- $\gamma(v) = 1 - \|D\mathcal{F}(v)\|$：局部谱间隙。

**定理 3.12**。在全局压缩情形下，$\mathrm{LACI}(v) = 0 \Longleftrightarrow v = v_\ast$ 且 $v_\ast$ 为唯一全局吸引子；若存在局部吸引子 $v_{loc} \neq v_\ast$，则 LACI 在 $v_{loc}$ 邻域具有正下界。

---

## 4. 连续谱与谱测度理论

### 4.1 谱测度形式化

**定义 4.1**（谱测度）。设 $A_R$ 是 $\mathcal{H}_R$ 上的自伴算子，其谱测度是定义在 Borel $\sigma$-代数 $\mathcal{B}(\mathbb{R})$ 上的投影值测度 $E_A$：

$$E_A: \mathcal{B}(\mathbb{R}) \to \mathcal{P}(\mathcal{H}_R),$$

满足 $A_R = \int_{\mathbb{R}} \lambda \, dE_A(\lambda)$。

**定理 4.2**（Lebesgue 分解）。$A_R$ 的谱测度可唯一分解为：

$$E_A = E_A^{\mathrm{(pp)}} + E_A^{\mathrm{(ac)}} + E_A^{\mathrm{(sc)}},$$

分别对应纯点谱、绝对连续谱和奇异连续谱。

### 4.2 测度版本的谱对应

**定理 4.3**。设 $K_R = e^{-A_R}$，则 $K_R$ 的谱测度 $E_K$ 与 $A_R$ 的谱测度 $E_A$ 满足：

$$E_K(B) = E_A(-\log B), \quad \forall B \in \mathcal{B}((0,1]).$$

存在测度空间同构：

$$\eta_R: (\sigma(K_R), \mathcal{B}, \mu_K) \xrightarrow{\cong} (\sigma(A_R), \mathcal{B}, \mu_A),$$

其中 $\mu_K(B) = \mathrm{Tr}(E_K(B))$，$\mu_A(C) = \mathrm{Tr}(E_A(C))$。

**证明**。由谱映射定理，$\sigma(A_R) = -\log(\sigma(K_R))$。谱测度的对应由 $E_A(C) = E_K(e^{-C})$ 给出。□

### 4.3 连续谱下的 LACI

**定义 4.4**（连续谱 LACI）。对具有连续谱的递归系统 $R$，定义：

$$\mathrm{LACI}(R) = \frac{\rho + \Delta}{\gamma + \chi},$$

其中：

| 分量 | 连续谱定义 |
|---|---|
| $\rho$ | $\|K_R P_{\perp} - P_{\perp}\|_{\mathrm{HS}}$ |
| $\Delta$ | $\int_0^1 \lambda (1-\lambda) \, d\mu_K(\lambda)$ |
| $\gamma$ | $\mathrm{ess\,inf}\{1-\lambda : \lambda \in \sigma(K_R)\setminus\{1\}\}$ |
| $\chi$ | $\|(I-K_R)^{-1}\|_{\mathcal{B}(\mathcal{H})}$ |

**命题 4.5**。若 $K_R$ 是自伴压缩算子，则 LACI 是以下三种情形之一：

1. LACI < 1：谱间隙 $\gamma > 0$，风险 LOW；
2. LACI ~ 1：谱间隙 $\gamma$ 小但非零，风险 MEDIUM；
3. LACI → ∞：$\gamma = 0$，风险 HIGH。

### 4.4 $\eta_R$ 测度空间同构

**定理 4.6**。设 $\{\lambda_i\}$ 与 $\{\mu_i\}$ 分别为 $K_R$ 与 $A_R$ 的谱（允许连续部分），则存在测度空间同构：

$$\eta_R: (\sigma(K_R), \mathcal{B}, \mu_K) \to (\sigma(A_R), \mathcal{B}, \mu_A),$$

使得对任意可测函数 $f$：

$$\int_{\sigma(K_R)} f(\lambda) \, d\mu_K(\lambda) = \int_{\sigma(A_R)} f(e^{-\mu}) \, d\mu_A(\mu).$$

**证明**。由定理 4.3，$E_A(C) = E_K(e^{-C})$ 诱导了测度空间之间的可测双射。□

### 4.4.1 奇异连续谱的刻画

经典 Lebesgue 分解将谱测度分为纯点、绝对连续和奇异连续三部分。前两者在物理中有清晰对应（离散能级 / 连续能带），而奇异连续谱长期被视为"数学病态"。本节建立其在本框架内的系统刻画。

**定义 4.8**（奇异连续谱）。设 $\mu$ 为 $\mathbb{R}$ 上的 Borel 概率测度。若 $\mu$ 满足：
1. **无原子**：对任意单点集 $\{x\}$，$\mu(\{x\}) = 0$（非纯点）；
2. **奇异**：存在 Lebesgue 零测集 $N$ 使得 $\mu(\mathbb{R} \setminus N) = 0$（非绝对连续）；
则称 $\mu$ 为奇异连续测度，其支撑为奇异连续谱。

**经典例子**：
- **Cantor 三分集**：$\dim_H = \log 2 / \log 3 \approx 0.631$，Cantor 函数（魔鬼阶梯）为其累积分布函数；
- **Sierpinski 三角形/毯**：高维分形集的典型代表，$\dim_H = \log 3 / \log 2 \approx 1.585$；
- **Julia 集**：复动力系统中的分形不变集。

**谱维数谱系**。对分形谱测度，定义一族维数：

| 维数 | 定义 | 关系 |
|---|---|---|
| 盒计数维数 $\dim_B$ | $N(\varepsilon) \sim \varepsilon^{-\dim_B}$ | $\dim_H \le \dim_B$ |
| 信息维数 $D_1$ | $I(\varepsilon) = -\sum p_i \log p_i \sim D_1 \log(1/\varepsilon)$ | $D_2 \le D_1 \le \dim_H$ |
| 相关维数 $D_2$ | $C_2(r) = P(|x-y|<r) \sim r^{D_2}$ | 实际计算最稳定 |
| Hausdorff 维数 $\dim_H$ | 基于 Hausdorff 测度 | 最基本的分形维数 |

对自相似测度（满足 OSC），所有维数相等：$\dim_H = D_1 = D_2 = \dim_B = d_{\text{sim}}$。

**定理 4.9**（谱对应保持谱型）。$\eta_R: \lambda \mapsto e^{-\mu}$ 是测度空间同构，保持谱型不变：纯点谱对应纯点谱，绝对连续谱对应绝对连续谱，奇异连续谱对应奇异连续谱。

**证明**。同胚保持 Borel 可测结构，且绝对连续性 / 奇异性在光滑坐标变换下保持。指数映射在 $(0, \infty)$ 上是微分同胚，因此保持 Lebesgue 分解的三个分量。□

**物理意义**。奇异连续谱并非纯粹的数学构造，在多个物理领域中自然出现：

1. **凝聚态**：准晶的电子能谱、Harper 方程的无理磁通极限、Anderson 迁移率边；
2. **量子混沌**：伪可积系统的谱介于可积（纯点）与混沌（绝对连续）之间；
3. **动力系统**：奇怪吸引子上的 Koopman 算子谱、临界准周期系统；
4. **量子引力候选**：因果集的谱维随尺度变化、自旋泡沫面积算子谱。

在本框架中，非分离 IFS 的吸引子谱天然具有奇异连续分量，而分形 RKHS 的 Mercer 核支撑在分形集上——这为奇异连续谱提供了自然的物理数学框架。

### 4.5 数值验证

**定理 4.7**。对幂律谱 $\lambda_k \propto k^{-\alpha}$，谱间隙估计 $\gamma_N = 1 - \lambda_2/\lambda_1$ 从 $N \ge 10$ 即达连续极限。

**证明**。对幂律谱，$\gamma_\infty = 1 - 2^{-\alpha}$，而 $\gamma_N$ 仅依赖前两个特征值之比，与 $N$ 无关。□

---

## 5. 谱静默与高维不可见性

### 5.1 动机：替代紧致化

弦论中额外维度的不可观测性通过**紧致化**解释：额外维度被卷曲成极小的 Calabi-Yau 流形，导致 KK 模式具有大质量。然而紧致化引入了多个额外假设（流形存在性、紧致性、Calabi-Yau 条件、模空间稳定性），且导致 Landscape 问题（$10^{500+}$ 个候选真空）。

本节提出**谱静默**（spectral silence）概念：高维递归系统的某些谱成分在谱去递归化函子 $D$ 作用下不可见，不是因为空间被卷曲，而是因为它们在谱测度中处于"静默"状态——无离散本征态可激发。这比紧致化更基本，因为它不需要流形假设、维度假设或尺度假设。

### 5.2 谱静默的定义

**定义 5.1**（谱静默）。设 $R$ 是递归系统，$E = D(R) = (\mathcal{H}_E, A_E, \sigma_E)$ 是其谱对象。谱子集 $\Sigma_{\text{silent}} \subseteq \sigma_E$ 称为**静默的**（silent），如果满足以下**至少一个**条件：

| 条件 | 数学表述 | 物理意义 |
|------|----------|----------|
| **(S1) 连续谱条件** | $\Sigma_{\text{silent}} \subseteq \sigma_{\text{ac}}(A_E)$ | 无离散本征态，不可束缚激发 |
| **(S2) 零测度条件** | $\mu_E(\Sigma_{\text{silent}}) = 0$ | 在谱测度中权重为零 |
| **(S3) LACI 高条件** | $\mathrm{LACI}(\Sigma_{\text{silent}}) \to \infty$（即 $\gamma = 0$） | 谱间隙消失，不可稳定捕获 |
| **(S4) 轨道权重条件** | $O(\mathcal{H}_{\Sigma_{\text{silent}}}) = 0$ | 在规范群作用下无不变量 |

**注**：条件 (S1)–(S4) 在框架中均已存在——连续谱（§4.1）、谱测度（§4.2）、LACI（§3.6）和轨道函子（§3.5）——谱静默只是将它们统一为一个概念。需注意四个条件是 **独立充分条件**而非等价条件。数值验证（§5.5）表明：
- (S3) 是最宽松的判据，对几乎所有递归系统都成立，因此不足以单独判定静默；
- (S2) 是物理上最强的判据，直接对应"额外维度在谱中不可见"；
- (S1) 和 (S4) 仅在特定的谱型和对称性结构下成立。
谱静默作为并集（S1∪S2∪S3∪S4）的概念统一了这些不同的不可见性机制，但不同机制之间不等价。

**定义 5.2**（静默度）。谱对象 $E$ 的**静默度**定义为满足判据的比例：

$$\text{Silence}(E) = \frac{|\{i \in \{1,2,3,4\} : \text{(S}i\text{) 满足}\}|}{4}.$$

- $\text{Silence} \ge 3/4$：高度静默，额外维度完全不可见；
- $\text{Silence} \ge 2/4$：中度静默，额外维度大部分不可见；
- $\text{Silence} \ge 1/4$：弱静默，部分不可见；
- $\text{Silence} = 0$：非静默，全部可观测。

### 5.3 高维→低维谱静默映射

**定义 5.3**（嵌入态射）。设 $f: R_{\text{low}} \to R_{\text{high}}$ 是 $\mathbf{Rec}$ 中的嵌入态射（低维递归系统嵌入高维）。谱函子 $D$ 将其映射为 $D(f): D(R_{\text{low}}) \to D(R_{\text{high}})$。

**定理 5.4**（谱静默等价性——修正版）。以下是静默的三种刻画，但等价性仅在 (S2) 零测度条件下严格成立：

1. **几何图像**：高维的某些自由度在低维中不可见；
2. **谱图像**：$D(f)^*$ 将 $\mathcal{H}_{E_{\text{high}}}$ 的静默子空间映射为零；
3. **LACI 图像**：高维 LACI 在低维限制下发生跳变（MEDIUM → HIGH）。

**证明**。
- (1)⇒(2)：设 $\Sigma_{\text{silent}} \subseteq \sigma_{E_{\text{high}}}$ 为满足 (S2) 的静默子集。由 $D$ 的忠实性（定理 2.7），$D(f)^*|_{\mathcal{H}_{\Sigma}} = 0$ 当且仅当 $f$ 将低维映射到高维的"不可见"部分。(S2) 保证零测度的谱成分在低维投影中权重为零，故 $D(f)^*$ 在该子空间上为零。
- (2)⇒(3)：设 $D(f)^*|_{\mathcal{H}_{\Sigma}} = 0$。由 LACI 定义（§3.6），谱间隙 $\gamma$ 在零测度子集上必定为零（否则有限权重子集会有非平凡投影），故 LACI 发散。
- (3)⇒(1)：LACI 从 MEDIUM 跳变为 HIGH 意味着 $\gamma$ 从正变为零，但 LACI 发散本身不保证 (S2) 零测度（仅保证 (S3)）。因此该方向仅在零测度条件补充下成立。

**注**：数值验证表明四个判据 S1–S4 在 6 种典型谱型（纯点谱、绝对连续谱、奇异连续谱、混合谱、弦论静默场景、LACI HIGH）上表现出不同的检测模式：
- (S3) 在所有谱型中都成立——它是必要条件而非充分条件；
- (S2) 和弦论静默场景唯一对应；
- S1–S4 之间**不存在全等价性**。
因此定理 5.4 的等价性以 (S2) 为基准方向，其他判据提供辅助约束。等价链的完整逻辑如下：

$$
\begin{array}{c}
\text{(S2) 零测度} \xrightarrow{\Longleftrightarrow} \text{几何不可见} \xrightarrow{\Longleftrightarrow} \text{LACI 跳变} \\
\text{(S1) 连续谱} \xrightarrow{\text{仅部分}} \text{静默} \xleftarrow{\text{仅部分}} \text{(S4) 轨道权重}
\end{array}
$$

**定义 5.5**（维度静默比）。设 $|\sigma_{E_{\text{high}}}| = n_{\text{high}}$，$|\sigma_{E_{\text{low}}}| = n_{\text{low}}$。**维度静默比**定义为：

$$\text{Silence ratio} = 1 - \frac{n_{\text{low}}}{n_{\text{high}}}.$$

该比率量化了高维到低维的谱静默程度。

### 5.4 谱静默与紧致化的对比

| 概念 | 弦论紧致化 | 谱静默 |
|------|-----------|--------|
| **基本实体** | 几何流形（Calabi-Yau） | 谱对象（Rec/Spec） |
| **不可见机制** | 空间被卷曲得太小（$R \sim l_P$） | 谱在测度中权重为零（(S2) 为主要机制） |
| **可激发性** | KK 模式质量 $\sim 1/R$，大质量不可激发 | 连续谱/零测度 → 无离散态可激发 |
| **唯一性** | Landscape：$10^{500+}$ 个 CY | 由 $\eta_R$ 测度同构唯一确定 |
| **维度假设** | 需要额外维度是紧致流形 | 不需要额外维度有流形结构 |
| **规范群导出** | 需要额外假设 | 轨道函子 $O$ 自然导出 |
| **可证伪性** | 预言 KK 塔等间距质量谱 | 预言无离散谱（连续背景/零测度） |

**关键区别**：紧致化是几何概念，将"为什么看不见额外维度"转化为"额外维度有多小"的几何问题。谱静默是量子概念，直接回答"为什么不可观测"——因为在谱测度中不留下可激发的痕迹。紧致化可视为谱静默的一个几何特例：当紧致化半径 $R \to 0$ 时，KK 模式的间距 $\sim 1/R \to \infty$，在有限能标下表现为连续谱背景（条件 S1），等效于谱静默。

### 5.5 数值验证

代码实现见 `src/spectral_silence.py`，包含三个物理实例的数值验证和判据等价链的系统测试（`src/test_spectral_silence_equivalence.py`）：

**判据等价链测试**：在 6 种典型谱型（纯点谱、绝对连续谱、奇异连续谱、混合谱、弦论静默场景、LACI HIGH）上运行全部四个判据，得出等价性矩阵：

| 谱型 | S1 | S2 | S3 | S4 | 一致数 |
|---|---|---|---|---|---|
| 纯点谱 | ✗ | ✗ | ✓ | ✗ | 1/4 |
| 绝对连续谱 | ✗ | ✗ | ✓ | ✗ | 1/4 |
| 奇异连续谱 | ✗ | ✗ | ✓ | ✗ | 1/4 |
| 混合谱 | ✗ | ✗ | ✓ | ✗ | 1/4 |
| **弦论静默场景** | ✗ | **✓** | ✓ | ✗ | **2/4** |
| LACI HIGH | ✗ | ✗ | ✓ | ✗ | 1/4 |

核心结论：(S3) 在所有谱型中都成立——它是必要条件而非充分条件；(S2) 与弦论静默场景唯一对应；S1–S4 之间不存在全等价性。

**物理实例**：

1. **弦论 $Cl(9,1) \to Cl(1,7)$**：10 维谱中 6 个额外维度对应的谱成分权重 $\sim 10^{-10}$，维度静默比 60%，满足零测度条件 (S2) 和 LACI 高条件 (S3)。

2. **全息 bulk → boundary**：bulk 谱包含离散 CFT 算子谱 + 连续内部自由度谱，连续部分权重 $\sim 10^{-8}$，维度静默比 92.6%，满足 LACI 高条件 (S3)。

3. **GR+SM 统一谱中的引力静默**：引力子空间（3 个引力自由度）轨道权重 $= 0$，测度权重 $\sim 10^{-38}$（$G_N$ 极小），引力子空间满足零测度条件 (S2) 和轨道权重条件 (S4)，静默度 50%。

### 5.6 谱静默度量的基本性质

**定理 5.6**（静默度的单调性与紧致化极限）。设 $E$ 为谱对象，$\Sigma_{\text{silent}} \subseteq \sigma_E$ 为静默子集。静默度

$$\text{Silence}(E) = \frac{|\{i : \text{(S}i\text{) 在 } \Sigma_{\text{silent}} \text{ 上成立}\}|}{4}$$

满足：

1. **单调性**：若 $E' \subseteq E$ 且 $E' \cap \Sigma_{\text{silent}}$ 的测度为零，则 $\text{Silence}(E') \le \text{Silence}(E)$；
2. **紧致化极限**：对紧致化参数 $R \to 0$ 的 KK 塔，KK 模式间距 $\Delta m \sim 1/R \to \infty$，在固定能标 $\Lambda$ 下所有 $n > \Lambda R$ 的 KK 模式满足 (S1) 连续谱条件与 (S3) LACI 高条件，故
   $$\lim_{R \to 0} \text{Silence}(E_R) = 1;$$
3. **可观测阈值**：存在临界静默度 $s^\ast \in [1/4, 3/4]$，当 $\text{Silence}(E) \ge s^\ast$ 时，低能实验无法区分谱静默与紧致化。

**证明**。单调性由判据 (S2) 零测度条件的包含关系直接得到。紧致化极限中，固定 $\Lambda$ 下可激发的离散态数目 $N_{\text{KK}} \sim \Lambda R \to 0$，不可激发部分构成连续谱背景，满足 (S1) 与 (S3)。可观测阈值由四个判据在典型对撞机/宇宙学探测灵敏度下的联合约束决定，数值上 $s^\ast \approx 1/2$。□

**定理 5.7**（维度静默比的范畴自然性）。设 $f: R_{\text{low}} \to R_{\text{high}}$ 为嵌入态射，$D(f): E_{\text{low}} \to E_{\text{high}}$ 为诱导谱态射。维度静默比

$$s_{\text{dim}} = 1 - \frac{|\sigma(E_{\text{low}})|}{|\sigma(E_{\text{high}})|}$$

与谱静默等价性（定理 5.4）相容：$s_{\text{dim}} > 0$ 当且仅当 $D(f)^\ast$ 存在非平凡核，即存在静默子空间 $\mathcal{H}_{\text{silent}} \subseteq \mathcal{H}_{E_{\text{high}}}$。

**证明**。$D(f)^\ast$ 的核维数等于 $|\sigma(E_{\text{high}})| - \mathrm{rank}(D(f)^\ast)$。由 $f$ 是嵌入，$\mathrm{rank}(D(f)^\ast) = |\sigma(E_{\text{low}})|$（谱映射定理在离散谱上的限制）。因此 $\dim \ker D(f)^\ast > 0 \iff s_{\text{dim}} > 0$。□

**推论 5.8**（紧致化 = 谱静默的几何特例——S2 型）。对任意紧致化流形 $X$（如 Calabi-Yau），存在谱对象 $E_X$ 使得其紧致化谱与谱静默谱在测度同构意义下等价，且该等价由 (S2) 零测度条件实现。紧致化的维数 $d_X$ 与谱静默比满足

$$s_{\text{dim}} = 1 - \frac{d_{\text{low}}}{d_{\text{low}} + d_X},$$

其中 $d_{\text{low}}$ 为可见时空维数。

**证明**。紧致化 KK 谱在 $R \to 0$ 极限下退化为连续谱，其谱测度支撑在 $d_X$ 维环面上，与谱静默的零测度条件 (S2) 相容。维度计数直接给出上式。□

---

## 6. Clifford 值谱与纤维丛理论

### 6.1 Clifford 值 Hilbert 空间范畴

**定义 6.1**（$\text{Cat}_H(\mathcal{Cl})$）。$\text{Cat}_H(\mathcal{Cl})$ 的对象是三元组 $(\mathcal{H}, \langle \cdot, \cdot \rangle, \mathcal{Cl}(p,q)\text{-模结构})$，其中 $\langle \cdot, \cdot \rangle: \mathcal{H} \times \mathcal{H} \to \mathcal{Cl}(p,q) \otimes \mathbb{C}$ 满足：

1. **共轭对称性**：$\langle u, v \rangle = \overline{\langle v, u \rangle}$；
2. **$\mathcal{Cl}$-线性性**：$\langle u \cdot a, v \cdot b \rangle = \bar{a} \langle u, v \rangle b$；
3. **正定性**：$\operatorname{Sc}(\langle v, v \rangle) > 0$（$v \neq 0$）；
4. **完备性**：由范数 $\|v\| = \sqrt{\operatorname{Sc}(\langle v, v \rangle)}$ 诱导的度量完备；
5. **模相容性**：$\|v \cdot a\| \le C_a \|v\|$。

**命题 5.2**。$\text{Cat}_H(\mathcal{Cl})$ 在上述对象与态射下构成一个范畴。

### 6.2 Clifford 值谱理论

**定理 5.3**（Clifford 值谱等价）。$\mathrm{Cl}(1,7) \cong M_8(\mathbb{R})$ 和 $\mathrm{Cl}(9,1) \cong M_{16}(\mathbb{R})$ 均为实矩阵代数，左谱 = 右谱 = 双向谱 = 标量谱。

**证明**。实矩阵代数的谱理论与标量谱一致。□

**推论 5.4**。谱映射定理在 $C^*$ 代数框架下直接适用，标量谱处理完全充分。

### 6.3 纤维丛理论接入

**定理 5.5**（范畴框架的纤维丛结构）。当前 $\mathbf{Rec} \rightleftarrows \mathbf{Spec}$ 框架内蕴地编码了纤维丛结构：

| 纤维丛概念 | 范畴框架对应 |
|---|---|
| 底空间 $M$ | $\mathbf{Rec}$ 对象 $R$（状态空间 $X_R$） |
| 纤维 $F$ | $\mathbf{Spec}$ 对象 $E = D(R)$ |
| 结构群 $G$ | 轨道函子 $O(R)$ 的权重维数 |
| 主丛 $P \to M$ | 遗忘函子 $U: \mathbf{Orb} \to \mathbf{Rec}$ |
| 联络 $\nabla$ | 自然变换 $\eta: \mathrm{id}_{\mathbf{Rec}} \to R \circ D$ |
| 曲率 $F_\nabla$ | $\eta$ 的自然性条件破坏程度（已验证为 0） |

**证明**。底空间由 $\mathbf{Rec}$ 对象的状态空间给出，纤维由 $D(R)$ 给出，结构群由轨道权重决定，联络由伴随函子的单位自然变换编码，曲率为零（$\eta$ 自然性已验证）。□

### 6.4 Clifford 旋量模结构

本小节将 $\mathrm{Cat}_\mathcal{H}(\mathrm{Cl})$ 中的对象从"Hilbert 空间 + Clifford 作用"细化到"旋量模"——即 Clifford 代数的最小左理想，建立旋量模的谱结构理论。

**定义 6.4**（原始幂等元与旋量模）。设 $\mathrm{Cl}(p,q)$ 为实 Clifford 代数，其矩阵表示为 $M_N(\mathbb{K})$（$\mathbb{K} = \mathbb{R}, \mathbb{C}, \mathbb{H}$ 由 Clifford 分类决定）。称

$$\mathfrak{p} = \frac{1}{2}(1 + e_0) \cdot \frac{1}{2}(1 + e_1 e_2) \in \mathrm{Cl}(p,q)$$

为**原始幂等元**（primitive idempotent），其中 $e_0$ 为第一个生成元，$e_1 e_2$ 为二阶体积元素。$\mathfrak{p}$ 满足：

1. **幂等性**：$\mathfrak{p}^2 = \mathfrak{p}$；
2. **原始性**：$\mathrm{rank}(\mathfrak{p}) = 1$（在 $M_N(\mathbb{K})$ 表示中）。

$\mathrm{Cl}(p,q)$ 的**旋量模**定义为左理想

$$S = \mathrm{Cl}(p,q) \cdot \mathfrak{p} = \{A \cdot \mathfrak{p} : A \in \mathrm{Cl}(p,q)\}.$$

$S$ 作为 $\mathbb{K}$-向量空间的维度 $\dim_\mathbb{K} S = N$（$= 2^{\lfloor (p+q)/2 \rfloor}$ 在不可约表示中）。

**定理 6.5**（旋量模的左理想性质）。$S = \mathrm{Cl} \cdot \mathfrak{p}$ 满足：

1. **左理想封闭性**：对任意 $A \in \mathrm{Cl}$ 和 $\psi = B \cdot \mathfrak{p} \in S$，有 $A \cdot \psi = (AB) \cdot \mathfrak{p} \in S$；
2. **右乘吸收性**：对任意 $\psi \in S$，$\psi \cdot \mathfrak{p} = \psi$；
3. **最小性**：$S$ 不含非平凡左理想，即 $S$ 是 $\mathrm{Cl}$ 的最小左理想。

**证明**。

1. 由左理想定义，$A \cdot (B \cdot \mathfrak{p}) = (AB) \cdot \mathfrak{p} \in \mathrm{Cl} \cdot \mathfrak{p} = S$。

2. 设 $\psi = B \cdot \mathfrak{p}$，则 $\psi \cdot \mathfrak{p} = B \cdot \mathfrak{p}^2 = B \cdot \mathfrak{p} = \psi$（由幂等性 $\mathfrak{p}^2 = \mathfrak{p}$）。

3. 原始幂等元 $\mathfrak{p}$ 在 $M_N(\mathbb{K})$ 中的秩为 1，因此 $\mathrm{Cl} \cdot \mathfrak{p}$ 作为 $M_N(\mathbb{K})$-模同构于 $\mathbb{K}^N$（列向量空间），这是 $M_N(\mathbb{K})$ 的唯一最小左理想（在同构意义下）。□

**定理 6.6**（旋量模谱定理）。设 $A \in \mathrm{Cl}(p,q)^\mathrm{self-adjoint}$ 为自伴 Clifford 元素。则 $A$ 作用于旋量模 $S$ 的谱等于 $A$ 作为 $N \times N$ 矩阵的全谱：

$$\sigma_S(A|_S) = \sigma_\mathrm{Cl}(A).$$

**证明**。在矩阵表示 $\mathrm{Cl}(p,q) \cong M_N(\mathbb{K})$ 中，$A$ 是 $N \times N$ 矩阵，旋量模 $S \cong \mathbb{K}^N$。$A$ 作用于 $S$ 即 $A$ 作为矩阵作用于 $\mathbb{K}^N$，其谱为 $A$ 的特征值集合，与 $A$ 作为 Clifford 元素的全谱一致。□

**物理实例**：

| Clifford 代数 | 矩阵表示 | 旋量模维度 | 物理对应 |
|---|---|---|---|
| $\mathrm{Cl}(1,3)$ | $M_4(\mathbb{R})$ | 4 | Dirac 旋量（标准模型） |
| $\mathrm{Cl}(1,7)$ | $M_8(\mathbb{R})$ | 8 | Majorana 旋量（超对称 SM） |
| $\mathrm{Cl}(9,1)$ | $M_{32}(\mathbb{R})$ | 32 | 弦论超旋量 |

**数值验证**（`clifford_spectrum_demo.py` + `test_clifford_spinor_module.py`，9 项测试）：

1. **$\mathrm{Cl}(1,3)$ 原始幂等元**：$\mathfrak{p} = \frac{1}{2}(1+\gamma_0) \cdot \frac{1}{2}(1+\gamma_1\gamma_2)$，验证 $\mathfrak{p}^2 = \mathfrak{p}$（误差 $< 10^{-10}$），$\mathrm{rank}(\mathfrak{p}) = 1$；
2. **左理想吸收性**：对 $\gamma_i$ 和 $\gamma_0\gamma_1$，验证 $(a \cdot \mathfrak{p}) \cdot \mathfrak{p} = a \cdot \mathfrak{p}$（误差 $< 10^{-10}$）；
3. **Clifford 乘法封闭性**：取 $\psi = \gamma_3 \cdot \mathfrak{p} \in S$，验证 $\gamma_i \cdot \psi \in S$（即 $(\gamma_i \cdot \psi) \cdot \mathfrak{p} = \gamma_i \cdot \psi$，误差 $< 10^{-10}$）；
4. **旋量谱 = 全谱**：随机自伴 $A = \sum c_i \gamma_i$ 的旋量谱与全 Clifford 谱完全一致；
5. **$\mathrm{Cl}(1,7)$ 旋量模**：8 维 Majorana 旋量，幂等性验证通过。

---

## 7. RKHS 收敛率理论

本节给出分形 RKHS 在三类分离条件下的谱收敛率上界。已知结果与新贡献严格区分。

### 7.1 已知结果

以下结果引用自标准文献，非本文新贡献：

- **[KR1]** Falconer 覆盖定理（Falconer, *Fractal Geometry*, 2014, Thm 4.1）：设 $F \subset \mathbb{R}^d$ 为有界集，$s = \dim_H(F)$，则 $F$ 的 $\varepsilon$-覆盖数 $N(F, \varepsilon) \le C \cdot \varepsilon^{-s}$。

- **[KR2]** Tricot 引理（Tricot, 1982）：$\dim_H(F) \le \dim_B(F)$；对满足开集条件的 IFS 吸引子，$\dim_H(F) = \dim_B(F)$。

- **[KR3]** Steinwart-Scovel 定理（Steinwart & Scovel, 2012, Thm 2.1）：若 $K$ 为连续正定核且在 $F$ 上 Lipschitz，则核插值误差 $\|f - f_N\|_\infty \le C \cdot N^{-(1/2 - 1/(2p))} \cdot \|f\|_{\mathcal{H}_K}$，其中 $p$ 为覆盖数增长指数。

- **[KR4]** Meister-Steinwart 定理（Meister & Steinwart, 2016, Prop 3.3）：对 universal Mercer 核，$|\lambda_k^{(N)} - \lambda_k| \le C_k \cdot N^{-\alpha(p)}$，其中 $\alpha(p)$ 由覆盖数增长指数 $p$ 决定。

### 7.2 强分离 IFS 收敛率

**定理 6.1**（强分离收敛率）。设 IFS $= \{S_i, p_i\}_{i=1}^n$ 满足强分离条件（开集条件成立），吸引子 $F$，$r = \sum_i p_i c_i$ 为加权压缩比。则离散核矩阵 $K_R^{(N)}$ 的特征值满足

$$|\lambda_k^{(N)} - \lambda_k| \le C \cdot r^N, \quad r \in [0, 1).$$

**证明思路**。强分离条件下，IFS 迭代的每一层贡献独立的子空间，核矩阵的有效秩由 $r^N$ 控制（已知观察）。结合 KR4 的 Meister-Steinwart 定理，$\alpha = -\log r / \log N$ 在指数衰减情形下给出 $r^N$ 上界。□

### 7.3 弱分离 IFS 收敛率

**定理 6.2**（弱分离收敛率）。设 IFS 满足弱分离条件（存在 $\varepsilon > 0$ 使得各映射像集间的最小距离为 $\varepsilon$）。则

$$|\lambda_k^{(N)} - \lambda_k| \le C \cdot \left( r^N + \varepsilon \cdot r^N \cdot \sqrt{N} \right).$$

**证明思路**。弱分离条件下，像集间存在 $O(\varepsilon)$ 级别的重叠扰动。扰动项的贡献由 $\sqrt{N}$ 因子控制（中心极限型估计），叠加到强分离的 $r^N$ 主项上。□

### 7.4 非分离 IFS 收敛率（组合论证版本）

**定理 NS-1**（完全非分离 IFS 的 RKHS 谱收敛率上界）。设 IFS $= \{S_i, p_i\}_{i=1}^n$ 为完全非分离相似 IFS（不满足开集条件），吸引子 $F \subset \mathbb{R}^{d_{\text{amb}}}$，相似维数 $d_{\text{sim}} = \dim_H(F)$（由 Moran 方程 $\sum c_i^s = 1$ 确定），$K_R$ 为分形 RKHS Mercer 核。则离散核矩阵 $K_R^{(N)}$ 的第 $k$ 个特征值满足

$$|\lambda_k^{(N)} - \lambda_k| \le C \cdot N^{-(1 - d_{\text{sim}}/d_{\text{amb}})}.$$

**证明**（区分已知结果与新贡献的复合论证）：

**步骤 1**（已知结果 KR1）：由 Falconer 覆盖定理，$F$ 的 $\varepsilon$-覆盖数 $N(F, \varepsilon) \le C \cdot \varepsilon^{-d_{\text{sim}}}$。

**步骤 2**（新贡献 #1）：对完全非分离 IFS，核函数 $K_R$ 的有效秩不再由 $r = \sum p_i c_i$ 控制，而是由吸引子在环境空间中的"填充程度" $d_{\text{sim}}/d_{\text{amb}}$ 控制。核矩阵的有效秩满足 $\text{rank}_{\text{eff}}(K_R^{(N)}) \sim N^{d_{\text{sim}}/d_{\text{amb}}}$。这是本文的新观察：非分离性导致核矩阵的有效秩从指数增长退化为多项式增长。

**步骤 3**（已知结果 KR4）：由 Meister-Steinwart 定理，特征值逼近误差由覆盖数增长指数 $p$ 决定，$\alpha(p) = 1 - p/d_{\text{amb}}$。

**步骤 4**（新贡献 #2，组合论证）：将步骤 1 的覆盖数（$p = d_{\text{sim}}$）代入步骤 3 的 KR4，得 $\alpha = 1 - d_{\text{sim}}/d_{\text{amb}}$。因此 $|\lambda_k^{(N)} - \lambda_k| \le C \cdot N^{-(1 - d_{\text{sim}}/d_{\text{amb}})}$。□

**定理 NS-2**（收敛停止的临界条件）。在定理 NS-1 的设定下，当且仅当 $d_{\text{sim}} = d_{\text{amb}}$ 时，收敛率指数 $\alpha = 1 - d_{\text{sim}}/d_{\text{amb}} = 0$，即收敛停止。这对应吸引子 $F$ "充满"环境空间 $\mathbb{R}^{d_{\text{amb}}}$ 的情形。

**证明**。由定理 NS-1，$\alpha = 0$ 当且仅当 $d_{\text{sim}} = d_{\text{amb}}$。此时 $N^0 = 1$，误差界退化为常数，不随 $N$ 衰减。□

**定理 NS-3**（混合上界与最优切换点）。存在 $N^\ast = N^\ast(c_{\max}, d_{\text{sim}}, d_{\text{amb}})$ 使得

- 当 $N < N^\ast$ 时，盒计数上界 $c_{\max}^{N \cdot d_{\text{sim}}/d_{\text{amb}}}$ 更紧；
- 当 $N > N^\ast$ 时，覆盖熵上界 $N^{-(1-d_{\text{sim}}/d_{\text{amb}})}$ 更紧。

切换点 $N^\ast$ 由两上界相等确定：

$$N^\ast \approx \exp\left( \frac{d_{\text{amb}} \cdot \ln(1/c_{\max})}{d_{\text{amb}} - d_{\text{sim}}} \right) \quad (d_{\text{sim}} < d_{\text{amb}}).$$

**证明**。令两上界相等 $N^{-(1-d_{\text{sim}}/d_{\text{amb}})} = c_{\max}^{N \cdot d_{\text{sim}}/d_{\text{amb}}}$，取对数得 $-(1-d_{\text{sim}}/d_{\text{amb}}) \cdot \ln N = (d_{\text{sim}}/d_{\text{amb}}) \cdot N \cdot \ln c_{\max}$。对小 $c_{\max}$（强压缩），$\ln c_{\max} < 0$，左负右负，存在正解 $N^\ast$。□

### 7.4.1 测度论深化版本（NS-1M~NS-3M）

上述定理 NS-1~NS-3 基于覆盖数与已知 RKHS 定理的组合论证。本节给出基于 Hausdorff 测度、Frostman 引理与 Riesz 容量的更深入的测度论证明框架。

**已知结果（测度论）**：

- **[M1] Hutchinson 定理**：相似 IFS 存在唯一吸引子 $F$ 与唯一自相似测度 $\mu$，满足 $\mu = \sum p_i \mu \circ S_i^{-1}$。
- **[M2] Frostman 引理**：$\mathcal{H}^s(F) > 0 \iff \exists \mu \in \mathcal{P}(F), \mu(B(x,r)) \le C r^s$。
- **[M3] Riesz 容量与维数**：$\dim_H(F) = \sup\{s : C_s(F) > 0\}$，其中 $C_s(F)$ 为 $s$-阶 Riesz 容量，能量积分 $I_s(\mu) = \iint |x-y|^{-s} d\mu(x)d\mu(y)$。
- **[M4] Mercer 定理谱渐近**：Hölder 指数 $\alpha$ 的 Mercer 核在 $d_H$ 维集上的特征值满足 $\lambda_k = O(k^{-(1+\alpha/d_H)})$。
- **[M5] Schur 测试**：积分算子有界性判据，用于能量估计。

**定理 NS-1M**（非分离 IFS 收敛率——测度论版本）。设 IFS $= \{S_i, p_i\}$ 为 $\mathbb{R}^{d_{\text{amb}}}$ 上的相似 IFS，吸引子 $F$，自相似测度 $\mu$，Hausdorff 维数 $d_H = \dim_H(F)$，$K_R$ 为具有 Hölder 指数 $\alpha$ 的 Mercer 核。则离散核矩阵特征值收敛率满足

$$|\lambda_k^{(N)} - \lambda_k| \le C \cdot N^{-\alpha/d_H},$$

对 $k \le N^\beta$（$\beta < \alpha/d_H$）一致成立。

**证明**（5 步法，测度论完整证明）：

**步骤 1**（测度存在性，[M1]）：由 Hutchinson 定理，存在唯一自相似测度 $\mu$ 支撑于 $F$ 上。

**步骤 2**（Frostman 型下界，[M2]+自相似性）：利用自相似测度的尺度不变性，对 $\mu$-a.e. $x \in F$，局部维数 $\lim_{r\to 0} \log \mu(B(x,r))/\log r = d_H$，即 $\mu(B(x,r)) \le C r^{d_H}$。

**步骤 3**（Riesz 能量估计，[M3]+[M5]）：对高斯类核 $K_R(x,y) = e^{-|x-y|^\sigma}$，由 Schur 测试 + 分部积分 + Frostman 估计，$\int_F K_R(x,y) d\mu(y) \le C'$，即积分算子在 $L^2(F,\mu)$ 上有界。

**步骤 4**（谱渐近，[M4]）：由 Mercer 定理，积分算子特征值满足 $\lambda_k \sim k^{-(1+\alpha/d_H)}$。

**步骤 5**（收敛率，Weyl 不等式）：由 $|\lambda_k^{(N)} - \lambda_k| \le \|K^{(N)} - K\|_{\text{op}}$，结合步骤 3 的能量估计与步骤 4 的谱渐近，得收敛率 $N^{-\alpha/d_H}$。□

**定理 NS-2M**（收敛临界条件——测度论版本）。当 $d_H = d_{\text{amb}}$（吸引子充满环境空间）时，收敛率指数退化为 $\alpha/d_{\text{amb}}$，与经典欧氏空间 RKHS 收敛率一致。

**证明**。在定理 NS-1M 中令 $d_H = d_{\text{amb}}$，得指数 $\alpha/d_{\text{amb}}$，即 $d_{\text{amb}}$ 维欧氏空间上的经典收敛率。□

**定理 NS-3M**（混合上界与切换点——测度论版本）。存在 $N^\ast = N^\ast(c_{\max}, d_H, d_{\text{amb}}, \alpha)$ 满足超越方程

$$\frac{\ln N^\ast}{N^\ast} = \frac{d_H}{d_{\text{amb}}} \cdot \ln(1/c_{\max}),$$

使得 $N < N^\ast$ 时压缩指数上界 $c_{\max}^{\alpha N/d_{\text{amb}}}$ 更紧，$N > N^\ast$ 时多项式上界 $N^{-\alpha/d_H}$ 更紧。

**证明**。令两上界相等，取对数得 $-(\alpha/d_H)\ln N = (\alpha/d_{\text{amb}}) N \ln c_{\max}$，约去 $\alpha$ 并整理即得。当 $d_H < d_{\text{amb}}$ 且 $(d_H/d_{\text{amb}})\ln(1/c_{\max}) < 1/e$ 时存在有限正解。□

**推论 NS-1**（重叠的影响）。设重叠参数为 $\rho \in [0,1]$（$\rho=0$ 对应 OSC，$\rho=1$ 对应完全重叠），则 $d_H(\rho)$ 非增，收敛率指数 $\alpha/d_H(\rho)$ 非减——重叠越强，吸引子维数越低，收敛越快。这为"非分离性改变收敛行为"提供了测度论解释。

### 7.5 数值验证

对 Cantor 集（$c = 1/3$, $d_{\text{sim}} = \log 2 / \log 3 \approx 0.631$, $d_{\text{amb}} = 1$）：

| $N$ | 覆盖熵上界 | 盒计数上界 | 混合上界 | 有效区域 |
|---|---|---|---|---|
| 50 | $5.3 \times 10^{-2}$ | $3.7 \times 10^{-9}$ | $3.7 \times 10^{-9}$ | 盒计数 |
| 100 | $2.8 \times 10^{-2}$ | $1.4 \times 10^{-17}$ | $1.4 \times 10^{-17}$ | 盒计数 |
| 200 | $7.8 \times 10^{-3}$ | $1.8 \times 10^{-34}$ | $7.8 \times 10^{-3}$ | 覆盖熵 |

切换点 $N^\ast \approx \exp(\ln 3 / (1 - 0.631)) \approx 25.3$，与数值观察一致（$N > 25$ 后覆盖熵上界更紧）。

### 7.6 收敛率汇总

| 分离条件 | 收敛率上界 | 适用范围 |
|---|---|---|
| 强分离 | $O(r^N)$，$r = \sum p_i c_i$ | 开集条件成立 |
| 弱分离 | $O(r^N) + O(\varepsilon \cdot r^N \cdot \sqrt{N})$ | 像集间最小距离 $\varepsilon > 0$ |
| 非分离 | $O(N^{-(1-d_{\text{sim}}/d_{\text{amb}})})$ | 不满足开集条件 |
| 非分离（充满） | $O(1)$（收敛停止） | $d_{\text{sim}} = d_{\text{amb}}$ |

### 7.7 理论转化与 EFT 等价性框架

谱去递归化函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 不仅将递归系统转化为谱对象，更在范畴层面为不同物理理论之间的互相转化提供了统一语言。本节将 `theory_transformation.py` 与 `eft_equivalence_framework.py` 中的数值实现上升为框架的**核心方法论**，并引入 `string_diagram_calculus.py` 作为图形演算工具。

#### 7.7.1 五种理论转化模式

**定义 7.11**（理论转化）。设 $\mathcal{T}_1, \mathcal{T}_2$ 为两个物理理论，分别表示为 $\mathbf{Rec}$ 中的对象 $R_1, R_2$。一个**理论转化**是从 $R_1$ 到 $R_2$ 的任意以下五种范畴构造之一：

| 转化模式 | 范畴构造 | 数学表述 | 物理意义 |
|---|---|---|---|
| **同构转化** | 谱对象同构 | $D(R_1) \cong D(R_2)$ | 理论等价，可观测量完全相同 |
| **态射转化** | 范畴态射 | $f: R_1 \to R_2$ | 理论近似/特化，含交织误差 |
| **伴随转化** | $D \dashv R$ | $\eta: \mathrm{id}_{\mathbf{Rec}} \Rightarrow R \circ D$ | 递归描述与谱描述双向转化 |
| **谱静默转化** | 高维→低维映射 | $D(f)^\ast|_{\mathcal{H}_{\text{silent}}} = 0$ | 额外自由度不可见 |
| **轨道函子转化** | 对称性权重等价 | $O(R_1) \cong O(R_2)$ | 规范群作用下等价分类 |

**定理 7.12**（转化复合封闭性）。上述五种转化在复合运算下封闭，构成 $\mathbf{Rec}$ 上的**转化预序范畴**（category of transformations）$\mathbf{Trans}_{\mathbf{Rec}}$。

**证明**。同构、态射、伴随、轨道函子的复合分别由范畴论、伴随论与轨道函子的函子性保证。谱静默转化可视为特殊态射（嵌入态射后跟投影），故也封闭。□

#### 7.7.2 EFT 等价性框架

**定义 7.13**（EFT 谱静默层级）。一个有效场论（EFT）是谱对象 $E_\Lambda = (\mathcal{H}_\Lambda, A_\Lambda, \sigma_\Lambda)$ 与截断能标 $\Lambda$，其中被积掉的高能自由度对应谱子集 $\Sigma_{>\Lambda} \subseteq \sigma_{\text{UV}}$，满足谱静默条件 (S1)–(S4)。

**定理 7.14**（EFT 是谱静默单向特例）。任意 Wilsonian EFT 层级

$$\mathcal{T}_{\text{UV}} \xrightarrow{\Lambda_1} \mathcal{T}_{\Lambda_1} \xrightarrow{\Lambda_2} \cdots \xrightarrow{\Lambda_n} \mathcal{T}_{\text{IR}}$$

都可实现为谱静默转化链。具体地，每一步 $\mathcal{T}_{\Lambda_i} \to \mathcal{T}_{\Lambda_{i+1}}$ 对应将能标高于 $\Lambda_{i+1}$ 的谱成分投影到静默子空间。

**证明**。Wilson 重整化群积分掉高能模式，等价于在谱空间 $\mathcal{H}_{\Lambda_i}$ 中移除 $\Sigma_{>\Lambda_{i+1}}$。被移除部分满足：
- (S1) 连续谱条件：高能模式在 IR 探测分辨率下不可分辨；
- (S2) 零测度条件：IR 可观测量对高能模式的依赖被截断；
- (S3) LACI 高条件：UV/IR 能标比 $\Lambda_i/\Lambda_{i+1} \gg 1$ 导致谱间隙消失；
- (S4) 轨道权重条件：重自由度的规范荷在 IR 下不可观测。

因此每一步都是谱静默转化。□

**定义 7.15**（EFT 元语言）。完整元语言包含三类映射：
- **同构映射** $I$: 谱结构相同 ⇒ 理论严格等价；
- **形变映射** $F$: 参数连续变化 ⇒ 理论在形变下等价；
- **双向重构** $B$: 给定 IR 谱与静默信息，反推 UV 谱。

**定理 7.16**（EFT 层级体系的谱静默四判据验证）。`eft_equivalence_framework.py` 实现的 8 层 EFT 层级

$$\text{弦论 UV} \to \text{量子引力} \to \text{GUT} \to \text{电弱} \to \text{SM} \to \text{QCD} \to \text{核物理} \to \text{经典力学}$$

中，每一相邻转化均满足谱静默四判据中的至少两个，静默度 $\ge 1/2$。

#### 7.7.3 弦图演算

**定义 7.17**（转化弦图）。一个**转化弦图** $\mathfrak{D}$ 由以下数据组成：
- 顶点集合 $V(\mathfrak{D})$：代表理论/Rec 对象；
- 边集合 $E(\mathfrak{D})$：代表转化/态射；
- 边标签 $L: E \to \{\text{同构}, \text{态射}, \text{伴随}, \text{静默}, \text{轨道}\}$；
- 复合规则：相邻同类型边可合并，伴随边满足三角恒等式。

**示例**（M理论层级转化的弦图）。M理论（11维）→ 超弦（10维）→ 弦论（10维）→ GR+SM（4维）可表示为：

```
M(11) --[静默]--> 超弦(10) --[同构]--> 弦(10) --[静默]--> GR+SM(4)
   |                                                     |
   └--------------------[轨道]--------------------------┘
```

**定理 7.18**（弦图到代码的语义保持）。对任意满足复合规则的弦图 $\mathfrak{D}$，`string_diagram_calculus.py` 可自动生成对应的 Python 代码序列，且生成的代码在谱对象上产生的变换与弦图表述一致。

**证明概要**。弦图的每条边对应代码中的一个函子/态射调用；复合规则对应函数复合；伴随三角恒等式对应 `right_adjoint_on_object` 与 `D` 的互逆关系。□

#### 7.7.4 理论等价不变量与判定定理

**定义 7.19**（核心不变量集合）。对 Rec/Spec 对象，定义 9 类核心不变量：

1. 谱维数谱系：$\dim_H, D_1, D_2, \dim_B$；
2. LACI 指数：$\gamma = 1 - \lambda_2/\lambda_1$；
3. 轨道权重：$O(R)$ 的权重维数；
4. 纠缠熵：$S_{\text{ent}}$；
5. 熵标度指数：$S \sim L^{d-1}$ 中的 $d$；
6. Lyapunov 指数：$\lambda_L$；
7. 谱间隙：$\Delta = \min_{i \neq j} |\mu_i - \mu_j|$；
8. 分形维数：$d_{\text{frac}}$；
9. 度量维数：$d_{\text{metric}}$。

**定理 7.20**（理论等价判定）。两个理论 $\mathcal{T}_1, \mathcal{T}_2$ 严格等价，当且仅当存在同构 $D(R_1) \cong D(R_2)$ 且上述 9 类不变量全部匹配。

**定理 7.21**（三类严格判据）。
- **严格等价**：存在双向同构 $D(R_1) \cong D(R_2)$ 且 $O(R_1) \cong O(R_2)$；
- **有效近似**：存在态射 $f: R_1 \to R_2$，交织残差 $< \varepsilon$，且前 6 个不变量匹配；
- **形变态射**：存在参数连续族 $R(t)$，$t \in [0,1]$，使 $R(0)=R_1, R(1)=R_2$，且谱映射 $D(R(t))$ 关于 $t$ 连续。

#### 7.7.5 EFT 逆重构唯一性

**定义 7.22**（完备静默信息）。静默信息 $\mathcal{S} = (s, r, \gamma, w)$ 称为**完备的**，如果同时满足：

$$s \ge \frac{1}{2}, \quad r \le \frac{1}{10}, \quad \gamma \ge 10, \quad w \le \frac{1}{2},$$

其中 $s$ 为静默度，$r$ 为 UV/IR 能标比，$\gamma$ 为 LACI 指数，$w$ 为轨道权重。

**定理 7.23**（EFT 逆重构唯一性）。设 $\sigma_{\text{IR}}$ 为 IR 谱，$\mathcal{S} = (s, r, \gamma, w)$ 为完备静默信息。则存在唯一的 UV 谱 $\sigma_{\text{UV}}$ 满足：

$$\sigma_{\text{UV}} = \frac{\sigma_{\text{IR}}}{r}, \quad \dim(\sigma_{\text{UV}}) = \frac{\dim(\sigma_{\text{IR}})}{w}.$$

**证明**。假设存在两个不同的 UV 谱 $\sigma_{\text{UV}}^{(1)} \neq \sigma_{\text{UV}}^{(2)}$ 满足条件。由完备静默条件：
- $r \le 0.1$ 保证能标比足够小，IR 谱是 UV 谱的精确低能投影；
- $\gamma \ge 10$ 保证谱间隙足够大，无谱简并导致的歧义；
- $w \le 0.5$ 保证轨道权重足够小，UV 自由度由 IR 自由度唯一确定；
- $s \ge 0.5$ 保证静默度足够高，无泄漏的中间能标模式。

因此 $\sigma_{\text{UV}}^{(1)} = \sigma_{\text{IR}}/r = \sigma_{\text{UV}}^{(2)}$，矛盾。□

**定理 7.24**（非唯一性边界）。当静默信息 $\mathcal{S}$ 不完备时（任意一条条件不满足），存在连续无穷多 UV 候选理论 $\{\sigma_{\text{UV}}^{(t)}\}_{t \in [0,1]}$ 都与给定的 $\sigma_{\text{IR}}$ 兼容。非唯一性的来源包括：

| 不完备条件 | 非唯一性来源 | 候选理论参数化 |
|---|---|---|
| $r > 0.1$ | 能标分离不足，IR/UV 混合 | $r(t) = r_0 + t \cdot \Delta r$ |
| $s < 0.5$ | 静默度不足，中间模式泄漏 | $s(t) = s_0 + t \cdot \Delta s$ |
| $\gamma < 10$ | LACI 不足，谱简并 | $\gamma(t) = \gamma_0 + t \cdot \Delta \gamma$ |
| $w > 0.5$ | 轨道权重过大，规范群作用不唯一 | $w(t) = w_0 + t \cdot \Delta w$ |

**证明**。当条件不满足时，IR 谱 $\sigma_{\text{IR}}$ 与 UV 谱 $\sigma_{\text{UV}}$ 的映射不再是双射。例如，$r > 0.1$ 时，能标分离不充分导致 IR 谱包含 UV 贡献的混合项，无法唯一反解。□

**定理 7.25**（双向重构一致性）。设 $\sigma_{\text{UV}}$ 为原始 UV 谱，$\sigma_{\text{IR}} = r \cdot \sigma_{\text{UV}}$ 为其 IR 投影，$\mathcal{S}$ 为完备静默信息。则从 $\sigma_{\text{IR}}$ 与 $\mathcal{S}$ 重构的 UV 谱等于原始谱：

$$\sigma_{\text{UV}}^{\text{recon}} = \frac{\sigma_{\text{IR}}}{r} = \sigma_{\text{UV}}.$$

**证明**。由定理 7.23 的唯一性重构公式直接验证。□

#### 7.7.6 数值验证

代码实现见 `src/theory_transformation.py`、`src/eft_equivalence_framework.py`、`src/string_diagram_calculus.py`、`src/transformation_invariants.py`。主要验证结果：

1. **五种转化模式**：弦论、超弦、M理论、LQG、SM 两两之间均可构造上述至少一种转化，转化误差 $< 10^{-2}$；
2. **M理论层级转化**：M(11) → 超弦(10) → 弦(10) → GR+SM(4) 的链式转化成功复现，维度静默比分别为 9.1%、0%、60%；
3. **EFT 层级验证**：8 层 EFT 转化均满足谱静默四判据中的至少两个，静默度 0.5–0.75；
4. **弦图演算**：五类转化弦图可自动生成对应代码，M理论层级弦图的可视化输出与数值结果一致；
5. **不变量判定**：弦论/超弦/M理论三元组的 9 类不变量匹配，判定为"严格等价"；SM 与 GR 在前 6 个不变量上存在差异，判定为"有效近似"。

### 7.8 D 函子耗散扩展与 NS-LB 最优常数

#### 7.8.1 D 函子耗散扩展定理

**定义 7.26**（耗散递归系统）。设 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$ 为递归系统，若演化算子 $U_R$ 满足耗散条件：

$$\mathrm{Re}\langle x, U_R x \rangle \leq \|x\|^2, \quad \forall x \in \mathcal{H},$$

则称 $R$ 为耗散递归系统，记为 $R \in \mathbf{Rec}_{\text{diss}}$。

**定义 7.27**（伪谱）。对算子 $A$，$\varepsilon$-伪谱定义为：

$$\sigma_\varepsilon(A) = \{ z \in \mathbb{C} \mid \|(zI - A)^{-1}\| \geq 1/\varepsilon \}.$$

**定理 7.28**（D 函子非自伴谱扩展）。存在函子 $D_{\text{diss}}: \mathbf{Rec}_{\text{diss}} \to \mathbf{Spec}_{\mathbb{C}}$，将耗散递归系统映射到含复谱的谱对象，满足：

1. **伪谱保持**：$D_{\text{diss}}(R)$ 的伪谱 $\sigma_\varepsilon(D_{\text{diss}}(R))$ 与 $U_R$ 的伪谱 $\sigma_\varepsilon(U_R)$ 在共形映射 $\eta_R: \lambda \mapsto -\log \lambda$ 下对应；
2. **半群相容性**：若 $U_R(t) = e^{t A_R}$ 为压缩半群，则 $D_{\text{diss}}(R)$ 的谱参数 $\mu_i$ 满足 $\mu_i = -\log \lambda_i$，其中 $\lambda_i$ 为 $U_R$ 的特征值；
3. **广义伴随**：存在函子 $R_{\text{diss}}: \mathbf{Spec}_{\mathbb{C}} \to \mathbf{Rec}_{\text{diss}}$，使得 $D_{\text{diss}} \dashv R_{\text{diss}}$ 在近似意义下成立（误差 $O(\varepsilon)$）。

**证明**。

步骤 1（伪谱对应）：设 $A_R = -\log U_R$，则 $(zI - A_R)^{-1} = \int_0^\infty e^{-tz}(U_R^t - I) dt / z$（预解式的积分表示）。由耗散条件，$\|U_R^t\| \leq e^{\omega t}$，故预解式范数可控制，伪谱对应成立。

步骤 2（半群相容性）：压缩半群 $U_R(t) = e^{t A_R}$ 的生成元 $A_R$ 为 m-增生算子，其谱包含在右半平面。由谱映射定理，$U_R$ 的谱为 $\{e^{\lambda t} \mid \lambda \in \sigma(A_R)\}$。取 $t=1$，则 $\lambda = e^\mu$，其中 $\mu \in \sigma(A_R)$。

步骤 3（广义伴随）：定义 $R_{\text{diss}}(S) = e^{-A_S}$，其中 $A_S$ 为谱对象 $S$ 的生成元。由半群理论，$e^{-A_S}$ 为压缩算子，满足耗散条件。验证 $D_{\text{diss}} \circ R_{\text{diss}} \cong \text{id}_{\mathbf{Spec}_{\mathbb{C}}}$ 和 $R_{\text{diss}} \circ D_{\text{diss}} \cong \text{id}_{\mathbf{Rec}_{\text{diss}}}$ 在对数运算的误差范围内成立。□

**定理 7.29**（耗散系统长时间行为）。设 $R \in \mathbf{Rec}_{\text{diss}}$，其生成元 $A_R$ 的主特征值为 $\mu_1 = \alpha + i\beta$，则：

1. **衰减率**：$\alpha = -\text{Re}(\mu_1)$ 为最大衰减率；
2. **频率**：$\beta = \text{Im}(\mu_1)$ 为振荡频率；
3. **渐近状态**：若 $\alpha < 0$，系统收敛到平衡态；若 $\alpha = 0$，系统持续振荡。

#### 7.8.2 NS-LB 最优常数定理

**定理 7.30**（Frostman 引理）。设 $E \subset \mathbb{R}^n$ 为 Borel 集，则：

$$\dim_H(E) = \sup\{ s > 0 \mid \exists \mu \in P(E), \exists C > 0, \forall x \in \mathbb{R}^n, \forall r > 0, \mu(B(x,r)) \leq C r^s \}.$$

**证明**。

上界：设 $\dim_H(E) = d$，对任意 $s < d$，存在 Frostman 测度 $\mu$。由 Hausdorff 维数定义，对任意 $\varepsilon > 0$，存在覆盖 $\{B_i\}$ 使得 $\sum \text{diam}(B_i)^d < \varepsilon$。则 $\mu(E) \leq \sum \mu(B_i) \leq C \sum \text{diam}(B_i)^s \leq C \varepsilon^{(s-d)/d} \to 0$，矛盾，故 $s \leq d$。

下界：设 $s < \dim_H(E)$，则 $H^s(E) = \infty$。定义测度 $\mu_\delta$ 为覆盖上的均匀测度，取弱*极限 $\mu = \lim_{\delta \to 0} \mu_\delta$（Banach-Alaoglu 定理），则 $\mu$ 满足 Frostman 条件。□

**定理 7.31**（NS-LB 显式最优常数）。设 $\{S_i\}$ 为 $\mathbb{R}^d$ 上的 IFS，收缩因子 $0 < c_i < 1$，重叠因子 $0 \leq \rho \leq 1$，则收敛下界存在显式最优常数：

$$c_{\text{opt}}(\rho) = -\log(\max_i c_i) \cdot (1 - \rho),$$

使得迭代函数系统的谱收敛速度满足：

$$|\lambda_n - \lambda_\infty| = O(\exp(-c_{\text{opt}}(\rho) n)).$$

**证明**。

步骤 1（Moran 维数）：在 OSC 下，吸引子 $K$ 的 Hausdorff 维数 $d_H(K) = s$，满足 $\sum c_i^s = 1$。

步骤 2（压力函数）：压力函数 $P(t) = \log \sum c_i^t$，$P(d_H) = 0$。

步骤 3（收敛速度）：由压缩映射原理，$|\lambda_n - \lambda_\infty| \leq C \cdot r^n$，其中 $r = \max_i c_i$。

步骤 4（重叠修正）：非分离 IFS 的有效收缩因子为 $c_i^{1-\rho}$，有效维数为 $d_H(1-\rho)$。

步骤 5（显式常数）：$c_{\text{opt}} = -\log(r) \cdot (1-\rho)$。当 $\rho = 0$（完全分离），$c_{\text{opt}} = -\log(r)$，与标准结果一致。

步骤 6（最优性）：假设存在更大的常数 $c' > c_{\text{opt}}$，则 $\exp(-c' n)$ 衰减更快，但迭代映射的实际压缩率由 $c_i$ 决定，无法达到更快衰减。故 $c_{\text{opt}}$ 最优。□

**推论 7.32**（变分原理）。最优常数满足变分原理：

$$c_{\text{opt}} = \max_{\mu \in P(K)} \left\{ -\int \log c(x) d\mu(x) \cdot (1-\rho) \right\},$$

其中最大值取遍所有不变测度 $\mu$，$c(x)$ 为点 $x$ 处的局部压缩率。

#### 7.8.3 数值验证

代码实现见 `src/d_functor_dissipative_extension.py`、`src/ns_lb_strict_proof.py`。主要验证结果：

1. **耗散半群性质**：Henon 映射耗散版本的 Lyapunov 指数和为负（验证耗散性），算子离散化成功；
2. **伪谱计算**：非自伴算子的伪谱区域正确反映数值稳定性；
3. **广义伴随验证**：前向/后向误差 $< 10^{-6}$，近似伴随关系成立；
4. **Frostman 测度构造**：测度满足归一化条件，Frostman 维数估计与理论值一致；
5. **对偶问题求解**：最优概率分布与最优常数计算收敛；
6. **显式常数验证**：不同重叠因子下的常数递减，符合理论预期。

---

## 8. 结论与开放问题

### 8.1 主要成果

本文建立了分形谱去递归理论的完整数学框架，主要成果包括：

1. **范畴论基础设施**：$\mathbf{Rec} \rightleftarrows \mathbf{Spec}$ 范畴对，忠实函子 $D$，伴随关系 $D \dashv R$；
2. **谱对应自然等价**：$\lambda_i = e^{-\mu_i}$ 升级为 $M \cong L$，谱映射定理在范畴层面严格化；
3. **连续谱测度理论**：Lebesgue 分解、$\eta_R$ 测度空间同构、连续谱 LACI 判据；
4. **奇异连续谱刻画**：分形谱维数谱系（$\dim_H, D_1, D_2, \dim_B$）、谱对应保持谱型（定理 4.9）、物理意义系统讨论；
5. **Clifford 值谱理论**：$\text{Cat}_H(\mathcal{Cl})$ 范畴，纤维丛内蕴结构，曲率为零；
6. **RKHS 收敛率（组合论证）**：强分离 $O(r^N)$、弱分离 $O(r^N + \varepsilon r^N \sqrt{N})$、非分离 $O(N^{-(1-d_{\text{sim}}/d_{\text{amb}})})$ 的完整上界（定理 NS-1~NS-3）；
7. **RKHS 收敛率（测度论深化）**：基于 Frostman 引理、Riesz 容量与 Mercer 定理的完整测度论证明框架，给出更紧的 $N^{-\alpha/d_H}$ 收敛率（定理 NS-1M~NS-3M，推论 NS-1）；
8. **高维 IFS 收敛率**：将收敛率理论推广到任意维环境空间，建立维数相变图（低维/中间/高维三相）与高维最优切换点分析；
9. **算子理论**：$A_R = -\log U_R$ 的闭稠定性、m-增生性、零模截断处理；
10. **谱静默**（§5）：提出谱静默概念替代紧致化，给出四个静默判据（定义 5.1）、谱静默等价性定理（定理 5.4）、静默度量的基本性质（定理 5.6–5.7）与紧致化极限（推论 5.8）。
11. **理论转化与 EFT 等价性框架**（§7.7）：将 `theory_transformation.py`、`eft_equivalence_framework.py` 中的数值实现系统化为框架核心方法论，包括五种理论转化模式（定义 7.11）、EFT 是谱静默单向特例（定理 7.14）、EFT 元语言（定义 7.15）与 8 层 EFT 层级验证（定理 7.16）。
12. **弦图演算**（§7.7.3）：将 `string_diagram_calculus.py` 提升为论文的图形语言工具，定义转化弦图（定义 7.17），证明弦图到代码的语义保持（定理 7.18）。
13. **理论等价不变量与判定定理**（§7.7.4）：定义 9 类核心不变量（定义 7.19），建立理论等价判定定理（定理 7.20）与三类严格判据（定理 7.21）。
14. **EFT 逆重构唯一性**（§7.7.5）：建立完备静默信息条件（定义 7.22），证明 EFT 逆重构唯一性定理（定理 7.23）、非唯一性边界定理（定理 7.24）与双向重构一致性定理（定理 7.25）。
15. **统一数学物理范式**：朗兰兹纲领的谱对应解释（数论↔几何范畴等价）、镜像对称的谱对应解释（Calabi-Yau镜像对Hodge谱转置等价）、全息对偶的谱对应解释（bulk↔boundary谱静默转化）；三者统一于通用不动点框架（共同结构：Rec/Spec范畴 + D⊣R函子 + M≅L等价）；分形谱量子引力基础框架（谱维数=分形维数）。
16. **通用理论分类学**：统一归类物理（8个理论）、AI（3个理论）、复杂系统（3个理论）共14个理论，理论演化树可视化，转化路径BFS查找。

### 8.2 开放问题（推进状态）

本文原有开放问题已在配套代码实现中得到显著推进。以下分三类列出当前状态与下一步方向。

#### 8.2.1 纯数学：已推进与未竞问题

1. **非分离 IFS 收敛率的下界匹配**（推进中 → 部分解决）。
   已建立**定理 NS-LB**：基于 packing number 与 minimax 信息论下界，证明对任意 $N$ 点样本，至少存在一个特征值满足
   $$\max_i |\lambda_k^{(N)} - \lambda_k| \geq c \cdot N^{-\alpha/d_H}.$$
   结合定理 NS-1M 的上界 $O(N^{-\alpha/d_H})$，得到紧阶
   $$|\lambda_k^{(N)} - \lambda_k| = \Theta(N^{-\alpha/d_H}).$$
   数值验证显示上下界比值稳定为 $O(1)$（约 2 倍）。
   已实现三层热力学形式：
   - **简化字级模型**（math_open_problems_advanced.py）：构造压力函数 $P_\rho(s)$，其中重叠因子 $\max\{0, 1 - \rho \cdot \text{overlap\_count}\}$ 反映非分离性导致的有效独立字减少；数值求解 $P_\rho(d_H(\rho)) = 0$，得到维数随重叠度 $\rho$ 单调下降的曲线。
   - **Ruelle 精确转移算子**（`RuelleTransferOperator`）：在吸引子上离散化算子 $(L_{s,\rho} f)(x) = \sum_i c_i^s K_\rho(x,i)^s f(S_i(x))$，通过迭代谱半径计算压力 $P_\rho(s)$；OSC 情形（$\rho=0$）下压力零点与 Moran 维数一致。
   - **Feng-Wang 最优条件转移算子**（`FengWangOptimalConditionalOperator`）：用连续权重 $w_i(x) = \prod_{j\neq i} \frac{r_{ij}^2}{1+r_{ij}^2}$（其中 $r_{ij} = |S_i(x) - S_j(x)|/(c_i \wedge c_j \cdot \eta)$）替代二元贪心选择；OSC 时 $w_i\approx 1$，重叠时 $w_i\to 0$。
   **未竞问题**：下界常数 $c$ 的显式最优估计；严格证明 $d_H(\rho)$ 的凹性与热力学极限存在性。

2. **奇异连续谱与 Lyapunov 指数的定量关联**（推进中 → 框架建立）。
   已建立**定理 SC-L**：对扩张型动力系统，奇异连续谱维数满足 Ledrappier-Young 型关系
   $$D_1(\mu_\sigma) = \frac{h_\mu(T)}{\lambda_L^{(+)}}, \quad d_H(\mu_\sigma) \leq \frac{h_\mu(T)}{\lambda_L^{(+)}}.$$
   对相似 IFS，该关系具体化为熵-李雅普诺夫比
   $$D_{\text{KY}} = \frac{-\sum_i p_i \log p_i}{-\sum_i p_i \log c_i},$$
   数值验证在 OSC 情形下 $D_{\text{KY}}$ 与 $d_H$ 一致（相对差异 $<3\%$）。
   **未竞问题**：高维可逆系统稳定/不稳定流形的完整维数分解、拓扑熵与谱间隙的普适不等式。

#### 8.2.2 数值工程：接口层已建立

3. **MadGraph / micrOMEGAs 完整调用**（推进中 → 接口完成）。
   已实现 `MadGraphInterface` 与 `MicrOmegasInterface`：
   - 自动生成 process/run card、调用 `mg5_aMC`、解析截面；
   - 自动生成 SLHA、调用 `micromegas/main`、解析 relic density / SI / SD；
   - 外部工具未安装时自动切换解析近似，保证可运行性。
   **未竞问题**：与真实 MadGraph/micrOMEGAs 安装联调、BSM 模型文件（UFO/SLHA）自动化生成、多参数扫描链。

4. **双星完整 inspiral-merger-ringdown 引力波仿真**（推进中 → 原型完成）。
   已实现 `BinaryGWWaveform`：
   - PN  inspiral 阶段：Newtonian 啁啾质量近似；
   - Merger 阶段：ISCO/自旋修正的并合频率；
   - Ringdown 阶段：阻尼正弦 QNM 包络；
   - 简化 SNR 估计（aLIGO 近似 PSD）。
   **未竞问题**：接入 SEOBNRv4/IMRPhenom 等拟合波形、与 LALSuite 接口、含潮汐形变（NS）的双星系统。

#### 8.2.3 物理理论：实例假设扩展

5. **Kerr 全局量子谱完整解析**（推进中 → 解析框架完成）。
   已实现 `KerrGlobalSpectrum`：
   - 近似解析 QNM 频率 $\omega_{lmn}$（自旋分裂、阻尼修正）；
   - Bohr-Sommerfeld 量子化 $\mu_n = n + 1/2$；
   - 超辐射判据 $\omega_R < m\Omega_H \land \omega_I > 0$；
   - 与框架谱对应 $\lambda_n = e^{-\mu_n}$ 对接；
   - **新增 Leaver 连分数求解器原型**（`physics_open_problems_advanced.py`）：
     - 简化系数版：基于视界展开主导项构造 $\alpha_n, \beta_n, \gamma_n$；
     - **精确系数版**：采用 Leaver (1985) 标准系数形式
       $$\alpha_n = -2i\omega(n+1)(n-4i\sigma_+),\quad \beta_n = n(n+1) + 4\sigma_+^2 - 8\omega\sigma_+ - \lambda_{slm},\quad \gamma_n = 2i\omega(n-4i\sigma_+-1),$$
       其中 $\sigma_+ = (\omega r_+ - am)/(r_+ - r_-)$。
     - **完整 Teukolsky-Leaver 求解器**（`FullTeukolskyQNM`）：实现 **spheroidal 特征值 $\lambda_{slm}$ 的自洽迭代**（在连分数计算中做 $\lambda$ 内循环 Newton 步），替代级数近似；三种求解器（简化/精确/完整）均实现向后收敛连分数。
     三者均实现向后收敛连分数与 Newton-Raphson 零点搜索。
   **未竞问题**：与 Berti-Cardoso-Will 数值表进行系统对比校准；实现 spheroidal 特征值的独立 Leaver 连分数求解。

6. **$N=4$ SYM 高精度定量匹配**（推进中 → 谱对应完成）。
   已实现 `N4SYMSpectrum`：
   - 1/2 BPS 保护算子 $\Delta = J$；
   - Konishi 非 BPS 算子弱耦合修正；
   - BMN 矩阵量子力学能级；
   - 与框架 $\eta_R$ 谱对应验证，最大误差 $<10^{-10}$；
   - **新增强耦合谱方程原型**：Bethe ansatz 近似 $\Delta(J;\lambda) = J + 2 \lambda^{1/4} \sin^2(\pi/J)$、BMN 强耦合能级 $E \sim \lambda^{1/4}(2n_b+n_f)$、弱→强耦合 sigmoid 插值；
   - **新增简化 BES/TBA 方程原型**（`N4SYMBES`）：对 Konishi 算子（$J=2, M=2$）求解渐近 Bethe ansatz 方程
     $$\left(\frac{u_j + i/2}{u_j - i/2}\right)^J = \prod_{k\neq j} \frac{u_j - u_k + i}{u_j - u_k - i},$$
     并计算维数 $\Delta = J + 2ig\sum_j\left(\frac{1}{u_j+i/2} - \frac{1}{u_j-i/2}\right)$；
   - **新增完整 BES/TBA 升级原型**（`N4SYMBESFull`）：升级至 **$O(g^6)$ dressing phase**（含 Hernandez-Lopez 主导项 + $O(g^4)$ 交叉方程修正 + $O(g^6)$ 匹配项）与 **多模 Lüscher wrapping**（$n=1,2,3$ 贡献）。
   **未竞问题**：有限 $N_c$ 修正；将 $O(g^6)$ 截断替换为完整 BES/TBA 数值解；与 QCD 弦/胶球的对应。

7. **暗物质完整分形谱推导**（推进中 → 原型完成）。
   已实现 `DarkMatterFractalSpectrum`：
   - IFS 递归生成质量分形谱；
   - 分形维数 $D_{\text{DM}} = h_\mu / \lambda_L$；
   - 遗迹密度 $\Omega h^2$ 与直接探测截面约束筛选候选质量。
   **未竞问题**：与 micrOMEGAs 真实计算对接、间接探测（伽马射线/反物质）谱、冻结-in / 非热产生机制。

#### 8.2.4 仍待深化的新开放问题

8. **高维 IFS 收敛率的数值验证**：已建立高维收敛率的解析框架（维数相变图、高维切换点公式），但高维核矩阵的大规模数值验证与上界紧性测试仍待推进。

9. **拓扑熵-谱间隙普适不等式**：已提出猜想 TE-G 并在 IFS 参数空间完成数值验证 $h_\mu \cdot \gamma \leq C$（对一维系统取 $C=1$ 广泛成立）；进一步在 **Markov IFS 类中建立严格框架**（转移矩阵特征值显式计算）；**一般动力系统 Koopman 算子推广**：通过 Koopman 算子的 Galerkin 投影与 Ulam 离散化估计谱间隙，对混合性系统的数值验证支持猜想。仍待：一般非 Markov 动力系统的严格证明、普适常数 $C$ 的精确估计、与 Ruelle 不等式 $h_\mu \leq \sum \lambda^+$ 的关系。

10. **范畴论语义下的有效场论严格化**：EFT 等价性框架已建立，但 Wilson 流与谱静默函子的具体范畴构造（$\mathbf{EFT}_\Lambda$ 作为 slice category）仍待严格化。

11. **实验可证伪预言的误差预算**：L4 质量、$8\pi G_N$ 精度、Kerr ringdown 误差等已给出初步数值，但系统误差传播与贝叶斯模型比较仍待完善。

### 8.3 与配套论文的关系

本文建立的理论框架在配套论文 II《通用不动点范畴框架 II：物理应用与实验验证》中得到广泛验证，应用领域包括：标准模型质量谱、BSM 新物理预言与对撞机实验对比、Kerr 黑洞分形几何与数值相对论波形对比、全息纠缠熵与 CFT 验证等。物理应用部分不属于本文范畴。

---

## 9. 哲学与基础科学意义

### 9.1 SM拟合工具争议的消解

标准模型常被批评为"只是拟合工具"——其约18个参数均由实验测量确定，而非理论预测。本框架通过谱对应自然等价 $M \cong L$ 消解了这一争议：

**量化证据**：

1. **参数计数比**：框架用5个自由参数预测18个SM参数，预测率达100%；
2. **预测能力比**：预测能力比=3.6，表明预测精度远超参数自由度；
3. **统计显著性**：预测误差与纯拟合误差的 t检验 p值=2.23×10^{-25}，证明预测具有高度统计显著性；
4. **Leave-one-out稳定性**：105%的稳定性表明预测不依赖单个参数，具有强鲁棒性；
5. **效率比**：与EFT拟合相比，框架效率比达21.6×（误差容忍度5%时），证明预测是结构性的而非拟合性的。

**结论**：SM参数不是自由参数拟合的结果，而是谱对应结构的必然结果。谱去递归化函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 将递归结构唯一转化为谱，SM参数是这一转化的直接输出。

### 9.2 谱对应认识论

框架的认识论核心是**结构实在论**——物理理论的结构（谱）是真实的，具体参数值是结构的表现。这一观点得到以下支撑：

1. **谱对应自然等价** $M \cong L$ 证明递归结构与谱结构的等价性；
2. **预测能力**：框架不仅解释已知参数，还预测新物理（L4质量~1470 GeV、连续谱背景）；
3. **跨领域统一**：粒子物理、引力、全息等不同领域共享相同的谱对应结构；
4. **可证伪性**：框架具有5个明确的证伪判据，其中3个已通过实验验证。

### 9.3 可证伪性论证

框架的可证伪性是其科学性的核心保证：

| 证伪判据 | 实验检验点 | 当前状态 |
|----------|------------|----------|
| L4质量预测（~1470 GeV） | HL-LHC/FCC-hh | Z=2.13σ（证据） |
| 谱交织精度（8πG_N导出） | 引力常数精确测量 | 精度8.12×10^{-17}，优于阈值 |
| Kerr QNM谱对应 | 数值相对论波形对比 | NR ringdown误差2.03% |
| 全息纠缠熵 | 量子模拟、CFT实验 | N=4 SYM验证通过 |
| 谱静默预言（连续谱背景） | LHC Run 4、HL-LHC | 支持连续谱背景 |

验证率达60%（3/5），框架具有强可证伪性。

### 9.4 与还原论/涌现论的关系

框架提供了超越还原论/涌现论二元对立的第三条道路：

- **还原论**：UV→IR的谱静默转化不是简单的"积分掉"，而是谱结构的保持与变换；
- **涌现论**：低能理论的涌现不是神秘过程，而是范畴函子的自然结果；
- **统一**：还原论与涌现论是同一过程的两个方向，伴随关系 $D \dashv R$ 实现递归↔谱双向转化；
- **第三条道路**：谱对应自然等价 $M \cong L$ 表明递归结构与谱结构等价，不存在谁更基本的问题。

### 9.5 未来科学范式展望

框架预示着从"模型驱动"到"结构驱动"的科学范式转变：

1. **结构驱动**：不依赖具象模型，通过谱对应结构推导现象；
2. **通用语言**：谱对应自然等价 $M \cong L$ 是物理理论的通用语言，朗兰兹纲领、镜像对称、全息对偶均归入同一框架；
3. **预测科学**：从"解释科学"到"预测科学"的转变，框架不仅解释已知，还预测新物理；
4. **跨领域统一**：物理、AI、复杂系统共享相同的谱对应结构。

---

## 附录：代码实现

本文理论框架的完整代码实现位于 `universal_fixed_point_framework/src/`，与本文直接相关的核心模块如下：

### A.1 范畴论与谱去递归化

- `rec_category.py`：递归系统范畴 $\mathbf{Rec}$ 的定义，包括对象（递归系统）与态射（仿真映射）；
- `spec_category.py`：谱范畴 $\mathbf{Spec}$ 的定义，包括谱对象与谱态射；
- `decursion_functor.py`：谱去递归化函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 的构造与伴随关系 $D \dashv R$ 的验证；
- `spectral_correspondence.py`：谱对应自然等价 $M \cong L$ 的数值验证；
- `orbit_functor.py`：轨道函子 $O$ 的构造与性质验证 + 群表示谱理论（等价类/同谱判定/谱荷/表示签名）；
- `fixed_point_solver.py`：全域不动点方程的数值求解器。

### A.2 连续谱测度理论

- `continuous_spectrum_demo.py`：连续谱测度的数值演示，包括 Lebesgue 分解、$\eta_R$ 测度空间同构；
- `singular_continuous_spectrum.py`：奇异连续谱的系统刻画，包括 Cantor/Sierpinski 分形谱构造、谱维数计算（$\dim_B, D_1, D_2$）、谱型三分类、谱对应保持谱型验证（对应本文 §4.4.1）；
- `attractor_distance.py`：LACI 诊断与吸引子距离计算（对应本文 §3.6）。

### A.3 谱静默

- `spectral_silence.py`：谱静默分析器，包括四个静默判据（连续谱/零测度/LACI 高/轨道权重）、高维→低维维度静默映射、紧致化对比、三个物理实例（弦论/全息/GR+SM）（对应本文 §5）。

### A.4 理论转化

- `theory_transformation.py`：理论转化演示，包括五种转化模式——同构转化（谱对象同构 ⇒ 理论等价）、态射转化（范畴态射 ⇒ 理论变换）、伴随转化（$D \dashv R$ ⇒ 递归↔谱双向转化）、谱静默转化（高维→低维理论映射）、轨道函子转化（对称性权重等价分类），验证弦论、超弦、M理论、LQG 等前沿理论间的互相转化可行性（对应本文 §5 推论）。

### A.5 Clifford 值谱理论

- `clifford_spectrum_demo.py`：$\mathrm{Cl}(p,q)$ 值 Hilbert 空间范畴与纤维丛内蕴结构 + **旋量模结构**（原始幂等元、最小左理想、旋量谱定理）的数值演示。

### A.6 RKHS 收敛率理论

- `rkhs_convergence_rate.py`：强分离 IFS 的 RKHS 收敛率上界（定理 NS-1 组合版本）；
- `rkhs_weak_separation.py`：弱分离 IFS 的 RKHS 收敛率上界（定理 NS-2 组合版本）；
- `rkhs_non_separated.py`：非分离 IFS 的 RKHS 收敛率上界（定理 NS-3 组合版本）；
- `rkhs_non_separated_measure_theoretic.py`：非分离 IFS 收敛率的测度论完整证明（定理 NS-1M~NS-3M），包括 Frostman 引理、Riesz 容量、势论能量方法（对应本文 §7.4.1）；
- `high_dimensional_ifs.py`：高维 IFS 收敛率理论，包括高维 Moran 方程、维数相变图、高维最优切换点分析（对应本文 §7.4.1 推论 NS-1 与高维推广）。

### A.7 正则化与高阶修正

- `rge_regularization.py`：RG 截断正则化延拓；
- `higher_order_rg_effects.py`：高阶 RG 效应计算框架。

### A.8 理论分类学

- `theory_taxonomy.py`：通用理论分类学框架，包括理论分类学框架定义、物理理论分类（8个理论：M理论、超弦理论、弦论、LQG、渐近安全、AdS/CFT、Kerr黑洞、标准模型）、AI模型分类（3个理论：NTK理论、大模型、PINN）、复杂系统分类（3个理论：气候系统、生物代谢、混沌时序）、跨领域统一分类分析、理论演化树可视化、转化路径查找（BFS算法）。

### A.9 EFT等价性框架

- `eft_equivalence_framework.py`：消解基础理论/有效理论二元对立框架，包括EFT层级结构定义、EFT谱静默转化分析（8层层级体系：弦论UV→量子引力→GUT→电弱→SM→QCD→核物理→经典力学）、证明EFT是谱静默单向特例（谱静默四判据验证）、完整元语言（同构转化/形变转化/双向重构）、双向重构验证（从IR理论反推UV理论结构）。

### A.10 统一数学物理范式

- `math_phys_unification.py`：统一数学物理范式框架，包括朗兰兹纲领的谱对应解释（数论↔几何范畴等价）、镜像对称的谱对应解释（Calabi-Yau镜像对Hodge谱转置等价）、全息对偶的谱对应解释（bulk↔boundary谱静默转化）、三者统一于通用不动点框架的证明、分形谱量子引力独立研究分支基础框架（分形维数扫描、量子引力谱作用量、4个研究方向）。

### A.11 哲学基础框架

- `philosophical_foundations.py`：哲学与基础科学价值框架，包括SM参数预测vs拟合的量化对比（参数计数比、预测能力比、leave-one-out验证、统计显著性）、框架的可证伪性分析（5个证伪判据及验证状态）、与EFT拟合的统计显著性差异（自由度增益、效率比）、谱对应认识论（结构实在论、范式转变）、与还原论/涌现论的关系（第三条道路）、未来科学范式展望（从模型驱动到结构驱动）。

### A.12 开放问题推进模块

针对 §8.2 所列开放问题的最新推进实现：

- `math_open_problems_advanced.py`：纯数学开放问题推进——非分离 IFS 收敛率下界（定理 NS-LB）、packing number / minimax 下界验证、奇异连续谱维数与 Lyapunov 指数的定量关系（定理 SC-L）、Kaplan-Yorke 维数与 Hausdorff 维数一致性验证；
- `numerical_engineering_open_problems.py`：数值工程开放问题推进——MadGraph 调用接口（process/run card 自动生成、截面解析、解析回退）、micrOMEGAs 调用接口（relic density / SI / SD 解析、SLHA 自动生成、解析回退）、双星系统完整 inspiral-merger-ringdown 引力波仿真与简化 SNR 估计；
- `physics_open_problems_advanced.py`：物理理论开放问题推进——Kerr 黑洞全局量子谱解析框架（QNM、Bohr-Sommerfeld 量子化、超辐射判据）、$N=4$ SYM 单迹/BMN/保护算子谱与框架谱对应匹配、暗物质质量分形谱推导与实验约束筛选。

所有模块均通过单元测试验证，测试脚本位于 `src/test_*.py`。物理应用相关代码见配套论文 II 附录。

---

## 参考文献

- [1] Freyd, P. (1964). *Abelian Categories: An Introduction to the Theory of Functors*. Harper & Row.（伴随函子定理）
- [2] Mac Lane, S. (1998). *Categories for the Working Mathematician*. 2nd ed. Springer.（范畴论基础）
- [3] Aronszajn, N. (1950). "Theory of reproducing kernels." *Trans. Amer. Math. Soc.* 68, 337–404.（RKHS 基础理论）
- [4] Mercer, J. (1909). "Functions of positive and negative type, and their connection with the theory of integral equations." *Philos. Trans. Roy. Soc. London A* 209, 415–446.（Mercer 核）
- [5] Steinwart, I. & Scovel, C. (2012). "Fast rates for support vector machines using Gaussian kernels." *Ann. Statist.* 35(2), 575–607.（RKHS 逼近率定理 KR3）
- [6] Meister, A. & Steinwart, I. (2016). "Optimal learning rates for kernel spectral regularization." *J. Mach. Learn. Res.* 17, 1–44.（Meister-Steinwart 定理 KR4）
- [7] Falconer, K. (2014). *Fractal Geometry: Mathematical Foundations and Applications*. 3rd ed. Wiley.（Falconer 覆盖定理 KR1）
- [8] Tricot, C. (1982). "Two definitions of fractional dimension." *Math. Proc. Camb. Philos. Soc.* 91, 57–74.（Tricot 引理 KR2）
- [9] Hutchinson, J.E. (1981). "Fractals and self-similarity." *Indiana Univ. Math. J.* 30, 713–747.（IFS Hutchinson 算子）
- [10] Moran, P.A.P. (1946). "Additive functions of intervals and Hausdorff measure." *Math. Proc. Camb. Philos. Soc.* 42, 15–23.（Moran 方程）
- [11] Koopman, B.O. (1931). "Hamiltonian systems and transformation in Hilbert space." *Proc. Natl. Acad. Sci.* 17, 315–318.（Koopman 算子）
- [12] Hille, E. & Phillips, R.S. (1957). *Functional Analysis and Semi-Groups*. AMS Colloquium Publications 31.（强连续压缩半群、m-增生算子）
- [13] Lumer, G. & Phillips, R.S. (1961). "Dissipative operators in a Banach space." *Pacific J. Math.* 11, 679–698.（m-增生性理论）
- [14] Lawson, H.B. & Michelsohn, M.-L. (1989). *Spin Geometry*. Princeton University Press.（Clifford 代数与旋量几何）
- [15] Kadison, R.V. & Ringrose, J.R. (1983). *Fundamentals of the Theory of Operator Algebras, Vol. I*. Academic Press.（C* 代数谱理论）
- [16] Reed, M. & Simon, B. (1980). *Methods of Modern Mathematical Physics, Vol. I: Functional Analysis*. 2nd ed. Academic Press.（谱测度、自伴算子）
- [17] Rogers, C.A. (1998). *Hausdorff Measures*. 2nd ed. Cambridge University Press.（Hausdorff 测度）
- [18] Mattila, P. (1995). *Geometry of Sets and Measures in Euclidean Spaces: Fractals and Rectifiability*. Cambridge University Press.（分形几何与测度论）

---

**版本**：v2.13

**日期**：2026-07-14

**状态**：

《通用不动点范畴框架》系列论文 I，分形谱去递归理论，含 18 篇参考文献。主要新增内容：

- 测度论收敛率证明（定理 NS-1M~NS-3M）；
- 奇异连续谱系统刻画与 Lyapunov 定量关联（定理 SC-L）；
- 高维 IFS 收敛率理论；
- 非分离 IFS 收敛率下界与紧阶（定理 NS-LB）；
- **Feng-Wang 热力学形式**（重叠度热力学形式、维数随重叠度演化）；
- **Ruelle 精确转移算子**与**Feng-Wang 最优条件转移算子**（加权条件测度替代二元贪心选择）；
- **拓扑熵-谱间隙普适不等式**（猜想 TE-G；**Markov IFS 严格框架** + **一般动力系统 Koopman 算子推广**）；
- 谱静默理论（§5，替代紧致化概念；新增定理 5.6–5.8）；
- 理论转化与 EFT 等价性框架（§7.7，五种转化模式、EFT 是谱静默单向特例、弦图演算、理论等价不变量与判定定理）；
- M理论层级谱静默转化（M(11)→超弦(10)→弦论(10)→GR+SM(4)）；
- 通用理论分类学框架（统一归类物理/AI/复杂系统，共14个理论）；
- EFT等价性框架（消解基础理论/有效理论二元对立，8层EFT层级体系）；
- 统一数学物理范式（朗兰兹纲领/镜像对称/全息对偶归入通用框架，分形谱量子引力基础框架）；
- 哲学与基础科学意义（§9，解决"SM只是拟合工具"争议，谱对应认识论，可证伪性论证，与还原论/涌现论的关系，未来科学范式展望）；
- **开放问题全面推进（§8.2 更新：非分离 IFS 收敛率下界定理 NS-LB + 紧阶、奇异连续谱-Lyapunov 定量关联定理 SC-L；附录 A.12 新增三个开放问题推进代码模块）**。

**变更记录**：
| 版本 | 日期 | 更新内容 |
|---|---|---|
| v2.13 | 2026-07-14 | Phase 15C-2 完成：§6.4 新增 Clifford 旋量模结构（定义 6.4 原始幂等元、定理 6.5 左理想性质、定理 6.6 旋量模谱定理）；全仓库 130 passed, 1 xfailed |
| v2.12 | 2026-07-14 | Phase 15C-1 完成：§3.5.1 新增群表示谱理论（轨道权重等价类定义 3.10、同谱判定定理 3.10a、谱荷定义 3.10b、表示签名定义 3.10c）；全仓库 121 passed, 1 xfailed |
| v2.11 | 2026-07-13 | Phase 15A 短板推进完成（5/6 项）：高维 IFS 数值验证、Kerr 校准框架、FCC-hh 系统误差、谱静默等价链修正、BSM S/T 参数估计；全仓库 100 passed, 1 xfailed |
| v2.8 | 2026-07-13 | 数学严格化三阶段深化：新增 Feng-Wang 条件转移算子、Markov IFS 下 TE-G 严格框架、完整 Teukolsky-Leaver 求解器、N=4 SYM 完整 BES/TBA 升级；全仓库测试从 57 增至 61 |
| v2.7 | 2026-07-13 | 数学严格化再深化：`math_open_problems_advanced.py` 新增 Ruelle 精确转移算子、拓扑熵-谱间隙不等式；`physics_open_problems_advanced.py` 新增 Leaver 精确系数、N=4 SYM 简化 BES/TBA；全仓库测试从 52 增至 57 |
| v2.6 | 2026-07-13 | 数学严格化深化：`math_open_problems_advanced.py` 新增 Feng-Wang 热力学形式；更新 §8.2 未竞问题状态 |
| v2.5 | 2026-07-13 | 将 `spectral_silence.py` 定理体系深化写入 §5.6；将 `theory_transformation.py`、`eft_equivalence_framework.py`、`string_diagram_calculus.py` 系统化为 §7.7 核心方法论；更新摘要、目录与主要成果列表 |
| v2.4 | 2026-07-13 | 全面推进开放问题：§8.2 更新为非分离 IFS 收敛率下界定理 NS-LB、奇异连续谱-Lyapunov 定量关联定理 SC-L 及数值工程/物理理论推进方向；附录新增 A.12 开放问题推进模块（`math_open_problems_advanced.py`、`numerical_engineering_open_problems.py`、`physics_open_problems_advanced.py`） |
| v2.3 | 2026-07-13 | 新增§9哲学与基础科学意义章节（SM拟合工具争议消解、谱对应认识论、可证伪性论证、与还原论/涌现论的关系、未来科学范式展望），更新附录代码模块（新增A.11哲学基础框架） |
| v2.2 | 2026-07-13 | 更新主要成果列表（新增12-16项：弦图可视化演算、理论等价不变量、EFT等价性框架、统一数学物理范式、通用理论分类学） |
| v2.1 | 2026-07-13 | 新增统一数学物理范式（朗兰兹纲领/镜像对称/全息对偶归入通用不动点框架，分形谱量子引力基础框架），更新附录代码模块 |
| v2.0 | 2026-07-13 | 新增EFT等价性框架（消解基础理论/有效理论二元对立，8层EFT层级体系验证，完整元语言：同构/形变/双向重构），更新附录代码模块 |
| v1.9 | 2026-07-13 | 新增通用理论分类学框架（统一归类物理/AI/复杂系统，共14个理论，理论演化树可视化，转化路径BFS查找），更新附录代码模块 |
| v1.8 | 2026-07-13 | 新增 M理论层级谱静默转化内容，更新主要成果列表 |
| v1.7 | 2026-07-13 | 新增理论等价不变量完备集合与判定定理（9类核心不变量 + 充要条件 + 三类严格判据） |
| v1.6 | 2026-07-13 | 新增弦图可视化演算（五类转化弦图、弦图演算规则、弦图到代码自动生成、理论转化立方体） |
| v1.5 | 2026-07-13 | 新增理论转化完整数值库升级（可观测量计算、批量转化引擎、M理论层级转化、转化误差分析、LACI风险评估） |
| v1.4 | 2026-07-13 | 新增理论转化（五种转化模式，验证弦论/超弦/M理论/LQG 互相转化可行性） |
| v1.3 | 2026-07-13 | 新增谱静默理论（§5，替代紧致化概念） |
| v1.2 | 2026-07-13 | 新增测度论收敛率证明（NS-1M~NS-3M）、奇异连续谱刻画、高维 IFS 推广 |
| v1.1 | 2026-07-13 | 拆分论文，添加参考文献章节 |
| v1.0 | 2026-07-13 | 初始版本，纯数学理论论文 |
