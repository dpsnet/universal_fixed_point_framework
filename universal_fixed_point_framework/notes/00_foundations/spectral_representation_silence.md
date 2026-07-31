# 表示静默（D-静默）：谱态射在递归表示下的不可表示性

> **来源**：UFPF 路径 B（Agda 重形式化）交叉校验发现。SpImD 子范畴方案的态射层（RIm_map/右三角）在有限维原型中结构性不可闭合，其数学本质是一种新的静默类型——**表示/编码层静默**。
>
> **状态**：研究笔记 v0.1（2026-07-31）。推导完整，未进入论文。

---

## 1. 背景：态射层不可闭合的发现链

伴随对 $D\dashv R$（$D:\mathbf{Rec}\to\mathbf{Sp}$ 谱化函子，$R$ 余伴随）的闭合历程：

1. **Lean 侧** `Adjunction.lean` 恒等原型编译失败（`nS=nT`、`step=id`、`S.A=单位阵` 三个隐含条件，`lake env lean` 实证）
2. **Agda 侧** SpImD 子范畴方案（对应 RAP5a）：对象层闭合（`DR-iso`/`left-triangle-img`），态射层（`RIm_map`/右三角）卡在 **D 的 full 性**
3. **基数反例**（决定性）：D 的 full 性在有限维原型中为假

## 2. 基数反例（决定性证据）

设 $X=Y$ 为 **2 状态平凡递归系统**（$\mathrm{step}=\mathrm{id}$）。则：

$$A_X = A_Y = \mathrm{transferMatrix}(\mathrm{id}) = I_2 \quad(\text{单位矩阵})$$

- **谱态射空间**：$\mathrm{Hom}_{\mathbf{Sp}}(D(X), D(Y)) = \{P \in \mathbb{C}^{2\times 2} : P\cdot I = I\cdot P\} = \mathbb{C}^{4}$——交织条件恒成立，**不可数无限**
- **递归态射空间**：$\mathrm{Hom}_{\mathbf{Rec}}(X, Y) = \{\mathrm{Fin}\,2 \to \mathrm{Fin}\,2\} = 4$ 个函数——**有限**

伴随自然同构要求 $\mathrm{Hom}_{\mathbf{Sp}}(D(X),D(Y)) \cong \mathrm{Hom}_{\mathbf{Rec}}(X,Y)$——**不可数集与有限集之间不存在双射**，矛盾。

**直接反例**：$P = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ 是合法谱态射（满足交织），但每行非"恰一个 1"，不是任何 $\mathrm{transferMatrix}(f)$。因此 **D 不 full**，`RIm_map` 不可定义。

## 3. 表示静默的定义

### 3.1 静默度的同构推广

框架既有定义（UFPF 修复方案定义 R7）：态射 $f$ 的可见性函数

$$v(f_t) = \frac{\|P_{V_\Lambda}D(f_t)\|}{\|D(f_t)\|} \in [0,1],$$

其中 $V_\Lambda = E_{A_2}([0,\Lambda])\mathcal H_{R_2}$ 为可观测谱子空间。

**表示静默（D-静默）**：谱态射 $\varphi \in \mathrm{Hom}_{\mathbf{Sp}}(E,F)$ 的 D-静默度

$$\boxed{S_D(\varphi) = 1 - \frac{\|P_{\mathrm{Im}(D)}(\varphi)\|}{\|\varphi\|}}$$

其中 $P_{\mathrm{Im}(D)}$ 是到转移矩阵像 $\mathrm{Im}(D)\subset\mathrm{Hom}_{\mathbf{Sp}}$ 的正交投影。结构上与定义 R7 **完全同构**——仅投影空间从"可观测谱子空间 $V_\Lambda$"换成"D 的像 $\mathrm{Im}(D)$"。

**定义（表示静默）**：$\varphi$ 是 **表示静默的**，当且仅当 $P_{\mathrm{Im}(D)}(\varphi)=0$（$\varphi$ 正交于所有转移矩阵），即 $\varphi$ 在递归表示下完全不可达。

### 3.2 与框架静默的对照

| | 框架静默（定义 R7） | 表示静默（D-静默） |
|:--|:--|:--|
| 判据 | $P_{V_\Lambda}D(f)=0$ | $P_{\mathrm{Im}(D)}(\varphi)=0$ |
| 静默度 | $1-\|P_{V_\Lambda}D(f)\|/\|D(f)\|$ | $1-\|P_{\mathrm{Im}(D)}(\varphi)\|/\|\varphi\|$ |
| 静默对象 | 态射 $f$ 的**像**落于不可观测谱 | 谱态射 $\varphi$ **本身**不可被 Rec 表示 |
| 类型 | 动力学层（沿演化参数 $t$） | 表示/编码层（静态结构） |
| 投影空间 | 谱子空间 $V_\Lambda$ | D 的像 $\mathrm{Im}(D)$ |

## 4. 量级分析

平凡系统反例中：$\mathrm{Im}(D)$ = 4 个转移矩阵（有限集），$\mathrm{Hom}_{\mathbf{Sp}} = \mathbb{C}^4$（连续统）。

- $\mathrm{Im}(D)$ 在 $\mathrm{Hom}_{\mathbf{Sp}}$ 中**测度为零**
- **"几乎所有"谱态射是表示静默的**（$S_D \approx 1$）

这是极端静默：连续统级的态射信息在递归表示下不可达。物理读法：只有"确定性跳转"型动力学（0-1、每行恰一 1）能被递归表示捕获；携带连续谱参数的态射（如 $P=\begin{pmatrix}1&0\\1&1\end{pmatrix}$ 的任意复参数）在递归表示下完全静默——类比量子相干在经典测量下的静默，但发生在**表示层**而非观测层。

## 5. 分层定位：S0 表示层

现有四层静默体系（S1 严格 / S2 渐近 / S3 ε-有效 / 辫子）均为**动力学/观测层**。表示静默构成新的一层：

- **S0（表示静默）**：$P_{\mathrm{Im}(D)}(\varphi)=0$——谱态射不可被递归表示
- 层级关系：S0 是"编码前"的静默（在 D 应用之前就不可表示），与 S1-S4 的"编码后不可观测"平行且独立

**理论收益**：态射限制为转移矩阵（此前被批评为"平庸化"）由此获得规范语义——它是**保留 D-非静默态射**的投影操作，而非任意的人为限制。

## 6. 对伴随闭合的影响

| 层 | SpImD 方案闭合状态 |
|:--|:--|
| 对象层（DR-iso、左三角） | ✅ 闭合（Agda `DecursionFunctor.agda §5`） |
| 态射层（RIm_map、右三角） | ❌ 有限维原型结构性不可闭合（基数反例） |

闭合仅当：(a) 态射限制为转移矩阵（保留 D-非静默态射，伴随即平庸化）；或 (b) 转无限维（论文 R11 断言：R(E) 状态空间 = $\mathcal D(A_E)$，态射为连续映射，基数可能自洽——但该断言**未形式化**，需 T3 谱定理验证）。

## 7. 形式化落点

- Agda：`agda_formalization/DecursionFunctor/DecursionFunctor.agda §5`（对象层闭合 + 态射层反例注释）
- Lean：`RAP5a_explicit_adjunction.lean`（`DFunctor_full_open` 反例审计注释）
- 账目：`roadmap/phase60_category_verification.md`（v0.13-v0.14）

## 8. 开放问题

1. 论文 R11 无限维态射层断言（谱交织 → 谱匹配数据）的严格证明——需谱定理 + 函数空间基数论证（T3）
2. D-静默度在一般（非平凡）谱对象上的刻画——$P_{\mathrm{Im}(D)}$ 的显式形式
3. 表示静默与动力学静默的复合行为（S0 静默态射是否在复合下封闭？是否形成 sieve？对照定理 R6）
4. 表示静默是否对应物理上已知的"经典化/相干性丢失"结构

---

*关联*：UFPF 修复方案 §10-13（静默体系 + R11）；paper I 定理 2.4.5；RAP5a；路径 B 闭合账目。
