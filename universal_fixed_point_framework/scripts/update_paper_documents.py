#!/usr/bin/env python3
"""
UFPF → MUFPF 学术文档批量更新脚本

本脚本用于第二阶段：批量更新 Paper I-XLIV 中的文本。
脚本会根据更名计划文档中的规范，自动替换论文中的 UFPF 相关文本。

替换规则（基于 roadmap/mu_renaming_plan.md）：

1. 学术引用格式：
   - 旧：UFPF (Universal Fixed Point Framework)
   - 新：MUFPF (Meta-Universal Fixed-Point Functorial Framework)

2. 论文标题格式：
   - 旧：通用不动点范畴框架（UFPF）
   - 新：元通用不动点函子范畴框架（MUFPF）

3. 缩写使用：
   - UFPF → MUFPF（独立出现时）
   - ufpf → mufpf（代码/变量名中）

4. 首次出现处理：
   - 在文档开头添加更名说明注释

使用方法：
    python update_paper_documents.py [--dry-run] [--directory DIR] [--backup]

参数：
    --dry-run     仅显示将要修改的内容，不实际修改
    --directory   指定扫描的目录（默认为 paper 目录）
    --backup      创建备份文件（.bak）

脚本位置：universal_fixed_point_framework/scripts/update_paper_documents.py
关联文档：roadmap/mu_renaming_plan.md
"""

import re
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================
# 替换规则配置（基于更名计划文档）
# ============================================================

# 规则 1: 学术引用格式（完整形式）
ACADEMIC_CITATION_RULES = [
    # 英文完整引用
    (r'UFPF\s*\(\s*Universal\s+Fixed\s+Point\s+Framework\s*\)',
     'MUFPF (Meta-Universal Fixed-Point Functorial Framework)'),
    # 英文引用变体（可能有不同空格）
    (r'UFPF\s*\(Universal Fixed Point Framework\)',
     'MUFPF (Meta-Universal Fixed-Point Functorial Framework)'),
    # 中文完整引用（带括号）
    (r'通用不动点范畴框架（UFPF）',
     '元通用不动点函子范畴框架（MUFPF）'),
    # 中文引用变体（带括号）
    (r'通用不动点框架（UFPF）',
     '元通用不动点函子范畴框架（MUFPF）'),
    # 中文名称单独出现（不带括号）
    (r'通用不动点范畴框架',
     '元通用不动点函子范畴框架'),
    # 中文名称变体（不带括号）
    (r'通用不动点框架',
     '元通用不动点函子范畴框架'),
]

# 规则 2: 独立缩写替换（UFPF → MUFPF）
# 使用单词边界或中文字符边界，避免替换已经是 MUFPF 的情况
# 注意：需要排除 MUFPF 中的 UFPF，使用负向后顾
ABBREVIATION_RULES = [
    # 英文缩写（独立出现，不是 MUFPF 的一部分，也不是 UFPFormalization 的一部分）
    # 使用负向后顾排除 M/m 开头的情况
    # 使用负向前瞻排除 F 结尾的情况，但允许中文字符
    (r'(?<![Mm])UFPF(?![FfA-Za-z])', 'MUFPF'),
    # 小写缩写（代码/变量名中）
    (r'(?<![Mm])ufpf(?![fa-z])', 'mufpf'),
    # UFPFormalization → MUFPFormalization
    (r'(?<![Mm])UFPFormalization\b', 'MUFPFormalization'),
    (r'(?<![Mm])ufpformalization\b', 'mufpformalization'),
]

# 规则 3: 特定术语替换
TERM_RULES = [
    # UFPF 理论
    (r'UFPF\s+理论', 'MUFPF 理论'),
    (r'UFPF\s+框架', 'MUFPF 框架'),
    (r'UFPF\s+体系', 'MUFPF 体系'),
    (r'UFPF\s+形式化', 'MUFPF 形式化'),
    # 英文术语
    (r'UFPF\s+theory', 'MUFPF theory'),
    (r'UFPF\s+framework', 'MUFPF framework'),
    (r'UFPF\s+formalization', 'MUFPF formalization'),
]

# 注意：不再在论文正文中添加更名通知
# 更名通知已单独创建为 paper/RENAME_NOTICE.md


def compile_rules():
    """编译所有替换规则为正则表达式对象。"""
    compiled_rules = []
    
    # 学术引用格式（优先级最高，先匹配）
    for pattern, replacement in ACADEMIC_CITATION_RULES:
        compiled_rules.append((re.compile(pattern, re.IGNORECASE), replacement))
    
    # 特定术语
    for pattern, replacement in TERM_RULES:
        compiled_rules.append((re.compile(pattern, re.IGNORECASE), replacement))
    
    # 独立缩写（优先级最低，最后匹配）
    for pattern, replacement in ABBREVIATION_RULES:
        compiled_rules.append((re.compile(pattern, re.IGNORECASE), replacement))
    
    return compiled_rules


def has_rename_notice(content: str) -> bool:
    """检查文档是否已有更名通知。"""
    return '更名通知' in content[:500]  # 只检查前500字符


def apply_replacements(content: str, compiled_rules: list) -> tuple:
    """
    应用所有替换规则。
    
    Returns:
        (替换后的内容, 替换计数)
    """
    total_replacements = 0
    
    for pattern, replacement in compiled_rules:
        new_content, count = pattern.subn(replacement, content)
        if count > 0:
            total_replacements += count
            content = new_content
    
    return content, total_replacements


def update_document(file_path: Path, compiled_rules: list, 
                   dry_run: bool = False, backup: bool = False) -> dict:
    """
    更新单个文档。
    
    Args:
        file_path: 文件路径
        compiled_rules: 编译后的替换规则
        dry_run: 仅显示修改，不实际执行
        backup: 创建备份文件
        
    Returns:
        处理结果字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'reason': str(e),
            'replacements': 0
        }
    
    # 应用替换规则
    new_content, replacements = apply_replacements(original_content, compiled_rules)
    
    # 检查是否需要添加变更记录（即使没有新的替换）
    needs_change_log = '## 变更记录' not in new_content and 'MUFPF' in new_content
    
    # 如果没有替换且不需要添加变更记录，跳过
    if replacements == 0 and not needs_change_log:
        return {
            'file': str(file_path),
            'status': 'skipped',
            'reason': 'no_ufpf_found',
            'replacements': 0
        }
    
    # 添加更名操作记录（只要文件包含 MUFPF 且没有更名记录）
    if needs_change_log or replacements > 0:
        # 更名记录行
        rename_record = f"| 2026-08-24 | v1.0 | 更名：UFPF → MUFPF（{replacements} 处替换）|"
        
        # 检查是否已有变更记录部分（支持多种格式）
        change_log_patterns = ['## 变更记录', '**变更记录**', '变更记录：']
        has_change_log = any(pattern in new_content for pattern in change_log_patterns)
        
        if has_change_log:
            # 在变更记录表格的最后一行后添加新记录
            # 查找变更记录表格的最后一行（以 | 结尾的行）
            lines = new_content.split('\n')
            last_table_line_idx = -1
            in_change_log = False
            
            for i, line in enumerate(lines):
                # 检测变更记录部分的开始
                if any(pattern in line for pattern in change_log_patterns):
                    in_change_log = True
                elif in_change_log and line.strip().startswith('|') and not any(header in line for header in ['日期', '版本', '---']):
                    last_table_line_idx = i
            
            if last_table_line_idx >= 0:
                # 在最后一行后插入新记录
                lines.insert(last_table_line_idx + 1, rename_record)
                new_content = '\n'.join(lines)
        else:
            # 没有变更记录部分，创建一个新的
            change_log = f"""

---

## 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
{rename_record}

> 更名原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
> 新名称 MUFPF (Meta-Universal Fixed-Point Functorial Framework) 具有全球唯一性。
> 详见：[更名通知](RENAME_NOTICE.md) | [更名计划](../roadmap/mu_renaming_plan.md)
"""
            # 确保文件末尾有换行符
            if not new_content.endswith('\n'):
                new_content += '\n'
            new_content += change_log
    
    if dry_run:
        return {
            'file': str(file_path),
            'status': 'would_modify',
            'replacements': replacements,
            'preview': new_content[:200] + '...'
        }
    
    # 创建备份
    if backup:
        backup_path = file_path.with_suffix('.md.bak')
        shutil.copy2(file_path, backup_path)
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return {
            'file': str(file_path),
            'status': 'modified',
            'replacements': replacements
        }
    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'reason': str(e),
            'replacements': replacements
        }


def generate_report(results: list, output_file: Path = None) -> str:
    """
    生成更新报告。
    
    Args:
        results: 处理结果列表
        output_file: 报告输出文件路径
        
    Returns:
        报告内容
    """
    # 统计数据
    total_files = len(results)
    modified_files = sum(1 for r in results if r['status'] == 'modified')
    skipped_files = sum(1 for r in results if r['status'] == 'skipped')
    error_files = sum(1 for r in results if r['status'] == 'error')
    would_modify_files = sum(1 for r in results if r['status'] == 'would_modify')
    total_replacements = sum(r.get('replacements', 0) for r in results)
    
    # 生成报告
    report = f"""# UFPF → MUFPF 学术文档更新报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**脚本**: update_paper_documents.py
**关联文档**: roadmap/mu_renaming_plan.md
**阶段**: 第二阶段 - 学术文档更新

---

## 一、总体统计

| 指标 | 数量 |
|------|------|
| 扫描文件总数 | {total_files} |
| 已修改文件数 | {modified_files} |
| 跳过文件数 | {skipped_files} |
| 错误文件数 | {error_files} |
| 将要修改文件数（dry-run） | {would_modify_files} |
| 替换总数 | {total_replacements} |

---

## 二、替换规则

### 2.1 学术引用格式

| 旧格式 | 新格式 |
|--------|--------|
| UFPF (Universal Fixed Point Framework) | MUFPF (Meta-Universal Fixed-Point Functorial Framework) |
| 通用不动点范畴框架（UFPF） | 元通用不动点函子范畴框架（MUFPF） |

### 2.2 缩写替换

| 旧格式 | 新格式 |
|--------|--------|
| UFPF | MUFPF |
| ufpf | mufpf |
| UFPFormalization | MUFPFormalization |

### 2.3 特定术语

| 旧格式 | 新格式 |
|--------|--------|
| UFPF 理论 | MUFPF 理论 |
| UFPF 框架 | MUFPF 框架 |
| UFPF 体系 | MUFPF 体系 |

---

## 三、详细文件列表

### 已修改文件
"""
    
    modified_list = [r for r in results if r['status'] == 'modified']
    if modified_list:
        for r in sorted(modified_list, key=lambda x: x['file']):
            report += f"- {Path(r['file']).name} (替换: {r['replacements']})\n"
    else:
        report += "- 无\n"
    
    report += """
### 跳过文件
"""
    
    skipped_list = [r for r in results if r['status'] == 'skipped']
    if skipped_list:
        for r in sorted(skipped_list, key=lambda x: x['file']):
            report += f"- {Path(r['file']).name}\n"
    else:
        report += "- 无\n"
    
    report += """
### 错误文件
"""
    
    error_list = [r for r in results if r['status'] == 'error']
    if error_list:
        for r in sorted(error_list, key=lambda x: x['file']):
            report += f"- {Path(r['file']).name}: {r['reason']}\n"
    else:
        report += "- 无\n"
    
    report += """
---

## 四、下一步行动

1. **验证更新结果**：检查更新后的文档是否正确
2. **第三阶段**：更新研究笔记
3. **第四阶段**：文档发布
4. **第五阶段**：代码批量更名与验证

---

*报告由 update_paper_documents.py 自动生成*
"""
    
    # 保存报告
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {output_file}")
    
    return report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='批量更新学术文档中的 UFPF 文本'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要修改的内容，不实际修改'
    )
    parser.add_argument(
        '--directory',
        type=str,
        default=None,
        help='指定扫描的目录（默认为 paper 目录）'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='创建备份文件（.bak）'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='paper_update_report.md',
        help='报告输出文件路径（默认：paper_update_report.md）'
    )
    
    args = parser.parse_args()
    
    # 确定项目根目录
    project_root = Path(__file__).parent.parent
    
    # 确定论文目录
    if args.directory:
        paper_dir = Path(args.directory)
    else:
        paper_dir = project_root / 'paper'
    
    print(f"项目根目录: {project_root}")
    print(f"论文目录: {paper_dir}")
    print(f"扫描模式: {'dry-run' if args.dry_run else '实际修改'}")
    print(f"创建备份: {'是' if args.backup else '否'}")
    print()
    
    # 检查论文目录是否存在
    if not paper_dir.exists():
        print(f"错误：论文目录不存在: {paper_dir}")
        return
    
    # 编译替换规则
    print("正在编译替换规则...")
    compiled_rules = compile_rules()
    print(f"已编译 {len(compiled_rules)} 条规则")
    print()
    
    # 扫描论文文件
    print("正在扫描论文文件...")
    md_files = sorted(paper_dir.glob('*.md'))
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    print()
    
    # 处理文件
    print("正在处理文件...")
    results = []
    for i, file_path in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] 处理: {file_path.name}")
        result = update_document(file_path, compiled_rules, 
                               dry_run=args.dry_run, backup=args.backup)
        results.append(result)
    
    print()
    
    # 生成报告
    report_file = project_root / args.output
    report = generate_report(results, report_file)
    
    # 显示摘要
    print("=" * 60)
    print("处理完成！")
    print("=" * 60)
    
    modified_count = sum(1 for r in results if r['status'] == 'modified')
    skipped_count = sum(1 for r in results if r['status'] == 'skipped')
    error_count = sum(1 for r in results if r['status'] == 'error')
    total_replacements = sum(r.get('replacements', 0) for r in results)
    
    print(f"已修改: {modified_count} 个文件")
    print(f"已跳过: {skipped_count} 个文件")
    print(f"错误: {error_count} 个文件")
    print(f"替换总数: {total_replacements}")
    print()
    print(f"详细报告: {report_file}")
    
    # 显示修改的文件列表
    if modified_count > 0:
        print()
        print("已修改的文件：")
        for r in results:
            if r['status'] == 'modified':
                print(f"  - {Path(r['file']).name} (替换: {r['replacements']})")


if __name__ == '__main__':
    main()
