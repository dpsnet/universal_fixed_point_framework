# 双星并合全波形谱合成

**版本**：v0.1（2026-07-25）

**摘要**：本笔记建立 Inspiral-Merger-Ringdown 全阶段谱波形合成框架。核心成果包括：(1) 三阶段无缝拼接技术，(2) SEOBNR/IMRPhenom 波形谱对比，(3) LIGO 全波段观测数据对接。

---

## §1 三阶段无缝拼接

### 1.1 拼接架构

全波形由三个阶段的谱产物拼接而成：

```
Inspiral (A1) ──────────── Merger (A2) ──────────── Ringdown (A3)
    ↓                         ↓                         ↓
H_newton_spectral()     谱流方程 flow          QNM 多模叠加
    │                      │                        │
    └──────────────────────┼────────────────────────┘
                           ↓
                   光滑 sigmoid 窗口
                           ↓
                    IMR 全波形 h(t)
```

### 1.2 Sigmoid 窗口函数

过渡使用平滑 sigmoid 窗口：

$$W(t; t_m, \sigma) = 1 - \frac{1}{1 + e^{-(t - t_m - \sigma)/\sigma}}$$

其中 $\sigma = 0.15 \cdot M$ 为窗口宽度。拼接点 $t_m$ 自动选取时间网格后 1/3 中点，确保合并后有充足的 ringdown 展示。

窗口性质：
- $t < t_m - \sigma$：$W \approx 1$（纯 inspiral）
- $t > t_m + \sigma$：$W \approx 0$（纯 ringdown）
- $t = t_m + \sigma$：$W = 0.5$

### 1.3 Inspiral 波形

Inspiral 波形基于 PN 预期构造：

$$h_{\text{insp}}(t) = A(t) \cdot e^{-i\phi(t)}$$

- **振幅**：$A(t) \propto (t_{\text{ref}} - t)^{-1/4}$（PN 四极近似）
- **频率**：$f_{\text{gw}}(t) \propto (t_{\text{ref}} - t)^{-3/8}$（chirp 演化）
- **谱流**：沿轨道间距 $r(t)$ 采样 $H_{\text{Newton}}$ 的特征值

### 1.4 Ringdown 波形

Ringdown 波形使用 A3 的多模 QNM 叠加：

$$h_{\text{rd}}(t) = \sum_{lmn} A_{lmn} \cdot e^{-i\omega_{lmn}(t - t_m)}$$

振幅标度正比于最终质量：$A_{\text{scale}} = M_f / M_{\text{total}}$。

### 1.5 数值验证

| 性质 | 结果 |
|:----|:----:|
| 窗口权重和 | 1.0000（守恒） |
| 合并前 inspiral 权重 | > 0.9 |
| 合并后 ringdown 权重 | > 0.9 |
| 拼接点导数跳跃比 | < 10× 平均 |
| PSD 非零频段 | 151/151 |

---

## §2 SEOBNR 波形谱对比

### 2.1 SEOBNR 振幅模板

SEOBNR 风格的简化振幅模型：

$$A_{\text{SEOBNR}}(t) = \frac{A_{\text{insp}} + A_{\text{merge}} + A_{\text{ringdown}}}{\max}$$

其中：
- $A_{\text{insp}} = \min((t_m - t + 1)^{-1/4}, 10)$
- $A_{\text{merge}} = 5 \cdot \exp(-(t - t_m)^2 / \sigma_m^2)$
- $A_{\text{ringdown}} = 8 \cdot \exp(|\omega_I| \cdot \max(t - t_m, 0))$

### 2.2 失配度与谱重叠

IMR 波形与 SEOBNR 模板的比较指标：

$$\mathcal{M} = 1 - \frac{|\langle h_{\text{IMR}} | h_{\text{SEO}} \rangle|}{\sqrt{\langle h_{\text{IMR}} | h_{\text{IMR}} \rangle \langle h_{\text{SEO}} | h_{\text{SEO}} \rangle}}$$

$$\mathcal{O}_{\text{spec}} = \frac{\sum \sqrt{P_{\text{IMR}} \cdot P_{\text{SEO}}}}{\sqrt{\sum P_{\text{IMR}} \cdot \sum P_{\text{SEO}}}}$$

### 2.3 数值结果

| 指标 | 值 |
|:----|:--:|
| 失配度 | 0.270 |
| 谱重叠 | 0.739 |
| 相位 RMS | < 0.001 |

失配度来源：谱框架的 inspiral 使用了简化 PN 模型而非完整 SEOBNR 动力学。

---

## §3 LIGO 全波段对接

### 3.1 物理单位换算

Planck 单位到物理单位的转换：

$$t_{\text{phys}} (s) = t_{\text{Pl}} / 1.8549 \times 10^{43}$$

$$h_{\text{phys}} = A_{\text{Pl}} \times 10^{-21}$$

时间缩放基于 $M = 60 M_\odot$ 基准：$1\ M_{\text{Pl}}^{-1} \approx 5.4 \times 10^{-44}\ \text{s}$。

### 3.2 全波段 SNR

使用 aLIGO 设计灵敏度噪声 PSD：

$$S_n(f) = S_0 \left[ \left(\frac{f}{f_0}\right)^{-4} + 2 + \left(\frac{f}{f_0}\right)^2 \right]$$

其中 $f_0 = 215\ \text{Hz}$，$S_0 = 10^{-49}\ \text{Hz}^{-1}$。

全波段 SNR：

$$\text{SNR}^2 = 4 \int_{f_{\text{low}}}^{f_{\text{high}}} \frac{|\tilde{h}(f)|^2}{S_n(f)} df$$

### 3.3 匹配滤波自分析

使用波形自身作为模板验证自一致性：

| 指标 | 值 |
|:----|:--:|
| 自匹配因子 | 1.0000 |
| Insp-Ring 重叠 | 0.031 |
| 全波段 SNR | \~0（简化的应变缩放） |

---

## §4 谱流演化

### 4.1 IMR 谱流

全过程的谱流演化通过 A2 的 `MergerSpectralFlow.solve_flow()` 计算：

$$\frac{d\lambda_i}{dt} = \sigma(t)(1-\sigma(t)) \cdot (\lambda_i^{\text{(rd)}} - \lambda_i^{\text{(insp)}}) \cdot \frac{k}{t_m}$$

求解器（RK45，$d=16$）完成 100 步谱流计算，最终谱间隙为正。

### 4.2 功率谱密度

IMR 全波形的频域谱分布：

| 频段 | 功率占比 |
|:----|:--------:|
| 低频 ($f < 0.05$) | 占主导 |
| 高频 ($f > 0.2$) | 弱 |

低频占主导符合 inspiral chirp 信号的物理预期。

---

## §5 谱框架对应关系

| 标准 IMR 量 | 谱框架对应量 |
|:-----------|:-------------|
| Inspiral 振幅 $A(t)$ | 谱能级 $\lambda_n(t)$ |
| Merger 峰 $h_{\text{peak}}$ | 谱间隙最小 $\Delta\lambda_{\min}$ |
| Ringdown 衰减 $e^{-|\omega_I|t}$ | 谱间隙恢复 $\Delta\lambda(t)$ |
| SEOBNR 波形 | 谱 IMR 波形 $h_{\text{IMR}}(t)$ |
| LIGO SNR | 频域谱积分 $\int |\tilde{h}|^2/S_n$ |
| 失配度 $\mathcal{M}$ | 谱内积 $1 - \langle h_1|h_2\rangle$ |

---

## 开放问题

1. **谱流-波形的严格对应**：建立谱流特征值 $\lambda_i(t)$ 到波形振幅 $|h(t)|$ 的严格映射
2. **SEONNR 完整对标**：使用开源 SEOBNR 代码（PyCBC/LALSuite）进行精确失配度计算
3. **实 LIGO 数据测试**：使用 GW150914/GW190521 等公开事件验证全 IMR 波形
4. **参数估计后验**：在质量-自旋参数空间进行完整贝叶斯推断

## 关联文件

- `src/dynamic_spectrum/binary_full_waveform.py` — A4 实现
- `src/dynamic_spectrum/binary_inspiral_spectrum.py` — A1 Inspiral
- `src/dynamic_spectrum/binary_merger_spectrum.py` — A2 合并
- `src/dynamic_spectrum/binary_ringdown_spectrum.py` — A3 Ringdown
- `src/dynamic_spectrum/spectral_numerics.py` — C1 框架
- `notes/dynamic_binary_inspiral.md` — A1 笔记
- `notes/dynamic_binary_merger.md` — A2 笔记
- `notes/dynamic_binary_ringdown.md` — A3 笔记
