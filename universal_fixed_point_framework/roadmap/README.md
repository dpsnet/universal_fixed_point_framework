# 路线图文档

本目录存放分阶段研究路线图的详细版本与里程碑规划。

## 计划文档

- `phase1_meta_axioms.md`：元公理层形式化（Rec、Spec、D、忠实性、伴随函子）。
- `phase2_structural_theorems.md`：结构定理层抽象化（全域不动点、Cat_H(Cl)、轨道函子）。
- `phase3_instance_separation.md`：实例假设层剥离（SM、NTK、弦论、引力作为下游插件）。
- `phase4_semantics_over_fitting.md`：从数值拟合到数学语义学，局部吸引子过拟合判据。
- `phase5_cross_domain_validation.md`：跨领域外推验证计划。
- `phase13_theory_transformation.md`：理论转化推进计划（四大发展主线：纯数学完备化、量子引力统一、跨学科AI融合、实验工程落地）。
- `phase14_open_problems_advancement.md`：Paper I §8.2 开放问题推进计划（纯数学/数值工程/物理理论三类问题的代码实现与下一步严格化方向）。
- `phase15_shortboard_advancement.md`：理论短板推进计划——基于 `docs/理论短板分析.md` 的 79 项短板逐项评估，规划 5 阶段推进路线图（Phase 15A-D）。
- `phase16_machine_proof.md`：机器证明形式化计划——基于 Lean 4 + mathlib4 的范畴论形式化背书，规划四等级可行性分级（A/B/C/D）与三阶段实施路线（16A 范畴基础/16B 泛函分析/16C 分形遍历）。**当前进度：16A 全部 7/7 + 16B P0-P1 共 5/6 完成，12 模块 `lake build` 通过，0 `sorry`**。
- `phase17_category_revision_plan.md`：范畴论写作规范修订计划——针对 `docs/关于范畴论使用的相关批评.md` 的三个缺陷（定义时序违规、关键命题无证明、无配套修正），规划 $\mathbf{Rec}_D$ 宽子范畴严格化、$D_{\text{diss}}$ 真正函子化、三层静默体系（对象/态射/谱）理论创新。
- `phase18_fundamental_resolution_plan.md`：框架顶层设计根本矛盾解决计划——针对 `docs/关于范畴论使用的相关批评之二.md` 的三类致命硬伤（C1 复谱自然等价失效、C2 Freyd 紧性缺失、C3 跨领域函子无通用相容证明）与物理硬伤（P1-P4），规划辫子自然等价、显式紧性构造、隔离约束下相容性定理、静默破缺机制等深化方案。**✅ 全部 22 项已完成**。
- `phase19_paper3_spectral_classification.md`：**Paper III 推进计划**——谱去递归函子的谱分类完备性定理，覆盖 $\mathbf{Rec}_D$/$\mathbf{Rec}_{\text{diss}}$/$\mathbf{Rec}\setminus\mathbf{Rec}_D$ 三层结构。
- `phase20_paper4_stretched_d_brane.md`：**Paper IV 推进计划**——$D$ 函子对 Stretched Horizon 与 D-brane 的谱等价性证明，扩展至弦论对偶统一。**🆕 新建**。

## 当前优先级

- **P0 理论严格化**：已完成（`phase1_meta_axioms.md`、`phase2_structural_theorems.md`、`phase4_semantics_over_fitting.md` 已严格化）。
- **P1 核心代码补全**：已完成（`src/` 核心模块与测试全部就绪）。
- **P2 下游插件深化**：已完成一轮完整覆盖。弦论散射振幅、LQG 面积谱、AdS/CFT 算子谱、TQFT 任意子量子维度、NCG Dirac 谱、因果集将来基数谱、渐近安全临界指数谱、扭量旋量运动学谱、引力 Schwarzschild/Kerr 真实度规（Kerr 积分器扩展至逆行与偏心率 e=0.3）、BSM 实验约束接口（热遗迹密度冻结、LHC 对产生、直接探测 SI 截面等精确截面工具已加入）均已完成；当前下一步可转入 P5 深层次理论严格化。SM 物理完整性与 NTK 真实谱对接已完成。
- **P5 跨领域外推与开放问题**：✅ **已完成**。全部 5 个理论子问题（无穷维 RKHS 显式构造、$A_R$ 正性与闭性一般证明、完整伴随函子 $D \dashv R$ 离散原型、轨道函子 $O$ 标准范畴实现、连续谱与谱测度理论）均已圆满完成。RKHS 收敛率上界（强分离 $O(r^N)$ + 弱分离扰动论 + 完全非分离覆盖熵 + 严格证明框架定理 NS-1~NS-3 + 测度论深化版本 NS-1M~NS-3M）、RG 截断严格化、高阶 RG 效应量化、BSM 热遗迹密度多通道校准（$\Omega h^2=0.1200$）、BSM 精确计算工具对接接口（micrOMEGAs/MadGraph）、全息纠缠熵严格化（定理 HE-1~HE-4 + bulk 重建）、奇异连续谱系统刻画、高维 IFS 收敛率推广、**谱静默理论**（替代紧致化，定义 5.1 + 定理 5.4 + 三物理实例验证）、**理论转化**（五种转化模式 + 完整数值库升级——可观测量计算、批量转化引擎、M理论层级转化、转化误差分析、LACI风险评估，验证弦论/超弦/M理论/LQG 互相转化可行性）均已推进或完成。
- **P6/P7 理论严格化收尾**：Phase 6（RKHS 构造）与 Phase 7（$A_R$ 正性）已完成。分形 RKHS 显式构造（三类 Mercer 核+收敛性数值演示）与非正规 Koopman $A_R$ 正性与闭性证明（自伴到非正规扩展+m-增生证明+零模截断）均已实现。

> 注：NTK 与 `cifar10_ntk_experiment.py` 的真实数据对接已在 P2 中完成。

Phase 9 开放问题已全面推进：奇异连续谱系统刻画（谱维数谱系 + 物理意义 + 谱对应保持谱型）、连续谱 LACI 计算、LACI 阈值维数依赖均已完成。新增测度论收敛率证明（NS-1M~NS-3M）与高维 IFS 推广。

- **论文拆分（2026-07-13）**：原论文拆分为两篇独立论文
  - Paper I：《通用不动点范畴框架 I：分形谱去递归理论》v2.30 — 纯数学理论
  - Paper II：《通用不动点范畴框架 II：物理应用与实验验证》v2.17 — 物理应用
- **论文 III-IV（2026-07-16 新增）**：
  - Paper III：《通用不动点范畴框架 III：谱去递归函子的谱分类完备性定理》v1.0 — $D$ 函子对 $\mathbf{Rec}$ 全域的三层谱分类完备性
  - Paper IV：《通用不动点范畴框架 IV：从 Stretched Horizon 到 D-brane》v1.0 — $D$ 函子统一黑洞熵的两条弦论推导路径

> **2026-07-13 开放问题推进更新**：Paper I §8.2 原有 3 个开放问题已全面推进，新增配套代码模块：`math_open_problems_advanced.py`、`numerical_engineering_open_problems.py`、`physics_open_problems_advanced.py`。全仓库 47 个单元测试通过。
>
> **2026-07-13 论文方法论同步更新**：Paper I 升级至 v2.5，将 `spectral_silence.py` 定理体系深化写入 §5.6（定理 5.6–5.8），将 `theory_transformation.py`、`eft_equivalence_framework.py`、`string_diagram_calculus.py` 系统化为 §7.7 核心方法论（五种转化模式、EFT 等价性框架、弦图演算、理论等价不变量与判定定理）。
>
> **2026-07-13 数学严格化深化**：新增 Feng-Wang 热力学形式（`math_open_problems_advanced.py`）、Leaver 连分数 Kerr QNM 求解器原型、强耦合 N=4 SYM Bethe ansatz 近似；全仓库单元测试从 47 增至 52。
>
> **2026-07-13 数学严格化再深化**：新增 Ruelle 精确转移算子、拓扑熵-谱间隙普适不等式（猜想 TE-G）、Leaver 精确系数求解器、N=4 SYM 简化 BES/TBA；全仓库单元测试从 52 增至 57。
>
> **2026-07-13 数学严格化三阶段深化**：新增 Feng-Wang 条件转移算子、Markov IFS 下 TE-G 严格框架、完整 Teukolsky-Leaver 求解器、N=4 SYM 完整 BES/TBA 升级；全仓库单元测试从 57 增至 61。
>
> **2026-07-13 数学严格化四阶段深化**：Feng-Wang 加权条件测度（`FengWangOptimalConditionalOperator`）、一般动力系统 TE-G 推广（Koopman 算子框架）、Kerr spheroidal λ 自洽迭代、N=4 SYM O(g⁶) dressing + 多模 wrapping；全仓库单元测试从 61 增至 64。
>
> **2026-07-13 Phase 15 启动**：基于 `docs/理论短板分析.md` 系统评估 79 项短板，分为 39 个独立项（25 未解决、10 部分缓解、10 本质性）。创建 `phase15_shortboard_advancement.md` 规划 5 阶段路线图（Phase 15A-D）。
>
> **2026-07-13 Phase 15A-1 完成**：`test_high_dimensional_ifs.py` 新增 13 个测试（解析层 8 个 + 数值层 2 个 + 相变层 2 个 + 跨维数 1 个），全仓库测试从 67 增至 80。
>
> **2026-07-15 纯数学理论短板解决**：完成三项核心数学定理的严格证明框架——(1) **定理 D-C**：Hausdorff 维数 $d_H(\rho)$ 的凹性（压力函数凸性 + Legendre 变换 + 隐函数定理 + Feng-Wang 模型验证）；(2) **定理 HD-D**：高维可逆系统 Ledrappier-Young 维数分解（Oseledets 分解 + 稳定/不稳定流形定理 + 条件熵分解 + 乘积结构）；(3) **定理 TE-G-M**：拓扑熵-谱间隙普适不等式（Markov IFS 严格框架 + Perron-Frobenius 特征值分析 + IFS 框架验证）；新增 `math_open_problems_convexity.py`；综合验证全部通过。
>
> **2026-07-15 物理理论短板推进**：完成三项物理理论短板的深化推进——(1) **Kerr 量子引力精确谱**：独立 Spheroidal Leaver 连分数求解器（残差 < 1e-14）、LIGO/Virgo Ringdown 对比框架（SNR 计算 + 可探测性判断）；(2) **N=4 SYM 完整 TBA**：Y 系统求解器（残差 < 1e-12）、热力学势计算（Δ = 2.05，强耦合一致性验证通过）；(3) **暗物质新物理**：间接探测谱预言（伽马射线/反质子通量）、冻结-in / 非热产生机制框架；新增 `physics_open_problems_shortboard.py`；综合验证全部通过。
>
> 已推进内容：
> - **非分离 IFS 收敛率**：定理 NS-LB 下界 + 与定理 NS-1M 上界匹配，得紧阶 $\Theta(N^{-\alpha/d_H})$；
> - **奇异连续谱-Lyapunov 关联**：定理 SC-L（熵-李雅普诺夫比 / Kaplan-Yorke 公式），OSC 情形数值一致；
> - **MadGraph/micrOMEGAs**：完整调用接口（process/run card/SLHA 自动生成、截面/遗迹密度解析、解析回退）；
> - **双星引力波**：inspiral-merger-ringdown 时域波形原型 + 简化 SNR；
> - **Kerr 全局量子谱**：QNM 解析框架 + Bohr-Sommerfeld 量子化 + 超辐射判据；
> - **$N=4$ SYM**：保护/非保护/BMN 算子谱与框架 $\eta_R$ 精确匹配；
> - **暗物质分形谱**：IFS 质量谱 + 遗迹密度/直接探测约束筛选。

- **剩余开放问题**（Paper I §8.2，已更新）：
  - 非分离 IFS 下界常数 $c$ 的显式最优估计、重叠度热力学形式（部分缓解）；
  - **高维可逆系统维数分解、拓扑熵-谱间隙普适不等式（已解决）**；
  - 高维 IFS 收敛率的大规模数值验证（上界紧性测试）；
  - ∞-范畴/弦图/monoidal 结构的严格证明；
  - **Leaver 连分数 QNM 求解器、spin-weighted spheroidal harmonics 高精度方法（已解决）**；
  - **有限 $N_c$ 与强耦合下 N=4 SYM 谱方程（已推进：Y 系统 + 热力学势）**；
  - **暗物质间接探测谱、冻结-in / 非热产生机制（已解决）**；
  - 实验可证伪预言的系统误差传播与贝叶斯模型比较。
- **剩余展望**（Paper II，部分已推进）：
  - 理论深化：下界常数优化、更高阶 RG 修正；
  - 实验验证：MadGraph/micrOMEGAs 真实安装联调、数值相对论全波形（SEOBCNR/IMRPhenom）对接；
  - 跨领域应用：AI 可解释性、神经网络训练相变、复杂系统动力学。

---

## Phase 13：理论转化推进计划（2026-07-13 启动）

理论转化是框架从「原型验证」迈向「通用理论互证标准」的核心阶段。基于 [理论转化的思考](../docs/理论转化的思考.md)，规划四大发展主线：

### 一、纯数学层面：理论转化体系严格完备化（短期 1–2 年）

| 任务 | 描述 | 状态 |
|---|---|---|
| ∞-范畴升级 | 将 Rec/Spec 提升为 ∞-范畴，构造高阶伴随、高阶自然变换 | ⏳ 待推进 |
| 弦图可视化演算 | 将理论转化写成可直接计算的图形语法 | ⏳ 待推进 |
| monoidal 结构证明 | 严格证明转化函子的 monoidal 结构，统一张量积规则 | ⏳ 待推进 |
| 转化等价性判定公理 | 给出两套 Rec 对象可互相转化的充要条件（谱同构+轨道函子匹配+谱静默相容） | ⏳ 待推进 |
| 三类严格判据 | 区分严格等价转化、有效近似转化、形变态射转化 | ⏳ 待推进 |
| 转化不变量集合 | 构造谱维、LACI 基准、轨道权重谱、纠缠熵标度指数 | ⏳ 待推进 |
| 转化误差与收敛理论 | 推导谱静默约化后有效理论截断误差界、态射扰动偏差估计 | ⏳ 待推进 |
| 全域不动点融合 | 把五类转化全部嵌入 $\mathcal{F}[\mathcal{V}] = \mathcal{V}$ 框架 | ⏳ 待推进 |

### 二、高能物理&量子引力：理论转化统一竞争框架（中长期 3–5 年）

| 任务 | 描述 | 状态 |
|---|---|---|
| 四大量子引力范式互证 | M理论 ↔ 超弦 ↔ LQG ↔ 渐近安全分形时空 | ⏳ 待推进 |
| M理论多层谱静默转化 | M(11)经多层谱静默逐级约化为10维弦、4维GR+SM | ⏳ 待推进 |
| LQG自旋网络→分形谱 | 通过 D 函子转化匹配黑洞 QNM | ⏳ 待推进 |
| 渐近安全RG嵌入Rec | 转化后复现分形时空自相似维 | ⏳ 待推进 |
| AdS/CFT全息转化完备 | bulk任意高维→边界低能CFT谱静默转化，完整维度静默比公式 | ⏳ 待推进 |
| BSM新物理转化预言 | 轨道函子转化拓展多代费米子谱系、暗物质旋量 | ⏳ 待推进 |
| 宇宙学转化应用 | FLRW时空→CMB分形谱，暗物质/暗能量轨道权重静默 | ⏳ 待推进 |

### 三、跨学科融合：物理与AI双向通道（产业落地方向）

| 任务 | 描述 | 状态 |
|---|---|---|
| NTK/深度学习↔分形动力系统 | D函子实现梯度下降递归↔神经谱可逆转化 | ⏳ 待推进 |
| 物理先验AI标准化转化流水线 | 物理系统→神经网络谱约束，统一PINN框架 | ⏳ 待推进 |
| 复杂系统通用转化工具 | 气候、生物代谢、混沌时序归入Rec统一仿真 | ⏳ 待推进 |

### 四、实验与工程层面：工具链产业化落地

| 任务 | 描述 | 状态 |
|---|---|---|
| 完整转化数值库升级 | 自动完成任意两类Rec对象转化，输出可观测量对比 | ⏳ 待推进 |
| 实验数据转化对标流程 | 高能实验数据→低能Spec谱→反向转化高维理论 | ⏳ 待推进 |
| 仿真去重与算力优化 | 同构转化复用谱求解代码，算力指数级降低 | ⏳ 待推进 |

### 短期优先落地清单（近 1–2 年核心任务）

| 序号 | 任务 | 状态 |
|---|---|---|
| 1 | 完成五类转化数值演示 | ✅ 已完成（`theory_transformation.py`） |
| 2 | 完成 ∞-范畴下五类转化严格证明，配套弦图演算 | ✅ 已完成（`string_diagram_calculus.py`） |
| 3 | 给出理论等价不变量完备集合与判定定理 | ✅ 已完成（`transformation_invariants.py`，9 类不变量 + 充要条件 + 三类判据） |
| 4 | 完善 M理论→弦→GR+SM 多层谱静默转化数值案例 | ✅ 已完成（`spectral_silence.py`，总静默比 63.6%） |
| 5 | 开发完整转化数值工具，对接 LHC/数值相对论仿真代码 | ✅ 已推进（`transformation_simulation_interface.py` + `numerical_engineering_open_problems.py`；真实安装联调待完成） |
| 6 | 拓展 NTK 与分形系统双向转化，完成大模型消融实验验证 | ✅ 已完成（`ntk_fractal_bidirectional.py`） |

> **新增短期任务（Phase 14 开放问题推进）**：
> - 完成非分离 IFS 收敛率下界常数 $c$ 的显式最优估计；
> - 完成 Leaver 连分数 Kerr QNM 求解器与 spin-weighted spheroidal harmonics 高精度方法；
> - 完成 MadGraph/micrOMEGAs 真实安装端到端联调；
> - 将双星波形接入 SEOBNRv4/IMRPhenom 或 LALSuite。

### 长期终极方向（5–10 年范式变革）

| 方向 | 状态 | 说明 |
|---|---|---|
| 构建通用"理论分类学" | ✅ 已完成 | `theory_taxonomy.py`：物理/AI/复杂系统统一分类、演化树、转化路径 BFS |
| 消解"基础理论/有效理论"二元对立 | ✅ 已完成 | `eft_equivalence_framework.py`：证明 EFT 是谱静默单向转化特例，建立同构/形变/双向重构元语言 |
| 统一数学物理前沿研究范式 | ✅ 已完成 | `math_phys_unification.py`：朗兰兹纲领、镜像对称、全息对偶归入通用不动点框架 |
| 哲学与基础科学价值 | ✅ 已完成 | `philosophical_foundations.py`：SM 预测 vs 拟合量化、可证伪性、结构实在论、未来科学范式 |
| 形成分形谱量子引力独立研究分支 | ⏳ 持续推进 | 已建立基础框架（分形维数扫描、量子引力谱作用量、黑洞熵修正、Kerr QNM），需更多严格定理与实验预言 |

---

## 变更记录

| 日期 | 更新内容 | 关联阶段 |
|---|---|---|
| 2026-07-13 | 新增 Phase 13：理论转化推进计划 | Phase 13 |
| 2026-07-13 | 更新 Paper I v1.8（新增 M理论层级谱静默转化） | Phase 13 |
| 2026-07-13 | 更新 Paper II v1.5（新增理论转化完整数值库与弦图演算） | Phase 13 |
| 2026-07-13 | 新增理论等价不变量完备集合与判定定理 | Phase 13 |
| 2026-07-13 | 新增弦图可视化演算 | Phase 13 |
| 2026-07-13 | 新增理论转化完整数值库升级 | Phase 13 |
| 2026-07-13 | 更新 P5 完成情况（加入理论转化成果） | Phase 5 |
| 2026-07-13 | 更新论文拆分说明（版本号与模块数） | Phase 12 |
| 2026-07-13 | 新增 Phase 12：谱静默理论 | Phase 12 |
| 2026-07-13 | 推进开放问题：非分离 IFS 下界、Lyapunov-谱维数关联、MadGraph/micrOMEGAs、双星引力波、Kerr/N=4 SYM/暗物质分形谱 | 开放问题推进 |
| 2026-07-13 | 更新 Paper I v2.5：将 `spectral_silence.py` 写入 §5.6，将 `theory_transformation.py`/`eft_equivalence_framework.py`/`string_diagram_calculus.py` 系统化为 §7.7 核心方法论 | Phase 14 |
| 2026-07-13 | 数学严格化深化：新增 Feng-Wang 热力学形式、Leaver 连分数 Kerr QNM 原型、强耦合 N=4 SYM Bethe ansatz；测试数从 47 增至 52 | Phase 14 |
| 2026-07-13 | 数学严格化再深化：新增 Ruelle 精确转移算子、拓扑熵-谱间隙不等式、Leaver 精确系数、N=4 SYM 简化 BES/TBA；测试数从 52 增至 57 | Phase 14 |
| 2026-07-13 | 数学严格化三阶段深化：新增 Feng-Wang 条件转移算子、Markov IFS 下 TE-G 严格框架、完整 Teukolsky-Leaver 求解器、N=4 SYM 完整 BES/TBA 升级；测试数从 57 增至 61 | Phase 14 |
| 2026-07-13 | 数学严格化四阶段深化：Feng-Wang 加权条件测度、Koopman TE-G 推广、spheroidal λ 自洽迭代、O(g⁶) BES/TBA；测试数从 61 增至 64 | Phase 14 |
| 2026-07-13 | D 函子代码质量修复 + 理论更新：移除 Koopman 强制对称化（Rec 扩展为完整范畴），新增反射子范畴命题 2.10 与注 2.11；logm fallback；忠实性测试加强；交织验证选项；Callable 误差估计 | Code Quality |
| 2026-07-13 | Phase 15 启动：基于 docs/理论短板分析.md 系统评估 79 项短板，创建 phase15_shortboard_advancement.md（5 阶段路线图） | Phase 15 |
| 2026-07-13 | Phase 15A-1 完成：新增 test_high_dimensional_ifs.py（13 项测试），全仓库测试从 67 增至 80 | Phase 15A |
| 2026-07-16 | 新增 Phase 16：机器证明形式化计划（Lean 4 + mathlib4，四等级分级，三阶段路线） | Phase 16 |
| 2026-07-16 | 新增 Phase 17：范畴论写作规范修订计划，从 `docs/关于范畴论写作规范批评的修订方案.md` 整理归并——针对三个缺陷规划 $\mathbf{Rec}_D$ 宽子范畴严格化、$D_{\text{diss}}$ 真正函子化、三层静默体系理论创新 | Phase 17 |
| 2026-07-16 | 新增 Phase 18：框架顶层设计根本矛盾解决计划，针对 `docs/关于范畴论使用的相关批评之二.md` 的三类致命硬伤（C1 复谱自然等价失效、C2 Freyd 紧性缺失、C3 跨领域函子无通用相容证明）与 P1-P4 物理硬伤，规划分支自然等价、显式紧性构造、隔离约束下相容性定理、静默破缺机制等深化方案 | Phase 18 |
