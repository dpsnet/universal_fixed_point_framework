# 非 Markov 系统 TE-G-M 不等式严格推广证明研究笔记

**日期**：2026-07-20
**关联**：Paper I §8.3.3 第 17 项；Paper I 定理 TE-G-M；Paper II §1.5.3
**状态**：Markov IFS 已证明，一般非 Markov 动力系统推广待严格证明

---

## 1. 问题陈述

**定理 TE-G-M**（Markov IFS 版本）：对归一化的 Markov IFS，拓扑熵 $h_{\text{top}}$ 与谱间隙 $\gamma$ 满足

$$h_{\text{top}} \cdot \gamma \leq C, \quad C \leq 1$$

当前证明依赖 Markov 划分的强结构：
- 转移矩阵 $A_{ij}$ 的 0-1 结构
- Perron-Frobenius 定理直接适用
- 压缩比 $c_i < 1$ 提供自然归一化

对于**非 Markov 系统**（如一般 Axiom A 吸引子、非一致双曲系统、耗散混沌），需要更一般的证明框架。

## 2. 非 Markov 系统的障碍

| Markov 情形 | 非 Markov 情形 | 影响 |
|:-----------|:--------------|:----|
| 符号编码精确 | 仅存在近似符号编码 | 转移矩阵不再精确 |
| 转移矩阵 0-1 | 转移"概率"需近似 | Perron-Frobenius 算子是无限维 |
| 压缩比 $c_i < 1$ 全局 | 局部 Lyapunov 指数变化 | 需要 Oseledets 分解 |
| 拓扑熵 = log λ_PF | 拓扑熵需用覆盖数定义 | 需要维数/熵估计 |
| 谱间隙由 Markov 矩阵给出 | 谱间隙来自拟紧算子 | 需要 Ruelle-Perron-Frobenius 理论 |

## 3. 推广策略

### 3.1 几何化证明路线

利用 Axiom A 吸引子的 Markov 近似：

1. **构造 Markov 划分序列**：对任意 $\varepsilon > 0$，存在有限 Markov 划分 $\mathcal{P}_\varepsilon$，其符号动力与原系统之间的时间重分误差 $< \varepsilon$
2. **近似系统的 TE-G-M**：对每个 $\varepsilon$ 近似系统，TE-G-M 成立
3. **取极限 $\varepsilon \to 0$**：证明 $h_{\text{top}} \cdot \gamma$ 在极限下保持上界

关键引理：拓扑熵和谱间隙在 Markov 近似下的**上半连续性**。

### 3.2 泛函分析证明路线

将 Ruelle-Perron-Frobenius 算子 $\mathcal{L}$ 视为拟紧算子：

- 谱间隙 $\gamma = 1 - |\lambda_2|/\lambda_1$，其中 $\lambda_1$ 为主导特征值
- Ruelle 不等式：$h_\mu \leq \sum_{\lambda_i > 0} \lambda_i \cdot d_i$
- 结合 Ledrappier-Young 维数分解（定理 HD-D）

目标不等式可重写为：

$$h_{\text{top}} \cdot \left(1 - \frac{|\lambda_2|}{\lambda_1}\right) \leq C$$

其中右侧常数 $C$ 可能依赖于系统的双曲性和维数。

### 3.3 谱框架证明路线

在 $\mathbf{Rec}/\mathbf{Spec}$ 框架内：

- 拓扑熵 $h_{\text{top}}$ 对应 $D(R)$ 的谱测度增长率
- 谱间隙 $\gamma$ 对应 $\mathbf{Spec}$ 对象的主导/次主导特征值分离
- 不等式 $h_{\text{top}} \cdot \gamma \leq C$ 可解释为"谱复杂度 × 谱分辨率有界"

这给出了 TE-G-M 的**范畴论诠释**：$\mathbf{Spec}$ 对象不能同时具有高复杂度和高分辨率。

## 4. 预期结果

**猜想 TE-G-M'**：对具有 SRB 测度的 C² Axiom A 吸引子，存在仅依赖于相空间维数 $d$ 和双曲性参数的常数 $C(d) \leq 1$，使得

$$h_{\text{top}} \cdot \gamma \leq C(d)$$

其中 $\gamma$ 是 Ruelle-Perron-Frobenius 算子在适当函数空间中的谱间隙。

## 5. 与论文关联

证明此猜想后，Paper I 定理 TE-G-M 可从 Markov IFS 推广到一般非 Markov 动力系统，Paper I §8.3.3 第 17 项"仍待深化"可升级为"完全解决"或部分解决。
