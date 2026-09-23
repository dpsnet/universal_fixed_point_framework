# Phase 70：超流相刚度与 T_c ∝ √ρ₀ 标度律的谱框架推导

**日期**：2026-09-11
**状态**：✅ 推导与形式化已完成，论文 Paper LVII 已达 v1.9（完整论文草稿）。v1.3 新增 §8.6b 跨尺度定量谱间隙谱系（δ_SC = Δλ_min/r*），全链 Δλ_min→δ_SC→ρ₀→T_c 在 `SuperfluidBridge.lean` 零 sorry 形式化；v1.4 新增 §8.6c 把守恒锚 1.764 内化为 πe^{−γ_E}（普适性定理 `BCSConstantOrigin.lean`）。v1.5 无量纲普适折叠并入 §8.6b（G2 收口）：`SuperfluidStiffness.lean` 新增 `universal_ratio_collapse_dimensionless`、`Tc_dimensionless_universal_ratio`、`dimensionless_ratio_at_fundamental_gap`，证明把 ρ₀ 链代入标度律后 E_F、k_B 全消去，T_c/Δ 恒等于无量纲普适常数 a_BCS，整条 ρ₀→√ρ₀→T_c 链折叠回凝聚态普适临界温度比。v1.6 新增 §8.6d 谱流 RG 多级常演化：把 §8.7#5 的单一自洽倍率 1/r* 分解为两级 EM 中间级链（Δλ_min→Δλ_min^EM→δ_SC），`SpectralFlowRG.lean` 12 定义/定理零 sorry（折叠 k₁k₂=r*、链一致 f₁f₂=1/r*），mpmath 50 位数值核验全过，代数因子分解层落地、动力学 RG 层诚实留待 §8.7#5。v1.7 新增 §8.6e 三级/多带谱系（`MultibandSpectralBridge.lean` 22 定义/定理零 sorry）。**v1.8 新增 §8.6f 谱流方程尺度动力学第一注入**：运行反常维度 ζ(r)∈(1,3/2)+非标度不变判据+EM 残差流闭合 f_EM(k₂)=c=f(r*)，`SpectralFlowDynamicsRG.lean` 15 定义/定理零 sorry，mpmath 60 位数值核验全过。**v1.9 新增 §8.6g 谱流 RG 流单参数族第二注入**：以闭合常数 $c$ 为参数唯一确定 $\rho(c)=f^{-1}(c)$，流不变折叠 `flow_telescoping`（$k_1k_2(c)=\rho(c)$）沿线保持、EM 锚 `flow_em_anchor_constant` 不随 $c$ 演化、β 通量 `rg_beta`∈(2/3,1) 及 β-形式 ODE 逆流解、运行指数沿流严格上升/β 严格递减，`SpectralFlowRGFlow.lean` 23 定义/定理零 sorry，mpmath 50 位数值核验 50/50 全过；推进 §8.7#5（开放项收窄为：EM 中间级由独立谱流方程涌现 + 独立能量锚选定 $c$ 截线落入材料 $\delta_{\text{SC}}$）。
**产出论文**：Paper LVII（编号紧随 Phase 66-69 系列的 Paper XLIX–LVI 之后）

---

## 1. 背景与动机

2026 年，Y. Tao 在 *Physica B* 742, 419333 发表"Universal square-root scaling between $T_c$ and superfluid phase stiffness: From cuprates to FeSe films"，从复数时间相对论（complex time relativity，基于 Tomita-Takesaki 定理与热时间假说）出发推导出 Božović 组 2016 年在 LSCO 薄膜中发现的根方标度律 $T_c = \gamma\sqrt{\rho_0}$，定量解释铜基（$\gamma \approx 3.7$ vs 实验 $4.2\pm0.5$ K^{1/2}）和铁基（$\gamma \approx 6.3$ vs 实验 $6.3$ K^{1/2}）超导。

本 Phase 的目标：**在 MUFPF 谱框架内内生推导超流相刚度 $\rho_0$ 的第一性原理定义，并由此导出 $T_c \propto \sqrt{\rho_0}$ 标度律，与 Tao 路径形成"殊途同归"的互补验证**。

研究笔记：`notes/02_superconductivity/spectral_superfluid_stiffness.md`（MUFPF-RN-RHO0-001, v1.0）

## 2. 核心推导链

### 2.1 起点：BCS 谱生成元（Paper XIV §2.1）

$$A_{\text{SC}} = \xi_k \sigma_z + \Delta \sigma_x, \quad \delta_{\text{SC}} = \min \sigma_+(A_{\text{SC}}) = \Delta$$

### 2.2 U(1) 相位扭曲与 Nambu 对易子

$$[\sigma_z, A_{\text{SC}}] = \Delta[\sigma_z, \sigma_x] = 2i\Delta\sigma_y$$
$$\|\partial_x A_{\text{SC}}\| = \Delta |\partial_x \phi|$$

**关键结构**：谱间隙 $\Delta$ 以线性形式控制谱生成元对相位扭曲的敏感度。

### 2.3 谱梯度能 → 谱刚度

$$f_{\text{grad}} = \frac{1}{2\beta_{\text{spec}}}\|\partial_x A_{\text{SC}}\|^2 = \frac{\Delta^2}{2\beta_{\text{spec}}}|\partial_x\phi|^2$$

与标准形式 $f_{\text{grad}} = \rho_0|\partial_x\phi|^2$ 对比：

$$\boxed{\rho_0 = \frac{\Delta^2}{2\beta_{\text{spec}}} = \frac{k_B \Delta^2}{2 E_F}}$$

其中 $\beta_{\text{spec}} = E_F/k_B$ 由谱流方程的不动点结构确定（Paper XIV §2.2）。

### 2.4 标度律导出

BCS 关系 $T_c = \Delta/(1.764\,k_B)$ 与 $\rho_0 \propto \Delta^2$ 联合：

$$\boxed{T_c = \gamma\sqrt{\rho_0}, \quad \gamma = \frac{\sqrt{2E_F/k_B}}{1.764}}$$

**平方根关系的本质**：$T_c \propto \Delta$（线性）× $\rho_0 \propto \Delta^2$（平方）→ $T_c \propto \sqrt{\rho_0}$。这一推导不依赖配对机制细节，是代数结构的内生推论。

## 3. 与 Tao (2026) 路径的比较

| 维度 | Tao 复时间路径 | MUFPF 谱框架路径 |
|:-----|:--------------|:----------------|
| 公理基础 | Tomita-Takesaki + 热时间假说 | Rec/Sp 范畴 + 谱流方程 |
| $\rho_0$ 的角色 | 序参量 VEV | $\Delta^2$ 与 $E_F$ 的代数组合 |
| $\gamma$ 来源 | 材料常数 $c_F = \nu_F/(2.14\sqrt{12}\gamma_F^d)$ | Fermi 能标 $E_F$ |
| 标度律成立范围 | $\gamma(2)^2 \approx 17$ K（铜基）| $E_F/(1.764^2 k_B)$ |
| 绝对零度图像 | 时空是类空的（度规退化） | 递归冻结（动力学静默） |
| 独有预言 | — | SU(2) Casimir 多带隙比量化 |

两条路径殊途同归，增强标度律可信度。可检验差异：$\gamma$ 与 $E_F$ 的标度关系、多带超导隙比、维度依赖。

## 4. 形式化状态

`SuperfluidStiffness.lean`（13 个定义/定理，零 sorry，构建通过 2026-09-17，含 v1.5 无量纲折叠新增）：

| 定义/定理 | 内容 | 状态 |
|:---------|:-----|:----:|
| `beta_spec` | $\beta_{\text{spec}} = E_F$（自然单位） | ✅ |
| `SpectralStiffness` | $\rho_0 = \Delta^2/(2\beta_{\text{spec}})$ | ✅ |
| `spectral_stiffness_gap_relation` | $\rho_0 = (1/(2E_F))\Delta^2$ | ✅ |
| `Tc_BCS` | $T_c = a_{\text{BCS}} \cdot \Delta$ | ✅ |
| `scaling_coefficient_gamma` | $\gamma = \sqrt{2E_F} \cdot a_{\text{BCS}}$ | ✅ |
| `Tc_sqrt_rho0_scaling` | $T_c = \gamma\sqrt{\rho_0}$ | ✅ |
| `dl_min_pos` | Cl(1,7) 基本谱间隙 $> 0$ | ✅ |
| `Tc_scaling_at_fundamental_gap` | 基本谱间隙处标度律成立 | ✅ |
| `universal_ratio_collapse_dimensionless` | **无量纲普适折叠**：$\gamma\sqrt{\rho_0}/\Delta = a_{\text{BCS}}$，$E_F$、$k_B$ 全消去 | ✅ |
| `Tc_dimensionless_universal_ratio` | $T_c/\Delta = a_{\text{BCS}} = 1/1.764$（经标度律链折叠 0 sorry） | ✅ |
| `dimensionless_ratio_at_fundamental_gap` | $T_c(dl_{\min})/dl_{\min} = a_{\text{BCS}}$ | ✅ |

`SuperfluidBridge.lean`（v1.3 新增，零 sorry，构建通过 2026-09-17；**v1.10 内部普适锁**）：

| 定义/定理 | 内容 | 状态 |
|:---------|:-----|:----:|
| `selfConsC` / `selfConsC_pos` | $c = a_{\text{BCS}}^3\cdot 4\pi > 0$ | ✅ |
| **`selfConsC_int` / `selfConsC_eq_int` / `selfConsC_int_pos`（v1.10）** | **内部普适锁** $c_0^{\text{int}}=(e^{γ_E}/π)^3\cdot4\pi$，$c_0=c_0^{\text{int}}$，正性（RN-ENDO-007） | ✅ |
| `r_star` / `r_star_spec` / `r_star_pos` / `r_star_closure` | 谱流自洽方程唯一正根 $r^*$（非自由参数） | ✅ |
| `deltaSC_categorical` / `deltaSC_explicit` / `gap_ratio_categorical` | **定量跨尺度桥**：$\delta_{\text{SC}} = \Delta\lambda_{\min}/r^*$ | ✅ |
| `stiffness_categorical` / `stiffness_gap_genealogy` / `Tc_scaling_from_categorical` | 全链折叠：$\rho_0 = (\Delta\lambda_{\min}/r^*)^2/(2E_F)$，$T_c = \gamma\sqrt{\rho_0}$ | ✅ |

跨尺度定量谱系（Paper LVII §8.6b）：Δλ_min → δ_SC = Δλ_min/r* → ρ₀ ∝ Δλ_min² → T_c = γ√ρ₀。范畴 Δ 内生贡献 Δλ_min 与 r* 的方程唯一性；物理输入保留 a_BCS、E_F（诚实边界 §8.6b）。

`BCSConstantOrigin.lean`（v1.4 新增，零 sorry）：`universal_ratio_cancellation` 证明临界比 Δ₀/T_c = πe^{−γ_E} = 1.764 与耦合 λ、截断 ω_D 无关；`universal_ratio_pos`。1.764 = πe^{−γ_E}（π=费米谱权重因子，e^{γ_E}=谱 ζ 正则化常数），普适性为定理（Paper LVII §8.6c，笔记 RN-ENDO-002）。

`SpectralFlowRG.lean`（v1.6 新增，零 sorry，编译通过 2026-09-17）：

| 定义/定理 | 内容 | 状态 |
|:---------|:-----|:----:|
| `dl_min_EM` / `dl_min_EM_pos` | 电磁中间级 $\Delta\lambda_{\min}^{(\text{EM})} = \Delta\lambda_{\min}/\sqrt{3}$（SU(2) Casimir 第一分量，非自由参数） | ✅ |
| `RG_k1` / `RG_k1_eq_sqrt3` | 第 1 级降级倍率 $k_1 = \Delta\lambda_{\min}/\Delta\lambda_{\min}^{(\text{EM})} = \sqrt{3}$（纯规范） | ✅ |
| `RG_k2` / `RG_k2_eq` | 第 2 级降级倍率 $k_2 = \Delta\lambda_{\min}^{(\text{EM})}/\delta_{\text{SC}} = r^*/\sqrt{3}$（BCS 动力学） | ✅ |
| `RG_telescoping` | **折叠不变式**：$k_1k_2 = r^*$（多级常演化 ≡ 单级自洽） | ✅ |
| `RG_f1` / `RG_f1_eq` | $f_1 = 1/\sqrt{3}$（规范增长因子） | ✅ |
| `RG_f2` / `RG_f2_eq` | $f_2 = \sqrt{3}/r^*$（动力学增长因子） | ✅ |
| `gap_ratio_telescoping` / `gap_ratio_multistage_eq_single` / `RG_chain_reproduces_single` | **链一致性**：$f_1f_2 = 1/r^* = \delta_{\text{SC}}/\Delta\lambda_{\min}$（两级路径 = 单级路径） | ✅ |

谱流 RG 多级常演化（Paper LVII §8.6d）：Δλ_min →¹⸍√³ Δλ_min^EM →^√³/r* δ_SC。代数因子分解层（两级倍率、折叠、链一致）已定理化；数值核验脚本 `verify_spectral_flow_RG_multistage.py`（mpmath 50 位，相对偏差 < 10⁻⁴⁵）全过。动力学 RG 层开放。

`MultibandSpectralBridge.lean`（v1.7 新增，零 sorry，编译通过 2026-09-17，3134 jobs）：

| 定义/定理 | 内容 | 状态 |
|:---------|:-----|:----:|
| `deltaSC_band1`/`deltaSC_band2`/`deltaSC_band3`（+`_pos`、`_closure`、`band1_rel_single`/`band3_rel_single`） | 三分支带隙 $\delta_{\text{SC}}^{(i)} = \Delta\lambda_i/r^*$（共享唯一根 | ✅ |
| `deltaSC_band2_eq_categorical` | 带2 即单级桥 $\delta_{\text{SC}} = \Delta\lambda_{\min}/r^*$（§8.6b） | ✅ |
| `band_ratio_1_over_2`/`band_ratio_3_over_2`/`band_ratio_3_over_1` | **多带隙比保持 Casimir 量化**：$1/\sqrt3:\;1:\sqrt2$（Paper XIV §6.1 定理化） | ✅ |
| `band_ratio_matches_casimir_12`/`_32` | 隙比 = Casimir 分量比（比例经 ÷r* 不变） | ✅ |
| `casimir_tower_2_over_1`/`casimir_tower_3_over_2`/`casimir_tower_3_over_1`/`casimir_tower_product_closure` | Casimir 升序三级塔：$k_{12}=\sqrt3$、$k_{23}=\sqrt2$、乘积 $\sqrt6$ | ✅ |

三级/多带谱系（Paper LVII §8.6e）：Δλ₁ --√3--> Δλ₂ --√2--> Δλ₃，三分支各经 ÷r* 化为带隙，隙比 = $\frac{1}{\sqrt3}:1:\sqrt2$。代数多带因子分解已定理化；数值核验 `verify_multiband_spectral.py`（mpmath 50 位，相对偏差 < 10⁻⁴⁵）全过。动力学逐级重解（§8.7#5）与带辨认对应（§8.7#8）开放。

`SpectralFlowDynamicsRG.lean`（v1.8 新增，零 sorry，编译通过 2026-09-17，3134 jobs）：

| 定义/定理 | 内容 | 状态 |
|:---------|:-----|:----:|
| `anom_dim` | 运行反常维度 $\zeta(r) = \dfrac{r f'(r)}{f(r)} = \dfrac{1 + \tfrac32\sqrt3\sqrt r}{1+\sqrt3\sqrt r}$ | ✅ |
| `anom_dim_gt_one` / `anom_dim_lt_threehalf` / `anom_dim_interior` | 落带 $1<\zeta(r)<\tfrac32$（$r>0$） | ✅ |
| `anom_dim_denom_pos` | 分母 $1+\sqrt3\sqrt r>0$ | ✅ |
| `em_residual_flow` | EM 残差流 $f_{\text{EM}}(u) = f(\sqrt3 u)=\sqrt3 u + 3\sqrt{\sqrt3}\,u\sqrt u$ | ✅ |
| `em_residual_flow_eq_selfCons` | $f_{\text{EM}}(u)=f(\sqrt3 u)$（解析等价） | ✅ |
| `RG_k2_pos` | $k_2>0$ | ✅ |
| `em_residual_closure` | **残差流闭合**：$f_{\text{EM}}(k_2)=f(r^*)=c=a_{\text{BCS}}^3\cdot4\pi$ | ✅ |
| `closed_constant_rg_invariant` | 闭常数 $c$ 在规范缩放下 RG 不变 | ✅ |
| `em_residual_root_unique` | $k_2$ 是 $f_{\text{EM}}(u)=c$ 的唯一正根 | ✅ |

谱流方程尺度动力学第一注入（Paper LVII §8.6f）：运行反常维度 $\zeta(r)\in(1,\tfrac32)$ 单调 1→3/2 诊断 $f$ **非标度不变**（无连续重整化流，"常演化只能是有限两级代数骨架"的定量判据）+ EM 残差流在 $k_2$ 处闭合到同一常数 $c$（$k_2$ 唯一正根）。数值核验 `verify_spectral_flow_dynamics_RG.py`（mpmath 60 位，15 项）全过。核心开放项（§8.7#5）：$k_2$ 由 EM 尺度自身**独立**谱流方程自洽涌现。

`SpectralFlowRGFlow.lean`（v1.9 新增，零 sorry，编译通过 2026-09-17，3135 jobs）：

| 定义/定理 | 内容 | 状态 |
|:---------|:-----|:----:|
| `r_star_flow` / `r_star_flow_spec` | 谱流 RG 流家族 $\rho(c)=f^{-1}(c)$：$0\le\rho(c)$ 且 $f(\rho(c))=c$ | ✅ |
| `r_star_flow_closure` / `flow_inverse_point` | 流闭合 $f\circ\rho=\mathrm{id}$、逆流 $\rho\circ f=\mathrm{id}$（水平簇即轨迹） | ✅ |
| `r_star_flow_pos` / `r_star_flow_at_physical` | $\rho(c)>0$；物理点锚定 $\rho(c_0)=r^*$ | ✅ |
| `r_star_flow_lt` | 流单调：$\rho(c_1)<\rho(c_2)$（$c_1<c_2$） | ✅ |
| `flow_k1_constant` / `flow_k2` / `flow_k2_lt` / `flow_k2_at_physical` | 动力学因子 $k_2(c)=\rho(c)/\sqrt3$，沿流单调，$k_2(c_0)=k_2$ | ✅ |
| `flow_telescoping` / `flow_em_anchor_constant` / `flow_anchor_orthogonal` | **流不变折叠** $k_1k_2(c)=\rho(c)$ 沿线保持；EM 锚不随 $c$ 演化；锚-动力学正交分解 | ✅ |
| `rg_beta` / `rg_beta_gt_two_thirds` / `rg_beta_lt_one` / `rg_beta_interior` | β 通量 $1/\zeta(r)\in(\tfrac23,1)$ | ✅ |
| `anom_dim_strictMono` / `flow_anom_dim_lt` / `flow_rg_beta_interior` / `flow_rg_beta_gt` | 运行指数沿流严格上升 $1\to\tfrac32$、β 沿流严格递减 $1\to\tfrac23$ | ✅ |

谱流 RG 流单参数族第二注入（Paper LVII §8.6g）：把 §8.6d 的单物理点折叠 $k_1k_2=r^*$ 推广为整条谱流族，流不变折叠沿线保持、EM 锚不随 $c$ 演化、β 通量∈(2/3,1) 且 β-形式 ODE $d\ln r/d\ln c=1/\zeta(r)$ 的积分解恰是流族自身（水平簇即轨迹）。数值核验 `verify_spectral_flow_RG_flow.py`（mpmath 50 位，50/50 全过，含 β-ODE 中心差分 $10^{-6}$）。核心开放项（§8.7#5）：EM 中间级由**独立**谱流方程涌现；用**独立能量锚选定 $c$ 截线**落入材料特定 $\delta_{\text{SC}}$。

## 5. Paper LVII 规划

**暂定标题**：《超流相刚度与 $T_c \propto \sqrt{\rho_0}$ 标度律的谱框架推导——兼与复时间相对论的互补比较》

**预计篇幅**：15–20 页

**优先级**：高（Tao 论文刚发表，对比评论时效窗口有限）

**论文结构**（初稿）：
1. 引言：Božović 实验发现与理论挑战
2. BCS 谱生成元与 Nambu 对易子结构（回顾 Paper XIV §2）
3. $\rho_0$ 的谱框架定义：$\rho_0 = k_B\Delta^2/(2E_F)$
4. $T_c \propto \sqrt{\rho_0}$ 的内生推导
5. 与 Tao (2026) 复时间路径的比较与互补性
6. 可检验预言：$\gamma$–$E_F$ 标度、多带隙比、维度依赖
7. 绝对零度：递归冻结 vs 类空时空
8. 形式化验证（Lean4 零 sorry）
9. 结论

**关联文档**：
- 研究笔记：`notes/02_superconductivity/spectral_superfluid_stiffness.md`
- 评论文章草稿：`notes/02_superconductivity/reply_tao_zhihu.md` / `.html`
- Lean 形式化：`formal_proof/MUFPFormalization/src/MUFPFormalization/SuperfluidStiffness.lean`、`SuperfluidBridge.lean`、`SpectralFlowRG.lean`
- 内生重建笔记：`notes/02_superconductivity/paper14_endogenous_rebuild_plan.md`（MUFPF-RN-ENDO-001）
- 谱常数来源：`notes/02_superconductivity/spectral_origin_of_bcs_constant.md`（RN-ENDO-002）、`notes/02_superconductivity/numeric_sources_pi_gamma.md`（RN-ENDO-003，π 与 e^{γ_E} 数值来源 + mpmath 60 位验证脚本 `verify_pi_gamma.py`）
- 多级常演化：`notes/02_superconductivity/spectral_flow_rg_multistage_evolution.md`（RN-ENDO-004，谱流 RG 多级常演化 + 诚实边界）
- 谱表述基础：Paper XIV（`paper/paper14_spectral_condensed_matter.md`）

## 6. 开放问题

1. $\gamma$ 的定量精度：当前 $E_F$ 取值为量级估计，需具体能带参数精确计算
2. 强耦合修正：$\Delta/E_F$ 不再是小量时标度律的偏离行为（Eliashberg 修正）
3. 维度依赖：2D 薄膜与 3D 块体的 $\gamma$ 是否满足 $\gamma \propto \sqrt{E_F}$ 而与维度无关
4. 与 `spectral_condensed_predictions.md` 中多带隙比预言的联合实验验证 —— **（2026-09-17 已给具体材料带辨认数值检验，RN-ENDO-006）**：预言隙比 $1/\sqrt3:1:\sqrt2$（相对比 $1:\sqrt3:\sqrt6$，极值 $\sqrt6\approx2.449$）对 MgB₂（σ=7.1, π=2.2–2.8 meV → 比 2.54–3.23）与 Ba₀.₆₈K₀.₃₂Fe₂As₂（11/3.5 meV → 3.14）的对比：MgB₂ 极值比跨落 $\sqrt6$ 附近（半定量一致，依赖 π 隙取值），Ba-122 高 $\sqrt6$ 约 +28% 未获清晰支持；且双带材料仅 2 隙、3 个 SU(2) 分量与物理带的一一对应**欠定**，需 ARPES 带分辨信息定案（§8.7#8 核心仍开放）。结论：**半定量一致而非证实**。
5. 跨尺度谱流 RG 常演化**动力学层**：§8.6b 已给出代数定量谱系，§8.6d（v1.6）又把单一谱间隙倍率 $r^*$ 分解为两级多级常演化（Δλ_min→Δλ_min^EM→δ_SC）并闭合**代数因子分解层**（`SpectralFlowRG.lean` 零 sorry）。§8.6f（v1.8）已给动力学层第一注入：运行反常维度 $\zeta(r)\in(1,\tfrac32)$ 且单调 1→3/2，诊断 $f$ 非标度不变（无连续重整化流），并证 EM 残差流闭合 $f_{\text{EM}}(k_2)=f(r^*)=c$、$k_2$ 唯一正根（`SpectralFlowDynamicsRG.lean` 零 sorry）。§8.6g（v1.9）已给动力学层第二注入：把折叠推广为整条谱流族 $\rho(c)=f^{-1}(c)$ 单参数族，流不变折叠沿线保持、EM 锚不随 $c$ 演化、β 通量∈(2/3,1) 及 β-形式 ODE 逆流解、运行指数沿流单调（`SpectralFlowRGFlow.lean` 零 sorry）。**（2026-09-17 补充，RN-ENDO-006）**『用独立能量锚选定 $c$ 截线』已给**具体材料数值落地**：以五个 BCS 材料实验比 $a_{\exp}=T_c/\Delta_0$（Pb 0.415、Al 0.576、Sn 0.542、Nb 0.519、Hg 0.438）为独立能量锚映射到谱流族 $c$ 截线（$r_{\text{mat}}=r^*a_{\exp}/a_{\text{BCS}}$，$c_{\text{mat}}=f(r_{\text{mat}})$），Al 近似普适（$c_{\text{mat}}/c_0=1.02$）、Pb/Hg 强耦合偏移 −33%/−29%，`material_csection_and_multiband.py`（mpmath 60 位）。**（2026-09-17 补充，RN-ENDO-004 v1.5）**动力学 RG **逐级重解**已给数值闭环：β-形式 ODE $d\ln r/d\ln c=\beta(r)=1/\zeta(r)\in(2/3,1)$ 沿 $[\ln0.2,\ln c_0]$ 实际逐步积分（Euler O(h)/RK4 O(h⁴)，20000 步映射误差 $1.4\times10^{-22}$，`dynamic_rg_stepwise_resolution.py`），在物理截线 $c=c_0$ 收敛回自洽根 $r^*$ 并完整复现流族——"流族是 β-ODE 的动态解、$r^*$ 在物理截线被**逐步重解（动态取得）**"就此验证；且 ζ/β 沿流诊断在五个材料截线逐材料成立（`anom_dim_strictMono` 复现，Al ζ=1.310>…>Pb ζ=1.290，β 随 $a_{\exp}$ 单调减小）。**仍开放**（Paper LVII §8.7#5 核心）的是让 $k_2$ 不由单一 $c$ 的反向重标度、而由 **EM 尺度自身的独立谱流方程**（带新的物理锚）自洽涌现——c 截线的"数值选取"是外部能量锚的映射，非内生涌现。**（2026-09-17 补充，RN-ENDO-007）**EM 独立谱流方程已按内部普适锁落地：把闭合常数锚由拟合 $a_{\text{BCS}}=1/1.764$ 切换为理论普适 $e^{γ_E}/π$（c=1 式内部锁定值，零测量），$c_0^{\text{int}}=(e^{γ_E}/π)^3\cdot4\pi$ 完全由 $\{\pi,e^{γ_E}\}$ 派生，EM 中间级 $k_2$ 由独立谱流方程 $f_{\text{EM}}(u)=c_0^{\text{int}}$ 精确唯一确定（$k_2=\rho(c_0^{\text{int}})/\sqrt3=0.50471$，自洽残差 $3\times10^{-61}$ EXACT，折叠 $\sqrt3 k_2=r^*$ 为派生恒等）。Lean 层 `a_BCS` 已切换、`selfConsC` 自动成为 $c_0^{\text{int}}$ 并新增 `selfConsC_int`/`selfConsC_eq_int`/`selfConsC_int_pos`；受影响的 0.016% 数值位移（$r^*$: 0.874037→0.874177 及 $\delta_{\text{SC}}$、$T_c$）待各下游文档逐项核对。**该方向最深形式仍开放**：一个**不共享** $c_0$、$g_{\text{EM}}\neq f(\sqrt3u)$、带**自身**闭合常数的真正独立 EM 动力学（此时折叠一般破缺，破缺量 $\Delta=1/\rho(c_{\text{EM}})-1/r^*$）。
6. 普适常数 π、e^{γ_E} 数值来源——已由 RN-ENDO-003 诚实分解：π ≡ 根本连通常数（多条独立精确表示唯一确定，BCS 中出现 = Matsubara 和 = 4arctan 1）；e^{γ_E} ≡ 定义性 + 谱定位（ζ 平凡极常数项），**无封闭形式、无理是否未决、数值不可约化**。因此"把 e^{γ_E} 数值从范畴结构算出"是**数学上不可行**的开放项，明确不伪称（Paper LVII §8.7#6、§8.6c）
