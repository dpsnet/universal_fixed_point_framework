# -*- coding: utf-8 -*-
import sys, time, os
sys.path.insert(0, r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts")
t0 = time.time()
print("step1 import reader", flush=True)
import importlib.util
spec = importlib.util.spec_from_file_location("rr", r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_m83e_desi_reader.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("step2 module loaded %.1fs" % (time.time() - t0), flush=True)
t1 = time.time()
d = m.DesiCoadd(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_desi_spec\coadd-main-bright-7110.fits")
print("step3 parse done %.1fs hdus=%d" % (time.time() - t1, len(d.hdus)), flush=True)
print("step4 hdu names:", [h["name"] for h in d.hdus[:6]], flush=True)
