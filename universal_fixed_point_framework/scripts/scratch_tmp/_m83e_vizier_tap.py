# -*- coding: utf-8 -*-
"""R3j：VizieR TAP 查 DESI MWD 目录（含坐标）"""
import requests

# 1) 查 TAP 元数据里匹配的目录
queries = [
    "SELECT catalog_name, description FROM TAP_SCHEMA.catalogues WHERE description LIKE '%magnetic white dwarf%'",
    "SELECT table_name, description FROM TAP_SCHEMA.tables WHERE description LIKE '%magnetic white dwarf%' OR table_name LIKE '%desi%'",
]
for q in queries:
    r = requests.post("https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync",
                      data={"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json",
                            "QUERY": q}, timeout=60)
    print(q[:50], "->", r.status_code)
    if r.status_code == 200:
        print(r.text[:800])
