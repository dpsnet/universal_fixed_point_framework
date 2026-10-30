# 粗粒化层级读数注记（递归层计数 → 谱层参数 → 观测时间）

> 承接：`mass_time_deflection_intuition.md` L183（"粗粒化直觉→各向同性必然"）、L201（弥漫结构对外可观测效应 = 内部结构在观测层的投影/粗粒化）、L358（"物理时间 = 谱层内禀流被递归层时钟读出的宏观量……完整粗粒化链尚未形式化，登记为开放问题，不硬推"）。
> 本文把 L358 的开放问题做**语义注记**：用已机检的代数定理（保迹/各向同性/等变平均/谱流保迹/rapidity 桥）锚定三级层级，逐层给出读数语义。**代数核心已机检；"递归层计数→谱层参数"的确切映射（步数累积如何化为 rapidity）仍为开放项，诚实保留。**

---

## §0 一句话结论

时间在 MUFPF 中分三层：**递归层计数**（离散步数，静默窗口分层）→ **谱层谱流参数**（rapidity φ，可加）→ **物理层观测时间**（偏转角 θ，cosh φ = sec θ）。
"粗粒化"是**跨层读出**的机制：微观（递归/谱层）对象在更大尺度（物理观测层）下表现为整体平均效应，其代数实现是**等变平均 groupAverage**——幂等投影、保迹（读数守恒）、输出各向同性（λI）。已机检的定理把"观测 = 读出 = 等变平均"这条链的**代数骨架**钉死。

---

## §1 三级层级（定义）

| 层级 | 载体 | 参数 | 内禀语义 | 机检锚点（Lean） |
|---|---|---|---|---|
| **① 递归层** | Rec 动力学（RecObj + step + 静默窗口） | 离散步数 k ∈ ℕ | 每一次递归 = 时间递进一层；静默 = 闭合冻结 + 零测度（非丢弃）；全静默 ⟹ 恒等 | `SilenceModel.lean`：`layeredStep` / `silentStep` / `silenceRec15_layered` / `orbitCount_layered` |
| **② 谱层** | 谱流（谱参数沿流演化） | rapidity φ ∈ ℝ | 内禀流时间；φ 可加（cosh(φ₁+φ₂)）——"沿 rapidity 移动" = 在时间中移动 | `RapidityTimeLayering.lean`：`rapidity_additive` / `cosh_sq_sub_sinh_sq` / `massReadout_flow_invariant` |
| **③ 物理层** | 观测（偏转时间轴） | 偏转角 θ ∈ ℝ | 时间轴的改变；与谱层 rapidity 同构 | `rapidity_theta_identity`（sin θ = tanh φ）⟹ `gamma_cosh_sec`（cosh φ = sec θ）；`readout_frequency_redshift`（ω_lab = ω₀·cos θ） |

层级间桥：**②→③ 是 φ↔θ 同构**（同一谱流的两种表述，笔记"偏转时间轴"段）；**①→② 是递归层时钟读出谱流**（步数累积 → 内禀时间参数）——后者仍未形式化（见 §7 开放项）。

---

## §2 读出机制：观测 = 读出

L358 原表述："物理时间 = 谱层内禀流（rapidity）被递归层时钟（步数累积）读出的宏观量。"

把"读出"解释为算符作用，则观测有三个不可分离的环节：

1. **求值**：取谱层对象的宏观读数（对矩阵 = 取迹 `Matrix.trace`——质量读数的代数实现 `massInertialReadout` / `massGravitationalReadout`）。
2. **粗粒化**：对弥漫结构的全部方向/窗口平均（`groupAverage` = C₄ 等变平均）。
3. **稳定化**：要求读数在粗粒化下不变（保迹）——否则"宏观量"无定义。

机检状态：1 与 2、3 的代数均已完成；环节间的物理映射（哪些方向进平均、哪些窗口进递归层）属参数化语义，不在代数层。

---

## §3 粗粒化 = 等变平均（为什么是 groupAverage）

粗粒化直觉（用户裁定）：**微观对象在更大尺度下的整体表现、平均效应**。在矩阵实现中：

```
groupAverage T = (1/4) • Σ_{k=0..3} R_k · T · R_kᵀ
```

即对 C₄ 旋转群（弥漫结构的离散对称骨架）做**等变平均**。已机检性质：

| 性质 | 定理 | 语义 |
|---|---|---|
| 旋转不变输出 | `groupAverage_rotation_invariant_all` | 平均后不依赖方向 ⟹ 各向同性必然（L183 代数闭环） |
| 幂等投影 | `groupAverage_idempotent` | 平均是投影：二次平均 = 一次平均（粗粒化是"稳定极限"） |
| 保对称 | `groupAverage_preserves_symmetric` | 对称结构平均后仍对称 |
| **保迹** | `groupAverage_trace_eq` | **trace(gA(T)) = trace(T)：粗粒化前后宏观读数同一 = 读数守恒** |
| 群元恒等 | `groupAverage_preserves_rotation` | 旋转群元自平均不动（SO(2) 阿贝尔 ⟹ Karcher 平凡） |
| 保持谱交织 | `groupAverage_preserves_intertwine` | 平均不破坏有效谱交织（T 结构涌现且弱等效保持） |

其中**保迹**是"粗粒化 = 涌现稳定性"的代数内核：更小尺度（微观）与更大尺度（宏观）的读数由同一算符连接且数值同一——这正是"平均效应"成立的条件。

---

## §4 保迹 = 读数守恒（质量读数的跨层同一）

**定理**（`groupAverage_trace_eq`）：`trace(groupAverage T) = trace(T)`。

物理解读：设 T 为某谱层对象、trace 为质量读数（`massReadout`），则**粗粒化前后质量读数同一**。与 `massReadout_flow_invariant`（谱流保迹 = 质量谱流不动点）并列：

- `massReadout_flow_invariant`：沿**谱流**（rapidity 方向）演化，质量读数不变——**谱层内**守恒；
- `groupAverage_trace_eq`：经**等变平均**（粗粒化），质量读数不变——**跨层**守恒。

两者合流 = "质量是跨层不变式"：无论沿内禀时间演化还是跨尺度平均，宏观质量读数不变。这是"质量 = 谱间隙（paper16 定理 6.3）"在观测层的稳定性表述。

---

## §5 各向同性必然（L183 闭环）

L183 的直觉："粗粒化直觉→各向同性必然"。代数链（全部机检）：

```
groupAverage（等变平均）→ 旋转不变输出 → λI（各向同性）
```

即 `groupAverage_rotation_invariant_all` ⟹ 平均结果与旋转交换 ⟹ 对称张量 ⇒ 标量 λI。粗粒化**必然**抹平方向依赖——不是假设，是等变平均的代数推论。

---

## §6 群元恒等与 Karcher 衔接

`groupAverage_preserves_rotation`：groupAverage(rot φ) = rot φ——**旋转结构在粗粒化下不动**。

- 物理：弥漫平均不改变旋转群元（时间轴偏转结构 R(φ) 是粗粒化不动点）；
- 数学：SO(2) 阿贝尔 ⟹ C₄ 共轭平凡 ⟹ Karcher/几何平均在群元上平凡 = 恒等；
- 衔接：非群元的保正交仍需黎曼化（欧氏平均反证保正交=1.0e+00 已证必要性）——开放项。

---

## §7 三级链的代数锚点表（全文汇总）

| 链段 | 语义 | Lean 定理 | 状态 |
|---|---|---|---|
| ① 递归层时钟 | 离散步数 = 时间递进层 | `SilenceModel`（分层步进/静默/轨道计数） | ✅ 机检 |
| ①→② 层间桥 | 步数累积 → rapidity（线性：n 步 = n·Δφ） | `rotExp_nat_mul` / `rot_nat_mul`（指数律整数幂） | ✅ 代数核心闭合 |
| ② 谱流时间 | rapidity 可加、保迹 | `rapidity_additive` / `massReadout_flow_invariant` | ✅ 机检 |
| ②→③ φ↔θ | 同一谱流两表述 | `rapidity_theta_identity` / `gamma_cosh_sec` | ✅ 机检 |
| ③ 物理读出 | ω_lab = ω₀·cos θ | `readout_frequency_redshift` / `readout_sec_form` | ✅ 机检 |
| 粗粒化 | 等变平均（幂等/保对称/保迹/各向同性/群元恒等/反射湮灭/保交织） | `ForceAverageIsotropy`（groupAverage 族） | ✅ 机检 |
| 读数守恒 | trace(gA(T)) = trace(T) | `groupAverage_trace_eq` | ✅ 机检 |

---

## §8 边界与开放项（诚实保留）

1. **①→② 层间桥代数核心已闭合**（2026-10-25：#34）：`rotExp_nat_mul` / `rot_nat_mul`
   （指数律整数幂：离散 n 步复合 = 谱参数 n·θ 一步到位 ⟹ 递归层时钟读出 rapidity = 线性累积
   n·Δφ）。**仍开放**：每步 Δφ 的取值（与递归层静默窗口尺度的耦合）属模型参数，不在代数层。
2. **Karcher 黎曼化**：非群元保正交——O(2) 情形已代数闭合（#32 群元恒等 + #33 反射湮灭，
   等变平均在 O(2) 上完全刻画）；一般矩阵的流形层形式化（SO(2) 圆上 Karcher 平均）仍需
   mathlib 流形工具。
3. **参数化语义**：哪些方向/窗口进入平均、静默窗口的尺度阈值——属模型参数，不在代数层。
4. 本文为**语义注记**，非新定理；所有数学断言均指向已机检 Lean 定理，无新增证明。
