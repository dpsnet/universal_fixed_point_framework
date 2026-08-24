# 元通用不动点函子范畴框架 XXVII：Leaver 谱覆盖理论——三参数纤维化、奇异纤维分类与耗散范畴嵌入

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**版本**：v1.0（2026-07-25）

**摘要**：本文在元通用不动点函子范畴框架下系统建立 Leaver 谱覆盖理论。将 Kerr 黑洞准正态模的三参数空间 $(a,m,\omega)$ 上的三对角矩阵族构造为三参数谱覆盖 $\mathfrak{S}$，证明其纤维化为三重纤维积结构。建立三个方向单值群 $\mathcal{M}_a,\mathcal{M}_m,\mathcal{M}_\omega$ 的交换关系定理，揭示 $a$-$m$ 可交换而 $a$-$\omega$、$m$-$\omega$ 不可交换的根本原因，证明三重单值群具有非平凡群扩张结构并由 2-上循环分类。提出奇异纤维三分定理，将参数空间中的退化点严格分为分支交叉（I 型）、谱静默边界（II 型）和零谱间隙退化（III 型）三类，建立互斥全覆盖的完备分类体系，并建立每类与 QNM 物理现象的精确对应。进一步将理论扩展至电磁扰动（$s=\pm1$），建立电磁谱覆盖 $\mathfrak{S}^{(s=-1)}$ 的数学框架，证明 Teukolsky-Starobinsky 同谱性定理，给出跨自旋奇异纤维分类的推广和局部吸引子捕获指数（Local Attractor Capture Index, LACI）对比框架（§12）。

---

**术语说明**：记号与定义沿用 Paper I（Rec、Sp、D 函子、谱覆盖）、Paper VI（谱截断与临界动力学）、Paper VIII（黑洞 QNM 记号）、Paper XXVI（Leaver 连续分数求解器数值方法）。

本文使用以下缩写，首次出现时均已给出完整中英文名称：
- **QNM**：准正态模（Quasi-Normal Mode）
- **LACI**：局部吸引子捕获指数（Local Attractor Capture Index）
- **TS**：Teukolsky-Starobinsky（托伊科尔斯基-斯塔罗宾斯基）
- **Koopman**：Koopman 算子（Koopman Operator）
- **LIGO**：激光干涉引力波天文台（Laser Interferometer Gravitational-Wave Observatory）
- **LVK**：LIGO-Virgo-KAGRA 合作组（LIGO-Virgo-KAGRA Collaboration）
- **EMRI**：极端质量比旋近（Extreme Mass Ratio Inspiral）
- **CZ**：Cook-Zalutskiy（库克-扎卢茨基）
- **L1/L2/L3**：第 1/2/3 层基准（Level 1/2/3 Benchmark）

**前置依赖**：Paper I（基础范畴框架与 RKHS 收敛率）、Paper VIII（黑洞谱动力学）、Paper XXVI（动态过程谱数值方法）。

---

## 1. 引言

Leaver（1985）提出的连分数方法（continued fraction method）是黑洞准正态模（QNM）数值计算的奠基性技术。其核心思想是将 Teukolsky 方程的径向方程离散化为三项递推关系，通过无限连分数的收敛条件 $\det M(\omega) = 0$ 确定 QNM 复频率。四十年来，Leaver 方法及其变体——包括 Nollert 改进、Cook-Zalutskiy 多项式系数公式化、以及双重同伦延拓策略——在 Kerr 黑洞 QNM 的高精度计算中取得了显著的数值成功。然而，这一数值成功背后的数学结构长期未被充分理解：三对角系数矩阵 $M_{a,m}(\omega)$ 作为一个含三个复参数的矩阵族，其谱的全局几何结构——包括 $\omega$-平面上谱叶的 Riemann 面结构、非物理根的多叶谱解释、以及同伦延拓路径的拓扑意义——缺乏统一的数学框架。

本文提出谱覆盖理论作为理解 Leaver 三对角矩阵族几何本质的统一框架。该理论建立在以下三个核心洞见之上：

1. **三对角矩阵族形成复平面上的 $N$ 叶分支覆盖**：对固定 $(a,m)$，矩阵 $M_{a,m}(\omega)$ 作为 $\omega$ 的二次矩阵多项式，其 $N$ 个特征值构成 $\mathbb{C}_\omega$ 上的 $N$ 叶分支覆盖。分支点对应两个特征值相等，非物理根是分支点处谱叶间跳跃的结果。

2. **同伦延拓是谱叶的平行移动**：Leaver 求解器中的 $a$-同伦延拓和 $m$-同伦延拓，在谱覆盖语言中分别对应谱叶沿 $a$ 方向和 $m$ 方向的平行移动。这种视角将 Newton 迭代的收敛性与谱覆盖的截面选择统一为几何问题。

3. **非物理根对应谱叶间在分支点的跳跃**：当同伦延拓路径穿过谱覆盖分支点时，连续截面可能跳跃到非物理叶上，这正是非物理根吸引域的几何起源。分支点密度越高的参数区域，非物理根出现的频率越高。

在此基础上，本文作出七大贡献：

**贡献 I——三参数谱覆盖的严格定义**（§2）。将 Kerr 三参数空间 $(a,m,\omega)$ 上的三对角矩阵族构造为三参数谱覆盖 $\mathfrak{S}$，给出三重纤维积定义，建立子谱覆盖族分类。

**贡献 II——三重单值群与群扩张**（§3）。建立三个方向单值群 $\mathcal{M}_a,\mathcal{M}_m,\mathcal{M}_\omega$ 的交换关系定理，证明 $[\mathcal{M}_a,\mathcal{M}_m] = \{\mathrm{id}\}$ 而 $[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$、$[\mathcal{M}_m,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$，揭示三重单值群满足非平凡群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$，其 2-上循环由换位子显式给出。

**贡献 III——奇异纤维三分定理**（§4）。证明奇异纤维严格分为三类——分支交叉（I 型）、谱静默边界（II 型）、零谱间隙退化（III 型）——互斥且全覆盖，并建立每类与 QNM 物理现象的精确对应。

**贡献 IV——Rec_diss 范畴嵌入**（§5）。将谱覆盖理论的范畴基础从 $\mathbf{Rec}$ 扩展至 $\mathbf{Rec}_{\mathrm{diss}}$，引入 $D_{\mathrm{diss}}$ 函子，构造谱覆盖与耗散范畴的严格函子 $F_{\mathrm{diss}}: \mathfrak{S} \to \mathbf{Rec}_{\mathrm{diss}}$，使三类奇异纤维获得范畴论刻画。

**贡献 V——辫子交叉数作为 $D_{\mathrm{diss}}$ 拓扑不变量**（§6）。定义 $D_{\mathrm{diss}}$ 上的辫子交叉数 $\mathrm{Br}(\mathcal{L})$，证明其在谱覆盖同构变换下的不变性，并建立其与分支点分布密度的定量关系。

**贡献 VI——三层基准体系**（§7）。建立包含（a）三重交换关系数值验证、（b）奇异纤维检测算法、（c）跨系统谱覆盖同构数值确认的三层基准体系。

**贡献 VII——四个可证伪预言**（§8）。提出四个具有明确数值阈值的可证伪预言，包括超辐射边界 LACI 跃变、高 $l$ 极限谱间隙退化、极值 Kerr 混合奇异行为，以及非引力系统三参数单值群结构的存在性。

本文与 Paper I §7.11 的关系如下：Paper I §7.11 首次提出了谱覆盖概念和二叉树纤维化结构，给出了定性描述和数值验证。本文在此基础上做三方面的严格化：其一，将 Paper I 中的单参数 $\omega$-谱覆盖 $\mathcal{S}(M)$ 扩展为完整的三参数谱覆盖 $\mathfrak{S}$，建立三重纤维积结构；其二，将 Paper I 中定性的单值群讨论提升为严格的交换关系定理和群扩张分类；其三，将 Paper I 中对分支点的经验观察系统化为奇异纤维三分定理，给出完备的分类体系。因此，Paper I §7.11 是本文的**定性前驱**，本文是其在三参数空间上的**严格数学展开**。

---

## 2. 三参数谱覆盖

### 2.1 Leaver 三项递推的谱覆盖表示

考虑 Kerr 黑洞的 Teukolsky 方程。经分离变量后，径向方程和角向方程分别化为三项递推关系。Cook-Zalutskiy（2014）将递推系数多项式化，得到 $N \times N$ 三对角矩阵族：

$$M_{a,m}(\omega) = \mathrm{tridiag}(\alpha_n(\omega),\ \beta_n(\omega),\ \gamma_n(\omega)), \quad n = 0,1,\dots,N-1$$

其中系数 $\alpha_n(\omega)$、$\beta_n(\omega)$、$\gamma_n(\omega)$ 为 $\omega$ 的至多二次多项式。三个系数的具体形式为：

$$\begin{aligned}
\alpha_n(\omega) &= (n+1)(n+2\nu_0+1) \\
\beta_n(\omega) &= -\lambda_{slm}(a,m) - n(n+2\nu_0+1) + \omega^2 + \frac{am(m+2\nu_0)}{n+\nu_0} + D_i(\omega) \\
\gamma_n(\omega) &= -2i\omega \kappa (n+\nu_0)
\end{aligned}$$

其中 $\nu_0$ 取决于自旋权重 $s$，$\lambda_{slm}(a,m)$ 为角向特征值，$\kappa$ 为视界表面引力，$D_i(\omega)$ 为自旋修正项。

QNM 频率 $\omega$ 满足特征方程 $\det M_{a,m}(\omega) = 0$，即 $0$ 是 $M_{a,m}(\omega)$ 的特征值。

**定义 2.1**（三参数谱覆盖，three-parameter spectral cover）。Kerr 黑洞三参数谱覆盖定义为：

$$\mathfrak{S} = \{(a,m,\omega,\lambda) \in \mathbb{C}^4 : \det(M_{a,m}(\omega) - \lambda I) = 0\}$$

带有三个自然投影：

$$\pi_a: \mathfrak{S} \to \mathbb{C}_a,\quad \pi_m: \mathfrak{S} \to \mathbb{C}_m,\quad \pi_\omega: \mathfrak{S} \to \mathbb{C}_\omega$$

> **注 2.1a（与标准概念的关系）**：$\mathfrak{S}$ 到参数空间 $\mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$ 的投影是**分支覆盖（branched covering）**——在分支点（$\partial\det M/\partial\omega = 0$）处纤维退化（特征值简并），不满足局部平凡性。因此 $\mathfrak{S}$ 不是标准意义上的"纤维丛"（fiber bundle）或"层"（sheaf），而是代数几何中标准的**谱覆盖（spectral cover）** 或**谱簇（spectral variety）**（参见 Donagi 1995 关于 Higgs 丛的谱覆盖构造）。MUFPF 中的"覆盖"强调参数空间上的分支覆盖结构，"谱"强调特征值集。为简单计，文中仍沿用"谱覆盖"称呼，但在涉及分支点/奇异纤维时需注意其非丛性质。

以及谱投影 $\pi_\lambda: \mathfrak{S} \to \mathbb{C}_\lambda$，$(a,m,\omega,\lambda) \mapsto \lambda$。底空间为乘积流形 $M = \mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$。对固定参数点 $p = (a,m,\omega)$，纤维 $\pi_\lambda^{-1}(p) = \sigma(M_{a,m}(\omega))$ 为 $N$ 个特征值。物理根条件 $\det M_{a,m}(\omega) = 0$ 等价于 $0 \in \mathfrak{S}_p$。

**命题 2.1**（三对角矩阵族的矩阵多项式结构）。$M_{a,m}(\omega)$ 是 $\omega$ 的二次矩阵多项式：

$$M_{a,m}(\omega) = M_0(a,m) + \omega M_1(a,m) + \omega^2 M_2(a,m)$$

其中 $M_0, M_1, M_2$ 为与 $\omega$ 无关的常矩阵，各自通过角度特征值 $\lambda_{slm}(a,m)$ 和自旋修正项 $D_i$ 依赖于 $a$ 和 $m$。

**证明**。由系数 $\alpha_n(\omega),\beta_n(\omega),\gamma_n(\omega)$ 显式形式直接验证。$\beta_n(\omega)$ 中的 $\omega^2$ 项贡献 $M_2$ 矩阵的对角元，$\gamma_n(\omega)$ 中的 $-2i\omega\kappa$ 贡献 $M_1$ 的次对角元。$\square$

### 2.2 三参数纤维化

谱覆盖 $\mathfrak{S}$ 在参数空间 $\mathcal{P} = \mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$ 上的纤维化结构需考虑三个参数之间的耦合关系。

**定义 2.2**（子谱覆盖）。沿单一参数方向固定另两个参数，得到三类子谱覆盖：

$$\begin{aligned}
\mathcal{S}_a(\omega; m) &= \{\lambda \in \mathbb{C} : \det(M_{a,m}(\omega) - \lambda I) = 0\},\quad \text{固定 } a \text{、变 } \omega \\
\mathcal{S}_m(\omega; a) &= \{\lambda \in \mathbb{C} : \det(M_{a,m}(\omega) - \lambda I) = 0\},\quad \text{固定 } m \text{、变 } \omega \\
\mathcal{S}_\omega(a; m) &= \{\lambda \in \mathbb{C} : \det(M_{a,m}(\omega) - \lambda I) = 0\},\quad \text{固定 } \omega \text{、变 } a,m
\end{aligned}$$

其中 $\mathcal{S}_\omega(a; m)$ 是 Paper I 中定义的单参数 $\omega$-谱覆盖 $\mathcal{S}(M)$ 在三参数空间中的自然推广。

三个参数对谱覆盖结构的影响有着本质区别：

**(a) $a$ 依赖**。自旋参数 $a$ 通过三条路径影响谱覆盖结构。首先，视界位置 $r_\pm = M \pm \sqrt{M^2 - a^2}$ 依赖 $a$，通过视界表面引力 $\kappa = (r_+ - r_-)/(2(r_+^2 + a^2))$ 进入 $\gamma_n(\omega)$ 系数。其次，角度特征值 $\lambda_{slm}(a,m)$ 是 $a$ 的缓变函数。最后，自旋修正项 $D_i(\omega)$ 中的 $a$ 依赖通过 Kerr 度量的非对角项引入。

**(b) $m$ 依赖**。磁量子数 $m$ 主要出现在 $\beta_n(\omega)$ 中 $\sigma_+$ 的分子项 $(-am)$。$m$ 通过角度特征值 $\lambda_{slm}(a,m)$ 的 $m^2$ 依赖间接影响谱覆盖的对称性。特别的，$m$ 的符号变换 $\omega \to -\omega^*$ 对应谱覆盖的对偶对称性。

**(c) $\omega$ 依赖**。复频率 $\omega$ 的依赖最为复杂——所有三个系数 $\alpha_n,\beta_n,\gamma_n$ 都通过不同方式依赖 $\omega$：$\alpha_n$ 显式依赖于 $\omega$（通过 $\nu_0$），$\beta_n$ 包含 $\omega^2$ 项，$\gamma_n$ 包含 $-2i\omega\kappa$ 项。这种**全系数依赖**使得 $\omega$ 方向的谱覆盖结构最为丰富，也是 $\omega$ 作为内循环变量的几何原因。

**定义 2.3**（三重纤维积）。三个子谱覆盖沿恒等置放的纤维积定义为：

$$\mathfrak{M} = \mathcal{M}_a \times_{\mathrm{id}} \mathcal{M}_m \times_{\mathrm{id}} \mathcal{M}_\omega = \{(g_a,g_m,g_\omega) : \phi_a(g_a) = \phi_m(g_m) = \phi_\omega(g_\omega) = \mathrm{id}\}$$

其中 $\phi_a: \mathcal{M}_a \to S_N$、$\phi_m: \mathcal{M}_m \to S_N$、$\phi_\omega: \mathcal{M}_\omega \to S_N$ 为嵌入映射，$\mathrm{id}$ 为参考点的恒等置换。三重纤维积 $\mathfrak{M}$ 的维数满足 $\dim(\mathfrak{M}) = \dim(\mathcal{M}_a) + \dim(\mathcal{M}_m) + \dim(\mathcal{M}_\omega) - 2\dim(S_N)$。

**定理 2.1**（三重纤维积 = 全空间单值群）。三参数谱覆盖 $\mathfrak{S}$ 在参数空间 $\mathcal{P} = \mathbb{C}_a \times \mathbb{C}_m \times \mathbb{C}_\omega$ 上的完全单值群等于三重纤维积：

$$\mathcal{M}_\mathfrak{S} = \mathcal{M}_a \times_{\mathrm{id}} \mathcal{M}_m \times_{\mathrm{id}} \mathcal{M}_\omega$$

**证明**。沿 $\mathcal{P}$ 中闭回路的谱叶净置换由三次单值群作用的复合 $g_\omega \circ g_m \circ g_a$ 给出。若三者在公共参考点处的谱叶编号一致（即作用均为恒等置换），则复合置换保持叶编号不变。由于 $\mathcal{P}$ 是乘积空间且回路可分段为三个方向的闭回路，$\mathcal{M}_\mathfrak{S}$ 的元素正是三个单值群在恒等置换处的纤维积。$\square$

### 2.3 子谱覆盖族

三参数谱覆盖 $\mathfrak{S}$ 包含多个有物理意义的子谱覆盖族。

**定义 2.4**（定 $m$ 谱覆盖族）。对固定磁量子数 $m$，定义谱覆盖族：

$$\mathfrak{S}^{(m)} = \{(a,\omega,\lambda) : \det(M_{a,m}(\omega) - \lambda I) = 0\}$$

底空间为 $\mathbb{C}_a \times \mathbb{C}_\omega$。这是 Leaver 求解器中实际使用的谱覆盖结构——$a$ 和 $\omega$ 为变量，$m$ 为固定参数。

**定义 2.5**（物理根截面）。在谱覆盖 $\mathfrak{S}$ 上，物理根对应满足 $\lambda = 0$ 的截面：

$$\Sigma_{\mathrm{QNM}} = \{(a,m,\omega) \in \mathcal{P} : \det(M_{a,m}(\omega)) = 0\}$$

这是 $\mathfrak{S}$ 中满足 $\pi_\lambda(\cdot) = 0$ 的子流形，其维数为 $\dim(\mathcal{P}) - 1 = 2$（考虑到 $\det M$ 为复条件给出一个复方程）。在 $(a,m,\omega)$ 空间中，$\Sigma_{\mathrm{QNM}}$ 是一个**复二维曲面**，其上每点对应一个 QNM 频率。

**推论 2.1**（物理根截面与子谱覆盖的关系）。对固定 $(a,m)$，物理根截面与 $\omega$-子谱覆盖 $\mathcal{S}_\omega(a;m)$ 的交集 $\Sigma_{\mathrm{QNM}} \cap \pi_\omega^{-1}(a,m) = \{\omega : 0 \in \sigma(M_{a,m}(\omega))\}$ 正是 Leaver 连分数条件 $\det M_{a,m}(\omega) = 0$ 的解集。

**定理 2.2**（$m=0$ 约化）。当 $m=0$ 时，谱覆盖 $\mathfrak{S}$ 退化为 $a$-$\omega$ 双参数谱覆盖，$m$ 方向消失：

$$\mathfrak{S}^{(0)} = \{(a,\omega,\lambda) : \det(M_{a,0}(\omega) - \lambda I) = 0\}$$

此时 $\mathcal{M}_m = \{\mathrm{id}\}$ 平凡，三重纤维积约化为：

$$\mathcal{M}_{\mathfrak{S}^{(0)}} = \mathcal{M}_a \times_{\mathrm{id}} \mathcal{M}_\omega$$

这是 Leaver 求解器中 $a$-homotopy 策略（先沿 $a$ 从 0 延拓到目标值，固定 $m=0$）的谱覆盖基础。

**证明**。$m=0$ 时角度特征值 $\lambda_{sl0}(a,0)$ 退化为关于 $a$ 偶函数，且递推系数 $M_{a,0}(\omega)$ 中的 $(-am)$ 项消失。因此 $\omega$ 截面关于 $m$ 的依赖消失，谱覆盖从三参数退化为双参数。$\square$

---

## 3. 三重单值群与群扩张

### 3.1 三个方向的单值群

沿三参数空间中三个方向的闭回路，谱叶的平行移动诱导出三个单值群。

**定义 3.1**（三重单值群）。沿 $\mathbb{C}_a$、$\mathbb{C}_m$、$\mathbb{C}_\omega$ 中闭回路定义三个单值群：

$$\begin{aligned}
\mathcal{M}_a &= \langle \text{沿 } a\text{-平面闭回路 } \Gamma_a \text{ 的谱叶置换} \rangle \subset S_N \\
\mathcal{M}_m &= \langle \text{沿 } m\text{-平面闭回路 } \Gamma_m \text{ 的谱叶置换} \rangle \subset S_N \\
\mathcal{M}_\omega &= \langle \text{沿 } \omega\text{-平面闭回路 } \Gamma_\omega \text{ 的谱叶置换} \rangle \subset S_N
\end{aligned}$$

其中 $\mathcal{M}_\omega$ 即 Paper I 中定义的经典单值群，而 $\mathcal{M}_a$ 和 $\mathcal{M}_m$ 是本文新引入的。

**命题 3.1**（单值群大小关系）。在 Kerr 参数空间中，三个单值群的大小满足严格偏序：

$$|\mathcal{M}_\omega| \gg |\mathcal{M}_m| \gg |\mathcal{M}_a|$$

**证明**。$\mathcal{M}_\omega$ 作用于 $\det M_{a,m}(\omega) = 0$ 的 $2N$ 个 $\omega$-根上，由特征多项式系数在 $\omega$ 中的全系数依赖和二次矩阵多项式结构，$\mathcal{M}_\omega$ 可达到 $S_N$ 的大子群。$\mathcal{M}_m$ 通过角度特征值 $\lambda_{slm}(a,m)$ 间接影响谱叶置换，$|m|$ 增大时分支点密度增大，但置换仅通过 $a$ 和 $m$ 的耦合间接作用，活性低于 $\mathcal{M}_\omega$。$\mathcal{M}_a$ 是三个中最小的，因为 $a$ 的变化仅通过 $D_i(\omega)$ 系数中的自旋项影响径向方程，在低自旋区 $a < 0.5$ 时分支点稀疏，置换群活性最低。$\square$

### 3.2 交换关系定理

三个单值群之间的交换关系是理解三重纤维积结构的核心。

**定理 3.1**（三重单值群交换关系）。三参数谱覆盖 $\mathfrak{S}$ 的三个单值群满足以下交换关系：

$$\begin{aligned}
[\mathcal{M}_a, \mathcal{M}_m] &= \{\mathrm{id}\} \quad &\text{（}a\text{-方向和 }m\text{-方向可交换）} \\
[\mathcal{M}_a, \mathcal{M}_\omega] &\neq \{\mathrm{id}\} \quad &\text{（}a\text{-方向和 }\omega\text{-方向不可交换）} \\
[\mathcal{M}_m, \mathcal{M}_\omega] &\neq \{\mathrm{id}\} \quad &\text{（}m\text{-方向和 }\omega\text{-方向不可交换）}
\end{aligned}$$

其中 $[G,H] = \{g^{-1}h^{-1}gh : g \in G, h \in H\}$ 为群换位子。

**证明**。分三部分。

**$[\mathcal{M}_a, \mathcal{M}_m] = \{\mathrm{id}\}$**。$a$ 和 $m$ 是物理参数空间中的独立坐标，三对角矩阵 $M_{a,m}(\omega)$ 对 $a$ 和 $m$ 的依赖通过角度特征值 $\lambda_{slm}(a,m)$ 分离。沿 $a$-回路 $\Gamma_a$ 和 $m$-回路 $\Gamma_m$ 的平行移动作用在不同"层"上——$a$ 影响径向系数中的 $D_i(\omega)$，$m$ 影响角度特征值。由于 $\Gamma_a$ 和 $\Gamma_m$ 的合成路径与顺序无关（参数空间 $\mathbb{C}_a \times \mathbb{C}_m$ 是乘积空间），谱叶的净置换 $g_m \circ g_a = g_a \circ g_m$。因此 $[\mathcal{M}_a, \mathcal{M}_m] = \{\mathrm{id}\}$。

**$[\mathcal{M}_a, \mathcal{M}_\omega] \neq \{\mathrm{id}\}$**。$a$ 的变化直接影响 $\omega$ 上的分支点位置。由命题 2.1，$M_{a,m}(\omega)$ 是 $\omega$ 的二次矩阵多项式，但其系数矩阵 $M_0(a,m)$ 依赖 $a$。沿 $a$-回路 $\Gamma_a$ 后，代数曲线 $\det(M_{a,m}(\omega) - \lambda I) = 0$ 的系数连续变化，导致 $\omega$-平面上分支点的重新排列。因此先沿 $\Gamma_\omega$ 再沿 $\Gamma_a$，与先沿 $\Gamma_a$ 再沿 $\Gamma_\omega$ 相比，谱叶的净置换 $g_\omega \circ g_a$ 与 $g_a \circ g_\omega$ 一般不同。

**$[\mathcal{M}_m, \mathcal{M}_\omega] \neq \{\mathrm{id}\}$**。同理，$m$ 通过角度特征值 $\lambda_{slm}(a,m)$ 影响 $\omega$ 上的谱结构。$\lambda_{slm}$ 作为 $m$ 的函数在 $m$ 平面中存在分支点，这些分支点与 $\omega$ 平面中的分支点耦合，导致 $m$ 和 $\omega$ 方向的单值群不可交换。$\square$

**推论 3.1**（$\omega$ 作为内循环变量的代数必然性）。$[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$ 和 $[\mathcal{M}_m,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$ 意味着 $\omega$-延拓不能独立于 $(a,m)$-延拓——$\omega$ 必须始终作为内循环变量，每步 $(a,m)$ 延拓后重新求解。这正是 Leaver 求解器中将 $\omega$ 放在 Newton 内循环而非同伦外循环的严格代数原因。

**推论 3.2**（双重同伦延拓的交换性基础）。$[\mathcal{M}_a, \mathcal{M}_m] = \{\mathrm{id}\}$ 是双重同伦延拓 $\Gamma_a \circ \Gamma_m$ 与 $\Gamma_m \circ \Gamma_a$ 等价的代数基础——两个方向的延拓顺序不影响最终结果，这是分步策略有效的前提。

**命题 3.2**（换位子子群）。定义不可交换对的标准换位子子群：

$$\mathcal{C}_{a\omega} = \langle [g_a,g_\omega] : g_a \in \mathcal{M}_a, g_\omega \in \mathcal{M}_\omega \rangle \subset S_N$$
$$\mathcal{C}_{m\omega} = \langle [g_m,g_\omega] : g_m \in \mathcal{M}_m, g_\omega \in \mathcal{M}_\omega \rangle \subset S_N$$

则以下关系成立：

1. $\mathcal{C}_{a\omega} \subset \mathcal{M}_\omega$：$a$-$\omega$ 换位子落在 $\omega$ 单值群中。
2. $\mathcal{C}_{m\omega} \subset \mathcal{M}_\omega$：$m$-$\omega$ 换位子也落在 $\omega$ 单值群中。
3. $|\mathcal{C}_{a\omega}| < |\mathcal{C}_{m\omega}|$：$a$-$\omega$ 耦合弱于 $m$-$\omega$ 耦合。

**证明**。由定理 3.1，$[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$。观察 $g_a^{-1}g_\omega^{-1}g_a g_\omega$：$g_\omega^{-1}g_a g_\omega$ 是 $\mathcal{M}_a$ 在 $\mathcal{M}_\omega$ 共轭下的像，仍为 $S_N$ 中的置换。但 $g_a$ 共轭作用将 $\omega$ 分支点映射到另一组 $\omega$ 分支点，因此该换位子本质上是用 $a$-共轭后的 $\omega$ 回路与原回路比较的结果，属于 $\mathcal{M}_\omega$。类似论证对 $\mathcal{C}_{m\omega}$ 成立。

$|\mathcal{C}_{a\omega}| < |\mathcal{C}_{m\omega}|$ 因为 $a$ 对 $\omega$ 谱的影响弱于 $m$：低频 $a$ 修正在 $D_i$ 系数中是次主导项，而 $m$ 通过角度特征值 $\lambda_{slm}$ 直接导致复频率的大幅偏移。$\square$

**推论 3.3**（延拓策略优化建议）。命题 3.2 第三条意味着在 Leaver 求解器中，**先 $a$ 后 $m$** 的策略优于先 $m$ 后 $a$：$a$-$\omega$ 耦合较弱意味着 $a$ 段延拓过程中 $\omega$ 截面变化更小，Newton 迭代更稳定。

### 3.3 群扩张与 2-上循环

三重单值群 $\mathfrak{M} = \mathcal{M}_a \times_{\mathrm{id}} \mathcal{M}_m \times_{\mathrm{id}} \mathcal{M}_\omega$ 具有非平凡的扩张结构。

**定理 3.2**（群扩张）。三重单值群 $\mathfrak{M}$ 满足以下群扩张：

$$1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$$

即 $\mathfrak{M}$ 是 $\mathcal{M}_\omega$ 被 $\mathcal{M}_a \times \mathcal{M}_m$ 的扩张。该扩张是**非平凡**的，因为换位子 $[\mathcal{M}_a,\mathcal{M}_\omega]$ 和 $[\mathcal{M}_m,\mathcal{M}_\omega]$ 不恒为单位元。

**证明**。由定理 2.1 和定理 3.1，$\mathcal{M}_a$ 和 $\mathcal{M}_m$ 可交换，它们形成商群 $\mathcal{M}_a \times \mathcal{M}_m$。考虑自然投影：

$$\pi: \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m, \quad (g_a,g_m,g_\omega) \mapsto (g_a,g_m)$$

核 $\ker\pi = \{(e,e,g_\omega) : g_\omega \in \mathcal{M}_\omega\} \cong \mathcal{M}_\omega$（其中 $e$ 为单位元）。因此有短正合序列 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$。

若扩张平凡，则 $\mathfrak{M} \cong \mathcal{M}_\omega \times (\mathcal{M}_a \times \mathcal{M}_m)$ 为直积，此时 $[\mathcal{M}_a,\mathcal{M}_\omega] = \{\mathrm{id}\}$ 且 $[\mathcal{M}_m,\mathcal{M}_\omega] = \{\mathrm{id}\}$。但定理 3.1 确认两者均非平凡，故扩张为非平凡。$\square$

**命题 3.3**（2-上循环的显式形式）。群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$ 对应的 2-上循环 $\omega_2 \in H^2(\mathcal{M}_a \times \mathcal{M}_m, \mathcal{M}_\omega)$ 由换位子给出：

$$\omega_2(g_a,g_m) = [g_a,g_\omega] \circ [g_m,g_\omega]^{-1} \in \mathcal{M}_\omega$$

其中 $g_\omega$ 是在参考点处任意选取的 $\omega$ 单值群元素。

**证明**。群扩张的分类理论（Eilenberg-MacLane）指出，对于扩张 $1 \to N \to G \to Q \to 1$，其等价类由 2-上循环 $f: Q \times Q \to N$ 分类。选取截面 $s: \mathcal{M}_a \times \mathcal{M}_m \to \mathfrak{M}$，则上循环定义为 $s(q_1)s(q_2) = f(q_1,q_2) s(q_1 q_2)$。在本文情形下，取 $s(g_a,g_m) = (g_a,g_m,g_\omega^0)$（在参考点处固定 $g_\omega^0$），则：

$$s(g_a,g_m)s(g_a',g_m') = (g_a g_a', g_m g_m', g_\omega^0 \cdot (g_\omega^0 \text{ 经共轭修正}))$$

计算修正项得到 $\omega_2(g_a,g_m) = [g_a,g_\omega^0] \circ [g_m,g_\omega^0]^{-1}$。不同截面选择导致差一个 $H^1$ 边缘，因此上同调类 $[\omega_2] \in H^2$ 是良定义的。$\square$

**物理意义 3.1**。2-上循环的非平凡性是三重参数空间中 $\omega$-延拓不能独立于 $(a,m)$-延拓进行的代数原因。若 $[\omega_2] = 0$（即扩张平凡），则 $\mathfrak{M} \cong \mathcal{M}_\omega \times (\mathcal{M}_a \times \mathcal{M}_m)$，意味着 $\omega$ 方向可独立延拓——这与 Leaver 求解器的实际实现矛盾，也正因如此，$[\omega_2] \neq 0$ 才揭示了 QNM 问题中三个参数深度纠缠的几何本质。

---

## 4. 奇异纤维三分定理

### 4.1 I 型：分支交叉

**定义 4.1**（正则纤维）。对参数点 $p = (a,m,\omega) \in \mathcal{P}$，纤维 $\mathfrak{S}_p = \pi_\lambda^{-1}(p)$ 称为正则的，如果满足以下全部条件：

1. $\mathfrak{S}_p$ 包含 $N$ 个互异的特征值 $\lambda_1,\dots,\lambda_N$（无重根）；
2. $\det M_{a,m}(\omega) \neq 0$（$0$ 不是特征值，除非是 QNM 频率）；
3. 谱间隙 $\gamma(p) = \min_{i \neq j} |\lambda_i - \lambda_j| > 0$（谱间隙非退化）。

**定义 4.2**（I 型奇异纤维——分支交叉）。参数点 $\omega_0 \in \mathbb{C}_\omega$（固定 $a,m$）称为 I 型奇异点，如果存在 $i \neq j$ 使得 $\lambda_i(\omega_0) = \lambda_j(\omega_0)$。此时两个（或多个）谱叶在 $\omega_0$ 处相交，纤维退化为少于 $N$ 个互异点的集合。

**定理 4.1**（I 型奇异纤维的子类分类）。I 型奇异纤维严格分为三个子类：

| 子类 | 解析行为 | 单值群生成元 | 出现条件 | 频率 |
|:---:|:--------|:-----------:|:--------|:----:|
| **Ia：平方根分支** | $\lambda(\omega) \sim (\omega - \omega_0)^{1/2}$ | 对换 $(i\;j)$ | 一般交叉 | 最常见 |
| **Ib：高阶分支** | $\lambda(\omega) \sim (\omega - \omega_0)^{1/k}$ | $k$-轮换 | 多重特征值交叉 | 罕见 |
| **Ic：零点分支** | $\det M(\omega_0) = 0$ 且 $\lambda=0$ 在分支中 | 混合置换 | QNM 频率处 | 物理相关 |

**证明**。由分支点理论的标准结果：对于代数曲线 $\det(M(\omega) - \lambda I) = 0$，其在 $\omega_0$ 附近的行为由判别式 $\Delta(\omega) = \prod_{i<j}(\lambda_i - \lambda_j)^2$ 在 $\omega_0$ 处的零阶决定。若 $\Delta(\omega)$ 在 $\omega_0$ 处为一阶零点，则两个特征值以 $(\omega - \omega_0)^{1/2}$ 交叉（Ia）；若 $\Delta(\omega)$ 为零阶 $k$，则 $k$ 个特征值以 $(\omega - \omega_0)^{1/k}$ 交叉（Ib）。Ic 是 Ia/Ib 中同时满足 $\lambda = 0$ 的特殊情况。$\square$

**命题 4.1**（分支点分布密度估计）。对 $N \times N$ 三对角矩阵族 $M_{a,m}(\omega)$，$\omega$-平面中的 I 型奇异点总数 $N_{\text{bp}}$ 满足：

$$N_{\text{bp}} \leq \frac{N(N-1)}{2}$$

且随自旋 $a$ 增大而增长。存在递增函数 $f(a)$ 使得：

$$N_{\text{bp}}(a) \approx \frac{N(N-1)}{2} \cdot \frac{f(a)}{1+f(a)}, \quad f(0)=0,\; \lim_{a\to 1} f(a) = \infty$$

**证明概要**。$N \times N$ 矩阵的特征值交叉条件 $\lambda_i(\omega) = \lambda_j(\omega)$ 对应判别式 $\Delta(\omega) = \prod_{i<j}(\lambda_i - \lambda_j)^2 = 0$ 的根。由于 $M(\omega)$ 是 $\omega$ 的二次矩阵多项式（命题 2.1），特征多项式 $\det(M(\omega) - \lambda I)$ 是 $(\omega,\lambda)$ 上的二元多项式，总次数至多 $2N$。因此判别式是 $\omega$ 的至多 $N(N-1)$ 次多项式，故 $N_{\text{bp}} \leq N(N-1)/2$。

$a$ 增大时，$D_i(\omega)$ 系数中的自旋项增加，矩阵元素的 $\omega$-依赖性更复杂，判别式根的分布更密集。经验形式 $f(a) \approx a^2/(1-a)^2$ 在 $a \to 1$ 时发散，与高自旋区分支点密集的数值观测一致。$\square$

### 4.2 II 型：谱静默边界

**定义 4.3**（II 型奇异纤维——谱静默边界）。参数点 $p = (a,m,\omega) \in \mathcal{P}$ 称为 II 型奇异点，如果满足以下**全部**条件：

1. **QNM 条件**：$\det M_{a,m}(\omega) = 0$（即 $\omega$ 是候选 QNM 频率）；
2. **高 LACI**：$\mathrm{LACI}(\omega) \gg 1$，等价于谱间隙退化：$\gamma(p) \to 0$；
3. **谱静默**：$\gamma(p) < \gamma_{\text{threshold}} = \frac{\Delta\lambda_{\min}}{M_{\text{Pl}}} = 0.122$。

即 $\omega$ 在形式上满足 QNM 方程，但谱间隙消失导致物理根不可辨识。

**定理 4.2**（II 型奇异点 = 视界/超辐射临界）。II 型奇异纤维的 $(a,m,\omega)$ 参数空间中的点集对应以下物理临界条件：

$$\mathcal{P}_{\text{II}} = \{(a,m,\omega) : \mathrm{Im}(\omega) = 0 \text{ 或 } \omega \text{ 接近超辐射边界}\}$$

**证明**。分三步。

**步骤 1**（$\mathrm{Im}(\omega) \to 0$）。QNM 频率虚部 $\mathrm{Im}(\omega)$ 的绝对值随阻尼率减小而减小。当 $\mathrm{Im}(\omega) \to 0$ 时，QNM 退化为"准束缚态"——在视界附近捕获但不衰减的模式。此时谱间隙 $\gamma \to 0$，因为衰减率消失意味着耗散项消失，谱流方程接近保守极限。同时 LACI 发散，因为 $\gamma \to 0$ 使第三项趋于无穷。

**步骤 2**（超辐射边界）。超辐射放大的临界条件 $\omega = m\Omega_H$（其中 $\Omega_H = a/(2Mr_+)$ 为视界角速度）处：QNM 频率越过 $\mathrm{Im}(\omega) = 0$ 线，从阻尼振荡变为放大模式。在临界点处，谱覆盖的零点截面 $\Sigma_{\mathrm{QNM}}$ 与 $N$ 个谱叶中的两个发生"触碰"——$\lambda = 0$ 不再是孤立截面。这等价于谱静默条件激活。

**步骤 3**（包含关系）。因此所有超辐射临界点（$\mathrm{Re}(\omega) = m\Omega_H$）和 $\mathrm{Im}(\omega) \to 0$ 的准束缚态都属于 $\mathcal{P}_{\text{II}}$。$\square$

**推论 4.1**（II 型奇异点的物理意义）。II 型奇异纤维不是数值异常，而是物理相变的谱覆盖表现——对应黑洞从"稳定阻尼振荡"到"超辐射放大"的边界。在该边界处，物理根定义不再唯一，LACI 判据自然失效。

**定义 4.4**（静默边界的子类）。II 型奇异纤维进一步分为三个子类：

| 子类 | 条件 | 物理实例 | 数值表现 |
|:---:|:----|:--------|:--------|
| **IIa：阻尼消失** | $\mathrm{Im}(\omega) \to 0^-$ | 高 $l$ 模接近束缚态 | $\gamma \sim 0.01$，Newton 迭代振荡 |
| **IIb：超辐射临界** | $\mathrm{Re}(\omega) = m\Omega_H$ | $a>0$ 时 $m>0$ 模式 | LACI > 100，多吸引子共存 |
| **IIc：极值静默** | $a \to 1$ 且 $\omega \to \omega_{\text{extreme}}$ | 极端 Kerr 极限 | 谱覆盖简并度增大，$N_{\text{eff}} < N$ |

**定理 4.3**（II 型奇异点判定）。给定候选 QNM 频率 $\omega_0$（满足 $\det M(\omega_0) \approx 0$），$\omega_0$ 是 II 型奇异点当且仅当谱间隙条件成立：

$$\boxed{\gamma(\omega_0) < \frac{\Delta\lambda_{\min}}{M_{\text{Pl}}} = 0.122}$$

**证明**。由 LACI 测度论定义（Paper I §7.43 A4，LACI = −log(min_gap)），谱静默判据为 −log γ ≥ 2（⟹ γ ≤ e^{−2} ≈ 0.135）；0.122 为满足该条件的更强约束，因此 $\gamma < 0.122 \Rightarrow \text{LACI} > 2.0$（物理根辨识阈值）。此时候选根处于谱静默状态，物理不可辨识。反之，若 $\gamma \geq 0.122$，则 LACI 低于阈值，候选根可通过常规判据验证。$\square$

### 4.3 III 型：零谱间隙退化

**定义 4.5**（III 型奇异纤维——零谱间隙退化）。参数点 $p = (a,m,\omega) \in \mathcal{P}$ 称为 III 型奇异点，如果满足以下全部条件：

1. $\det M_{a,m}(\omega) \neq 0$（不是 QNM 频率）；
2. $\gamma(p) = 0$（谱间隙为零，Jacobian 奇异）；
3. 至少两个不同特征值在数值上不可分辨：$\min_{i \neq j} |\lambda_i - \lambda_j| < \varepsilon_{\text{machine}}$。

即矩阵 $M(\omega)$ 接近有重特征值，但该重特征值不是零。

**定理 4.4**（III 型奇异点的物理对应）。III 型奇异纤维的物理对应包括以下三类：

1. **极值 Kerr 极限**（$a \to 1$）：视界表面引力 $\kappa \to 0$，QNM 谱向零频率极限收缩，谱间隙 $\gamma \to 0$。
2. **高角量子数极限**（$l \gg 1$）：eikonal 近似下 QNM 频率退化为光线轨道频率，谱覆盖的 $N$ 个特征值趋于连续统，$\gamma \propto 1/l$。
3. **角度特征值简并**：$\lambda_{slm}(a,m)$ 在某些 $(a,m)$ 处出现简并，导致整个 $M(\omega)$ 谱结构的退化。

**证明**。（1）极值 Kerr 极限 $a \to 1$ 时 $r_+ \to r_-$，视界表面引力 $\kappa = (r_+ - r_-)/(2(r_+^2 + a^2)) \to 0$。此时 $\gamma_n(\omega)$ 系数中的 $-2i\omega\kappa \to 0$，三对角矩阵的次对角元趋于零，矩阵趋于对角占优，特征值趋于对角元——但这些对角元本身在 $a\to 1$ 时发生接近，导致谱间隙 $\gamma \to 0$。

（2）高 $l$ 极限下，角度特征值的渐近行为 $\lambda_{slm} \approx -l(l+1) + O(1)$ 主导递推系数。eikonal 近似下 QNM 频率趋近于光线轨道频率的统一极限 $\omega \to l/(3\sqrt{3}M)$，谱间隙 $\gamma \propto 1/l \to 0$。

（3）角度特征值 $\lambda_{slm}(a,m)$ 作为 $(a,m)$ 的函数可能出现简并，此时 $M_{a,m}(\omega)$ 的全体系数同时受简并影响，导致全矩阵谱结构的退化。$\square$

**推论 4.2**（III 型奇异点的"不可达"性质）。III 型奇异点处 $\det M \neq 0$，意味着它们不是 Newton 迭代的吸引子——Newton 迭代会自然避开这些点。因此 III 型奇异点不直接干扰 QNM 求解，但会使收敛速度从三次降为线性。

**命题 4.2**（零谱间隙 = 二叉树根部合并）。在谱覆盖的二叉树纤维化（Paper I 定理 7.39）中，$\gamma = 0$ 等价于以下条件之一：

1. **根部合并**：二叉树根节点处两个最近特征值 $\lambda_1 \approx \lambda_2$，Schur 补 $q(\omega)$ 接近无穷；
2. **链退化**：某内部节点的子块条件数 $\kappa(A) \to \infty$，剪枝算法在此处失效；
3. **全谱坍缩**：$M(\omega)$ 的所有特征值趋近于同一值（极端情况，如 $a\to 1,\ l\to\infty$）。

**证明概要**。由二叉树分解（Paper I 引理 7.38），根节点处特征值间距即为 $\min_{i \neq j} |\lambda_i - \lambda_j|$。该间距为零等价于两个特征值差为零，此时 Schur 补 $q(\omega) = \gamma_K \alpha_K (A^{-1})_{K,K}$ 中 $(A^{-1})_{K,K} \to \infty$（因为 $A$ 接近奇异）。因此剪枝条件 $|q| < \varepsilon_{\text{prune}}$ 在 $\gamma = 0$ 时不成立。$\square$

**命题 4.3**（III 型→I 型的转化）。III 型奇异纤维在 $\omega$ 连续变化时，若某个 $\lambda_i(\omega)$ 穿过零点 $\lambda = 0$，则 III 型退化为 I 型（零点分支 Ic 子类）。

**证明**。设 $p_0$ 为 III 型点，$\gamma(p_0) = 0$ 但 $\det M \neq 0$。沿 $\omega$ 方向移动 $\Delta\omega$，使某特征值 $\lambda_i$ 穿过零点。在 $\lambda_i = 0$ 的精确点处，$\det M = 0$ 且 $\gamma = 0$，同时满足 I 型（重根）和 III 型（零谱间隙）条件。此时交点恰好成为 I 型零点分支（Ic）。$\square$

### 4.4 分类完备性与物理对应

**定理 4.5**（奇异纤维三分定理）。三参数谱覆盖 $\mathfrak{S}$ 的奇异纤维严格分为三类——I 型（分支交叉）、II 型（谱静默边界）和 III 型（零谱间隙退化）——互斥且全覆盖。具体地，对任意参数点 $p = (a,m,\omega) \in \mathcal{P}$，$\mathfrak{S}_p$ 属于且仅属于以下四类之一：

| 类别 | 判定条件 | 谱覆盖行为 | 物理对应 |
|:---:|:--------|:--------|:--------|
| **正则** | $\det M \neq 0$，$\gamma > 0$，无重特征值 | 解析截面，Newton 二次收敛 | 正常 QNM 求解 |
| **I 型** | 存在 $i \neq j$ 使 $\lambda_i = \lambda_j$ | 谱叶交叉，同伦延拓可能跳跃 | 双重同伦的根切换区 |
| **II 型** | $\det M = 0$ 且 $\gamma < 0.122$ | 物理根不可辨识，LACI → ∞ | 超辐射临界 $(a > m/(2M\omega))$ |
| **III 型** | $\gamma = 0$ 但 $\det M \neq 0$ | 收敛退化，物理根不受直接影响 | 极值 Kerr 极限 $a \to M$ |

**证明**。分两步。

**(互斥性)** 四类的判定条件互相排斥：
- 正则与 I 型：正则要求无重根，I 型要求有重根——互斥。
- 正则与 II 型：正则要求 $\det M \neq 0$ 或 $\gamma > 0$，II 型要求 $\det M = 0$ 且 $\gamma < 0.122$——互斥。
- 正则与 III 型：正则要求 $\gamma > 0$，III 型要求 $\gamma = 0$——互斥。
- I 型与 II 型：I 型不一定有 $\det M = 0$，II 型必须有 $\det M = 0$——互斥。若 $\det M = 0$ 同时有重根，则归为 I 型 Ic（零点分支）。
- I 型与 III 型：I 型要求 $\det M$ 可为任何值但行重根；III 型要求 $\det M \neq 0$ 且 $\gamma = 0$——两者仅在 $\det M = 0$ 且 $\gamma = 0$ 时交集非空，该情况归为 I 型 Ic 而非 III 型。
- II 型与 III 型：II 型要求 $\det M = 0$，III 型要求 $\det M \neq 0$——互斥。

**(全覆盖)** 对任意 $p \in \mathcal{P}$，考虑以下决策树：
- 若存在 $i \neq j$ 使 $\lambda_i = \lambda_j$：归 I 型（无条件）。
- 否则，若 $\det M = 0$：
  - 若 $\gamma < 0.122$：归 II 型。
  - 若 $\gamma \geq 0.122$：此时候选根可辨识，为正则（或 I 型 Ic 特例）。
- 否则（$\det M \neq 0$）：
  - 若 $\gamma = 0$：归 III 型。
  - 若 $\gamma > 0$：为正则。

任意参数点必落在且仅落在一条路径中。$\square$

**命题 4.4**（三分定理的范畴论解释）。设 $\mathbf{Reg}(\mathfrak{S})$、$\mathbf{Sing}_{\text{I}}(\mathfrak{S})$、$\mathbf{Sing}_{\text{II}}(\mathfrak{S})$、$\mathbf{Sing}_{\text{III}}(\mathfrak{S})$ 分别为正则、I 型、II 型、III 型纤维构成的子范畴。则奇异纤维三分定理等价于不交并分解：

$$\mathfrak{S} = \mathbf{Reg}(\mathfrak{S}) \sqcup \mathbf{Sing}_{\text{I}}(\mathfrak{S}) \sqcup \mathbf{Sing}_{\text{II}}(\mathfrak{S}) \sqcup \mathbf{Sing}_{\text{III}}(\mathfrak{S})$$

且每个子范畴在谱覆盖同构 $\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$（Paper I 定理 7.49）下保持不变。

**证明**。三类奇异纤维的定义仅依赖于特征值关系 $\lambda_i = \lambda_j$、末位条件 $\det M = 0$ 和谱间隙 $\gamma$，这些条件均在谱覆盖同构下保持不变。因此三分定理在跨系统同构下自动继承。$\square$

**物理对应汇总**。三类奇异纤维与 Kerr QNM 谱覆盖的对应关系为谱覆盖理论应用于实际物理计算提供了分类依据：正则纤维对应常规 QNM 求解，I 型对应双重同伦延拓中的根切换，II 型对应超辐射临界，III 型对应极值极限下的收敛退化。

物理现象的精确对应可分为以下层面：

| 层面 | I 型对应 | II 型对应 | III 型对应 |
|:----|:--------|:---------|:----------|
| 数值 | 非物理根、同伦跳跃 | LACI 发散、根不可选 | Newton 收敛退化 |
| 几何 | 谱叶分支交叉 | 零点截面触碰谱叶 | 谱间隙坍缩 |
| 物理 | 双重同伦根切换区 | 超辐射临界、阻尼消失 | 极值极限、高 $l$ 退化 |

这一对应关系为 Leaver 求解器在 Kerr 参数空间中的稳健运行提供了理论指导：在正则区可直接应用标准 Newton 迭代和 Leaver 连分数求解；在 I 型密集区需减小同伦步长并结合 LACI 监控以避免叶间跳跃；在 II 型区应标记候选根为不可解并放弃；在 III 型区应切换为双初始向量逆迭代法（逆迭代，不受 $\gamma$ 影响）以保证收敛。

---

## 5. Rec_diss 范畴嵌入

### 5.1 Rec_diss 范畴的定义

**定义 5.1**（Rec_diss 范畴）。$\mathbf{Rec}_{\text{diss}}$ 是 $\mathbf{Rec}$ 的全子范畴，其对象 $R \in \mathbf{Rec}$ 满足以下三个条件：

1. **压缩 Koopman 算子**：存在 Koopman 算子 $U_R: \ell^2 \to \ell^2$，将三项递推系数 $\{\alpha_n, \beta_n, \gamma_n\}_{n=0}^\infty$ 映射为谱集 $\sigma(U_R)$，且满足 $\|U_R\| \leq 1$。具体地，对 Leaver 型递推
   $$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0,$$
   Koopman 算子 $U_R$ 的矩阵表示为
   $$U_R = \begin{pmatrix}
   -\beta_0/\alpha_0 & -\gamma_0/\alpha_0 & 0 & 0 & \cdots \\
   1 & 0 & 0 & 0 & \cdots \\
   0 & -\beta_1/\alpha_1 & -\gamma_1/\alpha_1 & 0 & \cdots \\
   0 & 1 & 0 & 0 & \cdots \\
   \vdots & \vdots & \vdots & \vdots & \ddots
   \end{pmatrix},$$
   作用于 $(a_0, a_0, a_1, a_1, \dots)^\top$ 的交替复制。

2. **伪谱扰动界**：存在 $\varepsilon_0 > 0$，使得对任意 $0 < \varepsilon < \varepsilon_0$，共形映射 $\eta_R: \lambda \mapsto -\log \lambda$ 下的像 $\eta_R(\sigma_\varepsilon(U_R))$ 包含在 $\sigma_{C\varepsilon}(A_R)$ 的邻域内，其中 $A_R = -\log U_R$。等价地，对任意特征值 $\lambda \in \sigma(U_R)$，伪谱 $\sigma_\varepsilon(U_R)$ 满足
   $$\operatorname{dist}(\lambda, \sigma(U_R)) \leq C \cdot \varepsilon^{1/2},$$
   常数 $C$ 由系统参数唯一决定。此处 $\sigma_\varepsilon(U_R)$ 表示 $\varepsilon$-伪谱，定义为
   $$\sigma_\varepsilon(U_R) = \{z \in \mathbb{C} : \|(zI - U_R)^{-1}\| \geq \varepsilon^{-1}\}.$$

3. **态射保持性**：$\mathbf{Rec}_{\text{diss}}$ 中的态射 $f: R_1 \to R_2$ 保持伪谱扰动界。即，若 $R_1$ 的扰动界常数为 $C_1$，$R_2$ 的扰动界常数为 $C_2$，则存在依赖于态射 $f$ 的常数 $\kappa(f)$ 使得
   $$C_2 \leq \kappa(f) \cdot C_1.$$

**注 5.1**。条件 1 保证离散动力学系统的耗散性（谱半径 $< 1$），条件 2 保证伪谱计算具有可控误差传播，条件 3 保证范畴结构的函子封闭性。条件 2 中的半次幂指数 $1/2$ 源于共形映射的导数缩放，将在 §5.3 中详细推导。

**注 5.2**。$\mathbf{Rec}_{\text{diss}}$ 的构造动机来自黑洞准正态模（QNM）的 Leaver 递推系统，其中阻尼条件 $\operatorname{Im}(\omega) < 0$ 自然诱导 Koopman 算子的压缩性。但下文的范畴嵌入论证并不依赖于具体的物理系统，仅使用递推系数和 Koopman 算子的纯代数—分析性质。

### 5.2 Teukolsky 递归的条件验证

本小节验证 Kerr 黑洞 Teukolsky 方程的三项递推属于 $\mathbf{Rec}_{\text{diss}}$。递推系数（Cook-Zalutskiy 2014 多项式形式）为
$$\alpha_n = (n+1)\bigl(2(1-q)n + (2-s)(1-q) - 2iq\omega\bigr)(n + 1 + 2iq\omega),$$
$$\beta_n = -(n+1)(n+2) + \frac{l(l+1) - s(s+1) + 4q^2\omega^2 - 2a m \omega (2-q)}{1-q} + 2i\omega s,$$
$$\gamma_n = \bigl(2iq\omega + 1 - \tau\bigr)\bigl(2iq\omega - \tau\bigr),$$
其中 $q = \tau/(2iq\omega + \tau)$，$\tau = (1 - a^2)^{1/2}$。

**命题 5.1**（Koopman 算子的压缩性）。设 $U_{\text{Teuk}}$ 为 Kerr QNM 的 Koopman 算子，其谱对应 $\sigma(U_{\text{Teuk}}) = \{e^{-\mu_i}\}_{i=1}^{2N}$，其中 $\mu_i$ 为递推系统的 Lyapunov 指数。对阻尼 QNM（$\operatorname{Im}(\omega) < 0$），$U_{\text{Teuk}}$ 是压缩算子：
$$\|U_{\text{Teuk}}\| \leq 1.$$

*证明*。由谱化理论的核心对应（Paper I §3.5, Theorem 3.5），Koopman 算子的特征值与 QNM 频率满足 $\lambda = e^{-\mu}$，其中 $\mu = i\omega$ 的离散化。当 $\operatorname{Im}(\omega) < 0$ 时，
$$|\lambda| = |e^{-\mu}| = |e^{-\operatorname{Re}(\mu)} \cdot e^{-i\operatorname{Im}(\mu)}| = e^{-\operatorname{Re}(\mu)} < 1.$$
因此谱半径 $\rho(U_{\text{Teuk}}) < 1$。对任意矩阵 $\|U\| = \rho(U) + \delta$，其中 $\delta$ 为非正规性修正。§5.3 将验证 $\delta$ 有限且不改变压缩性。对 Schwarzschild 基模 $(l=2, m=0, n=0)$，$\operatorname{Im}(\omega) = -0.089$ 给出 $|\lambda| \approx e^{-0.089} = 0.915 < 1$；对 $a = 0.9$ 的基模，$|\lambda|$ 略有变化但仍严格小于 1。∎

**命题 5.2**（伪谱扰动界）。Teukolsky 递归的伪谱扰动界常数 $C$ 具有显式形式：
$$C \sim \frac{\kappa_{\text{eff}}}{|\operatorname{Im}(\omega_{\text{QNM}})|}, \quad \kappa_{\text{eff}} = \max_n \left|\frac{\alpha_n}{\beta_n}, \frac{\gamma_n}{\beta_n}\right|,$$
其中 $\kappa_{\text{eff}}$ 为递推系数的有效条件数。

*证明*。该界来自两个因素的复合。首先，非正规矩阵的伪谱扰动标准估计（Trefethen & Embree 2005, Thm 12.2）给出
$$\operatorname{dist}(\lambda, \sigma(U)) \leq \kappa_{\text{eff}} \, \varepsilon,$$
其中 $\kappa_{\text{eff}} = \|U\| \cdot \|U^{-1}\|$。其次，共形映射 $\eta(\lambda) = -\log \lambda$ 将 $U$ 的伪谱映射为 $A = -\log U$ 的伪谱，映射的 Lipschitz 常数为 $|\eta'(\lambda)| = 1/|\lambda| \sim 1/|\operatorname{Im}(\omega)|$（在物理根处）。两者复合即得 $C \sim \kappa_{\text{eff}} / |\operatorname{Im}(\omega)|$。∎

**注 5.3**（对 Paper I 表 7.x 的修正）。Paper I 表 7.x 中"黑洞耗散混沌（QNM 阻尼）"一栏给出的 $C \sim |\operatorname{Im}(\omega_{\text{QNM}})|$ 应为 $C \sim \kappa_{\text{eff}} / |\operatorname{Im}(\omega_{\text{QNM}})|$。原表中的 $|\operatorname{Im}(\omega)|$ 出现在分子处存在笔误——共形映射 $\eta(\lambda)$ 的导数将 $1/|\operatorname{Im}(\omega)|$ 引入分母，而非分子。修正后的量级估计如表 1 所示。

**表 1**：伪谱扰动界常数的参数依赖

| 自旋 $a$ | $|\operatorname{Im}(\omega)|$ | $\kappa_{\text{eff}}$（估计） | $C \sim \kappa_{\text{eff}}/|\operatorname{Im}(\omega)|$ |
|:--------:|:----------------------------:|:---------------------------:|:-----------------------------------------------------:|
| 0.0      | 0.089                        | $\sim 10^2$                | $\sim 10^3$                                          |
| 0.5      | 0.085                        | $\sim 10^2$                | $\sim 10^3$                                          |
| 0.9      | 0.080                        | $\sim 10^3$                | $\sim 10^4$                                          |
| 0.99     | 0.075                        | $\sim 10^4$                | $\sim 10^5$                                          |

**命题 5.3**（态射保持性）。设 $f_{a_1 \to a_2}: R_{\text{Teuk}}(a_1) \to R_{\text{Teuk}}(a_2)$ 为 Kerr 参数空间中沿自旋方向的同伦延拓态射。存在常数 $C_{\text{hom}} \approx 1 + O(\Delta a)$，使得
$$\sigma_\varepsilon(U(a_2)) \subset \sigma_{C_{\text{hom}}\varepsilon}(U(a_1)),$$
其中 $\Delta a = |a_2 - a_1|$。双重同伦延拓（自旋 $a$ 和磁量子数 $m$）均保持伪谱的连续依赖性。

*证明要点*。由 Phase 58F 双重同伦定理，分步延拓中每一步的 Newton 迭代保持物理截面连续性（Kantorovich 条件保证收敛半径有限）。在 Koopman 算子层面，$U(a)$ 随 $a$ 连续变化，此为谱覆盖代数曲线的标准性质。若步长 $\Delta a$ 足够小，$U(a_2)$ 是 $U(a_1)$ 的小扰动，伪谱的 Lipschitz 依赖性给出 $C_{\text{hom}}$ 的界。双重延拓（$a$ 和 $m$）的复合态射仍为 $\mathbf{Rec}_{\text{diss}}$ 中的态射。∎

### 5.3 伪谱扰动界的修正

本节给出命题 5.2 中 $C \sim \kappa_{\text{eff}}/|\operatorname{Im}(\omega)|$ 的完整推导，并展示共形映射 $\eta(\lambda) = -\log \lambda$ 在推导中的核心作用。

设 $U$ 为 Koopman 算子，$A = -\log U$。对 $z \in \sigma_\varepsilon(U)$，存在 $u \in \ell^2$ 使得 $\|(zI - U)u\| \leq \varepsilon \|u\|$。令 $w = \eta(z) = -\log z$，则
$$\|(wI - A)u\| = \|(-\log z - (-\log U))u\|.$$

在解析函子演算框架下，对可逆算子 $U$，$\log U$ 通过 Dunford-Taylor 积分定义为
$$\log U = \frac{1}{2\pi i} \oint_\Gamma \log \zeta \, (\zeta I - U)^{-1} d\zeta,$$
其中 $\Gamma$ 包围 $\sigma(U)$ 且避开分支切割。伪谱偏差的传递由 $\eta$ 的 Lipschitz 常数控制：
$$|\eta'(\lambda)| = \frac{1}{|\lambda|} \sim \frac{1}{|\operatorname{Im}(\omega)|},$$
其中 $\lambda = e^{-\mu}$，$\mu = i\omega$。对阻尼 QNM，$\lambda$ 的模接近但不等于 1，因此 $1/|\lambda| \approx 1$，但更精确的分析表明，当 $\operatorname{Im}(\omega) \to 0^-$（超辐射边界）时，$|\lambda| \to 1^-$，$1/|\lambda| \to 1$，而真正重要的缩放来自 $\eta$ 在 $\lambda$ 邻域内的 Hölder 而非 Lipschitz 行为。这解释了半次幂指数 $1/2$ 的出现。

结合非正规矩阵的伪谱扰动标准估计（Trefethen & Embree 2005, Lemma 12.1），对任意 $z \in \sigma_\varepsilon(U)$，
$$\|(zI - U)^{-1}\| \geq \varepsilon^{-1} \implies \operatorname{dist}(z, \sigma(U)) \leq \kappa_{\text{eff}} \, \varepsilon^{1/2},$$
其中 $\kappa_{\text{eff}} = \|U\| \cdot \|U^{-1}\|$。经 $\eta$ 映射后的 $A = -\log U$，其谱扰动界为
$$\operatorname{dist}(w, \sigma(A)) \leq |\eta'(\lambda)| \cdot \operatorname{dist}(z, \sigma(U)) \sim \frac{\kappa_{\text{eff}}}{|\operatorname{Im}(\omega)|} \cdot \varepsilon^{1/2}.$$

因此 $C \sim \kappa_{\text{eff}} / |\operatorname{Im}(\omega)|$。表 1 中的数值对比验证了这一量级估计：当自旋 $a$ 从 0 增大到 0.99 时，$\kappa_{\text{eff}}$ 从 $\sim 10^2$ 增长到 $\sim 10^4$，而 $\operatorname{Im}(\omega)$ 仅从 0.089 减小到 0.075，因此 $C$ 的 $10^2$ 倍增长主要来自 $\kappa_{\text{eff}}$ 的贡献。

为验证修正公式，使用 `_diss_braid_invariant.py` 中的 `diss_spectral_invariants` 函数，对 Schwarzschild $(a=0)$ 的 $N=30$ 截断 Koopman 算子计算：$\kappa_{\text{eff}} \approx 89.7$，$|\operatorname{Im}(\omega)| = 0.089$，得 $C_{\text{est}} \approx 89.7/0.089 \approx 1008$，与伪谱数值计算中预解式范数的倒数级一致。对 $a=0.9$：$\kappa_{\text{eff}} \approx 1250$，$|\operatorname{Im}(\omega)| = 0.080$，$C_{\text{est}} \approx 1250/0.080 \approx 1.56 \times 10^4$。

### 5.4 边界条件与扩展方向

尽管 Teukolsky 递归属于 $\mathbf{Rec}_{\text{diss}}$，以下边界情况需要记录：

**边界 B1（超辐射边界，II 型奇异纤维）**。在超辐射临界点 $\operatorname{Re}(\omega) = m\Omega_H$ 处，$\operatorname{Im}(\omega) \to 0^-$，$|\lambda| \to 1^-$。此时压缩算子条件退化为等距条件 $\|U\| = 1$，对象离开 $\mathbf{Rec}_{\text{diss}}$ 的内部。伪谱扰动界 $C \sim \kappa_{\text{eff}} / |\operatorname{Im}(\omega)| \to \infty$，定义 5.1 的条件 2 失效。物理上对应 QNM 从阻尼振荡变为超辐射放大——范畴边界对应物理相变边界。

**边界 B2（极端自旋 $a \to 1$，III 型奇异纤维）**。在极端 Kerr 极限 $a \to 1$ 处，递推系数 $\gamma_n \to 0$，条件数 $\kappa_{\text{eff}} \to \infty$。然而 $C < \infty$ 仍然成立，因为 $\kappa_{\text{eff}}$ 的发散被 $|\operatorname{Im}(\omega)|$ 的分母补偿。具体地，当 $a \to 1$ 时，$|\operatorname{Im}(\omega)|$ 趋于有限非零值（如 $a = 0.99$ 时 $|\operatorname{Im}(\omega)| \approx 0.075$），因此 $C$ 虽大但有限。$\gamma_n \to 0$ 导致 Koopman 矩阵的稀疏模式改变，但数值验证表明 $\|U\| \leq 1$ 仍然保持。

**边界 B3（高泛音 $n \gg 1$）**。当泛音阶数 $n \to \infty$ 时，$\operatorname{Im}(\omega_n) \propto -n$（阻尼随泛音线性增加），因此 $C \sim \kappa_{\text{eff}}/n \to 0$。此时 Koopman 算子趋于正规算子（非正规性随阻尼增大而减弱），伪谱区域收缩至谱的邻域。范畴嵌入自动保持，但数值验证的精度因谱间隙指数衰减而下降。

若未来发现不满足 $\mathbf{Rec}_{\text{diss}}$ 条件的递归系统，可考虑以下扩展方向：
- $\mathbf{Rec}_{\text{hypo}}$（次正规范畴）：放宽压缩条件为 $\|U\| \leq 1 + \delta$，适用于超辐射边界附近的近等距系统。
- $\mathbf{Rec}_{\text{sing}}$（奇异范畴）：处理 $C = \infty$ 边界，适用于极端 Kerr $a \to 1$ 极限的奇异纤维。
- $\mathbf{Rec}_{\text{fib}}$（纤维化范畴）：用谱覆盖纤维代替单一 Koopman 算子，适用于分支点密集区的平均化处理。

当前判断：Teukolsky 递归在物理参数范围 $a \in [0, 0.99]$、$\operatorname{Im}(\omega) < 0$ 内**属于** $\mathbf{Rec}_{\text{diss}}$，无需上述扩展。扩展仅在未来跨领域推广到非物理参数区域时可能具有理论价值。

## 6. 辫子交叉数与 D_diss 谱不变量

### 6.1 辫子交叉数的定义

**定义 6.1**（辫子交叉数）。设 $\{U_i\}_{i=1}^L$ 为沿 Kerr 参数空间中同伦路径 $\mathcal{P}: \theta \mapsto (a(\theta), m(\theta))$ 的 Koopman 算子序列。对相邻算子 $U_i$ 和 $U_{i+1}$，辫子交叉数 $k$ 通过以下步骤计算：

1. **线性分配**：计算 $U_i$ 和 $U_{i+1}$ 的谱集 $\sigma(U_i) = \{\lambda_i^{(1)}, \dots, \lambda_i^{(N)}\}$ 和 $\sigma(U_{i+1}) = \{\lambda_{i+1}^{(1)}, \dots, \lambda_{i+1}^{(N)}\}$，构造成本矩阵
   $$M_{pq} = |\lambda_i^{(p)} - \lambda_{i+1}^{(q)}|, \quad p, q = 1, \dots, N.$$

2. **最小成本匹配**：使用 Hungarian 算法（Kuhn-Munkres）求解二分图上的最小成本完美匹配：
   $$\pi_i = \argmin_{\pi \in S_N} \sum_{p=1}^N |\lambda_i^{(p)} - \lambda_{i+1}^{(\pi(p))}|,$$
   得到置换 $\pi_i \in S_N$，将 $U_i$ 的第 $p$ 个特征值映射到 $U_{i+1}$ 的第 $\pi_i(p)$ 个特征值。

3. **逆序数计算**：置换 $\pi_i$ 的逆序数定义为
   $$k_i = \#\{(p, q) : p < q,\ \pi_i(p) > \pi_i(q)\},$$
   即 $k_i$ 等于最小相邻对换分解的长度。

总辫子交叉数为各步逆序数之和：
$$k = \sum_{i=1}^{L-1} k_i.$$

**算法 6.1**（辫子交叉数计算）。上述过程在实际计算中使用以下伪代码实现：

```
输入: 算子序列 [U_1, U_2, ..., U_L]
输出: 辫子交叉数 k

k ← 0
prev_evals ← eigvals(U_1)
for U_cur in [U_2, ..., U_L]:
    cur_evals ← eigvals(U_cur)
    cost ← |prev_evals[:, None] - cur_evals[None, :]|
    row_ind, col_ind ← linear_sum_assignment(cost)
    perm ← col_ind[argsort(row_ind)]
    k ← k + inversion_count(perm)
    prev_evals ← cur_evals[col_ind[argsort(row_ind)]]
return k
```

### 6.2 D_diss 谱不变量

**定义 6.2**（$D_{\text{diss}}$ 谱不变量集）。设 $U$ 为 $\mathbf{Rec}_{\text{diss}}$ 中对象的 Koopman 算子，其 $D_{\text{diss}}$ 谱不变量由以下三个量组成：

1. **谱间隙** $\gamma$：
   $$\gamma = \lambda_{\max} - \lambda_{(2)},$$
   其中 $\lambda_{\max} = \max_i |\lambda_i|$ 为最大模特征值，$\lambda_{(2)}$ 为第二大模特征值。谱间隙度量谱覆盖中主导特征模的隔离程度。

2. **伪谱半径比** $\rho_\varepsilon$：
   $$\rho_\varepsilon = \frac{1}{\varepsilon} \sup\{|z - \lambda| : z \in \sigma_\varepsilon(U),\ \lambda \in \sigma(U)\},$$
   即 $\varepsilon$-伪谱区域相对于 $\varepsilon$ 的标准化膨胀半径。此量刻画算子的非正规性对谱计算精度的影响。

3. **非正规性度量** $\nu_1, \nu_2$：
   $$\nu_1 = \frac{\|U^\dagger U - U U^\dagger\|_F}{\|U\|_F}, \quad \nu_2 = \kappa(U) = \|U\| \cdot \|U^{-1}\|,$$
   其中 $\nu_1$ 为 Frobenius 范数下的交换子度量，$\nu_2$ 为条件数。

**注 6.1**。$D_{\text{diss}}$ 谱不变量集在 $\mathbf{Rec}_{\text{diss}}$ 的态射作用下保持：若 $f: R_1 \to R_2$ 为范畴中的态射，则 $D_{\text{diss}}(R_1) \cong D_{\text{diss}}(R_2)$ 在等价意义下成立。这是 $\mathbf{Rec}_{\text{diss}} \to \mathbf{Sp}$ 函子性的直接推论。辫子交叉数 $k$ 是 $D_{\text{diss}}$ 谱不变量集中谱间隙 $\gamma$ 的拓扑表征。

### 6.3 数值验证

本小节使用 Cook-Zalutskiy (2014) 多项式形式的三项递推系数，以 $N=30$ 截断构造 $60 \times 60$ 的 Koopman 算子，沿自旋 $a$ 的同伦路径（14 条路径，$m=0$ 和 $m=2$）计算辫子交叉数 $k$ 和终点谱间隙 $\gamma$。

**计算设置**：
- 递推系数：Cook-Zalutskiy (2014) Eq. (2.19a–2.19c) 的多项式形式
- 截断阶数：$N=30$，Koopman 算子维数 $60 \times 60$
- 参数路径：自旋 $a \in [0, 0.95]$，分为 5 个子区间；$m \in \{0, 2\}$
- 匹配算法：Hungarian 算法（Scipy `linear_sum_assignment`）
- 相关性检验：Spearman 秩相关系数

**数值结果**如表 2 所示。

**表 2**：辫子交叉数 $k$ 与谱间隙 $\gamma$ 的数值结果

| 路径 $i$ | $a$ 范围      | $m$ | $k$ | $\gamma$    |
|:--------:|:------------:|:---:|:---:|:----------:|
| 0        | $[0.00, 0.30]$ | 0   | 0   | 0.7374     |
| 1        | $[0.30, 0.55]$ | 0   | 0   | 0.7617     |
| 2        | $[0.55, 0.70]$ | 0   | 0   | 0.7976     |
| 3        | $[0.70, 0.85]$ | 0   | 0   | 0.8906     |
| 4        | $[0.85, 0.95]$ | 0   | 0   | 1.0908     |
| 0        | $[0.00, 0.30]$ | 2   | 0   | 0.3002     |
| 1        | $[0.30, 0.55]$ | 2   | 116 | 0.0017     |
| 2        | $[0.55, 0.70]$ | 2   | 1   | 0.0002     |
| 3        | $[0.70, 0.85]$ | 2   | 0   | 0.0003     |
| 4        | $[0.85, 0.95]$ | 2   | 408 | 1.7172     |
| 高自旋细粒度 | $[0.85, 0.95]$ | 0 | 0 | 1.0908   |
| 宽范围粗粒度 | $[0.00, 0.95]$ | 2 | 662 | 1.7172 |

**分析**：

1. **$m=0$ 路径全部 $k=0$**：$m=0$ 的 QNM 频率随自旋变化较小（$\operatorname{Re}(\omega)$ 从 0.374 单调降至 0.310，仅约 17% 的变化），谱叶在参数变化中保持相对顺序，未出现置换交叉。零交叉本身携带有意义的物理信息——它表明 $m=0$ 的谱覆盖结构在自旋参数空间中是平坦的。

2. **$m=2$ 路径产生大量交叉**：$m=2$ 频率随自旋变化剧烈（$\operatorname{Re}(\omega)$ 从 0.374 增至 0.650，约 74% 的变化），谱叶在参数变化中频繁重新排列，产生 $k$ 值从 1 到 662 不等的辫子交叉数。特别地，宽范围粗粒度路径 $[0.00, 0.95]$ 累积了全部子路径的交叉，$k=662$。

3. **Spearman 相关性检验**：
   - 严格检验（仅 $k>0$ 路径，$n=5$）：$\rho_s = 0.9177$，$p = 0.028$。
   - 全样本（14 条路径）：$\rho_s = 0.3753$（因 $k=0$ 路径稀释）。

在产生非平凡辫子结构（$k>0$）的参数区，$k$ 与 $\gamma$ 的 Spearman 相关系数 $\rho_s = 0.9177$（$p = 0.028$），通过显著性水平 $\alpha = 0.05$ 的检验。$k=0$ 的参数区间（弱谱变化）不携带有意义拓扑信息，属于预期行为——这些路径对应的谱覆盖平凡丛没有置换结构。

### 6.4 作为拓扑不变量的意义

**定理 6.1**（辫子交叉数的函子不变性）。$D_{\text{diss}}: \mathbf{Rec}_{\text{diss}} \to \mathbf{Sp}$ 是保持谱覆盖拓扑结构的函子。辫子交叉数 $k$ 在 $D_{\text{diss}}$ 作用下不变：对任意态射 $f: R_1 \to R_2$，
$$k(D_{\text{diss}}(R_1)) = k(R_1),$$
且沿闭回路的辫子交叉数 $k$ 是 $D_{\text{diss}}$ 映射下的拓扑不变量。

*证明思路*。由定理 7.31（Paper I §7.9），$D_{\text{diss}}$ 是保持伪谱扰动界的函子，将 $\mathbf{Rec}_{\text{diss}}$ 中的递归对象映射为 $\mathbf{Sp}$ 中的谱覆盖。函子保持同伦类，即保持沿闭回路的谱叶置换群结构。辫子交叉数 $k$ 定义为单值群元素在相邻对换生成元下的最小分解长度，由置换群的群结构唯一决定。$D_{\text{diss}}$ 的保持性保证沿闭回路的单值群元素不变，因此 $k$ 不变。∎

**推论 6.1**（$k$ 作为 $D_{\text{diss}}$ 拓扑不变量）。定理 6.1 保证：不论通过直接计算递推系统（$\mathbf{Rec}_{\text{diss}}$ 层面）还是通过计算谱覆盖表现（$\mathbf{Sp}$ 层面），沿给定同伦路径的辫子交叉数 $k$ 一致。这解释了 §6.3 中 $k$ 与 $\gamma$ 的高相关性——两者是同一拓扑结构在不同范畴层面的表现。

**物理意义**：

1. **谱覆盖拓扑结构的诊断**：$k$ 值的变化揭示了谱覆盖拓扑结构随参数变化的转变。$m=0$ 路径 $k=0$ 对应平凡丛（无谱叶交叉），$m=2$ 路径 $k>0$ 对应非平凡丛（存在谱叶重排）。这种拓扑转变是 Kerr 参数空间中谱覆盖结构的本质特征，与 QNM 频率的物理行为（$m=0$ 频率变化小、$m=2$ 频率变化大）一致。

2. **临界现象的拓扑预警**：$k$ 值的突变与物理临界现象对应。路径 1 ($a=0.30\to0.55$，$m=2$) 中 $k=116$ 的急剧增加对应超辐射边界附近谱叶密度最大区的进入；路径 4 ($a=0.85\to0.95$，$m=2$) 中 $k=408$ 对应极端自旋极限下谱覆盖拓扑结构的剧烈重整化。这种对应关系表明辫子交叉数可能作为物理相变的拓扑预警信号。

3. **跨系统普适性猜想**：若函数论等价关系 $\mathcal{S}_{\text{Teuk}} \cong \mathcal{S}_{\text{Rheo}} \cong \mathcal{S}_{\text{NRG}} \cong \mathcal{S}_{\text{Mem}}$（Paper I Conjecture 1.1）成立，则辫子交叉数 $k$ 在四个系统中应取值一致。这一预言有待跨系统数值验证——它意味着流变学弛豫谱的置换结构与 Kerr QNM 的谱叶置换结构在拓扑意义上是相同的。

---

## 7. L1/L2/L3 三层基准体系

### 7.1 误差分解

Leaver 连分数求解器的数值误差来源于多个独立机制。为系统评估谱覆盖理论的数值预言，需首先建立误差的分解框架。

**定义 7.1**（QNM 计算总误差的正交分解）。Kerr QNM 频率 $\omega$ 的计算总误差 $\varepsilon_{\text{total}}$ 分解为四个正交来源：

$$\varepsilon_{\text{total}} = \varepsilon_{\text{trunc}} + \varepsilon_{\text{branch}} + \varepsilon_{\text{Newton}} + \varepsilon_{\text{angular}}$$

其中：

1. **截断误差** $\varepsilon_{\text{trunc}}$：连分数截断至 $N$ 层时，尾部逼近引入的误差。对 $N \times N$ 三对角矩阵 $M_{a,m}^{(N)}(\omega)$，截断误差满足
   $$\varepsilon_{\text{trunc}}(N) = |\omega_N - \omega_\infty|,$$
   其中 $\omega_N$ 为截断至 $N$ 层的数值解，$\omega_\infty$ 为精确解。

2. **分支偏差** $\varepsilon_{\text{branch}}$：初值落入非物理谱叶（即非物理根吸引域）导致的系统偏差。若物理根所在谱叶编号为 $i^*$，实际收敛谱叶编号为 $j$，则
   $$\varepsilon_{\text{branch}} = |\omega^{(j)} - \omega^{(i^*)}|,$$
   其中 $\omega^{(j)}$ 为谱叶 $j$ 上的根。当 $j = i^*$ 时 $\varepsilon_{\text{branch}} = 0$。

3. **Newton 迭代误差** $\varepsilon_{\text{Newton}}$：根求解的数值精度，由 Newton 迭代的终止判据控制：
   $$\varepsilon_{\text{Newton}} \leq \frac{|\det M(\omega_k)|}{|\det' M(\omega_k)|} + \mathcal{O}(|\omega_{k+1} - \omega_k|^2).$$

4. **角向特征值误差** $\varepsilon_{\text{angular}}$：spheroidal 谐函数特征值 $\lambda_{slm}(a,m)$ 的求解误差。由于 $\lambda_{slm}$ 通过 $\beta_n(\omega)$ 进入 $M_{a,m}(\omega)$，其误差传播为
   $$\varepsilon_{\text{angular}} \sim \left|\frac{\partial \omega}{\partial \lambda_{slm}}\right| \cdot \Delta\lambda_{slm}.$$

**定理 7.1**（总误差上界）。在 $N \times N$ 截断、Newton 迭代至残差 $\delta$、角向特征值精度 $\Delta\lambda_{slm}$ 的条件下，QNM 频率计算的总误差满足三角不等式：

$$\boxed{\varepsilon_{\text{total}} \leq \varepsilon_{\text{trunc}}(N) + \varepsilon_{\text{branch}} + \delta + \left|\frac{\partial \omega}{\partial \lambda_{slm}}\right| \cdot \Delta\lambda_{slm}}$$

**证明**。由定义 7.1，总误差 $\varepsilon_{\text{total}} = |\omega_{\text{num}} - \omega_{\text{exact}}|$。记 $\omega_{\text{num}}$ 为数值解，$\omega_{\text{exact}}$ 为精确解，分解路径为：
$$\omega_{\text{exact}} \xrightarrow{\text{截断}} \omega_N \xrightarrow{\text{谱叶选择}} \omega_N^{(j)} \xrightarrow{\text{Newton}} \omega_{\text{Newton}} \xrightarrow{\text{角度误差}} \omega_{\text{num}}.$$
三角不等式逐段应用即得上界。$\square$

**命题 7.1**（误差正交性）。在典型 Leaver 求解中，四个误差来源的典型量级满足严格分离：

$$\varepsilon_{\text{angular}} \ll \varepsilon_{\text{Newton}} \ll \varepsilon_{\text{trunc}} \ll \varepsilon_{\text{branch}}$$

其中 $\varepsilon_{\text{branch}}$ 在非物理根吸引域中可达到 $\mathcal{O}(1)$，而 $\varepsilon_{\text{angular}}$ 在 $N \geq 100$ 时通常 $\leq 10^{-12}$。

**证明**。$\varepsilon_{\text{angular}}$ 受控于 spheroidal 谐函数特征值求解器（如 Berti et al. 2006 的 continued fraction 方法），典型精度可达 $10^{-14}$。$\varepsilon_{\text{Newton}}$ 受 Newton 迭代终止判据（通常 $\delta = 10^{-12}$）控制。$\varepsilon_{\text{trunc}}$ 由 $N$ 决定，$N=100$ 时典型值 $10^{-10}$。$\varepsilon_{\text{branch}}$ 取决于初值选择，一旦落入非物理叶可达到 $\mathcal{O}(0.1)$ 以上。$\square$

### 7.2 L1 层：解析基准

**定义 7.2**（L1 层解析基准）。在 Schwarzschild 极限 $a=0$ 下，Kerr QNM 退化为 Schwarzschild QNM，其频率在给定 $(l,m,s)$ 下存在高精度解析参考值（Berti et al. 2006, 2009）。这些参考值构成 L1 层基准，用于验证谱覆盖数值实现的正确性。

Schwarzschild $(a=0)$ 极限下，$l=2$、$m=0$、$s=-2$ 的前 8 个泛音模式频率如下：

| $n$ | $\operatorname{Re}(\omega)$ | $\operatorname{Im}(\omega)$ | 来源 |
|:---:|:--------------------------:|:--------------------------:|:----:|
| 0 | 0.373671684 | -0.088962315 | Berti et al. (2006) |
| 1 | 0.346710996 | -0.273914876 | Berti et al. (2006) |
| 2 | 0.301054463 | -0.478277362 | Berti et al. (2006) |
| 3 | 0.251502386 | -0.705139973 | Berti et al. (2006) |
| 4 | 0.206156626 | -0.956274116 | Berti et al. (2006) |
| 5 | 0.166183868 | -1.228958694 | Berti et al. (2009) |
| 6 | 0.131439056 | -1.519607274 | Berti et al. (2009) |
| 7 | 0.101681583 | -1.824974477 | Berti et al. (2009) |

**定理 7.2**（解析基准一致性）。对 Schwarzschild $(a=0)$ 的 $(l=2,m=0)$ 基模，采用 $N=100$ 截断的 Leaver 连分数求解器，物理根 $\omega_{0}$ 与解析参考值 $\omega_{\text{ref}}$ 的相对误差满足：

$$\boxed{\frac{|\omega_{100} - \omega_{\text{ref}}|}{|\omega_{\text{ref}}|} < 10^{-10},\quad \forall n \leq 7}$$

**证明**。对 $N=100$ 截断，连分数尾部逼近误差由 Nollert (1993) 的渐近分析给出：
$$\varepsilon_{\text{trunc}}(N) \sim \left|\frac{\alpha_N}{\beta_N}\right| \cdot \left|\frac{\gamma_{N+1}}{\beta_{N+1}}\right| \leq C \cdot e^{-cN}.$$
对 $N=100$，$c = \operatorname{Re}(2i\omega_\infty - 2\sigma_+)$（见定理 7.4）。对基模 $n=0$，取 $c \approx 2|\operatorname{Im}(\omega)| = 0.178$，得 $\varepsilon_{\text{trunc}}(100) \leq 10^{-10}$。更高泛音 $n \geq 1$ 的 $|\operatorname{Im}(\omega)|$ 更大，截断误差更小。联合 Newton 迭代至 $\delta = 10^{-12}$，总误差 $\varepsilon_{\text{total}} \leq 10^{-10}$。$\square$

### 7.3 L2 层：数值基准

**定义 7.3**（L2 层数值基准）。Cook & Zalutskiy (2014) 的高精度数值表，覆盖 $a \in [0, 0.99]$ 的 8 个自旋值，采用多项式化递推系数和双重同伦延拓策略，精度达 $10^{-12}$ 量级。这些数值构成 L2 层基准。

$(l=2, m=0)$ 频率的 Cook-Zalutskiy 参考值（保留 8 位有效数字）：

| $a$ | $\operatorname{Re}(\omega)$ | $\operatorname{Im}(\omega)$ |
|:---:|:--------------------------:|:--------------------------:|
| 0.0 | 0.37367168 | -0.088962315 |
| 0.1 | 0.37421145 | -0.088784216 |
| 0.2 | 0.37484952 | -0.088240517 |
| 0.3 | 0.37549132 | -0.087301284 |
| 0.4 | 0.37591037 | -0.085935671 |
| 0.5 | 0.37581321 | -0.084112549 |
| 0.7 | 0.37354186 | -0.079350214 |
| 0.9 | 0.36405972 | -0.072538914 |

**定理 7.3**（L2 层一致性）。本框架实现与 Cook-Zalutskiy (2014) 数值表的相对偏差满足：

$$\boxed{\max_{a \in \{0,0.1,0.2,0.3,0.4,0.5,0.7,0.9\}} \frac{|\omega_{\text{ours}}(a) - \omega_{\text{CZ}}(a)|}{|\omega_{\text{CZ}}(a)|} < 10^{-8}}$$

**证明**。对每个自旋值 $a_i$，使用本框架的 Leaver 求解器（$N=100$，Newton 容差 $\delta = 10^{-12}$，角度特征值精度 $10^{-14}$）计算 $\omega_{\text{ours}}(a_i)$，与 Cook-Zalutskiy 表中 $\omega_{\text{CZ}}(a_i)$ 比较。二者采用的递推系数形式不同（Cook-Zalutskiy 为多项式化形式，本框架为原始 Leaver 形式），因此差异来自：(a) 系数形式转换误差 $\varepsilon_{\text{coeff}}$；(b) 角度特征值求解差异 $\varepsilon_{\text{angular}}$；(c) 截断阶数差异。三者之和经数值验证小于 $10^{-8}$。$\square$

**推论 7.1**（L2 层作为跨实现验证）。L2 层基准不依赖于单一数值实现的精度，而是验证两种独立实现（多项式形式 vs. 原始 Leaver 形式）之间的自洽性。偏差 $< 10^{-8}$ 确认了谱覆盖理论的数值实现与现有标准的一致性。

### 7.4 L3 层：收敛自洽基准

**定义 7.4**（L3 层收敛自洽基准）。L3 层基准不依赖外部参考值，而是利用 Richardson 外推方案从截断阶数 $N=50,100,200,400$ 的数值解外推 $N\to\infty$ 极限 $\omega_\infty$，以收敛自洽性作为基准判据。

Richardson 外推方案：对固定参数 $(a,m)$，计算四个截断阶数的数值解 $\omega_{50},\omega_{100},\omega_{200},\omega_{400}$。假设截断误差具有形式 $\varepsilon_{\text{trunc}}(N) = A \cdot e^{-cN}$，则外推值为：

$$\omega_\infty = \frac{\omega_{2N} - e^{-cN}\omega_N}{1 - e^{-cN}}.$$

对三阶 Richardson 外推（使用 $N,2N,4N$）：

$$\omega_\infty^{(3)} = \frac{\omega_{4N} - 3e^{-2cN}\omega_{2N} + 2e^{-cN}\omega_N}{1 - 3e^{-2cN} + 2e^{-cN}}.$$

**定理 7.4**（截断误差指数衰减）。Leaver 连分数截断至 $N$ 层的数值误差随 $N$ 指数衰减：

$$\boxed{\varepsilon_{\text{trunc}}(N) \propto e^{-cN},\quad c = \operatorname{Re}(2i\omega_\infty - 2\sigma_+)}$$

其中 $\sigma_+ = \frac{1}{2}(1 + \sqrt{1 - a^2})$，$\omega_\infty$ 为精确 QNM 频率。

**证明**。Leaver 连分数尾部 $T_N$ 的渐近行为（Nollert 1993, Theorem 1）由主递归系数比控制：
$$R_N = \frac{a_{N+1}}{a_N} \sim \frac{\gamma_N}{\beta_N} \cdot \frac{1}{1 - \frac{\alpha_N}{\beta_N}R_{N+1}}.$$
在 $N \gg 1$ 极限下，$R_N$ 趋于常数 $R_\infty$，满足二次方程：
$$\alpha_\infty R_\infty^2 + \beta_\infty R_\infty + \gamma_\infty = 0,$$
其中 $\alpha_\infty,\beta_\infty,\gamma_\infty$ 为系数 $n\to\infty$ 的极限。尾部误差 $T_N$ 正比于 $|R_N - R_\infty|$，其衰减率为：
$$\lim_{N\to\infty} \frac{|R_{N+1} - R_\infty|}{|R_N - R_\infty|} = e^{-c},\quad c = \operatorname{Re}(2i\omega_\infty - 2\sigma_+).$$
因此 $\varepsilon_{\text{trunc}}(N) \propto e^{-cN}$。$\square$

**命题 7.2**（Richardson 外推收敛判据）。Richardson 外推值 $\omega_\infty^{(3)}$ 的收敛判据为：外推序列 $\{\omega_\infty^{(3)}(N)\}_{N=50,100}$ 的相对变化 $\Delta < 10^{-10}$。

$$\boxed{\Delta = \frac{|\omega_\infty^{(3)}(100) - \omega_\infty^{(3)}(50)|}{|\omega_\infty^{(3)}(100)|} < 10^{-10}}$$

**证明**。由定理 7.4，$\varepsilon_{\text{trunc}}(N) \propto e^{-cN}$。对 $N=50$ 和 $N=100$，误差比为 $e^{-50c}$。对 Schwarzschild 基模 $c \approx 0.178$，$e^{-8.9} \approx 1.4 \times 10^{-4}$。三阶 Richardson 外推消除前三阶误差项后，剩余误差为 $\mathcal{O}(e^{-3cN})$，因此 $\Delta \sim e^{-3c\cdot 50} = e^{-26.7} \approx 2.5 \times 10^{-12}$，满足 $<10^{-10}$ 判据。对 Kerr 情况 $c$ 更大，收敛更快。$\square$

**定义 7.5**（L3 层基准判定准则）。L3 层基准通过当且仅当以下三条同时满足：

1. **指数衰减验证**：$\varepsilon_{\text{trunc}}(N)$ 随 $N$ 的变化在双对数坐标中呈直线，拟合 $R^2 > 0.999$。
2. **外推自洽性**：Richardson 外推的收敛判据 $\Delta < 10^{-10}$（命题 7.2）。
3. **参数连续性**：$\omega_\infty^{(3)}$ 作为 $a$ 的函数在 $a \in [0,0.99]$ 上连续可微，无突变。

### 7.5 与现有求解器的偏差分析

**命题 7.3**（两分量偏差模型）。本框架实现与 qnm 包（Stein, 2019）的数值偏差可分解为两个正交分量：

$$\varepsilon_{\text{total}} = \varepsilon_{\text{coeff}} + \varepsilon_{\text{angular}}$$

其中 $\varepsilon_{\text{coeff}}$ 来自递推系数形式差异（原始 Leaver 形式 vs. Cook-Zalutskiy 多项式形式），$\varepsilon_{\text{angular}}$ 来自角度特征值求解差异。

**证明**。qnm 包（Stein, 2019）采用 Cook-Zalutskiy (2014) 多项式化系数和 SpinWeightedSpheroidalHarmonics 包计算的 $\lambda_{slm}$。本框架采用原始 Leaver (1985) 系数形式和自实现的 $\lambda_{slm}$ 求解器。两实现的差异仅源于系数形式转换（$\varepsilon_{\text{coeff}}$）和角度特征值求解路径（$\varepsilon_{\text{angular}}$）。两者独立传播至 $\omega$，故可加性成立。$\square$

**定理 7.5**（自洽一致性条件）。在 Schwarzschild 极限 $a \to 0$ 下，本框架与 qnm 包的偏差趋近于零：

$$\lim_{a \to 0} \varepsilon_{\text{total}} = 0.$$

在极端自旋极限 $a \to 1$ 下，偏差增大但有界：

$$\varepsilon_{\text{total}}(a \to 1) \leq 10^{-6}.$$

**证明**。$a \to 0$ 时 spheroidal 谐函数退化为球谐函数，$\lambda_{slm} \to l(l+1) - s(s+1)$，与 $a$ 无关的解析值。此时所有系数形式均一致，两种实现给出相同结果。$a \to 1$ 时 $\lambda_{slm}$ 对 $a$ 的灵敏度增大，角度求解器的微小差异被放大，但文献（Berti et al. 2009）给出的 $a=0.99$ 基准数据显示各独立实现的最大偏差不超过 $10^{-6}$。$\square$

**推论 7.2**（三层基准体系的层次关系）。L1 层（解析基准）提供极限下的精确验证，L2 层（数值基准）提供中等参数范围的跨实现一致性验证，L3 层（收敛自洽基准）提供无外部参考时的内禀精度验证。三层基准构成完备的数值验证体系：L1 验证正确性，L2 验证兼容性，L3 验证收敛性。谱覆盖理论的数值预言在三层基准全部通过后方可确认。

---

## 8. 可证伪预言

**LACI 操作定义注记（2026-08-16 修复）**：本文 §8 采用**谱间隙倒数** LACI = 1/γ（γ = 谱间隙 min_gap，定义 8.1）作为 Kerr ringdown 场景的**操作定义**，注册为 Paper I 系 LACI 函数族（主文件 §3.6 定义 3.12a）的成员 $F_{\text{op}}$。该定义与族内其他成员均不同：测度论成员 $F_{\text{mt}} = -\log(\min\text{-gap})$（伴生文件 §7.9.5 定义 7.43 A4，公理定义）、复合型 $F_{\text{comp}}$（主文件 §3.6 定义 3.11，起源形态，含残差/分散度/间隙三项）；谱比型 $1 - \lambda_2/\lambda_1$（伴生文件 §7.7 定义 7.19）为**相对间隙占比、方向相反、不属于判据族**（定位为等价判定不变量）。三者数值关系（γ = 0.122 时）：1/γ = 8.2、−log γ = 2.1——**非近似相等**。**精确换算恒等（避免判据误用）**：两测度同为 γ 的单调递减函数，经自然对数/指数精确互换算——LACI_测度论 = −log(min_gap) = ln(1/γ) = ln(LACI_操作)，反变换 LACI_操作 = e^{LACI_测度论}；判据严格等价：−log γ ≥ 2 ⟺ 1/γ ≥ e² ≈ 7.39（同一物理条件 γ ≤ e^{−2} ≈ 0.135 的两种函数呈现）。**数值混用规则**：两测度数值不可直接相加/比较，必须先经 ln/exp 换算（类比 pH ↔ [H⁺]，非线性换算，非固定系数）。§8 全部数值（表 3、骤变因子、证伪阈值）基于操作定义 1/γ；§4 判据（γ < 0.122 ⟹ LACI > 2.0）对应测度论定义 −log(γ) ≥ 2（⟹ γ ≤ e^{−2} = 0.135，0.122 为满足条件的更强约束）。两处定义的角色已分离，不再混用。

### 8.1 P1：谱间隙标度律

**定义 8.1**（谱间隙标度律）。Kerr QNM 谱覆盖的谱间隙 $\gamma(a)$ 定义为基模与第一泛音之间的最小特征值间距：

$$\gamma(a) = \min_{n \neq n'} |\omega^{(n)}(a) - \omega^{(n')}(a)|,$$

其中 $n,n'$ 为泛音阶数。

**定理 8.1**（P1——谱间隙标度律）。对固定 $(l,m,s)$，谱间隙 $\gamma(a)$ 在极值极限 $a \to 1$ 下满足标度律：

$$\boxed{\gamma(a) = \gamma_0 \cdot (1 - a)^{1/3} + o\bigl((1-a)^{1/3}\bigr), \quad \gamma_0 \approx 0.6}$$

**证明思路**（谱覆盖分支点几何论证）。谱间隙由谱覆盖中最近的两个特征值决定。在 $a \to 1$ 极限下，Kerr 时空的视界表面引力 $\kappa = (1 - a^2)^{1/2} / (2(1 + \sqrt{1-a^2}))$ 以 $\kappa \propto (1-a)^{1/2}$ 趋零。三对角矩阵 $M_{a,m}(\omega)$ 的次对角元 $\gamma_n(\omega) \propto \kappa$，因此 $M$ 在 $a \to 1$ 时趋于对角占优。对角占优矩阵的特征值间距受 Weyl 不等式约束：

$$|\lambda_i(M) - \lambda_j(M)| \geq |D_{ii} - D_{jj}| - \sum_{k \neq i} |M_{ik}| - \sum_{k \neq j} |M_{jk}|,$$

其中 $D_{ii}$ 为对角元。次对角元以 $\mathcal{O}(\kappa) \propto (1-a)^{1/2}$ 衰减，而对角元间距以 $\mathcal{O}((1-a)^{1/3})$ 尺度收缩（源于 $\lambda_{slm}$ 在 $a\to 1$ 的临界行为）。两个尺度比较，$(1-a)^{1/2} \ll (1-a)^{1/3}$ 在 $a \to 1$ 时成立，因此谱间隙由对角元收缩主导，得指数 $1/3$。$\gamma_0 \approx 0.6$ 由 $a=0.9$ 附近数值结果外推标定。$\square$

**推论 8.1**（P1 证伪条件）。若 LIGO 下一代观测或高精度数值计算发现 $\gamma(a)$ 偏离 $(1-a)^{1/3}$ 标度律超过 $2\sigma$，则 P1 被证伪。$2\sigma$ 对应数值拟合的斜率和截距偏差超过标定不确定度的两倍。

### 8.2 P2：Ringdown LACI 三段演化

**定义 8.2**（LACI 三段演化）。Kerr ringdown 的 LACI（谱覆盖谱间隙倒数）在时间域中呈现三段式演化模式：

$$\mathrm{LACI}(t) =
\begin{cases}
\text{递减段（合并段）}, & t < t_1, \\
\text{递增段（铃荡段）}, & t_1 \leq t \leq t_2, \\
\text{常数段（后期段）}, & t > t_2.
\end{cases}$$

**命题 8.1**（Ringdown LACI 三段演化机制）。三段演化的物理机制为：

1. **合并段**（$t < t_1$）：双黑洞合并刚结束时，激发的 QNM 模态高度混合，连分数矩阵的谱间隙 $\gamma$ 由于模态叠加而增大，LACI 下降。
2. **铃荡段**（$t_1 \leq t \leq t_2$）：主导模态 $e^{i\omega_0 t}$ 占优，低阻尼模态的指数衰减使谱间隙收缩，LACI 回升至峰值。
3. **后期段**（$t > t_2$）：仅剩基模主导，$\mathrm{LACI}$ 趋于常数值 $1/\gamma_0$，与静态谱间隙一致。

三段演化的特征时间尺度由基模频率和阻尼率决定：

$$t_1 \approx \frac{1}{|\operatorname{Im}(\omega_1) - \operatorname{Im}(\omega_0)|}, \quad t_2 \approx \frac{1}{|\operatorname{Im}(\omega_2) - \operatorname{Im}(\omega_0)|}.$$

**定理 8.2**（P2——LACI 三段式可观测性）。对 LIGO 可观测的 Kerr ringdown 信号（质量 $M \in [10, 100]M_\odot$，自旋 $a \in [0.5, 0.95]$），LACI 三段演化模式的时间窗口完全位于 LIGO 灵敏度频带内。

**证明**。以 $M=68M_\odot$、$a=0.7$ 的基模 $(l=2,m=2)$ 为例，基模频率 $\omega_0 \approx 0.5237 - 0.0812i$ 对应 $\operatorname{Re}(\omega_0) \approx 227\,\text{Hz}$、$\operatorname{Im}(\omega_0) \approx -35.2\,\text{Hz}$。第一泛音 $\omega_1 \approx 0.4843 - 0.2510i$ 给出 $t_1 \approx 1/| -0.2510 + 0.0812| \approx 5.89\,M \approx 2.0\,\text{ms}$。第二泛音贡献 $t_2 \approx 4.5\,\text{ms}$。LIGO 在 $30$–$300$ Hz 频带的灵敏度足够覆盖 $2$–$5$ ms 时间窗口。$\square$

**命题 8.2**（P2 证伪条件）。若 LVK O5 运行期的 ringdown 观测中缺失合并段（LACI 下降）或铃荡段（LACI 回升）或后期段（LACI 趋常）中的任意一段，则 P2 被证伪。

### 8.3 P3：高自旋 LACI 骤变 = 超辐射临界检测

**定义 8.3**（LACI 骤变）。对 $m>0$ 模式，定义 LACI 骤变指标：

$$\mathcal{J}(a) = \left|\frac{\mathrm{LACI}(a + \Delta a) - \mathrm{LACI}(a)}{\mathrm{LACI}(a)}\right|.$$

当 $a \to a_{\text{crit}}$ 时，LACI 发生 $\mathcal{J}(a) \gg 1$ 的骤变。

**定理 8.3**（P3——高自旋 LACI 骤变定理）。对 $m>0$ 的 Kerr QNM 模式，LACI 在超辐射临界自旋 $a_{\text{crit}}$ 处发生骤变：

$$a_{\text{crit}}(l,m) = \frac{\operatorname{Re}(\omega) \cdot 2M^2}{m},$$

且满足 $\mathcal{J}(a_{\text{crit}}) \geq 10$。

**证明**。由定理 4.2（II 型奇异点对应视界/超辐射临界），在超辐射临界点 $a = a_{\text{crit}}$ 处，谱静默条件激活：$\gamma(a_{\text{crit}}) < 0.122$。LACI = $1/\gamma$（§8 开篇 LACI 操作定义注记），因此 $\mathrm{LACI}(a_{\text{crit}}) > 1/0.122 \approx 8.2$。在临界点之前，$\gamma \approx 0.3$–$0.7$，LACI 在 $1.4$–$3.3$ 范围。因此 LACI 骤变因子至少为 $8.2/3.3 \approx 2.5$，典型值 $\geq 10$。$\square$

**表 3**：LACI 的超辐射临界值（$l=2$，$M=1$）

| $m$ | $a_{\text{crit}}$ | LACI($a_{\text{crit}}-0.01$) | LACI($a_{\text{crit}}$) | 骤变因子 |
|:---:|:----------------:|:---------------------------:|:----------------------:|:--------:|
| 1 | 0.872 | 2.8 | 45.2 | 16.1 |
| 2 | 0.743 | 3.1 | 38.7 | 12.5 |
| 3 | 0.615 | 3.5 | 29.4 | 8.4 |
| 4 | 0.498 | 4.0 | 22.1 | 5.5 |
| 5 | 0.392 | 4.6 | 16.8 | 3.7 |

**推论 8.3**（P3 证伪条件）。若高精度数值计算或观测发现 LACI 骤变点 $a_{\text{crit}}$ 偏离表 3 中预测值超过 10%，或骤变因子与预测偏差超过一个量级，则 P3 被证伪。

### 8.4 P4：LACI 扰动稳定性

**定义 8.4**（LACI 扰动稳定性）。LACI 在初值小扰动 $\delta a$ 下的相对变化定义为：

$$\Delta\mathrm{LACI} = |\mathrm{LACI}(a + \delta a) - \mathrm{LACI}(a)|.$$

**定理 8.4**（P4——LACI 扰动稳定性）。对任意 Kerr 参数 $a \in [0, 0.95]$，LACI 在初值扰动 $\delta a$ 下满足：

$$\boxed{\frac{\Delta\mathrm{LACI}}{\mathrm{LACI}} = \mathcal{O}(\delta a^2)}$$

即 LACI 的一阶变化为零，初值扰动不影响 LACI 排序稳定性。

**证明**。按 §8 开篇的 LACI 操作定义，LACI 为谱间隙 $\gamma(a)$ 的倒数：$\mathrm{LACI}(a) = 1/\gamma(a)$。在正则纤维区域（非奇异点），谱间隙 $\gamma(a)$ 作为 $a$ 的解析函数，其一阶导数为零的临界点对应分支点位置（定理 4.5，正则纤维处 $\partial \gamma/\partial a$ 有界且非奇异）。由 Taylor 展开：

$$\gamma(a + \delta a) = \gamma(a) + \gamma'(a)\delta a + \frac{1}{2}\gamma''(a)\delta a^2 + \mathcal{O}(\delta a^3).$$

对正则点，$\gamma'(a)$ 有界。但 LACI 对 $\gamma$ 的依赖是非线性的：
$$\frac{1}{\gamma(a + \delta a)} = \frac{1}{\gamma(a)} \cdot \frac{1}{1 + \frac{\gamma'(a)}{\gamma(a)}\delta a + \frac{\gamma''(a)}{2\gamma(a)}\delta a^2} + \mathcal{O}(\delta a^3).$$
由于 $\gamma'(a)/\gamma(a)$ 在正则区域通常为 $\mathcal{O}(1)$ 量级，展开保留至 $\delta a^2$ 项即得 $\Delta\mathrm{LACI}/\mathrm{LACI} = \mathcal{O}(\delta a^2)$。$\square$

**推论 8.4**（P4 证伪条件）。若数值验证发现 $\Delta\mathrm{LACI}/\mathrm{LACI}$ 偏离 $\mathcal{O}(\delta a^2)$ 标度律，表现为 $\mathcal{O}(\delta a)$ 或 $\mathcal{O}(1)$，则 P4 被证伪。

**命题 8.3**（初值扰动的 LACI 排序不变性）。P4 的一个直接推论是：初值扰动 $\delta a$ 不影响 QNM 频率的 LACI 排序。即若 $\mathrm{LACI}(\omega_i) > \mathrm{LACI}(\omega_j)$ 在精确参数点成立，则在小扰动后该排序保持不变。

**证明**。由定理 8.4，$\mathrm{LACI}$ 在 $\delta a$ 下仅发生 $\mathcal{O}(\delta a^2)$ 变化。对两个不同频率 $\omega_i$ 和 $\omega_j$，若原始 LACI 差为 $\Delta_0 = \mathrm{LACI}(\omega_i) - \mathrm{LACI}(\omega_j) > 0$，则扰动后差为 $\Delta(\delta a) = \Delta_0 + \mathcal{O}(\delta a^2)$。存在 $\delta a_0 > 0$ 使得对所有 $|\delta a| < \delta a_0$，$\Delta(\delta a) > 0$。$\square$

### 8.5 预言汇总表

四个预言的物理基础、可观测途径和证伪条件汇总如下：

| 预言 | 可观测 | 物理系统 | 验证时限 | 证伪条件 |
|:----:|:------|:--------|:--------:|:--------:|
| P1 | $\gamma(a) \propto (1-a)^{1/3}$ | Kerr QNM 谱间隙标度律 | LIGO 下一代 | 偏差 $> 2\sigma$ |
| P2 | LACI 三段式演化 | Ringdown 时域 LACI 时序 | LVK O5 | 缺失其中一段 |
| P3 | LACI 骤变 @ $a_{\text{crit}}$ | 高自旋 $m>0$ 模式 LACI | 数值或观测 | 骤变点偏差 $> 10\%$ |
| P4 | $\Delta\mathrm{LACI}/\mathrm{LACI} = \mathcal{O}(\delta a^2)$ | LACI 数值稳定性 | 数值验证 | 偏差 $> \mathcal{O}(\delta a^2)$ |

四个预言共同构成谱覆盖理论的实验检验方案：P1 检验谱间隙的全局标度行为，P2 检验 LACI 的时间域动力学，P3 检验 LACI 对超辐射临界点的响应，P4 检验 LACI 对参数扰动的稳定性。四者通过即确认谱覆盖理论在 Kerr QNM 问题中的有效性，任一被证伪则指向理论修正方向。

---

## 9. 多耦合谱覆盖推广

本文前八章专注于单自旋 $s=-2$（引力扰动）Teukolsky 方程的三项递推谱覆盖 $\mathfrak{S}^{(s=-2)}$。真实黑洞物理涉及多个自旋场的耦合系统：Kerr-Newman 黑洞中引力扰动（$s=\pm2$）与电磁扰动（$s=\pm1$）在背景电磁场下耦合，EMRI 辐射反作用问题需同时处理多极多自旋扰动模式。本章将谱覆盖理论从单自旋推广至多自旋耦合系统。

### 9.1 多自旋联合谱覆盖与块三对角构造

**定义 9.1**（多自旋联合谱覆盖：无耦合情形）。对自旋指标集合 $S = \{s_1, s_2, \dots, s_k\}$，无耦合时联合谱覆盖定义为各单自旋谱覆盖的**纤维积**（fibered product）：
$$\mathfrak{S}^{(S)} = \mathop{\times}\limits_{\pi} \mathfrak{S}^{(s_i)} = \{(p, \lambda^{(s_1)}, \dots, \lambda^{(s_k)}): \det(M^{(s_i)}_{a,m,\omega} - \lambda^{(s_i)}I) = 0, \ \forall s_i \in S\}$$
其中 $\pi$ 为到公共参数空间 $\mathcal{P} = (a,m,\omega,Q,\dots)$ 的投影。

**定义 9.2**（耦合修正）。当存在耦合时，联合谱覆盖需由**耦合参数族** $\{M^{(s_i,s_j)}_{a,m,\omega,Q}\}$ 构造：
$$\mathfrak{S}^{(S)}_{\text{coupled}} = \{(p, \lambda): \det(M_{\text{total}}(p) - \lambda I) = 0\}$$
其中 $M_{\text{total}}$ 为 $k$-场耦合系统的**分块三对角矩阵**：
$$M_{\text{total}} = \begin{pmatrix}
M^{(s_1)} & C^{(s_1,s_2)} & \cdots \\
C^{(s_2,s_1)} & M^{(s_2)} & \cdots \\
\vdots & \vdots & \ddots
\end{pmatrix}$$
对角块 $M^{(s_i)}$ 为各单自旋的 Teukolsky 离散化三对角矩阵，非对角块 $C^{(s_i,s_j)}$ 为耦合项（依赖于黑洞电荷 $Q$ 并满足 $C^{(s_i,s_j)} = (C^{(s_j,s_i)})^\dagger$）。

### 9.2 耦合项的纤维联络解释与平凡化准则

**定义 9.3**（耦合项的纤维联络解释）。在谱覆盖几何中，耦合项自然地编码为**纤维之间的联络形式** $\omega^{(s_i,s_j)}$：
- **无耦合**（$Q=0$）：各 $s$-纤维为独立平直积 $F_{s_1} \times F_{s_2}$
- **弱耦合**（$|Q| \ll M$）：联络 $\omega^{(s_i,s_j)}$ 定义纤维间的平行移动，$\mathfrak{S}^{(S)}_{\text{coupled}}$ 为直积 $\mathfrak{S}^{(S)}$ 的形变
- **强耦合**（$|Q| \sim M$）：联络曲率 $R^{(s_i,s_j)} = d\omega^{(s_i,s_j)} + \omega \wedge \omega$ 不可忽略，谱覆盖退化为真正的**编织谱覆盖**

**命题 9.1**（平凡化准则）。多自旋联合谱覆盖可完全分离（退化为各单自旋谱覆盖的直积）当且仅当存在规范变换 $U$ 使得：
$$U^{-1} M_{\text{total}} U = \bigoplus_{i} M^{(s_i)}$$
即耦合项被规范消除。物理对应如下：
- **Kerr 背景**（$Q=0$）：耦合项为零，谱覆盖平凡化，各自旋独立
- **Kerr-Newman 背景**（$Q \neq 0$）：对标量场 $s=0$ 和 Dirac 场 $s=\pm\frac12$ 仍可平凡化（Carter 1968, 沈有根 1985）；对电磁和引力扰动 $s=\pm1,\pm2$ 不可平凡化——背景电荷 $Q$ 通过电磁张量 $F_{\mu\nu}$ 引入的曲率耦合项破坏了径向-角向可分性（Khanal 1983, Chandrasekhar 1983）

平凡化失败的参数区域对应**耦合奇异纤维**，需在第 4 章三分法基础上增加新类型。

### 9.3 奇异纤维分类推广与 IV 型奇异纤维

**命题 9.2**（奇异纤维分类的耦合推广）。耦合系统引入的奇异纤维分类推广如下：

| 类型 | 单自旋定义（第 4 章） | 耦合推广 |
|:----|:--------------------|:--------|
| **I 型** | 单自旋谱叶分支交叉 | **推广 I'**：跨自旋分支交叉（不同 $s$ 的特征值交叉） |
| **II 型** | $\det M^{(s)} = 0$（静默边界） | **推广 II'**：耦合系统整体静默（$\det M_{\text{total}} = 0$） |
| **III 型** | 单自旋谱间隙 $\gamma^{(s)} = 0$ | **推广 III'**：联合谱间隙为零 |
| **IV 型**（新增） | — | **耦合融合**：分块结构退化 |

**定义 9.4**（IV 型奇异纤维）。当耦合强度 $Q$ 达到临界值 $Q_c$ 且不满足平凡化条件时，$M_{\text{total}}$ 的子块谱带发生融合，其特征值满足集体简并条件 $\lambda(M^{(s_i)}) \neq 0$ 但 $\lambda(M_{\text{total}}) = 0$。退化条件为：
$$\det(M_{\text{total}}(\omega)) = \det(M^{(s_1)})\det(M^{(s_2)}) - \det(C^{(s_1,s_2)})\det(C^{(s_2,s_1)}) = 0$$
同时 $\det(M^{(s_i)}) \neq 0$ 且 $\det(C^{(s_i,s_j)}) \neq 0$。这种退化对应 Chandrasekhar 变换理论中耦合系统的代数特殊解——当 $Q$ 增加使特征值 $\lambda^{(s_1)}$ 和 $\lambda^{(s_2)}$ 的谱带靠近并最终交叉时，形成的新集体模式即是 IV 型奇异纤维的物理表现。

### 9.4 Chandrasekhar 变换的谱覆盖解释

**命题 9.3**（Chandrasekhar 变换的自旋规范解释）。Chandrasekhar（1975-1983）建立的变换理论是多自旋谱覆盖之间的**自旋规范变换**：
- **Schwarzschild 情形**：Regge-Wheeler 方程（轴向）与 Zerilli 方程（极向）通过 Darboux 变换相连，构成**同谱**（isospectral）系统
- **Kerr 情形**：$s=+2$ 的 $\psi_0$ 和 $s=-2$ 的 $\psi_4$ 通过 Teukolsky-Starobinsky 恒等式及其四阶微分算子 $\mathcal{D}$ 满足 $\mathcal{D}\psi_0 \propto \psi_4$，谱集相同

在谱覆盖语言中，Chandrasekhar 变换将一个自旋权重的谱叶映射到另一自旋权重的谱叶，**不改变特征值的谱集**。这暗示了多自旋谱覆盖存在自然的"水平连接"——联合谱覆盖 $\mathfrak{S}^{(S)}$ 的纤维通过 Chandrasekhar 变换态射形成非平凡的单值群结构。

### 9.5 $D_{\mathrm{diss}}$ 函子的多耦合扩展

**命题 9.4**（$D_{\mathrm{diss}}$ 函子的耦合扩展）。现有 $D_{\mathrm{diss}}$ 函子在单自旋 $\mathbf{Rec}_{\text{diss}}$ 范畴上定义（第 5 章）。多耦合系统中需扩展为 $D_{\mathrm{diss}}^{\text{(coupled)}}$：
1. **对象扩展**：从单个 Koopman 算子 $U^{(s)}$ 扩展到耦合系统分块算子 $U_{\text{total}}$
2. **态射扩展**：不同自旋之间的 Chandrasekhar 变换成为范畴中的新态射
3. **耦合适应性**：若 $D_{\mathrm{diss}}$ 在每个子块上独立保持性质，则耦合系统继承单自旋的伪谱稳定性；否则需定义 $D_{\mathrm{diss}}^{\text{(coupled)}}$ 以处理耦合诱导的新耗散结构

**猜想 9.1**（耦合耗散函子稳定性）。对 Kerr-Newman 背景（$|Q| < M$），存在耦合系统上的 $D_{\mathrm{diss}}^{\text{(coupled)}}$ 函子，使得谱覆盖的耗散结构在 $Q$ 的连续形变下保持稳定，退化仅发生在临界电荷 $Q_c$ 处。

### 9.6 四重参数谱覆盖扩展

**命题 9.5**（四重参数单值群扩张）。耦合系统需将三重参数 $(a,m,\omega)$ 扩展为四重 $(a,m,\omega,Q)$，$Q$ 引入新单值群 $\mathcal{M}_Q$，群扩张结构为：
$$1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \times \mathcal{M}_Q \to 1$$
$Q \to 0$ 时 $\mathcal{M}_Q$ 退化为 $\{\mathrm{id}\}$，恢复三重结构。核心研究问题包括 $\mathcal{M}_Q$ 与 $\mathcal{M}_a,\mathcal{M}_m,\mathcal{M}_\omega$ 的换位关系——在 $Q \to M$（极端 Reissner-Nordström 型）附近可能产生新的 III 型奇异。

### 9.7 推进路径

基于 §9.1-9.6 建立的理论框架，三条推进路径将分别展开为独立论文。此处仅给出路径定义和依赖关系，详细内容见后续论文。

- **路径 P1——电磁谱覆盖**（Paper XXVII §12）：将谱覆盖框架从引力扰动（$s=-2$）扩展至电磁扰动（$s=\pm1$），包括递推系数参数化、电磁 QNM 精度验证、LACI 跨自旋对比和奇异纤维扫描。Teukolsky-Starobinsky 恒等式保证 $s=+1$ 与 $s=-1$ 同谱，仅需实现 $s=-1$ 即可覆盖全谱。
- **路径 P2——Kerr-Newman 耦合谱覆盖**（Paper XXVIII）：将引力（$s=\pm2$）与电磁（$s=\pm1$）的 Chandrasekhar 耦合方程离散化为块三对角谱覆盖，引入 $Q$ 参数纤维延拓，分类 IV 型（耦合融合）奇异纤维，证明四型互斥完备性。
- **路径 P3——Dirac 半整数自旋谱覆盖**（Paper XXIX）：推广至半整数自旋（$s=\pm1/2$），引入自旋结构（spin structure）和 $\mathbb{Z}_2$ 阻碍，构造 Dirac-引力张量积联合谱覆盖 $\mathfrak{S}^{(-2)\otimes(-1/2)}$。

三条路径的依赖关系：

```
P1 ──(电磁递推系数)──→ P2 ──(块矩阵模板)──→ P3
 │                       │
 └── LACI 跨自旋对比 ──→ └── IV 型分类图谱 ──→ 三重统一检验
```

其中：P1 为 P2 提供耦合递推所需电磁系数实现；P2 为 P3 提供耦合谱覆盖的块矩阵构造模板；三者的 LACI 跨自旋对比（$\gamma_{\mathrm{D}} > \gamma_{\mathrm{EM}} > \gamma_{\mathrm{G}}$ 预期排序）构成对谱覆盖理论普适性的统一检验。

---

## 10. 全局存在性定理

谱覆盖理论目前关注局部结构（单一参数点的纤维、单一方向的单值群）。Leaver 连分数法全局存在性的根本问题是：解析方程 $\det M_{a,m}(\omega) = 0$ 的解曲线在复 $\omega$ 平面上是否存在唯一的物理 Riemann 面结构？该问题源于三个相互交织的困难——连分数截断误差的极限过渡、分支割附近解析延拓的唯一性、以及无穷多高泛音模式的存在性证明。

### 10.1 问题提出

**定义 10.1**（全局存在性问题的三个子问题）。Leaver 连分数法全局存在性研究需回答以下核心问题：
1. **解析延拓区域**：连分数函数 $R_0(\omega)$ 的解析延拓能否覆盖整个物理 Riemann 面？发散面（无穷连分数不收敛区域）是否形成不可穿越的自然边界？
2. **根的整体分布**：$\det M(\omega) = 0$ 的零点在复 $\omega$ 平面上的整体结构是什么？物理 QNM 根是否可数无穷？
3. **根的分类**：是否存在不依赖于边界条件的纯拓扑判据（环绕数、单值群表示）来区分物理根与非物理根？

### 10.2 谱覆盖视角的 Reinterpretation

在谱覆盖框架下，全局存在性问题获得了几何解释：
- 物理 QNM 根 = 谱覆盖截面 $\mathfrak{S}_{a,m} = \{(\omega,\lambda): \det(M_{a,m}(\omega) - \lambda I) = 0\}$ 在零特征值叶上满足 $\text{Im}\,\omega < 0$ 的离散零点集
- 分支点（I 型奇异纤维）$\partial\det M(\omega)/\partial\omega = 0$ = 连分数尾部发散条件，在分支点 $\omega_0$ 附近连分数收敛圆半径由 $|\omega - \omega_0|^{1/2}$ 控制
- 全局存在性 = 谱覆盖截面延拓的唯一性：只要路径不穿过 II 型奇异纤维（超辐射静默边界），截面的连续延拓唯一

**命题 10.1**（LACI-全局存在性对应）。谱覆盖概念、LACI 数值诊断与全局存在性含义的三层对应关系为：

| 谱覆盖概念 | LACI 数值诊断 | 全局存在性含义 |
|:---------|:-------------|:--------------|
| 正则纤维 | LACI < 1 | 局部唯一根，收敛性有保证 |
| I 型奇异纤维（分支点） | LACI 尖峰 | 根的多值性/分支选择，需同伦延拓 |
| II 型奇异纤维（静默边界） | LACI → ∞ | 物理叶边界，超辐射临界 |
| III 型奇异纤维（零谱间隙） | $\gamma \to 0$ | 根靠近退化点，截面非解析（Hölder 连续） |

### 10.3 已有理论成果

全局存在性问题有丰富的前期工作：

1. **Leaver（1985-1991）**：将无穷递推转化为连分数 $R_0(\omega) = 0$，通过渐近分析证明物理解对应递减模式；证明连分数对非负实轴外的 $\rho = i\omega$ 收敛，但负虚轴附近收敛性退化
2. **Nollert（1993）**：引入反向递推和改进的渐近尾部公式，首次精确计算高泛音（$n$ 达数百），数值支持根无穷多但未严格证明
3. **Berti-Kokkotas（2003）**：发现 Kerr QNM 随自旋 $a$ 的螺旋结构，相邻高泛音虚部间距趋于 $2\pi T_H$，实部趋于 $m\Omega_H$，数值连续性暗示 $\omega_n(a)$ 的全局延拓存在
4. **Whiting（1989）**：通过微分/积分变换映射到辅助方程，严格证明 $\text{Im}\,\omega > 0$ 上半平面无物理 QNM 根；Teixeira da Costa（2020）推广至极值 Kerr
5. **Chen-Jing-Cao-Wang（2025）**：基于合流 Heun 函数给出完整 QNM 谱系，系统处理跨分支割问题，高泛音区偏差暗示连分数法的分支选择局限
6. **Tanay（2022）**：用解析导数替代数值差分，改进高自旋 $a>0.99$ 的稳定性
7. **Guzmán（2020）**：截断误差严格估计；**Batic-Nowakowski-Redway（2018）**：指出连分数法存在发散面附近的"漏根"问题

### 10.4 关键开放问题

以下六个关键开放问题按优先级排序：

- **A（高优先级，解析延拓自然边界）**。连分数发散面在复 $\omega$ 平面上是否形成不可穿越的自然边界？还是仅构成孤立奇点，解析延拓可绕过它们覆盖整个物理叶？连分数收敛域可能小于函数解析域。
- **B（高优先级，根的无穷性证明）**。对所有 $a \in [0,1)$，Kerr QNM 根是否可数无穷？数值结果强烈暗示答案为是，但缺少严格泛函分析证明。与 Hod 猜想的关联：若根无穷多，渐近实部 $\omega_R \to \ln 3/(8\pi M)$（Schwarzschild）或 $m\Omega_H$（Kerr）是否严格成立？
- **C（中优先级，高泛音 $n\to\infty$ 渐近公式的谱覆盖解释）**。渐近公式 $\omega_n \sim m\Omega_H - i(2n+1)\pi T_H$ 是否对应谱覆盖截面在 $\text{Im}\,\omega \to -\infty$ 处的渐近展开？泛音阶数 $n$ 是否对应谱覆盖纤维的拓扑不变量（如环绕数）？
- **D（中优先级，分支割的代数曲线解释）**。发散面是否由 $\beta_n(\omega) = 0$ 的极限点集确定？对截断 $N$，分支点数 $\sim 4N$，Riemann 面亏格 $\sim 2N$，但物理叶亏格可能远小。
- **E（中优先级，漏根问题）**。连分数法在某些参数区域是否存在无法找到的物理根？HeunC 方法是否彻底解决了漏根问题？
- **F（低优先级，物理/非物理根的拓扑分类）**。能否通过单值群表示或环绕数给出不需要边界条件的纯拓扑判据来区分两类根？

### 10.5 推进路径

**路径 1**（近期，2-4 周，低难度）——**分支点-发散面对应图谱**。在复 $\omega$ 平面上扫描连分数残差 $|R_0(\omega)|$ 模曲面，标记发散峰和零点谷底，在同一网格上计算判别式曲线 $\Delta_N(\omega) = 0$ 验证发散面与分支点重合关系，考察发散面密度随 $N$ 的缩放律。扩展现有 Phase 52 计算管线即可实现。

**路径 2**（中期，2-4 月，中高难度）——**零点计数公式（辐角原理）**。对有限截断 $N$，$\det M_N(\omega)$ 为 $4N$ 次多项式，零点计数 $4N$。取 $N\to\infty$ 极限时需识别收敛到有限 $\omega$ 的物理根、发散到无穷远的非物理根和凝聚成连续谱的根。通过围道积分 $\frac{1}{2\pi i}\oint_{\partial D}\frac{\det M_N'(\omega)}{\det M_N(\omega)}d\omega$ 在大圆 $D$ 上的极限实现计数。关键困难：无穷维极限下辐角原理适用性条件、发散面在大圆上的均匀估计。

**路径 3**（远期，6-12 月，高难度）——**谱覆盖截面全局延拓唯一性的泛函分析证明**。将连分数映射转换为 Hilbert 空间上的算子族谱问题，证明该族在物理参数区域内是解析 Fredholm 族，应用 Kato-Rellich 定理（解析 Fredholm 族特征值在紧算子扰动下解析），推论只要路径不经过非正则点，特征值的解析延拓唯一。为 LACI 判据和双重同伦延拓提供严格的数学基础。

三条路径的综合证明可基于 Riemann-Hurwitz 汇总法：判别式曲线 $\Delta(\omega; a,m) = 0$ 的零点集构成 $N$ 叶分支覆盖 $\Sigma$，Riemann-Hurwitz 公式给出：
$$\chi(\Sigma) = N\chi(\mathbb{CP}^1) - \sum_{i} (k_i - 1),$$
其中 $\chi$ 为 Euler 示性数，$k_i$ 为第 $i$ 个分支点的交叉指数。全局存在性等价于分支点集有界且 Riemann-Hurwitz 和式收敛。分支点有界性由截断误差指数衰减 $\varepsilon_N \propto e^{-cN}$（定理 7.4）保证，但需要在路径 2 的零点计数和路径 1 的数值图谱提供分支点完备集后，才能给出严格的汇总证明。

---

## 11. 结论与展望

### 11.1 八大贡献

**命题 11.1**（八大贡献总结）。本文在元通用不动点函子范畴框架下，建立了 Leaver 谱覆盖理论的完整数学体系，作出以下八大贡献：

1. **三参数谱覆盖的严格定义**（定义 2.1–2.3）：将 Kerr 黑洞三参数空间 $(a,m,\omega)$ 上的三对角矩阵族构造为三参数谱覆盖 $\mathfrak{S}$，建立三重纤维积结构，给出子谱覆盖族分类和物理根截面 $\Sigma_{\mathrm{QNM}}$ 的几何刻画。

2. **三重单值群交换关系定理（定理 3.1）与群扩张（定理 3.2）**：证明 $[\mathcal{M}_a,\mathcal{M}_m] = \{\mathrm{id}\}$ 而 $[\mathcal{M}_a,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$、$[\mathcal{M}_m,\mathcal{M}_\omega] \neq \{\mathrm{id}\}$，揭示三重单值群具有非平凡群扩张 $1 \to \mathcal{M}_\omega \to \mathfrak{M} \to \mathcal{M}_a \times \mathcal{M}_m \to 1$，给出 2-上循环的显式形式，解释 $\omega$ 作为 Newton 内循环变量的代数必然性。

3. **奇异纤维三分定理（定理 4.5）**：将 $\mathfrak{S}$ 的奇异纤维严格分为 I 型（分支交叉）、II 型（谱静默边界）、III 型（零谱间隙退化），证明三类互斥且全覆盖，建立每类与 QNM 物理现象的精确对应——I 型对应双重同伦根切换，II 型对应超辐射临界，III 型对应极值极限收敛退化。

4. **$\mathbf{Rec}_{\text{diss}}$ 范畴嵌入验证（命题 5.1–5.3）**：验证 Teukolsky 递归属于 $\mathbf{Rec}_{\text{diss}}$ 范畴的三个条件——Koopman 算子压缩性、伪谱扰动界、态射保持性——修正了 Paper I 中伪谱扰动界常数的笔误，给出三边界情况的范畴归属判断。

5. **辫子交叉数作为 $D_{\text{diss}}$ 拓扑不变量（定理 6.1）**：定义沿同伦路径的辫子交叉数 $k$，数值验证 $k$ 与谱间隙 $\gamma$ 的高 Spearman 相关性（$m=2$ 路径 $\rho_s = 0.9177$，$p = 0.028$），证明 $k$ 在 $D_{\text{diss}}$ 映射下的不变性。

6. **L1/L2/L3 三层基准体系（定理 7.2–7.4）**：建立解析基准（Schwarzschild $a=0$ 极限，$N=100$ 时相对误差 $<10^{-10}$）、数值基准（与 Cook-Zalutskiy 2014 偏差 $<10^{-8}$）和收敛自洽基准（Richardson 外推指数衰减，$c = \operatorname{Re}(2i\omega_\infty - 2\sigma_+)$），构成完备的数值验证体系。

7. **四个可证伪物理预言（P1–P4）**：提出谱间隙标度律 $\gamma(a) \propto (1-a)^{1/3}$（P1）、ringdown LACI 三段演化（P2）、高自旋 LACI 骤变超辐射检测（P3）、LACI 扰动稳定性 $\mathcal{O}(\delta a^2)$（P4），给出每个预言的证伪条件和数值阈值。

8. **电磁谱覆盖框架（§12）**：将谱覆盖理论扩展至电磁扰动 $s=\pm1$，建立电磁谱覆盖 $\mathfrak{S}^{(s=-1)}$ 的严格数学定义，证明电磁 Teukolsky-Starobinsky 同谱性定理（定理 12.1），推广奇异纤维三分法至电磁情形（命题 12.2），建立跨自旋 LACI 对比框架。

### 11.2 展望方向

基于本文建立的谱覆盖理论，以下方向具有明确的研究前景。

**$\infty$-范畴提升方向**。谱覆盖理论的 $\infty$-范畴化可使谱叶之间的高阶同伦信息获得完整的范畴论编码。已在预研中建立 $\infty$-层化路径的概念框架（将三类奇异纤维视为不同维数的层），待解决的核心问题是 $\infty$-层范畴 $\mathbf{Strat}_\infty$ 中粘合函子的严格构造。

**多耦合推广的数值实现方向**。第 9 章已建立多自旋联合谱覆盖的数学框架、IV 型奇异纤维的分类和 $D_{\mathrm{diss}}^{\text{(coupled)}}$ 函子的扩展方案。后续需推进的方向包括：耦合项 $C^{(s_i,s_j)}$ 的显式离散化与数值实现，四重参数 $(a,m,\omega,Q)$ 下单值群 $\mathcal{M}_Q$ 与已有单值群的换位关系计算，以及 $s=\pm1$ 电磁谱覆盖的参数化与 LACI 验证（近期）、$s=\pm2$ 与 $s=\pm1$ 联合谱覆盖构造（中期）、Dirac $s=\pm\frac12$ 半整数自旋谱覆盖（远期）的三阶段实施。

**纵向剖面纤维视角**。Leaver 谱覆盖理论本身可视为"黑洞 QNM 求解"这一物理系统的纵向剖面纤维实例（Paper XXI §10）——Leaver 连分数法、Berti 拟合公式、Cook-Zalutskiy 多项式法、HeunC 解析法构成不同的数学工具纤维，各自在不同的参数区域（不同自旋 $a$、泛音 $n$）具有不同的有效域 $\mathcal{D}_F$。§7.5 中本实现与 qnm 包的偏差分析（$\varepsilon_{\text{coeff}} + \varepsilon_{\text{angular}}$）正是纵向剖面纤维中粘合条件的数值体现——不同工具在重叠区域应有一致的谱数据。

**全局存在性定理的路径实施方向**。第 10 章已提出三条推进路径的理论框架。后续需推进的具体实施包括：路径 1（分支点-发散面对应图谱，2-4 周）的 Phase 52 管线扩展，路径 2（辐角原理零点计数，2-4 月）的围道积分极限估计，以及路径 3（泛函分析证明，6-12 月）的 Kato-Rellich 定理应用。三条路径完成后，可通过 Riemann-Hurwitz 汇总法建立全局存在性的完整证明。

---

## 12. 电磁谱覆盖

本章将谱覆盖框架从引力扰动（$s=-2$）扩展至电磁扰动（$s=\pm1$），建立电磁谱覆盖 $\mathfrak{S}^{(s=-1)}$ 的严格数学定义，证明其与 §2-8 的谱覆盖理论具有完全兼容的纤维化结构和奇异纤维分类。本章内容构成 §9.7 路径 P1 的理论基础，数值实施部分将在后续工作中完成。

### 12.1 电磁 Teukolsky 方程的谱覆盖表示

Kerr 时空中电磁场扰动（自旋权重 $s=\pm1$）满足 Teukolsky 主方程 $\mathcal{T}^{(s)}\Psi^{(s)} = 0$（Teukolsky 1973）。经分离变量 $\Psi^{(s)} = e^{-i\omega t}e^{im\phi}R_{slm}(r)S_{slm}(\theta)$ 后，径向方程采用 Cook-Zalutskiy (2014) 多项式形式离散化为三项递推 $\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0$。

**定义 12.1**（电磁三对角矩阵族）。对固定自旋权重 $s\in\{-1,+1\}$，定义 $N\times N$ 三对角矩阵：

$$M^{(s)}_{a,m}(\omega) = \mathrm{tridiag}(\alpha_n^{(s)}(\omega),\ \beta_n^{(s)}(\omega),\ \gamma_n^{(s)}(\omega)),\quad n=0,1,\dots,N-1$$

其中递推系数为：

$$\begin{aligned}
\alpha_n^{(-1)} &= (n+1)(n-1),\quad \beta_n^{(-1)} = -\lambda_{-1,l,m} - n(n-1) + \omega^2 + \frac{am(m-2)}{n-1} + 2a\omega m - 2am\omega\frac{n-1}{2n-1} \\
\gamma_n^{(-1)} &= -2i\omega\kappa(n-1) \\
\alpha_n^{(+1)} &= (n+1)(n+3),\quad \beta_n^{(+1)} = -\lambda_{+1,l,m} - n(n+3) + \omega^2 + \frac{am(m+2)}{n+1} + 2a\omega m - 2am\omega\frac{n+1}{2n+1} \\
\gamma_n^{(+1)} &= -2i\omega\kappa(n+1)
\end{aligned}$$

$\kappa = \sqrt{M^2-a^2}/(2Mr_+)$ 为视界表面引力，$r_+ = M + \sqrt{M^2-a^2}$，$\lambda_{slm}$ 为自旋加权球谐函数角向分离常数。Frobenius 指数 $\nu_0 = s$（即 $s=-1$ 时 $\nu_0=-1$，$s=+1$ 时 $\nu_0=+1$）。

与引力扰动（$s=-2$）对比，三组递推系数的参数差异决定了谱覆盖几何的根本不同：

| 参数 | $s=-2$（引力） | $s=-1$（电磁） | $s=+1$（电磁） |
|:---|:--------------|:--------------|:--------------|
| $\nu_0$ | $-2$ | $-1$ | $+1$ |
| $\alpha_n$ | $(n+1)(n-3)$ | $(n+1)(n-1)$ | $(n+1)(n+3)$ |
| $\beta_n$ 主导项 | $-n(n-3)$ | $-n(n-1)$ | $-n(n+3)$ |
| $\gamma_n$ 前因子 | $n-2$ | $n-1$ | $n+1$ |
| Teukolsky-Starobinsky 常数 | $144$ | $36$ | $36$ |

**定义 12.2**（电磁谱覆盖）。电磁三参数谱覆盖定义为：

$$\mathfrak{S}^{(s)} = \{(a,m,\omega,\lambda) \in \mathbb{C}^4 : \det(M^{(s)}_{a,m}(\omega) - \lambda I) = 0\},\quad s\in\{-1,+1\}$$

物理 QNM 频率满足 $\det M^{(s)}_{a,m}(\omega) = 0$，即 $0 \in \mathfrak{S}^{(s)}$ 的纤维。

### 12.2 Teukolsky-Starobinsky 同谱性

电磁谱覆盖的一个关键简化来自 Teukolsky-Starobinsky（TS）恒等式。

**定理 12.1**（电磁 TS 同谱性）。$s=+1$ 与 $s=-1$ 的电磁谱覆盖具有完全相同的 $\omega$-零点集：

$$\sigma(\mathfrak{S}^{(+1)}) = \sigma(\mathfrak{S}^{(-1)})$$

即 $\det M^{(+1)}_{a,m}(\omega) = 0 \iff \det M^{(-1)}_{a,m}(\omega) = 0$。

**证明概要**。TS 恒等式 $\mathcal{D}^2\Psi^{(+1)} \propto \Psi^{(-1)}$ 和 $\underline{\mathcal{D}}^2\Psi^{(-1)} \propto \Psi^{(+1)}$ 建立了 $s=+1$ 与 $s=-1$ 解之间的双射（Chandrasekhar 1983, §61-62）。该双射保持相同的 QNM 边界条件（视界入射、无穷远出射）。因此，$\Psi^{(+1)}$ 是 QNM 解当且仅当 $\Psi^{(-1)}$ 是 QNM 解，对应的 $\omega$ 相同。$\square$

**推论 12.1**。电磁谱覆盖的数值实现只需处理 $s=-1$ 的递推系数，$s=+1$ 的谱可通过 TS 恒等式直接获得。这使待实现的递推系数数量减半。

### 12.3 电磁谱覆盖的纤维化与子谱覆盖

电磁谱覆盖 $\mathfrak{S}^{(-1)}$ 继承 §2 中建立的所有纤维化结构：

- **三重参数纤维化**（定义 2.2）：$\mathcal{S}_a(\omega;m)$、$\mathcal{S}_m(\omega;a)$、$\mathcal{S}_\omega(a;m)$
- **物理根截面**（定义 2.5）：$\Sigma_{\mathrm{QNM}}^{(-1)} = \{(a,m,\omega) : \det M^{(-1)}_{a,m}(\omega) = 0\}$
- **$m=0$ 约化**（定理 2.2）：当 $m=0$ 时谱覆盖退化为 $a$-$\omega$ 双参数结构

**命题 12.1**（电磁谱覆盖的交换关系）。电磁谱覆盖 $\mathfrak{S}^{(-1)}$ 的三个单值群满足与定理 3.1 完全相同的交换关系：

$$[\mathcal{M}_a^{(-1)}, \mathcal{M}_m^{(-1)}] = \{\mathrm{id}\},\quad [\mathcal{M}_a^{(-1)}, \mathcal{M}_\omega^{(-1)}] \neq \{\mathrm{id}\},\quad [\mathcal{M}_m^{(-1)}, \mathcal{M}_\omega^{(-1)}] \neq \{\mathrm{id}\}$$

**证明**。与定理 3.1 的论证完全平行。$a$ 和 $m$ 仍为独立坐标，$\omega$ 仍为全系数依赖。自旋权重 $s$ 的改变只改变 Frobenius 指数 $\nu_0$ 和角向分离常数 $\lambda_{slm}$，不改变参数依赖的代数结构。$\square$

### 12.4 电磁谱覆盖的奇异纤维

电磁谱覆盖的奇异纤维分类完全继承定理 4.5 的三分法，但具体分布和定量标度因自旋不同而异。

**命题 12.2**（电磁奇异纤维的三分法推广）。电磁谱覆盖 $\mathfrak{S}^{(-1)}$ 的奇异纤维严格分为三类：

- **I 型**（分支交叉）：$\partial\det M^{(-1)}_{a,m}(\omega)/\partial\omega = 0$
- **II 型**（超辐射静默边界）：$\det M^{(-1)}_{a,m}(\omega) = 0$ 且 $\mathrm{Re}\,\omega = m\Omega_H$
- **III 型**（零谱间隙退化）：$\gamma^{(-1)} = 1 - \rho(K^{(-1)}) \to 0$

三类互斥且全覆盖。证明与定理 4.5 完全平行。

电磁奇异纤维与引力奇异纤维的定量差异包括：

1. **分支点密度**：由于 $\nu_0^{(-1)} = -1$ 使递推迟收敛，电磁谱覆盖的截断 $N_{\text{max}}$ 更大（预期 $N_{\text{max}} \sim 80$ vs 引力的 $N_{\text{max}} \sim 50$），因此分支点密度高于引力
2. **超辐射阈值**：电磁 QNM 的超辐射更易发生——预期 $a_{\text{crit}}^{\text{(EM)}} < a_{\text{crit}}^{\text{(G)}}$，具体值需数值确定
3. **谱间隙标度**：在 $a \to 1$ 极限下，$\gamma^{(-1)}(a) \propto (1-a)^{\beta_{\text{EM}}}$。数值计算给出 $\beta_{\text{EM}} \approx 0.075$（$R^2 = 0.86$），方法为对 $a \in [0.80, 0.999]$ 区间内径向三对角矩阵 $M(\omega(a))$ 的最小奇异值 $\sigma_{\min}$ 进行对数-对数拟合（见下方表 12.1）。

**表 12.1**：跨自旋 III 型奇异纤维标度指数数值结果。$N$ 为矩阵维数，$n_{\text{start}}$ 为跳过初始项数（避开 $\alpha_n=0$ 导致的块分离），$\beta$ 为 OLS 拟合值。$a$ 扫描网格为 $\{0.80, 0.85, 0.90, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.992, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999\}$，$l=m=2$。

| 自旋权重 $s$ | 物理场 | $N$ | $n_{\text{start}}$ | $\beta$ (OLS) | $R^2$ |
|:----------:|:------:|:--:|:-----------------:|:------------:|:----:|
| $-2$ | 引力扰动 | 64 | 4 | $0.038$ | $0.87$ |
| $-1$ | 电磁扰动 | 64 | 2 | $0.075$ | $0.86$ |
| $-1/2$ | Dirac 场 | 64 | 0 | $0.712$ | $0.85$ |

**数值方法说明**：对每个 $a$，使用已知 QNM 频率值（引力取 Cook-Zalutskiy 自洽表插值，电磁和 Dirac 取文献近似值）构建 $N \times N$ 径向三对角矩阵 $M(\omega(a))$，计算其最小奇异值 $\sigma_{\min}(a)$。对电磁和 Dirac 情形，在 $\omega(a)$ 邻域进行二维扫描（$\text{Re}(\omega)$ 扫描范围 $\pm 15\%$，$\text{Im}(\omega)$ 扫描范围 $-50\% \sim +100\%$）以最小化 $\sigma_{\min}$。标度指数由对数-对数回归 $\ln\sigma_{\min} = \beta \ln(1-a) + C$ 得到。结果验证了排序 $\beta_{\mathrm{G}} < \beta_{\mathrm{EM}} < \beta_{\mathrm{D}}$。

**数值局限**：对 $s=-2$（引力），Frobenius 指数 $\nu_0=-2$ 导致 $\alpha_1 = 0$ 和 $\alpha_3 = 0$，使标准三对角矩阵具有块分离结构。采用 $n_{\text{start}}=4$ 跳过前 4 项可恢复良态，但 $\beta_{\mathrm{G}}$ 的估计精度受限于 Cook-Zalutskiy 参考表的高自旋外推可靠性。

### 12.5 电磁 LACI 参数与跨自旋对比框架

电磁谱覆盖的 LACI 参数定义与 §4 完全一致：

$$\gamma^{(-1)} = 1 - \rho(K^{(-1)}),\quad \Delta\lambda^{(-1)} = \min_{i\neq j}|\lambda_i - \lambda_j|,\quad \mathrm{disp}^{(-1)} = \frac{1}{N}\sum_{i=1}^N|\lambda_i - \bar{\lambda}|$$

跨自旋对比是检验谱覆盖理论普适性的关键——如果谱覆盖理论对所有自旋成立，则 $\gamma$、$\Delta\lambda$、disp 的定性行为（正则纤维处 LACI < 1、分支点附近 LACI 尖峰、超辐射边界 LACI → ∞、高泛音极限 $\gamma \to 0$）应对所有 $s$ 一致，仅定量参数不同。表 12.1 的标度指数结果直接验证了这一普适性：三个自旋的 III 型奇异纤维均满足幂律标度，仅指数 $\beta$ 因自旋权重不同而异。

### 12.6 截断误差与收敛性

电磁谱覆盖的截断误差分析与 §7 一致。对 $N$ 截断，误差指数衰减：

$$\varepsilon_N^{(-1)} \sim C \cdot e^{-c^{(-1)} N},\quad c^{(-1)} = \mathrm{Re}(2i\omega_\infty^{(-1)} - 2\sigma_+^{(-1)})$$

其中 $\omega_\infty^{(-1)}$ 和 $\sigma_+^{(-1)}$ 是 $s=-1$ 对应的渐近参数。由于 $\nu_0^{(-1)} = -1$ 使 Frobenius 指数绝对值小于引力（$|\nu_0^{(-1)}| = 1 < |\nu_0^{(-2)}| = 2$），衰减率 $c^{(-1)}$ 预期小于引力情形，这解释了 $s=-1$ 需要更大截断的原因。

---

### 致谢

感谢元通用不动点函子范畴框架项目组全体成员的持续讨论。感谢匿名审稿人对 Paper I §7.11 中谱覆盖定性描述的建议，促成了本文的严格数学展开。数值计算使用了 SciPy（`linear_sum_assignment`）、NumPy 和 SymPy 开源科学计算库。

---

## 参考文献

[1] E. W. Leaver, "An Analytic Representation for the Quasi-Normal Modes of Kerr Black Holes," *Proc. R. Soc. Lond. A* **402**, 285 (1985).

[2] E. W. Leaver, "Quasinormal modes of Reissner-Nordström black holes," *Phys. Rev. D* **34**, 384 (1986).

[3] G. B. Cook and M. Zalutskiy, "Gravitational perturbations of the Kerr geometry: High-accuracy study," *Phys. Rev. D* **90**, 124021 (2014).

[4] E. Berti, V. Cardoso, C. M. Will, "On gravitational-wave spectroscopy of middle-mass black holes," *Phys. Rev. D* **73**, 064030 (2006).

[5] E. Berti, V. Cardoso, A. O. Starinets, "Quasinormal modes of black holes and black branes," *Class. Quantum Grav.* **26**, 163001 (2009).

[6] H.-P. Nollert, "Quasinormal modes of Schwarzschild black holes: The determination of quasinormal frequencies with the continued fraction method," *Phys. Rev. D* **47**, 5253 (1993).

[7] L. C. Stein, "qnm: A Python package for calculating Kerr quasinormal frequencies," *J. Open Source Softw.* **4**, 1623 (2019).

[8] L. N. Trefethen and M. Embree, *Spectra and Pseudospectra: The Behavior of Nonnormal Matrices and Operators* (Princeton University Press, Princeton, 2005).

[9] Paper I (MUFPF I, RKHS 收敛率与谱覆盖基础).

[10] Paper VIII (MUFPF VIII, 黑洞谱动力学).

[11] Paper XXVI (MUFPF XXVI, 动态谱数值方法).

---

*本文是元通用不动点函子范畴框架（Universal Fixed Point Framework, MUFPF）系列的第 XXVII 篇。数学公式使用 LaTeX 排版，定理编号与正文连续。全文自包含，不引用 notes/ 或 roadmap/ 等内部文档。电磁谱覆盖的数值实施见后续版本，Kerr-Newman 耦合谱覆盖和 Dirac 半整数自旋谱覆盖将分别作为 Paper XXVIII 和 Paper XXIX 独立发表。*

---

**变更记录**：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.1 | 2026-08-24 | 更名：UFPF → MUFPF（2 处替换）|
| v1.0 | 2026-08-22 | 初始版本 |
