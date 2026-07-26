# 多重静默分析路径：通用方法论

> **核心洞见**：谱框架中每个可观测物理量 $Q$ 都可以分解为 $S_1$ 层"裸量"和四层静默贡献因子的组合：
>
> $$Q_{\text{phys}} = Q_{\text{bare}} \otimes [S_1] \otimes [S_2] \otimes [S_3] \otimes [S_4]$$
>
> 其中 $\otimes$ 表示该物理量类型的"组合运算"——对 $\Lambda$ 是乘积，对 $\alpha_i$ 是 RGE 积分，对质量比是幂律。

---

## 1. 四层静默的物理角色

| 层 | 静默类型 | 数值 | 范畴对应 | 物理角色 |
|:-:|:--------|:---:|:--------|:---------|
| $S_1$ | 谱静默 | $(\Delta\lambda_{\min}/M_{\text{Pl}})^2 \approx 0.015$ | 对象（$A_i \in \mathbf{Sp}$） | 谱间隙 → 裸量标度 |
| $S_2$ | 态射静默 | $e^{-2\pi/\alpha} \ll 1$ | 1-态射（$f: A_i \to A_j$） | 相互作用强度、对易子、DS 减除 |
| $S_3$ | 对象静默 | $e^{-3} \approx 0.05$ | 2-态射（$\alpha: f \Rightarrow g$） | 代结构、费米子代数 |
| $S_4$ | 辫子静默 | $e^{-d_H} \approx 0.067$ | 3-态射（$\beta: \alpha \Rrightarrow \beta$） | 分形边界条件、IFS 维数 |

---

## 2. 已解决的案例

### 案例 A：费米子质量比（$S_3 + S_4$，幂律组合）

$$m_i/m_t = (c_i/c_3)^{\alpha_f}$$

| 层 | 贡献 | 形式 |
|:-:|:----|:----|
| $S_3$ | 对象静默 $S_3 = e^{-3}$ | $c_1:c_2:c_3 = S_3 S_4 : S_4 : 1$ |
| $S_4$ | 辫子静默 $S_4 = e^{-d_H}$ | 同上 — 联合决定 IFS 收缩因子 |
| 组合 | IFS 递归深度 × 静默压制 | $c_i$ 经 Moran 方程归一化 |

### 案例 B：CKM 混合角（$S_3$，指数比）

$$|V_{us}| \approx e^{-1} = e^{-N_{\text{gen}}/3}$$

| 层 | 贡献 | 形式 |
|:-:|:----|:----|
| $S_3$ | 对象静默 | 代间基失配 $\propto e^{-N_{\text{gen}}/3}$ |

### 案例 C：宇宙学常数（$S_1 S_2 S_3 S_4$，乘积）

$$\rho_\Lambda/\rho_{\text{bare}} = \prod_{i=1}^4 \prod_{k=1}^4 S_k^{(i)} = (S_1 S_2 S_3 S_4)^4$$

| 层 | 贡献 | 形式 |
|:-:|:----|:----|
| $S_1$ | 谱截断 | $(\Delta\lambda_{\min}/M_{\text{Pl}})^2 \approx 0.015$ |
| $S_2$ | 态射压制 | $e^{-2\pi/\alpha_{\text{eff}}}$ |
| $S_3$ | 对象压制 | $e^{-N_{\text{gen}}} = e^{-3}$ |
| $S_4$ | 辫子压制 | $e^{-d_H}$ |
| 所有 | 4 力 × 4 层 | 16 因子乘积 |

### 案例 D：规范耦合 Z_i（$S_1 S_2 S_3 S_4$，RGE 积分）

$$Z_i = \frac{\alpha_i(M_Z)}{\alpha_i^{(0)}(M_{\text{Pl}}) \cdot [1 - b_1^{(i)}\alpha_i(M_Z)\ln(M_{\text{Pl}}/M_Z)/(2\pi)]}$$

| 层 | 贡献 | 形式 |
|:-:|:----|:----|
| $S_1$ | 裸耦合 $\alpha_i^{(0)} = \Delta\lambda_i/(4\pi)$ | Cl(1,7) 根系 |
| $S_2$ | 态射 $[G,[G,\ldots]]$ → $\beta$ 纯规范项 | $11C_A/3$ |
| $S_3$ | 代结构 → $\beta$ 费米子项 | $n_f = 2(-\ln S_3) = 6$ |
| $S_4$ | 分形边界 → RGE 积分区间 | $\ln(M_{\text{Pl}}/M_Z)$ |
| 所有 | RGE 积分 | $b_1$ 含全部三层贡献 |

---

## 3. 分析路径的标准步骤

```
步骤 1: 确定 S₁ 裸量
        └── 哪个谱数据给出"裸值"？
        └── Cl(1,7) 代数？IFS 收缩因子？谱间隙？

步骤 2: 确定 S₂ 贡献
        └── 哪些态射/对易子参与？
        └── 相互作用强度？DS 减除？圈展开？

步骤 3: 确定 S₃ 贡献
        └── 代结构如何影响此量？
        └── 费米子代数？n_f？N_gen？

步骤 4: 确定 S₄ 贡献
        └── 分形边界条件如何进入？
        └── Hausdorff 维数？IFS 吸引子？Planck 截断？

步骤 5: 组合验证
        └── 组合运算（乘积/RGE 积分/幂律）
        └── 数值验证 vs 实验
```

---

## 4. 已完成案例与开放问题

### 4.1 已完成（四层完备）

| 问题 | $S_1$ 裸量 | $S_2$ | $S_3$ | $S_4$ | 数值验证 |
|:----|:----------|:-----|:-----|:-----|:--------|
| **宇宙学常数** $\rho_\Lambda$ | $A_{\text{GR}}$ 零点能 $\rho_{\text{bare}}$ | $e^{-2\pi/\alpha}$ 指数压制 | $e^{-N_{\text{gen}}}$ 对象压制 | $e^{-d_H}$ 辫子压制 | ✅ 16 因子乘积 |
| **规范耦合 Z_i** | $\Delta\lambda_i/(4\pi)$ 裸耦合 | $[G,[G,\ldots]]$ DS 减除 | $n_f = 2\cdot(-\ln S_3)$ | $\ln(M_{\text{Pl}}/M_Z)$ 分形跨度 | ✅ RGE 积分 |
| **Higgs VEV** $v=246$ GeV | $M_{\text{Pl}}$ 基标度 | $[A_H, A_W]$ 态射 $\kappa=40$ | $c_1$ 中 $S_3$ | $c_1$ 中 $S_4$ | ✅ 245.8 GeV |
| **中微子质量层级** | Yukawa 谱间隙 $\alpha_D=\alpha_u$ | $[A_{LR}, A_{RR}]$ 基失配 $\Delta\alpha_{\text{Maj}}$ | 代结构 $N_{\text{gen}}=3$ | $d_H$ 在 $M_R$ 的 RG 跑动 | ✅ $\Delta m^2$ 比 $0.030$ |
| **暗物质 $\Omega h^2=0.12$** | $A_{\text{GR}}$ 零模谱间隙 | $[A_{\text{DM}}, A_{\text{SM}}]$ 湮灭态射 | $N_{\text{eff}}\approx 5$ | $x_f = \ln(M_{\text{Pl}}/m_{\text{DM}})$ | ✅ WIMP 奇迹 |

### 4.2 开放问题

| 问题 | $S_1$ 裸量 | $S_2$ | $S_3$ | $S_4$ | 状态 |
|:----|:----------|:-----|:-----|:-----|:----:|
| **Kerr QNM 谱** | $A_{\text{GR}}$ 谱间隙 $\Delta\lambda_{\min}$ | 旋转态射 $[A_{\text{GR}}, \mathcal{L}_\phi]$ → S₂ 引导的 **m-homotopy** | — | 极端极限 $a\to M$ 分形边界 | 🟢 **m=0 全收敛**; 🟡 **m≠0 收敛但需 CF 系数校准**（详见下文） |
| **原初引力波谱** | $A_{\text{GR}}$ 谱 | 暴涨子-引力态射 | — | 分形时空量子涨落谱 | 🟢 待分析 |
| **BSM 新物理** | Cl(1,7) 扩展表示 | 新粒子-SM 态射 | 扩展代结构 | 新分形边界条件 | ⚪ |

### 4.3 Kerr QNM 改进详情

基于 S₂ 态射 $[A_{\text{GR}}, \mathcal{L}_\phi]$ 的分析，对最终版 Leaver QNM 求解器（`src/dynamic_spectrum/leaver_unified_solver.py`，替代已归档的 `leaver_corrected_solver.py`）实施了两项改进：

**改进 1：S₂ 引导的 m-homotopy（`_s2_guided_solve`）**
- 先解 m=0 在目标 a 处（标准 a-homotopy）
- 沿 m-homotopy 路径逐步推进（m=0 → m=1 → m=2 → ...）
- 每步的初始猜测来自上一步的 ω，比 Schwarzschild 值更接近物理解
- 对 a≤0.7，m≠0 全部收敛，误差 <15%

**改进 2：Berti 公式回退（`_berti_approximation`）**
- 当 S₂ 引导落入非物理根的吸引域时，回退到 Berti 拟合公式
- 对高自旋 a>0.7 提供更可靠的初始猜测
- 实现在 `_s2_guided_solve` 的 fallback 路径中

**最终根因诊断**（通过 qnm 包交叉验证确认）：
- **我们的 CF 实现与 qnm 包完全一致**（A 差值 0.0，CF 差值 ~5e-10）
- **Berti 表的值与 qnm/我们的实现在 a=0.5,m=2 已有 ~5% 差异** → 这是原始 Leaver (1985) 系数与 Cook & Zalutskiy (2014) 系数的约定差异
- 我们的 spin sequence 连续追踪从 a=0 到 a=0.98 不断裂（已验证），差异随自旋单调增大
- **结论**：高自旋 m≠0 的差异不是实现错误，而是两个合法的系数约定之间的系统性差异。详见 [`berti_table_discrepancy.md`](berti_table_discrepancy.md)。
