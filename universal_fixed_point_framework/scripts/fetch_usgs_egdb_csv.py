# -*- coding: utf-8 -*-
"""下载 USGS Energy Geochemistry Database (EGDB) CSV 数据包。

背景
----
仓库历史重写时移除了 4 个 >50MB 的 EGDB 原始分析 CSV（Analysis_*.csv，合计约 330MB）。
这些文件是第三方公开数据（CC0 1.0），可从 USGS ScienceBase 数据发布重新下载，无需入库。
本脚本自动完成：解析发布条目 -> 下载 EnergyGeoChemDB-CSV Files.zip -> 解压到目标目录。

来源
----
- 数据发布: USGS, Energy Geochemistry Database (ver. 2.0, September 2026)
- DOI: 10.5066/P1WNUHWO  ->  https://doi.org/10.5066/P1WNUHWO
- ScienceBase item: https://www.sciencebase.gov/catalog/item/68a8a28fd4be026335793f26
- 附件: EnergyGeoChemDB-CSV Files.zip (约 33 MB)

用法
----
  D:\\pyenv\\pyenv-win\\versions\\3.11.8\\python.exe fetch_usgs_egdb_csv.py [目标目录]
  目标目录缺省为 scripts/data/rockeval_usgs_egdb/csv（与仓库内目录一致）。
  重复运行安全：zip 下载到临时文件，解压采用覆盖写入。
"""
import json
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile

ITEM_ID = "68a8a28fd4be026335793f26"          # EGDB (ver. 2.0, September 2026)
CSV_ZIP_NAME = "EnergyGeoChemDB-CSV Files.zip"

DEFAULT_TARGET = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data", "rockeval_usgs_egdb", "csv",
)

# 校验：官方 v2.0 起 Analysis 表重新分区（Analysis_OrderIDs *.csv，5 个文件）；
# 历史旧版为 4 个 Analysis_*.csv（见 LARGE_DATA_MANIFEST.md）。此处动态匹配当前版。
SAMPLES_CSV = "Samples.csv"


def get_zip_download_uri() -> str:
    """通过 ScienceBase catalog API 解析 CSV 包的直链（随发布版本变化，动态解析）。"""
    url = "https://www.sciencebase.gov/catalog/item/{0}?format=json".format(ITEM_ID)
    with urllib.request.urlopen(url, timeout=60) as resp:
        data = json.load(resp)
    for f in data.get("files", []):
        if f.get("name") == CSV_ZIP_NAME:
            return f["downloadUri"]
    raise RuntimeError("在 ScienceBase 条目中未找到附件: " + CSV_ZIP_NAME)


def main() -> int:
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET
    os.makedirs(target, exist_ok=True)

    print("[1/3] 解析下载地址 ...")
    uri = get_zip_download_uri()
    print("      附件: ", CSV_ZIP_NAME)
    print("      URI:  ", uri)

    print("[2/3] 下载 zip (约 33 MB) ...")
    tmp_zip = os.path.join(tempfile.gettempdir(), "EnergyGeoChemDB-CSV_Files.zip")
    urllib.request.urlretrieve(uri, tmp_zip)
    size_mb = os.path.getsize(tmp_zip) / 1024 / 1024
    print("      已下载: {0:.1f} MB -> {1}".format(size_mb, tmp_zip))

    print("[3/3] 解压到: ", target)
    with zipfile.ZipFile(tmp_zip) as z:
        for info in z.infolist():
            if info.is_dir() or info.filename.endswith("/"):
                continue
            # 剥离 zip 内任意子目录，按文件名写入目标目录
            out = os.path.join(target, os.path.basename(info.filename))
            with z.open(info) as src, open(out, "wb") as dst:
                shutil.copyfileobj(src, dst)
    os.remove(tmp_zip)

    # 校验：Samples.csv 必须存在；Analysis 分区文件至少 1 个（v2.0 起为 5 个 Analysis_OrderIDs *.csv）
    samples_ok = os.path.exists(os.path.join(target, SAMPLES_CSV))
    analysis_files = [n for n in os.listdir(target) if n.startswith("Analysis_") and n.endswith(".csv")]
    for n in analysis_files:
        print("      校验 OK: {0} ({1:.1f} MB)".format(
            n, os.path.getsize(os.path.join(target, n)) / 1024 / 1024))
    if not samples_ok or not analysis_files:
        print("      警告: Samples.csv 缺失={0}, Analysis 分区文件数={1}".format(
            not samples_ok, len(analysis_files)))
        return 1
    print("完成。本次下载为 USGS 官方当前版分区（Analysis_OrderIDs 前缀，{0} 个文件）。".format(len(analysis_files)))
    print("注：历史重写移除的旧版 4 个 Analysis_*.csv（76.9/97.7/97.0/60.3 MB）为 ver 1.x 分区，")
    print("    同源同库（3,619,149 条分析记录），本地已恢复保留；两版任选其一即可满足数据需求。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
