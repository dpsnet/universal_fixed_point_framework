# -*- coding: utf-8 -*-
import io, re

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"
OUT = r"C:\Users\dps_n\AppData\Local\Temp\v13_final_check.txt"

t = io.open(P, encoding="utf-8").read()
lines = t.split("\n")
res = []

res.append("== 结构标题 ==")
for i, l in enumerate(lines, 1):
    if re.match(r"^#{2,4} (1\.\d|9\.1|9\.2|12\.4)", l):
        res.append("  L%-5d %s" % (i, l.strip()))

res.append("")
res.append("== 交叉引用 ==")
for pat in [r"§1\.[2-5]", r"§9\.1b", r"§12\.4\.1", r"§12\.4\.2", r"§9\.2f"]:
    hits = [(i + 1, l.strip()[:90]) for i, l in enumerate(lines) if re.search(pat, l)]
    res.append("  [%s] n=%d" % (pat, len(hits)))
    for ln, tx in hits[:6]:
        res.append("     L%d %s" % (ln, tx))

res.append("")
res.append("== 关键处置标记 ==")
marks = {
    "N1_g2_retract": "v1.3 撤销声明（评审 N1 处置）",
    "N1_branchA": "分支 A（活跃步）",
    "N2_fail_ledger": "失败核算",
    "N3_C1_blockquote": "C1 的精确地位（v1.3 修正，评审 N3）",
    "N4_Nactive_abstract": "N_active=3 有整数根 {3,5}",
    "N5_9_1b_header": "#### 9.1b",
    "sin2theta_census": "9.2f",
    "codata_protocol": "12.4.1",
}
for k, s in marks.items():
    res.append("  %-22s present=%s" % (k, s in t))

res.append("")
res.append("== 摘要指标句 ==")
for i, l in enumerate(lines, 1):
    if "韦达方程" in l and ("整数根" in l):
        res.append("  L%d: %s" % (i, l.strip()[:400]))

res.append("")
res.append("== 版本头 ==")
for i, l in enumerate(lines[:12], 1):
    if "版本" in l or "Lean 形式化状态" in l:
        res.append("  L%d: %s" % (i, l.strip()[:300]))

io.open(OUT, "w", encoding="utf-8").write("\n".join(res))
print("WROTE", OUT, len(res), "rows")
