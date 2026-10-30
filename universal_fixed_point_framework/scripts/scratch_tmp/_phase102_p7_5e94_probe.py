# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-94：高场 m 通道单态化判别——通道数闭式 vs A2 n_total
================================================================
假说：高场下每个 m 通道只剩 n_r=0 基态——通道数 = 束缚态总数 n_total
  通道数(B) = floor(2(1/B − 1/7)) + 1（统一闭式 1/B*=|m|/2+1/7+1/(7·2^|m|) 的判定）
判别：A2 14 点 n_total(B) vs 通道数闭式——找单态化临界场强（n_total = 通道数 的 B 域）
Paper 48 对接：强场样本（109-778 MG）中 B≥临界 的星——束缚态数 = 通道数闭式
"""
import json, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
A2 = json.load(open(os.path.join(BASE, "_gaia_abs", "paperX_eta_sc_B_bound.json"), encoding="utf-8"))

# A2 数据格式探测
print("A2 数据结构：", type(A2))
if isinstance(A2, dict):
    for k in list(A2.keys())[:5]:
        print("  key:", k, "->", A2[k] if not isinstance(A2[k], (list, dict)) else str(A2[k])[:80])
