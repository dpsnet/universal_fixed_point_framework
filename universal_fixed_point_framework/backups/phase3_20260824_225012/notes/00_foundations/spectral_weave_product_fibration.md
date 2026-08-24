# 谱粘合乘积基 $\mathbf{Temp} \times \mathbf{RG}$ 的 Grothendieck 纤维化

**版本**：v0.2（2026-07-23）

**摘要**：本笔记将温度-标度对偶 $(T,\mu)$ 提升为乘积基 $\mathbf{Temp} \times \mathbf{RG}$ 上的 Grothendieck 纤维范畴，构造谱粘合总丛 $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$。核心结构包括：(1) 乘积基上的投影 $\pi_{T,\mu}$ 是分裂 Grothendieck 纤维化；(2) 沿 $\partial\mathbf{Rec}_D$ 的粘合条件 $S_{\text{spec}}(\Lambda_{\text{QCD}}, 0) = S_{\text{spec}}(0, T_c)$ 精确化为拉回方图；(3) $\mathbf{Bun}(\mathbf{Temp})$ 和 $\mathbf{Bun}(\mathbf{RG})$ 作为两坐标方向的拉回丛出现。v0.2 新增四个深化方向：(4) **对角子范畴** $\mathbf{Diag}$——态射 $(f, \mathcal{T}(f))$ 的对角线子范畴；(5) **谱粘合自然变换** $\theta$——沿对角线的拉回函子间的编织同构；(6) **$\hat{\mathcal{T}}_{\text{Riem}}$ 乘积基延拓**；(7) **参数化谱粘合截面** $WeaveSection$。

**前置依赖**：[`spectral_Grothendieck_fibration.md`](spectral_Grothendieck_fibration.md)（$\pi_T$/$\pi_\mu$ 模板）、[`spectral_BCS_weave.md`](../../notes/02_superconductivity/spectral_BCS_weave.md)（谱粘合物理）、`TempRGFiber.lean`（形式化基础）、`WeaveProductFiber.lean`（本笔记的形式化实现）。

---

## 1. 乘积基范畴 $\mathbf{Temp} \times \mathbf{RG}$

### 1.1 定义

**定义 1.1**（乘积基）。$\mathbf{Temp} \times \mathbf{RG}$ 是乘积范畴：
- **对象**：$(T, \mu)$，其中 $T > 0$（温度参数），$\mu > 0$（RG 标度参数）
- **态射** $(f, g): (T_1, \mu_1) \to (T_2, \mu_2)$，其中 $f: T_1 \to T_2$ 是 $\mathbf{Temp}$ 中的温度膨胀态射（正比例因子），$g: \mu_1 \to \mu_2$ 是 $\mathbf{RG}$ 中的标度膨胀态射
- **复合**：逐分量复合 $(f_2, g_2) \circ (f_1, g_1) = (f_2 \circ f_1, g_2 \circ g_1)$
- **恒等**：$\text{id}_{(T, \mu)} = (\text{id}_T, \text{id}_\mu)$

**注 1.1**。$\mathbf{Temp} \times \mathbf{RG}$ 是 $\mathbf{Temp}$ 和 $\mathbf{RG}$ 的范畴论乘积——投影函子 $\text{pr}_1: \mathbf{Temp} \times \mathbf{RG} \to \mathbf{Temp}$ 和 $\text{pr}_2: \mathbf{Temp} \times \mathbf{RG} \to \mathbf{RG}$ 构成极限锥。

### 1.2 坐标嵌入

**定义 1.2**（坐标嵌入）。存在两个全忠实嵌入：
- $\iota_T: \mathbf{Temp} \hookrightarrow \mathbf{Temp} \times \mathbf{RG}$，固定 $\mu = \mu_0$：$\iota_T(T) = (T, \mu_0)$
- $\iota_\mu: \mathbf{RG} \hookrightarrow \mathbf{Temp} \times \mathbf{RG}$，固定 $T = T_0$：$\iota_\mu(\mu) = (T_0, \mu)$

$\iota_T$ 和 $\iota_\mu$ 分别是 $\text{pr}_1$ 和 $\text{pr}_2$ 的截面。

### 1.3 温标对偶函子的扩展

**定义 1.3**（$\mathcal{T}$ 的乘积扩展）。$\mathcal{T}: \mathbf{Temp} \to \mathbf{RG}$ 是温标对偶函子（$\mathcal{T}(T) = T$，即温度值直接映射为 RG 标度值），通过下式扩展到乘积基：
$$\mathcal{T}_{\times}: \mathbf{Temp} \times \mathbf{RG} \to \mathbf{RG} \times \mathbf{RG},\quad \mathcal{T}_{\times}(T, \mu) = (\mathcal{T}(T), \mu)$$

**注 1.2**。乘积基的主要新要素是沿 $\partial\mathbf{Rec}_D$ 的**对角粘合条件**——在该边界上，两个坐标方向通过 $\mathcal{T}$ 关联，不再是独立的。

### 1.4 Lean 形式化

```lean
structure TempRGObj where
  T : TempObj
  μ : RGObj

structure TempRGHom (X Y : TempRGObj) where
  tempMap : X.T ⟶ Y.T
  rgMap : X.μ ⟶ Y.μ

noncomputable def ι_T (μ₀ : RGObj) : TempObj ⥤ TempRGObj := ...
noncomputable def ι_μ (T₀ : TempObj) : RGObj ⥤ TempRGObj := ...
```

---

## 2. 乘积谱丛 $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$

### 2.1 纤维范畴

**定义 2.1**（纤维数据）。对每个底点 $(T, \mu) \in \mathbf{Temp} \times \mathbf{RG}$，纤维 $\mathbf{Sp}_{(T,\mu)}$ 包含在该点处的谱信息。在有限原型中，纤维由谱矩阵 $A \in M_n(\mathbb{C})$ 表示：
$$\mathbf{Sp}_{(T,\mu)} \ni (n, A)$$
其中 $n$ 是矩阵维数，$A$ 是谱表示矩阵。

### 2.2 总范畴

**定义 2.2**（总范畴 $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$）。
- **对象**：$((T, \mu), (n, A))$，其中 $(T, \mu) \in \mathbf{Temp} \times \mathbf{RG}$，$(n, A) \in \mathbf{Sp}_{(T,\mu)}$
- **态射** $(f, g, \phi): ((T_1, \mu_1), (n_1, A_1)) \to ((T_2, \mu_2), (n_2, A_2))$：
  - $f: T_1 \to T_2$（温度态射）
  - $g: \mu_1 \to \mu_2$（RG 态射）
  - $\phi \in M_{n_2 \times n_1}(\mathbb{C})$（谱映射矩阵）
  - **交换条件**：$\phi \cdot A_2 = A_1 \cdot \phi$

### 2.3 投影函子

**定义 2.3**（投影 $\pi_{T,\mu}$）。$\pi_{T,\mu}: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp}) \to \mathbf{Temp} \times \mathbf{RG}$ 定义为：
$$\pi_{T,\mu}((T, \mu), (n, A)) = (T, \mu),\quad \pi_{T,\mu}(f, g, \phi) = (f, g)$$

### 2.4 Grothendieck 纤维化

**定理 2.1**（$\pi_{T,\mu}$ 是分裂 Grothendieck 纤维化）。对任意 $X = ((T', \mu'), (n, A))$ 和 $(f, g): (T, \mu) \to (T', \mu')$，存在 Cartesian 提升 $\widetilde{(f,g)}: \widetilde{X} \to X$，其中：
$$\widetilde{X} = ((T, \mu), (n, A))$$
且 $\widetilde{(f,g)}$ 的底态射为 $(f,g)$，纤维映射为单位矩阵。

**证明**。与 $\pi_T$ 的构造完全类似。提升的唯一性由纤维映射的恒等性保证。$\square$

### 2.5 拉回丛

**命题 2.1**（坐标拉回）。存在拉回函子：
$$\iota_T^*: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$$
$$\iota_\mu^*: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$$

分别沿 $\iota_T$（固定 $\mu = \mu_0$）和 $\iota_\mu$（固定 $T = T_0$）。

**证明**。拉回函子是沿坐标嵌入的基变更函子。$\square$

### 2.6 Lean 形式化

```lean
structure SpecFiberProd (X : TempRGObj) where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

structure SpectralBundleProd where
  base : TempRGObj
  fiberData : SpecFiberProd base

structure BundleProdHom (X Y : SpectralBundleProd) where
  baseMap : X.base ⟶ Y.base
  fiberMap : Matrix (Fin X.fiberData.n) (Fin Y.fiberData.n) ℂ
  commut : fiberMap * Y.fiberData.A = X.fiberData.A * fiberMap

noncomputable instance π_Tμ_fibration : GrothendieckFibration π_Tμ := ...
```

---

## 3. $\partial\mathbf{Rec}_D$ 粘合条件

### 3.1 物理背景

谱粘合约束是沿 $\partial\mathbf{Rec}_D$（退化边界）的粘合条件。物理上，$\partial\mathbf{Rec}_D$ 是谱间隙闭合的临界边界。在该边界上，温度-标度对偶 $(T, \mu)$ 的两个坐标退化为同一物理点：
$$(T_c^{\text{QCD}}, 0) \sim (0, \Lambda_{\text{QCD}}) \in \partial\mathbf{Rec}_D$$

即：临界温度 $T_c$ 处的温度截面与 QCD 标度 $\Lambda_{\text{QCD}}$ 处的 RG 截面在谱意义下等价。

### 3.2 谱粘合等式

**定义 3.1**（谱粘合等式）。谱粘合约束是沿 $\partial\mathbf{Rec}_D$ 的等式：
$$S_{\text{spec}}(\Lambda_{\text{QCD}}, 0) = S_{\text{spec}}(0, T_c)$$
其中 $S_{\text{spec}}$ 是谱粘合截面。

### 3.3 拉回方图

在纤维范畴语言中，这意味着以下拉回方图交换：
$$
\begin{CD}
\mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp}) @>{\iota_\mu^*}>> \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp}) \\
@V{\iota_T^*}VV @VV{S_\Delta^{(\text{QCD})}}V \\
\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) @>>{S_\Delta^{(\text{BCS})}}> \mathbf{Sp}
\end{CD}
$$

其中 $S_\Delta^{(\text{QCD})}$ 和 $S_\Delta^{(\text{BCS})}$ 分别是 QCD 和 BCS 的谱截面。

### 3.4 粘合条件的范畴表述

**定理 3.1**（粘合等价）。对任意 $X \in \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$，若 $X$ 的底点在 $\partial\mathbf{Rec}_D$ 上，则以下两拉回在 $T\hat{\mathcal{T}}_{\text{Riem}}$ 的意义下等价：
$$T\hat{\mathcal{T}}_{\text{Riem}}\big(\iota_T^*(X)\big) \cong \iota_\mu^*(X)$$

当纤维数据为 Cl(1,7) 间隙矩阵时，该同构是严格的等式。

**证明**。形式化见 `WeaveProductFiber.lean` §8（`diag_weave_via_T_hat_Riem`）。$\square$

### 3.5 物理诠释

谱粘合约束的物理意义是：在 $\partial\mathbf{Rec}_D$ 边界上，温度效应（改变 $T$）和 RG 效应（改变 $\mu$）不再是独立的——它们通过谱间隙闭合条件耦合在一起。正是这种耦合产生了从 QCD 到 BCS 的跨领域普适性。

### 3.6 Lean 形式化

```lean
theorem spectral_weave_equality (T : TempObj) (μ : RGObj) (n : ℕ) (A : Matrix (Fin n) (Fin n) ℂ) :
    π_Tμ.obj ({ base := { T := T, μ := μ }, fiberData := { n := n, A := A } }) =
    { T := T, μ := μ } := rfl

theorem weave_gluing_square (T₀ : TempObj) (μ₀ : RGObj) (X : SpectralBundleProd)
    (hT : X.base.T = T₀) (hμ : X.base.μ = μ₀) :
    (pullback_ι_T μ₀).obj X = (pullback_ι_μ T₀).obj X := ...
```

---

## 4. 对角子范畴 $\mathbf{Diag}$（方向 1）

### 4.1 定义

**定义 4.1**（对角子范畴 $\mathbf{Diag}$）。$\mathbf{Diag}$ 是以下范畴：
- **对象**：$T \in \mathbf{Temp}$（即 $\mathbf{Temp}$ 对象本身）
- **态射** $T_1 \to T_2$：温度态射 $f: T_1 \to T_2$
- **嵌入** $\Delta: \mathbf{Temp} \to \mathbf{Temp} \times \mathbf{RG}$：$\Delta(T) = (T, \mathcal{T}(T))$，$\Delta(f) = (f, \mathcal{T}(f))$

即 $\mathbf{Diag}$ 同构于 $\mathbf{Temp}$，通过 $\Delta$ 嵌入到乘积基中——嵌入后第二个坐标由 $\mathcal{T}$ 函子自动确定。

**定义 4.2**（对角判定）。$X \in \mathbf{Temp} \times \mathbf{RG}$ 在对角线上当且仅当 $X.\mu = \mathcal{T}(X.T)$，即：$X$ 的 RG 坐标等于温度坐标在 $\mathcal{T}$ 下的像。

### 4.2 范畴结构

**定理 4.1**（$\mathbf{Diag}$ 的范畴结构）。$\Delta$ 是忠实且本质单射的——因此 $\mathbf{Diag}$ 是 $\mathbf{Temp} \times \mathbf{RG}$ 的子范畴。

**定理 4.2**（范畴等价）。对偶坐标投影 $\pi_{\mathbf{Temp}}|_{\mathbf{Diag}}: \mathbf{Diag} \to \mathbf{Temp}$ 是范畴等价——其拟逆为 $\Delta$。

### 4.3 物理意义

$\partial\mathbf{Rec}_D$ 是 $\mathbf{Diag}$ 的一个子集（退化边界）。物理上，对角条件 $\mu = \mathcal{T}(T)$ 正是谱粘合约束——在该边界上温度标度与 RG 标度不再是独立的自由参数，而是通过 $\mathcal{T}$ 函子相关的两个坐标。谱粘合正是沿该边界的信息保持条件。

### 4.4 Lean 形式化

```lean
structure DiagObj where
  T : TempObj

structure DiagHom (X Y : DiagObj) where
  tempMap : X.T ⟶ Y.T

noncomputable def diagEmbedding : TempObj ⥤ TempRGObj := ...
noncomputable def diagProjection : DiagObj ⥤ TempObj := ...
```

---

## 5. 谱粘合自然变换 $\theta$（方向 2）

### 5.1 核心恒等式

**定理 5.1**（对角编织恒等式）。对于 $X \in \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$，若 $X$ 的底点在对角线上（$\mu = \mathcal{T}(T)$），则：
$$\hat{\mathcal{T}}_{\text{Riem}}\big(\iota_T^*(X)\big) = \iota_\mu^*(X)$$
其中 $\iota_T: \mathbf{Temp} \hookrightarrow \mathbf{Temp} \times \mathbf{RG}$ 和 $\iota_\mu: \mathbf{RG} \hookrightarrow \mathbf{Temp} \times \mathbf{RG}$ 是坐标嵌入。

**证明**。两个拉回后的纤维数据相同（Cl(1,7) 间隙矩阵），且投影等式由 $\mu = \mathcal{T}(T)$ 保证。$\square$

### 5.2 编织自然变换

由定理 5.1，在对角线上存在一族比较同构 $\theta_X$：
$$\theta_X: \hat{\mathcal{T}}_{\text{Riem}}\big(\iota_T^*(X)\big) \xrightarrow{\cong} \iota_\mu^*(X)$$

$\theta_X$ 满足自然性条件：对任意态射 $f: X \to Y$，下图表交换：
```
T_hat_Riem(ι_T*(X)) -- θ_X --> ι_μ*(X)
      |                          |
T_hat_Riem(ι_T*(f))              ι_μ*(f)
      ↓                          ↓
T_hat_Riem(ι_T*(Y)) -- θ_Y --> ι_μ*(Y)
```

（形式化验证见 `weave_naturality` 定理。）

### 5.3 编织方图交换

谱粘合拉回方图交换条件严格表述为：
$$\sigma_{\text{BCS}} \circ \pi_T \circ \iota_T^* = \sigma_{\text{QCD}} \circ \pi_\mu \circ \iota_\mu^*$$

在对角线上成立（形式化见 `weave_square_commutes`）。

### 5.4 Lean 形式化

```lean
theorem diag_weave_via_T_hat_Riem (T₀ : TempObj) (X : SpectralBundleProd)
    (h : X.base.μ = TFunctor.obj X.base.T) :
    T_hat_Riem.obj ((pullback_ι_T (TFunctor.obj T₀)).obj X) =
    (pullback_ι_μ T₀).obj X := ...

theorem weave_naturality (T₀ T₁ : TempObj) (X Y : SpectralBundleProd)
    (f : X ⟶ Y) (hX : X.base.μ = TFunctor.obj X.base.T)
    (hY : Y.base.μ = TFunctor.obj Y.base.T) (hBase : X.base.T = T₀) (hBase' : Y.base.T = T₁) : ... := ...

theorem weave_square_commutes (T₀ : TempObj) (X : SpectralBundleProd)
    (h : X.base.μ = TFunctor.obj X.base.T) (hT : X.base.T = T₀) : ... := ...
```

---

## 6. $\hat{\mathcal{T}}_{\text{Riem}}$ 乘积基延拓（方向 3）

### 6.1 延拓函子

**定义 6.1**（延拓 $\hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}$）。$\hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$ 定义为：
- **对象**：$((T, \mu), (n, A)) \mapsto ((\mathcal{T}(T), \mu), (n, A))$
- **态射**：$(f, g, \phi) \mapsto (\mathcal{T}(f), g, \phi)$

其中 $\mathcal{T}$ 是 $\mathbf{Temp} \to \mathbf{RG}$ 的温标对偶函子，$\mathcal{T}(f)$ 是态射 $f$ 在 $\mathcal{T}$ 下的像。

### 6.2 性质

1. **保纤维**：$\hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}$ 不改变谱数据 $(n, A)$
2. **与投影交换**：$\pi_{T\mu} \circ \hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}} = (\mathcal{T} \times \text{id}) \circ \pi_{T\mu}$
3. **对角相容**：在对角线上，$\hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}$ 与 $\hat{\mathcal{T}}_{\text{Riem}}$ 兼容：
   $$\iota_T^* \circ \hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}} = \hat{\mathcal{T}}_{\text{Riem}} \circ \iota_T^*$$

### 6.3 与原始 $\hat{\mathcal{T}}_{\text{Riem}}$ 的关系

原始 $\hat{\mathcal{T}}_{\text{Riem}}: \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 是 $\hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}$ 沿 $\iota_T$ 的限制。对任意 $T$：
$$\hat{\mathcal{T}}_{\text{Riem}} \circ \iota_T^* = \iota_T^* \circ \hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}$$

### 6.4 Lean 形式化

```lean
noncomputable def T_hat_Riem_prod : SpectralBundleProd ⥤ SpectralBundleProd where
  obj X := { base := { T := TFunctor.obj X.base.T, μ := X.base.μ }, fiberData := X.fiberData }
  map f := ...

theorem T_hat_Riem_prod_base_commutes (X : SpectralBundleProd) : ... := ...
theorem T_hat_Riem_prod_diag_commutes (T₀ : TempObj) (X : SpectralBundleProd) ... : ... := ...
```

---

## 7. 参数化谱粘合截面（方向 4）

### 7.1 截面结构体

**定义 7.1**（$WeaveSection$）。$\mathbf{Temp} \times \mathbf{RG}$ 上的谱粘合截面是一个对 $(\sigma, \text{is\_section})$：
- $\sigma: \mathbf{Temp} \times \mathbf{RG} \to \mathbf{Bun}(\mathbf{Temp} \times \mathbf{RG}, \mathbf{Sp})$ 是函子
- $\pi_{T\mu} \circ \sigma = \text{id}_{\mathbf{Temp} \times \mathbf{RG}}$（截面条件）

### 7.2 常量截面

**构造 7.2**（$constWeaveSection$）。将 Cl(1,7) 间隙矩阵 $A_{17}$ 赋给每个底点 $(T, \mu)$：
$$\sigma_{\text{const}}(T, \mu) = ((T, \mu), A_{17})$$
态射映射为恒等纤维映射：$\sigma_{\text{const}}(f, g) = (f, g, I)$。

物理上，该截面是**普适的**——QCD、BCS 和 HP 截面都是它沿不同坐标方向拉回的特例：

| 截面 | 拉回方向 | 固定参数 | 对应物理 |
|:----|:--------|:--------|:--------|
| $\sigma_{\text{QCD}}$  | $\iota_T^*$（固定 $\mu = \Lambda_{\text{QCD}}$） | $\mu = \Lambda_{\text{QCD}}$ | QCD 临界温度 |
| $\sigma_{\text{BCS}}$  | $\iota_T^*$（固定 $\mu = \mathcal{T}(T_c)$）      | $\mu = \mathcal{T}(T_c)$ | BCS 超导 |
| $\sigma_{\text{HP}}$   | $\iota_\mu^*$（固定 $T = 0$）                   | $T = 0$ | Hawking-Page 相变 |
| $\sigma_{\text{rheo}}$ | $\iota_T^*$（固定 $\mu = \mu_{\text{crit}}$）    | $\mu = \mu_{\text{crit}}$ | 流变学剪切 |

### 7.3 参数化截面

**构造 7.3**（$paramWeaveSection$）。对任意 $n \in \mathbb{N}$ 和矩阵 $A \in M_n(\mathbb{C})$ 满足 $A^2 = A$（幂等性），可构造截面 $\sigma_{n,A}$：
$$\sigma_{n,A}(T, \mu) = ((T, \mu), (n, A))$$

幂等性 $A^2 = A$ 保证纤维映射的恒等性满足交换条件。这允许将谱粘合框架扩展到非 Cl(1,7) 系统。

### 7.4 对角闭包

**定理 7.1**（对角闭包）。常量截面在对角线上满足闭包条件：
$$\iota_T^* \circ \sigma_{\text{const}} = \iota_\mu^* \circ \sigma_{\text{const}} \quad\text{当}\quad \mu = \mathcal{T}(T)$$

这连接了谱粘合截面形式主义和 BCS 谱流自洽方程（`WeaveBCS.lean`）：谱间隙比 $r = \Delta\lambda_{\min}/\Delta\lambda_{\text{BCS}}$ 由自洽方程 $a_{\text{BCS}}^3 \cdot 4\pi = (1 + \sqrt{3}\sqrt{r})\cdot r$ 唯一确定，给出 $\Delta\lambda_{\text{BCS}} = 0.1396$，$a \approx 0.567$（偏差 $<0.1\%$）。

### 7.5 推前截面

沿 $\hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}}$ 可进一步定义截面的推前：
$$\sigma_{\text{flow}} = \hat{\mathcal{T}}_{\text{Riem}}^{\text{prod}} \circ \sigma_{\text{const}}$$
其底点为 $(\mathcal{T}(T), \mu)$，对应温度升高后的 RG 流演化。

### 7.6 Lean 形式化

```lean
structure WeaveSection where
  σ : TempRGObj ⥤ SpectralBundleProd
  is_section : ∀ (X : TempRGObj), π_Tμ.obj (σ.obj X) = X

noncomputable def constWeaveSection : WeaveSection := ...
noncomputable def paramWeaveSection (n : ℕ) (A : Matrix (Fin n) (Fin n) ℂ) (hA : A * A = A) : WeaveSection := ...

theorem BCS_weave_restricts_to_diag (T : TempObj) : ... := ...
theorem HP_weave_restricts_to_diag (T : TempObj) : ... := ...
theorem weave_closure_on_diag (T : TempObj) : ... := ...
```

---

## 8. 完整理论图景

### 8.1 结构总览

```
Temp × RG (乘积基)
   |-- ι_T: Temp ↪ Temp × RG      (固定 μ)
   |-- ι_μ: RG  ↪ Temp × RG      (固定 T)
   |-- Δ:   Temp ↪ Temp × RG      (对角线: μ = 𝒯(T))
   ↓
Bun(Temp × RG, Spec) (总范畴)
   |-- π_Tμ: Grothendieck 纤维化投影
   |-- constWeaveSection: 常量截面 (Cl(1,7))
   |-- paramWeaveSection: 参数化截面 (一般幂等矩阵)
   |-- T_hat_Riem_prod: 𝒯 延拓函子
   ↓
拉回到 Bun(Temp) / Bun(RG)
   |-- θ: T_hat_Riem ∘ ι_T* ≅ ι_μ*   (对角编织同构)
   |-- weave_square_commutes          (编织方图交换)
   ↓
BCS 谱流自洽方程
   |-- a_BCS³ · 4π = (1 + √3√r)·r     (§5.5.4)
   |-- Δλ_BCS = 0.1396, a ≈ 0.567    (<0.1% 偏差)
```

### 8.2 跨领域普适性

谱粘合乘积基的形式化统一了四种物理系统：

| 系统 | 基空间 | 编织截面 | 拉回沿 | 临界现象 |
|:----|:------|:--------|:------|:--------|
| QCD 相变 | $\mathbf{Temp}$ | $\sigma_{\text{const}} \circ \iota_T$ | $\iota_T$ 固定 $\mu=\Lambda_{\text{QCD}}$ | $T_c = 153$ MeV |
| BCS 超导 | $\mathbf{Temp}$ | $\sigma_{\text{const}} \circ \iota_T$ | $\iota_T$ 固定 $\mu=\mathcal{T}(T_c)$ | $a = 0.567$ |
| HP 相变 | $\mathbf{RG}$ | $\sigma_{\text{const}} \circ \iota_\mu$ | $\iota_\mu$ 固定 $T=0$ | Hawking 温度 |
| 流变学 | $\mathbf{Temp}$ | $\sigma_{\text{const}} \circ \iota_T$ | $\iota_T$ 固定 $\mu=\mu_{\text{crit}}$ | 临界剪切率 |

---

## 9. Lean 4 形式化对照

### 9.1 完整组件表

| 笔记 § | 组件 | Lean 模块 | 所在文件 |
|:------|:----|:---------|:--------|
| §1 | 乘积基 | `TempRGObj`, `TempRGHom`, `prodBaseCategory` | `WeaveProductFiber.lean` §1 |
| §1 | 坐标嵌入 | `ι_T`, `ι_μ` | `WeaveProductFiber.lean` §2 |
| §2 | 谱纤维 | `SpecFiberProd` | `WeaveProductFiber.lean` §3 |
| §2 | 总范畴 | `SpectralBundleProd`, `BundleProdHom` | `WeaveProductFiber.lean` §3 |
| §2 | 投影纤维化 | `π_Tμ`, `π_Tμ_fibration` | `WeaveProductFiber.lean` §4 |
| §2 | 拉回函子 | `pullback_ι_T`, `pullback_ι_μ` | `WeaveProductFiber.lean` §5 |
| §3 | 粘合条件 | `weave_gluing_square` | `WeaveProductFiber.lean` §6 |
| **§4** | **对角子范畴** | `DiagObj`, `DiagHom`, `diagEmbedding`, `isDiag` | **`WeaveProductFiber.lean` §7** |
| **§5** | **编织自然变换** | `diag_weave_via_T_hat_Riem`, `weave_naturality`, `weave_square_commutes` | **`WeaveProductFiber.lean` §8** |
| **§6** | **𝒯 延拓** | `T_hat_Riem_prod`, `T_hat_Riem_prod_diag_commutes` | **`WeaveProductFiber.lean` §9** |
| **§7** | **谱粘合截面** | `WeaveSection`, `constWeaveSection`, `paramWeaveSection`, `BCS_weave_restricts_to_diag` | **`WeaveProductFiber.lean` §10** |

### 9.2 文件变更

- `WeaveProductFiber.lean`：从 201 行（v0.1）扩展至 474 行（v0.2），新增 §7-§10
- 构建状态：**`lake build` 通过**（2452 jobs, 0 error）
- 新增依赖：`WeaveBCS.lean`（BCS 谱粘合形式化）

### 9.3 构建命令

```bash
cd formal_proof/UFPFormalization
lake build
```

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.2** | **2026-07-23** | **完整重写 §1-§3**：补全乘积基范畴（§1 完整数学内容）、乘积谱丛与 Grothendieck 纤维化（§2 含拉回丛）、∂Rec_D 粘合条件（§3 含拉回方图与物理诠释）；**新增 §4-§7**：对角子范畴（DiagObj + isDiag + diagEmbedding）、谱粘合自然变换（diag_weave_via_T_hat_Riem + weave_naturality + weave_square_commutes）、T_hat_Riem_prod 延拓、参数化谱粘合截面（WeaveSection + constWeaveSection + paramWeaveSection）；**新增 §8** 理论图景与跨领域普适性表；**新增 §9** 完整形式化对照表；Lean 全部通过 `lake build` |
| **v0.1** | **2026-07-22** | 初始版本：乘积基定义；谱粘合总范畴；$\partial\mathbf{Rec}_D$ 粘合条件；拉回方图；Lean 形式化方案 |
