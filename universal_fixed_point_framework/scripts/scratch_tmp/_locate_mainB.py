# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(p, encoding="utf-8").read()
# 找 4.2 倍 / Λ_QCD 缺口 / 主线 B 相关段落
for kw in ["4.2 倍", "Λ_QCD", "Lambda_QCD", "Λ_QCD 缺口", "主线 B"]:
    idx = 0
    hits = 0
    print(f"\n=== {kw} ===")
    while True:
        i = t.find(kw, idx)
        if i < 0: break
        s = max(0, i-150); e = min(len(t), i+150)
        print(f"  [{i}] …{t[s:e].replace(chr(10),' ')}…")
        idx = i + len(kw)
        hits += 1
        if hits >= 6: break
