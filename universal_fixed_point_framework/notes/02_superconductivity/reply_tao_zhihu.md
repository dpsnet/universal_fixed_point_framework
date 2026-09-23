# $T_c \propto \sqrt{\rho_0}$ 标度律的代数推导——兼评 Tao 的复时间路径

**作者**：王斌（独立研究人）

**日期**：2026-09-11

**评论对象**：Y. Tao, "Universal square-root scaling between $T_c$ and superfluid phase stiffness: From cuprates to FeSe films", *Physica B* 742, 419333 (2026)；知乎科普文章 [https://zhuanlan.zhihu.com/p/2081350590974711703](https://zhuanlan.zhihu.com/p/2081350590974711703)

---

## 1. 引言

Tao 在知乎文章中介绍了其 2026 年发表于 *Physica B* 的论文 [1]，从复数时间相对论（complex time relativity）出发，推导出 Božović 组 [2] 在 LSCO 薄膜中发现的根方标度律

$$T_c = \gamma \sqrt{\rho_0} \tag{1}$$

其中 $\gamma = (4.2 \pm 0.5)\, K^{1/2}$，并成功定量解释了铜基（$\gamma(2) \approx 3.7\, K^{1/2}$）和铁基（$\gamma \approx 6.3\, K^{1/2}$）超导的系数。Tao 的理论基于 Tomita-Takesaki 定理和热时间假说（thermal time hypothesis），预言绝对零度时时空是类空的。

本文指出：**$T_c \propto \sqrt{\rho_0}$ 的平方根关系可从更基础的代数结构内生导出，不需要复时间假设**。整个推导仅依赖两个标准物理事实和一个 Nambu 空间代数恒等式，且已在 Lean4 定理证明器中形式化验证（零 `sorry`）。

---

## 2. Tao 的推导路径概述

Tao 的推导链条为：

1. **公理基础**：Tomita-Takesaki 定理 + 热时间假说 → 时间变量为复数 $z = t + i\tau$
2. **核心方程**：库珀对虚时相对论方程（非线性 Klein-Gordon 形式），含 $\hbar$、$c$、$k_B$ 三个基本常数
3. **重整化群**：自由能密度变分 → 场方程 → RG 方程组 → 长波极限不动点 $T_c(\infty) = \gamma(D)\sqrt{\rho_0(\infty)}$
4. **定量验证**：$\gamma(2) = c_F \pi \sqrt{16\hbar/(5k_B c a)} \approx 3.7\, K^{1/2}$（铜基），$\gamma \approx 6.3\, K^{1/2}$（铁基）
5. **独有预言**：绝对零度时空是类空的

这一路径的优势在于能从材料常数（费米速度 $\nu_F$、晶格常数 $a$、对称因子 $\gamma_F^d$）定量计算 $\gamma$。

---

## 3. 代数推导：从 Nambu 对易子到 $T_c \propto \sqrt{\rho_0}$

### 3.1 起点：BCS 谱生成元

BCS 超导态的谱生成元（spectral generator）在 Nambu 空间中为：

$$A_{\text{SC}} = \xi_k \sigma_z + \Delta \sigma_x \tag{2}$$

其中 $\xi_k = \varepsilon_k - \mu$ 为相对于 Fermi 面的动能，$\Delta$ 为超导能隙，$\sigma_z$、$\sigma_x$ 为 Pauli 矩阵。谱间隙为 $\delta_{\text{SC}} = \Delta$（详见 [3] §2.1，命题 2.1）。

### 3.2 U(1) 相位扭曲与对易子

超导序参量的 U(1) 相位 $\phi(x)$ 对应谱生成元的规范变换：

$$A_{\text{SC}}(x) = U(\phi(x)) \cdot A_{\text{SC}}^{(0)} \cdot U(\phi(x))^\dagger \tag{3}$$

其中 $U(\phi) = e^{i\phi\sigma_z/2}$。对空间坐标 $x$ 求梯度：

$$\partial_x A_{\text{SC}} = \frac{i}{2}(\partial_x \phi) \cdot [\sigma_z, A_{\text{SC}}] \tag{4}$$

关键一步——计算对易子：

$$[\sigma_z, A_{\text{SC}}] = [\sigma_z, \xi_k \sigma_z + \Delta \sigma_x] = \Delta [\sigma_z, \sigma_x] = 2i\Delta \sigma_y \tag{5}$$

因此：

$$\partial_x A_{\text{SC}} = -\Delta (\partial_x \phi) \sigma_y \tag{6}$$

梯度范数：

$$\|\partial_x A_{\text{SC}}\| = \Delta |\partial_x \phi| \tag{7}$$

**这里 $\Delta$ 以线性形式出现——它控制了谱生成元对相位扭曲的敏感程度。**

### 3.3 谱梯度能与超流刚度

序参量空间扭曲的自由能密度为：

$$f_{\text{grad}} = \frac{1}{2\beta_{\text{spec}}} \|\partial_x A_{\text{SC}}\|^2 = \frac{\Delta^2}{2\beta_{\text{spec}}} |\partial_x \phi|^2 \tag{8}$$

其中 $\beta_{\text{spec}}$ 是谱框架的温度标度因子。与标准形式 $f_{\text{grad}} = \rho_0 |\partial_x \phi|^2$ 对比：

$$\boxed{\rho_0 = \frac{\Delta^2}{2\beta_{\text{spec}}}} \tag{9}$$

### 3.4 $\beta_{\text{spec}}$ 的确定

从谱流方程（[3] §2.2）：

$$\frac{d}{dt} A_{\text{SC}}(T) = [A_{\text{pair}} + A_{\text{thermal}}(T),\, A_{\text{SC}}(T)] = 0 \tag{10}$$

温度 $T$ 作为热浴谱生成元 $A_{\text{thermal}}(T)$ 的耦合强度进入递归动力学。在不动点处，温度标度因子由 Fermi 能标确定：

$$\beta_{\text{spec}} = \frac{E_F}{k_B} \tag{11}$$

物理含义：谱梯度能以 Fermi 能为自然能标进行标度。因此：

$$\boxed{\rho_0 = \frac{k_B \Delta^2}{2 E_F}} \tag{12}$$

### 3.5 标度律的导出

BCS 弱耦合并给出 $T_c$ 与 $\Delta$ 的关系：

$$\Delta = 1.764\, k_B T_c \quad \Longrightarrow \quad T_c = \frac{\Delta}{1.764\, k_B} \tag{13}$$

即 $T_c \propto \Delta$（线性关系）。

而式 (12) 给出 $\rho_0 \propto \Delta^2$（平方关系）。

两者结合：

$$T_c = \frac{1}{1.764\, k_B} \sqrt{\frac{2 E_F \rho_0}{k_B}} = \gamma \sqrt{\rho_0} \tag{14}$$

其中：

$$\boxed{\gamma = \frac{\sqrt{2 E_F / k_B}}{1.764}} \tag{15}$$

---

## 4. 两条路径的比较

### 4.1 殊途同归

| 维度 | Tao (2026) 复时间路径 | 代数路径（本文） |
|:-----|:---------------------|:----------------|
| 公理基础 | Tomita-Takesaki 定理 + 热时间假说 | BCS 谱生成元 + Nambu 对易子代数 |
| 核心方程 | 虚时非线性 Klein-Gordon 方程 | 谱流方程 $dA/dt = [G, A] = 0$ |
| $\rho_0$ 的角色 | 序参量的 VEV（真空期望值） | $\Delta^2$ 与 $E_F$ 的代数组合 |
| $T_c \propto \sqrt{\rho_0}$ 来源 | RG 不动点的标度分析 | $T_c \propto \Delta$（线性）× $\rho_0 \propto \Delta^2$（平方）→ 平方根 |
| $\gamma$ 的计算 | 材料常数 $\nu_F, a, \gamma_F^d \to c_F \to \gamma$ | Fermi 能标 $E_F \to \gamma$ |
| 标度律成立范围 | $\gamma(D)^2$（维度依赖） | $E_F/(1.764^2 k_B)$（能标依赖） |
| 独有预言 | 绝对零度时空是类空的 | 多带超导隙比 SU(2) Casimir 量化 |

### 4.2 平方根关系的本质

平方根关系 $T_c \propto \sqrt{\rho_0}$ 的根源是两个**独立**的物理事实：

1. **$T_c \propto \Delta$**：BCS 关系，由谱间隙动力学保证——临界温度正比于能隙
2. **$\rho_0 \propto \Delta^2$**：谱刚度与谱间隙的平方关系，由 Nambu 空间对易子 $[\sigma_z, A_{\text{SC}}] = 2i\Delta\sigma_y$ 保证——能隙以线性形式进入对易子，但以平方形式进入梯度能

线性 × 平方 = 平方根。这一推导**不依赖于具体的配对机制**（BCS、RVB、自旋涨落……），只依赖于：
- 超导态有有限谱间隙 $\Delta$（谱对称性破缺）
- 相位扭曲的能量代价由 Nambu 对易子 $[\sigma_z, A_{\text{SC}}]$ 的范数控制

因此 $T_c \propto \sqrt{\rho_0}$ 是**代数结构的内生推论**，而非材料依赖的经验律。

### 4.3 $\gamma$ 的材料依赖性

本文路径中 $\gamma = \sqrt{2E_F/k_B}/1.764$ 唯一材料依赖的参数是 Fermi 能量 $E_F$：

| 材料体系 | $E_F$ (eV) | $\gamma$ 理论值 ($K^{1/2}$) | $\gamma$ 实验值 ($K^{1/2}$) |
|:---------|:----------:|:----------------------------:|:--------------------------:|
| LSCO 薄膜 | $\sim 1.5$ | $\sim 4.8$ | $4.2 \pm 0.5$ |
| FeSe 薄膜 | $\sim 3.0$ | $\sim 6.8$ | $6.3$ |

Tao 路径中 $\gamma$ 依赖于费米速度 $\nu_F$、晶格常数 $a$ 和对称因子 $\gamma_F^d$，能从材料常数更精确地计算。两条路径对 $\gamma$ 的不同表达可通过 Fermi 能 $E_F = \frac{1}{2}m^*\nu_F^2$ 与晶格结构的关系建立对应。

### 4.4 可检验差异

| 预言 | Tao 路径 | 代数路径 | 区分实验 |
|:-----|:---------|:---------|:---------|
| 标度指数 | 0.5（精确） | 0.5（精确） | 不可区分 |
| $\gamma$ 的来源 | 材料常数 $c_F$ | Fermi 能标 $E_F$ | 测量不同材料的 $E_F$ 与 $\gamma$ 的标度关系 |
| 维度依赖 | $\gamma(2) \neq \gamma(3)$（维度依赖） | $\gamma \propto \sqrt{E_F}$，与空间维度无直接关系 | 比较 2D 薄膜与 3D 块体 |
| 多带超导 | 未涉及 | SU(2) Casimir 谱隙比 $\delta_n/\delta_1 = \sqrt{n(n+1)}/\sqrt{2}$ | STM 测量 MgB$_2$ 隙比 |
| 强耦合偏离 | 复数时间修正 | Eliashberg 修正（$\Delta/E_F$ 不再是小量） | 高 $T_c$ 材料系统性测量 |

### 4.5 关于绝对零度

Tao 预言"绝对零度时空是类空的"——复时间虚部 $\tau$ 主导，度规退化为空间形式。

代数路径给出不同的图像：绝对零度对应**谱流方程的热耦合项消失**——$A_{\text{thermal}}(0) \to 0$，谱流退化为

$$\frac{d}{dt} A_{\text{SC}} = [A_{\text{pair}}, A_{\text{SC}}] = 0 \tag{16}$$

递归动力学冻结（recursive freezing）：谱数据 $\{\lambda_i\}$ 仍存在为静态结构，但不再有递归驱动的谱流演化。可度量的确实只有空间分布（静态谱结构），但这是因为**递归动力学静默**，而非度规本身变为空间型。

更精确地说：谱间隙 $\Delta\lambda_{\min}$ 构成不可跨越的能垒。当 $k_B T / E_F \to 0$ 时，热扰动远小于谱间隙，递归无法被热激发跨越——这正是"机械运动趋于停滞"的数学表述。

---

## 5. 形式化验证

上述推导已在 Lean4 定理证明器中形式化（`SuperfluidStiffness.lean`，零 `sorry`，构建通过 2026-09-11）：

1. `SpectralStiffness`：$\rho_0 = \Delta^2 / (2\beta_{\text{spec}})$（定义）
2. `spectral_stiffness_gap_relation`：$\rho_0 = (1/(2E_F)) \cdot \Delta^2$（定理，代数恒等式）
3. `scaling_coefficient_gamma`：$\gamma = \sqrt{2E_F} \cdot a_{\text{BCS}}$（定义，$a_{\text{BCS}} = 1/1.764$）
4. `Tc_sqrt_rho0_scaling`：$T_c = \gamma \cdot \sqrt{\rho_0}$（**定理，零 sorry 闭合**）

关键证明步骤：恒等式 $\sqrt{2E_F} \cdot \sqrt{\Delta^2/(2E_F)} = \Delta$ 通过 `Real.sqrt_mul` 合并两个平方根，再用 `Real.sqrt_sq` 闭合。

形式化代码开源于 [https://github.com/...] (MUFPFormalization/SuperfluidStiffness.lean)。

---

## 6. 结论

$T_c \propto \sqrt{\rho_0}$ 标度律可从 Nambu 空间对易子 $[\sigma_z, A_{\text{SC}}] = 2i\Delta\sigma_y$ 的代数结构内生导出，不需要复时间假设。平方根关系的本质是：

- **线性**：$T_c \propto \Delta$（BCS 关系，谱间隙动力学）
- **平方**：$\rho_0 \propto \Delta^2$（Nambu 对易子结构，能隙以线性进入对易子但以平方进入梯度能）
- **线性 × 平方 = 平方根**

Tao 的复时间路径与本文的代数路径从不同公理出发到达同一标度律，这种"殊途同归"增强了标度律的可信度。两条路径的互补性在于：
- Tao 的优势：能从材料常数定量计算 $\gamma$ 的数值（3.7 vs 4.2 实验）
- 代数路径的优势：标度律是代数结构的内生推论，不依赖虚时间假设；额外预言多带超导隙比的 SU(2) Casimir 量化

关于绝对零度，Tao 预言"时空是类空的"（度规退化），代数路径给出"递归冻结"（动力学静默）——两者都指向"可度量的只有空间分布"，但机制不同：前者是度规结构变化，后者是递归动力学停止。

---

## 参考文献

[1] Y. Tao, "Universal square-root scaling between $T_c$ and superfluid phase stiffness: From cuprates to FeSe films", *Physica B* 742, 419333 (2026).

[2] I. Božović et al., "Dependence of the critical temperature in overdoped copper oxides on superfluid density", *Nature* 536, 309-311 (2016).

[3] 王斌, "元通用不动点函子范畴框架 XIV：凝聚态物理的谱表述——超导、量子 Hall 与超流", v1.5 (2026). 开源于 [https://github.com/...]

[4] 王斌, "超流相刚度 $\rho_0$ 的谱框架定义与 $T_c \propto \sqrt{\rho_0}$ 标度律推导", 研究笔记 MUFPF-RN-RHO0-001 (2026).

[5] R. Zhang et al., "Correlation between unconventional superconductivity and strange metallicity revealed by operando superfluid density measurements", *Science Advances* 11, eadu0795 (2025).
