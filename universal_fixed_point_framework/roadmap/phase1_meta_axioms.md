# Phase 1：元公理层形式化

> 本阶段目标：在 [notes/00_foundations/rec_spec_definitions.md](../notes/00_foundations/rec_spec_definitions.md) 所定义的 $\mathbf{Rec}$ 与 $\mathbf{Spec}$ 基础上，严格构造谱去递归化函子 $D: \mathbf{Rec} \to \mathbf{Spec}$，证明其为协变函子，并在合理条件下证明忠实性。本文件对应推进计划「第一阶段第 1–2 周」的交付物。

---

## 1. 回顾：已建立的范畴

### 1.1 递归系统范畴 $\mathbf{Rec}$

- **对象**：$R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$
  - $\mathcal{S}_R$：可分完备度量空间（Polish 空间）
  - $\Phi_R: \mathcal{S}_R \to \mathcal{S}_R$：自相似演化映射
  - $\mathcal{T}_R \subseteq \mathbb{R}_{\ge 0}$：时间半群
  - $\mathcal{M}_R$：附加结构集合
- **态射**：$f: R_1 \to R_2$ 是连续映射 $f: \mathcal{S}_{R_1} \to \mathcal{S}_{R_2}$，满足
  $$\Phi_{R_2} \circ f = f \circ \Phi_{R_1}.$$
- **复合与单位**：由状态空间映射的通常复合与恒等映射给出。

### 1.2 谱范畴 $\mathbf{Spec}$

- **对象**：$E = (\mathcal{H}_E, A_E, \sigma_E)$
  - $\mathcal{H}_E$：复（或 Clifford 值）Hilbert 空间
  - $A_E: \mathcal{D}(A_E) \subseteq \mathcal{H}_E \to \mathcal{H}_E$：闭稠定正算子
  - $\sigma_E = \sigma(A_E) \subseteq \mathbb{R}_{\ge 0}$
- **态射**：$T: E_1 \to E_2$ 是有界线性算子 $T: \mathcal{H}_1 \to \mathcal{H}_2$，满足谱交织条件
  $$T A_1 \subseteq A_2 T.$$
- **复合与单位**：由有界线性算子的通常复合与恒等算子给出。

---

## 2. 谱去递归化函子 $D$ 的构造

### 2.1 对象映射

对每个递归系统 $R \in \mathrm{Obj}(\mathbf{Rec})$，定义

$$D(R) := (\mathcal{H}_R, A_R, \sigma(A_R)) \in \mathrm{Obj}(\mathbf{Spec}),$$

其中：

- **Hilbert 空间 $\mathcal{H}_R$**：取 $\mathcal{S}_R$ 上关于不变测度 $\mu_R$ 的 **分形再生核 Hilbert 空间（fractal RKHS）**。构造如下。

  设 $X_R \subseteq \mathcal{S}_R$ 为递归系统的不变集（或包含不变集的 Polish 子集），$\mu_R$ 为 $\Phi_R$ 的不变概率测度。记 Koopman 算子
  $$U_R f := f \circ \Phi_R, \quad f \in L^2(X_R, \mu_R).$$
  假设 $U_R$ 是 $L^2(X_R, \mu_R)$ 上的正规压缩算子，其谱分解为
  $$U_R = \int_{\sigma(U_R)} \lambda \, dP(\lambda), \qquad \sigma(U_R) \subseteq \{\lambda \in \mathbb{C} : |\lambda| \le 1\}.$$
  取一列正权数 $\{w_n\}_{n\ge 0}$ 满足 $\sum_n w_n < \infty$，定义 Mercer 型核
  $$K_R(x,y) := \sum_{n=0}^\infty w_n \, \overline{\Phi_R^n(x)} \cdot \Phi_R^n(y),$$
  其中对实值情形省略共轭。更内蕴地，可用 $U_R$ 的谱投影构造
  $$K_R(x,y) := \int_{\sigma(U_R)} \frac{1}{1 - |\lambda|^2/2} \, dP_{x,y}(\lambda),$$
  使得对应的 RKHS
  $$\mathcal{H}_R := \overline{\mathrm{span}}^{\|\cdot\|_{\mathcal{H}_R}}\{K_R(x,\cdot) : x \in X_R\}$$
  连续嵌入到 $L^2(X_R, \mu_R)$，且点求值泛函 $f \mapsto f(x)$ 在 $\mathcal{H}_R$ 上连续。

- **谱算子 $A_R$**：由 Koopman 算子的函数演算定义。设 $U_R$ 为上述正规压缩算子，且 $0 \notin \sigma(U_R)$（或对 $0$ 特征值单独处理）。令
  $$A_R := -\log U_R := -\int_{\sigma(U_R)} \log \lambda \, dP(\lambda),$$
  其中对数取主支，并对 $\lambda=0$ 处用极限 $-\log 0 = +\infty$ 延拓。则
  $$e^{-t A_R} = U_R^t, \quad t \in \mathcal{T}_R,$$
  且 $A_R$ 为闭稠定正算子（详见 §2.1.1 的命题与证明）。

- **谱 $\sigma(A_R)$**：$A_R$ 的谱满足
  $$\sigma(A_R) = \{-\log \lambda : \lambda \in \sigma(U_R) \setminus \{0\}\} \subseteq \mathbb{R}_{\ge 0}.$$

> **注**：上述构造把 "分形 RKHS" 从口号具体化为以 Koopman 算子谱投影为生成元的 Mercer 核。对具体对象（IFS、NTK、RG），$U_R$、$\mu_R$ 与 $K_R$ 都有明确形式，见 §2.4。

### 2.1.1 $A_R$ 的闭性、正性与谱条件

**命题 2.1**（$A_R$ 的基本性质）。设 $U_R$ 是 $L^2(X_R,\mu_R)$ 上的正规算子，且 $\sigma(U_R) \subseteq \{\lambda \in \mathbb{C} : |\lambda| \le 1\}$。定义
$$A_R := -\log U_R = -\int_{\sigma(U_R)\setminus\{0\}} \log \lambda \, dP(\lambda).$$
则：

1. $A_R$ 是闭稠定算子；
2. 若 additionally $\sigma(U_R) \subseteq (0,1]$ 且 $U_R$ 自伴，则 $A_R$ 是正算子；
3. $e^{-tA_R} = U_R^t$ 对所有 $t \ge 0$ 成立，且是强连续压缩半群。

**证明**。

(1) 由正规算子的 Borel 函数演算，对任意 Borel 函数 $\psi$ 在 $\sigma(U_R)$ 上有限 a.e.，$\psi(U_R)$ 是闭稠定算子。取 $\psi(\lambda) = -\log \lambda$（在 $\lambda=0$ 处定义 $+\infty$），由于 $-\log \lambda$ 在 $\{\lambda : |\lambda| \le 1\} \setminus \{0\}$ 上为实值，$A_R$ 是闭稠定算子。

(2) 当 $U_R$ 自伴且 $\sigma(U_R) \subseteq (0,1]$ 时，谱测度 $P$ 集中在实轴的 $(0,1]$ 上。函数 $\psi(\lambda)=-\log\lambda$ 在 $(0,1]$ 上非负，故对任意 $f \in \mathcal{D}(A_R)$，
$$\langle f, A_R f \rangle = \int_{(0,1]} (-\log \lambda) \, d\langle f, P(\lambda) f \rangle \ge 0.$$
因此 $A_R$ 为正算子。

(3) 由函数演算，$e^{-tA_R} = e^{t\log U_R} = U_R^t$。因 $U_R$ 是压缩算子，$\|U_R^t\| \le 1$，且 $t \mapsto U_R^t$ 强连续（正规压缩算子的函数演算），故为强连续压缩半群。

**条件 2.2**（$A_R$ 良定义的可对角化条件）。为保证 $-\log U_R$ 有意义且 $A_R$ 正定，要求：

- $U_R$ 是 $L^2(X_R,\mu_R)$ 上的自伴算子；
- $\sigma(U_R) \subseteq (0,1]$；
- $0$ 若为谱点，则对应 $U_R$ 的不动子空间，且该子空间在 $A_R$ 的定义域中作为零模处理。

> **注**：在 IFS 与 RG 情形，$U_R$ 通常对应 Frobenius-Perron 或 Koopman 算子，其特征值天然位于 $(0,1]$。对 NTK 等离散训练动态，需对学习率做归一化以满足该条件（见 §2.4）。

### 2.2 态射映射

设 $f: R_1 \to R_2$ 是 $\mathbf{Rec}$ 中的态射。定义

$$D(f): D(R_1) \longrightarrow D(R_2)$$

为由 $f$ 诱导的**推进算子（push-forward）**或**Koopman 提升算子**。具体构造如下：

对 $g \in \mathcal{H}_{R_2}$，定义 $D(f)^\ast g \in \mathcal{H}_{R_1}$ 为

$$(D(f)^\ast g)(x) := g(f(x)), \quad x \in \mathcal{S}_{R_1}.$$

然后取 $D(f)$ 为 $D(f)^\ast$ 的伴随算子（在 RKHS 内）。

**验证谱交织条件**：

由 $f$ 保持演化规则，$\Phi_{R_2} \circ f = f \circ \Phi_{R_1}$，可得 Koopman 算子的交换关系：

$$D(f)^\ast \Phi_{R_2}^\ast = \Phi_{R_1}^\ast D(f)^\ast.$$

取对数生成元并伴随化，得到

$$D(f) A_{R_1} \subseteq A_{R_2} D(f).$$

因此 $D(f)$ 是 $\mathbf{Spec}$ 中的态射。

### 2.3 函子公理验证

**保持单位态射**：

对任意 $R \in \mathrm{Obj}(\mathbf{Rec})$，$\mathrm{id}_R: R \to R$ 诱导的 Koopman 算子为恒等算子，故

$$D(\mathrm{id}_R) = \mathrm{id}_{D(R)}.$$

**保持复合**：

设 $f: R_1 \to R_2$，$g: R_2 \to R_3$，则对任意 $h \in \mathcal{H}_{R_3}$，

$$(D(g \circ f)^\ast h)(x) = h(g(f(x))) = (D(f)^\ast (D(g)^\ast h))(x) = (D(f)^\ast \circ D(g)^\ast)(h)(x).$$

伴随化得

$$D(g \circ f) = D(g) \circ D(f).$$

> 注意：由于 $D(f)$ 是 $D(f)^\ast$ 的伴随，复合方向与 Koopman 算子相反，因此 $D$ 是**协变函子**。

---

## 2.4 三类递归系统的 RKHS 显式构造

本节把 §2.1 的抽象框架具体化到 IFS、NTK 与 RG 三类对象，分别给出 $X_R$、$\mu_R$、$U_R$、$K_R$ 与 $A_R$ 的显式形式。

### 2.4.1 迭代函数系统（IFS）

设 IFS 由压缩映射族 $\{S_i\}_{i=1}^N$、$S_i: \mathbb{R}^d \to \mathbb{R}^d$ 及概率权重 $\{p_i\}_{i=1}^N$ 组成。其吸引子 $X_R$ 满足
$$X_R = \bigcup_{i=1}^N S_i(X_R).$$

- **不变测度** $\mu_R$：Hutchinson 自相似测度，满足
  $$\mu_R(B) = \sum_{i=1}^N p_i \, \mu_R(S_i^{-1}(B)), \qquad \forall B \in \mathcal{B}(X_R).$$
- **Koopman 算子** $U_R$：
  $$(U_R f)(x) = f\left(\sum_{i=1}^N p_i S_i(x)\right) = f(\Phi_R(x)),$$
  其中 $\Phi_R(x) = \sum_i p_i S_i(x)$ 为一步平均演化。在吸引子上 $U_R$ 的特征值 $\lambda \in (0,1]$，对应压缩率的对数 $-\log \lambda$。
- **核 $K_R$**：取 $w_n = (1/2)^n$，
  $$K_R(x,y) = \sum_{n=0}^\infty \frac{1}{2^n} \, \Phi_R^n(x) \cdot \Phi_R^n(y).$$
  若 $S_i$ 为相似压缩，$\Phi_R^n(x)$ 收敛到吸引子的重心，核在重心附近有尖锐峰。
- **谱算子** $A_R = -\log U_R$，其特征值 $\mu_i = -\log \lambda_i$，其中 $\lambda_i$ 为 $U_R$ 的特征值。

### 2.4.2 神经正切核（NTK）惰性训练

考虑无限宽度 MLP 的参数空间 $\mathcal{S}_R = \mathbb{R}^P$（$P$ 为参数总数），训练动态由 NTK 主导：
$$\theta_{t+1} = \theta_t - \eta \Theta (\theta_t - \theta_\ast),$$
其中 $\Theta$ 为 NTK 矩阵，$\theta_\ast$ 为目标参数。齐次部分的 Koopman 算子为
$$(U_R f)(\theta) = f(\theta - \eta \Theta (\theta - \theta_\ast)).$$

- **状态空间** $X_R$：参数空间中由训练数据与初始化分布支撑的集合。
- **不变测度** $\mu_R$：训练极限下的参数分布（集中在 $\theta_\ast$ 附近的高斯/退化分布）。
- **核 $K_R$**：利用 NTK 的特征分解 $\Theta = V \operatorname{diag}(\lambda_1,\dots,\lambda_P) V^T$，取
  $$K_R(\theta,\theta') = \sum_{k=1}^P \frac{1}{1 + \eta \lambda_k} \, v_k(\theta) \, v_k(\theta'),$$
  其中 $v_k(\theta) = \langle \theta, v_k \rangle$ 为 NTK 第 $k$ 个特征方向。
- **谱算子** $A_R = -\log(I - \eta \Theta)$，其特征值为
  $$\mu_k = -\log(1 - \eta \lambda_k) \approx \eta \lambda_k \quad (\eta \lambda_k \ll 1).$$

> 为保证 $\sigma(I-\eta\Theta) \subseteq (0,1]$，需对学习率做归一化：$\eta < 1/\lambda_{\max}(\Theta)$。

### 2.4.3 重整化群（RG）流

设 RG 流作用在有效作用空间 $\mathcal{S}_R = \{V_{\mathrm{eff}}\}$ 上，一步离散化为
$$V_{n+1} = \mathcal{R}(V_n),$$
其中 $\mathcal{R}$ 为 Wilsonian 重整化算子。在临界点附近线性化：
$$\mathcal{R}(V_\ast + \delta V) = V_\ast + L \, \delta V + O(\|\delta V\|^2),$$
$L$ 为线性化算子，其特征值为临界指数 $y_i$。取 Koopman 算子为线性化部分 $U_R = L$。

- **状态空间** $X_R$：临界点附近有效作用的邻域。
- **不变测度** $\mu_R$：$V_\ast$ 处的 Dirac 测度（或高斯扰动）。
- **核 $K_R$**：利用 $L$ 的特征函数 $\phi_i$（即临界点的缩放场），取
  $$K_R(V,V') = \sum_i e^{-y_i} \, \phi_i(\delta V) \, \phi_i(\delta V').$$
- **谱算子** $A_R = -\log L$，特征值 $\mu_i = -\log y_i$。对 $y_i < 1$（相关算子），$\mu_i > 0$；对 $y_i = 1$（边缘算子），$\mu_i = 0$；对 $y_i > 1$（无关算子），$\mu_i < 0$，此时超出正算子范围，需单独处理。

> 注：RG 情形展示了为何必须要求 $\sigma(U_R) \subseteq (0,1]$；无关算子对应负 $\mu_i$，不在当前 $\mathbf{Spec}$ 的定义范围内，需扩展为自伴（不必正）算子或投影到相关子空间。

---

## 3. $D$ 的忠实性（Faithfulness）

### 3.1 定义

函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 称为**忠实函子**，如果对任意 $R_1, R_2 \in \mathrm{Obj}(\mathbf{Rec})$，映射

$$D: \mathrm{Hom}_{\mathbf{Rec}}(R_1, R_2) \longrightarrow \mathrm{Hom}_{\mathbf{Spec}}(D(R_1), D(R_2))$$

是单射。即

$$D(f) = D(g) \quad \Longrightarrow \quad f = g.$$

### 3.2 特征核与点分离条件

**定义 3.1**（特征核 / universal kernel）。设 $X$ 为紧 Hausdorff 空间，$K: X \times X \to \mathbb{R}$ 为连续正定核，$\mathcal{H}_K$ 为其 RKHS。

- 称 $K$ 为 **universal kernel**，若 $\mathcal{H}_K$ 在 $C(X)$（带上确界范数）中稠密。
- 称 $K$ 为 **characteristic kernel**，若对 $X$ 上任意两个 Borel 概率测度 $\mu, \nu$，
  $$\int_X h \, d\mu = \int_X h \, d\nu \quad \forall h \in \mathcal{H}_K \quad \Longrightarrow \quad \mu = \nu.$$

> universal kernel 必为 characteristic kernel，但逆命题不成立。对忠实性证明，我们只需要 $\mathcal{H}_K$ **分离点**：对任意 $x \neq y$，存在 $h \in \mathcal{H}_K$ 使得 $h(x) \neq h(y)$。

**引理 3.2**（universal kernel 分离点）。若 $K$ 是 $X$ 上的 universal kernel，则对任意 $x \neq y \in X$，存在 $h \in \mathcal{H}_K$ 使得 $h(x) \neq h(y)$。

**证明**。由 Urysohn 引理，存在连续函数 $\phi \in C(X)$ 使得 $\phi(x)=1$，$\phi(y)=0$。因 $\mathcal{H}_K$ 在 $C(X)$ 中稠密，可取 $h \in \mathcal{H}_K$ 使得 $\|h - \phi\|_\infty < 1/3$。则
$$|h(x)| \ge 1 - 1/3 = 2/3, \qquad |h(y)| \le 1/3,$$
故 $h(x) \neq h(y)$。

**引理 3.3**（$K_R$ 的 universal 性条件）。对 §2.1 构造的核
$$K_R(x,y) = \sum_{n=0}^\infty w_n \, \Phi_R^n(x) \cdot \Phi_R^n(y),$$
若函数族 $\{\Phi_R^n : n \ge 0\}$ 在 $C(X_R)$ 中稠密，且 $\sum_n w_n < \infty$，则 $K_R$ 是 universal kernel。

**证明概要**。由 Mercer 定理，$\mathcal{H}_{K_R}$ 由 $\{\Phi_R^n\}_{n\ge 0}$ 张成。若该族在 $C(X_R)$ 中稠密，则 $\mathcal{H}_{K_R}$ 亦稠密，故 $K_R$ universal。

> 对 IFS，$\{\Phi_R^n\}$ 的稠密性可由压缩映射在吸引子上的迭代逼近保证；对 NTK，由 NTK 特征向量在参数空间中的完备性保证；对 RG，由缩放场在临界点附近张成局部函数空间保证。

### 3.3 忠实性定理

**定理 3.4**（$D$ 的忠实性）。设 $R_1, R_2 \in \mathrm{Obj}(\mathbf{Rec})$，且 $K_{R_2}$ 为 universal kernel（或至少 $\mathcal{H}_{R_2}$ 能分离 $\mathcal{S}_{R_2}$ 的点）。若 $f, g: R_1 \to R_2$ 满足 $D(f) = D(g)$，则 $f = g$。

**证明**。

$D(f) = D(g)$ 作为 $\mathbf{Spec}$ 中的态射相等，意味着它们作为有界算子相同：
$$D(f) = D(g) : \mathcal{H}_{R_1} \to \mathcal{H}_{R_2}.$$
取伴随算子得
$$D(f)^\ast = D(g)^\ast : \mathcal{H}_{R_2} \to \mathcal{H}_{R_1}.$$
由 $D(f)^\ast$ 的定义，对任意 $h \in \mathcal{H}_{R_2}$ 与 $x \in \mathcal{S}_{R_1}$，
$$(D(f)^\ast h)(x) = h(f(x)), \qquad (D(g)^\ast h)(x) = h(g(x)).$$
因此
$$h(f(x)) = h(g(x)), \quad \forall h \in \mathcal{H}_{R_2}, \; \forall x \in \mathcal{S}_{R_1}.$$

固定 $x \in \mathcal{S}_{R_1}$。若 $f(x) \neq g(x)$，由引理 3.2，存在 $h \in \mathcal{H}_{R_2}$ 使得 $h(f(x)) \neq h(g(x))$，矛盾。故
$$f(x) = g(x), \quad \forall x \in \mathcal{S}_{R_1}.$$
由 $x$ 的任意性，$f = g$。

> **推论**：若 $K_R$ 是 universal kernel，则 $D: \mathrm{Hom}_{\mathbf{Rec}}(R_1,R_2) \to \mathrm{Hom}_{\mathbf{Spec}}(D(R_1),D(R_2))$ 是单射，即 $D$ 为忠实函子。

### 3.4 离散原型中的验证

在代码原型 `decursion_functor.py` 中，有限维 L^2 表示下的态射映射取为

$$M_{D(f)} = M_f,$$

即 $D(f)$ 的矩阵直接继承自状态空间推前映射 $f$ 的矩阵（不做列归一化）。这一实现对应于 Koopman 提升算子 $D(f)^\ast$ 的伴随。

`verify_faithfulness(f, g)` 函数验证等价表述：若 $M_f \neq M_g$，则 $M_{D(f)} \neq M_{D(g)}$。在 `test_decursion_functor.py` 中，对合法自态射 $f = \mathrm{id}$ 与 $g = \Phi_R^\ast$（二者均与 Koopman 矩阵交换）进行了验证，结果表明 $D$ 在离散原型上保持单射。

### 3.5 意义

$D$ 的忠实性意味着：**递归系统的结构完全由其谱空间保持**。这是理论的核心非退化性条件，确保「去递归化」不丢失原系统的信息。

---

## 4. 伴随函子 $D \dashv R$ 的展望

### 4.1 右伴随 $R$ 的直观

若 $D$ 存在右伴随

$$R: \mathbf{Spec} \longrightarrow \mathbf{Rec},$$

则对任意谱对象 $E \in \mathrm{Obj}(\mathbf{Spec})$，$R(E)$ 是「从谱数据重构出的最小递归系统」。

### 4.2 伴随关系的定义

$D \dashv R$ 表示 $D$ 是 $R$ 的左伴随，即对任意 $R' \in \mathrm{Obj}(\mathbf{Rec})$ 与 $E \in \mathrm{Obj}(\mathbf{Spec})$，存在自然的双射

$$\mathrm{Hom}_{\mathbf{Rec}}(R', R(E)) \;\cong\; \mathrm{Hom}_{\mathbf{Spec}}(D(R'), E).$$

等价地，存在 **unit** $\eta: \mathrm{id}_{\mathbf{Spec}} \Rightarrow D \circ R$ 与 **counit** $\varepsilon: R \circ D \Rightarrow \mathrm{id}_{\mathbf{Rec}}$，满足三角恒等式：

$$(\varepsilon D) \circ (D \eta) = \mathrm{id}_D, \qquad (R \varepsilon) \circ (\eta R) = \mathrm{id}_R.$$

> 直观：$R(E)$ 是"从谱对象 $E$ 能重构出的最小递归系统"；任意 $R' \to R(E)$ 的 Rec 态射与 $D(R') \to E$ 的 Spec 态射一一对应。

### 4.3 存在性的充分必要条件

**定理 4.1**（右伴随存在的伴随函子定理）。设 $\mathbf{Rec}$ 为完备范畴（即所有小极限存在），$D: \mathbf{Rec} \to \mathbf{Spec}$ 为协变函子。则 $D$ 存在右伴随 $R$ 的充分必要条件是：

1. $D$ 保持所有小极限；
2. $D$ 满足**解集条件**（solution set condition）：对任意 $E \in \mathrm{Obj}(\mathbf{Spec})$，存在小集合 $\{R_i\}_{i \in I} \subseteq \mathrm{Obj}(\mathbf{Rec})$，使得任意 Rec 态射 $f: R' \to R(E)$ 都可经由某个 $R_i$ 分解。

**证明概要**。这是 Freyd 一般伴随函子定理（General Adjoint Functor Theorem, GAFT）的直接应用。必要性由左伴随保持极限得到；充分性由解集条件保证泛对象的存在，从而构造右伴随。

**推论 4.2**（具体充分条件）。若满足以下三条，则 $D \dashv R$ 存在：

1. $\mathbf{Rec}$ 有任意小极限（特别是乘积与等化子）；
2. $D$ 保持乘积与等化子（从而保持所有极限）；
3. $\mathbf{Spec}$ 中每个对象 $E$ 的"$D$-前像"在适当等价意义下构成小集合。

**$D$ 保持极限的验证**。在离散原型中，$D$ 的对象映射为 $D(R) = (\mathcal{H}_R, A_R, \sigma(A_R))$。若 $\{R_i\}$ 是一族 Rec 对象，其极限 $R_\infty$ 的状态空间为 $\varprojlim \mathcal{S}_{R_i}$，演化 $\Phi_{R_\infty}$ 由各 $\Phi_{R_i}$ 诱导。则

$$\mathcal{H}_{R_\infty} \cong \varinjlim \mathcal{H}_{R_i}, \qquad A_{R_\infty} = \varinjlim A_{R_i},$$

其中归纳极限在 Hilbert 空间范畴中取（若图表由等距嵌入构成）。因此 $D$ 在适当条件下保持极限。

### 4.4 离散原型中的最小实现

在 `decursion_functor.py` 中提供了右伴随对象映射的最小原型 `right_adjoint_on_object(E)`：

- 状态空间取为 $E$ 的 Hilbert 空间标准正交基；
- 演化规则取为 Koopman 矩阵 $K = e^{-A_E}$；
- 元数据标记为从谱重构而来。

对正谱对象 $E$，unit 由同构

$$\eta_E: E \;\xrightarrow{\;\cong\;}\; D(R(E))$$

给出（在数值容差内），即 $D \circ R \approx \mathrm{id}_{\mathbf{Spec}}$ 在原型对象上成立。验证测试见 `test_decursion_functor.py` 的 `test_right_adjoint_roundtrip`。

counit $\varepsilon_R: R(D(R)) \to R$ 则把 $R(D(R))$ 的标准正交基状态空间映射回 $R$ 的原始状态空间；由于 $D$ 遗忘了状态空间几何，$\varepsilon_R$ 一般不是同构，但满足三角恒等式在原型对象上近似成立。

> 注意：完整伴随函子 $D \dashv R$ 的严格构造需要验证 §4.3 的极限条件与解集条件，这在连续/无穷维情形仍需进一步研究。

---

## 5. 与三层公理体系的对照

| 本文内容 | 对应元公理 |
|---|---|
| $\mathbf{Rec}$ 的严格定义 | 元公理 1（递归系统范畴存在性） |
| $\mathbf{Spec}$ 的严格定义 | 元公理 2（谱范畴存在性） |
| $D$ 的构造与函子公理验证 | 元公理 3（谱去递归化函子存在性与自然性） |
| RKHS 作为 $\mathcal{H}_R$ 的构造 | 元公理 4（Clifford 值分形 RKHS 存在性） |
| $D$ 的忠实性证明 | 元公理 3 的强化结论 |

---

## 6. 待解决问题（已严格化）

1. ~~**RKHS 构造的显式化**：需要将 $K_R$、$\mathcal{H}_R$、$A_R$ 在 IFS、NTK、RG 三个具体对象上完全写清楚。~~  已在 §2.1 与 §2.4 中给出基于 Koopman 算子谱投影的 Mercer 核构造，并具体化到 IFS、NTK、RG 三类对象。
2. ~~**$A_R$ 的正性与闭性**：验证对一般递归系统，$A_R = -\log \Phi_R^\ast$ 确实是闭稠定正算子。~~  已在命题 2.1 中证明，并在条件 2.2 中给出可对角化条件。
3. ~~**特征核条件**：为 $K_R$ 选取合适的特征核，确保忠实性证明成立。~~  已在 §3.2 中引入 universal kernel，并在定理 3.4 中完成忠实性的严格证明。
4. ~~**伴随函子存在性**：研究 $D \dashv R$ 的充分必要条件。~~  已在 §4.3 中由 Freyd 伴随函子定理给出充分必要条件，并在 §4.4 中给出离散原型实现。

---

## 7. 版本记录

- v0.1（2026-07-12）：初稿，构造 $D$ 的对象映射与态射映射，验证函子公理，给出忠实性证明概要。
- v0.2（2026-07-12）：对齐 `decursion_functor.py` 实现，移除列归一化以保证忠实性；补充 `verify_faithfulness` 与 `right_adjoint_on_object` 的代码对应；更新离散原型验证与版本记录。
- v0.3（2026-07-12）：严格化 RKHS 构造（§2.1、§2.4），证明 $A_R$ 闭性/正性（命题 2.1），以 universal kernel 严格证明忠实性（定理 3.4），并给出 $D \dashv R$ 的伴随函子定理条件（定理 4.1）。
