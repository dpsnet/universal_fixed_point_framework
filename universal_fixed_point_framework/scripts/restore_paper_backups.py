#!/usr/bin/env python3
"""
恢复论文备份文件脚本

本脚本用于恢复 paper 目录下的所有 .bak 备份文件。
"""

import shutil
from pathlib import Path


def main():
    """主函数"""
    # 确定项目根目录
    project_root = Path(__file__).parent.parent
    paper_dir = project_root / 'paper'
    
    print(f"项目根目录: {project_root}")
    print(f"论文目录: {paper_dir}")
    print()
    
    # 检查论文目录是否存在
    if not paper_dir.exists():
        print(f"错误：论文目录不存在: {paper_dir}")
        return
    
    # 扫描备份文件
    print("正在扫描备份文件...")
    bak_files = sorted(paper_dir.glob('*.bak'))
    print(f"找到 {len(bak_files)} 个备份文件")
    print()
    
    # 恢复备份
    print("正在恢复备份...")
    restored_count = 0
    for bak_file in bak_files:
        # 计算原始文件路径
        original_file = bak_file.with_suffix('')
        
        # 恢复备份
        try:
            shutil.copy2(bak_file, original_file)
            print(f"  已恢复: {bak_file.name} -> {original_file.name}")
            restored_count += 1
        except Exception as e:
            print(f"  错误：无法恢复 {bak_file.name}: {e}")
    
    print()
    print("=" * 60)
    print("恢复完成！")
    print("=" * 60)
    print(f"已恢复: {restored_count} 个文件")


if __name__ == '__main__':
    main()
