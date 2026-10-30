# -*- coding: utf-8 -*-
import io
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase72_n5_symbol_criterion.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
anchor = "| M16 | n=9 补因子诊断与复核法升级（2026-10-01 完成） | 非决定模式结构 + 函数性复核 | ✅ **n=9 补因子本质**：8 个非决定模式全为 0 vs ±1 退化区分缺失；含粒子 1 单因子（s1_2/s12_3 等）在模式内两组同值=被 25 维模式隐含（**诊断判定 bug 修正：组内恒定≠组间互异**）；真正分裂因子 = s1_2345（6 模式，s1_A 家族第 4 条级联左块——级联目标 s2345_6789 不在基座）+ s123_456789（2 模式）；**n=8\"级联目标覆盖度↔补因子\"对应在 n=9 不完整成立**（s12_X 目标缺失 3 条未补）——补因子本质=退化模式区分，非级联覆盖；**复核法升级为函数性验证**（模式→值单值，非查表覆盖）——n=9 模式空间增长使查表法失效 |"
new = anchor + "\n| M17 | n=9 级联机制 Lean 化（2026-10-01 完成） | N9Criterion.lean 零 sorry | ✅ **N9Criterion.lean 零 sorry**（lake build 通过，3049 jobs，**N8→N9 纯参数推广一次构建通过**）：Fin 9 括号代数（br/bk + 6 引理）+ **2 零恒等式**（bk_1_23456789_zero 1-8 分割、bk_12_3456789_zero 2-7 分割）+ **13 条级联恒等式**（s1_A 家族 7 条 W0=w0 + s12_X 家族 6 条 W0=w0+w1 双元素块，ZA/B 块积模式）+ 4 条 sgn 定理（congrArg）——**ZA/B 块积模式对任意 n 机械可复用**（级联机制机器证明链 n=5→n=9 完整） |"
assert anchor in s, "anchor not found"
s = s.replace(anchor, new, 1)
with io.open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("M17 appended")
