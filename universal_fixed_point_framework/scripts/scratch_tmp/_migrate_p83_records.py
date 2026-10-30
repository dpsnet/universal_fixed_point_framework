# -*- coding: utf-8 -*-
"""P83 工作记录迁移：Paper 58 -> Paper 48。
- Paper 48：附录 A 新增 P83 小节（脚本+证据索引）；v0.5 变更记录改"索引见附录 A"。
- Paper 58：附录 A 四行 P83 证据压缩为一行交叉引用；§10 E 段 P83 改写；变更记录 v0.100。"""
import io

def read(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()

def write(p, t):
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(t)

# ---------------- Paper 48 ----------------
P48 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
t48 = read(P48)

# 1) 附录 A 新增 P83 小节（锚点：结果数据列表末行）
anchor48 = "- `results/selection_effect_falsification.json` — 选择效应证伪汇总（四类检验结果）"
assert t48.count(anchor48) == 1, "p48 anchor fail"
p83_section = anchor48 + """

### P83 专业模型大气复核（工作记录，2026-09/10）

P83 工程（服务 §4.4 专业模型大气复核，与 §4.3.8 同一 B-残差梯度体系）全部脚本与证据，位于 MUFPF 工程 `scripts/` 与 `results/` 目录：

- `scripts/paperX_wd_m83a*.py` — Zeeman 波长反序混叠诊断、多变量控制、置换检验（源数据 `results/white_dwarf_analysis_v10/11_*_results.json`）
- `scripts/paperX_wd_m83c_s1-s4.py` — Koester 2010 LTE 复核（891 网格点 fid 表）；证据 `paperX_wd_m83c_samples.json`/`sample_list.json`/`fid_table.json`/`koester_ew.json`/`regression.json`；光谱缓存 `_koester_spec/`（292 个）
- `scripts/paperX_wd_m83c_tmap_s2-s3.py` — TMAP NLTE 热端复核（255 网格点）；证据 `paperX_wd_m83c_tmap_fid.json`/`paperX_wd_m83c_tmap_reg.json`；光谱缓存 `_tmap_spec/`（45 个）
- `scripts/paperX_wd_m83d_s1-s2.py` — 强场端扩展（Kepler+ 2013 全表 `paperX_wd_m83d_kepler2013.json` 539 行、60 颗采样 `paperX_wd_m83d_kepler_sample.json`；进行中）
"""
t48 = t48.replace(anchor48, p83_section)

# 2) v0.5 变更记录行末尾改写（行内子串替换）
old48 = "工作记录经 Paper 58 P83 段落盘，Paper 48 与 Paper 58 交叉引用。"
new48 = "P83 工作记录索引见附录 A（P83 小节）；与 Paper 58 交叉引用（Paper 58 保留理论镜像论证 §6.3 与检验结论引用，工作记录已迁至本文）。"
assert t48.count(old48) == 1, "p48 changelog fail"
t48 = t48.replace(old48, new48)
write(P48, t48)
print("P48 OK len=%d" % len(t48))

# ---------------- Paper 58 ----------------
P58 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
t58 = read(P58)
lines = t58.split("\n")

# 3) 附录 A：压缩四行 P83 证据行为一行交叉引用
out = []
removed = 0
compressed = ("| P83 白矮星 EW 独立预言（`scripts/paperX_wd_m83*.py` 全链 + `results/white_dwarf_analysis_v10/11_*_results.json`） | "
              "**§10 P83——服务 Paper 48 的专业模型大气复核**：Zeeman 波长反序混叠排除；Koester LTE（rho=-0.328 p=2.6e-07、beta=-0.289 p=6.7e-06）；"
              "TMAP NLTE 热端（rho=-0.395 p=5.5e-3、beta=-0.260 p=4.7e-2）；M83d 强场扩展（Kepler 2013，进行中）——"
              "完整工作记录已迁至 **Paper 48 附录 A（P83 小节）**，本侧仅保留交叉引用 | 已运行（PASS，见 Paper 48） |")
inserted = False
for ln in lines:
    if ln.startswith("| `scripts/paperX_wd_m83"):
        if not inserted:
            out.append(compressed)
            inserted = True
        removed += 1
        continue
    out.append(ln)
assert removed == 4, "p58 appendix removed=%d" % removed
t58 = "\n".join(out)

# 4) §10 E 段 P83 行改写（行匹配 startswith）
t58_new = []
replaced10 = False
for ln in t58.split("\n"):
    if ln.startswith("- **白矮星 EW 独立预言（P83"):
        ln = ("- **白矮星 EW 独立预言（P83——服务 Paper 48 拓扑禁戒观测验证）**：三层模型大气复核完成"
              "（Koester LTE ρ=-0.328 / TMAP NLTE ρ=-0.395，梯度跨多项式→Koester→TMAP 稳定）——"
              "结论与完整工作记录已归 **Paper 48（§4.4 + 附录 A P83 小节）**——本侧未决项仅余 "
              "**M83d 强场扩展**（Kepler+ 2013 60 颗，进行中）")
        replaced10 = True
    t58_new.append(ln)
assert replaced10, "p58 s10 fail"
t58 = "\n".join(t58_new)

# 5) 变更记录 v0.100（插在 v0.99 行前）
v100 = ("| v0.100 | 2026-10-07 | **P83 工作记录迁移（Paper 58 → Paper 48）**：附录 A 四行 P83 证据索引压缩为一行交叉引用"
        "（指向 Paper 48 §4.4 + 附录 A P83 小节）；§10 E 未决事项 P83 段改写为结论引用（仅余 M83d 未决）；"
        "Paper 48 已同步 v0.5（§4.4 结论 + 附录 A P83 小节工作记录）。理论镜像论证（§6.3 定理 6.1）保留本侧。 |")
t58_new = []
inserted100 = False
for ln in t58.split("\n"):
    if ln.startswith("| v0.99 |") and not inserted100:
        t58_new.append(v100)
        inserted100 = True
    t58_new.append(ln)
assert inserted100, "p58 v100 insert fail"
t58 = "\n".join(t58_new)

write(P58, t58)
print("P58 OK len=%d" % len(t58))
