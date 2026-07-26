# 谱手性规范理论与量子反常

## 核心目标

将手性费米子、ABJ 反常和反常消去条件翻译为谱语言，完善谱规范理论对标准模型手性结构的描述。

---

## 1. 谱手性费米子

### 1.1 Clifford 投影与手性谱旋量

对 Dirac 代数 $\mathrm{Cl}(1,3)$，手性投影算子为：
$$P_L = \frac{1 - \gamma^5}{2}, \quad P_R = \frac{1 + \gamma^5}{2}.$$

在 $\mathbf{Sp}$ 范畴中，手性投影对应于谱旋量对象的 $\mathbb{Z}_2$ 分级：

**定义 1**（谱手性旋量）。谱 Dirac 算子 $A_\psi = i\gamma^\mu\partial_\mu$ 与 $\gamma^5$ 反对易：
$$\{A_\psi, \gamma^5\} = 0.$$

谱旋量空间的 $\mathbb{Z}_2$ 分级：
$$\mathcal{H}_\psi = \mathcal{H}_L \oplus \mathcal{H}_R, \quad \mathcal{H}_{L/R} = P_{L/R} \mathcal{H}_\psi.$$

谱左手/右手 Weyl 旋量定义为：
$$\Psi_L = P_L \Psi, \quad \Psi_R = P_R \Psi.$$

### 1.2 谱 Weyl 拉格朗日量

无质量 Weyl 旋量的谱作用量：
$$\mathcal{L}_{\text{Weyl}}^{\text{spec}} = \operatorname{Tr}_{\mathcal{H}_L}\left( \bar{\Psi}_L [A_\psi, \Psi_L] \right) + (L \to R).$$

### 1.3 手性规范耦合

在谱规范理论中，左手场 $\Psi_L$ 和右手场 $\Psi_R$ 可携带不同的规范群表示：
$$\nabla_\mu \Psi_L = \partial_\mu \Psi_L + ig_L \mathcal{A}_\mu^L \Psi_L,$$
$$\nabla_\mu \Psi_R = \partial_\mu \Psi_R + ig_R \mathcal{A}_\mu^R \Psi_R.$$

对 $SU(2)_L \times U(1)_Y$：
- $\Psi_L$ 是 $SU(2)$ 二重态（$g_L = g_2$）
- $\Psi_R$ 是 $SU(2)$ 单态（$g_R = 0$）

---

## 2. 谱 ABJ 反常

### 2.1 三角图的谱翻译

标准 ABJ 反常来自 $VVA$ 三角图（两个矢量流、一个轴矢流）：

$$\partial^\mu j_\mu^5 = \frac{g^2}{16\pi^2} \epsilon^{\mu\nu\rho\sigma} F_{\mu\nu} F_{\rho\sigma}.$$

在谱语言中，反常对应于谱生成泛函在 $\gamma^5$ 手征变换下的非不变性：

**定理 1**（谱 ABJ 反常）。谱生成泛函 $Z_{\text{spec}}[J]$ 在手征变换 $\Psi \to e^{i\alpha\gamma^5}\Psi$ 下的变化为：
$$\delta_\alpha \ln Z_{\text{spec}} = \frac{g^2}{16\pi^2} \int d\lambda \, \alpha(\lambda) \cdot \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F} \wedge \mathcal{F}),$$
其中 $\mathcal{F}$ 是谱规范曲率。

### 2.2 谱反常的推导

在谱截断 $\Lambda$ 下，反常来自谱 Dirac 算子的手征 Jacobian：

$$\mathcal{J}[\alpha] = \exp\left(-2i \int_0^\infty dt \, \operatorname{Tr}_{\mathbf{Sp}}\left( \alpha \gamma^5 e^{-t A_\psi^2/\Lambda^2} \right)\right).$$

在 $t \to 0$ 时的 Heawood 展开给出：
$$\lim_{t\to 0} \operatorname{Tr}(\alpha \gamma^5 e^{-t A_\psi^2}) = \frac{1}{16\pi^2} \int d\lambda \, \alpha(\lambda) \cdot \operatorname{Tr}(\mathcal{F} \wedge \mathcal{F}) \cdot (1 + \mathcal{O}(t)).$$

谱截断 $\Lambda$ 在 $t \to 0$ 极限下消失，给出与截断无关的反常。

### 2.3 谱反常的函子不变性

**定理 2**（反常的函子不变性）。ABJ 反常在谱化函子 $D: \mathbf{Rec}_D \to \mathbf{Sp}$ 下保持：
$$D(\partial^\mu j_\mu^5) = \partial^\mu j_\mu^{5,\text{spec}}.$$

---

## 3. 谱反常消去

### 3.1 标准模型中的反常消去

SM 中所有反常必须消去以保证理论自洽：

| 反常类型 | 条件 | SM 状态 |
|:--------|:----|:-------:|
| $[SU(3)]^3$ | $\operatorname{Tr}(T^a\{T^b,T^c\})_{L-R} = 0$ | ✅ |
| $[SU(2)]^3$ | $\operatorname{Tr}(\sigma^a\{\sigma^b,\sigma^c\})_{L-R} = 0$ | ✅ |
| $[SU(2)]^2 U(1)$ | $\operatorname{Tr}(Y \sigma^a\sigma^b)_{L-R} = 0$ | ✅ |
| $U(1)^3$ | $\operatorname{Tr}(Y^3)_{L-R} = 0$ | ✅ |
| 引力-规范 | $\operatorname{Tr}(Y)_{L-R} = 0$ | ✅ |
| $U(1)$-引力$^2$ | $\operatorname{Tr}(Y)_{L-R} = 0$ | ✅ |

### 3.2 谱反常消去条件

在 $\mathbf{Sp}$ 范畴中，反常消去条件表示为谱迹的消失：

$$\boxed{\operatorname{Tr}_{\mathbf{Sp}}\left( \gamma^5 \{T^a, T^b\} \right)_{\text{全体费米子}} = 0},$$

其中 $T^a$ 是规范生成元在费米子表示上的作用。

对 SM 的每一代费米子：
$$\Psi_{\text{gen}} = \{Q_L, u_R, d_R, L_L, e_R\},$$

谱迹消去：
$$\sum_{\Psi \in \text{gen}} \operatorname{Tr}_{\mathcal{H}_\Psi}\left( \gamma^5 \, Y_\Psi^3 \right) = 0,$$
$$\sum_{\Psi \in \text{gen}} \operatorname{Tr}_{\mathcal{H}_\Psi}\left( \gamma^5 \, Y_\Psi \right) = 0.$$

### 3.3 谱 Witten 反常

$SU(2)$ 的 Witten 全局反常要求在 $SU(2)$ 二重态数为偶数：
$$\# \text{SU(2) 左手二重态} \in 2\mathbb{Z}.$$

在谱语言中，这对应于 $\pi_4(SU(2)) = \mathbb{Z}_2$ 的谱翻译——谱规范变换的第四同伦群不变量。

---

## 4. 谱瞬子与 $\theta$ 真空

### 4.1 谱瞬子

规范场的瞬子解在谱语言中对应于谱规范曲率的自对偶条件：
$$\mathcal{F} = \pm \star \mathcal{F}.$$

谱拓扑荷（Pontryagin 指数）为：
$$Q_{\text{top}} = \frac{g^2}{32\pi^2} \int d\lambda \, \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F} \wedge \mathcal{F}).$$

### 4.2 谱 $\theta$ 项

谱 $\theta$ 项为：
$$\mathcal{L}_\theta^{\text{spec}} = \theta \cdot \frac{g^2}{32\pi^2} \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F} \wedge \mathcal{F}),$$

其中 $\theta$ 是真空角参数。在 $\mathbf{Sp}$ 中，$\theta$ 是谱对象的拓扑不变量。

### 4.3 轴子与 $\theta$ 的动力学消解

通过 Peccei-Quinn 机制，$\theta$ 被动力学轴子场 $a$ 消解：
$$\mathcal{L}_{a}^{\text{spec}} = \frac12 \operatorname{Tr}_{\mathcal{H}_a}([A_a, a]^2) + \frac{a}{f_a} \cdot \frac{g^2}{32\pi^2} \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F} \wedge \mathcal{F}).$$

在谱语言中，轴子是 $\mathbf{Sp}$ 中的周期伪标量对象：
$$a(\lambda) \cong a(\lambda) + 2\pi f_a.$$

---

## 5. 与标准理论的对应

| 概念 | 标准 QFT | 谱版本 |
|:----|:---------|:-------|
| Weyl 费米子 | $\psi_L, \psi_R$ | $\Psi_L = P_L\Psi, \Psi_R = P_R\Psi$ |
| 手征反常 | $\partial^\mu j_\mu^5 = \frac{g^2}{16\pi^2}F\tilde{F}$ | $\delta_\alpha \ln Z_{\text{spec}} \propto \operatorname{Tr}(\mathcal{F}\wedge\mathcal{F})$ |
| 反常消去 | $\sum \operatorname{Tr}(T^a\{T^b,T^c\})_{L-R}=0$ | $\operatorname{Tr}_{\mathbf{Sp}}(\gamma^5\{T^a,T^b\})=0$ |
| $\theta$ 项 | $\theta \cdot F\tilde{F}$ | $\theta \cdot \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F}\wedge\mathcal{F})$ |
| 轴子 | $a/f_a \cdot F\tilde{F}$ | $a(\lambda)/f_a \cdot \operatorname{Tr}_{\mathfrak{g}}(\mathcal{F}\wedge\mathcal{F})$ |

---

## 6. 数值验证

### 6.1 手性投影

验证 $P_L, P_R$ 投影算子在谱旋量空间中的正交完备性：
$$P_L^2 = P_L, \quad P_R^2 = P_R, \quad P_L P_R = 0, \quad P_L + P_R = I.$$

### 6.2 反常因子计算

数值计算三角图对 $\operatorname{Tr}(\gamma^5 T^a T^b)$ 的贡献，验证反常消去条件。

### 6.3 谱瞬子拓扑荷

在离散谱截断下验证谱拓扑荷 $Q_{\text{top}}$ 的量子化：
$$Q_{\text{top}} \in \mathbb{Z}.$$

---

## 7. 开放问题

| 问题 | 难度 | 说明 |
|:----|:----:|------|
| 谱版本的 $SU(2)$ Witten 反常 | 🔴 | $\pi_4(SU(2))$ 的谱翻译与数值验证 |
| 谱轴子势的严格推导 | 🟡 | 瞬子效应在 $\mathbf{Sp}$ 中生成的轴子势 $V(a)$ |
| 谱反常匹配条件（'t Hooft） | 🔴 | 低能有效理论与高能理论的谱反常一致性 |
| 谱 $\theta$ 角的重整化 | 🟡 | $\theta$ 参数在谱截断下的跑动 |
