# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
print("RS len:", len(t), "; has167:", "104az-167" in t, "; 修正来源两分:", "修正来源两分" in t)
g = open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md", encoding="utf-8").read()
print("图谱 167:", "104az-167" in g)
