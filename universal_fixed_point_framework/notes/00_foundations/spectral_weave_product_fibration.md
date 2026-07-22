# 谱编织乘积基 $\mathbf{Temp} \times \mathbf{RG}$ 的 Grothendieck 纤维化

**版本**：v0.1（2026-07-22）

**摘要**：本笔记将温度-标度对偶 $(T,\mu)$ 提升为乘积基 $\mathbf{Temp} \times \mathbf{RG}$ 上的 Grothendieck 纤维范畴，构造谱编织总丛 $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec})$。核心成果包括：(1) 乘积基上的投影 $\pi_{T,\mu}$ 是分裂 Grothendieck 纤维化；(2) 沿 $\partial\mathbf{Rec}_D$ 的粘合条件 $S_{\text{spec}}(\Lambda_{\text{QCD}}, 0) = S_{\text{spec}}(0, T_c)$ 精确化为拉回方图；(3) $\mathbf{Bun}(\mathbf{Temp})$ 和 $\mathbf{Bun}(\mathbf{RG})$ 作为两坐标方向的拉回丛出现。

**前置依赖**：[`spectral_Grothendieck_fibration.md`](spectral_Grothendieck_fibration.md)（$\pi_T$/$\pi_\mu$ 模板）、[`spectral_BCS_weave.md`](../../notes/02_superconductivity/spectral_BCS_weave.md)（谱编织物理）、`TempRGFiber.lean`（形式化基础）。

---

## 1. 乘积基范畴 $\mathbf{Temp} \times \mathbf{RG}$

**定义 1.1**（乘积基）。$\mathbf{Temp} \times \mathbf{RG}$ 是乘积范畴：对象为 $(T, \mu)$（$T > 0$，$\mu > 0$），态射为 $(f, g): (T_1, \mu_1) \to (T_2, \mu_2)$，其中 $f: T_1 \to T_2$ 是温度膨胀，$g: \mu_1 \to \mu_2$ 是标度膨胀。

**注 1.1**。$\mathbf{Temp} \times \mathbf{RG}$ 的两个坐标方向分别由 $\pi_T$ 和 $\pi_\mu$ 的已有纤维结构覆盖。乘积基的主要新要素是沿 $\partial\mathbf{Rec}_D$ 的**对角粘合条件**。

---

## 2. 乘积谱丛 $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec})$

### 2.1 总范畴

**定义 2.1**。$\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec})$ 的对象为 $((T, \mu), \{\lambda_i(T, \mu)\})$，态射为 $(f_{\text{temp}}, g_{\text{RG}}, \phi_{\text{spec}})$。

### 2.2 拉回丛

**命题 2.1**（坐标拉回）。存在拉回函子：

$$\iota_T^*: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec}) \to \mathbf{Bun}(\mathbf{Temp}, \mathbf{Spec})$$
$$\iota_\mu^*: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec}) \to \mathbf{Bun}(\mathbf{RG}, \mathbf{Spec})$$

分别沿 $\iota_T: \mathbf{Temp} \hookrightarrow \mathbf{Temp} \times \mathbf{RG}$（固定 $\mu = \mu_0$）和 $\iota_\mu: \mathbf{RG} \hookrightarrow \mathbf{Temp} \times \mathbf{RG}$（固定 $T = T_0$）。

---

## 3. 谱编织约束与粘合

### 3.1 $\partial\mathbf{Rec}_D$ 粘合条件

谱编织约束是沿 $\partial\mathbf{Rec}_D$ 的粘合条件：

$$S_{\text{spec}}(\Lambda_{\text{QCD}}, 0) = S_{\text{spec}}(0, T_c)$$

在纤维范畴语言中，这意味着以下拉回方图交换：

$$
\begin{CD}
\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec}) @>{\iota_\mu^*}>> \mathbf{Bun}(\mathbf{RG}, \mathbf{Spec}) \\
@V{\iota_T^*}VV @VV{S_\Delta^{(\text{QCD})}}V \\
\mathbf{Bun}(\mathbf{Temp}, \mathbf{Spec}) @>>{S_\Delta^{(\text{BCS})}}> \mathbf{Spec}
\end{CD}
$$

其中 $S_{\text{spec}}$ 是谱编织截面。

### 3.2 与 $\partial\mathbf{Rec}_D$ 的关系

物理上，$\partial\mathbf{Rec}_D$ 是退化边界——谱间隙在该边界上闭合。温度-标度对偶 $(T, \mu)$ 在该边界上的截面退化为同一物理点：

$$(T_c^{\text{QCD}}, 0) \sim (0, \Lambda_{\text{QCD}}) \in \partial\mathbf{Rec}_D$$

---

## 4. Lean 4 形式化方案

### 4.1 复用组件

| 组件 | 来源 | 角色 |
|:----|:-----|:-----|
| `TempObj`, `RGObj` | `TempRGFiber.lean` | 基空间因子 |
| `CartesianLiftData` | `TempRGFiber.lean` | 乘积基的纤维化 |
| `QCDSection_cl17` | `TempRGFiber.lean` | QCD 截面 |
| `HPSection_cl17` | `TempRGFiber.lean` | HP 截面 |

### 4.2 新建内容

| 模块 | 内容 |
|:----|:-----|
| `ProdBase` | $\mathbf{Temp} \times \mathbf{RG}$ 乘积范畴 |
| `WeaveFiber` | $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Spec})$ 总范畴 |
| `WeaveGluing` | $\partial\mathbf{Rec}_D$ 粘合条件 |
| `PullbackFunctors` | 坐标拉回函子 $\iota_T^*$, $\iota_\mu^*$ |

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.1** | **2026-07-22** | 初始版本：乘积基定义；谱编织总范畴；$\partial\mathbf{Rec}_D$ 粘合条件；拉回方图；Lean 形式化方案 |
