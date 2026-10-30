# -*- coding: utf-8 -*-
"""n=6 判定表 → Lean 生成器 v2：paperX_n6_base12_table.json → N6Table.lean。
方案（避免 609 层嵌套 if 的 Decidable 递归深度超限）：
  - encode12 : (Fin 12 → ℤ) → Nat（位编码：s i = 1 → 2^i，s i = -1 → 0）
  - n6Table : List (Nat × ℤ)（609 条键值对，无嵌套）
  - lookup : List (Nat × ℤ) → Nat → ℤ（结构递归线性查找）
  - n6TableValue = lookup n6Table ∘ encode12
  - 抽查：example + native_decide（机器计算验证）
"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SCRIPT_DIR, "paperX_n6_base12_table.json")
OUT = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\N6Table.lean"

with open(SRC, encoding="utf-8") as f:
    table = json.load(f)

items = []
for k, v in table.items():
    sigs = [int(x) for x in k.split(",")]
    assert len(sigs) == 12 and v in (0, 1, -1)
    items.append((tuple(sigs), int(v)))
print(f"表条目: {len(items)}  非零: {sum(1 for _, v in items if v != 0)}")

# 位编码：位 i = 1 iff sig i = 1（权重 2^i）
def enc(sigs):
    total = 0
    for i, sv in enumerate(sigs):
        if sv == 1:
            total += 1 << i
    return total

lines = []
lines.append("/-")
lines.append("# N6Table.lean")
lines.append("")
lines.append("Phase 72 延伸（n=6 判据形式化·第二步：判定表可执行编码）")
lines.append("")
lines.append("609 条 12 因子基座判定表（paperX_n6_base12_table.json，独立复核 0 真违反）编码为")
lines.append("Lean 可执行查表函数 n6TableValue。编码方案：12 因子符号位编码为 Nat 键 + List 线性查找")
lines.append("（避免 609 层嵌套 if 的 Decidable 递归深度超限）。")
lines.append("")
lines.append("诚实定位：本表为数值闭合的经验判据（Python 层 vs BG 递归 0 真违反），")
lines.append("非从 (32) 解析定义推出的定理；Lean 化价值 = 判定表在形式化环境内可执行、可复现。")
lines.append("-/")
lines.append("import Mathlib.Data.Real.Basic")
lines.append("import Mathlib.Data.Int.Basic")
lines.append("import Mathlib.Tactic")
lines.append("")
lines.append("namespace N6Table")
lines.append("")
lines.append("/-- 12 因子符号 → 位编码键（位 i = 1 ⟺ s i = 1；权重 2^i） -/")
lines.append("def encode12 (s : Fin 12 → ℤ) : Nat :=")
terms = []
for i in range(12):
    terms.append(f"(if s {i} = 1 then {1 << i} else 0)")
lines.append("  " + " + ".join(terms))
lines.append("")
lines.append("/-- 线性查找（结构递归；未命中返回 0） -/")
lines.append("def lookup (t : List (Nat × ℤ)) (k : Nat) : ℤ :=")
lines.append("  match t with")
lines.append("  | [] => 0")
lines.append("  | (k', v) :: tl => if k = k' then v else lookup tl k")
lines.append("")
lines.append("/-- 判定表：609 条 (键, A_BG 值) -/")
lines.append("def n6Table : List (Nat × ℤ) :=")
for idx, (sigs, v) in enumerate(items):
    if idx == 0:
        lines.append("  [ (" + str(enc(sigs)) + ", " + str(v) + "),")
    else:
        lines.append("    (" + str(enc(sigs)) + ", " + str(v) + "),")
lines.append("  ]")
lines.append("")
lines.append("/-- n=6 判定表函数：12 因子符号 → A_BG ∈ {0,±1} -/")
lines.append("def n6TableValue (s : Fin 12 → ℤ) : ℤ := lookup n6Table (encode12 s)")
lines.append("")
lines.append("-- ==================== 抽查定理（native_decide 机器计算验证） ====================")
checks = items[:3] + [it for it in items if it[1] != 0][:3]
for sigs, v in checks:
    arms = " | ".join(f"⟨{i}, _⟩ => {sigs[i]}" for i in range(12))
    lines.append(f"example : n6TableValue (fun i => match i with | {arms} | _ => 0) = {v} := by")
    lines.append("  native_decide")
lines.append("")
lines.append("end N6Table")
lines.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"DONE -> {OUT} ({len(lines)} 行)")
