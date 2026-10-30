# -*- coding: utf-8 -*-
"""快速验证：TARGETID 列偏移修复（不打开 astropy 全文件）"""
import os, sys, time
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("r", r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_m83e_desi_reader.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

t0 = time.time()
d = m.DesiCoadd(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_desi_spec\coadd-main-bright-7110.fits")
print("parse %.2fs" % (time.time() - t0), flush=True)
h = d.hdu("FIBERMAP")
print("TARGETID meta:", h["ttypes"].get("TARGETID"), flush=True)
tid = d.col("FIBERMAP", "TARGETID")
print("TARGETID[0:6]", tid[:6], flush=True)
# 期望 [39633348317942239 39633344996051197 616094097299473103 ...]
exp = [39633348317942239, 39633344996051197, 616094097299473103, 39633344991859141, 39633344996049718, 39633344996049221]
print("match:", list(tid[:6]) == exp, flush=True)
