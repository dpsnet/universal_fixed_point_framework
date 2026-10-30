# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
for kw in ["织a", "0.0186", "18π"]:
    i = t.find(kw)
    print(f"--- {kw}: idx={i} ---")
    if i >= 0:
        print(t[max(0, i-300):i+400].replace("\n", " "))
