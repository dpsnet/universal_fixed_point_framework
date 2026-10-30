# -*- coding: utf-8 -*-
"""生成 N7Table.lean：n=7 判定表（2577 条 16 因子位编码键）Lean 可执行编码。
模板：N6Table.lean（位编码 + List 线性查找 + native_decide 抽查）。
"""
import io, json, os, random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization"

with open(os.path.join(SCRIPT_DIR, "paperX_n7_base16_table.json"), encoding="utf-8") as f:
    data = json.load(f)
table = data["table"]
basis = data["basis"]
n_factors = len(basis)
assert n_factors == 16, n_factors
print(f"判定表 {len(table)} 条, 基座 {n_factors} 因子")

def encode(syms):
    k = 0
    for i, x in enumerate(syms):
        if x == 1:
            k += 1 << i
    return k

def parse_key(k):
    return tuple(1 if x == "1" else -1 for x in k.split(","))

entries = []
for k, v in table.items():
    syms = parse_key(k)
    code = encode(syms)
    iv = 0 if abs(float(v)) < 1e-9 else (1 if float(v) > 0 else -1)
    entries.append((code, iv))

# 值分布
from collections import Counter
dist = Counter(iv for _, iv in entries)
print("值分布:", dict(dist))
assert len(set(code for code, _ in entries)) == len(entries), "duplicate keys"

# encode16 定义
enc_body = " + ".join(
    f"(if s {i} = 1 then {1 << i} else 0)" for i in range(16)
)

lines = []
lines.append("/-")
lines.append("# N7Table.lean")
lines.append("")
lines.append("Phase 72 延伸（n=7 判据形式化·判定表可执行编码，回溯补）")
lines.append("")
lines.append("2577 条 16 因子基座判定表（paperX_n7_base16_table.json，独立 2×20000 复核 0 真违反）编码为")
lines.append("Lean 可执行查表函数 n7TableValue。编码方案：16 因子符号位编码为 Nat 键 + List 线性查找")
lines.append("（避免 2577 层嵌套 if 的 Decidable 递归深度超限）。")
lines.append("")
lines.append("诚实定位：本表为数值闭合的经验判据（Python 层 vs BG 递归 0 真违反），")
lines.append("非从解析定义推出的定理；Lean 化价值 = 判定表在形式化环境内可执行、可复现。")
lines.append("-/")
lines.append("import Mathlib.Data.Real.Basic")
lines.append("import Mathlib.Data.Int.Basic")
lines.append("import Mathlib.Tactic")
lines.append("")
lines.append("namespace N7Table")
lines.append("")
lines.append("/-- 16 因子符号 → 位编码键（位 i = 1 ⟺ s i = 1；权重 2^i） -/")
lines.append(f"def encode16 (s : Fin 16 → ℤ) : Nat :=")
lines.append("  " + enc_body)
lines.append("")
lines.append("/-- 线性查找（结构递归；未命中返回 0） -/")
lines.append("def lookup (t : List (Nat × ℤ)) (k : Nat) : ℤ := ")
lines.append("  match t with")
lines.append("  | [] => 0")
lines.append("  | (k', v) :: tl => if k = k' then v else lookup tl k")
lines.append("")
# 分块定义：2577 条 cons 嵌套超递归深度上限（~1000 层），切 3 块（各 <900）后 ++ 拼接
BLOCK = 860
blocks = [entries[i:i + BLOCK] for i in range(0, len(entries), BLOCK)]
print("blocks:", [len(b) for b in blocks])

lines.append("")
for bi, blk in enumerate(blocks, 1):
    lines.append(f"/-- 判定表块 {bi}/{len(blocks)}（{len(blk)} 条） -/")
    lines.append(f"def n7TableBlock{bi} : List (Nat × ℤ) :=")
    lines.append("  [")
    for code, iv in blk:
        lines.append(f"    (({code}, {iv}) : Nat × ℤ),")
    lines.append("  ]")
    lines.append("")
lines.append("/-- 判定表：%d 条 (键, A_BG 值) = 块拼接 -/" % len(entries))
lines.append("def n7Table : List (Nat × ℤ) := " + " ++ ".join(f"n7TableBlock{i}" for i in range(1, len(blocks) + 1)))
lines.append("")
lines.append("/-- n=7 判定表函数：16 因子符号 → A_BG ∈ {0,±1} -/")
lines.append("def n7TableValue (s : Fin 16 → ℤ) : ℤ := lookup n7Table (encode16 s)")
lines.append("")
lines.append("-- ==================== 抽查定理（native_decide 机器计算验证） ====================")

# 抽查：全 +1 + 5 个随机模式
rng = random.Random(7)
samples = [("all_plus", [1] * 16)]
allkeys = list(table.keys())
for _ in range(5):
    k = rng.choice(allkeys)
    samples.append((k, list(parse_key(k))))

def sample_fn(name, syms):
    pat = "| " + " | ".join(
        f"⟨{i}, _⟩ => {syms[i]}" for i in range(16)
    )
    code = encode(syms)
    val = next((v for c, v in entries if c == code), 0)
    return f"example : n7TableValue (fun i => match i with {pat} | _ => 0) = {val} := by"

for name, syms in samples:
    lines.append(sample_fn(name, syms))
    lines.append("  native_decide")
lines.append("")
lines.append("end N7Table")

out = os.path.join(SRC, "N7Table.lean")
with io.open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("written:", out, "lines:", len(lines))
