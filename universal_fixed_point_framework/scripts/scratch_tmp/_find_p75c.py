# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(p, encoding="utf-8").read()
# 全部含 "P7-5c" 的行
lines = t.split("\n")
for i, ln in enumerate(lines):
    if "P7-5c" in ln or "锚定递归" in ln or "43.374" in ln or "16·dH" in ln or "16·d_H" in ln:
        print(i, ":", ln[:200])
