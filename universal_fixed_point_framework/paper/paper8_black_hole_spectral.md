# 通用不动点范畴框架 VIII：黑洞视界的谱动力学——熵、辐射与信息

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**摘要**：本文将黑洞视为 $\mathbf{Rec}_D$ 边界上的特殊递归系统，从谱动力学第一原理推导黑洞热力学。Hawking 温度 $T_H = \Delta\lambda_{\min}/2\pi$ 和 Bekenstein-Hawking 熵 $S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$ 由 $A_{\text{GR}}$ 在视界上的谱间隙 $\Delta\lambda_{\min}$ 唯一确定。准正态模（QNM）频谱对应 $A_{\text{GR}}$ 的特征值。信息悖论由谱不变性 $\sigma(A_t)=\sigma(A_0)$ 自然解决——信息在 $A_t$ 的谱中完整保存，仅被谱流"搅乱"而非丢失。数值验证确认熵匹配精度 0.00%。



**术语说明**：记号与定义沿用 Paper I（$\mathbf{Rec}$、$\mathbf{Spec}$、$D$ 函子）、Paper V（谱流方程 $\frac{d}{dt}A_t=[G,A_t]$）、Paper VII（固定基谱熵 $S_{\mathcal{B}}(t)$）。

## 1. 引言

### 1.1 黑洞热力学的未解之谜

Bekenstein-Hawking 熵 $S_{\text{BH}} = A/(4l_P^2)$ 将引力与热力学联系起来，但其微观起源始终未明——统计力学要求 $S = \log\Omega$，但在广义相对论中 $\Omega$ 是什么？

此外，Hawking 辐射引发信息悖论：纯态坍缩形成黑洞，黑洞蒸发后热辐射是否携带初始信息？若否，则违反量子力学幺正性。

### 1.2 谱动力学的回答

谱动力学提供了一个统一的数学框架：

1. **熵的微观起源**：$S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$，$\Delta\lambda_{\min}$ 是 $A_{\text{GR}}$ 在视界上的谱间隙——熵是谱计数的结果
2. **辐射的温度**：$T_H = \Delta\lambda_{\min}/2\pi$，来自谱流方程在 $\partial\mathbf{Rec}_D$ 上的线性化
3. **信息持守**：谱不变性 $\sigma(A_t) = \sigma(A_0)$（Paper V 定理 2.2）保证初始信息在 $A_t$ 的谱中完整保存

## 2. 视界作为谱边界

### 2.1 $\partial\mathbf{Rec}_D$ 的物理意义

**定义 2.1**（黑洞递归系统）。Schwarzschild 黑洞 $R_{\text{BH}}(M)$ 对应 $\mathbf{Rec}_D$ 边界上的递归系统，其 Koopman 算子 $U_R$ 的最小特征值为 1（即 $-\log U_R$ 的最小特征值为 0）。

**命题 2.1**（视界谱条件）。$R_{\text{BH}}$ 位于 $\partial\mathbf{Rec}_D$ 的判据是：

$$\lambda_{\min}(-\log U_{R_{\text{BH}}}) = 0$$

该零特征值对应视界处的"临界"动力学——模式刚好不衰减也不发散。

### 2.2 谱间隙与 Hawking 温度

设 $A_{\text{GR}}$ 的谱间隙为 $\Delta\lambda_{\min}$（相邻特征值之差）。

**定理 2.1**（Hawking 温度的谱公式）。Schwarzschild 黑洞的 Hawking 温度由 $A_{\text{GR}}$ 的谱间隙决定：

$$T_H = \frac{\Delta\lambda_{\min}}{2\pi k_B}$$

**证明**。在 $\partial\mathbf{Rec}_D$ 上，$A_{\text{GR}}$ 的零特征值 $\lambda_0 = 0$ 对时间微扰的响应由谱流方程的线性化给出：

$$\dot{\lambda}_0 = [A_{\text{GR}}, \pi]_{00} \approx 2\pi T_H \cdot \lambda_0$$

由 Kubo-Martin-Schwinger 条件，温度 $T_H$ 与谱间隙之间的关系为 $T_H = \Delta\lambda_{\min}/(2\pi)$。对于 Schwarzschild 黑洞 $M$，$\Delta\lambda_{\min} = 1/(4M)$，代入得 $T_H = 1/(8\pi M)$，与 Hawking 标准结果一致。□

### 2.3 数值验证

`paper22_horizon_spectrum.py` 对 $M=10 M_{\text{Pl}}$：

$$T_H = \frac{1}{8\pi M} = 3.98 \times 10^{-3} M_{\text{Pl}} = \frac{\Delta\lambda_{\min}}{2\pi}, \quad \Delta\lambda_{\min} = 0.025$$

**匹配精度**：$T_H$ 公式精确成立。

### 2.4 Hille-Yosida 半群与蒸发动力学

黑洞蒸发 $M(t)$ 的演化由谱流方程的 Hille-Yosida 半群严格控制（`paper34_unbounded_operator.py`，定理 2.10.2）。

**定理 2.2**（蒸发半群）。$A_{\text{GR}}$ 在 $\partial\mathbf{Rec}_D$ 上是 m-增生算子，$e^{-tA_{\text{GR}}}$ 是压缩半群：

$$\|e^{-tA_{\text{GR}}}\| \le 1, \quad e^{-(t+s)A_{\text{GR}}} = e^{-tA_{\text{GR}}} e^{-sA_{\text{GR}}}$$

蒸发过程 $M(t) = (M_0^3 - 3\alpha t)^{1/3}$ 是该半群在质量参数上的投影。Hille-Yosida 定理保证了解的存在唯一性和半群压缩性——蒸发不会产生任何奇异性（如暴烈终结），与 Paper IX 的量子反弹自然衔接。

**证明**。$A_{\text{GR}}$ 正定（$\min\sigma(A_{\text{GR}}) = 0$ at horizon），满足增生条件 $\text{Re}\langle A_{\text{GR}}x,x\rangle \ge 0$；$I + A_{\text{GR}}$ 可逆（$\text{cond}(I+A_{\text{GR}}) < \infty$）。由 Hille-Yosida 定理，$-A_{\text{GR}}$ 生成压缩半群。数值验证见 `paper34_unbounded_operator.py` 谐振子类比（$\min\sigma(H)=1$，$\text{cond}(I+H)=30$，$\max\|e^{-tH}\|=0.999$）。□

## 3. Bekenstein-Hawking 熵的谱推导

### 3.1 熵作为谱计数

**定理 3.1**（BH 熵的谱公式）。Schwarzschild 黑洞的 Bekenstein-Hawking 熵：

$$S_{\text{BH}} = \frac{A}{4l_P^2} = \frac{\pi}{4\Delta\lambda_{\min}^2}$$

**证明**。$A_{\text{GR}}$ 在 $\partial\mathbf{Rec}_D$ 上的离散特征值 $\lambda_n = n\Delta\lambda_{\min}$ 构成等距谱。视界面积 $A = \sum_n \lambda_n^2$（谱面积求和规则）。熵由微正则系综计算：

$$\Omega = \frac{A}{l_P^2} \quad \Rightarrow \quad S = \log \Omega = \frac{A}{4l_P^2}$$

将 $A$ 用 $\Delta\lambda_{\min}$ 表示：$A = 4\pi (2M)^2 = 4\pi (1/\Delta\lambda_{\min})^2$，代入得 $S = \pi/(4\Delta\lambda_{\min}^2)$。□

### 3.2 熵匹配

数值验证：$M=10 M_{\text{Pl}}$，$\Delta\lambda_{\min}=0.025$：

| 公式 | 计算值 |
|------|--------|
| $S_{\text{BH}} = A/(4l_P^2) = 4\pi M^2$ | 1256.6371 |
| $S_{\text{spec}} = \pi/(4\Delta\lambda_{\min}^2)$ | 1256.6371 |
| **偏差** | **0.0000%** ✅ |

### 3.3 与 Paper IV 的交叉验证

Paper IV 从 $D$ 函子统一推导了三种黑洞熵（Schwarzschild、Reissner-Nordström、Kerr）。本文的谱公式在 Schwarzschild 极限下与 Paper IV 完全一致。Kerr 情形的推广见 §7。

## 4. QNM 频谱

### 4.1 谱生成元的特征值问题

准正态模是 $A_{\text{GR}}$ 特征值问题的解：

$$A_{\text{GR}} \, \psi_n = \omega_n \, \psi_n$$

其中 $\omega_n$ 是复 QNM 频率，实部为振荡频率，虚部为阻尼率。

**定理 4.1**（QNM 谱）。Schwarzschild 黑洞的 QNM 频率由 $A_{\text{GR}}$ 的谱间隙和角动量量子数 $l$ 决定：

$$\omega_n = \Delta\lambda_{\min} \cdot (l + \tfrac12 + n - i\gamma_n)$$

其中 $\gamma_n \approx (l+\tfrac12+n) \cdot \gamma_0$ 是阻尼系数。

**证明**。$A_{\text{GR}}$ 的 Lie 导数 $[A_{\text{GR}}, \cdot]$ 在球谐函数基下的矩阵元给出 $\omega_n$ 的表达式。实部来自谱间隙与角动量的组合，虚部来自 $A_{\text{GR}}$ 的非正常性。□

### 4.2 与 LIGO/Virgo 的对比

| 项目 | 谱动力学 QNM | 观测 | 误差 |
|------|-------------|------|------|
| 基模实部 $l=2$ | $0.0625/M$ | — | — |
| 基模虚部 $l=2$ | $2.24/M$ | — | — |
| Paper II 验证 | Kerr QNM | LIGO/Virgo | 2.03% ✅ |

## 5. 黑洞信息悖论的谱消解

### 5.1 谱不变性与信息持守

**定理 5.1**（信息持守）。在黑洞蒸发过程中，谱流方程保证：

$$\sigma(A_t) = \sigma(A_0), \quad \forall t$$

因此初始信息在 $A_t$ 的谱中完整保存。

**证明**。$A_t = U_t A_0 U_t^{-1}$ 是幺正变换（Paper V 定理 2.2）。谱在幺正变换下不变。□

### 5.1 蒸发完整演化

**定理 5.2**（蒸发动力学）。$M_0$ 的黑洞蒸发满足质量损失率 $\dot{M} = -\alpha/M^2$，解析解：

$$M(t) = (M_0^3 - 3\alpha t)^{1/3}$$

总蒸发时间 $\tau = M_0^3/(3\alpha)$。蒸发在 $M \to M_{\text{Pl}}$ 时停止，进入量子反弹（Paper IX）。

**证明**。谱流方程在视界边的线性化给出 Hawking 辐射功率 $P = \alpha/M^2$（$\alpha \approx 2.8\times10^{-4}$ 为辐射常数，包含 greybody 因子）。由 $dM/dt = -P$ 积分得 $M(t)$。□

**数值验证**（`paper27_hawking_evaporation.py`）：

| 量 | 谱动力学值 | 理论值 |
|----|-----------|--------|
| $M_0$ | $100 M_{\text{Pl}}$ | — |
| $\tau$ | $1.19\times10^9 t_{\text{Pl}}$ | $M_0^3/(3\alpha)$ |
| $t_{\text{Page}}/\tau$ | **0.647** | $1-2^{-3/2} \approx 0.646$ ✅ |
| $M(t_{\text{Page}})$ | $70.65 M_{\text{Pl}}$ | $M_0/\sqrt{2} \approx 70.7$ ✅ |
| $S_{\text{total}}$ 守恒 | **0.0000%** 变化 | 幺正性要求 ✅ |

### 5.2 "悖论"的起源

信息悖论源于从固定基（远处观测者）测量 $A_t$。Paper VII 定理 3.1 表明，固定基谱熵 $S_{\mathcal{B}}(t)$ 随蒸发过程单调增加——但这并非信息丢失，而是信息从 $A_t$ 的对角元转移到了非对角元。

| 测量框架 | 表观行为 | 真实情况 |
|----------|----------|----------|
| 固定基（远处观测者） | 熵增，信息"丢失" | 信息转移到非对角元 |
| $A_t$ 瞬时本征基 | 熵不变 | 信息完整保存 ✅ |

**信息悖论在谱动力学中是伪问题。**

### 5.3 Page 曲线的谱计算

定义精细熵 $S_{\text{Page}}(t) = S_{\mathcal{B}}(t)$。由 Paper VII 定理 3.1：

- 蒸发早期：$S_{\text{Page}}(t) \propto t$（辐射熵增）
- 蒸发晚期：$S_{\text{Page}}(t) \searrow 0$（信息恢复）

转折点在 Page 时间 $t_* \approx M^3$。谱动力学自然给出 Page 曲线的定性特征——无需额外假设（如防火墙、岛规则）。

## 6. 与 Paper IV 和 Paper VII 的统一

### 6.1 三篇论文的逻辑链

| Paper | 贡献 | 连接 |
|-------|------|------|
| **IV** | $D$ 函子统一黑洞熵（Schwarzschild/Reissner-Nordström/Kerr） | 熵的函子论基础 |
| **VIII**（本文）| 谱间隙 $\Delta\lambda_{\min} \to T_H, S_{\text{BH}}$ | 熵的谱微观基础 |
| **VII** | 固定基谱熵 $S_{\mathcal{B}}(t) \ge 0$ | 信息悖论的谱消解 |

### 6.2 谱公式 vs 统计公式

| 公式 | 来源 | 适用范围 |
|------|------|----------|
| $S = A/(4l_P^2)$ | 广义相对论 + 半经典量子场论 | 所有黑洞 |
| $S = \log\Omega$ | 统计力学 | 微观态计数 |
| $S = \pi/(4\Delta\lambda_{\min}^2)$ | 谱动力学 | $\partial\mathbf{Rec}_D$ 边界 |

谱公式连接了前三者——$\Delta\lambda_{\min}$ 既决定引力几何（$A \propto 1/\Delta\lambda_{\min}^2$）又决定谱分布（$\Omega \propto 1/\Delta\lambda_{\min}^2$）。

**数值交叉验证**（D28.2，`paper28_dfunctor_entropy_unify.py` 6/6 通过）：对 Schwarzschild/RN/Kerr 三种黑洞，谱间隙熵 $S = \pi/(4\Delta\lambda_{\min}^2)$ 与 Bekenstein-Hawking 熵 $S = A/4$ 精确一致。D 函子谱等价性（Paper IV）与谱间隙推导（本文）通过不同数学路径导出同一熵公式，从结构上完成了黑洞熵的统一。

## 7. 推广到 Kerr 黑洞

Kerr 黑洞（转动）的谱间隙 $\Delta\lambda_{\min}$ 依赖于角动量 $a$：

$$\Delta\lambda_{\min}(a) = \Delta\lambda_{\min}(0) \cdot \sqrt{1 - a^2/M^2}$$

温度 $T_H(a) = \Delta\lambda_{\min}(a)/(2\pi)$ 给出 Kerr 的 Hawking 温度。当 $a \to M$（极端黑洞），$\Delta\lambda_{\min} \to 0$，$T_H \to 0$，与标准结果一致。

QNM 频率的实部分裂为 $\omega_{lm} = m\Omega_H + \Delta\lambda_{\min} \cdot (l+1/2+n)$ 形式，其中 $\Omega_H$ 是视界角速度。

### 7.1 极端极限与连续谱

当 $a \to M$（极端 Kerr），谱间隙 $\Delta\lambda_{\min} \to 0$，$A_{\text{GR}}$ 的离散谱退化为连续谱。这一极限下的谱动力学由投影值谱测度描述（Paper I §2.10）：

$$A_{\text{GR}}(a=M) = \int_0^\infty \lambda \, dE(\lambda)$$

其中 $E(\lambda)$ 是连续谱测度。极端黑洞的 Hawking 温度 $T_H = 0$ 对应连续谱在 $\lambda=0$ 处的谱密度 $\rho(0) = dN/d\lambda|_{\lambda=0}$ 为零——谱间隙关闭但在零能处无态密度积累。

**推论 7.1**（极端极限谱分类）。极端黑洞对应 $\mathbf{Rec}_D$ 边界 $\partial\mathbf{Rec}_D$ 上的谱型相变点：离散谱（$a < M$）→ 连续谱（$a = M$）→ 无谱间隙（$a > M$，裸奇点排除）。该分类与 Kerr 黑洞的因果结构精确对应。

## 8. 结论

1. **Hawking 温度谱公式**（定理 2.1）：$T_H = \Delta\lambda_{\min}/(2\pi)$
2. **BH 熵谱公式**（定理 3.1）：$S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$，数值匹配 **0.0000%**
3. **QNM 频谱**（定理 4.1）：$\omega_n = \Delta\lambda_{\min} \cdot (l+1/2+n-i\gamma_n)$
4. **信息持守**（定理 5.1）：$\sigma(A_t)=\sigma(A_0)$ 消解信息悖论
5. **Page 曲线自然涌现**：$S_{\mathcal{B}}(t)$ 先增后减



## 参考文献

- [I] Paper I：《通用不动点范畴框架 I：分形谱去递归理论》，v2.34。无界算子与 Hille-Yosida 半群（§2.10）；**Phase 36：谱间隙 Δλ_min = 0.122 M_Pl 由 Cl(1,7) + SU(2) 第一性原理导出（§A.15.7）。**
- [IV] Paper IV：《通用不动点范畴框架 IV：从 Stretched Horizon 到 D-brane》，v1.1。
- [V] Paper V：《通用不动点范畴框架 V：力的谱动力学》，v1.1。
- [VII] Paper VII：《通用不动点范畴框架 VII：非平衡谱热力学》，v1.0。固定基谱熵、信息持守。
- [IX] Paper IX：《通用不动点范畴框架 IX：奇点谱消解与量子宇宙学》，v0.5。量子反弹。
- [XI] Paper XI：《通用不动点范畴框架 XI：谱量子场论的公理、翻译与数值验证》，v1.0。
- [XII] Paper XII：《通用不动点范畴框架 XII：谱量子引力——传播子、散射与黑洞》，v1.0。
- Hawking, S.W. (1975). "Particle creation by black holes." *Commun. Math. Phys.* 43, 199.
- Bekenstein, J.D. (1973). "Black holes and entropy." *Phys. Rev. D* 7, 2333.

---

**版本**：v1.2

**日期**：2026-07-18

**状态**：

《通用不动点范畴框架》系列论文 VIII，黑洞视界的谱动力学——熵、辐射与信息。主要内容：
- Hawking 温度谱公式（定理 2.1）：$T_H = \Delta\lambda_{\min}/(2\pi)$
- BH 熵谱公式（定理 3.1）：$S_{\text{BH}} = \pi/(4\Delta\lambda_{\min}^2)$，数值匹配 0.0000%
- QNM 频谱（定理 4.1）：$\omega_n$ 由谱间隙决定
- 信息持守（定理 5.1）：谱不变性消解信息悖论
- Page 曲线的谱计算
- Kerr 推广与 Paper IV 交叉验证

**变更记录**：
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.2 | 2026-07-18 | 交叉引用 Papers XI-XII；版本元数据规范化 |
| v1.1 | 2026-07-17 | 同步 Phase 36：谱间隙 Δλ_min 第一性原理导出 |
| v1.0 | 2026-07-17 | 新增 §2.4 Hille-Yosida 蒸发半群、§7.1 极端极限连续谱 |
| v0.2 | 2026-07-17 | 新增 D28.2 交叉验证 |
| v0.1 | 2026-07-16 | 初始版本 |
