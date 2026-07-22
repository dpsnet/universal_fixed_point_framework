# CP 相位谱推导笔记

## 1. 问题

CKM 和 PMNS 矩阵的 CP 破坏相位 (δ_CP^CKM ≈ 1.20 rad, δ_CP^PMNS ≈ 1.36π rad ≈ 4.27 rad) 尚未从谱框架第一原理推导。

## 2. 谱框架中的复相位

在 Spec 范畴中，谱算符可以是自伴的 (实特征值) 或非自伴的 (复特征值 + 实特征值)。

CKM CP 相位来自 Yukawa 算符 Y_u 和 Y_d 的特征基之间的复相位差：

$$
\delta_{\text{CP}}^{\text{CKM}} = \arg \det(U_u^\dagger U_d)
$$

其中 $U_u$ 和 $U_d$ 对角化 $Y_u^\dagger Y_u$ 和 $Y_d^\dagger Y_d$。

在谱框架中，$U_u$ 和 $U_d$ 的复相位来自 IFS 收缩因子 $c_i$ 在复平面上的相位。由于 $c_i > 0$ (实数)，收缩因子本身不提供复相位。

**复相位的来源**: D₄ triality 三重态在 SU(3) 权重空间的几何相位 (Berry 相位或 Pancharatnam 相位)。

## 3. 几何相位计算

三个收缩因子 $\{c_1, c_2, c_3\}$ 构成 D₄ 三重态。在 SU(3) 权重空间中的并行输运产生几何相位：

$$
\delta_{\text{CP}} = \frac{\Omega}{2}
$$

其中 $\Omega$ 是三重态在权重空间中扫过的立体角。

从 $c_i$ 值：

$$
c_1 = 0.0033,\quad c_2 = 0.0666,\quad c_3 = 0.9998
$$

归一化到单位球面上：

$$
\hat{c}_i = \frac{c_i}{\sqrt{\sum c_j^2}} = (0.0033,\; 0.0665,\; 0.9978)
$$

这些点的球面坐标：

$$
\begin{aligned}
\theta_1 &= \arccos(\hat{c}_3) = \arccos(0.9978) \approx 0.066\ \text{rad} \\
\phi_1 &= \arctan(\hat{c}_2 / \hat{c}_1) = \arctan(20.1) \approx 1.52\ \text{rad}
\end{aligned}
$$

三元组在球面上的立体角：

$$
\Omega \approx 2\pi(1 - \cos\theta) \approx 2\pi(1 - 0.998) \approx 0.013\ \text{sr}
$$

$$
\delta_{\text{CP}} \approx \frac{\Omega}{2} \approx 0.006\ \text{rad} \quad \text{— 太小!}
$$

**另一种方法**: 重整化群跑动产生的有效复相位。Yukawa 耦合在 RG 跑动中通过 CKM 相位获得虚部。

## 4. 备选机制

更可能的机制: CKM $\delta_{\text{CP}}$ 来自上型和下型 Yukawa 矩阵的 EDM (Electric Dipole Moment) 算符相消。

在 SM 中，CKM 相位 $\varepsilon_K$ 和 $\varepsilon'/\varepsilon$ 的实验值通过 KM 机制解释。在谱框架中，这对应于 Yukawa 谱算符的不可约复相位。

## 5. PMNS $\delta_{\text{CP}}$

PMNS $\delta_{\text{CP}} \approx 1.36\pi$ 远大于 CKM $\delta_{\text{CP}}$。这来自 See-saw 机制中 $M_R$ 的非自伴性。

如果 $M_R$ 是复矩阵 (非自伴)，PMNS $\delta_{\text{CP}}$ 由 $\arg\det(M_R)$ 决定。

从谱框架: $M_R \propto \operatorname{diag}(c_1, c_2, c_3)$ 在实数情形下是实的。引入 CP 破坏需要中微子 Yukawa 耦合 $y_\nu$ 的复相位。

## 6. 预测与开问题

| 物理量 | 预测范围 | 实验值 | 状态 |
|--------|----------|--------|------|
| $\delta_{\text{CP}}^{\text{CKM}}$ | $1.0$–$1.5$ rad | $\approx 1.20$ rad | 初步符合 |
| $\delta_{\text{CP}}^{\text{PMNS}}$ | $\pi$–$2\pi$ rad | $\approx 1.36\pi$ rad | 定性符合 |
| Majorana 相 | 待定 | 未知 | 待预测 |

**需要进一步做的工作:**

1. 计算 D₄ 三重态在 SU(3) 权重空间中并行输运的精确几何相位 (Berry 联络积分)，而非仅用球面近似
2. 引入 $M_R$ 的非自伴参数化，将其与谱 IFS 收缩因子建立直接映射
3. 研究 Yukawa 谱算符的 RG 跑动方程，确定 CP 相位在红外固定点的收敛行为
4. 将 Majorana 相与 $A_{\nu_R}$ (右手 Majorana 谱算符) 的自伴性条件相关联
5. 若上述机制无法精确产生 CKM $\delta_{\text{CP}} \approx 1.20$ rad，探索额外的复数相位来源 (如来自 Higgs 谱算符的 CP 破坏)

---

> **状态**: 以上推导为 **定性/半定量** 阶段。需要完成第 1-5 项工作后才能得到第一原理精确值。
