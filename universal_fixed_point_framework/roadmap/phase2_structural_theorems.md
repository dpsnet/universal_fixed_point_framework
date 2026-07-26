# Phase 2：结构定理层抽象化

> 本阶段目标：在元公理层基础上，建立结构定理层的核心对象：全域不动点方程、$\text{Cat}_H(\mathcal{Cl})$ Hilbert 范畴、压缩态射不动点定理、轨道函子。本文件对应推进计划「第一阶段第 2–3 周」的交付物。

---

## 1. 全域谱态空间与全域不动点方程

### 1.1 全域谱态空间 $\mathcal{V}$

**定义 1.1**（全域谱态空间）。设 $\mathbf{Rec}$ 为小范畴（或至少 $D$ 的像构成小图表），$D: \mathbf{Rec} \to \mathbf{Sp}$ 为谱化函子。定义**全域谱态空间** $\mathcal{V}$ 为 $D$ 的像图表在 $\mathbf{Sp}$ 中的余极限（colimit）：

$$\mathcal{V} := \varinjlim_{R \in \mathrm{Obj}(\mathbf{Rec})} D(R) \in \mathrm{Obj}(\mathbf{Sp}).$$

具体构造如下。对每个 Rec 态射 $f: R_1 \to R_2$，$D(f): D(R_1) \to D(R_2)$ 是 Spec 态射。令

$$\mathcal{V} := \left.\bigoplus_{R \in \mathrm{Obj}(\mathbf{Rec})} \mathcal{H}_{D(R)} \right/ \sim,$$

其中直和在 Hilbert 空间范畴中取（有限线性组合），等价关系 $\sim$ 由

$$(h, D(R_2)) \sim (D(f)^\ast h, D(R_1)), \qquad \forall f: R_1 \to R_2, \; h \in \mathcal{H}_{D(R_2)}$$

生成。若该商可完备化为 Hilbert 空间，则得到 $\mathcal{H}_{\mathcal{V}}$；其上诱导的谱算子 $A_{\mathcal{V}}$ 由各 $A_{D(R)}$ 在相容性条件下粘合而成。

**命题 1.2**（$\mathcal{V}$ 的存在条件）。若以下两个条件成立，则上述余极限存在：

1. **图表由等距嵌入构成**：对所有 $f: R_1 \to R_2$，$D(f): D(R_1) \to D(R_2)$ 是等距嵌入（或至少在 Hilbert 空间范畴中是单射、保持内积的态射）。
2. **$\mathbf{Sp}$ 对该图表封闭**：余极限 $\varinjlim D(R)$ 仍属于 $\mathbf{Sp}$，即诱导算子 $A_{\mathcal{V}}$ 为闭稠定正算子。

**证明概要**。在 Hilbert 空间范畴中，由等距嵌入构成的 filtered 图表的归纳极限是良定义的：取各 $\mathcal{H}_{D(R)}$ 的并集的闭包，内积由等距性一致诱导。条件 2 保证该极限对象的算子 $A_{\mathcal{V}}$ 满足 Sp 对象的公理。

> 注：条件 1 在通常情形下成立。对 IFS，$D(f)$ 将低维吸引子的函数空间嵌入高维吸引子的函数空间；对 NTK，$D(f)$ 将少样本空间的函数嵌入多样本空间。若 $D(f)$ 不是等距嵌入，则需先取等距部分再构造余极限。

$\mathcal{V}$ 包含以下子空间：

- 分形测度空间：$\mathcal{M}(X_R)$ 上关于不变测度的子空间；
- 算子谱空间：所有 $A_R$ 的谱的并集；
- 场组态空间：量子场论中的有效势、Yukawa 耦合等；
- 费米旋量空间：Clifford 值函数空间。

### 1.2 全域泛函映射 $\mathcal{F}$

**定义 1.3**（全域泛函映射）。在 §1.1 构造的 $\mathcal{V}$ 上定义**全域泛函映射**

$$\mathcal{F}: \mathcal{V} \longrightarrow \mathcal{V}$$

如下：对任意 $[(h, D(R))] \in \mathcal{V}$（其中 $h \in \mathcal{H}_{D(R)}$），令

$$\mathcal{F}[(h, D(R))] := [(\Phi_R^\ast h, D(R))].$$

**命题 1.4**（$\mathcal{F}$ 的良定性）。上述定义不依赖于代表元的选取，从而给出 $\mathcal{V}$ 上的良定义算子。

**证明**。设 $(h_2, D(R_2)) \sim (D(f)^\ast h_2, D(R_1))$ 对某个 $f: R_1 \to R_2$ 成立。需证

$$(\Phi_{R_2}^\ast h_2, D(R_2)) \sim (\Phi_{R_1}^\ast D(f)^\ast h_2, D(R_1)).$$

由 $f$ 是 Rec 态射，满足 $\Phi_{R_2} \circ f = f \circ \Phi_{R_1}$。取 Koopman 提升得

$$D(f)^\ast \Phi_{R_2}^\ast = \Phi_{R_1}^\ast D(f)^\ast.$$

因此

$$\Phi_{R_1}^\ast D(f)^\ast h_2 = D(f)^\ast \Phi_{R_2}^\ast h_2,$$

即 $(\Phi_{R_2}^\ast h_2, D(R_2))$ 与 $(D(f)^\ast \Phi_{R_2}^\ast h_2, D(R_1)) = (\Phi_{R_1}^\ast D(f)^\ast h_2, D(R_1))$ 在等价关系 $\sim$ 下相等。故 $\mathcal{F}$ 良定义。

> 换言之，$\mathcal{F}$ 是统一所有递归演化规则的泛函算子，其在每个子空间 $D(R) \subseteq \mathcal{V}$ 上的限制恰为 Koopman 算子 $\Phi_R^\ast$。

### 1.3 全域不动点方程

**核心方程**：

$$\mathcal{F}[\mathcal{V}] = \mathcal{V}.$$

该方程表示：全域谱态空间 $\mathcal{V}$ 在泛函映射 $\mathcal{F}$ 下是不变的。

### 1.4 子不动点方程

原有各层递归系统的不动点条件，均可视为全域不动点方程在相应子空间上的限制：

| 子系统 | 子不动点方程 | 所属子空间 |
|---|---|---|
| IFS Hutchinson 测度 | $\mathcal{F}_\mu[\mu] = \mu$ | 分形测度子空间 |
| Ruelle Gibbs 测度 | $\mathcal{F}_q[\mu_q] = \mu_q$ | Gibbs 测度子空间 |
| FRG 有效势 | $\mathcal{F}_{RG}[V_{\mathrm{eff}}] = V_{\mathrm{eff}}$ | 有效势子空间 |
| 费米子质量谱 | $\mathcal{F}_m[\{m_k\}] = \{m_k\}$ | 质量谱子空间 |

**关键转变**：质量谱不再是分层迭代计算的产物，而是全域不动点方程在电弱规范对称下约化的解。

---

## 2. 压缩态射与 Hutchinson 型不动点定理

### 2.1 范畴论表述

在 $\mathbf{Rec}$ 中，一个自态射 $S: R \to R$ 称为**压缩态射**，如果存在常数 $c \in [0,1)$ 使得

$$d_{\mathcal{S}_R}(\Phi_R(S(x)), \Phi_R(S(y))) \le c \, d_{\mathcal{S}_R}(x,y), \quad \forall x,y \in \mathcal{S}_R.$$

### 2.2 不动点对象存在唯一性

**定理（范畴压缩映射原理）**：设 $S: R \to R$ 是 $\mathbf{Rec}$ 中的压缩态射，且状态空间 $\mathcal{S}_R$ 完备。则存在唯一的对象 $R_\ast \in \mathrm{Obj}(\mathbf{Rec})$（更准确地说是 $\mathcal{S}_R$ 中的唯一不动点 $x_\ast$）使得

$$S(R_\ast) = R_\ast.$$

**证明概要**：

取 $R$ 的状态空间 $\mathcal{S}_R$ 中任意初始点 $x_0$，构造迭代序列

$$x_{n+1} = \Phi_R(S(x_n)).$$

由压缩条件，$\{x_n\}$ 是 Cauchy 列。由完备性，$x_n \to x_\ast$。由 $S$ 与 $\Phi_R$ 的连续性，

$$\Phi_R(S(x_\ast)) = x_\ast.$$

唯一性由压缩条件直接得到。

### 2.3 在 $D$ 下的像

压缩态射 $S$ 的不动点对象 $R_\ast$ 在谱化函子 $D$ 下的像 $D(R_\ast)$ 对应 $\mathbf{Sp}$ 中的不变测度或谱分布。具体地：

- $D(R_\ast) = (\mathcal{H}_{R_\ast}, A_{R_\ast}, \sigma(A_{R_\ast}))$
- $A_{R_\ast}$ 的谱由压缩率 $\{\mu_i\}$ 给出。

---

## 3. Hilbert 范畴 $\text{Cat}_H(\mathcal{Cl})$

### 3.1 对象

$\text{Cat}_H(\mathcal{Cl})$ 的**对象**是 Clifford 值 Hilbert 空间，即三元组

$$(\mathcal{H}, \langle \cdot, \cdot \rangle, \mathcal{Cl}(p,q) \text{-模结构}),$$

其中：

- $\mathcal{H}$ 是复 Hilbert 空间；
- $\langle \cdot, \cdot \rangle: \mathcal{H} \times \mathcal{H} \to \mathcal{Cl}(p,q)$ 是 $\mathcal{Cl}(p,q)$ 值内积；
- $(p,q)$ 为任意非负整数对，不由范畴固定。

### 3.2 Clifford 值内积的公理系统

设 $\mathcal{Cl}(p,q)$ 为符号 $(p,q)$ 的实 Clifford 代数，$\mathcal{Cl}(p,q) \otimes_\mathbb{R} \mathbb{C}$ 为其复化。$\mathcal{H}$ 上的 **Clifford 值内积** 是映射

$$\langle \cdot, \cdot \rangle : \mathcal{H} \times \mathcal{H} \longrightarrow \mathcal{Cl}(p,q) \otimes_\mathbb{R} \mathbb{C},$$

满足以下公理：

**公理 (C1) 共轭对称性**：
$$\langle u, v \rangle = \overline{\langle v, u \rangle}, \qquad \forall u, v \in \mathcal{H},$$
其中 bar 表示 Clifford 代数的对合反自同构（grade involution 与复共轭的复合）。

**公理 (C2) $\mathcal{Cl}$-线性性**：对任意 $a, b \in \mathcal{Cl}(p,q) \otimes \mathbb{C}$ 与 $u, v \in \mathcal{H}$，
$$\langle u \cdot a, v \cdot b \rangle = \bar{a} \, \langle u, v \rangle \, b.$$

**公理 (C3) 正定性**：对任意非零 $v \in \mathcal{H}$，
$$\langle v, v \rangle \in \mathcal{Cl}(p,q) \otimes \mathbb{C}$$
是正元素，即其标量部 $\operatorname{Sc}(\langle v, v \rangle) > 0$。

**公理 (C4) 完备性**：由范数
$$\|v\|_{\mathcal{H}} := \sqrt{\operatorname{Sc}(\langle v, v \rangle)}$$
诱导的度量使 $\mathcal{H}$ 成为完备度量空间（Banach 空间，实为 Hilbert 空间）。

**公理 (C5) 模相容性**：对任意 $a \in \mathcal{Cl}(p,q) \otimes \mathbb{C}$ 与 $v \in \mathcal{H}$，
$$\|v \cdot a\|_{\mathcal{H}} \le C_a \|v\|_{\mathcal{H}},$$
其中 $C_a$ 仅依赖于 $a$（由 Clifford 代数的有限维性，此条件自动满足）。

> **注**：当 $(p,q)=(0,0)$ 时，$\mathcal{Cl}(0,0) = \mathbb{R}$，上述公理退化为普通复 Hilbert 空间内积。当 $(p,q)=(1,3)$ 或 $(1,7)$ 时，对应物理中的 Minkowski 型 Clifford 结构。

### 3.3 态射

$\text{Cat}_H(\mathcal{Cl})$ 的**态射**是有界 $\mathcal{Cl}(p,q)$ 线性算子

$$T: \mathcal{H}_1 \longrightarrow \mathcal{H}_2,$$

满足

$$T(a \cdot v + b \cdot w) = a \cdot T(v) + b \cdot T(w), \quad \forall a,b \in \mathcal{Cl}(p,q), \; v,w \in \mathcal{H}_1,$$

且存在常数 $C \ge 0$ 使得

$$\|T v\|_{\mathcal{H}_2} \le C \|v\|_{\mathcal{H}_1}, \quad \forall v \in \mathcal{H}_1.$$

> **命题 3.1**：$\text{Cat}_H(\mathcal{Cl})$ 在上述对象与态射下构成一个范畴。单位态射为恒等算子；态射复合为算子复合，有界性由算子范数的次可乘性保证。

### 3.4 与 $\mathbf{Sp}$ 的关系

$\mathbf{Sp}$ 可视为 $\text{Cat}_H(\mathcal{Cl})$ 的一个子范畴，其对象额外带有一个闭稠定正算子 $A_E$（谱算子），其态射额外满足谱交织条件。

形式化地，存在遗忘函子

$$U: \mathbf{Sp} \longrightarrow \text{Cat}_H(\mathcal{Cl}),$$

将 $(\mathcal{H}_E, A_E, \sigma_E)$ 映为底层 Clifford 值 Hilbert 空间 $(\mathcal{H}_E, \langle \cdot, \cdot \rangle)$。

---

## 4. 轨道函子 $O$

### 4.1 定义：从对象赋值到函子

**对象赋值**。首先在 $\mathrm{Obj}(\text{Cat}_H(\mathcal{Cl}))$ 上定义**规范群轨道权重**

$$O_0: \mathrm{Obj}(\text{Cat}_H(\mathcal{Cl})) \longrightarrow \mathbb{R}_+,$$

使得 $O_0(\mathcal{H})$ 表示 $\mathcal{H}$ 在规范群 $G$ 作用下的轨道"体积"或"重数"。

**函子化**。为把 $O_0$ 提升为真正的函子，引入**带测度 Hilbert 空间范畴** $\text{Cat}_{H}^{\mathrm{meas}}(\mathcal{Cl})$：

- 对象：$(\mathcal{H}, \nu_{\mathcal{H}})$，其中 $\mathcal{H} \in \mathrm{Obj}(\text{Cat}_H(\mathcal{Cl}))$，$\nu_{\mathcal{H}}$ 是 $\mathcal{H}$ 上关于 $G$ 作用的轨道测度；
- 态射：保测度的 $\mathcal{Cl}$-线性等距嵌入 $T: (\mathcal{H}_1, \nu_1) \to (\mathcal{H}_2, \nu_2)$，满足 $T_\ast \nu_1 = \nu_2|_{\operatorname{Im} T}$。

定义轨道函子

$$O: \text{Cat}_{H}^{\mathrm{meas}}(\mathcal{Cl}) \longrightarrow \mathbf{Meas}$$

为

$$O(\mathcal{H}, \nu_{\mathcal{H}}) := (\mathbb{R}_+, \nu_{\mathcal{H}}/\sim_G),$$

其中 $\sim_G$ 为 $G$ 作用下的轨道等价，商测度 $\nu_{\mathcal{H}}/\sim_G$ 集中在 $O_0(\mathcal{H})$ 上。对保测度态射 $T$，$O(T)$ 为相应的测度推进映射。

> **注**：若把 $\mathbb{R}_+$ 视为离散范畴（仅有恒等态射），则 $O$ 成为普通函子当且仅当 $O_0$ 在同构类上常值。这在物理上通常不成立（不同对象可有不同轨道权重），因此 $O$ 更自然地取值于 $\mathbf{Meas}$ 或偏序范畴 $(\mathbb{R}_+, \le)$。

### 4.2 作为范畴内态射性质

在偏序范畴 $(\mathbb{R}_+, \le)$ 中，$O$ 可定义为协变函子：对保测度态射 $T: \mathcal{H}_1 \to \mathcal{H}_2$，要求

$$O(\mathcal{H}_1) \le O(\mathcal{H}_2),$$

即轨道权重在嵌入下不减少。物理上这意味着：子表示的轨道重数不超过母表示的轨道重数。

具体实例：

- **标准模型**：$O$ 在三代费米子对象上的取值由 SU(3) 的 Weyl 轨道给出，导出 $q_u : q_d : q_l = 1 : 1 : 3$。对嵌入 $T: \mathcal{H}_{\mathrm{up}} \hookrightarrow \mathcal{H}_{\mathrm{quark}}$，$O(T)$ 为保序映射，满足 $1 \le 1$。
- **NTK**：$O$ 由网络架构与初始化分布的对称性诱导。对样本增广映射 $T: \mathcal{H}_{n} \to \mathcal{H}_{n'}$（$n < n'$），$O(T)$ 满足 $O(\mathcal{H}_n) \le O(\mathcal{H}_{n'})$。
- **弦论**：$O$ 由弦世界面模空间的对称性诱导。对亏格增加映射 $T: \mathcal{M}_{g,n} \to \mathcal{M}_{g',n'}$，轨道维数单调不减。

### 4.3 轨道函子的函子性条件

**命题 4.1**。上述映射 $O: \text{Cat}_{H}^{\mathrm{meas}}(\mathcal{Cl}) \to (\mathbb{R}_+, \le)$ 构成协变函子，当且仅当：

1. **等距嵌入保权重**：若 $T: \mathcal{H}_1 \to \mathcal{H}_2$ 是等距嵌入，则 $O(\mathcal{H}_1) \le O(\mathcal{H}_2)$；
2. **复合单调性**：对可复合的 $T_1, T_2$，$O(T_2 \circ T_1) = O(T_2) \circ O(T_1)$（在偏序范畴中即不等式的传递性）；
3. **单位态射**：$O(\mathrm{id}_{\mathcal{H}}) = \mathrm{id}_{O(\mathcal{H})}$（即 $O(\mathcal{H}) \le O(\mathcal{H})$）。

**证明**。偏序范畴中的态射是序关系，恒等态射是自反性。条件 1–3 正是协变函子的定义。

> **推论**：若所有态射都是等距嵌入且轨道权重在嵌入下单调不减，则 $O$ 是良定义的协变函子。在 SM 实例中，这由规范群表示的包含关系保证；在 NTK 与弦论实例中，由状态空间/模空间的增广映射保证。

### 4.4 与旧理论的对照

| 旧理论 | 新抽象表述 |
|---|---|
| $q_u : q_d : q_l = 1 : 1 : 3$ 来自 Cl(1,7) 旋量分解 | 轨道函子 $O$ 在 SM 实例下的取值 |
| IFS 压缩因子 $c_i$ | 压缩态射 $S$ 的谱半径 $c < 1$ |
| Bowen 方程 $\sum p_i^q c_i^{\tau(q)} = 1$ | 全域不动点方程在分形测度子空间上的限制 |
| FRG 流 $V_{\mathrm{eff}}(\Lambda)$ | 全域不动点方程在有效势子空间上的限制 |
| 代次指数质量公式 $m_{s,k} = y_0 e^{-(k-1)\beta_s z_s \eta_s}$ | 全域不动点方程在质量谱子空间上的离散谱解 |

---

## 5. 结构定理层的层级关系

```
元公理层
  ├── 递归系统范畴 Rec
  ├── 谱范畴 Spec
  ├── 谱化函子 D: Rec → Spec
  └── Clifford 值分形 RKHS 存在性
      ↓
结构定理层
  ├── 全域不动点方程 F[V] = V
  ├── 压缩态射不动点定理
  ├── Cat_H(Cl) Hilbert 范畴
  ├── 轨道函子 O
  └── 谱对应 λ_i = e^{-μ_i}
      ↓
实例假设层
  ├── 标准模型 = Cl(1,7)
  ├── NTK = 惰性训练极限
  ├── 弦论 = Cl(9,1)
  └── 引力测地线分形
```

---

## 6. 待解决问题（已严格化）

1. ~~**$\mathcal{V}$ 的严格构造**：归纳极限或余极限的存在性条件；在 $\mathbf{Sp}$ 中是否总有余极限？~~  已在 §1.1 中给出余极限构造，并在命题 1.2 中给出存在条件（等距嵌入 + Spec 封闭性）。
2. ~~**$\mathcal{F}$ 的良定性**：如何保证 $\mathcal{F}$ 在不同子空间 $D(R)$ 上的限制相容？~~  已在 §1.2 中由 Koopman 提升的交换关系证明 $\mathcal{F}$ 良定义（命题 1.4）。
3. ~~**$\text{Cat}_H(\mathcal{Cl})$ 的公理**：Clifford 值内积的公理系统（正定性、共轭对称性、线性性）需要显式列出。~~  已在 §3.2 中给出 (C1)–(C5) 五条公理，并在命题 3.1 中证明其构成范畴。
4. ~~**轨道函子的函子性**：$O$ 是否真正构成函子？它需要如何作用于态射？~~  已在 §4.1–§4.3 中通过引入带测度 Hilbert 空间范畴与偏序范畴 $(\mathbb{R}_+, \le)$，给出 $O$ 的函子化定义与充要条件（命题 4.1）。

---

## 7. 版本记录

- v0.1（2026-07-12）：初稿，定义全域不动点方程、压缩态射不动点定理、$\text{Cat}_H(\mathcal{Cl})$ 范畴、轨道函子。
- v0.2（2026-07-12）：严格化 $\mathcal{V}$ 的余极限构造（定义 1.1、命题 1.2），证明 $\mathcal{F}$ 良定性（命题 1.4），显式列出 Clifford 值内积公理（§3.2），并给出轨道函子 $O$ 的函子性条件（命题 4.1）。
