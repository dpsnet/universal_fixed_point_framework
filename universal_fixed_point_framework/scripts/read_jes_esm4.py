# -*- coding: utf-8 -*-
"""读取 JES 玛湖风城组补充材料 MOESM4 xlsx 全部内容。"""
import pandas as pd

path = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\jes_mahu_fengcheng\12583_2025_297_MOESM4_ESM.xlsx"
xl = pd.ExcelFile(path)
print(f"Sheets: {xl.sheet_names}")
for sheet in xl.sheet_names:
    df = xl.parse(sheet, header=None)
    print(f"\n--- Sheet: {sheet} | shape={df.shape} ---")
    with pd.option_context("display.max_rows", 300, "display.max_columns", 60,
                           "display.width", 300, "display.max_colwidth", 40):
        print(df.to_string())
