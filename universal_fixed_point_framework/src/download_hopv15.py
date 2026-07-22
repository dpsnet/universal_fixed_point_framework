#!/usr/bin/env python3
"""
HOPV15 数据集下载与验证脚本
=============================
下载 Harvard Organic Photovoltaics 2015 数据集
并用谱框架预言对其进行验证。

数据源: Lopez et al., Scientific Data (2016)
         https://doi.org/10.1038/sdata.2016.86
"""

import urllib.request
import json
import os
import sys
import zipfile
import csv
import io

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ZIP_PATH = os.path.join(DATA_DIR, "HOPV15.zip")
EXTRACT_DIR = os.path.join(DATA_DIR, "HOPV15")


def download_hopv15():
    """从 figshare 下载 HOPV15 数据集"""
    if os.path.exists(ZIP_PATH):
        print(f"[已存在] {ZIP_PATH}")
        return True
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 通过 figshare API 获取下载链接
    print("[1/3] 获取 HOPV15 文章信息...")
    api_url = "https://api.figshare.com/v2/articles/1610063"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            article = json.loads(resp.read())
    except Exception as e:
        print(f"  API 访问失败: {e}")
        print("  尝试直接下载...")
        # 备用直接下载链接
        direct_urls = [
            "https://figshare.com/ndownloader/files/4513735",
        ]
        for url in direct_urls:
            try:
                print(f"  尝试: {url}")
                urllib.request.urlretrieve(url, ZIP_PATH)
                print(f"  下载成功: {ZIP_PATH}")
                return True
            except Exception as e2:
                print(f"  失败: {e2}")
        return False
    
    files = article.get("files", [])
    if not files:
        print("  API 未返回文件信息")
        # 尝试 figshare 提供的备用文件系统
        # 使用 figshare 的私人下载端点
        download_url = "https://ndownloader.figshare.com/files/4513735"
        print(f"  尝试直接链接: {download_url}")
        try:
            urllib.request.urlretrieve(download_url, ZIP_PATH)
            print(f"  下载成功: {ZIP_PATH}")
            return True
        except Exception as e:
            print(f"  失败: {e}")
            return False
    
    dl_url = files[0]["download_url"]
    fname = files[0]["name"]
    print(f"  文件: {fname}")
    print(f"  大小: {files[0].get('size', 0) / 1e6:.1f} MB")
    
    print(f"[2/3] 下载 {fname}...")
    try:
        urllib.request.urlretrieve(dl_url, ZIP_PATH)
        print(f"  成功: {ZIP_PATH}")
    except Exception as e:
        print(f"  下载失败: {e}")
        return False
    
    return True


def extract_and_examine():
    """解压并检查 HOPV15 数据内容"""
    if not os.path.exists(ZIP_PATH):
        print("ZIP 文件不存在")
        return None
    
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
            file_list = zf.namelist()
            print(f"\nZIP 内容 ({len(file_list)} 文件):")
            for f in file_list[:20]:
                info = zf.getinfo(f)
                print(f"  {f:<50} {info.file_size:>10} bytes")
            if len(file_list) > 20:
                print(f"  ... 及另外 {len(file_list) - 20} 个文件")
            
            # 查找 CSV 或数据文件
            data_files = [f for f in file_list if f.endswith('.csv') or f.endswith('.txt') or f.endswith('.dat')]
            print(f"\n数据文件 ({len(data_files)} 个):")
            for f in data_files:
                print(f"  {f}")
            
            # 读取第一个 CSV 的前几行
            csv_files = [f for f in data_files if f.endswith('.csv')]
            if csv_files:
                target = csv_files[0]
                print(f"\n预览 {target}:")
                content = zf.read(target).decode('utf-8', errors='replace')
                lines = content.split('\n')
                for i, line in enumerate(lines[:10]):
                    print(f"  {line[:200]}")
            
            # 解压
            print(f"\n解压到 {EXTRACT_DIR}...")
            zf.extractall(EXTRACT_DIR)
            print("  完成")
            
            return csv_files[0] if csv_files else None
    
    except zipfile.BadZipFile:
        print("ZIP 文件损坏，尝试用其他方式读取")
        return None


def process_hopv_data(csv_path):
    """处理 HOPV15 数据，提取实验值用于谱框架验证"""
    full_path = os.path.join(EXTRACT_DIR, csv_path)
    if not os.path.exists(full_path):
        # 尝试直接查找
        for root, dirs, files in os.walk(EXTRACT_DIR):
            for f in files:
                if f.endswith('.csv'):
                    full_path = os.path.join(root, f)
                    break
            else:
                continue
            break
    
    if not os.path.exists(full_path):
        print(f"找不到数据文件: {csv_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"  处理 HOPV15 数据: {full_path}")
    print(f"{'='*60}")
    
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
    print(f"列名 ({len(headers)}):")
    for i, h in enumerate(headers):
        print(f"  [{i}] {h}")
    
    # 读取所有数据并分析
    data_rows = []
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_rows.append(row)
    
    print(f"\n总行数: {len(data_rows)}")
    
    # 寻找关键列
    possible_pce_cols = [h for h in headers if 'pce' in h.lower() or 'efficiency' in h.lower() or 'PCE' in h]
    possible_voc_cols = [h for h in headers if 'voc' in h.lower() or 'open' in h.lower() or 'Voc' in h]
    possible_homo_cols = [h for h in headers if 'homo' in h.lower()]
    possible_lumo_cols = [h for h in headers if 'lumo' in h.lower()]
    possible_gap_cols = [h for h in headers if 'gap' in h.lower() or 'hlgap' in h.lower()]
    
    print(f"\n可能的性能列:")
    print(f"  PCE: {possible_pce_cols}")
    print(f"  Voc: {possible_voc_cols}")
    print(f"  HOMO: {possible_homo_cols}")
    print(f"  LUMO: {possible_lumo_cols}")
    print(f"  HOMO-LUMO Gap: {possible_gap_cols}")
    
    # 提取数值进行统计分析
    numeric_data = {}
    for col in possible_pce_cols + possible_voc_cols + possible_homo_cols + possible_lumo_cols + possible_gap_cols:
        values = []
        for row in data_rows:
            val = row.get(col, '').strip()
            try:
                v = float(val)
                values.append(v)
            except (ValueError, TypeError):
                pass
        if values:
            numeric_data[col] = values
            print(f"\n  {col}:")
            print(f"    N={len(values)}, mean={sum(values)/len(values):.3f}, "
                  f"min={min(values):.3f}, max={max(values):.3f}")
    
    return data_rows, numeric_data


def main():
    print("HOPV15 数据集下载与谱验证")
    print("=" * 60)
    
    # Step 1: 下载
    success = download_hopv15()
    if not success:
        print("\n⚠ 下载失败。将继续使用已有数据（如有）进行分析。")
        print("  可手动下载: https://figshare.com/articles/dataset/HOPV15_Dataset/1610063")
    
    # Step 2: 检查
    if os.path.exists(ZIP_PATH) and os.path.getsize(ZIP_PATH) > 1000:
        csv_file = extract_and_examine()
        if csv_file:
            # Step 3: 处理
            process_hopv_data(csv_file)
    else:
        print(f"\nZIP 文件不存在或过小: {ZIP_PATH}")
        print("检查 data/ 目录...")
        for f in os.listdir(DATA_DIR):
            print(f"  {f}")
    
    print("\n" + "=" * 60)
    print("  完成。如果下载失败，请尝试手动下载并解压到 data/HOPV15/")
    print("=" * 60)


if __name__ == "__main__":
    main()
