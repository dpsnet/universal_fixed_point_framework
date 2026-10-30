# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
print("len:", len(t))
for n in [152, 153]:
    print("has", n, "104az-%d" % n in t)
G = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
g = open(G, encoding="utf-8").read()
print("--- 图谱 ---")
print("E0 in §0:", "E0『对数-指数对" in g)
print("三链 in §4:", "三链判别矩阵完成（104az-152）" in g)
print("更新153:", "104az-153" in g)
