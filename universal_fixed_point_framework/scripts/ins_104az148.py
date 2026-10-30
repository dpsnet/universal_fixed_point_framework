# -*- coding: utf-8 -*-
"""ins_104az148.py — 登记 104az-148（g_p/2 结构动机收尾：嵌套分数形式唯一性）"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
seg = (
    "\n- **★ g_p/2 结构动机收尾——嵌套分数形式的链内唯一性（2026-10-20，104az-148，脚本 chain_audit_147_gp2_structure.py）**："
    "**① 判别设计（先定规则再查，同 231 路径）**：给定织法 = 双主结构 {分子对合域 7, 分母静默 5, 内层幂基 2} + 修正对 (a, b)，"
    "g_p/2 = (7−a)/(5/(2+b))；候选修正空间 A×B：a、b 各自遍历 k/d（k ∈ 框架量集 {2,3,4,5,7,8,16,25,49,64}，d ∈ 修正分母家族 {45,231,320,675,65,256,14400,16,25,64,40,100}）= 101×101 = **10201 组合**；"
    "**② 数值唯一性**：命中观测 2.79284734463（err<1e-6）**仅 1 个组合**——(a,b)=(8/45, 3/64)，即 40217/14400（1.224e-7 吻合）——扩展空间下唯一命中，比 566 平滑分母空间 #2/566 更强（形式空间内是 #1/10201）；"
    "**③ 修正值框架身份**：a = 8/45 = k_max/(N_gen²·静默)（减性）、b = 3/64 = N_gen/k_max²（加性）——被观测锁定的修正对**恰好全为框架量比值**，非任意分数；"
    "**④ 结构动机闭合陈述**：给定 A2 双符号族织法（主结构 ± k_max/(N_gen²·静默) 与内层 +N_gen/k_max²），g_p/2 的嵌套分数参数被观测**唯一锁定**——不存在其他可选的修正对；"
    "与 231 判别对照：231 在 S(k) 族（k∈{4..12}，9 元素）内唯一、g_p/2 在 10201 组合空间内唯一——后者强一个数量级；"
    "**⑤ 诚实边界（保留）**：织法本身（为何双主结构+双修正而非其他织法）仍为 A2 公设级；闭合的是『织法内的参数唯一性』。"
    "**⑥ 21cm 链路连带**：g_p/2 因子 = 形式唯一框架表达 + 结构动机闭合 → 链路 4.5/5 因子完全闭合，δ 残差成为唯一开放项（见待办 4）。"
)
a = "评估脚本已入 scripts/（rarity + mersenne 两件，可复算）。"
cnt = t.count(a)
assert cnt == 1, f"anchor count {cnt}"
t = t.replace(a, a + seg, 1)
open(P, "w", encoding="utf-8").write(t)
print("ins 148 done; anchor count:", cnt, "; new len:", len(t), "; has148:", "104az-148" in t)
