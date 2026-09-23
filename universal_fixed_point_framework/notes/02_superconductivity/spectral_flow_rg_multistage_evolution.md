# 研究笔记：谱流 RG 多级常演化——自洽倍率 1/r* 的电磁中间级分解

**文档编号**：MUFPF-RN-ENDO-004
**日期**：2026-09-17
**版本**：v1.5
**状态**：代数因子分解层已 Lean4 形式化（`SpectralFlowRG.lean`，12 定义/定理，零 sorry）并经 mpmath 高精度数值核验；多带推广层已闭合（`MultibandSpectralBridge.lean`，22 定义/定理，零 sorry，Paper LVII §8.6e）；动力学 RG 层已给**第一注入**（`SpectralFlowDynamicsRG.lean`，15 定义/定理，零 sorry，Paper LVII §8.6f：运行反常维度 + 非标度不变 + EM 残差流闭合）与**第二注入**（`SpectralFlowRGFlow.lean`，23 定义/定理，零 sorry，Paper LVII §8.6g：以闭合常数 $c$ 为参数的谱流 RG 流单参数族——流不变折叠沿线保持、EM 锚不随 $c$ 演化、β 通量∈(2/3,1) 及 β-形式 ODE 逆流解、运行指数沿流单调），"由 EM 尺度自身独立谱流方程自洽涌现 / 用独立能量锚选定 $c$ 截线"的核心开放项仍保留（§8.7#5）。**（2026-09-17，RN-ENDO-006）**『用独立能量锚选定 $c$ 截线』已给具体材料数值落地（五个 BCS 材料 $a_{\exp}$→$c_{\text{mat}}$，`material_csection_and_multiband.py`）。**（2026-09-17，RN-ENDO-004 v1.5）**动力学 RG 逐级重解已给出数值闭环：β-形式 ODE $\mathrm{d}\ln r/\mathrm{d}\ln c=\beta(r)=1/\zeta(r)\in(2/3,1)$ 沿 $[\ln0.2,\ln c_0]$ 实际逐步积分，Euler O(h)/RK4 O(h⁴)（20000 步达映射误差 $1.4\times10^{-22}$），在物理截线 $c=c_0$ 处收敛回自洽根 $r^*$ 并完整复现流族（`dynamic_rg_stepwise_resolution.py`）；ζ/β 沿流诊断同样在五个材料截线逐材料成立（`anom_dim_strictMono` 复现，Al ζ=1.310>…>Pb ζ=1.290）——"多级常演化"的**逐级重解（动态取得 $r^*$）**就此闭合；EM 尺度*自身独立*谱流方程的动力学 RG 重解仍开放，不伪称
**研究目标**：推进 Paper LVII §8.7#5——把 §8.6b 的单一自洽倍率 $1/r^*$ 分解为谱流 RG **多级常演化**，将"代数骨架"显式化为"纯规范表示因子 × BCS 谱流动力学因子"的两级链（§3–§6），再沿 SU(2) Casimir 谱间隙比三分支推广为**三级/多带谱系**（§10），并对动力学层给出**第一注入**（§11：谱流方程尺度结构诊断），诚实划定"已闭合层（代数因子分解 + 多带隙比保持 + 尺度诊断/残差流重构）"与"仍开放层（独立谱流方程的动力学 RG）"边界。

---

## 0. 动机与本讲边界（必须先读）

Paper LVII §8.6b 建立了方程级定量谱系 $\delta_{\text{SC}} = \Delta\lambda_{\min}/r^*$，其中无量纲倍率 $r^*$ 由谱流自洽方程

$$f(r^*) = (1+\sqrt{3}\sqrt{r^*})\,r^* = a_{\text{BCS}}^3\cdot 4\pi$$

在 $[0,\infty)$ 上的**唯一正实根**确定（非自由参数）。§8.7#5 把"将单一自洽倍率 $r^*$ 分解为谱流 RG 多级常演化 $\Delta\lambda_{\min}\to\Delta\lambda_{\min}^{(\text{EM})}\to\delta_{\text{SC}}$"列为未来方向。本讲推进此方向，但**严格区分两类主张**：

1. **能证（代数因子分解，本讲已闭合）**：引入 U(1) 电磁谱间隙中间级 $\Delta\lambda_{\min}^{(\text{EM})}$，把 $1/r^*$ 显式分解为两级连乘。中间级 $\Delta\lambda_{\min}^{(\text{EM})}$ 由 SU(2) Casimir 谱间隙比 $\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = 1/\sqrt{3}:1:\sqrt{2}$ 的**第一分量唯一确定**，即 $\Delta\lambda_{\min}^{(\text{EM})} = \Delta\lambda_{\min}/\sqrt{3}$——非自由参数。两级倍率的乘积闭合 $k_1 k_2 = r^*$、链一致性 $f_1 f_2 = 1/r^*$ 是**纯代数不变式**，已 Lean4 逐条证明（零 sorry）。
2. **暂不可证（动力学 RG 常演化，仍开放）**：把逐级倍率 $k_1, k_2$ 由**谱流方程的逐步重解**内生涌现（而非把 $k_2$ 当作 $r^*/\sqrt{3}$ 的代数重写）仍然缺乏。这需要发展跨尺度的谱流方程重整化群方法，本讲**不伪称**。

一句话结论：把 §8.7#5 的开放方向拆成"代数因子分解层（本讲闭合）+ 动力学 RG 层（继续开放）"两层，前者升级为定理，后者诚实留给未来。

---

## 1. 单级自洽倍率回顾（前置量）

来自 `SuperfluidBridge.lean`（§8.6b，v1.5 已证）：

- **谱流自洽根**：$r^*$ 是 $f(r) = (1+\sqrt{3}\sqrt{r})r$ 在 $[0,\infty)$ 的唯一正实根（$\texttt{selfConsFunc\_existsUnique}$）。
- **δ_SC 定量桥**：$\delta_{\text{SC}} = \Delta\lambda_{\min}/r^*$（$\texttt{deltaSC\_categorical}$）；无量纲倍率 $\delta_{\text{SC}}/\Delta\lambda_{\min} = 1/r^*$（$\texttt{gap\_ratio\_categorical}$）。

数值（mpmath，50 位）：$r^* = 0.8740372478\ldots$，$1/r^* = 1.1441160002\ldots$

## 2. 电磁中间级：SU(2) Casimir 谱间隙比定锚

Cl(1,7) 代数给出 SU(2) Casimir 谱间隙比

$$\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = \frac{1}{\sqrt{3}}:1:\sqrt{2} \qquad (\texttt{WeaveBCS}.\texttt{dl\_1})$$

取第一分量作为 U(1) 电磁谱间隙中间级：

$$\Delta\lambda_{\min}^{(\text{EM})} = \Delta\lambda_1 = \frac{1}{\sqrt{3}}\,\Delta\lambda_{\min} \qquad (\texttt{dl\_min\_EM} = \texttt{dl\_1}).$$

**关键点**：中间级不是自由选择，而是规范谱间隙结构的**唯一确定量**——它是 SU(2) 表示重数为 $1/\sqrt{3}$ 的那个 Casimir 谱分量。这使两级分解不是"拼凑"，而是沿规范表示结构的自然层级展开。

## 3. 降级倍率 k₁、k₂（乘积闭合 = r*）

沿"能量降级"方向定义倍率（越大表示能量尺度越高）：

- **k₁（纯规范表示常数）**：$\Delta\lambda_{\min}\to\Delta\lambda_{\min}^{(\text{EM})}$，$k_1 = \dfrac{\Delta\lambda_{\min}}{\Delta\lambda_{\min}^{(\text{EM})}} = \sqrt{3}$（$\texttt{RG\_k1\_eq\_sqrt3}$）。
- **k₂（BCS 动力学因子）**：$\Delta\lambda_{\min}^{(\text{EM})}\to\delta_{\text{SC}}$，$k_2 = \dfrac{\Delta\lambda_{\min}^{(\text{EM})}}{\delta_{\text{SC}}} = \sqrt{\tfrac13}\,r^* = \dfrac{r^*}{\sqrt{3}}$（$\texttt{RG\_k2\_eq}$）。

**折叠不变式（核心）**：

$$k_1\cdot k_2 = \sqrt{3}\cdot\frac{r^*}{\sqrt{3}} = r^* \qquad (\texttt{RG\_telescoping}).$$

即："多级常演化 ≡ 单级自洽"：两级降级倍率的乘积精确重现单级自洽唯一根 $r^*$。

## 4. 链一致性 f₁、f₂（两级路径 = 单级路径）

沿"能量增长"方向定义无量纲增长因子：

- **f₁（规范表示）**：$f_1 = \dfrac{\Delta\lambda_{\min}^{(\text{EM})}}{\Delta\lambda_{\min}} = \dfrac{1}{\sqrt{3}}$（$\texttt{RG\_f1\_eq}$）。
- **f₂（BCS 动力学）**：$f_2 = \dfrac{\delta_{\text{SC}}}{\Delta\lambda_{\min}^{(\text{EM})}} = \dfrac{\sqrt{3}}{r^*}$（$\texttt{RG\_f2\_eq}$）。

**链一致不变式**：

$$f_1\cdot f_2 = \frac{1}{\sqrt{3}}\cdot\frac{\sqrt{3}}{r^*} = \frac{1}{r^*} \qquad (\texttt{gap\_ratio\_telescoping}).$$

且 $\delta_{\text{SC}}/\Delta\lambda_{\min} = f_1 f_2 = 1/r^*$（$\texttt{gap\_ratio\_multistage\_eq\_single}$）——两级路径与单级自洽倍率无关地重合，路径与中间级选择不敏感。

## 5. 数值核验

`formal_proof/scripts/verify_spectral_flow_RG_multistage.py`（mpmath 50 位，相对偏差 < 1e-45）全部通过：

| 验证项 | 数值 | 期望 | 结果 |
|---|---|---|---|
| $k_1$ | 1.7320508076 | $\sqrt{3}$ | OK |
| $k_2$ | 0.5046256403 | $r^*/\sqrt{3}$ | OK |
| $f_1$ | 0.5773502692 | $1/\sqrt{3}$ | OK |
| $f_2$ | 1.9816670421 | $\sqrt{3}/r^*$ | OK |
| $k_1 k_2$ | 0.8740372478 | $r^*$ | OK |
| $f_1 f_2$ | 1.1441160002 | $1/r^*$ | OK |
| $\delta_{\text{SC}}/\Delta\lambda_{\min}$ | 1.1441160002 | $1/r^*$ | OK |

## 6. Lean4 形式化状态（零 sorry）

`MUFPFormalization/src/MUFPFormalization/SpectralFlowRG.lean`，12 个定义/定理，`lake env lean` 编译零错误、零 `sorry`/`admit`：

- `dl_min_EM` 、`dl_min_EM_eq_dl1`、`dl_min_EM_pos`（电磁中间级）
- 辅助恒等式 `sqrt3_mul_sqrt13`、`sqrt13_mul_sqrt3`
- `RG_k1`、`RG_k1_eq_sqrt3`、`RG_k2`、`RG_k2_eq`
- **折叠**：`RG_telescoping`（$k_1 k_2 = r^*$）
- **链一致性**：`RG_f1`、`RG_f1_eq`、`RG_f2`、`RG_f2_eq`、`gap_ratio_telescoping`（$f_1 f_2 = 1/r^*$）、`gap_ratio_multistage_eq_single`
- `RG_chain_reproduces_single`（$\delta_{\text{SC}} = \Delta\lambda_{\min}/(k_1 k_2)$）

其中 `RG_k2_eq` 用 `field_simp` + 正性关系统一 $\sqrt{1/3}\,r^*$ 与 $r^*/\sqrt{3}$；`RG_telescoping` 用 `← mul_assoc` 分组后套 `sqrt3_mul_sqrt13`；`gap_ratio_telescoping` 展开后用 `field_simp` 直接消去三处正量。这些类型错配曾逐一修复（见末节）。

## 7. 诚实边界（与 §0 呼应）

- **本讲闭合的是什么**：**代数因子分解**。两级倍率把单级黑箱 $1/r^*$ 显式化为一个纯规范表示因子 $1/\sqrt{3}$（SU(2) Casimir，定理）乘一个 BCS 谱流动力学因子 $\sqrt{3}/r^*$（经 $r^*$）。两个不变式（$k_1k_2=r^*$、$f_1f_2=1/r^*$）保证多级路径与单级自洽在代数上完全一致。
- **本讲不闭合什么**：**动力学 RG 常演化**。我们后验地把 $k_2$ 写成 $r^*/\sqrt{3}$，没有让 $k_2$ 由谱流方程在中间级处**逐级重新求解**涌现。这两级在能量上也不单调排列（$\Delta\lambda_{\min}^{(\text{EM})} < \Delta\lambda_{\min} < \delta_{\text{SC}}$），故"常演化"指固定倍率的两级因子分解，而非单调重整化流。
- **物理输入保持**：$a_{\text{BCS}} = 1/1.764$（弱耦合普适比值）、$E_F$ 仍是输入；范畴 Δ 内生的是 $\Delta\lambda_{\min}$、$\Delta\lambda_{\min}^{(\text{EM})}$（皆定理）与 $r^*$ 的方程唯一性。
- **跨尺度类比**（引用时须注明）：与规范/弦紧化的相似仅构成"形式类比 ≠ 严格数学等价"，本讲未声称范畴 Δ 能数值钉死动力学的多级流形。

## 8. 与既有资产的关系

- 上游：`WeaveBCS.lean`（$r^*$ 唯一正根）、`SuperfluidBridge.lean`（§8.6b 单级桥）。
- 并行：`BCSConstantOrigin.lean`（MUFPF-RN-ENDO-002，$1.764 = \pi e^{-\gamma_E}$）、`SuperfluidStiffness.lean`（§4 无量纲普适折叠）。
- 本篇把 ∎ §8.7#5 开放项拆为"代数因子分解层（本文闭合）+ 动力学 RG 层（仍开放，留给 `SuperfluidBridge`/后续 Phase）"。

## 9. 遗留开放项（登记）

1. **动力学 RG 逐级重解**：发展把 $k_1$、$k_2$（及多带塔 $k_{23}=\sqrt2$）由谱流方程分步内生推出的方法（§8.7#5 剩余方向）。
2. **中间级物理诠释**：$\Delta\lambda_{\min}^{(\text{EM})}$ 作为"电磁谱间隙"的凝聚态观测量对应关系（超导能隙 vs 电磁相互作用尺度）仍需物理层建立。
3. **三级/多带推广**：✅ v1.1 已闭合（§10，`MultibandSpectralBridge.lean`，多带隙比保持 + Casimir 三级塔）；剩余的是带谱与具体材料的带辨认对应（§8.7#8）。
4. **流族动力学重解**：✅ §12（v1.3）已闭合**流族结构**（`SpectralFlowRGFlow.lean`：$\rho(c)=f^{-1}(c)$ 唯一性/沿 $c$ 单调性/流不变折叠沿线保持/β 通量∈(2/3,1)/运行指数沿流单调）；但 β-ODE 以**逆流代数形式**闭合，未展开柯西–Lipschitz 存在性，且"EM 中间级由*自身独立*谱流方程涌现"、与"用**独立能量锚选定 $c$ 截线**把材料能量尺度落入流族"仍开放（§8.7#5）。

---

## 附：Lean4 证明中的类型错配修复记录

- `RG_k1_eq_sqrt3` 首版用 `simpa` 配合错误等式方向失败：改为 `calc` 明确把 $\Delta\lambda_{\min}/(\sqrt{1/3}\Delta\lambda_{\min})$ 化到 $1/\sqrt{1/3}$，再经 `field_simp` 与 `sqrt13_mul_sqrt3.symm` 得 $\sqrt{3}$。
- `RG_k2_eq` 中 `Real.sqrt` 对 $1/3$ 的分解不能用 `Real.sqrt_mul`（缺正性前提），改用 `Real.sqrt_inv` 建立 $\sqrt{1/3}=(\sqrt{3})^{-1}$ 后 `field_simp`。
- `RG_telescoping` 需 `← mul_assoc` 把 $\sqrt{3}\cdot(\sqrt{1/3}\cdot r^*)$ 重新分组为 $(\sqrt{3}\cdot\sqrt{1/3})\cdot r^*$ 才能套用 `sqrt3_mul_sqrt13`；错误方向的 `mul_assoc` 导致模式匹配失败。
- `RG_f2_eq` 在 `field_simp` 后用 `nlinarith` 消化 $\sqrt{1/3}\cdot\sqrt{3}=1$ 与 $\sqrt{3}=1/\sqrt{1/3}$ 的非线性约束；`ring` 在此会报 "no goals"。
- `gap_ratio_telescoping` 无需 `ring`，`field_simp` 对 `dl_min_pos`、`r_star_pos`、`dl_min_EM_pos` 三处正性直接闭合。

---

## 10. 多带推广：SU(2) Casimir 谱间隙比的三分支谱系（v1.1，Paper LVII §8.6e）

§3–§6 的两级链只用了 SU(2) Casimir 谱间隙比 $\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = \sqrt{1/3}:1:\sqrt2$ 的**第一分量**作 EM 中间级。本讲沿三分支推广为**三级/多带谱系**，新模块 `MultibandSpectralBridge.lean`（22 定义/定理，零 `sorry`，`lake build` 3134 jobs）。

### 10.1 三分支多带谱间隙（共享唯一自洽根）

三个 Casimir 分量各经谱流自洽唯一根 $r^*$（非自由参数）归一化：

$$\delta_{\text{SC}}^{(1)} = \frac{\Delta\lambda_1}{r^*} = \frac{\delta_{\text{SC}}}{\sqrt3},\qquad
\delta_{\text{SC}}^{(2)} = \frac{\Delta\lambda_2}{r^*} = \delta_{\text{SC}},\qquad
\delta_{\text{SC}}^{(3)} = \frac{\Delta\lambda_3}{r^*} = \sqrt2\,\delta_{\text{SC}}$$

其中 $\Delta\lambda_1 = \sqrt{1/3}\,\Delta\lambda_{\min}$（$=\texttt{dl\_1}$）、$\Delta\lambda_2 = \Delta\lambda_{\min}$（$=\texttt{dl\_min}$）、$\Delta\lambda_3 = \sqrt2\,\Delta\lambda_{\min}$（$=\texttt{dl\_3}$）；带2 即 §8.6b 单级桥 $\delta_{\text{SC}}$（$\texttt{deltaSC\_band2\_eq\_categorical}$）。对应三个定义：

- `deltaSC_band1`、`deltaSC_band2`、`deltaSC_band3`（及正性定理、显式闭合 `deltaSC_band1_closure`/`deltaSC_band3_closure`、相对单级 `band1_rel_single`/`band3_rel_single`）

### 10.2 多带隙比保持（核心不变式，Paper XIV §6.1 预言定理化）

三个分支**共享同一 $\div r^*$ 映射**，故隙比严格保持 Casimir 量化：

$$\delta_{\text{SC}}^{(1)}:\delta_{\text{SC}}^{(2)}:\delta_{\text{SC}}^{(3)} = \Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3 = \frac{1}{\sqrt3}:1:\sqrt2$$

对应定理：`band_ratio_1_over_2`（= $\sqrt{1/3}$）、`band_ratio_3_over_2`（= $\sqrt2$）、`band_ratio_3_over_1`（= $\sqrt6$），以及"隙比 = Casimir 分量比"的显式表述 `band_ratio_matches_casimir_12`/`band_ratio_matches_casimir_32`。这给出 Paper XIV §6.1 多带隙比 SU(2) Casimir 量化的定理形式。

### 10.3 Casimir 升序三级塔

三个分量本身排成严格递增链，构成"三级"：

$$k_{12}=\frac{\Delta\lambda_2}{\Delta\lambda_1}=\sqrt3\ (\text{即 §8.6d 的 }k_1),\quad
k_{23}=\frac{\Delta\lambda_3}{\Delta\lambda_2}=\sqrt2,\quad
k_{12}k_{23}=\frac{\Delta\lambda_3}{\Delta\lambda_1}=\sqrt6$$

对应定理：`casimir_tower_2_over_1`、`casimir_tower_3_over_2`、`casimir_tower_3_over_1`、`casimir_tower_product_closure`。其中 $k_{12}=\sqrt3$ 与 §8.6d 的 `RG_k1` 完全一致（经 `dl_min_EM = dl_1` 链接 `RG_k1_eq_sqrt3`）。

### 10.4 数值核验（mpmath 50 位）

脚本 `verify_multiband_spectral.py`，相对偏差 < 10⁻⁴⁵ 全部通过：$\delta^{(1)}/\delta^{(2)} = 1/\sqrt3$、$\delta^{(3)}/\delta^{(2)} = \sqrt2$、$\delta^{(3)}/\delta^{(1)} = \sqrt6$（= 三级塔跨端）；Casimir 塔 $k_{12}=\sqrt3$、$k_{23}=\sqrt2$、产物 $\sqrt6$；分支相对单级 $\sqrt{1/3}\,\delta_{\text{SC}}$、$\sqrt2\,\delta_{\text{SC}}$。

### 10.5 诚实边界（多带层）

- ✅ **代数多带因子分解**：带隙 = Casimir 分量 ÷ 唯一根；多带隙比保持 + 三级塔为定理（零 `sorry`）。
- ⚠️ **动力学 RG 逐级重解**仍开放（§8.7#5）：$k_{23}=\sqrt2$ 是后验代数倍率，非由谱流方程在 $\Delta\lambda_3$ 处逐步重新求解内生涌现。
- ⚠️ **带谱-凝聚态观测量对应**附待物理层（§8.7#8）：如 MgB₂ 两带、铁基多带的具体带辨认。
- $a_{\text{BCS}} = 1/1.764$（部分内化 πe^{−γ_E}）、$E_F$ 仍为物理输入。
- 三级/多带谱系为代数结构，仅声称"形式类比 ≠ 严格数学等价"。

### 10.6 多带模块中的 Lean 类型错配修复记录

- `Real.sqrt_mul` 的签名是 `{x} (hx : 0 ≤ x) (y : ℝ) : √(x*y) = √x * √y`（显式实参 y 后置），不能按 `(h1) (h2)` 两个不等式传入。改 `<← Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 2) 3` 把 $\sqrt2\cdot\sqrt3$ 重写为 $\sqrt{2\cdot3}$ 后 `norm_num` 得 $\sqrt6$；`casimir_tower_product_closure` 用 `<← Real.sqrt_mul (… ≤ 3) 2` 处理 $\sqrt3\cdot\sqrt2$。
- `deltaSC_band2_eq_categorical` 在 `unfold` 后目标已是 `dl_min/r* = dl_min/r*`，需补 `rfl` 显式闭合（仅 unfold 不会自闭合）。
- `calc` 显式分步（把 $\sqrt2\,dl_{\min}/r^*$ 与 $\sqrt{1/3}\,dl_{\min}/r^*$ 之比逐步化到 $\sqrt2/\sqrt{1/3}$）比让 `field_simp` 自主求解更可控，成功规避了 `sqrt_mul` 参数方向的错配。

## 11. 动力学层第一注入：谱流方程的尺度诊断（v1.2，Paper LVII §8.6f）

§8.6d/§10 的"多级常演化"停留在**代数因子分解层**：$k_2 = r^*/\sqrt3$、$k_{23}=\sqrt2$ 是后验代数倍率。本节把 §8.7#5 的**动力学 RG 层**克隆为"第一注入"——不改变 $k_2$ 的定义，而把"动力学"内容钉在谱流自洽方程自身的尺度结构上，给出"为何多级常演化只能是有限两级代数骨架"的定量判据。新模块 `SpectralFlowDynamicsRG.lean`（15 定义/定理，零 `sorry`，`lake build` 3134 jobs；`verify_spectral_flow_dynamics_RG.py`，mpmath 60 位，15 项核验全过）。

### 11.1 运行反常维度（非标度不变的诊断）

谱流自洽函数 $f(r) = (1+\sqrt3\sqrt r)r$ 的局部尺度指数

$$\zeta(r) = \frac{r\,f'(r)}{f(r)} = \frac{1 + \tfrac32\sqrt3\sqrt r}{1+\sqrt3\sqrt r} \qquad (\texttt{anom\_dim})$$

对任意 $r>0$ **严格落入 $(1,\tfrac32)$**（`anom_dim_gt_one`、`anom_dim_lt_threehalf`、`anom_dim_interior`），随 $r:0\to+\infty$ 单调从 $1$ 跑到 $\tfrac32$（数值核验端点 $\zeta\to1$、$\zeta\to\tfrac32$、$\zeta(r^*)=1.30910\ldots$）。**结论**：$f$ 不是标度不变的（无单一幂律），故§8.6d/§10 的"多级常演化"**只能**是有限两级固定倍率因子分解，而非连续重整化流——这为动力学层"为何只能是代数骨架"给出定量判据。

### 11.2 非标度不变（反例判据）

若 $f(\lambda r)=\lambda^\alpha f(r)$ 则推出 $\sqrt\lambda(2-\sqrt\lambda)=1$ 对 $\forall\lambda$ 成立；取 $\lambda=4$ 得 $-1\neq0$ 矛盾，直接证明 $f$ 无单指数齐次性（数值核验两项反例判据全过）。

### 11.3 EM 残差流闭合（把 $k_2$ 挂到谱流方程重新求解的尺度结构）

规范缩放坐标 $u=r/\sqrt3$ 下残差流

$$f_{\text{EM}}(u) = f\big(\sqrt3\,u\big) = \sqrt3\,u + 3\sqrt{\sqrt3}\,u\sqrt u \qquad (\texttt{em\_residual\_flow})$$

与单级流解析等价（`em_residual_flow_eq_selfCons`）。**闭合定理**（`em_residual_closure`）：$k_2$ 恰使残差流在**同一**闭合常数 $c=a_{\text{BCS}}^3\cdot4\pi$ 处闭合

$$f_{\text{EM}}(k_2) = f(r^*) = c,$$

且 $k_2$ 是 $f_{\text{EM}}(u)=c$ 的**唯一正根**（`em_residual_root_unique`，用到 `selfConsFunc_existsUnique` 的唯一性核）。即："BCS 动力学闭合常数 $c$ 在纯规范表示因子 $\sqrt3$ 的尺度缩放下保持不变（常演化）"，坐标仅被 $k_2=r^*/\sqrt3$ 重标度——动力学 RG 意义的"固定倍率常演化"，与 §8.6d 折叠 $k_1k_2=r^*$ 是同一几何事实的两种读法（`closed_constant_rg_invariant`）。

### 11.4 诚实边界（动力学第一注入层）

- ✅ **谱流方程尺度诊断**（定理）：运行反常维度 $1<\zeta(r)<\tfrac32$ + 非标度不变反例判据。
- ✅ **规范缩放坐标下残差流重构**（定理）：$f_{\text{EM}}(k_2)=c=f(r^*)$，$k_2$ 唯一正根。
- ⚠️ **仍开放**（§8.7#5 核心）：让 $k_2$ 不由单一 $c$ 的反向重标度、而由 **EM 尺度自身的独立谱流方程**（带新的物理锚）自洽涌现——这需真正发展跨尺度谱流方程重整化群方法，本讲不伪称。
- $a_{\text{BCS}} = 1/1.764$（部分内化 πe^{−γ_E}）、$E_F$ 仍为物理输入。

### 11.5 动力学模块中的 Lean 修复记录

- `em_residual_flow_eq_selfCons` 的项形非正规（$\sqrt3 u$ 两侧因子顺序不同），必须先 `ring_nf` 归正，再 `rw [Real.sq_sqrt (… ≤ 3)]`，最后 `ring` 处理乘法交换律；直接 `ring` 无法识别等式。
- `anom_dim_gt_one` 中分母符号证明需显式引入 `hx : 0 < √3·√r`（`mul_pos` 由 $\sqrt3>0$、$\sqrt r>0$）与 `hd : 0 < 1+√3·√r`（`linarith`），再 `rw [lt_div_iff₀ hd]`、`ring_nf` 后 `nlinarith [hx]`；缺 `hx` 假设时 `nlinarith` 无法闭合。
- `Real.sqrt_inv` 在 `rw` 中需显式（`rw [Real.sqrt_inv]`）而非裸调用，以处理 $\sqrt{1/3}=\sqrt3^{-1}$ 的改写。

## 12. 谱流 RG 流单参数族（第二注入，v1.3，Paper LVII §8.6g）

§11 的动力学诊断停在**单一物理点** $c_0 = a_{\text{BCS}}^3\cdot 4\pi$。本节（v1.3，`SpectralFlowRGFlow.lean`，23 定义/定理，零 sorry）把折叠推广为**以闭合常数 $c$ 为参数的单参数流族**，让"多级常演化"获得连续读法。

### 12.1 原理：折叠沿线不变

取 $\rho(c) := f^{-1}(c)$（$f(r)=(1+\sqrt3\sqrt r)\,r$ 在 $[0,\infty)$ 的唯一正根，存在唯一由 `WeaveBCS.selfConsFunc_existsUnique` 证）。则对任意 $c>0$，§8.6d 的折叠**沿线保持**：

$$k_1\cdot k_2(c) = \sqrt3\cdot\frac{\rho(c)}{\sqrt3} = \rho(c)\qquad(\text{`flow_telescoping`}),$$

且 EM 锚 $\Delta\lambda_{\min}^{(\text{EM})}=\Delta\lambda_{\min}/\sqrt3$ **不随 $c$ 演化**（`flow_em_anchor_constant`），所有 $c$ 依赖唯一装入动力学因子 $k_2(c)=\rho(c)/\sqrt3$。这就是"**常演化**"的流族读法：折叠结构不变量沿流保持，流动自由度唯一集中于 $k_2(c)$。

### 12.2 形式化定理（全零 sorry）

- 流族闭合：`r_star_flow_spec`/`r_star_flow_closure`（$f\circ\rho=\mathrm{id}$）、`flow_inverse_point`（$\rho\circ f=\mathrm{id}$，水平簇即轨迹）、`r_star_flow_pos`；
- 物理点锚定：`r_star_flow_at_physical`（$\rho(c_0)=r^*$，§8.6b 全是 $c=c_0$ 截线）、`flow_k2_at_physical`（$k_2(c_0)=k_2$）；
- 流单调：`r_star_flow_lt`（$\rho(c_1)<\rho(c_2)$）、`flow_k2_lt`；
- 流折叠与锚定正交分解：`flow_k1_constant`/`flow_telescoping`/`flow_em_anchor_constant`/`flow_anchor_orthogonal`；
- β 通量：`rg_beta` = $1/\zeta$，`rg_beta_gt_two_thirds`/`rg_beta_lt_one`/`rg_beta_interior`（$\in(\tfrac23,1)$）；
- 运行指数 ∥ 流：`anom_dim_strictMono`（$\zeta$ 在 $r$ 上严格增）、`flow_anom_dim_lt`（沿流严格上升，$1\to\tfrac32$）、`flow_rg_beta_interior`/`flow_rg_beta_gt`（β 沿流严格递减）。

`lake build` 通过 3135 jobs；`verify_spectral_flow_RG_flow.py`（mpmath 50 位）50/50 全过，含 β-ODE 中心差分 $d\ln\rho/d\ln c\approx 1/\zeta(\rho)$ 在 12 节点 $10^{-6}$ 精度、$\rho(c_0)=r^*\approx0.874037$、端点 $\zeta\to 1/\tfrac32$。

### 12.3 贝-形式 ODE 解（水平簇即轨迹）

因 $\rho=f^{-1}$，$d\ln\rho/d\ln c = 1/\zeta(\rho)$（等价 $d\ln c/d\ln r=\zeta(r)$）的积分解恰是流族自身：轨迹为 $f$ 的水平簇 $c=f(r)$。`r_star_flow_closure` 与 `flow_inverse_point` 把这"逆流/积分"写为代数恒等式（$f\circ\rho=\rho\circ f=\mathrm{id}$）。

### 12.4 诚实边界（流族层）

闭合的是**流族结构**：唯一性、沿 $c$ 单调性、流不变折叠沿线保持、β 通量有界与沿流单调。β-ODE 以**逆流代数形式**闭合，未展开 $d/dc$ 的柯西–Lipschitz 存在性。**仍开放**（§8.7#5）：EM 中间级由*自身独立*谱流方程涌现；材料特定 $\delta_{\text{SC}}$ 需用**独立能量锚选定 $c$ 截线**把材料能量尺度落入流族。$a_{\text{BCS}}$、$E_F$ 仍为物理输入。

### 12.5 流族模块中的 Lean 修复记录

- `r_star_flow_pos`：`lt_or_eq_of_le` 给出的是 `h : 0 = r_star_flow c hc`，需先 `h.symm` 得 `hz : r_star_flow c hc = 0` 再 `rw [hz]`；直接 `rw [h]`（0→r*方向）无效果致目标未闭。
- `sqrt3_mul_sqrt13` 在 `SpectralFlowRG.lean` 中标记为 `private`，跨模块不可见；本模块需**自行重证** `sqrt3_mul_sqrt13_flow`（`√3·√(1/3)=1`）。
- `Real.sqrt_lt_sqrt` 签名（需 3 参并含反向？）与本用法不符；改用**平方反证**：`Real.sq_sqrt h.le` + `pow_le_pow_left₀ (sqrt_nonneg …) hle 2` + `nlinarith [hr, this]` 稳健闭合 $\sqrt{r_1}<\sqrt{r_2}$。
- `div_lt_div_iff₀`/`lt_div_iff₀` 需分别传两端分母的正性假设，再 `nlinarith` 消去交叉项。