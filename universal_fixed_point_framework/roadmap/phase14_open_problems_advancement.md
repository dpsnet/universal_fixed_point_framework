# Phase 14：开放问题推进计划

**版本**：v0.7

**日期**：2026-07-13

**状态**：已全面推进 Paper I §8.2 所列三类开放问题，并完成四轮数学严格化深化。新增代码模块保持为 4 个，测试数从 61 增至 64，全部通过。此外完成 D 函子代码质量修复并发现 $\mathbf{Sp}$ 是 $\mathbf{Rec}$ 的反射子范畴的理论结构（新增命题 2.10）。

---

## 一、阶段定位

本阶段针对 Paper I §8.2 与 Paper II 展望中的关键开放问题，建立从"理论框架"到"可运行代码"的推进路径。目标不是一次性解决所有数学严格性问题，而是：

1. 给出可验证的定理/猜想形式化表述；
2. 提供可执行的数值/符号验证代码；
3. 明确下一步严格化所需的数学工具与实验接口。

---

## 二、已推进内容

### 2.1 纯数学方向

| 开放问题 | 推进成果 | 代码 | 状态 |
|---|---|---|---|
| 非分离 IFS 收敛率最终紧性 | 定理 NS-LB：packing number / minimax 下界 $|\lambda_k^{(N)} - \lambda_k| \geq c N^{-\alpha/d_H}$；与 NS-1M 上界匹配得紧阶 $\Theta(N^{-\alpha/d_H})$ | `src/math_open_problems_advanced.py` | ✅ 已推进 |
| 非分离 IFS 重叠热力学形式 | **三层热力学形式**：(1) 简化字级模型 `feng_wang_pressure`；(2) **Ruelle 精确转移算子** `RuelleTransferOperator`；(3) **IFS 最优条件转移算子** `FengWangOptimalConditionalOperator`，加权条件测度替代贪心选择 | `src/math_open_problems_advanced.py` | ✅ 已推进 |
| 奇异连续谱的动力学刻画 | 定理 SC-L：$D_1 = h_\mu / \lambda_L^{(+)}$，对 IFS 具体化为 Kaplan-Yorke 熵-李雅普诺夫比；OSC 情形数值一致 | `src/math_open_problems_advanced.py` | ✅ 已推进 |
| 拓扑熵-谱间隙普适不等式 | 猜想 TE-G：$h_\mu \cdot \gamma \leq C$；**Markov IFS 严格框架** + **一般系统 Koopman 算子推广** | `src/math_open_problems_advanced.py` | ✅ 已推进 |
| 高维 IFS 收敛率数值验证 | 解析框架已完成，大规模核矩阵数值验证仍待推进 | `src/high_dimensional_ifs.py` | ⏳ 待深化 |

### 2.2 数值工程方向

| 开放问题 | 推进成果 | 代码 | 状态 |
|---|---|---|---|
| MadGraph 完整调用 | `MadGraphInterface`：process/run card 自动生成、`mg5_aMC` 调用、截面解析、解析近似回退 | `src/numerical_engineering_open_problems.py` | ✅ 接口完成，真实安装联调待完成 |
| micrOMEGAs 完整调用 | `MicrOmegasInterface`：SLHA 自动生成、`main` 调用、relic/SI/SD 解析、解析近似回退 | `src/numerical_engineering_open_problems.py` | ✅ 接口完成，真实安装联调待完成 |
| 双星 inspiral-merger-ringdown 引力波仿真 | `BinaryGWWaveform`：PN inspiral + ISCO merger + QNM ringdown + 简化 SNR | `src/numerical_engineering_open_problems.py` | ✅ 原型完成，IMR 拟合/LALSuite 对接待完成 |

### 2.3 物理理论方向

| 开放问题 | 推进成果 | 代码 | 状态 |
|---|---|---|---|
| Kerr 全局量子谱完整解析 | `KerrGlobalSpectrum`：近似 QNM 频率、Bohr-Sommerfeld 量子化、超辐射判据、谱对应；**简化系数 Leaver 求解器**、**精确系数 Leaver 求解器**、**自洽 Teukolsky-Leaver 求解器**（spheroidal λ 自洽迭代替代级数近似） | `src/physics_open_problems_advanced.py` | ✅ 解析框架完成，独立 Leaver 谱方法待深化 |
| $N=4$ SYM 高精度定量匹配 | `N4SYMSpectrum`：1/2 BPS、Konishi、BMN 能级；与框架 $\eta_R$ 精确匹配；强耦合 Bethe ansatz 近似 + 弱→强耦合插值；**简化 BES/TBA** `N4SYMBES`；**O(g⁶) BES/TBA 升级** `N4SYMBESFull`（$O(g^6)$ dressing phase + 多模 wrapping） | `src/physics_open_problems_advanced.py` | ✅ 谱对应完成，完整 BES/TBA 数值解待深化 |
| 暗物质完整分形谱推导 | `DarkMatterFractalSpectrum`：IFS 质量分形谱、$D_{\text{DM}} = h_\mu/\lambda_L$、遗迹密度/直接探测约束筛选 | `src/physics_open_problems_advanced.py` | ✅ 原型完成，间接探测/冻结-in 待深化 |

---

## 三、新增代码模块清单

- `src/math_open_problems_advanced.py`
- `src/numerical_engineering_open_problems.py`
- `src/physics_open_problems_advanced.py`
- `src/test_open_problems_advanced.py`

---

## 四、验证结果

- `python math_open_problems_advanced.py`：上下界比值稳定约 2；$D_{\text{KY}} = d_H$ 在 OSC 情形一致；IFS/Ruelle/条件转移算子维数随重叠度下降；拓扑熵-谱间隙不等式 $h_\mu\gamma \leq 1$ 广泛成立；Markov IFS 严格框架 $h_{\text{top}}\gamma \leq 1$ 显式验证。
- `python numerical_engineering_open_problems.py`：MadGraph/micrOMEGAs 解析回退输出合理，双星波形 f_merger ≈ 68 Hz、f_ring ≈ 188 Hz。
- `python physics_open_problems_advanced.py`：Kerr QNM 谱、Leaver 简化/精确/完整 Teukolsky 求解器、N=4 SYM 弱/强/BES/完整 BES 谱、暗物质约束筛选均正常输出。
- `pytest -q`：**64 passed**。

---

## 五、下一步计划

### 5.1 纯数学严格化

1. 显式优化定理 NS-LB 中的下界常数 $c$；
2. 将 IFS 条件转移算子中的贪心选择 $I(x)$ 提升为 IFS 原文的最优条件测度；严格证明 $d_H(\rho)$ 的凹性与热力学极限存在性；
3. 将 TE-G 从 Markov IFS 推广到一般动力系统并完成严格证明；精确估计普适常数 $C$；
4. 高维核矩阵的大规模数值紧性测试；
5. 拓扑熵与谱间隙的普适不等式。

### 5.2 数值工程落地

1. 在真实 MadGraph/micrOMEGAs 安装上完成端到端调用；
2. 将双星波形接入 SEOBNRv4/IMRPhenom 或 LALSuite；
3. 含潮汐形变（中子星）的双星系统扩展。

### 5.3 物理理论深化

1. 将 spin-weighted spheroidal 特征值级数近似替换为高精度谱方法或连分数求解；
2. 将简化 dressing phase/wrapping corrections 替换为完整 BES/TBA 数值解；
3. 暗物质间接探测谱与冻结-in / 非热产生机制。

---

## 六、风险与审稿挑战

### 6.1 仍需注意的风险

| 风险类型 | 具体表现 | 缓解策略 |
|---|---|---|
| **数值模拟/占位** | NTK 消融实验中的随机数、MadGraph 不可用时 fallback 到解析近似 | 在论文与代码中明确标注"解析回退"与"真实安装联调"的区分；优先完成真实工具端到端验证 |
| **数学证明简化假设** | 非分离 IFS 的 Hausdorff 维数估计用了简化模型，真实 IFS 热力学形式更复杂 | 在 §8.2 中明确列出未竞问题；下一步引入压力函数与变分原理严格化 |
| **物理实例近似性** | Kerr QNM 用了拟合公式而非严格 Leaver 连分数数值解 | 在论文中区分"解析框架"与"严格数值解"；下一步实现高精度 spheroidal 特征值 |
| **框架覆盖过广** | 数学家和物理学家都可能质疑其深度 | 在 §7.7 与 §9 中强调"核心方法论"定位；用具体定理+代码+数值验证支撑每一个主张；避免过度哲学化 |

### 6.2 审稿挑战预判

- **数学审稿人**可能质疑：非分离 IFS 下界定理 NS-LB 的常数 $c$ 是否最优；谱静默四判据的充分必要性；理论转化范畴 $\mathbf{Trans}_{\mathbf{Rec}}$ 是否真正构成范畴；拓扑熵-谱间隙不等式 TE-G 的普适性是否经过严格证明。
- **物理审稿人**可能质疑：Kerr QNM 拟合公式的精度；N=4 SYM 谱对应在强耦合下是否成立；MadGraph/micrOMEGAs 接口是否真实可用。
- **一般性质疑**：框架是否只是重新包装已有理论？回应：本框架提供**统一语言**（Rec/Sp + $D \dashv R$ + $M \cong L$），将分散的数学工具与物理实例纳入同一范畴，其价值在于发现跨领域的新对应关系（如 EFT = 谱静默、Kerr ringdown = 分形谱）。

---

## 七、下一步最关键的工作

按优先级排序：

1. **将 `spectral_silence.py` 的定理写入 Paper I**：已在 v2.5 中完成（§5.6 新增定理 5.6–5.8）。
2. **将 `eft_equivalence_framework.py` 和 `theory_transformation.py` 写入论文，作为框架核心方法论**：已在 v2.5 中完成（§7.7 五种转化模式、EFT 等价性框架、理论等价不变量与判定定理）。
3. **将弦图演算作为论文的图形语言工具**：已在 v2.5 中完成（§7.7.3 转化弦图定义与弦图到代码语义保持定理 7.18）。
4. **数学严格化深化**：IFS 最优条件测度、TE-G 一般动力系统证明、spheroidal 高精度谱方法、完整 BES/TBA 数值解。
5. **真实工具联调**：MadGraph/micrOMEGAs 端到端验证、LALSuite 双星波形对接。

---

## 八、依赖关系

```
Phase 14 开放问题推进
    │
    ├── 依赖：Phase 6（RKHS 收敛率理论）
    ├── 依赖：Phase 9（连续谱与谱测度理论）
    ├── 依赖：Phase 12（GR+SM 统一谱对应猜想）
    ├── 依赖：Phase 13（理论转化与仿真接口）
    └── 依赖：applications/ 各物理实例
```

---

## 九、版本记录

| 版本 | 日期 | 更新内容 |
|---|---|---|
| v0.6 | 2026-07-13 | 数学严格化四阶段深化：IFS 加权条件测度、Koopman TE-G 推广、spheroidal λ 自洽迭代、O(g⁶) BES/TBA；测试数从 61 增至 64；同步 Paper I v2.9 / Paper II v2.6 |
| v0.7 | 2026-07-13 | D 函子修复 + 理论更新：移除 Koopman 强制对称化（Rec 扩展）；新增反射子范畴命题 2.10 与注 2.11（$\mathbf{Sp}$ 是 $\mathbf{Rec}$ 的反射子范畴）；同步 Paper I v2.10 / Paper II v2.7 |
| v0.5 | 2026-07-13 | 数学严格化三阶段深化：新增 IFS 条件转移算子、Markov IFS 下 TE-G 严格框架、完整 Teukolsky-Leaver 求解器、N=4 SYM 完整 BES/TBA 升级；测试数从 57 增至 61 |
| v0.4 | 2026-07-13 | 数学严格化再深化：新增 Ruelle 精确转移算子、拓扑熵-谱间隙不等式、Leaver 精确系数、N=4 SYM 简化 BES/TBA；测试数从 52 增至 57 |
| v0.3 | 2026-07-13 | 数学严格化深化：新增 IFS 热力学形式、Leaver 连分数 Kerr QNM 原型、强耦合 N=4 SYM Bethe ansatz 近似；测试数从 47 增至 52 |
| v0.2 | 2026-07-13 | 同步 Paper I v2.5 更新；新增"风险与审稿挑战"与"下一步最关键工作"章节 |
| v0.1 | 2026-07-13 | 初始版本，汇总三类开放问题推进成果，定义下一步计划 |
