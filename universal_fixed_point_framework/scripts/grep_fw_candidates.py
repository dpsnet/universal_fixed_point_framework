# -*- coding: utf-8 -*-
"""grep_fw_candidates.py — 检查候选框架量整数在 RESEARCH_STATE.md 中的出现次数（独立 token）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
vals = [18,20,24,27,28,30,32,36,40,45,48,50,70,84,90,120,140,168,175,240,280,315,336,420,560,630,840]
for v in vals:
    # 独立整数 token（前后非数字）
    cnt = len(re.findall(rf"(?<![0-9]){v}(?![0-9])", t))
    print(f"{v} : {cnt}")
