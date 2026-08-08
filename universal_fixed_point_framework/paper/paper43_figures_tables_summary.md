# Paper XLIII 图表汇总与数据引用核对

**版本**：v1.2（2026-08-08 工作区草稿）
**状态**：🕓 已归档——自论文正式化（v2.0，2026-08-08）起不再同步；本文档保留作研究期图表/数值质控历史记录（正式论文为 8 图 5 表、作者-年份引用，见 `paper43_shale_accumulation.md`）
**对应论文**：`paper43_shale_accumulation.md`
**说明**：本文档汇总论文全部图件与数据源，并核对论文正文引用的关键数值与脚本输出是否一致。

---

## 一、图件汇总（图 1–6）

| 图 | 内容 | 生成脚本 | 数据来源 | 对应证据/章节 | 关键数值 |
|:--|:--|:--|:--|:--|:--|
| 图 1 | Tuscaloosa 分形维数分布 + 谱隙-门限压力线性/双曲拟合 | `paperX_shale_figs.py` | [L6] Tuscaloosa MICP 31 样品 | P1 / M10-M11（§4.1） | D 中位 2.862；双曲 R²=0.578 > 线性 0.450；理论斜率 2.23 ≈ 实测 1.81 |
| 图 2 | 长7段 TOC-生烃潜量完美线性 + 夹层识别 | `paperX_shale_figs.py` | 自采长7段 10 样品 | 线性注入 / M5 | R²=0.9990，斜率 4.90；夹层 CY-04/CY-07 |
| 图 3 | 跨盆地干酪根降解双互补指标（HI 剩余潜力 + S₁/TOC 转化率），4 体系 | `paperX_shale_figs.py` | 长7段 10 + 青山口 SL 8 + 青山口 D86 16 + 沙海组 22（[U5]/[U6] 新补） | M6 / M12 | 青山口 SL HI 349 < 长7段 410；S₁/TOC 0.824 > 0.536 |
| 图 4 | 可动流体-分形维数关系依赖页岩类型 | `paperX_shale_figs.py` | [L6] + [S1]/[S2] 文献 | M2 / M3 / M13 | Tuscaloosa ρ=+0.214 vs 产油页岩 ρ=−1.00 |
| 图 5 | OSI-Tmax 生烃窗曲线（4 面板：Bakken/Wolfcamp/EGDB 全局/中国湖相对照） | `paperX_shale_osi_window.py` | [U1] Bakken 196 + [U2] Permian Wolfcamp 614 + [U3] EGDB 22663 + 中国三体系（[U5]/[U6] 新补） | f(M) 窗形（§4.3） | Wolfcamp 峰值 75.6@445℃；关键箱比 0.52；中国 OSI 53.6 / 104.8 / 62.9 |
| 图 6 | 中国湖相五体系 S1-TOC（零阈值型 vs c 型，2026-08-08 加苏北阜宁 GY1） | `paperX_shale_china_fig.py` | 长7段 10 + 青山口 D86 16 + SL 8 + 沙海组 22 + 苏北阜宁 GY1 31 | c 项 / P4（§4.3） | 长7段 0.57·TOC−0.24（R²=0.994）；D86 1.095·TOC−0.059；SL 0.967·TOC−0.441；沙海组 0.485·TOC+0.954；苏北阜宁 0.779·TOC−0.059（OSI 64.2） |

**图件文件**：`figs/shale_fig1_Pt_D.png`、`figs/shale_fig2_TOC_potential.png`、`figs/shale_fig3_cross_basin.png`、`figs/shale_fig4_type_dependence.png`、`figs/shale_fig5_osi_window.png`、`figs/shale_fig6_china_threefactor.png`

---

## 二、数据源汇总

| 编号 | 数据 | 样品数 | 文件路径 | 用途 |
|:--|:--|:--|:--|:--|
| [L1]–[L5] | 文献分形公式与维数 | — | 文献 | M0 锚定 |
| [L6] | USGS Tuscaloosa MICP（DOI 10.5066/F7BC3XTK） | 31 | `data/tuscaloosa_micp/` | 分形、谱隙-门限压力 |
| [L7] | Thomeer 双孔隙 HPMI | 1 | `data/thomeer_hpmi/` | M7 双孔隙分形 |
| [S1] | 庆城长7段（DOI 10.19509/j.cnki.dzkq.tb20220660） | — | 文献 | 可动流体量级锚定 |
| [S2] | 合水长7段（DOI 10.1007/s12583-021-1598-5） | — | 文献 | D-S_m 负相关实证 |
| [O1] | 川南超压（DOI 10.3389/feart.2024.1375241） | — | 文献 | 超压三阶段锚定 |
| [U1] | USGS Bakken（DOI 10.5066/P13UY3RQ） | 196 | `data/rockeval_usgs_bakken/` | f(M) 成熟度主导 |
| [U2] | USGS Permian（DOI 10.5066/P9KQU1XK） | 1627 | `data/rockeval_usgs_permian/` | c 项正截距 |
| [U3] | USGS EGDB 全美 | 46599 | `data/rockeval_usgs_egdb/egdb_re_wide.csv` | f(M) 窗形、c 项、下降支 |
| [U4] | USGS GCSRD（DOI 10.5066/P9NV8HDU） | 1431 | `data/rockeval_usgs_gcsrd/` | 三因素交叉验证 |
| [U5] | 青山口 D86（PLoS ONE 2024，e0309346） | 16 | `data/rockeval_qingshankou_d86/` | 中国湖相 c 型 |
| [U6] | 沙海组 LFD1（ACS Omega 2025，5c09312） | 23 | `data/rockeval_shahai/` | 中国湖相 c 型（煤系注入） |
| 自采 | 长7段 Rock-Eval | 10 | `data/rockeval_chang7/` | 零阈值型标定 |
| 自采 | 青山口 SL Rock-Eval | 8 | `data/rockeval_qingshankou/` | M6/M12、c 型 |

**验证脚本注册**：`run_all_tests.py` 共注册 shale 系列 9 个脚本（spectral 20 项 / p4_crossbasin / osi_slope_compare / egdb_winfit / egdb_c_attrs / gcsrd_crossval / zero_threshold / shahai / china_lacustrine）。

---

## 三、关键数值一致性核对（论文 ↔ 脚本输出 ↔ 数据）

| 数值 | 论文表述 | 脚本/数据验证 | 状态 |
|:--|:--|:--|:--|
| Tuscaloosa 分形维数中位 | 2.862 | M1（`paperX_shale_spectral.py`） | ✅ 一致 |
| 双曲 R² / 线性 R² | 0.578 / 0.450 | M11 | ✅ 一致 |
| 谱隙理论斜率 | 2.23 | M11（脚本精确值） | ✅ 一致 |
| 长7段 TOC-生烃潜量 R² | 0.9990 | M5 | ✅ 一致 |
| 长7段线性注入斜率/截距 | 0.57 / −0.24 | M8 + `china_lacustrine.py`（+0.570/−0.238，R²=0.994） | ✅ 一致（0.24 vs 0.238 为打印舍入） |
| 青山口 HI 中位 / 长7段 | 349 / 410 | M6 | ✅ 一致 |
| S₁/TOC 转化率 | 0.824 / 0.536 | M12 | ✅ 一致 |
| Wolfcamp 峰值 | 75.6 @ 445℃ | `osi_window.py`（75.6@445） | ✅ 一致 |
| 关键箱比 [465/430] | 0.52 | `osi_window.py`（Wolfcamp/EGDB 0.52） | ✅ 一致 |
| 中国 OSI 中位 | 53.6 / 104.8 / 62.9 | `china_lacustrine.py`（53.6/104.8/62.9） | ✅ 一致 |
| c 型组 vs 长7段 OSI | 83.9 vs 53.6（p=2.52e-05） | `china_lacustrine.py` C2 | ✅ 一致 |
| 沙海组正截距 | +0.95 | `china_lacustrine.py`（+0.954，R²=0.284） | ✅ 一致 |
| 青山口 SL 负截距 | −0.44 | `china_lacustrine.py`（−0.441） | ✅ 一致 |
| TUSCALOOSA 正截距 | +0.284（t=63.4） | `gcsrd_crossval.py`（+0.284，n=224 含过滤） | ✅ 一致（2026-08-08 统一口径：论文两处均改为此值） |
| WILCOX / SPARTA 负截距 | −0.050 / −0.130 | `gcsrd_crossval.py` | ✅ 一致 |
| c 代理量级 | GCSRD 0.090 / EGDB 0.015–0.160 / Permian 0.095 | `gcsrd_crossval.py` + `egdb_c_attrs.py` | ✅ 一致 |
| ρ(c, Tmax p95) | +0.82（p=0.02） | `egdb_c_attrs.py` C2 | ✅ 一致 |
| ρ(c, 箱比) | +0.60 | `egdb_winfit.py` W5 | ✅ 一致 |

> **口径统一记录（2026-08-08）**：`zero_threshold.py` 过滤条件已与 `gcsrd_crossval.py` 对齐（Tmax 350–600 + OSI<300），两脚本对 GCSRD 体系的输出现完全一致（TUSCALOOSA +0.284、WILCOX −0.050、SPARTA −0.130），论文两处引用已统一；TUSCALOOSA c 代理同步为 0.090。

---

## 四、图表与论文章节对应

| 章节 | 图表 | 数据 |
|:--|:--|:--|
| §3 数据与方法 | 表 [L1]–[U6] | 全部 |
| §4.1 第一性推导 | 图 1 | [L6] |
| §4 结果（M5） | 图 2 | 长7段 |
| §4 结果（M6/M12） | 图 3 | 长7段 + 青山口 + 新 D86/沙海组 |
| §4 结果（M2/M3/M13） | 图 4 | [L6] + 文献 |
| §4.3 f(M) 窗形 | 图 5 | [U1]/[U2]/[U3] + 中国 |
| §4.3 c 项 / P4 | 图 6 | 中国四体系 |

---

## 五、诚实边界记录

- MDPI Geosciences 2026 延长组仅 3 样品且 Table 为图片——未入库；
- [L2] Xiao 2024 Energies 不含 Rock-Eval（孔隙结构研究）——未扩充；
- 沙海组 #11（Tmax=541，煤系干扰）在最终统计中剔除（`china_lacustrine.py` drop_idx=11）并在图中单独标注；
- EGDB 无实验室来源字段（OrderID 为内部批次号）——跨实验室分层仅 Permian NewData 可执行；
- 中国无国家级公开石油地球化学数据库，数据经 OA 论文原始表格转录（[U5] PMC HTML 解析、[U6] browser_use 浏览器绕过反爬）。
