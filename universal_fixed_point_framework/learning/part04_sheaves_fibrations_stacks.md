# Part 4：层、Grothendieck 纤维化与栈

> 目标：理解 UFPF 中谱丛、谱预层、Grothendieck 纤维化的构造，能够复述 Paper XXI 中 Temp/RG/Noise 等参数谱丛的定义。

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

**定义 4.5**（Cartan 提升）。函子 $\pi: \mathcal{E} \to \mathcal{B}$ 称为 Grothendieck 纤维化，若对任意 $e \in \mathcal{E}$ 和 $\mathcal{B}$ 中态射 $f: b \to \pi(e)$，存在 $\mathcal{E}$ 中态射 $\tilde{f}: e' \to e$（称为 Cartan 提升）满足：
- $\pi(\tilde{f}) = f$
- 万有性质：任何其他提升唯一分解通过 $\tilde{f}$

**定义 4.6**（分裂纤维化）。若 Cartan 提升的选择可规范化为函子（恒等保持、复合保持），则称分裂 Grothendieck 纤维化。

### UFPF 实例：谱丛总范畴

Paper XXI 定义 2.1-2.2：Grothendieck 纤维化是"一族对象随参数变化"的严格数学语言。UFPF 中所有物理实例均为分裂纤维化：

- **Temp**：温度参数谱丛 $\pi_T: \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \to \mathbf{Temp}$
- **RG**：能标参数谱丛 $\pi_\mu: \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp}) \to \mathbf{RG}$
- **Noise**：噪声强度谱丛 $\pi_\eta$
- **Sig**：Clifford 签名谱丛
- **Kerr**：黑洞参数谱丛
- **Flt**：味扇区谱丛

## 4.4 纤维与截面

**定义 4.7**（纤维）。对 $b \in \mathcal{B}$，纤维 $\mathcal{E}_b$ 是 $\pi^{-1}(b)$ 构成的子范畴。

**定义 4.8**（截面）。截面是函子 $\sigma: \mathcal{B} \to \mathcal{E}$ 使得 $\pi \circ \sigma = \mathrm{id}_{\mathcal{B}}$。

### UFPF 实例

Paper XXI §1.1：物理系统是参数空间上的谱族。截面编码物理可观测量作为参数的函数，如 $T_c$、$\Delta\lambda_{\min}$、QNM 频率等。

Paper XXII §2：Cartan 提升的谱流形式为：

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

## 4.7 练习

1. 验证常值预层 $\mathcal{F}(U) = S$（$S$ 为固定集合）是层。
2. 解释为什么 Paper XVI 中"广义协变原理等价于层公理"在物理上意味着什么。
3. 写出 Paper XXI 中 Grothendieck 纤维化的五个组成要素：基空间、纤维、投影、Cartan 提升、截面。
4. 在 Kerr 谱覆盖中，基空间是什么？纤维是什么？分支点对应什么物理现象？
5. 为什么 UFPF 中所有物理纤维化都是**分裂**的？非分裂纤维化可能出现在什么场景？

## 4.8 关键要点

- **预层**是反变函子，**层**额外满足局域性与粘合性。
- **Grothendieck 纤维化**是 UFPF 上层建筑的核心，统一了温度、能标、噪声、签名等参数化谱族。
- **截面**是物理可观测量的范畴论对应，**Cartan 提升**是参数演化的谱流方程。
- **谱栈/谱覆盖**将纤维化与层论结合，处理弯曲时空与多参数物理系统的局域-整体结构。
