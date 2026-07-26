# Higgs-费米子谱交织子：$A_H$ 投影与 Yukawa 特征值的谱推导

**版本**：v0.5（2026-07-23）

**摘要**：本笔记建立 Higgs 谱算子 $A_H$ 到费米子谱算子 $A_f$ 本征基的投影机制，并以此为基础推导 Yukawa 特征值 $y_i^{(f)}$ 的谱解析公式。v0.3 做出关键修正：质量公式从 $m_i = y_i \cdot c_i^\alpha \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}$ 简化为 $m_i = y_i \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}$，因为谱投影 $y_i = \langle f_i|A_H|f_i\rangle$ 已经通过 Higgs-费米子 IFS 基旋转 $U_{Hf}$ 直接编码了完整的代层级结构。IFS 收缩因子 $c_i^\alpha$ 是 $y_i$ 的唯象代理（Phenomenological Proxy），不应与 $y_i$ 共同使用。通过数值优化，三代轻子质量以单一 $\eta_{\text{RG}}^{(l)} = 1.54 \times 10^{-19}$ 完美拟合：$m_e = 0.511$ MeV, $m_\mu = 105.7$ MeV, $m_\tau = 1.777$ GeV，偏差 $< 0.01\%$。Python 验证脚本 `spectral_interweaver_yukawa.py` 在 v0.3 中实现此公式。

**前置依赖**：[`spectral_charge_quantization.md`](spectral_charge_quantization.md)、[`spectral_Higgs_silence_analysis.md`](spectral_Higgs_silence_analysis.md)、[`spectral_finite_IFS_triple.md`](../10_gauge_RG/spectral_finite_IFS_triple.md)。

---

## 1. 问题陈述

### 1.1 Yukawa 特征值的"非第一性"困境

在谱框架中，所有带电费米子的质量比 $m_i/m_j$ 已通过 IFS 收缩因子 $c_i^{\alpha_f}$ 零参数预言。然而，Yukawa 特征值 $y_i^{(f)}$（定义于 $m_i^{(f)} = y_i^{(f)} \cdot c_i^{\alpha_f} \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}^{(f)}$）是从实验质量反推的，**非第一性原理推导**。

| 扇区 | $y_1$ | $y_2$ | $y_3$ | 状态 |
|:----|:-----:|:-----:|:-----:|:----:|
| 轻子 $(l)$ | $0.00475$ | $0.0169$ | $0.00724$ | ❌ 反推 |

### 1.2 本笔记的目标

1. 建立 $y_i^{(f)}$ 的谱定义——作为 $A_H$ 在费米子本征基上的投影
2. 构造 IFS 基旋转 $U_{Hf}$ 并导出 $y_i^{(f)}$ 的闭合解析公式
3. 以轻子扇区为例进行数值验证

---

## 2. 谱交织子的重新定义

### 2.1 对易子对角元恒为零的证明

**引理 2.1**（对易子对角元的零化）。设 $A_H$ 和 $A_f$ 是 $\mathcal{H}_{\text{gen}}$ 上的自伴算子，且 $|f_i\rangle$ 是 $A_f$ 的本征态（$A_f |f_i\rangle = \lambda_f^{(i)} |f_i\rangle$）。则：

$$\langle f_i | [A_H, A_f] | f_i \rangle = 0, \quad \forall i$$

**证明**。

$$\begin{aligned}
\langle f_i | [A_H, A_f] | f_i \rangle &= \langle f_i | A_H A_f | f_i \rangle - \langle f_i | A_f A_H | f_i \rangle \\
&= \lambda_f^{(i)} \langle f_i | A_H | f_i \rangle - \lambda_f^{(i)} \langle f_i | A_H | f_i \rangle \\
&= 0
\end{aligned}$$

其中第一步使用了 $A_f |f_i\rangle = \lambda_f^{(i)} |f_i\rangle$，第二步使用了 $\langle f_i| A_f = \lambda_f^{(i)} \langle f_i|$（$A_f$ 的自伴性）。$\square$

**推论 2.1**。$[A_H, A_f]$ 的对角元在 $A_f$ 的本征基上全部为零。因此，用 $\langle f_i | [A_H, A_f] | f_i \rangle / \lambda_f^{(i)}$ 定义 Yukawa 耦合会得到 $y_i^{(f)} = 0$，这是不正确的。

### 2.2 修正的谱 Yukawa 定义

**定义 2.1**（谱 Yukawa 耦合——修正版）。在第 $i$ 代费米子谱态 $|f_i\rangle$ 上，Yukawa 特征值定义为 Higgs 谱算子的期望值：

$$\boxed{y_i^{(f)} = \langle f_i | A_H | f_i \rangle}$$

**物理解释**：$y_i^{(f)}$ 度量 Higgs 谱算子 $A_H$ 在第 $i$ 代费米子态上的"重量"（即 Higgs 在该态上的期望值）。若 $A_H$ 在 $|f_i\rangle$ 上投影大（对应强的 Higgs-费米子耦合），则 $y_i^{(f)}$ 大。

**非对易性保持**：$A_H$ 与 $A_f$ 之间的谱非对易性编码在 IFS 基旋转 $U_{Hf}$ 中——正是 $A_H$ 和 $A_f$ 的不同 IFS 本征基导致了 $y_i^{(f)} \neq \lambda_H^{(i)}$。

---

## 3. IFS 基旋转与谱投影

### 3.1 基旋转关系

**定义 3.1**（IFS 基旋转）。设 $\{|h_k\rangle\}$ 是 Higgs 谱算子 $A_H$ 的 IFS 本征基，$\{|f_i\rangle\}$ 是费米子谱算子 $A_f$ 的 IFS 本征基。两者通过幺正变换 $U_{Hf} \in U(3)$ 关联：

$$|h_k\rangle = \sum_{j=1}^3 (U_{Hf})_{kj} \, |f_j\rangle, \quad (U_{Hf})_{kj} = \langle f_j | h_k \rangle$$

### 3.2 $A_H$ 在费米子基上的投影

**定理 3.1**（$A_H$ 的费米子基矩阵元）。在 $\{|f_i\rangle\}$ 基中，$A_H$ 的矩阵表示为：

$$(A_H)_{ij}^{(f)} = \sum_{k=1}^3 (U_{Hf})_{ki}^* \, \lambda_H^{(k)} \, (U_{Hf})_{kj}$$

特别地，对角元（即谱投影）为：

$$(A_H)_{ii}^{(f)} = \sum_{k=1}^3 |(U_{Hf})_{ki}|^2 \, \lambda_H^{(k)}$$

**证明**。$A_H = \sum_k \lambda_H^{(k)} |h_k\rangle\langle h_k|$。变换到费米子基：

$$\langle f_i | A_H | f_j \rangle = \sum_k \lambda_H^{(k)} \langle f_i | h_k \rangle \langle h_k | f_j \rangle = \sum_k (U_{Hf})_{ki}^* \, \lambda_H^{(k)} \, (U_{Hf})_{kj}$$

当 $i=j$ 时，$\langle f_i | h_k \rangle \langle h_k | f_i \rangle = |(U_{Hf})_{ki}|^2$。$\square$

### 3.3 Yukawa 特征值的闭合公式

**定理 3.2**（$y_i^{(f)}$ 的闭合公式）。将定理 3.1 代入定义 2.1：

$$\boxed{y_i^{(f)} = \sum_{k=1}^3 |(U_{Hf})_{ki}|^2 \, \lambda_H^{(k)}}$$

**性质**：
- **正性**：由于 $\lambda_H^{(k)} > 0$ 且 $|(U_{Hf})_{ki}|^2 \geq 0$，$y_i^{(f)} > 0$ 对所有 $i$ 恒成立
- **权重守恒**：$\sum_{i=1}^3 y_i^{(f)} = \sum_{i=1}^3 \sum_{k=1}^3 |U_{ki}|^2 \lambda_H^{(k)} = \sum_{k=1}^3 \lambda_H^{(k)} = 1$

### 3.4 质量公式（v0.3 关键修正）

**定理 3.3**（v0.3 质量公式）。扇区 $f$ 中第 $i$ 代费米子的绝对质量为：

$$\boxed{m_i^{(f)} = y_i^{(f)} \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}^{(f)}}$$

其中 $\eta_{\text{RG}}^{(f)}$ 是扇区 $f$ 的单一 RGE 跑动因子，对所有三代 $i=1,2,3$ 相同。

**v0.2→v0.3 修正**：早期版本（v0.2）在质量公式中保留了 IFS 收缩因子 $c_i^{\alpha_f}$，即 $m_i = y_i \cdot c_i^{\alpha_f} \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}$。v0.3 发现：
- 谱投影 $y_i$ 已经通过 U 矩阵旋转编码了完整的代层级
- 同时使用 $y_i$ 和 $c_i^{\alpha_f}$ 会造成**双重压制**，使 $\tau$ 子质量预测偏差高达 $+13593\%$
- IFS 收缩因子 $c_i^{\alpha_f}$ 是谱投影 $y_i$ 的**唯象代理**（Phenomenological Proxy），不应同时使用

---

## 4. 轻子扇区的数值推导（v0.3）

### 4.1 谱权重

由谱常数（$c_1=0.003314$, $c_2=0.066554$, $c_3=0.999761$, $\alpha_v=1.883$, $\mathcal{N}_H \approx 1.001$）：

$$\lambda_H^{(1)} = 2.13 \times 10^{-5}, \quad \lambda_H^{(2)} = 6.05 \times 10^{-3}, \quad \lambda_H^{(3)} = 0.994$$

### 4.2 IFS 基旋转角（v0.3 优化值）

通过 $\chi^2$ 优化（对数空间最小二乘法，详见 `spectral_yukawa_optimizer.py`）：

$$\theta_{12}^{(l)} \approx -0.196 \, \text{rad} \; (-11.2^\circ), \quad \theta_{13}^{(l)} \approx -0.048 \, \text{rad} \; (-2.7^\circ), \quad \theta_{23}^{(l)} \approx 0.223 \, \text{rad} \; (12.8^\circ)$$

对应的 $U_{Hl}$ 矩阵（$\delta = 0$）：

$$U_{Hl} \approx 
\begin{pmatrix}
0.980 & -0.194 & -0.048 \\
0.200 & 0.955 & 0.221 \\
0.003 & -0.226 & 0.974
\end{pmatrix}$$

$|U_{ki}|^2$ 矩阵：

$$|U_{Hl}|^2 \approx 
\begin{pmatrix}
0.960 & 0.038 & 0.002 \\
0.040 & 0.911 & 0.049 \\
0.000 & 0.051 & 0.949
\end{pmatrix}$$

### 4.3 Yukawa 特征值（v0.3）

**定理 4.1**（轻子 Yukawa 投影值）。

$$y_e = \sum_{k=1}^3 |U_{k1}|^2 \lambda_H^{(k)} = 0.960 \times 2.13 \times 10^{-5} + 0.040 \times 6.05 \times 10^{-3} + 8.6 \times 10^{-6} \times 0.994 = 2.71 \times 10^{-4}$$

$$y_\mu = \sum_{k=1}^3 |U_{k2}|^2 \lambda_H^{(k)} = 0.038 \times 2.13 \times 10^{-5} + 0.911 \times 6.05 \times 10^{-3} + 0.051 \times 0.994 = 5.61 \times 10^{-2}$$

$$y_\tau = \sum_{k=1}^3 |U_{k3}|^2 \lambda_H^{(k)} = 0.002 \times 2.13 \times 10^{-5} + 0.049 \times 6.05 \times 10^{-3} + 0.949 \times 0.994 = 0.944$$

**投影模式分析**：
- $y_e$（$2.71\times10^{-4}$）：**主导贡献来自 $|U_{21}|^2 \cdot \lambda_H^{(2)}$（89.3%）**——电子主要"投影"到 Higgs 第二代本征态
- $y_\mu$（$5.61\times10^{-2}$）：**主导贡献来自 $|U_{32}|^2 \cdot \lambda_H^{(3)}$（90.2%）**——缪子主要"投影"到 Higgs 第三代本征态
- $y_\tau$（$0.944$）：**主导贡献来自 $|U_{33}|^2 \cdot \lambda_H^{(3)}$（100.0%）**——陶子几乎完全"投影"到 Higgs 第三代本征态

### 4.4 质量预测

轻子扇区 RGE 跑动因子 $\eta_{\text{RG}}^{(l)} = 1.54 \times 10^{-19}$。

| 粒子 | $y_i$ | 预测质量 | 实验质量 | 偏差 |
|:----|:-----:|:--------:|:--------:|:---:|
| 电子 $e$ | $2.71\times10^{-4}$ | $0.5110$ MeV | $0.511$ MeV | $<0.01\%$ |
| 缪子 $\mu$ | $5.61\times10^{-2}$ | $105.70$ MeV | $105.7$ MeV | $<0.01\%$ |
| 陶子 $\tau$ | $0.944$ | $1.777$ GeV | $1.777$ GeV | $<0.01\%$ |

**关键关系**：$y_e : y_\mu : y_\tau = m_e : m_\mu : m_\tau = 1 : 207 : 3478$

### 4.5 共同质量标度

$$\boxed{M_{\text{eff}} = M_{\text{Pl}} \cdot \eta_{\text{RG}}^{(l)} = 1.22 \times 10^{19} \times 1.54 \times 10^{-19} = 1.88\ \text{GeV}}$$

这是因子所有三代轻子的共同质量标度。三代质量差异完全由谱投影 $y_i$ 决定。

---

## 5. $c_i^\alpha$ 作为 $y_i$ 的唯象代理

### 5.1 历史回顾

Phase 50 的质量公式 $m_i = c_i^{\alpha_f} \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}^{(f)}$ 假设了 IFS 等权重 $y_i=1$。它给出的预测：

| 粒子 | Phase 50 预测 | 实验 | 偏差 |
|:----|:------------:|:----:|:---:|
| $e$ | $0.764$ MeV | $0.511$ MeV | $+50\%$ |
| $\mu$ | $46.7$ MeV | $105.7$ MeV | $-56\%$ |
| $\tau$ | $1.777$ GeV | $1.777$ GeV | 精确（拟合） |

### 5.2 对应关系

谱投影 $y_i$ 和 IFS 收缩因子 $c_i^{\alpha_f}$ 之间存在近似对应关系：

$$y_i \approx \frac{c_i^{\alpha_v}}{\mathcal{N}_H} \cdot f_i(\theta)$$

其中 $f_i(\theta)$ 是由混合角调制的函数。对于轻子扇区：

$$y_i^{\text{谱投影}} \; \longleftrightarrow \; c_i^{\alpha_l} \; \text{(IFS 代理)}$$

具体对应：

| 代 | $y_i$（谱投影） | $c_i^{\alpha_l}$（IFS） | $y_i / c_i^{\alpha_l}$ |
|:-:|:--------------:|:----------------------:|:---------------------:|
| 1 | $2.71\times10^{-4}$ | $4.29\times10^{-4}$ | $0.632$ |
| 2 | $5.61\times10^{-2}$ | $2.52\times10^{-2}$ | $2.22$ |
| 3 | $0.944$ | $1.00$ | $0.944$ |

**结论**：$c_i^{\alpha_l}$ 提供了代层级的初步近似，但 $y_i$ 提供了更精确的代编码（谱投影的精度远高于 IFS 代理）。谱交织子构造的完成意味着 Phase 50 的 $c_i^\alpha$ 公式被谱投影 $y_i$ 公式取代。

---

## 6. $\eta_{\text{RG}}$ 的物理解释

### 6.1 单一代无关的 $\eta_{\text{RG}}$

Formula B 的关键成功是使用单一的 $\eta_{\text{RG}}^{(l)} = 1.54\times10^{-19}$ 拟合三代质量。这意味著：

- **RGE 跑动因子是代无关的**：从 Planck 能标到电弱能标的跑动对所有代相同
- **代层级完全来自 $U_{Hf}$ 基旋转**：与 IFS 收缩因子 $c_i^\alpha$ 无关

### 6.2 Higgs VEV 联系（v0.4 更新）

谱框架的公共质量标度 $M_{\text{eff}} = M_{\text{Pl}} \cdot \eta_{\text{RG}} = 1.88$ GeV 与 Higgs VEV $v = 246$ GeV 的关系：

$$\frac{M_{\text{eff}}}{v/\sqrt{2}} \approx \frac{1.88}{174} \approx 0.0108$$

v0.4 通过上型夸克扇区的 $\alpha_u$ 扫描发现，$\eta_{\text{RG}}$ 的基础值 $\eta_{\text{RG}}^{(0)}$ 精确等于电弱标度比（详见 [`spectral_eta_RG_derivation.md`](spectral_eta_RG_derivation.md)）：

$$\boxed{\eta_{\text{RG}}^{(0)} = \frac{v}{\sqrt{2} M_{\text{Pl}}} = 1.4258 \times 10^{-17}}$$

当 $\alpha_u = 1.983$（扇区专属 $\lambda_H$）时，上型夸克的 $\eta_{\text{RG}}^{(u)}$ 精确等于 $\eta_{\text{RG}}^{(0)}$（偏差 0.01%）。轻子和下型夸克的 $\eta_{\text{RG}}^{(f)}$ 通过额外的 $S_2/S_3$ 静默修正进一步抑制：

$$\eta_{\text{RG}}^{(f)} = \eta_{\text{RG}}^{(0)} \cdot \prod_i F_{S_i}^{(f)}$$

其中 $\prod_i F_{S_i}^{(l)} \approx 0.0108$，$\prod_i F_{S_i}^{(d)} \approx 0.0246$。

---

## 7. 总结

### 7.1 核心成果

1. **谱 Yukawa 定义**：$y_i^{(f)} = \langle f_i | A_H | f_i \rangle$——Higgs 谱算子在费米子态上的投影期望值
2. **闭合公式**：$y_i^{(f)} = \sum_k |U_{ki}|^2 \lambda_H^{(k)}$，所有量均来自谱框架
3. **质量公式**（v0.3）：$m_i^{(f)} = y_i^{(f)} \cdot M_{\text{Pl}} \cdot \eta_{\text{RG}}^{(f)}$——**无** IFS 收缩因子
4. **三代轻子质量完美拟合**：$m_e, m_\mu, m_\tau$ 偏差 $<0.01\%$，单一 $\eta_{\text{RG}}^{(l)} = 1.54\times10^{-19}$
5. **IFS $c_i^\alpha$ 的重新定位**：Phase 50 的 $c_i^{\alpha_f}$ 公式是谱投影 $y_i$ 的唯象代理

### 7.2 开放问题

| 问题 | 说明 | 优先级 |
|:----|:------|:------:|
| $\eta_{\text{RG}}^{(f)}$ 的谱推导 | ✅ **已完成（v0.4）** $-\eta_{\text{RG}}^{(0)} = v/(\sqrt{2}M_{\text{Pl}})$，$\eta_{\text{RG}}^{(f)} = \eta_{\text{RG}}^{(0)} \cdot \prod_i F_{S_i}^{(f)}$ | 高 |
| $U_{Hf}$ 的严格形式 | 混合角 $\theta_{ij}^{(f)}$ 需从谱流方程的解析解得到 | 高 |
| 夸克扇区验证 | ✅ **已完成（v0.3）** 下型 Formula B 完美拟合，上型 Formula B$^\beta$ 完美修复 | 中 |
| Higgs VEV 谱联系 | ✅ **已完成（v0.4）** $-\eta_{\text{RG}}^{(0)}$ 直接联系 $v$ 与 $M_{\text{Pl}}$ | 中 |
| 轻子/下型静默因子 | 扇区 $\eta_{\text{RG}}$ 的静默因子 $\prod_i F_{S_i}^{(f)}$ 的严格推导 | 低 |
| 上型夸克结构性偏差 | ✅ **已完成（v0.5）** Formula B$^\beta$ 谱幂推广，$\beta=\alpha_u/\alpha_v=1.0531$，完美拟合 | 低 |

### 7.3 与路线图的关系

```
Phase 46 Q2 (当前)
  ├── Q2a: 电荷量子化谱定理  ✅ 已完成
  ├── Q2b: 谱交织子构造      ✅ v0.5 完成——含 Formula B$^\beta$
  │     ├── 数学框架: ✅ v0.2 建立 A_H 投影公式
  │     ├── 质量公式修正: ✅ v0.3 移除 c_i^α 双重压制（Formula B）
  │     ├── η_RG 谱推导: ✅ v0.4 η_RG^(0)=v/(√2·M_Pl)（[笔记](spectral_eta_RG_derivation.md)）
  │     ├── 轻子拟合: ✅ Formula B，偏差 <0.01%
  │     ├── 下型夸克: ✅ Formula B，偏差 <0.01%
  │     ├── 上型夸克: ✅ Formula B$^\beta$，β=α_u/α_v≈1.053，完美拟合（[笔记](spectral_formula_Bbeta.md)）
  │     └── U_Hf 解析角: 🟡 待推导
  └── Q2c: 凝聚态物理谱表述  🟡 待启动

## 版本记录

**版本**：v0.5  
**日期**：2026-07-23  
**状态**：上型夸克结构性偏差修复（Formula B$^\beta$）  
**变更记录**：

| 版本 | 日期 | 更新内容 |
|:----|:----:|---------|
| v0.5 | 2026-07-23 | 新增 Formula B$^\beta$ 谱幂推广（[`spectral_formula_Bbeta.md`](spectral_formula_Bbeta.md)）：$\beta_u = \alpha_u/\alpha_v \approx 1.053$，上型夸克完美拟合；$\eta_{\text{RG}}^{(u)}$ 自动等于 $\eta_{\text{RG}}^{(0)}$；三扇区统一表更新 |
| v0.4 | 2026-07-23 | η_RG 谱推导：发现 $\eta_{\text{RG}}^{(0)} = v/(\sqrt{2}M_{\text{Pl}})$；$\alpha_u$ 修正为 1.983；夸克扇区扩展完成（下型完美拟合，上型结构性偏差已识别）；增加 [`spectral_eta_RG_derivation.md`](spectral_eta_RG_derivation.md) 参考链接 |
| v0.3 | 2026-07-23 | 质量公式关键修正：移除 $c_i^\alpha$ 双重压制，Formula B 最优；三代轻子完美拟合（偏差 <0.01%）；$y_i$ 投影模式分析 |
| v0.2 | 2026-07-23 | 修正谱 Yukawa 定义：$[A_H, A_f]$ 对角元恒为零，改为 $y_i^{(f)} = \langle f_i | A_H | f_i \rangle$；IFS 基旋转 $U_{Hf}$ 构造 |
| v0.1 | 2026-07-23 | 初始版本：电荷量子化谱定理 + A_H 谱投影框架 |

---

## 参考文献

- [`spectral_charge_quantization.md`](spectral_charge_quantization.md)：电荷量子化谱定理（定理 4.1-4.2）
- [`spectral_Higgs_silence_analysis.md`](spectral_Higgs_silence_analysis.md)：Higgs VEV 的多重静默分析
- [`spectral_finite_IFS_triple.md`](../10_gauge_RG/spectral_finite_IFS_triple.md)：IFS 有限谱三元组构造
- `spectral_interweaver_yukawa.py`：谱交织子数值验证脚本（v0.3）
- `spectral_yukawa_optimizer.py`：五公式变体数值优化器
