# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

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
