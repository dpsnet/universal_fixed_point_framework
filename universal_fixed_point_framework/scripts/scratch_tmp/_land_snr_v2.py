# -*- coding: utf-8 -*-
"""落盘②：SNR 混杂控制结果 → Paper 48 §4.4 bullet + 附录 A P83 小节文件 + v0.5 变更记录追加。"""
import io

def rd(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()
def wr(p, t):
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(t)

P48 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
t = rd(P48)

# 1) §4.4 加 SNR 控制 bullet（锚点：无B偏倚 bullet 之后、结论 bullet 之前）
old = """- **检测筛选无 B 偏倚**：518 中未检测 279 颗 $\\log_{10}B$ 中位 2.49 vs 已检测 236 颗 2.43——筛选不以磁场强度为转移。
- **结论**："""
new = """- **检测筛选无 B 偏倚**：518 中未检测 279 颗 $\\log_{10}B$ 中位 2.49 vs 已检测 236 颗 2.43——筛选不以磁场强度为转移。
- **SNR 混杂控制**：从 SDSS 光谱 FITS 头提取 SN_MEDIAN（237 颗全部获得）后纳入回归——$\\log_{10}B$ 系数 $-0.289\\rightarrow-0.235$（$t=-3.72$，$p=1.97\\times10^{-4}$，仍 $p<0.001$）；残差-$\\log_{10}B$ Spearman $\\rho=-0.328$ → 控制 $\\log_{10}$SNR 后偏相关 $\\rho=-0.254$（$p=7.99\\times10^{-5}$）。SNR 有独立弱贡献（$\\log_{10}$SNR 系数 $-0.324$，$t=-3.60$）但与 B 效应不混淆——SNR 混杂无法解释 B-残差梯度。
- **结论**："""
assert t.count(old) == 1, "p48 s44 anchor"
t = t.replace(old, new)

# 2) 附录 A P83 小节补 SNR 文件（锚点：M83d 行之后）
old2 = "- `scripts/paperX_wd_m83d_s1-s2.py` — 强场端扩展（Kepler+ 2013 全表 `paperX_wd_m83d_kepler2013.json` 539 行、60 颗采样 `paperX_wd_m83d_kepler_sample.json`；进行中）"
new2 = old2 + "\n- `scripts/_snr_dl_list.json`/`_snr_results.json`/`_snr_regression.json` — SNR 混杂控制（237 颗 SDSS 光谱 SN_MEDIAN 提取与含 SNR 回归）"
assert t.count(old2) == 1, "p48 appendix anchor"
t = t.replace(old2, new2)

# 3) v0.5 变更记录行尾追加（锚点：行尾"…工作记录已迁至本文）。"）
old3 = "工作记录已迁至本文）。"
new3 = "工作记录已迁至本文）；审计补强：SNR 混杂控制（SDSS 光谱头 SN_MEDIAN 237 颗，加入回归后 log10B 系数 -0.289→-0.235 t=-3.72 p=1.97e-4 保持 p<0.001——SNR 无法解释 B-梯度）。"
assert t.count(old3) == 1, "p48 changelog anchor"
t = t.replace(old3, new3)

wr(P48, t)
print("P48 OK len=%d" % len(t))
