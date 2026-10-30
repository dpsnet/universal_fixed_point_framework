# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
print("RS len:", len(t), "; has158:", "104az-158" in t)
g = open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md", encoding="utf-8").read()
print("图谱 μ_t 行:", "氚核磁矩 μ_t" in g, "; 更新158:", "104az-158" in g)
