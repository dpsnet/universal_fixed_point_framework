# 研究笔记：EM 独立动力学结构论（Route A）——闭常数判表与二分定理解析

**文档编号**：MUFPF-RN-ENDO-008
**日期**：2026-09-17
**版本**：v1.0
**状态**：结构解析 + 数值判表完成（mpmath 60 位，`em_abelian_structural_criterion.py`）；二分定理第 1 次收敛【⟸ 方向】由判表自检验证，⟹ 方向待 Lean 形式化
**关联**：RN-ENDO-007 §5.1（最深开放项）；§8.7#5；`SpectralFlowRG.lean`（`dl_min_EM`，塔钉死定理）；`SpectralFlowDynamicsRG.lean`（`em_residual_flow`）；`SuperfluidBridge.lean`（`selfConsC_int`）；`BCSConstantOrigin.lean`（`a0=2e^{γ_E}/π`）

---

## 0. 目的与本讲的收敛点（必须先读）

RN-ENDO-007 把 §8.7#5 的最深开放项表述为：让 EM 中间级倍率由一个**不共享** $c_0$、流形状 $g_{\text{EM}}\neq f(\sqrt3\,u)$、带**自身**闭合常数的真正独立 EM 动力学自洽涌现。经评估选定 **路线 A · 阿贝尔扇区结构论**。本讲把路线 A 落到一个**可判定**的结构判表上，并**修正**了初版的形如 $g_{\text{EM}}(u)=(1+\beta\sqrt{u})u$ 的参数化错误。

**关键收敛（本讲核心）**：EM 中间级 $\Delta\lambda_{\min}^{(\text{EM})}=\Delta\lambda_{\min}/\sqrt3$ 已被 `SpectralFlowRG.dl_min_EM` 作为定理**钉死**（SU(2) Casimir 塔第一分量），因此 EM 阶段流 $f_{\text{EM}}(u)=f(\sqrt3\,u)=\sqrt3\,u(1+3^{3/4}\sqrt u)$ 的**形状不是自由参数——它被格局强制为规范的共轭**。于是路线 A 声称的"独立内容"**唯一可挂靠的自由度是 EM 阶段自身的闭合常数 $c_{\text{EM}}$**。这是本讲较 RN-ENDO-007 的重要推进：不是"形状 + 锚"双自由度，而是**形状钉死、锚唯一自由**。

由此折叠比化为 $c_{\text{EM}}$ 的纯函数：
$$F(c_{\text{EM}})=\frac{\delta'_{\text{SC}}}{\delta_{\text{SC}}}=\frac{r^*}{\sqrt3\,\bar u}=\frac{r^*}{\rho(c_{\text{EM}})},\qquad \bar u=\rho(c_{\text{EM}})/\sqrt3,\qquad \rho=f^{-1}.$$

**二分定理解析（待形式化）**：
$$F(c_{\text{EM}})=1 \iff c_{\text{EM}}=c_0.$$
- ⟸ **判表自检已验**（$F(c_0)=1$，差 $0.00$，$\bar u=\rho(c_0)/\sqrt3=r^*/{\sqrt3}$ 精确复现折叠）。
- ⟹ **待 Lean**：给内部普适锚集合 $c_{\text{EM}}\in\{c_0,c_{0D},c_0/8,\dots\}$，证 $F\neq1$ 当 $c_{\text{EM}}\neq c_0$（由 $f,\rho$ 严格单调性）。

**三种收敛**：
1. 若 ⟹ 证成立，则**唯一自洽的内部普适锁就是共享 $c_0$**，EM 独立动力学被**证明不存在**（动力学平庸、折叠必然）；§8.7#5 以"否定"收口——这是完全合法的裁决。
2. 若构出某个内部普适 $c_{\text{EM}}\neq c_0$ 且物理上必须采用，则给出**可测的 $F\neq1$** 与 $T_c$ 修正，EM 独立实存。
3. 两者都不伪称：判表只报"每个候选锁 ⟹ 每个 $F$"的证据，由框架选题而非拟合选题。

---

## 1. 为什么形状被钉死：塔钉死定理

谱流 RG 两级分解（RN-ENDO-004 / `SpectralFlowRG.lean`）：
$$\Delta\lambda_{\min}\xrightarrow{k_1=\sqrt3}\Delta\lambda_{\min}^{(\text{EM})}\xrightarrow{k_2}\delta_{\text{SC}},\qquad \Delta\lambda_{\min}^{(\text{EM})}=\frac{\Delta\lambda_{\min}}{\sqrt3}=dl_1.$$

$dl_1=\sqrt{1/3}\,dl_{\min}$（`WeaveBCS.dl_1`）与 $\Delta\lambda_{\min}^{(\text{EM})}=\Delta\lambda_{\min}/\sqrt3$（`SpectralFlowRG.dl_min_EM`）均为 Casimir 塔的**定理**（$|\Delta\lambda_1:\Delta\lambda_2:\Delta\lambda_3=1/\sqrt3:1:\sqrt2$）。因此 EM 中间级**不能由动力学重新选址**。EM 阶段的谱流闭合 $f_{\text{EM}}(u)=f(\sqrt3\,u)$ 中的 $\sqrt3$ 来自坐标规范、且 $\Delta\lambda^{(\text{EM})}$ 已固定——形状无悬空自由度。

> 若有人假设 $g_{\text{EM}}(u)=(1+\beta\sqrt u)u$（初版错误），其"共轭自检"$(\beta=\sqrt3,c_{\text{EM}}=c_0)$ 不会收敛到 $\bar u=r^*/{\sqrt3}$，因为 $f(\sqrt3 u)\neq(1+\sqrt3\sqrt u)u$。**正确共轭形是 $f(\sqrt3\,u)=\sqrt3\,u\,(1+3^{3/4}\sqrt u)$**。本讲据此废弃"形状自由参数 $\beta$"表述，独立自由度收敛为 $c_{\text{EM}}$ 单参数。

## 2. 内部普适间断面（$c_{\text{EM}}$ 候选锚，零测量）

全部取自 $\{\pi,e^{\gamma_E}\}$ 与整数/维数因子（c=1 式）：

| 记号 | 定义 | 数值 |
|:--|:--|:--|
| $c_0$ | $b^3\cdot4\pi$，$b=e^{\gamma_E}/\pi$（BCS 锁，共享） | 2.2898 3917 |
| $c_{0D}$ | $a_0^3\cdot4\pi=8c_0$，$a_0=2b=2e^{\gamma_E}/\pi$（Debye 有限部，`BCSConstantOrigin`） | 18.3187 1337 |
| $c_0/8$ | $(b/2)^3\cdot4\pi$（Debye 之半） | 0.2862 2989 |

仅两条是"物理命名"的（$c_0$、$c_{0D}$）；$c_0/8$ 为判形参考。电荷归一化路（$d_{\text{EM}}=2\sqrt{q^2}$ 引入电子电荷 $e$）需先内部锁定精细结构常数 $\alpha$，本轮未纳入（见 §5.2）。

## 3. 判表（数值，mpmath 60 位）

单级参考 $\bar u^{ref}=r^*/{\sqrt3}=0.50470\,62917$（$r^*=0.87417\,69392$）。

| $c_{\text{EM}}$ 锚 | $\rho(c_{\text{EM}})$ | $\bar u=\rho(c_{\text{EM}})/\sqrt3$ | $F=r^*/\rho(c_{\text{EM}})$ | $T_c$ 相对偏移 |
|:--|:--|:--|:--|:--|
| $c_0$（BCS，共享） | 0.8741 76939 | 0.5047 06292 | **1.0000 00000**（=折叠精确） | 0% |
| $c_{0D}=8c_0$（Debye） | 4.0743 23296 | 2.3523 11652 | 0.2145 5758 | −78.5% |
| $c_0/8$ | 0.1674 96985 | 0.0967 04429 | 5.2190 6075 | +421.9% |

`F = δ_SC'/δ_SC`：F=1 两路径同 δ_SC（EM 平庸）；F≠1 时 δ_SC（经 `T_c=γ√ρ₀∝δ_SC`）相对单级理论偏移 $F-1$。Debye 态 $c_{0D}$ 给出巨大负偏移，物理上不拟取，但与 $c_0$ 的**判别性完全分得开**。

## 4. 判定含义

1. **F=1 恒等（若 ⟹ 证成）**：到达"唯一自洽内部锁"——EM 阶段不可能独立，折叠是物理学事实而非语言伪饰。§8.7#5 以可证否定收口，是**有内容的收敛**。
2. **F≠1 实存**：则该 $c_{\text{EM}}$ 为真实 EM 独立锚，$F$ 是可测预言（可与材料 $a_{\exp}$ 截线对表，衔接 RN-ENDO-006 的五材料判据）。
3. **判表既不选锚也不否定**：它把路线 A 的决策从一个直觉/拟合问题，转成一个**可形式化的结构定理**问题——`∀内部普适锚 c_EM, F(c_EM)=1 ⟺ c_EM=c₀`。

## 5. 遗留开放项（登记）

1. **二分定理 ⟹ 方向 Lean 化**：在 `SuperfluidFlow`（新增或并入 `SpectralFlowRGFlow`）形式化 $F(c_{\text{EM}})=r^*/\rho(c_{\text{EM}})$ 与"$\rho$ 严格单调 ⟹ $c_{\text{EM}}\mapsto F^{-1}$ 单射 ⟹ F=1 唯一解 $c_{\text{EM}}=c_0$"。这需要 $\rho$ 的严格单调性与连续性在抽象 c 下（`r_star_flow_lt` 已有雏形）。
2. **电荷归一化路**：精细结构常数 $\alpha=e^2/4\pi$ 是否可内部锁定（维数论证）是本路线能否真正引入"阿贝尔电荷形状"的门槛；本轮明确未处理，不伪称。
3. **下坡归一化**：$c_{0D}$ 对应 Debye 锚给出 F≪1，若要被物理采用须解释"为什么 EM 阶段以 Debye 有限部而非 BCS 锁闭合并**强压制 δ_SC**"——这本身是新的可测断言，非本讲闭合。

---
*本笔记为研究笔记，不具形式论文引用资格；如需入文须在正式论文中自足展开（见项目硬约束）。*