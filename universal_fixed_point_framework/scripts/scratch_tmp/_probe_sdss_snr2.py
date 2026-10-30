# -*- coding: utf-8 -*-
"""SDSS SkyServer 连通性与字段逐级探测。"""
import urllib.request, urllib.parse, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def q(cmd, fmt="json"):
    url = "https://skyserver.sdss.org/dr17/SearchTools/sql"
    data = urllib.parse.urlencode({"cmd": cmd, "format": fmt}).encode()
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return "ERR %s" % e

print("T1:", q("SELECT TOP 2 plate, mjd, fiber FROM specObj")[:300])
print("T2:", q("SELECT TOP 2 plate, mjd, fiber, snMedian FROM specObj")[:300])
print("T3:", q("SELECT TOP 2 plate, mjd, fiber, median FROM specObj")[:300])
# 若 json 失败试 csv
print("T4:", q("SELECT TOP 2 plate, mjd, fiber FROM specObj WHERE ra BETWEEN 334.617 AND 334.621 AND dec BETWEEN -0.005 AND -0.001", "csv")[:300])
