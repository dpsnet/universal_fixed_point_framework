# Phase 52：动态过程谱数值库开发（2026-07-19）

## 战略定位

UFPF 框架目前在**静态/稳态解**方面已完全成熟（静态黑洞、静态宇宙谱计算完备），但在**动态过程**方面仍需拓展。本路线图旨在系统开发动态过程的谱数值库，重点覆盖两大方向：

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
| 超高能双星并合 | ⏳ 待启动 | 理论框架已建立，数值库待开发 |
| 普朗克能标多体散射 | ⏳ 待启动 | 理论框架已建立，数值库待开发 |

### 现有理论基础

- **谱引力子传播子**：✅ 已完成（`paperX_graviton_propagator.py`）
- **谱 Feynman 规则**：✅ 已完成（`notes/00_foundations/spectral_feynman_rules.md`）
- **谱路径积分**：✅ 已完成（`notes/00_foundations/spectral_path_integral.md`）
- **谱重整化程序**：✅ 已完成（`paperX_spectral_renormalization.py`）
- **普朗克尺度散射振幅**：🚧 进行中（`paperX_planck_scattering.py`）

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

### A1: 超高能双星并合——后牛顿谱展开

- **目标**：将后牛顿（PN）展开翻译为谱语言，计算 inspiral 阶段的辐射谱
- **内容**：
  - 双黑洞轨道运动的 PN 阶哈密顿量谱分解
  - 辐射功率谱 dE/df 的谱表示
  - 轨道参数（质量比、自旋）对谱的影响
- **产出**：`src/dynamic_spectrum/binary_inspiral_spectrum.py` + `notes/dynamic_binary_inspiral.md`
- **依赖**：谱引力子传播子（B1）、谱 Feynman 规则（T2）

### B1: 普朗克能标多体散射——2→2 散射谱

- **目标**：在谱截断 λ_max ∼ M_Pl 下计算 2→2 散射振幅谱
- **内容**：
  - 引力子-引力子散射谱振幅 M(s,t)
  - 引力子-物质散射谱振幅
  - 谱截断作为紫外正则化器的数值实现
- **产出**：`src/dynamic_spectrum/planck_scattering_2to2.py` + `notes/dynamic_planck_scattering.md`
- **依赖**：谱引力子传播子（B1）、谱路径积分（T3）

### C1: 谱数值框架搭建

- **目标**：构建统一的动态过程谱数值计算框架
- **内容**：
  - 谱矩阵运算库（稀疏矩阵、特征值求解）
  - 谱演化方程求解器（常微分方程、偏微分方程）
  - 数值精度控制与误差估计
- **产出**：`src/dynamic_spectrum/spectral_numerics.py`
- **依赖**：无（基础框架）

---

## 四、Phase 52B（5-8 周）：核心开发

### A2: 超高能双星并合——合并阶段谱演化

- **目标**：计算黑洞合并阶段的谱演化，包括准正常模（QNM）激发
- **内容**：
  - 合并过程的谱流方程数值解
  - QNM 激发谱与初始扰动的关系
  - 质量/自旋对合并谱的影响
- **产出**：`src/dynamic_spectrum/binary_merger_spectrum.py` + `notes/dynamic_binary_merger.md`
- **依赖**：A1 完成、谱流方程（Paper V）

### B2: 普朗克能标多体散射——2→N 散射谱

- **目标**：计算普朗克能标下的多粒子末态散射谱
- **内容**：
  - 多粒子相空间积分的谱表示
  - 2→3、2→4 散射谱振幅
  - 末态粒子谱分布
- **产出**：`src/dynamic_spectrum/planck_scattering_2ton.py`
- **依赖**：B1 完成、谱路径积分（T3）

### C2: 并行计算加速

- **目标**：利用并行计算加速大规模谱计算
- **内容**：
  - GPU 加速谱矩阵运算
  - 分布式谱演化计算
  - 内存优化策略
- **产出**：`src/dynamic_spectrum/spectral_parallel.py`
- **依赖**：C1 完成

---

## 五、Phase 52C（9-12 周）：深化拓展

### A3: 超高能双星并合——铃荡阶段谱分析

- **目标**：计算黑洞铃荡（ringdown）阶段的衰减谱
- **内容**：
  - QNM 衰减谱的精确计算（Leaver 方法谱实现）
  - 多模叠加谱分析
  - 与 LIGO 观测数据的对比框架
- **产出**：`src/dynamic_spectrum/binary_ringdown_spectrum.py` + `notes/dynamic_binary_ringdown.md`
- **依赖**：A2 完成、QNM 求解器（已有）

### B3: 普朗克能标多体散射——圈图修正谱

- **目标**：计算量子引力修正的圈图散射谱
- **内容**：
  - 单圈修正谱振幅
  - 谱重整化群改进
  - 紫外/红外行为分析
- **产出**：`src/dynamic_spectrum/planck_scattering_loop.py`
- **依赖**：B2 完成、谱重整化程序（T3）

### C3: 机器学习辅助

- **目标**：利用机器学习加速谱计算和数据分析
- **内容**：
  - 谱振幅的神经网络近似
  - 散射截面的快速评估
  - 实验数据拟合的贝叶斯推断
- **产出**：`src/dynamic_spectrum/spectral_machine_learning.py`
- **依赖**：C1-C2 完成

---

## 六、Phase 52D（13-16 周）：集成交付

### A4: 超高能双星并合——全波形谱合成

- **目标**：合成 inspiral-merger-ringdown 全阶段的完整谱
- **内容**：
  - 三阶段谱的无缝拼接
  - 与 SEOBNR/IMRPhenom 波形的谱对比
  - LIGO 观测数据对接框架
- **产出**：`src/dynamic_spectrum/binary_full_waveform.py` + `notes/dynamic_binary_full_waveform.md`
- **依赖**：A1-A3 全部完成

### B4: 普朗克能标多体散射——散射谱数据库

- **目标**：构建普朗克能标散射谱的完整数据库
- **内容**：
  - 参数扫描（能量、质量比、自旋）
  - 谱数据标准化存储
  - 查询接口与可视化工具
- **产出**：`src/dynamic_spectrum/planck_scattering_database.py`
- **依赖**：B1-B3 全部完成

### C4: 可视化工具链

- **目标**：构建动态过程谱的可视化工具链
- **内容**：
  - 谱演化动画
  - 散射振幅可视化
  - 实验数据对比绘图
- **产出**：`src/dynamic_spectrum/spectral_visualization.py`
- **依赖**：C1-C3 完成

---

## 七、实验对接路线

### LIGO/Virgo/KAGRA 对接

| 阶段 | 对接内容 | 产出 |
|:----|:--------|:----|
| Ringdown 对接 | QNM 谱与 LIGO ringdown 数据对比 | `paperX_ligo_ringdown_comparison.py` |
| Full IMRD 对接 | 全波形谱与 LIGO 观测波形对比 | `paperX_ligo_full_waveform.py` |
| 参数估计 | 利用谱信息约束黑洞参数 | `paperX_ligo_parameter_estimation.py` |

### 普朗克卫星对接

| 阶段 | 对接内容 | 产出 |
|:----|:--------|:----|
| CMB 谱对比 | 静态宇宙谱与 CMB 温度功率谱对比 | 已有（Paper II） |
| 引力波背景 | 双星并合背景谱与 PTA/LISA 灵敏度对比 | `paperX_gravitational_wave_background.py` |

---

## 八、里程碑与时间表

| 里程碑 | 内容 | 时间 | 状态 |
|:------|:----|:----:|:----:|
| M1 | Phase 52A 完成：后牛顿谱展开 + 2→2 散射谱 + 数值框架 | 第 4 周 | ⏳ |
| M2 | Phase 52B 完成：合并阶段谱 + 2→N 散射谱 + 并行加速 | 第 8 周 | ⏳ |
| M3 | Phase 52C 完成：铃荡阶段谱 + 圈图修正谱 + ML 辅助 | 第 12 周 | ⏳ |
| M4 | Phase 52D 完成：全波形谱合成 + 散射谱数据库 + 可视化 | 第 16 周 | ⏳ |
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
| `src/dynamic_spectrum/binary_full_waveform.py` | 全波形谱合成 |
| `src/dynamic_spectrum/planck_scattering_2to2.py` | 2→2 散射谱 |
| `src/dynamic_spectrum/planck_scattering_2ton.py` | 2→N 散射谱 |
| `src/dynamic_spectrum/planck_scattering_loop.py` | 圈图修正谱 |
| `src/dynamic_spectrum/planck_scattering_database.py` | 散射谱数据库 |
| `src/dynamic_spectrum/spectral_parallel.py` | 并行计算加速 |
| `src/dynamic_spectrum/spectral_machine_learning.py` | 机器学习辅助 |
| `src/dynamic_spectrum/spectral_visualization.py` | 可视化工具链 |

### 文档产出

| 文件 | 说明 |
|:----|:----|
| `notes/dynamic_binary_inspiral.md` | 双星并合 inspiral 阶段谱分析 |
| `notes/dynamic_binary_merger.md` | 双星并合合并阶段谱分析 |
| `notes/dynamic_binary_ringdown.md` | 双星并合铃荡阶段谱分析 |
| `notes/dynamic_binary_full_waveform.md` | 双星并合全波形谱分析 |
| `notes/dynamic_planck_scattering.md` | 普朗克能标多体散射谱分析 |

---

## 变更记录

| 日期 | 更新内容 | 关联 |
|:----|:----|:----|
| 2026-07-19 | 创建 Phase 52：动态过程谱数值库开发路线图 | 框架成熟度推进 |