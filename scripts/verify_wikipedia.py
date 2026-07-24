# -*- coding: utf-8 -*-
"""验证 Wikipedia 语料库并导出样本"""
import os
import pandas as pd

DATA_DIR = r"E:\workspace\hyper-resolution\data\wikipedia"
PARQUET = os.path.join(DATA_DIR, "wikipedia-20231101-simple.parquet")

df = pd.read_parquet(PARQUET)

print(f"文件大小: {os.path.getsize(PARQUET)/1e6:.1f} MB")
print(f"文章数量: {len(df):,}")
print(f"列: {list(df.columns)}")
print(f"总字符数: {df['text'].str.len().sum():,}")
print(f"平均每篇: {df['text'].str.len().mean():.0f} 字符")
print()

# 导出前 5 篇样本
sample_path = os.path.join(DATA_DIR, "sample_articles.txt")
with open(sample_path, "w", encoding="utf-8") as f:
    for _, row in df.head(5).iterrows():
        f.write(f"===== {row['title']} =====\n")
        f.write(row["text"][:1500] + "\n\n")
print(f"样本已导出: {sample_path}")
print()
print("===== 第一篇预览 =====")
print(df.iloc[0]["title"])
print(df.iloc[0]["text"][:400])
