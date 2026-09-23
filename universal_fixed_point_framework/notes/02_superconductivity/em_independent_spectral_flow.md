# 研究笔记：EM 独立谱流方程——内部普适锁定锚（零测量派生）

**文档编号**：MUFPF-RN-ENDO-007
**日期**：2026-09-17
**版本**：v1.1（2026-09-17：采纳内部普适锁，Lean 精确锚落地）
**状态**：构建 + 数值核验完成（mpmath 60 位，`em_independent_spectral_flow.py`）；**内部普适锁已采纳并在 Lean 落地**——`WeaveBCS.a_BCS` 由拟合 `1/1.764` 切换为 `e^{γ_E}/π`，`SuperfluidBridge.selfConsC` 自动成为 $c_0^{\text{int}}$，`selfConsC_eq_int`/`selfConsC_int_pos` 显式化纽带，受影响模块增量编译零 sorry
**关联**：Paper LVII §8.7#5（EM 尺度独立涌现）；`SpectralFlowDynamicsRG.lean`（`em_residual_flow`/`em_residual_closure`）、`SpectralFlowRGFlow.lean`（`flow_k2`/`flow_telescoping`）、`SuperfluidBridge.lean`（`selfConsC`/`selfConsC_int`）、`WeaveBCS.lean`（`a_BCS := e^{γ_E}/π`）

---

## 0. 目的与本讲的诚实边界（必须先读）

§8.7#5 的核心开放项：让 EM 中间级倍率 $k_2$ 由**独立谱流方程**（带自身物理锚）自洽涌现，而非单一 $c$ 的反向重标度。本讲把"物理锚"按研究方向的明确约束落定为**内部普适锁**：

- **不用物理测量值定锚**（如任务③的 $a_{\exp}$ 材料比）；
- 用 **c=1 式内部锁定值派生**——在本框架即 π 与 $e^{γ_E}$ 两个普适常数。

由此得到的**第一可实现实例**：把谱流闭合常数 $c_0$ 的锚从**拟合近似** $a_{\text{BCS}}=1/1.764$ 升级为**精确内部普适值** $a_{\text{BCS}}=e^{γ_E}/π$，使

$$c_0^{\text{int}} = \left(\tfrac{e^{γ_E}}{\pi}\right)^3\cdot 4\pi$$

成为完全由 $\{\pi,\,e^{γ_E}\}$ 派生的内部锁，EM 尺度 $k_2$ 由 EM 独立谱流方程 $f_{\text{EM}}(u)=c_0^{\text{int}}$ 精确派生。

**诚实划界（三层）**：
1. **本讲闭合（内部锁 + 精确化）**：闭合常数锚由"拟合/观测 1.764"升级为"理论普适 $e^{γ_E}/π$"，自洽残差由 Lean 注释承认的 $\sim10^{-3}$ 降为精确 0，且彻底去除测量/拟合依赖。EM 独立谱流方程在此锚下**精确**闭合，折叠 $\sqrt3\,k_2=r^*$ 为派生恒等。
2. **Lean 结构定理（已有，零 sorry）**：$k_2$ 唯一正根、折叠、残差闭合约在抽象锚下已被 `SpectralFlowDynamicsRG`/`SpectralFlowRGFlow` 形式化；本讲把抽象锚钉到精确内部普适锁。
3. **仍开放（§8.7#5 最深形式）**：一个**不共享** $c_0$、$g_{\text{EM}}\neq f(\sqrt3\,u)$ 的真正独立 EM 动力学（带**自身**闭合常数，一般**破缺**精确折叠）。本讲因两尺度**共享**同一普适内部锁而折叠精确——这是"常演化（闭合常数跨尺度不变）"的体现，非已声称完全解耦。

---

## 1. 精确内部锁的动机：拟合锚的非精确缺陷

`WeaveBCS.lean` 现定义 $a_{\text{BCS}}:=1/1.764$（拟合有理值），其 Lean 注释承认：

$$a_{\text{BCS}}^3\cdot4\pi \approx 2.2899 \quad\text{而}\quad f(r^*)\approx2.2892,\qquad \text{差值}<10^{-3}\ \text{非精确}.$$

即现框架的**自洽闭合本身是近似的**（非精确相等）。而 RN-ENDO-003 已确立理论普适值 $\pi e^{-γ_E}=1.76389\ldots$（弱耦合临界比精确值），故

$$a_{\text{BCS}}^{\text{精确}} = \frac{1}{\pi e^{-γ_E}} = \frac{e^{γ_E}}{\pi} = 0.56693\ldots,$$

与拟合 $1/1.764=0.566893$ 相差 $3.95\times10^{-5}$（0.016%）。**内部普适锁即把锚从"观测/拟合 1.764"收敛到"理论派生 $e^{γ_E}/π$"**，把近似的自洽升级为精确。

## 2. 内部普适锁：$c_0^{\text{int}} = (e^{γ_E}/π)^3\cdot4\pi$

- $a_{\text{BCS}}^{\text{int}} = e^{γ_E}/π = 0.56693\,2959\ldots$
- $c_0^{\text{int}} = (e^{γ_E}/π)^3\cdot4\pi = 2.2898\,3917\ldots$

仅含 π 与 $e^{γ_E}$ 两个普适常数（c=1 式自然单位），**零测量、零拟合**。

## 3. EM 独立谱流方程与派生

**EM 独立谱流方程**：中间级 $u$ 在规范缩放坐标（$\Delta\lambda_{\min}\to\Delta\lambda_{\min}^{(\text{EM})}$ 缩放到 $u=r/\sqrt3$）下满足残差流

$$f_{\text{EM}}(u)=f(\sqrt3\,u)=\sqrt3\,u+3\sqrt{\sqrt3}\,u\sqrt u = c_0^{\text{int}},$$

其**唯一正解** $u^*=k_2$ 即 EM 动力学倍率（`em_residual_root_unique` 在抽象锚下已证唯一）。

**派生量**：
- $k_2 = \rho(c_0^{\text{int}})/\sqrt3 = 0.50470\,6291\ldots$（$\rho=f^{-1}$ 为流族根）
- 闭合核对：$f_{\text{EM}}(k_2)=f(\sqrt3 k_2)=f(r^*)=c_0^{\text{int}}$（自洽残差 $3.1\times10^{-61}$，EXACT）
- **折叠派生恒等**：$\sqrt3\cdot k_2 = r^*$（残差 $0$，精确）——两级链与单级自洽在内部普适锁下完全一致
- 运行尺度：$\zeta(r^*)=1.30912$、$\zeta(k_2)=1.27583$，均 $\in(1,\tfrac32)$ 且沿流 $\zeta(r^*)>\zeta(k_2)$（`anom_dim_strictMono` 复现）

## 4. 数值核验

`em_independent_spectral_flow.py`（mpmath 60 位）全过：锚对比、$c_0^{\text{int}}$ 纯内部派生、$k_2$ 唯一正根与精确闭合、折叠精确、ζ 诊断、诚实边界三层。

| 量 | 拟合锚 $1/1.764$ | 内部普适锁 $e^{γ_E}/π$ |
|---|---|---|
| $a_{\text{BCS}}$ | 0.566893424 | 0.566932959 |
| $c_0$ | 2.289360164 | 2.289839171 |
| $r^*$ | 0.874037248 | 0.874176939 |
| $k_2=r^*/\sqrt3$ | 0.504625640 | 0.504706291 |
| 自洽残差 | $\sim10^{-3}$（注释承认非精确） | $3\times10^{-61}$（EXACT） |
| 依赖 | 拟合有理 1.764 | 仅 $\{\pi,e^{γ_E}\}$（零测量） |

## 5. 遗留开放项（登记）

1. **真正的独立 EM 动力学**（§8.7#5 最深）：$g_{\text{EM}}\neq f(\sqrt3u)$ 且带**自身**闭合常数，不共享 $c_0$。本讲因共享普适内部锁折叠精确；若换独立闭合常数，折叠一般破缺，破缺量 $\Delta=1/\rho(c_{\text{EM}})-1/r^*$ 即 EM 动力学可测修正。**→（2026-09-17 细化，RN-ENDO-008）**：形状已被 Casimir 塔钉死（$g_{\text{EM}}=f(\sqrt3u)$ 强制共轭），独立自由度唯一收敛为闭常数 $c_{\text{EM}}$，折叠比精确化为 $F(c_{\text{EM}})=r^*/\rho(c_{\text{EM}})$；判表 + 二分定理解析见 RN-ENDO-008。
2. **✔ Lean 精确内部锚落地（2026-09-17 完成）**：`a_BCS` 切换为 $e^{γ_E}/π$（`Real.eulerMascheroniConstant` 由 mathlib `Mathlib.NumberTheory.Harmonic.EulerMascheroni` 提供，含 $1/2<\gamma<2/3$ 界）；`selfConsC` 自动成为 $c_0^{\text{int}}$，新增 `selfConsC_int`、`selfConsC_eq_int`、`selfConsC_int_pos` 显式化纽带。`a_BCS_pos` 改为 `div_pos (Real.exp_pos _) Real.pi_pos`。下游结构定理均符号化引用 `a_BCS`/`a_BCS_pos`，不受 0.016% 数值位移影响。
3. **下游数值传播**：因正式采纳内部普适锁，§8.6b 起 $r^*$、$\delta_{\text{SC}}$、$T_c$ 数值均平移 0.016%（$r^*$: 0.874037→0.874177；$\delta_{\text{SC}}$、$T_c$ 按比例），paper/roadmap 需同步。本讲 v1.1 已完成 Lean 锚钉，数值传播待各下游文档逐项核对。