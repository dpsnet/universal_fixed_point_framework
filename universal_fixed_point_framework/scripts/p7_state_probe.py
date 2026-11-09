# -*- coding: utf-8 -*-
import io, os, time

A = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\paper\paper_SM_endogenous_derivation.md"
B = r"C:\Users\dps_n\AppData\Local\Temp\head_paper.md"

for p, tag in ((A, "WORK"), (B, "HEAD")):
    st = os.stat(p)
    t = io.open(p, encoding="utf-8", errors="ignore").read()
    print(tag, "mtime=", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)))
    print("  has_origin_narrative=", "框架起源——从脉冲神经网络" in t)
    print("  has_branchA=", "分支 A（活跃步）" in t)
    print("  has_active_process_old=", "活跃过程取活跃步" in t)
    print("  lines=", t.count("\n") + 1)
