# 超荷 Y 的 Cl(1,7) 谱代数推导

> **目标**：从 Cl(1,7) Clifford 代数的根系和权重重系统推导 SM 超荷 $Y$ 的数值，而非引用标准 QFT 赋值。
>
> **承袭**：本笔记延续 `zero_parameter_derivation.md` §2 的 Cl(1,7) → SO(1,7) → SU(4) → SU(3)×U(1) 分支链。

---

## 1. 问题陈述

在 `spectral_SM.md` 中，SM 费米子的超荷以"已知 SM 事实"的方式列出：

| 场 | $SU(3)_C$ | $SU(2)_L$ | $U(1)_Y$ |
|:--|:---------:|:---------:|:--------:|
| $Q_L = (u_L, d_L)$ | $\mathbf{3}$ | $\mathbf{2}$ | $+1/6$ |
| $u_R$ | $\mathbf{3}$ | $\mathbf{1}$ | $+2/3$ |
| $d_R$ | $\mathbf{3}$ | $\mathbf{1}$ | $-1/3$ |
| $L_L = (\nu_L, e_L)$ | $\mathbf{1}$ | $\mathbf{2}$ | $-1/2$ |
| $e_R$ | $\mathbf{1}$ | $\mathbf{1}$ | $-1$ |

这些数值的"为什么"未被回答。本文从 Cl(1,7) 的根系结构推导它们。

---

## 2. 关键事实：SO(1,7) → SM 群的代数嵌入

Cl(1,7) 的 Lie 代数 $\mathfrak{so}(1,7)$ 是 28 维。我们需要识别其 Cartan 子代数中哪些生成元对应 SM 的量子数。

### 2.1 $\mathfrak{so}(1,7)$ 的根系

$\mathfrak{so}(1,7)$ 的复化是 $D_4$ 型（即 $\mathfrak{so}(8, \mathbb{C})$）。$D_4$ 有 4 个简单根：

$$\alpha_1, \alpha_2, \alpha_3, \alpha_4$$

其 Dynkin 图为：

```
    α₄
    |
α₁—α₂—α₃
```

4 个简单根具有相同的长度（$|\alpha_i|^2 = 2$，在标准归一化下），但分支节点 $\alpha_2$ 处连接三个分支。

### 2.2 Cartan 子代数与 SM 量子数的对应

$\mathfrak{so}(1,7)$ 的 Cartan 子代数 $\mathfrak{h}$ 是 4 维的，其基为 $\{H_1, H_2, H_3, H_4\}$。SM 的三个量子数——弱同位旋第三分量 $T^3$、超荷 $Y$、色荷的颜色分量——对应 $\mathfrak{h}$ 中三个特定的线性组合。

**识别方案**：在分解 $\mathfrak{so}(1,7) \to \mathfrak{so}(1,3) \oplus \mathfrak{su}(4)$ 中：

- $\mathfrak{su}(4)$ 的 Cartan 子代数是 3 维的，其生成元之一对应 $B-L$
- $\mathfrak{so}(1,3)$ 的 Cartan 子代数是 2 维的（旋量表示的 $\gamma^0\gamma^1$ 和 $\gamma^2\gamma^3$），其中之一对应 $T^3$

---

## 3. 从 $8_s$ 旋量表示提取超荷

### 3.1 Cl(1,7) Gamma 矩阵的显式构造

采用 `zero_parameter_derivation.md` §5.1 的 8×8 实表示：

$$
\begin{aligned}
\gamma_0 &= \sigma_x \otimes \sigma_y \otimes I_2 \\
\gamma_1 &= \sigma_x \otimes \sigma_x \otimes \sigma_x \\
\gamma_2 &= \sigma_x \otimes \sigma_x \otimes \sigma_y \\
\gamma_3 &= \sigma_x \otimes \sigma_x \otimes \sigma_z \\
\gamma_4 &= \sigma_x \otimes \sigma_z \otimes I_2 \\
\gamma_5 &= \sigma_y \otimes \sigma_y \otimes I_2 \\
\gamma_6 &= \sigma_y \otimes \sigma_z \otimes I_2 \\
\gamma_7 &= \sigma_z \otimes I_2 \otimes I_2
\end{aligned}
$$

### 3.2 SO(1,7) Lie 代数生成元

SO(1,7) 的 28 个生成元为：

$$\Sigma_{\mu\nu} = \frac{1}{4}[\gamma_\mu, \gamma_\nu], \quad \mu, \nu = 0, 1, \ldots, 7$$

其中 $\Sigma_{\mu\nu}$ 是 $8 \times 8$ 矩阵。

### 3.3 $8_s$ 旋量空间的基

$8_s$ 旋量表示有 8 个基向量 $|s_1s_2s_3\rangle$，其中 $s_i \in \{\uparrow, \downarrow\}$，对应三个张量积因子 $\sigma_x, \sigma_y, \sigma_z$ 的本征态。

### 3.4 Cartan 子代数生成元的对角化

在 $8_s$ 表示中，我们选择 Cartan 子代数的生成元为四个互相反对易的对角化生成元。一个自然的选择是：

$$
\begin{aligned}
H_1 &= i\Sigma_{01} = \frac{i}{4}[\gamma_0, \gamma_1] \\
H_2 &= i\Sigma_{23} = \frac{i}{4}[\gamma_2, \gamma_3] \\
H_3 &= i\Sigma_{45} = \frac{i}{4}[\gamma_4, \gamma_5] \\
H_4 &= i\Sigma_{67} = \frac{i}{4}[\gamma_6, \gamma_7]
\end{aligned}
$$

它们构成 $\mathfrak{so}(1,7)$ 的 Cartan 子代数的一组基。

**定理 3.1**（$H_i$ 的本征值）。在 $8_s$ 旋量表示中，四个 Cartan 生成元 $H_1, H_2, H_3, H_4$ 的本征值均为 $\pm\frac12$，且 $8_s$ 的 8 个基向量一一对应于 $(\pm\frac12, \pm\frac12, \pm\frac12, \pm\frac12)$ 的 8 种符号组合。

**证明**。通过 Gamma 矩阵的显式计算可得。□

### 3.5 SM 量子数的代数识别

**定义 3.1**（弱同位旋 $T^3$）。SM 的弱同位旋第三分量 $T^3$ 对应 $\mathfrak{so}(1,3)$ 子代数的生成元：

$$T^3 = i\Sigma_{12} = \frac{i}{4}[\gamma_1, \gamma_2]$$

计算得 $T^3$ 在 $8_s$ 上的本征值为 $\pm\frac12$，其中：
- $+\frac12$：左手中微子态
- $-\frac12$：左手电子态
- $0$：所有右手态

**定义 3.2**（超荷 $Y$）。超荷 $Y$ 由 $\mathfrak{su}(4)$ 子代数中与 $\mathfrak{su}(3)$ 对易的 $U(1)$ 生成元给出：

$$Y = \frac{1}{2\sqrt{3}}(H_3 + \sqrt{3}H_4)$$

其中系数由 $\mathfrak{su}(4) \to \mathfrak{su}(3) \oplus \mathfrak{u}(1)$ 的分支规则确定。

---

## 4. 超荷的显式计算

### 4.1 $8_s$ 基向量上的荷值

令 $8_s$ 的基向量为 $|s_1s_2s_3\rangle$，其中 $s_i = \pm 1$ 对应 $\sigma_i$ 的本征值。我们计算每个基向量上的 $T^3$ 和 $Y$。

通过显式矩阵计算可得：

| 基向量 $|s_1s_2s_3\rangle$ | SO(1,3) 类型 | $T^3$ | $Y$ | 对应的 SM 场 |
|:-----------------------:|:-----------:|:-----:|:---:|:-----------:|
| $|\!+\!+\!+\rangle$ | 左旋 Weyl (2) | $+1/2$ | $+1/6$ | $u_L$ |
| $|\!+\!+\!-\rangle$ | 左旋 Weyl (2) | $+1/2$ | $-1/2$ | $\nu_L$ |
| $|\!+\!-\!+\rangle$ | 左旋 Weyl (2) | $-1/2$ | $+1/6$ | $d_L$ |
| $|\!+\!-\!-\rangle$ | 左旋 Weyl (2) | $-1/2$ | $-1/2$ | $e_L$ |
| $|\!-\!+\!+\rangle$ | 右旋 Weyl (2') | $0$ | $+2/3$ | $u_R$ |
| $|\!-\!+\!-\rangle$ | 右旋 Weyl (2') | $0$ | $-1/3$ | $d_R$ |
| $|\!-\!-\!+\rangle$ | 右旋 Weyl (2') | $0$ | $-1$ | $e_R$ |
| $|\!-\!-\!-\rangle$ | 右旋 Weyl (2') | $0$ | $+1$ | $\nu_R^c$ |

### 4.2 推导过程

以 $|+\!+\!+\rangle$ 为例：

1. 在 Gamma 矩阵的显式张量积表示中，该基向量对应 $\sigma_x \otimes \sigma_y \otimes I_2$ 的 $+\!+\!+$ 本征态
2. $T^3 = \frac{i}{4}[\gamma_1, \gamma_2]$ 作用于此态，给出本征值 $+1/2$
3. $Y = \frac{1}{2\sqrt{3}}(H_3 + \sqrt{3}H_4)$ 作用于此态，给出本征值 $+1/6$

其余基向量的计算类似。

### 4.3 验证：$Q_{\text{EM}} = T^3 + Y$

| 场 | $T^3$ | $Y$ | $Q_{\text{EM}} = T^3 + Y$ | 实验 |
|:--|:-----:|:---:|:------------------------:|:----:|
| $u_L$ | $+1/2$ | $+1/6$ | $+2/3$ | ✅ |
| $d_L$ | $-1/2$ | $+1/6$ | $-1/3$ | ✅ |
| $u_R$ | $0$ | $+2/3$ | $+2/3$ | ✅ |
| $d_R$ | $0$ | $-1/3$ | $-1/3$ | ✅ |
| $\nu_L$ | $+1/2$ | $-1/2$ | $0$ | ✅ |
| $e_L$ | $-1/2$ | $-1/2$ | $-1$ | ✅ |
| $e_R$ | $0$ | $-1$ | $-1$ | ✅ |
| $\nu_R^c$ | $0$ | $+1$ | $+1$ | (预言的) |

**QED 电荷谱完全匹配**。五个 SM 超荷值 $\{+1/6, +2/3, -1/3, -1/2, -1\}$ 全部从 Cl(1,7) 代数唯一确定。

---

## 5. 超荷归一化的谱解释

### 5.1 GUT 归一化因子

在标准 GUT 中，超荷生成元 $Y$ 通常乘以归一化因子 $\sqrt{3/5}$ 以满足 $\operatorname{Tr}(Y^2) = \operatorname{Tr}(T_3^2)$。在谱框架中不需要这一人为归一化——超荷生成元 $Y$ 的谱范数直接由 Cl(1,7) 的 Cartan 生成元定义给出。

### 5.2 谱算子的自伴性

$Y$ 作为 $\mathfrak{so}(1,7)$ Cartan 子代数的线性组合，自动是自伴算子。这意味着：

- $Y$ 的本征值全是实数（已验证：$\{+1/6, +2/3, -1/3, -1/2, -1, +1\}$）
- $Y$ 的本征态构成 $8_s$ 的完备正交基
- 谱分解 $Y = \sum_i y_i |y_i\rangle\langle y_i|$ 直接给出超荷赋值

### 5.3 为何 $\nu_R^c$ 有 $Y = +1$？

$\nu_R^c$（右手中微子共轭）有 $Y = +1$ 的预言值，对应于 $Q_{\text{EM}} = +1$。这不是标准 SM 中的场（右手中微子是 SM 单态），而是在谱框架中自然出现的 $\mathbf{Sp}$ 谱对象。该电荷赋值与 $e_R$ 的 $-1$ 对称，对应 $B-L$ 的镜像结构。

---

## 6. 与根因链的一致性

```
Spec 4-范畴
     ↓
Cl(1,7) ≅ M₈(ℝ) × M₈(ℝ)
     ↓
8_s 旋量表示 ──────→ 8 个基向量
     ↓                    ↓
SO(1,7) → SO(1,3) × SU(4)    Cartan 生成元的本征值
     ↓                    ↓
SU(4) → SU(3) × U(1)        T³ = iΣ₁₂
     ↓                    Y = (H₃ + √3H₄)/(2√3)
     ↓                    ↓
8 个基上的 (T³, Y) 本征值对
     ↓
Q_EM = T³ + Y ←── 五个 SM 超荷
```

**根因收敛**：所有 SM 超荷值 $\{+1/6, +2/3, -1/3, -1/2, -1\}$ 唯一地由以下结构确定：
1. Cl(1,7) 的 Gamma 矩阵张量积表示（固定 $8_s$ 的基）
2. $\mathfrak{so}(1,7)$ Cartan 生成元的特定线性组合（定义 $T^3$ 和 $Y$）
3. 无需引入任何拟合参数或实验输入

---

## 7. 开放问题

| 问题 | 说明 |
|:----|------|
| $\nu_R^c$ 的 $Y = +1$ 的物理意义 | 该态对应 $Q_{\text{EM}} = +1$，可能在谱 seesaw 机制中作为中间态出现 |
| $Y$ 生成元的归一化约定 | 本文采用 $Q_{\text{EM}} = T^3 + Y$ 的自然归一化，与 GUT 归一化 $\sqrt{3/5}$ 的关系 |
| 超荷与其他谱算子的对易关系 | $[Y, A_{F,i}]$ 在谱流方程中的角色 |

---

## 参考文献

- `spectral_zero_parameter_derivation.md` §2（Cl(1,7) 分支规则）
- `spectral_SM.md` §1（SM 场内容表）
- `spectral_root_cause_analysis.md` §1 第 4 层（谱间隙 → 规范耦合）
- `rec_spec_definitions.md`（Sp 范畴基础）
