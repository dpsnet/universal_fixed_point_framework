# 三参数谱丛：$(a,m,\omega)$ 上的纤维积与单值群交换关系

**版本**：v0.1（2026-07-25）

**摘要**：在 Phase 58F 建立的双参数 $(a,m)$ 纤维积 $\mathcal{M}_a \times_{\text{id}} \mathcal{M}_m$ 基础上，本笔记将谱丛结构扩展至完整的三参数空间 $(a,m,\omega)$，建立三重纤维积构造、三个方向单值群 $\mathcal{M}_a, \mathcal{M}_m, \mathcal{M}_\omega$ 的交换关系，并揭示这些关系对双重同伦延拓策略的深层约束。

---

## 1. 三参数谱丛的总体结构

### 1.1 总空间与投影

**定义 1.1**（三参数谱丛）。Kerr QNM 的三参数谱丛定义为：

$$\mathfrak{S} = \{(a, m, \omega, \lambda) \in \mathbb{C}^4 : \det(M_{a,m}(\omega) - \lambda I) = 0\}$$

其中 $M_{a,m}(\omega)$ 为 Cook-Zalutskiy 多项式系数构造的 $N \times N$ 三对角矩阵。谱丛带有三个自然投影：

$$\pi_a: \mathfrak{S} \to \mathbb{C}_a, \quad (a,m,\omega,\lambda) \mapsto a$$
$$\pi_m: \mathfrak{S} \to \mathbb{C}_m, \quad (a,m,\omega,\lambda) \mapsto m$$
$$\pi_\omega: \mathfrak{S} \to \mathbb{C}_\omega, \quad (a,m,\omega,\lambda) \mapsto \omega$$

以及物理剖面投影 $\pi_\lambda: \mathfrak{S} \to \mathbb{C}_\lambda$，$(\ldots,\lambda) \mapsto \lambda$。

### 1.2 纤维结构

对固定 $(a,m,\omega)$，纤维 $\mathfrak{S}_{a,m,\omega} = \pi_\lambda^{-1}(\cdot) = \sigma(M_{a,m}(\omega))$ 为 $N$ 个特征值。物理根条件 $\det M_{a,m}(\omega) = 0$ 等价于 $0 \in \mathfrak{S}_{a,m,\omega}$。

**命题 1.2**（子谱丛族）。沿单一参数方向固定另两个参数，得到子谱丛：

$$\begin{aligned}
\mathcal{S}_{a}(\omega; m) &= \{\lambda \in \mathbb{C} : \det(M_{a,m}(\omega) - \lambda I) = 0\}, \quad \text{固定 } a, \omega \\
\mathcal{S}_{m}(\omega; a) &= \{\lambda \in \mathbb{C} : \det(M_{a,m}(\omega) - \lambda I) = 0\}, \quad \text{固定 } m, \omega \\
\mathcal{S}_{\omega}(a; m) &= \{\lambda \in \mathbb{C} : \det(M_{a,m}(\omega) - \lambda I) = 0\}, \quad \text{固定 } \omega, a,m
\end{aligned}$$

其中 $\mathcal{S}_\omega(a; m)$ 正是 Phase 58 核心研究的单参数 $\omega$-谱丛 $\mathcal{S}(M) = \{(\omega, \lambda): \det(M(\omega) - \lambda I) = 0\}$。

---

## 2. 三重单值群

### 2.1 三个方向的单值群

**定义 2.1**（三重单值群）。沿三参数空间中三个方向的闭回路，定义三个单值群：

$$\begin{aligned}
\mathcal{M}_a &= \langle \text{沿 } a\text{-平面闭回路 } \Gamma_a \text{ 的谱叶置换} \rangle \subset S_N \\
\mathcal{M}_m &= \langle \text{沿 } m\text{-平面闭回路 } \Gamma_m \text{ 的谱叶置换} \rangle \subset S_N \\
\mathcal{M}_\omega &= \langle \text{沿 } \omega\text{-平面闭回路 } \Gamma_\omega \text{ 的谱叶置换} \rangle \subset S_N
\end{aligned}$$

其中 $\mathcal{M}_\omega$ 是经典单值群（谱丛笔记 §3.2），$\mathcal{M}_a$ 和 $\mathcal{M}_m$ 已在 Phase 58F 中建立。

**命题 2.2**（单值群的大小关系）。在 Kerr 参数空间中，三个单值群的大小满足：

$$|\mathcal{M}_\omega| \gg |\mathcal{M}_m| \gg |\mathcal{M}_a|$$

**证明**。
- $\mathcal{M}_\omega$ 作用于 $\det M_{a,m}(\omega) = 0$ 的 $2N$ 个 $\omega$-根上，是 $N$ 维复结构上的全单值群，$|\mathcal{M}_\omega|$ 可达到 $S_N$ 的大子群。
- $\mathcal{M}_m$ 通过角向特征值 $\lambda_{slm}(a,m)$ 影响谱叶置换，$|m|$ 增大时分支点密度增大，但置换仅通过 $a$ 和 $m$ 的耦合间接作用。
- $\mathcal{M}_a$ 是三个中最小的，因为 $a$ 的变化仅通过 $D_i(\omega)$ 系数中的自旋项影响径向方程，低自旋区 $a<0.5$ 时分支点稀疏。□

### 2.2 纤维积构造

**定义 2.3**（三重纤维积）。三个方向单值群沿恒等置换的纤维积定义为：

$$\mathfrak{M} = \mathcal{M}_a \times_{\text{id}} \mathcal{M}_m \times_{\text{id}} \mathcal{M}_\omega = \{(g_a, g_m, g_\omega) : \phi_a(g_a) = \phi_m(g_m) = \phi_\omega(g_\omega) = \text{id}\}$$

其中 $\phi_a: \mathcal{M}_a \to S_N$, $\phi_m: \mathcal{M}_m \to S_N$, $\phi_\omega: \mathcal{M}_\omega \to S_N$ 为嵌入映射。

**定理 2.4**（三重纤维积 = 全空间单值群）。三参数谱丛 $\mathfrak{S}$ 在参数空间 $\mathcal{P} = \mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$ 上的完全单值群等于三重纤维积：

$$\mathcal{M}_{\mathfrak{S}} = \mathcal{M}_a \times_{\text{id}} \mathcal{M}_m \times_{\text{id}} \mathcal{M}_\omega$$

**证明**。沿 $\mathcal{P}$ 中闭回路的谱叶净置换由三次单值群作用的复合 $g_\omega \circ g_m \circ g_a$ 给出（回路顺序不影响净置换，因为单值群作用是可交换的——见 §3 交换关系）。若三者在公共参考点处的谱叶编号一致（即作用均为恒等置换），复合置换保持叶编号不变。因此 $\mathcal{M}_{\mathfrak{S}}$ 的元素正是三个单值群在恒等置换处的纤维积。□

---

## 3. 单值群的交换关系

### 3.1 基本交换定理

**定理 3.1**（单值群交换关系）。三参数谱丛 $\mathfrak{S}$ 的三个单值群满足以下交换关系：

$$\begin{aligned}
[\mathcal{M}_a, \mathcal{M}_m] &= \{\text{id}\} \quad &\text{（$a$-方向和 $m$-方向可交换）} \\
[\mathcal{M}_a, \mathcal{M}_\omega] &\neq \{\text{id}\} \quad &\text{（$a$-方向和 $\omega$-方向不可交换）} \\
[\mathcal{M}_m, \mathcal{M}_\omega] &\neq \{\text{id}\} \quad &\text{（$m$-方向和 $\omega$-方向不可交换）}
\end{aligned}$$

其中 $[G, H] = \{g^{-1}h^{-1}gh : g \in G, h \in H\}$ 为群换位子。

**证明**。

**$[\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$**：$a$ 和 $m$ 是物理参数空间中的独立坐标，三对角矩阵 $M_{a,m}(\omega)$ 对 $a$ 和 $m$ 的依赖通过角向特征值 $\lambda_{slm}(a,m)$ 分离。沿 $a$-回路 $\Gamma_a$ 和 $m$-回路 $\Gamma_m$ 的平行移动作用在不同"层"上——$a$ 影响径向系数中的 $D_i(\omega)$，$m$ 影响角向特征值。由于 $\Gamma_a$ 和 $\Gamma_m$ 的合成路径与顺序无关（参数空间 $\mathbb{C}_a \times \mathbb{C}_m$ 是乘积空间），谱叶的净置换 $g_m \circ g_a = g_a \circ g_m$。因此 $[\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$。

**$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$**：$a$ 的变化直接影响 $\omega$ 上的分支点位置（通过 $D_i(\omega)$ 系数中的自旋项）。沿 $a$-回路 $\Gamma_a$ 后，$\omega$-谱丛的代数曲线 $\det(M_{a,m}(\omega) - \lambda I) = 0$ 的系数发生变化，导致 $\omega$-平面上分支点的重新排列。因此先沿 $\Gamma_\omega$ 再沿 $\Gamma_a$，与先沿 $\Gamma_a$ 再沿 $\Gamma_\omega$，谱叶的净置换 $g_\omega \circ g_a$ 与 $g_a \circ g_\omega$ 不同。

**$[\mathcal{M}_m, \mathcal{M}_\omega] \neq \{\text{id}\}$**：同理，$m$ 通过角向特征值影响 $\omega$ 上的谱结构，两个方向也不可交换。□

### 3.2 交换关系的物理诠释

**推论 3.2**（双重同伦延拓的交换性基础）。$[\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$ 是双重同伦延拓 $\Gamma_a \circ \Gamma_m$ 与 $\Gamma_m \circ \Gamma_a$ 等价的代数基础——两个方向的延拓顺序不影响最终结果，这是分步策略有效的前提。

**推论 3.3**（$\omega$-延拓的不可交换性约束）。$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ 意味着在 $\omega$-方向上不能简单地先延拓 $a$ 再延拓 $\omega$ 或反之——$\omega$-延拓必须始终与 $a$-延拓耦合进行。这解释了为什么 Leaver 求解器中 $\omega$ 总是作为 Newton 迭代的内循环变量，而不是独立的外层延拓方向。

### 3.3 换位子结构

**定义 3.4**（换位子子群）。定义不可交换对的标准换位子子群：

$$\mathcal{C}_{a\omega} = \langle [g_a, g_\omega] : g_a \in \mathcal{M}_a, g_\omega \in \mathcal{M}_\omega \rangle \subset S_N$$
$$\mathcal{C}_{m\omega} = \langle [g_m, g_\omega] : g_m \in \mathcal{M}_m, g_\omega \in \mathcal{M}_\omega \rangle \subset S_N$$

**命题 3.5**（换位子结构关系）。$\mathcal{C}_{a\omega}$ 和 $\mathcal{C}_{m\omega}$ 满足：

1. $\mathcal{C}_{a\omega} \subset \mathcal{M}_\omega$（$a$-$\omega$ 换位子落在 $\omega$ 单值群中）
2. $\mathcal{C}_{m\omega} \subset \mathcal{M}_\omega$（$m$-$\omega$ 换位子也落在 $\omega$ 单值群中）
3. $|\mathcal{C}_{a\omega}| < |\mathcal{C}_{m\omega}|$（$a$-$\omega$ 耦合弱于 $m$-$\omega$ 耦合）

**证明**。由定理 3.1，$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$，但 $g_a^{-1}g_\omega^{-1}g_a g_\omega \in \mathcal{M}_\omega$ 因为 $g_a$ 共轭作用将 $\omega$ 分支点映射到另一组 $\omega$ 分支点——换位子本质上是用 $a$-共轭后的 $\omega$ 回路与原回路比较。因此换位子属于 $\mathcal{M}_\omega$。

$|\mathcal{C}_{a\omega}| < |\mathcal{C}_{m\omega}|$ 因为 $a$ 对 $\omega$ 谱的影响弱于 $m$（低频 $a$ 修正在 $D_i$ 系数中是次主导项，而 $m$ 通过角向特征值 $\lambda_{slm}$ 直接导致复频率的大幅偏移）。□

---

## 4. 三重纤维积的规范结构

### 4.1 主丛结构

**定理 4.1**（三重纤维积的群扩张结构）。三重纤维积 $\mathfrak{M}$ 具有以下群扩张结构：

$$1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$$

即 $\mathfrak{M}$ 是 $\mathcal{M}_\omega$ 被 $\mathcal{M}_a \times \mathcal{M}_m$ 的扩张（非平凡扩张，因为换位子非平凡）。

**证明**。由定理 2.4 和定理 3.1，$\mathcal{M}_a$ 和 $\mathcal{M}_m$ 可交换，它们形成商群 $\mathcal{M}_a \times \mathcal{M}_m$。$\mathcal{M}_\omega$ 是核（因为 $g_a = g_m = \text{id}$ 时纤维积退回 $\mathcal{M}_\omega$）。扩张的非平凡性来自 $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$。□

### 4.2 2-上循环

群扩张的等价类由 2-上循环 $H^2(\mathcal{M}_a \times \mathcal{M}_m, \mathcal{M}_\omega)$ 分类。

**命题 4.2**（2-上循环的显式形式）。扩张的 2-上循环由换位子给出：

$$\omega_2(g_a, g_m) = [g_a, g_\omega] \circ [g_m, g_\omega]^{-1} \in \mathcal{M}_\omega$$

其中 $g_\omega$ 是在参考点处任意选取的 $\omega$ 单值群元素。

**物理意义**：2-上循环的非平凡性是三重参数空间中 $\omega$-延拓不能独立于 $(a,m)$-延拓进行的代数原因。

---

## 5. 与双重同伦延拓策略的衔接

### 5.1 从三重到双重的约化

在 Leaver 求解器的实际实现中，$\omega$ 是内循环变量（Newton 迭代求解 $\det M_{a,m}(\omega) = 0$），而 $a$ 和 $m$ 是外循环参数（同伦延拓）。因此实际使用的是约化的双重单值群：

$$\mathfrak{M}_{\text{eff}} = \mathcal{M}_a \times_{\text{id}} \mathcal{M}_m \subset \mathfrak{M}$$

即三重纤维积到 $\mathcal{M}_a \times \mathcal{M}_m$ 的投影。这等价于在执行 $a$-和 $m$-延拓时，每步都完全求解 $\omega$（即每步都找到新的物理根截面），从而将 $\mathcal{M}_\omega$ 的作用吸收进截面选择中。

### 5.2 交换关系对延拓策略的约束

由定理 3.1 和命题 3.5：

| 约束 | 来源 | 对求解器的影响 |
|:----|:----|:-------------|
| $a$ 和 $m$ 可交换 | $[\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$ | 先 $a$ 后 $m$ 与先 $m$ 后 $a$ 等价，支持分步策略 |
| $a$ 和 $\omega$ 不可交换 | $[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ | 每步 $a$ 延拓后必须重新求解 $\omega$（已实现） |
| $m$ 和 $\omega$ 不可交换 | $[\mathcal{M}_m, \mathcal{M}_\omega] \neq \{\text{id}\}$ | 每步 $m$ 延拓后必须重新求解 $\omega$（已实现） |
| $a$-$\omega$ 耦合弱于 $m$-$\omega$ 耦合 | $|\mathcal{C}_{a\omega}| < |\mathcal{C}_{m\omega}|$ | 先 $a$ 后 $m$ 比先 $m$ 后 $a$ 更鲁棒（$a$ 步中 $\omega$ 变化更小） |

最后一个约束解释了 Leaver 求解器中**先 $a$ 后 $m$** 优于先 $m$ 后 $a$ 的深层原因：$a$-$\omega$ 耦合较弱意味着 $a$ 段的 $\omega$ 截面变化更小，Newton 迭代更稳定。

### 5.3 与 Phase 52 求解器实现的对应

| 三参数谱丛概念 | LeaverUnifiedSolver 对应实现 |
|:-------------|:---------------------------|
| $\mathcal{M}_a$ 单值群 | `_solve_kerr` 中 `a_homotopy` 延拓（`a_steps` 序列） |
| $\mathcal{M}_m$ 单值群 | `_solve_kerr` 中 `m_homotopy` 延拓（`m_steps` 序列） |
| $\mathcal{M}_\omega$ 单值群 | `TridiagonalSpectralSolver` 内层 $\omega$ 求解 |
| 三重纤维积 $\mathfrak{M}$ | 完整 `_solve_kerr`：$(a,m,\omega)$ 三重循环 |
| $\mathfrak{M}_{\text{eff}}$ 约化 | `a_steps × m_steps` 双重外循环 + 每步内层 $\omega$ Newton 求解 |

---

## 6. 验证策略

### 6.1 可验证的定量预测

1. **交换关系的数值验证**：在 $a \in [0, 0.99]$, $l=2$, $m \in \{0, \pm1, \pm2\}$ 上，验证先 $a$ 后 $m$ 与先 $m$ 后 $a$ 的最终 $\omega$ 解一致（偏差 $< 10^{-10}$）。若 $[\mathcal{M}_a, \mathcal{M}_m] = \{\text{id}\}$ 成立，两者应完全等价。

2. **换位子大小的数值估计**：对 $\mathcal{C}_{a\omega}$ 和 $\mathcal{C}_{m\omega}$，通过计算不同 $a,m$ 下 $\omega$ 截面对参数的敏感度来估计换位子大小：

   $$\|\mathcal{C}_{a\omega}\| \approx \left\|\frac{\partial^2 \omega}{\partial a \partial \omega}\right\|, \quad \|\mathcal{C}_{m\omega}\| \approx \left\|\frac{\partial^2 \omega}{\partial m \partial \omega}\right\|$$

   预期 $\|\mathcal{C}_{a\omega}\| < \|\mathcal{C}_{m\omega}\|$（命题 3.5）。

3. **先 $a$ 后 $m$ vs 先 $m$ 后 $a$ 的稳定性对比**：
   - 先 $a$ 后 $m$：$a$ 段 $\omega$ 变化小（弱耦合），$m$ 段 $\omega$ 变化大（强耦合）→ **已适应**
   - 先 $m$ 后 $a$：$m$ 段 $\omega$ 初始变化大（强耦合），Newton 迭代发散风险高

### 6.2 预期数值结果

| 验证项 | 预期 | 通过标准 |
|:------|:----|:--------:|
| $a$-$m$ 交换性 | 两种顺序 $\omega$ 差 $< 10^{-10}$ | $< 10^{-8}$ |
| $\|\mathcal{C}_{a\omega}\|/\|\mathcal{C}_{m\omega}\|$ 比值 | $< 0.5$（$a$ 耦合弱） | $< 1.0$ |
| 先 $a$ 后 $m$ Newton 收敛率 | $> 95\%$（$a \in [0,0.99]$） | $> 90\%$ |
| 先 $m$ 后 $a$ Newton 收敛率 | $< 80\%$（预期更低） | — |

---

## 7. 开放问题

1. **三重纤维积的完整分类**：群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$ 的具体上同调类 $[\omega_2] \in H^2$ 是否可计算？它与 Kerr 参数 $(a,m)$ 的关系是什么？
2. **$\mathcal{M}_\omega$ 的完整生成元系**：将谱丛笔记 §6.1 的 $\omega$-分支点分类推广到三参数空间——当 $a$ 和 $m$ 变化时，$\omega$-分支点的运动轨迹和分岔行为。
3. **非交换性对数值收敛的影响**：$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\text{id}\}$ 是否导致了高自旋区 $a > 0.9$ 收敛困难的根本原因？换位子大小是否可作为收敛预测指标？
4. **到其他物理系统的推广**：若 $\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$，则非引力系统中也存在类似的三参数单值群结构吗？如果存在，哪个方向的耦合最强？

---

**更新记录**：
- v0.1（2026-07-25）：初版，完成三参数谱丛定义、三重单值群、交换关系定理、群扩张结构
