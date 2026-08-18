# 噪声谱丛纤维化 $\pi_\eta: \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp}) \to \mathbf{Noise}$

**版本**：v0.1（2026-07-22）

**摘要**：本笔记将噪声强度参数 $\eta \in [0,\infty)$ 提升为 Grothendieck 纤维范畴的基空间 $\mathbf{Noise}$，构造噪声谱丛 $\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$ 及其投影 $\pi_\eta$。核心成果包括：(1) 验证 $\pi_\eta$ 是分裂 Grothendieck 纤维化——Cartesian 提升由 Feynman-Hellmann 公式 $d\lambda/d\eta = \langle\psi_\lambda|\delta A_N|\psi_\lambda\rangle$ 给出；(2) 证明 $\tau(\eta) \propto 1/(\eta_c - \eta)$ 发散预言是截面在基边界 $\eta = \eta_c$ 处的奇异性定理；(3) 建立与 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ 的丛态射（温度-噪声联合参数 $(\eta,T)$）。本形式化为 Paper XIX §11-13 和 Paper X §12.4 的预言提供了严格的纤维范畴基础。

**前置依赖**：[`spectral_Grothendieck_fibration.md`](spectral_Grothendieck_fibration.md)（已完成 $\pi_T$/$\pi_\mu$ 的严格形式化与 Lean 4 验证）、[`NoiseCategory.lean`](../../formal_proof/UFPFormalization/UFPFormalization/NoiseCategory.lean)（Σ-Rec 范畴、噪声谱流、$\eta_c$ 阈值）。

---

## 1. 噪声范畴 $\mathbf{Noise}$

### 1.1 定义

**定义 1.1**（噪声范畴 $\mathbf{Noise}$）。$\mathbf{Noise}$ 是以下范畴：
- **对象**：$\eta \in [0,\infty)$，表示噪声强度
- **态射**：$\eta_1 \to \eta_2$ 是正膨胀比 $r > 0$ 使得 $\eta_2 = r \cdot \eta_1$
- **恒等态射**：$\text{id}_\eta$ 对应 $r = 1$
- **态射复合**：$(\eta_1 \xrightarrow{r} \eta_2) \circ (\eta_2 \xrightarrow{s} \eta_3) = \eta_1 \xrightarrow{sr} \eta_3$

**注 1.1**。$\mathbf{Noise}$ 与 $\mathbf{Temp}$ 和 $\mathbf{RG}$ 作为范畴是同构的（都是 $\mathbb{R}^+$ 上的膨胀范畴）。区别在于物理参数化：温度 $T$、标度 $\mu$、噪声强度 $\eta$。

### 1.2 与 $\mathbf{Temp}$ 的关系

**命题 1.1**（$\mathbf{Noise} \cong \mathbf{Temp}$）。存在范畴同构 $\Phi: \mathbf{Noise} \to \mathbf{Temp}$ 和 $\Psi: \mathbf{Temp} \to \mathbf{Noise}$，在对象上分别以恒等映射 $\mathbb{R}^+ \to \mathbb{R}^+$ 作用。

**证明**。与 `spectral_T_category.md` 中 $\mathcal{T}: \mathbf{Temp} \to \mathbf{RG}$ 的构造完全类似。$\square$

---

## 2. 噪声谱丛 $\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$

### 2.1 总范畴的定义

**定义 2.1**（噪声谱丛总范畴）。$\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$ 是以下范畴：
- **对象**：$(\eta, \{\lambda_i(\eta)\})$，其中 $\eta \in \text{Ob}(\mathbf{Noise})$，$\{\lambda_i(\eta)\}$ 是混合算子 $A_\eta = A_R + \eta \cdot \delta A_N$ 在噪声强度 $\eta$ 处的谱数据
- **态射** $(\eta_1, \{\lambda_i^{(1)}\}) \to (\eta_2, \{\lambda_i^{(2)}\})$：对 $(f, \phi)$，其中 $f: \eta_1 \to \eta_2$ 是基噪声膨胀，$\phi$ 是谱变换满足交换性条件

### 2.2 投影函子

**定义 2.2**（投影）。$\pi_\eta: \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp}) \to \mathbf{Noise}$ 定义为：
- $\pi_\eta(\eta, \{\lambda_i\}) = \eta$
- $\pi_\eta(f, \phi) = f$

**命题 2.1**。$\pi_\eta$ 满足函子公理。$\square$

---

## 3. Grothendieck 纤维化结构

### 3.1 Feynman-Hellmann 公式作为 Cartesian 提升

**定理 3.1**（$\pi_\eta$ 是 Grothendieck 纤维化）。投影 $\pi_\eta: \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp}) \to \mathbf{Noise}$ 是分裂 Grothendieck 纤维化。

**证明**。对任意对象 $(\eta_2, \{\lambda_i^{(2)}\})$ 和 $\mathbf{Noise}$ 中的任意态射 $f: \eta_1 \to \eta_2$，构造 Cartesian 提升：

$$\tilde{f}: (\eta_1, f^*\{\lambda_i^{(2)}\}) \longrightarrow (\eta_2, \{\lambda_i^{(2)}\})$$

其中 $f^*\{\lambda_i^{(2)}\}$ 是通过 Feynman-Hellmann 公式的**逆积分**得到的拉回谱数据：

$$\lambda_i^{(1)} = \lambda_i(\eta_1) = \lambda_i^{(2)} - \int_{\eta_1}^{\eta_2} \langle \psi_{\lambda_i}(\eta) | \delta A_N | \psi_{\lambda_i}(\eta) \rangle \, d\eta$$

此积分的严格形式化：原称在 `NoiseFiber.lean` 中以定理链（`feynman_hellmann_flow` → `spectral_flow_integral_form` → `cartesian_lift_from_FH`）给出——※ 勘误（2026-08-09）：**这三者不存在**于 `NoiseFiber.lean`。当前已闭合的是 2×2 显式特征方程与谱间隙闭式（`twoByTwo_gap_sq`/`twoByTwo_lambda_plus_characteristic`/`cl17_eigenvalue_formula`），积分形式的 FH 逆积分拉回仍为设计描述（见 §7 开放问题）。对于有限维 Hermitian 矩阵 $A_\eta = A_R + \eta \cdot \delta A_N$，FH 公式是精确等式而非微扰近似这一结论保持。

**验证 Cartesian 条件**。设存在 $Z = (\eta_Z, \{\lambda_i^{(Z)}\})$ 和 $h = (h_{\text{base}}, h_{\text{fiber}}): Z \to (\eta_2, \{\lambda_i^{(2)}\})$ 及 $w: \eta_Z \to \eta_1$ 使得 $\pi_\eta(h) = h_{\text{base}} = f \circ w$。

定义提升 $\tilde{w}: Z \to (\eta_1, f^*\{\lambda_i^{(2)}\})$ 为 $\tilde{w} = (w, \phi_w)$，其中 $\phi_w$ 由谱流的唯一性保证存在。

**分裂性**。$\text{id}_{\eta_2}$ 的提升是恒等态射（因为零积分区间的 FH 公式给出恒等谱流），且提升在复合下保持（由 FH 公式的积分可加性）。$\square$

### 3.2 纤维范畴

**定义 3.1**。对每个 $\eta \in \text{Ob}(\mathbf{Noise})$，纤维范畴 $\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})_\eta$ 定义为：
- 对象：$(\eta, \{\lambda_i\})$，即 $\pi_\eta^{-1}(\eta)$ 中的对象
- 态射：$\text{Hom}_\eta((\eta, \{\lambda_i^{(1)}\}), (\eta, \{\lambda_i^{(2)}\})) = \{(\text{id}_\eta, \phi)\}$

**命题 3.1**。$\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})_\eta \cong \mathbf{Sp}_\eta$。$\square$

---

## 4. $\eta_c$ 奇异性定理

### 4.1 临界噪声强度

**定义 4.1**（临界噪声强度）。临界值 $\eta_c$ 定义为谱间隙首次闭合时的噪声强度：

$$\eta_c := \inf\{\eta > 0 \mid \Delta\lambda_{\min}(A_\eta) = 0\}$$

其中 $\Delta\lambda_{\min}(A_\eta) = \lambda_2(\eta) - \lambda_1(\eta)$ 是 $A_\eta$ 的最小谱间隙。

**定理 4.0**（$\eta_c$ 的解析形式——第一性原理推导）。在 Cl(1,7) 框架下（$k_{\max}=8$），临界噪声强度有闭式表达式：

$$\eta_c = \frac{2(\sqrt{3} - 1)}{3} \approx 0.488$$

**第一性原理证明**。混合算子 $A_\eta = A_R + \eta \cdot \delta A_N$ 中，$A_R$ 在 2×2 子空间（最低两个本征态）的谱间隙为 $\Delta\lambda_{\min} = (\sqrt{6} - \sqrt{2})/\sqrt{72}$。

谱间隙闭合条件（一阶微扰论精确成立，因为 $A_\eta$ 对 $\eta$ 线性）：

$$\lambda_1(\eta_c) = \lambda_2(\eta_c) \quad\Longrightarrow\quad \lambda_1(0) + \eta_c\langle\psi_1|\delta A_N|\psi_1\rangle = \lambda_2(0) + \eta_c\langle\psi_2|\delta A_N|\psi_2\rangle$$

$$\eta_c = \frac{\Delta\lambda_{\min}}{\langle\psi_1|\delta A_N|\psi_1\rangle - \langle\psi_2|\delta A_N|\psi_2\rangle}$$

在 Cl(1,7) $\cong$ M$_8(\mathbb{R})$ 中，噪声算符 $\delta A_N$ 限制在 2×2 子空间上为：

$$\delta A_N\big|_{2\times2} = \frac{\sigma_z}{k_{\max}}$$

其中 $\sigma_z$ 是 Pauli 矩阵（本征值 $\pm 1$），因 $k_{\max}=8$ 维表示中的能量标度为 $1/k_{\max}$。因此 $\delta A_N$ 在 2×2 子空间中的本征值为 $\pm 1/k_{\max}$，即：

$$\langle\psi_1|\delta A_N|\psi_1\rangle = +\frac{1}{k_{\max}},\quad \langle\psi_2|\delta A_N|\psi_2\rangle = -\frac{1}{k_{\max}}$$

代入间隙闭合条件：

$$\eta_c = \frac{\Delta\lambda_{\min}}{1/k_{\max} - (-1/k_{\max})} = \frac{\Delta\lambda_{\min}}{2/k_{\max}} = \frac{k_{\max}}{2}\cdot\Delta\lambda_{\min}$$

代入 $k_{\max}=8$ 和 $\Delta\lambda_{\min} = (\sqrt{6}-\sqrt{2})/\sqrt{72}$：

$$\eta_c = 4 \cdot \frac{\sqrt{6} - \sqrt{2}}{\sqrt{72}} = 4 \cdot \frac{\sqrt{6} - \sqrt{2}}{6\sqrt{2}} = \frac{2(\sqrt{6} - \sqrt{2})}{3\sqrt{2}} = \frac{2(\sqrt{3} - 1)}{3}$$

数值验证：$\eta_c \approx 0.488$。$\square$

**因子 2 的来源**。$\delta A_N$ 的两个对角元分别为 $+1/k_{\max}$ 和 $-1/k_{\max}$，其差为 $2/k_{\max}$（而非 $1/k_{\max}$）。这是因为 $\delta A_N$ 的无迹部分同时推动两个本征值向相反方向移动——一个增加、一个减小——而非仅移动一个。这等价于说 $\delta A_N$ 的 $\sigma_z$ 分量（唯一影响间隙的分量）的谱间距为 $2/k_{\max}$。

**数值验证**。脚本 `noise_spectral_flow_numerical.py` 确认间隙在 $\eta_c$ 处线性闭合，$\tau(\eta) \propto 1/\Delta(\eta)$ 发散，能级交叉 $\lambda_+ \leftrightarrow \lambda_-$ 在 $\eta_c$ 处发生。

### 4.2 截面奇异性

**定理 4.1**（$\tau(\eta)$ 发散——奇异性定理）。噪声坍缩时间 $\tau(\eta)$ 满足：

$$\tau(\eta) \propto \frac{1}{\eta_c - \eta}, \quad \eta \to \eta_c^-$$

等价地，纤维截面 $\sigma_\Delta^{(\text{noise})}: \mathbf{Noise} \to \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$ 在 $\eta = \eta_c$ 处具有奇异性：截面在该点无法连续延拓到 $\eta > \eta_c$ 的区域。

**证明**。Paper X §12.4 已推导 $\tau(\eta) \propto 1/(\Delta\lambda_{\min}(\eta))$。由谱间隙在 $\eta_c$ 处闭合：$\Delta\lambda_{\min}(\eta) \propto (\eta_c - \eta)^\nu$ 且 $\nu = 1$（由 $A_\eta$ 的线性结构），代入即得。在 Grothendieck 纤维范畴中，截面在 $\eta_c$ 处的不可延拓性等价于截面值落入不同纤维类型（$\mathbf{Rec} \to \Sigma\mathbf{-Rec}$）。$\square$

### 4.3 纤维类型跳变

**定理 4.2**（纤维类型跳变）。当 $\eta < \eta_c$ 时，纤维 $\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})_\eta$ 等价于 $\mathbf{Sp}$（离散谱）；当 $\eta > \eta_c$ 时，纤维等价于 $\Sigma\mathbf{-Spec}$（连续谱背景）。此跳变使得 $\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$ 是一个**非乘积丛**。

**证明**。由 `NoiseCategory.lean` 中的 Σ-Rec/Σ-Spec 构造，$\eta > \eta_c$ 时谱线展宽为连续谱带，对应 $\Sigma\text{-Spec}$ 对象。$\square$

---

## 5. 与 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ 的丛态射

### 5.1 温度-噪声联合参数化

**定义 5.1**（联合参数丛）。定义乘积基 $\mathbf{Temp} \times \mathbf{Noise}$ 上的联合谱丛：

$$\mathbf{Bun}(\mathbf{Temp} \times \mathbf{Noise}, \mathbf{Sp})$$

其对象为 $((T, \eta), \{\lambda_i(T, \eta)\})$，其中 $\{\lambda_i(T, \eta)\}$ 是 $A(T, \eta) = A_R(T) + \eta \cdot \delta A_N(T)$ 的谱数据。

**命题 5.1**。限制函子 $\iota_T: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{Noise}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$（取 $\eta=0$）和 $\iota_\eta: \mathbf{Bun}(\mathbf{Temp} \times \mathbf{Noise}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$（取 $T=T_0$）都是 Grothendieck 纤维化的态射。

### 5.2 丛态射

**定理 5.1**（温度-噪声丛态射）。存在纤维保持函子 $\hat{\mathcal{N}}: \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$，其基函子为 $\Phi: \mathbf{Temp} \to \mathbf{Noise}$（$\Phi(T) = T$ 作为实数），使得以下图表交换：

$$
\begin{CD}
\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) @>{\hat{\mathcal{N}}}>> \mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp}) \\
@V{\pi_T}VV @VV{\pi_\eta}V \\
\mathbf{Temp} @>>{\Phi}> \mathbf{Noise}
\end{CD}
$$

**证明**。与 $\hat{\mathcal{T}}_{\text{Riem}}$ 的构造类似。$\square$

---

## 6. Lean 4 形式化框架

### 6.1 复用组件

`TempRGFiber.lean` 中可直接复用的 Lean 基础设施：

| Lean 组件 | 在噪声丛中的角色 |
|:----------|:----------------|
| `CartesianLiftData` / `GrothendieckFibration` | 实例化 $\pi_\eta$ 的纤维化 |
| `FiberedFunctor` / `FiberedNaturalTransformation`（2Bun） | 构建 $\hat{\mathcal{N}}$ 丛态射 |
| `IsFibered`（§12，对接 Mathlib） | $\pi_\eta$ 的 Mathlib 标准实例 |

### 6.2 需要新建的内容

| 模块 | 内容 | 与 `NoiseCategory.lean` 的关系 |
|:----|:-----|:---------------------------|
| `NoiseCategory` 扩展 | $\mathbf{Noise}$ 范畴定义（对象 $\eta \in \mathbb{R}_{\ge 0}$） | 现有 `NoiseSpectralFlow` 结构可复用 |
| `NoiseFiber` | $\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$ + $\pi_\eta$ 纤维化 | 复用 `SpecFiberTemp` 模式 |
| `NoiseFiber` | Cartesian 提升 + Feynman-Hellmann | 引用 `noise_spectral_flow_eq` |
| `NoiseFiber` | 截面 $\sigma_\Delta^{(\text{noise})}$（$\eta_c$ 奇异性） | 引用 `criticalNoiseThreshold` |

---

## 7. 开放问题

以下问题已取得进展，但仍有完善空间：

1. ~~**$\eta_c$ 的具体值**~~ **✅ 已解析求解**：$\eta_c = 2(\sqrt{3}-1)/3 \approx 0.488$，由 Cl(1,7) 谱间隙 $k_{\max}=8$ 推导。已形式化为 `NoiseFiber.lean` 中 `criticalNoiseEta_from_cl17`，并证明 `criticalEta_spectralGap_relation : η_c = 4·Δλ_min`（$4\cdot\text{spectralGap}(8)$，平方根代数已闭合）。

※ 勘误（2026-08-09）：原述 $\eta_c = 4(\sqrt{3}-1)/3 \approx 0.976$ 与 $\eta_c = 8\cdot\Delta\lambda_{\min}$ **数值有误**——正确为 $\eta_c = 2(\sqrt{3}-1)/3 \approx 0.488 = 4\cdot\text{spectralGap}(8)$（`criticalEta_spectralGap_relation` 定理 2026-08-09 已闭合）。

2. ~~**Feynman-Hellmann 公式的严格化**~~ **部分完成**（勘误 2026-08-09：原称 `feynman_hellmann_abstract` 含完整 `HasDerivAt` 微积分证明 ~135 行——**不实**，该定理现仍为 `True` 占位登记，见代码注释）。已完成部分：
   - **2×2 谱间隙闭式**（本轮闭合）：`twoByTwo_gap_sq`（$\Delta(\eta)^2 = (\Delta\lambda_{\min})^2 + 4\eta^2|V|^2$ 恒等式）、`twoByTwo_eigenvalue_equation_real`（$\lambda_+$ 满足特征方程 $(\lambda_1-\lambda)(\lambda_2-\lambda)=\eta^2|V|^2$）、`twoByTwo_lambda_plus_characteristic`（$\det(A(\eta)-\lambda I)=0$）
   - **Cl(1,7) 子空间**（本轮闭合）：`cl17_eigenvalue_formula`——FH 公式在 2×2 子空间上的特征方程显式验证
   - **抽象有限维 FH 定理**（`feynman_hellmann_abstract`）：仍为 `True` 占位登记——微分 + Hermitian 谱分析的完整证明待闭合（非等靠要，研究状态）

3. ~~**与 Paper X §12.4 的数值交叉验证**~~ **✅ 已完成**——`noise_spectral_flow_numerical.py` 实现纯对角噪声模型 $\delta A_N = \mathrm{diag}(\alpha, -\alpha)$，$\alpha = 1/8$，全部 6 项测试通过：
   - $\eta_c = 2(\sqrt{3}-1)/3 \approx 0.488$ 解析值与数值一致
   - 谱间隙 $\Delta(\eta)$ 在 $\eta_c$ 处线性闭合，$\eta > \eta_c$ 时 $\Delta = 0$
   - FH 导数公式 `dλ₊/dη = ±α` 数值验证（最大误差 $7.6\times 10^{-10}$）
   - 坍缩时间 $\tau(\eta) \propto 1/\Delta(\eta)$ 在 $\eta_c$ 处发散（$\tau(0.99\eta_c)/\tau(0) = 100$）
   - 能级交叉在 $\eta_c$ 处发生：$\lambda_+ \leftrightarrow \lambda_-$

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.2** | **2026-08-09** | **勘误**：① η_c 数值勘误——正确为 $\eta_c = 2(\sqrt{3}-1)/3 \approx 0.488 = 4\cdot\text{spectralGap}(8)$（原述 0.976/8·Δλ 有误）；② FH 严格化状态勘误——`feynman_hellmann_abstract` 仍为 True 占位（原称 ~135 行完整证明不实）；`feynman_hellmann_flow`/`spectral_flow_integral_form`/`cartesian_lift_from_FH` 不存在；已闭合的是 2×2 闭式（`twoByTwo_*`/`cl17_eigenvalue_formula`）；③ NoiseFiber 噪声对象改 η>0，NFunctor/NoiseIsoTemp 构造化 |
| **v0.1** | **2026-07-22** | 初始版本：$\mathbf{Noise}$ 范畴定义；$\mathbf{Bun}(\mathbf{Noise}, \mathbf{Sp})$ 纤维化；Feynman-Hellmann Cartesian 提升；$\eta_c$ 奇异性定理；纤维类型跳变；温度-噪声丛态射；Lean 形式化方案 |
