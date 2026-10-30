# -*- coding: utf-8 -*-
"""生成 N8Table.lean / N9Table.lean：判定表 Lean 可执行编码（通用生成器）。
- N8：23 因子纯 ±1 → 位编码 encode23（权重 2^i）
- N9：27 因子含 0 → 三进制编码 encode27（x=-1→0, x=0→1, x=1→2，权重 3^i）
- 分块（每块 <900 条）防 List cons 嵌套递归深度超限；每项整体类型标注防 MVar 超时
模板：N6Table.lean（位编码 + List 线性查找 + native_decide 抽查）。
"""
import io, json, os, random, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization"
BLOCK = 860

def make_table(json_path, out_name, ns, n_factors, enc_kind, basis_hint=None):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    if 'basis' in data and 'table' in data:
        basis = data['basis']
        table = data['table']
    else:
        basis = basis_hint if basis_hint is not None else [f"f{i}" for i in range(n_factors)]
        table = data
    assert len(basis) == n_factors, (len(basis), n_factors)
    print(f"[{out_name}] basis {n_factors} factors, table {len(table)} entries")

    def parse_key(k):
        return [int(x) for x in k.split(",")]

    def encode(syms):
        if enc_kind == "bit":
            k = 0
            for i, x in enumerate(syms):
                if x == 1:
                    k += 1 << i
            return k
        else:  # ternary
            k = 0
            w = 1
            for i, x in enumerate(syms):
                if x == 1:
                    k += 2 * w
                elif x == 0:
                    k += 1 * w
                w *= 3
            return k

    entries = []
    for k, v in table.items():
        syms = parse_key(k)
        code = encode(syms)
        bg = v['bg'] if isinstance(v, dict) else v
        iv = 0 if abs(float(bg)) < 1e-9 else (1 if float(bg) > 0 else -1)
        entries.append((code, iv))
    from collections import Counter
    dist = Counter(iv for _, iv in entries)
    print(f"  value dist: {dict(dist)}; unique codes: {len(set(c for c, _ in entries))}")
    assert len(set(c for c, _ in entries)) == len(entries), "duplicate codes!"

    # 编码函数体
    if enc_kind == "bit":
        enc_body = " + ".join(f"(if s {i} = 1 then {1 << i} else 0)" for i in range(n_factors))
        enc_name = f"encode{n_factors}"
        enc_doc = f"/-- {n_factors} 因子符号 → 位编码键（位 i = 1 ⟺ s i = 1；权重 2^i） -/"
    else:
        parts = []
        for i in range(n_factors):
            w = 3 ** i
            parts.append(f"(if s {i} = -1 then 0 else if s {i} = 0 then {w} else {2 * w})")
        enc_body = " + ".join(parts)
        enc_name = f"encode{n_factors}"
        enc_doc = f"/-- {n_factors} 因子符号（含 0）→ 三进制编码键（-1→0, 0→1, 1→2；权重 3^i） -/"

    blocks = [entries[i:i + BLOCK] for i in range(0, len(entries), BLOCK)]
    print(f"  blocks: {[len(b) for b in blocks]}")

    L = []
    L.append("/-")
    L.append(f"# {out_name}.lean")
    L.append("")
    L.append("Phase 72 延伸（判定表可执行编码，回溯补）")
    L.append("")
    L.append(f"{len(entries)} 条 {n_factors} 因子基座判定表编码为")
    L.append(f"Lean 可执行查表函数 n{ns}TableValue。编码方案：{enc_kind} 编码为 Nat 键 + List 线性查找")
    L.append("（避免嵌套 if 的 Decidable 递归深度超限；分块定义防 cons 嵌套递归深度超限）。")
    L.append("")
    L.append("诚实定位：本表为数值闭合的经验判据（Python 层 vs BG 递归 0 真违反），")
    L.append("非从解析定义推出的定理；Lean 化价值 = 判定表在形式化环境内可执行、可复现。")
    L.append("-/")
    L.append("import Mathlib.Data.Real.Basic")
    L.append("import Mathlib.Data.Int.Basic")
    L.append("import Mathlib.Tactic")
    L.append("")
    L.append(f"namespace N{ns}Table")
    L.append("")
    L.append(enc_doc)
    L.append(f"def {enc_name} (s : Fin {n_factors} → ℤ) : Nat :=")
    L.append("  " + enc_body)
    L.append("")
    L.append("/-- 线性查找（结构递归；未命中返回 0） -/")
    L.append("def lookup (t : List (Nat × ℤ)) (k : Nat) : ℤ :=")
    L.append("  match t with")
    L.append("  | [] => 0")
    L.append("  | (k', v) :: tl => if k = k' then v else lookup tl k")
    L.append("")
    for bi, blk in enumerate(blocks, 1):
        L.append(f"/-- 判定表块 {bi}/{len(blocks)}（{len(blk)} 条） -/")
        L.append(f"def n{ns}TableBlock{bi} : List (Nat × ℤ) :=")
        L.append("  [")
        for code, iv in blk:
            L.append(f"    (({code}, {iv}) : Nat × ℤ),")
        L.append("  ]")
        L.append("")
    L.append(f"/-- 判定表：{len(entries)} 条 (键, A_BG 值) = 块拼接 -/")
    L.append(f"def n{ns}Table : List (Nat × ℤ) := " + " ++ ".join(f"n{ns}TableBlock{i}" for i in range(1, len(blocks) + 1)))
    L.append("")
    L.append(f"/-- n={ns} 判定表函数：{n_factors} 因子符号 → A_BG ∈ {{0,±1}} -/")
    L.append(f"def n{ns}TableValue (s : Fin {n_factors} → ℤ) : ℤ := lookup n{ns}Table ({enc_name} s)")
    L.append("")
    L.append("-- ==================== 抽查定理（native_decide 机器计算验证） ====================")
    rng = random.Random(7)
    samples = [("all_plus", [1] * n_factors)]
    allkeys = list(table.keys())
    for _ in range(5):
        samples.append(("r" + str(_), parse_key(rng.choice(allkeys))))
    for name, syms in samples:
        pat = "| " + " | ".join(f"⟨{i}, _⟩ => {syms[i]}" for i in range(n_factors))
        code = encode(syms)
        val = next((v for c, v in entries if c == code), 0)
        L.append(f"example : n{ns}TableValue (fun i => match i with {pat} | _ => 0) = {val} := by")
        L.append("  native_decide")
    L.append("")
    L.append(f"end N{ns}Table")

    out = os.path.join(SRC, f"{out_name}.lean")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("written:", out, "lines:", len(L))

if __name__ == "__main__":
    # N8Table
    make_table(os.path.join(SCRIPT_DIR, "paperX_n8_base23_table.json"),
               "N8Table", "8", 23, "bit")
    # N9Table（无 basis 字段，用 BASE27）
    make_table(os.path.join(SCRIPT_DIR, "paperX_n9_base27_table.json"),
               "N9Table", "9", 27, "ternary",
               basis_hint=['s2_3','s2_3456789','s23_456789','s234_56789','s2345678_9',
                           's3_4','s3_456789','s34_56789','s345_6789',
                           's4_5','s4_56789','s45678_9',
                           's5_6','s5_678','s56_78','s5_6789','s5678_9',
                           's6_7','s67_8','s6_789','s678_9',
                           's7_8','s7_89','s78_9','s8_9',
                           's1_2345','s123_456789'])
