# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(p, encoding="utf-8").read()
# 找 d_H 公式出现的行
for m in re.finditer(r"d_H", t):
    s = max(0, m.start()-80)
    e = min(len(t), m.end()+80)
    frag = t[s:e].replace("\n", " ")
    print("...", frag, "...")
    print("---")
