# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
print("len:", len(t), "; has154:", "104az-154" in t)
G = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
g = open(G, encoding="utf-8").read()
print("图谱 §6 353:", "353 = 45·8−7" in g, "; 更新154:", "104az-154" in g)
