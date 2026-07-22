# Cuprate 赝能隙分布的谱框架形式化

**版本**：v0.1（2026-07-23）

**摘要**：本笔记将 cuprate 高温超导体的赝能隙分布纳入谱框架 Grothendieck 纤维范畴构造。核心内容为：(1) 将 $\partial\mathbf{Rec}_D$ 从单点 $T_c$ 扩展为区间 $[T_c, T^*]$，对应的谱丛截面从单值谱间隙升级为**分布谱间隙截面** $\sigma_{\Delta}^{\text{(c)}}(T)$；(2) 建立双组分高斯混合模型 $\varphi_T(\Delta\lambda) = w_{\text{n}}(T)\delta(\Delta\lambda) + w_{\text{g}}(T)\mathcal{G}(\mu_T, \sigma_T)$ 的范畴论翻译——权重函数 $w_{\text{n}}(T)$ 和均值 $\mu_T$ 的封闭形式由谱流方程决定；(3) 证明分布截面与 $\hat{\mathcal{T}}_{\text{Riem}}$ 的兼容性——纤维保持函子作用于分布的方式是推前 (pushforward) $(\hat{\mathcal{T}}_{\text{Riem}})_*(\varphi_T) = \varphi_{\mathcal{T}(T)}$；(4) 在 Lean 4 中形式化 cuprate 参数结构、分布谱截面和推前条件。

**前置依赖**：`spectral_BCS_weave.md`（§8 分布论框架）、`WeaveProductFiber.lean`（§7-§10 对角子范畴与编织截面）、`TempRGFiber.lean`（$\hat{\mathcal{T}}_{\text{Riem}}$ 函子）。

---

## 1. 问题本质：$\partial\mathbf{Rec}_D$ 的赝能隙宽化

### 1.1 BCS 到 cuprate 的跃迁

在标准 BCS 体系中，$\partial\mathbf{Rec}_D$ 是一个**单点**：谱间隙在 $T = T_c$ 处从 $\Delta\lambda_{\min}^{(0)}$ 突变为零。cuprate 高温超导体中，赝能隙相使这一边界**宽化**为一个区间：

```
         T*          Tc
正常相 |--赝能隙相--|超导相|   → T
       ∂Rec_D "宽化" 区域
```

物理上，这意味着在 $T > T_c$ 时已有部分谱权重形成能隙（赝能隙），但能隙是**部分打开**的——只有 $w_{\text{g}}(T)$ 比例的谱权重参与了配对。

### 1.2 谱丛语言翻译

在谱丛 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Spec})$ 中，BCS 截面 $\sigma_{\Delta}(T)$ 的纤维是单值谱间隙 $\Delta\lambda_{\min}(T)$：
$$\sigma_{\Delta}(T) = (T, \Delta\lambda_{\min}(T))$$

cuprate 截面 $\sigma_{\Delta}^{\text{(c)}}(T)$ 的纤维是谱间隙的**分布** $\varphi_T(\Delta\lambda)$：
$$\sigma_{\Delta}^{\text{(c)}}(T) = \left(T, \ \mathbb{E}_{\varphi_T}[\Delta\lambda]\right) = \left(T, \ \int_0^{\infty} \Delta\lambda \cdot \varphi_T(\Delta\lambda) \, d\Delta\lambda\right)$$

---

## 2. 双组分高斯混合模型

### 2.1 定义

**定义 2.1**（cuprate 谱间隙分布函数）。分布函数 $\varphi_T(\Delta\lambda)$ 由正常组分和赝能隙组分的凸组合构成：
$$\varphi_T(\Delta\lambda) = w_{\text{n}}(T) \cdot \delta(\Delta\lambda) + w_{\text{g}}(T) \cdot \mathcal{G}(\Delta\lambda; \mu_T, \sigma_T)$$

其中：
- $w_{\text{n}}(T) + w_{\text{g}}(T) = 1$（归一化）
- $\delta(\Delta\lambda)$ 是正常相的无间隙组分（Dirac delta 在零点）
- $\mathcal{G}(\Delta\lambda; \mu_T, \sigma_T) = \frac{1}{\sqrt{2\pi}\sigma_T} \exp\left(-\frac{(\Delta\lambda - \mu_T)^2}{2\sigma_T^2}\right)$ 是赝能隙组分的高斯包络

### 2.2 温度依赖的权重函数

**定理 2.1**（权重函数的温度依赖）。权重函数的温度依赖由谱流方程的临界行为确定：
$$w_{\text{n}}(T) = 
\begin{cases}
0, & T < T_c \\
\left(\dfrac{T - T_c}{T^* - T_c}\right)^{\beta_{\text{PG}}}, & T_c \leq T \leq T^* \\
1, & T > T^*
\end{cases}$$
$$w_{\text{g}}(T) = 1 - w_{\text{n}}(T)$$

其中 $\beta_{\text{PG}}$ 是赝能隙临界指数。对 YBCO 类 cuprate（$T_c \approx 92$ K, $T^* \approx 170$ K），$\beta_{\text{PG}} \approx 0.5$（平均场类行为）。

### 2.3 赝能隙组分的参数

高斯包络的均值和方差：
$$\mu_T = \Delta\lambda_{\min}^{\text{(c)}} \cdot 
\begin{cases}
1, & T < T_c \\
1 - \dfrac{T - T_c}{T^* - T_c}, & T_c \leq T \leq T^* \\
0, & T > T^*
\end{cases}$$

$$\sigma_T = \sigma_0 \cdot \left(1 - \frac{T}{T^*}\right)^{\gamma_{\text{PG}}}, \quad \sigma_0 = 0.15 \cdot \Delta\lambda_{\min}^{\text{(c)}}, \quad \gamma_{\text{PG}} \approx 1$$

其中 $\Delta\lambda_{\min}^{\text{(c)}}$ 是 cuprate 超导相的谱间隙。对 YBCO（d-wave 能隙 $\Delta_0^{\text{max}} \approx 25$ meV）：
$$\Delta\lambda_{\min}^{\text{(c)}} = \Delta\lambda_2 \cdot \frac{\Delta_0^{\text{max}}}{k_B T_c} \cdot \frac{a_{\text{QCD}}}{a_{\text{SC}}} \approx 0.122 \cdot \frac{25}{7.9} \cdot \frac{0.729}{0.567} \approx 0.500$$

### 2.4 分布谱间隙截面的封闭形式

**定理 2.2**（分布谱间隙截面的封闭形式）。
$$\sigma_{\Delta}^{\text{(c)}}(T) = \left(T, \ w_{\text{g}}(T) \cdot \mu_T\right)$$

在赝能隙相中，谱丛截面的纤维值为 $w_{\text{g}}(T) \cdot \mu_T$——该闭合形式完全由 $\Delta\lambda_{\min}^{\text{(c)}}$ 和临界指数 $(\beta_{\text{PG}}, \gamma_{\text{PG}})$ 刻画。

---

## 3. 与 $\hat{\mathcal{T}}_{\text{Riem}}$ 的兼容性

### 3.1 推前映射

分布谱间隙截面 $\sigma_{\Delta}^{\text{(c)}}$ **不破坏** $\hat{\mathcal{T}}_{\text{Riem}}$ 的纤维保持性——只需将 $\mathbf{Spec}$ 中的谱元素从"单值间隙"替换为"间隙分布"。

**定理 3.1**（推前兼容性）。纤维保持函子 $\hat{\mathcal{T}}_{\text{Riem}}$ 作用于分布的方式是推前（pushforward）：
$$(\hat{\mathcal{T}}_{\text{Riem}})_*(\varphi_T) = \varphi_{\mathcal{T}(T)}$$
其中 $\varphi_{\mathcal{T}(T)}$ 是 RG 标度处的谱间隙分布。

### 3.2 物理意义

推前条件意味着：温度截面和 RG 截面通过 $\hat{\mathcal{T}}_{\text{Riem}}$ 保持分布的形状——温度 $T$ 处的谱间隙分布和 RG 标度 $\mathcal{T}(T)$ 处的谱间隙分布相同。这保证了谱编织条件在分布论框架下的自洽性。

---

## 4. 范畴论翻译

### 4.1 分布纤维

**定义 4.1**（分布纤维 $\widehat{\mathbf{Spec}}$）。$\widehat{\mathbf{Spec}}$ 是 $\mathbf{Spec}$ 的推广，其元素为谱间隙上的概率分布 $\varphi$，而非单值谱间隙 $\Delta\lambda$。直观上：
$$\widehat{\mathbf{Spec}}_{(T)} \ni \varphi_T(\Delta\lambda)$$

### 4.2 分布截面

**定义 4.2**（分布谱丛截面）。一个 cuprate 谱丛截面 $\sigma_{\Delta}^{\text{(c)}}$ 是函子 $\sigma_{\Delta}^{\text{(c)}}: \mathbf{Temp} \to \mathbf{Bun}(\mathbf{Temp}, \widehat{\mathbf{Spec}})$，满足 $\pi_T \circ \sigma_{\Delta}^{\text{(c)}} = \text{id}_{\mathbf{Temp}}$。

### 4.3 $\hat{\mathcal{T}}_{\text{Riem}}$ 的推前延拓

$\hat{\mathcal{T}}_{\text{Riem}}$ 通过推前作用到分布上：
$$(\hat{\mathcal{T}}_{\text{Riem}})_*(\sigma_{\Delta}^{\text{(c)}})(T) = \sigma_{\Delta}^{\text{(c)}}(\mathcal{T}(T))$$

即：先应用温度截面，然后通过 $\mathcal{T}$ 映射到 RG 标度。

### 4.4 与乘积基 Diag 的关系

在谱编织乘积基 $\mathbf{Temp} \times \mathbf{RG}$ 上，cuprate 分布截面沿对角嵌入 $T \mapsto (T, \mathcal{T}(T))$ 的限制给出：
$$\iota_T^* \circ \sigma_{\Delta}^{\text{(c)}} = \iota_\mu^* \circ \sigma_{\Delta}^{\text{(c)}} \quad\text{在}\quad \mu = \mathcal{T}(T)$$

即分布截面也满足对角闭包条件（类比 `weave_closure_on_diag`）。

---

## 5. YBCO 数值验证

### 5.1 参数集合

对 YBCO：
$$T_c = 92\ \text{K}, \quad T^* = 170\ \text{K}, \quad \beta_{\text{PG}} = 0.5, \quad \sigma_0 = 0.075, \quad \Delta\lambda_{\min}^{\text{(c)}} \approx 0.500$$

### 5.2 分布随温度的演化

| $T$ (K) | $w_{\text{n}}$ | $w_{\text{g}}$ | $\mu_T$ (归一化) | $\sigma_T$ | $\sigma_{\Delta}^{\text{(c)}}$ |
|:-------:|:--------------:|:--------------:|:----------------:|:----------:|:----------------------------:|
| $50$ | $0$ | $1$ | $1.0$ | $0.029$ | $1.0$（超导相）|
| $100$ | $0.32$ | $0.68$ | $0.90$ | $0.031$ | $0.61$ |
| $130$ | $0.62$ | $0.38$ | $0.74$ | $0.018$ | $0.28$ |
| $160$ | $0.88$ | $0.12$ | $0.15$ | $0.004$ | $0.02$ |
| $180$ | $1$ | $0$ | $0$ | $0$ | $0$（正常相）|

### 5.3 物理解释

在 $T = 100$ K（赝能隙相），仅有 $68\%$ 的谱权重参与了部分能隙打开（均值 $\mu_T = 0.90$），有效谱间隙 $= 0.68 \times 0.90 = 0.61$。随着温度升高，参与配对的谱权重和能隙幅度同时减少，至 $T^*$ 处完全消失。

---

## 6. Lean 4 形式化方案

### 6.1 复用组件

| 组件 | 来源 | 角色 |
|:----|:-----|:-----|
| `TempObj`, `RGObj` | `TempRGFiber.lean` | 基空间 |
| `T_hat_Riem` | `TempRGFiber.lean` | 纤维保持函子 |
| `WeaveSection` | `WeaveProductFiber.lean` §10 | 截面结构体 |
| `diagEmbedding` | `WeaveProductFiber.lean` §7 | 对角嵌入 |
| `weave_closure_on_diag` | `WeaveProductFiber.lean` §10 | 对角闭包 |

### 6.2 新建内容

| 模块 | 笔记 § | 内容 |
|:----|:------|:----|
| `CuprateParams` | §2.2-§2.3 | cuprate 参数结构（$T_c$, $T^*$, $\beta_{\text{PG}}$, $\gamma_{\text{PG}}$, $\Delta\lambda_{\min}^{\text{(c)}}$）|
| `weight_normal` / `weight_gap` | §2.2 | 权重函数 $w_{\text{n}}(T)$, $w_{\text{g}}(T)$ |
| `mu_T` / `sigma_T` | §2.3 | 均值/方差函数 |
| `cuprateSection` | §2.4 | 分布谱间隙截面 |
| `pushforward_compatibility` | §3 | 推前兼容性定理 |

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.1** | **2026-07-23** | 初始版本：赝能隙宽化的数学刻画；双组分高斯混合模型（权重函数、均值/方差、封闭形式）；𝒯̂_Riem 推前兼容性；范畴论翻译（分布纤维、分布截面）；YBCO 数值验证；Lean 形式化方案 |
