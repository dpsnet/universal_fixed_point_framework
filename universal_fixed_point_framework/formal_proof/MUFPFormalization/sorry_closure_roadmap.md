# MUFPF 形式化 sorry 清零路线图

**文档编号**：MUFPF-SORRY-ROADMAP-001
**日期**：2026-09-11
**版本**：v1.0
**配套**：ENV_GUIDE.md v1.2 §9（统计口径）、§12（API 修复模式）

---

## 一、总览

| 日期 | 实际 sorry（剥离注释） | 显式 axiom | 状态 |
|:-----|:----------------------:|:----------:|:-----|
| 2026-09-10（修复前统计口径修正前） | 误报 ~41 | 4 | 口径错误，含注释提及 |
| 2026-09-11 上午 | 3 | 4 | 全库 0 error（ec5b4c9） |
| 2026-09-11 中午 | 1 | 4 | PinchTopology ×2 已清零 |
| **2026-09-11（当前）** | **0** | 4 | **全库 sorry 归零**（51f2302 后本轮修复） |

**2026-09-11 下午重大勘误（本轮）**：最后一个 sorry
（`einstein_divergence_free_from_bianchi`）经数值检验**证伪**——
它不是计算瓶颈，而是**恒假命题**（详见 §3.6）。已按勘误流程处置：
假定理删除、登记开放命题 `EinsteinDivergenceFree`（不断言）、
真空真定理 `einstein_divergence_free_vacuum` 替补。

**统计口径（重要）**：匹配 `\bsorry\b` 前必须先剥离 Lean 注释
（`/- -/` 可嵌套 + `--` 行注释）。原始 grep 的 ~41 处中 38 处为注释里的
缺口登记/历史记录。构建期 "declaration uses sorry" 警告可能来自
对含 sorry 模块的**下游依赖**，不代表该文件直接使用。

---

## 二、已闭合项详录（2026-09-11）

### 2.1 `kleinBottle_self_intersection`（PinchTopology.lean）— 真命题，已闭合

- **原状**：`step^[2] s0 ≠ s0` 以 sorry 占位，注释称 "decide 无法处理 iterate 求值"。
- **实际**：`step^[2] s0` 归约为 `KleinState.s2`，与 `s0` 是不同构造子，
  `intro h; cases h`（依靠 no-confusion）即闭合。
- **教训**：4 态归纳类型上，decide 受限时优先 `cases` 反证，比 decide 可靠。

### 2.2 `kleinBottle_has_pinch`（PinchTopology.lean）— **原陈述恒假**，已勘误重建

- **原陈述**：`∃ x y, x ≠ y ∧ step^[2] x = step^[2] y`，见证 s0/s2。
- **证伪**：`kleinStep` 是 4-循环，**任意次迭代都是双射**，
  `step^[2] s0 = s2`、`step^[2] s2 = s0`，而 `s2 ≠ s0` —— 命题恒假，
  旧注释 "rfl 无法处理 iterate 求值" 系误诊。
- **物理根源**：克莱因瓶自交是**几何**现象（两个离散层位于同一几何点），
  不是动力学碰撞（step 非单射）。4-循环模型中 step 永不非单射，
  "step 迭代相等" 无法刻画自交。
- **勘误方案**：新增几何投影（商映射）
  `kleinGeometricPoint : KleinState → Fin 2`（s0/s2→0，s1/s3→1），
  捏点/自交改述为 `∃ x y, x ≠ y ∧ kleinGeometricPoint x = kleinGeometricPoint y`，
  见证 s0/s2，一行 `rfl` 闭合。
- **下游同步**：`kleinBottle_3d_embedding_self_intersection` 同步改述
  （它是 kleinBottle_has_pinch 的直接引用，无其他依赖方）。
- **保留不变**：`hasPinchPoint`（step 非单射定义）本身不动——它用于
  连通和 `connectedSumRecObj` 等真正非单射的模型，那些定理独立成立。

---

## 三、剩余 1 项：Einstein 散度自由（SpectralMetric.lean:732）

### 3.1 目标

```lean
theorem einstein_divergence_free_from_bianchi (Γ : ChristoffelSymbol)
    (g : MetricTensor) (n : Fin 4) :
    einsteinDivergenceSum4 g (ricciFromChristoffel Γ)
      (scalarCurvature g (ricciFromChristoffel Γ)) n = 0
```

即 `Σ_m G_mn = 0`（G = Ric − ½Rg），是 Einstein 场方程自洽性的核心：
能动量守恒的先决条件。

### 3.2 已有基础设施（全部已闭合）

| 组件 | 状态 |
|:-----|:-----|
| `sum4` 显式 4 项和 + `sum4_eq_finset_sum` 桥接 | ✅ |
| `firstBianchiExplicit`（第一 Bianchi） | ✅ |
| `second_bianchi_discrete`（第二 Bianchi 离散形式，~48 个三次单项式，`simp only [tf]; ring_nf` 闭合） | ✅ |
| `einsteinDivergence_eq`（sum4 ↔ Finset.sum 桥接） | ✅ |
| `ricciFromChristoffel` / `scalarCurvature` / `einsteinTensor` 定义链 | ✅ |

### 3.3 瓶颈定位

`scalarCurvature` 展开为 `Σ_m Ric_mm` 后，Einstein 张量的
`g_mn × R` 项在 `n` 固定、m 遍历 4 值时展开为 **4 × 64 = 256 个单项式**，
`ring`/`ring_nf` 在该规模下无法在合理时间完成（kernel 归约爆炸）。

### 3.4 闭合路径（按推荐排序）

**路径 A（推荐）：trace-reversed 分而治之**
数学恒等式 `∇^μ G_μν = ∇^μ R_μν − ½ ∇_ν R`。分两个引理：

1. `lemma ricci_divergence_eq_half_scalar_gradient`：
   `Σ_m ∇R_mn = ½ ∇_n R`（第二 Bianchi 缩并的离散形式）。
   在离散骨架（无偏导数项）下即为 `sum4` 层面的恒等式，
   单项式规模 ~48–128，`simp only [discreteSecondBianchi, tf]; ring_nf` 模式
   已验证可行（同 `second_bianchi_discrete`）。
2. `lemma einstein_div_split`：
   用 `einsteinTensor` 定义拆分 `Σ_m G_mn = Σ_m Ric_mn − ½ Σ_m g_mn R`，
   代入引理 1 后 `Σ_m g_mn R = R`（度规归一，`fin_cases n` 后逐项验证），
   剩余 `½ R − ½ R = 0`。
单引理规模均 ≤128 单项式，绕开 256 项整攻。

**路径 B：对 m 分指标攻击**
`fin_cases n` 后 `fin_cases` 每个 m 的求和索引，把 256 项拆成 4 组 64 项
分别 `ring`。组内仍偏大，必要时再按 Γ 指标对拆分。机械但可靠。

**路径 C：线性组合策略**
`linear_combination`（Mathlib.Tactic.LinearCombination）以
`second_bianchi_discrete` 的实例为系数基底构造证明。
适合路径 A 的两引理形式。

**路径 D：升级计算引擎**
引入 `polyrith`（Sage 后端，需网络）或把骨架迁移到 `MvPolynomial` 商环
做可判定等式检查。工程量大，仅当 A–C 均失败时考虑。

### 3.6 最终处置（2026-09-11 下午）：证伪与勘误

**路径 A–C 全部失效——目标陈述被数值证伪，非计算瓶颈。**

数值检验（每类 ≥6 组独立随机样本）：

| 候选恒等式 | 残差 | 结论 |
|:-----------|:-----|:-----|
| 原式 `Σ_m G_mn = 0`（随机无挠 Γ + 对称 g） | 10⁰–10² | **恒假** |
| 协变散度版 `Σ_m ∇̃_m G_mn = 0`（联络项保留） | 同量级 | **恒假** |
| `Σ_m ∇̃_m Ric_mn = 0`（收缩 Bianchi 骨架版） | 同量级 | **恒假** |
| Einstein 散度 = 第二 Bianchi 缩并 | 不成立 | Bianchi 逐点为零 ⟹ 缩并恒零，而散度非零 |

**根源**（数学诊断）：连续理论中 ∇^μ G_μν = 0 的证明必须**同时使用**
∂ 项与 Γ 项（经度量相容性提升指标后联合抵消）；点值代数骨架丢弃全部
∂ 项后，守恒律的载体不复存在。且原式的普通指标求和**不是协变表述**
（坐标依赖），即使补上度量相容性也无法挽救。

**已实施处置**（SpectralMetric.lean）：
1. 删除假定理 `einstein_divergence_free_from_bianchi` 与依赖它的
   `secondBianchiFromDiscrete`（全库仅自引用，无下游破坏）；
2. 新增 `EinsteinDivergenceFree (Γ g) : Prop` 开放命题登记
   （不断言、不 axiomatize——普遍量化假命题与可判定反例并存将导致不一致）；
3. 新增真定理 `einstein_divergence_free_vacuum`（Ric ≡ 0 ⟹ G ≡ 0）；
4. 下游 `energy_momentum_conservation` / `BianchiEinsteinConservation` /
   `vacuumBianchiEinstein` 均为条件式或真空构造，**不受证伪影响**，保持有效。

**真值路径（未来工作，Phase 16B+）**：沿 RecObj step 的有限差分导数
（张量场在递归系统上的逐点差分 ∂̃_ρ T(x) := T(step_ρ x) − T(x)），
重建带 ∂ 项的离散第二 Bianchi，其缩并给出真正的协变守恒律。

**真值路径第一步已闭合（2026-09-11 晚，算子形式）**：
`DiscreteCovariantBianchi.lean`（§26，新模块，5 定理零 sorry，全库 3687 jobs
`lake build` 通过）。关键转折：数值预实验
（`numerical/phase16b_discrete_bianchi.py`）表明**朴素分量式含 ∂̃ 的离散第二
Bianchi 不成立**（残差 ~2–3 × |∂̃Γ·Γ|，离散 Leibniz 修正 ∂̃(AB)=∂̃A·B+A·∂̃B+
∂̃A·∂̃B 不可忽略），但**算子形式无条件精确成立**（与格点规范论同构）：

- `FrameRecObj`（RecObj + 四方向 stepD）+ `GammaField`（逐点无挠 Christoffel 场）；
- 协变差分算子 `covDiffOp D_ρ = S_ρ + A_ρ − 1`（场空间 `VecField F` 自同态，
  `Module.End` 环，乘法 = 复合）；
- **主定理 `discrete_second_bianchi_operator`**：
  Σ_cyc(ρ,μ,ν) [D_ρ, F_{μν}] = 0，其中 F_{μν} = [D_μ, D_ν]——
  Jacobi 恒等式（`end_jacobi_cyclic`），**无任何假设**（无挠/对易/度量相容均不必需）；
- `shiftOp_commute`（step 对易 ⟹ 移位算子交换）；
- `curvature_op_apply` / `curvature_op_apply_comm`：曲率算子分量展开
  = 双移位修正项（对易假设下消失）+ ∂̃_μΓ_ν·V(stepD μ x) − ∂̃_νΓ_μ·V(stepD ν x)
  + [Γ_μ,Γ_ν]·V(x)——与连续曲率逐项对应；修正项 O(a)，连续极限 a→0 消失
  （数值：分量式 |B|/|R| ∝ 1/n²，O(a²) 收敛）。

**剩余里程碑**：~~(a) 算子 F_{μν} 与点值骨架 `riemannExplicit` 的桥接~~
**（a）已闭合（2026-09-11，§26.6）**：`curvature_op_constant_field`
（常 Γ 场 `GammaConstant` + step 对易 ⟹ 曲率算子退化为骨架曲率
`skeletonCurvature` 的逐点乘法）+ `skeleton_second_bianchi`
（骨架层第二 Bianchi 自包含证明，无挠 + ring，与 SpectralMetric
`second_bianchi_discrete` 同构）——算子主定理与点值骨架连接为同一结构的
两个层级。

**(b) 度规缩并——骨架层代数核心已闭合（2026-09-11 深夜，§26.7，零 sorry，
全库 4078 jobs `lake build` 通过）**。数值预实验
（`numerical/phase16b_metric_contraction.py`，新增）三个结论：
① 离散 Christoffel 公式下度量相容残差 A ≡ 0 **逐点精确**（~1e-16，
纯代数恒等式 ginv·g = δ 不经过 ∂̃）；② **负面结果**：场层级 Einstein 协变
散度 E ≠ α·缩并(Bianchi)，E = O(a)（n 倍增 |E|/|G| 减半），是比缩并残差
O(a²) 高一阶的离散化 artifact——场层级不存在恒等式，开放命题
`EinsteinDivergenceFree` 维持开放；③ 常值 + 无挠 + 相容 ⟹ 骨架 Einstein
散度恒零（ω-联络等随机对照全部验证）。据此在 `DiscreteCovariantBianchi.lean`
§26.7 建成骨架层代数核心（局部无标架形态 `skCurv` + `SkeletonMetricCompat`）：

- `skeleton_g_gamma_exchange`：相容的 (gΓ)-交换改写形态（逐点恒等式）；
- `skeleton_curvature_skew`：相容 + g 对称 ⟹ Σ_a g_{ra} R̂^a_{sμν} 对
  (r↔s) 斜称——证明为四碎片 (gΓ)-交换 + 哑元对合配对（G₂=G₃、G₄=G₁），
  全显式 `Finset.mul_sum`/`sum_mul` 实例化（rw 模式变量不可依赖外层
  绑定变量）；
- `skeleton_first_bianchi`：无挠 ⟹ 第一 Bianchi（ring）；
- `skeleton_ricci_symmetric`：相容 + g/ginv 对称 + 逆对 ⟹ Riĉ_{σν} =
  Riĉ_{νσ}——两步：(i) 第一 Bianchi + 末两位反对称 ⟹ 差 = −δ-迹；
  (ii) δ-迹经逆对插入 + 斜称 + ginv 对称对合归零（`Finset.sum_eq_single`
  需显式 `f :=` 实例，且 `if r = r` 对自由变量不可定义归约，须保留
  if-形式经 calc 闭合）。

**(b)+ 续（2026-09-11 下午）——两个新闭合 + 主定理陈述被证伪（真空化）**：

- `sum4_ite_eq'` / `contraction_g_ginv`：δ-求值与 g–ginv 交换序缩并
  （`Finset.sum_eq_single` 显式 f 实例 + calc 闭合 if 形式）；
- **`discrete_christoffel_metric_compatible`（已闭合，一次通过）**：
  ∂̃_ρ g_{μν} = Σ_a(g_{μa}Γ^a_{ρν} + g_{νa}Γ^a_{ρμ}) 纯代数恒等式
  （`christoffelDisc` 定义；g 因子与 ½ 移入 σ-和 → 双和交换 → 缩并 δ →
  δ 求值 → dsym + ring 配对抵消）——数值 Q1 的 Lean 形式化；
- **`skGamma_zero_of_torsionfree_compatible`（澄清性引理，机器证明）**：
  常值骨架层上 **无挠 + 度规相容 ⟹ 联络恒为零**
  （轮换论证 Γ_{abc} = Γ_{acb}[无挠] = −Γ_{bca}[反对称] = −Γ_{bac}[无挠]
  = Γ_{cab}[反对称] = Γ_{cba}[无挠] = −Γ_{abc}[反对称] ⟹ 2Γ = 0，
  `skGamma`/`skGamma_antisymm`/`skGamma_symm23` 三引理 + linarith）。
  **这把"定理 B：无挠 + 相容 ⟹ E_skel = 0"的朴素陈述逼入真空**——前提
  只在零联络成立，恒等式空洞。

**主定理陈述证伪后的数值再刻画（phase16b_metric_contraction.py 补充实验，
2026-09-11）**：① 随机仅相容联络（不含无挠）|E| 非零（4/4 组 1.6e+1–4.4e+1）
——E_skel = 0 不是相容的推论；② ω-联络（数值上 |E|=0 的相容族）**并非全指标
无挠**——T^0_{ij} = Γ^0_{ij} − Γ^0_{ji} = −2ω_ij ≠ 0，它是挠率联络；
③ 在"非零分量恰含一个 0 指标"的 12 维相容子空间内采样：E = 0 ⟺
Gam[i,j,0] 对 (i,j) 反对称（即 D 反对称；C 任意反对称），ω-联络是其特例。

**剩余 (b) 主定理的重新表述（开放，比预想深刻）**：常值骨架层 E_skel = 0
的成立条件不是"无挠 + 相容"（真空），而是允许挠率下的结构性条件（数值显示
为 D-反对称型）。候选方向：(α) 把 E_skel 分解为"无挠部分贡献 + 挠率泛函"
的恒等式（Lean 可证的恒等式定理，ω-联络是其零点——挠率项精确抵消）；
(β) 在 RecObj step 语义下对 ∂̃ 重建协变散度的恒等式版本（真值路径，与
开放命题 EinsteinDivergenceFree 的 O(a) 残差分析衔接）。无论哪个方向，
开放命题 `EinsteinDivergenceFree` 维持开放，`skeleton_einstein_divergence_free`
不再以原陈述追逐（已证真空）。

**方向 (α) 符号结构结论（2026-09-11，sympy 精确 + 数值复核）**：恰单零指标
12 维族内，把 D 分解为反对称 A + 对称 S（ω 部分 + 挠率对称部分）：

- 空间分量恒等式：D₁ ≡ D₂ ≡ D₃ ≡ 0（整族多项式恒零，结构性——族内无
  Γ^i_jk 型分量，散度空间分量失去全部支撑项）；
- 时间分量分解：D₀ = L(C,A)·S + Cub(S)，线性部分 6 项（系数为 (C,A)
  二次型）、三次部分 16 项且**只含 S**、二次部分恒零（无 (C,A)×S² 交叉）；
  Cub(S) 在 det/tr 标准不变量下不分解，几何含义待定；
- **ω 联络（S=0）是 D_ν=0 的全部零点**（族内 3000 随机样本无反例；
  ω 样本 2000 个 max|D|=2.7e-15）；
- 全 48 维相容空间对照：4 分量一般全非零、对联络纯三次、无恒等式零点
  结构——上述刻画**限于恰单零指标族**，paper54 引用须写明该限制。

研究笔记：notes/04 `esk_torsion_decomposition.md`。脚本：
`numerical/phase16b_eskel_{factor,sdecomp,fullspace}.py`、
`numerical/phase16b_div4_family.py`。
Lean 形式化候选：D₁=D₂=D₃≡0 的结构证明（中等工作量）；
D₀ 37 项多项式恒等式成本高，暂不建议。

**(α)-1 已闭合（2026-09-11 晚，§26.8，全库 4078 jobs `lake build` 通过）**：
`DiscreteCovariantBianchi.lean` §26.8 建成骨架 Einstein 散度算子链
（`skRic`/`skScalar`/`skEin`/`skConnG`/`skDiv` + Minkowski 度规 `mink4` +
恰单零指标族显式查表 `singleZeroConn`），主定理
`single_zero_family_spatial_div_zero`：对任意 C D : Fin 4 → Fin 4 → ℝ（无需
任何对称性假设），D_k = Σ_{μ,a} η^{μa}∇̃_μG_{ak}（k=1,2,3）恒为零。
证明：fin_cases + show 数值化（Fin.succ 原始构造型不触发 vecCons 字面量引理，
先 show 为数字字面量）+ sum4 展开 + 矩阵字面量归约（cons_val_zero/one/two/
three + head/tail_cons）——simp 即闭合，ring_nf 不必需。模块现 19 定理零 sorry。

**(α)-2 已闭合（2026-09-12 凌晨，§26.8，全库 4078 jobs `lake build` 通过）**：
ω 联络零点定理 `single_zero_family_time_div_zero_omega`：C、D 均反对称
（D = A 纯 ω 部分，挠率 T^0_{ij} = −2A_{ji}）⟹ 时间分量 D₀ ≡ 0。
证明：反对称实例化为地面重写规则（hC/hD 在 i<j 的 6 对 + 对角 linarith 归零），
展开后 ring 闭合。与 (α)-1 合取：**ω-联络是全散度 D_ν = 0 的零点**（族内）。
前提不可减（符号验证：C 留对称部分时 D₀ 有 6 项残差 ≠ 0），
故 C 反对称是本质条件——族内 ω 零点刻画"无对称部分的恰单零指标联络"。
模块现 20 定理零 sorry。剩余 (α)：D₀ = L(C,A)·S + Cub(S) 的
显式分解形式化（37 项恒等式，建议先 sympy 整理中间引理链）。

**既有基础索引（2026-09-11 全库查证，接手人不必重查 90+ 篇）**：

| 层级 | 文档 | 与本路径的关系 |
|:-----|:-----|:---------------|
| 骨架（已机器证明） | paper54 §7（`connectionAction` / `second_bianchi_discrete` / `SecondBianchiIdentity` / `energy_momentum_conservation`）+ notes/04 `phase69_spectral_metric_origin` §3.3 | 不带 ∂ 项的离散第二 Bianchi 骨架已建成；paper54 §7.1"缩并得到 ∇^μ G_μν = 0"的断言即本 §3.6 证伪对象，paper54 已同步修订 |
| 离散微分技术先例（已机器证明） | paper44 曲率层（结构方程 Ω=dω+ω∧ω、Bianchi dΩ+[ω,Ω]=0、挠率反对称，Lean 零 sorry + 14/14 数值） | 库里唯一"离散外微分 + Bianchi"机器证明先例；sum4 显式求和技术可直接迁移 |
| 谱侧目标陈述（表述层） | paper16 主定理 22；notes/04 `spectral_lorentz_curved_spacetime` 命题 3.3 / 定理 C | 谱形式 Bianchi ⟺ 能动量守恒的目标陈述 |
| 离散导数算子概念近邻 | notes/00 `spec_infinity_prelim` §离散 Laplace/Toeplitz | 离散导数算子的最近邻概念，非 RecObj step 语义 |
| 连续极限（无微分算子） | paper34 + `ContinuumLimit.lean` | 嵌入层连续极限（Hölder/拟弧/谱流保持），不含导数重建 |
| 空白确认（已填补） | 方向化 step 曾全库仅命中本文件（2026-09-11 查证）；paper37 开放问题清单未登记本缺口 | ∂̃_ρ 方向化差分导数已在 `DiscreteCovariantBianchi.lean` 首次实现；paper37 待补登记 |

### 3.7 验证标准（已达成）

- [x] `lake build MUFPFormalization` 全库 0 error（4078 jobs，含 2026-09-11 新增/扩展 DiscreteCovariantBianchi §26.6–26.7）
- [x] 剥离注释后全库 sorry 计数 = 0
- [x] 假定理证伪记录保留（本文件 + Lean 源 docstring 双登记）

---

## 四、显式 axiom 登记（4 项，非 sorry，属 open 问题占位）

| # | 声明 | 文件 | 关闭路径 |
|:-:|:-----|:-----|:---------|
| 1 | `layer2_statistical_spectral_correspondence_open` | EDRNCrossFramework.lean:128 | Layer-2 统计谱对应需无穷维算子谱理论（Phase 16B） |
| 2 | `layer3_silence_discordance_full_equivalence_open` | EDRNCrossFramework.lean:140 | Layer-3 静默-失谐全等价，同上 |
| 3 | `D_partial` | GeneralMetaTheoremFramework.lean:89 | 一般递归系统的部分 D 函子，需极限/稠密性论证 |
| 4 | `D_partial_spec` | GeneralMetaTheoremFramework.lean:92 | D_partial 的规范公理，随 #3 一并关闭 |

**原则**：axiom 保持显式（不伪装成 sorry/theorem），命名带 `_open` 后缀，
关闭时逐条转为定理并删除。

---

## 五、防回归检查清单

- [ ] 新增 sorry 必须在旁注原因 + 在本文件登记 + 更新 ENV_GUIDE §9 计数
- [ ] 统计 sorry 必须用注释剥离口径（§一），禁止原始 grep 直接报数
- [ ] 定理陈述被证伪时（如 §2.2），勘误需保留原陈述与证伪记录
- [ ] 每闭合一项即运行 `lake build MUFPFormalization` 全库验证
