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
three + head/tail_cons）——simp 即闭合，ring_nf 不必需。

**查表勘误（2026-09-12 凌晨，分解定理证伪发现）**：`singleZeroConn` 初版
Γ^i_{j0} 块写成 D_{ji}（转置），正确族为 Γ^i_{j0} = D_{ij}。
(α)-1/(α)-2 的陈述不受影响（前者 D 全称量化、后者 D 反对称，均对转置不变），
但定义已勘误为正确族——由 (α)-3 分解定理的 ring 失败暴露（LHS 多出
2·tr(S)·Σ C_k·A_k 型残差），修正后三个定理全部 kernel 重验通过。

**(α)-2 已闭合（2026-09-12 凌晨，§26.8，全库 4078 jobs `lake build` 通过）**：
ω 联络零点定理 `single_zero_family_time_div_zero_omega`：C、D 均反对称
（D = A 纯 ω 部分，挠率 T^0_{ij} = −2A_{ji}）⟹ 时间分量 D₀ ≡ 0。
证明：反对称实例化为地面重写规则（hC/hD 在 i<j 的 6 对 + 对角 linarith 归零），
展开后 ring 闭合。与 (α)-1 合取：**ω-联络是全散度 D_ν = 0 的零点**（族内）。
前提不可减（符号验证：C 留对称部分时 D₀ 有 6 项残差 ≠ 0），
故 C 反对称是本质条件——族内 ω 零点刻画"无对称部分的恰单零指标联络"。
模块现 20 定理零 sorry。

**(α)-3 已闭合（2026-09-12 凌晨，§26.8，全库 4078 jobs `lake build` 通过）**：
时间分量挠率泛函分解定理 `single_zero_family_time_div_decomp`：C、A 反对称、
S 对称、D = A + S 下，D₀ = L(C,A)·S + Cub(S) 显式成立——L 为 21 项
（系数 (C,A) 二次型，含 A·C 混合），Cub 为 16 项纯 S 三次型，无 S⁰/S² 项。
RHS 由生成器 numerical/phase16b_d0_lean_gen.py 在 12 个标准原子上生成
（sympy 校验 D₀ = lin + cub），Lean 端 hC/hA/hS 实例化重写 + ring 闭合。
此定理同时暴露 singleZeroConn 查表转置勘误（见上）。方向 (α) 至此全部闭合。

**(β)-1 已闭合（2026-09-12，§26.9，全库 4078 jobs `lake build` 通过，模块 24 定理零 sorry）**：
RecObj step 语义下 ∂̃ 协变散度恒等式版本的第一个构件组，含四件：
① `stepDiff F ρ A := fun x => A (F.stepD ρ x) - A x`——∂̃ 沿 RecObj step 的
方向化差分的算子定义（首次在库里落地，补 2026-09-11 查证的空白）；
② Leibniz 修正恒等式 `stepDiff_mul`：∂̃(AB) = ∂̃A·B + A·∂̃B + ∂̃A·∂̃B
（`simp only [stepDiff]; ring` 闭合）——第三项即数值残差 ~2–3×|∂̃Γ·Γ|
量级的**代数源头**：离散差分不满足连续 Leibniz 律，协变导数算子的
"修正结构"由此而生；
③ 分量公式 `covDiffOp_apply`：(D_ρ W) x r 的显式四分量展开
（移位 + 规范作用，sum4 显式求和）；
④ 分量级循环恒等式 `discrete_second_bianchi_components`：
Σ_cyc(ρ,μ,ν) [(D_ρ(F_μν V)) − (F_μν(D_ρ V))] x r = 0，
由算子 Jacobi 恒等式（discrete_second_bianchi_operator）经
LinearMap.ext 逐点实例化，证明用 defeq（算子积/逐点作用/零映射均为
rfl 族），修正项（双移位、∂̃Γ、[Γ_μ,Γ_ν]、Leibniz 修正）在恒等式内
精确抵消。本定理是 skeleton_second_bianchi（∂̃≡0 骨架层）含 ∂̃ 项的
真值载体，连续极限 a → 0 逐型消失。
**(β)-2 已闭合（2026-09-12，§26.10，全库 4078 jobs `lake build` 通过，模块 25 定理零 sorry）**：
算子级 η-度规相容（Leibniz 修正版）`covDiffOp_metric_compatible`：
联络逐点取值于 𝔰𝔬(η)（相容假设 hη——即 §26.7 离散 Christoffel
逐点相容残差恒零条件的算子化，`discrete_christoffel_metric_compatible`
的结论形态）时，任意向量场 V、W 满足
  ∂̃_ρ⟨V, W⟩_η = ⟨D_ρ V, W⟩_η + ⟨V, D_ρ W⟩_η + ⟨∂̃_ρ V, ∂̃_ρ W⟩_η，
其中 ⟨·,·⟩_η 为 η-逐点配对（`etaPair`），D_ρ = covDiffOp，
∂̃_ρ 为纯移位差分。要点：①连续恒等式 ∂⟨V,W⟩ = ⟨∇V,W⟩+⟨V,∇W⟩
的离散精确形态含**第三修正项** ⟨∂̃V,∂̃W⟩——离散 Leibniz 修正
（stepDiff_mul）在场层级配对上的直接投影，光滑场上 O(a²)，即朴素
相容偏离的精确代数形态；②联络项双和 Σ_r Σ_s η_{rs}((ΓV)^r W^s +
V^r (ΓW)^s) 经 hcomp 逐点归零（Finset sum_comm 三重交换 +
mul_sum 提系数 + η 对称进入括号）；③这是把分量级 Bianchi
（discrete_second_bianchi_components）缩并成修正散度恒等式的
**结构件**——Ricci/Einstein 对称性的算子级来源。

**(β)-3 已闭合（2026-09-12，§26.11，全库 4078 jobs `lake build` 通过，
模块 28 定理零 sorry）**：修正张量第二 Bianchi 恒等式
`discrete_second_bianchi_tensor`——Σ_cyc(λ,μ,ν) (∇̃_λ R̂_{μν} −
C_{λμν})^r_s = 0（逐点精确，无任何假设）。推导链：算子恒等式作用于
常值试验场 v̂（`curvature_op_const_apply`：双移位项 v−v 抵消，F v̂ =
R̂·v），v-系数提取（`sum4_coeff_zero` 指示函数法）得张量恒等式。
**修正项 C 的化简形态**（数值调试发现第一版遗漏 R̂ 的 ∂̃Γ 作用项，
合并后精确相消化简）：
C = 双移位差 [Γ_λ(step_ν step_μ x) − Γ_λ(step_μ step_ν x)]
  + Σ_l ∂̃_μ Γ^r_{νl} · ∂̃_μ Γ^l_{λs} − Σ_l ∂̃_ν Γ^r_{μl} · ∂̃_ν Γ^l_{λs}，
三项全为二阶差分结构（光滑场 O(a²)）；退化链与骨架层一致
（StepsCommute 去双移位、GammaConstant 去 ∂̃Γ，两者同时成立退化为
skeleton_second_bianchi）。数值证据 `numerical/phase16b_beta3_debug.py`
（64 组 (λ,μ,ν)，worst |LHS−RHS| = 1.4e-14）。

**(β)-4 第一阶段已闭合（2026-09-12，§26.12，全库 4078 jobs `lake build`
通过，模块 31 定理零 sorry）**：离散 Riemann 散度恒等式
`discrete_riemann_divergence`——对 (β)-3 取 λ = r 裸迹缩并（无度量）：
Σ_r (∇̃_r R̂_{μν})^r_s − ∂̃_μ Riĉ_{sν} + ∂̃_ν Riĉ_{sμ}
= Cc3 − K2 − K3（逐点精确，无任何假设）。连续对应
∇^ρ R_{ρsμν} = ∇_μ Ric_{sν} − ∇_ν Ric_{sμ}；K2/K3 为联络一阶修正
（`contractConn2/3`），Cc3 为 C 的三循环位置裸迹（O(a²)）。
新定义 `ricciTensor`（裸迹 Ricci）。证明要点：循环位置二需逐点反对称
`naiveCurv(x,r,s,ν,r) = −naiveCurv(x,r,s,r,ν)` 归约耦合指标联络项——
ring 不交换求和指标、不提出 (∑)·c 因子，必须手工 `Finset.sum_comm` /
`(Finset.sum_mul _ _ _).symm` 逐步归约（详见
notes/04_lorentz_gravity/riemann_divergence_contraction.md）。数值证据
`numerical/phase16b_beta4_explore.py`（散度恒等式 worst 2.1e-14；
ginv 缩并循环和 −C 修正后 1.8e-15；附带发现场层级 Ricci 不对称
≈0.29·|Ric|——下阶段前置缺口）。

**(β)-4 前置缺口①已闭合（2026-09-12，§26.13，模块 33 定理零 sorry）**：
修正 Ricci 对称性 `modified_ricci_symmetry`——场层级
Riĉ_{σν} − Riĉ_{νσ} = ½ ginv^{ab}(PS_{bσaν} − PS_{bνaσ})，
PS 为 (0,4) 曲率对偶交换残差（lower4/pairSwapRes）。纯 δ-代数
（ginv 对称 + ginv·g=δ，无场方程/联络假设）；骨架层 ∂̃≡0 时
PS≡0 退化为 skeleton_ricci_symmetric。数值 max|A−rhs|=3.3e-15。
详见 notes/04_lorentz_gravity/modified_ricci_symmetry.md。

**(β)-4 第二阶段缺口②已闭合（2026-09-12，§26.14，模块 38 定理零 sorry）**：
ginv 升指标的 Leibniz 修正——①ginv 差分双移位变体
（∂̃ginv = −ginv(step)·∂̃g·ginv(x) 与 −ginv(x)·∂̃g·ginv(step)，逐点精确），
②离散度规相容（∂̃_ρ g_{μν} = g_{μλ}Γ^λ_{ρν} + g_{νλ}Γ^λ_{ρμ}，对离散
Christoffel 公式逐点精确，移位配置唯一），核心工具 `solve_right`
（A·g = B 在互逆对称下的显式解）。数值 max 残差 ≤ 2.1e-14。详见
notes/04_lorentz_gravity/ginv_leibniz_correction.md。

**(β)-4 缺口③第一阶段已闭合（2026-09-12，§26.15，模块 40 定理零 sorry）**：
Einstein 构造层——`scalarCurvature`（R̂ = ginv·Riĉ）、`einsteinTensor`
（G = Riĉ − ½gR̂）、`einstein_trace`（ginv·G = −R̂，4 维 δ-代数，
数值 1.1e-16）、`einstein_asymmetry`（G 不对称 = Riĉ 不对称，PS 承载）。
散度预实验（`numerical/phase16b_beta6_einstein_div.py`）三个结构结论：
①E = ∇̃^μG_{μν} 场层级不恒零且 PS 非主载体（对称化后 |E| 仅降 9%）；
②方向指标化精确分解 E = Σ∂̃H^{(μ)} − Σ∂̃ginv·G(step) + Σginv·connG
（3.6e-15；H^{(μ)} 的 μ 与求导方向绑定）；③E = O(ε) 一阶 artifact。
散度修正的显式闭合（类比 §26.12 的 Cc3−K2−K3 分解）留待下一阶段。
详见 notes/04_lorentz_gravity/einstein_tensor_construction.md。

**(β)-4 最后一步已闭合（2026-09-12，§26.16，模块 42 定理零 sorry）**：
修正的收缩 Bianchi 恒等式——`contracted_riemann_divergence`
（Q − T1 + T2 = Σ ginv·(Cc3−K2−K3)，§26.12 的 ginv 加权求和，无假设）
+ `scalar_curvature_leibniz`（T2 = ∂̃_νR̂ − Σ∂̃ginv·Riĉ(step)，移位积规则）。
数值端到端装配（`numerical/phase16b_beta7_contracted_bianchi.py`，
2.8e-14）：∇̃^μG_{μν} = Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B——
Einstein 散度修正的显式形态确立（无单一主载体，分布式抵消）。
**(β) 全部闭合。**

**新阶段第一轮已闭合（2026-09-12，§26.17，模块 43 定理零 sorry）**：
度规项散度的 δ 缩并——`covDiff02`（(0,2)-张量协变差分，移位混合约定，
与数值链 nabla02 一致）+ `metric_term_divergence`：在
`hctr : Σ_a ginv^{μa}g_{aν} = δ^μ_ν`（**直接走 hctr，无需 g 对称**）下，
`Σ_{μa} ginv^{μa}∇̃_μ(g_{aν}R̂) = ∂̃_νR̂ + Σ_{μa} ginv^{μa}(∂̃g·R̂(step) + 4 项
Γ·g·R̂ 移位修正)`（连续极限 O(a) artifact）。数值（`phase16b_beta8_metric_term.py`，
seed 43）：δ 展开 2.8e-14、相容代换 5.7e-14（∂̃g 用 §26.14
discrete_metric_compatible 代换后 B_ν 成纯 Γ·g·R̂ 七项）、ConnRic 曲率迹
展开 2.1e-14（ConnRic_ν = Σ_{μabr} ginv·Γ·naiveCurv 四重 K 型和，
纯 ricciTensor 定义展开，无 ∇̃/∂̃）。
**剩余（通往 EinsteinDivergenceFree 显式陈述）**：① ConnRic 的 K 型 Lean 化
（目标 §26.18，只含 γ 与 naiveCurv 原语）；② 全链代入后的
EinsteinDivergenceFree 最终显式陈述（纯曲率原语：ginv·Γ·g·R̂、
ginv·Γ·naiveCurv、∂̃R̂；数值装配已 2.8e-14 闭合）。

**新阶段第二轮已闭合（2026-09-12，§26.18，模块 44 定理零 sorry）**：
ConnRic 的 K 型 Lean 化——`conn02`（(0,2)-张量协变差分的联络部分，
covDiff02 = ∂̃ + conn02）+ `connric_curvature_expand`：纯 ricciTensor
定义展开 + 因子入和（unfold sum4; ring 逐 b 闭合），
`Σ_{μa} ginv^{μa}(conn_μRiĉ)_{aν} = Σ_{μabr} ginv^{μa}[Γ^b_{μa}(x)R̂_{rbrν}(step)
+ Γ^b_{μν}(x)R̂_{rar b}(step) − Γ^b_{μa}(step)R̂_{rbrν}(x) − Γ^b_{μν}(step)R̂_{rar b}(x)]`
（四重 K 型和，无 ∇̃/∂̃）。
**剩余仅一步**：EinsteinDivergenceFree 最终显式陈述——把 beta7 的
Q + T2 + ConnRic − ginv·(Cc3−K2−K3) − ½B 全链代入 §26.14–26.18 的
显式形态（contracted_riemann_divergence + scalar_curvature_leibniz +
metric_term_divergence + connric_curvature_expand），得到纯曲率原语
（ginv·Γ·g·R̂、ginv·Γ·naiveCurv、∂̃R̂）的完整修正公式；数值装配已 2.8e-14 闭合。

**新阶段收官已闭合（2026-09-12，§26.19，模块 45 定理零 sorry）——(β) 真值路径全链闭合**：
EinsteinDivergenceFree 的最终显式陈述——`einsteinDiv`（E_ν 定义）+
`einstein_divergence_explicit`：**E_ν = T1_ν + K_ν − ½(∂̃_νR̂ + 修正_ν)**
（纯曲率原语：∂̃Riĉ、ginv·Γ·naiveCurv、∂̃R̂、ginv·∂̃g·R̂、ginv·Γ·g·R̂）。
数值（phase16b_beta9，seed 43）：抵消形态 2.8e-14、全显式形态 3.2e-14。
结构性发现：代入收缩 Bianchi 后 **Q 与 T2 完全抵消**——第二 Bianchi 缩并修正
对 Einstein 散度无净贡献，E 完全由 Ricci 散度载体（T1+K）与度规项修正（½B）承载；
连续极限 O(a) 退化到经典 ∇^μG_{μν} = 0。证明：逐点线性 + covDiff02=∂̃+conn02
逐点 rfl + rw 代入 §26.17/§26.18，一次通过。
**§3.6 (β) 全链闭合。** 真值路径剩余工作仅为论文层面的表述整合（paper54 已同步），
形式化侧无未闭合缺口。

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

- [x] `lake build MUFPFormalization` 全库 0 error（4078 jobs，含 2026-09-11 新增/扩展 DiscreteCovariantBianchi §26.6–26.7 与 2026-09-12 §26.17）
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

---

## 六、NoiseCategory 占位定理真证与开放命题登记（2026-09-12，paper14 内生重建 G5）

**背景**：NoiseCategory.lean 原有 6 个 `: True := trivial` 占位定理（Thm 16.1/16.2/16.3、
17.2/17.3、17.7/17.8、Prop 17.1 等），本次按"真证可证的、删除无载体的、登记开放的"
三分类处置。全库 `lake build MUFPFormalization` 3688 jobs 通过，零 sorry。

### 6.1 本轮真证闭合（6 项，均零 sorry）

| 定理 | 处置 | 说明 |
|:-----|:-----|:-----|
| `sigmaRec_decomposition_unique`（Thm 16.1） | 真证 | 新增 `IsComponentReorder` def；恒等重排即唯一分解 |
| `spectral_sequence_convergence`（Thm 16.2） | 真证（有限原型版） | 新增 `truncateComponents`；有限支撑 ⟹ 有限步精确稳定（截断误差为零，强于 TV 界 C/n）。完整 TV 版见 §6.2 |
| `sigmaD_preserves_inductive_limit`（Thm 16.3） | 真证 | 逐分量最终相等版（`Filter.eventually_atTop` 全称名） |
| `ext_degenerates_to_sel`（Thm 17.2） | 真证 + **定义缺陷修复** | 见 §6.3 |
| `noise_spectral_flow_eq`（Thm 17.7） | 真证（迹导数版） | Tr(A+η·D) 对 η 的导数 = Tr(D)，谱一阶矩有限维约化；本征值投影版见 §6.2 |
| `dissSilent_component_size` | 真证 | 0 号噪声分量状态空间 = Fin S.n（`= rfl`） |

### 6.2 开放命题登记（4 项，占位定理已删除，Lean 内为 docstring/注释登记，不 axiomatize）

| # | 开放命题 | 原占位 | 关闭所需基础设施 |
|:-:|:---------|:-------|:-----------------|
| 1 | Thm 17.3 Ext 收敛率 O(1/√N) | `ext_convergence_rate` | 概率论语义：i.i.d. 局部 Rec 对象族构造 + RecObj 谱范数空间（有限原型不可陈述） |
| 2 | Thm 17.8 逆谱流噪声过滤 dA_ζ/dζ = −ζ·F[A_ζ] | `noise_filtering_flow` | "局域化算子 F"的数学定义 + 谱测度背景（有限原型不可陈述） |
| 3 | Thm 17.7 本征值投影版 dσ/dη = Tr(P_λ·δA_N)/‖∇σ‖ | （迹版已真证，投影版未陈述） | 谱投影 P_λ（自伴算子泛函演算 / 微扰论）。**代数前提已闭合（2026-09-20，§17.5-A2）**：`noiseEigenMultiset`（本征值多重集）+ `noise_spectral_flow_roots_trace`（谱一阶矩 Tr(A)=Σλ 计重数）——把迹导数公式落到本征值层；P_λ 的连续谱选择（La 算子级扰动）仍需谱测度/微扰论 |
| 4 | Thm 16.2 完整 TV 距离界 ‖μ_macro − μ_n‖_TV ≤ C/n | （有限步稳定版已真证） | 截断谱测度基础设施（测度论：macro 态为谱测度，TV 为测度全变差） |

**另登记（1 项，Lean 内为 `def ...Open : Prop` 存在双射、不断言）**：
`SelDissAdjunctionOpen`（Prop 17.1）——Sel ⊣ Diss 伴随的 Hom 集同构
`((sel ⟶ R) ≃ SigmaRecHom N (diss R data))`；关闭需 list-编码 Hom 的显式逆构造。
命名带 `Open` 后缀、类型为 `Prop`（非 `theorem`），与 §四 axiom 登记"保持显式、
关闭时转定理"原则一致。**诚实边界（2026-09-20）**：在当前具体定义下，
`selFunctor` 抽取单一分量（`Nat.find hDom`）而 `dissFunctor` 产出 `contractions i < 1`
的多份 R 拷贝（Σ-余积族），`SigmaRecHom` 的 `List` 结构使两侧势一般不等——该伴随
是**范畴层启发式声明**，非普遍双射；依"不作假断言"纪律不制造伪证明。可闭合的
受限形式是 data 使 Diss 退化为单点拷贝的情形（届时同构退化），但该退化使声明失去
伴随的本意，故暂保留开放登记，注明"非普遍双射、需在受限子类上重构"。完整 TV
距离界、收敛率、逆滤波同理保持开放。

### 6.3 意外收获：extFunctor 定义性缺陷（Thm 17.2 无法证明的根源）

原 `extFunctor` 以 `Finset.range 10` 截断扫描：第 10 个分量以后的非空分量被忽略，
且 `Finset.min'` 与 `Nat.find` 选择规则不同，导致存在 ext ≠ sel 的反例——
**Thm 17.2 原陈述不可证明是定义性 bug，非定理为假**。已改为全 ℕ `Nat.find` 扫描
（+ `Classical.propDecidable` 实例），此后 `ext_degenerates_to_sel` 以 `unfold`+`split`
 trivially 成立。该缺陷若带入 paper14 重建，将以"修正后实现"为准。

### 6.4 本轮验证

- [x] `lake build MUFPFormalization.NoiseCategory` 通过
- [x] `lake build MUFPFormalization` 全库 0 error（3688 jobs）
- [x] 注释剥离后全库 `by sorry` 计数 = 0（WeaveBCS.lean 5 处 "by sorry" 字样均为
      2026-08-04 开放项登记注释，非实际代码）
- [x] 开放命题不 axiomatize（§6.2 四项仅 docstring 登记，一项为 `def ...Open : Prop`）

---

## 七、NoiseEffectiveEpsilon：§3.4 ε_eff 闭式 Lean 化（paper14 内生重建 G5）

**背景**：paper14 §3.4 噪声范畴 $\mathbf{Noise}$ 的谱公理层修正公式
（v1.6 已诚实重定级为【谱公理】推导，非范畴 Δ 内生）——
`ε_eff(ξ) = n_imp·[ℓ_B² + ξ²·θ(ξ²/(2ℓ_B²))]`，`θ(t) = 1 − e^{−t}`；
临界阈值 `ε_c^eff = ε_c^(0)/(1 + ξ/ℓ_B)²`。本模块将 §3.4 的核心定性/定界
判别命题 Lean 化，零 sorry。文件：`src/MUFPFormalization/NoiseEffectiveEpsilon.lean`。

### 7.1 本轮闭合的判别性命题（全部零 sorry）

| 命题 | Lean 定理 | 说明 |
|:-----|:----------|:-----|
| θ(0) = 0 | `theta_zero` | 退化点值 |
| 退化值：ξ=0 ⟹ ε_eff = n_imp·ℓ_B²（＝短程情形点值） | `effEpsilon_zero` | ξ→0 项消失的精确稳定 |
| 远程因子非负：0 ≤ θ(t)（t≥0） | `theta_nonneg` | 远程因子 mpr 方向用 `Real.exp_le_exp.mpr` |
| 远程因子严格上界：θ(t) < 1 | `theta_lt_one` | 不完全湮灭、留阈值 |
| θ 单调不减 | `theta_mono` | exp 单调 + mpr 方向 |
| 远程主导分解：ε_eff = n_imp·ℓ_B² + n_imp·ξ²·θ | `effEpsilon_decompose` | `ring` 闭合 |
| 远程修正项非负（n_imp≥0, ξ²≥0, 0≤θ） | `effEpsilon_remote_correction_nonneg` | `mul_nonneg` 组合 |
| θ 处处连续 | `continuous_theta` | `fun_prop` |
| 退化极限：ξ→0 ⟹ ε_eff→n_imp·ℓ_B² | `effEpsilon_tendsto_zero` | 尤于连续性，`ContinuousAt` |
| 临界阈值 ε_c^eff 对 ξ 单调递减 | `effCriticalEpsilon_antitone` | `AntitoneOn (Set.Ici 0)`，`gcongr` 闭合 |
| 分母单调辅助引理 | `effCriticalEpsilon_denom_mono` | `nlinarith` 非线性 |

### 7.2 编译与 API 要点

- `lake build MUFPFormalization.NoiseEffectiveEpsilon` 通过，零 error、零 warning、零 sorry。
- **`Real.exp_le_exp` 是等价命题 `exp x ≤ exp y ↔ x ≤ y`，非函数**：由
  `-t ≤ 0` 推 `exp(-t) ≤ 1` 必须用 `.mpr`（`theta_nonneg`）；直接 `Real.exp_le_exp hlt`
  报 "Function expected"。
- **`sq_le_sq` 是等价 `a²≤b² ↔ |a|≤|b|`，非正向函数**；分母平方单调
  `(1+x₁/ℓ_B)²≤(1+x₂/ℓ_B)²` 改以 `nlinarith [mul_nonneg _ (sub_nonneg.mpr _)]`
  推导（`0≤a·(b−a)`、`0≤b·(b−a)` 组合 ⟹ `a²≤b²`）。
- `gcongr` 会利用上下文假设自动闭合分母正性与比较子目标，bullet 列表需按实际
  剩余子目标数编写（多写报 "No goals to be solved"）。
- 物理参数域：门限相关命题（退化/上界）不限制 ℓ_B 符号；单调/分母平方命题需
  ℓ_B > 0；n_imp ≥ 0、ξ ≥ 0 由物理约定显式给出。

### 7.3 诚实边界与开放登记

- **无穷远精确渐近 `ε_eff ~ n_imp·ξ² (ξ→∞)` 登记开放**：依赖 `e^{−t}→0`
  与 Fatou 两条无穷远比较引理的再交织，本模块以"上界 + 单调"给出定性/定界判别，
  足以支持"远程施主更强无序"与"ε_c^eff 单调下移"两点结论，但精确渐近未闭合。
- 《roadmap》按纪律不新增 axiom；开放项仅 docstring/注释登记。

### 7.4 本轮验证

- [x] `lake build MUFPFormalization.NoiseEffectiveEpsilon` 编译通过（3048 jobs，零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无 warning（未使用变量已清除、死代码已移除）

---

## 八、GPVortex：涡旋＝谱规范分支 + 拓扑荷守恒（paper14 §4.2，G4 代数核心）

**背景**：paper14 §4.2 命题 4.2（涡旋＝谱规范分支）/推论 4.2（涡旋稳定性 $dn/dt=0$）
的**谱代数根源**。真实涡旋拓扑荷 $n\in\mathbb{Z}$ 的严格 winding-number 定义
（$U_n=e^{in\phi}$）与同伦不变性需连续场论，保持开放；本模块在有限维矩阵代数层
闭合其谱代数内容。文件：`src/MUFPFormalization/GPVortex.lean`。

### 8.1 本轮闭合的判别性命题（全部零 sorry）

| 命题 | Lean 定理 | 说明 |
|:-----|:----------|:-----|
| 谱流幺正规范协变 | `spectralFlow_unitary_conj` | 幺正 $U$ 下规范分支 $(U^\dagger A_0 U,\,U^\dagger A_F U)$ 的谱流 = 原谱流的规范共轭；**规范变换与谱流映射交换**（涡旋规范分支沿谱流保结构）。核心：`Matrix.exp_conj` + 标量穿透 `Matrix.smul_mul`/`mul_smul` + 消去 $U^\dagger U=1$ |
| 规范分支保全部迹幂 | `vortex_trace_gaugeInvariant` | $\mathrm{tr}((U^\dagger A U)^k)=\mathrm{tr}(A^k)$；经 `SpectralInvariant.trace_pow_similar` 实例化 |
| 涡旋荷守恒 | `vortex_charge_conservation` | 规范分支谱流与原谱流每时刻 $t$ 的全迹幂全等（推论 4.2 $dn/dt=0$ 的有限维代数版本） |

### 8.2 编译与 API 要点

- `lake build MUFPFormalization.GPVortex` 通过（3188 jobs），零 error、零 warning、零 sorry。
- `open Matrix` 必须置于 `namespace MUFPF` **之外**，否则触发 ambiguous-namespace 警告。
- 谱流第二指数需先用 `rw [neg_smul]` 将 `(-t)•X` 统一为 `-(t•X)` 才能与 `set E1 := exp (-(t•A_F))` 对齐。
- `rw` 一次重写全部出现：`rw [hU, hU]` 在只有一个 `U*V` 时第二次报 "no occurrence"，应仅 `rw [hU]` 后 `simp`。

### 8.3 诚实边界与开放登记

- 闭合的是**谱代数根源**（规范分支保谱流结构 + 保迹幂/谱）；真实涡旋拓扑荷
  $n\in\mathbb{Z}$ 的严格 winding-number 定义（$U_n=e^{in\phi}$）与同伦不变性
  需连续场论（$S^1\to U(1)$ 度），登记开放，不 axiomatize。
- GP 方程（PDE）本身到谱流方程的翻译、连续性方程输入仍属【谱公理】层
  （GPEmergence/paper14 标注），不在本模块范围。

### 8.4 本轮验证

- [x] `lake build MUFPFormalization.GPVortex` 编译通过（3188 jobs，零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无 warning

## 九、GPFlowTimeDep：谱流的时间依赖守恒律（paper14 G4 时间依赖闭合）

**背景**：GPFlow §3 开放登记第 1 项「时间依赖守恒律 $d/dt\,\mathrm{tr}(A(t)^k)=0$」。
谱流方程 $dA/dt=[A_F,A]$ 的解为 $A(t)=\mathrm{exp}(t\cdot A_F)\cdot A_0\cdot
\mathrm{exp}(-t\cdot A_F)$（`spectralFlow`）。本模块证明**比 $d/dt=0$ 更强的点式
恒等**：$\mathrm{tr}(A(t)^k)=\mathrm{tr}(A_0^k)$ 对所有 $t$ 成立——由此
$t\mapsto\mathrm{tr}(A(t)^k)$ 为常值函数，其导数处处为 $0$。闭合的是守恒律
本身，不证明生成元级时间导数（见 9.3 诚实边界）。文件：
`src/MUFPFormalization/GPFlowTimeDep.lean`。

### 9.1 本轮闭合的判别性命题（全部零 sorry）

| 命题 | Lean 定理 | 说明 |
|:-----|:----------|:-----|
| exp 的右逆性 | `exp_smul_mul_exp_neg_smul` | $\mathrm{exp}(tA)\cdot\mathrm{exp}(-tA)=1$；经 `Matrix.exp_add_of_commute` + `neg_smul` + `add_neg_cancel` + `exp_zero`，避免 `exp_neg`（需 DivisionRing，矩阵非 DivisionRing） |
| exp 的左逆性 | `exp_neg_smul_mul_exp_smul` | $\mathrm{exp}(-tA)\cdot\mathrm{exp}(tA)=1$；同右逆，`Commute.refl` 取负左 |
| **谱流点式保迹幂（核心）** | `trace_pow_invariant_flow` | $\mathrm{tr}(\mathrm{spectralFlow}\,A_0 A_F t^k)=\mathrm{tr}(A_0^k)$ 对所有 $t$；由 §1/§2 得互逆对，实例化 `SpectralInvariant.trace_pow_similar`。经 Newton 恒等式蕴含 $A(t)$ 与 $A_0$ 同谱（保谱逐瞬间） |
| 时间依赖守恒律（微分形式） | `trace_pow_flow_conservation` | `HasDerivAt (fun τ => tr(spectralFlow A₀ A_F τ ^ k)) 0 t`，即 $d/dt\,\mathrm{tr}(A(t)^k)=0$；因该函数恒等于常值 $\mathrm{tr}(A_0^k)$（上一条逐点），借 `hasDerivAt_const` 闭合 |
| **谱沿解曲线逐点恒定（特征多项式层）** | `spectralFlow_charpoly_eq` | $\mathrm{charpoly}(\mathrm{spectralFlow}\,A_0 A_F t)=\mathrm{charpoly}(A_0)$；谱流解本就是 $A_0$ 的相似矩阵（§1/§2 互逆 exp 对），相似保特征多项式（mathlib `Matrix.charpoly_units_conj`，`@[simp]`）直接 `simpa` 闭合——比迹幂守恒更强一层（特征多项式 ⟹ 全部迹幂），见 9.5 |

### 9.2 编译与 API 要点

- `lake build MUFPFormalization.GPFlowTimeDep` 通过（3188 jobs），零 error、零 warning、零 sorry。
- `open Matrix` 置于 `namespace MUFPF` **之外**（同 8.2）。
- 矩阵指数必须用 **`Matrix.exp_add_of_commute`**（显式双实参）而非泛型
  `NormedSpace.exp_add_of_commute`——后者在此 mathlib 触发 smul 元变量歧义
  （`𝔸` 无法统一），前者显式给 `(t•A) (-(t•A))` 化解。
- `(-t)•A` 先 `rw [neg_smul]` 统一为 `-(t•A)` 再应用 `exp_add_of_commute`。
- `HasDerivAt` 的导数值须显式 `(0 : ℂ)`（否则与 ℝ 歧义）；`hasDerivAt_const`
  的 `c`、`x` 均为隐参，须 `(c := …) (x := …)` 显式命名，不能用位置实参。

### 9.3 诚实边界与开放登记

- 闭合的是**守恒律本身**（迹幂在解曲线上逐点恒定 + 其微分形式 = 0）。**生成元级
  时间导数** $dA/dt=[A_F,A]$（谱流方程本身）需 $\mathrm{exp}$ 的导数
  $d/dt\,\mathrm{exp}(tA_F)$——此 mathlib 版本对 `NormedSpace.exp` 缺席
  Fréchet/级数导数引理，矩阵非 `DivisionRing` 亦阻断 `exp_neg` 路径；该缺口属
  基础分析基础设施，登记开放，不 axiomatize。
- **特征值（计重数）逐点恒定**：§5 已证特征多项式沿解曲线逐点不变
  （`spectralFlow_charpoly_eq`）；特征多项式 ⟹ 特征值多重集只需乘法分解引理
  （根多重数基础设施，中等），为开放项；谱间隙保存是该读法直接推论。
- **依赖时间的幺正规范势**（$U=U(t)$ 时变）：$A\mapsto U(t)^\dagger A U(t)$ 的
  协变导数引入规范势 $U^\dagger\dot U$，需依赖时间的幺正群与分析，属远期。

### 9.4 本轮验证

- [x] `lake build MUFPFormalization.GPFlowTimeDep` 编译通过（3188 jobs，零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无 warning

### 9.5 特征多项式层补记（更新）

- §5 将守恒从"全部迹幂"加强到**特征多项式沿解曲线逐点不变**，直接实现
  GPFlow §3 #2 谱不变性的点式版本，无需遍历幂次 $k$。
- 关键构造：`let u : (Matrix (Fin n) (Fin n) ℂ)ˣ := ⟨exp(t·A_F), exp(-t·A_F),
  exp_smul_mul_exp_neg_smul t A_F, exp_neg_smul_mul_exp_smul t A_F⟩`
  把 exp 对打包为矩阵单位元；`spectralFlow` 恰为 `u.val·A₀·u⁻¹`（similar 形式）。
- `simpa [hsim] using Matrix.charpoly_units_conj u A₀` 即闭合——`simpa`
  自动用 `Units.coe_inv` 重写 $u^{-1}$ 的 coercion，避免手写 `(u⁻¹).val` 与
  `(u.val)⁻¹` 的定义等价。
- 开放：特征多项式 ⟹ 特征值多重集（乘法分解/根多重数基础设施，中等）已移入 open。

## 十、BerryChern §2.6：Berry 曲率的规范不变性（paper14 G3 代数核心补全）

**背景**：BerryChern §3 开放登记第 5 项「规范不变性」。用本征矢量 $u$ 表示的
Berry 联络 $A=i\langle u|\nabla u\rangle$ 在 $u\mapsto e^{i\theta}u$ 下不变的
微积分版需微分形式恒等式；本层闭合其**有限维代数内核**——Berry 曲率只依赖
占据带投影 $P$（规范不变对象）而非本征态基选取，具体化为**酉稳定化不变**：
对 $U^\dagger U=1$，$F(UPU^\dagger,UAU^\dagger,UBU^\dagger)=F(P,A,B)$。
文件 `src/MUFPFormalization/BerryChern.lean`（§2.6）。

### 10.1 本轮闭合的判别性命题（全部零 sorry）

| 命题 | Lean 定理 | 说明 |
|:-----|:----------|:-----|
| 酉共轭乘积整理 | `conj_mul_unitary` | $UAU^\dagger\,UBU^\dagger=U(AB)U^\dagger$；`noncomm_ring` 重排 + `rw [hU]` 消 $U^\dagger U$ + `simp [mul_assoc]` |
| 酉共轭迹不变 | `trace_conj_unitary` | $(UXU^\dagger).\mathrm{trace}=X.\mathrm{trace}$；迹循环性 `trace_mul_comm` + $U^\dagger U=1$ |
| **规范不变性（核心）** | `berryCurvature_unitary_conj` | $F(UPU^\dagger,UAU^\dagger,UBU^\dagger)=F(P,A,B)$；`conj_mul_unitary` 化简差核 + `trace_conj_unitary` 剥离酉共轭 |
| 规范无关实值性 | `berryCurvature_unitary_conj_im_eq_zero` | 规范变换后曲率仍实值（可积实值性不被破坏）；`berryCurvature_unitary_conj` + `berryCurvature_im_eq_zero` 一行合成 |

### 10.2 编译与 API 要点

- `lake build MUFPFormalization.BerryChern` 通过（3048 jobs），零 error、零 warning、零 sorry。
- 核心证明链：`hM`（差分核 = $U\cdot P(AB-BA)\cdot U^\dagger$）用两条
  `conj_mul_unitary` 重写内积、`congr 1` + `noncomm_ring` 整理差分，末步
  再 `conj_mul_unitary U P (AB-BA)` 合一；主定理 `calc` 四步即闭合。
- 差分整理 **不用 `mul_sub`**（目标形态是矩阵分配律，`rw [← mul_sub]` 幂方向
  不落位），直接 `congr 1` + `noncomm_ring` 交由矩阵环专家闭合。

### 10.3 诚实边界与开放登记

- 闭合的是**代数内核**：曲率对**酉稳定化**（与参数无关的固定 $U$）不变，确立
  "曲率只依赖占据带投影、与本征态相位选择无关"。**联络层面**——本征矢量表示
  $A=i\langle u|\nabla u\rangle$ 在逐点 $u\mapsto e^{i\theta(\mathbf k)}u$ 下的
  不变性，以及 $F=dA$ 与投影公式的一致，需微分形式恒等式，登记开放。
- 其余开放项不变：第一陈数积分定义（流形积分）、整性 $C\in\mathbb Z$（度理论）、
  TKNN（Kubo/泵浦）、绝热不变性（同伦）、切向分析构造（Kato 微扰），均需连续
  场论/同伦基础设施。

### 10.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（3048 jobs，零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无 warning

---

## 十一、GPFlowTimeDep §6：特征值多重集逐点恒定与行列式守恒（paper14 G4 谱层补全）

**背景**：GPFlowTimeDep §6 开放登记第 1 项「特征值（计重数）逐点恒定」。§5 已证
特征多项式沿解曲线逐点不变（`spectralFlow_charpoly_eq`）；本层用 `Polynomial.roots`
（ℂ 代数闭域，根多重集）把它落位到**谱集本身**：A(t) 与 A₀ 的特征值带重数完全
相同的多重集，并导出行列式（特征值乘积）守恒这一标量不变量。
文件 `src/MUFPFormalization/GPFlowTimeDep.lean`（§6）。

### 11.1 本轮闭合的判别性命题（全部零 sorry）

| 命题 | Lean 定理 | 说明 |
|:-----|:----------|:-----|
| 特征值多重集定义 | `spectrum_mulset` | $A.\mathrm{charpoly}.\mathrm{roots}$；非计算性定义（含 `Polynomial.roots`） |
| **特征值多重集逐点恒定（核心）** | `spectralFlow_roots_eq` | $\mathrm{multiset}(A(t))=\mathrm{multiset}(A_0)$；`unfold` + `congrArg Polynomial.roots (spectralFlow_charpoly_eq…)` 一行闭合 |
| 行列式（特征值乘积）守恒 | `spectralFlow_det_eq` | $\det A(t)=\det A_0$；`Matrix.det_eq_prod_roots_charpoly`（ℂ 代数闭）+ 根多重集恒等 + `congr_arg Multiset.prod` |

### 11.2 编译与 API 要点

- `lake build MUFPFormalization.GPFlowTimeDep` 通过（3460 jobs），零 error、零 sorry；
  自身无 warning（编译链上 `Silence.lean`/`SpectralDynamics.lean` 的 warning 为既有残余）。
- 新增 import：`Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs`（`det_eq_prod_roots_charpoly`）、
  `Mathlib.Algebra.Polynomial.Roots`（`Polynomial.roots`）、
  `Mathlib.Analysis.Complex.Polynomial.Basic`（**提供 `IsAlgClosed ℂ` 实例**——缺此则
  `det_eq_prod_roots_charpoly` 无法合成类型类）。
- 注意点：`congrArg` 是**项**（terminology），在 `by` 中需 `exact congrArg …`，不能当作战术；
  `det_eq_prod_roots_charpoly` 返回 `∀ A [IsAlgClosed K], A.det = A.charpoly.roots.prod`，
  需显式传入矩阵参数 `(Matrix.det_eq_prod_roots_charpoly A)`。

### 11.3 诚实边界与开放登记

- 闭合的是**谱恒定的多重集/标量落点**：特征值计重数逐点恒定 + 行列式守恒。
  注意 `spectralFlow_roots_eq`/`spectralFlow_det_eq` 与 §3 迹幂同一（`trace_pow_invariant_flow`）
  是**同一定义面上的两条等价路**（特征多项式 ⟷ 全部迹幂，Newton 恒等式），
  此处显式落到多重集而不需求 Newton 恒等式分解。
- 仍开放：**生成元级时间导数** $dA/dt=[A_F,A]$（需 exp 导数，mathlib 缺席）、
  依赖时间的幺正规范势（GPFlow §3 #5）、特征多项式 ⟹ 谱投影/谱隙的更细谱结构
  （需谱测度/同伦投影基础设施）。

### 11.4 本轮验证

- [x] `lake build MUFPFormalization.GPFlowTimeDep` 编译通过（3460 jobs，零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 全库 `lake build` 通过（6376 jobs），本模块无新增 warning

---

## 十二、BerryChern §2.7：陈数被积函数的 2-形式结构（paper14 G3 积分定义代数前提）

**背景**：BerryChern §3 开放登记第 1 项「第一陈数积分定义 $C=(1/2\pi)\int_{T^2}F\,d^2k$」
的**代数前提**。环面积分需 MeasureTheory + 流形积分（登记开放），但其**代数刻画**
可在有限维原型内闭合：被积函数必须是切向量 $(\partial_x,\partial_y)$ 上的**实值
反对称双线性 2-形式**（$d^2k=dk_x\wedge dk_y$ 反对称），且只依赖切向量的**带间
分量**。文件 `src/MUFPFormalization/BerryChern.lean`（§2.7）。

### 12.1 本轮闭合的判别性命题（全部零 sorry）

| 命题 | Lean 定理 | 说明 |
|:-----|:----------|:-----|
| 带内算子不贡献曲率迹核 | `trace_comm_commutator_zero` | $[P,X]=0\Rightarrow\mathrm{Tr}(P[X,B])=0$；迹循环性绕环 + $PX=XP$ 换序（9 步 calc） |
| **反对称性（核心）** | `berryCurvature_antisymm` | $F(P,B,A)=-F(P,A,B)$（$F_{xy}=-F_{yx}$）；`noncomm_ring` 证 $[B,A]=-[A,B]$ + 迹/标量线性 |
| 左线性 | `berryCurvature_add_left` | $F(P,A+X,B)=F(P,A,B)+F(P,X,B)$；`noncomm_ring` + `mul_add`/`trace_add` + `ring` |
| 右线性 | `berryCurvature_add_right` | $F(P,A,B+X)=F(P,A,B)+F(P,A,X)$；同左线性 |
| **带内平移不贡献** | `berryCurvature_shift_commute` | $[P,X]=0\Rightarrow F(P,A+X,B)=F(P,A,B)$；左线性拆分 + `trace_comm_commutator_zero` |
| 常数平移特例 | `berryCurvature_shift_const` | $F(P,A+c\cdot 1,B)=F(P,A,B)$；$[P,c\cdot 1]=0$（标量阵与一切矩阵交换） |

### 12.2 编译与 API 要点

- `lake build MUFPFormalization.BerryChern` 通过（3048 jobs），零 error、零 warning、零 sorry；
  全库 `lake build` 通过（6376 jobs）。
- 迹循环链（`trace_comm_commutator_zero`）：`Matrix.trace_mul_comm` 每次绕环一步、
  `← mul_assoc` 重结合，末步需 `rw [Matrix.trace_mul_comm, ← mul_assoc]` 两步
  （单步 `trace_mul_comm` 后留下 `(P·B·X).trace=(P·(B·X)).trace` 需再结合）。
- 交换子反对称：矩阵非交换，`ring` 失败（"no progress"），必须 `noncomm_ring`。

### 12.3 诚实边界与开放登记

- 闭合的是**被积函数的代数结构**：实值（§2）+ 反对称 + 双线性 + 带内平移不贡献
  ——陈数密度"可作 2-形式积分"（$d^2k=dk_x\wedge dk_y$ 反对称）的代数刻画，
  与 §2.5（切向量本身是带间的）互补构成"TKNN 只需带间矩阵元"论断的完整形式。
- 仍开放：**环面积分本身**（MeasureTheory + 流形积分）、$F$ 的连续性（⇐ $P$ 光滑，
  Kato 微扰层）、整性 $C\in\mathbb Z$（度理论）、TKNN（Kubo/泵浦）、绝热不变性
  （同伦）——均需连续场论/同伦/微积分基础设施。

### 12.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（3048 jobs，零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 全库 `lake build` 通过（6376 jobs），本模块无新增 warning

## 十三、BerryChern §2.8：陈数整性与绝热不变性的代数种子（paper14 G3 整性/绝热层）

**背景**：BerryChern §3 开放登记第 2 项「整性定理 $C\in\mathbb{Z}$」与第 4 项
「陈数绝热不变性（paper14 命题 3.1）」。两者在物理上最终归结为**占据带的整值
占据数**：占据带谱投影 $P$ 的迹（占据数）等于其秩（占据带维数/Landau 能级数），
整数；且谱投影沿**相似变换**（谱流/绝热演化的代数形式，$P\mapsto UPU^{-1}$）
保持幂等与秩不变——占据数沿绝热形变守恒。本层闭合这两个**代数种子**。

### 13.1 关闭的开放项

**已闭合**（对应 §3 第 2、4 项的代数种子）：
- **占据数 = 秩 ∈ ℤ**（整性的整数代数根源）——`trace_eq_rank_of_idempotent`
- **谱投影沿相似变换保持幂等 + 秩不变**（绝热不变性的代数根源）——
  `idempotent_conj_inv`/`rank_conj_inv_idempotent`

**维持开放**（需连续场论/同伦基础设施）：完整陈数 $C=(1/2\pi)\int F\,d^2k$ 的
整性（度理论/同伦提升，如 Atiyah-Singer 指标特殊化）与环面绝热演化（谱间隙不
闭合的参数形变的同伦不变性）。

文件 `src/MUFPFormalization/BerryChern.lean`（§2.8）。

### 13.2 交付定理

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:---------|
| **幂等阵迹 = 秩 ∈ ℤ（整性代数种子）** | `trace_eq_rank_of_idempotent` | $P.\mathrm{toLin}'$ 幂等 → `LinearMap.isProj_range_iff_isIdempotentElem`（mpr 方向，`IsIdempotentElem.isProj_range` 别名不存在）→ `IsProj.trace`（幂等线性映射迹 = 值域维数）→ `Matrix.trace_toLin'_eq`/`rank_eq_finrank_range_toLin` 桥接（后者需先 `rw [Matrix.toLin_eq_toLin']` 转 `toLin'`） |
| **共轭保持幂等** | `idempotent_conj_inv` | `noncomm_ring` 重排 + $U^{-1}U$ 消去中间对（只需单边 $U^{-1}U=1$）；calc 末步显式参数 `rw [mul_assoc U P P, hPP]` 先结合内层 $P\cdot P$ |
| **相似变换秩守恒（绝热不变性代数种子）** | `rank_conj_inv_idempotent` | 幂等保持 `idempotent_conj_inv` + 相似迹不变 `SpectralInvariant.trace_pow_similar`（k=1）+ 秩=迹 `trace_eq_rank_of_idempotent`；`exact_mod_cast` 落回 $\mathbb{Z}$ |

更新前 §十（12.2 v1.10 / 此时副本）余下的整性/绝热开放项在此转正为"代数种子
已闭合"，其余开放项（积分定义、TKNN、同伦不变性、切向分析）不变。

### 13.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（3049 jobs，零 error、零 warning）
- [x] `idempotent_conj_inv` 未用参数 $UU^{-1}=1$（hUU）按 linter 移除后零 warning
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 十四、BerryChern §2.9：离散 S¹ 绕行的代数底胞（paper14 G3 同伦层首个基建模块）

**背景**：BerryChern §3 开放登记第 1/2/4 项（环面积分、度理论整性、同伦不变）在
§十三（§2.8）后明确收敛到连续场论/同伦层。开启同伦层前，本层先闭合其**离散 S¹
绕行的代数底胞**——占据带与空带的**互补守恒**：陈数扰动在占据/空带间转移（参数
沿闭回绕行、能带交叉、占据数在带间跳变）时，任何时刻占据数（秩）仍整数且与空秩
相加恒为总带数 $n$。

### 14.1 关闭的开放项

**已闭合**（离散绕行的总荷守恒 + 整值占据数的代数细胞）：
- **补投影幂等**（空带/导带谱投影亦为幂等阵）——`complement_idempotent`
- **占据数 + 空数 = 总带数 $n$**（扰动转移总量守恒的秩论细胞）——
  `rank_add_complement_idempotent`
- **补秩**（空带数 = 总带数 − 占据数）——`complement_rank`

**新增开放项·维持开放**（§3 登记第 7 项）：完整**连续 S¹/环面**绕行的陈数积分、
度理论整性——**同秩投影酉等价**（任意同秩幂等谱投影在有限维中酉等价，→
$K_0(\mathbb{C})\cong\mathbb{Z}$ → 陈指数 → $C\in\mathbb{Z}$）——与同伦不变性，
均需完整酉群 $U(n)$/K₀ 处理，属后续同伦层基建。

文件 `src/MUFPFormalization/BerryChern.lean`（§2.9）。

### 14.2 交付定理

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:---------|
| **补投影幂等**：$P^2=P\Rightarrow(1-P)^2=1-P$ | `complement_idempotent` | `noncomm_ring` 展开 $(1-P)^2=1-P-P+P^2$ 后 `rw [hPP]` 落入 $P^2=P$ |
| **占据数 + 空数 = 总带数 $n$（总荷守恒）** | `rank_add_complement_idempotent` | 补投影幂等 + §2.8 `trace_eq_rank_of_idempotent`（幂等阵迹=秩）+ 矩阵迹线性 $\mathrm{Tr}(P+(1-P))=\mathrm{Tr}\,1=n$；`exact_mod_cast` 落回 $\mathbb{Z}$ |
| **补秩**：$\mathrm{rank}(1-P)=n-\mathrm{rank}\,P$ | `complement_rank` | 加和形式先 `rw [add_comm]` 换序再 `Nat.eq_sub_of_add_eq` 直接推出 |

要点：三条证明**无需子空间直和/秩-零度基础设施**，只复用 §2.8 的
`trace_eq_rank_of_idempotent`（幂等阵迹=秩）+ 矩阵迹的线性平凡
$\mathrm{Tr}(P+(1-P))=\mathrm{Tr}\,1=n$；`complement_rank` 中
`Nat.eq_sub_of_add_eq` 期望 $a+b=c$ 而定理给出 $P.rank+(1-P).rank=n$，须先
`rw [add_comm] at hadd` 交换加项。

### 14.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无子空间直和/秩-零度依赖（仅幂等阵迹=秩 + 矩阵迹线性）

## 十五、BerryChern §2.10：连续 S¹ 环绕数孢子 + 环面陈数积分承载形式（paper14 G3 积分/度理论层首块）

**背景**：§十四（§2.9）闭合离散 S¹ 绕行的代数底胞（总荷守恒/整值占据数）后，
跨入**连续积分/度理论层**。陈数整性 $C\in\mathbb{Z}$ 的物理根源之一是**环绕数取
整值**（恒等映射 $S^1\to S^1$ 的度 = 1）。mathlib 提供 `CircleIntegral`（单参数
环路积分 $\oint_{|z-c|=R}$，核心引理 `circleIntegral.integral_sub_center_inv`：
$(z-w)^{-1}$ 当 $|w-c|<R$ 时积分为 $2\pi i$）与 `TorusIntegral`（多参数环面积分
$\iint_{T^2}$）基础设施，故连续层最小孢子可在真证下闭合。

### 15.1 关闭的开放项

**已闭合**（连续 S¹ 恒等映射的度/环绕数 = 1 ∈ ℤ，积分/度理论层首块）：
- **单位圆留数孢子**：$\oint_{|z|=1} z^{-1}dz = 2\pi i$——`unitCircle_integral_inv`
- **归一化环绕数 = 1 ∈ ℤ**：$(2\pi i)^{-1}\oint z^{-1}dz = 1$——
  `unitCircle_windingNumber_eq_one`
- **环面陈数被积积分形式**（定义留档，§3 登记第 1 项的承载形式）——
  `noncomputable def chernIntegralTorus`

**新增开放项·维持开放**：环面 $T^2$ 上第一陈数 $C=(1/2\pi)\int F\,d^2k$ 的**完整
整性**（同秩投影酉等价 → $K_0(\mathbb{C})\cong\mathbb{Z}$ → 陈指数，§3 登记第 7 项）、
环面上 $F$ 的可积性/光滑性（⇐ $P$ 光滑）与 TKNN 场论形式，均属后续同伦层/度
理论基建。

文件 `src/MUFPFormalization/BerryChern.lean`（§2.10）。

### 15.2 交付定理

| 判别性命题 | Lean 定理/定义 | 证明要点 |
|:-----------|:----------|:---------|
| **单位圆留数孢子**：$\oint_{|z|=1} z^{-1}dz = 2\pi i$ | `unitCircle_integral_inv` | `circleIntegral.integral_sub_center_inv`，中心 0、半径 1，$(z-0)^{-1}=z^{-1}$ |
| **归一化环绕数 = 1 ∈ ℤ** | `unitCircle_windingNumber_eq_one` | 留数孢子 + `inv_mul_cancel₀`；归一化因子 $2\pi i\neq 0$ 由 `mul_ne_zero` 组合 $2,\pi,\mathrm{i}$ 三者非零 |
| **环面陈数被积积分形式**（定义层） | `noncomputable def chernIntegralTorus` | `torusIntegral` 双参数积分，中心 0、半径 1，ℂ² 参数 $\theta\in[0,2\pi]^2$ |

要点：`unitCircle_windingNumber_eq_one` 是陈数整性 $C\in\mathbb{Z}$ 在连续层的
第一块真证基石——度理论整值 $=1$ 的最简实例（恒等映射 $S^1\to S^1$ 的拓扑度），
连接离散 §2.9（总荷守恒）与环面整性。定义层 `chernIntegralTorus` 因 `torusIntegral`
非计算而须标记 `noncomputable`（`clockwise` 无关，系测度积分语义）。

### 15.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 扩展 mathlib 积分基础设施前依赖验证：`CircleIntegral`/`TorusIntegral` 导入可行，无自定义积分基建

## 十六、BerryChern §2.11：同秩投影的 K₀ 迹同态种子（paper14 G3 度理论整性核心的迹特征）

**背景**：§3 #7「同秩投影酉等价（K₀ = ℤ 度理论整性核心）」的完整论证需完整酉群
U(n)/同伦与 K₀ 表示论（等距等价、子空间直和）等大型基建。按项目纪律**只闭合真实
可达内容、不作伪证**，完整酉等价保持开放登记。但 K₀(ℂ)≅ℤ 的**秩定类性质**有一块
完全在现有代数工具内的真实种子：**迹同态**——K₀ 到 ℤ 的显式同构由 $\mathrm{Tr}$
（$K_0(\mathbb{C})\ni[\mathbb{C}^r]\mapsto r\in\mathbb{Z}$）实现，故同秩幂等投影
必然同迹 ∈ ℤ，且补投影亦同秩。

### 16.1 关闭的开放项

**已闭合**（§3 #7 的迹特征/互补类对称种子，"秩唯一决定 K₀ 类"的类一致性）：
- **同秩幂等投影迹类一致**：$\mathrm{rank}\,P=\mathrm{rank}\,Q\Rightarrow\mathrm{Tr}\,P=\mathrm{Tr}\,Q\in\mathbb{Z}$——`trace_eq_of_rank_eq_idempotent`
- **同秩投影互补类对称**：$\mathrm{rank}\,P=\mathrm{rank}\,Q\Rightarrow\mathrm{rank}(1-P)=\mathrm{rank}(1-Q)$——`complement_rank_eq_of_rank_eq`

**新增开放项·维持开放**（§3 #7）：真正的**酉等价构造**（∃ 酉 U，Q=U·P·U†）与
**相似共轭构造**（∃ 可逆 S，Q=S·P·S⁻¹）在连续 S¹/环面上仍登记开放，需完整
等距/酉群/K₀ 基建（mathlib 已具 `IsProj.eq_conj_prodMap`、`LinearEquiv.prodCongr`、
`prodEquivOfIsCompl` 骨架，但矩阵层共轭等式与有限维条件拼装为后续基建方向）。

文件 `src/MUFPFormalization/BerryChern.lean`（§2.11）。

### 16.2 交付定理

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:---------|
| **同秩幂等投影迹类一致**：$\mathrm{rank}\,P=\mathrm{rank}\,Q\Rightarrow\mathrm{Tr}\,P=\mathrm{Tr}\,Q$ | `trace_eq_of_rank_eq_idempotent` | 两边各自 `trace_eq_rank_of_idempotent`（幂等阵迹=秩）+ `congrArg` ℂ/ℕ 转换 |
| **同秩投影互补类对称**：$\mathrm{rank}\,P=\mathrm{rank}\,Q\Rightarrow\mathrm{rank}(1-P)=\mathrm{rank}(1-Q)$ | `complement_rank_eq_of_rank_eq` | 两侧各自 `complement_rank`（补秩 = n − rank）+ `congrArg` 传递 |

要点：两条定理靠 `calc` + `congrArg`（在 ℕ→ℂ 或 n−· 的逐点一致性下替换秩）
一行式闭合，**无需子空间/等距基建**——纯粹复用 §2.8（迹=秩）与 §2.9（补秩）。
迹特征说明占据数只由秩决定（与具体谱投影无关），是 K₀ 秩定类在矩阵层的体现。

### 16.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无子空间/等距依赖（仅复用迹=秩 + 补秩 + congrArg）

## 十七、BerryChern §2.12：一维退化环面环绕数孢子（paper14 G3 环面绕行整值的 $T^1$ 退化面）

**背景**：§3 #1 的环面积分定义层已有 §2.10 的 `chernIntegralTorus`（双参数承载）。
将 §2.10 的单位圆环绕数孢子（$\oint_{|z|=1}z^{-1}dz=2\pi i$ → 整值 1 ∈ ℤ）推广到
环面，mathlib 的 `torusIntegral_dim1` 证得**一维环面积分 = 圆周积分**（单参数环面
与圆周 $C(c_0,R_0)$ 等价），故最真实可达的第一块是**一维退化环面**：环面 $T^2$ 在
$n=1$（单参数）时的切面恰为圆周 $S^1$。

### 17.1 关闭的开放项

**已闭合**（§3 #1 的环面绕行整值孢子——$T^1$ 退化面）：**一维退化环面的环绕数整值**。
- **一维退化环面留数孢子**：$1$-参数环面（中心 0、半径 1）被积 $1/z_0$ = 单位圆留数
  $2\pi i$——`torusIntegral_dim1_winding`
- **一维退化环面归一化环绕数 = 1 ∈ ℤ**——`torusIntegral_dim1_windingNumber_eq_one`

**新增开放项·维持开放**（§3 #1）：二维 $T^2$ 被积 $F$ 的**完整归一化陈数与整性**
仍登记开放，需完整等距/度理论基建与 $F$ 可积性（⇐ $P$ 光滑）。

文件 `src/MUFPFormalization/BerryChern.lean`（§2.12）。

### 17.2 交付定理

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:---------|
| **一维退化环面留数孢子**：$1$-参数环面被积 $1/z_0$ = 单位圆留数 $2\pi i$ | `torusIntegral_dim1_winding` | `torusIntegral_dim1` 一维环面 = 圆周积分 + `unitCircle_integral_inv`（§2.10） |
| **一维退化环面归一化环绕数 = 1 ∈ ℤ** | `torusIntegral_dim1_windingNumber_eq_one` | 退化种子 + `inv_mul_cancel₀`（归一化因子 $2\pi i\neq 0$） |

要点：这是 §2.10 环绕数整值向**环面**转移的第一块真证基石——环面在一维退化
切面（圆周 $S^1$）上恒等映射的度/环绕数仍取整值 1，为二维环面整性陈数提供
一维退化边界条件。

实现过程修复一处叙述层 bug：`∯ z in T(...)` 已绑定 `z`，不得再写内层
`fun z : Fin 1 → ℂ => ...`，否则被积值域退化为函数类型导致
`NormedAddCommGroup ((Fin 1 → ℂ) → ℂ)` 合成失败——改用绑定变量 `(z 0)⁻¹`。

### 17.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0
- [x] 无新基建依赖（仅复用 `torusIntegral_dim1` + §2.10 引理）

## 十八、BerryChern §2.13：二维环面双留数整值孢子（paper14 G3 环面陈数整性的二维连续积分层核心孢子）

**背景**：§2.10 用单位圆环绕数孢子、§2.12 用一维退化环面（$T^1$ 侧）闭合了环绕数
整值向环面的转移。本层把 §2.11/§2.12 的环面绕行整值推进到**真正二维化的
双极点被积** $z_0^{-1}z_1^{-1}$，闭合二维环面 $T^2$ 上二维复面双极点的环形留数
整值 $=(2\pi i)^2$、归一化 $=1\in\mathbb{Z}$——环面陈数整性的**二维连续积分层
核心孢子**。

### 18.1 关闭的开放项

**已闭合**（§3 #1 环面陈数整性收敛到的**二维留数整值孢子**）：
- **二维环面双留数孢子**：$\iint_{T^2}z_0^{-1}z_1^{-1}d^2z=(2\pi i)^2$——
  `torusIntegral_dim2_double_inv`
  （按 `torusIntegral` 定义展开，参数立方 $[0,2\pi]^2$ 的 Jacobi 因子
  $\prod_i e^{\theta_i i}$ 与被积倒数逐点消约成常数 $-1$，立方体积
  `Real.volume_Icc_pi_toReal` 为 $(2\pi)^2$，$\mathrm{i}^2=-1$）
- **二维复面归一化环形留数 = 1 ∈ ℤ**——`torusIntegral_dim2_windingNumber_eq_one`
  （$(2\pi i)^{-2}$ 归一化 $=1$）

**新增开放项·维持开放**（§3 #1）：完整 $T^2$ 上一般被积陈数密度 $F$ 的归一化陈数
整性与 $F$ 的实可积性/光滑性（⇐ $P$ 光滑）仍登记开放，需完整度理论/同伦提升基建。

### 18.2 交付定理

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:---------|
| **二维环面双留数孢子**：$\iint_{T^2}z_0^{-1}z_1^{-1}d^2z=(2\pi i)^2$ | `torusIntegral_dim2_double_inv` | `torusIntegral` 定义展开，参数立方 $[0,2\pi]^2$ Jacobi 因子 $\prod_i e^{\theta_i i}$ 与被积倒数消约成常数 $-1$，立方体积 $(2\pi)^2$、$\mathrm{i}^2=-1$ |
| **二维复面归一化环形留数 = 1 ∈ ℤ** | `torusIntegral_dim2_windingNumber_eq_one` | $(2\pi i)^{-2}$ 归一化 $=1$ |

要点：闭合双极点被积 $z_0^{-1}z_1^{-1}$ 的二维环面留数环值（$=(2\pi i)^2$、
归一化 $=1\in\mathbb{Z}$）；完整 $T^2$ 上一般被积陈数密度的整性仍开放，需完整度
理论/同伦提升基建。

### 18.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 十九、BerryChern §2.14：自伴正交分解与相似共轭构造（paper14 G3 同秩投影酉等价的线性共轭支柱）

**背景**：§2.11 用迹同态种子（`trace_eq_of_rank_eq_idempotent` 同迹 ∈ ℤ）确立了
「秩唯一决定 K₀ 类」的**迹特征**；本层把同秩性提升到**映射的构造性等价**，在有限维复
内积空间 $E$ 中为同秩幂等投影 P、Q 显式构造可逆线性变换 S 使 $S\circ P=Q\circ S$，
并确立自伴幂等投影的正交分解——这是 §3 #7「同秩投影酉等价」（K₀=ℤ 度理论整性的
线性共轭支柱）的可逆层闭合。

### 19.1 关闭的开放项

**已闭合**（§3 #7 的**线性共轭支柱**）：
- **自伴幂等正交分解**：自伴幂等投影满足 $\ker=(\operatorname{range})^\perp$——
  `selfAdjoint_idempotent_ker_eq_orthogonal`
  （由 `IsSymmetric.orthogonal_range` 经 `isSymmetric_iff_isSelfAdjoint` 导出，
  确立「自伴幂等 ⟺ 正交投影」：酉等价 K₀ 稳定化的酉前提）
- **同秩幂等投影相似共轭构造**：$\exists\,S:E\simeq_\mathbb{C}E,\ S\circ P=Q\circ S$——
  `similar_conj_projections_of_eq_finrank`
  （幂等分解 `IsIdempotentElem.isCompl` 拆像/核直和 + `prodEquivOfIsCompl` 空间等价，
  经 finrank 加性 `Module.finrank_prod` 析出核同维 → `LinearEquiv.ofFinrankEq` 分块
  线性等价 → `LinearEquiv.prod` 合成显式 S；辅以对角化引理
  `idempotent_apply_of_mem_range`/`_mem_ker` 验证 S∘P=Q∘S）

**新增开放项·维持开放**（§3 #7）：闭合的是**相似共轭**（可逆线性 S）；**酉（等距）
强化**——将 S 升级为保内积的 `LinearIsometryEquiv`（$Q=U\cdot P\cdot U^\dagger$，
$U^\dagger=U^{-1}$）——需「同维子空间间等距等价（`toLinearIsometryEquiv`/紧致自伴
对角化）+ 正交直和合成（`orthogonalDecomposition` 产品等距）」等距基建，登记开放。
环面上完整第一陈数整性另需连续场论/度理论（同伦提升）基建。

### 19.2 交付定理

| 判别性命题 | Lean 定理 | 证明要点 |
|:-----------|:----------|:---------|
| **自伴幂等 ⟺ 正交投影**：$\ker=(\operatorname{range})^\perp$ | `selfAdjoint_idempotent_ker_eq_orthogonal` | `isSymmetric_iff_isSelfAdjoint` 转对称性 + `IsSymmetric.orthogonal_range` |
| **同秩幂等投影相似**：$\exists\,S,\ S\circ P=Q\circ S$ | `similar_conj_projections_of_eq_finrank` | `IsIdempotentElem.isCompl` 像/核直和 → `prodEquivOfIsCompl` 空间等价 → finrank 加性析出核同维 → `ofFinrankEq` 分块等价 → `LinearEquiv.prod` 合成；`idempotent_apply_of_mem_range/ker` 对角化 |

要点：闭合同秩幂等投影的**相似共轭构造**（∃ 可逆 S）与自伴投影的**正交分解**；
真正的**酉等价**（∃ 等距 U，Q=U·P·U†）需完整的同维子空间等距等价 + 正交直和合成
基建，登记开放，未以 sorry 掩盖。

### 19.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十、BerryChern §2.14：同秩投影酉（等距）等价（paper14 G3「秩唯一决定酉等价类」的等距/酉支柱）

**背景**：§十九 闭合了相似共轭（∃ 可逆线性 S，$Q=S\cdot P\cdot S^{-1}$），并如实登记
**酉（等距）强化**开放。本轮把 S 升级为**保内积酉** $\exists\,U:E\simeq_{\mathbb C}E$，
$Q\circ U=U\circ P$（即 $Q=U\cdot P\cdot U^{\dagger}$，$U^{\dagger}=U^{-1}$）——闭合
§3 #7「同秩投影酉等价（K₀ = ℤ 度理论整性核心）」在**有限维内积层**的代数 + 等距层。

### 20.1 闭合的开放项

- §3 #7「完整酉等价 $\exists$ 酉 U，Q=U·P·U†」：**有限维内积层闭合**（`same_rank_selfAdjoint_idempotent_unitary_conj`，显式等距/酉构造）。
- §十九 登记的「酉（等距）强化」开放项：**改为已闭合**（由本轮 §二十 闭合）。

### 20.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `exists_isometry_of_eq_finrank`（引理 A） | 同维有限维子空间 $V,W$ 间存在等距等价 $V\simeq_{\mathbb C}W$ | `stdOrthonormalBasis` + `Equiv.cast`（`congrArg Fin h` 指标等价）+ `OrthonormalBasis.equiv` |
| `linearIsometryEquiv_of_submodule`（引理 B） | 子空间等距 $S\to T$ 延伸为全空间等距等价 $E\simeq_{\mathbb C}E$ | `LinearIsometry.extend` + `toLinearIsometryEquiv` |
| `linearIsometryEquiv_of_submodule_apply`（作用） | 延伸等距在 $S$ 上等于 $e$：$U|_{S}=e$ | `LinearIsometry.extend_apply` |
| `linearIsometryEquiv_of_submodule_mem_orthogonal`（引理 C） | 延伸等距保正交补：$U(S^\perp)\subseteq T^\perp$ | 等距保内积 + e 满射拉回 + `Submodule.mem_orthogonal'` |
| `same_rank_selfAdjoint_idempotent_unitary_conj`（主定理） | 同秩自伴幂等（正交投影）P、Q 酉等价：$\exists$ 酉 $U$，$Q\circ U=U\circ P$ | 引理 A/B/C + `selfAdjoint_idempotent_ker_eq_orthogonal`（$\ker=(\operatorname{range})^\perp$），正交直和 $E=\operatorname{range}P\oplus\ker P$ 上逐段验证（P 在 range 恒等、ker 为零，`idempotent_apply_of_mem_range`/`_mem_ker`；Q 同理） |

**实现要点**：主定理用 `prodEquivOfIsCompl` 把空间正交直和系数化，`rcases eP.surjective`
展开任意 $x$，引理 A 给出占据带等距 $e:\operatorname{range}P\simeq\operatorname{range}Q$，引理 B 延伸为全空间
酉 $U$（作用引理定 $U(a)=e a$，引理 C 定 $U(b)\in T^\perp=\ker Q$），逐段验证
$Q\circ U=U\circ P$ 经 `LinearIsometryEquiv.inner_map_map`（等距保内积）与幂等对角化闭合。

**修复的一处编译错误**：相似共轭构造 `similar_conj_projections_of_eq_finrank` 中
`isoR.prod isoK` 的 `.prod` 被 dot-notation 解析为 `LinearMap.prod`（产出线性映射而非
线性等价），合成类型不匹配；改构造 LinearEquiv 复合 `eP.symm.trans ((isoR.prodCongr
isoK).trans eQ)`（乘积用 `LinearEquiv.prodCongr`），`hSa`/`hSb` 用 `change` +
`simp [eP,eQ,LinearEquiv.prodCongr_apply,coe_prodEquivOfIsCompl']` 展开闭合，零 linter 警告。

**诚实边界（随登）**：本轮闭合的是**有限维**内积层的显式酉等价（`LinearIsometryEquiv`）；
完整 $K_0(\mathbb{C})\cong\mathbb{Z}$（生成/自由交换群结构、$U(n)$ 酉群/同伦类与秩一一对应）
与环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升、§3 #4 绝热不变性）仍需完整
连续场论/度理论基建，登记开放，未以 sorry 掩盖。

### 20.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十一、BerryChern §2.15：K₀ 秩映射的直和加性种子（paper14 G3「K₀(ℂ)≅ℤ」加法幺半结构）

**背景**：§二十 闭合了「秩唯一决定酉等价类」（`same_rank_selfAdjoint_idempotent_unitary_conj`），
给出 $K_0(\mathbb{C})\cong\mathbb{Z}$ 秩映射作为**完全不变量的分类半边**。但 K₀ 是**加法幺半/群**：
其加法结构沿直和相加。本轮把秩映射提升到**直和加性**（$\operatorname{rank}(P\oplus Q)
=\operatorname{rank}P+\operatorname{rank}Q$），为 $K_0(\mathbb{C})\cong\mathbb{Z}$ 的**群同态**
提供加法结构种子——这是从「分类半边」迈向「幺半同构」的必要加性署名。

### 21.1 闭合的开放项

- §3 #7 登记的 K₀ 秩映射**直和加性种子**：**已闭合**（§2.15，零 sorry）。注意闭合的是**秩的加法
  属性**（幂等直和仍幂等 + 秩沿直和相加），而非 $K_0(\mathbb{C})\cong\mathbb{Z}$ 的完整幺半同构
  （Grothendieck 群构造/自由交换群，仍开放登记）。

### 21.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `prodSubmoduleLinearEquiv` | 子空间乘积 `Submodule.prod S T`（$E\times F$ 的子空间）线性等价于类型级乘积 `S × T` | `Submodule.mem_prod` 双向判定 + 逐分量线性验证 + `ext <;> rfl` |
| `directSum_idempotent` | 幂等 $P,Q$ 的直和 `P.prodMap Q`（块对角）仍幂等 | `LinearMap.prodMap_mul`（直和乘法 = 分量乘法） |
| `directSum_rank_add` | $\operatorname{rank}(P\oplus Q)=\operatorname{rank}P+\operatorname{rank}Q$ | `LinearMap.range_prodMap`（像 = 分量像之子空间乘积）+ `prodSubmoduleLinearEquiv`（其 `finrank_eq` 收紧）+ `Module.finrank_prod`（类型级乘积维数加性） |

**实现要点**：`directSum_rank_add` 的证明是一个三层 `calc` 链条。第一层 `rw [LinearMap.range_prodMap]`
把直和像识别为分量像的子空间乘积；第二层经 `prodSubmoduleLinearEquiv` 的 `finrank_eq` 把子空间乘积的
`Module.finrank` 转写到类型级乘积（这是收紧点：Submodule.prod 的维度在 mathlib 中不是预结算的
"分量之和"，需此显式线性等价桥接）；第三层 `Module.finrank_prod` 结算类型级乘积的加性。纯代数变量
（`[AddCommGroup E] [Module ℂ E]`）与内积空间变量分 section 隔离，避免作用域冲突。

### 21.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十二、BerryChern §2.16：K₀ 生成/自由交换群结构的基底（paper14 G3「K₀(ℂ)≅ℤ」自由交换群层）

**背景**：§2.14 闭合了「秩 ⇔ 酉类」逐对显式双射（`same_rank_iff_unitary_conj`，
$K_0(\mathbb{C})\to\mathbb{Z},\,[\mathbb{C}^r]\mapsto r$ 在投影层的分类半边），§2.15 闭合了
秩映射的直和加性（`directSum_rank_add`，加法幺半结构种子）。本轮把连接目标落实为
$K_0(\mathbb{C})\cong\mathbb{Z}$ 的**生成/自由交换群结构基底**：自由交换群在**单个生成元**
（占据带类别实例化为 `PUnit`）上同构于 $\mathbb{Z}$——这是「每个整数对应一个占据带维数
（秩）的自由交换群签名」的纯代数实现。

### 22.1 闭合的开放项

- 完整 K₀(ℂ)≅ℤ 的**生成/自由交换群结构基底**（单生成元 ≃ ℤ + 秩签名 lift 泛性质）：**已闭合**
  （§2.16，零 sorry）。注意闭合的是**纯代数自由交换群层**；把同秩酉类的**实际商幺半群**形成
  + **Grothendieck 化**（split-exact 关系商）+ $U(n)$ 酉群/同伦类与秩一一对应，以实现完整
  $K_0(\mathbb{C})\cong\mathbb{Z}$ 的**群结构同构**，仍登记开放（需完整商/群论/同伦基建）。

### 22.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `single_generator_freeAbelian_iso_int` | $\operatorname{FreeAbelianGroup}(\mathrm{PUnit})\cong\mathbb{Z}$（单生成元自由交换群 ≃ ℤ） | mathlib `FreeAbelianGroup.uniqueEquiv`（`FreeAbelianGroup.lift fun _ ↦ 1`，`zsmul penetration` + `induction_on`） |
| `rank_signature_lift` | 任意占据带生成元 ↦ 整数唯一扩展为群同态：`(Fin r → ℤ) → FreeAbelianGroup (Fin r) →+ ℤ` | `FreeAbelianGroup.lift` 泛性质实例化 |
| `rank_signature_single_eq` | 单生成元秩签名取 $1\in\mathbb{Z}$：`(single_generator_freeAbelian_iso_int)(of x) = 1` | `rw` + `rfl`（`uniqueEquiv` 生成元映射定义展开） |
| `single_signature_unique` | 签名唯一性：`(PUnit → ℤ) ≃ (FreeAbelianGroup PUnit →+ ℤ)` | `FreeAbelianGroup.lift` 泛性质 |

**实现要点**：`FreeAbelianGroup.uniqueEquiv T`（`T` 满足 `Unique`）把单生成元自由交换群同构于
$\mathbb{Z}$，正向为 `lift fun _ ↦ 1`（生成元 ↦ 1）、反向为 `n • of default`——单生成元签名取
$1$ 直接由 `uniqueEquiv` 定义展开（`rw [single_generator_freeAbelian_iso_int]; rfl`）闭合。
`rank_signature_lift` 只是 `FreeAbelianGroup.lift` 的 `(Fin r → ℤ)` 实例，体现自由交换群
同态由其生成元上的取值唯一决定。不依赖 Grothendieck 商构造，纯代数、完整推导。

### 22.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十三、BerryChern §2.17：同秩酉类的商幺半群载体（paper14 G3「K₀(ℂ)≅ℤ」商构造基石）

**背景**：§2.14 闭合「秩 ⇔ 酉类」逐对双射，§2.15 闭合直和加性，§2.16 闭合自由交换群基底。
本轮启动完整 K₀ Grothendieck 化的**第一块：商载体构造**——把同秩自伴幂等（正交）投影的
酉等价形式化为 `Setoid`（等价关系三条），构造商类型 `Quotient`，并把秩映射下降为商上的
良定义完全不变量。这是「K₀ 商代数」的**载体存在性**：酉类 = 秩的商对象存在，且秩是其上
良定义分类函数。

### 23.1 闭合的开放项

- 完整 K₀(ℂ)≅ℤ 的**商载体构造**（同秩酉类 Setoid + 商类型 + 秩完全不变量良定义）：**已闭合**
  （§2.17，零 sorry）。注意闭合的是**商载体**（等价关系 + 商的存在）；在商上定义**加法**
  （跨空间直和 $P\oplus Q$ 的商良定性）+ 证明商构成 **AddCommMonoid/Group**（Grothendieck
  化）+ 把商秩映射形成为幺半同构 $\mathrm{Quotient}\cong\mathbb{Z}$，以及 $U(n)$ 酉群/同伦类
  与秩一一对应，仍登记开放（需完整商/同伦基建）。

### 23.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `SelfAdjointIdemProj` | 自伴幂等（正交）投影子类型：`{P : E →ₗ E // IsIdempotentElem P ∧ P.IsSymmetric}` | `IsSymmetric` + `IsIdempotentElem`（§2.14 已用） |
| `ProjUnitaryRel` | 酉等价关系：`∃ U : E ≃ₗᵢ E, Q∘U = U∘P`（Q=U·P·U†） | `Isometry` 共轭定义 |
| `projUnitaryRel_refl` | P ~ P（U = 1） | `simp`（恒等） |
| `projUnitaryRel_symm` | P ~ Q ⟹ Q ~ P（U⁻¹） | `LinearIsometryEquiv.symm_apply_apply` + `apply_symm_apply` |
| `projUnitaryRel_trans` | P~Q ∧ Q~R ⟹ P~R（U₁.trans U₂） | 逐点 `LinearMap.ext_iff` 提取 + `coe_trans` |
| `projUnitarySetoid` | 酉等价是等价关系 ⟹ `Setoid` | `iseqv := ⟨refl, symm, trans⟩` |
| `rank_well_defined_on_quotient` | 同酉类同秩（商完全不变量） | `finrank_eq_of_unitary_conj`（不依赖幂等/自伴/有限维） |
| `quotientRank` | 商类型上秩函数 `Quotient → ℕ` | `Quotient.lift` + 上条良定义 |

**实现要点**：三条等价性是商构造核心。反身取恒等 $U=1$；对称证明 `P (U.symm x) = U.symm (Q x)`，
用 `LinearIsometryEquiv.symm_apply_apply`（`U.symm (U a) = a`）与 `apply_symm_apply`（`U (U.symm x) = x`）
闭环，关键是把共轭等式的逐点形式（`LinearMap.ext_iff.mp hU y`）与 `U.symm` 的消约精确拼接；传递取
`U₁.trans U₂`（mathlib 顺序：先 U₁ 再 U₂），逐点提取两段共轭后按分量复合（`coe_trans` 展开）。
`rank_well_defined_on_quotient` 直接复用 §2.14 的 `finrank_eq_of_unitary_conj`（它恰好只需共轭
关系，无需投影幂等/自伴/有限维），`quotientRank` 用 `Quotient.lift` 下降。三个引理都在纯
`[NormedAddCommGroup E][InnerProductSpace ℂ E]` 假设下成立，`quotientRank` 加 `[FiniteDimensional]`。

### 23.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十四、BerryChern §2.18：商秩的单射完全不变量（分类器）+ 可扩性 + 值域界

**背景**：§2.17 闭合商载体（商类型存在 + 秩良定义完全不变量）。本轮把「秩唯一决定酉类」
从**逐对显式双射**（§2.14 `same_rank_iff_unitary_conj`）升级为**函数级完全不变量**：`quotientRank`
在商上**单射**（不同酉类必有不同秩，商上无"同秩异类"），由此合并良定义为**可扩性/等值判定**
（商相等 ⟺ 同秩），并以**值域上界**（秩 ≤ dim E）把酉类集合如实嵌入 $\mathbb{N}_{\le\dim E}$。
这是「酉类=秩」在商层的**完全锁定**，是 Grothendieck 化（K₀(ℂ)≅ℤ）的**分类器落点**。

### 24.1 闭合的开放项

- 在 §2.17 商载体上，把「秩唯一决定酉等价类」的逐对双射提升为**函数级单射完全不变量**：
  **已闭合**（§2.18，零 sorry）。注意闭合的是 **商秩的完全不变量强化**（单射 + 可扩性 + 值域界）；
  在商上**定义加法**（跨空间直和 $P\oplus Q$ 的商良定性）+ 证明商构成 **AddCommMonoid/Group**
  （Grothendieck 化的群结构层）+ $U(n)$ 酉群/同伦类与秩一一对应，仍登记开放。

### 24.2 交付定理

| 定理 | 主张 | 基建 |
|------|------|------|
| `quotientRank_injective` | `quotientRank E : Quotient (projUnitarySetoid E) → ℕ` 单射——不同酉类必有不同秩 | `same_rank_iff_unitary_conj` 前向（同秩⟹酉等价）+ `Quotient.sound` |
| `quotientRank_ext` | 同秩 ⟺ 商相等（可扩性：良定义 + 单射合并） | `quotientRank_injective` 反向 + 良定义前向 |
| `quotientRank_le_dim` | `quotientRank ≤ dim E`（值域上界） | `Submodule.finrank_le` |

**实现要点**：单射性对任意 `⟨P⟩ ⟨Q⟩`，同秩 `h` 经 §2.14 前向得 `ProjUnitaryRel P Q`，再经
`Quotient.sound` 落入商相等——商对象的注入性完全由「秩 ⟹ 酉等价」承载；可扩性把良定义与单射
合并为双蕴含；有界性 `simp [quotientRank]` 后 `Submodule.finrank_le (LinearMap.range P.1)`。
三个定理均在 `[FiniteDimensional ℂ E]` 假设下。

### 24.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十五、BerryChern §2.19：商加法的载体——跨空间直和 P⊕Q 的商良定性

**背景**：§2.18 把商秩锁定为单射完全不变量（分类器）。本轮落实商加法的**对象层载体与商线性**：
在商上定义加法 $[P]\oplus[Q]:=[P\oplus Q]$ 与其**商良定性**（$P\sim P'∧Q\sim Q'⟹P\oplus Q\sim
P'\oplus Q'$）。对象载体取两空间 $E,F$ 的 **L²-乘积** `WithLp 2 (E × F)`——因 mathlib 对原始
二元乘积 $E\times F$ 不自动捆绑内积，需显式转移到注册了 `InnerProductSpace` 的 L²-乘积类型。
在 $E\times F$ 上定义块对角投影 $P\oplus Q:=P.\mathrm{prodMap}\,Q$（§2.15），经 `toL2`/`fromL2`
提升到 L²-乘积得自伴幂等（正交）投影 `projDirectSum`。这是 Grothendieck 化的**商加法对象载体**。

### 25.1 闭合的开放项

- 在 §2.18 商秩分类器基础上，落实**跨空间直和的商良定性**（商加法在对象层良定义）：**已闭合**
  （§2.19，零 sorry）。注意闭合的是**对象层的商线性**（直和幂等/自伴封闭 + 秩加性 +
  `projDirectSum_wellDefined`）；把商构成 **AddCommMonoid/Group**（在商类型上验证加法封闭/结合/
  单位）、完整 **Grothendieck 化**（split-exact 关系商），以及 $U(n)$ 酉群/同伦类与秩一一对应，
  仍登记开放。

### 25.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `toL2`/`fromL2` | 原始乘积 ⟷ L²-乘积 `WithLp 2 (E×F)` 的提升线性等价 | `WithLp.linearEquiv` |
| `projDirectSumMap` | 块对角投影 $P\oplus Q$（L²-乘积上） | `toL2.comp ((P.prodMap Q).comp fromL2)` |
| `projDirectSumMap_idempotent/symmetric` | 幂等、自伴 $P,Q$ 的直和仍幂等、自伴（落 `SelfAdjointIdemProj`） | `prodMap` 分量 + 共轭保内积 |
| `projDirectSum` | 跨空间直和的 `SelfAdjointIdemProj` 包装（商加法对象构造） | 上两条 + `SelfAdjointIdemProj` |
| `projDirectSumMap_rank_add` | `rank(P⊕Q) = rankP + rankQ` | `toL2.submoduleMap` 保 finrank + §2.15 `directSum_rank_add` |
| `quotientRank_projDirectSum_add` | 商秩直和加性：$[\mathbb{C}^r]\oplus[\mathbb{C}^s]\mapsto r+s$ | 上条 + `quotientRank` 展开 |
| `projDirectSum_wellDefined` | $P\sim P'∧Q\sim Q'⟹(P\oplus Q)\sim(P'\oplus Q')$（商线性） | §2.14 `same_rank_iff_unitary_conj` + 秩加性 |

**实现要点**：块对角投影经 `LinearMap.prodMap` 定义在原始乘积上，再由 `toL2`/`fromL2` 线性等价
共轭提升到 L²-乘积（因原始乘积无内积）。幂等/自伴在 `fromL2` 下逐分量验证（`WithLp.prod_inner_apply`
L²-内积分量相加 `inner_toL2`）。秩加性先证像集的 `toL2`-映射等式（`hrange`），再用
`toL2.submoduleMap` 的 `finrank_eq`（线性等价保 finrank）归约到 §2.15 `directSum_rank_add`。
`projDirectSum_wellDefined` 免构造乘积等距：分量同秩（`rank_well_defined_on_quotient`）⟹ 直和
同秩（`projDirectSumMap_rank_add`）⟹ §2.14 酉等价（`same_rank_iff_unitary_conj`）。子类型展开
用显式 `change`（`(projDirectSum P Q).1` ↔ `projDirectSumMap P.1 Q.1`）规避 `rw` 在 `implicit`
透明层下的 coercion 匹配失败。

### 25.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build`（6376 jobs）零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十六、BerryChern §2.20：K₀ 的 Grothendieck 群完成——ℕ 的 split-exact 完成 ≅ ℤ（把商构成群）

**背景**：§2.19 闭合商加法的对象层载体（跨空间直和 $P\oplus Q$ 的商良定性）后，落实完整
Grothendieck 化：把加性幺半群 ℕ 的 **split-exact 完成**形式化为差对等价，所得商**构成可加交换群**
且 ≅ ℤ。商秩分类器 `quotientRank` 把投影商类映到 ℕ 的差对，故 ℕ 的 Grothendieck 完成是
K₀(ℂ)≅ℤ 在**群层**的最简模型：`GrothQuot ≃+ ℤ`。§二十五（§2.19）诚实边界中「把商构成
AddCommGroup + Grothendieck 化（split-exact 关系商）」自此闭合。

### 26.1 闭合的开放项

- 在 §2.19 商加法对象载体基础上，落实**把商构成 AddCommGroup + 完整 Grothendieck 化**（split-exact
  关系商）：**已闭合**（§2.20，零 sorry）。注意闭合的是**秩层 ℕ 的 Grothendieck 群完成**
  （`GrothQuot` 构成 `AddCommGroup`、`grothToIntIso : GrothQuot ≃+ ℤ`）与投影层 Grothendieck 关系
  在秩层的判据（`projGrothRel_iff`）；把**投影商类本身**（自伴幂等投影的酉类商，§2.17/§2.19）作为
  Grothendieck 群的对象层完整 K₀ 结构（商加法沿商类型构成幺半群/群、投影类的 Grothendieck 群
  ≅ ℤ）、$U(n)$ 酉群/同伦类与秩一一对应（把逐对双射提升到群结构层，§3 #7 的商/群/同伦基建）仍
  登记开放。

### 26.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `GrothRel`/`grothRel_refl`/`_symm`/`_trans` | ℕ×ℕ 差对等价 $(a,b)\sim(c,d)\iff a+d=b+c$（反身+对称+传递） | `omega` |
| `grothSetoid` | `Setoid (ℕ×ℕ)`（商类型合法存在） | 上三条 |
| `GrothQuot` | 商类型（ℕ 的群完成载体） | `Quotient grothSetoid` |
| `grothToInt` | 秩差同态 $[(a,b)]\mapsto a-b$（商上良定义） | `Quotient.lift` + `omega` |
| `grothToInt_injective`/`_surjective` | 单射+满射 | `Quotient.sound` + `ring`/`Int.toNat_of_nonneg` |
| `grothToIntEquiv` | 双射 `GrothQuot ≃ ℤ` | `Equiv.ofBijective` |
| `grothQuotAddCommGroup` | 商构成 `AddCommGroup` | `Function.Injective.addCommGroup`（从 ℤ 传送） |
| `grothIntHom` | 群同态 `GrothQuot →+ ℤ` | `grothToInt` + 传送运算 |
| `grothToIntIso` | 群同构 `GrothQuot ≃+ ℤ`（K₀(ℂ)≅ℤ 群层） | `AddEquiv.ofBijective` |
| `grothToInt_add`/`grothAdd_mk_eq` | 加法保持 / 逐分量共合 $[a]+[c]=[a_1+c_1,a_2+c_2]$ | `grothToInt_injective` + `grothToIntIso.map_add` |
| `grothNeg_mk_eq`/`grothZero_eq` | 负数良定 $-[a,b]=[b,a]$ / 零良定 $0=[0,0]$ | `grothToInt_injective` + `map_neg`/`map_zero` |
| `grothQuot_to_freeAbelian` | 与 §2.16 会师 `GrothQuot ≃+ FreeAbelianGroup PUnit` | `grothToIntIso.trans single_generator_freeAbelian_iso_int.symm` |
| `projGrothRel` | 投影层 split-exact 差对 $P\oplus Q'\sim_{\text{酉}}P'\oplus Q$ | §2.19 `projDirectSum` + `ProjUnitaryRel` |
| `projGrothRel_iff` | 投影 Groth 关系 ⇔ 秩层加法等式 | §2.14 `same_rank_iff_unitary_conj` + §2.19 `quotientRank_projDirectSum_add` |
| `grothToInt_of_rank_diff` | 商秩差对送到 `grothToInt` = 秩之差 | `grothToInt_mk` |

**实现要点**：群结构不是逐公理手工构造，而是经单射 `grothToInt` 从 ℤ **传送**——`grothQuotAddCommGroup`
用 `Function.Injective.addCommGroup`（借助 `grothToIntEquiv` 的 `Equiv.apply_symm_apply` 桥接加法/
负/减/标量的良定义闭环）。`grothToInt_injective` 用 `Quotient.sound` 反推差对关系，单射处的代数
重排（$a-b=c-d\Rightarrow a+d=b+c$）用显式 `calc` + `ring`（`omega` 无法直接闭 ℤ 减法重排）；
`grothToInt_surjective` 按非负/负分 `by_cases`，`Int.toNat_of_nonneg` 提供 `toNat` 回代。`grothAdd_mk_eq`
等运算法经 `grothToInt_injective`（差同 ⟹ 类同）闭证。`projGrothRel_iff` 显式 `unfold projGrothRel
ProjUnitaryRel` 后经 §2.14 `same_rank_iff_unitary_conj` 转秩等式，再用 §2.19 `quotientRank_projDirectSum_add`
直和秩加性闭合，`change` 处理 `projDirectSum` 生成的 `WithLp 2 (E×E)` 商载体。

### 26.3 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十七、BerryChern §2.21：对象层 K₀——投影差对象商 + 秩差完全不变量（投影商类作为完整 K₀ 结构）

**背景**：§2.17–§2.20 完成从投影酉类商（`Quotient (projUnitarySetoid E)`）、商秩单射不变量
（`quotientRank`）、跨空间直和（`projDirectSum` + 秩加性）、秩层 Grothendieck 化（`GrothQuot ≃+ ℤ`）
到投影层差对关系（`projGrothRel_iff` ⇔秩层加法等式）的完整链条。§二十六（§2.20）诚实边界中把
「把**投影商类本身**作为 Grothendieck 群的**对象层完整 K₀ 结构**」留待后续。本层闭合其可证核心：
把投影层差对关系 `projGrothRel` 构造为**商**，并给出**对象层秩差完全不变量** `projToInt`——投影
酉类差对象（非秩层）的第一性分类器。

### 27.1 闭合的开放项

- **投影差对象商 + 秩差不完全变量**：把 §2.20 `projGrothRel`（酉等价差对象关系）构成 Setoid
  （`projGrothSetoid`），商类型 `ProjDiffQuot E` 存在，`projToInt E : ProjDiffQuot E → ℤ` 作为对象层
  秩差完全不变量（良定 + 单射），并经 §2.20 `grothToInt` 因子交接、沿跨空间直和加性。**已闭合**。

### 27.2 交付定理

| 定理/定义 | 主张 | 基建 |
|------|------|------|
| `projGrothRel_refl`/`_symm`/`_trans` | 酉等价差对象关系为等价关系（反身/对称/传递） | 经 §2.20 `projGrothRel_iff` 降秩 + `omega` |
| `projGrothSetoid` | `Setoid (SelfAdjointIdemProj E × SelfAdjointIdemProj E)`（商合法存在） | 上三条 |
| `ProjDiffQuot E` | 对象层差对象商类型（$[P]-[Q]$） | `Quotient (projGrothSetoid E)` |
| `projMk` | 代表元构造 `[(P,Q)]` | `Quotient.mk` |
| `projToInt` | 秩差完全不变量 `[(P,Q)] ↦ rankP - rankQ`（商上良定义） | `Quotient.lift` + `projGrothRel_iff` + `omega` |
| `projToInt_mk` | 代表元计算 | `rfl` |
| `projToInt_eq_grothToInt` | 与秩层 `grothToInt` 因子交接 | §2.20 `grothToInt_of_rank_diff` |
| `projToInt_injective` | 单射完全不变量（不同差对象不同秩差） | `Quotient.sound` + `grothToInt_injective` + `Quotient.exact` |
| `projToInt_projDirectSum_add` | 沿跨空间直和分解（K₀ 群同态种子） | §2.19 `quotientRank_projDirectSum_add` + `omega` |

**实现要点**：`projToInt` 的良定性用 `Quotient.lift`，证明中先 `change projGrothRel a c at h`
（把 Setoid 记号 `a ≈ c` 还原）再 `rw [projGrothRel_iff]` 降秩层，`exact_mod_cast` + `omega` 闭合法性。
`projToInt_injective` 内层先用 `rw [← projToInt_eq_grothToInt, ← projToInt_eq_grothToInt]` 把 `h`
改写为秩层 `grothToInt` 的相等（配 `change` 适配商 mk），再经 `grothToInt_injective` + `Quotient.exact`
得秩层 `GrothRel`，最后 `simpa [GrothRel]` 关合目标。

### 27.3 诚实边界

对象层闭合的是**商载体 + 秩差完全不变量（单射）**——即「对象 = 投影酉类差对象」的分类器层。
诚实区分：① `projToInt` 是**单射**而非双射——固定有限维 $E$ 的秩差被界于 $[-\dim E,\dim E]$，
值域是 $\mathbb{Z}$ 的有界子集（**单射嵌入 $\mathbb{Z}$**）；完整双射/群同构 `ProjDiffQuot ≃+ ℤ`
需把空间维数取遍（跨维度直和闭包），登记开放。② 对象层**商加法构成幺半群/群**的公理未逐公理
构造——固定有限维空间直接定义加法需把同类直和翻回同一商类型（跨空间直和落入更大空间），故诚实
对象层群结构经秩差分类器单射嵌入 $\mathbb{Z}$ 的子结构实现；完整对象层群 $\cong\mathbb{Z}$ 依赖
§2.16 自由交换群与 §2.20 `grothToIntIso` 的跨维度会师（已闭合）。

### 27.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十八、BerryChern §2.22：对象层分类器的精确值域——各秩投影可实现 + 像恰为有界整数区间

承接 §27（§2.21）在固定有限维 $E$ 上把 `projToInt` 做成**单射**秩差完全不变量（值域是 $\mathbb{Z}$
有界子集）。本节把这一"值域"彻底算清：证明**各秩投影 $P_k$ 均可实现**（对每个 $k\le\dim E$），并证得
**$\mathrm{range}\,(\mathrm{projToInt}\,E)=\{r\in\mathbb{Z}\mid -\dim E\le r\le\dim E\}$**，即投射像恰为
有界整数区间。由此正面给出 §27 诚实边界①（单射嵌入 $\mathbb{Z}$ 的有界子结构）的精确刻画，并把
"像非加法子幺半群"做成显式定理（闭会展碍，为跨维度 Grothendieck 化的秩可实现基建）。

### 28.1 闭合的开放项

- §27 诚实边界①（`projToInt` 单射嵌入 $\mathbb{Z}$ 的有界子集）：**改为已闭合**中的**精确值域层**
  ——`projToInt` 的像**恰为** $[-\dim E,\dim E]\cap\mathbb{Z}$，是**到有界区间的双射**（单射由
  §2.21 `projToInt_injective`，满射由本节整数值可达性分正负构造）。
- 各秩投影的可实现性（对象层是否有秩 $k$ 的投影类做代表元）：**闭合**——`projOfRank k` 对任意
  $k\le\dim E$ 给出秩恰为 $k$ 的自伴幂等投影。
- 值域恰为区间（秩之齐备性）：**闭合**——整数值可达性（非负取 $[P_k]-[0]$、负取 $[0]-[P_{(-r)}]$）
  配值域上界（`quotientRank_le_dim`）证双包含。

### 28.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `projOfRank` | 各秩投影可实现（$k\le\dim E$） | `stdOrthonormalBasis` 前 $k$ 基向量张成 $U_k$ 的 `starProjection`（幂等 + 自伴） |
| `projOfRank_rankE` | $\operatorname{finrank}(\mathrm{range}\,P_k)=k$ | `finrank_span_eq_card` + `range_starProjection` |
| `projOfRank_rank` | 商上 `quotientRank` 对 $P_k$ 取恰为 $k$ | `change` 转 `finrank` + 上式 |
| `projZero_rank` | 秩 0 投影（$P_0$）特例 | `projOfRank_rank 0` |
| `projToInt_reaches_nat` | 非负 $k$：$[P_k]-[0]$ 的秩差 $=k$ | `projToInt_mk` + 上式 + `norm_num` |
| `projToInt_reaches_neg` | 负 $-k$：$[0]-[P_k]$ 的秩差 $=-k$ | 同上对称 |
| `projToInt_mem_range_Icc` | 值域上界 $-\dim E\le … \le\dim E$ | 秩界 $[0,\dim E]$ + `exact_mod_cast` + `omega` |
| `projToInt_range_Icc` | 值域恰为区间：$\mathrm{range}=\{r\ |-\dim E\le r\le\dim E\}$ | 双包含：上界 + 整数值可达分正负（`Int.toNat_of_nonneg`） |
| `projToInt_range_not_submonoid` | 像非 $\mathbb{Z}$ 加法子幺半群 | $\dim E\ge1$ 取 $a=b=\alpha$，$2\alpha\notin[-\alpha,\alpha]$ |

**实现要点**：投影构造用 `Submodule.span ℂ` 张成前 $k$ 个标准正交基向量的子空间 $U_k$，其
`starProjection` 用 `Submodule.isSymmetricProjection_starProjection` 立得幂等 + 自伴（满足
`SelfAdjointIdemProj`）；秩恰为 $k$ 由 `OrthonormalBasis.toBasis.linearIndependent` 复合
`Fin.castLE` 得线性无关、`finrank_span_eq_card` 计数、`range_starProjection` 把像还原回 $U_k$。
整数值可达分正负两路：$r\ge0$ 用 `Int.toNat_of_nonneg` 把 $r$ 还原为自然数、取 $[P_r]-[0]$；
$r<0$ 用 $\neg0\le r$ 经 `omega` 得 $0\le-r\le\dim E$、取 $[0]-[P_{(-r)}]$、`neg_neg` 还原符号。
闭会展碍取 $a=b=\dim E$，经 `hdim`（$\dim E\ge1$）得 $2\alpha\notin[-\alpha,\alpha]$ 之界。

### 28.3 诚实边界

本节闭合的是**投影商类作为对象层的秩剪影／分类器层的精确值域**——即证明秩差完全不变量到达的有界
区间**恰为** $[-\dim E,\dim E]$（**单射 + 满射**，`projToInt` 是**到有界区间的双射**）。诚实区分：
① 该双射是**到有界整数区间**的双射，并非**到整个 ℤ** 的双射——`ProjDiffQuot E ≃+ ℤ`（**完整群同构**）
仍需跨维度直和闭包（把 $k\le\dim E$ 取遍所有有限维、沿直和并集）登记开放，本节区间的两个端元正是
闭会展碍的见证（$2\alpha$ 超出单空间可达集）。② **对象层商加法构成幺半群/群**仍未逐公理构造——本节
`projToInt_range_not_submonoid` 显式演示固定单空间的值域**非**加法子幺半群，正是为何闭合必须放在
§2.20 的秩层 Grothendieck 群与跨维度直和（§2.16/§2.20 会师）上。③ $U(n)$ 酉群/同伦类与秩一一对应
（提升到群结构层）仍登记开放。

### 28.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 二十九、BerryChern §2.23：K₀(ℂ)≅ℤ 的跨维度分组/生成基座——秩-1 类生成 + 跨维度满射到 ℤ

承接 §28（§2.22）：`projToInt` 在固定单空间是**到有界区间** $[-\dim E,\dim E]\cap\mathbb{Z}$ 的双射，
且像**非**加法子幺半群（闭会展碍）——完整对象层群必须**跨维度直和闭包**。本节把「维数取遍」
落成显式构造：以 `EuclideanSpace ℂ (Fin n)` 作跨维度标准空间，证**秩-1 类 $[\mathbb{C}^1]$ 生成
整个 Grothendieck 群**、**每个整数都被某维数空间投影类实现**（跨维度满射到 $\mathbb{Z}$）、并给出
对象层分类器与秩的直接等式——为「整体秩是 $\mathbb{Z}$ 双射（跨维度单射 §2.21 + 满射本节 +
加法 §2.19 直和秩加性）」补足生成/分组基建。

### 29.1 闭合的开放项

- §28 诚实边界①（跨维度满射侧）：**闭合**——`crossDim_reaches_any`：对每个整数 $r$，$r\ge0$ 取
  $\mathbb{C}^r$、$r<0$ 取 $\mathbb{C}^{-r}$，都有投影类 `projToInt = r`——解除单空间有界像的维数上界。
- §28 诚实边界②（生成侧）：**闭合**——`grothQuot_generated_by_one`：每个 Grothendieck 类都是
  秩-1 类 $[(1,0)]$ 的 $\mathbb{Z}$ 倍（$k\cdot[\mathbb{C}^1]=[(k,0)]$）——K₀(ℂ)≅ℤ 的**生成元层**真语句。
- 秩-1 类跨维度一致性：**闭合**——`rankOne_class_projToInt`（$[\mathbb{C}^1]\mapsto 1$）+
  `rankOne_class_any_dim`（任何 $\ge1$ 维空间的秩-1 投影类秩差都是 1）。
- 对象层分类器与秩的直接等式：**闭合**——`projClass_int_eq_rank`（$\mathrm{projToInt}\,E\,[P,0]=\operatorname{rank}P$）。

### 29.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `canonicalSpace` | 跨维度标准空间 `EuclideanSpace ℂ (Fin n)` | `abbrev`（`PiLp 2` 承载内积实例） |
| `canonicalSpace_finrank` | $\operatorname{finrank}_{\mathbb{C}}(\mathbb{C}^n)=n$ | `simp [EuclideanSpace]` |
| `rankOne_class_projToInt` | 秩-1 类 $[\mathbb{C}^1]\mapsto 1$ | `projToInt_reaches_nat 1` |
| `rankOne_class_any_dim` | 任何 $\ge1$ 维空间秩-1 类都取 1 | 同上 + `omega` |
| `crossDim_reaches_any` | 跨维度满射：每个整数都被某维数空间投影类实现 | 分正负取 $\mathbb{C}^{\pm r}$ + `Int.toNat_of_nonneg`/`neg_neg` |
| `grothOneClass` | Grothendieck 群秩-1 类代表元 $[(1,0)]$ | `Quotient.mk grothSetoid` |
| `grothToInt_grothOneClass` | 生成元类秩差 = 1 | `grothToInt_mk` + `norm_num` |
| `grothQuot_generated_by_one` | K₀ 由秩-1 类生成（每类是 $[\mathbb{C}^1]$ 的 $\mathbb{Z}$ 倍） | `grothToIntIso.injective` + `map_zsmul` |
| `projClass_int_eq_rank` | 对象层分类器即秩：$\mathrm{projToInt}\,E\,[P,0]=\operatorname{rank}P$ | `projToInt_mk` + `Quotient.lift_mk` + `projOfRank_rank` |

**实现要点**：跨维度标准空间取 `EuclideanSpace ℂ (Fin n)`（mathlib `PiLp 2` 承载内积/有限维实例，
`Fin n → ℂ` 裸函数型不自动带内积实例）；`canonicalSpace_finrank` 由 `simp` 直得。跨维度满射分正负
两路：$r\ge0$ 取 $k=r.\mathrm{toNat}$ 维标准空间上 $[P_k]-[0]$，$r<0$ 取 $k=(-r).\mathrm{toNat}$ 维上
$[0]-[P_k]$，符号还原用 `Int.toNat_of_nonneg` + `neg_neg`。秩-1 生成证明经 `grothToIntIso.injective`
（把 `x = n • grothOneClass` 推到 ℤ 侧）+ `map_zsmul`（同构保 $\mathbb{Z}$ 数乘）+ 生成元像为 1
（`grothToInt_grothOneClass`）+ `simp` 闭合。分类器=秩经 `projToInt_mk` 展开代表元、`quotientRank`
的 `Quotient.lift_mk` 化简、`projOfRank_rank 0` 得零投影秩 0。

### 29.3 诚实边界

本节闭合的是**秩层的跨维度分组/生成基底**——即「整体秩是 $\mathbb{Z}$ 双射」的**满射侧**（跨维度）
与**秩-1 生成**：`projToInt` 跨维度可到达**每个**整数（§2.23 `crossDim_reaches_any`），且 Grothendieck
群由 $[\mathbb{C}^1]$ 生成；配合 §2.21 `projToInt` 单射（跨维度单射侧）与 §2.19 直和秩加性（加法侧），
整体（跨所有有限维空间并集的）秩分类是 ℤ 双射。诚实区分：① **同一商类型的完整对象层 `AddCommGroup`**
——把 `ProjDiffQuot ≃+ ℤ` 做成对象层到整个 $\mathbb{Z}$ 的显式同构，需跨所有有限维空间取直和并集
（载体由 §2.20 `grothToIntIso`/§2.16 `grothQuot_to_freeAbelian` 提供，但对象层直和**封闭**需具体取
并集商类型，未构造）仍登记开放；② $U(n)$ 酉群/同伦类与秩一一对应（逐对双射提升到群结构层）仍开放。

### 29.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十、BerryChern §2.24：对象层 K₀ 群——跨维度直和闭包下的 `ProjClass ≃+ ℤ`（对象层完整群同构）

承接 §29（§2.23）：跨维度满射 + 秩-1 生成已把"维数取遍"落到**分类器层**，但"同一商类型的完整
对象层 `AddCommGroup` 结构"仍登记开放。本节把它在**对象层群结构**上收口：构造跨维度和型等距，
把 §2.19 直和投影搬回规范空间，在跨维度对象层载体上定义**由直和诱导的加法**，按秩作商得对象层
K₀ 类 `ProjClass`，证其构成可加交换群并**群同构于 ℤ**，且**类加法恰由直和实现**。

### 30.1 闭合的开放项

- §29 诚实边界①（同一商类型的完整对象层 `AddCommGroup`）：**闭合**——`ProjClass` 构成 `AddCommGroup`
  （`projClassAddCommGroup`）且 `projClassRankIso : ProjClass ≃+ ℤ`。
- 对象层群加法的**自然性**（由直和实现）：**闭合**——`projClassMk_add`：`[a] + [b] = [a ⊕ b]`。
- 跨维度直和的对象层承载（把 §2.19 `projDirectSum` 落到规范空间）：**闭合**——`canonicalSpaceAddIso` +
  `conjProj` + `projDirectSumCanon` + `projDirectSumCanon_rank` + `projToInt_projDirectSumCanon_add`。

### 30.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `canonicalSpaceAddIso` | 跨维度和型等距 $\mathbb{C}^{n+m} ≃ₗᵢ \mathbb{C}^n\times\mathbb{C}^m$ | `piLpCongrLeft` + `PiLp.sumPiLpEquivProdLpPiLp` |
| `conjProj` | 沿等距共轭投影仍自伴幂等 | 复合消约 + `LinearMap.isSymmetric_linearIsometryEquiv_conj_iff` |
| `conjProj_rank` | 共轭保秩 | `LinearMap.range_comp` + `LinearEquiv.finrank_map_eq` |
| `projDirectSumCanon` | §2.19 直和投影搬回规范空间 | `conjProj (canonicalSpaceAddIso n m).symm (projDirectSum P Q)` |
| `projDirectSumCanon_rank` | 规范直和投影秩 = 共轭保秩 | `conjProj_rank` |
| `projToInt_projDirectSumCanon_add` | 分类器沿规范直和加性 | `quotientRank_projDirectSum_add` |
| `ProjPoint` | 跨维度对象层载体 $\bigsqcup_n \mathrm{ProjDiffQuot}\,\mathbb{C}^n$ | `Σ n : ℕ, ProjDiffQuot (canonicalSpace n)` |
| `projDiffSumCanon` | 对象层差类的跨维度直和（双重商 lift） | `Quotient.lift₂` + `projToInt_injective` |
| `projPointRank_add` | 整体秩分类器沿直和加性 | `projDiffSumCanon_mk` + `projToInt_projDirectSumCanon_add` |
| `ProjClass` | 对象层 K₀ 类（按秩相等作商） | `Quotient projPointSetoid` |
| `projClassRank_injective` | 单射（秩唯一决定类） | `Quotient.sound` |
| `projClassRank_surjective` | 满射（§2.23 `crossDim_reaches_any`） | 构造代表元 |
| `projClassEquiv` | `ProjClass ≃ ℤ` | `Equiv.ofBijective` |
| `projClassAddCommGroup` | 对象层类构成可加交换群 | `Function.Injective.addCommGroup` |
| `projClassRankIso` | **对象层 K₀ ≃+ ℤ** | `AddEquiv.ofBijective` |
| `projClassMk_add` | 类加法即跨维度直和（自然性） | `projClassRank_add` + `projPointRank_add` |

**实现要点**：跨维度和型等距用 `LinearIsometryEquiv.piLpCongrLeft`（`finSumFinEquiv.symm` 指标重排）
复合 `PiLp.sumPiLpEquivProdLpPiLp`（`PiLp` 和型的等距分解，右端 L²-乘积 `WithLp 2`）。共轭投影
`conjProj` 的幂等由 `ext y` + `LinearIsometryEquiv.symm_apply_apply` 消约 + `P.2.1` 幂等闭合，
自伴直接取 `LinearMap.isSymmetric_linearIsometryEquiv_conj_iff` 的 mpr。共轭保秩经
`LinearMap.range_comp` 把像化为 `(range P).map e` + `LinearEquiv.finrank_map_eq`。跨维度差类直和
`projDiffSumCanon` 用 `Quotient.lift₂`，良定性经 `projToInt_injective` + `projToInt_projDirectSumCanon_add`
+ `Quotient.sound`。对象层群结构仿 §2.20：先经 `projClassEquiv` 定义 `Zero`/`Add`/`Neg`/`Sub`/`SMul`
实例，再用 `Function.Injective.addCommGroup`（`change` + `Equiv.apply_symm_apply` + `rfl`）传送。

### 30.3 诚实边界

本节闭合的是**对象层完整群结构 ≅ ℤ**——载体 `ProjPoint`/`ProjClass` + 由直和诱导的加法 + 群公理
（`projClassAddCommGroup`）+ 与 ℤ 的**群同构**（`projClassRankIso`）+ **类加法即直和的自然性**
（`projClassMk_add`）。由此 §2.22/§2.23 登记的「同一商类型的完整对象层 `AddCommGroup`
（`ProjDiffQuot ≃+ ℤ` 跨维度直和闭包）」由开放改为闭合（载体取跨维度 `Σ n, ProjDiffQuot (ℂ^n)` 并商、
加法由直和诱导）。仍登记开放：① $U(n)$ 酉群/同伦类与秩一一对应（把逐对双射提升到群结构层）；
② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）。

### 30.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十一、BerryChern §2.25：酉群作用层——`U(E)` 共轭作用、轨道 = 秩类、轨道空间 ≃ 秩集

承接 §三十（§2.24）：对象层 K₀ 群结构 ≅ ℤ 已收口。本节转向剩余开放项「$U(n)$ 酉群与秩一一对应」，
把 §2.21 的**逐对**酉双射（`same_rank_iff_unitary_conj`）提升到**群结构层**：把酉群在投影上的
共轭作用做成真正的 `MulAction`，证明**轨道 = 秩类**，并给出**轨道空间 ≃ 秩集**。

### 31.1 闭合的开放项

- 「$U(n)$ 酉群与秩一一对应」的**轨道层**：**闭合**——`orbitQuotEquivRankSet`：
  `Quotient (orbitRel) ≃ {k : ℕ // k ≤ dim E}`（轨道数 $=\dim E+1$）。
- 酉群作用的存在性与良定性：**闭合**——`unitaryConjAct : MulAction (unitaryEnd E) (SelfAdjointIdemProj E)`。
- 轨道刻画：**闭合**——`mem_orbit_iff_same_rank` / `orbit_eq_rankClass` / `orbit_eq_iff_same_rank`。

### 31.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `unitaryEnd` | 酉群 `E ≃ₗᵢ[ℂ] E` | `abbrev`（mathlib `Group` 实例） |
| `unitaryEnd_symm_one` / `_symm_mul` | 逆应用：单位恒等 / 乘积反序 | `change` 转 `⁻¹` + `mul_inv_rev` + `simp` |
| `unitaryConjAct` | 共轭作用 `u • P := conjProj u P` 为 `MulAction` | `one_smul`/`mul_smul` 经辅助引理 + `simp [conjProj]` |
| `unitaryConjAct_smul` | 作用律 `u • P = conjProj u P` | `rfl` |
| `unitaryConjAct_rank` | 作用保秩 | §2.24 `conjProj_rank` |
| `unitaryConjAct_rel` | 作用保持酉类 `ProjUnitaryRel P (u • P)` | 显式见证 `u` + `ext` + `simp` |
| `mem_orbit_iff_same_rank` | 轨道 = 秩类（成员判定） | §2.21 `same_rank_iff_unitary_conj` |
| `orbit_eq_rankClass` | 轨道作为集合 = 秩类 | 上式 `ext` |
| `orbit_eq_iff_same_rank` | 轨道相等 ⟺ 秩相等 | 上式 |
| `projRank` / `projRank_le_dim` | 投影秩函数 / 上界 | `Submodule.finrank_le` |
| `orbitRel_iff_same_rank` | 轨道关系 = 秩相等 | `orbitRel_apply` + `mem_orbit_iff` |
| `exists_projRank_eq` | 每个 $\le\dim E$ 的秩被实现 | §2.22 `projOfRank` |
| `orbitQuotToRank` / `_injective` / `_surjective` | 轨道空间 → 秩集（双射） | `Quotient.lift` + `projOfRank` |
| `orbitQuotEquivRankSet` | **轨道空间 ≃ 秩集** | `Equiv.ofBijective` |

**实现要点**：酉群取 `E ≃ₗᵢ[ℂ] E`（mathlib `Group` 实例，`(u*v) x = u (v x)`）。作用律证明需两条
逆应用引理：`(1 : E ≃ₗᵢ[ℂ] E).symm x = x`（`change` 转 `⁻¹` + `simp`）与
`(u * v).symm x = v.symm (u.symm x)`（`change` 转 `⁻¹` + `_root_.mul_inv_rev` + `simp`）；`MulAction`
的 `one_smul`/`mul_smul` 经 `show conjProj ... = ...` 展开 smul + `Subtype.ext` + `ext x` +
`simp [conjProj, 辅助引理]` 闭合。轨道 = 秩类经 §2.21 `same_rank_iff_unitary_conj` 双向构造
（`Q = U P U⁻¹` 即 `U • P = Q`）。轨道空间 ≃ 秩集：`Quotient.lift` 经 `orbitRel_iff_same_rank`
良定，单射用 `orbitRel_iff_same_rank` 反向、满射用 §2.22 `projOfRank` 实现每个秩。

### 31.3 诚实边界

本节闭合的是**轨道层**的对应——即把 §2.21 的**逐对**酉双射提升为**轨道分解**（轨道 = 秩类、
轨道空间 ≃ 秩集，轨道数 $=\dim E+1$）。诚实区分：① $U(n)$ **同伦层**（$U(n)$ 路径连通 /
投影空间连通分量与秩对应，需拓扑/同伦基建）仍登记开放——本节给出的是**集合/轨道层**的对应，
非连续同伦类的对应；② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）仍开放。

### 31.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十二、BerryChern §2.26：对象层 K₀ 的等距自然性——差类映射、分类器不变量、函子性与酉作用平凡

承接 §三十一（§2.25）：酉群共轭作用与轨道 = 秩类已闭合。本节补齐**对象层 K₀ 的自然性**：把 §2.24
的等距共轭 `conjProj` 沿对象层下降为差类映射 `conjProjQuot`，证明其与分类器交换、是双射、满足函子性，
并得出**酉群在对象层 K₀ 上作用平凡**（K₀ 是酉不变量）。

### 32.1 闭合的开放项

- 对象层 K₀ 的**等距不变量性**：**闭合**——`projToInt_conjProj` / `conjProjQuot_projToInt`。
- 等距诱导映射的**函子性**：**闭合**——`conjProjQuot_trans`（复合）/`conjProjQuot_refl`（单位）
  + 投影层辅助引理 `conjProj_trans`/`conjProj_refl`。
- **酉作用在对象层平凡**：**闭合**——`conjProjQuot_unitary_fixed`。

### 32.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `projToInt_conjProj` | 分类器等距不变量 | §2.24 `conjProj_rank` + `quotientRank` lift_mk |
| `conjProjQuot` | 等距诱导差类映射 `ProjDiffQuot E → ProjDiffQuot F` | `Quotient.lift` + `projToInt_injective` |
| `conjProjQuot_mk` | 代表元计算 | `rfl` |
| `conjProjQuot_projToInt` | 与分类器交换 | `Quotient.inductionOn` + 上式 |
| `conjProjQuot_injective` / `_surjective` | 单射 / 满射 | `projToInt` 单射 + `e.symm` |
| `conjProjQuotEquiv` | 双射 `ProjDiffQuot E ≃ ProjDiffQuot F` | `Equiv.ofBijective` |
| `conjProj_trans` / `conjProj_refl` | 共轭对复合/恒等相容 | `Subtype.ext` + `ext` + `simp [conjProj]` |
| `conjProjQuot_trans` / `conjProjQuot_refl` | 函子性（复合/单位） | `Quotient.inductionOn` + 上式 |
| `conjProjQuot_unitary_fixed` | **酉作用平凡**（K₀ 是酉不变量） | `projToInt_injective` + 交换律 |

**实现要点**：等距不变量 `projToInt_conjProj` 经 `projToInt_mk` 展开为 `quotientRank` 之差，
再用 `Quotient.lift_mk` 把 `quotientRank` 化为 `finrank (range ·)`，最后取 §2.24 `conjProj_rank` 保秩。
差类映射 `conjProjQuot` 的良定性经 `projToInt_injective`：把两边的 `projToInt` 用 `projToInt_conjProj`
化为原空间的 `projToInt`，再用 `Quotient.sound h` 的 `congrArg`。函子性经 `Quotient.inductionOn` +
`conjProjQuot_mk` 降到投影层，再由 `conjProj_trans`/`conjProj_refl` 闭合。酉作用平凡由
`projToInt` 单射 + `conjProjQuot_projToInt`（`projToInt (u • x) = projToInt x`）立得。

### 32.3 诚实边界

本节闭合的是**对象层 K₀ 的等距自然性**——差类映射 + 分类器交换 + 双射 + 函子性 + 酉作用平凡
（K₀ 是等距/酉不变量）。诚实区分：这是**集合/代数层**的自然性，不含拓扑/同伦内容。仍登记开放：
① $U(n)$ **同伦层**（路径连通 / 投影空间连通分量与秩对应——已确认当前 mathlib 尚无酉群连通性结果，
需拓扑/同伦基建）；② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）。

### 32.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十三、BerryChern §2.27：酉群连通性的拓扑基建第一层——局部路径连通与连通性归约

承接 §三十二（§2.26）：对象层 K₀ 自然性已闭合，但「$U(n)$ 与秩一一对应」的**同伦层**仍开放
（此前确认 mathlib `LinearAlgebra/Matrix` 无酉群连通性结果）。本节实地勘查发现**两个关键事实**：
(i) mathlib 已有 `Analysis/CStarAlgebra/Unitary/Connected.lean`——C\*-代数酉群的**局部路径连通**理论
与「路径分量 = 自伴指数乘积」刻画；(ii) `Matrix n n ℂ` 在 L²-算子范数下**是 C\*-代数**
（`Matrix.instCStarAlgebra`，需 `open scoped Matrix.Norms.L2Operator` 激活）。二者相合，可把 mathlib
酉群拓扑理论**直接实例化到矩阵酉群** `Matrix.unitaryGroup n ℂ`。

### 33.1 闭合的开放项

- $U(n)$ **局部拓扑基建**：**闭合**——局部路径连通 + 小球路径连通 + 小距离路径连通。
- **连通性的代数化与归约**：**闭合**——路径分量 = 自伴指数乘积；指数积覆盖 ⟹ 路径连通。
- 紧性辅助（有界性）：**闭合**——酉元各元素模 ≤ 1。

### 33.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `unitaryGroup_locallyPathConnected` | 矩阵酉群局部路径连通 | mathlib `Unitary.instLocallyPathConnectedSpace` |
| `unitaryGroup_joined` | `‖v-u‖<2` ⟹ `Joined u v` | mathlib `Unitary.joined` |
| `unitaryGroup_isPathConnected_ball` | 半径 < 2 球路径连通 | mathlib `Unitary.isPathConnected_ball` |
| `mem_pathComponent_one_iff_products` | `1` 的路径分量 = 有限个自伴指数之积 | mathlib `Unitary.mem_pathComponentOne_iff` |
| `unitaryGroup_entry_norm_le_one` | 酉元各元素模 ≤ 1 | mathlib `entry_norm_bound_of_unitary` |
| `pathConnectedSpace_unitaryGroup_of_products` | **连通性归约**：指数积覆盖 ⟹ 路径连通 | `mem_pathComponentOne_iff` + `PathConnectedSpace.mk` |

**实现要点**：关键在于让 `Matrix n n ℂ` 以 C\*-代数身份出现——其 `CStarAlgebra`/`NormedAlgebra`/
`MetricSpace` 实例均为 **scoped**（`scoped[Matrix.Norms.L2Operator] attribute [instance] …`），
故须在 section 内 `open scoped Matrix.Norms.L2Operator`。随后 mathlib 的 `Unitary` 拓扑定理可直接
以 `A := Matrix n n ℂ` 实例化（`unitaryGroup n ℂ` 与 `unitary (Matrix n n ℂ)` 定义等价）。
归约定理用 `PathConnectedSpace.mk`（需 `Nonempty` + `∀ x y, Joined x y`）：由
`mem_pathComponentOne_iff` 把「与 `1` 路径连通」转为指数积陈述，再用 `Joined.symm.trans` 拼接。

### 33.3 诚实边界

本节闭合的是**局部拓扑基建 + 连通性归约**——局部路径连通（mathlib 通用结论）、小球路径连通、
路径分量刻画、有界性，以及把**全局连通性归约为"指数积覆盖"**。诚实区分：① $U(n)$ **全局连通性**
本体仍开放——它等价于「每个酉阵 = 有限个自伴指数之积」，即酉阵的**正规谱定理/对数存在性**
（mathlib 目前仅有 Hermitian 谱定理 `Matrix.IsHermitian.eigenvectorUnitary`，正规矩阵的酉对角化缺）；
② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）仍开放。

### 33.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十四、BerryChern §2.28：全局连通性归约强化——`pathComponent 1` 是子群 + 「避开 -1」子类

承接 §三十三（§2.27）：全局连通性已归约为"指数积覆盖"。本节把该归约**强化为可操作形式**：证明指数积
集合 `pathComponent 1` 在 `Matrix.unitaryGroup n ℂ` 中是**子群**，从而把全局连通性化归为**单一群论
命题**；并证明**「避开 `-1`」子类**已落入该子群。

### 34.1 闭合的开放项

- 归约的可操作化（子群结构）：**闭合**——单位/乘法/逆封闭。
- 「避开 `-1`」子类的成员性：**闭合**——`‖u - 1‖ < 2` 时 `u ∈ pathComponent 1`。
- 连通性判据（充分条件群论化）：**闭合**——`(∀ u, u ∈ pathComponent 1) ⟹ PathConnectedSpace`。

### 34.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `expUnitary_neg` | 指数取逆公式 | `Commute.expUnitary_add` + `neg_add_cancel` |
| `expUnitary_mem_pathComponent_one` | 单指数落在 `pathComponent 1` | `mem_pathComponentOne_iff.mpr ⟨[x], _⟩` |
| `one_mem_pathComponent_one` | 单位落在 `pathComponent 1` | 空列表 |
| `mul_mem_pathComponent_one` | 乘法封闭 | `Joined.mul` |
| `reverse_map_neg_prod_mul_prod` | 逆序取负指数积 = 原积之逆 | 列表归纳 + `List.reverse_cons`/`prod_append` |
| `inv_mem_pathComponent_one` | 逆封闭 | `eq_inv_of_mul_eq_one_left` + 上式 |
| `mem_pathComponent_one_of_norm_sub_lt_two` | 「避开 `-1`」子类闭合 | mathlib `expUnitary_argSelfAdjoint` |
| `pathConnectedSpace_unitaryGroup_of_mem_pathComponent_one` | **连通性判据** | `Joined.refl`/`Joined.mul` + `PathConnectedSpace.mk` |

**实现要点**：`pathComponent 1 = {u | Joined 1 u}`（mathlib `mem_pathComponentOne_iff`），故子群封闭
可直接用 `Joined.mul`（拓扑群）与 `Joined.refl`；**逆封闭**因缺 `ContinuousInv` 实例改走列表技巧：
由 `u = ∏ expUnitary xᵢ` 得 `u⁻¹ = ∏ expUnitary (-x_{n+1-i})`（**逆序取负**），归纳证明需
`expUnitary (-x) * expUnitary x = 1` 且两因子**相邻**方可消去——故须 `l.reverse`。

### 34.3 诚实边界

本节闭合的是**归约强化**（子群结构 + 判据 + 已知子类）。全局连通性本体仍归约为**单一命题**
`∀ u : Matrix.unitaryGroup n ℂ, u ∈ pathComponent 1`（= 每个酉阵是有限个自伴指数之积），需**酉阵的
正规谱定理/对数存在性**（mathlib 目前仅有 Hermitian 谱定理 `Matrix.IsHermitian.eigenvectorUnitary`）。
两条可行路径：(i) 正规矩阵酉对角化（特征向量存在 + 正交补不变性 + 维数归纳）；(ii) 「旋转 + 指数」
技巧——取单位标量 ζ 使 `-ζ ∉ spectrum u`（需 `spectrum u` 有限），则 `u = (ζ·1)·(ζ⁻¹u)` 为两枚
「避开 `-1`」酉元之积，各由 `mem_pathComponent_one_of_norm_sub_lt_two` 落入子群，乘法封闭即得。
环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）仍开放。

### 34.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十五、BerryChern §2.29：矩阵谱有限性——"旋转 + 指数"路线的最后一块基建

承接 §三十四（§2.28）：全局连通性已归约为单一群论命题，并给出两条可行路径。本节补齐**路径 (ii)
「旋转 + 指数」**的最后一块基建——**矩阵谱有限性**（用于在单位圆上选出旋转标量 `ζ`）。

### 35.1 闭合的开放项

- 「旋转 + 指数」路线的谱有限性前提：**闭合**——`n×n` 复矩阵谱有限。

### 35.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `matrix_spectrum_finite` | `(spectrum ℂ A).Finite` | `Matrix.mem_spectrum_iff_isRoot_charpoly` + `charpoly_monic.ne_zero` + `Polynomial.mem_roots` + `Set.Finite.subset` |
| `matrix_spectrum_finite'` | `Finite ↥(spectrum ℂ A)` 类型类形式 | 同一结果（本版本 `Set.Finite s` 即 `Finite ↥s`） |
| `unitary_spectrum_finite` | 酉元（作为矩阵）谱有限 | `matrix_spectrum_finite` |

**实现要点**：本版本 mathlib 中 `Set.Finite s` 即子类型上的 `Finite s`，故「谱有限」写成
`(spectrum ℂ A).Finite` 后**同时**是类型类命题，可直接 `haveI` 引入。证明走「谱 = 特征多项式根集」：
`A.charpoly.roots.toFinset` 是有限集，用 `Set.Finite.subset` 归约，逐点用
`Matrix.mem_spectrum_iff_isRoot_charpoly` 把谱成员转为 `IsRoot`，再由 `mem_roots`（需
`charpoly ≠ 0`，由首一 `charpoly_monic.ne_zero`）转为根集成员。

### 35.3 诚实边界

本节闭合的是**谱有限性基建**。补齐后，「旋转 + 指数」路线尚差两块：
① **单位圆无穷 ⟹ 存在单位标量 `ζ` 使 `-ζ ∉ spectrum u`**（需 `Circle`/`Metric.sphere` 无穷）；
② **标量谱变换** `spectrum ℂ (c • A) = c • spectrum ℂ A`（`c ≠ 0`；mathlib 无现成引理，可由
`charpoly` 与行列式重推）。二者与 §2.28 `mem_pathComponent_one_of_norm_sub_lt_two` 合用即可闭合
全局连通性。另一条路（正规矩阵酉对角化：特征向量 + 正交补不变性 + 维数归纳）不受本层影响，仍登记
开放。环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）仍开放。

### 35.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十六、BerryChern §2.30：全局连通性收口——$U(n)$ 路径连通（K₀ 同伦层闭合）

承接 §三十五（§2.29）：谱有限性就位后，「旋转 + 指数」路线仅剩两块基建。本节一次性补完并**收口**。

### 36.1 闭合的开放项

- **单位圆无穷**（选旋转标量 `ζ` 的载体）：**闭合**——`unitCircle_infinite`。
- **标量谱变换**（把 `-1 ∉ spectrum (c•u)` 化归到 `-c⁻¹ ∉ spectrum u`）：**闭合**——`smul_mem_spectrum_iff`。
- **$U(n)$ 全局连通性**（= 每个酉元是有限个自伴指数之积）：**闭合**——`mem_pathComponent_one_unitary`
  + `pathConnectedSpace_unitaryGroup`。

### 36.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `isUnit_algebraMap_mul_iff` | 标量因子可提出单位判定 | 显式构造单位 `algebraMap c`（逆 `algebraMap c⁻¹`） |
| `smul_mem_spectrum_iff` | **标量谱变换** | `spectrum.mem_iff` + 因式分解 + 上式 |
| `unitCircle_infinite` | **单位圆无穷** | 半圆参数化 `x ↦ (x, √(1-x²))` 单射；`Set.Ioo_infinite.to_subtype` + `Set.infinite_range_of_injective` + `Complex.sq_norm`/`Real.sq_sqrt` |
| `exists_norm_eq_one_notMem_neg` | 单位圆可避开有限集 | `Set.Infinite.exists_notMem_finite` |
| `neg_one_notMem_spectrum_smul_one` | `ζ ≠ -1 ⟹ -1 ∉ spectrum (ζ•1)` | 显式单位 `(-(1+ζ)) • 1` |
| `smul_unitary_mem_unitary` | 标量旋转保持酉性 | `Unitary.mem_iff` 双向 + `star_smul`/`smul_mul_smul` |
| `scalar_smul_one_mem_pathComponent_one` | `ζ • 1 ∈ pathComponent 1` | `Unitary.norm_sub_one_lt_two_iff` + §2.28 判据 |
| `smul_unitary_mem_pathComponent_one` | `c • u ∈ pathComponent 1` | 同上 + 标量谱变换 |
| `mem_pathComponent_one_unitary` | **每个酉元 = 有限个指数之积** | 「旋转 + 指数」+ §2.28 乘法封闭 |
| `exists_expUnitary_prod_eq` | 指数积表示 | `mem_pathComponentOne_iff.mp` |
| `pathConnectedSpace_unitaryGroup` | **$U(n)$ 路径连通** | §2.28 判据 |
| `connectedSpace_unitaryGroup` | $U(n)$ 连通 | `PathConnectedSpace` 实例链 |

**实现要点**：「旋转 + 指数」——取单位圆上 `ζ` 使 `-ζ ∉ spectrum u`（谱有限 + 单位圆无穷）且 `ζ ≠ -1`
（把 `1` 也并入待避开的有限集），则 `u = (ζ • 1) · (ζ⁻¹ • u)`；两因子分别由
`Unitary.norm_sub_one_lt_two_iff` + §2.28 `mem_pathComponent_one_of_norm_sub_lt_two` 落入
`pathComponent 1`，乘法封闭即得。标量谱变换绕开 mathlib 缺失的 `spectrum (c • A) = c • spectrum A`
（改证等价的 `c⁻¹z ∈ spectrum a` 形式，直接经 `IsUnit` 判定因式分解）。

### 36.3 诚实边界

本节**闭合** $U(n)$ 全局连通性（路径连通）与等价的指数积覆盖定理，从而闭合 §3 #7 登记的
「$U(n)$ 酉群/同伦类与秩一一对应」的**连通性/同伦层**。**仍未闭合**：环面上陈数密度 $F$ 的连续场论/
度理论整性（含同伦提升，§3 #4）——需 `F` 的可积性/光滑性与环面积分层面的度理论，与群拓扑连通性
相互独立，登记开放。另一条路线（正规矩阵酉对角化）未采用，成为冗余路径。

### 36.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 零 error、零 `sorry`、零 `admit`
- [x] 剥离注释后本模块 `by sorry`/`admit` 计数 = 0

## 三十七、BerryChern §2.35–§2.37：Kato 微扰论三层——预解式恒等式 → 算子变量可微性

> **补记**：自 §三十六（§2.30）之后的 §2.31–§2.34（连续积分层：环绕数整值、一般度理论第一层、
> 度的同伦不变性、度的绝热不变性）已在 `BerryChern.lean` 闭合，其变更记录见 paper14 变更日志
> v1.39–v1.42 与 BerryChern §3 开放登记 #4；本路线自 Kato 层起续接本节。

承接 §三十六：§3 #4 剩余部分（**数值陈数** = 曲率积分）需要曲率被积 $F$ 的可积性/光滑性，
其源头是**投影族 $P(k)$ 关于参数的光滑性** —— Kato 解析微扰论。§2.35–§2.37 三层闭合该分析引擎。

### 37.1 闭合的开放项

- **预解式代数内核**（第一预解式恒等式，谱参数依赖）：**闭合** —— §2.35 `resolvent_sub_resolvent`。
- **第二预解式恒等式**（算子依赖，可微性代数引擎）：**闭合** —— §2.36 `resolvent_sub_resolvent_ops`。
- **预解式对算子变量的 Fréchet 可微性**（#3）：**闭合** —— §2.37 `resolvent_hasFDerivAt`。
- **`Matrix n n ℂ` 实例菱形障碍**：**闭合** —— `open scoped Matrix.Norms.L2Operator`（**无需 `letI`**，
  修正 §2.36 判断）。

### 37.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `resolvent_sub_resolvent`（§2.35） | 第一预解式恒等式（Hilbert，谱参数依赖） | `IsUnit.mul_val_inv`/`val_inv_mul` |
| `resolvent_sub_resolvent_ops`（§2.36） | 第二预解式恒等式 $R(a)-R(b)=R(a)(a-b)R(b)$ | 纯代数 + `abel` |
| `resolvent_diff_reduction`（§2.37） | 归约恒等式：误差项 $=R\delta(R'-R)$ | §2.36 恒等式 + `mul_sub` |
| `resolvent_hasFDerivAt`（§2.37） | **预解式算子变量可微性** $\mathrm D_aR:\delta\mapsto R\delta R$ | mathlib `spectrum.hasFDerivAt_resolvent`（需 `CompleteSpace`） |
| `matrix_l2_norm_witness`（§2.37） | L2 实例见证：$\lVert A\rVert = \lVert\texttt{toEuclideanCLM A}\rVert$ | `Matrix.l2_opNorm_toEuclideanCLM` |
| `matrix_resolvent_hasFDerivAt`（§2.37） | `Matrix n n ℂ` 固定 L2 实例特化 | 同上 |

**实现要点**：归约恒等式由 §2.36 第二预解式恒等式（取 `a ← a'`）得
$R(a')-R(a)=R(a)(a'-a)R(a')$，故误差项 $R(a')-R(a)-R(a)(a'-a)R(a)=R(a)(a'-a)(R(a')-R(a))$——
即 little-o 估计**完全归约**为**预解式连续性**。可微性本体由 mathlib `spectrum.hasFDerivAt_resolvent`
提供（内核 `hasFDerivAt_ringInverse`：`HasFDerivAt Ring.inverse (-mulLeftRight 𝕜 R x⁻¹ x⁻¹) x`，
与归约所得高阶项形式同构）。

### 37.3 诚实边界

本路线**闭合**预解式对算子变量的可微性（Kato 第三层，#3），从而为投影族 $P(k)$ 光滑性备好
分析引擎。**仍开放**：① 谱参数导数 $dR/dz=-R^2$（mathlib `spectrum.hasDerivAt_resolvent_const_left`
接口已备）；② Riesz 积分 $\oint R$ 下投影族 $P(k)$ 的显式光滑性；③ $F$ 的可积性与完整数值陈数。
实例菱形障碍最终解法为 `open scoped Matrix.Norms.L2Operator`（scoped 实例已足够，**修正**
§2.36 的「须 `letI`」判断）。

### 37.4 本轮验证

- [x] 探针 `_g37_probe.lean` 编译通过后剥离
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 4 定理：`resolvent_diff_reduction`/`resolvent_hasFDerivAt`/`matrix_l2_norm_witness`/`matrix_resolvent_hasFDerivAt`

## 三十八、BerryChern §2.38：Kato 微扰论第四层——谱参数导数 `dR/dz = -R²`

承接 §三十七（§2.35–§2.37）：§2.37 闭合**算子变量**方向的 Fréchet 可微性 `D_a R = δ ↦ R·δ·R`。
本节闭合**谱参数**方向的导数（Kato 谱参数导数）：$dR/dz = -R(a,z)^2$，并给出两层导数的相容性桥接。

### 38.1 闭合的开放项

- **谱参数导数** `dR/dz = -R²`：**闭合** —— §2.38 `resolvent_hasDerivAt`。
- **`Matrix n n ℂ` L2 特化**：**闭合** —— §2.38 `matrix_resolvent_hasDerivAt`。
- **两层导数相容性**（§2.37 ↔ §2.38）：**闭合** —— `resolvent_deriv_layers_agree`。

### 38.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `resolvent_hasDerivAt` | **谱参数导数** $dR/dz = -R^2$ | mathlib `spectrum.hasDerivAt_resolvent_const_left`（需 `CompleteSpace`） |
| `resolvent_deriv_layers_agree` | 两层导数相容：$-R^2 = -(R\cdot 1\cdot R)$ | 纯代数（`mulLeftRight_apply` + `pow_two`） |
| `matrix_resolvent_hasDerivAt` | `Matrix n n ℂ` 固定 L2 实例特化 | 同上 |

**实现要点**：mathlib 已备 `spectrum.hasDerivAt_resolvent_const_left`：
`HasDerivAt (resolvent a) (-(resolvent a k ^ 2)) k`（`Analysis/Normed/Algebra/GelfandFormula.lean`）。
两层相容性 `-R^2 = -(R\cdot1\cdot R)`（因 `mulLeftRight 𝕜 A R R 1 = R * 1 * R`）说明
$z\cdot1-a$ 中 $z$ 与 $a$ 的**反向中心耦合**：抬升 $a$ 的中心分量与降低 $z$ 等价、符号相反。

### 38.3 诚实边界

本节**闭合**预解式对谱参数的可微性（Kato 第四层）。至此 Kato 微扰论的**双层可微性基建**
（算子变量 + 谱参数）齐备。**仍开放**：① Riesz 积分 $\oint R$ 下投影族 $P(k)$ 的显式光滑性；
② $F$ 的可积性与完整数值陈数（⇐ $P(k)$ 光滑）。

### 38.4 本轮验证

- [x] 探针 `_g38_probe.lean` 编译通过（零 warning）后剥离
- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 3 定理：`resolvent_hasDerivAt`/`resolvent_deriv_layers_agree`/`matrix_resolvent_hasDerivAt`

## 三十九、BerryChern §2.39：Kato 微扰论第五层——Riesz 积分与投影族 `P(k)` 的定量光滑性

承接 §三十八（§2.35–§2.38）：预解式的**双层可微性**（算子变量 `D_aR = δ ↦ R·δ·R`、谱参数 `dR/dz = −R²`）
齐备后，本节把它**积分**成谱投影——**Riesz 积分** `P(a) = (2πi)⁻¹ ∮_{|z−c|=r} R(a,z) dz`。

### 39.1 闭合的开放项

- **Riesz 积分的定义与良定义性**：**闭合** —— `rieszIntegral` + `resolvent_differentiableOn_sphere` +
  `circleIntegrable_resolvent`。
- **围道微积分定量核心**：**闭合** —— `resolventCircleIntegrand`/`resolventCircleDeriv` +
  `norm_resolventCircleDeriv_le` + `norm_resolvent_sub_le`/`norm_resolvent_sub_le_of_bound`。
- **投影族 `P(k)` 的定量光滑性**：**闭合** —— `norm_rieszIntegral_sub_le`（参数 Lipschitz 估计）
  + `lipschitzOnWith_rieszIntegral` + `continuousAt_rieszIntegral`。

### 39.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `rieszIntegral` | **Riesz 积分（谱投影候选）** `(2πi)⁻¹ ∮ R dz` | `circleIntegral` + `smul` |
| `resolvent_differentiableOn_sphere` | 围道避开谱 ⟹ `z ↦ R(a,z)` 圆周上可微 | §2.38 `spectrum.hasDerivAt_resolvent_const_left` 逐点 |
| `circleIntegrable_resolvent` | **良定义性**：围道避开谱 ⟹ 圆周可积 | `ContinuousOn.circleIntegrable'` |
| `resolventCircleIntegrand` / `resolventCircleDeriv` | 围道被积函数及其对参数导数 | 定义（后者用 §2.37 `mulLeftRight`） |
| `norm_resolventCircleDeriv_le` | `‖deriv γ • R·(·)·R‖ ≤ \|r\|M²` | `deriv_circleMap` + `opNorm_mulLeftRight_apply_apply_le` |
| `norm_resolvent_sub_le` / `_of_bound` | `‖R(a)−R(b)‖ ≤ ‖R(a)‖‖R(b)‖‖a−b‖ ≤ M²‖a−b‖` | §2.36 第二预解式恒等式 + `norm_mul_le`（次可乘） |
| `norm_rieszIntegral_sub_le` | **参数 Lipschitz 估计** `‖P(a)−P(b)‖ ≤ r·M²·‖a−b‖` | `circleIntegral.norm_two_pi_i_inv_smul_integral_le_of_norm_le_const` |
| `lipschitzOnWith_rieszIntegral` | `P` 在 `ball a 1` 上 Lipschitz | `LipschitzOnWith.of_dist_le_mul` |
| `continuousAt_rieszIntegral` | **投影族参数连续性** | Lipschitz ⟹ `continuousOn` ⟹ `continuousAt` |

**实现要点**：Riesz 积分的归一化 `(2πi)⁻¹` 与 mathlib 的圆周积分范数估计
`circleIntegral.norm_two_pi_i_inv_smul_integral_le_of_norm_le_const`（`‖(2πi)⁻¹∮f‖ ≤ r·C`）恰好匹配；
参数估计用 `circleIntegral.integral_sub` 把差写成差函数的围道积分，再用 §2.36 恒等式的定量版逐点估计。

### 39.3 诚实边界

本节**闭合** Riesz 积分的**良定义性**与投影族 `P(k)` 的**定量光滑性（Lipschitz / 连续）**。
**仍开放**：① Riesz 积分的**微分** `HasFDerivAt (fun x => P(x)) (∮ R·(·)·R)`——**障碍已精确定位**：
参数积分求导（`hasFDerivAt_integral_of_dominated_of_fderiv_le`）的接口处再现 §2.35/§2.36 所记
**`HasFDerivAt` 实例菱形**（mathlib 侧 `NonUnitalNormedRing.toNormedAddCommGroup` vs 本文上下文侧
`NonUnitalSeminormedRing.toSeminormedAddCommGroup` 两条 `AddCommGroup` 路径），须以 `letI`
**显式固定实例**方可陈述/证明；② Riesz 投影的**幂等性** `P² = P`（需双重围道积分 + Cauchy 定理）；
③ $F$ 的可积性与完整数值陈数。

### 39.4 本轮验证

- [x] 探针 `_g39_probe.lean` 编译通过（零 warning）后剥离
- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 11 项：`rieszIntegral`/`resolvent_differentiableOn_sphere`/`circleIntegrable_resolvent`/
  `resolventCircleIntegrand`/`resolventCircleDeriv`/`norm_resolventCircleDeriv_le`/
  `norm_resolvent_sub_le`/`norm_resolvent_sub_le_of_bound`/`norm_rieszIntegral_sub_le`/
  `lipschitzOnWith_rieszIntegral`/`continuousAt_rieszIntegral`

## 四十、BerryChern §2.40：Kato 微扰论第六层——投影族 `P(k)` 的 Fréchet 可微性（正面攻克实例菱形）

承接 §三十九（§2.39）：Riesz 积分的**良定义性**与**定量光滑性**（Lipschitz / 连续）已闭合，
但**微分**受阻于参数积分求导接口处的 **`HasFDerivAt` 实例菱形**。本节**正面攻克**该菱形并闭合微分。

### 40.1 菱形的精确诊断（随登，修正 §2.35–§2.39 的初判）

本版本 mathlib 中 `HasFDerivAt` 的类型上下文（`Analysis/Calculus/FDeriv/Defs.lean`）为

```lean
variable {E : Type*} [AddCommGroup E] [Module 𝕜 E] [TopologicalSpace E]
variable {F : Type*} [AddCommGroup F] [Module 𝕜 F] [TopologicalSpace F]
```

即 `HasFDerivAt` **只要求** `AddCommGroup` / `Module` / `TopologicalSpace`（**不含范数**）。
用 `pp.explicit` 展开后可见，菱形**不在 `AddCommGroup A` 本身**，而在 **`Module ℂ A` 内部的
`SeminormedAddCommGroup A` 参数**上：

- 一条路径：`NormedRing A` → `NonUnitalSeminormedRing.toSeminormedAddCommGroup`；
- 另一条：`NormedAlgebra.toNormedSpace` 内部的 `NormedSpace` 自带的那条。

（`set_option pp.explicit true` 展开显示：goal 侧 `@NormedSpace.toModule ℂ A (NonUnitalSeminormedRing...)
(NormedAlgebra.toNormedSpace ℂ A)` vs term 侧 `(NormedAlgebra.toNormedSpace ℂ A).toModule`。）

### 40.2 解法（两条，均随登）

1. **让结论与引理逐字对齐**：把围道参数化定理的结论写成**集合积分形式**
   `∫ θ, ... ∂(volume.restrict (Ι 0 (2π)))`，与 `hasFDerivAt_integral_of_dominated_of_fderiv_le`
   的结论（`∫ a, F x a ∂μ`）**完全相同**。注意 `intervalIntegral` 是**独立定义**
   `intervalIntegral f a b μ := ∫ x in Ioc a b, f x ∂μ - ∫ x in Ioc b a, f x ∂μ`，
   与集合积分仅**命题相等**（`intervalIntegral.integral_of_le` + `Set.uIoc_of_le`）而非 defeq——
   这正是此前 `exact` 在同一形状上报类型不匹配的根因之一。
2. **弃用 `simpa ... using`**：`simpa only using e` 的语义是**脱离期望类型**独立精化 `e`，
   故 `e` 的实例参数由默认合成确定、与 goal 侧不一致；改用 `exact e` / `refine e`
   会把**期望类型传入**精化，实例参数即按 goal 侧确定。**判别实验**：同一目标下
   `simpa only using` 失败而 `exact` 成功（本轮探针 `_g40_probe.lean` 专此验证）。

### 40.3 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `rieszIntegral_eq_integral` | `intervalIntegral` ↔ 集合积分形式桥接 | `intervalIntegral.integral_of_le` + `Set.uIoc_of_le` |
| `hasFDerivAt_circleIntegral_resolvent` | 围道参数化形式的参数可微性（集合积分形式） | `hasFDerivAt_integral_of_dominated_of_fderiv_le`（全部 `exact`）+ §2.37 `spectrum.hasFDerivAt_resolvent` |
| `rieszIntegral_hasFDerivAt` | **Riesz 积分的微分** `D_a P = (2πi)⁻¹ ∮ R(a,z)·(·)·R(a,z) dz` | 上式 `.const_smul` + `Filter.EventuallyEq.hasFDerivAt_iff` |

**实现要点**：`h_diff` 一步用
`exact (spectrum.hasFDerivAt_resolvent hspec).const_smul (deriv (circleMap c r) θ)`
（**不用** `simpa only [...] using`）；末定理用 `Filter.EventuallyEq.hasFDerivAt_iff`
把 `(2πi)⁻¹ • ∫ ... ∂μ` 形式的 `HasFDerivAt` 转成 `fun x => rieszIntegral x c r`。

### 40.4 诚实边界

本节**闭合** Riesz 积分的**微分**（Kato 第六层）；至此投影族 `P(k)` 的 **C¹ 光滑性**在形式上就位
（`P` 可微，且导数 `∮ R·(·)·R` 由被积函数连续性与 §2.39 定量估计亦连续）。
**仍开放**：① Riesz 投影的**幂等性** `P² = P`（需双重围道积分 + Cauchy 定理）；
② $F$ 的可积性与完整数值陈数。

### 40.5 本轮验证

- [x] 探针 `_g40_probe.lean` 编译通过（零 warning）后剥离
- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 3 定理：`rieszIntegral_eq_integral`/`hasFDerivAt_circleIntegral_resolvent`/`rieszIntegral_hasFDerivAt`

## 四十一、BerryChern §2.41：Kato 微扰论第七层——Riesz 投影的幂等性 `P² = P`

承接 §四十（§2.40）：Riesz 积分 `P(a) = (2πi)⁻¹ ∮_{C(c,r)} R(a,z) dz` 的**良定义性**、
**定量光滑性**与**参数可微性**齐备后，本节闭合其**幂等性** `P² = P`——即该 Riesz 积分确为
**投影算子**（谱投影），从而 Berry 曲率 `F = −i·Tr(P [A,B])` 中的 `P` 具备「投影」代数身份。

### 41.1 闭合的开放项

- **Riesz 投影幂等性** `P² = P`：**闭合** —— `rieszIntegral_idempotent`（Kato 双重围道论证）。

### 41.2 证明路线（Kato 双重围道论证的 Lean 化）

设 `0 < r₂ < r₁`，闭环形区域 `D(c,r₁) \ D(c,r₂)` 避开谱。记
`K₁ = ∮_{C(c,r₁)} R(z) dz`、`K₂ = ∮_{C(c,r₂)} R(w) dw`（`R(·) = resolvent a (·)`）。

1. **双重围道归约** `circleIntegral_resolvent_mul_eq`：`K₁ K₂ = 2πi · K₂`。
   - 用 `circleIntegral_mul_const` / `circleIntegral_const_mul`（算子值圆周积分的右/左线性，
     由 `ContinuousLinearMap.intervalIntegral_comp_comm` + `ContinuousLinearMap.mul` 及其
     `flip` 给出）把 `K₁K₂` 改写为二重围道积分 `∮_{C(c,r₁)}∮_{C(c,r₂)} R(z)R(w)`；
   - 逐点用**预解式乘法恒等式** `resolvent_mul_resolvent_spectral`
     （`R(z)R(w) = (w−z)⁻¹ • (R(z)−R(w))`，由 §2.35 `resolvent_sub_resolvent` 提取中心标量
     `(w−z)·1` 得 `resolvent_sub_resolvent_smul`，再 `inv_smul_smul₀`）；
   - 内层线性拆出后，`z` 落在内圈 `C(c,r₂)` **之外**，故 `∮_{C(c,r₂)} (w−z)⁻¹ dw = 0`
     （`circleIntegral_inv_sub_eq_zero`，用 mathlib
     `circleIntegral_eq_zero_of_differentiable_on_off_countable` + `Set.countable_empty`）；
   - 剩一项 `−∮_{C(c,r₁)}∮_{C(c,r₂)} (w−z)⁻¹ • R(w)`，用**算子值双围道 Fubini 交换**
     `circleIntegral_circleIntegral_swap` 交换次序：先把二重围道积分参数化为
     `θ, φ ∈ [0,2π]` 上的二重 `intervalIntegral`（`circlePairIntegrand`），
     再由 `intervalIntegral_intervalIntegral_swap` 交换（可积性来自被积函数在参数化乘积
     `[0,2π]×[0,2π]` 上连续 ⟹ `integrableOn_compact`，再 `mono_set` 到 `Ι 0 2π ×ˢ Ι 0 2π`）；
   - 内层化为**标量留数** `∮_{C(c,r₁)} (w−z)⁻¹ dz = 2πi`（`w ∈ D(c,r₁)`，
     mathlib `circleIntegral.integral_sub_inv_of_mem_ball`），得 `K₁K₂ = 2πi·K₂`。
2. **标量归一化** `rieszIntegral_mul_eq`：`P₁P₂ = P₂`（因 `(2πi)⁻¹·(2πi)⁻¹·(2πi) = (2πi)⁻¹`）。
   代数链：`smul_mul_smul'`（`(c•x)(d•y) = (c*d)•(x*y)`）→ `hK` → **正向 `smul_smul`**
   → `mul_assoc` → `inv_mul_cancel₀` → `mul_one`。
   **踩坑随登**：mathlib `smul_smul` 的语句方向为 `a₁ • a₂ • b = (a₁*a₂) • b`
   （`Algebra/Group/Action/Defs.lean`），故 `a • b • x ↦ (a*b) • x` 的归约须用**正向**
   `rw [smul_smul]`；误用 `← smul_smul` 会反向拆成 `a • b • x` 致 `inv_mul_cancel₀` 失配。
3. **围道独立性** `rieszIntegral_eq_of_lt`：环形区域避开谱 ⟹ `P_{r₁} = P_{r₂}`
   （mathlib annulus 版 Cauchy–Goursat
   `circleIntegral_eq_of_differentiable_on_annulus_off_countable` + §2.38
   `spectrum.hasDerivAt_resolvent_const_left` 逐点给出环形区域上的 `DifferentiableOn`）。
4. **收口** `rieszIntegral_idempotent`：`P_{r₁}² = P_{r₁}P_{r₂} = P_{r₂} = P_{r₁}`。

### 41.3 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `smul_mul_smul'` | 混合标量-算子乘法结合律 `(c•x)(d•y) = (c*d)•(x*y)` | `smul_mul_assoc`/`mul_smul_comm`/`smul_smul` |
| `resolvent_sub_resolvent_smul` | **第一预解式恒等式（标量显式版）** `R(z)−R(w) = (w−z)•(R(z)R(w))` | §2.35 `resolvent_sub_resolvent` + `Algebra.smul_def`/`Algebra.commutes` |
| `resolvent_mul_resolvent_spectral` | 预解式乘法恒等式 `R(z)R(w) = (w−z)⁻¹•(R(z)−R(w))` | 上式 + `inv_smul_smul₀` |
| `circleIntegral_inv_sub_eq_zero` | **围道外留数** `z` 在 `D(c,r)` 外 ⟹ `∮(w−z)⁻¹dw = 0` | `circleIntegral_eq_zero_of_differentiable_on_off_countable` |
| `circleIntegral_mul_const` | 算子值圆周积分**右线性** `∮ f·b = (∮ f)·b` | `intervalIntegral_comp_comm` + `(mul ℂ A).flip` |
| `circleIntegral_const_mul` | 算子值圆周积分**左线性** `∮ b·f = b·(∮ f)` | `intervalIntegral_comp_comm` + `mul ℂ A` |
| `circlePairIntegrand` | 双围道被积函数的参数化 | 定义 |
| `circleIntegral_circleIntegral_swap` | **算子值双围道 Fubini 交换** | 参数化 + `intervalIntegral_intervalIntegral_swap` |
| `circleIntegral_resolvent_eq_of_lt` | **围道独立性（算子值）** 谱空环形 ⟹ `∮_{C(c,r₁)}R = ∮_{C(c,r₂)}R` | annulus Cauchy–Goursat |
| `continuousOn_resolvent` | 预解式在避开谱的集合上连续 | §2.38 谱参数导数的连续化 |
| `circleIntegrable_resolvent_of_nonneg` | 非负半径圆周上预解式可积 | 复用 §2.39 `circleIntegrable_resolvent`（`abs_of_nonneg`） |
| `circleMap_ne_circleMap` | 内半径非负且更小时两同心圆周点不相交 | 反证 + `abs_norm_sub_norm_le` |
| `circleIntegral_resolvent_mul_eq` | **双重围道核心** `K₁K₂ = 2πi·K₂` | 上列各件组装 |
| `rieszIntegral_mul_eq` | **标量归一化** `P₁P₂ = P₂` | `smul_mul_smul'` + `smul_smul` + `inv_mul_cancel₀` |
| `rieszIntegral_eq_of_lt` | Riesz 积分的**围道独立性** `P_{r₁} = P_{r₂}` | `circleIntegral_resolvent_eq_of_lt` |
| `rieszIntegral_idempotent` | **Riesz 投影幂等性** `P² = P` | `rieszIntegral_eq_of_lt` + `rieszIntegral_mul_eq` |

**实现要点**：算子值双围道积分不能直接调用 mathlib 的 Fubini，须**显式参数化**
（`circlePairIntegrand`，`θ` 对应外圈、`φ` 对应内圈）并用 `intervalIntegral_intervalIntegral_swap`
交换；交换所需的可积性由「被积函数在 `[0,2π]×[0,2π]` 上连续」经 `ContinuousOn.integrableOn_compact`
（`isCompact_Icc.prod isCompact_Icc`）+ `Set.prod_mono`（`Ι 0 2π ⊆ Icc 0 2π`）得到。

### 41.4 诚实边界

本节**闭合** Riesz 投影的**幂等性** `P² = P`（Kato 第七层）。假设为「存在 `0 < r₂ < r₁` 使
**闭环形区域** `D(c,r₁) \ D(c,r₂)` 避开谱」——即 `C(c,r₁)` 恰为**谱岛边界**（岛含于 `D(c,r₂)`，
或谱全在 `D(c,r₁)` 之外）。这是 Riesz 投影幂等性的**标准 Kato 前提**：单一围道本身不足以支撑
`P² = P` 的双重积分论证，须有辅助内圈作 Fubini 载体。
**仍开放**：$F$ 的可积性与完整数值陈数。

### 41.5 本轮验证

- [x] 探针 `_g42_probe.lean` / `_g42_scalar.lean` / `_g42_scalar2.lean` 编译通过（零 warning）后剥离
- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 16 项：`smul_mul_smul'`/`resolvent_sub_resolvent_smul`/`resolvent_mul_resolvent_spectral`/
  `circleIntegral_inv_sub_eq_zero`/`circleIntegral_mul_const`/`circleIntegral_const_mul`/
  `circlePairIntegrand`/`circleIntegral_circleIntegral_swap`/`circleIntegral_resolvent_eq_of_lt`/
  `continuousOn_resolvent`/`circleIntegrable_resolvent_of_nonneg`/`circleMap_ne_circleMap`/
  `circleIntegral_resolvent_mul_eq`/`rieszIntegral_mul_eq`/`rieszIntegral_eq_of_lt`/
  `rieszIntegral_idempotent`

## 四十二、BerryChern §2.42：Berry 曲率被积函数的连续性与环面可积性（闭合 §3 #1 的「F 可积性」）

承接 §四十一（§2.41）：Riesz 投影 `P` 的**良定义性**、**定量光滑性**、**参数可微性**与
**幂等性** `P² = P` 齐备后，Berry 曲率 `F = −i·Tr(P[A,B])` 中的 `P` 已具备完整分析身份。
本节闭合 §3 #1 登记中「环面上 `F` 的**可积性**（⇐ `P` 光滑）」这一开放项——即把「`P` 光滑」
经**多项式复合 + 紧致域**传化为被积函数的环面可积性。

### 42.1 闭合的开放项

- **环面上 Berry 曲率被积函数的可积性**（§3 #1 的「`F` 可积性」）：**闭合** ——
  `torusIntegrable_berryCurvature`（连续投影/切向量族 ⟹ `TorusIntegrable`）。

### 42.2 证明路线（多项式复合 + 紧致域）

1. **被积函数对三元组的连续性** `continuous_berryCurvature`：`F = −i·Tr(P[A,B])` 是矩阵乘法 +
   迹 + 标量乘的**多项式**复合，故 `(P,A,B) ↦ F(P,A,B)` 连续（`unfold berryCurvature` +
   `fun_prop`）。
2. **连续族复合** `continuous_berryCurvature_comp`：投影族 `x ↦ P(x)` 与切向量族 `x ↦ A(x),B(x)`
   连续 ⟹ `x ↦ F(P(x),A(x),B(x))` 连续（§2.39 已证 Riesz 积分族的参数连续性，此处为其复合层）。
3. **环面参数化连续性** `continuous_torusMap`：`θ ↦ (cᵢ + Rᵢ·e^{θᵢ i})ᵢ` 连续（`unfold torusMap` +
   `fun_prop`）。
4. **连续 ⟹ 环面可积** `torusIntegrable_of_continuous`：`f` 连续 ⟹ `f ∘ torusMap c R` 在紧致
   参数域 `Icc 0 (2π)ⁿ` 上连续 ⟹ 可积（`Continuous.integrableOn_Icc`）。
5. **主定理** `torusIntegrable_berryCurvature`：连续投影/切向量族 ⟹ `F(k)` 在
   `T² = {|z₀|=|z₁|=1}` 上可积——即 `chernIntegralTorus F` 的**分析前提**（被积可积）成立。
6. **先验有界性** `norm_chernIntegralTorus_le`：`‖F‖ ≤ C` 在环面上 ⟹ `‖∯ F‖ ≤ (2π)²·C`
   （mathlib `norm_torusIntegral_le_of_norm_le_const`，半径 1 时 `∏ᵢ|Rᵢ| = 1`）。

### 42.3 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `continuous_berryCurvature` | `F = −i·Tr(P[A,B])` 关于 `(P,A,B)` 连续 | `unfold` + `fun_prop` |
| `continuous_berryCurvature_comp` | 连续投影/切向量族 ⟹ 复合 `F` 连续 | `fun_prop` |
| `continuous_torusMap` | 环面参数化 `θ ↦ (cᵢ+Rᵢe^{θᵢi})ᵢ` 连续 | `unfold` + `fun_prop` |
| `torusIntegrable_of_continuous` | 连续 ⟹ `TorusIntegrable`（紧致域可积） | `Continuous.integrableOn_Icc` |
| `torusIntegrable_berryCurvature` | **连续族 ⟹ `F` 在 `T²` 上可积** | 上列各件组装 |
| `norm_chernIntegralTorus_le` | 陈数积分先验界 `‖∯F‖ ≤ (2π)²·C` | `norm_torusIntegral_le_of_norm_le_const` |

### 42.4 诚实边界

本节**闭合**被积函数的**连续性**与**环面可积性**（§3 #1 的「`F` 可积性」）。
**仍开放**：① 完整**数值**陈数（须将 `F` 具体化为 `P(k)` 的显式谱数据并在 `T²` 上求积分值）；
② 陈数**整性** `C ∈ ℤ`（度理论/同伦提升论证，§3 #2/#4）。

### 42.5 本轮验证

- [x] 探针 `_g43_probe.lean` 编译通过（零 warning）后剥离
- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 6 定理：`continuous_berryCurvature`/`continuous_berryCurvature_comp`/
  `continuous_torusMap`/`torusIntegrable_of_continuous`/`torusIntegrable_berryCurvature`/
  `norm_chernIntegralTorus_le`

## 四十三、BerryChern §2.43：环面留数定理（Laurent 单项式层）——`∮ z^m` 与 `∯ z₀^m z₁^n` 的完整分类

承接 §四十二（§2.42）：`F` 在 `T²` 上的**连续性**与**可积性**（即 `chernIntegralTorus F` 的
**分析前提**）闭合后，本节把「`∯ F` 的**数值**」在 **Laurent 单项式层**上真正算出来。
显式两带模型的曲率密度 `F` 在**全局标架**（`zᵢ = e^{iθᵢ}` 取作环面复坐标）下常可展为
`z₀^m z₁^n` 的**有限线性组合**，故其环面积分由本节分类定理给出**闭式**。

### 43.1 证明路线（全部落在复分析的留数定理上）

1. **一维留数分类** `circleIntegral_zpow_of_ne`/`circleIntegral_zpow_neg_one`：单位圆
   `C(0,1)` 上 `∮ z^m dz = 2πi·δ_{m,-1}`——仅 `m = -1` 有留数 `2πi`（mathlib
   `circleIntegral.integral_sub_zpow_of_ne` 与 `circleIntegral.integral_sub_inv_of_mem_ball`）。
2. **环面单项式可积性** `torusIntegrable_monomial`：`z₀^m z₁^n`（任意整数指数）在 `T²` 上
   可积——`torusMap` 分量 `e^{iθ}` 非零，故 `Continuous.zpow₀` + 紧致域 `Continuous.integrableOn_Icc`。
3. **环面单项式因子化** `torusIntegral_dim2_monomial_factor`：
   `∯_{T²} z₀^m z₁^n = (∮_{C(0,1)} z^m)·(∮_{C(0,1)} z^n)`——`torusIntegral_succ` 将二维环面沿
   第一坐标降维为一维圆周积分，`torusIntegral_dim1` 再把内层退化环面识别为单位圆 `C(0,1)`。
4. **环面留数定理（主定理）** `torusIntegral_dim2_monomial`：`∯_{T²} z₀^m z₁^n = (2πi)²`
   当且仅当 `m = n = -1`，否则为 `0`——二维环面上**仅**双极点被积 `z₀^{-1}z₁^{-1}` 有留数
   `(2πi)²`，与 §2.13 `torusIntegral_dim2_double_inv` 完全一致（后者是该主定理的特例）。
5. **Laurent 多项式线性化** `torusIntegral_dim2_laurentPoly`（§2.43.2）：由积分线性性，
   有限 Laurent 组合 `∑_{(m,n)∈s} c_{mn} z₀^m z₁^n` 的环面积分 `= (2πi)²·c_{-1,-1}`——即 `∯`
   是 **`z₀^{-1}z₁^{-1}` 系数提取器**，给出**标架类**被积的闭式求值。

### 43.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `circleIntegral_zpow_of_ne` | `m ≠ -1 ⟹ ∮_{C(0,1)} z^m = 0` | `circleIntegral.integral_sub_zpow_of_ne` |
| `circleIntegral_zpow_neg_one` | `∮_{C(0,1)} z⁻¹ = 2πi`（唯一一维留数） | `circleIntegral.integral_sub_inv_of_mem_ball` |
| `torusIntegrable_monomial` | `z₀^m z₁^n` 在 `T²` 上可积 | `Continuous.zpow₀` + `integrableOn_Icc` |
| `torusIntegral_dim2_monomial_factor` | `∯ z₀^m z₁^n = (∮ z^m)(∮ z^n)` | `torusIntegral_succ` + `torusIntegral_dim1` |
| `torusIntegral_dim2_monomial` | **环面留数定理**：非零仅当 `m=n=-1`，值 `(2πi)²` | 因子化 + 一维分类 |
| `torusIntegrable_monomial_const_mul` | `a·(z₀^m z₁^n)` 环面可积 | `IntegrableOn.const_mul` |
| `torusIntegrable_monomial_sum` | Laurent 有限和在 `T²` 上可积 | `Finset` 归纳 + `TorusIntegrable.add` |
| `torusIntegral_dim2_monomial_linear` | `∯` 对两项线性 | `torusIntegral_add` + `torusIntegral_const_mul` |
| `torusIntegral_dim2_monomial_sum` | `∯` 与有限和交换 | `Finset` 归纳 + `torusIntegral_add` |
| `torusIntegral_dim2_laurentPoly` | **`∯` 为 `z₀⁻¹z₁⁻¹` 系数提取器**：`= (2πi)²·c_{-1,-1}` | 上列各件 + `Finset.sum_eq_single` |

### 43.3 诚实边界

本节闭合 **Laurent 单项式层**的完整留数分类——即**标架类**被积（全局 Laurent 多项式）的
环面积分可**闭式**求值。**仍开放**：一般两带模型的曲率密度 `F` 通常含**非 Laurent** 结构
（如 `(1 + 2u)^{-3/2}` 型根式分母），其陈数**非零**的显式值与整性仍需完整度理论/数值积分
基建（§3 #1）；而**标架存在 ⟹ C = 0** 的结构性定理见 §2.44。

### 43.4 本轮验证

- [x] 探针 `_g44_probe.lean` 编译通过（零 warning）后剥离
- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 10 定理：`circleIntegral_zpow_of_ne`/`circleIntegral_zpow_neg_one`/
  `torusIntegrable_monomial`/`torusIntegral_dim2_monomial_factor`/`torusIntegral_dim2_monomial`/
  `torusIntegrable_monomial_const_mul`/`torusIntegrable_monomial_sum`/
  `torusIntegral_dim2_monomial_linear`/`torusIntegral_dim2_monomial_sum`/`torusIntegral_dim2_laurentPoly`

## 四十四、BerryChern §2.44：显式两带模型的结构性定理——互补带求和规则与标架类的闭式陈数

承接 §四十三（§2.43）：`∯` 化为 **`z₀⁻¹z₁⁻¹` 系数提取器**后，本节把该闭式求值与**两带模型**
的代数结构对接，闭合三条**结构性定理**（paper14 G3 的模型层）。

### 44.1 证明路线

1. **互补带求和规则（主定理）** `berryCurvature_add_complement`：对任意投影 `P` 与其补
   `Q = 1 − P`（空带/导带投影），取互补切向量 `−A, −B`，则 `F_P + F_Q = 0`——两带 Berry
   曲率**逐点相消**。证明只用 `Tr([A,B]) = 0`（迹循环性）与 `[−A,−B] = [A,B]`，**无需**幂等
   性或厄米性。积分层推论 `chernIntegralTorus_berryCurvature_add_complement`：
   `C_occ + C_empty = 0`——两带模型的总陈数荷守恒（连续层对偶 §2.9 的秩守恒）。
2. **平带类（常值投影/零切向量）** `berryCurvature_eq_zero_of_flat`：`A = B = 0 ⟹ F = 0`
   （⇒ `∯F = 0`，`chernIntegralTorus_flat_eq_zero`）——切向量恒零的平带/平凡标架类陈数为零。
3. **标架类的闭式陈数（§2.43 应用）** `chernIntegralTorus_laurentPoly`：若曲率密度 `F` 在环面
   复坐标下为 Laurent 多项式 `∑_{(m,n)∈s} c_{mn} z₀^m z₁^n`，则 `∯F = (2πi)²·c_{-1,-1}`；
   特别地，**无 `z₀⁻¹z₁⁻¹` 项**（`(-1,-1) ∉ s`）时 `∯F = 0`
   （`chernIntegralTorus_laurentPoly_eq_zero`）——即**标架类（无该极点项）⟹ C = 0**。

### 44.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `berryCurvature_neg_neg` | `F(P,−A,−B) = F(P,A,B)`（`[−A,−B]=[A,B]`） | `noncomm_ring` |
| `berryCurvature_add_complement` | **互补带求和规则** `F_P + F_Q = 0` | 迹循环性 `trace_mul_comm` |
| `chernIntegralTorus_berryCurvature_add_complement` | 积分层 `C_occ + C_empty = 0` | `torusIntegral_add` + §2.42 可积性 |
| `berryCurvature_eq_zero_of_flat` | 平带 `F(P,0,0) = 0` | `simp [berryCurvature]` |
| `chernIntegralTorus_flat_eq_zero` | 平带类 `∯F = 0` | 逐点消零 + `torusIntegral` |
| `chernIntegralTorus_laurentPoly` | **标架类闭式陈数** `∯F = (2πi)²·c_{-1,-1}` | §2.43 `torusIntegral_dim2_laurentPoly` |
| `chernIntegralTorus_laurentPoly_eq_zero` | **无 `z₀⁻¹z₁⁻¹` 项 ⟹ C = 0** | §2.43 分类 + `Finset.sum_eq_zero` |

### 44.3 诚实边界

本节闭合**互补带求和规则**、**平带类 C = 0** 与**标架类（Laurent 多项式层）的闭式陈数**。
**仍开放**：① 物理陈数 `C = (1/2π)∫ F d²k` 用 **BZ 测度 `d²k`**（非本文的复围道测度 `d²z`）
——「全局标架 ⟹ C = 0」的 **Stokes 论证**（`∫∫(∂₀A₁ − ∂₁A₀) d²k = 0`）需 BZ 测度积分基建，
登记开放；② 一般两带模型（含根式分母的 `F`）的非零陈数显式值与整性（§3 #1）。

### 44.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化：零 error、零 warning
- [x] `lake build` 全库零 error、零 `sorry`、零 `admit`
- [x] 新增 7 定理：`berryCurvature_neg_neg`/`berryCurvature_add_complement`/
  `chernIntegralTorus_berryCurvature_add_complement`/`berryCurvature_eq_zero_of_flat`/
  `chernIntegralTorus_flat_eq_zero`/`chernIntegralTorus_laurentPoly`/
  `chernIntegralTorus_laurentPoly_eq_zero`

## 四十五、BerryChern §2.45：布里渊区测度层——Fourier 系数提取、Stokes 论证与 Jacobi 字典

承接 §四十四（§2.44）的诚实边界开放项 ①：物理陈数 `C = (1/2π)∫_{BZ} F d²k` 用的是
**布里渊区测度 `d²k = dk₀dk₁`**（而非 §2.43 的**复围道测度 `d²z`**），「全局标架 ⟹ C = 0」
的 **Stokes 论证**需 BZ 测度积分基建。本节闭合该基建并给出四条测度层定理。

### 45.1 证明路线

1. **BZ 测度积分与物理陈数**：`bzIntegral F = ∫₀^{2π}∫₀^{2π} F dk₀dk₁`、
   `physicalChernNumber F = (2π)⁻¹·bzIntegral F`；基础线性/常值引理 `bzIntegral_zero`/
   `bzIntegral_neg`/`bzIntegral_const`（`bzIntegral_const c = (2π)²c`，`push_cast` + `ring`
   化解实→复强转）。
2. **BZ 层留数定理（Fourier 单项式，主定理）** `bzIntegral_bzFourier`：
   `∫_{BZ} e^{i(mk₀+nk₁)} d²k = (2π)²·δ_{m,0}δ_{n,0}`。一维情形
   `intervalIntegral_exp_int_mul_I`（`∫₀^{2π} e^{ink} dk = 2π·δ_{n,0}`）经
   `intervalIntegral.integral_deriv_eq_sub'`（原始函数 `e^{ink}/(in)`，`n ≠ 0`）与
   `Complex.exp_int_mul_two_pi_mul_I`（`e^{2πin} = 1`）端差相消证明；二维经 Fubini 分解
   `bzIntegral_separable`（`bzIntegral (f⊗g) = (∫f)(∫g)`，`integral_const_mul`/`integral_mul_const`）
   得到。推论 `bzIntegral_bzFourier_eq_zero`（非零频 ⟹ 0）、`bzIntegral_bzFourier_zero_zero`
   （零频 ⟹ `(2π)²`）。这与 §2.43 的**复围道留数定理** `torusIntegral_dim2_monomial`
   （唯一非零留数 `z₀⁻¹z₁⁻¹ ↦ (2πi)²`）互为**两套测度**下的平行结果。
3. **Stokes 论证（BZ 测度层）** `bzIntegral_stokes_eq_zero`：若曲率密度在 BZ 上为
   **单值联络的旋度** `F = ∂₀A₁ − ∂₁A₀`，且 `A₀, A₁` 关于对应变量 `2π`-周期、可微、
   导数可积（并满足 Fubini 交换的可积性），则 `bzIntegral F = 0`——**全局标架（单值联络）
   ⟹ 未归一化陈数为零**；推论 `physicalChernNumber_eq_zero_of_stokes` 给出 `C = 0`。
   证明：内层对 `∂₁A₀` 用 FTC（周期 ⟹ 端差为零）消去，外层经
   `intervalIntegral_intervalIntegral_swap`（Fubini）后用 FTC 消去 `∂₀A₁`。
4. **Jacobi 字典（复围道测度 `d²z` ↔ BZ 测度 `d²k`）** `torusIntegral_dim2_eq_bzIntegral`：
   `∯_{T²} F(z) d²z = ∫_{BZ} (∂z₀/∂k₀)(∂z₁/∂k₁)·F(z(k)) d²k`，其中 `zᵢ = e^{ikᵢ}`，
   Jacobi 因子 `∂zᵢ/∂kᵢ = i·zᵢ`（`circleMap_zero_one`/`deriv_circleMap_zero_one`）——把 §2.43
   的复围道积分与本节 BZ 积分**显式对接**。证明：`torusIntegral_succ` 沿第一坐标降维，
   内层 `T¹` 经 `torusIntegral_dim1` 识别为 `C(0,1)` 上的圆周积分，再展开 `circleIntegral`
   为 `[0,2π]` 上的区间积分，最后用 Fubini 把内层常数因子提出。单项式层推论
   `torusIntegral_dim2_monomial_eq_bzIntegral`：`∯_{T²} z₀^m z₁^n = −∫_{BZ} z₀^{m+1} z₁^{n+1} d²k`
   ——Jacobi 因子 `(iz₀)(iz₁) = −z₀z₁` 把 `z` 指数整体平移 `+1`，故 §2.43 的留数极点
   `(-1,-1)`（留数 `(2πi)²`）对应 BZ 层的零频 `(0,0)`（值 `(2π)²`），且 `(2πi)² = −(2π)²`，
   两套留数定理**完全一致**（`circleMap_zero_one_zpow` + `complex_I_sq` + `omega` 四分情形）。

### 45.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `bzIntegral` / `physicalChernNumber` | BZ 测度积分 / 物理陈数 `(2π)⁻¹∫F d²k` | 迭代区间积分 |
| `bzIntegral_const` | `∫_{BZ} c d²k = (2π)²c` | `integral_const` + `push_cast` + `ring` |
| `intervalIntegral_exp_int_mul_I` | **一维 BZ 留数** `∫₀^{2π}e^{ink}=2πδ_{n,0}` | FTC + `exp_int_mul_two_pi_mul_I` |
| `bzIntegral_separable` | Fubini 分解 `∫(f⊗g)=(∫f)(∫g)` | `integral_const_mul`/`integral_mul_const` |
| `bzIntegral_bzFourier` | **BZ 留数定理（主定理）** `∫e^{i(mk₀+nk₁)}=(2π)²δ_{m,0}δ_{n,0}` | `bzIntegral_separable` + 一维 |
| `bzIntegral_stokes_eq_zero` | **Stokes 论证** 单值联络 + 周期 ⟹ `∫F=0` | FTC + `intervalIntegral_intervalIntegral_swap` |
| `physicalChernNumber_eq_zero_of_stokes` | **全局标架 ⟹ C = 0** | `bzIntegral_stokes_eq_zero` |
| `torusIntegral_dim2_eq_bzIntegral` | **Jacobi 字典** `d²z` ↔ `d²k`（因子 `izᵢ`） | `torusIntegral_succ` + `torusIntegral_dim1` |
| `torusIntegral_dim2_monomial_eq_bzIntegral` | **两测度单项式一致** `∯z₀^mz₁^n=−∫z₀^{m+1}z₁^{n+1}` | §2.43 + `bzIntegral_bzFourier` + `omega` |

### 45.3 诚实边界

本节闭合 §四十四开放项 ①（BZ 测度基建 + Stokes 论证 + 两测度 Jacobi 字典）。
**仍开放**：② 一般两带模型（含根式分母的 `F`，如 `(1+2u)^{-3/2}` 型）的非零陈数显式值与
整性（§3 #1）；③ 具体模型的**数值**陈数（需本节字典 + 数值留数求值）。

### 45.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 强制重新精化（touch 触发）：零 error、零 warning
- [x] 全库零 `sorry`/`admit`（仅注释中出现 "sorry" 字样）
- [x] 新增 15 声明：`bzIntegral`/`physicalChernNumber`/`bzIntegral_zero`/`bzIntegral_neg`/
  `bzIntegral_const`/`complex_I_sq`/`intervalIntegral_exp_int_mul_I`/`bzFourier`/
  `bzIntegral_separable`/`bzIntegral_bzFourier`/`bzIntegral_bzFourier_eq_zero`/
  `bzIntegral_bzFourier_zero_zero`/`bzIntegral_stokes_eq_zero`/
  `physicalChernNumber_eq_zero_of_stokes`/`circleMap_zero_one`/`deriv_circleMap_zero_one`/
  `torusIntegral_dim2_eq_bzIntegral`/`circleMap_zero_one_zpow`/
  `torusIntegral_dim2_monomial_eq_bzIntegral`

## 四十六、BerryChern §2.46：显式两带模型——Pauli 代数核、根式分母层与可分离模型的零陈数

承接 §四十五（§2.45）的诚实边界开放项 ②（一般两带模型含**根式分母**的 `F` 的非零陈数
显式值与整性）与 ③（具体模型的**数值**陈数）。本节把 §2.44 的**结构性**结果落到
**显式模型**层，闭合「模型 → 曲率 → BZ 积分 → 陈数」的完整链条。

### 46.1 证明路线

1. **两带 Pauli 代数核**：复 Pauli 矩阵 `pauliSigmaX`/`pauliSigmaY`/`pauliSigmaZ`、
   Pauli 组合 `pauliVec d = d₀σₓ + d₁σᵧ + d₂σ_z`、复三维内积 `dot3`/叉积 `cross3`，
   以及乘法恒等式 `pauliVec_mul`（`(d·σ)(e·σ) = (d·e)·1 + i·(d×e)·σ`）、平方
   `pauliVec_sq`（`(d·σ)² = (d·d)·1`）、迹恒等式 `pauliVec_mul_trace`
   （`Tr((d·σ)(e·σ)) = 2 d·e`）、交换子 `pauliVec_commutator`
   （`[(d·σ),(e·σ)] = 2i·(d×e)·σ`），以及 `dot3_comm`/`cross3_self`/`cross3_anticomm`/
   `pauliVec_neg`/`pauliVec_trace`。
2. **两带投影与曲率闭式**：`bandProj n = ½(1 − n·σ)`（`n` 单位向量时是下能带谱投影），
   `bandProj_idempotent`（`n·n = 1 ⟹ P² = P`）/`bandProj_trace`（`Tr P = 1`）/
   `bandProj_complement`（`1 − P = bandProj(−n)`）。**曲率闭式** `berryCurvature_bandProj`：
   对切向量 `A = −½ a·σ`、`B = −½ b·σ`，`F = −i·Tr(P[A,B]) = −½ · n·(a × b)`
   ——**两带 Berry 曲率化为纯量三重积**。
3. **根式分母层（开放项 ② 的代数核）**：归一化 `n = d/s`（`s² = d·d`）时 Leibniz 展开
   给出 `∂ᵢn = (1/s)∂ᵢd + (修正)·d`。关键引理 `dot3_smul_cross3_smul`：
   `(c·d)·((c·a + q·d) × (c·b + t·d)) = c³ · d·(a × b)`——两个含 `d` 的修正项由
   纯量三重积**反对称性**（`dot3_self_cross_right`/`dot3_self_cross_left`：
   `d·(d×e) = d·(e×d) = 0`）消零。故**曲率闭式（根式分母显式）**
   `berryCurvature_normalized_d`：`F = −½·(1/s³)·d·(a × b)`，即 `F ∝ (d·d)^{−3/2}`
   ——**根式分母 `s⁻³` 显式出现，且与 Leibniz 修正项无关**。
4. **可分离模型与零陈数（开放项 ③ 的完整实例）**：显式模型
   `sepDr = (sin k₀ sin k₁, sin k₀ cos k₁, cos k₀)`（**单位向量**，`sepDr_unit`：
   `d·d = 1`），切向量 `sepAr`/`sepBr`，三重积 `sepDr_triple`：`d·(a × b) = −sin k₀`。
   代入曲率闭式得**显式曲率** `berryCurvature_sepD`：`F = ½ sin k₀`。BZ 层一维留数
   `intervalIntegral_sin_eq_zero`（`∫₀^{2π} sin = 0`，经 `intervalIntegral.integral_deriv_eq_sub'`
   与 `Real.cos` 原函数）+ 分离性 `bzIntegral_separable` 给出 `bzIntegral_separable_sin`：
   `∫_{BZ} c·sin k₀ d²k = 0`，故 `bzIntegral_berryCurvature_sepD`：未归一化陈数 = 0，
   推论 `physicalChernNumber_sepD_eq_zero`：**物理陈数 `C = 0`**——该可分离模型在 BZ 上
   **拓扑平凡**。ℝ→ℂ 桥 `dot3_ofReal`/`cross3_ofReal` + ℝ 版 `dot3r`/`cross3r`。

### 46.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `pauliVec_mul` | **Pauli 乘法恒等式** `(d·σ)(e·σ)=(d·e)1+i(d×e)·σ` | 逐元素 `fin_cases` + `ring_nf` |
| `pauliVec_sq` / `pauliVec_mul_trace` | `(d·σ)²=(d·d)1` / `Tr((d·σ)(e·σ))=2d·e` | `pauliVec_mul` + `cross3_self`/迹线性 |
| `pauliVec_commutator` | **Pauli 交换子** `[(d·σ),(e·σ)]=2i(d×e)·σ` | `pauliVec_mul` + `dot3_comm`/`cross3_anticomm` |
| `bandProj_idempotent` / `_trace` / `_complement` | 两带投影 `P=½(1−n·σ)` 幂等 / `Tr P=1` / `1−P=P(−n)` | `pauliVec_sq` + `hn` |
| `berryCurvature_bandProj` | **两带曲率闭式** `F=−½·n·(a×b)` | `pauliVec_commutator` + 迹恒等式 |
| `dot3_smul_cross3_smul` | **根式分母代数核** `(c·d)·((c·a+q·d)×(c·b+t·d))=c³·d·(a×b)` | 三重积反对称性消零 |
| `berryCurvature_normalized_d` | **归一化曲率闭式** `F=−½·s⁻³·d·(a×b)` | `berryCurvature_bandProj` + 上式 |
| `sepDr_unit` / `sepDr_triple` | 可分离模型单位性 `d·d=1` / 三重积 `d·(a×b)=−sin k₀` | 三角恒等式 + `linear_combination` |
| `berryCurvature_sepD` | **可分离模型显式曲率** `F=½ sin k₀` | 曲率闭式 + `dot3_ofReal`/`cross3_ofReal` |
| `intervalIntegral_sin_eq_zero` | 一维 BZ 正弦留数 `∫₀^{2π} sin = 0` | FTC `integral_deriv_eq_sub'` + `Real.cos` |
| `bzIntegral_separable_sin` | `∫_{BZ} c·sin k₀ d²k = 0` | `bzIntegral_separable` + 一维留数 |
| `physicalChernNumber_sepD_eq_zero` | **可分离模型物理陈数 `C = 0`** | `bzIntegral_berryCurvature_sepD` |

### 46.3 诚实边界

本节闭合 §四十五开放项 ② 的**代数核**（根式分母闭式 + Leibniz 修正消零）与开放项 ③ 的
**一个完整实例**（可分离模型 `C = 0`，全链条无 `sorry`）。**仍开放**：②′ 一般两带模型的
**非零**陈数显式值与整性——本轮数值勘查（`_model_explore6.py`/`_model_explore8.py`）表明
(i) QWZ 型模型 `d = (sin k₀, sin k₁, m + cos k₀ + cos k₁)` 的曲率分母
`(2 + m² + 2m(cos k₀+cos k₁) + 2cos k₀cos k₁)^{3/2}` **非 Laurent 且非初等**，其陈数
`C = ±1`（`−2 < m < 0` 取 `−1`，`0 < m < 2` 取 `+1`，`|m| > 2` 取 `0`）经数值积分确认但
**闭式求值需椭圆型积分或 T²→S² 度理论**；(ii) 所有由 **Laurent 多项式向量**
`u ∈ (ℂ[z^{±1}, w^{±1}])²` 生成的 rank-1 投影族（`u=(2+z,1+w)`、`(z+w,z−w)`、`(1,zw)` 等）
数值度均为 `0`——与 §2.44 的「全局标架（Laurent 层）⟹ `C = 0`」一致，说明**非零陈数必须
依赖非 Laurent 的本质奇异性/根式结构**，这为开放项 ②′ 提供了结构性判据。

### 46.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 通过（6376 jobs），本模块无新增 warning
- [x] 全库零 `sorry`/`admit`（仅注释中出现 "sorry" 字样）
- [x] 新增 41 声明：15 定义（`pauliSigmaX`/`pauliSigmaY`/`pauliSigmaZ`/`pauliVec`/`dot3`/
  `cross3`/`bandProj`/`dot3r`/`cross3r`/`sepDr`/`sepAr`/`sepBr`/`sepDc`/`sepAc`/`sepBc`）
  + 26 定理（`dot3_comm`…`physicalChernNumber_sepD_eq_zero`）

## 四十七、BerryChern §2.47：耦合两带模型的显式曲率——QWZ 型 `d = (sin k₀, sin k₁, m + cos k₀ + cos k₁)`

承接 §四十六（§2.46）的诚实边界开放项 ②′（一般两带模型含**根式分母**的 `F` 的非零陈数
显式值与整性）。§2.46 把根式分母层 `F = −½·s⁻³·d·(a × b)`（`s² = d·d`）在**抽象**层闭合，
并给出一个**单位向量**的可分离实例（`s = 1`，无根式分母）。本节把该层**实例化**到
**耦合**（非可分离、非单位）的 QWZ 型模型上——这是「模型 → 曲率 → 显式积分」链条中
「模型 → 曲率」一环在**非平凡模型**上的落地，也是开放项 ②′ 的显式被积函数。

### 47.1 证明路线

1. **QWZ 型 `d` 向量**：`qwzDr m k₀ k₁ = (sin k₀, sin k₁, m + cos k₀ + cos k₁)`，
   切向量 `qwzAr = ∂₀d = (cos k₀, 0, −sin k₀)`、`qwzBr = ∂₁d = (0, cos k₁, −sin k₁)`。
2. **归一化恒等式** `qwzDr_sq`：`d·d = (m + cos k₀ + cos k₁)² + sin²k₀ + sin²k₁`；
   等价展开 `qwzDr_sq_alt`：`d·d = 2 + m² + 2m(cos k₀ + cos k₁) + 2cos k₀cos k₁`
   ——即 §2.46 登记的**根式分母** `(2 + m² + 2m(cos k₀ + cos k₁) + 2cos k₀cos k₁)^{3/2}` 的底数。
3. **三重积** `qwzDr_triple`：`d·(∂₀d × ∂₁d) = cos k₀ + cos k₁ + m·cos k₀cos k₁`
   （由 `sin² + cos² = 1` 化简；注意此式**非纯代数**，需三角恒等式，与可分离模型的
   `−sin k₀` 不同）。
4. **显式曲率（根式分母显式）** `berryCurvature_qwz`：设 `s` 为归一化因子，则
   `F = −½·s⁻³·(cos k₀ + cos k₁ + m·cos k₀cos k₁)`；物理归一化 `qwzS m k₀ k₁ = √(d·d)`
   给出 `berryCurvature_qwz_unit`——**根式分母 `(d·d)^{−3/2}` 在耦合模型上显式出现**，
   且由 §2.46 的 `berryCurvature_normalized_d_zero`（Leibniz 修正项消零）与切向量取
   `(1/s)·∂ᵢd` 的**纯代数**计算给出，无需 `√` 的求导。
5. **平凡相与临界点的结构事实**：`qwzDr_sq_pos_of_abs_gt_two`（`|m| > 2` ⟹ `d` 处处非零，
   故 `n = d/|d|` 光滑且 `n_z` 恒同号——**平凡相**的代数前提）+ `qwzDr_zero_pi_zero`/
   `qwzDr_zero_zero_pi`（`m = 0` 时 `d` 在 `(π,0)`、`(0,π)` 处**消零**——狄拉克点/能隙闭合）。

### 47.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `qwzDr_sq` / `qwzDr_sq_alt` | 归一化恒等式 `d·d = (m+cos k₀+cos k₁)²+sin²k₀+sin²k₁` / 展开式 `= 2+m²+2m(cos k₀+cos k₁)+2cos k₀cos k₁` | 展开 + 三角恒等式 `linear_combination` |
| `qwzDr_triple` | **耦合三重积** `d·(∂₀d×∂₁d) = cos k₀+cos k₁+m·cos k₀cos k₁` | `sin²+cos²=1` 消约 |
| `qwzDr_sq_pos_of_abs_gt_two` | **平凡相非消零** `|m| > 2 ⟹ d·d > 0` | `abs_le` + 余弦界 `nlinarith` |
| `qwzDr_zero_pi_zero` / `qwzDr_zero_zero_pi` | **临界点** `m = 0` 时 `d(π,0)=0` / `d(0,π)=0` | `funext` + `fin_cases` |
| `berryCurvature_normalized_d_zero` | 根式分母层 `q=t=0` 特例 `F = −½·s⁻³·d·(a×b)` | §2.46 `berryCurvature_normalized_d` 特化 |
| `berryCurvature_qwz` | **QWZ 显式曲率（根式分母显式）** `F = −½·s⁻³·(cos k₀+cos k₁+m·cos k₀cos k₁)` | `dot3_ofReal`/`cross3_ofReal` + `qwzDr_triple` |
| `berryCurvature_qwz_unit` | **物理归一化特化** `s = √(d·d)`，`F ∝ (d·d)^{−3/2}` | `berryCurvature_qwz` 代入 `qwzS` |

### 47.3 诚实边界

本节交付开放项 ②′ 的**显式被积函数**（耦合模型的根式分母曲率）与平凡相/临界点的结构事实。
**仍开放**：QWZ 型**非零**陈数的**显式值**——该积分为
`∯ (cos k₀ + cos k₁ + m cos k₀cos k₁)/(2 + m² + 2m(cos k₀+cos k₁) + 2cos k₀cos k₁)^{3/2} d²k`，
其分母**非 Laurent 且非初等**（内层 `∫ dk₁/(a + b cos k₁)^{3/2}` 即完全椭圆积分），
闭式求值需 `T² → S²` 度理论（数值已确认 `−2 < m < 0` 取 `C = −1`、`0 < m < 2` 取 `C = +1`、
`|m| > 2` 取 `C = 0`；闭式 `C(m) = sgn(m) − ½(sgn(m+2) + sgn(m−2))`）。**可形式化路径**：
`|m| > 2` 时 `d_z` 恒同号 ⟹ `n` 落在一个半球（可缩）⟹ 陈数为零——可经 §2.45 的
**Stokes 论证** `bzIntegral_stokes_eq_zero` 与「立体角 1-形式」`αᵢ = (n₀∂ᵢn₁ − n₁∂ᵢn₀)/(1+n₂)`
（`dα = ω` 当 `n₂ ≠ −1`）落地（§四十八已交付该路径的代数核）。

### 47.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 通过（6376 jobs），本模块无新增 warning
- [x] 全库零 `sorry`/`admit`（仅注释中出现 "sorry" 字样）
- [x] 新增 16 声明：7 定义（`qwzDr`/`qwzAr`/`qwzBr`/`qwzDc`/`qwzAc`/`qwzBc`/`qwzS`）
  + 9 定理（`qwzDr_sq`…`berryCurvature_qwz_unit`）

## 四十八、BerryChern §2.48：平凡相的 Stokes 论证——立体角原函数与 QWZ 零陈数

承接 §四十七（§2.47）的诚实边界：QWZ 型模型平凡相 `|m| > 2` 的陈数应为零，其可形式化
路径是 §2.45 的 **Stokes 论证** `bzIntegral_stokes_eq_zero` 配合「立体角 1-形式」
`αᵢ = (n₀∂ᵢn₁ − n₁∂ᵢn₀)/(1+n₂)`（`dα = ω` 当 `n₂ ≠ −1`）。本节把该路径的**代数核**落地。

### 48.1 证明路线

1. **ℝ³ 向量代数**：内积对称性 `dot3r_comm`、叉积三重恒等式 `cross3r_cross_eq`、
   Lagrange 恒等式 `dot3r_cross3r_self`、正定性 `dot3r_self_eq_zero`、
   **平行引理** `eq_smul_of_cross3r_eq_zero`（`w × n = 0` 且 `n·n = 1` ⟹ `w = (n·w)·n`）
   与推论 `cross3r_cross_eq_zero`（`n ⊥ a₀, a₁` ⟹ `(a₀ × a₁) × n = 0`）。
2. **立体角原函数的系数级精确性（`dα = ω`）**：`solidAngle_primitive_core` /
   `solidAngle_primitive_exact`：`∂₀α₁ − ∂₁α₀ = n·(a₀ × a₁)`
   （`n` 单位、`aᵢ ⊥ n`、`1 + n_z ≠ 0`）。
3. **Stokes 归约**：`berryCurvatureScalar` / `berryCurvatureScalar_eq_primitive_curl`：
   两带 Berry 曲率标量 `F = −½·n·(a₀ × a₁) = −½·(∂₀α₁ − ∂₁α₀)`——即 §2.45 Stokes 论证所需的
   `F = ∂₀A₁ − ∂₁A₀` 在 `Aᵢ = −½·αᵢ` 处成立；ℝ→ℂ 桥 `berryCurvature_bandProj_ofReal`。
4. **QWZ 平凡相的单位向量与切向量**：`qwzNr`（`n = d/|d|`，单位性 `qwzNr_unit`）、
   `qwzAnr`/`qwzBnr`（真切向量 `∂ᵢn = (1/|d|)∂ᵢd − (d·∂ᵢd)/|d|³·d`，正交性
   `dot3r_qwzNr_qwzAnr`/`dot3r_qwzNr_qwzBnr`）、正则性 `qwzNz_pos`（`2 < m` ⟹ `n_z > 0`，
   故 `1 + n_z ≠ 0`——立体角原函数在 BZ 上**无 Dirac 弦**）。
   归一化三重积 `qwz_triple_normalized`：`n·(∂₀n × ∂₁n) = s⁻³·(cos k₀ + cos k₁ + m·cos k₀cos k₁)`
   （与 §2.47 `berryCurvature_qwz_unit` 一致）。
5. **QWZ 曲率的立体角归约** `qwz_curvature_eq_primitive_curl`：
   `F = −½·(∂₀α₁ − ∂₁α₀)`（QWZ 数据代入）。
6. **条件 Stokes 闭合** `physicalChernNumber_qwz_eq_zero_of_stokes`：
   若 QWZ 曲率由**单值联络** `(A₀, A₁)` 表出 `F = ∂₀A₁ − ∂₁A₀` 且满足 §2.45 的
   周期性/可微性/可积性前提，则物理陈数 `C = 0`。

### 48.2 交付定理

| 定理 | 内容 | 实现 |
| --- | --- | --- |
| `cross3r_cross_eq` | 叉积三重恒等式 `(a×b)×c = (a·c)b − (b·c)a` | `ext`/`fin_cases` + `ring` |
| `dot3r_cross3r_self` | Lagrange 恒等式 `(w×n)·(w×n) = (w·w)(n·n) − (w·n)²` | 展开 + `ring` |
| `eq_smul_of_cross3r_eq_zero` | **平行引理** `w×n=0, n·n=1 ⟹ w=(n·w)n` | Lagrange + 正定性 |
| `cross3r_cross_eq_zero` | `n⊥a₀,a₁ ⟹ (a₀×a₁)×n = 0` | 三重恒等式 + `dot3r_comm` |
| `solidAngle_primitive_core` | **立体角代数核** `2(a₀×a₁)_z/(1+n_z)+(n_x(a₀×a₁)_x+n_y(a₀×a₁)_y)/(1+n_z)² = n·(a₀×a₁)` | 平行引理 + `field_simp`/`linear_combination` |
| `solidAngle_primitive_exact` | **`dα = ω`** `∂₀α₁ − ∂₁α₀ = n·(a₀×a₁)` | `solidAnglePrimD0_sub_D1` + 代数核 |
| `berryCurvatureScalar_eq_primitive_curl` | **Stokes 归约** `F = −½·(∂₀α₁ − ∂₁α₀)` | `berryCurvatureScalar` + 精确性 |
| `berryCurvature_bandProj_ofReal` | ℝ→ℂ 桥（实标量曲率即复曲率） | `berryCurvature_bandProj` + `cross3_ofReal`/`dot3_ofReal` |
| `qwzNr_unit` / `dot3r_qwzNr_qwzAnr` / `dot3r_qwzNr_qwzBnr` | QWZ 单位向量 `\|n\|=1` / 正交性 `n·∂ᵢn = 0` | `field_simp` + `qwzSqrt_sq` |
| `qwzNz_pos` / `one_add_qwzNz_ne_zero` | **平凡相正则性** `2<m ⟹ n_z>0` / `1+n_z ≠ 0` | `div_pos` + 余弦界 |
| `dot3r_smul_cross3r_correction` | ℝ 版归一化三重积（Leibniz 修正项消零） | 展开 + `ring` |
| `qwz_triple_normalized` | **QWZ 归一化三重积** `n·(∂₀n×∂₁n) = s⁻³·(cos k₀+cos k₁+m·cos k₀cos k₁)` | 上式 + `qwzDr_triple` |
| `qwz_curvature_eq_primitive_curl` | QWZ 曲率立体角归约 `F = −½·(∂₀α₁−∂₁α₀)` | `berryCurvatureScalar_eq_primitive_curl` |
| `physicalChernNumber_qwz_eq_zero_of_stokes` | **条件 Stokes 闭合**（单值联络 ⟹ `C=0`） | §2.45 `physicalChernNumber_eq_zero_of_stokes` |

### 48.3 诚实边界

本节交付立体角原函数层的**代数核**与 QWZ 平凡相的**条件闭合**。**仍开放**：从立体角原函数
`αᵢ` 出发**构造**全局标架 `Aᵢ = −½·αᵢ` 并验证其 `2π`-周期性、可微性与可积性（即把
`physicalChernNumber_qwz_eq_zero_of_stokes` 的解析前提**无条件化**），从而给出 `2 < m` 时
`physicalChernNumber (qwzCurvature m) = 0` 的**无条件**证明（登记为下一层）；以及 `|m| < 2`
分支的非零陈数（椭圆积分 / `T²→S²` 度理论）。

### 48.4 本轮验证

- [x] `lake build MUFPFormalization.BerryChern` 编译通过（零 error、零 warning）
- [x] 全库 `lake build` 通过（6376 jobs），本模块无新增 warning
- [x] 全库零 `sorry`/`admit`（仅注释中出现 "sorry" 字样）
- [x] 新增 34 声明：10 定义（`solidAnglePrim`/`solidAnglePrimD0`/`solidAnglePrimD1`/
  `berryCurvatureScalar`/`qwzSqrt`/`qwzNr`/`qwzAnr`/`qwzBnr`/`qwzNz`/`qwzCurvature`）
  + 24 定理（`dot3r_comm`…`physicalChernNumber_qwz_eq_zero_of_stokes`）
