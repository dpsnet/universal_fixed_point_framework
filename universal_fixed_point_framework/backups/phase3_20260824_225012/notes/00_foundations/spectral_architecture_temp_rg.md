# Temp/RG 纤维范畴架构定位——与 $\mathbf{Rec}/\mathbf{Sp}$ 的关系分析

**版本**：v0.1（2026-07-22）

**摘要**：本笔记系统分析 Temp/RG 纤维范畴体系在 UFPF 整体架构中的定位。核心结论：(1) Temp/RG **不是** $\mathbf{Rec}$ 的子范畴，而是 $\mathbf{Sp}$ 上的纤维范畴扩展——参数化递归系统如何接近 $\partial\mathbf{Rec}_D$ 边界；(2) Temp/RG 与 Paper I（$\mathbf{Rec}$ 底层）、Paper XIX（$\mathbf{Rec}_{\text{id}}$ + $\Sigma$-$\mathbf{Rec}$ 扩展层）共同构成五层 UFPF 架构：$\mathbf{Bun} \supset \mathbf{Sp} \supset \mathbf{Rec} \supset \mathbf{Rec}_{\text{id}} \supset \Sigma$-$\mathbf{Rec}$；(3) Temp/RG 为 $(G, \eta)$ 二维相图引入第三个独立维度（温度-标度对偶）；(4) 该框架可覆盖 QCD（完全验证）、BCS 超导（框架即用）、Hawking-Page 相变（有基础）、流变学（需扩展）等多类物理系统。

---

## 1. 问题起源

在研究笔记 [spectral_T_category.md](spectral_T_category.md) 及后续系列笔记中，我们构造了温度参数范畴 $\mathbf{Temp}$、RG 标度参数范畴 $\mathbf{RG}$ 以及谱纤维丛上的 Riemann 函子 $\hat{\mathcal{T}}_{\text{Riem}}$。一个自然的架构问题随之产生：

> Temp/RG 体系与 Paper I 的 $\mathbf{Rec}/\mathbf{Sp}$ 框架、Paper XIX 的 $\mathbf{Rec}_{\text{id}}/\Sigma$-$\mathbf{Rec}$ 扩展是什么关系？是子范畴、扩展、还是独立框架？

本笔记旨在明确回答这一问题。

## 2. 子范畴判据分析

### 2.1 $\mathbf{Rec}$ 子范畴的条件

**定义 2.1**（子范畴）。$\mathcal{C} \subset \mathbf{Rec}$ 是子范畴当且仅当：

1. **对象包含**：$\text{Ob}(\mathcal{C}) \subseteq \text{Ob}(\mathbf{Rec})$
2. **态射包含**：$\text{Hom}_\mathcal{C}(X,Y) \subseteq \text{Hom}_{\mathbf{Rec}}(X,Y)$ 对所有 $X,Y \in \text{Ob}(\mathcal{C})$
3. **恒等与复合封闭**：$\mathcal{C}$ 包含 $\mathbf{Rec}$ 的恒等态射限制，且态射复合在 $\mathcal{C}$ 中封闭

### 2.2 否定证明

**定理 2.1**（Temp/RG 不是 Rec 的子范畴）。$\mathbf{Temp}$ 和 $\mathbf{RG}$ **不是** $\mathbf{Rec}$ 的任何形式子范畴。

**证明**。$\mathbf{Rec}$ 的对象是四元组 $R = (\mathcal{S}_R, \Phi_R, \mathcal{T}_R, \mathcal{M}_R)$，其中 $\mathcal{S}_R$ 是 Polish 空间，$\Phi_R$ 是自相似映射，$\mathcal{T}_R$ 是时间半群，$\mathcal{M}_R$ 是附加结构。而 $\mathbf{Temp}$ 的对象是实数 $T \in (0,\infty)$，$\mathbf{RG}$ 的对象是实数 $\mu \in (0,\infty)$。这两类对象在集合论上不交集——实数不是四元组。因此条件 1（对象包含）不满足，无需检查条件 2-3。$\square$

**推论 2.1**（不是 $\mathbf{Sp}$ 的子范畴）。$\mathbf{Temp}$ 和 $\mathbf{RG}$ 也不是 $\mathbf{Sp}$ 的子范畴，因为 $\mathbf{Sp}$ 的对象是 $(\mathcal{H}, A, \sigma(A))$（Hilbert 空间 + 算子 + 谱），而温度 $T$ 不是这类三元组。

### 2.3 直观理解

子范畴要求"是同一类东西的子集"。但：

- $\mathbf{Rec}$ 的对象 = **系统**（有状态空间、有演化映射）
- $\mathbf{Sp}$ 的对象 = **谱数据**（有 Hilbert 空间、有算子）
- $\mathbf{Temp}$ 的对象 = **参数值**（实数温度）

参数值既不是系统也不是谱数据，因此不可能成为任何一方的子范畴。

## 3. 正确的架构定位：纤维范畴

### 3.1 纤维范畴的定义

**定义 3.1**（纤维范畴的直觉）。一个以 $\mathcal{B}$ 为基的纤维范畴 $\mathcal{E} \to \mathcal{B}$ 是"$\mathcal{B}$ 上的参数化族"——对每个基对象 $b \in \text{Ob}(\mathcal{B})$，有一族纤维对象 $\mathcal{E}_b$；态射被投影到基空间的态射上。

对于 Temp/RG 体系：

- **基范畴**：$\mathbf{Temp}$ 或 $\mathbf{RG}$（参数空间，对象为实数）
- **纤维**：$\mathbf{Sp}$ 的谱数据（每个参数点对应一个谱生成元 $A(T)$ 或 $A(\mu)$）
- **总空间**：谱丛 $B_T = \{(T, \{\lambda_i\})\}$ 和 $B_\mu = \{(\mu, \{\lambda_i\})\}$
- **投影**：$\pi_T(T, \{\lambda_i\}) = T$、$\pi_\mu(\mu, \{\lambda_i\}) = \mu$

### 3.2 为什么是纤维范畴而非子范畴

| 特征 | 子范畴 | 纤维范畴 |
|:----|:------|:--------|
| 对象关系 | "是一种" | "被参数化" |
| 典型例子 | 群是集合的子范畴 | 向量丛是底流形上的纤维范畴 |
| 映射方向 | 包含 $\hookrightarrow$ | 投影 $\to$ |
| 额外结构 | 无 | 纤维+截面+联络 |
| Temp/RG 适用性 | ❌ | ✅ |

**纤维范畴的自然类比**：向量丛 $E \to M$ 中，纤维 $E_x$ 是向量空间，基 $M$ 是流形。Temp/RG 中，纤维是 $\mathbf{Sp}$ 谱数据，基是参数空间 $\mathbf{Temp}$ 或 $\mathbf{RG}$。谱丛截面 $\sigma_\Delta$ 如同向量丛的截面——选择每个纤维中的一个特定元素。

## 4. UFPF 完整五层架构

### 4.1 架构图

```
                    ┌─────────────────────────────────────┐
                    │        纤维范畴层（上层）              │
                    │  $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$  ←$\hat{\mathcal{T}}_{\text{Riem}}$→  $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$  │
                    │    参数化系统族如何接近 $\partial\mathbf{Rec}_D$ 边界 │
                    └────────────────┬────────────────────┘
                                     │ $\pi_T$  $\pi_\mu$
                    ┌────────────────↓────────────────────┐
                    │        谱范畴层（中间层）              │
                    │  $\mathbf{Sp}$：$(\mathcal{H}, A, \sigma(A))$           │
                    │    所有谱数据的统一载体               │
                    └────────────────┬────────────────────┘
                                     │ $D$  $R$
                    ┌────────────────↓────────────────────┐
                    │        递归系统层（Paper I 底层）      │
                    │  $\mathbf{Rec}$：$(\mathcal{S}, \Phi, \mathcal{T}, \mathcal{M})$         │
                    │    IFS / Koopman / RG 流 / Kerr ...   │
                    └────────────────┬────────────────────┘
                                     │ $\mathcal{L}$  $\iota$
                    ┌────────────────↓────────────────────┐
                    │        静态嵌入层（Paper XIX 扩展）    │
                    │  $\mathbf{Rec}_{\text{id}} \cong \mathbf{Riemann}$               │
                    │    紧致流形 / 稳态时空 / 静态拓扑      │
                    └────────────────┬────────────────────┘
                                     │ $\mathcal{S}el$  $\mathcal{D}iss$
                    ┌────────────────↓────────────────────┐
                    │        随机嵌入层（Paper XIX 扩展）    │
                    │  $\Sigma$-$\mathbf{Rec}$：可数直和余完备化         │
                    │    白噪声 / $1/f$ 噪声 / 涨落-耗散    │
                    └─────────────────────────────────────┘
```

### 4.2 各层功能

| 层 | 名称 | 核心范畴/函子 | 物理意义 | 来源 |
|:-:|:----|:------------|:--------|:----|
| V | 纤维范畴 | $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$, $\hat{\mathcal{T}}_{\text{Riem}}$ | 参数化系统接近 $\partial\mathbf{Rec}_D$ 的方式 | 本笔记系列 |
| IV | 谱范畴 | $\mathbf{Sp}$, $D$-$\mathbf{Rec}$ 伴随 | 谱数据，连接上下层的桥梁 | Paper I |
| III | 递归系统 | $\mathbf{Rec}$, $D \dashv R$ | 有确定性演化的动力系统 | Paper I |
| II | 静态嵌入 | $\mathbf{Rec}_{\text{id}}$, $\mathcal{L} \dashv \iota$ | 无演化的静态拓扑 | Paper XIX |
| I | 随机嵌入 | $\Sigma$-$\mathbf{Rec}$, $\mathcal{S}el \dashv \mathcal{D}iss$ | 无确定性映射的纯随机系统 | Paper XIX |

### 4.3 为什么这样分层

1. **V 在 IV 之上**：$\mathbf{Sp}$ 提供纤维数据，$\mathbf{Bun}$ 构造参数化族——自然的上层结构
2. **IV 在 III 之上**：$\mathbf{Rec}$ 通过 $D$ 函子映射到 $\mathbf{Sp}$，$\mathbf{Sp}$ 是 $\mathbf{Rec}$ 的谱像
3. **III 在 II 之上**：$\mathbf{Rec}_{\text{id}} \hookrightarrow \mathbf{Rec}$ 是反射子范畴，$\mathcal{L}$ 遗忘动力学
4. **II 在 I 之上**：$\Sigma$-$\mathbf{Rec}$ 通过 $\mathcal{S}el \dashv \mathcal{D}iss$ 与 $\mathbf{Rec}$ 连接，但与 $\mathbf{Rec}_{\text{id}}$ 正交

每层之间通过伴随对或函子连接，构成完整的、可计算的转换路径。

## 5. 与 Paper XIX 相图的关系

### 5.1 现有 $(G, \eta)$ 二维相图

Paper XIX §13 以 $(G, \eta)$ 为坐标建立了系统的分类相图：

| 区域 | $G$ | $\eta$ | 范畴 | 实例 |
|:---:|:---:|:------:|:----|:----|
| I | $\neq 0$ | 0 | $\mathbf{Rec}$ | IFS, Koopman, Kerr |
| II | $\neq 0$ | $<\eta_c$ | 混合 $\mathbf{Rec}$ | 含噪系统 |
| III | 0 | 0 | $\mathbf{Rec}_{\text{id}}$ | 紧致流形 |
| IV | 0 | $>\eta_c$ | $\Sigma$-$\mathbf{Rec}$ | 白噪声 |

### 5.2 第三维度：$(T, \mu)$ 参数空间

Temp/RG 引入第三个独立维度：

| 维度 | 参数 | 范畴表示 | 物理量 |
|:----:|:----|:--------|:------|
| $G$ | 谱流生成元范数 | $\mathbf{Rec}$ / $\mathbf{Rec}_{\text{id}}$ | 动力学强度 |
| $\eta$ | 噪声强度 | $\mathbf{Rec}$ / $\Sigma$-$\mathbf{Rec}$ | 随机性程度 |
| $(T, \mu)$ | 温度-标度对偶 | $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ / $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ | 距 $\partial\mathbf{Rec}_D$ 的距离 |

三个维度的正交性：
- **$G$ 与 $(T, \mu)$ 正交**：即使是纯静态系统（$G=0$），其参数谱丛 $B_T$ 仍存在（如热平衡态在不同温度下的谱族）
- **$\eta$ 与 $(T, \mu)$ 正交**：即使是纯噪声系统（$\eta > \eta_c$），其噪声谱仍随温度变化
- **$G$ 与 $\eta$ 正交**：已有 Paper XIX §13 证明

### 5.3 $\partial\mathbf{Rec}_D$ 的统一角色

$\partial\mathbf{Rec}_D$ 边界在三个维度的解释：

| 维度 | $\partial\mathbf{Rec}_D$ 的像 | 物理意义 |
|:----:|:---------------------------|:--------|
| $\mathbf{Rec}$ 层 | 谱间隙消失的递归系统 | 临界动力系统 |
| $\mathbf{Temp}$ 空间 | $\{T_c\}$ | 临界温度 |
| $\mathbf{RG}$ 空间 | $\{\Lambda_{\text{QCD}}\}$ | 朗道极点 |
| 簇结构保持 | $\mathcal{T}(T_c) = \Lambda_{\text{QCD}}$ | 三种视角统一 |

## 6. 物理系统覆盖分析

### 6.1 覆盖条件

一个物理系统可纳入 Temp/RG 纤维范畴框架当且仅当满足以下 5 个必要条件：

| 条件 | 描述 | 来源 |
|:----:|:-----|:----|
| **T1** | 同时具有温度 $T$ 参数和能标 $\mu$ 参数（或类似的热力学参数与 RG 参数对偶） | $\mathcal{T}$ 函子的定义域与值域 |
| **T2** | 存在可定义的谱间隙 $\Delta\lambda_{\min}$，且在某个参数值处消失（$\partial\mathbf{Rec}_D$） | 谱丛截面构造 |
| **T3** | 谱流生成元 $G_{\text{th}}$、$G_{\text{RG}}$ 属于 $\mathfrak{so}(1,1)$ 或可嵌入 | Paper XVI §2.2 |
| **T4** | $T$ 空间与 $\mu$ 空间的态射结构同构（均为 $\mathbb{R}^+$ 乘法群） | $\mathbf{Temp} \cong \mathbf{RG}$ |
| **T5** | $\partial\mathbf{Rec}_D$ 在 $T$ 空间和 $\mu$ 空间均为单点集（或有限点集） | 谱粘合临界嵌入 |

### 6.2 适用性矩阵

| 物理系统 | T1 | T2 | T3 | T4 | T5 | 等级 | 说明 |
|:---------|:--:|:--:|:--:|:--:|:--:|:----:|:-----|
| **QCD 禁闭-退禁闭** | ✅ | ✅ | ✅ | ✅ | ✅ | **完全覆盖** | $a=0.729$（0.1%偏差），路径 A/B/C 已完备 |
| **BCS 超导** | ✅ | ✅ | ✅ | ✅ | ✅ | **即用** | 需替换 $d_q \to d_{\text{BCS}}$ |
| **流变学剪切稀化/稠化** | ⚠️ | ✅ | ✅ | ✅ | ✅ | **强覆盖** | 应变率 $\dot\gamma$ 替代 $T$，需范畴名称统一 |
| **Hawking-Page 相变** | ✅ | ✅ | ✅ | ✅ | ✅ | **强覆盖** | $T_H \leftrightarrow M^{-1}$，有 Paper XII 基础 |
| **$^4$He $\lambda$ 相变** | ✅ | ✅ | ✅ | ✅ | ⚠️ | **部分** | 缺 RG 对偶 $\Lambda_{\text{He}}$ |
| **超流 $^3$He** | ✅ | ✅ | ✅ | ✅ | ⚠️ | **部分** | 多序参量致 $\partial\mathbf{Rec}_D$ 多分支 |
| **量子相变 (T=0)** | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | **弱** | 缺 $T$ 参数，需 $\mathbf{Crit}$ 范畴扩展 |
| **cuprate 高温超导** | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | **探索** | 赝能隙使 $\partial\mathbf{Rec}_D$ 为区间 |
| **Bose-Einstein 凝聚** | ✅ | ✅ | ✅ | ✅ | ⚠️ | **部分** | RG 对偶弱 |
| **量子 Hall 效应** | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | **弱** | 填充因子 $\nu$ 替代 $T$ |
| **铁磁-顺磁相变** | ✅ | ✅ | ✅ | ✅ | ⚠️ | **部分** | 缺 RG 标度对偶 |
| **极端黑洞极限** | ✅ | ✅ | ⚠️ | ✅ | ✅ | **部分** | $G_{\text{th}}$ 代数需曲率修正 |

### 6.3 推荐扩展优先级

| 优先级 | 系统 | 理由 | 工作预计 |
|:-----:|:-----|:-----|:--------|
| **P0** | BCS 超导 | 框架即用，只需替换自由度参数 | 1 笔记 + 1 脚本 |
| **P1** | Hawking-Page 相变 | 有 Paper XII 基础 | 1 笔记 |
| **P2** | 流变学严格化 | 需处理 $\mathbf{Rate}$ 范畴与 $\mathbf{Temp}$ 的关系 | 范畴论扩展 |
| **P3** | $^4$He $\lambda$ 相变 | 需解决 RG 对偶缺失 | 探索性 |
| **P4** | cuprate 分布论扩展 | 需框架本身扩展以处理"宽化临界区" | 框架级扩展 |

## 7. 与已有成果的整合关系

### 7.1 各文件角色

| 文件 | 定位 | 互引关系 |
|:----|:----|:--------|
| `spectral_T_category.md` | $\mathbf{Temp}$ 范畴 + 函子 $\mathcal{T}$ 的构建 | 本笔记的前置基础 |
| `spectral_T_category_riemann.md` | 谱纤维丛上的 Riemann 函子 $\hat{\mathcal{T}}_{\text{Riem}}$ | 依赖 spectral_T_category.md |
| `spectral_Riem_functoriality.md` | 函子性证明 + 自然变换 + 2-函子 | 依赖 spectral_T_category_riemann.md |
| `spectral_bundle_sections.md` | 谱丛截面 $\sigma_\Delta$ 显式构造 | 依赖 spectral_T_category_riemann.md |
| **本笔记** | 架构定位 + 物理系统覆盖分析 | 汇总以上全部 |

### 7.2 论文整合状态

Paper I §1.3 已新增跨论文定位段落（v2.45）。Paper XIX §17 已完整新增纤维范畴架构章节（v0.8）。当前 Temp/RG 体系以研究笔记形式存在，推荐采用以下策略：

1. **近期**：随着进一步的物理系统验证（如 BCS 试点），以 Paper XIX 增补形式发布（作为 §17 的丰富）
2. **中期**：若扩展到 3+ 个独立物理系统，考虑独立 Paper XXI
3. **长期**：若扩展到 5+ 个系统且包含完整的 Grothendieck 纤维范畴形式化，序列号可提升为早期论文编号

## 8. 结论

1. **架构定位**：Temp/RG **不是** $\mathbf{Rec}$ 的子范畴，而是 $\mathbf{Sp}$ 上的纤维范畴扩展
2. **架构层次**：UFPF 框架分为五层——$\mathbf{Bun}$（纤维范畴）$\supset$ $\mathbf{Sp}$（谱）$\supset$ $\mathbf{Rec}$（递归）$\supset$ $\mathbf{Rec}_{\text{id}}$（静态）$\supset$ $\Sigma$-$\mathbf{Rec}$（随机）
3. **维度扩展**：Temp/RG 为 $(G, \eta)$ 二维相图引入第三个维度——温度-标度对偶 $(T, \mu)$
4. **覆盖范围**：QCD 已完全验证，BCS 超导和 Hawking-Page 相变是最高优先级的扩展目标
5. **正交兼容**：Temp/RG 与 Paper I 底层 + Paper XIX 扩展层正交——Paper XIX 处理"横切"转化（动态↔静态↔随机），Temp/RG 处理"纵贯"参数化（连续温度族），两者结合构成 UFPF 的完整架构

---

**版本记录**：

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| v0.1 | 2026-07-22 | 初版：架构定位分析、物理系统覆盖矩阵、UFPF 五层架构图 |
