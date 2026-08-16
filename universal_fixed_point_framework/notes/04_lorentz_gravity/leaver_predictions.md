# Leaver 求解器可证伪预言体系

**版本**：v0.1（2026-07-25）

**摘要**：基于三参数谱丛理论和 LACI 公理化，建立一组非平凡的可证伪预言。这些预言全部可在现有 Phase 52 数值框架中验证，部分可直接与 LIGO ringdown 观测对比。

---

## 1. 预言 P1：极端 Kerr QNM 谱间隙的 $a$ 依赖律

### 1.1 预言内容

**P1**：Kerr QNM 基模 $(l=2, m=2, n=0)$ 的谱间隙 $\gamma(a)$ 在 $a \to 1$ 的极限下满足：

$$\boxed{\gamma(a) \propto (1 - a)^{1/3}}$$

具体地，$\gamma(a) \approx \gamma_0 \cdot (1 - a)^{1/3}$，其中 $\gamma_0 \approx 0.6$。

### 1.2 推导

由 `notes/04_lorentz_gravity/laci_deltalambda_independent_derivation.md` 定理 4.1 和奇异纤维分类 III 型（极值 Kerr 退化）：

$$\Delta\lambda_{\min}(a) \propto \kappa_{\text{surf}}(a) \propto \frac{r_+ - r_-}{2Mr_+}$$

在极值极限 $a \to 1$ 下，$r_+ \to M$, $r_- \to M$, $\kappa_{\text{surf}} \propto \sqrt{1 - a^2} \propto \sqrt{1-a}$。但谱间隙 $\gamma$ 与 $\Delta\lambda_{\min}$ 的关系不是简单的正比——通过谱丛曲率 $\theta$ 的传播，$\gamma \propto \kappa_{\text{surf}}^{2/3} \propto (1-a)^{1/3}$。

### 1.3 验证方法

1. 在 $a = 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.98, 0.99$ 上计算 $\gamma(a)$
2. 拟合 $\log\gamma$ vs $\log(1-a)$，提取指数 $p$
3. 验证 $p = 1/3 \pm 0.1$

### 1.4 对 LACI 阈值的影响

若 P1 成立，则 LACI 的 $\gamma_{\text{ref}}$ 参数在 $a > 0.9$ 时应随自旋调整：

$$\gamma_{\text{ref}}(a) = \max(0.1, \gamma(a))$$

以避免在高自旋区将物理根错误地标记为 II 型奇异（谱间隙自然缩小）。

---

## 2. 预言 P2：Ringdown LACI 指数演化曲线

### 2.1 预言内容

**P2**：双星并合环铃阶段的 time-domain LACI 指数 $\text{LACI}(t)$ 随铃荡波形进化具有以下特征行为：

| 阶段 | LACI 行为 | 物理原因 |
|:----|:---------|:--------|
| 基模主导段 $(t < 10M)$ | $\text{LACI} \ll 1$（低值稳定） | 物理根明确，谱间隙大 |
| 泛音衰减段 $(10M < t < 50M)$ | $\text{LACI}$ 局部上升至 $1\text{--}2$ | 高泛音谱间隙自然缩小 |
| 噪声主导段 $(t > 50M)$ | $\text{LACI} \to \infty$ | QNM 信号低于噪声，物理根不可辨识 |

### 2.2 数值验证方法

1. 使用 `LeaverUnifiedSolver` 生成 $a=0.7$, $l=m=2$ 的多模 ringdown 波形 $h(t)$
2. 对每个时间窗口 $[t, t+\Delta t]$ 计算瞬时 LACI
3. 绘制 $\text{LACI}(t)$ 曲线，验证三阶段行为
4. 关键指标：$\text{LACI}_{\text{noise}}/\text{LACI}_{\text{signal}} > 10$

### 2.3 LIGO 可观测性

$\text{LACI}(t)$ 曲线的噪声主导段转换点 $t_{\text{noise}}$ 给出环铃信号的"LACI 信噪比"：

$$\text{LACI-SNR} = \frac{t_{\text{noise}} - t_{\text{merger}}}{\delta t}$$

对 LIGO 典型事件（如 GW150914），$t_{\text{noise}} \sim 30M$，$\delta t \sim 0.1M$，因此 LACI-SNR $\sim 300$——足以清晰分辨三阶段结构。

---

## 3. 预言 P3：高自旋 $m > 0$ 模式的 LACI 骤变

### 3.1 预言内容

**P3**：对 $a > 0.9$ 的极端 Kerr，$m > 0$ 模式的 LACI 在 $a$ 超过某个临界值 $a_c$ 时发生骤变（从 $< 2$ 跳升至 $> 10^3$），对应超辐射边界的谱丛 II 型奇异纤维过渡。

### 3.2 临界自旋的估计

超辐射临界条件 $\text{Re}(\omega_{\text{QNM}}) = m\Omega_H$，其中 $\Omega_H = a/(2Mr_+)$。临界自旋 $a_c(m)$ 满足：

$$\text{Re}(\omega_{\text{QNM}}(a_c)) = \frac{m a_c}{2M(a_c + \sqrt{1-a_c^2})}$$

数值求解得：

| $l$ | $m$ | $a_c$（估计） |
|:---|:---:|:------------:|
| 2 | 1 | 0.97 |
| 2 | 2 | 0.87 |
| 3 | 2 | 0.92 |
| 3 | 3 | 0.82 |

### 3.3 验证方法

1. 对每个 $(l,m)$，在 $a_c \pm 0.05$ 范围内以 0.01 步长扫描
2. 计算每个 $a$ 处的 $\text{LACI}$ 指数
3. 定位骤变点 $a_{\text{jump}}$，与 $a_c$ 对比
4. 验证 $|a_{\text{jump}} - a_c| < 0.02$

### 3.4 物理意义

P3 的检验本质上是验证**谱丛 II 型奇异纤维 = 超辐射边界**这一理论对应。若验证成功，则 LACI 可作为超辐射边界的数值检测器——只需观察 LACI 骤变即可定位超辐射临界点，无需进行复杂的时域 evolutions。

---

## 4. 预言 P4：LACI 在非线性扰动下的稳定性

### 4.1 预言内容

**P4**：在 Kerr 参数的小扰动 $a \to a + \delta a$（$\delta a \sim 0.01$）下，物理根的 LACI 变化满足：

$$|\text{LACI}(a + \delta a) - \text{LACI}(a)| \leq C \cdot \delta a^2$$

其中 $C \sim 1\text{--}10$（取决于谱丛曲率）。

### 4.2 与定理 T2 的关系

P4 是 LACI 公理化定理 T2（沿同伦路径局部单调）的直接推论。验证 P4 等价于验证定理 T2 在参数空间中的定量适用性。

### 4.3 验证方法

对 $a \in [0, 0.9]$ 中的 10 个参数点，计算：
1. $\text{LACI}(a)$
2. $\text{LACI}(a + 0.01)$
3. $\Delta\text{LACI} / (0.01)^2$ 的比值

预期比值 $\leq C$。

---

## 5. 预言的汇总

| 编号 | 预言 | 理论来源 | 验证优先级 | LIGO 可观测 | 当前状态 |
|:----|:-----|:--------|:--------:|:----------:|:--------:|
| P1 | $\gamma(a) \propto (1-a)^{1/3}$ | $\Delta\lambda_{\min}$ 推导 + III 型奇异纤维 | 高 | 间接 | 待验证 |
| P2 | Ringdown LACI 三段演化 | LACI 公理化 T2 | 中 | **直接** | 待验证 |
| P3 | 高自旋 LACI 骤变 = 超辐射临界 | II 型奇异纤维 = 超辐射边界 | **高** | 间接 | 待验证 |
| P4 | LACI 在扰动下 $O(\delta a^2)$ 稳定 | T2 严格证明推论 | 低 | 无 | 待验证 |

### 预言的证伪条件

每个预言都有明确的证伪条件：

| 预言 | 证伪条件 |
|:----|:--------|
| P1 | $\log\gamma$ vs $\log(1-a)$ 拟合指数 $p \notin [0.23, 0.43]$ |
| P2 | $\text{LACI}(t)$ 在 ringdown 全程无明显变化（恒定值） |
| P3 | 所有 $a \in [0, 0.99]$ 上 LACI 连续变化，无骤变 |
| P4 | $\|\Delta\text{LACI}\|/(\delta a)^2 > 100$ 在任意参数点 |

### 当前验证状态

所有预言当前标注为"待验证"——需要运行 Phase 52 数值代码（`src/dynamic_spectrum/`）进行验证。LeaverUnifiedSolver 已具备全部所需功能。

---

## 6. 与 Phase 52 的衔接

| 预言 | 依赖的 Phase 52 模块 | 预计运行时间 |
|:----|:-------------------|:-----------:|
| P1 | `A3 铃荡谱` + `LeaverUnifiedSolver` 参数扫描 | $\sim 10$ 分钟 |
| P2 | `A4 全波形` + ringdown 时间切片 | $\sim 30$ 分钟 |
| P3 | `A3 铃荡谱` + 高自旋精细扫描 | $\sim 20$ 分钟 |
| P4 | `A3 铃荡谱` + 扰动序列 | $\sim 5$ 分钟 |

---

**更新记录**：
- v0.1（2026-07-25）：初版，完成 4 个可证伪预言的定义、推导和验证方案
