# Rec₂ 交换律偏差的 BCH 修正复合：数学推导与引力根源

> **来源**：`HigherRecCategory.lean` 三处 `sorry` 的闭合路径（R12 分析；`spectral_category_scope_stratification.md` 阶段 2/3 衔接；Sp 侧 `spExchangeLaw` 偏差化先例）。
> **状态**：研究笔记 v0.7（2026-08-04）。数学推导完成，数值验证 **16/16 检查通过** + 结构性诊断（D7/D8 结合律失败、D9 拉回 2-态射空间稀疏性），**选定路径 B（D-拉回）**，**Lean 实现完成**（`HigherRecCategory.lean` 重写，零 `sorry`，`lake build` 通过）；开放问题 7/8 **部分闭合**（§4.4 定理 11/12）。
> **规范声明**：本文为**谱新增**推导——Rec₂ 2-态射复合的修正形式与交换律偏差结构均为本框架新贡献，非既有文献结果。Sp 侧 `spExchangeLaw` 偏差定理（`HigherSpCategory.lean`，已机器证明）为既有资产，作为镜像模板引用。
> **理论地位**：交换律偏差 = 引力（Paper XXXV §2）。本文给出 Rec₂ 侧该机制的精确数学构造，作为 `HigherRecCategory.lean` 三处 `sorry` 由"定义性缺口登记"升级为"偏差定理族"的基础。
>
> **v0.4 更新（2026-08-04）**：结合律失败（§7 开放问题 6）后选定**路径 B（D-拉回）**——Rec₂ 2-态射改由 Sp₂（`HigherSpCategory.lean`，homotopy 结构良定义且结合）经 $D$ 拉回定义，见 §4.3。原 ℕ-指标 flow-diagonal 结构保留为"流分解"诠释。

---

## 1. 目标与先例

### 1.1 要闭合的开放项

`HigherRecCategory.lean` 三处 `sorry`（2026-08-04 诚实登记为定义性缺口）：

| 位置 | 内容 | 失败原因 |
|:--|:--|:--|
| `vertComp`（L58） | 竖复合（逐点加法）的自然性 | 交叉列取值不受控 |
| `horizComp`（L77） | 横复合（矩阵乘法）的自然性 | 交叉列取值不受控 |
| `exchange_law`（L123） | 交换律（要求交叉项 α·β′+β·α′ = 0） | 一般不成 |

**核心判断（延续 `spExchangeLaw` 教训）**：不证明严格交换律（弱范畴中为假；填成等式 ⟺ $G_N \to 0$，物理错误）。正确路径 = **构造满足自然性的修正复合**（BCH 型修正），再把交换律升级为**偏差定理**。

### 1.2 Sp 侧先例（已机器证明，镜像模板）

`HigherSpCategory.lean` 中 Sp₂ 交换律已按偏差化闭合：

- `spExchangeLaw_homotopy_deviation`：LHS∘RHS 的 homotopy 差 = $(R.P-Q.P)\,\alpha'.h + \beta.h\,(P'.P-Q'.P)$；
- `spExchangeLaw_deviation_partial_commutator`：偏差重写为谱算子对易子 $X.A\,H - 2\,\beta.h\,Y.A\,\alpha'.h + H\,Z.A$；
- `spExchangeLaw_deviation_strict_limit`：交织条件下偏差 = 0（= 引力解耦 $G_N\to0$）。

偏差范数 $\epsilon = \|\Delta_{\mathrm{Ex}}\|/\|A\| \approx 8.12\times10^{-17}$（`notes/08_first_principles/04_gravity_analysis.md` L86）——范畴"几乎严格"，引力极弱。

---

## 2. 问题精确化

### 2.1 记号

- 1-态射：$f : X \to Y$（$\mathbf{Rec}$ 态射，$f \circ X.\mathrm{step} = Y.\mathrm{step} \circ f$）。
- 转移算子：$T_f := \mathrm{transferMatrix}\,f \in \mathrm{Mat}(X.T,\,Y.T;\,\mathbb C)$，$(T_f)_{i j} = \mathbf 1[f(i)=j]$。
- 2-态射 $\alpha : f \Rightarrow g$（$f,g : X \to Y$）：$\alpha : \mathbb N \to \mathrm{Mat}(X.T,\,Y.T;\,\mathbb C)$，自然性
  $$\alpha(n{+}1)[x,\,g(x)] = \alpha(n)[x,\,f(x)] \qquad (\forall n \in \mathbb N,\ x \in X.T).$$

### 2.2 自然性的 diag 形式

**引理 1（diag 形式）**。自然性 ⟺
$$\operatorname{diag}\big(\alpha(n{+}1)\,T_g\big) = \operatorname{diag}\big(\alpha(n)\,T_f\big).$$

*证*。$(\alpha(n{+}1)T_g)_{xx} = \sum_y \alpha(n{+}1)[x,y]\,(T_g)_{yx} = \alpha(n{+}1)[x,g(x)]$，同理右端 $= \alpha(n)[x,f(x)]$。□

**推论 2（流动对角不变量）**。对链 $f_0 \Rightarrow f_1 \Rightarrow f_2 \Rightarrow \cdots$，沿"流动对角"取值
$$\alpha_k(n)[x,\,f_k(x)] \xlongequal{\text{自然性}} \alpha_k(n{+}1)[x,\,f_{k+1}(x)] \xlongequal{\text{链}} \alpha_{k+1}(n{+}1)[x,\,f_{k+1}(x)] = \cdots$$
在复合流动下**恒定**。特别地，$f = g$ 时 $\alpha(n)[x,f(x)]$ 不依赖 $n$（对角常数）。

> **结构含义**：2-态射的"流动对角"自由度是一个函数（每行一个值，不随 $n$ 变），离对角自由度自由。自然性只约束对角（相对 $T_f$/$T_g$ 的转移意义），不约束交叉列——这是逐点复合失效的根源。

---

## 3. 逐点复合的精确失效

**命题 3（竖复合失效）**。设 $\alpha : f \Rightarrow g$、$\beta : g \Rightarrow h$，$\gamma := \alpha + \beta$（逐点）。则 $\gamma$ 满足自然性当且仅当
$$\big[\alpha(n{+}1)[x,h(x)] - \alpha(n{+}1)[x,g(x)]\big] + \big[\beta(n)[x,g(x)] - \beta(n)[x,f(x)]\big] = 0 \qquad (\forall n,x),$$
即两个"失配项"之和为零（每个失配项各自为零是充分非必要）——一般不成立。

*证*。$\gamma(n{+}1)[x,h(x)] = \alpha(n{+}1)[x,h(x)] + \beta(n{+}1)[x,h(x)]$，$\gamma(n)[x,f(x)] = \alpha(n)[x,f(x)] + \beta(n)[x,f(x)]$。用 $\alpha$、$\beta$ 自然性：$\alpha(n{+}1)[x,g(x)] = \alpha(n)[x,f(x)]$、$\beta(n{+}1)[x,h(x)] = \beta(n)[x,g(x)]$。代入得两式相等 ⟺ $\alpha(n{+}1)[x,h(x)] - \alpha(n{+}1)[x,g(x)] = \beta(n)[x,g(x)] - \beta(n)[x,f(x)]$，即命题所述之和为零。□

> 注：甚至 $\beta : g \Rightarrow g$（同源）时仍要求 $\beta(n)[x,g(x)] = \beta(n)[x,f(x)]$——**逐点竖复合仅在 $f=g=h$ 且满足对角常数条件时合法**。横复合同理（交叉列 $g'(g(x))$ vs $g'(y)$ 不受控）。

---

## 4. 修正复合（BCH 型修正形式）

### 4.1 竖复合修正处方

**定义 4（竖复合修正）**。设 $\alpha : f \Rightarrow g$、$\beta : g \Rightarrow h$。定义
$$\gamma := \beta \circ_v \alpha := \alpha + \beta + C_v,$$
其中修正 $C_v$ 的**最小选择**：离对角全 0，流动对角初值 $C_v(0)[x,f(x)] := 0$，且流动增量由下式**唯一**确定（$\forall n,x$）：
$$C_v(n{+}1)[x,h(x)] - C_v(n)[x,f(x)] = \operatorname{diag}\big(\alpha(n{+}1)(T_g - T_h)\big)_{xx} + \operatorname{diag}\big(\beta(n)(T_f - T_g)\big)_{xx}.$$

> **推导**（关键，2026-08-04 手算例验证修正）：自然性要求 $\gamma(n{+}1)[x,h(x)] = \gamma(n)[x,f(x)]$，即
> $$C_v(n{+}1)[x,h(x)] - C_v(n)[x,f(x)] = \big[\alpha(n)[x,f(x)] - \alpha(n{+}1)[x,h(x)]\big] + \big[\beta(n)[x,f(x)] - \beta(n{+}1)[x,h(x)]\big].$$
> 用 $\alpha$ 自然性（$\alpha(n)[x,f(x)] = \alpha(n{+}1)[x,g(x)]$）与 $\beta$ 自然性（$\beta(n{+}1)[x,h(x)] = \beta(n)[x,g(x)]$）代入，即得上式。注意 $\alpha$ 项为 $T_g - T_h$（非 $T_h - T_g$）、$\beta$ 项取时间指标 $n$（非 $n{+}1$）。

**定理 5（竖复合自然性闭合）**。$\gamma : f \Rightarrow h$ 满足自然性。

*证*。直接计算：
$$\gamma(n{+}1)[x,h(x)] - \gamma(n)[x,f(x)] = \underbrace{\big[\alpha(n{+}1)[x,h(x)] - \alpha(n)[x,f(x)]\big]}_{= \alpha(n{+}1)[x,h(x)] - \alpha(n{+}1)[x,g(x)]\ \text{（$\alpha$ 自然性）}} + \underbrace{\big[\beta(n{+}1)[x,h(x)] - \beta(n)[x,f(x)]\big]}_{= \beta(n)[x,g(x)] - \beta(n)[x,f(x)]\ \text{（$\beta$ 自然性）}} + \big[C_v(n{+}1)[x,h(x)] - C_v(n)[x,f(x)]\big].$$
三项为 $\operatorname{diag}(\alpha(n{+}1)(T_h-T_g))_{xx} - \operatorname{diag}(\beta(n)(T_f-T_g))_{xx} + \operatorname{diag}(\alpha(n{+}1)(T_g-T_h))_{xx} + \operatorname{diag}(\beta(n)(T_f-T_g))_{xx} = 0$（定义 4）。□

**关键结构**：修正由**转移算子差**（$T_h-T_g$、$T_f-T_g$，符号随项而定）驱动——即由动力学与态射链的**非对易**度量驱动。当 $f = g = h$（$T_f = T_g = T_h$）时增量消失，$C_v \equiv 0$，退回 $\alpha + \beta$（与 §3 注一致）。

> **BCH 解释**：把 2-态射视为谱流"生成元"，则复合 = 生成元组合的指数化；$\alpha$、$\beta$ 作为无穷小，$\alpha + \beta$ 是一阶，$C_v$ 是使自然性成立的修正——离散/转移版本的对易子修正（连续极限下对应 BCH 公式 $e^A e^B = e^{A+B+[A,B]/2+\cdots}$ 的 $[A,B]/2$ 项）。$C_v \ne 0$ 即"流动非对易"，是引力偏差的载体。

### 4.2 横复合修正处方

**定义 6（横复合修正）**。设 $\alpha : f \Rightarrow g$（$f,g : X\to Y$）、$\alpha' : f' \Rightarrow g'$（$f',g' : Y\to Z$）。定义
$$\gamma' := \alpha \circ_h \alpha' := \alpha\cdot\alpha' + C_h,$$
其中 $(\alpha\cdot\alpha')(n) := \alpha(n)\cdot\alpha'(n)$（矩阵乘法），修正 $C_h$ 最小选择（离对角 0、流动对角初值 0），流动增量由失配项唯一确定：
$$C_h(n{+}1)[x,g'(g(x))] - C_h(n)[x,f'(f(x))] = -\Big[\big(\alpha(n{+}1)\alpha'(n{+}1)\big)_{x,\,g'(g(x))} - \big(\alpha(n)\alpha'(n)\big)_{x,\,f'(f(x))}\Big].$$

**定理 7（横复合自然性闭合）**。$\gamma' : f \circ f' \Rightarrow g \circ g'$ 满足自然性。*证*：与定理 5 同构（自然性为线性条件，修正精确消去失配）。□

> 注：$\circ_h$ 记法与 Rec 范畴复合 $f \circ f'$（实际代码为 $f \gg f'$，即先 $f$ 后 $f'$）对齐，矩阵乘积顺序以代码为准。

### 4.3 路径 B：D-拉回（选定方案，v0.4）

§7 开放问题 6 的诊断表明最小修正复合**非结合**（D7/D8），非 2-范畴合法复合。选定**路径 B**：Rec₂ 2-态射改由 Sp₂ 经谱化函子 $D$ 拉回定义——Sp₂ 的 homotopy 结构（`HigherSpCategory.lean`）**良定义且结合**（`spVertComp_assoc` 已机器证明；竖复合 = homotopy 和，横复合 = whiskering，均为标准 Godement 结构）。

**定义 8（拉回 2-态射）**。设 $f,g : X \to Y$（$\mathbf{Rec}$ 态射），定义
$$\mathrm{RecTwoMorphism}^{PB}(f,g) := \mathrm{SpTwoMorphism}(Df)(Dg),$$
即单个 homotopy 矩阵 $H \in \mathrm{Mat}(X.T, Y.T;\,\mathbb C)$ 满足 **homotopy 条件**（线性方程）
$$T_g - T_f = A_X\,H - H\,A_Y, \qquad A_X := \mathrm{stepMatrix}\,X.\mathrm{step},\quad A_Y := \mathrm{stepMatrix}\,Y.\mathrm{step}.$$

**命题 9（拉回结构的范畴律，全部由 Sp₂ 继承）**。
1. **良定义**：条件是 $H$ 的线性方程，故竖复合 $H_1 \circ_v H_2 := H_1 + H_2$、横复合 $H \circ_h H' := H\cdot T_{f'} + T_g\cdot H'$（whiskering）均良定义；
2. **结合律**：竖 $\circ_v$ 由矩阵加法继承（结合）；横 $\circ_h$ 由 whiskering 继承（结合）；
3. **单位**：零矩阵（$T_f - T_f = 0 = A_X\cdot 0 - 0\cdot A_Y$）；
4. **交换律偏差**：直接从 Sp₂ 继承（`spExchangeLaw_homotopy_deviation`/`_partial_commutator`/`_strict_limit`，已机器证明）。

*证*：逐项对应 $D$（$Df.P = T_f$，$D(X).A = A_X$），拉回后即 Sp₂ 结构；Sp₂ 侧定理直接适用。□

**推论 10（Rec₂ ⊂ Sp₂，圈定一致性）**。拉回定义的 Rec₂ 是 Sp₂ 在 D 像上的子 2-范畴（SpImD₂）。这与阶段 1 圈定（`spectral_category_scope_stratification.md` §2：D ⊣ R 伴随在 SpImD 上严格成立）完全一致——Rec 侧的 2-范畴结构由谱化嵌入继承，而非另行构造。

> **与原 ℕ-指标结构的联系（v0.7 已部分闭合，见 §4.4 定理 12）**：原 flow-diagonal 条件 $\alpha(n{+}1)[x,g(x)] = \alpha(n)[x,f(x)]$ 与拉回 homotopy $H$ 的精确对应——**时间无关子类** $\alpha(n) \equiv H$——已在同源情形建立；一般时间相关族的对应仍开放（§7 问题 7 残余）。

### 4.4 拉回 2-态射非空性与时间无关对应（v0.7，开放问题 7/8 部分闭合）

**设定**：$X, Y \in \mathbf{Rec}$（步进 $s_X, s_Y$），$f, g : X \to Y$ 为 RecHom；$L(H) := A_X H - H A_Y$（Sylvester 算子）。

**定理 11（非空性，可对角化步进）**。若 $A_X, A_Y$ 可对角化（如置换步进），则
$$\mathrm{Hom}^{PB}(f,g) \neq \varnothing \iff f = g, \qquad \mathrm{Hom}^{PB}(f,f) = \{H : A_X H = H A_Y\} \ (\text{交织子空间，含 } 0,\ \text{非空}).$$

*证*。$f,g$ 为 RecHom ⟹ $T_f, T_g$ 均交织 $A_X \leftrightarrow A_Y$（`transferMatrix_step_comm`），故 $T_g - T_f \in \ker(L)$。$A_X, A_Y$ 可对角化 ⟹ $L$ 半单 ⟹ $\mathrm{range}(L) \cap \ker(L) = \{0\}$。拉回条件可解 ⟺ $T_g - T_f \in \mathrm{range}(L)$ ⟺ $T_g - T_f = 0$ ⟺ $f = g$。同源时条件化为齐次 $A_X H = H A_Y$（解空间非空）。□

**定理 12（时间无关对应）**。时间无关族 $\alpha(n) \equiv H$ 恒满足同源自然性（$\alpha(n{+}1)[x,f(x)] = \alpha(n)[x,f(x)]$ 为恒等式）；且 $H \in \mathrm{Hom}^{PB}(f,f)$ ⟺ $H$ 另满足交织 $A_X H = H A_Y$。故
$$\{\text{拉回 2-态射}\} = \{\text{时间无关自然性族}\} \cap \{\text{交织矩阵}\} \quad (\text{同源情形}).$$
异源情形（$f \neq g$）：时间无关族还需 $H[x,g(x)] = H[x,f(x)]$ 才满足自然性，且定理 11 表明拉回 2-态射不存在（可对角化步进下）。

*证*：直接代入定义。□

> **结构诠释**：拉回定义比旧自然性定义**更严格**——Rec₂ 的 2-范畴结构本质上是**同源自交**（id 型 2-态射 + 交织矩阵），非平凡异源 2-态射在可对角化步进下不存在（数值 T15/T16 确认）。这与阶段 1 圈定"谱匹配双射 = 恒等映射（线性语义）"完全一致。开放问题 8 的非空性刻画**闭合**（可对角化情形）；不可对角化步进的一般情形仍开放。开放问题 7 的对应**部分闭合**（时间无关子类）。

---

## 5. 交换律偏差定理（引力根源的精确形式）

### 5.1 偏差对象

设 $\alpha : f \Rightarrow g$、$\beta : g \Rightarrow h$（$f,g,h : X \to Y$），$\alpha' : f' \Rightarrow g'$、$\beta' : g' \Rightarrow h'$（$f',g',h' : Y \to Z$）。定义
$$\mathrm{LHS} := (\beta \circ_v \alpha) \circ_h (\beta' \circ_v \alpha'), \qquad \mathrm{RHS} := (\beta \circ_h \beta') \circ_v (\alpha \circ_h \alpha').$$

**命题 8（偏差合法性）**。$\Delta := \mathrm{LHS} - \mathrm{RHS}$ 是合法的 2-态射（$f \circ f' \Rightarrow h \circ h'$）。

*证*。由定理 5、7，LHS、RHS 均为合法 2-态射；自然性是矩阵族的**线性条件**，故其差亦满足。□

### 5.2 偏差的主导结构

**定理 9（交换律偏差 = 交叉项 + 修正诱导项）**。$\Delta$ 可分解为
$$\Delta = \underbrace{\alpha\cdot\beta' + \beta\cdot\alpha'}_{\text{交叉项（水平-垂直非对易缺陷）}} + \underbrace{\delta C_{\text{v}} + \delta C_{\text{h}}}_{\text{修正诱导项}},$$
其中 $\delta C_{\text{v}}$、$\delta C_{\text{h}}$ 由 §4 修正 $C_v$、$C_h$ 的差诱导。

*证*。展开（省略 $n$）：$\mathrm{LHS} = (\alpha+\beta+C_v^{(1)})(\alpha'+\beta'+C_v^{(2)}) + C_h$，$\mathrm{RHS} = (\alpha\beta'+\beta\alpha'+\cdots) + C_v^{(\text{h})}$，整理即得。□

**推论 10（严格极限 = 引力消失）**。在严格极限下（$f=g=h$、$f'=g'=h'$，且 2-态射族可交换——等价地诸转移算子相等且 $\alpha\cdot\beta' + \beta\cdot\alpha' = 0$）：
$$\Delta = 0,$$
即交换律严格成立，$G_N \to 0$（引力解耦）。

*证*。严格极限下 $T_f=T_g=T_h$、$T_{f'}=T_{g'}=T_{h'}$，§4 修正增量消失（$C_v, C_h \equiv 0$）；交叉项为 0（可交换假设）。□

> **物理诠释（延续 Paper XXXV §2）**：$\Delta \neq 0$ 即交换律不严格成立，其范数 $\|\Delta\|_F$ 是引力的范畴论载体；$G_N \propto \|\Delta\|_F^2$（Phase C 关系，Paper XXXI；数值 $\epsilon = \|\Delta_{\mathrm{Ex}}\|/\|A\| \approx 8.12\times10^{-17}$）。本文把该机制从 Sp₂（已机器证明）推广到 Rec₂ 侧。

### 5.3 与 Sp 侧桥接

经谱化函子 $D$（`DecursionFunctor.lean`），Rec₂ 2-态射嵌入 Sp₂（`HigherSpCategory.lean`）。桥接目标（待形式化，非本文完成）：
$$D\big((\beta\circ_v\alpha)\circ_h(\beta'\circ_v\alpha')\big) - D\big((\beta\circ_h\beta')\circ_v(\alpha\circ_h\alpha')\big) \xlongequal{?} \text{Sp}_2\ \text{交换律偏差（对易子型）}.$$
两侧偏差相容性 = "引力根源"在 Rec/Sp 双侧的统一机器证明。

---

## 6. Lean 形式化路线（路径 B：D-拉回，镜像 `HigherSpCategory.lean`）

**选定方案（v0.4）**：`HigherRecCategory.lean` 的 `RecTwoMorphism` 按定义 8 重定义为 Sp₂ 2-态射在 $D$ 下的拉回（homotopy 矩阵 + 线性条件），三处 `sorry` 由该良定义结构消除。

**✅ 实现完成（v0.5，2026-08-04）**：`HigherRecCategory.lean` 已按路径 B 重写并全部机器证明（`lake build` 通过，零 `sorry`）：

| 定理 | 内容 | 镜像 |
|:--|:--|:--|
| `recVertComp`（+condition） | 竖复合（homotopy 和）良定义（命题 9.1） | `spVertComp`（已机器证明） |
| `recHorizComp`（+condition） | 横复合（whiskering）良定义（命题 9.1） | `spHorizComp`（已机器证明） |
| `transferMatrix_step_comm` | $T_f \cdot A_Y = A_X \cdot T_f$（RecHom 交织矩阵形式） | 新（$D$ 侧对应 `intertwine`） |
| `recVertComp_assoc` / `recHorizComp_assoc` | 竖/横结合律（命题 9.2） | `spVertComp_assoc`（已机器证明） |
| `recExchangeLaw_homotopy_deviation` | 交换律偏差 = $(T_h-T_g)\alpha' + \beta(T_{f'}-T_{g'})$ | `spExchangeLaw_homotopy_deviation` |
| `recExchangeLaw_partial_commutator` | 偏差 = $A_X(\beta\alpha') - 2\beta(A_Y\alpha') + (\beta\alpha')A_Z$ | `spExchangeLaw_deviation_partial_commutator` |
| `recExchangeLaw_strict_limit` | 交织条件下偏差 = 0（$G_N\to0$） | `spExchangeLaw_deviation_strict_limit` |

**前置依赖**：
- `transferMatrix`/`stepMatrix`/`DFunctor`（`DecursionFunctor.lean`，已有）；
- 矩阵加法/乘法/减法与 `ring`/`abel`（mathlib `Matrix`，`HigherSpCategory.lean` 已用同一批技巧）；
- **数值验证已完成**（2026-08-04，16/16 检查通过 + 诊断 D7/D8/D9）：`paperX_rec2_exchange_deviation.py`（已注册 `run_all_tests.py`）——BCH 修正处方自然性闭合、偏差合法性、裸偏差 = 交叉项、严格极限 Δ = 0、单位律、**D-拉回结构（T10-T14）**、**非空性/时间无关对应（T15/T16，§4.4）**；结合律不成立（D7/D8，§7 问题 6）、拉回 2-态射空间稀疏（D9，§7 问题 8）；
- **笔记先行**：路径 B 构造（§4.3）为本笔记 v0.4，Lean 实现以其为准（§4.1/4.2 的最小修正处方仅保留为分析工具，不进入 Lean 的复合定义）。

---

## 7. 开放问题与诚实边界

1. **$C_v$ 最小选择的唯一性**：流动对角增量唯一确定，但初值 $C_v(0)[x,f(x)] := 0$ 是约定；非零初值给出不同但同样合法的 2-态射。规范选择需物理判据（谱流规范）。
2. **修正项的封闭形式**：连续/无穷时极限下 $C_v$ 是否精确等于 BCH 对易子项 $[\alpha,\beta]/2$（当前为转移版本的离散增量），待推导。
3. **交叉项 $\alpha\cdot\beta' + \beta\cdot\alpha'$ 的范数绑定**：与 $r_{\mathrm{cat}}$、$\Delta\lambda_{\min}$ 的定量关系（Paper XXXI Phase C 在 Sp 侧已建立，Rec 侧待做）。
4. **Sp↔Rec 桥接**（§5.3）：$D$ 函子下两侧偏差的一致性，需额外引理（$D$ 对 2-态射的提升），独立于本文。
5. **非严格极限下交换律偏差与 `deltaSilence` 的关系**：偏差是否即静默层（Rec_lin/Rec_set 边界）的形式化载体（衔接 `spectral_representation_silence.md` 更新），待研判。
6. **最小修正的结合律失败（2026-08-04 数值诊断，决定性）**：`paperX_rec2_exchange_deviation.py` D7/D8 显示最小修正复合**不满足结合律**（竖偏差 $\sim 10^1$、横偏差 $\sim 5\times10^1$，O(1) 量级，非数值误差）。原因：结合律要求修正满足**余循环条件**
$$C_v(\alpha,\beta) + C_v\big(\alpha+\beta+C_v(\alpha,\beta),\,\delta\big) = C_v(\beta,\delta) + C_v\big(\alpha,\,\beta+\delta+C_v(\beta,\delta)\big),$$
最小选择（流动对角初值 0、离对角 0）不满足。**结论**：定义 4/6 的修正复合是"闭合自然性的预复合"，尚非 2-范畴的合法复合（单位律成立，见 T9）。**✅ 已选定路径 B（2026-08-04，v0.4）**：Rec₂ 2-态射按 §4.3 定义 8 由 Sp₂ 经 $D$ 拉回定义（homotopy 条件为线性方程，竖/横复合良定义且结合，交换律偏差由 Sp₂ 继承），三处 `sorry` 由该结构消除。路径 A（余循环选择，严格结合律的独立构造）保留为替代方案。
7. **拉回 homotopy 与原 ℕ-指标结构的对应（2026-08-04，🔶 部分闭合）**：**时间无关子类**已闭合——$\alpha(n) \equiv H$ 恒满足同源自然性，且 $H \in \mathrm{Hom}^{PB}(f,f)$ ⟺ $H$ 交织（§4.4 定理 12，数值 T15）。一般时间相关族 $\alpha(n)$ 的对应（"流分解" $H \leftrightarrow \alpha(n)$ 的谱流分辨/极限）仍开放；该对应若建立，将把 §4.1/4.2 的修正分析（作为 $H$ 的离散近似）与路径 B 完全统一。
8. **D-拉回 2-态射空间稀疏性（2026-08-04，🔶 部分闭合）**：转移矩阵恒有特征值 1（$\mathbf 1$ 为特征向量），故 Sylvester 方程 $A_X H - H A_Y = T_g - T_f$ 对一般 $f \neq g$ 罕见可解。**可对角化步进情形已闭合（§4.4 定理 11）**：$\mathrm{Hom}^{PB}(f,g) \neq \varnothing \iff f = g$（$T_g - T_f \in \ker L$ 且 $L$ 半单 ⟹ 须 $T_g = T_f$；数值 T16）。**不可对角化步进的一般情形仍开放**（如非双射函数的转移矩阵，亏损情形）。物理诠释：2-态射稀少 = 谱对应层的强约束（Rec₂ 本质为同源自交结构）。

---

## 8. 关联文件索引

| 文件 | 角色 |
|:--|:--|
| `formal_proof/.../HigherRecCategory.lean` | 本笔记的 Lean 载体（3 处 sorry 待升级为偏差定理） |
| `formal_proof/.../HigherSpCategory.lean` | Sp₂ 交换律偏差定理（已机器证明，镜像模板） |
| `formal_proof/.../DecursionFunctor.lean` | $D$ 函子、`transferMatrix`/`stepMatrix`（§5.3 桥接基础） |
| `paper/paper35_gravity_origin.md` | 交换律偏差 = 引力（Paper XXXV） |
| `notes/08_first_principles/04_gravity_analysis.md` | $\epsilon \approx 8.12\times10^{-17}$ 量化 |
| `notes/00_foundations/spectral_category_scope_stratification.md` | Rec_lin/Rec_set 分层（偏差 ↔ 边界静默） |
| `paperX_exchange_law_deviation.py` | Sp 侧偏差数值演示（简化模型） |
| `paperX_rec2_exchange_deviation.py` | 本笔记数值验证附件（8/8，已注册 `run_all_tests.py`） |
