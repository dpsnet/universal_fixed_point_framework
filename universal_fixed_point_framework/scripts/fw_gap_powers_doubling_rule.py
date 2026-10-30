# -*- coding: utf-8 -*-
"""FW 缺口机制候选验证：×幂基升级法则（2026-10-26）

FW 表两两组合 ×2 升级：6→12 ✓、10→20 ✓、14→28 ✓、15→30 ✓、21→42 ✓、
35→70 ✗（唯一断裂）。
候选法则：×幂基（×2）升级要求源值含活跃（N_gen=3）或幂基（2）——
纯静默域（静默×对合域 = 5×7 = 35）被禁。
验证：遍历 {2,3,5,7} 两两组合（FW 全在）+ ×2 升级的源值因子构成。
"""
import itertools

# 框架常数
powers, ngen, silence, involution = 2, 3, 5, 7
pairs = [(a, b) for a, b in itertools.combinations([powers, ngen, silence, involution], 2)]

print("=== FW 两两组合 ×2 升级表 ===")
for a, b in pairs:
    src = a * b
    dst = 2 * src
    # 源值是否含活跃（3）或幂基（2）
    has_active = (a == ngen or b == ngen)
    has_power = (a == powers or b == powers)
    has_silence = (a == silence or b == silence)
    has_invol = (a == involution or b == involution)
    # 已登记的 FW 升级状态（104az-195）
    status = {12: "✓", 20: "✓", 28: "✓", 30: "✓", 42: "✓", 70: "✗ 断裂"}.get(dst, "?")
    # 法则预测：含活跃或幂基 → 允许；纯静默域（静默×对合域）→ 禁
    rule_allow = has_active or has_power
    rule_pred = "允许" if rule_allow else "禁"
    match = "一致" if (rule_pred == "允许" and status.startswith("✓")) or (rule_pred == "禁" and status.startswith("✗")) else "不一致"
    print(f"  {a}×{b} = {src} → ×2 = {dst}：活跃={has_active} 幂基={has_power} 静默={has_silence} 对合={has_invol} | 法则={rule_pred} FW={status} {match}")

print()
print("=== 反例排查 ===")
print("10 = 幂基×静默（含幂基 ✓ 允许）、14 = 幂基×对合域（含幂基 ✓ 允许）")
print("15 = 活跃×静默（含活跃 ✓ 允许）、21 = 活跃×对合域（含活跃 ✓ 允许）")
print("35 = 静默×对合域（无活跃无幂基——纯静默域——禁 → 70 ✗）")
print()
print("=== 140/105 对照 ===")
print("105 = 3×5×7（含活跃 3）→ 210 ✓（104az-195：105→210 ✓）")
print("140 = 2×70（70 断裂继承）→ ✗——与 105→210 对照：含活跃 vs 纯静默域")
print()
print("=== 语义候选 ===")
print("'幂基翻倍升级（×2）需要链上活跃（N_gen=3）或幂基（2）节点在场——")
print("纯静默域直积（静默×对合域 = 5×7）无活跃/幂基支撑——翻倍断裂'")
print("——70 缺位机制候选（104az-195'静默域直积禁'的具体化）——观察级待全表验证")
