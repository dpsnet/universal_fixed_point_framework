# 双星并合合并阶段谱分析

**版本**：v0.1（2026-07-25）

**摘要**：本笔记建立黑洞合并阶段的谱演化框架，涵盖从 inspiral 末态到 ringdown 初态的连续过渡。核心成果包括：(1) 合并谱流方程数值解，(2) QNM 激发谱分析，(3) 合并-铃荡过渡区谱间隙动力学，(4) 全波形 IMR 谱合成。

---

## §1 残余黑洞属性

### 1.1 NR 拟合公式

双黑洞并合后的残余黑洞质量与自旋由数值相对论（NR）拟合公式确定：

$$M_f = M_{\text{total}} \cdot (1 - E_{\text{rad}})$$

其中辐射能量 $E_{\text{rad}}$ 依赖于对称质量比 $\nu = m_1 m_2 / M_{\text{total}}^2$ 和有效自旋 $\chi_{\text{eff}}$：

$$E_{\text{rad}} = \left(1 - \sqrt{\frac{8}{9}}\right) \cdot 4\nu \cdot (1 + 0.1\chi_{\text{eff}})$$

残余自旋近似为：

$$a_f \approx \chi_{\text{eff}} + \nu(\chi_1 + \chi_2) \cdot 0.1$$

### 1.2 残余 QNM 频率

残余黑洞的 QNM 频率使用 Berti 2006 的自旋依赖拟合公式：

$$\omega_{220}(a_*) = \frac{1}{M_f} \left[ \omega_0 + c_1 a_* + c_2 a_*^2 - i(\tau_0 + \tau_1 a_* + \tau_2 a_*^2) \right]$$

其中 $\omega_0 = 0.3737$, $\tau_0 = 0.0889$ 为 Schwarzschild 基频。

### 1.3 数值验证

| 参数 | 等质量非自旋 | 等质量高自旋 |
|:----|:-----------:|:-----------:|
| $M_f$ | 1.8856 $M_{\text{Pl}}$ | 1.8556 $M_{\text{Pl}}$ |
| $a_*$ | 0.0000 | 0.1634 |
| $\omega_{220}$ | 0.1982 - 0.0471i | 0.3703 - 0.0531i |

---

## §2 合并谱流方程

### 2.1 谱流框架

合并阶段的谱演化由谱流方程控制：

$$\frac{d\lambda_i}{dt} = F_i(\lambda, t)$$

其中 $\lambda_i$ 是谱特征值，$F_i$ 为流函数。合并过程建模为从双星谱（inspiral 端）向 QNM 谱（ringdown 端）的连续过渡。

### 2.2 过渡模型

使用 sigmoid 过渡函数实现两端的平滑切换：

$$\sigma(t) = \frac{1}{1 + e^{-k(t/t_m - 0.5)}}$$

其中 $k = 20$ 为过渡陡度，$t_m$ 为合并时间尺度。谱流速度：

$$\frac{d\lambda_i}{dt} = \sigma(1-\sigma) \cdot (\lambda_i^{\text{(ringdown)}} - \lambda_i^{\text{(inspiral)}}) \cdot \frac{k}{t_m}$$

### 2.3 两端谱结构

**Inspiral 端**（$t \ll t_m$）：

$$\lambda_n^{(0)} = -\frac{\mu M^2}{2n^2} \cdot \left[1 + \frac{\nu}{n^2}\varepsilon + \frac{\nu^2}{n^4}\varepsilon^2 + \frac{\nu^3}{n^6}\varepsilon^3\right]$$

**Ringdown 端**（$t \gg t_m$）：

$$\lambda_n = \lambda_{\text{offset}} + \omega_R^{(n)}$$

其中 $\omega_R^{(n)}$ 为 QNM 泛音实部，$\lambda_{\text{offset}}$ 保证谱连续性。

### 2.4 数值结果

谱流求解器（RK45，$d=16$，100 步）最小谱间隙 $\Delta\lambda_{\min} \approx 8.9 \times 10^{-6}$。

---

## §3 QNM 激发谱

### 3.1 激发振幅

QNM 激发振幅正比于合并瞬间的跃迁矩阵元：

$$A_{lmn} = \langle \psi_{lmn}^{\text{(QNM)}} | P_{\text{merge}} | \psi_0^{\text{(inspiral)}} \rangle$$

在谱框架中简化为：

$$|A_{lmn}| \propto \frac{1}{|\text{Im}(\omega_{lmn})|} \cdot \eta_{lm} \cdot e^{-n/2}$$

其中 $\eta_{lm}$ 为模依赖系数（$(2,2) = 1.0$, $(2,1) = 0.1$, $(3,3) = 0.05$ 等）。

### 3.2 铃荡波形

使用修正后的符号约定（$\omega = \omega_R - i|\omega_I|$）：

$$h(t) = \sum_{lmn} A_{lmn} \cdot e^{-i\omega_{lmn}t}$$

保证物理衰减：$|h(t)| \sim e^{-|\omega_I|t}$。

### 3.3 主导 QNM 模

| $(l,m,n)$ | $M\omega_R$ | $-M\omega_I$ | $|A|$（归一化） |
|:---------:|:----------:|:------------:|:--------------:|
| (2,2,0)   | 0.1982     | 0.0471      | 21.21 |
| (2,2,1)   | 0.1898     | 0.0489      | 10.07 |
| (2,1,0)   | 0.2039     | 0.0121      | 2.12 |
| (3,3,0)   | 0.3171     | 0.0047      | 1.06 |

---

## §4 谱间隙动力学

### 4.1 三阶段模型

合并-铃荡过渡区谱间隙经历三个阶段：

$$\Delta\lambda(t) = \Delta\lambda_{\text{inspiral}}(t) + \Delta\lambda_{\text{collapse}}(t) + \Delta\lambda_{\text{recovery}}(t)$$

**1. 压缩**（$t < t_{\text{merge}}$）：轨道间距减小驱动谱间隙线性缩小

$$\Delta\lambda_{\text{inspiral}} \propto \frac{r(t) - r_{\text{ISCO}}}{M}$$

**2. 坍缩**（$t \approx t_{\text{merge}}$）：在合并瞬间谱间隙急速下降

$$\Delta\lambda_{\text{collapse}} = e^{-|t-t_m|/\tau_m} \cdot \left(1 - e^{-(t-t_m)^2/\sigma^2}\right)$$

**3. 恢复**（$t > t_{\text{merge}}$）：QNM 衰减驱动谱间隙指数恢复

$$\Delta\lambda_{\text{recovery}} = 1 - \sum_{n} A_n e^{-(t-t_m)/\tau_n}$$

### 4.2 数值验证

| 阶段 | $\Delta\lambda$ |
|:----|:--------------:|
| 合并前 ($t=-2$) | 1.0000 |
| 合并处 ($t=0$) | 0.4105 |
| 合并后 ($t=5$) | 0.5912 |

间隙在合并点最小，铃荡恢复后回升，趋势与物理预期一致。

---

## §5 全波形 IMR 合成

### 5.1 波形结构

Inspiral-Merger-Ringdown 全波形由三阶段拼接：

$$h(t) = \begin{cases}
h_{\text{inspiral}}(t) \cdot \mathcal{E}(t), & t < t_m \\
h_{\text{ringdown}}(t - t_m), & t \geq t_m
\end{cases}$$

其中 $\mathcal{E}(t)$ 为 inspiral 包络函数，$h_{\text{ringdown}}$ 为多模 QNM 叠加。

### 5.2 包络模型

- **Inspiral 包络**：$\mathcal{E}(t) \propto 1/(t_m - t + \text{const})$，随接近合并发散
- **Ringdown 包络**：$\mathcal{E}(t) = e^{-(t-t_m)/\tau_{\text{QNM}}}$，指数衰减

### 5.3 数值验证

对 $M=2.0 M_{\text{Pl}}$ 等质量双星：
- 铃荡段 400 时间点，前 1/3 均值 0.966 > 后 1/3 均值 0.847，验证衰减趋势
- 铃荡包络单调递减

---

## §6 谱框架对应关系

| 标准合并量 | 谱框架对应量 |
|:----------|:------------|
| 残余黑洞质量 $M_f$ | 谱流终态特征值 |
| QNM 复频率 $\omega_{lmn}$ | 谱特征值 $\lambda_{lmn}$ |
| 激发振幅 $A_{lmn}$ | 谱跃迁矩阵元 |
| 合并时间 $t_{\text{merge}}$ | 谱间隙最小点 |
| 过渡宽度 | sigmoid 陡度 $k$ |
| IMR 全波形 | 谱流插值 $+$ 多模叠加 |

---

## 开放问题

1. **谱流方程的高精度求解**：使用自适应步长谱求解器改善谱间隙处的分辨率
2. **NR 拟合的谱对标**：与 SEOBNR/IMRPhenom 残余拟合公式精确对比
3. **自旋进动效应**：非对齐自旋下 QNM 激发谱的推广
4. **偏心合并**：$e > 0$ 时谱流方程的修正

## 关联文件

- `src/dynamic_spectrum/binary_merger_spectrum.py` — A2 实现
- `src/dynamic_spectrum/binary_inspiral_spectrum.py` — A1 Inspiral 阶段（谱流初态输入）
- `src/dynamic_spectrum/binary_ringdown_spectrum.py` — A3 Ringdown 阶段（谱流终态对标）
- `src/dynamic_spectrum/spectral_numerics.py` — C1 谱数值框架
- `notes/04_lorentz_gravity/dynamic_binary_inspiral.md` — A1 研究笔记
- `notes/04_lorentz_gravity/dynamic_binary_ringdown.md` — A3 研究笔记
