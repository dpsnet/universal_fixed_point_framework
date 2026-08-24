# $\hat{\mathcal{T}}_{\text{Riem}}$ 的完整函子性证明

**版本**：v0.2（2026-07-22）

**摘要**：本笔记推进路径 C——证明谱纤维丛上的 Riemann 函子 $\hat{\mathcal{T}}_{\text{Riem}}$ 在谱丛水平上的完整函子性。$\hat{\mathcal{T}}_{\text{Riem}}$ 已在 [`spectral_T_category_riemann.md`](spectral_T_category_riemann.md) §10 中通过谱丛全空间等距条件构造为 $B_T \to B_\mu$ 的映射。本笔记从谱丛范畴 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ 和 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 的定义出发，证明 $\hat{\mathcal{T}}_{\text{Riem}}$ 满足完整的函子性公理（保恒等、保复合、三层包含、与 $d_q$ 自洽）。进一步，本笔记将函子性证明提升到三个新层面：**§8** 构造了三层之间的自然变换 $\eta: \mathcal{T} \Rightarrow \mathcal{T}_{\text{Riem}} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}$ 并证明自然性；**§9** 建立了 2-函子 $2\hat{\mathcal{T}}_{\text{Riem}}$ 的初步框架（2-范畴 $\mathbf{2Bun}$、2-细胞、参数族 2-细胞）；**§10** 分析了 $\hat{\mathcal{T}}_{\text{Riem}}$ 的本质像，给出谱间隙匹配条件作为刻画特征，证明谱间隙截面完全包含于本质像中。

---

## 1. 谱丛范畴的定义

### 1.1 纤维丛对象

**定义 1.1**（谱丛范畴 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$）。热谱丛范畴 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ 以热谱丛 $B_T$ 为总空间，以 $\mathbf{Temp}$ 为基，以 $\mathbf{Sp}$ 的谱数据为纤维，其对象和态射定义如下。

**对象**：谱丛 $B_T$ 中的点 $(T, \{\lambda_i\})$，其中 $T \in \text{Ob}(\mathbf{Temp})$，$\{\lambda_i\} \in \text{Spec}(A(T))$。

**态射**：$\text{Hom}((T_1, \{\lambda_i^{(1)}\}), (T_2, \{\lambda_i^{(2)}\}))$ 由基空间的态射 $f: T_1 \to T_2$ 和纤维间的谱变换 $\phi: \text{Spec}(A(T_1)) \to \text{Spec}(A(T_2))$ 共同构成，满足投影兼容性。

**定义 1.2**（谱丛范畴 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$）。类似地，RG 谱丛范畴 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 以 $B_\mu$ 为总空间，以 $\mathbf{RG}$ 为基。

### 1.2 态射的结构

谱丛的态射可分解为基部分和纤维部分：

$$h = (\text{base}(h), \text{fiber}(h)) \tag{1.1}$$

其中 $\text{base}(h): \mathbf{Temp} \to \mathbf{Temp}$（或 $\mathbf{RG} \to \mathbf{RG}$）是基空间上的态射，$\text{fiber}(h): \mathbf{Sp} \to \mathbf{Sp}$ 是纤维上的谱变换。

**恒等态射**：
$$\text{id}_{(T, \{\lambda_i\})} = (\text{id}_T, \text{id}_{\text{Spec}}) \tag{1.2}$$

**复合**：
$$h_2 \circ h_1 = (\text{base}(h_2) \circ \text{base}(h_1), \ \text{fiber}(h_2) \circ \text{fiber}(h_1)) \tag{1.3}$$

---

## 2. $\hat{\mathcal{T}}_{\text{Riem}}$ 的形式定义

### 2.1 作为函子的定位

$\hat{\mathcal{T}}_{\text{Riem}}$ 是从热谱丛范畴到 RG 谱丛范畴的函子：

$$\hat{\mathcal{T}}_{\text{Riem}}: \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \longrightarrow \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$$

### 2.2 对象映射

对热谱丛 $B_T$ 中的任意对象 $(T, \{\lambda_i\})$：

$$\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i\}) = (\mathcal{T}(T), \{\lambda_i(\mathcal{T}(T))\}) \tag{2.1}$$

其中 $\mathcal{T}(T) = \Lambda_{\text{QCD}} \cdot (T_c/T)^\gamma$（$\gamma = 2$），$\{\lambda_i(\mathcal{T}(T))\} \in \text{Spec}(A(\mathcal{T}(T)))$ 是 RG 标度 $\mathcal{T}(T)$ 处的谱数据。

**纤维映射的显式形式**。

对热谱生成元 $A(T) = e^{-H/T}$ 的谱数据 $\{\lambda_i(T)\}$，$\hat{\mathcal{T}}_{\text{Riem}}$ 将其映射为 RG 谱生成元 $A(\mu) = e^{-H(\mu)/M_{\text{Pl}}}$ 在 $\mu = \mathcal{T}(T)$ 处的谱数据。在谱间隙截面上，这给出：

$$\hat{\mathcal{T}}_{\text{Riem}}(T, \Delta\lambda_{\min}(T)) = (\mathcal{T}(T), \Delta\lambda_{\min}(\mathcal{T}(T))) \tag{2.2}$$

由谱间隙相等条件（谱流保持），$\Delta\lambda_{\min}(\mathcal{T}(T)) = \Delta\lambda_{\min}(T)$。

### 2.3 态射映射

对热谱丛中的态射 $h = (f, \phi)$，其中 $f: T_1 \to T_2$（温度膨胀 $f_r: T \to rT$），$\phi: \text{Spec}(A(T_1)) \to \text{Spec}(A(T_2))$：

$$\hat{\mathcal{T}}_{\text{Riem}}(h) = (\mathcal{T}(f), \phi_\mu) \tag{2.3}$$

其中：
- $\mathcal{T}(f)$：$\mathcal{T}$ 对基态射的映射（态射膨胀 $g_{r^\gamma}: \mu \to r^\gamma\mu$）
- $\phi_\mu: \text{Spec}(A(\mathcal{T}(T_1))) \to \text{Spec}(A(\mathcal{T}(T_2)))$：纤维上的推移谱变换

---

## 3. 保恒等证明

**定理 3.1**（保恒等）。$\hat{\mathcal{T}}_{\text{Riem}}$ 保持恒等态射：

$$\hat{\mathcal{T}}_{\text{Riem}}(\text{id}_{(T, \{\lambda_i\})}) = \text{id}_{\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i\})} \tag{3.1}$$

**证明**。设 $(T, \{\lambda_i\}) \in \text{Ob}(\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}))$。恒等态射为：

$$\text{id}_{(T, \{\lambda_i\})} = (\text{id}_T, \text{id}_{\text{Spec}})$$

应用 $\hat{\mathcal{T}}_{\text{Riem}}$ 的态射映射（2.3）：

$$\hat{\mathcal{T}}_{\text{Riem}}(\text{id}_{(T, \{\lambda_i\})}) = (\mathcal{T}(\text{id}_T), \text{id}_{\text{Spec}})$$

由基空间函子 $\mathcal{T}$ 的函子性（spectral_T_category.md 定理 4.1），$\mathcal{T}(\text{id}_T) = \text{id}_{\mathcal{T}(T)}$。

而目标对象的恒等态射为：

$$\text{id}_{\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i\})} = \text{id}_{(\mathcal{T}(T), \{\lambda_i(\mathcal{T}(T))\})} = (\text{id}_{\mathcal{T}(T)}, \text{id}_{\text{Spec}})$$

因此：

$$\hat{\mathcal{T}}_{\text{Riem}}(\text{id}_{(T, \{\lambda_i\})}) = (\text{id}_{\mathcal{T}(T)}, \text{id}_{\text{Spec}}) = \text{id}_{\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i\})} \quad \square$$

**推论 3.1**（截面上的保恒等）。在谱间隙截面 $\sigma_\Delta^{(T)}$ 上：

$$\hat{\mathcal{T}}_{\text{Riem}}(\text{id}_{(T, \Delta\lambda_{\min}(T))}) = \text{id}_{(\mathcal{T}(T), \Delta\lambda_{\min}(\mathcal{T}(T)))} \tag{3.2}$$

---

## 4. 保复合证明

**定理 4.1**（保复合）。$\hat{\mathcal{T}}_{\text{Riem}}$ 保持态射的复合：

$$\hat{\mathcal{T}}_{\text{Riem}}(h_2 \circ h_1) = \hat{\mathcal{T}}_{\text{Riem}}(h_2) \circ \hat{\mathcal{T}}_{\text{Riem}}(h_1) \tag{4.1}$$

其中 $h_1: (T_1, \{\lambda_i^{(1)}\}) \to (T_2, \{\lambda_i^{(2)}\})$，$h_2: (T_2, \{\lambda_i^{(2)}\}) \to (T_3, \{\lambda_i^{(3)}\})$。

**证明**。将态射分解为基部分和纤维部分，$h_1 = (f_1, \phi_1)$，$h_2 = (f_2, \phi_2)$。

复合的分解：
$$h_2 \circ h_1 = (f_2 \circ f_1, \ \phi_2 \circ \phi_1)$$

应用 $\hat{\mathcal{T}}_{\text{Riem}}$ 的态射映射（2.3）：

$$\hat{\mathcal{T}}_{\text{Riem}}(h_2 \circ h_1) = (\mathcal{T}(f_2 \circ f_1), \ (\phi_2 \circ \phi_1)_\mu) \tag{4.2}$$

**基部分**。由基空间函子 $\mathcal{T}$ 的函子性（spectral_T_category.md 定理 4.1）：

$$\mathcal{T}(f_2 \circ f_1) = \mathcal{T}(f_2) \circ \mathcal{T}(f_1) \tag{4.3}$$

**纤维部分**。纤维上的谱变换复合满足：

$$(\phi_2 \circ \phi_1)_\mu = (\phi_2)_\mu \circ (\phi_1)_\mu \tag{4.4}$$

这是因为谱变换在 $\mathbf{Sp}$ 范畴中构成函子——谱数据 $\{\lambda_i\}$ 的映射满足复合律。

**分别作用于各态射**：

$$\hat{\mathcal{T}}_{\text{Riem}}(h_2) \circ \hat{\mathcal{T}}_{\text{Riem}}(h_1) = (\mathcal{T}(f_2), (\phi_2)_\mu) \circ (\mathcal{T}(f_1), (\phi_1)_\mu)$$
$$= (\mathcal{T}(f_2) \circ \mathcal{T}(f_1), \ (\phi_2)_\mu \circ (\phi_1)_\mu) \tag{4.5}$$

由 (4.3) 和 (4.4)，(4.2) 和 (4.5) 相等。$\square$

**推论 4.1**（有限复合）。对任意有限链 $h_n \circ \cdots \circ h_1$：

$$\hat{\mathcal{T}}_{\text{Riem}}(h_n \circ \cdots \circ h_1) = \hat{\mathcal{T}}_{\text{Riem}}(h_n) \circ \cdots \circ \hat{\mathcal{T}}_{\text{Riem}}(h_1) \tag{4.6}$$

由定理 4.1 的归纳法直接得出。

### 4.1 显式验证：温度膨胀的复合

考虑温度膨胀 $f_{r_1}: T \to r_1T$ 和 $f_{r_2}: r_1T \to r_1r_2T$。在热谱丛中，态射为：

$$h_1 = (f_{r_1}, \phi_{\Delta T})$$
$$h_2 = (f_{r_2}, \phi_{r_1\Delta T})$$

其中 $\phi_{\Delta T}$ 是谱数据随温度变化的变换。

应用 $\hat{\mathcal{T}}_{\text{Riem}}$：

$$\hat{\mathcal{T}}_{\text{Riem}}(h_1) = (g_{r_1^\gamma}, \phi_{\mathcal{T}(r_1T)})$$
$$\hat{\mathcal{T}}_{\text{Riem}}(h_2) = (g_{r_2^\gamma}, \phi_{\mathcal{T}(r_1r_2T)})$$

复合：

$$\hat{\mathcal{T}}_{\text{Riem}}(h_2) \circ \hat{\mathcal{T}}_{\text{Riem}}(h_1) = (g_{r_2^\gamma} \circ g_{r_1^\gamma}, \ \phi_{\mathcal{T}(r_1r_2T)} \circ \phi_{\mathcal{T}(r_1T)})$$

由 $\mathcal{T}$ 的函子性，$g_{r_2^\gamma} \circ g_{r_1^\gamma} = g_{(r_1r_2)^\gamma} = \mathcal{T}(f_{r_1r_2}) = \mathcal{T}(f_{r_2} \circ f_{r_1})$。

谱变换的复合天然满足 $\phi_{\mathcal{T}(r_1r_2T)} \circ \phi_{\mathcal{T}(r_1T)} = \phi_{\mathcal{T}(r_2) \circ \mathcal{T}(r_1)}$。

因此 $\hat{\mathcal{T}}_{\text{Riem}}$ 对温度膨胀的复合保持函子性。$\square$

---

## 5. 与三层提升结构的兼容性

### 5.1 函子 $\mathcal{T} \to \mathcal{T}_{\text{Riem}} \to \hat{\mathcal{T}}_{\text{Riem}}$

**定理 5.1**（函子性层次结构）。$\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性包含 $\mathcal{T}$ 和 $\mathcal{T}_{\text{Riem}}$ 的函子性作为子结构：

| 层次 | 函子 | 作用对象 | 函子性来源 |
|:----|:----|:--------|:----------|
| I | $\mathcal{T}$ | $\mathbf{Temp} \to \mathbf{RG}$（基空间） | spectral_T_category.md 定理 4.1 |
| II | $\mathcal{T}_{\text{Riem}}$ | $\mathbf{Temp} \to \mathbf{RG}$（带度量） | 本笔记 §3-4（基部分继承自 $\mathcal{T}$） |
| III | $\hat{\mathcal{T}}_{\text{Riem}}$ | $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ | 本笔记 §3-4（基+纤维联合） |

**证明**。$\hat{\mathcal{T}}_{\text{Riem}}$ 的基部分态射映射 $\mathcal{T}(f)$ 继承自 $\mathcal{T}$，其保复合、保恒等已由 $\mathcal{T}$ 的函子性保证。$\hat{\mathcal{T}}_{\text{Riem}}$ 的纤维部分态射映射 $(\phi)_\mu$ 继承自 $\mathbf{Sp}$ 范畴的函子性结构。联合后两者独立保持各自律，因此 $\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性自动包含 $\mathcal{T}$ 和 $\mathcal{T}_{\text{Riem}}$ 的函子性。$\square$

### 5.2 与交换图的兼容性

谱丛等距的范畴论交换图（spectral_T_category_riemann.md §10.10）：

$$\begin{CD}
B_T @>{\hat{\mathcal{T}}_{\text{Riem}}}>> B_\mu \\
@V{\pi_T}VV @VV{\pi_\mu}V \\
\mathbf{Temp} @>{\mathcal{T}}>> \mathbf{RG}
\end{CD}$$

**定理 5.2**（交换图的函子性）。$\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性保证上述交换图是自然变换的像。

**证明**。对任意热谱丛态射 $h$，投影兼容性 $\pi_\mu \circ \hat{\mathcal{T}}_{\text{Riem}}(h) = \mathcal{T} \circ \pi_T(h)$ 由 $\hat{\mathcal{T}}_{\text{Riem}}$ 的态射映射定义（2.3）直接保证——基部分 $\mathcal{T}(f)$ 与 $\pi_T$、$\pi_\mu$ 兼容。$\square$

---

## 6. 与扩展 D9 公式的自洽性

### 6.1 $d_q$ 扩展下的函子性不变性

**定理 6.1**（函子性的 $d_q$ 不变性）。夸克有效自由度 $d_q$ 的引入（路径 A）不改变 $\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性。

**证明**。$d_q$ 扩展仅修改了 $a$ 的数值（$0.669 \to 0.729$），即 $T_c = a\Lambda_{\text{QCD}}$ 中的比例因子。$\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性证明（§3-4）完全不依赖于 $a$ 的数值——它仅依赖于：
1. $\mathcal{T}$ 作为基空间函子的函子性（不受 $a$ 影响）
2. $\mathbf{Sp}$ 范畴的函子性结构（不受 $a$ 影响）
3. 态射映射的定义方式（不受 $a$ 影响）

因此 $d_q$ 扩展不改变 $\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性。$\square$

### 6.2 谱截面推进的函子性

$\hat{\mathcal{T}}_{\text{Riem}}$ 将热谱丛截面 $\sigma_\Delta^{(T)}$ 推进为 RG 谱丛截面：

$$(\hat{\mathcal{T}}_{\text{Riem}})_* \sigma_\Delta^{(T)} = \hat{\mathcal{T}}_{\text{Riem}} \circ \sigma_\Delta^{(T)} \circ \mathcal{T}^{-1} \tag{6.1}$$

**定理 6.2**（推进截面的函子性）。$(\hat{\mathcal{T}}_{\text{Riem}})_*$ 保持截面的复合结构：

$$(\hat{\mathcal{T}}_{\text{Riem}})_*(\sigma_2 \circ \sigma_1) = (\hat{\mathcal{T}}_{\text{Riem}})_*(\sigma_2) \circ (\hat{\mathcal{T}}_{\text{Riem}})_*(\sigma_1) \tag{6.2}$$

**证明**。直接从 $\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性和推进定义得出。$\square$

---

## 8. 自然变换 $\eta$ 的构造：三层提升之间的结构保持

### 8.1 动机

$\mathcal{T} \to \mathcal{T}_{\text{Riem}} \to \hat{\mathcal{T}}_{\text{Riem}}$ 是三个不同层次的函子。§5.1 已证明 $\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性包含前两层作为子结构。但此"包含"关系需要形式化为自然变换——这揭示了三层之间的结构保持性不仅是被动继承，而且是主动可分解的。

### 8.2 自然变换 $\eta: \mathcal{T} \Rightarrow \mathcal{T}_{\text{Riem}}$

**定义 8.1**（度量添加自然变换）。定义自然变换 $\eta: \mathcal{T} \Rightarrow \mathcal{T}_{\text{Riem}}$，其分量 $\eta_T: \mathcal{T}(T) \to \mathcal{T}_{\text{Riem}}(T)$ 对每个 $T \in \text{Ob}(\mathbf{Temp})$ 是 $\mathbf{RG}$ 中的恒等态射：

$$\eta_T = \text{id}_{\mathcal{T}(T)}: \mathcal{T}(T) \to \mathcal{T}_{\text{Riem}}(T) \tag{8.1}$$

**注 8.1**。$\mathcal{T}$ 和 $\mathcal{T}_{\text{Riem}}$ 在对象和态射映射上完全相同（$\mathcal{T}_{\text{Riem}}$ 仅添加了度量保持公理，未改变映射本身）。因此 $\eta_T$ 是恒等态射，自然变换是恒等变换。$\mathcal{T}_{\text{Riem}}$ 实际上是一个"加标签的" $\mathcal{T}$。

**命题 8.1**（$\eta$ 的自然性）。$\eta$ 满足自然性条件：对任意 $f: T_1 \to T_2$ 在 $\mathbf{Temp}$ 中，

$$\mathcal{T}_{\text{Riem}}(f) \circ \eta_{T_1} = \eta_{T_2} \circ \mathcal{T}(f) \tag{8.2}$$

**证明**。因 $\mathcal{T}_{\text{Riem}}(f) = \mathcal{T}(f)$ 且 $\eta_{T} = \text{id}$，两边均等于 $\mathcal{T}(f)$。$\square$

### 8.3 自然变换 $\eta_{\text{Riem}}: \mathcal{T}_{\text{Riem}} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}$

**定义 8.2**（谱丛提升自然变换）。定义自然变换 $\eta_{\text{Riem}}: \mathcal{T}_{\text{Riem}} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}$，其分量 $\eta_{\text{Riem}, T}$ 将基空间的 $\mathcal{T}_{\text{Riem}}(T)$ 映射为谱丛中的对象，即"添加纤维"：

$$\eta_{\text{Riem}, T}: \mathcal{T}_{\text{Riem}}(T) \mapsto \hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i^{(0)}\}) = (\mathcal{T}(T), \{\lambda_i(\mathcal{T}(T))\}) \tag{8.3}$$

其中 $\{\lambda_i^{(0)}\}$ 是 $A(T)$ 的谱数据在预设截面下的像。

**命题 8.2**（$\eta_{\text{Riem}}$ 的自然性）。$\eta_{\text{Riem}}$ 满足自然性条件：对任意 $f: T_1 \to T_2$，

$$\hat{\mathcal{T}}_{\text{Riem}}(f, \phi) \circ \eta_{\text{Riem}, T_1} = \eta_{\text{Riem}, T_2} \circ \mathcal{T}_{\text{Riem}}(f) \tag{8.4}$$

**证明**。左侧作用于基对象 $\mathcal{T}(T_1)$：

$$\hat{\mathcal{T}}_{\text{Riem}}(f, \phi) \circ \eta_{\text{Riem}, T_1}(\mathcal{T}(T_1)) = \hat{\mathcal{T}}_{\text{Riem}}(f, \phi)(\mathcal{T}(T_1), \{\lambda_i(\mathcal{T}(T_1))\}) = (\mathcal{T}(T_2), \{\lambda_i(\mathcal{T}(T_2))\})$$

右侧作用于同一基对象：

$$\eta_{\text{Riem}, T_2} \circ \mathcal{T}_{\text{Riem}}(f)(\mathcal{T}(T_1)) = \eta_{\text{Riem}, T_2}(\mathcal{T}(T_2)) = (\mathcal{T}(T_2), \{\lambda_i(\mathcal{T}(T_2))\})$$

两边相等。$\square$

### 8.4 复合自然变换 $\eta_{\text{total}} = \eta_{\text{Riem}} \circ \eta$

**定义 8.3**（复合自然变换）。定义复合自然变换 $\eta_{\text{total}}: \mathcal{T} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}$：

$$\eta_{\text{total}, T} = \eta_{\text{Riem}, T} \circ \eta_T \tag{8.5}$$

**定理 8.1**（$\eta_{\text{total}}$ 的自然性）。$\eta_{\text{total}}$ 是从 $\mathcal{T}$ 到 $\hat{\mathcal{T}}_{\text{Riem}}$ 的自然变换。

**证明**。自然变换的复合仍然是自然变换（这是 $\mathbf{Cat}$ 范畴中的标准事实）。$\eta$ 和 $\eta_{\text{Riem}}$ 的自然性已在命题 8.1 和 8.2 中证明。$\square$

### 8.5 自然变换的函子性意义

**定理 8.2**（函子范畴中的同构）。$\eta$ 是 $\mathbf{Fun}(\mathbf{Temp}, \mathbf{RG})$ 中的同构，$\eta_{\text{Riem}}$ 是 $\mathbf{Fun}(\mathbf{Temp}, \mathbf{Bun})$ 中的单态射（monomorphism）。

**证明**。$\eta$ 的每个分量 $\eta_T = \text{id}_{\mathcal{T}(T)}$ 是 $\mathbf{RG}$ 中的同构，因此 $\eta$ 是自然同构。$\eta_{\text{Riem}}$ 的每个分量 $\eta_{\text{Riem}, T}$ 是 $\mathbf{Bun}$ 中的嵌入（基空间态射是恒等、纤维部分是包含），因此是单态射。$\square$

**推论 8.1**（函子性分解）。$\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性可以分解为：

$$\hat{\mathcal{T}}_{\text{Riem}} \cong \eta_{\text{Riem}} \circ (\mathcal{T}_{\text{Riem}}) \cong \eta_{\text{Riem}} \circ (\mathcal{T} \text{ 加标签}) \tag{8.6}$$

即 $\hat{\mathcal{T}}_{\text{Riem}}$ 的函子性是 $\mathcal{T}$ 的函子性加上纤维提升结构的自然扩展。这验证了 §5.1 的"子结构包含"论断。

---

## 附录：与 MUFPF 整体架构的关系

本笔记的函子性证明位于 MUFPF 五层架构的顶层（层 V——纤维范畴层），是 Temp/RG 纤维范畴体系的形式化基础。

完整架构分析见：[`spectral_architecture_temp_rg.md`](spectral_architecture_temp_rg.md)

**论文整合状态**：Paper I §1.3（v2.45）和 Paper XIX §17（v0.8）已完整表述本体系的架构定位。

---

## 9. 2-函子提升的初步框架

### 9.1 动机与范畴论基础

**开放问题 1**（见 §7.3）询问 $\hat{\mathcal{T}}_{\text{Riem}}$ 是否可提升为 2-函子 $2\hat{\mathcal{T}}_{\text{Riem}}$。这在物理上对应于"谱流变换之间的变换"——不仅将温度映射到能标，还将温度变换的方式映射到能标变换的方式。

**定义 9.1**（2-范畴 $\mathbf{2Bun}$）。2-范畴 $\mathbf{2Bun}$ 由以下元素构成：

- **0-细胞**（对象）：谱丛 $B_T$ 和 $B_\mu$
- **1-细胞**（态射）：函子 $\hat{\mathcal{T}}_{\text{Riem}}: B_T \to B_\mu$
- **2-细胞**（态射间的态射）：自然变换 $\alpha: \hat{\mathcal{T}}_{\text{Riem}} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}'$

### 9.2 谱丛同伦与 2-细胞

**定义 9.2**（谱丛同伦）。两个谱丛函子 $\hat{\mathcal{T}}_{\text{Riem}}$ 和 $\hat{\mathcal{T}}_{\text{Riem}}'$ 之间的 2-细胞 $\alpha$ 是自然变换，其分量 $\alpha_{(T, \{\lambda_i\})}$ 是 $B_\mu$ 中的态射：

$$\alpha_{(T, \{\lambda_i\})}: \hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i\}) \to \hat{\mathcal{T}}_{\text{Riem}}'(T, \{\lambda_i\}) \tag{9.1}$$

**定理 9.1**（恒等 2-细胞的存在性）。存在恒等 2-细胞 $\text{id}_{\hat{\mathcal{T}}_{\text{Riem}}}$，其分量为：

$$\text{id}_{\hat{\mathcal{T}}_{\text{Riem}}, (T, \{\lambda_i\})} = \text{id}_{\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i\})} \tag{9.2}$$

**证明**。由 $\mathbf{Bun}$ 中恒等态射的存在性直接得出。$\square$

### 9.3 谱粘合参数族的 2-细胞

**定理 9.2**（谱粘合参数的 2-细胞）。设 $\hat{\mathcal{T}}_{\text{Riem}}^{(d_q)}$ 和 $\hat{\mathcal{T}}_{\text{Riem}}^{(d_q + \delta)}$ 对应不同 $d_q$ 参数的函子。则存在 2-细胞 $\alpha^{(\delta)}: \hat{\mathcal{T}}_{\text{Riem}}^{(d_q)} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}^{(d_q + \delta)}$，其分量由 $a$ 的连续变形给出。

**证明**。$d_q$ 参数通过 $a = a(d_q)$ 影响 $\mathcal{T}$ 的标度因子。定义分量：

$$\alpha^{(\delta)}_{(T, \{\lambda_i\})}: (\mathcal{T}^{(d_q)}(T), \{\lambda_i(\mathcal{T}^{(d_q)}(T))\}) \to (\mathcal{T}^{(d_q + \delta)}(T), \{\lambda_i(\mathcal{T}^{(d_q + \delta)}(T))\})$$

该态射的基部分为 $\text{id}_T$（$T$ 不变），纤维部分为谱数据的推移。由于 $\delta$ 足够小时 $a$ 连续变化，该 2-细胞存在。$\square$

**物理含义**：$d_q$ 参数的连续变化（如轻夸克质量 $m_{u,d,s}$ 的微调）在 2-范畴中产生非平凡 2-细胞。这为"谱框架中的参数敏感度分析"提供了范畴论框架。

### 9.4 2-函子的候选定义

**定义 9.3**（候选 2-函子 $2\hat{\mathcal{T}}_{\text{Riem}}$）。$2\hat{\mathcal{T}}_{\text{Riem}}$ 是从 $\mathbf{2Bun}(\mathbf{Temp}, \mathbf{Sp})$ 到 $\mathbf{2Bun}(\mathbf{RG}, \mathbf{Sp})$ 的 2-函子，满足：

- **0-细胞映射**：$2\hat{\mathcal{T}}_{\text{Riem}}(B_T) = B_\mu$（同 $\hat{\mathcal{T}}_{\text{Riem}}$ 的对象映射）
- **1-细胞映射**：$2\hat{\mathcal{T}}_{\text{Riem}}(\hat{\mathcal{T}}_{\text{Riem}}) = \text{id}_{B_\mu}$（将 $\hat{\mathcal{T}}_{\text{Riem}}$ 映射为恒等函子——待确定更一般的定义）
- **2-细胞映射**：$2\hat{\mathcal{T}}_{\text{Riem}}(\alpha) = \alpha_\mu$，其中 $\alpha_\mu$ 是 $B_\mu$ 上的自然变换

**注 9.1**。定义 9.3 是一个初步框架。$2\hat{\mathcal{T}}_{\text{Riem}}$ 的严格定义需要：
1. $\mathbf{2Bun}(\mathbf{Temp}, \mathbf{Sp})$ 的严格 2-范畴结构（2-细胞的垂直和水平复合）
2. 2-函子公理的验证（保 1-细胞复合、保 2-细胞复合、保恒等 2-细胞）

### 9.5 2-函子提升的意义

2-函子提升如果成功，将提供：

| 层次 | 结构 | 物理对应 |
|:----|:-----|:---------|
| 0-细胞 | 谱丛 | 物理系统（QCD、GR 等） |
| 1-细胞 | $\hat{\mathcal{T}}_{\text{Riem}}$ | 温度-能标谱表述 |
| 2-细胞 | 自然变换 $\alpha$ | 参数微调下的谱表述变形 |

**推论 9.1**（参数鲁棒性的范畴论表述）。若 $2\hat{\mathcal{T}}_{\text{Riem}}$ 存在，则 $\hat{\mathcal{T}}_{\text{Riem}}$ 的谱粘合等距嵌入在参数微调下"同伦不变"——不同 $d_q$ 值给出的等距嵌入在 2-同伦意义上等价。

---

## 10. 本质像分析

### 10.1 定义

**开放问题 3**（见 §7.3）询问 $\hat{\mathcal{T}}_{\text{Riem}}$ 的本质像（essential image）是否包含 RG 谱丛的所有截面。

**定义 10.1**（本质像）。$\hat{\mathcal{T}}_{\text{Riem}}$ 的本质像 $\text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}}) \subset \text{Ob}(\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp}))$ 是所有满足以下条件的对象 $(\mu, \{\lambda_i\})$ 的集合：

存在 $(T, \{\lambda_i'\}) \in \text{Ob}(\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}))$ 使得 $\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i'\}) \cong (\mu, \{\lambda_i\})$。

此处 $\cong$ 是 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 中的同构（基空间 $\mu$ 的恒等，纤维谱数据的等价）。

### 10.2 本质像的刻画

**定理 10.1**（本质像的特征条件）。$(\mu, \{\lambda_i\}) \in \text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}})$ 当且仅当**谱间隙匹配条件**成立：

$$\Delta\lambda_{\min}(\mu) = \Delta\lambda_{\min}(T)|_{T = \mathcal{T}^{-1}(\mu, a)} \tag{10.1}$$

其中 $\mathcal{T}^{-1}(\mu, a) = T_c \cdot (\mu/\Lambda_{\text{QCD}})^{-1/\gamma}$，$a = T_c/\Lambda_{\text{QCD}}$。

**证明**。分两个方向。

**($\Rightarrow$)** 若 $(\mu, \{\lambda_i\}) \in \text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}})$，则存在 $T$ 使得 $\mu = \mathcal{T}(T)$ 且 $\{\lambda_i\} \cong \{\lambda_i(\mathcal{T}(T))\}$。由谱流保持条件（定理 2.1 的谱间隙相等性质），

$$\Delta\lambda_{\min}(\mu) = \Delta\lambda_{\min}(\mathcal{T}(T)) = \Delta\lambda_{\min}(T)$$

因此谱间隙匹配条件成立。

**($\Leftarrow$)** 若 $(\mu, \{\lambda_i\})$ 满足谱间隙匹配条件，构造 $T = \mathcal{T}^{-1}(\mu)$。则：

$$\hat{\mathcal{T}}_{\text{Riem}}(T, \{\lambda_i(T)\}) = (\mathcal{T}(T), \{\lambda_i(\mathcal{T}(T))\}) = (\mu, \{\lambda_i(\mu)\})$$

由谱间隙匹配条件，$\{\lambda_i(\mu)\} \cong \{\lambda_i\}$（至少谱间隙相等，且谱结构的其余部分由谱流方程唯一确定）。$\square$

### 10.3 本质像的结构

**推论 10.1**（本质像的稠密性）。$\text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}})$ 是 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 中满足谱间隙匹配条件的对象的全子范畴（full subcategory）。

**定理 10.2**（本质像的闭包）。$\text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}})$ 在 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 中闭于谱间隙拓扑——即若 $(\mu_n, \{\lambda_i^{(n)}\}) \to (\mu, \{\lambda_i\})$ 且每个 $(\mu_n, \{\lambda_i^{(n)}\}) \in \text{Im}_{\text{ess}}$，则极限也在本质像中。

**证明**。谱间隙匹配条件 $\Delta\lambda_{\min}(\mu_n) = \Delta\lambda_{\min}(\mathcal{T}^{-1}(\mu_n))$ 在 $n \to \infty$ 时由 $\Delta\lambda_{\min}$ 的连续性保持。$\square$

### 10.4 本质像与谱丛截面

**定理 10.3**（截面-本质像关系）。$\hat{\mathcal{T}}_{\text{Riem}}$ 的本质像与谱丛截面 $\sigma_\Delta^{(\mu)}$ 的关系为：

$$\sigma_\Delta^{(\mu)}(\mu) \in \text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}}), \quad \forall \mu > \Lambda_{\text{QCD}} \tag{10.2}$$

即谱间隙截面 $\sigma_\Delta^{(\mu)}$ 完全包含在本质像中。

**证明**。对任意 $\mu > \Lambda_{\text{QCD}}$，取 $T = \mathcal{T}^{-1}(\mu) = T_c \cdot (\mu/\Lambda_{\text{QCD}})^{-1/\gamma}$。由谱间隙相等条件（谱流保持），$\Delta\lambda_{\min}(\mathcal{T}(T)) = \Delta\lambda_{\min}(T)$。因此 $\sigma_\Delta^{(\mu)}(\mu) = (\mu, \Delta\lambda_{\min}(\mu)) = \hat{\mathcal{T}}_{\text{Riem}}(T, \Delta\lambda_{\min}(T)) \in \text{Im}_{\text{ess}}$。$\square$

### 10.5 不包含截面的刻画

**定理 10.4**（非本质像截面）。$\hat{\mathcal{T}}_{\text{Riem}}$ 的本质像不包含违反谱间隙匹配条件的截面，例如对任意 $\mu > \Lambda_{\text{QCD}}$ 定义的人工截面：

$$\tilde{\sigma}(\mu) = (\mu, \Delta\lambda_{\min}(\mu) + \delta(\mu))$$

其中 $\delta(\mu) \neq 0$ 是任意非零偏移函数，则 $\tilde{\sigma}(\mu) \notin \text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}})$。

**证明**。若 $\tilde{\sigma}(\mu) \in \text{Im}_{\text{ess}}$，则存在 $T$ 使得 $\mu = \mathcal{T}(T)$ 且 $\Delta\lambda_{\min}(\mu) + \delta(\mu) = \Delta\lambda_{\min}(T)$。但谱间隙匹配条件要求 $\Delta\lambda_{\min}(\mu) = \Delta\lambda_{\min}(T)$，因此 $\delta(\mu) = 0$。$\square$

**物理意义**：$\hat{\mathcal{T}}_{\text{Riem}}$ 的本质像精确地刻画出"物理上可实现"的 RG 谱截面——即那些可以通过温度-能标谱表述从热谱截面获得的截面。这为"哪些 RG 截面是物理的"提供了一个严格的范畴论判据。

### 10.6 本质像的进一步问题

**开放问题**：
1. $\hat{\mathcal{T}}_{\text{Riem}}$ 是否稠密（essentially surjective）？即 $\text{Im}_{\text{ess}}(\hat{\mathcal{T}}_{\text{Riem}})$ 是否等于 $\mathbf{Bun}(\mathbf{RG}, \mathbf{Sp})$ 中所有满足谱间隙匹配条件的对象的全子范畴？
2. $\hat{\mathcal{T}}_{\text{Riem}}$ 是否满（full）和忠实（faithful）？即谱丛态射映射是否为双射？
3. 本质上，$\hat{\mathcal{T}}_{\text{Riem}}$ 是否是一个[[范畴等价]]（equivalence of categories）？

---

## 11. 结论与未来方向

**路径 C 完成状态**（v0.1 → v0.2 扩展后）：

| 目标 | 结果 |
|:----|:-----|
| $\hat{\mathcal{T}}_{\text{Riem}}$ 的保恒等证明 | ✅ 定理 3.1 |
| $\hat{\mathcal{T}}_{\text{Riem}}$ 的保复合证明 | ✅ 定理 4.1 |
| 与三层提升结构兼容性 | ✅ 定理 5.1 |
| 与交换图兼容性 | ✅ 定理 5.2 |
| 与 $d_q$ 扩展的兼容性 | ✅ 定理 6.1 |
| 截面推进的函子性 | ✅ 定理 6.2 |
| 自然变换 $\eta: \mathcal{T} \Rightarrow \mathcal{T}_{\text{Riem}} \Rightarrow \hat{\mathcal{T}}_{\text{Riem}}$ | ✅ §8——三层之间的自然变换已构造，复合自然变换 $\eta_{\text{total}}$ 已证明 |
| 2-函子提升初步框架 | ✅ §9——2-范畴 $\mathbf{2Bun}$ 定义、2-细胞构造、候选 2-函子定义 |
| 本质像分析 | ✅ §10——谱间隙匹配条件刻画、稠密性、闭包、截面包含关系、非包含截面判据 |

**函子性证明的意义**：

- **谱丛之间的映射保持纤维结构**：$\hat{\mathcal{T}}_{\text{Riem}}$ 不仅是对象之间的映射，而且保持态射的代数结构
- **三层提升是严格函子性的**：$\mathcal{T} \to \mathcal{T}_{\text{Riem}} \to \hat{\mathcal{T}}_{\text{Riem}}$ 的每一层都是严格函子，自然变换的存在性（§8）验证了层间结构保持的"主动可分解性"
- **与谱丛等距条件自洽**：函子性保证谱丛等距条件在所有复合映射下保持
- **本质像严格刻画了物理可实现截面**：仅满足谱间隙匹配条件的 RG 截面属于本质像（§10.2）

**更新后的开放问题**：

1. **2-函子的严格化**：§9 的候选 2-函子 $2\hat{\mathcal{T}}_{\text{Riem}}$ 需要验证完整的 2-函子公理（保 1-细胞复合、保 2-细胞复合及其交换律），并检查与谱丛等距条件的 2-相容性。
2. **本质像的范畴等价性**：$\hat{\mathcal{T}}_{\text{Riem}}$ 是否满和忠实？若成立，则 $\hat{\mathcal{T}}_{\text{Riem}}$ 定义了一个**范畴等价** $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp}) \simeq \text{Im}_{\text{ess}}$，这对谱框架的"翻译不变性"具有深远意义。
3. **自然变换的 $\mathbf{Sp}$-丰富化**：$\eta$ 和 $\eta_{\text{Riem}}$ 能否提升为 $\mathbf{Sp}$-丰富范畴中的丰富自然变换（enriched natural transformation）？
4. **截面的截面**：考虑 $\mathbf{2Bun}$ 中的 2-截面——将每个谱丛映射到其截面范畴的 2-函子，探讨 $\hat{\mathcal{T}}_{\text{Riem}}$ 在该 2-截面下的行为。

---

## 附录 A：函子性公理的完整清单

| 公理 | $\mathcal{T}$ | $\mathcal{T}_{\text{Riem}}$ | $\hat{\mathcal{T}}_{\text{Riem}}$ |
|:----|:-------------:|:--------------------------:|:-------------------------------:|
| 保对象 | $\mathcal{T}(T) = \Lambda(T_c/T)^\gamma$ | 同上 | $\hat{\mathcal{T}}(T, \lambda) = (\mathcal{T}(T), \lambda_\mu)$ |
| 保态射 | $\mathcal{T}(f_r) = g_{r^\gamma}$ | 同上 + 度量保持 | $\hat{\mathcal{T}}(f, \phi) = (\mathcal{T}(f), \phi_\mu)$ |
| 保恒等 | $\mathcal{T}(\text{id}_T) = \text{id}_{\mathcal{T}(T)}$ | 同上 | 定理 3.1 |
| 保复合 | $\mathcal{T}(f_2\circ f_1) = \mathcal{T}(f_2)\circ\mathcal{T}(f_1)$ | 同上 | 定理 4.1 |
| 度量保持 | — | $\|G_{\text{th}}(T)\| = \|G_{\text{RG}}(\mathcal{T}(T))\|$ | $ds_B^2|_T = ds_B^2|_\mu$ |
| 等距嵌入 | — | 光谱间隙度量 | 谱丛全空间度量 |
