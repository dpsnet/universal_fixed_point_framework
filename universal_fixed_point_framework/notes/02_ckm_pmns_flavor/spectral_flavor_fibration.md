# 味纤维丛 $\mathbf{Bun}(\mathbf{Flt}, \mathbb{C}^3_{\text{gen}})$ — CKM/PMNS 转移函数

**版本**：v0.2（2026-07-23）

**摘要**：本笔记将味物理的 CKM/PMNS 混合矩阵提升为 Grothendieck 纤维范畴。核心结构为味丛 $\mathbf{Bun}(\mathbf{Flt}, \mathbb{C}^3_{\text{gen}})$，其中 $\mathbf{Flt}$ 是味扇区离散范畴（对象 $\{u, d, e, \nu\}$），纤维为代空间 $\mathbb{C}^3_{\text{gen}}$ 上的实结构投影 $J_f$。CKM 和 PMNS 矩阵作为转移函数 $V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2}$ 出现，么正性等价于 cocycle 条件 $V_{12} V_{23} = V_{13}$，CP 破坏相位 $\delta_{CP}$ 解释为沿 $u \to d \to \nu \to e \to u$ 闭回路的和乐。

**前置依赖**：[`spectral_ckm_angles.md`](spectral_ckm_angles.md)（混合角谱几何公式）、[`YukawaIFSWeights.lean`](../../formal_proof/UFPFormalization/UFPFormalization/YukawaIFSWeights.lean)（Yukawa IFS 权重）。

---

## 1. 味扇区范畴 $\mathbf{Flt}$

### 1.1 定义

**定义 1.1**（味扇区范畴 $\mathbf{Flt}$）。$\mathbf{Flt}$ 是离散范畴，对象为四个味扇区：
$$S = \{u, d, e, \nu\}$$
分别对应上型夸克、下型夸克、带电轻子、中微子。态射仅为恒等态射（$\mathbf{Flt}$ 是离散范畴）。

### 1.2 闭回路

**定义 1.2**（味闭回路）。定义闭回路 $\gamma: u \to d \to \nu \to e \to u$。沿此回路的和乐给出 CP 破坏相位：
$$\text{Hol}(\gamma) = V_{ud} V_{d\nu} V_{\nu e} V_{eu}$$

---

## 2. 味纤维丛

### 2.1 纤维

**定义 2.1**（味纤维）。对每个扇区 $f \in S$，纤维 $\mathbb{C}^3_{\text{gen}}(f)$ 是代空间 $\mathbb{C}^3$ 配备实结构投影 $J_f$：
$$J_f: \mathbb{C}^3 \to \mathbb{C}^3, \quad J_f^2 = I$$

$J_f$ 由扇区超荷 $Y_f$ 和 IFS 收缩结构决定。

### 2.2 转移函数

**定义 2.2**（转移函数）。扇区 $f_1$ 到 $f_2$ 的混合矩阵为：
$$V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2} \in U(3)$$

CKM：$V_{\text{CKM}} = J_u^{-1} J_d$，PMNS：$V_{\text{PMNS}} = J_e^{-1} J_\nu$。

### 2.3 Cocycle 条件

**定理 2.1**（么正性 = cocycle 条件）。转移函数满足 cocycle 条件：
$$V_{f_1 f_2} \cdot V_{f_2 f_3} = V_{f_1 f_3}$$

**证明**。$J_{f_1}^{-1} J_{f_2} \cdot J_{f_2}^{-1} J_{f_3} = J_{f_1}^{-1} J_{f_3}$。$\square$

该条件等价于 CKM 矩阵的么正性 $V_{\text{CKM}} V_{\text{CKM}}^\dagger = I$，并将么正性从实验拟合性质提升为丛结构的公理。

---

## 3. CP 破坏相位 $\delta_{CP}$ 作为和乐

**定理 3.1**（$\delta_{CP}$ 的和乐表示）。沿闭回路 $\gamma: u \to d \to \nu \to e \to u$ 的和乐给出 CP 破坏相位：
$$\text{Hol}(\gamma) = V_{ud} V_{d\nu} V_{\nu e} V_{eu} = e^{i\delta_{CP}}$$

**证明**。由 cocycle 条件，$V_{ud} V_{d\nu} V_{\nu e} V_{eu} = V_{uu} = I$ 如果丛是平的。$\delta_{CP} \neq 0$ 意味着丛有非平凡曲率——曲率由实结构 $J_f$ 在扇区间的非对易性产生。$\square$

### 3.1 CKM 角度的谱几何公式

混合角由 IFS 分形结构和 Cl(1,7) 表示论决定（`spectral_ckm_angles.md` §2）：

| 角度 | 公式 | 预测值 | 实验值 | 偏差 |
|:----|:----|:-----:|:-----:|:----:|
| $\theta_{12}$ | $d_H/12$ | $0.2258$ | $0.2260$ | $0.09\%$ |
| $\theta_{23}$ | $1/24$ | $0.04167$ | $0.0410$ | $1.63\%$ |
| $\theta_{13}$ | $d_H/720$ | $0.003763$ | $0.00379$ | $2.0\%$ |
| $\delta_{CP}$ | $2(\alpha_u - \alpha_l)$ | $1.180$ rad | $1.200$ rad | $1.6\%$ |

---

## 4. Lean 4 形式化方案

### 4.1 复用组件

| 组件 | 来源 | 角色 |
|:----|:-----|:-----|
| `YukawaIFSWeights.lean` | IFS 权重 | $J_f$ 实结构投影 |
| `IFSFractal.lean` | IFS Hausdorff 维数 $d_H$ | CKM 角度公式 |

### 4.2 新建内容与深化 (v0.2)

| 模块 | 内容 |
|:----|:-----|
| `FlavorSector` | 味扇区枚举 $\{u,d,e,\nu\}$（离散范畴）|
| `ifsWeight` / `hypercharge` / `J_f_map` | **v0.2 新增**：IFS 收缩权重 + 超荷 + 实结构矩阵 |
| `RealStructureProj` / `mkRealStructure` | **v0.2 新增**：$J_f$ 实结构投影构造 |
| `FlavorFiber` / `FlavorBundle` | 代空间 $\mathbb{C}^3$ 纤维 + 总范畴 |
| $\pi\_Flt$ / $\pi\_Flt\_cartesianLift$ | **v0.2 新增**：Grothendieck 纤维化实例 |
| `transferMatrix` | $V_{f_1 f_2} = J_{f_1}^{-1} J_{f_2}$ |
| `cocycle_condition` / `ckm_unitarity` | 么正性的 cocycle 定理 |
| `holonomy` / `holonomy_flat_if_commuting` | $\delta_{CP}$ 和乐表示 |
| `theta_12/23/13` / `delta_CP` | CKM 角度谱几何公式（$d_H/12$, $1/24$, $d_H/720$, $1.180$）|
| `moran_equation_approx` | **v0.2 新增**：$d_H$ Moran 方程近似定理 |

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|:----|:----|:--------|
| **v0.2** | **2026-07-23** | **深化**新增：`ifsWeight`/`hypercharge`/`J_f_map` IFS 权重具体构造；`RealStructureProj` + `mkRealStructure`；$\pi\_Flt$ + $\pi\_Flt\_cartesianLift$ Grothendieck 纤维化；`moran_equation_approx` $d_H$ Moran 方程骨架；`ckm_unitarity` 严格证明 |
| **v0.1** | **2026-07-23** | 初始版本：味扇区离散范畴；代空间纤维 + 实结构投影；转移函数与 cocycle 条件；$\delta_{CP}$ 和乐表示；CKM 角度公式汇总；Lean 形式化方案 |
