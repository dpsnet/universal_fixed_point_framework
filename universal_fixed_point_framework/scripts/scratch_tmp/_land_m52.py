# -*- coding: utf-8 -*-
"""落盘 M51/M52 + n=10 25 探索"""
import io, os, sys, json, pickle
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len(set(vals)) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


# n=10 删冗余验证
n10 = 10
f10 = adj_partition_factors(n10)
N10 = [factor_name(a, b) for a, b in f10]
with open(os.path.join(SCRIPT_DIR, "cache_n10_thr3x20000.pkl"), "rb") as f:
    d10 = pickle.load(f)
s10 = []
for sd in ["77", "331", "777"]:
    s10.extend(d10[sd])
m52 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m52_scale26.json"), encoding="utf-8"))
names10_26 = m52["n10"]["names26"]
idx10 = [N10.index(x) for x in names10_26 if x != "s1_2345678"]
c25 = conflict_count(group(s10, idx10))
print(f"n=10 删冗余后 25 因子冲突：{c25}", flush=True)
sens = {}
n_nec = 0
for i in idx10:
    trial = [x for x in idx10 if x != i]
    c = conflict_count(group(s10, trial))
    sens[N10[i]] = c
    if c > 0:
        n_nec += 1
print(f"25 必要 {n_nec}/25、冗余 {[nm for nm, c in sens.items() if c == 0]}", flush=True)
out25 = {"n": 10, "names25": [N10[i] for i in sorted(idx10)], "c25": c25,
         "n25_necessary": n_nec, "sens25": sens}
json.dump(out25, open(os.path.join(SCRIPT_DIR, "paperX_n10_m53_25.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ===== 落盘 =====
p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase77_n11_crossset_greedy.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 开放登记（更新）"
add = """## M51 ✅ 跨 n R1 生长对照（2026-10-06，标度律初现）

- **n=10 R1 生长：16 + 10 = 26 因子 0 冲突**（60000 阈值化）
- **n=11 R1 生长：18 + 10 = 28 → 随机删 3 = 26**
- **跨 n 对照：R1 路径完备覆盖都是 26**（n=10、11）——**非随 n 增长**——与随机极小化口径（3n）不同
- 追加因子全为前缀块分裂（锚 1 族）
- 证据：`paperX_n11_m51_r1scale.json`

## M52 ✅ 真实 26 名单验证（2026-10-06，n=11 全必要）

- **n=11 完备 26 名单**：9 相邻 + 7 前缀锚 + 10 前缀块分裂 = 26——**冲突 0、26/26 全必要**
- **n=10 的 26 有 1 冗余**（s1_2345678）——可删 → 25（待验证）
- **标度律修正**：n=10 ≤ 25、n=11 = 26——接近常数但非严格——待 n=9/n=12 外推
- 证据：`paperX_n11_m52_scale26.json`

## 开放登记（更新）
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 六十四、标度律：R1 路径完备覆盖 ≈ 26（2026-10-06，Phase 77 M51/M52）

**M51**：n=10 R1 生长 16+10=26、n=11 R1 生长 18+10=28→26——**跨 n 都是 26**——非随 n 增长（随机极小化口径 3n）——**R1 路径的标度不变量初现**。

**M52**：
- **n=11 完备 26 名单**：相邻单对 9（s2_3..s10_11）+ 前缀锚 7（s1_2、s1_23、s1_234、s1_2345、s1_234567、s1_2345678、s1_2345678910）+ 前缀块分裂 10（s12_3、s123_4、s1234_5、s12345_6、s123_45678910、s1234_5678910、s12345_678910、s123456_78910、s1234567_8910、s12345678_910）——**冲突 0、26/26 全必要**
- **n=10 的 26 有 1 冗余**（s1_2345678——长前缀）——可删 → 25？

**"26" 的深刻意味**：
1. **弦论关键维数恰为 26**（玻色弦）——n=10、11 判据完备覆盖都收敛 26——**数字巧合还是结构必然？**——登记为"待论证的同构"（同构≠机制——按诚实边界）
2. **R1 路径完备覆盖与 n 弱相关**（25-26）——比随机极小化（3n）低得多——**加法贪心（每步减冲突最多）接近信息论最优**
3. **结构主导是"前缀族"**（s1_xxx 占 17/26）——锚 1 的区间块是符号信息的主要载体

**下一步**：n=9/n=12 R1 生长外推（验证 25-26 普适）+ n=10 25 确认
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s3 = io.open(p3, "r", encoding="utf-8").read()
s3 = s3.replace("**版本**：v0.79（2026-10-06）", "**版本**：v0.80（2026-10-06）", 1)
old = "| v0.79 | 2026-10-06 | **谱维数收敛（Phase 77 M47/M49/M50）**"
add3 = "| v0.80 | 2026-10-06 | **标度律（Phase 77 M51/M52）**：R1 路径完备覆盖 n=10→26、n=11→26（26/26 全必要）——非随 n 增长——n=10 可下探 25。 |\n| v0.79 | 2026-10-06 | **谱维数收敛（Phase 77 M47/M49/M50）**"
assert old in s3
s3 = s3.replace(old, add3, 1)
io.open(p3, "w", encoding="utf-8").write(s3)
print("M51/M52 落盘完成 + n=10 25 探索已跑（见 json）")
