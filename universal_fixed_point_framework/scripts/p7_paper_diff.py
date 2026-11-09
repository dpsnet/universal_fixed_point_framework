# -*- coding: utf-8 -*-
import difflib, io

A = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"
B = r"C:\Users\dps_n\AppData\Local\Temp\head_paper.md"

a = io.open(A, encoding="utf-8", errors="ignore").read().split("\n")
b = io.open(B, encoding="utf-8", errors="ignore").read().split("\n")

sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
out = []
n_add = n_del = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    out.append("### %s  HEAD[%d:%d] -> WORK[%d:%d]" % (tag, i1 + 1, i2, j1 + 1, j2))
    for l in b[i1:i2][:6]:
        out.append("  - " + l[:160])
        n_del += 1
    for l in a[j1:j2][:6]:
        out.append("  + " + l[:160])
        n_add += 1
    if len(out) > 60:
        break

io.open(r"C:\Users\dps_n\AppData\Local\Temp\paper_diff.txt", "w", encoding="utf-8").write("\n".join(out))
print("DIFF blocks written, add=%d del=%d" % (n_add, n_del))
