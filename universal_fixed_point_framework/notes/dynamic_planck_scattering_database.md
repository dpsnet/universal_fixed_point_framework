# 普朗克能标散射谱数据库分析

**版本**：v0.1（2026-07-25）

**摘要**：本笔记构建普朗克能标散射谱的完整数据库系统。核心成果包括：(1) 统一数据模型支持 7 种散射过程（引力子/引力子-物质/QED/软引力子），(2) 标准化 NPZ 存储与 JSON 元数据格式，(3) 多功能查询接口（能量区间、截面阈值、主导过程识别），(4) 可视化工具链（截面曲线、角分布、修正比较、过程主导图），(5) 全流程参数扫描验证（6/6 测试通过）。

---

## §1 数据库架构

### 1.1 覆盖的散射过程

数据库统一管理 B1-B3 模块的全部散射过程：

| 过程 | 枚举值 | 来源 | 公式 |
|:----|:------|:----|:----:|
| 引力子-引力子 2→2 | `gg_2to2` | B1 | $\sigma = \frac{1}{64\pi^2 s}\int |M_{\text{spec}}|^2 d\Omega$ |
| 引力子-物质 2→2 | `gm_2to2` | B1 | $\sigma = \frac{|M_{\phi h}|^2}{64\pi^2 s}$ |
| 软引力子 2→3 | `soft_2to3` | B2 | $\sigma = \kappa^2 S^{(1)} M_{2\to2}$ |
| 软引力子 2→4 | `soft_2to4` | B2 | $\sigma = \kappa^4 S^{(1)}S^{(2)} M_{2\to2}$ |
| QED Born | `qed_born` | B3 | $\sigma_0 = \frac{8\pi\alpha^2}{3s}$ |
| QED 单圈 | `qed_1loop` | B3 | $\sigma_1 = \sigma_0 \cdot |1+\delta_{\text{vp}}+\delta_{\text{vertex}}+\delta_{\text{box}}|^2$ |
| QED RG 改进 | `qed_rg` | B3 | $\sigma_{\text{RG}} = \sigma_0(\alpha \to \alpha(\sqrt{s}))$ |

### 1.2 数据模型

**EnergyScanPoint** 数据结构（每能量点 10 个字段）：

| 字段 | 类型 | 说明 |
|:----|:----:|:-----|
| E | float | 质心能（M_Pl） |
| sigma_gg_2to2 | float | 引力子-引力子截面 |
| sigma_gm_2to2 | float | 引力子-物质截面 |
| sigma_soft_2to3 | float | 2→3 截面 |
| sigma_soft_2to4 | float | 2→4 截面 |
| sigma_qed_born | float | QED Born 截面 |
| sigma_qed_1loop | float | QED 单圈截面 |
| sigma_qed_rg | float | QED RG 改进截面 |
| correction_1loop | float | 单圈修正因子 |
| amplitude | float | 引力子振幅模 |

**AngularScanPoint** 数据结构：

| 字段 | 类型 | 说明 |
|:----|:----:|:-----|
| cos_theta | float | 散射角余弦 |
| dsigma_dOmega | float | 微分散射截面 |
| amplitude | float | 振幅模 |

### 1.3 存储格式

- **NPZ 文件**: 压缩二进制存储数组数据（E, sigma_*, angular 数据）
- **JSON 元数据**: 嵌入扫描参数、物理常数、版本信息

---

## §2 能量扫描结果

### 2.1 引力子-引力子能量扫描

在 $E \in [0.01, 1.0] M_{\text{Pl}}$ 范围内扫描：

| $E \, (M_{\text{Pl}})$ | $\sigma_{gg}$ | 标度行为 |
|:--------------------:|:-------------:|:--------:|
| $0.0100$ | $1.54$ | — |
| $0.0316$ | $15.4$ | $\sim E^{2.0}$ |
| $0.1000$ | $151$ | $\sim E^{2.0}$ |
| $0.3162$ | $1264$ | $\sim E^{2.0}$ |
| $1.0000$ | $2090$ | UV 压制开始 |

截面随 $E^2$ 增长（与 $\kappa^2 s$ 标度一致），在 $E \sim M_{\text{Pl}}$ 时 UV 压制效应逐渐显现。

### 2.2 QED 过程对比

| $E \, (M_{\text{Pl}})$ | $\sigma_{\text{Born}}$ | $\sigma_{\text{1-loop}}$ | $\sigma_{\text{RG}}$ | RG/Born |
|:--------------------:|:---------------------:|:-----------------------:|:-------------------:|:-------:|
| $0.0100$ | $3.59 \times 10^3$ | $4.03 \times 10^3$ | $5.76 \times 10^3$ | 1.60 |
| $0.0585$ | $3.07$ | $3.43$ | $5.03$ | 1.64 |
| $0.3420$ | $2.63 \times 10^{-3}$ | $2.92 \times 10^{-3}$ | $4.39 \times 10^{-3}$ | 1.67 |
| $2.0000$ | $2.25 \times 10^{-6}$ | $2.48 \times 10^{-6}$ | $3.84 \times 10^{-6}$ | 1.71 |

RG 改进使截面增大 60-70%（高能 QED 跑动耦合显著增长），单圈修正稳定在 $\sim 10\%$。

---

## §3 角分布分析

以 $E = 0.1585 M_{\text{Pl}}$ 为例：

| $\cos\theta$ | $d\sigma/d\Omega$ | $|M|$ |
|:----------:|:-----------------:|:----:|
| $-0.99$ | $6.05 \times 10^4$ | $9.80 \times 10^2$ |
| $-0.71$ | $5.74 \times 10^1$ | $3.02 \times 10^1$ |
| $-0.42$ | $1.45 \times 10^1$ | $1.52 \times 10^1$ |
| $0.00$ | $8.28$ | $1.15 \times 10^1$ |
| $0.42$ | $1.45 \times 10^1$ | $1.52 \times 10^1$ |
| $0.71$ | $5.74 \times 10^1$ | $3.02 \times 10^1$ |
| $0.99$ | $6.05 \times 10^4$ | $9.80 \times 10^2$ |

角分布具有**前向/后向增强**特征（$\cos\theta \to \pm 1$ 时截面急剧增长），中间区域平坦，这是引力子交换的 $t$-道传播子增强效应。

---

## §4 过程主导图

不同能标区间的主导散射过程：

| 能量区间 $(M_{\text{Pl}})$ | 主导过程 | $\sigma\,(M_{\text{Pl}}^{-2})$ | 物理图像 |
|:------------------------:|:--------:|:----------------------------:|:--------|
| $[0.010, 0.010]$ | QED Born | $3.59 \times 10^3$ | 低能 QED 占优 |
| $[0.025, 0.025]$ | QED Born | $9.02 \times 10^1$ | 过渡区 |
| $[0.063, 0.063]$ | 引力子 2→2 | $6.10 \times 10^1$ | 引力子开始主导 |
| $[0.158, 0.398]$ | 引力子 2→2 | $3.69 \times 10^2 - 1.78 \times 10^3$ | 引力子主导 |
| $[1.000, 1.000]$ | 引力子 2→2 | $2.09 \times 10^3$ | UV 压制渐现 |

关键观察：在低能（$E \ll 0.1 M_{\text{Pl}}$）时 QED 过程占主导（电磁相互作用强于引力），而在 $E > 0.05 M_{\text{Pl}}$ 时引力子散射截面超过 QED 成为主导（$\kappa^2 s$ 标度的增长快于 $\alpha^2/s$ 标度的衰减）。

---

## §5 存储与查询接口

### 5.1 标准化存储

NPZ + JSON 双文件格式：
- `*.npz`: 压缩数值数组（能量列表、各过程截面、角分布）
- `*_meta.json`: 可读元数据（扫描参数、物理常数、版本、过程列表）

### 5.2 查询功能

| 查询方法 | 功能 | 示例 |
|:--------|:----|:-----|
| `query_energy_range(E_min, E_max)` | 能量区间过滤 | 区间 $[0.1, 0.5]$ → 3 点 |
| `query_cross_section_above(threshold, process)` | 截面阈值过滤 | $\sigma > 1.0$ → 10 点 |
| `query_correction_below(threshold)` | 微扰有效区识别 | $|\delta| < \text{threshold}$ |
| `get_dominant_process(E)` | 主导过程识别 | $E=0.6$ → gg_2to2 |

---

## §6 可视化工具

| 可视化方法 | 输出 | 用途 |
|:----------|:----|:-----|
| `plot_cross_section_vs_energy()` | 表格 | 多过程截面对比 |
| `plot_angular_distribution(E)` | 表格 | 固定能量角分布 |
| `plot_correction_comparison()` | 表格 | Born vs 1-loop vs RG |
| `plot_dominance_map()` | 表格 | 能标主导区划分 |
| `export_table(filename, format)` | CSV/TXT | 数据导出 |

---

## §7 数据库验证总结

| 测试项 | 通过 | 关键验证 |
|:------|:---:|:--------|
| 数据库创建 | ✅ | 名称、参数、元数据初始化正确 |
| 引力子能量扫描 | ✅ | 5 点扫描，截面 $\sigma \propto E^2$ 增长 |
| QED 多过程扫描 | ✅ | Born < 1-loop < RG，RG 增强 60-70% |
| 存储加载往返 | ✅ | 3 点数据 NPZ → 加载精度 $<10^{-10}$ |
| 查询接口 | ✅ | 能量区间、阈值、主导、摘要全部正确 |
| 可视化工具 | ✅ | 截面表、角分布、修正比、主导图全部可用 |

---

## §8 开放问题

1. **高维参数扫描**：当前仅实现能量扫描，需扩展到质量比、自旋参数的联合扫描
2. **时间序列数据库**：对非平衡散射过程（随时间演化的谱分布）的时间序列存储
3. **实验数据对接**：建立 LHC/未来对撞机数据的标准化导入接口
4. **实时计算引擎**：数据库驱动的在线散射振幅计算（插值加速）
5. **图形可视化**：利用 matplotlib/plotly 生成出版级图表
6. **数据库版本管理**：支持多版本谱数据的差异比较与回滚

---

## 关联文件

- `src/dynamic_spectrum/planck_scattering_database.py` — B4 实现（6/6 测试通过）
- `src/dynamic_spectrum/planck_scattering_2to2.py` — B1 2→2 散射谱
- `src/dynamic_spectrum/planck_scattering_2ton.py` — B2 2→N 散射谱
- `src/dynamic_spectrum/planck_scattering_loop.py` — B3 圈图修正谱
- `notes/dynamic_planck_scattering.md` — B1+B2 研究笔记（v0.2）
- `notes/dynamic_planck_scattering_loop.md` — B3 研究笔记（v0.1）
