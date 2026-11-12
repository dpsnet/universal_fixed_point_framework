# -*- coding: utf-8 -*-
"""准确扫描 Lean 源文件里真实的 `def ... := 3`（排除注释与 doc 代码块）。"""
import io, os, re, sys

SRC = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization"

def strip_comments(text):
    """把块注释 /-- -/ 与行注释 -- 替换为等长空白（保留行号）。"""
    out = []
    i = 0
    n = len(text)
    while i < n:
        # 块注释 /- ... -/ （含 /-- 与 /-!），Lean 的块注释可嵌套
        if text.startswith("/-", i):
            depth = 1
            start = i
            i += 2
            while i < n and depth > 0:
                if text.startswith("/-", i):
                    depth += 1
                    i += 2
                elif text.startswith("-/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            seg = text[start:i]
            out.append("".join("\n" if c == "\n" else " " for c in seg))
            continue
        # 行注释 -- （注意 "-/" 已在上面处理，且 "-->" 之类极少见）
        if text.startswith("--", i):
            start = i
            while i < n and text[i] != "\n":
                i += 1
            seg = text[start:i]
            out.append(" " * len(seg))
            continue
        out.append(text[i])
        i += 1
    return "".join(out)

PAT = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+)?(?:private\s+)?def\s+(\w+)\s*(?::\s*([^:=\n]+?))?\s*:=\s*3\s*$")

hits = []
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".lean"):
        continue
    p = os.path.join(SRC, fn)
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    code = strip_comments(raw)
    for idx, line in enumerate(code.split("\n"), 1):
        m = PAT.match(line)
        if m:
            hits.append((fn, idx, m.group(1), (m.group(2) or "").strip(), raw.split("\n")[idx-1].strip()))

print("REAL_DEF_EQ_3_COUNT=%d" % len(hits))
for h in hits:
    print("%-42s L%-5d %-16s %-6s | %s" % (h[0], h[1], h[2], h[3], h[4]))

# 同时统计“有声明无赋值”的裸 3 常量（如 axiom / theorem 中出现 = 3 的）
print()
print("--- 按类型分组 ---")
nat = [h for h in hits if h[3] == "ℕ"]
real = [h for h in hits if h[3] == "ℝ"]
other = [h for h in hits if h[3] not in ("ℕ", "ℝ")]
print("ℕ: %d" % len(nat))
for h in nat: print("   %s L%d %s" % (h[0], h[1], h[2]))
print("ℝ: %d" % len(real))
for h in real: print("   %s L%d %s" % (h[0], h[1], h[2]))
print("其他: %d" % len(other))
for h in other: print("   %s L%d %s : %r" % (h[0], h[1], h[2], h[3]))
