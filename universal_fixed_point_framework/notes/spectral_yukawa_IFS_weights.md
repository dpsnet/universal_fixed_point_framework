# IFS Yukawa权重：m_μ/m_τ偏差的根因与解决路径

## 1. 问题定位

Phase 50 的 α 公式（$m_i = c_i^\alpha$）假设了 IFS 等权重 $p_1 = p_2 = p_3$。
实际需要的权重比（从实验值反推）：

| 扇区 | $p_2/p_3$ | 含义 |
|:----|:--------:|:----|
| 轻子 | 2.36 | 第二代 Yukawa 耦合比第三代强 |
| 上型 | 1.43 | 上型第二代略强 |
| 下型 | 0.62 | 下型第二代弱于第三代 |

权重 $p_i$ 正是 Yukawa 矩阵 $Y_f = \operatorname{diag}(y_1, y_2, y_3)$ 的特征值（归一化到 $y_3$）。

---

## 2. 完整质量公式

$$m_i^{(f)} = y_i^{(f)} \cdot c_i^{\alpha_f}$$

其中 $y_i^{(f)}$ 是扇区 $f$ 的第 $i$ 代 Yukawa 特征值。Phase 50 的等权重假设对应 $y_i^{(f)} = 1$。

---

## 3. Yukawa 特征值的数据模式

从实验值计算 $y_i = m_i / (c_i^\alpha)$：

| 代 | 轻子 $y_i$ | 归一化 | 上型 $y_i$ | 归一化 | 下型 $y_i$ | 归一化 |
|:-:|:---------:|:-----:|:---------:|:-----:|:---------:|:-----:|
| 1 | 0.00475 | 0.656 | 0.00138 | 0.917 | 0.00355 | 4.18 |
| 2 | 0.0169 | 2.34 | 0.00215 | 1.43 | 0.000527 | 0.620 |
| 3 | 0.00724 | 1.00 | 0.00150 | 1.00 | 0.000850 | 1.00 |

轻子和上型的模式相近（$y_2 > y_3 > y_1$），下型不同（$y_1 > y_3 > y_2$）。

---

## 4. Yukawa矩阵的IFS约束

在 IFS 有限谱三元组中，生成元 $U_i$ 作用于 $M_3(\mathbb{C})$（代空间矩阵代数）。

$D_F$ 的 IFS 自相似方程：
$$D_F = \bigoplus_{i=1}^3 c_i^\alpha \cdot U_i D_F U_i^*$$

约化到代空间 $M_3(\mathbb{C})$ 给出 Yukawa 矩阵 $Y_f$ 的方程：
$$Y_f = \sum_i c_i^{\alpha_f} \cdot U_i Y_f U_i^*$$

此方程的解空间（满足谱三元组第一阶条件 $[D_F, a] = 0$ 的子空间）决定允许的 $Y_f$ 模式。

### 4.1 特殊情况：$\mathbb{Z}_3$ 对称性

若 $U_i$ 构成 $\mathbb{Z}_3$ 的表示（$U_1 = I, U_2 = \omega I, U_3 = \omega^2 I$，$\omega = e^{2\pi i/3}$），
则 $Y_f$ 的限制方程为 $Y_f = c_i^{\alpha_f} Y_f$，仅在 $\alpha_f = 0$ 时非平凡。

### 4.2 一般情况：非交换生成元

更一般的 $U_i$ 不构成交换群时，方程 $Y_f = \sum_i c_i^{\alpha_f} U_i Y_f U_i^*$ 的解由 $U_i$ 的表示结构和收缩因子 $c_i^\alpha$ 共同决定。这等价于 $Y_f$ 在超算子 $\Phi(X) = \sum_i c_i^{\alpha_f} U_i X U_i^*$ 下的不动点。

超算子 $\Phi$ 的特征值问题：
$$\Phi(X) = \lambda X$$

决定允许的 Yukawa 模式。主特征值 $\lambda = 1$ 对应解空间中的 Yukawa 矩阵。

---

## 5. 推进路径

| 步骤 | 内容 | 难度 |
|:----|:----|:---:|
| 1 | 确定 $U_i$ 在 $\mathcal{H}_{\text{gen}}$ 上的显式形式 | 中 |
| 2 | 解超算子 $\Phi$ 的不动点方程求 $Y_f$ | 中 |
| 3 | 验证第一阶条件 $[D_F, a] = 0$ 对 $Y_f$ 的约束 | 难 |
| 4 | 验证预测的 $y_i$ 与实验的 $m_i/c_i^\alpha$ 一致 | 易 |

**关键瓶颈**：步骤 1 需要将 $\mathbb{Z}_3$ 生成元 $U_i$ 具体化来自 $M_3(\mathbb{C})$ 代数的幺正表示。

---

## 6. 参考文献

1. Connes (1996), *Gravity coupled with matter...*, Commun. Math. Phys. 182, 155-176
2. Connes & Marcolli (2008), *Noncommutative Geometry, Quantum Fields and Motives*, §1.8-1.15
3. Chamseddine, Connes & Marcolli (2007), "Gravity and the standard model with neutrino mixing", *Adv. Theor. Math. Phys.* 11, 991-1089
4. Phase 50A: [`spectral_finite_IFS_triple.md`](spectral_finite_IFS_triple.md)
5. Phase 50D: [`paperX_alpha_first_principles.py`](../../paperX_alpha_first_principles.py)
