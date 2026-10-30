# -*- coding: utf-8 -*-
"""修正 M83d 表述：60 采样 = 全候选 60（无采样选择）；>105 MG 覆盖上限声明。v0.6.1"""
import io

def rd(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()
def wr(p, t):
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(t)

P48 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
t = rd(P48)

# 1) §4.4 结论：60 采样 → 全候选 60 + 覆盖上限
old1 = "**强场端独立目录交叉验证（M83d，完成）**：Kepler+ 2013 全表（539 颗，B 1–773 MG）60 颗采样、32 颗有效（B 10–105 MG，Teff 8000–40000 K 域重叠），同为 Koester2 口径——残差全负（-2.06 ~ +0.02），OLS（中心化，含 Teff/logg）$\\log_{10}B$ 系数 $-1.465$（$t=-4.44$），Spearman $\\rho=-0.722$（$p=3.05\\times10^{-6}$）——**负梯度在完全独立的强场目录中保持且更陡**。诚实标注：强场斜率陡化可能部分反映 Zeeman 分裂超出 80 Å 测量窗口的非对称截断（理论与观测同窗口，但归一化基线对分裂形态敏感）；方向性结论（高 B → 观测 EW 系统性低于理论）不受影响。"
new1 = ("**强场端独立目录交叉验证（M83d，完成）**：Kepler+ 2013 全表（539 颗，B 1–773 MG）中 10–300 MG 域全部候选 60 颗（Teff 8000–40000 K 域重叠且不重复 Amorim 样本——**无采样选择，候选即全采**）、32 颗有效（B 10–105 MG），同为 Koester2 口径——残差全负（-2.06 ~ +0.02），OLS（中心化，含 Teff/logg）$\\log_{10}B$ 系数 $-1.465$（$t=-4.44$），Spearman $\\rho=-0.722$（$p=3.05\\times10^{-6}$）——**负梯度在完全独立的强场目录中保持且更陡**。诚实标注：强场斜率陡化可能部分反映 Zeeman 分裂超出 80 Å 测量窗口的非对称截断（理论与观测同窗口，但归一化基线对分裂形态敏感）；方向性结论（高 B → 观测 EW 系统性低于理论）不受影响。**覆盖上限声明**：Kepler 目录 >105 MG 段候选仅 6 颗（100–200 MG 1 颗、200–300 MG 5 颗，温度域命中 5 颗）——强场端结论域为 B ≤ 105 MG，不外推至更高场强。")
assert t.count(old1) == 1, "anchor1"
t = t.replace(old1, new1)

# 2) §7.5 第 4 条：补"全候选"
old2 = "**部分解除（M83d）**：Kepler+ 2013 独立目录交叉验证完成——32 颗有效（B 10–105 MG）负梯度 $\\rho=-0.722$（$p=3.05\\times10^{-6}$），与 Amorim 518 样本方向一致，排除『目录内选择效应造成梯度』的可能；未测量性质（年龄/伴星频率/旋转）差异仍需更深目录（Kepler et al. 2019, 2021）进一步验证。"
new2 = "**部分解除（M83d）**：Kepler+ 2013 独立目录交叉验证完成——10–300 MG 域全候选 60 颗（无采样选择）、32 颗有效（B 10–105 MG）负梯度 $\\rho=-0.722$（$p=3.05\\times10^{-6}$），与 Amorim 518 样本方向一致，排除『目录内选择效应造成梯度』的可能；未测量性质（年龄/伴星频率/旋转）差异仍需更深目录（Kepler et al. 2019, 2021）进一步验证。"
assert t.count(old2) == 1, "anchor2"
t = t.replace(old2, new2)

# 3) §7.6 第 2 项：修正"余 479 颗"
old3 = "**完成（M83d）**：Kepler+ 2013 强场样本 60 颗采样下载与 EW 测量完成（32 颗有效，工作记录见 Paper 48 附录 A）；后续可从 Kepler+ 2013 余 479 颗继续扩样，或引入 Kepler et al. 2019/2021 目录。"
new3 = "**完成（M83d）**：Kepler+ 2013 强场样本全候选 60 颗下载与 EW 测量完成（32 颗有效——Kepler 表 10–300 MG 域已完整覆盖，余 479 颗中 448 颗为 <10 MG 不在强场目标域，无剩余可扩候选；工作记录见 Paper 48 附录 A）；后续扩样需引入其他目录（Kepler et al. 2019/2021）。"
assert t.count(old3) == 1, "anchor3"
t = t.replace(old3, new3)

# 4) 附录 A：采样描述修正
old4 = "- `scripts/paperX_wd_m83d_s1-s2.py` + `_m83d_recover.py` — 强场端扩展（Kepler+ 2013 全表 `paperX_wd_m83d_kepler2013.json` 539 行、60 颗采样 `paperX_wd_m83d_kepler_sample.json`、恢复脚本增量落盘；完成）"
new4 = "- `scripts/paperX_wd_m83d_s1-s2.py` + `_m83d_recover.py` + `_m83d_fill.py` — 强场端扩展（Kepler+ 2013 全表 `paperX_wd_m83d_kepler2013.json` 539 行；10–300 MG 域全候选 60 颗 `paperX_wd_m83d_kepler_sample.json`——候选即全采，无采样选择；恢复/补全脚本增量落盘；完成）"
assert t.count(old4) == 1, "anchor4"
t = t.replace(old4, new4)

# 5) 变更记录追加 v0.6.1
old5 = "### v0.6（2026-10-07）——M83d 强场端收尾"
new5 = "### v0.6.1（2026-10-07）——M83d 全候选澄清\n- 澄清：Kepler+ 2013 10–300 MG 域全候选 60 颗（Teff 域重叠且不重复 Amorim）——候选即全采，无采样选择（消除『为何 60 颗』口实）\n- 覆盖上限声明：Kepler 目录 >105 MG 段候选仅 6 颗，强场端结论域 B ≤ 105 MG，不外推\n- §7.6 第 2 项修正：Kepler 表无剩余可扩候选（余 479 颗中 448 颗 <10 MG），后续扩样需 Kepler et al. 2019/2021\n\n### v0.6（2026-10-07）——M83d 强场端收尾"
assert t.count(old5) == 1, "anchor5"
t = t.replace(old5, new5)

wr(P48, t)
print("P48 v0.6.1 OK len=%d" % len(t))
