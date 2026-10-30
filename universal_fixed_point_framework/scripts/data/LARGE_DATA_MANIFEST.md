# 大文件数据清单（LARGE DATA MANIFEST）

> 本清单记录 2026-10-30 历史重写时从 git 移除的 7 个 >50MB 文件。
> 这些文件**仍在本地工作区保留**（已从对象库完整恢复，字节数与原 blob 一致），
> 仅**解除 git 跟踪**（见 .gitignore「大文件保护」段）。如需在新机器上重建，按下述来源重新生成或下载。

## 一、4 个 USGS 公开数据 CSV（可重新下载）

| 文件 | 大小 | 性质 | 来源 |
|---|---|---|---|
| `scripts/data/rockeval_usgs_egdb/csv/EnergyGeoChemDB_csv/Analysis_AA-BJ.csv` | 97.7 MB | USGS EGDB 原始分析数据（RockEval 热解），按 OrderID 分区 AA–BJ99 | 见下 |
| `scripts/data/rockeval_usgs_egdb/csv/EnergyGeoChemDB_csv/Analysis_BK-ERP-00063.csv` | 97.0 MB | 同上，OrderID BK–ERP-00063 | 见下 |
| `scripts/data/rockeval_usgs_egdb/csv/EnergyGeoChemDB_csv/Analysis_00003-99043.csv` | 76.9 MB | 同上，OrderID 0003–99043 | 见下 |
| `scripts/data/rockeval_usgs_egdb/csv/EnergyGeoChemDB_csv/Analysis_ERP-00064-X1812.csv` | 60.3 MB | 同上，OrderID ERP-00064–X1812 | 见下 |

**官方来源**
- 数据发布：USGS《Energy Geochemistry Database (ver. 2.0, September 2026)》
- DOI：`10.5066/P1WNUHWO` → https://doi.org/10.5066/P1WNUHWO
- ScienceBase 条目：https://www.sciencebase.gov/catalog/item/68a8a28fd4be026335793f26
- 附件：**EnergyGeoChemDB-CSV Files.zip（约 33 MB）**，内含 Analysis 分区 CSV、Samples.csv 与 README
- 许可：CC0 1.0（公共领域）；更新记录见「USGS_Energy Geochmistry Database Revision History.txt」

**版本差异（重要）**：USGS 在 ver 2.0（2026-09 修订）对 Analysis 表**重新分区**——
官方 zip 当前为 **5 个 `Analysis_OrderIDs *.csv`**（107.6/108.6/93.8/75.7/66.4 MB），
本地保留的旧 4 文件是 **ver 1.x 分区**（76.9/97.7/97.0/60.3 MB）。两版同源同库
（3,619,149 条分析记录，仅 OrderID 切片边界不同），任选其一即可满足数据需求；
本地恢复文件保留旧名以匹配历史语义，若需官方最新分区直接运行下载脚本即可。

**自动下载脚本（已入库，git 跟踪）**
```powershell
D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\fetch_usgs_egdb_csv.py
```
- 脚本通过 ScienceBase catalog API 动态解析 zip 直链（版本更新后仍可用），下载并解压到
  `scripts/data/rockeval_usgs_egdb/csv/`（剥离 zip 内子目录），随后校验 Samples.csv 与
  Analysis 分区文件（动态匹配当前版文件名，不绑定旧名）。
- 已实测（2026-10-30）：33.3 MB zip 下载 → 解压出 5 个 `Analysis_OrderIDs *.csv` + Samples.csv，exit 0。

## 二、3 个数值脚本运行缓存（可重新生成）

| 文件 | 大小 | 生成脚本（均已入库） | 生成方式 |
|---|---|---|---|
| `scripts/cache_n11_5seed.pkl` | 78.3 MB | `scripts/paperX_n11_fill45.py` | 5 seed × 20000 采样（n=11），保存 pickle 缓存供复用 |
| `scripts/cache_n11_3x80000.pkl` | 187.7 MB | `scripts/paperX_n11_fill46_80000.py` | 复用 5seed 前 20000 → 77/331/777 续采 60000（累积 80000）后保存 |
| `scripts/cache_n10_3x80000.pkl` | 141.5 MB | `scripts/paperX_n10_audit59_80000.py` | 77/331/777 × 80000（n=10，165 因子），缓存存在则读、否则重采并保存 |

**再生成命令**（数值脚本统一用 pyenv Python，勿用裸 python）
```powershell
# 按依赖顺序：先 5seed，再 3x80000（n11），n10 独立可并行
D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\paperX_n11_fill45.py
D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\paperX_n11_fill46_80000.py
D:\pyenv\pyenv-win\versions\3.11.8\python.exe scripts\paperX_n10_audit59_80000.py
```
- 三个脚本均具备「缓存存在则加载」逻辑（`pickle.load`），再生成会覆盖本地缺失的 pkl。
- 注意：80000 级采样耗时较长（数十分钟级），非必要不必重跑；本地已有恢复的缓存文件可直接复用。
- 引用这些缓存的衍生脚本（`paperX_n11_audit46_80000.py`、`paperX_n11_crossset_audit50.py`、`paperX_n11_m30*` 等）在缓存缺失时会报错，先按上述命令补齐即可。

## 三、为何不入库（防复发约束）

- 3 个 pkl 为**运行缓存**：内容可由脚本确定性重生成，入库存放数百 MB 属于冗余。
- 4 个 CSV 为**第三方公开数据**：CC0 许可可从官方重下载；且超出 GitHub 100 MB 单文件硬限（
  179/141 MB 两个 pkl 曾触发 GH001 拒绝），git 仓库不适于托管。
- 防复发规则已写入 `.gitignore`（见「大文件保护」段）：`scripts/cache*.pkl`、
  `.../EnergyGeoChemDB_csv/Analysis_*.csv`、`.../rockeval_usgs_egdb/*.zip`、`.../drp443_ifn/IFN.raw`。

## 四、历史重写记录（2026-10-30）

- 起因：主题 D 批量提交误纳入 7 个大文件 → GitHub pre-receive hook GH001 拒绝。
- 处理：`git filter-branch --index-filter 'git rm --cached ...' 3408b46^..HEAD` 从 4 个提交移除；
  `refs/original` 备份引用删除 + `gc --prune=now`。
- 副作用：filter-branch 同时删除了工作区副本；7 个文件已从对象库（当时仍可达）完整恢复，
  字节数与 blob 逐一核对一致。
- 双远端已更新：Gitee（forced update）与 GitHub 均同步至 `61321e0`。
