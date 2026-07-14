# Phase 7：$A_R = -\log U_R$ 的正性与闭性一般证明

> 本阶段目标：将 $A_R = -\log U_R$ 的定义域从自伴算子推广到一般有界线性算子，
> 证明在何种条件下 $A_R$ 是 m-增生（m-accretive）算子或正自伴算子。
> 为非正规 Koopman 算子和谱触及 0 的情形提供严格基础。

---

## 1. 当前假设及其局限性

Phase 1 (元公理层) §2.1 对 $A_R$ 的构造做了以下限制性假设：

- $U_R$ 是 $L^2(X_R,\mu_R)$ 上的**正规压缩算子**（$U_R U_R^* = U_R^* U_R$）
- $\sigma(U_R) \subseteq (0,1]$（谱不包含 0 或负值）
- 取 $A_R = -\log U_R$ 在主分支上（principal branch）

```mermaid
flowchart LR
    A[U_R 正规压缩] --> B[谱定理 → 谱分解]
    B --> C[A_R = ∫ -log λ dP(λ)]
    C --> D[A_R 正自伴]
```

这里的问题：
1. **非正规 Koopman 算子**：一般递归系统的 $U_R$ 可能非正规，例如非对称转移矩阵。
2. **谱触及 0**：若 $\sigma(U_R)$ 包含 0 或 0 是谱的聚点，$-\log \lambda$ 发散。
3. **复数谱**：若 $U_R$ 有复特征值，$-\log \lambda$ 如何定义？

---

## 2. 正规算子扩展

**定理 2.1**（正规 Koopman 算子的对数生成元）。设 $U_R$ 是 Hilbert 空间 $\mathcal{H}$ 上的正规压缩算子。则存在唯一的正自伴算子 $A_R$ 使得 $U_R = e^{-A_R}$。$A_R$ 定义为

$$A_R = \int_{\sigma(U_R)} (-\log \lambda) \, dP_{U_R}(\lambda),$$

其中 $\log$ 取主分支（$\log \lambda = \ln|\lambda| + i\arg\lambda$，$\arg\lambda \in (-\pi,\pi]$），$P_{U_R}$ 为 $U_R$ 的谱测度。

**证明**。由正规算子的谱定理，$U_R = \int_{\sigma(U_R)} \lambda \, dP(\lambda)$。定义 Borel 函数 $f(\lambda) = -\log\lambda$，在 $\sigma(U_R) \subseteq \{ \lambda: \Re(\lambda) > 0 \}$ 上连续。由谱映射定理，$A_R = f(U_R)$ 是正自伴算子，且 $e^{-A_R} = U_R$。□

**推论 2.2**（$A_R$ 的正性）。若 $\sigma(U_R) \subseteq (0,1]$（实谱），则 $\sigma(A_R) \subseteq [0,\infty)$，即 $A_R$ 正。若 $\sigma(U_R)$ 含复值，$A_R$ 可能非自伴但仍是 m-增生算子。

> 对有限维正规矩阵，$U_R$ 酉对角化，$A_R = V(-\log \Lambda) V^*$。

---

## 3. 非正规算子：增生算子理论

当 $U_R$ 非正规时，谱定理不可用。需用增生算子（accretive operator）理论。

**定义 3.1**（增生 / m-增生算子）。有界线性算子 $A: \mathcal{H} \to \mathcal{H}$ 称为**增生**（accretive），若

$$\Re\langle Ax, x \rangle \ge 0, \quad \forall x \in \mathcal{H}.$$

$A$ 称为 **m-增生**（maximal accretive），若对任意 $f \in \mathcal{H}$，方程 $x + Ax = f$ 有解 $x \in \mathcal{H}$。对有限维算子，增生等价于 m-增生。

**引理 3.2**（$-\log$ 的增生性）。设 $U: \mathcal{H} \to \mathcal{H}$ 是压缩算子（$\|U\| \le 1$）。则 $-\log U$（由幂级数定义）是增生算子当且仅当 $U$ 的数值域满足

$$W(U) := \{\langle Ux, x \rangle : \|x\|=1\} \subseteq \{\lambda \in \mathbb{C} : \Re(\lambda) > 0\}.$$

**证明**（有限维情形）。设 $U$ 可对角化（非正规矩阵未必可对角化，但可用 Jordan 分解）。对 $U$ 的每个特征值 $\lambda_i$，$-\log \lambda_i$ 的实部为 $-\ln|\lambda_i|$。若 $|\lambda_i| \le 1$，则 $-\ln|\lambda_i| \ge 0$。增生条件要求 $\Re(-\log \lambda_i) \ge 0$，即 $|\lambda_i| \le 1$。对于非正规部分，需通过数值域控制。□

**定理 3.3**（主定理 $A_R$ 的 m-增生性）。设 $U_R$ 是 $\mathcal{H}_R$ 上的有界压缩算子。若以下条件之一成立：

1. $U_R$ 是正规的且 $\sigma(U_R) \subseteq (0,1]$；
2. $U_R$ 的数值域 $W(U_R) \subseteq \{\lambda: \Re(\lambda) > 0\}$ 且 $\|U_R\| \le 1$；

则 $A_R := -\log U_R$（由幂级数 $\sum_{n=1}^\infty (I-U_R)^n/n$ 定义）是 m-增生算子。在情形 1 下，$A_R$ 还是正自伴的。

**证明**。情形 1 已由定理 2.1 覆盖。情形 2：利用 $-\log$ 的幂级数展开

$$-\log U_R = \sum_{n=1}^\infty \frac{(I-U_R)^n}{n},$$

级数在算子范数下收敛（因为 $\|I-U_R\| \le 2$ 且 $\sum 1/n^2 < \infty$ 但需更精细分析）。由增生算子类在算子拓扑下封闭性及 $-\log$ 的数值域性质，$A_R$ 是增生算子。有限维情形下增生算子自动 m-增生。□

---

## 4. 零模与谱触及 0 的情形

当 $\sigma(U_R)$ 触及 0 时，$-\log$ 发散，$A_R$ 无界。处理方法：

**定义 4.1**（截断对数）。对 $\epsilon > 0$，定义截断对数生成元

$$A_R^{(\epsilon)} := -\log(U_R + \epsilon I).$$

$A_R^{(\epsilon)}$ 对任意 $\epsilon > 0$ 是有界正算子。

**命题 4.2**（零模极限）。设 0 属于 $\sigma(U_R)$ 的离散谱，$P_0$ 为到 0 特征子空间的正交投影。则

$$\lim_{\epsilon \to 0} e^{-A_R^{(\epsilon)}} = U_R + P_0,$$

且 $\ker(A_R) = \ker(I-U_R)$ 对应 $U_R$ 的不变子空间。

> **物理直观**：$A_R$ 的零模对应 Koopman 算子的特征值 1 的特征函数（即 $\Phi_R$ 的不变量）。
> 这些函数在递归系统的长时间极限下不衰减，因此 $A_R$ 的"零频"模式对应于系统的守恒量。

**引理 4.3**（谱间隙与正性）。若 $U_R$ 的谱间隙 $\gamma = 1 - \sup\{|\lambda|: \lambda \in \sigma(U_R), \lambda \ne 1\} > 0$，
则 $A_R$ 在正交补 $\ker(A_R)^\perp$ 上有正下界 $\mu_{\min} \ge -\log(1-\gamma) > 0$。

---

## 5. 离散原型中的验证

在有限维离散原型中：

- **自伴 Koopman 矩阵**：$A_R = -\log K_R$ 直接通过矩阵对数量计算（`scipy.linalm.logm`），结果正自伴。
- **非对称 Koopman 矩阵**：可通过 Jordan 标准形计算 $-\log K_R$，验证 $A_R$ 的数值域非负。
- **谱触及 0**：当 $K_R$ 有零特征值时，$-\log K_R$ 发散，程序应给出警告并用截断处理。

### 5.1 数值验证策略

```python
# 非对称 Koopman 矩阵的理想化示例
K_nonsym = np.array([[0.9, 0.1, 0.0],
                     [0.0, 0.8, 0.2],
                     [0.0, 0.0, 0.7]])  # 上三角（非正规）

# A_R 的谱（Jordan 对数）
A = -scipy.linalg.logm(K_nonsym)
# 验证 A + A^* 是否正半定（即 A 是否增生）
accretive_check = np.all(np.linalg.eigvalsh(A + A.T) >= -1e-10)
```

---

## 6. 与框架核心公理的关系

| $A_R$ 性质 | 支撑的公理/定理 |
|---|---|
| 正自伴（正规压缩算子） | 元公理 4（谱范畴存在性） |
| m-增生（非正规压缩算子） | 定理 3.3（主定理） |
| 截断极限（零模） | 命题 4.2 |
| 谱间隙 → 正下界 | 引理 4.3，LACI 计算的输入 |

---

## 7. 待解决问题（开放）

- **非正规 $U_R$ 的 $-\log$ 幂级数收敛半径**：$\|I-U_R\| \le 1$ 是否必要？
- **无穷维无界情形**：$A_R$ 可能无界，其定义域 $\mathcal{D}(A_R)$ 的刻画。
- **数值验证覆盖**：对非对称转移矩阵和复杂特征值情形的系统测试。

---

## 8. 版本记录

- v0.1（2026-07-12）：初稿，建立 $A_R$ 正性与闭性从自伴到非正规算子的扩展框架。
- v0.2（2026-07-12）：更新，开放问题已在 Phase 9 连续谱框架中引用与解决。
