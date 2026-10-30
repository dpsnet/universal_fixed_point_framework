# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(p, encoding="utf-8").read()
for key in ('104az-143', '104az-145', '104az-146'):
    i = t.find(key)
    if i >= 0:
        print(f"===== {key} @ idx {i} =====")
        print(t[i:i+2600])
        print()
