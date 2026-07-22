# CKM 的 $J$ 生成元旋转机制

## 1. 机制

IFS 谱三元组的实结构 $J$ 在代空间 $\mathbb{C}^3$ 上不同扇区有不同的投影 $J_{\text{gen}}^{(f)}$。这导致 Yukawa 矩阵 $Y_u$ 和 $Y_d$ 在不同基中对角化，产生 CKM 混合：

$$
V_{\text{CKM}} = U_u^* U_d
$$

其中 $U_f$ 对角化 $Y_f = J_{\text{gen}}^{(f)} \cdot \operatorname{diag}(c_1^{\alpha_f}, c_2^{\alpha_f}, 1) \cdot (J_{\text{gen}}^{(f)})^{-1}$。

### 1.1 数值估计

若 $J_{\text{gen}}^{(u)} = I$（约定），且 $J_{\text{gen}}^{(d)}$ 是 1-2 平面上的小旋转 $R(\theta)$，则：

$$|V_{us}| = |\sin\theta| = 0.224 \quad \Rightarrow \quad \theta \approx 0.226\ \text{rad} \ (13^\circ)$$

即 $J$ 在代空间上的 $u$-$d$ 投影差约 $13^\circ$。

### 1.2 预测方案

$$
J_{\text{gen}}^{(f)} = \exp\left(i \sum_{a} \phi_a^{(f)} T_a\right)
$$

其中 $T_a$ 是 $\mathfrak{su}(3)$（$\mathbb{C}^3$ 上的生成元），$\phi_a^{(f)}$ 是与扇区超荷 $Y_f$ 相关的相位。则：

$$V_{\text{CKM}} = \exp\left(-i\sum_a \phi_a^{(u)} T_a\right) \cdot \exp\left(i\sum_a \phi_a^{(d)} T_a\right)$$

## 2. 验证

最简单模型：$J$ 的旋转仅在 1-2 子空间非零，$u$-$d$ 差 $\theta = 0.226$：

$$V = \begin{pmatrix} \cos\theta & \sin\theta & 0 \\ -\sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

得到 $|V_{us}| = 0.224$（匹配），但 $|V_{cb}| = 0$（不匹配）。需要 2-3 混合的第二个角。

含两个旋转角（1-2 和 2-3）：

$$\theta_{12} \approx 0.226,\ \theta_{23} \approx 0.041$$

则 $|V_{us}| = 0.224$, $|V_{cb}| = 0.041$（均匹配实验）。

## 3. 开放问题

$\theta_{12}$ 和 $\theta_{23}$ 的值能否从 $J$ 的结构第一性推导？需要计算 $J$ 在 $\mathbb{C}^3$ 上对不同扇区超荷的依赖。

## 4. 参考文献

1. Chamseddine, Connes & Marcolli (2007), "Gravity and the standard model with neutrino mixing", *Adv. Theor. Math. Phys.* 11, 991-1089
2. `spectral_first_order_CKM.md` — 第一阶条件路径
3. PDG (2024), CKM 矩阵实验值
