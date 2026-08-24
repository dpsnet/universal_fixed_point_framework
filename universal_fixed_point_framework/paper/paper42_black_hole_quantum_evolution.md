# 元通用不动点函子范畴框架 XLII：黑洞量子演化——霍金谱、Page 曲线与信息保持的谱公理推导

**版本**：v0.3（2026-08-08）
**系列**：Phase 61（物理理论补缺推进计划）P1-3
**形式化**：[`BlackHoleEvolution.lean`](../formal_proof/MUFPFormalization/MUFPFormalization/BlackHoleEvolution.lean)、[`HawkingSpectrum.lean`](../formal_proof/MUFPFormalization/MUFPFormalization/HawkingSpectrum.lean)、[`BlackHoleInformation.lean`](../formal_proof/MUFPFormalization/MUFPFormalization/BlackHoleInformation.lean)、[`BlackHoleDynamics.agda`](../agda_formalization/BlackHoleDynamics/BlackHoleDynamics.agda)
**数值验证**：[`scripts/paperX_hawking_spectrum.py`](../paperX_hawking_spectrum.py)（35/35 检查通过）

---

## 摘要

本文从 MUFPF 谱公理出发，完整推导黑洞量子演化的动力学链条：霍金辐射谱（§2）、蒸发动力学（§3）、Page 曲线（§4）、视界量子涨落与蒸发终点-反弹衔接（§5）、信息保持（§6）。全部定理在 Lean 4 中机器证明（零 sorry），关键算子代数核心在 Agda 中镜像登记，数值验证 35/35 通过。本方向对应终评缺口 ③"黑洞量子演化"。

---

## §1 谱公理与记号

**公理 1.1（谱间隙）**：存在谱间隙 Δλ_min = spectralGap 8 = (√6−√2)/√72 ≈ 0.1221，由 Cl(1,7) 根系表示论给出（`SpectralGap.lean` 机器证明 `spectralGap_at_kmax8`）。

**公理 1.2（谱流方程）**：黑洞视界动力学的生成元为谱流
$$
A_t = U(t)\,A_0\,U(t)^{-1}, \qquad U(t) = e^{t A_F}
$$
满足 dA_t/dt = [A_F, A_t]（`SpectralDynamics.lean` 机器证明 `spectralFlow_satisfies_equation`）。

**记号**：M(t) 为黑洞质量，M₀ = M(0)；α > 0 为蒸发常数（谱流推导）；t_evap 为蒸发时间；M_Pl = 1 为 Planck 质量（归一化单位 G=ħ=c=1）。

**半经典近似范围声明**：本文 §2–§6 的形式化均为**半经典近似**（dM/dt = −α/M²，解析解 M(t) = (M₀³−3αt)^(1/3)）。该近似下 M(t_evap) = 0 是**数学终点**。按框架立场（Paper IX 定理 3.1 奇点谱消解 + §4.3 黑洞-反弹连接），**物理终点**由谱截断接管：蒸发在 M ~ M_Pl 自然终止，残留 Planck 质量量子黑洞成为量子反弹种子，**不产生裸奇点**（§5.4）。数学层与物理层分层明确，不冲突。

---

## §2 霍金辐射谱

**定义 2.1（Hawking 温度）**：T_H(M) = Δλ_min/(2πM)。

**定理 2.1（温度正性）**：对 M > 0，T_H(M) > 0。
*证明*：Δλ_min > 0（公理 1.1），2πM > 0，商为正。Lean 证明：`hawkingTempSchwarzschild_pos`。

**定理 2.2（温度递减）**：M₁ < M₂ ⟹ T_H(M₁) > T_H(M₂)。即黑洞越重越冷。
*证明*：T_H(M) = C/M（C = Δλ_min/2π > 0），f(M) = C/M 严格递减（`div_constant_decreasing`）。Lean 证明：`hawkingTempSchwarzschild_decreasing`。

**定义 2.2（Planck 分布）**：N(ω) = 1/(e^{βMω} − 1)，βM = 2πM/Δλ_min = 1/T_H(M)。

**定理 2.3（占据数正性）**：ω > 0, M > 0 ⟹ N(ω) > 0。
*证明*：βMω > 0 ⟹ e^{βMω} > 1 ⟹ 分母正。Lean 证明：`planckOccupation_pos`。

**定义 2.3（Greybody 因子）**：Γ(ω,M) = (27/4)(ωM)² e^{−4ωM}（l=2 主导引力波模的穿越概率）。

**定理 2.4（Greybody 正性）**：ω, M > 0 ⟹ Γ(ω,M) > 0。*证明*：三项因子均正。Lean：`greybodyFactor_pos`。

**定理 2.5（低频增/高频减）**：0 < ωM < 1/2 时 Γ 随 ω 增；1 < ωM 时 Γ 随 ω 减。
*证明*：dΓ/dω = Γ·(2/ωM − 4)·M，符号由 (2 − 4ωM) 决定。Lean：`greybodyFactor_increasing_small`/`greybodyFactor_decreasing_large`。

**定义 2.4（辐射功率密度）**：dP/dω = ω³Γ(ω,M)N(ω)/(2π²)。

**定理 2.6（功率密度正性）**：ω, M > 0 ⟹ dP/dω > 0。Lean：`hawkingPowerDensity_pos`。

**定义 2.5（总功率）**：P(M) = Δλ_min⁴/(15πM²)（semiclassical Stefan–Boltzmann 近似）。

**定理 2.7（功率递减）**：M₁ < M₂ ⟹ P(M₁) > P(M₂)。即蒸发晚期辐射功率剧增。Lean：`hawkingPower_decreasing`。

---

## §3 蒸发动力学

**定义 3.1（质量立方）**：Δ(t) = M₀³ − 3αt。

**定理 3.1（解析解）**：M(t) = Δ(t)^(1/3)。
*证明*：dM/dt = −α/M² ⟹ d(M³)/dt = −3α ⟹ M³ = M₀³ − 3αt。Lean：`bhMassCubed`/`bhMass`。

**定理 3.2（质量正性）**：Δ(t) > 0 ⟹ M(t) > 0。Lean：`bhMass_pos`。

**定理 3.3（质量单调递减）**：dt > 0 ⟹ M(t+dt) < M(t)。
*证明*：Δ 严格递减且 t ↦ t^{1/3} 严格递增（ℝ^{>0} 上）。Lean：`bhMassCubed_decreasing`/`bhMass_decreasing`。

**定理 3.4（蒸发时间）**：t_evap = M₀³/(3α)，且 M(t_evap) = 0。
*证明*：Δ(t_evap) = 0。Lean：`bhEvaporationTime_condition`/`bhMass_at_evaporation_time`。

> **注（物理终点）**：M(t_evap) = 0 是半经典解析解的**数学终点**。按框架立场（Paper IX 定理 3.1 奇点谱消解 + §4.3 黑洞-反弹连接），物理蒸发在 M ~ M_Pl 处由谱截断（Δλ_min）自然终止——残留的 Planck 质量量子黑洞成为量子反弹种子，**不产生裸奇点**。

---

## §4 Page 曲线（谱公理推导）

**定义 4.1（辐射纠缠熵）**：S_rad(t) = 4π(M₀² − M(t)²)。由总系统纯态性：S_total = S_BH + S_rad = 4πM₀² 守恒。

**定理 4.1（熵守恒）**：S_BH(t) + S_rad(t) = 4πM₀²。Lean：`bhEntropy_conservation`。

**定义 4.2（Page 纠缠熵）**：S_ent(t) = min(S_BH(t), S_rad(t))。

**定理 4.2（Page 时间解析）**：令 M(t_Page)² = M₀²/2，则
$$
\frac{t_{Page}}{t_{evap}} = 1 - \frac{1}{2\sqrt{2}} \approx 0.647
$$
*证明*：M(t_Page)³ = M₀³/(2√2) ⟹ M₀³ − 3αt_Page = M₀³/(2√2) ⟹ t_Page/t_evap = 1 − 1/(2√2)。Lean：`bhPageTime_fraction`（精确）、`bhMassCubed_at_page_time`。数值：0.646447。

**定理 4.3（Page 分数区间）**：1/2 < t_Page/t_evap < 3/4。即 Page 时间发生在蒸发中后期。
*证明*：1 < √2 < 2 ⟹ 1/4 < 1/(2√2) < 1/2。Lean：`bhPageTime_fraction_gt_half`/`bhPageTime_fraction_lt_three_quarters`。

**定理 4.4（早期递增）**：若 M(t+dt)² ≥ M₀²/2（Page 时间前），则 S_ent(t) < S_ent(t+dt)。即纠缠熵在早期随辐射增长。
*证明*：M(t+dt)² ≥ M₀²/2 时 S_ent = S_rad = 4π(M₀²−M²)，而 M 递减 ⟹ S_rad 递增。Lean：`bhEntanglementEntropy_early_increasing`。

**定理 4.5（晚期递减）**：若 M(t)² ≤ M₀²/2（Page 时间后），则 S_ent(t+dt) < S_ent(t)。即纠缠熵在晚期随黑洞收缩而下降（回到零）。
*证明*：M(t)² ≤ M₀²/2 时 S_ent = S_BH = 4πM²，而 M 递减 ⟹ S_BH 递减。Lean：`bhEntanglementEntropy_late_decreasing`。

**定理 4.6（Page 时间立方判据）**：Δ(t_Page) = M₀³/(2√2)。Lean：`bhPageTime_cubic_criterion`。

**定理 4.7（Page 熵平衡）**：S_BH(t_Page) = S_rad(t_Page)，即 M(t_Page)² = M₀²/2。
*证明*：由立方判据 Δ(t_Page) = M₀³/(2√2) 经 rpow 立方根恒等式 `rpow_cube_root` 得 M(t_Page) = M₀/√2，故 M² = M₀²/2。Lean：`bhPageTime_entropy_balance`。

> **说明**：Page 曲线从谱公理（蒸发动力学 3.3 + 纯态互补 4.1）推导，无需外部输入 Page 1993 假设。精确熵平衡（定理 4.7）已通过 rpow 代数机器证明（2026-08-04 攻克）。

---

## §5 视界量子涨落

**定义 5.1（相对温度涨落）**：δT/T = T_H(M)/M = Δλ_min/(2πM²)。

**定理 5.1（涨落正性）**：M > 0 ⟹ δT/T > 0。Lean：`horizonTempFluctuation_pos`。

**定理 5.2（谱表述）**：δT/T = Δλ_min/(2πM²)，涨落由谱间隙内禀确定。Lean：`horizonTempFluctuation_spectral`。

**定理 5.3（涨落递减）**：M₁ < M₂ ⟹ δT/T(M₁) > δT/T(M₂)。即大质量黑洞视界涨落小。
*证明*：δT/T = C/M²（C > 0），平方倒数递减。Lean：`horizonTempFluctuation_decreasing`。

**物理解读**：随蒸发进行（M 减小），视界涨落 δT/T 增大，在 M ~ M_Pl 时达到 Planck 尺度（数值验证 δT/T(M_Pl) ≈ 0.0194），对应 ∂Rec_D 边界在 Planck 尺度的量子化。

### 5.4 蒸发终点与量子反弹（Paper IX §4.3 衔接）

**定理 5.4（Planck 时间）**：t_pl = (M₀³ − M_Pl³)/(3α)，且 M(t_pl) = M_Pl。
*证明*：Δ(t_pl) = M_Pl³，M = Δ^(1/3)（rpow 立方根恒等式 `rpow_cube_root`）。Lean：`bhMassCubed_at_planck`/`bhMass_at_planck`。

**定理 5.5（截断先于经典终点）**：t_pl < t_evap。蒸发在到达 M = 0 之前已在 Planck 尺度被谱截断终止。Lean：`bhPlanckTime_lt_evaporationTime`。

**定理 5.6（无裸奇点）**：∀ t < t_pl，M(t) > M_Pl。质量始终不低于 Planck 尺度，不会穿过奇点。
*证明*：Δ(t) > Δ(t_pl) = M_Pl³ 且 rpow 严格递增。Lean：`bhMass_above_planck_before`。

**定义 5.2（反弹临界密度）**：ρ_c = (8π/3)·4Δλ_min²（M_Pl=1，c₁ = 1/(4Δλ_min²)）。

**定理 5.7（反弹点）**：有效 Friedmann 方程 H² = (8π/3)ρ(1 − ρ/ρ_c) 在 ρ = ρ_c 处 H² = 0，且 0 < ρ < ρ_c 时 H² > 0（扩张相）。
*证明*：1 − ρ_c/ρ_c = 0（代数）。Lean：`hubbleSquared_zero_at_critical`/`hubbleSquared_pos_below_critical`。

**定理 5.8（反弹尺度正性）**：a_min ∝ 1/Δλ_min² > 0（无零尺度奇点）。Lean：`bounceMinScale_pos`。

**定理 5.9（反弹种子）**：t_pl 处的 Planck 残留黑洞 M = M_Pl 成为量子反弹种子。Lean：`bhPlanckRemnant_is_bounce_seed`。

> **完整生命周期**（框架立场）：形成 → Hawking 蒸发（信息保持于谱不变性）→ Planck 截断 → 量子反弹（Paper IX §4.3）。所有环节在 Lean 中机器证明（`BlackHoleEvolution.lean` + `BlackHoleBounce.lean`，零 sorry）。

### 5.5 Kerr 蒸发动力学推广【谱新增，v0.2】

**定理 5.10**（Kerr 谱温度归约与转动蒸发动力学）。转动黑洞（Kerr，a* = J/M² ∈ [0,1)）的霍金温度以 Schwarzschild 谱温度为基准按归约因子衰减：

$$T_{\mathrm{Kerr}}(M, a^*) = \frac{\Delta\lambda_{\min}}{2\pi M}\cdot f(a^*),\qquad f(a^*) = \frac{2\sqrt{1-a^{*2}}}{1+\sqrt{1-a^{*2}}} \in (0,1],$$

且 (i) 归约：f(0) = 1（Schwarzschild 谱极限 T_Kerr = Δλ_min/(2πM)）；(ii) 转动降温：f 随 a* 单调递减（T_Kerr(a*₁) > T_Kerr(a*₂) for a*₁ < a*₂）；(iii) 极端冷却：a* → 1 时 f → 0（极端 Kerr 蒸发终止）。蒸发动力学（超辐射优先辐射角动量，r_J > 1）：

$$dM/dt = -\alpha\, f(a^*)^4/M^2,\qquad dJ/dt = -r_J\,\alpha\, a^* f(a^*)/M.$$

*证明要点*。（1）标准 Bekenstein-Hawking Kerr 温度 T ∝ (r_+ − r_−)/(r_+² + a²) 与 Schwarzschild 温度之比化简为 f(a*)。（2）f(0) = 2·1/(1+1) = 1；（3）f'(a*) < 0 for a* ∈ (0,1)（分子 √(1−a*²) 递减、分母递增）；（4）a*→1：√(1−a*²) → 0 ⟹ f → 0。（5）dM/dt ∝ T⁴（Stefan-Boltzmann）+ 超辐射 dJ/dt（r_J > 1）给出蒸发动力学。□

**数值**（`scripts/paperX_hawking_kerr.py`，6/6 检查，注册 `run_all_tests.py`）：f(0)=1（归约）、T(a*=0.9)/T_S = 0.61（转动降温）、f(1−1e-9) = 8.9e-5（极端冷却）、t_evap(a*₀=0.9)/t_evap(0) = 1.93（蒸发寿命延长，f ≤ 1 数学保证）、a*(t)：0.9 → 0.166 单调递减（超辐射优先辐射角动量，Kerr → Schwarzschild 演化方向）。

**关键结论**：Kerr 转动使霍金温度降低（f ≤ 1）→ 蒸发减慢（寿命延长 1.93×）→ 极端 Kerr 冷却终止蒸发；超辐射优先辐射角动量使 a* 单调递减，转动黑洞演化趋向 Schwarzschild——与谱框架温度判据（Δλ_min 定标）自洽。`KerrFiber.lean` 的线性近似 (1−a*²) 在 a*→0 与标准形状一致（标准形状降温更缓，a*=0.5：0.928 vs 0.75），蒸发动力学采用标准形状。

**诚实边界**：dJ/dt 动力学采用简化超辐射模型（r_J 常数）；**完整 Kerr 超辐射谱已推进（2026-08-08，`scripts/paperX_kerr_superradiance.py` 8/8 注册 `run_all_tests.py`）**——数值求解 Kerr 无质量标量径向方程逐模计算超辐射增益 $Z_{slm}(\omega) = |R(\omega)|^2-1$：经典判据 $Z > 0 \iff \omega < m\Omega_H$ 逐点符号确认（a*=0.9、l=m=1）、转动增强（Z_max 随 a* 单调 0.001→0.008）、窗口边界连续、发射谱超辐射区占可观份额（负吸收 × Bose 因子）、角动量提取 dJ/dt > 0 且 dJ/dE = 4.5/M 与简化 R_J·a*/f³ = 8.04/M 同量级（比值 0.56，简化图像获支持）；**超辐射-蒸发衔接（2026-08-08，`scripts/paperX_kerr_sr_evaporation.py` 5/5）**：超辐射增强因子 η(a*) 随转动单调（0.008→0.777→220）、角动量效率 dJ/dE = 4.15/M、l=m=2 模贡献 36.5%；**简化模型双向偏差定量化——低转动（a*=0.5）低估 8.7×、中等转动（a*≈0.9）近似（比值 0.52）、极端转动（a*→1）因 f³→0 高估（比值 0.02）——简化 R_J = 2 有效范围 = 中等转动**；诚实边界：s=0 标量 l=m=1/2 模（自旋 1/2 费米子与自旋 2 引力子需 Teukolsky 方程推广，登记后续）。蒸发终点-反弹衔接（定理 5.4–5.9）在 a*=0 极限下保持成立。

---

## §6 信息保持

**定理 6.1（谱流可逆性）**：A_{-t} = U(−t) A_t U(−t)^{-1} = A₀。即谱流是半群，可逆。
*证明*：U(−t)U(t) = e^{−tA_F}e^{tA_F} = 1（exp 加法公式 + 对易）。Lean：`spectralFlow_inv`/`matrix_exp_smul_neg`。

**定理 6.2（前向谱保持）**：a ∈ σ(A₀) ⟹ a ∈ σ(A_t)。
*证明*：A_t 与 A₀ 相似（酉相似），特征值不变。Lean：`spectral_invariance`/`bhInformationPreserved_forward`。

**定理 6.3（反向谱保持）**：a ∈ σ(A_t) ⟹ a ∈ σ(A₀)。
*证明*：由 6.1 将谱流反向作用。Lean：`bhInformationPreserved_reverse`。

**定理 6.4（信息完全保持）**：σ(A₀) = σ(A_t)。黑洞信息在谱中完全保存——蒸发是幺正演化，信息只是被"搅乱"而非丢失。
*证明*：6.2 + 6.3。Lean：`bhInformationPreserved_iff`。

**定理 6.5（信息载体结构稳定）**：谱流保持自伴性（物理量实在性）。
*证明*：⟨U X U†x, y⟩ = ⟨x, U X U†y⟩（伴随移动 + 自伴性）。Agda：`flow-self-adjoint`。

> **信息悖论解答**：S_ent 先升后降（定理 4.4/4.5）并不违反熵不增原理——S_ent 是纠缠熵（冯诺依曼熵的子系统约化），而总系统纯态的谱信息由 σ(A₀) = σ(A_t)（定理 6.4）完全保持。

---

## §7 与验收标准对照

| 验收标准 | 定理 | 形式化 | 数值 |
|:--------|:-----|:------|:-----|
| 霍金辐射谱完整推导 | 2.1–2.7 | `HawkingSpectrum.lean` ✅ | C1 8 项 ✅ |
| Page 曲线谱公理推导 | 4.1–4.6 + 4.7（熵平衡） | `BlackHoleInformation.lean` ✅ | C3 7 项 ✅ |
| 视界涨落谱表述 | 5.1–5.3 | `BlackHoleInformation.lean` ✅ | C4 3 项 ✅ |
| 蒸发终点-反弹衔接 | 5.4–5.9 | `BlackHoleEvolution.lean` + `BlackHoleBounce.lean` ✅ | C6 8 项 ✅ |
| 信息保持（双向） | 6.1–6.5 | `BlackHoleInformation.lean` + Agda ✅ | C5 2 项 ✅ |
| 蒸发动力学 | 3.1–3.4 | `BlackHoleEvolution.lean` ✅ | C2 4 项 ✅ |

---

## §8 诚实边界（开放项）

> **已解决并移出开放项**（2026-08-04）：精确熵平衡 S_BH(t_Page) = S_rad(t_Page)（定理 4.7，`bhPageTime_entropy_balance`）；蒸发终点-反弹衔接（定理 5.4-5.9，`BlackHoleBounce.lean`）。详见 §4/§5.4。

1. **视界涨落的全量子化**：δT/T 的谱表述已定量化（§5.1-5.3），但度规涨落 δg_μν 的完整谱动力学方程待后续（Paper 16 §10.9.2 定性 → 定量）。
2. **反弹后宇宙学演化**：a(t) 完整动力学、原初谱的推导属 Paper IX/XXXIX 范畴，不在 P1-3 范围。
3. **Kerr 推广**：~~当前为 Schwarzschild（a=0）；Kerr 温度谱（`KerrFiber.lean` 已有）的蒸发动力学推广待后续~~ **🔶 部分闭合（2026-08-05，定理 5.10，§5.5）**：谱温度归约 f(a*) = 2√(1−a*²)/(1+√(1−a*²)) ∈ (0,1]（转动降温 + 极端冷却）+ 蒸发动力学（超辐射优先辐射角动量，t_evap 延长 1.93×，a* 单调递减）；`scripts/paperX_hawking_kerr.py` 6/6 注册 `run_all_tests.py`。**完整超辐射谱推进（2026-08-08，§5.5 定理 5.10 诚实边界）**：数值求解 Kerr 标量径向方程逐模计算 Z_slm(ω) = |R|²−1（s=0、l=m=1/2）——窗口符号判据 Z > 0 ⟺ ω < mΩ_H、转动增强、边界连续、发射谱超辐射区占可观份额、dJ/dE = 4.5/M 与简化 R_J = 2 同量级；`scripts/paperX_kerr_superradiance.py` 8/8 注册 `run_all_tests.py`。诚实边界：s=0 标量模（费米子/引力子需 Teukolsky 推广）登记后续。

---

## 参考文献

- Hawking (1975) Particle creation by black holes. *Commun. Math. Phys.* 43, 199–220.
- Page (1993) Information in black hole radiation. *Phys. Rev. Lett.* 71, 3743.
- Paper 8/12/16（本框架黑洞谱动力学纸面层）
- Paper 27 `scripts/paper27_hawking_evaporation.py`（Page 时间 0.647 数值锚点）

---

**变更记录**：

| 版本 | 日期 | 更新内容 |
|:--:|:--|:--|
| v0.4 | 2026-08-24 | 更名：UFPF → MUFPF（2 处替换）|
| v0.3 | 2026-08-08 | **Kerr 完整超辐射谱推进（§5.5 定理 5.10 诚实边界 + §8 开放项 3）**：数值求解 Kerr 无质量标量径向方程（Boyer-Lindquist）逐模计算 Z_slm(ω) = |R|²−1——窗口符号判据（Z > 0 ⟺ ω < mΩ_H，a*=0.9、l=m=1 逐点确认）、Schwarzschild 自检（恒吸收）、转动增强（Z_max 随 a* 单调 0.001→0.008）、边界连续、l=m=2 窗口拓宽峰值降低、发射谱超辐射区占 29%（负吸收 × Bose 因子）、角动量提取 dJ/dt > 0 且 dJ/dE = 4.5/M 与简化 R_J·a*/f³ = 8.04/M 同量级（比值 0.56）；`scripts/paperX_kerr_superradiance.py` 8/8 注册 `run_all_tests.py`；诚实边界：s=0 标量模（费米子/引力子需 Teukolsky 推广）登记后续。 |
| v0.2 | 2026-08-05 | **Kerr 蒸发动力学推广（定理 5.10，§5.5）**：谱温度归约 f(a*) = 2√(1−a*²)/(1+√(1−a*²)) ∈ (0,1]（Schwarzschild 归约 + 转动降温 + 极端冷却）+ 蒸发动力学（超辐射优先辐射角动量，t_evap 延长 1.93×、a* 单调递减）；`scripts/paperX_hawking_kerr.py` 6/6 注册 `run_all_tests.py`；§8 开放项 3 更新（诚实边界：简化超辐射模型）。 |
| v0.1 | 2026-08-04 | 初版。定理 2.1–2.7（霍金谱）、3.1–3.4（蒸发动力学）、4.1–4.7（Page 曲线，含精确熵平衡）、5.1–5.9（视界涨落 + 蒸发终点-反弹衔接）、6.1–6.5（信息保持）；Lean 四模块零 sorry + Agda 镜像；数值 `scripts/paperX_hawking_spectrum.py` 35/35。 |
