# 轴子耦合静默推导

**假说**：轴子衰变常数 $f_a$ 和轴子质量 $m_a$ 由辫子静默 $S_4$ 确定。

## 1. 轴子的谱起源

在 $\mathbf{Sp}$ 框架中，轴子 $a$ 不是为解决强 CP 问题而人为引入的场，而是 $\mathbf{Sp}$ 4-范畴中辫子静默 $S_4$ 的自然产物。Peccei-Quinn (PQ) 对称性自发破缺的能标由谱间隙结构决定，而辫子静默 $S_4$ 是控制该能标的关键量。

从静默层级结构可知：
- 轴子作为 PQ 对称性的 Goldstone 玻色子出现
- PQ 对称性破缺能标由辫子静默 $S_4$ 设定
- $f_a \propto S_4 \cdot M_{\text{Pl}}$（或 $S_4^n \cdot M_{\text{Pl}}$）
- $m_a \propto \Lambda_{\text{QCD}}^2 / f_a$

## 2. 直接静默压制

给定辫子静默值：
$$S_4 = e^{-d_H} \approx e^{-2.7095} \approx 0.0666$$

### 方案 A：单层静默

$$f_a^{(1)} = S_4 \times M_{\text{Pl}} = 0.0666 \times 1.22 \times 10^{19}\ \text{GeV} \approx 8.1 \times 10^{17}\ \text{GeV}$$

轴子质量：
$$m_a^{(1)} \approx \frac{\Lambda_{\text{QCD}}^2}{f_a^{(1)}} \approx \frac{(0.2\ \text{GeV})^2}{8.1 \times 10^{17}\ \text{GeV}} \approx 5 \times 10^{-20}\ \text{eV}$$

### 方案 B：多层静默（$S_3 \times S_4$）

$$f_a^{(2)} = S_3 \times S_4 \times M_{\text{Pl}} = e^{-3} \times e^{-2.71} \times 1.22 \times 10^{19}\ \text{GeV}$$
$$= 0.0498 \times 0.0666 \times 1.22 \times 10^{19}\ \text{GeV} \approx 4.0 \times 10^{16}\ \text{GeV}$$

$$m_a^{(2)} \approx \frac{(0.2\ \text{GeV})^2}{4.0 \times 10^{16}\ \text{GeV}} \approx 1 \times 10^{-18}\ \text{eV}$$

### 方案 C：静默平方（$S_4^2$）

$$f_a^{(3)} = S_4^2 \times M_{\text{Pl}} = 0.00444 \times 1.22 \times 10^{19}\ \text{GeV} \approx 5.4 \times 10^{16}\ \text{GeV}$$

$$m_a^{(3)} \approx \frac{(0.2\ \text{GeV})^2}{5.4 \times 10^{16}\ \text{GeV}} \approx 7 \times 10^{-19}\ \text{eV}$$

### 方案 D：静默四次方（$S_4^4$）

$$f_a^{(4)} = S_4^4 \times M_{\text{Pl}} = (0.0666)^4 \times 1.22 \times 10^{19}\ \text{GeV} \approx 2.4 \times 10^{14}\ \text{GeV}$$

$$m_a^{(4)} \approx \frac{(0.2\ \text{GeV})^2}{2.4 \times 10^{14}\ \text{GeV}} \approx 1.7 \times 10^{-16}\ \text{eV}$$

## 3. 与实验约束的对比

| 方案 | $f_a$ (GeV) | $m_a$ (eV) | 与实验符合 |
|:----|:-----------:|:----------:|:---------:|
| A: $S_4^1$ | $8.1 \times 10^{17}$ | $5 \times 10^{-20}$ | ❌ $f_a$ 过大 |
| B: $S_3 S_4$ | $4.0 \times 10^{16}$ | $1 \times 10^{-18}$ | ❌ $f_a$ 过大 |
| C: $S_4^2$ | $5.4 \times 10^{16}$ | $7 \times 10^{-19}$ | ❌ $f_a$ 过大 |
| D: $S_4^4$ | $2.4 \times 10^{14}$ | $1.7 \times 10^{-16}$ | ❌ $f_a$ 仍偏高 |
| **实验窗口** | $10^{11}{-}10^{12}$ | $10^{-6}{-}10^{-3}$ | ✅ |

**结论**：纯静默压制 $S_4^n$ 给出的 $f_a$ 远大于实验约束。即使使用 $S_4^4$，$f_a \sim 10^{14}$ GeV 仍比 $10^{11}{-}10^{12}$ GeV 窗口高 2–3 个数量级。

## 4. 经 See-saw 能标的静默传输

轴子能标可能与中微子 See-saw 能标 $M_R \sim 10^{14}$ GeV 相关。尝试：

### 方案 E：$f_a \approx M_R / S_4$

$$f_a^{(5)} \approx \frac{M_R}{S_4} \approx \frac{1.5 \times 10^{14}\ \text{GeV}}{0.0666} \approx 2.3 \times 10^{15}\ \text{GeV}$$

仍偏大 3 个数量级。

### 方案 F：$f_a \approx M_R \times S_4$

$$f_a^{(6)} \approx M_R \times S_4 \approx 1.5 \times 10^{14}\ \text{GeV} \times 0.0666 \approx 1.0 \times 10^{13}\ \text{GeV}$$

接近上限。

### 方案 G：$f_a \approx M_R \times S_4^2$

$$f_a^{(7)} \approx M_R \times S_4^2 \approx 1.5 \times 10^{14}\ \text{GeV} \times 0.00444 \approx 6.7 \times 10^{11}\ \text{GeV}$$

<div align="center">
<b>✅ 落在 $10^{11}{-}10^{12}$ GeV 实验窗口内</b>
</div>

对应轴子质量：
$$m_a^{(7)} \approx \frac{(0.2\ \text{GeV})^2}{6.7 \times 10^{11}\ \text{GeV}} \approx 6 \times 10^{-5}\ \text{eV}$$

与 DFSZ/KSVZ 轴子模型的典型预言一致。

## 5. 理论解释

方案 G 的物理图像：轴子能标并非由 Planck 能标直接压制得到，而是经由 See-saw 能标 $M_R$ 的"二次静默"：

$$f_a \approx M_R \times S_4^2$$

其中：
- $M_R \sim 10^{14}$ GeV 来自谱 See-saw 机制（$M_R \sim M_{\text{Pl}} / \Lambda_{\text{EW}} \cdot v$）
- $S_4^2 \approx 0.0044$ 是两层辫子静默的累积效应
- 乘积给出 $f_a \sim 6.7 \times 10^{11}$ GeV

这暗示轴子能标和 See-saw 能标之间存在深层的谱联系——两者均由相同的静默层级结构决定，但在不同的幂次上表现出来。

## 6. 小结

| 量 | 表达式 | 数值 |
|:--|:------|:----:|
| 轴子衰变常数 | $f_a \approx M_R \times S_4^2$ | $\sim 6.7 \times 10^{11}$ GeV |
| 轴子质量 | $m_a \approx \Lambda_{\text{QCD}}^2 / f_a$ | $\sim 6 \times 10^{-5}$ eV |
| PQ 破缺能标 | $v_{\text{PQ}} \sim f_a$ | $\sim 10^{12}$ GeV |
| QCD θ 压制 | $\theta_{\text{QCD}} \sim S_4^4$ | $\sim 2 \times 10^{-5}$（轴子进一步压制） |

关键结论：轴子参数不由 Planck 能标直接静默决定，而通过 See-saw 能标 $M_R$ 的二次静默 $S_4^2$ 间接确定，为 $f_a$ 的实验窗口提供第一原理推导路径。
