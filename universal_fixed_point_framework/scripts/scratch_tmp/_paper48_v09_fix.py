# -*- coding: utf-8 -*-
import io
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
t = io.open(p, encoding="utf-8").read()
old = "全样本（400弱场）后$p$值从v9b的0.014降至0.00786，进入$p<0.01$的\"非常显著\"区间。"
new = "全样本（400弱场）后$p$值从早期迭代的0.014降至0.00786，进入$p<0.01$的\"非常显著\"区间。"
assert old in t, "not found"
t = t.replace(old, new)
io.open(p, "w", encoding="utf-8").write(t)
print("fixed")
