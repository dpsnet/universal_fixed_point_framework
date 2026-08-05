# Phase 22：谱动力学深化推进计划

**状态**：🆕 新建
**对应文档**：`notes/04_lorentz_gravity/spectral_dynamics_deepening.md`
**前置依赖**：Phase 21（Paper V 谱动力学，19/19 完成）

---

## 概述

Phase 22 在 Phase 21 的谱动力学基础框架之上，推进四个深层理论方向：
A. $\mathbf{Rec}/\mathbf{Sp}$ 高阶范畴拓展
B. 非平衡谱热力学
C. 黑洞视界谱动力学
D. 奇点谱消解

---

## 子任务清单

| 任务 | 交付物 | 状态 |
|------|--------|------|
| P22.1 高阶范畴概念框架 | `notes/04_lorentz_gravity/spectral_dynamics_deepening.md` §A | ✅ |
| P22.2 非平衡谱热力学 | `notes/04_lorentz_gravity/spectral_dynamics_deepening.md` §B | ✅ |
| P22.3 黑洞视界谱动力学 | `notes/04_lorentz_gravity/spectral_dynamics_deepening.md` §C | ✅ |
| P22.4 奇点谱消解 | `notes/04_lorentz_gravity/spectral_dynamics_deepening.md` §D | ✅ |
| P22.5 2-态射的谱流显式构造 | — | 🔲 |
| P22.6 谱熵产生率数值验证 | `scripts/paper22_spectral_entropy.py`（ΔS=0.054>0，固定基熵增验证热力学箭头） | ✅ |
| P22.7 视界谱数值模拟 (Kerr) | `scripts/paper22_horizon_spectrum.py`（T_H、S_BH匹配 0.00%、信息持守） | ✅ |
| P22.8 量子反弹宇宙数值模型 | — | 🔲 |
| P22.9 谱流体动力学 | `notes/04_lorentz_gravity/spectral_dynamics_deepening.md` §F + `scripts/paper22_fluid_dynamics.py`（K41谱、N-S谱流方程、跨领域类比） | ✅ |

---

## 与现有框架的关系

| 方向 | 连接 Phase 21 § | 连接 Paper |
|------|----------------|------------|
| A. 高阶范畴 | §2 谱流方程 | 延伸 |
| B. 非平衡热力学 | §4.2 谱动力学预言 | 新方向 |
| C. 黑洞视界 | §4.5 LQG 对应、§4.6 类 GR | Paper IV 交叉 |
| D. 奇点消解 | §4.5 $A_{\text{GR}}$ 离散谱、§7 宇宙学 | Paper II Kerr QNM |
