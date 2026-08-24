#!/usr/bin/env python3
"""
修复错误的更名记录脚本

本脚本用于删除论文中错误的更名记录（MUFPF → MUFPF）。
"""

import re
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
    
    # 扫描论文文件
    print("正在扫描论文文件...")
    md_files = sorted(paper_dir.glob('*.md'))
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    print()
    
    # 错误记录的正则表达式
    # 匹配 "| 2026-08-24 | v1.0 | 更名：MUFPF → MUFPF（X 处替换）|" 格式的行
    error_pattern = re.compile(r'^\| 2026-08-24 \| v1\.0 \| 更名：MUFPF → MUFPF.*\|$', re.MULTILINE)
    
    # 处理文件
    print("正在处理文件...")
    fixed_count = 0
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含错误记录
            if 'MUFPF → MUFPF' in content:
                # 删除错误记录
                new_content = error_pattern.sub('', content)
                
                # 清理多余的空行
                new_content = re.sub(r'\n{3,}', '\n\n', new_content)
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  已修复: {file_path.name}")
                fixed_count += 1
        except Exception as e:
            print(f"  错误：无法处理 {file_path.name}: {e}")
    
    print()
    print("=" * 60)
    print("修复完成！")
    print("=" * 60)
    print(f"已修复: {fixed_count} 个文件")


if __name__ == '__main__':
    main()
