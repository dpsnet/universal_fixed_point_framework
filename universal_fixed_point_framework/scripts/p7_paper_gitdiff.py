# -*- coding: utf-8 -*-
import hashlib, io

A = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"
B = r"C:\Users\dps_n\AppData\Local\Temp\head_paper.md"

def h(p):
    b = open(p, "rb").read()
    return len(b), hashlib.md5(b).hexdigest()

for p, tag in ((A, "WORK"), (B, "HEAD")):
    n, m = h(p)
    print(tag, "bytes=", n, "md5=", m, "lines=", len(open(p, encoding="utf-8", errors="ignore").read().split("\n")))

# 检查关键新文本是否在 HEAD 版中
ka = "族内枚举，v1.3 修正表述"
kb = "v1.3 两级撤账"
kc = "v1.3 撤回 7096 口径"
for p, tag in ((A, "WORK"), (B, "HEAD")):
    t = open(p, encoding="utf-8", errors="ignore").read()
    print(tag, "has_vieta_rewrite=", ka in t, "has_two_level=", kb in t, "has_jobs_retract=", kc in t)
