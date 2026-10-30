# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
print("RS len:", len(t), "; has171-173:", all(f"104az-{n}" in t for n in [171,172,173]), "; D双途径:", "B − 2/3375" in t)
g = open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md", encoding="utf-8").read()
print("图谱 171-173:", all(f"104az-{n}" in g for n in [171,172,173]))
