# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
print("RS len:", len(t), "; has163:", "104az-163" in t, "; NGKMOne:", "NGKMOneIdentity.lean" in t)
g = open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md", encoding="utf-8").read()
print("图谱 163:", "104az-163" in g)
import os
L = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\NGKMOneIdentity.lean"
print("lean 文件存在:", os.path.exists(L), "; 大小:", os.path.getsize(L) if os.path.exists(L) else 0)
