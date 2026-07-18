# 三层公理体系草案

> 本文档为「通用不动点范畴框架」的公理系统草案。核心目标：将原有 7 条公理拆分为不可被实例修改的**元公理层**、由元公理导出的**结构定理层**、以及可替换的**实例假设层**，从而彻底消除标准模型数值拟合对理论本体的反向修正。

---

## 0. 设计原则

1. **不可反馈原则**：实例假设层的任何拟合结果，不构成对元公理层与结构定理层的反驳。
2. **范畴表述原则**：理论本体使用范畴论语言，不绑定特定维度、特定分形映射或特定规范群。
3. **去递归原则**：递归迭代仅作为数值工具出现在实例假设层，不出现在理论公理本体。
4. **向下兼容原则**：抽象框架保留原有三条理论内核：
   - 分形压缩 ↔ 算子谱指数对应：$\lambda_i = e^{-\mu_i}$；
   - 递归系统可通过算子半群实现去递归；
   - 以 Clifford 值分形 RKHS 为泛函基底。

---

## 第二层：结构定理层（Application—测量公理 M1–M4）

在元公理 1–3 的基础上，[Paper X](../paper/paper10_spectral_quantum.md) 在 $\mathbf{Spec}$ 范畴中建立了量子测量的四条具体公理：

- **M1（谱投影公理）**：测量对应 $\mathbf{Spec}$ 中的投影态射族 $\{P_i\}$，满足幂等性、正交性和完备性。
- **M2（谱流动力学公理）**：测量过程中的谱流方程 $dA_t/dt = [A_{\text{int}}, A_t] + \kappa(\mathcal{D}(A_t)-A_t)$ 是元公理 3 谱去递归化函子的推广——添加了 $\kappa$ 对角化项。
- **M3（Born 规则公理）**：测量概率由轨道函子的谱权重给出，是 $\mathbf{Spec}$ 上的函子不变量。
- **M4（谱分支公理）**：实际观察结果由分支拓扑权重选择，对应 $\mathbf{Rec}$ 中递归系统的分支结构。

M1–M4 与三层公理体系的关系：
- M1–M2 在**结构定理层**：由元公理 2（$\mathbf{Spec}$ 存在性）和元公理 3（$D$ 函子存在性）导出。
- M3–M4 在**实例假设层**：Born 规则和分支选择可以通过替换为其他概率解释来修改。

详细推导见 Paper X §2 和配套笔记 `notes/spectral_measurement.md`。

---

## 第一层：元公理层（Meta-axioms）

> **不可被实例修改。** 本层定义「递归系统范畴」与「谱范畴」的存在性，以及二者之间自然对应的基本结构。

### 元公理 1（递归系统范畴存在性）

存在一个范畴 $\mathbf{Rec}$，称为**递归系统范畴**，满足：

- **对象**：递归系统 $R$， equipped with a self-similar evolution rule
  $$\Phi_R: \mathcal{S}_R \to \mathcal{S}_R,$$
  其中 $\mathcal{S}_R$ 为该递归系统的态空间。
- **态射**：$f: R_1 \to R_2$ 为态空间之间的连续映射，满足交换图
  $$\Phi_{R_2} \circ f = f \circ \Phi_{R_1}.$$

**复合律与单位律的严格定义**：见 [notes/rec_spec_definitions.md](../notes/rec_spec_definitions.md)。其中规定：
- 单位态射 $\mathrm{id}_R: R \to R$ 为 $\mathcal{S}_R$ 上的恒等映射；
- 态射复合 $g \circ f: R_1 \to R_3$ 由状态空间映射的通常复合给出，且复合存在的先决条件是 $\mathrm{target}(f) = \mathrm{source}(g)$（对象在状态空间与演化规则上严格相等，或在等价实例下满足统一等价关系）；
- 结合律与单位律由连续映射复合的相应性质直接得到。

> 注：IFS、神经网络前向传播、重整化群流、弦论拓扑递归均为 $\mathbf{Rec}$ 中的对象。

### 元公理 2（谱范畴存在性）

存在一个范畴 $\mathbf{Spec}$，称为**谱范畴**，满足：

- **对象**：三元组 $(\mathcal{H}, A, \sigma)$，其中 $\mathcal{H}$ 为复或 Clifford 值 Hilbert 空间，$A: \mathcal{D}(A) \subseteq \mathcal{H} \to \mathcal{H}$ 为闭稠定正算子，$\sigma = \sigma(A) \subseteq \mathbb{R}_{\ge 0}$。
- **态射**：有界线性算子 $T: \mathcal{H}_1 \to \mathcal{H}_2$，满足谱交织条件
  $$T A_1 \subseteq A_2 T.$$

**复合律与单位律的严格定义**：见 [notes/rec_spec_definitions.md](../notes/rec_spec_definitions.md)。复合由有界线性算子的通常复合给出，单位态射为恒等算子；交织条件的保持由算子复合的直接验证得到。

### 元公理 3（谱去递归化函子存在性与自然性）

存在一个协变函子
$$D: \mathbf{Rec} \longrightarrow \mathbf{Spec},$$
称为**谱去递归化函子**，将递归系统的自相似演化映射为算子半群的指数演化：

$$D(\Phi_R) = e^{-t A_R}, \quad t \ge 0,$$

其中 $A_R$ 为与递归系统 $R$ 关联的闭稠定正算子。

 furthermore，$D$ 满足自然性：对任意 $f: R_1 \to R_2$ 于 $\mathbf{Rec}$，下图交换：

```
R_1 --D--> Spec(R_1)
| f          | D(f)
v            v
R_2 --D--> Spec(R_2)
```

**忠实性与伴随函子的严格结果**：

- **忠实性**：若 $\mathcal{H}_{R_2}$ 的再生核为 universal kernel（或至少能分离 $\mathcal{S}_{R_2}$ 的点），则 $D$ 在 $\mathrm{Hom}_{\mathbf{Rec}}(R_1, R_2)$ 上是单射。证明见 [roadmap/phase1_meta_axioms.md](../roadmap/phase1_meta_axioms.md) 定理 3.4。
- **右伴随 $R$**：在 $\mathbf{Rec}$ 完备且 $D$ 保持小极限并满足解集条件下，$D$ 存在右伴随 $R: \mathbf{Spec} \to \mathbf{Rec}$。充分必要条件见 [roadmap/phase1_meta_axioms.md](../roadmap/phase1_meta_axioms.md) 定理 4.1。

### 元公理 4（再生核 Hilbert 空间存在性）

对任意 $R \in \mathrm{Obj}(\mathbf{Rec})$，$D(R)$ 可实现在一个 Clifford 值分形再生核 Hilbert 空间（Clifford-valued fractal RKHS）上。即存在核函数

$$K_R: X_R \times X_R \longrightarrow \mathcal{Cl}(p,q),$$

使得 $D(R)$ 的谱空间 $\mathcal{H}_R$ 具有再生性质：对任意 $x \in X_R$ 与 $f \in \mathcal{H}_R$，

$$f(x) = \langle f, K_R(x, \cdot) \rangle_{\mathcal{H}_R}.$$

> 注：$(p,q)$ 不固定，由实例假设层选定。

---

## 第二层：结构定理层（Structural Theorems）

> **形式固定，由元公理导出。** 本层将元公理具体化为压缩映射、多分形谱、算子半群等数学结构，但**不绑定任何具体物理模型或数值迭代算法**。

### 结构定理 1（压缩态射与 Hutchinson 不动点）

在 $\mathbf{Rec}$ 中，若态射 $S: R \to R$ 满足谱压缩条件

$$\sigma(S) < 1,$$

则存在唯一不动点对象 $R_\ast \in \mathrm{Obj}(\mathbf{Rec})$ 使得

$$S(R_\ast) = R_\ast.$$

该不动点对象在 $D$ 下的像 $D(R_\ast)$ 对应 $\mathbf{Spec}$ 中的不变测度/谱分布。

> 注：此定理替代原有 IFS 迭代式 $x_{n+1} = \bigcup S_i(x_n)$；迭代仅作为数值逼近手段。

### 结构定理 2（谱对应定理）

对任意 $R \in \mathrm{Obj}(\mathbf{Rec})$，设其压缩态射的谱为 $\{\mu_i\}$，算子半群生成元 $A_R$ 的离散谱为 $\{\lambda_i\}$，则存在范畴等价

$$\lambda_i = e^{-\mu_i}.$$

> 注：此为核心等式 $ \lambda_i = e^{-\mu_i}$ 的升级形式，从数值等式提升为两个范畴对象谱之间的自然等价。

**严格范畴自然等价**：定义两个从 $\mathbf{Rec}$ 到有限多重集合范畴的函子

- $M(R) := \sigma(-\log \Phi_R^\ast) = \{\mu_i\}$（压缩谱）；
- $L(R) := \sigma(\Phi_R^\ast) = \{\lambda_i\}$（算子半群谱）。

则对每个 $R \in \mathrm{Obj}(\mathbf{Rec})$，映射

$$\eta_R: M(R) \longrightarrow L(R), \quad \eta_R(\mu) := e^{-\mu}$$

给出自然变换 $\eta: M \Longrightarrow L$，且在每个对象上都是双射，因此 $M \cong L$。详细构造与证明见 [notes/spectral_correspondence_equivalence.md](../notes/spectral_correspondence_equivalence.md)。

### 结构定理 3（全域不动点方程）

存在全域谱态空间 $\mathcal{V}$ 与泛函映射

$$\mathcal{F}: \mathcal{V} \longrightarrow \mathcal{V},$$

使得所有子系统的不动点均为全域不动点方程

$$\mathcal{F}[\mathcal{V}] = \mathcal{V}$$

在相应子空间上的限制。具体地：

- IFS Hutchinson 测度：$\mathcal{F}_\mu[\mu] = \mu$；
- Ruelle Gibbs 测度：$\mathcal{F}_q[\mu_q] = \mu_q$；
- FRG 有效势不动点：$\mathcal{F}_{RG}[V_{\mathrm{eff}}] = V_{\mathrm{eff}}$；
- 费米子质量谱不动点：$\mathcal{F}_m[\{m_k\}] = \{m_k\}$。

**局部吸引子与全域不动点的距离度量**：设 $\mathcal{F}: \mathcal{V} \to \mathcal{V}$ 为全域泛函映射，$v_{num}$ 为数值迭代得到的近似解。定义局部吸引子捕获指数（LACI）

$$\mathrm{LACI}(v_{num}) := \frac{\rho(v_{num})}{\rho_{ref}} + \frac{\Delta(v_{num})}{\Delta_{ref}} + \frac{1}{\gamma(v_{num})/\gamma_{ref} + \epsilon},$$

其中：
- $\rho(v) = \|\mathcal{F}(v) - v\|$ 为不动点残差；
- $\Delta(v)$ 为从多个初值出发收敛吸引子的分散度；
- $\gamma(v) = 1 - \|D\mathcal{F}(v)\|$ 为局部谱间隙。

**定理**：在全局压缩情形下，$\mathrm{LACI}(v) = 0 \Longleftrightarrow v = v_\ast$ 且 $v_\ast$ 为唯一全局吸引子；若存在局部吸引子 $v_{loc} \neq v_\ast$，则 LACI 在 $v_{loc}$ 邻域具有正下界。证明见 [roadmap/phase4_semantics_over_fitting.md](../roadmap/phase4_semantics_over_fitting.md) 定理 2.1、2.2。

> 注：局部吸引子可严格表述为约束子集 $\mathcal{C} \subseteq \mathcal{V}$ 上的不动点 $v_{loc} \in \mathrm{Fix}(\mathcal{F}, \mathcal{C})$，而全局不动点 $v_\ast$ 是消除所有约束后的唯一不动点。见 [roadmap/phase4_semantics_over_fitting.md](../roadmap/phase4_semantics_over_fitting.md) 定理 4.1、4.2。

### 结构定理 4（算子半群去递归化）

任意递归系统 $R$ 的迭代演化 $\Phi_R^n$ 可由其去递归化像 $D(R) = e^{-t A_R}$ 的离散采样实现：

$$\Phi_R^n \cong e^{-n A_R}, \quad n \in \mathbb{N}.$$

> 注：此定理为「去递归」核心范式的数学表述。

### 结构定理 5（轨道函子与权重比例）

在 $\mathbf{Spec}$ 上可定义规范群轨道函子

$$O: \mathrm{Obj}(\mathbf{Spec}) \longrightarrow \mathbb{R}_+,$$

将对象映射为其在规范群作用下的轨道权重。轨道权重比例作为范畴内固有态射性质，不绑定具体 Clifford 代数签名或旋量表示。

> 注：原有 $q_u : q_d : q_l = 1 : 1 : 3$ 是此函子在标准模型实例下的取值。

---

## 第三层：实例假设层（Model Hypotheses）

> **可替换、不反馈到上层。** 本层将抽象框架应用于具体物理或数学系统。每个实例都是独立的「下游插件」。

### 实例假设 1（标准模型 = Cl(1,7) 低能实例）

在低能电弱对称性下，选取

- Clifford 签名 $(p,q) = (1,7)$；
- 规范群 $G_{SM} = SU(3)_C \times SU(2)_L \times U(1)_Y$；
- 轨道函子 $O$ 在三代费米子对象上的取值由 SU(3) Weyl 轨道给出。

在此假设下，全域不动点方程约化为可数值求解的质量谱方程，原有 `sm_mass_complete_v5.py` 中的 IFS、Bowen 方程、RG 迭代、代次指数公式全部作为数值工具出现。

### 实例假设 2（神经网络 NTK = 惰性训练极限）

在无限宽度神经网络的惰性训练（lazy training）极限下，选取

- 递归系统 $R_{NN}$ 为神经网络参数梯度下降动态；
- 谱去递归化像 $D(R_{NN})$ 为神经正切核（NTK）的谱演化；
- 轨道函子 $O$ 由网络架构与初始化分布决定。

### 实例假设 3（弦论 = Cl(9,1) 实例）

在弦论散射振幅的拓扑递归框架下，选取

- Clifford 签名 $(p,q) = (9,1)$ 或相应超对称签名；
- 递归系统 $R_{ST}$ 为 Eynard-Orantin 拓扑递归；
- 轨道函子 $O$ 由弦世界面模空间的对称性决定。

### 实例假设 4（引力测地线分形）

在强引力场中，将测地线方程的数值积分递归视为 $\mathbf{Rec}$ 对象，$D(R_{Geo})$ 给出测地线偏差算子的谱分布。

---

## 附：层级间的信息流规则

```
┌─────────────────────────────────────────┐
│  元公理层（Meta-axioms）：不可被实例修改      │
│  MA1: Rec 存在性                         │
│  MA2: Spec 存在性                        │
│  MA3: 谱去递归化函子 D: Rec → Spec        │
│  MA4: Clifford 值分形 RKHS 存在性          │
├─────────────────────────────────────────┤
│  结构定理层（Structural Theorems）：由元公理导出│
│  ST1: 压缩态射与 Hutchinson 不动点         │
│  ST2: 谱对应 λ_i = e^{-μ_i}               │
│  ST3: 全域不动点方程                       │
│  ST4: 算子半群去递归化                     │
│  ST5: 轨道函子 O                           │
├─────────────────────────────────────────┤
│  实例假设层（Model Hypotheses）：可替换、不反馈 │
│  MH1: 标准模型 = Cl(1,7)                  │
│  MH2: NTK = 惰性训练极限                   │
│  MH3: 弦论 = Cl(9,1)                      │
│  MH4: 引力测地线分形                       │
└─────────────────────────────────────────┘
```

**关键规则**：
- 元公理层 → 结构定理层：逻辑蕴含，单向。
- 结构定理层 → 实例假设层：特例化/约化，单向。
- 实例假设层 → 上层：**禁止反向修正。** 若某实例拟合不好，只能说明该实例不适合当前选择的函子/轨道取值，或需要引入新的实例假设，而非修改上层结构。

---

## 待解决问题（已严格化）

1. ~~严格定义 $\mathbf{Rec}$ 与 $\mathbf{Spec}$ 的对象与态射（特别是态射的复合律与单位律）。~~  已完成：详见 [notes/rec_spec_definitions.md](../notes/rec_spec_definitions.md) 与本文元公理 1、2 的严格化补充。
2. ~~证明谱去递归化函子 $D$ 的忠实性（faithfulness）。~~  已完成：见 [roadmap/phase1_meta_axioms.md](../roadmap/phase1_meta_axioms.md) 定理 3.4；本文元公理 3 已引用。
3. ~~研究伴随函子 $D \dashv R$ 的存在条件：$R: \mathbf{Spec} \to \mathbf{Rec}$ 将谱空间生成最小递归系统。~~  已完成：见 [roadmap/phase1_meta_axioms.md](../roadmap/phase1_meta_axioms.md) 定理 4.1；本文元公理 3 已引用。
4. ~~将结构定理 2 的 $ \lambda_i = e^{-\mu_i}$ 表述为严格的范畴自然等价，而非仅作为等式。~~  已完成：见 [notes/spectral_correspondence_equivalence.md](../notes/spectral_correspondence_equivalence.md) 与本文结构定理 2 的严格化补充。
5. ~~定义局部 Hutchinson 吸引子与全域不动点之间的「距离」度量，给出过拟合的几何判据。~~  已完成：见 [roadmap/phase4_semantics_over_fitting.md](../roadmap/phase4_semantics_over_fitting.md) 定理 2.1、2.2、4.1、4.2；本文结构定理 3 已引用。

---

## 版本记录

- v0.1（2026-07-12）：初稿，提出三层公理体系与待解决问题。
- v0.2（2026-07-12）：严格化 Rec/Spec 复合律与单位律，引用 D 忠实性、D⊣R、谱自然等价、LACI 等已完成定理，将待解决问题全部标记为已解决。
