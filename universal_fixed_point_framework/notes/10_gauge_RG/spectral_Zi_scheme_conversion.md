# S₁→S₂ 方案转换因子 Z_i 的谱推导

> **目标**：建立从 S₁ 层裸耦合 $\alpha_i^{(0)} = \Delta\lambda_i/(4\pi)$ 到 S₂ 层物理耦合 $\alpha_i^{\text{(phys)}}$ 的方案转换因子 $Z_i$，使其与根因链一致。
>
> **承袭**：根因链第 4 层（S₁：谱间隙→裸耦合）和第 4a 层（S₂：态射→RGE 跑动）的中间环节。

---

## 1. 问题

数值验证（`spectral_rge_running.py`）发现：

$$\alpha_s^{\text{(phys)}}(M_Z) = 0.0328 \quad \text{vs 实验} \quad 0.1179 \quad (\text{偏差 } -72\%)$$

根因链约束 $\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = \sqrt{2/3}:1:\sqrt{2}$ 不可调整。偏差来源不在 RGE 跑动本身（已跑至三圈），而在 S₁→S₂ 的**方案转换**：

$$\alpha_i^{\text{(phys)}} \neq \frac{\Delta\lambda_i}{4\pi}$$

必须有额外的有限重整化因子 $Z_i$。

---

## 2. DS 顶点减除提供的结构

Paper V §6.2 和 `paper31_threeloop_beta.py` 已证明：

1. 谱流对易子展开 $[G, [G, \ldots, [G, A]]]$ 的 $n$ 圈朴素 β 函数比 SM β 函数多一个 $C_A$ 因子
2. Dyson-Schwinger 顶点减除每阶去除一个 $C_A$，使 $\beta_n^{\text{(spec)}} = \beta_n^{\text{(SM)}}$
3. 该模式在 1/2/3 圈均 12/12 数值验证通过

**关键观察**：DS 顶点减除修正的是 β 函数的**结构**（群因子），而非其**数值**。这意味着在 M_Pl 能标，裸耦合 $\alpha_i^{(0)}$ 和物理耦合 $\alpha_i^{\text{(phys)}}$ 之间也存在由相同对易子结构决定的转换关系。

### 2.1 裸耦合与物理耦合的对易子关系

在谱框架中，规范耦合的"强度"不是任意参数，而是谱对易子 $[A_i, A_j]$ 的范数。设：

- $A_i$ 是第 $i$ 个规范群的谱生成元（对象，$S_1$ 层）
- $f_{ij}: A_i \to A_j$ 是连接不同谱生成元的态射（1-态射，$S_2$ 层）

裸耦合 $\alpha_i^{(0)}$ 来自 $A_i$ 的谱间隙 $\Delta\lambda_i$（$S_1$ 层量）。物理耦合 $\alpha_i^{\text{(phys)}}$ 来自对易子 $[A_i, A_j]$ 的谱范数（$S_2$ 层量）。

### 2.2 启发式推导

对 $SU(N)$ 规范群，对易子 $[A_i, A_j]$ 的谱范数正比于结构常数 $f^{abc}$ 的 $C_A$ 因子：

$$\|[A_i, A_j]\|_{\text{HS}} \propto C_A \cdot \|A_i\|_{\text{HS}}$$

DS 减除去除一个 $C_A$ 因子意味着物理耦合与裸耦合的关系为：

$$\alpha_i^{\text{(phys)}} = \frac{\Delta\lambda_i}{4\pi} \cdot \frac{1}{1 + \kappa_i \cdot C_A \cdot \alpha_i^{(0)}}$$

其中 $\kappa_i$ 是 DS 减除的剩余项系数。

### 2.3 数值约束

从 $\alpha_s(M_Z)$ 的实验值和 RGE 反向跑动，可反推 M_Pl 处所需的物理耦合：

$$\alpha_s^{\text{(phys)}}(M_{\text{Pl}}) \approx 0.0198 \quad (\text{来自 } \alpha_s(M_Z)=0.1179 \text{ 的 1-loop 反向})\\
\alpha_s^{(0)}(M_{\text{Pl}}) = 0.0137 \quad (\text{来自 } \Delta\lambda = \sqrt{2} \cdot 0.122/(4\pi))$$

所需的转换因子：

$$Z_3 = \frac{\alpha_s^{\text{(phys)}}}{\alpha_s^{(0)}} \approx \frac{0.0198}{0.0137} \approx 1.445$$

同理对 $SU(2)$ 和 $U(1)$：

$$Z_2 \approx 5.27,\quad Z_1 \approx 3.66$$

---

## 3. Z_i 的 DS 对易子推导

### 3.1 问题形式化

设 $\mathcal{A} = \{A_1, A_2, A_3\}$ 为三个规范谱生成元。完整谱对象 $A \in \mathbf{Spec}$ 包含 $\mathcal{A}$ 和引力谱生成元 $A_{\text{GR}}$。

谱对易子的 Jacobi 恒等式：

$$[A_i, [A_j, A_k]] + [A_j, [A_k, A_i]] + [A_k, [A_i, A_j]] = 0$$

DS 顶点减除的物理含义是：从 $[A_i, [A_j, A_k]]$ 中减去 $[A_i, [A_j, A_k]]_{\text{overlap}}$ 中与低阶对易子重叠的部分。

### 3.2 单圈 DS 减除

裸耦合 $\alpha_i^{(0)}$ 的 1-loop β 函数与 SM 无差异，因此单圈无 DS 减除：

$$\alpha_i^{\text{(phys)}} = \alpha_i^{(0)} + \mathcal{O}((\alpha_i^{(0)})^2)$$

### 3.3 双圈 DS 减除 → Z_i 的 O(α) 修正

双圈对易子 $[A_j, [A_j, A_i]]$ 的范数比 SM 预期多一个 $C_A$ 因子。DS 减除使：

从 $S_1$ 层到 $S_2$ 层的转换中，双圈态射复合 $f_{jk} \circ f_{ki}$ 的强度减半（去除一个 $C_A$）：

$$\alpha_i^{\text{(phys)}} = \alpha_i^{(0)} \left[1 + \delta_i^{\text{(DS)}} \cdot \alpha_i^{(0)} + \mathcal{O}((\alpha_i^{(0)})^2)\right]$$

其中 $\delta_i^{\text{(DS)}}$ 是 DS 顶点减除的剩余系数。对 $SU(3)$：

$$\delta_3^{\text{(DS)}} = \frac{C_A}{4\pi} \quad (\text{来自双圈 DS 减除的归一化})$$

代入 $\alpha_s^{(0)} = 0.0137$：

$$\alpha_s^{\text{(phys)}} \approx 0.0137 \left[1 + \frac{3}{4\pi} \cdot 0.0137\right] = 0.0137 \times 1.0033 \approx 0.01374$$

这仅带来 0.3% 的修正，远不足以解释 44.5% 的所需修正。

### 3.4 结论：单圈 DS 不足以解释 Z_i

纯 DS 对易子减除仅产生 $\mathcal{O}(\alpha) \sim 1\%$ 的修正。这与 -72% 的偏差不匹配。

这意味着 Z_i 的来源不是 DS 对易子减除（微扰），而是 $S_2$ 层的一个**非微扰**效应——类似于 $\Lambda$ 推导中 $S_2$ 作为 $e^{-2\pi/\alpha}$ 的指数压制。

---

## 4. 类 Λ 的 S₂ 非微扰方案转换

在 $\Lambda$ 推导中：

$$\rho_\Lambda = \rho_{\text{bare}} \cdot S_2^{(\text{eff})}, \quad S_2 = e^{-2\pi/\alpha_{\text{eff}}}$$

类似地，对规范耦合的 $S_1 \to S_2$ 转换：

$$\alpha_i^{\text{(phys)}} = \alpha_i^{(0)} \cdot \frac{1}{1 - \eta_i \cdot e^{-2\pi/\alpha_i^{(0)}}}$$

其中 $\eta_i$ 是 $\mathcal{O}(1)$ 的群论系数。

当 $\alpha_i^{(0)} \approx 0.01$ 时，$e^{-2\pi/0.01} \approx 10^{-273}$，可忽略。因此这个机制也不行。

---

## 5. 真正的答案：4π 归一化因子

退回最基础的出发点。$\alpha = \Delta\lambda/(4\pi)$ 中的 $4\pi$ 来自何处？

在标准的规范理论中，耦合常数 $g$ 通过作用量中的 $-\frac{1}{4g^2}F_{\mu\nu}F^{\mu\nu}$ 进入。谱框架中，谱生成元 $A_i$ 的谱间隙 $\Delta\lambda_i$ 是 $A_i$ 的特征值之差。

$4\pi$ 的来源：

1. **$\alpha = g^2/(4\pi)$**：这是 QED 以来的习惯定义
2. **$\alpha = \Delta\lambda/(4\pi)$**：这是谱框架将其对齐的翻译

但 $\Delta\lambda_i$ 的数值（$0.0996, 0.1222, 0.1725$）和 $g_i^2$ 无关——**$4\pi$ 是一个归一化约定**，不是物理推导。

**推论**：$\alpha_i = \Delta\lambda_i/(4\pi)$ 不是谱框架的第一原理结论，而是$S_2$ 层态射归一化约定。$Z_i$ 就是修正这个约定的方案转换。

### 5.1 $4\pi$ 的谱起源

在 $\mathbf{Spec}$ 范畴中，谱生成元 $A_i$ 的 Hilbert-Schmidt 范数 $\|A_i\|_{\text{HS}}$ 与其谱间隙的关系为：

$$\|A_i\|_{\text{HS}}^2 = \sum_k \lambda_k^2 \propto \Delta\lambda_i^2 \cdot \dim\mathcal{H}_i$$

物理耦合 $g_i$ 通过态射 $f: A_i \to \psi$（规范玻色子到费米子的耦合）定义。态射的强度由谱对易子 $[A_i, \psi]$ 的范数决定：

$$g_i \propto \|[A_i, \psi]\|_{\text{HS}}$$

这里出现了一个**额外的归一化因子**——它来自 $S_2$ 层态射复合的测度，不是 $S_1$ 层谱间隙的简单除法。

---

## 6. 开放问题

| 问题 | 状态 | 路径 |
|:----|:----|:-----|
| Z_i 的显式 DS 公式 | 🔴 未推导 | 需从 $[A_i, [A_j, A_k]]$ 的 HS 范数比计算 |
| $4\pi$ 的范畴起源 | 🟡 半定量 | 涉及 $\mathbf{Spec}$ 的态射空间维数 |
| Z_i 的数值预测 | 🔴 未计算 | 需 $SU(3)$ 对易子空间的显式谱分解 |

---

## 参考文献

- `spectral_root_cause_analysis.md` §4/§4a（根因链）
- `paper31_threeloop_beta.py`（DS 顶点减除验证）
- `spectral_rge_running.py`（数值偏差诊断）
- `spectral_RG_open_problems.md`（RGE 开放问题）
