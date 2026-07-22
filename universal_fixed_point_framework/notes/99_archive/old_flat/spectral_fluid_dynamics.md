# 谱流体动力学笔记

> **来源**: Paper VI — 通用不动点范畴框架 VI：谱流体动力学——从湍流谱到谱流几何（增强版 v2.0）
>
> **作者**: 王斌 | **版本**: v2.0 (2026-07-18)

---

## 1. 谱流体动力学公理 (B1-B3)

### 公理 B1：流体递归存在公理

对任意不可压流体系统 $F$，存在一个递归系统 $R_{\text{NS}} \in \mathbf{Rec}$，其 Koopman 算子 $U_t: f(\mathbf{v}_0) \mapsto f(\mathbf{v}(t))$ 满足半群性质 $U_{t+s} = U_t U_s$，且其谱像 $D(R_{\text{NS}}) = (\mathcal{H}_{\text{fluid}}, A_t, \sigma(A_t))$ 由速度场的 Koopman 生成元 $A_t = -\log U_t$ 给出。

### 公理 B2：对流-耗散分解公理

流体谱生成元 $A_t$ 的演化可分解为对易（保守）部分和反 Hermite（耗散）部分：

$$
\frac{d}{dt} A_t = [A_{\text{adv}}, A_t] - \nu \cdot \Delta_{\text{spec}} A_t + \mathcal{F}(t)
$$

其中：
- **$A_{\text{adv}}$**（对流谱生成元）：反 Hermite 算子，对应 $(\mathbf{v}\cdot\nabla)\mathbf{v}$
- **$\Delta_{\text{spec}}$**（谱拉普拉斯）：正定自伴算子，对应 $\nu\nabla^2$
- **$\mathcal{F}(t)$**（压力谱项）：由不可压约束谱投影消去

### 公理 B3：不可压谱约束公理

$$
\text{Tr}(A_t \cdot \mathcal{P}) = 0, \quad \forall t
$$

其中 $\mathcal{P}$ 是投影到散度自由模式的正交投影算子。压力项 $\mathcal{F}(t)$ 被唯一确定为保持该约束的校正项。

### 公理对应表

| 谱流体动力学 | 经典流体动力学 |
|-------------|---------------|
| $A_{\text{adv}}$ | $(\mathbf{v}\cdot\nabla)$ 算子 |
| $\Delta_{\text{spec}}$ | $\nabla^2$ |
| $\nu$ | 运动粘性系数 |
| $\mathcal{F}(t)$ | $-\nabla p$ |
| $\mathcal{P}$ | Helmholtz 投影 |
| $\text{Tr}(A_t \cdot \mathcal{P}) = 0$ | $\nabla \cdot \mathbf{v} = 0$ |

---

## 2. 谱 N-S 方程

### 核心方程

$$
\boxed{\frac{d}{dt} A_t = [A_{\text{adv}}, A_t] - \nu \cdot \Delta_{\text{spec}} A_t + \mathcal{F}(t)}
$$

- $A_t = -\log U_t$，$U_t$ 是速度场的 Koopman 算子
- $A_{\text{adv}}$ 是对流谱生成元（Koopman 算子下对流导数的生成元）
- $\Delta_{\text{spec}} = D(\nabla^2)$ 是粘性拉普拉斯的谱提升
- $\mathcal{F}(t)$ 是压力梯度项的谱表示

### 谱能量恒等式

$$
\frac{d}{dt} E(t) = \varepsilon_{\text{in}}(t) - \varepsilon_{\text{spec}}(t)
$$

其中：
- $E(t) = \frac{1}{2} \text{Tr}(A_t^2)$ —— 谱动能
- $\varepsilon_{\text{in}}(t) = \text{Tr}(A_t \cdot \mathcal{F}(t))$ —— 谱输入能率
- $\varepsilon_{\text{spec}}(t) = \nu \cdot \text{Tr}(\Delta_{\text{spec}} A_t \cdot A_t)$ —— 谱耗散率

对流项 $[A_{\text{adv}}, A_t]$ 在迹中对能量无贡献（循环性质 $\text{Tr}(A_t \cdot [A_{\text{adv}}, A_t]) = 0$）。

---

## 3. K41 湍流谱

### 标度解的唯一性

在惯性子区中，$A_t$ 的特征值 $\lambda_k$（波数 $k$ 处的谱分量）的唯一标度不变解为：

$$
\boxed{\lambda_k \propto k^{2/3}}
$$

对应的湍流动能谱：

$$
\boxed{E(k) \propto k^{-5/3}}
$$

### 推导要点

由能量通量 $\varepsilon_k = k \cdot \lambda_k^{3/2} = \text{const}$（惯性子区常数），设 $\lambda_k = C k^\alpha$，代入得 $1 + 3\alpha/2 = 0$，解得 $\alpha = -2/3$。谱框架中 $\lambda_k$ 对应涡旋翻转率 $\tau_k^{-1} \propto \varepsilon^{1/3} k^{2/3}$。由 $E(k) \propto k^{-1} \lambda_k^2$ 得 $E(k) \propto k^{-5/3}$。

### Kolmogorov 4/5 定律的谱版本

能量通量在惯性子区为常数：

$$
\varepsilon_k \equiv \text{Tr}(A_{\text{adv}} \cdot [A_{\text{adv}}, A_t])_k = \varepsilon = \text{const}
$$

等价于经典 $\langle (\delta v_\parallel)^3 \rangle = -\frac{4}{5} \varepsilon r$。

### 谱几何解释

K41 $-5/3$ 谱与引力 $1/r^2$ 律在本框架中源于同一数学结构——谱流在 $d=3$ 维物理空间中标度不变传播的必然结果：

| 量 | 引力 $1/r^2$ | 湍流 $k^{-5/3}$ |
|----|-------------|-----------------|
| 谱流方程 | $dA_t/dt = [A_{\text{GR}}, A_t]$ | $dA_t/dt = [A_{\text{adv}}, A_t]$ |
| 守恒量 | 谱通量 $\partial_r(r^{d-1}\rho)=0$ | 能量通量 $\varepsilon_k = \text{const}$ |
| 标度解 | $\rho \propto r^{-(d-1)}$ | $E(k) \propto k^{-5/3}$ |
| 几何来源 | $d=3$ 维空间通量守恒 | $d=3$ 维空间能量级串 |

---

## 4. 粘性耗散与谱截断

### 耗散子区谱行为

当 $k \gg k_\nu$，谱流方程退化为指数衰减：

$$
\frac{d}{dt} \lambda_k = -\nu k^2 \lambda_k \quad \Longrightarrow \quad \lambda_k(t) = \lambda_k(0) e^{-\nu k^2 t}
$$

### Kolmogorov 耗散尺度

谱截断波数由能量通量 $\varepsilon$ 与粘性 $\nu$ 决定：

$$
\boxed{k_\nu = \left(\frac{\varepsilon}{\nu^3}\right)^{1/4}}
$$

Kolmogorov 长度尺度 $\eta = 2\pi/k_\nu = (\nu^3/\varepsilon)^{1/4}$。

推导：惯性子区末端 $[A_{\text{adv}}, A_t] \sim \nu \Delta_{\text{spec}} A_t$，标度分析得 $k^{4/3} \sim \varepsilon^{1/3} \nu^{-1}$。

### 谱截断与 Planck 尺度截断的同构性

| 特征 | 湍流截断 | Planck 截断 |
|------|---------|------------|
| 截断机制 | $\nu k^2$ 耗散主导 | 谱离散化 $\lambda_{\max} \sim M_{\text{Pl}}$ |
| 截断尺度 | $k_\nu = (\varepsilon/\nu^3)^{1/4}$ | $k_{\text{Pl}} = M_{\text{Pl}}$ |
| 截断后行为 | $E(k) \propto e^{-\gamma k/k_\nu}$ | $\|A_{\text{GR}}\|_{\text{HS}} \to \lambda_{\max} < \infty$ |

两种截断都是谱动力学中的"奇点消解"机制——经典连续理论在小尺度发散，谱离散化或耗散机制在有限尺度截断。

### 谱耗散率恒等式

$$
\varepsilon_{\text{spec}} = \nu \cdot \text{Tr}(\Delta_{\text{spec}} A_t \cdot A_t) = \nu \int_0^\infty k^2 E(k) \, dk
$$

在惯性子区 $E(k) \propto k^{-5/3}$ 下，$k^2 E(k) \propto k^{1/3}$，积分由 $k_\nu$ 自然截断。

---

## 5. 湍流重整化群流

### 约化耦合常数

定义 $g(k)$ 为非线性对流强度与粘性耗散强度的比值：

$$
g(k) = \frac{\|[A_{\text{adv}}, A_t]\|_{\text{HS}}}{\nu k^2 \|A_t\|_{\text{HS}}}
$$

湍流 RG 流由 $g(k)$ 在波数尺度 $k$ 下的演化描述：

$$
\frac{dg}{d\ln k} = \beta_T(g)
$$

### $\beta$ 函数

一阶计算结果（与 Yakhot-Orszag 1986 一致）：

$$
\boxed{\beta_T(g) = \frac{dg}{d\ln k} = \left(\frac{3}{2} - n\right) g + O(g^2)}
$$

对 K41 谱 $n = 5/3$（即 $E(k) \propto k^{-5/3}$）：

$$
\boxed{\beta_T(g) = -\frac{1}{6} g + O(g^2)}
$$

### K41 谱为 UV 不动点

- $n < 5/3$：$\beta_T(g) > 0$（耦合随 $k$ 增长，流向 K41）
- $n = 5/3$：$\beta_T(g) = 0$（不动点）
- $n > 5/3$：$\beta_T(g) < 0$（耦合随 $k$ 减小，远离 K41）

K41 谱是惯性子区的唯一吸引不动点，$\beta_T'(g_*) = -1/6 < 0$ 保证线性稳定性。

### 与渐近安全引力的类比

| 特征 | 湍流 | 渐近安全引力 |
|------|------|-------------|
| UV 不动点 | K41 $E(k) \propto k^{-5/3}$ | $g_{\text{GR}} \to g_*$ |
| $\beta$ 函数 | $\beta_T(g) = -(1/6)g + O(g^2)$ | $\beta_{\text{GR}}(g) = (d-2)g + O(g^3)$ |
| 物理意义 | 高波数惯性子区标度不变 | 高能标度引力 UV 完备 |
| 截断 | $k_\nu$ 粘性截断 | $M_{\text{Pl}}$ Planck 截断 |

---

## 6. 谱 Reynolds 数

定义：

$$
\boxed{\text{Re}_{\text{spec}} = \frac{\|A_{\text{adv}}\|_{\text{HS}}}{\nu \cdot k_{\min}}}
$$

其中 $k_{\min}$ 为系统最小波数（最大尺度）。谱 Reynolds 数是对流项与粘性项强度的比值：

$$
\frac{\|[A_{\text{adv}}, A_t]\|_{\text{HS}}}{\|\nu \Delta_{\text{spec}} A_t\|_{\text{HS}}} \sim \frac{\|A_{\text{adv}}\|_{\text{HS}}}{\nu k_{\min}^2}
$$

经典 Reynolds 数 $\text{Re} = UL/\nu$ 通过 $U \propto \|A_{\text{adv}}\|_{\text{HS}}^{1/2}$、$L \propto 1/k_{\min}$ 对应。当 $\text{Re}_{\text{spec}}$ 超过临界阈值时，对流非线性项克服粘性阻尼，触发惯性子区建立和湍流级串。经典实验结果 $\text{Re}_{\text{crit}} \sim 2000$（管流）对应 $\text{Re}_{\text{spec}} > O(10^2)$。

---

## 7. 与谱热力学的联系 (Paper VII)

### 湍流谱熵

$$
S_{\text{turb}}(t) = -\sum_k p_k(t) \log p_k(t), \quad p_k(t) = \frac{|\langle \phi_k | A_t | \phi_k \rangle|}{\sum_j |\langle \phi_j | A_t | \phi_j \rangle|}
$$

在谱流方程下，湍流谱熵在统计稳态中达到极大值，惯性子区中 $dS_{\text{turb}}/dt \ge 0$。

### 谱 Onsager 倒易关系（湍流版本）

定义湍流谱流 $J_k = \text{Tr}(A_{\text{adv}} \cdot \dot{\rho}_t)_k$（波数 $k$ 处的能量通量）和谱力 $X_k = \partial(\nu k^2)/\partial k$（粘性梯度），Onsager 矩阵 $L_{kk'} = \partial J_k/\partial X_{k'}$ 满足对称性 $L_{kk'} = L_{k'k}$。

### 湍流涨落定理

在非平衡湍流稳态下，谱熵产生 $\Sigma_{\text{turb}} = \Delta S_{\text{turb}}$ 满足：

$$
\frac{P(\Sigma_{\text{turb}} = \sigma)}{P(\Sigma_{\text{turb}} = -\sigma)} = e^{\sigma}
$$

物理意义：湍流能量级串可视为"热力学"过程——能量从大尺度（低温热库）注入，通过惯性子区（准绝热过程）级串到小尺度（高温热库）耗散。

### 热力学量对照表

| 谱热力学 (Paper VII) | 谱流体动力学 |
|---------------------|-------------|
| $G = \sum_i g_i A_{F,i}$（全生成元） | $G_{\text{fluid}} = A_{\text{adv}}$（对流生成元） |
| $A_t$ 谱熵 $S_{\text{spec}}$ | $S_{\text{turb}} = -\sum_k p_k \log p_k$ |
| Onsager 力 $X_i = g_i$ | $X_k = \partial(\nu k^2)/\partial k$ |
| 谱流 $J_i = \text{Tr}(A_{F,i} \dot{\rho}_t)$ | $J_k = \text{Tr}(A_{\text{adv}} \cdot \dot{\rho}_t)_k$ |
| 涨落定理 $P(\Sigma)/P(-\Sigma) = e^\Sigma$ | 湍流涨落定理 |
| 平衡态：$[A_{F,i}, \rho_t] = 0$ | K41 惯性子区平衡湍流 |

---

## 8. 数值验证 (6/6 通过)

| 编号 | 检验名称 | 核心内容 | 状态 |
|------|---------|---------|------|
| 1 | N-S 谱等效性 | 谱 N-S 方程在连续极限退化为经典 N-S | ✅ |
| 2 | K41 谱斜率 | $\lambda_k \propto k^{2/3}$，$E(k) \propto k^{-5/3}$ | ✅ |
| 3 | 粘性截断尺度 | $k_\nu = (\varepsilon/\nu^3)^{1/4}$ | ✅ |
| 4 | RG $\beta$ 函数不动点 | $\beta_T(g_*) = 0$ 在 $n=5/3$ | ✅ |
| 5 | 能量级串守恒 | $\varepsilon_k = \text{const}$ 在惯性子区 | ✅ |
| 6 | 谱 Reynolds 数阈值 | $\text{Re}_{\text{spec}} > \text{Re}_{\text{crit}}$ 触发湍流 | ✅ |

所有 6 项概念验证均通过。完整的 DNS 验证（使用拟谱法 DNS 对标）留待后续工作。

---

## 9. 开放问题 (6 项)

1. **间歇性与高阶统计量**。当前框架仅给出 K41 平均谱。间歇性修正（$E(k) \propto k^{-5/3 - \mu}$，$\mu \approx 0.03-0.05$）对应高阶对易子 $[A_{\text{adv}}, [A_{\text{adv}}, A_t]]$ 的贡献。

2. **可压缩湍流**。需引入密度谱生成元 $\rho_{\text{spec}}$ 和声学模式 $A_{\text{acoustic}}$，公理 B3 需扩展。

3. **MHD 湍流**。需磁场谱生成元 $A_B$ 和对易关系 $[A_{\text{adv}}, A_B] \approx [\mathbf{v}\times\mathbf{B}, \mathbf{B}]$，对应 $A_{\text{EM}}$ 生成元的推广。

4. **壁湍流与边界层**。固壁边界条件在谱框架中对应 $\mathbf{Rec}$ 的边界对象——$A_t$ 在某些本征模上的约束。对数律 $u^+ \propto \log y^+$ 可能对应谱流方程的边界层解。

5. **直接数值模拟 (DNS) 验证**。完整数值验证（拟谱法 DNS 对标）是关键下一步。现有概念验证 6/6 通过。

6. **湍流-引力深度统一**。$k^{-5/3}$ 与 $1/r^2$ 的谱同源性暗示两者都是 $d=3$ 维空间中谱流标度不变的投影，可能涉及 AdS/CFT 的湍流版本。

---

## 核心结论汇总

| 编号 | 结论 | 定理 | 意义 |
|------|------|------|------|
| C1 | N-S 方程等价于谱流方程 | 定理 3.1–3.2 | 经典流体嵌入谱动力学 |
| C2 | K41 $-5/3$ 谱为谱流标度解 | 定理 4.2 | 湍流谱的第一性原理推导 |
| C3 | 谱截断 $k_\nu$ 与 Planck 截断同构 | 定理 5.3 | 跨领域统一结构 |
| C4 | 湍流 $\beta$ 函数 $\beta_T = -(1/6)g$ | 定理 6.1 | RG 框架的谱版本 |
| C5 | 谱耗散率 $\varepsilon_{\text{spec}} = \nu\text{Tr}(\Delta_{\text{spec}}A_t\cdot A_t)$ | 定理 3.3 | 能量级串的迹公式 |
| C6 | 湍流熵增 $dS_{\text{turb}}/dt \ge 0$ | 定理 7.1 | 热力学第二定律的湍流版本 |

---

*本笔记基于 Paper VI「通用不动点范畴框架 VI：谱流体动力学——从湍流谱到谱流几何」(v2.0, 2026-07-18) 整理，其独特内容（B1-B3 公理、湍流 RG β 函数、谱 Reynolds 数）来自临时文档 Paper XIII 的合并。*
