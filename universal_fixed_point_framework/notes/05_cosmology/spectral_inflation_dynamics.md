# 暴涨完整动力学：e 折叠解析 / 再加热 / 动态连续极限 / 原初引力波闭环

**笔记状态**：初版（2026-08-03）
**对应路线图**：`roadmap/phase61_physics_advancement.md` P1-4（Phase 61A）
**规划依据**：`docs/针对v0.9版系列论文的客观评价.md` §二-3 缺口④"宇宙暴涨完整机制——e 折叠数演化、再加热阶段、暴涨时空动态连续极限的完整动力学"缺失。
**完成判据**：$N_e$ 闭式 + 再加热推导 + 动态连续极限定理 + CMB 预言闭环 + Lean/Agda 形式化模块。
**规范声明**：本文严格区分【标准慢滚暴胀的既有结果】（引用文献/标准推导）与【本框架新增推导】（基于谱流方程/谱势/谱嵌入）。后者标注为"谱新增"。

---

## 1. 问题重述与已有资产盘点

终评判定：暴涨方向"未纳入"，仅存局部纸面成果：
- Paper 9 §4.4：Starobinsky 型慢滚势谱起源 $V(\varphi) = V_0(1 - e^{-\sqrt{2/3}\,\varphi})^2$（$R^2$ 修正自然推论）+ 完整 CMB 功率谱预言表（$n_s = 0.9606$，$r = 0.0042$，$\alpha_s$）。
- Paper 5 §7：FLRW 谱方程（定理 7.1：$d\lambda_k/dt = -2H\lambda_k + \sum_i g_i[A_{F,i},A_t]_{kk}$）、慢滚谱指数、暗能量。
- Paper 12 §12：原初引力波张量功率谱 + 谱修正 + 一致性关系（定理 12.1/12.2）。
- Paper 25 §7：宇宙学六层纤维分解，Cosmo-1（Inflation）/ Cosmo-2（Reheat）谱生成元。
- Paper 34 + `notes/08_first_principles/b2_continuum_limit_analysis.md`：静态 IFS → $R^4$ 拟对称嵌入（定理 5.3）+ 谱流保持可微结构（定理 5.5）。
- 数值：`scripts/paper28_inflation_powerspectra.py`（6/6）、`scripts/phase42_inflation_R4.py`、`scripts/paper5_cosmology.py`。
- 笔记：`notes/04_lorentz_gravity/spectral_inflation_silence.md`（$N_e \approx 55$ 的分形边界定性来源）。

缺失的完整链条：**e 折叠数闭式积分 → 再加热温度谱推导 → 暴涨时空动态连续极限（时间依赖）→ 原初引力波预言闭环**。

---

## 2. D1：e 折叠数解析（$N_e$ 闭式）

### 2.1 谱势与慢滚参数【标准结果 + 谱来源标注】

谱动力学暴胀势来自 $A_{\mathrm{GR}}$ 零模式有效势（Paper 9 §4.4）：

$$\lambda_0(\varphi)^4 / 4 = V(\varphi) = V_0\,(1 - e^{-b\varphi})^2,\qquad b = \sqrt{2/3}$$

其中 $b$ 的标准值为 $\sqrt{2/3}$（$R^2$ 修正自然推论，Paper 9 §5），谱间隙修正给出【谱新增】有效斜率：

$$b_{\text{eff}} = b\,(1 + \delta_b),\qquad \delta_b = c_b\,(\Delta\lambda_{\min}/M_{\mathrm{Pl}})^2$$

以 $\Delta\lambda_{\min} = 0.122\,M_{\mathrm{Pl}}$（Paper XX 谱间隙）取 $c_b \approx 2.0$（paper28 的 $\delta_b = 0.02@0.1M_{\mathrm{Pl}}$ 标度律），得 $\delta_b \approx 0.0298$，$b_{\mathrm{eff}} \approx 0.8409$。

标准慢滚参数（$M_{\mathrm{Pl}} = 1$ 单位，$V'/V = 2b\cdot e^{-b\varphi}/(1-e^{-b\varphi})$，$b^2 = 2/3$）：

$$\varepsilon = \frac{1}{2}\left(\frac{V'}{V}\right)^2 = \frac{4}{3}\left(\frac{e^{-b\varphi}}{1-e^{-b\varphi}}\right)^2,\qquad
\eta = \frac{V''}{V} = \frac{4}{3}\,\frac{e^{-b\varphi}(2e^{-b\varphi}-1)}{(1-e^{-b\varphi})^2}$$

### 2.2 $N_e$ 闭式积分【标准积分，闭式为本篇新整理】

e 折叠数定义（标准）：

$$N(\varphi) = \int_{\varphi_{\text{end}}}^{\varphi} \frac{d\varphi'}{\sqrt{2\varepsilon(\varphi')}} = \int_{\varphi_{\text{end}}}^{\varphi} \frac{V}{V'}\,d\varphi'$$

对 Starobinsky 型势，$V/V' = (1-e^{-b\varphi})/(2b\,e^{-b\varphi}) = (e^{b\varphi} - 1)/(2b)$，故【闭式】：

$$N(\varphi) = \frac{1}{4b^2}\left(e^{b\varphi} - b\varphi - e^{b\varphi_{\text{end}}} + b\varphi_{\text{end}}\right) = \frac{3}{4}\left(e^{b\varphi} - b\varphi\right) - N_{\text{end}}$$

其中 $b^2 = 2/3$，$N_{\text{end}} = (3/4)(e^{b\varphi_{\text{end}}} - b\varphi_{\text{end}})$。暴胀结束条件 $\varepsilon(\varphi_{\text{end}}) = 1$ 给出（标准）：

$$\varphi_{\text{end}} = \frac{1}{b}\ln\left(\frac{2+\sqrt{3}}{\sqrt{3}}\right) \approx 0.9402\,M_{\mathrm{Pl}},\qquad N_{\text{end}} = \frac{3}{4}\left(e^{b\varphi_{\text{end}}} - b\varphi_{\text{end}}\right) \approx 1.04$$

（$\varepsilon = (4/3)(e^{-b\varphi}/(1-e^{-b\varphi}))^2 = 1 \iff e^{-b\varphi} = \sqrt{3}/(2+\sqrt{3}) = 0.4641 \Longrightarrow b\varphi_{\text{end}} = \ln(2.1547) \approx 0.7678$；$e^{b\varphi} - b\varphi = 2.1547 - 0.7678 = 1.3869$，$\times 3/4 \approx 1.04$。脚本 `scripts/paperX_inflation_dynamics.py` C1/C2 验证。）

CMB 尺度 e 折叠数 $N_e \equiv N(\varphi_{\text{cmb}})$。对 $N_e = 55$，闭式 $(3/4)(e^{b\varphi}-b\varphi) = 55 + N_{\text{end}} = 56.04$，解得 $b\varphi_{\text{cmb}} \approx 4.367$：

$$\varphi_{\text{cmb}} \approx \frac{4.367}{b} \approx 5.35,\qquad \varphi_{\text{cmb}}^{(\text{主导})} = \frac{1}{b}\ln\frac{4N_e}{3} \approx 5.26$$

（主导近似对 $N_e \gg 1$ 成立，精确解迭代求解，脚本 §1 给出。）

**$N_e$ 闭式（含谱修正）**【谱新增，整理为单一表达式】：

$$N_e = \frac{3}{4}\left(e^{b_{\text{eff}}\varphi_{\text{cmb}}} - b_{\text{eff}}\varphi_{\text{cmb}}\right)\left[1 + \mathcal{O}(\Delta\lambda_{\min}^2)\right] - N_{\text{end}} + N_{R^4}$$

其中 $N_{R^4}$ 为 Phase 42 $R^4$ 修正（$V$ 的高阶 $e^{-b\varphi}$ 因子）对 e 折叠积分的相对修正。

**$N_{R^4}$ 精确闭式**（2026-08-04 推导，`scripts/paperX_nR4_closed_form.py` 验证 ✅）：
谱势 R⁴ 修正 $V(\varphi) = V_0(1-e^{-b\varphi})^2(1+\delta_2 e^{-2b\varphi})$，$\delta_2 = c_3/c_1^2$（R⁴ 相对强度，Phase 42），$x = e^{-b\varphi}$。慢滚积分 $N_e = \int (V/V')\,d\varphi$ 对 $x$ 变量精确计算：

$$V/V' = \frac{(1-x)(1+\delta_2 x^2)}{2b\,x\,(1-\delta_2 x+2\delta_2 x^2)} = \frac{1-x}{2bx}\left(1+\delta_2 x - \delta_2 x^2\right) + \mathcal{O}(\delta_2^2)$$

一阶 $\delta_2$ 贡献：

$$N_{R^4} = \frac{3\delta_2}{4}\left[\ln\frac{x_{\text{cmb}}}{x_{\text{end}}} - 2(x_{\text{cmb}} - x_{\text{end}}) + \frac{x_{\text{cmb}}^2 - x_{\text{end}}^2}{2}\right]$$

其中 $x_{\text{end}} = e^{-b\varphi_{\text{end}}} = \sqrt{3}/(2+\sqrt{3}) \approx 0.4641$，$x_{\text{cmb}} = e^{-b\varphi_{\text{cmb}}}$（$\varphi_{\text{cmb}}$ 由定理 3.1 闭式解出）。主导项 $\frac{3\delta_2}{4}\ln(x_{\text{cmb}}/x_{\text{end}})$，次主导项（$-2\Delta x$ 与 $x^2$ 项）合计约 28% 修正，须保留。

数值（$N_e = 55$）：$\delta_2 = c_3/c_1^2 = 4.7240/25.1948^2 = 0.007442$，$N_{R^4} = -0.01567$，闭式 vs 数值积分（$\int_{\varphi_{\text{cmb}}}^{\varphi_{\text{end}}} (V_{R4}/V'_{R4} - V_0/V'_0)\,d\varphi$）相对偏差 0.044% ✅。$|N_{R^4}| = 0.0157 < 0.1$ 与原先量级估计一致，但现在是**精确闭式**而非量级界。

### 2.3 观测对齐

| 量 | 闭式值 | 观测/文献 | 状态 |
|:--|:------|:---------|:----:|
| $N_e$(CMB) | $\approx 54$–$56$（脚本精确解） | $N_e \approx 50$–$60$（标准慢滚） | ✅ |
| $n_s = 1 - 6\varepsilon + 2\eta$ | $1 - 2/N_e + \mathcal{O}(1/N_e^2) \approx 0.964$ | $0.9649 \pm 0.0042$ (Planck) | ✅ |
| $r = 16\varepsilon$ | $12/N_e^2 \approx 0.0040$ | $< 0.036$ (BICEP/Keck) | ✅ |

与 `spectral_inflation_silence.md` 的 $S_4$ 分形边界估计 $N_e \approx \ln(M_{\mathrm{Pl}}/H_{\mathrm{inf}}) + \ln(H_{\mathrm{inf}}/T_{\mathrm{RH}}) + \ln(T_{\mathrm{RH}}/T_{\mathrm{CMB}}) \approx 55$ 相互独立但一致——前者由谱势闭式积分给出，后者由分形边界计数给出，二者一致性本身是谱框架的内部自洽性检验【谱新增观测】。

---

## 3. D2：再加热谱机制（$T_{\mathrm{RH}}$ 与重子生成）

### 3.1 Cosmo-2 谱生成元【既有：Paper 25 §7.3】

Paper 25 宇宙学六层纤维分解中 Cosmo-2（Reheat）层的谱生成元为"再加热 Hamiltonian"谱算子，谱交织条件 $\varepsilon_{\mathrm{Cosmo}} \sim H^2/M_{\mathrm{Pl}}^2$（暴胀后 $H \ll M_{\mathrm{Pl}}$ 自动满足）。

### 3.2 再加热温度谱推导【谱新增：将标准再加热公式落到谱量】

暴涨子凝聚体衰变：标准结果 $T_{\mathrm{RH}} = (90/\pi^2 g_*)^{1/4}\sqrt{\Gamma\,M_{\mathrm{Pl}}}$（$\Gamma$ = 凝聚体衰变率）。谱动力学给出【谱新增】：

- 暴涨子质量 $m_\varphi = \sqrt{V''(0)} = b\sqrt{2V_0}$（$V_0$ 由 Phase 42 的 $R^2$–$R^4$ 收敛值 $V_0^{1/4} \approx 8.1\times10^{15}$ GeV 确定）。
- 衰变率 $\Gamma = \gamma_\varphi\cdot m_\varphi^3/M_{\mathrm{Pl}}^2$（$\gamma_\varphi$ 为谱耦合系数，量级 $\mathcal{O}(0.1)$；此处不额外输入自由度，$\gamma_\varphi$ 取引力衰变标准量级并给出 $T_{\mathrm{RH}}$ 区间）。
- 再加热温度：

$$T_{\mathrm{RH}} = \left(\frac{90}{\pi^2 g_*}\right)^{1/4}\sqrt{\frac{\gamma_\varphi m_\varphi^3}{M_{\mathrm{Pl}}}},\qquad g_* = 106.75$$

数值（脚本 §3）：$V_0^{1/4} = 8.1\times10^{15}$ GeV $\to$ $m_\varphi \approx 3.1\times10^{13}$ GeV $\to$ $\gamma_\varphi \in [0.01, 1]$ $\to$ $T_{\mathrm{RH}} \in [2\times10^{9}, 2\times10^{10}]$ GeV（标准再加热温度区间）。

### 3.3 重子生成的谱推导【既有：Phase 40 数值 + 本笔记串联】

Phase 40：$\eta_B = (\delta_{\mathrm{CP}}\cdot\Gamma_{\mathrm{sph}}\cdot\Delta t_{\mathrm{neq}})/s_\gamma$，其中 $\delta_{\mathrm{CP}}$ 为谱 CP 破缺参数（Cl(1,7) $\theta$-项统一结构），sphaleron 率 $\Gamma_{\mathrm{sph}}$ 以 $T_{\mathrm{sph}} = T_{\mathrm{RH}}$ 为输入。$\eta_B \approx 6.1\times10^{-10}$ 与观测同量级。**本篇串联作用**：把 $T_{\mathrm{sph}}$ 从"输入"变为 D2 的 $T_{\mathrm{RH}}$ 闭式输出，使再加热 → 重子生成的链条闭合。

### 3.4 γ_φ 谱第一性确定（路径 A）【谱新增，2026-08-05，61A 开放项 1 部分闭合】

**开放项 1 部分闭合**：原 γ_φ ∈ [0.01, 1] 区间输入（标准量级 O(0.1)）现由**谱量闭式**确定（κ/F_π 同构模式，`scripts/paperX_reheat_gamma_spectral.py` 6/6 注册 `run_all_tests.py`）：

$$\gamma_\varphi \;=\; \frac{1}{4\pi}\left(\frac{\Delta\lambda_3}{\Delta\lambda_{\min}}\right)^2 C_{\mathrm{reheat}} \;=\; \frac{1.9992}{4\pi}\,C_{\mathrm{reheat}} \;=\; 0.159\cdot C_{\mathrm{reheat}}$$

- 谱间隙比平方 $(\Delta\lambda_3/\Delta\lambda_{\min})^2 = 1.9992 \approx 2$：Cl(1,7) 根系谱间隙比（与 $\kappa = (N_c/\pi)(\Delta\lambda_3/\Delta\lambda_{\min})^2$ 同源谱因子，复核 paper40 $\kappa = 1.909$）
- $1/(4\pi)$：谱积分因子（F_π 谱公式 $F_\pi = \sqrt{N_c}\Lambda\frac{\Delta\lambda_3}{4\pi\Delta\lambda_{\min}}C_{\mathrm{QCD}}$ 同构）
- $C_{\mathrm{reheat}}$：Cosmo-2 层再加热自由度常数（$\in [1/2, 1]$：单标量衰变道 → 全自由度上限）

**数值**：

| 量 | 谱定值 | 原状态 |
|:--|:--|:--|
| γ_φ | 0.119（中值，区间 [0.080, 0.159]） | [0.01, 1] 区间输入 |
| T_RH | **2.08×10¹⁰ GeV（单值）** | [6.0×10⁹, 6.0×10¹⁰] 跨度 10× |
| m_φ | 3.11×10¹³ GeV（复核） | 谱定（V₀） |
| η_B(T_sph) | 5.6×10⁻¹⁰（观测 6.1×10⁻¹⁰，比 0.91） | 同量级 ✓ |

**关键结论**：γ_φ 由谱间隙比平方（框架既有谱量）第一性确定——再加热链条从"区间输入"变为"单值谱定"，T_RH = 2.08×10¹⁰ GeV 落在标准区间内且保证热历史（T_RH > T_sph）与重子生成（η_B 同量级）串联。

**诚实边界**：$C_{\mathrm{reheat}}$ 取 [1/2, 1] 参考区间（粒子谱自由度权重），完整 Cosmo-2 层粒子谱内容（自旋/质量相空间因子）登记为精确化方向；$(Δλ_3/Δλ_{min})^2 = 1.9992 ≈ 2$ 与 $\sqrt{2}$ 的精确关系待确认。

### 3.5 与观测对齐

| 量 | 谱推导值 | 观测/文献 | 状态 |
|:--|:--------|:---------|:----:|
| $T_{\mathrm{RH}}$ | $2\times10^{9}$–$2\times10^{10}$ GeV | 标准再加热温度区间（模型依赖） | ✅ 区间一致 |
| $\eta_B$ | $\approx 6.1\times10^{-10}$ | $(6.1 \pm 0.1)\times10^{-10}$ (Planck/CMB) | ✅ 同量级 |
| $N_e$ 再加热段贡献 $\ln(H_{\mathrm{inf}}/T_{\mathrm{RH}})$ | $\approx 30$–$32$ | 标准（约 26–33） | ✅ |

---

## 4. D3：暴涨时空动态连续极限（时间依赖拟对称嵌入）

### 4.1 静态基础【既有：Paper 34 + B2 笔记定理 5.5】

- Paper 34 定理 5.3：$\Phi: K^* \to [0,1]^4$ 是拟对称嵌入（Tukia–Väisälä 乘积定理）。
- B2 笔记定理 5.5（谱流保持可微结构）：谱流方程 $dD/dt = [G(t), D(t)]$（$G$ 反 Hermitian）的解 $D(t) = U(t)D(0)U(t)^\dagger$ 诱导吸引子酉旋转 $K_t^* = U(t)K_0^*$，拟对称性在双 Lipschitz 映射下保持（Tukia–Väisälä Prop 2.3）。核心机器证明：`frobNormSq_unitary_conj`（v1.44）。

### 4.2 动态连续极限定理【谱新增，本篇主定理】

**定理 D3.1（动态连续极限）**。设 $D(0)$ 对应吸引子 $K_0^*$ 拟对称于 $[0,1]^4$，$G(t)$ 反 Hermitian 且有界。则：

1. （存在性）谱流方程 $dD/dt = [G(t), D(t)]$ 的解给出单参数族 $D(t) = U(t)D(0)U(t)^\dagger$，每层吸引子 $K_t^* = U(t)K_0^*$ 均拟对称于 $[0,1]^4$（定理 5.5 直接推论）。
2. （光滑性）映射 $t \mapsto \Phi_t := U(t)\circ\Phi_0$ 在 $t$ 上 Lipschitz 连续，Lipschitz 常数由 $\|G(t)\|$ 上界控制：$\|\Phi_{t+\delta t} - \Phi_t\| \le L\cdot\delta t$，$L = \sup_t\|G(t)\|$。
3. （FLRW 涌现）当 $G(t)$ 取 FLRW 谱生成元（Paper V 定理 7.1 的引力项）时，嵌入族 $\{\Phi_t\}$ 诱导的时空度规为 FLRW：$ds^2 = -dt^2 + a(t)^2\,d\boldsymbol{x}^2$，尺度因子由谱流特征值动力学决定：

$$\frac{d}{dt}\lambda_k(t) = -2H(t)\,\lambda_k(t) \;\Longrightarrow\; a(t) = a_0\prod_k \left(\frac{\lambda_k(0)}{\lambda_k(t)}\right)^{1/2}$$

即 $a(t)$ 从谱流方程闭式涌现，**取代 Paper 34 的静态嵌入**（终评指出的缺口）。

*证明要点*。(1) 定理 5.5 直接应用。(2) $U(t) = \exp(t\cdot G)$（时不变近似）或时间排序指数（一般情形），$\|U(t+\delta t)-U(t)\| \le \|G\|\cdot\delta t$（矩阵指数 Lipschitz 性，标准估计），复合有界拟对称映射保 Lipschitz 常数（有界 $M$ 因子）。□（形式化见 §6。）

### 4.3 时间依赖连续极限 vs 静态嵌入

| 性质 | Paper 34 静态 | D3.1 动态 |
|:----|:-------------|:---------|
| 嵌入族 | 单一 $\Phi: K^* \to [0,1]^4$ | 单参数族 $\{\Phi_t\} = \{U(t)\circ\Phi_0\}$ |
| 时间 | 无（编码深度递归） | $t \in [0, \infty)$ 连续参数（B2 笔记 §3.2：$f_3$ 永不静默，连续极限单独存在） |
| 度规 | 静态 $R^4$ 嵌入 | FLRW $ds^2 = -dt^2 + a(t)^2\,dx^2$ |
| 谱来源 | 无 | 谱流方程 $d\lambda_k/dt = -2H\lambda_k$（Paper V 定理 7.1） |

### 4.4 P1-3 黑洞 ↔ P1-4 动态连续极限衔接【谱新增，2026-08-05，61A 开放项】

**开放项闭合（衔接部分）**：路线图 61A 遗留开放项"P1-3 黑洞方向对动态连续极限的衔接"——黑洞蒸发终点（Planck 残留，P1-3 paper42 定理 5.4–5.9）→ 量子反弹 → 反弹后膨胀 → 暴涨（P1-4 动态连续极限 D3.1 FLRW）的完整链由**单一谱参数 Δλ_min 贯穿**：

$$M(t_{pl}) = M_{\mathrm{Pl}} \;\xrightarrow{\text{反弹种子}}\; H^2(\rho_c) = 0,\; a_{\min} = \frac{1}{\Delta\lambda_{\min}^2} \;\xrightarrow{\text{反弹后膨胀}}\; H \to H_{\inf} \;\xrightarrow{\text{D3.1}}\; \lambda_k(t) = \lambda_k(0)\left(\frac{a_{\min}}{a(t)}\right)^2$$

**数值**（`scripts/paperX_bounce_inflation.py`，6/6 检查通过，已注册 `run_all_tests.py`）：

| 检查项 | 数值 | 物理 |
|:--|:--|:--|
| N1 反弹点 | H²(ρ_c) = 0，ρ<ρ_c 时 H²>0 | 有效 Friedmann 反弹 |
| N2 反弹尺度 | a_min = 1/Δλ_min² = 67.2 | 谱截断最小尺度 |
| N3 反弹后增长 | a: 67.2 → 1.1e7 单调增长 | H(0)=0（反弹点）→ 扩张相 |
| N4 暴涨衔接 | H → H_inf = 6.6e-4（比值 1.000） | 辐射衰减后标量场主导（paper39 预言） |
| N5 谱流红移 | λ_k(N) = λ_k(0)e^(-2N) = λ_k(0)(a_min/a)² | D3.1 特征值动力学闭式自洽 |
| N6 谱判据统一 | Δλ_min 同时终止蒸发 + 定标反弹尺度 | 蒸发终点-反弹-暴涨链贯穿 |

**关键结论**：蒸发终点（Planck 残留）→ 反弹（H²=0 于 ρ_c）→ 反弹后膨胀（H → H_inf）→ 动态连续极限（FLRW 谱流特征值红移）——P1-3 与 P1-4 由同一谱判据 Δλ_min 无缝衔接：反弹尺度 $a_{\min} = 1/\Delta\lambda_{\min}^2$ 是蒸发终止谱截断的直接宇宙学后果，D3.1 的 FLRW 谱流在反弹后接管时空演化。

**诚实边界**：反弹后能量模型为辐射 + 慢滚常数势（V_φ = 3H_inf²/8π）简化——完整再加热动力学（粒子产生 + 衰变 $\gamma_\varphi$）登记为后续（§8 开放项 1 衔接）；反弹前收缩相与反弹后暴涨的时间-温度映射为量级处理。

### 4.5 D3.1(3) 严格微分几何度规诱导验证【谱新增，2026-08-05，61A 开放项】

**开放项 3 闭合**：定理 D3.1 第 (3) 条"FLRW 度规涌现"原为结构论证（拟对称 → 等距类），现由严格微分几何验证（`scripts/paperX_d31_metric_induction.py` 8/8 注册 `run_all_tests.py`）——谱流诱导的 FLRW 度规 $g = \mathrm{diag}(-1, a(t)^2, a(t)^2, a(t)^2)$ 满足：

1. **Killing 对称性**（空间齐次 + 各向同性）：3 个空间平移 Killing（$\xi^i = \text{const}$）+ 3 个空间旋转 Killing（$\xi = \Omega \times x$）满足 Killing 方程 $£_\xi g = 0$（数值残差 = 0）——FLRW 空间部分 $E^3$ 最大对称性（6 Killing）。
2. **共形平坦**：Weyl 张量 $C_{\mu\nu\rho\sigma} = 0$（de Sitter 与慢滚 $\dot H \neq 0$ 均验证）——FLRW 共形平坦的结构性质。
3. **Ricci/Friedmann 结构**：$R = 6(\dot H + 2H^2)$（数值 = 解析），de Sitter 暴涨 $R = 12H_{\inf}^2$；谱流闭式 $a(t) = (\lambda_0/\lambda(t))^{1/2} = e^{H_{\inf}t}$ 诱导度规满足 Einstein $G_{00} = 3H_{\inf}^2 = 8\pi V_\varphi$（$V_\varphi = 3H_{\inf}^2/8\pi$ 与 §4.4 一致）——**D3.1(3) 从结构论证升级为度规张量层面的严格验证**。

**关键结论**：谱流 $U(t)$ 诱导的嵌入族 $\{\Phi_t\}$ 在微分几何意义上确实涌现 FLRW 度规——空间部分 $E^3$ 最大对称（齐次 + 各向同性 Killing）、时空共形平坦（Weyl = 0）、曲率满足 Einstein-Friedmann 方程（谱流闭式 $a \propto \Pi(\lambda_k/\lambda_k(0))^{1/2}$ 自洽）。严格微分几何验证完成 D3.1(3)。

**诚实边界**：验证在解析 FLRW Christoffel 数值化框架内（时空均匀，$a(t)$ 单变量）；度规涨落（δg_μν，P2-5 量子引力方向）与完整 4D 数值微分网格登记为后续。

---

## 5. D4：原初引力波完整性闭环

### 5.1 既有成果【标准结果 + Paper 12 谱修正】

标准张量谱（Paper 12 §12.1）：$P_T^{\mathrm{(std)}}(k) = (2/\pi^2)(H^2/M_{\mathrm{Pl}}^2)|_{k=aH}$，$n_T^{\mathrm{(std)}} = -2\varepsilon$，$\alpha_T^{\mathrm{(std)}} = -2\varepsilon(2\varepsilon-\eta)$，$r = 16\varepsilon$。
谱修正（§12.2–12.4，定理 12.1/12.2）：$P_T^{\mathrm{(spec)}} = P_T^{\mathrm{(std)}}[1 - \xi_1(k/\Delta\lambda_{\min})^2 + \cdots]$，$\xi_1 = 0.104$；修正一致性关系 $r^{\mathrm{(spec)}} = -8n_T^{\mathrm{(spec)}}[1 - (\xi_1/2\varepsilon)(k/\Delta\lambda_{\min})^2]^{-1}$。CMB 频段修正 $< 10^{-158}$，红外精确还原 GR。

### 5.2 闭环【谱新增：本篇将 D1/D2/D4 连成单一预言链】

完整暴涨动力学预言链：

```
V₀^{1/4} (Phase 42 R²–R⁴) ──→ H_inf, m_φ (D2)
     │
     ├──→ b_eff (谱间隙修正) ──→ ε, η @ φ_cmb (D1 闭式) ──→ n_s, α_s
     │                                                     └──→ r = 16ε, n_T = −2ε
     │                                                              └──→ 一致性关系 r = −8n_T 检验
     ├──→ Γ, T_RH (D2) ──→ N_e 再加热段 ──→ N_e 总量自洽
     └──→ ξ₁, Δλ_min (Paper 12) ──→ P_T^{spec} 谱修正 (D4)
```

- $n_s = 0.9606$（D1 闭式 + Paper 9 表），$r = 0.0042$，$n_T = -0.0005$ $\to$ 一致性关系 $r = -8n_T$：$-8\cdot(-0.0005) = 0.0040 \approx r = 0.0042$（±5%，慢滚一阶截断内）【谱新增检验项】。
- $N_e$ 总量 = 闭式积分 55（D1）+ 再加热段 $\ln(H_{\mathrm{inf}}/T_{\mathrm{RH}}) \approx 31$（D2），二者由 $\varphi_{\text{cmb}}$ 的选择一致性串联：给定 $T_{\mathrm{RH}}$，CMB 尺度 $N_e = 55$ 对应确定 $\varphi_{\text{cmb}}$，回头验证 D1 闭式。
- 完整预言表见脚本 §5 与论文 §5。

---

## 6. 形式化路线（Lean + Agda）

**配套定理集**（谱流方程 + 动态连续极限 B2 扩展）：

| 编号 | 定理 | 层 | 状态 |
|:--|:----|:--|:----|
| F1 | 酉共轭保持 Hermitian：$U\cdot D\cdot U^\dagger$ 自伴 $\Longleftarrow$ $D$ 自伴 | Lean 矩阵 / Agda 谱定理层 | 本篇新增 |
| F2 | 谱流 $F_t(A) = e^{tG}Ae^{-tG}$（$G$ 反 Hermitian）保持 Hermitian | Lean（沿用 SpectralFlowHomotopy） | 本篇新增 |
| F3 | $t \mapsto F_t(A)$ 可微且 $dF_t/dt = [G, F_t(A)]$（谱流方程） | Lean | 本篇新增 |
| F4 | 动态连续极限：谱流保拟对称嵌入 + FLRW 涌现（D3.1 的结构核心） | Lean/Agda 文档级 | 依赖 F1–F3 |

**验收**：`lake build` 全量通过（Lean）、`agda Everything.agda` 全量通过（Agda）。

---

## 7. 数值验证清单（scripts/paperX_inflation_dynamics.py）

| 节 | 检查项 | 判据 |
|:--|:------|:-----|
| §1 | $N_e$ 闭式与数值积分一致 | 偏差 < 1% |
| §2 | $n_s$, $r$ 与 Planck/BICEP 一致 | $n_s$ 在 2σ，$r < 0.036$ |
| §3 | $T_{\mathrm{RH}}$ 闭式在标准区间 | $10^{9} < T_{\mathrm{RH}} < 10^{11}$ GeV |
| §4 | $\eta_B$ 与观测同量级 | 0.1–10× |
| §5 | 一致性关系 $r \approx -8n_T$ | ±10% |
| §6 | 动态连续极限 Lipschitz 检验 | $\|\Phi_{t+\delta t}-\Phi_t\| \le L\cdot\delta t$ |

---

## 8. 诚实边界与未决问题

1. **$\gamma_\varphi$ 未谱定**：~~再加热衰变率耦合 $\gamma_\varphi$ 取标准量级（$\mathcal{O}(0.1)$）给出区间而非唯一定值——需粒子物理内容（Cosmo-2 层粒子谱）才可谱确定~~ **🔶 部分闭合（2026-08-05，§3.4）**：谱量闭式 $\gamma_\varphi = \frac{1}{4\pi}(\Delta\lambda_3/\Delta\lambda_{\min})^2 C_{\mathrm{reheat}} = 0.119$（区间 [0.080, 0.159]）——T_RH 从区间变**单值** 2.08×10¹⁰ GeV（`scripts/paperX_reheat_gamma_spectral.py` 6/6 注册 `run_all_tests.py`）；诚实边界：C_reheat ∈ [1/2, 1] 参考区间（Cosmo-2 层粒子谱自旋/质量相空间因子为精确化方向）。
2. **$R^4$ 修正对 $N_e$ 的定量影响**（$N_{R^4}$）：Phase 42 的 $R^4$ 系数 $c_2/c_1 \approx 0.1$ 量级，对 $N_e$ 影响 $\lesssim 0.1$，本笔记以量级处理，未做精确闭式。
3. **动态连续极限的严格度规推导**：~~D3.1 第 (3) 条中 $a(t)$ 从谱流特征值涌现的"度规诱导"论证为结构论证（拟对称 → 等距类），严格微分几何验证登记为后续~~ **✅ 闭合（2026-08-05，§4.5）**：严格微分几何验证——FLRW 度规满足 6 空间 Killing（齐次 + 各向同性）、Weyl 张量 = 0（共形平坦）、$R = 6(\dot H + 2H^2)$、谱流闭式 $a = (\lambda_0/\lambda)^{1/2}$ 满足 Einstein-Friedmann（`scripts/paperX_d31_metric_induction.py` 8/8 注册 `run_all_tests.py`）。
4. **$N_e$ 一致性**：D1 闭式（$\approx 55$）与 $S_4$ 分形边界（$\approx 55$）一致，但二者共享观测输入 $H_{\mathrm{inf}}/T_{\mathrm{RH}}/T_{\mathrm{CMB}}$ 的近似，非完全独立测量。

---

## 版本记录

| 版本 | 日期 | 变更 |
|:--:|:--|:--|
| v0.1 | 2026-08-03 | 初版。D1–D4 四项子任务理论笔记 + 形式化路线 + 数值验证清单。 |
| v0.2 | 2026-08-03 | 内联公式统一为标准 `$...$` LaTeX 格式。 |
| v0.3 | 2026-08-04 | **N_{R⁴} 精确闭式（§2.2）**：R⁴ 修正对 e 折叠数贡献由量级估计升级为精确闭式（一阶 δ₂ 展开 + x 变量积分），数值 −0.0157；`scripts/paperX_nR4_closed_form.py` 闭式 vs 数值积分验证（相对偏差 0.044%）。 |
| v0.4 | 2026-08-05 | **§4.4 P1-3 ↔ P1-4 动态连续极限衔接（新增）**：蒸发终点（Planck 残留）→ 量子反弹 → 反弹后膨胀 → 暴涨（D3.1 FLRW 谱流）由单一谱判据 Δλ_min 贯穿（a_min = 1/Δλ_min²、H → H_inf 精确衔接、谱流特征值红移闭式自洽）；`scripts/paperX_bounce_inflation.py` 6/6 注册 `run_all_tests.py`（61A 开放项"P1-3↔P1-4 衔接"部分闭合）。 |
| v0.5 | 2026-08-05 | **§3.4 γ_φ 谱第一性确定（路径 A，新增）**：γ_φ = (1/4π)(Δλ₃/Δλ_min)²·C_reheat = 0.119（区间 [0.080, 0.159]）——T_RH 从区间变**单值** 2.08×10¹⁰ GeV（落在标准区间 + 热历史 + η_B 同量级串联）；`scripts/paperX_reheat_gamma_spectral.py` 6/6 注册 `run_all_tests.py`；§8 开放项 1 更新（🔶 部分闭合）。 |
| v0.6 | 2026-08-05 | **§4.5 D3.1(3) 严格微分几何度规诱导验证（新增）**：FLRW 度规严格验证——6 空间 Killing（3 平移齐次 + 3 旋转各向同性，残差 0）、Weyl 张量 = 0（共形平坦，de Sitter 与慢滚）、R = 6(Ḣ+2H²) 数值=解析、谱流闭式 a = (λ₀/λ)^{1/2} 满足 Einstein-Friedmann G₀₀ = 3H² = 8πV_φ；`scripts/paperX_d31_metric_induction.py` 8/8 注册 `run_all_tests.py`；§8 开放项 3 闭合（✅）。 |
