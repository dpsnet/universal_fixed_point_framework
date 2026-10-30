# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(p, encoding="utf-8").read()
for key in ["P7-5c", "m_τ 锚定递归", "1776", "43.37"]:
    idx = t.find(key)
    print("==", key, "idx=", idx)
    if idx > 0:
        print(t[max(0,idx-100):idx+600].replace("\n", " "))
        print()
