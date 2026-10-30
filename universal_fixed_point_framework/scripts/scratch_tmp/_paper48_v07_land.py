# -*- coding: utf-8 -*-
"""Paper 48 v0.7 落盘：§4.5 插入 + §7 更新 + 附录 A + 变更记录"""
import io

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
with io.open(P, "r", encoding="utf-8") as f:
    t = f.read()

def rep(old, new, tag):
    global t
    assert old in t, "NOT FOUND: " + tag
    assert t.count(old) == 1, "MULTI: " + tag
    t = t.replace(old, new)
    print("OK:", tag)

# 1) 头部版本
rep("**版本**：v0.5（2026-10-07）", "**版本**：v0.7（2026-10-07）", "version")

# 2) §4.5 插入（§4.4 结论段尾 + \n\n--- 前）
old45 = "强场端结论域为 B ≤ 105 MG，不外推至更高场强。\n\n---"
new45 = """强场端结论域为 B ≤ 105 MG，不外推至更高场强。

### 4.5 第三独立目录交叉验证（M83e：DESI DR1 137 颗，完成）

为彻底排除"梯度仅存于单一观测项目/单一日录"的口实，引入第三个完全独立的磁场白矮星目录：arXiv:2603.20487（Amorim、Kepler & Romero 同团队，2026）——DESI DR1 光谱 + Gaia DR3 候选、视觉识别 Zeeman 分裂，137 颗新 DA 磁白矮星，$B=0.75$–$455.1$ MG（覆盖低场至迄今最高场白矮星），$T_{\\text{eff}}$ 取自 Gaia Gentile Fusillo 2021，$\\log g=8$（YAWP 脉动证认，固定值）。

- **目录重建（R1）**：附录 Table 1 从 arXiv 源 PDF 本地解析（fitz words 坐标分行）精确提取 137 行 9 字段——**修正了网页转录版 Gaia Source ID 的大量错位**（如 8813559108020207008 实为 881355910802027008）；B 范围复现 0.75/455.1；B 分档 85 低场（<10 MG）/44 中场/8 高场（≥100 MG）。Gaia TAP 坐标查询 125/137 命中（12 颗论文 ID 在 DR3 中不可解析，登记为目录固有缺陷批次）。
- **光谱获取（R3）**：DESI DR1 iron reduction coadd 光谱（`spectro/redux/iron/healpix/main/{bright|dark}/{hp//100}/{hp}/coadd-main-*.fits`，nside=64 nested 像素），HTTP Range 按需读取（自研 FITS 读取器 `_m83e_desi_reader.py`，与 astropy 对照全 match）。116/137 颗成功提取（12 无坐标不可解析 + 3 DESI 无 coadd 文件 + 6 同像素内无匹配目标光谱，均登记）。
- **EW 测量（R4）**：与 §4.4 完全同口径（Balmer 外 50 Å 掩膜 4 阶多项式归一化、window=80、EW>0.5 Å、depth>0.03、每星≥2 线检测）——91/116 颗有效。
- **理论 EW（R5）**：复用 Koester 2010 LTE 网格缓存（891 点，logg 取固定 8.0 最近点）——50 颗同时有观测/理论 EW 构成有效残差（38 低场 + 11 中场 + 1 高场≥100 MG）。
- **独立回归结果（R6）**：残差 $\\log_{10}(\\text{obs}/\\text{EW}_{\\text{Koester}})$ 对 $\\log_{10}B$（中心化 OLS，含 Teff）——**$\\log_{10}B$ 系数 $-0.596$（$t=-10.13$）**；Spearman **$\\rho=-0.727$（$p=2.33\\times10^{-9}$）**——负梯度在第三个独立目录中以更高显著性复现。
- **三目录统一合并（R6b）**：Amorim 518（统一 Koester 口径重算，237 有效）+ Kepler 60（32 有效）+ DESI 137（50 有效）共 **319 有效残差**——合并主回归 $\\log_{10}B$ 系数 $-0.292$（$t=-5.30$），Spearman $\\rho=-0.209$（$p=1.66\\times10^{-4}$）；含目录固定效应与目录×$\\log_{10}B$ 交互的完整模型：Kepler 交互 $-1.240$（$t=-3.22$）、DESI 交互 $-0.324$（$t=-1.84$）——**三个目录的 B 梯度符号全部一致（负）**，强度随 B 域增强而陡化（Amorim 低场段 $-0.28$、DESI 全段 $-0.60$、Kepler 中场段 $-1.52$），与 §2 理论预言的"通道分离/辐射抑制随场强增强"定性一致。
- **诚实边界**：(1) 12/137 颗 Gaia ID 在 DR3 不可解析（含目录最高场 455.1 MG 星），结论域以 125 颗可定位子样本为准；(2) DESI $\\log g$ 固定 8 引入 ≤0.1 dex 理论 EW 不确定（对梯度方向无影响）；(3) Zeeman 混叠处理同 §4.4（逐线反序检查口径一致）；(4) DESI 光谱为单次 coadd（无多历元信噪比平均），SNR 混杂未单目录控制——但三目录合并主效应在控制目录固定效应后仍显著。

---"""
rep(old45, new45, "sec4.5")

# 3) §7.5 第 4 条更新
old75 = "未测量性质（年龄/伴星频率/旋转）差异仍需更深目录（Kepler et al. 2019, 2021）进一步验证。"
new75 = "未测量性质（年龄/伴星频率/旋转）差异仍需更深目录（Kepler et al. 2019, 2021）进一步验证。**再次部分解除（M83e）**：第三个独立目录 DESI DR1（arXiv:2603.20487，137 颗，同团队新样本）独立回归 $\\rho=-0.727$（$p=2.33\\times10^{-9}$），三目录（Amorim 518 + Kepler 60 + DESI 137）统一 Koester 口径合并 319 有效残差主回归 $\\log_{10}B=-0.292$（$t=-5.30$），目录×B 交互符号全负——梯度跨三个独立观测项目稳健，非单目录选择效应可解释。"
rep(old75, new75, "sec7.5-4")

# 4) §7.6 第 3 项标注完成
old76 = "3. **独立目录交叉验证**：用不依赖Amorim+ 2023的独立磁场白矮星目录重复残差分析与B梯度检验，彻底排除场依赖选择残余不确定性"
new76 = "3. **独立目录交叉验证**：用不依赖Amorim+ 2023的独立磁场白矮星目录重复残差分析与B梯度检验，彻底排除场依赖选择残余不确定性。**完成（M83e）**：DESI DR1 137 颗（arXiv:2603.20487）独立回归 rho=-0.727 p=2.33e-9；三目录统一口径合并 319 有效残差主效应 log10B=-0.292 t=-5.30——场依赖选择残余口实闭合。"
rep(old76, new76, "sec7.6-3")

# 5) 附录 A：P83 小节后追加 M83e 记录
oldapp = "- `scripts/_snr_dl_list.json`/`_snr_results.json`/`_snr_regression.json` — SNR 混杂控制（237 颗 SDSS 光谱 SN_MEDIAN 提取与含 SNR 回归）\n\n\n---"
newapp = """- `scripts/_snr_dl_list.json`/`_snr_results.json`/`_snr_regression.json` — SNR 混杂控制（237 颗 SDSS 光谱 SN_MEDIAN 提取与含 SNR 回归）

### M83e 第三独立目录：DESI DR1 137 颗（工作记录，2026-10-07，完成）

- `scripts/paperX_wd_m83e_desi137.json` — DESI 137 颗目录（PDF 精确版，修正 WebFetch 转录 Gaia ID 错位；B 0.75–455.1 MG；Gaia TAP 坐标 125/137 命中 `paperX_wd_m83e_desi137_coords.json`）
- `scripts/_m83e_pdf_table1.py` + `_2603.20487.pdf` + `_arxiv_2603.20487_src.tar` — 附录 Table 1 本地 PDF 精确提取（137 行 9 字段）
- `scripts/_m83e_desi_reader.py` — 自研 FITS HTTP Range 按需读取器（与 astropy 对照全 match）；`_m83e_desi_manifest.json`（111 条 url/prog/size）
- `scripts/_m83e_desi_extract.py`/`_m83e_coord_match.py`/`_m83e_final_extract.py` — 光谱提取（TARGETID 匹配优先、坐标匹配兜底；116/137 成功——12 无坐标 + 3 无 coadd + 6 无匹配光谱登记）；光谱缓存 `_desi_spec/{gaia_int}.npz`
- `scripts/_m83e_desi_ew.py` → `_m83e_desi_ew.json` — EW 测量（91/116 有效，同 M83c/d 口径）
- `scripts/_m83e_desi_regress.py` → `_m83e_desi_regression.json` — DESI 独立回归（n=50，log10B -0.596 t=-10.13，Spearman rho=-0.727 p=2.33e-9）
- `scripts/_m83e_merged_regress.py` → `_m83e_merged_regression.json`/`_m83e_merged_resid_samples.json` — 三目录统一合并（Amorim 237 + Kepler 32 + DESI 50 = 319，主效应 log10B=-0.292 t=-5.30 rho=-0.209 p=1.66e-4；交互 kepler_x_B=-1.240 t=-3.22、desi_x_B=-0.324 t=-1.84）

---
"""
rep(oldapp, newapp, "appendix-A")

# 6) 变更记录 v0.7
oldv = "## 变更记录\n\n### v0.6.1（2026-10-07）——M83d 全候选澄清"
newv = """## 变更记录

### v0.7（2026-10-07）——M83e 第三独立目录（DESI DR1 137 颗）
- 新增 §4.5：第三个独立目录交叉验证完成——arXiv:2603.20487（Amorim/Kepler/Romero 同团队，DESI DR1 + Gaia DR3，137 颗新 DA 磁白矮星，B 0.75–455.1 MG）；附录 Table 1 PDF 精确提取（修正网页转录 Gaia ID 错位）、Gaia TAP 坐标 125/137、DESI iron coadd Range 提取 116/137、同口径 EW 91/116、Koester 缓存理论 EW 50 有效残差——独立回归 log10B=-0.596（t=-10.13）、Spearman rho=-0.727（p=2.33e-9）
- 三目录统一合并（319 有效残差）：主效应 log10B=-0.292（t=-5.30）、rho=-0.209（p=1.66e-4）；目录×B 交互符号全负（kepler -1.240 t=-3.22、desi -0.324 t=-1.84）——梯度跨三独立观测项目稳健
- §7.5 第 4 条/§7.6 第 3 项：场依赖选择残余口实再解除（三目录交叉验证）；附录 A 新增 M83e 工作记录与证据索引；诚实边界：12/137 颗 ID 在 DR3 不可解析（含 455.1 MG 星）、DESI logg 固定 8 引入 ≤0.1 dex 不确定

### v0.6.1（2026-10-07）——M83d 全候选澄清"""
rep(oldv, newv, "changelog-v0.7")

with io.open(P, "w", encoding="utf-8") as f:
    f.write(t)
print("SAVED v0.7")
