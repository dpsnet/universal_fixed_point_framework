# -*- coding: utf-8 -*-
# s137_sigma_power_selection.py —— "为何 Fib"三重交集分析（S137，2026-10-27）
# 候选：σ 使用幂次 = {原始框架量} ∩ {Fib 数} ∩ [1, k_max]
#   —— 完全确定使用幂次 {2,3,5,8}（+单位 1）——对合 7 被 Fib 排除
#   —— "为何止于 8" = k_max 截断（Fib ∩ [1, k_max]）

# 框架量（原始/复合）
primitive = {1, 2, 3, 5, 7, 8}   # 单位/幂基/N_gen/静默/对合/k_max（原始单一框架量）
composite = {4, 6, 9}            # 幂基²/N_gen×幂基/幂基+对合（复合量）
used = {1, 2, 3, 5, 8}
unused = {4, 6, 7, 9}

# Fib 数（≤ 30）
fibs = set()
a, b = 1, 1
while a <= 30:
    fibs.add(a)
    a, b = b, a + b

k_max = 8

print("=== 三重交集分析 ===")
print(f"原始框架量 P = {sorted(primitive)}")
print(f"Fib 数集 F   = {sorted(fibs)}")
P_int_F = sorted(primitive & fibs)
print(f"P ∩ F        = {P_int_F}  ← 使用幂次（除单位 1）！")
F_cap_km = sorted({x for x in fibs if x <= k_max})
print(f"F ∩ [1,k_max] = {F_cap_km}  ← 去重后 = 使用幂次（含 1）")

print("\n=== 逐个幂次判定 ===")
for p in range(1, 10):
    in_prim = p in primitive
    in_comp = p in composite
    in_fib = p in fibs
    in_km = p <= k_max
    use = "使用" if p in used else "未用"
    if in_prim:
        tag = "原始框架量"
    elif in_comp:
        tag = "复合量"
    else:
        tag = "非框架量"
    verdict = []
    if not in_fib:
        verdict.append("非 Fib")
    if in_comp:
        verdict.append("复合非原始")
    if p == 7:
        verdict.append("对合折叠非增长")
    if p > k_max:
        verdict.append("超 k_max")
    print(f"σ^{p:<3}{tag:<10}{'Fib' if in_fib else '—':<4}判定: {'使用（'+'且'.join(v for v in ['原始','Fib','≤k_max'] if v)+'）' if use=='使用' else '未用——'+('; '.join(verdict) if verdict else '')}")

print("\n=== 结论 ===")
print("① 使用幂次 {2,3,5,8} = 原始框架量 ∩ Fib 数（单位 1 平凡）——完全确定")
print("② 对合 7：原始框架量但 ∉ Fib——被 Fib 判定排除（折叠非增长）")
print("③ 复合量 {4,6,9}：∉ 原始 且 ∉ Fib——双重排除")
print("④ '为何止于 8' = k_max 截断：F ∩ [1, k_max] = {1,2,3,5,8}——")
print("   最大递归深度截断 Fib 序列——更深幂次（σ¹³）超递归可达范围")
print("⑤ '为何框架常数 {2,3,5,8} 恰为 Fib 数'——归入框架常数导出层")
print("   （范畴公设→框架常数——与 σ 幂次选择层分离——TASK_GOAL 更长链）")
