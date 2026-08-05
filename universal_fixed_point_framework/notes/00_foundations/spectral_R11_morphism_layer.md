# R11 无限维态射层验证（P1）：谱匹配双射的语义分岔

> **来源**：P4（基数反例）收官后的决定性推进方向 P1。对应 paper I 定理 C2.3 第 2 步"态射对应"断言（`paper1_fractal_spectral_derecursion.md`）与 RAP5a `RIm_map` 开放项。
>
> **状态**：研究笔记 v0.3（2026-08-01）。理论分析 + 有限维数值验证（7/7 PASS）+ **Agda 形式化完整落地**（T3 谱定理层阶段 6 收官）。v0.2→v0.3：形式化闭环（P1Spectral 有限维特例 + SpectralTheory 无限维：定理 3 / corollary4-∞ / corollary5 / P1-linear-closure 全部可证；Fuglede 方向 intertwine-imp-spectral 降为可证定理；§9 更新）。v0.1→v0.2：命题 6 反例修正（ψ=|z|z → ψ=|z|，正齐次性）、引理 1 $(\Rightarrow)$ 完整论证（Cayley 变换 + Fuglede）、§10 数值验证。

---

## 1. 问题陈述

有限维原型中伴随 $D\dashv R$ 的泛化态射层结构性不可闭合（P4 已形式化：Hom_Sp 不可数 vs Hom_Rec 有限）。唯一可能的闭合路径是论文 R11/构造 C2.2 的**无限维**设定。待验证的核心断言（定理 C2.3 第 2 步，目前为手写论证）：

$$\mathrm{Hom}_{\mathbf{Sp}}(E, D(S)) \;\cong\; \mathrm{Hom}_{\mathbf{Rec}_D}(R(E), S),$$

其中：
- $E = (\mathcal H_E, A_E, \sigma_E) \in \mathbf{Sp}$，$A_E$ 稠定、自伴、正定（$\sigma(A_E)\subseteq[0,\infty)$），$\mathcal D(A_E)$ 为其定义域（图范数拓扑）；
- $S \in \mathbf{Rec}_D$，Koopman 算子 $\Phi_S = e^{-A_S}$（$A_S$ 自伴正定），$D(S) = (\mathcal H_S, A_S)$；
- $R(E) = (\mathcal D(A_E),\ e^{-A_E}|_{\mathcal D(A_E)},\ E_{A_E})$（构造 C2.2）。

**结论（本笔记）**：断言的真值取决于 **Rec 态射的语义**——这是 P1 的分岔点。

- **线性语义**（Rec 态射为有界线性算子，论文论证隐含假设）：谱匹配双射成立，且**双射就是恒等映射**（两边是同一方程的解集）。伴随在无限维闭合。
- **集合语义**（Rec 态射为连续集合映射，框架 RecHom 的原始语义 `toFun : Fin n → Fin m` 的无限维延伸）：双射**不成立**（连续非线性谱匹配映射远超线性解空间）。S0 表示静默升级为结构性现象。

框架的 Rec 范畴语义倾向后者，因此 P1 的正确结论是：**闭合需要显式限定 Rec_D 态射为线性连续谱匹配映射**（论文定理 2.4.5"受限态射层"的无限维版）。这构成一个新的论文层限定（P0 的姊妹修正）。

---

## 2. 断言的精确化：双射两侧的显式集合

设 $\mathcal L(\mathcal H_E, \mathcal H_S)$ 为有界线性算子空间。定义三个子集：

$$M_{\mathrm{Sp}} = \{T \in \mathcal L(\mathcal H_E,\mathcal H_S) : T A_E \subseteq A_S T\},$$

$$M_{\mathrm{Rec}} = \{f \in \mathcal L(\mathcal H_E,\mathcal H_S) : f\circ e^{-A_E} = e^{-A_S}\circ f \text{ 在 } \mathcal D(A_E)\text{ 上}\},$$

$$M_{\sigma} = \{X \in \mathcal L(\mathcal H_E,\mathcal H_S) : X E_{A_E}(\Omega) = E_{A_S}(\Omega) X,\ \forall \text{Borel }\Omega\subseteq\mathbb R\},$$

其中 $E_{A_E}, E_{A_S}$ 为谱测度。**谱匹配条件** $M_\sigma$ 是枢纽：$X$ 只连接两侧相同的谱值（在谱表示下 $X$ 与乘法算子族交换）。

**线性语义下的断言**即 $\mathrm{Hom}_{\mathbf{Sp}}(E,D(S)) = M_{\mathrm{Sp}}$、$\mathrm{Hom}_{\mathbf{Rec}_D}(R(E),S) = M_{\mathrm{Rec}}$，且 $M_{\mathrm{Sp}} = M_{\mathrm{Rec}}$（谱匹配双射 = 恒等）。

---

## 3. 核心观察：Rec 态射语义的分岔

框架的 Rec 范畴（`RecCategory.agda`）中态射为 $\mathrm{RecHom}(X,Y)$，字段 `toFun : Fin n → Fin m` 是**集合映射**（仅交换条件约束）。有限维下"集合映射"与"线性算子"的差别就是 P4 反例的本质（线性矩阵 $P=[[1,0],[1,1]]$ 非任何集合映射的转移矩阵像）。

无限维延伸有两种互不相容的选择：

**(a) 线性语义**：态射 $f:\mathcal D(A_E)\to\mathcal H_S$ 有界线性。此时 $f$ 由稠定定义域唯一延拓为 $\mathcal L(\mathcal H_E,\mathcal H_S)$ 的元素，交换条件是有界算子方程，谱论工具（Fuglede/互易）可用。→ 断言 A（§4）成立。

**(b) 集合语义**：态射为连续（非线性）映射 $\mathcal D(A_E)\to\mathcal H_S$。交换条件 $f\circ e^{-A_E} = e^{-A_S}\circ f$ 的解空间包含大量非线性谱匹配映射（如 $f(x) = \psi(x)$ 的任意谱不变复合），基数与结构远超 $M_{\mathrm{Sp}}$。→ 断言 B（§5）：双射不成立。

**框架默认语义为 (b)**——这是与论文论证（隐含 (a)）的根本分歧点，也是 P1 必须显式裁决的问题。

---

## 4. 断言 A（线性语义）：谱匹配双射 = 恒等

**引理 1（谱测度输送，交织 ⟺ 谱匹配）**。设 $A,B$ 为自伴算子（$\mathcal H_1,\mathcal H_2$ 上，$B$ 可为无界），$X\in\mathcal L(\mathcal H_1,\mathcal H_2)$。则 $X A \subseteq B X$ 当且仅当 $X E_A(\Omega) = E_B(\Omega) X$ 对所有 Borel $\Omega$ 成立。

- $(\Leftarrow)$ 直接：$XAx = X\int\lambda\,dE_A x = \int\lambda\,d(E_B X)x = BXx$，$x\in\mathcal D(A)$。
- $(\Rightarrow)$ 完整论证（依赖标准谱论事实，T3 形式化时需自建）：
  1. **有界情形**（$A,B$ 有界自伴，$XA=BX$）：由 $X A^k = B^k X$（归纳）得对任意多项式 $p$：$X p(A) = p(B) X$；Stone–Weierstrass 逼近到连续函数，单调收敛到指示函数，得谱测度输送 $X E_A(\Omega) = E_B(\Omega) X$。（等价表述：Fuglede 定理 $XN\subseteq MX$（正规）$\Rightarrow XN^\ast\subseteq M^\ast X$，谱投影由 Borel 函数演算。）
  2. **无界情形**（$XA\subseteq BX$，$X$ 有界）：经 **Cayley 变换** $U_A=(A-iI)(A+iI)^{-1}$（有界酉），交织传递为 $X U_A = U_B X$（标准事实，Reed–Simon Vol. I Thm VIII.21）；有界情形给出 $X E_{U_A}(\Omega) = E_{U_B}(\Omega) X$；Cayley 变换保持谱测度（$E_A \leftrightarrow E_{U_A}$），还原为 $X E_A(\Omega) = E_B(\Omega) X$。□

**引理 2（exp 单射 ⟹ 换位代数相等）**。设 $A$ 自伴且 $\sigma(A)\subseteq[0,\infty)$。则 $\{e^{-A}\}' = \{A\}'$（换位代数相等），且谱测度族互相可表达：$E_{e^{-A}}(\Omega) = E_A(-\log(\Omega\cap(0,1]))$，$E_A(\Omega) = E_{e^{-A}}(e^{-\Omega})$。

*证明要点*：$\phi(x)=e^{-x}:[0,\infty)\to(0,1]$ 是连续双射；Borel 函数演算下 $\phi$ 单射 ⟹ 谱测度经 $\phi$ 与 $\phi^{-1}$ 互相输送，两族生成同一 von Neumann 代数 $W^\ast(A)=W^\ast(e^{-A})$；换位代数由谱测度族决定。□

**定理 3（线性语义下谱匹配双射，即 P1 断言 A）**。在 §2 记号下，
$$M_{\mathrm{Sp}} = M_\sigma = M_{\mathrm{Rec}}.$$

*证明*：
1. $M_{\mathrm{Sp}} = M_\sigma$：引理 1（$X=T$，$A=A_E$, $B=A_S$）。□
2. $M_{\mathrm{Rec}} = M_\sigma$：对 $f\in M_{\mathrm{Rec}}$，$f\circ e^{-A_E} = e^{-A_S}\circ f$ 是有界算子方程。由引理 1（有界情形，Fuglede 直接适用）得谱测度输送 $f\,E_{e^{-A_E}}(\Omega) = E_{e^{-A_S}}(\Omega)\,f$；再由引理 2 把 $e^{-A}$ 的谱族换回 $A$ 的谱族，得 $f\in M_\sigma$。反向由引理 1 的 $(\Leftarrow)$ 与引理 2 直接。□

**推论 4（双射的显式形式）**。$\mathrm{Hom}_{\mathbf{Sp}}(E,D(S))$ 与 $\mathrm{Hom}_{\mathbf{Rec}_D}(R(E),S)$ 在 §2 的嵌入下是**同一个集合** $M_\sigma$（线性映射由稠定定义域唯一延拓/限制互逆），故自然同构是恒等映射，自然性自动成立。

**推论 5（对象重建）**。$D(R(E)) \cong E$：$A_{R(E)} = -\log(e^{-A_E}) = A_E$，因为 $\sigma(e^{-A_E})\subseteq(0,1]$ 且 $-\log\circ\,e^{-x}=x$ 在 $[0,\infty)$ 上（引理 2 的谱测度输送给出严格谱形式）。注：$\sigma(A_E)$ 含 $0$ 时 $1\in\sigma(e^{-A_E})$，$-\log(1)=0$ 仍良定义。

---

## 5. 断言 B（集合语义）：双射不成立

若 Rec 态射为连续（非线性）映射 $f:\mathcal D(A_E)\to\mathcal H_S$，则 $M_{\mathrm{Rec}}$ 替换为

$$M_{\mathrm{Rec}}^{\mathrm{set}} = \{f\in C(\mathcal D(A_E),\mathcal H_S) : f\circ e^{-A_E} = e^{-A_S}\circ f\}.$$

**命题 6（集合语义下无双射）**。一般情形 $M_{\mathrm{Rec}}^{\mathrm{set}} \supsetneq M_\sigma$，且不含于任何线性算子空间。

*证明要点*：
1. $M_\sigma \subseteq M_{\mathrm{Rec}}^{\mathrm{set}}$：线性谱匹配映射是连续映射且满足交换条件。□
2. 存在非线性元：若 $A_E=A_S=A$ 且 $A$ 有非平凡谱，取单位向量 $v$（$Av=\lambda v$，$\lambda\ge 0$）与连续 $\psi:\mathbb C\to\mathbb C$ 满足**正齐次度 1**：$\psi(cz)=c\psi(z)$ 对 $c\in(0,1]$（如 $\psi(z)=|z|$，或更一般 $\psi(z)=z\cdot g(\arg z)$；注意 $\psi(z)=|z|z$ 是齐次度 2，**不**满足）。定义 $f(x)=\psi(\langle x,v\rangle)\,v$。则 $A$ 自伴 $\Rightarrow \langle e^{-A}x,v\rangle=\langle x,e^{-A}v\rangle=e^{-\lambda}\langle x,v\rangle$，故 $f(e^{-A}x)=\psi(e^{-\lambda}\langle x,v\rangle)v=e^{-\lambda}\psi(\langle x,v\rangle)v=e^{-A}f(x)$（$e^{-\lambda}\in(0,1]$）。$f$ 连续、非线性（$\psi=|\cdot|$ 非线性），故 $f\in M_{\mathrm{Rec}}^{\mathrm{set}}\setminus M_\sigma$。□

**推论 7**。集合语义下：
- $M_{\mathrm{Rec}}^{\mathrm{set}}$ 基数（$|\mathbb C|$ 上连续函数空间，可分时 $=\mathfrak c^{|\mathbb N|}=\mathfrak c$）可能仍与 $M_\sigma$ 基数相当，但**结构不同**——双射不存在（非线性元无法与线性算子对应）。
- 这正是有限维 P4 反例的无限维版：**静默态射（谱匹配的集合映射非转移矩阵像）不随维度消失**。

---

## 6. 基数自洽分析

- **线性语义**：$M_{\mathrm{Sp}} = M_{\mathrm{Rec}} = M_\sigma$，基数自动相等（同一集合）。$|M_\sigma|\in\{0,1,\mathfrak c\}$ 型（谱匹配约束下，非零元通常整族出现）。基数自洽是定理 3 的**推论而非独立假设**。
- **集合语义**：$|M_{\mathrm{Rec}}^{\mathrm{set}}|$ 一般 $=\mathfrak c$（含常值映射与非线性元），$|M_{\mathrm{Sp}}|\le\mathfrak c$。基数缺口不复现为"有限 vs 不可数"，但**等势不等于双射**——结构差异（线性 vs 非线性）阻断自然同构。
- 论文 §6 与笔记 §9 的"基数可能自洽"判断：**在等势意义下正确，在双射意义下仅在线性语义成立**。

---

## 7. 严格条件清单（断言 A 成立所需）

1. $A_E$ **自伴正定**（$\sigma(A_E)\subseteq[0,\infty)$）且 m-增生——Hille–Yosida 前提（项目已登记教训：必须显式验证自伴性与正定性）。
2. $\Phi_{R(E)} = e^{-A_E}$ 由 Borel 函数演算定义（谱定理），有界压缩。
3. **Rec 态射限制为有界线性**（或至少线性且闭）——§3 的分岔裁决，论文需显式声明。
4. 谱测度输送引理依赖 **Fuglede 定理**（自伴情形，Reed–Simon 标准结果）——T3 形式化时列为待自建引理。
5. 定义域细节：$e^{-A_E}(\mathcal D(A_E))\subseteq\mathcal D(A_E)$（自伴 $A$ 的 $e^{-A}$ 保定义域），交织条件 $T(\mathcal D(A_E))\subseteq\mathcal D(A_S)$ 需逐项验证。
6. 对象层：$D(R(E))$ 的谱化作用在**图范数拓扑**的状态空间上——$D$ 对无限维对象的定义需与有限维兼容（谱测度保留，见构造 C2.2 附加结构）。

---

## 8. 结论与判定（P1 的两分支）

| 语义选择 | 谱匹配双射 | 伴随闭合 | S0 静默地位 |
|:--|:--|:--|:--|
| **线性**（Rec_D 态射 = 有界线性谱匹配算子） | ✅ 成立（恒等双射，定理 3） | ✅ 无限维闭合 | 仅有限维原型（维度伪影） |
| **集合**（Rec_D 态射 = 连续映射） | ❌ 不成立（命题 6） | ❌ 结构性不可闭合 | **结构性普遍现象**（含无限维） |

**关键发现**：P1 的答案不是"谱匹配断言对不对"，而是**框架必须裁决 Rec 态射的语义**。框架现有语义（`RecHom.toFun` 集合映射）指向集合分支；论文 C2.3 论证隐含线性分支。这是 P0（论文层范围修正）之后的**第二项必须的限定修正**：无限维闭合声明需显式注明"受限态射层 = 线性连续谱匹配映射"。

**推荐裁决**（论文层）：采用**线性语义**作无限维闭合路径——它给出干净的恒等双射（定理 3），且与有限维"受限态射层（转移矩阵）"语义连续（转移矩阵本身是线性算子）。集合语义下 Rec_D 需附加线性结构公理方可闭合，工程与概念代价均高。

---

## 9. 形式化落点（✅ 已完成：Agda T3 谱定理层，2026-08-01）

**状态更新**：P1 的 Agda 形式化已随 T3 阶段 6 收官**完整落地**（原"形式化依赖 T3 实分析层"已解除）。对应关系：

- **有限维特例（`P1Spectral/P1Spectral.agda`，v0.42-v0.44）**：定理 3 退化版 M_Sp = M_σ = M_Rec（谱匹配⟹交织/exp 交换**可证**，谱定理方向登记公理）+ 推论 4 恒等双射（Hom-Sp ≅ Hom-σ ≅ Hom-Rec，`corollary4`）。
- **无限维（`SpectralTheory/SpectralTheory.agda`，T3 阶段 6，v0.45-v0.76）**：
  - **引理 1 谱测度输送（交织 ⟺ 谱匹配）**：Fuglede 方向（交织⟹谱匹配）**降为可证定理**（`intertwine-imp-spectral`，§5g——证明链：多项式交换 §3b ⟹ fc 多项式/连续交换 §5f ⟹ 指示桥接 E(P) = fc(1_P) §5g 全链闭合）；反向（谱匹配⟹交织，σ-to-Sp）由谱积分线性推导（§1b/§3，可证）。
  - **引理 2 exp 单射**：M_Rec ⊆ M_σ（`Rec-to-σ` **可证**，§3）+ t 参数化（`Rec-t-to-σ`，§8b）。
  - **定理 3**：`theorem3`（M_Sp = M_σ = M_Rec 四方向，§5g）+ t 版（`theorem3-t`，§8c）。
  - **推论 4**：`corollary4-∞`（Hom_Sp ≅ₗ Hom_σ ×₁ Hom_Rec ≅ₗ Hom_σ，恒等双射，§6）。
  - **推论 5（对象重建）**：`corollary5`（recon-op = -log(e^(-A)) ≡ A，§5；recon-op 已降为定义）。
  - **Hille-Yosida 五条件齐备**（§1/§8/§12/§12b/§12c，含生成元 = -A 条件 v）。
  - **`P1-linear-closure`**（§9）：obj-recon（corollary5）× hom-bij（corollary4-∞）——**线性语义下伴随无限维闭合**的组装结论。

**对应本笔记断言**：断言 A（线性语义双射 = 恒等，定理 3）→ `theorem3` + `corollary4-∞`（已形式化）；引理 1 → `intertwine-imp-spectral`（§5g）+ `σ-to-Sp`（§3）（已形式化）；引理 2 → `Rec-to-σ`（§3）（已形式化）；对象重建 → `corollary5`（已形式化）。

**公理纪律**：谱论基础登记公理（谱测度/谱表示/半群对象/谱测度代数/完备性）+ 桥接公理（fc 定义性质/sup 算子序/经典扩展 indicator），每项注明模型必然性/用途/降定理路径，见 SpectralTheory §15 公理纪律审计（24 → 22 块 postulate）。

**剩余（非阻塞，后续层）**：
- **经典扩展层**：indicator 点态性质（1_P x = 1 ⟺ P x，需排中律）未显式登记——当前证明仅用桥接 E(P) = fc(1_P)。
- **测度论层**：spec-int 对无界 f 的 sup 收敛细节（截断逼近 f_n = min(f, n)）。
- **Lean**：Mathlib 谱论（`Spectrum`/`ContinuousFunctionalCalculus`）成熟后可直接形式化定理 3 的有限维/离散谱特例（路线图路径 A 持续主线）。

---

## 10. 数值验证（`scripts/paperX_spectral_matching.py`，7/7 PASS）

有限维数值验证（n=4,5,6 随机自伴 Hermitian 矩阵，解空间经 Kronecker 展开 + SVD 零空间）确认 §4/§5 的全部结构断言：

| # | 检查项 | 结果 |
|:-:|:--|:--|
| 1 | 交织 $X\cdot A_E = A_S\cdot X$ 解空间 = 谱匹配 $X E_{A_E}(\Omega)=E_{A_S}(\Omega)X$ 解空间（引理 1） | ✅ 4 组随机自伴一致（投影差 < 1e-6） |
| 2 | exp 交换 $X\cdot e^{-A_E}=e^{-A_S}\cdot X$ 解空间 = 谱匹配解空间（引理 2 + 定理 3） | ✅ 3 组随机自伴一致 |
| 3 | 谱匹配解空间闭式 $\dim M_\sigma=\sum_{\lambda\in\sigma_E\cap\sigma_S}m_E(\lambda)\,m_S(\lambda)$ | ✅ 3 组随机自伴 |
| 4 | 谱不相交（$\sigma_E\cap\sigma_S=\varnothing$）⟹ 三条件解空间均为 $\{0\}$ | ✅ |
| 5 | 命题 6 非线性元 $f(x)=|\langle x,v\rangle|\,v$ 满足交换条件（残差 0）且非线性（$f(-x)=f(x)\neq-f(x)$） | ✅ |
| 6 | **P1 反例修正**：$\psi(z)=|z|$ 正齐次（$\psi(cz)=c\psi(z)$）；$\psi(z)=|z|z$ 齐次度 2 不满足（误差 1.422） | ✅ |
| 7 | 重数块结构：$A_E=\mathrm{diag}(1,1,2)$，$A_S=\mathrm{diag}(1,2,2)$ ⟹ $\dim=4=2\cdot1+1\cdot2$，非零块仅在匹配本征空间间 | ✅ |

**验证意义**：三条件等价（定理 3 的核心）在有限维数值下完全成立，且谱匹配闭式给出解空间维数的精确刻画——这与"线性语义下双射 = 恒等"一致；检查 5/6 确认集合语义反例构造（$\psi=|\cdot|$ 沿本征方向）的正确性（含对初版 $\psi=|z|z$ 的错误修正）。

---

*关联*：paper I 定理 C2.3/2.4.5（限定修正）；`notes/00_foundations/spectral_representation_silence.md` §9（P1 判定）；RAP5a `RIm_map`；路线图 `phase60_category_verification.md`（T3 账目 + P1 状态）；数值脚本 `scripts/paperX_spectral_matching.py`（注册 `run_all_tests.py`）；Agda 形式化：`P1Spectral/P1Spectral.agda`（有限维特例）+ `SpectralTheory/SpectralTheory.agda`（无限维，§9 形式化落点）。
