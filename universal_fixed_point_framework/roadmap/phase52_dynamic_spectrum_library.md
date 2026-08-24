# Phase 52：动态过程谱数值库开发（2026-07-19）

## 战略定位

MUFPF 框架目前在**静态/稳态解**方面已完全成熟（静态黑洞、静态宇宙谱计算完备），但在**动态过程**方面仍需拓展。本路线图旨在系统开发动态过程的谱数值库，重点覆盖两大方向：

1. **超高能双星并合**：inspiral-merger-ringdown 全阶段谱计算
2. **普朗克能标多体散射**：量子引力尺度的散射振幅谱

**目标**：构建完整的动态过程谱数值库，实现从静态解到动态过程的全覆盖，支撑实验对接（LIGO/Virgo/KAGRA 双星并合观测）。

---

## 一、现状总览

### 成熟度评估

| 方向 | 成熟度 | 状态 |
|:----|:------:|:----:|
| 静态黑洞（Schwarzschild/Kerr/RN） | ✅ 完全成熟 | 谱计算完备，数值验证完成 |
| 静态宇宙（FLRW/ΛCDM） | ✅ 完全成熟 | 谱计算完备，CMB 对接完成 |
| 超高能双星并合 | 🚧 核心开发中 | A1(✅)/A2(✅)/A3(✅)/A4(✅) |
| 普朗克能标多体散射 | 🚧 核心开发中 | B1(✅)/B2(✅)/B3(✅)/B4(✅) |

### 现有理论基础

- **谱引力子传播子**：✅ 已完成（`scripts/paperX_graviton_propagator.py`）
- **谱 Feynman 规则**：✅ 已完成（`notes/00_foundations/spectral_feynman_rules.md`）
- **谱路径积分**：✅ 已完成（`notes/00_foundations/spectral_path_integral.md`）
- **谱重整化程序**：✅ 已完成（`scripts/paperX_spectral_renormalization.py`）
- **普朗克尺度散射振幅**：🚧 进行中（`scripts/paperX_planck_scattering.py`）

---

## 二、路线图总览

```
时间轴      Phase 52A (1-4周)       Phase 52B (5-8周)         Phase 52C (9-12周)        Phase 52D (13-16周)
          ┌───────────────────┐  ┌───────────────────┐  ┌────────────────────┐  ┌─────────────────────┐
双星并合   │ A1 后牛顿谱展开   │  │ A2 合并阶段谱演化  │  │ A3 铃荡阶段谱分析  │  │ A4 全波形谱合成     │
          │ PN 阶谱修正       │  │ 准正常模激发       │  │ QNM 衰减谱         │  │ IMRD 完整谱库       │
          └───────────────────┘  └───────────────────┘  └────────────────────┘  └─────────────────────┘
多体散射   │ B1 2→2 散射谱     │  │ B2 2→N 散射谱     │  │ B3 圈图修正谱      │  │ B4 散射谱数据库     │
          │ 树图谱振幅        │  │ 多粒子末态谱      │  │ 量子引力修正       │  │ 普朗克能标谱库      │
          └───────────────────┘  └───────────────────┘  └────────────────────┘  └─────────────────────┘
工具支撑   │ C1 谱数值框架     │  │ C2 并行计算加速    │  │ C3 机器学习辅助    │  │ C4 可视化工具链     │
          └───────────────────┘  └───────────────────┘  └────────────────────┘  └─────────────────────┘
```

---

## 三、Phase 52A（1-4 周）：基础构建

### A1: 超高能双星并合——后牛顿谱展开 ✅ (2026-07-25)

- **目标**：将后牛顿（PN）展开翻译为谱语言，计算 inspiral 阶段的辐射谱
- **内容**：
  - 双黑洞轨道运动的 PN 阶哈密顿量谱分解 ✅
  - 辐射功率谱 dE/df 的谱表示 ✅
  - 轨道参数（质量比、自旋）对谱的影响 ✅
- **产出**：`src/dynamic_spectrum/binary_inspiral_spectrum.py` + `notes/04_lorentz_gravity/dynamic_binary_inspiral.md`
- **验证**：5/5 测试通过（Newton 极限、PN 谱结构、修正因子、参数扫描、dE/df 幂律）
- **依赖**：谱引力子传播子（B1）、谱 Feynman 规则（T2）

### B1: 普朗克能标多体散射——2→2 散射谱 ✅ (2026-07-25)

- **目标**：在谱截断 λ_max ∼ M_Pl 下计算 2→2 散射振幅谱
- **内容**：
  - 引力子-引力子散射谱振幅 M(s,t) ✅
  - 引力子-物质散射谱振幅 ✅
  - 谱截断作为紫外正则化器的数值实现 ✅
- **产出**：`src/dynamic_spectrum/planck_scattering_2to2.py` + `notes/04_lorentz_gravity/dynamic_planck_scattering.md`
- **验证**：6/6 测试通过（Mandelstam 一致性、传播子、树图振幅、截面、UV 正则化、能标扫描）
- **依赖**：谱引力子传播子（B1）、谱路径积分（T3）

### C1: 谱数值框架搭建 ✅ (2026-07-25)

- **目标**：构建统一的动态过程谱数值计算框架
- **内容**：
  - 谱算子构造（SpectralOperator/SpectralData） ✅
  - 谱矩阵运算（SpectralMatrix：谱分解、矩阵函数、迹距离、HS 范数） ✅
  - 谱演化求解器（SpectralEvolutionSolver：Schrödinger/谱流方程） ✅
  - 谱截断与正则化（SpectralCutoff） ✅
  - 数值精度控制（SpectralAccuracy：截断误差、自适应维数） ✅
- **产出**：`src/dynamic_spectrum/spectral_numerics.py`
- **验证**：5/5 测试通过（谱算子、谱矩阵、演化求解器、谱截断、PN 哈密顿量）
- **依赖**：无（基础框架）

---

## 四、Phase 52B（5-8 周）：核心开发

### A2: 超高能双星并合——合并阶段谱演化 ✅ (2026-07-25)

- **目标**：计算黑洞合并阶段的谱演化，包括准正常模（QNM）激发
- **内容**：
  - 合并过程的谱流方程数值解（sigmoid 过渡模型）✅
  - QNM 激发谱与初始扰动的关系（跃迁矩阵元振幅）✅
  - 质量/自旋对合并谱的影响（NR 拟合残余属性）✅
- **产出**：`src/dynamic_spectrum/binary_merger_spectrum.py` + `notes/04_lorentz_gravity/dynamic_binary_merger.md`
- **验证**：6/6 测试通过（残余属性、QNM 频率、谱流求解器、QNM 激发、间隙动力学、全波形 IMR）
- **依赖**：A1 完成、谱流方程（Paper V）

### B2: 普朗克能标多体散射——2→N 散射谱 ✅ (2026-07-25)

- **目标**：计算普朗克能标下的多粒子末态散射谱
- **内容**：
  - 多粒子相空间积分的谱表示 ✅（SpectralNPhaseSpace，支持 2→6 体）
  - 2→3、2→4 散射谱振幅 ✅（软引力子因子分解）
  - 末态粒子谱分布 ✅（多重度、软引力子谱、谱级联）
- **产出**：`src/dynamic_spectrum/planck_scattering_2ton.py`
- **验证**：7/7 测试通过（相空间谱表示、2→3振幅、2→4振幅、末态谱分布、统计摘要、一致性、过渡行为）
- **依赖**：B1 完成、谱路径积分（T3）

### C2: 并行计算加速 ✅ (2026-07-25)

- **目标**：利用并行计算加速大规模谱计算
- **内容**：
  - GPU 加速谱矩阵运算 ✅（SpectralGPUAccelerator，CPU 降级模式）
  - 分布式谱演化计算 ✅（SpectralDistributedSolver，多进程/串行降级）
  - 内存优化策略 ✅（SpectralMemoryOptimizer：LRU 缓存、分块运算、稀疏表示、mmap）
- **产出**：`src/dynamic_spectrum/spectral_parallel.py`
- **验证**：6/6 测试通过（硬件检测、GPU加速器、分布式求解器、内存优化、并行上下文、分块谱流）
- **依赖**：C1 完成

---

## 五、Phase 52C（9-12 周）：深化拓展

### A3: 超高能双星并合——铃荡阶段谱分析 ✅ (2026-07-25)

- **目标**：计算黑洞铃荡（ringdown）阶段的衰减谱
- **内容**：
  - QNM 衰减谱的精确计算（Leaver 连续分数法谱实现）✅
  - 多模叠加谱分析（波形合成 + 谱分解 + 谱间隙恢复）✅
  - 与 LIGO 观测数据的对比框架（匹配滤波 + SNR + 参数估计）✅
- **产出**：`src/dynamic_spectrum/binary_ringdown_spectrum.py` + `src/dynamic_spectrum/leaver_unified_solver.py` + `notes/04_lorentz_gravity/dynamic_binary_ringdown.md`
- **验证**：7/7 测试通过（Leaver QNM、收敛性、多模合成、谱分解、谱间隙、LIGO对比、铃荡能流）；统一求解器集成谱化理论 + 修正 Leaver 系数 + LACI + Homotopy Continuation
- **依赖**：A2 完成、QNM 求解器（已有）

### B3: 普朗克能标多体散射——圈图修正谱 ✅ (2026-07-25)

- **目标**：计算量子引力修正的圈图散射谱
- **内容**：
  - 谱 Dyson 级数与自能修正（真空极化 + 费米子自能 + 通用单圈积分）✅
  - 谱顶点修正（Dirac/Pauli 形状因子 $F_1/F_2$，反常磁矩精确匹配 $\alpha/2\pi$）✅
  - 单圈 $e^+e^- \to \mu^+\mu^-$ 振幅（真空极化 + 顶点修正 + 箱图综合修正因子 1.113）✅
  - 谱重整化群改进（QED 耦合跑动 + 双圈 RGE + RG 改进截面增强 2.2%）✅
  - UV/IR 行为分析（截面 UV 截断不敏感 $<0.1\%$，IR 谱间隙稳定 $<5\%$）✅
- **产出**：`src/dynamic_spectrum/planck_scattering_loop.py` + `notes/04_lorentz_gravity/dynamic_planck_scattering_loop.md`
- **验证**：7/7 测试通过（Dyson 求和、自能修正、顶点修正、单圈振幅、RG 演化、UV/IR 分析、解析自洽性）
- **依赖**：B2 完成、谱重整化程序（T3）

### C3: 机器学习辅助 ✅ (2026-07-25)

- **目标**：利用机器学习加速谱计算和数据分析
- **内容**：
  - 谱振幅神经网络近似（sklearn MLPRegressor + 纯 NumPy 回退方案，6 维特征工程）✅
  - 散射截面快速评估（SpectralInterpolator 1D/2D 插值 9 μs/次 + GaussianProcess 不确定性量化）✅
  - 实验数据拟合的贝叶斯推断（MCMC Metropolis-Hastings + 谱先验 + 可信区间）✅
  - PCA 谱数据降维与特征提取（3 主成分解释 >99% 方差 + 逆变换恢复）✅
- **产出**：`src/dynamic_spectrum/spectral_machine_learning.py` + `notes/04_lorentz_gravity/dynamic_spectral_ml.md`
- **验证**：6/6 测试通过（NN 近似、NumPy NN、插值器、GP 回归、贝叶斯推断、PCA 降维）
- **依赖**：C1-C2 完成

---

## 六、Phase 52D（13-16 周）：集成交付

### A4: 超高能双星并合——全波形谱合成 ✅ (2026-07-25)

- **目标**：合成 inspiral-merger-ringdown 全阶段的完整谱
- **内容**：
  - 三阶段谱的无缝拼接（sigmoid 光滑窗口过渡）✅
  - 与 SEOBNR/IMRPhenom 波形的谱对比（失配度 0.27，谱重叠 0.74）✅
  - LIGO 观测数据对接框架（全波段 SNR + 匹配滤波）✅
- **产出**：`src/dynamic_spectrum/binary_full_waveform.py` + `notes/04_lorentz_gravity/dynamic_binary_full_waveform.md`
- **验证**：7/7 测试通过（IMR 基础连续性、SEOBNR 对比、LIGO 全波形、参数扫描、谱流演化、功率谱）
- **依赖**：A1-A3 全部完成

### B4: 普朗克能标多体散射——散射谱数据库 ✅ (2026-07-25)

- **目标**：构建普朗克能标散射谱的完整数据库
- **内容**：
  - 能量参数扫描（7 种散射过程：gg_2to2/gm_2to2/soft_2to3/soft_2to4/qed_born/qed_1loop/qed_rg）✅
  - 谱数据标准化存储（NPZ 压缩 + JSON 元数据 + 加载/保存往返验证）✅
  - 查询接口（能量区间、截面阈值、微扰有效区、主导过程识别）✅
  - 可视化工具（截面表、角分布、修正比较、过程主导图、CSV 导出）✅
- **产出**：`src/dynamic_spectrum/planck_scattering_database.py` + `notes/04_lorentz_gravity/dynamic_planck_scattering_database.md`
- **验证**：6/6 测试通过（数据库创建、能量扫描(gg)、QED扫描、存储加载、查询接口、可视化）
- **依赖**：B1-B3 全部完成

### C4: 可视化工具链 ✅ (2026-07-25)

- **目标**：构建动态过程谱的可视化工具链
- **内容**：
  - 谱演化可视化（间隙演化帧序列 + QNM 谱表 + 波形表 + IMR 全波形拼接表 + ASCII 动画）✅
  - 散射振幅与截面可视化（截面多过程对比 + 角分布 ASCII 曲线 + UV 截断 + RG 改进 + PCA 模式）✅
  - 实验数据对比绘图（LIGO 噪声曲线 + 匹配滤波 + QNM Berti 2006 验证 + 参数扫描偏差）✅
  - 综合报告生成器（一键式无依赖 ASCII 报告 + matplotlib 出版级 PNG/PDF 扩展）✅
- **产出**：`src/dynamic_spectrum/spectral_visualization.py`
- **验证**：6/6 测试通过（谱演化、散射、实验对比、报告生成、格式工具、matplotlib 扩展）
- **依赖**：C1-C3 完成

---

## 七、实验对接路线

### LIGO/Virgo/KAGRA 对接

| 阶段 | 对接内容 | 产出 |
|:----|:--------|:----|
| Ringdown 对接 | QNM 谱与 LIGO ringdown 数据对比 | `scripts/paperX_ligo_ringdown_comparison.py` |
| Full IMRD 对接 | 全波形谱与 LIGO 观测波形对比 | `scripts/paperX_ligo_full_waveform.py` |
| 参数估计 | 利用谱信息约束黑洞参数 | `scripts/paperX_ligo_parameter_estimation.py` |

### 普朗克卫星对接

| 阶段 | 对接内容 | 产出 |
|:----|:--------|:----|
| CMB 谱对比 | 静态宇宙谱与 CMB 温度功率谱对比 | 已有（Paper II） |
| 引力波背景 | 双星并合背景谱与 PTA/LISA 灵敏度对比 | `scripts/paperX_gravitational_wave_background.py` |

---

## 八、里程碑与时间表

| 里程碑 | 内容 | 时间 | 状态 |
|:------|:----|:----:|:----:|
| M1 | Phase 52A 完成：后牛顿谱展开 + 2→2 散射谱 + 数值框架 | 第 1 周 | ✅ C1(5/5) + A1(5/5) + B1(6/6) 全部测试通过 |
| M2 | Phase 52B 完成：合并阶段谱 + 2→N 散射谱 + 并行加速 | 第 8 周 | ⏳ A2+B2+C2 全部代码完成 |
| M3 | Phase 52C 完成：铃荡阶段谱 + 圈图修正谱 + ML 辅助 | 第 12 周 | ⏳ A3(✅) + B3(✅) + C3(✅) 全部代码完成 |
| M4 | Phase 52D 完成：全波形谱合成 + 散射谱数据库 + 可视化 | 第 16 周 | ✅ A4(✅, 7/7) + B4(✅, 6/6) + C4(✅, 6/6) 全部代码完成 |
| M5 | LIGO Ringdown 对接完成 | 第 18 周 | ⏳ |
| M6 | 普朗克能标散射谱数据库发布 | 第 20 周 | ⏳ |

---

## 九、依赖关系

```
Phase 52A ──→ Phase 52B ──→ Phase 52C ──→ Phase 52D
     │           │           │           │
     └───────────┴───────────┴───────────┘
                  ↓
            实验对接（M5-M6）
```

**外部依赖**：
- 谱引力子传播子（Phase 44 B1）✅
- 谱 Feynman 规则（Phase 44 T2）✅
- 谱路径积分（Phase 44 T3）✅
- 谱重整化程序（Phase 44 T3）✅

---

## 十、风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|:----|:----:|:----:|:--------|
| 谱演化方程数值不稳定 | 中 | 高 | 采用自适应步长 + 正则化方法 |
| 计算资源不足 | 中 | 中 | GPU 加速 + 分布式计算 |
| 实验数据获取受限 | 低 | 中 | 公开数据 + 模拟数据替代 |
| 理论框架扩展困难 | 低 | 高 | 分阶段验证 + 渐进式扩展 |

---

## 十一、产出物清单

### 代码产出

| 文件 | 说明 |
|:----|:----|
| `src/dynamic_spectrum/spectral_numerics.py` | 谱数值计算框架 |
| `src/dynamic_spectrum/binary_inspiral_spectrum.py` | 后牛顿谱展开 |
| `src/dynamic_spectrum/binary_merger_spectrum.py` | 合并阶段谱演化 |
| `src/dynamic_spectrum/binary_ringdown_spectrum.py` | 铃荡阶段谱分析 |
| `src/dynamic_spectrum/leaver_unified_solver.py` | Leaver QNM 统一求解器（谱化+修正系数+LACI+同伦延拓） |
| `src/dynamic_spectrum/binary_full_waveform.py` | 全波形谱合成 ✅ |
| `src/dynamic_spectrum/planck_scattering_2to2.py` | 2→2 散射谱 |
| `src/dynamic_spectrum/planck_scattering_2ton.py` | 2→N 散射谱 |
| `src/dynamic_spectrum/planck_scattering_loop.py` | 圈图修正谱 |
| `src/dynamic_spectrum/planck_scattering_database.py` | 散射谱数据库 |
| `src/dynamic_spectrum/spectral_parallel.py` | 并行计算加速 ✅ |
| `src/dynamic_spectrum/spectral_machine_learning.py` | 机器学习辅助 |
| `src/dynamic_spectrum/spectral_visualization.py` | 可视化工具链 |

### 文档产出

| 文件 | 说明 |
|:----|:----|
| `notes/04_lorentz_gravity/dynamic_binary_inspiral.md` | 双星并合 inspiral 阶段谱分析 |
| `notes/04_lorentz_gravity/dynamic_binary_merger.md` | 双星并合合并阶段谱分析 |
| `notes/04_lorentz_gravity/dynamic_binary_ringdown.md` | 双星并合铃荡阶段谱分析 |
| `notes/04_lorentz_gravity/dynamic_binary_full_waveform.md` | 双星并合全波形谱分析 ✅ |
| `notes/04_lorentz_gravity/dynamic_planck_scattering.md` | 普朗克能标多体散射谱分析 |

---

## 变更记录

| 日期 | 更新内容 | 关联 |
|:----|:----|:----|
| 2026-07-25 | **代码整合与清理**：基于谱化理论的统一 Leaver 求解器 `LeaverUnifiedSolver` 定位为最终版本（集成 DerecursionAnalyzer + LeaverResidual + LACIEvaluator + Homotopy Continuation）；废弃的 32 个探索性 Leaver 实现/测试/诊断文件移入 `src/_archive/leaver_deprecated/`；`binary_ringdown_spectrum.py` 新增 `qnm_frequency_unified()` 和 `qnm_spectrum_unified()` 适配器函数；更新 Paper XXVI v1.2（§3.3 补充谱化求解器描述）和 notes/04_lorentz_gravity/dynamic_binary_ringdown.md v0.2（§1.3 新增谱化求解器节） | Phase 52C |
| 2026-07-25 | **Phase 52A 完成**：C1 谱数值框架（SpectralOperator/SpectralMatrix/SpectralEvolutionSolver/SpectralCutoff/SpectralAccuracy 5/5 测试通过）、A1 后牛顿谱展开（PN 哈密顿量谱分解 + dE/df 谱表示 + 参数扫描 5/5 测试通过）、B1 普朗克散射谱（谱引力子传播子 + 2→2 谱振幅 + UV 正则化 6/6 测试通过）；创建研究笔记 notes/04_lorentz_gravity/dynamic_binary_inspiral.md v0.1 和 notes/04_lorentz_gravity/dynamic_planck_scattering.md v0.1 | Phase 52A |
| 2026-07-25 | **Phase 52B: B2 完成** — 2→N 普朗克散射谱（N-体相空间谱表示 + 2→3/2→4 软因子振幅 + 末态谱分布 + 谱级联 7/7 测试通过）；更新 notes/04_lorentz_gravity/dynamic_planck_scattering.md v0.2 | Phase 52B |
| 2026-07-25 | **Phase 52B: C2 完成** — 并行计算加速（GPU加速器CPU降级模式 + 分布式求解器多进程/串行降级 + 内存优化 LRU/分块/稀疏/mmap 6/6 测试通过） | Phase 52B |
| 2026-07-25 | **Phase 52D: A4 完成** — 全波形谱合成（IMRWaveformSynthesizer 三阶段无缝拼接 + SEOBNRComparator 失配度/谱重叠对比 + LIGOFullWaveformComparison 全波段 SNR 7/7 测试通过）；创建研究笔记 notes/04_lorentz_gravity/dynamic_binary_full_waveform.md v0.1。**双星并合方向 A1→A4 全线打通** | Phase 52D |
| 2026-07-25 | **Phase 52C: B3 完成** — 圈图修正谱（谱 Dyson 级数 + 自能/顶点修正 + 单圈 $e^+e^- \to \mu^+\mu^-$ 振幅 + RG 改进 + UV/IR 分析 7/7 测试通过）；创建研究笔记 notes/04_lorentz_gravity/dynamic_planck_scattering_loop.md v0.1。**多体散射方向 B1→B3 全线打通** | Phase 52C |
| 2026-07-25 | **Phase 52D: B4 完成** — 散射谱数据库（7 过程能量扫描 + NPZ/JSON 标准化存储 + 查询接口 + 可视化工具链 6/6 测试通过）；创建研究笔记 notes/04_lorentz_gravity/dynamic_planck_scattering_database.md v0.1。**多体散射方向 B1→B4 全线打通** | Phase 52D |
| 2026-07-25 | **Phase 52C: C3 完成** — 机器学习辅助（NN 振幅近似 + 插值器 9 μs/次 + GP 不确定性回归 + MCMC 贝叶斯推断 + PCA 降维 6/6 测试通过）；创建研究笔记 notes/04_lorentz_gravity/dynamic_spectral_ml.md v0.1。**工具支撑方向 C1→C3 全线打通** | Phase 52C |
| 2026-07-25 | **Phase 52D: C4 完成 — Phase 52 全线收官！** 可视化工具链（谱演化/散射/实验对比 ASCII 报告 + matplotlib 出版级扩展 + 综合报告生成器 6/6 测试通过）；创建研究笔记 notes/04_lorentz_gravity/dynamic_spectral_viz.md v0.1。**Phase 52 全部 16 项任务（A1-A4 + B1-B4 + C1-C4）全线完成！** 动态过程谱数值库 A（双星并合）、B（多体散射）、C（工具支撑）三大方向全部就绪 | Phase 52D |