# -*- coding: utf-8 -*-
"""R1-fix3：PDF words 坐标分行提取附录 Table 1（每行 9 字段）"""
import fitz, io, json, os, re

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
doc = fitz.open(os.path.join(BASE, "_2603.20487.pdf"))

records = []
for pg in range(7, 15):
    words = doc[pg].get_text("words")  # (x0,y0,x1,y1,word,...)
    # 按 y0 分桶（容差 3）
    rows_map = {}
    for w in words:
        y = round(w[1] / 3.0) * 3
        rows_map.setdefault(y, []).append(w)
    for y in sorted(rows_map):
        ws = sorted(rows_map[y], key=lambda w: w[0])
        toks = [w[4] for w in ws]
        # 表格行：9 个 token（Gaia ID 16-20 位开头 + DESI 16-20 位）
        if len(toks) == 9 and re.match(r"^\d{16,20}$", toks[0]) and re.match(r"^\d{16,20}$", toks[1]):
            records.append(toks)
        elif len(toks) >= 9 and re.match(r"^\d{16,20}$", toks[0]):
            # 可能有分页表头混入，取前 9
            records.append(toks[:9])

print("records:", len(records))
for r in records[:3] + records[-2:]:
    print(r)
# 校验：B 值范围、G 值
bs = [float(r[4]) for r in records if r[4] != "NA"]
print("B min/max:", min(bs), max(bs), "n_B:", len(bs))
out = {"n": len(records), "rows": records}
with io.open(os.path.join(BASE, "_m83e_pdf_table1.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print("saved")
