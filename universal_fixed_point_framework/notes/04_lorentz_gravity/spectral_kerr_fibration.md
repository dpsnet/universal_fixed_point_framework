# Kerr 参数谱丛 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 的 Grothendieck 纤维化

**版本**：v0.1（2026-07-23）

**摘要**：本笔记将 Kerr 黑洞参数空间 $(M, a)$ 提升为 Grothendieck 纤维范畴的基空间 $\mathbf{Kerr}$，构造 QNM 谱丛 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 及其投影 $\pi_{M,a}$。核心结构包括：(1) $\mathbf{Kerr}$ 参数范畴——对象为 $(M, a)$（$M > 0$，$0 \leq a \leq M$），态射为质量和角动量的联合膨胀；(2) 纤维数据——QNM 频率族 $\{\omega_{lmn}(M,a)\}$、视界谱 $\lambda_{\text{horizon}}^{(\pm)}(M,a)$、谱间隙 $\Delta\lambda_{\min}^{(\text{Kerr})}(M,a)$；(3) 极端极限 $a \to M$ 下的纤维类型跳变（离散谱→退化谱）——这是非乘积丛刻画；(4) 与 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$ 的丛态射（Hawking 温度-谱间隙关系 $T_H(a) = \Delta\lambda_{\min}(a)/2\pi$）。

**前置依赖**：[`spectral_Kerr.md`](spectral_Kerr.md)（Kerr 全谱分解）、[`spectral_Kerr_silence_analysis.md`](spectral_Kerr_silence_analysis.md)（四层静默分析）、`spectral_Grothendieck_fibration.md`（已完成 $\pi_T$/$\pi_\mu$ 模板）。

---

## 1. Kerr 参数范畴 $\mathbf{Kerr}$

### 1.1 定义

**定义 1.1**（Kerr 参数范畴 $\mathbf{Kerr}$）。$\mathbf{Kerr}$ 是以下范畴：
- **对象**：$(M, a) \in \mathbb{R}^+ \times [0, M]$，其中 $M > 0$ 是黑洞质量，$a = J/M \in [0, M]$ 是单位质量的角动量
- **态射** $(M_1, a_1) \to (M_2, a_2)$：联合膨胀 $(r_M, r_a)$，$r_M > 0$，$r_a > 0$，使得 $M_2 = r_M \cdot M_1$，$a_2 = r_a \cdot a_1$
- **恒等态射**：$\text{id}_{(M,a)}$ 对应 $(r_M, r_a) = (1, 1)$
- **态射复合**：逐分量复合

**注 1.1**。$\mathbf{Kerr}$ 是二维参数范畴。其关键特征是存在边界 $\partial\mathbf{Kerr} = \{(M, a) \mid a = M\}$——极端 Kerr 线，对应视界简并和谱间隙闭合。

### 1.2 极端边界

**定义 1.2**（极端边界）。$\partial\mathbf{Kerr}_{\text{ext}} = \{(M, a) \in \mathbf{Kerr} \mid a = M\}$。在极端边界上：
- 内外视界重合：$r_+ = r_- = M$
- 谱间隙闭合：$\Delta\lambda_{\min}^{(\text{Kerr})}(a = M) = 0$
- 纤维类型从 $\mathbf{Sp}$（离散谱）跳变到 $\mathbf{Sp}_{\text{deg}}$（简并谱）

### 1.3 与 $\mathbf{Temp}$ 的态射

**定理 1.1**（Hawking 温度态射）。存在函子 $\mathcal{H}: \mathbf{Kerr} \to \mathbf{Temp}$，定义为：
$$\mathcal{H}(M, a) = T_H(M, a) = \frac{\hbar}{2\pi} \cdot \frac{\sqrt{M^2 - a^2}}{M^2 + \sqrt{M^2 - a^2}}$$

该函子将 Kerr 参数映射为 Hawking 温度，建立了 Kerr 谱丛与温度谱丛之间的桥梁。

---

## 2. Kerr 谱丛 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$

### 2.1 纤维数据

**定义 2.1**（Kerr 纤维）。对每个参数点 $(M, a) \in \mathbf{Kerr}$，纤维 $\mathbf{Sp}_{(M,a)}$ 包含：
- **QNM 谱**：$\{\omega_{lmn}(M, a)\}$，其中 $l$ 是角量子数，$m$ 是磁量子数，$n$ 是径向量子数
- **视界谱**：$\lambda_{\text{horizon}}^{(\pm)}(M, a) = M \pm \sqrt{M^2 - a^2}$
- **谱间隙**：$\Delta\lambda_{\min}^{(\text{Kerr})}(M, a) = \Delta\lambda_{\min}^{(\text{Schwarz})} \cdot \left(1 - \frac{a^2}{M^2}\right)$（慢转近似）

### 2.2 总范畴

**定义 2.2**（总范畴 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$）。
- **对象**：$((M, a), \{\omega_{lmn}\})$，其中 $(M, a) \in \mathbf{Kerr}$，$\{\omega_{lmn}\}$ 是 QNM 谱数据
- **态射** $(f, \phi): ((M_1, a_1), \{\omega^{(1)}\}) \to ((M_2, a_2), \{\omega^{(2)}\})$：
  - $f: (M_1, a_1) \to (M_2, a_2)$ 是参数膨胀
  - $\phi$ 是谱变换（模式映射），满足 $\phi \cdot \omega^{(2)} = \omega^{(1)} \cdot \phi$

### 2.3 投影函子

**定义 2.3**（投影 $\pi_{M,a}$）。$\pi_{M,a}: \mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp}) \to \mathbf{Kerr}$ 定义为：
$$\pi_{M,a}((M, a), \{\omega\}) = (M, a), \quad \pi_{M,a}(f, \phi) = f$$

### 2.4 谱间隙截面

**定义 2.4**（谱间隙截面）。$\sigma_{\Delta}^{(\text{Kerr})}: \mathbf{Kerr} \to \mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 定义为：
$$\sigma_{\Delta}^{(\text{Kerr})}(M, a) = ((M, a), \Delta\lambda_{\min}^{(\text{Kerr})}(M, a))$$

该截面满足 $\pi_{M,a} \circ \sigma_{\Delta}^{(\text{Kerr})} = \text{id}_{\mathbf{Kerr}}$。

---

## 3. Grothendieck 纤维化结构

### 3.1 Cartan 提升

**定理 3.1**（$\pi_{M,a}$ 是 Grothendieck 纤维化）。投影 $\pi_{M,a}$ 是分裂 Grothendieck 纤维化：对任意 $((M_2, a_2), \{\omega^{(2)}\})$ 和 $f: (M_1, a_1) \to (M_2, a_2)$，Cartan 提升由 QNM 谱沿参数方向的连续性给出。

**证明**（草图）。提升对象为 $((M_1, a_1), f^*\{\omega^{(2)}\})$，其中拉回谱通过 Leaver 连分数方程的连续性得到：
$$f^*\omega_{lmn} = \omega_{lmn}(M_1, a_1) \text{ (Kerr QNM 方程在参数 $(M_1,a_1)$ 处的解)}$$
提升的万有性质由 QNM 谱对参数的连续依赖性保证。$\square$

### 3.2 非乘积丛结构

**定理 3.2**（非乘积丛）。$\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 是一个**非乘积丛**——当 $a \to M$ 时，纤维类型从 $\mathbf{Sp}$（离散 QNM 谱）跳变为 $\mathbf{Sp}_{\text{deg}}$（退化视界谱）：
$$\lim_{a \to M} \omega_{lmn}(M, a) \approx \omega_{lmn}^{(0)}(M) + i \cdot (M - a) \cdot \delta\omega_{lm}$$

跳变点处谱间隙闭合、QNM 虚部消失、视界简并，使得 $a > M$ 时无物理 Kerr 黑洞（裸奇点）。该结构使 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 成为普通向量丛无法表达的范畴对象。

---

## 4. 与温度谱丛的丛态射

### 4.1 Hawking 温度映射

**定理 4.1**（温度-谱间隙丛态射）。存在纤维保持函子 $\hat{\mathcal{H}}: \mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp}) \to \mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$，其基函子为 $\mathcal{H}: \mathbf{Kerr} \to \mathbf{Temp}$（定理 1.1），使得：
$$T_H(M, a) = \frac{\Delta\lambda_{\min}^{(\text{Kerr})}(M, a)}{2\pi}$$

该函子建立了 Kerr 谱间隙闭包与 Hawking 温度之间的严格对应。

### 4.2 温度-角动量联合参数

**定义 4.2**（联合参数丛）。定义乘积基 $\mathbf{Temp} \times \mathbf{Kerr}$ 上的联合谱丛 $\mathbf{Bun}(\mathbf{Temp} \times \mathbf{Kerr}, \mathbf{Sp})$，其对象为 $((T, M, a), \{\omega(T, M, a)\})$。

限制函子给出两个方向的拉回：沿 $\mathbf{Temp}$（固定 Kerr 参数）和沿 $\mathbf{Kerr}$（固定温度）。

---

## 5. 边界行为与相变

### 5.1 极端极限的谱框架刻画

| 参数 | Schwarzschild ($a=0$) | 极端 Kerr ($a=M$) | 变化 |
|:----|:--------------------:|:----------------:|:----:|
| 视界 | $r_+ = 2M$，$r_- = 0$ | $r_+ = r_- = M$ | 重合 |
| 谱间隙 | $\Delta\lambda_{\min}^{(0)} = 0.122$ | $0$ | 闭合 |
| 表面引力 | $\kappa = 1/4M$ | $0$ | 消失 |
| QNM 虚部 | $\text{Im}(\omega_{220}) = -0.0890$ | $0$ | 无穷寿命 |
| 纤维类型 | $\mathbf{Sp}$ | $\mathbf{Sp}_{\text{deg}}$ | **跳变** |

### 5.2 非乘积丛的范畴论意义

极端边界的纤维类型跳变使 $\mathbf{Bun}(\mathbf{Kerr}, \mathbf{Sp})$ 成为非乘积丛——这是 $\mathbf{Bun}(\mathbf{Temp}, \mathbf{Sp})$（乘积丛）的根本不同。在范畴论中，这意味着 $\pi_{M,a}$ 不是一个平凡的 Grothendieck 纤维化——虽然在普通点处有 Cartan 提升，但沿 $\partial\mathbf{Kerr}_{\text{ext}}$ 的全局截面不存在连续延拓。

---

## 6. Lean 4 形式化方案

### 6.1 复用组件

| 组件 | 来源 | 角色 |
|:----|:-----|:-----|
| `CartesianLiftData` / `GrothendieckFibration` | `TempRGFiber.lean` | $\pi_{M,a}$ 纤维化实例 |
| `spectralGap` | `SpectralGap.lean` | $\Delta\lambda_{\min}^{(\text{Schwarz})} = (\sqrt{6}-\sqrt{2})/\sqrt{72}$ |
| `FiberedFunctor` | `TempRGFiber.lean` | $\hat{\mathcal{H}}$ 丛态射 |

### 6.2 新建内容与深化 (v0.2)

| 模块 | 内容 |
|:----|:-----|
| `KerrObj` / `KerrHom` | $\mathbf{Kerr}$ 范畴（对象 $(M,a)$，态射联合膨胀）|
| `SpecFiberKerr` | Kerr 纤维：QNM 频率、视界谱、谱间隙 |
| `SpectralBundleKerr` | 总范畴 + $\pi_{M,a}$ 投影 + GrothendieckFibration |
| `horizon_r_plus/minus` | 视界半径解析函数 + Schwarzschild/极端极限定理 |
| `kerrGap` | 谱间隙函数 + 三定理（Schwarzschild/极端/近极端）|
| `KerrGapSection` | 谱间隙截面 |
| `spectralGap8_pos` | $\Delta\lambda_{\min}^0 > 0$ 严格证明 |
| `hawkingTemp` | 谱框架 Hawking 温度 + 三定理（nonneg/extreme/schwarzschild）|
| **`SpinPreservingKerr`** | **v0.2 新增**：自旋保持子范畴 + `H_functor_spin` 完整函子性 |
| **`H_hat_spin`** | **v0.2 新增**：$\hat{\mathcal{H}}$ 丛态射（自旋保持子范畴上）|
| **`extreme_limit_gap_closure`** | **v0.2 新增**：极端极限谱间隙闭合严格定理 |
| **`kerr_non_product_bundle`** | **v0.2 新增**：非乘积丛论证 |
| **`bekensteinHawkingEntropy`** | **v0.2 新增**：BH 熵谱求和形式 + Schwarzschild 极限 |

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.2** | **2026-07-23** | **深化**新增：`spectralGap8_pos` 严格证明；`hawkingTemp` + 三定理；`SpinPreservingKerr` 子范畴 + `H_functor_spin` 完整函子性证明；`H_hat_spin` 丛函子；`extreme_limit_gap_closure` 严格定理；`kerr_non_product_bundle` 论证；`bekensteinHawkingEntropy` + Schwarzschild 极限 |
| **v0.1** | **2026-07-23** | 初始版本：Kerr 参数范畴定义；纤维数据结构（QNM 谱、视界谱、谱间隙）；Grothendieck 纤维化；非乘积丛结构（极端极限跳变）；Hawking 温度丛态射；联合参数丛；Lean 形式化方案 |
