# Phase 99：LAMOST SNR 匹配中场扩样对照（Phase 97 登记的远期项）
**关联**：Paper 48 §4.9 中场全样本段；承接 Phase 97（SDSS SNR 门槛化——SDSS 老光谱 SNR 不对称，需 SNR 匹配新观测）
**日期**：2026-10-08
**状态**：✅ 完成（含通道打通与对照执行）

## 1. 目标

Phase 97 诚实结论：SDSS 老光谱 SNR 不对称（弱场 8.2 vs 中场 16.8），有线星 d_pure 对照在 SNR≥5 下差异消失——**SDSS 全样本支持性证据降级**。本 Phase 引入 **LAMOST 光谱**（SNR 通常高于 SDSS 老光谱）做 SNR 匹配的中场/弱场对照。

## 2. 路径（按优先级）

- **P1（首选）**：Amorim 804 颗磁场白矮星与 LAMOST DR 光谱交叉匹配（VizieR LAMOST 目录或 LAMOST DR 官网）→ 获取 LAMOST 光谱 → 同管线测线级 → 对照
- **P2**：LAMOST 白矮星目录（J/A+A/708/A275，10279 行）内若含磁场测量/光谱标识则直接使用
- **P3**：4MOST 无现成数据（未来巡天）——登记远期

## 3. 判据

- 获取的 LAMOST 中场/弱场光谱 SNR 匹配（中位差 <30%）→ 有线星 d_pure 对照
- 若 SNR 匹配后中场缺失方向保持 → **SDSS 支持性证据恢复/加固**
- 若 LAMOST 命中数不足（<20 对）或 SNR 仍不匹配 → 诚实标注：数据限制，保留远期
- 诚实边界：LAMOST 覆盖/仪器差异（分辨率 R~1800 低分辨）标注

## 4. 里程碑

| # | 内容 | 产物 |
|---|---|---|
| M99-1 | LAMOST 数据可用性探查（VizieR 目录/交叉匹配） | 可用性报告 |
| M99-2 | LAMOST 光谱获取 + SNR + 线级（若可用） | `paperX_wd_linelevel_lamost.json` |
| M99-3 | SNR 匹配对照 + 落盘 v0.30 | 论文 |

## 5. 执行记录

### M99-1（✅ 2026-10-08 修正重跑）：LAMOST 可用性 + 修正坐标全量匹配
- VizieR 检索：LAMOST DR11 = **V/162**（Luo+ 2026，最新）；V/146/V/149/V/153/V/156/V/164 为旧版
- **⚠ 坐标 bug 发现与修正**：首轮匹配（`paperX_lamost_crossmatch_full.json`）与试点（`pilot.json`）基于 J 名 **RA 未 ×15 + DEC 切片错位**的错误坐标（96/142、79.2/54.5 等数字全部作废）。修正版 `parse_jname`（RA°=(hh+mm/60+ss/3600)×15、DEC 带符号、切片 [1:10]/[10:19]）后重跑全量。
- **修正后全量匹配（cone 120″，V/162 snrr 列）**：中场 **91/142（64%）**、弱场 **61/99（62%）**
- **SNR 分布（修正后）**：中场中位 **28.6**（P25 7.7/P75 58.7）、弱场 **18.4**（P25 6.0/P75 46.7）
- **对比 SDSS（Phase 97）**：中场 16.8→28.6（~1.7×）、弱场 8.2→18.4（~2.2×）；场间中位差 **55%**（SDSS 105%）——SNR 匹配度改善但幅度有限
- 数据：`paperX_lamost_crossmatch_fixed.json`（✅ 权威）；`paperX_lamost_crossmatch_full.json`/`pilot.json`（❌ 错误坐标作废留底）

### M99-2（✅ 2026-10-08 通道实际打通——此前"认证阻塞"结论被推翻）
- **关键发现：LAMOST DR11 搜索/下载 API 匿名可用**（www.lamost.org/dr11/v2.0/search 右上 Login 按钮为被动 UI；表单/查询 API 无需登录）
- 查询链路：GET search 取 csrf_token → POST `/dr11/v2.0/table/combined/q`（cone 120″、showcol=combined.obsid/planid/spid/fiberid/class/snrr/ra/dec 等，csv 输出）
- 下载链路：POST `/dr11/v2.0/spectrum/tar?type=fits` + `obsid=`（逗号分隔批量，≤10 颗/批实测）→ application/x-tar → 成员 `spec-{lmjd}-{planid}_sp{spid}-{fiberid}.fits.gz`
- FITS 解析：HDU1 COADD（WAVELENGTH/FLUX/IVAR，3906 点 3700–9093 Å）；DA 判据=Balmer 序列形态（Hβ 浅→Hε/Hζ 深）
- **全量下载：151/151 命中星光谱成功**（`scripts\_lamost_spec\`）；线级分析 151/151 关联回星（spid/fiberid int 归一匹配 planid）
- 已验证死路：dr11.lamost.org/dr8.lamost.org（502 旧服务器下线）、NADC /lamost/（404）；NADC 登录对 DR11 官网查询非必需

### M99-3（✅ 2026-10-08 对照执行 + 落盘）：SNR 匹配对照——第二仪器复现 SDSS 降级结论
- **全样本（未匹配）**：Balmer 检测 中场 47/90（52%）、弱场 27/61（44%）；Hβ d_meas 中位 中场 0.100 vs 弱场 0.133（弱场更深，方向支持缺失——但 SNR 混杂：弱场 snrr 中位 9.9 vs 中场 21.0）
- **SNR 匹配对照（weak 子样本 snrr≥21.0，n=11，实际 snrr 中位 58.5）**：五线 d_pure 中位 **weak 0.151 vs mid 0.152（比值 1.00）**，Mann-Whitney U p=0.44（无显著差异）；Hβ d_meas weak 0.076 vs mid 0.100（方向甚至反转，n 过小）
- **判定**：LAMOST 独立仪器 SNR 匹配后**中场/弱场线级差异消失**——与 Phase 97 SDSS 结论一致，**SDSS 降级结论被第二仪器复现**（非恢复）；Paper 48 观测支持性证据维持"方向性提示"地位，主证据仍为 DESI（弱场 59 d_pure 0.149 vs 中场 18 0.026）
- 诚实边界：LAMOST R~1800 低分辨、蓝端（3700–4100 Å）效率低（Hδ/Hε/Hζ 蓝端 SNR 差致高阶线测量失败率高）；Balmer 检测样本选择本身含非 DA 混杂（Amorim 目录含 DB/DQ/DC）
- 数据：`paperX_lamost_linelevel_raw.json`；结论已改写 Paper 48 §4.9（v0.30 错误数字 96/142、79.2/54.5、4.7×/6.6× 已就地修正）

### M99-4（✅ 2026-10-08 延伸复核）：反常发射线伪影辨析（顺带诚实性修正，Phase 93 §5.2 复核）
- **起因**：LAMOST 六线检测（Hβ–Hη）3 颗发射线星全部显示吸收/平 → 追查 SDSS 多历元 → 发现表 5.2 负 EW 依赖归一化口径
- **多历元**（SDSS SQL specObj 0.04° 方窗）：J233817 有 2622-54095/2628-54326×2（2004–05）+ 论文 6161-56238（2011）；J225828 有 6293-56561（论文）+ 7768-58289×2（2019）；J101712 有 6458-56274×2（论文/同板）+ 2346-53734（2004）
- **口径敏感性**：粗口径（±6/±15Å 窗）与全局 4 次多项式口径（论文口径）对同一光谱给出相反符号（LAMOST Hη 粗口径吸收 0.64/0.89 vs 多项式口径 EM −6.18）；SDSS 6161 Hη 粗口径 abs+0.4 vs 多项式口径 EM −1.06
- **原始形态终审**（±25Å 每 5Å 中值、远旁瓣 ±100–140Å 归一）：
  - LAMOST 57052（J233817，2016，0″ 匹配）：Hζ 中心 0.670 vs 旁瓣 0.77–0.88、Hη 中心 0.637 vs 旁瓣 1.07–1.21——**深吸收，非发射**
  - SDSS 6161-56238-622（2011，论文表 5.2 光谱）：Hζ 中心 0.953 vs 旁瓣 0.94–0.99、Hη 中心 1.006 vs 旁瓣 0.94–1.02——**平坦，无发射峰**
- **判定**：论文表 5.2"反常 Balmer 发射线"为**全局多项式蓝端归一化伪影**（Balmer 带密集区多项式下弯→基线抬升→假负 EW）；两仪器同现（LAMOST Hη −6.18 ≈ SDSS −5.93）印证同源伪影；"吸收→发射翻转"观测现象**撤回**。Phase 93 NMLO 线序标度 m=3.39 保留为理论框架（模型侧），"三颗星应用拟合"撤回
- **诚实边界**：J233817 2005 年 2622-54095-174 粗口径曾现 Hε/Hη 负 EW（蓝端噪声+谱带形状），同法形态复核登记为后续项；**对主结论无影响**——拓扑禁戒主证据（46.9% EW 缺失、强场 40% 无线、π/σ 终审、归因裁决）均不依赖发射线
- 落盘：Paper 48 §5.2/5.3 就地改写（v0.31）；脚本 `_phase99_emission_eta.py`/`_phase99_sdss_multi.py`/`_phase99_sdss_ew.py`/`_phase99_poly_ew.py`/`_phase99_morph.py`

## 6. 关联

- Amorim 目录 J/ApJ/944/56（804 颗，含 Sp-ID）；LAMOST DR10 MWD 目录 J/A+A/708/A275（10279 行无 B 列）
- 管线：white_dwarf_analysis_v10.py（BALMER 五线、fit_line、d_pure）
- 系统代理可用：astroquery（VizieR/SDSS）；LAMOST DR 官网需另行验证
- 用户约束：先规划再推进、逐一推进、诚实标注、稿态就地改写
