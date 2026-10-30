# -*- coding: utf-8 -*-
"""ins_map195.py — generative_chain_map.md 登记 104az-195"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
t = open(P, encoding="utf-8").read()

anchor = "'为何 FW 表恰好含这些可分解值'未从公设导出）**。"
assert t.count(anchor) == 1, f"anchor count = {t.count(anchor)}"

entry = (
    "**104az-195（§3 ★★ FW 表可分解值完整谱与缺口定位）：可互异三元分解值恰 13 个（30/40/42/48/56/60/64/84/100/105/210/320/675 全素基）、过三约束恰 8 个（30/40/42/56/60/64/84/105）；'为何 8' = 三素因子直积 {30,42,105}（70 缺口）+ 幂混合 {40,56,60,64,84} + 210 和约束全淘汰；★★ FW 缺口谱 {24,70,140}：24 = N_gen×k_max 唯一缺位（N_gen×幂基/静默/对合域/不动点 全 FW）、35 的 ×幂基 升级断裂（两两组合 6 个全 FW、×2 唯独 35→70 ✗、105→210 ✓ 含 N_gen 允许）；家族敏感性：24/70 补位 → 闭包家族 11 → 14；公设级开放项收窄为 '为何 FW 不含 24 与 70'（N_gen×k_max 层级正交禁 + 静默域直积断裂机制，观察级未定论））**。"
)
t = t.replace(anchor, anchor + entry)
open(P, "w", encoding="utf-8").write(t)
print(f"图谱登记 104az-195 完成；len = {len(t)}；has195 = {'104az-195' in t}")
