# -*- coding: utf-8 -*-
"""R3k：从本地 PDF 核对 23 颗未命中 Gaia ID 原文（排除 WebFetch 转录错位）"""
import fitz, io, json, re, os

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)
with io.open(os.path.join(BASE, "paperX_wd_m83e_desi137_coords.json"), "r", encoding="utf-8") as f:
    co = json.load(f)["coords"]
miss = [s for s in cat["samples"] if str(s["gaia_int"]) not in co]
print("miss:", len(miss))

doc = fitz.open(os.path.join(BASE, "_2603.20487.pdf"))
# 附录表从 page 7 起（前面探测 Table1/Appendix）
full = ""
for i in range(6, 12):
    full += doc[i].get_text()
# 提取所有 17-20 位数字（Gaia ID）
ids_pdf = re.findall(r"\b(\d{16,20})\b", full)
print("PDF 提取 ID 数:", len(ids_pdf), "unique:", len(set(ids_pdf)))
# 对每颗 miss 星，找 PDF 中的原文
for s in miss:
    gid = str(s["gaia_int"])
    desi = s["desi_name"]
    # 在 PDF 全文找该 DESI name 附近的数字
    idx = full.find(desi)
    ctx = ""
    if idx >= 0:
        ctx = full[max(0, idx - 120): idx + 20].replace("\n", " ")
    cands = re.findall(r"\d{16,20}", ctx)
    print("%s desi=%s ctx=%s" % (gid, desi, cands[:4]))
