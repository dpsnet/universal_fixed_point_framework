# -*- coding: utf-8 -*-
"""落盘①：Paper 48 §4.3.8 无B偏倚交叉引用；Paper 58 §10 结论域声明。"""
import io

def rd(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()
def wr(p, t):
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(t)

# Paper 48
P48 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper48_topological_forbidden_frequency.md"
t = rd(P48)
old = "作为残余不确定性保留（见7.5节）。"
new = "作为残余不确定性保留（见7.5节）。检测筛选的无偏性另经§4.4显式检验（未检测279颗$\\log_{10}B$中位2.49 vs 已检测236颗2.43——筛选不以磁场强度为转移）。"
assert t.count(old) == 1, "p48 anchor"
t = t.replace(old, new)
wr(P48, t)
print("P48 OK")

# Paper 58
P58 = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper58_channel_separation_single_minus.md"
t = rd(P58)
old58 = "**M83d 强场扩展**（Kepler+ 2013 60 颗，进行中）"
new58 = "**M83d 强场扩展**（Kepler+ 2013 60 颗，进行中）。**结论域声明**：P83 结论域为 MG 级磁场白矮星（B 0.8–778 MG）——kG 级真弱场不在 Amorim 目录（Zeeman 分裂不可检测，目录固有边界），结论不外推至 kG 级"
assert t.count(old58) == 1, "p58 anchor"
t = t.replace(old58, new58)
wr(P58, t)
print("P58 OK")
