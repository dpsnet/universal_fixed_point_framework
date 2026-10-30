# -*- coding: utf-8 -*-
"""从 m83c_sample_list.json 取前 3 颗 name + 测试 SDSS specObj SNR 查询。"""
import io, json, os, re

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
with io.open(os.path.join(BASE, "paperX_wd_m83c_sample_list.json"), "r", encoding="utf-8") as f:
    lst = json.load(f)
print("total", len(lst))
for r in lst[:3]:
    print(r)
# 解析 SDSS 名（JHHMMSS.ss+DDMMSS.s）为度
def name_to_deg(name):
    # 形如 J114720.11+213456.7 或 J114720.11+213456.7 或 J114720+213456
    m = re.match(r"^J(\d{2})(\d{2})(\d{2}(?:\.\d+)?)([+-])(\d{2})(\d{2})(\d{2}(?:\.\d+)?)$", name)
    if not m:
        return None, None
    ra_h, ra_m, ra_s, sign, de_d, de_m, de_s = m.groups()
    ra = (int(ra_h)*15 + int(ra_m)*15/60 + float(ra_s)*15/3600)
    dec = (int(de_d) + int(de_m)/60 + float(de_s)/3600) * (1 if sign == "+" else -1)
    return ra, dec

for r in lst[:3]:
    ra, dec = name_to_deg(r["name"])
    print(r["name"], "->", ra, dec)
