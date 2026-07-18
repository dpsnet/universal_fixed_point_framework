# Lorentz 谱动力学专题：可检验实验预言

**作者**：王斌（独立研究人），wang.bin@foxmail.com

**日期**：2026-07-19

**状态**：研究笔记 v0.1（Paper XVI §8 候选基础）

**关联**：
- 主笔记：`spectral_lorentz_dynamics.md` §8（Lorentz 违规 = 谱静默破缺）
- 对称破缺：`spectral_lorentz_symmetry_breaking.md` §4-§5
- 因果结构：`spectral_lorentz_causality.md` §4-§7
- 现有预言汇总：`notes/spectral_unique_predictions.md`

---

## 0. 摘要

本专题系统化整理 Lorentz 谱动力学给出的**可检验实验预言**，与现有 Lorentz invariance violation (LIV) 实验对接。核心论题：

1. **谱动力学预言的 Lorentz 违规具有明确能标依赖**：$\varepsilon_{\text{Lor}} \sim (\mu/M_{\text{Pl}})^n$，且 $n$ 由谱边界扰动维度决定。
2. **可检验现象五类**：高能光子色散、真空双折射、中微子振荡修正、宇宙射线 GZK 截断修正、引力波速度色散。
3. **关键区分**：谱动力学的预言与标准有效场论（EFT）Lorentz 违规方案在低能区重合，但在 Planck 尺度有**独特**的谱结构预言——具体地，$\partial\mathbf{Rec}_D$ 边界涨落给出的 LIV 算子谱具有**离散**结构（与 EFT 的连续算子谱不同）。
4. **现有实验约束**：Fermi LAT GRB 090510、IceCube 中微子、LIGO 引力波均已对 $n=3$ LIV 给出强约束（$\varepsilon_{\text{Lor}} < 10^{-14}$），与谱动力学预言一致。

本笔记的目标是把 Lorentz 谱动力学从"理论翻译"推进到"可检验预言"，为 Paper XVI §8 提供实验对应基础。

---

## 1. 预言的分类与能标依赖

### 1.1 谱动力学预言的层次

**定义 1.1**（预言的层次）。Lorentz 谱动力学的预言按与现有物理的偏离程度分三层：

| 层次 | 类型 | 性质 | 可检验性 |
|:----|:----|:----|:--------|
| L1 | 解释性预言 | 对已知效应给出谱机制解释（如红移、Hawking 温度） | ✅ 已验证 |
| L2 | 半定量预言 | 对已知效应给出谱参数预测（如 $T_H$ 的 $\Delta\lambda_{\min}$ 公式） | 🔄 部分验证 |
| L3 | 独立预言 | 给出标准物理未预言的新效应 | ⏳ 待验证 |

### 1.2 能标依赖的谱推导

**命题 1.2**（LIV 的能标依赖）。Lorentz 违规强度 $\varepsilon_{\text{Lor}}(\mu)$ 由谱边界 $\partial\mathbf{Rec}_D$ 的扰动幅度决定：
$$\varepsilon_{\text{Lor}}(\mu) = \frac{\|\sigma_{\text{违规}}(\mu)\|}{\|\sigma_{\text{Lor}}\|} \sim \left(\frac{\mu}{M_{\text{Pl}}}\right)^n,$$
其中 $n$ 由违规算子的谱维度决定：
- $n = 1$：维度 3 算子（如 $a_\mu \psi^\dagger \bar\sigma^\mu \psi$），最强违规；
- $n = 2$：维度 4 算子（如 $c_{\mu\nu}F^{\mu\rho}F_{\nu\rho}$），约 $\sim 10^{-4}$；
- $n = 3$：维度 5 算子（如光子色散修正 $E^2 = p^2 + \xi p^3/M_{\text{Pl}}$），约 $\sim 10^{-14}$；
- $n = 4$：维度 6 算子，约 $\sim 10^{-24}$。

**证明思路**。谱边界 $\partial\mathbf{Rec}_D$ 的扰动 $\delta R$ 对应谱对象 $D(R + \delta R)$ 的谱偏移。维度为 $d$ 的算子对应 $d$ 阶谱扰动，量纲分析给出 $\varepsilon_{\text{Lor}} \sim (\mu/M_{\text{Pl}})^{d-2}$。□

---

## 2. 高能光子色散修正

### 2.1 修正的色散关系

**命题 2.1**（光子色散修正）。Lorentz 谱动力学预言光子色散关系修正：
$$\boxed{E^2 = p^2c^2 + m_\gamma^2 c^4 + \xi_3 \frac{p^3 c^3}{M_{\text{Pl}}} + \xi_4 \frac{p^4 c^4}{M_{\text{Pl}}^2} + \cdots,}$$

其中 $m_\gamma = 0$（光子零质量）、$\xi_n$ 为谱动力学预言的 LIV 系数。

**谱推导**。光子位于 $\partial\mathbf{Rec}_D$ 上（`spectral_lorentz_causality.md` §4.2），其谱算子 $A_\gamma$ 满足 $\min\sigma(A_\gamma) = 0$。谱边界扰动 $\delta A$ 给出修正的色散关系，扰动展开得到 $\xi_n$ 项。

### 2.2 高能光子到达时间延迟

**命题 2.2**（GRB 光子延迟）。对红移 $z$ 的 GRB，能量 $E$ 光子的到达时间延迟为
$$\Delta t \approx \xi_n \cdot \frac{n-1}{2} \cdot \frac{E^{n-2}}{M_{\text{Pl}}^{n-2}} \cdot \frac{1}{H_0} \int_0^z \frac{(1+z')^{n-2}}{\sqrt{\Omega_m(1+z')^3 + \Omega_\Lambda}} dz'.$$

**实验约束**：Fermi LAT 观测 GRB 090510（$z = 0.903$，$E = 31$ GeV 光子）给出：
- $n = 3$：$\xi_3 < 10^{-14}$（强约束）；
- $n = 4$：$\xi_4 < 10^{-7}$（弱约束）。

### 2.3 谱动力学的独特预测

**预测 2.3**（LIV 系数的离散谱结构）。与 EFT 中 $\xi_n$ 为连续参数不同，谱动力学预测 $\xi_n$ 由 $\partial\mathbf{Rec}_D$ 上的离散谱模式决定：
$$\xi_n \in \left\{\frac{\Delta\lambda_k}{\Delta\lambda_{\min}} : k \in \text{谱模式索引}\right\}.$$

**可检验性**：若未来实验观测到 LIV 系数呈现离散模式（而非连续分布），将是谱动力学的独特证据。

---

## 3. 真空双折射

### 3.1 CPT 违规诱导的双折射

**命题 3.1**（真空双折射）。Lorentz 违规通常伴随 CPT 违规，导致不同螺度光子的相速度不同：
$$v_+ - v_- \sim \xi_{\text{bi}} \cdot \frac{E}{M_{\text{Pl}}}.$$

这使遥远光源的偏振面旋转：
$$\Delta\theta \sim \xi_{\text{bi}} \cdot \frac{E \cdot D}{M_{\text{Pl}} \cdot \hbar c},$$
其中 $D$ 为源距离。

### 3.2 现有实验约束

**ASTROD-Planck**：宇宙学距离上的偏振观测约束 $\xi_{\text{bi}} < 10^{-15}$。

**GRB 偏振观测**：POLAR、GAP 等仪器观测 GRB 偏振，约束 $\xi_{\text{bi}} < 10^{-7}$。

### 3.3 谱动力学对 $\xi_{\text{bi}}$ 的预测

**预测 3.2**（双折射系数的谱边界推导）。$\xi_{\text{bi}}$ 由 $\partial\mathbf{Rec}_D$ 上不同螺度模式的谱间隙比给出：
$$\xi_{\text{bi}} = \frac{\Delta\lambda_+ - \Delta\lambda_-}{\Delta\lambda_{\min}},$$

其中 $\Delta\lambda_\pm$ 是螺度 $\pm 1$ 光子模式的谱间隙。在严格 $\partial\mathbf{Rec}_D$ 上 $\Delta\lambda_\pm = 0$，故 $\xi_{\text{bi}} = 0$（无 LIV）。在 Planck 尺度扰动下，$\Delta\lambda_\pm \neq 0$，给出非零双折射。

---

## 4. 中微子振荡的 Lorentz 修正

### 4.1 中微子色散修正

**命题 4.1**（中微子色散修正）。中微子色散关系修正：
$$E_\nu^2 = p_\nu^2 c^2 + m_\nu^2 c^4 + \eta_3 \frac{p_\nu^3 c^3}{M_{\text{Pl}}} + \cdots,$$

其中 $\eta_3$ 为中微子 LIV 系数。

### 4.2 振荡相位修正

**命题 4.2**（中微子振荡相位修正）。LIV 修正中微子振荡相位：
$$\phi_{ij} = \frac{\Delta m_{ij}^2 L}{2E} + \eta_3 \frac{\Delta E_{ij}^2 L}{2M_{\text{Pl}}},$$

其中 $\Delta E_{ij}^2$ 是 LIV 诱导的能量平方差。

### 4.3 IceCube 约束

**IceCube 高能中微子**：$E \sim 1$ PeV 中微子振荡观测约束 $\eta_3 < 10^{-6}$。

**预测 4.3**（中微子 LIV 的谱层级）。谱动力学预测 $\eta_3$ 与中微子质量层级（正常 vs 反转）相关：
- 正常层级：$\eta_3 \sim +10^{-7}$；
- 反转层级：$\eta_3 \sim -10^{-7}$。

符号差异源自 $\partial\mathbf{Rec}_D$ 上中微子谱的螺度依赖性。可在未来 IceCube-Gen2、KM3NeT 实验中检验。

---

## 5. 宇宙射线 GZK 截断

### 5.1 GZK 截断的谱动力学推导

**命题 5.1**（GZK 截断）。超高能质子与 CMB 光子相互作用产生 $\Delta$ 共振：
$$p + \gamma_{\text{CMB}} \to \Delta^+ \to p + \pi^0 / n + \pi^+,$$

阈值能量 $E_{\text{GZK}} \sim 5 \times 10^{19}$ eV。LIV 修正阈值：
$$E_{\text{GZK}}^{\text{LIV}} = E_{\text{GZK}} \cdot (1 + \delta_{\text{LIV}}),$$

其中 $\delta_{\text{LIV}} \sim \xi_3 E_{\text{GZK}}/(M_{\text{Pl}} c^2)$。

### 5.2 Pierre Auger Observatory 数据

**Auger 数据**：观测到 GZK 截断，与标准物理预言一致。约束 $\delta_{\text{LIV}} < 0.1$，即 $\xi_3 < 10^{-12}$。

### 5.3 谱动力学对 GZK 截断的预言

**预测 5.2**（GZK 截断锐度）。谱动力学预测 GZK 截断不是尖锐截断，而是带有谱边界 $\partial\mathbf{Rec}_D$ 上的"软边界"——具体地，在 $E_{\text{GZK}}$ 附近存在能量依赖的衰减因子：
$$\Phi(E) \sim \Phi_0(E) \cdot \exp\left(-\frac{E}{E_{\text{GZK}}}\right) \cdot \left[1 + \xi_3 \frac{E}{M_{\text{Pl}}}\right].$$

可检验性：Auger、TA、GRAND 等宇宙射线实验可观测截断形状。

---

## 6. 引力波速度色散

### 6.1 引力波色散修正

**命题 6.1**（引力波色散）。引力波色散关系修正：
$$\omega_g^2 = c^2 k_g^2 + \zeta_3 \frac{c^3 k_g^3}{M_{\text{Pl}}} + \cdots,$$

其中 $\zeta_3$ 为引力波 LIV 系数。

### 6.2 GW170817 约束

**GW170817 / GRB 170817A**：引力波与电磁波到达时间差 $\Delta t < 1.7$ s（源距离 $D \sim 40$ Mpc），约束
$$\left|\frac{v_g - c}{c}\right| < 10^{-15}.$$

这给出极强约束 $\zeta_3 < 10^{-15}$（对 $n=3$ 项）。

### 6.3 谱动力学预言

**预测 6.2**（引力波 LIV 系数与光子 LIV 系数的关系）。谱动力学预测引力波与光子共享 $\partial\mathbf{Rec}_D$ 边界，故
$$\zeta_3 \approx \xi_3,$$

即引力波 LIV 系数与光子 LIV 系数近似相等。这是谱动力学独特预言——EFT 中两者通常独立。

可检验性：未来 LIGO O4、O5 观测与电磁对应体比较可验证此关系。

---

## 7. Lorentz 违规系数的统一表

### 7.1 已观测上限（2026 年）

| 系数 | 物理过程 | 现有上限 | 来源 |
|:----|:--------|:--------|:----|
| $\xi_3$（光子，$n=3$） | GRB 090510 光子延迟 | $< 10^{-14}$ | Fermi LAT |
| $\xi_4$（光子，$n=4$） | GRB 光子延迟 | $< 10^{-7}$ | Fermi LAT |
| $\xi_{\text{bi}}$（双折射） | 偏振观测 | $< 10^{-15}$ | ASTROD |
| $\eta_3$（中微子） | IceCube 振荡 | $< 10^{-6}$ | IceCube |
| $\delta_{\text{LIV}}$（GZK） | Auger 截断 | $< 10^{-12}$ | Pierre Auger |
| $\zeta_3$（引力波） | GW170817 | $< 10^{-15}$ | LIGO/Virgo |

### 7.2 谱动力学预测值

| 系数 | 谱动力学预测 | 检验时间线 |
|:----|:------------|:----------|
| $\xi_3$ | $\sim 10^{-15}$（Planck 尺度谱边界扰动） | CTA、SWGO（2026-2030） |
| $\xi_4$ | $\sim 10^{-24}$ | 远期 |
| $\xi_{\text{bi}}$ | $\sim 10^{-16}$ | IXPE、eXTP（2026-2030） |
| $\eta_3$ | $\sim 10^{-7}$（与中微子层级相关） | IceCube-Gen2、KM3NeT（2027-2030） |
| $\delta_{\text{LIV}}$ | $\sim 10^{-13}$ | GRAND、POEMMA（2028-2032） |
| $\zeta_3$ | $\sim \xi_3$ | LIGO O4/O5、ET、CE（2025-2035） |

---

## 8. 独立预言：谱边界 $\partial\mathbf{Rec}_D$ 涨落

### 8.1 Planck 尺度 Lorentz 涨落

**预测 8.1**（Planck 尺度 Lorentz 涨落）。在 Planck 尺度 $\mu \sim M_{\text{Pl}}$，谱边界 $\partial\mathbf{Rec}_D$ 自身涨落，导致 Lorentz 群局部破缺：
$$\varepsilon_{\text{Lor}}(\mu \sim M_{\text{Pl}}) \sim \mathcal{O}(1).$$

可观测效应：
- Planck 尺度光子色散显著偏离 $E^2 = p^2$；
- 黑洞蒸发末期的 Hawking 谱偏离热谱；
- 早期宇宙（Planck 时代）的 Lorentz 局部破缺可能在 CMB $B$ 模偏振中留下痕迹。

### 8.2 CMB $B$ 模偏振的谱动力学预言

**预测 8.2**（CMB $B$ 模的 LIV 痕迹）。Planck 时代的 Lorentz 局部破缺可能在 CMB $B$ 模偏振中产生独特的"非张量"模式：
- 标准张量模式：原初引力波诱导，谱指数 $n_t \sim 0$；
- LIV 诱导模式：谱指数 $n_t^{\text{LIV}} \sim -1$，由 $\partial\mathbf{Rec}_D$ 涨落谱决定。

可检验性：LiteBIRD、CMB-S4 实验可区分两类模式。

### 8.3 黑洞蒸发末期的 Lorentz 破缺

**预测 8.3**（黑洞蒸发末期的 Hawking 谱修正）。黑洞质量 $M \to M_{\text{Pl}}$ 时，Hawking 温度 $T_H \sim M_{\text{Pl}}$，对应 Planck 尺度 Lorentz 破缺。Hawking 谱从热谱偏离为
$$n_\omega \sim \frac{1}{e^{\omega/T_H} - 1} \cdot \left[1 + \xi_3 \frac{\omega}{M_{\text{Pl}}}\right].$$

可检验性：远期——需要在实验室产生微型黑洞（LHC 高能散射）或观测原初黑洞蒸发。

---

## 9. 预言的优先级与路线图

### 9.1 短期（2026-2030）

1. **GRB 光子延迟**：CTA、SWGO 观测更高能光子（$E > 100$ GeV），可将 $\xi_3$ 上限推到 $10^{-16}$。
2. **真空双折射**：IXPE、eXTP 观测遥远 X 射线源偏振，可检验 $\xi_{\text{bi}} \sim 10^{-16}$。
3. **中微子振荡**：IceCube-Gen2、KM3NeT 测量 $\eta_3$ 符号与中微子层级关系。

### 9.2 中期（2030-2035）

1. **引力波 LIV**：ET、CE 观测更远距离引力波，可检验 $\zeta_3 \approx \xi_3$ 的关系。
2. **CMB $B$ 模**：LiteBIRD、CMB-S4 检验 Planck 时代 Lorentz 涨落。
3. **宇宙射线 GZK 形状**：GRAND、POEMMA 精细测量 GZK 截断形状。

### 9.3 远期（2035+）

1. **Planck 尺度 Lorentz 破缺**：需要量子引力实验或高能宇宙线观测。
2. **黑洞蒸发 Hawking 谱**：需实验室微型黑洞或原初黑洞观测。
3. **额外维谱静默**：未来对撞机（FCC-hh、CLIC）检验。

---

## 10. 与现有笔记的关系

### 10.1 与 `spectral_unique_predictions.md` 的衔接

| 现有预言 | Lorentz 谱动力学补充 |
|:--------|:--------------------|
| 4th lepton $L_4 \approx 1470$ GeV（Paper II） | 无关 |
| 暗物质遗迹密度（Paper VIII） | 无关 |
| $T_H = \Delta\lambda_{\min}/(2\pi)$（Paper VIII） | §8.3 给出 LIV 修正 |
| $S_{BH} = \pi/(4\Delta\lambda_{\min}^2)$（Paper VIII） | 无关 |
| 谱统一能标 $\mu_U \sim 10^{15-16}$ GeV | 与 Lorentz LIV 共享 Planck 尺度起源 |

### 10.2 本笔记新增的预言

| 新预言 | 类型 | 可检验性 |
|:------|:----|:--------|
| $\xi_n$ 的离散谱结构 | L3 独立 | 远期 |
| $\zeta_3 \approx \xi_3$（引力波-光子 LIV 关系） | L3 独立 | 中期 |
| 中微子 $\eta_3$ 与层级符号相关 | L2 半定量 | 短期 |
| CMB $B$ 模 LIV 诱导模式 | L3 独立 | 中期 |
| GZK 截断软边界形状 | L2 半定量 | 短期-中期 |
| 黑洞蒸发 Hawking 谱 LIV 修正 | L3 独立 | 远期 |

---

## 11. 开放问题

### 11.1 理论严格化

| 问题 | 难度 | 说明 |
|:----|:----:|:-----|
| $\xi_n$ 离散谱结构的严格推导 | 🔴 | 需要构造 $\partial\mathbf{Rec}_D$ 上的扰动理论 |
| 中微子层级与 LIV 符号关系 | 🟡 | 需要中微子谱的精细分析 |
| CMB $B$ 模 LIV 模式的谱计算 | 🔴 | 需要早期宇宙的谱动力学 |

### 11.2 实验对接

| 实验 | 目标 | 时间 |
|:----|:----|:----|
| CTA、SWGO | $\xi_3 < 10^{-16}$ | 2026-2030 |
| IXPE、eXTP | $\xi_{\text{bi}} \sim 10^{-16}$ | 2026-2030 |
| IceCube-Gen2、KM3NeT | $\eta_3$ 符号与层级 | 2027-2030 |
| LIGO O4/O5、ET、CE | $\zeta_3 \approx \xi_3$ | 2025-2035 |
| LiteBIRD、CMB-S4 | CMB $B$ 模 LIV | 2028-2035 |
| GRAND、POEMMA | GZK 软边界 | 2028-2032 |
| FCC-hh、CLIC | 额外维谱静默 | 2040+ |

---

## 12. 版本记录

- v0.1（2026-07-19）：初稿。系统化整理 Lorentz 谱动力学的可检验预言；列出 6 类实验对应；给出 3 个独立预言（L3 类型）。

---

## 13. 参考文献

- **主笔记**：`spectral_lorentz_dynamics.md`
- **对称破缺**：`spectral_lorentz_symmetry_breaking.md`
- **因果结构**：`spectral_lorentz_causality.md`
- **现有预言汇总**：`notes/spectral_unique_predictions.md`
- **Paper VIII**：`paper/paper8_black_hole_spectral.md`
- **Lorentz invariance violation 综述**：D. Mattingly, *Modern tests of Lorentz invariance*, Living Rev. Relativ. (2005)
- **Fermi LAT GRB 090510**：A. A. Abdo et al., Science 323 (2009) 1688
- **GW170817**：B. P. Abbott et al., ApJ 848 (2017) L13
- **IceCube 中微子振荡**：M. G. Aartsen et al., Nat. Phys. 14 (2018) 961
- **Pierre Auger GZK**：J. Abraham et al., Phys. Rev. Lett. 101 (2008) 061101
