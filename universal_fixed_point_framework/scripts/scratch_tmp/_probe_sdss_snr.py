# -*- coding: utf-8 -*-
"""测试 SDSS SkyServer specObj SNR 查询（unverified SSL）。"""
import urllib.request, urllib.parse, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def q(cmd):
    url = "https://skyserver.sdss.org/dr17/SearchTools/sql"
    data = urllib.parse.urlencode({"cmd": cmd, "format": "json"}).encode()
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return "ERR %s" % e

for fld in ["snMedian", "median", "z"]:
    cmd = "SELECT TOP 3 plate, mjd, fiber, %s FROM specObj WHERE ra BETWEEN 334.617 AND 334.621 AND dec BETWEEN -0.005 AND -0.001" % fld
    out = q(cmd)
    print("FLD=%s -> %s" % (fld, out[:500]))
