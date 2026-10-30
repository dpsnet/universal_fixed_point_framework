# -*- coding: utf-8 -*-
"""Paper 48 v0.8 落盘：窗口扫描截断实测排除 + 变更记录"""
import io

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
t = io.open(P, "r", encoding="utf-8").read()

def rep(old, new, tag):
    global t
    assert old in t, "NOT FOUND: " + tag
    assert t.count(old) == 1, "MULTI: " + tag
    t = t.replace(old, new)
    print("OK:", tag)

# 1) §4.4 截断诚实标注 → 实测排除（就地改）
old1 = "诚实标注：强场斜率陡化可能部分反映 Zeeman 分裂超出 80 Å 测量窗口的非对称截断（理论与观测同窗口，但归一化基线对分裂形态敏感）；方向性结论（高 B → 观测 EW 系统性低于理论）不受影响。"
new1 = "诚实标注→**实测排除（Phase 74 窗口扫描）**：Zeeman 分裂超出 80 Å 测量窗口的非对称截断曾是强场斜率陡化的候选解释——现经窗口扫描检验排除：Kepler 32 颗（B 14–212 MG）与 DESI 49 颗在 W=80/160/320 Å 三窗口（half-gap 截断防相邻线重叠）重测 EW、理论同窗口重算——合并 81 颗回归 log10B 系数 -0.507/-0.442/-0.484（t=-5.71/-4.78/-5.17），Kepler 强场交互 -0.936/-1.080/-1.055——**斜率完全不随窗口收敛到 0，强场端反而稳定**；逐星验证高场星 EW 确随窗口恢复（B=51 MG +20%、B=172 MG +64%）但梯度保持。方向性结论（高 B → 观测 EW 系统性低于理论）获窗口鲁棒性验证。"
rep(old1, new1, "sec4.4-trunc")

# 2) §4.5 诚实边界第 (3) 条更新
old2 = "(3) Zeeman 混叠处理同 §4.4（逐线反序检查口径一致）；"
new2 = "(3) Zeeman 混叠处理同 §4.4（逐线反序检查口径一致）；高场 Zeeman 截断口实经窗口扫描实测排除（§4.4，W=80/160/320 Å 斜率不收敛）；"
rep(old2, new2, "sec4.5-bound3")

# 3) 附录 A 追加 Phase 74 工作记录（在 M83e 记录块末尾、--- 前）
old3 = "- `scripts/_m83e_merged_regress.py` → `_m83e_merged_regression.json`/`_m83e_merged_resid_samples.json` — 三目录统一合并（Amorim 237 + Kepler 32 + DESI 50 = 319，主效应 log10B=-0.292 t=-5.30 rho=-0.209 p=1.66e-4；交互 kepler_x_B=-1.240 t=-3.22、desi_x_B=-0.324 t=-1.84）\n\n---"
new3 = """- `scripts/_m83e_merged_regress.py` → `_m83e_merged_regression.json`/`_m83e_merged_resid_samples.json` — 三目录统一合并（Amorim 237 + Kepler 32 + DESI 50 = 319，主效应 log10B=-0.292 t=-5.30 rho=-0.209 p=1.66e-4；交互 kepler_x_B=-1.240 t=-3.22、desi_x_B=-0.324 t=-1.84）

### Phase 74 窗口扫描：Zeeman 截断实测排除（工作记录，2026-10-07，完成）

- `scripts/_m83e_window_scan.py` → `_m83e_window_scan.json`/`_m83e_window_scan_regs.json` — DESI 91 颗多窗口（80/160/320 Å + half-gap 截断）EW 与 Koester 同窗口理论 EW：49 有效残差，log10B -0.468/-0.406/-0.445（t=-9.55/-8.77/-9.17）、ρ -0.735/-0.708/-0.759（p<1e-8）——窗口扩展斜率不消失；逐星 B=51 MG EW +20%、B=172 MG +64%
- `scripts/_m83d_window_scan.py` → `_m83d_window_scan.json` — Kepler 32 颗（B 14–212 MG，SDSS 光谱 astroquery 重取 34/34）多窗口：log10B -1.343/-1.431/-1.440（t≈-4.1）、ρ≈-0.71——中场/强场段斜率窗口扩展完全稳定；高场星 Zeeman 展宽实测（B=53 MG 仅 Hε/Hζ、B=105 MG 仅 Hη、B=212 MG 无检测）
- `scripts/_m83e_m83d_window_merge.py` → `_m83e_m83d_window_merge.json` — 合并 81 颗统一回归（目录固定效应+交互）：W=80/160/320 log10B -0.507/-0.442/-0.484（t=-5.71/-4.78/-5.17）、ρ -0.513/-0.440/-0.379、Kepler×B -0.936/-1.080/-1.055——斜率不收敛到 0，Zeeman 截断假说实测排除

---
"""
rep(old3, new3, "appendix-phase74")

# 4) 版本号 v0.7 → v0.8
rep("**版本**：v0.7（2026-10-07）", "**版本**：v0.8（2026-10-07）", "version")

# 5) 变更记录 v0.8
old5 = "## 变更记录\n\n### v0.7（2026-10-07）——M83e 第三独立目录（DESI DR1 137 颗）"
new5 = """## 变更记录

### v0.8（2026-10-07）——Phase 74 窗口扫描：Zeeman 截断实测排除
- §4.4：原"强场斜率陡化可能部分反映 Zeeman 截断"诚实标注升级为实测排除——窗口扫描（80/160/320 Å + half-gap）DESI 49 + Kepler 32 = 81 颗合并回归 log10B -0.507/-0.442/-0.484（t=-5.71/-4.78/-5.17），Kepler 强场交互 -0.936/-1.080/-1.055 稳定——斜率不收敛，截断不解释梯度
- §4.5 诚实边界第 (3) 条：Zeeman 截断口实闭合；附录 A 新增 Phase 74 工作记录与证据索引
- 保留边界：B>100 MG 个体星有效检测线数少（1–2 线），个体残差不确定度升高；窗口上限受相邻线距物理限制；Zeeman 多分量拟合仍为高场端最终解（§7.6 第 4 项未来工作）

### v0.7（2026-10-07）——M83e 第三独立目录（DESI DR1 137 颗）"""
rep(old5, new5, "changelog-v0.8")

io.open(P, "w", encoding="utf-8").write(t)
print("SAVED v0.8")
