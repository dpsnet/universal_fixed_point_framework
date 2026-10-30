# -*- coding: utf-8 -*-
"""ins_map194.py — generative_chain_map.md 登记 104az-194"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
t = open(P, encoding="utf-8").read()

anchor = "'为何恰为 1+11'未机制化）**。"
assert t.count(anchor) == 1, f"anchor count = {t.count(anchor)}"

entry = (
    "**104az-194（§3 ★★ 闭包家族结构刻画——'为何 1+11'机制闭合）：三约束结构定理 A 零误报零漏报（无单位 3 元闭包 ⟺ 素基 ⊆{2,3,5,7} ∧ 全和 ≤15 ∧ 全积/两两积 ∈ FW——455 候选 286→23→11 = 真闭包 11）；结构定理 B 互异分解计数精确 = 11（30/40/42/56/64/105 单分解 + 60 三分解 + 84 双分解——'为何 11' = FW 表乘法分解 + 和约束组合计数）；结构定理 C 4 元闭包 = {1} ∪ 无单位 3 元闭包全提升自动（积谱含两两积、和谱含两两和、a≤15 → 1+a 自动——结构必然而非巧合）；淘汰原因谱：24 = N_gen×k_max 缺口淘汰 48 两分解、和 >15 淘汰 100/210/320/675；★★ 42/105 分解级解释——差异因子 {2|5} = {幂基|静默} 获分解强制（42 = 2×3×7、105 = 3×5×7 唯一互异分解）；瓶颈敏感点：24 若获身份家族扩至 12；诚实边界：'为何 FW 表恰好含这些可分解值'未从公设导出）**。"
)
t = t.replace(anchor, anchor + entry)
open(P, "w", encoding="utf-8").write(t)
print(f"图谱登记 104az-194 完成；len = {len(t)}；has194 = {'104az-194' in t}")
