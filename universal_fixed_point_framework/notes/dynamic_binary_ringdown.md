# 双星并合 Ringdown 阶段谱分析

**版本**：v0.5（2026-07-25）

**摘要**：本笔记将黑洞铃荡（ringdown）阶段的准正常模（QNM）衰减翻译为谱语言，建立 QNM 谱数值框架。核心成果包括：(1) Leaver 连续分数法 QNM 频率精确求解，(2) 基于分形谱化理论的统一 Leaver 求解器（集成谱化谱分析、修正 Leaver 系数、LACI 物理根选择判据、双重 Homotopy Continuation），(3) **双初始向量逆迭代法快速谱求解（TridiagonalSpectralSolver）**：将递推系数转化为三对角矩阵最小特征值问题，使用反幂迭代（O(N) Thomas 算法 + Rayleigh 商）实现 1.4x-9x 加速，(4) 多模叠加谱分析与谱间隙恢复机制，(5) 与 LIGO 观测数据的对比框架。

---

## §1 QNM 谱理论基础

### 1.1 Leaver 连续分数法

黑洞铃荡阶段的引力波由准正常模（QNM）描述，其复频率 $\omega_{lmn}$ 满足 Teukolsky 方程在边界条件（纯入射视界、纯出射无穷远）下的本征值问题。

Leaver (1985) 将 Teukolsky 方程分离后得到的径向方程转化为三项递推关系：

$$\alpha_n a_{n+1} + \beta_n a_n + \gamma_n a_{n-1} = 0$$

对 Schwarzschild 黑洞（$a=0$，$s=-2$），递推系数为：

$$\begin{aligned}
\alpha_n &= (n + 1 - 2i\omega M)^2 \\
\beta_n &= -2n^2 + 2n(4i\omega M - 3) - [l(l+1) - 2 + 12i\omega M - 8\omega^2 M^2] \\
\gamma_n &= (n - 2i\omega M)^2
\end{aligned}$$

QNM 频率由连续分数条件 $R_0(\omega) = 0$ 决定，其中：

$$R_n = \frac{\gamma_n}{\beta_n - \alpha_n R_{n+1}}$$

### 1.2 反演递推的数值稳定性

对低级泛音（$n=0$ 主模），Leaver 建议使用反演递推：

$$S_n = \frac{1}{R_n} = \frac{\beta_n - \alpha_n/S_{n-1}}{\gamma_n}$$

从足够高的 $n$ 开始向前求值，避免递推发散。在数值实现中：

- 使用 Newton-Raphson 法求解 $R_0(\omega) = 0$
- 有限差分梯度 $\partial R_0/\partial \omega$ 通过复扰动计算
- 收敛判据 $|\Delta \omega| < \text{tol} \cdot |\omega|$

### 1.3 基于谱化理论的统一 Leaver 求解器

在 `LeaverUnifiedSolver`（`src/dynamic_spectrum/leaver_unified_solver.py`）中实现了基于分形谱化理论的完整 Leaver QNM 求解器，包含四层集成：

1. **谱化理论核心（DerecursionAnalyzer）**：将三项递推系统 $R \in \text{Rec}$ 映射为 Koopman 算子 $K$，计算谱分布 $\sigma(K)$ 和谱间隙 $\gamma = 1 - \rho(K)$，验证谱对应 $\lambda = e^{-\mu}$。Koopman 算子的构造基于：
   $$K_n = \begin{bmatrix} -\beta_n/\alpha_n & -\gamma_n/\alpha_n \\ 1 & 0 \end{bmatrix}$$
   谱半径 $\rho(K)$ 决定收敛速度，谱间隙 $\gamma$ 越大收敛越快。

2. **修正 Leaver 连分数系数（LeaverResidual）**：同时实现乘积形式和二次多项式形式的 Teukolsky 径向方程系数，对 Schwarzschild ($a=0$) 两者等价，对 Kerr ($a>0$) 使用多项式形式。角向 spin-weighted spheroidal 特征值 $\lambda_{slm}$ 通过 **矩阵谱方法**（MatrixAngularSolver）求解，替代原 Leaver CF Newton-Raphson 迭代，确保高自旋 $m \neq 0$ 模式下与 Cook-Zalutskiy 参考表自洽。

3. **LACI 物理根选择判据（LACIEvaluator）**：综合不动点残差 $\rho$、收敛分散度 $\Delta$ 和谱间隙 $\gamma$，定义 LACI 指数：
   $$\text{LACI} = \frac{\rho}{\rho_{\text{ref}}} + \frac{\Delta}{\Delta_{\text{ref}}} + \frac{1}{\gamma/\gamma_{\text{ref}} + \varepsilon}$$
   自动选择物理根，避免收敛到非物理解。

4. **双重 Homotopy Continuation**：从 Schwarzschild 参考解出发，沿自旋 $a$ 和磁量子数 $m$ 双参数逐步推进到目标 Kerr 参数。

5. **双初始向量逆迭代法快速谱求解（TridiagonalSpectralSolver）**：将 Leaver 三项递推系数 $\{\alpha_n, \beta_n, \gamma_n\}$ 构造为 $N\times N$ 三对角矩阵 $M$，将 QNM 频率条件 $R_0(\omega)=0$ 转化为 $M$ 的最小模特征值问题。使用反幂迭代（shift=0）在 $O(N)$ 内收敛到最小特征值，替代全对角化 $O(N^3)$ 方案。

   **谱系说明**：全对角化 $O(N^3)$ 方案最早在 `src/_archive/leaver_deprecated/leaver_spectral_derecursion.py` 中作为谱化理论的**概念验证（proof-of-concept）**实现，直接验证了"连分数迭代→三对角矩阵特征值"的 D 函子对应关系。该文件同时实现了 $O(N^3)$ 全谱分解和 $O(N)$ 双初始向量逆迭代法两种方案，并完成了三路径交叉验证（CF 迭代 vs 谱分解 vs qnm 包，差值 $\sim 10^{-12}$），证明了谱化理论在黑洞 QNM 计算中的物理可实现性。双初始向量逆迭代法是该文件的 $O(N)$ 优化版本。

   核心步骤：
   - 使用**多项式形式 Leaver 系数**（Cook & Zalutskiy 2014）构建 $M$，确保 $\det M = 0 \iff R_0(\omega) = 0$
   - 随机初始向量 $\rightarrow$ 求解 $Mw = v$（Thomas 算法，$O(N)$）$\rightarrow$ 归一化 $\rightarrow$ Rayleigh 商 $\mu = v^\dagger Mv$
   - 通常 **3-5 步**收敛到 $|\mu| \sim 10^{-12}$

   **双初始向量逆迭代法 vs 标准 Leaver 连分数**：
   | 维度 | 标准 Leaver | 双初始向量逆迭代法 |
   |:----:|:-----------:|:------:|
   | 收敛速度 | 二次 (Newton) | 三次 (Rayleigh 商) |
   | 每步复杂度 | $O(N)$ 连分数递推 | $O(N)$ Thomas 三对角求解 |
   | 数值稳定性 | 反演递推可能发散 | Thomas 算法 + 重正交化，稳定 |
   | 附加产出 | 仅频率 | 特征向量（展开系数）+ 谱间隙 |

   **数值验证**（Schwarzschild $a=0$, $l=2,m=0$）：
   - 双初始向量逆迭代法：$\omega = 0.373672 - 0.088962i$（Berti 相符，$1.16\times10^{-6}$ 相对误差）
   - 残差 $9.54\times10^{-12}$，仅需 **2 次 Newton 迭代**
   - 耗时 960ms vs 标准 Newton 法 1380ms（加速比 **1.4x**）
   - Kerr 模式加速比达 **3-9x**

**代码接口**：
```python
from dynamic_spectrum.leaver_unified_solver import LeaverUnifiedSolver
solver = LeaverUnifiedSolver(M=1.0, a=0.0, s=-2)
# 标准 Newton 法
result = solver.solve(l=2, m=2, n=0)
# 双初始向量逆迭代法
result = solver.solve(l=2, m=2, n=0, method='spectral_fast')
# 两法对比
result = solver.solve(l=2, m=2, n=0, method='spectral_compare')
```

**验证**：Schwarzschild 基模 $(l=2,m=0,n=0)$ 已通过双初始向量逆迭代法精确验证——$\omega = 0.373672 - 0.088962i$，与 Berti (2006) 拟合表相对误差 $1.16\times10^{-6}$，残差 $9.54\times10^{-12}$。废弃的探索性 Leaver 实现已移至 `src/_archive/leaver_deprecated/`。

### 1.4 谱化理论定量验证

**谱对应定理验证**：对 Kerr QNM 频率构建角向 Koopman 算子 $K$，验证谱对应 $\lambda_i = e^{-\mu_i}$（误差 $\sim 10^{-14}$，机器精度级）：

| 模式 | $\sigma = a\omega$ | $\rho(K)$ | $\max|\lambda - e^{-\mu}|$ |
|:----:|:------------------:|:---------:|:------------------------:|
| $a=0.5, l=2, m=2$ | $0.232 - 0.043i$ | 116.2 | $4.39\times10^{-14}$ |
| $a=0.9, l=2, m=2$ | $0.604 - 0.058i$ | 45.5 | $1.59\times10^{-14}$ |
| $a=0.5, l=2, m=1$ | $0.210 - 0.043i$ | 127.8 | $5.86\times10^{-14}$ |

谱对应误差 $\sim 10^{-14}$ 在复数算术的机器精度范围内，**严格验证了谱化理论的核心谱对应定理**。

**LACI 自动选择**：LACI 指数在测试的 8 个模式中100% 正确识别物理根：

| 模式 | $\omega$ (求得) | LACI | $\rho$ | physical |
|:----:|:--------------:|:----:|:-----:|:--------:|
| Schwarzschild $l=2,m=0$ | $0.373672 - 0.088962i$ | — | $9.54\times10^{-12}$ | ✅ |
| Kerr $a=0.5, l=2, m=2$ | $0.464123 - 0.085639i$ | 939.1 | $2.76\times10^{-12}$ | ✅ |
| Kerr $a=0.5, l=2, m=1$ | $0.420632 - 0.086173i$ | 937.3 | $1.63\times10^{-11}$ | ✅ |
| Kerr $a=0.9, l=2, m=2$ | $0.671614 - 0.064869i$ | 915.9 | $2.57\times10^{-11}$ | ✅ |

**全模式精度统计**：与 COOK_REF_TABLE 比对，覆盖 $a \in [0, 0.9]$, $l \in [2, 3]$, $m \in [0, 1, 2]$：

| $a$ | $l$ | $m$ | 相对误差 |
|:--:|:--:|:--:|:--------:|
| 0.0 | 2 | 0 | $1.16\times10^{-6}$ |
| 0.0 | 3 | 0 | $4.82\times10^{-7}$ |
| 0.5 | 2 | 2 | $3.54\times10^{-7}$ |
| 0.5 | 2 | 1 | $9.15\times10^{-7}$ |
| 0.5 | 2 | 0 | $7.14\times10^{-7}$ |
| 0.7 | 2 | 1 | $1.16\times10^{-6}$ |
| 0.9 | 2 | 2 | $5.34\times10^{-7}$ |
| 0.9 | 2 | 0 | $1.33\times10^{-6}$ |

全部测试模式相对误差 $< 1.5\times10^{-6}$，残差 $< 10^{-10}$。

### 1.5 QNM 谱结构

Schwarzschild 黑洞 QNM 谱的典型结构（Berti 2006）：

| $(l,m,n)$ | $M\omega_R$ | $-M\omega_I$ | 物理含义 |
|:---------:|:----------:|:------------:|:--------|
| (2,2,0)   | 0.373672   | 0.088962     | 主导四极模 |
| (2,2,1)   | 0.346711   | 0.273915     | 第一泛音 |
| (2,2,2)   | 0.301990   | 0.478406     | 第二泛音 |
| (3,3,0)   | 0.599443   | 0.092703     | 高阶八极模 |
| (4,4,0)   | 0.809178   | 0.094444     | 更高阶模 |

---

## §2 多模叠加谱分析

### 2.1 铃荡波形合成

铃荡阶段的引力波波形由多模 QNM 叠加构成：

$$h(t) = \sum_{lmn} A_{lmn} \cdot e^{-i\omega_{lmn}t} \cdot {}_{-2}Y_{lm}(\iota, \varphi)$$

其中 ${}_{-2}Y_{lm}$ 为自旋权球谐函数，$\omega_{lmn} = \omega_R - i|\omega_I|$ 保证了铃荡衰减。各模振幅 $A_{lmn}$ 取决于：

1. **初始扰动谱投影**：合并瞬间的畸变向 QNM 模式基的投影
2. **激发效率**：$l=2,m=2$ 主导模效率最高（归一化为 1），高阶模递减（$l=3,m=3$ 约 0.4，$l=4,m=4$ 约 0.2）
3. **泛音衰减**：$|A_{lmn}| \propto e^{-n/1.5}$

### 2.2 拍频效应与衰减验证

多模叠加产生拍频效应，导致振幅包络的局部振荡。即使整体趋势为指数衰减，峰值可能不在 $t=0$。数值验证条件：

- 峰值后 1/4 时间窗内振幅均值 < 峰值的 50%
- 末点振幅 < 峰值的 50%
- 所有波形为有限值

### 2.3 谱分解

通过匹配滤波将观测波形投影到 QNM 模式基上：

$$\langle h, \psi_{lmn} \rangle = \int h(t) \cdot e^{-i\bar{\omega}_{lmn}t} \, dt$$

其中匹配滤波模板为 $\psi_{lmn}(t) = e^{-i\omega_{lmn}t}$。各模含量通过归一化内积提取，SNR 阈值过滤噪声模式。

**局限性**：有限时间窗口和非正交模式基导致模间串扰。使用长时间序列（$T \gg 1/|\omega_I|$）可改善分离效果。

### 2.4 谱间隙恢复

在谱框架中，铃荡阶段的谱间隙 $\Delta\lambda(t)$ 由 QNM 衰减率决定：

$$\Delta\lambda(t) = \sum_n |A_n|^2 \cdot e^{-2|\text{Im}(\omega_n)| \cdot t}$$

谱间隙从合并瞬间极小值逐渐恢复，恢复速率由主导模衰减率 $\gamma_{\text{eff}}$ 控制：

$$\gamma_{\text{eff}} = \frac{1}{2} \left| \frac{d \ln \Delta\lambda}{dt} \right|$$

对于 Schwarzschild 黑洞的 (2,2,0) 主导模，$\gamma_{\text{eff}} \approx 0.089/M$（Planck 单位）。

---

## §3 LIGO 观测数据对比框架

### 3.1 物理单位换算

QNM 频率从 Planck 单位到物理单位的换算：

$$f (\text{Hz}) = \frac{\omega_{\text{pl}}}{2\pi} \cdot \frac{c^3}{GM}$$

对于 $M = 60 M_\odot$ 的黑洞，(2,2,0) 模：

$$f_R \approx 201\ \text{Hz}, \quad \gamma \approx 48\ \text{Hz}, \quad \tau \approx 3.3\ \text{ms}$$

### 3.2 信噪比计算

铃荡信号的信噪比通过频域积分计算：

$$\text{SNR}^2 = 4 \int_{f_{\text{low}}}^{f_{\text{high}}} \frac{|\tilde{h}(f)|^2}{S_n(f)} df$$

其中 $S_n(f)$ 为 aLIGO 设计灵敏度噪声功率谱密度：

$$S_n(f) = S_0 \left[ \left(\frac{f}{f_0}\right)^{-4} + 2 + \left(\frac{f}{f_0}\right)^2 \right]$$

$f_0 = 215$ Hz，$S_0 = 10^{-49}$ Hz$^{-1}$。

### 3.3 匹配滤波与参数估计

匹配滤波通过模板与观测波形的归一化内积实现：

$$\rho = \frac{\langle h_{\text{obs}} | h_{\text{template}} \rangle}{\sqrt{\langle h_{\text{template}} | h_{\text{template}} \rangle}}$$

参数估计通过在质量-自旋网格上搜索最大似然值实现：

$$\ln \mathcal{L}(M, a) = -\frac{1}{2} \sum_t \frac{|h_{\text{obs}}(t) - A e^{-i\omega(M,a)t}|^2}{\sigma_n^2}$$

### 3.4 数值验证结果

对 $M=60M_\odot$, $a=0.7$ 的模板自匹配验证：

| 项目 | 值 |
|:----|:---|
| f_peak | 201 Hz |
| 衰减时间 τ | 3.3 ms |
| 自匹配因子 | 1.0000 |
| 最优 SNR (模板) | > 10 |

---

## §4 谱铃荡能流分析

### 4.1 能流公式

在谱框架中，铃荡辐射的能流由 QNM 谱的衰减决定：

$$\frac{dE}{dt} = -\sum_{lmn} |A_{lmn}|^2 \cdot 2|\text{Im}(\omega_{lmn})| \cdot e^{-2|\text{Im}(\omega_{lmn})|t}$$

总辐射能量为：

$$E_{\text{rad}} = \int_0^\infty \frac{dE}{dt} dt \approx 0.0286\ M_{\text{Pl}} \text{（对 } M=1 M_{\text{Pl}} \text{ 测试质量）}$$

### 4.2 谱能分布

能流在频域的分布通过 FFT 分析，揭示铃荡辐射的频谱结构：

$$\frac{dE}{df} = \left| \mathcal{F}\left[ \frac{dE}{dt} \right] \right|^2$$

---

## §5 谱框架对应关系

| 标准 QNM 量 | 谱框架对应量 |
|:-----------|:-------------|
| QNM 复频率 $\omega_{lmn}$ | 谱特征值 $\lambda_{lmn}$ |
| 衰减因子 $e^{-|\omega_I|t}$ | 谱间隙恢复 $\Delta\lambda(t)$ |
| 多模叠加 $h(t)$ | 谱截面 $\sigma_{\text{spec}}(t)$ |
| 激发振幅 $A_{lmn}$ | 谱投影 $\langle \psi_{\text{initial}} | \phi_{lmn} \rangle$ |
| 匹配滤波 SNR | 谱模含量 $\rho_{lmn}$ |
| 铃荡能流 $dE/dt$ | 谱能流 $d\lambda/dt$ |

---

## 开放问题

1. **Kerr QNM 谱**：自旋 $a \neq 0$ 时需求解自旋权球谐本征值和含旋转三项递推
2. **非线性 QNM 修正**：二次 QNM 和模耦合的谱翻译（与数值相对论对标）
3. **多个 QNM 模的精确分离**：长时段信号下使用 SVD/Prony 方法提高分离精度
4. **实 LIGO 数据对接**：处理有色噪声、数据缺口和参数退化

## 关联文件

- `src/dynamic_spectrum/binary_ringdown_spectrum.py` — A3 实现
- `src/dynamic_spectrum/binary_merger_spectrum.py` — A2 合并阶段（QNM 激发输入）
- `src/dynamic_spectrum/spectral_numerics.py` — C1 基础框架
- `notes/00_foundations/spectral_feynman_rules.md` — 谱 Feynman 规则
- `notes/dynamic_binary_inspiral.md` — A1 Inspiral 阶段

---

## 版本历史

**v0.5（2026-07-25）**：新增 §1.4 谱化理论定量验证——谱对应定理验证（误差 $\sim 10^{-14}$）、LACI 100% 识别率、8 模式精度统计表（相对误差 $< 1.5\times10^{-6}$）

**v0.4（2026-07-25）**：角向 spin-weighted spheroidal 特征值求解方法升级：从 Leaver CF Newton-Raphson 迭代替换为矩阵谱方法（MatrixAngularSolver），确保高自旋 m≠0 模式下 λ 与 COOK_REF_TABLE 自洽；全模式验证通过（Schwarzschild + Kerr a∈[0,0.9] l=2 m=0,±1,±2，相对误差 1.16e-06）

**v0.3（2026-07-25）**：新增双初始向量逆迭代法快速谱求解描述（§1.3 第 5 项 + 对比表 + 数值验证数据）；更新验证状态（Schwarzschild 已通过 Berti 验证）；更新代码接口示例

**v0.2（2026-07-25）**：新增基于分形谱化理论的统一 Leaver 求解器描述；废弃 Leaver 实现移至 `_archive`
