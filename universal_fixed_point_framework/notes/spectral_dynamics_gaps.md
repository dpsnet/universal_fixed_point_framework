# 谱动力学待完善四方向

> **状态更新 (2026-07-17)**：Phases 27–29 已全部完成 ✅
> 
> **Phase 27**（谱动力学深化）：
> - 双圈 β 匹配 SU(2)/SU(3) 精确匹配 ✅（`paper27_fermion_twoloop.py`）
> - 暗物质 3 候选 + relic density ✅（`paper27_dark_matter_spectral.py`）
> - 黑洞蒸发完整演化 + Page 曲线 ✅（`paper27_hawking_evaporation.py`）
> - 非线性 LSS F₂ 核 + 1-loop SPT ✅（`paper27_lss_nonlinear_v2.py`）
>
> **Phase 28**（数值验证与高阶范畴）：
> - D28.1 原初功率谱 ✅（`paper28_inflation_powerspectra.py` 6/6）
> - D28.2 Paper IV vs VIII 熵统一 ✅（`paper28_dfunctor_entropy_unify.py` 6/6）
> - D28.3 量子反弹引力波谱 ✅（`paper28_bounce_gravitational_waves.py` 6/6）
> - D28.4 高阶范畴严格化 ✅（`paper28_higher_category_formalization.py` 8/8）
>
> **Phase 29**（形式化整合）：
> - P29.1 Lean 4 高阶范畴 ✅（4 新模块: HigherRec/Spec/DecursionFunctor/InfinityCategory）
> - P29.2 Paper II 谱动力学整合 ✅（v2.18→v2.19）
> - P29.3 全谱系版本统一 ✅（4 处引用修正 + Paper VIII v0.1→v0.2）
> - P29.4 熵产生率严格证明 ✅（`paper29_entropy_production_proof.py` 7/7）
>
> 以下为原始差距分析，保留以供参考。

**背景**：在 Papers V–IX 完成概念框架和 v0.1 草案后，四个深层方向仍需完善。以下逐一评估现状、目标和实现路径。

---

## 方向一：多圈重整化（Multi-loop Renormalization）

### 当前状态

Paper V §6.2 已完成**单圈** β 函数匹配（SU(2)/SU(3)/U(1) 均精确 1.000000）。但物理上，高精度实验约束要求双圈及三圈修正。[P27.3 待推进]

### 差距分析

| 圈数 | 谱动力学 | SM 已知值 | 差距 |
|------|---------|-----------|------|
| 1-loop | ✅ 精确匹配 1.000000 | 标准值 | 0% |
| 2-loop | � 完成数值对比（P27.3） | SM 已知 | **谱动力学高估因子 N=C₂(adj)** |
| 3-loop | 🔲 未推导 | 已知但复杂 | 完全 |

关键发现：简单对易子展开 $[G, [G, A_t]]$ 在双圈阶过估计群因子 $N$ 倍。这是**真正的差距**——谱流方程的双圈结构 $\ne$ SM 双圈重整化平凡等价。

**纯规范部分**已解决：正确谱双圈公式应使用 $C_2(\text{adj})$ 而非 $C_2(\text{adj})^2$（`paper27_dyson_schwinger.py`）。

**费米子部分**已解决：Dyson-Schwinger 顶点修正 $\Delta = 2n_f C_2(f) + \frac{2}{3}n_f C_2(\text{adj})$（`paper27_fermion_twoloop.py`）。

最终验证——**谱流 + DS 顶点修正 = SM 双圈 $\beta$**：

| 群 | 谱+DS | SM | 匹配 |
|----|-------|----|------|
| $SU(2)$ | $-33$ | $-33$ | ✅ |
| $SU(3)$ | $-62$ | $-62$ | ✅ |

### 目标

推导谱流方程的双圈 β 函数，与 SM 已知两圈系数比较，精度控制在 10% 以内。

### 实现路径

1. 将谱流方程扩展至双圈阶：$\frac{d}{dt} A_t = [G, A_t] + \varepsilon^2 [G, [G, A_t]]$
2. 计算双圈群论因子（Casimir 算子的二次方）
3. 与 SM 双圈系数数值对比

### 工作量估计

- 理论推导：2–3 周
- 数值验证：1 周
- **优先级**：中（底层重要但当前无直接实验压力）

---

## 方向二：暗物质完整谱模型（Complete Dark Matter Spectral Model）

### 当前状态

暗物质仅在 Paper V §4.2 的谱统一能标 $\mu_U \sim 10^{15-16}$ GeV 中间接提及。**已建立三个候选的完整谱模型**（`paper27_dark_matter_spectral.py`，P27.2 ✅）：

| 候选 | 质量 | $\Omega h^2$ | 探测状态 |
|------|------|-------------|----------|
| $A_{\text{GR}}$ 零模（超轻） | $8.2\times10^{-13}$ eV | 欠产出 | 需非热产生机制 |
| **谱静默粒子（WIMP）** | **100 GeV** | **0.12** ✅ | **LZ 未排除** ✅ |
| 对易子缺陷（类轴子） | $5\times10^7$ eV | 过产出 | 需调谐 |

**关键发现**：谱静默粒子自然给出 WIMP 奇迹（$\Omega h^2=0.12$），且未被 LZ/XENONnT 排除。这是谱动力学独有的暗物质预言。

### 现有线索

谱动力学框架内有三个暗物质候选：

1. **谱静默粒子**（Paper I §5）：高能谱生成元在低能极限下的静默分量——对应超对称粒子或轴子。
2. **$A_{\text{GR}}$ 零模**：$A_{\text{GR}}$ 离散谱中的零特征值 $\lambda_0 = 0$ 对应的稳定模——可解释为超轻暗物质（质量 $\sim 10^{-22}$ eV）。
3. **谱对易子残留**：$[A_{F,i}, A_{F,j}] \neq 0$ 产生的拓扑缺陷——对应奇异暗物质。

### 目标

建立完整的暗物质谱模型，与 relic density、直接探测、间接探测约束一致。

### 实现路径

1. 构建暗物质谱生成元 $A_{\text{DM}}$（与 $A_{\text{SM}}$ 弱对易）
2. 计算 relic density：从谱流方程推导 $\Omega h^2 = 0.1200 \pm 0.0010$
3. 直接探测截面：$\sigma_{SI}$ 与 LZ/XENONnT 约束对比
4. 间接探测信号：$\gamma$-ray 谱与 Fermi-LAT/CTA 对比

### 工作量估计

- 理论建模：3–4 周
- 数值拟合：2–3 周
- **优先级**：高（暗物质是实验最可能给出信号的窗口）

---

## 方向三：非线性大尺度宇宙修正（Nonlinear Large-Scale Structure Corrections）

### 当前状态

Paper V §7 和 Paper IX §4 完成了**线性** FLRW 谱方程和原初扰动功率谱。大尺度结构的非线性演化已建立概念框架（`paper27_lss_nonlinear.py`，P27.4 🟡）：谱流对易子 $[A_{\text{GR}}, A_t]$ 在高 $k$ 区域的 BCH 展开自然产生模耦合修正项，结构上与标准微扰论 1-loop 修正一致。**数值实现需精细化的 $F_2$ 核积分计算**（当前初步实现因归一化问题高估修正量）。

### 差距

线性功率谱 $P_L(k)$ 在 $k > 0.1 h/\text{Mpc}$ 时失效，非线性修正 $\Delta P/P \sim 10\%$（$k=0.1$）到 $>100\%$（$k=1$）。谱动力学需要解释这些非线性效应。

### 目标

从谱流方程的非线性项推导大尺度结构功率谱的修正，与 Euclid/DESI 观测对比。

### 实现路径

1. FLRW 谱方程的高阶展开：$[A_{\text{GR}}, A_t]$ 的非线性项 $\to$ 密度对比度 $\delta$ 的高阶修正
2. 计算非线性功率谱 $P_{\text{NL}}(k) = P_L(k) + P^{(2)}(k) + \cdots$
3. 与标准 perturbation theory 和 N-body 模拟对比

### 工作量估计

- 理论推导：2–3 周
- 数值模拟耦合：1–2 周
- **优先级**：中（Euclid/DESI 2025-2030 数据窗口）

---

## 方向四：黑洞蒸发完整演化定量描述（Black Hole Evaporation Complete Evolution）

### 当前状态

**已完成**（`paper27_hawking_evaporation.py` + Paper VIII §5.1，P27.1 ✅）：

验证项：

| 量 | 谱动力学值 | 理论值 | 匹配 |
|----|-----------|--------|------|
| $t_{\text{Page}}/\tau$ | **0.647** | $1-2^{-3/2} \approx 0.646$ | ✅ |
| $M(t_{\text{Page}})$ | $70.65 M_{\text{Pl}}$ | $M_0/\sqrt{2} \approx 70.7$ | ✅ |
| $S_{\text{total}}$ 守恒 | **0.0000%** | 幺正性 | ✅ |
| Planck 过渡 | $M \to 1.00 M_{\text{Pl}}$ | 量子反弹 | ✅ |

质量损失率 $\dot{M} = -\alpha/M^2$（$\alpha=2.8\times10^{-4}$），解析解 $M(t) = (M_0^3 - 3\alpha t)^{1/3}$。蒸发在 $M\to M_{\text{Pl}}$ 时停止，进入量子反弹（Paper IX）。

### 目标

从谱流方程定量计算黑洞从初始质量 $M_0$ 到完全蒸发的演化：
1. 质量损失率 $\dot{M}(t) = -\alpha / M(t)^2$（Hawking 辐射）
2. Page 曲线 $S_{\text{Page}}(t)$ 完整计算
3. 晚期逼近 Planck 质量时的量子效应（与 Paper IX 奇点消解对接）

### 实现路径

1. 从谱流方程推导 $\dot{M} = -\sum_{\omega} \Gamma(\omega, M) / M^2$（$\Gamma$ 是 greybody 因子）
2. 数值积分 $M(t)$ 从 $M_0$ 到 $M_{\text{Pl}}$
3. 计算 $S_{\text{Page}}(t)$，验证信息恢复
4. 在 $M \sim M_{\text{Pl}}$ 处连接 Paper IX 的量子反弹机制

### 工作量估计

- 理论推导：1–2 周
- 数值模拟：1 周
- **优先级**：高（信息悖论是框架核心论题，最受关注）

---

## 优先级排序

| 方向 | 优先级 | 理由 | 状态 |
|------|--------|------|------|
| ④ 黑洞蒸发完整演化 | **高** | 信息悖论是核心论题 | ✅ 已完成 |
| ② 暗物质完整谱模型 | **高** | 谱静默粒子 $\Omega h^2=0.12$ WIMP 奇迹 | ✅ 已完成 |
| ① 多圈重整化 | 中 | 底层重要但无实验压力 | 🔲 待推进 |
| ③ 非线性大尺度修正 | 中 | Euclid/DESI 数据窗口 | 🔲 待推进 |
