# 递归系统范畴 $\mathbf{Rec}$ 与谱范畴 $\mathbf{Spec}$ 的严格定义

> 本文档是「通用不动点范畴框架」奠基期的第一项交付物。目标是为三层公理体系中的元公理 1–2 提供严格、可操作的数学定义，并为后续函子 $D: \mathbf{Rec} \to \mathbf{Spec}$ 的建立奠定基础。

---

## 1. 设计目标

我们希望构造两个范畴：

1. **递归系统范畴 $\mathbf{Rec}$**：其对象是各种递归/自相似系统（IFS、神经网络训练、重整化群流、拓扑递归等），其态射是这些系统之间的结构保持映射。
2. **谱范畴 $\mathbf{Spec}$**：其对象是 Hilbert/赋范空间上的线性算子及其谱，其态射是保持谱结构的线性映射。

然后建立**谱去递归化函子** $D: \mathbf{Rec} \to \mathbf{Spec}$，将「递归迭代」映射为「算子半群指数演化」，从而实现理论的「去递归」核心范式。

---

## 2. 递归系统范畴 $\mathbf{Rec}$

### 2.1 对象

一个**递归系统** $R$ 是一个四元组

$$R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R),$$

其中：

- $\mathcal{S}_R$：状态空间，一个可分的完备度量空间（通常是 Polish 空间）。
- $\Phi_R: \mathcal{S}_R \to \mathcal{S}_R$：自相似演化映射，描述系统的一步演化规则。
- $\mathcal{T}_R \subseteq \mathbb{R}_{\ge 0}$：时间半群，通常为 $\mathbb{N}$（离散）或 $\mathbb{R}_{\ge 0}$（连续）。
- $\mathcal{M}_R$：附加结构集合（例如 IFS 的压缩映射族、神经网络的架构参数、RG 的能标截断等）。附加结构仅用于区分不同类型的递归系统，不影响范畴的基本构造。

> **直观例子**：
> - IFS：$\mathcal{S}_R = \mathbb{R}^d$，$\Phi_R(x) = \bigcup_{i=1}^N S_i(x)$，$\mathcal{M}_R = \{S_i\}_{i=1}^N$。
> - 神经网络训练：$\mathcal{S}_R = \mathbb{R}^{\#参数}$，$\Phi_R$ 为梯度下降一步更新，$\mathcal{M}_R = \{网络结构, 学习率, 损失函数\}$。

### 2.2 态射

设 $R_1, R_2 \in \mathrm{Obj}(\mathbf{Rec})$，一个**态射** $f: R_1 \to R_2$ 是一个连续映射

$$f: \mathcal{S}_{R_1} \longrightarrow \mathcal{S}_{R_2},$$

满足以下交换图：

```
S_{R_1} --Φ_{R_1}--> S_{R_1}
   | f                    | f
   v                      v
S_{R_2} --Φ_{R_2}--> S_{R_2}
```

即

$$\Phi_{R_2} \circ f = f \circ \Phi_{R_1}.$$

> **物理意义**：$f$ 是 $R_1$ 到 $R_2$ 的嵌入或模拟映射，保持一步演化规则。

### 2.3 态射的复合

设 $f: R_1 \to R_2$，$g: R_2 \to R_3$。在范畴论中，复合 $g \circ f$ 有定义的**先决条件**是目标对象与源对象严格相等：

$$\mathrm{target}(f) = R_2 = \mathrm{source}(g).$$

在满足该条件后，定义复合 $g \circ f: R_1 \to R_3$ 为状态空间映射的通常复合：

$$(g \circ f)(x) = g(f(x)), \quad \forall x \in \mathcal{S}_{R_1}.$$

**验证复合保持演化规则**：

$$\Phi_{R_3} \circ (g \circ f) = (\Phi_{R_3} \circ g) \circ f = (g \circ \Phi_{R_2}) \circ f = g \circ (\Phi_{R_2} \circ f) = g \circ (f \circ \Phi_{R_1}) = (g \circ f) \circ \Phi_{R_1}.$$

因此 $g \circ f \in \mathrm{Hom}(R_1, R_3)$。

### 2.4 单位态射

对每个 $R \in \mathrm{Obj}(\mathbf{Rec})$，单位态射

$$\mathrm{id}_R: R \to R$$

取为状态空间上的恒等映射 $\mathrm{id}_{\mathcal{S}_R}$。显然满足

$$\Phi_R \circ \mathrm{id}_R = \mathrm{id}_R \circ \Phi_R.$$

### 2.5 范畴公理验证

- **结合律**：由状态空间映射复合的结合律保证。
- **单位律**：对任意 $f: R_1 \to R_2$，
  $$f \circ \mathrm{id}_{R_1} = f = \mathrm{id}_{R_2} \circ f.$$

因此 $(\mathbf{Rec}, \circ, \mathrm{id})$ 构成一个范畴。

### 2.6 压缩态射子范畴

我们将在结构定理层使用压缩条件。定义**压缩态射** $S: R \to R$ 为满足

$$d(\Phi_R(S(x)), \Phi_R(S(y))) \le c \, d(x,y), \quad c < 1, \quad \forall x,y \in \mathcal{S}_R$$

的自态射。所有压缩态射构成 $\mathbf{Rec}$ 的一个宽子范畴（wide subcategory）。

> 注：此条件后续用于证明 Hutchinson 型不动点对象的存在唯一性。

### 2.7 与代码实现的对应：有限维离散情形

在代码原型 `rec_category.py` 中，递归系统 $R$ 被离散化为有限状态空间 $X_R = \{x_1, \dots, x_n\}$。态射 $f: R_1 \to R_2$ 表示为一个矩阵

$$M_f \in \mathbb{R}^{n_2 \times n_1},$$

其中 $(M_f)_{ij}$ 表示 $x_j^{(1)}$ 被映射到 $x_i^{(2)}$ 的权重。

**复合律的矩阵实现**：

设 $f: R_1 \to R_2$，$g: R_2 \to R_3$，则复合 $g \circ f: R_1 \to R_3$ 的矩阵为矩阵乘积

$$M_{g \circ f} = M_g \cdot M_f \in \mathbb{R}^{n_3 \times n_1}.$$

**单位态射的矩阵实现**：

对象 $R$ 上的单位态射 $\mathrm{id}_R$ 对应单位矩阵 $I_n \in \mathbb{R}^{n \times n}$。

**范畴公理的矩阵验证**：

1. **结合律**：对任意可复合的三元组 $f, g, h$，
   $$M_{h \circ (g \circ f)} = M_h (M_g M_f) = (M_h M_g) M_f = M_{(h \circ g) \circ f},$$
   由矩阵乘法的结合律保证。

2. **单位律**：对任意 $f: R_1 \to R_2$，
   $$M_{f \circ \mathrm{id}_{R_1}} = M_f \cdot I_{n_1} = M_f = I_{n_2} \cdot M_f = M_{\mathrm{id}_{R_2} \circ f}.$$

3. **复合的存在条件**：$g \circ f$ 有定义当且仅当 $f$ 的目标对象与 $g$ 的源对象相等。在离散实现中，对象相等要求两个实例的**状态空间**与**演化规则**均一致（在数值容差内）：
   $$n_{R_2} = n_{R_2'}, \quad X_{R_2} = X_{R_2'}, \quad \Phi_{R_2} = \Phi_{R_2'}.$$
   仅状态空间维数相同或采样点相同，不足以保证对象相等；不同的演化规则定义不同的 Rec 对象。

---

## 3. 谱范畴 $\mathbf{Spec}$

### 3.1 对象

一个**谱对象** $E$ 是一个三元组

$$E = (\mathcal{H}_E, A_E, \sigma_E),$$

其中：

- $\mathcal{H}_E$：一个复（或 Clifford 值）Hilbert 空间。
- $A_E: \mathcal{D}(A_E) \subseteq \mathcal{H}_E \to \mathcal{H}_E$：一个闭稠定正算子，称为谱算子。
- $\sigma_E \subseteq \mathbb{C}$：$A_E$ 的谱。对正算子，$\sigma_E \subseteq \mathbb{R}_{\ge 0}$。

> **与分形谱去递归理论的关联**：$A_E$ 是算子半群 $e^{-t A_E}$ 的生成元，其离散谱 $ \lambda_i = e^{-\mu_i}$ 对应递归系统的分形谱。

### 3.2 态射

设 $E_1 = (\mathcal{H}_1, A_1, \sigma_1)$，$E_2 = (\mathcal{H}_2, A_2, \sigma_2) \in \mathrm{Obj}(\mathbf{Spec})$，一个**态射** $T: E_1 \to E_2$ 是一个有界线性算子

$$T: \mathcal{H}_1 \longrightarrow \mathcal{H}_2,$$

满足**谱交织条件**

$$T A_1 \subseteq A_2 T,$$

即对任意 $u \in \mathcal{D}(A_1)$，有 $T u \in \mathcal{D}(A_2)$ 且

$$T A_1 u = A_2 T u.$$

> **物理意义**：$T$ 将 $E_1$ 的谱结构嵌入或投影到 $E_2$ 的谱结构中。

### 3.3 态射的复合

设 $T: E_1 \to E_2$，$U: E_2 \to E_3$ 为谱态射。在范畴论中，复合 $U \circ T$ 有定义的**先决条件**是目标对象与源对象严格相等：

$$\mathrm{target}(T) = E_2 = \mathrm{source}(U).$$

在满足该条件后，定义复合 $U \circ T: E_1 \to E_3$ 为有界线性算子的通常复合。

**验证谱交织条件**：

对 $u \in \mathcal{D}(A_1)$，

$$(U \circ T) A_1 u = U (T A_1 u) = U (A_2 T u) = A_3 U (T u) = A_3 (U \circ T) u.$$

因此 $U \circ T$ 满足谱交织条件。

### 3.4 单位态射

对每个 $E \in \mathrm{Obj}(\mathbf{Spec})$，单位态射

$$\mathrm{id}_E: E \to E$$

取为 $\mathcal{H}_E$ 上的恒等算子 $I_{\mathcal{H}_E}$。显然满足 $I A_E = A_E I$。

### 3.5 范畴公理验证

- **结合律**：有界线性算子复合的结合律。
- **单位律**：$T \circ I_{\mathcal{H}_1} = T = I_{\mathcal{H}_2} \circ T$。

因此 $(\mathbf{Spec}, \circ, \mathrm{id})$ 构成一个范畴。

### 3.6 谱映射的保持性

若 $T: E_1 \to E_2$ 是 $\mathbf{Spec}$ 中的同构（即 $T$ 可逆且 $T^{-1}$ 也满足谱交织条件），则 $A_1$ 与 $A_2$ 是**相似算子**，从而

$$\sigma_1 = \sigma_2.$$

更一般地，若 $T$ 是单射（或满射），则 $\sigma_1 \subseteq \sigma_2$（或 $\sigma_2 \subseteq \sigma_1$ 在适当条件下）。这一性质将在证明 $D$ 忠实性时用到。

### 3.7 与代码实现的对应：有限维离散情形

在代码原型 `spec_category.py` 中，谱对象 $E$ 被实现为有限维 Hilbert 空间上的三元组

$$E = (\mathcal{H}_E, A_E, \sigma_E), \quad \mathcal{H}_E \cong \mathbb{C}^n,$$

其中 $A_E \in \mathbb{C}^{n \times n}$ 是 Hermitian 正半定矩阵。

**态射的矩阵实现**：

态射 $T: E_1 \to E_2$ 表示为一个矩阵

$$M_T \in \mathbb{C}^{n_2 \times n_1},$$

满足强谱交织条件

$$M_T A_1 = A_2 M_T.$$

**复合律的矩阵实现**：

设 $T: E_1 \to E_2$，$U: E_2 \to E_3$，则复合 $U \circ T: E_1 \to E_3$ 的矩阵为

$$M_{U \circ T} = M_U \cdot M_T \in \mathbb{C}^{n_3 \times n_1}.$$

**验证强交织条件的矩阵形式**：

$$(M_U M_T) A_1 = M_U (M_T A_1) = M_U (A_2 M_T) = (M_U A_2) M_T = (A_3 M_U) M_T = A_3 (M_U M_T).$$

**单位态射的矩阵实现**：

对象 $E$ 上的单位态射 $\mathrm{id}_E$ 对应单位矩阵 $I_n \in \mathbb{C}^{n \times n}$，显然满足 $I_n A_E = A_E I_n$。

**范畴公理的矩阵验证**：

1. **结合律**：由矩阵乘法结合律保证。
2. **单位律**：$M_T I_{n_1} = M_T = I_{n_2} M_T$。
3. **复合的存在条件**：$U \circ T$ 有定义当且仅当 $T$ 的目标对象与 $U$ 的源对象相等。在离散实现中，对象相等要求两个实例的**Hilbert 空间维数**与**谱算子**均一致（在数值容差内）：
   $$n_2 = n_2', \quad A_{E_2} = A_{E_2'}.$$
   仅维数相同不足以保证对象相等；不同的谱算子定义不同的 Spec 对象。

---

## 4. 两个范畴的关系初探

我们期望构造函子

$$D: \mathbf{Rec} \longrightarrow \mathbf{Spec},$$

使得对任意递归系统 $R$，$D(R)$ 是其「去递归化」后的谱对象。具体地：

- $D(R) = (\mathcal{H}_R, A_R, \sigma(A_R))$
- 对态射 $f: R_1 \to R_2$，$D(f): D(R_1) \to D(R_2)$ 是满足谱交织条件的有界线性算子。

下一步（`roadmap/phase1_meta_axioms.md`）将严格定义 $D$ 并证明：

1. $D$ 是协变函子；
2. $D$ 保持单位态射与复合；
3. 在适当条件下，$D$ 是忠实函子。

---

## 5. 待澄清问题与处理优先级

### P0：工作假设规范（已确定，可直接用于代码实现）

以下三个问题已在第二阶段开始前给出明确工作假设。这些假设不影响理论最终正确性，但为代码原型提供唯一、可执行的设计约束。

---

#### 假设 1：$\mathcal{H}_R$ 的构造 —— 有限采样 + 离散 RKHS 逼近

**问题**：对每个递归系统 $R$，如何从 $\mathcal{S}_R$ 自然构造 Hilbert 空间？

**工作假设**：

1. 在代码原型中，每个递归系统 $R$ 的状态空间 $\mathcal{S}_R$ 先取为**有限采样点集**
   $$X_R = \{x_1, x_2, \dots, x_n\} \subset \mathcal{S}_R.$$
   对连续/分形系统，$X_R$ 是递归不变集上的一个有限样本或轨道截断。

2. 在 $X_R$ 上定义离散测度 $\mu_R$（通常为均匀测度 $\mu_R(x_i) = 1/n$，或由压缩权重诱导的非均匀测度）。

3. Hilbert 空间取为有限维 $L^2$ 空间
   $$\mathcal{H}_R := L^2(X_R, \mu_R) \cong \mathbb{C}^n$$
   配备标准内积
   $$\langle f, g \rangle_{\mathcal{H}_R} = \sum_{i=1}^n \overline{f(x_i)} g(x_i) \mu_R(x_i).$$

4. 对 Clifford 值情形，将 $\mathbb{C}^n$ 替换为 Clifford 值函数空间
   $$\mathcal{H}_R^{\mathcal{Cl}} := \{f: X_R \to \mathcal{Cl}(p,q)\},$$
   内积取值于 $\mathcal{Cl}(p,q)$，在原型中先退化为逐分量的复内积。

5. 嵌入映射 $i_R: X_R \hookrightarrow \mathcal{H}_R$ 定义为点求值泛函的 Riesz 表示：
   $$i_R(x_i) = e_i,$$
   其中 $e_i$ 为 $\mathcal{H}_R$ 的标准正交基（对应 $X_R$ 中第 $i$ 个点）。

**代码实现约束**：
- `spec_category.py` 中 `SpectralObject` 的 `hilbert_space` 字段为 `numpy.ndarray` 或 `scipy.sparse` 矩阵。
- 状态空间维度 `n` 作为构造参数传入。
- 测度 `mu` 默认为均匀分布，允许通过 `weights` 参数覆盖。

**边界条件**：
- 当 $n \to \infty$ 时，有限维 $L^2(X_R, \mu_R)$ 在适当条件下逼近连续 RKHS。原型阶段不处理极限过程。

---

#### 假设 2：$A_R$ 的符号 —— 先限制为正算子

**问题**：$A_R$ 是否总是正算子？

**工作假设**：

1. 在代码原型中，**$A_R$ 必须是有限维 Hermitian 正半定矩阵**（或实对称正半定矩阵）。

2. $A_R$ 通过 Koopman 算子 $\Phi_R^\ast$ 定义：
   $$A_R = -\log \Phi_R^\ast,$$
   其中 $\Phi_R^\ast$ 是作用在 $\mathcal{H}_R$ 上的压缩/随机转移矩阵，其特征值满足 $0 < \lambda_i \le 1$。

3. 为保证 $A_R$ 良定义且正半定，要求：
   - $\Phi_R^\ast$ 可对角化；
   - 所有特征值 $\lambda_i \in (0, 1]$；
   - 对 $\lambda_i = 0$ 或负特征值的情形，原型阶段报错或截断。

4. 对振荡型 RG 流等更一般系统，**不在第二阶段处理**。后续可通过允许 $A_R$ 为自伴（不一定正）或正规矩阵来扩展。

**代码实现约束**：
- `spec_category.py` 中实现 `PositiveSpectralObject` 类。
- 构造时检查 $A_R$ 是否为 Hermitian 正半定（数值容差 `tol=1e-10`）。
- 提供 `from_koopman(koopman_matrix)` 类方法，自动计算 $A_R = -\log(\text{koopman_matrix})$。

**边界条件**：
- 若 $\Phi_R^\ast$ 不可对角化或存在 Jordan 块，原型阶段采用谱投影截断，仅保留可对角化部分。

---

#### 假设 3：谱交织条件的强弱 —— 先用强交织，预留弱交织接口

**问题**：当前定义 $T A_1 = A_2 T$ 是否过强？

**工作假设**：

1. 原型阶段**强制使用强交织条件**：$\mathbf{Spec}$ 中的态射 $T: E_1 \to E_2$ 必须满足
   $$T A_1 = A_2 T$$
   作为矩阵等式（在有限维情形下）。

2. 强交织的验证算法：对给定的矩阵 $T$、$A_1$、$A_2$，计算
   $$\mathrm{residual} = \|T A_1 - A_2 T\|_F$$
   若 residual 小于阈值 `tol`，则判定 $T$ 为合法态射。

3. 预留弱交织扩展接口：后续可引入 `"weak"` 模式，仅要求 $T$ 保持谱测度或谱投影，例如
   $$T P_1(\Delta) = P_2(\Delta) T, \quad \forall \text{ Borel 集 } \Delta,$$
   其中 $P_i$ 为 $A_i$ 的谱测度。原型阶段不实现，但代码接口保留 `intertwining="strict"` 参数。

**代码实现约束**：
- `spec_category.py` 中 `is_morphism(T, source, target, mode="strict", tol=1e-10)` 函数。
- 默认 `mode="strict"`。
- 强交织下，若 $T$ 不是单射，允许其像为 $E_2$ 的约化子空间。

**边界条件**：
- 当 $\dim E_1 \neq \dim E_2$ 时，$T$ 为矩形矩阵。强交织条件仍按矩阵等式验证，不要求 $T$ 可逆。

---

#### 假设综合：代码原型中的最小对象定义

基于上述三个假设，第二阶段代码原型中的核心数据结构如下：

```python
# rec_category.py
@dataclass
class RecObject:
    state_space: np.ndarray      # 有限采样点集 X_R，形状 (n, d)
    evolution: Callable          # Φ_R: X_R -> X_R，或转移矩阵
    time_semigroup: str = "N"    # "N" 或 "R+"
    metadata: dict = field(default_factory=dict)

@dataclass
class RecMorphism:
    source: RecObject
    target: RecObject
    map: np.ndarray              # f: X_{R1} -> X_{R2}，可为索引映射或插值矩阵

# spec_category.py
@dataclass
class PositiveSpectralObject:
    hilbert_space_basis: np.ndarray  # 标准正交基，形状 (n, n)
    operator_A: np.ndarray           # Hermitian 正半定矩阵，形状 (n, n)
    spectrum: np.ndarray             # σ(A_R)

@dataclass
class SpectralMorphism:
    source: PositiveSpectralObject
    target: PositiveSpectralObject
    matrix: np.ndarray               # T: H_1 -> H_2
    intertwining_mode: str = "strict"
```

**下一步**：基于以上假设，可立即开始实现 `rec_category.py` 与 `spec_category.py`。

### P1：可延至后续阶段解决

这些问题主要影响理论的严格性与证明表述，不影响最小可运行原型。

#### 4. 同构标准（已严格化）

**$\mathbf{Rec}$ 中的同构**。设 $f: R_1 \to R_2$ 为 $\mathbf{Rec}$ 中的态射。称 $f$ 为**同构**，若 $f: \mathcal{S}_{R_1} \to \mathcal{S}_{R_2}$ 是同胚（homeomorphism），且其逆映射 $f^{-1}: \mathcal{S}_{R_2} \to \mathcal{S}_{R_1}$ 也是 $\mathbf{Rec}$ 中的态射（即满足 $\Phi_{R_1} \circ f^{-1} = f^{-1} \circ \Phi_{R_2}$）。

> 注：若 $\mathcal{S}_{R_1}, \mathcal{S}_{R_2}$ 仅为度量空间而非拓扑空间，可退化为双射且双向连续的映射；在离散原型中，同构对应状态空间点之间的一一对应（置换矩阵）。

**$\mathbf{Spec}$ 中的同构**。设 $T: E_1 \to E_2$ 为 $\mathbf{Spec}$ 中的态射。称 $T$ 为**同构**，若 $T: \mathcal{H}_1 \to \mathcal{H}_2$ 是有界可逆线性算子，且其逆 $T^{-1}$ 也满足谱交织条件（即 $T^{-1} A_2 \subseteq A_1 T^{-1}$）。

> 强标准：若进一步要求 $T$ 为**酉算子**（$T^\ast T = I_{\mathcal{H}_1}$，$T T^\ast = I_{\mathcal{H}_2}$），则 $A_1$ 与 $A_2$ 酉等价，谱完全相同（包括重数）。强标准适用于需要保持 Hilbert 空间几何的情形。
> 
> 弱标准：仅要求 $T$ 有界可逆，则 $A_1$ 与 $A_2$ 相似，谱作为集合相同（重数可能因 Jordan 结构而不同）。

**与忠实性的关系**。在 phase1 的忠实性证明中，只需 $\mathcal{H}_{R_2}$ 能分离 $\mathcal{S}_{R_2}$ 的点，不要求 $f$ 为同胚或 $T$ 为酉算子。因此强同构标准不是忠实性的必要条件，而是保证 $D$ 把同构映为同构的充分条件。

**离散原型中的对应**。在 `rec_category.py` 中，Rec 同构对应可逆的置换/权重矩阵；在 `spec_category.py` 中，Spec 同构对应满足 $M_T A_1 = A_2 M_T$ 的可逆矩阵 $M_T$（强标准下为酉矩阵）。

---

## 6. 版本记录

- v0.1（2026-07-12）：初稿，定义 $\mathbf{Rec}$ 与 $\mathbf{Spec}$ 的对象、态射、复合与单位，提出待澄清问题。
- v0.2（2026-07-12）：严格化同构标准：Rec 同构要求同胚且逆为态射；Spec 同构要求有界可逆且逆满足谱交织，强标准下为酉算子。

---

## 7. 相关论文

本文档定义的 $\mathbf{Rec}$ 与 $\mathbf{Spec}$ 范畴是以下论文的范畴论基础：

- **Paper X**：`paper/paper10_spectral_quantum.md` — 在 $\mathbf{Spec}$ 范畴中建立了量子测量的 M1-M4 公理系统。其中 M1（谱投影公理）直接使用本文 §3 中 $\mathbf{Spec}$ 对象的投影态射结构；M2（谱流动力学公理）使用本文 §3.2 中态射的谱交织条件。详见 Paper X §2。
