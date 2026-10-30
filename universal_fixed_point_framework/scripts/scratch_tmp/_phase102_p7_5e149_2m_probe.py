# -*- coding: utf-8 -*-
"""
P7-5e-149：2^m 静默族机制判别——1/(7·2^m) 指数精确性检验
================================================================
闭式 1/B* = |m|/2 + 1/7 + 1/(7·2^m)（129：256/256 点 0.02% 级）。
缺口域截距 = 1/7·(1+2^{-m})。判别：
P1 小 m（1..32）闭式残差 δ_cl = cl − 1/B* 的量级与结构
P2 残差 vs 1/(7·2^m)：指数精确（残差 ~0.02% 均匀）或带 O(1/m) 修正
P3 残差/1(7·2^m) 的 m 依赖 → 判别 2^{-m} 纯指数 or 修正指数
P4 框架候选：2^{-m} = e^{-m ln2}（隧穿因子 e^{-S} 形式？）
"""
import json, numpy as np

print("=== P7-5e-149 2^m 静默族机制判别 ===", flush=True)
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
# 读三源数据
data = {}
for fn, tag in [("_phase102_p7_5e_fullchain_tridiag.json", "tridiag"),
                ("_phase102_p7_5e117_m32_scan.json", "m32"),
                ("_phase102_p7_5e124_spectral_m256.json", "spec256")]:
    try:
        with open(base + "\\" + fn, "r", encoding="utf-8") as f:
            d = json.load(f)
        data[tag] = d
        print("  %s 读入（键：%s）" % (tag, list(d.keys())[:8]), flush=True)
    except Exception as e:
        print("  %s 读取失败：%s" % (tag, e), flush=True)

# 从 tridiag 提取 (m, B*)——尝试常见结构
def find_bstar(d):
    out = {}
    # 尝试多种结构
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict) and "B" in v and "m" in v:
                out[abs(v["m"])] = v["B"]
            elif isinstance(v, (int, float)) and isinstance(k, str) and k.isdigit():
                pass
    return out

# 更通用：搜索 Bstar/bstar/B_star 等键
print("--- 数据结构探测 ---", flush=True)
for tag, d in data.items():
    if isinstance(d, dict):
        sample_keys = list(d.keys())[:5]
        print("  %s：dict，样例键 %s，首值类型 %s" % (tag, sample_keys, type(d[list(d.keys())[0]]).__name__), flush=True)
    elif isinstance(d, list):
        print("  %s：list 长度 %d，首元素 %s" % (tag, len(d), str(d[0])[:100]), flush=True)
