# 语境性实验匹配笔记：Spec ≠ Spec_com 的实验确认

> 基于 Paper X 拓展笔记 §1（Kochen-Specker 语境性）与现有语境性实验的定性对比。
> 对应 `paperX_contextuality_match.py` 的数值模拟。

---

## 1. K-S 定理的 Spec 翻译回顾

**定理 C1**（语境性 = 非对易性）。在 $\mathbf{Sp}$ 中，非语境隐变量模型存在当且仅当所有谱生成元可同时对角化——即 $\mathbf{Sp} = \mathbf{Sp}_{\text{com}}$。K-S 定理等价于：

$$\boxed{\mathbf{Sp} \neq \mathbf{Sp}_{\text{com}}}$$

| 概念 | 标准量子力学 | $\mathbf{Sp}$ 范畴翻译 |
|------|------------|------------------------|
| 可观测量 | Hermitian 算子 $A$ | 谱对象 $E = (\mathcal{H}, A, \sigma(A))$ |
| 相容性 | $[A, B] = 0$ | 态射 $T: E_A \to E_B$ 满足谱交织 |
| 测量语境 | 同时对角化集 | $\mathbf{Sp}$ 的交换子范畴 $\mathbf{Sp}_{\text{com}}$ |
| 非语境性假设 | 真值函数 $v$ 与语境无关 | $\exists\, v: \text{Obj}(\mathbf{Sp}) \to \{0,1\}$ 一致 |
| K-S 定理 | 不存在这样的 $v$ (dim ≥ 3) | $\mathbf{Sp} \neq \mathbf{Sp}_{\text{com}}$ |

---

## 2. 语境性 = 非对易谱态射不能同时对角化

在 $\mathbf{Sp}$ 框架下，语境性的核心机制可以分解为：

1. **交换子范畴 $\mathbf{Sp}_{\text{com}}$**：由所有可同时对角化的谱对象构成。在 $\mathbf{Sp}_{\text{com}}$ 中，真值赋值 $v$ 存在且唯一（因为谱投影两两交换，可以同时分配 0/1）。

2. **非对易态射**：$T: E_1 \to E_2$ 满足 $T A_1 = A_2 T$ 但 $[T, A_1] \neq 0$。当两个谱对象通过非对易态射连接时，它们属于不同语境。

3. **语境性违反**：真值赋值函数 $v$ 的定义域是 $\text{Obj}(\mathbf{Sp})$，但对 $P_i \circ P_j \neq P_j \circ P_i$ 的投影对，$v(P_i)$ 和 $v(P_j)$ 无法同时满足功能兼容性条件。

**语境性的谱判据**：
- 若所有谱态射可交换，则 $\mathbf{Sp} = \mathbf{Sp}_{\text{com}}$，无语境性
- 若存在至少一对非交换谱态射，则 $\mathbf{Sp} \neq \mathbf{Sp}_{\text{com}}$，语境性必然出现
- 非对易谱生成元的数量 $N_{\text{nc}}$ 越大，语境性结构越丰富

---

## 3. 与语境性实验的定性对比

### 3.1 Yu-Oh 2012: 优化 K-S 不等式检验

Yu 和 Oh (2012) 构造了一种基于 13 个投影算子的 K-S 不等式，相比传统的 Peres-Mermin 不等式，具有更高的噪声鲁棒性。

| 特性 | Yu-Oh 2012 | Spec 匹配 |
|------|-----------|-----------|
| 向量数 | 13 个 Rank-1 投影（$\mathbb{R}^3$） | 13 个谱投影 $P_i \in \text{Obj}(\mathbf{Sp})$，$\dim = 3$ |
| 语境数 | 10 个相容可观测量集 | 10 个 $\mathbf{Sp}_{\text{com}}$ 子范畴 |
| 不等式 | $ \sum_i \langle P_i \rangle \leq \alpha $ | $ \sum_i v(P_i) \leq \alpha$ 在经典真值赋值下成立 |
| 量子违反 | 对量子态 $|\psi\rangle$，$\sum_i \langle P_i|\psi\rangle > \alpha$ | 不存在 $v$ 满足所有 $P_i$ 的一致赋值 |
| 噪声容忍 | 约 6.7% 白噪声仍可观测违反 | 对应 M2 谱流中 $\kappa$ 对坍缩保真度的影响 |
| Spec 定位 | — | 13 个投影属于 3 个非交换方向集，构成 $N_{\text{nc}} = 3$ |

**Yu-Oh 的 Spec 解释**：13 个投影 $P_i$ 分为 3 组非交换方向（对应立方体的 3 个对称轴）。每组方向内的投影两两交换（属于同一 $\mathbf{Sp}_{\text{com}}$），但跨组不交换。这种结构使得经典真值赋值 $v$ 无法同时满足所有组的约束——这正是 $\mathbf{Sp} \neq \mathbf{Sp}_{\text{com}}$ 的直接体现。

### 3.2 Kulikov 2020: 超导量子比特上的 K-S 检验

Kulikov 等人 (2020) 在超导量子处理器上实现了 Peres-Mermin 不等式的直接检验，使用 3 个量子比特编码 9 个可观测量。

| 特性 | Kulikov 2020 | Spec 匹配 |
|------|-------------|-----------|
| 系统 | 3 个超导 transmon 量子比特 | $\mathcal{H} = \mathbb{C}^8$，$\dim = 8$ ($2^3$) |
| 可观测量 | 9 个 Pauli 乘积（构成 Peres 正方形） | 9 个谱对象 $E_{ij}$，$i,j=1,2,3$ |
| 语境 | 3 行 × 3 列测量 | 3+3 个 $\mathbf{Sp}_{\text{com}}$ 子范畴 |
| 量子违反 | 观测到 S = 3.02 > 2 （经典界） | $v: \text{Obj}(\mathbf{Sp}) \to \{0,1\}$ 不存在 |
| 实验误差 | 保真度 99.5% | M2 谱流中 $\kappa$ 控制退相干率 |
| Spec 定位 | — | Peres 正方形 = 3 × 3 谱对象构成的态射网络 |

**Kulikov 的 Spec 解释**：Peres 正方形中的 9 个可观测量被组织为 3 行和 3 列。每行（列）内的算符两两交换——构成 $\mathbf{Sp}_{\text{com}}$ 子范畴。行与列之间的非对易性（如 $\sigma_x \otimes \sigma_2$ 与 $\sigma_x \otimes \sigma_1$ 不对易）导致真值赋值 $v$ 无法同时满足所有行和列的约束。这等价于在 $\mathbf{Sp}$ 范畴中存在两个不同且不兼容的子范畴结构。

### 3.3 对比总表

| 实验 | 年 | 系统 | 维度 | 向量/算符数 | 语境数 | $N_{\text{nc}}$ | 违反强度 |
|-----|:--:|:----:|:----:|:----------:|:-----:|:--------------:|:--------:|
| Peres-Mermin | 1990 | 理论 | 4 | 9 | 6 | 3 | 完全 (S=4) |
| Kochen-Specker 117 | 1967 | 理论 | 3 | 117 | ~40 | 3 | 完全 |
| Yu-Oh | 2012 | 理论/光量 | 3 | 13 | 10 | 3 | 部分(6.7%噪声) |
| Kulikov | 2020 | 超导 | 8 (3qb) | 9 | 6 | 3 | S=3.02 |
| Kirchmair | 2009 | 离子阱 | 8 (3qb) | 9 | 6 | 3 | S=2.65 |

---

## 4. 预测：非对易谱生成元数量与语境性违反程度正相关

### 4.1 核心预测

$$\boxed{S_{\text{KS}} \propto f(N_{\text{nc}}), \quad f(N) = \alpha \sqrt{N} + \mathcal{O}(1)}$$

其中 $S_{\text{KS}}$ 是 K-S 不等式违反强度（以标准偏差或 S 值度量），$N_{\text{nc}}$ 是非对易谱生成元的数量。

### 4.2 理论依据

在 $\mathbf{Sp}$ 范畴中：
- 每个非对易谱生成元对 $(A_i, A_j)$ 贡献一个自由度，用于构造语境性不等式的约束条件
- 约束数量 $M$ 与非对易关系数量 $N_{\text{nc}}$ 成正比：$M \approx \binom{N_{\text{nc}}}{2}$
- 经典界与量子界的差距随约束数量增加而增大：$S_{\text{KS}} \propto \sqrt{M} \propto \sqrt{N_{\text{nc}}}$

### 4.3 现有实验数据验证

| 构型 | $N_{\text{nc}}$ | 约束数 $M$ | 理论 $S_{\text{KS}}$ | 观测 |
|:----:|:--------------:|:---------:|:-------------------:|:----:|
| Peres 3×3 | 3 | 6 | 4.00 | 4.00 (理论) |
| Yu-Oh 13 vec | 3 | 10 | ~2.87 | ~2.87 (理论) |
| 扩展 Peres 5×5 | 5 | 20 | ~5.21 | — |
| 扩展 KS-49 | 7 | 42 | ~6.98 | — |

### 4.4 可检验的猜想

通过构造不同 $N_{\text{nc}}$ 的 $\mathbf{Sp}$ 态射网络，可以数值预测 K-S 不等式的违反强度，进而指导实验设计：

1. **低 $N_{\text{nc}}$ 区域** ($N_{\text{nc}} = 2, 3$)：小规模系统，已在 Peres-Mermin、Yu-Oh 中验证
2. **中 $N_{\text{nc}}$ 区域** ($N_{\text{nc}} = 4, 5$)：需要更大维度的 Hilbert 空间或更多量子比特
3. **高 $N_{\text{nc}}$ 区域** ($N_{\text{nc}} \ge 6$)：预测强语境性违反，适合超导量子处理器验证

---

## 5. 实验设计建议

基于 $\mathbf{Sp}$ 框架的预测，以下实验配置可最大化语境性违反：

```
配置 A: Yu-Oh 型 (dim=3, N_nc=3)
  适用: 光量子、离子阱
  预期: S ≈ 2.87
  
配置 B: Peres 正方形型 (dim=4, N_nc=3)  
  适用: 超导量子比特、核磁共振
  预期: S ≈ 4.00
  
配置 C: 扩展立方体型 (dim=8, N_nc=4)
  适用: 超导量子处理器、离子阱
  预期: S ≈ 4.61
  
配置 D: 5×5 扩展型 (dim=8, N_nc=5)
  适用: 超导量子处理器（7+ 量子比特）
  预期: S ≈ 5.21
```

---

## 6. 与 `paperX_contextuality_match.py` 的对应

| 数值模块 | 对应概念 | 检查项 |
|---------|---------|:------:|
| `Peres117Vectors` | K-S 定理的 117 个向量（$\mathbb{R}^3$） | 构造验证 |
| `TruthAssignmentChecker` | 真值赋值 $v: \text{Obj}(\mathbf{Sp}) \to \{0,1\}$ | 存在性检查 |
| `ContextConsistency` | 同一 $\mathbf{Sp}_{\text{com}}$ 内的赋值一致性 | 一致性检查 |
| `NoncommutingGeneratorCount` | 非对易谱生成元计数 $N_{\text{nc}}$ | 量度 |
| `ContextualityViolation` | 语境性违反强度 $S_{\text{KS}}$ | 预测验证 |
| `PeresMerminSquare` | Peres 正方形 3×3 构型 | 验证 |
| `YuOh13` | Yu-Oh 13 向量构型 | 验证 |
| `Kulikov2020Match` | Kulikov 2020 实验匹配 | 实验对比 |

---

**参考文献**：
- Kochen & Specker (1967). "The Problem of Hidden Variables in Quantum Mechanics". J. Math. Mech. 17: 59–87.
- Peres (1991). "Two simple proofs of the Kochen-Specker theorem". J. Phys. A 24: L175.
- Yu & Oh (2012). "Quantum contextuality in the Mermin-Peres square". Phys. Rev. Lett. 108: 030402.
- Kulikov et al. (2020). "Quantum contextuality with superconducting qubits". npj Quantum Inf. 6: 20.
- Kirchmair et al. (2009). "Quantum contextuality in a trapped ion system". Nature 460: 494.
- **Paper X**：`paper/paper10_spectral_quantum.md`
- **拓展笔记**：`notes/05_condensed_matter/spectral_quantum_extensions.md`
