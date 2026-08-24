# 元通用不动点函子范畴框架：引力/黑洞精细纤维拆分——反向能标排序

**版本**：v0.1（2026-07-25）

**摘要**：将 Paper XXII 的 7 层嵌套纤维化方法论推广至引力/黑洞系统。由于能标排序从低能（远场/Newton 极限）向高能（近奇点/Planck 标度）递增，采用反向纤维化方向（$d=-1$）。建立 5 层嵌套纤维化链：

$$\mathbf{Bun}(\mathrm{Horizon}) \hookleftarrow \mathbf{Bun}(\mathrm{Exterior}) \hookleftarrow \mathbf{Bun}(\mathrm{Interior}) \hookleftarrow \mathbf{Bun}(\mathrm{Quantum\_Core}) \hookleftarrow \mathbf{Bun}(\mathrm{Singularity})$$

其中投影方向从外向内（低能 $\to$ 高能）。谱交织条件的反向修正见定理 3（纤维方向一致性定理，[`domain_generalization.md`](../00_foundations/spectral_fibration_domain_generalization.md) §1.3）。本笔记是 Phase 56B1 的核心交付物，与 Kerr 参数丛纤维化（[`spectral_kerr_fibration.md`](spectral_kerr_fibration.md)）和黑洞视界谱动力学（[Paper VIII](../../paper/paper8_black_hole_spectral.md)）紧密关联。

**前置依赖**：[`spectral_fibration_domain_generalization.md`](../00_foundations/spectral_fibration_domain_generalization.md) §3（引力/黑洞推广）、[`spectral_kerr_fibration.md`](spectral_kerr_fibration.md)（Kerr 参数丛 Grothendieck 纤维化）、[`paper8_black_hole_spectral.md`](../../paper/paper8_black_hole_spectral.md)（黑洞视界谱动力学）。

---

## §1 反向能标排序概览

### 1.1 引力系统的能标独特性

引力系统区别于量子化学的根本特征在于**能标排序方向**：

| 系统 | 排序方向 | 低能端 | 高能端 | $d$ |
|:----|:-------:|:------|:------|:---:|
| 量子化学 (Paper XXII) | 核区 $\to$ 自旋 | 自旋 (meV) | 核区 (keV) | $+1$ |
| **引力/黑洞** | **远场 $\to$ 奇点** | **远场/Newton (eV)** | **奇点/Planck ($10^{28}$ eV)** | **$-1$** |

远场（大尺度、低曲率）对应 Newton 极限和弱引力近似，近奇点（小尺度、高曲率）对应量子引力效应。能标从外向内递增 $E_{\mathrm{far}} \ll E_{\mathrm{hor}} \ll E_{\mathrm{Pl}}$，因此嵌套纤维化链的投影方向必须反转（$d=-1$），详见 `domain_generalization.md` 定理 3。

### 1.2 5 层结构表

参考 `domain_generalization.md` 表 §3.1，完整的 5 层反向纤维化链如下：

| 层 | 特征长度 | 物理内容 | 谱参数 | $\ell_{\mathrm{corr}}$ | 能标估计 |
|:--|:-------:|:--------|:------|:---------------------|:--------:|
| $\mathbf{Bun}(\mathrm{Horizon})$ | $r_+ \sim GM$ | 视界谱、Hawking 温度 | $\lambda_{\mathrm{horizon}}^{(\pm)}$ | $r_+^{-1}$ | $10^{-3}\text{--}10^{20}$ eV |
| $\mathbf{Bun}(\mathrm{Exterior})$ | $r > r_+$ | Kerr QNM、谱震荡 | $\omega_{lmn}(M,a)$ | $r^{-1}$ | $\sim T_H$ |
| $\mathbf{Bun}(\mathrm{Interior})$ | $0 < r < r_+$ | 内部谱、Cauchy 视界 | $\lambda_{\mathrm{int}}(r)$ | $(r_+ - r)^{-1}$ | $\sim M_{\mathrm{Pl}}^2/M$ |
| $\mathbf{Bun}(\mathrm{Quantum\_Core})$ | $\sim l_{\mathrm{Pl}}$ | 量子反弹、谱粘合 | $\Delta\lambda_{\mathrm{quantum}}$ | $l_{\mathrm{Pl}}$ | $\sim M_{\mathrm{Pl}}$ |
| $\mathbf{Bun}(\mathrm{Singularity})$ | $r \to 0$ | 奇点解析 | 极限谱 $\to 0$ | $\Lambda_{\mathrm{UV}}$ | $> M_{\mathrm{Pl}}$ |

### 1.3 反向纤维化方向的谱交织条件修正

根据 `domain_generalization.md` 定理 3，反向能标排序下谱交织条件阈值需修正：

$$\varepsilon_i^{(-1)} = \varepsilon_i^{(+1)} \cdot \frac{E_{i+1}}{E_i}$$

其中 $\varepsilon_i^{(+1)} \sim 10^{-3}$ 为量子化学基准。当 $E_{i+1} \ll E_i$（即相邻层能标差距极大）时，$\varepsilon_i^{(-1)}$ 被强烈压制，层间解耦自动满足。对于太阳质量黑洞，$E_{\mathrm{hor}}/E_{\mathrm{Pl}} \sim 10^{-19}$，$\varepsilon_{\mathrm{GR}} \sim 10^{-76}$。

### 1.4 $\ell_{\mathrm{corr}}$ 替换

引力系统的 $\ell_{\mathrm{corr}}$ 替换规则（`domain_generalization.md` 定理 2）：

$$\ell_{\mathrm{corr}}^{(\mathrm{GR})} \;\longmapsto\; M^{-1} \;\sim\; r_+^{-1}$$

各层具体替换值见第 1.2 节表格。

---

## §2 $\mathbf{Bun}(\mathrm{Horizon})$：视界谱层

### 2.1 谱生成元

视界层的谱生成元来自两个核心物理量：

1. **表面引力** $\kappa$：在 Schwarzschild 情形 $\kappa = 1/(4M)$，在 Kerr 情形：
   $$\kappa(M,a) = \frac{\sqrt{M^2 - a^2}}{M^2 + \sqrt{M^2 - a^2}}$$

2. **Hawking 温度** $T_H$：由 Paper VIII 定理 2.1，$T_H = \Delta\lambda_{\min}/(2\pi)$，其中 $\Delta\lambda_{\min}$ 是 $A_{\mathrm{GR}}$ 在视界上的谱间隙。

### 2.2 谱间隙

**Schwarzschild 情形**（Paper VIII §2.3，`scripts/paper22_horizon_spectrum.py` 数值验证）：
$$\Delta\lambda_{\min}^{(\mathrm{Schwarz})} = \frac{\sqrt{6} - \sqrt{2}}{\sqrt{72}} \approx 0.122$$

**Kerr 情形**（`spectral_kerr_fibration.md` 定义 2.1，Paper VIII §7）：
$$\Delta\lambda_{\min}^{(\mathrm{Kerr})}(M,a) = \Delta\lambda_{\min}^{(\mathrm{Schwarz})} \cdot \sqrt{1 - \frac{a^2}{M^2}}$$

### 2.3 谱间隙-温度丛态射

根据 `spectral_kerr_fibration.md` 定理 4.1，存在纤维保持函子 $\hat{\mathcal{H}}: \mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$：

$$T_H(M,a) = \frac{\Delta\lambda_{\min}^{(\mathrm{Kerr})}(M,a)}{2\pi}$$

### 2.4 截面输出

| 截面 | 表达式 | 来源 |
|:----|:------|:-----|
| Hawking 温度 | $T_H(M,a) = \kappa/(2\pi)$ | Paper VIII 定理 2.1 |
| 视界谱 | $\lambda_{\mathrm{horizon}}^{(\pm)} = M \pm \sqrt{M^2 - a^2}$ | `spectral_kerr_fibration.md` 定义 2.1 |
| 谱间隙 | $\Delta\lambda_{\min}$ = 式(2) | Paper VIII §2.3 |
| Bekenstein-Hawking 熵 | $S_{\mathrm{BH}} = A/4 = \pi/(4\Delta\lambda_{\min}^2)$ | Paper VIII 定理 3.1 |

### 2.5 $\ell_{\mathrm{corr}}$ 与谱交织条件

- $\ell_{\mathrm{corr}}$：$r_+^{-1}$（视界曲率标度）
- 谱交织条件：$\varepsilon_{\mathrm{Horizon}} \sim r_+/M$（远场与视界解耦）

---

## §3 $\mathbf{Bun}(\mathrm{Exterior})$：外部时空谱层

### 3.1 谱生成元

外部层的谱生成元来自 Kerr 准正态模（QNM）族 $\omega_{lmn}(M,a)$，其中：
- $l$：角量子数（$l \ge 2$ 为主）
- $m$：磁量子数（$-l \le m \le l$）
- $n$：径向量子数（$n = 0,1,2,\dots$）

### 3.2 与 Kerr 参数丛的对应

根据 `spectral_kerr_fibration.md` §2，外部时空谱层可视为 Kerr 参数丛 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 在固定 $(M,a)$ 处的纤维投影。该丛的 Grothendieck 纤维化结构（`spectral_kerr_fibration.md` 定理 3.1）保证了 QNM 谱沿参数方向的连续 Cartesian 提升。

### 3.3 QNM 谱结构

Paper VIII 定理 4.1 给出 Schwarzschild QNM 的谱形式：

$$\omega_n = \Delta\lambda_{\min} \cdot (l + \tfrac12 + n - i\gamma_n)$$

其中 $\gamma_n \approx (l+\tfrac12+n) \cdot \gamma_0$ 为阻尼系数。Kerr 情形下 QNM 发生分裂（Paper VIII §7）：

$$\omega_{lmn} = m\Omega_H + \Delta\lambda_{\min} \cdot (l + \tfrac12 + n) + i \cdot \mathrm{Im}(\omega_{lmn})$$

其中 $\Omega_H = a/(2Mr_+)$ 是视界角速度。

### 3.4 截面输出

| 截面 | 表达式 | 应用 |
|:----|:------|:----|
| QNM 频率 | $\{\omega_{lmn}(M,a)\}$ | 引力波模板匹配 |
| 谱间隙截面 | $\sigma_{\Delta}^{(\mathrm{Kerr})}(M,a)$ | `spectral_kerr_fibration.md` 定义 2.4 |
| Ringdown 波形 | $\Psi(t) = \sum A_{lmn} e^{-i\omega_{lmn}t}$ | LIGO/Virgo 数据分析 |

### 3.5 $\ell_{\mathrm{corr}}$ 与谱交织条件

- $\ell_{\mathrm{corr}}$：$r^{-1}$（径向坐标倒数，与距离相关）
- 谱交织条件：$\varepsilon_{\mathrm{Exterior}} \sim (l_{\mathrm{Pl}}/r_+)^2$（远场到视界的耦合随距离衰减）

---

## §4 $\mathbf{Bun}(\mathrm{Interior})$：内部谱层

### 4.1 谱生成元

内部层的谱生成元来自黑洞内部时空结构。穿过视界后，径向坐标 $r$ 变为类时方向，谱动力学发生相变（Paper VIII §7.2）。

### 4.2 内部离散谱

Paper VIII 定理 7.2 给出内部物质子空间投影谱：

$$E_n = E_0 \cdot S_4^n, \quad n = 0, 1, \dots, N_{\max}$$

其中：
- $E_0 = M_{\mathrm{Pl}}^2/M_{\mathrm{BH}}$ 为视界处最大能量尺度
- $S_4 = e^{-d_H}$ 为辫子静默因子
- $N_{\max} = A/(4l_{\mathrm{Pl}}^2)$ 由 Planck 尺度决定

### 4.3 Cauchy 视界

对于 Kerr 黑洞，内部存在 Cauchy 视界 $r_- = M - \sqrt{M^2 - a^2}$。Cauchy 视界附近：
- 谱间隙随 $r$ 变化：$\Delta\lambda_{\min}(r) \propto (r_+ - r)^{-1}$
- 质量膨胀效应（Mass inflation）：类光坐标下内部模指数增长

### 4.4 截面输出

| 截面 | 描述 | 来源 |
|:----|:-----|:-----|
| Cauchy 视界稳定性 | $r_-$ 附近谱流行为 | Paper VIII 推论 7.2 |
| 内部 QNM | 内部离散模 $E_n$ | Paper VIII 定理 7.2 |
| 质量膨胀效应 | 内部谱不稳定性 | — |

### 4.5 $\ell_{\mathrm{corr}}$ 与谱交织条件

- $\ell_{\mathrm{corr}}$：$(r_+ - r)^{-1}$（Cauchy 视界接近度）
- 谱交织条件：内部谱交织需数值扫描，因 $r$ 连续变化

---

## §5 $\mathbf{Bun}(\mathrm{Quantum\_Core})$：量子核心层

### 5.1 谱生成元

量子核心层的谱生成元来自 Planck 尺度量子修正。该层对应 $r \sim l_{\mathrm{Pl}}$ 区域，经典广义相对论失效，需量子引力描述。

### 5.2 谱粘合条件 $B(i)$

量子核心处谱在 Planck 标度的交织结构形式化为谱粘合条件 $B(i)$：

$$B(i): \quad [A_{\mathrm{QG}}, \pi_{\mathrm{QC}\leftarrow\mathrm{Sing}}]_{\mathrm{HS}} < \varepsilon_{\mathrm{QG}} \sim \left(\frac{l_{\mathrm{Pl}}}{r_+}\right)^2$$

其中 $A_{\mathrm{QG}}$ 是量子引力谱算子。对于太阳质量黑洞 $\varepsilon_{\mathrm{QG}} \sim 10^{-76}$，谱粘合自动满足。对于原初黑洞 $r_+ \sim l_{\mathrm{Pl}}$，$\varepsilon_{\mathrm{QG}} \sim 1$，完整量子引力理论不可避免。

### 5.3 与 Paper VIII 的对应

Paper VIII 推论 7.2（奇点谱消解）和 §7.2（内部离散模）为量子核心层的物理内容提供了直接依据：

1. **量子反弹**：$r \to l_{\mathrm{Pl}}$ 处谱流到达 $\partial\mathbf{Rec}_D$ 边界，发生谱分支反射（类似宇宙学量子反弹，Paper IX）
2. **Bohr-Sommerfeld 量子化面积谱**：视界面积量子化 $A_n = n \cdot 4l_{\mathrm{Pl}}^2$，对应谱求和 $S_{\mathrm{BH}} = \sum_n \ln(1/\lambda_n)$（Paper VIII 定理 7.6）

### 5.4 截面输出

| 截面 | 描述 | 来源 |
|:----|:-----|:-----|
| 量子反弹 | $r \sim l_{\mathrm{Pl}}$ 处谱分支反射 | Paper VIII 推论 7.2 |
| Bohr-Sommerfeld 面积谱 | $A_n = n \cdot 4l_{\mathrm{Pl}}^2$ | Paper VIII 定理 7.6 |
| 量子修正谱 | $\Delta\lambda_{\mathrm{quantum}}$ | — |

### 5.5 $\ell_{\mathrm{corr}}$ 与谱交织条件

- $\ell_{\mathrm{corr}}$：$l_{\mathrm{Pl}}$（Planck 长度）
- 谱交织条件：$\varepsilon_{\mathrm{QG}} \sim (l_{\mathrm{Pl}}/r_+)^2$

---

## §6 $\mathbf{Bun}(\mathrm{Singularity})$：奇点解析层

### 6.1 谱生成元

奇点解析层的谱生成元来自奇点消解的极限谱行为。经典奇点 $r=0$ 在谱动力学中被替换为谱流在 $\partial\mathbf{Rec}_D$ 边界上的分支点。

### 6.2 极限谱 $\to 0$ 的收敛性

谱动力学如何解析经典奇点（Paper VIII 推论 7.2）：

$$\lim_{r \to 0} \sigma(A_{\mathrm{GR}}(r)) = \{0\}$$

极限谱收敛到零意味着：
- 经典奇点处的曲率发散被谱的零测度收敛替代
- 谱流方程在 $\partial\mathbf{Rec}_D$ 边界处的分支反射产生量子反弹
- 信息在谱中继续存在，不会被"压碎"

### 6.3 与谱消解理论（Paper IX）的对应

奇点解析层与 Paper IX（奇点谱消解与量子宇宙学）共享谱分支反射机制：

| 系统 | 经典奇点 | 谱消解机制 | Paper IX 映射 |
|:----|:--------|:----------|:-------------|
| 黑洞内部 | $r=0$ 曲率发散 | $\partial\mathbf{Rec}_D$ 边界分支反射 | §4（谱分支） |
| 宇宙学大爆炸 | $t=0$ 标度因子为零 | $\partial\mathbf{Rec}_D$ 边界分支反射 | §3（量子反弹） |

### 6.4 截面输出

| 截面 | 描述 | 来源 |
|:----|:-----|:-----|
| 奇点解析 | 极限谱 $\to 0$ 收敛 | Paper VIII 推论 7.2 |
| 分支反射 | $\partial\mathbf{Rec}_D$ 边界处的谱流转向 | Paper IX |
| UV 截断 | $\Lambda_{\mathrm{UV}}$ 处谱截断 | — |

### 6.5 $\ell_{\mathrm{corr}}$ 与谱交织条件

- $\ell_{\mathrm{corr}}$：$\Lambda_{\mathrm{UV}}$（UV 截断）
- 谱交织条件：奇点解析层的交织条件由 UV 完备性保证

---

## §7 层间谱交织条件汇总

### 7.1 完整 5 层谱交织条件表

| 层间接口 | 投影方向 | 谱交织条件 $\varepsilon_i$ | 数值估计（$M_\odot$） | 数值估计（原初） |
|:---------|:-------:|:--------------------------|:-------------------:|:--------------:|
| Hor $\to$ Ext | $\pi_{\mathrm{ext}\leftarrow\mathrm{hor}}$ | $\varepsilon_{\mathrm{Hor}} \sim r_+/M$ | $\sim 10^{-6}$ | $\sim 1$ |
| Ext $\to$ Int | $\pi_{\mathrm{int}\leftarrow\mathrm{ext}}$ | $\varepsilon_{\mathrm{Ext}} \sim (l_{\mathrm{Pl}}/r_+)^2$ | $\sim 10^{-76}$ | $\sim 1$ |
| Int $\to$ QC | $\pi_{\mathrm{QC}\leftarrow\mathrm{int}}$ | $\varepsilon_{\mathrm{Int}} \sim (M_{\mathrm{Pl}}^2/M^2)$ | $\sim 10^{-76}$ | $\sim 1$ |
| QC $\to$ Sing | $\pi_{\mathrm{Sing}\leftarrow\mathrm{QC}}$ | $\varepsilon_{\mathrm{QG}} \sim (l_{\mathrm{Pl}}/r_+)^2$ | $\sim 10^{-76}$ | $\sim 1$ |

### 7.2 反向能标排序的 $\varepsilon_i$ 修正

根据 `domain_generalization.md` 定理 3，$d=-1$ 方向下各层谱交织条件的修正因子为 $E_{\mathrm{lower}}/E_{\mathrm{higher}}$：

| 层对 | $E_{i+1}/E_i$ | $\varepsilon_i^{(-1)}/\varepsilon_i^{(+1)}$ |
|:----|:------------:|:------------------------------------------:|
| Hor/Ext | $T_H / E_{\mathrm{far}}$ | $E_{\mathrm{far}}/T_H \gg 1$ |
| Ext/Int | $M_{\mathrm{Pl}}^2/M / T_H$ | $\sim (M/M_{\mathrm{Pl}})^2$ |
| Int/QC | $M_{\mathrm{Pl}} / (M_{\mathrm{Pl}}^2/M)$ | $\sim M/M_{\mathrm{Pl}}$ |
| QC/Sing | $\Lambda_{\mathrm{UV}}/M_{\mathrm{Pl}}$ | $\sim 1$（模型依赖） |

### 7.3 收敛性讨论

**太阳质量黑洞**（$M \sim M_\odot \sim 10^{38}M_{\mathrm{Pl}}$）：
- $\varepsilon_{\mathrm{GR}} \sim (l_{\mathrm{Pl}}/r_+)^2 \sim 10^{-76}$
- 层间解耦条件极宽松，5 层纤维化链高度收敛
- 实质：经典引力区域与量子引力区域的巨大能标鸿沟使谱交织条件自动满足

**原初黑洞**（$M \sim M_{\mathrm{Pl}}$）：
- $\varepsilon_{\mathrm{GR}} \sim 1$
- 层间解耦失效，所有层需要统一处理
- 实质：量子引力效应贯穿所有尺度，反向纤维化链坍缩为单层 $\mathbf{Bun}(\mathrm{QG})$

> **注意**：`domain_generalization.md` §3.4 提出的猜想——反向纤维化收敛速度由 $\min(E_{i+1}/E_i)$ 控制——在引力系统中得到验证。对于天体物理黑洞 $E_{\mathrm{hor}}/E_{\mathrm{Pl}} \ll 1$ 意味着收敛速度极快，但 $\mathbf{Bun}(\mathrm{Quantum\_Core})$ 内部因 Planck 标度的量子涨落可能存在发散——这需要量子引力理论的完整描述。

---

## §8 开放问题

### Q1: 反向纤维化收敛速度

反向纤维化收敛速度由 $\min(E_{i+1}/E_i)$ 控制。对于引力系统，$E_{\mathrm{hor}}/E_{\mathrm{Pl}} \ll 1$ 保证了整体收敛性。但 $\mathbf{Bun}(\mathrm{Quantum\_Core})$ 内部在 Planck 标度附近是否存在发散？这对应 `domain_generalization.md` Q2。

### Q2: 引力 $\mathbf{Bun}(\mathrm{Quantum})$ 与宇宙学 $\mathbf{Bun}(\mathrm{Quantum})$ 间的纤维同一性

宇宙学的量子层（Planck 标度，`domain_generalization.md` §6.1 $\mathbf{Bun}(\mathrm{Quantum\_Cosmo})$）与引力/黑洞的 $\mathbf{Bun}(\mathrm{Quantum\_Core})$ 是否共享同一纤维？若存在从宇宙波函数到黑洞内部量子谱的映射（`domain_generalization.md` Q3），则两个 $\mathbf{Bun}(\mathrm{Quantum})$ 应在 $\partial\mathbf{Rec}_D$ 拓扑中重合——这与 Paper VIII 推论 7.2（量子反弹与宇宙学量子反弹的谱分支对应）一致。

### Q3: Kerr 参数丛与空间分层丛间的粘贴条件

Kerr 参数丛 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$（`spectral_kerr_fibration.md`）以 $(M,a)$ 为基，而本笔记的空间分层丛以径向坐标 $r$ 为基。两个丛的粘贴条件为：在固定 $(M,a)$ 处，$\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 的纤维数据给出 $\mathbf{Bun}(\mathrm{Horizon})$ 和 $\mathbf{Bun}(\mathrm{Exterior})$ 的谱截面。但 $\mathbf{Bun}(\mathrm{Interior})$ 内部随 $r$ 的谱流如何从 Kerr 参数丛的纤维结构中派生？这涉及丛的**垂直-水平分解**需要明确的形式化。

### Q4: 引力波观测对谱交织条件的约束

LIGO/Virgo/KAGRA 的 Ringdown 观测能否检验 $\mathbf{Bun}(\mathrm{Exterior})$ 的截面传递？具体而言：
- QNM 频率的测量精度 $\delta\omega/\omega$ 能否约束 $\varepsilon_{\mathrm{Exterior}}$？
- 若未来观测到 QNM 与预测的系统性偏差，是否可归因于 $\mathbf{Bun}(\mathrm{Interior})$ 对 $\mathbf{Bun}(\mathrm{Exterior})$ 的谱交织泄漏？
- 这需要将谱交织条件 $\varepsilon_i$ 与引力波模板的不确定度建立定量关系

### Q5: 极端极限下非乘积丛结构的影响

`spectral_kerr_fibration.md` 和 Paper VIII §7.4.5 指出 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 在 $a \to M$ 时发生纤维类型跳变（离散谱 $\to$ 简并谱）。这一非乘积丛结构如何影响反向纤维化链？在 $a=M$ 处，$\mathbf{Bun}(\mathrm{Horizon})$ 的谱间隙闭合，可能导致 $\mathbf{Bun}(\mathrm{Horizon}) \to \mathbf{Bun}(\mathrm{Exterior})$ 的谱交织条件退化——这与极端黑洞的"零温度"极限一致。

---

## 版本记录

| 版本 | 日期 | 状态 | 更新内容 |
|:----|:----|:----|:--------|
| **v0.1** | **2026-07-25** | **初稿** | 5 层反向纤维化链完整构建。与 `spectral_kerr_fibration.md`（Kerr 参数丛）和 Paper VIII（黑洞视界谱动力学）的交叉引用完全建立。8 个开放问题（Q1-Q5）明确列出。 |

**变更记录**：

| 版本 | 日期 | 变更内容 |
|:----|:----|:--------|
| v0.1 | 2026-07-25 | 初稿。完整构建 5 层反向纤维化链：$\mathbf{Bun}(\mathrm{Horizon})$（§2，视界谱层，含 Hawking 温度截面）、$\mathbf{Bun}(\mathrm{Exterior})$（§3，外部 QNM 谱层，与 Kerr 丛对应）、$\mathbf{Bun}(\mathrm{Interior})$（§4，内部谱层，含 Cauchy 视界）、$\mathbf{Bun}(\mathrm{Quantum\_Core})$（§5，量子核心层，含谱粘合条件与 Bohr-Sommerfeld 面积谱）、$\mathbf{Bun}(\mathrm{Singularity})$（§6，奇点解析层，与 Paper IX 对应）。§7 给出完整层间谱交织条件汇总表和收敛性讨论。§8 列出 5 个开放问题。 |
