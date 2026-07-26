# 语境性层——Kochen-Specker 定理的预层无全局截面表述

**版本**：v0.2（2026-07-23）

**摘要**：本笔记将 Kochen-Specker 语境性定理翻译为谱框架中的层论表述。基为 $\mathbf{Sp}$ 的交换子范畴覆盖 $\{\mathbf{Sp}_{\text{com}}^{(i)}\}$（每个覆盖对应一个测量语境），纤维为 $\{0,1\}$ 真值赋值。K-S 定理等价于该预层无全局截面。v0.2 新增 **Peres-Mermin 方具体构造**——9 可观测量（$\sigma_x\otimes I$, $I\otimes\sigma_x$, $\sigma_x\otimes\sigma_x$ 等）在 6 个语境（3 行 + 3 列）上的矛盾证明：行乘积 $=+1$ 而列乘积 $=-1$，同一连乘不能同时等于两个值。

**前置依赖**：[`spectral_contextuality_experiment.md`](spectral_contextuality_experiment.md)（语境性实验匹配）。

---

## 1. 语境覆盖

**定义 1.1**（交换子范畴覆盖）。令 $\mathcal{C} = \{\mathbf{Sp}_{\text{com}}^{(1)}, \ldots, \mathbf{Sp}_{\text{com}}^{(k)}\}$ 是 $\mathbf{Sp}$ 的交换子范畴族，其中每个 $\mathbf{Sp}_{\text{com}}^{(i)}$ 由一组两两交换的谱对象构成。$\mathcal{C}$ 覆盖 $\mathbf{Sp}$ 当：
$$\bigcup_i \text{Obj}(\mathbf{Sp}_{\text{com}}^{(i)}) = \text{Obj}(\mathbf{Sp})$$

**注 1.1**。语境覆盖的存在性由 K-S 定理保证：如果存在一个交换子范畴覆盖整个 $\mathbf{Sp}$，则非语境隐变量模型存在。

---

## 2. Peres-Mermin 方（v0.2 新增）

### 2.1 9 可观测量

Peres-Mermin 方（1990）给出了 K-S 定理的最简证明之一，仅需 9 个可观测量：

| $\sigma_x \otimes I$ | $I \otimes \sigma_x$ | $\sigma_x \otimes \sigma_x$ |
|:--------------------:|:--------------------:|:--------------------------:|
| $I \otimes \sigma_y$ | $\sigma_y \otimes I$ | $\sigma_y \otimes \sigma_y$ |
| $\sigma_x \otimes \sigma_y$ | $\sigma_y \otimes \sigma_x$ | $\sigma_z \otimes \sigma_z$ |

**6 个语境**：3 行 + 3 列，每个语境中的 3 个可观测两两交换。

### 2.2 矛盾

对 $\{0,1\}$ 真值赋值 $v$，令 $+1$ 映射为 $1$，$-1$ 映射为 $0$（因为 $0$ 在乘法中吸收）：

- **行乘积**：每行 3 个可观测量乘积 $= +1$ → 在 $\mathbb{N}$ 中 $= 1$
- **列乘积**：前两列乘积 $= +1$，第三列乘积 $= -1$ → 在 $\mathbb{N}$ 中 $= 0$

因此所有行乘积连乘 $= 1$，所有列乘积连乘 $= 0$。但行连乘与列连乘是同一个连乘（每个可观测量恰好出现一次），矛盾。

---

## 3. 真值赋值预层

**定义 3.1**（真值赋值预层）。$\mathcal{F}: \mathcal{C}^{\text{op}} \to \mathbf{Set}$ 定义为：
- $\mathcal{F}(\mathbf{Sp}_{\text{com}}^{(i)}) = \{v: \text{Obj}(\mathbf{Sp}_{\text{com}}^{(i)}) \to \{0,1\} \mid v \text{ 是乘法同态}\}$
- 限制态射 $\mathcal{F}(\mathbf{Sp}_{\text{com}}^{(i)} \supseteq \mathbf{Sp}_{\text{com}}^{(j)})$：真值赋值的限制

对 PM 方：$\mathcal{F}(\text{RowA}) = \{v \mid v(A_1)v(A_2)v(A_3) = 1\}$，依此类推。

---

## 4. K-S 定理 = 无全局截面（严格证明）

**定理 4.1**（K-S 定理的 PM 证明）。对 Peres-Mermin 方覆盖 $\mathcal{C}_{\text{PM}}$，预层 $\mathcal{F}_{\text{PM}}$ 无全局截面：
$$\not\exists\, s \in \mathcal{F}_{\text{PM}}(\mathbf{Sp}) \quad \text{使得} \quad s|_{\text{RowA}}, s|_{\text{RowB}}, s|_{\text{RowC}}, s|_{\text{Col1}}, s|_{\text{Col2}}, s|_{\text{Col3}}$$

**证明**。已形式化为 `pm_presheaf_no_global_section` 定理：假设存在全局截面 $s$，则从 $s$ 构造 $PMContextProduct$——但 `pm_no_global_assignment` 证明这样的赋值不可能存在（行连乘 $=1$ 且 $=0$）。矛盾。$\square$

---

## 5. Lean 4 形式化方案

### 5.1 组件（v0.2）

| 组件 | 内容 | 状态 |
|:----|:-----|:----:|
| `PMObservable` (9 种) | $A_1, A_2, A_3, B_1, B_2, B_3, C_1, C_2, C_3$ | ✅ |
| `PMContext` (6 种) | RowA, RowB, RowC, Col1, Col2, Col3 | ✅ |
| `pmContextObjects` | 每个语境的可观测量集合 | ✅ |
| `PMTruthAssignment` | $\{0,1\}$ 真值赋值 | ✅ |
| `PMContextProduct` | 语境乘积约束 | ✅ |
| `pm_no_global_assignment` | **无全局赋值的严格证明**（行/列乘积矛盾） | ✅ **无 sorry** |
| `PMContextCover` / `PMPresheaf` | 语境覆盖 + 真值赋值预层 | ✅ |
| `pm_presheaf_no_global_section` | **K-S 定理 = 预层无全局截面** | ✅ **无 sorry** |

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.2** | **2026-07-23** | **深化**：新增 Peres-Mermin 方具体构造（9 可观测量 × 6 语境）；`pm_no_global_assignment` 行/列乘积矛盾严格证明（$1\neq0$）；`pm_presheaf_no_global_section` 无 `sorry`；完整定理链：假设全局截面 → 构造赋值 → 导出矛盾 |
| **v0.1** | **2026-07-23** | 初始版本：语境覆盖定义；真值赋值预层；K-S 无全局截面定理（占位符）|
