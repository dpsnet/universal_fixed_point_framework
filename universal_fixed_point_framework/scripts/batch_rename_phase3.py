#!/usr/bin/env python3
"""
UFPF → MUFPF 批量更名脚本（第三阶段 + 4.2.2路线图）
处理目录: roadmap, notes, learning, README.md
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(r"e:\workspace\hyper-resolution\universal_fixed_point_framework")

# 需要处理的目录列表
TARGET_DIRS = [
    PROJECT_ROOT / "roadmap",
    PROJECT_ROOT / "notes",
    PROJECT_ROOT / "learning",
]

# 需要处理的文件扩展名
FILE_EXTENSIONS = {".md", ".py", ".tex"}

# 排除的文件（更名计划本身不修改）
EXCLUDE_FILES = {"mu_renaming_plan.md"}

# 替换规则 (旧 -> 新)
REPLACEMENTS = [
    # 1. 英文全称替换
    (r"Universal Fixed Point Framework", "Meta-Universal Fixed-Point Functorial Framework"),
    
    # 2. 中文全称替换
    (r"通用不动点范畴框架", "元通用不动点函子范畴框架"),
    
    # 3. 缩写替换（大写）
    ("UFPF", "MUFPF"),
    
    # 4. 命名空间替换
    ("UFPFormalization", "MUFPFormalization"),
    
    # 5. 小写形式替换（用于变量名、文件名等）
    ("ufpf", "mufpf"),
    
    # 6. 混合大小写替换
    ("Ufpf", "Mufpf"),
]

def create_backup(file_path):
    """创建文件备份"""
    backup_dir = PROJECT_ROOT / "backups" / f"phase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    relative_path = file_path.relative_to(PROJECT_ROOT)
    backup_path = backup_dir / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(file_path, backup_path)
    return backup_path

def count_occurrences(content, old_str):
    """统计字符串出现次数"""
    return content.count(old_str)

def apply_replacements(content, file_path):
    """应用所有替换规则，返回替换统计"""
    stats = {}
    modified_content = content
    
    for old, new in REPLACEMENTS:
        count = count_occurrences(modified_content, old)
        if count > 0:
            modified_content = modified_content.replace(old, new)
            stats[f"{old} -> {new}"] = count
    
    return modified_content, stats

def process_file(file_path, dry_run=False):
    """处理单个文件"""
    if file_path.name in EXCLUDE_FILES:
        return None, {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"  [ERROR] 读取文件失败: {e}")
        return None, {}
    
    modified_content, stats = apply_replacements(original_content, file_path)
    
    if not stats:
        return None, {}  # 没有需要替换的内容
    
    if dry_run:
        return None, stats
    
    # 创建备份
    backup_path = create_backup(file_path)
    
    # 写入修改后的内容
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        return backup_path, stats
    except Exception as e:
        print(f"  [ERROR] 写入文件失败: {e}")
        # 恢复备份
        shutil.copy2(backup_path, file_path)
        return None, {}

def process_directory(dir_path, dry_run=False):
    """处理目录下的所有文件"""
    results = {
        "total_files": 0,
        "modified_files": 0,
        "total_replacements": 0,
        "file_details": [],
        "replacement_summary": {}
    }
    
    if not dir_path.exists():
        print(f"  [WARNING] 目录不存在: {dir_path}")
        return results
    
    for file_path in dir_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in FILE_EXTENSIONS:
            results["total_files"] += 1
            
            backup_path, stats = process_file(file_path, dry_run)
            
            if stats:
                results["modified_files"] += 1
                total_in_file = sum(stats.values())
                results["total_replacements"] += total_in_file
                
                # 记录文件详情
                relative_path = file_path.relative_to(PROJECT_ROOT)
                results["file_details"].append({
                    "file": str(relative_path),
                    "replacements": total_in_file,
                    "details": stats
                })
                
                # 更新汇总
                for key, count in stats.items():
                    results["replacement_summary"][key] = results["replacement_summary"].get(key, 0) + count
                
                status = "[DRY-RUN]" if dry_run else "[OK]"
                print(f"  {status} {relative_path}: {total_in_file} 处替换")
    
    return results

def process_readme():
    """处理根目录的 README.md"""
    readme_path = PROJECT_ROOT / "README.md"
    if not readme_path.exists():
        return None, {}
    
    results = {
        "total_files": 1,
        "modified_files": 0,
        "total_replacements": 0,
        "file_details": [],
        "replacement_summary": {}
    }
    
    backup_path, stats = process_file(readme_path)
    
    if stats:
        results["modified_files"] = 1
        total_in_file = sum(stats.values())
        results["total_replacements"] = total_in_file
        
        results["file_details"].append({
            "file": "README.md",
            "replacements": total_in_file,
            "details": stats
        })
        
        for key, count in stats.items():
            results["replacement_summary"][key] = results["replacement_summary"].get(key, 0) + count
        
        print(f"  [OK] README.md: {total_in_file} 处替换")
    
    return results

def generate_report(all_results, output_path):
    """生成更名报告"""
    report_lines = [
        "# UFPF → MUFPF 更名报告（第三阶段 + 4.2.2路线图）",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## 一、处理范围",
        "",
        "| 目录 | 总文件数 | 已修改文件 | 替换次数 |",
        "|------|----------|------------|----------|",
    ]
    
    total_files = 0
    total_modified = 0
    total_replacements = 0
    
    for dir_name, results in all_results.items():
        total_files += results["total_files"]
        total_modified += results["modified_files"]
        total_replacements += results["total_replacements"]
        report_lines.append(f"| {dir_name} | {results['total_files']} | {results['modified_files']} | {results['total_replacements']} |")
    
    report_lines.extend([
        f"| **总计** | **{total_files}** | **{total_modified}** | **{total_replacements}** |",
        "",
        "---",
        "",
        "## 二、替换规则汇总",
        "",
        "| 替换规则 | 替换次数 |",
        "|----------|----------|",
    ])
    
    # 合并所有替换汇总
    combined_summary = {}
    for results in all_results.values():
        for key, count in results["replacement_summary"].items():
            combined_summary[key] = combined_summary.get(key, 0) + count
    
    for rule, count in sorted(combined_summary.items(), key=lambda x: -x[1]):
        report_lines.append(f"| `{rule}` | {count} |")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## 三、修改文件列表",
        "",
    ])
    
    for dir_name, results in all_results.items():
        if results["file_details"]:
            report_lines.append(f"### {dir_name}")
            report_lines.append("")
            for detail in sorted(results["file_details"], key=lambda x: -x["replacements"]):
                report_lines.append(f"- `{detail['file']}`: {detail['replacements']} 处替换")
            report_lines.append("")
    
    report_lines.extend([
        "---",
        "",
        "## 四、备份信息",
        "",
        f"所有原始文件已备份至: `backups/phase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}/`",
        "",
        "---",
        "",
        "*本报告由批量更名脚本自动生成*"
    ])
    
    report_content = "\n".join(report_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return output_path

def main():
    """主函数"""
    print("=" * 60)
    print("UFPF → MUFPF 批量更名脚本")
    print("=" * 60)
    print()
    
    # 检查是否为 dry-run 模式
    dry_run = "--dry-run" in os.sys.argv
    if dry_run:
        print("[DRY-RUN 模式] 仅统计替换数量，不实际修改文件")
        print()
    
    all_results = {}
    
    # 处理各目录
    for target_dir in TARGET_DIRS:
        dir_name = target_dir.name
        print(f"处理目录: {dir_name}")
        print("-" * 40)
        
        results = process_directory(target_dir, dry_run)
        all_results[dir_name] = results
        
        print(f"  统计: {results['modified_files']}/{results['total_files']} 文件已修改, {results['total_replacements']} 处替换")
        print()
    
    # 处理 README.md
    print("处理文件: README.md")
    print("-" * 40)
    readme_results = process_readme()
    if readme_results:
        all_results["README.md"] = readme_results
        print(f"  统计: {readme_results['modified_files']}/{readme_results['total_files']} 文件已修改, {readme_results['total_replacements']} 处替换")
    print()
    
    # 生成报告
    if not dry_run:
        report_path = PROJECT_ROOT / "rename_report_phase3.md"
        generate_report(all_results, report_path)
        print(f"更名报告已生成: {report_path}")
    
    # 打印汇总
    print()
    print("=" * 60)
    print("处理完成!")
    print("=" * 60)
    
    total_files = sum(r["total_files"] for r in all_results.values())
    total_modified = sum(r["modified_files"] for r in all_results.values())
    total_replacements = sum(r["total_replacements"] for r in all_results.values())
    
    print(f"总文件数: {total_files}")
    print(f"已修改文件: {total_modified}")
    print(f"总替换次数: {total_replacements}")

if __name__ == "__main__":
    main()
