# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(p, encoding="utf-8").read()
for n in [148, 149, 150, 151]:
    s = "104az-%d" % n
    idx = t.find(s)
    print(n, "idx=", idx)
    if idx > 0:
        # 打印该段前 200 字符
        print("  ", t[idx:idx+200].replace("\n", " ")[:200])
# 总长与最后段
print("len", len(t))
