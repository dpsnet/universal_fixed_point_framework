# -*- coding: utf-8 -*-
"""落盘 M47/M49/M50：roadmap + 笔记 §63 + Paper 58 v0.79"""
import io

p = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/roadmap/phase77_n11_crossset_greedy.md'
s = io.open(p, encoding='utf-8').read()
anchor = "## 开放登记（更新）"
add = """## M47 ✅ 50 轮下探（2026-10-06，随机极小化下界 38）

- 50 轮终局最小 **38**（轮16）——38/38 全必要
- 随机极小化观测区间 [38, 48]——R1 生长 26 已远优于

## M49 ✅ n=10 阈值化谱维数（2026-10-06，跨 n 对照）

- **n=10 阈值化（3 seed × 20000 = 60000，A_BG）——165 阈值化 0 冲突**（无全补）
- 3 轮极小化 [50, 48, **33**]——**谱维数 33**
- 跨 n 对照：n=11 随机极小化 38-48 vs n=10 = 33——**随机极小化口径下谱维数随 n 增长**
- 证据：`paperX_n10_m49_thr_spectral.json` + `cache_n10_thr3x20000.pkl`

## M50 ✅ R1 28 验证 + 26 收敛（2026-10-06，谱维数上界 26）

- **28 名单 0 冲突复验 ✓**——25/28 必要——**3 冗余**（s1_23456、s1_2345678、s1_23456789——长前缀）
- **28 起点 10 轮最小化：全 26**（10/10 一致）——**R1 路径稳定极小 26**
- **n=11 谱维数链**：随机极小化 38-48（陷阱）→ R1 生长 28 → 26——**上界 ≤ 26**
- 证据：`paperX_n11_m50_r1min.json`
- **M51 已启动**：n=10 R1 生长（对照 26 的标度律）

## 开放登记（更新）
"""
assert anchor in s
s = s.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8').write(s)

p2 = "E:/workspace/hyper-resolution/universal_fixed_point_framework/notes/06_photon_topology/note_phase72_n10_criterion.md"
s2 = io.open(p2, encoding="utf-8").read()
add2 = """
## 六十三、谱维数收敛：n=11 → 26、n=10 → 33（2026-10-06，Phase 77 M47/M49/M50）

**M47**：50 轮随机极小化——最小 **38**（38/38 必要）——随机极小化区间 [38, 48]。

**M49**：n=10 阈值化（3×20000，A_BG）——165 阈值化 0 冲突——3 轮极小化 [50,48,**33**]——**n=10 谱维数 33**（随机极小化口径）——跨 n 对照：谱维数随 n 增长（33 → 38-48）。

**M50**：R1 28 名单复验 0 冲突——**25/28 必要**（3 冗余：s1_23456、s1_2345678、s1_23456789——长前缀冲突 0——被删）——**28 起点 10 轮最小化全 26**（稳定）——**R1 路径谱维数 ≤ 26**。

**谱维数链（n=11）**：
```
随机极小化（220 删）：38-48  ← 局部极小陷阱（删序依赖）
R1 生长（18 加）：28 → 删 3 冗余 → 26（稳定，10/10 轮）
```

**重要**：
1. **26 是 R1 路径稳定极小**——但全局最小未知（n=10 的 33 vs n=11 的 26 不可直接比——口径不同）
2. **n=10 的 R1 生长待 M51**——若 n=10 R1 生长也 ~20 出头——标度律初现
3. **26 名单结构**：R1 18（相邻 + 前缀）+ 追加 10 前缀块分裂 − 3 长前缀冗余
4. **跨 n 标度**：随机极小化口径 ~3n（33 ≈ 3×10+3、38-48 ≈ 3×11+5-15）——R1 口径待测
"""
io.open(p2, "w", encoding="utf-8").write(s2 + add2)

p3 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
s3 = io.open(p3, "r", encoding="utf-8").read()
s3 = s3.replace("**版本**：v0.78（2026-10-06）", "**版本**：v0.79（2026-10-06）", 1)
old = "| v0.78 | 2026-10-06 | **R1 生长律（Phase 77 M48）**"
add3 = "| v0.79 | 2026-10-06 | **谱维数收敛（Phase 77 M47/M49/M50）**：n=11 R1 路径稳定 26（28 删 3 冗余）；随机极小化 [38,48]；n=10 阈值化谱维数 33——跨 n 对照。 |\n| v0.78 | 2026-10-06 | **R1 生长律（Phase 77 M48）**"
assert old in s3
s3 = s3.replace(old, add3, 1)
io.open(p3, "w", encoding="utf-8").write(s3)
print("M47/M49/M50 落盘完成（roadmap + 笔记 §63 + Paper 58 v0.79）")
