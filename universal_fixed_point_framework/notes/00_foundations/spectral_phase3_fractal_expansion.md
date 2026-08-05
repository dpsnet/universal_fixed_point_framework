# 阶段 3：IFS 分形扩张——Σ-Rec coproduct 谱对应与 Weierstrass 谱隙导出

> **来源**：`notes/00_foundations/spectral_category_scope_stratification.md` §3.3（分形扩张路径）与阶段 3 任务（"桥接 `IFSFractal.lean` 的 IFS 分解到 `NoiseCategory.lean` 的 Σ-Rec；至少 1 个分形函数（Weierstrass）的谱隙从 IFS 参数导出"）。
> **状态**：研究笔记 v0.2（2026-08-05）。阶段 3 **子任务 1（数值层）+ 子任务 2（Lean 符号编码）完成**：数值验证 **7/7 检查通过**（`paperX_ifs_sigma_rec_spectral.py`，已注册 `run_all_tests.py`）；Lean 侧 `IFSRecCoding.lean` **编译通过（`lake build`，零 `sorry`）**——符号动力学 RecObj、局部线性片、coproduct 对象编码、不动点刻画。`NoiseCategory.lean` 完整 Σ-Rec 范畴存在**既有编译错误**（独立修复任务）。
> **规范声明**：本文为**谱新增**推导——"IFS 分解 → Σ-Rec coproduct → 谱对应"的数值验证与构造是阶段 3 的推进记录；`IFSFractal.lean`（IFS/Attractor/SelfSimilarMeasure/HausdorffDim 基础设施）与 `NoiseCategory.lean`（Σ-Rec/ι_Σ，§15.3 D 保持 coproduct 机器证明）为既有资产。

---

## 1. 阶段 3 目标与扩张路径

阶段 2（分层）完成后，非线性分形函数（Weierstrass、Cantor 等）**不满足线性条件**，不在 Rec_lin 中。扩张路径（§3.3）：

$$
\underbrace{\text{IFS 分解}}_{\text{局部线性片 }\{f_i\}} \;\longrightarrow\; \underbrace{\Sigma\text{-Rec coproduct}}_{\bigoplus_{i \in I} R_i,\ R_i \in \mathbf{Rec}_{lin}} \;\longrightarrow\; \underbrace{\text{谱对应}}_{D \text{ 在每片上保持线性谱，整体 } = \bigoplus \sigma_D(R_i)}
$$

**关键**：分形的谱对应走"局部线性 + 全局 coproduct"路径，不经过 D ⊣ R 伴随的全范畴有效性（阶段 1 圈定的边界之外）。

## 2. 构造（首个数值子任务）

### 2.1 Σ-Rec 编码（S2）

对 2-map IFS $\{f_1, f_2\}$（压缩仿射），Hutchinson 迭代采样吸引子点集 $P \subset \mathbb R$（S1）。**Σ-Rec 编码**：每个点归入"最近片"——$x \in R_i$ 若 $i = \arg\min_j |x - f_j(x)|$。每片 $R_i$ 为一个 $\mathbf{Rec}$ 对象：

- 状态空间 $R_i.T$ = 片内点集；
- 步进 $R_i.\mathrm{step}$ = 片映射 $f_i$ 诱导的确定性转移（$f_i(p)$ 在片内取最近点）。

整体 $\Sigma$-Rec 对象 = $\bigoplus_i R_i$，对应整体谱化转移矩阵 $T = \mathrm{blockdiag}(T_1, T_2)$。

### 2.2 D 保持 coproduct 的数值镜像（S3）

**验证**：块对角矩阵特征值 = 各块特征值并集（代数重数相加）：
$$\sigma(T) = \sigma(T_1) \cup \sigma(T_2),$$
数值残差 $< 10^{-9}$。这是 `NoiseCategory.lean` §15.3 机器证明定理（Σ-D 保持 coproduct）的数值镜像——阶段 3 的"整体谱 = 各片谱的 coproduct"机制在数值层面成立。单位模特征值数量亦逐块守恒（确定性步进的谱结构：特征值 ∈ {单位根} ∪ {0}）。

### 2.3 谱性质从 IFS 参数导出（S4/S5，阶段 3 验证目标）

**S4（Cantor，谱复杂度）**：真对称 Cantor IFS $f_1(t) = ct$、$f_2(t) = ct + (1-c)$（$c \in (0, 0.5)$），Moran 维数 $d = \ln 2 / \ln(1/c)$。分形 RKHS 核矩阵 $K_{xy} = \exp(-|x-y|^2/2\sigma^2)$ 的**有效秩**（累计 95% 谱能量的特征值个数）：

| $c$ | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 |
|:--|:--|:--|:--|:--|:--|:--|
| $d$ | 0.431 | 0.500 | 0.576 | 0.660 | 0.756 | 0.868 |
| 有效秩 | 12 | 15 | 19 | 28 | 35 | 50 |

**有效秩随分形维数严格单调递增**（对核尺度 σ 稳健）——分形维数越大，RKHS 谱需要越多分量达到同一能量占比。**谱复杂度从 IFS 压缩比导出**。

**S5（Weierstrass，谱隙，阶段 3 验证目标正面命中）**：Weierstrass 图 IFS（2D）
$$f_1(t, y) = \Big(\tfrac{t}{b}, \tfrac{y}{b}\Big), \qquad f_2(t, y) = \Big(\tfrac{t+1}{b}, \tfrac{y+a}{b}\Big),$$
固定 $b = 3$、扫描 $a \in (0,1)$（$ab \geq 1$ 保持非光滑）。Moran 维数 $d(a) = 2 + \ln a / \ln b$（Falconer）：

| $a$ | 0.30 | 0.45 | 0.60 | 0.75 | 0.90 |
|:--|:--|:--|:--|:--|:--|
| $d$ | 0.904 | 1.273 | 1.535 | 1.738 | 1.904 |
| 核谱隙 $1 - \lambda_2/\lambda_1$ | 0.0142 | 0.0126 | 0.0103 | 0.0074 | 0.0043 |

**谱隙随 Moran 维数单调递减**（$d \uparrow \Rightarrow \mathrm{gap} \downarrow$）：图越"皱"（维数越高），核谱越接近全 1 退化结构。这是阶段 3 验证目标"**至少 1 个分形函数（Weierstrass）的谱隙从 IFS 参数导出**"的数值实现。

> **注（1D 谱隙的非单调教训）**：早期设计用 1D 区间型 IFS + 固定 σ 扫描"谱隙 vs 压缩比"得非单调结果（gaps = [0.053, 0.057, 0.043, 0.178, ...]）——根源是 1D 吸引子尺度随压缩比变化、与固定 σ 不匹配，且区间型吸引子非真分形。**改用（a）谱复杂度（有效秩，对 σ 稳健）与（b）2D Weierstrass 图（真分形）后单调性干净成立**。诚实登记：谱隙作为单一数值量对核尺度敏感，谱复杂度与 2D 真分形是稳健载体。

## 3. 与 Lean 的桥接点

| 阶段 3 组件 | Lean 侧 | 状态 |
|:--|:--|:--|
| IFS / 吸引子 / 维数 | `IFSFractal.lean`（IFS、Attractor、SelfSimilarMeasure、HausdorffDim） | ✅ 已有 |
| **IFS → Σ-Rec 符号编码** | **`IFSRecCoding.lean`（新，2026-08-05，`lake build` 通过，零 `sorry`）**：`symbolicRecObj`（符号动力学 RecObj，左移补 0 步进）、`symbolicSlice`（局部线性片 RecObj）、`symbolicCoproductObj`（coproduct 对象编码）、`symbolicStep_fixedPoint_eq_zero`（不动点 ⟹ 全零，末位为 0 + 平移链） | ✅ 新增 |
| Σ-Rec coproduct 谱保持 | `NoiseCategory.lean` §15.3（Σ-D 保持 coproduct） | ⚠️ 既有编译错误（缺 `CategoryTheory` import 等，2026-08-05 核实，独立修复任务） |
| 谱隙从压缩比导出 | 待（依赖有限维谱积分层） | ⏳ 阶段 3 依赖 |

**下一步候选**：
1. 修复 `NoiseCategory.lean` 的既有编译错误（`CategoryTheory` import、`Full`/`Faithful` 解析、ext 失败），使完整 Σ-Rec 范畴可用；
2. 态射层桥接：片嵌入 RecHom（符号转移与各片谱的精确关系，IFSRecCoding 诚实边界）；
3. 将 Weierstrass 图 IFS 的压缩比 → 谱隙关系整理为 Lean 命题（依赖有限维谱积分层，mathlib `ContinuousFunctionalCalculus` 桥接）。

---

## 4. 关联文件索引

| 文件 | 角色 |
|:--|:--|
| `paperX_ifs_sigma_rec_spectral.py` | 本笔记的数值验证附件（S1-S5，7/7，已注册 `run_all_tests.py`） |
| `formal_proof/.../IFSRecCoding.lean` | IFS → Σ-Rec 符号编码（子任务 2，编译通过，零 `sorry`） |
| `formal_proof/.../IFSFractal.lean` | IFS 分解基础设施（阶段 3 依赖） |
| `formal_proof/.../NoiseCategory.lean` | Σ-Rec / ι_Σ / §15.3 D 保持 coproduct（⚠️ 既有编译错误，待修复） |
| `notes/00_foundations/spectral_category_scope_stratification.md` | 阶段 3 规划出处（§3.3、§4 阶段 3） |
| `paper/paper1_fractal_spectral_derecursion.md` | 分形 RKHS / IFS 收敛率理论（上层论文） |
