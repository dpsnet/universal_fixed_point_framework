# -*- coding: utf-8 -*-
import io
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\roadmap\phase72_n5_symbol_criterion.md"
with io.open(p, "r", encoding="utf-8") as f:
    s = f.read()
lines = s.split("\n")
for i, ln in enumerate(lines):
    if "阶数规律修正" in ln:
        j = ln.find("阶数规律修正")
        print(f"LINE {i}: repr around anchor:")
        print(repr(ln[j-30:j+80]))
        break
