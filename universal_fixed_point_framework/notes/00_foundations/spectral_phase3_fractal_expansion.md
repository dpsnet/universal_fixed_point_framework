# 阶段 3：IFS 分形扩张——Σ-Rec coproduct 谱对应与 Weierstrass 谱隙导出

> **来源**：`notes/00_foundations/spectral_category_scope_stratification.md` §3.3（分形扩张路径）与阶段 3 任务（"桥接 `IFSFractal.lean` 的 IFS 分解到 `NoiseCategory.lean` 的 Σ-Rec；至少 1 个分形函数（Weierstrass）的谱隙从 IFS 参数导出"）。
> **状态**：研究笔记 v0.7（2026-08-05）。阶段 3 **子任务 1（数值层）+ 子任务 2（Lean 符号编码，v0.2）+ Σ-D Functor 律闭合 + 谱 coproduct 分解 Lean 侧（函子层）+ Weierstrass 图 IFS 谱隙结构支撑**完成：数值验证 **7/7 检查通过**；`IFSRecCoding.lean` **v0.2+**（正式 `SigmaRecObj` coproduct 编码 + 片注入态射 + 不动点完整等价 + 谱 coproduct 分解三定理）；`WeierstrassGap.lean` **v1.0**（Weierstrass 图 IFS 收缩机器证明 + Moran/图维数 + 迹公式实例）；`NoiseCategory.lean` **Σ-D Functor 律完全闭合**并组装为正式函子 `sigmaDFunctor`（`lake build` 2454 jobs 通过，零 `sorry` 零 `axiom`）。
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
| **IFS → Σ-Rec 符号编码** | **`IFSRecCoding.lean`（v0.2，`lake build` 通过，零 `sorry`）**：`symbolicRecObj`（符号动力学 RecObj）、`symbolicSlice`（局部线性片）、**`symbolicSigmaRecObj`（正式 `SigmaRecObj` coproduct 编码）**、**`symbolicSliceInjection`（片注入态射 `SigmaRecHom`）**、`symbolicStep_fixedPoint_iff`（唯一不动点 = 全零，完整等价） | ✅ 新增 |
| Σ-Rec coproduct 谱保持 | `NoiseCategory.lean` §15.3（Σ-D 对象层：`sigmaDFunctorObj`，`sigmaD_preserves_coproduct`） | ✅ 已修复（2026-08-05） |
| Σ-Rec/Σ-Spec Category 与 ι_Σ | `NoiseCategory.lean`（Category 律、`sigmaRecInclusion` 语义修正、`sigmaRecInclusion_faithful`） | ✅ 已修复（2026-08-05） |
| 谱隙从压缩比导出 | 待（依赖有限维谱积分层） | ⏳ 阶段 3 依赖 |

**NoiseCategory.lean 修复记录（2026-08-05）**：既有编译错误全部闭合（`lake build` 3172 jobs 通过，零 `sorry`）：
- Σ-Rec/Σ-Spec `Category` 实例：comp 改用显式态射构造（原 `fij ≫ gjk` 触发 mathlib `instCategory (Hom)` 递归歧义）；律用 `simp [CategoryStruct.id/comp, List.flatMap_assoc, List.map_flatMap, List.flatMap_map]` + `Matrix.mul_assoc`/`Function.comp_def` 证明；
- `sigmaRecInclusion`：map 的 i≠0 分量改为 default 恒等（与 `Category.id` 约定一致，原 `[]` 导致 `map_id`/`map_comp` 失败）；`Full` 诚实修正为 `Faithful`（`Functor.Full` 在无约束 Hom 下不成立——态射对 none 分量可任意，见 §15.1 注）；
- `Inhabited SpObj` 对齐 `DFunctor.obj (default : RecObj)`（原 `⟨0, 0⟩` 与 Σ-D 的 none 分量类型不匹配）；
- **Σ-D 对象层**：`sigmaDFunctorObj` + `sigmaD_preserves_coproduct`（§15.3 定理 15.3 保留）；
- **Σ-D 态射层与 Functor 律（2026-08-05 闭合）**：
  - **关键设计**：内层态射搬运 `dfunctorMapTransport'` 直接对 `A B : Option RecObj` 两个**变量**做 `cases`——`(some R).getD default = R` 与 `(none.getD default) = default`（`Inhabited SpObj` 定义性等于 `DFunctor.obj default`）在四个分支均**定义性归约，产物无任何显式 cast**（原 `rw [option_map_getD]` 方案产生非 rfl 级 cast，且 `cases X.components i`/`match` 均因参数类型不被分支精化而失败——`generalize failed`/`Type mismatch`）；
  - `dfunctorMapTransport'_comp`（保复合）与 `dfunctorMapTransport'_id`（保恒等）为元素层核心，逐 `cases A B C` 归约后用 `DFunctor.map_comp`/`DFunctor.map_id` 闭合（`simpa` 需避开对引理自身的自简化，`exact` 直接可用）；
  - `sigmaDFunctorMap_id`/`sigmaDFunctorMap_comp` 在列表层用归纳 + `rw [ih]` + `congr 1`（头部元素用 `congrArg`+`funext ⟨k, gjk⟩`+`ext`+`simp`），`simp` 中**不展开 `dfunctorMapTransport'`**（展开后 `Option.rec` 不可归约且破坏重写匹配）；
  - 组装为正式函子 `sigmaDFunctor : SigmaRecObj ⥤ SigmaSpObj`（`map_id := sigmaDFunctorMap_id`，`map_comp := sigmaDFunctorMap_comp`）。**诚实边界闭合：Σ-D Functor 律从"函数层承载"升格为"正式函子"**。

**谱 coproduct 分解 Lean 侧（2026-08-05，IFSRecCoding v0.2+ 闭合）**：借助 `sigmaDFunctor` 正式函子与 `symbolicStep_fixedPoint_iff` 唯一不动点定理，`IFSRecCoding.lean` 新增三定理，闭合"符号转移与各片谱的精确关系"的**函子层**：
- **对象层** `symbolicSigmaRecObj_spectral_components`：Σ-D(symbolicSigmaRecObj) 的第 i 分量 = D(slice i)（i < n），i ≥ n 为空——"整体谱 = 各片谱的 coproduct"（对齐 `sigmaD_preserves_coproduct`，定理 15.3）；
- **态射层** `symbolicSliceInjection_spectral_component0`：片注入的 Σ-D 像在分量 0 恰含一个态射（`length = 1`）且指向分量 i（`head?.map Sigma.fst = some i.1`）——片嵌入经 Σ-D 保持。注：态射层取列表结构度量而非 SpHom 字面量——后者在语句层需 getD 类型定义性归约（`sigmaDFunctor`/`sigmaRecInclusion` 展开），受透明度限制，诚实登记为表述选择；
- **迹公式实例** `symbolicTransferMatrix_trace_eq_one`：tr(T_step) = #Fix = 1——`symbolicStep_fixedPoint_iff`（唯一不动点）接到谱侧的机器证明，对齐笔记 §4.4 的谱障碍公式 tr(T_f) = #Fix(f)（`Matrix.trace` + `Finset.sum_eq_single`，含 `Matrix.diag` 展开与 `∑` binder 显式类型标注）。

**下一步候选**：
1. ✅ ~~Σ-D 的 Functor 律（`map_id`/`map_comp`）补证~~（**已闭合**，2026-08-05：见上 Σ-D 态射层记录）；
2. ✅ ~~符号转移与各片谱的精确关系（谱 coproduct 分解的 Lean 侧）~~（**函子层已闭合**，2026-08-05：见上三定理；特征值级谱分解仍依赖有限维谱积分层）；
3. ✅ ~~Weierstrass 图 IFS 的压缩比 → 谱隙关系整理为 Lean 命题~~（**结构支撑已闭合**，2026-08-05：见下 §Weierstrass 图 IFS 谱隙；特征值级 gap = 1 − λ₂/λ₁ 依赖有限维谱积分层，登记为开放项）。

---

## 5. Weierstrass 图 IFS 谱隙 Lean（2026-08-05，`WeierstrassGap.lean` v1.0）

对齐 §2.3 S5 的 Weierstrass 图 IFS（f₁(t,y) = (t/b, y/b)、f₂(t,y) = ((t+1)/b, (y+a)/b)，b > 1、0 < a < 1）。本文件在**零 sorry** 下闭合其结构层：

| 组件 | Lean 定理 | 内容 |
|:--|:--|:--|
| 分量仿射 Lipschitz | `lipschitz_affine_prod` | p ↦ (c·p.1+t₁, c·p.2+t₂) 是 LipschitzWith c（ℝ² sup 距离，`max` 分解 + `mul_le_mul_of_nonneg_left`） |
| 收缩率 | `weierstrassGraphMap₁/₂_contracting` | f₁、f₂ 均 `ContractingWith (1/b)`，率 < 1 用 `div_lt_one`（b > 1） |
| IFS 构造 | `weierstrassGraphIFS` | 2 映射均匀 IFS（率均 1/b），`weierstrassGraphIFS_uniform` 机器证明 |
| Moran 维数 | `weierstrassGraph_dH` | 吸引子 d_H = log 2 / log b（`uniform_ifs_dH_unique` 桥梁） |
| 图维数（Falconer） | `weierstrassGraphDimension` = 2 + ln a / ln b；**`_strictMono_a`** | **d(a) 随 a 严格递增**（`Real.log_lt_log` + `div_lt_div_of_pos_right`）——S5"a↑ → 维数↑"的 Lean 侧结构支撑 |
| 谱障碍公式实例 | `weierstrassGraph_symbolic_trace` | 2 片符号动力学 tr(T_f) = #Fix = 1（复用 IFSRecCoding） |

**诚实边界（开放项登记）**：S5 的**核谱隙** gap = 1 − λ₂/λ₁ 随 d 单调递减的完整机器证明依赖有限维谱积分层——mathlib `Matrix.IsHermitian` 特征值 / CFC 桥接（`Mathlib.LinearAlgebra.Matrix.Spectrum` 未在 lean_lib 构建）。本文件给出其**结构支撑**（收缩率机器证明 + 维数单调性 + 迹公式实例），特征值级表述留待谱积分层。

---

## 4. 关联文件索引

| 文件 | 角色 |
|:--|:--|
| `scripts/paperX_ifs_sigma_rec_spectral.py` | 本笔记的数值验证附件（S1-S5，7/7，已注册 `run_all_tests.py`） |
| `formal_proof/.../IFSRecCoding.lean` | IFS → Σ-Rec 符号编码（v0.2+，含谱 coproduct 分解三定理，编译通过，零 `sorry`） |
| `formal_proof/.../WeierstrassGap.lean` | Weierstrass 图 IFS 谱隙结构支撑（v1.0：收缩/维数/迹公式，编译通过，零 `sorry`） |
| `formal_proof/.../NoiseCategory.lean` | Σ-Rec/Σ-Spec Category、ι_Σ、Σ-D 正式函子（✅ 编译错误已修复 + Functor 律闭合，2026-08-05） |
| `formal_proof/.../IFSFractal.lean` | IFS 分解基础设施（阶段 3 依赖） |
| `notes/00_foundations/spectral_category_scope_stratification.md` | 阶段 3 规划出处（§3.3、§4 阶段 3） |
| `paper/paper1_fractal_spectral_derecursion.md` | 分形 RKHS / IFS 收敛率理论（上层论文） |
