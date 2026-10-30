# -*- coding: utf-8 -*-
"""chain_audit_161_highprec_combos.py — 核磁子链高精度组合结构展开（μ_³H/μ_³He/μ_d 组合）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

mh3 = 2.9789624656   # 氚核 ³H
mhe3 = 2.1274977     # 氦-3 ³He（绝对值；真实为负）
md = 0.8574382308    # 氘核 ²H
mp2 = 2.79284734462  # g_p/2
mn2 = 1.91304273     # g_n/2（绝对值）

print("=== 1. 氚/氦-3 磁矩比（7/5 = 对合域/静默 候选）===")
r = mh3/mhe3
print(f"μ_³H/|μ_³He| = {r:.9f}")
print(f"7/5 = 1.4：dev {(r-1.4)/1.4*100:+.5f}%")
print(f"对照：μ_³He/μ_³H = {1/r:.7f} vs 5/7 = 0.7142857：dev {(1/r-5/7)/(5/7)*100:+.5f}%")

print("\n=== 2. 三高精度量两两关系全扫描（差值/和/比）===")
pairs = [
    ("μ_³H−|μ_³He|", mh3-mhe3),
    ("μ_³H+|μ_³He|", mh3+mhe3),
    ("|μ_³He|−μ_d", mhe3-md),
    ("μ_³H−μ_d", mh3-md),
    ("|μ_³He|/μ_d", mhe3/md),
    ("μ_³H/μ_d", mh3/md),
    ("μ_³H−|μ_³He|−μ_d", mh3-mhe3-md),
    ("|μ_³He|×μ_d", mhe3*md),
]
cands = {
    "N_gen=3": 3, "不动点=4": 4, "静默=5": 5, "对合域=7": 7, "k_max=8": 8,
    "N_gen²=9": 9, "16": 16, "25": 25, "49": 49, "64": 64,
    "7/5": 1.4, "5/7": 5/7, "6/7": 6/7, "3/2": 1.5, "16/15": 16/15,
    "2": 2, "10": 10, "3.5": 3.5, "2.5": 2.5, "1.75": 1.75,
    "231/100": 2.31, "65/24": 65/24, "16259/6000": 16259/6000,
}
for pname, v in pairs:
    best = None
    for cname, c in cands.items():
        dev = (v-c)/c*100
        if abs(dev) < 0.05 and (best is None or abs(dev) < abs(best[2])):
            best = (cname, c, dev)
    if best:
        print(f"  ★ {pname} = {v:.7f} ≈ {best[0]} = {best[1]}（dev {best[2]:+.4f}%）")
    else:
        print(f"  · {pname} = {v:.7f}（无 0.05% 内命中）")

print("\n=== 3. μ_³He 绝对值的框架候选精搜 ===")
tgt = mhe3
print(f"|μ_³He| = {tgt:.9f}（精度 3e-8）")
for cname, c in cands.items():
    dev = (tgt-c)/c*100
    if abs(dev) < 0.5:
        print(f"  {cname} = {c}: dev {dev:+.4f}%")
print("对照：μ_³H×5/7 =", mh3*5/7, "dev", f"{(tgt-mh3*5/7)/(mh3*5/7)*100:+.5f}%")
print("对照：μ_³H−μ_d =", mh3-md, "dev", f"{(tgt-(mh3-md))/(mh3-md)*100:+.5f}%")

print("\n=== 4. 对合域 7 在核磁子链中的枢纽出现统计 ===")
print("μ_d ≈ 6/7（分母对合域）")
print("μ_³H/|μ_³He| ≈ 7/5（分子对合域）")
print("g_p/g_n = 73/50：73 = 8·9+1（无 7）；但 44/23 中 44 = 5·8+4（无 7）")
print("μ_N/μ_B = 371/2430：371 = 7×(45+8)（分子含 7）")
print("→ 对合域 7 出现：μ_d（分母）、μ_³H/μ_³He（分子）、371（分子因子）——三处")

print("\n=== 5. 判别汇总 ===")
print("① μ_³H/|μ_³He| ≈ 7/5 dev +0.016%（略超 0.01% 阈值——登记组合候选）")
print("② μ_³H−|μ_³He| = 0.8514647（无身份）")
print("③ 对合域 7 三处枢纽——核磁子链含 7 结构与不含 7 结构分裂（μ_d/μ_³H~³He 系 vs g_p/g_n 系）")
print("④ 精度：μ_³H/μ_³He 两量均为 1e-8 级测量——组合候选虽 0.016% 但两输入高精度，残差真实存在")
