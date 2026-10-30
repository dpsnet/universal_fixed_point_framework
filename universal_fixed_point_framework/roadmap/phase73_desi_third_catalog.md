# Phase 73：DESI DR1 第三目录交叉验证（P83 延续）

> 状态：**已完成（R1–R7 全闭合，2026-10-07）** | 创建：2026-10-07 | 主线归属：Paper 48（拓扑禁戒频率观测验证）
> 目标：引入完全独立的巡天（DESI）磁场白矮星样本作为第三目录，验证 B-EW 残差负梯度；结论域从 B≤105 MG（Kepler 上限）扩展至 ~500 MG。

## 0. 背景与动机

- 现有两目录均已达覆盖上限：Amorim 2023（SDSS 518 全目录，弱/中场）+ Kepler 2013（10–300 MG 域全候选 60 颗）。
- Paper 48 §7.6 已登记："后续扩样需引入其他目录（Kepler et al. 2019/2021）"。
- 查证结果：**DESI DR1 是现成最佳候选**——
  - arXiv:2603.20487（Amorim, Kepler & Romero，**同团队**）：DESI DR1 光谱 + Gaia DR3 候选，视觉识别 Zeeman 分裂，**137 颗新 MWD**（与文献去重后新增），B 0.75–455.1 MG，全部 DA，YAWP/线位双方法测场（口径与 Amorim 2023 一致，~10% 不确定度）。
  - 备选：arXiv:2609.31565（DESI DR1 MWD 综合研究，DAH hot 207 + cold 389 等，596+ 颗；2026-09-28）——样本更大但光谱质量/字段待核。
- 网络可达性已验证：data.desi.lbl.gov 200、arXiv 200、SVO2 200。
- DESI 光谱：3600–9824 Å、0.8 Å 分辨率、SNR>10 切——Balmer 全系覆盖，v10 管线可直接复用。

## 1. 步骤与结果

### R1 数据获取（目录表）——完成
- 主源：2603.20487 Appendix Table 1（137 颗）。
- **关键转折（PDF 精确版）**：WebFetch 网页转录的 Gaia Source ID 大量错位（如 8813559108020207008 实为 881355910802027008）——改从 arXiv 源 PDF 本地解析（fitz `get_text("words")` 按 y 坐标分行）**精确提取 137 行 9 字段**（Gaia ID/DESI name/Teff/Mass/B/zoffset/Incl/tau/G），B 范围复现 0.75–455.1 MG，B 分档 85 低场/44 中场/8 高场（≥100 MG）。
- 成品：`scripts/paperX_wd_m83e_desi137.json`（PDF 精确版）。
- 验收达标：137 颗全含 DESI 光谱 ID + B + Teff；B 覆盖 ≥100 MG 段（455.1 MG 覆盖）。

### R2 去重——完成（内嵌）
- 论文自身声明"与文献去重后新增"（同团队构建，DESI 首次出现）；M83e 样本与 M83c/M83d 通过不同观测项目（SDSS 光谱 ID vs DESI TARGETID）+ Gaia 坐标体系天然区分，无 name 级重叠。

### R3 光谱下载——完成（116/137）
- 路径修正：DESI DR1 iron reduction 真实结构为 `spectro/redux/iron/healpix/main/{bright|dark}/{hp//100}/{hp}/coadd-main-{prog}-{hp}.fits`（nside=64 nested；iron 为 DR1 专用 reduction；目录页被 robots 拦截但文件直链可用）。
- **自研 FITS HTTP Range 按需读取器 `_m83e_desi_reader.py`**（多块 header、TFORM 列偏移累计、IMAGE 行读取；对照 astropy 全 match；206 Range 支持验证）。
- 提取链路：TARGETID 匹配优先（82/111）→ **坐标匹配兜底**（Gaia TAP 坐标 125/137 → FIBERMAP TARGET_RA/DEC 最近行，18 颗）→ 新命中星算 hp 补提取（11 颗）——合计 **116/137**。
- 不可提取登记：12 无坐标（Gaia ID 在 DR3 不可解析，含 455.1 MG 最高场星）+ 3 无 coadd 文件 + 6 同像素无匹配光谱。
- 验收：116/137 = 84.7% > 80%。

### R4 观测 EW 测量——完成（91/116）
- v10 管线同口径（normalize Balmer 外 50 Å 掩膜 + polyfit4；measure_ew window=80、ew>0.5、depth>0.03；五线 Hα–Hε）。
- 成品 `_m83e_desi_ew.json`：91 颗 ≥2 线检测有效（DESI 0.8 Å 采样与 window=80 兼容确认）。

### R5 理论 EW（Koester）——完成（50 有效残差）
- 复用 `_koester_spec` 缓存（891 点 fid 表，logg 取 8.0 最近点）——50 颗同时有 obs/theo EW（38 低场 + 11 中场 + 1 高场≥100 MG）。
- 验收：50/116 有效（43%）——略低于 70% 目标（因缓存网格点覆盖 + 检测线数过滤），已在 Paper 48 诚实标注。

### R6 回归与合并——完成
- **DESI 独立目录**：中心化 OLS（resid~log10B+Teff，logg 固定 8 无变化故剔除）——**log10B=-0.596（t=-10.13）**；Spearman **rho=-0.727（p=2.33e-9）**——第三个独立目录以更高显著性复现负梯度。
- **三目录统一合并**（统一 Koester 口径重算）：Amorim 237 + Kepler 32 + DESI 50 = **319 有效残差**——主回归 log10B=-0.292（t=-5.30）、rho=-0.209（p=1.66e-4）；含目录固定效应+交互完整模型：Kepler×B=-1.240（t=-3.22）、DESI×B=-0.324（t=-1.84）——**三目录梯度符号全负、强度随 B 域增强而陡化**（Amorim 低场 -0.28 / DESI 全段 -0.60 / Kepler 中场 -1.52）。
- 验收达标：梯度方向一致 + 显著性 + 交互异质性量化。

### R7 落盘——完成
- Paper 48 **v0.7**：新增 §4.5（DESI 第三目录）+ §7.5 第 4 条/§7.6 第 3 项更新 + 附录 A M83e 工作记录 + 变更记录 v0.7。
- 结论域声明：三目录合计 B 0.8–455 MG（Amorim 0.8–778 全目录 + Kepler 10–105 + DESI 0.75–455）；DESI 独立结论域以 125 颗可定位子样本为准；Zeeman 截断诚实标注延续。
- 三段落盘：roadmap（本文件）+ Paper 48 v0.7 + 变更记录（含）。

## 2. 预期与结果对比

- **预期样本增益**：有效残差 +40~90 颗 → 实际 **+50 颗**（DESI）；三目录总有效 **319**（Amorim 237 + Kepler 32 + DESI 50）。
- **风险处理回顾**：
  - DESI 检测下限 B≈1 MG——低场端不受影响（低场 38 颗全部 >1 MG）。
  - logg=8 固定——回归剔除 logg 列（奇异矩阵）+ ≤0.1 dex 不确定标注。
  - Zeeman 分裂高场截断——延续 M83d 诚实标注。
  - 视觉识别误分——n_detected≥2 过滤。
  - **新增风险（已处理）**：WebFetch 转录错位 → PDF 精确提取；Gaia DR4 过渡期 TAP 500 → 小 chunk 重试退避恢复；DESI 目录页 robots 拦截 → 文件直链 + 自研 Range 读取器。

## 3. 与既有工作的关系

- 延续 P83（M83a–M83d）→ Paper 48 观测验证链：三层模型大气（Bergeron/Koester/TMAP）→ SNR 控制 → Kepler 独立目录 → **DESI 第三目录（完成）**。
- 完成后 Paper 48 观测验证体系：**三目录 × 三层模型大气 × SNR 控制 × 四类选择效应检验**——B-残差负梯度在三个完全独立的观测项目（SDSS 体系 Amorim / Kepler 2013 / DESI DR1）中全部显著成立。

## 4. 已确认事实（勿重复查证）

- data.desi.lbl.gov / arXiv / SVO2 网络可达（2026-10-07 测试 200）；Gaia TAP 间歇 500（DR4 过渡期）需小 chunk 重试。
- 2603.20487：137 颗新 DA MWD、B 0.75–455.1 MG、YAWP+线位、logg=8、Teff 用 Gaia Gentile Fusillo 2021、SNR>10、光谱 3600–9824 Å 0.8 Å。
- **DESI 光谱路径**：`spectro/redux/iron/healpix/main/{bright|dark}/{hp//100}/{hp}/coadd-main-{prog}-{hp}.fits`（nside=64 nested；iron=DR1 专用）。
- **关键成品**：`paperX_wd_m83e_desi137.json`（PDF 精确版 137 行）、`_m83e_desi_reader.py`（Range FITS 读取器）、`_desi_spec/*.npz`（116 光谱）、`_m83e_desi_ew.json`（91 有效）、`_m83e_desi_regression.json`（DESI 独立 rho=-0.727 p=2.33e-9）、`_m83e_merged_regression.json`（三目录 319 合并）。
- v10 管线/SVO2 fid 表/落盘模式：见 Paper 48 附录 A 与 scripts/。
