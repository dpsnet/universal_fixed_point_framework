# -*- coding: utf-8 -*-
# ins_rm_104az140.py — roadmap 登记 104az-140（插在 139 段之后）
import io

p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase102b_full_endogenous_roadmap.md"
with io.open(p, encoding="utf-8") as f:
    t = f.read()

seg = """- **★★ 预言 C 宿主判别 + 闭包等价机器证明（2026-10-20，Phase 104az-140）**：**① 线频率比宿主**：Δλ₁₆ = 231/5800 = (ν_γ/R)·(11/58) = (21/100)·(11/58)——ν_γ/R = 1/4−1/25 = 21/100（n=5 静默层 Balmer Hγ，与 DESI 分子族同源）、11 = N_active+k_max（塔第三项）、58 = k_max×对合域+幂基（B_th 链因子）；**② 分子双因子**：231 = 21×11（观测侧 DESI Hγ 分子基 × 代数侧塔第三项）；**③ 判别签名**：修正量 1/5800（相对 0.431%），41 MG 谱隙观测量可分辨；**④ 恒等闭环**：400×(232/231)×(231/5800) = 16（预言 C 精确）；**⑤ ★★★ 7-平滑⟺闭包机器证明**：`SqDiffClosure.lean` 新增 Smooth7 谓词 + closure_iff_adjacent_smooth（双向：因子继承 + Euclid）——137 段"数值验证非 Lean 证明"边界正式闭合；**⑥ 675/Mordell 代数恒等固化**（mordell_solution/closure_675_dual 等），唯一性登记开放项；Lean：InvolutionTripleGap 3051 + SqDiffClosure 3049 jobs 零 sorry 零 warning；诚实边界：线频率比分解为代数重写（非独立先验预言），宿主物理观测量待锁定。
"""

a = "诚实边界：统计为数值验证，质数偏好机制未形式化。"
c = t.count(a)
print("anchor count:", c)
assert c == 1, "anchor not unique"
t2 = t.replace(a, a + "\n" + seg, 1)
with io.open(p, "w", encoding="utf-8") as f:
    f.write(t2)
print("RM new len:", len(t2))
print("done")
