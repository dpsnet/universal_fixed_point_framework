# -*- coding: utf-8 -*-
"""读取 JES 玛湖风城组补充材料 xlsx 全部 sheet 内容并打印。"""
import pandas as pd
import os

data_dir = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data"
files = [os.path.join("jes_mahu_fengcheng", "12583_2025_297_MOESM2_ESM.xlsx"),
         os.path.join("jes_mahu_fengcheng", "12583_2025_297_MOESM3_ESM.xlsx")]

for fn in files:
    path = os.path.join(data_dir, fn)
    print("\n" + "#" * 80)
    print(f"FILE: {fn}")
    print("#" * 80)
    xl = pd.ExcelFile(path)
    print(f"Sheets: {xl.sheet_names}")
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, header=None)
        print(f"\n--- Sheet: {sheet} | shape={df.shape} ---")
        # 打印全部内容（前 60 行以内）
        with pd.option_context("display.max_rows", 200, "display.max_columns", 50,
                               "display.width", 250, "display.max_colwidth", 40):
            print(df.to_string())
