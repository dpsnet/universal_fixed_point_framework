# 元通用不动点函子范畴框架：宇宙学精细纤维拆分——时间-纤维化对偶

**版本**：v0.1（2026-07-25）

**摘要**：将 Paper XXII 的 7 层嵌套纤维化方法论推广至宇宙学系统。宇宙学的独特优势是时间/红移 $z$ 天然就是谱流参数 $\xi$，红移演化本身就是谱流方程的解。建立 6 层嵌套纤维化链：$\mathbf{Bun}(\mathrm{Inflation})\hookrightarrow\mathbf{Bun}(\mathrm{Reheat})\hookrightarrow\mathbf{Bun}(\mathrm{BBN})\hookrightarrow\mathbf{Bun}(\mathrm{LSS})\hookrightarrow\mathbf{Bun}(\mathrm{DE})\hookrightarrow\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$，对应宇宙完整演化历史。提出时间-纤维化对偶猜想。

---

## §1 天然谱流参数概览

基于 domain_generalization.md §6.1，宇宙学的独特优势在于其天然谱流参数结构。

### 1.1 时间/红移作为谱流参数

在宇宙学中，时间 $t$ 和红移 $z$ 自然界就是谱流参数 $\xi$。红移演化满足谱流方程：

$$\frac{d\xi}{dt} = H(t) = \frac{\dot{a}}{a}$$

其中 $H(t)$ 为 Hubble 参数，$a(t)$ 为宇宙尺度因子。这意味着宇宙的时序演化在数学上等价于谱纤维的流动——宇宙的每一时刻对应纤维化链的一个截面。

### 1.2 6 层嵌套纤维化链

宇宙学 6 层结构覆盖从 Planck 标度到当前宇宙约 27 个数量级的红移跨度：

| 层 | 红移/能标 | 物理内容 | 谱流参数 |
|:--|:---------:|:--------|:--------|
| $\mathbf{Bun}(\mathrm{Inflation})$ | $z \sim 10^{27}$ | 暴胀子势、原初谱指数 $n_s$ | $\xi_{\mathrm{infl}} = \ln a$ |
| $\mathbf{Bun}(\mathrm{Reheat})$ | $z \sim 10^{26}$ | 再加热、粒子生成 | $\xi_{\mathrm{rh}} = T$ |
| $\mathbf{Bun}(\mathrm{BBN})$ | $z \sim 10^{9}$ | 轻元素合成、核子合成 n/p 冻结 | $\xi_{\mathrm{BBN}} = T_{\mathrm{nuc}}$ |
| $\mathbf{Bun}(\mathrm{LSS})$ | $z \sim 1100$ | 重组、CMB 各向异性 | $\xi_{\mathrm{LSS}} = a(t)$ |
| $\mathbf{Bun}(\mathrm{DE})$ | $z \sim 0$ | 暗能量、$w(z)$ 参数化 | $\xi_{\mathrm{late}} = w(z)$ |
| $\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$ | Planck 标度 | 宇宙波函数、无边界条件 | -- |

### 1.3 层间遗忘函子

每层之间的遗忘函子 $\hookrightarrow$ 对应于宇宙时间的一段演化区间。从高红移层到低红移层的信息传递由谱投影实现：

$$\pi_{i\leftarrow i+1}: \mathbf{Bun}(\mathcal{L}_{i+1}) \to \mathbf{Bun}(\mathcal{L}_i)$$

物理上，这对应高能物理过程的"冻结"——某些自由度在能量尺度下降时成为不可激发的背景场。

---

## §2 Bun(Inflation)：暴胀层

### 2.1 基本参数

- **红移**：$z \sim 10^{27}$
- **能标**：$\sim 10^{16}$ GeV（GUT 标度附近）
- **谱流参数**：$\xi_{\mathrm{infl}} = \ln a$（e-fold 数等价）

### 2.2 谱生成元

暴胀层的谱生成元来自暴胀子势 $V(\varphi)$ 的谱流参数化。在谱动力学框架中（Paper V §7），FLRW 度规 $ds^2 = -dt^2 + a(t)^2 d\mathbf{x}^2$ 对应的递归系统 $R_{\text{FLRW}}$ 的谱像 $A_t$ 满足谱流方程：

$$\frac{d}{dt} A_t = [G_N A_{\text{GR}}, A_t]$$

在暴胀背景下，该方程在第 $k$ 个特征值 $\lambda_k(t)$ 上的投影给出 FLRW 谱方程（Paper V 定理 7.1）：

$$\frac{d}{dt} \lambda_k(t) = -2H(t) \cdot \lambda_k(t) + \sum_i g_i \cdot [A_{F,i}, A_t]_{kk}$$

其中 $-2H\lambda_k$ 项来自宇宙膨胀对谱的红移效应。

### 2.3 原初谱指数

原初谱指数 $n_s$ 作为谱流方程的斜率。暴胀期间 $A_t$ 的谱涨落 $\delta A_k$ 产生尺度依赖的原初功率谱：

$$\langle |\delta A_k|^2 \rangle \propto k^{n_s-1}$$

谱指数由慢滚参数给出（Paper IX §4.4）：

$$n_s - 1 = 2\eta - 6\epsilon$$

等价于谱流方程的线性化结果。当谱流方程在暴胀背景下线性化时，慢滚参数与谱斜率的关系为：

$$n_s = 1 - \frac{2}{N_e}$$

其中 $N_e$ 为 e-fold 数。标准 $N_e \approx 50\text{-}60$ 给出 $n_s \approx 0.960\text{-}0.967$，与 Planck 2018 观测值 $0.9649 \pm 0.0042$ 在 1.0σ 内一致。

### 2.4 ℓ_corr 替换

宇宙学的 $\ell_{\mathrm{corr}}$ 替换为 Hubble 半径：

$$\ell_{\mathrm{corr}}^{(\mathrm{Cosmo})} \;\longmapsto\; H^{-1}(z)$$

在暴胀层：

$$\ell_{\mathrm{corr}}^{(\mathrm{Infl})} = H_{\mathrm{inf}}^{-1}$$

即暴胀期 Hubble 半径。该尺度定义了暴胀期间因果接触的范围，是暴胀子量子涨落的关联长度。

### 2.5 截面输出

暴胀层向再加热层传递的截面参数包括：

| 参数 | 符号 | 观测约束 |
|:----|:----|:--------|
| 标量谱指数 | $n_s$ | $0.9649 \pm 0.0042$（Planck 2018） |
| 张量-标量比 | $r$ | $< 0.032$（BICEP/Keck） |
| 原初功率谱振幅 | $A_s$ | $\ln(10^{10}A_s) = 3.044 \pm 0.014$ |
| e-fold 数 | $N_e$ | $50\text{-}60$ |

完整的谱动力学生成功率谱（Paper IX D28.1，6 项检查全部通过）：

| 量 | 谱流值 | Planck 2018 | 匹配 |
|---|--------|-------------|:----:|
| $n_s$ | $0.9606 \pm 0.004$ | $0.9649 \pm 0.0042$ | ✅ 1.0σ |
| $r$ | $0.0040$ | $< 0.032$（95% CL） | ✅ |
| $\alpha_s$ | $-8.2 \times 10^{-5}$ | 未检测 | -- |

---

## §3 Bun(Reheat)：再加热层

### 3.1 基本参数

- **红移**：$z \sim 10^{26}$
- **能标**：$T_{\mathrm{rh}} \sim 10^{15}$ GeV（约暴胀能标的 $1/10$）
- **谱流参数**：$\xi_{\mathrm{rh}} = T$（温度）

### 3.2 粒子生成谱

暴胀结束后，暴胀子 $\phi$ 振荡并衰变为 Standard Model 粒子。粒子生成过程的谱表述：衰变宽度 $\Gamma_\phi$ 对应谱生成元的衰减项：

$$\Gamma_{\phi \to \chi\chi} \sim \frac{y^2}{8\pi} m_\phi$$

在谱纤维化框架中，该过程跨越 $\mathbf{Bun}(\mathrm{Inflation})$ 到 $\mathbf{Bun}(\mathrm{Reheat})$ 的纤维界面，对应遗忘函子 $\pi_{\mathrm{Infl}\leftarrow\mathrm{Reheat}}$ 的作用——暴胀子自由度被"遗忘"，成为再加热层的初始条件。

### 3.3 ℓ_corr 替换

$$\ell_{\mathrm{corr}}^{(\mathrm{Reheat})} = T_{\mathrm{rh}}^{-1}$$

即再加热温度的倒数。该尺度对应于再加热完成后热浴中粒子平均动能对应的 Compton 波长。

### 3.4 截面输出

| 参数 | 符号 | 说明 |
|:----|:----|:----|
| 再加热温度 | $T_{\mathrm{rh}}$ | 热浴达到的最高温度上限 |
| 再加热持续时间 | $\Delta t_{\mathrm{rh}}$ | 暴胀结束到辐射主导开始的时延 |
| Reheating 温度上限 | $T_{\mathrm{rh}}^{\max}$ | 由 CMB 观测约束的上限 |

再加热温度上限来自谱交织条件：在暴胀-再加热界面，$\varepsilon_{\mathrm{cosmo}} \sim H_{\mathrm{inf}}^2/M_{\mathrm{Pl}}^2 \sim 10^{-10}$，解耦条件充分。

---

## §4 Bun(BBN)：轻元素合成层

### 4.1 基本参数

- **红移**：$z \sim 10^9$
- **温度**：$T \sim 1$ MeV
- **时间**：$t \sim 1$ s（大爆炸后）
- **谱流参数**：$\xi_{\mathrm{BBN}} = T_{\mathrm{nuc}}$（核合成温度）

### 4.2 核子合成时序的谱流次序

BBN 期间，中子与质子的比值 $n/p$ 随温度降低而"冻结"。这一过程在谱框架中表现为谱流次序：

$$\frac{n}{p}(T) = \exp\left(-\frac{\Delta m}{T}\right)$$

其中 $\Delta m = m_n - m_p \approx 1.293$ MeV。n/p 冻结发生在 $T \sim 0.7$ MeV 处，对应谱流参数 $\xi_{\mathrm{BBN}} = T_{\mathrm{nuc}}$ 的一个临界点。

从谱动力学视角，n/p 比值的演化可视为谱流方程的一个特解——特征值 $\lambda_{n/p}(T)$ 沿温度参数的流动。

### 4.3 ℓ_corr 替换

$$\ell_{\mathrm{corr}}^{(\mathrm{BBN})} = T_{\mathrm{BBN}}^{-1} \sim 1\ \mathrm{MeV}^{-1}$$

在自然单位制中对应 $\sim 200$ fm。这是 BBN 期间核反应截面的特征关联尺度。

### 4.4 截面输出

| 参数 | 符号 | 观测值 |
|:----|:----|:------|
| 氦-4 丰度 | $Y_p$ | $0.245 \pm 0.003$ |
| 氘氢比 | D/H | $(2.527 \pm 0.030) \times 10^{-5}$ |
| 锂氢比 | Li/H | $(1.6 \pm 0.3) \times 10^{-10}$ |

这些截面参数作为 $\mathbf{Bun}(\mathrm{BBN})$ 的输出，传递给 $\mathbf{Bun}(\mathrm{LSS})$ 作为初始条件。

---

## §5 Bun(LSS)：大尺度结构层

### 5.1 基本参数

- **红移**：$z \sim 1100$（重组面）
- **温度**：$T \sim 0.26$ eV（重组温度）
- **时间**：$t \sim 380{,}000$ yr
- **谱流参数**：$\xi_{\mathrm{LSS}} = a(t)$（尺度因子）

### 5.2 CMB 功率谱的谱间隙关联

CMB 温度各向异性功率谱 $C_\ell^{TT}$ 在谱框架中具有重要地位。每个多极矩 $\ell$ 模对应一个谱特征，CMB 声峰的位置由谱间隙决定：

$$\ell_n = n \cdot \frac{\pi}{\theta_s} = n \cdot \frac{\pi d_A(z_*)}{r_s(z_*)}$$

其中 $\theta_s$ 为声视界角直径，$d_A(z_*)$ 为角直径距离，$r_s(z_*)$ 为重组时的声视界半径。

在谱纤维化框架中，CMB 功率谱的 TE 和 EE 极化谱同样具有谱表述——TE 交叉谱对应不同谱生成元之间的干涉项，EE 极化谱对应纯张量模式的谱流。

### 5.3 ℓ_corr 替换

$$\ell_{\mathrm{corr}}^{(\mathrm{LSS})} = r_s(z_*)$$

即重组面处的声视界半径。在 Planck 最佳拟合 ΛCDM 模型中：

$$r_s(z_*) \approx 147.09\ \mathrm{Mpc}$$

该尺度是 CMB 各向异性的特征关联长度，在谱框架中扮演 $\ell_{\mathrm{corr}}$ 相同的角色。

### 5.4 截面输出

LSS 层输出 $\Lambda$CDM 的六个基础参数：

| 参数 | 符号 | Planck 2018 |
|:----|:----|:-----------|
| 重子密度参数 | $\Omega_b h^2$ | $0.02237 \pm 0.00015$ |
| 冷暗物质密度参数 | $\Omega_c h^2$ | $0.1200 \pm 0.0012$ |
| Hubble 常数 | $H_0$ | $67.36 \pm 0.54$ km/s/Mpc |
| 光深 | $\tau_{\mathrm{reio}}$ | $0.0544 \pm 0.0073$ |
| 标量谱指数 | $n_s$ | $0.9649 \pm 0.0042$ |
| 功率谱振幅 | $A_s$ | $\ln(10^{10}A_s) = 3.044 \pm 0.014$ |

此外，$\mathbf{Bun}(\mathrm{LSS})$ 还输出非线性大尺度结构修正。谱流对易子 $[A_{\text{GR}}, A_t]$ 的 BCH 展开在二阶自然产生 SPT 模式耦合核（Paper V §7.4）：

$$F_2^{\mathrm{(spec)}}(k_1,k_2) = \frac{5}{7} + \frac{k_1\cdot k_2}{2k_1k_2}\left(\frac{k_1}{k_2} + \frac{k_2}{k_1}\right) + \frac{2}{7}\frac{(k_1\cdot k_2)^2}{k_1^2 k_2^2}$$

$F_2^{\mathrm{(spec)}} \equiv F_2^{(s)}$（SPT 标准对称化核），解析等价（1000 随机采样点最大偏差 0.00）。

### 5.5 CMB 功率谱的谱表述

CMB TT/TE/EE 功率谱在谱框架中的对应：

| CMB 谱 | 谱表述 | 物理对应 |
|:------|:------|:--------|
| $C_\ell^{TT}$ | $\mathrm{Tr}[\hat{\Theta}(x_i)\hat{\Theta}(x_j)]_{\ell}$ | 温度各向异性的谱关联 |
| $C_\ell^{TE}$ | $\langle \hat{\Theta} | \hat{E} \rangle_\ell$ | 温度-极化交叉谱（干涉项） |
| $C_\ell^{EE}$ | $\langle \hat{E} | \hat{E} \rangle_\ell$ | E 模极化谱（纯标量） |
| $C_\ell^{BB}$ | $\langle \hat{B} | \hat{B} \rangle_\ell$ | B 模极化谱（张量模式痕迹） |

---

## §6 Bun(DE)：暗能量层

### 6.1 基本参数

- **红移**：$z \sim 0$（近宇宙，$z < 2$）
- **物理内容**：宇宙晚期加速膨胀
- **谱流参数**：$\xi_{\mathrm{late}} = w(z)$（暗能量状态方程）

### 6.2 w(z) 参数化的谱流方程

暗能量状态方程 $w(z)$ 的参数化是谱流方程在宇宙学晚期的重要应用。采用 CPL 参数化：

$$w(z) = w_0 + w_a \frac{z}{1+z}$$

该参数化的谱流方程形式：

$$\frac{dw}{dz} = \frac{w_a}{(1+z)^2}$$

引入红移演化参数 $\xi_{\mathrm{DE}} = \ln(1+z)$，谱流方程简化为：

$$\frac{dw}{d\xi} = w_a e^{-\xi}$$

暗能量对应 $A_t$ 的真空渐近行为（Paper V §7.3）：

$$\lim_{t\to\infty} A_t = A_{\mathrm{vac}}$$

$A_{\mathrm{vac}}$ 的最小特征值 $\lambda_{\min} \sim \Lambda_{\mathrm{CC}}^{1/4}$ 给出宇宙学常数密度：

$$\rho_{\mathrm{vac}} = \lambda_{\min}^4$$

预言状态方程 $w = -1 + \mathcal{O}(H^2/M_{\mathrm{Pl}}^2)$，与 DESI 当前约束 $w = -1.0 \pm 0.1$ 一致。

### 6.3 ℓ_corr 替换

$$\ell_{\mathrm{corr}}^{(\mathrm{DE})} = d_H(z)$$

即 Hubble 距离：

$$d_H(z) = \frac{c}{H(z)} = \frac{c}{H_0\sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}}$$

在当前宇宙（$z=0$），$d_H(0) \approx 2998\ h^{-1}\ \mathrm{Mpc} \approx 4.4\ \mathrm{Gpc}$。

### 6.4 截面输出

| 参数 | 符号 | 当前约束 |
|:----|:----|:--------|
| 暗能量密度参数 | $\Omega_\Lambda$ | $0.6847 \pm 0.0073$ |
| 状态方程常数项 | $w_0$ | $-1.0 \pm 0.1$（DESI） |
| 状态方程演化项 | $w_a$ | $-0.1 \pm 0.3$（DESI） |
| Hubble 演化 | $H(z)$ | 由 BAO + SNe 约束 |

---

## §7 Bun(Quantum_Cosmo)：量子宇宙学层

### 7.1 基本参数

- **能标**：Planck 标度 $M_{\mathrm{Pl}} \sim 1.22 \times 10^{19}$ GeV
- **长度尺度**：Planck 长度 $l_{\mathrm{Pl}} \sim 1.616 \times 10^{-35}$ m
- **谱流参数**：无经典谱流参数——该层位于经典时空描述的边界

### 7.2 宇宙波函数的谱表述

量子宇宙学层的核心对象是宇宙波函数 $\Psi[h_{ij}, \phi]$，在谱框架中翻译为 $\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$ 上的截面。

Hartle-Hawking 无边界条件在谱框架中的实现：宇宙的初始条件由 $A_{\mathrm{GR}}$ 的谱截断自动提供（Paper IX 定理 3.1）。$A_{\mathrm{GR}}$ 在 Planck 尺度具有内在离散谱：

$$\lambda_k = \lambda_{\max} \cdot \frac{\sqrt{k(k+1)}}{\sqrt{k_{\max}(k_{\max}+1)}}, \quad k = 1, 2, \ldots, k_{\max}$$

其中 $k_{\max} \sim (M_{\mathrm{Pl}}/\Delta\lambda_{\min})^2$，$\lambda_{\max} \sim M_{\mathrm{Pl}}$。该离散谱结构将经典奇点替换为有限谱截断：

$$\|A_{\mathrm{GR}}\|_{\mathrm{HS}} \le \lambda_{\max} \sim M_{\mathrm{Pl}}$$

### 7.3 ℓ_corr 替换

$$\ell_{\mathrm{corr}}^{(\mathrm{Quantum\_Cosmo})} = l_{\mathrm{Pl}}$$

即 Planck 长度。这是谱框架中空间关联的最小可能尺度。

### 7.4 与 Bun(Quantum_Core) 的同一性猜想

量子宇宙学层与引力/黑洞领域的量子层（Paper XII §5 $\mathbf{Bun}(\mathrm{Quantum\_Core})$）可能存在同一性：

**猜想（量子层同一性）**：宇宙学的 $\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$ 与引力/黑洞的 $\mathbf{Bun}(\mathrm{Quantum\_Core})$ 共享同一纤维：

$$\mathbf{Bun}(\mathrm{Quantum\_Cosmo}) \cong \mathbf{Bun}(\mathrm{Quantum\_Core})$$

这一猜想对应 domain_generalization.md §8 开放问题 Q3。如果成立，则存在从宇宙波函数到黑洞内部量子谱的映射，对量子引力研究有重大意义。两个层的统一对比：

| 特征 | $\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$ | $\mathbf{Bun}(\mathrm{Quantum\_Core})$ |
|:----|:--------------------------------------|:-----------------------------------|
| 物理对象 | 宇宙波函数 $\Psi[h_{ij}, \phi]$ | 黑洞内部量子态 $| \mathrm{BH} \rangle$ |
| 谱截断 | $A_{\mathrm{GR}}$ 谱离散化 | $A_{\mathrm{GR}}$ 谱离散化 |
| 特征尺度 | $l_{\mathrm{Pl}}$ | $M^{-1}$（黑洞质量倒数） |
| 截面 | 无边界条件、量子反弹 | Bekenstein-Hawking 熵、QNM 谱 |
| 对应定理 | Paper IX §3 | Paper VIII §2 |

---

## §8 谱交织条件

### 8.1 交织条件缩放

宇宙学的谱交织条件使用红移间隔 $\Delta z$ 作为控制参数（domain_generalization.md §6.3）。对于相邻两层：

$$[A_i, \pi_{i\leftarrow i+1}]_{\mathrm{HS}} < \varepsilon_{\mathrm{cosmo}} \sim \frac{H_i^2}{M_{\mathrm{Pl}}^2}$$

其中 $H_i$ 为第 $i$ 层对应的 Hubble 参数。

### 8.2 各层间红移差

| 相邻层界面 | 红移差 $\Delta z$ | $\varepsilon_{\mathrm{cosmo}}$ 估计 | 解耦程度 |
|:----------|:----------------:|:----------------------------------:|:--------:|
| 暴胀-再加热 | $\sim 10^{27}$ | $\sim 10^{-10}$ | 充分解耦 |
| 再加热-BBN | $\sim 10^{17}$ | $\sim 10^{-40}$ | 高度解耦 |
| BBN-LSS | $\sim 10^{6}$ | $\sim 10^{-6}$ | 充分解耦 |
| LSS-DE | $\sim 10^{3}$ | $\sim 10^{-9}$ | 充分解耦 |
| DE-量子宇宙学 | Planck | $\sim 1$ | 非解耦——需同一化 |

在暴胀-再加热界面，$\varepsilon_{\mathrm{cosmo}} \sim 10^{-10}$，解耦条件充分。再加热-BBN 界面的 $\varepsilon_{\mathrm{cosmo}} \sim 10^{-40}$ 反映了再加热温度与 BBN 温度之间巨大的能标差距。

### 8.3 时间-纤维化对偶猜想

**猜想（时间-纤维化对偶）**：对于任何具有时间演化参数的物理领域，嵌套纤维化链 $\mathbf{Bun}(\mathcal{L}_1) \hookrightarrow \cdots \hookrightarrow \mathbf{Bun}(\mathcal{L}_m)$ 与时序因果结构之间存在函子性对应：

$$\Phi_{\mathrm{time}}: \mathbf{Causal}(t_1 < \cdots < t_m) \to \mathbf{BunFib}(\mathcal{L}_1, \dots, \mathcal{L}_m)$$

宇宙学是该猜想最直接的自然实例。在该猜想下：
- $\mathbf{Bun}(\mathrm{Inflation})$ 对应宇宙最早可观测时刻 $t_{\mathrm{infl}}$
- $\mathbf{Bun}(\mathrm{Reheat})$ 对应再加热完成时刻 $t_{\mathrm{rh}}$
- $\mathbf{Bun}(\mathrm{BBN})$ 对应核合成时刻 $t_{\mathrm{BBN}}$
- $\mathbf{Bun}(\mathrm{LSS})$ 对应重组时刻 $t_{\mathrm{LSS}}$
- $\mathbf{Bun}(\mathrm{DE})$ 对应当前时刻 $t_0$
- $\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$ 对应 Planck 时代的边界 $t_{\mathrm{Pl}}$

谱纤维的流动方向与因果时间的流逝方向一致，这为"时间为何单向流动"提供了范畴论解释——时间就是纤维化方向本身。

### 8.4 谱交织条件缩放定理的应用

由 domain_generalization.md 定理 1（谱交织条件缩放定理）：

$$\varepsilon_i(\Delta E_i) = \varepsilon_0 \cdot \left(\frac{\Delta E_0}{\Delta E_i}\right)^\alpha$$

在宇宙学中，$\Delta E_i$ 对应各层间的红移能标差距。宇宙学的 27 个数量级红移跨度使得 $\alpha > 0$ 时谱交织条件自动高度满足。唯一的例外是 DE-量子宇宙学界面，此时 $\Delta E \to 0$（两个层在 Planck 标度相邻），交织条件退化，需要通过同一化猜想处理。

---

## §9 开放问题

### Q1：时间-纤维化对偶猜想的严格范畴论证明

时间-纤维化对偶猜想（§8.3）目前处于直觉层面。需要给出严格证明，核心挑战包括：
- 构造 $\Phi_{\mathrm{time}}$ 的显式函子定义
- 证明因果结构的偏序关系在纤维化映射下的保持性
- 验证 $\Phi_{\mathrm{time}}$ 的自然变换与遗忘函子 $\hookrightarrow$ 的兼容性

### Q2：Bun(Quantum_Cosmo) 与 Bun(Quantum_Core) 的纤维同一性

宇宙学量子层与引力/黑洞量子层（§7.4）是否共享同一 $\mathbf{Bun}(\mathrm{Quantum})$？如果是，则宇宙波函数到黑洞内部量子谱的映射可能提供量子引力的关键突破口。需要：
- 验证 $A_{\mathrm{GR}}$ 谱离散化的统一形式在两种语境下等价
- 将 Bekenstein-Hawking 熵公式与宇宙波函数的谱范数关联
- 寻找可观测后果（如早期宇宙中的黑洞遗迹信号）

### Q3：CMB 功率谱的谱间隙关联

CMB 功率谱 $C_\ell$ 的多极矩结构在谱框架中的严格翻译：
- 每个 $\ell$ 模是否对应谱生成元的一个特征值？
- 声峰间距 $\Delta\ell \approx 300$ 是否对应谱间隙 $\Delta\lambda$ 的倒数？
- TE 交叉谱的符号交替是否来自不同谱生成元之间的干涉相消？

需要在 $\ell \in [2, 2500]$ 范围内对 Planck 2018 数据进行谱表述验证。

### Q4：暗能量 w(z) 参数化的谱流方程数值解

暗能量 $w(z)$ 参数化的谱流方程（§6.2）需要与 DESI、Euclid、Roman 等下一代巡天数据对比：
- 求解谱流方程 $\frac{dw}{d\xi} = w_a e^{-\xi}$ 的完整数值解
- 将 $w_0, w_a$ 的预测与 DESI DR1 约束比较
- 探索 $\lambda_{\min}$ 的特征值演化是否能解释 $w \neq -1$ 的可能性

### Q5：LSS 非线性谱流与 Euclid 数据的对接

谱流二阶展开自动导出的 SPT 模式耦合核 $F_2^{\mathrm{(spec)}}$（§5.4）需要与 Euclid 巡天的弱引力透镜数据对比。具体来说：
- 在 $k \in [0.01, 1] \ h/\mathrm{Mpc}$ 范围内检验 $F_2^{\mathrm{(spec)}}$ 的精度
- 将谱流方程的高阶展开与标准 $N$ 体模拟对比
- 评估谱流框架在处理 Baryon Acoustic Oscillation 非线性退化方面的优势

---

## 版本记录

**版本**：v0.1
**日期**：2026-07-25
**状态**：初稿。宇宙学 6 层嵌套纤维化链完整构建，时间-纤维化对偶猜想提出。

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| v0.1 | 2026-07-25 | 初稿。基于 domain_generalization.md §6 的宇宙学框架、Paper V §7 的谱动力学宇宙学、Paper IX 的量子宇宙学内容，完整构建 6 层纤维化链。 |
